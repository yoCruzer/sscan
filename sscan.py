#!/usr/bin/env python
# coding:utf-8#

"""
SSCAN - Scan Security Tools
@author Feei <wufeifei[at]wufeifei.com>
"""

import time
import re
import urllib
import urllib2


class sscan:
    startTime = time.time()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': 1,
        'Referer': 'http://www.baidu.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    rules = [
        # Info
        '/.svn/entries',
        '/.git/config',
        '/WEB-INF/web.xml',
        '/config.inc.php.bak',
        '/.config.inc.php.swp',
        '/.index.php.swp',
        '/phpinfo.php',
        '/config/config_ucenter.php.bak',
        '/config/config_global.php.bak',
        '/config/.config_ucenter.php.swp',
        '/config/.config_global.php.swp',
        '/readme',
        '/readme.md',
        '/readme.txt',
        # Back File
        '/data.tar',
        '/data.rar',
        '/data.zip',
        '/www.tar.gz',
        '/www.tar',
        '/www.rar',
        '/www.zip',
        '/www.tar.gz',
        '/web.rar',
        '/web.tar',
        '/web.tar.gz',
        # Component
        '/uc_server/',
        '/phpmyadmin/',
        '/upload/',
        '/cacti/index.php',
        # Test
        '/upload.html',
        '/test.html',
        '/ceshi/',
        # Mange Dashboard
        '/admin/',
        '/invoker/JMXInvokerServlet',
        '/admin-console/',
        '/jmx-console/',
    ]
    success = []

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
                i += 1
                print i
                # print line
                url = line.split(',')
                url = 'http://www.' + url[1].strip()
                self.scan(url)

    def scan(self, url):
        if url[len(url) - 1] == '/':
            url = url[:len(url) - 1]
        print 'TEST:' + url
        for rule in self.rules:
            self.get(url + rule)
        print self.success
        print 'TotalTime: %s' % ((time.time() - self.startTime) / 10)

    def get(self, url):
        f = open('/tmp/.tmp', 'w')
        try:
            class NoRedirectHandler(urllib2.HTTPRedirectHandler):
                def http_error_302(self, req, fp, code, msg, headers):
                    infourl = urllib.addinfourl(fp, headers, req.get_full_url())
                    infourl.status = code
                    infourl.code = code
                    return infourl

                http_error_300 = http_error_302
                http_error_301 = http_error_302
                http_error_303 = http_error_302
                http_error_307 = http_error_302

            opener = urllib2.build_opener(NoRedirectHandler())
            urllib2.install_opener(opener)
            req = urllib2.Request(url, None, self.headers)
            result = urllib2.urlopen(req, timeout=3)
        except urllib2.HTTPError as e:
            msg = str(e.code) + '[ORIGIN]'
        except urllib2.URLError as e:
            msg = e.reason
        except Exception as e:
            msg = e
        else:
            # Handle 404
            body = result.read()
            not_found = ['404', '找不到', '不存在', '抱歉', '再试', '不合法', '被阻断', '访问禁止', 'not allowed']
            is_not_found = 0
            for nf in not_found:
                if nf in body:
                    is_not_found = 1
                    break
            if is_not_found == 1:
                msg = '404[CUSTOM]'
            elif result.code in (300, 301, 302, 303, 307):
                msg = str(result.code) + '[CUSTOM]'
            else:
                self.success.append(url)
                msg = str(result.getcode()) + '[SUCCESS]'
        url = url.replace('http://', '')
        msg += url
        print msg
        f.write(msg + '\n')
        f.close()

sscan = sscan()
# sscan.dict()
sscan.scan('http://f.mogujie.com/')
# sscan.search()
