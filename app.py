import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
# Cấu hình kết nối Cloudinary bảo mật từ Streamlit Secrets
import cloudinary
import cloudinary.uploader
import cloudinary.api
import cloud_sync
# Cấu hình kết nối Cloudinary bảo mật từ Streamlit Secrets
cloudinary.config(
    cloud_name = st.secrets["CLOUDINARY_CLOUD_NAME"],
    api_key = st.secrets["CLOUDINARY_API_KEY"],
    api_secret = st.secrets["CLOUDINARY_API_SECRET"],
    secure = True
)


# Cấu hình giao diện trang web
st.set_page_config(
    page_title="MPM20 - AI Adopt Pocket",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Tự động khôi phục phiên đăng nhập từ URL ngay khi tải lại trang (F5)
if "logged_in_user" in st.query_params and not st.session_state.get("authenticated", False):
    st.session_state["authenticated"] = True
    # Lưu phiên vào URL để chống mất trạng thái khi Refresh
st.query_params["logged_in_user"] = st.session_state["user_email"]
# ==========================================
# CSS ĐẶC BIỆT: ÉP BUỘC TÔ MÀU 2 TAB CHÍNH
# ==========================================
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }
    header {visibility: hidden;}
    
    .main {
        background-color: #0e1117;
        color: #e2e8f0;
    }

    /* Ép màu cho các tab bằng thuộc tính cấu trúc nội bộ của Streamlit */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #161b22;
        padding: 10px;
        border-radius: 12px;
    }

    /* Tab 1: Xanh lá hơi đậm (#15803d) */
    .stTabs [data-baseweb="tab-list"] button:nth-child(1) {
        background-color: #15803d !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        border: 1px solid #22c55e !important;
    }

    /* Tab 2: Xanh dương hơi đậm (#0369a1) */
    .stTabs [data-baseweb="tab-list"] button:nth-child(2) {
        background-color: #0369a1 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        border: 1px solid #38bdf8 !important;
    }

    /* Trạng thái khi hover hoặc active */
    .stTabs [data-baseweb="tab-list"] button:nth-child(1):hover,
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"]:nth-child(1) {
        background-color: #166534 !important;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
    }

    .stTabs [data-baseweb="tab-list"] button:nth-child(2):hover,
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"]:nth-child(2) {
        background-color: #075985 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }

    .chat-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CƠ SỞ DỮ LIỆU TÀI KHOẢN & BỘ NHỚ LƯU TRỮ
# ==========================================
USER_CREDENTIALS = {
    "vuongtbichtuyen@gmail.com": "123456",
    "230110quynhanh@gmail.com": "123456",
    "phamtvien@gmail.com": "123456",
}

if "discussions" not in st.session_state:
    st.session_state.discussions = []

if "call_status" not in st.session_state:
    st.session_state.call_status = False

if "uploaded_files_store" not in st.session_state:
    st.session_state.uploaded_files_store = {}

for tab_k in ["doc", "exams", "disc", "insight", "appcode", "example", "pm", "qs"]:
    if tab_k not in st.session_state.uploaded_files_store:
        st.session_state.uploaded_files_store[tab_k] = []

if "active_users" not in st.session_state:
    st.session_state.active_users = set()

if "daily_visits" not in st.session_state:
    st.session_state.daily_visits = 0
    st.session_state.last_visit_date = datetime.now().date()

today = datetime.now().date()
if st.session_state.last_visit_date != today:
    st.session_state.daily_visits = 0
    st.session_state.last_visit_date = today

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# ==========================================
# GIAO DIỆN ĐĂNG NHẬP
# ==========================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🚀 MPM20 – AI</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Đăng nhập hệ thống bảo mật nội bộ</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            input_email = st.text_input("📧 Email Google:")
            input_password = st.text_input("🔑 Mật khẩu:", type="password")
            submit_btn = st.form_submit_button("Đăng nhập hệ thống", use_container_width=True)
            
            if submit_btn:
                cleaned_email = input_email.strip().lower()
                if cleaned_email in USER_CREDENTIALS and USER_CREDENTIALS[cleaned_email] == input_password:
                    st.session_state.logged_in = True
                    st.session_state.user_email = cleaned_email
                    st.session_state.active_users.add(cleaned_email)
                    st.session_state.daily_visits += 1
                    st.rerun()
                else:
                    st.error("❌ Sai Email hoặc Mật khẩu truy cập!")
    st.stop()

# ==========================================
# SAU KHI ĐĂNG NHẬP THÀNH CÔNG
# ==========================================
# Sửa lại đoạn gán query params an toàn hơn:
if "user_email" in st.session_state:
    st.query_params["logged_in_user"] = st.session_state["user_email"]
# ==========================================
user_email = st.session_state.user_email
st.session_state.active_users.add(user_email)

top_col1, top_col2, top_col3 = st.columns([3, 3, 1])
with top_col1:
    st.markdown("### ⚡ MPM20 - AI")
