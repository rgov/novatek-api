#!/usr/bin/env python

import datetime
import logging
import os
import re
import requests
import subprocess
import sys
import threading
import time

import status

from novatek import Novatek


logging.basicConfig(
  datefmt='%m-%d-%y %H:%M:%S',
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.INFO
)


N = Novatek()


logging.info('Waiting for camera on network')
status.led_on()
while True:
  try:
    N.ping()
    break
  except requests.exceptions.ConnectionError:
    pass
  except KeyboardInterrupt:
    sys.exit(1)
  except Exception:
    logging.exception('Unhandled exception while waiting for camera')
    raise
  time.sleep(1.0)


logging.info('Configuring camera')
N.set_mode(Novatek.MODE['Video'])  # needs to be in video mode to take photos??


def capture():
  logging.info('Starting capture')
  try:
    N.take_photo()
    return True
  except Exception as e:
    logging.exception('Capture failed')
    raise

def get_remaining_captures():
  try:
    x = N.get_capture_num()
    logging.info('Space remaining to store %i photos', x)
    return x
  except Exception as e:
    logging.exception('Failed to get remaining space')
    raise

def report_status(healthy):
  threading.Thread(target=status.report_status, args=(healthy,)).start()

# Capture
while True:
  healthy = True
  
  try:
    capture()
    while get_remaining_captures() < 20:
      files = N.get_file_list()
      oldest = files[0]  # big assumption that this is oldest
      logging.warn('Disk space is too low, purging %s', oldest)
      Novatek().delete_file(oldest)
  except KeyboardInterrupt:
    break
  except Exception:
    healthy = False
  
  report_status(healthy)
  time.sleep(30)
