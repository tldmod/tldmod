from module_info import wb_compile_switch as is_wb

if   (is_wb == 0):
  from header_triggers_mb import *
elif (is_wb == 1):
  from header_triggers_wb import *