"""
Splash Screen Component — RaphaID AI Clinical Boot Screen

Renders ONE self-animating, full-screen medical boot overlay using pure CSS
keyframes. No JavaScript, no CDN, no external assets — safe for air-gapped use. Flat solid colours only (single accent, no gradients).

Why single-shot rendering:
    Streamlit strips <script> tags from injected HTML. The previous version
    tried to animate the progress bar with JavaScript, so nothing rendered and
    the screen appeared empty. This version builds one clean single-line HTML
    string (no indentation => Markdown cannot turn it into a code block) and
    animates everything with CSS, so one render call is all that is needed.
"""

import streamlit as st
import time

# ---------------------------------------------------------------------------
# Palette — mirrors app/components/theme.py
# ---------------------------------------------------------------------------
# Single brand accent on deep navy — flat solids only, no gradients.
_ACCENT = "#64ffda"
_TEAL = _ACCENT
_EMERALD = _ACCENT  # unified (was #4ade80)
_CYAN = _ACCENT  # unified (was #38bdf8)
_BG_DARK = "#0a0f1d"
_BG_MID = "#111936"
_TEXT = "#f1f5f9"
_TEXT_DIM = "#94a3b8"
_TEXT_MUTED = "#64748b"
_BORDER = "rgba(100, 255, 218, 0.25)"


def _icon(paths: str, color: str, size: int = 18, width: float = 2) -> str:
    """Build a tiny inline SVG icon on a single line (never indented)."""
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
        f'stroke-linejoin="round">{paths}</svg>'
    )


# Heartbeat glyph paths reused in a few places
_ECG_PATHS = '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'
_MICROSCOPE_PATHS = (
    '<circle cx="12" cy="12" r="5"/><path d="M12 1v2"/><path d="M12 21v2"/>'
    '<path d="M4.22 4.22l1.42 1.42"/><path d="M18.36 18.36l1.42 1.42"/>'
    '<path d="M1 12h2"/><path d="M21 12h2"/><path d="M4.22 19.78l1.42-1.42"/>'
    '<path d="M18.36 5.64l1.42-1.42"/>'
)
_SCAN_PATHS = (
    '<path d="M12 5a3 3 0 1 0-3 3.5"/><path d="M12 5c0 1.38-2 2.5-3 3.5"/>'
    '<circle cx="12" cy="12" r="3"/><path d="M12 15v4"/>'
)
_ASSISTANT_PATHS = (
    '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/>'
    '<path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 10v4"/><path d="M9 10v4"/>'
)


