from module_info import *

if (wb_compile_switch == 0):
  from header_mission_templates_mb import *
elif (wb_compile_switch == 1):
  from header_mission_templates_wb import *