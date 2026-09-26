"""
RaphaID AI — Offline Multi-Disease Diagnostic Tool
Main Streamlit application integrating Detection, Radiology, and Chatbot modules.

Boot order matters here. Streamlit renders nothing until the script yields its
first element, so the clinical boot splash is painted BEFORE the heavy imports
(torch, ultralytics, ...). Without this, the browser sits on Streamlit's grey
loading skeleton for the entire cold start.
"""

import sys
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Project root on sys.path so `app.*` and `src.*` resolve.
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# set_page_config() must be the very first Streamlit command in the script.
st.set_page_config(
    page_title="RaphaID AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# BOOT SPLASH — paint first, import afterwards.
# Each _splash.step() marks a real boot stage so the bar reflects actual work.
# ---------------------------------------------------------------------------
from app.components.splash import SplashController  # noqa: E402

_splash = SplashController(min_duration=3.5, duration=4.0)
_splash.start("Booting RaphaID AI clinical platform...")

# ---------------------------------------------------------------------------
# CRITICAL FIX: PyTorch 2.1+ torch.classes compatibility
# Must be applied BEFORE any torch/ultralytics imports
# ---------------------------------------------------------------------------
_splash.step(10, "Initialising neural network runtime...")
import torch
import torch._classes as _tc


# Monkey patch _ClassNamespace to gracefully handle __path__/__file__ access
# This prevents: "Tried to instantiate class '__path__.__file__', but it does not exist!"
_original_namespace_getattr = _tc._ClassNamespace.__getattr__

def _safe_namespace_getattr(self, attr):
    try:
        return _original_namespace_getattr(self, attr)
    except RuntimeError as e:
        error_str = str(e)
        # Handle __path__.__file__ and similar access patterns that fail in PyTorch 2.1+
        if '__path__' in error_str or '__file__' in error_str:
            # Return empty list for __path__ access (common pattern for namespace packages)
            # Return empty string for __file__ access
            return [] if '__path__' in self.name else ''
        raise

_tc._ClassNamespace.__getattr__ = _safe_namespace_getattr
_splash.step(22, "Loading deep learning engine...")
# ---------------------------------------------------------------------------

import time
from datetime import datetime

import cv2
import numpy as np
import pandas as pd
from PIL import Image

_splash.step(34, "Loading imaging and data libraries...")

# ---------------------------------------------------------------------------
# Imports from new module structure
# ---------------------------------------------------------------------------
from app.components.theme import apply_theme, get_theme_colors
from app.components.navigation import render_navigation
from app.components.footer import render_footer, update_session_metrics

_splash.step(46, "Applying clinical interface theme...")

from app.modules.detection import (
    MalariaDetector,
    SickleCellDetector,
    ALLDetector,
    IronDeficiencyDetector,
    load_malaria_model,
    load_sickle_cell_model,
    load_all_model,
    load_iron_deficiency_model,
)

_splash.step(62, "Initialising microscopy detection modules...")

from app.modules.radiology import (
    MRIDetector,
    CTScanDetector,
    XRayDetector,
    load_mri_model,
    load_ct_model,
    load_xray_model,
)

_splash.step(78, "Preparing radiology inference engines...")

from src.utils.quality_check import assess_image_quality
from src.utils.report_generator import (
    generate_mri_report,
    generate_ct_report,
    generate_xray_report,
    generate_csv_report_radiology,
)

_splash.step(90, "Loading clinical reporting services...")

from src.utils.session_manager import get_session_manager

_splash.step(96, "Restoring local session store...")

# NOTE: app.modules.chatbot is imported lazily inside main() on purpose —
# sentence-transformers + chromadb + langchain add roughly half a minute to a
# cold start, and most sessions never open the assistant.


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DETECTION_SUBMODULES = {
    "malaria": "Malaria",
    "sickle_cell": "Sickle Cell",
    "all": "ALL Leukemia",
    "iron_deficiency": "Iron Deficiency",
}

RADIOLOGY_SUBMODULES = {
    "mri": "MRI Brain",
    "ct": "CT Chest",
    "xray": "X-ray Chest",
}

MODEL_PATHS = {
    "detection": {
        "malaria": "models/detection/malaria_yolov8n.pt",
        "sickle_cell": "models/detection/sickle_cell_yolov8n.pt",
        "all": "models/detection/all_yolov8n.pt",
        "iron_deficiency": "models/detection/iron_deficiency_yolov8n.pt",
    },
    "radiology": {
        "mri": "models/radiology/mri_yolov8n.pt",
        "ct": "models/radiology/ct_yolov8n.pt",
        "xray": "models/radiology/xray_yolov8n.pt",
    },
}

# Default model configs per submodule
DETECTION_CONFIGS = {
    "malaria": {
        "classes": ["ring", "trophozoite", "schizont", "gametocyte", "red_blood_cell"],
        "parasite_classes": {"ring", "trophozoite", "schizont", "gametocyte"},
        "uncertainty_low": 0.35,
        "uncertainty_high": 0.45,
    },
    "sickle_cell": {
        "classes": ["normal_rbc", "sickle_cell", "target_cell", "spherocyte"],
        "abnormal_classes": {"sickle_cell", "target_cell", "spherocyte"},
        "uncertainty_low": 0.35,
        "uncertainty_high": 0.45,
    },
    "all": {
        "classes": ["lymphoblast", "normal_lymphocyte", "smudge_cell"],
        "blast_classes": {"lymphoblast"},
        "uncertainty_low": 0.35,
        "uncertainty_high": 0.45,
    },
    "iron_deficiency": {
        "classes": ["microcyte", "hypochromic", "normal_rbc", "pencil_cell"],
        "abnormal_classes": {"microcyte", "hypochromic", "pencil_cell"},
        "uncertainty_low": 0.35,
        "uncertainty_high": 0.45,
    },
}


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------
def _downscale_if_needed(image_bgr: np.ndarray, max_dimension: int = 1600) -> np.ndarray:
    """Downscale image if too large to prevent OOM."""
    h, w = image_bgr.shape[:2]
    longest_side = max(h, w)
    if longest_side <= max_dimension:
        return image_bgr
    scale = max_dimension / longest_side
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(image_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)


def _is_uncertain(confidence: float, low: float = 0.35, high: float = 0.45) -> bool:
    return low <= confidence <= high


def _count_tiers(detections, parasite_classes, low=0.35, high=0.45):
    uncertain = confident = 0
    for d in detections:
        if d.class_name not in parasite_classes:
            continue
        if low <= d.confidence <= high:
            uncertain += 1
        elif d.confidence > high:
            confident += 1
    return uncertain, confident


def _draw_filtered(image_bgr, detections, config, class_colors, submodule: str):
    """Draw detections with uncertainty highlighting, optionally filtering classes."""
    img = image_bgr.copy()
    show_all = st.session_state.get(f"show_all_{submodule}", True)

    for det in detections:
        # Skip normal/healthy classes if filter is on
        if not show_all:
            skip_classes = {"red_blood_cell", "normal_rbc", "normal_lymphocyte", "normal"}
            if det.class_name in skip_classes:
                continue

        x1, y1, x2, y2 = [int(v) for v in det.bbox_xyxy]
        is_uncertain_det = _is_uncertain(det.confidence, config["uncertainty_low"], config["uncertainty_high"])

        if is_uncertain_det:
            color = (0, 255, 255)  # Yellow
            thickness = 3
            label = f"INCONCLUSIVE {det.confidence:.2f}"
            text_color = (0, 0, 0)
        else:
            color = class_colors.get(det.class_name, (255, 255, 255))
            is_target = (
                det.class_name in config.get("parasite_classes", set()) or
                det.class_name in config.get("abnormal_classes", set()) or
                det.class_name in config.get("blast_classes", set())
            )
            thickness = 2 if is_target else 1
            label = f"{det.class_name} {det.confidence:.2f}"
            text_color = (255, 255, 255)

        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)
        cv2.putText(img, label, (x1 + 2, y1 - 4),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 1, cv2.LINE_AA)
    return img


