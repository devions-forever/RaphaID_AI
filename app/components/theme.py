"""
Clinical Theme — Flat Dark Theme for RaphaID AI
Single accent teal (#64FFDA), safety red (#F87171) for errors/alerts only.
Strictly zero gradients. Medical PACS/workstation density and precision.

IMPORTANT — why this file uses ``string.Template`` instead of an f-string:
The previous revision built the stylesheet with an f-string and forgot to
escape the CSS braces after the button section, so Python evaluated
``{ background-color: ... }`` as an f-string expression and raised
``NameError: name 'background' is not defined`` at runtime. ``Template``
leaves ``{`` / ``}`` completely alone and only substitutes ``$tokens``,
which makes that whole class of bug impossible.
"""

from string import Template

import streamlit as st


def get_theme_colors() -> dict:
    """Return the clinical colour palette — flat navy + single teal accent."""
    return {
        # Background (locked)
        "bg_primary": "#0A0F1D",
        "bg_secondary": "#0D1528",
        "bg_card": "#111A2E",
        "bg_hover": "#16213E",
        "bg_elevated": "#16203A",
        # Text
        "text_primary": "#E8EDF3",
        "text_secondary": "#8A94A6",
        "text_muted": "#5C6779",
        "text_accent": "#64FFDA",
        # Text used ON the teal accent fill (13.9:1 contrast)
        "text_on_accent": "#08111F",
        # Accents — single teal + safety red only
        "accent_teal": "#64FFDA",
        "accent_teal_strong": "#52E0BE",
        "accent_emerald": "#64FFDA",
        "accent_red": "#F87171",
        "accent_orange": "#64FFDA",
        "accent_yellow": "#64FFDA",
        "accent_purple": "#8A94A6",
        # Borders
        "border_subtle": "#1F2D44",
        "border_strong": "#2A3B57",
        "border_accent": "#64FFDA",
        # Status
        "success": "#64FFDA",
        "warning": "#8A94A6",
        "error": "#F87171",
        "info": "#64FFDA",
    }


