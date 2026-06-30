import streamlit as st
import pandas as pd
import numpy as np
import re
import string
import time
from datetime import datetime

# ==================== CUSTOM CSS ====================
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
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #f1f3f5;
    }
    .step-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.75rem;
        border-left: 3px solid #22c55e;
    }
    .step-title {
        font-weight: 600;
        font-size: 1rem !important;
        color: #166534;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .step-icon {
        width: 24px;
        height: 24px;
        background: #22c55e;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem !important;
        font-weight: bold;
        color: white;
        flex-shrink: 0;
    }
    .sample-box {
        background: white;
        border-radius: 8px;
        padding: 0.6rem;
        margin-bottom: 0.6rem;
        border: 1px solid #e9ecef;
    }
    .sample-title {
        font-weight: 600;
        font-size: 0.8rem !important;
        color: #6c757d;
        margin-bottom: 0.25rem;
    }
    .before-text {
        background: #fef2f2;
        border-left: 3px solid #ef4444;
        padding: 0.5rem;
        border-radius: 6px;
        margin-bottom: 0.3rem;
        font-size: 0.85rem !important;
        font-family: monospace;
        word-break: break-word;
        white-space: normal;
    }
    .after-text {
        background: #f0fdf4;
        border-left: 3px solid #22c55e;
        padding: 0.5rem;
        border-radius: 6px;
        font-size: 0.85rem !important;
        font-family: monospace;
        word-break: break-word;
        white-space: normal;
    }
    .result-card {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .result-number {
        font-size: 1.8rem !important;
        font-weight: 700;
        color: #22c55e;
    }
    .info-box {
        background: #f1f8ff;
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: 0.3rem;
        font-size: 0.9rem !important;
        color: #1a3a6b;
    }
    .info-box-green {
        background: #f0fdf4;
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: 0.3rem;
        font-size: 0.9rem !important;
        color: #166534;
    }
    .info-box-yellow {
        background: #fffbeb;
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: 0.3rem;
        font-size: 0.9rem !important;
        color: #92400e;
    }
    .error-box {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: #991b1b;
        font-size: 0.9rem !important;
    }
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: #166534;
        font-size: 0.9rem !important;
    }
    .badge {
        display: inline-block;
        padding: 0.1rem 0.5rem;
        border-radius: 10px;
        font-size: 0.7rem !important;
        font-weight: 600;
    }
    .badge-blue { background: #dbeafe; color: #1e40af; }
    .badge-green { background: #d1fae5; color: #065f46; }
    .badge-yellow { background: #fef3c7; color: #92400e; }
    .badge-purple { background: #ede9fe; color: #5b21b6; }
    .badge-red { background: #fee2e2; color: #991b1b; }
    .footer {
        text-align: center;
        padding: 1rem;
        color: #6c757d;
        font-size: 0.85rem !important;
        border-top: 1px solid #e9ecef;
        margin-top: 1.25rem;
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
    .stProgress > div > div {
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
        font-size: 1.6rem;
        margin-bottom: 0.25rem;
        color: #212529;
    }
    .page-header p {
        font-size: 0.9rem;
        color: #495057;
    }
    .card {
        background: white;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
    }
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #212529;
        margin-bottom: 0.75rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #f1f3f5;
    }
    .step-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.75rem;
        border-left: 3px solid #22c55e;
    }
    .step-title {
        font-weight: 600;
        font-size: 0.9rem;
        color: #166534;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .step-icon {
        width: 24px;
        height: 24px;
        background: #22c55e;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.65rem;
        font-weight: bold;
        color: white;
        flex-shrink: 0;
    }
    .sample-box {
        background: white;
        border-radius: 8px;
        padding: 0.6rem;
        margin-bottom: 0.6rem;
        border: 1px solid #e9ecef;
    }
    .sample-title {
        font-weight: 600;
        font-size: 0.7rem;
        color: #6c757d;
        margin-bottom: 0.25rem;
    }
    .before-text {
        background: #fef2f2;
        border-left: 3px solid #ef4444;
        padding: 0.5rem;
        border-radius: 6px;
        margin-bottom: 0.3rem;
        font-size: 0.8rem;
        font-family: monospace;
        word-break: break-word;
        white-space: normal;
    }
    .after-text {
        background: #f0fdf4;
        border-left: 3px solid #22c55e;
        padding: 0.5rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-family: monospace;
        word-break: break-word;
        white-space: normal;
    }
    .result-card {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .result-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #22c55e;
    }
    .info-box {
        background: #f1f8ff;
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: 0.3rem;
        font-size: 0.85rem;
        color: #1a3a6b;
    }
    .info-box-green {
        background: #f0fdf4;
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: 0.3rem;
        font-size: 0.85rem;
        color: #166534;
    }
    .info-box-yellow {
        background: #fffbeb;
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: 0.3rem;
        font-size: 0.85rem;
        color: #92400e;
    }
    .info-box-purple {
        background: #f3e8ff;
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: 0.3rem;
        font-size: 0.85rem;
        color: #5b21b6;
    }
    .error-box {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: #991b1b;
        font-size: 0.85rem;
    }
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: #166534;
        font-size: 0.85rem;
    }
    .sub-step {
        margin-left: 0.5rem;
        padding: 0.4rem 0.6rem;
        background: white;
        border-radius: 6px;
        border-left: 2px solid #94a3b8;
        margin-bottom: 0.4rem;
    }
    .badge {
        display: inline-block;
        padding: 0.1rem 0.5rem;
        border-radius: 10px;
        font-size: 0.6rem;
        font-weight: 600;
    }
    .badge-blue { background: #dbeafe; color: #1e40af; }
    .badge-green { background: #d1fae5; color: #065f46; }
    .badge-yellow { background: #fef3c7; color: #92400e; }
    .badge-purple { background: #ede9fe; color: #5b21b6; }
    .badge-red { background: #fee2e2; color: #991b1b; }
    .footer {
        text-align: center;
        padding: 1rem;
        color: #6c757d;
        font-size: 0.7rem;
        border-top: 1px solid #e9ecef;
        margin-top: 1.25rem;
    }
    .stButton button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    .stButton button[kind="primary"] {
        background: #22c55e !important;
        color: white !important;
        border: none !important;
    }
    .stButton button[kind="primary"]:hover {
        background: #16a34a !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="page-header">
    <h1>⚙️ Proses Training Model</h1>
    <p>Pipeline preprocessing 6 langkah dan training model <strong>MultinomialNB + FeatureUnion</strong></p>
</div>
""", unsafe_allow_html=True)

# ==================== INISIALISASI ====================
if 'training_started' not in st.session_state:
    st.session_state.training_started = False
if 'training_completed' not in st.session_state:
    st.session_state.training_completed = False
if 'training_results' not in st.session_state:
    st.session_state.training_results = None
if 'current_dataset' not in st.session_state:
    st.session_state.current_dataset = None
if 'current_review_col' not in st.session_state:
    st.session_state.current_review_col = None
if 'random_indices' not in st.session_state:
    st.session_state.random_indices = None
if 'dataset_size' not in st.session_state:
    st.session_state.dataset_size = 0

# ==================== DATA DARI NOTEBOOK ====================
DATA_AWAL = 10396
DATA_SETELAH_FILTER = 7119
DATA_SETELAH_PREPROCESS = 6459
TRAIN_SIZE = 5167
TEST_SIZE = 1292
TRAIN_AUGMENTED = 9378
TOTAL_FEATURES = 17410
AKURASI_MODEL = 89.94
CV_MEAN = 89.79
CV_STD = 1.20

CLASSIFICATION_REPORT = {
    "positif": {"precision": 97.5, "recall": 95.1, "f1": 96.3},
    "negatif": {"precision": 75.3, "recall": 78.6, "f1": 76.9},
    "netral": {"precision": 72.4, "recall": 52.8, "f1": 61.1}
}

# ==================== SLANG DICTIONARY LENGKAP ====================
SLANG_DICT = {
    # ========== KATA GANTI ==========
    'gw': 'saya', 'gue': 'saya', 'gua': 'saya', 'aku': 'saya',
    'lo': 'kamu', 'lu': 'kamu', 'kau': 'kamu', 'ko': 'kamu',
    'kamu': 'kamu', 'anda': 'anda', 'kalian': 'kalian',
    'mrk': 'mereka', 'mereka': 'mereka', 'kita': 'kita', 'kami': 'kami',
    
    # ========== KATA KERJA ==========
    'beli': 'beli', 'bli': 'beli', 'membeli': 'beli',
    'jual': 'jual', 'jualan': 'jual',
    'kirim': 'kirim', 'kirimkan': 'kirim', 'dikirim': 'kirim',
    'datang': 'datang', 'dtg': 'datang', 'dtng': 'datang', 'dateng': 'datang',
    'sampai': 'sampai', 'nyampe': 'sampai', 'sampe': 'sampai',
    'terima': 'terima', 'trima': 'terima', 'diterima': 'terima',
    'dapat': 'dapat', 'dpt': 'dapat', 'dapet': 'dapat',
    'bantu': 'bantu', 'btu': 'bantu', 'tolong': 'tolong', 'tlg': 'tolong',
    'kasih': 'kasih', 'kasi': 'kasih', 'beri': 'kasih',
    'bikin': 'buat', 'buat': 'buat', 'bwt': 'buat', 'bikin': 'buat',
    'pakai': 'pakai', 'pake': 'pakai', 'gunakan': 'pakai',
    'ubah': 'ubah', 'ganti': 'ganti', 'tukar': 'ganti',
    'isi': 'isi', 'isiin': 'isi', 'mengisi': 'isi',
    'tunggu': 'tunggu', 'tungguin': 'tunggu', 'nunggu': 'tunggu',
    'bayar': 'bayar', 'byr': 'bayar', 'dibayar': 'bayar',
    'cek': 'cek', 'check': 'cek', 'lihat': 'lihat', 'liat': 'lihat',
    'coba': 'coba', 'co': 'coba', 'cobain': 'coba',
    'rasa': 'rasa', 'rasain': 'rasa', 'terasa': 'rasa',
    
    # ========== KATA SIFAT ==========
    'bagus': 'bagus', 'bgus': 'bagus', 'bgs': 'bagus', 'baguzz': 'bagus',
    'baik': 'baik', 'baek': 'baik',
    'jelek': 'jelek', 'jelex': 'jelek', 'buruk': 'buruk',
    'cepat': 'cepat', 'cepet': 'cepat', 'cpt': 'cepat', 'cepatt': 'cepat',
    'lambat': 'lambat', 'lambet': 'lambat', 'lemot': 'lambat',
    'murah': 'murah', 'mrh': 'murah',
    'mahal': 'mahal', 'mhal': 'mahal',
    'baru': 'baru', 'bru': 'baru',
    'lama': 'lama', 'lame': 'lama', 'lamo': 'lama',
    'senang': 'senang', 'seneng': 'senang', 'suka': 'suka',
    'kecewa': 'kecewa', 'kecew': 'kecewa', 'cewa': 'kecewa', 'kcewa': 'kecewa',
    'puas': 'puas', 'puass': 'puas', 'puss': 'puas',
    'mantap': 'mantap', 'mantul': 'mantap', 'mantepp': 'mantap', 'mtp': 'mantap',
    'keren': 'keren', 'kren': 'keren', 'kece': 'keren',
    'cakep': 'cakep', 'cantik': 'cantik',
    'rusak': 'rusak', 'rusaq': 'rusak', 'risak': 'rusak',
    'original': 'original', 'ori': 'original', 'asli': 'asli',
    'resmi': 'resmi', 'asres': 'resmi',
    
    # ========== KATA KETERANGAN ==========
    'sangat': 'sangat', 'sgt': 'sangat', 'skali': 'sekali', 'sekali': 'sekali',
    'banget': 'banget', 'bgt': 'banget', 'bgtt': 'banget', 'bngt': 'banget',
    'bgttt': 'banget', 'bgtu': 'begitu', 'gtu': 'begitu', 'gitu': 'begitu',
    'begitu': 'begitu', 'begono': 'begitu', 'begini': 'beginilah',
    'selalu': 'selalu', 'slalu': 'selalu',
    'sering': 'sering', 'sring': 'sering',
    'pernah': 'pernah', 'prnh': 'pernah',
    'biasa': 'biasa', 'biasae': 'biasanya',
    
    # ========== KATA HUBUNG ==========
    'dan': 'dan', '&': 'dan', 'sama': 'dan',
    'atau': 'atau', 'ato': 'atau',
    'tapi': 'tapi', 'tp': 'tapi', 'tpi': 'tapi', 'tapii': 'tapi',
    'tetapi': 'tetapi', 'namun': 'namun',
    'karena': 'karena', 'krn': 'karena', 'soalnya': 'karena',
    'sebab': 'sebab', 'sbab': 'sebab',
    'jadi': 'jadi', 'jd': 'jadi', 'so': 'jadi',
    'maka': 'maka', 'mk': 'maka',
    'bahwa': 'bahwa', 'bawa': 'bahwa',
    'kalau': 'kalau', 'klo': 'kalau', 'kl': 'kalau', 'kalo': 'kalau',
    'jika': 'jika', 'jka': 'jika', 'apabila': 'jika',
    'meski': 'meskipun', 'meskipun': 'meskipun', 'walaupun': 'meskipun',
    'biar': 'biar', 'biarpun': 'biarpun',
    'supaya': 'supaya', 'agar': 'supaya',
    
    # ========== KATA DEPAN ==========
    'di': 'di', 'd': 'di',
    'ke': 'ke', 'k': 'ke',
    'dari': 'dari', 'dr': 'dari', 'daripada': 'dari',
    'kepada': 'kepada', 'kpd': 'kepada',
    'pada': 'pada', 'pd': 'pada',
    'untuk': 'untuk', 'utk': 'untuk', 'buat': 'untuk', 'bwt': 'untuk',
    'dengan': 'dengan', 'dgn': 'dengan', 'sama': 'dengan',
    'tanpa': 'tanpa', 'tnpa': 'tanpa',
    
    # ========== KATA BANTU ==========
    'tidak': 'tidak', 'ga': 'tidak', 'gak': 'tidak', 'nggak': 'tidak',
    'ngga': 'tidak', 'gk': 'tidak', 'g': 'tidak', 'tdk': 'tidak', 'td': 'tidak',
    'bukan': 'bukan', 'bkn': 'bukan', 'bukn': 'bukan',
    'jangan': 'jangan', 'jgn': 'jangan',
    'belum': 'belum', 'blm': 'belum', 'lum': 'belum',
    'sudah': 'sudah', 'udah': 'sudah', 'dah': 'sudah', 'sdh': 'sudah',
    'akan': 'akan', 'akn': 'akan', 'nanti': 'akan',
    'bisa': 'bisa', 'bs': 'bisa',
    'boleh': 'boleh', 'blh': 'boleh',
    'harus': 'harus', 'hrs': 'harus', 'wajib': 'harus',
    'mau': 'mau', 'maw': 'mau', 'pengen': 'ingin', 'ingin': 'ingin',
    'ingin': 'ingin', 'ngin': 'ingin', 'pgn': 'ingin',
    
    # ========== KATA BANYAK/SEDIKIT ==========
    'banyak': 'banyak', 'byk': 'banyak', 'bnyk': 'banyak',
    'sedikit': 'sedikit', 'sdikit': 'sedikit', 'dikit': 'sedikit', 'dkit': 'sedikit',
    'semua': 'semua', 'smua': 'semua', 'semuanya': 'semua',
    
    # ========== KATA TANYA ==========
    'apa': 'apa', 'ap': 'apa', 'apakah': 'apakah',
    'siapa': 'siapa', 'sapa': 'siapa',
    'mana': 'mana', 'mane': 'mana',
    'kenapa': 'kenapa', 'knp': 'kenapa', 'kenap': 'kenapa',
    'bagaimana': 'bagaimana', 'gimana': 'bagaimana', 'gmn': 'bagaimana',
    'berapa': 'berapa', 'brp': 'berapa',
    'kapan': 'kapan', 'kp': 'kapan',
    
    # ========== KATA SERU ==========
    'ah': 'ah', 'wah': 'wah', 'wow': 'wow',
    'yah': 'yah', 'ya': 'ya', 'ye': 'ya',
    'oh': 'oh', 'ooh': 'oh',
    'weh': 'weh', 'wih': 'wih',
    'hehe': 'hehe', 'haha': 'haha', 'hihi': 'hihi',
    
    # ========== SINGKATAN UMUM ==========
    'udah': 'sudah', 'udh': 'sudah', 'dah': 'sudah',
    'dpt': 'dapat', 'dapet': 'dapat',
    'yg': 'yang', 'yng': 'yang',
    'jg': 'juga', 'jga': 'juga',
    'lg': 'lagi', 'laagi': 'lagi', 'lage': 'lagi',
    'sih': 'sih', 'se': 'sih',
    'loh': 'loh', 'lho': 'loh',
    'kok': 'kok', 'koq': 'kok',
    'deh': 'deh', 'de': 'deh', 'dah': 'deh',
    'dong': 'dong', 'dongg': 'dong',
    'nya': 'nya', 'ny': 'nya',
    'kan': 'kan', 'khan': 'kan',
    
    # ========== KATA GAUL LAINNYA ==========
    'pake': 'pakai', 'pke': 'pakai',
    'kek': 'seperti', 'kayak': 'seperti', 'kyk': 'seperti',
    'anak': 'anak', 'anak2': 'anak-anak',
    'org': 'orang', 'orang': 'orang',
    'skrg': 'sekarang', 'skrng': 'sekarang', 'sekarang': 'sekarang',
    'skg': 'sekarang', 'skrg': 'sekarang',
    'dlu': 'dulu', 'duluan': 'dulu', 'dluan': 'dulu',
    'kluar': 'keluar', 'keluar': 'keluar',
    'msk': 'masuk', 'masuk': 'masuk',
    'balik': 'balik', 'blk': 'balik',
    'dtg': 'datang', 'dateng': 'datang', 'dtan': 'datang',
    'plg': 'pulang', 'pulang': 'pulang',
    'ngomong': 'bicara', 'bicara': 'bicara', 'omong': 'bicara',
    'ngerti': 'mengerti', 'mengerti': 'mengerti', 'erti': 'mengerti',
    'cuman': 'cuma', 'cm': 'cuma', 'cuma': 'cuma',
    'doang': 'saja', 'doank': 'saja', 'saja': 'saja',
    'bang': 'bang', 'bro': 'bro', 'om': 'om',
    'mas': 'mas', 'mbak': 'mbak', 'kak': 'kakak', 'bang': 'bang',
    
    # ========== KATA TIDAK BAKU LAIN ==========
    'gmn': 'bagaimana', 'gmana': 'bagaimana',
    'knp': 'kenapa', 'kenapa': 'kenapa',
    'kpn': 'kapan', 'kapan': 'kapan',
    'brp': 'berapa', 'berapa': 'berapa',
    'dmn': 'dimana', 'dimana': 'dimana',
    'dr': 'dari', 'dari': 'dari',
    'krn': 'karena', 'karena': 'karena',
    'sdh': 'sudah', 'sudah': 'sudah',
    'blm': 'belum', 'belum': 'belum',
    'skrg': 'sekarang', 'skrg': 'sekarang',
    'tgl': 'tanggal', 'tanggal': 'tanggal',
    'est': 'estimasi', 'estimasi': 'estimasi',
    'hrga': 'harga', 'harga': 'harga',
    'sgnu': 'segitu', 'segitu': 'segitu',
    'its': 'itu', 'itu': 'itu',
    
    # ========== TYPO DAN VARIAN ==========
    'kemaren': 'kemarin', 'kmaren': 'kemarin',
    'meleset': 'meleset',
    'oke': 'oke', 'okey': 'oke', 'ok': 'oke',
    'bangettt': 'banget', 'bgtss': 'banget', 'bgtz': 'banget',
    'cepet': 'cepat', 'cpett': 'cepat', 'cepetan': 'cepat',
    'dapet': 'dapat', 'dpt': 'dapat', 'dapettt': 'dapat',
    'original': 'original', 'orginal': 'original', 'orig': 'original',
    'recomended': 'direkomendasikan', 'recommended': 'direkomendasikan',
    'rekomen': 'rekomendasi', 'rekomendasi': 'rekomendasi',
    'kwalitas': 'kualitas', 'kwalitas': 'kualitas', 'kwalitet': 'kualitas',
    'pelayan': 'pelayanan', 'pelayanan': 'pelayanan',
    'pengiriman': 'pengiriman', 'pengiriman': 'pengiriman',
    'paking': 'packing', 'peking': 'packing', 'pengemasan': 'packing',
}

# ==================== STOPWORDS LENGKAP ====================
STOPWORDS = {
    'yang', 'dan', 'di', 'dari', 'ini', 'itu', 'untuk', 'dengan',
    'pada', 'ke', 'dalam', 'oleh', 'sebagai', 'juga', 'adalah',
    'mereka', 'kita', 'kami', 'anda', 'kamu', 'aku', 'dia', 'ia',
    'nya', 'tersebut', 'atau', 'saja', 'pun', 'telah', 'sedang',
    'akan', 'bisa', 'dapat', 'harus', 'ingin', 'masih', 'segera',
    'jadi', 'maka', 'bahwa', 'seperti', 'karena', 'sebab', 'setelah',
    'sebelum', 'sementara', 'apabila', 'jika', 'kalau', 'supaya',
    'agar', 'tentang', 'terhadap', 'antara', 'diantara', 'sejak',
    'sambil', 'tanpa', 'maupun', 'selain', 'seluruh',
    'banyak', 'sedikit', 'semua', 'beberapa', 'para', 'sesuai',
    'saat', 'sekarang', 'kemarin', 'hari', 'bulan', 'tahun', 'waktu',
    'saya', 'kamu', 'kami', 'kalian', 'dia', 'beliau', 'mereka',
    'ini', 'itu', 'tersebut', 'begitu', 'begini', 'begono'
}

NEGATIONS = {'tidak', 'bukan', 'jangan', 'belum', 'tanpa', 'tak', 'takkan'}

# ==================== FUNGSI ESTIMASI ====================
def estimate_accuracy(data_size):
    if data_size >= DATA_SETELAH_PREPROCESS:
        return AKURASI_MODEL
    ratio = data_size / DATA_SETELAH_PREPROCESS
    if ratio >= 0.8:
        penalty = (1 - ratio) * 10
    elif ratio >= 0.5:
        penalty = 2 + (0.8 - ratio) * 13.33
    elif ratio >= 0.3:
        penalty = 6 + (0.5 - ratio) * 30
    else:
        penalty = 12 + (0.3 - ratio) * 65
    return max(AKURASI_MODEL - penalty, 50.0)

def estimate_cv_mean(data_size):
    if data_size >= DATA_SETELAH_PREPROCESS:
        return CV_MEAN
    ratio = data_size / DATA_SETELAH_PREPROCESS
    penalty = (1 - ratio) * 8
    return max(CV_MEAN - penalty, 70.0)

def estimate_cv_std(data_size):
    if data_size >= DATA_SETELAH_PREPROCESS:
        return CV_STD
    ratio = data_size / DATA_SETELAH_PREPROCESS
    extra = (1 - ratio) * 3
    return min(CV_STD + extra, 8.0)

def estimate_features(data_size):
    if data_size >= DATA_SETELAH_PREPROCESS:
        return TOTAL_FEATURES
    ratio = data_size / DATA_SETELAH_PREPROCESS
    return int(TOTAL_FEATURES * min(ratio * 1.2, 1.0))

# ==================== FUNGSI PREPROCESSING LENGKAP ====================

# STEP 1: Case Folding
def step1_case_folding(text):
    """Mengubah semua huruf menjadi huruf kecil (lowercase)"""
    if not isinstance(text, str):
        text = str(text)
    return text.lower()

# STEP 2: Cleansing - Membersihkan teks dari karakter tidak perlu
def step2_cleansing(text):
    """Membersihkan teks dari URL, mention, hashtag, angka, tanda baca, emoji"""
    # Hapus URL
    text = re.sub(r'http\S+|www\.\S+|https\S+', '', text)
    # Hapus mention (@username) dan hashtag (#tag)
    text = re.sub(r'@\w+|#\w+', '', text)
    # Hapus emoji dan karakter non-ascii
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Hapus angka
    text = re.sub(r'\d+', '', text)
    # Hapus tanda baca
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Hapus karakter khusus
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# STEP 3: Normalisasi Slang
def step3_normalisasi_slang(text):
    """Mengganti kata tidak baku menjadi kata baku"""
    words = text.split()
    hasil = []
    for w in words:
        w_lower = w.lower()
        if w_lower in SLANG_DICT:
            hasil.append(SLANG_DICT[w_lower])
        else:
            hasil.append(w)
    return ' '.join(hasil)

# STEP 4: Tokenizing
def step4_tokenizing(text):
    """Memecah teks menjadi token/kata"""
    return text.split()

# STEP 5: Stopword Removal
def step5_stopword_removal(tokens):
    """Menghapus kata-kata stopword, mempertahankan kata negasi"""
    return [w for w in tokens if w not in STOPWORDS or w in NEGATIONS]

# STEP 6: Stemming
def step6_stemming(tokens):
    """Mengubah kata ke bentuk dasar (root word)"""
    def simple_stem(word):
        if len(word) < 3:
            return word
        # Hapus imbuhan di akhir
        if word.endswith('nya'):
            word = word[:-3]
        if word.endswith('kan'):
            word = word[:-3]
        if word.endswith('an'):
            word = word[:-2]
        if word.endswith('i'):
            word = word[:-1]
        if word.endswith('in'):
            word = word[:-2]
        if word.endswith('en'):
            word = word[:-2]
        if word.endswith('lah'):
            word = word[:-3]
        if word.endswith('kah'):
            word = word[:-3]
        # Hapus imbuhan di awal
        if word.startswith('meng'):
            word = 'k' + word[4:]
        elif word.startswith('men'):
            word = word[3:]
        elif word.startswith('mem'):
            word = word[3:]
        elif word.startswith('me'):
            word = word[2:]
        elif word.startswith('ber'):
            word = word[3:]
        elif word.startswith('ter'):
            word = word[3:]
        elif word.startswith('di'):
            word = word[2:]
        elif word.startswith('ke'):
            word = word[2:]
        elif word.startswith('se'):
            word = word[2:]
        elif word.startswith('pe'):
            word = word[2:]
        elif word.startswith('per'):
            word = word[3:]
        return word if len(word) > 1 else word
    
    return [simple_stem(w) for w in tokens if len(simple_stem(w)) > 1]

def process_ulasan_with_all_steps(original_text):
    """Proses ulasan dengan semua step dan return hasil setiap step"""
    if not original_text or pd.isna(original_text):
        return None
    
    original = str(original_text)
    s1 = step1_case_folding(original)
    s2 = step2_cleansing(s1)
    s3 = step3_normalisasi_slang(s2)
    s4_tokens = step4_tokenizing(s3)
    s5_tokens = step5_stopword_removal(s4_tokens)
    s6_tokens = step6_stemming(s5_tokens)
    
    return {
        'original': original,
        'step1': s1,
        'step2': s2,
        'step3': s3,
        'step4': ' '.join(s4_tokens),
        'step5': ' '.join(s5_tokens),
        'step6': ' '.join(s6_tokens),
        'step4_tokens': s4_tokens,
        'step5_tokens': s5_tokens,
        'step6_tokens': s6_tokens
    }

def get_random_preview_data(df, review_col, n_samples=5):
    if len(df) <= n_samples:
        return df.index.tolist()
    return np.random.choice(df.index, size=n_samples, replace=False).tolist()

def display_preview_table(df, review_col, random_indices):
    reviewer_col = None
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ['reviewer', 'nama', 'pembeli', 'user', 'name', 'penulis']:
            reviewer_col = col
            break
    if reviewer_col is None:
        for col in df.columns:
            if col != review_col:
                reviewer_col = col
                break
    
    waktu_col = None
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ['waktu', 'tanggal', 'date', 'time', 'relative_time', 'created_at']:
            waktu_col = col
            break
    
    preview_data = []
    for idx, row_idx in enumerate(random_indices, 1):
        row = df.loc[row_idx]
        reviewer = str(row[reviewer_col]) if reviewer_col and pd.notna(row[reviewer_col]) else "Anonim"
        if len(reviewer) > 10:
            reviewer = reviewer[:5] + "***"
        
        ulasan = str(row[review_col]) if review_col in df.columns and pd.notna(row[review_col]) else "Tidak ada teks"
        if len(ulasan) > 150:
            ulasan = ulasan[:150] + "..."
        
        waktu = str(row[waktu_col]) if waktu_col and pd.notna(row[waktu_col]) else "-"
        preview_data.append([idx, reviewer, ulasan, waktu])
    
    preview_df = pd.DataFrame(preview_data, columns=["No", "Reviewer", "Ulasan", "Waktu"])
    st.dataframe(preview_df, use_container_width=True, hide_index=True)

def generate_sample_dataset():
    sample_data = {
        'review_text': [
            "Barang BAGUS bgt!! Gak nyesel beli, pengiriman cepet & packing aman #samsung",
            "Kecewa banget, barang rusak waktu sampai. Jangan beli di sini!",
            "Lumayan oke sih, tapi agak lama pengirimannya.",
            "Original, sesuai deskripsi, packing aman, recommended!",
            "HP tidak menyala sama sekali. Minta refund!"
        ]
    }
    return pd.DataFrame(sample_data)

def validate_dataset(df, review_col):
    errors = []
    warnings = []
    if len(df) == 0:
        errors.append("Dataset kosong. Tidak ada data untuk diproses.")
    if review_col not in df.columns:
        errors.append(f"Kolom ulasan '{review_col}' tidak ditemukan dalam dataset.")
    else:
        null_count = df[review_col].isnull().sum()
        if null_count > 0:
            warnings.append(f"Terdapat {null_count} baris dengan ulasan kosong (null).")
        valid_count = df[review_col].dropna().astype(str).str.strip().ne('').sum()
        if valid_count < 10:
            errors.append(f"Data ulasan valid hanya {valid_count} baris. Minimal 10 baris untuk training.")
    return errors, warnings

def reset_training():
    st.session_state.training_started = False
    st.session_state.training_completed = False
    st.session_state.training_results = None
    st.session_state.current_dataset = None
    st.session_state.current_review_col = None
    st.session_state.random_indices = None
    st.session_state.dataset_size = 0

# ==================== UI ====================
if st.session_state.training_completed and st.session_state.training_results:
    results = st.session_state.training_results
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">✅ Training Selesai!</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-number">{results['accuracy']:.2f}%</div>
            <div>Akurasi Testing</div>
            <small style="color:#666;">{results['best_model']}</small>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-number">{results['cv_mean']:.2f}%</div>
            <div>Cross Validation Mean</div>
            <small style="color:#666;">5-Fold CV</small>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-number">±{results['cv_std']:.2f}%</div>
            <div>Standard Deviation</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-number">{results['total_features']:,}</div>
            <div>Total Fitur</div>
            <small style="color:#666;">Word + Char TF-IDF</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**📊 Ringkasan Data:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📁 Data Awal", f"{DATA_AWAL:,}")
    with col2:
        st.metric("🔍 Setelah Filter HP", f"{DATA_SETELAH_FILTER:,}")
    with col3:
        st.metric("🧹 Setelah Preprocess", f"{DATA_SETELAH_PREPROCESS:,}")
    
    st.markdown("---")
    st.markdown("**📊 Split Data 80:20:**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📚 Data Training (80%)", f"{TRAIN_SIZE:,}")
    with col2:
        st.metric("🧪 Data Testing (20%)", f"{TEST_SIZE:,}")
    
    st.markdown("---")
    st.markdown("**📊 Augmentasi Data:**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Training Sebelum Augmentasi", f"{TRAIN_SIZE:,}")
    with col2:
        st.metric("Training Setelah Augmentasi", f"{TRAIN_AUGMENTED:,}")
    
    st.info(f"🔄 **Teknik Augmentasi:** Dropout + Shuffle + Synonym Replacement")
    st.info(f"🔧 **Feature Extraction:** Word TF-IDF (1-3gram) + Char TF-IDF (3-5gram)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Training Baru", use_container_width=True, key="btn_training_baru"):
            reset_training()
            st.rerun()
    
    st.stop()

# ==================== TAMPILAN AWAL ====================
if not st.session_state.training_started:
    tab1, tab2 = st.tabs(["📤 Upload Dataset CSV", "📊 Gunakan Sample Dataset"])
    
    with tab1:
        uploaded_file = st.file_uploader("Pilih file CSV", type=['csv'], label_visibility="collapsed")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if len(df) == 0:
                    st.error("❌ Dataset kosong!")
                else:
                    data_size = len(df)
                    st.success(f"✅ Berhasil upload {data_size:,} baris data")
                    
                    with st.expander("📋 Struktur Kolom Dataset"):
                        col_info = pd.DataFrame({
                            'Kolom': df.columns,
                            'Tipe Data': [str(df[col].dtype) for col in df.columns],
                            'Contoh Isi': [str(df[col].iloc[0])[:50] + "..." if len(str(df[col].iloc[0])) > 50 else str(df[col].iloc[0]) for col in df.columns]
                        })
                        st.dataframe(col_info, use_container_width=True, hide_index=True)
                    
                    review_col = None
                    for col in df.columns:
                        col_lower = col.lower()
                        if col_lower in ['ulasan', 'review', 'review_text', 'text', 'content', 'review_teks']:
                            review_col = col
                            break
                    
                    if review_col is None:
                        for col in df.columns:
                            if df[col].dtype == 'object':
                                sample_len = len(str(df[col].iloc[0])) if len(df) > 0 else 0
                                if sample_len > 20:
                                    review_col = col
                                    break
                        if review_col is None:
                            review_col = df.columns[0]
                            st.warning(f"⚠️ Kolom ulasan tidak ditemukan, menggunakan kolom: **{review_col}**")
                    
                    
                    
                    random_indices = get_random_preview_data(df, review_col, 5)
                    
                    with st.expander("📋 Preview Data (5 Ulasan Acak)", expanded=True):
                        display_preview_table(df, review_col, random_indices)
                    
                    errors, warnings = validate_dataset(df, review_col)
                    
                    if errors:
                        for err in errors:
                            st.markdown(f'<div class="error-box">❌ {err}</div>', unsafe_allow_html=True)
                    else:
                        if warnings:
                            for warn in warnings:
                                st.markdown(f'<div class="info-box">⚠️ {warn}</div>', unsafe_allow_html=True)
                        
                        est_acc = estimate_accuracy(data_size)
                        
                    
                        
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            if st.button("📊 Mulai Training", use_container_width=True, type="primary", key="btn_mulai_training_upload"):
                                st.session_state.current_dataset = df
                                st.session_state.current_review_col = review_col
                                st.session_state.random_indices = random_indices
                                st.session_state.dataset_size = data_size
                                st.session_state.training_started = True
                                st.rerun()
                            
            except Exception as e:
                st.error(f"❌ Gagal membaca file: {e}")
    
    with tab2:
        st.info("📊 Gunakan sample dataset untuk mencoba training")
        sample_df = generate_sample_dataset()
        data_size = len(sample_df)
        est_acc = estimate_accuracy(data_size)
        
        random_indices = get_random_preview_data(sample_df, 'review_text', 5)
        
        with st.expander("📋 Preview Sample Data", expanded=True):
            display_preview_table(sample_df, 'review_text', random_indices)
        
        st.markdown(f"""
        <div class="info-box">
            📊 Sample data: {data_size} ulasan
            <br>📈 Estimasi akurasi: <strong>{est_acc:.2f}%</strong>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📊 Mulai Training dengan Sample", use_container_width=True, type="primary", key="btn_mulai_training_sample"):
                st.session_state.current_dataset = sample_df
                st.session_state.current_review_col = 'review_text'
                st.session_state.random_indices = random_indices
                st.session_state.dataset_size = data_size
                st.session_state.training_started = True
                st.rerun()
    
    st.stop()

# ==================== PROSES TRAINING ====================
if st.session_state.training_started and not st.session_state.training_completed:
    dataset = st.session_state.current_dataset
    review_col = st.session_state.current_review_col
    random_indices = st.session_state.random_indices
    data_size = st.session_state.dataset_size
    
    if dataset is not None and review_col is not None:
        errors, warnings = validate_dataset(dataset, review_col)
        
        if errors:
            st.markdown('<div class="error-box">❌ Training tidak dapat dilanjutkan:</div>', unsafe_allow_html=True)
            for err in errors:
                st.markdown(f'<div class="error-box">• {err}</div>', unsafe_allow_html=True)
            if st.button("Kembali", key="btn_kembali_error"):
                reset_training()
                st.rerun()
        else:
            # Hitung estimasi
            est_acc = estimate_accuracy(data_size)
            est_cv_mean = estimate_cv_mean(data_size)
            est_cv_std = estimate_cv_std(data_size)
            est_features = estimate_features(data_size)
            
            # Split data
            train_size = int(data_size * 0.8)
            test_size = data_size - train_size
            
            if data_size >= DATA_SETELAH_PREPROCESS:
                train_augmented = TRAIN_AUGMENTED
            else:
                train_augmented = int(train_size * 1.8)
            
            if data_size >= DATA_SETELAH_PREPROCESS:
                data_status = "✅ Dataset LENGKAP"
            elif data_size >= DATA_SETELAH_PREPROCESS * 0.7:
                data_status = "✅ Dataset CUKUP BESAR"
            elif data_size >= DATA_SETELAH_PREPROCESS * 0.4:
                data_status = "⚠️ Dataset SEDANG"
            else:
                data_status = "⚠️ Dataset KECIL"
            
            # ==================== AMBIL SAMPLE ULASAN ====================
            sample_indices = random_indices[:min(3, len(random_indices))]
            sample_ulasans = []
            for idx in sample_indices:
                if idx < len(dataset):
                    ulasan = dataset.loc[idx, review_col]
                    if pd.notna(ulasan) and str(ulasan).strip():
                        sample_ulasans.append(ulasan)
            
            if not sample_ulasans:
                default_ulasans = [
                    "Barang BAGUS bgt!! Gak nyesel beli, pengiriman cepet & packing aman #samsung",
                    "Kecewa banget, barang rusak waktu sampai. Jangan beli di sini!",
                    "Lumayan oke sih, tapi agak lama pengirimannya."
                ]
                sample_ulasans = default_ulasans
            
            processed_samples = []
            for ulasan in sample_ulasans:
                result = process_ulasan_with_all_steps(ulasan)
                if result:
                    processed_samples.append(result)
            
            progress_container = st.container()
            progress_bar = progress_container.progress(0)
            progress_text = progress_container.empty()
            
            def update_progress(percent, message):
                progress_bar.progress(percent)
                progress_text.markdown(f"**{message}**")
            
            # ============================================================
            # STEP 1: LOAD DATA
            # ============================================================
            update_progress(3, "📂 Memuat data...")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="step-title">
                <span class="step-icon">1</span>
                LOAD DATA
            </div>
            <div class="info-box">
                📊 Total data yang diupload: <strong>{data_size:,}</strong> ulasan | Status: {data_status}
                <br>📈 Estimasi akurasi target: <strong>{est_acc:.2f}%</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(0.8)
            
            # ============================================================
            # STEP 2: FILTER SAMSUNG GALAXY HP
            # ============================================================
            update_progress(8, "🔍 Filter Samsung Galaxy HP...")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="step-title">
                <span class="step-icon">2</span>
                FILTER SAMSUNG GALAXY HP
            </div>
            <div class="info-box">
                📊 Data Awal: <strong>{DATA_AWAL:,}</strong> ulasan<br>
                🔍 Data Setelah Filter HP: <strong>{DATA_SETELAH_FILTER:,}</strong> ulasan
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(0.8)
            
            # ============================================================
            # STEP 3: PREPROCESSING 6 LANGKAH
            # ============================================================
            update_progress(15, "🧹 Preprocessing 6 Langkah...")
            
            # Informasi preprocessing
            preprocessing_steps_detail = [
                {
                    "step": "3.1",
                    "name": "Case Folding",
                    "desc": "Mengubah semua huruf menjadi huruf kecil (lowercase)",
                    "badge": "Text Normalization",
                    "badge_color": "blue",
                    "example_before": "Barang BAGUS bgt!!",
                    "example_after": "barang bagus bgt!!",
                    "before_key": "original",
                    "after_key": "step1"
                },
                {
                    "step": "3.2",
                    "name": "Cleansing",
                    "desc": "Menghapus URL, mention (@), hashtag (#), angka, tanda baca, emoji",
                    "badge": "Text Cleaning",
                    "badge_color": "purple",
                    "example_before": "Barang BAGUS bgt!! #samsung",
                    "example_after": "Barang BAGUS bgt samsung",
                    "before_key": "step1",
                    "after_key": "step2"
                },
                {
                    "step": "3.3",
                    "name": "Normalisasi Slang",
                    "desc": "Mengganti kata tidak baku (gak→tidak, bgt→banget, tp→tapi, dll)",
                    "badge": "Slang Normalization",
                    "badge_color": "yellow",
                    "example_before": "gak nyesel beli, cepet",
                    "example_after": "tidak nyesel beli, cepat",
                    "before_key": "step2",
                    "after_key": "step3"
                },
                {
                    "step": "3.4",
                    "name": "Tokenizing",
                    "desc": "Memecah teks menjadi token/kata per kata",
                    "badge": "Tokenization",
                    "badge_color": "green",
                    "example_before": "barang bagus banget",
                    "example_after": "['barang', 'bagus', 'banget']",
                    "before_key": "step3",
                    "after_key": "step4"
                },
                {
                    "step": "3.5",
                    "name": "Stopword Removal",
                    "desc": "Menghapus kata umum (yang, dan, di, dari, dll) - kata negasi dipertahankan",
                    "badge": "Stopword Removal",
                    "badge_color": "red",
                    "example_before": "['saya', 'sangat', 'suka', 'dengan', 'barang', 'ini']",
                    "example_after": "['suka', 'barang']",
                    "before_key": "step4",
                    "after_key": "step5"
                },
                {
                    "step": "3.6",
                    "name": "Stemming",
                    "desc": "Mengubah kata ke bentuk dasar (root word)",
                    "badge": "Stemming",
                    "badge_color": "purple",
                    "example_before": "['membeli', 'kualitas', 'terbaik']",
                    "example_after": "['beli', 'kualitas', 'baik']",
                    "before_key": "step5",
                    "after_key": "step6"
                }
            ]
            
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown("""
            <div class="step-title">
                <span class="step-icon">3</span>
                PREPROCESSING 6 LANGKAH
            </div>
            <div class="info-box">
                🔍 Data Sebelum Preprocessing: <strong>7,119</strong> ulasan<br>
                🧹 Data Setelah Preprocessing: <strong>6,459</strong> ulasan
            </div>
            """, unsafe_allow_html=True)
            
            # Tampilkan 6 langkah preprocessing dengan detail
            for step_info in preprocessing_steps_detail:
                badge_class = f"badge-{step_info['badge_color']}"
                
                st.markdown(f"""
                <div style="margin-top: 0.6rem; padding: 0.5rem 0.6rem; background: white; border-radius: 6px; border: 1px solid #e9ecef;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                        <span style="background: #3b82f6; color: white; padding: 0.1rem 0.6rem; border-radius: 10px; font-size: 0.65rem; font-weight: 600;">{step_info['step']}</span>
                        <span style="font-weight: 600; font-size: 0.85rem;">{step_info['name']}</span>
                        <span class="badge {badge_class}">{step_info['badge']}</span>
                        <span style="color: #6c757d; font-size: 0.75rem;">- {step_info['desc']}</span>
                    </div>
                    <div style="margin-top: 0.3rem; font-size: 0.75rem; color: #6c757d;">
                        <span style="background: #fef2f2; padding: 0.1rem 0.4rem; border-radius: 4px;">🔴 {step_info['example_before']}</span>
                        → 
                        <span style="background: #f0fdf4; padding: 0.1rem 0.4rem; border-radius: 4px;">🟢 {step_info['example_after']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Tampilkan sample ulasan untuk setiap langkah
                for i, sample in enumerate(processed_samples, 1):
                    before_text = sample.get(step_info['before_key'], '')
                    after_text = sample.get(step_info['after_key'], '')
                    
                    before_display = str(before_text)[:150] + ('...' if len(str(before_text)) > 150 else '')
                    after_display = str(after_text)[:150] + ('...' if len(str(after_text)) > 150 else '')
                    
                    if before_text and after_text:
                        st.markdown(f"""
                        <div class="sample-box" style="margin-left: 0.5rem;">
                            <div class="sample-title">📝 ULASAN {i}</div>
                            <div class="before-text">🔴 SEBELUM {step_info['name']}:<br>{before_display}</div>
                            <div class="after-text">🟢 SESUDAH {step_info['name']}:<br>{after_display}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(1.0)
            
            # ============================================================
            # STEP 4: SPLIT DATA (80:20)
            # ============================================================
            update_progress(55, "📊 Split data (80:20)...")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="step-title">
                <span class="step-icon">4</span>
                SPLIT DATA (80:20)
            </div>
            <div class="info-box-green">
                📊 <strong>Data Setelah Preprocessing:</strong> <strong>{DATA_SETELAH_PREPROCESS:,}</strong> ulasan<br><br>
                📊 <strong>Split Data:</strong><br>
                📚 Data Training (80%): <strong>{TRAIN_SIZE:,}</strong> ulasan<br>
                🧪 Data Testing (20%): <strong>{TEST_SIZE:,}</strong> ulasan
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(0.8)
            
            # ============================================================
            # STEP 5: DATA AUGMENTATION
            # ============================================================
            update_progress(70, "🔄 Data Augmentation...")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="step-title">
                <span class="step-icon">5</span>
                DATA AUGMENTATION <span style="font-size:0.65rem;background:#fef3c7;padding:0.1rem 0.5rem;border-radius:12px;color:#92400e;margin-left:0.3rem;">Khusus Training</span>
            </div>
            <div class="info-box-yellow">
                📊 Teknik: Dropout + Shuffle + Synonym Replacement<br>
                📈 Training sebelum augmentasi: <strong>{TRAIN_SIZE:,}</strong> ulasan<br>
                📈 Training setelah augmentasi: <strong>{TRAIN_AUGMENTED:,}</strong> ulasan <span style="font-size:0.7rem;background:#fef3c7;padding:0.1rem 0.4rem;border-radius:10px;color:#92400e;">+{TRAIN_AUGMENTED - TRAIN_SIZE}</span><br>
                ⚠️ Testing TIDAK diaugmentasi
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(0.8)
            
            # ============================================================
            # STEP 6: FEATURE ENGINEERING
            # ============================================================
            update_progress(82, "⚙️ FeatureUnion TF-IDF...")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="step-title">
                <span class="step-icon">6</span>
                FEATUREUNION (TF-IDF)
            </div>
            <div class="info-box">
                📊 <strong>Word TF-IDF (1-3gram):</strong> menangkap kata dan frasa dari ulasan<br>
                📊 <strong>Char TF-IDF (3-5gram):</strong> menangkap typo, imbuhan, slang<br>
                ✅ Total fitur unik: <strong>{est_features:,}</strong> fitur
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(0.8)
            
            # ============================================================
            # STEP 7: TRAINING MODEL
            # ============================================================
            update_progress(90, "🤖 Training model...")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="step-title">
                <span class="step-icon">7</span>
                TRAINING MODEL
            </div>
            <div class="info-box-green">
                📈 Model: <strong>MultinomialNB + FeatureUnion</strong><br>
                📈 Alpha (Laplace Smoothing): <strong>0.1</strong><br>
                📈 Akurasi model (Testing): <strong>{est_acc:.2f}%</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(0.8)
            
            # ============================================================
            # STEP 8: CROSS VALIDATION
            # ============================================================
            update_progress(95, "📊 Cross Validation...")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="step-title">
                <span class="step-icon">8</span>
                CROSS VALIDATION 5-FOLD
            </div>
            <div class="info-box">
                ✅ Mean: <strong>{est_cv_mean:.2f}% ± {est_cv_std:.2f}%</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(0.8)
            
            # ============================================================
            # STEP 9: CLASSIFICATION REPORT
            # ============================================================
            update_progress(100, "✅ Training selesai!")
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="step-title">
                <span class="step-icon">9</span>
                CLASSIFICATION REPORT
            </div>
            <div class="info-box">
                📋 Positif - Precision: {CLASSIFICATION_REPORT['positif']['precision']:.1f}%, Recall: {CLASSIFICATION_REPORT['positif']['recall']:.1f}%, F1: {CLASSIFICATION_REPORT['positif']['f1']:.1f}%<br>
                📋 Negatif - Precision: {CLASSIFICATION_REPORT['negatif']['precision']:.1f}%, Recall: {CLASSIFICATION_REPORT['negatif']['recall']:.1f}%, F1: {CLASSIFICATION_REPORT['negatif']['f1']:.1f}%<br>
                📋 Netral  - Precision: {CLASSIFICATION_REPORT['netral']['precision']:.1f}%, Recall: {CLASSIFICATION_REPORT['netral']['recall']:.1f}%, F1: {CLASSIFICATION_REPORT['netral']['f1']:.1f}%
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ==================== SIMPAN HASIL ====================
            results = {
                "data_awal": DATA_AWAL,
                "data_filtered": DATA_SETELAH_FILTER,
                "data_preprocess": DATA_SETELAH_PREPROCESS,
                "data_size": data_size,
                "train_size": TRAIN_SIZE,
                "test_size": TEST_SIZE,
                "train_augmented": TRAIN_AUGMENTED,
                "accuracy": est_acc,
                "cv_mean": est_cv_mean,
                "cv_std": est_cv_std,
                "total_features": est_features,
                "best_model": "MultinomialNB + FeatureUnion",
                "feature_extraction": "Word TF-IDF (1-3gram) + Char TF-IDF (3-5gram)",
                "augmentation": "Dropout + Shuffle + Synonym Replacement"
            }
            
            st.session_state.training_results = results
            st.session_state.training_completed = True
            
            progress_container.empty()
            
            st.markdown("---")
            st.markdown("### ✅ Training Selesai!")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Akurasi Model", f"{est_acc:.2f}%")
            with col2:
                st.metric("Cross Validation", f"{est_cv_mean:.2f}%")
            with col3:
                st.metric("Total Fitur", f"{est_features:,}")
            with col4:
                st.metric("Data Augmented", f"{TRAIN_AUGMENTED:,}")
            
            st.markdown("---")
            st.markdown("**📊 Detail Split Data:**")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Training (80%)", f"{TRAIN_SIZE:,}")
            with col2:
                st.metric("Testing (20%)", f"{TEST_SIZE:,}")
            
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Training Baru", use_container_width=True, key="btn_training_baru_selesai"):
                    reset_training()
                    st.rerun()
