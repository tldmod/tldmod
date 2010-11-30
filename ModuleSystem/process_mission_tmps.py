import string
import types

from module_info import *
from module_mission_templates import *

from process_common import *
from process_operations import *

mission_template_name_pos = 0
mission_template_flags_pos = 1
mission_template_types_pos = 2
mission_template_desc_pos = 3
mission_template_groups_pos =4
mission_template_triggers_pos = 5

def save_triggers(file,template_name,triggers,variable_list,variable_uses,tag_uses,quick_strings):
  file.write("%d\n"%len(triggers))
  for i in xrange(len(triggers)):
    trigger = triggers[i]
    file.write("%f %f %f "%(trigger[trigger_check_pos],trigger[trigger_delay_pos],trigger[trigger_rearm_pos]))
    save_statement_block(file, 0, 1, trigger[trigger_conditions_pos]  , variable_list,variable_uses,tag_uses,quick_strings)
    save_statement_block(file, 0, 1, trigger[trigger_consequences_pos], variable_list,variable_uses,tag_uses,quick_strings)
    file.write("\n")
  file.write("\n")

def save_mission_template_group(file,entry):
  if (len(entry[5]) > 8):
    print "ERROR: Too many item_overrides!"
    error()
  file.write("%d %d %d %d %d %d  "%(entry[0],entry[1],entry[2],entry[3],entry[4], len(entry[5])))
  for item_override in entry[5]:
    add_tag_use(tag_uses,tag_item,item_override)
    file.write("%d "%(item_override))
  file.write("\n")
    
def save_mission_templates(variables,variable_uses,tag_uses,quick_strings):
  file = open(export_dir + "mission_templates.txt","w")
  file.write("missionsfile version 1\n")
  file.write(" %d\n"%(len(mission_templates)))
  for mission_template in mission_templates:
    file.write("mst_%s %s %d "%(convert_to_identifier(mission_template[mission_template_name_pos]),convert_to_identifier(mission_template[mission_template_name_pos]),mission_template[mission_template_flags_pos]))
    file.write(" %d\n"%(mission_template[mission_template_types_pos]))
    file.write("%s \n"%(string.replace(mission_template[mission_template_desc_pos]," ","_")))
    file.write("\n%d "%len(mission_template[mission_template_groups_pos]))
    for group in mission_template[mission_template_groups_pos]:
      save_mission_template_group(file,group)
    save_triggers(file,convert_to_identifier(mission_template[mission_template_name_pos]), mission_template[mission_template_triggers_pos],variables,variable_uses,tag_uses,quick_strings)
    file.write("\n")
  file.close()

def save_python_header():
  file = open("./ID_mission_templates.py","w")
  for i_mission_template in xrange(len(mission_templates)):
    file.write("mst_%s = %d\n"%(mission_templates[i_mission_template][0],i_mission_template))
  file.close()

print "Exporting mission_template data..."
save_python_header()
variable_uses = []
variables = load_variables(export_dir, variable_uses)
tag_uses = load_tag_uses(export_dir)
quick_strings = load_quick_strings(export_dir)
save_mission_templates(variables,variable_uses,tag_uses,quick_strings)
save_variables(export_dir,variables,variable_uses)
save_tag_uses(export_dir,tag_uses)
save_quick_strings(export_dir,quick_strings)

#print "Finished."
  
