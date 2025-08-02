import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Chuyển đổi số dòng", layout="centered")

@st.cache_data
def convert_df(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

def split_and_download_excel(uploaded_file, rows_per_file):
    try:
        if uploaded_file is not None: 
            df = pd.read_excel(uploaded_file, engine='openpyxl', dtype=str)

        st.success("✅ Đã đọc file thành công!")
        st.subheader("📄 Các cột trong file:")
        st.write(df.columns.tolist())
        st.subheader("👁️ Xem trước dữ liệu:")
        st.dataframe(df.head(10))

  
      
        output_prefix = "data_split_"
        total_rows = len(df)
        total_parts = (total_rows + rows_per_file - 1) // rows_per_file

        st.write(f"🔹 Tổng số dòng: {total_rows}")
        st.write(f"🔹 Sẽ chia thành {total_parts} file nhỏ.")

        for i in range(total_parts):
            start = i * rows_per_file
            end = min(start + rows_per_file, total_rows)
            df_part = df.iloc[start:end]
            output = convert_df(df_part)
            st.download_button(
                label=f"📥 Tải file kết quả {i+1}",
                data=output,
                file_name=f"{output_prefix}{i+1}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Lỗi khi xử lý: {e}")



