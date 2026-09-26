"""Temporary self-test for SplashController (no browser needed)."""
import sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
from app.components.splash import SplashController, _build_splash_html

# --- Fake Streamlit surface -------------------------------------------------
renders = []
emptied = []


class FakePlaceholder:
    def markdown(self, body, unsafe_allow_html=False):
        renders.append(body)

    def empty(self):
        emptied.append(True)


st.empty = lambda: FakePlaceholder()          # type: ignore[assignment]
st.session_state = {}                          # type: ignore[assignment]

# --- Test 1: normal boot ----------------------------------------------------
splash = SplashController(min_duration=1.0)
assert splash.start("boot") is True
assert splash.active is True
assert len(renders) == 1

splash.step(62, "detection modules")
splash.step(40, "should be ignored (monotonic)")   # lower -> must not regress
splash.step(96, "reporting")
splash.complete()

assert len(emptied) == 1, "splash must be cleared exactly once"
assert st.session_state["splash_shown"] is True
assert splash.active is False

# Progress must never go backwards
assert "width:62%" in renders[1]
assert "width:62%" in renders[2], "progress regressed on a lower step()"
assert "width:96%" in renders[3]
assert "width:100%" in renders[4]

# Every render must be a single line (no Markdown code-block leak)
assert all("\n" not in r for r in renders), "multi-line HTML would leak as text"

# --- Test 2: rerun must be a no-op -----------------------------------------
before = len(renders)
splash2 = SplashController(min_duration=1.0)
assert splash2.start() is False, "second start() must skip (splash_shown already True)"
splash2.step(50, "x")
splash2.complete()
assert len(renders) == before, "rerun must not render anything"
assert len(emptied) == 1, "rerun must not clear anything"

# --- Test 3: min_duration is honoured --------------------------------------
st.session_state = {}
renders.clear(); emptied.clear()
c = SplashController(min_duration=1.2)
c.start("boot")
t0 = time.perf_counter()
c.complete()
elapsed = time.perf_counter() - t0
assert elapsed >= 1.2, f"min_duration not honoured (took {elapsed:.2f}s)"

# --- Test 4: HTML escaping --------------------------------------------------
h = _build_splash_html(50, "<script>alert(1)</script> & stuff")
assert "<script>" not in h, "status text was not escaped"
assert "&lt;script&gt;" in h

print("ALL SPLASH SELF-TESTS PASSED")
print(f"  renders={len(renders)}, emptied={len(emptied)}, min_duration honoured={elapsed:.2f}s")
print(f"  html is single-line: {all(chr(10) not in r for r in renders)}")
