import string
from header_common import *
from module_info import *
from process_common import *

if (wb_compile_switch == 0):
  from process_animations_mb import *
  
elif (wb_compile_switch == 1):
  from process_animations_wb import *

