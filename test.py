import unittest2
import mock
from insta_crawler import _get_phantomjs_path_for_platform, get_rendered_javascript, get_image_urls

sample_rendered_html = """
<div>
    <div class="_nljxa">
        <div class="_myci9">
            <a class="_8mlbc _vbtk2 _t5r8b" href="/p/BKoJpWnA9wN/">
                <div class="_22yr2">
                    <div class="_jjzlb"><img alt="I'm so tiny haha (Tanx @hvioletart!)" class="_icyx7" id="pImage_0" src="https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14334461_1735674300019917_185651481788022784_n.jpg?ig_cache_key=MTM0NDM2NjkxMjk2NDEyMzY2MQ%3D%3D.2" style="">
                    </div>
                    <!-- react-empty: 45 -->
                    <div class="_ovg3g"></div>
                </div>
            </a>
            <a class="_8mlbc _vbtk2 _t5r8b" href="/p/BKlJrYggayt/">
                <div class="_22yr2">
                    <div class="_jjzlb"><img alt="I'm at a mansion haha wow. Tanx @airbnb for putting me up!" class="_icyx7" id="pImage_1" src="https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14334700_843501332451925_1343924359_n.jpg?ig_cache_key=MTM0MzUyMjYyNzUxMTIzMzcwOQ%3D%3D.2" style="">
                    </div>
                    <!-- react-empty: 53 -->
                    <div class="_ovg3g"></div>
                </div>
            </a>
            <a class="_8mlbc _vbtk2 _t5r8b" href="/p/BKjsNxJADKO/">
                <div class="_22yr2">
                    <div class="_jjzlb"><img alt="Hmmm otay I'll take a look at the dessert menu" class="_icyx7" id="pImage_2" src="https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14272080_1601097096850651_228267775_n.jpg?ig_cache_key=MTM0MzExMTU3NDA1MDU4MzE4Mg%3D%3D.2" style="">
                    </div>
                    <!-- react-empty: 61 -->
                    <div class="_ovg3g"></div>
                </div>
            </a>
        </div>
        <div class="_myci9">
            <a class="_8mlbc _vbtk2 _t5r8b" href="/p/BKgbqKfA_fh/">
                <div class="_22yr2">
                    <div class="_jjzlb"><img alt="Found out they serve brunch l8" class="_icyx7" id="pImage_3" src="https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/e15/14334744_173479766391861_1537082147_n.jpg?ig_cache_key=MTM0MjE5NDMzMzY4ODAwMjUyOQ%3D%3D.2" style="">
                    </div>
                    <!-- react-empty: 70 -->
                    <div class="_ovg3g"></div>
                </div>
                <div class="_1lp5e">
                    <div class="_cxj4a"><span class=" _1kaa3 _soakw coreSpriteVideoIconMobile">Video</span>
                    </div>
                </div>
            </a>
            <a class="_8mlbc _vbtk2 _t5r8b" href="/p/BKMow2MATE4/">
                <div class="_22yr2">
                    <div class="_jjzlb"><img alt="Don't cross the orange line it's the law" class="_icyx7" id="pImage_4" src="https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/e15/14309781_1600992890194394_2124763659_n.jpg?ig_cache_key=MTMzNjYyMjQ2ODAwMDk4NTQwMA%3D%3D.2" style="">
                    </div>
                    <!-- react-empty: 81 -->
                    <div class="_ovg3g"></div>
                </div>
                <div class="_1lp5e">
                    <div class="_cxj4a"><span class=" _1kaa3 _soakw coreSpriteVideoIconMobile">Video</span>
                    </div>
                </div>
            </a>
            <a class="_8mlbc _vbtk2 _t5r8b" href="/p/BKD78mXA0bM/">
                <div class="_22yr2">
                    <div class="_jjzlb"><img alt="B kewl stay in skewl" class="_icyx7" id="pImage_5" src="https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14099904_1274764009213932_664849750_n.jpg?ig_cache_key=MTMzNDE3MzU2MzczMjgzODA5Mg%3D%3D.2" style="">
                    </div>
                    <!-- react-empty: 92 -->
                    <div class="_ovg3g"></div>
                </div>
            </a>
        </div>
        <div class="_myci9">
            <a class="_8mlbc _vbtk2 _t5r8b" href="/p/BKBNUq4AEHA/">
                <div class="_22yr2">
                    <div class="_jjzlb"><img alt="I got sox" class="_icyx7" id="pImage_6" src="https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c78.0.924.924/14272122_1779743115635833_1962253108_n.jpg?ig_cache_key=MTMzMzQwNTU1OTcwOTI1NDA4MA%3D%3D.2.c" style="">
                    </div>
                    <!-- react-empty: 101 -->
                    <div class="_ovg3g"></div>
                </div>
            </a>
            <a class="_8mlbc _vbtk2 _t5r8b" href="/p/BJ5wi_8AbHZ/">
                <div class="_22yr2">
                    <div class="_jjzlb"><img alt="Good marnieing" class="_icyx7" id="pImage_7" src="https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14063424_1431845810165853_1801723452_n.jpg?ig_cache_key=MTMzMTMwODY3NjIxMTkxMzE3Nw%3D%3D.2" style="">
                    </div>
                    <!-- react-empty: 109 -->
                    <div class="_ovg3g"></div>
                </div>
            </a>
            <a class="_8mlbc _vbtk2 _t5r8b" href="/p/BJqjxkyANiU/">
                <div class="_22yr2">
                    <div class="_jjzlb"><img alt="Don't steal my sunshine remember that song haha" class="_icyx7" id="pImage_8" src="https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/13703163_757914917645546_1898072282_n.jpg?ig_cache_key=MTMyNzAzMDM3ODU4OTkwMjk5Ng%3D%3D.2" style="">
                    </div>
                    <!-- react-empty: 117 -->
                    <div class="_ovg3g"></div>
                </div>
            </a>
        </div>
        <div class="_myci9">
            <a class="_8mlbc _vbtk2 _t5r8b" href="/p/BJlE72VgLwn/">
                <div class="_22yr2">
                    <div class="_jjzlb"><img alt="Here's me w/ dogs 4 #nationaldogday (I'm a dog too)" class="_icyx7" id="pImage_9" src="https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14063348_753369908099097_509136331_n.jpg?ig_cache_key=MTMyNTQ4NzM3MDMwODQ2Nzc1MQ%3D%3D.2" style="">
                    </div>
                    <!-- react-empty: 126 -->
                    <div class="_ovg3g"></div>
                </div>
            </a>
            <a class="_8mlbc _vbtk2 _t5r8b" href="/p/BJafEetgc-p/">
                <div class="_22yr2">
                    <div class="_jjzlb"><img alt="Me in a art (@franfranmaster)" class="_icyx7" id="pImage_10" src="https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14072845_838267372939669_541092323_n.jpg?ig_cache_key=MTMyMjUwNjA4Nzg4MjE0OTgwMQ%3D%3D.2" style="">
                    </div>
                    <!-- react-empty: 134 -->
                    <div class="_ovg3g"></div>
                </div>
            </a>
        </div>
    </div>
    <div class="_ikcuh">
        <div class="_4tedc">
            <iframe aria-hidden="true" class="_823eg" tabindex="-1"></iframe>
        </div>
    </div>
    <div class=" _stvbq"><a class=" _1ooyk" href="/p/undefined/?max_id=1304636815571002918">Load more</a>
    </div>
</div>
""".strip()

