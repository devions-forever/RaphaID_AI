"""
Navigation Component — Unified Medical Navigation Rail
Zero duplicate elements, clean clinical branding, inline SVG telemetry.
"""

from typing import Dict, Callable, Optional
import streamlit as st

from app.components.icons import get_icon
from app.components.status import check_model_status


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
        # Brand Header — Medical Cross & Pulse Insignia
        brand_icon = get_icon("brand", "#64ffda", "32", "32")
        st.markdown(f"""
        <div style="text-align: center; padding: 1.1rem 0.8rem; margin-bottom: 0.8rem;
                    background: #111a2e; border-radius: 12px; border: 1px solid #1f2d44;">
            <div style="display: inline-flex; align-items: center; justify-content: center;
                        width: 48px; height: 48px; border-radius: 12px;
                        background: rgba(100, 255, 218, 0.08); border: 1px solid rgba(100, 255, 218, 0.25);
                        margin-bottom: 0.5rem;">
                {brand_icon}
            </div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.01em;">
                RaphaID AI
            </div>
            <div style="font-size: 0.72rem; color: #8a94a6; margin-top: 0.2rem;">
                Clinical Decision Support · African Healthcare
            </div>
            <div style="margin-top: 0.6rem;">
                <span class="rh-badge" style="color: #64ffda; border-color: rgba(100, 255, 218, 0.3); background: rgba(100, 255, 218, 0.06); font-size: 0.68rem;">
                    OFFLINE · AIR-GAPPED
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Main Navigation List
        st.markdown(
            "<div style='font-size: 0.72rem; font-weight: 700; color: #8a94a6; "
            "text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem; padding-left: 0.2rem;'>"
            "Clinical Modules</div>",
            unsafe_allow_html=True,
        )

        for module_key, module_info in modules.items():
            is_active = module_key == current_module
            dot = "●" if is_active else "○"

            if st.button(
                f"{dot}  {module_info['label']}",
                key=f"nav_{module_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                help=f"Navigate to {module_info['label']}",
            ):
                if module_key == "dashboard" and on_home_click:
                    on_home_click()
                on_module_change(module_key)
                st.rerun()

            # Submodule hierarchy (only under active module)
            if is_active and "submodules" in module_info:
                sub_keys = list(module_info["submodules"].keys())
                current_sub = st.session_state.get(f"{module_key}_submodule", sub_keys[0])
                try:
                    idx = sub_keys.index(current_sub)
                except ValueError:
                    idx = 0

                def format_sub(key: str) -> str:
                    base_label = module_info["submodules"][key]
                    is_ready = status_map.get(key, {}).get("ready", False)
                    status_text = "Ready" if is_ready else "Pending"
                    return f"{base_label} ({status_text})"

                chosen = st.radio(
                    f"{module_info['label']} selection",
                    options=sub_keys,
                    format_func=format_sub,
                    index=idx,
                    key=f"nav_radio_{module_key}",
                    label_visibility="collapsed",
                )
                if chosen != current_sub:
                    st.session_state[f"{module_key}_submodule"] = chosen
                    st.rerun()

        st.markdown("---")

        # System Hardware & Engine Telemetry
        st.markdown(
            "<div style='font-size: 0.72rem; font-weight: 700; color: #8a94a6; "
            "text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem; padding-left: 0.2rem;'>"
            "System Telemetry</div>",
            unsafe_allow_html=True,
        )

        ready_count = sum(1 for v in status_map.values() if v.get("ready", False))
        total_count = len(status_map)

        status_items = [
            ("models", "Models", f"{ready_count}/{total_count} Active"),
            ("device", "Engine", "CPU / ONNX"),
            ("ram", "RAM Target", "< 6 GB"),
            ("offline", "Network", "Air-Gapped"),
        ]

        st.markdown("""
        <div style="background: #111a2e; border: 1px solid #1f2d44; border-radius: 8px; padding: 0.6rem 0.8rem;">
        """ + "".join([
            f"""<div style="font-size: 0.78rem; padding: 3px 0; display: flex; justify-content: space-between; align-items: center;">
                <span style="display: flex; align-items: center; gap: 0.45rem; color: #8a94a6;">
                    {get_icon(key, '#64ffda', '16', '16')}
                    <span>{label}</span>
                </span>
                <span style="font-weight: 600; color: {'#64ffda' if 'Air-Gapped' in val or 'Active' in val else '#e8edf3'}; font-size: 0.76rem;">
                    {val}
                </span>
            </div>""" for key, label, val in status_items
        ]) + "</div>", unsafe_allow_html=True)


def render_module_tabs(module_key: str, submodules: Dict[str, str]) -> str:
    """Render tabs for submodules within a module."""
    tabs = st.tabs(list(submodules.values()))
    for i, (sub_key, sub_label) in enumerate(submodules.items()):
        with tabs[i]:
            pass
    return list(submodules.keys())[0]