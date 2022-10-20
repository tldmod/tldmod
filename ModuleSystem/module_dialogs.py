﻿# -*- coding: utf-8 -*-
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
from header_terrain_types import * #TLD

from module_constants import *
from module_info import wb_compile_switch as is_a_wb_dialog


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
                               (this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end),
                               (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
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
                               (this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end),
                               (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
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
      (str_store_string, s4, "@i wont a bonerlrord port nao!!11!"),
      (str_store_string, s5, "@Install TLD in your Bannerlord Modules folder, add the line 'compatible_with_wfas = 1' to module.ini, and you can play it both on Warband AND Warrider 0.202!"),
      (str_store_string, s6, "@Bannerlord runs on a different engine. We won't be able to port TLD to Bannerlord like we ported it to Warband."),
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
      (str_store_string, s4, "@Y NO ChINESE??"),
      (str_store_string, s5, "@Just to troll you, troll!"),
      (str_store_string, s6, "@Thanks to our volunteer translators, translations to Traditional and Simplified Chinese are available. But you need to follow our guide on Steam Workshop in order to use them."),
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
  
[trp_easter_egg_troll, "troll_beaten", [(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_continue")], "I bow to your wisdom, Master Baiter of Trolls!", "troll_talk_1",[]],
[trp_easter_egg_troll, "troll_goodbye", [(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_continue")], "TROLLOLOLOLOLOLOLOLOLOL!", "close_window",[(call_script,"script_stand_back"),]],
  
 
 #### HOBBITS CHATS... prelimintaries (mtarini)
 
 # phase 1: first time talk

[trp_merry_notmet, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 1),], "Hello again, {playername}!","hobbit_merry_talk_met",[] ],
[trp_pippin_notmet, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 1),], "Hello again, {playername}!","hobbit_pippin_talk_met",[] ],
 
[trp_merry_notmet, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),], "Hello, {sir/madam}! My name is Meriadoc Brandybuck but you can call me Merry!","hobbit_general_talk_1",[] ],
[trp_pippin_notmet, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_met_previously, 0),], "Hello, {sir/madam}! My name is Peregrin Took but you can call me Pippin!","hobbit_general_talk_1",[] ],

[anyone|plyr, "hobbit_general_talk_1", [], "I don't have time now.","close_window",[(call_script,"script_stand_back"), ], ],

[anyone|plyr, "hobbit_general_talk_1", [(troop_slot_eq, "trp_pippin_notmet", slot_troop_met_previously, 0),(troop_slot_eq, "trp_merry_notmet", slot_troop_met_previously, 0),], 
  "Say. I think I never seen one of your kind.","hobbit_general_talk_first_met",[(troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1),] ],

#Kham Hobbit Changes Begin

[anyone|plyr, "hobbit_general_talk_1", [
  (eq, "$g_talk_troop", "trp_pippin_notmet"), 
  (troop_slot_eq, "trp_merry_notmet", slot_troop_met_previously, 1)], 
    "Say. I think I've met another one like you, in Edoras.","hobbit_general_talk_second_met",[
      (troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1)] 
],


[anyone|plyr, "hobbit_general_talk_1", [
  (eq, "$g_talk_troop", "trp_merry_notmet"), 
  (troop_slot_eq, "trp_pippin_notmet", slot_troop_met_previously, 1)], 
    "Say. I think I've met another one like you, in Minas Tirith.","hobbit_general_talk_second_met",[
      (troop_set_slot, "$g_talk_troop", slot_troop_met_previously, 1),] 
  ],

[anyone,  "hobbit_general_talk_first_met", [], 
  "I know. I came from afar! I'm a Hobbit, {sir/madam}, from the Shire.","hobbit_general_talk_3",[] ],

[trp_merry_notmet,   "hobbit_general_talk_second_met", [], 
  "Oh, that must have been my dear cousin! Peregrin Took, or Pippin, how they call him. We are Hobbits, {sir/madam}, and we come from the Shire, both of us! Good old Pippin, I wonder how he is doing in Minas Tirith.","hobbit_general_talk_ask",[] ],

[trp_pippin_notmet,   "hobbit_general_talk_second_met", [], "Oh, that must have been my dear cousin! Meriadoc Brandybuck, or Merry, how they call him. We are Hobbits, {sir/madam}, and we come from the Shire, both of us! Good old Merry, I wonder how he is doing back in Edoras.","hobbit_general_talk_ask",[] ],

##Kham - Hobbit request START

[anyone,   "hobbit_general_talk_ask", [], 
  "May I ask a favour of you, {my lord/my lady}.","hobbit_general_talk_ask_1",[] ],

[anyone|plyr,   "hobbit_general_talk_ask_1", [
  (try_begin),
    (eq, "$g_talk_troop", "trp_merry_notmet"),
    (str_store_string, s1, "@Merry"),
  (else_try),
    (str_store_string, s1, "@Pippin"),
  (try_end)], 
    "Of course, {s1}. What is it?","hobbit_general_talk_ask_2",[] 
],

[anyone,   "hobbit_general_talk_ask_2", [
  (try_begin),
    (eq, "$g_talk_troop", "trp_merry_notmet"),
    (str_store_string, s1, "@Pippin"),
    (str_store_string, s2, "@the Citadel"),
    (str_store_string, s3, "@Minas Tirith"),
    (str_store_string, s4, "@Steward Denethor"),
  (else_try),
    (str_store_string, s1, "@Merry"),
    (str_store_string, s2, "@the Golden Hall"),
    (str_store_string, s3, "@Edoras"),
    (str_store_string, s4, "@King Theoden"),
  (try_end)],
    "Could you deliver a message to my cousin, {s1}? He is at {s2}, in {s3}, in the service of {s4}.","hobbit_general_talk_ask_3",[] 
],

[anyone|plyr,   "hobbit_general_talk_ask_3", [
  (try_begin),
    (eq, "$g_talk_troop", "trp_merry_notmet"),
    (str_store_string, s1, "@Minas Tirith"),
  (else_try),
    (str_store_string, s1, "@Edoras"),
  (try_end)], 
  "I will be passing by {s1} and will be glad to pass on this message to your cousin.","hobbit_general_talk_ask_accept",[
    (setup_quest_text, "qst_deliver_message_hobbit"),
    (try_begin),
      (eq, "$g_talk_troop", "trp_merry_notmet"),
      (str_store_string, s2, "@Merry asked you to deliver a message to his cousin, Pippin, in Minas Tirith."),
    (else_try),
      (str_store_string, s2, "@Pippin asked you to deliver a message to his cousin, Merry, in Edoras."),
    (try_end),
    (call_script, "script_start_quest", "qst_deliver_message_hobbit", "$g_talk_troop"),
    (try_begin),
      (eq, "$g_talk_troop", "trp_merry_notmet"),
      (quest_set_slot, "qst_deliver_message_hobbit", slot_quest_target_troop, "trp_pippin_notmet"),
    (else_try),
      (quest_set_slot, "qst_deliver_message_hobbit", slot_quest_target_troop, "trp_merry_notmet"),
    (try_end),] 
],

[anyone|plyr,   "hobbit_general_talk_ask_3", [
  (try_begin),
    (eq, "$g_talk_troop", "trp_merry_notmet"),
    (str_store_string, s1, "@Merry"),
  (else_try),
    (str_store_string, s1, "@Pippin"),
  (try_end)], 
    "I'm sorry, {s1}, but I do not have the time.","hobbit_general_talk_ask_reject",[] 

],


[anyone,   "hobbit_general_talk_ask_accept", [
  (store_random_in_range, ":random", 0, 3),
  (try_begin),
    (eq, "$g_talk_troop", "trp_merry_notmet"),
    (try_begin),
      (eq, ":random", 0),
      (str_store_string, s1, "@Tell him I've grown another inch!"),
    (else_try),
      (eq, ":random", 1),
      (str_store_string, s1, "@Tell Pip he smokes too much!"),
    (else_try),
      (str_store_string, s1, "@Tell him I can ride a grown horse now!"),
    (try_end),
  (else_try),
    (try_begin),
      (eq, ":random", 0),
      (str_store_string, s1, "@Ask him if he has any pipe-weed left!"),
    (else_try),
      (eq, ":random", 1),
      (str_store_string, s1, "@Tell him I'll be the tall one when we see each other again!"),
    (else_try),
      (eq, ":random", 2),
      (str_store_string, s1, "@Ask if he's seen Gandalf!"),
    (try_end),
  (try_end)], 
    "Thanks! {s1}","close_window",[(call_script, "script_stand_back")] 
],


[anyone,   "hobbit_general_talk_ask_reject", [
  (try_begin),
    (eq, "$g_talk_troop", "trp_merry_notmet"),
    (str_store_string, s1, "@Minas Tirith"),
  (else_try),
    (str_store_string, s1, "@Edoras"),
  (try_end)], 
    "I understand. I'll send it to the next caravan to {s1} then.","hobbit_general_talk_3",[] 

],

## Kham - Hobbit Request END

[anyone|plyr,  "hobbit_general_talk_3", [], "Well, goodbye now.","close_window",[  (call_script,"script_stand_back"), ] ],

# phase 2: any other time
[trp_merry, "start", [], "Welcome back, {playername}!","hobbit_merry_talk_met",[] ],
[trp_pippin, "start", [], "Welcome back, {playername}!","hobbit_pippin_talk_met",[] ],

##Kham - Hobbit Deliver Start

[anyone|plyr, "hobbit_merry_talk_met", [
  (check_quest_active, "qst_deliver_message_hobbit"),
  (quest_slot_eq, "qst_deliver_message_hobbit", slot_quest_target_troop, "trp_merry_notmet"),], 
    "Hello, messer Merry. I have a message here from your cousin, Pippin, in Minas Tirith.","hobbit_deliver_message",[]
],

[anyone|plyr, "hobbit_pippin_talk_met", [
  (check_quest_active, "qst_deliver_message_hobbit"),
  (quest_slot_eq, "qst_deliver_message_hobbit", slot_quest_target_troop, "trp_pippin_notmet"),], 
    "Hello, messer Pippin. I have a message here from your cousin, Merry, in Edoras.","hobbit_deliver_message",[]
],

[anyone, "hobbit_deliver_message", [], 
  "Thank you, {playername}. It was good of you to bring this to me.","close_window",[
    (agent_set_animation, "$current_player_agent", "anim_cancel_ani_stand"),
    (call_script, "script_finish_quest", "qst_deliver_message_hobbit", 100),
    (add_xp_as_reward, 250),
    (display_message, "@You gained 250 experience.", color_good_news),
    (try_begin),
      (eq, "$g_talk_troop", "trp_merry"),
      (call_script, "script_add_faction_rps", "fac_rohan", 250),
    (else_try),
      (call_script, "script_add_faction_rps", "fac_gondor", 250),
    (try_end)],
],

##Kham - Hobbit Deliver End
##Kham - Hobbit Changes END

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
[trp_treebeard, "treebeard_introduce_5", [], "(The stiff-limbed giant and his fellow Ents stand still for many minutes in silence while a breeze passes through their leafy hairs and beards. They look at each other for another prolonged moment until an unusually hasty Ent who is resembling a rowan tree seems to want to speak. However, he stays silent until the giant stiff-limbed Ent continues:)", "treebeard_questtalk",[]],
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
"(The stiff-limbed giant and his fellow Ents stand still in silence while a breeze passes through their leafy hairs and beards.)", "close_window",[(call_script,"script_stand_back"),]],
  
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

[anyone,"hostile_dialog", [(call_script, "script_encounter_agent_draw_weapon"),], "{s4}", "close_window",[(call_script,"script_stand_back"),]],

[anyone|plyr,"start", [ (eq,"$talk_context",tc_make_enemy_join_player),
            (str_store_item_name, s4, "itm_angmar_whip_reward")],
"Bow to the power of the {s4} and serve me!", "looters_2_join", []],

[anyone,"looters_2_join", [], "We will obey, Master.", "close_window", [
     (call_script,"script_stand_back"),
   (call_script, "script_party_add_party", "p_main_party", "$g_encountered_party"),
     (call_script, "script_safe_remove_party", "$g_encountered_party"),
   (change_screen_return),
     (assign, "$g_leave_encounter", 1)]],
  
#[party_tpl|pt_looters|plyr,"looters_2", [(store_character_level,reg1,"trp_player"),(lt,reg1,4)], 
#"I'm not afraid of you lot. Fight me if you dare!", "close_window", [(encounter_attack)]],
# [party_tpl|pt_looters|plyr,"looters_2", [], 
# "You'll have nothing of mine but cold steel, scum.", "close_window", [(call_script,"script_start_current_battle"),(encounter_attack)]],
#####################################################################
#TLD STUFFF
#####################################################################

[pt_wild_troll|party_tpl, "start", [(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_continue")], "^^GROWL!^^", "close_window",[] ],
[pt_raging_trolls|party_tpl, "start", [(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_continue")], "^^GROWL!^^", "close_window",[] ],


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
    (quest_get_slot, ":scout_leader", "qst_dispatch_scouts", slot_quest_object_troop), #also accept direct upgrade of the leader troop
    (troop_get_upgrade_troop, ":scout_leader_upgrade_1", ":scout_leader", 0),
    (troop_get_upgrade_troop, ":scout_leader_upgrade_2", ":scout_leader", 1),
    
    (this_or_next|eq, ":scout_leader", "$g_talk_troop"),
    (this_or_next|eq, ":scout_leader_upgrade_1", "$g_talk_troop"),
    (eq, ":scout_leader_upgrade_2", "$g_talk_troop"),
    # count if enough troops
    (quest_get_slot, ":quest_object_faction", "qst_dispatch_scouts", slot_quest_object_faction),
	(quest_get_slot, ":quest_target_amount", "qst_dispatch_scouts", slot_quest_target_amount),
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
  (ge, ":total_troops", ":quest_target_amount"),   
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
	(quest_get_slot, ":quest_target_amount", "qst_dispatch_scouts", slot_quest_target_amount),
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
  (assign,":scouts2fill", ":quest_target_amount"),  # pick troops for scout party, starting from lowest level
  (val_sub, ":scouts2fill", 1), #1 scout troop is already assigned
  (assign, ":num_tries", ":scouts2fill"),
  (try_for_range,":unused",0, ":num_tries"),
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
            (assign,":unused",":num_tries"),
        (assign,":n",":scouts2fill"),
        (try_end),
        (party_remove_members, "p_main_party", ":mintroop", ":n"),
        (party_add_members, ":scout_party", ":mintroop", ":n"),
        (val_sub,":scouts2fill",":n"),
    (else_try), (display_message,"@Something wrong, not enough troops for scout party"),
    (try_end),
    (try_end),
    (call_script, "script_party_calculate_strength", ":scout_party", 0),
    (assign, ":party_strength", reg0),
    (store_div, ":rank_reward_bonus", ":party_strength", 5),
	(assign, ":fac_str_bonus", ":rank_reward_bonus"),
    (quest_get_slot, ":rank_reward", "qst_dispatch_scouts", slot_quest_rank_reward),
    (quest_get_slot, ":fac_str_effect", "qst_dispatch_scouts", slot_quest_giver_fac_str_effect),
    (val_add, ":rank_reward", ":rank_reward_bonus"),
    (val_add, ":fac_str_effect", ":fac_str_bonus"),
    (quest_set_slot, "qst_dispatch_scouts", slot_quest_rank_reward, ":rank_reward"),
    (quest_set_slot, "qst_dispatch_scouts", slot_quest_giver_fac_str_effect, ":fac_str_effect"),
    
    (call_script, "script_succeed_quest", "qst_dispatch_scouts")]],

[anyone|plyr, "member_scout_1", [],  "Wait a minute, not just yet.", "close_window", [(call_script,"script_stand_back"),]],
[anyone,"do_member_trade", [], "Anything else?", "member_talk",[]],

[anyone,"member_chat_00", [(store_conversation_troop,"$g_talk_troop"),
                          (troop_is_hero,"$g_talk_troop"),
                          (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
                          (str_store_string, s5, ":honorific"),
                          (try_begin),
                            (eq, "$g_talk_troop", trp_npc21),
                            (store_conversation_agent, ":troll_agent"),
                            (agent_set_animation, ":troll_agent", "anim_troll_or_ent_bend_continue"),
                          (try_end),],
"Yes, {s5}?", "member_talk",[]],

[anyone|plyr,"member_talk", [(call_script, "script_unequip_items", "$g_talk_troop")],"Let me see your equipment.", "member_trade",[]],
[anyone,"member_trade",[      (store_character_level, ":talk_troop_level", "$g_talk_troop"),
            (ge, ":talk_troop_level", 30),
            (store_character_level, ":player_level", "trp_player"),
            (val_add, ":player_level", 10),
            (this_or_next|ge, ":talk_troop_level", ":player_level"), # if player level + 10 > npc level (e.g. 46 for Glorfindel), skip this
            (eq, "$g_talk_troop", "trp_npc21"), #also Berta
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

## Ziggy Convo Here after Ritual Success

[anyone|plyr,"member_talk", [(eq, "$g_talk_troop", "trp_npc20"),(troops_can_join, 1), (troop_slot_eq, "trp_npc20", slot_troop_wealth, 2)], 
  "Zigûrphel, I require another Wolf of you. Can you do this?", "ziggy_ask_more",
  []],

[anyone,"ziggy_ask_more", [(party_get_num_prisoners, ":num_prisoners", "p_main_party"), (lt, ":num_prisoners", 1),], 
  "You have no life to offer, Commander.", "close_window",
  [(change_screen_map)]],


[anyone,"ziggy_ask_more", [(store_current_hours, ":cur_hours"), (troop_get_slot, ":ziggy_rested", "trp_npc20", slot_troop_trainer_met), (lt, ":cur_hours", ":ziggy_rested")], 
  "Give me some more time, Commander. The ritual drained me.", "ziggy_not_rested",
  []],

[anyone,"ziggy_ask_more", [
  (party_get_num_prisoners, ":num_prisoners", "p_main_party"), (ge, ":num_prisoners", 1),
  (store_current_hours, ":cur_hours"), (troop_get_slot, ":ziggy_rested", "trp_npc20", slot_troop_trainer_met), (ge, ":cur_hours", ":ziggy_rested"),
  (party_get_num_companion_stacks,":stacks","p_main_party"),
  (assign, ":num_werewolves", 0),
  (try_for_range,":stack",0,":stacks"),
    (party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack"),
    (eq, ":troop_id", "trp_werewolf"),
    (party_stack_get_size, ":num_werewolves", "p_main_party", ":stack"),
  (try_end),
  (store_character_level, ":ziggy_level", "trp_npc20"),
  (store_sub, ":ziggy_wolves", ":ziggy_level", 14),
  (ge, ":num_werewolves", ":ziggy_wolves"),
  ],
  "I can only control so much. I'll need to become more powerful...", "close_window",
  [(change_screen_map)]],

[anyone,"ziggy_ask_more", [
  (party_get_num_prisoners, ":num_prisoners", "p_main_party"), (ge, ":num_prisoners", 1),
  (store_current_hours, ":cur_hours"), (troop_get_slot, ":ziggy_rested", "trp_npc20", slot_troop_trainer_met), (ge, ":cur_hours", ":ziggy_rested"),
  (party_get_num_companion_stacks,":stacks","p_main_party"),
  (assign, ":num_werewolves", 0),
  (try_for_range,":stack",0,":stacks"),
    (party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack"),
    (eq, ":troop_id", "trp_werewolf"),
    (party_stack_get_size, ":num_werewolves", "p_main_party", ":stack"),
  (try_end),
  (store_character_level, ":ziggy_level", "trp_npc20"),
  (store_sub, ":ziggy_wolves", ":ziggy_level", 14),
  (lt, ":num_werewolves", ":ziggy_wolves"),], 
  "Of course, Commander. Which one do you have to offer?", "ziggy_choose_prisoners",
  []],

[anyone|plyr,"ziggy_not_rested", [], 
  "Rest quick then, I need more of these.", "close_window",
  [(change_screen_map)]],



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
# (troop_get_slot, ":wound_mask", "$g_talk_troop", slot_troop_wound_mask),
# (try_begin),
#   (neq, ":wound_mask", 0),
#   (str_store_string, s12, "@I'm seriously injured. I need healing."),
# (else_try),
#   (str_store_string, s12, "@I don't have serious injuries, thank you."),
# (try_end)],
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

[anyone, "start", [(this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end), (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
                     (this_or_next|eq, "$talk_context", tc_court_talk), #TLD
                     (this_or_next|eq, "$talk_context", tc_town_talk), #TLD
                     (eq, "$talk_context", tc_tavern_talk),
                     (main_party_has_troop, "$g_talk_troop"),],
"Let's leave whenever you are ready.", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "start", [(this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end), (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_turned_down_twice, 1),],
"Please do not waste any more of my time today. Perhaps we shall meet again.", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "start", [(this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end), (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (eq, "$g_talk_troop_met", 0),
                     (troop_get_slot, ":intro", "$g_talk_troop", slot_troop_intro),
                     (str_store_string, 5, ":intro"),
                     (str_store_party_name, 20, "$g_encountered_party"),],
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
"{s7}", "close_window", [(call_script,"script_stand_back")]],

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
"Unfortunately, I can't take on any more hands in my party right now.", "close_window", [(call_script,"script_stand_back"),(try_begin),(eq, "$g_talk_troop", trp_npc21),(agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_rise"), (try_end),]],

[anyone|plyr, "companion_recruit_signup_response",[
                    (hero_can_join, "p_main_party"),
                    (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_1),
                    (str_store_string, 6, ":signup_response")],
"{s6}", "companion_recruit_rank", []],

[anyone|plyr, "companion_recruit_signup_response",[
                    (hero_can_join, "p_main_party"),
                     (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
                     (str_store_string, 7, ":signup_response")],
"{s7}", "close_window", [(call_script,"script_stand_back")]],

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
Let's speak again when you are more accomplished.", "close_window", [(call_script,"script_stand_back")]],

# rank ok
[anyone, "companion_recruit_rank", [],"I'm glad to see you have become {s29}, and I'm looking forward to joining you.", "companion_recruit_payment", []],
   
[anyone|auto_proceed, "companion_recruit_payment", [
      (troop_slot_eq, "$g_talk_troop", slot_troop_payment_request, 0)],
".", "companion_recruit_signup_confirm", []],
  
[anyone, "companion_recruit_payment", [
        (this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end),
        (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
        (try_begin),
            (is_between, "$g_talk_troop", companions_begin, companions_end),
            (store_sub, ":npc_offset", "$g_talk_troop", "trp_npc1"),
            (store_add, ":dialog_line", "str_npc1_payment", ":npc_offset"),
        (else_try),
            (store_sub, ":npc_offset", "$g_talk_troop", "trp_npc18"),
            (store_add, ":dialog_line", "str_npc18_payment", ":npc_offset"),
        (try_end),
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
          (try_begin),
            (is_between, "$g_talk_troop", companions_begin, companions_end),
            (store_sub, ":npc_offset", "$g_talk_troop", "trp_npc1"),
            (store_add, ":dialog_line", "str_npc1_payment_response", ":npc_offset"),
          (else_try),
            (store_sub, ":npc_offset", "$g_talk_troop", "trp_npc18"),
            (store_add, ":dialog_line", "str_npc18_payment_response", ":npc_offset"),
          (try_end),
          (str_store_string, s6, ":dialog_line")],
"{s6}", "companion_recruit_signup_confirm", [
                    (troop_get_slot, ":amount_requested", "$g_talk_troop", slot_troop_payment_request),#
                    (gt, ":amount_requested", 0),
          (call_script, "script_spend_influence_of", ":amount_requested", "$g_talk_troop_faction"),
                    (troop_set_slot, "$g_talk_troop", slot_troop_payment_request, 0)]],

[anyone|plyr, "companion_recruit_payment_response", [
                     (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
                     (str_store_string, s7, ":signup_response")],
"Well, there's little I can do then.", "close_window", [(call_script,"script_stand_back")]],

[anyone, "start", [(this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end), (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
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
"{s4}", "close_window", [(call_script,"script_stand_back")]],


[anyone, "start", [(this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end), (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
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
[anyone|plyr, "companion_recruit_secondchance", [],  "Never mind.", "close_window", [(call_script,"script_stand_back")]],

[anyone, "companion_recruit_backstory_delayed",
   [(troop_get_slot, ":backstory_delayed", "$g_talk_troop", slot_troop_backstory_delayed),
     (str_store_string, 5, ":backstory_delayed")],
"{s5}", "companion_recruit_backstory_delayed_response", []],

[anyone|plyr, "companion_recruit_backstory_delayed_response", [], "I might be able to use you in my company.", "companion_recruit_signup_b", []],
[anyone|plyr, "companion_recruit_backstory_delayed_response", [], "Never mind, another time perhaps.", "close_window", [(call_script,"script_stand_back")]],

[anyone, "companion_recruit_signup_confirm", [], "Good! Give me a few moments to prepare and I'll be ready to move.", "close_window",
   [(call_script,"script_stand_back"),
   (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
   (party_set_slot, "$current_town", slot_party_has_companion, 0),
   (try_begin),
    (eq, "$g_talk_troop", "trp_npc21"),
    (troop_add_item, "trp_npc21", "itm_troll_shield_a", imod_poor),
   (else_try),
    (eq, "$g_talk_troop", "trp_npc18"),
    (neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate), #First time
    (troop_remove_item, "trp_npc18","itm_feet_chains"),
    (troop_remove_item, "trp_npc18","itm_prisoner_coll_chain"),
    #(troop_add_item, "trp_npc18", "itm_khand_light"),
    (troop_add_item, "trp_npc18", "itm_javelin"),
    (troop_add_item, "trp_npc18", "itm_leather_boots"),
    (troop_add_item, "trp_npc18", "itm_khand_helm_mask"),
    (troop_add_item, "trp_npc18", "itm_khand_pitsword"),
    (troop_add_item, "trp_npc18", "itm_easterling_hawk_shield"),
    (troop_equip_items, "trp_npc18"),
  (try_end),]],



### Rehire dialogues
[anyone, "start", [(this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end), (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate)],
"My offer to rejoin you still stands, if you'll have me.", "companion_rehire", []],

### If the companion and the player were separated in battle
[anyone, "start", [(this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end), (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
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
[anyone, "start", [(this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end), (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_turned_down_twice, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_quit),
                     (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_rehire_speech),
                     (str_store_string, 5, ":speech")],
"{s5}", "companion_rehire", [(troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate)]],

###If the player and the companion parted on good terms
[anyone, "start", [(this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end), (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
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
[anyone, "companion_rehire_refused", [], "Well... Look me up if you change your mind, eh?", "close_window", [(call_script,"script_stand_back")]],

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

# Ziggy's Werewolf Convo First / Second Time

[anyone, "event_triggered", [
                     (eq, "$g_talk_troop", "trp_npc20"), #Ziggy
                     (eq, "$talk_context", tc_starting_quest),  
                     (troop_slot_eq, "trp_npc20", slot_troop_wealth, 0), #First time talk 
                     ],
  "Commander, a word. You have crushed our foes, and taken some prisoners - well and good. I have a mighty gift to offer you, if you would but grant me a small thing in exchange: give into my hands one of those we captured.", "ziggy_ask_prisoners", []],

[anyone, "event_triggered", [
                     (eq, "$g_talk_troop", "trp_npc20"), #Ziggy
                     (eq, "$talk_context", tc_starting_quest),  
                     (troop_slot_eq, "trp_npc20", slot_troop_wealth, 1), #Second time talk 
                     ],
  "Commander, congratulations on your triumph. If you remember what I told you the last time, I have a use for one of these captives. It will be to your benefit, Commander, I assure you.", "ziggy_ask_prisoners", []],

[anyone|plyr, "ziggy_ask_prisoners", [],
  "Enough of your mysteries, Zigûrphel! Speak plainly! What do you want a prisoner for?", "ziggy_ask_why", []],

[anyone, "ziggy_ask_why", [],
  "Patience, patience, Commander! Only indulge me in this trifling matter, and I will show you a marvel.", "ziggy_reason", []],

[anyone|plyr, "ziggy_reason", [],
  "You intrigue me. Very well. I will leave one of the captives to your... tender care.", "ziggy_yes", []],


[anyone|plyr, "ziggy_reason", [],
  "Not at this time, Zigûrphel. Go back to your post.", "ziggy_no", []],

[anyone, "ziggy_no", [(troop_slot_eq, "trp_npc20", slot_troop_wealth, 0)],
  "Very well, Commander, but you would be a fool to forego my gift.", "close_window", [(troop_set_slot, "trp_npc20", slot_troop_wealth, 1),(change_screen_map)]],

[anyone, "ziggy_no", [(troop_slot_ge, "trp_npc20", slot_troop_wealth, 1)],
  "Very well, Commander.", "close_window", [(change_screen_map)]],

[anyone, "ziggy_yes", [],
  "Excellent. Which of these specimens would you give?", "ziggy_choose_prisoners", []],

[anyone|plyr|repeat_for_1000, "ziggy_choose_prisoners", 
  [   (party_get_num_prisoner_stacks, ":num_prisoners", "p_main_party"),
      (ge, ":num_prisoners", 1),
      (store_repeat_object, ":prisoners"),
      #(val_add, ":prisoners", soldiers_begin),
      (is_between, ":prisoners", soldiers_begin, soldiers_end),
      (neg|is_between, ":prisoners", kingdom_heroes_begin, kingdom_heroes_end),
      (party_count_prisoners_of_type, ":prisoner_type", "p_main_party", ":prisoners"),
      (gt, ":prisoner_type", 0),
      (str_store_troop_name, s1, ":prisoners"),
  ],
  
  "{s1}", "ziggy_chosen_prisoner", 
  [(store_repeat_object, "$temp"),
   ]],

[anyone|plyr, "ziggy_choose_prisoners", 
  [],
  "I have none I want to offer.", "ziggy_no", 
  [(troop_set_slot, "trp_npc20", slot_troop_wealth, 2)]],

[anyone, "ziggy_chosen_prisoner", [(neg|troop_slot_eq, "trp_npc20", slot_troop_wealth, 2)],
  "Thank you, Commander! A moment... ah yes, this one should do nicely... Agannūlo burudan kinum! Kadō nakh, îdô ugru-dalad dâira!", "ziggy_ritual", 
  [(store_character_level, ":ziggy_level", "trp_npc20"),
   (store_character_level, ":prisoner_level", "$temp"),
   (store_mul, ":chance", ":ziggy_level", 2),
   (val_add, ":chance", ":prisoner_level"),
   (val_min, ":chance", 100),
   (assign, "$temp2", 0),
   (store_random_in_range, ":random", 0, 100),
   (try_begin),
    (le,":random", ":chance"),
    (assign, "$temp2", 1),
   (else_try),
    (assign, "$temp2", 0),
   (try_end)]],

[anyone, "ziggy_chosen_prisoner", [(troop_slot_eq, "trp_npc20", slot_troop_wealth, 2)],
  " What have we here? Proud, defiant? Fearful, as you should be? Now shall I give you a reason for fear, indeed! Agannūlo burudan kinum! Kadō nakh, îdô ugru-dalad dâira!", "ziggy_ritual", 
  [(store_character_level, ":ziggy_level", "trp_npc20"),
   (store_character_level, ":prisoner_level", "$temp"),
   (store_mul, ":chance", ":ziggy_level", 2),
   (val_add, ":chance", ":prisoner_level"),
   (val_min, ":chance", 100),
   (assign, "$temp2", 0),
   (store_random_in_range, ":random", 0, 100),
   (try_begin),
    (le,":random", ":chance"),
    (assign, "$temp2", 1),
   (else_try),
    (assign, "$temp2", 0),
   (try_end)]],

[anyone, "ziggy_ritual", [(troop_slot_eq, "trp_npc20", slot_troop_wealth, 0), (eq, "$temp2", 1),],
  "Oh yes... yes! Behold, Commander! Gaze upon what I, Zigûrphel, have achieved! Know you of the wolves of Angband? Of Draugluin, or of mighty Carcharoth who slew Huan the Hound of Valinor? Just as the Dark Lord could twist and trap a captive spirit into a vessel fit for his purposes, I too have bound a lesser spirit and yoked it to us as a great beast of shadow! This one is not as great as Draugluin's first brood, of course, nothing like, but it will serve.", "ziggy_ritual_succeed", 
  [(str_store_troop_name, s24, "$temp"),
   (party_remove_prisoners, "p_main_party", "$temp", 1),
   (troop_set_slot, "trp_npc20", slot_troop_wealth, 2),
   (party_force_add_members, "p_main_party", "trp_werewolf", 1),
   (store_character_level, ":ziggy_level", "trp_npc20"),
   (store_character_level, ":prisoner_level", "$temp"),
   (store_mul, ":xp_reward", ":ziggy_level",":ziggy_level"),
   (val_mul, ":xp_reward", ":prisoner_level"),
   (val_div, ":xp_reward", 10), #tweakable
   (add_xp_to_troop, ":xp_reward", "trp_npc20"),
   (assign, reg78, ":xp_reward"),
   (display_message, "@Zigûrphel gained {reg78} experience."),   
   ]],

[anyone, "ziggy_ritual", [(troop_slot_ge, "trp_npc20", slot_troop_wealth, 2), (eq, "$temp2", 1),],
  "Always such a joy to bring a foe properly to heel.", "ziggy_ritual_succeed", 
  [(party_remove_prisoners, "p_main_party", "$temp", 1),
   (party_add_members, "p_main_party", "trp_werewolf", 1),
   (store_character_level, ":ziggy_level", "trp_npc20"),
   (store_character_level, ":prisoner_level", "$temp"),
   (store_mul, ":xp_reward", ":ziggy_level",":ziggy_level"),
   (val_mul, ":xp_reward", ":prisoner_level"),
   (val_div, ":xp_reward", 10), #tweakable
   (add_xp_to_troop, ":xp_reward", "trp_npc20"),
   (assign, reg78, ":xp_reward"),
   (display_message, "@Zigûrphel gained {reg78} experience."), 
   ]],

[anyone, "ziggy_ritual", [(eq, "$temp2", 0),],
  "Ach! This one was too weak! Worthless! Give me a stronger one, Commander, one who will not fail!", "ziggy_choose_prisoners", 
  [(party_remove_prisoners, "p_main_party", "$temp", 1),]],

[anyone, "ziggy_ritual_succeed", [],
  "And of course, allow me but a little rest; then you may pass another captive into my care. I will do the rest.", "close_window", 
  [(store_current_hours, ":cur_hours"),
   (val_add, ":cur_hours", 24), #add one day
   (troop_set_slot, "trp_npc20", slot_troop_trainer_met, ":cur_hours"), #use this slot to check if Ziggy can provide more wolves
   (change_screen_map)]],


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
                     (str_store_string, 5, ":speech"),
                     (try_begin),
                        (eq, "$g_talk_troop", trp_npc21),
                        (store_conversation_agent, ":troll_agent"),
                        (agent_set_animation, ":troll_agent", "anim_troll_or_ent_bend_continue"),
                     (try_end),],
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
                     (str_store_string, 5, ":speech"),
                     (try_begin),
                        (eq, "$g_talk_troop", trp_npc21),
                        (store_conversation_agent, ":troll_agent"),
                        (agent_set_animation, ":troll_agent", "anim_troll_or_ent_bend_continue"),
                     (try_end),],
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
                     (str_store_string, 5, ":speech"),
                     (try_begin),
                        (eq, "$g_talk_troop", trp_npc21),
                        (store_conversation_agent, ":troll_agent"),
                        (agent_set_animation, ":troll_agent", "anim_troll_or_ent_bend_continue"),
                     (try_end),],
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
                     (str_store_string, 5, ":speech"),
                     (try_begin),
                        (eq, "$g_talk_troop", trp_npc21),
                        (store_conversation_agent, ":troll_agent"),
                        (agent_set_animation, ":troll_agent", "anim_troll_or_ent_bend_continue"),
                     (try_end),],
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
                     (try_end),
                     (try_begin),
                        (eq, "$g_talk_troop", trp_npc21),
                        (store_conversation_agent, ":troll_agent"),
                        (agent_set_animation, ":troll_agent", "anim_troll_or_ent_bend_continue"),
                     (try_end),],
"{s5}, {reg6?our:my} {s6} homeland is suffering grievously in the War, I ask you to consider helping {reg6?our:my} people as soon as we are rested and ready.", "companion_faction_demolished", []],

[anyone|plyr, "companion_faction_demolished", [],  "Then we shall ride to aid {s6} immediately.", "close_window", [(call_script,"script_stand_back"),]],
[anyone|plyr, "companion_faction_demolished", [],  "I'm sorry, but we are needed elsewhere.", "close_window", [(call_script,"script_stand_back"),]],

[anyone, "event_triggered", [
                     (eq, "$npc_map_talk_context", slot_troop_home), 
                     (store_conversation_troop, "$map_talk_troop"),
                     (troop_get_slot, ":speech", "$map_talk_troop", slot_troop_home_intro),
                     (str_store_string, s5, ":speech"),
                     (try_begin),
                        (eq, "$g_talk_troop", trp_npc21),
                        (store_conversation_agent, ":troll_agent"),
                        (agent_set_animation, ":troll_agent", "anim_troll_or_ent_bend_continue"),
                     (try_end),],
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
   [(agent_get_entry_no, ":entry", "$g_talk_agent"),
    (this_or_next|eq,":entry",24),(eq, "$talk_context", tc_hire_troops), 
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
    (else_try), (ge, ":rank", 4), (str_store_string, s33, "@Greetings, {s23}, {s24}."),  # player not same faction, but trusted
    (else_try), (ge, ":rank", 1), (str_store_string, s33, "@Greetings, {s23}."), # player not much trusted
    (else_try), (str_store_string, s33, "@So, you are {s23}. I hear you fight for our {s25} friends, so I guess I should consider you an ally."), # player unknown
    (try_end),

    #TLD Kham - If troll, bend.
    (try_begin),
      (troop_get_type, ":is_troll", "$g_talk_troop"),
      (eq, ":is_troll", tf_troll),
      (agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_continue"),
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
  [ (assign, ":continue",0),
    (try_begin),
      (is_between, "$g_encountered_party", "p_advcamp_gondor", "p_centers_end"),
      (store_faction_of_party, ":fac_adv", "$g_encountered_party"),
      (eq, ":fac_adv", "$players_kingdom"),
      (assign, ":continue", 1),
    (try_end),

    (this_or_next | faction_slot_eq, "$players_kingdom", slot_faction_capital, "$g_encountered_party"), #Capitols ...
    (               eq, ":continue", 1),  # or adv camp only.
  
   # keep troops only at faction's capital or adv camps

   (try_begin),
    (faction_slot_eq, "$players_kingdom", slot_faction_capital, "$g_encountered_party"),
    (troop_get_slot, ":reserve_party", "trp_player", slot_troop_player_reserve_party),
   (else_try),
    (is_between, "$g_encountered_party", "p_advcamp_gondor", "p_centers_end"),
    (troop_get_slot, ":reserve_party", "trp_player", slot_troop_player_reserve_adv_camp),
   (try_end),
  
  # check if first time or depleted, and initialize
      
    (try_begin),
      (gt, ":reserve_party", 0),
      (neg|party_is_active, ":reserve_party"), # depleted
      (assign, ":reserve_party", 0),
    (try_end),
      
      (try_begin),
    (eq, ":reserve_party", 0), #first time or depleted
        (spawn_around_party, "$g_encountered_party", "pt_volunteers"),
        (assign, ":reserve_party", reg0),
        (party_add_members, ":reserve_party", "trp_looter", 1), #.. or change_screen_exchange_with_party will crash
        (party_remove_members, ":reserve_party", "trp_looter", 1),
        
        (try_begin),
          (is_between, "$g_encountered_party", "p_advcamp_gondor", "p_centers_end"),
          (troop_set_slot, "trp_player", slot_troop_player_reserve_adv_camp, ":reserve_party"),
        (else_try),
          (troop_set_slot, "trp_player", slot_troop_player_reserve_party, ":reserve_party"),
        (try_end),
        
        (party_attach_to_party, ":reserve_party", "$g_encountered_party"),
        (party_set_name, ":reserve_party", "@{playername}'s Reserves"),
        (party_set_flags, ":reserve_party", pf_no_label),
        (party_set_ai_behavior, ":reserve_party", ai_bhvr_hold),
      (try_end)], 
"I want to review my soldiers stationed here.", "close_window", [
    (call_script,"script_stand_back"),
      #(change_screen_exchange_members, 0,":reserve_party"), # doesn't work without changing context...
      (jump_to_menu, "mnu_auto_player_garrison"), #...therefore, hackery ensues
  ]],

# TLD Kham - Player Hire Troll

[anyone|plyr,"player_hire_troop", 
  [
   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_troll_troop, -1),
   (try_begin),
    (eq, "$g_encountered_party", "p_town_dol_guldur"),
    (assign, "$g_talk_troop_faction", "fac_guldur"),
   (try_end),
  ], 
  "I am a commander worthy of a fighting Troll - give me one!", "player_hire_trolls_take", []],

[anyone,"player_hire_trolls_take", 
  [
   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_troll_troop, -1),
   (party_get_free_companions_capacity,reg10,"p_main_party"), (le,reg10,0),
  ], 
  "Looking to raise your own Black Legion, are you? Come back when you can add a full-grown Troll to your ranks.", "close_window", [(call_script, "script_stand_back")]],

[anyone,"player_hire_trolls_take", 
  [
   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_troll_troop, -1),
   (party_get_free_companions_capacity,reg10,"p_main_party"), (gt,reg10,0),
   (call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (assign, ":rank", reg0), #rank points to rank number 0-9
   (call_script, "script_get_rank_title_to_s24", "$g_talk_troop_faction"), 
   (str_store_string_reg, s25, s24), #to s25 (current rank)
   (call_script, "script_get_any_rank_title_to_s24", "$g_talk_troop_faction", 4), #to s24
   (le, ":rank", 3),], 
  "You? You lowly maggot. Get out of my sight. Fighting Troll, indeed. (You need to be {s24} or higher)", "close_window", [(call_script, "script_stand_back")]],


[anyone,"player_hire_trolls_take", 
  
  [
   (faction_get_slot, ":fac_troll",  "$g_talk_troop_faction", slot_faction_troll_troop),
   (gt, ":fac_troll", 0),
   (party_get_free_companions_capacity,reg10,"p_main_party"), (gt,reg10,0),
   (call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (assign, ":rank", reg0), #rank points to rank number 0-9
   (gt, ":rank", 3),
   (store_character_level, ":troll_level", ":fac_troll"),
   (val_sub, ":troll_level", 30),
   (val_mul, ":troll_level", 2), #Inf. Cost
   (assign, reg21, ":troll_level"),
  ], 
  "It will cost {reg21} influence.", "player_hire_trolls_how_many", []],


[anyone|plyr,"player_hire_trolls_take", 
  [], 
  "I’ve changed my mind.", "close_window", [(call_script, "script_stand_back")]],

[anyone|plyr,"player_hire_trolls_how_many", 
  [ 
    (faction_get_slot, reg20, "$g_talk_troop_faction", slot_faction_influence),
    (ge, reg20, reg21), #reg21 is inf cost
  ], 
  "A fearsome beast. And now, it is mine!", "player_hire_troll_buy_done", []],

[anyone|plyr,"player_hire_trolls_how_many", 
  [], 
  "They will fight better with sheets of iron protecting them. Make it so!", "player_hire_troll_armoured", []],

[anyone,"player_hire_troll_armoured", 
  [
    (try_begin),
      (eq, "$g_talk_troop_faction", "fac_gundabad"),
      (str_store_string, s55, "@Maybe the weaklings of the south put armour on their soft-skinned Trolls. Not us - our Trolls are of Gundabad!"),
    (else_try),
      (str_store_string, s55, "@Do I look like a smith to you? Pah. Go talk to one."),
    (try_end),
  ], 
  "{s55}", "player_hire_trolls_how_many", []],

[anyone|plyr,"player_hire_trolls_how_many", 
  [], 
  "I’ve changed my mind.", "player_hire_troll_buy_not_enough", []],

[anyone,"player_hire_troll_buy_not_enough", 
  [], 
  "Wasting my time...", "close_window", [(call_script, "script_stand_back"),]],

[anyone,"player_hire_troll_buy_done", 
  [], 
  "Take good care of this big fellow now, and he’ll take good care of you! Ha!", "close_window", 
  [
    (faction_get_slot, ":fac_troll",  "$g_talk_troop_faction", slot_faction_troll_troop),
    (call_script, "script_spend_influence_of", reg21, "$g_talk_troop_faction"),
    (party_add_members, "p_main_party", ":fac_troll", 1),
    (call_script, "script_stand_back"),
  ]],

# TLD Kham - Player Hire Troll END



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

# Selling all prisoners 
[anyone|plyr, "player_hire_troop", [(store_num_regular_prisoners,reg5),(ge,reg5,1)],
"I want you to take all the prisoners I have with me.", "tld_sell_prisoners_all", [
    #this could be moved to a script if it's used anywhere else
    (assign, ":total_income", 0),
    (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
    (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":troop_no", "p_main_party", ":i_stack"),
        #Won't come up much in TLD but is possible if on the capture a commander quest
        (call_script, "script_game_check_prisoner_can_be_sold", ":troop_no"),
        (eq, reg0, 1),
        (party_prisoner_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
        (call_script, "script_game_get_prisoner_price", ":troop_no"),
        (assign, ":sell_price", reg0),
        (store_mul, ":stack_total_price", ":sell_price", ":stack_size"),
        (val_add, ":total_income", ":stack_total_price"),
        (party_remove_prisoners, "p_main_party", ":troop_no", ":stack_size"),
    (try_end),
    (call_script, "script_add_faction_rps", "$g_talk_troop_faction", ":total_income"),
]],
[anyone, "tld_sell_prisoners_all", [], "Very well, I'll take them all to our dungeons.", "player_hire_troop_nextcycle",[]],

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

"{s4}", "player_hire_troop_reunite",

#swy-- workaround a bug where the player would get stuck in the conversation menu with the barracks guy after donating some troops to his camp.
#   -- because the player insists on upgrading his troops inside the give_members screen, the before/after count doesn't match and none of the following dialog options kick. Boom, stuck.
#   -- what i've made is to make impossible for the player to upgrade his troops in here by returning a crazy amount of points/money in "script_game_get_upgrade_cost", so the button stays disabled.
#   -- more info: http://mbx.streetofeyes.com/index.php/topic,3465.msg68239.html#msg68239

  (is_a_wb_dialog
   and
  [
   (assign, "$tld_forbid_troop_upgrade_mode", 1),
   (change_screen_give_members),
  ]
   or
  [
   (change_screen_give_members)
  ])
  
# disabled in the next dialog -> player_hire_troop_reunite (already loaded when the give_members is accessed) -> player_hire_troop_nextcycle

],

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

##Kham - Reinforce Center Quest Troop Count HERE
[anyone,"player_hire_troop_reunite_1",  
   [
    (gt, reg28, reg0),# player gave fittings too (party size decreased)
    (val_sub, reg28, reg0),
    (assign, ":troops_given", reg28), #Kham - For Reinforce Quest
    (val_sub, reg28, 1), #calculate how many troops given (minus 1)
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
        (try_end),

    #Kham - Reinforce Center Troop Count    
    (try_begin),
      (check_quest_active, "qst_blank_quest_16"),
      (quest_get_slot, ":target_center", "qst_blank_quest_16", slot_quest_target_center),
      (eq, "$g_encountered_party", ":target_center"),
      (str_store_party_name, s8, ":target_center"),
      (quest_get_slot, ":amount", "qst_blank_quest_16", slot_quest_target_amount),
      (quest_get_slot, ":current", "qst_blank_quest_16", slot_quest_current_state),
      (try_begin),
        (lt, ":current", ":amount"), #This means that the player has given some troops already.
        (assign, ":amount", ":current"),
      (try_end),
      (try_begin),
        (eq, ":troops_given", ":amount"),
        (call_script, "script_succeed_quest", "qst_blank_quest_16"),
        (quest_set_slot, "qst_blank_quest_16", slot_quest_current_state, 0),
      (else_try),
        (lt, ":troops_given", ":amount"),
        (val_sub, ":amount", ":troops_given"),
        (quest_set_slot, "qst_blank_quest_16", slot_quest_current_state, ":amount"),
      (else_try),
        (gt, ":troops_given", ":amount"),
        (val_sub, ":amount", ":troops_given"),
        (call_script, "script_succeed_quest", "qst_blank_quest_16"),
        (quest_set_slot, "qst_blank_quest_16", slot_quest_current_state, ":amount"),
      (try_end),
      
      (quest_get_slot, ":donated", "qst_blank_quest_16", slot_quest_current_state),
      (quest_get_slot, ":orig_amount", "qst_blank_quest_16", slot_quest_target_amount),
      (store_sub, reg55, ":orig_amount", ":donated"),
      (str_store_string, s5, "@You have reinforced {s8} with {reg55} troops."),
      (add_quest_note_from_sreg, "qst_blank_quest_16", 3, s5, 0),
    (try_end),],
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
    ] + (is_a_wb_dialog and [(assign,"$tld_forbid_troop_upgrade_mode",0)] or []) ],

    




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
  [(quest_get_slot,":quest_object_troop", "qst_lend_surgeon", slot_quest_object_troop),
  (store_attribute_level, ":int", ":quest_object_troop", ca_intelligence),
  (val_mul, ":int",":int"),
  (assign, ":reward_xp", 500),
  (val_mul, ":reward_xp",":int"),
  (val_div, ":reward_xp", 300),
  (add_xp_to_troop, ":reward_xp", ":quest_object_troop"),
  (str_store_troop_name,s3,":quest_object_troop"),
  (assign, reg78, ":reward_xp"),
  (display_message, "@ {s3} gained {reg78} experience."),
  
  (call_script, "script_finish_quest", "qst_lend_surgeon", 100),
  (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]],

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
   
[anyone|plyr, "lord_active_mission_2", [(party_count_prisoners_of_type, ":num_trolls", "p_main_party", "trp_wild_troll"),
                    (ge, ":num_trolls", 2), 
                    (store_partner_quest,":lords_quest"),(eq,":lords_quest","qst_capture_troll"),], 
"Master, I hereby give you not one, but a pair of beasts!","lord_capture_troll_completed_two_trolls",[]],

[anyone|plyr, "lord_active_mission_2", [(party_count_prisoners_of_type, ":num_trolls", "p_main_party", "trp_wild_troll"),
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
    (party_remove_prisoners, "p_main_party", "trp_wild_troll", 2)]],

[anyone|plyr, "lord_capture_troll_completed_two_trolls_thankyou",[(troops_can_join, 1),],
"Can a savage beast be made to obey commands?","lord_capture_troll_completed_two_trolls_thankyou_info",[]],

[anyone|plyr, "lord_capture_troll_completed_two_trolls_thankyou",[(troops_can_join, 1),],
"Thank you, Master. You will be pleased by the way this troll will be put in good use.","lord_capture_troll_completed_two_trolls_thankyou_accept",[]],

[anyone|plyr, "lord_capture_troll_completed_two_trolls_thankyou",[(troops_can_join, 1),],
"Thank you, master. But I'm not worth of your great gift. It is too dangerous for me.","lord_capture_troll_completed_two_trolls_thankyou_refuse",[]],

[anyone|plyr, "lord_capture_troll_completed_two_trolls_thankyou",[(troops_can_join|neg, 1),],
"Thank you, master. But I'm not worth of your great gift. [no room in party!]","lord_capture_troll_completed_two_trolls_thankyou_refuse",[]],

# [anyone|plyr, "lord_capture_troll_completed_two_trolls_thankyou",[(faction_get_slot, reg20, "$g_talk_troop_faction", slot_faction_influence)],
# "Master, I will bring greater havoc if you also provide an armour for the beast [10/{reg20} influence].","lord_capture_troll_completed_two_trolls_thankyou_raise",[]],

[anyone, "lord_capture_troll_completed_two_trolls_thankyou_info",[],
"Are you questioning the abilities of your Master, {playername}? This beast is trained to attack enemies on sight. This is enough. But, you and your warriors keep at due distance from the beast when it fights, and never stand between it and its victims.","lord_capture_troll_completed_two_trolls_thankyou",[]],

[anyone, "lord_capture_troll_completed_two_trolls_thankyou_accept",[],
"Now bring havoc to my enemies with your new gift","lord_pretalk", 
	[(faction_get_slot, ":troll",  "$g_talk_troop_faction", slot_faction_troll_troop),(party_add_members, "p_main_party", ":troll", 1)]],

[anyone, "lord_capture_troll_completed_two_trolls_thankyou_refuse",[],
"As you wish, then. Someone else among of my servants will known how to use this mighty tool of war.","lord_pretalk",[]],

# [anyone, "lord_capture_troll_completed_two_trolls_thankyou_raise",[(faction_slot_ge, "$g_talk_troop_faction", slot_faction_influence, 10)],
# "You dare ask for an fully armoured battle troll, {playername}, to keep under your command? That's not a small thing to ask for. But you are a skilled servant, and we know your motivations. We like that. It shall be granted.","lord_pretalk",
  # [(party_add_members, "p_main_party", "trp_isen_armored_troll", 1),
   # (call_script, "script_spend_influence_of", 10, "$g_talk_troop_faction"),]],

# [anyone, "lord_capture_troll_completed_two_trolls_thankyou_raise",[(neg|faction_slot_ge, "$g_talk_troop_faction", slot_faction_influence, 10)],
# "How dare you ask Us for more than We have planned for you in our great Wisdom? {playername}, you proved a mighty Servant today, but don't let your insolence test Our patience any further.","lord_capture_troll_completed_two_trolls_thankyou",[]],

[anyone, "lord_capture_troll_completed_one_troll",[],
"Excellent, {playername}. You are a most faithful and useful servant. This troll will be most useful for our purposes. That it is taken to the dungeons!", "close_window",[
  (call_script,"script_stand_back"),
  (call_script, "script_finish_quest", "qst_capture_troll", 100),
      (call_script, "script_change_player_relation_with_troop","$g_talk_troop",5),
  (troop_remove_item,"trp_player","itm_wheeled_cage"), # Take his cage back
  (party_remove_prisoners, "p_main_party", "trp_wild_troll", 1)]],
  
[anyone,"lord_start", [(store_partner_quest,":lords_quest"),
                         (eq,":lords_quest","qst_capture_troll"),
                         (check_quest_failed, "qst_capture_troll")],
"Too long ago, I asked you to take me one troll alive. But I should have known. \
How could I expect someone like {playername} to be up to the challenge. My servant was not skilled or faithful enough.", "close_window",[
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



#### Kham Destroy Scout Camp Quests Completion Start ####

[anyone,"lord_start", [
    (check_quest_active, "qst_destroy_scout_camp"),    
    (check_quest_succeeded, "qst_destroy_scout_camp"),
    (quest_get_slot, ":giver_troop", "qst_destroy_scout_camp", slot_quest_giver_troop),
    (eq, "$g_talk_troop", ":giver_troop"),
    (quest_get_slot, ":quest_target_center", "qst_destroy_scout_camp", slot_quest_target_center),
    (str_store_party_name,12,":quest_target_center")],
"Our scouts near {s12} have told us about your success. This will teach them from spying on us.^^The destruction of this camp will surely halt our enemies' advance.", "lord_generic_mission_completed",[

    (call_script,"script_destroy_scout_camp_consequences",1),
    (call_script, "script_finish_quest", "qst_destroy_scout_camp", 100),
    ]],

[anyone,"lord_start", [
    (check_quest_active, "qst_destroy_scout_camp"),
    (check_quest_failed, "qst_destroy_scout_camp"),
    (quest_get_slot, ":giver_troop", "qst_destroy_scout_camp", slot_quest_giver_troop),
    (eq, "$g_talk_troop", ":giver_troop"),
    (quest_get_slot, ":quest_target_center", "qst_destroy_scout_camp", slot_quest_target_center),
    (str_store_party_name,s12,":quest_target_center")],
"Our scouts near {s12}'s camp saw you and your men retreat. This is disappointing, {playername}. ^^Your failure resulted in the attack of vital supply lines. It will take some time to recover.", "destroy_scout_camp_failed",[
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -2),
  
    (call_script,"script_destroy_scout_camp_consequences",0),
    (cancel_quest, "qst_destroy_scout_camp"),
    ]],

[anyone|plyr, "destroy_scout_camp_failed",[],
  "I will do better next time.", "close_window",[],
  ],


#### Kham Destroy Scout Camp Quests Completion End ####

#### Kham Defend / Raid Village Quests Completion Start ####

[anyone,"lord_start", [
    (check_quest_active, "qst_defend_village"),
    (check_quest_succeeded, "qst_defend_village"),
    (quest_slot_eq, "qst_defend_village", slot_quest_giver_troop,"$g_talk_troop"),
    (quest_get_slot, ":quest_target_center", "qst_defend_village", slot_quest_object_center),
    (str_store_party_name,12,":quest_target_center")],
"We have heard from our scouts near {s12} that you have valiantly defended the village. These raiders are becoming bolder every day... ^^We sense that war is surely coming. Thank you once more, {playername}.", "lord_generic_mission_completed",[
    (call_script, "script_finish_quest", "qst_defend_village", 100),
    ]],

[anyone,"lord_start", [
    (check_quest_active, "qst_defend_village"),
    (check_quest_failed, "qst_defend_village"),
    (quest_slot_eq, "qst_defend_village", slot_quest_giver_troop,"$g_talk_troop"),
    (quest_get_slot, ":quest_target_center", "qst_defend_village", slot_quest_object_center),
    (str_store_party_name,12,":quest_target_center")],
"We have heard from our scouts near {s12} that you have failed to defend the village. The villagers were either slaughtered or made into slaves. These raiders are becoming bolder every day... ^^We sense that war is surely coming.", "defend_village_failed",[
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (cancel_quest, "qst_defend_village"),
    ]],

[anyone|plyr, "defend_village_failed",[],
  "I will do better next time.", "close_window",[],
  ],


[anyone,"lord_start", [
    (check_quest_active, "qst_raid_village"),    
    (check_quest_succeeded, "qst_raid_village"),
    (quest_get_slot, ":giver_troop", "qst_raid_village", slot_quest_giver_troop),
    (eq, "$g_talk_troop", ":giver_troop"),
    (quest_get_slot, ":quest_target_center", "qst_raid_village", slot_quest_object_center),
    (str_store_party_name,12,":quest_target_center")],
"We saw the flames coming from the village near {s12}. We heard the screams. This is only the beginning, {playername}. ^^War is coming.", "lord_generic_mission_completed",[
    (call_script, "script_finish_quest", "qst_raid_village", 100),
    ]],

[anyone,"lord_start", [
    (check_quest_active, "qst_raid_village"),
    (check_quest_failed, "qst_raid_village"),
    (quest_get_slot, ":giver_troop", "qst_raid_village", slot_quest_giver_troop),
    (eq, "$g_talk_troop", ":giver_troop"),
    (quest_get_slot, ":quest_target_center", "qst_raid_village", slot_quest_object_center),
    (str_store_party_name,12,":quest_target_center")],
"We saw some of your men running away from the village near {s12}. You dare come back here and show your face, {playername}?. ^^There will be war, but with failures like this, you may be its first casualty.", "raid_village_failed",[
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (cancel_quest, "qst_raid_village"),
    ]],

[anyone|plyr, "raid_village_failed",[],
  "I will do better next time.", "close_window",[],
  ],


#### Kham Defend / Raid  Village Quests Completion End ####

#### Kham Defeat Lord Completion Start ####

[anyone,"lord_start", [
    (check_quest_active, "qst_blank_quest_06"),
    (quest_slot_eq, "qst_blank_quest_06", slot_quest_object_troop,"$g_talk_troop"),
    (check_quest_succeeded, "qst_blank_quest_06"),
    (quest_slot_eq, "qst_blank_quest_06", slot_quest_object_troop,"$g_talk_troop"),
    (quest_get_slot, ":quest_target_troop", "qst_blank_quest_06", slot_quest_target_troop),
    (str_store_troop_name, s7, ":quest_target_troop"),
    (str_store_faction_name, s8, ":quest_target_troop"),
    (try_begin),
      (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
      (str_store_string, s5, "@{playername}, our scouts brought word of your success. May you live beyond this day in years of blessedness! With the hosts of {s7} thrown back by your victory, the enemy’s great advance has faltered. We may hope that there is now contention within their ranks, and among their captains. And, too, we may hope that they now hold a healthy fear of you! You have won us a brief rest from weariness, at the least."),
    (else_try),
      (str_store_string, s5, "@Well, {playername}, you’ve returned, and with good news for us, it would seem. I see now you are not only made of brag and hot air - ah, if only I could have seen {s7} fall before you with my own eyes! Our foes are now desperately disheartened, no doubt. Lost their heads, I warrant. Cut off the head of a serpent, as they say, and the deal’s done. Well, I must now lead my host to win the real victory. Your contribution will be reported, {playername}, to your betters. Have no fear about that."),
    (try_end),
    ],
"{s5}", "lord_defeat_lord_complete",[
    (call_script, "script_finish_quest", "qst_blank_quest_06", 100),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5),
    ]],

[anyone|plyr,"lord_defeat_lord_complete", [
    (quest_get_slot, ":quest_target_troop", "qst_blank_quest_06", slot_quest_target_troop),
    (str_store_troop_name, s7, ":quest_target_troop"),
    (str_store_faction_name, s8, ":quest_target_troop"),
    (try_begin),
      (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
      (str_store_string, s5, "@Alas that I could not bring a final end to {s7} of {s8}, but if we should meet again, let them beware."),
    (else_try),
      (str_store_string, s5, "@ I should rather make report of my victory over {s7} of {s8} myself - the chief glory is mine, and you will not forget it!"),
    (try_end),],
"{s5}", "close_window",[
    (call_script, "script_finish_quest", "qst_blank_quest_06", 100),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 8),
    ]],


[anyone,"lord_start", [
    (check_quest_active, "qst_blank_quest_06"),
    (quest_slot_eq, "qst_blank_quest_06", slot_quest_object_troop,"$g_talk_troop"),
    (check_quest_failed, "qst_blank_quest_06"),
    (quest_slot_eq, "qst_blank_quest_06", slot_quest_object_troop,"$g_talk_troop"),],
"I have heard that you failed to do what I asked you to. Disappointing, {playername}.", "lord_target_lord_failed",[
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -2),
    (cancel_quest, "qst_blank_quest_06"),
    ]],

[anyone|plyr, "lord_target_lord_failed",[],
  "I will do better next time.", "close_window",[],
  ],

#### Kham Kill Quests Completion Start ####

[anyone,"lord_start", [
    (check_quest_active, "qst_blank_quest_04"),
    (quest_slot_eq, "qst_blank_quest_04", slot_quest_object_troop,"$g_talk_troop"),
    (check_quest_succeeded, "qst_blank_quest_04"),
    (quest_slot_eq, "qst_blank_quest_04", slot_quest_object_troop,"$g_talk_troop"),
    ],
"Your men have witnessed your bravery in battle, {playername}. You have shown them that we are the superior force.", "lord_generic_mission_completed",[
    (call_script, "script_finish_quest", "qst_blank_quest_04", 100),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5),
    ]],

[anyone,"lord_start", [
    (check_quest_active, "qst_blank_quest_04"),
    (quest_slot_eq, "qst_blank_quest_04", slot_quest_object_troop,"$g_talk_troop"),
    (check_quest_failed, "qst_blank_quest_04"),
    (quest_slot_eq, "qst_blank_quest_04", slot_quest_object_troop,"$g_talk_troop"),],
"I have heard that you failed to do what I asked you to. Disappointing, {playername}.", "kill_quest_failed",[
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (cancel_quest, "qst_blank_quest_04"),
    ]],


[anyone,"lord_start", [
    (check_quest_active, "qst_blank_quest_05"),
    (quest_slot_eq, "qst_blank_quest_05", slot_quest_object_troop,"$g_talk_troop"),
    (check_quest_succeeded, "qst_blank_quest_05"),
    (quest_slot_eq, "qst_blank_quest_05", slot_quest_object_troop,"$g_talk_troop"),
    ],
"Your men have witnessed your bravery in battle, {playername}. You have earned my respect.", "lord_generic_mission_completed",[
    (call_script, "script_finish_quest", "qst_blank_quest_05", 100),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
    ]],

[anyone,"lord_start", [
    (check_quest_active, "qst_blank_quest_05"),
    (quest_slot_eq, "qst_blank_quest_05", slot_quest_object_troop,"$g_talk_troop"),
    (check_quest_failed, "qst_blank_quest_05"),
    (quest_slot_eq, "qst_blank_quest_05", slot_quest_object_troop,"$g_talk_troop"),],
"I have heard that you failed to do what I asked you to. Disappointing, {playername}.", "kill_quest_failed",[
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (cancel_quest, "qst_blank_quest_05"),
    ]],

[anyone|plyr, "kill_quest_failed",[],
  "I will do better next time.", "close_window",[],
  ],
#### Kham Kill Quests Completion END ####

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

## Defend Refugees Completion Dialogues - Kham

[anyone,"lord_start", [(check_quest_active,"qst_blank_quest_01"),
                       (check_quest_succeeded, "qst_blank_quest_01"),
                       (quest_get_slot, ":quest_giver", "qst_blank_quest_01", slot_quest_giver_troop),
                       (eq, ":quest_giver", "$g_talk_troop"),],
"I have received reports that all refugees were safely escorted. We thank you {playername} for your help. In this war, it is the innocent that suffer the most.", "lord_generic_mission_completed",
   [(call_script, "script_finish_quest", "qst_blank_quest_01", 100),
    (assign, reg18, "$qst_raider_party_defeated"),
    (call_script, "script_cf_get_random_enemy_center_in_theater","p_main_party"),
    (store_faction_of_party, ":faction", reg0),
    (str_store_faction_name, s1, ":faction"),
    (faction_get_slot,":enemy_strength",":faction",slot_faction_strength_tmp),
    (store_mul, ":reduction", 15, reg18), #15 victory points per raider party killed
    (assign, reg19, ":reduction"),
    (val_sub, ":enemy_strength", ":reduction"),
    (display_message, "@Foiling the enemy's attempts at attacking the refugee trains have weakened their resolve ({s1} has lost {reg19} faction strength due to your victory against {reg18} raiders).", color_good_news),
    (faction_set_slot,":faction",slot_faction_strength_tmp,":enemy_strength"), ]],

[anyone,"lord_start", [ (check_quest_active,"qst_blank_quest_01"),
                        (check_quest_failed, "qst_blank_quest_01"),
                        (quest_get_slot, ":quest_giver", "qst_blank_quest_01", slot_quest_giver_troop),
                        (eq, ":quest_giver", "$g_talk_troop"),],
"{playername}, I have received reports that the refugees were intercepted by raiders and were all slaughtered. This is very disappointing...", "lord_defend_refugees_failed", []],

[anyone|plyr,"lord_defend_refugees_failed", [(str_store_troop_name, s65, "$g_talk_troop")],
   "Forgive me, {s65}, I was unable to defend them.", "lord_defend_refugees_failed_1a", []],

[anyone,"lord_defend_refugees_failed_1a", [],
"It is the innocent that suffer the most in wars. There might be more refugee trains in the future, {playername}. I hope you are more prepared next time.", "lord_pretalk",
   [(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-1),
    (call_script, "script_end_quest", "qst_blank_quest_01"),
    (assign, reg18, "$qst_raider_party_defeated"),
    (call_script, "script_cf_get_random_enemy_center_in_theater", "p_main_party"),
    (store_faction_of_party, ":faction", reg0),
    (str_store_faction_name, s1, ":faction"),
    (faction_get_slot, ":enemy_strength", ":faction", slot_faction_strength_tmp),
    (store_mul, ":reduction", 15, reg18), #15 victory points per raider party killed
    (assign, reg19, ":reduction"),
    (val_sub, ":enemy_strength", ":reduction"),
    (val_add, ":enemy_strength", 50), #50 victory points for the enemy
    (display_message, "@The slaughter and looting of the refugee train has strengthened the enemy ({s1} has gained 50 faction strength).", color_bad_news),
    (display_message, "@You did, however, defeat {reg18} raiders, weakening the enemy's resolve ({s1} has lost {reg19} faction strength).", color_good_news),
    (faction_set_slot, ":faction", slot_faction_strength_tmp, ":enemy_strength"), ]],

[anyone,"lord_start", [(check_quest_active,"qst_blank_quest_01"),
                       (check_quest_concluded, "qst_blank_quest_01"),
                       (quest_get_slot, ":quest_giver", "qst_blank_quest_01", slot_quest_giver_troop),
                       (eq, ":quest_giver", "$g_talk_troop"),
                       (assign, reg17, "$qst_refugees_escaped")],
"I have received reports that only {reg17} refugee trains reached their destination. This is unfortunate, but that is the cost of war. There might be more refugee trains in the future, {playername}. I hope you are more prepared next time.", "lord_defend_refugees_half_completed",
   [(store_mul, ":completion", "$qst_refugees_escaped", 100),
    (val_div, ":completion", 3),
    (call_script, "script_finish_quest", "qst_blank_quest_01", ":completion"),
    (assign, reg18, "$qst_raider_party_defeated"),
    (call_script, "script_cf_get_random_enemy_center_in_theater", "p_main_party"),
    (store_faction_of_party, ":faction", reg0),
    (str_store_faction_name, s1, ":faction"),
    (faction_get_slot, ":enemy_strength", ":faction", slot_faction_strength_tmp),
    (store_mul, ":reduction", 15, reg18), #15 victory points per raider party killed
    (assign, reg19, ":reduction"),
    (val_sub, ":enemy_strength", ":reduction"),
    (store_sub, ":num_killed", 3, "$qst_refugees_escaped"),
    (val_mul, ":num_killed", 15), #Number of refugees killed x 15 = VP for enemy
    (assign, reg20, ":num_killed"),
    (val_add, ":enemy_strength", ":num_killed"), 
    (display_message, "@The slaughter and looting of the refugee train has strengthened the enemy ({s1} has gained {reg20} faction strength).", color_bad_news),
    (display_message, "@You did, however, defeat {reg18} raiders, weakening the enemy's resolve ({s1} has lost {reg19} faction strength).", color_good_news),
    (faction_set_slot, ":faction", slot_faction_strength_tmp, ":enemy_strength"), ]],

[anyone|plyr,"lord_defend_refugees_half_completed", [], "I will be more prepared next time, my lord. ", "lord_pretalk", []],

## Defend Refugees Completion Dialogues END - Kham

## Hunt Down Refugees Completion Dialogues - Kham

[anyone,"lord_start", [(check_quest_active,"qst_blank_quest_02"),
                       (check_quest_succeeded, "qst_blank_quest_02"),
                       (quest_get_slot, ":quest_giver", "qst_blank_quest_02", slot_quest_giver_troop),
                       (eq, ":quest_giver", "$g_talk_troop")],
"I have received reports that the refugees were all killed, and that prisoner trains will be coming soon... You did well, {playername}. This is only the beginning, we shall rule over this land soon enough.", "lord_generic_mission_completed",
   [(call_script, "script_finish_quest", "qst_blank_quest_02", 100),
    (call_script, "script_cf_get_random_enemy_center_in_theater","p_main_party"),
    (store_faction_of_party, ":faction", reg0),
    (str_store_faction_name, s1, ":faction"),
    (faction_get_slot,":enemy_strength",":faction",slot_faction_strength_tmp),
    (val_sub, ":enemy_strength", 75), #75 Str Points reduction for completing the quest
    (display_message, "@Killing the refugees from {s1} and enslaving the survivors have demoralized their people ({s1} has lost {reg19} faction strength).", color_good_news),
    (faction_set_slot,":faction",slot_faction_strength_tmp,":enemy_strength"), ]],

[anyone,"lord_start", [ (check_quest_active,"qst_blank_quest_02"),
                        (check_quest_failed, "qst_blank_quest_02"),
                        (quest_get_slot, ":quest_giver", "qst_blank_quest_02", slot_quest_giver_troop),
                        (eq, ":quest_giver", "$g_talk_troop"),
                        (assign, reg1, "$qst_refugees_escaped")],
"{playername}, our spies tell us that you failed to intercept {reg1} of the refugee trains. They are weak and slow, and still you fail. What use are you?", "lord_hunt_refugees_failed", []],

[anyone|plyr,"lord_hunt_refugees_failed", [(str_store_troop_name, s65, "$g_talk_troop")],
   "They were slippery, master. I was unable to track them down.", "lord_hunt_refugees_failed_1", []],

[anyone,"lord_hunt_refugees_failed_1", [],
"Maybe you are not good enough to command the armies that will bring this world to its heels if you cannot even defeat the wounded and the sick!^^ Begone, and pray I give you a second chance.", "lord_pretalk",
   [(call_script, "script_change_player_relation_with_troop","$g_talk_troop",-1),
    (call_script, "script_end_quest", "qst_blank_quest_02"),
    (assign, reg18, "$qst_refugees_killed"),
    (call_script, "script_cf_get_random_enemy_center_in_theater", "p_main_party"),
    (store_faction_of_party, ":faction", reg0),
    (str_store_faction_name, s1, ":faction"),
    (faction_get_slot, ":enemy_strength", ":faction", slot_faction_strength_tmp),
    (store_mul, ":reduction", 15, reg18), #15 victory points per refugee party killed
    (assign, reg19, ":reduction"),
    (assign, reg20, "$qst_refugees_escaped"),
    (val_sub, ":enemy_strength", ":reduction"),
    (try_begin),
      (ge, "$qst_refugees_escaped",1),
      (assign, ":vp", 20),
    (else_try),
      (assign, ":vp", 30),
    (try_end),
    (val_add, ":enemy_strength", ":vp"), #VP for enemy depends if there were refugees that escaped.
    (assign, reg22, ":vp"),
    (display_message, "@{reg20} refugee trains escaped and improved the enemy's morale ({s1} has gained {reg22} faction strength).", color_bad_news),
    (try_begin),
      (ge, "$qst_refugees_killed",1),
      (display_message, "@You did, however, defeat {reg18} refugee trains, weakening the enemy's resolve ({s1} has lost {reg19} faction strength).", color_good_news),
    (try_end),
    (faction_set_slot, ":faction", slot_faction_strength_tmp, ":enemy_strength"), ]],


## Hunt Down Refugees Completion Dialogues END - Kham
#### Kham Sea Battle Quest Completion Start ####

[anyone|plyr,"lord_start", [
    (check_quest_active, "qst_blank_quest_03"),    
    (check_quest_succeeded, "qst_blank_quest_03"),
    (quest_get_slot, ":giver_troop", "qst_blank_quest_03", slot_quest_giver_troop),
    (eq, "$g_talk_troop", ":giver_troop"),
    (quest_get_slot, ":quest_target_center", "qst_blank_quest_03", slot_quest_target_center),
    (str_store_party_name, s12,":quest_target_center"),
    (try_begin),
    (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
    (try_begin), #South Good
      (eq, "$g_talk_troop_faction", "fac_gondor"),
      (str_store_string, s5, "@My lord, {s12} is safe. The Corsairs were defeated."),
    (else_try),
      (str_store_string, s5, "@My lord, Esgaroth is safe. The men of Rhûn were defeated."),
    (try_end),
  (else_try),
    (try_begin),
      (eq, "$g_talk_troop_faction", "fac_umbar"), #South Evil
      (str_store_string, s5, "@The surroundings of {s12} burn. The pillaging was glorious indeed!"),
    (else_try),
      (str_store_string, s5, "@The surroundings of Esgaroth burn. The pillaging was glorious indeed!"),
    (try_end),
  (try_end)],
"{s5}", "lord_sea_battle_completed",[]],

[anyone,"lord_sea_battle_completed", [
    (quest_get_slot, ":quest_target_center", "qst_blank_quest_03", slot_quest_target_center),
    (str_store_party_name, s12,":quest_target_center"),
    (try_begin),
      (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
      (try_begin), #South Good
        (eq, "$g_talk_troop_faction", "fac_gondor"),
        (str_store_string, s5, "@This is welcome news indeed, {playername}. We were ill-prepared for such bold action from the Corsairs. But thanks to you, the black sails have been driven away, at least for a time, and we may hope, at least, that we have struck them a blow this day. You have our thanks."),
      (else_try),
        (str_store_string, s5, "@ Good work, {playername}! They showed more cunning than we credited them with, I'll give them that. But these Easterlings don't fight half as well on their boats as they do on their horses, it would seem! Perhaps we, too, should consider launching a fleet of our own... In any case, we thank you, {playername}, on behalf of Esgaroth and all the people of Dale."),
      (try_end),
    (else_try),
      (try_begin),
        (eq, "$g_talk_troop_faction", "fac_umbar"), #South Evil
        (str_store_string, s5, "@Even from here, we could see the flames and smell the despair of our enemies on the wind! You have done splendidly, {playername}. Let terror now strike the heart of every man, woman and child in Gondor, for they know now that not even their mightiest strongholds are beyond our reach!"),
      (else_try),
        (str_store_string, s5, "@Even from here, we could see the flames and smell the despair of our enemies on the wind! You have done splendidly, {playername}. Let terror now strike the heart of every man, woman and child in Dale, for they know now that not even their mightiest strongholds are beyond our reach!"),
      (try_end),
    (try_end)],
"{s5}", "lord_pretalk",[

    (call_script,"script_quest_sea_battle_consequences",1),
    (call_script, "script_finish_quest", "qst_blank_quest_03", 100),
    ]],

[anyone|plyr,"lord_start", [
    (check_quest_active, "qst_blank_quest_03"),
    (check_quest_failed, "qst_blank_quest_03"),
    (quest_get_slot, ":giver_troop", "qst_blank_quest_03", slot_quest_giver_troop),
    (eq, "$g_talk_troop", ":giver_troop"),
    (quest_get_slot, ":quest_target_center", "qst_blank_quest_03", slot_quest_target_center),
    (str_store_faction_name,s12,":quest_target_center"),
    (try_begin),
    (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
      (try_begin), #South Good
        (eq, "$g_talk_troop_faction", "fac_gondor"),
        (str_store_string, s5, "@My lord, they fell upon us with great force. We could not repel the Corsairs."),
      (else_try),
        (str_store_string, s5, "@My lord, they fell upon us with great force. We could not repel the warriors of Rhûn."),
      (try_end),
    (else_try),
      (try_begin),
        (eq, "$g_talk_troop_faction", "fac_umbar"), #South Evil
        (str_store_string, s5, "@The raid on {s12} failed, thanks to the incompetence of our allies!"),
      (else_try),
        (str_store_string, s5, "@This raid was ill-fated from the start. We should never have gotten on those rickety rafts!"),
      (try_end),
    (try_end)],
"{s5}", "sea_battle_quest_failed_1",[]],

[anyone,"sea_battle_quest_failed_1", [
    (quest_get_slot, ":quest_target_center", "qst_blank_quest_03", slot_quest_target_center),
    (str_store_faction_name,s12,":quest_target_center"),
    (try_begin),
    (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
      (try_begin), #South Good
        (eq, "$g_talk_troop_faction", "fac_gondor"),
        (str_store_string, s5, "@This is evil news you bring. The black sails grow ever bolder, and all of Belfalas now lies ever more under their shadow. I will not blame you overmuch, {playername}, for your failure, but we have been struck a sore blow indeed, a sore blow. Go now. Hope dwindles for Gondor, and we must fight to keep what remains of it alive."),
      (else_try),
        (str_store_string, s5, "@This is evil news you bring. The Easterlings grow ever bolder, and Esgaroth burns. I will not blame you overmuch, {playername}, for your failure, but we have been struck a sore blow indeed, a sore blow. Go now. Hope dwindles for our kingdom, and we must fight to keep what remains of it alive."),
      (try_end),
    (else_try),
      (try_begin),
        (eq, "$g_talk_troop_faction", "fac_umbar"), #South Evil
        (str_store_string, s5, "@Pah! It seems you weren't able to find your sea-legs, {playername}. Now they sit, these men of Gondor, high in their towers, vain as kings, laughing as the black sails burn! Perhaps a stint at the oars of a galley would be fitting punishment for your troops; a pity they are under your command, and not mine. The Eye will not be pleased. Leave me now. "),
      (else_try),
        (str_store_string, s5, "@Have you nothing better than weak excuses to offer for your failure, {playername}? Perhaps you are not as strong as we had believed. Serve our cause better in future, {playername}. There will be no mercy for the weak!"),
      (try_end),
    (try_end)],
"{s5}", "lord_pretalk",[
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -2),

    (call_script,"script_quest_sea_battle_consequences",0),
    (cancel_quest, "qst_blank_quest_03"),
    ]],



#### Kham Sea Battle Quest Completion End ####

#### Kham Guardian Party Quest START


[anyone,"lord_start", [
    (check_quest_active, "qst_guardian_party_quest"),
    (quest_slot_eq, "qst_guardian_party_quest", slot_quest_dont_give_again_period, 0),   
    (neg|quest_slot_ge, "qst_guardian_party_quest", slot_quest_current_state, 3), 
    (quest_get_slot, ":giver_troop", "qst_guardian_party_quest", slot_quest_target_troop),
    (eq, "$g_talk_troop", ":giver_troop"),
    (str_store_string, s5, "@{playername}, we have Isengard on their knees. They have launched their last stand and is protecting Saruman in his tower. Ride with me and meet them!"),
    ],
"{s5}", "lord_guardian_party_start",[]],


[anyone,"lord_start", [
    (check_quest_active, "qst_guardian_party_quest"),
    (quest_slot_ge, "qst_guardian_party_quest", slot_quest_dont_give_again_period, 1),   
    (neg|quest_slot_ge, "qst_guardian_party_quest", slot_quest_current_state, 3), 
    (quest_get_slot, ":giver_troop", "qst_guardian_party_quest", slot_quest_target_troop),
    (eq, "$g_talk_troop", ":giver_troop"),
    (str_store_string, s5, "@Are you ready to meet Isengard's last stand?"),
    ],
"{s5}", "lord_guardian_party_start",[]],


[anyone|plyr,"lord_pretalk", [
    (check_quest_active, "qst_guardian_party_quest"),
    (neg|quest_slot_eq, "qst_guardian_party_quest", slot_quest_dont_give_again_period, 0),    
    (quest_get_slot, ":giver_troop", "qst_guardian_party_quest", slot_quest_target_troop),
    (eq, "$g_talk_troop", ":giver_troop"),
    (str_store_string, s5, "@I am ready to ride with you against Isengard."),
    ],
"{s5}", "lord_guardian_party_agree",[]],

[anyone|plyr,"lord_guardian_party_start", [
    (str_store_string, s5, "@I am ready to ride with you and meet them. Let us end this now."),
    ],
"{s5}", "lord_guardian_party_agree",[]],

[anyone|plyr,"lord_guardian_party_start", [
    (str_store_string, s5, "@I am not ready to ride with you yet. I need some more time."),
    ],
"{s5}", "lord_guardian_party_wait",[
  (quest_get_slot, ":wait_time", "qst_guardian_party_quest", slot_quest_dont_give_again_period),
  (val_add, ":wait_time", 1),
  (quest_set_slot, "qst_guardian_party_quest", slot_quest_dont_give_again_period, ":wait_time"),]],


[anyone,"lord_guardian_party_agree", [ (party_get_num_companions, ":party_size", "p_main_party",), (lt, ":party_size", 31),
    (str_store_string, s5, "@You do not have enough troops to help in this battle. Raise at least 30 men and join me soon!"),
    ],
"{s5}", "close_window",[
  (quest_get_slot, ":wait_time", "qst_guardian_party_quest", slot_quest_dont_give_again_period),
  (val_add, ":wait_time", 1),
  (quest_set_slot, "qst_guardian_party_quest", slot_quest_dont_give_again_period, ":wait_time"),]],


[anyone,"lord_guardian_party_agree", [ (party_get_num_companions, ":party_size", "p_main_party",), (ge, ":party_size", 31),
    (str_store_string, s5, "@Stay close, we will take position near the enemy. When we have all gathered, we will strike."),
    ],
"{s5}", "close_window",[
  (quest_set_slot, "qst_guardian_party_quest", slot_quest_current_state, 3),
  (call_script,"script_stand_back"),
  (eq,"$talk_context",tc_party_encounter),
  (assign, "$g_leave_encounter", 1)]],

[anyone,"lord_guardian_party_wait", [
    (quest_get_slot, ":wait_time", "qst_guardian_party_quest", slot_quest_dont_give_again_period),
    (try_begin),
      (gt, ":wait_time", 2),
      (str_store_string, s5, "@You have taken too long... We shall ride now, with or without you. We will gather near the enemy, and in 3 days time, we will strike."),
    (else_try),
      (str_store_string, s5, "@Make haste, {playername}. We do not want them to recover."),
    (try_end),
    ],
"{s5}", "close_window",[
    (quest_get_slot, ":wait_time", "qst_guardian_party_quest", slot_quest_dont_give_again_period),
    (try_begin),
      (gt, ":wait_time", 2),
      (quest_set_slot, "qst_guardian_party_quest", slot_quest_current_state, 3),
    (try_end),
    (call_script,"script_stand_back"),(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],

#### Kham Guardian Party Quest END


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
   [ (quest_get_slot, ":quest_target_item", "qst_deliver_cattle_to_army", slot_quest_target_item),
     (quest_get_slot, ":quest_target_amount", "qst_deliver_cattle_to_army", slot_quest_target_amount),
     (troop_remove_items, "trp_player", ":quest_target_item", ":quest_target_amount"),
     (store_item_value, ":item_value", ":quest_target_item"),
     (val_mul, ":item_value", 150), (val_div, ":item_value", 100), #50% profit
     (store_mul, ":reward", ":quest_target_amount", ":item_value"),
     #(call_script, "script_troop_add_gold", "trp_player", ":reward"),
     (call_script, "script_add_faction_rps", "$g_talk_troop_faction", ":reward"),
     (val_div, ":reward", 5),
     (add_xp_as_reward, ":reward"),
	 (store_mul, ":rank_reward", ":quest_target_amount", 2),
     (call_script, "script_increase_rank", "$g_talk_troop_faction", ":rank_reward"),
     (call_script, "script_end_quest", "qst_deliver_cattle_to_army"),
	 (store_div, ":relation", ":quest_target_amount", 2),
	 (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", ":relation"),
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
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4),
#     (call_script, "script_troop_add_gold", "trp_player", 100),
     (add_xp_as_reward, 100),
     (call_script, "script_increase_rank", "$g_talk_troop_faction", 10),
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

[anyone,"lord_report_to_army_completed", [
  (call_script, "script_get_faction_rank", "$g_talk_troop_faction"), 
  (assign, ":rank", reg0), #rank points to rank number 0-9
  (call_script, "script_get_rank_title_to_s24", "$g_talk_troop_faction"), 
  (str_store_string_reg, s25, s24), #to s25 (current rank)
  (call_script, "script_get_any_rank_title_to_s24", "$g_talk_troop_faction", 8), #to s24 (highest rank) #kham - reduced from 9
  (try_begin),
    (lt, ":rank", 8), #kham - reduced from 9
    (str_store_string, s3, "@Moreover, should you become {s24}, you will be welcomed to my War Council, where you can make decisions that will affect the course of our campaign. For the moment, as a {s25}, just follow us and stay close. We'll be moving soon."),
  (else_try),
    (str_store_string, s3, "@For the moment, just follow us and stay close. We'll be moving soon."),
  (try_end),
  ], 
  "Excellent. I will send the word when I have a task for you. {s3}", "close_window",[
     (call_script,"script_stand_back"),
	 (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
	 (store_div, ":rank_reward", reg0, 100),
     (call_script, "script_increase_rank", "$g_talk_troop_faction", ":rank_reward"),
	 (store_div, ":relation_reward", ":rank_reward", 2),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", ":relation_reward"),
     (call_script, "script_end_quest", "qst_report_to_army"),
     (quest_set_slot, "qst_report_to_army", slot_quest_giver_troop, "$g_talk_troop"),
     #Activating follow army quest
     (str_store_troop_name_link, s9, "$g_talk_troop"),
     (setup_quest_text, "qst_follow_army"),
     (str_store_string, s2, "@{s9} wants you to follow his army until further notice."),
     (call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop"),
     (store_current_hours, ":cur_hours"),
     (quest_set_slot, "qst_follow_army", slot_quest_xp_reward, ":cur_hours"), #store beginning of player following in an unused slot, to calulcate xp reward later)
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
###Kham - Intro Quest START #####

[anyone, "lord_start", [
  (check_quest_active, "qst_tld_introduction"),
  (quest_slot_eq, "qst_tld_introduction", slot_quest_target_troop, "$g_talk_troop"),
  (faction_get_slot, ":side", "$players_kingdom", slot_faction_side),
  (str_clear, s5),
  (faction_get_slot, ":faction_theater", "$players_kingdom", slot_faction_active_theater),
  (try_begin),
    (eq, ":side", faction_side_good),
    (try_begin),
      (eq, ":faction_theater", theater_SE),
      (str_store_string, s11, "@Sauron in Mordor, the Corsairs of Umbar, the Variags of Khand, and Harad Tribesmen"),
    (else_try),
      (eq, ":faction_theater", theater_SW),
      (str_store_string, s11, "@Saruman in Isengard and the Wildmen of Dunland"),
    (else_try),
      (eq, ":faction_theater", theater_C),
      (str_store_string, s11, "@Orcs of Moria and Dol Guldur"),
    (else_try),
      (str_store_string, s11, "@Orcs of Gundabad and the Warriors of Rhun"),
    (try_end),
  (else_try),
    (eq, ":faction_theater", theater_SE),
    (str_store_string, s11, "@Men of Gondor"),
  (else_try),
    (eq, ":faction_theater", theater_SW),
    (str_store_string, s11, "@Riders of Rohan"),
  (else_try),
    (eq, ":faction_theater", theater_C),
    (str_store_string, s11, "@Elves of Imladris and Lothlorien"),
  (else_try),
    (str_store_string, s11, "@Men of Dale, Dwarves of Erebor, Beorn's kinsmen, and the Elves of Mirkwood"),
  (try_end),
  (try_begin),
    (eq, ":side", faction_side_good),
    (str_store_string, s5, "@Ah, {playername}, it is good you have come. War is at our doorstep and we need soldiers and captains alike to fulfill their oaths.^^We are at war with {s11}, but we have to gather our strength and weaken the enemy before we can hope to move against their strong-points and fortresses. Each defeat of our enemies will bring us closer to victory and strengthen our resolve, so I trust you to fight our enemy at every opportunity, be it a mere scout party or a war host. Yet do not rush into battle alone, you must fight alongside our brave captains and our allies also."),
  (else_try),
    (str_store_string, s5, "@About time you showed up, {playername}. We're at war now and I will not tolerate any insubordination. We are fighting against {s11}, but we have to gather our strength and smite the enemy in the field before we can move against their fortresses. Each defeat of our enemies will strengthen our war efforts and bring them closer to their utter destruction. So I trust you to fight our enemy at every opportunity, be it a mere scout party or a war host. Also, you are to support our captains and our allies if you see them fight. Do not fail them or I will know."),
  (try_end)],
  "{s5}", "tld_intro_1", []],

[anyone, "tld_intro_1", [], 
 "War Tutorial:^^\
- Factions will only initiate sieges when they are strong enough.^\
- Most settlements can only be sieged if their faction is weakened enough. Usually, capitals will be sieged last.^\
- If a faction loses their capital, they will be defeated.^\
- Factions gain strength from victories in the field and from holding certain key settlements.^\
- Factions lose strength from defeats in the field or from losing settlements.^\
- Some quests or events can affect faction strength.^\
- You can compare the current faction strength ratings in the 'Reports' menu.^\
- See the Info Pages for more TLD guides.", "lord_pretalk", [
  (add_xp_as_reward,50),
  (call_script,"script_end_quest","qst_tld_introduction"),]],


#TLD: your king gives you a faction intro when you first meet him
[anyone,"lord_start", [
        (faction_slot_eq,"$players_kingdom",slot_faction_leader,"$g_talk_troop"),
        (eq, "$g_talk_troop_met", 0)],
"Ah, welcome, {s24}.^You should already know that {s12}. \
Your duty is to help in our struggle, {playername}. When you prove yourself worthy of my confidence [level {reg1}], I will also allow you access to that chest over there, for you to store your personal belongings."
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
[anyone,"lord_pretalk", [], "Anything else?", "lord_talk",[] + (is_a_wb_dialog and [(assign,"$tld_forbid_troop_upgrade_mode",0)] or []) ],
#[anyone,"hero_pretalk", [], "Anything else?", "lord_talk",[]],

##### TODO: QUESTS COMMENT OUT BEGIN
[anyone|plyr,"lord_talk", [(eq, "$cheat_mode", 1)], "Increase Relation", "lord_pretalk",[(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5),]],
#Friendship Rewards Begin
[anyone|plyr,"lord_talk", [(eq, "$cheat_mode", 1)], "Force Friendship Reward", "lord_pretalk",[
    (call_script, "script_lord_friendship_reward_progress", "$g_talk_troop", 100),]],
#Friendship Rewards End
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
	#(quest_get_slot, ":duration", slot_quest_target_amount),
    (party_add_members, "p_main_party", ":quest_target_troop", 1),
    # (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
    # (add_xp_as_reward, 100),
    (call_script, "script_finish_quest", "qst_lend_companion", 100),
    (str_store_troop_name,s14,":quest_target_troop"),
    (troop_get_type, reg3, ":quest_target_troop"),
    (try_begin),
      (gt, reg3, 1), #MV: non-humans are male
      (assign, reg3, 0),
	(try_end),
	  
    (assign, ":reward_xp", 500),
	(store_attribute_level, ":int", ":quest_target_troop", ca_intelligence),
	(store_character_level, ":lvl", ":quest_target_troop"),
    (val_mul, ":int",":lvl"),  
	(val_mul, ":reward_xp",":int"),
	(val_div, ":reward_xp", 100),
	#(val_mul, ":reward_xp",":duration"), #scale with days you have to give them away, in case we want to make duration vary in future. Doesn't yet work, because slot_quest_target_amount is actually the campaign date
    (add_xp_to_troop, ":reward_xp", ":quest_target_troop"), #Lets give em XP
    (assign, reg78, ":reward_xp"),
    (display_message, "@ {s14} gained {reg78} experience."),]],
   
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
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4)]],

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

# TLD: Dwarf Lord takes Moria book, and gives player lotsa rank pts. Placeholder for now... (CppCoder) -- Reinplemented by Kham, Dialogue by Yarrum

[anyone|plyr,"lord_talk", 
  [(eq, "$g_talk_troop", "trp_dwarf_lord"),
   (player_has_item, "itm_book_of_moria"),
   (store_troop_faction, ":faction", "trp_player"),
   (str_clear, s3),
   (try_begin),
      (eq, ":faction", "fac_dwarf"),
      (str_store_string, s3, "@My king"),
    (else_try),
      (str_store_string, s3, "@Lord"),
    (try_end)], 
      "{s3}, I have a matter which I must bring to your attention.", "dwarf_lord_book", []],

[anyone,"dwarf_lord_book", 
  [], "Speak freely, {playername}.", "dwarf_lord_book_give", []],

[anyone|plyr,"dwarf_lord_book_give", 
  [], "I ventured deep into the Mines of Moria and found record of Balin's company.", "dwarf_lord_book_give_a", []],

[anyone,"dwarf_lord_book_give_a", 
  [], "You speak of my kin as though they are a memory. Is it so?", "dwarf_lord_book_give_b", []],

[anyone|plyr,"dwarf_lord_book_give_b", 
  [], "I'm afraid it is. I'd have searched further but I was beset by goblins, and in great number. I bring only this...", "dwarf_lord_book_give_c", 
    [(troop_remove_item, "trp_player", "itm_book_of_moria"), (assign, "$moria_book_given",1)]],

[anyone,"dwarf_lord_book_give_c", 
  [], "'We cannot get out. We cannot get out...They are coming.'", "dwarf_lord_book_give_d", []],

[anyone,"dwarf_lord_book_give_d", 
  [], "So it is as I feared. I had counseled Balin against this expedition but he was resolved. A fool I was for giving him leave to go.", "dwarf_lord_book_give_e", []],

[anyone,"dwarf_lord_book_give_e", 
  [], "You have done Erebor a great service, {playername}, and your deed will not go unrewarded.", "dwarf_lord_book_give_f", 
    [(call_script, "script_increase_rank",   "fac_dwarf", 50),
     (call_script, "script_add_faction_rps", "fac_dwarf", 300),]],

[anyone|plyr,"dwarf_lord_book_give_f", 
  [(store_troop_faction, ":faction", "trp_player"),
   (str_clear, s3),
   (try_begin),
      (eq, ":faction", "fac_dwarf"),
      (str_store_string, s3, "@my king"),
    (else_try),
      (str_store_string, s3, "@lord"),
    (try_end)], 
      "Thank you, {s3}.", "dwarf_lord_book_give_g", []],

[anyone|plyr,"dwarf_lord_book_give_g", 
  [], "What will you do now?", "dwarf_lord_book_give_h", []],

[anyone,"dwarf_lord_book_give_h", 
  [], "We will not let the murders of our kin go unanswered. We will bring ruin and death to those who have wronged us. From the peaks of Mt. Gundabad to the deepest pits of Khazad-dûm, the Misty Mountains will be stained black with goblin blood.", "dwarf_lord_book_give_i", []],

[anyone|plyr,"dwarf_lord_book_give_i", 
  [(check_quest_active|neg, "qst_oath_of_vengeance"),
   (this_or_next|faction_slot_eq, "fac_moria", slot_faction_state, sfs_active),
   (faction_slot_eq, "fac_gundabad", slot_faction_state, sfs_active),
   (store_troop_faction, ":faction", "trp_player"),
   (str_clear, s3),
   (str_clear, s4),
   (try_begin),
      (eq, ":faction", "fac_dwarf"),
      (str_store_string, s3, "@my king"),
      (str_store_string, s4, "@our"),
    (else_try),
      (str_store_string, s3, "@lord"),
      (str_store_string, s4, "@your"),
    (try_end)], 
      "{s3}, I wish to help {s4} people avenge Balin and his company.", "dwarf_lord_avenge", []],

[anyone|plyr,"dwarf_lord_book_give_i", 
  [], "I wish you good luck with that.", "lord_pretalk", []],

[anyone,"dwarf_lord_avenge", 
  [], "Very good, {playername}. Go with the blessings of Durin's folk and bring death to our enemies. Make them know pain and fear as our people have known them.", "close_window", 
    [(str_clear, s4),(str_clear, s3),(str_clear, s2),
     (str_store_troop_name, s4, "$g_talk_troop"),
     (store_troop_faction, ":target", "$g_talk_troop"),
     (quest_set_slot, "qst_oath_of_vengeance", 4, ":target"), # remember source ally faction
     (quest_set_slot, "qst_oath_of_vengeance", 5, "trp_dwarf_lord"), # CppCoder: remember source hero
     (store_current_day, ":day"),
     (quest_set_slot, "qst_oath_of_vengeance", 1, ":day"),
     (try_begin),
        (faction_slot_eq, "fac_moria", slot_faction_state, sfs_active),
        (faction_slot_eq, "fac_gundabad", slot_faction_state, sfs_active),
        (str_store_string, s3, "@Moria and Gundabad"),
      (else_try),
        (faction_slot_eq, "fac_moria", slot_faction_state, sfs_active),
        (str_store_string, s3, "@Moria"),
      (else_try),
        (faction_slot_eq, "fac_gundabad", slot_faction_state, sfs_active),
        (str_store_string, s3, "@Gundabad"),  
      (try_end),      
     (quest_set_slot, "qst_oath_of_vengeance", 2, "fac_moria"), # target faction
     (quest_set_slot, "qst_oath_of_vengeance", 7, "fac_gundabad"), # target faction 2
     (quest_set_slot, "qst_oath_of_vengeance", 6, 1),
     (setup_quest_text, "qst_oath_of_vengeance"),
     (str_store_string, s2, "@You swear an oath of vengeance against {s3}. You must now kill as many of the troops of Moria and Gundabad as possible in the coming days. You are keenly aware that your followers have witnessed this oath and you do not wish to become known as an oathbreaker. An orgy of bloodletting must now begin!^."),
     (call_script, "script_start_quest", "qst_oath_of_vengeance", "trp_player")]],

# TLD: End Dwarf Lord takes Moria book - Implemented by Kham

#TLD Dain II Ironfoot dialogue (Kolba, modified by CppCoder) -- begin

[anyone|plyr,"lord_talk", [(eq, "$g_talk_troop", "trp_dwarf_lord"),(check_quest_active,"qst_find_lost_spears"),(neg|quest_slot_ge, "qst_find_lost_spears", slot_quest_current_state, 1) ], "My lord, I wish to enter into the lonely mountains, in search of King Bladorthin's lost spears.", "find_lost_spears_permission", []],
                            
[anyone,"find_lost_spears_permission",[(check_quest_active,"qst_find_lost_spears"),(quest_slot_eq, "qst_find_lost_spears", slot_quest_current_state, 10),], "I already gave you permission, {playername}.", "lord_pretalk", []],

[anyone,"find_lost_spears_permission",[(check_quest_active,"qst_find_lost_spears"),(quest_slot_eq, "qst_find_lost_spears", slot_quest_current_state, 0),(ge, "$g_talk_troop_relation", 5)], "Alright, {playername}, you may enter into the mountains.", "find_lost_spears_permission_yes", [(quest_set_slot, "qst_find_lost_spears", slot_quest_current_state, 10),]],

[anyone,"find_lost_spears_permission",[(check_quest_active,"qst_find_lost_spears"),(quest_slot_eq, "qst_find_lost_spears", slot_quest_current_state, 0)],"I'm sorry, but I don't know or trust you well enough, {playername}.", "lord_pretalk", []],

[anyone|plyr,"find_lost_spears_permission_yes",[], "I thank you, my Lord.", "lord_pretalk",[]],

[anyone|plyr,"lord_talk", [(eq, "$g_talk_troop", "trp_dwarf_lord"),(check_quest_active,"qst_find_lost_spears"),(quest_slot_eq, "qst_find_lost_spears", slot_quest_current_state, 15),], 
"My lord, I found a sack with a fading emblem of grapes and some shards of wood and metal inside that could have belong to a spear.", "tell_dorwinion_sack", []],

[anyone,"tell_dorwinion_sack",
  [], "Very interesting. This ancient sack could have born the mark of the finest wines that could only come from Dorwinion.", "tell_dorwinion_sack_2",
  []],
[anyone|plyr,"tell_dorwinion_sack_2",
  [], "I also found this Rhun helm in the sack. Could this tell us more about what happened to the Spears?", "tell_dorwinion_sack_3",
  []],
[anyone,"tell_dorwinion_sack_3",
  [], "Caravans are often robbed along the way. That helm is from a Rhun Scout. Follow the river down south to the Sea of Rhun and search the trade routes to Dorwinion and you may find what you are looking for. NOTE: THIS QUEST IS NOT YET COMPLETED. TO BE CONTINUED.", "lord_pretalk", 
      [(quest_set_slot, "qst_find_lost_spears", slot_quest_current_state, 20),
      (str_store_string, s2, "@The search for the Lost Spears has led you to Dorwinion, the site of the ancient northern kingdom of King Bladorthin. TO BE CONTINUED"),
      (add_quest_note_from_sreg, "qst_find_lost_spears", 1, s2, 0),
      (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
      (add_xp_as_reward,50),
      (call_script,"script_end_quest", "qst_find_lost_spears"),
      #(enable_party, "p_amath_dollen_fortress"),
      ]],


#TLD Dain II Ironfoot dialogue (Kolba, modified by CppCoder, Continued by Kham) -- end
              
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


##Kham - Lord Healers Start

[anyone|plyr,"lord_talk", [
  (this_or_next|eq, "$g_talk_troop", "trp_imladris_lord"), #Elrond
  (this_or_next|eq, "$g_talk_troop", "trp_knight_1_4"), #Orthalion
  (this_or_next|eq, "$g_talk_troop", "trp_knight_3_7"), #Orophin
  (this_or_next|eq, "$g_talk_troop", "trp_knight_2_2"), #Berúthiel
  (             eq, "$g_talk_troop", "trp_knight_2_7"), #Na'man

  (eq, "$tld_option_injuries", 1),
  ], 
    "I have heard that you were a great healer. Is this true, and can you help me?", "lord_healer_wound_ask",[]],

[anyone,"lord_healer_wound_ask", [
      (call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (assign, ":rank", reg0), #rank points to rank number 0-9
      (lt, ":rank", 3),
      (call_script, "script_get_rank_title_to_s24", "$g_talk_troop_faction"), (str_store_string_reg, s25, s24), #to s25 (current rank)
      (call_script, "script_get_any_rank_title_to_s24", "$g_talk_troop_faction", 3), #to s24
      (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
      (str_store_string, s2, "@(You need to be {s24} or higher)."),
      (try_begin),
        (neq, ":side", faction_side_good),
        (str_store_string, s1, "@You are not worthy of my skills. Prove yourself first, and rise above {s25}. {s2}"),
      (else_try),
        (str_store_string, s1, "@I am sorry. I cannot attend to you as a {s25} as there are more pressing issues. {s2}"), 
      (try_end), ], 
          "{s1}", "lord_pretalk",[]],

[anyone,"lord_healer_wound_ask", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s1, "@Yes, I am, and I can help you for a price."),
  (else_try),
    (str_store_string, s1, "@You heard right, and yes, I can aid you."),
  (try_end)], 
    "{s1}", "lord_healer_wound_ask_check",[]],

[anyone|plyr,"lord_healer_wound_ask_check", [

  (troop_get_slot, ":wound_mask", "trp_player", slot_troop_wound_mask),
  (assign, ":wounds", 0), 

  # Check If there are any wounds (player) before continuing with dialogue
  (try_begin),
    (neq, ":wound_mask", 0),
    
    (try_begin),(store_and,":x",":wound_mask",wound_head ),(neq,":x",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":x",":wound_mask",wound_chest),(neq,":x",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":x",":wound_mask",wound_arm  ),(neq,":x",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":x",":wound_mask",wound_leg  ),(neq,":x",0),(val_add,":wounds",1),(try_end),
    (troop_set_slot, "trp_player", slot_troop_needs_healing, 1), #Set the slot
    #(display_message, "@DEBUG: Player is wounded"),

  (else_try),
  # Check If any companions are wounded before continuing with dialogue
  (try_for_range, ":npc", companions_begin, new_companions_end),
    (this_or_next|is_between, ":npc", companions_begin, companions_end),
    (is_between, ":npc", new_companions_begin, new_companions_end),
    (main_party_has_troop, ":npc"),
    (troop_get_slot, ":wound_mask_npc", ":npc", slot_troop_wound_mask),
    (neq, ":wound_mask_npc", 0),
    #(assign, ":wounds", 0), 
    (try_begin),(store_and,":y",":wound_mask_npc",wound_head ),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":y",":wound_mask_npc",wound_chest),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":y",":wound_mask_npc",wound_arm  ),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":y",":wound_mask_npc",wound_leg  ),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (troop_set_slot, ":npc", slot_troop_needs_healing, 1), #Set the slot
    (str_store_troop_name, s3, ":npc"),
    #(display_message, "@DEBUG:{s3} is wounded"),
  (try_end),
  (try_end),

  #Do we continue?
  (gt, ":wounds",0),
  ], 
    "My men and I have wounds that require more than just time to heal. Can you heal our wounds?", "lord_healer_wound_heal",[]],




[anyone|plyr,"lord_healer_wound_ask_check", [
  (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
  (assign, ":yes",0),
  (try_for_range, ":stack", 0, ":num_stacks"),
    (party_stack_get_num_wounded, ":wounded", "p_main_party", ":stack"),
    (ge, ":wounded", 1),
    (assign, ":yes",1),
  (try_end),

  (eq, ":yes", 1)], 
    "My men and I are injured, and we do not have the time to wait for them to heal. Can you provide aid?", "lord_healer_injured_ask",[]],

[anyone|plyr,"lord_healer_wound_ask_check", [], 
    "Not right now.", "lord_pretalk",[]],


[anyone,"lord_healer_wound_heal", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (str_store_string, s2, "@(Costs 1000 Resource, 5 Influence)"),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s1, "@I can see that. I'll have my men stand guard while I deal with you. It will take some time. {s2}"),
  (else_try),
    (str_store_string, s1, "@Yes, I see that. I can do tend to you yes, but it will take me away from important tasks. {s2}"),
  (try_end)], 
    "{s1}", "lord_healers_wound_check",[]],

[anyone,"lord_healer_injured_ask", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (str_store_string, s2, "@(Costs 1500 Resource, 10 Influence)"),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s1, "@I'll have my personal healers deal with you. They are the best. Tell me when you want them here. {s2}"),
  (else_try),
    (str_store_string, s1, "@I'll have my personal healers tend to your men. They are the best at what they do. Let me know when you need them. {s2}"),
  (try_end)], 
    "{s1}", "lord_healers_injured_check",[]],

[anyone|plyr,"lord_healers_injured_check", [
  (call_script,"script_update_respoint"),
  (faction_get_slot, ":rps", "$g_talk_troop_faction", slot_faction_respoint),
  (faction_get_slot, ":inf", "$g_talk_troop_faction", slot_faction_influence),
  (ge, ":inf", 10),
  (ge,":rps", 1500)], 
    "Yes, attend to us.", "lord_healers_injured_heal",[]],


[anyone|plyr,"lord_healers_wound_check", [
  (call_script,"script_update_respoint"),
  (faction_get_slot, ":rps", "$g_talk_troop_faction", slot_faction_respoint),
  (faction_get_slot, ":inf", "$g_talk_troop_faction", slot_faction_influence),
  (ge, ":inf", 5),
  (ge,":rps", 1000)], 
    "Yes, attend to us.", "lord_healers_wound_heal",[]],


[anyone|plyr,"lord_healers_wound_check", [], 
    "Not right now.", "lord_pretalk",[]],

[anyone|plyr,"lord_healers_injured_check", [], 
    "Not right now.", "lord_pretalk",[]],

[anyone,"lord_healers_injured_heal", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s12, "@I'll have them here shortly."),
  (else_try),
    (str_store_string, s12, "@Let us begin. My healers will take care of you and your men."),
  (try_end)], 
    "{s12}", "lord_healers_wound_done",[
      (heal_party, "p_main_party")]],

[anyone,"lord_healers_wound_heal", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s12, "@Alright! This is going to hurt... a lot."),
  (else_try),
    (str_store_string, s12, "@Let us begin. It may take some time. Just relax and leave the rest to me."),
  (try_end)], 
    "{s12}", "lord_healers_wound_done",[
      
      (call_script, "script_add_faction_rps", "$g_talk_troop_faction", -500),
      (call_script, "script_spend_influence_of", 5, "$g_talk_troop_faction"),

      ## Get Faction Side
      (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),

      (try_begin), #Check if wounded - Start with Evil
        (neq, ":side", faction_side_good),

        #If Player is Wounded & Evil Side - Heal then hurt him.
        (try_begin),
          (troop_slot_eq, "trp_player", slot_troop_needs_healing, 1),
          (call_script, "script_healing_routine_full", "trp_player"),
          (troop_set_slot, "trp_player", slot_troop_needs_healing, 0), #Set the Slot
          (store_troop_health, ":plyr_hp", "trp_player"),
          (val_sub, ":plyr_hp", 20),
          (try_begin),
            (le, ":plyr_hp", 0),
            (troop_set_health, "trp_player", 5),
          (else_try),
            (troop_set_health, "trp_player", ":plyr_hp"),
          (try_end),
        (try_end),

        #If any companion is wounded & Evil Side - heal then hurt them
        (try_begin),
          (try_for_range, ":npc", companions_begin, new_companions_end),
            (this_or_next|is_between, ":npc", companions_begin, companions_end),
            (is_between, ":npc", new_companions_begin, new_companions_end),
            (troop_slot_eq, ":npc", slot_troop_needs_healing, 1),
            (call_script, "script_healing_routine_full", ":npc"),
            (troop_set_slot, ":npc", slot_troop_needs_healing, 0), #Set the Slot
            (store_troop_health, ":npc_hp", ":npc"),
            (val_sub, ":npc_hp", 20),
            (try_begin),
              (le, ":npc_hp", 0),
              (troop_set_health, ":npc", 5),
            (else_try),
              (troop_set_health, ":npc", ":npc_hp"),
            (try_end),
          (try_end),
        (try_end),

      #If Player is Wounded & Good Side - Heal then Rest
      (else_try),
        (try_begin),
          (troop_slot_eq, "trp_player", slot_troop_needs_healing, 1),
          (call_script, "script_healing_routine_full", "trp_player"),
          (troop_set_slot, "trp_player", slot_troop_needs_healing, 0), #Set the slot
        (try_end),
        
        #If any companion is wounded & Good Side - heal then rest
        (try_begin),
          (try_for_range, ":npc", companions_begin, new_companions_end),
            (this_or_next|is_between, ":npc", companions_begin, companions_end),
            (is_between, ":npc", new_companions_begin, new_companions_end),
            (troop_slot_eq, ":npc", slot_troop_needs_healing, 1),
            (call_script, "script_healing_routine_full", ":npc"),
            (troop_set_slot, ":npc", slot_troop_needs_healing, 0), #Set the slot
          (try_end),
        (try_end),
      (try_end),
      ]],

[anyone,"lord_healers_wound_done", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s12, "@Impressive... You didn't flinch much. Go back to your post."),
  (else_try),
    (str_store_string, s12, "@Rest, the wounds have been taken care of."),
  (try_end)], 
    "{s12}", "close_window",[
      (call_script, "script_stand_back"),
      (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
      (try_begin),
        (eq, ":side", faction_side_good),
        (change_screen_map),
        (rest_for_hours, 4,15,0),
      (try_end)]],

### Kham Lord Healers END


###Kham Quest -- Ring Hunters --- Either Dwarf_Lord or imladris_lord #####

[anyone|plyr,"lord_talk",[
 (this_or_next|eq, "$g_talk_troop","trp_dwarf_lord"),
 (eq, "$g_talk_troop","trp_imladris_lord"), 
 (ge, "$g_talk_troop_relation", 5),
 (neg|check_quest_finished, "qst_ring_hunters"),
 (neg|quest_slot_ge,"qst_ring_hunters",slot_quest_current_state,10),
 (store_character_level, ":playerlvl", "trp_player"),
 (ge, ":playerlvl",11),],
  "My lord, I am prepared to take more arduous tasks to serve you better and end this war. What would you have me do?",
  "ring_hunters_start", []],

[anyone,"ring_hunters_start",
[],
  "{playername}, you have done great deeds and proven yourself worthy of the task I will now request of you. I trust you to deal with this matter as best you see fit, but know that our foe is dangerous and bloodshed will be unavoidable. Is your company strong enough for battle?","ring_hunters_check", []],

[anyone|plyr,"ring_hunters_check",[
  (party_get_num_companions, ":party_size", "p_main_party"),(ge, ":party_size", 30),],
  "Yes, my lord. I have a group of well-trained, battlehardened men. We are ready for anything.","ring_hunters_1",
  []],

[anyone|plyr,"ring_hunters_check",
[],
  "I am afraid not, my lord.", "ring_hunters_check_failed",[]],

[anyone,"ring_hunters_check_failed",
[],
  "Then you are not ready for this task yet,{playername}. Go and gather more troops.","lord_pretalk",
  [(display_message, "@Your party must be at least 30 strong to begin this quest", color_neutral_news),]],
 

[anyone, "ring_hunters_1",
  [],
  "Excellent. The North has recently been plagued by a marauding band of outlaws, who raid villages and ambush travellers searching for rings of any kind\
   You are to hunt these bandits down and put an end to their quest. Survivors of their last pillaging have reported two groups.\
   The first is returning with their loot to their encampment on the eaves of Mirkwood. The other, advances towards Beorn's House in great numbers, and I fear what may happen if they are left unimpeded.","ring_hunters_2",
  []],

[anyone|plyr,"ring_hunters_2",
[],
  "My lord, what could they be searching for?", "ring_hunters_what",
[]],

[anyone|plyr,"ring_hunters_2",
[],
  "My lord, I will do what is necessary to stop these... 'Ring Hunters'", "ring_hunters_accept",
[]],

[anyone|plyr,"ring_hunters_2",
[],
  "I am not ready for such a task just yet.","ring_hunters_reject",
[]],

[anyone,"ring_hunters_accept", ### Spawns Ring Hunter party near Beorn's House & Spawns Bandit Hideout near Mirkwood Forest
[],
  "With bravery in your heart and sharp steel in your hands you will, {playername}. We will await news of your success.","close_window",[
  (quest_set_slot,"qst_ring_hunters",slot_quest_target_troop,"$g_talk_troop"),
  (setup_quest_text, "qst_ring_hunters"),
  (str_store_string, s2, "@You were tasked to hunt down the bandits that have been recently wreaking havoc in the North. You can either attack them in their hideout near Mirkwood Forest or intercept them near Beorn's House."),
  (call_script, "script_start_quest", "qst_ring_hunters", "$g_talk_troop"),
  (quest_set_slot, "qst_ring_hunters", slot_quest_current_state, 10),
  (enable_party,"p_ring_hunter_lair"),
  (set_spawn_radius, 5),(spawn_around_party, "p_town_beorn_house", "pt_ring_hunters"),
  (assign,"$qst_ring_hunter_party",reg0),
  (assign,"$qst_ring_hunter_lord","$g_talk_troop"),
]],


[anyone,"ring_hunters_reject",
[],
  "I see. Let me know when you are, but make haste, we do not want them to succeed.","lord_pretalk",
[]],

[anyone,"ring_hunters_what",  ### Elf Lord Question
  [(eq,"$g_talk_troop","trp_imladris_lord"),],
  "Designs of the Enemy are hidden from us, but we can see thes ruffians are bent on finding what they are looking for.\
  I cannot reveal all that we know, for much hangs in the balance and secrecy is paramount. Whatever they seek must be a powerful weapon, one to be used to cause more destruction in the Dark Lord's name.",
   "ring_hunters_2",
   []],

[anyone,"ring_hunters_what",  ### Dwarf Lord Question
  [(eq,"$g_talk_troop","trp_dwarf_lord"),],
  "The Dark Lord previously sent emissaries to different dwarven clans, asking about the rings of power given to our people. These bandits may be looking for them, or others like them...\
   Whether true or not, they must not fall into the Dark Lord's hands.",
   "ring_hunters_2",
   []],


[anyone|plyr,"lord_talk",[    ### Ring Hunter Quest Completion - Party Defeated.
 (this_or_next|eq, "$g_talk_troop","trp_dwarf_lord"),
 (eq, "$g_talk_troop","trp_imladris_lord"), 
 (check_quest_active,"qst_ring_hunters2"),
 (quest_slot_eq, "qst_ring_hunters2", slot_quest_current_state, 10)],
  "My lord, I come bearing ill news... Though I have defeated the Ring Hunters terrorizing the villages, their leaders were not there. They may have found what they were looking for", "ring_hunter_party_defeated",
 []],

[anyone,"ring_hunter_party_defeated",
  [],
    "This is not ill news,{playername}. We have heard of your great victory! The lives of those villagers matter more to our cause than any weapon. As we speak, the Beornings are amassing their strength, invigorated by your victory.\
     Moreover, we don't believe that these Ring Hunters found what they are looking for. If it was the weapon we feared, then we would have felt something... a disturbance.", "ring_hunter_party_defeated2",
    []],

[anyone|plyr,"ring_hunter_party_defeated2",
  [],
    "I am glad, then. Whatever this weapon may have been... they may still be looking for it. I will remain vigilant and remain on the lookout for more of these Ring Hunters.", "ring_hunter_quest_end",
    []],
[anyone,"ring_hunter_quest_end",
  [],
    "We all will. Thank you once more for your service, {playername}.","close_window",
    [ (call_script,"script_increase_rank","$g_talk_troop_faction",20),
      (add_xp_as_reward,500),
      (call_script,"script_end_quest","qst_ring_hunters2"),
      (faction_get_slot,":evil","fac_mordor",slot_faction_strength_tmp), 
      (val_add, ":evil", 30),
      (display_message,"@Mordor gains Faction Strength as they received an unknown weapon",color_bad_news),
      (faction_get_slot,":win","fac_beorn",slot_faction_strength_tmp),
      (val_add, ":win", 150),
      (display_message,"@Beornings gain Faction Strength as news of your victory spreads.",color_good_news),
      (faction_set_slot,"fac_beorn",slot_faction_strength_tmp,":win"),
      (faction_set_slot,"fac_mordor",slot_faction_strength_tmp,":evil"),
      ]],



[anyone|plyr,"lord_talk",[    ### Ring Hunter Quest Completion - Lair Defeated.
 (this_or_next|eq, "$g_talk_troop","trp_dwarf_lord"),
 (eq, "$g_talk_troop","trp_imladris_lord"), 
 (check_quest_active,"qst_ring_hunters2"),
 (quest_slot_eq, "qst_ring_hunters2", slot_quest_current_state, 20)],
  "My lord, though I was unable to intercept the Ring Hunters terrorizing the villages, I was able to defeat their leaders in their lair. They had this in their possession.", "ring_hunter_lair_defeated_elf",
 []],

[anyone,"ring_hunter_lair_defeated_elf",
[],
  "I see, a ring, but not THE ring. Not even one of the great rings, yet not a mere trinket either. There is some power woven into it.", "ring_hunter_lair_defeated",
  []],

[anyone|plyr,"ring_hunter_lair_defeated",
  [],
  "Then we were right to snatch it from the Dark Lord’s fingers, before he could use it to spread his Shadow over the land and have it seep into the hearts of many.","ring_hunter_lair_defeated2",
  []],

[anyone,"ring_hunter_lair_defeated2",
  [],
    "You must keep this ring and use it to fight the Enemy and his armies. I trust you to use it well.", "ring_hunter_lair_quest_end",
  []],

[anyone|plyr,"ring_hunter_lair_quest_end",
  [],
    "This is an honour, my Lord, thank you! My heart will stay true and my arm strong.","close_window",
    [ (call_script,"script_increase_rank","$g_talk_troop_faction",20),
      (str_store_faction_name, s14, "$g_talk_troop_faction"),
      (add_xp_as_reward,500),
      (call_script,"script_end_quest","qst_ring_hunters2"),
      (faction_get_slot,":loss","fac_beorn",slot_faction_strength_tmp),
      (val_sub, ":loss", 50),
      (display_message,"@Beornings lose Faction strength when they were attacked.",color_bad_news),
      (faction_get_slot,":win","$g_talk_troop_faction",slot_faction_strength_tmp),
      (val_add, ":win", 150),
      (display_message,"@ {s14} gains faction strength as news of the Ring of Power spreads.",color_good_news),
      (faction_set_slot,"fac_beorn",slot_faction_strength_tmp,":loss"),
      (faction_set_slot,"$g_talk_troop_faction",slot_faction_strength_tmp,":win"),
    ]],

      
      


##Ring Hunter Party Combat
[anyone,"start",
  [(check_quest_active, "qst_ring_hunters"),
   (eq,"$g_encountered_party","$qst_ring_hunter_party"),
  ],
    "Look here, men. More lambs to the slaughter.","ring_hunters_party_attack",
  []],
[anyone|plyr,"ring_hunters_party_attack",
  [],
    "Your rampage has come to an end.","ring_hunters_party_attack_2",
  []],

[anyone,"ring_hunters_party_attack_2",
  [],
    "Check their packs and their fingers. Save one to torture. Everyone else is for eating!","close_window",
  [
   (quest_set_slot,"qst_ring_hunters",slot_quest_current_state,14),
   (encounter_attack),
   ]], 


## Ring Hunter Lair Party Defeat
[trp_ring_hunter_lt,"start",
  [],
    "That ring belongs to the Dark Lord! You can not have it!", "ring_hunter_lair_defeat",
  []],

[anyone|plyr,"ring_hunter_lair_defeat",
  [],
    "It belongs to me now.","ring_hunter_lair_defeat2",
  [ (store_random_in_range, ":ring", 1, 3),
    (try_begin),
      (eq,":ring",1),
      (troop_add_item,"trp_player","itm_ring_a_reward"),
    (else_try),
      (troop_add_item,"trp_player","itm_ring_b_reward"),
    (end_try)]
  ],

[anyone,"ring_hunter_lair_defeat2",
  [],
    "Do you think you’ve won a great victory? A pale tattered shade of one, perhaps. Bah! Our warband marched out long before you arrived. You are too late to save those they went after!","close_window",
  [   (call_script,"script_end_quest","qst_ring_hunters"),
      (setup_quest_text, "qst_ring_hunters2"),
      (str_store_string, s2, "@You must return and report back that you have defeated the Ring Hunter leaders and have taken a magical ring."),
      (call_script,"script_start_quest","qst_ring_hunters2","$qst_ring_hunter_lord"),
      (quest_set_slot,"qst_ring_hunters2",slot_quest_current_state,20),
      (call_script,"script_stand_back"),
      (disable_party,"p_ring_hunter_lair"),
      (call_script, "script_safe_remove_party","$qst_ring_hunter_party"),
      (assign, "$g_leave_encounter",1),
      (change_screen_return),
      ]],

[party_tpl|pt_beorn_messenger,"start",
  [(str_store_troop_name,s1,"$qst_ring_hunter_lord")],
    "My {lord/lady}, we received a warning from {s1} that a large outlaw warband was headed our way! Alas, there was no time to gather enough warriors. Having heard the sound of battle, we prepared for the worst!","beorn_message",
    []],
[anyone|plyr,"beorn_message",
  [],
    "That was no band of ordinary outlaws. They were the Dark Lord's worst of the worst, at least here in the North. Their leaders, however, were not here. Their den lies near Mirkwood Forest and I must make haste.","beorn_message2",
  []],
[anyone,"beorn_message2",
  [],
    "Yes, we were warned about the camp also and sent scouts towards it. We saw them burn it down and swiftly ride towards Mordor. If you chose to rush there first, you may not have been able to help us. We are truly grateful for your victory!","beorn_message_end",
    []],

[anyone|plyr,"beorn_message_end",
  [(str_store_troop_name,s1,"$qst_ring_hunter_lord")],
    "I must report back and tell {s1} about the battle. Go back to your village and dispatch scouts. There may be stragglers.","beorn_message_close",
    []],
[anyone,"beorn_message_close",
  [],
    "Yes, commander. We shall remain vigilant and send for more men from the distant hamlets. Your victory today has inspired us all.","close_window",     
  [(store_encountered_party, ":beorn_m"),
   (call_script,"script_stand_back"),
   (call_script,"script_increase_rank","$g_talk_troop_faction",55),
   (call_script,"script_end_quest","qst_ring_hunters"),
   (setup_quest_text, "qst_ring_hunters2"),
   (str_store_string, s2, "@You must return and report back that you have defeated the Ring Hunter party, but the leaders may have acquired what they were looking for."),
   (call_script,"script_start_quest","qst_ring_hunters2","$qst_ring_hunter_lord"),
   (quest_set_slot,"qst_ring_hunters2",slot_quest_current_state,10),
   (disable_party,"p_ring_hunter_lair"),
   (assign,"$g_leave_encounter",1),
   (change_screen_map),
   (call_script, "script_safe_remove_party",":beorn_m"),
  ]],

#### Kham Ring Hunters End  ###########

  
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
   "lord_give_troops_check",
   [
    (party_clear, "p_main_party_backup"),#GA: changed to exchange from whole party then return non-faction guys to player
    (assign, "$g_move_heroes", 0),
    (call_script, "script_party_add_party_companions", "p_main_party_backup", "p_main_party"), #keep this backup for later
    (party_get_num_companions, reg28, "p_main_party"), # reg28: initial main party size
    (call_script, "script_get_party_disband_cost", "p_main_party", 1),
    (assign, "$initial_party_value", reg0), # initial party total value
   ] +

#swy-- workaround a bug where the player would get stuck in the conversation menu with the barracks guy after donating some troops to his camp.
#   -- because the player insists on upgrading his troops inside the give_members screen, the before/after count doesn't match and none of the following dialog options kick. Boom, stuck.
#   -- what i've made is to make impossible for the player to upgrade his troops in here by returning a crazy amount of points/money in "script_game_get_upgrade_cost", so the button stays disabled.
#   -- more info: http://mbx.streetofeyes.com/index.php/topic,3465.msg68239.html#msg68239

  (is_a_wb_dialog
   and
  [
   (assign, "$tld_forbid_troop_upgrade_mode", 1),
   (change_screen_give_members),
  ]
   or
  [
   (change_screen_give_members)
  ])
  
# disabled in the next dialog -> lord_give_troops_check (already loaded when the give_members is accessed) -> lord_give_troops_check_1 (3 paths) -> lord_pretalk

],

[anyone,"lord_give_troops", [], "Unfortunately you don't have any {s14} soldiers to reinforce me with.", "lord_pretalk", []],

[anyone,"lord_give_troops_check", [], "Let me check the soldier roster...", "lord_give_troops_check_1", [] ],

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
                (try_begin),
                  (this_or_next|eq, ":item", "itm_orc_brew"),
                  (eq, ":item", "itm_lembas"),
                  (str_store_item_name, s31, ":item"),
                  (str_store_string, s20, "@{s31} (Consumable. Can be rebought)"),
                    ] + (is_a_wb_dialog and [
                  (else_try),
                  (neg|item_has_property, ":item", itp_unique),
                  (str_store_item_name, s31, ":item"),
                  (str_store_string, s20, "@{s31} (Can be rebought)"),
                    ] or []) + [ 
                (else_try),
                  (str_store_item_name, s20, ":item"),
                (try_end),
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
     (store_mul, ":relation_modifier", "$g_talk_troop_relation", ":price"), #lower price with relation
     (val_div, ":relation_modifier", 200),
     (val_sub, ":price", ":relation_modifier"),
	 (val_max, ":price", ":rank_index"),
     (ge, ":influence", ":price"), # player has enough influence to buy?
   
   
   # don't let player buy something which he cannot ride personally
   # (assign, ":cant_ride", 0),
   # (try_begin),
    # (item_get_type, ":it", ":item"),
    # (eq, ":it", itp_type_horse),
    # (call_script, "script_cf_troop_cant_ride_item","$g_player_troop",":item"), 
    # (assign, ":cant_ride", 1),
   # (try_end),
   # (neq,":cant_ride",1),
   
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
     (try_begin),
        (this_or_next|eq, ":item", "itm_lembas"),
        (this_or_next|eq, ":item", "itm_orc_brew"),
         ] + (is_a_wb_dialog and [
         (neg|item_has_property, ":item", itp_unique),
         ] or []) + [ 
        (item_set_slot, ":item", slot_item_given_as_reward, 0), # can't give more then one, except for those listed above - Kham
      (else_try),
        (item_set_slot, ":item", slot_item_given_as_reward, 1),
      (try_end),
     (call_script, "script_apply_attribute_bonuses"), # update player attributes for rings and such
     (call_script, "script_get_player_party_morale_values"),
     (val_add, ":recent_events_morale", reg0),
   (val_clamp, ":recent_events_morale", 0, 100), #GA overflow fixage 
     (party_set_morale, "p_main_party", ":recent_events_morale"), # update morale for cauldrons and such
	 #(call_script, "script_get_faction_rank", "$g_talk_troop_faction"),(assign, ":rank", reg0),
     (store_mul, ":price", ":rank_index", 5), # reward item price = 5*rank
     (store_mul, ":relation_modifier", "$g_talk_troop_relation", ":price"), #lower price with relation
     (val_div, ":relation_modifier", 200),
     (val_sub, ":price", ":relation_modifier"),
	 (val_max, ":price", ":rank_index"),
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
      (lt, ":rank", 8), #kham - reduced from 9
      (call_script, "script_get_rank_title_to_s24", "$g_talk_troop_faction"), (str_store_string_reg, s25, s24), #to s25 (current rank)
      (call_script, "script_get_any_rank_title_to_s24", "$g_talk_troop_faction", 8), #to s24 (highest rank) #kham - reduced from 9
   ], "I would hardly take advice if you are merely {s25}, {playername}. I would have been more inclined to listen if you were {s24}, but you are not.", "lord_pretalk",[]],
[anyone, "marshall_ask", [ #insufficient influence
     (assign, ":siege_command_cost", tld_command_cost_siege),
	 (store_mul, ":relation_modifier", "$g_talk_troop_relation", ":siege_command_cost"), #reduce influence cost with relation
	 (val_div, ":relation_modifier", 160),
	 (val_sub, ":siege_command_cost", ":relation_modifier"),
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
     (neg|faction_slot_ge, "$g_talk_troop_faction", slot_faction_strength, 3200), #Kham - Changed from fac_str_ok
     (call_script, "script_faction_strength_string_to_s23", "$g_talk_troop_faction"),     
   ], "We can hardly afford to meet the enemy head on, {playername}. We still need to build up our forces and become strong, alas we are merely {s23}.", "lord_pretalk",[]],
#[anyone, "marshall_ask", [ #busy campaigning - Kham: Removed this. If player is rank 8, they should make time for them (sept 18)
#     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_default), #not on campaign
#     (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_ai_state, sfai_gathering_army), #not gathering army
#   ], "We are on a campaign, {playername}, your advice would have to wait.", "lord_pretalk",[]],
[anyone, "marshall_ask", [], "I'm listening, {playername}. What do you suggest?", "marshall_suggest",[]],

#Suggest to attack besieged center ASAP - Kham
[anyone|plyr,"marshall_suggest", [
    (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_besieging_center),
    (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
    (party_slot_eq, ":ai_object", slot_center_is_besieged_by, "$g_talk_troop_party"),
    (str_store_party_name, s11, ":ai_object"),

    (assign, "$temp_action_cost", tld_command_cost_engage), #25,
	(store_mul, ":relation_modifier", "$g_talk_troop_relation", "$temp_action_cost"), #reduce influence cost with relation
	(val_div, ":relation_modifier", 160),
	(val_sub, "$temp_action_cost", ":relation_modifier"),
    (try_begin),
      (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
      (val_mul, "$temp_action_cost", 2),
      (val_div, "$temp_action_cost", 3), # 16 for tld_command_cost_engage=25
    (try_end),
    (assign, reg1, "$temp_action_cost"),
    (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
    (ge, reg2, "$temp_action_cost"),
  ],
 "Together, you and I can take {s11}. You should assault immediately... [Costs {reg1}/{reg2} influence]", "lord_give_order_assault",
[ (assign, "$tld_action_cost", tld_command_cost_engage),
  (try_begin),
    (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
    (val_mul, "$tld_action_cost", 2),
    (val_div, "$tld_action_cost", 3),
  (try_end)]],  

##Kham - Player initiated sieges BEGIN
[anyone|plyr, "marshall_suggest", [
  (try_begin),
    (eq, "$player_looks_like_an_orc",1),
    (str_store_string, s4, "@I wish to raze an enemy settlement to the ground."),
  (else_try),
    (str_store_string, s4, "@I wish to lead our men in an assault on an enemy settlement."),
  (try_end),
  ],
  "{s4}", "player_siege_ask",
  []],
##Kham - Player Initiated Sieges cont'd below

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

##Kham - Player initiated sieges CONTINUED

[anyone, "player_siege_ask", [
  (try_begin),
    (eq, "$player_looks_like_an_orc", 1),
    (str_store_string, s4, "@More snaga who will throw themselves at the enemy’s walls? Listen close and I might let you try."),
  (else_try),
    (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
    (str_store_string, s4, "@Indeed? Few men are so quick to volunteer to die on the battlements. There is much we must discuss before I can give you leave to go"),
  (else_try),
    (str_store_string, s4, "@Indeed? That is no small undertaking and there are matters which we must discuss before I can give you leave to go."),
  (try_end),
  ], 
    "{s4}", "player_siege_discuss",
  []],

[anyone|plyr, "player_siege_discuss", [],
  "I am listening, my Lord.", "player_siege_discuss_1",
  []],

[anyone, "player_siege_discuss_1", [
  (try_begin),
    (eq, "$player_looks_like_an_orc", 1),
    (str_store_string, s4, "@First, sieges are only an option for the strongest! Here is all that needs doing:"),
  (else_try),
    (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
    (str_store_string, s4, "@Here is all that needs doing:"),
  (else_try),
    (str_store_string, s4, "@Firstly, we must think to the hindrances of this task:"),
  (try_end),],
  "{s4}", "player_siege_discuss_1a",
  []],

[anyone, "player_siege_discuss_1a", [
  (store_add, reg3, tld_player_siege_resp_cost,0),
  (assign, ":siege_command_cost", tld_command_cost_siege),
  (store_mul, ":relation_modifier", "$g_talk_troop_relation", ":siege_command_cost"), #reduce influence cost with relation
  (val_div, ":relation_modifier", 160),
  (val_sub, ":siege_command_cost", ":relation_modifier"),
     (try_begin),
       (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
       (val_mul, ":siege_command_cost", 2),
       (val_div, ":siege_command_cost", 3), # 33 for tld_command_cost_siege=50
     (try_end),
     (assign, reg15, ":siege_command_cost"),
  (try_begin),
    (eq, "$player_looks_like_an_orc", 1),
    (str_store_string, s4, "@You need sharp weapons, fresh meat for your troops and wargs, wood to fuel the fires, and draughts to make the weaklings keep up. You also have to keep your scum in line or they’ll all kill each other before you’ve even got to the walls. We’re too busy with our own fights to take care of your lot — be prepared to provide what is needed to keep the maggots moving.^[requires {reg3} resources, {reg15} influence]"),
  (else_try),
    (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
    (str_store_string, s4, "@Steel must be kept sharp, men and horses fed, fires kept burning, water fetched, wounds tended — you and your men are no use to us if you can’t maintain your campaign. As we are spread too thin already to give you what is required, you must be prepared to provide what is needed to keep your army operational in a siege.^[requires {reg3} resources, {reg15} influence]"),
  (else_try),
    (str_store_string, s4, "@Steel must be kept sharp, soldiers and horses fed, fires kept burning, water fetched, wounds tended — a battle less glorious but no less important than the one you will fight on the ramparts. As we are spread too thin already to give you what is required, you must be prepared to provide what is needed to keep your army operational in a siege.^[requires {reg3} resources, {reg15} influence]"),
  (try_end),],
  "{s4}", "player_siege_discuss_2",
  []],

[anyone, "player_siege_discuss_2", [
  (try_begin),
    (eq, "$player_looks_like_an_orc", 1),
    (str_store_string, s4, "@Next, if you try to attack an enemy capital, I’ll stick you if you ain’t dead already.. We only march there when the Master commands it. You go where the enemy is weak and can be beaten."),
  (else_try),
    (str_store_string, s4, "@Secondly, you do not have permission to lead our people against an enemy capital. These places can only be overcome when the full strength of our forces stands united. You are to strike only where our foe has been weakened sufficiently that they would be defeated."),
  (try_end)],
  "{s4}", "player_siege_discuss_3",
  []],

[anyone, "player_siege_discuss_3", [
  (store_troop_faction,":fac", "$g_talk_troop"), 
  (str_store_faction_name, s2, ":fac"),
  (try_begin),
    (eq, "$player_looks_like_an_orc", 1),
    (str_store_string, s4, "@Third, {s2} is on its own campaign. We’ll fight with you if the pickings look good, but you better be strong enough to win on your own, or you won’t last long."),
  (else_try),
    (str_store_string, s4, "@Furthermore, you must know that {s2} is occupied with its own campaign. Our banners will follow you into battle if circumstance permits, but do not trust to hope — you may well be forced to stand alone."),
  (try_end)],
  "{s4}", "player_siege_discuss_4",
  []],

[anyone, "player_siege_discuss_4", [
  (call_script, "script_get_rank_title_to_s24", "$g_talk_troop_faction"), (str_store_string_reg, s25, s24), #to s25 (current rank)
  (store_troop_faction,":fac", "$g_talk_troop"), 
  (str_store_faction_name, s2, ":fac"),
  (try_begin),
    (eq, "$player_looks_like_an_orc", 1),
    (str_store_string, s4, "@Last, remember that as a {s25}, the Master has got no time for failure. You risk much for {s2} when you fight — bring us defeat and we’ll make sure you wish you’d never been born."),
  (else_try),
    (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
    (str_store_string, s4, "@Finally, remember that as a {s25}, you live and die by your successes and failures. You risk much for {s2} when you march into battle — bring ruin upon it and the consequences will be severe."),
  (else_try),
    (str_store_string, s4, "@Finally, remember that as a {s25}, you may bask in the glory of a victory hard-won and call that victory your own but all who dwell in {s2} will pay the price of your failure. You carry the fate of {s2} into battle with you — bring ruin upon it and the consequences will be severe."),
  (try_end),
  ],
  "{s4}", "player_siege_discuss_5",
  []],

[anyone, "player_siege_discuss_5", [
  (try_begin),
    (eq, "$player_looks_like_an_orc",1),
    (str_store_string, s4, "@Still think you can handle it?"),
  (else_try),
    (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
    (str_store_string, s4, "@Knowing what I have told you, do you still think yourself capable?"),
  (else_try),
    (str_store_string, s4, "@Knowing what I have told you, do you still wish to proceed?"),
  (try_end)],
  "{s4}", "player_siege_resource_check",
  []],


[anyone|plyr, "player_siege_resource_check", [
  (call_script,"script_update_respoint"),
  (faction_get_slot, ":rps", "$g_talk_troop_faction", slot_faction_respoint),
  (ge,":rps",tld_player_siege_resp_cost),
  (try_begin),
    (eq, "$player_looks_like_an_orc",1),
    (str_store_string, s4, "@Give me the banner of the Master!"),
  (else_try),
    (str_store_string, s4, "@Yes, my lord. Let me carry our banner into battle."),
  (try_end),
  ],
  "{s4}", "player_siege_check_passed",
  []],

[anyone|plyr, "player_siege_resource_check", [],
  "No, the time is not yet right.", "lord_pretalk",
  []],

[anyone, "player_siege_check_passed", [(store_troop_faction,":fac", "$g_talk_troop"), (str_store_faction_name, s2, ":fac")],
  "Very well. Go, {playername}, and march with the blessings of {s2}. We are counting on you to lead our people to victory.","player_siege_accept",
  [
  (call_script, "script_add_faction_rps", "$g_talk_troop_faction", -tld_player_siege_resp_cost),
  (assign, ":siege_command_cost", tld_command_cost_siege),
  (store_mul, ":relation_modifier", "$g_talk_troop_relation", ":siege_command_cost"), #reduce influence cost with relation
  (val_div, ":relation_modifier", 160),
  (val_sub, ":siege_command_cost", ":relation_modifier"),
     (try_begin),
       (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
       (val_mul, ":siege_command_cost", 2),
       (val_div, ":siege_command_cost", 3), # 33 for tld_command_cost_siege=50
     (try_end),
     (call_script, "script_spend_influence_of", ":siege_command_cost", "$g_talk_troop_faction"),
     (assign, "$player_allowed_siege",1)]],

[anyone|plyr, "player_siege_accept",[(store_troop_faction,":fac", "$g_talk_troop"), (str_store_faction_name, s2, ":fac")],
  "Thank you, my Lord. I will not let you and {s2} down.", "close_window",
  []],

[anyone, "marshall_answer", [],
   "Very well, {playername}, I shall defer to your judgement. I shall send messengers to gather our forces.^Follow me and stay close - we ride to {s4}!", "close_window",
   [
     (assign, ":siege_target", "$temp"),
     #faction AI
     (faction_set_slot, "$g_talk_troop_faction", slot_faction_ai_state, sfai_attacking_center),
     (faction_set_slot, "$g_talk_troop_faction", slot_faction_ai_object, ":siege_target"),
     (store_current_hours, ":cur_hours"),
     (val_add, ":cur_hours", 72), #72 hours no AI recalc
     (faction_set_slot, "$g_talk_troop_faction", slot_faction_scripted_until, ":cur_hours"),
     
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
	 (store_mul, ":relation_modifier", "$g_talk_troop_relation", ":siege_command_cost"), #reduce influence cost with relation
	 (val_div, ":relation_modifier", 160),
	 (val_sub, ":siege_command_cost", ":relation_modifier"),
     (try_begin),
       (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
       (val_mul, ":siege_command_cost", 2),
       (val_div, ":siege_command_cost", 3), # 33 for tld_command_cost_siege=50
     (try_end),
     (call_script, "script_spend_influence_of", ":siege_command_cost", "$g_talk_troop_faction"),

     (str_store_party_name, s4, ":siege_target"),    
	 (call_script,"script_stand_back"),(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1),
   ]],

# TLD: Accept a delivered gift (CppCoder)
# TODO: Add dialog for evil characters, this is currently only for good players.

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
  (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"), #must be a king
  (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),  
  (quest_slot_eq|neg, "qst_deliver_gift", slot_quest_target_faction, "$g_talk_troop_faction"), # can't ask to deliver a gift from the faction you are giving a gift to.
  (quest_get_slot, ":days_remaining", "qst_deliver_gift", slot_quest_dont_give_again_remaining_days),
  (this_or_next|eq, cheat_switch, 1), # (CppCoder): Always available while debugging.
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
], "{s1}", "send_gift_3",[(store_repeat_object, "$temp")]],

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
  (call_script,"script_update_respoint"),
  (faction_get_slot,  ":rps", "$g_talk_troop_faction", slot_faction_respoint),
  (ge,":rps",reg14), # Player must be able to afford gift...
  (str_store_string, s1, "@{s2} [{reg14} Resource Points]"),  
], "{s1}", "send_gift_5",[(store_repeat_object, "$temp_2")]],

[anyone|plyr,"send_gift_4",[], "Nevermind.", "lord_pretalk",[]],

[anyone,"send_gift_5",[], "All right {playername}. Good Luck.", "lord_pretalk",
[
      (store_add, ":target_faction", "$temp", kingdoms_begin),
      (assign, ":gift_no", "$temp_2"),
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
  (quest_set_slot, "qst_deliver_gift", slot_quest_giver_troop, "$g_talk_troop"),
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
	 (store_mul, ":relation_modifier", "$g_talk_troop_relation", ":min_command_cost"), #reduce influence cost with relation
	 (val_div, ":relation_modifier", 130),
	 (val_sub, ":min_command_cost", ":relation_modifier"),
     (try_begin),
       (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
       (val_mul, ":min_command_cost", 2),
       (val_div, ":min_command_cost", 3), # min_command_cost is 3 now (for tld_command_cost_goto=5)
     (try_end),
     (ge, ":influence", ":min_command_cost"), #the lowest cost among the actions below
	 (call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (store_mul, ":condition", reg0, 10), # InVain: Removed trait check below, instead add relation+rank condition
	 (val_add, ":condition", "$g_talk_troop_relation"), 	
	 (ge, ":condition", 50),
	 
     # check if traits are needed 
     # (assign, ":trait_check_passed", 1),
     # (try_begin),
       # (eq, "$g_talk_troop_faction", "fac_gondor"),
       # (troop_slot_eq, "trp_traits", slot_trait_gondor_friend, 0),
       # (assign, ":trait_check_passed", 0),
     # (try_end),
     # (try_begin),
       # (eq, "$g_talk_troop_faction", "fac_rohan"),
       # (troop_slot_eq, "trp_traits", slot_trait_rohan_friend, 0),
       # (assign, ":trait_check_passed", 0),
     # (try_end),
     # (try_begin),
       # (this_or_next|eq, "$g_talk_troop_faction", "fac_lorien"),
       # (this_or_next|eq, "$g_talk_troop_faction", "fac_imladris"),
       # (eq, "$g_talk_troop_faction", "fac_woodelf"),
       # (troop_slot_eq, "trp_traits", slot_trait_elf_friend, 0),
       # (assign, ":trait_check_passed", 0),
     # (try_end),
     # (eq, ":trait_check_passed", 1),
   ],
"I have a new task for you.", "lord_give_order_ask",[]],

[anyone,"lord_give_order_ask", [], "Yes?", "lord_give_order",[]],


[anyone|plyr,"lord_give_order", [
    (assign, "$temp_action_cost", tld_command_cost_follow),
	(store_mul, ":relation_modifier", "$g_talk_troop_relation", "$temp_action_cost"), #reduce influence cost with relation
	 (val_div, ":relation_modifier", 130),
	 (val_sub, "$temp_action_cost", ":relation_modifier"),
    (try_begin),
      (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
      (val_mul, "$temp_action_cost", 2),
      (val_div, "$temp_action_cost", 3), # 13 for tld_command_cost_follow=20
    (try_end),
    (assign, reg1, "$temp_action_cost"),
    (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
    (ge, reg2, "$temp_action_cost"),
	(call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (store_mul, ":condition", reg0, 10), # InVain: add relation+rank condition
	(val_add, ":condition", "$g_talk_troop_relation"), 	
	(ge, ":condition", 50)], 
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
	(store_mul, ":relation_modifier", "$g_talk_troop_relation", "$temp_action_cost"), #reduce influence cost with relation
	 (val_div, ":relation_modifier", 130),
	 (val_sub, "$temp_action_cost", ":relation_modifier"),
    (try_begin),
      (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
      (val_mul, "$temp_action_cost", 2),
      (val_div, "$temp_action_cost", 3), # 3 for tld_command_cost_goto=5
    (try_end),
    (assign, reg1, "$temp_action_cost"),
    (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
    (ge, reg2, "$temp_action_cost"),
	(call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (store_mul, ":condition", reg0, 10), # InVain: add relation+rank condition
	(val_add, ":condition", "$g_talk_troop_relation"), 	
	(ge, ":condition", 70)], 
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
	(store_mul, ":relation_modifier", "$g_talk_troop_relation", "$temp_action_cost"), #reduce influence cost with relation
	 (val_div, ":relation_modifier", 130),
	 (val_sub, "$temp_action_cost", ":relation_modifier"),
    (try_begin),
      (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
      (val_mul, "$temp_action_cost", 2),
      (val_div, "$temp_action_cost", 3), # 6 for tld_command_cost_patrol=10
    (try_end),
    (assign, reg1, "$temp_action_cost"),
    (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
    (ge, reg2, "$temp_action_cost"),
	(call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (store_mul, ":condition", reg0, 10), # InVain: add relation+rank condition
	(val_add, ":condition", "$g_talk_troop_relation"), 	
	(ge, ":condition", 60)],  
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
	(store_mul, ":relation_modifier", "$g_talk_troop_relation", "$temp_action_cost"), #reduce influence cost with relation
	 (val_div, ":relation_modifier", 130),
	 (val_sub, "$temp_action_cost", ":relation_modifier"),
    (try_begin),
      (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
      (val_mul, "$temp_action_cost", 2),
      (val_div, "$temp_action_cost", 3), # 16 for tld_command_cost_engage=25
    (try_end),
    (assign, reg1, "$temp_action_cost"),
    (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
    (ge, reg2, "$temp_action_cost"),
	(call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (store_mul, ":condition", reg0, 10), # InVain: add relation+rank condition
	(val_add, ":condition", "$g_talk_troop_relation"), 	
	(ge, ":condition", 80)], 
"Engage enemies around... [Costs {reg1}/{reg2} influence]", "lord_give_order_details_ask",[
     (assign, "$temp", spai_raiding_around_center), #not really, changed later to spai_patrolling_around_center
     (assign, "$tld_action_cost", tld_command_cost_engage),
     (try_begin),
  (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
  (val_mul, "$tld_action_cost", 2),
  (val_div, "$tld_action_cost", 3),
     (try_end)]],

#Suggest to attack besieged center ASAP - Kham
[anyone|plyr,"lord_give_order", [
    (party_slot_eq, "$g_talk_troop_party", slot_party_ai_state, spai_besieging_center),
    (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
    (party_slot_eq, ":ai_object", slot_center_is_besieged_by, "$g_talk_troop_party"),
    (str_store_party_name, s11, ":ai_object"),

    (assign, "$temp_action_cost", tld_command_cost_engage), #25,
	(store_mul, ":relation_modifier", "$g_talk_troop_relation", "$temp_action_cost"), #reduce influence cost with relation
	(val_div, ":relation_modifier", 160),
	(val_sub, "$temp_action_cost", ":relation_modifier"),
    (try_begin),
      (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
      (val_mul, "$temp_action_cost", 2),
      (val_div, "$temp_action_cost", 3), # 16 for tld_command_cost_engage=25
    (try_end),
    (assign, reg1, "$temp_action_cost"),
    (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
    (ge, reg2, "$temp_action_cost"),
  ],
 "Together, you and I can take {s11}. You should assault immediately... [Costs {reg1}/{reg2} influence]", "lord_give_order_assault",
[ (assign, "$tld_action_cost", tld_command_cost_engage),
  (try_begin),
    (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
    (val_mul, "$tld_action_cost", 2),
    (val_div, "$tld_action_cost", 3),
  (try_end)]],   
  
[anyone,"lord_give_order_assault", [
  (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
  (party_get_slot, ":besieging_party", ":ai_object", slot_center_is_besieged_by),
  (neq, ":besieging_party", "$g_talk_troop_party"),
  (party_stack_get_troop_id, ":siege_commander", ":besieging_party", 0),
  (str_store_troop_name, s4, ":siege_commander"),
  ],
 "{s4} is directing this siege. I suggest you speak to them.", "lord_pretalk",
[]],

[anyone,"lord_give_order_assault", [
  (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
  (party_get_slot, ":siege_begun", ":ai_object", slot_center_siege_begin_hours),
  (store_current_hours, ":cur_hour"),
  (store_sub, ":hours_of_siege", ":cur_hour", ":siege_begun"),
  
  (try_begin),
    (assign, ":hours_required", 6),
  (try_end),
  (val_sub, ":hours_required", ":hours_of_siege"),
  (gt, ":hours_required", 0),
  (try_begin),
    (gt, ":hours_required", 1),
    (assign, reg3, ":hours_required"),
    (str_store_string, s11, "@{reg3} hours."),
  (else_try),
    (str_store_string, s11, "@hour."),
  (try_end),
  ],
   "Our preparations are not yet ready. We need another {s11}", "lord_pretalk",
[]],

[anyone,"lord_give_order_assault", [
  ],
   "Very well -- Attack the walls!", "close_window",
  [
  (party_get_slot, ":ai_object", "$g_talk_troop_party", slot_party_ai_object),
  (call_script, "script_begin_assault_on_center", ":ai_object"),

  (assign, "$g_leave_encounter", 1),
  (call_script,"script_stand_back"),
  (store_current_hours, ":cur_time"),
  (store_add, ":obey_until_time", ":cur_time", 5*24), # commands last 5 days
  (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
  (party_set_slot, ":party_no", slot_party_follow_player_until_time, ":obey_until_time"), #no lord ai changes until this time
  (store_mul, ":relation_modifier", "$g_talk_troop_relation", "$tld_action_cost"), #reduce influence cost with relation
  (val_div, ":relation_modifier", 160),
  (val_sub, "$tld_action_cost", ":relation_modifier"),
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
  (val_add, "$trait_check_commands_issued", 1),
]],
   

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
	 (store_mul, ":relation_modifier", "$g_talk_troop_relation", "$tld_action_cost"), #reduce influence cost with relation
	 (val_div, ":relation_modifier", 130),
	 (val_sub, "$tld_action_cost", ":relation_modifier"),
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
     # (assign, "$g_recalculate_ais", 2)]],

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
     # (assign, "$g_recalculate_ais", 2)]],

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

#Active quests
##### TODO: QUESTS COMMENT OUT BEGIN

## Kham - Defeat Target Lord Quest Init Start

[anyone,"lord_tell_mission", [
  (eq,"$random_quest_no","qst_blank_quest_06"),
  (quest_get_slot, ":quest_target_troop", "qst_blank_quest_06", slot_quest_target_troop),
  (str_store_troop_name, s7, ":quest_target_troop"),
  (str_store_faction_name, s8, ":quest_target_troop"),
  (try_begin),
    (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
    (str_store_string, s5, "@{playername}, you may have seen the hosts of {s7}. Of all the captains arrayed against us, at present {s7} of {s8} has won the greatest renown. Their mere presence on the field is enough to embolden our enemies and weaken the resolve of our allies. {playername}, if you wish to do a great deed in this war, strike down the host of {s7} in open battle, in sight of all! Thus may hope be rekindled, and dread fill the hearts of those who would come against us."),
  (else_try),
    (str_store_string, s5, "@Do you mark how our bravest fighters falter at the mere mention of {s7} of {s8}? A great warrior, oh yes, a capable captain. We cannot allow that to run amok like this! Everywhere their face is shown, our lines bend back, and our foes find new courage. This cannot be. I command that you, {playername}, challenge and defeat the soldiers of {s7} in open battle. To see {s7} struck down by you will freeze the blood and marrow of his followers, and show our own troops that our enemies can be thrown down!"),
  (try_end),],
 "{s5}", "lord_mission_told_target_lord",[]],


[anyone|plyr,"lord_mission_told_target_lord", [
(eq,"$random_quest_no","qst_blank_quest_06"),
(try_begin),
  (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
  (str_store_string, s5, "@This is a chance for me to show my quality. I shall defeat {s7} in the sight of enemy and ally alike."),
(else_try),
  (str_store_string, s5, "@Accursed be those who follow {s7} this day, for I shall strike them down for all to see!."),
(try_end),],
"{s5}", "lord_mission_accepted",[
      (quest_get_slot, ":quest_target_troop", "qst_blank_quest_06", slot_quest_target_troop),
      (str_store_troop_name, s35, ":quest_target_troop"),
      (str_store_faction_name, s36, ":quest_target_troop"),
      (str_store_troop_name_link, s9, "$g_talk_troop"),
      (str_store_string, s10, "@{s9} wants you to defeat {s35} of {s36} in battle."),
      (setup_quest_text,"$random_quest_no"),
      (str_store_string, s2, "@{s10}")]],

[anyone|plyr,"lord_mission_told_target_lord", [
(eq,"$random_quest_no","qst_blank_quest_06"),
(try_begin),
  (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
  (str_store_string, s6, "@I humbly ask that you find another for this task. I do not think I could best {s7} in battle."),
(else_try),
  (str_store_string, s6, "@Mercy, I crave! To face {s7} in open battle is sheer folly! I cannot do this thing!"),
(try_end),
],
"{s6}.", "lord_mission_rejected",[]],


## Kham Kill Quest INIT START
[anyone,"lord_tell_mission", [
  (eq,"$random_quest_no","qst_blank_quest_04"),
  #(quest_get_slot, ":quest_target_troop", "qst_blank_quest_04", slot_quest_target_troop),
  (quest_get_slot, ":quest_target_faction", "qst_blank_quest_04", slot_quest_target_faction),
  (quest_get_slot, ":quest_target_troop_type", "qst_blank_quest_04", slot_quest_target_party_template), #Troop Type (1 or 2)
  (quest_get_slot, reg22, "qst_blank_quest_04", slot_quest_target_amount),
  #(str_store_troop_name_plural, s6, ":quest_target_troop"),
  (str_store_faction_name, s7, ":quest_target_faction"),
  (try_begin),
    (eq, ":quest_target_troop_type", 1),
    (str_store_string, s6, "@strong warriors from {s7}"),
  (else_try),
    (str_store_string, s6, "@champions from {s7}, the strongest in the field"),
  (try_end),
  (try_begin),
    (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
    (str_store_string, s5, "@{playername}, the men have heard stories about fierce enemy troops. Stories of these terrors are demoralizing the men. I want you to show the men that they have nothing to fear. I want you to challenge and defeat {reg22} {s6}."),
  (else_try),
    (str_store_string, s5, "@{playername}, I want you to show the men that enemy troops are of no consequence. I want you to personally slay {reg22} {s6}! Do this to show we are the superior force!"),
  (try_end),],
 "{s5}", "lord_mission_told_kill_quest_targeted",[]],

[anyone|plyr,"lord_mission_told_kill_quest_targeted", [
(eq,"$random_quest_no","qst_blank_quest_04"),
(str_store_string, s7, "@I will do what you asked, and the men will witness."),],
"{s7}", "lord_mission_accepted",[
      #(quest_get_slot, ":quest_target_troop", "qst_blank_quest_04", slot_quest_target_troop),
      (quest_get_slot, ":quest_target_faction", "qst_blank_quest_04", slot_quest_target_faction),
      (quest_get_slot, ":quest_target_troop_type", "qst_blank_quest_04", slot_quest_target_party_template), #Troop Type (1 or 2)
      (quest_get_slot, reg22, "qst_blank_quest_04", slot_quest_target_amount),

      #(str_store_troop_name_plural, s6, ":quest_target_troop"),
      (str_store_troop_name_link, s9, "$g_talk_troop"),
      (try_begin),
        (eq, ":quest_target_troop_type", 1),
        (str_store_string, s6, "@high level troops from"),
      (else_try),
        (str_store_string, s6, "@elite level troops from"),
      (try_end),
      (str_store_faction_name, s7, ":quest_target_faction"),
      (str_store_string, s8, "@{s9} wants you to personally defeat {reg22} {s6} {s7}."),
      #(str_store_troop_name_plural, s36, ":quest_target_troop"),
      (str_store_string, s35, "@{reg22}"),
      (setup_quest_text,"$random_quest_no"),
      (str_store_string, s2, "@{s8}")]],

[anyone,"lord_tell_mission", [
  (eq,"$random_quest_no","qst_blank_quest_05"),
  (quest_get_slot, ":quest_target_faction", "qst_blank_quest_05", slot_quest_target_faction),
  (quest_get_slot, reg22, "qst_blank_quest_05", slot_quest_target_amount),
  (str_store_faction_name, s7, ":quest_target_faction"),
  (store_character_level, ":player_level", "trp_player"),
  (try_begin),
    (gt, ":player_level", 20),
    (str_store_string, s6, "@I want you to personally slay"),
  (else_try),
    (str_store_string, s6, "@I want you and your men to kill"),
  (try_end),
  (str_store_string, s5, "@{playername}, you need to earn my respect and that of your men. {s6} {reg22} {s7} troops!")],
 "{s5}", "lord_mission_told_kill_quest_faction",[]],

[anyone|plyr,"lord_mission_told_kill_quest_faction", [
(eq,"$random_quest_no","qst_blank_quest_05"),
(str_store_string, s7, "@I will do what you asked, and the men will witness."),],
"{s7}", "lord_mission_accepted",[
      (quest_get_slot, ":quest_target_faction", "qst_blank_quest_05", slot_quest_target_faction),
      (quest_get_slot, reg22, "qst_blank_quest_05", slot_quest_target_amount),
      (str_store_faction_name, s6, ":quest_target_faction"),
      (str_store_troop_name_link, s9, "$g_talk_troop"),
      (store_character_level, ":player_level", "trp_player"),
      (try_begin),
        (gt, ":player_level", 20),
        (str_store_string, s7, "@{s9} wants you to personally kill {reg22} {s6} troops."),
      (else_try),
        (str_store_string, s7, "@{s9} wants you and your men to kill {reg22} {s6} troops."),
      (try_end),
      (str_store_faction_name, s36, ":quest_target_faction"),
      (str_store_string, s35, "@{reg22}"),
      (setup_quest_text,"$random_quest_no"),
      (str_store_string, s2, "@{s7}")]],


[anyone|plyr,"lord_mission_told_kill_quest_targeted", [
(eq,"$random_quest_no","qst_blank_quest_04"),
],
"I cannot do this now.", "lord_mission_rejected",[]],

[anyone|plyr,"lord_mission_told_kill_quest_faction", [
(eq,"$random_quest_no","qst_blank_quest_05"),
],
"I cannot do this now.", "lord_mission_rejected",[]],
# Kill Quest END

## Kham Sea Battle INIT START
[anyone,"lord_tell_mission", [
  (eq,"$random_quest_no","qst_blank_quest_03"),
  (quest_get_slot, ":quest_target_center", "qst_blank_quest_03", slot_quest_target_center),
  (quest_get_slot, ":quest_object_center", "qst_blank_quest_03", slot_quest_object_center),
  (str_store_party_name, s6, ":quest_target_center"),
  (str_store_party_name, s7, ":quest_object_center"),
  (try_begin),
    (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
    (try_begin), #South Good
      (eq, "$g_talk_troop_faction", "fac_gondor"),
      (str_store_string, s5, "@{playername}, we have received grim tidings. The Corsairs of Umbar grow ever bolder, and even as we speak, a fleet gathers not far from {s6}. Already they reave along the coastline, and soon they shall be upon the city itself.^^ We must intercept the fleet before it reaches the city. Hasten to {s6}, and speak to the local authorities."),
    (else_try),
      (str_store_string, s5, "@{playername}, we have received grim tidings. The savages of Rhûn have more cunning and boldness than we thought - unseen by our scouts, they have built a sufficiency of boats and rafts to carry them across the Long Lake, and they are striking directly at Esgaroth!^^ We must intercept the fleet before it reaches the city. Lead your troops there as swiftly as you can, and drive the barbarians back across the water!"),
    (try_end),
  (else_try),
    (try_begin),
      (eq, "$g_talk_troop_faction", "fac_umbar"), #South Evil
      (str_store_string, s5, "@If you seek pillage and plunder, here is a matchless opportunity, {playername}.^^ A Corsair fleet is launching from the port at {s7}, and will set a course straight for {s6}, which is ripe for the plucking! Join them in their assault, and share in the spoils!"),
    (else_try),
      (str_store_string, s5, "@The soft weaklings of Esgaroth are no match for our swift horsemen and ferocious warriors, {playername}. This is known. The Lake-men believe themselves safe, across the water from us, but we shall soon show them otherwise!^^ We have made boats, and rafts, good enough to carry our warriors straight across the lake. They won't be expecting us! ^^Go to the Main Camp, and speak to the camp commander if you wish to join the assault."),
    (try_end),
  (try_end)],
 "{s5}", "lord_mission_told_sea_battle",[
    (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
    (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
    (str_store_troop_name_link, s9, "$g_talk_troop"),
    (str_store_party_name_link, s3, ":quest_target_center"),
    (str_store_party_name_link, s4, ":quest_object_center"),
    (try_begin),
      (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
      (try_begin), #South Good
        (eq, "$g_talk_troop_faction", "fac_gondor"),
        (str_store_string, s7, "@{s9} asked you to help defend {s3} against a Corsair raid. Hasten to the city, speak to the guild master, and lend your aid to the local garrison."),
      (else_try),
        (str_store_string, s7, "@{s9} asked you to help defend Esgaroth against a naval incursion, of all things, made by Rhûn. Hasten to the Lake-town, speak to the guild master, and lend your aid to the local garrison."),
      (try_end),
    (else_try),
      (try_begin),
        (eq, "$g_talk_troop_faction", "fac_umbar"), #South Evil
        (str_store_string, s7, "@{s9} offered you an opportunity to join a naval raid against {s3}. Make your way to {s4}, speak to the camp commander, and join the assault."),
      (else_try),
        (str_store_string, s7, "@{s9} offered you an opportunity to join a naval raid against Esgaroth. Make your way to {s4}, speak to the camp commander, and join the assault."),
      (try_end),
    (try_end),
    (setup_quest_text,"$random_quest_no"),
    (str_store_string, s2, "@{s7}")]],

[anyone|plyr,"lord_mission_told_sea_battle", [
(eq,"$random_quest_no","qst_blank_quest_03"),
(try_begin),
    (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
    (try_begin), #South Good
      (eq, "$g_talk_troop_faction", "fac_gondor"),
      (str_store_string, s5, "@We will go as swiftly as we may, and pray we are not too late."),
    (else_try),
      (str_store_string, s5, "@We will go as swiftly as we may, and pray we are not too late."),
    (try_end),
  (else_try),
    (try_begin),
      (eq, "$g_talk_troop_faction", "fac_umbar"), #South Evil
      (str_store_string, s5, "@We shall plunder their port and seize their riches for ourselves!"),
    (else_try),
      (str_store_string, s5, "@We shall plunder the Lake Town and seize their riches for ourselves!"),
    (try_end),
  (try_end)],
"{s5}", "lord_mission_accepted",[]],

[anyone|plyr,"lord_mission_told_sea_battle", [
(eq,"$random_quest_no","qst_blank_quest_03"),
(try_begin),
    (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
    (try_begin), #South Good
      (eq, "$g_talk_troop_faction", "fac_gondor"),
      (str_store_string, s5, "@I'm sorry, but we cannot aid them now."),
    (else_try),
      (str_store_string, s5, "@I'm sorry, but we cannot aid them now."),
    (try_end),
  (else_try),
    (try_begin),
      (eq, "$g_talk_troop_faction", "fac_umbar"), #South Evil
      (str_store_string, s5, "@Bah! Far more glory to be won elsewhere than with paltry piracy."),
    (else_try),
      (str_store_string, s5, "@This raid does not interest me. I shall win glory elsewhere."),
    (try_end),
  (try_end)],
"{s5}", "lord_mission_rejected",[]],
## Sea Battle INIT END

#### Kham Destroy Scout Camp Quests Start ####


[anyone,"lord_tell_mission", [
  (eq,"$random_quest_no","qst_destroy_scout_camp"),
  (quest_get_slot, ":target_center", "qst_destroy_scout_camp", slot_quest_target_center),
  (store_faction_of_party, ":fac",":target_center"),
  (str_store_faction_name, s3, ":fac")],
    "{playername}, we have received word that {s3} has a scout camp nearby, Make sure you are not seen and destroy it before they learn about our plans.", "lord_mission_destroy_scout_camp_a",
[]],

[anyone|plyr,"lord_mission_destroy_scout_camp_a", [],
    "Consider it done.", "lord_mission_destroy_scout_camp_accept",
[]],

[anyone|plyr,"lord_mission_destroy_scout_camp_a", [],
    "I do not have the time for this.", "lord_mission_destroy_scout_camp_reject",
[]],


[anyone,"lord_mission_destroy_scout_camp_accept",[],
  "We shall await news of your success.","close_window",
      [
      #(quest_get_slot, ":quest_target_party_template", "$random_quest_no", slot_quest_target_party_template),
      #(quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
      #(assign, ":terrain_check", 0), # Check if spawned camp is not in weird terrain
      #(try_for_range_backwards, ":tries_left", 0, 10),
      #  (eq, ":terrain_check",0),
      #  (set_spawn_radius, 15),
      #  (spawn_around_party,"$g_encountered_party",":quest_target_party_template"),
      #  (try_begin),
      #    (party_get_current_terrain, ":terrain_type", reg0),
      #    (assign, "$qst_destroy_scout_camp_party", reg0),
      #    (neq, ":terrain_type", rt_water),
      #    (neq, ":terrain_type", rt_mountain),
      #    (neq, ":terrain_type", rt_river),
      #    (assign, ":terrain_check", 1),
      #  (else_try),
      #    (gt,":tries_left",0), #last ditch effort, if 10 iterations of the above doesnt work, just spawn it, and hope for the best
      #    (call_script, "script_safe_remove_party", reg0),
      #  (try_end),
      #(try_end),
      (call_script, "script_get_region_of_party", "$qst_destroy_scout_camp_party"),
      (store_add, reg2, str_shortname_region_begin , reg1),
      (try_begin),
        (ge, reg1, region_rhun),
        (store_sub, reg2, reg1, region_rhun),
        (val_add, reg2, str_shortname_region_begin_new),
      (try_end),
      (str_store_string,s1,reg2),
      (quest_get_slot, reg3, "$random_quest_no", slot_quest_expiration_days),
      (str_store_troop_name_link,s9,"$g_talk_troop"),
      (setup_quest_text,"$random_quest_no"),
      (str_store_string, s2, "@{s9} asked you to destroy a scout camp near {s1}."),
      (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
      (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
      (call_script, "script_stand_back"),
      (assign, "$g_leave_encounter", 1),
      ]],

[anyone,"lord_mission_destroy_scout_camp_reject", [],
    "I see. That is disappointing.", "close_window",
[(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    (try_begin),
      (quest_slot_eq, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 0),
      (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 7),
    (try_end),
 (call_script,"script_safe_remove_party","$qst_destroy_scout_camp_party"),
 (call_script, "script_stand_back"),
 (assign, "$g_leave_encounter", 1),
]],


#### Kham Destroy Scout Camp Quest End #######

#### Kham Defend / Raid Village Quests Start ########
#### Kham Defend Village - Good Start


[anyone,"lord_tell_mission", [
  (eq,"$random_quest_no","qst_defend_village"),
  (quest_get_slot, ":quest_object_center", "qst_defend_village", slot_quest_object_center),
  (str_store_party_name,12,":quest_object_center")],
    "{playername}, we have received reports from our scouts that a raiding party is on its way to a village near {s12}.", "lord_mission_defend_village_a",
[]],

[anyone|plyr,"lord_mission_defend_village_a", [],
    "Are you able to send men?", "lord_mission_defend_village_b",
[]],


[anyone,"lord_mission_defend_village_b",
[],
    "We can, but it will take time to mobilize. We fear that we may be too late when we do. ^^You and your men seem able to ride out quickly. Can you defend this village?", "lord_mission_defend_question",
[]],

[anyone|plyr,"lord_mission_defend_question",[
  (party_get_num_companions, ":party_size", "p_main_party"),(ge, ":party_size", 10),],
    "My men and I are ready. We shall ride out at once.", "lord_mission_defend_accept",
  []],

[anyone|plyr,"lord_mission_defend_question",
[],
  "I am afraid I may not have enough men with me currently...", "lord_mission_defend_reject",[
  (display_message, "@Your party must be at least 10 strong to begin this quest", color_neutral_news),
]],


[anyone|plyr,"lord_mission_defend_question",
[],
    "I am afraid I cannot do this task.", "lord_mission_defend_reject",
[]],

[anyone,"lord_mission_defend_accept", [],
  "Thank you, {playername}. Now go, quickly!","close_window",[
      (quest_get_slot, ":quest_giver_center", "$random_quest_no", slot_quest_giver_center),
      (quest_get_slot, ":quest_target_party_template", "$random_quest_no", slot_quest_target_party_template),
      (set_spawn_radius, 10),
      (spawn_around_party,":quest_giver_center",":quest_target_party_template"),
      (assign, "$qst_defend_village_party", reg0),
      (str_store_party_name, s1, ":quest_giver_center"),
      (quest_get_slot, reg3, "$random_quest_no", slot_quest_expiration_days),
      (str_store_troop_name_link,s9,"$g_talk_troop"),
      (setup_quest_text,"$random_quest_no"),
      (str_store_string, s2, "@{s9} asked you to defend a village under attack near {s1}."),
      (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
      (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
      (call_script, "script_stand_back"),
      (assign, "$g_leave_encounter", 1),
      ]],

[anyone,"lord_mission_defend_reject",
  [],
    "I see. Then I will send what troops I can. Let us hope we are not too late.", "close_window",
  [
    (try_begin),
      (quest_slot_eq, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 0),
      (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 7),
    (try_end),
   (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
   (call_script, "script_stand_back"),
   (assign, "$g_leave_encounter", 1),]
],

##### Kham Defend Village End
##### Kham Raid Village Start


[anyone,"lord_tell_mission", [
  (eq,"$random_quest_no","qst_raid_village"),
  (quest_get_slot, ":raid_village_faction", "qst_raid_village", slot_quest_target_faction),
  (try_begin), ## Elves are not likely to be guarding villages. Make an exception
    (this_or_next|eq,":raid_village_faction", "fac_imladris"),
    (this_or_next|eq,":raid_village_faction", "fac_lorien"),
    (this_or_next|eq,":raid_village_faction", "fac_woodelf"),
    (neg|is_between, ":raid_village_faction", kingdoms_begin, kingdoms_end), ## For some reason, the search counts 'ruins' etc. This takes them out! 
    (assign,":raid_village_faction", "fac_rohan"), ## Rohan is the closest to areas where elves would mostly be.
  (try_end),
  (str_store_faction_name,s3,":raid_village_faction")],
    "{playername}, there is a village nearby that is ripe for the picking. Our scouts tell us that they are protected by {s3}, but they are few and can easily be defeated. ^^You happen to be the first commander I have told. What do you want to do with this information?", "lord_mission_raid_village_a",
[]],

[anyone|plyr,"lord_mission_raid_village_a", [
  (party_get_num_companions, ":party_size", "p_main_party"),(ge, ":party_size", 10),
 ],
    "I will raid that village, kill every man we see, and enslave all women and children!", "lord_raid_village_accept",
[]],


[anyone|plyr,"lord_mission_raid_village_a",
[],
  "I cannot raid with these weaklings with me right now...", "lord_raid_village_reject",[
  (display_message, "@Your party must be at least 10 strong to begin this quest", color_neutral_news),
]],


[anyone|plyr,"lord_mission_raid_village_a", [],
    "I do not have the time to raid puny villages!", "lord_raid_village_reject",
[]],


[anyone,"lord_raid_village_accept",[],
  "Then what are you doing standing around here?","close_window",
      [
      (quest_get_slot, ":quest_target_party_template", "$random_quest_no", slot_quest_target_party_template),
      (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
      (set_spawn_radius, 15),
      (spawn_around_party,":quest_target_center",":quest_target_party_template"),
      (assign, "$qst_raid_village_party", reg0),
      (str_store_party_name, s1, ":quest_target_center"),
      (quest_get_slot, reg3, "$random_quest_no", slot_quest_expiration_days),
      (str_store_troop_name_link,s9,"$g_talk_troop"),
      (setup_quest_text,"$random_quest_no"),
      (str_store_string, s2, "@{s9} asked you to raid a village near {s1}."),
      (call_script, "script_change_player_relation_with_troop","$g_talk_troop",1),
      (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
      (call_script, "script_stand_back"),
      (assign, "$g_leave_encounter", 1),
      ]],

[anyone,"lord_raid_village_reject", [],
    "The excuses of cowards. Go away, your cowardly stench is insulting.", "close_window",
[(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    (try_begin),
      (quest_slot_eq, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 0),
      (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 7),
    (try_end),
 (call_script, "script_stand_back"),
 (assign, "$g_leave_encounter", 1),]],


##### Raid Village - Kham - End #######
##### Village Quests - Kham - End ##########

# TLD - mirkwood sorcerer quest finish (GA, fixed by CppCoder) -- begin.

[anyone|plyr,"lord_active_mission_1", [ 
                            (check_quest_active,"qst_mirkwood_sorcerer"),
                            (check_quest_succeeded, "qst_mirkwood_sorcerer"),
                            (eq, "$g_talk_troop", "trp_lorien_lord")],
"The sorcerer of Mirkwood has been slain, my Lady.", "lord_mission_sorcerer_completed",[]],

# CppCoder: Need someone to improve this dialog below...
[anyone|plyr,"lord_active_mission_1", [
                            (check_quest_active,"qst_mirkwood_sorcerer"),
                            (check_quest_failed, "qst_mirkwood_sorcerer"),
                            (eq, "$g_talk_troop", "trp_lorien_lord"),
          (quest_slot_eq,"qst_mirkwood_sorcerer",slot_quest_current_state,0),],
"Forgive me, my Lady, but urgent matters have prevented me from slaying the sorcerer, and in the meantime he has fled.", "lord_mission_sorcerer_failed",[]], 

[anyone|plyr,"lord_active_mission_1", [
                            (check_quest_active,"qst_mirkwood_sorcerer"),
                            (check_quest_failed, "qst_mirkwood_sorcerer"),
                            (eq, "$g_talk_troop", "trp_lorien_lord"),
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
  #Kham - Eliminate Patrols Refactor START
  #(quest_get_slot, ":quest_target_party_template", "qst_eliminate_patrols", slot_quest_target_party_template),
  #(store_num_parties_destroyed_by_player, ":num_destroyed", ":quest_target_party_template"),
  #(party_template_get_slot, ":previous_num_destroyed", ":quest_target_party_template", slot_party_template_num_killed),
  #(val_sub, ":num_destroyed", ":previous_num_destroyed"),
  (quest_get_slot, ":to_destroy", "qst_eliminate_patrols", slot_quest_target_amount),
  (quest_get_slot, ":num_destroyed","qst_eliminate_patrols",slot_quest_current_state),
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
                                         (quest_get_slot, reg66, "qst_raise_troops", slot_quest_current_state),                                
                                         ] + (is_a_wb_dialog and [
                                         (quest_slot_eq, "qst_raise_troops", slot_quest_current_state, -1),
                                         ] or []) + [ 
                                         (quest_get_slot, ":quest_target_troop", ":lords_quest", slot_quest_target_troop),
                                         (quest_get_slot, ":quest_target_amount", ":lords_quest", slot_quest_target_amount),
										 (store_div, ":min_quest_target_amount", ":quest_target_amount", 2), #InVain: Hand in the quest earlier, but scale reward
                                         (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_target_troop"),
                                         (ge, ":num_companions", ":min_quest_target_amount"),  
										 (val_min, ":num_companions", ":quest_target_amount"),
                                         (assign, reg1, ":num_companions"),
                                         (str_store_troop_name_plural, s13, ":quest_target_troop")],
"Indeed. I have raised {reg1} {s13}. You can take them.", "lord_raise_troops_thank",[
  (quest_get_slot, ":quest_target_troop", "qst_raise_troops", slot_quest_target_troop),
  (quest_get_slot, ":quest_target_amount", "qst_raise_troops", slot_quest_target_amount),
  (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_target_troop"),
  (val_min, ":num_companions", ":quest_target_amount"),
  (quest_set_slot, "qst_raise_troops", slot_quest_current_state, ":num_companions"),
  (party_remove_members, "p_main_party", ":quest_target_troop", ":num_companions"),
  (val_mul, ":num_companions", 100),
  (store_div, ":finish_percentage", ":num_companions", ":quest_target_amount"),
  (val_min, ":finish_percentage", 100),
  (call_script, "script_finish_quest", "qst_raise_troops", ":finish_percentage"),
  (troop_get_slot, ":cur_lords_party", "$g_talk_troop", slot_troop_leaded_party),
  (gt, ":cur_lords_party", 0),
  (party_add_members, ":cur_lords_party", ":quest_target_troop", ":quest_target_amount")]],

] + (is_a_wb_dialog and [
[anyone|plyr,"lord_active_mission_2", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
                     (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                                         (store_partner_quest,":lords_quest"),
                                         (this_or_next|eq,":lords_quest","qst_raise_troops"),
                                         (check_quest_active, "qst_raise_troops"),
                                         (quest_slot_eq, "qst_raise_troops", slot_quest_giver_troop, "$g_talk_troop"),
                                         (quest_slot_ge, "qst_raise_troops", slot_quest_current_state, 1),
										 (quest_get_slot, ":trained_recruits", ":lords_quest", slot_quest_current_state),
                                         (quest_get_slot, ":quest_target_amount", ":lords_quest", slot_quest_target_amount),
                                         (assign, reg1, ":trained_recruits"),
                                         (assign, reg2, ":quest_target_amount"),
                                        ],

"Indeed. I have trained {reg2} troops, and {reg1} of them have learned well. You can take them, they should be more prepared for battle.", "lord_raise_troops_thank",[
  (quest_get_slot, ":trained_recruits", "qst_raise_troops", slot_quest_current_state), #InVain: now, we reduce it wrt to number of troops we defeated in the arena
  (val_mul, ":trained_recruits", 100),
  (quest_get_slot, ":quest_target_amount", "qst_raise_troops", slot_quest_target_amount),  
  (store_div, ":finish_percentage", ":trained_recruits", ":quest_target_amount"),
  (val_min, ":finish_percentage", 100),
  (call_script, "script_finish_quest", "qst_raise_troops", ":finish_percentage"),
  (troop_get_slot, ":cur_lords_party", "$g_talk_troop", slot_troop_leaded_party),
  (gt, ":cur_lords_party", 0),
  (faction_get_slot, ":tier_2_troop", "$g_talk_troop_faction", slot_faction_tier_2_troop),
  (party_add_members, ":cur_lords_party", ":tier_2_troop", "$g_arena_training_kills")]],

] or []) + [ 

#partly succeeded
[anyone,"lord_raise_troops_thank", [],
"{s4}", "lord_raise_troops_thank_2",[
	(quest_get_slot, ":quest_target_amount", "qst_raise_troops", slot_quest_target_amount),
	(quest_get_slot, ":trained_recruits", "qst_raise_troops", slot_quest_current_state),
     (try_begin),
       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
	   (ge, ":trained_recruits", ":quest_target_amount"),
       (str_store_string, s4, "@These soldiers may well turn the tide in my plans, {playername}. I am confident you've trained them well. My thanks and my compliments to you."),
     (else_try),
	   (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
	   (lt, ":trained_recruits", ":quest_target_amount"),
       (str_store_string, s4, "@I wish you had trained them all, {playername}. But in these evil times, I will take whatever you can offer."),
     (else_try),
		(ge, ":trained_recruits", ":quest_target_amount"),
		(str_store_string, s4, "@Good work in shaping up those recruits, {playername}, you have been most useful. Hopefully they'll last longer than the last batch, but come see me again if they don't."),
     (else_try),
       (str_store_string, s4, "@Is that all you could do, {playername}? These will hardly replace yesterday's losses. Give them to me!"),
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
"A troll is a dangerous creature indeed. A giant monster which possesses an incredible strength in its deformed muscles. Their skin is as hard as iron, and a tree trunk is but a small club when wielded in their hands. It is rumored that a single troll can easily best a group of half a dozen well armed and trained men, wasting each of them with a single blow. Not only men but horses too fear trolls. Be careful if you plan to charge one while mounted.", "lord_mission_told",[]],

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
[anyone, "lord_mission_mirkwood_sorcerer_rejected", [], "I understand, {playername}. But do not tally for too long, for the effort of resisting his magic is wearying me.", "lord_pretalk",[(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1)]], 

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
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",3),
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

] + (is_a_wb_dialog and [
#Kham - Alternate Training
[anyone|plyr,"lord_mission_raise_troops_told", [(quest_get_slot, reg1, "$random_quest_no", slot_quest_target_amount), (val_div, reg1, 2), (val_max, reg1, 2),],
"I suggest another method, {s65}. I'll take {reg1} fresh recruits to the training fields teach them a thing or two...", "lord_mission_raise_troops_alternate_1",[]],
[anyone|plyr,"lord_mission_raise_troops_alternate_1", [(quest_get_slot, reg1, "$random_quest_no", slot_quest_target_amount), (val_div, reg1, 2), (val_max, reg1, 2),],
"I suggest another method, {s65}.... I'll take {reg1} fresh recruits to the training fields teach them a thing or two. They won't become {s14} afterwards, but this is one step towards that.", "lord_mission_raise_troops_alternate",[]],
] or []) + [ 

[anyone|plyr,"lord_mission_raise_troops_told", [], "I am too busy these days to train anyone.", "lord_mission_raise_troops_rejected",[]],

[anyone,"lord_mission_raise_troops_accepted", [], 
"You've taken a weight off my shoulders, {playername}.\
 I shall tell my sergeants to send you the recruits and attach them to your command.\
 Also, I'll advance you some money to help with expenses. Here, this purse should do it.\
 Thank you for your help.", "close_window",
   [(call_script,"script_stand_back"),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (quest_set_slot, "qst_raise_troops", slot_quest_current_state, -1),
    #(call_script, "script_troop_add_gold", "trp_player",100),
    (call_script, "script_add_faction_rps", "$g_talk_troop_faction", 100),
    
    (quest_get_slot, ":recruit_troop", "$random_quest_no", slot_quest_object_troop),
    (quest_get_slot, ":num_recruits", "$random_quest_no", slot_quest_target_amount),
    (party_add_members, "p_main_party", ":recruit_troop", ":num_recruits"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
    (assign, "$g_leave_encounter",1)]],

] + (is_a_wb_dialog and [

[anyone,"lord_mission_raise_troops_alternate", [], 
"This is an interesting proposal, {playername}.\
 I shall tell my sergeants to send the recruits to the training field.\
 Follow them there, and whip them up to shape. I will be watching.\
 Thank you for your help.", "close_window",
   [(call_script,"script_stand_back"),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (quest_get_slot, ":num_recruits", "$random_quest_no", slot_quest_target_amount),
    (val_div, ":num_recruits", 2),
    (val_max, ":num_recruits", 2),
    (quest_set_slot, "$random_quest_no", slot_quest_target_amount, ":num_recruits"),
	(store_mul, ":quest_gold_reward", ":num_recruits", 50),
	(quest_set_slot, "$random_quest_no", slot_quest_gold_reward, ":quest_gold_reward"),
	(store_mul, ":quest_xp_reward", ":num_recruits", 20),
	(quest_set_slot, "$random_quest_no", slot_quest_xp_reward, ":quest_xp_reward"),
	(store_mul, ":quest_rank_reward", ":num_recruits", 3),
	(quest_set_slot, "$random_quest_no", slot_quest_rank_reward, ":quest_rank_reward"),
	(store_mul, ":quest_giver_fac_str_effect", ":num_recruits", 10),
	(quest_set_slot, "$random_quest_no", slot_quest_giver_fac_str_effect, ":quest_giver_fac_str_effect"),
    (call_script, "script_change_player_relation_with_troop","$g_talk_troop",2),
    (assign, "$g_leave_encounter",1),
    (change_screen_return),
    (jump_to_menu, "mnu_alternate_training_fight"),
  ]],

] or []) + [ 


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
 There has been news recently that the fugitive has been seen at {s3}.\
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

## Defend Refugees INIT START
[anyone,"lord_tell_mission", [
  (eq,"$random_quest_no","qst_blank_quest_01"),
  (quest_get_slot, ":quest_target_center", "qst_blank_quest_01", slot_quest_target_center),
  (str_store_party_name, s6, ":quest_target_center")],
 "There are refugees on their way to {s6}. They will be moving slow, and as such, is a moving target to our enemies. Defend them until they reach their destination.", "lord_mission_told",[
       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
       (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
       (str_store_troop_name_link, s9, "$g_talk_troop"),
       (str_store_party_name_link, s3, ":quest_target_center"),
       (str_store_party_name_link, s4, ":quest_object_center"),
       (setup_quest_text,"$random_quest_no"),
       (str_store_string, s2, "@{s9} asked you to defend 3 groups of refugees on their way to {s3}.")]],

## Defend Refugees INIT END

## Hunt Down Refugees INIT START
[anyone,"lord_tell_mission", [
  (eq,"$random_quest_no","qst_blank_quest_02"),
  (quest_get_slot, ":quest_target_center", "qst_blank_quest_02", slot_quest_target_center),
  (str_store_party_name, s6, ":quest_target_center")],
 "Our spies tell us that there are refugees on their way to {s6}. They will be slow because of all the old, the sick, and the dying. Hunt them down, kill all the men, and take everyone else as slaves. Make sure none arrive at their destination!", "lord_mission_told",[
       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
       (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),
       (str_store_troop_name_link, s9, "$g_talk_troop"),
       (str_store_party_name_link, s3, ":quest_target_center"),
       (str_store_party_name_link, s4, ":quest_object_center"),
       (setup_quest_text,"$random_quest_no"),
       (str_store_string, s2, "@{s9} asked you to hunt down 3 groups of refugees on their way to {s3}.")]],

## Hunt Down Refugees INIT END


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
 I want you to assemble a scouting party, get close enough to {s13}, and dispatch the scouts. I will also give you a few recruits, but you should not send them out on their own."), #Good
       (else_try),
         (str_store_string, s5, "@My spies tell me the enemy is up to something in {s13}.\
 Our cowardly scouts have so far failed to get close enough and tell us anything of import.\
 I want you to recruit your own scouting party, get close enough to {s13}, and leave them there. Make sure they don't turn around and flee! I will give you these recruits, they won't be missed."), #Evil
       (try_end),
#       (faction_get_slot, ":tier_1_troop", "$g_talk_troop_faction", slot_faction_tier_1_troop), #4 of these
#       (str_store_troop_name_plural, s16, ":tier_1_troop"),
#       (faction_get_slot, ":tier_2_troop", "$g_talk_troop_faction", slot_faction_tier_2_troop), #2 of these
#       (str_store_troop_name_plural, s15, ":tier_2_troop"),
       (str_store_faction_name, s15, "$g_talk_troop_faction"),
       (faction_get_slot, ":tier_3_troop", "$g_talk_troop_faction", slot_faction_tier_3_troop), #1 of these, and used for member chat
       (str_store_troop_name, s14, ":tier_3_troop"),
	   (quest_get_slot, reg1, "qst_dispatch_scouts", slot_quest_target_amount),
       (setup_quest_text, "qst_dispatch_scouts"),
       (str_store_string, s2, "@{s9} asked you to dispatch a scout party near {s13}.^Obtain {reg1} soldiers of {s15}, of which at least 1 is {s14}, get close to {s13} and talk to the {s14} to dispatch the party.")]],
    
[anyone,"lord_tell_mission", [(eq,"$random_quest_no","qst_eliminate_patrols")],
"{s5}", "lord_mission_told", [
       (quest_get_slot, ":quest_target_party_template", "qst_eliminate_patrols", slot_quest_target_party_template),
       (quest_get_slot, reg1, "qst_eliminate_patrols", slot_quest_target_amount),
       (spawn_around_party, "p_main_party", ":quest_target_party_template"),
       (assign, ":fake_party", reg0),
       (str_store_party_name, s13, ":fake_party"),
       (call_script, "script_safe_remove_party", ":fake_party"),
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


## Quest Acceptance Dialogues - This handles any party creation after accepting a quest

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
    (else_try),
      (eq, "$random_quest_no", "qst_blank_quest_01"), #Defend Refugees
      (call_script, "script_cf_quest_defend_refugees_party_creation"),
    (else_try),
      (eq, "$random_quest_no", "qst_blank_quest_02"), #Hunt down Refugees
      (call_script, "script_cf_quest_hunt_refugees_party_creation"),
    (else_try),
       (eq, "$random_quest_no", "qst_dispatch_scouts"), 
       (faction_get_slot, ":tier_1_troop", "$g_talk_troop_faction", slot_faction_tier_1_troop),
       (str_store_troop_name_plural, s16, ":tier_1_troop"),
	   (quest_get_slot, reg1, "qst_dispatch_scouts", slot_quest_target_amount),
       (val_div, reg1, 2),
       (try_for_range, ":unused", 0, reg1), #check party size
        (neg|troops_can_join, reg1),
        (val_sub, reg1, 1),
       (try_end),
       (party_add_members, "p_main_party", ":tier_1_troop", reg1),
       (display_message, "@{reg1} {s16} joined your party."),
  (try_end),
  (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
  (try_begin),
    (eq, "$random_quest_no", "qst_lend_surgeon"),
    (assign, "$g_leave_town_outside", 1),
    (assign,"$auto_enter_town","$g_encountered_party"),
#   (store_current_hours, "$quest_given_time"),
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
      (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 7),
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

#Friendship Rewards Begin
[anyone,"lord_leave", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_friendship_reward_type, friendship_reward_troops),
    (troop_set_slot, "$g_talk_troop", slot_troop_friendship_reward_type, friendship_reward_none),
    (troop_slot_ge, "$g_talk_troop", slot_troop_friendship_reward_progress, 100),
    (troop_set_slot, "$g_talk_troop", slot_troop_friendship_reward_progress, 0),
    (troop_get_slot, reg40, "$g_talk_troop", slot_troop_friendship_reward_id),

    (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
    (assign, ":player_relation", reg0),
    (call_script, "script_lord_reward_troops_count", "$g_talk_troop"),
    (store_sub, reg42, reg41, 1),

    (try_begin),
        (eq, "$player_looks_like_an_orc", 1),
        (try_begin),
            (ge, ":player_relation", 70),
            (str_store_string,s23,"@Wait, {playername}. I don't say this often, but you are an exceptionally reliable servant."),
        (else_try),
            (str_store_string,s23,"@Halt, {playername}. I once thought you little more than a snaga, but you are proving to be a useful servant."),
        (try_end),
        (str_store_string, s24, "@Take these warriors, that your horde might continue to serve me."),
    (else_try),
        (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
                (try_begin),
            (ge, ":player_relation", 70),
            (str_store_string,s23,"@One last thing, {playername}. In a land filled with backstabbers and rivals, you have always been a true ally."),
        (else_try),
            (str_store_string,s23,"@Wait, {playername}. When we met I sensed in you a rival, but I see now I was mistaken."),
        (try_end),
        (str_store_string, s24, "@Take these warriors, and use them to strike down our foes."),
    (else_try),
        (try_begin),
            (ge, ":player_relation", 70),
            (str_store_string,s23,"@Before you leave, {playername}, know that you have always been a good friend to me."),
        (else_try),
            (str_store_string,s23,"@Wait, {playername}. I don't know you half as well as I should like, but thus far you have been a good friend."),
        (try_end),
        (str_store_string, s24, "@Allow me to repay you by giving you some troops."),
    (try_end),

    (str_store_troop_name_by_count, s25, reg40, reg41),

    #TODO: Ren - Add additional friendship rewards. Maybe. Some of this may also need to be moved to a script if it's reused elsewhere (such as after a battle)
    ], "{s23} {s24} I have {reg41} {s25} who {reg42?are:is} prepared to join you.", "lord_offer_troops",[]],

    [anyone|plyr,"lord_offer_troops", [
        (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
        (gt, ":free_capacity", 0), #skip this option if the player has no room
        (try_begin),
            (ge, ":free_capacity", reg41),
            (assign, reg42, 1),
        (else_try),
            (assign, reg42, 0),
            (assign, reg41, ":free_capacity"),
        (try_end),
    ], "Thank you, {reg42?I will gladly accept them into my party:but I fear I only have room for {reg41}}.", "close_window",[
        (party_add_members, "p_main_party", reg40, reg41),
        (call_script,"script_stand_back"),(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)
    ]],

    [anyone|plyr,"lord_offer_troops", [], "I fear I cannot accept them at this time.", "close_window",[(call_script,"script_stand_back"),(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],

    [anyone,"lord_leave", [
    (troop_slot_eq, "$g_talk_troop", slot_troop_friendship_reward_type, friendship_reward_gear),
    (troop_set_slot, "$g_talk_troop", slot_troop_friendship_reward_type, friendship_reward_none),
    (troop_slot_ge, "$g_talk_troop", slot_troop_friendship_reward_progress, 100),
    (troop_set_slot, "$g_talk_troop", slot_troop_friendship_reward_progress, 0),
    (troop_get_slot, reg40, "$g_talk_troop", slot_troop_friendship_reward_id),

    (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
    (assign, ":player_relation", reg0),
    (call_script, "script_lord_reward_equipment_modifier", "$g_talk_troop"),
    (str_store_item_name, s22, reg40),

    (try_begin),
        (eq, "$player_looks_like_an_orc", 1),
        (try_begin),
            (ge, ":player_relation", 70),
            (str_store_string,s23,"@Wait, {playername}. Capable servants like you and your warriors deserve the best equipment."),
        (else_try),
            (str_store_string,s23,"@Halt, {playername}. It's shameful to have my servants using such inferior equipment."),
        (try_end),
        (str_store_string, s24, "@Take this {s22} and let it aid your rampage."),
    (else_try),
        (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
                (try_begin),
            (ge, ":player_relation", 70),
            (str_store_string,s23,"@Before you go, {playername}. Great warriors like you and your companions deserve only the best weapons, armor, and mounts."),
        (else_try),
            (str_store_string,s23,"@Wait, {playername}. Your army has done well, but I think you'd do better with superior equipment."),
        (try_end),
        (str_store_string, s24, "@Take this {s22}. I have no need of it."),
    (else_try),
        (try_begin),
            (ge, ":player_relation", 70),
            (str_store_string,s23,"@Just a moment, {playername}. Heroes like you and your companions are worthy of the finest weapons, armor, and horses."),
        (else_try),
            (str_store_string,s23,"@Wait, {playername}. You have been an able commander in the war effort. I think it's time you had some better equipment."),
        (try_end),
        (str_store_string, s24, "@Accept this {s22}, may it aid you and your companions."),
    (try_end),
    ], "{s23} {s24}", "lord_offer_item",[]],

    [anyone|plyr,"lord_offer_item", [
        (store_free_inventory_capacity, ":free_capacity"),
        (gt, ":free_capacity", 0), #skip this option if the player has no room
    ], "Thank you, I shall see  that it is put to good use.", "close_window",[
        (troop_add_item, "trp_player", reg40, reg41),
        (call_script,"script_stand_back"),(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)
    ]],

    [anyone|plyr,"lord_offer_item", [], "I'm afraid I must decline.", "close_window",[(call_script,"script_stand_back"),(eq,"$talk_context",tc_party_encounter),(assign, "$g_leave_encounter", 1)]],
#Friendship Rewards End

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
# [anyone,"start",[(eq, "$talk_context", 0),
        # (agent_get_entry_no, ":entry", "$g_talk_agent"),
        # (eq,":entry",24),
                # (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                # (party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player")], #player visited prison in brigand fort only?
# "Good day, Commander. Will you be visiting the prison?", "prison_guard_players",[]],
# [anyone|plyr,"prison_guard_players", [(neg|party_slot_eq, "$current_town", slot_town_prison, -1)],
# "Yes. Unlock the door.", "close_window",[(call_script,"script_stand_back"),(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],
# [anyone|plyr,"prison_guard_players", [], "No, not now.", "close_window",[(call_script,"script_stand_back"),]],

# [anyone,"start", [(eq, "$talk_context", 0),(agent_get_entry_no, ":entry", "$g_talk_agent"),(eq,":entry",24)],
# "Yes? What do you want?", "prison_guard_talk",[]],
# [anyone|plyr,"prison_guard_talk", [], "Who is imprisoned here?", "prison_guard_ask_prisoners",[]],
# [anyone|plyr,"prison_guard_talk", [(neg|party_slot_eq, "$current_town", slot_town_prison, -1)],
# "I want to speak with a prisoner.", "prison_guard_visit_prison",[]], 

# [anyone,"prison_guard_ask_prisoners", [],
# "Currently, {s51} {reg1?are:is} imprisoned here.","prison_guard_talk",[(party_clear, "p_temp_party"),
                                                                              # (assign, ":num_heroes", 0),
                                                                              # (party_get_num_prisoner_stacks, ":num_stacks","$g_encountered_party"),
                                                                              # (try_for_range, ":i_stack", 0, ":num_stacks"),
                                                                                # (party_prisoner_stack_get_troop_id, ":stack_troop","$g_encountered_party",":i_stack"),
                                                                                # (troop_is_hero, ":stack_troop"),
                                                                                # (party_add_members, "p_temp_party", ":stack_troop", 1),
                                                                                # (val_add, ":num_heroes", 1),
                                                                              # (try_end),
                                                                              # (call_script, "script_print_party_members", "p_temp_party"),
                                                                              # (try_begin),
                                                                                # (gt, ":num_heroes", 1),
                                                                                # (assign, reg1, 1),
                                                                              # (else_try),
                                                                                # (assign, reg1, 0),
                                                                              # (try_end)]],
  
# [anyone,"prison_guard_visit_prison", [(this_or_next|faction_slot_eq, "$g_encountered_party_faction",slot_faction_marshall,"trp_player"),
                                        # (this_or_next|party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
                                        # (eq, "$g_encountered_party_faction", "$players_kingdom")],
# "Of course, Commander. Go in.", "close_window",[(call_script,"script_stand_back"),(call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],

# [anyone,"prison_guard_visit_prison", [], "You need to get permission from the lord to talk to prisoners.", "prison_guard_visit_prison_2",[]],

# [anyone|plyr,"prison_guard_visit_prison_2", [], "All right then. I'll try that.", "close_window",[(call_script,"script_stand_back"),]],
# [anyone|plyr,"prison_guard_visit_prison_2", [], "Come on now. I thought you were the boss here.", "prison_guard_visit_prison_3",[]],
# [anyone,"prison_guard_visit_prison_3", [], "He-heh. You got that right. Still, I can't let you into the prison.", "prison_guard_visit_prison_4",[]],
  
# [anyone|plyr,"prison_guard_visit_prison_4", [], "All right then. I'll leave now.", "close_window",[(call_script,"script_stand_back"),]],
# [anyone|plyr,"prison_guard_visit_prison_4", [(store_troop_gold,":gold","trp_player"),(ge,":gold",100)],
# "I found a purse with 100 denars a few paces away. I reckon it belongs to you.", "prison_guard_visit_prison_5",[]],

# [anyone,"prison_guard_visit_prison_5", [], "Ah! I was looking for this all day. How good of you to bring it back {sir/madam}.\
 # Well, now that I know what an honest {man/lady} you are, there can be no harm in letting you inside. Go in.", "close_window",[
    # (call_script,"script_stand_back"),
    # (troop_remove_gold, "trp_player",100),
    # (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle")]],

# [anyone|plyr,"prison_guard_talk", [], "Never mind.", "close_window",[(call_script,"script_stand_back"),]],




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
##                                        (call_script, "script_safe_remove_party", "$g_encountered_party"),
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

### TLD dialogs: starting quest caravan master talk - Kham changed context and removed quest. This should be enough
#[trp_start_quest_caravaneer,"party_relieved", [(eq,"$talk_context",tc_starting_quest)], 
#"Thank you for helping! We are safe now.", "caravan_help0",[]], 




######### Start Quest Dialogues - Started by GA, Completed by Kham ######################
######### Start Quest - Caravan                                    ######################
[trp_start_quest_caravaneer,"start", 
  [], "Thank you for helping! We are safe now. My name is Torbal, and I was just delivering some goods when we were attacked.^^ Have you seen those large orcs before? Those do not look like regular mountain ilk we are used to fend off easily. And the paint on their shields is an ancient Mordor sign. I haven't seen those this side of the river for a long time. ^^Dire things are afoot.. War is coming! ^^I advise you to go to the nearest town and warn everyone about what you've seen to whomever is in command there. It's an important matter, so please make haste.", "caravan_help1",
    []],

[trp_start_quest_caravaneer|plyr,"caravan_help1",
   [], 
    "No, I have never seen such a large orc before. Nasty things... ^^I am a Soldier in this coming war that we have all been sensing.", "caravan_help2",
    []],

###Assist Dialogue Conditions####
[trp_start_quest_caravaneer,"caravan_help2", 
  [
    (str_clear,s10),
    (try_begin),
      (eq,"$assist","fac_dwarf"),
      (str_store_string, s10, "@the Dwarves, so that if you pass by Erebor or the Iron Hills, you can try to arm yourself with the fabled Dwarven weaponry"),
    (else_try),
      (eq,"$assist","fac_gondor"),
      (str_store_string, s10, "@Gondor, so that if you pass by their lands, you can try to purchase some of their well-known armours"),
    (else_try),
      (eq,"$assist","fac_rohan"),
      (str_store_string, s10, "@Rohan, so that if you pass by their lands, you can try to purchase some of their fabled horses"),
    (else_try),
      (str_store_string, s10, "@Dale, so that if you pass by their lands, you can try to purchase some of their well-known bows"),
    (try_end),
   ], 
    "You are? Of course you are! I have seen that you are a capable warrior. ^^I am indeed lucky today, so I shall take advantage of this good fortune and make haste to my village and warn my people of these foul beasts. ^^Here, have some of the local currency used by {s10}", "caravan_help_tut",
      []],

###Assist Dialogue Conditions - End####

[trp_start_quest_caravaneer,"caravan_help_tut",
    [(str_store_faction_name, s11, "$assist"), ],
      "(RESOURCE POINT TUTORIAL)^^ Resource Points which you can use to purchase from the people of {s11} are not the ones you earned in your own faction, but the ones you will earn in {s11}. ^^See REPORTS for more information.", "caravan_help3",[]],


[trp_start_quest_caravaneer|plyr,"caravan_help3", 
  [], 
    "Safe journey to you, Torbal. I'm sure we will meet again.", "caravan_help4",
  []],

[trp_start_quest_caravaneer,"caravan_help4",
  [],
    "I look forward to it. My guards here have seen you fight and will definitely tell their Lord all about you. ^^If you assist their people enough times, you will definitely become reknowned amongst them, which can lead to many great things! ^^I for one am well known, and have even been given a monthly income for all the work that I do!","caravan_help_fac_tut",
    []],

[trp_start_quest_caravaneer,"caravan_help_fac_tut",
  [],
    "(FACTION RANKS TUTORIAL) ^^Rank points allow you to rise up in the ranks of your faction (and/or other factions). ^^This will determine your max party size, weekly faction resource income, and unlock other faction specific rewards.", "caravan_help5",[]],

[trp_start_quest_caravaneer|plyr, "caravan_help5",
  [],
    "I will remember that. Thank you Torbal, and stay safe.", "close_window",
      [
        (call_script,"script_stand_back"),
        (assign, "$g_leave_encounter",1),
        (change_screen_return),
        (call_script,"script_add_faction_rps", "$assist", 150),
        (call_script,"script_increase_rank", "$assist",10),
      ]
],


######### Start Quest - Caravan - End                              ######################


#[trp_start_quest_caravaneer,"caravan_help2", [], "You are? Of course you are! I have seen that you are a capable warrior. I have a personal business I would like your help with. There is a small fort near Nindalf swamps, where common people and travellers can find food and lodge. It's run by a local chief who does not answer neither to Gondor, nor to Rohan. I'm a merchant traveller myself, so I have respect for people wishing to be free from lordship bonds, as long as they behave. But being independent, they are also powerless before enemy onslaught. War outbreak in next several days looks like a certain thing to me. I want you to get to those people and see if you can help them survive. Tell the chief, Balan, that Torbal asked you to deliver 'a fishslap'. He will recognize it was me who sent you.", "caravan_help3",[]],
#[trp_start_quest_caravaneer|plyr,"caravan_help3", [], "I'll deliver your message. Safe journey to you, Torbal. I'm sure we will meet again.", "close_window",[(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1),(change_screen_return),]],
# end starting quest caravan master talk



### Kham Start Quest Caravan - Evil

[trp_start_quest_uruk,"start", 
  [], 
    "And who are you? We needed none of your interference, nar!", "caravan_attack1",
  []],

[trp_start_quest_uruk|plyr,"caravan_attack1", 
  [ 
    (str_clear, s10),
    (try_begin),
      (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_hand),      
      (str_store_string, s10, "@Without my help you would all lie dead and burnt!^^ I come to answer the call of Saruman, of Isengard. Cross me at your peril!"),
    (else_try),
      (str_store_string, s10, "@Without my help you would all lie dead and burnt!^^ I come to answer the call of the Lord of Mordor, who will soon be Lord of all the World."),
    (try_end),
  ], "{s10}", "caravan_attack2",
  []],

[trp_start_quest_uruk,"caravan_attack2", 
  [ 
    (str_clear, s10),
    (try_begin),
      (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_hand),      
      (str_store_string, s10, "@ *snort* There is only one Lord of all the world, scum. Soon or late, you will answer to Lugbúrz, weakling!"),
    (else_try),
      (str_store_string, s10, "@*snort* Another one for the meat-shield, to eat arrows! Be off, weakling. We have no use for you."),
    (try_end),
   ], "{s10}", "caravan_attack3",
  []],

[trp_start_quest_uruk|plyr,"caravan_attack3", 
  [], "Weakling? Let’s see who the weakling is! (Difficult)", "close_window",
  [
    (jump_to_menu, "mnu_start_quest_duel"),
    (assign,"$start_quest_duel", 1),
  ]],

[trp_start_quest_uruk|plyr,"caravan_attack3", 
  [], 
    "Go on then, coward. I'll see your corpse in the fields.", "close_window",
  [
    (jump_to_menu,"mnu_starting_quest_victory_evil_no_duel"),
    (assign,"$start_quest_duel", 0),
  ]],

[trp_start_quest_orc,"start", 
  [
    (eq,"$start_quest_duel",0),
    (str_clear, s10),
    (try_begin),
      (eq,"$assist","fac_moria"),
      (str_store_string, s10, "@Go to Moria, and get a nice warg for yourself - or some snagas of your own, if you like!"),
    (else_try),
      (eq,"$assist","fac_isengard"),
      (str_store_string, s10, "@Go to Isengard, and get something for yourself - maybe some of the fighting Uruk-Hai will follow you!"),
    (else_try),
      (eq,"$assist","fac_gundabad"),
      (str_store_string, s10, "@Go up north, to Gundabad - dumb and ugly, they are, but they have good furs."),
    (else_try),
      (eq,"$assist","fac_mordor"),
      (str_store_string, s10, "@Get some snagas of your own, like these fellows here who follow me. Maybe you’ll have a war party of your own soon enough!"),
    (else_try),
      (eq,"$assist","fac_rhun"),
      (str_store_string, s10, "@Our friends and allies will hear of you, don’t doubt it! Might be they’d be willing to give you a new mount, or a new blade. No one has time for the weak, but if you’re strong, ha, we help those who help us, see? Trade some of those spoils for a good horse, maybe, with those Men of Rhûn - for riding or eating, your choice, har!"),
    (try_end),
  ], 
    "*snicker* No harm in biding one’s time, warrior! Some of the lads might not think so much of you, but not me, oh no. I saw you fight. Won’t bet against you! {s10}^^But we all stick to our own kind, we do. Serve the Eye, serve the Dark Lord, yes, but do a deed in the East, and the South takes no notice, and likewise. Help the Eye, and the White Hand cares not. Help the Old Man, and the Dark Tower thinks why you waste your time not doing work for it!", "caravan_res_tut1",
    []],

[trp_start_quest_orc,"start", 
  [
    (eq,"$start_quest_duel",1),
    (str_clear, s10),
    (try_begin),
      (eq,"$assist","fac_moria"),
      (str_store_string, s10, "@Go to Moria, and get a nice warg for yourself - or some snagas of your own, if you like!"),
    (else_try),
      (eq,"$assist","fac_isengard"),
      (str_store_string, s10, "@Go to Isengard, and get something for yourself - maybe some of the fighting Uruk-Hai will follow you!"),
    (else_try),
      (eq,"$assist","fac_gundabad"),
      (str_store_string, s10, "@Go up north, to Gundabad - dumb and ugly, they are, but they have good furs."),
    (else_try),
      (eq,"$assist","fac_mordor"),
      (str_store_string, s10, "@Get some snagas of your own, like these fellows here who follow me. Maybe you’ll have a war party of your own soon enough!"),
    (else_try),
      (eq,"$assist","fac_rhun"),
      (str_store_string, s10, "@Trade some of those spoils for a good horse, maybe, with those Men of Rhûn - for riding or eating, your choice, har!"),
    (try_end),
  ], 
    "*snicker* I s’pose I’m the leader now. You are a fierce warrior, yes! Take your share of the loot. Some o’ the lads were betting on you being warg meat, but not me, oh no. I saw you fight. Won’t bet against you!^^Our friends and allies will hear of you, don’t doubt it! Might be they’d be willing to give you a new mount, or a new blade. No one has time for the weak, but if you’re strong, ha, we help those who help us, see? {s10}^^But we all stick to our own kind, we do. Serve the Eye, serve the Dark Lord, yes, but do a deed in the East, and the South takes no notice, and likewise. Help the Eye, and the White Hand cares not. Help the Old Man, and the Dark Tower thinks why you waste your time not doing work for it!", "caravan_res_tut2",
    []],

[trp_start_quest_orc,"caravan_res_tut1", 
  [],
   "(RESOURCE POINT TUTORIAL)^^ Resource Points which you can use to purchase from the people of Mordor are not the ones you earned in your own faction, but the ones you will earn in Mordor. ^^See REPORTS for more information.", "caravan_noduel",[]],

[trp_start_quest_orc,"caravan_res_tut2", 
  [],
   "(RESOURCE POINT TUTORIAL)^^ Resource Points which you can use to purchase from the people of Mordor are not the ones you earned in your own faction, but the ones you will earn in Mordor. ^^See REPORTS for more information.", "caravan_duel1",[]],

[trp_start_quest_orc|plyr,"caravan_noduel", 
  [], 
    "I could kill him as easily as I spit! But I have nothing to prove to the likes of him.", "caravan_duel2", 
    []],

[trp_start_quest_orc|plyr,"caravan_duel1", 
  [], 
    "What I do is none of your affair, Orc. But I will help our allies and slay our foes.", "caravan_duel2", 
    []],

[trp_start_quest_orc, "caravan_duel2",
  [],
    "Fair enough, fair enough! Look at these cowering wretches around us! Ha! They fear you, oh yes, as they should, as they should! I don’t. Heh. But then, I owe you a favour, don’t I! I’ll do you a good turn in my way. I’ll tell the Bosses about you today. Word’ll get around. And when the Bosses hear enough about you… why, could be they’d have something special for you. Gifts, power, respect! I’m going back now for a nice big helping myself!", "caravan_fac_tut",
    []],

[trp_start_quest_orc,"caravan_fac_tut", 
  [],
   "(FACTION RANKS TUTORIAL) ^^Rank points allow you to rise up in the ranks of your faction (and/or other factions). ^^This will determine your max party size, weekly faction resource income, and unlock other faction specific rewards.", "caravan_duel3",[]],


[trp_start_quest_orc|plyr,"caravan_duel3", 
  [ 
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_rhun"),
      (str_store_string, s10, "@That is not a smart thing to say in front of a Rhun Warrior...Next time I see you, I will kill you."),
    (else_try),
      (str_store_string, s10, "@They will all know my name... They will know to fear it"),
    (try_end),
  ], 
    "{s10}", "close_window", 
   [
        (str_clear,s10),
        (call_script,"script_stand_back"),
        (assign, "$g_leave_encounter",1),
        (change_screen_return),
        (call_script,"script_add_faction_rps", "$assist", 150),
        (try_begin),
          (eq, "$start_quest_duel", 1),
          (troop_add_item, "trp_player", "itm_metal_scraps_medium"),
          (call_script,"script_increase_rank", "$assist",15),
        (else_try),
          (call_script,"script_increase_rank", "$assist",10),
        (try_end),
      ]
],
### Kham Start Quest Dialogue - Evil End

### Kham Start Quest Dialogue - Elves Start

[trp_start_quest_woodelf,"start", 
  [
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_imladris"),
      (str_store_string, s10, "@Suilad, mellon! It is not oft we meet folk from the Hidden Valley in our realm. We give thanks to the stars they lead you to our aid, and to you as well - le hannon!"),
    (else_try),
      (eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@Suilad, mellon! It is rare to have one of our woodland kin come to our aid - le hannon!"),
    (else_try),
      (eq,"$players_kingdom", "fac_beorn"),
      (str_store_string, s10, "@Suilad, mellon! That is - thank you, friend!^^ At first I wasn’t sure if a goblin sabre, or a raging bear would be our doom. Alas, the stars were kind to send you to our aid."),
    (try_end),
  ], 
    "{s10}", "woodelf_help_1",
  []],

[trp_start_quest_woodelf|plyr,"woodelf_help_1", 
  [
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_imladris"),
      (str_store_string, s10, "@Alas, it is not a pleasant purpose or mere wandering that bring me and others serving lord Elrond to these lands... "),
    (else_try),
      (eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@You wouldn't have need of our aid if you kept your borders shut!"),
    (else_try),
      (eq,"$players_kingdom", "fac_beorn"),
      (str_store_string, s10, "@(*growl* I know your tongue, elf, well enough to know if you mock me or if you give thanks... "),
    (try_end),
  ], 
    "{s10}", "woodelf_help_1a",
  []],

[trp_start_quest_woodelf|plyr,"woodelf_help_1", 
  [
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_imladris"),
      (str_store_string, s10, "@Istan quete ya merin, ar lá hanyuvatyen. Deep are my master’s designs, not for all to see and understand."),
    (else_try),
      (eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@Alae! Our green woods are heavily patrolled, our thick gates stand firm, king Thranduil’s halls secure. It would be wise to follow our example."),
    (else_try),
      (eq,"$players_kingdom", "fac_beorn"),
      (str_store_string, s10, "@(say nothing)"),
    (try_end),
  ], 
    "{s10}", "woodelf_help_2",
  []],

[trp_start_quest_woodelf|plyr,"woodelf_help_1a", 
  [
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_imladris"),
      (str_store_string, s10, "@Alas, it is not a pleasant purpose or mere wandering that bring me and others serving lord Elrond to these lands. ^^An ancient evil stirred in the dark places and now it swarms into the light. Wise ones across the Mountains answered the call and hosts of Imladris march to battle, to fight for the North."),
    (else_try),
      (eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@You wouldn't have need of our aid if you kept your borders shut! ^^Tales of the Forest Witch only scare away witless fools - not so the orc filth we just slew."),
    (else_try),
      (eq,"$players_kingdom", "fac_beorn"),
      (str_store_string, s10, "@*growl* I know your tongue, elf, well enough to know if you mock me or if you give thanks.^^ Stars had none to do with it - I sensed the filth and followed a trail. I would have slain them were you in danger or not."),
    (try_end),
  ], 
    "{s10}", "woodelf_help_2a",
  []],


[trp_start_quest_woodelf,"woodelf_help_2",
 [
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_imladris"),
      (str_store_string, s10, "@Keep your secrets then, friend, but the Golden Woods whisper of your kin’s arrival. ^^We will inform our lady Galadriel of lord Elrond’s coming, though I suspect she knows of it already. And we shall speak of you too, to all our people. ^^Le maethor veleg a gornui! Your valour and deeds shall be known and your needs met whenever you visit our Valley of Singing Gold."),
    (else_try),
      (eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@We walk under the sun and the stars, to dwell in caves is not our desire. Still, your undoubtedly well meant counsel is well received. ^^Your wisdom and brave deeds shall be known, your needs met whenever you wander into our domain."),
   (else_try),
      (eq,"$players_kingdom", "fac_beorn"),
      (str_store_string, s10, "@*he sighs and smiles slightly* ^^Very well. For our common purpose we are happy to share all, even if words are in short supply where you come from."),
    (try_end),
 ], 
  "{s10}", "woodelf_help_3",[]],


[trp_start_quest_woodelf,"woodelf_help_2a",
 [
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_imladris"),
      (str_store_string, s10, "@For some months we have watched the orc filth multiplying and staining our woods. ^^We will inform our lady Galadriel of lord Elrond’s coming, though I suspect she knows of it already. And we shall speak of you too, to all our people. ^^Le maethor veleg a gornui! Your valour and deeds shall be known and your needs met whenever you visit our Valley of Singing Gold."),
    (else_try),
      (eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@Calm yourself, friend. Pedin i phith in aniron, a nin u-cheniathog. ^^We shall speak of you to all our people. Your valour and deeds shall be known, your needs met whenever you come to bask in the light of our Golden Valley."),
   (else_try),
      (eq,"$players_kingdom", "fac_beorn"),
      (str_store_string, s10, "@Stars sail through the heavenly seas, men tread the earth. Truly, who can say if their paths follow each other? We shall speak of you to all our people. Your deeds shall be known and your needs met, were you to chase a star to the Golden Valley."),
    (try_end),
 ], 
  "{s10}", "woodelf_help_3",[]],

[trp_start_quest_woodelf,"woodelf_help_3",
 [
    (str_clear,s10),
    (try_begin),
      (this_or_next|eq,"$players_kingdom", "fac_imladris"),
      (this_or_next|eq,"$players_kingdom", "fac_beorn"),
      (             eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@(RESOURCE POINT TUTORIAL)^^ Resource Points which you can use to purchase from the people of Lorien are not the ones you earned in your own faction, but the ones you will earn in Lothlorien. ^^See REPORTS for more information."),
    (else_try),
      (eq,"$players_kingdom", "fac_lorien"),
      (str_store_string, s10, "@(RESOURCE POINT TUTORIAL)^^ Resource Points which you can use to purchase from the people of Beorn are not the ones you earned in Lothlorien, but the ones you will earn in Beorn. ^^See REPORTS for more information."),
    (try_end),
 ], 
  "{s10}", "woodelf_help_4",[]],




[trp_start_quest_woodelf|plyr,"woodelf_help_4",
 [
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_imladris"),
      (str_store_string, s10, "@I have long wished to visit the woodland folk..."),
    (else_try),
      (eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@What form shall the favour of Lorien take..."),
   (else_try),
      (eq,"$players_kingdom", "fac_beorn"),
      (str_store_string, s10, "@Our bees make honey and wax, our herds give milk, butter and cheese..."),
    (try_end),
 ], 
  "{s10}", "woodelf_help_4a",[]],


[trp_start_quest_woodelf|plyr,"woodelf_help_4a",
 [
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_imladris"),
      (str_store_string, s10, "@I have long wished to visit the woodland folk, taste your lembas and hear your songs! ^^We brought sparkling golden wines, dusty tomes and proud ancient banners to remind us of our stream-singing valley, but I’m curious what unique wonders are to be found in Laurelindorenan."),
    (else_try),
      (eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@What form shall the favour of Lorien take? ^^Gold that turns into leaves come morning? Clear tasteless drink and dusty fairy-bread for my troops? ^^Blood-red wine, freshly hunted deer, armouries filled with sharp spears and keen arrows! That is hospitality I prefer."),
   (else_try),
      (eq,"$players_kingdom", "fac_beorn"),
      (str_store_string, s10, "@Our bees make honey and wax, our herds give milk, butter and cheese.^^ Bread we make ourselves, a sharp axe I can trade for with dwarves when they pass through.^^ What else would I need, what more than a pair of strong hands?"),
    (try_end),
 ], 
  "{s10}", "woodelf_help_5",[]],

[trp_start_quest_woodelf|plyr,"woodelf_help_4",
 [
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_imladris"),
      (str_store_string, s10, "@If fate wills it, I shall walk your lands again, and know all their secrets."),
    (else_try),
      (eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@If I ever have need for the kind of help Lorien can offer, I shall come for it. Whatever use it may be."),
   (else_try),
      (eq,"$players_kingdom", "fac_beorn"),
      (str_store_string, s10, "@(nod and say nothing)"),
    (try_end),
 ], 
  "{s10}", "woodelf_help_5",[]],

[trp_start_quest_woodelf,"woodelf_help_5",
 [
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_imladris"),
      (str_store_string, s10, "@Oh, there are many and any friend of Lorien is welcome to these gifts! ^^Should we stand shoulder to shoulder on the field of battle again, or should you do the bidding of our Lady and her lords, our people will reward your kindness with all you would require - bright weapons, hard corselets of mail, white-feathered arrows and provisions for your troops. ^^Who knows, in time you might become a great {lord/lady} of Lorien yourself, one who could offer counsel to others, or ask favours of them."),
    (else_try),
      (eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@The joys of the Golden Valley are many and a true friend of Lorien is welcome to them. ^^Should we stand shoulder to shoulder on the field of battle again, or should you do the bidding of our Lady and her lords, our people will reward your effort with all you would require - bright weapons, hard corselets of mail, deadly arrows and nourishing food for your troops.^^Who knows, in time you might become a great {lord/lady} of Lorien yourself, one who would share wisdom with others, or ask favours of them."),
   (else_try),
      (eq,"$players_kingdom", "fac_beorn"),
      (str_store_string, s10, "@Our Golden Valley gives goods aplenty and a friend to Lorien is welcome to them. ^^Should we stand shoulder to shoulder on the field of battle again, or should you aid the designs of our Lady and her lords, our people will reward your effort with all you would require while far away from home."),
    (try_end),
 ], 
  "{s10}", "woodelf_help_6",[]],

[trp_start_quest_woodelf,"woodelf_help_6",
 [], 
  "(FACTION RANKS TUTORIAL) ^^Rank points allow you to rise up in the ranks of your faction (and/or other factions). ^^This will determine your max party size, weekly faction resource income, and unlock other faction specific rewards.", "woodelf_help_7",[]],


[trp_start_quest_woodelf|plyr,"woodelf_help_7",
 [
    (str_clear,s10),
    (try_begin),
      (eq,"$players_kingdom", "fac_imladris"),
      (str_store_string, s10, "@I shall keep that in mind.^^ Hantanyel, áva márië!"),
    (else_try),
      (eq,"$players_kingdom", "fac_woodelf"),
      (str_store_string, s10, "@That may be so, some paths of the world run crooked.^^ Boe i 'waen!"),
    (else_try),
      (eq,"$players_kingdom", "fac_beorn"),
      (str_store_string, s10, "@I seldom wander far away from home. Be off now, as fast as you can. There may be more goblins prowling around."),
    (try_end),
 ], 
  "{s10}", "close_window",
  [ 
    (call_script,"script_stand_back"),
    (assign, "$g_leave_encounter",1),
    (change_screen_return),
    (call_script,"script_add_faction_rps", "$assist", 150),
    (call_script,"script_increase_rank", "$assist",10),
  ]],


[trp_start_quest_woodelf|plyr,"woodelf_help_7",
 [
   
    (eq,"$players_kingdom", "fac_beorn"),
 ],
  "(Raise your hand and leave without a word)", "close_window",
  [ 
     (str_clear,s10),
    (call_script,"script_stand_back"),
    (assign, "$g_leave_encounter",1),
    (change_screen_return),
    (call_script,"script_add_faction_rps", "$assist", 150),
    (call_script,"script_increase_rank", "$assist",10),
  ]],   


###Lorien####

[trp_start_quest_beorning,"start", 
  [
    (eq, "$players_kingdom","fac_lorien"),
  ], 
    "*He sizes you up with a frown.* ^^Shiny things like you is what draws goblins from the mountains into our forest. But you kill them good, for that we give thanks.", "beorn_help1",
  []],

[trp_start_quest_beorning|plyr,"beorn_help1", 
  [], 
    "Well met! Even though we seldom leave our woods, I would not refuse aid to any who oppose servants of the Enemy.", "beorn_help2",
  []],

[trp_start_quest_beorning|plyr,"beorn_help1", 
  [], 
    "(nod without saying a word)", "beorn_help2a",
  []],

[trp_start_quest_beorning,"beorn_help2", 
  [], 
    "It is wise not to go near those who serve him, but today it seems we can not get far enough. ^^All our people will know how many goblin heads you let roll today! And all will welcome you with mead and bread, were you to arrive at one of our steads.", "beorn_help3",
  []],

[trp_start_quest_beorning,"beorn_help2a",
 [],
  "*grunts appreciatively* ^^An elf of a few words, eh? You seem more like our kind, none of that dull elven singing or boring poetry. ^^A good story, from the days when the hills were young and forests without end, that’s what we like best! ^^And that’s what I’ll tell my people about you. All will know how many orc filth you rid them of today. Mead and warm hearts will welcome you in any of our wooden halls.", "beorn_help3",[]],


[trp_start_quest_beorning,"beorn_help3",
 [], 
  "(RESOURCE POINT TUTORIAL)^^ Resource Points which you can use to purchase from the people of Beorn are not the ones you earned in Lothlorien, but the ones you will earn in Beorn. ^^See REPORTS for more information.", "beorn_help4",
  []],


[trp_start_quest_beorning|plyr,"beorn_help4",
 [], 
  "*laugh with a pleasant ring* Do you deem elves to be bear-brothers too?...", "beorn_help4a",
 []],

[trp_start_quest_beorning|plyr,"beorn_help4a",
 [], 
  "*laugh with a pleasant ring* Do you deem elves to be bear-brothers too?... Golden mead is sweet and warms the heart, but perhaps elven blades and keen arrows are needed more in these dark days..", "beorn_help5",
 []],

 [trp_start_quest_beorning|plyr,"beorn_help4",
 [], 
  "(place a hand on your heart, nod and smile)", "beorn_help5",
 []],

[trp_start_quest_beorning,"beorn_help5",
 [], 
  "We may be rough and hairy, grim and dark. But we help our friends, those who help us. ^^If our chiefs think you and your actions worthy, we will follow you to battle.", "beorn_help6",
 []],


[trp_start_quest_beorning,"beorn_help6",
 [], 
  "(FACTION RANKS TUTORIAL) ^^Rank points allow you to rise up in the ranks of your faction (and/or other factions). ^^This will determine your max party size, weekly faction resource income, and unlock other faction specific rewards.",
   "beorn_help7",[]],


 [trp_start_quest_beorning|plyr,"beorn_help7",
 [], 
  "Le fael, friend! Farewell. ", "close_window",
 [
    (call_script,"script_stand_back"),
    (assign, "$g_leave_encounter",1),
    (change_screen_return),
    (call_script,"script_add_faction_rps", "$assist", 150),
    (call_script,"script_increase_rank", "$assist",10),
  ]],

 [trp_start_quest_beorning|plyr,"beorn_help7",
 [], 
  "(raise your hand and leave without a word)", "close_window",
 [
    (call_script,"script_stand_back"),
    (assign, "$g_leave_encounter",1),
    (change_screen_return),
    (call_script,"script_add_faction_rps", "$assist", 150),
    (call_script,"script_increase_rank", "$assist",10),
  ]],


### Kham Start Quest Dialogue - Elves End

### Kham Start Quest Dialogue - Easterlings Start

[trp_start_quest_mordor_scout,"start", 
  [],
   "Great eyes and ears you have there! If you hadn’t warned us, those green-clad tree-climbers would’ve had the jump on us, I warrant - or perhaps escaped, and brought down more of their fellows on our heads! Now they’re for the maggots and crows, and our mission is safe. Ai! The Bosses will be pleased.", "kill_scout_1",[]],

[trp_start_quest_mordor_scout|plyr,"kill_scout_1", 
  [],
   "Watch where you’re taking us, Orc. We have not travelled this far to perish in an ambush, before the war has even begun!", "kill_scout_2",[]],

[trp_start_quest_mordor_scout,"kill_scout_2", 
  [],
   "And war we shall have, indeed! Have no fear, warrior, Mordor is an ally to you and yours. Take this chit - get some supplies. Good for use in all Mordor outposts! Get a round of Orc brew on me!", "kill_scout_3",[]],

[trp_start_quest_mordor_scout,"kill_scout_3", 
  [],
   "(RESOURCE POINT TUTORIAL)^^ Resource Points which you can use to purchase from the people of Mordor are not the ones you earned in your own faction, but the ones you will earn in Mordor. ^^See REPORTS for more information.", "kill_scout_4",[]],

[trp_start_quest_mordor_scout|plyr,"kill_scout_4", 
  [],
   "You want us to drink Orc swill? We'd rather be drinking our own piss.", "kill_scout_5",[]],


[trp_start_quest_mordor_scout,"kill_scout_5", 
  [],
   "Ha! I knew you foreigners did such things! I’ve won my bet with Gothmog, thanks to you!!^^ I’ll tell him and the other Bosses about you, for sure. Lugbúrz will know how useful you were today, have no fear! The Great Eye is upon you, now!^^But we all stick to our own kind, we do. Serve the Eye, serve the Dark Lord, yes, but do a deed in the East, and the South takes no notice, and likewise. Help the Eye, and the White Hand cares not. Help the Old Man, and the Dark Tower thinks why you waste your time not doing work for it!", "kill_scout_6",[]],

[trp_start_quest_mordor_scout,"kill_scout_6", 
  [],
   "(FACTION RANKS TUTORIAL) ^^Rank points allow you to rise up in the ranks of your faction (and/or other factions). ^^This will determine your max party size, weekly faction resource income, and unlock other faction specific rewards.", "kill_scout_7",[]],

[trp_start_quest_mordor_scout|plyr,"kill_scout_7", 
  [],
   "What I do is none of your affair, you disgusting creature. Now let’s move!", "kill_scout_8",[]],

[trp_start_quest_mordor_scout,"kill_scout_8", 
  [],
   "As you wish, as you wish. This way!", "close_window",
  [ 
    (call_script,"script_stand_back"),
    (assign, "$g_leave_encounter",1),
    (change_screen_return),
    (call_script,"script_add_faction_rps", "$assist", 150),
    (call_script,"script_increase_rank", "$assist",10),
  ]],



[trp_start_quest_mordor_scout|plyr,"woodelf_help_1", [], "I have never seen such a large orc before. Nasty things. Do not fret. I am a Soldier in this coming war that we have all been sensing.", "woodelf_help_2",[]],

[trp_start_quest_mordor_scout,"woodelf_help_2", [], "You are? Of course you are! I have seen that you are a capable warrior. I am indeed lucky today, so I shall take advantage of this good fortune and make haste to my village and warn my people of these foul beasts.", "woodelf_help_3",[]],
[trp_start_quest_mordor_scout|plyr,"woodelf_help_3", [], "Safe journey to you, Torbal. I'm sure we will meet again.", "close_window",[(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1),(change_screen_return),]],

### Kham Start Quest Dialogue - Easterlings End
### Kham Healers Dialogue Begin

[anyone,"start", [
      (is_between, "$g_talk_troop", "trp_morannon_healer", "trp_hungry_uruk"),
      (call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (assign, ":rank", reg0), #rank points to rank number 0-9
      (lt, ":rank", 3),
      (call_script, "script_get_rank_title_to_s24", "$g_talk_troop_faction"), (str_store_string_reg, s25, s24), #to s25 (current rank)
      (call_script, "script_get_any_rank_title_to_s24", "$g_talk_troop_faction", 4), #to s24
      (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
      (str_store_string, s2, "@(You need to be {s24} or higher)."),
      (try_begin),
        (neq, ":side", faction_side_good),
        (str_store_string, s1, "@Who are you? A mere {s25}? I do not have time for the likes of you! Leave me be! {s2}"),
      (else_try),
        (str_store_string, s1, "@I am sorry. I cannot attend to you as a {s25} as there are more pressing issues. {s2}"), 
      (try_end), ], 
          "{s1}", "close_window",[(call_script, "script_stand_back")]],

[anyone,"start", [
  (is_between, "$g_talk_troop", "trp_morannon_healer", "trp_hungry_uruk"),
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s1, "@What do you want?"),
  (else_try),
    (str_store_string, s1, "@Greetings, {playername}. What can I do for you?"),
  (try_end)], 
    "{s1}", "healers_ask",[]],


[anyone|plyr,"healers_ask", [], 
    "What do you do?.", "healer_who",[]],

[anyone|plyr,"healers_ask", [
  (eq, "$tld_option_injuries", 1),
  (troop_get_slot, ":wound_mask", "trp_player", slot_troop_wound_mask),
  (assign, ":wounds", 0), 

  # Check If there are any wounds (player) before continuing with dialogue
  (try_begin),
    (neq, ":wound_mask", 0),
    
    (try_begin),(store_and,":x",":wound_mask",wound_head ),(neq,":x",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":x",":wound_mask",wound_chest),(neq,":x",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":x",":wound_mask",wound_arm  ),(neq,":x",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":x",":wound_mask",wound_leg  ),(neq,":x",0),(val_add,":wounds",1),(try_end),
    (troop_set_slot, "trp_player", slot_troop_needs_healing, 1), #Set the slot
    #(display_message, "@DEBUG: Player is wounded"),

  (else_try),
  # Check If any companions are wounded before continuing with dialogue
  (try_for_range, ":npc", companions_begin, companions_end),
    (main_party_has_troop, ":npc"),
    (troop_get_slot, ":wound_mask_npc", ":npc", slot_troop_wound_mask),
    (neq, ":wound_mask_npc", 0),
    #(assign, ":wounds", 0), 
    (try_begin),(store_and,":y",":wound_mask_npc",wound_head ),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":y",":wound_mask_npc",wound_chest),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":y",":wound_mask_npc",wound_arm  ),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":y",":wound_mask_npc",wound_leg  ),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (troop_set_slot, ":npc", slot_troop_needs_healing, 1), #Set the slot
    (str_store_troop_name, s3, ":npc"),
    #(display_message, "@DEBUG:{s3} is wounded"),
  (try_end),
    (try_for_range, ":npc", new_companions_begin, new_companions_end),
    (main_party_has_troop, ":npc"),
    (troop_get_slot, ":wound_mask_npc", ":npc", slot_troop_wound_mask),
    (neq, ":wound_mask_npc", 0),
    #(assign, ":wounds", 0), 
    (try_begin),(store_and,":y",":wound_mask_npc",wound_head ),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":y",":wound_mask_npc",wound_chest),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":y",":wound_mask_npc",wound_arm  ),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (try_begin),(store_and,":y",":wound_mask_npc",wound_leg  ),(neq,":y",0),(val_add,":wounds",1),(try_end),
    (troop_set_slot, ":npc", slot_troop_needs_healing, 1), #Set the slot
    (str_store_troop_name, s3, ":npc"),
    #(display_message, "@DEBUG:{s3} is wounded"),
  (try_end),
  (try_end),

  #Do we continue?
  (gt, ":wounds",0),
  ], 
    "My men and I have wounds that require more than just time to heal. Can you heal our wounds?", "healer_wound_ask",[]],

[anyone|plyr,"healers_ask", [
  (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
  (assign, ":yes",0),
  (try_for_range, ":stack", 0, ":num_stacks"),
    (party_stack_get_num_wounded, ":wounded", "p_main_party", ":stack"),
    (ge, ":wounded", 1),
    (assign, ":yes",1),
  (try_end),

  (eq, ":yes", 1)], 
    "My men and I are injured, and we do not have the time to wait for them to heal. Can you provide aid?", "healer_injured_ask",[]],

[anyone|plyr,"healers_ask", [], 
    "Nothing.", "close_window",[(call_script, "script_stand_back")]],

[anyone,"healer_who", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s1, "@What? You come to me and you do not know what I do? Take a look around you.^^ Do you see the blood? Do you hear the crying? Do you feel their pain? That is what I do! I break things to make them better again! If you come to me, broken and in pain, I can make you better!"),
  (else_try),
    (str_store_string, s1, "@I am a healer. Come to me when you or your companions are seriously wounded, and I will mend your injuries to the best of my ability."),
  (try_end)], 
    "{s1}.", "healers_ask",[]],

[anyone,"healer_wound_ask", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (str_store_string, s2, "@(Costs 500 Resource, 5 Influence)"),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s1, "@Ha! I can see that! I can do that, yes.. Aside from your blood, this is not for free! {s2}"),
  (else_try),
    (str_store_string, s1, "@Yes, I see that. We can do tend to you yes, but I'll need to send for some ingredients. {s2}"),
  (try_end)], 
    "{s1}", "healers_wound_check",[]],

[anyone,"healer_injured_ask", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (str_store_string, s2, "@(Costs 1000 Resource, 10 Influence)"),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s1, "@I'll have my worms deal with you. They are not the best, but sometimes, they get the job done. Tell me when you want them here. {s2}"),
  (else_try),
    (str_store_string, s1, "@I'll have my assistants tend to your men. They are still learning, so please bear with them. Let me know when you need them. {s2}"),
  (try_end)], 
    "{s1}", "healers_injured_check",[]],

[anyone|plyr,"healers_injured_check", [
  (call_script,"script_update_respoint"),
  (faction_get_slot, ":rps", "$g_talk_troop_faction", slot_faction_respoint),
  (faction_get_slot, ":inf", "$g_talk_troop_faction", slot_faction_influence),
  (ge, ":inf", 10),
  (ge,":rps", 1000)], 
    "Yes, attend to us.", "healers_injured_heal",[]],


[anyone|plyr,"healers_wound_check", [
  (call_script,"script_update_respoint"),
  (faction_get_slot, ":rps", "$g_talk_troop_faction", slot_faction_respoint),
  (faction_get_slot, ":inf", "$g_talk_troop_faction", slot_faction_influence),
  (ge, ":inf", 5),
  (ge,":rps", 500)], 
    "Yes, attend to us.", "healers_wound_heal",[]],


[anyone|plyr,"healers_wound_check", [], 
    "Not right now.", "close_window",[(call_script, "script_stand_back")]],

[anyone|plyr,"healers_injured_check", [], 
    "Not right now.", "close_window",[(call_script, "script_stand_back")]],

[anyone,"healers_injured_heal", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s12, "@Alright! Worms! Get over hear and deal with this!"),
  (else_try),
    (str_store_string, s12, "@Let us begin. My assistants will take care of you and your men."),
  (try_end)], 
    "{s12}", "healers_wound_done",[
      (heal_party, "p_main_party")]],

[anyone,"healers_wound_heal", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s12, "@Alright! This is going to hurt... a lot."),
  (else_try),
    (str_store_string, s12, "@Let us begin. It may take some time. Just relax and leave the rest to me."),
  (try_end)], 
    "{s12}", "healers_wound_done",[
      
      (call_script, "script_add_faction_rps", "$g_talk_troop_faction", -500),
      (call_script, "script_spend_influence_of", 5, "$g_talk_troop_faction"),

      ## Get Faction Side
      (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),

      (try_begin), #Check if wounded - Start with Evil
        (neq, ":side", faction_side_good),

        #If Player is Wounded & Evil Side - Heal then hurt him.
        (try_begin),
          (troop_slot_eq, "trp_player", slot_troop_needs_healing, 1),
          (call_script, "script_healing_routine_full", "trp_player"),
          (troop_set_slot, "trp_player", slot_troop_needs_healing, 0), #Set the Slot
          (store_troop_health, ":plyr_hp", "trp_player"),
          (val_sub, ":plyr_hp", 20),
          (try_begin),
            (le, ":plyr_hp", 0),
            (troop_set_health, "trp_player", 5),
          (else_try),
            (troop_set_health, "trp_player", ":plyr_hp"),
          (try_end),
        (try_end),

        #If any companion is wounded & Evil Side - heal then hurt them
        (try_begin),
          (try_for_range, ":npc", companions_begin, companions_end),
            (troop_slot_eq, ":npc", slot_troop_needs_healing, 1),
            (call_script, "script_healing_routine_full", ":npc"),
            (troop_set_slot, ":npc", slot_troop_needs_healing, 0), #Set the Slot
            (store_troop_health, ":npc_hp", ":npc"),
            (val_sub, ":npc_hp", 20),
            (try_begin),
              (le, ":npc_hp", 0),
              (troop_set_health, ":npc", 5),
            (else_try),
              (troop_set_health, ":npc", ":npc_hp"),
            (try_end),
          (try_end),

          (try_for_range, ":npc", new_companions_begin, new_companions_end),
            (troop_slot_eq, ":npc", slot_troop_needs_healing, 1),
            (call_script, "script_healing_routine_full", ":npc"),
            (troop_set_slot, ":npc", slot_troop_needs_healing, 0), #Set the Slot
            (store_troop_health, ":npc_hp", ":npc"),
            (val_sub, ":npc_hp", 20),
            (try_begin),
              (le, ":npc_hp", 0),
              (troop_set_health, ":npc", 5),
            (else_try),
              (troop_set_health, ":npc", ":npc_hp"),
            (try_end),
          (try_end),
        (try_end),

      #If Player is Wounded & Good Side - Heal then Rest
      (else_try),
        (try_begin),
          (troop_slot_eq, "trp_player", slot_troop_needs_healing, 1),
          (call_script, "script_healing_routine_full", "trp_player"),
          (troop_set_slot, "trp_player", slot_troop_needs_healing, 0), #Set the slot
        (try_end),
        
        #If any companion is wounded & Good Side - heal then rest
        (try_begin),
          (try_for_range, ":npc", companions_begin, companions_end),
            (troop_slot_eq, ":npc", slot_troop_needs_healing, 1),
            (call_script, "script_healing_routine_full", ":npc"),
            (troop_set_slot, ":npc", slot_troop_needs_healing, 0), #Set the slot
          (try_end),

          (try_for_range, ":npc", new_companions_begin, new_companions_end),
            (troop_slot_eq, ":npc", slot_troop_needs_healing, 1),
            (call_script, "script_healing_routine_full", ":npc"),
            (troop_set_slot, ":npc", slot_troop_needs_healing, 0), #Set the slot
          (try_end),
        (try_end),
      (try_end),
      ]],

[anyone,"healers_wound_done", [
  (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
  (try_begin),
    (neq, ":side", faction_side_good),
    (str_store_string, s12, "@All done! Ha! You didn't scream much, impressive! Now go, leave me be."),
  (else_try),
    (str_store_string, s12, "@We've done what We can. Now you and your men need some rest."),
  (try_end)], 
    "{s12}", "close_window",[
      (call_script, "script_stand_back"),
      (faction_get_slot, ":side", "$g_talk_troop_faction", slot_faction_side),
      (try_begin),
        (eq, ":side", faction_side_good),
        (change_screen_map),
        (rest_for_hours, 8,15,0),
      (try_end)]],

# Healers Dialogue END
# Morale Troops Dialogue Start - Kham

[anyone,"start", [
  (this_or_next|eq, "$g_talk_troop", "trp_hungry_orc"), 
  (eq, "$g_talk_troop", "trp_hungry_uruk"),
  (store_random_in_range, ":random", 0, 100),
  (try_begin),
    (le, ":random", 50),
    (str_store_string, s1, "@Boss, the lads are hungry! We're doing all the hard work and still we're starving!"),
  (else_try),
    (str_store_string, s1, "@Master, the lads are hungry! We can't do all this fighting on empty stomachs!"),
  (try_end),
    ],"{s1}", "hungry_orc_1", []],

[anyone|plyr,"hungry_orc_1", [],"What do you expect me to do about it, rat?", "hungry_orc_2", []],
[anyone,"hungry_orc_2", [],"Those weaklings over there are no use in a proper fight, anyway. Let us eat THEM!", "hungry_orc_choice", []],
[anyone|plyr,"hungry_orc_choice", [],"All right, grab them! [Kill a few weaklings to feed your orcs.]", "hungry_orc_eat", []],
[anyone|plyr,"hungry_orc_choice", [],"No way. None of my men get eaten! Fall back in line or I'll have you eat your own tongue! [Leadership Check]", "hungry_orc_no_check", []],
[anyone,"hungry_orc_eat", [
  (store_random_in_range, ":random", 0, 100),
  (try_begin),
    (le, ":random", 50),
    (str_store_string, s1, "@Yes! With proper fed bellies, we'll serve you twice as well!"),
  (else_try),
    (str_store_string, s1, "@As you command, master, heh heh. Meat's back on the menu, boys!"),
  (try_end),],"{s1}", "close_window", 
  [(party_get_num_companions, ":troops", "p_main_party"),
   (val_div, ":troops",10), #Eat 10% of your low level troops
   (val_min, ":troops", 10), #Up to a max of 10
   (call_script, "script_remove_highest_or_lowest_level_troop", "p_main_party", ":troops", 0),
   (assign, reg1, ":troops"),
   (display_message, "@Your Orcs & Uruks ate {reg1} men!", color_bad_news),
   (party_get_morale, ":morale", "p_main_party"),
   (try_begin), #If the player has low morale and no food: low morale constant + 10 = Current Player Morale + X
    (le, ":morale", low_party_morale),
    (store_sub, ":diff", low_party_morale, ":morale"),
    (store_add, ":morale_gain", ":diff", 10),
    (call_script, "script_change_player_party_morale", ":morale_gain"),
  (else_try),
    (call_script, "script_change_player_party_morale", 8), #If the player just has no food (ie, party morale is > low morale constant, we'll just add +5 morale.
  (try_end),
  (troop_set_slot, "trp_player", slot_troop_state, 99), #use this to make sure trigger fires again after 36 hours.
  #(change_screen_map),
  (jump_to_menu, "mnu_precannibalism"),
  ]],

[anyone,"hungry_orc_no_check", 
  [(party_get_skill_level, ":leadership", "p_main_party", skl_leadership),
   (assign, ":chance", 100),
    (try_begin),
      (gt, ":leadership", 5),
      (assign, ":continue",1),
    (else_try),
      (eq, ":leadership", 5),
      (assign, ":chance", 80),
    (else_try),
      (eq, ":leadership", 4),
      (assign, ":chance", 60),
    (else_try),
      (eq, ":leadership", 3),
      (assign, ":chance", 40),
    (else_try),
      (eq, ":leadership", 2),
      (assign, ":chance", 20),
    (else_try),
      (assign, ":chance", 10),
    (try_end),
    (party_get_morale, ":morale", "p_main_party"),
    (try_begin),
      (le, ":morale", low_party_morale),
      (val_sub, ":chance", 10),
    (try_end),
    (store_random_in_range, ":random", 0, 100),
    (str_clear, s2),
    (try_begin),
      (this_or_next| eq, ":continue", 1),
      (              le, ":random", ":chance"),
      (assign, "$leadership_check",1),
      (str_store_string, s2, "@Yes master! As you command, master!"),
    (else_try),
      (assign, "$leadership_check", 0),
      (str_store_string, s2, "@Harr harr harr! You don't frighten ME! Next time it's YOU that we eat!"),
    (try_end),
    
    ##Debug
    #(assign, reg1, ":random"),
    #(assign, reg2, ":chance"),
    #(assign, reg3, ":leadership"),
    #(display_message, "@{reg1} random number - {reg2} chance - {reg3} leadership")

    ],"{s2}", "close_window", 
  [
   (try_begin),
     (eq, "$leadership_check",1),
     (party_get_morale, ":morale", "p_main_party"),
     (try_begin),
      (le, ":morale", low_party_morale),
      (store_sub, ":diff", low_party_morale, ":morale"),
      (store_add, ":morale_gain", ":diff", 2),
      (call_script, "script_change_player_party_morale", ":morale_gain"),
     (else_try),
      (call_script, "script_change_player_party_morale", 4), #If the player just has no food (ie, party morale is > low morale constant, we'll just add +4 morale.
     (try_end),
   (else_try),
     (party_get_num_companions, ":troops", "p_main_party"),
     #(val_div, ":troops",20), #Eat 20% of your low level troops
     (val_min, ":troops", 15), #Up to a max of 10
     (call_script, "script_remove_highest_or_lowest_level_troop", "p_main_party", ":troops", 0),
     (assign, reg1, ":troops"),
     (display_message, "@Your Orcs & Uruks ate {reg1} men!", color_bad_news),
     (party_get_morale, ":morale", "p_main_party"),
     (try_begin), #If the player has low morale and no food: low morale constant + 2 = Current Player Morale + X
      (le, ":morale", low_party_morale),
      (store_sub, ":diff", low_party_morale, ":morale"),
      (store_add, ":morale_gain", ":diff", 2),
      (call_script, "script_change_player_party_morale", ":morale_gain"),
    (else_try),
      (call_script, "script_change_player_party_morale", 4), #If the player just has no food (ie, party morale is > low morale constant, we'll just add +5 morale.
    (try_end),
   (try_end),
   (troop_set_slot, "trp_player", slot_troop_state, 99), #use this to make sure trigger fires again after 36 hours.
   #(change_screen_map)
   (jump_to_menu, "mnu_precannibalism"),
   ]],

[anyone,"start", [(this_or_next|eq, "$g_talk_troop", "trp_longing_lorien"), (this_or_next|eq, "$g_talk_troop", "trp_longing_imladris"),(eq, "$g_talk_troop", "trp_longing_woodelf")],"Look, my {lord/lady}, gulls! A wonder they are to me and a trouble to my heart.", "sad_elf_1", []],
[anyone|plyr,"sad_elf_1", [],"I hear their voices. What news do they bring?", "sad_elf_2", []],
[anyone,"sad_elf_2", [],"Ah, tales from the sea. And from beyond. My {lord/lady}, I have grown weary of this war we fight, weary of this soil we drag ourselves on. I fear Ennor (Middle-Earth) is lost for me. Let me leave!", "sad_elf_choice", []],
[anyone|plyr,"sad_elf_choice", [],"I feel your pain. You have done your share in this war. You may leave.", "sad_elf_leave", []],
[anyone|plyr,"sad_elf_choice", [],"The Elves must not abandon Middle-earth to the shadow. This war we fight not for ourselves and each of us will have to play their role. I cannot give you leave. [Leadership Check]", "sad_elf_no", []],

[anyone,"sad_elf_leave", [],"Thank you, my {lord/lady}!^^To the Sea, to the Sea! The white gulls are crying,^The wind is blowing, and the white foam is flying.^West, west away, the round sun is falling.", "close_window", 
[(call_script, "script_remove_highest_or_lowest_level_troop", "p_main_party", 1, 1), #Only 1 high level elf leaves.
 (display_message, "@One {s6} left the party.", color_bad_news),
 (party_get_morale, ":morale", "p_main_party"),
 (set_show_messages, 0),
 (try_begin),
  (le, ":morale", low_party_morale),
  (store_sub, ":diff", low_party_morale, ":morale"),
  (store_add, ":morale_gain", ":diff", 10),
  (call_script, "script_change_player_party_morale", ":morale_gain"),
 (else_try),
  (call_script, "script_change_player_party_morale", 5),
 (try_end),
 (set_show_messages, 1),
 (troop_set_slot, "trp_player", slot_troop_state, 99), #use this to make sure trigger fires again after 36 hours.
 #(change_screen_map)
 (jump_to_menu, "mnu_precannibalism"),
 ]],

[anyone,"sad_elf_no", [
    (party_get_skill_level, ":leadership", "p_main_party", skl_leadership),
    (assign, ":chance", 100),
    (try_begin),
      (gt, ":leadership", 5),
      (assign, ":continue",1),
    (else_try),
      (eq, ":leadership", 5),
      (assign, ":chance", 80),
    (else_try),
      (eq, ":leadership", 4),
      (assign, ":chance", 60),
    (else_try),
      (eq, ":leadership", 3),
      (assign, ":chance", 40),
    (else_try),
      (eq, ":leadership", 2),
      (assign, ":chance", 20),
    (else_try),
      (assign, ":chance", 10),
    (try_end),
    (try_begin),
      (troop_slot_eq, "trp_traits", slot_trait_elf_friend, 1),
      (val_add, ":chance", 20),
    (try_end),
    (store_random_in_range, ":random", 0, 100),
    (str_clear, s2),
    (try_begin),
      (this_or_next| eq, ":continue", 1),
      (              le, ":random", ":chance"),
      (assign, "$leadership_check",1),
      (str_store_string, s2, "@I understand. I will stay with you. For a while."),
    (else_try),
      (assign, "$leadership_check", 0),
      (str_store_string, s2, "@I have played my role for many long years, for many lifetimes of mortal men. This war is for Mankind to fight. I will leave for the West and some may decide to follow me."),
    (try_end),
    
    ##Debug
    #(assign, reg1, ":random"),
    #(assign, reg2, ":chance"),
    #(assign, reg3, ":leadership"),
    #(display_message, "@{reg1} random number - {reg2} chance - {reg3} leadership")

    ],"{s2}.", "close_window", 

  [
   (try_begin),
     (eq, "$leadership_check",1),
     (party_get_morale, ":morale", "p_main_party"),
     (try_begin),
      (le, ":morale", low_party_morale),
      (store_sub, ":diff", low_party_morale, ":morale"),
      (store_add, ":morale_gain", ":diff", 4),
      (call_script, "script_change_player_party_morale", ":morale_gain"),
     (else_try),
      (call_script, "script_change_player_party_morale", 6),
     (try_end),
   (else_try),
     (store_random_in_range, ":ran_troops", 0, 100),
     (assign, ":troops", 1),
     (try_begin),
      (le, ":ran_troops", 50),
      (assign, ":troops",2),
     (else_try),
      (assign, ":troops",3),
     (try_end),
     (call_script, "script_remove_highest_or_lowest_level_troop", "p_main_party", ":troops", 1),
     (assign, reg1, ":troops"),
     (display_message, "@{reg1} Veteran Elves decided to leave your party.", color_bad_news),
   (try_end),
   (party_get_morale, ":morale", "p_main_party"),
   (set_show_messages, 0),
   (try_begin),
    (le, ":morale", low_party_morale),
    (store_sub, ":diff", low_party_morale, ":morale"),
    (store_add, ":morale_gain", ":diff", 2),
    (call_script, "script_change_player_party_morale", ":morale_gain"),
   (else_try),
    (call_script, "script_change_player_party_morale", 4),
   (try_end),
   (set_show_messages, 1),
   (troop_set_slot, "trp_player", slot_troop_state, 99), #use this to make sure trigger fires again after 36 hours.
   #(change_screen_map)
   (jump_to_menu, "mnu_precannibalism"),
   ]],

# Morale Troops Dialogue END - Kham



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
 You must have confused me with someone else.", "fugitive_3",[(call_script, "script_encounter_agent_draw_weapon"),]],

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



#Tavern Talk (with troops)
# [anyone, "start", [(eq, "$talk_context", tc_tavern_talk),
                     # (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                     # (party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                     # (gt, ":mercenary_amount", 0),
                     # (store_sub, reg3, ":mercenary_amount", 1),
                     # (store_sub, reg4, reg3, 1),
                     # (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                     # (assign, ":join_cost", reg0),
                     # (store_mul, reg5, ":mercenary_amount", reg0),
                     # (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                     # (val_min, ":mercenary_amount", ":free_capacity"),
                     # (store_troop_gold, ":cur_gold", "trp_player"),
                     # (try_begin),
                       # (gt, ":join_cost", 0),
                       # (val_div, ":cur_gold", ":join_cost"),
                       # (val_min, ":mercenary_amount", ":cur_gold"),
                     # (try_end),
                     # (assign, "$temp", ":mercenary_amount")],
# "Do you have a need for mercenaries, Commander?\
 # {reg3?Me and {reg4?{reg3} of my mates:one of my mates} are:I am} looking for a master.\
 # We'll join you for {reg5} denars.", "mercenary_tavern_talk", []],

# [anyone, "start", [(eq, "$talk_context", tc_tavern_talk)], "Any orders, Commander?", "mercenary_after_recruited", []],
# [anyone|plyr, "mercenary_after_recruited", [], "Make your preparations. We'll be moving at dawn.", "mercenary_after_recruited_2", []],
# [anyone|plyr, "mercenary_after_recruited", [], "Take your time. We'll be staying in this town for a while.", "mercenary_after_recruited_2", []],
# [anyone, "mercenary_after_recruited_2", [], "Yes, Commander. We'll be ready when you tell us to leave.", "close_window", [(call_script,"script_stand_back"),]],

# [anyone|plyr, "mercenary_tavern_talk", [(party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                                          # (eq, ":mercenary_amount", "$temp"),
                                          # (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          # (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          # (store_mul, reg5, "$temp", reg0)],
# "All right. I will hire all of you. Here is {reg5} denars.", "mercenary_tavern_talk_hire", []],

# [anyone|plyr, "mercenary_tavern_talk", [(party_get_slot, ":mercenary_amount", "$g_encountered_party", slot_center_mercenary_troop_amount),
                                          # (lt, "$temp", ":mercenary_amount"),
                                          # (gt, "$temp", 0),
                                          # (assign, reg6, "$temp"),
                                          # (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                                          # (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                                          # (store_mul, reg5, "$temp", reg0)],
# "All right. But I can only hire {reg6} of you. Here is {reg5} denars.", "mercenary_tavern_talk_hire", []],


# [anyone, "mercenary_tavern_talk_hire", [(store_random_in_range, ":rand", 0, 4),
                                          # (try_begin),
                                            # (eq, ":rand", 0),
                                            # (gt, "$temp", 1),
                                            # (str_store_string, s17,
                                             # "@You chose well, {sir/madam}. My lads know how to keep their word and earn their pay."),
                                          # (else_try),
                                            # (eq, ":rand", 1), 
                                            # (str_store_string, s17,
                                             # "@Well done, {sir/madam}. Keep the money and wine coming our way, and there's no foe in Calradia you need fear."),
                                          # (else_try),
                                            # (eq, ":rand", 2), 
                                            # (str_store_string, s17,
                                             # "@We are at your service, {sir/madam}. Point us in the direction of those who need hurting, and we'll do the rest."),
                                          # (else_try),
                                            # (str_store_string, s17,
                                             # "@You will not be dissapointed {sir/madam}. You will not find better warriors in all Calradia."),
                                          # (try_end)],
# "{s17}", "close_window", [  (call_script,"script_stand_back"),
              # (party_get_slot, ":mercenary_troop", "$g_encountered_party", slot_center_mercenary_troop_type),
                            # (call_script, "script_game_get_join_cost", ":mercenary_troop"),
                            # (store_mul, ":total_cost", "$temp", reg0),
                            # (troop_remove_gold, "trp_player", ":total_cost"),
                            # (party_add_members, "p_main_party", ":mercenary_troop", "$temp"),
                            # (party_set_slot, "$g_encountered_party", slot_center_mercenary_troop_amount, 0)]],

# [anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          # (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          # (ge, ":free_capacity", 1)],
# "That sounds good. But I can't afford to hire any more men right now.", "tavern_mercenary_cant_lead", []],
  
# [anyone, "tavern_mercenary_cant_lead", [], "That's a pity. Well, {reg3?we will:I will} be lingering around here for a while,\
 # if you need to hire anyone.", "close_window", [(call_script,"script_stand_back"),]],
  
# [anyone|plyr, "mercenary_tavern_talk", [(eq, "$temp", 0),
                                          # (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                                          # (eq, ":free_capacity", 0)],
# "That sounds good. But I can't lead any more men right now.", "tavern_mercenary_cant_lead", []],

# [anyone|plyr, "mercenary_tavern_talk", [], "Sorry. I don't need any other men right now.", "close_window", [(call_script,"script_stand_back"),]],

#Trainers
#Reward for results
[anyone,"start", [(is_between, "$g_talk_troop", training_ground_trainers_begin, training_ground_trainers_end),
      (troop_slot_eq, "$g_talk_troop", slot_troop_trainer_waiting_for_result, 1),
      (troop_get_slot, ":training_mode", "$g_talk_troop", slot_troop_trainer_training_mode),
      (eq, ":training_mode", abm_gauntlet)],
   "You have survived up to Gauntlet wave {reg2}. {s4}", "trainer_pretalk",[
      (troop_set_slot, "$g_talk_troop", slot_troop_trainer_waiting_for_result, 0),
      (troop_get_slot, ":wave_reached", "$g_talk_troop", slot_troop_trainer_training_result),
      (val_max, ":wave_reached", 1), # (CC) Should prevent losing RPs due to evacuating the training grounds.
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

[anyone,"mayor_begin", [(check_quest_active, "qst_deal_with_night_bandits"),
                          (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_succeeded, "qst_deal_with_night_bandits"), (assign, reg14, 150),(str_store_faction_name, s14, "$ambient_faction"),],
"Very nice work, {playername}, you made short work of those lawless curs!"+earned_reg14_rp_of_s14, "lord_deal_with_night_bandits_completed",[
    (call_script, "script_finish_quest", "qst_deal_with_night_bandits", 100)]],

[anyone|plyr,"lord_deal_with_night_bandits_completed", [], "They had it coming.", "close_window",[(call_script,"script_stand_back"),]],

# CppCoder: Improved so the mayor accepts better metal scraps    

# Medium Grade Scraps
[anyone|plyr,"mayor_talk", [(check_quest_active,"qst_deliver_iron"),
        (eq, 1, 0), # enable/disable switch
                              (quest_slot_eq, "qst_deliver_iron", slot_quest_target_center, "$g_encountered_party"),
                              (quest_get_slot, ":quest_target_item", "qst_deliver_iron", slot_quest_target_item),
            (eq, ":quest_target_item", "itm_metal_scraps_bad"),
                              (quest_get_slot, ":quest_target_amount", "qst_deliver_iron", slot_quest_target_amount),
                              (store_item_kind_count, ":item_count", "itm_metal_scraps_medium"),
                              (ge, ":item_count", ":quest_target_amount"),
                              (assign, reg9, ":quest_target_amount"),
                              (str_store_item_name, s3, ":quest_target_item"),
                              (str_store_item_name, s4, "itm_metal_scraps_medium")],
"I've brought you better quality metal, {reg9} units of {s4}, when you requested {s3}.", "mayor_deliver_iron",
    [
      (assign, "$temp", 0),
            (quest_set_slot, "qst_deliver_iron", slot_quest_target_item, "itm_metal_scraps_medium"),
                        (quest_get_slot, ":quest_target_amount", "qst_deliver_iron", slot_quest_target_amount),
                        (quest_get_slot, ":quest_target_item", "qst_deliver_iron", slot_quest_target_item),     
              (store_item_value, ":item_value", ":quest_target_item"),
              (val_mul, ":item_value", 2), #2x profit
              (store_mul, ":quest_gold_reward", ":quest_target_amount", ":item_value"),
            (quest_set_slot, "qst_deliver_iron", slot_quest_gold_reward, ":quest_gold_reward"),
    ]],

# High Grade Scraps
[anyone|plyr,"mayor_talk", [(check_quest_active,"qst_deliver_iron"),
                              (quest_slot_eq, "qst_deliver_iron", slot_quest_target_center, "$g_encountered_party"),
                              (quest_get_slot, ":quest_target_item", "qst_deliver_iron", slot_quest_target_item),
            (eq|this_or_next, ":quest_target_item", "itm_metal_scraps_bad"),
            (eq, ":quest_target_item", "itm_metal_scraps_medium"),
                              (quest_get_slot, ":quest_target_amount", "qst_deliver_iron", slot_quest_target_amount),
                              (store_item_kind_count, ":item_count", "itm_metal_scraps_good"),
                              (ge, ":item_count", ":quest_target_amount"),
                              (assign, reg9, ":quest_target_amount"),
                              (str_store_item_name, s3, ":quest_target_item"),
                              (str_store_item_name, s4, "itm_metal_scraps_good")],
"I've brought you better quality metal, {reg9} units of {s4}, when you requested {s3}.", "mayor_deliver_iron",
    [
      (assign, "$temp", 0),
            (quest_set_slot, "qst_deliver_iron", slot_quest_target_item, "itm_metal_scraps_good"),
                        (quest_get_slot, ":quest_target_item", "qst_deliver_iron", slot_quest_target_item), 
                        (quest_get_slot, ":quest_target_amount", "qst_deliver_iron", slot_quest_target_amount),   
              (store_item_value, ":item_value", ":quest_target_item"),
              (val_mul, ":item_value", 2), #2x profit
              (store_mul, ":quest_gold_reward", ":quest_target_amount", ":item_value"),
            (quest_set_slot, "qst_deliver_iron", slot_quest_gold_reward, ":quest_gold_reward"),
    ]],

# Original scraps

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

#Kham - Sea Battle - Volunteer START
[anyone|plyr,"mayor_talk", [(check_quest_active,"qst_blank_quest_03"),
                            (neg|check_quest_succeeded, "qst_blank_quest_03"),
                            (quest_slot_eq, "qst_blank_quest_03", slot_quest_object_center, "$g_encountered_party"),
                            (quest_get_slot, ":quest_target_center", "qst_blank_quest_03", slot_quest_target_center),
                            (str_store_party_name, s4, ":quest_target_center"),
                            (quest_get_slot, ":giver", "qst_blank_quest_03", slot_quest_object_troop),
                            (str_store_troop_name, s3, ":giver"),
                            (try_begin),
                              (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
                              (str_store_string, s5, "@We've been sent by {s3}. We have come to join our strength to yours."),
                            (else_try),
                              (str_store_string, s5, "@{s3} has sent us, to join the fleet attacking {s4}."),
                            (try_end),
                            ],
"{s5}", "mayor_sea_battle_start",[]],

[anyone, "mayor_sea_battle_start", [],
  "Excellent! We are in dire need of crewmen. Are you ready to board the ships?", "mayor_sea_battle_question", []],

[anyone|plyr, "mayor_sea_battle_question",[],
  "Yes, I am.", "mayor_sea_battle_yes", []],

[anyone|plyr, "mayor_sea_battle_question", [],
  "I need some time to get ready.", "mayor_sea_battle_no", []],

[anyone, "mayor_sea_battle_yes", [],
  "Good. Have your troops board the ship now, we will set sail soon.", "close_window", 
    [(jump_to_menu, "mnu_sea_battle_quest")]],

[anyone, "mayor_sea_battle_no", [],
  "Hurry, we don't have much time before we must set sail.", "close_window", []],

#Kham - Sea Battle - Volunteer END
#Kham - Reinforce Center Completion

[anyone|plyr,"mayor_talk", [(check_quest_active,"qst_blank_quest_16"),
                            (quest_slot_eq, "qst_blank_quest_16", slot_quest_object_center, "$g_encountered_party"),
                            (quest_get_slot, ":to_reinforce", "qst_blank_quest_16", slot_quest_target_center),
                            (str_store_party_name, s3, ":to_reinforce"),
                            (check_quest_succeeded, "qst_blank_quest_16")],
"I have reinforced {s3} as you have asked me to.", "mayor_reinforced_center_finished",[]],

[anyone,"mayor_reinforced_center_finished", [
  (quest_get_slot, ":troops_given", "qst_blank_quest_16", slot_quest_current_state),
  (val_mul, ":troops_given", -1),
  (try_begin),
    (gt, ":troops_given", 0),
    (assign, reg10, ":troops_given"),
    (str_store_string, s4, "@Excellent, {playername}! I heard that you gave them more than what I requested. That is great work.^^ Here, take this as an extra reward for exceeding our expectations. ^^ We need to win this war as soon as possible."),
  (else_try),
    (assign, reg10, 0),
    (str_store_string, s4, "@Excellent, {playername}. That will surely help them out. We need to win this war as soon as possible."),
  (try_end)],
"{s4}", "close_window", [
  (call_script, "script_finish_quest", "qst_blank_quest_16", 100),
  (quest_get_slot, ":to_reinforce", "qst_blank_quest_16", slot_quest_target_center),
  (str_store_party_name, s1, ":to_reinforce"),
  (store_faction_of_party, ":fac", ":to_reinforce"),
  (str_store_faction_name, s2, ":fac"),
  (faction_get_slot,":strength",":fac",slot_faction_strength_tmp),
  (val_add, ":strength", 80), #50 Str Points increase for completing the quest
  (assign, reg50, 80),
  (display_message, "@Reinforcing {s1} has strengthened {s2}. ({s2} has gained {reg50} faction strength).", color_good_news),
  (faction_set_slot,":fac",slot_faction_strength_tmp,":strength"),
  (try_begin),
    (gt, reg10, 0),
    (is_between, reg10, 1, 16),
    (troop_add_items, "trp_player", "itm_metal_scraps_good", 2),
    (call_script, "script_increase_rank", "$g_talk_troop_faction", 12),
  (else_try),
    (gt, reg10, 0),
    (gt, reg10, 16),
    (troop_add_items, "trp_player", "itm_metal_scraps_good",4),
    (call_script, "script_increase_rank", "$g_talk_troop_faction", 18),
  (try_end),]],

#Kham - Reinforce Center Completion END
#### Kham Kill Quest Bandit Completion Start ####

[anyone,"mayor_begin", [
    (check_quest_active, "qst_blank_quest_17"),
    (check_quest_succeeded, "qst_blank_quest_17"),
    (quest_slot_eq, "qst_blank_quest_17", slot_quest_object_troop,"$g_talk_troop"),
    (try_begin),
      (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
      (str_store_string, s5, "@The watchmen in the city have reported a remarkable decrease in ambushes. You have done your job well. Thank you, {playername}."),
    (else_try),
      (str_store_string, s5, "@Our guards have seen the vermin run away with their tails tucked between their legs. You have done well in showing these pests that we control this area."),
    (try_end),
    ],
"{s5}", "mayor_kill_bandit_quest_complete",[
    (call_script, "script_finish_quest", "qst_blank_quest_17", 100),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
    ]],

[anyone|plyr,"mayor_kill_bandit_quest_complete", [
    (try_begin),
      (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
      (str_store_string, s5, "@It was nothing. I will keep watch should they resurface."),
    (else_try),
      (str_store_string, s5, "@Slaying these maggots was nothing. I'll keep watch should they become bold again."),
    (try_end),
    ],
"{s5}", "close_window",[
    (call_script, "script_stand_back"),
    ]],

[anyone,"mayor_begin", [
    (check_quest_active, "qst_blank_quest_17"),
    (check_quest_failed, "qst_blank_quest_17"),
    (quest_slot_eq, "qst_blank_quest_17", slot_quest_object_troop,"$g_talk_troop"),],
"I have heard that you failed to do what I asked you to. Disappointing, {playername}.", "kill_quest_bandits_failed",[
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
	(try_begin), #find remaining quest target parties, make them normal parties (spawned from Quest Helper Trigger )
	   (quest_get_slot, ":target_template", "qst_blank_quest_17", slot_quest_target_party_template),
		(try_for_parties, ":quest_targets"),
			(party_get_template_id, ":party_template", ":quest_targets"),
			(eq, ":party_template", ":target_template"),
			(party_set_faction, ":quest_targets", "fac_outlaws"),
			(party_set_flags, ":quest_targets", pf_quest_party, 0),
		(try_end),
	(try_end),
    (cancel_quest, "qst_blank_quest_17"),
    ]],

[anyone|plyr, "kill_quest_bandits_failed",[],
  "I will do better next time.", "close_window",[],
  ],
#### Kham Kill Quest Bandit Completion END ####


[anyone|plyr,"mayor_talk", [(check_quest_active,"qst_deliver_food"),
                            (quest_slot_eq, "qst_deliver_food", slot_quest_target_center, "$g_encountered_party"),
                            #(quest_get_slot, ":quest_target_item", "qst_deliver_food", slot_quest_target_item),
                            (quest_get_slot, ":quest_target_amount", "qst_deliver_food", slot_quest_target_amount),
              (assign, ":item_count",0),
              (try_for_range, ":food_item", food_begin, food_end),
                (neq, ":food_item", "itm_lembas"), # Lembas don't get counted - Kham
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
      (neq, ":food_item", "itm_lembas"), # Lembas don't get taken - Kham
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
	  (quest_get_slot,":total_looters","qst_deal_with_looters",slot_quest_target_amount),
      (store_num_parties_destroyed_by_player, ":num_looters_destroyed", ":looter_template"),
      (party_template_get_slot,":previous_looters_destroyed",":looter_template",slot_party_template_num_killed),
      (val_sub,":num_looters_destroyed",":previous_looters_destroyed"),
      (quest_get_slot,":looters_paid_for","qst_deal_with_looters",slot_quest_current_state),
      (store_sub,":looter_bounty",":num_looters_destroyed",":looters_paid_for"), 
	  (val_sub,":total_looters",":looters_paid_for"), #get remaining looter parties, limit the reward (so we can avoid exploiting the quest helper trigger)
	  (val_min,":looter_bounty",":total_looters"),
	  (assign,reg14,":looter_bounty"),(assign,reg15,40),
	  (call_script, "script_increase_rank", "$g_talk_troop_faction", ":looter_bounty"),
	  (val_mul, ":looter_bounty", 2),
	  (call_script, "script_change_player_relation_with_center", "$current_town", ":looter_bounty"),
      (val_mul,":looter_bounty",20),
      #(call_script, "script_troop_add_gold","trp_player",":looter_bounty"),
      (call_script, "script_add_faction_rps", "$g_talk_troop_faction", ":looter_bounty"),
	  #(call_script, "script_change_player_relation_with_center", "$current_town", 2),
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
        (party_is_active, ":cur_party_no"),
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

[anyone|plyr,"mayor_talk", [
                              (store_partner_quest, ":partner_quest"),
                              (try_begin), #Reinforce Center Exception
                                (this_or_next|check_quest_active, "qst_blank_quest_16"),
                                (check_quest_active, "qst_blank_quest_17"),
                                (assign, ":partner_quest", 1),
                              (try_end),
                              (lt, ":partner_quest", 0),
                              (eq,"$merchant_quest_last_offerer", "$g_talk_troop"),
                              (ge,"$merchant_offered_quest",0)],
"About that task you needed me to do...", "merchant_quest_last_offered_job",[]],

[anyone|plyr,"mayor_talk", [(store_partner_quest,reg2),(ge,reg2,0)],
"About the task you gave me...", "merchant_quest_about_job",[]],

[anyone|plyr,"mayor_talk", [], 
"I want to know the location of someone.", "mayor_talk_ask_location",[]],

# Guild Master + Companion Talk START

[anyone|plyr,"mayor_talk", [
  (troop_slot_ge, "$g_talk_troop", slot_troop_gm_companion_ask, 0), 
  (troop_get_slot, ":intro", "$g_talk_troop", slot_troop_gm_companion_ask),
  (str_store_string, s55, ":intro"),
], 
"{s55}", "mayor_talk_ask_companion",[]],

[anyone,"mayor_talk_ask_companion", [
  (party_slot_eq, "$current_town", slot_party_has_companion, 1),
  (troop_get_slot, ":companion", "$g_talk_troop", slot_troop_gm_companion_1),
  (try_begin),
    (this_or_next|eq, "$current_town", "p_town_henneth_annun"),
    (eq, "$current_town", "p_town_hornburg"),
    (troop_get_slot, ":companion", "$g_talk_troop", slot_troop_gm_companion_2),
  (try_end),
  (str_store_string, s55, ":companion"),
], 
"{s55}", "mayor_talk_companion_thanks",[]],

[anyone,"mayor_talk_ask_companion", [
  (neg|party_slot_eq, "$current_town", slot_party_has_companion, 1),
  (troop_get_slot, ":companion", "$g_talk_troop", slot_troop_gm_companion_none),
  (str_store_string, s55, ":companion"),
], 
"{s55}", "mayor_talk_companion_no_thanks",[]],

[anyone|plyr,"mayor_talk_companion_thanks", [
  (party_slot_eq, "$current_town", slot_party_has_companion, 1),
  (troop_get_slot, ":companion_found", "$g_talk_troop", slot_troop_gm_companion_player_found),
  (str_store_string, s55, ":companion_found"),
], 
"{s55}", "mayor_talk",[]],

[anyone|plyr,"mayor_talk_companion_no_thanks", [
  (neg|party_slot_eq, "$current_town", slot_party_has_companion, 1),
  (troop_get_slot, ":companion", "$g_talk_troop", slot_troop_gm_companion_player_none),
  (str_store_string, s55, ":companion"),
], 
"{s55}", "mayor_talk",[]],

[anyone|plyr,"mayor_talk", [(eq, "$cheat_mode", 1)], "Increase Relation", "mayor_friendly_pretalk",[(call_script, "script_change_player_relation_with_center", "$current_town", 5),]],

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

[anyone,"mayor_talk_ask_location", [], "I'll do what I can. I only hear their coming and going if they were recently in another center. If they are not in a center, I hear about the region they are around from caravans.", "mayor_talk_ask_location_2",[]],

[anyone|plyr|repeat_for_troops,"mayor_talk_ask_location_2", [(store_repeat_object, ":troop_no"),
                                                              (store_troop_faction, ":talk_faction", "$g_talk_troop"),
                                                              (is_between, ":troop_no", heroes_begin, heroes_end),
                                                              (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                                                              (store_troop_faction, ":faction_no", ":troop_no"),
                                                              (eq, ":talk_faction", ":faction_no"),
                                                              (str_store_troop_name, s1, ":troop_no")],
"{s1}", "mayor_talk_ask_location_3",[(store_repeat_object, "$hero_requested_to_learn_location")]],

[anyone|plyr,"mayor_talk_ask_location_2", [], "Never mind.", "mayor_pretalk",[]],

[anyone,"mayor_talk_ask_location_3",
   [ (call_script, "script_guild_master_update_troop_location_notes", "$hero_requested_to_learn_location", 1),
     (call_script, "script_guild_master_get_information_about_troops_position", "$hero_requested_to_learn_location", 0)], 
"{s1}", "mayor_pretalk",[]],
  


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

#Kham - Reinforce Center INIT

[anyone,"merchant_quest_requested", [(eq,"$random_merchant_quest_no","qst_blank_quest_16"),], 
"Thanks for offering to help.^^\
This war has waged for so long that some of our centers are no longer looking good.^^\
Perhaps you can go and reinforce a center in need...", "merchant_quest_brief",[]],

[anyone,"merchant_quest_brief", [
  (eq,"$random_merchant_quest_no","qst_blank_quest_16"),
  (quest_get_slot, ":target_center", "qst_blank_quest_16", slot_quest_target_center),
  (str_store_party_name, s5, ":target_center"),
  (quest_get_slot, ":amount", "qst_blank_quest_16", slot_quest_target_amount),
  (assign, reg5, ":amount"),],
"{s5} has been battered by the enemy. We will need to send help. ^^\
I need someone to reinforce {s5} by at least {reg5} soldiers.^^ \
It does not matter if they are experienced or not. They just need whatever you can provide.^^ \
If you are able to do this, they can withstand more attacks.^^ What do you say?", "merchant_quest_brief_reinforce_center",[]], 

[anyone|plyr,"merchant_quest_brief_reinforce_center", [],
"Alright. I will do what I can.", "merchant_quest_taken",[
    (quest_get_slot, reg5, "qst_blank_quest_16", slot_quest_target_amount),
    (quest_get_slot, reg6, "qst_blank_quest_16", slot_quest_expiration_days),
    (quest_get_slot, ":object_center", "qst_blank_quest_16", slot_quest_object_center),
    (quest_get_slot, ":target_center", "qst_blank_quest_16", slot_quest_target_center),
    (quest_set_slot, "qst_blank_quest_16", slot_quest_current_state, reg5),
    (str_store_troop_name, s9, "$g_talk_troop"),
    (str_store_party_name_link, s3, ":target_center"),
    (str_store_party_name_link, s4, ":object_center"),
    (str_clear, s6), 
    (setup_quest_text,"qst_blank_quest_16"),
    (str_store_string, s2, "@The {s9} of {s4} asked you to reinforce {s3} with at least {reg5} troops within {reg6} days. Speak to {s3}'s barracks master. The quality of the troop you provide does not matter."),
    (call_script, "script_start_quest", "qst_blank_quest_16", "$g_talk_troop"),
    (str_store_string, s5, "@You have reinforced {s3} with 0 troops."),
    (add_quest_note_from_sreg, "qst_blank_quest_16", 3, s5, 0),
 ]],

[anyone|plyr,"merchant_quest_brief_reinforce_center", [], "I am sorry, you'll need to find someone else for that.", "merchant_quest_stall",[]],

#Kham - Reinforce Center INIT END

## Kham Kill Quest Bandits INIT START

[anyone,"merchant_quest_requested", [
  (eq,"$random_merchant_quest_no","qst_blank_quest_17"),
  (quest_get_slot, ":quest_target_troop", "qst_blank_quest_17", slot_quest_target_troop),
  (quest_get_slot, reg22, "qst_blank_quest_17", slot_quest_target_amount),
  (str_store_troop_name_plural, s6, ":quest_target_troop"),
  (try_begin),
    (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
    (str_store_string, s5, "@Thank you for offering to help, {playername}.^^\
The caravans going to and fro the city have been attacked multiple times by {s6}. They are getting bolder with every ambush, and are moving closer and closer to the city."),
  (else_try),
    (str_store_string, s5, "@Good of you to ask, {playername}.^^\
There are {s6} moving about the area, thinking that they are in charge. No one is doing anything so they are getting bolder and are taking what is rightfully ours."),
  (try_end),], 
"{s5}", "merchant_quest_brief",[]],

[anyone,"merchant_quest_brief", [
  (eq,"$random_merchant_quest_no","qst_blank_quest_17"),
  (quest_get_slot, ":quest_target_troop", "qst_blank_quest_17", slot_quest_target_troop),
  (quest_get_slot, reg22, "qst_blank_quest_17", slot_quest_target_amount),
  (str_store_troop_name_plural, s6, ":quest_target_troop"),
  (try_begin),
    (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
    (str_store_string, s5, "@The people have asked for help in slaying at least {reg22} {s6}, in hopes that this will keep them away for some time.\
^^Would you be able to do this?"),
  (else_try),
    (str_store_string, s5, "@I want you to slay at least {reg22} {s6}, to show those weaklings that they are inconsequential.\
^^What do you say?"),
  (try_end),],
 "{s5}", "mayor_mission_told_kill_quest_bandit",[]],

[anyone|plyr,"mayor_mission_told_kill_quest_bandit", [
(eq,"$random_merchant_quest_no","qst_blank_quest_17"),
(str_store_string, s7, "@We will get rid of these pests."),],
"{s7}", "merchant_quest_taken",[
      (quest_get_slot, ":quest_target_troop", "qst_blank_quest_17", slot_quest_target_troop),
      (quest_get_slot, reg22, "qst_blank_quest_17", slot_quest_target_amount),
      (str_store_troop_name_plural, s6, ":quest_target_troop"),
      (str_store_troop_name_link, s9, "$g_talk_troop"),
      
      (str_store_troop_name_plural, s36, ":quest_target_troop"),
      (setup_quest_text,"qst_blank_quest_17"),
      (str_store_string, s2, "@{s9} wants you to slay {reg22} {s6} in battles."),
      (call_script, "script_start_quest", "qst_blank_quest_17", "$g_talk_troop"),
      (quest_get_slot, ":target_template", "qst_blank_quest_17", slot_quest_target_party_template),
      (store_random_in_range, ":rand", 3, 7),
      (try_for_range, ":unused", 1, ":rand"),
        (store_random_in_range, ":rand_dist", 5, 20),
        (set_spawn_radius, ":rand_dist"),
        (spawn_around_party, "$g_encountered_party", ":target_template"),
        (assign, ":spawned", reg0),
        (party_add_members, ":spawned", ":quest_target_troop", ":rand"),
		(party_set_faction, ":spawned", "fac_deserters"), #Kham: so they don't get into fights
      (try_end),

]],

[anyone|plyr,"mayor_mission_told_kill_quest_bandit", [
(eq,"$random_merchant_quest_no","qst_blank_quest_17"),
],
"I cannot do this now.", "merchant_quest_stall",[]],

# Kill Quest Bandits END


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
   [(set_spawn_radius,4),
    (quest_get_slot, ":quest_giver_center", "qst_troublesome_bandits", slot_quest_giver_center),
    (spawn_around_party,":quest_giver_center","pt_troublesome_bandits"),
	(assign, ":bandit_party", reg0),
	(store_character_level, ":player_level", "trp_player"),
	(try_for_range, ":unused", 0, ":player_level"),
		(party_upgrade_with_xp, ":bandit_party", 100, 0),
	(try_end),
	(try_begin),
		(store_random_in_range, ":troll_chance", 0, 100),
		(ge, ":player_level", 12),
		(val_mul, ":player_level", 2),
		(ge, ":player_level", ":troll_chance"),
		(party_force_add_members, ":bandit_party", "trp_wild_troll", 1),
	(try_end),
    (quest_set_slot, "qst_troublesome_bandits", slot_quest_target_party, ":bandit_party"),
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
"Do I indeed! There's a group of bandits harassing the place, and I'm at the end of my rope as to how to deal with them.\
 They've been ambushing and robbing drunken recruits under the cover of night,\
 and then fading away quick as lightning when the guards finally show up. We've not been able to catch a one of them.\
 They only attack lone people, never daring to show themselves when there's a group about.\
 I need someone who can take on these bandits alone and win. That seems to be the only way of getting rid of them.\
 Are you up to the task?", "merchant_quest_deal_with_night_bandits",[]],

[anyone,"merchant_quest_brief",[(eq,"$random_merchant_quest_no","qst_deal_with_night_bandits")],
"There's a group of bandits harassing the place, and I'm at the end of my rope as to how to deal with them.\
 They've been ambushing and robbing drunken recruits under the cover of night,\
 and then fading away quick as lightning when the guards finally show up. We've not been able to catch a one of them.\
 They only attack lone people, never daring to show themselves when there's a group about.\
 I need someone who can take on these bandits alone and win. That seems to be the only way of getting rid of them.\
 Are you up to the task?", "merchant_quest_deal_with_night_bandits",[]],

[anyone|plyr,"merchant_quest_deal_with_night_bandits", [],
"Killing rogue bandits? Why, certainly!", "deal_with_night_bandits_quest_taken",[
     (str_store_party_name_link, s14, "$g_encountered_party"),
     (str_store_troop_name, s9, "$g_talk_troop"),
     (setup_quest_text, "qst_deal_with_night_bandits"),
     (str_store_string, s2, "@The {s9} of {s14} has asked you to deal with a group of bandits making trouble in {s14}. They only come out at night, and only attack lone people on the streets."),
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

[anyone,"merchant_quest_requested", [], "Nothing right now, Commander. There’ll be more to do soon enough! Keep your blades sharp and wet.", "mayor_pretalk",[]],


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
[anyone,"prisoner_chat_00", [(store_conversation_troop,reg1),(troop_get_type, ":troll", reg1),(eq, ":troll", tf_troll), (agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_continue")], "^^GROWL!^^", "close_window",[]],

[anyone,"prisoner_chat_00", [], "You put me in chains already, what more do you want?", "prisoner_chat_3",[]],
[anyone|plyr,"prisoner_chat_3", [],"Don't try anything, you scum!", "prisoner_chat_4",[]],
[anyone|plyr,"prisoner_chat_3", [
  (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),(neg|troop_is_hero,"$g_talk_troop"), (neg|is_between, "$g_talk_troop", heroes_begin, heroes_end),
  (str_clear, s20),(try_begin),(neq, "$talk_context", tc_troop_review_talk ),(str_store_string, s20, "@_Guards, slaughter him!"), (try_end),
], 
"You happen to be our next dinner!{s20}", "prisoner_slaughter",[]],
[anyone,"prisoner_chat_4", [],"Yeah, like I'm in a position for trying? Get lost!", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"prisoner_slaughter", [(eq, "$talk_context", tc_troop_review_talk), (neg|is_between, "$g_talk_troop", heroes_begin, heroes_end), ], "One day you will pay!", "prisoner_slaughter_02",[
  (try_begin),
    (lt, "$butcher_trait_kills",35),
    (val_add, "$butcher_trait_kills",1),
  (else_try),
    (ge, "$butcher_trait_kills", 35),
    (call_script, "script_cf_gain_trait_butcher"),
  (try_end),]],

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
    #(agent_set_hit_points,":agent",0,0),
    
    #(agent_deliver_damage_to_agent, reg1, ":agent"),
  (try_end),
  (party_remove_prisoners, "p_main_party", "$g_talk_troop", 1),
  (try_begin),
    (lt, "$butcher_trait_kills",35),
    (val_add, "$butcher_trait_kills",1),
  (else_try),
    (ge, "$butcher_trait_kills", 35),
    (call_script, "script_cf_gain_trait_butcher"),
  (try_end),
  (try_begin),
    (troop_slot_eq, "trp_traits",  slot_trait_butcher,1),
    (troop_add_item,"trp_player", "itm_human_meat",imod_fresh),
    (troop_add_item,"trp_player", "itm_human_meat",imod_fresh),
  (else_try),
    (troop_add_item,"trp_player", "itm_human_meat",imod_fresh),
  (try_end)]],

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

# TLD Kham - Player Upgrade Troll

[anyone|plyr,"town_merchant_talk", 
  [
   (is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),
   (this_or_next|neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_troll_troop, -1),
   (eq, "$g_talk_troop_faction", "fac_gundabad"),

   (try_begin),
    (eq, "$g_encountered_party", "p_town_dol_guldur"),
    (assign, "$g_talk_troop_faction", "fac_guldur"),
   (try_end),

   (party_get_num_companion_stacks,":stacks","p_main_party"),
   (assign, ":num_trolls", 0),
   (try_for_range,":stack",0,":stacks"),
    (party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack"),
    (is_between, ":troop_id", "trp_moria_troll", "trp_multiplayer_profile_troop_male"), #Troll Range
    (party_stack_get_size, ":num_trolls", "p_main_party", ":stack"),
   (try_end),
   (gt, ":num_trolls", 0),

  ], 
  "I want to strengthen my trolls!", "player_upgrade_trolls_take", []],


[anyone,"player_upgrade_trolls_take", 
  [
   (neq, "$g_talk_troop_faction", "fac_gundabad"),
   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_troll_troop, -1),
   (party_get_free_companions_capacity,reg10,"p_main_party"), (gt,reg10,0),
   (call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (assign, ":rank", reg0), #rank points to rank number 0-9
   (call_script, "script_get_rank_title_to_s24", "$g_talk_troop_faction"), 
   (str_store_string_reg, s25, s24), #to s25 (current rank)
   (call_script, "script_get_any_rank_title_to_s24", "$g_talk_troop_faction", 6), #to s24
   (le, ":rank", 5),

  ], 
  "Who are you to ask this of me? Pah! Begone! (You need to be {s24} or higher)", "close_window", [(call_script, "script_stand_back")]],


[anyone,"player_upgrade_trolls_take", 
  [

   (neq, "$g_talk_troop_faction", "fac_gundabad"),
   (faction_get_slot, ":fac_troll",  "$g_talk_troop_faction", slot_faction_troll_troop),
   (troop_get_upgrade_troop, ":fac_troll_up", ":fac_troll", 0),
   (troop_get_slot, ":armoured", ":fac_troll_up", slot_troop_troll_armoured_variant),
   (gt, ":armoured", 0), 
   (party_get_num_companion_stacks,":stacks","p_main_party"),
   (assign, ":num_trolls", 0),
   (try_for_range,":stack",0,":stacks"),
    (party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack"),
    (eq, ":troop_id", ":fac_troll_up"), #They have unarmoured ones?
    (val_add, ":num_trolls", 1),
   (try_end),
   (gt, ":num_trolls", 0),
   (store_character_level, ":price", ":armoured"),
   (val_mul, ":price", 300), 
   (assign, reg21, ":price"),

  ], 
  "You’ve done us many a good turn. We’ll help put some iron on your boy here! ({reg21} resource points)", "player_upgrade_trolls_ask", []],

[anyone,"player_upgrade_trolls_take", 
  [
   (neq, "$g_talk_troop_faction", "fac_gundabad"),
   (faction_get_slot, ":fac_troll",  "$g_talk_troop_faction", slot_faction_troll_troop),
   (party_get_num_companion_stacks,":stacks","p_main_party"),
   (assign, ":num_trolls", 0),
   (try_for_range,":stack",0,":stacks"),
    (party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack"),
    (eq, ":troop_id", ":fac_troll"),
    (party_stack_get_size, ":num_trolls", "p_main_party", ":stack"),
   (try_end),
   (gt, ":num_trolls", 0),

  ], 
  "Your trolls are like mewling babes. Get them blooded good and proper first!", "close_window", [(call_script, "script_stand_back")]],

[anyone,"player_upgrade_trolls_take", 
  [


   (eq, "$g_talk_troop_faction", "fac_gundabad"),

  ], 
  "We don't do that here...", "close_window", [(call_script, "script_stand_back")]],

[anyone,"player_upgrade_trolls_take", 
  [

   (neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_troll_troop, -1),
   (faction_get_slot, ":fac_troll",  "$g_talk_troop_faction", slot_faction_troll_troop),
   (troop_get_upgrade_troop, ":fac_troll_up", ":fac_troll", 0),
   (party_get_num_companion_stacks,":stacks","p_main_party"),
   (assign, ":num_trolls", 0),
   (try_for_range,":stack",0,":stacks"),
    (party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack"),
    (is_between, ":troop_id", "trp_moria_troll", "trp_multiplayer_profile_troop_male"), #Troll Range
    (neq, ":troop_id", ":fac_troll_up"), #if none of them are from smith's faction
    (party_stack_get_size, ":num_trolls", "p_main_party", ":stack"),
   (try_end),
   (gt, ":num_trolls", 0), #if none of them are from smith's faction

  ], 
  "Your trolls don’t even talk proper! They’re not our kind. Take them back to where they came from!", "close_window", [(call_script, "script_stand_back")]],


[anyone|plyr,"player_upgrade_trolls_take", 
  [], 
  "Forget it", "player_upgrade_troll_not_enough", []],


[anyone|plyr,"player_upgrade_trolls_ask", 
  [ 
    (call_script,"script_update_respoint"),
    (faction_get_slot,  ":rp", "$g_talk_troop_faction", slot_faction_respoint),
    (ge, ":rp", reg21), #reg21 is rps cost
  ], 
  "I'll armour one of them.", "player_upgrade_troll_buy_done", []],

[anyone|plyr,"player_upgrade_trolls_ask", 
  [ (call_script,"script_update_respoint"),
    (faction_get_slot,  ":rp", "$g_talk_troop_faction", slot_faction_respoint),
    (lt, ":rp", reg21), #reg21 is rps cost
  ], 
  "Perhaps I haven’t earned this yet. I’ll not trouble you with this trifle", "player_upgrade_troll_not_enough", []],

[anyone|plyr,"player_upgrade_trolls_ask", 
  [], 
  "Forget it", "player_upgrade_troll_not_enough", []],

[anyone,"player_upgrade_troll_not_enough", 
  [], 
  "Wasting my time...", "close_window", [(call_script, "script_stand_back")]],

[anyone,"player_upgrade_troll_buy_done", 
  [], 
  "Yes… yes! Come here, you big lunk, you...", "close_window", 
  [
   (faction_slot_ge, "$g_talk_troop_faction", slot_faction_troll_troop, 0),
   (faction_get_slot, ":fac_troll",  "$g_talk_troop_faction", slot_faction_troll_troop),
   (troop_get_upgrade_troop, ":fac_troll_up", ":fac_troll", 0),
   (troop_get_slot, ":armoured", ":fac_troll_up", slot_troop_troll_armoured_variant),
   (gt, ":armoured", 0), 
   (party_get_num_companion_stacks,":stacks","p_main_party"),
   (assign, ":num_trolls", 0),
   (try_for_range,":stack",0,":stacks"),
    (party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack"),
    (eq, ":troop_id", ":fac_troll_up"), #They have unarmoured ones?
    (val_add, ":num_trolls", 1),
   (try_end),
   (gt, ":num_trolls", 0),
   (store_character_level, ":price", ":armoured"),
   (val_mul, ":price", -300), 
   (party_remove_members, "p_main_party", ":fac_troll_up", 1),
   (party_add_members, "p_main_party", ":armoured", 1),
   (call_script, "script_add_faction_rps", "$g_talk_troop_faction", ":price"),
   (call_script, "script_stand_back")
  ]],

# TLD Kham - Player Upgrade Troll END


[anyone,"trade_requested_weapons", [], "Ah, yes commander. These wares are the best you'll find anywhere.", "merchant_trade",[#(assign, "$equip_needs_checking", 1),
  (change_screen_trade)]],
[anyone,"trade_requested_horse", [], "Fierce mounts for the riding and killing, and meat to feed them with! You won't find better beasts than these anywhere else.", "merchant_trade",[#(assign, "$equip_needs_checking", 1),
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
#         (is_between,"$g_talk_troop",walkers_begin, walkers_end),
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
                                      # (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                                      # (str_store_string, s10, "@{s6} This place and the surrounding lands belong to you of course, my {lord/lady}."),
                                    # (else_try),
                                      (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
                                      (ge, ":town_lord", 0),
                                      (str_store_troop_name, s7, ":town_lord"),
                                      (store_troop_faction, ":town_lord_faction", ":town_lord"),
                                      (str_store_faction_name, s8, ":town_lord_faction"),
                                      (str_store_string, s10, "@{s6} This place and the surrounding lands belong to {s7} of {s8}."),
                                    (try_end),
                                    # (str_clear, s5),
                                    # (assign, reg20, 0),
                                    # (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
                                      # (store_sub, ":cur_good_slot", ":cur_good", trade_goods_begin),
                                      # (val_add, ":cur_good_slot", slot_town_trade_good_productions_begin),
                                      # (party_get_slot, ":production", "$g_encountered_party", ":cur_good_slot"),
                                      # (ge, ":production", 10),
                                      # (str_store_item_name, s3, ":cur_good"),
                                      # (try_begin),
                                        # (eq, reg20, 0),
                                        # (str_store_string, s5, s3),
                                      # (else_try),
                                        # (eq, reg20, 1),
                                        # (str_store_string, s5, "@{s3} and {s5}"),
                                      # (else_try),
                                        # (str_store_string, s5, "@{s3}, {s5}"),
                                      # (try_end),
                                      # (val_add, reg20, 1),
                                    # (try_end),
                                    # (str_store_string, s11, "@{reg20?We mostly produce {s5} here:We don't produce much here these days}.\
 # If you would like to learn more, you can speak with our {reg4?guildmaster:village elder}. He is nearby, right over there."),
 ],
"{s10}", "town_dweller_talk",[]], #was "{s10} {s11}"

[anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_village),
                                     (eq, "$welfare_inquired", 0)], #Just keep this to keep the Global Variable in use.
"How is life here?", "town_dweller_talk",[(assign, "$welfare_inquired", 1)]],
  #[anyone|plyr,"town_dweller_talk", [(party_slot_eq, "$current_town", slot_party_type, spt_town),
                                     # (eq, "$welfare_inquired", 0)], "How is life here?", "town_dweller_ask_situation",[(assign, "$welfare_inquired", 1)]],


# [anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         # (assign, ":walker_type", reg0),
                                         # (eq, ":walker_type", walkert_needs_money),
                                         # (party_slot_eq, "$current_town", slot_party_type, spt_village)],
# "Disaster has struck my family, {sir/madam}. A pestilence has ruined the crops on our fields, and my poor children lie at home hungry and sick.\
 # My neighbours are too poor themselves to help me.", "town_dweller_poor",[]],

# [anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         # (assign, ":walker_type", reg0),
                                         # (eq, ":walker_type", walkert_needs_money)],
# "My life is miserable, {sir/madam}. I haven't been able to find a job for months, and my poor children go to bed hungry each night.\
 # My neighbours are too poor themselves to help me.", "town_dweller_poor",[]],

# [anyone|plyr,"town_dweller_poor", [(store_troop_gold, ":gold", "trp_player"),
                                     # (ge, ":gold", 300),
                                     # ],
# "Then take these 300 denars. I hope this will help you and your family.", "town_dweller_poor_paid", [(troop_remove_gold, "trp_player", 300)]],

# [anyone|plyr,"town_dweller_poor", [], "Then you must work harder and bear your burden without complaining.", "town_dweller_poor_not_paid",[]],
# [anyone,"town_dweller_poor_not_paid", [], "Yes {sir/madam}. I will do as you say.", "close_window",[(call_script,"script_stand_back"),]],

# [anyone,"town_dweller_poor_paid", [], "{My lord/My good lady}. \
 # You are so good and generous. I will tell everyone how you helped us.", "close_window",
   # [(call_script,"script_stand_back"),
    # (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 1),
    # (call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
    # (assign, ":walker_no", reg2),
    # (call_script, "script_center_set_walker_to_type", "$g_encountered_party", ":walker_no", walkert_needs_money_helped)]],

# [anyone,"town_dweller_ask_situation", [(call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
                                         # (assign, ":walker_type", reg0),
                                         # (eq, ":walker_type", walkert_needs_money_helped)],
# "Thank you for your kindness {sir/madam}. With your help our lives will be better. I will pray for you everyday.", "close_window",[(call_script,"script_stand_back"),]],

# [anyone,"town_dweller_ask_situation", [(neg|party_slot_ge, "$current_town", slot_town_prosperity, 30)],
# "Times are hard, {sir/madam}. We work hard all day and yet we go to sleep hungry most nights.", "town_dweller_talk",[]],
  
# [anyone,"town_dweller_ask_situation", [(neg|party_slot_ge, "$current_town", slot_town_prosperity, 70)],
# "Times are hard, {sir/madam}. But we must count our blessings.", "town_dweller_talk",[]],
# [anyone,"town_dweller_ask_situation", [],
# "We are not doing too badly {sir/madam}. We must count our blessings.", "town_dweller_talk",[]],

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
[anyone,"member_chat_00", [(troop_get_type, ":troll", "$g_talk_troop"),(eq, ":troll", tf_troll),(store_conversation_agent, ":troll_agent"), (agent_set_animation, ":troll_agent", "anim_troll_or_ent_bend_continue")], "^^GROWL!^^", "close_window",[]],

[anyone,"member_chat_00", [(eq, "$g_talk_troop", "trp_werewolf")], "^^Grrrrr.....^^", "close_window",[]],

[anyone,"member_chat_00", [(troop_slot_eq,  "$g_talk_troop", slot_troop_upkeep_not_paid,0)], # or else, incipit is different
"Your orders, Commander?", "regular_member_talk",[]],

[anyone|plyr,"regular_member_talk", [], "Tell me about yourself", "view_regular_char_requested",[]],
[anyone,"view_regular_char_requested", [], "Yes, Commander. Let me tell you all there is to know about me.", "do_regular_member_view_char",[[change_screen_view_character]]],
[anyone,"do_regular_member_view_char", [], "Anything else?", "regular_member_talk",[]],

# TLD: can disband members for Res Point (mtarini)
  
[anyone,"member_chat_00", [
      (neg|troop_slot_eq, "$g_talk_troop", slot_troop_upkeep_not_paid,0), # if the troop wasn't paid last time, and it is on the leave
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
      (call_script, "script_safe_remove_party", "$g_encountered_party"),
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
      (agent_set_animation, "$g_talk_agent", "anim_troll_or_ent_bend_continue"),
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
      (call_script, "script_safe_remove_party", "$g_encountered_party"),
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
  [(neq, "$g_encountered_party_type", spt_kingdom_caravan),
   (neq, "$g_encountered_party_type", spt_prisoner_train),
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

#party that follows you
[anyone,"start", [(eq,"$talk_context",tc_party_encounter),
                    (eq,"$encountered_party_hostile",0),
                    (is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end),
                    (party_slot_eq, "$g_encountered_party", slot_party_following_player, 1),],    
"We are following your orders, {s24}.", "party_encounter_friend",
     [(call_script, "script_get_rank_title_to_s24", "$g_encountered_party_faction" )]],
     
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
        (neq, "$g_encountered_party_type", spt_kingdom_caravan),
        (neq, "$g_encountered_party_type", spt_prisoner_train),
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

#Kham - Regular Parties follow Player


[anyone|plyr,"party_encounter_friend", [
        (neg|party_slot_eq, "$g_encountered_party", slot_party_following_player, 1), #Don't show if already following player
        (call_script, "script_get_faction_rank", "$g_talk_troop_faction"), 
        (assign, ":rank", reg0), #rank points to rank number 0-9 
        (assign, ":continue", 0),
        (try_begin),
          (eq, "$g_encountered_party_type", spt_scout),
          (ge, ":rank", 3),
          (try_begin),
            (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
            (assign, "$tld_action_cost", 3),
          (else_try),
            (assign, "$tld_action_cost", 5),
          (try_end),
          (assign, ":continue", 1),
        (else_try),
          (eq, "$g_encountered_party_type", spt_raider),
          (ge, ":rank", 5),
          (try_begin),
            (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
            (assign, "$tld_action_cost", 7),
          (else_try),
            (assign, "$tld_action_cost", 10),
          (try_end),
          (assign, ":continue", 1),
        (else_try),
          (eq, "$g_encountered_party_type", spt_patrol),
          (ge, ":rank", 7),
          (try_begin),
            (troop_slot_eq, "trp_traits", slot_trait_command_voice, 1),
            (assign, "$tld_action_cost", 11),
          (else_try),
            (assign, "$tld_action_cost", 15),
          (try_end),
          (assign, ":continue", 1),
        (try_end),
        (eq, ":continue", 1),
        (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
        (assign, reg1, "$tld_action_cost"),
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@I will need your help, please follow me. [Costs {reg1}/{reg2} influence]"),
        (else_try),
          (str_store_string, s4, "@You and your men must follow me. [Costs {reg1}/{reg2} influence]"),
        (try_end)],
"{s4}", "party_follow_player_pass", []],

[anyone,"party_follow_player_pass", [
        (call_script, "script_check_num_following_player"),
        (eq, reg65, 0),
        (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
        (ge, reg2, "$tld_action_cost"),
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@It looks like you have too many followers already."),
        (else_try),
          (str_store_string, s4, "@Why do you need us? You have all you need following you already!"),
        (try_end)],
"{s4}", "close_window", [(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)]],

[anyone,"party_follow_player_pass", [
        (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
        (assign, reg1, "$tld_action_cost"),
        (ge, reg2, "$tld_action_cost"),
        (call_script, "script_check_num_following_player"),
        (eq, reg65, 1),
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@We will follow you, though we cannot wander too far."),
        (else_try),
          (str_store_string, s4, "@If there is killing, we will follow. But we cannot go too far, or we will get in trouble."),
        (try_end)],
"{s4}", "party_follow_player_continue", []],

[anyone,"party_follow_player_pass", [
        (call_script, "script_check_num_following_player"),
        (eq, reg65, 1),
        (faction_get_slot, reg2, "$g_talk_troop_faction", slot_faction_influence),
        (assign, reg1, "$tld_action_cost"),
        (lt, reg2, "$tld_action_cost"),
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@We cannot leave our post to follow you for now. [Not enough influence points (Requires {reg1})]"),
        (else_try),
          (str_store_string, s4, "@Who are you to command us? [Not enough influence points (Requires {reg1})]"),
        (try_end)],
"{s4}", "party_encounter_friend", []],


[anyone|plyr,"party_follow_player_continue", [
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@Then let us go. Stay close. I will need you soon."),
        (else_try),
          (str_store_string, s4, "@There will be blood, that is for sure. Stay close, or miss out."),
        (try_end)],
"{s4}", "close_window", [
  (call_script,"script_stand_back"),(assign, "$g_leave_encounter",1),
  (call_script, "script_party_follow_player", "$g_encountered_party"),
  (val_add, "$trait_check_commands_issued", 1),
]],


[anyone|plyr,"party_encounter_friend", [
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@Goodbye, friends."),
        (else_try),
          (str_store_string, s4, "@See you later if you don't get killed."),
        (try_end)],
"{s4}", "close_window", [(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)]],

[anyone|plyr,"party_encounter_friend", [
        (party_slot_eq, "$g_encountered_party", slot_party_following_player, 1),
        
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@I don't need your help any longer. Go home."),
        (else_try),
          (str_store_string, s4, "@I don't have any need for you. Get lost."),
        (try_end)],
"{s4}", "party_follow_player_dismiss", [
        (assign, ":followers", "$g_encountered_party"),
        (party_set_slot, "$g_encountered_party", slot_party_following_player, 0),
        (party_set_slot, "$g_encountered_party", slot_party_commander_party, -1),
        (party_get_slot, ":home_center", ":followers", slot_party_home_center),
        (try_begin),
          (ge, ":home_center", 1),
          (party_get_position, pos1, ":home_center"),
          (party_set_slot, ":followers", slot_party_ai_object, ":home_center"),
        (else_try),
          (faction_get_slot, ":faction_capital", "$g_talk_troop_faction", slot_faction_capital), 
          (party_get_position, pos1, ":faction_capital"),
          (party_set_slot, ":followers", slot_party_ai_object, ":faction_capital"),
        (try_end),
        (party_set_slot, ":followers", slot_party_ai_state, spai_undefined),
        (party_set_ai_behavior, ":followers", ai_bhvr_patrol_location),
        (party_set_ai_target_position, ":followers", pos1),
        (party_set_ai_patrol_radius, ":followers", 10),
        (str_store_party_name, s5, ":followers"),
        (display_message, "@{s5} has stopped following you."),
        
        (assign, ":scouts", 0),
        (assign, ":raider", 0),
        (assign, ":war_party", 0),
          
        #Count remaining followers
        (try_for_parties, ":followers"),
          (party_slot_eq, ":followers", slot_party_following_player, 1),
          (party_is_active, ":followers"),
          
          
          (party_get_slot, ":type", ":followers", slot_party_type),
          (try_begin),
            (eq, ":type", spt_scout),
            (val_add, ":scouts", 1),
          (else_try),
            (eq, ":type", spt_raider),
            (val_add, ":raider", 1),
          (else_try),
            (eq, ":type", spt_patrol),
            (val_add, ":war_party", 1),
          (try_end),
        (try_end),
        
        (store_add, ":cur_followers", ":scouts", ":raider"),
        (val_add, ":cur_followers", ":war_party"),
        
        #Debug
        #(assign, reg66, ":scouts"),
        #(assign, reg67, ":raider"),
        #(assign, reg68, ":war_party"),
        (assign, reg69, ":cur_followers"),
        
        (try_begin),
          (eq, ":cur_followers", 1),
          (display_message, "@You have {reg69} ally party following you", message_neutral),
        (else_try),
          (gt, ":cur_followers", 1),
          (display_message, "@You have {reg69} ally parties following you", message_neutral),
        (try_end),
        
        #(display_message, "@Total: {reg69} - Scouts:{reg66} - Raiders: {reg67} - Patrols: {reg68}", color_good_news),
        
        (party_set_slot, "p_main_party", slot_party_number_following_player, ":cur_followers"),
       
]],

[anyone,"party_follow_player_dismiss", [
        (try_begin),
          (faction_slot_eq, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
          (str_store_string, s4, "@We will return to our previous task. Goodbye."),
        (else_try),
          (str_store_string, s4, "@Lads, we're going home!"),
        (try_end)],
"{s4}", "close_window", [(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)]],

[anyone,"party_reinforce", [
     #War not started
     (eq,"$tld_war_began",0),],
"We haven't seen much enemy activity yet. Maybe later, thanks.", "party_reinforce_end", []],
[anyone,"party_reinforce", [
     #prevent some exploitation by placing caps on party size #InVain: Reduce limits slightly
     (assign, ":party_limit", 100), #was 80, affects hosts
     (try_begin),(eq, "$g_encountered_party_type", spt_scout          ),(assign, ":party_limit", 10), #was 20
      (else_try),(eq, "$g_encountered_party_type", spt_raider         ),(assign, ":party_limit", 30), #was 50
      (else_try),(eq, "$g_encountered_party_type", spt_patrol         ),(assign, ":party_limit", 50), #was 80
      (else_try),(eq, "$g_encountered_party_type", spt_kingdom_caravan),(assign, ":party_limit", 50), #was 100
      (else_try),(eq, "$g_encountered_party_type", spt_prisoner_train ),(assign, ":party_limit", 50), #was 80
     (try_end),
	 (store_faction_of_party, ":faction", "$g_encountered_party"), #scale by faction type
	 (try_begin), #orc factions 200%
		  (this_or_next|eq, ":faction", "fac_mordor"),
          (this_or_next|eq, ":faction", "fac_isengard"),
          (this_or_next|eq, ":faction", "fac_moria"),
          (this_or_next|eq, ":faction", "fac_guldur"),
          (eq, ":faction", "fac_gundabad"),	(val_mul, ":party_limit", 2),
	  (else_try), #other evil factions 150%
		  (faction_get_slot, ":faction_side", ":faction", slot_faction_side),
		  (this_or_next|eq, ":faction_side", faction_side_eye),
          (eq, ":faction_side", faction_side_hand),	(val_mul, ":party_limit", 3), (val_div, ":party_limit", 2),
	  (else_try), #elf factions: 70%
		  (is_between, ":faction", fac_lorien, fac_dale), (val_mul, ":party_limit", 7), (val_div, ":party_limit", 10),
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
    
    ] +

#swy-- workaround a bug where the player would get stuck in the conversation menu with the barracks guy after donating some troops to his camp.
#   -- because the player insists on upgrading his troops inside the give_members screen, the before/after count doesn't match and none of the following dialog options kick. Boom, stuck.
#   -- what i've made is to make impossible for the player to upgrade his troops in here by returning a crazy amount of points/money in "script_game_get_upgrade_cost", so the button stays disabled.
#   -- more info: http://mbx.streetofeyes.com/index.php/topic,3465.msg68239.html#msg68239

  (is_a_wb_dialog
   and
  [
   (assign, "$tld_forbid_troop_upgrade_mode", 1),
   (change_screen_give_members),
   #(assign,"$tld_forbid_troop_upgrade_mode",0)
  ]
   or
  [
   (change_screen_give_members)
  ])
  
# disabled in the next dialog -> party_reinforce_check (already loaded when the give_members is accessed) -> party_reinforce_check_1 (3 branches) -> party_reinforce_end
  
],

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
"{s4}", "close_window", [(call_script,"script_stand_back"),(assign, "$g_leave_encounter",1)] + (is_a_wb_dialog and [(assign,"$tld_forbid_troop_upgrade_mode",0)] or []) ],


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

] + (is_a_wb_dialog and [
#### Kham Ori's Last Stand Dialogues ##########

[anyone, "start", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 1),],
  "You there! You survived? Good! You can't be waving a stick about! Take this!", "close_window", 
  [ (get_player_agent_no, ":player"),
    (agent_unequip_item, ":player", "itm_wood_club"),
    (agent_equip_item, ":player", "itm_dwarf_sword_a"),
    (agent_set_wielded_item, ":player", "itm_dwarf_sword_a"),
    (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 20),]],

[anyone, "start", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 2),],
  "You fight well, kinsman! I don't know how you've been surviving so far. I remember you joining us recently, before all this... before Balin fell... Where are you from?", "ori_choose_1", 
  []],

[anyone|plyr, "ori_choose_1", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 2),],
  "I was a tracker, sent to the woods near the Bear people. I recently heard about Balin's company and joined.", "ori_choose_finish", 
  [ (get_player_agent_no, ":player"),
    (agent_equip_item, ":player", "itm_dwarf_horn_bow"),
    (agent_equip_item, ":player", "itm_arrows"),
    (agent_equip_item, ":player", "itm_arrows"),
    (agent_set_wielded_item, ":player", "itm_dwarf_horn_bow"),
    (troop_set_slot, "$g_player_troop", slot_troop_morality_state, 1), #1 for Bow. Remember this for future dialogues
    (troop_raise_proficiency_linear, "$g_player_troop", wpt_archery, 35),
    (troop_raise_skill, "$g_player_troop", skl_power_draw, 1),
    (troop_raise_skill, "$g_player_troop", skl_athletics, 2), ]],

[anyone|plyr, "ori_choose_1", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 2),],
  "I am a distant cousin, a veteran bodyguard from a mine far away. Then I heard of Balin and joined.", "ori_choose_finish", 
  [ (get_player_agent_no, ":player"),
    (agent_equip_item, ":player", "itm_dwarf_shield_b"),
    (agent_set_wielded_item, ":player", "itm_dwarf_shield_b"),
    (troop_set_slot, "$g_player_troop", slot_troop_morality_state, 2), #2 for 1h. Remember this for future dialogues
    (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 35),
    (troop_raise_skill, "$g_player_troop", skl_power_strike, 1),
    (troop_raise_skill, "$g_player_troop", skl_ironflesh, 1),
    (troop_raise_skill, "$g_player_troop", skl_shield, 2),]],

[anyone|plyr, "ori_choose_1", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 2),],
  "I am from the Iron Hills, a veteran of the wars, and a miner during peace. I heard of Balin and joined, wanting more kill orcs.", "ori_choose_finish", 
  [ (get_player_agent_no, ":player"),
    (agent_equip_item, ":player", "itm_dwarf_great_mattock"),
    (agent_equip_item, ":player", "itm_dwarf_throwing_axe"),
    (agent_equip_item, ":player", "itm_dwarf_throwing_axe"),
    (agent_set_wielded_item, ":player", "itm_dwarf_great_mattock"),
    (troop_set_slot, "$g_player_troop", slot_troop_morality_state, 3), #3 for 2h. Remember this for future dialogues
    (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 35),
    (troop_raise_proficiency_linear, "$g_player_troop", wpt_throwing, 40),
    (troop_raise_skill, "$g_player_troop", skl_power_strike, 2),
    (troop_raise_skill, "$g_player_troop", skl_power_throw, 1),
    (troop_raise_skill, "$g_player_troop", skl_athletics, 1),]],

[anyone, "ori_choose_finish", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 2),],
  "Good to know! I found these, fit for your background. We shall make our stand here and take as many of them with us!", "close_window", 
  [(assign, "$temp", 0), (display_message, "@You ready your weapons, feeling the rush of past experience through your body. (Weapon Profeciencies and Abilities improved)", color_neutral_news)]],

[anyone, "start", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 3),],
  "It looks like you are shaking off those rusty skills, eh? Here, take a swig of this. It will make you feel better. More orcs are coming!", "close_window", 
  [ (troop_get_slot, ":weapon_selection", "$g_player_troop", slot_troop_morality_state),
    (get_player_agent_no, ":player"),
    (try_begin),
      (eq, ":weapon_selection", 1),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_archery, 20),
      (troop_raise_skill, "$g_player_troop", skl_power_draw, 1),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 1),
      (agent_refill_ammo, ":player"),
    (else_try),
      (eq, ":weapon_selection", 2),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 20),
      (troop_raise_skill, "$g_player_troop", skl_shield, 1),
      (troop_raise_skill, "$g_player_troop", skl_ironflesh, 1),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 1),
      (agent_refill_wielded_shield_hit_points, ":player"),
    (else_try),
      (eq, ":weapon_selection", 3),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 20),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 20),
      (troop_raise_skill, "$g_player_troop", skl_power_throw, 1),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 1),
      (troop_raise_skill, "$g_player_troop", skl_athletics, 1),
    (try_end),
    (agent_set_hit_points, ":player", 100),
    (troop_raise_attribute, "$g_player_troop", ca_strength, 3),
    (troop_raise_attribute, "$g_player_troop", ca_agility, 3),
    (assign, "$temp", 0),
    (display_message, "@The previous battle warmed you up. You feel invigorated, and ready for more. (Attributes, Abilities, and Weapon Profeciencies Improved)", color_neutral_news)]],

[anyone, "start", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 4),],
  "Take that dusty thing off you and wear this. Should protect you better. These orcs bite hard!", "close_window", 
  [(assign, "$temp", 0),
    (get_player_agent_no, ":player"),
    (agent_unequip_item, ":player", "itm_dwarf_vest"),
    (agent_equip_item, ":player", "itm_leather_dwarf_armor_b"),]],

[anyone, "start", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 5),],
  "Something big is coming! Get ready!", "close_window", 
  [(assign, "$temp", 0),
    (get_player_agent_no, ":player"),
    (agent_set_hit_points, ":player", 100),
    (agent_refill_ammo, ":player"),
    (play_sound, "snd_troll_grunt_long"),]],

[anyone, "start", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 6),],
  "There are too many of them... but we are dwarves!", "close_window", 
  [(assign, "$temp", 0),
    (troop_get_slot, ":weapon_selection", "$g_player_troop", slot_troop_morality_state),
    (get_player_agent_no, ":player"),
    (try_begin),
      (eq, ":weapon_selection", 1),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_archery, 20),
      (troop_raise_skill, "$g_player_troop", skl_power_draw, 1),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 1),
      (agent_refill_ammo, ":player"),
    (else_try),
      (eq, ":weapon_selection", 2),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 20),
      (troop_raise_skill, "$g_player_troop", skl_shield, 1),
      (troop_raise_skill, "$g_player_troop", skl_ironflesh, 1),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 1),
    (else_try),
      (eq, ":weapon_selection", 3),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 30),
      (troop_raise_skill, "$g_player_troop", skl_power_throw, 1),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 1),
      (troop_raise_skill, "$g_player_troop", skl_athletics, 1),
    (try_end),
    (troop_raise_attribute, "$g_player_troop", ca_strength, 3),
    (troop_raise_attribute, "$g_player_troop", ca_agility, 3),
    (display_message, "@You are tired, but adrenaline coursing through your veins steel you for more. (Attributes, Abilities, and Weapon Profeciencies Improved)", color_neutral_news),

  ]],

[anyone, "start", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 7),],
  "Those orcs opened up a cavern filled with treasures. Here are some that I found, go ahead and take them.", "close_window", 
  [(assign, "$temp", 0),
    (troop_get_slot, ":weapon_selection", "$g_player_troop", slot_troop_morality_state),
    (get_player_agent_no, ":player"),
    (try_begin),
      (eq, ":weapon_selection", 1),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_archery, 20),
      (troop_raise_skill, "$g_player_troop", skl_power_draw, 2),
      (agent_refill_ammo, ":player"),
      (agent_unequip_item, ":player", "itm_dwarf_horn_bow"),
      (agent_equip_item, ":player", "itm_mirkwood_bow"),
      (agent_unequip_item, ":player", "itm_dwarf_sword_a"),
      (agent_equip_item, ":player", "itm_dwarf_hand_axe"),
      (agent_set_wielded_item, ":player", "itm_mirkwood_bow"),
    (else_try),
      (eq, ":weapon_selection", 2),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 20),
      (troop_raise_skill, "$g_player_troop", skl_ironflesh, 2),
      (agent_unequip_item, ":player", "itm_dwarf_sword_a"),
      (agent_equip_item, ":player", "itm_dwarf_battle_axe"),
      (agent_set_wielded_item, ":player", "itm_dwarf_battle_axe"),
      (agent_refill_wielded_shield_hit_points, ":player"),
    (else_try),
      (eq, ":weapon_selection", 3),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 20),
      (troop_raise_skill, "$g_player_troop", skl_power_throw, 1),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 2),
      (troop_raise_skill, "$g_player_troop", skl_athletics, 1),
      (agent_unequip_item, ":player", "itm_dwarf_great_mattock"),
      (agent_equip_item, ":player", "itm_dwarf_great_axe"),
      (agent_set_wielded_item, ":player", "itm_dwarf_great_axe"),
      (agent_refill_ammo, ":player"),
    (try_end),
    (agent_set_hit_points, ":player", 100),
    (agent_refill_ammo, ":player"),
    (display_message, "@These are great weapons indeed. They feel strange to the touch... (Abilities and Weapon Profeciencies Improved)", color_neutral_news),
  ]],

  [anyone, "start", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 8),],
  "No.... I hear them... they are outside! They are everywhere!", "close_window", 
  [ (play_sound, "snd_troll_grunt_long"),
    (assign, "$temp", 0),
    (troop_get_slot, ":weapon_selection", "$g_player_troop", slot_troop_morality_state),
    (try_begin),
      (eq, ":weapon_selection", 1),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_archery, 20),
      (troop_raise_skill, "$g_player_troop", skl_power_draw, 2),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 2),
    (else_try),
      (eq, ":weapon_selection", 2),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 20),
      (troop_raise_skill, "$g_player_troop", skl_ironflesh, 2),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 2),
    (else_try),
      (eq, ":weapon_selection", 3),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 20),
      (troop_raise_skill, "$g_player_troop", skl_power_throw, 2),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 2),
      (troop_raise_skill, "$g_player_troop", skl_athletics, 2),
    (try_end),
    (display_message, "@You can barely raise your weapon now... but seeing your kinsmen around you strengthen your resolve. (Abilities and Weapon Profeciencies Improved).", color_neutral_news),
  ]],

  [anyone, "start", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(eq, "$enemy_reinforcement_stage", 9),],
    "Here... Our Lord Balin's... you are worthy of these...", "close_window", 
  [ (assign, "$temp", 0),
    (get_player_agent_no, ":player"),
    (agent_unequip_item, ":player", "itm_leather_dwarf_armor_b"),
    (agent_equip_item, ":player", "itm_dwarf_armor_c"),
    (agent_unequip_item, ":player", "itm_dwarf_hood"),
    (agent_equip_item, ":player", "itm_dwarf_helm_p"),

    (troop_get_slot, ":weapon_selection", "$g_player_troop", slot_troop_morality_state),
    (try_begin),
      (eq, ":weapon_selection", 1),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_archery, 50),
      (troop_raise_skill, "$g_player_troop", skl_power_draw, 3),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 3),
      (agent_unequip_item, ":player", "itm_mirkwood_bow"),
      (agent_equip_item, ":player", "itm_lorien_bow_reward"),
      (agent_set_wielded_item, ":player", "itm_lorien_bow_reward"),
      (agent_refill_ammo, ":player"),
    (else_try),
      (eq, ":weapon_selection", 2),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 50),
      (troop_raise_skill, "$g_player_troop", skl_ironflesh, 3),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 3),
      (troop_raise_skill, "$g_player_troop", skl_shield, 5),
      (agent_unequip_item, ":player", "itm_dwarf_shield_b"),
      (agent_equip_item, ":player", "itm_dwarf_shield_reward"),
      (agent_set_wielded_item, ":player", "itm_dwarf_shield_reward"),
    (else_try),
      (eq, ":weapon_selection", 3),
      (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 50),
      (troop_raise_skill, "$g_player_troop", skl_power_throw, 5),
      (troop_raise_skill, "$g_player_troop", skl_power_strike, 3),
      (troop_raise_skill, "$g_player_troop", skl_athletics, 3),
      (agent_unequip_item, ":player", "itm_dwarf_great_axe"),
      (agent_equip_item, ":player", "itm_dwarf_great_axe_reward"),
      (agent_set_wielded_item, ":player", "itm_dwarf_great_axe_reward"),
      (agent_refill_ammo, ":player"),
    (try_end),
    (troop_raise_attribute, "$g_player_troop", ca_strength, 5),
    (troop_raise_attribute, "$g_player_troop", ca_agility, 5),
    (display_message, "@With Lord Balin's treasures bestowed upon you and the memory of his death fresh in your mind, your rage burns stronger. (Attributes, Abilities and Weapon Profeciencies Improved)", color_neutral_news),
  ]],

  [anyone, "start", [(eq, "$g_talk_troop", "trp_generic_hero_infantry"),(ge, "$enemy_reinforcement_stage", 10),
                      (store_random_in_range, ":random_speech", 0, 6), 
                      (try_begin),
                        (eq, ":random_speech", 0),
                        (str_store_string, s5, "@We cannot hold... we are finished..."),
                        (str_store_string, s6, "@You do not know how long you can still last..."),
                      (else_try),
                        (eq, ":random_speech", 1),
                        (str_store_string, s5, "@How long can we keep this up? I cannot hold my axe anymore...."),
                        (str_store_string, s6, "@You know that the end is near..."),
                      (else_try),
                        (eq, ":random_speech", 2),
                        (str_store_string, s5, "@You.... good....dwarf...."),
                        (str_store_string, s6, "@You can no longer raise your weapon..."),
                      (else_try),
                        (eq, ":random_speech", 3),
                        (str_store_string, s5, "@There are too many... there are too many...."),
                        (str_store_string, s6, "@.........."),
                      (else_try),
                        (eq, ":random_speech", 4),
                        (str_store_string, s5, "@It is off to work we go...."),
                        (str_store_string, s6, "@Your mind starts to wander... thinking of gold and treasures..."),
                      (else_try),
                        (eq, ":random_speech", 5),
                        (str_store_string, s5, "@..............."),
                        (str_store_string, s6, "@Sleep sounds good..."),
                      (else_try),
                        (str_store_string, s5, "@For Balin!!"),
                        (str_store_string, s6, "@For Balin..."),
                      (try_end),],
  "{s5}", "close_window", 
  [ (assign, "$ally_reinforcement_stage", 8), (display_message, "@{s6}", color_neutral_news)]],

] or []) + [ 

######## Ori's Last Stand END ##############

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
      (this_or_next|is_between, "$g_talk_troop", companions_begin, companions_end),
      (is_between, "$g_talk_troop", new_companions_begin, new_companions_end),
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

[anyone|plyr,"free", [[in_meta_mission]], " Good-bye.", "close_window",[(call_script,"script_stand_back"),]],
[anyone|plyr,"free", [[neg|in_meta_mission]], " [Leave]", "close_window",[(call_script,"script_stand_back"),]],

[anyone,"free", [], "NO MATCHING SENTENCE!", "close_window",[(call_script,"script_stand_back"),]],
[anyone,"start", [], "NO MATCHING SENTENCE!", "close_window",[(call_script,"script_stand_back"),]],

]
