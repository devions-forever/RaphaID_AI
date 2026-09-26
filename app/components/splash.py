"""
Splash Screen Component — 5-Second Medical Loading Screen
Displays branding and initialization status.
Uses inline SVGs - no external dependencies.
"""

import streamlit as st
import time
from typing import Optional


def render_splash_screen(duration: float = 5.0) -> bool:
    """
    Render a splash screen for the specified duration.
    
    Args:
        duration: Time in seconds to display splash screen
        
    Returns:
        True if splash screen completed, False if skipped
    """
    # Check if splash was already shown this session
    if st.session_state.get("splash_shown", False):
        return True
    
    # Placeholder for splash content
    splash_placeholder = st.empty()
    
    colors = {
        "bg_primary": "#0d0d1a",
        "bg_secondary": "#16213e",
        "bg_card": "#1a1a2e",
        "accent_teal": "#64ffda",
        "accent_emerald": "#4ade80",
        "text_primary": "#D8DEE9",
        "text_secondary": "#8892b0",
        "border_subtle": "#233554",
    }
    
    splash_html = f"""
    <div style="
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, {colors['bg_primary']}, {colors['bg_secondary']}, {colors['bg_card']});
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    ">
        <!-- Logo -->
        <div style="
            width: 120px; height: 120px;
            border-radius: 50%;
            background: linear-gradient(135deg, {colors['accent_teal']}, {colors['accent_emerald']});
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 0 60px rgba(100, 255, 218, 0.4), 0 0 100px rgba(74, 222, 128, 0.2);
            animation: pulse 2s ease-in-out infinite;
        ">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#0d0d1a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
                <circle cx="12" cy="12" r="3"/>
            </svg>
        </div>
        
        <style>
            @keyframes pulse {{
                0%, 100% {{ box-shadow: 0 0 60px rgba(100, 255, 218, 0.4), 0 0 100px rgba(74, 222, 128, 0.2); }}
                50% {{ box-shadow: 0 0 80px rgba(100, 255, 218, 0.6), 0 0 120px rgba(74, 222, 128, 0.3); }}
            }}
            @keyframes fadeInUp {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
        
        <!-- Title -->
        <h1 style="
            color: {colors['text_primary']};
            font-size: 2.5rem;
            font-weight: 800;
            margin: 1.5rem 0 0.5rem;
            letter-spacing: -0.02em;
            animation: fadeInUp 0.6s ease-out 0.2s both;
        ">RaphaID AI</h1>
        
        <!-- Subtitle -->
        <p style="
            color: {colors['accent_teal']};
            font-size: 1.1rem;
            font-weight: 500;
            margin: 0 0 2rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            animation: fadeInUp 0.6s ease-out 0.4s both;
        ">Offline Multi-Disease Diagnostic</p>
        
        <!-- Loading Bar -->
        <div style="
            width: 300px;
            height: 4px;
            background: {colors['border_subtle']};
            border-radius: 2px;
            overflow: hidden;
            animation: fadeInUp 0.6s ease-out 0.6s both;
        ">
            <div id="splash-progress" style="
                width: 0%;
                height: 100%;
                background: linear-gradient(90deg, {colors['accent_teal']}, {colors['accent_emerald']});
                border-radius: 2px;
                transition: width 0.1s linear;
            "></div>
        </div>
        
        <!-- Status Text -->
        <p id="splash-status" style="
            color: {colors['text_secondary']};
            font-size: 0.85rem;
            margin-top: 1rem;
            animation: fadeInUp 0.6s ease-out 0.8s both;
        ">Initializing medical AI systems...</p>
        
        <!-- Version -->
        <p style="
            color: {colors['text_secondary']};
            font-size: 0.7rem;
            margin-top: 2rem;
            opacity: 0.6;
        ">RaphaID v1(PalsmoId ) · Devions</p>
    </div>
    """
    
    splash_placeholder.markdown(splash_html, unsafe_allow_html=True)
    
    # Simulate loading with progress updates
    status_messages = [
        "Loading neural network weights...",
        "Initializing detection modules...",
        "Preparing radiology engines...",
        "Loading medical knowledge base...",
        "Calibrating clinical workflows...",
        "System ready",
    ]
    
    steps = len(status_messages)
    for i, msg in enumerate(status_messages):
        progress = int(((i + 1) / steps) * 100)
        
        # Update progress bar and status via JavaScript
        update_js = f"""
        <script>
            const progressEl = document.getElementById('splash-progress');
            const statusEl = document.getElementById('splash-status');
            if (progressEl) progressEl.style.width = '{progress}%';
            if (statusEl) statusEl.textContent = '{msg}';
        </script>
        """
        splash_placeholder.markdown(splash_html + update_js, unsafe_allow_html=True)
        time.sleep(duration / steps)
    
    # Mark splash as shown
    st.session_state["splash_shown"] = True
    
    # Clear splash
    splash_placeholder.empty()
    
    return True


def render_home_button(on_click=None) -> None:
    """
    Render a home button that returns to dashboard.
    Can be placed in sidebar or header.
    """
    if st.button(
        "Home",
                key="home_button",
        use_container_width=True,
        type="secondary",
        help="Return to main dashboard",
    ):
        if on_click:
            on_click()
        st.session_state["current_module"] = "dashboard"
        st.rerun()