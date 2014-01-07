import string
from header_common import *
from module_info import *
from process_common import *

if (wb_compile_switch):
  from process_animations_wb import *
else:
  from process_animations_mb import *

