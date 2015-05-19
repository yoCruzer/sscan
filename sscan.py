#!/usr/bin/env python
# coding:utf-8#

"""
sscan - Scan Security Tools
@author Feei <wufeifei[at]wufeifei.com>
"""

import time
import re
import urllib
import urllib2


class sscan:
    startTime = time.time()
    rules = [
        '/config/config_global.php.bak',
        '/config/config_ucenter.php.bak',
        '/.svn/entries',
        '/.git/config',
        '/WEB-INF/web.xml',
        '/.config.inc.php.swp',
        '/.index.php.swp',
        '/data.tar',
        '/www.tar',
        '/www.tar.gz',
        '/phpmyadmin/',
        '/upload/',
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': 1,
        'Referer': 'http://www.baidu.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    def search(self):
        url = 'https://www.baidu.com/s?'
        query = {
            'wd': '测试'
        }
        url = url + urllib.urlencode(query)
        req = urllib2.Request(url, None, self.headers)
        r = urllib2.urlopen(req)
        body = r.read()
        print re.findall('([\w-]+\.[\w-]+(.com|.cn|.org|.net|.edu|.gov){1})', body)

    def dict(self):
        with open("top-cn.csv", "r") as ins:
            i = 0
            for line in ins:
                i = i + 1
                print i
                # print line
                url = line.split(',')
                url = 'http://www.' + url[1].strip()
                self.scan(url)

    def scan(self, url):
        urls = []
        if url[len(url) - 1] == '/':
            url = url[:len(url) - 1]
        print 'TEST:' + url
        for rule in self.rules:
            self.get(url + rule)
        print 'TotalTime: %s' % ((time.time() - self.startTime) / 10)

    def get(self, url):
        f = open('/tmp/.tmp', 'w')
        try:
            req = urllib2.Request(url, None, self.headers)
            result = urllib2.urlopen(req, timeout=3)
        except urllib2.HTTPError as e:
            f.write(str(e.code) + '[ORIGIN]' + url + '\n')
        except urllib2.URLError as e:
            print e.reason
        except socket.error as e:
            print e
        except Exception as e:
            print e
        else:
            # Body is have 404
            body = result.read()
            if '404' in body or '找不到' in body or '不存在' in body:
                f.write(str(404) + '[CUSTOM]' + url + '\n')
            else:
                f.write(str(result.getcode()) + url + '\n')
                print str(result.getcode()) + url
        f.close()


sscan = sscan()
sscan.dict()
# sscan.scan('http://www.xnwgj.gov.cn/bbs/')
# sscan.search()
