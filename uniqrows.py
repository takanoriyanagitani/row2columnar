from heapq     import merge
from operator  import itemgetter
from itertools import imap, groupby, islice

def merge_rows(r1=iter([]), r2=iter([]), r2k=itemgetter(0)):
  ti1 = imap(lambda row: (r2k(row), row), r1)
  ti2 = imap(lambda row: (r2k(row), row), r2)
  return merge(*(ti1, ti2))

def i2r_default(i=iter([])): return list(islice(i, 1))

def l1st_alt(l=list(), alt=None): return alt if len(l) < 1 else l[0]

def g2r_default(t=tuple(), iter2row=i2r_default, alt=None):
  k = t[0]
  i = t[1]
  r = iter2row(i)
  return l1st_alt(r, alt)

def merged_rows2uniq(rows=iter([]), r2k=itemgetter(0), group2row=g2r_default):
  grouped = groupby(rows, r2k)
  return imap(g2r_default, grouped)
