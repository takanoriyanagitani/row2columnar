import struct
import json
from cStringIO import StringIO

import row2writers

def test_row2writers_dict():
  row = dict(i=0, n="c", v=2.99792458)

  fi = StringIO()
  fn = StringIO()
  fv = StringIO()

  si = lambda v: struct.pack("<q", v)
  sn = lambda v: json.dumps(v)+"\n"
  sv = lambda v: struct.pack("<d", v)

  wi = lambda v: fi.write(si(v)) or 1
  wn = lambda v: fn.write(sn(v)) or 1
  wv = lambda v: fv.write(sv(v)) or 1

  writers = dict(i=wi, n=wn, v=wv)

  a = row2writers.row2writers_dict(row, writers)

  assert 3 == a

  fi.seek(0)
  fn.seek(0)
  fv.seek(0)

  bi = fi.read(8)
  bn = fn.read(3)
  bv = fv.read(8)

  assert 8 == len(bi)
  assert 3 == len(bn)
  assert 8 == len(bv)

  assert 0          == struct.unpack("<q", bi)[0]
  assert 2.99792458 == struct.unpack("<d", bv)[0]

  jn = json.loads(bn)
  assert "c" == jn

def test_row2writers_list():
  row = [0, "mfkm", 3.776]

  f0 = StringIO()
  f1 = StringIO()
  f2 = StringIO()

  s0 = lambda v: struct.pack("<q", v)
  s1 = lambda v: json.dumps(v)+"\n"
  s2 = lambda v: struct.pack("<d", v)

  w0 = lambda v: f0.write(s0(v)) or 1
  w1 = lambda v: f1.write(s1(v)) or 1
  w2 = lambda v: f2.write(s2(v)) or 1

  writers = [w0, w1, w2]

  a = row2writers.row2writers_list(row, writers)

  assert 3 == a

  f0.seek(0)
  f1.seek(0)
  f2.seek(0)

  b0 = f0.read(8)
  b1 = f1.read(7)
  b2 = f2.read(8)

  assert 8 == len(b0)
  assert 7 == len(b1)
  assert 8 == len(b2)

  assert 0     == struct.unpack("<q", b0)[0]
  assert 3.776 == struct.unpack("<d", b2)[0]

  j1 = json.loads(b1)
  assert "mfkm" == j1
