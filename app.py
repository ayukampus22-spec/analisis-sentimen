import streamlit as st
import os

st.set_page_config(
    page_title="SentimenAnalis - Analisis Sentimen Samsung Galaxy",
    page_icon="📱",
    layout="wide"
)

# Hide default Streamlit menu dan perbesar ukuran teks
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppHeader {display: none;}
    
    /* Perbesar semua teks */
    * {
        font-size: 16px !important;
    }
    
    /* Perbesar heading */
    h1 {
        font-size: 32px !important;
    }
    h2 {
        font-size: 28px !important;
    }
    h3 {
        font-size: 24px !important;
    }
    h4 {
        font-size: 20px !important;
    }
    h5 {
        font-size: 18px !important;
    }
    h6 {
        font-size: 16px !important;
    }
    
    /* Perbesar teks di sidebar */
    [data-testid="stSidebar"] * {
        font-size: 16px !important;
    }
    [data-testid="stSidebar"] h1 {
        font-size: 28px !important;
    }
    
    /* Perbesar teks di button */
    .stButton button {
        font-size: 16px !important;
    }
    
    /* Perbesar teks di input */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        font-size: 16px !important;
    }
    
    /* Perbesar teks di dataframe */
    .stDataFrame {
        font-size: 16px !important;
    }
    
    /* Perbesar teks di metric */
    .stMetric {
        font-size: 18px !important;
    }
    .stMetric label {
        font-size: 16px !important;
    }
    .stMetric .stMetric-value {
        font-size: 28px !important;
    }
    
    /* Perbesar teks di tabs */
    .stTabs [role="tab"] {
        font-size: 16px !important;
    }
    
    /* Perbesar teks di expander */
    .streamlit-expanderHeader {
        font-size: 18px !important;
    }
    
    /* Perbesar teks di markdown */
    .stMarkdown {
        font-size: 16px !important;
    }
    .stMarkdown p {
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    
    /* Perbesar teks di alert/notification */
    .stAlert {
        font-size: 16px !important;
    }
    .stAlert div {
        font-size: 16px !important;
    }
    
    /* Perbesar teks di caption */
    .stCaption {
        font-size: 14px !important;
    }
    
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    .stSidebarNav {
        display: none !important;
    }
    
    [data-testid="stSidebar"] {
        background: #f8fafc;
        border-right: 1px solid #eef2f6;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background: transparent;
        color: #475569;
        border: none;
        border-radius: 12px;
        text-align: left;
        padding: 0.8rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
        width: 100%;
        justify-content: flex-start;
        font-size: 16px !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: #e8f5ed;
        color: #2ecc71;
    }
    
    [data-testid="stSidebar"] .stButton button:active {
        background: #2ecc71;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi halaman aktif
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"

# ==================== SIDEBAR KUSTOM ====================
with st.sidebar:
    st.markdown("# 📱 SentimenAnalis")
    st.markdown("Analisis Sentimen Ulasan Produk Samsung Galaxy")
    st.markdown("---")
    
    # Menu navigasi
    menu_items = {
        "🏠 Beranda": "Beranda",
        "📁 Scraping Data": "Scraping",
        "📊 Kelola Data": "Kelola_Data",
        "⚙️ Proses Training": "Proses_Training",
        "📈 Hasil Analisis": "Hasil",
        "🎯 Prediksi": "Prediksi"
    }
    
    for label, page in menu_items.items():
        if st.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.current_page = page
            st.rerun()
    
    st.markdown("---")
    
 
    st.caption("© 2026 SentimenAnalis")

# ==================== LOAD PAGE ====================
def load_page(page_name):
    file_mapping = {
        "Beranda": "Beranda.py",
        "Scraping": "Scraping.py",
        "Kelola_Data": "Kelola_Data.py",
        "Proses_Training": "Proses_Training.py",
        "Hasil": "Hasil.py",
        "Prediksi": "Prediksi.py"
    }
    
    filename = file_mapping.get(page_name, f"{page_name}.py")
    page_path = os.path.join("pages", filename)
    
    if os.path.exists(page_path):
        with open(page_path, "r", encoding="utf-8") as f:
            code = f.read()
        exec(code, globals())
    else:
        st.error(f"Halaman {filename} tidak ditemukan di folder pages/")
        st.info("Pastikan file berada di folder 'pages'")

load_page(st.session_state.current_page)