def _render_detection_gallery(image_bgr, detections, config, title="Detection Close-ups"):
    """Render zoomable gallery of detection crops."""
    target_classes = config.get("parasite_classes") or config.get("abnormal_classes") or config.get("blast_classes", set())
    target_dets = [d for d in detections if d.class_name in target_classes]

    if not target_dets:
        st.info(f"No target detections to display for {title.lower()}.")
        return

    from app.components.icons import get_icon
    st.markdown(f"### {get_icon('magnifying_glass_chart', '#64ffda', '20', '20')} {title}", unsafe_allow_html=True)
    st.caption("Zoomed crops for visual verification")

    img_h, img_w = image_bgr.shape[:2]
    gallery_items = []

    for det in target_dets:
        x1, y1, x2, y2 = [int(v) for v in det.bbox_xyxy]
        bw, bh = x2 - x1, y2 - y1
        if bw <= 0 or bh <= 0:
            continue

        pad_x, pad_y = max(1, int(bw * 0.1)), max(1, int(bh * 0.1))
        cx1, cy1 = max(0, x1 - pad_x), max(0, y1 - pad_y)
        cx2, cy2 = min(img_w, x2 + pad_x), min(img_h, y2 + pad_y)

        crop = image_bgr[cy1:cy2, cx1:cx2]
        if crop.size == 0:
            continue

        crop = cv2.resize(crop, (150, 150), interpolation=cv2.INTER_CUBIC)
        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)

        uncertain = _is_uncertain(det.confidence, config["uncertainty_low"], config["uncertainty_high"])
        gallery_items.append({
            "image": crop,
            "class_name": det.class_name,
            "confidence": det.confidence,
            "is_uncertain": uncertain,
        })

    if not gallery_items:
        return

    # Sort: uncertain first
    gallery_items.sort(key=lambda x: (not x["is_uncertain"], -x["confidence"]))

    # Render in grid
    max_initial = 12
    initial = gallery_items[:max_initial]
    remaining = gallery_items[max_initial:]

    def _render_grid(items):
        cols = st.columns(4)
        for i, item in enumerate(items):
            with cols[i % 4]:
                st.image(item["image"], use_container_width=True)
                name = item["class_name"].replace("_", " ").title()
                st.markdown(f"**{name}**")
                st.caption(f"Conf: {item['confidence']:.1%}")
                st.caption("⚠️ Needs review" if item["is_uncertain"] else "✓ High confidence")

    _render_grid(initial)

    if remaining:
        expanded = st.session_state.get("gallery_expanded", False)
        if expanded:
            _render_grid(remaining)
        _, c, _ = st.columns([2, 1, 2])
        with c:
            if expanded:
                if st.button("🔼 Show less", key="gallery_collapse", use_container_width=True):
                    st.session_state.gallery_expanded = False
                    st.rerun()
            else:
                if st.button(f"🔽 Show all {len(gallery_items)}", key="gallery_expand", use_container_width=True):
                    st.session_state.gallery_expanded = True
                    st.rerun()


