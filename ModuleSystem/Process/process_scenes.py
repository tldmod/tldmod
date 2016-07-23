from module_info import *
from module_scenes import *

from process_common import *

def save_python_header():
  ofile = open("./ID/ID_scenes.py","w")
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
  ofile.write(" %s %s %s "%(sf(vec[0]),sf(vec[1]),sf(vec[2])))
  
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
  
    #swy-- force to mark as enabled the disable_grass flag on Warband to avoid crashes
    #      a terrain code is made of five chunks of eight hex numbers each (32 bits)
    #      
    #      disable_grass is enabled when there's a b01 within its two bit bracket, located at 2 bit lshifts in the 5th chunk.    
    #      reference: http://mbmodwiki.ollclan.eu/SceneObj#Terrain_Codes
    
    from module_info import wb_compile_switch as is_a_wb_scene
    
    if (is_a_wb_scene and False): #swy-- disabled again now that we've a correct reverse engineered wb-compatible flora data file
      
      # enable the flag
      terrain_code = int(scene[7],16) | 0b01 << (32 * 5) + 2
      
      # 0x000000012c60280000034cd300003efe00004b34000059be
      #        0x52c60280000034cd300003efe00004b34000059beL
      #          ^
      
      # convert tuple to list, so we can modify it
      scene = list(scene)
      
      # format it as a string w/ zero padding until the 48th hex number!
      scene[7] = '0x%048x\n' % terrain_code
      
      # go back to being an immutable tuple because we can
      scene = tuple(scene)
      
      
      # the result is something like this, before/after.
      # doesn't looks like much, but fixes all the crashes.
      
      # 0x0000000329602800000691a400003efe00004b34000059be
      # 0x0000000729602800000691a400003efe00004b34000059be
      #          ^
      
    
    ofile.write("scn_%s %s %d %s %s %s %s %s %s %s %s "%(convert_to_identifier(scene[0]),replace_spaces(scene[0]),scene[1], scene[2],scene[3],sf(scene[4][0]),sf(scene[4][1]),sf(scene[5][0]),sf(scene[5][1]),sf(scene[6]),scene[7]))
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
