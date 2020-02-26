#!/usr/bin/python3
# parse_web_dir.py
# simple program to extract desired URLs from index.html of release directory
#
# parameters:
# 1: html document of release directory 
# 2: prefix - find sub-URLs that start with this name
# 3: match_string_csv - comma-separated list of match strings you want
#
# for example:
#  wget https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/pre-release/latest/
# ./parse_web_dir.py /var/tmp/index.html \
#    rhcos installer-kernel,installer-initramfs,metal
#

import os, sys
from bs4 import BeautifulSoup

html_doc = sys.argv[1]
prefix = sys.argv[2]
match_string_csv = sys.argv[3]

# read the HTML
with open(html_doc) as f:
    soup = BeautifulSoup(f, 'html.parser')
#print(soup.prettify())

# find the files in this directory that you want
match_strings = match_string_csv.split(',')
for link in soup.find_all('a'):
  l = link.get('href')
  if l.startswith(prefix):
    for m in match_strings:
        if l.__contains__(m):
            print(l)
            break
