from module_info import *

if (wb_compile_switch == 0):
  from header_operations_mb1011 import *
elif (wb_compile_switch == 1):
  from header_operations_wb import *