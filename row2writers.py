from itertools import imap, ifilter, izip

def row2writers_dict(row=dict(), writers=dict(), writes2result=sum):
  keys = ifilter(lambda k: k in row, writers.iterkeys())
  writes = imap(lambda k: writers[k](row[k]), keys)
  return writes2result(writes)

def row2writers_list(row=list(), writers=list(), writes2result=sum):
  rw = izip(row, writers)
  writes = imap(lambda t: t[1](t[0]), rw)
  return writes2result(writes)
