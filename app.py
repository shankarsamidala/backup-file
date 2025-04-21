
import streamlit as st
import os
import shutil
import random
import string
from pathlib import Path

# Directories (these reset on Streamlit Cloud sessions)
UPLOAD_DIR = Path("uploads")
BACKUP_DIR = Path("backup")
UPLOAD_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

# Generate a secure recovery code
def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Page Config
st.set_page_config(page_title="🛡️ Secure Backup App", layout="centered")
st.title("🛡️ Secure Backup & Restore")
st.caption("Upload image → backup automatically → recover with secure code")

# -----------------------------
# Upload Section
# -----------------------------
st.header("📤 Upload Image")
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    file_name = uploaded_file.name
    upload_path = UPLOAD_DIR / file_name
    backup_path = BACKUP_DIR / file_name

    # Save to uploads and backup
    with open(upload_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    shutil.copy(upload_path, backup_path)

    # Create and store recovery code
    recovery_code = generate_code()
    st.session_state['recovery_map'] = st.session_state.get('recovery_map', {})
    st.session_state['recovery_map'][recovery_code] = file_name

    st.success("✅ File uploaded and backed up successfully!")
    st.info(f"🔐 Recovery Code: **{recovery_code}** (Save this code!)")

# -----------------------------
# Simulate Deletion (for demo)
# -----------------------------
st.header("🧪 Simulate File Deletion")
delete_file = st.text_input("Filename to delete from uploads/")
if st.button("🗑️ Delete File"):
    path = UPLOAD_DIR / delete_file
    if path.exists():
        path.unlink()
        st.warning(f"{delete_file} deleted from uploads/")
    else:
        st.error("File not found.")

# -----------------------------
# Recovery Section
# -----------------------------
st.header("♻️ Recover Deleted File")
recovery_input = st.text_input("Enter 8-digit Recovery Code")
if st.button("♻️ Recover"):
    recovery_map = st.session_state.get('recovery_map', {})
    if recovery_input in recovery_map:
        filename = recovery_map[recovery_input]
        src = BACKUP_DIR / filename
        dest = UPLOAD_DIR / filename
        if src.exists():
            shutil.copy(src, dest)
            st.success(f"✅ Recovered: {filename}")
        else:
            st.error("❌ Backup missing.")
    else:
        st.error("Invalid recovery code.")

# -----------------------------
# Uploaded File Viewer
# -----------------------------
st.header("📂 Uploaded Files")
uploaded_files = list(UPLOAD_DIR.glob("*"))
if uploaded_files:
    for f in uploaded_files:
        st.image(f, caption=f.name, width=200)
else:
    st.info("No images found.")
