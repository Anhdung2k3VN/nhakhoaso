import streamlit as st
import random
import requests

from xulydata import xuly_file
from khachhang import xuly_khach_hang
from chiafile import split_and_download_excel
from gopfile_app import gop_excel
from navbar import navbar, set_background, load_quotes
from fill import render_fill_page
from data_df import handle_file_upload
from customer_df import handle_customer_file
from getdate import handle_date_file
from background import render_background_selector


# ------------------ CÀI ĐẶT GIAO DIỆN ------------------
st.set_page_config(page_title="Xử Lý Dữ Liệu", layout="wide")

# Load CSS
with open("asset/css/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------ HÌNH NỀN ------------------
default_background = "asset/img/background.jpg"
if "bg_path" not in st.session_state:
    st.session_state.bg_path = default_background
set_background(st.session_state.bg_path)
# ------------------ HÀM DÙNG CHUNG ------------------
def handle_excel_upload(title, handler_func, extra_input=None):
    st.header(title)
    uploaded_file = st.file_uploader("📤 Tải lên file Excel (.xlsx)", type=["xlsx"])
    if uploaded_file:
        st.subheader("Xử lý dữ liệu từ file đã tải lên:")
        st.write("Vui lòng đợi trong giây lát...")
        if extra_input is not None:
            handler_func(uploaded_file, extra_input)
        else:
            handler_func(uploaded_file)
    else:
        st.info("📎 Vui lòng tải lên file Excel để bắt đầu.")

# ------------------ ĐIỀU HƯỚNG ------------------
page = navbar()

# ------------------ TRANG CHỦ ------------------
if page == "home":
    quotes = load_quotes('quotes_tien_hiep.json')

    if "quote" not in st.session_state:
        st.session_state.quote = random.choice(quotes)

    if st.button("𖦹"):
        st.session_state.quote = random.choice(quotes)

    quote = st.session_state.quote
    st.markdown(f"""
        <div class='quote-box'>
            <p class='quote-text'>“{quote['quote']}”</p>
            <p class='quote-author'>— {quote['author']}</p>
        </div>
    """, unsafe_allow_html=True)

# ------------------ CÁC CHỨC NĂNG ------------------
elif page == "data_treatment":
    handle_excel_upload("Tải file & xử lý dữ liệu điều trị", xuly_file)

elif page == "customer_info":
    handle_excel_upload("Tải file & xử lý thông tin khách hàng", xuly_khach_hang)

elif page == "split_file":
    rows_per_file = st.number_input("🔢 Số dòng mỗi file (không tính dòng tiêu đề):", min_value=1, value=4999)
    handle_excel_upload("Tải file & xử lý chia nhỏ file Excel", split_and_download_excel, extra_input=rows_per_file)

elif page == "merge_excel":
    st.header("Gộp nhiều file Excel thành một")
    uploaded_files = st.file_uploader("📤 Tải lên các file Excel (.xlsx)", type=["xlsx"], accept_multiple_files=True)
    if uploaded_files:
        gop_excel(uploaded_files)
    else:
        st.info("📎 Vui lòng tải lên ít nhất một file Excel để gộp.")

elif page == "fill_data":
    handle_excel_upload("Điền dữ liệu từ dưới lên", render_fill_page)

elif page == "data_df":
    handle_excel_upload("Xử lý thông tin điều trị", handle_file_upload)

elif page == "customer_df":
    handle_excel_upload("Xử lý thông tin khách hàng", handle_customer_file)

elif page == "getdate_df":
    handle_excel_upload("Xử lý ngày tạo", handle_date_file)


elif page == "background":
    render_background_selector(total_per_page=48)
elif page == "contact":
    st.header("📞 Liên hệ")
    st.write("Facebook: [https://fb.com/doananhdung.work](https://fb.com/doananhdung.work)")


