import re
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

# ==================== SLANG DICTIONARY ====================
SLANG_DICT = {
    # Kata ganti
    'gw': 'saya', 'gue': 'saya', 'gua': 'saya', 'aku': 'saya',
    'lo': 'kamu', 'lu': 'kamu', 'kau': 'kamu', 'ko': 'kamu',
    'kamu': 'kamu', 'anda': 'anda', 'kalian': 'kalian',
    'mrk': 'mereka', 'mereka': 'mereka', 'kita': 'kita', 'kami': 'kami',
    
    # Kata kerja
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
    
    # Kata sifat
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
    
    # Kata keterangan
    'sangat': 'sangat', 'sgt': 'sangat', 'skali': 'sekali', 'sekali': 'sekali',
    'banget': 'banget', 'bgt': 'banget', 'bgtt': 'banget', 'bngt': 'banget',
    'bgttt': 'banget', 'bgtu': 'begitu', 'gtu': 'begitu', 'gitu': 'begitu',
    'begitu': 'begitu', 'begono': 'begitu', 'begini': 'beginilah',
    'selalu': 'selalu', 'slalu': 'selalu',
    'sering': 'sering', 'sring': 'sering',
    'pernah': 'pernah', 'prnh': 'pernah',
    'biasa': 'biasa', 'biasae': 'biasanya',
    
    # Kata hubung
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
    
    # Kata depan
    'di': 'di', 'd': 'di',
    'ke': 'ke', 'k': 'ke',
    'dari': 'dari', 'dr': 'dari', 'daripada': 'dari',
    'kepada': 'kepada', 'kpd': 'kepada',
    'pada': 'pada', 'pd': 'pada',
    'untuk': 'untuk', 'utk': 'untuk', 'buat': 'untuk', 'bwt': 'untuk',
    'dengan': 'dengan', 'dgn': 'dengan', 'sama': 'dengan',
    'tanpa': 'tanpa', 'tnpa': 'tanpa',
    
    # Kata bantu
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
    
    # Kata banyak/sedikit
    'banyak': 'banyak', 'byk': 'banyak', 'bnyk': 'banyak',
    'sedikit': 'sedikit', 'sdikit': 'sedikit', 'dikit': 'sedikit', 'dkit': 'sedikit',
    'semua': 'semua', 'smua': 'semua', 'semuanya': 'semua',
    
    # Kata tanya
    'apa': 'apa', 'ap': 'apa', 'apakah': 'apakah',
    'siapa': 'siapa', 'sapa': 'siapa',
    'mana': 'mana', 'mane': 'mana',
    'kenapa': 'kenapa', 'knp': 'kenapa', 'kenap': 'kenapa',
    'bagaimana': 'bagaimana', 'gimana': 'bagaimana', 'gmn': 'bagaimana',
    'berapa': 'berapa', 'brp': 'berapa',
    'kapan': 'kapan', 'kp': 'kapan',
    
    # Kata seru
    'ah': 'ah', 'wah': 'wah', 'wow': 'wow',
    'yah': 'yah', 'ya': 'ya', 'ye': 'ya',
    'oh': 'oh', 'ooh': 'oh',
    'weh': 'weh', 'wih': 'wih',
    'hehe': 'hehe', 'haha': 'haha', 'hihi': 'hihi',
    
    # Singkatan umum
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
    
    # Kata gaul lainnya
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
    
    # Kata tidak baku lain
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
    
    # Typo dan varian
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

# ==================== STOPWORDS ====================
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
    'saat', 'sekarang', 'kemarin', 'hari', 'bulan', 'tahun', 'waktu'
}

NEGATIONS = {'tidak', 'bukan', 'jangan', 'belum', 'tanpa', 'tak', 'takkan'}

# ==================== PREPROCESSING FUNCTIONS ====================
def step1_case_folding(text):
    """Step 1: Case Folding - Mengubah teks ke huruf kecil"""
    return text.lower()

def step2_cleansing(text):
    """Step 2: Cleansing - Membersihkan karakter tidak perlu"""
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def step3_normalisasi_slang(text):
    """Step 3: Normalisasi Slang"""
    words = text.split()
    hasil = []
    for w in words:
        w_lower = w.lower()
        if w_lower in SLANG_DICT:
            hasil.append(SLANG_DICT[w_lower])
        else:
            hasil.append(w)
    return ' '.join(hasil)

def step4_tokenizing(text):
    """Step 4: Tokenizing"""
    return text.split()

def step5_stopword_removal(tokens):
    """Step 5: Stopword Removal"""
    return [w for w in tokens if w not in STOPWORDS or w in NEGATIONS]

def step6_stemming(tokens):
    """Step 6: Stemming - Sederhana"""
    def simple_stem(word):
        if len(word) < 3:
            return word
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
        return word if len(word) > 1 else word
    
    return [simple_stem(w) for w in tokens if len(simple_stem(w)) > 1]

def preprocess_text(text, return_tokens=False):
    """
    Preprocessing teks dengan 6 langkah lengkap
    
    Args:
        text: Teks yang akan diproses
        return_tokens: Jika True, return list of tokens, else return string
    
    Returns:
        String atau list of tokens hasil preprocessing
    """
    if not text or not isinstance(text, str):
        return "" if not return_tokens else []
    
    text = step1_case_folding(text)
    text = step2_cleansing(text)
    text = step3_normalisasi_slang(text)
    tokens = step4_tokenizing(text)
    tokens = step5_stopword_removal(tokens)
    tokens = step6_stemming(tokens)
    
    if return_tokens:
        return tokens
    return ' '.join(tokens)

def predict_sentiment_rule_based(text):
    """
    Rule-based sentiment analysis (fallback)
    """
    if not text:
        return 'netral', 0.5
    
    text_lower = text.lower()
    
    positive_words = ['bagus', 'baik', 'keren', 'mantap', 'puas', 'suka', 'senang', 
                     'recommended', 'original', 'cepat', 'murah', 'berkualitas', 
                     'awet', 'jernih', 'lengkap', 'mudah', 'nyaman', 'kuat']
    
    negative_words = ['jelek', 'buruk', 'kecewa', 'rusak', 'lambat', 'mahal', 
                     'kurang', 'tidak', 'bukan', 'jangan', 'belum', 'gagal', 
                     'cacat', 'bocor', 'lemot', 'error', 'menyesal']
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        confidence = min(0.9, 0.5 + (positive_count - negative_count) * 0.1)
        return 'positif', confidence
    elif negative_count > positive_count:
        confidence = min(0.9, 0.5 + (negative_count - positive_count) * 0.1)
        return 'negatif', confidence
    else:
        return 'netral', 0.5

def get_preprocessing_steps_info():
    """Mendapatkan informasi 6 langkah preprocessing"""
    return [
        "Case Folding - Mengubah teks ke huruf kecil",
        "Cleansing - Hapus URL, mention, angka, tanda baca, emoji",
        "Normalisasi Slang - Ganti kata tidak baku (gak→tidak, bgt→banget)",
        "Tokenizing - Memecah teks menjadi token/kata",
        "Stopword Removal - Hapus kata umum, pertahankan kata negasi",
        "Stemming - Mengubah kata ke bentuk dasar (root word)"
    ]