"""
Footer Component — Session/Metrics/Analytics Panels (flat, icon-based).
"""

from datetime import datetime
from typing import Dict, Any

import streamlit as st

from app.components.htmlkit import render_html
from app.components.icons import get_icon


def _panel(title: str, icon_key: str, rows: str) -> None:
    """One footer panel: icon + title heading followed by a label/value list."""
    render_html(
        f"{get_icon(icon_key, '#64ffda', '16', '16')} "
        "<span style='font-weight:700;color:#e8edf3;font-size:0.9rem;'>" + title + "</span>"
    )
    render_html(
        "<div style='font-size:0.85rem;color:#8a94a6;line-height:1.9;'>" + rows + "</div>"
    )


def render_footer(
    session_data: Dict[str, Any] = None,
    show_analytics: bool = True,
) -> None:
    """
    Render the footer with session info, metrics, and analytics.

    Args:
        session_data: Current session data dict
        show_analytics: Whether to show analytics panel
    """
    if session_data is None:
        session_data = st.session_state.get("session_data", {})

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        metrics_rows = (
            f"<div><strong>Session ID:</strong> {str(session_data.get('session_id', 'N/A'))[:8]}</div>"
            f"<div><strong>Started:</strong> {session_data.get('start_time', datetime.now().strftime('%H:%M:%S'))}</div>"
            f"<div><strong>Module:</strong> {str(session_data.get('current_module', 'dashboard')).title()}</div>"
            f"<div><strong>Analyses:</strong> {session_data.get('analysis_count', 0)}</div>"
        )
        _panel("Session Info", "dashboard", metrics_rows)

    with col2:
        metrics = session_data.get("metrics", {})
        metric_rows = (
            f"<div><strong>Total Detections:</strong> {metrics.get('total_detections', 0)}</div>"
            f"<div><strong>Positive Cases:</strong> {metrics.get('positive_cases', 0)}</div>"
            f"<div><strong>Verifications:</strong> {metrics.get('verifications', 0)}</div>"
            f"<div><strong>Reports:</strong> {metrics.get('reports_generated', 0)}</div>"
        )
        _panel("Quick Metrics", "memory", metric_rows)

    with col3:
        if show_analytics:
            analytics = session_data.get("analytics", {})
            analytics_rows = "".join(
                f"<div><strong>{label}:</strong> {analytics.get(key, 0)} scans</div>"
                for key, label in (
                    ("malaria", "Malaria"),
                    ("sickle_cell", "Sickle Cell"),
                    ("all", "ALL"),
                    ("iron_deficiency", "Iron Def"),
                    ("mri", "MRI"),
                    ("ct", "CT"),
                    ("xray", "X-ray"),
                )
            )
            _panel("Analytics", "magnifying_glass_chart", analytics_rows)

    render_html(
        "<div class='footer-credit'>"
        "RaphaID AI v1.0 &nbsp;&middot;&nbsp; CPU-only &nbsp;&middot;&nbsp; Fully offline<br>"
        "Built by Team Devions &nbsp;&middot;&nbsp; NACOS UI &times; DATICAN Competition 2026"
        "</div>"
    )


def update_session_metrics(module: str, result: Dict = None) -> None:
    """Update session metrics after an analysis."""
    if "session_data" not in st.session_state:
        st.session_state.session_data = {
            "session_id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "start_time": datetime.now().strftime("%H:%M:%S"),
            "current_module": "dashboard",
            "analysis_count": 0,
            "metrics": {
                "total_detections": 0,
                "positive_cases": 0,
                "verifications": 0,
                "reports_generated": 0,
            },
            "analytics": {
                "malaria": 0,
                "sickle_cell": 0,
                "all": 0,
                "iron_deficiency": 0,
                "mri": 0,
                "ct": 0,
                "xray": 0,
            },
        }

    session = st.session_state.session_data
    session["analysis_count"] += 1
    session["current_module"] = module

    if result:
        session["metrics"]["total_detections"] += result.get("total_detections", 0)
        if result.get("positive", False):
            session["metrics"]["positive_cases"] += 1

    module_map = {
        "malaria": "malaria",
        "sickle_cell": "sickle_cell",
        "all": "all",
        "iron_deficiency": "iron_deficiency",
        "mri": "mri",
        "ct": "ct",
        "xray": "xray",
    }
    if module in module_map:
        session["analytics"][module_map[module]] += 1
