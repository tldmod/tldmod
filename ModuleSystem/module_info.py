
# Point export_dir to the folder you will be keeping your module
# Make sure you use forward slashes (/) and NOT backward slashes (\)
from header_common import *

wb_compile_switch = 0

if (wb_compile_switch == 0):
  export_dir = "../"
elif (wb_compile_switch == 1):
  export_dir = "../_wb/"
