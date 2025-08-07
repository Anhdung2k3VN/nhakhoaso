import pandas as pd
from io import BytesIO
import streamlit as st

def convert_gender(gender):
    gender = str(gender).strip().lower()
    if gender == "nam":
        return 1
    elif gender == "nữ":
        return 2
    else:
        return 3

def convert_sdt(value):
    phone = str(value).strip()
    phone = phone.replace(".0", "").replace(" ", "").replace("-", "")
    if phone and phone.isdigit() and not phone.startswith("0") and len(phone) == 9:
        phone = "0" + phone
    return phone

def format_date(value):
    try:
        return pd.to_datetime(value, dayfirst=True).strftime("%d/%m/%Y")
    except:
        return ""

def process_customer_data(df):
    df.columns = df.columns.str.strip()

    # Làm sạch số điện thoại và loại bỏ dòng trùng
    df["Điện thoại"] = df["Điện thoại"].apply(convert_sdt)
    df.drop_duplicates(subset=["Mã hồ sơ"], inplace=True)
    # df.drop_duplicates(subset=["Điện thoại"], inplace=True)

    rows = []

    for _, row in df.iterrows():
        new_row = {
            "Mã KH": int(row["Mã hồ sơ"]) if pd.notna(row["Mã hồ sơ"]) else None,
            "Tên khách hàng* \n(bắt buộc)": row.get("Họ tên", ""),
            "Điện thoại": row["Điện thoại"],
            "Email": "",
            "Ngày sinh \n(DD/MM/YYYY hoặc DD-MM-YYYY)": format_date(row.get("Ngày sinh", "")),
            "Giới tính \n(1. Nam, 2. Nữ, 3. Khác)": convert_gender(row.get("Giới tính", "")),
            "Địa chỉ": row.get("Địa chỉ", ""),
            "Nguồn": row.get("Nguồn khách hàng", ""),
            "Ghi chú": ""
        }
        rows.append(new_row)

    return pd.DataFrame(rows)

def handle_customer_file(uploaded_file):
    try:
        input_df = pd.read_excel(uploaded_file)

        processed_df = process_customer_data(input_df)

        st.subheader("📋 Dữ liệu sau xử lý")
        st.dataframe(processed_df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            processed_df.to_excel(writer, index=False)
        output.seek(0)

        st.download_button(
            label="📤 Tải về file kết quả",
            data=output,
            file_name="output_khachhang.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"❌ Lỗi xử lý file: {e}")
