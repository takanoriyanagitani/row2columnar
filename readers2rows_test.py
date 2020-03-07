import json
import struct
import os
from cStringIO import StringIO

import readers2rows

def test_column2i_text():
  jsonl = iter([
    json.dumps("helo")+"\n",
    json.dumps("helo, wrld")+"\n",
  ])
  e = [
    "helo",
    "helo, wrld",
  ]
  a = list(readers2rows.column2i_text(jsonl))
  assert e[0] == a[0]
  assert e[1] == a[1]

  i2 = iter([
    "634",
    "333",
  ])
  e2 = [
    "634",
    "333",
  ]
  a2 = list(readers2rows.column2i_text(i2, t2v=lambda s: s))
  assert e2[0] == a2[0]
  assert e2[1] == a2[1]
  pass

def test_nan2alt():
  assert 0.0 == readers2rows.nan2alt()
  assert 0.0 == readers2rows.nan2alt(0.0)
  assert 0.0 == readers2rows.nan2alt(0.0, 0.0)
  assert 0.0 == readers2rows.nan2alt(float("nan"), 0.0)
  assert 1.0 == readers2rows.nan2alt(float("nan"), 1.0)
  assert 1.0 == readers2rows.nan2alt(1.0,          0.0)

def test_lebytes2float_slow():
  assert 0.0 == readers2rows.lebytes2float_slow()
  assert 0.0 == readers2rows.lebytes2float_slow(struct.pack("<d", 0.0))
  assert 1.0 == readers2rows.lebytes2float_slow(struct.pack("<d", 1.0))
  assert 0.0 == readers2rows.lebytes2float_slow(struct.pack("<d", float("nan")))
  assert 0.0 == readers2rows.lebytes2float_slow(struct.pack("<h", 1))

def test_lebytes2float_fast():
  assert 0.0 == readers2rows.lebytes2float_fast(struct.pack("<d", 0.0))
  assert 1.0 == readers2rows.lebytes2float_fast(struct.pack("<d", 1.0))
  assert 0.0 == readers2rows.lebytes2float_fast(struct.pack("<d", float("nan")))

def test_lebytes2avx256d_slow():
  assert (0.0, 0.0, 0.0, 0.0) == readers2rows.lebytes2avx256d_slow()
  assert (0.0, 0.0, 0.0, 0.0) == readers2rows.lebytes2avx256d_slow(struct.pack("<dddd", 0,0,0,0))
  i = struct.pack("<dddd", 0.0, 1.0, 2.0, float("nan"))
  e = (0.0, 1.0, 2.0, 0.0)
  a = readers2rows.lebytes2avx256d_slow(i)
  assert e[0] == a[0]
  assert e[1] == a[1]
  assert e[2] == a[2]
  assert e[3] == a[3]

def test_lebytes2avx256d_fast():
  assert (0.0, 0.0, 0.0, 0.0) == readers2rows.lebytes2avx256d_fast(struct.pack("<dddd", 0,0,0,0))
  i = struct.pack("<dddd", 0.0, 1.0, 2.0, float("nan"))
  e = (0.0, 1.0, 2.0, 0.0)
  a = readers2rows.lebytes2avx256d_fast(i)
  assert e[0] == a[0]
  assert e[1] == a[1]
  assert e[2] == a[2]
  assert e[3] == a[3]

def test_column2i_ledouble():
  s = StringIO()
  s.write(struct.pack("<d", 0.0))
  s.write(struct.pack("<d", 1.0))
  s.write(struct.pack("<d", 2.0))
  s.write(struct.pack("<d", float("nan")))
  s.seek(0, os.SEEK_SET)
  e = [ 0.0, 1.0, 2.0, 0.0 ]
  a = list(readers2rows.column2i_ledouble(s))
  assert e[0] == a[0]
  assert e[1] == a[1]
  assert e[2] == a[2]
  assert e[3] == a[3]
  s.close()

def test_column2i_leavx256d():
  s = StringIO()

  s.write(struct.pack("<d", 0.0))
  s.write(struct.pack("<d", 1.0))
  s.write(struct.pack("<d", 2.0))
  s.write(struct.pack("<d", float("nan")))

  s.write(struct.pack("<d", 4.0))
  s.write(struct.pack("<d", 5.0))
  s.write(struct.pack("<d", 6.0))
  s.write(struct.pack("<d", 7.0))

  s.seek(0, os.SEEK_SET)
  e = [
    (0.0, 1.0, 2.0, 0.0),
    (4.0, 5.0, 6.0, 7.0),
  ]
  a = list(readers2rows.column2i_leavx256d(s))
  assert tuple == type(a[0])
  assert tuple == type(a[1])
  assert 4 == len(a[0])
  assert 4 == len(a[1])
  assert e[0] == a[0]
  assert e[1] == a[1]
  s.close()

def test_readers2iterators():
  sf = StringIO()
  st = StringIO()
  sf.write(struct.pack("<dddd", 0.0,1.0,2.0,float("nan")))
  st.writelines(iter([
    json.dumps("hw")+"\n",
    json.dumps("helo")+"\n",
    json.dumps("h,w")+"\n",
    json.dumps("helo, world")+"\n",
  ]))
  sf.seek(0)
  st.seek(0)
  readers = [sf, st]
  r2i = [readers2rows.column2i_ledouble, readers2rows.column2i_text]

  a = readers2rows.readers2iterators(readers, r2i)
  assert list == type(a)
  assert 2 == len(a)
  i0 = a[0]
  i1 = a[1]
  lf = list(i0)
  lt = list(i1)
  assert 4 == len(lf)
  assert 4 == len(lt)
  assert [0.0, 1.0, 2.0, 0.0] == lf
  assert [
    "hw",
    "helo",
    "h,w",
    "helo, world",
  ] == lt
