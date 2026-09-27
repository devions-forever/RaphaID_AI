"""
Clinical Top Bar — RaphaID AI.

A single, non-intrusive utility strip pinned above the workspace. It answers the
questions a clinician asks on every screen: *where am I, which patient is loaded,
is the platform ready, and is it offline?*

The right-hand side also carries the live "system running" pulse that the team's
original header had, so the platform always signals that it is active.
"""

from datetime import datetime
from typing import Optional

import streamlit as st

from app.components.htmlkit import render_html
from app.components.icons import get_icon
from app.components.status import check_model_status

MODULE_LABELS = {
    "dashboard": "Clinical Dashboard",
    "detection": "Blood Pathology",
    "radiology": "Radiology Imaging",
    "chatbot": "Medical Assistant",
}

SUBMODULE_LABELS = {
    "malaria": "Malaria",
    "sickle_cell": "Sickle Cell",
    "all": "ALL Leukemia",
    "iron_deficiency": "Iron Deficiency",
    "mri": "MRI Brain",
    "ct": "CT Chest",
    "xray": "Chest X-ray",
}


def _item(icon_key: str, text: str, color: str = "#64ffda") -> str:
    return (
        '<span class="rh-topbar-item">'
        f"{get_icon(icon_key, color, '14', '14')}"
        f"<span>{text}</span>"
        "</span>"
    )


def render_topbar(module: str, submodule: Optional[str] = None) -> None:
    """Render the persistent clinical status bar for the current workspace."""
    details = st.session_state.get("patient_details", {}) or {}
    session = st.session_state.get("session_data", {}) or {}

    facility = details.get("facility") or "RaphaID Clinical Workstation"
    clinician = details.get("clinician") or "Unassigned clinician"

    patient_bits = []
    if details.get("name"):
        patient_bits.append(str(details["name"]))
    if details.get("patient_id"):
        patient_bits.append(f"ID {details['patient_id']}")
    if details.get("age"):
        patient_bits.append(f"{details['age']}y")
    if details.get("sex"):
        patient_bits.append(str(details["sex"]))
    patient_text = " · ".join(patient_bits) if patient_bits else "No patient loaded"

    crumb = MODULE_LABELS.get(module, module.title())
    if submodule:
        crumb = f"{crumb} / {SUBMODULE_LABELS.get(submodule, submodule)}"

    status = check_model_status()
    ready = sum(1 for v in status.values() if v.get("ready"))
    total = len(status) or 1
    models_ok = ready == total
    models_chip = (
        f'<span class="rh-topbar-chip{"" if models_ok else " is-muted"}">'
        f"{get_icon('models', '#64ffda' if models_ok else '#8a94a6', '13', '13')}"
        f"{ready}/{total} models ready</span>"
    )

    started = session.get("start_time", datetime.now().strftime("%H:%M:%S"))
    now = datetime.now().strftime("%H:%M")

    render_html(
        '<div class="rh-topbar">'
        '<div class="rh-topbar-group">'
        + _item("user_doctor", f"<strong>{facility}</strong>")
        + '<span class="rh-topbar-sep"></span>'
        + _item("user_doctor", clinician, "#8a94a6")
        + '<span class="rh-topbar-sep"></span>'
        + _item("vial", patient_text, "#8a94a6")
        + "</div>"
        + '<div class="rh-topbar-group">'
        + _item("dashboard", crumb, "#8a94a6")
        + '<span class="rh-topbar-sep"></span>'
        + models_chip
        + '<span class="rh-topbar-chip">'
        + get_icon("offline", "#64ffda", "13", "13")
        + "Offline</span>"
        + '<span class="rh-topbar-item">'
        + '<span class="rh-pulse"></span>'
        + f"<span>Live &middot; {started} &rarr; {now}</span>"
        + "</span>"
        + "</div>"
        + "</div>"
    )
