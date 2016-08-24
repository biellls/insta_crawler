import argparse
import os
import urllib2
import re
import json
import logging
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from ConfigParser import ConfigParser

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

images_metadata.close()
videos_metadata.close()
logging.info('Process finished')
