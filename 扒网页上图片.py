# -*- encoding:utf-8 -*-

import urllib2
from lxml import etree

def main():
    request = urllib2.Request("http://www.sohu.com/a/61291010_103936")
    response = urllib2.urlopen(request)
    html = response.read()

    page = etree.HTML(html)
    count = 0
    for url in page.xpath(u"//img/@src"):
        if url.startswith("http:"):
            print url

            try:
                img_request = urllib2.Request(url)
                img_response = urllib2.urlopen(img_request)
                img = img_response.read()
            except:
                continue

            count += 1
            filename = str(count)+".jpg"
            pic_out = file(filename, 'w')
            pic_out.write(img)
            pic_out.close()

if __name__ == '__main__':
    main()