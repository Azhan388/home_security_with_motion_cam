import streamlit as st
import os
import time
import shutil

st.set_page_config(page_title="Security Gallery", layout="wide")

st.title("🛡️ Home Security Gallery")

path = "captures"

# --- Bagian Sidebar untuk Kontrol ---
with st.sidebar:
    st.header("Pengaturan")
    if st.button("🗑️ Hapus Semua Foto", type="primary"):
        if os.path.exists(path):
            # Menghapus semua file di dalam folder
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    st.error(f"Gagal menghapus {filename}: {e}")
            st.warning("Semua foto telah dihapus!")
            time.sleep(1)
            st.rerun()

# --- Bagian Utama Galeri ---
if not os.path.exists(path):
    os.makedirs(path) # Buat folder jika belum ada
    st.info(f"Folder '{path}' telah dibuat. Menunggu kiriman foto...")
else:
    files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".jpg")]
    files.sort(key=os.path.getmtime, reverse=True) 
    
    if files:
        st.success(f"Ditemukan {len(files)} foto!")
        
        # Grid Galeri
        cols = st.columns(3) 
        for idx, file_path in enumerate(files):
            with cols[idx % 3]:
                st.image(file_path, caption=os.path.basename(file_path), use_container_width=True)
    else:
        st.info("Belum ada foto. Gerakkan tangan di depan sensor! 🖐️")

# Refresh otomatis
time.sleep(3)
st.rerun()