sample_img_urls = [
    u'https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14334461_1735674300019917_185651481788022784_n.jpg?ig_cache_key=MTM0NDM2NjkxMjk2NDEyMzY2MQ%3D%3D.2',
    u'https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14334700_843501332451925_1343924359_n.jpg?ig_cache_key=MTM0MzUyMjYyNzUxMTIzMzcwOQ%3D%3D.2',
    u'https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14272080_1601097096850651_228267775_n.jpg?ig_cache_key=MTM0MzExMTU3NDA1MDU4MzE4Mg%3D%3D.2',
    u'https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/e15/14334744_173479766391861_1537082147_n.jpg?ig_cache_key=MTM0MjE5NDMzMzY4ODAwMjUyOQ%3D%3D.2',
    u'https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/e15/14309781_1600992890194394_2124763659_n.jpg?ig_cache_key=MTMzNjYyMjQ2ODAwMDk4NTQwMA%3D%3D.2',
    u'https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14099904_1274764009213932_664849750_n.jpg?ig_cache_key=MTMzNDE3MzU2MzczMjgzODA5Mg%3D%3D.2',
    u'https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c78.0.924.924/14272122_1779743115635833_1962253108_n.jpg?ig_cache_key=MTMzMzQwNTU1OTcwOTI1NDA4MA%3D%3D.2.c',
    u'https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14063424_1431845810165853_1801723452_n.jpg?ig_cache_key=MTMzMTMwODY3NjIxMTkxMzE3Nw%3D%3D.2',
    u'https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/13703163_757914917645546_1898072282_n.jpg?ig_cache_key=MTMyNzAzMDM3ODU4OTkwMjk5Ng%3D%3D.2',
    u'https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14063348_753369908099097_509136331_n.jpg?ig_cache_key=MTMyNTQ4NzM3MDMwODQ2Nzc1MQ%3D%3D.2',
    u'https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/14072845_838267372939669_541092323_n.jpg?ig_cache_key=MTMyMjUwNjA4Nzg4MjE0OTgwMQ%3D%3D.2'
]

class MockBrowser(object):
    def get(self, url):
        self.page_source = 'some html source'

class TestRenderedJavascriptMethods(unittest2.TestCase):
    @mock.patch('insta_crawler.platform')
    def test_get_phantomjs_path_for_platform(self, mock_platform):
        mock_platform.system.return_value = 'Windows'
        self.assertEqual(_get_phantomjs_path_for_platform(), './phantomjs.exe')

    def test_get_rendered_javascript(self):
        self.assertEqual(get_rendered_javascript('fakeurl', MockBrowser()), 'some html source')

    def test_get_image_urls(self):
        self.maxDiff = None
        self.assertEqual(get_image_urls(sample_rendered_html), sample_img_urls)

