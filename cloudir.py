#!/usr/bin/env python

from cloudapp.cloud import Cloud

import os
import tempfile

CLOUD_USER = 'user@gmail.com'
CLOUD_PASS = 'password123'

DIR = 'test-files'
EXTS = ['markdown', 'md', 'txt']
TITLE = 'cloudir test'


def fill_template(title, file_index):
	template = ''.join(file('template.html').readlines())
	template = template.replace('$$$title$$$', title)
	template = template.replace('<!--', file_index + '\n\n<!--')	
	return template

def make_dir_entry(title, url):
	return """<div class="file">
	<img alt="" class="icon" src="http://vu0.org/files/file.png"/>
	<p><a href="%s">%s</a></p>
</div>
""" % (url, title)

def upload_files_from_directory(mycloud, directory):
	file_index = ''
	for f in os.listdir(directory):
		if os.path.splitext(f)[1][1:] in EXTS:
			path = os.path.join(directory, f)
			uploaded = mycloud.upload_file(path)
			file_index += make_dir_entry(f, uploaded['url'])
	return file_index

def upload_string_as_file(mycloud, string, suffix):
	index = tempfile.NamedTemporaryFile(suffix=suffix, dir='.')
	index.write(string)
	index.flush()
	uploaded = mycloud.upload_file(index.name)
	index.close()
	return uploaded['remote_url']

if __name__ == '__main__':
	mycloud = Cloud()
	mycloud.auth(CLOUD_USER, CLOUD_PASS)

	file_index = upload_files_from_directory(mycloud, DIR)
	template = fill_template(TITLE, file_index)
	print upload_string_as_file(mycloud, template, '.html')
