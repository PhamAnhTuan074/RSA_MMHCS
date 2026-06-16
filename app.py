"""Entry point for the RSA Learning Lab Streamlit application."""

import streamlit as st

from ui import page_cipher, page_simulation, page_theory
from ui.shared import (
    apply_styles,
    init_session_state,
    render_brand,
    render_footer,
)


st.set_page_config(
    page_title="RSA Learning Lab",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()
init_session_state()
render_brand()

st.sidebar.markdown(
    '<div class="sidebar-group">Ba phần học tập</div>',
    unsafe_allow_html=True,
)

PAGES = {
    "01 · Lý thuyết RSA": page_theory.render,
    "02 · Mô phỏng từng bước": page_simulation.render,
    "03 · Mã Hóa, Giải Mã": page_cipher.render,
}

selected_page = st.sidebar.radio(
    "Điều hướng",
    list(PAGES),
    label_visibility="collapsed",
    key="main_page",
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div class="sidebar-group">Lộ trình mô phỏng</div>',
    unsafe_allow_html=True,
)
st.sidebar.caption(
    "Chọn p,q → tính n → tính φ(n) → kiểm tra e → tìm d → "
    "xuất khóa → mã hóa → giải mã → đối chiếu hoặc thực hành trực tiếp."
)
st.sidebar.warning(
    "Các số nhỏ trong website chỉ phục vụ học tập, không dùng để bảo mật dữ liệu thật."
)

PAGES[selected_page]()
render_footer()
