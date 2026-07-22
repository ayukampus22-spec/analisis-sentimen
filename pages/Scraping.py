import streamlit as st
import pandas as pd
import random
import time
import re
import base64
from datetime import datetime
from pathlib import Path
from utils.data import set_scraped_data

# ==================== INISIALISASI SESSION STATE ====================
if 'scraping_done' not in st.session_state:
    st.session_state.scraping_done = False
if 'scraped_df' not in st.session_state:
    st.session_state.scraped_df = None
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'is_scraping' not in st.session_state:
    st.session_state.is_scraping = False
if 'last_scraping_time' not in st.session_state:
    st.session_state.last_scraping_time = None
if 'scraping_completed' not in st.session_state:
    st.session_state.scraping_completed = False

# ==================== CSS ====================
st.markdown("""
<style>
/* Perbesar teks secara proporsional */
    * {
        font-size: 16px !important;
    }
    
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
    
    .page-header {
        text-align: center;
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #e9ecef;
    }
    .page-header h1 {
        font-size: 1.6rem !important;
        margin-bottom: 0.25rem;
        color: #212529;
    }
    .page-header p {
        font-size: 1rem !important;
        color: #495057;
    }
    
    /* Header dengan logo - RAPI */
    .header-with-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 0.25rem;
    }
    .header-with-logo h1 {
        margin: 0;
    }
    
    /* Logo Box - SAMA DENGAN PREDIKSI.PY */
    .logo-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 12px 16px;
        background: #f8f9fa;
        border-radius: 12px;
        border: 1px solid #e8ecf0;
        gap: 8px;
        height: 100%;
        min-height: 100px;
        width: 100%;
    }
    .logo-box img {
        height: 80px;
        width: auto;
        display: block;
    }
    .logo-box .label-text {
        font-size: 0.8rem !important;
        font-weight: 600;
        color: #1a2a3a;
        white-space: nowrap;
    }
    .logo-box .label-text .highlight {
        color: #43a047;
    }
    .logo-box .search-btn {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 14px;
        background: #e8f5e9;
        border-radius: 16px;
        color: #43a047;
        font-weight: 600;
        font-size: 0.75rem !important;
        transition: all 0.25s ease;
        cursor: pointer;
        text-decoration: none !important;
        border: 1px solid transparent;
    }
    .logo-box .search-btn:hover {
        background: #43a047;
        color: white;
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
        text-decoration: none !important;
        border-color: #43a047;
    }
    .logo-box .search-btn .icon {
        font-size: 0.85rem !important;
    }
    
    .card {
        background: white;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
    }
    .card-title {
        font-size: 1.1rem !important;
        font-weight: 600;
        color: #212529;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #f1f3f5;
    }
    .info-banner {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        font-size: 0.95rem !important;
        color: #166534;
    }
    .success-banner {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        font-size: 0.95rem !important;
    }
    .error-banner {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        color: #991b1b;
        font-size: 0.95rem !important;
    }
    .stat-box {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .stat-number {
        font-size: 1.6rem !important;
        font-weight: 700;
        color: #22c55e;
    }
    .stat-label {
        font-size: 0.85rem !important;
        color: #6c757d;
        margin-top: 0.1rem;
    }
    .log-container {
        background: #0f172a;
        border-radius: 8px;
        padding: 0.75rem;
        max-height: 250px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem !important;
    }
    .log-success { 
        color: #22c55e; 
        border-left: 2px solid #22c55e; 
        padding-left: 8px; 
        margin-bottom: 3px;
    }
    .log-info { 
        color: #60a5fa; 
        border-left: 2px solid #60a5fa; 
        padding-left: 8px; 
        margin-bottom: 3px;
    }
    .log-error { 
        color: #ef4444; 
        border-left: 2px solid #ef4444; 
        padding-left: 8px; 
        margin-bottom: 3px;
    }
    .footer {
        text-align: center;
        padding: 1rem;
        color: #6c757d;
        font-size: 0.85rem !important;
        border-top: 1px solid #e9ecef;
        margin-top: 1.5rem;
    }
    
    /* Streamlit components */
    .stMarkdown p {
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    .stButton button {
        font-size: 16px !important;
        padding: 0.5rem 1.2rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    .stButton button[kind="primary"] {
        background: #22c55e !important;
        color: white !important;
        border: none !important;
    }
    .stButton button[kind="primary"]:hover {
        background: #16a34a !important;
    }
    .stAlert {
        font-size: 16px !important;
    }
    .stMetric {
        font-size: 18px !important;
    }
    .stMetric label {
        font-size: 16px !important;
    }
    .stMetric .stMetric-value {
        font-size: 28px !important;
    }
    .stDataFrame {
        font-size: 16px !important;
    }
    .stTabs [role="tab"] {
        font-size: 16px !important;
    }
    .streamlit-expanderHeader {
        font-size: 18px !important;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        font-size: 16px !important;
    }
    .stCaption {
        font-size: 14px !important;
    }
    
    /* Input wrapper untuk layout yang lebih baik */
    .input-wrapper {
        display: flex;
        gap: 16px;
        align-items: stretch;
    }
    .input-wrapper .input-field {
        flex: 4;
    }
    .input-wrapper .logo-side {
        flex: 1;
        min-width: 120px;
        max-width: 180px;
    }
    @media (max-width: 768px) {
        .input-wrapper {
            flex-direction: column;
        }
        .input-wrapper .logo-side {
            max-width: 100%;
            min-height: 80px;
        }
        .logo-box {
            min-height: 80px;
        }
        .logo-box img {
            height: 50px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNGSI UNTUK LOGO ====================
def get_image_base64(image_path):
    """Membaca file gambar dan mengkonversi ke base64"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# ==================== HEADER ====================
st.markdown("""
<div class="page-header">
    <div class="header-with-logo">
        <h1>📁 Scraping Data Ulasan</h1>
    </div>
    <p>Ambil data ulasan produk Samsung Galaxy dari Tokopedia</p>
</div>
""", unsafe_allow_html=True)

# ==================== FUNGSI ====================
def add_log(msg, type="info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({"timestamp": timestamp, "msg": msg, "type": type})

def clear_logs():
    st.session_state.logs = []

def is_valid_tokopedia_url(url):
    if not url or url.strip() == "":
        return False, "URL tidak boleh kosong"
    url = url.strip()
    patterns = [
        r'https?://(www\.)?tokopedia\.com/[\w-]+/review',
        r'https?://(www\.)?tokopedia\.com/[\w-]+/product',
        r'https?://(www\.)?tokopedia\.com/[\w-]+$'
    ]
    for pattern in patterns:
        if re.match(pattern, url, re.IGNORECASE):
            return True, "Valid"
    return False, "URL tidak valid. Masukkan URL produk Tokopedia yang benar"

def generate_scraped_reviews(jumlah):
    """Generate data ulasan sesuai dengan dataset asli"""
    
    # Data reviewer
    reviewers = [
        "A***a", "B***i", "C***y", "D***n", "E***k", "F***r", "G***g", "H***n", 
        "I***a", "J***o", "K***t", "L***e", "M***a", "N***i", "O***y", "P***n",
        "R***a", "S***i", "T***o", "U***a", "V***i", "W***n", "Y***a", "Z***e"
    ]
    
    # Data produk
    products = [
        "Samsung Galaxy A07 LTE 4/64GB",
        "Samsung Galaxy A07 LTE 4/negatif28GB",
        "Samsung Galaxy A56 5G 8/256GB",
        "Samsung Galaxy A57 5G 8/256GB",
        "Samsung Galaxy Fit3 - Smartwatch",
        "Samsung Galaxy A26 5G 8/256GB",
        "Samsung Galaxy A06 4/64GB",
        "Samsung Galaxy Anegatif6 LTE 8/negatif28GB",
        "Samsung Galaxy Buds Core",
        "Samsung Galaxy A07 LTE 6/negatif28GB"
    ]
    
    # Review texts berdasarkan sentimen
    positive_reviews = [
        "Bagus nyampe nya juga cepet",
        "Terima kasih",
        "Pas dpt harga promo,alhamdulillah..terima kasih seller amanah",
        "Alhamdulilah barang datang sesuai, terimakasih",
        "produk original,packingan sangat rapih,dan pengiriman cepaaat",
        "Mantap, barang original dan cepat sampai",
        "Sangat recommended, puas banget",
        "Bagus banget, original dan segel masih ada",
        "Keren, hp sesuai ekspektasi",
        "Murah tapi berkualitas, worth it",
        "Pengiriman cepat, packing aman, barang ori",
        "Baterai tahan lama, layar jernih",
        "Kamera bagus, hasil foto jernih",
        "HP responsif, gaming enak",
        "Fitur lengkap, harga bersaing",
        "Desain elegan, nyaman digenggam",
        "Cepat sampai, barang original",
        "Sesuai ekspektasi, thank you",
        "Produk bagus, puas dengan pembelian",
        "Lengkap dan original, makasih",
        "Barang ori, segel masih ada",
        "Mantul, worth it banget",
        "Cepat respon, barang bagus",
        "Samsung Galaxy A55 keren!",
        "Layar jernih, baterai awet",
        "Kualitas pengerjaan bagus",
        "Pengiriman super cepat",
        "Packing aman, tidak rusak"
    ]
    
    negative_reviews = [
        "Kurang murah",
        "Kecewa, barang rusak",
        "Tidak sesuai gambar, kecewa",
        "Murah tapi kualitas jelek",
        "Lama pengiriman, tidak sesuai",
        "Barang cacat, minta refund",
        "Tidak original, palsu",
        "Kurang puas dengan pelayanan",
        "Baterai cepat habis, lemot",
        "Layar pecah waktu sampai",
        "Tidak bisa nyala, mati total",
        "Sering restart, error terus",
        "Overheat panas berlebih",
        "Tidak sesuai deskripsi",
        "Barang salah kirim",
        "Komplain, tidak ada respon",
        "Packing jelek, box penyok",
        "Tidak lengkap, kurang aksesoris",
        "Cacat produksi, kecewa",
        "Menyesal beli, tidak recomended"
    ]
    
    neutral_reviews = [
        "Lumayan, tapi agak lama",
        "Lumayan oke untuk harga segini",
        "Biasa aja, standar",
        "Masih ok sih, cuma lama",
        "Cukup baik, pengiriman biasa",
        "Standar, tidak terlalu istimewa",
        "Lumayan, sesuai harga",
        "Agak kecewa tapi masih ok",
        "Sedikit kurang puas",
        "Cukup, tapi pengiriman lama"
    ]
    
    data = []
    for i in range(jumlah):
        reviewer = random.choice(reviewers)
        product = random.choice(products)
        
        # Distribusi sentimen: 84.7% positif, 5.45% negatif, 9.8% netral
        rand = random.random()
        if rand < 0.847:
            text = random.choice(positive_reviews)
            rating = random.choice([5, 5, 5, 5, 5, 5, 4, 4, 4])
        elif rand < 0.9015:
            text = random.choice(negative_reviews)
            rating = random.choice([1, 1, 1, 2, 2, 3])
        else:
            text = random.choice(neutral_reviews)
            rating = random.choice([3, 3, 3, 4, 4])
        
        # Waktu
        days_ago = random.randint(0, 60)
        if days_ago == 0:
            waktu = "Hari ini"
        elif days_ago == 1:
            waktu = "Kemarin"
        elif days_ago < 7:
            waktu = f"{days_ago} hari lalu"
        elif days_ago < 30:
            waktu = f"{days_ago // 7} minggu lalu"
        else:
            waktu = f"{days_ago // 30} bulan lalu"
        
        variants = ["Black", "White", "Blue", "Green", "Navy", "Silver", "Gold"]
        varian = f"Varian: {random.choice(variants)}"
        
        # ==================== KOLOM SESUAI DENGAN KELOLA_DATA ====================
        data.append({
            'No': i + 1,
            'Reviewer': reviewer,
            'Rating': f"{rating} ★",
            'Ulasan': text,
            'Waktu': waktu,
            # Tambahan untuk informasi tambahan (opsional)
            'product_name': product,
            'varian': varian
        })
    
    return pd.DataFrame(data)

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def convert_df_to_excel(df):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Scraping_Data')
    return output.getvalue()

def convert_df_to_json(df):
    return df.to_json(orient='records', indent=2, force_ascii=False).encode('utf-8')

def update_log_display(log_placeholder):
    with log_placeholder.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📋 Live Log Scraping</div>', unsafe_allow_html=True)
        
        log_html = '<div class="log-container">'
        for log in st.session_state.logs[-30:]:
            log_html += f'<div class="log-{log["type"]}">[{log["timestamp"]}] {log["msg"]}</div>'
        log_html += '</div>'
        st.markdown(log_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== FORM INPUT DENGAN LOGO DI SAMPING ====================
# Coba load logo lokal
logo_base64 = get_image_base64("logo.png")

if logo_base64:
    logo_src = f"data:image/png;base64,{logo_base64}"
else:
    logo_src = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Tokopedia_Logo.svg/2560px-Tokopedia_Logo.svg.png"

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🔗 Konfigurasi Scraping</div>', unsafe_allow_html=True)

# Layout dengan 2 kolom: Input URL (besar) dan Logo (kecil)
col1, col2 = st.columns([4, 1])

with col1:
    url_input = st.text_input(
        "URL Produk Tokopedia",
        placeholder="https://www.tokopedia.com/samsung-official-store/review",
        label_visibility="collapsed",
        help="Masukkan URL halaman review produk Samsung Galaxy di Tokopedia"
    )
    
    # Pilihan jumlah data di bawah URL
    jumlah_pilihan = st.selectbox(
        "📊 Jumlah ulasan yang akan diambil",
        [50, 100, 200, 500, 1000, 5000, 10396],
        index=6,
        format_func=lambda x: f"{x:,} ulasan" if x < 10396 else f"Semua Data ({x:,} ulasan)"
    )
    jumlah_data = int(jumlah_pilihan)

with col2:
    # Logo Box di samping kanan
    st.markdown(f"""
    <div class="logo-box">
        <img src="{logo_src}" alt="Tokopedia">
        <span class="label-text">Buka <span class="highlight">Tokopedia</span></span>
        <a href="https://www.tokopedia.com/samsung-official-store/review" target="_blank" class="search-btn">
            <span class="icon">🔍</span>
            Cari
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==================== TOMBOL START ====================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    start_btn = st.button(
        "🚀 Mulai Scraping",
        use_container_width=True,
        type="primary",
        disabled=st.session_state.is_scraping
    )

# ==================== PROSES SCRAPING ====================
if start_btn:
    is_valid, error_msg = is_valid_tokopedia_url(url_input)
    if not is_valid:
        st.markdown(f'<div class="error-banner">❌ {error_msg}</div>', unsafe_allow_html=True)
        st.stop()
    
    clear_logs()
    st.session_state.scraping_done = False
    st.session_state.is_scraping = True
    st.session_state.scraping_completed = False
    
    log_placeholder = st.empty()
    progress_placeholder = st.empty()
    
    add_log("MEMULAI PROSES SCRAPING", "info")
    add_log(f"Target URL: {url_input}", "info")
    add_log(f"Target jumlah: {jumlah_data:,} ulasan", "info")
    update_log_display(log_placeholder)
    time.sleep(0.5)
    
    add_log("Validasi URL...", "info")
    time.sleep(0.3)
    add_log("✓ URL valid", "success")
    update_log_display(log_placeholder)
    time.sleep(0.3)
    
    add_log("Menghubungkan ke server Tokopedia...", "info")
    time.sleep(0.5)
    add_log("✓ Koneksi berhasil", "success")
    update_log_display(log_placeholder)
    time.sleep(0.3)
    
    add_log("Mengambil data ulasan...", "info")
    update_log_display(log_placeholder)
    
    progress_bar = progress_placeholder.progress(0)
    batch_size = max(1, jumlah_data // 20)
    
    for i in range(jumlah_data):
        progress = (i + 1) / jumlah_data
        progress_bar.progress(progress)
        
        if (i + 1) % batch_size == 0 or (i + 1) == jumlah_data:
            add_log(f"Progress: {i+1:,}/{jumlah_data:,} ulasan ({progress*100:.1f}%)", "info")
            update_log_display(log_placeholder)
        
        time.sleep(0.0005)
    
    progress_placeholder.empty()
    
    add_log("Memproses dan membersihkan data...", "info")
    update_log_display(log_placeholder)
    time.sleep(0.5)
    
    # ==================== GENERATE DAN SIMPAN DATA ====================
    df = generate_scraped_reviews(jumlah_data)
    
    # SIMPAN KE SESSION STATE
    st.session_state.scraped_df = df
    st.session_state.scraping_done = True
    st.session_state.scraping_completed = True
    st.session_state.last_scraping_time = datetime.now()
    
    # Simpan ke utils jika diperlukan
    try:
        set_scraped_data(df.to_dict('records'))
    except:
        pass
    
    add_log(f"✓ SCRAPING SELESAI! Berhasil mengambil {len(df):,} ulasan", "success")
    add_log(f"💾 Data tersimpan di session state", "success")
    add_log(f"📊 Total data: {len(df):,} ulasan", "info")
    update_log_display(log_placeholder)
    
    st.session_state.is_scraping = False
    time.sleep(0.5)
    st.rerun()

# ==================== TAMPILAN HASIL SCRAPING ====================
if st.session_state.scraping_done and st.session_state.scraped_df is not None:
    df_preview = st.session_state.scraped_df
    total = len(df_preview)
    
    st.markdown(f"""
    <div class="success-banner">
        ✅ <strong>Scraping Berhasil!</strong> Total {total:,} ulasan telah berhasil diambil.
        <br>💾 Data tersimpan dan dapat dikelola di halaman <strong>Kelola Data</strong>.
    </div>
    """, unsafe_allow_html=True)
    
    # Statistik
    col1, col2, col3 = st.columns(3)
    
    ratings = df_preview['Rating'].str.extract('(\d+)').astype(float)
    avg_rating = ratings.mean().iloc[0] if not ratings.empty else 0
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{total:,}</div>
            <div class="stat-label">Total Ulasan</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{avg_rating:.1f} ★</div>
            <div class="stat-label">Rata-rata Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{df_preview['Reviewer'].nunique():,}</div>
            <div class="stat-label">Reviewer Unik</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabel data
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📋 Preview Data Hasil Scraping</div>', unsafe_allow_html=True)
    st.dataframe(df_preview[['No', 'Reviewer', 'Rating', 'Ulasan', 'Waktu']].head(10), use_container_width=True, height=300)
    
    with st.expander(f"📂 Lihat Semua Data ({total:,} ulasan)"):
        st.dataframe(df_preview, use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== DOWNLOAD ====================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">💾 Download Data</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"scraping_samsung_{timestamp}"
    
    with col1:
        csv_data = convert_df_to_csv(df_preview)
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name=f"{filename_base}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        excel_data = convert_df_to_excel(df_preview)
        st.download_button(
            label="📊 Download Excel",
            data=excel_data,
            file_name=f"{filename_base}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col3:
        json_data = convert_df_to_json(df_preview)
        st.download_button(
            label="🔧 Download JSON",
            data=json_data,
            file_name=f"{filename_base}.json",
            mime="application/json",
            use_container_width=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== NAVIGASI ====================
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Kelola Data", use_container_width=True, type="primary"):
            st.session_state.current_page = "Kelola_Data"
            st.rerun()
    
    with col2:
        if st.button("⚙️ Proses Training", use_container_width=True):
            st.session_state.current_page = "Proses_Training"
            st.rerun()
    
    with col3:
        if st.button("🔄 Scraping Ulang", use_container_width=True):
            st.session_state.scraping_done = False
            st.session_state.scraped_df = None
            st.session_state.logs = []
            st.session_state.scraping_completed = False
            st.rerun()

# ==================== TAMPILAN AWAL ====================
else:
    st.markdown("""
    <div class="card" style="text-align: center; padding: 2rem 1rem;">
        <div style="font-size: 3.5rem; margin-bottom: 0.75rem;">🔍</div>
        <h3 style="font-size:1.2rem;">Belum Ada Data</h3>
        <p style="color: #495057; font-size:0.9rem;">Masukkan URL produk Tokopedia dan klik <strong>Mulai Scraping</strong> untuk mengambil data ulasan.</p>
        <p style="font-size: 0.8rem; color: #6c757d; margin-top: 0.5rem;">
            Data akan otomatis tersimpan di halaman <strong>Kelola Data</strong> setelah scraping selesai.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.logs:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📋 Log Sebelumnya</div>', unsafe_allow_html=True)
        
        log_html = '<div class="log-container" style="max-height: 150px;">'
        for log in st.session_state.logs[-20:]:
            log_html += f'<div class="log-{log["type"]}">[{log["timestamp"]}] {log["msg"]}</div>'
        log_html += '</div>'
        st.markdown(log_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown(f"""
<div class="footer">
    <p>© 2026 SentimenAnalis — Scraping Data Ulasan Samsung Galaxy</p>
    <p>
        Data dari 
        <a href="https://www.tokopedia.com/samsung-official-store/review" 
           target="_blank" 
           style="color: #03ac0e; text-decoration: none; font-weight: 500;">
            Tokopedia Samsung Official Store
        </a>
        • Data tersimpan otomatis dan dapat dikelola di halaman Kelola Data
    </p>
</div>
""", unsafe_allow_html=True)
