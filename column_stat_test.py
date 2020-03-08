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

def test_float_add():
  nan = float("nan")
  assert 0.0 == column_stat.float_add()
  assert 0.0 == column_stat.float_add(None, None)
  assert 0.0 == column_stat.float_add(nan, nan)
  assert 0.0 == column_stat.float_add(0.0, None)
  assert 0.0 == column_stat.float_add(0.0, nan)
  assert 0.0 == column_stat.float_add(nan,  0.0)
  assert 0.0 == column_stat.float_add(None, 0.0)
  assert 1.0 == column_stat.float_add(None, 1.0)
  assert 1.0 == column_stat.float_add(nan, 1.0)
  assert 1.0 == column_stat.float_add(1.0, nan)
  assert 1.0 == column_stat.float_add(1.0, None)
  assert 3.0 == column_stat.float_add(1.0, 2.0)
  assert 3.0 == column_stat.float_add(2.0, 1.0)

def test_m256d_add():
  nan = float("nan")
  assert (0.0, 0.0, 0.0, 0.0) == column_stat.m256d_add()
  assert (0.0, 0.0, 0.0, 0.0) == column_stat.m256d_add((0.0, 0.0, 0.0, 0.0))
  assert (0.0, 0.0, 0.0, 0.0) == column_stat.m256d_add((0.0, 0.0, 0.0, 0.0), None)
  assert (0.0, 0.0, 0.0, 0.0) == column_stat.m256d_add((nan, nan, nan, nan), None)
  assert (0.0, 0.0, 0.0, 0.0) == column_stat.m256d_add(None, (0.0, 0.0, 0.0, 0.0))
  assert (0.0, 0.0, 0.0, 0.0) == column_stat.m256d_add(None, (nan, nan, nan, nan))
  assert (0.0, 1.0, 2.0, 3.0) == column_stat.m256d_add((0.0,1.0,2.0,3.0),(nan,nan,nan,nan))
  assert (0.0, 1.0, 2.0, 3.0) == column_stat.m256d_add((nan,nan,nan,nan),(0.0,1.0,2.0,3.0))
  assert (0.0, 1.0, 2.0, 3.0) == column_stat.m256d_add((0.0,0.5,1.0,1.5),(0.0,0.5,1.0,1.5))

def test_numbers2stat_m256d():
  nan = float("nan")
  d256bits = iter([
    (nan, 1.0, 2.0, 3.0),
    (1.0, nan, 3.0, 4.0),
    (2.0, 3.0, nan, 5.0),
    None,
    (3.0, 4.0, 5.0, nan),
  ])
  a = column_stat.numbers2stat_m256d(d256bits)
  assert dict == type(a)
  assert "sum" in a
  s = a["sum"]
  assert tuple == type(s)
  assert 4 == len(s)
  assert (6.0, 8.0, 10.0, 12.0) == s
