"""
RBC Morphology Classification Module

Uses a YOLOv8 classification model trained on erythrocytesIDB 2017.

Classes:
- circular
- elongated
- other

Important:
This module classifies an individual RBC image/crop.
It does not detect RBCs inside a full-field smear.
"""

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO


CLASS_NAMES = ["circular", "elongated", "other"]

UNCERTAINTY_THRESHOLD_LOW = 0.35
UNCERTAINTY_THRESHOLD_HIGH = 0.45


@dataclass
class Classification:
    class_name: str
    class_id: int
    confidence: float


@dataclass
class SickleCellResult:
    image_path: str
    classification: Optional[Classification] = None
    annotated_image: Optional[np.ndarray] = None
    inference_time_sec: float = 0.0

    # Compatibility fields used by the existing RaphaID UI.
    detections: List[Classification] = field(default_factory=list)

    total_normal: int = 0
    total_abnormal: int = 0
    sickle_count: int = 0
    target_count: int = 0
    spherocyte_count: int = 0
    sickle_percentage: float = 0.0

    morphology_class: str = ""
    morphology_confidence: float = 0.0

    def compute_metrics(self) -> None:
        """
        Map the morphology result into the existing session/report fields.

        'elongated' is a morphology class from erythrocytesIDB.
        It is deliberately NOT renamed to 'sickle_cell'.
        """
        if self.classification is None:
            return

        self.morphology_class = self.classification.class_name
        self.morphology_confidence = self.classification.confidence

        if self.morphology_class == "circular":
            self.total_normal = 1
        elif self.morphology_class == "elongated":
            self.total_abnormal = 1
        elif self.morphology_class == "other":
            self.total_abnormal = 1

    def summary(self) -> Dict:
        return {
            "image": self.image_path,
            "classification": self.morphology_class,
            "confidence": round(self.morphology_confidence, 4),
            "inference_time_sec": round(self.inference_time_sec, 4),
        }


class SickleCellDetector:
    """
    Compatibility wrapper around the YOLOv8 classification model.

    The existing application calls this object a 'Detector', so the name is
    retained to avoid unnecessary changes elsewhere in the codebase.
    """

    def __init__(self, weights_path: str, device: str = "cpu"):
        self.model = YOLO(weights_path)
        self.device = device

        print(
            f"Loaded RBC morphology classifier from "
            f"{weights_path} (device={device})"
        )

    def predict(
        self,
        image_source: str | np.ndarray,
        conf: float = 0.25,
        iou: float = 0.45,
        imgsz: int = 224,
        annotate: bool = True,
    ) -> SickleCellResult:

        del conf
        del iou

        start_time = time.perf_counter()

        results = self.model.predict(
            source=image_source,
            imgsz=imgsz,
            device=self.device,
            verbose=False,
        )

        inference_time_sec = time.perf_counter() - start_time

        result = results[0]

        # Classification models expose probabilities through result.probs.
        if result.probs is None:
            raise RuntimeError(
                "The loaded model did not return classification probabilities. "
                "Make sure the Sickle Cell model is a YOLO classification model."
            )

        class_id = int(result.probs.top1)
        confidence = float(result.probs.top1conf)

        if class_id >= len(CLASS_NAMES):
            class_name = f"class_{class_id}"
        else:
            class_name = CLASS_NAMES[class_id]

        classification = Classification(
            class_name=class_name,
            class_id=class_id,
            confidence=confidence,
        )

        annotated_img = None

        if annotate:
            annotated_img = self._draw_classification(
                result,
                classification,
            )

        img_path = (
            image_source
            if isinstance(image_source, str)
            else "<numpy_array>"
        )

        pred_result = SickleCellResult(
            image_path=img_path,
            classification=classification,
            annotated_image=annotated_img,
            inference_time_sec=inference_time_sec,
            detections=[classification],
        )

        pred_result.compute_metrics()

        return pred_result

    def _draw_classification(
        self,
        yolo_result,
        classification: Classification,
    ) -> np.ndarray:

        img = yolo_result.orig_img.copy()

        confidence = classification.confidence
        class_name = classification.class_name

        is_uncertain = (
            UNCERTAINTY_THRESHOLD_LOW
            <= confidence
            <= UNCERTAINTY_THRESHOLD_HIGH
        )

        if is_uncertain:
            label = f"INCONCLUSIVE — {class_name} ({confidence:.2f})"
            color = (0, 255, 255)
            text_color = (0, 0, 0)
        else:
            label = f"{class_name.upper()} ({confidence:.2f})"
            color = (0, 255, 0) if class_name == "circular" else (0, 0, 255)
            text_color = (255, 255, 255)

        height, width = img.shape[:2]

        cv2.rectangle(
            img,
            (0, 0),
            (width - 1, height - 1),
            color,
            4,
        )

        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = max(0.55, min(width, height) / 350)
        thickness = 2

        (tw, th), _ = cv2.getTextSize(
            label,
            font,
            scale,
            thickness,
        )

        cv2.rectangle(
            img,
            (0, 0),
            (min(width, tw + 16), th + 16),
            color,
            -1,
        )

        cv2.putText(
            img,
            label,
            (8, th + 7),
            font,
            scale,
            text_color,
            thickness,
            cv2.LINE_AA,
        )

        return img

    def predict_batch(
        self,
        source_dir: str,
        conf: float = 0.25,
        iou: float = 0.45,
        imgsz: int = 224,
        save_dir: Optional[str] = None,
    ) -> List[SickleCellResult]:

        del conf
        del iou

        source_path = Path(source_dir)

        image_extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".tif",
            ".tiff",
            ".bmp",
        }

        image_files = sorted(
            f
            for f in source_path.iterdir()
            if f.suffix.lower() in image_extensions
        )

        if not image_files:
            print(f"No images found in {source_path}")
            return []

        if save_dir:
            Path(save_dir).mkdir(parents=True, exist_ok=True)

        results: List[SickleCellResult] = []

        for img_file in image_files:
            pred = self.predict(
                str(img_file),
                imgsz=imgsz,
            )

            results.append(pred)

            if save_dir and pred.annotated_image is not None:
                save_path = Path(save_dir) / f"pred_{img_file.name}"
                cv2.imwrite(
                    str(save_path),
                    pred.annotated_image,
                )

        print(f"Processed {len(results)} images.")

        return results


@st.cache_resource
def load_sickle_cell_model(
    weights_path: str,
    device: str = "cpu",
) -> SickleCellDetector | None:

    """Cached loader for the local RBC morphology classifier."""

    if not Path(weights_path).exists():
        print(
            f"RBC morphology model weights not found locally: "
            f"{weights_path}"
        )
        return None

    try:
        return SickleCellDetector(
            weights_path,
            device,
        )
    except Exception as e:
        print(
            f"Failed to load RBC morphology classifier: {e}"
        )
        return None