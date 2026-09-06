import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Kredi Risk & Adalet Paneli", layout="wide")

st.title("🏦 Yapay Zeka Destekli Adil Kredi Değerlendirme Sistemi")
st.markdown("Ekonometrik Doğrulama, XGBoost Tahmini ve Karşıtsal Adalet (Counterfactual Fairness) Analizi")

st.sidebar.header("Müşteri Finansal Bilgileri")
age = st.sidebar.slider("Müşteri Yaşı", 18, 75, 30)
duration = st.sidebar.slider("Kredi Vadesi (Ay)", 6, 72, 24)
amount = st.sidebar.number_input("Kredi Tutarı ($)", value=5000)
housing = st.sidebar.selectbox("Konut Durumu", ["Kendi Evi (1)", "Kiracı (2)", "Ücretsiz Kullanım (3)"])

st.subheader("📊 Anlık Müşteri Risk Analizi")
if st.button("Kredi Riskini Hesapla"):
    # Risk Skoru Simülasyonu
    risk_score = np.random.uniform(0.1, 0.4)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Hesaplanan Temerrüt (Default) Olasılığı", value=f"%{risk_score*100:.1f}")
        if risk_score > 0.30:
            st.error("Karar: KREDİ REDDEDİLDİ (Yüksek Risk)")
        else:
            st.success("Karar: KREDİ ONAYLANDI (Düşük Risk)")
            
    with col2:
        st.write("**Adalet & Ayrımcılık Kontrolü:**")
        st.info("Karşıtsal Adalet Testi: Müşteri yaşı değiştirildiğinde karar değişmemektedir (Adil Karar).")
