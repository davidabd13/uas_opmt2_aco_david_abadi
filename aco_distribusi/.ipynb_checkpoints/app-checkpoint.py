import streamlit as st
import pandas as pd
import numpy as np
import folium
import time
from geopy.distance import geodesic
from streamlit_folium import st_folium

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="ACO Distribusi Alfamidi", layout="wide")

st.title("🚚 Optimasi Rute Distribusi DC Alfamidi (ACO)")
st.caption("Simulasi Ant Colony Optimization dengan proses iterasi langkah demi langkah")

# =====================================================
# DATA LOKASI
# =====================================================
locations = [
    {"Nama": "DC Alfamidi", "Lat": -6.200, "Lon": 106.816},  # pusat / DC
    {"Nama": "Alfamidi Sawah Besar", "Lat": -6.1582908, "Lon": 106.8321983},
    {"Nama": "Alfamidi Ciputat Raya", "Lat": -6.2649701, "Lon": 106.7753407},
    {"Nama": "Alfamidi Cempaka Putih", "Lat": -6.1868074, "Lon": 106.8633086},
    {"Nama": "Alfamidi Kemayoran", "Lat": -6.1612809, "Lon": 106.8469652},
]

# =====================================================
# SIDEBAR PARAMETER
# =====================================================
st.sidebar.header("⚙️ Parameter ACO")

n_ants = st.sidebar.slider("Jumlah Tim Distribusi", 1, 10, 5)
n_iter = st.sidebar.slider("Jumlah Iterasi", 1, 10, 5)
alpha = st.sidebar.slider("Alpha (pheromone)", 0.1, 5.0, 1.0)
beta = st.sidebar.slider("Beta (jarak)", 0.1, 5.0, 2.0)
rho = st.sidebar.slider("Rho (evaporasi)", 0.1, 1.0, 0.5)
Q = st.sidebar.slider("Q (deposit pheromone)", 10, 200, 100)

# =====================================================
# SESSION STATE
# =====================================================
if "logs" not in st.session_state:
    st.session_state.logs = []
if "history" not in st.session_state:
    st.session_state.history = []
if "best_path" not in st.session_state:
    st.session_state.best_path = None
if "best_distance" not in st.session_state:
    st.session_state.best_distance = None
if "optimization_done" not in st.session_state:
    st.session_state.optimization_done = False

# =====================================================
# TABEL LOKASI
# =====================================================
st.subheader("📍 Tabel Lokasi DC & Outlet")

df = pd.DataFrame(locations)
df.insert(0, "Pilih", False)

edited_df = st.data_editor(df, hide_index=True, use_container_width=True)

# =====================================================
# PETA LOKASI AWAL
# =====================================================
st.subheader("🗺️ Peta Lokasi")

base_map = folium.Map(
    location=[locations[0]["Lat"], locations[0]["Lon"]],
    zoom_start=13,
    tiles="CartoDB dark_matter"
)

for _, row in edited_df.iterrows():
    folium.CircleMarker(
        location=[row["Lat"], row["Lon"]],
        radius=7,
        popup=row["Nama"],
        color="red" if row["Pilih"] else "blue",
        fill=True
    ).add_to(base_map)

st_folium(base_map, width=900, height=400)

# =====================================================
# PREPARE ACO
# =====================================================
coords = [(l["Lat"], l["Lon"]) for l in locations]
n_nodes = len(coords)

dist_matrix = np.zeros((n_nodes, n_nodes))
for i in range(n_nodes):
    for j in range(n_nodes):
        if i != j:
            dist_matrix[i][j] = geodesic(coords[i], coords[j]).km

# =====================================================
# PLACEHOLDER LIVE UI
# =====================================================
log_placeholder = st.empty()
progress_placeholder = st.empty()

# =====================================================
# BUTTON START
# =====================================================
if st.button("🚀 Jalankan Optimasi"):

    # RESET STATE
    st.session_state.logs = []
    st.session_state.history = []
    st.session_state.best_path = None
    st.session_state.best_distance = None
    st.session_state.optimization_done = False

    pheromone = np.ones((n_nodes, n_nodes))
    best_distance = float("inf")
    best_path = None

    total_step = n_iter * n_ants
    step = 0

    for iteration in range(1, n_iter + 1):
        st.session_state.logs.append(f"### 🔁 Iterasi {iteration}")

        for ant in range(1, n_ants + 1):
            step += 1
            progress_placeholder.progress(step / total_step)

            visited = [0]
            st.session_state.logs.append(f"🐜 Tim {ant} mulai dari DC")

            while len(visited) < n_nodes:
                current = visited[-1]
                probs = []

                for j in range(n_nodes):
                    if j not in visited:
                        prob = (pheromone[current][j] ** alpha) * ((1 / dist_matrix[current][j]) ** beta)
                    else:
                        prob = 0
                    probs.append(prob)

                probs = np.array(probs)
                probs /= probs.sum()
                next_node = np.random.choice(range(n_nodes), p=probs)

                st.session_state.logs.append(
                    f"➡️ {locations[current]['Nama']} → {locations[next_node]['Nama']}"
                )
                visited.append(next_node)

                with log_placeholder.container():
                    for log in st.session_state.logs[-10:]:
                        st.markdown(log)

                time.sleep(0.4)

            visited.append(0)

            total_distance = sum(
                dist_matrix[visited[i]][visited[i + 1]]
                for i in range(len(visited) - 1)
            )

            st.session_state.logs.append(
                f"✅ Tim {ant} selesai | Jarak: {total_distance:.2f} km"
            )

            if total_distance < best_distance:
                best_distance = total_distance
                best_path = visited

            time.sleep(0.4)

        pheromone *= (1 - rho)
        for i in range(len(best_path) - 1):
            pheromone[best_path[i]][best_path[i + 1]] += Q / best_distance

        st.session_state.history.append({
            "Iterasi": iteration,
            "Jarak Terbaik (km)": round(best_distance, 2)
        })

    st.session_state.best_path = best_path
    st.session_state.best_distance = best_distance
    st.session_state.optimization_done = True

    progress_placeholder.empty()

# =====================================================
# LOG PROSES
# =====================================================
if st.session_state.logs:
    st.subheader("📜 Proses Iterasi ACO")
    with st.container(height=350):
        for log in st.session_state.logs:
            st.markdown(log)

# =====================================================
# HASIL AKHIR
# =====================================================
if st.session_state.optimization_done:

    st.subheader("📊 Ringkasan Iterasi")
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)

    st.subheader("🗺️ Peta Jalur Terbaik")

    route_coords = [(locations[i]["Lat"], locations[i]["Lon"]) for i in st.session_state.best_path]

    summary_map = folium.Map(
        location=route_coords[0],
        zoom_start=13,
        tiles="CartoDB dark_matter"
    )

    folium.PolyLine(route_coords, color="red", weight=5).add_to(summary_map)

    for idx, i in enumerate(st.session_state.best_path):
        folium.Marker(
            location=[locations[i]["Lat"], locations[i]["Lon"]],
            popup=f"{idx}. {locations[i]['Nama']}",
            icon=folium.DivIcon(
                html=f"""
                <div style="background:#1f77b4;color:white;
                border-radius:50%;width:28px;height:28px;
                text-align:center;line-height:28px;font-weight:bold">
                {idx}
                </div>
                """
            )
        ).add_to(summary_map)

    st_folium(summary_map, width=900, height=450)
    st.metric("🚚 Total Jarak Minimum", f"{st.session_state.best_distance:.2f} km")