def _render_patient_intake():
    """Render patient information form in sidebar/expander."""
    if "patient_details" not in st.session_state:
        st.session_state.patient_details = {
            "name": "", "age": None, "sex": "", "patient_id": "",
            "clinician": "", "facility": "", "notes": "",
        }

    with st.expander("Patient Information", expanded=False):
        st.caption("Session-only storage. Not saved to server. All fields optional.")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.patient_details["name"] = st.text_input(
                "Patient Name", value=st.session_state.patient_details["name"],
                placeholder="e.g. Femi Okoro", key="pt_name"
            )
            age_val = st.number_input("Age", 0, 120,
                value=st.session_state.patient_details["age"] or 0,
                key="pt_age", help="0 = unknown")
            st.session_state.patient_details["age"] = age_val if age_val > 0 else None

        with c2:
            sex_opts = ["", "Male", "Female", "Other / Prefer not to say"]
            curr_sex = st.session_state.patient_details["sex"]
            idx = sex_opts.index(curr_sex) if curr_sex in sex_opts else 0
            st.session_state.patient_details["sex"] = st.selectbox(
                "Sex", sex_opts, index=idx, key="pt_sex"
            )
            st.session_state.patient_details["patient_id"] = st.text_input(
                "Patient / Sample ID", value=st.session_state.patient_details["patient_id"],
                placeholder="e.g. LAB-2026-00142", key="pt_id"
            )

        with c3:
            st.session_state.patient_details["clinician"] = st.text_input(
                "Requesting Clinician", value=st.session_state.patient_details["clinician"],
                placeholder="e.g. Dr. O.I Olayemi", key="pt_clinician"
            )
            st.session_state.patient_details["facility"] = st.text_input(
                "Health Facility", value=st.session_state.patient_details["facility"],
                placeholder="e.g. UCH Ibadan", key="pt_facility"
            )

        st.session_state.patient_details["notes"] = st.text_area(
            "Clinical Notes", value=st.session_state.patient_details["notes"],
            placeholder="Brief history...", max_chars=250, height=80, key="pt_notes"
        )

        if st.button("🗑 Clear", key="clear_patient"):
            st.session_state.patient_details = {k: ("" if k != "age" else None) for k in st.session_state.patient_details}
            st.rerun()


