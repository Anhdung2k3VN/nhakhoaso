# app.py
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Gộp Excel + Chuẩn hoá Ngày", layout="wide")


def normalize_date_column(df: pd.DataFrame, col_name: str = "Ngày", output_format: str = "%d/%m/%Y %H:%M"):
    """
    Chuẩn hoá cột ngày:
      - Nhận cả chuỗi, ISO, có microseconds, và cả số serial Excel (45678.5)
      - Trả về CHUỖI theo output_format để Excel không tự đổi
    """
    if col_name not in df.columns:
        return df  # không có cột -> bỏ qua

    s = df[col_name].astype(str).str.strip().replace({"nan": "", "NaT": ""})
    # đánh dấu ô nào là số serial Excel (ví dụ "45678.5")
    num_mask = s.str.fullmatch(r"\d+(\.\d+)?", na=False)

    # parse chuỗi ngày
    dt_text = pd.to_datetime(
        s.where(~num_mask)  # chỉ phần không phải số
         .str.replace("T", " ", regex=False)            # ISO -> space
         .str.replace(r"\.\d{3,6}$", "", regex=True),   # bỏ microseconds .893000
        dayfirst=True, errors="coerce"
    )

    # parse số serial excel (mốc 1899-12-30)
    base = pd.Timestamp("1899-12-30")
    dt_num = pd.to_timedelta(
        pd.to_numeric(s.where(num_mask), errors="coerce"), unit="D"
    ) + base

    # gộp 2 kết quả, cái nào parse được dùng cái đó
    dt = dt_text.fillna(dt_num)

    # format về CHUỖI để Excel không tự đổi
    df[col_name] = dt.dt.strftime(output_format).fillna("")

    return df


@st.cache_data
def convert_df_to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()


def gop_excel(files, date_col_name="Ngày", date_output_format="%d/%m/%Y %H:%M"):
    st.subheader("📁 Gộp các file Excel")

    combined_df = pd.DataFrame()
    for file in files:
        # Đọc: mặc định để pandas tự suy kiểu; đọc lỗi ô lẻ vẫn ok
        df = pd.read_excel(file, engine="openpyxl")
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    st.success(f"✅ Đã gộp {len(files)} file. Tổng {len(combined_df)} dòng.")

    # ============== Làm sạch nhẹ ==============
    # Bỏ cột trùng tên (nếu có)
    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

    # Chuẩn hoá kiểu số nguyên bị đọc thành float .0
    # (chỉ áp dụng cho cột numeric hoặc float)
    for col in combined_df.select_dtypes(include=["float"]):
        try:
            # nếu toàn bộ là số nguyên -> chuyển sang Int64 (giữ NaN)
            if pd.notna(combined_df[col]).all() and (combined_df[col] % 1 == 0).all():
                combined_df[col] = combined_df[col].astype("Int64")
        except Exception:
            # có NaN hoặc dữ liệu lẫn -> bỏ qua
            pass

    # Với cột object, thay NaN bằng chuỗi rỗng, rồi ép về str để export an toàn
    for col in combined_df.columns:
        if combined_df[col].dtype == "object":
            combined_df[col] = combined_df[col].fillna("").astype(str)

    # ============== Chuẩn hoá cột ngày ==============
    combined_df = normalize_date_column(
        combined_df, col_name=date_col_name, output_format=date_output_format
    )

    # Hiển thị preview
    st.subheader("📊 Dữ liệu sau khi gộp & chuẩn hoá")
    st.dataframe(combined_df, use_container_width=True)

    # Xuất file
    excel_bytes = convert_df_to_excel_bytes(combined_df)
    st.download_button(
        label="📥 Tải file đã gộp",
        data=excel_bytes,
        file_name="file_da_gop.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# ======================== UI ========================
st.title("🧩 Gộp Excel & Chuẩn hoá cột Ngày")
st.markdown(
    "- Tải lên **nhiều file Excel** (xlsx).\n"
    "- Cột ngày mặc định là **'Ngày'**. Bạn có thể đổi tên cột và định dạng xuất."
)

left, right = st.columns([2, 1])
with left:
    files = st.file_uploader(
        "Chọn các file Excel (xlsx)", type=["xlsx"], accept_multiple_files=True
    )

with right:
    date_col_name = st.text_input("Tên cột ngày:", value="Ngày")
    fmt_choice = st.selectbox(
        "Định dạng ngày xuất:",
        options=[
            "%d/%m/%Y %H:%M",
            "%d/%m/%Y %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
            "%d/%m/%Y",
        ],
        index=0,
    )

st.markdown("---")

if files:
    try:
        gop_excel(files, date_col_name=date_col_name, date_output_format=fmt_choice)
    except Exception as e:
        st.error(f"❌ Lỗi khi gộp file: {e}")
else:
    st.info("⬆️ Hãy chọn ít nhất 1 file Excel để bắt đầu.")
