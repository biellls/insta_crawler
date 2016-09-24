import argparse
import platform
import time
import os
import urllib2
import re
import json
import logging
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from ConfigParser import ConfigParser
from bs4 import BeautifulSoup


LOAD_TIMEOUT_SECONDS = 15
MAX_RETRIES = 5
SCROLL_WAIT = 2


def _get_phantomjs_path_for_platform():
  if platform.system() == 'Windows':
    return './phantomjs.exe'
  else:
    return './phantomjs'


def get_phantomjs_browser():
  PHANTOMJS_PATH = _get_phantomjs_path_for_platform()
  return webdriver.PhantomJS(PHANTOMJS_PATH)


def get_rendered_javascript(url, browser=None):
  browser = browser or get_phantomjs_browser()
  browser.get(url)
  return browser.page_source


def get_max_id(html):
  search_obj = re.search('max_id=([0-9]+)">', html)
  return json.loads(search_obj.group(1))
  return None if search_obj is None else json.loads(search_obj.group(1))


def build_instagram_url(profile, max_id=None):
  if max_id is not None:
    url = 'https://www.instagram.com/{}/?max_id={}'.format(profile, max_id)
  else:
    url = 'https://www.instagram.com/{}/'.format(profile)
  return url


def get_id(url):
  """
  >>> get_id('https://someurl.com/foo/bar/myimg.jpg?ig_cache_key=mycachekey')
  'mycachekey'
  """
  return url.split('cache_key=')[-1]


def get_image_name(url):
  """
  >>> get_image_name('https://someurl.com/foo/bar/myimg.jpg?ig_cache_key=mycachekey')
  'myimg.jpg'
  """
  return url.split('cache_key=')[-2].split('/')[-1].split('?')[0]


def get_image_urls(html):
  soup = BeautifulSoup(html, "html.parser")
  imgs = soup.find_all("img", {"id": re.compile("pImage_[\d]+")})
  return [img['src'] for img in imgs]


def download_images(html):
  imgurls = get_image_urls(html)
  total_downloaded = 0
  nimages = len(imgurls)
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
    total_downloaded += 1
    logging.info("Downloaded {} out of {} images".format(total_downloaded, nimages))
  return len(imgurls)

def image_total(profile):
  response = urllib2.urlopen(build_instagram_url(profile))
  html = response.read()
  search_obj = re.search('sharedData = (.*);', html)
  json_obj = json.loads(search_obj.group(1))
  return json_obj['entry_data']['ProfilePage'][0]['user']['media']['count']


def _load_more(browser):
  WebDriverWait(browser, LOAD_TIMEOUT_SECONDS).until(
    EC.presence_of_element_located((By.LINK_TEXT, "Load more"))
  )
  browser.find_element_by_link_text("Load more").click()


def _num_loaded_images(browser):
  return len(get_image_urls(browser.page_source))


def _scroll_to_bottom(browser):
  browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def load_full_page(profile, browser=None):
  """ Returns rendered HTML for the full page
  Actions performed to get full HTML:
  - Render initial page
  - Click on "Load more" button"
  - Scroll to bottom to load more images
  - Stop when we have all the images
  """
  total_images = image_total(profile)
  browser = browser or get_phantomjs_browser()
  browser.get(build_instagram_url(profile))
  _load_more(browser)
  loaded_images = _num_loaded_images(browser)
  retries = 0
  while loaded_images < total_images:
    _scroll_to_bottom(browser)
    time.sleep(SCROLL_WAIT)
    logging.info("Scrolled to bottom. Loaded {} out of {} images".format(_num_loaded_images(browser), total_images))
    previous_loaded_images = loaded_images
    loaded_images = _num_loaded_images(browser)
    if previous_loaded_images == loaded_images and loaded_images != total_images:
      retries += 1
      if retries == MAX_RETRIES:
        logging.info("Cannot load full page")
        raise Exception("Cannot load full page")
  return browser.page_source


def historical_extraction(profile):
  full_page = load_full_page(profile)
  download_images(full_page)


def latest_extraction(profile):
  logging.info('Crawling latest profile information...')
  response = urllib2.urlopen(build_instagram_url(profile))
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
        notification_msg = 'New image found in profie {}: {}'.format(profile_name, media_id)
      elif media_type == 'videos':
        videos_metadata.write('{}\n'.format(media_id))
        notification_msg = 'New video found in profile {}: {}'.format(profile_name, media_id)
      logging.info(notification_msg)
      media_request = urllib2.Request(media_src)
      media_data = urllib2.urlopen(media_request).read()
      media_path = 'insta_crawler/{}/{}/{}.png'.format(profile_name, media_type, media_id)
      media_file = open(media_path, 'w')
      media_file.write(media_data)
      media_file.close()
      send_notification_by_mail(subject='{} has added new items to Instagram'.format(profile_name),
                                message=notification_msg,
                                image=media_path)


def send_notification_by_mail(subject, message, image):
  try:
    parser = ConfigParser()
    parser.read('insta_crawler.cfg')
    smtp_host = parser.get('smtp', 'smtp_host')
    smtp_port = parser.getint('smtp', 'smtp_port')
    smtp_starttls = parser.getboolean('smtp', 'smtp_starttls')
    smtp_ssl = parser.getboolean('smtp', 'smtp_ssl')
    smtp_user = parser.get('smtp', 'smtp_user')
    smtp_password = parser.get('smtp', 'smtp_password')
    recipients = [recipient.strip() for recipient in parser.get('smtp', 'smtp_recipients').split(',')]

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.preamble = message
    fp = open(image, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    srv = smtplib.SMTP_SSL(smtp_host, smtp_port) if smtp_ssl else smtplib.SMTP(smtp_host, smtp_port)
    if smtp_starttls:
      srv.starttls()
    srv.login(smtp_user, smtp_password)
    srv.sendmail(smtp_user, recipients, msg.as_string())
    srv.quit()
  except:
    logging.error('Notification could not be send')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--profile', help='Instagram profile name', required=True)
  parser.add_argument('--historical', help='Perform historical extraction of n pages (12 images per page))', action='store_true')
  parser.add_argument('--clear-metadata', dest="clear_metadata", help='Clears all metadata files', action='store_true')
  args = parser.parse_args()

  profile_name = args.profile

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

  if args.historical:
    historical_extraction(profile_name)
  else:
    latest_extraction(profile_name)

  images_metadata.close()
  videos_metadata.close()
  logging.info('Process finished')

