import streamlit as st
from xulydata import xuly_file
from navbar import navbar

st.set_page_config(page_title="Xử Lý Dữ Liệu", layout="wide")
page = navbar()

if page == "🏠 Trang chủ":
    st.header("Chào mừng đến với ứng dụng xử lý dữ liệu!")
    st.write("Ứng dụng hỗ trợ xử lý dữ liệu khách hàng.")

elif page == "📁 Xử lý dữ liệu":
    st.header("Tải file & xử lý")
    uploaded_file = st.file_uploader("📤 Tải lên file Excel (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        st.subheader("Xử lý dữ liệu từ file đã tải lên:")
        st.write("Vui lòng đợi trong giây lát...")
        xuly_file(uploaded_file)
    else:
        st.info("📎 Vui lòng tải lên file Excel để bắt đầu.")

elif page == "📄 Hướng dẫn":
    st.header("Hướng dẫn sử dụng")
    st.write("Để sử dụng ứng dụng này, bạn vui lòng làm theo các bước sau:")
    st.write("1. Tải lên file Excel cần xử lý.")
    st.write("2. Chọn các tùy chọn xử lý dữ liệu.")
    st.write("3. Nhấn nút 'Xử lý' để bắt đầu.")

elif page == "📞 Liên hệ":
    st.header("Liên hệ")
    st.write("Facebook: [fb.com/yourpage](https://fb.com/yourpage)")
