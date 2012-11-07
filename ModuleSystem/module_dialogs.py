from header_common import *
from header_dialogs import *
from header_operations import *
from header_parties import *
from header_item_modifiers import *
from header_skills import *
from header_triggers import *
from ID_troops import *
from ID_party_templates import *
from header_troops import *
from header_items import * #TLD

from module_constants import *


####################################################################################################################
# During a dialog, the dialog lines are scanned from top to bottom.
# If the dialog-line is spoken by the player, all the matching lines are displayed for the player to pick from.
# If the dialog-line is spoken by another, the first (top-most) matching line is selected.
#
#  Each dialog line contains the following fields:
# 1) Dialogue partner: This should match the person player is talking to.
#    Usually this is a troop-id.
#    You can also use a party-template-id by appending '|party_tpl' to this field.
#    Use the constant 'anyone' if you'd like the line to match anybody.
#    Appending '|plyr' to this field means that the actual line is spoken by the player
#    Appending '|other(troop_id)' means that this line is spoken by a third person on the scene.
#       (You must make sure that this third person is present on the scene)
#
# 2) Starting dialog-state:
#    During a dialog there's always an active Dialog-state.
#    A dialog-line's starting dialog state must be the same as the active dialog state, for the line to be a possible candidate.
#    If the dialog is started by meeting a party on the map, initially, the active dialog state is "start"
#    If the dialog is started by speaking to an NPC in a town, initially, the active dialog state is "start"
#    If the dialog is started by helping a party defeat another party, initially, the active dialog state is "party_relieved"
#    If the dialog is started by liberating a prisoner, initially, the active dialog state is "prisoner_liberated"
#    If the dialog is started by defeating a party led by a hero, initially, the active dialog state is "enemy_defeated"
#    If the dialog is started by a trigger, initially, the active dialog state is "event_triggered"
# 3) Conditions block (list): This must be a valid operation block. See header_operations.py for reference.  
# 4) Dialog Text (string):
# 5) Ending dialog-state:
#    If a dialog line is picked, the active dialog-state will become the picked line's ending dialog-state.
# 6) Consequences block (list): This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

dialogs = [

[anyone ,"start", [(store_conversation_troop, "$g_talk_troop"),
                     (store_conversation_agent, "$g_talk_agent"),
                     (store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
#                     (troop_get_slot, "$g_talk_troop_relation", "$g_talk_troop", slot_troop_player_relation),
                     (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
                     (assign, "$g_talk_troop_relation", reg0),
                     (try_begin),
#                       (this_or_next|is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
                       (is_between, "$g_talk_troop", mayors_begin, mayors_end),
                       (party_get_slot, "$g_talk_troop_relation", "$current_town", slot_center_player_relation),
                     (try_end),
                     (store_relation, "$g_talk_troop_faction_relation", "$g_talk_troop_faction", "fac_player_faction"),
                     (assign, "$g_talk_troop_party", "$g_encountered_party"),
                     (try_begin),
                       (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
                       (troop_get_slot, "$g_talk_troop_party", "$g_talk_troop", slot_troop_leaded_party),
                     (try_end),
  				 	(str_store_faction_name, s14, "$ambient_faction"),

#                     (assign, "$g_talk_troop_kingdom_relation", 0),
#                     (try_begin),
#                       (gt, "$players_kingdom", 0),
#                       (store_relation, "$g_talk_troop_kingdom_relation", "$g_talk_troop_faction", "$players_kingdom"),
#                     (try_end),
                     (store_current_hours, "$g_current_hours"),
                     (troop_get_slot, "$g_talk_troop_last_talk_time", "$g_talk_troop", slot_troop_last_talk_time),
                     (troop_set_slot, "$g_talk_troop", slot_troop_last_talk_time, "$g_current_hours"),
                     (store_sub, "$g_time_since_last_talk","$g_current_hours","$g_talk_troop_last_talk_time"),
                     (troop_get_slot, "$g_talk_troop_met", "$g_talk_troop", slot_troop_met),
                     (troop_set_slot, "$g_talk_troop", slot_troop_met, 1),
                     (try_begin),
#                       (this_or_next|eq, "$talk_context", tc_party_encounter),
#                       (this_or_next|eq, "$talk_context", tc_castle_commander),
                       (call_script, "script_party_calculate_strength", "p_collective_enemy",0),
                       (assign, "$g_enemy_strength", reg0),
                       (call_script, "script_party_calculate_strength", "p_main_party",0),
                       (assign, "$g_ally_strength", reg0),
                       #(store_mul, "$g_strength_ratio", "$g_ally_strength", 100),
                       #(val_div, "$g_strength_ratio", "$g_enemy_strength"),
                     (try_end),
                     (assign, "$g_comment_found", 0),
                     (try_begin),
                       (troop_is_hero, "$g_talk_troop"),
                       (talk_info_show, 1),
                       (call_script, "script_setup_talk_info"),
                    (try_end),
                    (try_begin),
						(is_between, "$g_talk_troop", kingdom_heroes_begin, kingdom_heroes_end),
						(call_script, "script_get_relevant_comment_to_s42"),
						(assign, "$g_comment_found", reg0),
                    (try_end),
                    (troop_get_type, reg65, "$g_talk_troop"),
                    (try_begin),
                       (neq, reg65, 1), #not female
                       (assign, reg65, 0), #make it male for strings
                    (try_end),
                    (try_begin),
                       (faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop"),
                       (try_begin),
                         (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
                         (str_store_string,s64,"@{reg65?my Lady:my Lord}"), #bug fix
                         (str_store_string,s66,"@{reg65?My Lady:My Lord}"), #bug fix
                       (else_try),
                         (str_store_string,s64,"@{reg65?mistress:master}"), #bug fix
                         (str_store_string,s66,"@{reg65?Mistress:Master}"), #bug fix
                       (try_end),
                    (else_try),
                       (try_begin),
                         (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
                         (str_store_string,s64,"@{reg65?madame:sir}"), #bug fix
                         (str_store_string,s66,"@{reg65?Madame:Sir}"), #bug fix
                       (else_try),
                         (str_store_string,s64,"@{reg65?mistress:master}"), #bug fix
                         (str_store_string,s66,"@{reg65?Mistress:Master}"), #bug fix
                       (try_end),
                    (try_end),
                    (str_store_string_reg,s65,s64),
                    (str_store_string_reg,s67,s66), #bug fix
                    # put orc/uruk heads out of the way
					(get_player_agent_no, "$current_player_agent"),
					(troop_get_type, ":race", "$player_current_troop_type"),
					(try_begin),
						(is_between, ":race", tf_orc_begin, tf_orc_end),
						(agent_get_horse,reg1,"$current_player_agent"),
						(try_begin),(eq, reg1, -1),(agent_set_animation, "$current_player_agent", "anim_lean_from_camera"),
						 (else_try),               (agent_set_animation, "$current_player_agent", "anim_lean_from_camera_mounted"),
						(try_end),
					(try_end),
					(eq, 1, 0)],
"Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],

# unified chat for review or access from party window (mtarini)
[anyone|auto_proceed,"start", [(eq, "$talk_context", tc_troop_review_talk),(agent_has_item_equipped, "$g_talk_agent", "itm_feet_chains")], "___", "prisoner_chat_00",[]],
[anyone|auto_proceed ,"prisoner_chat", [], "___", "prisoner_chat_00",[]],
[anyone|auto_proceed,"start", [(eq, "$talk_context", tc_troop_review_talk),], "___", "member_chat_00",[]],
[anyone|auto_proceed ,"member_chat", [], "___", "member_chat_00",[]],


[anyone ,"member_chat_00", [(store_conversation_troop, "$g_talk_troop"),
                           (try_begin),
                               (is_between, "$g_talk_troop", companions_begin, companions_end),
                               (talk_info_show, 1),
                               (call_script, "script_setup_talk_info_companions"),
                           (try_end),
                     (troop_get_type, reg65, "$g_talk_troop"),
                     (try_begin),
                       (neq, reg65, 1), #not female
                       (assign, reg65, 0), #make it male for strings
                     (try_end),
                     (try_begin),
                       (faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop"),
                       (try_begin),
                         (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
                         (str_store_string,s64,"@{reg65?my Lady:my Lord}"), #bug fix
                         (str_store_string,s66,"@{reg65?My Lady:My Lord}"), #bug fix
                       (else_try),
                         (str_store_string,s64,"@{reg65?mistress:master}"), #bug fix
                         (str_store_string,s66,"@{reg65?Mistress:Master}"), #bug fix
                       (try_end),
                     (else_try),
                       (try_begin),
                         (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
                         (str_store_string,s64,"@{reg65?madame:sir}"), #bug fix
                         (str_store_string,s66,"@{reg65?Madame:Sir}"), #bug fix
                       (else_try),
                         (str_store_string,s64,"@{reg65?mistress:master}"), #bug fix
                         (str_store_string,s66,"@{reg65?Mistress:Master}"), #bug fix
                       (try_end),
                     (try_end),
                     (str_store_string_reg,s65,s64),
                     # put orc/uruk heads out of the way
					 (get_player_agent_no, "$current_player_agent"),
					 (agent_get_horse,reg1,"$current_player_agent"),
					 (troop_get_type, ":race", "$player_current_troop_type"),
                    (try_begin),
						(is_between, ":race", tf_orc_begin, tf_orc_end),
						(try_begin),(eq, reg1, -1),(agent_set_animation, "$current_player_agent", "anim_lean_from_camera"),
						 (else_try),               (agent_set_animation, "$current_player_agent", "anim_lean_from_camera_mounted"),
						(try_end),
					(try_end),
					(eq, 1, 0)],  
"Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],

[anyone ,"event_triggered", [(store_conversation_troop, "$g_talk_troop"),
                           (try_begin),
                               (is_between, "$g_talk_troop", companions_begin, companions_end),
                               (talk_info_show, 1),
                               (call_script, "script_setup_talk_info_companions"),
                           (try_end),
                     (troop_get_type, reg65, "$g_talk_troop"),
                     (try_begin),
                       (neq, reg65, 1), #not female
                       (assign, reg65, 0), #make it male for strings
                     (try_end),
                     (try_begin),
                       (faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop"),
                       (try_begin),
                         (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
                         (str_store_string,s64,"@{reg65?my Lady:my Lord}"), #bug fix
                         (str_store_string,s66,"@{reg65?My Lady:My Lord}"), #bug fix
                       (else_try),
                         (str_store_string,s64,"@{reg65?mistress:master}"), #bug fix
                         (str_store_string,s66,"@{reg65?Mistress:Master}"), #bug fix
                       (try_end),
                     (else_try),
                       (try_begin),
                         (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
                         (str_store_string,s64,"@{reg65?madame:sir}"), #bug fix
                         (str_store_string,s66,"@{reg65?Madame:Sir}"), #bug fix
                       (else_try),
                         (str_store_string,s64,"@{reg65?mistress:master}"), #bug fix
                         (str_store_string,s66,"@{reg65?Mistress:Master}"), #bug fix
                       (try_end),
                    (try_end),
                    (str_store_string_reg,s65,s64),
                    # put orc/uruk heads out of the way
					(get_player_agent_no, "$current_player_agent"),
					(agent_get_horse,reg1,"$current_player_agent"),
					(troop_get_type, ":race", "$player_current_troop_type"),
					(try_begin),
						(is_between, ":race", tf_orc_begin, tf_orc_end),
						(try_begin),(eq, reg1, -1),(agent_set_animation, "$current_player_agent", "anim_lean_from_camera"),
						 (else_try),               (agent_set_animation, "$current_player_agent", "anim_lean_from_camera_mounted"),
						(try_end),
					(try_end),
					(eq, 1, 0)],  
"Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],

#GA: orc pretender dialogs
[trp_orc_pretender, "start", [(eq,"$mutiny_stage",0)], "Hey, {playername}. We tell you what.. ^Lads here grumbling! Want more fun, less marching around.", "mutiny_pretalk_1",[]],
[trp_orc_pretender|plyr, "mutiny_pretalk_1", [], "Fall back in line, maggot! We are at war and I'm your commander.", "mutiny_pretalk_2",[]],
[trp_orc_pretender, "mutiny_pretalk_2", [], "As you wish, commander. As you wish...", "close_window",[(assign,"$mutiny_stage",1),(jump_to_menu, "mnu_premutiny")]],

[trp_orc_pretender, "start", [(eq,"$mutiny_stage",2)], "Hey, commander. We tell you what... Lads here are not happy, not happy at all. ^Not enough manflesh, not enough fun. ^Lads here talk you not good enough, commander!", "mutiny_talk_1",[]],
[trp_orc_pretender|plyr, "mutiny_talk_1", [], "What? Mutiny while at war? ^This is punishable by death, maggot!", "mutiny_talk_2",[]],
[trp_orc_pretender, "mutiny_talk_2", [], "We tell you what... ^Lads here think I be better commander for them when I KILL YOU!", "close_window",[
	(assign,"$mutiny_stage",3),
    (jump_to_menu, "mnu_mutiny")]],

#MV: Easter Egg Troll dialogs
[trp_easter_egg_troll, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_continue")], "Problem?", "troll_introduce_1",[]],
[trp_easter_egg_troll, "start", [(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_continue")], "U mad?", "troll_talk_1",[]],
  
[trp_easter_egg_troll|plyr, "troll_introduce_1", [], "Whoa! A talking troll?!", "troll_goodbye",[(troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1)]],
[trp_easter_egg_troll|plyr, "troll_introduce_1", [], "I own a horse.", "close_window",[(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_rise"),(call_script,"script_stand_back"),]],
  
[trp_easter_egg_troll|plyr, "troll_talk_1", [], "Troll me, troll.", "troll_talk_2",[]],
[trp_easter_egg_troll|plyr, "troll_talk_1", [], "I own a horse.", "close_window",[(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_rise"),(call_script,"script_stand_back"),]],
  
[trp_easter_egg_troll, "troll_talk_2", [
    (store_random_in_range, ":random", 0, 11),
    (try_begin),    #s4: troll question, s5: fail answer, s6: win answer
      (eq, ":random", 0),
      (str_store_string, s4, "@How do magnets work?"),
      (str_store_string, s5, "@Um... by enchanting iron?"),
      (str_store_string, s6, "@Magnets are made of metal, which is mined from the ground. They are magnetic because the metal still contains pieces of gravity inside it."),
    (else_try),
      (eq, ":random", 1),
      (str_store_string, s4, "@i wont a warband port nao!!11!"),
      (str_store_string, s5, "@I'm sure the TLD team will get to it when they can."),
      (str_store_string, s6, "@Install TLD in your Warband Modules folder, add the line 'compatible_with_warband = 1' to module.ini, and you can play it on Warband!"),
    (else_try),
      (eq, ":random", 2),
      (str_store_string, s4, "@dis mod takes 2 long 2 releaze! it sux!!11!"),
      (str_store_string, s5, "@Well, there's a lot of new graphics and stuff, I guess that takes time."),
      (str_store_string, s6, "@It has been recently released, if you missed the link, you can download it at lemonparty.org."),
    (else_try),
      (eq, ":random", 3),
      (str_store_string, s4, "@i wont decapitated elephants in multi, nao!!11!"),
      (str_store_string, s5, "@I don't think there's multiplayer in TLD, but elephants would be nice."),
      (str_store_string, s6, "@There is a hidden elephant deathmatch mode in TLD, but you need to remove all your savegames first, play for a 100 game days without saving then go to the character screen and press Alt+F4. Totally worth it!"),
    (else_try),
      (eq, ":random", 4),
      (str_store_string, s4, "@Did you bring your zupdog?"),
      (str_store_string, s5, "@What's zupdog?"),
      (str_store_string, s6, "@My zupdog is ill, but I brought my zupmaiass."),
    (else_try), #MV: next Triglav's jokes, don't blame me :)
      (eq, ":random", 5),
      (str_store_string, s4, "@Wai no plate armour in mod???"),
      (str_store_string, s5, "@What is plate armour? Never heard of it."),
      (str_store_string, s6, "@Wai no female trolls? Eh? Eh? You ma biatch!"),
    (else_try),
      (eq, ":random", 6),
      (str_store_string, s4, "@WHEN U REALSE MOD?!!?"),
      (str_store_string, s5, "@But we did release. You're in it. And why are you shouting?"),
      (str_store_string, s6, "@YES! ALSO SOMETIMES IS!"),
    (else_try),
      (eq, ":random", 7),
      (str_store_string, s4, "@Wai u no work wiht otehr mods to make a super LOTR mod?"),
      (str_store_string, s5, "@Every mod team works according to their standards, you can't make mods cooperate if their vision is different."),
      (str_store_string, s6, "@Because we don't have a sense of humour and most of them are just too funny for us."),
    (else_try),
      (eq, ":random", 8),
      (str_store_string, s4, "@In movies trolls are big and fat, wai u make me skinny?"),
      (str_store_string, s5, "@We interpreted Tolkien like this."),
      (str_store_string, s6, "@But we did make you as stupid as in the movies. That's gotta count for something."),
    (else_try),
      (eq, ":random", 9),
      (str_store_string, s4, "@What is news? Got any screenshots?"),
      (str_store_string, s5, "@Well just look around you, what do you need screenshots for?"),
      (str_store_string, s6, "@Say cheese!"),
    (else_try),
      #(eq, ":random", 10),
      (str_store_string, s4, "@Why did you make mod installation so complex?"), #GA
      (str_store_string, s5, "@Well, if you are here and talking to me, you must've RTFM successfully after all"),
      (str_store_string, s6, "@You just got windyflorated!"),
    (try_end)],
"Challenge accepted!^^{s4}", "troll_talk_3",[]],
    
[trp_easter_egg_troll|plyr, "troll_talk_3", [
    (store_attribute_level, ":int", "trp_player", ca_intelligence),
    (gt, ":int", 12)],
"{s6}", "troll_beaten",[]],
[trp_easter_egg_troll|plyr, "troll_talk_3", [
    (store_attribute_level, ":int", "trp_player", ca_intelligence),
    (le, ":int", 12)],
"{s5}", "troll_goodbye",[]],
  
[trp_easter_egg_troll, "troll_beaten", [(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_rise")], "I bow to your wisdom, Master Baiter of Trolls!", "troll_talk_1",[]],
[trp_easter_egg_troll, "troll_goodbye", [(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_rise")], "TROLLOLOLOLOLOLOLOLOLOL!", "close_window",[(call_script,"script_stand_back"),]],
  
 
 #### HOBBITS CHATS... prelimintaries (mtarini)
 
 # phase 1: first time talk

[trp_merry_notmet, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 1),], "Hello again, {playername}!","hobbit_merry_talk_met",[] ],
[trp_pippin_notmet, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 1),], "Hello again, {playername}!","hobbit_pippin_talk_met",[] ],
 
[trp_merry_notmet, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),], "Hello, {sir/madam}! My name is Meriadoc Brandybuck but you can call me Merry!","hobbit_general_talk_1",[] ],
[trp_pippin_notmet, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),], "Hello, {sir/madam}! My name is Peregrin Took but you can call me Pippin!","hobbit_general_talk_1",[] ],

[anyone|plyr, "hobbit_general_talk_1", [], "I don't have time now.","close_window",[(call_script,"script_stand_back"), ], ],

[anyone|plyr, "hobbit_general_talk_1", [(troop_slot_eq, "trp_pippin_notmet", slot_troop_met_previously, 0),(troop_slot_eq, "trp_merry_notmet", slot_troop_met_previously, 0),], 
	"Say. I think I never seen one of your kind.","hobbit_general_talk_first_met",[(troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1),] ],

[anyone|plyr, "hobbit_general_talk_1", [(eq, "$g_talk_troop", "trp_pippin_notmet"), (troop_slot_eq, "trp_merry_notmet", slot_troop_met_previously, 1),], "Say. I think I've met another one like you, in Edoras.","hobbit_general_talk_second_met",[(troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1),] ],

[anyone|plyr, "hobbit_general_talk_1", [(eq, "$g_talk_troop", "trp_merry_notmet"), (troop_slot_eq, "trp_pippin_notmet", slot_troop_met_previously, 1),], "Say. I think I've met another one like you, in Minas Tirith.","hobbit_general_talk_second_met",[(troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1),] ],

[anyone,  "hobbit_general_talk_first_met", [], "I know. I came from afar! I'm a Hobbit, {sir/madam}, from the Shire.","hobbit_general_talk_3",[] ],

[trp_merry_notmet,   "hobbit_general_talk_second_met", [], "Oh, that must have been my dear cousin! Peregrin Took, or Pippin, how they call him. We are Hobbits, {sir/madam}, and we come from the Shire, both of us! Good old Pippin, I wonder how he is doing in Minas Tirith.","hobbit_general_talk_3",[] ],

[trp_pippin_notmet,   "hobbit_general_talk_second_met", [], "Oh, that must have been my dear cousin! Meriadoc Brandybuck, or Merry, how they call him. We are Hobbits, {sir/madam}, and we come from the Shire, both of us! Good old Merry, I wonder how he is doing back in Edoras.","hobbit_general_talk_3",[] ],

[anyone|plyr,  "hobbit_general_talk_3", [], "Well, goodbye now.","close_window",[  (call_script,"script_stand_back"), ] ],

# phase 2: any other time
[trp_merry, "start", [], "Welcome back, {playername}!","hobbit_merry_talk_met",[] ],
[trp_pippin, "start", [], "Welcome back, {playername}!","hobbit_pippin_talk_met",[] ],

[anyone|plyr, "hobbit_merry_talk_met", [], "Hello, messer Merry.","close_window",[(agent_set_animation, "$current_player_agent", "anim_cancel_ani_stand")] ],
[anyone|plyr, "hobbit_pippin_talk_met", [], "Hello, messer Pippin.","close_window",[(agent_set_animation, "$current_player_agent", "anim_cancel_ani_stand")] ],

  
#MV: Treebeard dialogs - text by Treebeard (JL)
[trp_treebeard, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_continue")],
"(You find that you are looking at a most extraordinary creature. He is very tall and stiff-limbed with bark-like skin and leafy hair. Moss is also covering parts of his body. But at the moment you are noting little but the eyes. The deep eyes are surveying you, slow and solemn but very sharp and penetrating. You think they are brown, shot with green light, as if there is an enormous well behind them, filled up with ages of memory and long, slow, steady thinking. But on the surface his eyes are sparkling with the present... like the sun shimmering on the outer leaves of a vast tree, or the ripples of a very deep lake.)", "treebeard_introduce_1", []],
[trp_treebeard, "treebeard_introduce_1", [], "(You are about to say something but a strange stifling feeling falls upon you, as if the air is too thin or too scanty for breathing... with an almost desperate inhale of air you manage to shake loose the feeling and the huge tree-like creature drops the intensity of his gaze a little bit. The creature continues to look at you and you notice the other huge tree creatures are watching you too, as if expecting you to speak...)", "treebeard_introduce_2",[]],
[trp_treebeard|plyr, "treebeard_introduce_2", [], "Pardon my intrusion... I'm but a weary traveler seeking refuge from recent events... my name is {playername}. Might I ask who you are?", "treebeard_introduce_3",[]],
[trp_treebeard, "treebeard_introduce_3", [], "(The stiff-limbed tree giant slowly opens his mouth which is concealed behind small branches, leaves and moss. With a very deep, slow and booming voice he very slowly expounds in a most commanding way:)^\
  'Hrooom... Hmmm... *I* am not going to tell you my name... not yet at any rate. For one thing it would take a long while. My name is growing all the time and I've lived a very long, long time; so my name is like a story. Real names tell you the story of things they belong to in my language, in the Old Entish as you might say. It is a lovely language, but it takes a very long time saying anything in it, because we do not say anything in it, unless it is worth taking a long time to say, and to listen to.'", "treebeard_introduce_4",[]],
[trp_treebeard|plyr, "treebeard_introduce_4", [], "Oh, you are an Ent! Legends speak of you and I am honored to be in your presence. I do not wish to impose and will leave if you so wish.", "treebeard_introduce_5",[]],
[trp_treebeard, "treebeard_introduce_5", [], "(The stiff-limped giant and his fellow Ents stand still for many minutes in silence while a breeze passes through their leafy hairs and beards. They look at each other for another prolonged moment until an unusually hasty Ent who is resembling a rowan tree seems to want to speak. However, he stays silent until the giant stiff-limped Ent continues:)", "treebeard_questtalk",[]],
[trp_treebeard|auto_proceed, "start", [], "ERROR", "treebeard_questtalk",[]],
  
  # [trp_treebeard|plyr, "treebeard_introduce_1", [], "Hi, talking tree!", "treebeard_talk",[
   # (troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1),
  # ]],
  # [trp_treebeard|plyr, "treebeard_introduce_1", [], "I'm not a little orc. Goodbye.", "close_window",[]],
  
[trp_treebeard, "treebeard_questtalk", [
	 (neg|check_quest_active, "qst_treebeard_kill_orcs"),
	 (quest_slot_eq, "qst_treebeard_kill_orcs", slot_quest_current_state, 0),
	 (troop_get_type, reg1, "trp_player"),
	 (try_begin),
	   (is_between, reg1, tf_elf_begin, tf_elf_end),
	   (assign, reg1, 0), #elves
	 (else_try),
	   (assign, reg1, 1), #others
	 (try_end),
	 (troop_get_slot, reg2, "trp_treebeard", slot_troop_met_previously)], 
"{reg2?As I said before...:Hroom... We appreciate the courteous manners that you display. It is {reg1?unusual from your race:nice to speak with elves again}.} Times are not good, ever since the Entwives disappeared - and now there are many evil creatures released by the Dark Lord himself who are trying to destroy our homes. We seek someone who is fast but not hasty. Someone who can help us while we discuss our next moves.^Many bands of orcs have raided the woods and burned down our trees with fire arrows - if you were to defeat the orcs and make sure that they do not threaten the woods we would be grateful and consider you a true friend. Do this and we will talk again.",
  "treebeard_quest_brief",[(troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1)]],
  
[trp_treebeard|plyr,"treebeard_quest_brief", [],
"Orcs are vile creatures indeed. I will make sure they do not harm the forest again.", "close_window", [
	(call_script,"script_stand_back"),
	(set_spawn_radius,7),
    (spawn_around_party, "p_fangorn_center", "pt_fangorn_orcs"),
    (quest_set_slot, "qst_treebeard_kill_orcs", slot_quest_target_party, reg0),
    (quest_set_slot, "qst_treebeard_kill_orcs", slot_quest_giver_troop, "trp_treebeard"),
    (setup_quest_text, "qst_treebeard_kill_orcs"),
    (str_store_string, s2, "@Treebeard wants you find and defeat the orcs cutting down trees in Fangorn."),
    (call_script, "script_start_quest", "qst_treebeard_kill_orcs", "trp_treebeard")]],
  # [trp_treebeard, "treebeard_quest_taken", [], "Good. And bring me some orc ears when you are done.", "close_window", []],
  
[trp_treebeard|plyr,"treebeard_quest_brief", [], "Sorry. I don't have time for this right now.", "treebeard_pretalk",[]],
    
[trp_treebeard, "treebeard_questtalk", [(check_quest_active, "qst_treebeard_kill_orcs"),
                                          (check_quest_succeeded, "qst_treebeard_kill_orcs")], 
"(The Ent leader slowly opens his concealed mouth and the other Ents look at you and also slowly begin to utter a long deep sound that makes the ground shake a little - you realize that they are laughing in an Entish way. A relatively young Rowan tree looking Ent stomps his seven-toed large feet in the ground and the shake almost makes you fall.)^'Easy there, Quickbeam, we don't want to hurt our young warrior friend. Hrrrm... I am Treebeard, the oldest of the Ents, and we are all grateful for your services... Hrrrm... Let me give you a gift of Ent Water to celebrate your success.'", "close_window",[
    (call_script,"script_stand_back"),
	(add_xp_as_reward, 2000),
    (troop_add_item, "trp_player", "itm_ent_water", 0), #MV: reward for defeating the orcs
    (call_script, "script_end_quest", "qst_treebeard_kill_orcs"),
    (quest_set_slot, "qst_treebeard_kill_orcs", slot_quest_current_state, 1)]],
  
[trp_treebeard, "treebeard_questtalk", [(check_quest_active, "qst_treebeard_kill_orcs")], 
"(The stiff-limped giant and his fellow Ents stand still in silence while a breeze passes through their leafy hairs and beards.)", "close_window",[(call_script,"script_stand_back"),]],
  
[trp_treebeard|auto_proceed, "treebeard_questtalk", [], "ERROR", "treebeard_pretalk",[]],
  
[trp_treebeard, "treebeard_pretalk", [], "Hrooom... What would you like to know, young friend?", "treebeard_talk_response",[]],

[trp_treebeard|plyr, "treebeard_talk_response", [], "Tell me more about you.", "treebeard_about_himself",[]],
[trp_treebeard|plyr, "treebeard_talk_response", [], "Tell me about the Entwives.", "treebeard_about_entwives",[]],
[trp_treebeard|plyr, "treebeard_talk_response", [], "Tell me about the Ents.", "treebeard_about_ents",[]],
[trp_treebeard|plyr, "treebeard_talk_response", [], "Never mind, goodbye.", "close_window",[(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_rise"),(call_script,"script_stand_back"),]],
  
[trp_treebeard, "treebeard_about_himself", [(quest_slot_eq, "qst_treebeard_kill_orcs", slot_quest_current_state, 0)],
"(The Ent leader looks distant and solemn. After a while he slowly says:)^'Don't be hasty... we can talk more about this when the woods are safe from the orcs.'", "treebeard_pretalk",[]],
[trp_treebeard, "treebeard_about_himself", [],
"Hrooom... I am the oldest of my kind hmmm... I am known as Treebeard by a few mortals and the Elves call me Fangorn. Hummm... I, Skinbark and Leaflock are the only Ents who have walked the forests before the Darkness. I am no longer very bendable as I used to be... young Quickbeam can bend and sway, like a slender tree in the wind... Hummm... If the Entwives were here...", "treebeard_pretalk",[]],

[trp_treebeard, "treebeard_about_entwives", [(quest_slot_eq, "qst_treebeard_kill_orcs", slot_quest_current_state, 0)],
"(The Ent leader suddenly gets an expression of sadness and his voice is unusually deep.)^'Hummm... This is a sad tale... when the woods are free from the orcs we can discuss this.'", "treebeard_pretalk",[]],
[trp_treebeard, "treebeard_about_entwives", [],
"Ahummm... the beautiful Entwives... they like to plant and grow... we should have listened more to them... Hrooom... then they left to the Brown Lands to plant gardens and they taught mortals about making the lands fertile... we used to visit them... until... Sauron attacked... the Entwives are now lost... Hummm... Fimbrethil... her hue of ripe grain... we have looked for them... but not found them... yet...", "treebeard_pretalk",[]],
    
[trp_treebeard, "treebeard_about_ents", [],
"Hrooom... We are shepherds of the Trees and we protect them from perils. We are older than any of the mortal races but not as old as the Elves who cured us from dumbness. Things have changed over the ages. In the beginning we were more hasty and flexible. Over time many of us have been lost. Some of us are still true Ents, and lively enough in our fashion, but many are growing sleepy, going tree-ish, as you might say. Most of the trees are just trees, of course; but many are half awake. Some are quite wide awake, and a few are, well, ah, well getting Entish. That is going on all the time. When that happens to a tree, you find that some have bad hearts. Still, we do what we can. We keep off strangers and the foolhardy; and we train and we teach, we walk and we weed.", "treebeard_pretalk",[]],

#  [trp_treebeard|plyr, "treebeard_talk_1", [], "Troll me, troll.", "treebeard_talk_2",[]],
  # [trp_treebeard|plyr, "treebeard_talk_1", [], "Likewise.", "close_window",[]],
  
  # [trp_treebeard, "treebeard_goodbye", [], "Goodbye, little orc!", "close_window",[]],

#MV: Other ents
[trp_ent_1, "start", [], "Mmmmm?", "close_window",[(call_script,"script_stand_back"),]],
[trp_ent_2, "start", [], "Mmhhrmmm?", "close_window",[(call_script,"script_stand_back"),]],
[trp_ent_3, "start", [], "Mmmrhrrhmm?", "close_window",[(call_script,"script_stand_back"),]],

 # [party_tpl|pt_manhunters,"start", [(eq,"$talk_context",tc_party_encounter)], "Hey, you there! You seen any outlaws around here?", "manhunter_talk_b",[]],
 # [party_tpl|pt_manhunters|plyr,"manhunter_talk_b", [], "Yes, they went this way about an hour ago.", "manhunter_talk_b1",[]],
 # [party_tpl|pt_manhunters,"manhunter_talk_b1", [], "I knew it! Come on, lads, lets go get these bastards! Thanks a lot, friend.", "close_window",[(assign, "$g_leave_encounter",1)]],
 # [party_tpl|pt_manhunters|plyr,"manhunter_talk_b", [], "No, haven't seen any outlaws lately.", "manhunter_talk_b2",[]],
 # [party_tpl|pt_manhunters,"manhunter_talk_b2", [], "Bah. They're holed up in this country like rats, but we'll smoke them out yet. Sooner or later.", "close_window",[(assign, "$g_leave_encounter",1)]],


# [anyone,"bandit_introduce", [
      # (store_random_in_range, ":rand", 11, 15),
        # (str_store_string, s11, "@I can smell a fat purse a mile away. Methinks yours could do with some lightening, eh?"),
        # (str_store_string, s12, "@Why, it be another traveller, chance met upon the road! I should warn you, country here's a mite dangerous for a good {fellow/woman} like you. But for a small donation my boys and I'll make sure you get rightways to your destination, eh?"),
        # (str_store_string, s13, "@Well well, look at this! You'd best start coughing up some silver, friend, or me and my boys'll have to break you."),
		# (str_store_string, s14, "@There's a toll for passin' through this land, payable to us, so if you don't mind we'll just be collectin' our due from your purse..."),
        # (str_store_string_reg, s5, ":rand"),], 
# "{s5}", "bandit_talk",[
# ]],



# [anyone|plyr,"bandit_meet", [], 
# "Your luck has run out, wretch. Prepare to die!", "bandit_attack",[
    # (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until, 0)]],
  
# [anyone,"bandit_attack", [
      # (store_random_in_range, ":rand", 11, 15),
        # (str_store_string, s11, "@Another fool come to throw {him/her}self on my weapon, eh? Fine, let's fight!"),
        # (str_store_string, s12, "@We're not afraid of you, {sirrah/wench}. Time to bust some heads!"),
        # (str_store_string, s13, "@That was a mistake. Now I'm going to have to make your death long and painful."),
        # (str_store_string, s14, "@Brave words. Let's see you back them up with deeds, cur!"),
        # (str_store_string_reg, s5, ":rand")], 
# "{s5}", "close_window",[]],


[anyone|auto_proceed,"start", [(eq,"$talk_context",tc_party_encounter),(eq,"$encountered_party_hostile",1),], "Warning: This line should never be displayed.", "hostile_dialog",[
	(assign, ":defending", 1),
	(try_begin),
		(encountered_party_is_attacker),
		(assign, ":defending", 0),
	(try_end),
	(call_script, "script_str_store_party_battle_cry_in_s4", "$g_encountered_party", ":defending" )]],

[anyone,"hostile_dialog", [], "{s4}", "close_window",[(call_script,"script_stand_back"),]],

[anyone|plyr,"start", [ (eq,"$talk_context",tc_make_enemy_join_player),
						(str_store_item_name, s4, "itm_angmar_whip_reward")],
"Bow to the power of the {s4} and serve me!", "looters_2_join", []],

[anyone,"looters_2_join", [], "We will obey, Master.", "close_window", [
     (call_script,"script_stand_back"),
	 (call_script, "script_party_add_party", "p_main_party", "$g_encountered_party"),
     (remove_party, "$g_encountered_party"),
	 (change_screen_return),
     (assign, "$g_leave_encounter", 1)]],
  
#[party_tpl|pt_looters|plyr,"looters_2", [(store_character_level,reg1,"trp_player"),(lt,reg1,4)], 
#"I'm not afraid of you lot. Fight me if you dare!", "close_window", [(encounter_attack)]],
# [party_tpl|pt_looters|plyr,"looters_2", [], 
# "You'll have nothing of mine but cold steel, scum.", "close_window", [(call_script,"script_start_current_battle"),(encounter_attack)]],
#####################################################################
#TLD STUFFF
#####################################################################

[pt_wild_troll|party_tpl, "start", [], "^^GROWL!^^", "close_window",[] ],


### COMPANIONS
[anyone,"start", [(troop_slot_eq,"$g_talk_troop", slot_troop_occupation, slto_player_companion),
                    (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
                    (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
                    (ge, ":num_stacks", 1),
                    (party_stack_get_troop_id, ":castle_leader", "$g_encountered_party", 0),
                    (eq, ":castle_leader", "$g_talk_troop"),
                    (eq, "$talk_context", 0)],
"Yes, {playername}? What can I do for you?", "member_castellan_talk",[]],
  
[anyone,"member_castellan_pretalk", [], "Anything else?", "member_castellan_talk",[]],
  
[anyone|plyr,"member_castellan_talk", [], "I want to review the castle garrison.", "member_review_castle_garrison",[]],
[anyone,"member_review_castle_garrison", [], "Of course. Here are our lists, let me know of any changes you require...", "member_castellan_pretalk",[(change_screen_exchange_members,0)]],
[anyone|plyr,"member_castellan_talk", [], "Let me see your equipment.", "member_review_castellan_equipment",[]],
[anyone,"member_review_castellan_equipment", [], "Very well, it's all here...", "member_castellan_pretalk",[#(assign, "$equip_needs_checking", 1),
  (change_screen_equip_other),(call_script, "script_check_equipped_items","$g_talk_troop")]],
[anyone|plyr,"member_castellan_talk", [], "I want you to abandon the castle and join my party.", "member_castellan_join",[]],
[anyone,"member_castellan_join", [(party_can_join_party,"$g_encountered_party","p_main_party")],
"I've grown quite fond of the place... But if it is your wish, {playername}, I'll come with you.", "close_window", [
       (call_script,"script_stand_back"),
	   (assign, "$g_move_heroes", 1),
       (call_script, "script_party_add_party", "p_main_party", "$g_encountered_party"),
       (party_clear, "$g_encountered_party")]],
[anyone,"member_castellan_join", [], "And where would we sleep? You're dragging a whole army with you, {playername}, there's no more room for all of us.", "member_castellan_pretalk",[]],
  
[anyone|plyr,"member_castellan_talk", [], "[Leave]", "close_window",[(call_script,"script_stand_back"),]],


# [anyone,"start", [(troop_slot_eq,"$g_talk_troop", slot_troop_occupation, slto_player_companion),
                    # (neg|main_party_has_troop,"$g_talk_troop"),
                    # (eq, "$talk_context", tc_party_encounter)],
# "Do you want me to rejoin you?", "member_wilderness_talk",[]],
# [anyone,"start", [(neg|main_party_has_troop,"$g_talk_troop"),(eq, "$g_encountered_party", "p_four_ways_inn")], "Do you want me to rejoin you?", "member_inn_talk",[]],
#[anyone,"member_separate_inn", [], "I don't know what you will do without me, but you are the boss. I'll wait for you at the Four Ways inn.", "close_window",
#[anyone,"member_separate_inn", [], "All right then. I'll meet you at the four ways inn. Good luck.", "close_window",
#   [(remove_member_from_party,"$g_talk_troop", "p_main_party"),(add_troop_to_site, "$g_talk_troop", "scn_four_ways_inn", borcha_inn_entry)]],

#Quest heroes member chats

  # [trp_kidnapped_girl,"member_chat", [], "Are we home yet?", "kidnapped_girl_chat_1",[]],
  # [trp_kidnapped_girl|plyr,"kidnapped_girl_chat_1", [], "Not yet.", "kidnapped_girl_chat_2",[]],
  # [trp_kidnapped_girl,"kidnapped_girl_chat_2", [], "I can't wait to get back. I've missed my family so much, I'd give anything to see them again.", "close_window",[]],

[anyone,"member_chat_00",[
    (check_quest_active, "qst_escort_messenger"),
    (this_or_next|eq, "$g_talk_troop", "trp_messenger_dwarf"),
    (this_or_next|eq, "$g_talk_troop", "trp_messenger_elf"),
    (this_or_next|eq, "$g_talk_troop", "trp_messenger_man"),
    (eq, "$g_talk_troop", "trp_messenger_orc")],
"{playername}, when do you think we can reach our destination?", "member_lady_1",[]],
[anyone|plyr, "member_lady_1", [],  "We still have a long way ahead of us.", "close_window", [(call_script,"script_stand_back"),]],
[anyone|plyr, "member_lady_1", [],  "Very soon. We're almost there.", "close_window", [(call_script,"script_stand_back"),]],

[anyone,"member_chat_00", [
    (check_quest_active, "qst_dispatch_scouts"),
    (quest_slot_eq, "qst_dispatch_scouts", slot_quest_object_troop, "$g_talk_troop"),
    # count if enough troops
    (quest_get_slot, ":quest_object_faction", "qst_dispatch_scouts", slot_quest_object_faction),
	(party_get_num_companion_stacks,":stacks","p_main_party"),
    (assign,":total_troops", 0),
	(try_for_range,":stack",0,":stacks"), # count troops of suitable quest faction, not including heroes
	   (party_stack_get_troop_id,":troop","p_main_party",":stack"),
       (neg|troop_is_hero,":troop"),
	   (store_troop_faction,":troop_faction",":troop"),
	   (eq, ":troop_faction",":quest_object_faction"),
	      (party_stack_get_size,":n","p_main_party",":stack"),
		  (val_add,":total_troops",":n"),
    (try_end),
	(ge, ":total_troops", 7),	  
#    (faction_get_slot, ":tier_1_troop", ":quest_object_faction", slot_faction_tier_1_troop), #4 of these
#    (party_count_companions_of_type, ":num_tier_1", "p_main_party", ":tier_1_troop"),
#    (ge, ":num_tier_1", 4),
#    (faction_get_slot, ":tier_2_troop", ":quest_object_faction", slot_faction_tier_2_troop), #2 of these
#    (party_count_companions_of_type, ":num_tier_2", "p_main_party", ":tier_2_troop"),
#    (ge, ":num_tier_2", 2),
    # see if close enough
    (quest_get_slot, ":quest_target_center", "qst_dispatch_scouts", slot_quest_target_center),
    (store_distance_to_party_from_party, ":dist", ":quest_target_center", "p_main_party"),
    (lt, ":dist", 7)],
"We are ready to go on our scouting mission. Should we go now?", "member_scout_1",[]],

[anyone|plyr, "member_scout_1", [],  "Yes, you've got your orders. Goodbye.", "close_window", [
	(call_script,"script_stand_back"),
    #remove troops from our party
    (quest_get_slot, ":quest_object_faction", "qst_dispatch_scouts", slot_quest_object_faction),
#    (faction_get_slot, ":tier_1_troop", ":quest_object_faction", slot_faction_tier_1_troop), #4 of these
#    (party_remove_members, "p_main_party", ":tier_1_troop", 4),
#    (faction_get_slot, ":tier_2_troop", ":quest_object_faction", slot_faction_tier_2_troop), #2 of these
#    (party_remove_members, "p_main_party", ":tier_2_troop", 2),
    (faction_get_slot, ":tier_3_troop", ":quest_object_faction", slot_faction_tier_3_troop), #1 of these, and used for member chat
    (party_remove_members, "p_main_party", ":tier_3_troop", 1),
    #create a real scouting party with 1 tier3 troop and 6 troops of minimal available level
    (quest_get_slot, ":quest_target_party_template", "qst_dispatch_scouts", slot_quest_target_party_template),
    (set_spawn_radius, 1),
    (spawn_around_party, "p_main_party", ":quest_target_party_template"),
    (assign, ":scout_party", reg0),
    (party_clear, ":scout_party"),
    (party_add_members, ":scout_party", ":tier_3_troop", 1),
#    (party_add_members, ":scout_party", ":tier_2_troop", 2),
#    (party_add_members, ":scout_party", ":tier_1_troop", 4),
    (party_set_slot, ":scout_party", slot_party_type, spt_scout),
    (faction_get_slot, ":capital", ":quest_object_faction", slot_faction_capital),
    (party_set_slot, ":scout_party", slot_party_home_center, ":capital"), #er... something
    (party_set_slot, ":scout_party", slot_party_victory_value, ws_scout_vp), # victory points for party kill
    (party_set_faction, ":scout_party", ":quest_object_faction"),
    (quest_get_slot, ":quest_target_center", "qst_dispatch_scouts", slot_quest_target_center),
    (party_set_slot, ":scout_party", slot_party_ai_object, ":quest_target_center"),
    (party_set_slot, ":scout_party", slot_party_ai_state, spai_undefined),
    (party_set_ai_behavior, ":scout_party", ai_bhvr_patrol_location),
    (party_set_ai_patrol_radius, ":scout_party", 30),
	(assign,":scouts2fill", 6),  # pick 6 troops for scout party, starting from lowest level
	(try_for_range,":unused",0,6),
      (gt,":scouts2fill", 0),
      (assign,":minlevel", 100),
      (assign,":mintroop", "trp_no_troop"),
      (party_get_num_companion_stacks,":stacks","p_main_party"),
	  (try_for_range,":stack",0,":stacks"), # find min level and troop
	     (party_stack_get_troop_id,":troop","p_main_party",":stack"),
         (neg|troop_is_hero,":troop"),
	     (store_troop_faction,":troop_faction",":troop"),
	     (eq, ":troop_faction",":quest_object_faction"),
	        (store_character_level,":level",":troop"),
		    (try_begin),
		      (lt,":level",":minlevel"),
			    (assign,":minlevel",":level"), #remember new minimal level troop 
			    (assign,":mintroop",":troop"),
		    (try_end),
	  (try_end),
	  (try_begin), # extracting troops into scout party
	    (neq,":mintroop","trp_no_troop"), # if suitable troops exist
        (party_count_companions_of_type, ":n", "p_main_party", ":mintroop"),
        (try_begin),
          (ge, ":n", ":scouts2fill"), # enough troops here, end iterations
            (assign,":unused",5),
		    (assign,":n",":scouts2fill"),
        (try_end),
        (party_remove_members, "p_main_party", ":mintroop", ":n"),
        (party_add_members, ":scout_party", ":mintroop", ":n"),
        (val_sub,":scouts2fill",":n"),
	  (else_try), (display_message,"@Something wrong, not enought troops for scout party"),
	  (try_end),
    (try_end),
    (call_script, "script_succeed_quest", "qst_dispatch_scouts")]],

[anyone|plyr, "member_scout_1", [],  "Wait a minute, not just yet.", "close_window", [(call_script,"script_stand_back"),]],
[anyone,"do_member_trade", [], "Anything else?", "member_talk",[]],

[anyone,"member_chat_00", [(store_conversation_troop,"$g_talk_troop"),
                          (troop_is_hero,"$g_talk_troop"),
                          (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
                          (str_store_string, s5, ":honorific")],
"Yes, {s5}?", "member_talk",[]],

[anyone|plyr,"member_talk", [(call_script, "script_unequip_items", "$g_talk_troop")],"Let me see your equipment.", "member_trade",[]],
[anyone,"member_trade",[			(store_character_level, ":talk_troop_level", "$g_talk_troop"),
						(ge, ":talk_troop_level", 40),
                        			(store_character_level, ":player_level", "trp_player"),
                        			(val_add, ":player_level", 10),
						(ge, ":talk_troop_level", ":player_level"), # if player level + 10 > npc level (e.g. 46 for Glorfindel), skip this
                        ],
"I'm sorry, my equipment is my own.", "do_member_trade",[]], #Glorfindel and others being pricks
[anyone,"member_trade", [], "Very well, it's all here...", "do_member_trade",[(change_screen_equip_other)]],

#[anyone,"do_member_trade", [], "Anything else?", "member_talk",[]],

[anyone|plyr,"member_talk", [], "What can you tell me about your skills?", "view_member_char_requested",[]],
[anyone,"view_member_char_requested", [], "All right, let me tell you...", "do_member_view_char",[(change_screen_view_character)]],

[anyone|plyr,"member_talk", [], "We need to separate for a while.", "member_separate",[
            # (call_script, "script_npc_morale", "$g_talk_troop"),
            # (assign, "$npc_quit_morale", reg0),
      ]],

# (CppCoder): TODO: Fix companions going back to ruins if there hometown is destroyed.
[anyone,"member_separate", [#            (gt, "$npc_quit_morale", 30),
        (troop_get_slot, ":home_center", "$g_talk_troop", slot_troop_cur_center),
        (try_begin),
          (gt, ":home_center", 0),
          (str_store_party_name, s4, ":home_center"),
        (else_try),
          (str_store_string, s4, "@my home town"),
        (try_end)],
"Oh really? Well, I'm not just going to wait around here. I'm going to go back to {s4}. Is that what you want?", "member_separate_confirm",[]],
[anyone|plyr,"member_separate_confirm", [], "That's right. We need to part ways.", "member_separate_yes",[]],
[anyone|plyr,"member_separate_confirm", [], "No, I'd rather have you at my side.", "do_member_trade",[]],

[anyone,"member_separate_yes", [], "Well. I'll be off, then. Look me up if you need me.", "close_window",[
		(call_script,"script_stand_back"),
		(troop_set_slot, "$g_talk_troop", slot_troop_occupation, 0),
        (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_dismissed),
        (remove_member_from_party, "$g_talk_troop")]],

[anyone|plyr,"member_talk", [], "I'd like to ask you something.", "member_question",[]],
[anyone|plyr,"member_talk", [], "Never mind.", "close_window",[(call_script,"script_stand_back"),]],
[anyone,"member_question", [], "Very well. What did you want to ask?", "member_question_2",[]],

#MV: disabled - useless info, companions don't leave if their morale drops
[anyone|plyr,"member_question_2", [(eq,1,0)], "How do you feel about the way things are going in this company?", "member_morale",[]],
[anyone|plyr,"member_question_2", [], "How is your health?", "member_health",[]],
[anyone|plyr,"member_question_2", [], "Tell me your story again.", "member_background_recap",[]],

[anyone,"member_morale", [(call_script, "script_npc_morale", "$g_talk_troop"),], "{s21}", "do_member_trade",[]],

[anyone,"member_background_recap", [
          (troop_get_slot, ":first_met", "$g_talk_troop", slot_troop_first_encountered),
          (str_store_party_name, 20, ":first_met"),
          #(troop_get_slot, ":home", "$g_talk_troop", slot_troop_home),
          #(str_store_party_name, 21, ":home"),
          (troop_get_slot, ":recap", "$g_talk_troop", slot_troop_home_recap),
          (str_store_string, 5, ":recap")],
"{s5}", "member_background_recap_2",[]],

[anyone,"member_background_recap_2", [
          (str_clear, 19),
          (troop_get_slot, ":background", "$g_talk_troop", slot_troop_backstory_b),
          (str_store_string, 5, ":background")],
"{s5}", "member_background_recap_3",[]],

[anyone,"member_background_recap_3", [], "Then shortly after, I joined up with you.", "do_member_trade",[]],
[anyone,"do_member_view_char", [], "Anything else?", "member_talk",[]],

# ORIGINAL MEMBER HEALTH
#[anyone,"member_health", [
#	(troop_get_slot, ":wound_mask", "$g_talk_troop", slot_troop_wound_mask),
#	(try_begin),
#		(neq, ":wound_mask", 0),
#		(str_store_string, s12, "@I'm seriously injured. I need healing."),
#	(else_try),
#		(str_store_string, s12, "@I don't have serious injuries, thank you."),
#	(try_end)],
#"{s12}", "do_member_trade",[]],

# NEW MEMBER HEALTH
[anyone,"member_health", [
	(troop_get_slot, ":wound_mask", "$g_talk_troop", slot_troop_wound_mask),
	(try_begin),
		(neq, ":wound_mask", 0),
		(assign, ":str_reg", s1), 
		(assign, ":wounds", 0), 
		(try_begin),(store_and,":x",":wound_mask",wound_head ),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_head"),(val_add, ":str_reg", 1),(try_end),
		(try_begin),(store_and,":x",":wound_mask",wound_chest),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_chest"),(val_add, ":str_reg", 1),(try_end),
		(try_begin),(store_and,":x",":wound_mask",wound_arm  ),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_arm"),(val_add, ":str_reg", 1),(try_end),
		(try_begin),(store_and,":x",":wound_mask",wound_leg  ),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_leg"),(val_add, ":str_reg", 1),(try_end),
		(str_store_string, s12, "@I am in perfect health."),
        	(try_begin),
			(eq, ":wounds", 1),
			(str_store_string, s12, "@I am suffering from {s1}."),
		(else_try),
			(eq, ":wounds", 2),
			(str_store_string, s12, "@I am suffering from {s1} and {s2}."),
		(else_try),
			(eq, ":wounds", 3),
			(str_store_string, s12, "@I am suffering from {s1}, {s2}, and {s3}."),
		(else_try),
			(eq, ":wounds", 4),
			(str_store_string, s12, "@I am suffering from {s1}, {s2}, {s3} and {s4}."),
		(else_try),
			(str_store_string, s12, "@I am in perfect health."),
		(try_end),
	(else_try),
		(str_store_string, s12, "@I don't have any serious injuries, thank you."),
	(try_end)],
"{s12}", "do_member_trade",[]],

[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (this_or_next|eq, "$talk_context", tc_court_talk), #TLD
                     (this_or_next|eq, "$talk_context", tc_town_talk), #TLD
                     (eq, "$talk_context", tc_tavern_talk),
                     (main_party_has_troop, "$g_talk_troop")],
"Let's leave whenever you are ready.", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_turned_down_twice, 1)],
"Please do not waste any more of my time today. Perhaps we shall meet again.", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (eq, "$g_talk_troop_met", 0),
                     (troop_get_slot, ":intro", "$g_talk_troop", slot_troop_intro),
                     (str_store_string, 5, ":intro"),
                     (str_store_party_name, 20, "$g_encountered_party")],
"{s5}", "companion_recruit_intro_response", [(troop_set_slot, "$g_talk_troop", slot_troop_first_encountered, "$g_encountered_party"),]],


[anyone|plyr, "companion_recruit_intro_response", [
                     (troop_get_slot, ":intro_response", "$g_talk_troop", slot_troop_intro_response_1),
                     (str_store_string, 6, ":intro_response")], 
"{s6}", "companion_recruit_backstory_a", []],

[anyone|plyr, "companion_recruit_intro_response", [
                     (troop_get_slot, ":intro_response", "$g_talk_troop", slot_troop_intro_response_2),
                     (str_store_string, 7, ":intro_response")],
"{s7}", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "companion_recruit_backstory_a", [(troop_get_slot, ":backstory_a", "$g_talk_troop", slot_troop_backstory_a),
                     (str_store_string, 5, ":backstory_a"),
                     (str_store_string, 19, "str_here_plus_space"),
                     (str_store_party_name, 20, "$g_encountered_party")],
"{s5}", "companion_recruit_backstory_b", []],

[anyone, "companion_recruit_backstory_b", [(troop_get_slot, ":backstory_b", "$g_talk_troop", slot_troop_backstory_b),
                     (str_store_string, 5, ":backstory_b"),
                     (str_store_party_name, 20, "$g_encountered_party")],
"{s5}", "companion_recruit_backstory_c", []],

[anyone, "companion_recruit_backstory_c", [(troop_get_slot, ":backstory_c", "$g_talk_troop", slot_troop_backstory_c),
                     (str_store_string, 5, ":backstory_c")],
"{s5}", "companion_recruit_backstory_response", []],

[anyone|plyr, "companion_recruit_backstory_response", [
                     (troop_get_slot, ":backstory_response", "$g_talk_troop", slot_troop_backstory_response_1),
                     (str_store_string, 6, ":backstory_response")],
"{s6}", "companion_recruit_signup", []],

[anyone|plyr, "companion_recruit_backstory_response", [
                     (troop_get_slot, ":backstory_response", "$g_talk_troop", slot_troop_backstory_response_2),
                     (str_store_string, 7, ":backstory_response")],
"{s7}", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "companion_recruit_signup", [(troop_get_slot, ":signup", "$g_talk_troop", slot_troop_signup),
                     (str_store_string, 5, ":signup"),
                     (str_store_party_name, 20, "$g_encountered_party")],
"{s5}", "companion_recruit_signup_b", []],

[anyone, "companion_recruit_signup_b", [
      (troop_get_slot, ":signup", "$g_talk_troop", slot_troop_signup_2),
      (troop_get_slot, reg3, "$g_talk_troop", slot_troop_payment_request),#
      (str_store_string, 5, ":signup"),
      (str_store_party_name, 20, "$g_encountered_party")],
"{s5}", "companion_recruit_signup_response", []],

[anyone|plyr, "companion_recruit_signup_response", [(neg|hero_can_join, "p_main_party")],
"Unfortunately, I can't take on any more hands in my party right now.", "close_window", [(call_script,"script_stand_back"),]],

[anyone|plyr, "companion_recruit_signup_response",[
                    (hero_can_join, "p_main_party"),
                    (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_1),
                    (str_store_string, 6, ":signup_response")],
"{s6}", "companion_recruit_rank", []],

[anyone|plyr, "companion_recruit_signup_response",[
                    (hero_can_join, "p_main_party"),
                     (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
                     (str_store_string, 7, ":signup_response")],
"{s7}", "close_window", [(call_script,"script_stand_back"),]],

# rank 0 needed - don't mention it at all
[anyone|auto_proceed, "companion_recruit_rank", [
      (troop_slot_eq, "$g_talk_troop", slot_troop_rank_request, 0)],
".", "companion_recruit_payment", []],
   
# rank not ok
[anyone, "companion_recruit_rank", [ 
      (troop_get_slot, ":rank_needed", "$g_talk_troop", slot_troop_rank_request),
      (call_script, "script_get_rank_points_for_rank", ":rank_needed"), #convert to rank points
      (assign, ":rank_points_needed", reg0),
      (faction_get_slot, ":rank_points_held", "$g_talk_troop_faction", slot_faction_rank),
      (call_script, "script_get_rank_title_to_s24", "$g_talk_troop_faction"), (str_store_string_reg, s29, s24), #to s29
      # determine needed rank title
      (call_script, "script_get_any_rank_title_to_s24", "$g_talk_troop_faction", ":rank_needed"), #to s24
      (store_sub, reg3, ":rank_points_needed", ":rank_points_held"), # reg3: how many more rank points are needed to recruit
      (gt, reg3, 0)], # not enough?
"It seems that you are not esteemed enough by my people, {playername}. \
You are a {s29} and you need to be a {s24} for me to join [{reg3} more rank points needed].^\
Let's speak again when you are more accomplished.", "close_window", [(call_script,"script_stand_back"),]],

# rank ok
[anyone, "companion_recruit_rank", [],"I'm glad to see you have become {s29}, and I'm looking forward to joining you.", "companion_recruit_payment", []],
   
[anyone|auto_proceed, "companion_recruit_payment", [
      (troop_slot_eq, "$g_talk_troop", slot_troop_payment_request, 0)],
".", "companion_recruit_signup_confirm", []],
  
[anyone, "companion_recruit_payment", [
      (store_sub, ":npc_offset", "$g_talk_troop", "trp_npc1"),
      (store_add, ":dialog_line", "str_npc1_payment", ":npc_offset"),
      (troop_get_slot, reg14, "$g_talk_troop", slot_troop_payment_request),
      (store_troop_faction, ":faction", "$g_talk_troop"),
      (str_store_faction_name, s14, ":faction"),
      (str_store_string, s5, ":dialog_line")],
"{s5}", "companion_recruit_payment_response", []],

[anyone|plyr, "companion_recruit_payment_response", [
                    (hero_can_join, "p_main_party"),
					(store_troop_faction, ":fac", "$g_talk_troop"),
                    (faction_get_slot, ":inf", ":fac", slot_faction_influence),#
                    (troop_get_slot, ":amount_requested", "$g_talk_troop", slot_troop_payment_request),#
                    (ge, ":inf", ":amount_requested"),#
                    (assign, reg14, ":amount_requested"),
					(assign, reg15, ":inf"),
                    (store_sub, ":npc_offset", "$g_talk_troop", "trp_npc1"),
                    (store_add, ":dialog_line", "str_npc1_payment_response", ":npc_offset"),
                    (str_store_string, s6, ":dialog_line")],
"{s6}", "companion_recruit_signup_confirm", [
                    (troop_get_slot, ":amount_requested", "$g_talk_troop", slot_troop_payment_request),#
                    (gt, ":amount_requested", 0),
					(call_script, "script_spend_influence_of", ":amount_requested", "$g_talk_troop_faction"),
                    (troop_set_slot, "$g_talk_troop", slot_troop_payment_request, 0)]],

[anyone|plyr, "companion_recruit_payment_response", [
                     (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
                     (str_store_string, s7, ":signup_response")],
"Well, there's little I can do then.", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 1),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, 0)],
"We meet again.", "companion_recruit_meet_again", [(troop_set_slot, "$g_talk_troop", slot_troop_turned_down_twice, 1)]],

[anyone|plyr, "companion_recruit_meet_again", [], "So... What have you been doing since our last encounter?", "companion_recruit_backstory_delayed", []],
[anyone|plyr, "companion_recruit_meet_again", [
   (try_begin),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
     (str_store_string, s4, "@Good day to you."),
   (else_try),
     (str_store_string, s4, "@Ah, it's you again. Goodbye."),
   (try_end)],
"{s4}", "close_window", [(call_script,"script_stand_back"),]],


[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, 0)],
"Yes?", "companion_recruit_secondchance", [(troop_set_slot, "$g_talk_troop", slot_troop_turned_down_twice, 1)]],

[anyone|plyr, "companion_recruit_secondchance", [
   (try_begin),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
     (str_store_string, s4, "@My apologies if I was rude, earlier. What was your story again?"),
   (else_try),
     (str_store_string, s4, "@I was reconsidering our last conversation. What was your story again?"),
   (try_end)],
"{s4}", "companion_recruit_backstory_b", []],
[anyone|plyr, "companion_recruit_secondchance", [],  "Never mind.", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "companion_recruit_backstory_delayed",
   [(troop_get_slot, ":backstory_delayed", "$g_talk_troop", slot_troop_backstory_delayed),
     (str_store_string, 5, ":backstory_delayed")],
"{s5}", "companion_recruit_backstory_delayed_response", []],

[anyone|plyr, "companion_recruit_backstory_delayed_response", [], "I might be able to use you in my company.", "companion_recruit_signup_b", []],
[anyone|plyr, "companion_recruit_backstory_delayed_response", [], "Never mind, another time perhaps.", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "companion_recruit_signup_confirm", [], "Good! Give me a few moments to prepare and I'll be ready to move.", "close_window",
   [(call_script,"script_stand_back"),
   (call_script, "script_recruit_troop_as_companion", "$g_talk_troop")]],



### Rehire dialogues
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate)],
"My offer to rejoin you still stands, if you'll have me.", "companion_rehire", []],

### If the companion and the player were separated in battle
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_scattered),
                     (assign, ":battle_fate", "str_battle_fate_1"),
                     (store_random_in_range, ":fate_roll", 0, 5),
                     (val_add, ":battle_fate", ":fate_roll"),
                     (str_store_string, 6, ":battle_fate"),
                     (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
                     (str_store_string, 5, ":honorific")],
"It is good to see you alive, {s5}! {s6}, and I did not know whether you had been captured, or slain, or got away. I've been waiting here since then, looking for news of your fate. Shall I get my gear together and rejoin your company?",
   "companion_rehire", [(troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),]],

### If the player and the companion parted on bad terms
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_turned_down_twice, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_quit),
                     (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_rehire_speech),
                     (str_store_string, 5, ":speech")],
"{s5}", "companion_rehire", [(troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate)]],

###If the player and the companion parted on good terms
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     #(troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_dismissed),
                     (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
                     (str_store_string, 21, ":honorific"),
                     (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_backstory_delayed),
                     (str_store_string, 5, ":speech")],
"It is good to see you, {s21}! To tell you the truth, I had hoped to run into you.", "companion_was_dismissed", [
	(troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate)]],

[anyone, "companion_was_dismissed", [
                      (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_backstory_delayed),
                     (str_store_string, 5, ":speech")],
"{s5}. Would you want me to rejoin your company?", "companion_rehire", []],

[anyone|plyr, "companion_rehire", [(hero_can_join, "p_main_party")], "Welcome back, my friend!", "companion_recruit_signup_confirm", []],
[anyone|plyr, "companion_rehire", [],  "Sorry, I can't take on anyone else right now.", "companion_rehire_refused", []],
[anyone, "companion_rehire_refused", [], "Well... Look me up if you change your mind, eh?", "close_window", [(call_script,"script_stand_back"),]],

#[anyone, "event_triggered",
#   [ (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "$g_talk_troop"),
#     (ge, "$g_center_taken_by_player_faction", 0),
#     (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
#    ], "{s1} is not being managed by anyone. Whom shall I put in charge?", "center_captured_lord_advice", []],
#
#[anyone|plyr|repeat_for_troops, "center_captured_lord_advice",
#   [ (store_repeat_object, ":troop_no"),
#     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
#     (neq, "$g_talk_troop", ":troop_no"),
#     (neq, "trp_player", ":troop_no"),
#     (store_troop_faction, ":faction_no", ":troop_no"),
#     (eq, ":faction_no", "fac_player_supporters_faction"),
#     (str_store_troop_name, s11, ":troop_no"),
#     (call_script, "script_print_troop_owned_centers_in_numbers_to_s0", ":troop_no"),
#     (try_begin),
#       (eq, reg0, 0),
#       (str_store_string, s1, "@(no fiefs)"),
#     (else_try),
#       (str_store_string, s1, "@(fiefs: {s0})"),
#     (try_end),
#     ],
#   "{s11}. {s1}", "center_captured_lord_advice_2",
#   [ (store_repeat_object, "$temp")]],
#
#[anyone|plyr, "center_captured_lord_advice",
#   [ (call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "trp_player"),
#     (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
#    ],
#   "Please {s65}, I want to have {s1} for myself. (fiefs: {s0})", "center_captured_lord_advice_2",
#   [ (assign, "$temp", "trp_player")]],
#
#[anyone|plyr, "center_captured_lord_advice",
#   [
#     (call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "$g_talk_troop"),
#     (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
#     ],
#   "{s66}, you should have {s1} for yourself. (fiefs: {s0})", "center_captured_lord_advice_2",
#   [(assign, "$temp", "$g_talk_troop")]],

#[anyone, "center_captured_lord_advice_2",
#   [# (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "$g_talk_troop"),
#     (ge, "$g_center_taken_by_player_faction", 0),
#     ],
#   "Hmmm. All right, {playername}. I value your counsel highly. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}.", "close_window",
#   [ (assign, ":new_owner", "$temp"),
#     (call_script, "script_calculate_troop_score_for_center", ":new_owner", "$g_center_taken_by_player_faction"),
#     (assign, ":new_owner_score", reg0),
#     (assign, ":total_negative_effect"),
#     (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
#       (store_troop_faction, ":cur_faction", ":cur_troop"),
#       (eq, ":cur_faction", "fac_player_supporters_faction"),
#       (neq, ":cur_troop", ":new_owner"),
#       (call_script, "script_calculate_troop_score_for_center", ":cur_troop", "$g_center_taken_by_player_faction"),
#       (assign, ":cur_troop_score", reg0),
#       (gt, ":cur_troop_score", ":new_owner_score"),
#       (store_sub, ":difference", ":cur_troop_score", ":new_owner_score"),
#       (store_random_in_range, ":random_dif", 0, ":difference"),
#       (val_div, ":random_dif", 1000),
#       (gt, ":random_dif", 0),
       # (val_add, ":total_negative_effect", ":random_dif"),
       # (val_mul, ":random_dif", -1),
       # (call_script, "script_change_player_relation_with_troop", ":cur_troop", ":random_dif"),
     # (try_end),
     # (val_mul, ":total_negative_effect", 2),
     # (val_div, ":total_negative_effect", 3),
     # (val_add, ":total_negative_effect", 5),
     # (try_begin),
       # (neq, ":new_owner", "trp_player"),
       # (val_min, ":total_negative_effect", 30),
       # (call_script, "script_change_player_relation_with_troop", ":new_owner", ":total_negative_effect"),
     # (try_end),
     # (call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", ":new_owner", 0),
     # (try_begin),
       # (neq, ":new_owner", "trp_player"),
       # (call_script, "script_cf_reinforce_party", "$g_center_taken_by_player_faction"),
       # (call_script, "script_cf_reinforce_party", "$g_center_taken_by_player_faction"),
     # (try_end),

     # (assign, reg6, 0),
     # (assign, reg7, 0),
     # (try_begin),
       # (eq, "$temp", "$g_talk_troop"),
       # (assign, reg6, 1),
     # (else_try),
       # (eq, "$temp", "trp_player"),
       # (assign, reg7, 1),
     # (else_try),
       # (str_store_troop_name, s11, "$temp"),
     # (try_end),
     # (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
     # (troop_get_type, reg3, "$temp"),
     # (assign, "$g_center_taken_by_player_faction", -1),
     # ]],
#Morality objections
[anyone, "event_triggered", [
                     (store_conversation_troop, "$map_talk_troop"),
                     (eq, "$map_talk_troop", "$npc_with_grievance"), 
                     (eq, "$npc_map_talk_context", slot_troop_morality_state), 
                     (try_begin),
                         (eq, "$npc_grievance_slot", slot_troop_morality_state),
                         (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_morality_speech),
                     (else_try),
                         (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_2ary_morality_speech),
                     (try_end),
                     (str_store_string, 21, "$npc_grievance_string"),
                     (str_store_string, 5, ":speech")],
"{s5}", "companion_objection_response", [(assign, "$npc_with_grievance", 0)]],

[anyone|plyr, "companion_objection_response", [(eq, "$npc_praise_not_complaint", 1)],
"Thank you, I appreciate your support.", "close_window", [(troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_acknowledged),(call_script,"script_stand_back"),]],

[anyone|plyr, "companion_objection_response", [(eq, "$npc_praise_not_complaint", 0)],
"Hopefully it won't happen again.", "close_window", [(troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_acknowledged),(call_script,"script_stand_back"),]],

[anyone|plyr, "companion_objection_response", [(eq, "$npc_praise_not_complaint", 0)],
"Your objection is noted, but I have more important things on my mind.", "close_window", [
					(call_script,"script_stand_back"),
                    (troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_dismissed),
                    (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_morality_penalties),
                    (val_add, ":grievance", 10),
                    (troop_set_slot, "$map_talk_troop", slot_troop_morality_penalties, ":grievance")]],

##[anyone|plyr, "companion_objection_response", [
##      ],  "I prefer my followers to keep their opinions to themselves.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", "$npc_grievance_slot", tms_dismissed),
##                    (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_morality_penalties),
##                    (val_add, ":grievance", 10),
##                    (troop_set_slot, "$map_talk_troop", slot_troop_morality_penalties, ":grievance"),
##                    (assign, "$disable_npc_complaints", 1),
##          ]],

# Personality clash 2 objections
[anyone, "event_triggered", [
                     (store_conversation_troop, "$map_talk_troop"),
                     (eq, "$map_talk_troop", "$npc_with_personality_clash_2"), 
                     (eq, "$npc_map_talk_context", slot_troop_personalityclash2_state), 

                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalityclash2_speech),
                     (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
                     (str_store_troop_name, 11, ":object"),
                     (str_store_string, 5, ":speech")],
"{s5}", "companion_personalityclash2_b", [
                    (assign, "$npc_with_personality_clash_2", 0),
                    (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_personalityclash_penalties),
                    (val_add, ":grievance", 5),
                    (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_penalties, ":grievance")]],

[anyone, "companion_personalityclash2_b", [],
"{s5}", "companion_personalityclash2_response", [
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalityclash2_speech_b),
                     (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
                     (str_store_troop_name, 11, ":object"),
                     (str_store_string, 5, ":speech")]],

[anyone|plyr, "companion_personalityclash2_response", [
      (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
      (str_store_troop_name, s11, ":object"),
      (troop_get_type, reg11, ":object"),
      (try_begin),
        (gt, reg11, 1), #MV: non-humans are male
        (assign, reg11, 0),
      (try_end)],
"I deem {s11} a valuable member of this company. You should appreciate {reg11?her:him} more.", "close_window", [
                    (call_script,"script_stand_back"),
					(troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, pclash_penalty_to_self)]],

[anyone|plyr, "companion_personalityclash2_response", [
      (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
      (str_store_troop_name, s11, ":object"),
      (troop_get_type, reg11, ":object"),
      (try_begin),
        (gt, reg11, 1), #MV: non-humans are male
        (assign, reg11, 0),
      (try_end)],
"You are right. I'm not happy with {s11}'s behavior myself and will let {reg11?her:him} know that.", "close_window", [
                    (call_script,"script_stand_back"),
					(troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, pclash_penalty_to_other)]],
  
[anyone|plyr, "companion_personalityclash2_response", [],
"I don't have time for petty squabbles.", "close_window", [
					(call_script,"script_stand_back"),
					(troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, pclash_penalty_to_both)]],

##[anyone|plyr, "companion_personalityclash2_response", [
##      ],  "Your grievance is noted. Now fall back in line.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, 1),
##          ]],

##[anyone|plyr, "companion_personalityclash2_response", [
##      ],  "I prefer my followers to keep their opinions to themselves.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, 1),
##                    (assign, "$disable_npc_complaints", 1),
##          ]],

# Personality clash objections

[anyone, "event_triggered", [
                     (store_conversation_troop, "$map_talk_troop"),
                     (eq, "$map_talk_troop", "$npc_with_personality_clash"),
                     (eq, "$npc_map_talk_context", slot_troop_personalityclash_state), 
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalityclash_speech),
                     (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
                     (str_store_troop_name, 11, ":object"),
                     (str_store_string, 5, ":speech")],
"{s5}", "companion_personalityclash_b", [
                    (assign, "$npc_with_personality_clash", 0),
                    (troop_get_slot, ":grievance", "$map_talk_troop", slot_troop_personalityclash_penalties),
                    (val_add, ":grievance", 5),
                    (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_penalties, ":grievance")]],

[anyone, "companion_personalityclash_b", [],
"{s5}", "companion_personalityclash_response", [
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalityclash_speech_b),
                     (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
                     (str_store_troop_name, 11, ":object"),
                     (str_store_string, 5, ":speech")]],

[anyone|plyr, "companion_personalityclash_response", [
      (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
      (str_store_troop_name, s11, ":object"),
      (troop_get_type, reg11, ":object"),
      (try_begin),
        (gt, reg11, 1), #MV: non-humans are male
        (assign, reg11, 0),
      (try_end)],
"I deem {s11} a valuable member of this company. You should appreciate {reg11?her:him} more.", "close_window", [
                    (call_script,"script_stand_back"),
					(troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_state, pclash_penalty_to_self)]],

[anyone|plyr, "companion_personalityclash_response", [
      (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
      (str_store_troop_name, s11, ":object"),
      (troop_get_type, reg11, ":object"),
      (try_begin),
        (gt, reg11, 1), #MV: non-humans are male
        (assign, reg11, 0),
      (try_end)],
"You are right. I'm not happy with {s11}'s behavior myself and will let {reg11?her:him} know that.", "close_window", [
          (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_state, pclash_penalty_to_other)]],
  
[anyone|plyr, "companion_personalityclash_response", [],
"I don't have time for petty squabbles.", "close_window", [
		(call_script,"script_stand_back"),
		(troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_state, pclash_penalty_to_both)]],

##[anyone|plyr, "companion_personalityclash_response", [
##      ],  "Your grievance is noted. Now fall back in line.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_state, 1),
##          ]],

##[anyone|plyr, "companion_personalityclash_response", [
##      ],  "I prefer my followers to keep their opinions to themselves.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash_state, 1),
##                    (assign, "$disable_npc_complaints", 1),
##          ]],



# Personality match

[anyone, "event_triggered", [
                     (eq, "$npc_map_talk_context", slot_troop_personalitymatch_state), 
                     (store_conversation_troop, "$map_talk_troop"),
                     (eq, "$map_talk_troop", "$npc_with_personality_match"),

                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalitymatch_speech),
                     (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalitymatch_object),
                     (str_store_troop_name, 11, ":object"),
                     (str_store_string, 5, ":speech")],
   "{s5}", "companion_personalitymatch_b", [(assign, "$npc_with_personality_match", 0)]],

[anyone, "companion_personalitymatch_b", [
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_personalitymatch_speech_b),
                     (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalitymatch_object),
                     (str_store_troop_name, 11, ":object"),
                     (str_store_string, 5, ":speech")],
"{s5}", "companion_personalitymatch_response", []],


[anyone|plyr, "companion_personalitymatch_response", [],  "Very good.", "close_window", [
					(call_script,"script_stand_back"),
					(troop_set_slot, "$map_talk_troop", slot_troop_personalitymatch_state, 1)]],

##[anyone|plyr, "companion_personalitymatch_response", [
##      ],  "I prefer my followers to keep their opinions to themselves.", "close_window", [
##                    (troop_set_slot, "$map_talk_troop", slot_troop_personalitymatch_state, 1),
##                    (assign, "$disable_npc_complaints", 1),
##          ]],


#TLD: companions complain about their home faction getting demolished
[anyone, "event_triggered", [
                     (eq, "$npc_map_talk_context", slot_troop_last_complaint_hours), 
                     (store_conversation_troop, "$map_talk_troop"),
                     (troop_get_slot, ":honorific", "$map_talk_troop", slot_troop_honorific),
                     (str_store_string, s5, ":honorific"),
                     (store_troop_faction, ":npc_faction", "$map_talk_troop"),
                     (str_store_faction_name, s6, ":npc_faction"),
                     (assign, reg6, 0),
                     (try_begin),
                       (eq, "$players_kingdom", ":npc_faction"),
                       (assign, reg6, 1),
                     (try_end)],
"{s5}, {reg6?our:my} {s6} homeland is suffering grievously in the War, I ask you to consider helping {reg6?our:my} people as soon as we are rested and ready.", "companion_faction_demolished", []],

[anyone|plyr, "companion_faction_demolished", [],  "Then we shall ride to aid {s6} immediately.", "close_window", [(call_script,"script_stand_back"),]],
[anyone|plyr, "companion_faction_demolished", [],  "I'm sorry, but we are needed elsewhere.", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "event_triggered", [
                     (eq, "$npc_map_talk_context", slot_troop_home), 
                     (store_conversation_troop, "$map_talk_troop"),
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_intro),
                     (str_store_string, s5, ":speech")],
"{s5}", "companion_home_description", [(troop_set_slot, "$map_talk_troop", slot_troop_home_speech_delivered, 1)]],

[anyone|plyr, "companion_home_description", [],  "Tell me more.", "companion_home_description_2", []],
[anyone|plyr, "companion_home_description", [],  "We don't have time to chat just now.", "close_window", [(call_script,"script_stand_back"),]],
[anyone|plyr, "companion_home_description", [],  "I prefer my companions not to bother me with such trivialities.", "close_window", [
					(call_script,"script_stand_back"),
                    (assign, "$disable_local_histories", 1)]],

[anyone, "companion_home_description_2", [
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_description),
                     (str_store_string, 5, ":speech")],
"{s5}", "companion_home_description_3", []],

[anyone, "companion_home_description_3", [
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_description_2),
                     (str_store_string, 5, ":speech")],
"{s5}", "close_window", [(call_script,"script_stand_back"),]],


# TLD recruiting in city -- mtarini

[anyone,"start", 
   [    (eq, "$talk_context", tc_hire_troops), 
		# prepare strings useful in the folowing dialog
		(str_store_party_name, s21, "$g_encountered_party"), # s21: CITY NAME
		(str_store_faction_name, s22, "$g_encountered_party_faction"), # s22: faction name
		(str_store_faction_name, s14, "$g_encountered_party_faction"), # s14:  faction name
		(str_store_troop_name, s23, "$g_player_troop"), # s23: Player name
		(call_script, "script_get_rank_title_to_s24", "$players_kingdom" ),(str_store_string_reg, s29, s24), # s29: player TITLE  (among own faction)
		(call_script, "script_get_rank_title_to_s24", "$g_encountered_party_faction" ), # s24: player TITLE  (among city faction)
		(str_store_faction_name, s25, "$players_kingdom"), # s25: Player's faction name
		(assign, reg26, 0),(try_begin),(eq,"$players_kingdom","$g_encountered_party_faction"),(assign,reg26,1),(try_end), # reg26: 1 if city of player faction
		(party_get_num_companions, reg27, "p_main_party"), # reg27: initial party size

		# prepare greeting string
        (call_script, "script_get_faction_rank", "$g_encountered_party_faction"),
        (assign, ":rank", reg0),
		(try_begin),(eq, reg26, 1)  , (str_store_string, s33, "@Greetings, {s23}, {s24}."), # same faction (military salute?)
		(else_try),	(ge, ":rank", 4), (str_store_string, s33, "@Greetings, {s23}, {s24}."),  # player not same faction, but trusted
		(else_try),	(ge, ":rank", 1), (str_store_string, s33, "@Greetings, {s23}."), # player not much trusted
		(else_try),	(str_store_string, s33, "@So, you are {s23}. I hear you fight for our {s25} friends, so I guess I should consider you an ally."), # player unknown
		(try_end),

		# just to see if someone can be given away: backup party, then see if troops which can be given away 
		(call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
		(call_script, "script_party_split_by_faction", "p_main_party_backup", "p_temp_party", "$g_encountered_party_faction")],
"{s33}^^I am in charge of the forces garrisoned here at {s21}. Did you want to see me?", "player_hire_troop", []],

[anyone|plyr,"player_hire_troop", 
	[(party_get_free_companions_capacity,reg10,"p_main_party"), (gt,reg10,0),
     (try_begin),
       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
       (str_store_string, s4, "@I need volunteers willing to follow me on dangerous missions."),
     (else_try),
       (str_store_string, s4, "@I need some soldiers to replace my dead."),
     (try_end)], 
"{s4}", "player_hire_troop_take", [
		# prepare party to recruit  from
		(party_get_slot, "$hiring_from", "$current_town", slot_town_volunteer_pt ),
		(assign, "$num_hirable", 0),
		(try_begin),
			(gt, "$hiring_from", 0),
			(party_is_active, "$hiring_from"),
			(store_party_size, "$num_hirable" , "$hiring_from"),
			(set_mercenary_source_party,"$hiring_from"),
			(call_script, "script_get_party_min_join_cost", "$hiring_from"),
			(assign, "$cheapest_join", reg0),
		(try_end)]],

[anyone|plyr,"player_hire_troop", 
	[(party_get_num_companions,reg11,"p_main_party_backup"), (gt,reg11,1)], # player has someone to give away 
	"Some of the soldiers in my group would be more useful here, to defend {s21}.", "player_hire_troop_give", [
        #GA: changed into trade as a whole main party, then return given non-faction troops back to player
		(party_clear, "p_main_party_backup"),
		(assign, "$g_move_heroes", 0),
        (call_script, "script_party_add_party_companions", "p_main_party_backup", "p_main_party"), #keep this backup for later
		(party_get_num_companions, reg28, "p_main_party"), # reg28: initial party size
		(call_script, "script_get_party_disband_cost", "p_main_party",1),(assign, "$initial_party_value", reg0), # initial party total value
	]],

# Player reserves - no upkeep for now - exploitable!
[anyone|plyr,"player_hire_troop", 
	[ (faction_slot_eq, "$players_kingdom", slot_faction_capital, "$g_encountered_party"), # keep troops only at faction's capital
      # check if first time or depleted, and initialize
      (troop_get_slot, ":reserve_party", "trp_player", slot_troop_player_reserve_party),
	  (try_begin),
		(gt, ":reserve_party", 0),
		(neg|party_is_active, ":reserve_party"), # depleted
		(assign, ":reserve_party", 0),
	  (try_end),
      (try_begin),
		(eq, ":reserve_party", 0), #first time or depleted
        (spawn_around_party, "$g_encountered_party"),
        (assign, ":reserve_party", reg0),
        (party_add_members, ":reserve_party", "trp_looter", 1), #.. or change_screen_exchange_with_party will crash
        (party_remove_members, ":reserve_party", "trp_looter", 1),
        (troop_set_slot, "trp_player", slot_troop_player_reserve_party, ":reserve_party"),
        (party_attach_to_party, ":reserve_party", "$g_encountered_party"),
        (party_set_name, ":reserve_party", "@{playername}'s Reserves"),
        (party_set_flags, ":reserve_party", pf_no_label),
        (party_set_ai_behavior, ":reserve_party", ai_bhvr_hold),
      (try_end)], 
"I want to review my soldiers stationed here.", "close_window", [
		(call_script,"script_stand_back"),
      #(troop_get_slot, ":reserve_party", "trp_player", slot_troop_player_reserve_party),
      #(change_screen_exchange_with_party, ":reserve_party"), # doesn't work without changing context...
      (jump_to_menu, "mnu_auto_player_garrison"), #...therefore, hackery ensues
	]],

# Training
[anyone|plyr,"player_hire_troop",[ (neg|party_slot_eq, "$g_encountered_party", slot_town_arena, -1)], 
"I need some training.", "close_window", [(call_script,"script_stand_back"),(jump_to_menu, "mnu_auto_training_ground_trainer")]],

# Selling prisoners 
[anyone|plyr, "player_hire_troop", [(store_num_regular_prisoners,reg5),(ge,reg5,1)],
"I have brought you some prisoners.", "tld_sell_prisoners", []],
[anyone, "tld_sell_prisoners", [
  (try_begin),(ge, reg5,30),(str_store_string, s33, "@Excellent job, {s23}! I wish all our commanders were as dedicated as you.^"),
   (else_try),(ge, reg5,20),(str_store_string, s33, "@Nicely done, {s23}."),
   (else_try),(ge, reg5,10),(str_store_string, s33, "@Good work, {s23}."),
   (else_try),(ge, reg5, 5),(str_store_string, s33, "@The more you capture, the better, {s23}."),
   (else_try),              (str_store_string, s33, "@Caught a few stragglers, {s23}?"),
  (try_end)],
"{s33} Let's see the wretched scum.", "tld_sell_prisoners_check",[(change_screen_trade_prisoners)]],

# this one is needed because change_screen_trade_* needs another dialog to update the main party
[anyone, "tld_sell_prisoners_check", [], "Let me check our dungeon records...", "tld_sell_prisoners_2", []],

[anyone, "tld_sell_prisoners_2", [(store_num_regular_prisoners,reg6),(eq,reg5,reg6)],
"Changed your mind, eh?", "player_hire_troop_nextcycle", []],
[anyone, "tld_sell_prisoners_2", [], "I'll make sure they won't escape from our dungeons.", "player_hire_troop_nextcycle",[]],

[anyone|plyr,"player_hire_troop", [], "Farewell.", "close_window", [(call_script,"script_stand_back"),]],

# Hiring troops
[anyone,"player_hire_troop_take", 
  [(eq,"$num_hirable" ,0),
   (try_begin),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
     (str_store_string, s4, "@I am sorry, no one else is ready to go.^They will serve {s22} by holding the defences here."),
   (else_try),
     (str_store_string, s4, "@Tough luck, but we don't have any. Come back later."),
   (try_end)], # no one wants to join
"{s4}", "player_hire_troop_nextcycle", []],

[anyone,"player_hire_troop_take", 
  [(store_troop_gold, ":cur_gold", "$g_player_troop"), (gt,"$cheapest_join",":cur_gold"),
   (try_begin),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
     (str_store_string, s4, "@There are brave soldiers willing to risk their life, but in these dark times I cannot afford to let them leave the defences here.^"+not_enough_rp),
   (else_try),
     (str_store_string, s4, "@We have some spare troops, but we can't afford to lose them to the likes of you.^"+not_enough_rp),
   (try_end)], # these who want to join cost too much
"{s4}", "player_hire_troop_nextcycle", []],

[anyone,"player_hire_troop_take", 
	[(gt,"$num_hirable" ,0),   # there's someone to hire...
	 (store_troop_gold, ":cur_gold", "$g_player_troop"), (le,"$cheapest_join",":cur_gold"),
     (try_begin),
       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
       (str_store_string, s4, "@There are brave soldiers here volunteering for field duty.^^I think I can let a few of them go with you."),
     (else_try),
       (str_store_string, s4, "@There are spare troops here that wouldn't mind a little blood-letting.^^I can let a few of them go with you."),
     (try_end)], # and player can afford it
"{s4}", "player_hire_troop_pre_pre_nextcycle", [(change_screen_buy_mercenaries)]],

# Selling troops
[anyone,"player_hire_troop_give", 
	 [  (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@Strenghten defences in {s21}? This is surely welcome. Note that we can only accept our own people."),
        (else_try),
          (str_store_string, s4, "@Strenghten defences in {s21}? Well, as long as they are not crippled, why not. Just be sure you give away our own troops, for we have no use for outsiders here."),
        (try_end)],
"{s4}", "player_hire_troop_reunite", [(change_screen_give_members)]],

[anyone,"player_hire_troop_pre_pre_nextcycle", [], 
"Let me check the troop roster...", "player_hire_troop_pre_nextcycle", []],

[anyone,"player_hire_troop_pre_nextcycle", 
	 [ (party_get_num_companions, reg10, "p_main_party"), (eq, reg10, reg27),],
"So you've changed your mind...^I see.", "player_hire_troop_nextcycle", []],

[anyone,"player_hire_troop_pre_nextcycle", 
	 [  (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@Please return them in one piece. I personally know the valor of each one of them. And here we need every soul."),
        (else_try),
          (str_store_string, s4, "@Don't let them all die in one place. Except the cowards. Put those in your front ranks, you know the drill by now."),
        (try_end)], # party increased size 
"{s4}", "player_hire_troop_nextcycle", []],

[anyone,"player_hire_troop_reunite", [], 
"Let me check the troop roster...", "player_hire_troop_reunite_1", []],

[anyone,"player_hire_troop_reunite_1", [
		(call_script, "script_party_eject_nonfaction","$g_encountered_party", "p_main_party", "p_main_party_backup"), #"p_main_party_backup" contains nonfaction troops returned
		(party_get_num_companions, reg0, "p_main_party"),
		(party_get_num_companions, reg46, "p_main_party_backup"),
		(eq, reg46, 0),(eq, reg28, reg0)], # player didn't give anyone (party size unchanged)
"So you've changed your mind...^I see.", "player_hire_troop_nextcycle", []],

[anyone,"player_hire_troop_reunite_1", [(gt, reg46, 0),(eq, reg28, reg0)], # player gave nonfittings only (party size unchanged)
"We don't have use for those troops here...^Take them back.", "player_hire_troop_nextcycle", []],

[anyone,"player_hire_troop_reunite_1", 	
	 [  (gt, reg28, reg0),# player gave fittings too (party size decreased)
		(val_sub, reg28, reg0),(val_sub, reg28, 1), #calculate how many troops given (minus 1)
		(call_script, "script_get_party_disband_cost", "p_main_party", 1),
        (val_sub, "$initial_party_value", reg0), #calculate how much monetary value given
		(try_begin),(eq, reg26, 1),(str_store_string, s31, "@Thank you, commander.^"),(str_clear, s32), #player is in own faction
		 (else_try),               (str_store_string, s32, "@^{s22} is grateful to you, {s23}, {s29}^"),(str_clear, s31),
		(try_end),
		(assign, reg14, "$initial_party_value"),
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@{s31}{reg28?Those:That} brave {reg28?soldiers:soldier} will surely help us defend {s21}.{s32}"+earned_reg14_rp_of_s14),
        (else_try),
          (str_store_string, s4, "@{s31}{reg28?Those:That} useful {reg28?troops:troop} will help us hold {s21}.{s32}"+earned_reg14_rp_of_s14),
        (try_end),
		(try_begin), # if nonfittings were given
          (gt, reg46, 0),
          (str_store_string, s4, "@{s4} ^Oh, and take back those of your soldiers, that are not our kin."),
        (try_end)],
"{s4}", "player_hire_troop_reunite_2", [(troop_add_gold, "$g_player_troop", "$initial_party_value"),]],

[anyone|plyr,"player_hire_troop_reunite_2", 
	 [ (try_begin),(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
		                          (str_store_string, s31, "@I don't need them anyway, so save it."),
	    (else_try),(eq, reg26, 1),(str_store_string, s31, "@It is my duty to protect our people."), #player is of the same faction
	    (else_try),               (str_store_string, s31, "@It is my duty to protect our allies."),
	   (try_end)], 
"{s31}", "player_hire_troop_nextcycle", []],

[anyone,"player_hire_troop_nextcycle", [],
"Anything else?", "player_hire_troop", [
		(party_get_num_companions, reg27, "p_main_party"), # refresh reg27
		# prepare troops which can be given away (others are in moved in temp party)
		#(call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
		#(call_script, "script_party_split_by_faction", "p_main_party_backup", "p_temp_party","$g_encountered_party_faction"),
		]],

		




# Kingdom Lords:
[anyone,"start", [(eq, "$talk_context", tc_castle_commander)], "What do you want?", "player_siege_castle_commander_1", []],
[anyone|plyr,"player_siege_castle_commander_1", [], "Surrender! Your situation is hopeless!", "player_siege_ask_surrender", []],
[anyone|plyr,"player_siege_castle_commander_1", [], "Nothing. I'll leave you now.", "close_window", [(call_script,"script_stand_back"),]],
  
[anyone,"player_siege_ask_surrender", [(lt, "$g_enemy_strength", 100), (store_mul,":required_str","$g_enemy_strength",5),(ge, "$g_ally_strength", ":required_str")],
   "Perhaps... Do you give your word of honour that we'll be treated well?", "player_siege_ask_surrender_treatment", []],
[anyone,"player_siege_ask_surrender", [(lt, "$g_enemy_strength", 200), (store_mul,":required_str","$g_enemy_strength",3),(ge, "$g_ally_strength", ":required_str")],
   "We are ready to leave this castle to you and march away if you give me your word of honour that you'll let us leave unmolested.", "player_siege_ask_leave_unmolested", []],
[anyone,"player_siege_ask_surrender", [], "Surrender? Hah! We can hold these walls until we all die of old age.", "close_window", [(call_script,"script_stand_back"),]],

[anyone|plyr,"player_siege_ask_surrender_treatment", [], "I give you nothing. Surrender now or prepare to die!", "player_siege_ask_surrender_treatment_reject", []],
[anyone,"player_siege_ask_surrender_treatment_reject", [], "Bastard. We will fight you to the last man!", "close_window", [(call_script,"script_stand_back"),]],
[anyone|plyr,"player_siege_ask_surrender_treatment", [], "You will be ransomed and your soldiers will live. I give you my word.", "player_siege_ask_surrender_treatment_accept", []],
[anyone,"player_siege_ask_surrender_treatment_accept", [], "Very well then. Under those terms, I offer you my surrender.", "close_window", [(call_script,"script_stand_back"),(assign,"$g_enemy_surrenders",1)]],

[anyone|plyr,"player_siege_ask_leave_unmolested", [], "You have my word. You will not come under attack if you leave the castle.", "player_siege_ask_leave_unmolested_accept", []],
[anyone,"player_siege_ask_leave_unmolested_accept", [], "Very well. Then we leave this castle to you. You have won this day. But we'll meet again.", "close_window", [(assign,"$g_castle_left_to_player",1)]],
[anyone|plyr,"player_siege_ask_leave_unmolested", [], "Unacceptable. I want prisoners.", "player_siege_ask_leave_unmolested_reject", []],
[anyone,"player_siege_ask_leave_unmolested_reject", [], "Then we will defend this castle to the death, and this parley is done. Farewell.", "close_window", [(call_script,"script_stand_back"),]],

#After battle texts
 
#Troop commentary changes begin
[anyone,"start", [(eq,"$talk_context",tc_hero_defeated),
                    (troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero)],
"{s43}", "defeat_lord_answer",
   [(troop_set_slot, "$g_talk_troop", slot_troop_leaded_party, -1),
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_surrender_offer_default")]],

[anyone|plyr,"defeat_lord_answer", [],
"You are my prisoner now.", "defeat_lord_answer_1",
   [ #(troop_set_slot, "$g_talk_troop", slot_troop_is_prisoner, 1),
     (troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
     (party_force_add_prisoners, "p_main_party", "$g_talk_troop", 1),#take prisoner
     (call_script, "script_add_log_entry", logent_lord_captured_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction")]],

[anyone,"defeat_lord_answer_1", [], "I am at your mercy.", "close_window", [(call_script,"script_stand_back"),]],

[anyone|plyr,"defeat_lord_answer", [], "You have fought well. You are free to go.", "defeat_lord_answer_2",
   [#(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5),
    #(call_script, "script_change_player_honor", 3),
    (call_script, "script_add_log_entry", logent_lord_defeated_but_let_go_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction")]],

[anyone,"defeat_lord_answer_2", [],"{s43}", "close_window", [
	(call_script,"script_stand_back"),
	(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_prisoner_released_default")]],
#Troop commentary changes end

#Troop commentaries changes begin
[anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                    (lt,"$g_encountered_party_relation",0),
                    (encountered_party_is_attacker),
                    (eq, "$g_talk_troop_met", 1),],
"{playername}!", "party_encounter_lord_hostile_attacker", []],

[anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                    (lt,"$g_encountered_party_relation",0),
                    (encountered_party_is_attacker)],
"Halt!", "party_encounter_lord_hostile_attacker", []],

[anyone,"party_encounter_lord_hostile_attacker", [(gt, "$g_comment_found", 0)],
"{s42}", "party_encounter_lord_hostile_attacker", [
                         #MV: no relation changes with enemy lords
                         # (try_begin),
                           # (neq, "$log_comment_relation_change", 0),
                           # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", "$log_comment_relation_change"),
                         # (try_end),
                         (assign, "$g_comment_found", 0)]],

#Troop commentaries changes end
[anyone,"party_encounter_lord_hostile_attacker", [], "{s43}", "party_encounter_lord_hostile_attacker_2",
   [(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_surrender_demand_default")]],

[anyone|plyr,"party_encounter_lord_hostile_attacker_2", [], "Is there no way to avoid this battle? I don't want to fight with you.", "party_encounter_offer_dont_fight", []],
[anyone|plyr,"party_encounter_lord_hostile_attacker_2", [],"Don't attack! We surrender.", "close_window", [(call_script,"script_stand_back"),(assign,"$g_player_surrenders",1)]],
[anyone|plyr,"party_encounter_lord_hostile_attacker_2", [], "We will fight you to the end!", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "party_encounter_offer_dont_fight", [(gt, "$g_talk_troop_relation", 30),
#TODO: Add adition conditions, lord personalities, battle advantage, etc...                                                
                    ],
   "I owe you a favor, don't I. Well... all right then. I will let you go just this once.", "close_window", [
	(call_script,"script_stand_back"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop", -7),
    (store_current_hours,":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),
    (assign, "$g_leave_encounter",1)]],
  
[anyone, "party_encounter_offer_dont_fight", [], "Ha-ha. But I want to fight with you.", "close_window", [(call_script,"script_stand_back"),]],
  


# Events....
#Meeting.

  #[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     # (check_quest_active, "qst_join_faction"),
                     # (eq, "$g_invite_faction_lord", "$g_talk_troop"),
                     # (try_begin),
                       # (gt, "$g_invite_offered_center", 0),
                       # (store_faction_of_party, ":offered_center_faction", "$g_invite_offered_center"),
                       # (neq, ":offered_center_faction", "$g_talk_troop_faction"),
                       # (call_script, "script_get_poorest_village_of_faction", "$g_talk_troop_faction"),
                       # (assign, "$g_invite_offered_center", reg0),
                     # (try_end),
                     # ],
   # #TODO: change conversations according to relation.
   # "{playername}, I've been expecting you. Word has reached my ears of your exploits.\
 # Why, I keep hearing such tales of prowess and bravery that my mind was quickly made up.\
 # I knew that I had found someone worthy of becoming my vassal.", "lord_invite_1",
   # []],


  #[anyone|plyr ,"lord_invite_1", [],  "Thank you, {s65}, you honour me with your offer.", "lord_invite_2",  []],
  #[anyone|plyr ,"lord_invite_1", [],  "It is good to have my true value recognised.", "lord_invite_2",  []],
   
  #[anyone ,"lord_invite_2", [],  "Aye. Let us dispense with the formalities, {playername}; are you ready to swear homage to me?", "lord_invite_3",  []],
    
  #[anyone|plyr ,"lord_invite_3", [],  "Yes, {s65}.", "lord_give_oath_2",  []],
  #[anyone|plyr ,"lord_invite_3", [],  "No, {s65}. I cannot serve you right now.", "lord_enter_service_reject",  []],

[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (eq,"$talk_context",tc_town_talk),
                     (eq, "$sneaked_into_town",1)],
"Away with you, vile beggar.", "close_window",  [(call_script,"script_stand_back"),]],
  
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (neq, "$g_talk_troop_met", 0),
                     (gt, "$g_time_since_last_talk", 24),
                     (gt, "$g_talk_troop_relation", 50),
                     (gt, "$g_talk_troop_faction_relation", 10),
                     (le,"$talk_context",tc_siege_commander)],
"If it isn't my brave champion, {playername}...", "lord_start",  []],
  
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (neq, "$g_talk_troop_met", 0),
                     (gt, "$g_time_since_last_talk", 24),
                     (gt, "$g_talk_troop_relation", 10),
                     (le,"$talk_context",tc_siege_commander)],
"Good to see you again {playername}...", "lord_start", []],

[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (neq, "$g_talk_troop_met", 0),
                     (gt, "$g_time_since_last_talk", 24),
#                     (lt, "$g_talk_troop_faction_relation", 0),
                     (le,"$talk_context",tc_siege_commander)],
"We meet again, {playername}...", "lord_start", []],

#TLD: your fellow kingdom lords know you
[anyone|auto_proceed ,"start", [
                     (eq,"$players_kingdom","$g_talk_troop_faction"),
                     (troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (eq, "$g_talk_troop_met", 0),
                     (ge, "$g_talk_troop_faction_relation", 0),
                     (le,"$talk_context",tc_siege_commander)],
"INVALID", "lord_intro", []],
   
[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (eq, "$g_talk_troop_met", 0),
                     (ge, "$g_talk_troop_faction_relation", 0),
                     (le,"$talk_context",tc_siege_commander)],
"Do I know you?", "lord_meet_neutral", []],
  
[anyone|plyr ,"lord_meet_neutral", [],  "I am {playername}.", "lord_intro", []],
[anyone|plyr ,"lord_meet_neutral", [],  "My name is {playername}. At your service.", "lord_intro", []],

[anyone ,"lord_intro", [],
"{s11}", "lord_start",   [(faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
                          (str_store_faction_name, s6, "$g_talk_troop_faction"),
                          (assign, reg4, 0),
                          (str_store_troop_name, s4, "$g_talk_troop"),
                          (try_begin),
                            (eq, ":faction_leader", "$g_talk_troop"),
                            (str_store_troop_name_plural, s15,"$g_talk_troop"), #GA: plural name for kings contains referral to them
                            (str_store_string, s9, "@I am {s4}, {s15} of {s6}", 0),
                          (else_try),
                            (str_store_string, s9, "@I am {s4}, a commander of {s6}", 0),
                          (try_end),
                          (assign, ":num_centers", 0),
                          (str_clear, s8),
                          (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
                            (party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
							(party_slot_eq, ":cur_center", slot_town_lord, "$g_talk_troop"),
                            (party_is_active, ":cur_center"), #TLD
                            (try_begin),
                              (eq, ":num_centers", 0),
                              (str_store_party_name, s8, ":cur_center"),
                            (else_try),
                              (eq, ":num_centers", 1),
                              (str_store_party_name, s7, ":cur_center"),
                              (str_store_string, s8, "@{s7} and {s8}"),
                            (else_try),
                              (str_store_party_name, s7, ":cur_center"),
                              (str_store_string, s8, "@{s7}, {s8}"),
                            (try_end),
                            (val_add, ":num_centers", 1),
                          (try_end),
                          (assign, reg5, ":num_centers"),
                          (str_store_string, s11, "@{s9}{reg5? and the ruler of {s8}.:.", 0)]],

#[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
#                     (eq, "$g_talk_troop_met", 0),
#                     (ge, "$g_talk_troop_faction_relation", 0),
#                     (le,"$talk_context",tc_siege_commander),
#                     ],
#   "Who is this then?", "lord_meet_ally", []],
#[anyone|plyr ,"lord_meet_ally", [],  "I am {playername} sir. A warrior of {s4}.", "lord_start", []],
#[anyone|plyr ,"lord_meet_ally", [],  "I am but a soldier of {s4} sir. My name is {playername}.", "lord_start", []],

[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                     (eq, "$g_talk_troop_met", 0),
                     (lt, "$g_talk_troop_faction_relation", 0),
#                     (str_store_faction_name, s4,  "$players_kingdom"),
                     (le,"$talk_context",tc_siege_commander)],
"{s43}", "lord_meet_enemy", [(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_enemy_meet_default")]],
   
[anyone|plyr ,"lord_meet_enemy", [],  "I am {playername}.", "lord_intro", []],  #A warrior of {s4}.
[anyone|plyr ,"lord_meet_enemy", [],  "They know me as {playername}. Mark it down, you shall be hearing of me a lot.", "lord_intro", []],
#[anyone, "lord_meet_enemy_2", [],  "{playername} eh? Never heard of you. What do want?", "lord_talk", []],

[anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_hero),
                   (le,"$talk_context",tc_siege_commander)],
"Well, {playername}...", "lord_start",[]],

[anyone,"lord_start", [(gt, "$g_comment_found", 0)], #changed to s32 from s62 because overlaps with setup_talk_info strings
"{s42}", "lord_start", [
#      (store_current_hours, ":cur_time"),
#      (troop_set_slot, "$g_talk_troop", slot_troop_last_comment_time, ":cur_time"),
       (try_begin),
         (neq, "$log_comment_relation_change", 0),
         (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", "$log_comment_relation_change"),
       (try_end),
       (assign, "$g_comment_found", 0)]],  

[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                       (eq,":lords_quest","qst_lend_surgeon"),
                       (quest_slot_eq, "qst_lend_surgeon", slot_quest_giver_troop, "$g_talk_troop")],
"Your surgeon managed to convince my friend and made the operation.  All we can do now is pray for his recovery.\
 Anyway, I thank you for lending your surgeon to me, {playername}. You have a noble spirit. I will not forget it.", "lord_generic_mission_completed",
	[(call_script, "script_finish_quest", "qst_lend_surgeon", 100),
	(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
##### TODO: QUESTS COMMENT OUT BEGIN

##
##[anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_bring_prisoners_to_enemy"),
##                         (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_current_state, 0),
##                         (check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##                         (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                         (assign, reg1, ":quest_target_amount")],
##   "TODO: You have brought the prisoners and received {reg1} denars. Give me the money now.", "lord_bring_prisoners_complete_2",[]],
##
##[anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_bring_prisoners_to_enemy"),
##                         (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_current_state, 1),#Some of them were brought only
##                         (check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##                         (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                         (assign, reg1, ":quest_target_amount")],
##   "TODO: You have brought the prisoners but some of them died during your expedition. Give me the full money of {reg1} denars.", "lord_bring_prisoners_complete_2",[]],
##
##
##[anyone|plyr,"lord_bring_prisoners_complete_2", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                                   (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                                   (ge, ":cur_gold", ":quest_target_amount")],
##   "TODO: Here it is.", "lord_generic_mission_thank", [(quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                                  (troop_remove_gold, "trp_player", ":quest_target_amount"),
##                                                  (call_script, "script_finish_quest", "qst_bring_prisoners_to_enemy", 100)]],
##  
##[anyone|plyr,"lord_bring_prisoners_complete_2", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                                   (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                                   (lt, ":cur_gold", ":quest_target_amount")],
##   "TODO: I'm afraid I spent some of it, I don't have that much money with me.", "lord_bring_prisoners_no_money", [(quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                                                                                                   (call_script, "script_change_debt_to_troop", "$g_talk_troop", ":quest_target_amount"),#Adding the taken money as a debt
##                                                                                                                   (call_script, "script_finish_quest", "qst_bring_prisoners_to_enemy", 100)]],
##
##[anyone,"lord_bring_prisoners_no_money", [],
##   "TODO: You owe me that money!", "lord_pretalk", []],
##
##

  #[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         # (eq,":lords_quest","qst_incriminate_loyal_commander"),
                         # (check_quest_succeeded, "qst_incriminate_loyal_commander"),
                         # (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
                         # (str_store_troop_name, s3, ":quest_target_troop"),
                         # (quest_get_slot, reg5, "qst_incriminate_loyal_commander", slot_quest_gold_reward),
                         # ],
   # "Hah! Our little plot against {s3} worked perfectly, {playername}.\
 # The fool has lost one of his most valuable retainers, and we are one step closer to bringing him to his knees.\
 # Here, this purse contains {reg5} denars, and I wish you to have it. You deserve every copper.\
 # And, need I remind you, there could be much more to come if you've a mind to earn it...", "lord_generic_mission_completed",[
     # (call_script, "script_end_quest", "qst_incriminate_loyal_commander"),
     # (call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
     # (call_script, "script_change_player_honor", -10),
     # ]],

  #[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         # (eq,":lords_quest","qst_incriminate_loyal_commander"),
                         # (check_quest_failed, "qst_incriminate_loyal_commander")],
   # "You werent't able to complete a simple task. I had set up everything.\
 # The only thing you needed to do was sacrifice a messenger, and we would be celebrating now.\
 # But no, you were too damned honorable, weren't you?", "close_window",[
     # (call_script, "script_end_quest", "qst_incriminate_loyal_commander"),
     # (call_script, "script_change_player_relation_with_troop","$g_talk_troop",-5),
     # (call_script, "script_change_player_honor", 3),
 # ]],
  # #TODO: NO GENERIC MISSION FAILED ANYMORE!!!!

  #TLD quests fail/success BEGIN:

[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                       (eq,":lords_quest","qst_investigate_fangorn"),
                       (check_quest_succeeded, "qst_investigate_fangorn")],
"So, {playername}, you return from Fangorn. What did you find out?", "lord_investigate_fangorn_completed0",[]],
	 
[anyone|plyr, "lord_investigate_fangorn_completed0",[], "The trees are alive! They assault our troops!","lord_investigate_fangorn_completed1",[]],
	
[anyone, "lord_investigate_fangorn_completed1",[],
"I suspected that all along. You have been of good service to me, {playername}.","close_window",[
	(call_script,"script_stand_back"),
	(call_script, "script_finish_quest", "qst_investigate_fangorn", 100),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",5)]],

[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_investigate_fangorn"),
                         (check_quest_failed, "qst_investigate_fangorn")],
"My patience is over. \
I was expecting you to tell me something about Fangorn by now, but you know nothing.", "close_window",[
	(call_script,"script_stand_back"),
	(call_script, "script_end_quest", "qst_investigate_fangorn"),
	(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-5)]],
  
  
    # CAPTURE TROLL QUEST START
	
    #[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
    #                     (eq,":lords_quest","qst_capture_troll"),
    #                     (check_quest_succeeded, "qst_capture_troll"),
    #                     ],
   #"{playername}! I asked you to bring me one troll beast.", "lord_capture_troll_completed0",[
   #  ]],
	 
[anyone|plyr, "lord_active_mission_2", [(party_count_prisoners_of_type, ":num_trolls", "p_main_party", "trp_troll_of_moria"),
										(ge, ":num_trolls", 2), 
										(store_partner_quest,":lords_quest"),(eq,":lords_quest","qst_capture_troll"),],	
"Master, I hereby give you not one, but a pair of beasts!","lord_capture_troll_completed_two_trolls",[]],

[anyone|plyr, "lord_active_mission_2", [(party_count_prisoners_of_type, ":num_trolls", "p_main_party", "trp_troll_of_moria"),
										(eq, ":num_trolls", 1), 
										(store_partner_quest,":lords_quest"),(eq,":lords_quest","qst_capture_troll"),
										],	
"Master, I subjugated the beast you have asked for!","lord_capture_troll_completed_one_troll",[]],
	
	
[anyone, "lord_capture_troll_completed_two_trolls",[],
"Two beasts! Excellent, {playername}. You proved worthy, and skill and dedication must be rewarded. With your two trolls, We can now make without one of those We were using for Our experiments. It is a fully trained slave, ready to fight under command. We mean YOUR command, {playername}.",
	"lord_capture_troll_completed_two_trolls_thankyou",
	[ (call_script, "script_finish_quest", "qst_capture_troll", 100),
      	  (call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
	  (troop_remove_item,"trp_player","itm_wheeled_cage"), # Take his cage back
	  (party_remove_prisoners, "p_main_party", "trp_troll_of_moria", 2)]],

[anyone|plyr, "lord_capture_troll_completed_two_trolls_thankyou",[(troops_can_join, 1),],
"Can a savage beast be made to obey commands?","lord_capture_troll_completed_two_trolls_thankyou_info",[]],

[anyone|plyr, "lord_capture_troll_completed_two_trolls_thankyou",[(troops_can_join, 1),],
"Thank you, Master. You will be pleased by the way this troll will be put in good use.","lord_capture_troll_completed_two_trolls_thankyou_accept",[]],

[anyone|plyr, "lord_capture_troll_completed_two_trolls_thankyou",[(troops_can_join, 1),],
"Thank you, master. But I'm not worth of your great gift. It is too dangerous for me.","lord_capture_troll_completed_two_trolls_thankyou_refuse",[]],

[anyone|plyr, "lord_capture_troll_completed_two_trolls_thankyou",[(troops_can_join|neg, 1),],
"Thank you, master. But I'm not worth of your great gift. [no room in party!]","lord_capture_troll_completed_two_trolls_thankyou_refuse",[]],

[anyone|plyr, "lord_capture_troll_completed_two_trolls_thankyou",[(faction_get_slot, reg20, "$g_talk_troop_faction", slot_faction_influence)],
"Master, I will bring greater havoc if you also provide an armour for the beast [10/{reg20} influence].","lord_capture_troll_completed_two_trolls_thankyou_raise",[]],

[anyone, "lord_capture_troll_completed_two_trolls_thankyou_info",[],
"Are you questioning the abilities of your Master, {playername}? This beast is trained to attack enemies on sight. This is enough. But, you and your warriors keep at due distance from the beast when it fights, and never stand between it and its victims.","lord_capture_troll_completed_two_trolls_thankyou",[]],

[anyone, "lord_capture_troll_completed_two_trolls_thankyou_accept",[],
"Now bring havoc to my enemies with your new gift","lord_pretalk", [(party_add_members, "p_main_party", "trp_troll_of_moria", 1)]],

[anyone, "lord_capture_troll_completed_two_trolls_thankyou_refuse",[],
"As you wish, then. Someone else among of my servants will known how to use this mighty tool of war.","lord_pretalk",[]],

[anyone, "lord_capture_troll_completed_two_trolls_thankyou_raise",[(faction_slot_ge, "$g_talk_troop_faction", slot_faction_influence, 10)],
"You dare ask for an fully armoured battle troll, {playername}, to keep under your command? That's not a small thing to ask for. But you are a skilled servant, and we know your motivations. We like that. It shall be granted.","lord_pretalk",
	[(party_add_members, "p_main_party", "trp_armoured_troll", 1),
	 (call_script, "script_spend_influence_of", 10, "$g_talk_troop_faction"),]],

[anyone, "lord_capture_troll_completed_two_trolls_thankyou_raise",[(neg|faction_slot_ge, "$g_talk_troop_faction", slot_faction_influence, 10)],
"How dare you ask Us for more than We have planned for you in our great Wisdom? {playername}, you proved a mighty Servant today, but don't let your insolence test Our patience any further.","lord_capture_troll_completed_two_trolls_thankyou",[]],

[anyone, "lord_capture_troll_completed_one_troll",[],
"Excellent, {playername}. You are a most faithful and useful servant. This troll will be most useful for our purposes. That it is taken to the dungeons!", "close_window",[
	(call_script,"script_stand_back"),
	(call_script, "script_finish_quest", "qst_capture_troll", 100),
    	(call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
	(troop_remove_item,"trp_player","itm_wheeled_cage"), # Take his cage back
	(party_remove_prisoners, "p_main_party", "trp_troll_of_moria", 1)]],
	
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_capture_troll"),
                         (check_quest_failed, "qst_capture_troll")],
"Too long ago, I asked you to take me one troll alive. But I should have known. \
How could I expect someone like {playername} to be up to the challange. My servant was not skilled or faithful enough.", "close_window",[
   (call_script,"script_stand_back"),
   (call_script, "script_end_quest", "qst_capture_troll"),
   (call_script, "script_change_player_relation_with_troop","$g_talk_troop",-5)]],
  
    # CAPTURE TROLL QUEST END
	  
	# KILL TROLL QUEST START
[anyone,"lord_start", [
	  (store_partner_quest,":lords_quest"),
	  (eq,":lords_quest","qst_kill_troll"),
	  (check_quest_succeeded, "qst_kill_troll"),
	  (quest_get_slot, ":quest_object_center", "qst_kill_troll", slot_quest_object_center),
	  (str_store_party_name,12,":quest_object_center")],
"News of your accomplishment against the wild trolls reached me. {s12} has one fear less to worry about, thanks to you, {playername}.", "lord_generic_mission_completed",[
	  (call_script, "script_finish_quest", "qst_kill_troll", 100),
	  (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3)]],
	# KILL TROLL QUEST END

	  #TLD quests fail/success END:
 
	 

  #[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         # (eq,":lords_quest","qst_meet_spy_in_enemy_town"),
                         # (check_quest_succeeded, "qst_meet_spy_in_enemy_town"),
                         # ],
   # "Have you brought me any news about that task I gave you? You know the one I mean...", "quest_meet_spy_in_enemy_town_completed",
   # []],

  #[anyone|plyr, "quest_meet_spy_in_enemy_town_completed", [],
   # "I have the reports you wanted right here.", "quest_meet_spy_in_enemy_town_completed_2",[]],

  #[anyone, "quest_meet_spy_in_enemy_town_completed_2", [],
   # "Ahh, well done. It's good to have competent {men/people} on my side. Here is the payment I promised you.", "lord_pretalk",
   # [
     # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
     # (add_xp_as_reward, 500),
     # (quest_get_slot, ":gold", "qst_meet_spy_in_enemy_town", slot_quest_gold_reward),
     # (call_script, "script_troop_add_gold", "trp_player", ":gold"),
     # (call_script, "script_end_quest", "qst_meet_spy_in_enemy_town"),
     # ]],

  #[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         # (eq,":lords_quest","qst_raid_caravan_to_start_war"),
                         # (check_quest_succeeded, "qst_raid_caravan_to_start_war"),
                         # (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
                         # (str_store_faction_name, s13, ":quest_target_faction"),
                         # ],
   # "Brilliant work, {playername}! Your caravan raids really got their attention, I must say.\
 # I've just received word that {s13} has declared war!\
 # Now the time has come for us to reap the benefits of our hard work, {playername}.\
 # And by that I of course mean taking and plundering {s13} land!\
 # This war is going to make us rich {men/souls}, mark my words!", "lord_pretalk",
   # [
    # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
    # (try_for_range, ":vassal", kingdom_heroes_begin, kingdom_heroes_end),
      # (store_troop_faction, ":vassal_fac", ":vassal"),
      # (eq, ":vassal_fac", "$players_kingdom"),
      # (neq,  ":vassal", "$g_talk_troop"),
      # (store_random_in_range, ":rel_change", -5, 4),
      # (call_script, "script_change_player_relation_with_troop", ":vassal", ":rel_change"),
    # (try_end),
    # #TODO: Add gold reward notification before the quest is given. 500 gold is not mentioned anywhere.
    # (call_script, "script_troop_add_gold", "trp_player", 500),
    # (add_xp_as_reward, 2000),
    # (call_script, "script_change_player_honor", -5),
    # (call_script, "script_end_quest", "qst_raid_caravan_to_start_war")
    # ]],

  #[anyone,"lord_start", [(store_partner_quest, ":lords_quest"),
                         # (eq, ":lords_quest", "qst_raid_caravan_to_start_war"),
                         # (check_quest_failed, "qst_raid_caravan_to_start_war"),
                         # ],
   # "You incompetent buffoon!\
 # What in Hell made you think that getting yourself captured while trying to start a war was a good idea?\
 # These plans took months to prepare, and now everything's been ruined! I will not forget this, {playername}.\
 # Oh, be assured that I will not.", "lord_pretalk",
   # [
    # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -10),
    # (call_script, "script_end_quest", "qst_raid_caravan_to_start_war")
    # ]],

  #[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         # (eq,":lords_quest","qst_collect_debt"),
                         # (quest_slot_eq, "qst_collect_debt", slot_quest_current_state, 1),
                         # (quest_get_slot, ":target_troop", "qst_collect_debt", slot_quest_target_troop),
                         # (str_store_troop_name, s7, ":target_troop"),
                         # (quest_get_slot, ":total_collected","qst_collect_debt",slot_quest_target_amount),
                         # (store_div, reg3, ":total_collected", 5),
                         # (store_sub, reg4, ":total_collected", reg3)],
   # "I'm told that you've collected the money owed me from {s7}. Good, it's past time I had it back.\
 # I believe I promised to give you one-fifth of it all, eh?\
 # Well, that makes {reg3} denars, so if you give me my share -- that's {reg4} denars -- you can keep the rest.", "lord_collect_debt_completed", []],

  
  #[anyone|plyr,"lord_collect_debt_completed", [(store_troop_gold, ":gold", "trp_player"),
                                               # (ge, ":gold", reg4)],
   # "Of course, {s65}. {reg4} denars, all here.", "lord_collect_debt_pay",[]],

  #[anyone,"lord_collect_debt_pay", [],
   # "I must admit I'm impressed, {playername}. I had lost hope of ever getting this money back.\
 # Please accept my sincere thanks.", "lord_pretalk",[
     # (troop_remove_gold, "trp_player", reg4),
     # (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
     # (add_xp_as_reward, 100),
     # (call_script, "script_end_quest", "qst_collect_debt")
     # ]],
  
  #[anyone|plyr,"lord_collect_debt_completed", [], "I am afraid I don't have the money with me sir.", "lord_collect_debt_no_pay",[]],
  #[anyone,"lord_collect_debt_no_pay", [], "Is this a joke?\
 # I know full well that {s7} gave you the money, and I want every denar owed to me, {sir/madam}.\
 # As far as I'm concerned, I hold you personally in my debt until I see that silver.", "close_window",[
     # (call_script, "script_change_debt_to_troop", "$g_talk_troop", reg4),
     # (call_script, "script_end_quest", "qst_collect_debt"),

     # (call_script, "script_objectionable_action", tmt_honest, "str_squander_money"),
     # ]],

  #[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         # (eq,":lords_quest","qst_kill_local_merchant"),
                         # (check_quest_succeeded, "qst_kill_local_merchant"),
                         # (quest_slot_eq, "qst_kill_local_merchant", slot_quest_current_state, 1)],
   # "I heard you got rid of that poxy merchant that was causing me so much grief.\
 # I can see you're not afraid to get your hands dirty, eh? I like that in a {man/woman}.\
 # Here's your reward. Remember, {playername}, stick with me and we'll go a long, long way together.", "close_window",
   # [ (call_script, "script_troop_add_gold", "trp_player", 600),
     # (call_script, "script_change_player_relation_with_troop","$g_talk_troop",4),
     # (add_xp_as_reward, 300),
     # (call_script, "script_end_quest", "qst_kill_local_merchant"),

     # (call_script, "script_objectionable_action", tmt_humanitarian, "str_murder_merchant"), 
     
     # (assign, "$g_leave_encounter", 1)]],

  #[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         # (eq,":lords_quest","qst_kill_local_merchant"),
                         # (check_quest_failed, "qst_kill_local_merchant")],
   # "Oh, it's you. Enlighten me, how exactly does one lose a simple fight to some poxy, lowborn merchant?\
 # Truly, if I ever need my guardsmen to take a lesson in how to lay down and die, I'll be sure to come to you.\
 # Just leave me be, {playername}, I have things to do.", "close_window",
   # [(call_script, "script_end_quest", "qst_kill_local_merchant"),
    # (assign, "$g_leave_encounter", 1)]],

  #[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         # (eq,":lords_quest","qst_kill_local_merchant"),
                         # (check_quest_succeeded, "qst_kill_local_merchant"),
                         # (quest_slot_eq, "qst_kill_local_merchant", slot_quest_current_state, 2)],
   # "You! Do you have sawdust between your ears? Did you think that when I said to kill the merchant,\
 # I meant you to have a nice chat with him and then let him go?! What possessed you?", "lord_kill_local_merchant_let_go",[]],

  #[anyone|plyr,"lord_kill_local_merchant_let_go", [],
   # "Sir, I made sure he will not act against you.", "lord_kill_local_merchant_let_go_2",[]],

  #[anyone,"lord_kill_local_merchant_let_go_2", [],
   # "Piffle. You were supposed to remove him, not give him a sermon and send him on his way.\
 # He had better do as you say, or you'll both regret it.\
 # Here, this is half the money I promised you. Don't say a word, {playername}, you're lucky to get even that.\
 # I have little use for {men/people} who cannot follow orders.", "lord_pretalk",
   # [(call_script, "script_troop_add_gold", "trp_player", 300),
     # (call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
     # (add_xp_as_reward, 500),
     # (call_script, "script_end_quest", "qst_kill_local_merchant"),
     # (assign, "$g_leave_encounter", 1)
    # ]],

##[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_hunt_down_raiders"),
##                         (check_quest_failed, "qst_hunt_down_raiders")],
##   "I heard that those raiders you were after have got away. Do you have an explanation?", "quest_hunt_down_raiders_failed",[]],
##[anyone|plyr,"quest_hunt_down_raiders_failed", [],  "They were too quick for us my lord. But next time we'll get them", "quest_hunt_down_raiders_failed_2",[]],
##[anyone|plyr,"quest_hunt_down_raiders_failed", [],  "They were too strong and well armed my lord. But we'll be ready for them next time.", "quest_hunt_down_raiders_failed_2",[]],
##  
##[anyone|plyr,"quest_hunt_down_raiders_failed", [],  "Well, it was a long call anyway. Next time do make sure that you are better prepared.",
##   "lord_pretalk",[(call_script, "script_end_quest", "qst_hunt_down_raiders")]],
##
##
##
##[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_hunt_down_raiders"),
##                         (check_quest_succeeded, "qst_hunt_down_raiders")],
##   "I heard that you have given those raiders the punishment they deserved. Well done {playername}.\
## ", "lord_generic_mission_completed",[(call_script, "script_finish_quest", "qst_hunt_down_raiders", 100),
##                                      (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3)]],
##


##[anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_defend_nobles_against_peasants"),
##                         (this_or_next|check_quest_succeeded, "qst_defend_nobles_against_peasants"),
##                         (check_quest_failed, "qst_defend_nobles_against_peasants"),
##                         (assign, ":num_saved", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee_woman"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (assign, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_saved"),
##                         (eq, ":num_saved", "$qst_defend_nobles_against_peasants_num_nobles_to_save")],
##   "TODO: You have saved all of them. Good boy.", "lord_generic_mission_completed",
##   [(party_remove_members, "p_main_party", "trp_noble_refugee", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##    (party_remove_members, "p_main_party", "trp_noble_refugee_woman", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##    (call_script, "script_finish_quest", "qst_defend_nobles_against_peasants", 100)]],
##
##[anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_defend_nobles_against_peasants"),
##                         (this_or_next|check_quest_succeeded, "qst_defend_nobles_against_peasants"),
##                         (check_quest_failed, "qst_defend_nobles_against_peasants"),
##                         (assign, ":num_saved", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee_woman"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (assign, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_saved"),
##                         (lt, ":num_saved", "$qst_defend_nobles_against_peasants_num_nobles_to_save"),
##                         (gt, "$qst_defend_nobles_against_peasants_num_nobles_saved", 0)],
##   "TODO: You have saved some of them. Half good boy.", "lord_capture_conspirators_half_completed",
##   [(party_remove_members, "p_main_party", "trp_noble_refugee", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##    (party_remove_members, "p_main_party", "trp_noble_refugee_woman", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##    (assign, ":ratio", 100),
##    (val_mul, ":ratio", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##    (val_div, ":ratio", "$qst_defend_nobles_against_peasants_num_nobles_to_save"),
##    (call_script, "script_finish_quest", "qst_defend_nobles_against_peasants", ":ratio")]],
##
##[anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_defend_nobles_against_peasants"),
##                         (this_or_next|check_quest_succeeded, "qst_defend_nobles_against_peasants"),
##                         (check_quest_failed, "qst_defend_nobles_against_peasants"),
##                         (assign, ":num_saved", "$qst_defend_nobles_against_peasants_num_nobles_saved"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (party_count_companions_of_type, ":num_nobles", "p_main_party", "trp_noble_refugee_woman"),
##                         (val_add, ":num_saved", ":num_nobles"),
##                         (eq, ":num_saved", 0)],
##   "TODO: You have saved none of them. Bad boy.", "lord_generic_mission_failed", []],
##
##
##[anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_capture_conspirators"),
##                         (this_or_next|check_quest_succeeded, "qst_capture_conspirators"),
##                         (check_quest_failed, "qst_capture_conspirators"),
##                         (party_count_prisoners_of_type, ":num_conspirators", "p_main_party", "trp_conspirator"),
##                         (party_count_prisoners_of_type, ":num_conspirator_leaders", "p_main_party", "trp_conspirator_leader"),
##                         (store_add, ":sum_captured", ":num_conspirators", ":num_conspirator_leaders"),
##                         (ge, ":sum_captured", "$qst_capture_conspirators_num_troops_to_capture")],
##   "TODO: You have captured all of them. Good boy.", "lord_generic_mission_completed",
##   [(party_remove_prisoners, "p_main_party", "trp_conspirator_leader", "$qst_capture_conspirators_num_troops_to_capture"),
##    (party_remove_prisoners, "p_main_party", "trp_spy_partner", "$qst_capture_conspirators_num_troops_to_capture"),
##    (call_script, "script_finish_quest", "qst_capture_conspirators", 100)]],
##
##[anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_capture_conspirators"),
##                         (this_or_next|check_quest_succeeded, "qst_capture_conspirators"),
##                         (check_quest_failed, "qst_capture_conspirators"),
##                         (party_count_prisoners_of_type, ":num_conspirators", "p_main_party", "trp_conspirator"),
##                         (party_count_prisoners_of_type, ":num_conspirator_leaders", "p_main_party", "trp_conspirator_leader"),
##                         (store_add, ":sum_captured", ":num_conspirators", ":num_conspirator_leaders"),
##                         (lt, ":sum_captured", "$qst_capture_conspirators_num_troops_to_capture"),
##                         (gt, ":sum_captured", 0)],
##   "TODO: You have captured some of them. Half good boy.", "lord_capture_conspirators_half_completed",
##   [(assign, ":sum_removed", 0),
##    (party_remove_prisoners, "p_main_party", "trp_conspirator_leader", "$qst_capture_conspirators_num_troops_to_capture"),
##    (val_add, ":sum_removed", reg0),
##    (party_remove_prisoners, "p_main_party", "trp_conspirator", "$qst_capture_conspirators_num_troops_to_capture"),
##    (val_add, ":sum_removed", reg0),
##    (val_mul, ":sum_removed", 100),
##    (val_div, ":sum_removed", "$qst_capture_conspirators_num_troops_to_capture"),
##    (call_script, "script_finish_quest", "qst_capture_conspirators", ":sum_removed")]],
##
##[anyone,"lord_start", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                         (store_partner_quest,":lords_quest"),
##                         (eq,":lords_quest","qst_capture_conspirators"),
##                         (this_or_next|check_quest_succeeded, "qst_capture_conspirators"),
##                         (check_quest_failed, "qst_capture_conspirators"),
##                         (party_count_prisoners_of_type, ":num_conspirators", "p_main_party", "trp_conspirator"),
##                         (party_count_prisoners_of_type, ":num_conspirator_leaders", "p_main_party", "trp_conspirator_leader"),
##                         (store_add, ":sum_captured", ":num_conspirators", ":num_conspirator_leaders"),
##                         (eq, ":sum_captured", 0)],
##   "TODO: You have captured none of them. Bad boy.", "lord_generic_mission_failed", []],
##
##[anyone|plyr,"lord_capture_conspirators_half_completed", [],
##   "TODO: That's all I can do.", "lord_pretalk", []],


[anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
						 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (quest_get_slot, ":spy_troop", "qst_follow_spy", slot_quest_object_troop),
                         (quest_get_slot, ":spy_partner", "qst_follow_spy", slot_quest_target_troop),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", ":spy_troop"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", ":spy_partner"),
                         (gt, ":num_spies", 0),
                         (gt, ":num_spy_partners", 0)],
"{s4}", "lord_follow_spy_completed",
   [(quest_get_slot, ":spy_troop", "qst_follow_spy", slot_quest_object_troop),
    (quest_get_slot, ":spy_partner", "qst_follow_spy", slot_quest_target_troop),
    (party_remove_prisoners, "p_main_party", ":spy_troop", 1),
    (party_remove_prisoners, "p_main_party", ":spy_partner", 1),
    (call_script, "script_finish_quest", "qst_follow_spy", 100),
    (try_begin),
      (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
      (str_store_string, s4, "@Very well done, {playername}! You captured both the spy and his handler, just as I'd hoped,\
 and the pair are now safely locked up, waiting to be questioned.\
 They will have some explaining to do! Anyway, I'm very pleased with your success, {playername}, and I give you\
 this purse as a token of my appreciation."),
    (else_try),
      (str_store_string, s4, "@Beautiful work, {playername}! You captured both the spy and his handler, just as you were told,\
 and the pair are now safely locked up in my dungeon, waiting to be questioned.\
 My torturer shall be busy tonight! Anyway, I'm very pleased with your success, {playername}, and I give you\
 this purse as a token of my appreciation."),
    (try_end)]],

[anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
						 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (quest_get_slot, ":spy_troop", "qst_follow_spy", slot_quest_object_troop),
                         (quest_get_slot, ":spy_partner", "qst_follow_spy", slot_quest_target_troop),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", ":spy_troop"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", ":spy_partner"),
                         (gt, ":num_spies", 0),
                         (eq, ":num_spy_partners", 0)],
"Blast and damn you! I wanted TWO prisoners, {playername} -- what you've brought me is one step short of\
 useless! I already know everything the spy knows, it was the handler I was after.\
 Here, half a job gets you half a reward. Take it and begone.", "lord_follow_spy_half_completed",
   [(quest_get_slot, ":spy_troop", "qst_follow_spy", slot_quest_object_troop),
    (party_remove_prisoners, "p_main_party", ":spy_troop", 1),
    (call_script, "script_finish_quest", "qst_follow_spy", 50)]],

[anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
					     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (quest_get_slot, ":spy_troop", "qst_follow_spy", slot_quest_object_troop),
                         (quest_get_slot, ":spy_partner", "qst_follow_spy", slot_quest_target_troop),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", ":spy_troop"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", ":spy_partner"),
                         (eq, ":num_spies", 0),
                         (gt, ":num_spy_partners", 0)],
"I asked you for two prisoners, {playername}, not one. Two. Still, I suppose you did capture the spy's handler,\
 the more important one of the pair. The spy will not dare return here and will prove quite useless to\
 whatever master he served. 'Tis better than nothing.\
 However, you'll understand if I pay you half the promised reward for what is but half a success.", "lord_follow_spy_half_completed",
   [(quest_get_slot, ":spy_partner", "qst_follow_spy", slot_quest_target_troop),
    (party_remove_prisoners, "p_main_party", ":spy_partner", 1),
    (call_script, "script_finish_quest", "qst_follow_spy", 75)]],

[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (quest_get_slot, ":spy_troop", "qst_follow_spy", slot_quest_object_troop),
                         (quest_get_slot, ":spy_partner", "qst_follow_spy", slot_quest_target_troop),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", ":spy_troop"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", ":spy_partner"),
                         (eq, ":num_spies", 0),
                         (eq, ":num_spy_partners", 0)],
"Truly, {playername}, you are nothing short of totally incompetent.\
 Failing to capture both the spy AND his handler plumbs astonishing new depths of failure.\
 Forget any reward I offered you. You've done nothing to earn it.", "lord_follow_spy_failed",
   [(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-2),
    (call_script, "script_end_quest", "qst_follow_spy")]],

[anyone|plyr,"lord_follow_spy_half_completed", [], "I did my best, {s65}.", "lord_pretalk", []],
[anyone|plyr,"lord_follow_spy_completed", [], "Thank you, {s65}.", "lord_pretalk", []],
[anyone|plyr,"lord_follow_spy_failed", [], "Hrm. As you like, {s65}.", "lord_pretalk", []],


[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_bring_back_runaway_serfs"),
                         (check_quest_succeeded, "qst_bring_back_runaway_serfs")],
"Damn me, but you've done it, {playername}. All the slaves are back and they're busy preparing for the harvest.\
 You certainly earned your reward. Here, take it, with my compliments.", "lord_generic_mission_completed",
   [(call_script, "script_finish_quest", "qst_bring_back_runaway_serfs", 100),
    (call_script, "script_objectionable_action", tmt_humanitarian, "str_round_up_serfs")]],

[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_bring_back_runaway_serfs"),
                         (check_quest_failed, "qst_bring_back_runaway_serfs"),],
"{playername}. I have been waiting patiently for my slaves, yet none have returned. Have you an explanation?\
 Were you outwitted by simple animals, or are you merely incompetent?", "lord_bring_back_runaway_serfs_failed", []],

[anyone|plyr,"lord_bring_back_runaway_serfs_failed", [],
   "Forgive me, {s65}, those slaves were slippery as eels.", "lord_bring_back_runaway_serfs_failed_1a", []],
  #[anyone|plyr,"lord_bring_back_runaway_serfs_failed", [],
   # "Perhaps if you had treated them better...", "lord_bring_back_runaway_serfs_failed_1b", []],

[anyone,"lord_bring_back_runaway_serfs_failed_1a", [],
"Hmph, that is hardly an excuse for failure, {playername}.\
 Now if you will excuse me, I need to capture new men to work these fields before we all starve.", "lord_pretalk",
   [(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-1),
    (call_script, "script_end_quest", "qst_bring_back_runaway_serfs")]],
  #[anyone,"lord_bring_back_runaway_serfs_failed_1b", [],
   # "Hah, now you reveal your true colours, traitor! Your words match your actions all too well. I should never have trusted you.", "close_window",
   # [(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-10),
    # (quest_get_slot, ":home_village", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    # (call_script, "script_change_player_relation_with_center",":home_village",6),
    # (call_script, "script_end_quest", "qst_bring_back_runaway_serfs"),
    # (assign, "$g_leave_encounter", 1),
    # ]],

[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_bring_back_runaway_serfs"),
                         (check_quest_concluded, "qst_bring_back_runaway_serfs"),
                         (assign, reg17, "$qst_bring_back_runaway_serfs_num_parties_returned")],
"You disappoint me, {playername}. There were 3 groups of slaves that I charged you to return. 3. Not {reg17}.\
 I suppose the ones who did come back shall have to work twice as hard to make up for those that got away.\
 As for your reward, {playername}, I'll only pay you for the slaves you returned, not the ones you let fly.\
 Here. Take it, and let this business be done.", "lord_runaway_serf_half_completed",
   [(store_mul, ":completion", "$qst_bring_back_runaway_serfs_num_parties_returned", 100),
    (val_div, ":completion", 3),
    (call_script, "script_objectionable_action", tmt_humanitarian, "str_round_up_serfs"),
    (call_script, "script_finish_quest", "qst_bring_back_runaway_serfs", ":completion")]],

[anyone|plyr,"lord_runaway_serf_half_completed", [], "Thank you, {s65}. You are indeed generous.", "lord_pretalk", []],
[anyone|plyr,"lord_runaway_serf_half_completed", [], "Bah, this proved to be a waste of my time.", "lord_pretalk", []],

  #[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         # (eq,":lords_quest","qst_deal_with_bandits_at_lords_village"),
                         # (check_quest_succeeded, "qst_deal_with_bandits_at_lords_village")],
   # "{playername}, I was told that you have crushed the bandits at my village of {s5}. Please know that I am most grateful to you for that.\
 # Please, let me pay the expenses of your campaign. Here, I hope these {reg14} denars will be adequate.", "lord_deal_with_bandits_completed",
   # [
       # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
       # (store_character_level, ":level", "trp_player"),
       # (store_mul, ":reward", ":level", 20),
       # (val_add, ":reward", 300),
       # (call_script, "script_troop_add_gold", "trp_player", ":reward"),
       # (add_xp_as_reward, 350),
       # (call_script, "script_end_quest", "qst_deal_with_bandits_at_lords_village"),
       # (assign, reg14, ":reward"),
       # (quest_get_slot, ":village", "qst_deal_with_bandits_at_lords_village", slot_quest_target_center),
       # (str_store_party_name, s5, ":village"),
       # ]],

  #[anyone|plyr, "lord_deal_with_bandits_completed", [],
   # "Not a problem, {s65}.", "lord_pretalk",[]],
  #[anyone|plyr, "lord_deal_with_bandits_completed", [],
   # "Glad to be of service.", "lord_pretalk",[]],
  #[anyone|plyr, "lord_deal_with_bandits_completed", [],
   # "It was mere child's play.", "lord_pretalk",[]],

  #[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         # (eq,":lords_quest","qst_deal_with_bandits_at_lords_village"),
                         # (check_quest_concluded, "qst_deal_with_bandits_at_lords_village")],
   # "Damn it, {playername}. I heard that you were unable to drive off the bandits from my village of {s5}, and thanks to you, my village now lies in ruins.\
 # Everyone said that you were a capable warrior, but appearently, they were wrong.", "lord_pretalk",
   # [
       # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
       # (call_script, "script_end_quest", "qst_deal_with_bandits_at_lords_village"),
       # (quest_get_slot, ":village", "qst_deal_with_bandits_at_lords_village", slot_quest_target_center),
       # (str_store_party_name, s5, ":village"),
       # ]],


[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq, ":lords_quest", "qst_deliver_cattle_to_army"),
                         (quest_get_slot, ":quest_target_item", "qst_deliver_cattle_to_army", slot_quest_target_item),
                         (store_item_kind_count, ":item_count", ":quest_target_item"),
                         #(check_quest_succeeded, "qst_deliver_cattle_to_army"),
                         (quest_get_slot, reg13, "qst_deliver_cattle_to_army", slot_quest_target_amount),
                         (ge, ":item_count", reg13),
                         (str_store_item_name, s4, ":quest_target_item")], 
"Ah, {playername}. I am pleased that you delivered {reg13} units of {s4}, as I requested. I'm impressed.", "lord_deliver_cattle_to_army_thank",
   [ (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
     (quest_get_slot, ":quest_target_item", "qst_deliver_cattle_to_army", slot_quest_target_item),
     (quest_get_slot, ":quest_target_amount", "qst_deliver_cattle_to_army", slot_quest_target_amount),
     (troop_remove_items, "trp_player", ":quest_target_item", ":quest_target_amount"),
     (store_item_value, ":item_value", ":quest_target_item"),
     (val_mul, ":item_value", 150), (val_div, ":item_value", 100), #50% profit
     (store_mul, ":reward", ":quest_target_amount", ":item_value"),
     #(call_script, "script_troop_add_gold", "trp_player", ":reward"),
     (call_script, "script_add_faction_rps", "$g_talk_troop_faction", ":reward"),
     (val_div, ":reward", 5),
     (add_xp_as_reward, ":reward"),
     (call_script, "script_increase_rank", "$g_talk_troop_faction", 8),
     (call_script, "script_end_quest", "qst_deliver_cattle_to_army"),
     #Reactivating follow army quest
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (setup_quest_text, "qst_follow_army"),
     (str_store_string, s2, "@Your mission is complete, {s9} wants you to resume following his army until further notice."),
     (call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop")]],

[anyone|plyr, "lord_deliver_cattle_to_army_thank", [], "Not a problem, {s65}.", "lord_pretalk",[]],
[anyone|plyr, "lord_deliver_cattle_to_army_thank", [], "Glad to be of service.", "lord_pretalk",[]],
  #[anyone|plyr, "lord_deliver_cattle_to_army_thank", [], "Mere child's play.", "lord_pretalk",[]],

[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq, ":lords_quest", "qst_scout_waypoints"),
                         (check_quest_succeeded, "qst_scout_waypoints"),
                         (str_store_party_name, s13, "$qst_scout_waypoints_wp_1"),
                         (str_store_party_name, s14, "$qst_scout_waypoints_wp_2"),
                         (str_store_party_name, s15, "$qst_scout_waypoints_wp_3")], 
"You make a good scout, {playername}. My runner just brought me your reports of the mission to {s13}, {s14} and {s15}. Well done.", "lord_scout_waypoints_thank",
   [ #TODO: Change reward
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
#     (call_script, "script_troop_add_gold", "trp_player", 100),
     (add_xp_as_reward, 100),
     (call_script, "script_increase_rank", "$g_talk_troop_faction", 6),
     (call_script, "script_end_quest", "qst_scout_waypoints"),
     #Reactivating follow army quest
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (setup_quest_text, "qst_follow_army"),
     (str_store_string, s2, "@Your mission is complete, {s9} wants you to resume following his army until further notice."),
     (call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop")]],

[anyone|plyr, "lord_scout_waypoints_thank", [], "A simple task, {s65}.", "lord_pretalk",[]],
[anyone|plyr, "lord_scout_waypoints_thank", [], "Nothing I couldn't handle.", "lord_pretalk",[]],
[anyone|plyr, "lord_scout_waypoints_thank", [], "My pleasure, sir.", "lord_pretalk",[]],
  


[anyone, "lord_start",
   [ (check_quest_active, "qst_follow_army"),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),
     (eq, "$g_random_army_quest", "qst_deliver_cattle_to_army"),
     (quest_get_slot, ":quest_target_item", "$g_random_army_quest", slot_quest_target_item),
     (quest_get_slot, ":quest_target_amount", "$g_random_army_quest", slot_quest_target_amount),
     (assign, reg3, ":quest_target_amount"),
     (str_store_item_name, s4, ":quest_target_item")],
"The army's supplies are dwindling too quickly, {playername}. I need you to bring me {reg3} units of {s4} so I can keep the troops fed. I care very little about where you get them, just bring them to me as soon as you can.", "lord_mission_told_deliver_cattle_to_army",[]],

[anyone|plyr,"lord_mission_told_deliver_cattle_to_army", [], "Very well, I can find you some {s4}.", "lord_mission_told_deliver_cattle_to_army_accepted",[]],
[anyone|plyr,"lord_mission_told_deliver_cattle_to_army", [], "Sorry, sir, I have other plans.", "lord_mission_told_deliver_cattle_to_army_rejected",[]],

[anyone,"lord_mission_told_deliver_cattle_to_army_accepted", [], "Excellent! You know what to do, {playername}, now get to it. I need that food sooner rather than later.", "close_window",
   [ (call_script,"script_stand_back"),
     (call_script, "script_end_quest", "qst_follow_army"),
     (quest_get_slot, ":quest_target_item", "$g_random_army_quest", slot_quest_target_item),
     (quest_get_slot, ":quest_target_amount", "$g_random_army_quest", slot_quest_target_amount),
     (str_store_troop_name_link, s13, "$g_talk_troop"),
     (assign, reg3, ":quest_target_amount"),
     (str_store_item_name, s4, ":quest_target_item"),
     (setup_quest_text, "$g_random_army_quest"),
     (str_store_string, s2, "@{s13} asked you to gather {reg3} units of {s4} and deliver them back to him."),
     (call_script, "script_start_quest", "$g_random_army_quest", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter",1)]],

[anyone, "lord_mission_told_deliver_cattle_to_army_rejected", [], "That . . . is unfortunate, {playername}. I shall have to find someone else who's up to the task. Please go now, I've work to do.", "close_window",
   [(call_script,"script_stand_back"),
   (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    (assign, "$g_leave_encounter",1),]],
  


[anyone,"lord_start",[(check_quest_active,"qst_report_to_army"),
                        (quest_slot_eq, "qst_report_to_army", slot_quest_target_troop, "$g_talk_troop")],
"Ah, you have arrived at last, {playername}. We've been expecting you. I hope you have brought with you troops of sufficient number and experience.", "lord_report_to_army_asked",[]],

[anyone|plyr,"lord_report_to_army_asked", [(quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
                                             (call_script, "script_party_count_fit_for_battle", "p_main_party"),
                                             (gt, reg0, ":quest_target_amount")], # +1 for player
"I have a company of good, hardened soldiers with me. We are ready to join you.", "lord_report_to_army_completed",[]],

[anyone|plyr,"lord_report_to_army_asked", [],
   "I don't have the sufficient number of troops yet. I will need some more time.", "lord_report_to_army_continue",[]],

[anyone,"lord_report_to_army_completed", [], "Excellent. I will send the word when I have a task for you. For the moment, just follow us and stay close. We'll be moving soon.", "close_window",[
     (call_script,"script_stand_back"),
	 (call_script, "script_increase_rank", "$g_talk_troop_faction", 1),
     (call_script, "script_end_quest", "qst_report_to_army"),
     (quest_set_slot, "qst_report_to_army", slot_quest_giver_troop, "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
     #Activating follow army quest
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (setup_quest_text, "qst_follow_army"),
     (str_store_string, s2, "@{s9} wants you to follow his army until further notice."),
     (call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop"),
     #(assign, "$g_player_follow_army_warnings", 0),
     (assign, "$g_leave_encounter", 1)]],

[anyone,"lord_report_to_army_continue", [], "Then you'd better hurry. We'll be moving out soon against the enemy and I need every able hand we can muster.", "close_window",
   [(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)]],   #Must be closed because of not letting player to terminate this quest on the general conversation

[anyone, "lord_start",
   [ (check_quest_active, "qst_follow_army"),
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"),
     (eq, "$g_random_army_quest", "qst_scout_waypoints"),
     (str_store_party_name, s13, "$qst_scout_waypoints_wp_1"),
     (str_store_party_name, s14, "$qst_scout_waypoints_wp_2"),
     (str_store_party_name, s15, "$qst_scout_waypoints_wp_3")],
"{playername}, I need a volunteer to scout the area. We're sorely lacking in information,\
 and I simply must have a better picture of the situation before we can proceed.\
 I want you to go to {s13}, {s14} and {s15} and report back whatever you find.", "lord_mission_told_scout_waypoints",[]],

[anyone|plyr, "lord_mission_told_scout_waypoints", [], "You've found your volunteer, sir.", "lord_mission_told_scout_waypoints_accepted",[]],
[anyone|plyr, "lord_mission_told_scout_waypoints", [], "I fear I must decline.", "lord_mission_told_scout_waypoints_rejected",[]],

[anyone,"lord_mission_told_scout_waypoints_accepted", [], 
"Good! Simply pass near {s13}, {s14} and {s15} and check out what's there. Make a note of anything you find and return to me as soon as possible.", "close_window",
   [ (call_script,"script_stand_back"),
     (call_script, "script_end_quest", "qst_follow_army"),
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (str_store_party_name_link, s13, "$qst_scout_waypoints_wp_1"),
     (str_store_party_name_link, s14, "$qst_scout_waypoints_wp_2"),
     (str_store_party_name_link, s15, "$qst_scout_waypoints_wp_3"),
     (setup_quest_text, "$g_random_army_quest"),
     (str_store_string, s2, "@{s9} asked you to scout {s13}, {s14} and {s15}, then report back."),
     (call_script, "script_start_quest", "$g_random_army_quest", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter",1)]],

[anyone,"lord_mission_told_scout_waypoints_rejected", [], 
"Hm. I'm disappointed, {playername}. Very disappointed. We'll talk later, I need to go and find somebody to scout for us.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],


  

##
##[anyone,"lord_start",[(check_quest_active,"qst_rescue_lady_under_siege"),
##                        (quest_slot_eq, "qst_rescue_lady_under_siege", slot_quest_target_troop, "$g_talk_troop"),
##                        (quest_slot_eq, "qst_rescue_lady_under_siege", slot_quest_current_state, 1)],
##   "I heard that you have rescued my {s7} from the siege of {s5} and brought her to safety.\
## I am in your debt for this {playername}. Thank you.", "lord_generic_mission_completed",
##   [(quest_get_slot, ":quest_object_troop", "qst_rescue_lady_under_siege", slot_quest_object_troop),
##    (try_begin),
##      (troop_slot_eq, "$g_talk_troop", slot_troop_daughter, ":quest_object_troop"),
##      (str_store_string, s7, "str_daughter"),
##    (else_try),
##      (str_store_string, s7, "str_wife"),
##    (try_end),
##    (remove_member_from_party, ":quest_object_troop"),
##    (try_begin),
##      (is_between, "$g_encountered_party", centers_begin, centers_end),#Lord might be in wilderness
##      (troop_set_slot, ":quest_object_troop", slot_troop_cur_center, "$g_encountered_party"),
##    (try_end),
##    (call_script, "script_finish_quest", "qst_rescue_lady_under_siege", 100),
##    (call_script, "script_change_player_relation_with_troop","$g_talk_troop", 4),    
##    ]],
##
##### TODO: QUESTS COMMENT OUT END

[anyone,"lord_generic_mission_thank", [
    (try_begin),
      (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
      (str_store_string, s4, "@You have been most helpful, {playername}. My thanks."),
    (else_try),
      (str_store_string, s4, "@You are a good servant, {playername}. Carry on."),
    (try_end),
    ],
"{s4}", "lord_generic_mission_completed",[]],
[anyone,"lord_generic_mission_thank_extra", [
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1), # bonus goodwill
    (try_begin),
      (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
      (str_store_string, s4, "@Superb work, {playername}. I admire your attitude."),
    (else_try),
      (str_store_string, s4, "@Your efficiency is pleasing, {playername}. Continue and you will go far."),
    (try_end),
    ],
"{s4}", "lord_generic_mission_completed",[]],

[anyone|plyr,"lord_generic_mission_completed", [
    (try_begin),
      (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
      (str_store_string, s4, "@It was an honour to serve."),
    (else_try),
      (str_store_string, s4, "@Your wish is my command."),
    (try_end),
    ],
"{s4}", "lord_pretalk",[]],

##[anyone|plyr,"lord_generic_mission_failed", [],
##   "I'm sorry I failed you sir. It won't happen again.", "lord_pretalk",
##   [(store_partner_quest,":lords_quest"),
##    (call_script, "script_finish_quest", ":lords_quest"),
##    ]],
  
# [anyone,"lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                         # (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         # (troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
                         # (gt, ":cur_debt", 0),
                         # (assign, reg1, ":cur_debt")],
# "I think you owe me {reg1} RPs, {playername}. Do you intend to pay your debt anytime soon?", "lord_pay_debt_2",[]],

# [anyone|plyr, "lord_pay_debt_2", [(troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
                                    # (store_troop_gold, ":cur_gold", "trp_player"),
                                    # (le, ":cur_debt", ":cur_gold")],
# "That is why I came, {s65}. Here it is, every denar I owe you.", "lord_pay_debt_3_1", [
	# (troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
	# (troop_remove_gold, "trp_player", ":cur_debt"),
	# (troop_set_slot, "$g_talk_troop", slot_troop_player_debt, 0)]],

# [anyone|plyr, "lord_pay_debt_2", [], "Alas, I don't have sufficient funds, {s65}. But I'll pay you soon enough.", "lord_pay_debt_3_2", []],
# [anyone, "lord_pay_debt_3_1", [], "Ah, excellent. You are a {man/woman} of honour, {playername}. I am satisfied, your debt to me has been paid in full.", "lord_pretalk", []],
# [anyone, "lord_pay_debt_3_2", [], "Well, don't keep me waiting much longer.", "lord_pretalk", []],
   
[anyone,"lord_start", [(party_slot_eq, "$g_encountered_party",slot_town_lord, "$g_talk_troop"),#we are talking to Town's Lord.
                         (ge,"$g_talk_troop_faction_relation",0),
						 (str_store_faction_name, s14, "$g_talk_troop_faction"),
                         (neq, "$g_ransom_offer_rejected", 1),
                         (lt, "$g_encountered_party_2", 0), #town is not under siege
                         (hero_can_join_as_prisoner, "$g_encountered_party"),
                         (store_random_in_range, ":random_no", 0, 100),
                         (lt, ":random_no", 10),#start this conversation with a 10% chance
                         (party_get_num_prisoner_stacks,":num_prisoner_stacks","p_main_party"),
                         (assign, "$prisoner_lord_to_buy", -1),
                         (try_for_range,":i_pris_stack",0,":num_prisoner_stacks"),
                           (party_prisoner_stack_get_troop_id, ":t_id", "p_main_party", ":i_pris_stack"),
                           (troop_slot_eq, ":t_id", slot_troop_occupation, slto_kingdom_hero),
                           (store_troop_faction, ":fac", ":t_id"),
                           (store_relation, ":rel", ":fac", "$g_talk_troop_faction"),
                           (lt,  ":rel", 0),
                           (assign, "$prisoner_lord_to_buy", ":t_id"),
                         (try_end),
                         (gt, "$prisoner_lord_to_buy", 0), #we have a prisoner lord.
                         (assign, ":continue", 1),
                         (try_begin),
                           (check_quest_active, "qst_capture_enemy_hero"),
                           #(store_troop_faction, ":prisoner_faction", "$prisoner_lord_to_buy"),
                           #(quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":prisoner_faction"),
                           (assign, ":continue", 0),
                         (try_end),
                         (eq, ":continue", 1),
                         (str_store_troop_name, s3, "$prisoner_lord_to_buy"),
                         (assign, reg5, "$prisoner_lord_to_buy"),
                         (call_script, "script_calculate_ransom_amount_for_troop", "$prisoner_lord_to_buy"),
                         (assign, reg14, reg0),
                         (val_div, reg14, 2),
                         (assign, "$temp", reg14)],
"I heard that you have captured our enemy {s3} and he is with you at the moment. Good job!^\
 Leave him to us, there is a lot of information which we need to extract from him..."+promise_reg14_rp_of_s14 , "lord_buy_prisoner", []],

[anyone|plyr,"lord_buy_prisoner", [], "Well, he is all yours.", "lord_buy_prisoner_accept", []],
[anyone|plyr,"lord_buy_prisoner", [], "I fear I have other plans for him.", "lord_buy_prisoner_deny", [(assign, "$g_ransom_offer_rejected", 1),]],

[anyone,"lord_buy_prisoner_accept", [],
"Excellent!\
 I'll send my men to take him to our prison with due haste. This will surely help our cause.", "lord_pretalk", [
     (remove_troops_from_prisoners,  "$prisoner_lord_to_buy", 1),
     (call_script, "script_add_faction_rps", "$g_talk_troop_faction", "$temp"),
     #(call_script, "script_troop_add_gold", "trp_player", "$temp"),
     (party_add_prisoners, "$g_encountered_party", "$prisoner_lord_to_buy", 1),
     #(troop_set_slot, "$prisoner_lord_to_buy", slot_troop_is_prisoner, 1),
     (troop_set_slot, "$prisoner_lord_to_buy", slot_troop_prisoner_of_party, "$g_encountered_party")]],

[anyone,"lord_buy_prisoner_deny", [], "Too bad, he would have been precious for us, {playername}.", "lord_pretalk", []],

#TLD: your king gives you a faction intro when you first meet him
[anyone,"lord_start", [
        (faction_slot_eq,"$players_kingdom",slot_faction_leader,"$g_talk_troop"),
        (eq, "$g_talk_troop_met", 0)],
"Ah, welcome, {s24}.^You should already know that {s12}. \
Your duty is to help in our struggle, {playername}. When you prove yourself worthy of my confidence [level {reg1}], I will also allow you access to that chest over there."
#^As your {s15}, I grant you a simple mount to help you in your travels.
		, "lord_pretalk",[
          (assign, ":num_theater_enemies", 0),
          (faction_get_slot, ":faction_theater", "$g_encountered_party_faction", slot_faction_active_theater),
          (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
            (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
            (store_relation, ":cur_relation", ":cur_faction", "$g_talk_troop_faction"),
            (lt, ":cur_relation", 0),
            (faction_slot_eq, ":cur_faction", slot_faction_active_theater, ":faction_theater"),
            (try_begin),
              (eq, ":num_theater_enemies", 0),
              (str_store_faction_name_link, s13, ":cur_faction"),
            (else_try),
              (eq, ":num_theater_enemies", 1),
              (str_store_faction_name_link, s11, ":cur_faction"),
              (str_store_string, s13, "@{s11} and {s13}"),
            (else_try),
              (str_store_faction_name_link, s11, ":cur_faction"),
              (str_store_string, s13, "@{s11}, {s13}"),
            (try_end),
            (val_add, ":num_theater_enemies", 1),
          (try_end),
          (try_begin),
            (gt, ":num_theater_enemies", 0),
            (str_store_string, s12, "@we are fighting against {s13}"),
          (else_try),
            (str_store_string, s12, "@we are not fighting anyone at the moment"),
          (try_end),
          (str_store_troop_name_plural, s15,"$g_talk_troop"), #GA: plural name for kings contains referral to them
          (call_script, "script_get_rank_title_to_s24", "$players_kingdom"), #in s24
          # (try_begin),
            # (eq, "$player_looks_like_an_orc",1),
            # (troop_add_item, "trp_player", "itm_warg_1b", imod_swaybacked),
          # (else_try),
            # (troop_add_item, "trp_player", "itm_sumpter_horse", imod_swaybacked),
          # (try_end),
          (assign, reg1, tld_player_level_to_own_chest)]],

[anyone,"lord_start", [], "What is it?", "lord_talk",[]],
[anyone,"lord_pretalk", [], "Anything else?", "lord_talk",[]],
#[anyone,"hero_pretalk", [], "Anything else?", "lord_talk",[]],

##### TODO: QUESTS COMMENT OUT BEGIN

[anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                            (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                            (check_quest_active,"qst_lend_companion"),
                            (quest_slot_eq, "qst_lend_companion", slot_quest_giver_troop, "$g_talk_troop"),
                            (store_current_day, ":cur_day"),
                            (quest_get_slot, ":quest_target_amount", "qst_lend_companion", slot_quest_target_amount),
                            (ge, ":cur_day", ":quest_target_amount"),
                            (quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
                            (str_store_troop_name,s14,":quest_target_troop"),
                            (troop_get_type, reg3, ":quest_target_troop"),
                            (try_begin),
                              (gt, reg3, 1), #MV: non-humans are male
                              (assign, reg3, 0),
                            (try_end)],
"I should like {s14} returned to me, {s65}, if you no longer require {reg3?her:his} services.", "lord_lend_companion_end", []],

[anyone,"lord_lend_companion_end",[(neg|hero_can_join, "p_main_party")],
"You've too many men in your company already, {playername}. You could not lead any more at the moment.", "lord_pretalk", []],

[anyone,"lord_lend_companion_end",[],
"Certainly, {playername}. {reg3?She:He} is a bright {reg3?girl:fellow}, you're a lucky commander to have such worthy companions.", "lord_pretalk", [
    (quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
    (party_add_members, "p_main_party", ":quest_target_troop", 1),
    # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
    # (add_xp_as_reward, 100),
    (call_script, "script_finish_quest", "qst_lend_companion", 100),
    (str_store_troop_name,s14,":quest_target_troop"),
    (troop_get_type, reg3, ":quest_target_troop"),
    (try_begin),
      (gt, reg3, 1), #MV: non-humans are male
      (assign, reg3, 0),
    (try_end)]],
   
  #[anyone|plyr,"lord_talk",[(check_quest_active,"qst_collect_debt"),
                            # (quest_slot_eq,  "qst_collect_debt", slot_quest_current_state, 0),
                            # (quest_get_slot, ":quest_target_troop", "qst_collect_debt", slot_quest_target_troop),
                            # (eq,"$g_talk_troop",":quest_target_troop"),
                            # (quest_get_slot, ":quest_giver_troop", "qst_collect_debt", slot_quest_giver_troop),
                            # (str_store_troop_name,1,":quest_giver_troop")],
   # "I've come to collect the debt you owe to {s1}.", "lord_ask_to_collect_debt",
   # [(assign, "$g_convince_quest", "qst_collect_debt")]],

  #[anyone,"lord_ask_to_collect_debt", [],  "Oh. Well, {s1} did lend me some silver a ways back,\
 # but I've done him many favours in the past and I consider that money as my due payment.", "lord_ask_to_collect_debt_2",[]],
  #[anyone|plyr,"lord_ask_to_collect_debt_2", [],  "{s1} considers it a debt. He asked me to speak to you on his behalf.", "convince_begin",[]],
  #[anyone|plyr,"lord_ask_to_collect_debt_2", [],  "Then I will not press the matter any further.", "lord_pretalk",[]],


  #[anyone,"convince_accept",[(check_quest_active, "qst_collect_debt"),
                             # (quest_slot_eq, "qst_collect_debt", slot_quest_target_troop, "$g_talk_troop"),
                             # (quest_get_slot, ":quest_giver_troop", "qst_collect_debt", slot_quest_giver_troop),
                             # (str_store_troop_name,s8,":quest_giver_troop"),
                             # (quest_get_slot, reg10, "qst_collect_debt", slot_quest_target_amount)],
   # "My debt to {s8} has long been overdue and was a source of great discomfort to me.\
 # Thank you for accepting to take the money to him.\
 # Please give him these {reg10} denars and thank him on my behalf.", "close_window",
   # [(call_script, "script_troop_add_gold", "trp_player", reg10),
    # (quest_set_slot,  "qst_collect_debt", slot_quest_current_state, 1),
    # (call_script, "script_succeed_quest", "qst_collect_debt"),
    # (assign, "$g_leave_encounter", 1),
    # ]],


  #[anyone|plyr,"lord_talk",[(check_quest_active,"qst_persuade_lords_to_make_peace"),
                            # (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
                            # (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
                            # (this_or_next|eq, ":quest_target_troop", "$g_talk_troop"),
                            # (eq, ":quest_object_troop", "$g_talk_troop"),
                            # (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                            # (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
                            # (str_store_faction_name, s12, ":quest_target_faction"),
                            # (str_store_faction_name, s13, ":quest_object_faction"),
                            # ],
   # "Please, {s64}, it's time to end this war between {s12} and {s13}.", "lord_ask_to_make_peace",
   # [(assign, "$g_convince_quest", "qst_persuade_lords_to_make_peace")]],

  #[anyone,"lord_ask_to_make_peace", [], "Eh? I'm not sure I heard you right, {playername}.\
 # War is not easily forgotten by either side of the conflict, and I have a very long memory.\
 # Why should I take any interest in brokering peace with those dogs?", "lord_ask_to_make_peace_2",[]],

  #[anyone|plyr,"lord_ask_to_make_peace_2", [],  "Perhaps I can talk you into it...", "convince_begin",[]],
  #[anyone|plyr,"lord_ask_to_make_peace_2", [],  "Never mind, peace can wait for now.", "lord_pretalk",[]],

  #[anyone,"convince_accept",[(check_quest_active, "qst_persuade_lords_to_make_peace"),
                             # (this_or_next|quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, "$g_talk_troop"),
                             # (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, "$g_talk_troop"),
                             # (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
                             # (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                             # (str_store_faction_name, s12, ":quest_object_faction"),
                             # (str_store_faction_name, s13, ":quest_target_faction"),
                             # (try_begin), # store name of other faction
                               # (eq,":quest_object_faction","$g_talk_troop_faction"),
                               # (str_store_faction_name, s14, ":quest_target_faction"),
                               # (else_try),
                               # (str_store_faction_name, s14, ":quest_object_faction"),
                             # (try_end),
                             # ],
   # "You... have convinced me, {playername}. Very well then, you've my blessing to bring a peace offer to {s14}. I cannot guarantee they will accept it, but on the off-chance they do, I will stand by it.", "close_window",
   # [(store_mul, ":new_value", "$g_talk_troop", -1),
    # (try_begin),
      # (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, "$g_talk_troop"),
      # (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":new_value"),
    # (else_try),
      # (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":new_value"),
    # (try_end),
    # (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_convince_value, 1500),#reseting convince value for the second persuasion
    # (assign, "$g_leave_encounter", 1),
    # (neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, 0),
    # (neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, 0),
    # (call_script, "script_succeed_quest", "qst_persuade_lords_to_make_peace"),
    # ]],


##
##
##[anyone|plyr,"lord_talk",[(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                            (check_quest_active,"qst_bring_reinforcements_to_siege"),
##                             (quest_get_slot, ":quest_target_troop", "qst_bring_reinforcements_to_siege", slot_quest_target_troop),
##                             (eq,"$g_talk_troop",":quest_target_troop"),
##                             (quest_get_slot, ":quest_giver_troop", "qst_bring_reinforcements_to_siege", slot_quest_giver_troop),
##                             (quest_get_slot, ":quest_target_amount", "qst_bring_reinforcements_to_siege", slot_quest_target_amount),
##                             (quest_get_slot, ":quest_object_troop", "qst_bring_reinforcements_to_siege", slot_quest_object_troop),
##                             (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_object_troop"),
##                             (ge, ":num_companions", ":quest_target_amount"),
##                             (str_store_troop_name,1,":quest_giver_troop"),
##                             (assign, reg1, ":quest_target_amount"),
##                             (str_store_troop_name,2,":quest_object_troop")],
##   "Sir, {s1} ordered me to bring {reg1} {s2} to reinforce your siege.", "lord_reinforcement_brought",
##   [(quest_get_slot, ":quest_target_amount", "qst_bring_reinforcements_to_siege", slot_quest_target_amount),
##    (quest_get_slot, ":quest_target_party", "qst_bring_reinforcements_to_siege", slot_quest_target_party),
##    (quest_get_slot, ":quest_object_troop", "qst_bring_reinforcements_to_siege", slot_quest_object_troop),
##    (party_remove_members, "p_main_party", ":quest_object_troop", ":quest_target_amount"),
##    (party_add_members, ":quest_target_party", ":quest_object_troop", ":quest_target_amount"),
##    (call_script, "script_finish_quest", "qst_bring_reinforcements_to_siege", 100),
##    ]],
##
##[anyone|plyr,"lord_talk",[(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                            (check_quest_active,"qst_bring_reinforcements_to_siege"),
##                             (quest_get_slot, ":quest_target_troop", "qst_bring_reinforcements_to_siege", slot_quest_target_troop),
##                             (eq,"$g_talk_troop",":quest_target_troop"),
##                             (quest_get_slot, ":quest_giver_troop", "qst_bring_reinforcements_to_siege", slot_quest_giver_troop),
##                             (quest_get_slot, ":quest_target_amount", "qst_bring_reinforcements_to_siege", slot_quest_target_amount),
##                             (quest_get_slot, ":quest_object_troop", "qst_bring_reinforcements_to_siege", slot_quest_object_troop),
##                             (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_object_troop"),
##                             (lt, ":num_companions", ":quest_target_amount"),
##                             (gt, ":num_companions", 0),
##                             (str_store_troop_name,1,":quest_giver_troop"),
##                             (assign, reg1, ":quest_target_amount"),
##                             (str_store_troop_name,2,":quest_object_troop")],
##   "Sir, {s1} ordered me to bring {reg1} {s2} as a reinforcement to your siege, but unfortunately I lost some of them during my expedition.", "lord_reinforcement_brought_some",
##   [(quest_get_slot, ":quest_target_amount", "qst_bring_reinforcements_to_siege", slot_quest_target_amount),
##    (quest_get_slot, ":quest_target_party", "qst_bring_reinforcements_to_siege", slot_quest_target_party),
##    (quest_get_slot, ":quest_object_troop", "qst_bring_reinforcements_to_siege", slot_quest_object_troop),
##    (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_object_troop"),
##    (party_remove_members, "p_main_party", ":quest_object_troop", ":num_companions"),
##    (party_add_members, ":quest_target_party", ":quest_object_troop", ":num_companions"),
##    (assign, ":percentage_completed", 100),
##    (val_mul, ":percentage_completed", ":num_companions"),
##    (val_div, ":percentage_completed", ":quest_target_amount"),
##    (call_script, "script_finish_quest", "qst_bring_reinforcements_to_siege", ":percentage_completed"),
##     ]],
##
##[anyone,"lord_reinforcement_brought", [], "Well done {playername}. These men will no doubt be very useful. I will speak to {s1} of your help.", "lord_pretalk",[]],
##[anyone,"lord_reinforcement_brought_some", [], "That's not quite good enough {playername}. But I suppose it is better than no reinforcements at all. Whatever, I'll tell {s1} you tried your best.", "lord_pretalk",[]],
##

  #[anyone|plyr,"lord_talk",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                            # (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                            # (check_quest_active,"qst_duel_for_lady"),
                            # (neg|check_quest_concluded,"qst_duel_for_lady"),
                            # (quest_slot_eq, "qst_duel_for_lady", slot_quest_target_troop, "$g_talk_troop"),
                            # (quest_get_slot, ":quest_giver_troop", "qst_duel_for_lady", slot_quest_giver_troop),
                            # (str_store_troop_name,1,":quest_giver_troop")],
   # "I want you to take back your accusations against {s1}.", "lord_challenge_duel_for_lady", []],
  #[anyone,"lord_challenge_duel_for_lady", [], "What accusations?\
 # Everyone knows that she beds her stable boys and anyone else she can lay hands on while her husband is away.\
 # I merely repeat the words of many.", "lord_challenge_duel_for_lady_2",[]],
  #[anyone|plyr,"lord_challenge_duel_for_lady_2", [], "You will recant these lies, sirrah, or prove them against my sword!", "lord_challenge_duel_for_lady_3",[]],
  #[anyone|plyr,"lord_challenge_duel_for_lady_2", [], "If you say so...", "lord_pretalk",[]],
  #[anyone,"lord_challenge_duel_for_lady_3", [], "You are challenging me to a duel? How droll!\
 # As you wish, {playername}, it will be good sport to bash your head in.", "close_window",
   # [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -20),
    # (assign, "$g_leave_encounter", 1),
    # (try_begin),
      # (is_between, "$g_encountered_party", centers_begin, centers_end),
      # (party_get_slot, ":arena_scene", "$g_encountered_party", slot_town_arena),
    # (else_try),
      # (assign, ":closest_dist", 100000),
      # (assign, ":closest_town", -1),
      # (try_for_range, ":cur_town", centers_begin, centers_end),
        # (store_distance_to_party_from_party, ":dist", ":cur_town", "p_main_party"),
        # (lt, ":dist", ":closest_dist"),
        # (assign, ":closest_dist", ":dist"),
        # (assign, ":closest_town", ":cur_town"),
      # (try_end),
      # (party_get_slot, ":arena_scene", ":closest_town", slot_town_arena),
    # (try_end),
    # (modify_visitors_at_site, ":arena_scene"),
    # (reset_visitors),
    # (set_visitor, 0, "trp_player"),
    # (set_visitor, 1, "$g_talk_troop"),
    # (set_jump_mission, "mt_arena_challenge_fight"),
    # (jump_to_scene, ":arena_scene"),
    # (try_begin),
      # (neq, "$talk_context", tc_court_talk),
      # (jump_to_menu, "mnu_arena_duel_fight"),
    # (try_end),
    # ]],

  
[anyone|plyr,"lord_talk",[(check_quest_active,"qst_deliver_message"),
                             (quest_get_slot, ":quest_target_troop", "qst_deliver_message", slot_quest_target_troop),
                             (eq,"$g_talk_troop",":quest_target_troop"),
                             (quest_get_slot, ":quest_giver_troop", "qst_deliver_message", slot_quest_giver_troop),
                             (str_store_troop_name,s9,":quest_giver_troop")],
"I bring a message from {s9}.", "lord_message_delivered", []],

[anyone,"lord_message_delivered", [], "{s4}", "lord_pretalk",[
     (call_script, "script_finish_quest", "qst_deliver_message", 100),
     #(call_script, "script_end_quest", "qst_deliver_message"),
     (quest_get_slot, ":quest_giver", "qst_deliver_message", slot_quest_giver_troop),
     (str_store_troop_name,s9,":quest_giver"),
     (try_begin),
       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
       (str_store_string, s4, "@Oh? Let me see that...\
 Well well well! It was good of you to bring me this, {playername}. Take my seal as proof that I've received it,\
 and give my regards to {s9} when you see him again."),
     (else_try),
       (str_store_string, s4, "@Give me that!\
 Hrmph! Good that you brought me this, {playername}, you are a useful servant. Tell {s9} to employ you more often."),
     (try_end),
     #(call_script, "script_change_player_relation_with_troop", ":quest_giver", 1),
     (quest_get_slot, ":reward", "qst_deliver_message", slot_quest_gold_reward),
     (call_script, "script_add_faction_rps", "$g_talk_troop_faction", ":reward"),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1)]],

[anyone|plyr,"lord_talk",[(check_quest_active,"qst_deliver_message_to_enemy_lord"),
                            (quest_get_slot, ":quest_target_troop", "qst_deliver_message_to_enemy_lord", slot_quest_target_troop),
                            (eq,"$g_talk_troop",":quest_target_troop"),
                            (quest_get_slot, ":quest_giver_troop", "qst_deliver_message_to_enemy_lord", slot_quest_giver_troop),
                            (str_store_troop_name,s9,":quest_giver_troop")],
"I bring a message from {s9}.", "lord_message_delivered_enemy", []],

[anyone,"lord_message_delivered_enemy", [], "{s4}", "close_window",[
     (call_script,"script_stand_back"),
	 (try_begin),
       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
       (str_store_string, s4, "@What? Let me see that... Hmmm. It was good of you to bring me this, {playername}. Now begone."),
     (else_try),
       (str_store_string, s4, "@Give me that! Hrmph! You are a useful servant to your masters, {playername}, but all of you will be dead before long. Not now though, so scurry off."),
     (try_end),
     #(call_script, "script_end_quest", "qst_deliver_message_to_enemy_lord"),
     (call_script, "script_finish_quest", "qst_deliver_message_to_enemy_lord", 100),
     #(quest_get_slot, ":quest_giver", "qst_deliver_message_to_enemy_lord", slot_quest_giver_troop),
     #(call_script, "script_change_player_relation_with_troop", ":quest_giver", 3),
     #(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter", 1)]],

  #[anyone|plyr,"lord_talk", [(check_quest_active,"qst_deliver_message_to_prisoner_lord"),
                             # (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, "$g_talk_troop"),
                             # (quest_get_slot, ":quest_giver_troop", "qst_deliver_message_to_prisoner_lord", slot_quest_giver_troop),
                             # (str_store_troop_name, s11, ":quest_giver_troop")],
   # "I bring a message from {s11}.", "lord_deliver_message_prisoner",
   # [
     # #TODO: Add reward
     # (call_script, "script_end_quest", "qst_deliver_message_to_prisoner_lord"),
     # ]],

  #[anyone,"lord_deliver_message_prisoner", [], "Can it be true?\
 # Oh, thank you kindly, {playername}! You have brought hope and some small ray of light to these bleak walls.\
 # Perhaps one day I will be able to repay you.", "lord_deliver_message_prisoner_2",[]],
  #[anyone|plyr,"lord_deliver_message_prisoner_2", [], " 'Twas the least I could do, {s65}.", "lord_deliver_message_prisoner_2a",[]],
  #[anyone,"lord_deliver_message_prisoner_2a", [], "You've no idea how grateful I am, {playername}. A thousand thanks and more.", "close_window",[]],
  #[anyone|plyr,"lord_deliver_message_prisoner_2", [], "Worry not, {s65}. You'll have ample opportunity once you are free again.", "lord_deliver_message_prisoner_2b",[]],
  #[anyone,"lord_deliver_message_prisoner_2b", [], "Hah, of course, {playername}. My eternal thanks go with you.", "close_window",[]],

  #[anyone|plyr,"lord_talk", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 1),
                             # (troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             # (check_quest_active,"qst_rescue_lord_by_replace"),
                             # (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, "$g_talk_troop"),
                             # (neg|check_quest_succeeded, "qst_rescue_lord_by_replace")],
   # "Fear not, I am here to rescue you.", "lord_rescue_by_replace_offer",[]],
  #[anyone,"lord_rescue_by_replace_offer", [],
   # "By God, are you serious? What is your plan?", "lord_rescue_by_replace_offer_2",[]],
  #[anyone|plyr,"lord_rescue_by_replace_offer_2", [],
   # "A simple ruse, {s65}. If we exchange garments, I shall take your place here in prison,\
 # while you make your escape disguised as myself.\
 # I paid the guards a handsome bribe, with which I am sure they have already purchased half the wine stocks of the nearest tavern.\
 # With some luck they'll soon get so drunk they'd have trouble\
 # recognising their own mothers, let alone telling one of us from the other.\
 # At least not until you are safely away.", "lord_rescue_by_replace_offer_3",[]],
  #[anyone,"lord_rescue_by_replace_offer_3", [],
   # "Hmm, it might just work... But what of you, my {friend/lady}? The guards won't take kindly to this trickery.\
 # You may end up spending some time in this cell yourself.", "lord_rescue_by_replace_offer_4",[]],
  #[anyone|plyr,"lord_rescue_by_replace_offer_4", [],
   # "Not to worry, {s65}. The place is already starting to grow on me.", "lord_rescue_by_replace_offer_5a",[]],
  #[anyone|plyr,"lord_rescue_by_replace_offer_4", [],
   # "I shall be fine as long there is an ample reward waiting at the end.", "lord_rescue_by_replace_offer_5b",[]],
  #[anyone,"lord_rescue_by_replace_offer_5a",[],
   # "You are a brave soul indeed. I won't forget this.", "lord_rescue_by_replace_offer_6",[]],
  #[anyone,"lord_rescue_by_replace_offer_5b",[],
   # "Of course, my {friend/lady}, of course! Come to me when you have regained your freedom,\
 # and perhaps I shall be able to repay the debt I owe you.", "lord_rescue_by_replace_offer_6",[]],
  #[anyone|plyr,"lord_rescue_by_replace_offer_6",[],
   # "Quickly, {s65}, let us change garments. It is past time you were away from here.", "close_window",
   # [(call_script, "script_succeed_quest", "qst_rescue_lord_by_replace"),
    # (quest_get_slot, ":quest_target_troop", "qst_rescue_lord_by_replace", slot_quest_target_troop),
    # (quest_get_slot, ":quest_target_center", "qst_rescue_lord_by_replace", slot_quest_target_center),
    # (party_remove_prisoners, ":quest_target_center", ":quest_target_troop", 1),
    # #(troop_set_slot, ":quest_target_troop", slot_troop_is_prisoner, 0),
    # (troop_set_slot, ":quest_target_troop", slot_troop_prisoner_of_party, -1),
    # (assign, "$auto_menu", -1),
    # (assign, "$capturer_party", "$g_encountered_party"),
    # (jump_to_menu, "mnu_captivity_rescue_lord_taken_prisoner"),
    # (finish_mission),
    # ]],

##  
##[anyone|plyr,"lord_talk", [(check_quest_active, "qst_deliver_message_to_lover"),
##                             (troop_get_slot, ":cur_daughter", "$g_talk_troop", slot_troop_daughter),
##                             (quest_slot_eq, "qst_deliver_message_to_lover", slot_quest_target_troop, ":cur_daughter"),
##                             (quest_get_slot, ":troop_no", "qst_deliver_message_to_lover", slot_quest_giver_troop),
##                             (str_store_troop_name, 3, ":troop_no"),
##                             (str_store_troop_name, 4, ":cur_daughter")],
##   "My lord, {s3} asked me to give this letter to your daughter, but I think you should read it first.", "lord_deliver_message_to_lover_tell_father",[]],
##
##[anyone,"lord_deliver_message_to_lover_tell_father", [],
##   "That swine called {s3} is trying to approach my daughter eh? You have made the right decision by bringing this letter to me. I'll have a long talk with {s4} about it.", "lord_pretalk",
##   [(add_xp_as_reward, 200),
##    (call_script, "script_troop_add_gold", "trp_player", 1000),
##    (quest_get_slot, ":quest_giver", "qst_deliver_message_to_lover", slot_quest_giver_troop),
##    (quest_get_slot, ":target_troop", "qst_deliver_message_to_lover", slot_quest_target_troop),
##    (call_script, "script_change_player_relation_with_troop", ":quest_giver", -20),
##    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
##    (call_script, "script_change_player_relation_with_troop", ":target_troop", -10),
##    (call_script, "script_end_quest", "qst_deliver_message_to_lover"),
##    #Adding betrayal to the quest giver
##    (troop_set_slot, ":quest_giver", slot_troop_last_quest, "qst_deliver_message_to_lover"),
##    (troop_set_slot, ":quest_giver", slot_troop_last_quest_betrayed, 1)]],
##
##
##### TODO: QUESTS COMMENT OUT END

[anyone|plyr,"lord_talk", [(store_partner_quest,":lords_quest"),
                             (ge,":lords_quest",0)],
"About the task you gave me...", "lord_active_mission_1",[]],

# [anyone|plyr,"lord_talk", [(faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader, "$g_talk_troop"),
                             # (eq, "$players_kingdom", "$g_talk_troop_faction"),
                             # (gt, "$mercenary_service_accumulated_pay", 0)],
# "{s67}, I humbly request the weekly payment for my service.", "lord_pay_mercenary",[]],

# [anyone,"lord_pay_mercenary", [(assign, reg8, "$mercenary_service_accumulated_pay")],
# "Hmm, let me see... According to my ledgers, we owe you {reg8} RPs for your work. Here you are.", "lord_pay_mercenary_2",
   # [(troop_add_gold, "trp_player", "$mercenary_service_accumulated_pay"),
    # (assign, "$mercenary_service_accumulated_pay", 0)]],
# [anyone|plyr,"lord_pay_mercenary_2", [], "Thank you, sir.", "lord_pretalk", []],


[anyone|plyr,"lord_talk", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             (ge, "$g_talk_troop_faction_relation", 0),
                             (store_partner_quest,":lords_quest"),
                             (lt,":lords_quest",0)], 
"Do you have any tasks for me?", "lord_request_mission_ask",[]],

# TLD: Dwarf Lord takes Moria book, and gives player lotsa rank pts. Placeholder for now... (CppCoder)

#[anyone|plyr,"lord_talk", [(eq, "$g_talk_troop", "trp_dwarf_lord"),(player_has_item, "itm_book_of_moria"),(eq, cheat_switch, 1)], "My lord, I found this book...", "dwarf_lord_book", []],
#[anyone,"dwarf_lord_book", [(troop_remove_item, "trp_player", "itm_book_of_moria"),(call_script, "script_increase_rank", "fac_dwarf", 100)], "Give it to me, raw and wwwwrrrrigling...", "lord_pretalk", []],

# TLD: End Dwarf Lord takes Moria book

#TLD Dain II Ironfoot dialogue (Kolba, modified by CppCoder) -- begin

[anyone|plyr,"lord_talk", [(eq, "$g_talk_troop", "trp_dwarf_lord"),(check_quest_active,"qst_find_lost_spears")], "My lord, I wish to enter into the lonely mountains, in search of King Bladorthin's lost spears.", "find_lost_spears_permission", []],
                            
[anyone,"find_lost_spears_permission",[(quest_slot_ge, "qst_find_lost_spears", slot_quest_current_state, 1),], "I already gave you permission, {playername}.", "lord_pretalk", []],
[anyone,"find_lost_spears_permission",[(quest_slot_eq, "qst_find_lost_spears", slot_quest_current_state, 0),(ge, "$g_talk_troop_relation", 5)], "Alright, {playername}, you may enter into the mountains.", "find_lost_spears_permission_yes", [(quest_set_slot, "qst_find_lost_spears", slot_quest_current_state, 1),]],
[anyone,"find_lost_spears_permission",[(quest_slot_eq, "qst_find_lost_spears", slot_quest_current_state, 0)],"I'm sorry, but I don't know or trust you well enough, {playername}.", "lord_pretalk", []],

[anyone|plyr,"find_lost_spears_permission_yes",[], "I thank you, my Lord.", "lord_pretalk",[]],
              
#TLD Dain II Ironfoot dialogue (Kolba, modified by CppCoder) -- end
              
   #TLD - those oath options disabled for now, as no consequence menu is freezing game (Kolba)
                                                                                                                                                                                    
##[anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
##                             (ge, "$g_talk_troop_faction_relation", 0),
##                             #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
##                             (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
##                             (neq, "$players_kingdom", "$g_talk_troop_faction"),
##                             (store_partner_quest, ":lords_quest"),
##                             (neq, ":lords_quest", "qst_join_faction"),
##                            ],
##   "{s66}, I have come to offer you my sword in vassalage!", "lord_ask_enter_service",[]],
##
##
##[anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
##                             (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
##                             (eq, "$players_kingdom", "$g_talk_troop_faction"),
##                             (eq, "$player_has_homage", 0),
##                             (store_partner_quest, ":lords_quest"),
##                             (neq, ":lords_quest", "qst_join_faction"),
##                            ],
##   "{s66}, I wish to become your sworn {man/woman} and fight for your honour.", "lord_ask_enter_service",[]],
##
##[anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
##                             (ge, "$g_talk_troop_faction_relation", 0),
##                             #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
##                             (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
##                             (eq, "$players_kingdom", "$g_talk_troop_faction"),
##                             (eq, "$player_has_homage", 1),
##                            ],
##   "{s66}, I wish to be released from my oath to you.", "lord_ask_leave_service",[]],

    #TLD - oath options end (Kolba)
  

##[anyone|plyr,"lord_talk", [(le,"$talk_context", tc_party_encounter),
##                             (ge, "$g_talk_troop_faction_relation", 0),
##                             (troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                             (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
##                             (eq, "$players_kingdom", 0),
##                             (eq,1,0)],
##   "TODO2:I want to fight alongside you against your enemies.", "close_window",[]],



# [anyone|plyr,"lord_talk", [(eq, 1, 0),(le,"$talk_context", tc_party_encounter),(ge, "$g_talk_troop_faction_relation", 0)],
   # "I have an offer for you.", "lord_talk_preoffer",[]],
  
[anyone|plyr,"lord_talk", [(eq,"$encountered_party_hostile",0),
                             (eq,"$talk_context", tc_party_encounter), #works only on map: lords in towns get reinforced anyway
                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             (gt,"$tld_war_began",0),
                             (troop_get_slot, ":party", "$g_talk_troop", slot_troop_leaded_party),
                             (gt, ":party", 0),
                             (party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_party), # hosts only
                     #prevent some exploitation by placing caps on party size
                             (call_script, "script_party_get_ideal_size", ":party"),
                             (assign, ":ideal_size", reg0),
                             (party_get_num_companions, ":party_size", ":party"),
                             (lt, ":party_size", ":ideal_size"),
                             (try_begin),
                               (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
                               (str_store_string, s4, "@Do you need reinforcements?"),
                             (else_try),
                               (str_store_string, s4, "@You don't look too strong, do you need troops?"),
                             (try_end)],
"{s4}", "lord_give_troops",[
   #init from TLD recruiting in city - modified, copy of party_encounter_friend dialog code
		# prepare strings useful in the folowing dialog
		(str_store_faction_name, s14, "$g_talk_troop_faction"), # s22: Party faction name
		(call_script, "script_get_rank_title_to_s24", "$players_kingdom" ),(str_store_string_reg, s29, s24), # s29: player rank title with own faction
		(call_script, "script_get_rank_title_to_s24", "$g_talk_troop_faction" ), # s24: player rank title with this faction
		(assign, reg26, 0),(try_begin),(eq,"$players_kingdom","$g_talk_troop_faction"),(assign,reg26,1),(try_end), # reg26: 1 if party of player faction
		(party_get_num_companions, reg27, "p_main_party"), # reg27: initial party size
		# just to see if someone can be given away: backup party, then see if troops which can be given away 
		(call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
		(call_script, "script_party_split_by_faction", "p_main_party_backup", "p_temp_party", "$g_talk_troop_faction")]],

#Reinforcement code from town garrison reinforcement, register init above
[anyone,"lord_give_troops", [(party_get_num_companions,reg11,"p_main_party_backup"), (gt,reg11,1)],
	 "Reinforce my party? I can always use a few more soldiers.", 
	 "lord_give_troops_check", [
		(party_clear, "p_main_party_backup"),#GA: changed to exchange from whole party then return non-faction guys to player
		(assign, "$g_move_heroes", 0),
        (call_script, "script_party_add_party_companions", "p_main_party_backup", "p_main_party"), #keep this backup for later
		(party_get_num_companions, reg28, "p_main_party"), # reg28: initial main party size
		(call_script, "script_get_party_disband_cost", "p_main_party", 1), (assign, "$initial_party_value", reg0), # initial party total value
        (change_screen_give_members)]],
[anyone,"lord_give_troops", [], "Unfortunately you don't have any {s14} soldiers to reinforce me with.", "lord_pretalk", []],

[anyone,"lord_give_troops_check", [], "Let me check the soldier roster...", "lord_give_troops_check_1", []],

[anyone,"lord_give_troops_check_1", [
		(call_script, "script_party_eject_nonfaction","$g_encountered_party", "p_main_party", "p_main_party_backup"), #"p_main_party_backup" contains nonfaction troops returned
		(party_get_num_companions, reg0, "p_main_party"),
		(party_get_num_companions, reg46, "p_main_party_backup"),
		(eq, reg46, 0),(eq, reg28, reg0)], # player didn't give anyone (party size unchanged)
"So you've changed your mind...^I see.", "lord_pretalk", []],

[anyone,"lord_give_troops_check_1", [(gt, reg46, 0),(eq, reg28, reg0)], # player gave nonfittings only (party size unchanged)
"I don't have use for those troops here...^Take them back.", "lord_pretalk", []],

[anyone,"lord_give_troops_check_1", [(gt, reg28, reg0),# player gave fittings too (party size decreased)
        (val_sub, reg28, reg0),(val_sub, reg28, 1), #calculate how many troops given (minus 1)
		(call_script, "script_get_party_disband_cost", "p_main_party", 1),
        (val_sub, "$initial_party_value", reg0), #calculate how much monetary value given
		(try_begin),(eq, reg26, 1),(str_store_string, s31, "@Thank you, commander.^"),(str_clear, s32),
		 (else_try),               (str_store_string, s32, "@^{s14} is grateful to you, {playername}, {s29}^"),(str_clear, s31),
		(try_end),
		(assign, reg14, "$initial_party_value"),
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@{s31}{reg28?Those:That} brave {reg28?soldiers:soldier} will surely help us defend our lands.{s32}"+earned_reg14_rp_of_s14),
        (else_try),
          (str_store_string, s4, "@{s31}{reg28?Those:That} useful {reg28?troops:troop} will help us wreak more havoc.{s32}"+earned_reg14_rp_of_s14),
        (try_end), 
		(try_begin), # if nonfittings were given
          (gt, reg46, 0),
          (str_store_string, s4, "@{s4} ^Oh, and take back those soldiers who are not our kin, I have no use for them."),
        (try_end)],
"{s4}", "lord_give_troops_check_2", [(call_script, "script_add_faction_rps", "$g_talk_troop_faction", "$initial_party_value")]],

[anyone|plyr,"lord_give_troops_check_2", 
	[ (try_begin),(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
		                         (str_store_string, s31, "@I don't need them anyway, so save it."),
	   (else_try),(eq, reg26, 1),(str_store_string, s31, "@It is my duty to help our people."),
	   (else_try),               (str_store_string, s31, "@It is my duty to help our allies."),
	  (try_end)],
"{s31}", "lord_pretalk", []],

#[anyone,"lord_give_troops", [],
   # "Well, I could use some good soldiers. Thank you.", "lord_pretalk",
   # [
     # (change_screen_give_members),
     # ]],
  
#TLD: Ask a friendly king for reward items 
[anyone|plyr,"lord_talk",[
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"), #must be a king
     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0)], 
"I want to request a special item.", "lord_get_reward_item_ask",[]],

[anyone,"lord_get_reward_item_ask", [(store_free_inventory_capacity,reg1,"trp_player"),(eq, reg1,0)], "Seems like you have no place in your inventory for anything else. Make some room, then return.", "lord_talk",[]],
[anyone,"lord_get_reward_item_ask", [(store_free_inventory_capacity,reg1,"trp_player"),(gt, reg1,0)], "Really? Remember that you need to hold a certain rank and command considerable influence to deserve special items.^What can I give you?", "lord_get_reward_item",[]],
   
[anyone|plyr|repeat_for_100,"lord_get_reward_item", [
     (store_repeat_object, ":rank_index"),
     (is_between, ":rank_index", 0, 10),
     (call_script, "script_get_faction_rank", "$g_talk_troop_faction"),(assign, ":rank", reg0), #rank points to rank number 0-9
     
     (ge, ":rank", ":rank_index"), #player of sufficient rank?
     (store_sub, ":faction_index", "$g_talk_troop_faction", kingdoms_begin),
     (assign, ":item_exists", 0),    #find a reward item for specified rank if it exists
     (try_begin),
        ]+concatenate_scripts([
            [
            (eq, ":faction_index", x),
            ]+concatenate_scripts([[
              (try_begin),
                (eq, ":rank_index", fac_reward_items_list[x][item_entry][0]),
                (assign, ":item", fac_reward_items_list[x][item_entry][1]),
                (item_slot_eq, ":item", slot_item_given_as_reward, 0), # not already given
                (assign, ":item_exists", 1),
                (str_store_item_name, s20, ":item"),
              (try_end),
                ] for item_entry in range(len(fac_reward_items_list[x]))
            ])+[
         (else_try),
            ] for x in range(len(fac_reward_items_list))
        ])+[
     (try_end),
     (eq, ":item_exists", 1),
     (faction_get_slot, ":influence", "$g_talk_troop_faction", slot_faction_influence),
     (store_mul, ":price", ":rank_index", 5), # reward item price = 5*rank
     (ge, ":influence", ":price"), # player has enough influence to buy?
	 
	 
	 # don't let player buy something which he cannot ride personally
	 (assign, ":cant_ride", 0),
	 (try_begin),
		(item_get_type, ":it", ":item"),
		(eq, ":it", itp_type_horse),
		(call_script, "script_cf_troop_cant_ride_item","$g_player_troop",":item"), 
		(assign, ":cant_ride", 1),
	 (try_end),
	 (neq,":cant_ride",1),
	 
	 (try_begin),
	   (eq, "$g_talk_troop_faction", "$players_kingdom"),
	   (call_script, "script_get_own_rank_title_to_s24", "$g_talk_troop_faction", ":rank_index"),
	 (else_try),
	   (call_script, "script_get_allied_rank_title_to_s24", "$g_talk_troop_faction", ":rank_index"),
	 (try_end),
     #required rank title in s24
     (assign, reg14, ":price"),
     (assign, reg15, ":influence")],
"{s24}: {s20}"+spend_reg14_inf_on_reg15, "lord_get_reward_item_answer",[
     (store_repeat_object, ":rank_index"),
     (store_sub, ":faction_index", "$g_talk_troop_faction", kingdoms_begin),
     #find it again
     (try_begin),
        ]+concatenate_scripts([
            [
            (eq, ":faction_index", x),
            ]+concatenate_scripts([[
              (try_begin),
                (eq, ":rank_index", fac_reward_items_list[x][item_entry][0]),
                (assign, ":item", fac_reward_items_list[x][item_entry][1]),
                (assign, ":modifier", fac_reward_items_list[x][item_entry][2]),
              (try_end),
                ] for item_entry in range(len(fac_reward_items_list[x]))
            ])+[
         (else_try),
            ] for x in range(len(fac_reward_items_list))
        ])+[
     (try_end),
     (party_get_morale, ":recent_events_morale", "p_main_party"), #for later
     (call_script, "script_get_player_party_morale_values"),
     (val_sub, ":recent_events_morale", reg0),
     # and give it away
     (troop_add_item, "trp_player", ":item", ":modifier"),
     (item_set_slot, ":item", slot_item_given_as_reward, 1), # can't give more then one
     (call_script, "script_apply_attribute_bonuses"), # update player attributes for rings and such
     (call_script, "script_get_player_party_morale_values"),
     (val_add, ":recent_events_morale", reg0),
	 (val_clamp, ":recent_events_morale", 0, 100), #GA overflow fixage 
     (party_set_morale, "p_main_party", ":recent_events_morale"), # update morale for cauldrons and such
     (store_mul, ":price", ":rank_index", 5), # reward item price = 5*rank
	 (call_script, "script_spend_influence_of", ":price", "$g_talk_troop_faction")
,]],
        
[anyone|plyr,"lord_get_reward_item", [], "Never mind then.", "lord_pretalk", []],
[anyone,"lord_get_reward_item_answer", [], "Very well. May you use it to vanquish our enemies.", "lord_pretalk", []],

# TLD: give siege (and other?) suggestions to marshalls (MV)

[anyone|plyr, "lord_talk",
   [
     (faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"), #only with marshalls
     (ge, "$tld_war_began", 1),
   ],
"I would like to have a council with you about the War.", "marshall_ask",[]],

[anyone, "marshall_ask", [ #insufficient rank
      (call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (assign, ":rank", reg0), #rank points to rank number 0-9
      (lt, ":rank", 9),
      (call_script, "script_get_rank_title_to_s24", "$g_talk_troop_faction"), (str_store_string_reg, s25, s24), #to s25 (current rank)
      (call_script, "script_get_any_rank_title_to_s24", "$g_talk_troop_faction", 9), #to s24 (highest rank)
   ], "I would hardly take advice if you are merely {s25}, {playername}. I would have been more inclined to listen if you were {s24}, but you are not.", "lord_pretalk",[]],
[anyone, "marshall_ask", [ #insufficient influence
     (assign, ":siege_command_cost", tld_command_cost_siege),
     (try_begin),
       (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
       (val_mul, ":siege_command_cost", 2),
       (val_div, ":siege_command_cost", 3), # 33 for tld_command_cost_siege=50
     (try_end),
     (faction_get_slot, reg14, "$g_talk_troop_faction", slot_faction_influence),
     (lt, reg14, ":siege_command_cost"),
     (assign, reg15, ":siege_command_cost"),
   ], "You are an accomplished commander, {playername}, but your influence is waning. It would not be prudent to listen to your advice.^[{reg15} influence needed, only {reg14} held]", "lord_pretalk",[]],
[anyone, "marshall_ask", [ #insufficient faction strength
     (eq, "$tld_option_siege_reqs", 0), # Normal attacking siege reqs
     (neg|faction_slot_ge, "$g_talk_troop_faction", slot_faction_strength, fac_str_ok),
     (call_script, "script_faction_strength_string_to_s23", "$g_talk_troop_faction"),     
   ], "We can hardly afford to meet the enemy head on, {playername}. We still need to build up our forces and become strong, alas we are merely {s23}.", "lord_pretalk",[]],
[anyone, "marshall_ask", [ #busy campaigning
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_default), #not on campaign
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_gathering_army), #not gathering army
   ], "We are on a campaign, {playername}, your advice would have to wait.", "lord_pretalk",[]],
[anyone, "marshall_ask", [], "I'm listening, {playername}. What do you suggest?", "marshall_suggest",[]],

[anyone|plyr|repeat_for_parties, "marshall_suggest",
   [ (store_repeat_object, ":party_no"),
     (party_is_active, ":party_no"), #TLD
     #conditions for sieging (see also script_decide_faction_ai)
     (party_slot_eq, ":party_no", slot_center_destroyed, 0), #not destroyed
     (party_slot_eq, ":party_no", slot_party_type, spt_town), #a town
     (party_slot_eq, ":party_no", slot_center_is_besieged_by, -1), #not under siege
     
     (store_faction_of_party, ":enemy_faction", ":party_no"),
     (store_relation, ":relation", ":enemy_faction", "$g_talk_troop_faction"),
     (lt, ":relation", 0), #an enemy town

     (faction_get_slot, ":lord_theater", "$g_talk_troop_faction", slot_faction_active_theater),
     (party_slot_eq, ":party_no", slot_center_theater, ":lord_theater"), # an enemy town in active theater
     
     (party_get_slot, ":siegable", ":party_no", slot_center_siegability),
     (neq, ":siegable", tld_siegable_never), #some places are never siegable
     
     #make sure the enemy faction is weak enough to be sieged
     (faction_get_slot, ":enemy_faction_strength", ":enemy_faction", slot_faction_strength),       
     (this_or_next|eq, "$tld_option_siege_reqs", 2), # No siege reqs
     (this_or_next|eq, ":siegable", tld_siegable_always), # camps and such can always be sieged
     (lt, ":enemy_faction_strength", "$g_fac_str_siegable"), # otherwise, defenders need to be weak
     #if it's a faction capital, the enemy needs to be very weak
     (store_sub, ":capital_siegable_str", "$g_fac_str_siegable", fac_str_weak-fac_str_very_weak), #-1000
     (this_or_next|eq, "$tld_option_siege_reqs", 2), # No siege reqs
     (this_or_next|lt, ":enemy_faction_strength", ":capital_siegable_str"),
     (this_or_next|eq, ":siegable", tld_siegable_always), # camps and such can always be sieged
     (neq, ":siegable", tld_siegable_capital), #if a capital, needs also fac_str_very_weak

     #end siege conditions
     (str_store_party_name, s1, ":party_no")],
   "We should ride to besiege {s1} at once.", "marshall_answer",[(store_repeat_object, "$temp")]],
[anyone|plyr, "marshall_suggest", [], "Never mind, I trust your judgement.", "lord_pretalk",[]],

[anyone, "marshall_answer", [],
   "Very well, {playername}, I shall defer to your judgement. I shall send messengers to gather our forces.^Follow me and stay close - we ride to {s4}!", "close_window",
   [
     (assign, ":siege_target", "$temp"),
     #faction AI
     (faction_set_slot, "$g_talk_troop_faction", slot_faction_ai_state, sfai_attacking_center),
     (faction_set_slot, "$g_talk_troop_faction", slot_faction_ai_object, ":siege_target"),
     
     #marshall party AI
     (troop_get_slot, ":marshall_party", "$g_talk_troop", slot_troop_leaded_party),
     (call_script, "script_party_set_ai_state", ":marshall_party", spai_besieging_center, ":siege_target"),
     (party_set_ai_initiative, ":marshall_party", 0), #no chasing around
     (party_set_slot, ":marshall_party", slot_party_commander_party, -1),
     
     #make all available faction hosts follow
     (try_for_range, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
       (troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
       (neg|troop_slot_ge, ":lord", slot_troop_prisoner_of_party, 0),
       (store_troop_faction, ":lord_faction", ":lord"),
       (eq, ":lord_faction", "$g_talk_troop_faction"),
       (troop_get_slot, ":lord_party", ":lord", slot_troop_leaded_party),
       (gt, ":lord_party", 0),
       (party_is_active, ":lord_party"),
       (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, ":lord"), #skip kings and marshalls
       (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, ":lord"),
       #(party_slot_eq, ":lord_party", slot_party_type, spt_kingdom_hero_party), #intentionally not a condition, for fun
       
       #now, just follow and shut up
       (party_set_slot, ":lord_party", slot_party_commander_party, ":marshall_party"),
       (call_script, "script_party_set_ai_state", ":lord_party", spai_accompanying_army, ":marshall_party"),
       (party_set_ai_initiative, ":lord_party", 10), #don't react to random enemies much
     (try_end),

     #deduct influence cost
     (assign, ":siege_command_cost", tld_command_cost_siege),
     (try_begin),
       (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
       (val_mul, ":siege_command_cost", 2),
       (val_div, ":siege_command_cost", 3), # 33 for tld_command_cost_siege=50
     (try_end),
     (call_script, "script_spend_influence_of", ":siege_command_cost", "$g_talk_troop_faction"),
     
     (str_store_party_name, s4, ":siege_target"),    
   ]],

# TLD: Accept a delivered gift (CppCoder)
[anyone|plyr,"lord_talk",[
	(check_quest_active,"qst_deliver_gift"),
	(quest_slot_eq, "qst_deliver_gift", slot_quest_target_faction, "$g_talk_troop_faction"), #must be correct faction
        (quest_get_slot, ":giver_item_str", "qst_deliver_gift", slot_quest_target_amount),
        (quest_get_slot, ":giver_faction", "qst_deliver_gift", slot_quest_object_faction),
	(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"), #must be a king
	(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),	
	(str_store_faction_name, s3, ":giver_faction"),
	(str_store_faction_name, s2, "$g_talk_troop_faction"),
	(str_store_string, s1, ":giver_item_str"),
   ], 
"I bring a gift of {s1} from {s3} to the people of {s2}.", "deliver_gift_1",[]],

[anyone,"deliver_gift_1",[
	(store_sub, ":faction_index", "$g_talk_troop_faction", kingdoms_begin),
        (quest_get_slot, ":original_faction", "qst_deliver_gift", slot_quest_object_faction),
        (quest_get_slot, ":giver_gift_str", "qst_deliver_gift", slot_quest_target_amount),
        (quest_get_slot, ":gold", "qst_deliver_gift", slot_quest_gold_reward),
   	(quest_set_slot, "qst_deliver_gift", slot_quest_gold_reward, 0),
	(call_script, "script_finish_quest", "qst_deliver_gift", 100),
	(call_script, "script_add_faction_rps", "$g_talk_troop_faction", ":gold"),
        (quest_get_slot, ":gift_no", "qst_deliver_gift", slot_quest_target_item),
	(assign, reg20, ":gift_no"),
	(store_mul, ":gift_str", ":faction_index", tld_gifts_per_faction),
	(val_add, ":gift_str", gift_strings_begin),
	(val_add, ":gift_str", ":gift_no"),
	(str_store_string, s1, ":giver_gift_str"),
	(str_store_string, s2, ":gift_str"),
	(str_store_faction_name, s3, "$g_talk_troop_faction"),
	(str_store_faction_name, s4, ":original_faction"),
   	(quest_set_slot, "qst_deliver_gift", slot_quest_target_faction, 0),
   	(quest_set_slot, "qst_deliver_gift", slot_quest_object_faction, 0),
	(str_store_string, s5, "@The people of {s3} thank you for your gift, {playername}. In exchange for your gift of {s1}, we will send the people of {s4} a gift of {s2}. I thank you once again, {playername}."),

], "{s5}", "lord_pretalk", []],

# TLD: Deliver gift to other allied factions (CppCoder)

[anyone|plyr,"lord_talk",[
	#(eq, cheat_switch, 1), # (CppCoder): Enabled only in dev, for now.
	(faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"), #must be a king
	(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),	
	(quest_slot_eq|neg, "qst_deliver_gift", slot_quest_target_faction, "$g_talk_troop_faction"), # can't ask to deliver a gift from the faction you are giving a gift to.
	(quest_get_slot, ":days_remaining", "qst_deliver_gift", slot_quest_dont_give_again_remaining_days),
	(le, ":days_remaining", 0),
	(try_begin),
		(faction_slot_eq|this_or_next, "$g_talk_troop_faction", slot_faction_side, faction_side_good), # Good or Evil men
		(faction_slot_eq|neg, "$g_talk_troop_faction", slot_faction_culture, mtf_culture_orcs),
		(str_store_string, s1, "@I want to deliver a gift to our allies."),
		(str_store_string, s4, "@delivering a gift"),
	(else_try),
		(str_store_string, s1, "@I want to bring a bribe to our allies."),
		(str_store_string, s4, "@delivering a bribe"),
	(try_end),
   ], 
"{s1}", "send_gift_1",[]],
   
[anyone,"send_gift_1",[(check_quest_active,"qst_deliver_gift")], "You are already {s4}, {playername}. It would be wise to deliver that one first.", "lord_pretalk",[]],
[anyone,"send_gift_1",[(call_script,"script_update_respoint"),(faction_get_slot, ":rps", "$g_talk_troop_faction", slot_faction_respoint),(lt,":rps",500),], "Unfortunately, you cannot afford to send a gift right now {playername}."+not_enough_rp, "lord_pretalk",[]],

# Good factions and evil men send gifts, others send bribes.
[anyone,"send_gift_1",
	[
	(faction_slot_eq|this_or_next, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
	(faction_slot_eq|neg, "$g_talk_troop_faction", slot_faction_culture, mtf_culture_orcs),
	], 
	"Very well. To whom would you like to deliver a gift?", "send_gift_2",[]],
[anyone,"send_gift_1",[], "Very Well. Who do you want to give a bribe to?", "send_gift_2",[]],

[anyone|plyr|repeat_for_100,"send_gift_2",
[
	(store_repeat_object, ":faction_index"),
	(store_sub, ":num_kingdoms", kingdoms_end, kingdoms_begin),
	(lt, ":faction_index", ":num_kingdoms"),
	(store_add, ":faction_no", ":faction_index", kingdoms_begin),
	(this_or_next|eq, cheat_switch, 1), # Allows debuggers to give gifts to their own faction. ;) (CppCoder)
	(neq, "$g_talk_troop_faction", ":faction_no"),
        (store_relation, ":relation", ":faction_no", "$g_talk_troop_faction"),
	(ge, ":relation", 0), # Allies only
	(str_store_faction_name, s1, ":faction_no"),
], "{s1}", "send_gift_3",[(store_repeat_object, reg1)]],

[anyone|plyr,"send_gift_2",[], "Nevermind.", "lord_pretalk",[]],

[anyone,"send_gift_3",
	[
	(faction_slot_eq|this_or_next, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
	(faction_slot_eq|neg, "$g_talk_troop_faction", slot_faction_culture, mtf_culture_orcs),
	], "Which gift would you like to give to them?", "send_gift_4",[]],

[anyone,"send_gift_3",[], "What bribe do you want to give them?", "send_gift_4",[]],

[anyone|plyr|repeat_for_100,"send_gift_4",
[
	(store_repeat_object, ":gift_no"),
	(lt, ":gift_no", 5),
	(store_sub, ":faction_index", "$g_talk_troop_faction", kingdoms_begin),
	(store_mul, ":gift_str", ":faction_index", tld_gifts_per_faction),
	(val_add, ":gift_str", gift_strings_begin),
	(val_add, ":gift_str", ":gift_no"),
	(str_store_string, s2, ":gift_str"),
	(store_mul, ":gift_cost_a", ":gift_no", ":gift_no"),
	(store_mul, ":gift_cost", ":gift_cost_a", 500),
	(store_add, reg14, ":gift_cost", 500),
	(faction_get_slot,  ":rps", "$g_talk_troop_faction", slot_faction_respoint),
	(ge,":rps",reg14), # Player must be able to afford gift...
	(str_store_string, s1, "@{s2} [{reg14} Resource Points]"),	
], "{s1}", "send_gift_5",[(store_repeat_object, reg2)]],

[anyone|plyr,"send_gift_4",[], "Nevermind.", "lord_pretalk",[]],

[anyone,"send_gift_5",[], "All right {playername}. Good Luck.", "lord_pretalk",
[
    	(store_add, ":target_faction", reg1, kingdoms_begin),
    	(assign, ":gift_no", reg2),
	(store_sub, ":faction_index", "$g_talk_troop_faction", kingdoms_begin),
	(store_mul, ":gift_str", ":faction_index", 5),
	(val_add, ":gift_str", gift_strings_begin),
	(val_add, ":gift_str", ":gift_no"),
	(store_mul, ":gift_cost_a", ":gift_no", ":gift_no"), # i^2
	(store_mul, ":gift_cost", ":gift_cost_a", 500), # (i^2)*500
	(store_add, reg14, ":gift_cost", 500), #(i^2)*500 + 500
	(store_sub, reg0, 0, reg14),
	(call_script, "script_add_faction_rps", "$g_talk_troop_faction", reg0),
	(str_store_string, s1, ":gift_str"),
    	(str_store_faction_name, s2, "$g_talk_troop_faction"),
    	(str_store_faction_name, s3, ":target_faction"),
   	(quest_set_slot, "qst_deliver_gift", slot_quest_gold_reward, reg14),
   	(quest_set_slot, "qst_deliver_gift", slot_quest_target_item, ":gift_no"),
   	(quest_set_slot, "qst_deliver_gift", slot_quest_target_amount, ":gift_str"),
   	(quest_set_slot, "qst_deliver_gift", slot_quest_target_faction, ":target_faction"),
   	(quest_set_slot, "qst_deliver_gift", slot_quest_object_faction, "$g_talk_troop_faction"),
   	(quest_set_slot, "qst_deliver_gift", slot_quest_object_faction, "$g_talk_troop_faction"),
	(quest_set_slot, "qst_deliver_gift", slot_quest_dont_give_again_remaining_days, 15), # Can only give a gift every 15 days.
	(try_begin),
		(faction_slot_eq|this_or_next, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
		(faction_slot_eq|neg, "$g_talk_troop_faction", slot_faction_culture, mtf_culture_orcs),
		(str_store_string, s4, "@Gift"),
    		(setup_quest_text,"qst_deliver_gift"),
    		(str_store_string, s2, "@You have requested to deliver a gift of {s1} to {s3} from {s2}. The people of {s3} will surely appreciate this kind gesture."),
    		(call_script, "script_start_quest", "qst_deliver_gift", "$g_talk_troop"),
	(else_try),
		(str_store_string, s4, "@Bribe"),
    		(setup_quest_text,"qst_deliver_gift"),
    		(str_store_string, s2, "@You have requested to deliver a bribe of {s1} to {s3} from {s2}. Hopefully you can get some sort of reward from them in exchange."),
    		(call_script, "script_start_quest", "qst_deliver_gift", "$g_talk_troop"),		
	(try_end),
]],

# TLD: give orders to lords (MV)

[anyone|plyr,"lord_talk",
   [ # TLD: give orders if you have some minimum faction influence
     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"), #can't give orders to kings
     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "$g_talk_troop"), #can't give orders to marshalls
     (faction_get_slot, ":influence", "$g_talk_troop_faction", slot_faction_influence),
     (assign, ":min_command_cost", tld_command_cost_goto),
     (try_begin),
       (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
       (val_mul, ":min_command_cost", 2),
       (val_div, ":min_command_cost", 3), # min_command_cost is 3 now (for tld_command_cost_goto=5)
     (try_end),
     (ge, ":influence", ":min_command_cost"), #the lowest cost among the actions below
     # check if traits are needed
     (assign, ":trait_check_passed", 1),
     (try_begin),
       (eq, "$g_talk_troop_faction", "fac_gondor"),
       (troop_slot_eq, "trp_traits", slot_trait_gondor_friend, 0),
       (assign, ":trait_check_passed", 0),
     (try_end),
     (try_begin),
       (eq, "$g_talk_troop_faction", "fac_rohan"),
       (troop_slot_eq, "trp_traits", slot_trait_rohan_friend, 0),
       (assign, ":trait_check_passed", 0),
     (try_end),
     (try_begin),
       (this_or_next|eq, "$g_talk_troop_faction", "fac_lorien"),
       (this_or_next|eq, "$g_talk_troop_faction", "fac_imladris"),
       (eq, "$g_talk_troop_faction", "fac_woodelf"),
       (troop_slot_eq, "trp_traits", slot_trait_elf_friend, 0),
       (assign, ":trait_check_passed", 0),
     (try_end),
     (eq, ":trait_check_passed", 1),
   ],
"I have a new task for you.", "lord_give_order_ask",[]],

[anyone,"lord_give_order_ask", [], "Yes?", "lord_give_order",[]],


[anyone|plyr,"lord_give_order", [
    (assign, "$temp_action_cost", tld_command_cost_follow),
    (try_begin),
      (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
      (val_mul, "$temp_action_cost", 2),
      (val_div, "$temp_action_cost", 3), # 13 for tld_command_cost_follow=20
    (try_end),
    (assign, reg1, "$temp_action_cost"),
    (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
    (ge, reg2, "$temp_action_cost")], 
"Follow me. [Costs {reg1}/{reg2} influence]", "lord_give_order_answer", [
     (assign, "$temp", spai_accompanying_army),
     (assign, "$temp_2", "p_main_party"),
     (assign, "$tld_action_cost", tld_command_cost_follow),
     (try_begin),
	(troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
	(val_mul, "$tld_action_cost", 2),
	(val_div, "$tld_action_cost", 3),
     (try_end)]],

[anyone|plyr,"lord_give_order", [
    (assign, "$temp_action_cost", tld_command_cost_goto),
    (try_begin),
      (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
      (val_mul, "$temp_action_cost", 2),
      (val_div, "$temp_action_cost", 3), # 3 for tld_command_cost_goto=5
    (try_end),
    (assign, reg1, "$temp_action_cost"),
    (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
    (ge, reg2, "$temp_action_cost")], 
"Go to... [Costs {reg1}/{reg2} influence]", "lord_give_order_details_ask",[
     (assign, "$temp", spai_holding_center),
     (assign, "$tld_action_cost", tld_command_cost_goto),
     (try_begin),
	(troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
	(val_mul, "$tld_action_cost", 2),
	(val_div, "$tld_action_cost", 3),
     (try_end)]],

  #[anyone|plyr,"lord_give_order", [],
   # "Raid around the village of...", "lord_give_order_details_ask",
   # [
     # (assign, "$temp", spai_raiding_around_center),
     # ]],

[anyone|plyr,"lord_give_order", [
    (assign, "$temp_action_cost", tld_command_cost_patrol),
    (try_begin),
      (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
      (val_mul, "$temp_action_cost", 2),
      (val_div, "$temp_action_cost", 3), # 6 for tld_command_cost_patrol=10
    (try_end),
    (assign, reg1, "$temp_action_cost"),
    (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
    (ge, reg2, "$temp_action_cost")],  
"Patrol around... [Costs {reg1}/{reg2} influence]", "lord_give_order_details_ask",[
     (assign, "$temp", spai_patrolling_around_center),
     (assign, "$tld_action_cost", tld_command_cost_patrol),
     (try_begin),
	(troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
	(val_mul, "$tld_action_cost", 2),
	(val_div, "$tld_action_cost", 3),
     (try_end)]],

[anyone|plyr,"lord_give_order", [
    (assign, "$temp_action_cost", tld_command_cost_engage),
    (try_begin),
      (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
      (val_mul, "$temp_action_cost", 2),
      (val_div, "$temp_action_cost", 3), # 16 for tld_command_cost_engage=25
    (try_end),
    (assign, reg1, "$temp_action_cost"),
    (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
    (ge, reg2, "$temp_action_cost")], 
"Engage enemies around... [Costs {reg1}/{reg2} influence]", "lord_give_order_details_ask",[
     (assign, "$temp", spai_raiding_around_center), #not really, changed later to spai_patrolling_around_center
     (assign, "$tld_action_cost", tld_command_cost_engage),
     (try_begin),
	(troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
	(val_mul, "$tld_action_cost", 2),
	(val_div, "$tld_action_cost", 3),
     (try_end)]],

[anyone|plyr,"lord_give_order", [(neg|troop_slot_eq, "$g_talk_troop", slot_troop_player_order_state, spai_undefined)],
   "I won't need you for some time. You are free to do as you like.", "lord_give_order_stop", []],

[anyone|plyr,"lord_give_order", [], "Never mind.", "lord_pretalk", []],
[anyone,"lord_give_order_details_ask", [], "Where?", "lord_give_order_details",[]],

[anyone|plyr|repeat_for_parties, "lord_give_order_details",
   [ (store_repeat_object, ":party_no"),
     (party_is_active, ":party_no"), #TLD
     (store_faction_of_party, ":party_faction", ":party_no"),
     (store_relation, ":relation", ":party_faction", "$g_talk_troop_faction"),
     (faction_get_slot, ":lord_theater", "$g_encountered_party_faction", slot_faction_active_theater),
     (assign, ":continue", 0),
     (try_begin),
       (eq, "$temp", spai_holding_center),
       (try_begin),
         (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_castle),
         (party_slot_eq, ":party_no", slot_party_type, spt_town),
         (eq, ":party_faction", "$g_talk_troop_faction"),
         (assign, ":continue", 1),
       (try_end),
     (else_try),
       (eq, "$temp", spai_patrolling_around_center),
       (try_begin),
         (eq, ":party_faction", "$g_talk_troop_faction"),
         (is_between, ":party_no", centers_begin, centers_end),
         (assign, ":continue", 1),
       (try_end),
     (else_try),
       (eq, "$temp", spai_raiding_around_center),
       (try_begin),
         (party_slot_eq, ":party_no", slot_party_type, spt_town),
         (lt, ":relation", 0),
         (party_slot_eq, ":party_no", slot_center_theater, ":lord_theater"), # must be in active theater
         (assign, ":continue", 1),
       (try_end),
     (try_end),
     (eq, ":continue", 1),
     #(neq, ":party_no", "$g_encountered_party"), #MV
     (str_store_party_name, s1, ":party_no")],
   "{s1}", "lord_give_order_answer",[(store_repeat_object, "$temp_2")]],

[anyone|plyr, "lord_give_order_details", [], "Never mind.", "lord_pretalk",[]],

[anyone,"lord_give_order_stop", [],
   "All right. I will do that.", "lord_pretalk",
   [ (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, -1),
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (try_begin),
       (gt, ":party_no", 0),
       (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
       (party_set_slot, ":party_no", slot_party_commander_party, -1),
     (try_end)]],
  
[anyone,"lord_give_order_answer", [
     (assign, ":continue", 0),
     (try_begin),
       (troop_slot_ge, "$g_talk_troop", slot_troop_readiness_to_follow_orders, 60),
       (assign, ":continue", 1),
     (else_try),
       (troop_slot_ge, "$g_talk_troop", slot_troop_readiness_to_follow_orders, 10),
       (neg|troop_slot_eq, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
       (assign, ":continue", 1),
     (try_end),
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (this_or_next|le, ":party_no", 0),
     (eq, ":continue", 0)],  #Meaning that hero does not want to follow player orders for a while.
"I am sorry. I am needed somewhere else at the moment.", "lord_pretalk",[
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, -1)]],

[anyone|auto_proceed,"lord_give_order_answer",[],
".", "lord_give_order_answer_2", [
     (try_begin),
       (eq, "$temp", spai_raiding_around_center),
       (assign, "$temp", spai_patrolling_around_center), # simply patrol around enemy town.. does this work?
     (try_end),
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (call_script, "script_party_set_ai_state", ":party_no", "$temp", "$temp_2"),
     (try_begin),
       (eq, "$temp", spai_accompanying_army),
       (party_set_slot, ":party_no", slot_party_commander_party, "$temp_2"),
     (else_try),
       (party_set_slot, ":party_no", slot_party_commander_party, -1),
     (try_end),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, "$temp"),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, "$temp_2"),
     #Checking if the order is accepted by the ai
     #(call_script, "script_recalculate_ai_for_troop", "$g_talk_troop"), #TLD: disabled! lords should always obey..
     ]],

[anyone,"lord_give_order_answer_2", [
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (party_slot_eq, ":party_no", slot_party_ai_state, "$temp"),
     (party_slot_eq, ":party_no", slot_party_ai_object, "$temp_2"),
     (assign, "$g_leave_encounter", 1)],
"I will do that.", "close_window", [
     (call_script,"script_stand_back"),
	 (store_current_hours, ":cur_time"),
     (store_add, ":obey_until_time", ":cur_time", 5*24), # commands last 5 days
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (party_set_slot, ":party_no", slot_party_follow_player_until_time, ":obey_until_time"), #no lord ai changes until this time
     (faction_get_slot, ":influence", "$g_talk_troop_faction", slot_faction_influence),
	(try_begin),
		(eq, cheat_switch, 1),
		(assign, reg0, "$tld_action_cost"),
		(assign, reg1, "$temp_action_cost"),
		(display_message, "@Taking {reg0} inf. Alt?={reg1}"),
	(try_end),
     (val_sub, ":influence", "$tld_action_cost"),
     (faction_set_slot, "$g_talk_troop_faction", slot_faction_influence, ":influence"),
     (assign, reg0, "$tld_action_cost"),
     (assign, reg1, ":influence"),
     (str_store_faction_name, s1, "$g_talk_troop_faction"),
     (display_message, "@You spent {reg0} of your influence with {s1}, with {reg1} remaining."),
     (val_add, "$trait_check_commands_issued", 1),]],

[anyone,"lord_give_order_answer_2", [],#Meaning that the AI decision function did not follow the order.
"I am sorry, it is not possible for me to do that.", "lord_pretalk",[ 
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, -1)]],

# [anyone|plyr,"lord_talk",
   # [ (eq, "$g_talk_troop_faction", "$players_kingdom"),
     # (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
     # #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
     # (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
     # (faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default)], 
# "I want to start a new campaign. Let us assemble the army here.", "lord_give_order_call_to_arms_verify",[]],

# [anyone,"lord_give_order_call_to_arms_verify", [], "You wish to summon all lords for a new campaign?", "lord_give_order_call_to_arms_verify_2",[]],

# [anyone|plyr,"lord_give_order_call_to_arms_verify_2", [], "Yes. We must gather all our forces before we march on the enemy.", "lord_give_order_call_to_arms",[]],
# [anyone|plyr,"lord_give_order_call_to_arms_verify_2", [], "On second thought, it won't be necessary to summon everyone.", "lord_pretalk",[]],

# [anyone,"lord_give_order_call_to_arms",[],
# "All right then. I will send messengers and tell everyone to come here.", "lord_pretalk",[
     # (faction_set_slot, "$players_kingdom", slot_faction_ai_state, sfai_gathering_army),
     # (assign, "$g_recalculate_ais", 1)]],

# [anyone|plyr,"lord_talk",
   # [ (eq, "$g_talk_troop_faction", "$players_kingdom"),
     # (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
     # #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
     # (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
     # (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default)], 
# "I want to end the campaign and let everyone return home.", "lord_give_order_disband_army_verify", []],

# [anyone,"lord_give_order_disband_army_verify", [], "You want to end the current campaign and release all lords from duty?", "lord_give_order_disband_army_2",[]],
# [anyone|plyr,"lord_give_order_disband_army_2", [], "Yes. We no longer need all our forces here.", "lord_give_order_disband_army",[]],
# [anyone|plyr,"lord_give_order_disband_army_2", [], "On second thought, it will be better to stay together for now.", "lord_pretalk",[]],

# [anyone,"lord_give_order_disband_army", [],
# "All right. I will let everyone know that they are released from duty.", "lord_pretalk",
   # [ (faction_set_slot, "$players_kingdom", slot_faction_ai_state, sfai_default),
     # (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
       # (troop_get_slot, ":party_no", ":cur_troop", slot_troop_leaded_party),
       # (gt, ":party_no", 0),
       # (party_slot_eq, ":party_no", slot_party_commander_party, "p_main_party"),
       # (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
       # (party_set_slot, ":party_no", slot_party_commander_party, -1),
     # (try_end),
     # (assign, "$g_recalculate_ais", 1)]],

[anyone|plyr,"lord_talk", [(ge, "$g_talk_troop_faction_relation", 0)], "I wish to ask you something.", "lord_talk_ask_something",[]],
[anyone,"lord_talk_ask_something", [], "Aye? What is it?", "lord_talk_ask_something_2",[]],

[anyone|plyr,"lord_talk_ask_something_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                                             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0)], 
"I want to know the location of someone.", "lord_talk_ask_location",[]],

[anyone|plyr,"lord_talk_ask_something_2", [], "What are you and your men doing?", "lord_tell_objective",[]],
  
[anyone|plyr,"lord_talk_ask_something_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
											 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0)], 
"How goes the war?", "lord_talk_ask_about_war",[]],
  
[anyone|plyr,"lord_talk_ask_something_2", [], "Never mind.", "lord_pretalk",[]],
[anyone,"lord_talk_ask_location", [], "Very well, I may or may not have an answer for you. About whom do you wish to hear?", "lord_talk_ask_location_2",[]],

[anyone|plyr|repeat_for_troops,"lord_talk_ask_location_2", [(store_repeat_object, ":troop_no"),
                                                              (neq, "$g_talk_troop", ":troop_no"),
															  (store_troop_faction, ":talk_faction", "$g_talk_troop"),
                                                              (is_between, ":troop_no", heroes_begin, heroes_end),
                                                              (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                                                              (store_troop_faction, ":faction_no", ":troop_no"),
                                                              (eq, ":talk_faction", ":faction_no"),
                                                              (str_store_troop_name, s1, ":troop_no")],
"{s1}", "lord_talk_ask_location_3",[(store_repeat_object, "$hero_requested_to_learn_location")]],

[anyone|plyr,"lord_talk_ask_location_2", [], "Never mind.", "lord_pretalk",[]],

[anyone,"lord_talk_ask_location_3",
   [ (call_script, "script_update_troop_location_notes", "$hero_requested_to_learn_location", 1),
     (call_script, "script_get_information_about_troops_position", "$hero_requested_to_learn_location", 0)], 
"{s1}", "lord_pretalk",[]],

[anyone,"lord_talk_ask_about_war", [],
   "{s12}", "lord_talk_ask_about_war_2",[
	(assign, ":num_enemies", 0),
	(assign, ":num_theater_enemies", 0),
	(faction_get_slot, ":faction_theater", "$g_encountered_party_faction", slot_faction_active_theater),
	(try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
		(faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
		(store_relation, ":cur_relation", ":cur_faction", "$g_talk_troop_faction"),
		(lt, ":cur_relation", 0),
		(try_begin),
		  (eq, ":num_enemies", 0),
		  (str_store_faction_name_link, s12, ":cur_faction"),
		(else_try),
		  (eq, ":num_enemies", 1),
		  (str_store_faction_name_link, s11, ":cur_faction"),
		  (str_store_string, s12, "@{s11} and {s12}"),
		(else_try),
		  (str_store_faction_name_link, s11, ":cur_faction"),
		  (str_store_string, s12, "@{s11}, {s12}"),
		(try_end),
		(val_add, ":num_enemies", 1),
		(faction_slot_eq, ":cur_faction", slot_faction_active_theater, ":faction_theater"),
		(try_begin),
		  (eq, ":num_theater_enemies", 0),
		  (str_store_faction_name_link, s13, ":cur_faction"),
		(else_try),
		  (eq, ":num_theater_enemies", 1),
		  (str_store_faction_name_link, s11, ":cur_faction"),
		  (str_store_string, s13, "@{s11} and {s13}"),
		(else_try),
		  (str_store_faction_name_link, s11, ":cur_faction"),
		  (str_store_string, s13, "@{s11}, {s13}"),
		(try_end),
		(val_add, ":num_theater_enemies", 1),
	(try_end),
	(try_begin),
		(eq, ":num_enemies", 0),
		(str_store_string, s12, "@The War is over, {playername}, haven't you heard?"),
		(else_try),
		(try_begin),
		  (gt, ":num_theater_enemies", 0),
		  (str_store_string, s12, "@We are at war with {s12}. However, we are mostly fighting against {s13}."),
		(else_try),
		  (str_store_string, s12, "@We are at war with {s12}. However, there are only skirmishes at the moment."),
		(try_end),
	(try_end)]],

[anyone|plyr|repeat_for_factions, "lord_talk_ask_about_war_2", [(store_repeat_object, ":faction_no"),
                                                                  (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
                                                                  (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
                                                                     (store_relation, ":cur_relation", ":faction_no", "$g_talk_troop_faction"),
                                                                     (lt, ":cur_relation", 0),
                                                                     (str_store_faction_name, s1, ":faction_no")],
"Tell me more about the war with {s1}.", "lord_talk_ask_about_war_details",[(store_repeat_object, "$faction_requested_to_learn_more_details_about_the_war_against")]],

[anyone|plyr,"lord_talk_ask_about_war_2", [], "That's all I wanted to know. Thank you.", "lord_pretalk",[]],

[anyone,"lord_talk_ask_about_war_details", [],
"We are {s22} and they are {s23}. Overall, {s9}.", "lord_talk_ask_about_war_2",[
	(call_script, "script_faction_strength_string_to_s23", "$g_encountered_party_faction"),
	(str_store_string_reg, s22, s23),
	(call_script, "script_faction_strength_string_to_s23", "$faction_requested_to_learn_more_details_about_the_war_against"),
	(faction_get_slot, ":faction_theater", "$g_encountered_party_faction", slot_faction_active_theater),
	(try_begin),
	  (faction_slot_eq, "$faction_requested_to_learn_more_details_about_the_war_against", slot_faction_active_theater, ":faction_theater"),
	  (faction_get_slot, ":our_str", "$g_encountered_party_faction", slot_faction_strength),
	  (faction_get_slot, ":enemy_str", "$faction_requested_to_learn_more_details_about_the_war_against", slot_faction_strength),
	  (store_sub, ":advantage", ":our_str", ":enemy_str"), #-7000 to +7000
	  (val_div, ":advantage", 1200), # -5 to +5
	  (val_clamp, ":advantage", -4, 5), # -4 to +4
	  (val_add, ":advantage", 4),
	  (store_add, ":adv_str", "str_war_report_minus_4", ":advantage"),
	  (str_store_string, s9, ":adv_str"),
	(else_try),
	  (str_store_string, s9, "@we are not too concerned with them at the moment, since we are fighting other enemies closer to home"),
	(try_end)]],


[anyone|plyr,"lord_talk", [(eq,"$talk_context",tc_party_encounter),
                             (lt, "$g_encountered_party_relation", 0),
                             (str_store_troop_name,s4,"$g_talk_troop")],
   "Today is a good day for battle, {s4}!", "party_encounter_lord_hostile_ultimatum_surrender", []],
   
[anyone,"party_encounter_lord_hostile_ultimatum_surrender", [],
"{s43}", "close_window", [
       (call_script,"script_stand_back"),
	   (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default"),
       (assign,"$encountered_party_hostile",1)]],




# [anyone|plyr,"lord_talk", [(eq, "$cheat_mode", 1),
                             # #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                             # (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             # #(ge, "$g_talk_troop_faction_relation", 10),
                             # ],
# "CHEAT:I want to suggest a course of action.", "lord_suggest_action_ask",[]],

[anyone,"lord_tell_objective", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 1),
                                  # insert this string where appropriate
                                  (str_clear, s5),
                                  (try_begin),
                                    (store_current_hours, ":cur_time"),
                                    (party_slot_ge, "$g_talk_troop_party", slot_party_follow_player_until_time, ":cur_time"), # MV: under orders
                                    (str_store_string, s5, "@, under your orders"),
                                  (try_end),
                                  (troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0)],
"What am I doing? What does it look like I'm doing?! I'm a prisoner here!", "lord_pretalk",[]],

[anyone,"lord_tell_objective", [(troop_slot_eq, "$g_talk_troop", slot_troop_leaded_party, -1)],
"I am not commanding any men at the moment.", "lord_pretalk",[]],

[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_holding_center),
                                  (party_get_attached_to, ":cur_center_no", "$g_talk_troop_party"),
                                  (try_begin),
                                    (lt, ":cur_center_no", 0),
                                    (party_get_cur_town, ":cur_center_no", "$g_talk_troop_party"),
                                  (try_end),
                                  (is_between, ":cur_center_no", centers_begin, centers_end)],
"We are resting at {s1}{s5}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                              (str_store_party_name, s1, ":ai_object")]],

[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_holding_center)],
"We are travelling to {s1}{s5}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                 (str_store_party_name, s1, ":ai_object")]],

[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_recruiting_troops)],
"We are recruiting new soldiers from {s1}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                 (str_store_party_name, s1, ":ai_object")]],

[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_patrolling_around_center)],
"We are scouting for the enemy around {s1}{s5}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                      (str_store_party_name, s1, ":ai_object")]],

#[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_raiding_around_center)],
#   "We ride out to lay waste to village of {s1} to punish the foe for his misdeeds.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
#                                                               (str_store_party_name, s1, ":ai_object")]],

[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_raiding_around_center)],
"We are laying waste to the village of {s1}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                               (str_store_party_name, s1, ":ai_object")]],

[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_retreating_to_center)],
"We are retreating to {s1}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                               (str_store_party_name, s1, ":ai_object")]],

[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_besieging_center)],
"We are besieging {s1}{s5}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                               (str_store_party_name, s1, ":ai_object")]],

[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_engaging_army),
                                  (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                  (party_is_active, ":ai_object")],
"We are fighting against {s1}{s5}.", "lord_pretalk",[
     (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
     (try_begin),
       (eq, ":ai_object", "p_main_party"),
       (str_store_string, s1, "@your party"),
     (else_try),
       (str_store_party_name, s1, ":ai_object"),
     (try_end)]],

[anyone,"lord_tell_objective", [(party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_accompanying_army)],
"We are accompanying {s1}{s5}.", "lord_pretalk",[(party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                                 (str_store_party_name, s1, ":ai_object")]],


[anyone,"lord_tell_objective",[
     (assign, ":pass", 0),
     (try_begin),
       (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_undefined),
       (assign, ":pass", 1),
     (else_try),
       (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_engaging_army),
       (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
       (neg|party_is_active, ":ai_object"),
       (assign, ":pass", 1),
     (try_end),
     (eq, ":pass", 1)],
"We are reconsidering our next objective.", "lord_pretalk",[]],

[anyone,"lord_tell_objective", [],
"I don't know: {reg1} {s1}", "lord_pretalk",[(party_get_slot, reg1, "$g_talk_troop_party", slot_party_ai_state),
                                             (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
                                             (str_store_party_name, s1, ":ai_object")]],

  #[anyone|plyr,"lord_talk",
   # [
     # (eq, "$talk_context", tc_party_encounter),
     # (eq, "$g_talk_troop_faction", "$players_kingdom"),
     # (party_slot_eq, "$g_encountered_party", slot_party_following_player, 0),
     # (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_marshall, "trp_player"),
     # ],
   # "Will you follow me? I have a plan.", "lord_ask_follow",[]],

  #[anyone,"lord_ask_follow", [(party_get_slot, ":dont_follow_until_time", "$g_encountered_party", slot_party_dont_follow_player_until_time),
                              # (store_current_hours, ":cur_time"),
                              # (lt, ":cur_time", ":dont_follow_until_time")],
   # "I enjoy your company, {playername}, but there are other things I must attend to. Perhaps in a few days I can ride with you again.", "close_window",
   # [(assign, "$g_leave_encounter",1)]],

  #[anyone,"lord_ask_follow", [(troop_get_slot, ":troop_renown", "$g_talk_troop", slot_troop_renown),
                              # (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
                              # (val_mul, ":troop_renown", 3),
                              # (val_div, ":troop_renown", 4),
                              # (lt, ":player_renown", ":troop_renown"),
                              # ],
   # "That would hardly be proper, {playername}. Why don't you follow me instead?", "close_window",
   # [(assign, "$g_leave_encounter",1)]],

  #[anyone,"lord_ask_follow", [(lt, "$g_talk_troop_relation", 25)],
   # "{s43}", "close_window",
   # [
       # (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_follow_refusal_default"),
       # (assign, "$g_leave_encounter",1)]],
# #Post 0907 changes end

  #[anyone,"lord_ask_follow", [],
   # "Lead the way, {playername}! Let us bring death and defeat to all our enemies.", "close_window",
   # [(party_set_slot, "$g_talk_troop_party", slot_party_commander_party, "p_main_party"),
    # (call_script, "script_party_decide_next_ai_state_under_command", "$g_talk_troop_party"),
    # (store_current_hours, ":follow_until_time"),
    # (store_add, ":follow_period", 30, "$g_talk_troop_relation"),
    # (val_div, ":follow_period", 2),
    # (val_add, ":follow_until_time", ":follow_period"),
    # (party_set_slot, "$g_encountered_party", slot_party_follow_player_until_time, ":follow_until_time"),
    # (party_set_slot, "$g_encountered_party", slot_party_following_player, 1),
    # (assign, "$g_leave_encounter",1)]],

 #[anyone,"lord_talk_preoffer", [], "Yes?", "lord_talk_offer",[]],
#[anyone|plyr,"lord_talk_offer", [(eq,1,0)], "I wish to ransom one of your prisoners.", "knight_offer_join",[]],
 #[anyone|plyr,"lord_talk_offer", [], "Never mind.", "lord_pretalk",[]],

 #[anyone ,"knight_offer_join", [(call_script, "script_cf_is_quest_troop", "$g_talk_troop")],
   # "I fear I cannot join you at the moment, {playername}, I've important business to attend to and it cannot wait.", "hero_pretalk",[]],

 #[anyone ,"knight_offer_join", [(lt, "$g_talk_troop_relation", 5),
                                 # (store_character_level,":player_level","trp_player"),
                                 # (store_character_level,":talk_troop_level","$g_talk_troop"),
                                 # (val_mul,":player_level",2),
                                 # (lt, ":player_level", ":talk_troop_level")],
# "You forget your place, {sir/madam}. I do not take orders from the likes of you.", "hero_pretalk",[]],
  
 #[anyone ,"knight_offer_join", [
       # (assign, ":num_player_companions",0),
       # (try_for_range, ":hero_id", heroes_begin, heroes_end),
         # (troop_slot_eq, ":hero_id",slot_troop_occupation, slto_player_companion),
         # (val_add, ":num_player_companions",1),
       # (try_end),
       # (assign, reg5, ":num_player_companions"),
       # (store_add, reg6, reg5, 1),
       # (val_mul, reg6,reg6),
       # (val_mul, reg6, 1000),
       # (gt, reg6,0)], #note that we abuse the value of reg6 in the next line.
 # "I would be glad to fight at your side, my friend, but there is a problem...\
 # The thing is, I've found myself in a bit of debt that I must repay very soon. {reg6} denars altogether,\
 # and I am honour-bound to return every coin. Unless you've got {reg6} denars with you that you can spare,\
 # I've to keep my mind on getting this weight off my neck.", "knight_offer_join_2",[]],

 #[anyone ,"knight_offer_join", [(gt,reg6, 100000)], "Join you? I think not.", "close_window",[]],
 #[anyone ,"knight_offer_join", [], "Aye, my friend, I'll be happy to join you.", "knight_offer_join_2",[]],
 #[anyone|plyr,"knight_offer_join_2", [(gt, reg6,0),(store_troop_gold, ":gold", "trp_player"),(gt,":gold",reg6)],
# "Here, take it, all {reg6} denars you need. 'Tis only money.", "knight_offer_join_accept",[(troop_remove_gold, "trp_player",reg6)]],
 #[anyone|plyr,"knight_offer_join_2", [(le, reg6,0)], "Then let us ride together, my friend.", "knight_offer_join_accept",[]],
 #[anyone|plyr,"knight_offer_join_2", [(eq, "$talk_context", tc_hero_freed)], "That's good to know. I will think on it.", "close_window",[]],
 #[anyone|plyr,"knight_offer_join_2", [(neq, "$talk_context", tc_hero_freed)], "That's good to know. I will think on it.", "hero_pretalk",[]],
  
  
 #[anyone ,"knight_offer_join_accept", [(troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1)],
# "I've some trusted men in my band who could be of use to you. What do you wish to do with them?", "knight_offer_join_accept_party",[]],
 #[anyone ,"knight_offer_join_accept", [], "Ah, certainly, it might be fun!", "close_window",[
      # (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
      # (assign, "$g_leave_encounter",1)]],
  
 #[anyone|plyr,"knight_offer_join_accept_party", [], "You may disband your men. I've no need for other troops.", "knight_join_party_disband",[]],
 #[anyone|plyr,"knight_offer_join_accept_party", [(troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
                                       # (party_can_join_party,":companions_party","p_main_party")], 
# "Your men may join as well. We need every soldier we can muster.", "knight_join_party_join",[]],
 #[anyone|plyr,"knight_offer_join_accept_party", [(is_between,"$g_encountered_party",centers_begin, centers_end)], 
# "Lead your men out of the town. I shall catch up with you on the road.", "knight_join_party_lead_out",[]],
 #[anyone|plyr,"knight_offer_join_accept_party", [(neg|is_between,"$g_encountered_party",centers_begin, centers_end)],
# "Keep doing what you were doing. I'll catch up with you later.", "knight_join_party_lead_out",[]],


 #[anyone ,"knight_join_party_disband", [], "Ah . . . Very well, {playername}. Much as I dislike losing good men,\
 # the decision is yours. I'll disband my troops and join you.", "close_window",[
      # (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
      # (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
      # (party_detach, ":companions_party"),
      # (remove_party, ":companions_party"),
      # (assign, "$g_leave_encounter",1)]],

 #[anyone ,"knight_join_party_join", [], "Excellent.\
 # My lads and I will ride with you.", "close_window",[
      # (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
      # (party_remove_members, "p_main_party", "$g_talk_troop", 1),
      # (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
      # (assign, "$g_move_heroes", 1),
      # (call_script, "script_party_add_party", "p_main_party", ":companions_party"),
      # (party_detach, ":companions_party"),
      # (remove_party, ":companions_party"),
      # (assign, "$g_leave_encounter",1)]],

 #[anyone ,"knight_join_party_lead_out", [], "Very well then.\
 # I shall maintain a patrol of this area. Return if you have further orders for me.", "close_window",[
      # (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
      # (party_remove_members, "p_main_party", "$g_talk_troop", 1),
      # (troop_get_slot, ":companions_party","$g_talk_troop", slot_troop_leaded_party),
      # (party_set_faction, ":companions_party", "fac_player_supporters_faction"),
      # (party_detach, ":companions_party"),
      # (party_set_ai_behavior, ":companions_party", ai_bhvr_patrol_location),
      # (party_set_flags, ":companions_party", pf_default_behavior, 0)]],



#Active quests
##### TODO: QUESTS COMMENT OUT BEGIN

# TLD - mirkwood sorcerer quest finish (GA, fixed by CppCoder) -- begin.

[anyone|plyr,"lord_active_mission_1", [	(store_partner_quest,":lords_quest"),
                       			(eq,":lords_quest","qst_mirkwood_sorcerer"),
                       			(check_quest_succeeded, "qst_mirkwood_sorcerer")],
"The sorcerer of Mirkwood has been slain, my Lady.", "lord_mission_sorcerer_completed",[]],

# CppCoder: Need someone to improve this dialog below...
[anyone|plyr,"lord_active_mission_1", [	(store_partner_quest,":lords_quest"),
                       			(eq,":lords_quest","qst_mirkwood_sorcerer"),
                       			(check_quest_failed, "qst_mirkwood_sorcerer"),
					(quest_slot_eq,"qst_mirkwood_sorcerer",slot_quest_current_state,0),],
"Forgive me, my Lady, but urgent matters have prevented me from slaying the sorcerer, and in the meantime he has fled.", "lord_mission_sorcerer_failed",[]], 

[anyone|plyr,"lord_active_mission_1", [	(store_partner_quest,":lords_quest"),
                       			(eq,":lords_quest","qst_mirkwood_sorcerer"),
                       			(check_quest_failed, "qst_mirkwood_sorcerer"),
					(quest_slot_eq,"qst_mirkwood_sorcerer",slot_quest_current_state,3),],
"The sorcerer of Mirkwood still lives. We interrupted his rituals but he has fled.", "lord_mission_sorcerer_failed",[]],

[anyone,"lord_mission_sorcerer_completed", [], "Yes {playername}, I had sensed his death. The veil of sorcery has been lifted from the wood and much of my power has returned. You have performed a great service for our people and as such you are entitled to a gift. Take this...", "lord_pretalk",
[
	(call_script, "script_finish_quest", "qst_mirkwood_sorcerer", 100),
	(call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
	(call_script, "script_cf_gain_trait_elf_friend")
]],

[anyone,"lord_mission_sorcerer_failed", [], "Yes {playername}, I sense the dark arts of enemy still pressing upon us. His efforts seem greater now. It is unfortunate that you could not stop him. No doubt he will take additional precautions in future to ward against our efforts. He will likely never be found while Dol Guldur still stands. Thank you for your efforts but leave me now. I grow tired.", "lord_pretalk",
[
	(call_script,"script_stand_back"),
	(call_script, "script_finish_quest", "qst_mirkwood_sorcerer", 20),
]],

# TLD - mirkwood sorcerer quest finish (GA, fixed by CppCoder) -- end.

[anyone,"lord_active_mission_1", [(store_partner_quest,":lords_quest"),
                                    (eq,":lords_quest","qst_lend_companion"),
                                    #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                                    (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                                    (check_quest_active,"qst_lend_companion"),
                                    (quest_slot_eq, "qst_lend_companion", slot_quest_giver_troop, "$g_talk_troop"),
                                    (store_current_day, ":cur_day"),
                                    (quest_get_slot, ":quest_target_amount", "qst_lend_companion", slot_quest_target_amount),
                                    (ge, ":cur_day", ":quest_target_amount"),
##                                    (quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
##                                    (str_store_troop_name,s14,":quest_target_troop"),
##                                    (troop_get_type, reg3, ":quest_target_troop"),
                                    ],
"Oh, you want your companion back? I see...", "lord_lend_companion_end",[]],




[anyone,"lord_active_mission_1",[(store_partner_quest,":lords_quest"),
								(eq,":lords_quest","qst_lend_companion")],
"{playername}, I must beg your patience, I still have need of your companion. Please return later when things have settled.", "lord_pretalk",[]],
[anyone,"lord_active_mission_1", [], "Yes, have you made any progress on it?", "lord_active_mission_2",[]],

[anyone|plyr,"lord_active_mission_2",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                            (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                            (check_quest_active,"qst_capture_prisoners"),
                            (quest_slot_eq, "qst_capture_prisoners", slot_quest_giver_troop, "$g_talk_troop"),
                            (quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
                            #(quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
                            #(party_count_prisoners_of_type, ":count_prisoners", "p_main_party", ":quest_target_troop"),
                            (assign, ":count_prisoners", 0),
                            (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_main_party"),
                            (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
                              (party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
                              (neg|troop_is_hero, ":stack_troop"), #no heroes
                              (store_troop_faction, ":troop_faction", ":stack_troop"),
                              (is_between, ":troop_faction", kingdoms_begin, kingdoms_end), #no bandits
                              (store_relation, ":relation", ":troop_faction", "$g_talk_troop_faction"),
                              (lt, ":relation", 0), #no friendly bandits, like deserters
                              (party_prisoner_stack_get_size, ":stack_size","p_main_party",":stack_no"),
                              (val_add, ":count_prisoners", ":stack_size"),
                            (try_end),
                            (ge, ":count_prisoners", ":quest_target_amount"),
                            (assign, reg1, ":quest_target_amount")],
"Indeed. I brought you {reg1} prisoners.", "lord_generic_mission_thank",
   [(quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
    #(quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
    #MV: remove the last X prisoners
    (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_main_party"),
    (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
      (gt, ":quest_target_amount", 0),
      (party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
      (neg|troop_is_hero, ":stack_troop"), #no heroes
      (store_troop_faction, ":troop_faction", ":stack_troop"),
      (is_between, ":troop_faction", kingdoms_begin, kingdoms_end), #no bandits
      (store_relation, ":relation", ":troop_faction", "$g_talk_troop_faction"),
      (lt, ":relation", 0), #no friendly bandits, like deserters
      (party_prisoner_stack_get_size, ":stack_size","p_main_party",":stack_no"),
      (try_begin),
        (ge, ":quest_target_amount", ":stack_size"),
        (assign, ":to_remove", ":stack_size"),
      (else_try),
        (assign, ":to_remove", ":quest_target_amount"),
      (try_end),
      (val_sub, ":quest_target_amount", ":to_remove"),
      (party_remove_prisoners, "p_main_party", ":stack_troop", ":to_remove"),
    (try_end),
    #(party_remove_prisoners, "p_main_party", ":quest_target_troop", ":quest_target_amount"),
    #(party_add_prisoners, "$g_encountered_party", ":quest_target_troop", ":quest_target_amount"),
    (call_script, "script_finish_quest", "qst_capture_prisoners", 100)]],

[anyone|plyr,"lord_active_mission_2",[#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                            (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                            (check_quest_active,"qst_capture_prisoners"),
                            (quest_slot_eq, "qst_capture_prisoners", slot_quest_giver_troop, "$g_talk_troop"),
                            (quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
                            #(quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
                            #(party_count_prisoners_of_type, ":count_prisoners", "p_main_party", ":quest_target_troop"),
                            (assign, ":count_prisoners", 0),
                            (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_main_party"),
                            (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
                              (party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
                              (neg|troop_is_hero, ":stack_troop"), #no heroes
                              (store_troop_faction, ":troop_faction", ":stack_troop"),
                              (is_between, ":troop_faction", kingdoms_begin, kingdoms_end), #no bandits
                              (store_relation, ":relation", ":troop_faction", "$g_talk_troop_faction"),
                              (lt, ":relation", 0), #no friendly bandits, like deserters
                              (party_prisoner_stack_get_size, ":stack_size","p_main_party",":stack_no"),
                              (val_add, ":count_prisoners", ":stack_size"),
                            (try_end),
                            (gt, ":count_prisoners", ":quest_target_amount"),
                            (store_mul, ":max_prisoners", ":quest_target_amount", 2),
                            (val_min, ":max_prisoners", ":count_prisoners"),
                            (assign, "$temp", ":max_prisoners"),
                            (assign, reg2, ":max_prisoners"),
                            (assign, reg1, ":quest_target_amount")],
"Why, I have brought you {reg2} prisoners, in case {reg1} are not enough.", "lord_generic_mission_thank_extra",
   [#(quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
    (assign, ":quest_target_amount", "$temp"),
    (quest_set_slot, "qst_capture_prisoners", slot_quest_rank_reward, ":quest_target_amount"), #only increase rank reward, leave gold/xp the same (too much trouble)
    #MV: remove the last X prisoners
    (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_main_party"),
    (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
      (gt, ":quest_target_amount", 0),
      (party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
      (neg|troop_is_hero, ":stack_troop"), #no heroes
      (store_troop_faction, ":troop_faction", ":stack_troop"),
      (is_between, ":troop_faction", kingdoms_begin, kingdoms_end), #no bandits
      (store_relation, ":relation", ":troop_faction", "$g_talk_troop_faction"),
      (lt, ":relation", 0), #no friendly bandits, like deserters
      (party_prisoner_stack_get_size, ":stack_size","p_main_party",":stack_no"),
      (try_begin),
        (ge, ":quest_target_amount", ":stack_size"),
        (assign, ":to_remove", ":stack_size"),
      (else_try),
        (assign, ":to_remove", ":quest_target_amount"),
      (try_end),
      (val_sub, ":quest_target_amount", ":to_remove"),
      (party_remove_prisoners, "p_main_party", ":stack_troop", ":to_remove"),
    (try_end),
    #(party_remove_prisoners, "p_main_party", ":quest_target_troop", ":quest_target_amount"),
    #(party_add_prisoners, "$g_encountered_party", ":quest_target_troop", ":quest_target_amount"),
    (call_script, "script_finish_quest", "qst_capture_prisoners", 100)]],

[anyone|plyr,"lord_active_mission_2",[
                            (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),                           
                            (check_quest_succeeded,"qst_rescue_prisoners"),
                            (quest_slot_eq, "qst_rescue_prisoners", slot_quest_giver_troop, "$g_talk_troop"),
                            (quest_get_slot, ":quest_target_amount", "qst_rescue_prisoners", slot_quest_target_amount),
                             #slot_quest_current_state is where the actual number of rescued prisoners is kept
                            (quest_slot_ge, "qst_rescue_prisoners", slot_quest_current_state, ":quest_target_amount"),
                            (assign, reg1, ":quest_target_amount")],
"Indeed. I have rescued {reg1} allied prisoners and they joined my party.", "lord_generic_mission_thank", [(call_script, "script_finish_quest", "qst_rescue_prisoners", 100)]],

[anyone|plyr,"lord_active_mission_2",[
                            (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),                           
                            (check_quest_succeeded,"qst_scout_enemy_town"),
                            (quest_slot_eq, "qst_scout_enemy_town", slot_quest_giver_troop, "$g_talk_troop"),
                            (quest_slot_eq, "qst_scout_enemy_town", slot_quest_target_troop, 1), #scouted
                            (quest_get_slot, ":quest_target_center", "qst_scout_enemy_town", slot_quest_target_center),
                            (str_store_party_name, s13, ":quest_target_center")],
"Indeed. I have scouted {s13}.", "lord_generic_mission_thank", [(call_script, "script_finish_quest", "qst_scout_enemy_town", 100)]],

[anyone|plyr,"lord_active_mission_2",[
                            (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),                           
                            (check_quest_succeeded,"qst_dispatch_scouts"),
                            (quest_slot_eq, "qst_dispatch_scouts", slot_quest_giver_troop, "$g_talk_troop")],
"Indeed. I have dispatched the scouts.", "lord_generic_mission_thank", [(call_script, "script_finish_quest", "qst_dispatch_scouts", 100)]],

[anyone|plyr,"lord_active_mission_2",[
	(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),                           
	(check_quest_active, "qst_eliminate_patrols"),
	(quest_slot_eq, "qst_eliminate_patrols", slot_quest_giver_troop, "$g_talk_troop"),
	(quest_get_slot, ":quest_target_party_template", "qst_eliminate_patrols", slot_quest_target_party_template),
	(store_num_parties_destroyed_by_player, ":num_destroyed", ":quest_target_party_template"),
	(party_template_get_slot, ":previous_num_destroyed", ":quest_target_party_template", slot_party_template_num_killed),
	(val_sub, ":num_destroyed", ":previous_num_destroyed"),
	(quest_get_slot, ":to_destroy", "qst_eliminate_patrols", slot_quest_target_amount),
	(le, ":to_destroy", ":num_destroyed")],
"Indeed. I have defeated enough enemy parties.", "lord_generic_mission_thank", [(call_script, "script_finish_quest", "qst_eliminate_patrols", 100)]],

[anyone|plyr,"lord_active_mission_2",
   [ #(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
     (store_partner_quest, ":lords_quest"),
     (eq, ":lords_quest", "qst_capture_enemy_hero"),
     (assign, ":has_prisoner", 0),
     #(quest_get_slot, ":quest_target_faction", "qst_capture_enemy_hero", slot_quest_target_faction),
     (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_prisoner_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
       (troop_is_hero, ":stack_troop"),
       #(store_troop_faction, ":stack_faction", ":stack_troop"),
       #(eq, ":quest_target_faction", ":stack_faction"),
       (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
       (assign, ":has_prisoner", 1),
       (quest_set_slot, "qst_capture_enemy_hero", slot_quest_target_troop, ":stack_troop"),
     (try_end),
     (eq, ":has_prisoner", 1)],
"Oh, indeed. I've captured an enemy commander for you.", "capture_enemy_hero_thank", []],

[anyone,"capture_enemy_hero_thank", [],
"Many thanks, my friend. He will serve very well for questioning. You've done a fine work here.", "capture_enemy_hero_thank_2",
   [(quest_get_slot, ":quest_target_troop", "qst_capture_enemy_hero", slot_quest_target_troop),
     # (quest_get_slot, ":quest_target_faction", "qst_capture_enemy_hero", slot_quest_target_faction),
     (party_remove_prisoners, "p_main_party", ":quest_target_troop", 1),
     # (store_relation, ":reln", "$g_encountered_party_faction", ":quest_target_faction"),
     # (try_begin),
       # (lt, ":reln", 0),
       # (party_add_prisoners, "$g_encountered_party", ":quest_target_troop", 1), #Adding him to the dungeon
     # (else_try),
       #Do not add a non-enemy lord to the dungeon (due to recent diplomatic changes or due to a neutral town/castle)
       #(troop_set_slot, ":quest_target_troop", slot_troop_is_prisoner, 0),
       (troop_set_slot, ":quest_target_troop", slot_troop_prisoner_of_party, -1),
     # (try_end),
     # (quest_get_slot, ":reward", "qst_capture_enemy_hero", slot_quest_gold_reward),
     # (call_script, "script_troop_add_gold", "trp_player", ":reward"),
     # (add_xp_as_reward, 2500),
     # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4),
     (call_script, "script_finish_quest", "qst_capture_enemy_hero", 100),
     (try_begin),
       (eq, "$g_talk_troop_faction", "fac_gondor"),
       (call_script, "script_cf_gain_trait_stewards_blessing"),
     (try_end),
     (try_begin),
       (eq, "$g_talk_troop_faction", "fac_rohan"),
       (call_script, "script_cf_gain_trait_kings_man"),
     (try_end),
     (try_begin),
       (eq, "$g_talk_troop_faction", "fac_lorien"),
       (call_script, "script_cf_gain_trait_elf_friend"),
     (try_end),]],

[anyone|plyr,"capture_enemy_hero_thank_2", [], "Certainly, {s65}.", "lord_pretalk",[]],
[anyone|plyr,"capture_enemy_hero_thank_2", [], "It was nothing.", "lord_pretalk",[]],
#[anyone|plyr,"capture_enemy_hero_thank_2", [], "Give me more of a challenge next time.", "lord_pretalk",[]],

##
##[anyone|plyr,"lord_active_mission_2", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                                         (store_partner_quest,":lords_quest"),
##                                         (eq,":lords_quest","qst_capture_messenger"),
##                                         (quest_get_slot, ":quest_target_troop", ":lords_quest", slot_quest_target_troop),
##                                         (quest_get_slot, ":quest_target_amount", ":lords_quest", slot_quest_target_amount),
##                                         (store_num_parties_destroyed_by_player, ":num_destroyed", "pt_messenger_party"),
##                                         (gt, ":num_destroyed", ":quest_target_amount"),
##                                         (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_target_troop"),
##                                         (ge, ":num_prisoners", 1),
##                                         (str_store_troop_name, 3, ":quest_target_troop")],
##   "Indeed sir. I have captured a {s3} my lord.", "lord_generic_mission_thank",[(quest_get_slot, ":quest_target_troop", "qst_capture_messenger", slot_quest_target_troop),
##                                                                     (party_remove_prisoners, "p_main_party", ":quest_target_troop", 1),
##                                                                     (party_add_prisoners, "$g_encountered_party", ":quest_target_troop", 1),#Adding him to the dungeon
##                                                                     (call_script, "script_finish_quest", "qst_capture_messenger", 100)]],
##  
##
[anyone|plyr,"lord_active_mission_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
										 (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                                         (store_partner_quest,":lords_quest"),
                                         (eq,":lords_quest","qst_raise_troops"),
                                         (quest_get_slot, ":quest_target_troop", ":lords_quest", slot_quest_target_troop),
                                         (quest_get_slot, ":quest_target_amount", ":lords_quest", slot_quest_target_amount),
                                         (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_target_troop"),
                                         (ge, ":num_companions", ":quest_target_amount"),
                                         (assign, reg1, ":quest_target_amount"),
                                         (str_store_troop_name_plural, s13, ":quest_target_troop")],
"Indeed. I have raised {reg1} {s13}. You can take them.", "lord_raise_troops_thank",[
	(quest_get_slot, ":quest_target_troop", "qst_raise_troops", slot_quest_target_troop),
	(quest_get_slot, ":quest_target_amount", "qst_raise_troops", slot_quest_target_amount),
	#(call_script,"script_change_player_relation_with_troop","$g_talk_troop",8),
	(party_remove_members, "p_main_party", ":quest_target_troop", ":quest_target_amount"),
	#(call_script, "script_end_quest", "qst_raise_troops"),
	(call_script, "script_finish_quest", "qst_raise_troops", 100),
	(troop_get_slot, ":cur_lords_party", "$g_talk_troop", slot_troop_leaded_party),
	(gt, ":cur_lords_party", 0),
	(party_add_members, ":cur_lords_party", ":quest_target_troop", ":quest_target_amount")]],

[anyone,"lord_raise_troops_thank", [],
"{s4}", "lord_raise_troops_thank_2",[
     (try_begin),
       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
       (str_store_string, s4, "@These soldiers may well turn the tide in my plans, {playername}. I am confident you've trained them well. My thanks and my compliments to you."),
     (else_try),
       (str_store_string, s4, "@Good work in shaping up those recruits, {playername}, you have been most useful. Hopefully they'll last longer than the last batch, but come see me again if they don't."),
     (try_end)]],

[anyone|plyr,"lord_raise_troops_thank_2", [],
"{s4}", "lord_pretalk",[
     (try_begin),
       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
       (str_store_string, s4, "@Well, the soldiers are at your command now, sir. I am sure you will take good care of them."),
     (else_try),
       (str_store_string, s4, "@Well, you may do as you please. My companions and I can always toughen up more if needed."),
     (try_end)]],

[anyone|plyr,"lord_active_mission_2", [(store_partner_quest,":lords_quest"),
                                         (eq, ":lords_quest", "qst_hunt_down_fugitive"),
                                         (check_quest_succeeded, "qst_hunt_down_fugitive"),
                                         (quest_get_slot, ":quest_target_center", "qst_hunt_down_fugitive", slot_quest_target_center),
                                         (str_store_party_name, s3, ":quest_target_center"),
                                         (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
                                         (quest_get_slot, ":quest_object_troop", "qst_hunt_down_fugitive", slot_quest_object_troop),
                                         (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna", ":quest_object_troop"),
                                         (str_store_string, s4, s50),],
"I found {s4} hiding in {s3} and gave him his punishment.", "lord_hunt_down_fugitive_success",[]],

[anyone|plyr,"lord_active_mission_2", [(store_partner_quest,":lords_quest"),
                                         (eq, ":lords_quest", "qst_hunt_down_fugitive"),
                                         (check_quest_failed, "qst_hunt_down_fugitive")],
"I'm afraid he got away.", "lord_hunt_down_fugitive_fail", []],

[anyone,"lord_hunt_down_fugitive_success", [],
"And we'll all be a lot better off without him! Thank you, {playername}, \
 for removing this long-festering thorn from my side. 'Tis good to know you can be trusted to handle things \
 with an appropriate level of tactfulness. \
 I've sent a note to our intendants already, and you can count on additional supplies from us.", "lord_hunt_down_fugitive_success_2", []],
  
[anyone|plyr,"lord_hunt_down_fugitive_success_2", [],
"Thank you, {s65}.", "lord_hunt_down_fugitive_reward_accept",[]],
  #[anyone|plyr,"lord_hunt_down_fugitive_success_2", [(faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good)],
   # "This is blood money. I can't accept it.", "lord_hunt_down_fugitive_reward_reject",[]],

#Post 0907 changes begin
[anyone,"lord_hunt_down_fugitive_reward_accept", [],
"I'll notify our intendants of your service, {playername}. Once again, you've my thanks for ridding me of that {s44}.", "lord_pretalk",[
       (troop_get_slot, ":insult_string", "$g_talk_troop", slot_lord_reputation_type),
       (val_add, ":insult_string", "str_lord_insult_default"),
       (str_store_string, s44, ":insult_string"),
       # (call_script, "script_troop_add_gold", "trp_player", 300),
       # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
       (call_script, "script_finish_quest", "qst_hunt_down_fugitive", 100)]],

  #[anyone,"lord_hunt_down_fugitive_reward_reject", [],
   # "You are a person for whom justice is its own reward, eh? As you wish it, {playername}, as you wish it.\
 # An honourable sentiment, to be true. Regardless, you've my thanks for ridding me of that {s44}.", "lord_pretalk",[

       # (troop_get_slot, ":insult_string", "$g_talk_troop", slot_lord_reputation_type),
       # (val_add, ":insult_string", "str_lord_insult_default"),
       # (str_store_string, s44, ":insult_string"),
       
       # #(call_script, "script_change_player_honor", 3),
       # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
       # (call_script, "script_end_quest", "qst_hunt_down_fugitive"),
       # ]],

[anyone,"lord_hunt_down_fugitive_fail", [],
"It is a sad day when that {s44} manages to avoid my grasp yet again.\
 I thought you would be able to do this, {playername}. Clearly I was wrong.", "lord_pretalk",
   [(troop_get_slot, ":insult_string", "$g_talk_troop", slot_lord_reputation_type),
    (val_add, ":insult_string", "str_lord_insult_default"),
    (str_store_string, 44, ":insult_string"),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (call_script, "script_end_quest", "qst_hunt_down_fugitive")]],
#Post 0907 changes end



##
##
##[anyone|plyr,"lord_active_mission_2", [(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
##                                         (store_partner_quest,":lords_quest"),
##                                         (eq,":lords_quest","qst_bring_back_deserters"),
##                                         (quest_get_slot, ":quest_target_troop", ":lords_quest", slot_quest_target_troop),
##                                         (quest_get_slot, ":quest_target_amount", ":lords_quest", slot_quest_target_amount),
##                                         (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_target_troop"),
##                                         (ge, ":num_prisoners", ":quest_target_amount"),
##                                         (assign, reg1, ":quest_target_amount")],
##   "Yes sir. I have brought {reg1} deserters as you asked me to.", "lord_generic_mission_thank",[(quest_get_slot, ":quest_target_troop", "qst_bring_back_deserters", slot_quest_target_troop),
##                                                                                     (quest_get_slot, ":quest_target_amount", "qst_bring_back_deserters", slot_quest_target_amount),
##                                                                                     (party_remove_prisoners, "p_main_party", ":quest_target_troop", ":quest_target_amount"),
##                                                                                     (faction_get_slot, ":faction_tier_2_troop", "$g_talk_troop_faction", slot_faction_tier_2_troop),
##                                                                                     (try_begin),
##                                                                                       (gt, ":faction_tier_2_troop", 0),
##                                                                                       (troop_get_slot, ":cur_lords_party", "$g_talk_troop", slot_troop_leaded_party),
##                                                                                       (gt, ":cur_lords_party", 0),
##                                                                                       (party_add_members, ":cur_lords_party", ":faction_tier_2_troop", ":quest_target_amount"),
##                                                                                     (try_end),
##                                                                                     (call_script, "script_finish_quest", "qst_bring_back_deserters", 100)]],
## 
##
##### TODO: QUESTS COMMENT OUT END
[anyone|plyr,"lord_active_mission_2", [], "I am still working on it.", "lord_active_mission_3",[]],
[anyone|plyr,"lord_active_mission_2", [(store_partner_quest,":lords_quest"),(neq, ":lords_quest", "qst_mirkwood_sorcerer")], "I am afraid I won't be able to do this quest.", "lord_mission_failed",[]],
[anyone,"lord_active_mission_3", [], "Good. Remember, I am counting on you.", "lord_pretalk",[]],

#Post 0907 changes begin
[anyone,"lord_mission_failed", [], "{s43}", "lord_pretalk",
   [(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_mission_failed_default"),
    (store_partner_quest,":lords_quest"),
    (try_begin),(eq, ":lords_quest", "qst_capture_troll"),(troop_remove_item,"trp_player","itm_wheeled_cage"),(try_end), # CppCoder: Remove wheeled cage when failed/ended quest
    (call_script, "script_abort_quest", ":lords_quest", 1)]],
#Post 0907 changes end
  

##### TODO: QUESTS COMMENT OUT BEGIN
#Request Mission
 
[anyone,"lord_request_mission_ask", [(store_partner_quest,":lords_quest"),(ge,":lords_quest",0)],
"You still haven't finished the last task I gave you, {playername}. You should be working on that, not asking me for other things to do.", "lord_pretalk",[]],

[anyone,"lord_request_mission_ask", [(troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 1)],
"I don't have any other task for you right now.", "lord_pretalk",[]],
[anyone|auto_proceed,"lord_request_mission_ask", [], "A task?", "lord_tell_mission",
   [ (call_script, "script_get_random_quest", "$g_talk_troop"),
     (assign, "$random_quest_no", reg0)]],

    # TLD mission: capture troll (mtarini) -- begin 
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_capture_troll")],
"You are a brave servant, {playername}, and we will give you a glimpse of our plans.\
 We need fresh monstrous blood and flesh. We need it to twist it and bend it and torture it and tame it and reshape it and breed it, to forge and strengthen our own breeds of colossal warriors!", "lord_mission_capture_troll_1", []],
  
[anyone|plyr,"lord_mission_capture_troll_1", [], "How can I serve, Master?", "lord_mission_capture_troll_2",[]],

[anyone,"lord_mission_capture_troll_2", [], "A wild cave troll, {playername}. Capture one strong exemplar for me and bring it to me, alive. We need one more of them for Our experiments! Two, would be better. The more we have, the better.",
  "lord_mission_capture_troll_3",[]],

[anyone|plyr,"lord_mission_capture_troll_3", [], "Where can such a beast be found?",                   "lord_mission_capture_troll_infoa",[]],
[anyone|plyr,"lord_mission_capture_troll_3", [], "How can such a beast be captured?",                  "lord_mission_capture_troll_infob",[]],
[anyone|plyr,"lord_mission_capture_troll_3", [], "How can such a beast be transported to you?",        "lord_mission_capture_troll_infoc",[]],
[anyone|plyr,"lord_mission_capture_troll_3", [], "You shall have your wild troll, Master.",            "lord_mission_capture_troll_accepted",[]],
[anyone|plyr,"lord_mission_capture_troll_3", [], "Mercy, Master! That beast will smash me like a bug!","lord_mission_capture_troll_rejected",[]],

[anyone,"lord_mission_capture_troll_infoa", [], "In these time of blood and shadows, wild cave trolls are growing excited and they are spreading from their lairs in the Misty Mountains... the best place where to look would be around the caves there.","lord_mission_capture_troll_3",[]],
[anyone,"lord_mission_capture_troll_infob", [], "You shall find one, and take it down in combat. Fear not of killing it during the fight: a troll is too coriaceous a beast for your weapons to kill it right away... and they do recover, more than you would expect. After it falls over its own black blood, you shall carry it to our feet, still breathing.","lord_mission_capture_troll_3",[]],
[anyone,"lord_mission_capture_troll_infoc", [], "You will be provided with a robust wheeled cage. It harbours more than enough space for a troll, and it can be pulled around. Hasten your steps on the way back: not even the metal of the cage is totally safe against the fury of a troll blinded by rage and pain. Make sure it does not break free and kill you.","lord_mission_capture_troll_3",[]],
  
[anyone,"lord_mission_capture_troll_rejected", [], 
"Only now you reveal what you are really worth, but I knew that of you all along. Weak, coward {playername}. Now begone.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
   (assign, "$g_leave_encounter",1)]], 
 
[anyone,"lord_mission_capture_troll_accepted", [], 
"I knew I could count on your strength and bravery. Slaves, give to {playername} one of our wheeled cages! {playername}, return when you have my gift. I want it before {reg1} dawns are passed.", "lord_pretalk",[
    (troop_add_item, "trp_player","itm_wheeled_cage",0),
    # CppCoder bugfix: Fill out capture wild troll quest text.
    (str_store_troop_name_link,s9,"$g_talk_troop"),
    (setup_quest_text,"$random_quest_no"),
    (str_store_string, s2, "@{s9} asked you to bring back a savage troll for use in his army."),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (quest_get_slot, reg1, "$random_quest_no", slot_quest_expiration_days)]],
   
    # TLD mission: capture troll (mtarini) -- end

[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_kill_troll")],
"Our land is facing dangers that were unheard of in our times. People are disappearing in the outskirts of {s3}. Not only commoners, but even small armed groups who venture outside the walls never return. There have been the strangest rumors, but I know what we are facing.", "lord_tell_mission_kill_troll", [
	(quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
	(str_store_party_name_link,3,":quest_object_center")]],

	
[anyone,"lord_tell_mission_kill_troll", [],
"Wild trolls, {playername}. Giant beasts, twisted montrousities. They never ventured so far from their dark caves in the mountains but at least one of them have been sighted around {s3}. I don't know what witchery has caused this, but I need that thing to be dispatched.", "lord_mission_told",
    [  (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
       (str_store_party_name_link, s3, ":quest_object_center")]],

[anyone|plyr,"lord_mission_told", [(eq,"$random_quest_no","qst_kill_troll")],
"How can those beasts be fought?", "lord_mission_kill_troll_info_a",[]],

[anyone,"lord_mission_kill_troll_info_a", [],
"A troll is a dangerous creature indeed. A giant monster which possesses an incredible strength in its deformed muscles. Their skin is as hard as iron, and a tree trunk is but a small club when wielded in their hands. It is rumored that a single troll can esily best a group of half a dozen well armed and trained men, wasting each of them with a single blow. Not only men but horses too fear trolls. Be careful if you plan to charge one while mounted.", "lord_mission_told",[]],

[anyone|plyr,"lord_mission_told", [(eq,"$random_quest_no","qst_kill_troll")],
"Do you think it comes from Mordor, or Isengard?", "lord_mission_kill_troll_info_b",[]],

[anyone,"lord_mission_kill_troll_info_b",  [(quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
											(str_store_party_name_link,s3,":quest_object_center")],
"No, I don't think so. We have news that both the White Wizard and the Black Tower have all kinds of monsters among their ranks, but from what I hear the beast terrifying {s3} is one savage, untamed beast. Remember, there could be more than one. But you can be sure that some obscure craft from the Enemy has led this new plague upon us.", "lord_mission_told",[]],

# TLD mission: investigate fangorn (mtarini) -- begin 
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_investigate_fangorn")],
"Here is a mission for a trusted and brave servant like you, {playername}.\
 The strangest rumors reach my ears from the forest of Fangorn.\
 Minions sent to harvest wood, and even my commanders traversing the place, occasionally fail to return.\
 Other times, they report of mysterious losses among their troops.\
 They blame ghosts, spirits of the wood, ancient curses...\
 Nonsense! Puny excuses for their own cowardice or ineptitude!", "lord_mission_investigate_fangorn_0", []],

[anyone|plyr,"lord_mission_investigate_fangorn_0", [], "What do you command me to do about it, Master?", "lord_mission_investigate_fangorn_1",[]],
  
[anyone|plyr,"lord_mission_investigate_fangorn_0", [], "But Master, there is danger and pain in Fangorn! I've felt it myself!", "lord_mission_investigate_fangorn_rejected",[]],

[anyone,"lord_mission_investigate_fangorn_1", [],
"Maybe it is just that my other servants are unable to prevent the most cowardly worms in their troops from deserting.\
  Fools, blinded by superstitions. \
  Or, maybe, it is the treacherous ambushes of elven scum, hiding in the putrid trees as they usually do. \
  It could even be lowborn traitors from Rohan.\
  Or who knows what else. I want you to find out, {playername}.", "lord_mission_investigate_fangorn_2", []],
  
[anyone|plyr,"lord_mission_investigate_fangorn_2", [], "I fear no elves or spirit. Leave this to me, Master.", "lord_mission_investigate_fangorn_accepted",[]],
[anyone|plyr,"lord_mission_investigate_fangorn_2", [], "Master, pity your servant! Don't ask me to venture in that cursed place!", "lord_mission_investigate_fangorn_rejected",[]],

[anyone,"lord_mission_investigate_fangorn_rejected", [], "So you are like the other worms: a superstitious, worthless coward.\
  I overestimated you. Now, begone!", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
   (assign, "$g_leave_encounter",1)]], 
 
[anyone,"lord_mission_investigate_fangorn_accepted", [], 
"Good.\
 Go there and shed some light on this matter. Then return to me and report.\
 I expect to see you back with news before {reg1} dawns are passed.", "lord_pretalk",
   [
    (try_begin),
	# CppCoder bugfix: Fill out fangorn quest text.
	(eq, "$random_quest_no", "qst_investigate_fangorn"),
        (str_store_troop_name_link,s9,"$g_talk_troop"),
        (setup_quest_text, "qst_investigate_fangorn"),
        (str_store_string, s2, "@{s9} asked you to find out what is going on in the Fangorn Forest, and to report back."),
    (try_end),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (quest_get_slot, reg1, "$random_quest_no", slot_quest_expiration_days)]],
# TLD mission: investigate fangorn (mtarini) -- end

# TLD mission: Find the lost spears of king Bladorthin (Kolba) -- begin

[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_find_lost_spears")],
"Here is a mission for a trusted and brave commander like you, {playername}.\
 We are ill equipped to fight off the Rhun hordes.\
 Our armies are losing battles one by one.\
 A legend tells that once upon a time, there were spears made by Dwarves for the armies of the great King Bladorthin (long since dead),\
 each had a thrice-forged head and their shafts were inlaid with cunning gold, but they were never delivered or paid for..", "lord_mission_find_lost_spears", []],

[anyone|plyr,"lord_mission_find_lost_spears",[],
"What do you command me to do about it, my lord?","lord_mission_find_lost_spears_1",[]],

[anyone,"lord_mission_find_lost_spears_1",[],
"These weapons would increase the effectiveness of our armies, but above all they will lift the spirits of our men. You'll have to find these spears.\
 You'll have to go ask the dwarves for permission to search for the spears in the deeps of the Lonely Mountain.\
 Beware, you may encounter some orcs or trolls in the tunnels. Are you available for this task?","lord_mission_find_lost_spears_2",[]],

[anyone|plyr,"lord_mission_find_lost_spears_2", [], "I fear no orcs nor trolls! I will find these spears for you, my lord.","lord_mission_find_lost_spears_accepted",[]],
[anyone|plyr,"lord_mission_find_lost_spears_2", [], "I'm afraid I can't help you, my lord.","lord_mission_find_lost_spears_rejected",[]],

[anyone,"lord_mission_find_lost_spears_rejected", [], "I see that discretion is the better part of your valor. Maybe you should stick to scouting duties.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
   (assign, "$g_leave_encounter",1)]],

[anyone,"lord_mission_find_lost_spears_accepted", [], "Good luck then!","lord_pretalk",
     [
	(setup_quest_text,"qst_find_lost_spears"),
        (str_store_troop_name_link,s9,"$g_talk_troop"),
        (str_store_troop_name_link,s5,"trp_dwarf_lord"),
	(str_store_string, s2, "@{s9} asked you to find the lost spears the dwarves once made for King Bladorthin. You will have to ask {s5} for permission to search for the spears in the depths of the Lonely Mountain."),
	(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    	(call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    	(quest_get_slot, reg1, "$random_quest_no", slot_quest_expiration_days)
     ]
],

#TLD mission: Find the lost spears of king Bladorthin (Kolba) -- end

# TLD mission: slay mirkwood sorcerer (GA, fixed by CppCoder) -- begin

[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_mirkwood_sorcerer")], "There is an important service you can deliver to our people, {playername}.", "lord_mission_mirkwood_sorcerer", []],
[anyone, "lord_mission_mirkwood_sorcerer", [], "My power to defend and preserve Lothlorien has been diminished by the devices of the enemy. A master sorcerer of Dol Guldur is invoking powerful charms that inhibit our defenses. Though he is a mortal, he has become one of the enemies greatest pupils in the use of arcane rituals and he represents a great threat to our people. You must hunt him down and destroy him!", "lord_mission_mirkwood_sorcerer_0", []],
[anyone|plyr, "lord_mission_mirkwood_sorcerer_0", [], "Where can I find the sorcerer, my Lady?", "lord_mission_mirkwood_sorcerer_1", []],
[anyone, "lord_mission_mirkwood_sorcerer_1", [], "Search for him in Mirkwood forest, not far from Dol Guldur itself. He is both a well guarded and a cautious foe so you will need to use stealth to prevent the alarm from being raised. If he escapes, he will relocate to other dark places that we know not of and continue his wickedness unchallenged. There will be only one opportunity to defeat him. Much depends on your success. Go with our blessings.", "lord_mission_mirkwood_sorcerer_2", []],
[anyone|plyr, "lord_mission_mirkwood_sorcerer_2", [], "As you command, my Lady. I will try my best to eliminate this evil.", "lord_pretalk", 
[
	(setup_quest_text,"qst_mirkwood_sorcerer"),
        (str_store_troop_name_link,s9,"$g_talk_troop"),
	(str_store_string, s2, "@{s9} has asked you to slay the Dol Guldur sorcerer in Mirkwood."),
	(call_script, "script_start_quest", "qst_mirkwood_sorcerer", "$g_talk_troop"),	
	(quest_set_slot, "qst_mirkwood_sorcerer", slot_quest_current_state, 0),
	(quest_set_slot, "qst_mirkwood_sorcerer", slot_quest_dont_give_again_period, 10000), # can get it only once
	(call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
	(enable_party, "p_ancient_ruins"),
]
],
[anyone|plyr, "lord_mission_mirkwood_sorcerer_2", [], "Forgive me, my Lady. I have some pressing matters to attend before I can help your people with this endevour.", "lord_mission_mirkwood_sorcerer_rejected", []],
[anyone, "lord_mission_mirkwood_sorcerer_rejected", [], "I understand, {playername}. But do not tally for too long, I'm growing tired of resisting his evil magic.", "lord_pretalk",[(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]], 

# TLD mission: slay mirkwood sorcerer (GA, fixed by CppCoder) -- end

#TLD mission: nowy quest (Kolba) -- begin
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deliver_message")],
"I need to send a letter to {s13} who should be currently at {s4}.\
 If you will be heading towards there, would you deliver it to him?\
 The letter needs to be in his hands in 30 days.", "lord_mission_deliver_message",
   [ (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
     (str_store_troop_name_link,s13,":quest_target_troop"),
     (str_store_party_name_link,s4,":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
     (str_store_string, s2, "@{s9} asked you to take a message to {s13}. {s13} was believed to be at {s4} when you were given this quest.")]],

[anyone|plyr,"lord_mission_deliver_message", [], "Certainly, I intend to pass by {s4} and it would be no trouble.", "lord_mission_deliver_message_accepted",[]],
[anyone|plyr,"lord_mission_deliver_message", [], "I doubt I'll be seeing {s13} anytime soon, {s65}. You'd best send it with someone else.", "lord_mission_deliver_message_rejected",[]],
#[anyone|plyr,"lord_mission_deliver_message", [], "I am no errand boy, sir. Hire a courier for your trivialities.", "lord_mission_deliver_message_rejected_rudely",[]],

[anyone,"lord_mission_deliver_message_accepted", [], 
"I appreciate it, {playername}. Here's the letter. Give my regards to {s13} when you see him.", "close_window",
   [(call_script,"script_stand_back"),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    #(call_script, "script_troop_add_gold", "trp_player", 20),
    (call_script, "script_add_faction_rps", "$g_talk_troop_faction", 20),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
    (assign, "$g_leave_encounter",1)]],

[anyone,"lord_mission_deliver_message_rejected", [], 
"Ah, all right then. Well, I am sure I will find someone else.", "lord_pretalk", [
     (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
  
  #[anyone,"lord_mission_deliver_message_rejected_rudely", [], "Hm, is this how you respond to a polite request\
 # for a small favor? A poor show, {playername}. I didn't know you would take offence.", "lord_mission_deliver_message_rejected_rudely_2",[]],
    
  #[anyone|plyr,"lord_mission_deliver_message_rejected_rudely_2", [], "Then you shall know better from now on.", "lord_mission_deliver_message_rejected_rudely_3",[]],
  #[anyone|plyr,"lord_mission_deliver_message_rejected_rudely_2", [], "Forgive my temper, {s65}. I'll deliver your letter.", "lord_mission_deliver_message_accepted",[]],

  #[anyone,"lord_mission_deliver_message_rejected_rudely_3", [], "All right. I will remember that.", "close_window",[
    # (call_script, "script_change_player_relation_with_troop","$g_talk_troop",-4),
    # (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 150),
    # (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),    
    # (assign, "$g_leave_encounter",1),
      # ]],

[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deliver_message_to_enemy_lord")],
"I need to deliver a letter to {s13} of {s15}, who must be at {s4} currently.\
 If you are going towards there, would you deliver my letter to him? The letter needs to reach him in 40 days.", "lord_mission_deliver_message", [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
##     (str_store_party_name,2,"$g_encountered_party"),
     (str_store_troop_name_link,s13,":quest_target_troop"),
     (str_store_party_name_link,s4,":quest_target_center"),
     (store_troop_faction, ":target_faction", ":quest_target_troop"),
     (str_store_faction_name_link,s15,":target_faction"),
     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
     (str_store_string, s2, "@{s9} asked you to take a message to {s13} of {s15}. {s13} was believed to be at {s4} when you were given this quest.")]],

  
##
##[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deliver_message_to_lover")],
##   "My dear friend, I have a deep affection for {s3} and I believe she feels the same way for me as well.\
## Alas, her father {s5} finds me unsuitable for her and will do anything to prevent our union.\
## I really need your help. Please, will you take this letter to her? She should be at {s4} at the moment.", "lord_mission_told",
##   [
##     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##     (str_store_troop_name_link,1,"$g_talk_troop"),
##     (str_store_party_name_link,2,"$g_encountered_party"),
##     (str_store_troop_name_link,3,":quest_target_troop"),
##     (str_store_party_name_link,4,":quest_target_center"),
##     (setup_quest_text,"$random_quest_no"),
##     (try_begin),
##       (is_between, "$g_encountered_party", centers_begin, centers_end),
##       (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##     (else_try),
##       (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##     (try_end),
##   ]],
##
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_escort_messenger")],
"There is an urgent matter... My messenger is due to report on our battle plans to commanders in {s14}.\
 His trip has been postponed several times already with all the trouble on the roads,\
 but this time he must get through. So, I want to at least make sure he's well-guarded.\
 I trust you well, {playername} so I would be very grateful if you could escort him to {s14}\
 and make sure he arrives safe and sound.", "lord_mission_told", [
     #(quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_troop_name_link, s11, "$g_talk_troop"),
     (str_store_party_name_link, s14, ":quest_target_center"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to escort his messenger to {s14}.")]],

##
##[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_hunt_down_raiders")],
## "A messenger came with important news a few hours ago.\
## A group of enemy raiders have attacked a village near {s3}.\
## They have murdered anyone who tried to resist, stolen everything they could carry and put the rest to fire.\
## Now, they must be on their way back to their base at {s4}.\
## You must catch them on the way and make them pay for their crimes.", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
##       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##       (str_store_party_name_link,3,":quest_object_center"),
##       (str_store_party_name_link,4,":quest_target_center"),
##    ]],
##  
##[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_bring_back_deserters")],
## "I am worried about the growing number of deserters. If we don't do something about it, we may soon have noone left to fight in our wars.\
## I want you to go now and bring back {reg1} {s3}. I would ask you to hang the bastards but we are short of men and we need them back in the ranks.", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##      
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (str_store_troop_name_plural,3,":quest_target_troop"),
##       (assign, reg1, ":quest_target_amount"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##    ]],
##
##[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deliver_supply_to_center_under_siege")],
## "The enemy has besieged {s5}. Our brothers there are doing their best to fend off attacks, but they can't hold for long without supplies.\
## We need someone to take the supplies they need and make it into the town as soon as possible.\
## It's a very dangerous job, but if there's one person who can do it, it's you {playername}.\
## You can take the supplies from seneschal {s3}. When you arrive at {s5}, give them to the seneschal of that town.", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##       (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##      
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (str_store_troop_name_link,3,":quest_object_troop"),
##       (str_store_troop_name,4,":quest_target_troop"),
##       (str_store_party_name_link,5,":quest_target_center"),
##       (assign, reg1, ":quest_target_amount"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##    ]],
##
##[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_bring_reinforcements_to_siege")],
## "{s4} has besieged {s5} and God willing, that town will not hold for long.\
## Still I promised him to send {reg1} {s3} as reinforcements and I need someone to lead those men.\
## Can you take them to {s4}?", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##       (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##      
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (str_store_troop_name_plural,3,":quest_object_troop"),
##       (str_store_troop_name_link,4,":quest_target_troop"),
##       (str_store_party_name_link,5,":quest_target_center"),
##       (assign, reg1, ":quest_target_amount"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##    ]],
##

[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_lend_surgeon")],
"I have a friend here, an old warrior, who is very sick. Pestilence has infected an old battle wound,\
and unless he is seen to by a surgeon soon, he will surely die. This man is dear to me, {playername},\
but he's also stubborn as a hog and refuses to have anyone look at his injury because he doesn't trust the physicians here.\
I have heard that you've a capable surgeon with you. If you would let your surgeon come here and have a look,\
{reg3?she:he} may be able to convince him to give his consent to an operation.\
Please, I will be deeply indebted to you if you grant me this request.", "lord_mission_told",[
	(quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
	(str_store_troop_name_link,s1,"$g_talk_troop"),
	(str_store_party_name,s2,"$g_encountered_party"),
	(str_store_troop_name,s3,":quest_object_troop"),
	(troop_get_type, reg3, ":quest_object_troop"),(try_begin),(gt,reg3,1),(assign,reg3,0),(try_end), #MV: non-humans are male
	(setup_quest_text,"$random_quest_no"),
	(try_begin),
		(is_between, "$g_encountered_party", centers_begin, centers_end),
		(setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
	(else_try),
		(setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
	(try_end),
	(str_store_string, s2, "@Lend your experienced surgeon {s3} to {s1}.")]],

# GA: Deal with raiders
# [anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_deal_with_bandits_at_lords_village")],
# "A group of enemy raiders is bound to one of the nearby hamlets. \
# We have few spare soldiers here at the moment, and your help is urgently needed, {playername}.", "lord_mission_deal_with_bandits_told",
	# [(quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
	# (str_store_party_name_link,s15,":quest_target_center"),
	# (str_store_troop_name_link,s13,"$g_talk_troop"),
	# (setup_quest_text,"$random_quest_no"),
	# (str_store_string, s2, "@{s13} asked you to dedend the village from raiders and then report back to him.")]],

# [anyone|plyr,"lord_mission_deal_with_bandits_told", [],"Worry not, I will go and defend the people.", "lord_mission_deal_with_bandits_accepted",[]],
# [anyone|plyr,"lord_mission_deal_with_bandits_told", [],"You shall have to find help elsewhere, I am too busy.", "lord_mission_deal_with_bandits_rejected",[]],

# [anyone,"lord_mission_deal_with_bandits_accepted", [], "Hurry and pay those scum in their own blood", "close_window",
    # [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     # (call_script, "script_troop_add_gold", "trp_player", 200),
     # (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
     # (assign, "$g_leave_encounter",1)]],
# [anyone,"lord_mission_deal_with_bandits_rejected", [], "Ah... Very well then, forget I brought it up.", "lord_pretalk",
	# [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],

# Raise troops
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_raise_troops")],
"{s4}", "lord_tell_mission_raise_troops",[
     # (troop_get_slot, ":training_string", "$g_talk_troop", slot_lord_reputation_type),
     # (val_add, ":training_string", "str_troop_train_request_default"),
     # (str_store_string, s44, ":training_string")
     (try_begin),
       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
       (str_store_string, s4, "@No commander should have to admit this, {playername}, but I was inspecting my soldiers the other day\
 and there are such here who don't know which end of a sword to hold. They need someone to show them the meaning of valor.\
 You are a warrior of renown, {playername}. Will you train some troops for me? I would be grateful to you."),
     (else_try),
       (str_store_string, s4, "@No commander should have to admit this, {playername}, but I was inspecting my soldiers the other day\
 and executed some of them for incompetence. They need someone with steel in his back to flog some courage into them, or kill them trying.\
 You are a warrior of renown, {playername}. Will you train some troops for me? I can make it worthwhile for you."),
     (try_end)]],

[anyone|plyr,"lord_tell_mission_raise_troops", [], "How many men do you need?", "lord_tell_mission_raise_troops_2",[]],

[anyone,"lord_tell_mission_raise_troops_2", [], 
"If you can raise {reg1} {s14} and bring them to me, that will probably be enough.", "lord_mission_raise_troops_told",
   [ (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, reg1, "$random_quest_no", slot_quest_target_amount),
     (str_store_troop_name_link,s9,"$g_talk_troop"),
     (str_store_troop_name_plural,s14,":quest_target_troop"),
     (setup_quest_text,"$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to raise {reg1} {s14} and bring them to him.")]],

[anyone|plyr,"lord_mission_raise_troops_told", [(quest_get_slot, reg1, "$random_quest_no", slot_quest_target_amount)],
"Of course, {s65}. Give me {reg1} fresh recruits and I'll train them to be {s14}.", "lord_mission_raise_troops_accepted",[]],
[anyone|plyr,"lord_mission_raise_troops_told", [], "I am too busy these days to train anyone.", "lord_mission_raise_troops_rejected",[]],

[anyone,"lord_mission_raise_troops_accepted", [], 
"You've taken a weight off my shoulders, {playername}.\
 I shall tell my sergeants to send you the recruits and attach them to your command.\
 Also, I'll advance you some money to help with expenses. Here, this purse should do it.\
 Thank you for your help.", "close_window",
   [(call_script,"script_stand_back"),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    #(call_script, "script_troop_add_gold", "trp_player",100),
    (call_script, "script_add_faction_rps", "$g_talk_troop_faction", 100),
    
    (quest_get_slot, ":recruit_troop", "$random_quest_no", slot_quest_object_troop),
    (quest_get_slot, ":num_recruits", "$random_quest_no", slot_quest_target_amount),
    (party_add_members, "p_main_party", ":recruit_troop", ":num_recruits"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
    (assign, "$g_leave_encounter",1)]],

[anyone,"lord_mission_raise_troops_rejected", [], 
"Oh, of course. I had expected as much. Well, good luck to you then.", "lord_pretalk", [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
  

#Collect Taxes
  #[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_collect_taxes"),
                                # (assign, reg9, 0),
                                # (try_begin),
                                  # (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                  # (party_slot_eq, ":quest_target_center", slot_party_type, spt_town),
                                  # (assign, reg9, 1),
                                # (try_end),
                                # ], "You probably know that I am the lord of the {reg9?town:village} of {s3}.\
 # However, it has been months since {s3} has delivered the taxes and rents due me as its rightful lord.\
 # Apparently the populace there has grown unruly lately and I need someone to go there and remind them of\
 # their obligations. And to . . . persuade them if they won't listen.\
 # If you go there and raise the taxes they owe me, I will grant you one-fifth of everything you collect.", "lord_mission_collect_taxes_told",
   # [
     # (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     # (str_store_troop_name_link,s9,"$g_talk_troop"),
     # (str_store_party_name_link,s3,":quest_target_center"),
     # (setup_quest_text,"$random_quest_no"),
     # (str_store_string, s2, "@{s9} asked you to collect taxes from {s3}. He offered to leave you one-fifth of all the money you collect there."),
   # ]],

  #[anyone|plyr,"lord_mission_collect_taxes_told", [],
   # "A fair offer, {s65}. We have an agreement.", "lord_mission_collect_taxes_accepted",[]],
  #[anyone|plyr,"lord_mission_collect_taxes_told", [], "Forgive me, I don't have the time.", "lord_mission_collect_taxes_rejected",[]],

  #[anyone,"lord_mission_collect_taxes_accepted", [], "Welcome news, {playername}.\
 # I will entrust this matter to you.\
 # Remember, those {reg9?townsmen:peasants} are foxy beasts, they will make every excuse not to pay me my rightful incomes.\
 # Do not let them fool you.", "close_window",
   # [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    # (call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
    # (assign, "$g_leave_encounter",1),
    # (assign, reg9, 0),
    # (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
    # (try_begin),
      # (party_slot_eq, ":quest_target_center", slot_party_type, spt_town),
      # (assign, reg9, 1),
    # (try_end),
   # ]],
  
  #[anyone,"lord_mission_collect_taxes_rejected", [], "Oh, yes. Well, good luck to you then.", "lord_pretalk",
   # [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],

#Hunt down fugitive
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_hunt_down_fugitive")],
"I have something you could help with, an issue with the lawless villain known as {s4}. \
 He murdered one of my bodyguards and has been on the run from his judgment ever since.\
 There were news recently that the fugitive has been seen at {s3}.\
 You might be able to hunt him down and deliver him swift justice, and I'll reward you in turn.", "lord_mission_hunt_down_fugitive_told", [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":quest_target_dna", "$random_quest_no", slot_quest_target_dna),
     (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
     (str_store_troop_name_link,s9, "$g_talk_troop"),
     (str_store_party_name_link,s3, ":quest_target_center"),
     (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna", ":quest_object_troop"),
     (str_store_string, s4, s50),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to hunt down a fugitive named {s4}. He is currently believed to be at {s3}.")]],

[anyone|plyr,"lord_mission_hunt_down_fugitive_told", [], "Then I will hunt him down and execute the law.", "lord_mission_hunt_down_fugitive_accepted",[]],
[anyone|plyr,"lord_mission_hunt_down_fugitive_told", [], "I am too busy to go after him at the moment.", "lord_mission_hunt_down_fugitive_rejected",[]],

[anyone,"lord_mission_hunt_down_fugitive_accepted", [], 
"That's excellent, {playername}. \
 I will be grateful, and of course your prowess wil be duly noted. \
 Well, good hunting to you.", "close_window",
   [(call_script,"script_stand_back"),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
    (assign, "$g_leave_encounter",1)]],

[anyone,"lord_mission_hunt_down_fugitive_rejected", [], "As you wish, {playername}.\
I suppose there are plenty of bounty hunters around to get the job done . . .", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],



##[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_capture_messenger")],
##   "The enemy seems to be preparing for some kind of action and I want to know what their plans are.\
## Capture one of their messengers and bring him to me.", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##      
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (str_store_troop_name,3,":quest_target_troop"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##   ]],
##

  #[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_kill_local_merchant")],
   # "The wretched truth is that I owe a considerable sum of money to one of the merchants here in {s3}.\
 # I've no intention of paying it back, of course, but that loud-mouthed fool is making a terrible fuss about it.\
 # He even had the audacity to come and threaten me -- me! --\
 # with a letter of complaint to the trade guilds and bankers. Why, he'd ruin my good reputation!\
 # So I need a {man/woman} I can trust, someone who will guarantee the man's silence. For good.", "lord_mission_told_kill_local_merchant",
   # [
       # (str_store_troop_name_link,s9,"$g_talk_troop"),
       # (str_store_party_name_link,s3,"$current_town"),
       # (setup_quest_text,"$random_quest_no"),
       # (str_store_string, s2, "@{s9} asked you to assassinate a local merchant at {s3}."),
   # ]],
  
  #[anyone|plyr,"lord_mission_told_kill_local_merchant", [], "Worry not, he shan't breathe a word.", "lord_mission_accepted_kill_local_merchant",[]],
  #[anyone|plyr,"lord_mission_told_kill_local_merchant", [], "I'm no common murderer, sir. Find someone else for your dirty job.", "lord_mission_rejected",[]],

  #[anyone,"lord_mission_accepted_kill_local_merchant", [], "Very good. I trust in your skill and discretion,\
 # {playername}. Do not disappoint me.\
 # Go now and wait for my word, I'll send you a message telling when and where you can catch the merchant.\
 # Dispose of him for me and I shall reward you generously.", "close_window",
   # [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    # (assign, "$g_leave_town",1),
    # (assign, "$qst_kill_local_merchant_center", "$current_town"),
    # (rest_for_hours, 10, 4, 0),
    # (finish_mission),
    # ]],

  #[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_meet_spy_in_enemy_town"),
                                # (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                # (str_store_party_name, s13, ":quest_target_center"),
                                # (store_faction_of_party,":quest_target_center_faction",),
                                # (str_store_faction_name, s14, ":quest_target_center_faction"),
                                # ],
   # "I have a sensitive matter which needs tending to, {playername}, and no trustworthy retainers to take care of it. The fact is that I have a spy in {s13} to keep an eye on things for me, and report anything that might warrant my attention. Every week I send someone to collect the spy's reports and bring them back to me. The job's yours if you wish it.", "lord_mission_told_meet_spy_in_enemy_town",
   # [
   # ]],

  #[anyone|plyr,"lord_mission_told_meet_spy_in_enemy_town", [], "I don't mind a bit of skullduggery. Count me in.", "quest_meet_spy_in_enemy_town_accepted",[]],
  #[anyone|plyr,"lord_mission_told_meet_spy_in_enemy_town", [], "I must decline. This cloak-and-dagger work isn't fit for me.", "quest_meet_spy_in_enemy_town_rejected",[]],

  #[anyone,"quest_meet_spy_in_enemy_town_accepted", [], "Excellent! Make your way to {s13} as soon as you can, the spy will be waiting.", "quest_meet_spy_in_enemy_town_accepted_response",
   # [
     # (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     # (quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
     # (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
     # (val_add, ":countersign", countersigns_begin),
     # (str_store_troop_name_link, s9, "$g_talk_troop"),
     # (str_store_string, s11, ":secret_sign"),
     # (str_store_string, s12, ":countersign"),
     # (str_store_party_name_link, s13, ":quest_target_center"),
     # (setup_quest_text, "$random_quest_no"),
     # (str_store_string, s2, "@{s9} has asked you to meet with a spy in {s13}."),
     # (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     # (call_script, "script_cf_center_get_free_walker", ":quest_target_center"),
     # (call_script, "script_center_set_walker_to_type", ":quest_target_center", reg0, walkert_spy),
     # (str_store_item_name,s14,"$spy_item_worn"),
     # #TODO: Change this value
     # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     # (assign, "$g_leave_encounter",1),
    # ]],
  #[anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [(quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                                                  # (str_store_party_name_link, s13, ":quest_target_center")],
   # "{s13} is heavily defended. How can I get close without being noticed?", "quest_meet_spy_in_enemy_town_accepted_2",
   # []],
  #[anyone,"quest_meet_spy_in_enemy_town_accepted_2", [], "You shall have to use stealth. Take care to avoid enemy strongholds, villages and patrols, and don't bring too many men with you. If you fail to sneak in the first time, give it a while for the garrison to lower its guard again, or you may have a difficult time infiltrating the town.", "quest_meet_spy_in_enemy_town_accepted_response",
   # []],
  #[anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [], "How will I recognise the spy?", "quest_meet_spy_in_enemy_town_accepted_3",
   # []],
  #[anyone,"quest_meet_spy_in_enemy_town_accepted_3", [(quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                                      # (str_store_party_name_link, s13, ":quest_target_center"),
                                                      # (troop_get_type, reg7, "$spy_quest_troop"),
                                                      # (quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
                                                      # (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
                                                      # (val_add, ":countersign", countersigns_begin),
                                                      # (str_store_string, s11, ":secret_sign"),
                                                      # (str_store_string, s12, ":countersign"),],
   # "Once you get to {s13} you must talk to the locals, the spy will be one of them. If you think you've found the spy, say the phrase '{s11}' The spy will respond with the phrase '{s12}' Thus you will know the other, and {reg7?she:he} will give you any information {reg7?she:he}'s gathered in my service.", "quest_meet_spy_in_enemy_town_accepted_response",
   # []],
  #[anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [], "Will I be paid?", "quest_meet_spy_in_enemy_town_accepted_4",
   # []],
  #[anyone,"quest_meet_spy_in_enemy_town_accepted_4", [], "Of course, I have plenty of silver in my coffers for loyal {men/women} like you. Do well by me, {playername}, and you'll rise high.", "quest_meet_spy_in_enemy_town_accepted_response",
   # []],
  #[anyone|plyr,"quest_meet_spy_in_enemy_town_accepted_response", [], "I know what to do. Farewell, my lord.", "quest_meet_spy_in_enemy_town_accepted_end",
   # []],
  #[anyone,"quest_meet_spy_in_enemy_town_accepted_end", [(quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
                                                        # (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
                                                        # (val_add, ":countersign", countersigns_begin),
                                                        # (str_store_string, s11, ":secret_sign"),
                                                        # (str_store_string, s12, ":countersign")],
   # "Good luck, {playername}. Remember, the secret phrase is '{s11}' The counterphrase is '{s12}' Bring any reports back to me, and I'll compensate you for your trouble.", "lord_pretalk",
   # []],

  #[anyone,"quest_meet_spy_in_enemy_town_rejected", [], "As you wish, {playername}, but I strongly advise you to forget anything I told you about any spies. They do not exist, have never existed, and no one will ever find them. Remember that.", "lord_pretalk",
   # [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],


    

  #[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_raid_caravan_to_start_war"),
                                # (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
                                # (str_store_faction_name_link, s13, ":quest_target_faction")],
   # "This peace with {s13} ill suits me, {playername}. We've let those swine have their way for far too long.\
 # Now they get stronger with each passing and their arrogance knows no bounds.\
 # I say, we must wage war on them before it's too late!\
 # Unfortunately, some of the bleeding hearts among our realm's lords are blocking a possible declaration of war.\
 # Witless cowards with no stomach for blood.", "lord_mission_told_raid_caravan_to_start_war",
   # [
   # ]],

  #[anyone|plyr,"lord_mission_told_raid_caravan_to_start_war", [], "You are right, {s65}, but what can we do?", "lord_mission_tell_raid_caravan_to_start_war_2",[]],
  #[anyone|plyr,"lord_mission_told_raid_caravan_to_start_war", [], "I disagree, sir. Peace is prefarable to war.", "quest_raid_caravan_to_start_war_rejected_1",[]],

  #[anyone,"lord_mission_tell_raid_caravan_to_start_war_2", [(quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
                                                            # (str_store_faction_name_link, s13, ":quest_target_faction")],
   # "Ah, 'tis good to hear someone who understands!\
 # As a matter of fact, there is something we can do, {playername}. A little bit of provocation.\
 # The dogs in {s13} are very fond of their merchant caravans, and rely on them overmuch.\
 # If one of our war parties managed to enter their territory and pillage some of their caravans,\
 # they would have ample cause to declare war on our kingdom.\
 # And then, well, even the cowards among us must rise to defend themselves.\
 # So what do you say? Are you interested?", "lord_mission_tell_raid_caravan_to_start_war_3",[]],

  #[anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_3", [], "An excellent plan. Count me in.", "quest_raid_caravan_to_start_war_accepted",[]],
  #[anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_3", [], "Why don't you raid the caravans yourself?", "lord_mission_tell_raid_caravan_to_start_war_4",[]],

  #[anyone,"lord_mission_tell_raid_caravan_to_start_war_4", [
  	# ], "Well, {playername}, some of the lords in our kingdom\
 # won't like the idea of someone inciting a war without their consent.\
 # They are already looking for an excuse to get at me, and if I did this they could make me pay for it dearly.\
 # You, on the other hand, are young and well liked and daring, so you might just get away with it.\
 # And of course I will back you up and defend your actions against your opponents.\
 # All in all, a few lords might be upset at your endeavour, but I am sure you won't be bothered with that.", "lord_mission_tell_raid_caravan_to_start_war_5",[]],

  #[anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_5", [], "Then I will go and raid those caravans!", "quest_raid_caravan_to_start_war_accepted",[]],
  #[anyone|plyr,"lord_mission_tell_raid_caravan_to_start_war_5", [], "I don't like this. Find yourself someone else to take the blame for your schemes.", "quest_raid_caravan_to_start_war_rejected_2",[]],

  #[anyone,"quest_raid_caravan_to_start_war_accepted", [], "Very good!\
 # Now, don't forget that you must capture and loot at least {reg13} caravans to make sure that those fools in {s13} get really infuriated.\
 # Once you do that, return to me and make sure you are not captured by their patrols.\
 # If they catch you, our plan will fail without a doubt and you will be facing a long time in prisons.\
 # Now, good luck and good hunting to you.", "close_window",
   # [
     # (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     # (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
     # (str_store_troop_name_link, s9, "$g_talk_troop"),
     # (str_store_faction_name_link, s13, ":quest_target_faction"),
     # (assign, reg13, ":quest_target_amount"),
     # (setup_quest_text,"$random_quest_no"),
     # (str_store_string, s2, "@{s9} asked you to capture and loot {reg13} caravans so as to provoke a war with {s13}."),
     # (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     # (call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
     # (assign, "$g_leave_encounter",1),
    # ]],


  #[anyone,"quest_raid_caravan_to_start_war_rejected_1", [], "Ah, you think so? But how long will your precious peace last? Not long, believe me.", "lord_pretalk",
   # [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
  #[anyone,"quest_raid_caravan_to_start_war_rejected_2", [], "Hm. As you wish, {playername}.\
 # I thought you had some fire in you, but it seems I was wrong.", "lord_pretalk",
   # [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],


[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_bring_back_runaway_serfs")],
 "Well, some of the slaves working in {s4} have run away. \
 The ungrateful swine, whose lives we spared! \
 From what I've been hearing, they're running to {s3} as fast as they can,\
 and have split up into three groups to try and avoid capture.\
 I want you to capture all three groups and fetch them back to {s4} by whatever means necessary.\
 I should really have them hanged for attempting to escape, but we need hands now,\
 so I'll let them go off this time with a good beating.", "lord_mission_told", [
       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
       (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
       (str_store_troop_name_link, s9, "$g_talk_troop"),
       (str_store_party_name_link, s3, ":quest_target_center"),
       (str_store_party_name_link, s4, ":quest_object_center"),
       (setup_quest_text,"$random_quest_no"),
       (str_store_string, s2, "@{s9} asked you to catch the three groups of runaway slaves and bring them back to {s4}, alive and breathing. He said that all three groups are heading towards {s3}.")]],

[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_follow_spy")],
 "I have good information that a man in this very town is actually an enemy spy.\
 He should be seized and hanged for his impudence,\
 but we also believe that very soon he will leave town to meet with his master,\
 the man to whom the spy feeds all his little whispers.\
 The spy himself is of little import, but the master is a dangerous man, and could tell us a great deal\
 if we could only get our hands on him...", "lord_tell_mission_follow_spy",[]],
 
[anyone,"lord_tell_mission_follow_spy", [],
 "I want you to wait here until the spy leaves town. Then you must follow him, stealthily, to the meeting place.\
 You must take absolute care not to be seen by the spy on your way, else he may suspect foul play and turn back.\
 When the master appears, you must ambush and arrest them and bring the pair back to me.\
 Alive, if you please.", "lord_tell_mission_follow_spy_2",[]],

[anyone|plyr, "lord_tell_mission_follow_spy_2", [], "I'll do it, {s65}.", "lord_tell_mission_follow_spy_accepted", []],
[anyone|plyr, "lord_tell_mission_follow_spy_2", [], "No, this skulking is not for me.", "lord_tell_mission_follow_spy_rejected", []],

[anyone,"lord_tell_mission_follow_spy_accepted", [],
"Good, I'm sure you'll do a fine job of it. One of my men will point the spy out to you when he leaves,\
 so you will know the man to follow. Remember, I want them both, and I want them alive.", "close_window",
   [ (call_script,"script_stand_back"),
     (str_store_troop_name_link, s11, "$g_talk_troop"),
     (str_store_party_name_link, s12, "$g_encountered_party"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to follow the spy that will leave {s12}. Be careful not to let the spy see you on the way, or he may get suspicious and turn back. Once the spy meets with his accomplice, you are to capture them and bring them back to {s11}."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),

     (quest_get_slot, ":spy_partners_template", "qst_follow_spy", slot_quest_target_party),
     (spawn_around_party, "p_main_party", ":spy_partners_template"),
     (assign, "$qst_follow_spy_spy_partners_party", reg0),
     (party_set_position, "$qst_follow_spy_spy_partners_party", pos63),
     (party_set_ai_behavior, "$qst_follow_spy_spy_partners_party", ai_bhvr_hold),
     (party_set_flags, "$qst_follow_spy_spy_partners_party", pf_default_behavior, 0),
     (set_spawn_radius, 0),
     (quest_get_slot, ":spy_template", "qst_follow_spy", slot_quest_target_party_template),
     (spawn_around_party, "$g_encountered_party", ":spy_template"),
     (assign, "$qst_follow_spy_spy_party", reg0),
     (party_set_ai_behavior, "$qst_follow_spy_spy_party", ai_bhvr_travel_to_party),
     (party_set_ai_object, "$qst_follow_spy_spy_party", "$qst_follow_spy_spy_partners_party"),
     (party_set_flags, "$qst_follow_spy_spy_party", pf_default_behavior, 0),
     (assign, "$g_leave_town", 1),
     (rest_for_hours, 2, 4, 0)]], #no need to set g_leave_encounter to 1 since this quest can only be given at a town

[anyone,"lord_tell_mission_follow_spy_rejected", [], "A shame. Well, carry on as you were, {playername}...", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],



[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_capture_enemy_hero")],
 "There is a difficult job I need done, {playername}, and you may be the one who can carry it off.\
 I need someone to capture one of the enemy commanders and bring him to me.\
 Afterwards, I'll be able to question him on the enemy battle plans.\
 It is a simple enough job, but whomever you choose will be guarded by an elite band of personal retainers.\
 Are you up for a fight?", "lord_tell_mission_capture_enemy_hero", []],

[anyone|plyr, "lord_tell_mission_capture_enemy_hero", [], "Consider it done, {s65}.", "lord_tell_mission_capture_enemy_hero_accepted", []],
[anyone|plyr, "lord_tell_mission_capture_enemy_hero", [], "I must refuse, {s65}. I don't want to get close to any of them.", "lord_tell_mission_capture_enemy_hero_rejected", []],

[anyone,"lord_tell_mission_capture_enemy_hero_accepted", [],
"I like your spirit! Go and bring me one of our enemies,\
 and I'll toast your name in my hall when you return! And reward you for your efforts, of course...", "close_window",
   [ (call_script,"script_stand_back"),
     #(quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (str_store_troop_name_link, s11, "$g_talk_troop"),
     #(str_store_faction_name_link, s13, ":quest_target_faction"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to capture an enemy commander and then bring him back to {s11} for questioning."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter",1)]],

[anyone,"lord_tell_mission_capture_enemy_hero_rejected", [],
"Clearly you lack the mettle I had thought you possessed. Very well, {playername}, I will find someone else.", "lord_pretalk",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],



[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_lend_companion")],
"I don't have a task for you right now, but your companion {s3} is a skilled {reg3?lass:fellow}\
 and I need someone with {reg3?her:his} talents. Will you lend {reg3?her:him} to me for a while?", "lord_tell_mission_lend_companion", [
       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
       (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
       (val_add, ":quest_target_amount", 1),
       (assign, reg1, ":quest_target_amount"),
       (str_store_troop_name_link,s9,"$g_talk_troop"),
       (str_store_troop_name,s3,":quest_target_troop"),
       (setup_quest_text,"$random_quest_no"),
       (troop_get_type, reg3, ":quest_target_troop"),
       (try_begin),
         (gt, reg3, 1), #MV: non-humans are male
         (assign, reg3, 0),
       (try_end),
       (str_store_string, s2, "@{s9} asked you to lend your companion {s3} to him for a week.")]],

[anyone|plyr,"lord_tell_mission_lend_companion", [], "How long will you be needing {reg3?her:him}?", "lord_tell_mission_lend_companion_2", []],
[anyone,"lord_tell_mission_lend_companion_2", [], "Just a few days, a week at most.", "lord_mission_lend_companion_told", []],

[anyone|plyr,"lord_mission_lend_companion_told", [(quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),(str_store_troop_name,s3,":quest_target_troop"),],
"Then I will leave {s3} with you for one week.", "lord_tell_mission_lend_companion_accepted", []],

[anyone|plyr,"lord_mission_lend_companion_told", [(quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),(str_store_troop_name,s3,":quest_target_troop"),],
"I am sorry, but I cannot do without {s3} for a whole week.", "lord_tell_mission_lend_companion_rejected", []],

[anyone,"lord_tell_mission_lend_companion_accepted", [],
   "I cannot thank you enough, {playername}. Worry not, your companion shall be returned to you with due haste.", "close_window",
   [(call_script,"script_stand_back"),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
    (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
    (party_remove_members, "p_main_party", ":quest_target_troop", 1),
    (assign, "$g_leave_encounter",1)]],

[anyone,"lord_tell_mission_lend_companion_rejected", [],
"Well, that's damned unfortunate, but I suppose I cannot force you or {s3} to agree.\
 I shall have to make do without.", "lord_pretalk", [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],

 
  #[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_collect_debt")],
   # "Some time ago, I loaned out a considerable sum of money to {s3}. {reg4} denars, to be precise.\
 # He was supposed to pay it back within a month but I haven't received a copper from him since.\
 # That was months ago. If you could collect the debt from him on my behalf,\
 # I would be grateful indeed. I would even let you keep one fifth of the money for your trouble.\
 # What do you say?", "lord_tell_mission_collect_debt",
   # [
     # (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     # (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     # (quest_get_slot, reg4, "$random_quest_no", slot_quest_target_amount),
     # (str_store_troop_name_link,s9,"$g_talk_troop"),
     # (str_store_troop_name_link,s3,":quest_target_troop"),
     # (str_store_party_name_link,s4,":quest_target_center"),
     # (setup_quest_text,"$random_quest_no"),
     # (str_store_string, s2, "@{s9} asked you to collect the debt of {reg4} denars {s3} owes to him. {s3} was at {s4} when you were given this quest."),
   # ]],
  #[anyone|plyr,"lord_tell_mission_collect_debt", [],
 # "Do you know where I can find {s3}, {s65}?", "lord_tell_mission_collect_debt_2", []],
  #[anyone,"lord_tell_mission_collect_debt_2", [],
 # "If you leave now, you should be able to find him at {s4}.\
 # I've no doubt that he will be suitably embarassed by his conduct and give you all the money he owes me.", "lord_tell_mission_collect_debt_3", []],
  #[anyone|plyr,"lord_tell_mission_collect_debt_3", [], "Then I will talk to {s3} on your behalf.", "lord_tell_mission_collect_debt_accepted", []],
  #[anyone|plyr,"lord_tell_mission_collect_debt_3", [], "Forgive me, {s65}, but I doubt I would be more successful than yourself.", "lord_tell_mission_collect_debt_rejected", []],

  #[anyone,"lord_tell_mission_collect_debt_accepted", [], "You made me very happy by accepting this {playername}. Please, talk to {s3} and don't leave him without my money.", "close_window",
   # [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    # (call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
    # (assign, "$g_leave_encounter",1),
   # ]],

  #[anyone,"lord_tell_mission_collect_debt_rejected", [], "Perhaps not, {playername}. I suppose I'm never getting that money back...", "lord_pretalk",
   # [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],
 
##
##[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_capture_conspirators")],
## "TODO: I want you to capture troops in {reg1} conspirator parties that plan to rebel against me and join {s3}.", "lord_mission_told",
##   [
##       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
##       (assign, reg1, "$qst_capture_conspirators_num_parties_to_spawn"),
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (str_store_troop_name,3,":quest_target_troop"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##    ]],
##
##
##[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_defend_nobles_against_peasants")],
## "TODO: I want you to defend {reg1} noble parties against peasants.", "lord_mission_told",
##   [
##       (assign, reg1, "$qst_defend_nobles_against_peasants_num_noble_parties_to_spawn"),
##       (str_store_troop_name_link,1,"$g_talk_troop"),
##       (str_store_party_name_link,2,"$g_encountered_party"),
##       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
##    ]],
##
##

  #[anyone,"lord_tell_mission", [(eq, "$random_quest_no", "qst_incriminate_loyal_commander"),
                                # (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
                                # (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
                                # (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                # (str_store_troop_name_link, s13,":quest_target_troop"),
                                # (str_store_party_name_link, s14,":quest_target_center"),
                                # (str_store_troop_name_link, s15,":quest_object_troop"),
                                # ],
 # "I tell you, that blubbering fool {s13} is not fit to rule {s14}.\
 # God knows he would be divested of his lands in an instant were it not for one of his loyal vassals, {s15}.\
 # As long as he has his vassal aiding him, it will be a difficult job beating him.\
 # So I need to get {s15} out of the picture, and I have a plan just to do that...\
 # With your help, naturally.", "lord_tell_mission_incriminate_commander",[]],

  #[anyone|plyr,"lord_tell_mission_incriminate_commander", [], "{s66}, I am all ears.", "lord_tell_mission_incriminate_commander_2",[]],
  #[anyone|plyr,"lord_tell_mission_incriminate_commander", [], "I don't wish to involve myself in anything dishonourable against {s15}.", "lord_tell_mission_incriminate_commander_rejected",[]],

  #[anyone,"lord_tell_mission_incriminate_commander_rejected", [], "Dishonourable? Bah!\
 # I was hoping I could count on you, {playername}, but you've shown me what a fool I was.\
 # I shall have to find someone whose loyalty I can trust.", "lord_pretalk",
   # [(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-5),
    # (call_script, "script_change_player_honor", 2)]],

  #[anyone,"lord_tell_mission_incriminate_commander_2", [], "I have written a fake letter to {s15},\
 # bearing my own seal, which implicates him in a conspiracy with us to stage a coup in {s14}, in my favour.\
 # If we can make {s13} believe the letter is genuine, he will deal with {s15} very swiftly.\
 # Of course, the challenge there is to convince {s13} that the letter is indeed real...", "lord_tell_mission_incriminate_commander_3",[]],

  #[anyone|plyr,"lord_tell_mission_incriminate_commander_3", [], "Please continue, {s65}...", "lord_tell_mission_incriminate_commander_4",[]],
  #[anyone|plyr,"lord_tell_mission_incriminate_commander_3", [], "No, I will not sully myself with this dishonourable scheme.", "lord_tell_mission_incriminate_commander_rejected",[]],

  #[anyone,"lord_tell_mission_incriminate_commander_4", [], "This is where you come into play.\
 # You'll take the letter to {s14}, then give it to one of your soldiers and instruct him to take it to {s15}.\
 # I will have one of my spies inform the town garrison so that your man will be arrested on his way.\
 # The guards will then find the letter and take it to {s13}.\
 # They'll torture your man, of course, to try and get the truth out of him,\
 # but all he knows is that you ordered the letter to be delivered to {s15} under the utmost secrecy.\
 # {s13} knows you serve me, and the fool will certainly believe the whole charade.", "lord_tell_mission_incriminate_commander_5",[]],
  
  #[anyone|plyr,"lord_tell_mission_incriminate_commander_5", [], "Is that all?", "lord_tell_mission_incriminate_commander_7",[]],
  #[anyone,"lord_tell_mission_incriminate_commander_7", [(str_store_troop_name, s8, "$incriminate_quest_sacrificed_troop"),
                                                        # (str_store_troop_name_plural, s9, "$incriminate_quest_sacrificed_troop"),
      # ], "There is one more thing...\
 # Your messenger must be someone trustworthy. If you sent the letter with a simple peasant, someone expendable,\
 # {s13} might suspect a plot. He may have the wits of a snail, but even a snail can see the obvious.\
 # Give the letter to someone of rank. One of your {s9}, perhaps.", "lord_tell_mission_incriminate_commander_8",[]],
  #[anyone|plyr,"lord_tell_mission_incriminate_commander_8", [], "What? I can't send one of my trusted {s9} to his death!", "lord_tell_mission_incriminate_commander_9",[]],
  #[anyone|plyr,"lord_tell_mission_incriminate_commander_8", [], "Then a {s8} it will be.", "lord_tell_mission_incriminate_commander_fin",[]],
  #[anyone,"lord_tell_mission_incriminate_commander_9", [], "Come now, {playername}.\
 # There is a place for sentimentality, but this is not it. Believe me, you shall be generously compensated,\
 # and what is the purpose of soldiers if not to die at our say-so?", "lord_tell_mission_incriminate_commander_10",[]],
  #[anyone|plyr,"lord_tell_mission_incriminate_commander_10", [], "A {s8} it is.", "lord_tell_mission_incriminate_commander_fin",[]],
  #[anyone|plyr,"lord_tell_mission_incriminate_commander_10", [], "No, I'll not sacrifice one of my chosen men.", "lord_tell_mission_incriminate_commander_rejected",[]],
   
 #[anyone,"lord_tell_mission_incriminate_commander_fin", [], "I can't tell you how pleased I am to hear that,\
 # {playername}. You are removing one of the greatest obstacles in my path.\
 # Here is the letter, as well as 300 denars for your expenses.\
 # Remember, there'll be more once you succeed. Much, much more...", "lord_pretalk",
   # [
       # (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
       # (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
       # (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
       # (call_script, "script_troop_add_gold", "trp_player",300),
       # (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
       # (str_store_troop_name_link, s11,"$g_talk_troop"),
       # (str_store_troop_name_link, s13,":quest_target_troop"),
       # (str_store_party_name_link, s14,":quest_target_center"),
       # (str_store_troop_name_plural, s15,"$incriminate_quest_sacrificed_troop"),
       # (str_store_troop_name_link, s16,":quest_object_troop"),
       # (setup_quest_text,"$random_quest_no"),
       # (str_store_string, s2, "@{s11} gave you a fake letter to fool {s13} into banishing his vassal {s16}.\
 # You are to go near {s14}, give the letter to one of your {s15} and send him into the town as a messenger,\
 # believing his orders to be genuine."),
       # (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    # ]],

[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_capture_prisoners")],
 "Our scouts have noticed a recent increase in enemy activity.\
 Unfortunately they almost never succeed in capturing live prisoners and bring them in for questioning,\
 so we can piece together what the enemy is up to.\
 So, I need a good warrior to find me {reg1} enemy prisoners, that I may question them.", "lord_mission_told",
   [   #(quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
       (quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
       (assign,reg1,":quest_target_amount"),
       (str_store_troop_name_link,s9,"$g_talk_troop"),
##       (str_store_party_name,2,"$g_encountered_party"),
       #(str_store_troop_name_by_count,3,":quest_target_troop",":quest_target_amount"),
       (setup_quest_text,"$random_quest_no"),
##       (try_begin),
##         (is_between, "$g_encountered_party", centers_begin, centers_end),
##         (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##       (else_try),
##         (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##       (try_end),
       (str_store_string, s2, "@{s9} has requested you to bring him {reg1} enemy prisoners.")]],

[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_rescue_prisoners")],
 "{s5}", "lord_mission_told",
   [   (quest_get_slot, ":quest_target_amount", "qst_rescue_prisoners", slot_quest_target_amount),
       (assign,reg1,":quest_target_amount"),
       (str_store_troop_name_link,s9,"$g_talk_troop"),
       (try_begin),
         (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
         (str_store_string, s5, "@We have reports that several of our allied patrols were ambushed and defeated.\
 Some of the men may still yet live, captured by the enemy.\
 Yet, the morale of my troops suffers, as the captured men will surely be killed, imprisoned or worse.\
 I want you to rescue {reg1} prisoners, and bolster the morale of our troops."), #Good
       (else_try),
         (str_store_string, s5, "@We have reports that several of our patrols were ambushed and defeated.\
 Some of the cowards may still yet live, captured by the enemy.\
 As much as they are expendable, it's a waste to let them die in some prison hole.\
 I want you to rescue {reg1} prisoners, and make them fight for us again."), #Evil
       (try_end),
       (setup_quest_text, "qst_rescue_prisoners"),
       (str_store_string, s2, "@{s9} has asked you to rescue {reg1} prisoners.")]],

[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_scout_enemy_town")],
 "{s5}", "lord_mission_told",
   [   (quest_get_slot, ":quest_target_center", "qst_scout_enemy_town", slot_quest_target_center),
       (str_store_party_name, s13, ":quest_target_center"),
       (str_store_troop_name_link, s9, "$g_talk_troop"),
       (try_begin),
         (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
         (str_store_string, s5, "@We have reports that an enemy host may be gathering in {s13}.\
 Clearly, this is of grave concern to me, as I don't know how many troops the enemy has and whether my soldiers will be ready to meet them\
 on the field of battle.\
 I want you to get close enough to {s13}, and find out as much as you can."), #Good
       (else_try),
         (str_store_string, s5, "@My spies tell me of a large group of warriors gathering in {s13}.\
 They should be no match for us and our servants, but it wouldn't hurt to know just how many of them are there.\
 I want you to get close enough to {s13}, and find out as much as you can."), #Evil
       (try_end),
       (setup_quest_text, "qst_scout_enemy_town"),
       (str_store_string, s2, "@{s9} asked you to scout around {s13}.")]],
    
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_dispatch_scouts")],
"{s5}", "lord_mission_told", [
       (quest_get_slot, ":quest_target_center", "qst_dispatch_scouts", slot_quest_target_center),
       (str_store_party_name, s13, ":quest_target_center"),
       (str_store_troop_name_link, s9, "$g_talk_troop"),
       (try_begin),
         (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
         (str_store_string, s5, "@We have reports of some enemy activity near {s13}.\
 Our scouts have so far failed to get close enough and scout the area for enemy comings and goings.\
 I want you to assemble a scouting party, get close enough to {s13}, and dispatch the scouts."), #Good
       (else_try),
         (str_store_string, s5, "@My spies tell me the enemy is up to something in {s13}.\
 Our cowardly scouts have so far failed to get close enough and tell us anything of import.\
 I want you to recruit your own scouting party, get close enough to {s13}, and leave them there. Make sure they don't turn around and flee!"), #Evil
       (try_end),
#       (faction_get_slot, ":tier_1_troop", "$g_talk_troop_faction", slot_faction_tier_1_troop), #4 of these
#       (str_store_troop_name_plural, s16, ":tier_1_troop"),
#       (faction_get_slot, ":tier_2_troop", "$g_talk_troop_faction", slot_faction_tier_2_troop), #2 of these
#       (str_store_troop_name_plural, s15, ":tier_2_troop"),
       (str_store_faction_name, s15, "$g_talk_troop_faction"),
       (faction_get_slot, ":tier_3_troop", "$g_talk_troop_faction", slot_faction_tier_3_troop), #1 of these, and used for member chat
       (str_store_troop_name, s14, ":tier_3_troop"),
       (setup_quest_text, "qst_dispatch_scouts"),
       (str_store_string, s2, "@{s9} asked you to dispatch a scout party near {s13}.^Obtain 7 soldiers of {s15}, of which at least 1 is {s14}, get close to {s13} and talk to the {s14} to dispatch the party.")]],
    
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_eliminate_patrols")],
"{s5}", "lord_mission_told", [
       (quest_get_slot, ":quest_target_party_template", "qst_eliminate_patrols", slot_quest_target_party_template),
       (quest_get_slot, reg1, "qst_eliminate_patrols", slot_quest_target_amount),
       (spawn_around_party, "p_main_party", ":quest_target_party_template"),
       (assign, ":fake_party", reg0),
       (str_store_party_name, s13, ":fake_party"),
       (remove_party, ":fake_party"),
       (str_store_troop_name_link, s9, "$g_talk_troop"),
       (try_begin),
         (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
         (str_store_string, s5, "@We need to take the battle to the enemy, {playername}.\
 At this moment, we can do this by striking at his patrols and communications.\
 I want you to eliminate {reg1} {s13} parties, that would help us regain initiative."), #Good
       (else_try),
         (str_store_string, s5, "@We need to grind down our worthless enemies, {playername}.\
 Their patrols and supply trains are growing too bold for my liking.\
 I want you to eliminate {reg1} {s13} parties, so they'll learn to fear what's coming."), #Evil
       (try_end),
       (setup_quest_text, "qst_eliminate_patrols"),
       (str_store_string, s2, "@{s9} asked you to eliminate {reg1} {s13} parties.")]],
    

[anyone,"lord_tell_mission", [], "No, {playername}. I do not need your help at this time.", "lord_pretalk",[]],

[anyone|plyr,"lord_mission_told", [], "You can count on me, {s65}.", "lord_mission_accepted",[]],
[anyone|plyr,"lord_mission_told", [], "I fear I cannot accept such a mission at the moment.", "lord_mission_rejected",[]],

[anyone,"lord_mission_accepted", [], "Excellent, {playername}, excellent. I have every confidence in you.", "close_window",
   [(call_script,"script_stand_back"),
    (assign, "$g_leave_encounter",1),
    (try_begin),
      (eq, "$random_quest_no", "qst_escort_messenger"),
      (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
      #(troop_set_slot, ":quest_object_troop", slot_troop_cur_center, 0),
      (troop_join, ":quest_object_troop"),
    (else_try),
	  (eq, "$random_quest_no", "qst_kill_troll"),
	  (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
	  (set_spawn_radius, 3),
	  (spawn_around_party,":quest_object_center","pt_raging_trolls"),
	  (assign, ":quest_target_party", reg0),
	  (party_relocate_near_party, ":quest_target_party", ":quest_object_center"),
	  (quest_set_slot, "$random_quest_no", slot_quest_target_party, ":quest_target_party"),
	  (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
      (party_set_slot, ":quest_target_party", slot_party_ai_object, ":quest_object_center"),
      (party_set_slot, ":quest_target_party", slot_party_ai_state, spai_undefined),
      (party_set_ai_behavior, ":quest_target_party", ai_bhvr_patrol_location),
      (party_set_ai_patrol_radius, ":quest_target_party", 10),
	  # (str_store_troop_name,s1,"$g_talk_troop"),
	  # (str_store_party_name,s2,"$g_encountered_party"),
	  (str_store_troop_name_link,s9,"$g_talk_troop"),
      (str_store_party_name_link,s13,":quest_object_center"),
      (party_set_morale, ":quest_target_party", 20), # (CppCoder): Make trolls walk slower.
	 
      # (try_begin),
        # (is_between, "$g_encountered_party", centers_begin, centers_end),
        # (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
      # (else_try),
        # (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
      # (try_end),
      (setup_quest_text, "qst_kill_troll"),
      (str_store_string, s2, "@{s9} asked you to free {s13} from the menace of a Troll raging in its outskirts."),

##    (else_try),
##      (eq, "$random_quest_no", "qst_hunt_down_raiders"),
##      (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
##      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##      (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
##      (set_spawn_radius, 3),
##      (call_script, "script_cf_create_kingdom_party", ":quest_target_faction", spt_raider),
###      (spawn_around_party,":quest_object_center",":quest_target_party_template"),
##      (assign, ":quest_target_party", reg0),
##      (party_relocate_near_party, reg0, ":quest_object_center"),
##      (quest_set_slot, "$random_quest_no", slot_quest_target_party, ":quest_target_party"),
##      (party_set_ai_behavior,":quest_target_party",ai_bhvr_travel_to_party),
##      (party_set_ai_object,":quest_target_party",":quest_target_center"),
##      (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
##      (party_set_faction,":quest_target_party",":quest_target_faction"),
##      (str_store_troop_name,1,"$g_talk_troop"),
##      (str_store_party_name,2,"$g_encountered_party"),
##      (str_store_party_name,3,":quest_object_center"),
##      (str_store_party_name,4,":quest_target_center"),
##      (setup_quest_text,"$random_quest_no"),
##      (try_begin),
##        (is_between, "$g_encountered_party", centers_begin, centers_end),
##        (setup_quest_giver, "$random_quest_no", "str_given_by_s1_at_s2"),
##      (else_try),
##        (setup_quest_giver,"$random_quest_no", "str_given_by_s1_in_wilderness"),
##      (try_end),
##    (else_try),
##      (eq, "$random_quest_no", "qst_bring_reinforcements_to_siege"),
##      (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##      (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##      (troop_get_slot, ":cur_party", "$g_talk_troop", slot_troop_leaded_party),
##      (party_remove_members, ":cur_party", ":quest_object_troop", ":quest_target_amount"),
##      (party_add_members, "p_main_party", ":quest_object_troop", ":quest_target_amount"),
##    (else_try),
##      (eq, "$random_quest_no", "qst_bring_prisoners_to_enemy"),
##      (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
##      (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
##      (party_add_prisoners, "p_main_party", ":quest_object_troop", ":quest_target_amount"),
    (else_try),
      (eq, "$random_quest_no", "qst_deliver_message_to_enemy_lord"),
      #(call_script, "script_troop_add_gold", "trp_player",10),
      (call_script, "script_add_faction_rps", "$g_talk_troop_faction", 10),
    (else_try),
      (eq, "$random_quest_no", "qst_bring_back_runaway_serfs"),
      (quest_get_slot, ":quest_giver_center", "$random_quest_no", slot_quest_giver_center),
      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
      (quest_get_slot, ":quest_target_party_template", "$random_quest_no", slot_quest_target_party_template),

      (set_spawn_radius, 3),
      (spawn_around_party,":quest_giver_center",":quest_target_party_template"),
      (assign, "$qst_bring_back_runaway_serfs_party_1", reg0),
      (party_set_ai_behavior,"$qst_bring_back_runaway_serfs_party_1",ai_bhvr_travel_to_party),
      (party_set_ai_object,"$qst_bring_back_runaway_serfs_party_1",":quest_target_center"),
      (party_set_flags, "$qst_bring_back_runaway_serfs_party_1", pf_default_behavior, 0),
      (spawn_around_party,":quest_giver_center",":quest_target_party_template"),
      (assign, "$qst_bring_back_runaway_serfs_party_2", reg0),
      (party_set_ai_behavior,"$qst_bring_back_runaway_serfs_party_2",ai_bhvr_travel_to_party),
      (party_set_ai_object,"$qst_bring_back_runaway_serfs_party_2",":quest_target_center"),
      (party_set_flags, "$qst_bring_back_runaway_serfs_party_2", pf_default_behavior, 0),
      (spawn_around_party,":quest_giver_center",":quest_target_party_template"),
      (assign, "$qst_bring_back_runaway_serfs_party_3", reg0),
      (party_set_ai_behavior,"$qst_bring_back_runaway_serfs_party_3",ai_bhvr_travel_to_party),
      (party_set_ai_object,"$qst_bring_back_runaway_serfs_party_3",":quest_target_center"),
      (party_set_flags, "$qst_bring_back_runaway_serfs_party_3", pf_default_behavior, 0),
      (rest_for_hours, 2, 4), #TLD was 1,4
##    (else_try),
##      (eq, "$random_quest_no", "qst_capture_conspirators"),
##      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##      (spawn_around_party,"p_main_party","pt_conspirator_leader"),
##      (assign, "$qst_capture_conspirators_party_1", reg0),
##      (assign, "$qst_capture_conspirators_num_parties_spawned", 1),
##      (party_set_ai_behavior, "$qst_capture_conspirators_party_1", ai_bhvr_hold),
##      (party_set_flags, "$qst_capture_conspirators_party_1", pf_default_behavior, 0),
##      (party_get_position, pos1, ":quest_target_center"),
##      (call_script, "script_map_get_random_position_around_position_within_range", 17, 19),
##      (party_set_position, "$qst_capture_conspirators_party_1", pos2),
##      (party_get_num_companions, ":num_companions", "$qst_capture_conspirators_party_1"),
##      (val_add, "$qst_capture_conspirators_num_troops_to_capture", ":num_companions"),
##    (else_try),
##      (eq, "$random_quest_no", "qst_defend_nobles_against_peasants"),
##      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
##      (set_spawn_radius, 9),
##      (try_for_range, ":unused", 0, "$qst_defend_nobles_against_peasants_num_peasant_parties_to_spawn"),
##        (spawn_around_party, ":quest_target_center", "pt_peasant_rebels"),
##        (try_begin),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_1", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_1", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_2", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_2", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_3", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_3", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_4", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_4", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_5", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_5", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_6", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_6", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_7", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_7", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_peasant_party_8", 0),
##          (assign, "$qst_defend_nobles_against_peasants_peasant_party_8", reg0),
##        (try_end),
##      (try_end),
##      (set_spawn_radius, 0),
##      (party_get_position, pos1, ":quest_target_center"),
##      (try_for_range, ":unused", 0, "$qst_defend_nobles_against_peasants_num_noble_parties_to_spawn"),
##        (spawn_around_party, ":quest_target_center", "pt_noble_refugees"),
##        (assign, ":cur_noble_party", reg0),
##        (party_set_ai_behavior, ":cur_noble_party", ai_bhvr_travel_to_party),
##        (party_set_ai_object, ":cur_noble_party", ":quest_target_center"),
##	    (party_set_flags, ":cur_noble_party", pf_default_behavior, 0),
##        (call_script, "script_map_get_random_position_around_position_within_range", 13, 17),
##        (party_set_position, ":cur_noble_party", pos2),
##        (party_get_num_companions, ":num_companions", ":cur_noble_party"),
##        (val_add, "$qst_defend_nobles_against_peasants_num_nobles_to_save", ":num_companions"),
##        (try_begin),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_1", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_1", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_2", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_2", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_3", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_3", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_4", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_4", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_5", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_5", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_6", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_6", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_7", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_7", reg0),
##        (else_try),
##          (le, "$qst_defend_nobles_against_peasants_noble_party_8", 0),
##          (assign, "$qst_defend_nobles_against_peasants_noble_party_8", reg0),
##        (try_end),
##      (try_end),
	(try_end),
	(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
	(try_begin),
		(eq, "$random_quest_no", "qst_lend_surgeon"),
		(assign, "$g_leave_town_outside", 1),
		(assign,"$auto_enter_town","$g_encountered_party"),
#		(store_current_hours, "$quest_given_time"),
		(rest_for_hours, 4),
		(assign, "$lord_requested_to_talk_to", "$g_talk_troop"),
	(try_end)]],
	
[anyone,"lord_mission_rejected", [], 
"Is that so? Well, I suppose you're just not up to the task.\
 I shall have to look for somebody with more mettle.", "close_window",
   [(call_script,"script_stand_back"),
    (assign, "$g_leave_encounter",1),
    #(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (try_begin),
      (quest_slot_eq, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 0),
      (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 1),
    (try_end),
    (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],


##### TODO: QUESTS COMMENT OUT END

#Leave
[anyone|plyr,"lord_talk", [(troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0)], "I must leave now.", "lord_leave_prison",[]],
[anyone|plyr,"lord_talk", [(lt, "$g_talk_troop_faction_relation", 0)], "This little chat is over. I leave now.", "lord_leave",[]],
[anyone|plyr,"lord_talk", [(ge, "$g_talk_troop_faction_relation", 0)], "I must beg my leave.", "lord_leave",[]],

# [anyone,"lord_leave", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
      # (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
      # (lt, "$g_talk_troop_faction_relation", 0),
      # (store_partner_quest,":enemy_lord_quest"),
      # (lt, ":enemy_lord_quest", 0),
      # (troop_slot_eq, "$g_talk_troop", slot_troop_does_not_give_quest, 0),      
      # (call_script, "script_get_random_quest", "$g_talk_troop"),
      # (assign, "$random_quest_no", reg0),
      # (ge, "$random_quest_no", 0)],
# "Before you go, {playername}, I have something to ask of you... We may be enemies in this war,\
 # but I pray that you believe, as I do, that we can still be civil towards each other.\
 # Thus I hoped that you would be kind enough to assist me in something important to me.", "lord_leave_give_quest",[]],

# [anyone|plyr,"lord_leave_give_quest", [], "I am listening.", "enemy_lord_tell_mission",[]],

#[anyone,"enemy_lord_tell_mission", [(str_store_quest_name, s7, "$random_quest_no")], "ERROR: Enemy lord quest not handled: {s7}.", "close_window", []],

[anyone,"lord_leave_prison", [], "We'll meet again.", "close_window",[(call_script,"script_stand_back"),]],

[anyone|auto_proceed,"lord_leave", [(lt, "$g_talk_troop_faction_relation", 0)],
"We'll see about that, {playername}.", "close_window",[(call_script,"script_stand_back"),(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],

[anyone|auto_proceed,"lord_leave", [(faction_slot_eq,"$g_talk_troop_faction",slot_faction_leader,"$g_talk_troop")],
"Of course, {playername}. Farewell.", "close_window",[(call_script,"script_stand_back"),(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],

[anyone|auto_proceed,"lord_leave", [(ge,"$g_talk_troop_relation",10)],
"Good journeys to you, {playername}.", "close_window",[(call_script,"script_stand_back"),(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],

[anyone|auto_proceed,"lord_leave", [(ge, "$g_talk_troop_faction_relation", 0)],
"Yes, yes. Farewell.", "close_window",[(call_script,"script_stand_back"),(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],

[anyone|auto_proceed,"lord_leave", [],
"We will meet again.", "close_window",[(call_script,"script_stand_back"),(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],



[anyone,"start", [  (check_quest_active, "qst_escort_messenger"),
                    (eq, "$talk_context", tc_entering_center_quest_talk),
                    (quest_slot_eq, "qst_escort_messenger", slot_quest_object_troop, "$g_talk_troop")],
"Thank you for escorting me here, {playername}, and ensuring my safe passage. Your services will be duly noted. ", "lady_escort_lady_succeeded",
   [ #(quest_get_slot, ":cur_center", "qst_escort_messenger", slot_quest_target_center),
     #(add_xp_as_reward, 300),
     #(quest_get_slot, ":quest_giver", "qst_escort_messenger", slot_quest_giver_troop),
     #(store_troop_faction, ":quest_faction", ":quest_giver"),
     #(call_script, "script_troop_add_gold_faction", "trp_player", 250, ":quest_faction"),
     #(call_script, "script_increase_rank", ":quest_faction", 10),
     (call_script, "script_finish_quest", "qst_escort_messenger", 100),
     #(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
     #(troop_set_slot, "$g_talk_troop", slot_troop_cur_center, ":cur_center"),
     (remove_member_from_party,"$g_talk_troop")]],

[anyone|plyr,"lady_escort_lady_succeeded", [], "It was an honor to serve.", "close_window",[(call_script,"script_stand_back"),]],


# [anyone ,"start", [(troop_slot_eq,"$g_talk_troop",slot_troop_occupation, slto_kingdom_lady),
                     # (eq, "$g_talk_troop_met", 0),
                     # (le,"$talk_context",tc_siege_commander)],
# "I say, you don't look familiar...", "lady_premeet", []],

# [anyone|plyr ,"lady_premeet", [],  "I am {playername}.", "lady_meet", []],
# [anyone|plyr ,"lady_premeet", [],  "My name is {playername}. At your service.", "lady_meet", []],
# [anyone, "lady_meet", [],  "{playername}? I do not believe I've heard of you before.", "lady_meet_end", []],
# [anyone, "lady_meet_end", [],  "Can I help you with anything?", "lady_talk", []],

# [anyone,"start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
                  # (le,"$talk_context",tc_siege_commander)],
# "Yes?", "lady_talk",[]],

##### TODO: QUESTS COMMENT OUT BEGIN

# lady talk removed



# Prison Guards
[anyone,"start",[(eq, "$talk_context", 0),
				(agent_get_entry_no, ":entry", "$g_talk_agent"),
				(eq,":entry",24),
                (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                (party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player")], #player visited prison in brigand fort only?
"Good day, Commander. Will you be visiting the prison?", "prison_guard_players",[]],
[anyone|plyr,"prison_guard_players", [(neg|party_slot_eq, "$current_town", slot_town_prison, -1)],
"Yes. Unlock the door.", "close_window",[(call_script,"script_stand_back"),(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],
[anyone|plyr,"prison_guard_players", [], "No, not now.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"start", [(eq, "$talk_context", 0),(agent_get_entry_no, ":entry", "$g_talk_agent"),(eq,":entry",24)],
"Yes? What do you want?", "prison_guard_talk",[]],
[anyone|plyr,"prison_guard_talk", [], "Who is imprisoned here?", "prison_guard_ask_prisoners",[]],
[anyone|plyr,"prison_guard_talk", [(neg|party_slot_eq, "$current_town", slot_town_prison, -1)],
"I want to speak with a prisoner.", "prison_guard_visit_prison",[]], 

[anyone,"prison_guard_ask_prisoners", [],
"Currently, {s51} {reg1?are:is} imprisoned here.","prison_guard_talk",[(party_clear, "p_temp_party"),
                                                                              (assign, ":num_heroes", 0),
                                                                              (party_get_num_prisoner_stacks, ":num_stacks","$g_encountered_party"),
                                                                              (try_for_range, ":i_stack", 0, ":num_stacks"),
                                                                                (party_prisoner_stack_get_troop_id, ":stack_troop","$g_encountered_party",":i_stack"),
                                                                                (troop_is_hero, ":stack_troop"),
                                                                                (party_add_members, "p_temp_party", ":stack_troop", 1),
                                                                                (val_add, ":num_heroes", 1),
                                                                              (try_end),
                                                                              (call_script, "script_print_party_members", "p_temp_party"),
                                                                              (try_begin),
                                                                                (gt, ":num_heroes", 1),
                                                                                (assign, reg1, 1),
                                                                              (else_try),
                                                                                (assign, reg1, 0),
                                                                              (try_end)]],
  
[anyone,"prison_guard_visit_prison", [(this_or_next|faction_slot_eq, "$g_encountered_party_faction",slot_faction_marshall,"trp_player"),
                                        (this_or_next|party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
                                        (eq, "$g_encountered_party_faction", "$players_kingdom")],
"Of course, Commander. Go in.", "close_window",[(call_script,"script_stand_back"),(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],

[anyone,"prison_guard_visit_prison", [], "You need to get permission from the lord to talk to prisoners.", "prison_guard_visit_prison_2",[]],

[anyone|plyr,"prison_guard_visit_prison_2", [], "All right then. I'll try that.", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"prison_guard_visit_prison_2", [], "Come on now. I thought you were the boss here.", "prison_guard_visit_prison_3",[]],
[anyone,"prison_guard_visit_prison_3", [], "He-heh. You got that right. Still, I can't let you into the prison.", "prison_guard_visit_prison_4",[]],
  
[anyone|plyr,"prison_guard_visit_prison_4", [], "All right then. I'll leave now.", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"prison_guard_visit_prison_4", [(store_troop_gold,":gold","trp_player"),(ge,":gold",100)],
"I found a purse with 100 denars a few paces away. I reckon it belongs to you.", "prison_guard_visit_prison_5",[]],

[anyone,"prison_guard_visit_prison_5", [], "Ah! I was looking for this all day. How good of you to bring it back {sir/madam}.\
 Well, now that I know what an honest {man/lady} you are, there can be no harm in letting you inside. Go in.", "close_window",[
		(call_script,"script_stand_back"),
		(troop_remove_gold, "trp_player",100),
		(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],

[anyone|plyr,"prison_guard_talk", [], "Never mind.", "close_window",[(call_script,"script_stand_back"),]],




# Castle Guards
[anyone,"start",[(eq, "$talk_context", 0),
				(agent_get_entry_no, ":entry", "$g_talk_agent"),
				(eq,":entry",23),
                (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                (party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player")],
"Your orders, Commander?", "castle_guard_players",[]],

[anyone|plyr,"castle_guard_players", [(neg|party_slot_eq, "$current_town", slot_town_castle, -1)],
"Open the door. I'll go in.", "close_window",[(call_script,"script_stand_back"),(call_script, "script_enter_court", "$current_town")]],

[anyone|plyr,"castle_guard_players", [], "Never mind.", "close_window",[(call_script,"script_stand_back"),]],


[anyone,"start",[(eq, "$talk_context", 0),
				(agent_get_entry_no, ":entry", "$g_talk_agent"),
				(eq,":entry",23),
                (eq, "$sneaked_into_town",1),
                (gt,"$g_time_since_last_talk",0)],
"Get out of my sight, beggar! You stink!", "castle_guard_sneaked_intro_1",[]],
[anyone,"start",[(eq, "$talk_context", 0),
				(eq, "$sneaked_into_town",1),
				(agent_get_entry_no, ":entry", "$g_talk_agent"),
				(eq,":entry",23)],
"Get lost before I lose my temper you vile beggar!", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"castle_guard_sneaked_intro_1", [(neg|party_slot_eq, "$current_town", slot_town_castle, -1)], 
"I want to enter the hall and speak to the lord.", "castle_guard_sneaked_intro_2",[]],
[anyone|plyr,"castle_guard_sneaked_intro_1", [], "[Leave]", "close_window",[(call_script,"script_stand_back"),]],
[anyone,"castle_guard_sneaked_intro_2", [], "Are you out of your mind, {man/woman}?\
 Beggars are not allowed into the hall. Now get lost or I'll beat you bloody.", "close_window",[(call_script,"script_stand_back"),]],
  
  
[anyone,"start",[(eq, "$talk_context", 0),
				(agent_get_entry_no, ":entry", "$g_talk_agent"),
				(eq,":entry",23)],
"What do you want?", "castle_guard_intro_1",[]],

[anyone|plyr,"castle_guard_intro_1", [(neg|party_slot_eq, "$current_town", slot_town_castle, -1)],
"I want to enter the hall and speak to the lord.", "castle_guard_intro_2",[]],

[anyone|plyr,"castle_guard_intro_1", [], "Never mind.", "close_window",[(call_script,"script_stand_back"),]],
[anyone,"castle_guard_intro_2", [], "You can go in after leaving your weapons with me. No one is allowed to carry arms into the lord's hall.", "castle_guard_intro_2",[]],
[anyone|plyr,"castle_guard_intro_2", [], "Here, take my arms. I'll go in.", "close_window", [(call_script,"script_stand_back"),(call_script, "script_enter_court", "$current_town")]],
[anyone|plyr,"castle_guard_intro_2", [], "No, I give my arms to no one.", "castle_guard_intro_2b", []],
[anyone,"castle_guard_intro_2b", [], "Then you can't go in.", "close_window", [(call_script,"script_stand_back"),]],
  
##[anyone|plyr,"castle_guard_intro_1", [],
##   "Never mind.", "close_window",[]],
##[anyone,"castle_guard_intro_2", [],
##   "Does the lord expect you?", "castle_guard_intro_3",[]],
##[anyone|plyr,"castle_guard_intro_3", [], "Yes.", "castle_guard_intro_check",[]],
##[anyone|plyr,"castle_guard_intro_3", [], "No.", "castle_guard_intro_no",[]],
##[anyone,"castle_guard_intro_check", [], "Hmm. All right {sir/madam}.\
## You can go in. But you must leave your weapons with me. Noone's allowed into the court with weapons.", "close_window",[]],
##[anyone,"castle_guard_intro_check", [], "You liar!\
## Our lord would have no business with a filthy vagabond like you. Get lost now before I kick your butt.", "close_window",[]],
##[anyone,"castle_guard_intro_no", [], "Well... What business do you have here then?", "castle_guard_intro_4",[]],
##[anyone|plyr,"castle_guard_intro_4", [], "I wish to present the lord some gifts.", "castle_guard_intro_gifts",[]],
##[anyone|plyr,"castle_guard_intro_4", [], "I have an important matter to discuss with the lord. Make way now.", "castle_guard_intro_check",[]],
##[anyone,"castle_guard_intro_gifts", [], "Really? What gifts?", "castle_guard_intro_5",[]],
##[anyone|plyr,"castle_guard_intro_4", [], "Many gifts. For example, I have a gift of 20 denars here for his loyal servants.", "castle_guard_intro_gifts",[]],
##[anyone|plyr,"castle_guard_intro_4", [], "My gifts are of no concern to you. They are for your lords and ladies..", "castle_guard_intro_check",[]],
##[anyone,"castle_guard_intro_gifts", [], "Oh! you can give those 20 denars to me. I can distribute them for you.\
## You can enter the court and present your gifts to the lord. I'm sure he'll be pleased.\
## But you must leave your weapons with me. Noone's allowed into the court with weapons.", "close_window",[]],

#Kingdom Parties
#[anyone,"start", [(this_or_next|eq,"$g_encountered_party_template","pt_swadian_foragers"),
#                    (eq,"$g_encountered_party_template","pt_vaegir_foragers"),
##[anyone,"start", [(this_or_next|party_slot_eq,"$g_encountered_party",slot_party_type, spt_forager),
##                    (this_or_next|party_slot_eq,"$g_encountered_party",slot_party_type, spt_scout),
##                    (party_slot_eq,"$g_encountered_party",slot_party_type, spt_patrol),
##                    (str_store_faction_name,5,"$g_encountered_party_faction")],
##   "In the name of the {s5}.", "kingdom_party_encounter",[]],
##  
##[anyone,"kingdom_party_encounter", [(le,"$g_encountered_party_relation",-10)],
##   "Surrender now, and save yourself the indignity of defeat!", "kingdom_party_encounter_war",[]],
##[anyone|plyr,"kingdom_party_encounter_war", [],  "[Go to Battle]", "close_window",[(encounter_attack)]],
##
##[anyone,"kingdom_party_encounter", [(ge,"$g_encountered_party_relation",10)],
##   "Greetings, fellow warrior.", "close_window",[(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
##
##[anyone,"kingdom_party_encounter", [],
##   "You can go.", "close_window",[]],



#Player Parties
##  [party_tpl|pt_old_garrison,"start", [],
##   "They told us to leave the castle to the new garrison {sir/madam}. So we left and came to rejoin you.", "player_old_garrison_encounter",[]],
##  
##[anyone|plyr,"player_old_garrison_encounter", [(party_can_join)],
##   "You have done well. You'll join my command now.", "close_window",[(assign, "$g_move_heroes", 1),
##                                        (call_script, "script_party_add_party", "p_main_party", "$g_encountered_party"),
##                                        (remove_party, "$g_encountered_party"),
##                                        (assign, "$g_leave_encounter", 1)]],
##[anyone|plyr,"player_old_garrison_encounter", [(assign, reg1, 0),
##                                                 (try_begin),
##                                                   (neg|party_can_join),
##                                                   (assign, reg1, 1),
##                                                 (try_end)],
##   "You can't join us now{reg1?, I can't command all the lot of you:}. Follow our lead.", "close_window",[(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_attack_party),
##                                                                         (party_set_ai_object, "$g_encountered_party", "p_main_party"),
##                                                                         (party_set_flags, "$g_encountered_party", pf_default_behavior, 0),
##                                                                         (assign, "$g_leave_encounter", 1)]],
##
##[anyone|plyr,"player_old_garrison_encounter", [(assign, reg1, 0),
##                                                 (try_begin),
##                                                   (neg|party_can_join),
##                                                   (assign, reg1, 1),
##                                                 (try_end)],
##   "You can't join us now{reg1?, I can't command all the lot of you:}. Stay here and wait for me.", "close_window",[
##       (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_travel_to_point),
##       (party_get_position, pos1, "$g_encountered_party"),
##       (party_set_ai_target_position, "$g_encountered_party", pos1),
##       (party_set_flags, "$g_encountered_party", pf_default_behavior, 0),
##       (assign, "$g_leave_encounter", 1)]],
##






[anyone,"start", [(eq, "$talk_context", tc_castle_gate)], "What do you want?", "castle_gate_guard_talk",[]],
[anyone,"castle_gate_guard_pretalk", [], "Yes?", "castle_gate_guard_talk",[]],
[anyone|plyr,"castle_gate_guard_talk", [(ge, "$g_encountered_party_relation", 0)], "We need shelter for the night. Will you let us in?", "castle_gate_open",[]],
[anyone|plyr,"castle_gate_guard_talk", [(party_slot_ge, "$g_encountered_party", slot_town_lord, 1)], "I want to speak with the lord of the castle.", "request_meeting_castle_lord",[]],
[anyone|plyr,"castle_gate_guard_talk", [], "I want to speak with someone in the castle.", "request_meeting_other",[]],
[anyone|plyr,"castle_gate_guard_talk", [], "[Leave]", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"request_meeting_castle_lord", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
                                         (eq, "$g_encountered_party", reg0),
                                         (str_store_troop_name, s2, ":castle_lord"),
                                         (assign, "$lord_requested_to_talk_to", ":castle_lord"),],
"Wait here. {s2} will see you.", "close_window",[(call_script,"script_stand_back"),]],
  
[anyone,"request_meeting_castle_lord", [],  "My lord is not here now.", "castle_gate_guard_pretalk",[]],
[anyone,"request_meeting_other", [],  "Who is that?", "request_meeting_3",[]],

[anyone|plyr|repeat_for_troops,"request_meeting_3", [(store_repeat_object, ":troop_no"),
                                                       (troop_is_hero, ":troop_no"),
                                                       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                                                       (call_script, "script_get_troop_attached_party", ":troop_no"),
                                                       (eq, "$g_encountered_party", reg0),
                                                       (str_store_troop_name, s3, ":troop_no"),
                                                       ],
"{s3}", "request_meeting_4",[(store_repeat_object, "$lord_requested_to_talk_to")]],

[anyone|plyr,"request_meeting_3", [], "Never mind.", "close_window",[(call_script,"script_stand_back"),(assign, "$lord_requested_to_talk_to", 0)]],
[anyone,"request_meeting_4", [], "Wait there. I'll send him your request.", "request_meeting_5",[]],
[anyone|plyr,"request_meeting_5", [], "I'm waiting...", "request_meeting_6",[]],

[anyone,"request_meeting_6",[
     (call_script, "script_troop_get_player_relation", "$lord_requested_to_talk_to"),
     (assign, ":lord_relation", reg0),
     (gt, ":lord_relation", -20)], 
"All right. {s2} will talk to you now.", "close_window",[(call_script,"script_stand_back"),(str_store_troop_name, s2, "$lord_requested_to_talk_to")]],

[anyone,"request_meeting_6", [(str_store_troop_name, s2, "$lord_requested_to_talk_to")], "{s2} says he will not see you. Begone now.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
							 (call_script, "script_get_troop_attached_party", ":castle_lord"),
							 (eq, "$g_encountered_party", reg0),
							 (ge, "$g_encountered_party_relation", 0),
							 (call_script, "script_troop_get_player_relation", ":castle_lord"),
							 (assign, ":castle_lord_relation", reg0),
							 #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
							 (ge, ":castle_lord_relation", 5),
							 (str_store_troop_name, s2, ":castle_lord")],
"My lord {s2} will be happy to see you {sir/madam}.\
 Come on in. I am opening the gates for you.", "close_window",[(call_script,"script_stand_back"),(assign,"$g_permitted_to_center",1)]],


[anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
							 (call_script, "script_get_troop_attached_party", ":castle_lord"),
							 (neq, "$g_encountered_party", reg0),
							 (ge, "$g_encountered_party_relation", 0),
							 (call_script, "script_troop_get_player_relation", ":castle_lord"),
							 (assign, ":castle_lord_relation", reg0),
							 #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
							 (ge, ":castle_lord_relation", 5),
							 (str_store_troop_name, s2, ":castle_lord")],
"My lord {s2} is not in the castle now.\
 But I think he would approve of you taking shelter here.\
 Come on in. I am opening the gates for you.", "close_window",[(call_script,"script_stand_back"),(assign,"$g_permitted_to_center",1)]],
 
[anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                               (call_script, "script_troop_get_player_relation", ":castle_lord"),
                               (assign, ":castle_lord_relation", reg0),
                               #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                               (ge, ":castle_lord_relation", -2)],
"Come on in. I am opening the gates for you.", "close_window",[(call_script,"script_stand_back"),(assign,"$g_permitted_to_center",1)]],
                                         
[anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                               (call_script, "script_troop_get_player_relation", ":castle_lord"),
                               (assign, ":castle_lord_relation", reg0),
                               #(troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
                               (ge, ":castle_lord_relation", -19),
                               (str_store_troop_name, s2, ":castle_lord")],
"Come on in. But make sure your men behave sensibly within the walls. \
 My lord {s2} does not want trouble here.", "close_window", [(call_script,"script_stand_back"),(assign,"$g_permitted_to_center",1)]],
 
[anyone,"castle_gate_open", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
                               (str_store_troop_name, s2, ":castle_lord")],
"My lord {s2} does not want you here. Begone now.", "close_window",[(call_script,"script_stand_back"),]],


#Enemy Kingdom Meetings


#[anyone,"start", [(eq, "$talk_context", tc_lord_talk_in_center)],
#   "Greetings {playername}.", "request_meeting_1",[]],

#[anyone,"request_meeting_pretalk", [(eq, "$talk_context", tc_lord_talk_in_center)],
#   "Yes?", "request_meeting_1",[]],
  
#[anyone|plyr,"request_meeting_1", [(ge, "$g_encountered_party_faction", 0)], "Open the gates and let me in!", "request_meeting_open_gates",[]],
  
#[anyone|plyr,"request_meeting_1", [(party_slot_ge, "$g_encountered_party", slot_town_lord, 1)], "I want to speak with the lord of the castle.", "request_meeting_castle_lord",[]],
#[anyone|plyr,"request_meeting_1", [], "I want to speak with someone in the castle.", "request_meeting_other",[]],

##### TODO: QUESTS COMMENT OUT BEGIN
##[anyone|plyr,"request_meeting_1",[(check_quest_active,"qst_bring_prisoners_to_enemy"),
##                                    (neg|check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##                                    (quest_get_slot, ":quest_giver_troop", "qst_bring_prisoners_to_enemy", slot_quest_giver_troop),
##                                    (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##                                    (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_target_center, "$g_encountered_party"),
##                                    (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_object_troop"),
##                                    (ge, ":num_prisoners", ":quest_target_amount"),
##                                    (str_store_troop_name,1,":quest_giver_troop"),
##                                    (assign, reg1, ":quest_target_amount"),
##                                    (str_store_troop_name_plural,2,":quest_object_troop")],
##   "TODO: Sir, lord {s1} ordered me to bring {reg1} {s2} for ransom.", "guard_prisoners_brought",
##   [(quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##    (quest_get_slot, ":quest_target_center", "qst_bring_prisoners_to_enemy", slot_quest_target_center),
##    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##    (party_remove_prisoners, "p_main_party", ":quest_object_troop", ":quest_target_amount"),
##    (party_add_members, ":quest_target_center", ":quest_object_troop", ":quest_target_amount"),
##    (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##    (assign, ":reward", reg0),
##    (val_mul, ":reward", ":quest_target_amount"),
##    (val_div, ":reward", 2),
##    (call_script, "script_troop_add_gold", "trp_player",":reward"),
##    (party_get_slot, ":cur_lord", "$g_encountered_party", slot_town_lord),#Removing gold from the town owner's wealth
##    (troop_get_slot, ":cur_wealth", ":cur_lord", slot_troop_wealth),
##    (val_sub, ":cur_wealth", ":reward"),
##    (troop_set_slot, ":cur_lord", slot_troop_wealth, ":cur_wealth"),
##    (quest_set_slot, "qst_bring_prisoners_to_enemy", slot_quest_target_amount, ":reward"),
##    (succeed_quest, "qst_bring_prisoners_to_enemy"),
##    ]],
##
##[anyone|plyr,"request_meeting_1",[(check_quest_active,"qst_bring_prisoners_to_enemy"),
##                                    (neg|check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##                                    (quest_get_slot, ":quest_giver_troop", "qst_bring_prisoners_to_enemy", slot_quest_giver_troop),
##                                    (quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##                                    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##                                    (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_target_center, "$g_encountered_party"),
##                                    (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_object_troop"),
##                                    (lt, ":num_prisoners", ":quest_target_amount"),
##                                    (gt, ":num_prisoners", 0),
##                                    (str_store_troop_name,1,":quest_giver_troop"),
##                                    (assign, reg1, ":quest_target_amount"),
##                                    (str_store_troop_name_plural,2,":quest_object_troop")],
##   "TODO: Sir, lord {s1} ordered me to bring {reg1} {s2} for ransom, but some of them died during my expedition.", "guard_prisoners_brought_some",
##   [(quest_get_slot, ":quest_target_amount", "qst_bring_prisoners_to_enemy", slot_quest_target_amount),
##    (quest_get_slot, ":quest_target_center", "qst_bring_prisoners_to_enemy", slot_quest_target_center),
##    (quest_get_slot, ":quest_object_troop", "qst_bring_prisoners_to_enemy", slot_quest_object_troop),
##    (party_count_prisoners_of_type, ":num_prisoners", "p_main_party", ":quest_object_troop"),
##    (party_remove_prisoners, "p_main_party", ":quest_object_troop", ":num_prisoners"),
##    (party_add_members, ":quest_target_center", ":quest_object_troop", ":num_prisoners"),
##    (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##    (assign, ":reward", reg0),
##    (val_mul, ":reward", ":num_prisoners"),
##    (val_div, ":reward", 2),
##    (call_script, "script_troop_add_gold", "trp_player",":reward"),
##    (party_get_slot, ":cur_lord", "$g_encountered_party", slot_town_lord),#Removing gold from the town owner's wealth
##    (troop_get_slot, ":cur_wealth", ":cur_lord", slot_troop_wealth),
##    (val_sub, ":cur_wealth", ":reward"),
##    (troop_set_slot, ":cur_lord", slot_troop_wealth, ":cur_wealth"),
##    (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##    (assign, ":reward", reg0),
##    (val_mul, ":reward", ":quest_target_amount"),
##    (val_div, ":reward", 2),
##    (quest_set_slot, "qst_bring_prisoners_to_enemy", slot_quest_current_state, 1),#Some of the prisoners are given, so it's state will change for remembering that.
##    (quest_set_slot, "qst_bring_prisoners_to_enemy", slot_quest_target_amount, ":reward"),#Still needs to pay the lord the full price of the prisoners
##    (succeed_quest, "qst_bring_prisoners_to_enemy"),
##    ]],
##
##
##[anyone,"guard_prisoners_brought", [],
##   "TODO: Thank you. Here is the money for prisoners.", "request_meeting_pretalk",[]],
##
##[anyone,"guard_prisoners_brought_some", [],
##   "TODO: Thank you, but that's not enough. Here is the money for prisoners.", "request_meeting_pretalk",[]],

#[anyone|plyr,"request_meeting_1", [], "[Leave]", "close_window",[]],




  
##[anyone,"request_meeting_open_gates", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
##                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
##                                         (eq, "$g_encountered_party", reg0),
##                                         (str_store_troop_name, 1, ":castle_lord")
##                                         ],  "My lord {s1} is in the castle now. You must ask his permission to enter.", "request_meeting_pretalk",[]],
##
##[anyone,"request_meeting_open_gates", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),
##                                         (call_script, "script_get_troop_attached_party", ":castle_lord"),
##                                         (neq, "$g_encountered_party", reg0),
##                                         (ge, "$g_encountered_party_relation", 0),
##                                         (troop_get_slot, ":castle_lord_relation", ":castle_lord", slot_troop_player_relation),
##                                         (ge, ":castle_lord_relation", 20),
##                                         (str_store_troop_name, 1, ":castle_lord")
##                                         ],  "My lord {s1} is not in the castle now.\
## But I think he would approve of you taking shelter here, {sir/madam}.\
## Come on in. I am opening the gates for you.", "close_window",[]],
##  
##[anyone,"request_meeting_open_gates", [(party_get_slot, ":castle_lord", "$g_encountered_party", slot_town_lord),(str_store_troop_name, 1, ":castle_lord")],
##   "My lord {s1} is not in the castle now. I can't allow you into the castle without his orders.", "request_meeting_pretalk",[]],
  

  

# Quest conversations

##### TODO: QUESTS COMMENT OUT BEGIN
  
##  [party_tpl|pt_peasant_rebels,"start", [],
##   "TODO: What.", "peasant_rebel_talk",[]],
##[anyone|plyr, "peasant_rebel_talk", [], "TODO: Die.", "close_window",[]],
##[anyone|plyr, "peasant_rebel_talk", [], "TODO: Nothing.", "close_window",[(assign, "$g_leave_encounter",1)]],
##
##  [party_tpl|pt_noble_refugees,"start", [],
##   "TODO: What.", "noble_refugee_talk",[]],
##[anyone|plyr, "noble_refugee_talk", [], "TODO: Nothing.", "close_window",[(assign, "$g_leave_encounter",1)]],
##

### TLD dialogs: starting quest caravan master talk
[trp_start_quest_caravaneer,"party_relieved", [(eq,"$talk_context",tc_starting_quest)], 
"Thank you for helping! We are safe now.", "caravan_help0",[]], 
[trp_start_quest_caravaneer,"caravan_help0", [], "Thank you for helping! We are safe now. \
Have you seen those large orcs before? Those do not look like regular mountain ilk we are used to fend off easily. \
And the paint on their shields is an ancient Mordor sign. I haven't seen those this side of the river for a long time. \
Dire things are afoot.. War is coming! I advise you to go to Edoras, the capital of your people, \
and deliver the message about what you've seen to whomever is in command there. \
It's an important matter, so please make haste.", "caravan_help1",[
       (setup_quest_text, "qst_tld_introduction"),
       (str_store_string, s2, "str_tld_introduction"),
       (add_quest_note_from_sreg, "qst_tld_introduction", 0, s2, 0),
       (start_quest, "qst_tld_introduction")]],
[trp_start_quest_caravaneer|plyr,"caravan_help1", [], "Yeah, I never seen such a large orc before. Nasty things.", "caravan_help2",[]],
[trp_start_quest_caravaneer,"caravan_help2", [], "Also, I see you are a capable warrior. I have a personal business I would like your help with. There is a small fort near Nindalf swamps, where common people and travellers can find food and lodge. It's run by a local chief who does not answer neither to Gondor, nor to Rohan. I'm a merchant traveller myself, so I have respect for people wishing to be free from lordship bonds, as long as they behave. But being independent, they are also powerless before enemy onslaught. War outbreak in next several days looks like a certain thing to me. I want you to get to those people and see if you can help them survive. Tell the chief, Balan, that Torbal asked you to deliver 'a fishslap'. He will recognize it was me who sent you.", "caravan_help3",[]],
[trp_start_quest_caravaneer|plyr,"caravan_help3", [], "I'll deliver your message. Safe journey to you, Torbal. I'm sure we will meet again.", "close_window",[(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)]],
# end starting quest caravan master talk

[anyone,"start", [(eq,"$talk_context",tc_join_battle_ally)],"You have come just in time. Let us join our forces now and teach our enemy a lesson.", "close_window", [(call_script,"script_stand_back"),]],
[anyone,"start", [(eq,"$talk_context",tc_join_battle_enemy)],"You are making a big mistake by fighting against us.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 17)],
"I don't think we have met properly my friend. You just saved my life out there, and I still don't know your name...", "ally_thanks_meet", []],


[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 5),
		    (str_store_troop_name, s1, "$g_talk_troop")],
"Your help was most welcome stranger. My name is {s1}. Can I learn yours?", "ally_thanks_meet", []],

[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 0),
                    (str_store_troop_name, s1, "$g_talk_troop")],
"Thanks for your help, stranger. We haven't met properly yet, have we? What is your name?", "ally_thanks_meet", []],

[anyone|plyr,"ally_thanks_meet", [], "My name is {playername}.", "ally_thanks_meet_2", []],

[anyone, "ally_thanks_meet_2", [(ge, "$g_talk_troop_relation", 15),(str_store_troop_name, s1, "$g_talk_troop")],
"Well met indeed {playername}. My name is {s1} and I am forever in your debt. If there is ever anything I can help you with, just let me know...", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "ally_thanks_meet_2", [(ge, "$g_talk_troop_relation", 5),], "Well met {playername}. I am in your debt for what you just did. I hope one day I will find a way to repay it.", "close_window", [(call_script,"script_stand_back"),]],
[anyone, "ally_thanks_meet_2", [], "Well met {playername}. I am {s1}. Thanks for your help and I hope we meet again.", "close_window", [(call_script,"script_stand_back"),]],

#Post 0907 changes begin
[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", 30),
                    (ge, "$g_relation_boost", 10)],
"Again you save our necks, {playername}! Truly, you are the best of friends. {s43}", "close_window", [
		(call_script,"script_stand_back"),
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
       (try_begin),
         (party_stack_get_troop_id, ":enemy_party_leader", "p_encountered_party_backup", 0),
         (is_between, ":enemy_party_leader", kingdom_heroes_begin, kingdom_heroes_end),
         (call_script, "script_add_log_entry", logent_lord_helped_by_player, "trp_player",  -1, ":enemy_party_leader", -1),
       (try_end)]],
  
[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", 20),
                    (ge, "$g_relation_boost", 5)],
"You arrived just in the nick of time! {playername}. You have my deepest thanks! {s43}", "close_window", [
       (call_script,"script_stand_back"),
	   (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
       (try_begin),
         (party_stack_get_troop_id, ":enemy_party_leader", "p_encountered_party_backup", 0),
         (is_between, ":enemy_party_leader", kingdom_heroes_begin, kingdom_heroes_end),
         (call_script, "script_add_log_entry", logent_lord_helped_by_player, "trp_player",  -1, ":enemy_party_leader", -1),
       (try_end)]],
  
[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", 0),
                    (ge, "$g_relation_boost", 3)],
"You turned up just in time, {playername}. I will not forget your help. {s43}", "close_window", [
       (call_script,"script_stand_back"),
	   (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
       (try_begin),
         (party_stack_get_troop_id, ":enemy_party_leader", "p_encountered_party_backup", 0),
         (is_between, ":enemy_party_leader", kingdom_heroes_begin, kingdom_heroes_end),
         (call_script, "script_add_log_entry", logent_lord_helped_by_player, "trp_player",  -1, ":enemy_party_leader", -1),
       (try_end)]],

[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", -5),],
"Good to see you here, {playername}. {s43}", "close_window", [
                    (call_script,"script_stand_back"),
					(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default")]],

[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_relation_boost", 4)],
"{s43}", "close_window", [
				(call_script,"script_stand_back"),
				(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_grudging_default")]],

[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop")],
"{s43}", "close_window", [
				(call_script,"script_stand_back"),
				(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_unfriendly_default")]],


#[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
#                    (troop_is_hero, "$g_talk_troop"),
#                    (ge, "$g_talk_troop_relation", -20),
#                    ],
#   "So, this is {playername}. Well, your help wasn't really needed, but I guess you had nothing better to do, right?", "close_window", []],

#[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
#                    (troop_is_hero, "$g_talk_troop"),
#                    ],
#   "Who told you to come to our help? I certainly didn't. Begone now. I want nothing from you and I will not let you steal my victory.", "close_window", []],

#Post 0907 changes begin

[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                    (ge, "$g_relation_boost", 10),
                    (party_get_num_companions, reg1, "$g_encountered_party"),
                    (val_sub, reg1, 1)],
"Thank you for your help, Commander. You saved {reg1?our lives:my life} out there.", "close_window", [(call_script,"script_stand_back"),]],

[anyone,"start", [(eq,"$talk_context",tc_ally_thanks),
                  (ge, "$g_relation_boost", 5)],
"Thank you for your help, Commander. Things didn't look very well for us but then you came up and everything changed.", "close_window", [(call_script,"script_stand_back"),]],

[anyone,"start", [(eq,"$talk_context",tc_ally_thanks)],
"Thank you for your help, Commander. It was fortunate to have you nearby.", "close_window", [(call_script,"script_stand_back"),]],
  
  #[anyone,"start", [(eq, "$talk_context", tc_hero_freed),
                    # (store_conversation_troop,":cur_troop"),
                    # (eq,":cur_troop","trp_kidnapped_girl"),],
   # "Oh {sir/madam}. Thank you so much for rescuing me. Will you take me to my family now?", "kidnapped_girl_liberated_battle",[]],

[anyone,"start", [(eq,"$talk_context",tc_hero_freed)], "I am in your debt for freeing me friend.", "freed_hero_answer", []],

[anyone|plyr,"freed_hero_answer", [],
"You're not going anywhere. You'll be my prisoner now!", "freed_hero_answer_1",[
     (store_conversation_troop, ":cur_troop_id"), 
     (party_add_prisoners, "p_main_party", ":cur_troop_id", 1)]],

[anyone,"freed_hero_answer_1", [], "Alas. Will my luck never change?", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"freed_hero_answer", [], "You're free to go, {s65}.", "freed_hero_answer_2",[]],
[anyone,"freed_hero_answer_2", [],"Thank you, Commander. I never forget someone who's done me a good turn.", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"freed_hero_answer", [],"Would you like to join me?", "freed_hero_answer_3",[]],

[anyone,"freed_hero_answer_3", [(store_random_in_range, ":random_no",0,2),(eq, ":random_no", 0)],
"All right I will join you.", "close_window",[
	 (call_script,"script_stand_back"),
     (store_conversation_troop, ":cur_troop_id"), 
     (party_add_members, "p_main_party", ":cur_troop_id", 1)]],

[anyone,"freed_hero_answer_3", [], "No, I want to go on my own.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"start", [(eq,"$talk_context",tc_hero_defeated)],
   "You'll not live long to enjoy your victory. My kinsmen will soon wipe out the stain of this defeat.", "defeat_hero_answer",[]],

[anyone|plyr,"defeat_hero_answer", [],
"You are my prisoner now.", "defeat_hero_answer_1",[
     (party_add_prisoners, "p_main_party", "$g_talk_troop", 1),#take prisoner
     (troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),]],

[anyone,"defeat_hero_answer_1", [], "Damn you. You will regret this.", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"defeat_hero_answer", [], "You're free to go this time, but don't cross my path again.", "defeat_hero_answer_2",[]],
[anyone,"defeat_hero_answer_2", [], "We will meet again.", "close_window", [(call_script,"script_stand_back"),]],



# Local merchant

  # [trp_local_merchant,"start", [], "Mercy! Please don't kill me!", "local_merchant_mercy",[]],
  #[anyone|plyr,"local_merchant_mercy", [(quest_get_slot, ":quest_giver_troop", "qst_kill_local_merchant", slot_quest_giver_troop),(str_store_troop_name, s2, ":quest_giver_troop")],
   # "I have nothing against you man. But {s2} wants you dead. Sorry.", "local_merchant_mercy_no",[]],
  #[anyone,"local_merchant_mercy_no", [], "Damn you! May you burn in Hell!", "close_window",[]],
  #[anyone|plyr,"local_merchant_mercy", [], "I'll let you live, if you promise me...", "local_merchant_mercy_yes",[]],

  #[anyone,"local_merchant_mercy_yes", [], "Of course, I promise, I'll do anything. Just spare my life... ", "local_merchant_mercy_yes_2",[]],
  #[anyone|plyr,"local_merchant_mercy_yes_2", [], "You are going to forget about {s2}'s debt to you.\
 # And you will sign a paper stating that he owes you nothing.", "local_merchant_mercy_yes_3",[]],
  #[anyone,"local_merchant_mercy_yes_3", [], "Yes, of course. I'll do as you say.", "local_merchant_mercy_yes_4",[]],
  #[anyone|plyr,"local_merchant_mercy_yes_4", [], "And if my lord hears so much of a hint of a complaint about this issue, then I'll come back for you,\
 # and it won't matter how much you scream for mercy then.\
 # Do you understand me?", "local_merchant_mercy_yes_5",[]],
  #[anyone,"local_merchant_mercy_yes_5", [], "Yes {sir/madam}. Don't worry. I won't make any complaint.", "local_merchant_mercy_yes_6",[]],
  #[anyone|plyr,"local_merchant_mercy_yes_6", [], "Good. Go now, before I change my mind.", "close_window",
   # [(quest_set_slot, "qst_kill_local_merchant", slot_quest_current_state, 2),
    # (call_script, "script_succeed_quest", "qst_kill_local_merchant"),
    # (finish_mission),
    # ]],

# Village traitor

[anyone,"start",[(check_quest_active, "qst_hunt_down_fugitive"),
				(quest_get_slot, ":quest_object_troop", "qst_hunt_down_fugitive", slot_quest_object_troop),
				(eq, "$g_talk_troop", ":quest_object_troop")], 
"Yes, what do you want?", "fugitive_1",[]],

[anyone|plyr,"fugitive_1", [
     (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
     (quest_get_slot, ":quest_object_troop", "qst_hunt_down_fugitive", slot_quest_object_troop),
     (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna", ":quest_object_troop"),
     (str_store_string, s4, s50)], 
"I am looking for a fugitive by the name of {s4}. You fit his description.", "fugitive_2",[]],

[anyone|plyr,"fugitive_1", [], "Nothing. Sorry to trouble you.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"fugitive_2", [], "I do not know what you are talking about.\
 You must have confused me with someone else.", "fugitive_3",[]],

[anyone|plyr,"fugitive_3", [], "Then drop your sword. If you are innocent, you have nothing to fear.\
 We'll go now and talk to the guard captain to see who is confused.", "fugitive_4",[]],

[anyone,"fugitive_4", [], "Damn you! You will not be going anywhere!", "close_window",
   [(call_script,"script_stand_back"),
    (set_party_battle_mode),
    (get_player_agent_no, ":player_agent"),
    (try_for_agents, ":cur_agent"),
      (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
      (try_begin),
        (eq, ":cur_agent_troop", "$g_talk_troop"),
        (agent_set_team, ":cur_agent", 3),
      (else_try),
        (eq, ":cur_agent", ":player_agent"),
        (agent_set_team, ":cur_agent", 2),
      (try_end),
    (try_end),
    (team_set_relation, 2, 3, -1),
    (team_set_relation, 2, 0, 0),
    (team_set_relation, 3, 0, 0),
    (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 1)]],


  #[anyone,"member_chat", [(check_quest_active, "qst_incriminate_loyal_commander"),
                          # (quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_current_state, 0),
                          # (store_conversation_troop, "$g_talk_troop"),
                          # (eq, "$g_talk_troop", "$incriminate_quest_sacrificed_troop"),
                          # (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                          # (store_distance_to_party_from_party, ":distance", "p_main_party", ":quest_target_center"),
                          # (lt, ":distance", 10),
                          # ], "Yes {sir/madam}?", "sacrificed_messenger_1",[]],

  #[anyone|plyr,"sacrificed_messenger_1", [(quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                          # (str_store_party_name, s1, ":quest_target_center"),
                                          # (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
                                          # (str_store_troop_name, s2, ":quest_object_troop"),],
   # "Take this letter to {s1} and give it to {s2}.", "sacrificed_messenger_2",[]],
  #[anyone|plyr,"sacrificed_messenger_1", [],
   # "Nothing. Nothing at all.", "close_window",[]],

  #[anyone,"sacrificed_messenger_2", [],
   # "Yes {sir/madam}. You can trust me. I will not fail you.", "sacrificed_messenger_3",[]],

  #[anyone|plyr,"sacrificed_messenger_3", [],
   # "Good. I will not forget your service. You will be rewarded when you return.", "close_window",[(party_remove_members, "p_main_party", "$g_talk_troop", 1),
                                     # (set_spawn_radius, 0),
                                     # (spawn_around_party, "p_main_party", "pt_sacrificed_messenger"),
                                     # (assign, ":new_party", reg0),
                                     # (party_add_members, ":new_party", "$g_talk_troop", 1),
                                     # (party_set_ai_behavior, ":new_party", ai_bhvr_travel_to_party),
                                     # (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                     # (party_set_ai_object, ":new_party", ":quest_target_center"),
                                     # (party_set_flags, ":new_party", pf_default_behavior, 0),
                                     # (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 2),
                                     # (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_target_party, ":new_party")]],
  #[anyone|plyr,"sacrificed_messenger_3", [], "Arggh! I can't do this. I can't send you to your own death!", "sacrificed_messenger_cancel",[]],
  #[anyone,"sacrificed_messenger_cancel", [], "What do you mean {sir/madam}", "sacrificed_messenger_cancel_2",[]],
  #[anyone|plyr,"sacrificed_messenger_cancel_2", [(quest_get_slot, ":quest_giver", "qst_incriminate_loyal_commander", slot_quest_giver_troop),
                                                 # (str_store_troop_name, s3, ":quest_giver"),
      # ], "There's a trap set up for you in the town.\
 # {s3} ordered me to sacrifice one of my chosen warriors to fool the enemy,\
 # but he will just need to find another way.", "sacrificed_messenger_cancel_3",[
     # (quest_get_slot, ":quest_giver", "qst_incriminate_loyal_commander", slot_quest_giver_troop),
     # (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 1),
     # (call_script, "script_change_player_relation_with_troop",":quest_giver",-5),
     # (call_script, "script_change_player_honor", 3),
     # (call_script, "script_fail_quest", "qst_incriminate_loyal_commander"),
     # ]],
  #[anyone,"sacrificed_messenger_cancel_3", [], "Thank you, {sir/madam}.\
 # I will follow you to the gates of hell. But this would not be a good death.", "close_window",[]],

  # [party_tpl|pt_sacrificed_messenger,"start", [],
   # "Don't worry, {sir/madam}, I'm on my way.", "close_window",[(assign, "$g_leave_encounter",1)]],

#Spy

[anyone,"start",   [(check_quest_active, "qst_follow_spy"),
					(quest_get_slot, ":spy_troop", "qst_follow_spy", slot_quest_object_troop),
					(eq, "$g_talk_troop", ":spy_troop")], 
"Good day. Such fine weather don't you think? If you'll excuse me now I must go on my way.", "follow_spy_talk",[]],

[anyone|plyr,"follow_spy_talk",[(quest_get_slot, ":quest_giver", "qst_follow_spy", slot_quest_giver_troop),
								(str_store_troop_name, s1, ":quest_giver"),],
"In the name of {s1}, you are under arrest!", "follow_spy_talk_2", []],

[anyone, "follow_spy_talk_2", [], "You won't get me alive!", "close_window", [(call_script,"script_stand_back"),]],
[anyone|plyr, "follow_spy_talk", [], "Never mind me. I was just passing by.", "close_window", [
	(call_script,"script_stand_back"),
	(assign, "$g_leave_encounter",1)]],

[anyone,"start", [ (check_quest_active, "qst_follow_spy"),
    (quest_get_slot, ":spy_partner", "qst_follow_spy", slot_quest_target_troop),
    (eq, "$g_talk_troop", ":spy_partner")],
"Greetings.", "spy_partners_talk",[]],

[anyone|plyr,"spy_partners_talk",[(quest_get_slot, ":quest_giver", "qst_follow_spy", slot_quest_giver_troop),
								(str_store_troop_name, s1, ":quest_giver"),],
"In the name of {s1} You are under arrest!", "spy_partners_talk_2",[]],

[anyone,"spy_partners_talk_2", [], "You will have to fight us first!", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"spy_partners_talk", [], "Never mind me. I was just passing by.", "close_window",[
	(call_script,"script_stand_back"),
	(assign, "$g_leave_encounter",1)]],


###Conspirator
##
##  [party_tpl|pt_conspirator_leader,"start", [], "TODO: Hello.", "conspirator_talk",[]],
##  [party_tpl|pt_conspirator,"start", [], "TODO: Hello.", "conspirator_talk",[]],
##
##[anyone|plyr,"conspirator_talk", [(gt, "$qst_capture_conspirators_leave_meeting_counter", 0),
##                                    (quest_get_slot,":quest_giver","qst_capture_conspirators",slot_quest_giver_troop),
##                                    (str_store_troop_name,s1,":quest_giver")],
##   "TODO: In the name of {s1}, you are under arrest!", "conspirator_talk_2",[]],
##
##[anyone|plyr,"conspirator_talk", [], "TODO: Bye.", "close_window",[(assign, "$g_leave_encounter",1)]],
##
##[anyone,"conspirator_talk_2", [], "You won't get me alive!", "close_window",[]],
##
#Runaway Peasants


[party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_center, 0)],#slot_town_center is used for first time meeting
"Good day master.", "runaway_serf_intro_1", [(party_set_slot, "$g_encountered_party", slot_town_center, 1)]],
  
[anyone|plyr,"runaway_serf_intro_1", [(quest_get_slot, ":lord", "qst_bring_back_runaway_serfs", slot_quest_giver_troop),
                                        (str_store_troop_name, s4, ":lord")],
"I have been sent by your {s4} whom you are running from. He will not punish you if you return now.", "runaway_serf_intro_2",[]],
   
[anyone,"runaway_serf_intro_2", [(quest_get_slot, ":target_center", "qst_bring_back_runaway_serfs", slot_quest_target_center),
                                   (str_store_party_name, s6, ":target_center"),
                                   (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                   (str_store_party_name, s1, ":quest_object_center")],
"My good master. Our lives at {s1} was unbearable. We worked all day long and still went to bed hungry.\
 We are going to {s6} to start a new life, where we will be treated like humans.", "runaway_serf_intro_3",[]],

[anyone|plyr,"runaway_serf_intro_3", [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                        (str_store_party_name, s1, ":quest_object_center"),],
"You have gone against our laws by running from slavery. You will go back to {s1} now!", "runaway_serf_go_back",
   [#(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    #(call_script, "script_change_player_relation_with_center", ":quest_object_center", -1)
    ]],

  #[anyone|plyr,"runaway_serf_intro_3", [], "Well, maybe you are right. All right then. If anyone asks, I haven't seen you.", "runaway_serf_let_go",
   # [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    # (call_script, "script_change_player_relation_with_center", ":quest_object_center", 1)
    # ]],

[party_tpl|pt_runaway_serfs,"runaway_serf_go_back", [(quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                                       (str_store_party_name, s5, ":home_center")],
"All right master. As you wish. We'll head back to {s5} now.", "close_window",
   [(call_script,"script_stand_back"),
    (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (party_set_ai_object, "$g_encountered_party", ":quest_object_center"),
    (assign, "$g_leave_encounter",1)]],
  
  #[anyone,"runaway_serf_let_go", [], "God bless you, {sir/madam}. We will not forget your help.", "close_window",
   # [(party_set_slot, "$g_encountered_party", slot_town_castle, 1),
    # (assign, "$g_leave_encounter",1)]],
  

  # [party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_castle, 1),
                                        # ],
   # "Good day {sir/madam}. Don't worry. If anyone asks, we haven't seen you.", "runaway_serf_reconsider",[]],

  #[anyone|plyr,"runaway_serf_reconsider", [], "I have changed my mind. You must back to your master!", "runaway_serf_go_back",
   # [(party_set_slot, "$g_encountered_party", slot_town_castle, 0),
    # (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    # (call_script, "script_change_player_relation_with_center", ":quest_object_center", -2)]],

  #[anyone|plyr,"runaway_serf_reconsider", [], "Good. Go quickly now before I change my mind.", "runaway_serf_let_go",[]],
  
  
[party_tpl|pt_runaway_serfs,"start", [(party_slot_eq, "$g_encountered_party", slot_town_castle, 0),
                                        (get_party_ai_object, ":cur_ai_object"),
                                        (quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
                                        (neq, ":home_center", ":cur_ai_object")],
"Good day master. We were heading back to {s5}, but I am afraid we lost our way.", "runaway_serf_talk_caught",[]],

[anyone|plyr,"runaway_serf_talk_caught", [], "Do not test my patience. You are going back now!", "runaway_serf_go_back",[]],
  #[anyone|plyr,"runaway_serf_talk_caught", [], "Well, if you are that eager to go, then go.", "runaway_serf_let_go",
   # [(quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    # (call_script, "script_change_player_relation_with_center", ":quest_object_center", 1)]],
  
[party_tpl|pt_runaway_serfs,"start",[(quest_get_slot, ":home_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
									(str_store_party_name, s5, ":home_center")], 
"We are on our way back to {s5} master.", "runaway_serf_talk_again_return",[]],
  
[anyone|plyr,"runaway_serf_talk_again_return", [], "Make haste now. The sooner you return the better.", "runaway_serf_talk_again_return_2",[]],
[anyone|plyr,"runaway_serf_talk_again_return", [], "Good. Keep going.", "runaway_serf_talk_again_return_2",[]],
[anyone|plyr,"runaway_serf_talk_again_return_2", [], "Yes master. As you wish.", "close_window",[
	(call_script,"script_stand_back"),
	(assign, "$g_leave_encounter",1)]],
  

#Deserters
# [party_tpl|pt_deserters, "start", [(eq,"$talk_context",tc_party_encounter),
                                   # (party_get_slot,":protected_until_hours", "$g_encountered_party",slot_party_ignore_player_until),
                                   # (store_current_hours,":cur_hours"),
                                   # (store_sub, ":protection_remaining",":protected_until_hours",":cur_hours"),
                                   # (gt, ":protection_remaining", 0)], 
# "What do you want? You want to pay us some more money?", "deserter_paid_talk",[]],
# [anyone|plyr,"deserter_paid_talk", [], "Sorry to trouble you. I'll be on my way now.", "deserter_paid_talk_2a",[]],
# [anyone,"deserter_paid_talk_2a", [], "Yeah. Stop fooling around and go make some money.\
 # I want to see that purse full next time I see you.", "close_window",[(assign, "$g_leave_encounter",1)]],
# [anyone|plyr,"deserter_paid_talk", [], "No. It's your turn to pay me this time.", "deserter_paid_talk_2b",[]],
# [anyone,"deserter_paid_talk_2b", [], 
# "What nonsense are you talking about? You want trouble? You got it.", "close_window",[
       # (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,0),
       # (party_ignore_player, "$g_encountered_party", 0)]],
  
# [party_tpl|pt_deserters,"start", [(eq,"$talk_context",tc_party_encounter)], 
# "We are the free brothers.\
 # We will fight only for ourselves from now on.\
 # Now give us your gold or taste our steel.", "deserter_talk",[]],
 
 
##[anyone|plyr,"deserter_talk", [(check_quest_active, "qst_bring_back_deserters"),
##                                 (quest_get_slot, ":target_deserter_troop", "qst_bring_back_deserters", slot_quest_target_troop),
##                                 (party_count_members_of_type, ":num_deserters", "$g_encountered_party",":target_deserter_troop"),
##                                 (gt, ":num_deserters", 1)],
##   "If you surrender to me now, you will rejoin the army of your kingdom without being punished. Otherwise you'll get a taste of my sword.", "deserter_join_as_prisoner",[]],
#[anyone|plyr,"deserter_talk", [], "When I'm done with you, you'll regret ever leaving your army.", "close_window",[]],
#[anyone|plyr,"deserter_talk", [], "There's no need to fight. I am ready to pay for free passage.", "deserter_barter",[]],

##[anyone,"deserter_join_as_prisoner", [(call_script, "script_party_calculate_strength", "p_main_party"),
##                                        (assign, ":player_strength", reg0),
##                                        (store_encountered_party,":encountered_party"),
##                                        (call_script, "script_party_calculate_strength", ":encountered_party"),
##                                        (assign, ":enemy_strength", reg0),
##                                        (val_mul, ":enemy_strength", 2),
##                                        (ge, ":player_strength", ":enemy_strength")],
##   "All right we join you then.", "close_window",[(assign, "$g_enemy_surrenders", 1)]],
##[anyone,"deserter_join_as_prisoner", [], "TODO: We will never surrender!", "close_window",[(encounter_attack)]],

# [anyone,"deserter_barter", [], "Good. You are clever. You pay us {reg5} RPs. Then you can go.", "deserter_barter_2",[(assign,"$deserter_tribute",150),(assign,reg5,"$deserter_tribute")]],
# [anyone|plyr,"deserter_barter_2", [(store_troop_gold,reg2),(ge,reg2,"$deserter_tribute"),(assign,reg5,"$deserter_tribute")],
# "All right here's your {reg5} RPs.", "deserter_barter_3a",[(troop_remove_gold, "trp_player","$deserter_tribute")]],
# [anyone|plyr,"deserter_barter_2", [], "I don't have that much money with me", "deserter_barter_3b",[]],
# [anyone,"deserter_barter_3b", [], "Too bad. Then we'll have to sell you to the slavers.", "close_window",[]],

# [anyone,"deserter_barter_3a", [], 
# "Heh. That wasn't difficult now was it? All right. Go now.", "close_window",[
    # (store_current_hours,":protected_until"),
    # (val_add, ":protected_until", 72),
    # (party_set_slot,"$g_encountered_party",slot_party_ignore_player_until,":protected_until"),
    # (party_ignore_player, "$g_encountered_party", 72),
    # (assign, "$g_leave_encounter",1)]],

##### TODO: QUESTS COMMENT OUT END

#Tavernkeepers

# [anyone ,"start", [(store_conversation_troop,reg1),(ge,reg1,tavernkeepers_begin),(lt,reg1,tavernkeepers_end)],
# "Good day dear {sir/madam}. How can I help you?", "tavernkeeper_talk",[]],
  
# [anyone,"tavernkeeper_pretalk", [], "Anything else?", "tavernkeeper_talk",[]],

[anyone|plyr,"mayor_talk", [(check_quest_active,"qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (ge, ":item_count", ":quest_target_amount"),
                                     (assign, reg9, ":quest_target_amount"),
                                     (str_store_item_name, s4, ":quest_target_item")],
"I was told to deliver you {reg9} units of {s4}.", "mayor_deliver_wine",[]],

[anyone,"mayor_deliver_wine", [],
 "At last! Our stocks were almost depleted.\
 I had arranged for the delivery of the {s4} in advance.\
 And give {s9} my regards."+earned_reg14_rp_of_s14, "mayor_pretalk",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_gold_reward", "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (troop_remove_items, "trp_player", ":quest_target_item", ":quest_target_amount"),
    # (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    # (assign, ":xp_reward", ":quest_gold_reward"),
    # (val_mul, ":xp_reward", 4),
    # (add_xp_as_reward, ":xp_reward"),
    (assign, reg14, ":quest_gold_reward"),
	(str_store_faction_name, s14, "$ambient_faction"),
    (str_store_item_name, s4, ":quest_target_item"),
    (str_store_troop_name, s9, ":quest_giver_troop"),
    # (quest_get_slot, ":giver_town", "qst_deliver_wine", slot_quest_giver_center),
    # (call_script, "script_change_player_relation_with_center", ":giver_town", 2),
    (call_script, "script_change_player_relation_with_center", "$current_town", 1),
    (call_script, "script_finish_quest", "qst_deliver_wine", 100)]],

	
[anyone|plyr,"mayor_talk", [(check_quest_active,"qst_deliver_wine"),
                                     (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                     (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     (lt, ":item_count", ":quest_target_amount"),
                                     (gt, ":item_count", 0),
                                     (assign, reg9, ":quest_target_amount"),
                                     (str_store_item_name, s4, ":quest_target_item")],
"I was on a mission to deliver you {reg9} units of {s4}, but I lost some of the cargo to the enemy.", "mayor_deliver_wine_incomplete",[]],

[anyone,"mayor_deliver_wine_incomplete", [],
 "They will pay for this!\
 Well, at least we have some {s4}.\
 Thank you anyway."+earned_reg14_rp_of_s14, "mayor_pretalk",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_gold_reward", "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    (store_item_kind_count, ":item_count", ":quest_target_item"),
    (troop_remove_items, "trp_player", ":quest_target_item", ":item_count"),
    (val_mul, ":quest_gold_reward", ":item_count"),
    (val_div, ":quest_gold_reward", ":quest_target_amount"),
    #(call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    (call_script, "script_add_faction_rps", "$g_talk_troop_faction", ":quest_gold_reward"),
    (assign, reg14, ":quest_gold_reward"),
	(str_store_faction_name, s14, "$ambient_faction"),
    (assign, ":xp_reward", ":quest_gold_reward"),
    (val_mul, ":xp_reward", 4),
    (add_xp_as_reward, ":xp_reward"),
    (str_store_troop_name, s1, ":quest_giver_troop"),
    # (assign, ":debt", "$qst_deliver_wine_debt"),
    # (store_sub, ":item_left", ":quest_target_amount", ":item_count"),
    # (val_mul, ":debt", ":item_left"),
    # (val_div, ":debt", ":quest_target_amount"),
    # (val_add, "$debt_to_merchants_guild", ":debt"),
    (quest_get_slot, ":giver_town", "qst_deliver_wine", slot_quest_giver_center),
    (call_script, "script_change_player_relation_with_center", ":giver_town", 1),
    (call_script, "script_end_quest", "qst_deliver_wine")]],
  
# [anyone|plyr,"mayor_talk", [(check_quest_active,"qst_deliver_wine"),
                                     # (quest_slot_eq, "qst_deliver_wine", slot_quest_target_center, "$g_encountered_party"),
                                     # (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
                                     # (store_item_kind_count, ":item_count", ":quest_target_item"),
                                     # (eq, ":item_count", 0),
                                     # (quest_get_slot, reg9, "qst_deliver_wine", slot_quest_target_amount),
                                     # (str_store_item_name, s4, ":quest_target_item")],
# "I was told to deliver you {reg9} units of {s4}, but I lost the cargo on the way.", "tavernkeeper_deliver_wine_lost",[]],
  
# [anyone,"tavernkeeper_deliver_wine_lost", [],
 # "What? I was waiting for that {s4} for weeks!\
 # And now you are telling me that you lost it?\
 # You may rest assured that I will let {s1} know about this.", "mayor_pretalk",
   # [(add_xp_as_reward, 40),
    # (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    # (quest_get_slot, ":quest_giver_troop", "qst_deliver_wine", slot_quest_giver_troop),
    # (str_store_item_name, s4, ":quest_target_item"),
    # (str_store_troop_name, s1, ":quest_giver_troop"),
    # (val_add, "$debt_to_merchants_guild", "$qst_deliver_wine_debt"),
    # (call_script, "script_end_quest", "qst_deliver_wine")]],

##[anyone|plyr,"tavernkeeper_talk", [], "I need to hire some soldiers. Can you help me?", "tavernkeeper_buy_peasants",[]],
##[anyone,"tavernkeeper_buy_peasants",
##   [
##       (store_encountered_party,reg(3)),
##       (store_faction_of_party,reg(4),reg(3)),
##       (store_relation,reg(5),"fac_player_supporters_faction",reg(4)),
##       (lt, reg(5), -3),
##    ], "I don't think anyone from this town will follow somebody like you. Try your luck elsewhere.", "tavernkeeper_buy_peasants_2",[]],
##[anyone,"tavernkeeper_buy_peasants", [], "I know a few fellows who would follow you if you paid for their equipment.", "tavernkeeper_buy_peasants_2",[(set_mercenary_source_party,"$tavernkeeper_party"),[change_screen_buy_mercenaries]]],
##[anyone,"tavernkeeper_buy_peasants_2", [], "Anything else?", "tavernkeeper_talk",[]],
##
##[anyone|plyr,"tavernkeeper_talk", [], "I want to rest for a while.", "tavernkeeper_rest",[]],
###[anyone,"tavernkeeper_rest", [], "Of course... How long do you want to rest?", "tavernkeeper_rest_2",[]],
##[anyone,"tavernkeeper_rest",
##   [
##       (store_encountered_party,reg(3)),
##       (store_faction_of_party,reg(4),reg(3)),
##       (store_relation,reg(5),"fac_player_supporters_faction",reg(4)),
##       (lt, reg(5), -3),
##      ], "You look like trouble stranger. I can't allow you to stay for the night. No.", "close_window",
##   []],
##[anyone,"tavernkeeper_rest", [], "Of course... That will be {reg3} denars for the room and food. How long do you want to rest?", "tavernkeeper_rest_2",
##   [(store_party_size,reg(3)),
##    (val_add,reg(3),1),
##    (val_div,reg(3),3),
##    (val_max,reg(3),1),
##    (assign,"$tavern_rest_cost",reg(3))]],
##[anyone|plyr,"tavernkeeper_rest_2", [(store_time_of_day,reg(1)),
##                                       (val_add,reg(1),7),
##                                       (val_mod,reg(1),24),
##                                       (lt,reg(1),12),
##                                       (store_troop_gold,reg(8),"trp_player"),
##                                       (ge,reg(8),"$tavern_rest_cost"),
##                                       ],
##   "I want to rest until morning.", "close_window",
##   [(assign, reg(2), 13),(val_sub,reg(2),reg(1)),(assign, "$g_town_visit_after_rest", 1),(rest_for_hours, reg(2)),(troop_remove_gold, "trp_player","$tavern_rest_cost"),(call_script, "script_change_player_party_morale", 2)]],
##[anyone|plyr,"tavernkeeper_rest_2", [(store_time_of_day,reg(1)),
##                                       (val_add,reg(1),7),
##                                       (val_mod,reg(1),24),
##                                       (ge,reg(1),12),
##                                       (store_troop_gold,reg(8),"trp_player"),
##                                       (ge,reg(8),"$tavern_rest_cost"),
##                                       ],
##   "I want to rest until evening.", "close_window",
##   [(assign, reg(2), 28),(val_sub,reg(2),reg(1)),(assign, "$g_town_visit_after_rest", 1),(rest_for_hours, reg(2)),(troop_remove_gold, "trp_player","$tavern_rest_cost"),(call_script, "script_change_player_party_morale", 2)]],
##[anyone|plyr,"tavernkeeper_rest_2", [], "Forget it.", "close_window",[]],

# [anyone|plyr,"tavernkeeper_talk",[(store_current_hours,":cur_hours"),
								  # (val_sub, ":cur_hours", 24),
								  # (gt, ":cur_hours", "$buy_drinks_last_time")], 
# "I'd like to buy every man who comes in here tonight a jar of your best wine.", "tavernkeeper_buy_drinks",[]],

# [anyone,"tavernkeeper_buy_drinks",[], 
# "Of course, {my lord/my lady}. I reckon {reg5} denars should be enough for that. What should I tell the lads?", "tavernkeeper_buy_drinks_2",[
        # (assign, "$temp", 1000),
        # (assign, reg5, "$temp")]],

# [anyone|plyr,"tavernkeeper_buy_drinks_2",  [(store_troop_gold, ":gold", "trp_player"),
											# (ge, ":gold", "$temp"),
											# (str_store_party_name, s10, "$current_town")], 
# "Let everyone know of the generosity of {playername} to the people of {s10}.", "tavernkeeper_buy_drinks_end",[]],

# [anyone,"tavernkeeper_buy_drinks_end",[], 
# "Don't worry {sir/madam}. Your name will be cheered and toasted here all night.", "tavernkeeper_pretalk",[
       # (troop_remove_gold, "trp_player", "$temp"),
       # (call_script, "script_change_player_relation_with_center", "$current_town", 1),
       # (store_current_hours,":cur_hours"),
       # (assign, "$buy_drinks_last_time", ":cur_hours"),]],

    # #####################################################################################
   # Test: Tavern recruitment and Ale Begin ############################################
   #####################################################################################
# [anyone|plyr,"tavernkeeper_talk",[(store_current_hours,":cur_hours"),
								  # (val_sub, ":cur_hours", 24),
								  # (gt, ":cur_hours", "$buy_drinks_last_time")], 
# "I'd like to buy me and my men a barrel of your best ale.", "tavernkeeper_buy_drinks_troops",[]],

# [anyone,"tavernkeeper_buy_drinks_troops", [], 
# "Of course, {my lord/my lady}. I reckon {reg5} denars should be enough for that. What should I tell the lads?", "tavernkeeper_buy_drinks_troops_2",[
        # (assign, "$temp", 20),
      # (store_party_size_wo_prisoners, reg5, "p_main_party"),
      # (store_mul, "$temp", "$temp", reg5),
        # (assign, reg5, "$temp")]],

# [anyone|plyr,"tavernkeeper_buy_drinks_troops_2",[(store_troop_gold, ":gold", "trp_player"),
												# (ge, ":gold", "$temp"),
												# (str_store_party_name, s10, "$current_town")], 
# "The price is fair enough, let my men have at it.", "tavernkeeper_buy_drinks_troops_end",[]],

# [anyone,"tavernkeeper_buy_drinks_troops_end", [], 
# "Don't worry {sir/madam}. Your men will enjoy their pints.", "tavernkeeper_pretalk",[
      # (troop_remove_gold, "trp_player", "$temp"),
      # (call_script, "script_change_player_party_morale", 20),
      # (store_current_hours,":cur_hours"),
      # (assign, "$buy_drinks_last_time", ":cur_hours"),
      # (rest_for_hours, 2, 5, 0)]],

#[anyone|plyr,"tavernkeeper_buy_drinks_troops_2", [], "Actually, cancel that order.", "tavernkeeper_pretalk",[]],
   #####################################################################################
   # Test: Tavern recruitment and Ale End ##############################################
   #####################################################################################

#[anyone|plyr,"tavernkeeper_talk", [], "I guess I should leave now.", "close_window",[]],

#Tavern Talk (with companions)
#[anyone, "companion_recruit_yes", [(neg|hero_can_join, "p_main_party"),], "I don't think can lead any more men than you do now.\
# You need to release someone from service if you want me to join your party.", "close_window", []], 

# [anyone|plyr,"tavernkeeper_buy_drinks_2", [], "Actually, cancel that order.", "tavernkeeper_pretalk",[]],
# [anyone|plyr,"tavernkeeper_talk", [], "I guess I should leave now.", "close_window",[]],

#Tavern Talk (with companions)
#[anyone, "companion_recruit_yes", [(neg|hero_can_join, "p_main_party"),], "I don't think can lead any more men than you do now.\
# You need to release someone from service if you want me to join your party.", "close_window", []],



#Tavern Talk (with travelers)
# [anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
                     # (str_store_troop_name, s10, "$g_talk_troop"),
                     # (eq,"$g_talk_troop_met",0)],
# "Greetings, friend. You look like the kind of {man/person} who'd do well to know me.\
 # I travel a lot all across Calradia and keep an open ear.\
 # I can provide you information that you might find useful. For a meager price of course.", "tavern_traveler_talk", [(assign, "$traveler_land_asked", 0)]],

# [anyone, "start",[
     # (is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
     # (gt, "$last_lost_companion", 0),
     # (assign, ":companion_found_town", -1),
     # (troop_get_slot, ":companion_found_town", "$last_lost_companion", slot_troop_cur_center),
     # (is_between, ":companion_found_town", centers_begin, centers_end),
     # (str_store_troop_name, s10, "$last_lost_companion"),
     # (str_store_party_name, s11, ":companion_found_town")],
# "Greetings, {playername}. I saw your companion {s10} at a tavern in {s11} some days ago. I thought you might like to know.", "tavern_traveler_lost_companion_thanks",
   # [(assign, "$last_lost_companion", 0)]],

# [anyone|plyr, "tavern_traveler_lost_companion_thanks", [(troop_get_type, reg3, "$last_lost_companion")], "Thanks. I'll go and find {reg3?her:him} there.", "tavern_traveler_pretalk", []],
# [anyone|plyr, "tavern_traveler_lost_companion_thanks", [], "Thanks, but I don't really care.", "tavern_traveler_pretalk", []],

# [anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end)],
# "Greetings, {playername}.", "tavern_traveler_talk", [(assign, "$traveler_land_asked", 0)]],

# [anyone, "tavern_traveler_pretalk", [], "Yes?", "tavern_traveler_talk", []],
# [anyone|plyr, "tavern_traveler_talk", [(eq, "$traveler_land_asked", 0)], "What can you tell me about this land?", "tavern_traveler_tell_kingdoms", [(assign, "$traveler_land_asked", 1)]],
# [anyone, "tavern_traveler_tell_kingdoms", [], "Calradia is divided between rival kingdoms, which can neither manage to live in peace with their neighbours,\
 # nor completely eliminate them.\
 # As a result, there's seldom a break to the bitter wars which plague this land and drain its life blood.\
 # Well, at least this must be a good place to be for an adventurer such as yourself.\
 # With some luck and skill, you can make a name for yourself here, amass a fortune perhaps, or gain great power.\
 # Opportunities are endless and so are the rewards, if you are willing to risk your life for them.", "tavern_traveler_tell_kingdoms_2", []],
  
# [anyone|plyr, "tavern_traveler_tell_kingdoms_2", [], "Tell me more about these opportunities.", "tavern_traveler_tell_kingdoms_3", []],
# [anyone|plyr, "tavern_traveler_tell_kingdoms_2", [], "Thank you. That was all I needed to know", "close_window", []],

# [anyone, "tavern_traveler_tell_kingdoms_3", [(gt, "$player_has_homage", 0)], "Well, you probably know everything I could tell you already. You seem to be doing pretty well.",
   # "tavern_traveler_tell_kingdoms_4", []],
# [anyone, "tavern_traveler_tell_kingdoms_3", [], "The kingdoms will pay good money for mercenaries if they are engaged in a war.\
 # If you have done a bit of fighting, speaking with one of their lords will probably result in being offered a mercenary contract.\
 # However the real rewards come if you can manage to become a vassal to a king.\
 # A vassal can own villages, castles and towns and get rich with the taxes and revenues of these estates.\
 # Normally, only nobles of the realm own land in this way,\
 # but in time of war, a king will not hesitate to accept someone who distinugishes {himself/herself} on the battlefield as a vassal, and grant {him/her} the right to own land.",
   # "tavern_traveler_tell_kingdoms_4", []],

# [anyone, "tavern_traveler_tell_kingdoms_4", [], "The only path closed to a an adventurer such as you would be becoming the {king/queen} of a kingdom.\
 # The people and nobles of these lands would never accept an upstart adventurer as their ruler.\
 # But don't think that kings can sit on their thrones too comfortably, either. They have their own rivals,\
 # those who are born to the right family, who could go around and stir up trouble saying they have a better claim to the throne than the current king.\
 # If those claim holders could find supporters, they could easily start civil wars and perhaps even replace the king one day.",
   # "tavern_traveler_tell_kingdoms_5", []],

# [anyone|plyr, "tavern_traveler_tell_kingdoms_5", [], "I guess I heard enough already. Thank you.", "close_window", []],
# [anyone|plyr, "tavern_traveler_talk", [], "I am looking for one of my companions...", "tavern_traveler_companion_location", []],
# [anyone, "tavern_traveler_companion_location", [], "Maybe I can help you. Who are you looking for?", "tavern_traveler_companion_location_ask", []],

# [anyone|plyr|repeat_for_troops, "tavern_traveler_companion_location_ask", [
     # (store_repeat_object, ":troop_no"),
     # (is_between, ":troop_no", companions_begin, companions_end),
     # (troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),
     # (troop_slot_ge, ":troop_no", slot_troop_playerparty_history, 1),
     # (str_store_troop_name, s11, ":troop_no")],  
#"{s11}", "tavern_traveler_companion_location_ask_2",
   # [(store_repeat_object, "$temp")]],

# [anyone|plyr, "tavern_traveler_companion_location_ask", [],  "Never mind.", "tavern_traveler_pretalk", []],

# [anyone, "tavern_traveler_companion_location_ask_2", [(str_store_troop_name, s15, "$temp")], "I guess I know where {s15} is. For 30 denars, I'll tell you.", "tavern_traveler_companion_location_ask_money", []],

# [anyone|plyr, "tavern_traveler_companion_location_ask_money", [
     # (store_troop_gold, ":cur_gold", "trp_player"),
     # (ge, ":cur_gold", 30),
     # ], "All right. Here is 30 denars.", "tavern_traveler_companion_location_tell",
   # [(troop_remove_gold, "trp_player", 30) ]],
  
# [anyone|plyr, "tavern_traveler_companion_location_ask_money", [], "Never mind.", "tavern_traveler_pretalk", []],

# [anyone, "tavern_traveler_companion_location_tell", [], "{s15} is currently at {s11}.", "tavern_traveler_pretalk", [
     # (str_store_troop_name, s15, "$temp"),
     # (troop_get_slot, ":cur_center", "$temp", slot_troop_cur_center),
     # (str_store_party_name, s11, ":cur_center"),
     # ]],
  
# [anyone|plyr, "tavern_traveler_talk", [],
   # "Farewell.", "close_window", []],

# [anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
                     # (party_get_slot, ":info_faction", "$g_encountered_party", slot_center_traveler_info_faction),
                     # (str_store_faction_name, s17, ":info_faction")],
# "Greetings. They say you're the kind of {man/woman} who'd be interested to hear that I travel frequently to {s17}. I'll tell you all I know for a mere 100 denars.", "tavern_traveler_answer", []],

# [anyone|plyr, "tavern_traveler_answer", [(store_troop_gold, ":cur_gold", "trp_player"),
                                            # (ge, ":cur_gold", 100)],
# "Here's 100 denars. Tell me what you know.", "tavern_traveler_continue", [(party_get_slot, ":info_faction", "$g_encountered_party", slot_center_traveler_info_faction),
                                           # (call_script, "script_update_faction_traveler_notes", ":info_faction"),
                                           # (change_screen_notes, 2, ":info_faction")]],

# [anyone|plyr, "tavern_traveler_answer", [], "Sorry friend. I am not interested.", "close_window", []],
# [anyone, "tavern_traveler_continue", [], "Well, that's all I can tell you. Good bye.", "close_window", [(troop_remove_gold, "trp_player", 100),]],



#Tavern Talk (with troops)
[anyone, "start", [(eq, "$talk_context", tc_tavern_talk),
                     (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                     (party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                     (gt, ":mercenary_amount", 0),
                     (store_sub, reg3, ":mercenary_amount", 1),
                     (store_sub, reg4, reg3, 1),
                     (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                     (assign, ":join_cost", reg0),
                     (store_mul, reg5, ":mercenary_amount", reg0),
                     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                     (val_min, ":mercenary_amount", ":free_capacity"),
                     (store_troop_gold, ":cur_gold", "trp_player"),
                     (try_begin),
                       (gt, ":join_cost", 0),
                       (val_div, ":cur_gold", ":join_cost"),
                       (val_min, ":mercenary_amount", ":cur_gold"),
                     (try_end),
                     (assign, "$temp", ":mercenary_amount")],
"Do you have a need for mercenaries, Commander?\
 {reg3?Me and {reg4?{reg3} of my mates:one of my mates} are:I am} looking for a master.\
 We'll join you for {reg5} denars.", "mercenary_tavern_talk", []],

[anyone, "start", [(eq, "$talk_context", tc_tavern_talk)], "Any orders, Commander?", "mercenary_after_recruited", []],
[anyone|plyr, "mercenary_after_recruited", [], "Make your preparations. We'll be moving at dawn.", "mercenary_after_recruited_2", []],
[anyone|plyr, "mercenary_after_recruited", [], "Take your time. We'll be staying in this town for a while.", "mercenary_after_recruited_2", []],
[anyone, "mercenary_after_recruited_2", [], "Yes, Commander. We'll be ready when you tell us to leave.", "close_window", [(call_script,"script_stand_back"),]],

[anyone|plyr, "mercenary_tavern_talk", [(party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                                          (eq, ":mercenary_amount", "$temp"),
                                          (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          (store_mul, reg5, "$temp", reg0)],
"All right. I will hire all of you. Here is {reg5} denars.", "mercenary_tavern_talk_hire", []],

[anyone|plyr, "mercenary_tavern_talk", [(party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                                          (lt, "$temp", ":mercenary_amount"),
                                          (gt, "$temp", 0),
                                          (assign, reg6, "$temp"),
                                          (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          (store_mul, reg5, "$temp", reg0)],
"All right. But I can only hire {reg6} of you. Here is {reg5} denars.", "mercenary_tavern_talk_hire", []],


[anyone, "mercenary_tavern_talk_hire", [(store_random_in_range, ":rand", 0, 4),
                                          (try_begin),
                                            (eq, ":rand", 0),
                                            (gt, "$temp", 1),
                                            (str_store_string, s17,
                                             "@You chose well, {sir/madam}. My lads know how to keep their word and earn their pay."),
                                          (else_try),
                                            (eq, ":rand", 1), 
                                            (str_store_string, s17,
                                             "@Well done, {sir/madam}. Keep the money and wine coming our way, and there's no foe in Calradia you need fear."),
                                          (else_try),
                                            (eq, ":rand", 2), 
                                            (str_store_string, s17,
                                             "@We are at your service, {sir/madam}. Point us in the direction of those who need hurting, and we'll do the rest."),
                                          (else_try),
                                            (str_store_string, s17,
                                             "@You will not be dissapointed {sir/madam}. You will not find better warriors in all Calradia."),
                                          (try_end)],
"{s17}", "close_window", [  (call_script,"script_stand_back"),
							(party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                            (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                            (store_mul, ":total_cost", "$temp", reg0),
                            (troop_remove_gold, "trp_player", ":total_cost"),
                            (party_add_members, "p_main_party", ":mercenary_troop", "$temp"),
                            (party_set_slot, "$g_encountered_party", slot_center_mercenary_troop_amount, 0)]],

[anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (ge, ":free_capacity", 1)],
"That sounds good. But I can't afford to hire any more men right now.", "tavern_mercenary_cant_lead", []],
  
[anyone, "tavern_mercenary_cant_lead", [], "That's a pity. Well, {reg3?we will:I will} be lingering around here for a while,\
 if you need to hire anyone.", "close_window", [(call_script,"script_stand_back"),]],
  
[anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          (eq, ":free_capacity", 0)],
"That sounds good. But I can't lead any more men right now.", "tavern_mercenary_cant_lead", []],

[anyone|plyr, "mercenary_tavern_talk", [], "Sorry. I don't need any other men right now.", "close_window", [(call_script,"script_stand_back"),]],

#Trainers
#Reward for results
[anyone,"start", [(is_between, "$g_talk_troop", training_ground_trainers_begin, training_ground_trainers_end),
      (troop_slot_eq, "$g_talk_troop", slot_troop_trainer_waiting_for_result, 1),
      (troop_get_slot, ":training_mode", "$g_talk_troop", slot_troop_trainer_training_mode),
      (eq, ":training_mode", abm_gauntlet)],
   "You have survived up to Gauntlet wave {reg2}. {s4}", "trainer_pretalk",[
      (troop_set_slot, "$g_talk_troop", slot_troop_trainer_waiting_for_result, 0),
      (troop_get_slot, ":wave_reached", "$g_talk_troop", slot_troop_trainer_training_result),
      (store_sub, ":reward_xp", ":wave_reached", 1),
      (store_mul, ":reward_gold", ":reward_xp", 30), #30,60,..
      (val_mul, ":reward_xp", 50), #50,100,..
      (add_xp_as_reward, ":reward_xp"),
      #(call_script, "script_troop_add_gold", "trp_player", ":reward_gold"),
      (call_script, "script_add_faction_rps", "$ambient_faction", ":reward_gold"),
      (try_begin),
        (ge, ":wave_reached", 10),
        (str_store_string, s4, "@What an amazing feat of arms!"),
      (else_try),
        (ge, ":wave_reached", 5),
        (str_store_string, s4, "@Well done!"),
      (else_try),
        (ge, ":wave_reached", 2),
        (str_store_string, s4, "@Nice legwork."),
      (else_try),
        (str_store_string, s4, "@Heh."),
      (try_end),
      #Trait gain checks
      (try_begin),
        (ge, ":wave_reached", 5),
        (try_begin),
          (this_or_next|eq, "$g_talk_troop", "trp_trainer_mordor"), #used instead of faction check.. bad style?
          (eq, "$g_talk_troop", "trp_trainer_isengard"),
          (call_script, "script_cf_gain_trait_orc_pit_champion"),
        (try_end),
        (try_begin),
          (this_or_next|eq, "$g_talk_troop", "trp_trainer_khand"),
          (this_or_next|eq, "$g_talk_troop", "trp_trainer_rhun"),
          (eq, "$g_talk_troop", "trp_trainer_harad"),
          (call_script, "script_cf_gain_trait_brigand_friend"),
        (try_end),
      (try_end),
      (assign, reg2, ":wave_reached")]],

[anyone,"start", [(is_between, "$g_talk_troop", training_ground_trainers_begin, training_ground_trainers_end),
      (troop_slot_eq, "$g_talk_troop", slot_troop_trainer_waiting_for_result, 1),
      (troop_slot_eq, "$g_talk_troop", slot_troop_trainer_training_result, 100)],
"Very good, you've eliminated all the opponents.", "trainer_pretalk",[
      (troop_set_slot, "$g_talk_troop", slot_troop_trainer_waiting_for_result, 0),
      (troop_get_slot, ":training_mode", "$g_talk_troop", slot_troop_trainer_training_mode),
      (troop_get_slot, ":num_opponents", "$g_talk_troop", slot_troop_trainer_num_opponents_to_beat),
      (assign, ":reward_xp", 0),
      (assign, ":reward_gold", 0),
      #rewards
      (try_begin),
        (eq, ":training_mode", abm_training),
        (store_sub, ":reward_xp", ":num_opponents", 1),
        (val_mul, ":reward_xp", 20), #0-60
		(add_xp_to_troop, ":reward_xp", "trp_player"),
      (else_try),
        (eq, ":training_mode", abm_team),
        (store_div, ":reward_xp", ":num_opponents", 4),
        (val_sub, ":reward_xp", 1), #0-2
        (store_mul, ":reward_gold", ":reward_xp", 40), #0-80
        (val_mul, ":reward_xp", 30), #0-60
		(add_xp_as_reward, ":reward_xp"),
      (try_end), # no rewards for mass melee
      (call_script, "script_add_faction_rps", "$ambient_faction", ":reward_gold"),
      #(call_script, "script_troop_add_gold", "trp_player", ":reward_gold"),
      ]],
     
[anyone,"start", [(is_between, "$g_talk_troop", training_ground_trainers_begin, training_ground_trainers_end),
      (troop_slot_eq, "$g_talk_troop", slot_troop_trainer_waiting_for_result, 1),
      (try_begin),
        (troop_slot_ge, "$g_talk_troop", slot_troop_trainer_training_result, 75),
        (str_store_string, s4, "@Good moves, but you may still need some work to do."),
      (else_try),
        (troop_slot_ge, "$g_talk_troop", slot_troop_trainer_training_result, 50),
        (str_store_string, s4, "@More than half of the opponents, not bad."),
      (else_try),
        (troop_slot_ge, "$g_talk_troop", slot_troop_trainer_training_result, 25),
        (str_store_string, s4, "@You'll need to try harder than that."),
      (else_try),
        (str_store_string, s4, "@Well... better here than in combat, eh?"),
      (try_end)],
"{s4}.", "trainer_pretalk",[(troop_set_slot, "$g_talk_troop", slot_troop_trainer_waiting_for_result, 0)]],


[anyone,"start", [(is_between, "$g_talk_troop", training_ground_trainers_begin, training_ground_trainers_end)],
"Good day. Ready for some training today?", "trainer_talk",[]],

[anyone,"trainer_pretalk", [], "Are you ready for some training?", "trainer_talk",[]],
[anyone|plyr,"trainer_talk", [], "First, tell me something about combat...", "trainer_combat_begin",[]],
[anyone|plyr,"trainer_talk", [], "I'm ready for training.", "trainer_choose_mode",[]],
[anyone|plyr,"trainer_talk", [], "I need to leave now. Farewell.", "close_window",[(call_script,"script_stand_back"),]],
[anyone,"trainer_combat_begin", [], "What do you want to know?", "trainer_talk_combat",[]],
[anyone,"trainer_combat_pretalk", [], "What else do you want to know?", "trainer_talk_combat",[]],

[anyone|plyr,"trainer_talk_combat", [], "Tell me about defending myself.", "trainer_explain_defense",[]],
[anyone|plyr,"trainer_talk_combat", [], "Tell me about attacking with weapons.", "trainer_explain_attack",[]],
[anyone|plyr,"trainer_talk_combat", [], "Tell me about fighting on horseback.", "trainer_explain_horseback",[]],
#[anyone|plyr,"trainer_talk_combat", [], "Tell me about using ranged weapons.", "trainer_explain_ranged",[]],
#[anyone|plyr,"trainer_talk_combat", [], "Tell me about weapon types.", "trainer_explain_weapon_types",[]],
[anyone|plyr,"trainer_talk_combat", [], "I guess I know all the theory I need. Let's talk about something else.", "trainer_pretalk",[]],

[anyone,"trainer_explain_defense", [], "Good question. The first thing you should know as a fighter is how to defend yourself.\
 Keeping yourself out of harm's way is the first rule of combat, and it is much more important than giving harm to others.\
 Everybody can swing a sword around and hope to cut some flesh, but only those fighters that are experts at defense live to tell of it.",
	"trainer_explain_defense_2",[]],
[anyone,"trainer_explain_defense_2", [], "Now. Defending yourself is easiest if you are equipped with a shield.\
 Just block with your shield. [Hold down the right mouse button to defend yourself with the shield.] In this state, you will be able to deflect all attacks that come from your front. However, you will still be open to strikes from your sides or your back.", "trainer_explain_defense_3",[]],
[anyone|plyr,"trainer_explain_defense_3", [], "What if I don't have shield?", "trainer_explain_defense_4",[]],
[anyone,"trainer_explain_defense_4", [], "Then you will have to use your weapon to block your opponent.\
 This is a bit more difficult than defending with a shield.\
 Defending with a weapon, you can block against only ONE attack direction.\
 That is, you block against either overhead swings, side swings or thrusts.\
 Therefore you must watch your opponent carefully and start to block AFTER he starts his attack.\
 In this way you will be able to block against the direction of his current attack.\
 If you start to block BEFORE he makes his move, he may just attack in another direction than the one you are blocking against and score a hit.", "trainer_combat_pretalk",[]],
[anyone,"trainer_explain_attack", [], "Good question. Attacking is the best defence, they say.\
 A tactic many fighters find useful is taking an offensive stance and readying your weapon for attack, waiting for the right moment for swinging it.\
 [You can ready your weapon for attack by pressing and holding down the left mouse button.]", "trainer_explain_attack_2",[]],
[anyone|plyr,"trainer_explain_attack_2", [], "That sounds useful.", "trainer_explain_attack_3",[]],
[anyone,"trainer_explain_attack_3", [], "It is a good tactic, but remember that, your opponent may see that and take a defensive stance against the direction you are swinging your weapon.\
 If that happens, you must break your attack and quickly attack from another direction\
 [You may cancel your current attack by quickly tapping the right mouse button].", "trainer_explain_attack_4",[]],
[anyone|plyr,"trainer_explain_attack_4", [], "If my opponent is defending against the direction I am attacking from, I will break and use another direction.", "trainer_explain_attack_5",[]],
[anyone,"trainer_explain_attack_5", [], "Yes, selecting the direction you swing your weapon is a crucial skill.\
 There are four main directions you may use: right swing, left swing, overhead swing and thrust. You must use each one wisely.\
 [to control your swing direction with default controls, move your mouse in the direction you want to swing from as you press the left mouse button].", "trainer_combat_pretalk",[]],
[anyone,"trainer_explain_horseback", [], "Very good question. A horse may be a warrior's most powerful weapon in combat.\
 It gives you speed, height, power and initiative. A lot of deadly weapons will become even deadlier on horseback.\
 However you must pay particular attention to horse-mounted enemies couching their lances, as they may take down any opponent in one hit.\
 [To use the couched lance yourself, wield a lance or similar weapon, and speed up your horse without pressing attack or defense buttons.\
 after you reach a speed, you'll lower your lance. Then try to target your enemies by maneuvering your horse.]", "trainer_combat_pretalk",[]],

# Choosing training parameters
# Training mode   
[anyone,"trainer_choose_mode", [],
"We have several training modes to improve our soldiers' skills. Single combat will pit you against one to four opponents, in team combat your team of four will face four, eight or twelve combatants, and, finally, Gauntlet is the ultimate challenge for any warrior - you'll face waves of increasing number of opponents all by yourself. Mass melee is a simple brawl.^Which one do you prefer?", "trainer_choose_mode_player",[
     (assign, "$g_tld_training_mode", 0),
     (assign, "$g_tld_training_opponents", 0),
     (assign, "$g_tld_training_weapon", 0),
     (assign, "$g_tld_training_wave", 0)]],

[anyone|plyr,"trainer_choose_mode_player",[], "Single combat.", "trainer_choose_opponents",[(assign, "$g_tld_training_mode", abm_training)]],   
[anyone|plyr,"trainer_choose_mode_player",[(neq, "$g_talk_troop", "trp_trainer_dwarf")], 
"Team combat.", "trainer_choose_opponents",[(assign, "$g_tld_training_mode", abm_team)]],   
[anyone|plyr,"trainer_choose_mode_player",[(neq, "$g_talk_troop", "trp_trainer_dwarf")], 
"Gauntlet.", "trainer_choose_weapon",[(assign, "$g_tld_training_mode", abm_gauntlet),(assign, "$g_tld_training_opponents", 12)]],   
[anyone|plyr,"trainer_choose_mode_player",[(neq, "$g_talk_troop", "trp_trainer_dwarf")], 
"Mass melee.", "trainer_choose_weapon",[(assign, "$g_tld_training_mode", abm_mass_melee),(assign, "$g_tld_training_opponents", 12)]],
[anyone|plyr,"trainer_choose_mode_player",[], "None of that, I've changed my mind.", "trainer_pretalk",[]],
 
# Number of opponents
[anyone,"trainer_choose_opponents",[], "Now choose the number of opponents.", "trainer_choose_opponents_player",[]],   

[anyone|plyr,"trainer_choose_opponents_player",[(eq, "$g_tld_training_mode", abm_training)],
"One.", "trainer_choose_weapon",[(assign, "$g_tld_training_opponents", 1)]],   
[anyone|plyr,"trainer_choose_opponents_player",[(eq, "$g_tld_training_mode", abm_training)],
"Two.", "trainer_choose_weapon",[(assign, "$g_tld_training_opponents", 2)]],   
[anyone|plyr,"trainer_choose_opponents_player",[(eq, "$g_tld_training_mode", abm_training)],
"Three.", "trainer_choose_weapon",[(assign, "$g_tld_training_opponents", 3)]],   
[anyone|plyr,"trainer_choose_opponents_player",[(eq, "$g_tld_training_mode", abm_training)],
"Four, I feel lucky today.", "trainer_choose_weapon",[(assign, "$g_tld_training_opponents", 4)]],
   
[anyone|plyr,"trainer_choose_opponents_player",[(eq, "$g_tld_training_mode", abm_team)],
"Four.", "trainer_choose_weapon",[(assign, "$g_tld_training_opponents", 4)]],   
[anyone|plyr,"trainer_choose_opponents_player",[(eq, "$g_tld_training_mode", abm_team)],
"Eight.", "trainer_choose_weapon",[(assign, "$g_tld_training_opponents", 8)]],   
[anyone|plyr,"trainer_choose_opponents_player",[(eq, "$g_tld_training_mode", abm_team)],
"Twelve, me and my companions can take on anyone.", "trainer_choose_weapon",[(assign, "$g_tld_training_opponents", 12)]],   

[anyone|plyr,"trainer_choose_opponents_player",[], "None, I've changed my mind.", "trainer_pretalk",[]],
 
# Player weapon type
[anyone,"trainer_choose_weapon",[], "And finally choose your preferred weapon type.", "trainer_choose_weapon_player",[]],   

[anyone|plyr,"trainer_choose_weapon_player",[], "One-handed weapons.", "trainer_begin_training",[(assign, "$g_tld_training_weapon", itp_type_one_handed_wpn)]],   
[anyone|plyr,"trainer_choose_weapon_player",[], "Two-handed weapons.", "trainer_begin_training",[(assign, "$g_tld_training_weapon", itp_type_two_handed_wpn)]],   
[anyone|plyr,"trainer_choose_weapon_player",[], "Polearms.", "trainer_begin_training",[(assign, "$g_tld_training_weapon", itp_type_polearm)]],   
[anyone|plyr,"trainer_choose_weapon_player",[(neq, "$g_tld_training_mode", abm_mass_melee)], "Bows.", "trainer_begin_training",[(assign, "$g_tld_training_weapon", itp_type_bow)]],   
[anyone|plyr,"trainer_choose_weapon_player",[(neq, "$g_tld_training_mode", abm_mass_melee)], "Thrown weapons.", "trainer_begin_training",[(assign, "$g_tld_training_weapon", itp_type_thrown)]],   
[anyone|plyr,"trainer_choose_weapon_player",[], "None, I've changed my mind.", "trainer_pretalk",[]],

# Set up training and start 
[anyone,"trainer_begin_training",[], 
"Very well, here we go. Once you finish training, come back and speak to me.", "close_window",[
     (call_script,"script_stand_back"),
	 # Setting slots for use in reward dialog only - training code uses globals only (except slot_troop_trainer_training_result)
     (troop_set_slot, "$g_talk_troop", slot_troop_trainer_training_mode, "$g_tld_training_mode"),
     (troop_set_slot, "$g_talk_troop", slot_troop_trainer_num_opponents_to_beat, "$g_tld_training_opponents"),
     (troop_set_slot, "$g_talk_troop", slot_troop_trainer_training_result, 0),
     (troop_set_slot, "$g_talk_troop", slot_troop_trainer_waiting_for_result, 1),
     (call_script, "script_tld_start_training_at_training_ground")]],   


#Crooks

##[anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(eq,"$g_talk_troop_met",0),(eq,"$sneaked_into_town",0),(store_random_in_range, reg2, 2)],
##   "You {reg2?looking for:want} something?:", "crook_intro_1",[]],
##[anyone|plyr,"crook_intro_1",[],"I am trying to learn my way around the town.", "crook_intro_2",[]],
##  
##[anyone,"crook_intro_2",[(eq,"$crook_talk_order",0),(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
##"Then you came to the right guy. My name is {s1}, and I know everyone and everything that goes around in this town.\
## Anyone you want to meet, I can arrange it. Anything you need to know, I can find out. For the the right price, of course. Do you have gold?", "crook_intro_2a",[]],
##[anyone|plyr,"crook_intro_2a",[],"I have gold. Plenty of it.", "crook_intro_2a_1a",[]],
##[anyone|plyr,"crook_intro_2a",[],"Not really.", "crook_intro_2a_1b",[]],
##[anyone,"crook_intro_2a_1a",[],"Good. That means you and I will be great friends.", "crook_talk",[]],
##[anyone,"crook_intro_2a_1b",[],"Then you should look into earning some. Listen to me now, for I'll give you some free advice.\
## The easiest way to make money is to fight in the tournaments and bet on yourself. If you are good, you'll quickly get yourself enough money to get going.", "crook_talk",[]],
##
##[anyone,"crook_intro_2",[(eq,"$crook_talk_order",1),(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
##"Then you need to go no further. I am {s1}, and I can provide you anything... For the the right price.", "crook_intro_2b",[]],
##[anyone|plyr,"crook_intro_2b",[],"Are you a dealer?", "crook_intro_2b_1",[]],
##[anyone,"crook_intro_2b_1",[],"A dealer? Yes. I deal in knowledge... connections.. lies... secrets... Those are what I deal in. Interested?", "crook_talk",[]],
##
##[anyone,"crook_intro_2",[(eq,"$crook_talk_order",2),(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
##"Then this is your lucky day. Because you are talking to {s1}, and I know every piss-stained brick of this wicked town.\
##I know every person, every dirty little secret. And all that knowledge can be yours. For a price.", "crook_talk",[]],
##
##[anyone,"crook_intro_2",[(val_add,"$crook_talk_order",1),(str_store_troop_name,s1,"$g_talk_troop")],
## "Then {s1} is at your service {sir/madam}. If you want to know what's really going on in this town, or arrange a meeting in secret, then come to me. I can help you.", "crook_talk",[]],
##
##[anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(eq,"$g_talk_troop_met",0),(eq,"$sneaked_into_town",1),(eq,"$crook_sneak_intro_order",0),(val_add,"$crook_sneak_intro_order",1)],
##   "Good day. {playername} right?", "crook_intro_sneak_1",[]],
##[anyone|plyr,"crook_intro_sneak_1", [], "You must be mistaken. I'm just a poor pilgrim. I don't answer to that name.", "crook_intro_sneak_2",[]],
##[anyone,"crook_intro_sneak_2", [(str_store_troop_name,s1,"$g_talk_troop")], "Of course you do. And if the town guards knew you were here, they'd be upon you this minute.\
## But don't worry. Noone knows it is {playername} under that hood. Except me of course. But I am {s1}. It is my business to know things.", "crook_intro_sneak_3",[]],
##[anyone|plyr,"crook_intro_sneak_3", [], "You won't tip off the guards about my presence?", "crook_intro_sneak_4",[]],
##[anyone,"crook_intro_sneak_4", [], "What? Of course not! Well, maybe I would, but the new captain of the guards is a dung-eating cheat.\
## I led him to this fugitive, and the man was worth his weight in silver as prize money. But I swear, I didn't see a penny of it.\
## The bastard took it all to himself. So your secret is safe with me.", "crook_intro_sneak_5",[]],
##[anyone,"crook_intro_sneak_5", [], "Besides, I heard you have a talent for surviving any kind of ordeal.\
## I wouldn't want you to survive this one as well and then come after me with a sword. Ha-hah.", "crook_talk",[]],
##
##
##[anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(eq,"$g_talk_troop_met",0),(eq,"$sneaked_into_town",1),(str_store_troop_name,s1,"$g_talk_troop")],
##   "{s1} is at your service {sir/madam}. If you want to know what's really going on in this town, or arrange a meeting in secret, then come to me. I can help you.", "crook_talk",[]],

##[anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end),(store_character_level, ":cur_level", "trp_player"),(lt,":cur_level",8)],
##   "{You again?/Delighted to see you again my pretty.}", "crook_talk",[]],
##[anyone ,"start", [(is_between,"$g_talk_troop",crooks_begin,crooks_end)],
##   "I see that you need my services {sir/madam}...", "crook_talk",[]],
##[anyone ,"crook_pretalk", [],
##   "Is that all?", "crook_talk",[]],


  
##[anyone|plyr,"crook_talk", [], "I'm looking for a person...", "crook_search_person",[]],
##[anyone|plyr,"crook_talk", [], "I want you to arrange me a meeting with someone...", "crook_request_meeting",[]],
##[anyone|plyr,"crook_talk", [], "[Leave]", "close_window",[]],



#[anyone,"crook_enter_dungeon", [], "Alright but this will cost you 50 denars.", "crook_enter_dungeon_2", []],
#[anyone|plyr, "crook_enter_dungeon_2", [(store_troop_gold, ":cur_gold", "trp_player"),(ge, ":cur_gold", 50)],
#"TODO: Here it is. 50 denars.", "crook_enter_dungeon_3_1",[(troop_remove_gold, "trp_player", 50)]],
#[anyone|plyr, "crook_enter_dungeon_2", [(store_troop_gold, ":cur_gold", "trp_player"),(ge, ":cur_gold", 50)],
#"Never mind then.", "crook_pretalk",[]],
#[anyone|plyr, "crook_enter_dungeon_2", [(store_troop_gold, ":cur_gold", "trp_player"),(lt, ":cur_gold", 50)],
#"TODO: I don't have that much money.", "crook_enter_dungeon_3_2",[]],
#[anyone,"crook_enter_dungeon_3_1", [],
#"TODO: There you go.", "close_window", [(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],
#[anyone,"crook_enter_dungeon_3_2", [],
#"TODO: Come back later then.", "crook_pretalk",[]],
 

##[anyone, "crook_request_meeting", [],
##   "Who do you want to meet with?", "crook_request_meeting_2",[]],
##[anyone|plyr|repeat_for_troops,"crook_request_meeting_2", [(store_encountered_party, ":center_no"),
##                                                             (store_repeat_object, ":troop_no"),
##                                                             (is_between, ":troop_no", heroes_begin, heroes_end),
##                                                             (troop_get_slot, ":cur_center", ":troop_no", slot_troop_cur_center),
##                                                             (call_script, "script_get_troop_attached_party", ":troop_no"),
##                                                             (assign, ":cur_center_2", reg0),
##                                                             (this_or_next|eq, ":cur_center", ":center_no"),
##                                                             (eq, ":cur_center_2", ":center_no"),
##                                                             (neg|party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),#Neglect the ruler of the center
##                                                             (str_store_troop_name, s1, ":troop_no")],
##   "{s1}", "crook_request_meeting_3", [(store_repeat_object, "$selected_troop")]],
##
##[anyone|plyr,"crook_request_meeting_2", [], "Never mind.", "crook_pretalk", []],
##
##[anyone,"crook_request_meeting_3", [],
##   "Alright but this will cost you 50 denars.", "crook_request_meeting_4", []],
##
##[anyone|plyr, "crook_request_meeting_4", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                            (ge, ":cur_gold", 50)],
##   "TODO: Here it is. 50 denars.", "crook_search_person_5_1",[(troop_remove_gold, "trp_player", 50)]],
##
##[anyone|plyr, "crook_request_meeting_4", [(store_troop_gold, ":cur_gold", "trp_player"),
##                                            (ge, ":cur_gold", 50)],
##   "Never mind then.", "crook_pretalk",[]],
##
##[anyone|plyr, "crook_request_meeting_4", [(store_troop_gold, ":cur_gold", "trp_player"),(lt, ":cur_gold", 50)],
##   "TODO: I don't have that much money.", "crook_search_person_5_2",[]],
##
##[anyone, "crook_search_person_5_1", [],
##   "TODO: Ok.", "close_window",[(party_get_slot, ":town_alley", "$g_encountered_party", slot_town_alley),
##                                (modify_visitors_at_site,":town_alley"),(reset_visitors),
##                                (set_visitor,0,"trp_player"),
##                                (set_visitor,17,"$selected_troop"),
##                                (set_jump_mission,"mt_conversation_encounter"),
##                                (jump_to_scene,":town_alley"),
##                                (assign, "$talk_context", tc_back_alley),
##                                (change_screen_map_conversation, "$selected_troop")]],
##
##[anyone, "crook_search_person_5_2", [],"TODO: Come back later then.", "crook_pretalk",[]],
##[anyone, "crook_search_person"    , [],"TODO: Who are you searching for?", "crook_search_person_2",[]],
##[anyone|plyr|repeat_for_factions,"crook_search_person_2", [(store_repeat_object, ":faction_no"),
##                                                             (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
##                                                             (str_store_faction_name, s1, ":faction_no")],
##"TODO: I'm looking for a {s1}.", "crook_search_person_3", [(store_repeat_object, "$selected_faction")]],
##
##[anyone|plyr,"crook_search_person_2", [], "Never mind.", "crook_pretalk", []],
##[anyone, "crook_search_person_3", [],"TODO: Who?", "crook_search_person_4",[]],
##[anyone|plyr|repeat_for_troops,"crook_search_person_4", [(store_repeat_object, ":troop_no"),
##                                                           (is_between, ":troop_no", heroes_begin, heroes_end),
##                                                           (store_troop_faction, ":faction_no", ":troop_no"),
##                                                           (eq, ":faction_no", "$selected_faction"),
##                                                           (str_store_troop_name, s1, ":troop_no")],
##"{s1}", "crook_search_person_5", [(store_repeat_object, "$selected_troop")]],
##[anyone|plyr,"crook_search_person_4", [], "Never mind.", "crook_pretalk", []],
##[anyone, "crook_search_person_5", [(call_script, "script_get_information_about_troops_position", "$selected_troop", 0),
##                                     (eq, reg0, 1),
##                                     (str_store_troop_name, s1, "$selected_troop")],
##"TODO: I know where {s1} is at the moment, but hearing it will cost you 50 denars.", "crook_search_person_6",[]],
##[anyone, "crook_search_person_5", [],"TODO: Sorry I don't know anything.", "crook_pretalk",[]],
##[anyone|plyr, "crook_search_person_6", [(store_troop_gold, ":cur_gold", "trp_player"),(ge, ":cur_gold", 50)],
##"TODO: Here it is. 50 denars.", "crook_search_person_7_1",[(troop_remove_gold, "trp_player", 50)]],
##[anyone|plyr, "crook_search_person_6", [(store_troop_gold, ":cur_gold", "trp_player"),(ge, ":cur_gold", 50)],
##"Never mind then.", "crook_pretalk",[]],
##[anyone|plyr, "crook_search_person_6", [(store_troop_gold, ":cur_gold", "trp_player"),(lt, ":cur_gold", 50)],
##"TODO: I don't have that much money.", "crook_search_person_7_2",[]],
##[anyone, "crook_search_person_7_1", [(call_script, "script_get_information_about_troops_position", "$selected_troop", 0)],
##"{s1}", "crook_pretalk",[]],
##[anyone, "crook_search_person_7_2", [],"TODO: Come back later then.", "crook_pretalk",[]],
##  

#Mayor talk (town elder)

[anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end),
                   (eq, "$sneaked_into_town",1)],
"Away with you, vile beggar.", "close_window",[(call_script,"script_stand_back"),]],
   
[anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end),(eq,"$g_talk_troop_met",0),
                   (this_or_next|eq, "$players_kingdom", "$g_encountered_party_faction"),
                   (eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),],
"Good day, my lord.", "mayor_begin",[]],
[anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end),(eq,"$g_talk_troop_met",0),
                   (str_store_party_name, s9, "$current_town")],
"Hello stranger, you seem to be new to {s9}. I am the guild master of the town.", "mayor_talk",[]],
  
[anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end)],
"Good day, {playername}.", "mayor_begin",[]],


  #[anyone,"mayor_begin", [(check_quest_active, "qst_persuade_lords_to_make_peace"),
                          # (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_giver_troop, "$g_talk_troop"),
                          # (check_quest_succeeded, "qst_persuade_lords_to_make_peace"),
                          # (quest_get_slot, ":quest_target_troop", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
                          # (quest_get_slot, ":quest_object_troop", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),
                          # (val_mul, ":quest_target_troop", -1),
                          # (val_mul, ":quest_object_troop", -1),
                          # (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
                          # (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
                          # (str_store_troop_name, s12, ":quest_target_troop"),
                          # (str_store_troop_name, s13, ":quest_object_troop"),
                          # (str_store_faction_name, s14, ":quest_target_faction"),
                          # (str_store_faction_name, s15, ":quest_object_faction"),
                          # (str_store_party_name, s19, "$current_town"),
                         # ],
   # "{playername}, it was an incredible feat to get {s14} and {s15} make peace, and you made it happen.\
 # Your involvement has not only saved our town from disaster, but it has also saved thousands of lives, and put an end to all the grief this bitter war has caused.\
 # As the townspeople of {s19}, know that we'll be good on our word, and we are ready to pay the {reg12} denars we promised.", "lord_persuade_lords_to_make_peace_completed",
   # [#(quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
    # #(quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
    # # commented by GA, no peace in TLD
	# #Forcing 2 factions to make peace within 72 hours.
# #    (assign, "$g_force_peace_faction_1", ":quest_target_faction"),
# #    (assign, "$g_force_peace_faction_2", ":quest_object_faction"),
    # (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    # (assign, reg12, ":quest_reward"),
    # #TODO: Change these values
    # (add_xp_as_reward, 4000),
    # ]],


  #[anyone|plyr,"lord_persuade_lords_to_make_peace_completed", [],
   # "Thank you. Let me have the money.", "lord_persuade_lords_to_make_peace_pay",[]],
  #[anyone|plyr,"lord_persuade_lords_to_make_peace_completed", [],
   # "No need for a payment. I only did what was right.", "lord_persuade_lords_to_make_peace_no_pay",[]],

  #[anyone ,"lord_persuade_lords_to_make_peace_pay", [],
   # "Oh, yes, of course. We had already got the money for you.\
 # Here, please accept these {reg12} denars together with our most sincere thanks.\
 # Me and the people of our town will not forget your help.", "close_window",
   # [(quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    # (call_script, "script_troop_add_gold","trp_player",":quest_reward"),
    # (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    # (call_script, "script_end_quest", "qst_persuade_lords_to_make_peace"),
    # (quest_get_slot, ":quest_reward", "qst_persuade_lords_to_make_peace", slot_quest_gold_reward),
    # (assign, reg12, ":quest_reward")
    # ]],

  #[anyone ,"lord_persuade_lords_to_make_peace_no_pay", [],
   # "You are indeed an extraordinary person, {sir/madame}, and it is an honour for me to have known you.\
 # You not only did what was impossible and put an end to this terrible war, but you won't even accept a reward for it.\
 # Very well, I will not insist on the matter, but please know that you will have our eternal respect and gratitude.", "close_window",
   # [
    # (call_script, "script_change_player_honor", 3),
    # (call_script, "script_change_player_relation_with_center", "$current_town", 8),
    # (call_script, "script_end_quest", "qst_persuade_lords_to_make_peace"),
    # ]],

[anyone,"mayor_begin", [(check_quest_active, "qst_deal_with_night_bandits"),
                          (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_succeeded, "qst_deal_with_night_bandits"), (assign, reg14, 150),(str_store_faction_name, s14, "$ambient_faction"),],
"Very nice work, {playername}, you made short work of those lawless curs!"+earned_reg14_rp_of_s14, "lord_deal_with_night_bandits_completed",[
    (call_script, "script_finish_quest", "qst_deal_with_night_bandits", 100)]],

[anyone|plyr,"lord_deal_with_night_bandits_completed", [], "They had it coming.", "close_window",[(call_script,"script_stand_back"),]],

# TODO: CppCoder: Improve so the mayor accepts better metal scraps    

[anyone|plyr,"mayor_talk", [(check_quest_active,"qst_deliver_iron"),
                              (quest_slot_eq, "qst_deliver_iron", slot_quest_target_center, "$g_encountered_party"),
                              (quest_get_slot, ":quest_target_item", "qst_deliver_iron", slot_quest_target_item),
                              (quest_get_slot, ":quest_target_amount", "qst_deliver_iron", slot_quest_target_amount),
                              (store_item_kind_count, ":item_count", ":quest_target_item"),
                              (ge, ":item_count", ":quest_target_amount"),
                              (assign, reg9, ":quest_target_amount"),
                              (str_store_item_name, s4, ":quest_target_item")],
"Here's your metal supply, {reg9} units of {s4}.", "mayor_deliver_iron",[(assign, "$temp", 0)]],

[anyone|plyr,"mayor_talk", [(check_quest_active,"qst_deliver_iron"),
                              (quest_slot_eq, "qst_deliver_iron", slot_quest_target_center, "$g_encountered_party"),
                              (quest_get_slot, ":quest_target_item", "qst_deliver_iron", slot_quest_target_item),
                              (quest_get_slot, ":quest_target_amount", "qst_deliver_iron", slot_quest_target_amount),
                              (store_item_kind_count, ":item_count", ":quest_target_item"),
                              (gt, ":item_count", ":quest_target_amount"),
                              (store_mul, ":max_count", ":quest_target_amount", 2),
                              (val_min, ":max_count", ":item_count"),
                              (assign, "$temp", ":max_count"),
                              (assign, reg8, ":max_count"),
                              (assign, reg9, ":quest_target_amount"),
                              (str_store_item_name, s4, ":quest_target_item")],
"I've brought more metal, {reg8} units of {s4}, when you requested {reg9}.", "mayor_deliver_iron",[
        #reset quest amount and rank reward
        (quest_set_slot, "qst_deliver_iron", slot_quest_target_amount, "$temp"),
        (store_div, ":quest_rank_reward", "$temp", 2),
        (quest_set_slot, "qst_deliver_iron", slot_quest_rank_reward, ":quest_rank_reward"), #only increase rank reward, leave gold/xp the same (too much trouble)
        ]],

   
[anyone,"mayor_deliver_iron", [],
"Very nice work, {playername}. Our smiths will find ways to put everything they are given to good use.", "mayor_deliver_iron_completed",
    [ (quest_get_slot, ":quest_target_item", "qst_deliver_iron", slot_quest_target_item),
      (quest_get_slot, ":quest_target_amount", "qst_deliver_iron", slot_quest_target_amount),
      (troop_remove_items, "trp_player", ":quest_target_item", ":quest_target_amount"),
      (call_script, "script_finish_quest", "qst_deliver_iron", 100)]],

[anyone|plyr,"mayor_deliver_iron_completed", [], "I do what I can.", "close_window",[(call_script,"script_stand_back"),]],
   
[anyone|plyr,"mayor_talk", [(check_quest_active,"qst_deliver_food"),
                            (quest_slot_eq, "qst_deliver_food", slot_quest_target_center, "$g_encountered_party"),
                            #(quest_get_slot, ":quest_target_item", "qst_deliver_food", slot_quest_target_item),
                            (quest_get_slot, ":quest_target_amount", "qst_deliver_food", slot_quest_target_amount),
							(assign, ":item_count",0),
							(try_for_range, ":food_item", food_begin, food_end),
								(store_item_kind_count, ":item_count_i", ":food_item"),
								(val_add, ":item_count", ":item_count_i"),
							(try_end),
                            (ge, ":item_count", ":quest_target_amount"),
                            (assign, reg9, ":quest_target_amount")], #(str_store_item_name, s4, ":quest_target_item"),
"Here's your food, {reg9} units.", "mayor_deliver_food",[]],
   
[anyone,"mayor_deliver_food", [],
"Very nice work, {playername}, our food stores are full again and nobody will starve for now.", "mayor_deliver_food_completed",
    [ (quest_get_slot, ":to_give", "qst_deliver_food", slot_quest_target_amount),
	  # remove a total of :to_give food items
	  (try_for_range, ":food_item", food_begin, food_end),
			(ge, ":to_give", 0),
			(store_item_kind_count, ":item_count_i", ":food_item"),
			(val_min, ":item_count_i", ":to_give" ),
			(troop_remove_items, "trp_player", ":food_item", ":item_count_i"),
			(val_sub, ":to_give", ":item_count_i"),
	  (try_end),
      (call_script, "script_finish_quest", "qst_deliver_food", 100)]],

[anyone|plyr,"mayor_deliver_food_completed", [], "I do what I can.", "close_window",[(call_script,"script_stand_back"),]],

# Ryan BEGIN
[anyone,"mayor_begin", [(check_quest_active, "qst_deal_with_looters"),
                          (quest_slot_eq, "qst_deal_with_looters", slot_quest_giver_troop, "$g_talk_troop")],
"Ah, {playername}. Have you any progress to report?", "mayor_looters_quest_response",[]],

[anyone|plyr,"mayor_looters_quest_response",[
     (quest_get_slot, ":looter_template", "qst_deal_with_looters", slot_quest_target_party_template),
     (store_num_parties_destroyed_by_player, ":num_looters_destroyed", ":looter_template"),
     (party_template_get_slot,":previous_looters_destroyed",":looter_template",slot_party_template_num_killed),
     (val_sub,":num_looters_destroyed",":previous_looters_destroyed"),
     (quest_get_slot,":looters_paid_for","qst_deal_with_looters",slot_quest_current_state),
     (lt,":looters_paid_for",":num_looters_destroyed")],
"I've killed some tribal orcs.", "mayor_looters_quest_destroyed",[]],
  #[anyone|plyr,"mayor_looters_quest_response", [(eq,1,0)
  # ],
   # "I've brought you some goods.", "mayor_looters_quest_goods",[]],
[anyone|plyr,"mayor_looters_quest_response", [], "Not yet, sir. Farewell.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"mayor_looters_quest_destroyed", [],
"Aye, my scouts saw the whole thing. That should keep those tribal orcs at bay!"+earned_reg14_times_reg15_rp_of_s14, "mayor_looters_quest_destroyed_2",[
      (quest_get_slot, ":looter_template", "qst_deal_with_looters", slot_quest_target_party_template),
      (store_num_parties_destroyed_by_player, ":num_looters_destroyed", ":looter_template"),
      (party_template_get_slot,":previous_looters_destroyed",":looter_template",slot_party_template_num_killed),
      (val_sub,":num_looters_destroyed",":previous_looters_destroyed"),
      (quest_get_slot,":looters_paid_for","qst_deal_with_looters",slot_quest_current_state),
      (store_sub,":looter_bounty",":num_looters_destroyed",":looters_paid_for"),
      (assign,reg14,":looter_bounty"),(assign,reg15,40),
      (val_mul,":looter_bounty",40),
      #(call_script, "script_troop_add_gold","trp_player",":looter_bounty"),
      (call_script, "script_add_faction_rps", "$g_talk_troop_faction", ":looter_bounty"),
      (assign,":looters_paid_for",":num_looters_destroyed"),
      (quest_set_slot,"qst_deal_with_looters",slot_quest_current_state,":looters_paid_for")]],
	  
[anyone,"mayor_looters_quest_destroyed_2", [
      (quest_get_slot,":total_looters","qst_deal_with_looters",slot_quest_target_amount),
      (quest_slot_ge,"qst_deal_with_looters",slot_quest_current_state,":total_looters"), # looters paid for >= total looters
      (quest_get_slot,":xp_reward","qst_deal_with_looters",slot_quest_xp_reward),
      (quest_get_slot,":gold_reward","qst_deal_with_looters",slot_quest_gold_reward),
      (quest_get_slot,":rank_reward","qst_deal_with_looters",slot_quest_rank_reward),
      (add_xp_as_reward, ":xp_reward"),
      #(call_script, "script_troop_add_gold","trp_player",":gold_reward"),
      (call_script, "script_add_faction_rps", "$g_talk_troop_faction", ":gold_reward"),
      (call_script, "script_increase_rank", "$g_talk_troop_faction", ":rank_reward"),
      (call_script, "script_change_player_relation_with_center", "$current_town", 5),
      (quest_get_slot, ":looter_template", "qst_deal_with_looters", slot_quest_target_party_template),
      (call_script, "script_end_quest", "qst_deal_with_looters"),
      (try_for_parties, ":cur_party_no"),
        (party_get_template_id, ":cur_party_template", ":cur_party_no"),
        (eq, ":cur_party_template", ":looter_template"),
        (party_set_flags, ":cur_party_no", pf_quest_party, 0),
      (try_end)],
"And that's not the only good news! Thanks to you, the tribal orcs have ceased to be a threat. We've not had a single attack reported for some time now. \
 If there are any of them left, they've either run off or gone deep into hiding. That's good for the safety of the place! \
 I think that concludes your task, {playername}. Thank you, and farewell.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"mayor_looters_quest_destroyed_2", [], "Anything else you need?", "mayor_looters_quest_response",[]],


  #[anyone,"mayor_looters_quest_goods", [
      # (quest_get_slot,reg1,"qst_deal_with_looters",slot_quest_target_item),
  # ],
   # "Hah, I knew I could count on you! Just tell me which item to take from your baggage, and I'll send some men to collect it.\
 # I still need {reg1} denars' worth of goods.",
   # "mayor_looters_quest_goods_response",[
      # ]],
  #[anyone|plyr|repeat_for_100,"mayor_looters_quest_goods_response", [
      # (store_repeat_object,":goods"),
      # (val_add,":goods",trade_goods_begin),
      # (is_between,":goods",trade_goods_begin,trade_goods_end),
      # (player_has_item,":goods"),
      # (str_store_item_name,s5,":goods"),
  # ],
   # "{s5}.", "mayor_looters_quest_goods_2",[
      # (store_repeat_object,":goods"),
      # (val_add,":goods",trade_goods_begin),
      # (troop_remove_items,"trp_player",":goods",1),
      # (assign,":value",reg0),
      # (call_script, "script_troop_add_gold","trp_player",":value"),
      # (quest_get_slot,":gold_num","qst_deal_with_looters",slot_quest_target_item),
      # (val_sub,":gold_num",":value"),
      # (quest_set_slot,"qst_deal_with_looters",slot_quest_target_item,":gold_num"),
      # (str_store_item_name,s6,":goods"),
   # ]],
  #[anyone|plyr,"mayor_looters_quest_goods_response", [
  # ],
   # "Nothing at the moment, sir.", "mayor_looters_quest_goods_3",[]],

  #[anyone,"mayor_looters_quest_goods_3", [
  # ],
   # "Anything else you need?",
   # "mayor_looters_quest_response",[
      # ]],

  #[anyone,"mayor_looters_quest_goods_2", [
      # (quest_slot_ge,"qst_deal_with_looters",slot_quest_target_item,1),
      # (quest_get_slot,reg1,"qst_deal_with_looters",slot_quest_target_item),
  # ],
   # "Excellent, here is the money for your {s6}. Do you have any more goods to give me? I still need {reg1} denars' worth of goods.",
   # "mayor_looters_quest_goods_response",[
      # ]],
  #[anyone,"mayor_looters_quest_goods_2", [
      # (neg|quest_slot_ge,"qst_deal_with_looters",slot_quest_target_item,1),
      # (quest_get_slot,":xp_reward","qst_deal_with_looters",slot_quest_xp_reward),
      # (quest_get_slot,":gold_reward","qst_deal_with_looters",slot_quest_gold_reward),
      # (add_xp_as_reward, ":xp_reward"),
      # (call_script, "script_troop_add_gold","trp_player",":gold_reward"),
      # (call_script, "script_change_player_relation_with_center", "$current_town", 3),
      # (quest_get_slot, ":looter_template", "qst_deal_with_looters", slot_quest_target_party_template),
      # (call_script, "script_end_quest", "qst_deal_with_looters"),
      # (try_for_parties, ":cur_party_no"),
        # (party_get_template_id, ":cur_party_template", ":cur_party_no"),
        # (eq, ":cur_party_template", ":looter_template"),
        # (party_set_flags, ":cur_party_no", pf_quest_party, 0),
      # (try_end),
  # ],
   # "Well done, {playername}, that's the last of the goods I need. Here is the money for your {s6}, and a small bonus for helping me out.\
 # I'm afraid I won't be paying for any more goods, nor bounties on looters, but you're welcome to keep hunting the bastards if any remain.\
 # Thank you for your help, I won't forget it.",
   # "close_window",[
      # ]],
# Ryan END



[anyone,"mayor_begin", [(check_quest_active, "qst_move_cattle_herd"),
                          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_succeeded, "qst_move_cattle_herd")],
"Good to see you again {playername}. I have heard that you have delivered those people successfully. \
 I will tell our commander how reliable you are."+earned_reg14_rp_of_s14, "close_window",
   [(call_script,"script_stand_back"),
    (quest_get_slot, ":quest_gold_reward", "qst_move_cattle_herd", slot_quest_gold_reward),
    # (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    # (store_div, ":xp_reward", ":quest_gold_reward", 3),
    # (add_xp_as_reward, ":xp_reward"),
    #(call_script, "script_change_player_relation_with_center", "$current_town", 3),    
    (call_script, "script_finish_quest", "qst_move_cattle_herd", 100),
    (assign, reg14, ":quest_gold_reward")]],
  
[anyone,"mayor_begin", [(check_quest_active, "qst_move_cattle_herd"),
                          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_failed, "qst_move_cattle_herd")],
"I heard that you have lost those people on your way to {s9}. \
 I had a very difficult time explaining your failure to the commander here. \
 Do you have anything to say?", "move_cattle_herd_failed",[]],

[anyone|plyr ,"move_cattle_herd_failed", [], "I am sorry. But I was attacked on the way.", "move_cattle_herd_failed_2",[]],
[anyone|plyr ,"move_cattle_herd_failed", [], "I am sorry. Those people wandered off during the night.", "move_cattle_herd_failed_2",[]],

[anyone,"move_cattle_herd_failed_2", [],
"Well, it was your responsibility to deliver them safely, no matter what. \
 You should know that the commander demanded to know who is responsible for this failure. \
 So I told him it was you.", "close_window",
   [(call_script,"script_stand_back"),
    #(assign, "$debt_to_merchants_guild", 1000),
    (call_script, "script_change_player_relation_with_center", "$current_town", -2),
    (call_script, "script_end_quest", "qst_move_cattle_herd"),]],

  #[anyone,"mayor_begin", [(check_quest_active, "qst_kidnapped_girl"),
                          # (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 4),
                          # (quest_slot_eq, "qst_kidnapped_girl", slot_quest_giver_troop, "$g_talk_troop"),
                          # ],
   # "Dear {playername}. I am in your debt for bringing back my friend's daughter.\
  # Please take these {reg8} denars that I promised you.\
  # My friend wished he could give more but paying that ransom brought him to his knees.", "close_window",
   # [(quest_get_slot, ":quest_gold_reward", "qst_kidnapped_girl", slot_quest_gold_reward),
    # (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
    # (assign, reg8, ":quest_gold_reward"),
    # (assign, ":xp_reward", ":quest_gold_reward"),
    # (val_mul, ":xp_reward", 2),
    # (val_add, ":xp_reward", 100),
    # (add_xp_as_reward, ":xp_reward"),
    # (call_script, "script_change_player_relation_with_center", "$current_town", 2),    
    # (call_script, "script_end_quest", "qst_kidnapped_girl"),
    # ]],
  
[anyone,"mayor_begin", [(check_quest_active, "qst_troublesome_bandits"),
                          (check_quest_succeeded, "qst_troublesome_bandits"),
                          (quest_slot_eq, "qst_troublesome_bandits", slot_quest_giver_troop, "$g_talk_troop")],
"I have heard about your deeds. You have given those goblins the punishment they deserved. \
 You are really as good as they say."+earned_reg14_rp_of_s14,
   "mayor_friendly_pretalk", [(quest_get_slot, ":quest_gold_reward", "qst_troublesome_bandits", slot_quest_gold_reward),
                              # (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
                              # (assign, ":xp_reward", ":quest_gold_reward"),
                              # (val_mul, ":xp_reward", 7),
                              # (add_xp_as_reward, ":xp_reward"),
                              # (call_script, "script_change_player_relation_with_center", "$current_town", 2),
                              (call_script, "script_finish_quest", "qst_troublesome_bandits", 100),
                              (assign, reg14, ":quest_gold_reward")]],

# [anyone,"mayor_begin", [(ge, "$debt_to_merchants_guild", 50)],
# "According to my accounts, you owe the merchants guild {reg1} RPs.\
 # I'd better collect that now.", "merchant_ask_for_debts",[(assign,reg1,"$debt_to_merchants_guild")]],
# [anyone|plyr,"merchant_ask_for_debts", [[store_troop_gold,reg5,"trp_player"],[ge,reg5,"$debt_to_merchants_guild"]],
# "Alright. I'll pay my debt to you.", "merchant_debts_paid",[[troop_remove_gold, "trp_player","$debt_to_merchants_guild"],
                                                                # [assign,"$debt_to_merchants_guild",0]]],

# [anyone, "merchant_debts_paid", [], "Excellent. I'll let my fellow merchants know that you are clear of any debts.", "mayor_pretalk",[]],
# [anyone|plyr, "merchant_ask_for_debts", [], "I'm afraid I can't pay that sum now.", "merchant_debts_not_paid",[]],
# [anyone, "merchant_debts_not_paid", [(assign,reg1,"$debt_to_merchants_guild")], "In that case, I am afraid, I can't deal with you. Guild rules... \
 # Come back when you can pay the {reg1} RPs. \
 # And know that we'll be charging an interest to your debt. \
 # So the sooner you pay it, the better.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"mayor_begin", [], "What can I do for you?", "mayor_talk", []],
[anyone,"mayor_friendly_pretalk", [], "Now... What else may I do for you?", "mayor_talk",[]],
[anyone,"mayor_pretalk", [], "Yes?", "mayor_talk",[]],
[anyone|plyr,"mayor_talk", [], "Can you tell me about what you do?", "mayor_info_begin",[]],

[anyone|plyr,"mayor_talk", [(store_partner_quest, ":partner_quest"),
                              (lt, ":partner_quest", 0),
                              (neq, "$merchant_quest_last_offerer", "$g_talk_troop")],
"How can I serve our cause?", "merchant_quest_requested",[
     (assign,"$merchant_quest_last_offerer", "$g_talk_troop"),
     (call_script, "script_get_random_quest", "$g_talk_troop"),
     (assign, "$random_merchant_quest_no", reg0),
     (assign,"$merchant_offered_quest","$random_merchant_quest_no")]],

[anyone|plyr,"mayor_talk", [(store_partner_quest, ":partner_quest"),
                              (lt, ":partner_quest", 0),
                              (eq,"$merchant_quest_last_offerer", "$g_talk_troop"),
                              (ge,"$merchant_offered_quest",0)],
"About that task you needed me to do...", "merchant_quest_last_offered_job",[]],

[anyone|plyr,"mayor_talk", [(store_partner_quest,reg2),(ge,reg2,0)],
"About the task you gave me...", "merchant_quest_about_job",[]],

[anyone|plyr,"mayor_talk", [], "[Leave]", "close_window",[(call_script,"script_stand_back"),]],

[anyone, "mayor_info_begin", [(str_store_party_name, s9, "$current_town")],
"I am the local authority here in {s9}. You can say I am in charge of everyday tasks.\
 There is always something to do, so if you want to help let me know.", "mayor_info_talk",[(assign, "$mayor_info_lord_told",0)]],

[anyone|plyr,"mayor_info_talk",[(eq, "$mayor_info_lord_told",0)], "Who rules this town?", "mayor_info_lord",[]],
[anyone, "mayor_info_lord", [(party_get_slot, ":town_lord","$current_town",slot_town_lord),(str_store_troop_name, s10, ":town_lord")],
"Our lord is {s10}.", "mayor_info_talk",[(assign, "$mayor_info_lord_told",1)]],
  
[anyone|plyr,"mayor_info_talk",[], "That's all I need to know. Thanks.", "mayor_pretalk",[]],
  

[anyone,"merchant_quest_about_job", [], "What about it?", "merchant_quest_about_job_2",[]],
[anyone|plyr,"merchant_quest_about_job_2", [], "What if I can't finish it?", "merchant_quest_what_if_fail",[]],
[anyone|plyr,"merchant_quest_about_job_2", [], "Well, I'm still working on it.", "merchant_quest_about_job_working",[]],
[anyone,"merchant_quest_about_job_working", [], "Good. I'm sure you will handle it.", "mayor_pretalk",[]],


[anyone,"merchant_quest_last_offered_job", [], "Eh, you want to reconsider that. Good...", "merchant_quest_brief",
   [[assign,"$random_merchant_quest_no","$merchant_offered_quest"]]],


[anyone,"merchant_quest_what_if_fail", [(store_partner_quest,":partner_quest"),(eq,":partner_quest","qst_deliver_wine")],
   "I hope you don't fail. We cannot afford to lose the cargo you were carrying.", "mayor_pretalk",[]],
[anyone,"merchant_quest_what_if_fail", [], "Well, just do your best to finish it.", "mayor_pretalk",[]],

[anyone,"merchant_quest_taken", [], "Excellent. I am counting on you then. Good luck.", "mayor_pretalk",[]],
[anyone,"merchant_quest_stall", [], "Well, I'll see to find someone else. But tell me if you change your mind.", "mayor_pretalk",[]],

###################################################################3
# Random Merchant quests....
##############################
	
# Ryan BEGIN
  # deal with looters
[anyone,"merchant_quest_requested",[(eq,"$random_merchant_quest_no","qst_deal_with_looters")],
"Well, you look able enough. I think I might have something you could do.", "merchant_quest_brief", []],

[anyone,"merchant_quest_brief",[
     (eq,"$random_merchant_quest_no","qst_deal_with_looters"),
     (try_begin),
       (party_slot_eq,"$g_encountered_party",slot_party_type,spt_town),
       (str_store_string,s5,"@town"),
     (else_try),
       (party_slot_eq,"$g_encountered_party",slot_party_type,spt_village),
       (str_store_string,s5,"@village"),
     (try_end)],
"We've had some fighting near the {s5} lately, with all the chaos that comes with it,\
 and that's attracted a few bands of tribal orcs to raid the surroundings during the confusion.\
 I need somebody to teach those orcs a lesson.\
 Sound like your kind of work?", "merchant_quest_looters_choice", []],

[anyone|plyr,"merchant_quest_looters_choice", [], "Aye, I'll do it.", "merchant_quest_looters_brief", []],
[anyone|plyr,"merchant_quest_looters_choice", [], "I'm afraid you have to find someone else for that.", "merchant_quest_stall",[]],

[anyone,"merchant_quest_looters_brief", [
   (try_begin),
     (party_slot_eq,"$g_encountered_party",slot_party_type,spt_town),
     (str_store_string,s5,"@town"),
   (else_try),
     (party_slot_eq,"$g_encountered_party",slot_party_type,spt_village),
     (str_store_string,s5,"@village"),
   (try_end),

#     (party_get_slot,":merchant","$current_town",slot_town_merchant),
#     (troop_clear_inventory,":merchant"),
   (store_random_in_range,":random_num_looters",3,7),
   (quest_set_slot,"qst_deal_with_looters",slot_quest_target_amount,":random_num_looters"),
   (quest_get_slot, ":looter_template", "qst_deal_with_looters", slot_quest_target_party_template),
   (try_for_range,":unused",0,":random_num_looters"),
     (store_random_in_range,":random_radius",5,14),
     (set_spawn_radius,":random_radius"),
     (spawn_around_party,"$g_encountered_party",":looter_template"),
     (party_set_flags, reg0, pf_quest_party, 1),
     (party_set_faction, reg0, "fac_neutral"), #MV: so they don't get into fights
   (try_end),
   (str_store_troop_name, s9, "$g_talk_troop"),
   (str_store_party_name_link, s13, "$g_encountered_party"),
   (str_store_party_name, s4, "$g_encountered_party"),
   (setup_quest_text, "qst_deal_with_looters"),
   (str_store_string, s2, "@The {s9} of {s13} has asked you to deal with tribal orcs in the surrounding countryside."),
   (call_script, "script_start_quest", "qst_deal_with_looters", "$g_talk_troop"),
   (assign, "$g_leave_encounter",1)],
"Excellent! You'll find the tribal orcs roaming around the countryside, probably looking to raid more farms.\
 Kill the tribal orcs, and rid us of their presence.\
 I'll pass a word to our supply chief, and you will get rewarded for every band of tribal orcs you destroy,\
 until all the orcs are dealt with.", "close_window",[(call_script,"script_stand_back"),]],
# Ryan END

  # deliver wine:
[anyone,"merchant_quest_requested", [(eq,"$random_merchant_quest_no","qst_deliver_wine"),], 
"Thanks for offering to help.\
 Actually I was looking for someone to deliver some {s4}.\
 Perhaps you can do that...", "merchant_quest_brief",
   [(quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (str_store_item_name, s4, ":quest_target_item")]],

[anyone,"merchant_quest_brief", [(eq,"$random_merchant_quest_no","qst_deliver_wine")],
   "I have a cargo of {s6} that needs to be delivered to the {s10} in {s4}.\
 We need {reg5} units of {s6} to reach {s4} in {reg6} days.\
 Can you do that?" + promise_reg14_rp_of_s14, "merchant_quest_brief_deliver_wine",
   [(quest_get_slot, reg5, "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, reg14, "qst_deliver_wine", slot_quest_gold_reward),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (quest_get_slot, ":quest_target_center", "qst_deliver_wine", slot_quest_target_center),
    (quest_get_slot, ":quest_target_troop", "qst_deliver_wine", slot_quest_target_troop),
    (quest_get_slot, reg6, "qst_deliver_wine", slot_quest_expiration_days),
    (str_store_troop_name, s9, "$g_talk_troop"),
    (str_store_troop_name, s10, ":quest_target_troop"),
    (str_store_party_name_link, s3, "$g_encountered_party"),
    (str_store_party_name_link, s4, ":quest_target_center"),
    (str_store_item_name, s6, ":quest_target_item"),
    (setup_quest_text,"qst_deliver_wine"),
    (str_store_string, s2, "@{s9} of {s3} asked you to deliver {reg5} units of {s6} to the {s10} in {s4} in {reg6} days."),
    #s2 should not be changed until the decision is made
   ]],
  
[anyone|plyr,"merchant_quest_brief_deliver_wine", [(store_free_inventory_capacity,":capacity"),
                                                     (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
                                                     (ge, ":capacity", ":quest_target_amount")],
"Alright. I will make the delivery.", "merchant_quest_taken",
   [(quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
    (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
    (troop_add_items, "trp_player", ":quest_target_item",":quest_target_amount"),
    (call_script, "script_start_quest", "qst_deliver_wine", "$g_talk_troop")]],

[anyone|plyr,"merchant_quest_brief_deliver_wine", [], "I am afraid I can't carry all that cargo now.", "merchant_quest_stall",[]],
  
# deliver_food:
[anyone,"merchant_quest_requested", [(eq,"$random_merchant_quest_no","qst_deliver_food"),], 
"Thanks for offering to help.\
Actually I was looking for someone to supply us with Food.\
Perhaps you can do that...", "merchant_quest_brief",[]],

[anyone,"merchant_quest_brief", [(eq,"$random_merchant_quest_no","qst_deliver_food")],
"Our food supplies are dwindling and the supply trains are getting waylaid by the enemy.\
I need someone to bring us {reg5} units of food in {reg6} days, or we'll begin to starve.\
Maybe nearby friendly towns have enough for us too. What do you say?", "merchant_quest_brief_deliver_food",[
     (quest_get_slot, reg5, "qst_deliver_food", slot_quest_target_amount),
     (quest_get_slot, reg6, "qst_deliver_food", slot_quest_expiration_days),
     #(quest_get_slot, ":quest_target_item", "qst_deliver_food", slot_quest_target_item),
     (str_store_troop_name, s9, "$g_talk_troop"),
     (str_store_party_name_link, s3, "$g_encountered_party"),
	 (str_clear, s6), 
     (setup_quest_text,"qst_deliver_food"),
     (str_store_string, s2, "@The {s9} of {s3} asked you to bring him {reg5} units of food in {reg6} days.")]], #s2 should not be changed until the decision is made

[anyone|plyr,"merchant_quest_brief_deliver_food", [],
"Alright. I will find the food and bring it to you.", "merchant_quest_taken",[
    (call_script, "script_start_quest", "qst_deliver_food", "$g_talk_troop")]],

[anyone|plyr,"merchant_quest_brief_deliver_food", [], "I am sorry, you'll need to find someone else for that.", "merchant_quest_stall",[]],

# deliver_iron:
[anyone,"merchant_quest_requested", [(eq,"$random_merchant_quest_no","qst_deliver_iron"),
									(faction_slot_eq, "$g_encountered_party_faction", slot_faction_side, faction_side_good),], 
"A task, you say?\
 Actually I am looking for someone to supply us with ore and metals.\
 Mines and roads are not safe anymore, and getting resupplied with raw materials is more and more difficult.\
 The enemy must have its own obscure, but efficient ways of extracting ore, as we've seen even orcs and other lowly beasts in their ranks go around covered with metal.\
 Its quality matches that of the wearers: it is low-grade, cheap iron; the kind we would consider treacherous and not trust in normal times.\
 But in these times our smelters learnt how to deal with poor materials too, if necessary.\
 Every little bit helps.", "merchant_quest_brief",[]],

[anyone,"merchant_quest_requested", [(eq,"$random_merchant_quest_no","qst_deliver_iron"),
									(neg|faction_slot_eq, "$g_encountered_party_faction", slot_faction_side, faction_side_good),], 
"A task, you say?\
 The Master demands more troops every day, and they are never battle-worthy enough for Him... but armours don't just grow on skins, you know?\
^The maggots in charge of bringing ore supplies are treacherous and weak, they get themselves slaughtered too easily and we are left without materials.\
 But these men, these elves... they always go around covered with shiny, precious metals protecting them as if they were all kings, down to their lowest-born...\
^Scavenge their corpses and bring me the metal, {playername}. With a pound of that iron, our smelter can make enough material to cover an entire pack of warriors."
, "merchant_quest_brief",[]],

   
[anyone,"merchant_quest_brief", [
     (eq,"$random_merchant_quest_no","qst_deliver_iron"),
     (str_clear, s9), (str_store_troop_name, s9, "$g_talk_troop"),
     (str_clear, s3), (str_store_party_name_link, s3, "$g_encountered_party"),
	 (quest_get_slot, ":quest_target_item", "qst_deliver_iron", slot_quest_target_item),
	 (str_clear, s6),  (str_store_item_name, s6, ":quest_target_item"),
	 (quest_get_slot, reg5, "qst_deliver_iron", slot_quest_target_amount),
     (quest_get_slot, reg6, "qst_deliver_iron", slot_quest_expiration_days),
     ],
"We need {reg5} units of {s6} in {reg6} days, before our weaponsmiths run out of raw materials.\
 What do you say?", "merchant_quest_brief_deliver_iron",
   [
    
    (setup_quest_text,"qst_deliver_iron"),
    (quest_get_slot, reg0, "qst_deliver_iron", slot_quest_expiration_days),
    (str_store_string, s2, "@The {s9} of {s3} asked you to bring him {reg5} units of {s6} in {reg0} days.")]],#s2 should not be changed until the decision is made
   
[anyone|plyr,"merchant_quest_brief_deliver_iron", [],
"Alright. I will get the metal scraps and bring them to you.", "merchant_quest_taken", [
    (call_script, "script_start_quest", "qst_deliver_iron", "$g_talk_troop")]],

[anyone|plyr,"merchant_quest_brief_deliver_iron", [], "I am too busy to deal with that.", "merchant_quest_stall",[]],

#escort merchant caravan:
[anyone,"merchant_quest_requested", [(eq,"$random_merchant_quest_no","qst_escort_merchant_caravan")], "Thanks for offering to help.\
 Actually I was looking for someone to escort a supply train.\
 Perhaps you can do that...", "merchant_quest_brief",[]],

[anyone,"merchant_quest_brief", [(eq, "$random_merchant_quest_no", "qst_escort_merchant_caravan")],
"I am going to send a supply train to {s8}.\
 However with all those enemy patrols out there, I don't want to send them without an extra escort.\
 A group at least {reg4} would offer them adequate protection.\
 Can you lead that supply train to {s8} in 7 days?"+promise_reg14_rp_of_s14
 , "escort_merchant_caravan_quest_brief",
   [
# Bugfix - CppCoder
    (quest_get_slot, reg14, "qst_escort_merchant_caravan", slot_quest_gold_reward),
    (quest_get_slot, reg4, "qst_escort_merchant_caravan", slot_quest_target_amount),
    #(quest_get_slot, reg6, "qst_escort_merchant_caravan", slot_quest_expiration_days),
    (quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
    (str_store_party_name, s8, ":quest_target_center")]],
  
[anyone|plyr,"escort_merchant_caravan_quest_brief", [(store_party_size_wo_prisoners, ":party_size", "p_main_party"),
                                                       (quest_get_slot, ":quest_target_amount", "qst_escort_merchant_caravan", slot_quest_target_amount),
                                                       (ge,":party_size",":quest_target_amount")],
"Alright. I will escort the supply train.", "merchant_quest_taken",
   [(quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
    (quest_get_slot, ":quest_caravan", "qst_escort_merchant_caravan", slot_quest_target_party_template),
    (set_spawn_radius, 1),
    (spawn_around_party, "$g_encountered_party", ":quest_caravan"),
    (assign, ":quest_target_party", reg0),
    (party_set_ai_behavior, ":quest_target_party", ai_bhvr_track_party),
    (party_set_ai_object, ":quest_target_party", "p_main_party"),
    (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
    (party_set_slot, ":quest_target_party", slot_party_victory_value, ws_caravan_vp), # victory points for party kill
    (quest_set_slot, "qst_escort_merchant_caravan", slot_quest_target_party, ":quest_target_party"),
    (quest_set_slot, "qst_escort_merchant_caravan", slot_quest_current_state, 0),
    (str_store_party_name_link, s8, ":quest_target_center"),
    (setup_quest_text, "qst_escort_merchant_caravan"),
    (str_store_string, s2, "@Escort the supply train to {s8}."),
    (call_script, "script_start_quest", "qst_escort_merchant_caravan", "$g_talk_troop")]],
  
[anyone|plyr,"escort_merchant_caravan_quest_brief", [(store_party_size_wo_prisoners, ":party_size", "p_main_party"),
                                                       (quest_get_slot, ":quest_target_amount", "qst_escort_merchant_caravan", slot_quest_target_amount),
                                                       (lt,":party_size",":quest_target_amount"),],
"I am afraid I don't have that many soldiers with me.", "merchant_quest_stall",[]],
[anyone|plyr,"escort_merchant_caravan_quest_brief", [(store_party_size_wo_prisoners, ":party_size", "p_main_party"),
                                                       (quest_get_slot, ":quest_target_amount", "qst_escort_merchant_caravan", slot_quest_target_amount),
                                                       (ge,":party_size",":quest_target_amount"),],
"Sorry. I can't do that right now", "merchant_quest_stall",[]],

[anyone, "start", [ (check_quest_active, "qst_escort_merchant_caravan"),
					(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
					(eq,"$g_encountered_party",":quest_target_party"),
					(quest_slot_eq,"qst_escort_merchant_caravan", slot_quest_current_state, 2)],
"We can cover the rest of the way ourselves. Thanks.", "close_window",[
					(call_script,"script_stand_back"),
					(assign, "$g_leave_encounter", 1)]],
  
[anyone, "start", [ (check_quest_active, "qst_escort_merchant_caravan"),
                      (quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                      (eq,"$g_encountered_party",":quest_target_party"),
                      (quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
                      (store_distance_to_party_from_party, ":dist", ":quest_target_center",":quest_target_party"),
                      (lt,":dist",4),
                      (quest_slot_eq, "qst_escort_merchant_caravan", slot_quest_current_state, 1)],
"Well, we have almost reached {s21}. We can cover the rest of the way ourselves.\
 Thanks for escorting us. Good luck."+earned_reg14_rp_of_s14, "close_window",[
		(call_script,"script_stand_back"),
		(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
		(quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
		(quest_get_slot, ":quest_gold_reward", "qst_escort_merchant_caravan", slot_quest_gold_reward),
		(party_set_ai_behavior, ":quest_target_party", ai_bhvr_travel_to_party),
		(party_set_ai_object, ":quest_target_party", ":quest_target_center"),
		(party_set_flags, ":quest_target_party", pf_default_behavior, 0),
		(str_store_party_name, s21, ":quest_target_center"),
		(quest_set_slot, "qst_escort_merchant_caravan", slot_quest_current_state, 2),
		(call_script, "script_finish_quest", "qst_escort_merchant_caravan", 100),
		(assign, reg14, ":quest_gold_reward"),
		#(str_store_faction_name, s14, "$ambient_faction"),
		(store_faction_of_party, ":faction", "$g_encountered_party"),
		(str_store_faction_name, s14, ":faction"),
		(assign, "$g_leave_encounter", 1)]],
  
[anyone, "start", [ (check_quest_active, "qst_escort_merchant_caravan"),
                      (quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                      (eq,"$g_encountered_party",":quest_target_party"),
                      (quest_slot_eq, "qst_escort_merchant_caravan", slot_quest_current_state, 0)],
"Greetings. You must be our escort, right?", "merchant_caravan_intro_1",[(quest_set_slot, "qst_escort_merchant_caravan", slot_quest_current_state, 1),]],
  
[anyone|plyr,"merchant_caravan_intro_1", [], 
"Yes. My name is {playername}. I will lead you to {s1}.", "merchant_caravan_intro_2",[
   (quest_get_slot, ":quest_target_center", "qst_escort_merchant_caravan", slot_quest_target_center),
   (str_store_party_name, s1, ":quest_target_center")]],
  
[anyone,"merchant_caravan_intro_2", [], "Well, It is good to know we won't travel alone. What do you want us to do now?", "escort_merchant_caravan_talk",[]],
  
[anyone, "start", [ (check_quest_active, "qst_escort_merchant_caravan"),
                      (quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                      (eq, "$g_encountered_party", ":quest_target_party")],
"Eh. We've made it this far... What do you want us to do?", "escort_merchant_caravan_talk",[]],
  
[anyone|plyr,"escort_merchant_caravan_talk", [], "You follow my lead. I'll take you through a safe route.", "merchant_caravan_follow_lead",[]],
[anyone,"merchant_caravan_follow_lead", [], "Alright. We'll be right behind you.", "close_window",[
			(call_script,"script_stand_back"),
			(assign, "$escort_merchant_caravan_mode", 0),
			(assign, "$g_leave_encounter", 1)]],
[anyone|plyr,"escort_merchant_caravan_talk", [], "You stay here for a while. I'll go ahead and check the road.", "merchant_caravan_stay_here",[]],
[anyone,"merchant_caravan_stay_here", [], "Alright. We'll be waiting here for you.", "close_window",[
			(call_script,"script_stand_back"),
			(assign, "$escort_merchant_caravan_mode", 1),
			(assign, "$g_leave_encounter", 1)]],
#[anyone|plyr,"escort_merchant_caravan_talk", [], "You go ahead to {s1}. I'll catch up with you.", "merchant_caravan_go_to_destination",[]],
#[anyone,"merchant_caravan_go_to_destination", [], "Alright. But stay close.", "close_window",[(assign,"$escort_merchant_caravan_mode",2),(assign, "$g_leave_encounter", 1)]],


# Troublesome bandits:
[anyone,"merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_troublesome_bandits")],
 "Actually, I was looking for an able commander like you.\
 There's this group of particularly troublesome goblins.\
 They have infested the neighbourhood and are preying on supply trains and stray warriors.\
 They have avoided all our patrols up to now.\
 If someone doesn't stop them soon, I would need to request serious military action...", "merchant_quest_brief",[]],

[anyone,"merchant_quest_brief", [(eq,"$random_merchant_quest_no", "qst_troublesome_bandits")],
  "I need someone to hunt down those troublesome goblins.\
 It's dangerous work. But I believe that you are the one for it.\
 What do you say?"+promise_reg14_rp_of_s14, "troublesome_bandits_quest_brief",[(quest_get_slot, reg14, "qst_troublesome_bandits", slot_quest_gold_reward)]],

[anyone|plyr,"troublesome_bandits_quest_brief", [],
"Alright. I will hunt down the goblins.", "merchant_quest_taken_bandits",
   [(set_spawn_radius,7),
    (quest_get_slot, ":quest_giver_center", "qst_troublesome_bandits", slot_quest_giver_center),
    (spawn_around_party,":quest_giver_center","pt_troublesome_bandits"),
    (quest_set_slot, "qst_troublesome_bandits", slot_quest_target_party, reg0),
    (store_num_parties_destroyed,"$qst_troublesome_bandits_eliminated","pt_troublesome_bandits"),
    (store_num_parties_destroyed_by_player, "$qst_troublesome_bandits_eliminated_by_player", "pt_troublesome_bandits"),
    (str_store_troop_name, s9, "$g_talk_troop"),
    (str_store_party_name_link, s4, "$g_encountered_party"),
    (setup_quest_text,"qst_troublesome_bandits"),
    (str_store_string, s2, "@The {s9} of {s4} asked you to hunt down the troublesome goblins in the vicinity of the town."),
    (call_script, "script_start_quest", "qst_troublesome_bandits", "$g_talk_troop")]],

[anyone,"merchant_quest_taken_bandits", [], "You will? I am so happy to hear that. Good luck to you.", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"troublesome_bandits_quest_brief", [], "Sorry. I don't have time for this right now.", "merchant_quest_stall",[]],



#deal with night bandits
[anyone,"merchant_quest_requested",[(eq, "$random_merchant_quest_no", "qst_deal_with_night_bandits")],
"Do I indeed! There's a group of rogue goblins harassing the place, and I'm at the end of my rope as to how to deal with them.\
 They've been ambushing and robbing drunken recruits under the cover of night,\
 and then fading away quick as lightning when the guards finally show up. We've not been able to catch a one of them.\
 They only attack lone people, never daring to show themselves when there's a group about.\
 I need someone who can take on these goblins alone and win. That seems to be the only way of getting rid of them.\
 Are you up to the task?", "merchant_quest_deal_with_night_bandits",[]],

[anyone,"merchant_quest_brief",[(eq,"$random_merchant_quest_no","qst_deal_with_night_bandits")],
"There's a group of rogue goblins harassing the place, and I'm at the end of my rope as to how to deal with them.\
 They've been ambushing and robbing drunken recruits under the cover of night,\
 and then fading away quick as lightning when the guards finally show up. We've not been able to catch a one of them.\
 They only attack lone people, never daring to show themselves when there's a group about.\
 I need someone who can take on these goblins alone and win. That seems to be the only way of getting rid of them.\
 Are you up to the task?", "merchant_quest_deal_with_night_bandits",[]],

[anyone|plyr,"merchant_quest_deal_with_night_bandits", [],
"Killing rogue goblins? Why, certainly!", "deal_with_night_bandits_quest_taken",[
     (str_store_party_name_link, s14, "$g_encountered_party"),
     (str_store_troop_name, s9, "$g_talk_troop"),
     (setup_quest_text, "qst_deal_with_night_bandits"),
     (str_store_string, s2, "@The {s9} of {s14} has asked you to deal with a group of goblins making trouble in {s14}. They only come out at night, and only attack lone people on the streets."),
     (call_script, "script_start_quest", "qst_deal_with_night_bandits", "$g_talk_troop")]],
  
[anyone|plyr, "merchant_quest_deal_with_night_bandits", [], "No, I'm not interested.", "merchant_quest_stall",[]],

[anyone,"deal_with_night_bandits_quest_taken", [], "That takes a weight off my shoulders, {playername}.\
 You can expect a fine reward if you come back successful. Just don't get yourself killed, eh?", "mayor_pretalk",[]],


#move cattle herd
[anyone,"merchant_quest_requested", [(eq, "$random_merchant_quest_no", "qst_move_cattle_herd"),
                                     (try_begin),
                                       (faction_slot_eq, "$g_encountered_party_faction", slot_faction_side, faction_side_good),
                                       (str_store_string, s12, "@refugees"),
                                     (else_try),
                                       (str_store_string, s12, "@slaves"),
                                     (try_end),
                                     (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
                                     (str_store_party_name,s13,":target_center"),],
"The garrison commander here is looking for a resourceful warrior to take a group of {s12} to {s13}.", "merchant_quest_brief",[]],

[anyone,"merchant_quest_brief",[
    (eq,"$random_merchant_quest_no","qst_move_cattle_herd"),
    (quest_get_slot, reg14, "qst_move_cattle_herd", slot_quest_gold_reward),
    (quest_get_slot, reg6, "qst_move_cattle_herd", slot_quest_expiration_days),
    (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
    (str_store_party_name, s13, ":target_center")],
"The group must arrive at {s13} within {reg6} days. Sooner is better, much better, \
 but it must be absolutely no later than {reg6} days. \
 Can you do that?"+promise_reg14_rp_of_s14, "move_cattle_herd_quest_brief",[]],

#MV: remove when quest dialogs are done, or bugs are fixed . No, DON'T REMOVE, ever (MT). MV: ok.
[anyone,"merchant_quest_brief", [(str_store_quest_name,s4,"$random_merchant_quest_no")],
"DEBUG: It seems some coder abused his arcane powers, and forgot to put a dialog here. The quest is {s4}.", "mayor_pretalk",[]],
  
[anyone|plyr,"move_cattle_herd_quest_brief", [], 
"Aye, I can take them to {s13}.","move_cattle_herd_quest_taken",[
     #(call_script, "script_create_cattle_herd", "$g_encountered_party", 0),
     (set_spawn_radius, 1),
     (spawn_around_party, "$g_encountered_party", "pt_village_farmers"),
     (assign, ":herd_party", reg0),
     (str_store_faction_name, s1, "$g_encountered_party_faction"),
     (try_begin),
       (faction_slot_eq, "$g_encountered_party_faction", slot_faction_side, faction_side_good),
       (party_set_name, ":herd_party", "@{s1} Refugees"),
       (str_store_string, s12, "@refugees"),
     (else_try),
       (party_set_name, ":herd_party", "@{s1} Slaves"),
       (str_store_string, s12, "@slaves"),
     (try_end),
     (party_set_faction, ":herd_party", "$g_encountered_party_faction"),
     (party_set_slot, ":herd_party", slot_party_type, spt_cattle_herd),
     (party_set_slot, ":herd_party", slot_party_ai_state, spai_undefined),
     (party_set_slot, ":herd_party", slot_cattle_driven_by_player, 1),
     (party_set_ai_behavior, ":herd_party", ai_bhvr_escort_party), #make it easy on the player
     (party_set_ai_object, ":herd_party", "p_main_party"),
     #(party_set_ai_behavior, ":herd_party", ai_bhvr_hold),
     (party_set_slot, ":herd_party", slot_party_commander_party, -1),
     (quest_set_slot, "qst_move_cattle_herd", slot_quest_target_party, ":herd_party"),
     (str_store_party_name_link, s10, "$g_encountered_party"),
     (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
     (str_store_party_name_link, s13, ":target_center"),
     (quest_get_slot, reg8, "qst_move_cattle_herd", slot_quest_gold_reward),
     (setup_quest_text, "qst_move_cattle_herd"),
     (str_store_troop_name, s11, "$g_talk_troop"),
     (str_store_string, s2, "@The {s11} of {s10} asked you to escort some {s12} to {s13}."),
     (call_script, "script_start_quest", "qst_move_cattle_herd", "$g_talk_troop")]],
	 
[anyone|plyr,"move_cattle_herd_quest_brief", [],"I am sorry, but no.", "merchant_quest_stall",[]],

[anyone,"move_cattle_herd_quest_taken", [], "Splendid. You can find them right outside the town.\
 After you take them to {s13}, return back to me and I will give you your pay.", "mayor_pretalk",[]],


################################################# 
#################### Random merchant quests end

[anyone,"merchant_quest_requested", [], "Thanks, commander, but we don't need anything else right now. I'll let you know when we do.", "mayor_pretalk",[]],


#Village elders
# ...

#Goods Merchants
# [anyone ,"start", [(is_between,"$g_talk_troop",goods_merchants_begin,goods_merchants_end),
                     # (eq, "$sneaked_into_town",1)],
# "Away with you, vile beggar.", "close_window",[]],
  
# [anyone ,"start", [(is_between,"$g_talk_troop",goods_merchants_begin,goods_merchants_end),
                     # (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
# "{My lord/my lady}, you honour my humble shop with your presence.", "goods_merchant_talk",[]],
# [anyone ,"start", [(is_between,"$g_talk_troop",goods_merchants_begin,goods_merchants_end)],
# "Welcome commander. What can I do for you?", "goods_merchant_talk",[]],

#[trp_salt_mine_merchant,"start", [], "Hello.", "goods_merchant_talk",[]],
#[anyone,"merchant_begin", [], " What can I do for you?", "goods_merchant_talk",[]],
#[anyone,"goods_merchant_pretalk", [], "Anything else?", "goods_merchant_talk",[]],

[anyone|plyr,"goods_merchant_talk", [(call_script, "script_check_equipped_items", "trp_player")], "I want to buy a few items... and perhaps sell some.", "goods_trade_requested",[]],
[anyone,"goods_trade_requested", [], "Sure, sure... Here, have a look at my stock...", "goods_trade_completed",[#(assign, "$equip_needs_checking", 1),
  (change_screen_trade)]],
[anyone,"goods_trade_completed", [], "Anything else?", "goods_merchant_talk",[]],
[anyone|plyr,"goods_merchant_talk", [], "Nothing. Thanks.", "close_window",[(call_script,"script_stand_back"),]],
  

#### ARENA MASTERS
# ...
  
#Quest dialogs
  
[party_tpl|pt_troublesome_bandits,"start", [(quest_slot_eq, "qst_troublesome_bandits", slot_quest_target_party, "$g_encountered_party")],"What? We will kill. We will take your food and mounts and eat 'em. We will eat you.", "troublesome_bandits_intro_1",[]],
[anyone|plyr,"troublesome_bandits_intro_1", [],
"You'll regret causing trouble around these parts. You should have never left your mountain caves.",
   "troublesome_bandits_intro_2", []],
[anyone,"troublesome_bandits_intro_2", [],
"Kill now! Eat later!", "close_window",[(call_script,"script_stand_back"),(encounter_attack)]],
 
[party_tpl|pt_fangorn_orcs,"start", [(quest_slot_eq, "qst_treebeard_kill_orcs", slot_quest_target_party, "$g_encountered_party")],
   "Eh? The Old Man won't be happy if you interrupt the work of his servants.", "fangorn_orcs_intro_1",[]],
[anyone|plyr,"fangorn_orcs_intro_1", [], "Stop harming this forest and leave, or you'll regret it!", "fangorn_orcs_intro_2", []],
[anyone,"fangorn_orcs_intro_2", [], "Har-har! We'll cut and burn as we please! After we are done with you...", "close_window",[(encounter_attack)]],
 
[party_tpl|pt_rescued_prisoners,"start", [(eq,"$talk_context",tc_party_encounter)], "Do you want us to follow you?", "disbanded_troop_ask",[]],
[anyone|plyr,"disbanded_troop_ask", [], "Yes. Let us ride together.", "disbanded_troop_join",[]],
[anyone|plyr,"disbanded_troop_ask", [], "No. Not at this time.", "close_window",[(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)]],
[anyone,"disbanded_troop_join", [[neg|party_can_join]], "Unfortunately. You do not have room in your party for us.", "close_window",[(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)]],
[anyone,"disbanded_troop_join", [], "We are at your command.", "close_window",[(call_script,"script_stand_back"),(party_join),(assign, "$g_leave_encounter",1)]],
   
[party_tpl|pt_enemy,"start", [(eq,"$talk_context",tc_party_encounter)], "You will not capture me again. Not this time.", "enemy_talk_1",[]],
[party_tpl|pt_enemy|plyr,"enemy_talk_1", [], "You don't have a chance against me. Give up.", "enemy_talk_2",[]],
[party_tpl|pt_enemy,"enemy_talk_2", [], "I will give up when you are dead!", "close_window",[(call_script,"script_stand_back"),(encounter_attack)]],


# prisoner talk
#[anyone|plyr,"prisoner_chat_00", [], "Guards, bring me that one!", "prisoner_chat_2",[]],

# CppCoder bugfix: Trolls go rawr...
[anyone,"prisoner_chat_00", [(store_conversation_troop,reg1),(troop_get_type, ":troll", reg1),(eq, ":troll", tf_troll)], "^^GROWL!^^", "close_window",[]],

[anyone,"prisoner_chat_00", [], "You put me in chains already, what more do you want?", "prisoner_chat_3",[]],
[anyone|plyr,"prisoner_chat_3", [],"Don't try anything, you scum!", "prisoner_chat_4",[]],
[anyone|plyr,"prisoner_chat_3", [
  (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),(neg|troop_is_hero,"$g_talk_troop"),
  (str_clear, s20),(try_begin),(neq, "$talk_context", tc_troop_review_talk ),(str_store_string, s20, "@_Guards, slaughter him!"), (try_end),
], 
"You happen to be our next dinner!{s20}", "prisoner_slaughter",[]],
[anyone,"prisoner_chat_4", [],"Yeah, like I'm in a position for trying? Get lost!", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"prisoner_slaughter", [(eq, "$talk_context", tc_troop_review_talk )], "One day you will pay!", "prisoner_slaughter_02",[]],

[anyone|auto_proceed,"prisoner_slaughter_02", [], "_", "close_window",[
	(call_script,"script_stand_back"),(display_message, "@Slaughter him for fresh human meat!",),
]],

[anyone,"prisoner_slaughter", [], "One day you will pay.... Aaa-ghgllr!...", "close_window",[
	(mission_cam_set_mode, 1, 1, 0),
	(play_sound,"snd_man_die"),
	(get_player_agent_no, reg1),
	(try_for_agents, ":agent"), # make a prisoner die in conversation window
		(neq, ":agent", reg1),
		(agent_is_human, ":agent"),
		(agent_get_troop_id, "$g_talk_troop", ":agent"), #apparently prisoner talk defines $g_talk_troop incorrectly. MB bug
		(neg|troop_is_hero, "$g_talk_troop"),
		(agent_set_animation, ":agent", "anim_fall_body_back"), 
		(agent_set_hit_points,":agent",0,0),
		
		(agent_deliver_damage_to_agent, reg1, ":agent"),
	(try_end),
	(party_remove_prisoners, "p_main_party", "$g_talk_troop", 1),
	(troop_add_item,"trp_player", "itm_human_meat",imod_fresh)]],

[anyone,"start", [(this_or_next|is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),
                    #(this_or_next|is_between,"$g_talk_troop",armor_merchants_begin, armor_merchants_end),
                    (             is_between,"$g_talk_troop",horse_merchants_begin, horse_merchants_end),
                    (eq, "$sneaked_into_town",1)],
"Away with you, vile beggar.", "close_window",[(call_script,"script_stand_back"),]],
                    
[anyone,"start", [(party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                    (this_or_next|is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),
                    #(this_or_next|is_between,"$g_talk_troop",armor_merchants_begin, armor_merchants_end),
                    (             is_between,"$g_talk_troop",horse_merchants_begin, horse_merchants_end)],
"Greetings, Commander. How can I serve you today?", "town_merchant_talk",[]],

[anyone,"start", [(this_or_next|is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),
                    #(this_or_next|is_between,"$g_talk_troop",armor_merchants_begin, armor_merchants_end),
                    (             is_between,"$g_talk_troop",horse_merchants_begin, horse_merchants_end)], 
"Good day. What can I do for you?", "town_merchant_talk",[]],

[anyone|plyr,"town_merchant_talk", [(is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),(call_script, "script_check_equipped_items", "trp_player")],
"I want to request new equipment. Show me what you have in your warehouse.", "trade_requested_weapons",[]],

[anyone|plyr,"town_merchant_talk", [(is_between,"$g_talk_troop",horse_merchants_begin,horse_merchants_end),(call_script, "script_check_equipped_items", "trp_player")],
"I am thinking of getting a mount.", "trade_requested_horse",[]],

[anyone,"trade_requested_weapons", [], "Ah, yes commander. These wares are the best you'll find anywhere.", "merchant_trade",[#(assign, "$equip_needs_checking", 1),
  (change_screen_trade)]],
[anyone,"trade_requested_horse", [], "You have a fine eye, Commander. You won't find better beasts than these anywhere else.", "merchant_trade",[#(assign, "$equip_needs_checking", 1),
                  (change_screen_trade)]],

[anyone,"merchant_trade", [], "Anything else?", "town_merchant_talk",[]],
[anyone|plyr,"town_merchant_talk", [], "Tell me. What are people talking about these days?", "merchant_gossip",[]],
[anyone,"merchant_gossip", [ (call_script,"script_tld_get_rumor_to_s61", "$g_talk_troop", "$current_town", "$g_talk_agent")],
"{s61}" , "town_merchant_talk",[]],
[anyone|plyr,"town_merchant_talk", [], "Good-bye.", "close_window",[(call_script,"script_stand_back"),]],




##[anyone,"start", [(eq, "$talk_context", 0),
##                    (is_between,"$g_talk_troop",walkers_begin, walkers_end),
##                    (eq, "$sneaked_into_town",1),
##                     ], "Stay away beggar!", "close_window",[]],
  
[anyone,"start", [(eq, "$talk_context", 0),
                    (agent_get_entry_no, ":entry", "$g_talk_agent"),
					(is_between,":entry",town_walker_entries_start, 40),
#					(is_between,"$g_talk_troop",walkers_begin, walkers_end),
                    (party_slot_eq, "$current_town", slot_town_lord, "trp_player")], 
"Excuse me?", "town_dweller_talk",[(assign, "$welfare_inquired",0),(assign, "$rumors_inquired",0),(assign, "$info_inquired",0)]],

[anyone,"start", [(eq, "$talk_context", 0),
                    (agent_get_entry_no, ":entry", "$g_talk_agent"),
					(is_between,":entry",town_walker_entries_start, 40)], 
"Good day, Commander.", "town_dweller_talk",[(assign, "$welfare_inquired", 0),(assign, "$rumors_inquired",0),(assign, "$info_inquired",0)]],

[anyone|plyr,"town_dweller_talk", [(check_quest_active, "qst_hunt_down_fugitive"),
                                     (neg|check_quest_concluded, "qst_hunt_down_fugitive"),
                                      (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
                                      (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
                                      (quest_get_slot, ":quest_object_troop", "qst_hunt_down_fugitive", slot_quest_object_troop),
                                      (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna", ":quest_object_troop"),
                                      (str_store_string, s4, s50),
                                      ],
"I am looking for a fugitive by the name of {s4}. I was told he may be hiding here.", "town_dweller_ask_fugitive",[]],

[anyone ,"town_dweller_ask_fugitive", [],"Strangers come and go to our town. If he is hiding here, you will surely find him if you look around.", "close_window",[(call_script,"script_stand_back"),]],


[anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_village),
                                     (eq, "$info_inquired", 0)], "What can you tell me about this village?", "town_dweller_ask_info",[(assign, "$info_inquired", 1)]],
[anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_town),
                                     (eq, "$info_inquired", 0)], "What can you tell me about this place?", "town_dweller_ask_info",[(assign, "$info_inquired", 1)]],

[anyone,"town_dweller_ask_info", [(str_store_party_name, s5, "$current_town"),
                                    (assign, reg4, 0),
                                    (try_begin),
                                      (party_slot_eq, "$current_town", slot_party_type, spt_town),
                                      (assign, reg4, 1),
                                    (try_end),
                                    (str_store_string, s6, "@This is {s5}, Commander."),
                                    (str_clear, s10),
                                    (try_begin),
                                      (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                                      (str_store_string, s10, "@{s6} This place and the surrounding lands belong to you of course, my {lord/lady}."),
                                    (else_try),
                                      (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
                                      (ge, ":town_lord", 0),
                                      (str_store_troop_name, s7, ":town_lord"),
                                      (store_troop_faction, ":town_lord_faction", ":town_lord"),
                                      (str_store_faction_name, s8, ":town_lord_faction"),
                                      (str_store_string, s10, "@{s6} This place and the surrounding lands belong to {s7} of {s8}."),
                                    (try_end),
                                    (str_clear, s5),
                                    (assign, reg20, 0),
                                    (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
                                      (store_sub, ":cur_good_slot", ":cur_good", trade_goods_begin),
                                      (val_add, ":cur_good_slot", slot_town_trade_good_productions_begin),
                                      (party_get_slot, ":production", "$g_encountered_party", ":cur_good_slot"),
                                      (ge, ":production", 10),
                                      (str_store_item_name, s3, ":cur_good"),
                                      (try_begin),
                                        (eq, reg20, 0),
                                        (str_store_string, s5, s3),
                                      (else_try),
                                        (eq, reg20, 1),
                                        (str_store_string, s5, "@{s3} and {s5}"),
                                      (else_try),
                                        (str_store_string, s5, "@{s3}, {s5}"),
                                      (try_end),
                                      (val_add, reg20, 1),
                                    (try_end),
                                    (str_store_string, s11, "@{reg20?We mostly produce {s5} here:We don't produce much here these days}.\
 If you would like to learn more, you can speak with our {reg4?guildmaster:village elder}. He is nearby, right over there."),],
"{s10}", "town_dweller_talk",[]], #was "{s10} {s11}"

[anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_village),
                                     (eq, "$welfare_inquired", 0)], 
"How is life here?", "town_dweller_ask_situation",[(assign, "$welfare_inquired", 1)]],
  #[anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_town),
                                     # (eq, "$welfare_inquired", 0)], "How is life here?", "town_dweller_ask_situation",[(assign, "$welfare_inquired", 1)]],


[anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
                                         (eq, ":walker_type", walkert_needs_money),
                                         (party_slot_eq, "$current_town", slot_party_type, spt_village)],
"Disaster has struck my family, {sir/madam}. A pestilence has ruined the crops on our fields, and my poor children lie at home hungry and sick.\
 My neighbours are too poor themselves to help me.", "town_dweller_poor",[]],

[anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
                                         (eq, ":walker_type", walkert_needs_money)],
"My life is miserable, {sir/madam}. I haven't been able to find a job for months, and my poor children go to bed hungry each night.\
 My neighbours are too poor themselves to help me.", "town_dweller_poor",[]],

[anyone|plyr,"town_dweller_poor", [(store_troop_gold, ":gold", "trp_player"),
                                     (ge, ":gold", 300),
                                     ],
"Then take these 300 denars. I hope this will help you and your family.", "town_dweller_poor_paid", [(troop_remove_gold, "trp_player", 300)]],

[anyone|plyr,"town_dweller_poor", [], "Then you must work harder and bear your burden without complaining.", "town_dweller_poor_not_paid",[]],
[anyone,"town_dweller_poor_not_paid", [], "Yes {sir/madam}. I will do as you say.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"town_dweller_poor_paid", [], "{My lord/My good lady}. \
 You are so good and generous. I will tell everyone how you helped us.", "close_window",
   [(call_script,"script_stand_back"),
    (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 1),
    (call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
    (assign, ":walker_no", reg2),
    (call_script, "script_center_set_walker_to_type", "$g_encountered_party", ":walker_no", walkert_needs_money_helped)]],

[anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         (assign, ":walker_type", reg0),
                                         (eq, ":walker_type", walkert_needs_money_helped)],
"Thank you for your kindness {sir/madam}. With your help our lives will be better. I will pray for you everyday.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"town_dweller_ask_situation", [(neg|party_slot_ge, "$current_town", slot_town_prosperity, 30)],
"Times are hard, {sir/madam}. We work hard all day and yet we go to sleep hungry most nights.", "town_dweller_talk",[]],
  
[anyone,"town_dweller_ask_situation", [(neg|party_slot_ge, "$current_town", slot_town_prosperity, 70)],
"Times are hard, {sir/madam}. But we must count our blessings.", "town_dweller_talk",[]],
[anyone,"town_dweller_ask_situation", [],
"We are not doing too badly {sir/madam}. We must count our blessings.", "town_dweller_talk",[]],

[anyone|plyr,"town_dweller_talk", [(eq, "$rumors_inquired", 0)], "What is the latest rumor around here?", "town_dweller_ask_rumor",[(assign, "$rumors_inquired", 1)]],
[anyone,"town_dweller_ask_rumor", [(neg|party_slot_ge, "$current_town", slot_center_player_relation, -5)], "I don't know anything that would be of interest to you.", "town_dweller_talk",[]],
  
  #[anyone,"town_dweller_ask_rumor", [(store_mul, ":rumor_id", "$current_town", 197),
                                     # (val_add,  ":rumor_id", "$g_talk_agent"),
                                     # (call_script, "script_get_rumor_to_s61", ":rumor_id"),
                                     # (gt, reg0, 0)], "{s61}", "town_dweller_talk",[]],

# TLD stuff                                     
[anyone,"town_dweller_ask_rumor", [(call_script, "script_tld_get_rumor_to_s61", "$g_talk_troop", "$current_town", "$g_talk_agent")],"{s61}" , "town_dweller_talk",[]],

  #[anyone,"town_dweller_ask_rumor", [], "I haven't heard anything interesting lately.", "town_dweller_talk",[]],
  
  # Brawls for evil sides
[anyone|plyr,"town_dweller_talk", [
    (neg|faction_slot_eq, "$g_encountered_party_faction", slot_faction_side, faction_side_good),
    (neg|troop_is_wounded, "trp_player"), # to prevent endless brawls
    (store_random_in_range, ":random", 0, 4),
    (try_begin),
      (eq, ":random", 0),
      (str_store_string, s4, "@Hey scum! I can fix that jaw of yours."),
    (else_try),
      (eq, ":random", 1),
      (str_store_string, s4, "@Watch where you're going, maggot!"),
    (else_try),
      (eq, ":random", 2),
      (str_store_string, s4, "@I don't like your face! I think it needs some fixing."),
    (else_try),
      (str_store_string, s4, "@What are you looking at? WHAT?"),
    (try_end)],
"{s4}", "town_dweller_brawl",[]],
[anyone,"town_dweller_brawl", [], "Are you threatening me? The guards hardly wait for your type to show up.", "town_dweller_brawl_confirm",[]],
[anyone|plyr,"town_dweller_brawl_confirm", [], "Oh really? Let's see what you've got.", "close_window", [
	(call_script,"script_stand_back"),
    (jump_to_menu, "mnu_auto_town_brawl"),
    (try_begin),
      (neg|party_slot_eq, "$current_town", slot_town_elder, "trp_no_troop"), #has to have a way to restore bad rels
      (call_script, "script_change_player_relation_with_center", "$current_town", -2),
    (try_end),
    (call_script, "script_increase_rank", "$g_encountered_party_faction", -1),
    (finish_mission)]],

[anyone|plyr,"town_dweller_brawl_confirm", [], "No, I thought you were someone else.", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"town_dweller_talk", [], "[Leave]", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (party_slot_eq,"$current_town",slot_town_lord, "trp_player")],
"Yes, Commander?", "player_castle_guard_talk",[]],
[anyone|plyr,"player_castle_guard_talk", [], "How goes the watch, soldier?", "player_castle_guard_talk_2",[]],
[anyone,"player_castle_guard_talk_2", [], "All is quiet Commander. Nothing to report.", "player_castle_guard_talk_3",[]],
[anyone|plyr,"player_castle_guard_talk_3", [], "Good. Keep your eyes open.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                    (eq, "$players_kingdom", "$g_encountered_party_faction"),
#                    (troop_slot_ge, "trp_player", slot_troop_renown, 100),
                    (str_store_party_name, s10, "$current_town")],
"Good day, Commander. It's good having you here in {s10}.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end)],
"Mind your manners around here and we'll have no trouble.", "close_window",[(call_script,"script_stand_back"),]],

# Easter Egg joke cutscene: available from MT castle guards on midnight
[anyone,"start", [(eq, "$talk_context", tc_court_talk),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (eq, "$g_encountered_party", "p_town_minas_tirith"),
                    (store_time_of_day, ":cur_time_of_day"),
                    (eq, ":cur_time_of_day", 0),],
"Ah, just past midnight. You know, an unusual incident happened recently - do you want to hear about it?", "hall_guard_easter_egg",[]],
[anyone|plyr,"hall_guard_easter_egg", [], "Yes, please go on.", "hall_guard_easter_egg_scene",[]],
[anyone|plyr,"hall_guard_easter_egg", [], "No, I don't care for gossip.", "close_window",[(call_script,"script_stand_back"),]],
[anyone,"hall_guard_easter_egg_scene", [], "Well.. an unusual group of adventurers appeared recently: a man, a dwarf and an elf, and then...", "close_window",[(call_script,"script_stand_back"),(jump_to_menu, "mnu_auto_intro_joke"),(finish_mission)]],

[anyone,"start", [(eq, "$talk_context", tc_court_talk),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end),
                    (party_slot_eq,"$current_town",slot_town_lord, "trp_player")],
"Your orders, Commander?", "hall_guard_talk",[]],

[anyone,"start", [(eq, "$talk_context", tc_court_talk),
                    (is_between,"$g_talk_troop",regular_troops_begin, regular_troops_end),
                    (is_between,"$g_encountered_party_faction",kingdoms_begin, kingdoms_end)],
"We are not supposed to talk while on guard, Commander.", "close_window",[(call_script,"script_stand_back"),]],
                     
[anyone|plyr,"hall_guard_talk", [], "Stay on duty and let me know if anyone comes to see me.", "hall_guard_duty",[]],
[anyone,"hall_guard_duty", [], "Yes, Commander. As you wish.", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"hall_guard_talk", [], "I want you to arrest this man immediately!", "hall_guard_arrest",[]],
[anyone,"hall_guard_arrest", [], "Who do you want arrested, Commander?", "hall_guard_arrest_2",[]],
[anyone|plyr,"hall_guard_arrest_2", [], "Ah, never mind my high spirits lads.", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"hall_guard_arrest_2", [], "Forget it. I will find another way to deal with this.", "close_window",[(call_script,"script_stand_back"),]],
[anyone,"enemy_defeated", [], "Arggh! I hate this.", "close_window",[(call_script,"script_stand_back"),]],
[anyone,"party_relieved", [], "Thank you for helping us against those bastards.", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"start", [(eq,"$talk_context", tc_party_encounter),(store_encountered_party, reg(5)),(party_get_template_id,reg(7),reg(5)),(eq,reg(7),"pt_sea_raiders")],
"I will drink from your skull!", "battle_reason_stated",[(play_sound,"snd_encounter_sea_raiders")]],
  
######################################
# GENERIC MEMBER CHAT
######################################

# CppCoder bugfix: Trolls go rawr...   
[anyone,"member_chat_00", [(troop_get_type, ":troll", "$g_talk_troop"),(eq, ":troll", tf_troll)], "^^GROWL!^^", "close_window",[]],

[anyone,"member_chat_00", [(troop_slot_eq,  "$g_talk_troop", slot_troop_upkeep_not_paid,0)], # or else, incipit is different
"Your orders, Commander?", "regular_member_talk",[]],

[anyone|plyr,"regular_member_talk", [], "Tell me about yourself", "view_regular_char_requested",[]],
[anyone,"view_regular_char_requested", [], "Yes, Commander. Let me tell you all there is to know about me.", "do_regular_member_view_char",[[change_screen_view_character]]],
[anyone,"do_regular_member_view_char", [], "Anything else?", "regular_member_talk",[]],

# TLD: can disband members for Res Point (mtarini)
  
[anyone,"member_chat_00", [
      (neg|troop_slot_eq, reg11, "$g_talk_troop", slot_troop_upkeep_not_paid,0), # if the troop wasn't paid last time, and it is on the leave
     (store_partner_faction, reg14),
    (str_store_faction_name, s14, reg14),
	(call_script, "script_get_troop_disband_cost", "$g_talk_troop",0,0),(assign, reg14, reg0),],
"It has been an honour to serve {s14} under your command, Commander.^^Now, as you know, I've been reassigned to home defense.^I shall soon leave."+promise_reg14_rp_of_s14, 
  "disband_regular_member_confirm_yn",[]],

[anyone|plyr,"regular_member_talk", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_upkeep_not_paid,0), # it was paid... still player can send him away
	(call_script, "script_cf_is_troop_in_party_not_wounded", "$g_talk_troop", "p_main_party"), # not wounded 
    (store_partner_faction, reg10),
    (is_between, reg10, kingdoms_begin, kingdoms_end), #no bandits
    (str_store_faction_name, s12, reg10)],
"Your services are now more urgent back home in {s12}, than here with me.", "disband_regular_member_confirm",[]],

[anyone|plyr,"regular_member_talk", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_upkeep_not_paid,0),  # it was paid... still player can send him away
	(call_script, "script_cf_is_troop_in_party_wounded", "$g_talk_troop", "p_main_party"),# wounded 
    (store_partner_faction, reg10),
    (is_between, reg10, kingdoms_begin, kingdoms_end), #no bandits
    (str_store_faction_name, s12, reg10)],
"You are wounded... you should go back home in {s12}, where you can be more useful than here.", "disband_regular_member_confirm",[]],

[anyone|plyr,"regular_member_talk", [], "Nothing. Keep moving.", "close_window",[(call_script,"script_stand_back"),]],
  
[anyone,"disband_regular_member_confirm", [
	(call_script, "script_get_troop_disband_cost", "$g_talk_troop",0,0),(assign, reg14, reg0),
    (store_partner_faction, reg10),(str_store_faction_name, s14, reg10)],
"Shall I leave your command, and go back home to defend my hometown?"+promise_reg14_rp_of_s14, "disband_regular_member_confirm_yn",[]],

[anyone|plyr,"disband_regular_member_confirm_yn", [(str_store_troop_name_plural, s15,"$g_talk_troop")],
"Yes, go there and await further orders from {s14}. Good luck, soldier!", "close_window",[
	(call_script,"script_stand_back"),
	(call_script, "script_get_troop_disband_cost", "$g_talk_troop",0,0),(assign, ":gain", reg0),
    #(party_remove_members_wounded_first,"p_main_party","$g_talk_troop",1),
	(remove_member_from_party,"$g_talk_troop"),
	(store_partner_faction, reg10),
	(call_script, "script_add_faction_rps", reg10, ":gain")]],

[anyone|plyr,"disband_regular_member_confirm_yn", [(troop_slot_eq, "$g_talk_troop", slot_troop_upkeep_not_paid,0)],
"Not yet, I still need you here.", "close_window",[(call_script,"script_stand_back"),]],

[anyone|plyr,"disband_regular_member_confirm_yn", [(neg|troop_slot_eq, "$g_talk_troop", slot_troop_upkeep_not_paid,0)],
"But you are still needed here, as well!", "disband_regular_member_insist",[ ]],

[anyone,"disband_regular_member_insist", [ ], "I know, but my duty brings me to different battles.^I will soon leave.", "close_window",[(call_script,"script_stand_back"),]],

# BEGIN ROUTED DIALOGS

[anyone, "start", [
			(eq, "$talk_context", tc_party_encounter),
                  	(eq, "$g_encountered_party_template", "pt_routed_allies"),
			(troop_get_type, ":race", "$g_talk_troop"),
			(neq, ":race", tf_troll),
			(assign, reg1, 0),
			(try_begin),
				(faction_slot_eq|this_or_next, "$g_encountered_party_faction", slot_faction_side, faction_side_good),
				(eq|this_or_next, ":race", tf_evil_man),
				(eq, ":race", tf_harad),			
				(assign, reg1, 1),
			(try_end),
		  ], 
		"{reg1?My lord:Master}, you have survived! Shall we join you again?", "routed_allies_talk", [] ],

[anyone|plyr, "routed_allies_talk", 
		[
			(eq, "$talk_context", tc_party_encounter),
                  	(eq, "$g_encountered_party_template", "pt_routed_allies"),
			(party_can_join_party,"$g_encountered_party","p_main_party"),
			(str_store_faction_name, s1, "$g_encountered_party_faction"),
			(try_begin),
				(eq, "$g_encountered_party_faction", "fac_isengard"),
				(str_store_string, s1, "@the white hand"),
			(else_try),
				(eq, "$g_encountered_party_faction", "fac_mordor"),
				(str_store_string, s1, "@the lidless eye"),
			(try_end),
		 ], 
		"Yes, together we shall fight for {s1} once again.", "close_window", 
		[
			(call_script, "script_party_add_party_companions", "p_main_party", "$g_encountered_party"),
			(call_script, "script_party_add_party_prisoners", "p_main_party", "$g_encountered_party"),
			(remove_party, "$g_encountered_party"),
			(assign, "$g_leave_encounter",1),			
		] 
],

[anyone|plyr, "routed_allies_talk", 
		[
			(eq, "$talk_context", tc_party_encounter),
                  	(eq, "$g_encountered_party_template", "pt_routed_allies"),
		 ], 
		"Not yet, soldier.", "close_window", [(assign, "$g_leave_encounter",1)] ],

# Trolls only, sort of a placeholder.

[anyone, "start", [
			(eq, "$talk_context", tc_party_encounter),
                  	(eq, "$g_encountered_party_template", "pt_routed_allies"),
			(troop_get_type, ":race", "$g_talk_troop"),
			(eq, ":race", tf_troll),
		  ], 
		"^^GROWL!^^", "routed_allies_talk_troll", [] ],

[anyone|plyr, "routed_allies_talk_troll", 
		[
			(eq, "$talk_context", tc_party_encounter),
                  	(eq, "$g_encountered_party_template", "pt_routed_allies"),
		 ], 
		"[Have them join you again]", "close_window", 
		[
			(call_script, "script_party_add_party_companions", "p_main_party", "$g_encountered_party"),
			(call_script, "script_party_add_party_prisoners", "p_main_party", "$g_encountered_party"),
			(remove_party, "$g_encountered_party"),
			(assign, "$g_leave_encounter",1)
		] ],

[anyone|plyr, "routed_allies_talk_troll", 
		[
			(eq, "$talk_context", tc_party_encounter),
                  	(eq, "$g_encountered_party_template", "pt_routed_allies"),
		 ], 
		"[Leave]", "close_window", [(assign, "$g_leave_encounter",1)] ],

# END ROUTED DIALOGS

#TLD: faction specific non-lord party encounter dialogs for friends and enemies
# (note: depends on lord dialogs coming before this; also bandits are not handled here)

#Friendly faction party: they don't trust you (rank 0 with them)
[anyone,"start", 
	[
		(eq,"$talk_context",tc_party_encounter),
		(eq,"$encountered_party_hostile",0),
		(is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end),
		(faction_slot_eq, "$g_encountered_party_faction", slot_faction_rank, 0),
	],
	"{s14}","party_encounter_distrusted_friend_1",
	[ 
		(call_script, "script_get_region_of_party", "$g_encountered_party"), (assign, ":encounter_region", reg1), 
		(faction_get_slot, ":encountered_side", "$g_encountered_party_faction", slot_faction_side),
		(call_script, "script_region_get_faction", ":encounter_region",  ":encountered_side"), (assign, ":encounter_faction", reg1), 
		(call_script, "script_str_store_distrusting_friend_dialog_in_s14_to_18", "$players_kingdom", "$g_encountered_party_faction",  ":encounter_faction"),
	]
],

[anyone|plyr, "party_encounter_distrusted_friend_1",  [], "{s15}",  "party_encounter_distrusted_friend_2a", [] ],

[anyone, "party_encounter_distrusted_friend_2a",  [], "{s16}",  "close_window", [ (call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)] ],

[anyone|plyr, "party_encounter_distrusted_friend_1",  [], "{s17}",  "party_encounter_distrusted_friend_2b", [] ],

[anyone, "party_encounter_distrusted_friend_2b",  [], "{s18}",  "close_window", [ (call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)] ],
		
# even with distrusted friends, you can hand troops of their faction
[anyone|plyr, "party_encounter_distrusted_friend_1",  
	[
		(call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
		(call_script, "script_party_split_by_faction", "p_main_party_backup", "p_temp_party", "$g_encountered_party_faction"),
		(party_get_num_companions,reg11,"p_main_party_backup"), (gt,reg11,1), # you have troop of their faction
		(try_begin),
			(faction_slot_eq, "$g_encountered_party_faction", slot_faction_side, faction_side_good),
			(str_store_string, s37, "@I have some of your people with me. I'll let them join you, to help your cause."),
		(else_try),
			(str_store_string, s37, "@Some of your stinky kin are with me. I'm sure they'd rather go with you."),
		(try_end),
	], 
	"{s37}",  "party_reinforce", [] ],

		

#Friendly faction party: they trust you.
[anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (eq,"$encountered_party_hostile",0),
                    (is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end)],
"{s4} What brings you here, {s24}?", "party_encounter_friend",
   [ # find the greeting
     (store_sub, ":greet_str", "$g_encountered_party_faction", kingdoms_begin),
     (val_mul, ":greet_str", 2),
     (val_add, ":greet_str", "str_party_greet_friend_gondor"),
     (str_store_string, s4, ":greet_str"),
     # add a note for home faction
     (try_begin),
       (eq, "$g_encountered_party_faction", "$players_kingdom"),
       (str_store_string, s4, "@{s4} It is always good to see one of our own."),
     (try_end),
     # find party home and target centers, if any
     (party_get_slot, ":home_center", "$g_encountered_party", slot_party_home_center),
     (try_begin),
       (gt, ":home_center", 0),
       (str_store_party_name, s11, ":home_center"),
     (else_try),
       (str_store_string, s11, "@a nearby town"), #defensive
     (try_end),
     (party_get_slot, ":target_center", "$g_encountered_party", slot_party_ai_object),
     (try_begin),
       (gt, ":target_center", 0),
       (str_store_party_name, s12, ":target_center"),
     (else_try),
       (str_store_string, s12, "@that town over there"), #defensive
     (try_end),
     # describe what the party is doing
     (try_begin),
       (eq, "$g_encountered_party_type", spt_scout),
       (str_store_string, s4, "@{s4}^We are from {s11}, scouting in the direction of {s12}."),
     (else_try),
       (eq, "$g_encountered_party_type", spt_raider),
       (assign, reg1, 0),
       (try_begin),
         (faction_slot_eq, "$g_encountered_party_faction", slot_faction_side, faction_side_good),
         (assign, reg1, 1),
       (try_end),
       (str_store_string, s4, "@{s4}^We are {reg1?foraging:raiding} around {s11}."),
     (else_try),
       (eq, "$g_encountered_party_type", spt_patrol),
       (str_store_string, s4, "@{s4}^We are patrolling around {s11}."),
     (else_try),
       (eq, "$g_encountered_party_type", spt_kingdom_caravan),
       (str_store_string, s4, "@{s4}^We are carrying supplies from {s11} to {s12}."),
     (else_try),
       (eq, "$g_encountered_party_type", spt_prisoner_train),
       (str_store_string, s4, "@{s4}^We are escorting prisoners to {s12}."),
     (try_end),
     (call_script, "script_get_rank_title_to_s24", "$g_encountered_party_faction" )]],

[anyone|plyr,"party_encounter_friend", [
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@Greetings, do you need reinforcements?"),
        (else_try),
          (str_store_string, s4, "@You don't look too strong, do you need troops?"),
        (try_end),        
        ],
"{s4}", "party_reinforce", [
   #init from TLD recruiting in city - modified
		# prepare strings useful in the folowing dialog
		(str_store_faction_name, s22, "$g_encountered_party_faction"), # s22: Party faction name
		(call_script, "script_get_rank_title_to_s24", "$players_kingdom" ),(str_store_string_reg, s29, s24), # s29: player rank title with own faction
		(call_script, "script_get_rank_title_to_s24", "$g_encountered_party_faction" ), # s24: player rank title with this faction
		(assign, reg26, 0),(try_begin),(eq,"$players_kingdom","$g_encountered_party_faction"),(assign,reg26,1),(try_end), # reg26: 1 if party of player faction
		(party_get_num_companions, reg27, "p_main_party"), # reg27: initial party size
		# just to see if someone can be given away: backup party, then see if troops which can be given away 
		(call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
		(call_script, "script_party_split_by_faction", "p_main_party_backup", "p_temp_party", "$g_encountered_party_faction")
		]],

[anyone|plyr,"party_encounter_friend", [
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@Goodbye, friends."),
        (else_try),
          (str_store_string, s4, "@See you later if you don't get killed."),
        (try_end)],
"{s4}", "close_window", [(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)]],

[anyone,"party_reinforce", [
     #War not started
     (eq,"$tld_war_began",0),],
"We haven't seen much enemy activity yet. Maybe later, thanks.", "party_reinforce_end", []],
[anyone,"party_reinforce", [
     #prevent some exploitation by placing caps on party size
     (assign, ":party_limit", 80),
     (try_begin),(eq, "$g_encountered_party_type", spt_scout          ),(assign, ":party_limit", 20),
      (else_try),(eq, "$g_encountered_party_type", spt_raider         ),(assign, ":party_limit", 50),
      (else_try),(eq, "$g_encountered_party_type", spt_patrol         ),(assign, ":party_limit", 80),
      (else_try),(eq, "$g_encountered_party_type", spt_kingdom_caravan),(assign, ":party_limit", 100),
      (else_try),(eq, "$g_encountered_party_type", spt_prisoner_train ),(assign, ":party_limit", 80),
     (try_end),
     (party_get_num_companions, ":party_size", "$g_encountered_party"),
     (ge, ":party_size", ":party_limit")],
"We don't need any more soldiers, thank you.", "party_reinforce_end", []],
#Reinforcement code from town garrison reinforcement, register init above
[anyone,"party_reinforce", [(party_get_num_companions,reg11,"p_main_party_backup"), (gt,reg11,1)],
	 "Reinforce our party? We can use a few more soldiers, but keep in mind we only accept troops of our faction.", 
	 "party_reinforce_check", [
        #GA: allowed player to transfer whatever troops in exchange screen. Unfitting ones will be returned to him later
		(party_clear, "p_main_party_backup"),
		(assign, "$g_move_heroes", 0),
        (call_script, "script_party_add_party_companions", "p_main_party_backup", "p_main_party"), #keep this backup for later
		(party_get_num_companions, reg28, "p_main_party"), # reg28: initial party size (after removing troops unfit to be given)
		(call_script, "script_get_party_disband_cost", "p_main_party",1),(assign, "$initial_party_value", reg0), # initial party total value (after removing troops ...)
        (change_screen_give_members)]],
[anyone,"party_reinforce", [], "Unfortunately you don't have any {s22} soldiers to reinforce us with.", "party_reinforce_end", []],

[anyone,"party_reinforce_check", [], "Let me check the soldier roster... ", "party_reinforce_check_1", []], 

[anyone,"party_reinforce_check_1", [ # only 1st condition needs party script
		#script restores main party, "p_main_party_backup" contains nonfaction troops returned to main party
		(call_script, "script_party_eject_nonfaction","$g_encountered_party", "p_main_party", "p_main_party_backup"),
		(party_get_num_companions, reg10, "p_main_party"),
		(party_get_num_companions, reg46, "p_main_party_backup"),
		#(display_message, "@TROOPS:{reg10} in main party, {reg46} nonfaction, {reg28} initially in main party"),
		(eq, reg46, 0),(eq, reg28, reg10)], # player didn't give anyone (party size unchanged)
"So you've changed your mind...^I see.", "party_reinforce_end", []],

[anyone,"party_reinforce_check_1", [(gt, reg46, 0),(eq, reg28, reg10)], # player gave only unfitting troops (party size unchanged)
"Those soldiers are of no use to us. ^Take them back.", "party_reinforce_end", []],

[anyone,"party_reinforce_check_1", 
	 [  (gt, reg28, reg10),# player gave fittings too (party size decreased)
	    (val_sub, reg28, reg10),(val_sub, reg28, 1), # calculate # of soldiers transferred -1
		(call_script, "script_get_party_disband_cost", "p_main_party", 1),(val_sub, "$initial_party_value", reg0), # calculate value transferred
		(str_store_faction_name, s14, "$g_encountered_party_faction"),
		(str_clear, s31), (str_clear, s32),
		(try_begin),(eq, reg26, 1),(str_store_string, s31, "@Thank you, commander.^"),
		 (else_try),               (str_store_string, s32, "@^{s14} is grateful to you, {playername}, {s29}^"),
		(try_end),
		(assign, reg14, "$initial_party_value"),
        (try_begin),(gt, reg46, 0),(str_store_string, s23, "@ ^Oh, and take back those who are not our people."), #if gave unfitting troops
		 (else_try),               (str_store_string, s23, "str_empty_string"),
		(try_end),
		(try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@{s31}{reg28?Those:That} brave {reg28?soldiers:soldier} will surely help us defend our lands.{s32} {s23}"+earned_reg14_rp_of_s14),
        (else_try),
          (str_store_string, s4, "@{s31}{reg28?Those:That} useful {reg28?troops:troop} will help us wreak more havoc.{s32}^{s23}"+earned_reg14_rp_of_s14),
        (try_end)],
"{s4}", "party_reinforce_check_2", [(call_script, "script_add_faction_rps", "$g_encountered_party_faction", "$initial_party_value")]],

[anyone|plyr,"party_reinforce_check_2", 
	[ (try_begin),(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
		                         (str_store_string, s31, "@I don't need them anyway, so save it."),
	   (else_try),(eq, reg26, 1),(str_store_string, s31, "@It is my duty to help our people."),
	   (else_try),               (str_store_string, s31, "@It is my duty to help our allies."),
	  (try_end)],
"{s31}", "party_reinforce_end", []],

[anyone,"party_reinforce_end", [
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@Good luck in your travels."),
        (else_try),
          (str_store_string, s4, "@Try not getting yourself killed."),
        (try_end)],
"{s4}", "close_window", [(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)]],


#Enemy faction party
# [anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    # (eq,"$encountered_party_hostile",1),
                    # (is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end)],
# "{s4}", "party_encounter_enemy",[
     # (store_sub, ":greet_str", "$g_encountered_party_faction", kingdoms_begin),
     # (val_mul, ":greet_str", 2),
     # (val_add, ":greet_str", "str_party_greet_enemy_gondor"),
     # (str_store_string, s4, ":greet_str"),
     # (try_begin),
       # (encountered_party_is_attacker),
       # (str_store_string, s4, "@{s4} Surrender or die!"),
     # (else_try),
       # (str_store_string, s4, "@{s4} Attack, and you will pay dearly!"),
     # (try_end)]],

# [anyone|plyr,"party_encounter_enemy", [(encountered_party_is_attacker)], "We will fight you to the end!", "close_window", []], #auto-attack
# [anyone|plyr,"party_encounter_enemy", [(encountered_party_is_attacker)], "Don't attack! We surrender.", "close_window", [(assign,"$g_player_surrenders",1)]],
# [anyone|plyr,"party_encounter_enemy", [(neg|encountered_party_is_attacker)], "Let's fight and see!", "close_window", [(encounter_attack)]],
# [anyone|plyr,"party_encounter_enemy", [(neg|encountered_party_is_attacker)], "Not this time. Begone.", "close_window", [(assign, "$g_leave_encounter",1)]],

[anyone,"start", [(eq, "$talk_context", tc_party_encounter),
                  (eq, "$g_encountered_party_template", "pt_gandalf"),
                  (eq, "$g_tld_gandalf_state", 0),], #not willing to talk
"You are making me late! Wizards are never late!", "close_window", [(assign, "$g_leave_encounter", 1)]],

[anyone,"start", [(eq, "$talk_context", tc_party_encounter),
                  (eq, "$g_encountered_party_template", "pt_nazgul"),
                  (eq, "$g_tld_nazgul_state", 0),], #not willing to talk
"It... beckonsssssss...", "close_window", [(assign, "$g_leave_encounter", 1)]],


######################################
# GENERIC PARTY ENCOUNTER
######################################

[anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (gt,"$encountered_party_hostile",0),
                    (encountered_party_is_attacker)],
"You have no chance against us. Surrender now or we will kill you all...", "party_encounter_hostile_attacker",
   [(try_begin),
      (eq,"$g_encountered_party_template","pt_steppe_bandits"),
      (play_sound, "snd_encounter_steppe_bandits"),
    (try_end)]],
	
[anyone|plyr,"party_encounter_hostile_attacker", [],"Don't attack! We surrender.", "close_window", [(call_script,"script_stand_back"),(assign,"$g_player_surrenders",1)]],
[anyone|plyr,"party_encounter_hostile_attacker", [],"We will fight you to the end!", "close_window", [(call_script,"script_stand_back"),]],
  
[anyone,"start", [(eq,"$talk_context",tc_party_encounter), (neg|encountered_party_is_attacker)],
"What do you want?", "party_encounter_hostile_defender",[]],

[anyone|plyr,"party_encounter_hostile_defender", [], "Surrender or die!", "party_encounter_hostile_ultimatum_surrender", []],

#post 0907 changes begin
[anyone,"party_encounter_hostile_ultimatum_surrender", [],
"{s43}", "close_window", [(call_script,"script_stand_back"),(call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_challenged_default")]],
#post 0907 changes end

# CppCoder: Reclaiming companions lost due to lack of RPs. This is a catch dialog.

[anyone,"start", [
			(is_between, "$g_talk_troop", companions_begin, companions_end),
                    	(troop_get_slot, ":intro", "$g_talk_troop", slot_troop_rehire_speech),
                    	(str_store_string, s5, ":intro"),
		], 
"{s5}", "companion_rehire",[]],



[anyone|plyr,"party_encounter_hostile_defender", [], "Nothing. We'll leave you in peace.", "close_window", [(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)]],
[trp_human_prisoner,"start", [], "* stares at you silently *", "close_window",[(agent_set_animation, "$current_player_agent", "anim_cancel_ani_stand")]],
[anyone,"start", [], "Surrender or die. Make your choice.", "battle_reason_stated",[]],
[anyone|plyr,"battle_reason_stated", [], "I am not afraid of you. I will fight.", "close_window",[(call_script,"script_stand_back"),(encounter_attack)]],
[anyone,"start", [], "Hello. What can I do for you?", "free",[]],
[anyone|plyr,"free", [(neg|in_meta_mission)], "Tell me about yourself", "view_char_requested",[]],
[anyone,"view_char_requested", [], "Very well, listen to this...", "view_char",[(change_screen_view_character)]],
[anyone,"view_char", [], "Anything else?", "free",[]],
[anyone|plyr,"end", [], "[Done]", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"start", [], "Drop your weapons and surrender if you want to live", "threaten_1",[]],
[anyone,"threaten_1", [], "We will fight you first", "end",[(encounter_attack)]],

#[anyone|plyr,"free", [[partner_is_mercmaster]], "I need to hire some mercenaries.", "mercenaries_requested",[]],
#[anyone,"mercenaries_requested", [], "I have the toughest fighters in all Calradia.", "buy_mercenaries",[[change_screen_buy_mercenaries]]],
#[anyone,"buy_mercenaries", [], "Anything else?", "free",[]],

#[anyone|plyr,"free", [[partner_is_recruitable]], "I need a capable sergeant like yourself. How much do you ask to work for me?", "employ_mercenary_requested",[]],
#[anyone,"employ_mercenary_requested", [[store_mercenary_price,0],[store_mercenary_wage,1]], "I want {reg0} denars now and {reg1} denars as monthly payment.", "employ_mercenary_2",[]],
#[anyone|plyr,"employ_mercenary_2", [], "I see I need to think of this.", "employ_mercenary_giveup",[]],
#[anyone|plyr,"employ_mercenary_2", [[neg|hero_can_join]], "I don't have any more room in my party right now. I will talk to you again later.", "employ_mercenary_giveup",[]],
#[anyone|plyr,"employ_mercenary_2", [[player_gold_ge,reg(0)],[hero_can_join]], "That's fine. Here's the {reg0} denars. From now on you work for me.", "employ_mercenary_commit",[[troop_remove_gold, "trp_player",reg(0)],[recruit_mercenary]]],
#[anyone,"employ_mercenary_giveup", [], "Suits me.", "free",[]],
#[anyone,"employ_mercenary_commit", [], "You got yourself the best fighter in the land.", "end",[]],


[anyone|plyr,"free", [[in_meta_mission]], " Good-bye.", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"free", [[neg|in_meta_mission]], " [Leave]", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"free", [], "NO MATCHING SENTENCE!", "close_window",[(call_script,"script_stand_back"),]],
[anyone,"start", [], "NO MATCHING SENTENCE!", "close_window",[(call_script,"script_stand_back"),]],

]
