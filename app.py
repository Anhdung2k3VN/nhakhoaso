import streamlit as st
import pandas as pd

st.title("🔍 xử lý dữ liệu Excel")

uploaded_file = st.file_uploader("📂 Tải lên file Excel (.xlsx)", type="xlsx")

