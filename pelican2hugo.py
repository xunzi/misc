#!/usr/bin/env python3
# converts blog post front matter
# from pelican to hugo format
#pelican headers
#Title: von Linux zu MacOS
#Date: 2010-09-14 14:09
#Tags: helferlein,macos,linux
#Slug: von-linux-zu-macos

#hugo headers
#---
#title: "Sysadmin Toolbox"
#date: 2020-11-14
#draft: true
#tags: [ 'sysadmin', 'tools of the trade' ]
#slug: "sysadmin-toolbox"
#---



import jinja2
import re
import sys
import argparse

header_pattern = r'^(.+):\s(.+)$'

tpl_hugo = """---\ntitle: "{{ title }}"
date: {{ date  }}
tags: {{ tags }}
slug: {{ slug }}
---
{{ payload }}
"""

def handle_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--infile", help="Input file")
	parser.add_argument("-o", "--overwrite", help="Overwrite input file", 
		action="store_true", default=False)
	_args = parser.parse_args()
	return _args
	
def mangle_headers(header_line):
	[ header_name, header_value ] = header_line.split(':', maxsplit=1)
	header_name = header_name.strip()
	header_value = header_value.strip()
	if header_name.lower() == 'date':
		header_value = header_value.split()[0]
	elif header_name.lower() == 'tags':
		header_value = header_value.lower().split(',')
	return { header_name.lower(): header_value } 

if __name__ == "__main__":
	content_dict = {}
	args = handle_args()
	with open(args.infile) as infh:
		content = infh.read()
	if content.startswith("---"):
		print("Already in Hugo format")
		sys.exit(1)
	[ headers, text ] = content.split("\n\n", maxsplit=1)
	for header in headers.splitlines():
		content_dict.update(mangle_headers(header))
	content_dict.update(payload = text)
	out_text = jinja2.Template(tpl_hugo).render(content_dict)
	if args.overwrite:
		with open(args.infile, 'w') as outfh:
			outfh.write(out_text)
	else:
		print(out_text)
