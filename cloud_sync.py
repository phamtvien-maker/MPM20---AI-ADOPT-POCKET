import streamlit as st

try:
  import cloudinary.api
except ImportError:
  pass


def sync_files_from_cloudinary(tab_key="doc"):
  """Hàm tự động quét và kéo file riêng biệt theo từng tab từ Cloudinary về giao diện"""
  if "uploaded_files_store" not in st.session_state:
    st.session_state.uploaded_files_store = {}

  if tab_key not in st.session_state.uploaded_files_store:
    st.session_state.uploaded_files_store[tab_key] = []

  # Chỉ gọi API đồng bộ 1 lần duy nhất cho từng tab khi khởi động phiên làm việc
  if not st.session_state.get(f"synced_{tab_key}", False):
    try:
      all_resources = []
      folder_prefix = f"MPM20_AI_Storage/{tab_key}"

      # Quét tài liệu dạng raw (pdf, docx, xlsx, py...) thuộc riêng thư mục tab_key
      try:
        res_raw = cloudinary.api.resources(
            type="upload",
            resource_type="raw",
            prefix=folder_prefix,
            max_results=50,
        )
        all_resources.extend(res_raw.get("resources", []))
      except Exception:
        pass

      # Quét tài liệu dạng image (png, jpg...) thuộc riêng thư mục tab_key
      try:
        res_img = cloudinary.api.resources(
            type="upload",
            resource_type="image",
            prefix=folder_prefix,
            max_results=50,
        )
        all_resources.extend(res_img.get("resources", []))
      except Exception:
        pass

      st.session_state.uploaded_files_store[tab_key] = []

      for res in all_resources:
        public_id = res.get("public_id", "")
        # Lọc bỏ tiền tố thư mục để lấy đúng tên file gốc
        file_name = public_id.replace(f"{folder_prefix}/", "")
        file_url = res.get("secure_url")
        file_size = round(res.get("bytes", 0) / 1024, 2)
        file_format = res.get("format", "file")

        st.session_state.uploaded_files_store[tab_key].append({
            "name": file_name,
            "size": file_size,
            "user": "Cloud Sync",
            "time": res.get("created_at", "")[:19].replace("T", " "),
            "data": file_url,
            "type": file_format,
        })

      st.session_state[f"synced_{tab_key}"] = True
    except Exception as e:
      pass
