import math

def number_alt_float_none(f=0.0, alt=0.0): return alt if None == f else f
def number_alt_float_nan(f=0.0, alt=0.0):  return alt if math.isnan(f) else f
def number_alt_float_nn(f=0.0, alt=0.0):
  return number_alt_float_nan(
    number_alt_float_none(f, alt),
    alt
  )