def _render_detection_module(submodule: str):
    """Render the Detection module UI for a specific disease."""
    config = DETECTION_CONFIGS[submodule]
    model_path = MODEL_PATHS["detection"][submodule]

    # Module-specific config
    if submodule == "malaria":
        detector_loader = load_malaria_model
        class_colors = {
            "red_blood_cell": (200, 200, 200), "ring": (0, 0, 255),
            "trophozoite": (0, 165, 255), "schizont": (0, 255, 255), "gametocyte": (255, 0, 255),
        }
        metric_keys = ["total_rbc", "total_parasites", "parasitemia_pct"]
    elif submodule == "sickle_cell":
        detector_loader = load_sickle_cell_model
        class_colors = {
            "normal_rbc": (200, 200, 200), "sickle_cell": (0, 0, 255),
            "target_cell": (0, 165, 255), "spherocyte": (255, 0, 255),
        }
        metric_keys = ["total_normal", "total_abnormal", "sickle_percentage"]
    elif submodule == "all":
        detector_loader = load_all_model
        class_colors = {
            "normal_lymphocyte": (200, 200, 200), "lymphoblast": (0, 0, 255),
            "smudge_cell": (0, 165, 255),
        }
        metric_keys = ["total_cells", "blast_count", "blast_percentage"]
    else:  # iron_deficiency
        detector_loader = load_iron_deficiency_model
        class_colors = {
            "normal_rbc": (200, 200, 200), "microcyte": (0, 0, 255),
            "hypochromic": (0, 165, 255), "pencil_cell": (255, 0, 255),
        }
        metric_keys = ["total_cells", "normal_count", "abnormal_percentage"]

    from app.components.status import (
        check_model_status,
        missing_model_banner,
        workflow_stepper,
    )

    STEPS = ["Upload", "Quality", "Analyse", "Verify", "Report"]

    # Sidebar settings
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Detection Settings")
        conf = st.slider("Confidence Threshold", 0.05, 0.95, 0.25, 0.05, key=f"conf_{submodule}")
        iou = st.slider("NMS IoU", 0.1, 0.9, 0.45, 0.05, key=f"iou_{submodule}")
        st.checkbox(
            "Show all classes (incl. healthy)", value=True, key=f"show_all_{submodule}"
        )

    # Model status — designed pending state instead of a dead-end error wall.
    model_ready = check_model_status().get(submodule, {}).get("ready", False)
    if model_ready:
        detector = detector_loader(model_path)
        if detector is not None:
            model_ready = True
    else:
        detector = None
    if detector is None:
        model_ready = False
        detector = None

    workflow_stepper(STEPS, active=0)
    if not model_ready:
        missing_model_banner(
            DETECTION_SUBMODULES.get(submodule, submodule),
            MODEL_PATHS["detection"][submodule],
        )

    # Patient intake — collapsed so Upload/Analyse stay near the top.
    _render_patient_intake()

    # Image upload
    st.markdown("---")
    st.markdown("#### Upload slide")
    uploaded = st.file_uploader(
        "Microscopy image (PNG, JPG, TIF, BMP)",
        type=["png", "jpg", "jpeg", "tif", "tiff", "bmp"],
        key=f"uploader_{submodule}"
    )

    # Sample images — clinical thumbnails with real labels.
    st.markdown("**Or try a sample:**")
    s1, s2, s3 = st.columns(3)
    samples = {
        "Infected": "app/samples/infected_sample.jpg",
        "Mixed field": "app/samples/mixed_sample.jpg",
        "Healthy": "app/samples/healthy_sample.jpg",
    }
    for i, (label, path) in enumerate(samples.items()):
        with [s1, s2, s3][i]:
            if Path(path).exists():
                st.image(path, use_container_width=True, caption=label)
            if st.button(label, key=f"sample_{submodule}_{i}", use_container_width=True):
                st.session_state[f"sample_{submodule}"] = path
                st.rerun()

    has_image = uploaded or f"sample_{submodule}" in st.session_state
    if has_image:
        if uploaded:
            file_bytes = np.frombuffer(uploaded.read(), np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            img_name = uploaded.name
        else:
            img = cv2.imread(st.session_state[f"sample_{submodule}"])
            img_name = Path(st.session_state[f"sample_{submodule}"]).name

        if img is None:
            st.error("Could not decode image.")
            return

        img = _downscale_if_needed(img)

        # Quality check — themed card instead of raw emoji alerts.
        from app.components.status import quality_card
        quality = assess_image_quality(img, "microscopy")
        quality_card(quality)
        if not quality["passed"]:
            st.stop()
        workflow_stepper(STEPS, active=2)

        # Run inference
        analyse_kwargs = dict(
            type="primary", key=f"analyse_{submodule}", use_container_width=True
        )
        if not model_ready:
            st.button(
                "Analyse Slide — waiting for model weights",
                disabled=True,
                help=f"Drop weights at {MODEL_PATHS['detection'][submodule]} to enable this button.",
                **analyse_kwargs,
            )
        elif st.button("Analyse Slide", **analyse_kwargs):
            with st.spinner("Running detection..."):
                result = detector.predict(img, conf=conf, iou=iou, annotate=True)
            st.session_state[f"result_{submodule}"] = result
            st.session_state[f"img_{submodule}"] = img
            st.session_state[f"img_name_{submodule}"] = img_name
            st.rerun()

    # Display results
    result_key = f"result_{submodule}"
    if result_key in st.session_state:
        result = st.session_state[result_key]
        img = st.session_state[f"img_{submodule}"]
        img_name = st.session_state[f"img_name_{submodule}"]

        workflow_stepper(STEPS, active=3)

        # Metrics with plain-English interpretation under each value.
        interp = {
            "malaria": ["Cells counted in the field", "Parasite-positive cells", "Parasitaemia — WHO severity band applies"],
            "sickle_cell": ["Normal morphology cells", "Abnormal shape variants", "Abnormal share of the field"],
            "all": ["Lymphocytes counted", "Blast cells detected", "Blast share — escalation threshold is clinical"],
            "iron_deficiency": ["RBCs counted", "Normal morphometry", "Microcytic/hypochromic share"],
        }[submodule]
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(DETECTION_SUBMODULES and interp[0], getattr(result, metric_keys[0], len(result.detections)))
            st.caption(interp[0])
        with m2:
            st.metric(interp[1], getattr(result, metric_keys[1], 0))
            st.caption("Model-detected, requires human confirmation")
        with m3:
            st.metric(interp[2], f"{getattr(result, metric_keys[2], 0):.2f}%")
            st.caption("Estimate — not a laboratory value")

        # Images
        c1, c2 = st.columns(2)
        with c1:
            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original", use_container_width=True)
        with c2:
            display_img = _draw_filtered(img, result.detections, config, class_colors, submodule)
            st.image(cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB), caption="Detections", use_container_width=True)

        # Uncertainty check — themed callout, verification lands with orchestrator.
        parasite_classes = config.get("parasite_classes") or config.get("abnormal_classes") or config.get("blast_classes", set())
        unc, conf_cnt = _count_tiers(result.detections, parasite_classes, config["uncertainty_low"], config["uncertainty_high"])
        if unc > 0:
            from app.components.status import callout
            callout(
                f"{unc} detection(s) in the 35–45% confidence band need human verification.",
                "These are drawn with thick yellow boxes. Orchestrator verification activates when weights are connected.",
                kind="warning",
            )

        # Gallery
        _render_detection_gallery(img, result.detections, config)

        # Downloads
        workflow_stepper(STEPS, active=4)
        st.markdown("---")
        st.markdown("#### Download Reports")
        d1, d2, d3 = st.columns(3)
        with d1:
            st.download_button(
                "PDF Report",
                data=b"",
                file_name=f"{submodule}_report_{Path(img_name).stem}.pdf",
                mime="application/pdf",
                disabled=True,
                help="PDF template ready — activates when the report generator is wired to results.",
                use_container_width=True,
            )
        with d2:
            # CSV
            import csv, io
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["class", "confidence", "x1", "y1", "x2", "y2"])
            for d in result.detections:
                writer.writerow([d.class_name, f"{d.confidence:.4f}", *[f"{v:.1f}" for v in d.bbox_xyxy]])
            st.download_button("CSV detections", output.getvalue(),
                             f"detections_{Path(img_name).stem}.csv", "text/csv",
                             use_container_width=True)
        with d3:
            if result.annotated_image is not None:
                pil_img = Image.fromarray(cv2.cvtColor(result.annotated_image, cv2.COLOR_BGR2RGB))
                buf = io.BytesIO()
                pil_img.save(buf, format="PNG")
                st.download_button("Annotated image", buf.getvalue(),
                                 f"annotated_{Path(img_name).stem}.png", "image/png",
                                 use_container_width=True)

        # Update session metrics
        update_session_metrics(submodule, {"total_detections": len(result.detections), "positive": getattr(result, metric_keys[1], 0) > 0})


