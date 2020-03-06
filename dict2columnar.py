from itertools import imap

def consume_key(key="", values=dict()):
  v = values[key]
  c = v["consumer"]
  d = v["data"]
  return c(d)

def consume_dict(d=dict(), keys=[], result_consumer=sum):
  results = imap(partial(consume_key, values=d), keys)
  return result_consumer(results)
