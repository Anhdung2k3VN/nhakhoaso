import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Chuyển đổi khách hàng", layout="centered")

def xuly_khach_hang(uploaded_file):
    try:
        data1 = pd.read_excel(uploaded_file, engine="openpyxl")
        st.success("✅ Đã đọc file thành công!")

        # Hiển thị cột
        st.subheader("📄 Các cột trong file:")
        st.write(data1.columns.tolist())

        # Kiểm tra cột bắt buộc
        required_cols = ["Số HS", "Họ và tên", "Điện thoại", "Năm sinh", "Giới tính", "Địa chỉ", "Nguồn khách"]
        missing = [col for col in required_cols if col not in data1.columns]
        if missing:
            st.error(f"❌ Thiếu cột: {', '.join(missing)}")
            return

        # --- Bước 2: Lọc ra khách hàng duy nhất ---
        df_customers = data1[required_cols].drop_duplicates().copy()

        # --- Bước 3: Xử lý giới tính và năm sinh ---
        gender_map = {"Nam": 1, "Nữ": 2}
        df_customers["Giới tính"] = df_customers["Giới tính"].map(gender_map).fillna(3).astype(int)
        df_customers["Năm sinh"] = df_customers["Năm sinh"].apply(
            lambda x: str(int(x)) if pd.notnull(x) else ""
        ).astype(str)

        # --- Bước 4: Tạo DataFrame đầu ra ---
        converted = pd.DataFrame()
        converted["Mã KH\n* Để trống hệ thống sẽ tự tạo mã\n* Cập nhật đè dữ liệu căn cứ vào mã KH"] = df_customers["Số HS"]
        converted["Tên khách hàng* \n(bắt buộc)"] = df_customers["Họ và tên"]
        converted["Điện thoại"] = df_customers["Điện thoại"]
        converted["Email"] = ""
        converted["Ngày sinh \n(DD/MM/YYYY hoặc DD-MM-YYYY)"] = df_customers["Năm sinh"]
        converted["Giới tính \n(1. 1, 2. 2, 3. Khác)"] = df_customers["Giới tính"]
        converted["Địa chỉ"] = df_customers["Địa chỉ"]
        converted["Nguồn\n* Cần tạo nguồn với tên tương ứng trong hệ thống trước khi nhập liệu"] = df_customers["Nguồn khách"]
        converted["Ghi chú"] = ""
        df_output = converted

        st.success("✅ Đã xử lý dữ liệu thành công!")
        st.subheader("📋 Dữ liệu sau khi chuyển đổi")
        st.dataframe(df_output)

        # ==== TẢI FILE ====
        @st.cache_data
        def convert_df(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        output = convert_df(df_output)

        st.download_button(
            label="📥 Tải file kết quả",
            data=output,
            file_name="converted_customers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Lỗi khi xử lý: {e}")

