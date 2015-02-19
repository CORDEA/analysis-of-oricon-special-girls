#!/usr/bin/env python
# encoding:utf-8
#
# Copyright [2015] [Yoshihiro Tanaka]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__Author__ =  "Yoshihiro Tanaka"
__date__   =  "2015-02-17"


from HTMLParser import HTMLParser, HTMLParseError
import urllib2
import sys

#ref. http://ymotongpoo.hatenablog.com/entry/20081211/1228985067
class OriconHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.snapFlag = False
        self.perFlag = False
        self.dataList = []
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'ul' == tag and 'class' in attrs:
            if "list-snap clearfix" == attrs['class']:
                self.snapFlag = True

        if self.snapFlag:
            data = ''
            if 'a' == tag:
                data = [attrs['href']]
            if 'img' == tag:
                data = [attrs['src'], attrs['alt']]
            if 'em' == tag:
                self.perFlag = True
            if len(data) > 0:
                self.dataList += data

    def handle_endtag(self, tag):
        if self.snapFlag:
            if 'ul' == tag:
                self.snapFlag = False
        if self.perFlag:
            if 'em' == tag:
                print '\t'.join(self.dataList)
                self.dataList = []
                self.perFlag = False

    def handle_data(self, data):
        if self.perFlag:
            self.dataList.append(data)

url = 'http://www.oricon.co.jp/special/girls/rank/'
if sys.argv[1] != 1:
    url += 'p/' + str(sys.argv[1]) + '/'

data = urllib2.urlopen(url)

parser = OriconHTMLParser()
parser.feed(data.read())

parser.close()
data.close()
