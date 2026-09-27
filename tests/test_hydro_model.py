import pandas as pd
from src.hydro_model import calculate_cross_border_arbitrage


def test_calculate_cross_border_arbitrage():
  # ساخت داده نمونه (Mock Data) برای تست
  data = {
      "timestamp": pd.date_range(start="2026-01-01", periods=3, freq="h"),
      "price_DE": [100.0, 50.0, 120.0],
      "price_CH": [80.0, 55.0, 90.0],
  }
  df = pd.DataFrame(data)

  # اجرای تابع محاسبه آربیتراژ با آستانه 15 یورو
  df_result = calculate_cross_border_arbitrage(df, threshold=15.0)

  # بررسی وجود ستون‌های جدید
  assert "price_spread" in df_result.columns
  assert "arbitrage_opportunity" in df_result.columns

  # بررسی صحت محاسبات اسپرد (قیمت آلمان منهای سوئیس)
  assert df_result.loc[0, "price_spread"] == 20.0  # 100 - 80 = 20 (> 15 -> فرصت دارد)
  assert df_result.loc[0, "arbitrage_opportunity"] == 1

  assert (
      df_result.loc[1, "price_spread"] == -5.0
  )  # 50 - 55 = -5 (قدر مطلق کمتر از 15 -> بدون فرصت)
  assert df_result.loc[1, "arbitrage_opportunity"] == 0
