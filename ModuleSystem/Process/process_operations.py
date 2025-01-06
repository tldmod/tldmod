# -*- coding: utf-8 -*-
import string
import types

from process_common import *
from header_common import *
from header_operations import *

from module_strings import *
from module_skills import *
from module_music import *
from module_meshes import *
from module_sounds import *
from module_items import *
from module_troops import *
from module_factions import *
from module_quests import *
from module_party_templates import *
from module_parties import *
from module_scenes import *
from module_scripts import *
from module_mission_templates import *
from module_game_menus import *
from module_particle_systems import *
from module_scene_props import *
from module_scene_props import *
from module_presentations import *
from module_map_icons import *
from module_tableau_materials import *

from module_info import *
if (not wb_compile_switch):
  from module_animations import *
else:
  from module_animations_wb import *

def get_id_value(tag, identifier, tag_uses):
  tag_type = -1
  id_no = -1
  if (tag == "str"):
    id_no = find_object(strings,identifier)
    tag_type = tag_string
  elif (tag == "itm"):
    id_no = find_object(items,identifier)
    tag_type = tag_item
  elif (tag == "trp"):
    id_no = find_object(troops,identifier)
    tag_type = tag_troop
  elif (tag == "fac"):
    id_no = find_object(factions,identifier)
    tag_type = tag_faction
  elif (tag == "qst"):
    id_no = find_object(quests,identifier)
    tag_type = tag_quest
  elif (tag == "pt"):
    id_no = find_object(party_templates,identifier)
    tag_type = tag_party_tpl
  elif (tag == "p"):
    id_no = find_object(parties,identifier)
    tag_type = tag_party
  elif (tag == "scn"):
    id_no = find_object(scenes,identifier)
    tag_type = tag_scene
  elif (tag == "mt"):
    id_no = find_object(mission_templates,identifier)
    tag_type = tag_mission_tpl
  elif (tag == "mnu"):
    id_no = find_object(game_menus,identifier)
    tag_type = tag_menu
  elif (tag == "script"):
    id_no = find_object(scripts,identifier)
    tag_type = tag_script
  elif (tag == "psys"):
    id_no = find_object(particle_systems,identifier)
    tag_type = tag_particle_sys
  elif (tag == "spr"):
    id_no = find_object(scene_props,identifier)
    tag_type = tag_scene_prop
  elif (tag == "prsnt"):
    id_no = find_object(presentations,identifier)
    tag_type = tag_presentation
  elif (tag == "snd"):
    id_no = find_object(sounds,identifier)
    tag_type = tag_sound
  elif (tag == "icon"):
    id_no = find_object(map_icons,identifier)
    tag_type = tag_map_icon
  elif (tag == "skl"):
    id_no = find_object(skills,identifier)
    tag_type = tag_skill
  elif (tag == "track"):
    id_no = find_object(tracks,identifier)
    tag_type = tag_track
  elif (tag == "mesh"):
    id_no = find_object(meshes,identifier)
    tag_type = tag_mesh
  elif (tag == "anim"):
    id_no = find_object(animations,identifier)
    tag_type = tag_animation
  elif (tag == "tableau"):
    id_no = find_object(tableaus,identifier)
    tag_type = tag_tableau

  if (tag_type > -1 and id_no > -1):
    add_tag_use(tag_uses,tag_type,id_no)
  return (tag_type, id_no)
  
def get_identifier_value(str, tag_uses):
  underscore_pos = str.find("_")
  result = -1
  if (underscore_pos > 0):
    tag_str = str[0:underscore_pos]
    id_str  = str[underscore_pos + 1:len(str)]
    (tag_type, id_no) = get_id_value(tag_str,id_str,tag_uses)
    if (tag_type > 0):
      if (id_no < 0):
        print("Error: Unable to find object:" + str)
      else:
        #@swy-antireveng#
        #> The game only needs type tags for registers, local variables, global variables, strings, quick strings
        #result = id_no | (tag_type << op_num_value_bits)
        if(tag_type==tag_register or tag_type==tag_local_variable or tag_type==tag_variable or tag_type==tag_string or tag_type==tag_quick_string):
          result = id_no | (tag_type << op_num_value_bits)
        else:
          result = id_no
    else:
      print("Error: Unrecognized tag:" +tag_str + "in object:" + str)
  else:
    print("Error: Invalid object:" +str + ".Variables should start with $ sign and references should start with a tag")
  return result

def load_quick_strings(export_dir):
  quick_strings = []
  try:
    file = open(export_dir + "quick_strings.txt", "r", encoding='utf-8')
    str_list = file.readlines()
    file.close()
    for s in str_list:
      s = s.strip()
      if s:
        ssplit = s.split(' ')
        if len(ssplit) == 2:
          quick_strings.append(ssplit)
  except FileNotFoundError:
    print("Creating new quick_strings.txt file...")
  return quick_strings

