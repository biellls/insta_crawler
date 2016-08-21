import argparse
import platform
from selenium import webdriver
import os
import urllib2
import re
import json
import logging


def __get_phantomjs_path_for_platform():
  if platform.system() == 'Windows':
    return './phantomjs.exe'
  else:
    return './phantomjs'


def get_phantomjs_browser():
  PHANTOMJS_PATH = __get_phantomjs_path_for_platform()
  return webdriver.PhantomJS(PHANTOMJS_PATH)


def get_rendered_javascript(url, browser=None):
  browser = browser or get_phantomjs_browser()
  browser.get(url)
  return browser.page_source


def get_max_id(html):
  search_obj = re.search('max_id=([0-9]+)">', html)
  json_obj = json.loads(search_obj.group(1))
  return json_obj

def get_urls_npages(profile, npages=1):
  """
  Given the number of pages to show returns the url to display all of them
  """
  browser = get_phantomjs_browser()
  url = 'https://www.instagram.com/{}/'.format(profile)
  html = get_rendered_javascript(url, browser)
  urls = [url]
  while npages > 1:
    max_id = get_max_id(html)
    url = 'https://www.instagram.com/{}/?max_id={}'.format(profile, max_id)
    html = get_rendered_javascript(url, browser)
    npages -= 1
    urls.append(url)
  return urls

def download_from_profile(profile, max_id=None):
  if max_id is not None:
    url = 'https://www.instagram.com/{}/?max_id={}'.format(profile, max_id)
  else:
    url = 'https://www.instagram.com/{}/'.format(profile)
  response = urllib2.urlopen(url)
  html = response.read()
  search_obj = re.search('sharedData = (.*);', html)
  json_obj = json.loads(search_obj.group(1))
  media_files = json_obj['entry_data']['ProfilePage'][0]['user']['media']['nodes']
  logging.info('Analizing media...')
  for file in media_files:
    media_id = file['id']
    if media_id not in images and media_id not in videos:
      media_src = file['display_src']
      media_type = 'videos' if file['is_video'] else 'images'
      if media_type == 'images':
        images_metadata.write('{}\n'.format(media_id))
        logging.info('New image found: {}'.format(media_id))
      elif media_type == 'videos':
        videos_metadata.write('{}\n'.format(media_id))
        logging.info('New video found: {}'.format(media_id))
      media_request = urllib2.Request(media_src)
      media_data = urllib2.urlopen(media_request).read()
      media_file = open('insta_crawler/{}/{}/{}.png'.format(profile_name, media_type, media_id), 'w')
      media_file.write(media_data)
      media_file.close()


logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--profile', help='Instagram profile name', required=True)
args = parser.parse_args()

profile_name = args.profile

images_dir = 'insta_crawler/{}/images/'.format(profile_name)
if not os.path.exists(images_dir):
  os.makedirs(images_dir)
videos_dir = 'insta_crawler/{}/videos/'.format(profile_name)
if not os.path.exists(videos_dir):
  os.makedirs(videos_dir)

images_metadata = open('insta_crawler/{}/.images'.format(profile_name), 'a+')
images_metadata.seek(0)
images = images_metadata.read().splitlines()
videos_metadata = open('insta_crawler/{}/.videos'.format(profile_name), 'a+')
videos_metadata.seek(0)
videos = videos_metadata.read().splitlines()

logging.info('Crawling latest profile information...')
max_id = None
urls = get_urls_npages(profile_name, 2)
for url in urls:
  logging.info('Fetching images from url %s'%url)
  download_from_profile(profile_name, max_id)
  
#response = urllib2.urlopen('https://www.instagram.com/{}/'.format(profile_name))
#html = response.read()
#search_obj = re.search('sharedData = (.*);', html)
#json_obj = json.loads(search_obj.group(1))
#media_files = json_obj['entry_data']['ProfilePage'][0]['user']['media']['nodes']
#logging.info('Analizing media...')
#for file in media_files:
#  media_id = file['id']
#  if media_id not in images and media_id not in videos:
#    media_src = file['display_src']
#    media_type = 'videos' if file['is_video'] else 'images'
#    if media_type == 'images':
#      images_metadata.write('{}\n'.format(media_id))
#      logging.info('New image found: {}'.format(media_id))
#    elif media_type == 'videos':
#      videos_metadata.write('{}\n'.format(media_id))
#      logging.info('New video found: {}'.format(media_id))
#    media_request = urllib2.Request(media_src)
#    media_data = urllib2.urlopen(media_request).read()
#    media_file = open('insta_crawler/{}/{}/{}.png'.format(profile_name, media_type, media_id), 'w')
#    media_file.write(media_data)
#    media_file.close()

images_metadata.close()
videos_metadata.close()
logging.info('Process finished')

