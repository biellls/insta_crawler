Insta Crawler
=============

This python script crawls the landing page of an Instagram public profile and analyze the last 12 media items, downloading new images and videos.

With two separate metadata dictionaries, the script tracks the images and videos downloaded to the local filesystem. If new images or videos appear in the landing page of the profile, the script downloads them and update the metadata dictionaries.

When new media files are found it can send notifications by mail. To do so, a mailing configuration should be set up in the insta_crawler.cfg file.

Usage:
```
python insta_crawler.py --profile sdiazb
```
