#!/usr/bin/env python3
# coding=utf-8

import hashlib
import json
import os

if __name__ == '__main__':
	hashes = {}

	def hashFile(filename):
		global hashes

		with open(filename, 'rb') as file:
			hashes[filename] = hashlib.sha1(file.read()).hexdigest()

	def hashDir(directory):
		for entry in os.scandir(directory):
			if (entry.is_file()):
				hashFile(directory + '/' + entry.name)
			else:
				hashDir(directory + '/' + entry.name)

	hashFile('last-updated.json')
	hashDir('database')
	hashDir('images')

	with open('sha1sum.json', 'w') as file:
		json.dump(hashes, file, sort_keys=True, indent='\t')
