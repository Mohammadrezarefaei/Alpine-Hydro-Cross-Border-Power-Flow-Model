import os
import matplotlib.pyplot as plt
import pandas as pd


def generate_hydro_plots(df: pd.DataFrame):
  os.makedirs("outputs", exist_ok=True)
  fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

  # نمودار اول: سطح مخزن سوئیس
  axes[0].plot(
      df["timestamp"],
      df["swiss_reservoir_level_pct"],
      color="blue",
      label="Swiss Reservoir Level (%)",
  )
  axes[0].axhline(
      y=40, color="red", linestyle="--", label="Critical Threshold (40%)"
  )
  axes[0].set_ylabel("Level (%)")
  axes[0].legend(loc="upper right")
  axes[0].grid(True, linestyle=":", alpha=0.6)

  # نمودار دوم: قیمت‌های Day-Ahead در آلمان و سوئیس
  axes[1].plot(
      df["timestamp"],
      df["price_DE"],
      color="orange",
      label="Germany Price (€/MWh)",
      alpha=0.8,
  )
  axes[1].plot(
      df["timestamp"],
      df["price_CH"],
      color="green",
      label="Switzerland Price (€/MWh)",
      alpha=0.8,
  )
  axes[1].set_ylabel("Price (€/MWh)")
  axes[1].legend(loc="upper right")
  axes[1].grid(True, linestyle=":", alpha=0.6)

  # نمودار سوم: جریان‌های قدرت فرامرزی
  axes[2].plot(
      df["timestamp"],
      df["cross_border_flow_mw"],
      color="purple",
      label="Cross-Border Flow (MW)",
  )
  axes[2].axhline(y=0, color="black", linestyle="-", linewidth=0.8)
  axes[2].set_ylabel("Flow (MW)")
  axes[2].set_xlabel("Timestamp")
  axes[2].legend(loc="upper right")
  axes[2].grid(True, linestyle=":", alpha=0.6)

  plt.suptitle(
      "Alpine Hydro & Cross-Border Power Flow Dynamics",
      fontsize=14,
      fontweight="bold",
  )
  plt.tight_layout()

  chart_path = "outputs/alpine_hydro_dynamics.png"
  plt.savefig(chart_path, dpi=300)
  plt.close()
