import os
import google.generativeai as genai
import pandas as pd
import streamlit as st

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

# Kiểm tra xem có file nào vừa được bấm nút "Phân tích AI" từ trang chủ truyền sang không
selected_doc = st.session_state.get("selected_doc_for_ai", None)

source_options = [
    "Sử dụng toàn bộ kho tài liệu hệ thống MPM20",
    "Tải file mới trực tiếp cho AI",
]
if selected_doc:
  source_options.insert(
      0, f"📄 Tài liệu vừa chọn: {selected_doc.get('name')}"
  )

selected_source = st.sidebar.selectbox(
    "Chọn nguồn dữ liệu phân tích:", source_options
)

context_text = ""

if selected_doc and selected_source.startswith("📄 Tài liệu vừa chọn"):
  try:
    file_data = selected_doc.get("data")
    file_name = selected_doc.get("name", "")
    if file_name.endswith((".txt", ".py", ".csv", ".md", ".json", ".ppt")):
      context_text = file_data.decode("utf-8", errors="ignore")
    else:
      context_text = f"[Đã nạp file tài liệu: {file_name}]"
    st.sidebar.success(f"✅ Đã kết nối với file: {file_name}")
  except Exception as e:
    st.sidebar.error(f"Lỗi đọc file: {e}")

elif selected_source == "Tải file mới trực tiếp cho AI":
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
        context_text = f"[Đã nạp file đa phương tiện: {uploaded_ai_file.name}]"
        st.sidebar.success(f"✅ Đã nạp file {uploaded_ai_file.name} lên hệ thống")
    except Exception as e:
      st.sidebar.error(f"Lỗi đọc file: {e}")

else:
  st.sidebar.info(
      "💡 AI đang tự động quét và tổng hợp toàn bộ file từ mọi tab trong hệ"
      " thống MPM20."
  )
  all_files_content = []

  # Quét toàn bộ các kho lưu trữ file trong session_state của ứng dụng
  # (Hỗ trợ chia sẻ dữ liệu giữa app.py và các trang pages/)
  for tab_k in [
      "doc",
      "exams",
      "disc",
      "insight",
      "appcode",
      "example",
      "pm",
      "qs",
  ]:
    # Lấy dữ liệu trực tiếp từ session state hoặc khôi phục từ Cloudinary nếu cần
    files_list = st.session_state.get("uploaded_files_store", {}).get(tab_k, [])
    for f in files_list:
      if isinstance(f.get("data"), bytes):
        try:
          decoded_content = f["data"].decode("utf-8", errors="ignore")
          all_files_content.append(
              f"--- Kho: {tab_k.upper()} | File: {f['name']} ---\n"
              f"{decoded_content}"
          )
        except Exception:
          all_files_content.append(
              f"--- Kho: {tab_k.upper()} | File: {f['name']} (Định dạng nhị"
              " phân) ---"
          )

  if all_files_content:
    context_text = "\n\n".join(all_files_content)
    st.sidebar.success(
        f"✅ Đã tổng hợp thành công tài liệu từ hệ thống MPM20!"
    )
  else:
    st.sidebar.warning(
        "⚠️ Chưa tìm thấy file nào trong hệ thống. Vui lòng upload file ở trang"
        " chính."
    )

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
        Dưới đây là nguồn tài liệu được cung cấp từ hệ thống MPM20:
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
