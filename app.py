
import streamlit as st
import cv2
import numpy as np
from PIL import Image

# 1. Sayfa Ayarları (Tablet uyumu için)
st.set_page_config(page_title="TeraScan Jeo-Analiz", layout="wide")

st.title("🏗️ TERASCAN TABLET JEO-ANALİZ")
st.sidebar.header("📊 Kontrol Paneli")
st.sidebar.info("Jeolojik katman analizi ve yapı inceleme paneli.")

# 2. Dosya Yükleme Alanı
dosya = st.sidebar.file_uploader("Saha Fotoğrafı Yükle", type=['jpg', 'jpeg', 'png'])

if dosya is not None:
    # Görüntüyü oku
    image = Image.open(dosya)
    img_array = np.array(image)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📸 Orijinal Saha Verisi")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("🔍 Katman/Yapı Analizi")
        # Gri tonlama ve Kenar belirleme (Katmanları yakalar)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        kenarlar = cv2.Canny(blur, 40, 120)
        
        st.image(kenarlar, use_container_width=True, caption="Belirlenen Jeolojik Hatlar")

    # 3. Teknik Bilgiler ve Notlar
    st.divider()
    st.write(f"**Görüntü Boyutu:** {img_array.shape[1]} x {img_array.shape[0]} px")
    notlar = st.text_area("Saha Gözlemleri", placeholder="Katman yapısı hakkında not alın...")
    
    if st.button("Analiz Raporunu Kaydet"):
        st.balloons()
        st.success("Rapor taslağı oluşturuldu!")

else:
    st.warning("Lütfen sol menüden bir saha fotoğrafı seçerek analizi başlatın.")
