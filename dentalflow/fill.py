# fill.py

import streamlit as st
import pandas as pd
from io import BytesIO

def process_excel(file):
    # Đọc file, ép kiểu 'Điện thoại' về dạng chuỗi
    df = pd.read_excel(file, dtype={'Điện thoại': str})

    # Xử lý điền dữ liệu từ dưới lên
    df_reversed = df[::-1].copy()
    df_filled = df_reversed.ffill()
    df_result = df_filled[::-1]

    return df_result

def to_excel_bytes(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

def render_fill_page(uploaded_file):
    st.subheader("📊 Kết quả sau khi xử lý:")

    # Gọi xử lý
    df_result = process_excel(uploaded_file)
    st.dataframe(df_result.head())

    # Nút tải file kết quả
    excel_data = to_excel_bytes(df_result)
    st.download_button(
        label="📥 Tải xuống file đã xử lý",
        data=excel_data,
        file_name="output_filled.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
