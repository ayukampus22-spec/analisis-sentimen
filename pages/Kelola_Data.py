import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

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
    
    .main > div {
        padding-top: 0.5rem;
    }
    
    .header {
        text-align: center;
        padding: 1.25rem 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 1.25rem;
        border: 1px solid #e9ecef;
    }
    .header h1 {
        font-size: 1.5rem !important;
        font-weight: 600;
        color: #212529;
        margin: 0;
    }
    .header p {
        color: #495057;
        font-size: 0.95rem !important;
        margin: 0.15rem 0 0 0;
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
    
    .stat-box {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .stat-number {
        font-size: 1.5rem !important;
        font-weight: 700;
        color: #22c55e;
    }
    .stat-label {
        font-size: 0.85rem !important;
        color: #6c757d;
        margin-top: 0.1rem;
    }
    
    .banner-info {
        background: #f1f8ff;
        border-left: 3px solid #3b82f6;
        padding: 0.6rem 0.9rem;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        font-size: 0.95rem !important;
        color: #1a3a6b;
    }
    .banner-success {
        background: #f0fdf4;
        border-left: 3px solid #22c55e;
        padding: 0.6rem 0.9rem;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        font-size: 0.95rem !important;
        color: #166534;
    }
    .banner-warning {
        background: #fffbeb;
        border-left: 3px solid #eab308;
        padding: 0.6rem 0.9rem;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        font-size: 0.95rem !important;
        color: #92400e;
    }
    .banner-empty {
        text-align: center;
        padding: 2rem 1rem;
    }
    .banner-empty h3 {
        font-size: 1.2rem !important;
        color: #212529;
        margin: 0.5rem 0 0.25rem 0;
    }
    .banner-empty p {
        color: #6c757d;
        font-size: 0.95rem !important;
        margin: 0;
    }
    .banner-empty .icon {
        font-size: 3.5rem !important;
    }
    
    .edit-panel {
        background: #fefce8;
        border: 1px solid #eab308;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.75rem 0;
    }
    .edit-panel-title {
        font-weight: 600;
        color: #92400e;
        font-size: 1rem !important;
        margin-bottom: 0.5rem;
    }
    
    .delete-box {
        background: #fef2f2;
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.75rem 0;
    }
    .delete-box h4 {
        color: #dc2626;
        font-size: 1.1rem !important;
        margin: 0 0 0.25rem 0;
    }
    .delete-box p {
        font-size: 0.95rem !important;
        color: #495057;
        margin: 0.15rem 0;
    }
    .delete-box .small {
        font-size: 0.85rem !important;
        color: #6c757d;
    }
    
    .delete-all-box {
        background: #fef2f2;
        border: 2px solid #dc2626;
        border-radius: 8px;
        padding: 1.25rem;
        text-align: center;
        margin: 0.75rem 0;
    }
    .delete-all-box h4 {
        color: #dc2626;
        font-size: 1.2rem !important;
        margin: 0 0 0.25rem 0;
    }
    .delete-all-box p {
        font-size: 0.95rem !important;
        color: #495057;
        margin: 0.15rem 0;
    }
    .delete-all-box .small {
        font-size: 0.85rem !important;
        color: #6c757d;
    }
    
    .stButton button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 16px !important;
        padding: 0.5rem 1.2rem !important;
    }
    .stButton button[kind="primary"] {
        background: #22c55e !important;
        color: white !important;
        border: none !important;
    }
    .stButton button[kind="primary"]:hover {
        background: #16a34a !important;
    }
    .btn-danger {
        background: #ef4444 !important;
        color: white !important;
        border: none !important;
    }
    .btn-danger:hover {
        background: #dc2626 !important;
    }
    .btn-warning {
        background: #eab308 !important;
        color: white !important;
        border: none !important;
    }
    .btn-warning:hover {
        background: #ca8a04 !important;
    }
    
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        font-size: 16px !important;
    }
    
    .footer {
        text-align: center;
        padding: 1rem;
        color: #6c757d;
        font-size: 0.85rem !important;
        border-top: 1px solid #e9ecef;
        margin-top: 1.25rem;
    }
    .footer p {
        margin: 0.1rem 0;
    }
    
    hr {
        margin: 0.75rem 0;
        border-color: #e9ecef;
    }
    .caption {
        font-size: 0.85rem !important;
        color: #6c757d;
        margin-top: 0.25rem;
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
    .stCaption {
        font-size: 14px !important;
    }
    /* Base */
    .main > div {
        padding-top: 0.5rem;
    }
    
    /* Header */
    .header {
        text-align: center;
        padding: 1.25rem 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 1.25rem;
        border: 1px solid #e9ecef;
    }
    .header h1 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #212529;
        margin: 0;
    }
    .header p {
        color: #495057;
        font-size: 0.85rem;
        margin: 0.15rem 0 0 0;
    }
    
    /* Cards */
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
    
    /* Stats */
    .stat-box {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .stat-number {
        font-size: 1.5rem;
        font-weight: 700;
        color: #22c55e;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #6c757d;
        margin-top: 0.1rem;
    }
    
    /* Banners */
    .banner-info {
        background: #f1f8ff;
        border-left: 3px solid #3b82f6;
        padding: 0.6rem 0.9rem;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        font-size: 0.85rem;
        color: #1a3a6b;
    }
    .banner-success {
        background: #f0fdf4;
        border-left: 3px solid #22c55e;
        padding: 0.6rem 0.9rem;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        font-size: 0.85rem;
        color: #166534;
    }
    .banner-warning {
        background: #fffbeb;
        border-left: 3px solid #eab308;
        padding: 0.6rem 0.9rem;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        font-size: 0.85rem;
        color: #92400e;
    }
    .banner-empty {
        text-align: center;
        padding: 2rem 1rem;
    }
    .banner-empty h3 {
        font-size: 1.1rem;
        color: #212529;
        margin: 0.5rem 0 0.25rem 0;
    }
    .banner-empty p {
        color: #6c757d;
        font-size: 0.85rem;
        margin: 0;
    }
    .banner-empty .icon {
        font-size: 3rem;
    }
    
    /* Edit Panel */
    .edit-panel {
        background: #fefce8;
        border: 1px solid #eab308;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.75rem 0;
    }
    .edit-panel-title {
        font-weight: 600;
        color: #92400e;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    /* Delete Confirm */
    .delete-box {
        background: #fef2f2;
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.75rem 0;
    }
    .delete-box h4 {
        color: #dc2626;
        font-size: 1rem;
        margin: 0 0 0.25rem 0;
    }
    .delete-box p {
        font-size: 0.9rem;
        color: #495057;
        margin: 0.15rem 0;
    }
    .delete-box .small {
        font-size: 0.8rem;
        color: #6c757d;
    }
    
    .delete-all-box {
        background: #fef2f2;
        border: 2px solid #dc2626;
        border-radius: 8px;
        padding: 1.25rem;
        text-align: center;
        margin: 0.75rem 0;
    }
    .delete-all-box h4 {
        color: #dc2626;
        font-size: 1.1rem;
        margin: 0 0 0.25rem 0;
    }
    .delete-all-box p {
        font-size: 0.9rem;
        color: #495057;
        margin: 0.15rem 0;
    }
    .delete-all-box .small {
        font-size: 0.8rem;
        color: #6c757d;
    }
    
    /* Buttons */
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
    .btn-danger {
        background: #ef4444 !important;
        color: white !important;
        border: none !important;
    }
    .btn-danger:hover {
        background: #dc2626 !important;
    }
    .btn-warning {
        background: #eab308 !important;
        color: white !important;
        border: none !important;
    }
    .btn-warning:hover {
        background: #ca8a04 !important;
    }
    
    /* Form elements */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        font-size: 0.9rem !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 2px rgba(34,197,94,0.1) !important;
    }
    .stSelectbox div[data-baseweb="select"]:focus {
        border-color: #22c55e !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #6c757d;
        font-size: 0.7rem;
        border-top: 1px solid #e9ecef;
        margin-top: 1.25rem;
    }
    .footer p {
        margin: 0.1rem 0;
    }
    
    /* Misc */
    hr {
        margin: 0.75rem 0;
        border-color: #e9ecef;
    }
    .caption {
        font-size: 0.8rem;
        color: #6c757d;
        margin-top: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="header">
    <h1>Kelola Data</h1>
    <p>Edit, hapus, dan kelola data ulasan yang telah di-scrape</p>
</div>
""", unsafe_allow_html=True)

# ==================== INISIALISASI ====================
if 'scraped_df' not in st.session_state:
    st.session_state.scraped_df = None
if 'scraping_done' not in st.session_state:
    st.session_state.scraping_done = False
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'delete_index' not in st.session_state:
    st.session_state.delete_index = None
if 'delete_confirm' not in st.session_state:
    st.session_state.delete_confirm = False
if 'delete_all_confirm' not in st.session_state:
    st.session_state.delete_all_confirm = False

# ==================== FUNGSI ====================
def get_data_stats(df):
    if df is None or df.empty:
        return {"total": 0, "rating_avg": 0, "unique_reviewers": 0}
    
    stats = {"total": len(df), "rating_avg": 0, "unique_reviewers": 0}
    
    if 'Rating' in df.columns:
        try:
            ratings = df['Rating'].str.extract('(\d+)').astype(float)
            if not ratings.empty:
                stats["rating_avg"] = ratings.mean().iloc[0]
        except:
            pass
    
    if 'Reviewer' in df.columns:
        stats["unique_reviewers"] = df['Reviewer'].nunique()
    
    return stats

def cancel_edit():
    st.session_state.edit_index = None
    st.session_state.edit_mode = False

def cancel_delete():
    st.session_state.delete_index = None
    st.session_state.delete_confirm = False

# ==================== DATA ====================
df = st.session_state.scraped_df
has_data = df is not None and not df.empty
stats = get_data_stats(df)

# ==================== STATISTIK ====================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">Ringkasan Data</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{stats['total']:,}</div>
        <div class="stat-label">Total Ulasan</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{stats['rating_avg']:.1f} ★</div>
        <div class="stat-label">Rata-rata Rating</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{stats['unique_reviewers']:,}</div>
        <div class="stat-label">Reviewer Unik</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==================== CEK DATA ====================
if not has_data:
    st.markdown("""
    <div class="card banner-empty">
        <div class="icon">📭</div>
        <h3>Belum Ada Data</h3>
        <p>Lakukan scraping data terlebih dahulu di halaman <strong>Scraping</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Gunakan Sample Data", use_container_width=True, type="primary"):
            sample_reviewers = ["A***a", "B***i", "C***y", "D***n", "E***k"]
            sample_texts = [
                "Bagus banget, original dan cepat sampai",
                "Terima kasih, barang sesuai deskripsi",
                "Mantap, packing rapi dan aman",
                "Alhamdulillah, barang bagus",
                "Keren, recommended",
                "Cepat sampai, barang original",
                "Kecewa, barang rusak",
                "Lumayan oke untuk harga segini",
                "Biasa aja, standar",
                "Lengkap dan original, makasih"
            ]
            
            sample_data = []
            for i in range(15):
                sample_data.append({
                    'No': i + 1,
                    'Reviewer': random.choice(sample_reviewers),
                    'Rating': f"{random.choice([5,5,5,5,4,4,4,3])} ★",
                    'Ulasan': random.choice(sample_texts),
                    'Waktu': f"{random.randint(1,30)} hari lalu"
                })
            
            st.session_state.scraped_df = pd.DataFrame(sample_data)
            st.session_state.scraping_done = True
            st.rerun()
    
    st.stop()

# ==================== TAMPILKAN DATA ====================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">Data Ulasan</div>', unsafe_allow_html=True)

df_display = df.copy()
df_display.index = range(1, len(df_display) + 1)

show_limit = st.selectbox(
    "Tampilkan data",
    [10, 25, 50, 100, "Semua"],
    index=1,
    format_func=lambda x: f"{x} baris" if x != "Semua" else "Semua Data"
)

if show_limit != "Semua":
    display_df = df_display.head(int(show_limit))
else:
    display_df = df_display

st.dataframe(display_df, use_container_width=True, height=320)
st.caption(f"Menampilkan {len(display_df)} dari {len(df)} baris data")
st.markdown('</div>', unsafe_allow_html=True)

# ==================== PANEL EDIT/HAPUS ====================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">Edit atau Hapus Data</div>', unsafe_allow_html=True)

st.markdown('<div class="banner-info">Pilih nomor baris, lalu klik tombol Edit atau Hapus.</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    row_number = st.number_input(
        "Nomor Baris",
        min_value=1,
        max_value=len(df),
        value=1,
        step=1,
        key="row_selector"
    )

with col2:
    if st.button("✏️ Edit", use_container_width=True, type="primary"):
        st.session_state.edit_index = row_number - 1
        st.session_state.edit_mode = True
        st.session_state.delete_index = None
        st.rerun()

with col3:
    if st.button("🗑️ Hapus", use_container_width=True):
        st.session_state.delete_index = row_number - 1
        st.session_state.delete_confirm = False
        st.session_state.edit_index = None
        st.session_state.edit_mode = False
        st.rerun()

# ==================== PANEL EDIT ====================
if st.session_state.edit_mode and st.session_state.edit_index is not None:
    edit_idx = st.session_state.edit_index
    
    if edit_idx < len(df):
        row_data = df.iloc[edit_idx].to_dict()
        
        st.markdown("---")
        st.markdown(f"""
        <div class="edit-panel">
            <div class="edit-panel-title">Mengedit Baris #{edit_idx + 1}</div>
        """, unsafe_allow_html=True)
        
        with st.form(key="edit_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_reviewer = st.text_input(
                    "Reviewer", 
                    value=row_data.get('Reviewer', ''),
                    placeholder="Nama reviewer"
                )
                
                rating_options = ["1 ★", "2 ★", "3 ★", "4 ★", "5 ★"]
                current_rating = row_data.get('Rating', '5 ★')
                default_idx = rating_options.index(current_rating) if current_rating in rating_options else 4
                
                new_rating = st.selectbox(
                    "Rating",
                    options=rating_options,
                    index=default_idx
                )
            
            with col2:
                new_ulasan = st.text_area(
                    "Ulasan",
                    value=row_data.get('Ulasan', ''),
                    height=70,
                    placeholder="Teks ulasan"
                )
                
                new_waktu = st.text_input(
                    "Waktu",
                    value=row_data.get('Waktu', ''),
                    placeholder="Contoh: 2 hari lalu"
                )
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                submitted = st.form_submit_button("💾 Simpan", use_container_width=True, type="primary")
            
            with col_btn2:
                cancel = st.form_submit_button("Batal", use_container_width=True)
            
            with col_btn3:
                delete_btn = st.form_submit_button("🗑️ Hapus", use_container_width=True)
            
            if submitted:
                df.at[edit_idx, 'Reviewer'] = new_reviewer
                df.at[edit_idx, 'Rating'] = new_rating
                df.at[edit_idx, 'Ulasan'] = new_ulasan
                df.at[edit_idx, 'Waktu'] = new_waktu
                
                st.session_state.scraped_df = df
                cancel_edit()
                st.success("✅ Data berhasil diperbarui!")
                time.sleep(0.5)
                st.rerun()
            
            if cancel:
                cancel_edit()
                st.rerun()
            
            if delete_btn:
                df_cleaned = df.drop(edit_idx).reset_index(drop=True)
                st.session_state.scraped_df = df_cleaned
                cancel_edit()
                st.success(f"✅ Baris #{edit_idx + 1} berhasil dihapus!")
                time.sleep(0.5)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== HAPUS BARIS ====================
if st.session_state.delete_index is not None and not st.session_state.edit_mode:
    del_idx = st.session_state.delete_index
    
    if del_idx < len(df):
        row_data = df.iloc[del_idx].to_dict()
        
        st.markdown("---")
        
        if not st.session_state.delete_confirm:
            st.markdown(f"""
            <div class="delete-box">
                <h4>⚠️ Konfirmasi Hapus</h4>
                <p>Hapus baris <strong>#{del_idx + 1}</strong>?</p>
                <p class="small">"{str(row_data.get('Ulasan', ''))[:80]}..."</p>
                <p class="small" style="color:#999;">Tindakan ini tidak dapat dibatalkan.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("✅ Ya, Hapus", use_container_width=True, type="primary"):
                    st.session_state.delete_confirm = True
                    st.rerun()
            with col2:
                if st.button("Batal", use_container_width=True):
                    cancel_delete()
                    st.rerun()
        else:
            df_cleaned = df.drop(del_idx).reset_index(drop=True)
            st.session_state.scraped_df = df_cleaned
            st.session_state.delete_index = None
            st.session_state.delete_confirm = False
            st.success(f"✅ Baris #{del_idx + 1} berhasil dihapus!")
            time.sleep(0.5)
            st.rerun()

# ==================== HAPUS SEMUA ====================
st.markdown("---")
st.markdown("### Hapus Semua Data")

if not st.session_state.delete_all_confirm:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚠️ Hapus Semua Data", use_container_width=True):
            st.session_state.delete_all_confirm = True
            st.rerun()
else:
    st.markdown(f"""
    <div class="delete-all-box">
        <h4>⚠️ PERINGATAN</h4>
        <p>Anda akan menghapus <strong>SEMUA {len(df):,} data</strong>.</p>
        <p class="small">Tindakan ini tidak dapat dibatalkan!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("✅ Ya, Hapus Semua", use_container_width=True, type="primary"):
            st.session_state.scraped_df = None
            st.session_state.scraping_done = False
            st.session_state.delete_all_confirm = False
            st.session_state.edit_index = None
            st.session_state.edit_mode = False
            st.session_state.delete_index = None
            st.success("✅ Semua data berhasil dihapus!")
            time.sleep(0.5)
            st.rerun()
    with col2:
        if st.button("Batal", use_container_width=True):
            st.session_state.delete_all_confirm = False
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p>© 2026 SentimenAnalis — Kelola Data Scraping</p>
    <p>Data tersimpan secara otomatis selama sesi berlangsung</p>
</div>
""", unsafe_allow_html=True)