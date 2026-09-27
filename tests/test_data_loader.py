import pandas as pd
from src.data_loader import load_alpine_hydro_data


def test_load_alpine_hydro_data():
  df = load_alpine_hydro_data()

  # بررسی اینکه خروجی دیتافریم است
  assert isinstance(df, pd.DataFrame)

  # بررسی وجود ستون‌های کلیدی
  expected_columns = [
      "timestamp",
      "swiss_reservoir_level_pct",
      "price_DE",
      "price_CH",
      "cross_border_flow_mw",
  ]
  for col in expected_columns:
    assert col in df.columns

  # بررسی اینکه درصد سطح مخزن در محدوده معتبر (بین 0 تا 100) قرار دارد
  assert df["swiss_reservoir_level_pct"].min() >= 0
  assert df["swiss_reservoir_level_pct"].max() <= 100

  # بررسی اینکه تعداد سطوح داده ساعتی صفر نیست
  assert len(df) > 0
