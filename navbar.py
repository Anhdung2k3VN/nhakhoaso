# navbar.py
import streamlit as st
import json

def navbar():
    st.sidebar.title("🔸 Menu điều hướng")
    
    # Cấu trúc trang chính
    page = {
        "🏠 Trang chủ": "home",
        "🦷 Nha khoa số": {
            "📋 Thông tin khách hàng": "customer_info",
            "📁 Dữ liệu điều trị": "data_treatment"
        },
         "🦷 Dental flow": {
             "📋 Fill data": "fill_data",
            "📋 Thông tin khách hàng": "customer_df",
            "📁 Dữ liệu điều trị": "data_df",
            "📅 Ngày tạo": "getdate_df"
        },
        "📂 Chia file": "split_file",
        "📂 Gộp file": "merge_excel",
        "📄 Hướng dẫn": "guide",
        "📞 Liên hệ": "contact"
    }

    main_choices = list(page.keys())
    selected_main = st.sidebar.radio("Chọn trang:", main_choices)

    # Nếu chọn mục có submenu (Nha khoa số)
    if isinstance(page[selected_main], dict):
        submenu_keys = list(page[selected_main].keys())
        selected_sub = st.sidebar.radio(f"→ {selected_main}:", submenu_keys)
        return page[selected_main][selected_sub]
    else:
        return page[selected_main]
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

def load_quotes(filepath='quotes_tien_hiep.json'):
    """Tải danh sách quotes từ file JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Lỗi: Không tìm thấy file '{filepath}'. Hãy chắc chắn file tồn tại trong cùng thư mục.")
        return []
    except json.JSONDecodeError:
        st.error(f"Lỗi: File '{filepath}' có định dạng JSON không hợp lệ.")
        return []