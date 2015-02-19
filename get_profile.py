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
import os, sys, commands, time, types

#ref. http://ymotongpoo.hatenablog.com/entry/20081211/1228985067
class OriconHTMLParser(HTMLParser):
    def __init__(self, profileid, flag):
        HTMLParser.__init__(self)
        self.flag = flag
        if flag:
            self.snapFlag = False
        else:
            self.profFlag = False
            self.thFlag = False
            self.tdFlag = False
            self.dataDict = {}
        self.profileid = profileid
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        flag  = self.flag
        if flag:
            if 'div' == tag and 'class' in attrs:
                if "photo-main" == attrs['class']:
                    self.snapFlag = True
        else:
            if 'table' == tag and 'class' in attrs:
                if "tbl-profile" == attrs['class']:
                    self.profFlag = True

        if flag:
            if self.snapFlag:
                if 'img' == tag:
                    downloadImage([self.profileid, attrs['alt'], attrs['src'].split('/')[-2]])
        else:
            if self.profFlag:
                if 'span' == tag:
                    self.thFlag = True
                if 'td' == tag:
                    self.tdFlag = True

    def handle_endtag(self, tag):
        if self.flag:
            if self.snapFlag:
                if 'div' == tag:
                    self.snapFlag = False
        else:
            if self.profFlag:
                if 'table' == tag:
                    downloadProfile([self.profileid, self.dataDict])
                    self.profFlag = False

    def handle_data(self, data):
        if not self.flag:
            if self.thFlag:
                self.th = data
                self.thFlag = False
            if self.tdFlag:
                self.dataDict[self.th] = data
                self.tdFlag = False

def downloadImage(data):
    path = "girls_image/" + str(data[0]) + '/'
    os.system('mkdir ' + path)
    baseurl = 'http://life-cdn.oricon.co.jp/girls/img/photo/'
    url_1 = baseurl + data[2] + '/b_0'
    url_2 = baseurl + data[2] + '/' + data[2] + '_b_0'
    url = [url_1, url_2]
    for i in range(1, 10):
        if len(data[0]) == 2:
            url = url[::-1]
        flag = commands.getoutput('wget ' + url[0] + str(i) + '.jpg' + ' -P ' + path + ';echo $?')
        if flag != 0:
            os.system('wget ' + url[1] + str(i) + '.jpg' + ' -P ' + path)
        time.sleep(1.0)
    return path

def downloadProfile(data):
    path = "girls_image/" + str(data[0]) + '/'
    with open(path + 'profile.tsv', 'w') as f:
        for k, v in data[1].items():
            f.write('\t'.join([k, v]) + '\n')

def parser(url, profileid, flag):
    data = urllib2.urlopen(url)

    parser = OriconHTMLParser(profileid, flag)
    parser.feed(data.read())

    parser.close()
    data.close()

def main():
    f = open(sys.argv[1])

    for line in f:
        profileid = line.rstrip()
        url = 'http://www.oricon.co.jp/special/girls/' + profileid + '/'
        parser(url, profileid, True)
        url = url + 'profile/'
        parser(url, profileid, False)
        
        time.sleep(5.0)

if __name__=='__main__':
    main()
