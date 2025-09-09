import os
import argparse
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from ultralytics import YOLO
from PIL import Image

def prepare_dataset(csv_path, images_dir, out_dir="datasets/tapas", val_split=0.2):
    """
    Prepara dataset en formato YOLO a partir de un CSV (tipo VIA/VGG) con anotaciones.
    """

    # Leer CSV
    df = pd.read_csv(csv_path)

    # Extraer clase desde region_attributes
    if "region_attributes" in df.columns:
        def extract_class(val):
            try:
                data = json.loads(val.replace("'", "\""))
                return data.get("type", None)
            except:
                return None
        df["class"] = df["region_attributes"].apply(extract_class)

    # Extraer bounding boxes desde region_shape_attributes
    if "region_shape_attributes" in df.columns:
        def extract_bbox(val):
            try:
                data = json.loads(val.replace("'", "\""))
                if all(k in data for k in ["x", "y", "width", "height"]):
                    return data["x"], data["y"], data["width"], data["height"]
            except:
                return None
        df["bbox"] = df["region_shape_attributes"].apply(extract_bbox)

    # Verificar columnas requeridas
    if "filename" not in df.columns or "class" not in df.columns or "bbox" not in df.columns:
        raise ValueError("El CSV debe contener filename, class y bbox (region_shape_attributes).")

    # Crear carpetas de salida
    for split in ["train", "val"]:
        os.makedirs(os.path.join(out_dir, split, "images"), exist_ok=True)
        os.makedirs(os.path.join(out_dir, split, "labels"), exist_ok=True)

    # Separar en train y val
    train_df, val_df = train_test_split(df, test_size=val_split, stratify=df["class"], random_state=42)

    # Crear mapeo de clases
    class_map = {cls: i for i, cls in enumerate(df["class"].dropna().unique())}
    print("Mapeo de clases:", class_map)

    def write_labels(data, split):
        for _, row in data.iterrows():
            img_name = row["filename"]
            cls = row["class"]
            bbox = row["bbox"]

            if not isinstance(img_name, str) or bbox is None:
                continue

            img_src = os.path.join(images_dir, img_name)
            img_dst = os.path.join(out_dir, split, "images", img_name)

            if os.path.exists(img_src):
                # Copiar imagen a la carpeta correspondiente
                os.system(f'copy "{img_src}" "{img_dst}"') if os.name == "nt" else os.system(f'cp "{img_src}" "{img_dst}"')

                # Obtener tamaño de imagen para normalizar bbox
                with Image.open(img_src) as im:
                    img_w, img_h = im.size

                x, y, w, h = bbox
                x_center = (x + w / 2) / img_w
                y_center = (y + h / 2) / img_h
                w_norm = w / img_w
                h_norm = h / img_h

                # Guardar archivo .txt
                label_path = os.path.join(out_dir, split, "labels", os.path.splitext(img_name)[0] + ".txt")
                with open(label_path, "a") as f:  # "a" para múltiples objetos por imagen
                    f.write(f"{class_map[cls]} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")

    write_labels(train_df, "train")
    write_labels(val_df, "val")

    # Generar archivo data.yaml
    yaml_path = os.path.join(out_dir, "data.yaml")
    with open(yaml_path, "w") as f:
        f.write(f"path: {os.path.abspath(out_dir)}\n")
        f.write("train: train/images\n")
        f.write("val: val/images\n")
        f.write("names:\n")
        for cls, idx in class_map.items():
            f.write(f"  {idx}: {cls}\n")

    return yaml_path


def main(args):
    # Preparar dataset
    yaml_path = prepare_dataset(args.csv_path, args.images_dir, args.out_dir, args.val_split)

    # Entrenar modelo YOLO
    model = YOLO(args.model)
    model.train(data=yaml_path, epochs=args.epochs, imgsz=args.imgsz, batch=args.batch)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", type=str, required=True, help="Ruta al archivo CSV con anotaciones")
    parser.add_argument("--images_dir", type=str, required=True, help="Directorio con imágenes")
    parser.add_argument("--out_dir", type=str, default="datasets/tapas", help="Carpeta de salida")
    parser.add_argument("--val_split", type=float, default=0.2, help="Proporción de validación")
    parser.add_argument("--epochs", type=int, default=10, help="Número de épocas de entrenamiento")
    parser.add_argument("--imgsz", type=int, default=640, help="Tamaño de imagen")
    parser.add_argument("--batch", type=int, default=4, help="Tamaño de batch")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Modelo base YOLO (ej: yolov8n.pt)")

    args = parser.parse_args()
    main(args)
