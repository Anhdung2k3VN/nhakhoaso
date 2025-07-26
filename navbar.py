# navbar.py
import streamlit as st

def navbar():
    st.sidebar.title("🔸 Menu điều hướng")
    page = st.sidebar.radio(
        "Chọn trang",
        ("🏠 Trang chủ", "📁 Dữ liệu điều trị", "📁 Thông tin khách hàng", "📄 Hướng dẫn", "📞 Liên hệ"),
        index=0
    )
    return page
