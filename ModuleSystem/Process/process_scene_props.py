import string

from module_info import *
from module_scene_props import *

from process_common import *
from process_operations import *

def save_scene_props(variable_list,variable_uses,tag_uses,quick_strings):
  ofile = open(export_dir + "scene_props.txt","w")
  ofile.write("scene_propsfile version 1\n")
  ofile.write(" %d\n"%(len(scene_props)))
  for scene_prop in scene_props:
    #swy-- fix shameful, sneaky typo rename of TW, that in WB breaks compatibility with existing ladder meshes, fsck you TW, FSCK YOU! >:(
    from module_info import wb_compile_switch as is_a_wb_scene_prop
    if (is_a_wb_scene_prop):
      scene_prop=list(scene_prop)
      scene_prop[2]=str(scene_prop[2]).replace("leadder","ladder")
      scene_prop[3]=str(scene_prop[3]).replace("leadder","ladder")
      #swy-- use old model included with the patch, the one coming with WB lacks a entrance ramp on one of the sides, sigh :(
      scene_prop[2]=str(scene_prop[2]).replace("castle_f_gatehouse_a","castle_f_gatehouse_a_compat")
   
    #<fisheye> modified the following code to allow for higher hit points on destructable scene props
    #ofile.write("spr_%s %d %d %s %s "%(scene_prop[0], scene_prop[1], get_spr_hit_points(scene_prop[1]), scene_prop[2], scene_prop[3]))
    if (len(scene_prop) == 5):
      ofile.write("spr_%s %d %d %s %s "%(scene_prop[0], scene_prop[1], get_spr_hit_points(scene_prop[1]), scene_prop[2], scene_prop[3]))
    elif (len(scene_prop) == 6):
      ofile.write("spr_%s %d %d %s %s "%(scene_prop[0], scene_prop[1], scene_prop[5] , scene_prop[2], scene_prop[3]))
    save_simple_triggers(ofile,scene_prop[4]  , variable_list,variable_uses,tag_uses,quick_strings)
    ofile.write("\n")
  ofile.close()


def save_python_header():
  from module_info import wb_compile_switch as is_wb
  if (is_wb):
    file = open("./ID/ID_scene_props_wb.py","w")
  else:
    file = open("./ID/ID_scene_props_mb.py","w")
  for i_scene_prop in xrange(len(scene_props)):
    file.write("spr_%s = %d\n"%(scene_props[i_scene_prop][0],i_scene_prop))
  file.close()

print "Exporting scene props..."
save_python_header()
variable_uses = []
variables = load_variables(export_dir,variable_uses)
tag_uses = load_tag_uses(export_dir)
quick_strings = load_quick_strings(export_dir)
save_scene_props(variables,variable_uses,tag_uses,quick_strings)
save_variables(export_dir,variables,variable_uses)
save_tag_uses(export_dir,tag_uses)
save_quick_strings(export_dir,quick_strings)
