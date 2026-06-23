# utils/data.py

# Data hasil training dari notebook (akan ditampilkan di halaman Hasil)
TRAINING_RESULTS = {
    "dataset": {
        "total_awal": 10307,
        "setelah_filter": 6467,
        "training_data": 5173,
        "training_augmented": 8329,
        "testing_data": 1294,
        "total_features": 24657,
        "label_distribution": {
            "positif": 5481,
            "netral": 634,
            "negatif": 352
        },
        "label_percentages": {
            "positif": 84.8,
            "netral": 9.8,
            "negatif": 5.4
        }
    },
    "best_nb_model": "ComplementNB + FeatureUnion",
    "best_nb_accuracy": 92.43,
    "best_overall_model": "GridSearch LinearSVC (Pembanding)",
    "best_overall_accuracy": 93.87,
    "cross_validation": {
        "mean": 97.13,
        "std": 0.57,
        "folds": [97.60, 97.06, 97.78, 97.06, 96.16]
    },
    "models": {
        "MultinomialNB Murni": 85.67,
        "ComplementNB Baseline": 87.34,
        "ComplementNB + GridSearch": 90.26,
        "ComplementNB + FeatureUnion": 92.43,
        "Voting Ensemble (Pembanding)": 92.12,
        "GridSearch LinearSVC (Pembanding)": 93.87
    },
    "classification_report": {
        "negatif": {"precision": 0.53, "recall": 0.77, "f1": 0.63, "support": 70},
        "netral": {"precision": 0.65, "recall": 0.55, "f1": 0.60, "support": 127},
        "positif": {"precision": 0.96, "recall": 0.95, "f1": 0.96, "support": 1097}
    },
    "confusion_matrix": [[1053, 20, 24], [7, 55, 8], [28, 7, 92]],
    "preprocessing_steps": [
        "Case Folding", 
        "Cleansing", 
        "Normalisasi Slang", 
        "Tokenizing", 
        "Stopword Removal", 
        "Stemming"
    ],
    "feature_extraction": "Word TF-IDF (1-3gram) + Char TF-IDF (3-5gram)",  # ← TAMBAHKAN INI
    "augmentation": "Dropout + Shuffle + Synonym Replacement",
    "top_words": [
        {"word": "bagus", "count": 245, "sentiment": "positif"},
        {"word": "samsung", "count": 412, "sentiment": "netral"},
        {"word": "kecewa", "count": 89, "sentiment": "negatif"},
        {"word": "recommended", "count": 156, "sentiment": "positif"},
        {"word": "original", "count": 203, "sentiment": "positif"},
        {"word": "rusak", "count": 67, "sentiment": "negatif"},
        {"word": "cepat", "count": 178, "sentiment": "positif"},
        {"word": "puas", "count": 234, "sentiment": "positif"},
        {"word": "mantap", "count": 134, "sentiment": "positif"},
        {"word": "keren", "count": 98, "sentiment": "positif"},
        {"word": "baterai", "count": 76, "sentiment": "netral"},
        {"word": "kamera", "count": 112, "sentiment": "positif"},
        {"word": "layar", "count": 134, "sentiment": "positif"},
        {"word": "harga", "count": 89, "sentiment": "netral"},
        {"word": "packing", "count": 189, "sentiment": "positif"}
    ]
}

def get_training_results():
    return TRAINING_RESULTS

# Data hasil scraping (akan disimpan sementara)
SCRAPED_DATA = {
    "data": [],
    "total": 0
}

def get_scraped_data():
    return SCRAPED_DATA

def set_scraped_data(data):
    global SCRAPED_DATA
    SCRAPED_DATA["data"] = data
    SCRAPED_DATA["total"] = len(data)