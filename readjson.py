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

import json, sys, os, time

def main():
    bef = []
    beftime = 0.0
    while True:
        filepath = '/home/compbio/.mozilla/firefox/2rx2yf69.default/sessionstore-backups/recovery.js'
        mtime = os.stat(filepath).st_mtime
        if mtime != beftime:
            f = open(filepath)
            data = json.load(f)
            readdata = data['windows'][0]['cookies'][0]['value']
            items = readdata.split('%7C')

            if bef != items:
                writeFile(items[3:5])
                writeFile(items[10:12])
                bef = items
                print "write to file."
        beftime = mtime
        time.sleep(1.0)

def writeFile(items):
    with open('girls.tsv', 'a') as fw:
        fw.write('\t'.join(items) + '\n')

if __name__=='__main__':
    os.system('touch girls.tsv')
    main()
