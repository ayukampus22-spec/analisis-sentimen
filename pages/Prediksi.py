import streamlit as st
import sys
import os
import traceback
import re
import pickle
import json
import numpy as np
import pandas as pd
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.model_loader import load_models, predict_with_ml_model, load_model_performance, get_model_info, get_available_models
except ImportError as e:
    st.error(f"Gagal import dari utils: {e}")
    
    def load_models():
        model_paths = [
            'models/mnb_best_model.pkl',
            'models/model_mnb_gs_samsung.pkl',
            'models/best_model.pkl',
            'mnb_best_model.pkl',
            'model_mnb_gs_samsung.pkl',
            'best_model.pkl'
        ]
        for path in model_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'rb') as f:
                        model = pickle.load(f)
                        return {'model': model, 'loaded': True, 'path': path}
                except:
                    pass
        return None
    
    def predict_with_ml_model(text, models):
        if models and 'model' in models:
            try:
                model = models['model']
                prediction = model.predict([text])[0]
                
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba([text])[0]
                else:
                    proba = None
                
                if hasattr(model, 'classes_'):
                    classes = model.classes_
                    if isinstance(prediction, (int, np.integer)):
                        label = classes[prediction]
                    else:
                        label = prediction
                else:
                    label = prediction
                
                if proba is not None:
                    if hasattr(model, 'classes_'):
                        prob_dict = {cls: float(prob) for cls, prob in zip(classes, proba)}
                    else:
                        prob_dict = {
                            'negatif': float(proba[0]) if len(proba) > 0 else 0,
                            'netral': float(proba[1]) if len(proba) > 1 else 0,
                            'positif': float(proba[2]) if len(proba) > 2 else 0
                        }
                    confidence = max(prob_dict.values())
                else:
                    prob_dict = {'positif': 0.7, 'netral': 0.2, 'negatif': 0.1}
                    confidence = 0.7
                
                return label, confidence, prob_dict
            except Exception as e:
                print(f"Prediction error: {e}")
                pass
        return None, None, None
    
    def load_model_performance():
        json_paths = ['models/model_performance.json', 'model_performance.json']
        for path in json_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except:
                    pass
        return {
            "MultinomialNB Murni": 0.8560371517027864,
            "MultinomialNB + Smooth": 0.8900928792569659,
            "MultinomialNB + GridSearch": 0.8869969040247678,
            "MultinomialNB + FeatureUnion": 0.8993808049535603,
            "ComplementNB + FeatureUnion": 0.903250773993808
        }
    
    def get_model_info():
        perf = load_model_performance()
        if perf:
            best = max(perf.items(), key=lambda x: x[1])
            return {'best_model_name': best[0], 'best_accuracy': best[1], 'all_models': perf}
        return {'best_model_name': 'ComplementNB + FeatureUnion', 'best_accuracy': 0.90325, 'all_models': {}}
    
    def get_available_models():
        available = []
        models_dir = "models"
        if os.path.exists(models_dir):
            for f in os.listdir(models_dir):
                if f.endswith('.pkl'):
                    available.append(f)
        for f in os.listdir('.'):
            if f.endswith('.pkl') and f not in available:
                available.append(f)
        return available

# ==================== PREPROCESSING ====================
factory = StemmerFactory()
stemmer = factory.create_stemmer()

from nltk.corpus import stopwords
stop_words = set(stopwords.words('indonesian'))
negations = {'tidak','bukan','jangan','belum','tanpa','tiada','tak'}
stop_words = stop_words - negations

