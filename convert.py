#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from struct import unpack
from shutil import rmtree
from zipfile import ZipFile
from tempfile import gettempdir
from datetime import datetime, timedelta
from os import removedirs, mkdir, listdir
from os.path import join, abspath, isfile, isdir, splitext


def unzip_jtv(file_name):

	# Faggoten function to decode file names for MAC and WIN zip-files
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
			# print file_path
			with open(file_path, 'w') as f:
				f.write(z.read(name))
	return extract_path


def process_jtv_directory(jtv_path):

	def list_ndx(path):
		for f in listdir(path):
			if isfile(join(jtv_path, f)) and splitext(f)[1].lower() == '.ndx':
				yield f

	def from_timestamp(timestamp):
		return datetime(1601, 1, 1) + timedelta(seconds = int(timestamp / 10000000))

	print 'Processing "%s"' % jtv_path
	for ndx in list_ndx(jtv_path):
		pdt = splitext(ndx)[0] + '.pdt'
		print u'============================================================================'
		print splitext(pdt)[0]
		print u'----------------------------------------------------------------------------'
		with open(join(jtv_path, pdt), 'r') as pdt_file:
			hdr = pdt_file.read(26)
			entries = dict()
			if hdr != 'JTV 3.x TV Program Data\x0a\x0a\x0a':
				print pdt, 'does not contain valid header!'
				continue
			key = 26
			while True:
				str_len = pdt_file.read(2)
				if str_len == '':
					break
				l = unpack('H', str_len)[0]
				track = pdt_file.read(l).decode('cp1251').encode('utf-8')
				if track == '':
					break
				entries[key] = track
				key += l + 2
			# JTV 3.x TV Program Data
			with open(join(jtv_path, ndx), 'r') as ndx_file:
				num_entries = unpack('H', ndx_file.read(2))[0]
				for i in range(0, num_entries):
					ndx_file.read(2)
					time = from_timestamp(unpack('Q', ndx_file.read(8))[0])
					offset = unpack('H', ndx_file.read(2))[0]
					print time, entries[offset]

	# for f in list_ndx(jtv_path):
		# print f


if __name__ == '__main__':
	for p in [ abspath(p) for p in argv[1:] ]:
		if isfile(p) and splitext(p)[1].lower() == '.zip':
			process_jtv_directory(unzip_jtv(p))
		elif isdir(p):
			process_jtv_directory(p)
		else:
			print 'Expected zip archive or directory!'
