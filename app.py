import streamlit as st




st.markdown("""
    <style>

    .stSidebar {
        background-color: rgba(0, 0, 0, 0.5);
    }
    .stHeader {
        background-color: rgba(255, 255, 255, 0.8);
        color: black;
        font-size: 24px;
        font-weight: bold;
    }
    .stMarkdown {
      
        color: white !important;
        font-size: 16px;
    }
    header[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0.0); 
    box-shadow: none; 
    color: white !important;
    }
    .stApp {
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
    }

   div[role="alert"] {
    background-color: rgba(255, 255, 255, 0.8) !important;
    color: #333 !important;
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 16px;
    font-style: italic;
    }
 
    </style>
""", unsafe_allow_html=True)


import requests
from xulydata import xuly_file
from khachhang import xuly_khach_hang
from chiafile import split_and_download_excel
from navbar import navbar
from navbar import set_background_from_local
from navbar import load_quotes
import json

import random


st.set_page_config(page_title="Xử Lý Dữ Liệu", layout="wide")
page = navbar()
set_background_from_local("background.jpg")




# In thử 1 quote ngẫu nhiên


if page == "home":
   
    
  
  
   
    quotes = load_quotes('quotes_tien_hiep.json')
    random_quote = random.choice(quotes)
    # Hiển thị quote và tác giả với CSS đẹp mắt
    st.markdown(f"""
    <div class='quote-box'>
        <p class='quote-text'>“{random_quote['quote']}”</p>
        <p class='quote-author'>— {random_quote['author']}</p>
    </div>
""", unsafe_allow_html=True)

# CSS tùy biến
    st.markdown("""
    <style>
    .quote-box {
        background-color: rgba(255, 255, 255, 0.8);
        color: #333;
        font-style: italic;
        font-size: 20px;
        border: 1px solid #ccc;
        padding: 20px 20px 20px 30px;
        margin: 20px auto;
        width: 90%;
        max-width: 800px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    .quote-text {
        margin-bottom: 10px;
    }

    .quote-author {
        font-weight: bold;
        color: #444;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)



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