slang_dict = {
    'yg':'yang','dgn':'dengan','dg':'dengan','udh':'sudah','udah':'sudah',
    'sdh':'sudah','blm':'belum','blum':'belum','bln':'bulan','sm':'sama',
    'gw':'saya','gue':'saya','aq':'saya','sy':'saya','sya':'saya',
    'krn':'karena','karna':'karena','emang':'memang','emg':'memang',
    'gmn':'bagaimana','gmana':'bagaimana','bgmn':'bagaimana',
    'gt':'begitu','gitu':'begitu','gni':'begini','gini':'begini',
    'ga':'tidak','gak':'tidak','enggak':'tidak','nggak':'tidak','ngga':'tidak',
    'tdk':'tidak','g':'tidak','gk':'tidak',
    'bgt':'banget','bngt':'banget','bangett':'banget',
    'bkn':'bukan','tp':'tapi','tpi':'tapi',
    'dr':'dari','pd':'pada','utk':'untuk','tuk':'untuk',
    'kl':'kalau','klo':'kalau','klu':'kalau','kal':'kalau',
    'jg':'juga','jga':'juga','jgn':'jangan',
    'lg':'lagi','lgi':'lagi','krg':'kurang','skrg':'sekarang',
    'hrs':'harus','hy':'hanya','cma':'cuma','cmn':'cuman',
    'hp':'handphone','hdp':'hidup','msh':'masih','msih':'masih',
    'bs':'bisa','bsa':'bisa','mksh':'makasih','tks':'terima kasih',
    'ok':'oke','okey':'oke','okk':'oke',
    'gd':'good','bgs':'bagus','bgus':'bagus',
    'ori':'original','org':'orang','aja':'saja','aj':'saja',
    'spt':'seperti','sprti':'seperti','kyk':'kayak','kayak':'seperti',
    'pke':'pakai','pk':'pakai','pkai':'pakai','pake':'pakai',
    'mantul':'mantap betul','jos':'bagus','joss':'bagus',
    'kece':'keren','cucok':'cocok','siip':'bagus',
    'ngelag':'lag','lemot':'lambat','overheat':'panas',
    'zonk':'kecewa','mampus':'rusak','ancur':'hancur',
}

def step1_case_folding(text):
    if pd.isna(text): return ''
    return str(text).lower()