_CSS_TEMPLATE = Template("""
/* ============================================================
   0. TOKENS
============================================================ */
:root {
    --rh-bg: $bg_primary;
    --rh-bg-2: $bg_secondary;
    --rh-card: $bg_card;
    --rh-hover: $bg_hover;
    --rh-border: $border_subtle;
    --rh-border-strong: $border_strong;
    --rh-text: $text_primary;
    --rh-text-2: $text_secondary;
    --rh-text-3: $text_muted;
    --rh-accent: $accent_teal;
    --rh-on-accent: $text_on_accent;
    --rh-danger: $accent_red;
    --rh-radius: 10px;
}

/* ============================================================
   1. GLOBAL SHELL
============================================================ */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stHeader"], [data-testid="stToolbar"],
.main, .block-container {
    background-color: $bg_primary !important;
    color: $text_primary !important;
}

[data-testid="stAppViewContainer"] > .main .block-container,
.main .block-container,
.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    padding-left: 2.4rem !important;
    padding-right: 2.4rem !important;
    max-width: 1320px !important;
    /* Keep the workspace centred whether or not the sidebar is collapsed.
       (A hard-coded sidebar width here was what stopped the main pane from
        expanding when the rail was hidden.) */
    margin-left: auto !important;
    margin-right: auto !important;
    width: 100% !important;
}

/* Collapsed rail: Streamlit floats a "reopen" chevron in the top-left corner.
   The workspace gets extra gutters, and the header keeps its full-bleed
   background but reserves left padding so the chevron never sits on top of
   the header's content. */
body:has([data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stMain"] .block-container {
    padding-left: 4.6rem !important;
    padding-right: 4rem !important;
}
body:has([data-testid="stSidebar"][aria-expanded="false"]) .rh-topbar {
    margin: 0 -4rem 1.2rem -4.6rem !important;
    padding-left: 3.4rem !important;
    padding-right: 3.4rem !important;
}

/* NOTE: do NOT raise [data-testid="stSidebarCollapsedControl"] with z-index.
   Streamlit relies on the expanded sidebar painting over it — lifting it makes
   a second, stray chevron appear on top of the sidebar while it is open. */

section.main, [data-testid="stAppViewContainer"] > .main { width: 100% !important; }

[data-testid="stDecoration"] { display: none !important; }

/* ============================================================
   HEADER
   The empty Streamlit header band is removed. The clinical bar
   (.rh-topbar) IS the header now: it is the first element in the main
   pane and sticks to the very top. Streamlit's header element is kept at
   zero height purely so the animated running indicator can live in the
   top-right corner of that header on every page.
============================================================ */
[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
    border: none !important;
    overflow: visible !important;
    backdrop-filter: none !important;
    pointer-events: none !important;
    z-index: 999990 !important;
}
[data-testid="stToolbar"], [data-testid="stMainMenu"] { display: none !important; }

/* The top-right running indicator — the animated "system is working" cue and
   its "Running..." label. Pinned to the viewport so it floats over the header
   even though its parent has zero height. Visibility is left to Streamlit, so
   it still appears only while the script is executing. */
[data-testid="stStatusWidget"] {
    position: fixed !important;
    top: 0.8rem !important;
    right: 1.4rem !important;
    z-index: 2147483000 !important;
    pointer-events: auto !important;
    background: $bg_card !important;
    border: 1px solid $border_subtle !important;
    border-radius: 999px !important;
    padding: 2px 12px !important;
    margin: 0 !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.35) !important;
}
[data-testid="stStatusWidget"] * { color: $text_primary !important; }
[data-testid="stStatusWidget"] svg,
[data-testid="stStatusWidget"] img { fill: $accent_teal !important; }

/* Global type */
html, body, [class*="css"] {
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
}

.main .block-container h2 { margin-top: 1.5rem; margin-bottom: 0.7rem; }
.main .block-container h3 {
    margin-top: 1.35rem;
    margin-bottom: 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid $border_subtle;
    font-size: 1.12rem !important;
}
.main .block-container h2:first-child,
.main .block-container h3:first-child { margin-top: 0.2rem; }

/* Keep Streamlit-native text readable */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] .stMarkdown { color: $text_primary; }

a { color: $accent_teal !important; text-decoration: none; }
a:hover { text-decoration: underline; }

code {
    background: $bg_card !important;
    color: $accent_teal !important;
    padding: 1px 6px;
    border-radius: 5px;
    border: 1px solid $border_subtle;
    font-size: 0.85em;
}

/* ============================================================
   2. SIDEBAR SHELL  (spacing + bottom breathing room)
============================================================ */
[data-testid="stSidebar"] {
    background-color: $bg_primary !important;
    border-right: 1px solid $border_subtle !important;
}

/* Only pin the width while the rail is expanded — forcing it unconditionally
   prevented Streamlit from collapsing the sidebar. */
[data-testid="stSidebar"][aria-expanded="true"] {
    width: 300px !important;
    min-width: 300px !important;
}

[data-testid="stSidebar"] > div { background-color: $bg_primary !important; }

[data-testid="stSidebar"] [data-testid="stSidebarContent"] { overflow-x: hidden; }

/* --- STICKY SIDEBAR HEADER -------------------------------------------
   stSidebarContent is the sidebar's scroll container and stSidebarHeader is
   its direct child, so making it sticky keeps the collapse control reachable
   at any scroll position. It scrolls away with the rail when collapsed. */
[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
    position: sticky !important;
    top: 0 !important;
    z-index: 30 !important;
    height: auto !important;
    min-height: 2.9rem !important;
    background: $bg_primary !important;
    border-bottom: 1px solid $border_subtle !important;
    padding: 0.45rem 0.7rem 0.45rem 0.95rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
}

/* Title for the sticky rail header (no widget available inside it). */
[data-testid="stSidebar"] [data-testid="stSidebarHeader"]::before {
    content: "RaphaID AI";
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: $text_muted;
    white-space: nowrap;
}

/* Streamlit reserves this for the app logo, which RaphaID renders itself. */
[data-testid="stSidebar"] [data-testid="stLogoSpacer"] { display: none !important; }

/* Streamlit only reveals the collapse control on hover — keep it permanent so
   the rail can always be closed, at any scroll position. */
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
    display: block !important;
    height: auto !important;
    width: auto !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 1.85rem !important;
    height: 1.85rem !important;
    min-height: 1.85rem !important;
    padding: 0 !important;
    border-radius: 7px !important;
    background: $bg_card !important;
    border: 1px solid $border_subtle !important;
    color: $text_secondary !important;
    transition: border-color 0.15s ease, color 0.15s ease !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover {
    border-color: $accent_teal !important;
    color: $accent_teal !important;
    background: $bg_hover !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button svg {
    color: inherit !important;
    fill: currentColor !important;
    width: 16px !important;
    height: 16px !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding: 0.9rem 0.95rem 3.5rem 0.95rem !important;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { row-gap: 0.3rem !important; }

/* Sidebar section labels */
.rh-nav-label {
    font-size: 0.68rem;
    font-weight: 800;
    color: $text_muted;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 1.1rem 0 0.55rem 0;
    padding-left: 0.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.rh-nav-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: $border_subtle;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    margin: 1.1rem 0 !important;
    border-top: 1px solid $border_subtle !important;
}

/* ============================================================
   3. SIDEBAR NAVIGATION BUTTONS  (contrast-critical)
============================================================ */
[data-testid="stSidebar"] div[data-testid="stButton"] { margin-bottom: 0.5rem !important; }

[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    background-color: $bg_card !important;
    background-image: none !important;
    color: $text_primary !important;
    -webkit-text-fill-color: $text_primary !important;
    border: 1px solid $border_subtle !important;
    border-radius: 9px !important;
    padding: 0.7rem 0.95rem !important;
    min-height: 2.75rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    text-align: left !important;
    justify-content: flex-start !important;
    box-shadow: none !important;
    width: 100% !important;
    transition: background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button p,
[data-testid="stSidebar"] div[data-testid="stButton"] > button span,
[data-testid="stSidebar"] div[data-testid="stButton"] > button div,
[data-testid="stSidebar"] div[data-testid="stButton"] > button [data-testid="stMarkdownContainer"] * {
    color: $text_primary !important;
    -webkit-text-fill-color: $text_primary !important;
    font-weight: 600 !important;
    margin: 0 !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
    background-color: $bg_hover !important;
    border-color: rgba(100, 255, 218, 0.55) !important;
}
[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover p,
[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover span,
[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover div,
[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover [data-testid="stMarkdownContainer"] * {
    color: $accent_teal !important;
    -webkit-text-fill-color: $accent_teal !important;
}

/* --- ACTIVE NAV ITEM: teal fill + near-black navy text (13.9:1) ---
   Streamlit paints primary-button labels white by default, which is what
   made the active nav label unreadable on the teal fill. Every descendant
   is forced dark, including the Markdown container wrapper.            */
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"],
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:hover,
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:focus,
[data-testid="stSidebar"] div[data-testid="stButton"] > button[data-testid="baseButton-primary"],
[data-testid="stSidebar"] div[data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover {
    background-color: $accent_teal !important;
    background-image: none !important;
    border: 1px solid $accent_teal !important;
    box-shadow: 0 2px 12px rgba(100, 255, 218, 0.22) !important;
    font-weight: 800 !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] p,
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] span,
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] div,
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] svg,
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] [data-testid="stMarkdownContainer"] *,
[data-testid="stSidebar"] div[data-testid="stButton"] > button[data-testid="baseButton-primary"] p,
[data-testid="stSidebar"] div[data-testid="stButton"] > button[data-testid="baseButton-primary"] span,
[data-testid="stSidebar"] div[data-testid="stButton"] > button[data-testid="baseButton-primary"] div,
[data-testid="stSidebar"] div[data-testid="stButton"] > button[data-testid="baseButton-primary"] [data-testid="stMarkdownContainer"] * {
    color: $text_on_accent !important;
    -webkit-text-fill-color: $text_on_accent !important;
    font-weight: 800 !important;
    stroke: $text_on_accent !important;
    fill: $text_on_accent !important;
}

/* --- Submodule radio pills --- */
[data-testid="stSidebar"] div[data-testid="stRadio"] {
    background: $bg_secondary !important;
    border-left: 2px solid $accent_teal !important;
    border-radius: 0 9px 9px 0 !important;
    padding: 0.6rem 0.75rem 0.6rem 0.7rem !important;
    margin: 0.1rem 0 0.95rem 0.35rem !important;
}

[data-testid="stSidebar"] div[data-testid="stRadio"] > div { gap: 0.15rem !important; }

[data-testid="stSidebar"] div[data-testid="stRadio"] label {
    border-radius: 7px !important;
    padding: 0.35rem 0.45rem !important;
    transition: background-color 0.15s ease !important;
}
[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
    background: rgba(100, 255, 218, 0.06) !important;
}

[data-testid="stSidebar"] div[data-testid="stRadio"] label p,
[data-testid="stSidebar"] div[data-testid="stRadio"] label span,
[data-testid="stSidebar"] div[data-testid="stRadio"] label div {
    color: $text_secondary !important;
    -webkit-text-fill-color: $text_secondary !important;
    font-size: 0.83rem !important;
}
[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover p,
[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover span {
    color: $accent_teal !important;
    -webkit-text-fill-color: $accent_teal !important;
}

/* ============================================================
   4. BUTTONS (global)
   Selectors are descendant-based ("[data-testid=...] button") because
   Streamlit wraps the <button> in tooltip/overlay divs on some releases,
   which silently defeated the old ".stButton > button" child selectors.
============================================================ */
[data-testid="stButton"] button,
[data-testid="stDownloadButton"] button,
[data-testid="stFormSubmitButton"] button {
    background-color: $bg_card !important;
    background-image: none !important;
    color: $text_primary !important;
    -webkit-text-fill-color: $text_primary !important;
    border: 1px solid $border_subtle !important;
    border-radius: 9px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.01em !important;
    transition: border-color 0.2s ease, background-color 0.2s ease, color 0.2s ease !important;
    box-shadow: none !important;
}

[data-testid="stButton"] button p,
[data-testid="stButton"] button span,
[data-testid="stButton"] button div,
[data-testid="stDownloadButton"] button p,
[data-testid="stDownloadButton"] button span,
[data-testid="stDownloadButton"] button div {
    color: $text_primary !important;
    -webkit-text-fill-color: $text_primary !important;
}

[data-testid="stButton"] button:hover,
[data-testid="stDownloadButton"] button:hover {
    background-color: $bg_hover !important;
    border-color: $accent_teal !important;
}
[data-testid="stButton"] button:hover p,
[data-testid="stButton"] button:hover span,
[data-testid="stDownloadButton"] button:hover p,
[data-testid="stDownloadButton"] button:hover span {
    color: $accent_teal !important;
    -webkit-text-fill-color: $accent_teal !important;
}

[data-testid="stButton"] button:focus:not(:active) {
    border-color: $accent_teal !important;
    box-shadow: 0 0 0 2px rgba(100, 255, 218, 0.25) !important;
}

/* --- PRIMARY BUTTONS: solid teal fill + deep navy label, app-wide.
   This is the readability fix: Streamlit's own theme paints primary-button
   labels WHITE, which is unreadable on the teal fill. Every descendant is
   forced dark, including the Markdown container Streamlit wraps the label in. */
button[kind="primary"],
button[kind="primaryFormSubmit"],
button[data-testid="baseButton-primary"],
button[data-testid="baseButton-primaryFormSubmit"] {
    background-color: $accent_teal !important;
    background-image: none !important;
    border: 1px solid $accent_teal !important;
    font-weight: 800 !important;
    box-shadow: none !important;
}

button[kind="primary"]:hover,
button[kind="primaryFormSubmit"]:hover,
button[data-testid="baseButton-primary"]:hover,
button[data-testid="baseButton-primaryFormSubmit"]:hover {
    background-color: $accent_teal_strong !important;
    border-color: $accent_teal_strong !important;
    box-shadow: 0 2px 10px rgba(100, 255, 218, 0.22) !important;
}

button[kind="primary"],
button[kind="primary"] *,
button[kind="primary"] p,
button[kind="primary"] span,
button[kind="primary"] div,
button[kind="primary"] svg,
button[kind="primary"] [data-testid="stMarkdownContainer"],
button[kind="primary"] [data-testid="stMarkdownContainer"] *,
button[kind="primaryFormSubmit"],
button[kind="primaryFormSubmit"] *,
button[kind="primaryFormSubmit"] p,
button[kind="primaryFormSubmit"] span,
button[kind="primaryFormSubmit"] div,
button[kind="primaryFormSubmit"] [data-testid="stMarkdownContainer"] *,
button[data-testid="baseButton-primary"],
button[data-testid="baseButton-primary"] *,
button[data-testid="baseButton-primary"] [data-testid="stMarkdownContainer"] *,
button[data-testid="baseButton-primaryFormSubmit"],
button[data-testid="baseButton-primaryFormSubmit"] * {
    color: $text_on_accent !important;
    -webkit-text-fill-color: $text_on_accent !important;
    stroke: $text_on_accent !important;
    fill: $text_on_accent !important;
}

/* Disabled */
[data-testid="stButton"] button:disabled,
[data-testid="stButton"] button[disabled],
[data-testid="stDownloadButton"] button:disabled {
    background-color: $bg_secondary !important;
    border-color: $border_subtle !important;
    cursor: not-allowed !important;
    box-shadow: none !important;
}
[data-testid="stButton"] button:disabled p,
[data-testid="stButton"] button:disabled span,
[data-testid="stButton"] button[disabled] p,
[data-testid="stButton"] button[disabled] span {
    color: $text_muted !important;
    -webkit-text-fill-color: $text_muted !important;
}
/* ============================================================
   5. CLINICAL HEADER BAR — this IS the app header (sticky, per-page)
============================================================ */
/* Streamlit wraps every st.markdown in a container that is exactly as tall as
   its content, and a sticky element can only travel inside its parent's box.
   So the stickiness has to live on the WRAPPER, not on .rh-topbar itself —
   otherwise the header scrolls away with its own 50px-tall parent. */
div[data-testid="stElementContainer"]:has(
    > div[data-testid="stMarkdown"]
    > div[data-testid="stMarkdownContainer"]
    > .rh-topbar
) {
    position: sticky !important;
    top: 0 !important;
    z-index: 900 !important;
}

.rh-topbar {
    display: flex;
    align-items: center;
    justify-content: center;   /* header content is centred, not pushed to the edges */
    gap: 2.4rem;
    flex-wrap: wrap;
    background: $bg_secondary !important;
    border: none;
    border-bottom: 1px solid $border_subtle;
    border-radius: 0 0 14px 14px;
    padding: 0.7rem 2rem;
    margin: 0 -2.4rem 1.2rem -2.4rem; /* full-bleed across the content pane */
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.28);
}

/* ============================================================
   5b. SPLASH OVERLAY
   The hard overrides live here, NOT inline: Streamlit's HTML pipeline drops
   any inline style attribute containing "!important", which used to strip the
   overlay's positioning and break its centring.
============================================================ */
.raphaid-splash-root {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    background: $bg_primary !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    z-index: 2147483000 !important;
    margin: 0 !important;
    padding: 24px !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}
.rh-topbar-group { display: flex; align-items: center; gap: 0.65rem; flex-wrap: wrap; }
.rh-topbar-item {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.78rem;
    color: $text_secondary;
    white-space: nowrap;
}
.rh-topbar-item strong { color: $text_primary; font-weight: 700; }
.rh-topbar-item .rh-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: $accent_teal; box-shadow: 0 0 8px rgba(100, 255, 218, 0.6);
}
.rh-topbar-sep { width: 1px; height: 18px; background: $border_subtle; }
.rh-topbar-chip {
    display: inline-flex; align-items: center; gap: 0.4rem;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 3px 10px; border-radius: 999px;
    border: 1px solid rgba(100, 255, 218, 0.3);
    background: rgba(100, 255, 218, 0.07);
    color: $accent_teal;
}
.rh-topbar-chip.is-muted {
    border-color: $border_subtle;
    background: rgba(255, 255, 255, 0.02);
    color: $text_secondary;
}

/* Live activity pulse — the animated "system is running" cue carried over from
   the team's original header design. */
@keyframes rhPulse {
    0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 0 0 rgba(100, 255, 218, 0.45); }
    50%      { opacity: 0.6; transform: scale(0.82); box-shadow: 0 0 0 6px rgba(100, 255, 218, 0); }
}
.rh-pulse {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: $accent_teal;
    animation: rhPulse 1.7s ease-in-out infinite;
}

/* ============================================================
   6. SHARED CLINICAL SURFACES
============================================================ */
.rh-hero {
    background: $bg_card;
    border: 1px solid $border_subtle;
    border-radius: 14px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.3rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.rh-hero::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: $accent_teal;
    opacity: 0.75;
}

.rh-card {
    background: $bg_card;
    border: 1px solid $border_subtle;
    border-radius: 12px;
    padding: 1.15rem;
    margin-bottom: 0.9rem;
    transition: border-color 0.2s ease, transform 0.2s ease;
}
.rh-card:hover { border-color: rgba(100, 255, 218, 0.32); }

.rh-badge {
    display: inline-block;
    border: 1px solid $border_subtle;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 999px;
    padding: 3px 11px;
    font-size: 0.72rem;
    color: $text_secondary;
    margin: 0 4px 4px 0;
    letter-spacing: 0.04em;
    white-space: nowrap;
}

.rh-stepper {
    background: $bg_card;
    border: 1px solid $border_subtle;
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.1rem;
}
.rh-step { flex: 1; min-width: 118px; text-align: center; font-size: 0.8rem; color: $text_secondary; }

.rh-empty {
    background: $bg_card;
    border: 1px dashed $border_strong;
    border-radius: 14px;
    padding: 2.5rem 1.5rem;
    text-align: center;
    color: $text_secondary;
    margin-bottom: 1.1rem;
}

.rh-pending {
    background: $bg_card;
    border: 1px solid $border_subtle;
    border-left: 3px solid $accent_teal;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
}

.rh-kpi {
    background: $bg_card;
    border: 1px solid $border_subtle;
    border-radius: 12px;
    padding: 1rem 0.85rem;
    text-align: center;
    height: 100%;
    transition: border-color 0.2s ease;
}
.rh-kpi:hover { border-color: rgba(100, 255, 218, 0.32); }
.rh-kpi-value {
    font-size: 1.7rem; font-weight: 800; color: $accent_teal;
    letter-spacing: -0.02em; line-height: 1.1;
}
.rh-kpi-label {
    font-size: 0.68rem; color: $text_secondary; text-transform: uppercase;
    letter-spacing: 0.08em; margin-top: 0.35rem; line-height: 1.35;
}

/* ============================================================
   7. MEDICAL ASSISTANT / CHAT
============================================================ */
.rh-chat-row { display: flex; gap: 0.7rem; margin-bottom: 0.9rem; align-items: flex-start; }
.rh-chat-row.is-user { flex-direction: row-reverse; }
.rh-avatar {
    flex: 0 0 auto;
    width: 34px; height: 34px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    border: 1px solid $border_subtle; background: $bg_card;
}
.rh-avatar.is-user { border-color: rgba(100, 255, 218, 0.3); background: rgba(100, 255, 218, 0.07); }
.rh-bubble {
    flex: 1 1 auto;
    max-width: 88%;
    background: $bg_card;
    border: 1px solid $border_subtle;
    border-radius: 12px;
    padding: 0.85rem 1.05rem;
    color: $text_primary;
    font-size: 0.92rem;
    line-height: 1.65;
}
.rh-bubble.is-user {
    background: rgba(100, 255, 218, 0.07);
    border-color: rgba(100, 255, 218, 0.28);
}
.rh-bubble-head {
    font-size: 0.68rem; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.1em; color: $text_secondary; margin-bottom: 0.4rem;
}
.rh-bubble.is-user .rh-bubble-head { color: $accent_teal; }

.rh-cite {
    background: $bg_secondary;
    border: 1px solid $border_subtle;
    border-left: 3px solid $accent_teal;
    border-radius: 0 8px 8px 0;
    padding: 0.65rem 0.9rem;
    margin: 0.45rem 0;
}
.rh-cite-name { font-size: 0.79rem; font-weight: 700; color: $accent_teal; }
.rh-cite-score { font-size: 0.68rem; color: $text_secondary; }
.rh-cite-snippet { font-size: 0.79rem; color: $text_primary; line-height: 1.5; font-style: italic; margin-top: 0.3rem; }

.rh-meter {
    height: 6px; border-radius: 3px; background: rgba(255, 255, 255, 0.06);
    overflow: hidden; margin-top: 0.35rem;
}
.rh-meter > span { display: block; height: 100%; border-radius: 3px; }

/* Streamlit chat primitives (themed to match the RaphaID bubble language) */
[data-testid="stChatMessage"] {
    background: $bg_card !important;
    border: 1px solid $border_subtle !important;
    border-left: 3px solid rgba(100, 255, 218, 0.55) !important;
    border-radius: 4px 12px 12px 4px !important;
    padding: 0.95rem 1.1rem !important;
    margin-bottom: 0.8rem !important;
}

/* Clinician query bubbles — teal-tinted, right-aligned accent */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(100, 255, 218, 0.07) !important;
    border-color: rgba(100, 255, 218, 0.28) !important;
    border-left-color: $accent_teal !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-left-color: $accent_teal !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p { margin-bottom: 0.55rem; }
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p:last-child { margin-bottom: 0; }
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong { color: #FFFFFF; }
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ul,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ol { padding-left: 1.2rem; }
[data-testid="stChatInput"] {
    background: $bg_card !important;
    border: 1px solid $border_subtle !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: $text_primary !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: $text_muted !important; }
[data-testid="stChatInput"]:focus-within { border-color: $accent_teal !important; }

/* ============================================================
   8. METRICS, TABLES, DATA
============================================================ */
[data-testid="stMetric"], .metric-card {
    background: $bg_card !important;
    border: 1px solid $border_subtle !important;
    border-radius: 12px !important;
    padding: 1rem 1.1rem !important;
    text-align: center !important;
    margin-bottom: 0.85rem !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"], .metric-value {
    color: $accent_teal !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    line-height: 1.1 !important;
}
[data-testid="stMetric"] [data-testid="stMetricLabel"], .metric-label {
    color: $text_secondary !important;
    text-transform: uppercase !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.06em !important;
    margin-top: 0.35rem !important;
}

.detection-table {
    width: 100%;
    border-collapse: collapse;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid $border_subtle;
    margin-bottom: 1.1rem;
}
.detection-table th {
    background: $bg_secondary;
    color: $accent_teal;
    padding: 0.7rem 1rem;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 700;
    border-bottom: 1px solid $border_subtle;
    text-align: left;
}
.detection-table td {
    padding: 0.65rem 1rem;
    border-bottom: 1px solid $border_subtle;
    color: $text_primary;
    font-size: 0.88rem;
    background: $bg_card;
}
.detection-table tr:last-child td { border-bottom: none; }
.detection-table tr:hover td { background: $bg_hover; }

[data-testid="stDataFrame"] {
    border: 1px solid $border_subtle !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ============================================================
   9. FORM CONTROLS
============================================================ */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background-color: $bg_card !important;
    color: $text_primary !important;
    border: 1px solid $border_subtle !important;
    border-radius: 9px !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color: $text_muted !important; }
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
    border-color: $accent_teal !important;
    box-shadow: 0 0 0 2px rgba(100, 255, 218, 0.18) !important;
}

[data-baseweb="select"] > div {
    background-color: $bg_card !important;
    color: $text_primary !important;
    border-color: $border_subtle !important;
    border-radius: 9px !important;
}
[data-baseweb="popover"], [role="listbox"] {
    background-color: $bg_card !important;
    border: 1px solid $border_subtle !important;
}
[role="option"] { background-color: $bg_card !important; color: $text_primary !important; }
[role="option"]:hover { background-color: $bg_hover !important; color: $accent_teal !important; }

[data-testid="stFileUploader"] { background-color: transparent !important; }
[data-testid="stFileUploaderDropzone"] {
    background-color: $bg_card !important;
    border: 1px dashed $border_strong !important;
    border-radius: 12px !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stFileUploaderDropzone"]:hover { border-color: $accent_teal !important; }
[data-testid="stFileUploaderDropzone"] small { color: $text_muted !important; }

[data-testid="stExpander"] {
    background-color: $bg_card !important;
    border: 1px solid $border_subtle !important;
    border-radius: 12px !important;
    margin-bottom: 0.85rem !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    color: $text_primary !important;
    background-color: transparent !important;
    font-weight: 600 !important;
    padding: 0.7rem 0.9rem !important;
}
[data-testid="stExpander"] summary:hover { color: $accent_teal !important; }

[data-testid="stSlider"] [role="slider"] { background: $accent_teal !important; }
[data-testid="stCheckbox"] label span { color: $text_primary !important; }
[data-testid="stToggle"] label span { color: $text_primary !important; }

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0.35rem;
    border-bottom: 1px solid $border_subtle;
    background: transparent;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 0.5rem 0.9rem !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] p { color: $text_secondary !important; font-weight: 600 !important; }
[data-testid="stTabs"] [aria-selected="true"] p { color: $accent_teal !important; }
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background-color: $accent_teal !important; }

/* Spinner / progress */
[data-testid="stSpinner"] i { border-top-color: $accent_teal !important; }
.stProgress > div > div > div > div { background-color: $accent_teal !important; }

/* ============================================================
   10. NATIVE ALERTS
============================================================ */
[data-testid="stInfo"], [data-testid="stSuccess"],
[data-testid="stWarning"], [data-testid="stError"] {
    border-radius: 0 10px 10px 0 !important;
    color: $text_primary !important;
}
[data-testid="stInfo"] {
    background-color: rgba(100, 255, 218, 0.06) !important;
    border-left: 3px solid $accent_teal !important;
}
[data-testid="stSuccess"] {
    background-color: rgba(100, 255, 218, 0.06) !important;
    border-left: 3px solid $accent_teal !important;
}
[data-testid="stWarning"] {
    background-color: rgba(138, 148, 166, 0.09) !important;
    border-left: 3px solid $text_secondary !important;
}
[data-testid="stError"] {
    background-color: rgba(248, 113, 113, 0.08) !important;
    border-left: 3px solid $accent_red !important;
}
[data-testid="stInfo"] p, [data-testid="stSuccess"] p,
[data-testid="stWarning"] p, [data-testid="stError"] p { color: $text_primary !important; }

/* ============================================================
   11. FOOTER, DIVIDERS, SCROLLBARS
============================================================ */
.footer-credit {
    text-align: center;
    color: $text_muted;
    font-size: 0.76rem;
    padding: 1.6rem 0 1rem;
    border-top: 1px solid $border_subtle;
    margin-top: 2.2rem;
    letter-spacing: 0.03em;
    line-height: 1.7;
}

hr {
    border: none !important;
    border-top: 1px solid $border_subtle !important;
    margin: 1.3rem 0 !important;
}

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: $bg_primary; }
::-webkit-scrollbar-thumb { background: $border_strong; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: $accent_teal; }

/* ============================================================
   12. RESPONSIVE
============================================================ */
@media (max-width: 900px) {
    .block-container { padding-left: 1.2rem !important; padding-right: 1.2rem !important; }
    .rh-topbar { padding: 0.6rem 1rem; margin: -0.1rem -1.2rem 1rem -1.2rem; gap: 1.2rem; }
    .rh-topbar-item { font-size: 0.72rem; }
    .rh-hero { padding: 1.1rem; }
    .rh-bubble { max-width: 100%; }
}
""")


def apply_theme() -> None:
    """Apply the clinical dark theme via unified CSS injection."""
    colors = get_theme_colors()

    # Template.substitute only touches $tokens — CSS braces pass through untouched.
    css = _CSS_TEMPLATE.substitute(**colors)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    try:
        st.config.set_option("theme.base", "dark")
        st.config.set_option("theme.primaryColor", colors["accent_teal"])
        st.config.set_option("theme.backgroundColor", colors["bg_primary"])
        st.config.set_option("theme.secondaryBackgroundColor", colors["bg_card"])
        st.config.set_option("theme.textColor", colors["text_primary"])
    except Exception:
        pass
