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
# GIAO DIỆN CSS: MÀU SẮC NHẸ NHÀNG, HIỆU ỨNG 3D & KHUNG CHAT
# ==========================================
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #e2e8f0;
    }
    /* Tùy chỉnh màu sắc các Tab nhẹ nhàng, không chói */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: #1e293b;
        border-radius: 8px 8px 0px 0px;
        color: #94a3b8;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #334155;
        color: #f1f5f9;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    /* Khung chat thảo luận gom gọn */
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
}

# Khởi tạo Session State cho lịch sử chat và kho lưu trữ file cho TẤT CẢ các tab
if "discussions" not in st.session_state:
    st.session_state.discussions = []

if "call_status" not in st.session_state:
    st.session_state.call_status = False

if "uploaded_files_store" not in st.session_state:
    st.session_state.uploaded_files_store = {
        "doc": [], "exams": [], "disc": [], "insight": [],
        "appcode": [], "example": [], "pm": [], "qs": []
    }

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

# Header hiển thị thông tin & Thống kê
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
# HÀM HỖ TRỢ HIỂN THỊ KHUNG UPLOAD & DOWNLOAD CHUNG CHO MỌI TAB
# ==========================================
def render_upload_download_section(tab_key, tab_name):
    st.markdown(f"#### 📂 Quản lý tài liệu: {tab_name}")
    col_up, col_down = st.columns(2)
    
    with col_up:
        st.markdown("##### 📤 Upload tài liệu lên hệ thống")
        uploaded_file = st.file_uploader(f"Chọn file cho {tab_name}:", key=f"up_{tab_key}")
        if uploaded_file is not None:
            file_info = {"name": uploaded_file.name, "size": round(uploaded_file.size / 1024, 2), "user": user_email, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            if file_info not in st.session_state.uploaded_files_store[tab_key]:
                st.session_state.uploaded_files_store[tab_key].append(file_info)
            st.success(f"✅ Đã lưu file **{uploaded_file.name}** thành công!")

        st.markdown("##### 📚 Danh sách file đã lưu:")
        if st.session_state.uploaded_files_store[tab_key]:
            for f in st.session_state.uploaded_files_store[tab_key]:
                st.info(f"📄 **{f['name']}** ({f['size']} KB) - *{f['user']}* [{f['time']}]")
        else:
            st.write("_Chưa có tài liệu nào._")

    with col_down:
        st.markdown("##### 📥 Download biểu mẫu/tài liệu về máy")
        sample_text = f"TÀI LIỆU TIU CHUẨN MPM20 - PHÂN MỤC {tab_name.upper()}".encode("utf-8")
        st.download_button(
            label=f"📥 Tải tài liệu mẫu {tab_name} (TXT/PDF)",
            data=sample_text,
            file_name=f"Tai_lieu_{tab_key}_MPM20.txt",
            mime="text/plain",
            key=f"dl_{tab_key}"
        )
        
        # Tạo thêm file Excel mẫu phụ trợ download
        df_sample = pd.DataFrame({"STT": [1, 2], "Nội dung": [f"Mẫu dữ liệu 1 - {tab_name}", f"Mẫu dữ liệu 2 - {tab_name}"]})
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as writer:
            df_sample.to_excel(writer, index=False, sheet_name='Sheet1')
        st.download_button(
            label=f"📊 Tải Biểu mẫu Excel {tab_name}",
            data=buf.getvalue(),
            file_name=f"Bieu_mau_{tab_key}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"dl_excel_{tab_key}"
        )

# ==========================================
# ĐIỀU HƯỚNG NHÁNH CHÍNH
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
        
        # Khu vực điều khiển Cuộc gọi nhóm
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
        
        # Khung chat hiển thị sát nhau
        with st.container():
            st.markdown('<div class="chat-box">', unsafe_allow_html=True)
            if st.session_state.discussions:
                for item in st.session_state.discussions:
                    st.markdown(f"💬 **{item['user']}** <span style='color: gray; font-size: 0.8rem;'>({item['time']})</span>:<br>{item['content']}", unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 5px 0; border-color: #30363d;'>", unsafe_allow_html=True)
            else:
                st.write("_Chưa có nội dung trò chuyện nào._")
            st.markdown('</div>', unsafe_allow_html=True)

        # Form nhập tin nhắn chat
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
