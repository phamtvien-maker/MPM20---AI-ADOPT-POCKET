import streamlit as st
try:
    import cloudinary.api
except ImportError:
    pass

def sync_files_from_cloudinary(tab_key="doc"):
    """Hàm tự động quét và kéo toàn bộ file từ thư mục Cloudinary về giao diện"""
    if "uploaded_files_store" not in st.session_state:
        st.session_state.uploaded_files_store = {}
        
    if tab_key not in st.session_state.uploaded_files_store:
        st.session_state.uploaded_files_store[tab_key] = []
        
    # Chỉ gọi API đồng bộ 1 lần duy nhất khi khởi động phiên làm việc
    if not st.session_state.get(f"synced_{tab_key}", False):
        try:
            # Lấy danh sách tài liệu từ Cloudinary (hỗ trợ cả file raw và image)
            result = cloudinary.api.resources(
                type="upload", 
                prefix="MPM20_AI_Storage", 
                max_results=50
            )
            resources = result.get("resources", [])
            st.session_state.uploaded_files_store[tab_key] = []
            
            for res in resources:
                public_id = res.get("public_id", "")
                file_name = public_id.replace("MPM20_AI_Storage/", "")
                file_url = res.get("secure_url")
                file_size = round(res.get("bytes", 0) / 1024, 2)
                file_format = res.get("format", "file")
                
                st.session_state.uploaded_files_store[tab_key].append({
                    "name": file_name,
                    "size": file_size,
                    "user": "Cloud Sync",
                    "time": res.get("created_at", "")[:19].replace("T", " "),
                    "data": file_url,
                    "type": file_format
                })
            st.session_state[f"synced_{tab_key}"] = True
        except Exception as e:
            pass
