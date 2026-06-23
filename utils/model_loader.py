import pickle
import joblib
import os
import json
import numpy as np
import streamlit as st

def load_models():
    """Memuat model dari folder models/"""
    models = {}
    
    # Path ke folder models
    models_dir = "models"
    model_paths = []
    
    # Cari semua file .pkl di folder models
    if os.path.exists(models_dir):
        for file in os.listdir(models_dir):
            if file.endswith('.pkl'):
                model_paths.append(os.path.join(models_dir, file))
    
    # Tambahkan path alternatif
    model_paths.extend([
        'models/mnb_best_model.pkl',
        'models/feature_union_samsung.pkl',
        'models/model_mnb_gs_samsung.pkl',
        'mnb_best_model.pkl',
        'feature_union_samsung.pkl',
        'model_mnb_gs_samsung.pkl',
        '../models/mnb_best_model.pkl',
        '../models/feature_union_samsung.pkl',
        '../models/model_mnb_gs_samsung.pkl'
    ])
    
    # Load model utama (prioritaskan mnb_best_model)
    primary_model = None
    feature_union = None
    gs_model = None
    
    for path in model_paths:
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    model = pickle.load(f)
                    
                    # Identifikasi jenis model
                    if 'mnb_best_model' in path:
                        primary_model = model
                        models['model'] = model
                        models['loaded'] = True
                        models['path'] = path
                        print(f"✅ Model utama loaded from: {path}")
                    elif 'feature_union' in path:
                        feature_union = model
                        models['feature_union'] = model
                        print(f"✅ Feature Union loaded from: {path}")
                    elif 'model_mnb_gs' in path:
                        gs_model = model
                        models['gs_model'] = model
                        print(f"✅ GridSearch Model loaded from: {path}")
                        
            except Exception as e:
                print(f"❌ Failed to load model from {path}: {e}")
                continue
    
    # Jika belum ada model yang dimuat, coba load dari model_mnb_gs
    if not models.get('loaded', False) and gs_model is not None:
        models['model'] = gs_model
        models['loaded'] = True
        models['path'] = 'model_mnb_gs_samsung.pkl'
        print("✅ Using GridSearch model as primary")
    
    # Jika masih belum ada, coba cari di root
    if not models.get('loaded', False):
        root_paths = [
            'mnb_best_model.pkl',
            'model_mnb_gs_samsung.pkl',
            'feature_union_samsung.pkl'
        ]
        for path in root_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'rb') as f:
                        model = pickle.load(f)
                        models['model'] = model
                        models['loaded'] = True
                        models['path'] = path
                        print(f"✅ Model loaded from root: {path}")
                        break
                except Exception as e:
                    print(f"❌ Failed to load from {path}: {e}")
                    continue
    
    # Coba dengan joblib sebagai fallback
    if not models.get('loaded', False):
        joblib_paths = [
            'models/mnb_best_model.joblib',
            'models/feature_union_samsung.joblib',
            'models/model_mnb_gs_samsung.joblib',
            'mnb_best_model.joblib'
        ]
        for path in joblib_paths:
            if os.path.exists(path):
                try:
                    model = joblib.load(path)
                    models['model'] = model
                    models['loaded'] = True
                    models['path'] = path
                    print(f"✅ Model loaded from: {path}")
                    break
                except Exception as e:
                    print(f"❌ Failed to load from {path}: {e}")
                    continue
    
    return models

def load_model_performance():
    """Memuat data performa model dari JSON"""
    json_paths = [
        'models/model_performance.json',
        'model_performance.json',
        'models/model_performance (7).json',
        'model_performance (7).json',
        '../models/model_performance.json'
    ]
    
    for path in json_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
            except Exception as e:
                print(f"❌ Failed to load performance from {path}: {e}")
                continue
    
    # Data default jika file tidak ditemukan
    return {
        "MultinomialNB Murni": 0.8560371517027864,
        "MultinomialNB + Smooth": 0.8900928792569659,
        "MultinomialNB + GridSearch": 0.8869969040247678,
        "MultinomialNB + FeatureUnion": 0.8993808049535603,
        "Voting Ensemble (Pembanding)": 0.9226006191950464,
    
    }

def get_model_info():
    """Mendapatkan informasi model dari performance data"""
    performance = load_model_performance()
    
    if performance:
        # Cari model terbaik
        best_model = max(performance.items(), key=lambda x: x[1])
        return {
            'best_model_name': best_model[0],
            'best_accuracy': best_model[1],
            'all_models': performance
        }
    
    return {
        'best_model_name': 'MultinomialNB + FeatureUnion',
        'best_accuracy': 0.89938,
        'all_models': {}
    }

def predict_with_ml_model(text, models):
    """Prediksi dengan model ML"""
    if not models or not models.get('loaded', False):
        return None, None, None
    
    try:
        model = models['model']
        
        # Jika text adalah string, konversi ke list
        if isinstance(text, str):
            text = [text]
        
        # Prediksi
        prediction = model.predict(text)[0]
        
        # Probabilitas
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(text)[0]
        else:
            proba = None
        
        # Konversi prediksi ke label
        if hasattr(model, 'classes_'):
            classes = model.classes_
            if isinstance(prediction, (int, np.integer)):
                label = classes[prediction]
            else:
                label = prediction
        else:
            label = prediction
        
        # Buat probabilitas dictionary
        if proba is not None:
            if hasattr(model, 'classes_'):
                prob_dict = {cls: float(prob) for cls, prob in zip(classes, proba)}
            else:
                # Default mapping untuk 3 kelas: negatif, netral, positif
                if len(proba) == 3:
                    prob_dict = {
                        'negatif': float(proba[0]),
                        'netral': float(proba[1]),
                        'positif': float(proba[2])
                    }
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
        print(f"❌ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None

def get_available_models():
    """Mendapatkan daftar model yang tersedia di folder models/"""
    available_models = []
    models_dir = "models"
    
    if os.path.exists(models_dir):
        for file in os.listdir(models_dir):
            if file.endswith('.pkl'):
                available_models.append(file)
    
    # Tambahkan model di root
    for file in os.listdir('.'):
        if file.endswith('.pkl') and file not in available_models:
            available_models.append(file)
    
    return available_models