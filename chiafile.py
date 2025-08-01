import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Chuyển đổi số dòng", layout="centered")

def split_and_download_excel(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl', dtype=str)
        st.success("✅ Đã đọc file thành công!")

        # Hiển thị cột
        st.subheader("📄 Các cột trong file:")
        st.write(df.columns.tolist())

        # ==== BƯỚC XỬ LÝ ====
        rows_per_file = 4999  # Số dòng tối đa mỗi file (bao gồm tiêu đề)
        
        output_prefix = "data_split_"

        # --- Số dòng và số phần cần chia ---
        total_rows = len(df)
        total_parts = (total_rows + rows_per_file - 1) // rows_per_file

        st.write(f"🔹 Tổng số dòng: {total_rows}")
        st.write(f"🔹 Sẽ chia thành {total_parts} file, mỗi file tối đa {rows_per_file} dòng (có tiêu đề)")

        # --- Lặp và ghi từng phần nhỏ ---
        for i in range(total_parts):
            start = i * rows_per_file
            end = min(start + rows_per_file, total_rows)
            df_part = df.iloc[start:end]  # vẫn giữ tiêu đề (header)

            # ==== TẢI FILE ====
            @st.cache_data
            def convert_df(df):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                return output.getvalue()

            output = convert_df(df_part)

            st.download_button(
                label=f"📥 Tải file kết quả {i+1}",
                data=output,
                file_name=f"{output_prefix}{i+1}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Lỗi khi xử lý: {e}")

