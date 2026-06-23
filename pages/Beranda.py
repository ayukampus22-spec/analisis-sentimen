import streamlit as st

st.markdown("""
<style>
    /* Perbesar semua teks di halaman ini */
    * {
        font-size: 18px !important;
    }
    
    h1 {
        font-size: 36px !important;
    }
    h2 {
        font-size: 32px !important;
    }
    h3 {
        font-size: 28px !important;
    }
    h4 {
        font-size: 24px !important;
    }
    h5 {
        font-size: 20px !important;
    }
    h6 {
        font-size: 18px !important;
    }
    
    .hero {
        background: linear-gradient(120deg, #ffffff 0%, #f8fafc 100%);
        padding: 3rem 2rem;
        text-align: center;
        border-radius: 24px;
        margin-bottom: 2rem;
        border: 1px solid #eef2f8;
    }
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
    }
    .hero-title .highlight {
        background: linear-gradient(120deg, #2ecc71, #27ae60);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-desc {
        color: #5b6e8c;
        max-width: 600px;
        margin: 0 auto 1.5rem;
        font-size: 1.4rem !important;
        line-height: 1.8;
    }
    .feature-card {
        background: white;
        padding: 2rem 1rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #eef2f8;
        transition: all 0.2s;
        height: 100%;
    }
    .feature-card:hover {
        border-color: #2ecc71;
    }
    .feature-icon {
        width: 72px;
        height: 72px;
        background: #e8f5ed;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
    }
    .feature-icon i { 
        font-size: 34px !important; 
        color: #2ecc71; 
    }
    .feature-card h4 { 
        font-size: 1.4rem !important; 
        margin-bottom: 0.75rem;
        font-weight: 600;
    }
    .feature-card p { 
        font-size: 1.1rem !important; 
        color: #6b7c93;
        line-height: 1.6;
    }
    .step-card { 
        text-align: center;
        padding: 1rem 0.5rem;
    }
    .step-number {
        width: 64px;
        height: 64px;
        background: #e8f5ed;
        color: #2ecc71;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem !important;
        font-weight: 700;
        margin: 0 auto 0.75rem;
    }
    .step-card h4 { 
        font-size: 1.3rem !important; 
        margin-bottom: 0.75rem;
        font-weight: 600;
    }
    .step-card p { 
        font-size: 1.1rem !important; 
        color: #6b7c93;
        line-height: 1.6;
    }
    .footer {
        background: #1e293b;
        padding: 2.5rem 1.5rem;
        text-align: center;
        border-radius: 20px;
        margin-top: 2rem;
    }
    .footer p { 
        color: #94a3b8; 
        font-size: 1.1rem !important; 
        margin: 0;
        font-weight: 400;
    }
    /* Judul section Cara Kerja */
    .section-title {
        font-size: 2.5rem !important;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0;
        color: #1e293b;
    }
    hr {
        margin: 2.5rem 0;
        border: none;
        border-top: 2px solid #eef2f8;
    }
    
    /* Perbesar teks di semua komponen Streamlit */
    .stMarkdown {
        font-size: 18px !important;
    }
    .stMarkdown p {
        font-size: 18px !important;
        line-height: 1.8 !important;
    }
    .stButton button {
        font-size: 18px !important;
        padding: 0.6rem 1.5rem !important;
    }
    .stAlert {
        font-size: 18px !important;
    }
    .stAlert div {
        font-size: 18px !important;
    }
    .stDataFrame {
        font-size: 18px !important;
    }
    .stMetric {
        font-size: 20px !important;
    }
    .stMetric label {
        font-size: 18px !important;
    }
    .stMetric .stMetric-value {
        font-size: 32px !important;
    }
    .stTabs [role="tab"] {
        font-size: 18px !important;
    }
    .streamlit-expanderHeader {
        font-size: 20px !important;
    }
    .stTextInput input, 
    .stTextArea textarea, 
    .stSelectbox select {
        font-size: 18px !important;
    }
    .stCaption {
        font-size: 16px !important;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">
        Analisis Sentimen <br>
        <span class="highlight">Ulasan Produk</span>
    </div>
    <div class="hero-desc">
        Platform cerdas untuk menganalisis sentimen ulasan produk 
        menggunakan teknologi Machine Learning dengan akurasi tinggi
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"><i class="fas fa-brain"></i></div>
        <h4>Machine Learning</h4>
        <p>Naive Bayes untuk klasifikasi otomatis</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"><i class="fas fa-chart-line"></i></div>
        <h4>Visualisasi Data</h4>
        <p>Grafik interaktif pola sentimen</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"><i class="fas fa-gauge-high"></i></div>
        <h4>Proses Cepat</h4>
        <p>Analisis ribuan ulasan instan</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"><i class="fas fa-file-export"></i></div>
        <h4>Export Data</h4>
        <p>Unduh hasil dalam format CSV</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Cara Kerja</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">1</div>
        <h4>Scraping Data</h4>
        <p>Ambil ulasan dari Tokopedia</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">2</div>
        <h4>Proses Training</h4>
        <p>Training model Naive Bayes</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">3</div>
        <h4>Hasil Analisis</h4>
        <p>Lihat akurasi & confusion matrix</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">4</div>
        <h4>Prediksi</h4>
        <p>Uji dengan teks ulasan baru</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <p>© 2026 SentimenAnalis — Analisis Sentimen Ulasan Produk</p>
</div>
""", unsafe_allow_html=True)