# coding: utf8
'''
test_crawl_exception_handling.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''
import os
import shutil

from nose.plugins.attrib import attr

from plugins.tests.helper import PluginTest, PluginConfig


@attr('smoke')
class TestCrawlExceptions(PluginTest):

    target_url = 'http://moth/w3af/crawl/web_spider/follow_links/'

    _run_configs = {
        'cfg': {
            'target': target_url + '1.html',
            'plugins': {
                'crawl': (
                    PluginConfig('failing_spider',
                                 ('only_forward', True, PluginConfig.BOOL)),
                )
            }
        },
    }

    def setUp(self):
        '''
        This is a rather complex setUp since I need to move the failing_spider.py
        plugin to the plugin directory in order to be able to run it afterwards.

        In the tearDown method, I'll remove the file.
        '''
        self.src = os.path.join(
            'plugins', 'tests', 'crawl', 'failing_spider.py')
        self.dst = os.path.join('plugins', 'crawl', 'failing_spider.py')
        shutil.copy(self.src, self.dst)

        super(TestCrawlExceptions, self).setUp()

    def tearDown(self):
        if os.path.exists(self.dst):
            os.remove(self.dst)

        if os.path.exists(self.dst + 'c'):  # pyc file
            os.remove(self.dst + 'c')

        # This is a very special case in which I don't want the assertion in
        # the original tearDown() to trigger on me!
        self.w3afcore.exception_handler.clear()

        super(TestCrawlExceptions, self).tearDown()

    def test_spider_found_urls(self):
        cfg = self._run_configs['cfg']
        self._scan(cfg['target'], cfg['plugins'])

        # I tried to make some more advanced unittests here, but it was
        # very difficult to get a result that was NOT random from failing_spider
        # + exception_handler .
        #
        # Simply test that the scan was able to finish without a crash generated by
        # the failing_spider.py plugin.
        self.assertTrue(True)
