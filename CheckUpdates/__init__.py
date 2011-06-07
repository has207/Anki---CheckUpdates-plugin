# -*- coding: utf-8 -*-
# Author: Herman Sheremetyev <herman@swebpage.com>
# License: WTFPL, version 2 or later; http://sam.zoy.org/wtfpl/COPYING

import cStringIO
import gzip
import simplejson
import urllib2

def get_data():
  sock = urllib2.urlopen("http://ankiweb.net/file/search?t=1&c=1")
  data = sock.read()
  try:
    data = gzip.GzipFile(fileobj=cStringIO.StringIO(data)).read()
  except:
    # the server is sending gzipped data, but a transparent
    # proxy or antivirus software may be decompressing it
    # before we get it
    pass
  return simplejson.loads(unicode(data))


def check_for_updates():
  registered = []
  current = {}
  for val in mw.registeredPlugins.values():
    registered.append(unicode(val['name']))
  plugin_data = get_data()
  for plugin in plugin_data:
    if unicode(plugin[2]) in registered:
      current[plugin[2]] = plugin[9]

  raise Exception, '%s %s' % (registered, current)


from ankiqt import mw
mw.registerPlugin("Check Updates", 976)

from anki.hooks import addHook
addHook('init', check_for_updates)
