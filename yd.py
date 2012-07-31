#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib
import sys

KEY = 555326493
USER = 'cassvin'
URL = 'http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=json&version=1.1&q=' % (USER, KEY)

class NoneError(Exception):
  pass


def tr(q):
  if not q:
    raise NoneError
  url = URL + urllib.quote(q)
  resp = urllib.urlopen(url)
  i = resp.read()
  resp.close()
  return extract_json(i)
  

def extract_json(i):
  rs = []
  t = ''
  i_dic = json.loads(i)
  rs.append('[ translation ]')
  rs.append(i_dic['translation'][0])
  basic = i_dic.get('basic')
  if basic:
    if basic.get('phonetic'):
      rs[-1] = rs[-1] + '   ' + i_dic['basic']['phonetic']
    if basic.get('explains'):
      rs.append('[ explains ]')
      rs.append('\n'.join(basic['explains']))
  web = i_dic.get('web')
  if web:
    rs.append('[ phrase ]')
    for e in web:
      t = e['key'].ljust(24) + ','.join(e['value']) 
      rs.append(t)
  rs.append('[ End ]')
  o = '\n'.join(rs)
  return o
  

if __name__ == '__main__':
  print 'Welcome to Leon Hui\'s translator gadget!' 
  while True:
    try:
      q = raw_input('>>> ').strip()
      o = tr(q)
    except NoneError:
      continue
    except KeyboardInterrupt:
      print '\r'
      continue
    except EOFError:
      print '\r'
      sys.exit(0)
    except IOError, e:
      print 'Error: %s' % e
      continue
    else:
      print o

