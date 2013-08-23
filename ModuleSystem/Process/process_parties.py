import types
from header_game_menus import *
from module_info import *
from module_game_menus import *
from module_parties import *
from process_operations import *

from process_common import *


def save_parties(parties):
  file = open(export_dir + "parties.txt","w")
  file.write("partiesfile version 1\n")
  file.write("%d %d\n"%(len(parties), len(parties)))
  for i_party in xrange(len(parties)):
    party = parties[i_party]
    #print[party[0]]
    if (party[5] >= 0):
      add_tag_use(tag_uses,tag_faction,party[5])

    file.write(" 1 %d %d "%(i_party, i_party))
#    file.write(" 1 %d "%(i_party))
    file.write("p_%s %s %d "%(convert_to_identifier(party[0]),replace_spaces(party[1]),party[2]))
    menu_no = 0
    menu_param = party[3]
    if (type(menu_param) == types.StringType):
      menu_no = find_object(game_menus,menu_param)
      if (menu_no < 0):
        print "Error: Unable to find menu-id :" + menu_param
    else:
      menu_no = menu_param
    file.write("%d "%(menu_no))
    
    file.write("%d %d %d %d %d "%(party[4], party[5], party[6], party[6],party[7]))
    ai_behavior_object = 0
    ai_param = party[8]
    if (type(ai_param) == types.StringType):
      ai_behavior_object = find_object(parties,ai_param)
      if (ai_behavior_object < 0):
        print "Error: Unable to find party-id :" + ai_param
    else:
      ai_behavior_object = ai_param
    file.write("%d %d "%(ai_behavior_object,ai_behavior_object))
    position = party[9]
    default_behavior_location = position
    file.write("%f %f "%(default_behavior_location[0],default_behavior_location[1]))
    file.write("%f %f "%(default_behavior_location[0],default_behavior_location[1]))
    file.write("%f %f 0.0 "%position)
    member_list = party[10]
    file.write("%d "%len(member_list))
    for member in member_list:
      add_tag_use(tag_uses,tag_troop,member[0])
      file.write("%d %d 0 %d "%(member[0],member[1],member[2]))
    bearing = 0.0
    if (len(party) > 11):
      bearing = (3.1415926 / 180.0) * party[11]
    file.write("\n%f\n"%(bearing))
  file.close()

def save_python_header(parties):
  file = open("./ID_parties.py","w")
  for i_party in xrange(len(parties)):
    file.write("p_%s = %d\n"%(convert_to_identifier(parties[i_party][0]),i_party))
  file.close()


print "Exporting parties"
tag_uses = load_tag_uses(export_dir)
save_python_header(parties)
save_parties(parties)
save_tag_uses(export_dir, tag_uses)
#print "Generating C header..."
#save_c_header()
#print "Generating Python header..."
#print "Finished."
