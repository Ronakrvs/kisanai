"""
Training script for crop disease detection model.

Dataset: PlantVillage (download from Kaggle)
Model: YOLOv8n-cls (classification)

Steps:
1. Download dataset: kaggle datasets download -d abdallahalidev/plantvillage-dataset
2. Unzip and organize into train/val folders
3. Run this script
4. Export to ONNX
"""

from ultralytics import YOLO


def train():
    model = YOLO("yolov8n-cls.pt")

    results = model.train(
        data="data/",       # path to PlantVillage dataset
        epochs=100,
        imgsz=224,          # classification uses smaller images
        batch=32,
        device="cpu",       # use "0" for GPU
        project="runs/classify",
        name="disease_v1",
        patience=15,
        lr0=0.001,
    )
    print("Training complete:", results)


def export():
    model = YOLO("runs/classify/disease_v1/weights/best.pt")
    model.export(format="onnx", imgsz=224, dynamic=False)
    print("Exported to ONNX. Move best.onnx to models/disease_model.onnx")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        export()
    else:
        train()
