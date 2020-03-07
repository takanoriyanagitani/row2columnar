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

def test_iterators2rows_t():
  i1 = iter([0,1,2])
  i2 = iter([3,4])
  e  = [
    (0, 3),
    (1, 4),
    (2, None),
  ]
  a  = list(readers2rows.iterators2rows_t((i1, i2)))
  assert a == e

def test_iterators2rows_l():
  i1 = iter([0,1,2])
  i2 = iter(["3","4"])
  e  = [
    (0, "3"),
    (1, "4"),
    (2, None),
  ]
  a  = list(readers2rows.iterators2rows_l([i1, i2]))
  assert a == e

def test_readers2rows():
  ri = StringIO()
  rt = StringIO()
  ra = StringIO()

  ri.write(struct.pack("<qqq", 333, 634, 3776))
  rt.writelines(iter([
    json.dumps("tt")+"\n",
    json.dumps("st")+"\n",
    json.dumps("mf")+"\n",
  ]))
  nan = float("nan")
  ra.write(struct.pack("<dddd", 0.0, 1.0, 2.0, nan))
  ra.write(struct.pack("<dddd", 1.0, 2.0, nan, 4.0))
  ra.write(struct.pack("<dddd", 2.0, nan, 4.0, 5.0))
  ra.write(struct.pack("<dddd", nan, 4.0, 5.0, 6.0))

  ri.seek(0)
  rt.seek(0)
  ra.seek(0)

  readers = [ ri, rt, ra ]
  r2i = [
    readers2rows.column2i_leint64,
    readers2rows.column2i_text,
    readers2rows.column2i_leavx256d,
  ]
  a = list(readers2rows.readers2rows(readers, r2i))

  assert 4 == len(a)
  a0 = a[0]
  a1 = a[1]
  a2 = a[2]
  a3 = a[3]

  assert tuple == type(a0)
  assert tuple == type(a1)
  assert tuple == type(a2)
  assert tuple == type(a3)

  assert 3 == len(a0)
  assert 3 == len(a1)
  assert 3 == len(a2)
  assert 3 == len(a3)

  assert type(a0[0]) in [long, int]
  assert type(a1[0]) in [long, int]
  assert type(a2[0]) in [long, int]
  assert None == a3[0]
  assert 333  == a0[0]
  assert 634  == a1[0]
  assert 3776 == a2[0]

  assert type(a0[1]) in [str, unicode, bytes]
  assert type(a1[1]) in [str, unicode, bytes]
  assert type(a2[1]) in [str, unicode, bytes]
  assert None == a3[1]
  assert "tt" == a0[1]
  assert "st" == a1[1]
  assert "mf" == a2[1]

  assert tuple == type(a0[2])
  assert tuple == type(a1[2])
  assert tuple == type(a2[2])
  assert tuple == type(a3[2])

  avx0 = a0[2]
  avx1 = a1[2]
  avx2 = a2[2]
  avx3 = a3[2]

  assert 4 == len(avx0)
  assert 4 == len(avx1)
  assert 4 == len(avx2)
  assert 4 == len(avx3)

  assert (0.0, 1.0, 2.0, 0.0) == avx0
  assert (1.0, 2.0, 0.0, 4.0) == avx1
  assert (2.0, 0.0, 4.0, 5.0) == avx2
  assert (0.0, 4.0, 5.0, 6.0) == avx3
  pass
