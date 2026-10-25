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
# GIAO DIỆN CSS 3D, ĐÓNG KHUNG VÀ MÀU SẮC TAB
# ==========================================
st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
    }
    /* Hiệu ứng 3D và đóng khung cho các khối container */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e293b;
        border-radius: 8px 8px 0px 0px;
        color: #ffffff;
        font-weight: bold;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #334155;
        transform: translateY(-2px);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
    }
    /* Khung chứa nội dung 3D */
    div.element-container {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CƠ SỞ DỮ LIỆU TÀI KHOẢN & LƯU TRỮ TẠM THỜI (SESSION STATE)
# ==========================================
USER_CREDENTIALS = {
    "vuongtbichtuyen@gmail.com": "123456",
    "230110quynhanh@gmail.com": "123456",
}

# Khởi tạo bộ nhớ lưu trữ lịch sử thảo luận và file riêng biệt cho từng tab
if "discussions" not in st.session_state:
    st.session_state.discussions = [] # Lưu danh sách thảo luận toàn cục hoặc theo chuyên đề

if "uploaded_files_store" not in st.session_state:
    st.session_state.uploaded_files_store = {
        "doc": [],
        "pm": [],
        "qs": []
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
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Hệ thống quản trị nội bộ 3D - Yêu cầu xác thực tài khoản</p>", unsafe_allow_html=True)
        
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

# Header hiển thị thông tin & Thống kê trực quan
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
st.markdown("## ⚡ MPM20 - 3D Dashboard Quản Trị Dự Án")

# ==========================================
# ĐIỀU HƯỚNG NHÁNH CHÍNH DẠNG TAB 3D NGANG
# ==========================================
main_tab1, main_tab2 = st.tabs([
    "📌 Nhánh 1: MPM (Quản trị & Tri thức)", 
    "🛠️ Nhánh 2: Ứng dụng & Thực thi (App/Code)"
])

# ==========================================
# NỘI DUNG NHÁNH 1
# ==========================================
with main_tab1:
    st.markdown("### 📌 MPM Core System")
    
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "📄 Doc (Tài liệu & Upload)", 
        "📝 Exams (Bài kiểm tra)", 
        "💬 Disc. (Thảo luận & Lịch sử)", 
        "💡 Core Insight"
    ])
    
    with sub_tab1:
        st.markdown("#### 📂 Kho Tài liệu & Quản lý File Nội bộ (Tab Doc)")
        col_up, col_down = st.columns(2)
        
        with col_up:
            st.markdown("##### 📤 Tải tài liệu lên Tab Doc")
            doc_file = st.file_uploader("Chọn file (PDF, Word, Excel...):", type=["pdf", "docx", "xlsx", "pptx", "png"], key="doc_up_file")
            if doc_file is not None:
                # Lưu vào kho file của Tab Doc
                file_info = {"name": doc_file.name, "size": round(doc_file.size / 1024, 2), "user": user_email, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                if file_info not in st.session_state.uploaded_files_store["doc"]:
                    st.session_state.uploaded_files_store["doc"].append(file_info)
                st.success(f"✅ Đã tải lên và lưu thành công file **{doc_file.name}** vào Tab Doc!")

            # Hiển thị danh sách file đã lưu trong Tab Doc
            st.markdown("##### 📚 Danh sách file đã lưu trong Tab Doc:")
            if st.session_state.uploaded_files_store["doc"]:
                for f in st.session_state.uploaded_files_store["doc"]:
                    st.info(f"📄 **{f['name']}** ({f['size']} KB) - Tải lên bởi *{f['user']}* vào lúc `{f['time']}`")
            else:
                st.write("_Chưa có tài liệu nào được tải lên._")

        with col_down:
            st.markdown("##### 📥 Tải tài liệu mẫu về máy")
            doc_sample_1 = "TÀI LIỆU QUY TRÌNH MPM20 SYSTEM - BẢN CHUẨN 2026"
            st.download_button(
                label="📄 Tải Quy trình MPM20 (TXT/PDF)",
                data=doc_sample_1,
                file_name="Quy_trinh_MPM20_Standard.txt",
                mime="text/plain",
                key="dl_doc_tab1"
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
                key="dl_excel_tab1"
            )
            
    with sub_tab2:
        st.markdown("#### 📝 Bài kiểm tra đánh giá năng lực")
        ans = st.radio("Đâu là tiêu chí quan trọng nhất trong quản lý chi phí (QS)?", (
            "Kiểm soát khối lượng & dự toán", 
            "Trang trí văn phòng", 
            "Thời gian họp"
        ), key="exam_r1")
        if st.button("Kiểm tra kết quả", key="btn_ex1"):
            if "Kiểm soát" in ans:
                st.success(f"Chúc mừng tài khoản **{user_email}**, chính xác tuyệt đối!")
            else:
                st.error("Chưa chính xác, hãy xem lại tài liệu phần QS.")
                
    with sub_tab3:
        st.markdown("#### 💬 Thảo luận nhóm nội보 & Lịch sử thời gian")
        
        # Form nhập nội dung thảo luận
        with st.form("discussion_form"):
            opinion = st.text_area("Nhập ý kiến đóng góp / Ghi chú dự án:")
            submit_disc = st.form_submit_button("Gửi ý kiến thảo luận")
            if submit_disc and opinion.strip():
                new_disc = {
                    "user": user_email,
                    "content": opinion.strip(),
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.discussions.insert(0, new_disc) # Đưa lên đầu
                st.success("✅ Ý kiến đã được lưu trữ vào hệ thống lịch sử!")

        st.markdown("---")
        st.markdown("##### 📜 Lịch sử nội dung thảo luận:")
        if st.session_state.discussions:
            for item in st.session_state.discussions:
                st.markdown(f"> 🕒 **{item['time']}** | 👤 **{item['user']}**:\n>\n> {item['content']}")
                st.markdown("---")
        else:
            st.write("_Chưa có ý kiến thảo luận nào được ghi nhận._")
            
    with sub_tab4:
        st.markdown("#### 💡 Core Insight (Góc nhìn cốt lõi)")
        st.info("Phân tích chiến lược tích hợp AI vào vận hành quản lý dự án, tối ưu hóa dòng tiền và tiến độ thi công hạ tầng đô thị.")

# ==========================================
# NỘI DUNG NHÁNH 2
# ==========================================
with main_tab2:
    st.markdown("### 🛠️ Ứng dụng & Giải pháp Thực thi")
    
    sub_tab_2a, sub_tab_2b, sub_tab_2c, sub_tab_2d = st.tabs([
        "💻 App & Code", 
        "📊 Example Works", 
        "🏗️ PM Construction", 
        "📐 QS Construction"
    ])
    
    with sub_tab_2a:
        st.markdown("#### 💻 Ứng dụng & Mã nguồn Python tự động hóa")
        st.code("""
import pandas as pd

def process_qs_data(file_path):
    df = pd.read_excel(file_path)
    print("Xử lý dữ liệu QS thành công!")
    return df
        """, language="python")
        
    with sub_tab_2b:
        st.markdown("#### 📊 Example Works (Case study mẫu)")
        st.write("- Mô phỏng quản lý hạ tầng Khu đô thị Vạn Phúc.\n- Tự động hóa báo cáo tuần qua Python & Excel.")
        
    with sub_tab_2c:
        st.markdown("#### 🏗️ PM Construction (Quản lý dự án)")
        col_pm1, col_pm2 = st.columns(2)
        
        with col_pm1:
            st.markdown("##### 📤 Upload Báo cáo tiến độ (PM)")
            pm_file = st.file_uploader("Tải lên tệp PM (.pdf, .docx, .xlsx):", key="pm_up_file", type=["pdf", "docx", "xlsx"])
            if pm_file:
                file_info = {"name": pm_file.name, "size": round(pm_file.size / 1024, 2), "user": user_email, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                if file_info not in st.session_state.uploaded_files_store["pm"]:
                    st.session_state.uploaded_files_store["pm"].append(file_info)
                st.success(f"✅ Đã lưu file PM: **{pm_file.name}**")

            st.markdown("##### 📁 Kho file PM đã lưu:")
            if st.session_state.uploaded_files_store["pm"]:
                for f in st.session_state.uploaded_files_store["pm"]:
                    st.info(f"🏗️ **{f['name']}** ({f['size']} KB) - *{f['user']}* [{f['time']}]")
            else:
                st.write("_Chưa có tài liệu PM nào._")

        with col_pm2:
            st.markdown("##### 📥 Tải biểu mẫu PM về máy")
            st.download_button(
                label="📥 Tải Nhật ký thi công mẫu (Excel)",
                data=b"Nhat ky thi công mau MPM20",
                file_name="Nhat_ky_thi_cong_PM.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_pm_sample"
            )
            
    with sub_tab_2d:
        st.markdown("#### 📐 QS Construction (Kỹ sư Định lượng / Khối lượng)")
        
        col_qs1, col_qs2 = st.columns(2)
        with col_qs1:
            st.markdown("##### Bảng tổng hợp khối lượng mẫu")
            qs_df = pd.DataFrame([
                {"STT": 1, "Hạng mục": "Bê tông móng", "Khối lượng": "1,200 m3", "Đơn giá (VND)": "1,500,000"},
                {"STT": 2, "Hạng mục": "Cốt thép D12-D28", "Khối lượng": "120 Tấn", "Đơn giá (VND)": "18,000,000"},
                {"STT": 3, "Hạng mục": "Cáp hạ thế XLPE/PVC", "Khối lượng": "450 m", "Đơn giá (VND)": "320,000"}
            ])
            st.dataframe(qs_df, use_container_width=True)
            
            # Nút tải bảng khối lượng mẫu về máy
            buf_qs = io.BytesIO()
            with pd.ExcelWriter(buf_qs, engine='openpyxl') as writer:
                qs_df.to_excel(writer, index=False, sheet_name='Khoi_luong_QS')
            st.download_button(
                label="📊 Tải Bảng khối lượng QS (Excel)",
                data=buf_qs.getvalue(),
                file_name="Bang_Khoi_Luong_QS.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_qs_table"
            )

        with col_qs2:
            st.markdown("##### 📤 Upload bảng tính dự toán QS")
            qs_file = st.file_uploader("Tải lên file dự toán (.xlsx, .xls):", key="qs_up_file", type=["xlsx", "xls"])
            if qs_file:
                file_info = {"name": qs_file.name, "size": round(qs_file.size / 1024, 2), "user": user_email, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                if file_info not in st.session_state.uploaded_files_store["qs"]:
                    st.session_state.uploaded_files_store["qs"].append(file_info)
                st.success(f"✅ Đã lưu file QS: **{qs_file.name}**")

            st.markdown("##### 📁 Kho file QS đã lưu:")
            if st.session_state.uploaded_files_store["qs"]:
                for f in st.session_state.uploaded_files_store["qs"]:
                    st.info(f"📐 **{f['name']}** ({f['size']} KB) - *{f['user']}* [{f['time']}]")
            else:
                st.write("_Chưa có tài liệu QS nào._")
