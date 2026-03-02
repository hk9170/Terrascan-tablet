import streamlit as st
import cv2
import numpy as np
from PIL import Image
import plotly.graph_objects as go

# Sayfa Yapılandırması
st.set_page_config(page_title="TeraScan 3D Pro", layout="wide")
st.title("🌋 TERASCAN 3D | Jeolojik Yüzey Analizi")

# Yan Panel (Sidebar)
st.sidebar.header("🛠️ Kontrol Merkezi")
uploaded_file = st.sidebar.file_uploader("📸 Yeni Saha Fotoğrafı Yükle", type=['jpg', 'jpeg', 'png'])

st.sidebar.subheader("🔍 Analiz Ayarları")
alt = st.sidebar.slider("Hassasiyet (Alt)", 10, 200, 50)
ust = st.sidebar.slider("Hassasiyet (Üst)", 100, 300, 150)

if uploaded_file:
    # Görüntü İşleme
    image = Image.open(uploaded_file)
    img_array = np.array(image.convert('RGB'))
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # 1. Sekmeli Görünüm (2D ve 3D arasında geçiş için)
    tab1, tab2 = st.tabs(["📊 2D Analiz", "🌐 3D Görselleştirme"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Orijinal Saha Verisi")
            st.image(image, use_container_width=True)
        with col2:
            st.subheader("Kenar & Tabaka Tespiti")
            edges = cv2.Canny(gray, alt, ust)
            st.image(edges, use_container_width=True)

    with tab2:
        st.subheader("İnteraktif 3D Katman Modeli")
        # Görüntüyü küçültelim (Performans için)
        scale_percent = 20 
        width = int(gray.shape[1] * scale_percent / 100)
        height = int(gray.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_gray = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)

        # 3D Yüzey Oluşturma
        z_data = resized_gray
        fig = go.Figure(data=[go.Surface(z=z_data, colorscale='Viridis')])
        
        fig.update_layout(
            title='Yüzey Sertlik/Yoğunluk Haritası',
            autosize=True,
            width=800, height=800,
            margin=dict(l=65, r=50, b=65, t=90)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 Yukarıdaki modeli parmağınızla çevirebilir, yakınlaştırabilirsiniz.")

else:
    st.info("👈 Analize başlamak için sol panelden bir fotoğraf yükleyin.")
