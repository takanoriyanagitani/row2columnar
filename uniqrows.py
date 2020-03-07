from heapq     import merge
from operator  import itemgetter
from itertools import imap

def merge_rows(r1=iter([]), r2=iter([]), r2k=itemgetter(0)):
  ti1 = imap(lambda row: (r2k(row), row), r1)
  ti2 = imap(lambda row: (r2k(row), row), r2)
  return merge(*(ti1, ti2))
