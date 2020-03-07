import json
import struct
import math
import sys
from itertools import imap, repeat, takewhile
from operator  import methodcaller

def nnan(f=0.0): return not math.isnan(f)
def nan2alt(f=0.0, alt=0.0): return nnan(f) and f or alt
def lebytes2float_slow(b=None, f=nan2alt):
  valid   = bytes == type(b) and 8 == len(b)
  invalid = not valid
  return f(
    invalid and float("nan") or struct.unpack("<d", b)[0]
  )
def lebytes2float_fast(b=None, f=nan2alt): return f(struct.unpack("<d", b)[0])

def lebytes2avx256d_slow(b=None, f=nan2alt):
  valid   = bytes == type(b) and 32 == len(b)
  invalid = not valid
  t = invalid and (
    float("nan"),
    float("nan"),
    float("nan"),
    float("nan"),
  ) or struct.unpack("<dddd", b)
  return (
    f(t[0]),
    f(t[1]),
    f(t[2]),
    f(t[3]),
  )

def lebytes2avx256d_fast(b=None, f=nan2alt):
  t = struct.unpack("<dddd", b)
  return (
    f(t[0]),
    f(t[1]),
    f(t[2]),
    f(t[3]),
  )

def column2i_text(i=iter([]), t2v=json.loads): return imap(t2v, i)

def column2i_ledouble(i=sys.stdin, f=nan2alt):
  reads = imap(methodcaller("read", 8), repeat(i))
  limited = takewhile(lambda b: bytes == type(b) and 8 == len(b), reads)
  return imap(lebytes2float_fast, limited)

def column2i_leavx256d(i=sys.stdin, f=nan2alt):
  reads = imap(methodcaller("read", 32), repeat(i))
  limited = takewhile(lambda b: bytes == type(b) and 32 == len(b), reads)
  return imap(lebytes2avx256d_fast, limited)

#def readers2rows(readers=list()):
#  pass
