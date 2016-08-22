import argparse
import platform
from selenium import webdriver
import os
import urllib2
import re
import json
import logging
from bs4 import BeautifulSoup


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


def build_instagram_url(profile, max_id=None):
  if max_id is not None:
    url = 'https://www.instagram.com/{}/?max_id={}'.format(profile, max_id)
  else:
    url = 'https://www.instagram.com/{}/'.format(profile)
  return url


def get_id(url):
  return url.split('cache_key=')[-1]


def get_image_name(url):
  return url.split('cache_key=')[-2].split('/')[-1].split('?')[0]


def get_image_urls(html):
  soup = BeautifulSoup(html, "html.parser")
  imgs = [soup.find("img", {"id": "pImage_0"})['src']]
  for i in range(1, 12):
    imgs.append(soup.find("img", {"id": "pImage_{}".format(i)})['src'])
  return imgs


def download_images(html):
  imgurls = get_image_urls(html)
  for imgurl in imgurls:
    media_id = get_id(imgurl)
    if media_id not in images:
      logging.info('New image found: {}'.format(media_id))
      images_metadata.write('{}\n'.format(media_id))
      media_request = urllib2.Request(imgurl)
      media_data = urllib2.urlopen(media_request).read()
      imgname = get_image_name(imgurl)
      media_file = open('insta_crawler/{}/historical/{}.png'.format(profile_name, imgname), 'w')
      media_file.write(media_data)
      media_file.close()


def historical_extraction(profile, npages):
  browser = get_phantomjs_browser()
  url = build_instagram_url(profile)
  html = get_rendered_javascript(url, browser)
  download_images(html)
  while npages > 1:
    max_id = get_max_id(html)
    url = build_instagram_url(profile, max_id)
    html = get_rendered_javascript(url, browser)
    download_images(html)
    npages -= 1


def latest_extraction(profile):
  logging.info('Crawling latest profile information...')
  response = urllib2.urlopen('https://www.instagram.com/{}/'.format(profile))
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
parser.add_argument('--historical', help='Perform historical extraction of n pages (12 images per page))')
parser.add_argument('--clear-metadata', dest="clear_metadata", help='Clears all metadata files', action='store_true')
args = parser.parse_args()

profile_name = args.profile
npages = args.historical

images_dir = 'insta_crawler/{}/images/'.format(profile_name)
if not os.path.exists(images_dir):
  os.makedirs(images_dir)
videos_dir = 'insta_crawler/{}/videos/'.format(profile_name)
if not os.path.exists(videos_dir):
  os.makedirs(videos_dir)
historical_dir = 'insta_crawler/{}/historical/'.format(profile_name)
if not os.path.exists(historical_dir):
  os.makedirs(historical_dir)

images_metadata_path = 'insta_crawler/{}/.images'.format(profile_name)
videos_metadata_path = 'insta_crawler/{}/.videos'.format(profile_name)
if args.clear_metadata:
  if os.path.isfile(images_metadata_path):
    os.remove(images_metadata_path)
  if os.path.isfile(videos_metadata_path):
    os.remove(videos_metadata_path)
  logging.info('Cleared metadata')
  exit()

images_metadata = open(images_metadata_path, 'a+')
images_metadata.seek(0)
images = images_metadata.read().splitlines()
videos_metadata = open(videos_metadata_path, 'a+')
videos_metadata.seek(0)
videos = videos_metadata.read().splitlines()

if args.historical is not None:
  historical_extraction(profile_name, int(npages))
else:
  latest_extraction(profile_name)

images_metadata.close()
videos_metadata.close()
logging.info('Process finished')

