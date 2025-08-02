import streamlit as st
import json
import base64
from pathlib import Path

# ---------------- NAVIGATION ----------------
def navbar():
    st.sidebar.title("🔸 Menu điều hướng")
    
    page = {
        "🏡 Trang chủ": "home",
        "🦷 Nha khoa số": {
            "👤 Thông tin khách hàng": "customer_info",
            "📊 Dữ liệu điều trị": "data_treatment"
        },
        "💻 Dental Flow": {
            "📝 Fill Data": "fill_data",
            "👥 Thông tin khách hàng": "customer_df",
            "📈 Dữ liệu điều trị": "data_df",
            "📆 Ngày tạo": "getdate_df"
        },
        "🪓 Chia file": "split_file",
        "🧩 Gộp file": "merge_excel",
        "🎨 Hình nền": "background",
        "☎️ Liên hệ": "contact"
    }

    main_choices = list(page.keys())
    selected_main = st.sidebar.radio("Chọn trang:", main_choices)

    if isinstance(page[selected_main], dict):
        submenu_keys = list(page[selected_main].keys())
        selected_sub = st.sidebar.radio(f"→ {selected_main}:", submenu_keys)
        return page[selected_main][selected_sub]
    else:
        return page[selected_main]

# ---------------- BACKGROUND ----------------

@st.cache_resource
def set_background(path):
    import base64
    if path.startswith("http"):
        bg_url = path
    else:
        with open(path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            bg_url = f"data:image/jpeg;base64,{encoded}"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{bg_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ---------------- QUOTES ----------------
def load_quotes(filepath='quotes_tien_hiep.json'):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Lỗi: Không tìm thấy file '{filepath}'.")
        return []
    except json.JSONDecodeError:
        st.error(f"Lỗi: File '{filepath}' không đúng định dạng JSON.")
        return []
