import argparse
import os
import urllib2
import re
import json
import logging

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
response = urllib2.urlopen('https://www.instagram.com/{}/'.format(profile_name))
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

images_metadata.close()
videos_metadata.close()
logging.info('Process finished')
