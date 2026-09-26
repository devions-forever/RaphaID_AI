import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    '<div id="t1" style="display:flex;align-items:center;justify-content:center;">A</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div id="t2" style="position:fixed !important;top:0 !important;display:flex !important;'
    'align-items:center !important;">B</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div id="t3" class="x" style="position:fixed !important;top:0 !important;left:0 !important;'
    'right:0 !important;bottom:0 !important;width:100vw !important;height:100vh !important;'
    'background:#0a0f1d !important;display:flex !important;flex-direction:column !important;'
    'align-items:center !important;justify-content:center !important;z-index:2147483000 !important;'
    'margin:0 !important;padding:24px !important;box-sizing:border-box !important;'
    'overflow:hidden !important;pointer-events:all !important;">C</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div id="t4" style="position:fixed;top:0;display:flex;align-items:center;justify-content:center;'
    'width:100vw;height:100vh;background:#0a0f1d;z-index:999;margin:0;padding:24px;'
    'box-sizing:border-box;overflow:hidden;">D</div>',
    unsafe_allow_html=True,
)
