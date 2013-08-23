from module_info import *
from module_simple_triggers import *

from process_common import *
from process_operations import *

def save_simple_triggers(variable_list,variable_uses,triggers,tag_uses,quick_strings):
  file = open(export_dir + "simple_triggers.txt","w")
  file.write("simple_triggers_file version 1\n")
  file.write("%d\n"%len(simple_triggers))
  for i in xrange(len(simple_triggers)):
    simple_trigger = simple_triggers[i]
    file.write("%f "%(simple_trigger[0]))
    save_statement_block(file,0, 1, simple_trigger[1]  , variable_list,variable_uses,tag_uses,quick_strings)
    file.write("\n")
  file.close()


print "exporting simple triggers..."
variable_uses = []
variables = load_variables(export_dir,variable_uses)
tag_uses = load_tag_uses(export_dir)
quick_strings = load_quick_strings(export_dir)
save_simple_triggers(variables,variable_uses,simple_triggers,tag_uses,quick_strings)
save_variables(export_dir,variables,variable_uses)
save_tag_uses(export_dir,tag_uses)
save_quick_strings(export_dir,quick_strings)
#print "finished."
