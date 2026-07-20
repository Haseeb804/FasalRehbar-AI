"""
detection.ml — real inference engine for PakAgri.

Loads the EfficientNet-B0 crop classifier and, per crop, the EfficientNet-B0 +
YOLOv8s-cls disease-classification ensemble trained in the KisanBid Colab notebooks.

See ml_models/README.md for where to place the trained weight files.
"""
