#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
  import cv2
  has_cv = True
except:
  has_cv = False

try:
  import picamera
  has_picamera = True
except:
  has_picamera = False

from datetime import datetime
from os import path
import argparse
import os
import subprocess
import sys
import threading

import util


###############################################################################
# Arguments
###############################################################################
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--camera', dest='camera_id', action='store', default=-1, type=int,
  help='The index of the camera. Skip this to get the default camera.',
)
parser.add_argument('-i', '--interval', dest='interval', action='store', default=10, type=float,
  help='How often the snapshots will be taken in seconds (default: 10s).',
)
parser.add_argument('-n', '--name', dest='name', action='store', default='my-camera',
  help='''
    Name for the camera feed. Only lowercase letters (a-z), numbers (0-9) and
    dashes (-) are allowed. Maximum length should be 32 characters.
  ''',
)
parser.add_argument('-s', '--size', dest='size', action='store', default='640x480',
  help='Set the size of the image (default: 640x480)',
)
parser.add_argument('-r', '--rotation', dest='rotation', action='store', default=0, type=int,
  help='Set image rotation for PiCamera or fswebcam (90, 180, 270).',
)
parser.add_argument('--fswebcam', dest='fswebcam', action='store_true',
  help='Use fswebcam package.',
)

args = parser.parse_args()


###############################################################################
# Camera
###############################################################################
class Camera(object):
  def __init__(self, *arg, **kwargs):
    self.name = util.slugify(kwargs.pop('name', 'my-camera'))
    self.directory = kwargs.pop('directory', path.dirname(path.realpath(__file__)))
    self.width = kwargs.pop('width', 640)
    self.height = kwargs.pop('height', 480)
    self.rotation = kwargs.pop('rotation', 0)
    self.init_camera()
    if self.is_working():
      util.print_out('CAMERA LOADED', self.full_name())
    else:
      util.print_out('CAMERA FAILD', self.full_name())

  def init_camera(self):
    pass

  def is_working():
    return False

  def get_fullname(self):
    timestamp = datetime.utcnow()
    dirname = path.join(self.directory, self.name, timestamp.strftime('%Y-%m-%d-%H-00'))
    filename = util.set_filename(self.name, timestamp)
    util.make_dirs(dirname)
    return path.join(dirname, filename)

  def save(self):
    pass

  def close(self):
    pass

  def full_name(self):
    return '%s (%dx%d)' % (self.name, self.width, self.height)


###############################################################################
# OpenCV Camera
###############################################################################
class CVCamera(Camera):
  def __init__(self, *arg, **kwargs):
    self.capture = cv2.VideoCapture(kwargs.pop('camera_id'))
    Camera.__init__(self, *arg, **kwargs)

  def init_camera(self, **kwargs):
    self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.width)
    self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.height)

  def is_working(self):
    return self.capture.read() is not None

  def save(self):
    retval, image = self.capture.read()
    filename = self.get_fullname()
    cv2.imwrite(filename, image)
    util.print_out('SAVED', path.basename(filename))

  def close(self):
    self.capture.release()


###############################################################################
# PiCamera
###############################################################################
class PiCamera(Camera):
  def __init__(self, *arg, **kwargs):
    self.camera = picamera.PiCamera()
    Camera.__init__(self, *arg, **kwargs)

  def init_camera(self, **kwargs):
    self.camera.rotation = self.rotation
    self.camera.resolution = (self.width, self.height)

  def is_working(self):
    return bool(self.camera)

  def save(self):
    filename = self.get_fullname()
    self.camera.capture(filename)
    util.print_out('SAVED', path.basename(filename))

  def close(self):
    self.camera.close()


###############################################################################
# FSWebCam - A hackky way using fswebcam command
###############################################################################
class FSWebCamera(Camera):
  def is_working(self):
    cmd = 'fswebcam /dev/null'
    try:
      result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except:
      return False
    return result.find('Writing JPEG image to') != -1

  def save(self):
    filename = self.get_fullname()
    cmd = 'fswebcam -r %dx%d --no-banner --rotate %d %s' % (
      self.width, self.height, self.rotation, filename,
    )
    try:
      result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
      if result.find('Writing JPEG image to') != -1:
        util.print_out('SAVED', path.basename(filename))
        return True
    except subprocess.CalledProcessError:
      pass

    util.print_out('FAILED', path.basename(filename))
    return False


###############################################################################
# Main
###############################################################################
root = path.dirname(path.realpath(__file__))


def next_capture(camera):
  thread = threading.Timer(args.interval, next_capture, args=[camera])
  thread.start()
  camera.save()


def start_camera():
  camera = None
  try:
    width = int(args.size.split('x')[0])
    height = int(args.size.split('x')[1])
  except:
    raise sys.exit('Wrong size format. e.g. 800x600, 640x480, 320x240...')

  settings = {
    'width': width,
    'height': height,
    'name': args.name,
    'directory': path.join(root, 'feed'),
    'rotation': args.rotation,
  }

  if args.fswebcam:
    util.print_out('CAMERA INIT', args.name)
    camera = FSWebCamera(**settings)
  elif has_cv:
    util.print_out('CAMERA INIT', '%s (%d)' % (args.name, args.camera_id))
    camera = CVCamera(camera_id=args.camera_id, **settings)
  elif has_picamera:
    util.print_out('CAMERA INIT', args.name)
    camera = PiCamera(**settings)

  if camera and camera.is_working():
    next_capture(camera)


if __name__ == '__main__':
  name = args.name.lower()
  if name != util.slugify(unicode(name)) or len(name) > 32:
    raise sys.exit('''
      Bad camera name. Only lowercase letters (a-z), numbers (0-9) and
      dashes (-) are allowed. Maximum length should be 32 characters.
    ''')

  start_camera()
