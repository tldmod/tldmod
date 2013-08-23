from module_info import *
import os

print "Initializing..."

try:
  os.remove(export_dir + 'tag_uses.txt')
except:
  a = []
try:
  os.remove(export_dir + 'quick_strings.txt')
except:
  a = []
