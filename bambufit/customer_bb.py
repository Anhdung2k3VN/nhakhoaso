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
    import re
    phone = str(value).strip()
    phone = re.sub(r"[^\d]", "", phone)
    if len(phone) == 9 and not phone.startswith("0"):
        phone = "0" + phone
    elif len(phone) == 10 and phone.startswith("0"):
        pass
    else:
        phone = ""
    return phone

def format_year_to_date(value):
    try:
        year = int(float(value))
        if year == 0:
            return ""
        return f"01/01/{year}"
    except:
        return ""


def process_customer_data(df):
    df.columns = df.columns.str.strip()
    df = df[df["ID"].notna()]  # loại bỏ dòng trống

    df["Di động"] = df["Di động"].apply(convert_sdt)
    df["NS"] = df["NS"].apply(format_year_to_date)
    df["G.Tính"] = df["G.Tính"].apply(convert_gender)

    df.drop_duplicates(subset=["ID"], inplace=True)

    output_df = pd.DataFrame({
        "Mã KH": df["ID"].astype(str),
        "Tên khách hàng* \n(bắt buộc)": df["Họ và tên"].fillna(""),
        "Điện thoại": df["Di động"],
        "Email": "",
        "Ngày sinh \n(DD/MM/YYYY hoặc DD-MM-YYYY)": df["NS"],
        "Giới tính \n(1. Nam, 2. Nữ, 3. Khác)": df["G.Tính"],
        "Địa chỉ": df["Địa chỉ"].fillna(""),
        "Nguồn": df["Nguồn khách"].fillna(""),
        "Ghi chú": ""
    })

    return output_df

def customer_file_bambufit(uploaded_file):
    try:
        input_df = pd.read_excel(uploaded_file, sheet_name=None)
        sheet_names = list(input_df.keys())
        df = input_df[sheet_names[0]]

        processed_df = process_customer_data(df)

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