def save_quick_strings(export_dir, quick_strings):
  file = open(export_dir + "quick_strings.txt", "w", encoding='utf-8')
  file.write("%d\n"%len(quick_strings))
  for i in range(len(quick_strings)):
    file.write("%s %s\n"%(remove_exclamation_marker_on_mb1011(quick_strings[i][0]),remove_exclamation_marker_on_mb1011(replace_spaces(quick_strings[i][1]))))
  file.close()

def load_variables(export_dir,variable_uses):
  variables = []
  try:
    file = open(export_dir + "variables.txt","r", encoding='utf-8')
    var_list = file.readlines()
    file.close()
    for v in var_list:
      vv = v.strip()
      if vv:
        variables.append(vv)
  except FileNotFoundError:
    print("variables.txt not found. Creating new variables.txt file")

  try:
    file = open(export_dir + "variable_uses.txt","r", encoding='utf-8')
    var_list = file.readlines()
    file.close()
    for v in  var_list:
      vv = v.strip()
      if vv:
        variable_uses.append(int(vv))
  except FileNotFoundError:
    print("variable_uses.txt not found. Creating new variable_uses.txt file")

  return variables

def save_variables(export_dir,variables_list,variable_uses,):
  file = open(export_dir + "variables.txt","w", encoding='utf-8')
  for i in range(len(variables_list)):
    file.write("%s\n"%variables_list[i])
  file.close()
  file = open(export_dir + "variable_uses.txt","w", encoding='utf-8')
  for i in range(len(variables_list)):
    file.write("%d\n"%variable_uses[i])
  file.close()

def ensure_tag_use(tag_uses, tag_no, object_no):
  if len(tag_uses[tag_no]) <= object_no:
    num_to_add = object_no + 1 - len(tag_uses[tag_no])
    for j in range(num_to_add):
      tag_uses[tag_no].append(0)

def add_tag_use(tag_uses, tag_no, object_no):
  #TODO: Uncomment to make build_module_check_tags work
#  ensure_tag_use(tag_uses, tag_no, object_no)
#  tag_uses[tag_no][object_no] = tag_uses[tag_no][object_no] + 1
  pass
    
def load_tag_uses(export_dir):
  tag_uses = []
  for i in range(tags_end):
    sub_tag_uses = []
    tag_uses.append(sub_tag_uses)
    
  try:
    file = open(export_dir + "tag_uses.txt","r", encoding='utf-8')
    var_list = file.readlines()
    file.close()
    for v in  var_list:
      vv = v.strip(v).split(';')
      if vv:
        for v2 in vv:
          vvv = v2.split(' ')
          if len(vvv) >= 3:
            ensure_tag_use(tag_uses,int(vvv[0]),int(vvv[1]))
            tag_uses[int(vvv[0])][int(vvv[1])] = int(vvv[2])
  except FileNotFoundError:
    print("Creating new tag_uses.txt file...")
  return tag_uses

def save_tag_uses(export_dir,tag_uses):
  file = open(export_dir + "tag_uses.txt","w", encoding='utf-8')
  for i in range(len(tag_uses)):
    for j in range(len(tag_uses[i])):
      file.write("%d %d %d;" % (i, j, tag_uses[i][j]))
    file.write("\n")
  file.close()

def add_cookie(cookies_list,cookie_string):
  found = 0
  result = -1
  for i_t in range(len(cookies_list)):
    if cookie_string == cookies_list[i_t]:
      found = 1
      result = i_t
      break
  if not found:
    cookies_list.append(cookie_string)
    result = len(cookies_list) - 1
  return result

def get_cookie(cookies_list,cookie_string):
  found = 0
  result = -1
  for i_t in range(len(cookies_list)):
    if cookie_string == cookies_list[i_t]:
      found = 1
      result = i_t
      break
  if not found:
    print("ERROR: input token not found:" + cookie_string)
    cookies_list.append(cookie_string)
    result = len(cookies_list) - 1
  return result


def check_varible_not_defined(variable_string,variables_list):
  for i_t in range(len(variables_list)):
    if variable_string == variables_list[i_t]:
      print("WARNING: Variable name used for both local and global contexts:" + variable_string)
      break

#def add_get_variable(variable_string,variables_list):
#  found = 0
#  result = -1
#  for i_t in range(len(variables_list)):
#    if variable_string == variables_list[i_t]:
#      found = 1
#      result = i_t
#      break
#  if not found:
#    variables_list.append(variable_string)
#    result = len(variables_list) - 1
#  return result
    
def add_variable(variable_string,variables_list,variable_uses):
  found = 0
  for i_t in range(len(variables_list)):
    if variable_string == variables_list[i_t]:
      found = 1
      variable_uses[i_t] = variable_uses[i_t] - 1
      break
  if not found:
    variables_list.append(variable_string)
    variable_uses.append(-1)

