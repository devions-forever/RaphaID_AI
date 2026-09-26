"""Flat clinical status + shared cards — RaphaID AI.

Dark navy preserved. Single accent teal (#64ffda) + safety red (#F87171).
No gradients. No emoji. Icons come from app.components.icons.
Handles the real state of this repo: 1/7 weights present, rest pending.
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.components.icons import get_icon


# Expected weight files per submodule (must match streamlit_app MODEL_PATHS).
MODEL_FILES: dict[str, str] = {
    "malaria": "models/detection/malaria_yolov8n.pt",
    "sickle_cell": "models/detection/sickle_cell_yolov8n.pt",
    "all": "models/detection/all_yolov8n.pt",
    "iron_deficiency": "models/detection/iron_deficiency_yolov8n.pt",
    "mri": "models/radiology/mri_yolov8n.pt",
    "ct": "models/radiology/ct_yolov8n.pt",
    "xray": "models/radiology/xray_yolov8n.pt",
}

# Legacy single-file model from the original malaria demo.
LEGACY_MODEL = "models/best.pt"


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def check_model_status() -> dict[str, dict]:
    """Return {submodule: {ready: bool, path: str}} without loading weights."""
    root = _project_root()
    status: dict[str, dict] = {}
    for key, rel in MODEL_FILES.items():
        p = root / rel
        ready = p.exists() and p.stat().st_size > 0
        # Malaria can fall back to the legacy best.pt for demo purposes.
        if not ready and key == "malaria" and (root / LEGACY_MODEL).exists():
            ready = True
            rel = LEGACY_MODEL
        status[key] = {"ready": ready, "path": rel}
    return status


def readiness_strip(status: dict[str, dict] | None = None) -> tuple[int, int]:
    """Flat model-readiness strip. Returns (ready, total)."""
    status = status or check_model_status()
    ready = sum(1 for v in status.values() if v["ready"])
    total = len(status)

    labels = {
        "malaria": "Malaria",
        "sickle_cell": "Sickle Cell",
        "all": "ALL",
        "iron_deficiency": "Iron Def.",
        "mri": "MRI",
        "ct": "CT",
        "xray": "X-ray",
    }
    chips = []
    for key, info in status.items():
        dot = "#64ffda" if info["ready"] else "#5c6779"
        state = "ready" if info["ready"] else "pending weights"
        chips.append(
            f'<span style="display:inline-flex;align-items:center;gap:6px;'
            f'border:1px solid #1f2d44;border-radius:999px;padding:4px 10px;'
            f'margin:0 6px 6px 0;font-size:.76rem;color:#8a94a6;">'
            f'<span style="width:7px;height:7px;border-radius:50%;background:{dot};"></span>'
            f'{labels.get(key, key)} · {state}</span>'
        )
    st.markdown(
        "<div style='background:#111a2e;border:1px solid #1f2d44;border-radius:10px;"
        "padding:.8rem 1rem;margin-bottom:1rem;'>"
        f"<div style='font-size:.72rem;color:#8a94a6;text-transform:uppercase;"
        f"letter-spacing:.1em;margin-bottom:.5rem;'>Model readiness — {ready}/{total} ready</div>"
        f"<div>{''.join(chips)}</div>"
        "<div style='font-size:.76rem;color:#5c6779;margin-top:.4rem;'>"
        "Pending modules show sample UI and precise weight paths. No dummy results are generated."
        "</div></div>",
        unsafe_allow_html=True,
    )
    return ready, total


def metric_card(label: str, value: str, icon_key: str = "dashboard") -> None:
    st.markdown(
        "<div class='rh-card' style='text-align:center;'>"
        f"<div style='color:#64ffda;margin-bottom:.4rem;'>{get_icon(icon_key, '#64ffda', '24', '24')}</div>"
        f"<div style='font-size:1.6rem;font-weight:800;color:#e8edf3;'>{value}</div>"
        f"<div style='font-size:.7rem;color:#8a94a6;text-transform:uppercase;"
        f"letter-spacing:.08em;margin-top:.3rem;'>{label}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def info_card(title: str, content: str, icon_key: str = "dashboard") -> None:
    st.markdown(
        "<div class='rh-card'>"
        f"<div style='font-weight:700;color:#e8edf3;margin-bottom:.4rem;display:flex;"
        f"align-items:center;gap:.5rem;'>{get_icon(icon_key, '#64ffda', '18', '18')}{title}</div>"
        f"<div style='color:#8a94a6;font-size:.88rem;'>{content}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def missing_model_banner(submodule: str, expected_path: str) -> None:
    st.markdown(
        "<div style='background:#111a2e;border:1px solid #1f2d44;border-left:3px solid #64ffda;"
        "border-radius:0 10px 10px 0;padding:1rem 1.2rem;margin:1rem 0;'>"
        f"<div style='font-weight:700;color:#e8edf3;margin-bottom:.3rem;'>"
        f"{get_icon('memory', '#64ffda', '18', '18')} Model pending — {submodule}</div>"
        "<div style='font-size:.86rem;color:#8a94a6;'>Your team has not connected weights for this "
        "module yet. The page layout below is live; inference is disabled until weights arrive.<br>"
        f"Expected file: <code style='color:#64ffda;'>{expected_path}</code></div>"
        "</div>",
        unsafe_allow_html=True,
    )


def workflow_stepper(steps: list[str], active: int) -> None:
    """Flat 5-step clinical workflow indicator.

    steps: label list, e.g. ["Upload", "Quality", "Analyse", "Verify", "Report"]
    active: 0-based index of the current step. Steps before it render as done,
    the active step is accent-highlighted, later steps stay muted.
    """
    active = max(0, min(active, len(steps) - 1))
    parts = []
    for i, label in enumerate(steps):
        if i < active:
            dot, color, weight = "#64ffda", "#e8edf3", "600"
        elif i == active:
            dot, color, weight = "#64ffda", "#64ffda", "700"
        else:
            dot, color, weight = "#1f2d44", "#5c6779", "500"
        parts.append(
            f'<span style="display:inline-flex;align-items:center;gap:6px;'
            f'font-size:.76rem;color:{color};font-weight:{weight};">'
            f'<span style="width:8px;height:8px;border-radius:50%;background:{dot};"></span>'
            f"{i + 1}. {label}</span>"
        )
    st.markdown(
        '<div class="rh-stepper" style="display:flex;flex-wrap:wrap;gap:.9rem;'
        'align-items:center;margin-bottom:1rem;">'
        + '<span style="color:#5c6779;">&rarr;</span>'.join(parts)
        + "</div>",
        unsafe_allow_html=True,
    )


def quality_card(quality: dict) -> None:
    """Render an image-quality check result as a themed card instead of raw alerts."""
    passed = quality.get("passed", False)
    warnings = quality.get("has_warnings", False)
    if not passed:
        accent, title, state = "#F87171", "Quality check failed", "Blocked — recapture the sample"
    elif warnings:
        accent, title, state = "#64ffda", "Quality check passed with warnings", "Usable — review notes"
    else:
        accent, title, state = "#64ffda", "Quality check passed", "Ready for analysis"
    issues_html = ""
    for issue in quality.get("issues", []):
        sev = issue.get("severity", "info")
        col = "#F87171" if sev == "error" else "#8a94a6"
        issues_html += (
            f'<div style="font-size:.8rem;color:{col};margin-top:.25rem;">'
            f'{issue.get("message", "")} ({issue.get("detail", "")})</div>'
        )
    if not issues_html:
        issues_html = '<div style="font-size:.8rem;color:#5c6779;margin-top:.25rem;">No blur, exposure or saturation issues detected.</div>'
    st.markdown(
        f'<div class="rh-card" style="border-left:3px solid {accent};">'
        f'<div style="font-weight:700;color:#e8edf3;">{title}</div>'
        f'<div style="font-size:.78rem;color:#8a94a6;">{state}</div>'
        f"{issues_html}</div>",
        unsafe_allow_html=True,
    )
