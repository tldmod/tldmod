
# Point export_dir to the folder you will be keeping your module
# Make sure you use forward slashes (/) and NOT backward slashes (\)
from header_common import *
from os import system, environ

# Set it to True/False depending if you want to build
# for Warband/1.011, respectively. Easy as pie.
wb_compile_switch = False


# By default it will be built either on the parent folder or a _wb sibling.
if (not wb_compile_switch and not "BUILD_TLD_WB" in environ):
  export_dir = "../"; wb_compile_switch = 0
  system("title building tld for 1011--")
else:
  export_dir = "../_wb/"; wb_compile_switch = 1
  system("title building tld for wb--")