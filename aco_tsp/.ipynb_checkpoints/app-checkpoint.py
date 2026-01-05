import streamlit as st
import numpy as np
import time

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="ACO - Traveling Salesman Problem",
    layout="wide"
)

st.title("🐜 Ant Colony Optimization – Traveling Salesman Problem")
st.caption("Simulasi ACO")

# ======================================================
# SIDEBAR : PARAMETER ACO
# ======================================================
st.sidebar.header("Parameter ACO")

num_ants = st.sidebar.slider("Jumlah Semut", 1, 20, 5)
num_iter = st.sidebar.slider("Jumlah Iterasi", 1, 10, 5)
alpha = st.sidebar.slider("Alpha (Feromon)", 0.1, 5.0, 1.0)
beta = st.sidebar.slider("Beta (Jarak)", 0.1, 5.0, 2.0)
rho = st.sidebar.slider("Rho (Evaporasi)", 0.0, 1.0, 0.5)
Q = st.sidebar.slider("Q (Deposit Feromon)", 10, 200, 100)
delay = st.sidebar.slider("Delay Visualisasi (detik)", 0.0, 1.0, 0.5)

# ======================================================
# DATA KOTA
# ======================================================
st.subheader("📍 Data Kota")

cities = np.array([
    [0, 0],
    [2, 4],
    [3, 1],
    [5, 6],
    [6, 2]
])

st.dataframe(
    {"Kota": range(len(cities)), "X": cities[:, 0], "Y": cities[:, 1]},
    use_container_width=True
)

# ======================================================
# PERHITUNGAN JARAK & VISIBILITY
# ======================================================
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

n = len(cities)

distances = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        distances[i, j] = euclidean_distance(cities[i], cities[j])

visibility = 1 / (distances + np.eye(n))

# ======================================================
# TOMBOL SIMULASI
# ======================================================
st.divider()
btn_run = st.button("🚀 Jalankan Simulasi ACO")

# ======================================================
# PROSES ACO
# ======================================================
if btn_run:
    pheromone = np.ones((n, n))
    best_distance = float("inf")
    best_route = None

    st.subheader("📊 Proses Iterasi")

    for iteration in range(1, num_iter + 1):
        iter_best_distance = float("inf")
        iter_best_route = None

        for _ in range(num_ants):
            visited = [0]
            current = 0

            while len(visited) < n:
                probs = []
                for j in range(n):
                    if j not in visited:
                        prob = (pheromone[current][j] ** alpha) * (visibility[current][j] ** beta)
                    else:
                        prob = 0
                    probs.append(prob)

                probs = np.array(probs)
                probs /= probs.sum()

                next_city = int(np.random.choice(range(n), p=probs))
                visited.append(next_city)
                current = next_city

            visited.append(0)

            total_dist = sum(
                distances[visited[i]][visited[i + 1]]
                for i in range(len(visited) - 1)
            )

            if total_dist < iter_best_distance:
                iter_best_distance = total_dist
                iter_best_route = [int(x) for x in visited]

        if iter_best_distance < best_distance:
            best_distance = iter_best_distance
            best_route = iter_best_route

        pheromone *= (1 - rho)
        for i in range(len(best_route) - 1):
            pheromone[best_route[i]][best_route[i + 1]] += Q / best_distance

        # ======================================================
        # OUTPUT ITERASI HORIZONTAL
        # ======================================================
        c1, c2, c3 = st.columns([1, 4, 2])

        with c1:
            st.markdown(
                f"""
                <div style="padding:10px; background:#111f3b; border-radius:8px; text-align:center;">
                    <b>Iterasi</b><br>{iteration}
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div style="padding:10px; background:#0d1d3d; border-radius:8px;">
                    <b>Rute Terbaik</b><br>
                    {iter_best_route}
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div style="padding:10px; background:#0d1d3d; border-radius:8px; text-align:center;">
                    <b>Jarak</b><br>
                    {round(iter_best_distance, 3)}
                </div>
                """,
                unsafe_allow_html=True
            )

        time.sleep(delay)

    # ======================================================
    # KESIMPULAN
    # ======================================================
    st.divider()
    st.subheader("📌 Kesimpulan Akhir")

    st.success(
        f"""
        ✔ Simulasi ACO berjalan sebanyak **{num_iter} iterasi**  
        ✔ Menggunakan **{num_ants} semut**  

        🔹 **Rute terbaik yang diperoleh:**  
        {best_route}

        🔹 **Total jarak minimum:**  
        {round(best_distance, 3)}

        **Kesimpulan:**  
        Algoritma Ant Colony Optimization berhasil menemukan solusi mendekati optimal
        untuk Traveling Salesman Problem dengan memanfaatkan mekanisme feromon,
        probabilitas jarak, dan proses iteratif.
        """
    )
