"""
Navigation Component — Unified Medical Navigation Rail
Zero duplicate elements, clean clinical branding, inline SVG telemetry.

Contrast contract (enforced together with theme.py):
  * inactive item -> card background, light text
  * active   item -> solid teal fill, deep-navy text  (13.9:1, never white-on-teal)
"""

from functools import partial
from typing import Dict, Callable, Optional

import streamlit as st

from app.components.icons import get_icon
from app.components.htmlkit import render_html
from app.components.status import check_model_status


def _format_submodule(key: str, labels: Dict[str, str], status_map: Dict[str, Dict]) -> str:
    """Label a submodule radio option with its live readiness state.

    Defined at module level and bound with ``functools.partial`` on purpose: a
    closure defined inside the module loop would late-bind ``module_info`` and
    blow up with ``KeyError: 'submodules'`` the moment Streamlit re-evaluates
    the widget on a later rerun.
    """
    base_label = labels.get(key, key)
    is_ready = status_map.get(key, {}).get("ready", False)
    return f"{base_label}  ·  {'Ready' if is_ready else 'Pending'}"


def _brand_header() -> None:
    """Compact deployment-posture strip.

    The rail's sticky header already carries the "RaphaID AI" wordmark, so this
    card only needs to state the mission and the air-gapped posture.
    """
    brand_icon = get_icon("brand", "#64ffda", "22", "22")
    render_html(
        '<div style="background:#111a2e; border:1px solid #1f2d44; border-radius:11px; '
        'padding:0.75rem 0.85rem; margin-bottom:0.35rem; display:flex; align-items:center; '
        'gap:0.7rem;">'
        '<div style="flex:0 0 auto; display:flex; align-items:center; justify-content:center; '
        'width:38px; height:38px; border-radius:10px; background:rgba(100,255,218,0.08); '
        'border:1px solid rgba(100,255,218,0.28);">'
        f"{brand_icon}</div>"
        '<div style="min-width:0;">'
        '<div style="font-size:0.76rem; font-weight:700; color:#e8edf3; line-height:1.35;">'
        "Clinical Decision Support</div>"
        '<div style="font-size:0.68rem; color:#8a94a6; line-height:1.35;">'
        "African Healthcare &middot; Research Use</div>"
        '<div style="margin-top:0.35rem;">'
        '<span style="display:inline-flex; align-items:center; gap:5px; font-size:0.6rem; '
        'font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#64ffda; '
        'border:1px solid rgba(100,255,218,0.3); background:rgba(100,255,218,0.06); '
        'border-radius:999px; padding:2px 8px;">'
        '<span style="width:5px; height:5px; border-radius:50%; background:#64ffda;"></span>'
        "Offline &middot; Air-Gapped</span>"
        "</div></div></div>"
    )


def _section_label(text: str) -> None:
    render_html(f'<div class="rh-nav-label">{text}</div>')


