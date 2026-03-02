import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# 1. Profesyonel Sayfa Ayarları
st.set_page_config(page_title="TeraScan Pro v2", layout="wide")

# Tablet için Özel Görünüm (CSS)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #007bff; color: white; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3b4e,#2e3b4e); color: white; }
    </style>
    """, unsafe_allow_index=True)

st.title("🏗️ TERASCAN PRO | Jeolojik Analiz")
st.markdown("---")

# 2. Yan Panel (Kontrol Merkezi)
st.sidebar.header("🛠️ Analiz Paneli")
st.sidebar.info("Saha fotoğraflarını yükleyip hassasiyet ayarlarını buradan yapabilirsiniz.")

# Fotoğraf Yükleme
dosya = st.sidebar.file_uploader("📸 Fotoğraf Seç veya Çek", type=['jpg', 'jpeg', 'png'])

# Hassasiyet Ayarları (Sürgüler)
st.sidebar.subheader("🔍 Filtre Ayarları")
alt_esik = st.sidebar.slider("Çizgi Yoğunluğu (Alt)", 10, 200, 50)
ust_esik = st.sidebar.slider("Çizgi Yoğunluğu (Üst)", 100, 300, 150)
blur_seviyesi = st.sidebar.select_slider("Gürültü Filtresi", options=[1, 3, 5, 7], value=3)

if dosya is not None:
    # Görüntü İşleme Aşaması
    image = Image.open(dosya)
    img_array = np.array(image.convert('RGB'))
    
    # Analiz Sütunları
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ Orijinal Saha Verisi")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("🔬 Katman/Yapı Analizi")
        # OpenCV İşlemleri
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (blur_seviyesi, blur_seviyesi), 0)
        kenarlar = cv2.Canny(blur, alt_esik, ust_esik)
        st.image(kenarlar, use_container_width=True, clamp=True)

    # 3. Raporlama ve Notlar
    st.markdown("---")
    st.subheader("📝 Saha Notları ve Rapor")
    notlar = st.text_area("Gözlemlerinizi buraya yazın...", placeholder="Örn: Kalker tabakalı yapı, 30 derece eğimli...")
    
    # Rapor Hazırlama
    rapor_metni = f"TERASCAN TEKNİK RAPORU\n\nAnaliz Hassasiyeti: {alt_esik}-{ust_esik}\nNotlar: {notlar}"
    
    # İndirme Butonu (Gerçek Dosya Oluşturur)
    st.download_button(
        label="📥 Raporu Dosya Olarak Kaydet",
        data=rapor_metni,
        file_name="jeolojik_analiz_raporu.txt",
        mime="text/plain"
    )

else:
    st.warning("👈 Lütfen sol panelden bir saha fotoğrafı seçerek analizi başlatın.")

st.sidebar.markdown("---")
st.sidebar.write("v2.0 | Saha Mühendisi Modu")
