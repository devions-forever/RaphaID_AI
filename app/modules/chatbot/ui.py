"""
Chatbot UI — Clinical Guideline Copilot for RaphaID AI.

Streamlit components for RAG-powered clinical decision support.
Flat clinical dark theme, zero emojis, full citation grounding display.

Layout
------
1. Copilot header          — identity, knowledge-base telemetry, guardrail posture
2. Query launchpad         — one-tap clinical topic chips (compact empty state)
3. Consultation transcript — labelled clinician query / clinical note bubbles,
                             confidence meter and grounded citation panel
4. Consultation controls   — sidebar clear / reload / export
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List

import streamlit as st

from app.components.icons import get_icon
from app.components.htmlkit import render_html
from app.components.status import callout

from .rag_pipeline import get_rag_pipeline
from .langgraph_orchestrator import get_orchestrator

KNOWLEDGE_DIR = "data/medical_knowledge"

# One-tap launchpad topics: (short button label, full clinical query sent to the copilot).
QUICK_CHIPS = [
    ("Severe malaria treatment",
     "WHO guidelines for severe P. falciparum malaria with parenteral artesunate protocol"),
    ("Sickle cell crisis",
     "Clinical management protocol for acute sickle cell vaso-occlusive crisis"),
    ("Iron deficiency workup",
     "Iron deficiency anaemia: laboratory workup, interpretation and treatment thresholds"),
    ("ALL induction complications",
     "Complications during ALL induction chemotherapy and their clinical management"),
    ("TB vs pneumonia on CXR",
     "Chest X-ray differentiation between bacterial lobar pneumonia and pulmonary tuberculosis"),
    ("Paediatric antimalarial dosing",
     "Weight-based artemether-lumefantrine dosage schedule for pediatric uncomplicated malaria"),
]

# Guardrail posture — rendered as one compact chip row, not four bulky cards.
GUARDRAIL_CHIPS = [
    ("file_medical", "WHO &middot; NCDC grounded"),
    ("magnifying_glass_chart", "Citations verified"),
    ("warning", "Uncertainty flagged"),
    ("shield", "Fully offline"),
]


# ---------------------------------------------------------------------------
# Small renderers
# ---------------------------------------------------------------------------
def _confidence_meta(confidence: float) -> Dict[str, str]:
    """Map a grounding score to a label, colour and clinical action."""
    if confidence >= 0.8:
        return {
            "label": "Well-Grounded · Official Guidelines",
            "short": "High grounding",
            "color": "#64ffda",
            "action": "Safe to use as decision support",
        }
    if confidence >= 0.5:
        return {
            "label": "Partial Grounding · Verify with Specialist",
            "short": "Partial grounding",
            "color": "#ffd700",
            "action": "Cross-check against local protocol",
        }
    return {
        "label": "Clinical Review Required · Unverified",
        "short": "Low grounding",
        "color": "#f87171",
        "action": "Escalate to a qualified specialist",
    }


def _confidence_badge(confidence: float) -> str:
    """Render a clinical grounding score badge (HTML string)."""
    meta = _confidence_meta(confidence)
    return (
        f'<span style="display:inline-flex; align-items:center; gap:6px; padding:3px 10px; '
        f'border:1px solid {meta["color"]}55; background:{meta["color"]}14; color:{meta["color"]}; '
        f'border-radius:999px; font-size:0.72rem; font-weight:700; letter-spacing:0.04em; '
        f'text-transform:uppercase;">'
        f'<span style="width:6px; height:6px; border-radius:50%; background:{meta["color"]};"></span>'
        f'{meta["label"]} ({confidence:.0%})</span>'
    )


def _confidence_meter(confidence: float) -> str:
    """Render the grounding score as a labelled meter bar."""
    meta = _confidence_meta(confidence)
    pct = max(0.0, min(confidence, 1.0)) * 100
    return (
        f'<div style="margin-top:0.7rem; padding-top:0.65rem; border-top:1px solid #1f2d44;">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; '
        f'font-size:0.7rem; text-transform:uppercase; letter-spacing:0.08em; color:#8a94a6;">'
        f'<span>Grounding confidence</span>'
        f'<span style="color:{meta["color"]}; font-weight:800;">{confidence:.0%}</span></div>'
        f'<div class="rh-meter"><span style="width:{pct:.0f}%; background:{meta["color"]};"></span></div>'
        f'<div style="font-size:0.74rem; color:#8a94a6; margin-top:0.4rem;">{meta["action"]}</div>'
        f'</div>'
    )


def _render_copilot_header(chunks_loaded: int, docs_indexed: int) -> None:
    """Render clinical copilot hero and live knowledge base telemetry."""
    assistant_icon = get_icon("chatbot", "#64ffda", "28", "28")
    kb_ready = chunks_loaded > 0
    kb_color = "#64ffda" if kb_ready else "#f87171"
    kb_text = (
        f"{docs_indexed} docs · {chunks_loaded} chunks indexed"
        if kb_ready
        else "Guidelines not indexed"
    )

    render_html(
        f"""
        <div class="rh-hero" style="padding:1.15rem 1.4rem; margin-bottom:1.15rem; text-align:left;">
            <div style="display:flex; align-items:center; justify-content:space-between;
                        flex-wrap:wrap; gap:0.8rem;">
                <div style="display:flex; align-items:center; gap:0.85rem;">
                    <div style="display:flex; align-items:center; justify-content:center;
                                width:46px; height:46px; border-radius:12px;
                                background:rgba(100,255,218,0.08);
                                border:1px solid rgba(100,255,218,0.28);">
                        {assistant_icon}
                    </div>
                    <div>
                        <div style="font-size:0.70rem; color:#8a94a6; text-transform:uppercase;
                                    letter-spacing:0.1em; font-weight:700;">
                            Clinical AI Copilot &middot; Decision Support
                        </div>
                        <div style="font-size:1.45rem; font-weight:800; color:#FFFFFF;
                                    letter-spacing:-0.01em; line-height:1.2;">
                            Medical Assistant
                        </div>
                    </div>
                </div>
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                    <span class="rh-badge" style="color:{kb_color};
                          border-color:{kb_color}55; background:{kb_color}14; font-size:0.72rem;">
                        {kb_text}
                    </span>
                    <span class="rh-badge" style="color:#64ffda;
                          border-color:rgba(100,255,218,0.3);
                          background:rgba(100,255,218,0.06); font-size:0.72rem;">
                        Local RAG &middot; Air-Gapped
                    </span>
                </div>
            </div>
            <div style="margin-top:0.7rem; padding-top:0.7rem; border-top:1px solid #1f2d44;
                        display:flex; align-items:center; justify-content:space-between;
                        flex-wrap:wrap; gap:0.5rem;">
                <div style="font-size:0.78rem; color:#8a94a6;">
                    Answers are grounded in WHO guidelines, NCDC clinical protocols and
                    CheXpert literature with strict citation verification.
                </div>
                <div style="font-size:0.70rem; color:#5c6779;">
                    Research &amp; Decision Support Only
                </div>
            </div>
        </div>
        """,
    )


def _render_capability_strip() -> None:
    """Compact one-line guardrail posture (replaces the old four-card grid)."""
    chips = "".join(
        '<span style="display:inline-flex; align-items:center; gap:6px; font-size:0.72rem; '
        'color:#8a94a6; border:1px solid #1f2d44; background:rgba(255,255,255,0.02); '
        'border-radius:999px; padding:4px 11px; margin:0 6px 6px 0; white-space:nowrap;">'
        f"{get_icon(icon, '#64ffda', '14', '14')}{label}</span>"
        for icon, label in GUARDRAIL_CHIPS
    )
    render_html(f'<div style="text-align:center; margin:-0.25rem 0 0.4rem 0;">{chips}</div>')


def _render_launchpad() -> None:
    """Compact clinical query launchpad — one-tap topics, no bulky prompt cards."""
    render_html(
        '<div style="text-align:center; margin:1.5rem 0 0.9rem 0;">'
        '<div style="font-size:1.05rem; font-weight:700; color:#FFFFFF;">'
        "Start with a common clinical query</div>"
        '<div style="font-size:0.8rem; color:#8a94a6; margin-top:0.3rem;">'
        "Tap a topic to consult the guideline copilot, or type your own question below.</div>"
        "</div>"
    )

    chip_cols = st.columns(3)
    for i, (label, query) in enumerate(QUICK_CHIPS):
        with chip_cols[i % 3]:
            if st.button(label, key=f"chip_{i}", use_container_width=True, help=query):
                st.session_state["pending_prompt"] = query
                st.rerun()


def _render_citations(citations: List[Dict]) -> None:
    """Render structured medical literature citations as grounded source cards."""
    if not citations:
        return

    blocks = []
    for i, cit in enumerate(citations):
        source_name = cit.get("metadata", {}).get("source", f"Guideline Doc {i + 1}")
        clean_name = (
            Path(source_name).name.replace(".md", "").replace(".txt", "").replace("_", " ").title()
        )
        distance = cit.get("distance", 0.0)
        relevance = 1.0 - min(float(distance or 0.0), 1.0)
        snippet = (cit.get("content", "") or "").strip()[:280]
        blocks.append(
            f"""
            <div class="rh-cite">
                <div style="display:flex; justify-content:space-between; align-items:center; gap:0.6rem;">
                    <span class="rh-cite-name">[{i + 1}] {clean_name}</span>
                    <span class="rh-cite-score">Relevance {relevance:.1%}</span>
                </div>
                <div class="rh-cite-snippet">&ldquo;{snippet}&hellip;&rdquo;</div>
            </div>
            """
        )

    with st.expander(f"Grounded Guideline Sources · {len(citations)} citations", expanded=False):
        render_html("".join(blocks))


def _render_assistant_note(msg: Dict) -> None:
    """Render one clinical decision-support note inside an assistant bubble."""
    with st.chat_message("assistant"):
        intent = (msg.get("intent") or "general").replace("_", " ").title()
        render_html(
            f"""
            <div style="display:flex; align-items:center; justify-content:space-between;
                        gap:0.6rem; flex-wrap:wrap; margin-bottom:0.55rem;">
                <span style="display:inline-flex; align-items:center; gap:0.45rem;
                             font-size:0.68rem; font-weight:800; text-transform:uppercase;
                             letter-spacing:0.1em; color:#64ffda;">
                    {get_icon('chatbot', '#64ffda', '15', '15')}
                    Clinical Decision Support Note
                </span>
                <span class="rh-badge" style="margin:0; font-size:0.66rem;">
                    Intent: {intent}
                </span>
            </div>
            """,
        )

        st.markdown(msg["content"])

        if msg.get("confidence") is not None:
            render_html(_confidence_meter(msg["confidence"]))

        if msg.get("citations"):
            _render_citations(msg["citations"])


def _render_user_query(msg: Dict) -> None:
    """Render one clinician query inside a user bubble."""
    with st.chat_message("user"):
        render_html(
            f"""
            <div style="display:inline-flex; align-items:center; gap:0.45rem;
                        font-size:0.68rem; font-weight:800; text-transform:uppercase;
                        letter-spacing:0.1em; color:#64ffda; margin-bottom:0.4rem;">
                {get_icon('user_doctor', '#64ffda', '15', '15')}
                Clinician Query
            </div>
            """,
        )
        st.markdown(msg["content"])


def _build_transcript() -> str:
    """Build a plain-markdown transcript of the consultation for export."""
    lines = [
        "# RaphaID AI — Clinical Consultation Transcript",
        f"_Generated {datetime.now().strftime('%d %B %Y, %H:%M')} · Offline decision support_",
        "",
        "> Research and decision support only. Not a substitute for clinical judgement.",
        "",
    ]
    for msg in st.session_state.get("chat_history", []):
        if msg["role"] == "user":
            lines += ["## Clinician Query", msg["content"], ""]
        else:
            intent = (msg.get("intent") or "general").replace("_", " ").title()
            conf = msg.get("confidence")
            lines += [
                "## Clinical Decision Support Note",
                f"**Intent:** {intent}" + (f"  ·  **Grounding:** {conf:.0%}" if conf is not None else ""),
                "",
                msg["content"],
                "",
            ]
            for i, cit in enumerate(msg.get("citations", []) or []):
                src = Path(cit.get("metadata", {}).get("source", "unknown")).name
                lines.append(f"- [{i + 1}] {src}")
            lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def render_chatbot_ui() -> None:
    """Render the medical assistant clinical chatbot UI."""
    try:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # NOTE: must be an explicit False check — the previous `not in` test meant
        # "Reload KB" set the flag to False and the pipeline never re-indexed.
        if not st.session_state.get("rag_initialized", False):
            with st.spinner("Indexing local medical knowledge base..."):
                rag = get_rag_pipeline()
                chunks_loaded = rag.load_medical_knowledge(KNOWLEDGE_DIR)
                st.session_state["kb_chunks"] = chunks_loaded
                st.session_state["rag_initialized"] = True

        chunks_loaded = st.session_state.get("kb_chunks", 0)
        kb_path = Path(KNOWLEDGE_DIR)
        docs_indexed = (
            len(list(kb_path.glob("*.md"))) + len(list(kb_path.glob("*.txt")))
            if kb_path.exists()
            else 0
        )

        orchestrator = get_orchestrator()
    except ImportError as exc:
        st.error(
            "The medical assistant requires optional dependencies that are not "
            "installed in this environment."
        )
        st.code("pip install -r requirements.txt")
        st.caption(str(exc))
        return

    _render_copilot_header(chunks_loaded, docs_indexed)
    _render_capability_strip()

    if not st.session_state.chat_history:
        _render_launchpad()
    else:
        render_html(
            '<div style="font-size:0.70rem; font-weight:800; color:#5c6779; '
            'text-transform:uppercase; letter-spacing:0.12em; margin:1.3rem 0 0.6rem 0;">'
            "Consultation Transcript</div>",
        )

    def _process(prompt: str) -> None:
        """Run one query through the orchestrator and record session history."""
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        _render_user_query({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Searching official medical guidelines and verifying grounding..."):
                result = orchestrator.process_query(prompt)

            note = {
                "role": "assistant",
                "content": result["response"],
                "citations": result.get("citations", []),
                "confidence": result.get("confidence", 0.0),
                "intent": result.get("intent", "general"),
                "needs_escalation": result.get("needs_escalation", False),
            }
            _render_assistant_note(note)

        st.session_state.chat_history.append(note)

    # Replay prior turns
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            _render_user_query(msg)
        else:
            _render_assistant_note(msg)

    # Input handling
    pending = st.session_state.pop("pending_prompt", None)
    prompt = pending or st.chat_input(
        "Ask a clinical question (e.g. 'WHO severe malaria treatment protocol...')"
    )
    if prompt:
        _process(prompt)

    # Sidebar consultation controls
    with st.sidebar:
        render_html('<div class="rh-nav-label">Consultation Controls</div>')

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Clear Chat", key="chat_clear", use_container_width=True,
                         help="Clear consultation history"):
                st.session_state.chat_history = []
                st.rerun()
        with c2:
            if st.button("Reload KB", key="chat_reload", use_container_width=True,
                         help="Re-index the local guideline documents"):
                st.session_state["rag_initialized"] = False
                st.rerun()

        if st.session_state.chat_history:
            st.download_button(
                "Export Transcript (.md)",
                data=_build_transcript(),
                file_name=f"raphaid_consultation_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

        render_html('<div class="rh-nav-label">Assistant Guardrails</div>')
        render_html(
            """<div style="font-size:0.78rem; color:#8a94a6; line-height:1.65;
                       background:#111a2e; border:1px solid #1f2d44; border-radius:10px;
                       padding:0.7rem 0.85rem;">
                <div>&bull; Grounded strictly in local guideline documents</div>
                <div>&bull; Hallucination filter &amp; term verification</div>
                <div>&bull; Low-confidence triggers specialist escalation</div>
                <div>&bull; Completely private &amp; offline (zero telemetry sent)</div>
            </div>""",
        )
        render_html('<div style="height:1.5rem;"></div>')
