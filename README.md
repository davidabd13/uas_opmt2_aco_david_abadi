# 🚚 Optimasi Rute Distribusi DC Alfamidi Menggunakan Ant Colony Optimization (ACO)

Proyek ini merupakan simulasi **optimasi rute distribusi** dari **Distribution Center (DC) Alfamidi ke beberapa outlet di Jakarta** menggunakan **Algoritma Ant Colony Optimization (ACO)**.  
Aplikasi dibangun secara interaktif menggunakan **Streamlit**, dengan visualisasi peta berbasis **Folium** dan perhitungan jarak geografis menggunakan **Geopy**.

---

## 📌 Latar Belakang
Dalam sistem distribusi ritel seperti Alfamidi, penentuan rute pengiriman yang efisien sangat penting untuk:
- Mengurangi jarak tempuh
- Menghemat biaya operasional
- Meningkatkan ketepatan waktu pengiriman

Permasalahan ini dapat dimodelkan sebagai **Traveling Salesman Problem (TSP)**, yang diselesaikan menggunakan **Ant Colony Optimization (ACO)**, sebuah algoritma metaheuristik yang terinspirasi dari perilaku semut dalam menemukan jalur terpendek menuju sumber makanan.

---

## 🧠 Algoritma yang Digunakan
**Ant Colony Optimization (ACO)** dengan mekanisme:
- Inisialisasi pheromone
- Probabilistic transition rule berbasis pheromone dan jarak
- Multi-ant dan multi-iteration
- Evaporasi pheromone
- Update pheromone berdasarkan solusi terbaik (Best Ant Strategy)

---

## 🗺️ Fitur Aplikasi
- ✅ Input lokasi DC dan outlet (koordinat latitude & longitude)
- ✅ Visualisasi peta lokasi outlet
- ✅ Simulasi proses ACO **langkah demi langkah**
- ✅ Log iterasi real-time (seperti proses loading)
- ✅ Ringkasan hasil setiap iterasi
- ✅ Visualisasi rute distribusi terbaik di peta
- ✅ Parameter ACO dapat diatur secara dinamis

---

## 🛠️ Teknologi yang Digunakan
- **Python 3**
- **Streamlit** – antarmuka interaktif
- **NumPy** – perhitungan numerik
- **Pandas** – pengolahan data
- **Folium** – visualisasi peta
- **Geopy** – perhitungan jarak geografis (geodesic)
- **Streamlit-Folium** – integrasi Folium dengan Streamlit

---

## 📂 Struktur Proyek
aco_distribusi/
│
├── app.py # Aplikasi utama Streamlit (ACO + Visualisasi)
├── README.md # Dokumentasi proyek
└── requirements.txt

---

## ▶️ Cara Menjalankan Aplikasi

### 1️⃣ Clone Repository
```bash
git clone https://github.com/username/aco-distribusi-alfamidi.git
cd aco-distribusi-alfamidi

