
# Point export_dir to the folder you will be keeping your module
# Make sure you use forward slashes (/) and NOT backward slashes (\)
from header_common import *
from os import system

wb_compile_switch = 0

if (wb_compile_switch == 0):
  export_dir = "../"
  system("title building tld for 1011--")
elif (wb_compile_switch == 1):
  export_dir = "../_wb/"
  system("title building tld for wb--")