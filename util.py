# -*- coding: utf-8 -*-

import os
import shutil
from datetime import datetime
import re
import unicodedata


def make_dirs(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)


def remove_dir(directory):
  if os.path.isdir(directory):
    shutil.rmtree(directory)


def print_out(line=None, value=None):
  timestamp = datetime.now().strftime('%H:%M:%S')
  if value is not None and not line:
    line = value
    value = None
  if not line:
    line = '-' * 64
  if value is not None:
    print '[%s] %16s: %s' % (timestamp, line, value)
  else:
    print '[%s] %s' % (timestamp, line)


_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')


def slugify(text):
  if not isinstance(text, unicode):
    text = unicode(text)
  text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
  text = unicode(_slugify_strip_re.sub('', text).strip().lower())
  return _slugify_hyphenate_re.sub('-', text)


def set_filename(name, timestamp=None):
  timestamp = timestamp or datetime.utcnow()
  filename = timestamp.strftime('%Y-%m-%d-%H-%M-%S-%f.jpg')
  return '%s~%s' % (slugify(name), filename)


def split_filename(filename):
  try:
    root = os.path.splitext(filename)[0]
    parts = root.split('~')
    if len(parts) == 1:
      name = 'pss-camera'
      timestamp = parts[0]
    else:
      name = slugify(parts[0])
      timestamp = parts[1]

    dt = [2015, 1, 1, 0, 0, 0, 0]
    tok = map(int, (x for x in timestamp.split('-')))
    for i in range(len(tok)):
      dt[i] = tok[i]

    return name, datetime(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6])
  except:
    return None, None


if __name__ == '__main__':
  print ''
  print split_filename('FOO BAR~2015-10-17-02-34-22-847043.jpg')
  print split_filename('nice~2015-10.jpg')
  print split_filename(set_filename('foobar'))
  print split_filename('201sd5-sd10-17-02-34.jpg')
  print create_name_from_email('pss-camera')
