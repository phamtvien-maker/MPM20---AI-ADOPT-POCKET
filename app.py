import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Cấu hình giao diện trang web (Layout rộng tối đa)
st.set_page_config(
    page_title="MPM20 - AI Adopt Pocket",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# GIAO DIỆN CSS TÙY CHỈNH (DARK THEME & TAB BUTTONS)
# ==========================================
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CƠ SỞ DỮ LIỆU THÀNH VIÊN (EMAIL & MẬT KHẨU)
# ==========================================
USER_CREDENTIALS = {
    "vuongtbichtuyen@gmail.com": "123456",
    "230110quynhanh@gmail.com": "123456",
}

# Khởi tạo bộ đếm truy cập toàn cục trong phiên chạy ứng dụng
if "active_users" not in st.session_state:
    st.session_state.active_users = set()

if "daily_visits" not in st.session_state:
    st.session_state.daily_visits = 0
    st.session_state.last_visit_date = datetime.now().date()

# Reset đếm lượt truy cập theo ngày mới
today = datetime.now().date()
if st.session_state.last_visit_date != today:
    st.session_state.daily_visits = 0
    st.session_state.last_visit_date = today

# Khởi tạo trạng thái phiên đăng nhập
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# ==========================================
# GIAO DIỆN ĐĂNG NHẬP (NẾU CHƯA LOGIN)
# ==========================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🚀 MPM20 – AI Adopt Pocket</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Hệ thống quản trị nội bộ chuyên sâu (Yêu cầu xác thực tài khoản)</p>", unsafe_allow_html=True)
        
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
# SAU KHI ĐĂNG NHẬP THÀNH CÔNG (DASHBOARD CHÍNH)
# ==========================================
user_email = st.session_state.user_email

# Đảm bảo ghi nhận vào danh sách active
st.session_state.active_users.add(user_email)

# Thanh Header trên cùng mô phỏng style bảng điều khiển mẫu
header_col1, header_col2, header_col3 = st.columns([3, 3, 2])
with header_col1:
    st.markdown(f"👤 **Thành viên:** `{user_email}`")
with header_col2:
    # Hiển thị số liệu thống kê truy cập trực quan
    st.markdown(f"🟢 **Online:** `{len(st.session_state.active_users)} người` | 📊 **Truy cập hôm nay:** `{st.session_state.daily_visits} lượt`")
with header_col3:
    if st.button("🚪 Đăng xuất", use_container_width=True):
        if user_email in st.session_state.active_users:
            st.session_state.active_users.remove(user_email)
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()

st.markdown("---")

# Tiêu đề ứng dụng
st.markdown("## ⚡ MPM20 - Pocket Dashboard")

# ==========================================
# ĐIỀU HƯỚNG NHÁNH CHÍNH DẠNG TAB BẤM NGANG
# ==========================================
main_tab1, main_tab2 = st.tabs([
    "📌 Nhánh 1: MPM (Quản trị & Tri thức)", 
    "🛠️ Nhánh 2: Ứng dụng & Thực thi (App/Code)"
])

# ==========================================
# NỘI DUNG NHÁNH 1
# ==========================================
with main_tab1:
    st.markdown("### 📌 MPM Core System & Tài liệu")
    
    # Các phân mục nhánh 1 bố trí thành các Tab ngang
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "📄 Doc (Tài liệu & Upload)", 
        "📝 Exams (Bài kiểm tra)", 
        "💬 Disc. (Thảo luận)", 
        "💡 Core Insight"
    ])
    
    with sub_tab1:
        st.subheader("Kho Tài liệu & Quản lý File Nội bộ")
        col_up, col_down = st.columns(2)
        
        with col_up:
            st.markdown("#### 📤 Tải tài liệu lên Web")
            uploaded_file = st.file_uploader(
                "Chọn file từ máy tính (PDF, Word, Excel, PNG...):", 
                type=["pdf", "docx", "xlsx", "pptx", "png", "jpg"],
                key="doc_upload_tab1"
            )
            if uploaded_file is not None:
                st.success(f"✅ Tệp do **{user_email}** tải lên: **{uploaded_file.name}** ({round(uploaded_file.size / 1024, 2)} KB)")

        with col_down:
            st.markdown("#### 📥 Tải tài liệu mẫu về máy")
            doc_sample_1 = "TÀI LIỆU QUY TRÌNH MPM20 SYSTEM - BẢN CHUẨN 2026"
            st.download_button(
                label="📄 Tải Quy trình MPM20 (TXT/PDF)",
                data=doc_sample_1,
                file_name="Quy_trinh_MPM20_Standard.txt",
                mime="text/plain",
                key="dl_doc_1"
            )
            
            df_template = pd.DataFrame({
                "STT": [1, 2, 3],
                "Tên tài liệu": ["Quy chuẩn thiết kế", "Hồ sơ nghiệm thu", "Báo cáo tuần"],
                "Trạng thái": ["Phê duyệt", "Đang xem xét", "Mới"]
            })
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_template.to_excel(writer, index=False, sheet_name='Danh_sach')
            
            st.download_button(
                label="📊 Tải Biểu mẫu Báo cáo (Excel)",
                data=buffer.getvalue(),
                file_name="Bieu_mau_MPM20.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_excel_1"
            )
            
    with sub_tab2:
        st.subheader("📝 Bài kiểm tra đánh giá năng lực")
        ans = st.radio("Đâu là tiêu chí quan trọng nhất trong quản lý chi phí (QS)?", (
            "Kiểm soát khối lượng & dự toán", 
            "Trang trí văn phòng", 
            "Thời gian họp"
        ), key="exam_radio")
        if st.button("Kiểm tra kết quả", key="btn_exam"):
            if "Kiểm soát" in ans:
                st.success(f"Chúc mừng tài khoản **{user_email}**, chính xác tuyệt đối!")
            else:
                st.error("Chưa chính xác, hãy xem lại tài liệu phần QS.")
                
    with sub_tab3:
        st.subheader("💬 Thảo luận nhóm nội bộ MPM")
        opinion = st.text_area("Ý kiến đóng góp / Ghi chú dự án:", key="opinion_box")
        if st.button("Gửi ý kiến", key="btn_opinion") and opinion:
            st.success(f"Ý kiến từ email **{user_email}** đã được ghi nhận vào hệ thống nội bộ.")
            
    with sub_tab4:
        st.subheader("💡 Core Insight (Góc nhìn cốt lõi)")
        st.info("Phân tích chiến lược tích hợp AI vào vận hành quản lý dự án, tối ưu hóa dòng tiền và tiến độ thi công hạ tầng đô thị.")

