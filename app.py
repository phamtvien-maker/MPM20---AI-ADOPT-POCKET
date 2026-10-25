import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="MPM20 - AI Adopt Pocket",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# GIAO DIỆN CSS: TÔ MÀU SẴN + HIỆU ỨNG 3D NỔI BẬT CHO 2 TAB
# ==========================================
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #e2e8f0;
    }
    
    /* Cấu hình tổng thể cho các Tab chính */
    div[data-baseweb="tab-list"] {
        gap: 12px !important;
        padding: 5px 0px !important;
    }

    /* Target trực tiếp nút Tab 1 (Nhánh 1) - Xanh lá nhạt + Hiệu ứng 3D */
    div[data-baseweb="tab-list"] button:nth-child(1) {
        background: linear-gradient(145deg, #dcfce7, #bbf7d0) !important;
        color: #14532d !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        border-radius: 10px 10px 0px 0px !important;
        border: 2px solid #86efac !important;
        box-shadow: 0px 6px 10px rgba(34, 197, 94, 0.25), inset 0px 1px 0px rgba(255, 255, 255, 0.8) !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Target trực tiếp nút Tab 2 (Nhánh 2) - Xanh dương nhạt + Hiệu ứng 3D */
    div[data-baseweb="tab-list"] button:nth-child(2) {
        background: linear-gradient(145deg, #e0f2fe, #bae6fd) !important;
        color: #0c4a6e !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        border-radius: 10px 10px 0px 0px !important;
        border: 2px solid #7dd3fc !important;
        box-shadow: 0px 6px 10px rgba(2, 132, 199, 0.25), inset 0px 1px 0px rgba(255, 255, 255, 0.8) !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Khi di chuột (Hover) tạo hiệu ứng nhô cao 3D */
    div[data-baseweb="tab-list"] button:nth-child(1):hover {
        transform: translateY(-3px) !important;
        box-shadow: 0px 8px 15px rgba(34, 197, 94, 0.4) !important;
    }
    div[data-baseweb="tab-list"] button:nth-child(2):hover {
        transform: translateY(-3px) !important;
        box-shadow: 0px 8px 15px rgba(2, 132, 199, 0.4) !important;
    }

    /* Trang thái Active khi được bấm chọn */
    div[data-baseweb="tab-list"] button[aria-selected="true"]:nth-child(1) {
        background: linear-gradient(145deg, #16a34a, #15803d) !important;
        color: #ffffff !important;
        border-color: #22c55e !important;
        box-shadow: 0px 8px 15px rgba(22, 163, 74, 0.5) !important;
    }
    div[data-baseweb="tab-list"] button[aria-selected="true"]:nth-child(2) {
        background: linear-gradient(145deg, #0284c7, #0369a1) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0px 8px 15px rgba(2, 132, 199, 0.5) !important;
    }

    /* Khung chat thảo luận */
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
        st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🚀 MPM20 – AI Adopt Pocket</h2>", unsafe_allow_html=True)
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
user_email = st.session_state.user_email
st.session_state.active_users.add(user_email)

hcol1, hcol2, hcol3 = st.columns([3, 3, 2])
with hcol1:
    st.markdown(f"👤 **Thành viên:** `{user_email}`")
with hcol2:
    st.markdown(f"🟢 **Online:** `{len(st.session_state.active_users)} người` | 📊 **Truy cập hôm nay:** `{st.session_state.daily_visits} lượt`")
with hcol3:
    if st.button("🚪 Đăng xuất", use_container_width=True):
        if user_email in st.session_state.active_users:
            st.session_state.active_users.remove(user_email)
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()

st.markdown("---")
st.markdown("## ⚡ MPM20 - Dashboard Quản Trị Dự Án Chuyên Sâu")

# ==========================================
# HÀM HỖ TRỢ UPLOAD & ĐỌC / MỞ TÀI LIỆU CỤ THỂ
# ==========================================
def render_upload_download_section(tab_key, tab_name):
    st.markdown(f"#### 📂 Quản lý tài liệu: {tab_name}")
    
    st.markdown("##### 📤 Upload tài liệu lên hệ thống")
    uploaded_file = st.file_uploader(f"Chọn file từ máy tính cho {tab_name}:", key=f"up_{tab_key}")
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_info = {
            "name": uploaded_file.name, 
            "size": round(uploaded_file.size / 1024, 2), 
            "user": user_email, 
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
                # Nút tải xuống để mở trực tiếp bằng phần mềm mặc định trên máy (Excel, Word, Adobe...)
                st.download_button(
                    label="💻 Tải về & Mở bằng App máy",
                    data=f['data'],
                    file_name=f['name'],
                    key=f"dl_file_{tab_key}_{idx}"
                )
            with f_col3:
                if st.button("📖 Xem nhanh trên Web", key=f"read_file_{tab_key}_{idx}"):
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
                            st.info("💡 Để xem và chỉnh sửa file này bằng phần mềm chuyên dụng (Excel, Word, AutoCAD, Powerpoint...) trên máy tính của bạn, vui lòng bấm nút **'💻 Tải về & Mở bằng App máy'** sát bên cạnh.")
                    except Exception as e:
                        st.error(f"Không thể đọc trực tiếp file này trên web: {e}")
            st.markdown("---")
    else:
        st.write("_Chưa có tài liệu nào được tải lên._")

# ==========================================
# ĐIỀU HƯỚNG NHÁNH CHÍNH (ĐÃ TÔ MÀU 3D ĐẶC BIỆT)
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