def _telemetry_card(status_map: Dict[str, Dict]) -> None:
    """Compact hardware / engine telemetry block."""
    ready_count = sum(1 for v in status_map.values() if v.get("ready", False))
    total_count = len(status_map) or 1
    pct = int(round(100 * ready_count / total_count))

    items = [
        ("models", "Models", f"{ready_count}/{total_count} Active", ready_count == total_count),
        ("device", "Engine", "CPU / ONNX", None),
        ("ram", "RAM Target", "< 6 GB", None),
        ("offline", "Network", "Air-Gapped", True),
    ]

    rows = "".join(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
                    padding:5px 0; border-bottom:1px solid rgba(31,45,68,0.6);">
            <span style="display:flex; align-items:center; gap:0.5rem; color:#8a94a6;
                         font-size:0.77rem;">
                {get_icon(key, '#64ffda', '15', '15')}<span>{label}</span>
            </span>
            <span style="font-weight:700; font-size:0.75rem; color:{'#64ffda' if flag else '#e8edf3'};">
                {value}
            </span>
        </div>
        """
        for key, label, value, flag in items
    )

    render_html(
        f"""
        <div style="background:#111a2e; border:1px solid #1f2d44; border-radius:10px;
                    padding:0.7rem 0.85rem;">
            {rows}
            <div style="margin-top:0.6rem;">
                <div style="display:flex; justify-content:space-between; font-size:0.68rem;
                            color:#5c6779; margin-bottom:0.3rem;">
                    <span>Weight readiness</span><span>{pct}%</span>
                </div>
                <div style="height:5px; border-radius:3px; background:rgba(255,255,255,0.06);
                            overflow:hidden;">
                    <div style="width:{pct}%; height:100%; border-radius:3px; background:#64ffda;"></div>
                </div>
            </div>
        </div>
        """
    )


def render_navigation(
    current_module: str,
    on_module_change: Callable[[str], None],
    modules: Optional[Dict[str, Dict]] = None,
    on_home_click: Optional[Callable[[], None]] = None,
) -> None:
    """
    Render clinical navigation in the sidebar with single-element module items
    and dynamic readiness indicators.
    """
    if modules is None:
        modules = {
            "dashboard": {
                "label": "Clinical Dashboard",
                "icon": "dashboard",
            },
            "detection": {
                "label": "Blood Pathology",
                "icon": "detection",
                "submodules": {
                    "malaria": "Malaria",
                    "sickle_cell": "Sickle Cell",
                    "all": "ALL Leukemia",
                    "iron_deficiency": "Iron Deficiency",
                },
            },
            "radiology": {
                "label": "Radiology Imaging",
                "icon": "radiology",
                "submodules": {
                    "mri": "MRI Brain",
                    "ct": "CT Chest",
                    "xray": "Chest X-ray",
                },
            },
            "chatbot": {
                "label": "Medical Assistant",
                "icon": "chatbot",
            },
        }

    status_map = check_model_status()

    with st.sidebar:
        _brand_header()
        _section_label("Clinical Modules")

        for module_key, module_info in modules.items():
            is_active = module_key == current_module
            marker = "◆" if is_active else "◇"

            if st.button(
                f"{marker}  {module_info['label']}",
                key=f"nav_{module_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                help=f"Navigate to {module_info['label']}",
            ):
                if module_key == "dashboard" and on_home_click:
                    on_home_click()
                on_module_change(module_key)
                st.rerun()

            # Submodule hierarchy (only under the active module)
            if is_active and "submodules" in module_info:
                sub_labels = dict(module_info["submodules"])
                sub_keys = list(sub_labels.keys())
                current_sub = st.session_state.get(f"{module_key}_submodule", sub_keys[0])
                try:
                    idx = sub_keys.index(current_sub)
                except ValueError:
                    idx = 0

                chosen = st.radio(
                    f"{module_info['label']} selection",
                    options=sub_keys,
                    format_func=partial(
                        _format_submodule, labels=sub_labels, status_map=status_map
                    ),
                    index=idx,
                    key=f"nav_radio_{module_key}",
                    label_visibility="collapsed",
                )
                if chosen != current_sub:
                    st.session_state[f"{module_key}_submodule"] = chosen
                    st.rerun()

        _section_label("System Telemetry")
        _telemetry_card(status_map)

        # Generous bottom breathing room + build stamp (fixes cramped sidebar foot)
        render_html(
            """
            <div style="height:1.75rem;"></div>
            <div style="border-top:1px solid #1f2d44; padding-top:0.7rem; margin-bottom:2.25rem;
                        text-align:center; font-size:0.68rem; color:#5c6779; line-height:1.7;">
                RaphaID AI <span style="color:#8a94a6;">v1.0</span><br>
                Team Devions &middot; NACOS UI &times; DATICAN 2026
            </div>
            """
        )


def render_module_tabs(module_key: str, submodules: Dict[str, str]) -> str:
    """Render tabs for submodules within a module."""
    tabs = st.tabs(list(submodules.values()))
    for i, (sub_key, sub_label) in enumerate(submodules.items()):
        with tabs[i]:
            pass
    return list(submodules.keys())[0]
