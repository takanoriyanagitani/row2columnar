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

def float_add(a=0.0, b=0.0):
  invalid_a = float != type(a) or math.isnan(a)
  invalid_b = float != type(b) or math.isnan(b)
  na = 0.0 if invalid_a else a
  nb = 0.0 if invalid_b else b
  return na + nb

def m256d_add(a=(0.0,0.0,0.0,0.0), b=(0.0,0.0,0.0,0.0), z=(0.0,0.0,0.0,0.0)):
  na = z if None == a else a
  nb = z if None == b else b
  return (
    float_add(na[0], nb[0]),
    float_add(na[1], nb[1]),
    float_add(na[2], nb[2]),
    float_add(na[3], nb[3]),
  )

def m256d_max(a=(0.0,0.0,0.0,0.0), b=(0.0,0.0,0.0,0.0), z=(None,None,None,None)):
  na = z if None == a else a
  nb = z if None == b else b
  return (
    max_float(na[0], nb[0]),
    max_float(na[1], nb[1]),
    max_float(na[2], nb[2]),
    max_float(na[3], nb[3]),
  )

def m256d_min(a=(0.0,0.0,0.0,0.0), b=(0.0,0.0,0.0,0.0), z=(None,None,None,None)):
  na = z if None == a else a
  nb = z if None == b else b
  return (
    min_float(na[0], nb[0]),
    min_float(na[1], nb[1]),
    min_float(na[2], nb[2]),
    min_float(na[3], nb[3]),
  )

def m256d2stat_default(stat=dict(), m256d=(0.0,0.0,0.0,0.0), alt=0.0):
  stat["sum"] = m256d_add(stat.get("sum", (0,0,0,0,0,0,0,0)), m256d)
  stat["max"] = m256d_max(stat.get("max", None), m256d)
  stat["min"] = m256d_min(stat.get("min", None), m256d)
  return stat

def numbers2stat_m256d(d256bits=iter([]), m256d2stat=m256d2stat_default, stat0=dict()):
  return reduce(m256d2stat, d256bits, stat0)