def _render_radiology_module(submodule: str):
    """Render the Radiology module UI for a specific modality."""
    model_path = MODEL_PATHS["radiology"][submodule]

    if submodule == "mri":
        detector_loader = load_mri_model
        report_gen = generate_mri_report
        modality_name = "MRI Brain"
    elif submodule == "ct":
        detector_loader = load_ct_model
        report_gen = generate_ct_report
        modality_name = "CT Chest"
    else:  # xray
        detector_loader = load_xray_model
        report_gen = generate_xray_report
        modality_name = "Chest X-ray"

    from app.components.status import (
        check_model_status,
        missing_model_banner,
        quality_card,
        workflow_stepper,
        metric_card,
        callout,
    )

    STEPS = ["Upload", "Quality", "Analyse", "Verify", "Report"]

    with st.sidebar:
        st.markdown("---")
        st.markdown("### Radiology Settings")
        conf = st.slider("Confidence Threshold", 0.05, 0.95, 0.25, 0.05, key=f"conf_{submodule}")
        iou = st.slider("NMS IoU", 0.1, 0.9, 0.45, 0.05, key=f"iou_{submodule}")

    # Model status — designed pending state instead of a dead-end error wall.
    model_ready = check_model_status().get(submodule, {}).get("ready", False)
    detector = None
    if model_ready:
        detector = detector_loader(model_path)
        model_ready = detector is not None

    workflow_stepper(STEPS, active=0)
    if not model_ready:
        missing_model_banner(modality_name, MODEL_PATHS["radiology"][submodule])

    _render_patient_intake()

    st.markdown("---")
    st.markdown("#### Upload study")
    uploaded = st.file_uploader(
        f"{modality_name} image (PNG, JPG, TIF, DICOM)",
        type=["png", "jpg", "jpeg", "tif", "tiff", "dcm"],
        key=f"uploader_{submodule}"
    )

    has_image = uploaded
    if has_image:
        dicom_meta = None
        if uploaded.name.lower().endswith(".dcm"):
            import pydicom
            ds = pydicom.dcmread(uploaded)
            pixel_array = ds.pixel_array
            if pixel_array.dtype != np.uint8:
                pixel_array = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            img = cv2.cvtColor(pixel_array, cv2.COLOR_GRAY2BGR) if len(pixel_array.shape) == 2 else pixel_array
            # DICOM header as a themed meta card.
            dicom_meta = {
                "Modality": str(getattr(ds, "Modality", "N/A")),
                "Rows x Cols": f"{getattr(ds, 'Rows', '?')} x {getattr(ds, 'Columns', '?')}",
                "Bits stored": str(getattr(ds, "BitsStored", "?")),
                "Patient ID": str(getattr(ds, "PatientID", "N/A"))[:24],
            }
            st.markdown(
                "<div class='rh-card' style='border-left:3px solid #64ffda;'>"
                "<div style='font-weight:700;color:#e8edf3;margin-bottom:.3rem;'>DICOM header</div>"
                + "".join(
                    f"<div style='font-size:.8rem;color:#8a94a6;'>{k}: <span style='color:#e8edf3;'>{v}</span></div>"
                    for k, v in dicom_meta.items()
                )
                + "</div>",
                unsafe_allow_html=True,
            )
        else:
            file_bytes = np.frombuffer(uploaded.read(), np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img_name = uploaded.name

        if img is None:
            st.error("Could not decode image.")
            return

        img = _downscale_if_needed(img)

        # Quality check — themed card instead of raw emoji alerts.
        quality = assess_image_quality(img, submodule)
        quality_card(quality)
        if not quality["passed"]:
            st.stop()
        workflow_stepper(STEPS, active=2)

        # Run inference — disabled until weights arrive.
        analyse_kwargs = dict(
            type="primary", key=f"analyse_{submodule}", use_container_width=True
        )
        if not model_ready:
            st.button(
                f"Analyse {modality_name} — waiting for model weights",
                disabled=True,
                help=f"Drop weights at {MODEL_PATHS['radiology'][submodule]} to enable this button.",
                **analyse_kwargs,
            )
        elif st.button(f"Analyse {modality_name}", **analyse_kwargs):
            with st.spinner(f"Analyzing {modality_name}..."):
                result = detector.predict(img, conf=conf, iou=iou, annotate=True)
            st.session_state[f"result_{submodule}"] = result
            st.session_state[f"img_{submodule}"] = img
            st.session_state[f"img_name_{submodule}"] = img_name
            st.rerun()

    result_key = f"result_{submodule}"
    if result_key in st.session_state:
        result = st.session_state[result_key]
        img = st.session_state[f"img_{submodule}"]
        img_name = st.session_state[f"img_name_{submodule}"]

        # Results — interpreted metrics, stepper at the Verify/Report stage.
        workflow_stepper(STEPS, active=4)
        st.markdown("### Analysis results")
        summary = result.summary()

        total = summary["total_detections"]
        if submodule == "mri":
            focus_label, focus_value = "Tumor volume", f"{summary.get('tumor_volume_mm3', 0):.1f} mm³"
        elif submodule == "ct":
            focus_label, focus_value = "Nodule count", str(summary.get("nodule_count", 0))
        else:
            focus_label, focus_value = "Pneumonia foci", str(summary.get("pneumonia_count", 0))

        k1, k2, k3 = st.columns(3)
        with k1:
            metric_card("Total detections", str(total), submodule)
        with k2:
            metric_card(focus_label, focus_value, submodule)
        with k3:
            metric_card("Inference time", f"{summary['inference_time_sec']:.2f}s", "bolt")

        callout(
            f"{total} finding{'s' if total != 1 else ''} annotated on this study.",
            "Findings are decision support only — confirm against the full study and "
            "report to a radiologist before any clinical action.",
            kind="info" if total else "warning",
        )

        # Images
        c1, c2 = st.columns(2)
        with c1:
            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original", use_container_width=True)
        with c2:
            if result.annotated_image is not None:
                st.image(cv2.cvtColor(result.annotated_image, cv2.COLOR_BGR2RGB),
                        caption="Detections", use_container_width=True)

        # Detection table — themed, not stock Streamlit.
        counts = result._per_class_counts() if hasattr(result, '_per_class_counts') else {}
        if counts:
            st.markdown("### Detection summary")
            rows = "".join(
                f"<tr><td>{k.replace('_', ' ').title()}</td><td style='text-align:right;"
                f"color:#64ffda;font-weight:700;'>{v}</td></tr>"
                for k, v in counts.items()
            )
            st.markdown(
                "<table class='detection-table'>"
                "<tr><th>Class</th><th style='text-align:right;'>Count</th></tr>"
                f"{rows}</table>",
                unsafe_allow_html=True,
            )

        # Downloads — radiology keeps real PDF/CSV/image exports.
        st.markdown("---")
        st.markdown("### Download reports")
        d1, d2, d3 = st.columns(3)
        with d1:
            try:
                pdf_bytes = report_gen(
                    result,
                    patient_details=st.session_state.get("patient_details"),
                    report_meta=st.session_state.get("report_meta"),
                )
                st.download_button("PDF report", pdf_bytes,
                                 f"{submodule}_report_{Path(img_name).stem}.pdf", "application/pdf")
            except Exception as e:
                callout("PDF export failed", str(e), kind="error")
        with d2:
            csv_data = generate_csv_report_radiology(result, submodule)
            st.download_button("CSV detections", csv_data,
                             f"{submodule}_detections_{Path(img_name).stem}.csv", "text/csv")
        with d3:
            if result.annotated_image is not None:
                pil_img = Image.fromarray(cv2.cvtColor(result.annotated_image, cv2.COLOR_BGR2RGB))
                buf = io.BytesIO()
                pil_img.save(buf, format="PNG")
                st.download_button("Annotated image", buf.getvalue(),
                                 f"annotated_{Path(img_name).stem}.png", "image/png")

        update_session_metrics(submodule, {"total_detections": summary["total_detections"], "positive": summary["total_detections"] > 0})


def _render_dashboard():
    """Render the main dashboard."""
    colors = get_theme_colors()
    from app.components.icons import get_icon

    st.markdown(f"""
    <div class="rh-hero">
        <h2 style="color: #FFFFFF; margin-bottom: 0.2rem; font-size: 1.8rem; display: flex; align-items: center; justify-content: center; gap: 0.75rem;">
           {get_icon("dashboard", "#64ffda", "28", "28")} RaphaID AI
        </h2>
        <p style="color: #D8DEE9; margin: 0 0 0.3rem 0; font-size: 0.95rem;">
            Offline Multi-Disease Diagnostic Tool
        </p>
        <p style="margin: 0.6rem 0 0 0;">
            <span class="rh-badge">Air-gapped</span>
            <span class="rh-badge">CPU-only</span>
            <span class="rh-badge">WHO Workflow</span>
        </p>
        <p style="color: #8A94A6; margin: 0.6rem 0 0 0; font-size: 0.78rem;">
            YOLOv8n · Human Verification · PDF + CSV Reports
        </p>
    </div>
    """, unsafe_allow_html=True)

    from app.components.status import readiness_strip, check_model_status
    _status = check_model_status()
    readiness_strip(_status)

    # Quick actions — flat action cards with status (icons, not emoji).
    st.markdown("### Quick Actions")
    det_ready = _status.get("malaria", {}).get("ready", False)
    rad_ready = any(_status.get(k, {}).get("ready", False) for k in ("mri", "ct", "xray"))
    kb_dir = Path(__file__).resolve().parent.parent / "data" / "medical_knowledge"
    kb_ready = kb_dir.exists() and any(kb_dir.glob("*.md")) | any(kb_dir.glob("*.txt")) if kb_dir.exists() else False
    actions = [
        ("detection", "Blood Microscopy", "Malaria, Sickle Cell, ALL, Iron Def.",
         "Ready — demo weights" if det_ready else "Pending weights", det_ready),
        ("radiology", "Radiology Imaging", "MRI Brain, CT Chest, X-ray Chest",
         "Ready" if rad_ready else "Pending weights", rad_ready),
        ("chatbot", "Clinical Assistant", "Guideline-grounded Q&A with citations",
         "Ready" if kb_ready else "Needs guideline files", kb_ready),
    ]
    c1, c2, c3 = st.columns(3)
    for col, (icon, title, desc, badge, _ok) in zip((c1, c2, c3), actions):
        with col:
            st.markdown(
                f"<div class='rh-card' style='text-align:center;'>"
                f"<div style='color:#64ffda;margin-bottom:.4rem;'>{get_icon(icon, '#64ffda', '28', '28')}</div>"
                f"<div style='font-weight:700;color:#e8edf3;'>{title}</div>"
                f"<div style='font-size:.8rem;color:#8a94a6;margin:.25rem 0 .5rem 0;'>{desc}</div>"
                f"<span class='rh-badge'>{badge}</span>"
                "</div>",
                unsafe_allow_html=True,
            )
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button(
            "New Detection",
            use_container_width=True, type="primary",
            help="Start a new blood pathology detection analysis"
        ):
            st.session_state["current_module"] = "detection"
            st.session_state["detection_submodule"] = "malaria"
            st.rerun()
    with b2:
        if st.button(
            "New Radiology Scan",
            use_container_width=True,
            help="Start a new radiology imaging analysis"
        ):
            st.session_state["current_module"] = "radiology"
            st.session_state["radiology_submodule"] = "mri"
            st.rerun()
    with b3:
        if st.button(
            "Medical Assistant",
            use_container_width=True,
            help="Open the AI medical assistant chatbot"
        ):
            st.session_state["current_module"] = "chatbot"
            st.rerun()

    # Honest capabilities with medical icons (no fake performance claims).
    st.markdown("### Capabilities")
    facts = [
        ("microchip", "Model", "YOLOv8n"),
        ("bacterium", "Detection", "4 Diseases"),
        ("xray_icon", "Radiology", "3 Modalities"),
        ("robot", "Assistant", "RAG + LangGraph"),
        ("bolt", "Compute", "CPU only"),
        ("memory", "RAM Target", "< 6 GB"),
        ("shield", "Offline", "Fully Air-gapped"),
        ("file_medical", "Reports", "PDF + CSV"),
    ]
    for row_start in range(0, len(facts), 4):
        cols = st.columns(4)
        for col, (icon, label, value) in zip(cols, facts[row_start:row_start + 4]):
            with col:
                st.markdown(
                    f"<div class='rh-card' style='text-align:center;padding:.8rem;'>"
                    f"<div style='color:#64ffda;'>{get_icon(icon, '#64ffda', '26', '26')}</div>"
                    f"<div style='font-size:.68rem;color:#8a94a6;text-transform:uppercase;"
                    f"letter-spacing:.08em;margin-top:.35rem;'>{label}</div>"
                    f"<div style='font-size:1rem;font-weight:700;color:#e8edf3;margin-top:.25rem;'>{value}</div>"
                    "</div>",
                    unsafe_allow_html=True,
                )

    # Recent activity this session (honest — reads real session state only).
    session = st.session_state.get("session_data", {})
    analyses = session.get("analysis_count", 0)
    metrics = session.get("metrics", {})
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        from app.components.status import metric_card
        metric_card("Analyses this session", str(analyses), "magnifying_glass_chart")
    with a2:
        metric_card("Total detections", str(metrics.get("total_detections", 0)), "detection")
    with a3:
        metric_card("Positive cases", str(metrics.get("positive_cases", 0)), "vial")
    with a4:
        metric_card("Reports generated", str(metrics.get("reports_generated", 0)), "file_medical")

    # Clinical workflow with medical icons — themed flat stepper, no gradients.
    st.markdown("### Clinical Workflow")
    workflow_steps = [
        ("vial", "Upload", "Sample/Image"),
        ("magnifying_glass_chart", "Quality", "Auto-Check"),
        ("brain", "Detect", "AI Inference"),
        ("user_doctor", "Verify", "Clinician Review"),
        ("file_medical_2", "Report", "PDF/CSV Export"),
    ]
    workflow_html = '<div class="rh-stepper" style="display:flex;flex-wrap:wrap;gap:.5rem;justify-content:space-between;">'
    for i, (icon, title, desc) in enumerate(workflow_steps):
        workflow_html += (
            f'<div class="rh-step">'
            f'<div style="color:#64ffda;">{get_icon(icon, "#64ffda", "26", "26")}</div>'
            f'<div style="font-weight:600;">{title}</div>'
            f'<div style="font-size:.75rem;color:#8a94a6;">{desc}</div>'
            "</div>"
        )
        if i < len(workflow_steps) - 1:
            workflow_html += '<div style="color:#64ffda;align-self:center;">&rarr;</div>'
    workflow_html += "</div>"
    st.markdown(workflow_html, unsafe_allow_html=True)

    # Disclaimer
    st.warning(
        "Disclaimer: For research use and decision support only. Not intended as a "
        "standalone diagnostic tool. All findings require confirmation "
        "by a qualified specialist."
    )

    # Footer
    render_footer()


def main():
    # NOTE: st.set_page_config() already ran at the top of this module, before
    # the heavy imports, so that the boot splash could paint first.

    # Apply theme before the splash lifts, so the dashboard is styled on reveal.
    apply_theme()

    # Every boot stage is complete — lift the splash and show the app.
    _splash.complete()

    # Session state initialization
    defaults = {
        "current_module": "dashboard",
        "detection_submodule": "malaria",
        "radiology_submodule": "mri",
        "report_meta": {
            "report_number": f"RPT-{datetime.now().strftime('%Y%m%d')}-{np.random.randint(10000, 99999)}",
            "study_id": f"STD-{np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 2).tolist()[0]}{np.random.randint(100, 999)}",
            "date": datetime.now().strftime("%d %B %Y"),
            "time": datetime.now().strftime("%H:%M"),
        },
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Initialize session manager
    session_mgr = get_session_manager()
    if "session_data" not in st.session_state:
        st.session_state.session_data = {
            "session_id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "start_time": datetime.now().strftime("%H:%M:%S"),
            "current_module": "dashboard",
            "analysis_count": 0,
            "metrics": {"total_detections": 0, "positive_cases": 0, "verifications": 0, "reports_generated": 0},
            "analytics": {"malaria": 0, "sickle_cell": 0, "all": 0, "iron_deficiency": 0, "mri": 0, "ct": 0, "xray": 0},
        }

    # Navigation callback
    def on_module_change(module):
        st.session_state["current_module"] = module
        st.session_state.session_data["current_module"] = module

    def on_home_click():
        """Callback when home button is clicked."""
        pass  # State is handled in navigation component

    # Render sidebar navigation with home button
    render_navigation(
        st.session_state["current_module"], 
        on_module_change,
        on_home_click=on_home_click
    )

    # Route to module
    module = st.session_state["current_module"]

    if module == "dashboard":
        _render_dashboard()

    elif module == "detection":
        submodule = st.session_state.get("detection_submodule", "malaria")
        from app.components.icons import get_icon
        icon_html = get_icon(submodule, "#64ffda", "22", "22")
        st.markdown(f'### {icon_html} {DETECTION_SUBMODULES[submodule]} Detection', unsafe_allow_html=True)
        _render_detection_module(submodule)

    elif module == "radiology":
        submodule = st.session_state.get("radiology_submodule", "mri")
        from app.components.icons import get_icon
        icon_html = get_icon(submodule, "#64ffda", "22", "22")
        st.markdown(f'### {icon_html} {RADIOLOGY_SUBMODULES[submodule]} Analysis', unsafe_allow_html=True)
        _render_radiology_module(submodule)

    elif module == "chatbot":
        # Imported lazily on purpose: this module pulls in sentence-transformers,
        # chromadb, langchain and langgraph, which add a large chunk of cold-start
        # time and are not needed unless the user opens the assistant.
        from app.modules.chatbot import render_chatbot_ui
        render_chatbot_ui()


if __name__ == "__main__":
    main()