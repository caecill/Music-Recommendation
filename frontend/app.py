# ============================================================
# app.py — Entry point utama aplikasi (Streamlit)
# Berfungsi sebagai loader: membaca halaman HTML + menyisipkan
# konfigurasi (API URL, user_id) lalu merendernya di dalam iframe.
# ============================================================

import streamlit as st
import os

st.set_page_config(
    page_title="Music Recommendation | Premium Curator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",  # Sembunyikan sidebar Streamlit bawaan
)

API_BASE_URL = "http://127.0.0.1:8000"        # URL backend FastAPI

# Daftar halaman utama (membutuhkan sidebar)
pages = {
    "Home": "homepage.html",
    "Explore": "explore.html",
    "Listening History": "listening_history.html",
    "Catalog": "catalog.html",
    "Graph View": "graph_view.html",
}

# Daftar halaman auth (tanpa sidebar — fullscreen)
auth_pages = {
    "Login": "login.html",
    "Register": "register.html",
}

# Baca parameter query string: ?page=...&user_id=...
current_page = st.query_params.get("page", "Home")
user_id = st.query_params.get("user_id", "")

# ============ HALAMAN AUTH (Login/Register) ============
if current_page in auth_pages:
    html_file = auth_pages[current_page]
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Sisipkan API_BASE_URL sebagai global JS
    config_script = f"<script>window.__API_BASE_URL = '{API_BASE_URL}';</script>"
    content = content.replace("</head>", config_script + "</head>")

    # CSS: fullscreen, sembunyikan semua elemen Streamlit
    st.markdown("""
    <style>
        .stApp { background: #131313; }
        .stMainBlockContainer { padding: 0 !important; max-width: 100% !important; }
        .st-emotion-cache-uf99v8 { padding-top: 0 !important; }
        .stAppDeployButton, #MainMenu, header[data-testid="stHeader"],
        section[data-testid="stSidebar"] { display: none !important; }
        iframe { height: 100vh !important; width: 100vw !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)
    st.components.v1.html(content, height=1000)
    st.stop()  # Hentikan eksekusi di sini

# ============ HALAMAN UTAMA (dengan sidebar) ============

# Redirect ke Home jika halaman tidak dikenal
if current_page not in pages:
    current_page = "Home"
    st.query_params.page = current_page

# CSS: sembunyikan chrome Streamlit agar UI HTML murni terlihat
st.markdown("""
<style>
    .stMainBlockContainer { padding: 0 !important; max-width: 100% !important; }
    .st-emotion-cache-uf99v8 { padding-top: 0 !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    .stAppViewBlock .stMainBlockContainer { padding-left: 0 !important; }
    .stAppDeployButton { display: none !important; }
    #MainMenu { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    iframe { height: 100vh !important; }
</style>
""", unsafe_allow_html=True)

# Baca sidebar.js dan inline-kan ke dalam HTML
with open("sidebar.js", "r", encoding="utf-8") as f:
    sidebar_script = f.read()

# Baca halaman HTML yang diminta
html_file = pages[current_page]
with open(html_file, "r", encoding="utf-8") as f:
    html_content = f.read()

# Sisipkan konfigurasi API + user_id ke dalam <head>
config_script = f"""<script>
window.__API_BASE_URL = "{API_BASE_URL}";
window.__USER_ID = "{user_id}";
</script>"""

html_content = html_content.replace("</head>", config_script + "</head>")

# Ganti tag <script src="sidebar.js"> dengan script inline
html_content = html_content.replace(
    '<script src="sidebar.js"></script>',
    f"<script>{sidebar_script}</script>",
)

# Render HTML final di dalam iframe Streamlit
st.components.v1.html(html_content,)
