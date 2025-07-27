import streamlit as st
import requests
from xulydata import xuly_file
from khachhang import xuly_khach_hang
from chiafile import split_and_download_excel
from navbar import navbar
from navbar import set_background_from_local
from navbar import read_quotes_from_file

import random


st.set_page_config(page_title="Xử Lý Dữ Liệu", layout="wide")
page = navbar()
set_background_from_local("background.jpg")




# In thử 1 quote ngẫu nhiên


if page == "home":

    st.header("Chào mừng đến với ứng dụng xử lý dữ liệu!")
  
  
    st.markdown("💡 **Quote hôm nay:**")
    quotes = read_quotes_from_file("quotes_tien_hiep.txt")
    st.info(f"💬 {random.choice(quotes)}")

elif page == "data_treatment":

    st.header("Tải file & xử lý dữ liệu điều trị")
    uploaded_file = st.file_uploader("📤 Tải lên file Excel (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        st.subheader("Xử lý dữ liệu từ file đã tải lên:")
        st.write("Vui lòng đợi trong giây lát...")
        xuly_file(uploaded_file)
    else:
        st.info("📎 Vui lòng tải lên file Excel để bắt đầu.")


elif page == "customer_info":
  
    st.header("Tải file & xử lý thông tin khách hàng")
    uploaded_file = st.file_uploader("📤 Tải lên file Excel (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        st.subheader("Xử lý dữ liệu từ file đã tải lên:")
        st.write("Vui lòng đợi trong giây lát...")
        xuly_khach_hang(uploaded_file)
    else:
        st.info("📎 Vui lòng tải lên file Excel để bắt đầu.")

elif page == "split_file":
   
    st.header("Tải file & xử lý chia nhỏ file Excel")
    uploaded_file = st.file_uploader("📤 Tải lên file Excel (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
       split_and_download_excel(uploaded_file)
       st.write("Quá trình chia nhỏ file đã hoàn tất!")
    else:
        st.info("📎 Vui lòng tải lên file Excel để bắt đầu.")


elif page == "guide":
 
    st.header("Hướng dẫn sử dụng")
    st.write("Để sử dụng ứng dụng này, bạn vui lòng làm theo các bước sau:")
    st.write("1. Chọn các tùy chọn xử lý dữ liệu.")
    st.write("2. Tải lên file Excel cần xử lý.")
    st.write("3. Chờ trong giây lát.")

elif page == "contact":

    st.write("Facebook: https://fb.com/doananhdung.work")


st.markdown("""
    <style>

    .stSidebar {
        background-color: rgba(0, 0, 0, 0.5);
    }
    .stHeader {
        background-color: rgba(255, 255, 255, 0.8);
    }
    .stMarkdown {

        color: rgba(255, 255, 255, 0.8);
        font-size: 16px;
    }

   
  
    </style>
""", unsafe_allow_html=True)

