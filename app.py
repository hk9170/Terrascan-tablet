
import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Uygulama Başlığı ve Sayfa Düzeni
st.set_page_config(page_title="TeraScan Pro", layout="wide")
st.title("🏗️ TERASCAN PRO | Jeolojik Analiz")

# Yan Panel Ayarları
st.sidebar.header("🛠️ Kontrol Paneli")
dosya = st.sidebar.file_uploader("📸 Fotoğraf Yükle", type=['jpg', 'jpeg', 'png'])

# Analiz Parametreleri
st.sidebar.subheader("🔍 Analiz Ayarları")
alt = st.sidebar.slider("Hassasiyet (Alt Eşik)", 10, 200, 50)
ust = st.sidebar.slider("Hassasiyet (Üst Eşik)", 100, 300, 150)

if dosya:
    # Görüntüyü Oku
    img = Image.open(dosya)
    img_array = np.array(img.convert('RGB'))
    
    # Ekranı İkiye Böl
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ Orijinal Görüntü")
        st.image(img, use_container_width=True)
        
    with col2:
        st.subheader("🔬 Katman ve Çatlak Analizi")
        # Görüntü İşleme (Kenar Algılama)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        edges = cv2.Canny(blur, alt, ust)
        st.image(edges, use_container_width=True, clamp=True)
    
    st.success("✅ Analiz tamamlandı. Ayarları sol panelden değiştirebilirsiniz.")
else:
    st.info("👈 Başlamak için sol taraftaki panelden bir saha fotoğrafı yükleyin.")

st.sidebar.markdown("---")
st.sidebar.write("v2.1 | Jeoloji Mühendisliği Modu")
