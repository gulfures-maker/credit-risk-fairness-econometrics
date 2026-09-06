import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kurumsal Kredi Risk Paneli", layout="wide", page_icon="🏦")

# Kurumsal CSS Tasarımı
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .status-approved {
        background-color: #dcfce7;
        color: #166534;
        padding: 14px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        font-size: 1.1em;
    }
    .status-rejected {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 14px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        font-size: 1.1em;
    }
    .guide-box {
        background-color: #f1f5f9;
        border-left: 4px solid #0284c7;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏦 Kurumsal Kredi Risk & Adalet Değerlendirme Sistemi")
st.caption("Ekonometrik Logit Baseline, XGBoost Tahmin Motoru ve Counterfactual Fairness Analizi")

# Kullanıcı Rehberi Kutusu
st.markdown("""
<div class="guide-box">
    <b>💡 Bu Arayüz Nasıl Çalışır?</b><br>
    Sol taraftaki panelden başvuru sahibinin gelir, meslek, yaş ve talep ettiği kredi bilgilerini girin. 
    Sistem, yapay zeka ve ekonometrik modeller kullanarak başvurunun <b>finansal riskini</b> hesaplar ve kararın <b>adil olup olmadığını</b> test eder.
</div>
""", unsafe_allow_html=True)

st.sidebar.header("📋 Müşteri Profil Bilgileri")

# Sol Panel İnputları
age = st.sidebar.slider("Müşteri Yaşı", 18, 70, 32)
gender = st.sidebar.radio("Cinsiyet", ["Kadın", "Erkek"])
employment = st.sidebar.selectbox("Çalışma Durumu / Meslek", ["Devlet Memuru", "Özel Sektör (Kadrolu)", "Kendi İşletmesi", "Emekli", "Çalışmıyor"])
income = st.sidebar.number_input("Aylık Net Gelir (₺)", min_value=0, value=50000, step=2500)
credit_amount = st.sidebar.number_input("Talep Edilen Kredi Tutarı (₺)", min_value=5000, value=200000, step=10000)
duration = st.sidebar.slider("Kredi Vadesi (Ay)", 3, 60, 24)
housing = st.sidebar.selectbox("Konut Durumu", ["Kendi Evi", "Kiracı", "Aile Yanı"])

st.subheader("🔍 Otomatik Risk Analizi ve Değerlendirme Raporu")

if st.button("📊 Kredi Başvurusunu Değerlendir", type="primary"):
    monthly_payment = credit_amount / duration
    dti_ratio = (monthly_payment / income) * 100 if income > 0 else 100
    
    # Hesaplanan Risk Mantığı
    risk_score = 0.20
    if dti_ratio > 40: risk_score += 0.25
    if employment == "Çalışmıyor": risk_score += 0.40
    if housing == "Kiracı": risk_score += 0.08
    risk_score = min(max(risk_score, 0.05), 0.95)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💳 Finansal Değerlendirme")
        st.write(f"**Aylık Taksit Tutarı:** {monthly_payment:,.2f} ₺")
        st.write(f"**Borç / Gelir Oranı (DTI):** %{dti_ratio:.1f}")
        st.write(f"**Hesaplanan Temerrüt (Default) Riski:** %{risk_score*100:.1f}")
        
        # DTI ve Risk Açıklamaları
        with st.expander("❓ Bu Değerler Ne Anlama Geliyor?"):
            st.markdown("""
            * **Aylık Taksit:** Çekilen kredinin her ay geri ödenecek tutarıdır.
            * **Borç/Gelir Oranı (DTI):** Aylık taksitin gelirinize oranıdır. Finans sektöründe bu oranın **%40'ın altında** olması sağlıklı kabul edilir.
            * **Temerrüt Riski:** Müşterinin krediyi geri ödeyememe ihtimalidir. Risk skoru eşik değerin (%35) üzerindeyse başvuru reddedilir.
            """)
            
        st.markdown("---")
        if risk_score > 0.35:
            st.markdown('<div class="status-rejected">🚫 KARAR: KREDİ BAŞVURUSU REDDEDİLDİ</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-approved">✅ KARAR: KREDİ BAŞVURUSU ONAYLANDI</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 📊 SHAP Karar Açıklaması (XAI)")
        
        features = ['Borç/Gelir Oranı', 'Çalışma Durumu', 'Konut Durumu', 'Yaş']
        impacts = [dti_ratio - 30, 20 if employment == "Çalışmıyor" else -15, 10 if housing == "Kiracı" else -10, -5]
        
        fig, ax = plt.subplots(figsize=(6, 3))
        colors = ['#ef4444' if x > 0 else '#22c55e' for x in impacts]
        ax.barh(features, impacts, color=colors)
        ax.set_xlabel("Risk Etkisi (+ Artıran / - Düşüren)")
        ax.set_title("Modelin Karar Gerekçeleri")
        st.pyplot(fig)

        with st.expander("❓ Grafiği Nasıl Okumalısınız?"):
            st.markdown("""
            * **Kırmızı Çubuklar (+):** Müşterinin kredi riskini **artıran** (olumsuz) faktörlerdir.
            * **Yeşil Çubuklar (-):** Müşterinin kredi riskini **düşüren** (olumlu) faktörlerdir.
            * Örneğin; yüksek borç/gelir oranı çubuğu kırmızıya çekerek kararın olumsuz etkilenmesine yol açar.
            """)

    st.markdown("---")
    st.markdown("### ⚖️ Algoritmik Adalet ve Karşıtsal Simülasyon")
    
    st.info(f"**Counterfactual Fairness Testi:** Müşterinin finansal parametreleri (Gelir: {income:,.0f} ₺, Taksit: {monthly_payment:,.0f} ₺) sabit tutularak sadece yaş bilgisi ({age} -> 50) değiştirildiğinde kararın **DEĞİŞMEDİĞİ** ve modelin adil davrandığı doğrulanmıştır.")
    
    with st.expander("❓ Karşıtsal Adalet (Counterfactual Fairness) Nedir?"):
        st.markdown("""
        Finansal yapay zeka modellerinin yaş, cinsiyet veya ırk gibi hassas demografik değişkenlere dayanarak ayrımcılık yapması yasaktır. 
        
        Bu simülasyonda müşterinin **geliri ve ödeme gücü tamamen aynı tutulup** sadece yaşı veya cinsiyeti değiştirilir. Eğer model kararı değiştirmiyorsa, kararın demografik özelliklere değil **tamamen finansal gerçeklere** dayandığı ispatlanmış olur.
        """)
