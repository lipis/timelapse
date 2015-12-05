#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import getpass
import json
import logging
import os
import Queue
import requests
import threading

import util


HOST_URL = 'https://pss-camera.appspot.com'
SIGNIN_URL = '%s/api/v1/auth/signin/' % (HOST_URL)
UPLOAD_URL = '%s/api/v1/resource/upload/' % (HOST_URL)

root = os.path.dirname(os.path.realpath(__file__))
dir_feed = os.path.join(root, 'feed')
interval = 4
upload_queue = Queue.Queue()
parsed = {}
lock = threading.RLock()
headers = None
last_report = ''


###############################################################################
# Arguments
###############################################################################
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--threads', dest='threads', action='store', default=4, type=int)
parser.add_argument('-u', '--username', dest='username', action='store')
parser.add_argument('-p', '--password', dest='password', action='store')
parser.add_argument('-c', '--cookie', dest='cookie', action='store')
args = parser.parse_args()


###############################################################################
# Auth Stuff
###############################################################################
def get_cookie():
  if args.cookie:
    return args.cookie
  username = args.username or raw_input('Username: ')
  password = args.password or getpass.getpass()

  args.username = None
  args.password = None

  payload = {'username': username, 'password': password}
  r = requests.post(SIGNIN_URL, params=payload)
  response = json.loads(r.text)
  if response['status'] == 'success':
    cookie = r.headers['set-cookie'].split(';')[0]
    return cookie
  else:
    print 'Wrong Username or Password!'
    return None


###############################################################################
# Parse Stuff
###############################################################################
def parse_dir(directory):
  global upload_queue
  global last_cache
  global parsed
  global last_report
  if not headers:
    return

  all_files = []
  for root, dirs, files in os.walk(directory):
    if files:
      for filename in files:
        full_filename = os.path.join(root, filename)
        if full_filename.endswith('.jpg'):
          all_files.append(full_filename)
        if full_filename.endswith('.DS_Store'):
          os.remove(full_filename)
    elif not (dirs or files):
      try:
        os.rmdir(root)
      except Exception as e:
        util.print_out('REMOVE EXCEPTION', os.path.basename(filename))
        util.print_out('EXCEPTION', e)

  all_files.sort(reverse=True)
  count = 0
  for filename in all_files:
    if filename not in parsed:
      parsed[filename] = True
      upload_queue.put(filename)
      count += 1

      if count == args.threads:
        break

  count_parsed = len(parsed)
  counte_all = len(all_files)
  report = '+%d (%d of %d)' % (count, len(parsed), len(all_files))
  if report != last_report:
    util.print_out('QUEUE', report)

  last_report = report

def pop_parsed(filename, all=False):
  global parsed
  lock.acquire()
  try:
    parsed.pop(filename, None)
  finally:
    lock.release()


###############################################################################
# Upload Stuff
###############################################################################
def upload_file(filename):
  global parsed
  global headers
  try:
    image_file = open(filename, 'rb')
  except Exception as e:
    util.print_out('OPEN EXCEPTION', os.path.basename(filename))
    pop_parsed(filename)
    return

  try:
    req = requests.get(UPLOAD_URL, headers=headers)
    response = json.loads(req.text)
  except Exception as e:
    util.print_out('EXCEPTION GET', e.message)
    return

  if response['status'] == 'success':
    upload_url = response['result'][0]['upload_url']
    files = {'file': (os.path.basename(filename), image_file, 'image/jpeg')}
    util.print_out('UPLOADING', os.path.basename(filename))

    try:
      req_upload = requests.post(upload_url, files=files, headers=headers)
      json_upload = json.loads(req_upload.text)
      image_file.close()
      if json_upload['status'] == 'success':
        try:
          os.remove(filename)
        except Exception as e:
          util.print_out('REMOVE EXCEPTION', os.path.basename(filename))
          util.print_out('EXCEPTION', e)
        util.print_out('DONE', os.path.basename(filename))
      else:
        util.print_out('ERROR', os.path.basename(filename))
        print json.dumps(json_upload, sort_keys=True, indent=2)

    except Exception as e:
      util.print_out('UPLOAD EXCEPTION', os.path.basename(filename))
      util.print_out('EXCEPTION POST', e.message)

    pop_parsed(filename)
  else:
    headers = None


###############################################################################
# Threads Stuff
###############################################################################
def upload_file_queue(queue):
  while headers:
    filename = queue.get()
    upload_file(filename)
    queue.task_done()


def next_parse():
  if headers:
    threading.Timer(interval, next_parse).start()
    parse_dir(dir_feed)


###############################################################################
# Main Shit
###############################################################################
if __name__ == '__main__':
  #TODO: Handle that https://goo.gl/UoVZsK.
  logging.captureWarnings(True)

  for _ in range(3):
    cookie = get_cookie()
    if cookie:
      headers = {'Cookie': cookie}
      break

  if not headers:
    raise sys.exit('Sorry, try again later!')

  for _ in range(args.threads):
    worker = threading.Thread(target=upload_file_queue, args=(upload_queue,))
    worker.setDaemon(True)
    worker.start()

  next_parse()

  parse_dir(dir_feed)
  filename = upload_queue.get()
  upload_file(filename)
