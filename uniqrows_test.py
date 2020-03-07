from operator import itemgetter

import uniqrows

def test_merge_rows():
  r1 = [
    dict(i=0, n="tt", h= 333),
    dict(i=1, n="st", h= 634),
    dict(i=2, n="mf", h=3776),
  ]
  r2 = [
    dict(i=0, n="tt", h= 333),
    dict(i=1, n="st", h= 634),
    dict(i=2, n="mf", h=3776),
    dict(i=3, n="mt", h= 599),
  ]
  r2k = itemgetter("i")

  a = list(uniqrows.merge_rows(r1, r2, r2k))
  assert 7 == len(a)
  assert tuple == type(a[0])
  assert tuple == type(a[1])
  assert tuple == type(a[2])
  assert tuple == type(a[3])
  assert tuple == type(a[4])
  assert tuple == type(a[5])
  assert tuple == type(a[6])

  a0 = a[0]
  a1 = a[1]
  a2 = a[2]
  a3 = a[3]
  a4 = a[4]
  a5 = a[5]
  a6 = a[6]

  assert 2 == len(a0)
  assert 2 == len(a1)
  assert 2 == len(a2)
  assert 2 == len(a3)
  assert 2 == len(a4)
  assert 2 == len(a5)
  assert 2 == len(a6)

  assert int == type(a0[0])
  assert int == type(a1[0])
  assert int == type(a2[0])
  assert int == type(a3[0])
  assert int == type(a4[0])
  assert int == type(a5[0])
  assert int == type(a6[0])

  assert 0 == a0[0]
  assert 0 == a1[0]
  assert 1 == a2[0]
  assert 1 == a3[0]
  assert 2 == a4[0]
  assert 2 == a5[0]
  assert 3 == a6[0]

  assert dict == type(a0[1])
  assert dict == type(a1[1])
  assert dict == type(a2[1])
  assert dict == type(a3[1])
  assert dict == type(a4[1])
  assert dict == type(a5[1])
  assert dict == type(a6[1])

  assert dict(i=0, n="tt", h= 333) == a0[1]
  assert dict(i=0, n="tt", h= 333) == a1[1]
  assert dict(i=1, n="st", h= 634) == a2[1]
  assert dict(i=1, n="st", h= 634) == a3[1]
  assert dict(i=2, n="mf", h=3776) == a4[1]
  assert dict(i=2, n="mf", h=3776) == a5[1]
  assert dict(i=3, n="mt", h= 599) == a6[1]

def test_merged_rows2uniq():
  rows = iter([
    dict(n="tt", h=333),
    dict(n="tt", h=333),
    dict(n="st", h=634),
    dict(n="mt", h=599),
  ])
  r2k = itemgetter("n")
  uniq = list(uniqrows.merged_rows2uniq(rows, r2k))

  assert 3 == len(uniq)
  a0 = uniq[0]
  a1 = uniq[1]
  a2 = uniq[2]

  assert dict == type(a0)
  assert dict == type(a1)
  assert dict == type(a2)

  assert dict(n="tt", h=333) == a0
  assert dict(n="st", h=634) == a1
  assert dict(n="mt", h=599) == a2
