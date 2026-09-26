"""
Chatbot UI — Medical Assistant Interface
Streamlit components for the RAG-powered chatbot.

P5 upgrade: icon header, knowledge-base status card, designed empty state,
flat confidence badges, no emoji (inline SVG only). RAG/orchestrator logic
is unchanged from the original implementation.
"""

import streamlit as st
from typing import List, Dict

from app.components.icons import get_icon
from app.components.status import callout

from .rag_pipeline import get_rag_pipeline
from .langgraph_orchestrator import get_orchestrator

EXAMPLE_QUERIES = [
    "WHO malaria treatment guidelines for severe cases",
    "Sickle cell crisis management guidelines",
    "Pneumonia vs TB differential on chest X-ray",
]


def _confidence_badge(confidence: float) -> str:
    """Flat confidence badge (well-grounded / partial / escalate)."""
    if confidence >= 0.8:
        label, color = "Well-grounded", "#4ade80"
    elif confidence >= 0.5:
        label, color = "Partial grounding", "#ffd700"
    else:
        label, color = "Escalate to specialist", "#e94560"
    return (
        f'<span style="display:inline-block; padding:0.2rem 0.7rem;'
        f' border:1px solid {color}; color:{color}; border-radius:6px;'
        f' font-size:0.75rem; font-weight:600; letter-spacing:0.05em;'
        f' text-transform:uppercase;">{label} · {confidence:.0%}</span>'
    )


