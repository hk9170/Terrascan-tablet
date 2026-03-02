
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# 1. Sayfa Ayarları
st.set_page_config(page_title="TeraScan Pro v2", layout="wide")

st.title("🏗️ TERASCAN PRO | Jeolojik Analiz")

# 2. Yan Panel
st.sidebar.header("🛠️ Analiz Paneli")
dosya = st.sidebar.file_uploader("📸 Fotoğraf Seç", type=['jpg', 'jpeg', 'png'])

# Ayar Sürgüleri
alt_esik = st.sidebar.slider("Çizgi Yoğunluğu (Alt)", 10, 200, 50)
ust_esik = st.sidebar.slider("Çizgi Yoğunluğu (Üst)", 100, 300, 150)

if dosya is not None:
    image = Image.open(dosya)
    img_array = np.array(image.convert('RGB'))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ Orijinal")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("🔬 Analiz")
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        kenarlar = cv2.Canny(blur, alt_esik, ust_esik)
        st.image(kenarlar, use_container_width=True, clamp=True)
else:
    st.info("👈 Lütfen sol panelden bir fotoğraf yükleyin.")
