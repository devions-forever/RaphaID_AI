"""
Shared UI Components — RaphaID AI
Flat clinical theme, zero emojis, SVG icon integration.
"""

from typing import Dict, List, Any
import streamlit as st

from app.components.icons import get_icon


def metric_card(label: str, value: str, icon_key: str = "dashboard", color: str = "#64ffda") -> None:
    """Render a styled clinical metric card."""
    icon_html = get_icon(icon_key, color, "24", "24") if icon_key else ""
    st.markdown(f"""
    <div class="rh-card" style="text-align: center; height: 100%;">
        <div style="display: flex; justify-content: center; margin-bottom: 0.4rem;">{icon_html}</div>
        <div class="metric-value" style="color: {color};">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def info_card(title: str, content: str, icon_key: str = "brand") -> None:
    """Render a clinical info card."""
    icon_html = get_icon(icon_key, "#64ffda", "18", "18") if icon_key else ""
    st.markdown(f"""
    <div class="rh-card">
        <div style="font-weight: 700; color: #FFFFFF; margin-bottom: 0.4rem; display: flex; align-items: center; gap: 0.5rem;">
            <span>{icon_html}</span>
            <span>{title}</span>
        </div>
        <div style="color: #8A94A6; font-size: 0.88rem; line-height: 1.6;">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def status_badge(text: str, status: str = "info") -> None:
    """Render a status badge."""
    palette = {
        "success": ("rgba(100, 255, 218, 0.12)", "#64ffda", "rgba(100, 255, 218, 0.3)"),
        "warning": ("rgba(138, 148, 166, 0.12)", "#8a94a6", "#1f2d44"),
        "error": ("rgba(248, 113, 113, 0.12)", "#f87171", "rgba(248, 113, 113, 0.3)"),
        "info": ("rgba(100, 255, 218, 0.08)", "#64ffda", "rgba(100, 255, 218, 0.25)"),
    }
    bg, fg, border = palette.get(status, palette["info"])
    st.markdown(f"""
    <span style="
        background: {bg};
        color: {fg};
        border: 1px solid {border};
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    ">{text}</span>
    """, unsafe_allow_html=True)


def detection_table(detections: List[Dict], class_colors: Dict = None) -> None:
    """Render a styled detection table."""
    if not detections:
        st.info("No detections to display.")
        return

    import pandas as pd
    df = pd.DataFrame(detections)
    st.dataframe(df, use_container_width=True, hide_index=True)


def patient_summary(details: Dict) -> None:
    """Render a compact patient summary."""
    parts = []
    if details.get("name"):
        parts.append(f"**{details['name']}**")
    if details.get("age"):
        parts.append(f"Age {details['age']}")
    if details.get("sex"):
        parts.append(details["sex"])
    if details.get("patient_id"):
        parts.append(f"ID: `{details['patient_id']}`")

    if parts:
        st.markdown(
            f"<div class='rh-card' style='padding: 0.6rem 0.9rem; margin-bottom: 0.6rem;'>"
            f"<span style='color: #64ffda; font-weight: 600; font-size: 0.8rem; margin-right: 0.5rem;'>PATIENT RECORD:</span>"
            f"<span style='color: #e8edf3; font-size: 0.85rem;'>{' · '.join(parts)}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.caption("No patient details entered")


def download_buttons(pdf_bytes: bytes = None, csv_data: str = None, img_bytes: bytes = None,
                     prefix: str = "report") -> None:
    """Render download buttons for clinical reports (no emojis)."""
    c1, c2, c3 = st.columns(3)
    if pdf_bytes:
        with c1:
            st.download_button("Download PDF Report", pdf_bytes, f"{prefix}.pdf", "application/pdf", use_container_width=True)
    if csv_data:
        with c2:
            st.download_button("Export CSV Detections", csv_data, f"{prefix}.csv", "text/csv", use_container_width=True)
    if img_bytes:
        with c3:
            st.download_button("Download Annotated Image", img_bytes, f"{prefix}.png", "image/png", use_container_width=True)