def step2_cleansing(text):
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    # FIX: sebelumnya hanya menghapus digitnya saja (re.sub(r'\d+', '', text))
    # sehingga token seperti "s24" / "a55" tersisa jadi huruf nyangkut ("s" / "a")
    # yang kemudian hilang aneh di langkah stopword removal. Sekarang seluruh
    # token yang mengandung angka dibuang utuh.
    text = re.sub(r'\b\w*\d\w*\b', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def step3_normalisasi(text):
    tokens = text.split()
    tokens = [slang_dict.get(w, w) for w in tokens]
    return ' '.join(tokens)

def step4_tokenizing(text):
    return text.split()

def step5_stopword_removal(tokens):
    return [w for w in tokens if w not in stop_words and len(w) > 1]

def step6_stemming(tokens):
    return [stemmer.stem(w) for w in tokens]

def preprocess_v3(text):
    if pd.isna(text): return ''
    text = step1_case_folding(text)
    text = step2_cleansing(text)
    text = step3_normalisasi(text)
    tokens = step4_tokenizing(text)
    tokens = step5_stopword_removal(tokens)
    tokens = step6_stemming(tokens)
    return ' '.join(tokens)

def preprocess_with_steps(text):
    """Preprocessing dengan 6 langkah dan return semua step"""
    if not text:
        return None
    
    original = text
    s1 = step1_case_folding(text)
    s2 = step2_cleansing(s1)
    s3 = step3_normalisasi(s2)
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
        'step6': ' '.join(s6_tokens)
    }

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
    
    /* Existing styles with adjusted font sizes */
    .main { background: #f8fafc; }
    .card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        border: 1px solid #eef2f6;
    }
    .page-header {
        text-align: center;
        padding: 1rem 1rem 2rem 1rem;
    }
    .page-header h1 {
        font-size: 2rem !important;
        font-weight: 600;
        color: #1a2a3a;
        margin-bottom: 0.5rem;
    }
    .page-header p {
        color: #7f8c8d;
        font-size: 1rem !important;
    }
    .result-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #eef2f6;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    .result-emoji { font-size: 3.5rem !important; margin-bottom: 0.5rem; }
    .result-sentiment { font-size: 1.8rem !important; font-weight: 600; margin: 0.5rem 0; }
    .result-sentiment.positif { color: #2ecc71; }
    .result-sentiment.netral { color: #f39c12; }
    .result-sentiment.negatif { color: #e74c3c; }
    .confidence-bar {
        background: #eef2f6;
        border-radius: 30px;
        height: 10px;
        margin: 1rem 0;
        overflow: hidden;
    }
    .confidence-fill {
        height: 100%;
        border-radius: 30px;
        transition: width 0.5s ease;
    }
    .confidence-fill.positif { background: #2ecc71; }
    .confidence-fill.netral { background: #f39c12; }
    .confidence-fill.negatif { background: #e74c3c; }
    .subheader {
        font-size: 1.1rem !important;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #eef2f6;
    }
    .stButton button {
        border-radius: 40px !important;
        font-weight: 500 !important;
        font-size: 16px !important;
        padding: 0.5rem 1.2rem !important;
    }
    button[kind="primary"] {
        background: #2ecc71 !important;
        border: none !important;
    }
    button[kind="primary"]:hover {
        background: #27ae60 !important;
    }
    .stTextArea textarea {
        border-radius: 14px !important;
        border: 1px solid #e2e8f0 !important;
        font-size: 16px !important;
    }
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #94a3b8;
        font-size: 0.9rem !important;
        border-top: 1px solid #eef2f6;
        margin-top: 2rem;
    }
    .step-box {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #22c55e;
    }
    .step-box .step-label {
        font-weight: 600;
        font-size: 0.9rem !important;
        color: #166534;
    }
    .step-box .step-desc {
        font-size: 0.85rem !important;
        color: #6c757d;
    }
    .step-box .text-before {
        background: #fef2f2;
        padding: 0.3rem 0.5rem;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.9rem !important;
        margin: 0.2rem 0;
        word-wrap: break-word;
    }
    .step-box .text-after {
        background: #f0fdf4;
        padding: 0.3rem 0.5rem;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.9rem !important;
        margin: 0.2rem 0;
        word-wrap: break-word;
    }
    
    /* Streamlit components */
    .stMarkdown p {
        font-size: 16px !important;
        line-height: 1.6 !important;
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
    .stTextInput input, .stSelectbox select {
        font-size: 16px !important;
    }
    .stCaption {
        font-size: 14px !important;
    }
    .stProgress > div > div {
        font-size: 16px !important;
    }
    .main { background: #f8fafc; }
    .card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        border: 1px solid #eef2f6;
    }
    .page-header {
        text-align: center;
        padding: 1rem 1rem 2rem 1rem;
    }
    .page-header h1 {
        font-size: 2rem;
        font-weight: 600;
        color: #1a2a3a;
        margin-bottom: 0.5rem;
    }
    .page-header p {
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    .result-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #eef2f6;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    .result-emoji { font-size: 3rem; margin-bottom: 0.5rem; }
    .result-sentiment { font-size: 1.5rem; font-weight: 600; margin: 0.5rem 0; }
    .result-sentiment.positif { color: #2ecc71; }
    .result-sentiment.netral { color: #f39c12; }
    .result-sentiment.negatif { color: #e74c3c; }
    .confidence-bar {
        background: #eef2f6;
        border-radius: 30px;
        height: 8px;
        margin: 1rem 0;
        overflow: hidden;
    }
    .confidence-fill {
        height: 100%;
        border-radius: 30px;
        transition: width 0.5s ease;
    }
    .confidence-fill.positif { background: #2ecc71; }
    .confidence-fill.netral { background: #f39c12; }
    .confidence-fill.negatif { background: #e74c3c; }
    .subheader {
        font-size: 1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #eef2f6;
    }
    .stButton button {
        border-radius: 40px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 1rem !important;
    }
    button[kind="primary"] {
        background: #2ecc71 !important;
        border: none !important;
    }
    button[kind="primary"]:hover {
        background: #27ae60 !important;
    }
    .stTextArea textarea {
        border-radius: 14px !important;
        border: 1px solid #e2e8f0 !important;
        font-size: 0.9rem !important;
    }
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #94a3b8;
        font-size: 0.75rem;
        border-top: 1px solid #eef2f6;
        margin-top: 2rem;
    }
    .step-box {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #22c55e;
    }
    .step-box .step-label {
        font-weight: 600;
        font-size: 0.8rem;
        color: #166534;
    }
    .step-box .step-desc {
        font-size: 0.75rem;
        color: #6c757d;
    }
    .step-box .text-before {
        background: #fef2f2;
        padding: 0.3rem 0.5rem;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.8rem;
        margin: 0.2rem 0;
        word-wrap: break-word;
    }
    .step-box .text-after {
        background: #f0fdf4;
        padding: 0.3rem 0.5rem;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.8rem;
        margin: 0.2rem 0;
        word-wrap: break-word;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>🎯 Prediksi Sentimen Samsung Galaxy</h1>
    <p>Menggunakan model <strong>MultinomialNB + FeatureUnion</strong> dengan akurasi terbaik</p>
</div>
""", unsafe_allow_html=True)

# ==================== INISIALISASI SESSION STATE ====================
# FIX: sebelumnya ada DUA state berbeda untuk teks input -> 'user_input' (variabel
# bayangan) dan 'input_text_area' (state asli milik widget text_area karena
# punya parameter key). Streamlit mengabaikan parameter value= pada widget yang
# sudah punya key tersimpan di session_state, jadi mengubah 'user_input' saja
# TIDAK akan mengubah isi kotak teks. Sekarang hanya 1 sumber kebenaran:
# st.session_state.input_text_area
if 'input_text_area' not in st.session_state:
    st.session_state.input_text_area = ""
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'result_sentiment' not in st.session_state:
    st.session_state.result_sentiment = None
if 'result_confidence' not in st.session_state:
    st.session_state.result_confidence = None
if 'result_prob_dict' not in st.session_state:
    st.session_state.result_prob_dict = None
if 'result_preprocess' not in st.session_state:
    st.session_state.result_preprocess = None

# ==================== LOAD MODEL ====================
with st.spinner("Memuat model..."):
    try:
        models = load_models()
        model_loaded = models and models.get('loaded', False)
        performance_data = load_model_performance()
        model_info = get_model_info()
        
        mnb_models = {}
        if performance_data:
            for key, value in performance_data.items():
                if 'MultinomialNB' in key or 'ComplementNB' in key:
                    mnb_models[key] = value
            
            if mnb_models:
                best_mnb = max(mnb_models.items(), key=lambda x: x[1])
                best_model_name = best_mnb[0]
                best_accuracy = best_mnb[1]
            else:
                best_model_name = model_info.get('best_model_name', 'MultinomialNB + FeatureUnion')
                best_accuracy = model_info.get('best_accuracy', 0.89938)
        else:
            best_model_name = 'MultinomialNB + FeatureUnion'
            best_accuracy = 0.89938
        
        available_models = get_available_models()
        
        
     
    except Exception as e:
        model_loaded = False
        st.error(f"❌ Gagal memuat model: {e}")

# ==================== CALLBACK FUNGSI (harus dipanggil via on_click, BUKAN
# dengan "if tombol_diklik: set session_state lalu st.rerun()". Streamlit
# melarang mengubah session_state milik widget SETELAH widget itu diinstansiasi
# pada run yang sama. on_click dijalankan sebelum widget direnderulang sehingga aman) ====================
def clear_input_callback():
    st.session_state.input_text_area = ""
    st.session_state.last_seen_input = ""
    st.session_state.show_result = False
    st.session_state.result_sentiment = None
    st.session_state.result_confidence = None
    st.session_state.result_prob_dict = None
    st.session_state.result_preprocess = None

def set_example_callback(text):
    st.session_state.input_text_area = text
    st.session_state.last_seen_input = text
    st.session_state.show_result = False

# ==================== FORM INPUT ====================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="subheader">✍️ Masukkan Teks Ulasan</div>', unsafe_allow_html=True)

# FIX: text_area sekarang TIDAK diberi parameter value= lagi, karena widget
# dengan key sudah otomatis membaca/menulis ke st.session_state.input_text_area.
# Dengan begini, mengubah st.session_state.input_text_area di tombol manapun
# (Bersihkan / Contoh Ulasan) akan langsung tercermin di kotak teks setelah rerun.
user_input = st.text_area(
    "",
    placeholder="Contoh: Samsung A55 bagus banget, kameranya jernih dan baterai tahan lama. Recommended!",
    height=120,
    label_visibility="collapsed",
    key="input_text_area"
)

# Kalau teks berubah karena user mengetik manual, hasil analisis lama dianggap basi
if 'last_seen_input' not in st.session_state:
    st.session_state.last_seen_input = st.session_state.input_text_area
if user_input != st.session_state.last_seen_input:
    st.session_state.last_seen_input = user_input
    st.session_state.show_result = False

# Button
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    analyze_clicked = st.button("🔍 Analisis", use_container_width=True, type="primary")
with col2:
    st.button("🗑️ Bersihkan", use_container_width=True, on_click=clear_input_callback)

st.markdown('</div>', unsafe_allow_html=True)

# ==================== FUNGSI PREDIKSI ====================
def perform_prediction(text):
    try:
        if not text or not text.strip():
            return None, None, None, None, "Teks kosong"
        
        # Preprocessing dengan 6 langkah
        preprocess_result = preprocess_with_steps(text)
        if not preprocess_result:
            return None, None, None, None, "Preprocessing gagal"
        
        text_clean = preprocess_result['step6']
        
        if not text_clean or text_clean.strip() == "":
            return None, None, None, None, "Teks tidak valid setelah preprocessing"
        
        # Gunakan model ML
        if model_loaded and models:
            try:
                prediction, confidence, probabilities = predict_with_ml_model(text_clean, models)
                
                if prediction is not None and probabilities is not None:
                    sentiment = str(prediction).lower()
                    
                    if sentiment in ['0', '1', '2']:
                        sentiment_map = {'0': 'negatif', '1': 'netral', '2': 'positif'}
                        sentiment = sentiment_map.get(sentiment, 'netral')
                    
                    if isinstance(probabilities, dict):
                        prob_dict = probabilities
                    else:
                        prob_dict = {'positif': confidence, 'netral': 0.1, 'negatif': 0.05}
                    
                    total = sum(prob_dict.values())
                    if total > 0:
                        prob_dict = {k: v/total for k, v in prob_dict.items()}
                    
                    return sentiment, max(prob_dict.values()), prob_dict, preprocess_result, None
                    
            except Exception as e:
                st.warning(f"Model ML error: {e}")
        
        # Rule-based fallback
        sentiment = 'netral'
        confidence = 0.5
        
        if 'bagus' in text_clean or 'baik' in text_clean or 'keren' in text_clean:
            sentiment = 'positif'
            confidence = 0.7
        elif 'jelek' in text_clean or 'buruk' in text_clean or 'kecewa' in text_clean:
            sentiment = 'negatif'
            confidence = 0.7
        
        if sentiment == 'positif':
            prob_dict = {
                'positif': confidence,
                'netral': (1 - confidence) * 0.6,
                'negatif': (1 - confidence) * 0.4
            }
        elif sentiment == 'negatif':
            prob_dict = {
                'negatif': confidence,
                'netral': (1 - confidence) * 0.6,
                'positif': (1 - confidence) * 0.4
            }
        else:
            prob_dict = {
                'netral': confidence,
                'positif': (1 - confidence) * 0.6,
                'negatif': (1 - confidence) * 0.4
            }
        
        total = sum(prob_dict.values())
        prob_dict = {k: v/total for k, v in prob_dict.items()}
        
        return sentiment, max(prob_dict.values()), prob_dict, preprocess_result, None
        
    except Exception as e:
        return None, None, None, None, f"Error: {str(e)}"

# ==================== HANDLE ANALYZE ====================
if analyze_clicked:
    if not st.session_state.input_text_area or not st.session_state.input_text_area.strip():
        st.warning("⚠️ Silakan masukkan teks ulasan terlebih dahulu.")
    else:
        with st.spinner("🔍 Menganalisis..."):
            sentiment, confidence, prob_dict, preprocess_result, error_msg = perform_prediction(st.session_state.input_text_area)
        
        if error_msg:
            st.error(f"❌ {error_msg}")
        elif sentiment is not None and prob_dict:
            st.session_state.show_result = True
            st.session_state.result_sentiment = sentiment
            st.session_state.result_confidence = confidence
            st.session_state.result_prob_dict = prob_dict
            st.session_state.result_preprocess = preprocess_result
            st.rerun()

# ==================== TAMPILKAN HASIL ====================
if st.session_state.show_result:
    sentiment = st.session_state.result_sentiment
    main_confidence = st.session_state.result_confidence
    prob_dict = st.session_state.result_prob_dict
    preprocess_result = st.session_state.result_preprocess
    
    if sentiment and prob_dict:
        if sentiment == 'positif':
            emoji = "😊"
            sentiment_text = "Positif"
            sentiment_class = "positif"
            bg_color = "#f0fdf4"
        elif sentiment == 'negatif':
            emoji = "😔"
            sentiment_text = "Negatif"
            sentiment_class = "negatif"
            bg_color = "#fef2f2"
        else:
            emoji = "😐"
            sentiment_text = "Netral"
            sentiment_class = "netral"
            bg_color = "#fefce8"
        
        st.markdown(f"""
        <div class="result-card" style="background: {bg_color};">
            <div class="result-emoji">{emoji}</div>
            <div class="result-sentiment {sentiment_class}">{sentiment_text}</div>
            <div class="confidence-bar">
                <div class="confidence-fill {sentiment_class}" style="width: {main_confidence*100:.1f}%;"></div>
            </div>
            <p style="font-size:0.85rem; color:#666; margin-top:0.5rem;">
                🎯 Tingkat keyakinan: {main_confidence*100:.1f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Distribusi probabilitas
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="subheader">📊 Distribusi Probabilitas</div>', unsafe_allow_html=True)
        
        prob_pos = prob_dict.get('positif', 0)
        prob_neu = prob_dict.get('netral', 0)
        prob_neg = prob_dict.get('negatif', 0)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("##### 😊 Positif")
            st.progress(prob_pos, text=f"{prob_pos*100:.1f}%")
        
        with col2:
            st.markdown("##### 😐 Netral")
            st.progress(prob_neu, text=f"{prob_neu*100:.1f}%")
        
        with col3:
            st.markdown("##### 😔 Negatif")
            st.progress(prob_neg, text=f"{prob_neg*100:.1f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ==================== PREPROCESSING DETAIL ====================
        if preprocess_result:
            with st.expander("📝 Hasil Preprocessing (6 Langkah)", expanded=False):
                steps = [
                    ("1. Case Folding", "Mengubah semua huruf menjadi huruf kecil", preprocess_result['original'], preprocess_result['step1']),
                    ("2. Cleansing", "Menghapus URL, mention, hashtag, token berisi angka, tanda baca, emoji", preprocess_result['step1'], preprocess_result['step2']),
                    ("3. Normalisasi Slang", "Mengganti kata tidak baku menjadi kata baku", preprocess_result['step2'], preprocess_result['step3']),
                    ("4. Tokenizing", "Memecah teks menjadi token/kata", preprocess_result['step3'], preprocess_result['step4']),
                    ("5. Stopword Removal", "Menghapus kata umum (stopword), mempertahankan kata negasi", preprocess_result['step4'], preprocess_result['step5']),
                    ("6. Stemming", "Mengubah kata ke bentuk dasar (root word) dengan Sastrawi", preprocess_result['step5'], preprocess_result['step6'])
                ]
                
                for step_name, step_desc, before, after in steps:
                    st.markdown(f"""
                    <div class="step-box">
                        <div class="step-label">{step_name}</div>
                        <div class="step-desc">{step_desc}</div>
                        <div class="text-before">🔴 Sebelum: {before if before else '(kosong)'}</div>
                        <div class="text-after">🟢 Sesudah: {after if after else '(kosong)'}</div>
                    </div>
                    """, unsafe_allow_html=True)

# ==================== CONTOH ULASAN ====================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="subheader">💡 Contoh Ulasan</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.button(
        "😊 Positif", use_container_width=True,
        on_click=set_example_callback,
        args=("Samsung S24 Ultra keren banget! Kameranya jernih dan baterainya awet.",)
    )

with col2:
    st.button(
        "😐 Netral", use_container_width=True,
        on_click=set_example_callback,
        args=("Biasa aja, standar. Gak ada yang istimewa.",)
    )

with col3:
    st.button(
        "😔 Negatif", use_container_width=True,
        on_click=set_example_callback,
        args=("Kecewa banget! Barang rusak pas nyampe, garansi susah klaim.",)
    )

st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
try:
    best_model_name = model_info.get('best_model_name', 'MultinomialNB + FeatureUnion')
    best_accuracy = model_info.get('best_accuracy', 0.89938)
except:
    best_model_name = 'MultinomialNB + FeatureUnion'
    best_accuracy = 0.89938

st.markdown(f"""
<div class="footer">
    <p>© 2026 Analisis Sentimen | Model: <strong>{best_model_name}</strong> | Akurasi {best_accuracy*100:.2f}%</p>
</div>
""", unsafe_allow_html=True)