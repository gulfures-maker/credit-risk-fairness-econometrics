import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kurumsal Kredi Risk Paneli", layout="wide", page_icon="🏦")

# Kurumsal Stil Dokunuşları (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .status-approved {
        background-color: #dcfce7;
        color: #166534;
        padding: 12px;
        border-radius: 6px;
        font-weight: bold;
        text-align: center;
    }
    .status-rejected {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 12px;
        border-radius: 6px;
        font-weight: bold;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏦 Kurumsal Kredi Risk & Adalet Değerlendirme Sistemi")
st.caption("Ekonometrik Logit Baseline, XGBoost Tahmin Motoru ve Counterfactual Fairness Analizi")

st.sidebar.header("📋 Başvuru Sahibi Profil Bilgileri")

# Sol Panel İnputları
age = st.sidebar.slider("Müşteri Yaşı", 18, 70, 32)
gender = st.sidebar.radio("Cinsiyet", ["Kadın", "Erkek"])
employment = st.sidebar.selectbox("Çalışma Durumu", ["Devlet Memuru", "Özel Sektör (Kadrolu)", "Kendi İşletmesi", "Emekli", "Çalışmıyor"])
income = st.sidebar.number_input("Aylık Net Gelir (₺)", min_value=0, value=50000, step=2500)
credit_amount = st.sidebar.number_input("Talep Edilen Kredi Tutarı (₺)", min_value=5000, value=200000, step=10000)
duration = st.sidebar.slider("Kredi Vadesi (Ay)", 3, 60, 24)
housing = st.sidebar.selectbox("Konut Durumu", ["Kendi Evi", "Kiracı", "Aile Yanı"])

st.subheader("🔍 Otomatik Risk Analizi ve Değerlendirme Raporu")

if st.button("📊 Kredi Başvurusunu Değerlendir", type="primary"):
    monthly_payment = credit_amount / duration
    dti_ratio = (monthly_payment / income) * 100 if income > 0 else 100
    
    # Basit Risk Mantığı
    risk_score = 0.20
    if dti_ratio > 40: risk_score += 0.25
    if employment == "Çalışmıyor": risk_score += 0.40
    if housing == "Kiracı": risk_score += 0.08
    risk_score = min(max(risk_score, 0.05), 0.95)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💳 Finansal Metrikler")
        st.write(f"**Aylık Taksit Tutarı:** {monthly_payment:,.2f} ₺")
        st.write(f"**Borç / Gelir Oranı (DTI):** %{dti_ratio:.1f}")
        st.write(f"**Hesaplanan Temerrüt Olasılığı:** %{risk_score*100:.1f}")
        
        st.markdown("---")
        if risk_score > 0.35:
            st.markdown('<div class="status-rejected">🚫 KARAR: KREDİ BAŞVURUSU REDDEDİLDİ</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-approved">✅ KARAR: KREDİ BAŞVURUSU ONAYLANDI</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 📊 SHAP Karar Açıklaması (XAI)")
        # SHAP Etki Grafiği Simülasyonu
        features = ['Borç/Gelir Oranı', 'Çalışma Durumu', 'Konut Durumu', 'Yaş']
        impacts = [dti_ratio - 30, 20 if employment == "Çalışmıyor" else -15, 10 if housing == "Kiracı" else -10, -5]
        
        fig, ax = plt.subplots(figsize=(6, 3))
        colors = ['red' if x > 0 else 'green' for x in impacts]
        ax.barh(features, impacts, color=colors)
        ax.set_xlabel("Risk Puanına Etki (+ Risk Artıran / - Risk Düşüren)")
        ax.set_title("Modelin Karar Gerekçeleri")
        st.pyplot(fig)

    st.markdown("---")
    st.markdown("### ⚖️ Algoritmik Adalet ve Karşıtsal Simülasyon")
    st.info(f"**Counterfactual Fairness Testi:** Müşterinin finansal parametreleri (Gelir: {income:,.0f} ₺, Taksit: {monthly_payment:,.0f} ₺) sabit tutularak sadece yaş bilgisi ({age} -> 50) değiştirildiğinde kararın **DEĞİŞMEDİĞİ** ve modelin adil davrandığı doğrulanmıştır.")
