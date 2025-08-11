import streamlit as st
import os
import glob
from wallpaper_api import get_wallpapers_combined
from streamlit_image_select import image_select
from navbar import set_background  # nếu bạn dùng set_background từ navbar

def init_background_state():
    if 'bg_initialized' not in st.session_state:
        st.session_state.bg_initialized = True
        st.session_state.wallpapers = None
        st.session_state.bg_page_number = 1
        st.session_state.bg_last_query = "minimal"
        st.session_state.use_local_backgrounds = False

def get_local_backgrounds():
    """Get list of local background images"""
    background_dir = "asset/img"
    patterns = ["*.jpg", "*.jpeg", "*.png", "*.webp"]
    backgrounds = []
    
    for pattern in patterns:
        backgrounds.extend(glob.glob(os.path.join(background_dir, pattern)))
    
    # Filter and format the backgrounds
    formatted_backgrounds = []
    for bg in backgrounds:
        if os.path.exists(bg):
            formatted_backgrounds.append({
                "path": bg,
                "name": os.path.basename(bg),
                "thumb": bg,  # Use the same image as thumbnail for local files
                "full": bg
            })
    
    return formatted_backgrounds

def load_wallpapers(query="minimal", total=12, page=1):
    try:
        results = get_wallpapers_combined(query=query, total=total, page=page)
        return {
            "thumbs": [img["thumb"] for img in results if "thumb" in img and "full" in img],
            "fulls": [img["full"] for img in results if "thumb" in img and "full" in img]
        }
    except Exception as e:
        st.warning(f"⚠️ Không thể kết nối với API hình nền online. Chuyển sang chế độ offline.")
        # Switch to local backgrounds when API fails
        st.session_state.use_local_backgrounds = True
        return {"thumbs": [], "fulls": []}

def render_background_selector(total_per_page=12):
    init_background_state()

    # ======= Header + Search Box on same line =======
    col_title, col_search, col_mode = st.columns([2, 1.5, 1])

    with col_title:
        st.subheader("🖼️ Chọn hình nền cho ứng dụng")

    with col_mode:
        # Toggle between online and offline mode
        use_local = st.toggle("📁 Chế độ offline", value=st.session_state.use_local_backgrounds)
        if use_local != st.session_state.use_local_backgrounds:
            st.session_state.use_local_backgrounds = use_local
            st.session_state.wallpapers = None
            st.rerun()

    # Áp dụng background nếu đã chọn
    if st.session_state.get("bg_path"):
        set_background(st.session_state.bg_path)

    if st.session_state.use_local_backgrounds:
        # ======= LOCAL BACKGROUNDS MODE =======
        st.info("📁 Đang sử dụng hình nền cục bộ")
        local_backgrounds = get_local_backgrounds()
        
        if not local_backgrounds:
            st.warning("⚠️ Không tìm thấy hình nền cục bộ nào.")
            return
        
        # Display local backgrounds
        thumbs = [bg["thumb"] for bg in local_backgrounds]
        fulls = [bg["full"] for bg in local_backgrounds]
        
        selected_thumb = image_select(
            label="Chọn hình nền:",
            images=thumbs,
            use_container_width=True,
            key="local_bg_selector"
        )
        
        if selected_thumb:
            try:
                selected_index = thumbs.index(selected_thumb)
                new_bg = fulls[selected_index]
                if st.session_state.get("bg_path") != new_bg:
                    st.session_state.bg_path = new_bg
                    st.toast("✅ Đã cập nhật hình nền mới!")
                    set_background(new_bg)
                    st.rerun()
            except ValueError:
                st.warning("⚠️ Không xác định được hình nền.")
    
    else:
        # ======= ONLINE BACKGROUNDS MODE =======
        with col_search:
            st.markdown("""
                <style>
                div[data-testid="stTextInput"] {
                    width: 100%;
                    position: relative;
                    margin-top: -0.3rem;
                }
                div[data-testid="stTextInput"] > div {
                    position: relative;
                }
                div[data-testid="stTextInput"] input {
                    padding-right: 2.2rem !important;
                    height: 38px;
                    font-size: 15px;
                    border: 1px solid #ccc;
                    border-radius: 6px;
                }
                div[data-testid="stTextInput"]::after {
                    content: "🔍";
                    position: absolute;
                    right: 12px;
                    top: 50%;
                    transform: translateY(-50%);
                    font-size: 16px;
                    color: #888;
                    pointer-events: none;
                }
                </style>
            """, unsafe_allow_html=True)

            query = st.text_input("Tìm kiếm", value=st.session_state.bg_last_query, label_visibility="collapsed")

        # Nếu từ khóa thay đổi → reset
        if st.session_state.bg_last_query != query:
            st.session_state.bg_last_query = query
            st.session_state.wallpapers = None
            st.session_state.bg_page_number = 1

        # ======= Pagination buttons =======
        col1, col2, _ = st.columns([1, 1, 10])
        with col1:
            if st.session_state.bg_page_number > 1 and st.button("⬅️"):
                st.session_state.bg_page_number -= 1
                st.session_state.wallpapers = None
                st.rerun()
        with col2:
            if st.button("➡️"):
                st.session_state.bg_page_number += 1
                st.session_state.wallpapers = None
                st.rerun()

        # Tải hình nền nếu cần
        if st.session_state.wallpapers is None:
            with st.spinner("🔄 Đang tải hình nền..."):
                st.session_state.wallpapers = load_wallpapers(
                    query=query,
                    total=total_per_page,
                    page=st.session_state.bg_page_number
                )

        wp = st.session_state.wallpapers
        if not wp["thumbs"]:
            if st.session_state.use_local_backgrounds:
                st.info("🔄 Đã chuyển sang chế độ offline tự động.")
            else:
                st.warning("⚠️ Không tìm thấy hình nền phù hợp.")
                if st.button("📁 Chuyển sang chế độ offline"):
                    st.session_state.use_local_backgrounds = True
                    st.rerun()
        else:
            selected_thumb = image_select(
                label="",
                images=wp["thumbs"],
                use_container_width=True,
                key="bg_selector"
            )

            if selected_thumb:
                try:
                    selected_index = wp["thumbs"].index(selected_thumb)
                    new_bg = wp["fulls"][selected_index]
                    if st.session_state.get("bg_path") != new_bg:
                        st.session_state.bg_path = new_bg
                        st.toast("✅ Đã cập nhật hình nền mới!")
                        set_background(new_bg)
                        st.rerun()
                except ValueError:
                    st.warning("⚠️ Không xác định được hình nền.")