def get_variable(variable_string,variables_list,variable_uses, calling_script):
  found = 0
  result = -1
  var_string = variable_string[1:]
  for i_t in range(len(variables_list)):
    if var_string == variables_list[i_t]:
      found = 1
      result = i_t
      variable_uses[result] = variable_uses[result] + 1
      break
  if not found:
    if (variable_string[0] == '$'):
      variables_list.append(variable_string)
      variable_uses.append(0)
      result = len(variables_list) - 1
      print("WARNING: Usage of unassigned global variable: " + variable_string + " in script '" + calling_script + "'")
    else:
      print("ERROR: Usage of unassigned local variable: " + variable_string + " in script '" + calling_script + "'")
  return result

def is_lhs_operation(op_code):
  found = 0
  if op_code in lhs_operations:
      return 1
  return 0

def is_lhs_operation_for_global_vars(op_code):
  found = 0
  if op_code in lhs_operations:
      return 1
  if op_code in global_lhs_operations:
      return 1
  return 0

def is_can_fail_operation(op_code):
  found = 0
  if op_code in can_fail_operations:
      return 1
  return 0

def search_quick_string_keys(key, quick_strings):
  index = -1
  for i in range(len(quick_strings)):
    if quick_strings[i][0] == key:
      index = i
  return index

def insert_quick_string_with_auto_id(sentence,quick_strings):
  index = 0
  text = convert_to_identifier_with_no_lowercase(sentence)
  
  #swy-- strip non ANSI codepoints to avoid encoding problems. e.g: Lórien -> Lrien
  #   -- qstr_A_golden_mist_from_L0xC3 -> qstr_A_golden_mist_from_Lr
  text = str(text.encode("ascii", "ignore").decode("utf-8", "ignore"))

  sentence = replace_spaces(sentence)
  done = 0
  i = 20
  lt = len(text)
  if (i > lt):
    i  = lt
  auto_id = "qstr_" + text[0:i]
  done = 0
  index = search_quick_string_keys(auto_id, quick_strings)
  if index >= 0 and (quick_strings[index][1] == sentence):
    done = 1
  while (i <= lt) and not done:
    auto_id = "qstr_" + text[0:i]
    index = search_quick_string_keys(auto_id, quick_strings)
    if index >= 0:
      if quick_strings[index][1] == sentence:
        done = 1
      else:
        i += 1
    else:      
      done = 1
      index = len(quick_strings)
      quick_strings.append([auto_id, sentence])
  if not done:
    number = 1
    new_auto_id = auto_id + str(number)
    while new_auto_id in quick_strings:
      number += 1
      new_auto_id = auto_id + str(number)
    auto_id = new_auto_id
    index = len(quick_strings)
    quick_strings.append([auto_id, sentence])
  return index


def process_param(param,global_vars_list,global_var_uses, local_vars_list, local_var_uses, tag_uses, quick_strings, calling_script):
  result = 0
  if (type(param) == str):
    if (param[0] == '$'):
      check_varible_not_defined(param[1:], local_vars_list)
      result = get_variable(param, global_vars_list,global_var_uses, calling_script)
      result |= opmask_variable
    elif (param[0] == ':'):
      check_varible_not_defined(param[1:], global_vars_list)
      result = get_variable(param, local_vars_list,local_var_uses, calling_script)
      result |= opmask_local_variable
    elif (param[0] == '@'):
      result = insert_quick_string_with_auto_id(param[1:], quick_strings)
      result |= opmask_quick_string
    else:
      result = get_identifier_value(param.lower(), tag_uses)
      if (result < 0):
        print("ERROR: Illegal Identifier:" + param)
  else:
    result = param
  return result

def save_statement(ofile,opcode,no_variables,statement,variable_list,variable_uses,local_vars_list,local_var_uses,tag_uses,quick_strings, calling_script):
  if no_variables == 0:
    lenstatement = len(statement) - 1
    if (is_lhs_operation(opcode) == 1):
      if (lenstatement > 0):
        param = statement[1]
        if (type(param) == str):
          if (param[0] == ':'):
            add_variable(param[1:], local_vars_list, local_var_uses)
  else:
    lenstatement = 0
  ofile.write("%d %d "%(opcode, lenstatement))
  for i in range(lenstatement):
    operand = process_param(statement[i + 1],variable_list,variable_uses,local_vars_list,local_var_uses,tag_uses,quick_strings, calling_script)
    ofile.write("%d "%operand)

