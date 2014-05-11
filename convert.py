#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from shutil import rmtree
from zipfile import ZipFile
from tempfile import gettempdir
from os import removedirs, mkdir
from os.path import join, abspath, isfile, isdir, splitext


def unzip_jtv(file_name):

	# Function decode file names for MAC and WIN zip-files
	def decode_name(name):
		try:
			return name.decode('utf-8').encode('utf-8')
		except:
			return name.decode('cp866').encode('utf-8')

	# Make temp directory
	extract_path = join(gettempdir(), 'jtv_to_xmltv')
	try:
		rmtree(extract_path)
	except OSError as e:
		print e
	mkdir(extract_path)
	# Extract EPG
	with ZipFile(file_name) as z:
		for name in z.namelist():
			file_path = join(extract_path, decode_name(name))
			print file_path
			with open(file_path, 'w') as f:
				f.write(z.read(name))
	return extract_path


def process_jtv_directory(jtv_path):
	print 'Processing "%s"' % jtv_path


if __name__ == '__main__':
	for p in [ abspath(p) for p in argv[1:] ]:
		if isfile(p) and splitext(p)[1].lower() == '.zip':
			process_jtv_directory(unzip_jtv(p))
		elif isdir(p):
			process_jtv_directory(p)
		else:
			print 'Expected zip archive or directory!'
