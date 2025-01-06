import string

from process_operations import *
from process_common import *
from module_items import *
from header_items import *

from module_info import wb_compile_switch as is_a_wb_item

#swy-- always compile this file in M&B 1.011 mode; no matter what (!)
wb_compile_switch = 0

def get_item_code(item):
  prefix = "it_"
  code = prefix + item[0]
  return code

def save_python_header():
  from module_info import wb_compile_switch as is_wb
  if (is_wb):
    file = open("./ID/ID_items_wb.py","w", encoding='utf-8')
  else:
    file = open("./ID/ID_items_mb.py","w", encoding='utf-8')
  for i_item in range(len(items)):
    file.write("itm_%s = %d\n"%(convert_to_identifier(items[i_item][0]),i_item))
  file.close()

def write_items(variable_list,variable_uses,tag_uses,quick_strings):
  itemkinds_file_name = export_dir + "item_kinds1.txt"
  ofile = open(itemkinds_file_name,"w", encoding='utf-8')
  ofile.write("itemsfile version 2\n")
  ofile.write("%d\n"%len(items))
  for index,item in enumerate(items):
    if (item[3] & itp_shop) > 0:
      id_no = find_object(items,convert_to_identifier(item[0]))
      add_tag_use(tag_uses,tag_item,id_no)
    ofile.write(" itm_%s %s %s %d "%(convert_to_identifier(item[0]),remove_exclamation_marker_on_mb1011(replace_spaces(item[1])),remove_exclamation_marker_on_mb1011(replace_spaces(item[1])),len(item[2])))
    item_variations = item[2]
    for item_variation in item_variations:
      #swy-- different dummy mesh for warband, for invisible objects, fixes galadriel's appearance, meshes have to have more than two characters to work.
      item_variation = list(item_variation)
      # if (is_a_wb_item and item_variation[0]=="0") or (index<=(len(items)/2)):
      # if (is_a_wb_item and item_variation[0]=="0") or (index>=(len(items)/2)):
      if (is_a_wb_item and item_variation[0]=="0"):
        item_variation[0]="dummy_mesh"

      # swy: get rid of/unset any Warband-only flags from the common items file
      #      seems like adding the itp_no_blur bits to M&B 1.011 causes the game
      #      to add a dummy "Requires : 16" line because the space was used for that: https://cdn.discordapp.com/attachments/492787561769599008/951814574968025149/nightly_build.JPG
      if not is_a_wb_item:
        item[3] &= ~itp_no_blur # potentially add more excluded ones here with ~(itp_no_blur | itp_other_wb_flag | itp_even_more_wb_flags)

      ofile.write(" %s %d "%(item_variation[0],item_variation[1]))
    ofile.write(" %d %d %d %d %s %d %d %d %d %d %d %d %d %d %d %d %d\n"%(item[3], item[4], item[5], item[7],
                                                   sf(get_weight(item[6])),
                                                   get_abundance(item[6]),                  
                                                   get_head_armor(item[6]),
                                                   get_body_armor(item[6]),
                                                   get_leg_armor(item[6]),
                                                   get_difficulty(item[6]),
                                                   get_hit_points(item[6]),
                                                   get_speed_rating(item[6]),
                                                   get_missile_speed(item[6]),
                                                   get_weapon_length(item[6]),
                                                   get_max_ammo(item[6]),
                                                   get_thrust_damage(item[6]),
                                                   get_swing_damage(item[6]),
                                                               ))
    if (wb_compile_switch == 1):
      if (len(item) > 9):
        ofile.write(" %d\n"%(len(item[9])))
        for item_faction in item[9]:
          ofile.write(" %d"%item_faction)
        ofile.write("\n")
      else:
        ofile.write(" 0\n")
    trigger_list = []
    if (len(item) > 8):
      trigger_list = item[8]
    save_simple_triggers(ofile,trigger_list, variable_list,variable_uses,tag_uses,quick_strings)


  ofile.close()

print("Exporting item data...")
save_python_header()



variable_uses = []
variables = load_variables(export_dir,variable_uses)
tag_uses = load_tag_uses(export_dir)
quick_strings = load_quick_strings(export_dir)
write_items(variables,variable_uses,tag_uses,quick_strings)
save_variables(export_dir,variables,variable_uses)
save_tag_uses(export_dir,tag_uses)
save_quick_strings(export_dir,quick_strings)
#print "Finished with Items."
