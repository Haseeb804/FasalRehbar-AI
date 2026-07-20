"""
Preprocessing that exactly mirrors the KisanBid training notebooks'
`val_transform` — this MUST stay in sync with the notebooks, since a mismatch
here (different resize, different normalization) silently degrades accuracy
without throwing any error.
"""
import numpy as np
from PIL import Image

import albumentations as A
from albumentations.pytorch import ToTensorV2

IMG_SIZE = 224
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

val_transform = A.Compose([
    A.Resize(IMG_SIZE, IMG_SIZE),
    A.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ToTensorV2(),
])


def load_image_tensor(image_path, device):
    """
    Load an image file and return (image_rgb_ndarray, (1, 3, 224, 224) tensor).

    Pillow is used for opening so any format it supports — including .jfif, .webp,
    .bmp, etc. — works transparently. The explicit .convert("RGB") also handles
    RGBA PNGs and paletted images without error.
    """
    image_rgb = np.array(Image.open(image_path).convert("RGB"))
    tensor = val_transform(image=image_rgb)["image"].unsqueeze(0).to(device)
    return image_rgb, tensor

