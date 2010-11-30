from module_info import *
from module_scenes import *

from process_common import *

def save_python_header():
  ofile = open("./ID_scenes.py","w")
  for i_scene in xrange(len(scenes)):
    ofile.write("scn_%s = %d\n"%(convert_to_identifier(scenes[i_scene][0]),i_scene))
  ofile.close()

print "Exporting scene data..."
save_python_header()

from process_operations import *
from module_troops import *

scene_name_pos = 0
passages_pos = 8
scene_outer_terrain_pos = 10


def write_vec(ofile,vec):
  ofile.write(" %f %f %f "%vec)
  
def write_passage(ofile,scenes,passage):
  scene_no = 0
  found = 0
  while (not found) and (scene_no < len(scenes)):
    if (scenes[scene_no][0] == passage):
      found = 1
    else:
      scene_no += 1
  if (passage == "exit"):
    scene_no = 100000
  elif (passage == ""):
    scene_no = 0
  elif not found:
    print "Error passage not found:"
    print passage
    do_error()
  ofile.write(" %d "%scene_no)


def save_scenes(variables,variable_uses,tag_uses):
  ofile = open(export_dir + "scenes.txt","w")
  ofile.write("scenesfile version 1\n")
  ofile.write(" %d\n"%len(scenes))
  for scene in scenes:
    ofile.write("scn_%s %s %d %s %s %f %f %f %f %f %s "%(convert_to_identifier(scene[0]),replace_spaces(scene[0]),scene[1], scene[2],scene[3],scene[4][0],scene[4][1],scene[5][0],scene[5][1],scene[6],scene[7]))
    passages = scene[passages_pos]
    ofile.write("\n  %d "%len(passages))
    for passage in passages:
      write_passage(ofile,scenes,passage)
    chest_troops = scene[9]
    ofile.write("\n  %d "%len(chest_troops))
    for chest_troop in chest_troops:
      troop_no = find_troop(troops,chest_troop)
      if (troop_no < 0):
        print "Error unable to find chest-troop: " + chest_troop
        troop_no = 0
      else:
        add_tag_use(tag_uses,tag_troop,troop_no)
      ofile.write(" %d "%troop_no)
    ofile.write("\n")
    if (len(scene) > scene_outer_terrain_pos):
      ofile.write(" %s "%scene[scene_outer_terrain_pos])
    else:
      ofile.write(" 0 ")
    ofile.write("\n")
  ofile.close()

variable_uses = []
variables = load_variables(export_dir, variable_uses)
tag_uses = load_tag_uses(export_dir)
quick_strings = load_quick_strings(export_dir)
save_scenes(variables,variable_uses,tag_uses)
save_variables(export_dir,variables,variable_uses)
save_tag_uses(export_dir,tag_uses)
save_quick_strings(export_dir,quick_strings)