# ==========================================
# NỘI DUNG NHÁNH 2
# ==========================================
with main_tab2:
    st.markdown("### 🛠️ Ứng dụng, Mã nguồn & Giải pháp Thực thi")
    
    # Các phân mục nhánh 2 bố trí thành các Tab ngang
    sub_tab_2a, sub_tab_2b, sub_tab_2c, sub_tab_2d = st.tabs([
        "💻 App & Code", 
        "📊 Example Works", 
        "🏗️ PM Construction", 
        "📐 QS Construction"
    ])
    
    with sub_tab_2a:
        st.subheader("Ứng dụng & Mã nguồn Python tự động hóa")
        st.code("""
import pandas as pd

def process_qs_data(file_path):
    df = pd.read_excel(file_path)
    print("Xử lý dữ liệu QS thành công!")
    return df
        """, language="python")
        
    with sub_tab_2b:
        st.subheader("Example Works (Các công trình/case study mẫu)")
        st.write("- Mô phỏng quản lý hạ tầng Khu đô thị Vạn Phúc.\n- Tự động hóa báo cáo tuần qua Python & Excel.")
        
    with sub_tab_2c:
        st.subheader("PM Construction (Dành cho Quản lý dự án xây dựng)")
        st.write(f"Tài khoản đang thao tác: **{user_email}**")
        up_pm = st.file_uploader("📤 Upload Báo cáo tiến độ / Nhật ký thi công (PM):", key="pm_up_tab2")
        if up_pm:
            st.success(f"Đã ghi nhận tệp PM từ **{user_email}**: {up_pm.name}")
            
    with sub_tab_2d:
        st.subheader("QS Construction (Dành cho Kỹ sư Định lượng / Khối lượng)")
        st.markdown("#### Bảng tổng hợp khối lượng mẫu")
        qs_df = pd.DataFrame([
            {"STT": 1, "Hạng mục": "Bê tông móng", "Khối lượng": "1,200 m3", "Đơn giá (VND)": "1,500,000"},
            {"STT": 2, "Hạng mục": "Cốt thép D12-D28", "Khối lượng": "120 Tấn", "Đơn giá (VND)": "18,000,000"},
            {"STT": 3, "Hạng mục": "Cáp hạ thế XLPE/PVC", "Khối lượng": "450 m", "Đơn giá (VND)": "320,000"}
        ])
        st.dataframe(qs_df, use_container_width=True)
        
        up_qs = st.file_uploader("📤 Upload bảng tính dự toán / Bóc tách khối lượng (.xlsx):", key="qs_up_tab2", type=["xlsx", "xls"])
        if up_qs:
            st.success(f"Đã tải lên tệp QS từ email **{user_email}**: {up_qs.name}")
