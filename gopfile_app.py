import streamlit as st
import pandas as pd
import io

def gop_excel(files):
    try:
        st.subheader("📁 Gộp các file Excel")

        # Gộp dữ liệu từ các file
        combined_df = pd.DataFrame()
        for file in files:
            df = pd.read_excel(file, engine='openpyxl')
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        st.success("✅ Đã gộp file thành công!")

        # ====================
        # Làm sạch dữ liệu số: bỏ .0
        # ====================
        for col in combined_df.select_dtypes(include=["float"]):
            if (combined_df[col] % 1 == 0).all():
                combined_df[col] = combined_df[col].astype("Int64")  # giữ NaN an toàn

        # ====================
        # Thay NaN bằng chuỗi rỗng CHỈ CHO CỘT CHUỖI
        # ====================
        for col in combined_df.select_dtypes(include=["object", "string"]):
            combined_df[col] = combined_df[col].fillna('')

        # ====================
        # Ép kiểu object -> string (tránh lỗi khi export)
        # ====================
        for col in combined_df.select_dtypes(include=["object"]):
            combined_df[col] = combined_df[col].astype(str)

        # ====================
        # Loại bỏ cột bị trùng tên (nếu có)
        # ====================
        combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

        # Hiển thị preview
        st.subheader("📊 Dữ liệu sau khi gộp")
        st.dataframe(combined_df)

        # Chuẩn bị file để tải
        @st.cache_data
        def convert_df(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        output = convert_df(combined_df)

        st.download_button(
            label="📥 Tải file đã gộp",
            data=output,
            file_name="file_da_gop.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Lỗi khi gộp file: {e}")
