import math

import column_stat

def test_max_float():
  nan = float("nan")
  assert 0.0 == column_stat.max_float()
  assert math.isnan(column_stat.max_float(None, None))
  assert math.isnan(column_stat.max_float(nan, nan))
  assert 0.0 == column_stat.max_float(None, 0.0)
  assert 0.0 == column_stat.max_float(0.0, None)
  assert 0.0 == column_stat.max_float(0.0, nan)
  assert 0.0 == column_stat.max_float(nan, 0.0)
  assert 1.0 == column_stat.max_float(nan, 1.0)
  assert 1.0 == column_stat.max_float(1.0, None)
  assert 1.0 == column_stat.max_float(1.0, 0.0)
  assert 1.0 == column_stat.max_float(0.0, 1.0)

def test_min_float():
  nan = float("nan")
  assert 0.0 == column_stat.min_float()
  assert math.isnan(column_stat.min_float(None, None))
  assert math.isnan(column_stat.min_float(nan, nan))
  assert 0.0 == column_stat.min_float(None, 0.0)
  assert 0.0 == column_stat.min_float(0.0, None)
  assert 0.0 == column_stat.min_float(0.0, nan)
  assert 0.0 == column_stat.min_float(nan, 0.0)
  assert 1.0 == column_stat.min_float(nan, 1.0)
  assert 1.0 == column_stat.min_float(1.0, None)
  assert 0.0 == column_stat.min_float(1.0, 0.0)
  assert 0.0 == column_stat.min_float(0.0, 1.0)

def test_numbers2stat_float():
  nan = float("nan")
  numbers = iter([
    0.0,
    1.0,
    nan,
    None,
    2.0,
  ])
  a = column_stat.numbers2stat_float(numbers)
  assert dict == type(a)
  assert "sum" in a
  assert "max" in a
  assert "min" in a

  assert 3.0 == a["sum"]
  assert 2.0 == a["max"]
  assert 0.0 == a["min"]