def _build_splash_html(progress: int = 0, status: str = "Booting clinical AI platform...", duration: float = 4.0) -> str:
    """
    Build the full splash overlay as a single-line HTML string.

    Every element is animated with CSS keyframes so no JavaScript is required.

    Args:
        progress: Percentage (0-100) shown in the label and the progress bar.
        status:   Human-readable boot stage shown under the bar.
        duration: Seconds per ECG sweep cycle.
    """
    progress = max(0, min(int(progress), 100))
    status = (
        str(status)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    # Heartbeat trace reused twice: a dim static guide + a bright animated sweep
    ecg_d = (
        "M0 20 L62 20 L74 12 L84 28 L94 20 L118 20 L130 4 L142 36 L153 11 "
        "L164 25 L172 20 L206 20 L218 12 L228 28 L236 20 L380 20"
    )

    css = (
        "<style>"
        # Orb glow pulse
        "@keyframes rpOrb{0%,100%{transform:scale(1);filter:drop-shadow(0 0 20px rgba(100,255,218,.30));}"
        "50%{transform:scale(1.06);filter:drop-shadow(0 0 44px rgba(100,255,218,.55));}}"
        # Rotating dashed scan ring
        "@keyframes rpSpin{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}"
        # Counter-rotating inner ring
        "@keyframes rpSpinRev{from{transform:rotate(360deg);}to{transform:rotate(0deg);}}"
        # ECG sweep across the trace
        "@keyframes rpEcg{0%{stroke-dashoffset:900;}100%{stroke-dashoffset:-140;}}"
        # Progress bar auto-fill
        "@keyframes rpFill{0%{width:0%;}12%{width:14%;}30%{width:34%;}52%{width:56%;}"
        "76%{width:79%;}100%{width:100%;}}"
        # Shimmer travelling along the progress bar
        "@keyframes rpShimmer{0%{transform:translateX(-120%);}100%{transform:translateX(420%);}}"
        # Blinking activity dot
        "@keyframes rpBlink{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.25;transform:scale(.75);}}"
        # Text rise-in
        "@keyframes rpRise{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}"
        # Chip activation glow
        "@keyframes rpChip{0%,100%{box-shadow:0 0 0 rgba(100,255,218,0);}"
        "50%{box-shadow:0 0 18px rgba(100,255,218,.25);}}"
        "</style>"
    )

    orb = (
        '<div style="position:relative;width:132px;height:132px;margin-bottom:18px;'
        'display:flex;align-items:center;justify-content:center;">'
        # outer dashed ring
        f'<div style="position:absolute;inset:-10px;border-radius:50%;border:1.5px dashed {_BORDER};'
        'animation:rpSpin 22s linear infinite;"></div>'
        # inner solid ring, counter-rotating
        f'<div style="position:absolute;inset:-2px;border-radius:50%;'
        f'border:2px solid rgba(100,255,218,.30);border-top-color:{_CYAN};'
        'animation:rpSpinRev 6s linear infinite;"></div>'
        # core orb
        f'<div style="width:106px;height:106px;border-radius:50%;'
        f'background:#12253a;'
        f'border:2px solid {_TEAL};display:flex;align-items:center;justify-content:center;'
        'animation:rpOrb 2.6s ease-in-out infinite;">'
        f'{_icon(_ECG_PATHS, _TEAL, 52, 2.2)}'
        '</div>'
        '</div>'
    )
    title = (
        f'<h1 style="margin:0 0 6px 0;font-size:2.4rem;font-weight:800;letter-spacing:-.02em;'
        f'color:{_TEXT};text-align:center;animation:rpRise .7s ease-out .1s both;">RaphaID '
        f'<span style="color:#64ffda;'
        f'">AI</span></h1>'
    )

    subtitle = (
        '<div style="display:flex;align-items:center;justify-content:center;gap:9px;'
        'margin-bottom:22px;animation:rpRise .7s ease-out .25s both;">'
        f'<span style="width:7px;height:7px;border-radius:50%;background:#64ffda;'
        f'box-shadow:0 0 9px #64ffda;"></span>'
        f'<span style="color:{_TEAL};font-size:.80rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:.20em;">Offline Multi-Disease Clinical Diagnostic Suite</span>'
        '</div>'
    )

    ecg = (
        '<div style="width:392px;max-width:88vw;height:40px;margin-bottom:20px;'
        'animation:rpRise .7s ease-out .4s both;">'
        '<svg width="100%" height="40" viewBox="0 0 380 40" fill="none" '
        'xmlns="http://www.w3.org/2000/svg" style="overflow:visible;">'
        f'<path d="{ecg_d}" stroke="rgba(100,255,218,.16)" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="{ecg_d}" stroke="#64ffda" stroke-width="2.6" '
        'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="150 750" '
        f'style="animation:rpEcg {duration}s linear infinite;"/>'
        ''
        '</svg></div>'
    )

    def chip(paths, colour, label, detail, delay):
        return (
            f'<div style="display:flex;align-items:center;gap:10px;padding:8px 15px;'
            f'background:rgba(255,255,255,.035);border:1px solid rgba(100,255,218,.18);'
            f'border-radius:9px;animation:rpChip 3.2s ease-in-out {delay}s infinite,'
            f'rpRise .7s ease-out {delay}s both;">'
            f'{_icon(paths, colour, 19, 2)}'
            '<div style="text-align:left;">'
            f'<div style="color:{_TEXT};font-size:.75rem;font-weight:700;line-height:1.15;">{label}</div>'
            f'<div style="color:{colour};font-size:.66rem;font-weight:500;">{detail}</div>'
            '</div></div>'
        )

    chips = (
        '<div style="display:flex;gap:12px;margin-bottom:26px;max-width:92vw;flex-wrap:wrap;'
        'justify-content:center;">'
        + chip(_MICROSCOPE_PATHS, _TEAL, "Blood Microscopy", "Malaria &middot; Sickle Cell &middot; ALL", ".55")
        + chip(_SCAN_PATHS, _TEAL, "Radiology AI", "MRI &middot; CT &middot; X-Ray", ".70")
        + chip(_ASSISTANT_PATHS, _TEAL, "Clinical Assistant", "RAG &middot; WHO Guidelines", ".85")
        + '</div>'
    )

    progress_block = (
        '<div style="width:392px;max-width:88vw;margin-bottom:10px;'
        'animation:rpRise .7s ease-out 1s both;">'
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:7px;">'
        f'<span style="color:{_TEXT_DIM};font-size:.76rem;font-weight:600;">Neural Diagnostic Pipeline</span>'
        f'<span style="color:{_TEAL};font-size:.76rem;font-family:monospace;font-weight:700;">'
        f'{progress}%</span></div>'
        '<div style="width:100%;height:8px;background:rgba(35,53,84,.65);border-radius:4px;'
        'overflow:hidden;position:relative;border:1px solid rgba(100,255,218,.18);'
        'box-shadow:inset 0 1px 3px rgba(0,0,0,.6);">'
        f'<div style="width:{progress}%;height:100%;border-radius:4px;'
        f'background:#64ffda;'
        'transition:width .45s cubic-bezier(.35,.15,.25,1);'
        'box-shadow:0 0 14px rgba(100,255,218,.6);"></div>'
        '<div style="position:absolute;top:0;left:0;height:100%;width:80px;'
        'background:rgba(255,255,255,.35);'
        'animation:rpShimmer 1.8s linear infinite;"></div>'
        '</div></div>'
    )

    status_block = (
        '<div style="display:flex;align-items:center;gap:9px;margin-bottom:26px;min-height:1.35rem;'
        'animation:rpRise .7s ease-out 1.2s both;">'
        f'<span style="width:8px;height:8px;border-radius:50%;background:{_TEAL};'
        'animation:rpBlink 1.3s ease-in-out infinite;"></span>'
        f'<span style="color:{_TEXT};font-size:.86rem;font-weight:500;">'
        f'{status}</span></div>'
    )

    badge = (
        '<div style="display:flex;align-items:center;gap:13px;padding:6px 16px;'
        'background:rgba(13,22,45,.65);border:1px solid rgba(100,255,218,.20);border-radius:22px;'
        'animation:rpRise .7s ease-out 1.4s both;">'
        f'<span style="color:{_TEXT_MUTED};font-size:.70rem;letter-spacing:.05em;">'
        'RaphaID v1.0 &middot; Devions</span>'
        '<span style="color:rgba(255,255,255,.15);">|</span>'
        f'<span style="color:{_EMERALD};font-size:.70rem;font-weight:600;display:flex;'
        'align-items:center;gap:5px;">'
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="20 6 9 17 4 12"/></svg>Air-gapped &middot; CPU Only</span>'
        '<span style="color:rgba(255,255,255,.15);">|</span>'
        f'<span style="color:{_TEXT_MUTED};font-size:.70rem;">WHO-aligned</span>'
        '</div>'
    )

    overlay_open = (
        '<div class="raphaid-splash-root" style="position:fixed !important;top:0 !important;'
        'left:0 !important;right:0 !important;bottom:0 !important;width:100vw !important;'
        'height:100vh !important;'
        f'background:#0a0f1d '
        '!important;display:flex !important;flex-direction:column !important;'
        'align-items:center !important;justify-content:center !important;'
        'z-index:2147483000 !important;margin:0 !important;padding:24px !important;'
        'box-sizing:border-box !important;overflow:hidden !important;pointer-events:all !important;'
        'font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif !important;">'
    )

    html = (
        overlay_open + css + orb + title + subtitle + ecg
        + chips + progress_block + status_block + badge + "</div>"
    )

    # Force a single line: the Markdown parser treats 4-space-indented lines as
    # code blocks, which is what previously leaked raw HTML onto the screen.
    return " ".join(html.split())


class SplashController:
    """
    Progressive, real-time boot splash.

    Paints immediately — before the heavy imports (torch, ultralytics,
    sentence-transformers, chromadb ...) — so the browser never sits on
    Streamlit's grey "loading" skeleton during a cold start. The bar then
    advances at *real* checkpoints as each boot stage finishes.

    Typical use at the top of a Streamlit entrypoint::

        splash = SplashController(min_duration=3.5)
        splash.start("Booting RaphaID AI...")
        import torch                      # heavy
        splash.step(24, "Loading deep learning engine...")
        ...
        splash.complete()                 # called from main()

    Safe to call on every rerun: if the splash already played in this browser
    session, ``start`` returns False and all later calls become no-ops.
    """

    def __init__(self, min_duration: float = 3.5, duration: float = 4.0):
        self._min_duration = float(min_duration)
        self._duration = float(duration)
        self._placeholder = None
        self._started_at = 0.0
        self._progress = 0
        self.active = False

    # -- internal ----------------------------------------------------------
    def _render(self, label: str) -> None:
        if self._placeholder is None:
            return
        self._placeholder.markdown(
            _build_splash_html(self._progress, label, self._duration),
            unsafe_allow_html=True,
        )

    # -- public API --------------------------------------------------------
    def start(self, label: str = "Booting clinical AI platform...") -> bool:
        """Paint the splash at once. Returns False if it already played."""
        if st.session_state.get("splash_shown", False):
            return False

        self._placeholder = st.empty()
        self._started_at = time.perf_counter()
        self._progress = 4
        self.active = True
        self._render(label)
        return True

    def step(self, progress: int, label: str) -> None:
        """Advance to a real boot stage. Progress is clamped and monotonic."""
        if not self.active:
            return
        self._progress = max(self._progress, min(int(progress), 99))
        self._render(label)

    def complete(self, label: str = "Clinical workspace ready") -> None:
        """Show 100 %, honour the minimum on-screen time, then remove."""
        if not self.active:
            return
        self._progress = 100
        self._render(label)

        elapsed = time.perf_counter() - self._started_at
        remaining = self._min_duration - elapsed
        if remaining > 0:
            time.sleep(remaining)

        self._placeholder.empty()
        self._placeholder = None
        st.session_state["splash_shown"] = True
        self.active = False


def render_splash_screen(duration: float = 4.0) -> bool:
    """
    Convenience wrapper: show the splash for a fixed time, then clear it.

    Prefer :class:`SplashController` when you want the bar to track real boot
    stages. Kept for simple call sites and backwards compatibility.
    """
    splash = SplashController(min_duration=duration, duration=duration)
    if not splash.start():
        return True
    splash.complete()
    return True


def render_home_button(on_click=None) -> None:
    """
    Standalone Home button that returns to the dashboard.

    The primary Home control lives in app/components/navigation.py; this is an
    optional extra for custom headers or landing layouts.
    """
    if st.button(
        "Home",
        key="home_button_standalone",
        use_container_width=True,
        type="secondary",
        help="Return to main dashboard",
    ):
        if on_click:
            on_click()
        st.session_state["current_module"] = "dashboard"
        st.rerun()


