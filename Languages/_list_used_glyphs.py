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
db_aval = ""

with open("../../Data/font_data.xml") as f:
 for line in f:
  if line.startswith("<character"):
    split = line.split()
    db_aval = db_aval + chr(int( split[1].split("=")[1].strip('"') ))

db_aval = "".join(set(db_aval)) # remove duplicates
db_aval = ''.join(sorted(db_aval)) # sort them

print("Available glyphs in the font (%u): %s" % (len(db_aval), "".join(db_aval)))


for file in sorted(glob.glob('*.csv')):
    print(file)

    with codecs.open(file, 'r', 'UTF-8') as f:
        for line in f:
            thing = line.replace('^','').replace('{','').replace('}','').rstrip()
            if thing:
                string=thing.split("|")[1]
                db = db + string # append all the combined strings in the translation
                #print(string)

db = "".join(set(db)) # remove duplicates
db = ''.join(sorted(db)) # sort them
print("==========\r\nDB of used glyphs (" + "%u" % len(db) + "): " + db)

#print((list(set(db) - set(db_aval))))
#exit()

db_intersection = "".join(list(set(db) - set(db_aval)))
db_intersection = ''.join(sorted(db_intersection)) # sort them

print("==========\r\nDB of missing glyphs that won't be displayed by the font (" + "%u" % len(db_intersection) + "): " + db_intersection)
