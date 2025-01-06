import string

from module_scripts import *

from process_common import *
from process_operations import *

from module_info import wb_compile_switch as is_wb

def save_scripts(variable_list,variable_uses,scripts,tag_uses,quick_strings):
  file = open(export_dir + "scripts.txt","w")
  file.write("scriptsfile version 1\n")
  file.write("%d\n"%len(scripts))
  temp_list = []
  list_type = type(temp_list)
  s_num = 0
  for i_script in range(len(scripts)):
    func = scripts[i_script]
    script_name = convert_to_identifier(func[0])
    #MV: removed script name obfuscation.. made impossible helping players
    # if cheat_switch == 0:  
      # if (not(script_name.startswith("game_"))):
        # s_num = s_num + 1
        # script_name = "s" + str(s_num) 
    if (type(func[1]) == list_type):
      #file.write("%s -1\n"%(convert_to_identifier(func[0])))
      file.write("%s -1\n"%script_name)
      save_statement_block(file,convert_to_identifier(func[0]), 0,func[1], variable_list,variable_uses,tag_uses,quick_strings, convert_to_identifier(func[0]) )
    else:
      #file.write("%s %f\n"%(convert_to_identifier(func[0]), func[1]))
      file.write("%s %s\n"%(script_name, sf(func[1])))
      save_statement_block(file,convert_to_identifier(func[0]), 0,func[2], variable_list,variable_uses,tag_uses,quick_strings, convert_to_identifier(func[0]) )
    file.write("\n")
  file.close()

def save_python_header():
  if (is_wb):
    file = open("./ID/ID_scripts_wb.py","w", encoding='utf-8')
  else:
    file = open("./ID/ID_scripts_mb.py","w", encoding='utf-8')
  for i_script in range(len(scripts)):
    file.write("script_%s = %d\n"%(convert_to_identifier(scripts[i_script][0]),i_script))
  file.write("\n\n")
  file.close()


print("Exporting scripts...")
save_python_header()
variable_uses = []
variables = load_variables(export_dir, variable_uses)
tag_uses = load_tag_uses(export_dir)
quick_strings = load_quick_strings(export_dir)
save_scripts(variables,variable_uses,scripts,tag_uses,quick_strings)
save_variables(export_dir,variables,variable_uses)
save_tag_uses(export_dir, tag_uses)
save_quick_strings(export_dir,quick_strings)
