import numpy as np
import pandas as pd


def load_alpine_hydro_data(
    start_date="2025-10-01", end_date="2026-03-31", threshold=40.0
):
  date_rng = pd.date_range(start=start_date, end=end_date, freq="h")
  df = pd.DataFrame(date_rng, columns=["timestamp"])

  np.random.seed(42)
  # شبیه‌سازی روند تخلیه مخازن در ماه‌های سرد سال
  df["swiss_reservoir_level_pct"] = 80 - (
      np.linspace(0, 30, len(df))
      + np.sin(np.linspace(0, 3 * np.pi, len(df))) * 5
  )
  df["swiss_reservoir_level_pct"] = df["swiss_reservoir_level_pct"].clip(
      15, 95
  )

  # قیمت‌گذاری مبتنی بر آستانه بحرانی مخزن
  df["price_DE"] = (
      80
      + np.random.normal(0, 25, len(df))
      + (df["swiss_reservoir_level_pct"] < threshold) * 40
  )
  df["price_CH"] = df["price_DE"] + np.random.normal(0, 10, len(df))
  df["cross_border_flow_mw"] = (
      df["price_DE"] - df["price_CH"]
  ) * 25 + np.random.normal(0, 200, len(df))

  return df
