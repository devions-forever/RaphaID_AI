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
        # Brand - flat dark navy, single teal accent
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;
                    background: #111a2e;
                    border-radius: 12px; border: 1px solid #1f2d44;">
            <div style="font-size: 2.5rem; color: #64ffda; display: inline-flex;">{get_icon("dashboard", "#64ffda", "40", "40")}</div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #e8edf3; margin-top: 0.5rem;">
                RaphaID AI
            </div>
            <div style="font-size: 0.75rem; color: #8a94a6; margin-top: 0.25rem;">
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
            icon_color = "#64ffda" if is_active else "#8a94a6"
            icon_html = get_icon(module_info['icon'], icon_color, "20", "20")
            dot = "#64ffda" if is_active else "#5c6779"
            border = "1px solid #64ffda" if is_active else "1px solid #1f2d44"
            bg = "#0d1528" if is_active else "#111a2e"

            st.markdown(
                f"<div style='display:flex;align-items:center;gap:.6rem;"
                f"padding:.55rem .7rem;margin-bottom:.4rem;border:{border};"
                f"border-radius:8px;background:{bg};'>"
                f"<span style='width:7px;height:7px;border-radius:50%;background:{dot};"
                f"flex-shrink:0;'></span>"
                f"{icon_html}"
                f"<span style='font-weight:{700 if is_active else 600};"
                f"color:{'#64ffda' if is_active else '#e8edf3'};font-size:.92rem;'>"
                f"{module_info['label']}</span></div>",
                unsafe_allow_html=True,
            )
            if st.button(
                module_info['label'],
                key=f"nav_{module_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                on_module_change(module_key)
                st.rerun()

            # Show submodules if active - radio keeps one widget, one rerun
            if is_active and "submodules" in module_info:
                sub_keys = list(module_info["submodules"].keys())
                current_sub = st.session_state.get(f"{module_key}_submodule", sub_keys[0])
                try:
                    idx = sub_keys.index(current_sub)
                except ValueError:
                    idx = 0
                chosen = st.radio(
                    f"{module_info['label']} type",
                    options=sub_keys,
                    format_func=lambda k: module_info["submodules"][k],
                    index=idx,
                    key=f"nav_radio_{module_key}",
                    label_visibility="collapsed",
                )
                if chosen != current_sub:
                    st.session_state[f"{module_key}_submodule"] = chosen
                    st.rerun()

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