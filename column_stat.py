import math

import number_alt

def max_float(a=0.0, b=0.0):
  invalid_a = float != type(a) or math.isnan(a)
  invalid_b = float != type(b) or math.isnan(b)
  valid_a = 0 if invalid_a else 1
  valid_b = 0 if invalid_b else 2
  i = valid_a + valid_b
  return {
    0: float("nan"),
    1: a,
    2: b,
    3: max(a,b),
  }[i]

def min_float(a=0.0, b=0.0):
  invalid_a = float != type(a) or math.isnan(a)
  invalid_b = float != type(b) or math.isnan(b)
  valid_a = 0 if invalid_a else 1
  valid_b = 0 if invalid_b else 2
  i = valid_a + valid_b
  return {
    0: float("nan"),
    1: a,
    2: b,
    3: min(a,b),
  }[i]

def float2stat_default(stat=dict(), number=0.0, alt=0.0):
  stat["sum"] = stat.get("sum", 0.0)  + number_alt.number_alt_float_nn(number, alt)
  stat["max"] = max_float(stat.get("max", None), number)
  stat["min"] = min_float(stat.get("min", None), number)
  return stat

def numbers2stat_float(numbers=iter([]), float2stat=float2stat_default, stat0=dict()):
  return reduce(float2stat, numbers, stat0)
