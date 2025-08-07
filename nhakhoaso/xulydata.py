import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Chuyển đổi dữ liệu điều trị", layout="centered")


def xuly_file(uploaded_file):

    try:
        data1 = pd.read_excel(uploaded_file, engine="openpyxl")
        st.success("✅ Đã đọc file thành công!")

        # Hiển thị cột
        st.subheader("📄 Các cột trong file:")
        st.write(data1.columns.tolist())

        # ==== BƯỚC XỬ LÝ ====
        converted = pd.DataFrame()

        # 1. Mã KH
        converted["Mã KH"] = data1.get("Số HS", "")

        # 2. Tên khách hàng
        converted["Tên khách hàng"] = (
            data1.get("Họ và tên")
            .fillna("")
            .astype(str)
            .str.replace(r"\*", "", regex=True)
            .str.strip()
        )

        # 3. SĐT khách hàng
        converted["SDT khách hàng"] = data1.get("Điện thoại", "")

        # 4. Ngày điều trị
        def format_date_safe(x):
            if pd.isna(x):
                return ""
            return pd.to_datetime(x).strftime("%d/%m/%Y 00:00")

        converted["Ngày điều trị"] = data1.get("Ngày", pd.Series([""] * len(data1))).apply(format_date_safe)

        # 5. Thông tin điều trị
        converted["Thông tin điều trị"] = (
            data1.get("Tên thủ thuật ")
            .fillna("")
            .astype(str)
            .str.replace(r"\*", "", regex=True)
            .str.strip()
        )

        # 6. Răng/Chẩn đoán
        converted["Răng/Chẩn đoán"] = data1["Lịch liệu trình"].fillna("KHÁM & TƯ VẤN")


        # 7. Tổng tiền
        converted["Tổng tiền"] = data1.get("Thực thu", 0) + data1.get("Còn nợ", 0)

        # 8. Thanh toán
        converted["Thanh toán"] = data1.get("Thực thu", 0)

        # 9. Còn lại
        converted["Còn lại"] = data1.get("Còn nợ", 0)

        # 10. Bác sĩ
        converted["Bác sĩ"] = (
            data1.get("Bác sĩ")
            .fillna("")
            .astype(str)
            .str.replace(r"\*", "", regex=True)
            .str.strip()
        )

        # 11. Phụ tá
        converted["Phụ tá"] = ""

        # 12. Nguồn tiền
        converted["Nguồn tiền"] = data1.get("HTT Toán", "")

        # 13. Mã dịch vụ
        converted["Mã dịch vụ"] = ""

        # 14. Trạng thái
        converted["Trạng thái"] = ""

        # ==== HIỂN THỊ DỮ LIỆU KẾT QUẢ ====
        st.subheader("📋 Dữ liệu sau khi chuyển đổi")
        st.dataframe(converted)

        # ==== TẢI FILE ====
        @st.cache_data
        def convert_df(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        output = convert_df(converted)

        st.download_button(
            label="📥 Tải file kết quả",
            data=output,
            file_name="converted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Lỗi khi xử lý: {e}")
