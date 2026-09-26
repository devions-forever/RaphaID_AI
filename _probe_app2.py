import streamlit as st
st.set_page_config(layout="wide")
with st.sidebar:
    st.markdown("### Plain sidebar")
    st.button("Nav one")
    st.button("Nav two")
st.markdown("## Plain main")
