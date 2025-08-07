import pandas as pd
from io import BytesIO
import streamlit as st

def format_datetime(value):
    try:
        dt = pd.to_datetime(value, dayfirst=True, errors='coerce')
        if pd.isna(dt):
            return ""
        return dt.strftime("%d/%m/%Y %H:%M")
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
        val_str = ''.join(filter(str.isdigit, val_str))  # giữ lại chỉ số
        if len(val_str) == 9 and not val_str.startswith("0"):
            val_str = "0" + val_str
        elif len(val_str) == 10 and val_str.startswith("0"):
            pass
        else:
            val_str = ""
        return val_str
    except:
        return ""

def process_customer_data(df):
    df.columns = df.columns.str.strip()

    # 💡 Chỉ định các cột thông tin cần fill xuống
    columns_to_fill = ["ID", "Họ và tên", "Di động"]

    df[columns_to_fill] = df[columns_to_fill].fillna(method='ffill')

    rows = []
    for _, row in df.iterrows():
        ngay = row.get("Ngày")
        gio = row.get("Giờ")
        datetime_str = f"{ngay} {gio}"

        new_row = {
            "Mã KH": safe_str(row.get("ID")),
            "Tên khách hàng": safe_str(row.get("Họ và tên")),
            "SDT khách hàng": safe_phone(row.get("Di động")),
            "Ngày điều trị (*)": format_datetime(datetime_str),
            "Thông tin điều trị (*)": safe_str(row.get("Thủ thuật")),
            "Răng/Chẩn đoán": safe_str(row.get("Nội dung điều trị")),
            "Tổng tiền": safe_int(row.get("Phải trả")),
            "Thanh toán": safe_int(row.get("Đã thu")),
            "Còn lại": safe_int(row.get("Còn nợ")),
            "Bác sĩ": safe_str(row.get("Bác sỹ")),
            "Phụ tá": "",
            "Nguồn tiền": "",
            "Mã dịch vụ": "",
            "Trạng thái": ""
        }
        rows.append(new_row)

    return pd.DataFrame(rows)


def data_loaded_file(uploaded_file):
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
            file_name="output_khachhang.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"❌ Lỗi xử lý file: {e}")