def _render_knowledge_status(chunks_loaded: int) -> None:
    """Show whether the RAG knowledge base has guideline documents loaded."""
    if chunks_loaded > 0:
        body = (
            f'<div style="display:flex; align-items:center; gap:0.6rem;">'
            f'{get_icon("check", "#4ade80", "18", "18")}'
            f'<strong style="color:#FFFFFF;">Knowledge base ready</strong>'
            f'<span style="color:#8892b0; font-size:0.85rem;">'
            f'{chunks_loaded} guideline chunks loaded</span></div>'
        )
    else:
        body = (
            f'<div style="display:flex; align-items:center; gap:0.6rem;">'
            f'{get_icon("warning", "#ffd700", "18", "18")}'
            f'<strong style="color:#FFFFFF;">No guideline documents</strong>'
            f'<span style="color:#8892b0; font-size:0.85rem;">'
            f'Add .md or .txt files to data/medical_knowledge/ to enable '
            f'grounded answers</span></div>'
        )
    # info_card() takes (title, content) and renders itself — it does NOT return
    # HTML, so it must never be wrapped in st.markdown(...). This card is built
    # directly so the loaded/pending accent border shows correctly.
    accent = "#64ffda" if chunks_loaded > 0 else "#5c6779"
    st.markdown(
        f'<div class="rh-card" style="border-left:3px solid {accent};">'
        f"<div>{body}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def _render_empty_state() -> None:
    """Designed first-run state instead of a blank chat pane."""
    st.markdown(
        f'<div class="rh-empty" style="text-align:center; padding:2.5rem 1.5rem;">'
        f'<div style="margin-bottom:0.8rem;">'
        f'{get_icon("chatbot", "#64ffda", "40", "40")}</div>'
        f'<div style="color:#FFFFFF; font-weight:700; font-size:1.05rem;">'
        f'How can I assist you today?</div>'
        f'<div style="color:#8892b0; font-size:0.85rem; margin-top:0.4rem;">'
        f'Ask about treatment guidelines, diagnostic criteria, or differentials. '
        f'Responses cite retrieved sources.</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="color:#8892b0; font-size:0.78rem; text-transform:uppercase;'
        ' letter-spacing:0.08em; margin:1.2rem 0 0.5rem;">Example prompts</div>',
        unsafe_allow_html=True,
    )
    for ex in EXAMPLE_QUERIES:
        if st.button(ex, key=f"ex_{ex[:24]}", use_container_width=True):
            # Populate the pending prompt; processed exactly like chat_input.
            st.session_state["pending_prompt"] = ex
            st.rerun()


def render_chatbot_ui() -> None:
    """Render the medical assistant chatbot UI."""
    try:
        # Icon header — no emoji, consistent with the rest of the app.
        st.markdown(
            f'<div class="rh-hero" style="display:flex; align-items:center;'
            f' gap:0.75rem; padding:1rem 1.4rem; margin-bottom:1rem;">'
            f'{get_icon("chatbot", "#64ffda", "26", "26")}'
            f'<span style="color:#FFFFFF; font-size:1.3rem; font-weight:800;">'
            f'Medical Assistant</span>'
            f'<span style="color:#8892b0; font-size:0.8rem; margin-left:auto;">'
            f'RAG + LangGraph · WHO/NCDC guidelines · citations included</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="color:#8892b0; font-size:0.82rem; margin-bottom:1rem;">'
            'Decision support only — not for standalone diagnosis.</div>',
            unsafe_allow_html=True,
        )

        # Initialize session state for chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if "rag_initialized" not in st.session_state:
            with st.spinner("Loading medical knowledge base..."):
                rag = get_rag_pipeline()
                chunks_loaded = rag.load_medical_knowledge()
                st.session_state.rag_initialized = True
                st.session_state["kb_chunks"] = chunks_loaded

        chunks_loaded = st.session_state.get("kb_chunks", 0)
        _render_knowledge_status(chunks_loaded)

        # Initialize orchestrator
        orchestrator = get_orchestrator()
    except ImportError as exc:
        st.error(
            "The medical chatbot requires optional dependencies that are not "
            "installed in this environment."
        )
        st.code("pip install -r requirements.txt")
        st.caption(str(exc))
        return

    def _process(prompt: str) -> None:
        """Run one query through the orchestrator (single shared path)."""
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Retrieving guidelines and generating response..."):
                result = orchestrator.process_query(prompt)
            st.markdown(result["response"])
            st.markdown(_confidence_badge(result["confidence"]),
                        unsafe_allow_html=True)
            if result["citations"]:
                with st.expander("Sources"):
                    for cit in result["citations"]:
                        st.markdown(
                            f'**{cit["metadata"].get("source", "unknown")}** '
                            f'(distance: {cit["distance"]:.3f})'
                        )
                        st.caption(cit["content"][:300] + "...")
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": result["response"],
                "citations": result["citations"],
                "confidence": result["confidence"],
            })

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("confidence") is not None:
                st.markdown(_confidence_badge(msg["confidence"]),
                            unsafe_allow_html=True)
            if msg.get("citations"):
                with st.expander("Sources"):
                    for cit in msg["citations"]:
                        st.markdown(
                            f'**{cit["metadata"].get("source", "unknown")}** '
                            f'(distance: {cit["distance"]:.3f})'
                        )
                        st.caption(cit["content"][:300] + "...")

    # Empty state (only before the first exchange)
    if not st.session_state.chat_history:
        _render_empty_state()

    # Resolve prompt: example button (pending_prompt) or typed chat input.
    pending = st.session_state.pop("pending_prompt", None)
    prompt = pending or st.chat_input(
        "Ask a medical question (e.g. 'WHO malaria treatment guidelines...')"
    )
    if prompt:
        _process(prompt)

    # Sidebar controls — text labels, no emoji.
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Chatbot Controls")

        if st.button("Clear chat history", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

        if st.button("Reload knowledge base", use_container_width=True):
            st.session_state.rag_initialized = False
            st.rerun()

        st.markdown("---")
        st.markdown("### About this assistant")
        st.markdown(
            '<div style="color:#8892b0; font-size:0.8rem; line-height:1.6;">'
            'Answers are retrieved from local guideline documents, generated by '
            'a local LLM, then checked for grounding. Low-confidence responses '
            'are escalated for specialist review.</div>',
            unsafe_allow_html=True,
        )
