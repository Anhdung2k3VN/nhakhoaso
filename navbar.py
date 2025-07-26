# navbar.py
import streamlit as st

def navbar():
    st.sidebar.title("🔸 Menu điều hướng")
    page = st.sidebar.radio(
        "Chọn trang",
        ("🏠 Trang chủ", "📁 Dữ liệu điều trị", "📁 Thông tin khách hàng","📁 Chia nhỏ file", "📄 Hướng dẫn", "📞 Liên hệ"),
        index=0
    )
    return page
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

    # .block-container {{
    #     background-color: rgba(255, 255, 255, 0.8);
    #     padding: 2rem;
    #     border-radius: 10px;
    # }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

    