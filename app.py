import streamlit as st
import pandas as pd
import io

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="MPM20 - AI Adopt Pocket",
    page_icon="🚀",
    layout="wide"
)

# Tiêu đề chính của Website
st.title("🚀 MPM20 – AI Adopt Pocket")
st.caption("Nền tảng quản trị dự án, lưu trữ tài liệu & ứng dụng AI chuyên sâu (Tối đa 10 thành viên)")

# Thanh điều hướng phân chia theo 2 nhánh chính
branch = st.sidebar.radio("📂 Chọn nhánh chính:", [
    "📌 Nhánh 1: MPM (Quản trị & Tri thức)", 
    "🛠️ Nhánh 2: Ứng dụng & Thực thi (App/Code)"
])

# ==========================================
# NHÁNH 1: MPM (Doc, Exams, Disc., Core Insight)
# ==========================================
if branch == "📌 Nhánh 1: MPM (Quản trị & Tri thức)":
    st.header("📌 Nhánh 1: MPM Core System")
    
    sub_menu_1 = st.selectbox("Chọn danh mục nhánh 1:", [
        "Doc (Tài liệu & Upload)", 
        "Exams (Bài kiểm tra)", 
        "Disc. (Thảo luận)", 
        "Core Insight"
    ])
    
    if sub_menu_1 == "Doc (Tài liệu & Upload)":
        st.subheader("📄 Kho Tài liệu & Quản lý File Nội bộ")
        st.write("Nơi lưu trữ, chia sẻ và tải lên/tải về các tài liệu chuẩn của hệ thống MPM20.")
        
        col_up, col_down = st.columns(2)
        
        # --- TÍNH NĂNG UPLOAD ---
        with col_up:
            st.markdown("### 📤 Tải tài liệu mới lên Web")
            uploaded_file = st.file_uploader(
                "Chọn file từ máy tính (PDF, Word, Excel, PNG...):", 
                type=["pdf", "docx", "xlsx", "pptx", "png", "jpg"],
                key="doc_upload"
            )
            if uploaded_file is not None:
                st.success(f"✅ Đã tải lên thành công file: **{uploaded_file.name}**")
                st.info(f"Dung lượng: {round(uploaded_file.size / 1024, 2)} KB")

        # --- TÍNH NĂNG DOWNLOAD ---
        with col_down:
            st.markdown("### 📥 Tải tài liệu mẫu về máy")
            st.write("Danh sách tài liệu tiêu chuẩn có sẵn:")
            
            doc_sample_1 = "TÀI LIỆU QUY TRÌNH MPM20 SYSTEM - BẢN CHUẨN 2026"
            st.download_button(
                label="📄 Tải Quy trình MPM20 (TXT/PDF)",
                data=doc_sample_1,
                file_name="Quy_trinh_MPM20_Standard.txt",
                mime="text/plain"
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
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
    elif sub_menu_1 == "Exams (Bài kiểm tra)":
        st.subheader("📝 Bài kiểm tra đánh giá năng lực")
        ans = st.radio("Đâu là tiêu chí quan trọng nhất trong quản lý chi phí (QS)?", (
            "Kiểm soát khối lượng & dự toán", 
            "Trang trí văn phòng", 
            "Thời gian họp"
        ))
        if st.button("Kiểm tra kết quả"):
            if "Kiểm soát" in ans:
                st.success("Chính xác tuyệt đối!")
            else:
                st.error("Chưa chính xác, hãy xem lại tài liệu phần QS.")
                
    elif sub_menu_1 == "Disc. (Thảo luận)":
        st.subheader("💬 Thảo luận nhóm MPM (Tối đa 10 thành viên)")
        name = st.text_input("Tên thành viên:")
        opinion = st.text_area("Ý kiến đóng góp / Ghi chú dự án:")
        if st.button("Gửi ý kiến") and name and opinion:
            st.success(f"Cảm ơn **{name}**, ý kiến đã được ghi nhận trên hệ thống nội bộ.")
            
    elif sub_menu_1 == "Core Insight":
        st.subheader("💡 Core Insight (Góc nhìn cốt lõi)")
        st.info("Phân tích chiến lược tích hợp AI vào vận hành quản lý dự án, tối ưu hóa dòng tiền và tiến độ thi công hạ tầng đô thị.")

# ==========================================
# NHÁNH 2: App, Code, Example Works -> PM Constr & QS Constr
# ==========================================
else:
    st.header("🛠️ Nhánh 2: Ứng dụng, Mã nguồn & Giải pháp Thực thi")
    
    sub_menu_2 = st.selectbox("Chọn danh mục nhánh 2:", [
        "App & Code", 
        "Example Works (Ví dụ thực tế)", 
        "PM Construction (Quản lý dự án)", 
        "QS Construction (Định lượng & Dự toán)"
    ])
    
    if sub_menu_2 == "App & Code":
        st.subheader("💻 Ứng dụng & Mã nguồn Python tự động hóa")
        st.write("Các đoạn mã tự động bóc tách khối lượng và phân tích dự án:")
        st.code("""
import pandas as pd

def process_qs_data(file_path):
    df = pd.read_excel(file_path)
    print("Xử lý dữ liệu QS thành công!")
    return df
        """, language="python")
        
    elif sub_menu_2 == "Example Works (Ví dụ thực tế)":
        st.subheader("📊 Example Works (Các công trình/case study mẫu)")
        st.write("- Mô phỏng quản lý hạ tầng Khu đô thị Vạn Phúc.\n- Tự động hóa báo cáo tuần qua Python & Excel.")
        
    elif sub_menu_2 == "PM Construction (Quản lý dự án)":
        st.subheader("🏗️ PM Construction (Dành cho Quản lý dự án xây dựng)")
        st.write("Giải pháp điều phối thi công, quản lý nhà thầu và hồ sơ bản vẽ.")
        
        up_pm = st.file_uploader("📤 Upload Báo cáo tiến độ / Nhật ký thi công (PM):", key="pm_up")
        if up_pm:
            st.success(f"Đã ghi nhận tệp PM: {up_pm.name}")
        
    elif sub_menu_2 == "QS Construction (Định lượng & Dự toán)":
        st.subheader("📐 QS Construction (Dành cho Kỹ sư Định lượng / Khối lượng)")
        st.write("Công cụ kiểm soát khối lượng phát sinh, thanh quyết toán và dự toán chi phí.")
        
        st.markdown("#### Bảng tổng hợp khối lượng mẫu")
        qs_df = pd.DataFrame([
            {"STT": 1, "Hạng mục": "Bê tông móng", "Khối lượng": "1,200 m3", "Đơn giá (VND)": "1,500,000"},
            {"STT": 2, "Hạng mục": "Cốt thép D12-D28", "Khối lượng": "120 Tấn", "Đơn giá (VND)": "18,000,000"},
            {"STT": 3, "Hạng mục": "Cáp hạ thế XLPE/PVC", "Khối lượng": "450 m", "Đơn giá (VND)": "320,000"}
        ])
        st.dataframe(qs_df, use_container_width=True)
        
        up_qs = st.file_uploader("📤 Upload bảng tính dự toán / Bóc tách khối lượng (.xlsx):", key="qs_up", type=["xlsx", "xls"])
        if up_qs:
            st.success(f"Đã tải lên tệp dữ liệu QS: {up_qs.name}")
