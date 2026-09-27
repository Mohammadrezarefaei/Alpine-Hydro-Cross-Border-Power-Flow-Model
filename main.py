import os
import streamlit as st
from src.data_loader import load_alpine_hydro_data
from src.hydro_model import calculate_cross_border_arbitrage
from src.visualizer import generate_hydro_plots

# تنظیمات صفحه استریم‌لیت
st.set_page_config(
    page_title="Alpine Hydro & Cross-Border Power Flow Model",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Alpine Hydro & Cross-Border Power Flow Model")
st.markdown(
    "Interactive engineering and data analytical application modeling seasonal"
    " water and power flow dynamics across Alpine borders (Switzerland and"
    " Germany)."
)

# --- Sidebar Controls ---
st.sidebar.header("🎛️ Simulation Parameters")

critical_threshold = st.sidebar.slider(
    "Swiss Reservoir Critical Level (%)",
    min_value=20.0,
    max_value=60.0,
    value=40.0,
    step=1.0,
    help="Threshold below which Swiss winter scarcity pricing kicks in.",
)

arbitrage_spread = st.sidebar.slider(
    "Arbitrage Spread Threshold (€/MWh)",
    min_value=5.0,
    max_value=30.0,
    value=15.0,
    step=1.0,
    help="Minimum price spread required to trigger cross-border arbitrage.",
)

# --- Data Processing Pipeline ---
with st.spinner("Running Alpine hydro and power flow simulation..."):
  df_raw = load_alpine_hydro_data(threshold=critical_threshold)
  df_processed = calculate_cross_border_arbitrage(
      df_raw, threshold=arbitrage_spread
  )
  generate_hydro_plots(df_processed)

# --- Main Dashboard Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric(
    "Average DE Price",
    f"{df_processed['price_DE'].mean():.2f} €/MWh",
    delta=f"{df_processed['price_DE'].std():.1f} Vol",
)
col2.metric(
    "Average CH Price",
    f"{df_processed['price_CH'].mean():.2f} €/MWh",
    delta=f"{df_processed['price_CH'].std():.1f} Vol",
)
col3.metric(
    "Arbitrage Hours Detected",
    f"{int(df_processed['arbitrage_opportunity'].sum())} hrs",
    delta=f"{(df_processed['arbitrage_opportunity'].mean()*100):.1f}%",
)

st.markdown("---")

# --- Display Generated Charts ---
st.subheader("📈 Simulation Dynamics & Analytics")
chart_path = "outputs/alpine_hydro_dynamics.png"
if os.path.exists(chart_path):
  st.image(
      chart_path,
      caption=(
          "Multi-panel analytical charts tracking reservoir levels,"
          " wholesale prices, and cross-border exchange volumes."
      ),
      use_container_width=True,
  )
else:
  st.warning(
      "Outputs chart not found yet. Please verify the visualizer module."
  )

# --- Data Preview Table ---
st.subheader("📊 Processed Time-Series Data Sample")
st.dataframe(df_processed.head(10), use_container_width=True)

# --- Sidebar Download Button for Outputs ---
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Download Bundle")
output_dir = "outputs"
zip_filename = "alpine_hydro_outputs_bundle"
zip_path = f"{zip_filename}.zip"

if os.path.exists(output_dir):
  import base64
  import shutil

  shutil.make_archive(zip_filename, "zip", output_dir)
  if os.path.exists(zip_path):
    with open(zip_path, "rb") as f:
      bytes_data = f.read()
    b64 = base64.b64encode(bytes_data).decode()
    href = f'<a href="data:file/zip;base64,{b64}" download="{zip_path}" style="text-decoration: none;"><button style="background-color: #ff4b4b; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">📦 Download All Outputs (.zip)</button></a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
