"""
HTML injection helper — RaphaID AI.

Why this exists
---------------
Streamlit runs every ``st.markdown(..., unsafe_allow_html=True)`` payload through
the Markdown parser first. Markdown treats **any line indented by four or more
spaces as a code block**, so a nicely indented HTML template like::

    st.markdown(f\"\"\"
        <div class="rh-card">
            <span>Hello</span>
        </div>
    \"\"\", unsafe_allow_html=True)

renders as literal escaped text on the page instead of a styled card. That is
exactly what broke the sidebar brand block, the telemetry card and the footer
panels.

``render_html`` collapses the markup to a single line first, so the leading
indentation disappears and the Markdown parser always sees an HTML block. This
is the same technique ``app/components/splash.py`` already used.
"""

import re

import streamlit as st

_WHITESPACE = re.compile(r"\s+")


def html_str(markup: str) -> str:
    """Collapse an indented HTML template onto one line."""
    return _WHITESPACE.sub(" ", markup).strip()


def render_html(markup: str) -> None:
    """Render trusted HTML safely, immune to Markdown's 4-space code-block rule."""
    st.markdown(html_str(markup), unsafe_allow_html=True)
