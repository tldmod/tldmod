# -*- coding: utf-8 -*-

'''
 All-in-one SHA-1-izer for ReactOS Applications Manager DB Packages 2000 Ex Pro Gold redux v1337
 *a shiny masterpiece of modern technology*  *requires python 3*  *please kill me*
 --
 Copyright (c) 2015 Created by Ismael Ferreras Morezuelas (swyterzone+tld@gmail.com)
 
 use as: cd <lang-folder> && python ../_list_used_glyphs.py > output.txt

 Released under the liberal 2-clause BSD license.
 <http://opensource.org/licenses/BSD-2-Clause>
'''
import sys
import glob
import codecs

db = ""

for file in sorted(glob.glob('*.csv')):
    print(file)

    with codecs.open(file, 'r', 'UTF-8') as f:
        for line in f:
			thing = line.replace('^','').replace('{','').replace('}','').rstrip()
			if thing:
				string=thing.split("|")[1]
				db = db + string # append all the combined strings in the translation
			# print(string)

db = "".join(set(db)) # remove duplicates
db = ''.join(sorted(db)) # sort them
print("==========\r\nDB of used glyphs (" + str(len(db)) + "): " + db.encode('utf-8'))