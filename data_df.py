import pandas as pd
from io import BytesIO
import streamlit as st

def format_datetime(value):
    try:
        return pd.to_datetime(value).strftime("%d/%m/%Y %H:%M")
    except:
        return ""

def safe_int(val):
    try:
        return int(float(val)) if pd.notna(val) else 0
    except:
        return 0

def safe_str(val):
    try:
        if pd.isna(val): return ""
        return str(val).strip()
    except:
        return ""

def safe_phone(val):
    try:
        if pd.isna(val):
            return ""
        val_str = str(val).strip()
        if val_str.endswith('.0'):
            val_str = val_str[:-2]
        if not val_str.startswith("0"):
            val_str = "0" + val_str
        return val_str
    except:
        return ""

def merge_phu_ta(pt1, pt2):
    pt1 = safe_str(pt1)
    pt2 = safe_str(pt2)
    if pt1 and pt2:
        return f"{pt1}, {pt2}"
    return pt1 or pt2

def process_customer_data(df):
    df.columns = df.columns.str.strip()
    rows = []

    for _, row in df.iterrows():
        new_row = {
            "Mã KH": safe_int(row.get("Mã hồ sơ")),
            "Tên khách hàng": safe_str(row.get("Họ tên")),
            "SDT khách hàng": safe_phone(row.get("Điện thoại")),
            "Ngày điều trị (*)": format_datetime(row.get("Ngày điều trị")),
            "Thông tin điều trị (*)": safe_str(row.get("Thủ thuật")),
            "Răng/Chẩn đoán": safe_str(row.get("Nội dung điều trị")),
            "Tổng tiền": safe_int(row.get("Phải thanh toán")),
            "Thanh toán": safe_int(row.get("Đã thanh toán")),
            "Còn lại": safe_int(row.get("Còn lại")),
            "Bác sĩ": safe_str(row.get("Bác sĩ điều trị")),
            "Phụ tá": merge_phu_ta(row.get("Trợ thủ 1"), row.get("Trợ thủ 2")),
            "Nguồn tiền": "",
            "Mã dịch vụ": "",
            "Trạng thái": ""
        }
        rows.append(new_row)

    return pd.DataFrame(rows)

def handle_file_upload(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        processed_df = process_customer_data(df)

        st.subheader("📄 Dữ liệu đã xử lý")
        st.dataframe(processed_df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            processed_df.to_excel(writer, index=False)
        output.seek(0)

        st.download_button(
            label="📥 Tải về file kết quả",
            data=output,
            file_name="output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"❌ Lỗi xử lý file: {e}")
