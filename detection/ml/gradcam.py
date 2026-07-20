"""
Grad-CAM "affected region" visualization.

IMPORTANT — read before trusting this for anything precise: this is NOT a trained
object detector. Your training datasets only have whole-image disease labels (no
bounding-box annotations), so a real trained detector isn't possible from this data.
What this DOES give you: a heatmap of where the EfficientNet-B0 model's attention was
strongest when making its prediction, converted into an approximate bounding box by
thresholding that heatmap. Treat the box as "roughly where the model is focusing," not
a precise lesion boundary. A real trained detector would need manually annotated
bounding boxes on a representative subset of images.
"""
import logging

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

logger = logging.getLogger("pakagri.ml")


class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.gradients = None
        self.activations = None
        target_layer.register_forward_hook(self._save_activation)
        target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, input, output):
        self.activations = output.detach()

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate(self, input_tensor, class_idx):
        self.model.zero_grad()
        output = self.model(input_tensor)
        score = output[0, class_idx]
        score.backward()

        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * self.activations).sum(dim=1, keepdim=True)
        cam = F.relu(cam)
        cam = cam.squeeze().cpu().numpy()

        cam = cam - cam.min()
        cam = cam / (cam.max() + 1e-8)
        return cam


def generate_analysis_image(image_path, effnet_model, class_idx, label, confidence,
                             output_path, threshold=0.5):
    """
    Builds a 3-panel image (original | heatmap overlay | approximate box) and saves
    it to output_path. Returns True on success, False if it couldn't be generated
    (e.g. no EfficientNet model available — Grad-CAM needs conv layer access, which
    YOLO's classification head doesn't expose in the same way).
    """
    try:
        image_rgb = np.array(Image.open(image_path).convert("RGB"))
        from .transforms import val_transform
        tensor = val_transform(image=image_rgb)["image"].unsqueeze(0)
        tensor = tensor.to(next(effnet_model.parameters()).device)

        target_layer = effnet_model.conv_head  # final conv layer of timm's efficientnet_b0
        cam_engine = GradCAM(effnet_model, target_layer)
        cam = cam_engine.generate(tensor, class_idx)

        h, w = image_rgb.shape[:2]
        cam_resized = cv2.resize(cam, (w, h))

        heatmap_color = cv2.applyColorMap(np.uint8(255 * cam_resized), cv2.COLORMAP_JET)
        heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)
        overlay = np.uint8(0.55 * image_rgb + 0.45 * heatmap_color)

        mask = (cam_resized >= threshold).astype(np.uint8)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        boxed = image_rgb.copy()
        if contours:
            largest = max(contours, key=cv2.contourArea)
            x, y, bw, bh = cv2.boundingRect(largest)
            cv2.rectangle(boxed, (x, y), (x + bw, y + bh), (255, 0, 0), 3)
            cv2.putText(boxed, f"{label} {confidence * 100:.1f}%",
                        (x, max(y - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Stack the 3 panels side by side into one image
        panels = [image_rgb, overlay, boxed]
        target_h = min(p.shape[0] for p in panels)
        resized_panels = []
        for p in panels:
            scale = target_h / p.shape[0]
            new_w = int(p.shape[1] * scale)
            resized_panels.append(cv2.resize(p, (new_w, target_h)))
        combined = np.concatenate(resized_panels, axis=1)

        Image.fromarray(combined).save(output_path, quality=90)
        return True
    except Exception:
        logger.exception("Grad-CAM analysis image generation failed for %s", image_path)
        return False
