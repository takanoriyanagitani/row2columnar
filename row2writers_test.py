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
