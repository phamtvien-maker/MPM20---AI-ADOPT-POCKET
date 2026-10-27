import os
import google.generativeai as genai
import pandas as pd
import streamlit as st

# Cấu hình giao diện trang
st.set_page_config(
    page_title="MPM20 - Notebook AI Assistant", page_icon="🤖", layout="wide"
)

st.markdown("## 🤖 Trợ lý AI Phân Tích Tài Liệu (Phong cách NotebookLM)")
st.markdown(
    "Trợ lý này có thể đọc hiểu, tóm tắt và trả lời mọi câu hỏi dựa trên các tài"
    " liệu dự án MPM20 của bạn."
)
st.markdown("---")

# Kết nối Gemini API từ st.secrets (đã cấu hình trên Streamlit Cloud)
if "GEMINI_API_KEY" in st.secrets:
  genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
  st.error("❌ Vui lòng cấu hình GEMINI_API_KEY trong Secrets storage của Streamlit!")
  st.stop()

# Khởi tạo mô hình Gemini thông minh
model = genai.GenerativeModel("gemini-1.5-pro")

# Khởi tạo lịch sử chat
if "notebook_chat_history" not in st.session_state:
  st.session_state.notebook_chat_history = []

# Nguồn dữ liệu cho AI ở Sidebar
st.sidebar.markdown("### 📚 Nguồn tài liệu cho AI")
selected_source = st.sidebar.selectbox(
    "Chọn nguồn dữ liệu phân tích:",
    ["Tải file mới trực tiếp cho AI", "Sử dụng kho tài liệu hệ thống MPM20"],
)

context_text = ""

if selected_source == "Tải file mới trực tiếp cho AI":
  uploaded_ai_file = st.sidebar.file_uploader(
      "Tải tài liệu (PDF, TXT, CSV, Python...)",
      type=["pdf", "txt", "csv", "py", "md"],
  )
  if uploaded_ai_file is not None:
    try:
      if uploaded_ai_file.type == "text/plain" or uploaded_ai_file.name.endswith(
          (".py", ".txt", ".md", ".csv")
      ):
        context_text = uploaded_ai_file.getvalue().decode("utf-8")
        st.sidebar.success(f"✅ Đã đọc xong file {uploaded_ai_file.name}")
      else:
        with open(uploaded_ai_file.name, "wb") as f:
          f.write(uploaded_ai_file.getbuffer())
        g_file = genai.upload_file(uploaded_ai_file.name)
        context_text = f"[Đã nạp file đa phương tiện: {uploaded_ai_file.name}]"
        st.sidebar.success(f"✅ Đã nạp file {uploaded_ai_file.name} lên hệ thống")
    except Exception as e:
      st.sidebar.error(f"Lỗi đọc file: {e}")

else:
  st.sidebar.info(
      "💡 AI đang tự động tổng hợp thông tin từ các kho lưu trữ trong ứng dụng"
      " MPM20."
  )
  if "uploaded_files_store" in st.session_state:
    all_files_content = []
    for tab_k, files in st.session_state.uploaded_files_store.items():
      for f in files:
        if isinstance(f.get("data"), bytes):
          try:
            all_files_content.append(
                f"--- File: {f['name']} (Tab: {tab_k}) ---\n"
                f"{f['data'].decode('utf-8', errors='ignore')}"
            )
          except Exception:
            pass
    context_text = "\n\n".join(all_files_content)

# Hiển thị lịch sử trò chuyện
for message in st.session_state.notebook_chat_history:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Khung nhập câu hỏi
if user_prompt := st.chat_input(
    "Nhập yêu cầu phân tích (Ví dụ: Tóm tắt điểm chính, tính toán chi phí...):"
):
  st.session_state.notebook_chat_history.append(
      {"role": "user", "content": user_prompt}
  )
  with st.chat_message("user"):
    st.markdown(user_prompt)

  with st.chat_message("assistant"):
    with st.spinner("🤖 Trợ lý AI đang nghiên cứu tài liệu..."):
      try:
        full_prompt = f"""
                Bạn là một Trợ lý AI chuyên gia quản lý dự án (PM) và quản lý chi phí (QS) cao cấp, thông minh giống như Google NotebookLM.
                Dưới đây là nguồn tài liệu được cung cấp:
                ====================
                {context_text}
                ====================
                
                Dựa vào nguồn tài liệu trên, hãy trả lời câu hỏi hoặc thực hiện yêu cầu sau một cách chính xác, chuyên nghiệp và có cấu trúc rõ ràng (dùng Markdown, bullet points):
                Yêu cầu: {user_prompt}
                """

        response = model.generate_content(full_prompt)
        ai_response = response.text

        st.markdown(ai_response)
        st.session_state.notebook_chat_history.append(
            {"role": "assistant", "content": ai_response}
        )
      except Exception as e:
        error_msg = f"❌ Đã xảy ra lỗi khi gọi Gemini API: {e}"
        st.error(error_msg)
        st.session_state.notebook_chat_history.append(
            {"role": "assistant", "content": error_msg}
        )
