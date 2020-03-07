from itertools import imap, ifilter

def row2writers_dict(row=dict(), writers=dict(), writes2result=sum):
  keys = ifilter(lambda k: k in row, writers.iterkeys())
  writes = imap(lambda k: writers[k](row[k]), keys)
  return writes2result(writes)
