# navbar.py
import streamlit as st

def navbar():
    st.sidebar.title("🔸 Menu điều hướng")

    page = {
        "🏠 Trang chủ": "home",
        "📁 Dữ liệu điều trị": "data_treatment",
        "📁 Thông tin khách hàng": "customer_info",
        "📁 Chia nhỏ file": "split_file",
        "📄 Hướng dẫn": "guide",
        "📞 Liên hệ": "contact"
    }
    selected_page = st.sidebar.radio("Chọn trang:", list(page.keys()))
    return page[selected_page]

import base64

def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
def set_background_from_local(image_path):
    base64_img = get_base64_of_image(image_path)
    css_code = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

def read_quotes_from_file(file_path="quotes_tien_hiep.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            quotes = [line.strip() for line in f if line.strip()]
        return quotes
    except Exception as e:
        print(f"Lỗi khi đọc file quote: {e}")
        return []
