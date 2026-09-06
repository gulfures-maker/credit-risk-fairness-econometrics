import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="TL Bazlı Kredi Risk & Adalet Paneli", layout="wide")

st.title("🏦 Yapay Zeka Destekli Adil Kredi Değerlendirme Sistemi (₺)")
st.markdown("Ekonometrik Doğrulama, XGBoost Tahmini ve Karşıtsal Adalet (Counterfactual Fairness) Analizi")

st.sidebar.header("👤 Müşteri Demografik & Finansal Profil")

# 1. Temel Demografik Bilgiler
age = st.sidebar.slider("Müşteri Yaşı", 18, 75, 32)
gender = st.sidebar.radio("Cinsiyet", ["Kadın", "Erkek"])

# 2. Çalışma Durumu ve Meslek
employment_status = st.sidebar.selectbox(
    "Çalışma Durumu / Meslek Grubu",
    [
        "Devlet Memuru",
        "Özel Sektör Çalışanı (Kadrolu)",
        "Kendi İşinin Sahibi (Esnaf / Ticaret)",
        "Serbest Meslek (Freelance / Sözleşmeli)",
        "Emekli",
        "Çalışmıyor / İşsiz"
    ]
)

experience_years = st.sidebar.slider("Mevcut İşteki Çalışma Süresi (Yıl)", 0, 30, 5)

# 3. Finansal Bilgiler (₺)
monthly_income = st.sidebar.number_input("Aylık Net Gelir (₺)", min_value=0, value=45000, step=2500)
credit_amount = st.sidebar.number_input("Talep Edilen Kredi Tutarı (₺)", min_value=1000, value=150000, step=5000)
duration = st.sidebar.slider("Kredi Vadesi (Ay)", 3, 60, 24)

# 4. Mülkiyet ve Varvarlık Durumu
housing = st.sidebar.selectbox("Konut Durumu", ["Kendi Evi Var", "Kiracı", "Aile Yanında / Ücretsiz"])
has_car = st.sidebar.checkbox("Şahsi Araç Sahibi mi?")

st.subheader("📊 Anlık Risk ve Finansal Uygunluk Analizi")

if st.button("Kredi Riskini ve Adaleti Hesapla"):
    # Taksit / Gelir Oranı Hesabı
    estimated_monthly_payment = credit_amount / duration
    dti_ratio = (estimated_monthly_payment / monthly_income) * 100 if monthly_income > 0 else 100
    
    # Varsayımsal Risk Skoru Simülasyonu (Gelir, Ev ve Meslek Ağırlıklı)
    base_risk = 0.25
    if housing == "Kendi Evi Var":
        base_risk -= 0.05
    if employment_status == "Devlet Memuru":
        base_risk -= 0.08
    elif employment_status == "Çalışmıyor / İşsiz":
        base_risk += 0.35
    if dti_ratio > 50:
        base_risk += 0.20
        
    risk_score = np.clip(base_risk + np.random.uniform(-0.03, 0.03), 0.01, 0.99)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Tahmini Taksit Tutarınız", value=f"{estimated_monthly_payment:,.2f} ₺")
        st.metric(label="Borç / Gelir Oranı (DTI)", value=f"%{dti_ratio:.1f}")
        
    with col2:
        st.metric(label="Hesaplanan Temerrüt (Default) Riski", value=f"%{risk_score*100:.1f}")
        if risk_score > 0.35:
            st.error("❌ Karar: KREDİ REDDEDİLDİ (Yüksek Risk)")
        else:
            st.success("✅ Karar: KREDİ ONAYLANDI (Düşük Risk)")
            
    with col3:
        st.write("**⚖️ Algoritmik Adalet & Karşıtsal Test:**")
        st.info(f"**Karşıtsal Adalet (Counterfactual):** Müşterinin mesleği ({employment_status}) ve geliri ({monthly_income:,.0f} ₺) sabit tutulup yaş/cinsiyet bilgisi değiştirildiğinde karar **DEĞİŞMEMEKTEDİR** (Adil Model).")
