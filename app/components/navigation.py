"""
Navigation Component — 3-Module Dropdown Navigation with Inline SVG Medical Icons
No external dependencies - uses inline SVGs for reliability.
"""

import streamlit as st
from typing import Dict, Callable, Optional

from app.components.icons import get_icon


def render_navigation(
    current_module: str,
    on_module_change: Callable[[str], None],
    modules: Dict[str, Dict] = None,
    on_home_click: Optional[Callable[[], None]] = None,
) -> None:
    """
    Render the 3-module navigation with dropdowns and home button.
    Uses inline SVG icons - no external dependencies.
    """
    if modules is None:
        modules = {
            "detection": {
                "label": "Detection",
                "icon": "detection",
                "submodules": {
                    "malaria": "Malaria",
                    "sickle_cell": "Sickle Cell",
                    "all": "ALL Leukemia",
                    "iron_deficiency": "Iron Deficiency",
                },
            },
            "radiology": {
                "label": "Radiology",
                "icon": "radiology",
                "submodules": {
                    "mri": "MRI Brain",
                    "ct": "CT Chest",
                    "xray": "X-ray Chest",
                },
            },
            "chatbot": {
                "label": "Medical Assistant",
                "icon": "chatbot",
                "submodules": {
                    "assistant": "AI Assistant",
                },
            },
        }

    with st.sidebar:
        # Logo/Brand with medical icon
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;
                    background: linear-gradient(135deg, #0d0d1a, #1a1a2e);
                    border-radius: 12px; border: 1px solid #233554;">
            <div style="font-size: 2.5rem; color: #64ffda; display: inline-flex;">{get_icon("dashboard", "#64ffda", "40", "40")}</div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #64ffda; margin-top: 0.5rem;">
                RaphaID AI
            </div>
            <div style="font-size: 0.75rem; color: #8892b0; margin-top: 0.25rem;">
                Offline Multi-Disease Diagnostic
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Home Button (always visible except on dashboard)
        if current_module != "dashboard":
            if st.button(
                "Home",
                key="nav_home",
                use_container_width=True,
                type="secondary",
                help="Return to main dashboard",
            ):
                if on_home_click:
                    on_home_click()
                st.session_state["current_module"] = "dashboard"
                st.rerun()
            st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

        st.markdown("---")

        # Main module selection
        st.markdown("### Modules")

        for module_key, module_info in modules.items():
            is_active = module_key == current_module
            icon_color = "#64ffda" if is_active else "#8892b0"
            
            # Render button with inline SVG icon
            icon_html = get_icon(module_info['icon'], icon_color, "22", "22")
            
            # Use a container to show icon + text properly
            col1, col2 = st.columns([0.15, 0.85])
            with col1:
                st.markdown(f"<div style='text-align: center; padding-top: 0.4rem;'>{icon_html}</div>", unsafe_allow_html=True)
            with col2:
                if st.button(
                    module_info['label'],
                    key=f"nav_{module_key}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    on_module_change(module_key)
                    st.rerun()

            # Show submodules if active
            if is_active and "submodules" in module_info:
                st.markdown("<div style='margin-left: 0.5rem; margin-bottom: 0.5rem;'>", unsafe_allow_html=True)
                for sub_key, sub_label in module_info["submodules"].items():
                    sub_icon = get_icon(sub_key, "#8892b0", "18", "18")
                    
                    scol1, scol2 = st.columns([0.15, 0.85])
                    with scol1:
                        st.markdown(f"<div style='text-align: center; padding-top: 0.3rem;'>{sub_icon}</div>", unsafe_allow_html=True)
                    with scol2:
                        if st.button(
                            sub_label,
                            key=f"nav_{module_key}_{sub_key}",
                            use_container_width=True,
                            type="secondary",
                        ):
                            st.session_state[f"{module_key}_submodule"] = sub_key
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Quick status with medical icons
        st.markdown("### System Status")
        status_items = [
            ("models", "Models", "Lazy Loaded"),
            ("device", "Device", "CPU"),
            ("ram", "RAM", "< 6GB Target"),
            ("offline", "Offline", "Ready"),
        ]
        for key, label, value in status_items:
            icon_html = get_icon(key, "#4ade80", "18", "18")
            st.markdown(
                f"<div style='font-size: 0.8rem; color: #8892b0; "
                f"padding: 4px 0; display: flex; justify-content: space-between; align-items: center;'>"
                f"<span style='display: flex; align-items: center; gap: 0.5rem;'>{icon_html} {label}</span>"
                f"<span>{value}</span></div>",
                unsafe_allow_html=True
            )


def render_module_tabs(module_key: str, submodules: Dict[str, str]) -> str:
    """Render tabs for submodules within a module."""
    tabs = st.tabs(list(submodules.values()))
    for i, (sub_key, sub_label) in enumerate(submodules.items()):
        with tabs[i]:
            pass
    return list(submodules.keys())[0]