with top_col2:
    st.markdown(f"👤 `{user_email}` | 🟢 Online: **{len(st.session_state.active_users)}** | 📊 Hôm nay: **{st.session_state.daily_visits}**")
with top_col3:
    if st.button("Đăng xuất", use_container_width=True):
            st.query_params.clear()  # <-- CHÈN DÒNG NÀY VÀO DÒNG 180
            if user_email in st.session_state.active_users:
                st.session_state.active_users.remove(user_email)
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.rerun()

st.markdown("<hr style='margin: 0px 0px 10px 0px; border-color: #30363d;'>", unsafe_allow_html=True)

# ==========================================
# HÀM HỖ TRỢ UPLOAD & ĐỌC / MỞ TÀI LIỆU
# ==========================================
def render_upload_download_section(tab_key, tab_name):
    # --- CHÈN DÒNG NÀY VÀO NGAY ĐẦU HÀM ---
    cloud_sync.sync_files_from_cloudinary(tab_key)
    st.markdown(f"#### 📂 Quản lý tài liệu: {tab_name}")
    
    st.markdown("##### 📤 Upload tài liệu lên hệ thống")
    uploaded_file = st.file_uploader(f"Chọn file từ máy tính cho {tab_name}:", key=f"up_{tab_key}")
    if uploaded_file is not None:
        # --- ĐỒNG BỘ LÊN CLOUDINARY VĨNH VIỄN ---
        with st.spinner("Đang đồng bộ file lên Cloudinary..."):
            try:
                resource_type = "image" if uploaded_file.type.startswith("image/") else "raw"
                response = cloudinary.uploader.upload(
                    uploaded_file,
                    folder="MPM20_AI_Storage",
                    public_id=uploaded_file.name,
                    resource_type=resource_type,
                    overwrite=True
                )
                file_url = response.get('secure_url')
                st.success(f"✅ Đã lưu vĩnh viễn file {uploaded_file.name} lên Cloud!")
            except Exception as e:
                st.error(f"❌ Lỗi đồng bộ Cloud: {e}")
        # ----------------------------------------

        file_bytes = uploaded_file.getvalue()
        file_info = {
            "name": uploaded_file.name,
            "size": round(uploaded_file.size / 1024, 2),
            "user": user_email,
            "time": (datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S"),
            "data": file_bytes,
            "type": uploaded_file.type
        }
        if tab_key not in st.session_state.uploaded_files_store:
            st.session_state.uploaded_files_store[tab_key] = []
        
        if not any(f['name'] == uploaded_file.name and f['time'] == file_info['time'] for f in st.session_state.uploaded_files_store[tab_key]):
            st.session_state.uploaded_files_store[tab_key].append(file_info)
            st.success(f"✅ Đã lưu file **{uploaded_file.name}** thành công!")

    st.markdown("---")
    st.markdown("##### 📚 Danh sách tài liệu đã lưu & Tùy chọn đọc/mở:")
    
    if tab_key in st.session_state.uploaded_files_store and st.session_state.uploaded_files_store[tab_key]:
        for idx, f in enumerate(st.session_state.uploaded_files_store[tab_key]):
            f_col1, f_col2, f_col3 = st.columns([3, 1, 1])
            with f_col1:
                st.markdown(f"📄 **{f['name']}** `({f['size']} KB)`<br><span style='font-size:0.8rem; color:gray;'>Tải bởi: {f['user']} [{f['time']}]</span>", unsafe_allow_html=True)
            with f_col2:
                st.download_button(
                    label="💻 Tải về & Mở App máy",
                    data=f['data'],
                    file_name=f['name'],
                    key=f"dl_file_{tab_key}_{idx}"
                )
            with f_col3:
                if st.button("📖 Xem nhanh", key=f"read_file_{tab_key}_{idx}"):
                    st.session_state[f"view_{tab_key}_{idx}"] = not st.session_state.get(f"view_{tab_key}_{idx}", False)

            if st.session_state.get(f"view_{tab_key}_{idx}", False):
                with st.expander(f"🔎 Xem nội dung trực tuyến: {f['name']}", expanded=True):
                    try:
                        if "text" in f['type'] or f['name'].endswith(('.txt', '.py', '.csv', '.md', '.json')):
                            st.text(f['data'].decode("utf-8", errors="ignore"))
                        elif f['name'].endswith(('.xlsx', '.xls')):
                            df_view = pd.read_excel(io.BytesIO(f['data']))
                            st.dataframe(df_view, use_container_width=True)
                        elif "image" in f['type']:
                            st.image(f['data'], caption=f['name'])
                        else:
                            st.info("💡 Vui lòng bấm nút **'💻 Tải về & Mở App máy'** để xem file bằng phần mềm chuyên dụng (Excel, Word, AutoCAD...) trên máy tính.")
                    except Exception as e:
                        st.error(f"Không thể đọc file này: {e}")
            st.markdown("---")
    else:
        st.write("_Chưa có tài liệu nào được tải lên._")

# ==========================================
# ĐIỀU HƯỚNG 2 NHÁNH CHÍNH
# ==========================================
main_tab1, main_tab2 = st.tabs([
    "📌 Nhánh 1: MPM (Quản trị & Tri thức)", 
    "🛠️ Nhánh 2: Ứng dụng & Thực thi (App/Code)"
])

# ==========================================
# NỘI DUNG NHÁNH 1
# ==========================================
with main_tab1:
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "📄 Doc", 
        "📝 Exams", 
        "💬 Disc. (Thảo luận & Gọi nhóm)", 
        "💡 Core Insight"
    ])
    
    with sub_tab1:
        render_upload_download_section("doc", "Doc (Tài liệu)")
            
    with sub_tab2:
        render_upload_download_section("exams", "Exams (Bài kiểm tra)")
        st.markdown("---")
        st.markdown("##### Câu hỏi đánh giá nhanh:")
        ans = st.radio("Đâu là tiêu chí quan trọng nhất trong quản lý chi phí (QS)?", ("Kiểm soát khối lượng & dự toán", "Thời gian họp"), key="ex_r")
        if st.button("Kiểm tra kết quả"):
            if "Kiểm soát" in ans:
                st.success("Chính xác tuyệt đối!")
            else:
                st.error("Chưa chính xác.")
                
    with sub_tab3:
        st.markdown("#### 💬 Thảo luận nhóm nội bộ & Cuộc gọi trực tuyến")
        
        call_col1, call_col2 = st.columns([2, 2])
        with call_col1:
            if not st.session_state.call_status:
                if st.button("📞 🟢 Bắt đầu cuộc gọi nhóm", use_container_width=True):
                    st.session_state.call_status = True
                    st.rerun()
            else:
                if st.button("📴 🔴 Kết thúc cuộc gọi nhóm", use_container_width=True):
                    st.session_state.call_status = False
                    st.rerun()
        with call_col2:
            if st.session_state.call_status:
                st.markdown("🟢 **Trạng thái:** Đang trong cuộc gọi nhóm trực tuyến...")
            else:
                st.markdown("⚪ **Trạng thái:** Cuộc gọi đã kết thúc.")

        st.markdown("---")
        render_upload_download_section("disc", "Disc (Thảo luận)")
        
        st.markdown("---")
        st.markdown("##### 📜 Luồng cuộc trò chuyện nhóm (Gom gọn trong khung):")
        
        with st.container():
            st.markdown('<div class="chat-box">', unsafe_allow_html=True)
            if st.session_state.discussions:
                for item in st.session_state.discussions:
                    st.markdown(f"💬 **{item['user']}** <span style='color: gray; font-size: 0.8rem;'>({item['time']})</span>:<br>{item['content']}", unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 5px 0; border-color: #30363d;'>", unsafe_allow_html=True)
            else:
                st.write("_Chưa có nội dung trò chuyện nào._")
            st.markdown('</div>', unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            chat_input = st.text_input("Nhập nội dung trao đổi...")
            send_chat = st.form_submit_button("Gửi tin nhắn")
            if send_chat and chat_input.strip():
                new_msg = {
                    "user": user_email,
                    "content": chat_input.strip(),
                    "time": datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
                }
                st.session_state.discussions.append(new_msg)
                st.rerun()
            
    with sub_tab4:
        render_upload_download_section("insight", "Core Insight")
        st.markdown("---")
        st.info("Phân tích chiến lược tích hợp AI vào vận hành quản lý dự án, tối ưu hóa dòng tiền và tiến độ thi công hạ tầng đô thị.")

# ==========================================
# NỘI DUNG NHÁNH 2
# ==========================================
with main_tab2:
    sub_tab_2a, sub_tab_2b, sub_tab_2c, sub_tab_2d = st.tabs([
        "💻 App & Code", 
        "📊 Example Works", 
        "🏗️ PM Construction", 
        "📐 QS Construction"
    ])
    
    with sub_tab_2a:
        render_upload_download_section("appcode", "App & Code")
        st.markdown("---")
        st.code("""import pandas as pd
def process_qs_data(file_path):
    df = pd.read_excel(file_path)
    return df""", language="python")
        
    with sub_tab_2b:
        render_upload_download_section("example", "Example Works")
        st.markdown("---")
        st.write("- Mô phỏng quản lý hạ tầng Khu đô thị Vạn Phúc.\n- Tự động hóa báo cáo tuần qua Python & Excel.")
        
    with sub_tab_2c:
        render_upload_download_section("pm", "PM Construction")
            
    with sub_tab_2d:
        render_upload_download_section("qs", "QS Construction")
        st.markdown("---")
        qs_df = pd.DataFrame([
            {"STT": 1, "Hạng mục": "Bê tông móng", "Khối lượng": "1,200 m3", "Đơn giá (VND)": "1,500,000"},
            {"STT": 2, "Hạng mục": "Cốt thép D12-D28", "Khối lượng": "120 Tấn", "Đơn giá (VND)": "18,000,000"}
        ])
        st.dataframe(qs_df, use_container_width=True)
