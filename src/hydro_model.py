import numpy as np
import pandas as pd


def calculate_cross_border_arbitrage(
    df: pd.DataFrame, threshold: float = 15.0
) -> pd.DataFrame:
  """محاسبه اسپرد قیمت بین آلمان و سوئیس و شناسایی فرصت‌های آربیتراژ"""
  df["price_spread"] = df["price_DE"] - df["price_CH"]
  df["arbitrage_opportunity"] = np.where(
      df["price_spread"].abs() > threshold, 1, 0
  )
  return df
