#import string
#import types

from module_info import *
from module_triggers import *
from module_dialogs import *
from module_simple_triggers import *
from module_presentations import *

from process_common import *
from process_operations import *



#-------------------------------------------------------

def compile_all_global_vars(variable_list,variable_uses, triggers, sentences, game_menus, mission_templates, scripts, simple_triggers):
  temp_list = []
  list_type = type(temp_list)
  for trigger in triggers:
    try:
      compile_global_vars(trigger[3], variable_list,variable_uses),
      compile_global_vars(trigger[4], variable_list,variable_uses),
    except:
      print "Error in trigger:"
      print trigger
      
  for sentence in sentences:
    try:
      compile_global_vars(sentence[2], variable_list,variable_uses),
      compile_global_vars(sentence[5], variable_list,variable_uses),
    except:
      print "Error in dialog line:"
      print sentence

  for game_menu in game_menus:
    try:
      compile_global_vars(game_menu[4], variable_list,variable_uses)
      menu_items = game_menu[5]
      for menu_item in menu_items:
        compile_global_vars(menu_item[1], variable_list,variable_uses)
        compile_global_vars(menu_item[3], variable_list,variable_uses)
    except:
      print "Error in game menu:"
      print game_menu

  for mission_template in mission_templates:
    try:
      mt_triggers = mission_template[5]
      for mt_trigger in mt_triggers:
        compile_global_vars(mt_trigger[3], variable_list,variable_uses)
        compile_global_vars(mt_trigger[4], variable_list,variable_uses)
    except:
      print "Error in mission template:"
      print mission_template

  for presentation in presentations:
    try:
      prsnt_triggers = presentation[3]
      for prsnt_trigger in prsnt_triggers:
        compile_global_vars(prsnt_trigger[1], variable_list,variable_uses)
    except:
      print "Error in presentation:"
      print presentation

  for i_script in xrange(len(scripts)):
    try:
      func = scripts[i_script]
      if (type(func[1]) == list_type):
        compile_global_vars(func[1], variable_list,variable_uses)
      else:
        compile_global_vars(func[2], variable_list,variable_uses)
    except:
      print "Error in script:"
      print func

  for simple_trigger in simple_triggers:
    try:
      compile_global_vars(simple_trigger[1]  , variable_list,variable_uses)
    except:
      print "Error in simple trigger:"
      print simple_trigger


print "Compiling all global variables..."
variables = []
variable_uses = []

#MORDACHAI - Preserve previous global variable order, for save-game compatibility...
try:
  file = open("variables.txt","r")
  var_list = file.readlines()
  file.close()
  for v in var_list:
    vv = string.strip(v)
    if vv:
      variables.append(vv)
      variable_uses.append(0)
except:
  print "Variables.txt not found. No attempt to maintain save game compatibility will be made for this build."

compile_all_global_vars(variables, variable_uses, triggers, dialogs, game_menus, mission_templates, scripts, simple_triggers)
save_variables(export_dir, variables, variable_uses)

#MORDACHAI - write out the new version of variables.txt to our module system folder, so we can maintain compatibility with it...
file = open("variables.txt","w")
for i in xrange(len(variables)):
  file.write("%s\n"%variables[i])
file.close()