"""  
  (
    "defense_1",mtf_battle_mode,stand_fast,
    "You wait, your weapons ready, your senses alert. Some of your companions start to sing an old song, trying to forget their fear. You smile and let your thoughts wander away for a second. Then the lookout's cry shatters the melancholy: 'Enemies! They are coming'",
    [
     (2,mtef_leader_only,0,group(1),1),
     (2,mtef_no_leader,0,group(1),3),
     (0,mtef_no_leader,0,group(1),0),
     (4,mtef_enemy_party|mtef_reverse_order,0,group(2)|aif_start_alarmed,5)],
    [],
    [
      (ti_val(0), ti_val(0), ti_once, [[mission_cookie_eq,0,0],[store_mission_timer_a,1],[ge,reg(1),10],[store_enemy_count,2],[lt,reg(2),3]], [[add_reinforcements_to_entry,3,3],[reset_mission_timer_a],[increment_mission_cookie,0]]),
      (ti_val(0), ti_val(0), ti_once, [[mission_cookie_eq,0,1],[store_mission_timer_a,1],[ge,reg(1),10],[store_enemy_count,2],[lt,reg(2),3]], [[add_reinforcements_to_entry,3,3],[reset_mission_timer_a],[increment_mission_cookie,0]]),
      (ti_val(0), ti_val(0), ti_once, [[mission_cookie_eq,5,0],[store_mission_timer_b,1],[ge,reg(1),10],[store_friend_count,2],[lt,reg(2),3]], [[add_reinforcements_to_entry,2,2],[reset_mission_timer_b],[increment_mission_cookie,5]]),
      (ti_val(0), ti_val(0), ti_once, [[mission_cookie_eq,5,1],[store_mission_timer_b,1],[ge,reg(1),10],[store_friend_count,2],[lt,reg(2),3]], [[add_reinforcements_to_entry,2,2],[reset_mission_timer_b],[increment_mission_cookie,5]]),
      (ti_val(0), ti_val(0), ti_once, [[all_enemies_defeated,2]], [[set_mission_result,1] ,[finish_mission,1]]),
      (ti_val(0), ti_val(0), ti_once, [[main_hero_fallen]], [[set_mission_result,-1],[finish_mission,1]]),
    ],
  ),
   (
    "chase_1",mtf_battle_mode,chase,
    "You close up on the enemy thinking that this will be an easy victory. But as you come within shooting range, enemy fighters stop fleeing and turn to meet you. Perhaps they are experienced enough to know that they can't outrun you. Or perhaps their warrior pride triumphed over their fear. Whatever it is, these men now seem to be willing to put up a fight and your job will not be easy",
    [(0,mtef_leader_only,0,group(1),1),(0,mtef_regulars_only,0,group(1),1),(1,mtef_regulars_only|mtef_enemy_party,0,aisb_hit_run,1),(2,mtef_regulars_only|mtef_enemy_party,0,0,2),(3,mtef_regulars_only|mtef_enemy_party,0,0,1),(4,mtef_regulars_only|mtef_enemy_party,0,group(2),2)],
    [],
    [
      (ti_val(0), ti_val(0), ti_once, [[all_enemies_defeated,2]], [[set_mission_result,1] ,[finish_mission,1]]),
      (ti_val(0), ti_val(0), ti_once, [[main_hero_fallen]], [[set_mission_result,-1],[finish_mission,1]]),
    ],
  ),
  (
    "slip_siege_fight_1",mtf_battle_mode,retreat_fight,
    "You lead your retreating party through a back road which, oddly enough, seems to be completely unguarded.\
 You decide to proceed with extreme caution. Very soon, you spot a movement in the bushes ahead.\
 Not taking any chances, you send an arrow into the bushes. The arrow sinks behind leaves and immediately produces\
 a sharp cry followed by some heavy cursing. Within seconds, a score of armored warriors rush out of hiding places.",
    [(2,mtef_leader_only,0,group(1),1),(2,mtef_no_leader,0,group(1)|aif_start_alarmed,3),(3,mtef_enemy_party|mtef_reverse_order,0,aif_start_alarmed,6)],
#    [(0,mtef_leader_only,0,group(1),1),(0,mtef_regulars_only,0,group(1),2|mtnf_const|mtnf_rand),(3,mtef_regulars_only|mtef_enemy_party,0,aif_start_alarmed,2|mtnf_const),(4,mtef_regulars_only|mtef_enemy_party,0,aif_start_alarmed,2|mtnf_const|mtnf_rand)],
    [],
    [
      (ti_val(0), ti_val(0), ti_once, [[all_enemies_defeated,3]], [[set_mission_result,1] ,[finish_mission,1]]),
      (ti_val(0), ti_val(0), ti_once, [[main_hero_fallen]], [[set_mission_result,-1],[finish_mission,1]]),
    ],
  ),
"""
