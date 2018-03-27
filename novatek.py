#!/usr/bin/env python

import requests

from xml.etree import ElementTree

# Web server is running:
# http://www.rejetto.com/hfs/

class Novatek:
  BASE_URL = 'http://192.168.1.254'
  
  MODE = {
    'Video': 0,
    'Photo': 1,
    'Preview': 2
  }
  
  EV = {
    '+2.0': 0,
    '+1.7': 1,
    '+1.3': 2,
    '+1.0': 3,
    '+0.7': 4,
    '+0.3': 5,
    '0.0':  6,
    '-0.3': 7,
    '-0.7': 8,
    '-1.0': 9,
    '-1.3': 10,
    '-1.7': 11,
    '-2.0': 12
  }
  
  VIDEO_RESOLUTION = {
    # 4K?
    '1080p 60 FPS': 4,
    '1080p 30 FPS': 5,
    '720p 120 FPS': 6,
    '720p 60 FPS':  7,
    '720p 30 FPS':  8,
  }
  
  PHOTO_RESOLUTION = {
    '5120x3840': 0,
    '4608x3456': 1,
    '4032x3024': 2,
    '3648x2736': 3,
    '3264x2448': 4,
    '2592x1944': 5,
    '2048x1536': 6
  }
  
  def _get(self, cmd, params=[], url='/'):
    params = [('custom', '1'), ('cmd', cmd)] + params
    r = requests.get(Novatek.BASE_URL + url, params=params)
    return r
  
  def _get_xml(self, *args, **kwargs):
    r = self._get(*args, **kwargs)
    return ElementTree.fromstring(r.text)
  
  def take_photo(self):
    x = self._get_xml(1001)
    return x.find('./File/FPATH').text
  
  def set_photo_resolution(self, res):
    x = self._get_xml(1002, [('par', str(res))])
  
  def get_capture_num(self):
    '''The number of captures we can take with the remaining space'''
    x = self._get_xml(1003)
    return int(x.find('./Value').text)
  
  def start_record(self):
    return self._get(2001, [('str', '1')])
    
  def stop_record(self):
    return self._get(2001, [('str', '0')])
  
  def set_video_resolution(self, mode):
    return self._get(2002, [('par', str(mode))])
    
  def set_hdr(self, hdr):
    flag = '1' if hdr else '0'
    return self._get(2004, [('par', flag)])
  
  def set_ev(self, ev):
    return self._get(2005, [('par', str(ev))])
  
  def set_motion_detect(self, detect):
    flag = '1' if detect else '0'
    return self._get(2006, [('par', flag)])
  
  def set_audio_capture(self, capture):
    flag = '1' if capture else '0'
    return self._get(2007, [('par', flag)])
  
  def set_timestamp(self, stamp):
    flag = '1' if stamp else '0'
    return self._get(2008, [('par', flag)])
  
  # 2009: MAX_RECODE_TIME?
  
  def ping(self):
    # What does this do? Check battery?
    return self._get(2016)
      
  def set_mode(self, mode):
    return self._get(3001, [('par', str(mode))])
  
  def set_wifi_ssid(self, ssid):
    return self._get(3003, [('str', ssid)])
  
  def set_wifi_password(self, password):
    return self._get(3004, [('str', password)])
  
  def set_date(self, date):
    return self._get(3005, [('str', date.strftime("%Y-%m-%d"))])
  
  def set_time(self, time):
    return self._get(3006, [('str', time.strftime("%H:%M:%S"))])
  
  def format_sd(self):
    return self._get(3010, [('str', '1')])
  
  def reset_config(self):
    x = self._get_xml(3011)
  
  def get_config(self):
    x = self._get_xml(3014)
    config = { k.text: v.text for k, v in \
      zip(x.findall('./Cmd'), x.findall('./Status')) }
    return config
  
  def get_file_list(self):
    '''Returns a list of file paths, but does not include any metadata'''
    x = self._get_xml(3015)
    paths = []
    for file in x.findall('.//File'):
      paths.append(file.find('./FPATH').text)
    return paths
    
  # 3017? -> Value 32010764288, 32005423104... disk free space in bytes?
  # 3019? -> Value 1, or 5? something to do with charging?
  
  def has_sdcard(self):
    x = self._get_xml(3024)
    return x.find('./Value').text == '1'
  
  def delete_file(self, path):
    # Full Windows-style path, A:\Novatek\...
    x = self._get_xml(4003, [('str', path)])
  
  # 4004: delete all files?
  
  # TODO:
  # upload files
  
  def get_file(self, path):
    if path.startswith('A:\\'):
      path = path[2:].replace('\\', '/')
    return requests.get(BASE_URL + path).contents
  
  def get_file_thumbnail(self, path):
     if path.startswith('A:\\'):
       path = path[2:].replace('\\', '/')
     return self._get(4001, url=path).contents

