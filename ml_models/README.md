# ML Model Weights — where to put your Colab-trained files

This folder is where the app loads its models from at runtime. Copy the files from your
`MyDrive/KisanBid_Data/saved_models/` folder into this folder, keeping the **exact same names and layout**
your training notebooks already produced. Nothing needs renaming if you copy the whole `saved_models/`
folder contents in as-is.

```
ml_models/
├── classification/
│   ├── effnet_b0_best.pth        <- from Notebook 0 (Crop Classifier)
│   └── eval_metrics.json         <- from Notebook 0 (used to read crop class names/order)
│
└── disease/
    ├── mango_effnet_b0_best.pth              <- from KisanBid_Mango_Disease.ipynb
    ├── mango_eval_summary.json               <- from the same notebook (Section 4)
    ├── yolov8s_cls_mango/weights/best.pt      <- from the same notebook (Section 3)
    │
    ├── onion_effnet_b0_best.pth
    ├── onion_eval_summary.json
    ├── yolov8s_cls_onion/weights/best.pt
    │
    ├── sugarcane_effnet_b0_best.pth
    ├── sugarcane_eval_summary.json
    └── yolov8s_cls_sugarcane/weights/best.pt
```

## Why the `.json` files matter

`eval_metrics.json` and `*_eval_summary.json` aren't just metrics — they also record the **exact class
list and order** each model was trained with (the `"classes"` key). The app reads these to know which
index in the model's output corresponds to which crop/disease name, so it doesn't need you to
retype/guess the class list by hand (and can't get it wrong due to a typo).

**After copying your files in, run:**

```bash
python manage.py sync_ml_metadata
```

This reads those JSON files and creates/updates the `Crop` and `Disease` rows in the database to match
exactly what your models can predict — including "Healthy" — without overwriting any knowledge-base text
(description/symptoms/treatment/etc.) you've already filled in for existing diseases.

Then, optionally, run:

```bash
python manage.py seed_disease_content
```

This fills in **draft** knowledge-base content (symptoms, causes, organic/chemical treatment, prevention,
severity) for commonly-known disease names, so you're not starting from a completely blank admin panel.
**Review and edit this content before relying on it in production** — it's a reasonable starting draft,
not verified agricultural advice.

## Notes

- If a weight file is missing, the app **does not crash** — it logs a clear warning and that specific
  model is skipped (e.g. if only EfficientNet is present but not YOLOv8s-cls, the app falls back to
  EfficientNet-only predictions for that crop).
- `ML_DEVICE` in your `.env` controls whether inference runs on CPU or GPU (`cpu` or `cuda`). Most
  production Django servers don't have a GPU attached — CPU inference works fine for a single-image
  request, just slower (typically 1-3 seconds per image) than the Colab GPU training environment.