def compile_global_vars_in_statement(statement,variable_list, variable_uses):
  opcode = 0
  if not hasattr(statement, '__len__'):
    opcode = statement
  else:
    opcode = statement[0]
    if (is_lhs_operation_for_global_vars(opcode) == 1):
      if (len(statement) > 1):
        param = statement[1]
        if (type(param) == str):
          if (statement[1][0] == '$'):
            add_variable(statement[1][1:], variable_list, variable_uses)

def save_statement_block(ofile,statement_name,can_fail_statement,statement_block,variable_list, variable_uses,tag_uses,quick_strings, calling_script):
  local_vars = []
  local_var_uses = []
  ofile.write(" %d "%(len(statement_block)))
  store_script_param_1_uses = 0
  store_script_param_2_uses = 0
  current_depth = 0
  can_fail = 0
  for i in range(len(statement_block)):
    statement = statement_block[i]
    if not hasattr(statement, '__len__'):
      opcode = statement
      no_variables = 1
    else:
      opcode = statement[0]
      no_variables = 0
    if (opcode in [try_begin,
                   try_for_range,
                   try_for_range_backwards,
                   try_for_parties,
                   try_for_agents,
                   try_for_prop_instances]):
      current_depth = current_depth + 1
    elif (opcode == try_end):
      current_depth = current_depth - 1
    elif (opcode == store_script_param_1 or (opcode == store_script_param and statement[2] == 1)):
      store_script_param_1_uses = store_script_param_1_uses + 1
    elif (opcode == store_script_param_2 or (opcode == store_script_param and statement[2] == 2)):
      store_script_param_2_uses = store_script_param_2_uses + 1
    elif (can_fail_statement == 0 and current_depth == 0
          and (is_can_fail_operation(opcode)
               or ((opcode == call_script) and (statement[1].startswith("cf_", 7))))
          and (not statement_name.startswith("cf_"))
          
          #swy-- we don't care about these ones, a bad practice, i know!
          and (statement_name!="rout_check" and statement_name!="coherence")):
      
      print("WARNING: Script can fail at operation #" + str(i) + ". Use cf_ at the beginning of its name: " + statement_name)

    # swy: enhancement to track down buggy chained condition blocks, suggested by @Aro
    next_opcode = 0
    if (i + 1) < len(statement_block): # swy: don't try to grab a next opcode when we're the last operation in the block
      next_opcode = hasattr(statement_block[i + 1], '__len__') and statement_block[i + 1][0] or \
                                                                   statement_block[i + 1] # swy: if an operation tuple doesn't have parameters and hence no comma separators they are just integers and not actual tuples, handle both types gracefully
    if (opcode & this_or_next) and (next_opcode & (0xFFFF)) not in can_fail_operations:   # swy: if our operation has this_or_next and the following operation isn't eq/ge/... or any other check (e.g. that we're the actual last condition in the chain)
      print("WARNING: swy: this_or_next in the last chained condition, probably a mistake: " + str(statement_name)) + " / " + str(calling_script) + " " + str(i)
    # --

    save_statement(ofile,opcode,no_variables,statement,variable_list,variable_uses,local_vars, local_var_uses,tag_uses,quick_strings, calling_script)

  if (store_script_param_1_uses > 1):
    print("WARNING: store_script_param_1 is used more than once:" + statement_name)
  if (store_script_param_2_uses > 1):
    print("WARNING: store_script_param_2 is used more than once:" + statement_name)
  i = 0
  while (i < len(local_vars)):
    if (local_var_uses[i] == 0 and not(local_vars[i].startswith("unused"))):
      print("WARNING: Local variable never used: " + local_vars[i]+ ", at: " + str(statement_name) + " in script '" + calling_script + "'")
    i = i + 1
  if (len(local_vars) > 128):
   print("WARNING: Script uses more than 128 local wariables: " + str(statement_name) + "variables count:" + str(len(local_vars)))
  
  # Indentation Enhancement By Vorne
  # http://forums.taleworlds.com/index.php/topic,189368.0.html
  
  if current_depth != 0:
    if current_depth > 0:
      missing = " missing"
    else:
      missing = " extra"
      current_depth *= -1
    
    if statement_name == 0:
      statement_name = calling_script
      
    print("WARNING: " + current_depth + missing + " try_end: " + str(statement_name))
  
  #>

def compile_global_vars(statement_block,variable_list, variable_uses):
  for statement in statement_block:
    compile_global_vars_in_statement(statement, variable_list, variable_uses)


def save_simple_triggers(ofile,triggers,variable_list, variable_uses,tag_uses,quick_strings):
  ofile.write("%d\n"%len(triggers))
  trigger_id = 0
  for trigger in triggers:
    ofile.write("%s "%(sf(trigger[0])))
    save_statement_block(ofile,0,1,trigger[1]  , variable_list, variable_uses,tag_uses,quick_strings, "trigger " + str(trigger_id))
    ofile.write("\n")
    trigger_id += 1
  ofile.write("\n")
  
