#!/usr/bin/env python

import datetime
import logging
import os
import re
import subprocess
import time

from novatek import Novatek


logging.basicConfig(
  datefmt='%m-%d-%y %H:%M:%S',
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.INFO
)


logging.info('Configuring camera')
N = Novatek()
N.set_mode(Novatek.MODE['Video'])  # needs to be in video mode to take photos??


def capture():
  logging.info('Starting capture')
  try:
    N.take_photo()
  except Exception as e:
    logging.exception('Capture failed')

def get_remaining_captures():
  try:
    x = N.get_capture_num()
    logging.info('Space remaining to store %i photos', x)
    return x
  except Exception as e:
    logging.exception('Failed to get remaining space')
    return 1000

# Capture
while True:
  capture()
  while get_remaining_captures() < 20:
    files = N.get_file_list()
    oldest = files[0]  # big assumption that this is oldest
    logging.warn('Disk space is too low, purging %s', oldest)
    Novatek().delete_file(oldest)
  time.sleep(60)
