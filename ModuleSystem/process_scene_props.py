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
    ofile.write("spr_%s %d %d %s %s "%(scene_prop[0], scene_prop[1], get_spr_hit_points(scene_prop[1]), scene_prop[2], scene_prop[3]))
    save_simple_triggers(ofile,scene_prop[4]  , variable_list,variable_uses,tag_uses,quick_strings)
    ofile.write("\n")
  ofile.close()


def save_python_header():
  file = open("./ID_scene_props.py","w")
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
