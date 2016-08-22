Insta Crawler
=============

This python script crawls the landing page of an Instagram public profile and analyze the last 12 media items, downloading new images and videos.

With two separate metadata dictionaries, it tracks the images and videos downloaded to the local filesystem. If new images or videos appear in the landing page of the profile, the script downloads them and update the metadata dictionaries. **Note:** Currently the metadata ids for historical and latest extractions are different, so the files will be downloaded twice.

Requirements:
Download phantomJS from the following website: https://bitbucket.org/ariya/phantomjs/downloads and copy the phantomjs executable to the same directory as insta_crawler. This is necessary for the historical extraction.
This can be done by executing the configure script (currently only for Linux and OS X):
```
./configure
```

The following pip packages are necessary for the historical extraction:
```
pip install selenium
pip install bs4
```

Usage:
```
# Latest extraction
python insta_crawler.py --profile sdiazb
# Historical extraction (3 pages or 3*12 pictures in this example)
python insta_crawler.py --profile sdiazb --historical 3
# Clear metadata
python insta_crawler.py --profile sdiazb --clear-metadata
```
