"""Temporary smoke test — boots the real Streamlit app via AppTest and walks every route."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from streamlit.testing.v1 import AppTest  # noqa: E402

APP = str(ROOT / "app" / "streamlit_app.py")
failures = []


def check(label: str, at: AppTest) -> None:
    if at.exception:
        for exc in at.exception:
            msg = getattr(exc, "value", exc)
            print(f"  FAIL {label}: {msg}", flush=True)
            failures.append(label)
        return
    print(f"  ok   {label}", flush=True)


def markdown_blob(at: AppTest) -> str:
    return "\n".join(getattr(m, "value", "") or "" for m in at.markdown)


at = AppTest.from_file(APP, default_timeout=300)
at.run()
check("dashboard boot", at)

blob = markdown_blob(at)
for needle in ("rh-topbar", "rh-hero", "rh-nav-label", "rh-kpi"):
    print(f"  {'ok  ' if needle in blob else 'MISS'} markup contains {needle}", flush=True)
    if needle not in blob:
        failures.append(f"markup:{needle}")

# --- Detection module (all four submodules) ---
for sub in ("malaria", "sickle_cell", "all", "iron_deficiency"):
    at.session_state["current_module"] = "detection"
    at.session_state["detection_submodule"] = sub
    at.run()
    check(f"detection/{sub}", at)

# --- Radiology module ---
for sub in ("mri", "ct", "xray"):
    at.session_state["current_module"] = "radiology"
    at.session_state["radiology_submodule"] = sub
    at.run()
    check(f"radiology/{sub}", at)

# --- Medical Assistant ---
at.session_state["current_module"] = "chatbot"
at.run()
check("chatbot render", at)
blob = markdown_blob(at)
for needle in ("Clinical Query Launchpad", "rh-kpi", "Medical Assistant"):
    print(f"  {'ok  ' if needle in blob else 'MISS'} chatbot contains {needle}", flush=True)
    if needle not in blob:
        failures.append(f"chatbot:{needle}")

print("\nRESULT:", "PASS" if not failures else f"FAIL -> {failures}", flush=True)
sys.exit(0 if not failures else 1)
