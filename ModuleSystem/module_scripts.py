# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from ID_animations import *
from ID_troops import *
from ID_factions import *
from module_troops import *

from module_scripts_ai import *
from module_scripts_form import *
from module_scripts_morale import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

### a crude code to insert an increasing number (mtarini)
___val = 0 
def next_count(): 
  global ___val
  ___val=___val+1
  return ___val
def first_count(): 
  global ___val
  ___val=0
  return ___val
def curr_count(): 
  global ___val
  return ___val
  
### TLD item factionization, with subfactions (mtarini, GA)
def set_item_faction():
	command_list = []
	for i_troop in xrange(29,430): #regular troops here
		# mtarini: store all flags in a slot, for later use
		command_list.append((troop_set_slot, i_troop, slot_troop_flags, troops[i_troop][3]))
	for i_troop in xrange(29,823): #all troops
		#GA assign troops to proper subfactions acc to troops[i_troop][5]
		troopsub = troops[i_troop][5]
		if troopsub > 0: command_list.append((troop_set_slot, i_troop, slot_troop_subfaction, troopsub))
	for i_item in xrange(23,825): #regular items here
		faction = 0
		sfaction = 0
		for i_troop in xrange(29,430): # search items inside troop inventory
			if i_item in troops[i_troop][7]:
				faction = faction | (1 << troops[i_troop][6])
				troopsub = troops[i_troop][5]
				if troopsub > 0: sfaction = sfaction | (1 << troops[i_troop][5])
		if faction > 0: command_list.append((item_set_slot, i_item, slot_item_faction, faction))
		if sfaction > 0: command_list.append((item_set_slot, i_item, slot_item_subfaction, sfaction))
	return command_list [:]

companionPriceMult = 100 # this is used to multiply old hiring praces for companions (in res point) to new prices (in influence) - MV: nerfed down to 50, was 20 - another nerf, Glorfindel now 50, others reasonable

scripts = [

("troop_get_cheer_sound", [
	(store_script_param_1, ":trp"),		
	(troop_get_type, ":race",":trp"),
	(try_begin),(eq,":race",0x0),(assign,reg1,"snd_man_victory"),
	(else_try), (eq,":race",0x1),(assign,reg1,-1), # woman
	(else_try), (eq,":race",0x2),(assign,reg1,"snd_gondor_victory_player"),
	(else_try), (eq,":race",0x3),(assign,reg1,"snd_rohan_victory"),
	(else_try), (eq,":race",0x4),(assign,reg1,"snd_dunlender_victory"),
	(else_try), (eq,":race",0x5),(assign,reg1,"snd_orc_victory"),
	(else_try), (eq,":race",0x6),(assign,reg1,"snd_uruk_victory"),
	(else_try), (eq,":race",0x7),(assign,reg1,"snd_uruk_victory"),
	(else_try), (eq,":race",0x8),(assign,reg1,"snd_haradrim_victory"),
	(else_try), (eq,":race",0x9),(assign,reg1,"snd_man_victory"), # dwarf
	(else_try), (eq,":race",0xA),(assign,reg1,"snd_troll_victory"),
	(else_try), (eq,":race",0xB),(assign,reg1,"snd_dunedain_victory_player"),
	(else_try), (eq,":race",0xC),(assign,reg1,"snd_mirkwood_victory_player"),
	(else_try), (eq,":race",0xD),(assign,reg1,"snd_mirkwood_victory_player"),
	(else_try), (eq,":race",0xE),(assign,reg1,"snd_mirkwood_victory_player"),
	(else_try), (eq,":race",0xF),(assign,reg1,"snd_man_victory"), # Khand   +  Rhun   +   Easterling
	(else_try),(assign,reg1,"snd_man_victory"), 
	(try_end),
]),

############################# TLD player icon (mtarini)
# script_init_player_map_icons
("init_player_map_icons",[
	# defaults
  	(assign, "$g_player_icon_mounted", "icon_player_horseman"),
	(assign, "$g_player_icon_foot_melee", "icon_player"),
	(assign, "$g_player_icon_foot_archer","icon_player"),

	(assign, ":fac","$players_kingdom"),
	(troop_get_type, ":race","$g_player_troop"),
	(assign, ":subfac","$players_subkingdom"),
	(assign, ":subfac","$players_subkingdom"),

	(try_begin),
		(eq,0,1),
	]+concatenate_scripts([
	(else_try),
		(eq, ":fac", faction_player_icons[y][0]),
		(assign, "$g_player_icon_mounted",    faction_player_icons[y][1]),
		(assign, "$g_player_icon_foot_melee", faction_player_icons[y][2]),
		(assign, "$g_player_icon_foot_archer",faction_player_icons[y][3]),
	]for y in range(len(faction_player_icons)) ) +[
	(try_end),
	# overrite choice for gondor subfaction
	(try_begin),(eq, ":fac", "fac_gondor"), 
	(try_begin),
		(eq,0,1),
	]+concatenate_scripts([
	(else_try),
		(eq, ":subfac", subfaction_gondor_player_icons[y][0]),
		(assign, "$g_player_icon_mounted",    subfaction_gondor_player_icons[y][1]),
		(assign, "$g_player_icon_foot_melee", subfaction_gondor_player_icons[y][2]),
		(assign, "$g_player_icon_foot_archer",subfaction_gondor_player_icons[y][3]),
	]for y in range(len(subfaction_gondor_player_icons)) ) +[
	(try_end),
	(try_end),
		
	# fix mordor and isengard NON orcs
	(try_begin),
		(neg|is_between, ":race", tf_orc_begin, tf_orc_end),
		(try_begin),
			(eq, ":fac", "fac_mordor"),
			(assign, "$g_player_icon_mounted", "icon_mordor_captain"),
			(assign, "$g_player_icon_foot_melee", "icon_player"),
			(assign, "$g_player_icon_foot_archer","icon_player"),
		(try_end),
		(try_begin),
			(eq, ":fac", "fac_isengard"),
			(assign, "$g_player_icon_mounted", "icon_isengard_captain"),
			(assign, "$g_player_icon_foot_melee", "icon_player"),
			(assign, "$g_player_icon_foot_archer","icon_player"),
		(try_end),		
	(try_end),
	# fix mordor and isengard orcs NON uruk (non mounted only)
	(try_begin),
		(eq, ":race", tf_orc),
		(try_begin),
			(eq, ":fac", "fac_mordor"),
			(assign, "$g_player_icon_foot_melee", "icon_orc"),
			(assign, "$g_player_icon_foot_archer","icon_orc"),
		(try_end),
		(try_begin),
			(eq, ":fac", "fac_isengard"),
			(assign, "$g_player_icon_foot_melee", "icon_orc_isengard"),
			(assign, "$g_player_icon_foot_archer","icon_orc_isengard"),
		(try_end),		
	(try_end),	
]),

# script_determine_what_player_looks_like  
# no input. Call me when player can have changed look   (mtarini)
("determine_what_player_looks_like", [
    (troop_get_type, ":race","$g_player_troop"),
	(try_begin),
		(is_between, ":race", tf_orc_begin, tf_orc_end),
		(assign, "$player_looks_like_an_orc",1),
	(else_try),
		(assign, "$player_looks_like_an_orc",0),
	(try_end),
]),

#############################  TLD PLAYER REWARD SYSTEM --- SCRIPTS   (mtarini)  #############################?#
# script_player_meets_party 
# PlayerRewardSystem: call this when enetring a city, or meeting a party, so that player's "gold" will update    (mtarini)
# param1: encountered party
("player_meets_party",[
    #MV: old code: didn't work too well, should have detected "territory", not opposing party faction
	# (try_begin),
	  # (store_script_param_1, ":party"),
	  # (store_faction_of_party, ":fac", ":party"),
	  # (is_between, ":fac", kingdoms_begin, kingdoms_end),
	  # (neq, "$ambient_faction", ":fac"), # no need to swap anything, already right
	  # (store_relation, reg0, "fac_player_faction", ":fac"),
      # (ge, reg0, 0), # only with non-enemies	
	  # (call_script, "script_set_ambient_faction", ":fac"),
	# (try_end),

	(store_script_param_1, ":party"),

	(assign, ":closest_faction", -1),
	(try_begin),
		# check if visiting a friendly town, to optimize code
		(is_between, ":party", centers_begin, centers_end),
		(store_faction_of_party, ":center_faction", ":party"),
		(store_relation, ":relation", ":center_faction", "$players_kingdom"),
		(ge, ":relation", 0),
		(assign, ":closest_faction", ":center_faction"),
	(else_try),
		# find closest friendly active center to determine in whose "territory" is the main party
		(assign, ":mindist", 100000),
		(try_for_range, ":center_no", centers_begin, centers_end),
			(party_is_active, ":center_no"),
			(party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD - not destroyed
			(store_faction_of_party, ":center_faction", ":center_no"),
			(store_relation, ":relation", ":center_faction", "$players_kingdom"),
			(ge, ":relation", 0), # friendly center found
			(store_distance_to_party_from_party, ":dist", "p_main_party", ":center_no"),
			(lt, ":dist", ":mindist"),
			(assign, ":mindist", ":dist"),
			(assign, ":closest_faction", ":center_faction"),
		(try_end),
		(try_begin),
			(eq, ":closest_faction", -1), #all friendly factions defeated, the player is his own faction :)
			(assign, ":closest_faction", "$players_kingdom"),
		(try_end),
	(try_end),
	(try_begin),
		(neq, "$ambient_faction", ":closest_faction"), # no need to swap anything, already right
		(call_script, "script_set_ambient_faction", ":closest_faction"),
	(try_end),
]),

# script_add_faction_rps  
# PlayerRewardSystem:  adds / removes (if neg) some respoints (parameter2) to a given faction (parameter1)  (mtarini)
# messes up s0, reg0
("add_faction_rps",[
	(store_script_param_1, ":fac"),
	(store_script_param_2, ":diff"),
	(store_mul,  ":diff_neg",  ":diff", -1), # diff = - diff
	(try_begin),
		(eq, "$ambient_faction", ":fac"), 
		# just rise player gold 
		(set_show_messages, 0),
		(try_begin),(gt, ":diff", 0),
			(troop_add_gold, "$g_player_troop", ":diff"),
		(else_try),
			(troop_remove_gold, "$g_player_troop", ":diff_neg"),
		(try_end),
		(set_show_messages, 1),
	(try_end),

	# rise res. points of that faction
	(faction_get_slot,  ":rp", ":fac", slot_faction_respoint),
	(store_add,":rp",":rp",":diff"),
	(faction_set_slot, ":fac", slot_faction_respoint, ":rp"),

	# mordor and guldur common currency
	(try_begin),
		(eq, ":fac", "fac_mordor"),
		(faction_set_slot, "fac_guldur", slot_faction_respoint, ":rp"),		 	
	(try_end), 
	(try_begin),
		(eq, ":fac", "fac_guldur"), 
		(faction_set_slot, "fac_mordor", slot_faction_respoint, ":rp"),	
	(try_end),

	# CC: fixes the problem where mordor and guldur resources weren't correctly mixing.	
	(try_begin),
		(eq|this_or_next, "$ambient_faction", "fac_mordor"),
		(eq, "$ambient_faction", "fac_guldur"),
		(store_troop_gold, ":cur_gold", "$g_player_troop"),
		(faction_get_slot,  ":rps", "$ambient_faction", slot_faction_respoint),
		(store_sub, ":rps_diff", ":rps", ":cur_gold"),
		(set_show_messages, 0),
		(try_begin),
			(gt, ":rps_diff", 0),
			(troop_remove_gold, "$g_player_troop", ":rps_diff"),
		(else_try),
			(lt, ":rps_diff", 0),
			(troop_add_gold, "$g_player_troop", ":rps_diff"),
		(try_end),
		(set_show_messages, 1),
	(try_end),	

	(str_store_faction_name, s0, ":fac"),
	(try_begin),(gt, ":diff", 0),
		(assign, reg0, ":diff"),
		(display_message, "@You gained {reg0} Resource Points of {s0}."),
	(else_try),(gt, ":diff_neg", 0),
		(assign, reg0, ":diff_neg"),
		(display_message, "@You lost {reg0} Resource Points of {s0}."),
	(try_end),
]),

# script_update_respoint
# PlayerRewardSystem, update_respoint script: makes sure that respoints of active faction reflect current "gold"(no params)  (mtarini)
("update_respoint",[
	(store_troop_gold, ":cur_gold", "$g_player_troop"),
	(faction_set_slot, "$ambient_faction", slot_faction_respoint, ":cur_gold"),
	(try_begin),(eq, "$ambient_faction", "fac_mordor"), (faction_set_slot, "fac_guldur", slot_faction_respoint, ":cur_gold"),(try_end), # mordor and guldur common currency
	(try_begin),(eq, "$ambient_faction", "fac_guldur"), (faction_set_slot, "fac_mordor", slot_faction_respoint, ":cur_gold"),(try_end),
]),

# script_reward_system_init
# PlayerRewardSystem: init (mtarini)
("reward_system_init",[
	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(try_begin),
			(eq,"$players_kingdom", ":fac"),
			(store_troop_gold, ":gold_player", "$g_player_troop"),
			(faction_set_slot,  ":fac", slot_faction_influence, 1),
			(faction_set_slot,  ":fac", slot_faction_rank     , 50),
			(faction_set_slot,  ":fac", slot_faction_respoint , ":gold_player"),
			(assign, "$ambient_faction", ":fac"),
		(else_try),
			(faction_set_slot,  ":fac", slot_faction_influence, 0),
			(faction_set_slot,  ":fac", slot_faction_rank     , 0),
			(faction_set_slot,  ":fac", slot_faction_respoint , 0),
		(try_end),
	(try_end),
	#(str_store_faction_name,s3,"$players_kingdom"),(store_troop_gold, reg3, "$g_player_troop"),
	#(display_message, "@debug: player has faction '{s3}' and {reg3} gold"),
	#]+concatenate_scripts([
	#	(store_set_slot, faction_init[y][0], slot_faction_influence, 0),
	#	(store_set_slot, faction_init[y][0], slot_faction_rank, 0),
	#	(store_set_slot, faction_init[y][0], slot_faction_respoint, 0),
	#]for y in range(len(faction_init)) ) +[
]),

# script_set_ambient_faction
# PlayerRewardSystem, script: stores current gold to appropriate faction's respoint, and resoruce point of a parameter faction to current gold  (mtarini)
# param1: new current faction
("set_ambient_faction",[
    (try_begin),
      (store_script_param_1, ":fac"),
	  (store_troop_gold, ":old_gold", "$g_player_troop"),
	  (faction_get_slot, ":new_gold",  ":fac", slot_faction_respoint),
	  (faction_set_slot, "$ambient_faction", slot_faction_respoint, ":old_gold"),
	
	  (neq, "$ambient_faction", ":fac"), # no need to swap, already right
	  (assign, "$ambient_faction", ":fac"),	
	
	  (set_show_messages, 0),
	  (try_begin),
        (gt, ":old_gold", ":new_gold"),
		(store_sub, ":diff", ":old_gold", ":new_gold"),
		(troop_remove_gold, "$g_player_troop", ":diff"),
	  (else_try),
		(store_sub, ":diff", ":new_gold", ":old_gold"),
		(troop_add_gold, "$g_player_troop", ":diff"),
	  (try_end),
	  (set_show_messages, 1),
	#(str_store_faction_name, s10, "$ambient_faction"),			
	#(display_message, "@info: now using Resource Pts. of {s10}." ),
	(try_end),
]),

# script_rank_income_to_player
# PlayerRewardSystem: rank_income (mtarini)
# gives to player the income of his rank
# messes up s24
("rank_income_to_player",[
	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":fac", slot_faction_state, sfs_active), #MV fix: dead factions don't pay you

		# Allows us modders to cap the resource points income. (CppCoder)
		(faction_get_slot, ":total_rp",  ":fac", slot_faction_respoint),
		(this_or_next|eq, tld_rp_cap, -1),
		(lt, ":total_rp", tld_rp_cap),

		(call_script, "script_get_faction_rank", ":fac"),
		(assign, ":rank", reg0),
		(gt, ":rank", 0),
		(call_script, "script_get_rank_title_to_s24", ":fac"),
		(display_message, "@{s24}:"),
		(store_mul, ":income", ":rank", ":rank"), 
		(store_mul, ":rank10", ":rank", 10), 
		(val_mul, ":income", 5),  #  ( rank^2 *5 +rank * 10) =  0,  15 , 30, 55, 90 , 135, 190, 255, ... per day.
		(val_add, ":income", ":rank10"),
		(call_script, "script_add_faction_rps", ":fac", ":income"),
	(try_end),
]),

# script_get_own_rank_title_to_s24 
# PlayerRewardSystem, script: stores in s24 title of home faction rank 
# param1: faction
# param2: rank 
# param3: career variant (e.g. ranger vs knight) TODO
# output: string 24
("get_own_rank_title_to_s24",[
	(store_script_param_1, ":faction"),
	(store_script_param_2, ":rank"),
    (val_clamp, ":rank", 0, 10),
    
    (store_sub, ":string", ":faction", kingdoms_begin),
    (val_mul, ":string", 10), #10 ranks
    (val_add, ":string", ":rank"),
    (val_add, ":string", "str_gondor_rank_0"),
    (str_store_string, s24, ":string"),
]),

# script_get_allied_rank_title_to_s24
# PlayerRewardSystem, script: stores in s24 title of a faction, rank, career  (mtarini)
# param1: faction
# param2: rank 
# output: string 24
# messes up s5
("get_allied_rank_title_to_s24",[
	(store_script_param_1, ":fac"),
	(store_script_param_2, ":rank"),
	(str_store_faction_name, s5, ":fac"),
    (try_begin),
        (faction_slot_eq, ":fac", slot_faction_side, faction_side_good),
        (try_begin),(ge, ":rank", 9),(str_store_string, s24, "@Great Hope of {s5}"),
         (else_try),(eq, ":rank", 8),(str_store_string, s24, "@Hope of {s5}"),
         (else_try),(eq, ":rank", 7),(str_store_string, s24, "@Indispensable Ally of {s5}"),
         (else_try),(eq, ":rank", 6),(str_store_string, s24, "@Faithful Ally of {s5}"),
         (else_try),(eq, ":rank", 5),(str_store_string, s24, "@Trusted Friend of {s5}"),
         (else_try),(eq, ":rank", 4),(str_store_string, s24, "@Close Friend of {s5}"),
         (else_try),(eq, ":rank", 3),(str_store_string, s24, "@Friend of {s5}"),
         (else_try),(eq, ":rank", 2),(str_store_string, s24, "@Familiar to {s5}"),
         (else_try),(eq, ":rank", 1),(str_store_string, s24, "@Known to {s5}"),
         (else_try),                 (str_store_string, s24, "@Stranger to {s5}"),
        (try_end),
    (else_try),
        (try_begin),(ge, ":rank", 9),(str_store_string, s24, "@Great Enforcer of {s5}"),
         (else_try),(eq, ":rank", 8),(str_store_string, s24, "@Enforcer of {s5}"),
         (else_try),(eq, ":rank", 7),(str_store_string, s24, "@Important Ally of {s5}"),
         (else_try),(eq, ":rank", 6),(str_store_string, s24, "@Ally of {s5}"),
         (else_try),(eq, ":rank", 5),(str_store_string, s24, "@Accomplice of {s5}"),
         (else_try),(eq, ":rank", 4),(str_store_string, s24, "@Useful Tool of {s5}"),
         (else_try),(eq, ":rank", 3),(str_store_string, s24, "@Servant of {s5}"),
         (else_try),(eq, ":rank", 2),(str_store_string, s24, "@Familiar to {s5}"),
         (else_try),(eq, ":rank", 1),(str_store_string, s24, "@Known to {s5}"),
         (else_try),                 (str_store_string, s24, "@Unknown to {s5}"),
        (try_end),
    (try_end),
]),

# script_get_rank_title_to_s24  
("get_rank_title_to_s24",[
	(store_script_param_1, ":faction"),
    (call_script, "script_get_faction_rank", ":faction"),
    (assign, ":rank", reg0),
    (call_script, "script_get_any_rank_title_to_s24", ":faction", ":rank"),
]),

# script_get_any_rank_title_to_s24  
("get_any_rank_title_to_s24",[
	(store_script_param_1, ":faction"),
	(store_script_param_2, ":rank"),
	(try_begin),
		(eq, ":faction", "$players_kingdom"),
		(call_script, "script_get_own_rank_title_to_s24", ":faction", ":rank"),
	(else_try),
		(call_script, "script_get_allied_rank_title_to_s24", ":faction", ":rank"),
	(try_end),
]),

# script_new_rank_attained
# messes up s10
("new_rank_attained",
    [ (store_script_param_1, ":fac"),
      (store_script_param_2, ":rank"),
      (store_script_param, ":is_promoted", 3),
	  (play_sound, "snd_level_up"),
	  (call_script, "script_get_rank_title_to_s24", ":fac"),
	  (str_store_troop_name, s10, "trp_player"),
      (assign, reg0, ":rank"),
      (assign, reg1, ":is_promoted"),
      (assign, ":news_color", color_bad_news),
      (try_begin),
        (eq, ":is_promoted", 1),
        (assign, ":news_color", color_good_news),
      (try_end),
	  (display_message, "@You have been {reg1?promoted:demoted} to {s24} ({reg0})!", ":news_color"),
]),

# script_increase_rank
# difference can be a negative value
# messes up s11
("increase_rank",
    [ (store_script_param_1, ":fac"),# gain rank (need rank points to advance)
      (store_script_param_2, ":difference"),
      
	  (try_begin),
          (is_between, ":fac", kingdoms_begin, kingdoms_end),
          (neq, ":difference", 0),
          (call_script, "script_get_faction_rank", ":fac"),
          (assign, ":old_rank", reg0),
          (faction_get_slot, ":val", ":fac", slot_faction_rank),
          (val_add, ":val", ":difference"),
          (ge, ":val", 0), #no negative rank points
          (faction_set_slot, ":fac", slot_faction_rank, ":val"),
          (call_script, "script_get_faction_rank", ":fac"),
          (assign, ":new_rank", reg0),
          
        # gain influence = 1/8 rank points gain (rounded) Was 1/10
          (faction_get_slot, ":val", ":fac", slot_faction_influence),
          (store_add, ":inf_dif", ":difference", 8/2),
          (val_div, ":inf_dif", 8),
          (val_add, ":val", ":inf_dif"),
          (faction_set_slot, ":fac", slot_faction_influence, ":val"),

          # display message
          # (store_mod, reg10, ":difference", 100),(store_div, reg11, ":difference", 100),
          # (try_begin), (lt, reg10, 10), (str_store_string, s10, "@.0"), (else_try), (str_store_string, s10, "@."), (try_end),
          (str_store_faction_name, s11, ":fac"),
          (assign, reg11, ":difference"),
          (assign, reg12, ":inf_dif"),
          (assign, reg1, 1),
          (assign, ":news_color", color_good_news),
          (try_begin),
            (lt, reg11, 0),
            (val_abs, reg11),
            (val_abs, reg12),
            (assign, reg1, 0),
            (assign, ":news_color", color_bad_news),
          (try_end),
#          (display_message, "@{reg1?Earned:Lost} {reg12} influence with {s11}.", ":news_color"), # MV: why do this??
          (display_message, "@You {reg1?earned:lost} {reg11} rank points {reg12?and {reg12} influence :}with {s11}.", ":news_color"),
          
          # rank increased?
          (try_begin),
            (neq, ":old_rank", ":new_rank"),
            (call_script, "script_new_rank_attained", ":fac", ":new_rank", reg1),
          (try_end),
      (try_end),
]),

# script_get_faction_rank
# converts rank points to rank number
# input: faction
# output: reg0 = rank 0-9 or higher
("get_faction_rank",
    [ (store_script_param_1, ":faction"),
    
      (faction_get_slot, ":rank_points", ":faction", slot_faction_rank),
    # current formula rank points (rank) = Ax^2 + Bx
      (assign, ":A", 5),
      (assign, ":B", 45),
    # rank = (sqrt(B*B+4*A*rp)-B)/(2*A)
      (store_mul, ":AC4", ":rank_points", 4),
      (val_mul, ":AC4", ":A"),
      (store_mul, ":rank", ":B", ":B"),
      (val_add, ":rank", ":AC4"),
      (convert_to_fixed_point, ":rank"),
      (store_sqrt, ":rank", ":rank"),
      (convert_from_fixed_point, ":rank"),
      (val_sub, ":rank", ":B"),
      (val_div, ":rank", 2),
      (val_div, ":rank", ":A"),
    
      (assign, reg0, ":rank"),
]),

# script_get_rank_points_for_rank
# converts rank number to rank points
# input: rank 0-9 or higher
# output: reg0 = rank points needed
("get_rank_points_for_rank",
    [ (store_script_param_1, ":rank"),
      # current formula rank points (rank) = Ax^2 + Bx
      (assign, ":A", 5),
      (assign, ":B", 45),
      (store_mul, ":ranksquared", ":rank", ":rank"),
      (store_mul, ":rank_points", ":ranksquared", ":A"),
      (store_mul, ":Bx", ":rank", ":B"),
      (val_add, ":rank_points", ":Bx"),
      (assign, reg0, ":rank_points"),
]),

# script_find_closest_enemy_town_or_host  
# input: faction f,  party x
# output: reg0 = closest party to x enemy of f, but friend of player, reg1 = its distance
("find_closest_enemy_town_or_host",[
	(store_script_param, ":fac", 1),
	(store_script_param, ":target", 2),
	(assign, ":mindist", 100000),
	(assign, ":res", -1),
    (try_for_parties, ":party"),
       (party_is_active, ":party"),
	   
       (party_slot_eq, ":party", slot_center_destroyed, 0), # TLD
       (this_or_next|party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_party),  # its a host
       (this_or_next|party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_alone),  # or a lone hero
	   (is_between, ":party", centers_begin, centers_end),  #or a town
	   
	   (store_faction_of_party, ":pfac", ":party"),
	   (store_relation, ":relation", ":pfac", ":fac"),
	   (lt, ":relation", 0), # it's an enemy...
	   
	   (store_relation, ":relation", ":pfac", "$players_kingdom"),
	   (ge, ":relation", 0), # and it's your friend
 
       (store_distance_to_party_from_party, ":dist", ":party", ":target"),
       (lt, ":dist", ":mindist"),
	   (assign, ":mindist", ":dist"),
	   (assign, ":res", ":party"),
     (try_end),
	 (assign, reg0, ":res"),
	 (assign, reg1, ":dist"),
]),

#script_spend_influence_of
("spend_influence_of",[
	(store_script_param_1, ":price"),
	(store_script_param_2, ":fac"),
	
    (faction_get_slot, ":influence", ":fac",  slot_faction_influence),
    (val_sub, ":influence", ":price"),
    (faction_set_slot, ":fac",  slot_faction_influence, ":influence"),
    (str_store_faction_name, s1, ":fac"),
    (assign, reg10, ":price"),
    (assign, reg11, ":influence"),
    (display_message, "@You spent {reg10} of your influence with {s1}, with {reg11} remaining.")
]),
	 
# script_game_get_join_cost
# This script is called from the game engine for calculating troop join cost.
# Input:   param1: troop_id,
# Output: reg0: join cost
("game_get_join_cost",
  [ (store_script_param_1, ":troop_id"),
	(call_script, "script_game_get_troop_wage", ":troop_id",0),
	(store_mul, ":join_cost", reg0, 3), # to join, twice than day upkeep x 3
    
    # trait discounts: 75% of the original price
    (store_troop_faction, ":troop_faction", ":troop_id"),
    (assign, ":apply_discount", 0),
    (try_begin),
      (eq, ":troop_faction", "fac_gondor"),
      (troop_slot_eq, "trp_traits", slot_trait_gondor_friend, 1),
      (assign, ":apply_discount", 1),
    (try_end),
    (try_begin),
      (eq, ":troop_faction", "fac_rohan"),
      (troop_slot_eq, "trp_traits", slot_trait_rohan_friend, 1),
      (assign, ":apply_discount", 1),
    (try_end),
    (try_begin),
      (this_or_next|eq, ":troop_faction", "fac_lorien"),
      (this_or_next|eq, ":troop_faction", "fac_imladris"),
      (eq, ":troop_faction", "fac_woodelf"),
      (troop_slot_eq, "trp_traits", slot_trait_elf_friend, 1),
      (assign, ":apply_discount", 1),
    (try_end),
    (try_begin),
      (this_or_next|eq, ":troop_faction", "fac_harad"),
      (this_or_next|eq, ":troop_faction", "fac_rhun"),
      (eq, ":troop_faction", "fac_khand"),
      (troop_slot_eq, "trp_traits", slot_trait_brigand_friend, 1),
      (assign, ":apply_discount", 1),
    (try_end),
    (try_begin),
      (eq, ":apply_discount", 1),
      (val_mul, ":join_cost", 3),
      (val_div, ":join_cost", 4),
    (try_end),
     
    (assign, reg0, ":join_cost"),
	(set_trigger_result, reg0),
]),
  
# script_get_troop_disband_cost
# Call this script to know how much the player earns if he sends this troop home  (mtarini)
# Input:   param1: troop_id,  
# Input:   param2: 0 = auto, 1 = perfect helath  2 =  wounded
# Input:   param3: 0 = sent home from map,   1 = given to city,    2 = given to host
# Output: reg0: leave cost
("get_troop_disband_cost",
  [	    (store_script_param_1, ":troop_id"),
		(store_script_param_2, ":opt"),
		(store_script_param,   ":origin", 3),
		
		# determine if troop is wounded
		(assign, ":wounded",0),
		(try_begin),(eq,":opt",0), # auto check if wounded
			(try_begin),
			  (call_script, "script_cf_is_troop_in_party_wounded", ":troop_id", "p_main_party"),
			  (assign, ":wounded",1),
			(try_end),
		(else_try),  (eq,":opt",2), # assume it is wounded
			(assign, ":wounded",1),
		(try_end),

		(assign, ":perc", 80), # base: 80 percent
		(try_begin),(eq,":origin",0), (assign, ":perc", 70), (try_end), # from map: 70%
		(try_begin),(eq,":origin",1), (assign, ":perc", 80), (try_end), # to city garrison: 80%
		(try_begin),(eq,":origin",2), (assign, ":perc", 90), (try_end), # to war party: 90%
		(try_begin),(eq,":wounded",1),(val_sub,":perc", 30), (try_end), # if wounded: -30%
		
		(call_script, "script_game_get_join_cost", ":troop_id"),
		(val_mul, reg0, ":perc"), 
		(val_div, reg0, 100), # when this troop leaves, you gain  $ join_cost * perc/100  
]),

# script_get_party_disband_cost 
# Call this script to know how much the player earns if this entire party is disbanded (mtarini)
# Input:   param1: party_id,  
# Input:   param2: 0 = sent home from map,   1 = given to city    2 = given to host
# Output: reg0: leave cost of party  
("get_party_disband_cost",
  [	(store_script_param_1, ":party_id"),
	(store_script_param_2, ":origin"),
	(party_get_num_companion_stacks, ":num_stacks", ":party_id"),
	(assign, ":tot", 0),
	(try_for_range, ":i", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",  ":party_id", ":i"),
        (party_stack_get_size, ":n_ok", ":party_id", ":i"),
        (party_stack_get_num_wounded, ":n_wounded", ":party_id", ":i"),
		(val_sub, ":n_ok", ":n_wounded"),
		
        (call_script, "script_get_troop_disband_cost", ":stack_troop",1,":origin"),
        (val_mul, reg0, ":n_ok"),
        (val_add, ":tot", reg0),
		
        (call_script, "script_get_troop_disband_cost", ":stack_troop",2,":origin"),
        (val_mul, reg0, ":n_wounded"),
        (val_add, ":tot", reg0),
    (try_end),
    (assign, reg0, ":tot"),
]),

# script_game_get_troop_wage  
# This script is called from the game engine for calculating troop wages.  (mod by mtarini)
# Input: param1: troop_id, param2: party-id
# Output: reg0: weekly wage
("game_get_troop_wage",
    [ (store_script_param_1, ":troop_id"),
      (store_script_param_2, ":unused"), #party id
  
      (store_troop_faction, ":troop_faction", ":troop_id"),
	  (store_character_level, ":troop_level", ":troop_id"),
      (assign, ":wage", ":troop_level"),
      (val_add, ":wage", 3),
      (val_mul, ":wage", ":wage"),
      (val_div, ":wage", 25),

	  (troop_get_type, ":race", ":troop_id"),
	  (try_begin),
        (eq, ":race", tf_troll),
		(val_add, ":wage", 5),
		(val_mul, ":wage", 27),# trolls cost x 27
	  (try_end),
	  
      (try_begin), #mounted troops cost 50% more than the normal cost
        (troop_is_mounted, ":troop_id"),
        (val_mul, ":wage", 150),
        (val_div, ":wage", 100),
      (try_end),
	  (try_begin), #discount if you have beorning chief armor
	  (troop_has_item_equipped, "trp_player", "itm_beorn_chief"),
	  (eq, ":troop_faction", "fac_beorn"),
        (val_mul, ":wage", 100),
        (val_div, ":wage", 115),
      (try_end),
	  (try_begin), #discount if you have chieftain sword
	  (troop_has_item_equipped, "trp_player", "itm_dun_berserker"),
	  (eq, ":troop_faction", "fac_dunland"),
        (val_mul, ":wage", 100),
        (val_div, ":wage", 115),
      (try_end),
	  
	  (try_begin), #discount if you have warg rider helmet
	  (troop_has_item_equipped, "trp_player", "itm_gundabad_helm_e"),
	  (this_or_next|eq, ":troop_id", "trp_goblin_rider_gundabad"),
	  (this_or_next|eq, ":troop_id", "trp_warg_rider_gundabad"),
        (eq, ":troop_id", "trp_goblin_north_clan_rider"),
		  (val_mul, ":wage", 100),
        (val_div, ":wage", 120),
      (try_end),
	   (try_begin), #discount if you have warg rider helmet
	  (troop_has_item_equipped, "trp_player", "itm_gundabad_helm_e"),
	  (this_or_next|eq, ":troop_id", "trp_wolf_rider_of_moria"),
	  (this_or_next|eq, ":troop_id", "trp_warg_rider_of_moria"),
	  (this_or_next|eq, ":troop_id", "trp_warg_rider_of_gorgoroth"),
	  (this_or_next|eq, ":troop_id", "trp_great_warg_rider_of_mordor"),
	  (this_or_next|eq, ":troop_id", "trp_wolf_rider_of_isengard"),
	  (this_or_next|eq, ":troop_id", "trp_warg_rider_of_isengard"),
	  (this_or_next|eq, ":troop_id", "trp_white_hand_rider"),
        (eq, ":troop_id", "trp_bolg_clan_rider"),
		  (val_mul, ":wage", 100),
        (val_div, ":wage", 110),
      (try_end),
       
	  (try_begin),
		(troop_is_hero,":troop_id"), # no upkeep for heros! (player included)
		(assign, reg0, 0),
      (try_end),
      
	  (try_begin),
		(neg|is_between, ":troop_faction", kingdoms_begin, kingdoms_end), # bandits are free
		(assign, reg0, 0),
      (try_end),
	  
      (assign, reg0, ":wage"),
      (set_trigger_result, reg0),
]),

# script_game_get_total_wage  (mod by mtarini)
# This script is called from the game engine for calculating total wage of the player party which is shown at the party window.
# Input: none
# Output: reg0: weekly wage
("game_get_total_wage",
    [ (assign, ":total_wage", 0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
        (call_script, "script_game_get_troop_wage", ":stack_troop",0),
        (val_mul, reg0, ":stack_size"),
        (val_add, ":total_wage", reg0),
      (try_end),
      (assign, reg0, ":total_wage"),
      (set_trigger_result, reg0),
]),

#MV: Note that non-kingdom troops like bandits don't need upkeep!

# script_compute_wage_per_faction  (mtarini)
# Input: arg1 = faction
# Output: reg4 = weekly wage per faction (player has to pay)
("compute_wage_per_faction",
  [ (store_script_param_1, ":fac"),
	(assign, ":party", "p_main_party"),
	(assign, ":spending",  0), # for this faction
	(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
	
	(try_for_range, ":i", 0, ":num_stacks"),
		(party_stack_get_size, ":stack_size",":party",":i"),
		(party_stack_get_troop_id, ":stack_troop",":party",":i"),

		(store_troop_faction, ":fac_troop", ":stack_troop"),
		(eq,":fac_troop",":fac"),
		
		(call_script, "script_game_get_troop_wage", ":stack_troop",0 ),
		(assign, ":cur_wage", reg0),
		(val_mul, ":cur_wage", ":stack_size"),
						
		(val_add, ":spending", ":cur_wage"),
	(try_end),  # end of for each stack
	(assign, reg4, ":spending"),
]),

#MV: update this script to charge for player's reserves (p_player_garrison) - or not   
# script_make_player_pay_upkeep  (mtarini)
# no input, no output
("make_player_pay_upkeep",
   [(call_script, "script_update_respoint"), # make sure respoint are up-to-date (with current gold)
	(assign, ":party", "p_main_party"), # pay only for player party (no garrisons, for now)
	(party_get_num_companion_stacks, ":num_stacks",":party"),
	
	(assign, ":n_tot_unpaid_troops",  0), # for all factions
	(assign, ":tot_spending",  0), # for all factions
	(str_clear, s10 ), # list of unpaid faction

	(display_message, "@Troop upkeep:"),

	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(try_begin),
			(eq, ":fac", "fac_guldur"),
			(faction_get_slot, ":allowance",  "fac_mordor", slot_faction_respoint),
		(else_try),
			(faction_get_slot, ":allowance",  ":fac", slot_faction_respoint),
		(try_end),
		
		(assign, ":spending",  0), # for this faction
		(assign, ":n_unpaid_troops",  0), # for this faction
		
		(try_for_range_backwards, ":i", 0, ":num_stacks"),
			(party_stack_get_size, ":stack_size",":party",":i"),
			(party_stack_get_troop_id, ":stack_troop",":party",":i"),

			(store_troop_faction, ":fac_troop", ":stack_troop"),
			(eq,":fac_troop",":fac"),
			
			(call_script, "script_game_get_troop_wage", ":stack_troop",0 ),
			(assign, ":cur_wage", reg0),
			(val_mul, ":cur_wage", ":stack_size"),		
			
			# up to 50% discont, if spent time indoor
			(store_sub, ":total_payment", 8, "$g_cur_week_half_daily_wage_payments"), #between 0 and 4
			(val_mul, ":cur_wage", ":total_payment"),
		
			(val_div, ":cur_wage", 8),
		
			(try_begin), (ge,  ":allowance",":cur_wage"), 
				# CAN afford
				(val_add, ":spending", ":cur_wage"),
				(val_add, ":tot_spending", ":cur_wage"),
				(val_sub, ":allowance",":cur_wage"), 
				(troop_set_slot, ":stack_troop", slot_troop_upkeep_not_paid, 0),
			(else_try),
				# CAN'T afford
				(val_add, ":n_unpaid_troops", ":stack_size"),
				(troop_set_slot, ":stack_troop", slot_troop_upkeep_not_paid, 1),
			(try_end),
			
		(try_end),  # end of for each stack

		(try_begin),(gt,  ":n_unpaid_troops", 0 ), 
		    (assign, reg12, ":n_unpaid_troops"),
			(str_store_faction_name,s11,":fac"),
			(try_begin), (gt, ":n_tot_unpaid_troops", 0),  #  not first time
				(str_store_string, s10, "@{s11} and {s10}"), 
				(str_store_string, s12, "@their"), 
			(else_try),
				(str_store_string, s10, "@{s11}"),
				(str_store_string, s12, "@its"), 
			(try_end),
			(assign, ":n_unpaid_troops", ":stack_size" ), # for this faction
		(try_end),
		
		(val_add, ":n_tot_unpaid_troops", ":n_unpaid_troops"),
		
		(gt,  ":spending", 0),
		(store_mul, reg10, ":spending", -1),
		(call_script, "script_add_faction_rps", ":fac", reg10),
	(try_end),  # end of for each faction

	(try_begin),(eq,  ":tot_spending", 0 ),(eq,  ":n_tot_unpaid_troops", 0 ), 
		(display_message, "@[no upkeep costs]"),
	(try_end),
	(try_begin),(gt, ":n_tot_unpaid_troops", 0),
		(display_message, "@Short of Resource Points!!", color_bad_news),
		(display_message, "@{s10} will soon reassign some of {s12} troops away from your party!", color_bad_news),
	(try_end),
	(assign, "$g_cur_week_half_daily_wage_payments", 0), # reset "rest in city" discount
]),

# script_make_unpaid_troop_go  (mtarini)
#  No input, no output. Just makes the "unpaid" troops of player party leave the party, if you still don't have the money
("make_unpaid_troop_go",[
	(call_script, "script_update_respoint"), # make sure respoint are up-to-date (with current gold)
	(assign, ":party", "p_main_party"), 
	(party_get_num_companion_stacks, ":num_stacks",":party"),
	
	(assign, ":tot_spending",  0), # for all factions
	(str_clear, s12 ), # list of unpaid faction

	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(faction_get_slot, ":allowance",  ":fac", slot_faction_respoint),
		(assign, ":spending",  0), # for this faction
		#(assign, ":n_tot_left",  0), # for this factions
		(assign,  ":msg_shown", 0),
		(try_for_range_backwards, ":i", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop",":party",":i"),  
			(ge, ":stack_troop", 0),
			(troop_slot_eq, ":stack_troop", slot_troop_upkeep_not_paid, 1), # the upkeep of these guys wasn't paid
			(store_troop_faction, ":fac_troop", ":stack_troop"),(eq,":fac_troop",":fac"),  # and they are of the right faction
			(troop_set_slot, ":stack_troop", slot_troop_upkeep_not_paid, 0),

			(party_stack_get_size, ":stack_size",":party",":i"),
			(party_stack_get_num_wounded, ":stack_wounded",":party",":i"),
			

			(call_script, "script_game_get_troop_wage", ":stack_troop",0 ), (assign, ":wage", reg0),
			(call_script, "script_get_troop_disband_cost", ":stack_troop",1 ,0 ), (assign, ":gain_ok", reg0),
			(call_script, "script_get_troop_disband_cost", ":stack_troop",2 ,0 ), (assign, ":gain_ko", reg0),

			# up to 50% discount, if spent time indoor
			(store_sub, ":total_payment", 8, "$g_cur_week_half_daily_wage_payments"), #between 0 and 4
			(val_mul, ":wage", ":total_payment"),
			(val_div, ":wage", 8),
			
			(assign, ":n_left",  0), # for his stack

			(try_for_range, ":unused", 0, ":stack_size"), # for each troop in stack
			
				(try_begin), (ge,  ":allowance",":wage"), # CAN afford: stays. Pay wage
					(val_add, ":spending", ":wage"),
					(val_add, ":tot_spending", ":wage"),
					(val_sub, ":allowance",":wage"), 
				(else_try),   # CAN'T afford: leaves. Gain premium.
					(assign, ":gain", ":gain_ok"),
					(try_begin), (gt, ":stack_wounded", 0),  # if wounded, gain less money
						(val_sub, ":stack_wounded", 1),
						(assign, ":gain", ":gain_ko"),
					(try_end),
					(val_sub, ":spending", ":gain"),  # gain RP
					(val_sub, ":tot_spending", ":gain"), # gain RP
					(val_add, ":allowance",":gain"), # gain RP
					(val_add, ":n_left",  1), 
					#(val_add, ":n_tot_left",  1), 
				(try_end),
			(try_end), # end of a stack
			
			(gt, ":n_left", 0),
			(try_begin),(eq, ":msg_shown", 0),
				(str_store_faction_name,s11,":fac"),
				(display_message, "@Superior orders from {s11} to reassign troops:", color_bad_news),
				(assign,  ":msg_shown", 1), # only once
			(try_end),
			
			(str_store_troop_name_by_count,s10,":stack_troop", ":n_left"),
			(assign, reg12, ":n_left"),
			
			(display_message, "@{reg12} {s10} left the party!", color_bad_news),
			(party_remove_members, ":party", ":stack_troop", ":n_left"),
		(try_end),  # end of for all stacks
		
		(neq,  ":spending", 0),
		(store_mul, reg10, ":spending", -1),
		(call_script, "script_add_faction_rps", ":fac", reg10),
	(try_end),  # end of for each faction
]),
	
#############################  TLD PLAYER REWARD SYSTEM --- SCRIPTS  END  (mtarini)  #############################?#

### given two factions, fails if they are not allies...
("cf_factions_are_allies", [
	(store_script_param_1, ":a"),
	(store_script_param_2, ":b"),
	(faction_get_slot, ":a",":a", slot_faction_side),
	(faction_get_slot, ":b",":b", slot_faction_side),
	(try_begin), # eye and hand still allies?
		(le, "$tld_war_began",1),
		(try_begin), 
			(eq,":a", faction_side_hand),(assign,":a",faction_side_eye),
		(try_end),
		(try_begin), 
			(eq,":b", faction_side_hand),(assign,":b",faction_side_eye),
		(try_end),
	(try_end),
    (eq,":a",":b"),
]),
	 
# script_get_entry_point_with_most_similar_facing (mtarini)
# used to make warg spawn from an entry point which will give it an appropriate facing
# stores in reg1 the entry point  (in 0..64) with a facting more similar to 1st param 
("get_entry_point_with_most_similar_facing", 
 [  (store_script_param_1, ":target"),
	(store_add, ":target2", ":target", 360),
	(try_begin),
		(ge,":target", 180), (store_add, ":target2", ":target", -360),
	(try_end),
	
	(assign, reg1, 5),
	(assign, ":best", 9999),
	(try_for_range, ":i", 5, 9), # avoid 0..4
		(entry_point_get_position,pos10,":i"),
		(position_get_rotation_around_z, reg10, pos10),
		#(try_begin),(assign,reg5,":i"),(le,reg5,20),(display_message, "@Pos N.{reg5}:{reg10}"),(try_end),
		(neq,reg10,0.0), # skip undefined positions
		# find min distance from target2, target (store in reg12)
		(store_sub, reg11, reg10, ":target2"),(val_abs, reg11),
		(store_sub, reg12, reg10, ":target"), (val_abs, reg12),
		(val_min, reg12,reg11),
		(lt, reg12, ":best"), 
		(assign, ":best", reg12),
		(assign, reg1, ":i"),
	(try_end),
	#(set_show_messages,1),
	#(display_message, "@Selected:{reg1}"),
]),


# 
("cf_troop_cant_ride_item", [

	(store_script_param_1, ":trp"),
	(store_script_param_2, ":mount_item"),
    (troop_get_type, ":race", ":trp"),
	
	
	(assign, ":mount_type", 0), # 0 = horse   1 = warg, 2 = huge warg  3 = pony
	(try_begin),(eq,":mount_item", "itm_warg_reward"),                      (assign, ":mount_type", 2),
	 (else_try),(is_between, ":mount_item", item_warg_begin, item_warg_end),(assign, ":mount_type", 1),
	 (else_try),(eq, ":mount_item", "itm_spider"),                          (assign, ":mount_type", 1), # Only orcs can ride spiders 
	 (else_try),(eq, ":mount_item", "itm_pony"),                            (assign, ":mount_type", 3),
	(try_end),

	(assign, ":rider_type", 0), # 0 = human   1 = orc,   2 = uruk      3 = dwarf
	(try_begin),(eq, ":race", tf_orc),                          (assign, ":rider_type" , 1), # non-orcs (uruks & hai included) cannot ride ordinary wargs
	 (else_try),(is_between, ":race", tf_orc_begin, tf_orc_end),(assign, ":rider_type" , 2),
	 (else_try),(eq, ":race", tf_dwarf),                        (assign, ":rider_type" , 3),
	(try_end),
	
	#(assign, reg10,":rider_type"),(assign, reg12,":mount_item"),(assign, reg11,":mount_type"), (display_message, "@cazz {reg10} {reg11} (itm: {reg12})"),
	
	(neq, ":mount_type", ":rider_type"), # non orc riding wargs, or orc riding non wargs
]),

#script_cf_is_troop_in_party_wounded 
#is a regular troop wounded inside a party?  (mtarini)
# INPUT: arg1 = faction_no, arg2 = owner_troop_no
#OUTPUT: nothing (can fail)
("cf_is_troop_in_party_wounded",
    [ (store_script_param, ":troop", 1),
      (store_script_param, ":party", 2),
	  (assign, ":yes", 0), 
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
        (eq, ":stack_troop", ":troop"),
		(party_stack_get_num_wounded,":nw",":party",":i_stack"),
		(gt, ":nw", 1), # if there are wounded
        (assign, ":yes", 1), # then yes
      (try_end),
	  (eq, ":yes", 1), # fails if not wounded
]),

#script_cf_is_troop_in_party_not_wounded 
# as above, but the opposite
("cf_is_troop_in_party_not_wounded",[
      (store_script_param, ":troop", 1),
      (store_script_param, ":party", 2),
	  (assign, ":yes", 0), 
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
        (eq, ":stack_troop", ":troop"),
		(party_stack_get_num_wounded,":nw",":party",":i_stack"),
		(gt, ":nw", 1), # if there are wounded
        (assign, ":yes", 1), # then yes
      (try_end),
	  (eq, ":yes", 0), # fails if not wounded   ]),
]),  

#############################  TLD FANGORN SCRIPTS   (mtarini)  #############################?#
#script_fangorn_deal_damage
# script: deal 'fangorn damage' to a party (abstact attack by ents):  (mtarini)
#  INPUT: party to deal damage
#  OUTPUT: reg0 killed troops. reg1 = wonded troops. reg2 = wounded player (1 or 0)
("fangorn_deal_damage", 
  [(store_script_param_1, ":party"),
   (assign,":killed",0),
   (assign,":wounded",0),
   (assign,":leader_wounded",0),
   (try_begin),
     (store_random_in_range, reg0,0,100),
     (lt, reg0, "$g_fangorn_rope_pulled"), # if fangorn rope is not pulled enough, get away with this 
     (party_get_num_companion_stacks, ":num_stacks",":party"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),

         (party_stack_get_troop_id, ":stack_troop",":party",":i_stack"),
         (party_stack_get_size, ":stack_size",":party",":i_stack"),

         (assign, reg0, ":stack_size"),
          #(display_message,"@DEBUG: processing a stack of {reg0} troops"),

         (try_for_range, ":i",0,":stack_size"),
          (store_random_in_range, reg0,0,5), (eq, reg0, 2),  # kill 1 in 5
           (try_begin),
             (store_random_in_range, reg0,0,2), (this_or_next|eq, reg0, 0),  # wound 1 in 2 just wounded (and all heros)
             (troop_is_hero,":stack_troop"),
             (neg|troop_is_wounded,":stack_troop"),
             # wound
             (party_wound_members,":party",":stack_troop",1),
             (try_begin),
                (troop_is_hero,":stack_troop"),
                (troop_set_health,":stack_troop",0), # heroes  (including player) gets 0 health
             (try_end),
             (try_begin),
                (eq, ":i",0),
                (val_add,":leader_wounded",1),
             (else_try),
                (val_add,":wounded",1),
             (try_end),
           (else_try), #kill
             (neg|troop_is_hero,":stack_troop"), #MV
             (party_remove_members,":party",":stack_troop",1),
             (val_add,":killed",reg0),
           (try_end),
         (try_end),         
     (try_end),
   (try_end),
   (assign, reg0, ":killed"),
   (assign, reg1, ":wounded"),
   (assign, reg2, ":leader_wounded"),
]),

#script_after_fangorn_damage_to_player 
# script: after_fangorn_damage_to_player:  (mtarini)
("after_fangorn_damage_to_player",
   [ (try_begin),
       (this_or_next|gt,reg0,0),
       (gt,reg1,0),
       (display_message,"@Fangorn claimed {reg0} killed and {reg1} wounded among your troops!", color_bad_news),
     (try_end),
     (try_begin),
       (eq,reg2,1),
       (display_message,"@You were wounded in Fangorn!", color_bad_news),
     (try_end),
   
     (assign, ":player_victim", reg2),
     (store_add, ":troop_victims", reg1,reg0), # killed + wounded victims
     
     (try_begin),  
       (eq, ":player_victim",  1),
       (eq, ":troop_victims", 0), 
       (jump_to_menu, "mnu_fangorn_killed_player_only"),
     (else_try),
       (eq, ":player_victim",  0),
       (gt, ":troop_victims", 0), 
       (jump_to_menu, "mnu_fangorn_killed_troop_only"),
     (else_try),
       (eq, ":player_victim",  1),
       (gt, ":troop_victims", 0), 
       (jump_to_menu, "mnu_fangorn_killed_troop_and_player"),
     (else_try),
       (change_screen_map), # no victims at all
     (try_end),
]),

#script_party_is_in_fangorn
# Script: is this party curretnly inside fangorn?   (mtarini)
#    INPUT: party to test
#    OUTPUT: reg0  = 1 if yes
("party_is_in_fangorn",
   [(set_fixed_point_multiplier, 100),
    (store_script_param_1, ":party"),
    (party_get_position, pos1, ":party"),
    (party_get_position, pos2, "p_fangorn_center"),
    (get_distance_between_positions, ":dist", pos1, pos2),
    (party_get_current_terrain, ":terrain_type", ":party"),
# (assign, reg0, ":dist"),
# (assign, reg1, ":terrain_type"),
# (display_message,"@Distance from Fangorn: {reg0}, terrain: {reg1}"),
    (try_begin),
      (lt, ":dist", 2400), #MV: was 3200
      (this_or_next|eq, ":terrain_type", rt_steppe_forest),
      (this_or_next|eq, ":terrain_type", rt_forest),
      (eq, ":terrain_type", rt_snow_forest),
      (assign, reg0, 1),
    (else_try),
      (assign, reg0, 0),
    (try_end),
]),

#script_fangorn_fight_ents
# Script: start a battle with wandering ents  (mtarini)
("fangorn_fight_ents",[
	#(assign, ":ent_troop", "trp_ent"), # should be ents!
	(jump_to_scene, "scn_random_scene_plain_forest"),
	#(call_script, "script_setup_random_scene"),
	(set_jump_mission,"mt_fangorn_battle"),
	(modify_visitors_at_site, "scn_random_scene_plain_forest"),
	(reset_visitors),
	(set_party_battle_mode),
	#(store_random_in_range,":n_ents1",1,5),
	#(store_random_in_range,":n_ents2",1,5),
	#(store_add,":n_ents",":n_ents1",":n_ents2"), # 2d5 ents!  
	#(set_visitor, 3, ":ent_troop"),
	#(set_visitor, 2, ":ent_troop"),
	#(set_visitors, 3, ":ent_troop", ":n_ents2"),
	#(set_visitors, 16, ":ent_troop", ":n_ents2"),
	#(set_visitors, 17, ":ent_troop", ":n_ents2"),
	#(set_visitors, 0, ":ent_troop", ":n_ents2"),
	#(set_visitors, 1, ":ent_troop", ":n_ents2"),
	#(set_visitors, 2, "trp_farmer", "$qst_eliminate_bandits_infesting_village_num_villagers"),
	(set_battle_advantage, 0),
	(assign, "$g_battle_result", 0),
	#(set_jump_mission,"mt_fangorn_battle"),
	#(display_message,"@You lead the exploration inside Fangorn forest..."),
	(assign, "$g_next_menu", "mnu_fangorn_battle_debrief"),        
	(jump_to_menu, "mnu_battle_debrief"),
	(assign, "$g_mt_mode", vba_normal),
	(assign, "$cant_leave_encounter", 1),
	(change_screen_mission),
]),
#############################  TLD FANGORN SCRIPTS  END ##############################

##############################  GAME START MEGASCRIPT  ###############################

#script_game_start:
# This script is called when a new game is started
# INPUT: none
("game_start",[
	(faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
	(troop_set_slot, "trp_player", slot_troop_occupation, slto_kingdom_hero),
	(troop_set_slot, "trp_player", slot_troop_prisoner_of_party, -1),
	(try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
		(troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, -1),
		(troop_set_slot, ":cur_troop", slot_troop_custom_banner_flag_type, -1),
		(troop_set_slot, ":cur_troop", slot_troop_custom_banner_map_flag_type, -1),
	(try_end),
	(troop_set_slot, "trp_player", slot_troop_custom_banner_flag_type, -1),
	(troop_set_slot, "trp_player", slot_troop_custom_banner_map_flag_type, -1),
	#Assigning global constant
	(call_script, "script_store_average_center_value_per_faction"),

	(troop_set_slot, "trp_player", slot_troop_custom_banner_bg_color_1, 0xFFFFFFFF),
	(troop_set_slot, "trp_player", slot_troop_custom_banner_bg_color_2, 0xFFFFFFFF),
	(troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_1, 0xFFFFFFFF),
	(troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_2, 0xFFFFFFFF),
	(troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_3, 0xFFFFFFFF),
	(troop_set_slot, "trp_player", slot_troop_custom_banner_charge_color_4, 0xFFFFFFFF),

	(faction_set_slot, "fac_outlaws", slot_faction_side  , faction_side_noside),
	(faction_set_slot, "fac_deserters", slot_faction_side  , faction_side_noside),
	(faction_set_slot, "fac_mountain_bandits", slot_faction_side  , faction_side_noside),
	(faction_set_slot, "fac_forest_bandits", slot_faction_side  , faction_side_noside),
	(faction_set_slot, "fac_commoners", slot_faction_side  , faction_side_good),

	#Setting background colors for banners
	]+[ (troop_set_slot, "trp_banner_background_color_array", x,  color_list[x])  for x in range(len(color_list)) ]+[

	(str_store_troop_name, s5, "trp_player"),
	(party_set_name, "p_main_party", s5),
	(call_script, "script_update_party_creation_random_limits"),
	# Reseting player party icon
	(assign, "$g_player_party_icon", -1),
	# Setting food bonuses
	(item_set_slot, "itm_smoked_fish", slot_item_food_bonus, 5),
	(item_set_slot, "itm_dried_meat", slot_item_food_bonus, 5),
	(item_set_slot, "itm_cattle_meat", slot_item_food_bonus, 7),
	(item_set_slot, "itm_human_meat", slot_item_food_bonus, 6),
	#(item_set_slot, "itm_lembas", slot_item_food_bonus, 20),
	(item_set_slot, "itm_maggoty_bread", slot_item_food_bonus, 2),
	(item_set_slot, "itm_cram", slot_item_food_bonus, 3),

	(call_script, "script_initialize_npcs"),

	# Setting book intelligence requirements
	#(item_set_slot, "itm_book_tactics", slot_item_intelligence_requirement, 9),
	  

	]+[
	# Faction init from data in module_constants.py
	# War system (foxyman)
	(faction_set_slot, faction_init[x][0], slot_faction_strength        , faction_init[x][1])     for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_culture         , faction_init[x][2])     for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_leader          , faction_init[x][3][0])  for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_marshall        , faction_init[x][3][1])  for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_tier_1_troop    , faction_init[x][4][0])  for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_tier_2_troop    , faction_init[x][4][1])  for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_tier_3_troop    , faction_init[x][4][2])  for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_tier_4_troop    , faction_init[x][4][3])  for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_tier_5_troop    , faction_init[x][4][4])  for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_reinforcements_a, faction_init[x][5][0])  for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_reinforcements_b, faction_init[x][5][1])  for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_reinforcements_c, faction_init[x][5][2])  for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_prisoner_train  , faction_init[x][5][3])  for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_party_map_banner, faction_init[x][7])     for x in range(len(faction_init)) ]+[
	# troop slots
	(faction_set_slot, faction_init[x][0], slot_faction_deserter_troop    , faction_init[x][8][0]) for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_guard_troop       , faction_init[x][8][1]) for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_messenger_troop   , faction_init[x][8][2]) for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_prison_guard_troop, faction_init[x][8][3]) for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_castle_guard_troop, faction_init[x][8][4]) for x in range(len(faction_init)) ]+[

	(faction_set_slot, faction_init[x][0], slot_faction_capital           , faction_init[x][9])    for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_side              , faction_init[x][10])   for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_home_theater      , faction_init[x][11])   for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_init[x][0], slot_faction_advance_camp      , faction_init[x][12])   for x in range(len(faction_init)) ]+[
	# rumors in shops and tavers
	(faction_set_slot, faction_strings[x][0], slot_faction_rumors_begin   , faction_strings[x][1])    for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_strings[x][0], slot_faction_rumors_end     , faction_strings[x][2])    for x in range(len(faction_init)) ]+[
	# ambient sounds
	(faction_set_slot, faction_strings[x][0], slot_faction_ambient_sound_day   , faction_strings[x][3])    for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_strings[x][0], slot_faction_ambient_sound_always, faction_strings[x][4])    for x in range(len(faction_init)) ]+[
	(faction_set_slot, faction_strings[x][0], slot_faction_occasional_sound1_day,faction_strings[x][5])    for x in range(len(faction_init)) ]+[

	# fixed faction info      
	(try_for_range, ":faction", kingdoms_begin, kingdoms_end),
		(faction_get_slot, reg30, ":faction", slot_faction_strength),
		(faction_set_slot, ":faction", slot_faction_strength_tmp, reg30),
		(faction_get_slot, reg30, ":faction", slot_faction_home_theater),
		(faction_set_slot, ":faction", slot_faction_active_theater, reg30),
		(assign, reg30, 1),
		(try_for_range, ":unused", 0, ":faction"),
			(val_mul, reg30, 2),
		(try_end),
		(faction_set_slot, ":faction", slot_faction_mask, reg30),
	(try_end),
	(faction_set_slot, "fac_player_supporters_faction", slot_faction_marshall, "trp_player"),

	# Towns:
	(try_for_range, ":item_no", trade_goods_begin, trade_goods_end),
		(store_sub, ":offset", ":item_no", trade_goods_begin),
		(val_add, ":offset", slot_town_trade_good_prices_begin),
		(try_for_range, ":center_no", centers_begin, centers_end),
			(party_set_slot, ":center_no", ":offset", average_price_factor),
		(try_end),
	(try_end),
	
	# setting up trade and messenger routes
	]+concatenate_scripts([
	[
	(call_script, "script_set_trade_route_between_centers", routes_list[x][0], routes_list[x][y]) for y in range (len(routes_list[x]))
	] for x in range(len(routes_list))
	])+[
	(call_script, "script_center_change_trade_good_production", "p_town_minas_tirith", "itm_tools", 110, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_pelargir", "itm_smoked_fish", 130, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_linhir", "itm_tools", 120, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_dol_amroth", "itm_tools", 130, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_edhellond", "itm_tools", 80, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_lossarnach", "itm_tools", 130, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_tarnost", "itm_tools", 140, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_tarnost", "itm_smoked_fish", 110, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_erech", "itm_tools", 130, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_pinnath_gelin", "itm_tools", 135, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_aldburg", "itm_tools", 86, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_edoras", "itm_tools", 130, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_hornburg", "itm_tools", 140, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_east_emnet", "itm_dried_meat", 120, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_westfold", "itm_tools", 120, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_west_emnet", "itm_tools", 100, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_eastfold", "itm_tools", 100, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_morannon", "itm_tools", 100, 0),
	(call_script, "script_center_change_trade_good_production", "p_town_minas_morgul", "itm_tools", 125, 0),
	(try_for_range, ":unused", 0, 1),
		(call_script, "script_average_trade_good_productions"),
	(try_end),
	(call_script, "script_normalize_trade_good_productions"),

	# Centers init from data in module_constants.py
	]+[
	(party_set_slot, center_list[x][0], slot_town_center          , center_list[x][1][0]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_town_castle          , center_list[x][1][1]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_town_prison          , center_list[x][1][2]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_town_tavern          , center_list[x][1][3]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_town_arena           , center_list[x][1][4]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_town_walls           , center_list[x][1][5]) for x in range(len(center_list)) ]+[   
	(party_set_slot, center_list[x][0], slot_town_menu_background , center_list[x][1][6]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_town_elder           , center_list[x][2][3]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_town_barman          , center_list[x][2][0]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_town_weaponsmith     , center_list[x][2][1]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_town_merchant        , center_list[x][2][2]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_town_recruits_pt     , center_list[x][2][4]) for x in range(len(center_list)) ]+[
	#walker types
	(party_set_slot, center_list[x][0], slot_center_walker_0_troop, center_list[x][2][6]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_walker_1_troop, center_list[x][2][7]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_walker_2_troop, center_list[x][2][8]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_walker_3_troop, center_list[x][2][9]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_walker_4_troop, center_list[x][2][6]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_walker_5_troop, center_list[x][2][7]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_walker_6_troop, center_list[x][2][8]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_walker_7_troop, center_list[x][2][9]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_walker_8_troop, center_list[x][2][6]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_walker_9_troop, center_list[x][2][7]) for x in range(len(center_list)) ]+[
	(party_set_banner_icon,             center_list[x][0],          center_list[x][3][0]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_strength_income,   center_list[x][6]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_garrison_limit,    center_list[x][7]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_destroy_on_capture,center_list[x][8]) for x in range(len(center_list)) ]+[
	(party_set_slot, center_list[x][0], slot_center_siegability,       center_list[x][9]) for x in range(len(center_list)) ]+[
	#item abundancy in center shops
	(troop_set_slot, center_list[x][2][1], slot_troop_shop_gold    ,center_list[x][4][0]) for x in range(len(center_list)) ]+[
	(troop_set_slot, center_list[x][2][2], slot_troop_shop_gold    ,center_list[x][4][0]) for x in range(len(center_list)) ]+[
	#battlegear and horses numbers stored in merchant troop skills
	(troop_set_slot, "trp_skill2item_type", x ,skill2item_list[x]) for x in range(len(skill2item_list)) ]+[

	# give centers to lords, put said lord there
	(call_script, "script_give_center_to_lord", center_list[x][0], center_list[x][2][5], 0) for x in range(len(center_list)) ]+[ 
	# center fixed info filling
	(try_for_range, ":town_no", centers_begin, centers_end),
		(party_set_slot, ":town_no", slot_party_type, spt_town),
		(try_begin),
			(party_slot_eq, ":town_no", slot_town_walls, -1),
			(party_get_slot, reg30, ":town_no", slot_town_center),
			(party_set_slot, ":town_no", slot_town_walls, reg30),
		(try_end),
		(party_set_slot, ":town_no", slot_town_store, "scn_town_store"),
		(party_set_slot, ":town_no", slot_town_alley, "scn_town_alley"),
	(try_end),

	# Centers spawns init from ws_party_spawns_list in module_constants.py      
	]+[
	(party_set_slot, ws_party_spawns_list[x][0], slot_center_spawn_scouts,  ws_party_spawns_list[x][1]) for x in range(len(ws_party_spawns_list)) ]+[
	(party_set_slot, ws_party_spawns_list[x][0], slot_center_spawn_raiders, ws_party_spawns_list[x][2]) for x in range(len(ws_party_spawns_list)) ]+[
	(party_set_slot, ws_party_spawns_list[x][0], slot_center_spawn_patrol,  ws_party_spawns_list[x][3]) for x in range(len(ws_party_spawns_list)) ]+[
	(party_set_slot, ws_party_spawns_list[x][0], slot_center_spawn_caravan, ws_party_spawns_list[x][4]) for x in range(len(ws_party_spawns_list)) ]+[
	# disable some evil centers at start
	]+[   (disable_party, centers_disabled_at_start[x]) for x in range(len(centers_disabled_at_start)) ]+[
	# make henneth hardly visible when player is evil
	(try_begin),
		(neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
		(party_set_flags, "p_town_henneth_annun", pf_always_visible, 0),
	(try_end),
	(try_for_range, ":center_no", centers_begin, centers_end),
		(party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
		(party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
		(party_set_slot, ":center_no", slot_center_last_taken_by_troop, -1),
		#Assigning random prosperity
		(store_random_in_range, ":random_prosperity_adder", -25, 15),
		(call_script, "script_get_center_ideal_prosperity", ":center_no"),
		(assign, ":prosperity", reg0),
		(val_add, ":prosperity", ":random_prosperity_adder"),
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(val_add, ":prosperity", 20),
		(try_end),
		(val_clamp, ":prosperity", 0, 100),
		(party_set_slot, ":center_no", slot_town_prosperity, ":prosperity"),
	(try_end),
	  
	(try_for_range, ":town_no", centers_begin, centers_end),
		(store_faction_of_party, ":faction", ":town_no"),
		(faction_get_slot, ":tmp",":faction", slot_faction_reinforcements_a),
		(party_set_slot, ":town_no", slot_town_reinforcements_a, ":tmp"),
		(faction_get_slot, ":tmp",":faction", slot_faction_reinforcements_b),
		(party_set_slot, ":town_no", slot_town_reinforcements_b, ":tmp"),
		(faction_get_slot, ":tmp",":faction", slot_faction_reinforcements_c),
		(party_set_slot, ":town_no", slot_town_reinforcements_c, ":tmp"),
	# set center theater according to faction theater - never changes except for advance camps
		(faction_get_slot, ":tmp", ":faction", slot_faction_home_theater),
		(party_set_slot, ":town_no", slot_center_theater, ":tmp"),
	# victory points value on capture/destruction
		(party_set_slot, ":town_no", slot_party_victory_value, ws_center_vp),
	# ambient sounds for centers from faction defaults
		(faction_get_slot, ":tmp", ":faction", slot_faction_ambient_sound_day),
		(party_set_slot, ":town_no", slot_center_ambient_sound_day, ":tmp"),
		(faction_get_slot, ":tmp", ":faction", slot_faction_ambient_sound_always),
		(party_set_slot, ":town_no", slot_center_ambient_sound_always, ":tmp"),
		(faction_get_slot, ":tmp", ":faction", slot_faction_occasional_sound1_day),
		(party_set_slot, ":town_no", slot_center_occasional_sound1_day, ":tmp"),
	(try_end),
	]+[
# specific centers ambient sounds
	(party_set_slot, center_sounds[x][0], slot_center_ambient_sound_day   , center_sounds[x][1])  for x in range(len(center_sounds)) ]+[
	(party_set_slot, center_sounds[x][0], slot_center_ambient_sound_always, center_sounds[x][2])  for x in range(len(center_sounds)) ]+[
	(party_set_slot, center_sounds[x][0], slot_center_occasional_sound1_day,center_sounds[x][3])  for x in range(len(center_sounds)) ]+[

	(party_set_slot, subfaction_data[x][1], slot_town_reinforcements_a, subfaction_data[x][4][0])  for x in range(len(subfaction_data)) ]+[
	(party_set_slot, subfaction_data[x][1], slot_town_reinforcements_b, subfaction_data[x][4][1])  for x in range(len(subfaction_data)) ]+[
	(party_set_slot, subfaction_data[x][1], slot_town_reinforcements_c, subfaction_data[x][4][2])  for x in range(len(subfaction_data)) ]+[

	(party_add_members, subfaction_data[x][1], subfaction_data[x][5][y],1)  for x in range(len(subfaction_data)) for y in range(len(subfaction_data[x][5])) ]+[

#Initialize walkers
	(try_for_range, ":center_no", centers_begin, centers_end),
		(party_slot_eq, ":center_no", slot_party_type, spt_town),
		(try_for_range, ":walker_no", 0, num_town_walkers),
			(call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
		(try_end),
	(try_end),
# TLD banner assignment		
# assign main faction banners to kings, then lords
    ]+[
	(troop_set_slot, faction_init[x][3][0], slot_troop_banner_scene_prop, faction_init[x][6]) for x in range(len(faction_init)) ]+[   

	(try_for_range, ":kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
		(troop_add_gold,":kingdom_hero",100000),
		(store_troop_faction, ":kingdom_hero_faction", ":kingdom_hero"),
	# other heroes get banners like lords, except Rohan & Gondor vassals (which will be overwritten later)
		(faction_get_slot,":kingdom_leader",":kingdom_hero_faction",slot_faction_leader),
		(troop_get_slot, ":banner_id", ":kingdom_leader", slot_troop_banner_scene_prop),
		(troop_set_slot, ":kingdom_hero", slot_troop_banner_scene_prop, ":banner_id"),

        (store_character_level, ":level", ":kingdom_hero"),
        (store_mul, ":renown", ":level", ":level"),
        (val_div, ":renown", 2),
        (try_begin),
			(faction_slot_eq, ":kingdom_hero_faction", slot_faction_leader, ":kingdom_hero"),
			(troop_set_slot, ":kingdom_hero", slot_troop_loyalty, 100),
			(store_random_in_range, ":random_renown", 250, 400),
        (else_try),
			(store_random_in_range, ":random_loyalty", 50, 100),
			(troop_set_slot, ":kingdom_hero", slot_troop_loyalty, ":random_loyalty"),
			(store_random_in_range, ":random_renown", 100, 200),
        (try_end),
		(val_add, ":renown", ":random_renown"),
		(troop_set_slot, ":kingdom_hero", slot_troop_renown, ":renown"),
		(store_random_in_range, ":random_readiness", 0, 100),
		(troop_set_slot, ":kingdom_hero", slot_troop_readiness_to_join_army, ":random_readiness"),
		(troop_set_slot, ":kingdom_hero", slot_troop_readiness_to_follow_orders, 100),
		(troop_set_slot, ":kingdom_hero", slot_troop_player_order_state, spai_undefined),
		(troop_set_slot, ":kingdom_hero", slot_troop_player_order_object, -1),
	(try_end),
# Rohan lord banners
	(troop_set_slot, "trp_knight_1_9", slot_troop_banner_scene_prop, "spr_banner_f01"), #westfold
	(troop_set_slot, "trp_knight_1_10", slot_troop_banner_scene_prop, "spr_banner_f05"), #westemnet
	(troop_set_slot, "trp_knight_1_11", slot_troop_banner_scene_prop, "spr_banner_f02"), #aldburg
#	(troop_set_slot, "trp_knight_1_12", slot_troop_banner_scene_prop, "spr_banner_ed"), # hama is kings man
	(troop_set_slot, "trp_knight_1_13", slot_troop_banner_scene_prop, "spr_banner_f06"), #eastfold
	(troop_set_slot, "trp_knight_1_14", slot_troop_banner_scene_prop, "spr_banner_f07"), #eastemnet
# Gondor vassals lord banners
	(troop_set_slot, "trp_knight_1_1", slot_troop_banner_scene_prop, "spr_banner_ek"), #lamedon
	(troop_set_slot, "trp_knight_1_3", slot_troop_banner_scene_prop, "spr_banner_er"), #dol amroth
	(troop_set_slot, "trp_knight_1_4", slot_troop_banner_scene_prop, "spr_banner_en"), #pelargir
	(troop_set_slot, "trp_knight_1_5", slot_troop_banner_scene_prop, "spr_banner_ed"), #blackroot vale
	(troop_set_slot, "trp_knight_1_6", slot_troop_banner_scene_prop, "spr_banner_eg"), #pinnath gelin
	(troop_set_slot, "trp_knight_1_8", slot_troop_banner_scene_prop, "spr_banner_f21"), #lossarnach

# fill center slots	
	(try_for_range, ":center_no", centers_begin, centers_end),
		(store_faction_of_party, ":original_faction", ":center_no"),
		#        (faction_get_slot, ":culture", ":original_faction", slot_faction_culture),
		#        (party_set_slot, ":center_no", slot_center_culture,  ":culture"),
		(party_set_slot, ":center_no", slot_center_original_faction,  ":original_faction"),
		(party_set_slot, ":center_no", slot_center_ex_faction,  ":original_faction"),
		# TLD center guards
		(faction_get_slot, ":troop", ":original_faction", slot_faction_guard_troop),
		(party_set_slot, ":center_no", slot_town_guard_troop,  ":troop"),
		(faction_get_slot, ":troop", ":original_faction", slot_faction_prison_guard_troop),
		(party_set_slot, ":center_no", slot_town_prison_guard_troop,  ":troop"),
		(faction_get_slot, ":troop", ":original_faction", slot_faction_castle_guard_troop),
		(party_set_slot, ":center_no", slot_town_castle_guard_troop,  ":troop"),
	(try_end),
# TLD specific center guards
	]+concatenate_scripts([[
	(party_set_slot, subfaction_data[x][1], slot_town_guard_troop          , subfaction_data[x][3][0]) ,
	(party_set_slot, subfaction_data[x][1], slot_town_prison_guard_troop   , subfaction_data[x][3][1]) ,
	(party_set_slot, subfaction_data[x][1], slot_town_castle_guard_troop   , subfaction_data[x][3][2]) ,
	(party_set_slot, subfaction_data[x][1],slot_party_subfaction    , subfaction_data[x][0]),
	(party_get_slot, ":weaponsmith",      subfaction_data[x][1]    , slot_town_weaponsmith),
	(troop_set_slot, ":weaponsmith",      slot_troop_subfaction    , subfaction_data[x][0]),
	]   for x in range(len(subfaction_data)) ])+[
	
# rohan towns subfaction assignment  (currently, for sake or geographical region identification  only)
	(party_set_slot, "p_town_east_emnet", slot_party_subfaction    , subfac_east_emnet),
	(party_set_slot, "p_town_west_emnet", slot_party_subfaction    , subfac_west_emnet),
	(party_set_slot, "p_town_eastfold", slot_party_subfaction      , subfac_eastfold),
	(party_set_slot, "p_town_westfold", slot_party_subfaction      , subfac_westfold),

	(party_set_slot, "p_town_minas_tirith", slot_town_castle_guard_troop, "trp_steward_guard"), # minas tirith exception

# set kingdom_heros status and wealth of heroes and kings
	(try_for_range, ":troop_id", kingdom_heroes_begin, kingdom_heroes_end),
		(store_troop_faction, ":faction_id", ":troop_id"),
		(is_between, ":faction_id", kingdoms_begin, kingdoms_end),
		(troop_set_slot, ":troop_id", slot_troop_original_faction, ":faction_id"),
		(troop_set_slot, ":troop_id", slot_troop_occupation, slto_kingdom_hero),
		(try_begin),
			(faction_slot_eq, ":faction_id", slot_faction_leader, ":troop_id"),
			(troop_set_slot, ":troop_id", slot_troop_wealth, 200000),
		(else_try),
			(troop_set_slot, ":troop_id", slot_troop_wealth, 60000),
		(try_end),
	(try_end),
	#add town garrisons
	(try_for_range, ":center_no", centers_begin, centers_end),
		(assign, ":initial_wealth", 20000),#Add initial center wealth
		(try_begin),
			(is_between, ":center_no", centers_begin, centers_end),
			(val_mul, ":initial_wealth", 2),
		(try_end),
		(party_set_slot, ":center_no", slot_town_wealth, ":initial_wealth"),

		(assign, ":garrison_strength", 13), 
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(assign, ":garrison_strength", 20), 
		(try_end),
		(try_begin), # TLD: capitals get more
			(store_faction_of_party, ":center_faction", ":center_no"),
			(faction_slot_eq, ":center_faction", slot_faction_capital, ":center_no"),
			(assign, ":garrison_strength", 30), 
		(try_end),
		(party_get_slot, ":garrison_limit", ":center_no", slot_center_garrison_limit),
		(try_for_range, ":unused", 0, ":garrison_strength"),
			(call_script, "script_cf_reinforce_party", ":center_no"),
			(try_begin), #TLD: don't go overboard
				(party_get_num_companions, ":garrison_size", ":center_no"),
				(le, ":garrison_limit", ":garrison_size"),
				(assign, ":garrison_strength", 0),
			(try_end),
		(try_end),

		#Fill town food stores upto 1/2 the limit
		(call_script, "script_center_get_food_store_limit", ":center_no"),
		(assign,  ":food_store_limit", reg0),
		(val_div, ":food_store_limit", 2),
		(party_set_slot, ":center_no", slot_party_food_store, ":food_store_limit"),
	(try_end),

# spawn some lords in distinct towns, TLD
    ]+[
	(call_script, "script_create_kingdom_hero_party", lords_spawn[x][0], lords_spawn[x][1]) for x in range(len(lords_spawn)) ]+[  

# spawn other specific location lords
      (try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(faction_get_slot, ":king", ":fac",  slot_faction_leader ),
		(faction_get_slot, ":marshal", ":fac",  slot_faction_marshall ),
		(faction_get_slot, ":town", ":fac",  slot_faction_capital ),
		(try_begin),(troop_slot_eq, ":king", slot_troop_leaded_party, 0),
			(str_store_troop_name, s15, ":king"),
			(str_store_party_name, s16, ":town"),
			#(display_message, "@deploying king {s15} in {s16}"),
			(call_script, "script_create_kingdom_hero_party", ":king", ":town"),
		(try_end),
		(try_begin),(troop_slot_eq, ":marshal", slot_troop_leaded_party, 0),
			(str_store_troop_name, s15, ":marshal"),
			(str_store_party_name, s16, ":town"),
			#(display_message, "@deploying marshal {s15} in {s16}"),
			(call_script, "script_create_kingdom_hero_party", ":marshal", ":town"),
		(try_end),
	  (try_end),

# spawn any other lord in random places, TLD
      (try_for_range, ":hero", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_slot_eq, ":hero", slot_troop_leaded_party, 0),
	    (store_troop_faction, ":faction", ":hero"),
        (call_script,"script_cf_select_random_town_with_faction", ":faction"),(assign,":center",reg0),
        (call_script, "script_create_kingdom_hero_party", ":hero", ":center"),
        (party_set_slot, ":center", slot_town_player_odds, 1000),  
      (try_end),
	  
      (try_for_range, ":unused", 0, 8),
        (call_script, "script_spawn_bandits"),
      (try_end),
      (set_spawn_radius, 50),
      (try_for_range, ":unused", 0, 25),
        (spawn_around_party,"p_main_party","pt_looters"),
      (try_end),

# generating notes
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_update_faction_notes", ":faction_no"),
        (store_random_in_range, ":random_no", -60, 0),
        (faction_set_slot, ":faction_no", slot_faction_ai_last_offensive_time, ":random_no"),
      (try_end),
	  (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
        (call_script, "script_update_troop_notes", ":cur_troop"),
      (try_end),
      (call_script, "script_update_troop_notes", "trp_player"),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (call_script, "script_update_center_notes", ":cur_center"),
      (try_end),
      
#MV: good lords are upstanding, Eye sadistic, Hand cunning
      (try_for_range, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
        (store_troop_faction, ":lord_faction", ":lord"),
        (try_begin),
          (faction_slot_eq, ":lord_faction", slot_faction_side, faction_side_good),
          (troop_set_slot, ":lord", slot_lord_reputation_type, lrep_upstanding),
        (else_try),
          (faction_slot_eq, ":lord_faction", slot_faction_side, faction_side_eye),
          (troop_set_slot, ":lord", slot_lord_reputation_type, lrep_debauched),
        (else_try),
          (troop_set_slot, ":lord", slot_lord_reputation_type, lrep_cunning),
        (try_end),
      (try_end),

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":faction_no"),
      (try_end),

      (call_script, "script_get_player_party_morale_values"),
      (party_set_morale, "p_main_party", reg0),

# assigning game global variables
	(assign, "$g_fangorn_rope_pulled", 0),
	#(assign, "$g_ent_seen", 0),
	(assign, "$g_ent_water_ever_drunk", 0),
	(assign, "$g_ent_water_taking_effect", 0),
	(assign, "$number_of_player_deaths", 0),      
	(assign, "$g_player_luck", 200),
	(assign, "$disable_npc_complaints", 0), #MV: back to 0
	(assign, "$tld_war_began",0),
	(assign, "$prev_day", 1),
	(assign, "$dungeons_in_scene", 0), # flag for dungeon presence in a scene
	(assign, "$found_moria_entrance", 0),
	(assign, "$current_player_region", -1),
	(assign, "$spawn_horse", 1),
	(assign, "$gate_breached", 0),# destructible gate variables
	(assign, "$gate_aggravator_agent", 0),
#    (assign, "$equip_needs_checking", 1),
	(assign, "$g_tld_conversations_done", 0),
	(assign, "$g_tld_gandalf_state", -1),
	(assign, "$g_tld_nazgul_state", -1),



   ################ 808 globals
    (assign, "$trait_captain_infantry_week", 0),
    (assign, "$trait_captain_archer_week", 0),
    (assign, "$trait_captain_cavalry_week", 0),
    (assign, "$trait_check_commands_issued", 0),
	(assign, "$trait_check_stealth_success", 0),
	(assign, "$trait_check_unarmored_berserker", 0),
	(assign, "$trait_check_battle_scarred", 0),
#	(assign, "$minas_tirith_healing", 0),
#    (assign, "$edoras_healing"      , 0),
#    (assign, "$isengard_healing"    , 0),
#    (assign, "$morannon_healing"    , 0),
	(assign, "$meta_alarm", 0),
    (assign, "$alarm_level", 0),
    (assign, "$rescue_stage", 0),
	(assign, "$active_rescue", 0),
#	(assign, "$sorcerer_quest", 0),
	(assign, "$rescue_wall_battle", 0),
	(assign, "$rescue_courtyard_scene_2", 0),
	(assign, "$rescue_stealth_scene_2", 0),
	(assign, "$wall_mounted_troop1", 0),
	#(assign, "$wall_mounted_troop2", 0),
	(assign, "$wall_mounted_troop3", 0),
	#(assign, "$wall_mounted_troop4", 0),
	(assign, "$wall_mounted_troop5", 0),
	(assign, "$wall_missile_troop1", 0),
	(assign, "$wall_missile_troop2", 0),
	(assign, "$wall_missile_troop3", 0),
	(assign, "$wall_missile_troop4", 0),
	(assign, "$wall_missile_troop5", 0),  
	(assign, "$rescue_convo_troop", 0),  	

   #initialize game option defaults (see camp menu)
	(assign, "$tld_option_crossdressing", 0), # item restrictions ON by default
	(assign, "$tld_option_formations", 1),# ON by default
	(assign, "$tld_option_town_menu_hidden", 1), #town features hidden by default
	(assign, "$tld_option_injuries", 1), #injuries for npcs and player ON by default
	(assign, "$tld_option_death_npc", 1), #permanent death for npcs ON by default
	(assign, "$tld_option_death_player", 0), #permanent death for player OFF by default
	(assign, "$tld_option_cutscenes", 1),# ON by default
	(assign, "$tld_option_morale", 1), # Battle morale ON by default
	(assign, "$wound_setting", 12), # rnd, 0-3 result in wounds
	(assign, "$healing_setting", 7), # rnd, 0-3 result in wounds
	
	(assign, "$initial_party_value", 0),   
	(assign, "$player_side_faction", 0),
	(assign, "$enemy_side_faction", 0),
	(assign, "$inital_player_xp", 0),
	# savegame compartibillity globals. USE THOSE in code if need be
	# Feel free to rename them... BUT if so rename then in variables.txt BEFORE you compile your code!!!
	(assign, "$g_fac_str_siegable", fac_str_weak), #when can you siege a faction, increases with player level
	#(assign, "$battle_renown_total", 0),
	(assign, "$g_variable7", 0), (assign, reg0, "$g_variable7"), #MV: to get rid of build warnings - remove on use
	(assign, "$g_defiled_armor_item", "itm_defiled_armor_gondor"), 
	(assign, "$g_defiled_armor_rotation", 0), 
    #these are used for strategic options/tweaks
	(assign, "$tld_option_siege_reqs", 0), #0,1,2 : Siege strength requirements: Normal/Halved/None
	(assign, "$tld_option_siege_relax_rate", 100), #50/100/200 : Siege str. req. relaxation rate
	(assign, "$tld_option_regen_rate", 0), #0,1,2,3 : Str. regen rate: Normal/Halved/Battles only/None
	(assign, "$tld_option_regen_limit", 500), #500/1000/1500 : Factions don't regen below
	(assign, "$tld_option_max_parties", 850), #300/350/400/450...900 : Parties don't spawn after this many parties are on map.
						  # 
]),    

# script_refresh_volunteers_in_town (mtarini and others)
("refresh_volunteers_in_town",[
   (store_script_param_1, ":town"),
   (party_get_slot, ":volunteers", ":town", slot_town_volunteer_pt),
   (try_begin),
	(store_faction_of_party, ":fac", ":town"), # friendly towns only
	(store_relation, ":rel", ":fac", "$players_kingdom"), #MV fixed
 	(ge, ":rel", 0),

	(try_begin),
		(gt, ":volunteers", 0),
		(neg|party_is_active, ":volunteers"), # depleted
		(assign, ":volunteers", 0),
	(try_end),
	(try_begin),
		(eq, ":volunteers", 0),
		(spawn_around_party, ":town", "pt_none"),
		(assign, ":volunteers", reg0),
		(party_attach_to_party, ":volunteers", ":town"),
		(party_set_slot, ":town", slot_town_volunteer_pt, ":volunteers"),
		(party_set_name, ":volunteers", "@Volunteers"), # was "@_+_"
		(party_set_flags, ":volunteers", pf_no_label),
		(party_set_ai_behavior, ":volunteers", ai_bhvr_hold),
	(try_end),
	
	# compute ideal number of volunteers
	(store_party_size_wo_prisoners, ":to_add", ":town"),
    (val_div, ":to_add", 20), #   base: [num-garrison] / 20
    (call_script, "script_get_faction_rank", ":fac"),
    (assign, ":rank", reg0),
    (val_add, ":to_add", ":rank"), #  + rank
	(store_skill_level, ":lead_bonus", "skl_leadership", "trp_player"),
    (val_div, ":lead_bonus", 2),
    (val_add, ":to_add", ":lead_bonus"),   # +leadership / 2
    # orc bonus
    (assign, ":is_orc_faction", 0),
    (try_begin),
      (this_or_next|eq, ":fac", "fac_mordor"),
      (this_or_next|eq, ":fac", "fac_isengard"),
      (this_or_next|eq, ":fac", "fac_moria"),
      (this_or_next|eq, ":fac", "fac_guldur"),
      (eq, ":fac", "fac_gundabad"),
      (assign, ":is_orc_faction", 1),
      (val_mul, ":to_add", 120), (val_div, ":to_add", 100), #+20% for orc factions
	(try_end),
    # town relations bonus +size*rel/100
    (party_get_slot, ":center_relation", ":town", slot_center_player_relation),
    (val_add, ":center_relation", 100),
    (val_mul, ":to_add", ":center_relation"), (val_div, ":to_add", 100),
    
    (assign, ":ideal_size", ":to_add"),
	
	# compute how many soldiers to add to volunteers
	(store_party_size, ":vol_total", ":volunteers"),
	(val_sub, ":to_add", ":vol_total"), # how many troops to add/remove to volunteers (in theory)
	(val_mul, ":to_add", 2), (val_div, ":to_add", 3), # fill 2/3 of the gap per time
	(store_random_in_range, ":rand", 0, 5), (val_add, ":rand", -2), (val_add, ":to_add", ":rand"), # plus random -2 .. +2
    (store_add, ":target_size", ":vol_total", ":to_add"),

    (party_get_slot, ":recruit_template", ":town", slot_town_recruits_pt),
	(try_begin),
		(gt, ":to_add", 0), # add volunteers!
        # this is to simulate slower growth for smaller templates (e.g. rangers)
        (store_div, ":reinf_rounds", ":to_add", 3), #average troops per template is 3-4; need minimum of 3 to actually reinforce
		(try_for_range, ":unused", 0, ":reinf_rounds"),
            (try_begin),
              (store_party_size, ":current_size", ":volunteers"),
              (le, ":target_size", ":current_size"),
              (assign, ":reinf_rounds", 0), #stop reinforcing if already too many
            (else_try),
              (party_add_template, ":volunteers", ":recruit_template"),
            (try_end),

            #old code using garrison troops
			# # select three potential volunteers
			# (call_script, "script_cf_party_select_random_regular_troop", ":town"),(assign,":vol0", reg0),  # can fail
			# (call_script, "script_cf_party_select_random_regular_troop", ":town"),(assign,":vol1", reg0),  # can fail
			# (call_script, "script_cf_party_select_random_regular_troop", ":town"),(assign,":vol2", reg0),  # can fail
			# # select lower in grade
			# (store_character_level, ":lvl0", ":vol0"),
			# (store_character_level, ":lvl1", ":vol1"),
			# (store_character_level, ":lvl2", ":vol2"),
			# (try_begin), (lt, ":lvl1",":lvl0"), (assign,":vol0",":vol1"),(assign,":lvl0",":lvl1"),  (try_end),
			# (try_begin), (store_random_in_range, ":tmp", 1,101), (le, ":tmp", 66),
			   # (lt, ":lvl2",":lvl0"), (assign,":vol0",":vol2"),(try_end), 
			# # move the guy from garrison to volunteers
			# (party_remove_members_wounded_first, ":town", ":vol0", 1),
			# (party_add_members, ":volunteers", ":vol0", 1),
		(try_end),
        (store_party_size, ":vol_total", ":volunteers"), # recompute for the benefit of puny orcs below
	(else_try),
		(lt, ":to_add", 0), # remove volunteers! #MV: kept this code, effect: a trickle of player recruits joins the garrison
		(val_mul, ":to_add", -1),
		(try_for_range, ":unused", 0, ":to_add"),
			(call_script, "script_cf_party_select_random_regular_troop", ":volunteers"), (assign, ":guy", reg0),  # can fail
			(party_remove_members_wounded_first, ":volunteers", ":guy", 1),
			(party_add_members, ":town", ":guy", 1),
		(try_end),
	(try_end),
    
    # add a couple of orc volunteers each day
    (try_begin),
      (eq, ":is_orc_faction", 1),
      (gt, ":ideal_size", ":vol_total"), #only if needed
      (faction_get_slot, ":puny_orc", ":fac", slot_faction_tier_1_troop),
      (gt, ":puny_orc", 0),
      (party_add_members, ":volunteers", ":puny_orc", 2),
	(try_end),
   (try_end),
]),

# script_game_event_party_encounter:
# This script is called from the game engine whenever player party encounters another party or a battle on the world map
# INPUT:
# param1: encountered_party
# param2: second encountered_party (if this was a battle
("game_event_party_encounter", [

	(store_script_param_1, "$g_encountered_party"),
	(store_script_param_2, "$g_encountered_party_2"),# encountered_party2 is set when we come across a battle or siege, otherwise it's a negative value

	(party_get_current_terrain, "$current_player_terrain","p_main_party"),
	(call_script, "script_get_region_of_party","p_main_party"),(assign, "$current_player_region", reg1),
	(call_script, "script_get_close_landmark","p_main_party"), (assign, "$current_player_landmark", reg0),


	# if camping very close to a town, enter town instead...
	(try_begin),
		(eq, "$g_encountered_party", "p_camp_bandits"   ),
		(lt, "$g_encountered_party_2", 0  ),
	    (is_between, "$current_player_landmark", centers_begin, centers_end),
	  	(store_distance_to_party_from_party, ":party_distance", "p_main_party", "$current_player_landmark"),
	  	(lt, ":party_distance", 1),
	    (assign, "$g_encountered_party", "$current_player_landmark" ),
	(try_end),	
	
	#(str_store_party_name, s15, "$g_encountered_party"),(display_message, "@event_party_encounter: {s15}"),
	(call_script, "script_player_meets_party","$g_encountered_party"),  # to set resource points (mtarini)
	#(store_encountered_party, "$g_encountered_party"),
	#(store_encountered_party2,"$g_encountered_party_2"), # encountered_party2 is set when we come across a battle or siege, otherwise it's a minus value
	(store_faction_of_party, "$g_encountered_party_faction","$g_encountered_party"),
	(store_relation, "$g_encountered_party_relation", "$g_encountered_party_faction", "fac_player_faction"),
	(party_get_slot, "$g_encountered_party_type", "$g_encountered_party", slot_party_type),
	(party_get_template_id,"$g_encountered_party_template","$g_encountered_party"),
	#(try_begin),
	#	(gt, "$g_encountered_party_2", 0),
	#	(store_faction_of_party, "$g_encountered_party_2_faction","$g_encountered_party_2"),
	#	(store_relation, "$g_encountered_party_2_relation", "$g_encountered_party_2_faction", "fac_player_faction"),
	#	(party_get_template_id,"$g_encountered_party_2_template","$g_encountered_party_2"),
	#(else_try),
	#	(assign, "$g_encountered_party_2_faction",-1),
	#	(assign, "$g_encountered_party_2_relation", 0),
	#	(assign,"$g_encountered_party_2_template", -1),
	#(try_end),

#NPC companion changes begin
	(call_script, "script_party_count_fit_regulars", "p_main_party"),
	(assign, "$playerparty_prebattle_regulars", reg0),
	(assign, "$g_last_rest_center", -1),
	(assign, "$talk_context", 0),
	(assign,"$g_player_surrenders",0),
	(assign,"$g_enemy_surrenders",0),
	(assign, "$g_leave_encounter",0),
	(assign, "$g_engaged_enemy", 0),

	(try_begin),
		(neg|is_between, "$g_encountered_party", centers_begin, centers_end),
		(rest_for_hours, 0), #stop waiting
	(try_end),

	(assign, "$new_encounter", 1), #check this in the menu.
	(assign, "$prebattle_talk_done",0), #check this in the menu.
	(try_begin),
		(lt, "$g_encountered_party_2",0), #Normal encounter. Not battle or siege.
		(try_begin),(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town ),
				    (party_slot_eq, "$g_encountered_party", slot_center_destroyed, 0), (jump_to_menu, "mnu_castle_outside"),
		 (else_try),(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
				    (party_slot_eq, "$g_encountered_party", slot_center_destroyed, 1),	(jump_to_menu, "mnu_town_ruins"),
         (else_try),(party_slot_eq, "$g_encountered_party", slot_party_type, spt_cattle_herd),(jump_to_menu, "mnu_cattle_herd"), #MV: DON'T REMOVE
		 (else_try),(eq, "$g_encountered_party", "p_test_scene"     ),(jump_to_menu, "mnu_test_scene"),
		 (else_try),(eq, "$g_encountered_party", "p_battlefields"   ),(jump_to_menu, "mnu_battlefields"),
		#(else_try),(eq, "$g_encountered_party", "p_training_ground"),(jump_to_menu, "mnu_tutorial"),
		 (else_try),(eq, "$g_encountered_party", "p_camp_bandits"   ),(jump_to_menu, "mnu_camp"),
		 (else_try),(eq, "$g_encountered_party", "p_ancient_ruins"  ),(jump_to_menu, "mnu_ancient_ruins"), #TLD sorcerer
		 (else_try),(eq, "$g_encountered_party_template", "pt_ruins"),(jump_to_menu, "mnu_ruins"), #TLD ruins
		 (else_try),(eq, "$g_encountered_party_template", "pt_legendary_place"),(jump_to_menu, "mnu_legendary_place"), #TLD legendary places
		 (else_try),(eq, "$g_encountered_party_template", "pt_mound"),(jump_to_menu, "mnu_burial_mound"), #TLD 808
		 (else_try),(eq, "$g_encountered_party_template", "pt_pyre" ),(jump_to_menu, "mnu_funeral_pyre"), #TLD 808
		 (else_try),(eq, "$g_encountered_party", "p_old_ford"   ),(jump_to_menu, "mnu_camp"),
		#(else_try),(eq, "$g_encountered_party_template", "pt_defend_refugees"),(jump_to_menu, "mnu_defend_refugees"), #TODO
		(else_try),(jump_to_menu, "mnu_simple_encounter"),
		(try_end),
	(else_try), #Battle or siege
		(try_begin),
			(this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
			(party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
			(try_begin),
				(eq, "$auto_enter_town", "$g_encountered_party"),
				(jump_to_menu, "mnu_town"),
			(else_try),
				(eq, "$auto_besiege_town", "$g_encountered_party"),
				(jump_to_menu, "mnu_besiegers_camp_with_allies"),
			(else_try),
				(jump_to_menu, "mnu_join_siege_outside"),
			(try_end),
		(else_try),
			(jump_to_menu, "mnu_pre_join"),
		(try_end),
	(try_end),
	(assign,"$auto_enter_town",0),
	(assign,"$auto_besiege_town",0),
]),

#script_game_event_simulate_battle:
# This script is called whenever the game simulates the battle between two parties on the map.
# INPUT:
# param1: Defender Party
# param2: Attacker Party
("game_event_simulate_battle",[
	(store_script_param_1, ":root_defender_party"),
	(store_script_param_2, ":root_attacker_party"),

	(try_begin),
		(this_or_next|neg|party_is_active,":root_defender_party"),
		(neg|party_is_active,":root_attacker_party"),
		(set_trigger_result, 1),
	(else_try),
		(store_faction_of_party, ":defender_faction", ":root_defender_party"),
		(store_faction_of_party, ":attacker_faction", ":root_attacker_party"),
		(neq, ":defender_faction", "fac_player_faction"),
		(neq, ":attacker_faction", "fac_player_faction"),
		(store_relation, ":reln", ":defender_faction", ":attacker_faction"),
		(ge, ":reln", 0),
		(set_trigger_result, 1),
	(else_try),
		(assign, ":trigger_result", 0),

		(try_begin),
			(this_or_next|eq, "$g_battle_simulation_cancel_for_party", ":root_defender_party"),
			(eq, "$g_battle_simulation_cancel_for_party", ":root_attacker_party"),
			(assign, "$g_battle_simulation_cancel_for_party", -1),
			(assign, "$auto_enter_town", "$g_battle_simulation_auto_enter_town_after_battle"),
			(assign, ":trigger_result", 1),
		(else_try),
			(try_begin),
				(this_or_next|party_slot_eq, ":root_defender_party", slot_party_retreat_flag, 1),
				(party_slot_eq, ":root_attacker_party", slot_party_retreat_flag, 1),
				(assign, ":trigger_result", 1), #End battle!
			(try_end),
			(party_set_slot, ":root_attacker_party", slot_party_retreat_flag, 0),
			##         (assign, ":cancel_attack", 0),
			(party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
			(party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),
			#          (call_script, "script_party_count_fit_for_battle", "p_collective_ally"),
			(call_script, "script_party_calculate_strength", "p_collective_ally", 0),
			(assign, ":defender_strength", reg0),
			#           (call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
			(call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
			(assign, ":attacker_strength", reg0),
			(store_div, ":defender_strength", ":defender_strength", 20),
			(val_min, ":defender_strength", 50),
			(val_max, ":defender_strength", 1),
			(store_div, ":attacker_strength", ":attacker_strength", 20),
			(val_min, ":attacker_strength", 50),
			(val_add, ":attacker_strength", 1),
			(try_begin),
				#For sieges increase attacker casualties and reduce defender casualties.
				(this_or_next|party_slot_eq, ":root_defender_party", slot_party_type, spt_castle),
				(party_slot_eq, ":root_defender_party", slot_party_type, spt_town),
				(val_mul, ":defender_strength", 3),
				(val_div, ":defender_strength", 2),
				(val_div, ":attacker_strength", 2),
			(try_end),

			(try_begin),
				# night in TLD is primary WAR TIME =)! GA
				#             (neg|is_currently_night), #Don't fight at night
				(inflict_casualties_to_party_group, ":root_attacker_party", ":defender_strength", "p_temp_casualties"),
				(party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),
			(try_end),
			(call_script, "script_party_count_fit_for_battle", "p_collective_enemy", 0),
			(assign, ":new_attacker_strength", reg0),

			(try_begin),
				(gt, ":new_attacker_strength", 0),
				# night in TLD is primary WAR TIME =)! GA
				#             (neg|is_currently_night), #Don't fight at night
				(inflict_casualties_to_party_group, ":root_defender_party", ":attacker_strength", "p_temp_casualties"),
				(party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
			(try_end),
			(call_script, "script_party_count_fit_for_battle", "p_collective_ally", 0),
			(assign, ":new_defender_strength", reg0),

			(try_begin),
				(this_or_next|eq, ":new_attacker_strength", 0),
				(eq, ":new_defender_strength", 0),
				# Battle concluded! determine winner
				(try_begin),
					(eq, ":new_attacker_strength", 0),
					(eq, ":new_defender_strength", 0),
					(assign, ":root_winner_party", -1),
					(assign, ":root_defeated_party", -1),
					(assign, ":collective_casualties", -1),
				(else_try),
					(eq, ":new_attacker_strength", 0),
					(assign, ":root_winner_party",   ":root_defender_party"),
					(assign, ":root_defeated_party", ":root_attacker_party"),
					(assign, ":collective_casualties",    "p_collective_enemy"),
				(else_try),
					(assign, ":root_winner_party", ":root_attacker_party"),
					(assign, ":root_defeated_party",  ":root_defender_party"),
					(assign, ":collective_casualties",  "p_collective_ally"),
				(try_end),
				
				(party_clear, "p_temp_party"),
				(try_begin),
					(ge, ":root_winner_party", 0),
					(call_script, "script_get_nonempty_party_in_group", ":root_winner_party"),
					(assign, ":nonempty_winner_party", reg0),
					(call_script, "script_remove_empty_parties_in_group", ":root_winner_party"), #GA: purge all empty winner parties, stash prisoners to p_temp_party
					(store_faction_of_party, ":faction_receiving_prisoners", ":nonempty_winner_party"),
					(store_faction_of_party, ":defeated_faction", ":root_defeated_party"),
				(else_try),
					(assign, ":nonempty_winner_party", -1),
				(try_end),

				(try_begin),
					(ge, ":collective_casualties", 0),
					(assign, "$g_move_heroes", 1), 
					(party_set_faction, "p_temp_party", ":faction_receiving_prisoners"),
					(call_script, "script_party_add_party_prisoners", "p_temp_party", ":collective_casualties"),
					(call_script, "script_party_prisoners_add_party_companions", "p_temp_party", ":collective_casualties"),
				(try_end),

				(try_begin),
					(ge, ":collective_casualties", 0),
					(party_get_num_companion_stacks, ":num_stacks", ":collective_casualties"),
				(else_try),
					(assign, ":num_stacks", 0),
				(try_end),
				(try_for_range, ":troop_iterator", 0, ":num_stacks"),
					(party_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
					(troop_is_hero, ":cur_troop_id"),
					(call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
					(troop_set_slot, ":cur_troop_id", slot_troop_leaded_party, -1),
					(store_random_in_range, ":rand", 0, 100),
					(str_store_troop_name_link, s1, ":cur_troop_id"),
					(str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
					(store_troop_faction, ":defeated_troop_faction", ":cur_troop_id"),
					(str_store_faction_name_link, s3, ":defeated_troop_faction"),
					(try_begin),
						(ge, ":rand", hero_escape_after_defeat_chance),
						(party_stack_get_troop_id, ":leader_troop_id", ":nonempty_winner_party", 0),
						(is_between, ":leader_troop_id", kingdom_heroes_begin, kingdom_heroes_end), #disable non-kingdom parties capturing enemy lords
						#                 (party_add_prisoners, ":nonempty_winner_party", ":cur_troop_id", 1), #TLD: lords captured will later be moved to prisoner train
						(gt, reg0, 0),
						#(troop_set_slot, ":cur_troop_id", slot_troop_is_prisoner, 1),
						(troop_set_slot, ":cur_troop_id", slot_troop_prisoner_of_party, ":nonempty_winner_party"),
						(display_log_message, "str_hero_taken_prisoner"),
					(else_try),
						(party_remove_members, "p_temp_party", ":cur_troop_id", 1), #TLD: lords captured will later be moved to prisoner train
						(try_begin),
							(store_relation, ":rel", "$players_kingdom", ":defeated_troop_faction"),
							(lt, ":rel", 0),
							(assign, ":news_color", color_good_news),
						(else_try),
							(assign, ":news_color", color_bad_news),
						(try_end),
						(display_message,"@{s1} of {s3} was defeated in battle.", ":news_color"),
						#(display_message,"@{s1} of {s3} was defeated in battle but managed to escape.", ":news_color"),
						######################## map heroes injuries and deaths
						(eq, "$tld_option_death_npc", 1), # if death option is available
						(store_random_in_range,":rnd",0,100),
						(try_begin),
							(lt,":rnd",5), # die with 5% prob when lost a battle
							(is_between, ":cur_troop_id", "trp_knight_1_1", kingdom_heroes_end), #kings and marshals cannot die for now
                            (store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
                            (neg|faction_slot_eq, ":cur_troop_faction", slot_faction_marshall, ":cur_troop_id"), #make sure it's not a marshall
                            # MV: additional random chance to survive if there are too few lords in the faction
                            (assign, ":total_lords", 0), # exclude non-active kings, but count himself
                            (try_for_range, ":some_lord", kingdom_heroes_begin, kingdom_heroes_end),
                                (store_troop_faction, ":some_lord_faction", ":some_lord"),
                                (eq, ":some_lord_faction", ":cur_troop_faction"),
                                # is not a king OR is a marshall (=don't count non-active kings)
                                (this_or_next|neg|faction_slot_eq, ":some_lord_faction", slot_faction_leader, ":some_lord"),
                                (faction_slot_eq, ":some_lord_faction", slot_faction_marshall, ":some_lord"),
                                (neg|troop_slot_eq, ":some_lord", slot_troop_wound_mask, wound_death), #not dead
                                (val_add, ":total_lords", 1),
                            (try_end),
                            # 1 lord left (him) 0%, 2 lords left 10% (some small factions),... 6 lords left 50% chance to die
                            (store_random_in_range,":rnd_last_chance",0,100),
                            (store_sub, ":last_chance", ":total_lords", 1),
                            (val_mul, ":last_chance", 10),
                            (lt, ":rnd_last_chance", ":last_chance"), # die for real?
							(call_script, "script_hero_leader_killed_abstractly", ":cur_troop_id",":nonempty_winner_party"),
						(try_end),
					(try_end),
					(try_begin),
						(store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
						(faction_slot_eq, ":cur_troop_faction", slot_faction_marshall, ":cur_troop_id"),
						#Marshall is defeated, refresh ai.
						(assign, "$g_recalculate_ais", 1),
					(try_end),
				(try_end),
				(try_begin),
					(ge, ":collective_casualties", 0),
					(party_get_num_prisoner_stacks, ":num_stacks", ":collective_casualties"),
				(else_try),
					(assign, ":num_stacks", 0),
				(try_end),
				(try_for_range, ":troop_iterator", 0, ":num_stacks"),
					(party_prisoner_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
					(troop_is_hero, ":cur_troop_id"),
					(call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
					(store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
					(str_store_troop_name_link, s1, ":cur_troop_id"),
					(str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
					(str_store_faction_name_link, s3, ":cur_troop_faction"),
					(display_log_message,"str_hero_freed"),
				(try_end),

				(try_begin),
					# TLD: spawn prisoner train
					(store_party_size, ":size", "p_temp_party"),
					(gt, ":size", 0),
					(try_begin),
						(store_party_size, ":size", "p_temp_party"),
						(store_party_size_wo_prisoners, ":comps", "p_temp_party"),
						(val_sub, ":size", ":comps"),
						(gt, ":size", 0),
						(is_between, ":faction_receiving_prisoners", kingdoms_begin, kingdoms_end),
						(faction_get_slot, ":prisoner_train_pt", ":faction_receiving_prisoners", slot_faction_prisoner_train),
						(neq, ":prisoner_train_pt", -1),
						(set_spawn_radius, 1),
						(spawn_around_party, ":nonempty_winner_party", ":prisoner_train_pt"),
						(assign, ":prisoner_train", reg0),
						(party_set_faction, ":prisoner_train", ":faction_receiving_prisoners"),
						(party_set_slot, ":prisoner_train", slot_party_victory_value, ws_p_train_vp),
						(party_set_slot, ":prisoner_train", slot_party_type, spt_prisoner_train),
						(assign, "$g_move_heroes", 0), #MV set to 0, lords escape
						(call_script, "script_party_prisoners_add_party_prisoners", ":prisoner_train", "p_temp_party"),
						(call_script, "script_party_remove_all_prisoners", "p_temp_party"),
						(call_script, "script_find_random_nearby_friendly_town", ":prisoner_train", 1),
						#                        (str_store_faction_name, s1, ":faction_receiving_prisoners"),
						#                        (party_set_name, ":prisoner_train", "@{s1} Prisoner Train"),
						(party_set_slot, ":prisoner_train", slot_party_ai_state, spai_undefined),
						(party_set_ai_behavior, ":prisoner_train", ai_bhvr_travel_to_party),
						(party_set_ai_object, ":prisoner_train", reg0),
						(party_set_slot, ":prisoner_train", slot_party_ai_object, reg0),
						(party_set_flags, ":prisoner_train", pf_default_behavior, 0),
					(try_end),
					(try_begin),
						(gt, ":root_winner_party", 0),
						(distribute_party_among_party_group, "p_temp_party", ":root_winner_party"),
					(try_end),                      
                # TLD: spawn prisoner train end
				(try_end),

				(call_script, "script_clear_party_group", ":root_defeated_party", ":faction_receiving_prisoners"),
				(assign, ":trigger_result", 1), #End battle!

				#Center captured
				(try_begin),
					(ge, ":collective_casualties", 0),
					(party_get_slot, ":cur_party_type", ":root_defeated_party", slot_party_type),
					(this_or_next|eq, ":cur_party_type", spt_town),
					(eq, ":cur_party_type", spt_castle),

					(assign, "$g_recalculate_ais", 1),

					(store_faction_of_party, ":winner_faction", ":root_winner_party"),
					(store_faction_of_party, ":defeated_faction", ":root_defeated_party"),

					(str_store_party_name, s1, ":root_defeated_party"),
					(str_store_faction_name, s2, ":winner_faction"),
					(str_store_faction_name, s3, ":defeated_faction"),
					(try_begin),
						(store_relation, ":rel", "$players_kingdom", ":winner_faction"),
						(gt, ":rel", 0),
						(assign, ":news_color", color_good_news),
                        (play_sound, "snd_enemy_lord_dies"),
					(else_try),
						(assign, ":news_color", color_bad_news),
                        (play_sound, "snd_lord_dies"),
					(try_end),
					(try_begin),
						(party_slot_ge, ":root_defeated_party", slot_center_destroy_on_capture, 1),
						(display_log_message, "@{s2} have razed {s1}!", ":news_color"),
					(else_try),
						(display_log_message, "str_center_captured", ":news_color"),
					(try_end),

					(try_begin),
						(eq, "$g_encountered_party", ":root_defeated_party"),
						##                  (display_message, "@Player participation in siege called from g_encountered_party"),
						(call_script, "script_add_log_entry", logent_player_participated_in_siege, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
					(try_end),
  ##             (try_begin),
  ##                  (eq, "$g_encountered_party_2", ":root_defeated_party"),
  ##                  (display_message, "@Player participation in siege called from game_event_simulate_battle thanks to g_encountered_party"),
  ##             (try_end),
  ##             (try_begin),
  ##                  (eq, "$g_enemy_party", ":root_defeated_party"),
  ##                  (display_message, "@Player participation in siege called from game_event_simulate_battle thanks to g_encountered_party"),
  ##             (try_end),


					(try_begin),
						(party_get_num_companion_stacks, ":num_stacks", ":root_winner_party"),
						(gt, ":num_stacks", 0),
						(party_stack_get_troop_id, ":leader_troop_no", ":root_winner_party", 0),
						(is_between, ":leader_troop_no", kingdom_heroes_begin, kingdom_heroes_end),
						(party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, ":leader_troop_no"),
					(else_try),
						(party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, -1),
					(try_end),

					(call_script, "script_lift_siege", ":root_defeated_party", 0),
					(try_begin), #TLD: if center destroyable, disable it, otherwise proceed as normal
						(party_slot_ge, ":root_defeated_party", slot_center_destroy_on_capture, 1),
						(call_script, "script_destroy_center", ":root_defeated_party"),
					(else_try),
						(call_script, "script_give_center_to_faction", ":root_defeated_party", ":winner_faction"),
						(call_script, "script_order_best_besieger_party_to_guard_center", ":root_defeated_party", ":winner_faction"),
						# add a small garrison
						(try_for_range, ":unused", 0, 5),
							(call_script, "script_cf_reinforce_party", ":root_defeated_party"),
						(try_end),
					(try_end),
				(try_end),
			(try_end),

			#ADD XP
			(try_begin),
				(party_slot_eq, ":root_attacker_party", slot_party_type, spt_kingdom_hero_party),
				(store_random_in_range, ":random_num",0, 100),
				(lt, ":random_num", 25),
				(gt, ":new_attacker_strength", 0),
				(call_script, "script_upgrade_hero_party", ":root_attacker_party", 1000),
			(try_end),
			(try_begin),
				(party_slot_eq, ":root_defender_party", slot_party_type, spt_kingdom_hero_party),
				(store_random_in_range, ":random_num",0, 100),
				(lt, ":random_num", 25),
				(gt, ":new_defender_strength", 0),
				(call_script, "script_upgrade_hero_party", ":root_defender_party", 1000),
			(try_end),

			(store_random_in_range, ":random_num", 0, 100),
			(try_begin),
				(lt, ":random_num", 10),
				##           (this_or_next|lt, ":random_num", 10),
				##           (eq, ":cancel_attack", 1),
				(assign, ":trigger_result", 1), #End battle!
			(try_end),
		(try_end),
		(set_trigger_result, ":trigger_result"),
	(try_end),
]),

#script_game_event_battle_end:
# This script is called whenever the game ends the battle between two parties on the map.
# INPUT:
# param1: Defender Party
# param2: Attacker Party
("game_event_battle_end",[
    #(store_script_param_1, ":root_defender_party"),
    #(store_script_param_2, ":root_attacker_party"),
      
	#Fixing deleted heroes
	(try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
		(troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
		(troop_get_slot, ":cur_prisoner_of_party", ":cur_troop", slot_troop_prisoner_of_party),
		(try_begin),
			(ge, ":cur_party", 0),
			(assign, ":continue", 0),
			(try_begin),
				(neg|party_is_active, ":cur_party"),
				(assign, ":continue", 1),
			(else_try),
				(party_count_companions_of_type, ":amount", ":cur_party", ":cur_troop"),
				(le, ":amount", 0),
				(assign, ":continue", 1),
			(try_end),
			(eq, ":continue", 1),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s1, ":cur_troop"),
				(display_message, "@DEBUG: {s1} no longer leads a party."),
			(try_end),
			(troop_set_slot, ":cur_troop", slot_troop_leaded_party, -1),
		(try_end),
		(try_begin),
			(ge, ":cur_prisoner_of_party", 0),
			(assign, ":continue", 0),
			(try_begin),
				(neg|party_is_active, ":cur_prisoner_of_party"),
				(assign, ":continue", 1),
			(else_try),
				(party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party", ":cur_troop"),
				(le, ":amount", 0),
				(assign, ":continue", 1),
			(try_end),
			(eq, ":continue", 1),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s1, ":cur_troop"),
				(display_message, "@DEBUG: {s1} is no longer a prisoner."),
			(try_end),
			(call_script, "script_remove_troop_from_prison", ":cur_troop"),
		#searching player
			(try_begin),
				(party_count_prisoners_of_type, ":amount", "p_main_party", ":cur_troop"),
				(gt, ":amount", 0),
				(troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, "p_main_party"),
				(assign, ":continue", 0),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s1, ":cur_troop"),
					(display_message, "@DEBUG: {s1} is now a prisoner of player."),
				(try_end),
			(try_end),
			(eq, ":continue", 1),
		#searching kingdom heroes
			(try_for_range, ":cur_troop_2", kingdom_heroes_begin, kingdom_heroes_end),
				(eq, ":continue", 1),
				(troop_get_slot, ":cur_prisoner_of_party_2", ":cur_troop_2", slot_troop_leaded_party),
				(party_is_active, ":cur_prisoner_of_party_2"),
				(party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party_2", ":cur_troop"),
				(gt, ":amount", 0),
				(troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, ":cur_prisoner_of_party_2"),
				(assign, ":continue", 0),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s1, ":cur_troop"),
					(str_store_party_name, s2, ":cur_prisoner_of_party_2"),
					(display_message, "@DEBUG: {s1} is now a prisoner of {s2}."),
				(try_end),
			(try_end),
		#searching walled centers
			(try_for_range, ":cur_prisoner_of_party_2", centers_begin, centers_end),
				(party_slot_eq, ":cur_prisoner_of_party_2", slot_center_destroyed, 0), #TLD - not destroyed
				(eq, ":continue", 1),
				(party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party_2", ":cur_troop"),
				(gt, ":amount", 0),
				(troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, ":cur_prisoner_of_party_2"),
				(assign, ":continue", 0),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s1, ":cur_troop"),
					(str_store_party_name, s2, ":cur_prisoner_of_party_2"),
					(display_message, "@DEBUG: {s1} is now a prisoner of {s2}."),
				(try_end),
			(try_end),
		(try_end),
	(try_end),
]),

#script_order_best_besieger_party_to_guard_center:
# INPUT: param1: defeated_center, param2: winner_faction
("order_best_besieger_party_to_guard_center",[
	(store_script_param, ":defeated_center", 1),
	(store_script_param, ":winner_faction", 2),
	(assign, ":best_party", -1),
	(assign, ":best_party_strength", 0),
	(try_for_range, ":kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
		(troop_get_slot, ":kingdom_hero_party", ":kingdom_hero", slot_troop_leaded_party),
		(gt, ":kingdom_hero_party", 0),
		(store_distance_to_party_from_party, ":dist", ":kingdom_hero_party", ":defeated_center"),
		(lt, ":dist", 5),
		(store_faction_of_party, ":kingdom_hero_party_faction", ":kingdom_hero_party"),
		(eq, ":winner_faction", ":kingdom_hero_party_faction"),
		#If marshall has captured the castle, then do not leave him behind.
		(neg|faction_slot_eq, ":winner_faction", slot_faction_marshall, ":kingdom_hero"),
		(assign, ":has_besiege_ai", 0),
		(try_begin),
			(party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_besieging_center),
			(party_slot_eq, ":kingdom_hero_party", slot_party_ai_object, ":defeated_center"),
			(assign, ":has_besiege_ai", 1),
		(else_try),
			(party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_accompanying_army),
			(party_get_slot, ":kingdom_hero_party_commander_party", ":kingdom_hero_party", slot_party_commander_party),
			(party_slot_eq, ":kingdom_hero_party_commander_party", slot_party_ai_state, spai_besieging_center),
			(party_slot_eq, ":kingdom_hero_party_commander_party", slot_party_ai_object, ":defeated_center"),
			(assign, ":has_besiege_ai", 1),
		(try_end),
		(eq, ":has_besiege_ai", 1),
		(party_get_slot, ":kingdom_hero_party_strength", ":kingdom_hero_party", slot_party_cached_strength),#recently calculated
		(gt, ":kingdom_hero_party_strength", ":best_party_strength"),
		(assign, ":best_party_strength", ":kingdom_hero_party_strength"),
		(assign, ":best_party", ":kingdom_hero_party"),
	(try_end),
	(try_begin),
		(gt, ":best_party", 0),
		(call_script, "script_party_set_ai_state", ":best_party", spai_holding_center, ":defeated_center"),
		(party_set_slot, ":best_party", slot_party_commander_party, -1),
		(party_set_flags, ":best_party", pf_default_behavior, 1),
	(try_end),
]),

#script_game_get_item_buy_price_factor:
# This script is called from the game engine for calculating the buying price of any item.
# INPUT: param1: item_kind_id
# OUTPUT: trigger_result and reg0 = price_factor
("game_get_item_buy_price_factor",
    [ (store_script_param_1, ":item_kind_id"),
      (assign, ":price_factor", 100),

      (call_script, "script_get_trade_penalty", ":item_kind_id"),
      (assign, ":trade_penalty", reg0),
      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price_factor", "$g_encountered_party", ":item_slot_no"),
        (val_mul, ":price_factor", 100), #normalize price factor to range 0..100
        (val_div, ":price_factor", average_price_factor),
      (try_end),
      (store_add, ":penalty_factor", 100, ":trade_penalty"),
      (val_mul, ":price_factor", ":penalty_factor"),
      (val_div, ":price_factor", 100),
      (assign, reg0, ":price_factor"),
      (set_trigger_result, reg0),
]),

#script_game_get_item_sell_price_factor:
# This script is called from the game engine for calculating the selling price of any item.
# INPUT: param1: item_kind_id
# OUTPUT: trigger_result and reg0 = price_factor
("game_get_item_sell_price_factor",
    [ (store_script_param_1, ":item_kind_id"),
#      (assign, ":price_factor", 100),
#      (call_script, "script_get_trade_penalty", ":item_kind_id"),
#      (assign, ":trade_penalty", reg0),
    # (try_begin),
      # (is_between, "$g_encountered_party", centers_begin, centers_end),
      # (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
      # (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
      # (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
      # (party_get_slot, ":price_factor", "$g_encountered_party", ":item_slot_no"),
      # (val_mul, ":price_factor", 100),#normalize price factor to range 0..100
      # (val_div, ":price_factor", average_price_factor),
    # (else_try),
      # (val_mul, ":trade_penalty", 4),        #increase trade penalty while selling
    # (try_end),
    # (store_add, ":penalty_divisor", 100, ":trade_penalty"),
    # (val_mul, ":price_factor", 100),
    # (val_div, ":price_factor", ":penalty_divisor"),
	  
	(party_get_skill_level, ":trade_skill", "p_main_party", skl_trade), #trade skill adds 5% per level up to 100% price
	(val_mul, ":trade_skill", 5),
    (store_add, reg0, 50, ":trade_skill"),
	  
#	(store_faction_of_party,":faction","$g_encountered_party"),
	(faction_get_slot, ":faction_mask", "$ambient_faction", slot_faction_mask),# items of wrong faction are less valuable when selling
	(item_get_slot,":item_faction_mask",":item_kind_id",slot_item_faction),
    (val_and,":item_faction_mask",":faction_mask"),
	(try_begin),
		(eq,":item_faction_mask",0),
		(val_div, reg0,5), # discount for wrong faction items 80%
	(try_end),
	(val_min, reg0, 100),
    (set_trigger_result, reg0),
]),

# script_get_trade_penalty
# Input: param1 troop_id,
# Output: reg0
("get_trade_penalty",
    [ (store_script_param_1, ":item_kind_id"),
      (assign, ":penalty",0),
      
      (party_get_skill_level, ":trade_skill", "p_main_party", skl_trade),
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (assign, ":penalty",20),
        (store_mul, ":skill_bonus", ":trade_skill", 1),
        (val_sub, ":penalty", ":skill_bonus"),
      (else_try),
        (assign, ":penalty",100),
        (store_mul, ":skill_bonus", ":trade_skill", 5),
        (val_sub, ":penalty", ":skill_bonus"),
      (try_end),
      (assign, ":penalty_multiplier", 1000),
##       # Apply penalty if player is hostile to merchants faction
##      (store_relation, ":merchants_reln", "fac_merchants", "fac_player_supporters_faction"),
##      (try_begin),
##        (lt, ":merchants_reln", 0),
##        (store_sub, ":merchants_reln_dif", 10, ":merchants_reln"),
##        (store_mul, ":merchants_relation_penalty", ":merchants_reln_dif", 20),
##        (val_add, ":penalty_multiplier", ":merchants_relation_penalty"),
##      (try_end),
       # Apply penalty if player is on bad terms with the town
      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (party_get_slot, ":center_relation", "$g_encountered_party", slot_center_player_relation),
        (store_mul, ":center_relation_penalty", ":center_relation", -3),
        (val_add, ":penalty_multiplier", ":center_relation_penalty"),
        (try_begin),
          (lt, ":center_relation", 0),
          (store_sub, ":center_penalty_multiplier", 100, ":center_relation"),
          (val_mul, ":penalty_multiplier", ":center_penalty_multiplier"),
          (val_div, ":penalty_multiplier", 100),
        (try_end),
      (try_end),
   # Apply penalty if player is on bad terms with the merchant (not currently used)
      (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
      (assign, ":troop_reln", reg0),
      #(troop_get_slot, ":troop_reln", "$g_talk_troop", slot_troop_player_relation),
      (try_begin),
        (lt, ":troop_reln", 0),
        (store_sub, ":troop_reln_dif", 0, ":troop_reln"),
        (store_mul, ":troop_relation_penalty", ":troop_reln_dif", 20),
        (val_add, ":penalty_multiplier", ":troop_relation_penalty"),
      (try_end),
      
      (val_mul, ":penalty",  ":penalty_multiplier"),
      (val_div, ":penalty", 1000),
      (val_max, ":penalty", 1),
      (assign, reg0, ":penalty"),
]),

#script_game_event_buy_item:
# This script is called from the game engine when player buys an item.
# INPUT: param1: item_kind_id
("game_event_buy_item",
    [ (store_script_param_1, ":item_kind_id"),
      (store_script_param_2, ":reclaim_mode"),
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":multiplier", "$g_encountered_party", ":item_slot_no"),
        (try_begin),
          (eq, ":reclaim_mode", 0),
          (val_add, ":multiplier", 10),
        (else_try),
          (val_add, ":multiplier", 15),
        (try_end),
        (val_min, ":multiplier", maximum_price_factor),
        (party_set_slot, "$g_encountered_party", ":item_slot_no", ":multiplier"),
      (try_end),
#	  (assign, "$equip_needs_checking", 1), #TLD, need to check
]),

#script_game_event_sell_item:
# This script is called from the game engine when player sells an item.
# INPUT: param1 = item_kind_id
("game_event_sell_item",
    [ (store_script_param_1, ":item_kind_id"),
      (store_script_param_2, ":return_mode"),
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":multiplier", "$g_encountered_party", ":item_slot_no"),
        (try_begin),
          (eq, ":return_mode", 0),
          (val_sub, ":multiplier", 15),
        (else_try),
          (val_sub, ":multiplier", 10),
        (try_end),
        (val_max, ":multiplier", minimum_price_factor),
        (party_set_slot, "$g_encountered_party", ":item_slot_no", ":multiplier"),
      (try_end),
]),

# script_game_get_prisoner_price
# This script is called from the game engine for calculating prisoner price
# Input: param1 = troop_id,
# Output: reg0
("game_get_prisoner_price",
    [ (store_script_param_1, ":troop_id"),
      (assign, reg0, 50),
      (try_begin),
        (store_character_level, ":troop_level", ":troop_id"),
        (assign, ":ransom_amount", ":troop_level"),
        (val_add, ":ransom_amount", 10), 
        (val_mul, ":ransom_amount", ":ransom_amount"),
        (val_div, ":ransom_amount", 6),
        (assign, reg0, ":ransom_amount"),
      (try_end),
      (set_trigger_result, reg0),
]),

# script_game_check_prisoner_can_be_sold
# This script is called from the game engine for checking if a given troop can be sold.
# Input: param1: troop_id,
# Output: reg0: 1= can be sold; 0= cannot be sold.
("game_check_prisoner_can_be_sold",
    [ (store_script_param_1, ":troop_id"),
      (assign, reg0, 0),
      (try_begin),
        (neg|troop_is_hero, ":troop_id"),
        (assign, reg0, 1),
      (try_end),
      (set_trigger_result, reg0),
]),

#script_game_event_detect_party:
# This script is called from the game engine when player party inspects another party.
# INPUT: param1 = Party-id
("game_event_detect_party",
    [   (store_script_param_1, ":party_id"),
        (try_begin),
          (party_slot_eq, ":party_id", slot_party_type, spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":leader", ":party_id", 0),
          (is_between, ":leader", kingdom_heroes_begin, kingdom_heroes_end),
          (call_script, "script_update_troop_location_notes", ":leader", 0),
        (else_try),
          (is_between, ":party_id", centers_begin, centers_end),
          (party_get_num_attached_parties, ":num_attached_parties",  ":party_id"),
          (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
            (party_get_attached_party_with_rank, ":attached_party", ":party_id", ":attached_party_rank"),
            (party_stack_get_troop_id, ":leader", ":attached_party", 0),
            (is_between, ":leader", kingdom_heroes_begin, kingdom_heroes_end),
            (call_script, "script_update_troop_location_notes", ":leader", 0),
          (try_end),
        (try_end),
]),

#script_game_event_undetect_party:
# This script is called from the game engine when player party inspects another party.
# INPUT: param1 = Party-id
("game_event_undetect_party",
    [   (store_script_param_1, ":party_id"),
        (try_begin),
          (party_slot_eq, ":party_id", slot_party_type, spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":leader", ":party_id", 0),
          (is_between, ":leader", kingdom_heroes_begin, kingdom_heroes_end),
          (call_script, "script_update_troop_location_notes", ":leader", 0),
        (try_end),
]),

#script_game_get_statistics_line:
# This script is called from the game engine when statistics page is opened.
# INPUT: param1 = line_no
("game_get_statistics_line",
    [ (store_script_param_1, ":line_no"),
      (try_begin),
        (eq, ":line_no", 0),
        (assign, reg1, "$number_of_player_deaths"),
		(store_sub, reg2, reg1, 1),
		(str_store_string, s1, "@Left for dead but miraculously survived: {reg1?{reg1} time{reg2?s:}:NEVER}"),
        (set_result_string, s1),
	  # skip line 1, for a sspacer
      (else_try),
        (eq, ":line_no", 2),
        (get_player_agent_kill_count, reg1),
		(str_store_string, s1, "str_number_of_troops_killed_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 3),
        (get_player_agent_kill_count, reg1, 1),
        (str_store_string, s1, "str_number_of_troops_wounded_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 4),
        (get_player_agent_own_troop_kill_count, reg1),
        (str_store_string, s1, "str_number_of_own_troops_killed_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 5),
        (get_player_agent_own_troop_kill_count, reg1, 1),
        (str_store_string, s1, "str_number_of_own_troops_wounded_reg1"),
        (set_result_string, s1),
      # (else_try),
        # (eq, ":line_no", 5), # test!!
        # (get_player_agent_own_troop_kill_count, reg1, 1),
		# (str_store_string, s1, "@So let's think of something worth keeping track of!"),
        # (set_result_string, s1),
     (try_end),
]),

#script_game_get_date_text:
# This script is called from the game engine when the date needs to be displayed.
# INPUT: arg1 = number of days passed since the beginning of the game
# OUTPUT: result string = date
# TLD: used Steward's Reckoning!!! -- mtarini
("game_get_date_text",
    [ (store_script_param_2, ":num_hours"),
      (store_div, ":num_days", ":num_hours", 24),
      (store_add, ":cur_day", ":num_days", 15),
      (assign, ":cur_month", 7),
      (assign, ":cur_year", 3018), # -- osgiliath conquered by mordor in 3018 -- mtarini
      (assign, ":try_range", 99999),
      (try_for_range, ":unused", 0, ":try_range"),
        (try_begin),
		   # the 5 "one day months"
          (this_or_next|eq, ":cur_month", 1),
          (this_or_next|eq, ":cur_month", 5),
          (this_or_next|eq, ":cur_month", 9),
          (this_or_next|eq, ":cur_month",13),
          (eq,              ":cur_month",17),
          (assign, ":month_day_limit", 1),
        (else_try),
		  # normal othor months have 30 days
          (assign, ":month_day_limit", 30),
        (try_end),
        (try_begin),
          (gt, ":cur_day", ":month_day_limit"),
          (val_sub, ":cur_day", ":month_day_limit"),
          (val_add, ":cur_month", 1),
          (try_begin),
            (gt, ":cur_month", 17),
            (val_sub, ":cur_month", 17),
            (val_add, ":cur_year", 1),
          (try_end),
        (else_try),
          (assign, ":try_range", 0),
        (try_end),
      (try_end),
      (assign, reg1, ":cur_day"),
      (assign, reg2, ":cur_year"),
      (try_begin),(eq, ":cur_month", 1), (str_store_string, s1,   "str_calendar_spec_day_1"),
      (else_try) ,(eq, ":cur_month", 2), (str_store_string, s1, "str_january_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 3), (str_store_string, s1, "str_february_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 4), (str_store_string, s1, "str_march_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 5), (str_store_string, s1,   "str_calendar_spec_day_2"),
      (else_try) ,(eq, ":cur_month", 6), (str_store_string, s1, "str_april_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 7), (str_store_string, s1, "str_may_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 8), (str_store_string, s1, "str_june_reg1_reg2"),
      (else_try) ,(eq, ":cur_month", 9), (str_store_string, s1,   "str_calendar_spec_day_3"),
      (else_try) ,(eq, ":cur_month",10), (str_store_string, s1, "str_july_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",11), (str_store_string, s1, "str_august_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",12), (str_store_string, s1, "str_september_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",13), (str_store_string, s1,   "str_calendar_spec_day_4"),
      (else_try) ,(eq, ":cur_month",14), (str_store_string, s1, "str_october_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",15), (str_store_string, s1, "str_november_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",16), (str_store_string, s1, "str_december_reg1_reg2"),
      (else_try) ,(eq, ":cur_month",17), (str_store_string, s1,   "str_calendar_spec_day_5"),
      (try_end),
      (set_result_string, s1),
]),  

#script_game_get_money_text:
# This script is called from the game engine when an amount of money needs to be displayed.
# INPUT: arg1 = amount in units
# OUTPUT: result string = money in text
("game_get_money_text",
    [ (store_script_param_1, ":amount"),
	  (str_store_faction_name, s2, "$ambient_faction"),
      (try_begin),
        (eq, ":amount", 1),
		(str_store_string, s1, "@1 Res.Pt ({s2})"),
        #(str_store_string, s1, "str_1_denar"),
      (else_try),
        (assign, reg1, ":amount"),
		(str_store_string, s1, "@{reg1} Res.Pts ({s2})"),
        #(str_store_string, s1, "str_reg1_denars"),
      (try_end),
      (set_result_string, s1),
]),

#script_game_get_party_companion_limit:
# This script is called from the game engine when the companion limit is needed for a party.
# INPUT: arg1 = none
# OUTPUT: reg0 = companion_limit
("game_get_party_companion_limit",
    [ #(assign, ":troop_no", "trp_player"),
      (assign, ":limit", 10),
      (store_skill_level, ":skill", "skl_leadership", "trp_player"),
      (store_attribute_level, ":charisma", "trp_player", ca_charisma),
      (val_mul, ":skill", 5),
      (val_add, ":limit", ":skill"),
      (val_add, ":limit", ":charisma"),
	#GA: add some capacity if there are orcs in the party (you can recruit loads of orcs in TLD)  
	  (assign,":total",0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"), #count number of orcs in party
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (troop_get_type, ":type", ":stack_troop"),
		(eq, ":type", tf_orc),
		  (neg|troop_is_mounted, ":stack_troop"),
		  (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
          (val_add, ":total", ":stack_size"),
      (try_end),  
	  (val_mul, ":total", orc_bonus_nominator  ),
	  (val_div, ":total", orc_bonus_denominator),
	  (val_add, ":limit", ":total"),
	  # no player renown in TLD	
      # (troop_get_slot, ":troop_renown", "trp_player", slot_troop_renown),
      # (store_div, ":renown_bonus", ":troop_renown", 25),
      # (val_add, ":limit", ":renown_bonus"),
      
      # MV: Add ranks bonus - note that it also counts ranks with dead and turned-hostile factions
      (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
        (call_script, "script_get_faction_rank", ":faction"),
        (val_add, ":limit", reg0),
        (try_begin),
		  (eq, ":faction", "$players_kingdom"),
          (val_add, ":limit", reg0), # double for home faction
        (try_end),
      (try_end),
      
      (assign, reg0, ":limit"),
      (set_trigger_result, reg0),
]),

# script_get_party_tot_join_cost (mtarini)
# Input: arg1 = party_no
# Output: reg0 = total 
("get_party_total_join_cost",
    [ (store_script_param_1, ":party_no"),
      (assign, ":total", 0),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
        (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
        (call_script, "script_game_get_join_cost", ":stack_troop",0),
        (val_mul, reg0, ":stack_size"),
        (val_add, ":total", reg0),
      (try_end),
      (assign, reg0, ":total"),
]),

# script_get_party_min_join_cost (mtarini)
# Input: arg1 = party_no
# Output: reg0 = returns party with minimal cost
("get_party_min_join_cost",
    [ (store_script_param_1, ":party_no"),
      (assign, ":res", 9999999),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
        (call_script, "script_game_get_join_cost", ":stack_troop",0),
        (val_min, ":res", reg0),
      (try_end),
      (assign, reg0, ":res"),
]),

# script_get_party_max_ranking_slot(mtarini)
# Input: arg1 = party_no
# Output: reg0 = returns party slot with max cost
("get_party_max_ranking_slot",
    [ (store_script_param_1, ":party_no"),
	  (assign, ":res", 0),
	  (assign, ":max", 0),
      (store_faction_of_party, ":pfac", ":party_no"),
      (party_get_slot, ":psubfac", ":party_no", slot_party_subfaction),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
		(store_character_level, ":lvl", ":stack_troop"),
		(store_troop_faction, ":fac",  ":stack_troop"),
		(troop_get_slot, ":subfac", ":stack_troop", slot_troop_subfaction),
		(try_begin), (eq, ":fac", ":pfac"), (val_add,  ":lvl", 20), (try_end),  # bonus for same faction
		(try_begin), (eq, ":subfac", ":psubfac"), (val_add,  ":lvl", 20), (try_end), # bonus for same subfaction
		(try_begin),
			(lt, ":max", ":lvl"),
			(assign, ":max", ":lvl"),
			(assign, ":res", ":i_stack"),
		(try_end),
      (try_end),
      (assign, reg0, ":res"),
]),

# script_party_split_by_faction (mtarini)
# Input: arg1 = party_A, retains only the player and troops of given faction
# Input: arg2 = party_B, receives the rest, old A = new A + new B
# Input: arg3 = faction
("party_split_by_faction",
    [ (store_script_param_1, ":partyA"),
      (store_script_param_2, ":partyB"),
      (store_script_param, ":fac", 3),
      (party_get_num_companion_stacks, ":num_stacks", ":partyA"),
	  (party_clear, ":partyB"),
	  
      (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":partyA", ":i_stack"),
        (store_troop_faction, ":fac_t", ":stack_troop"),
		(neq,  ":stack_troop", "trp_player"), # player stays in A
		(neg|troop_is_hero, ":stack_troop"),  # heroes stay in A (for hosts and stuff)
		(neq, ":fac_t", ":fac"),
        (party_stack_get_size,  ":stack_size",":partyA",":i_stack"),
        (party_remove_members, ":partyA", ":stack_troop",  ":stack_size"),
		(party_add_members, ":partyB", ":stack_troop",  ":stack_size"),
	(try_end),
]),

# script_reconstruct_main_party (MV)
# Reconstruct main party after splitting by script_party_split_by_faction
("reconstruct_main_party",[
	#(call_script, "script_party_add_party", "p_main_party", "p_temp_party"), #mtarini code that was replaced
    
    #MV: recreate the main party from p_encountered_party_backup (main backup) and p_main_party (factionalized main minus troops given away)
    #  I replaced the script_party_add_party solely because it messes up the party order as set by the player
    #  Possible bug in any case: loss of stack experience which is kept by the engine only for main party stacks
    (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
    (party_get_num_companion_stacks, ":num_stacks_2", "p_main_party"),
    # for every troop in p_encountered_party_backup try to find a match in p_main_party and remove as many as needed
    (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":stack_troop", "p_encountered_party_backup", ":i_stack"),
      (party_stack_get_size, ":stack_size", "p_encountered_party_backup", ":i_stack"),
      (neg|troop_is_hero, ":stack_troop"), #no heroes
      (store_troop_faction, ":troop_faction", ":stack_troop"),
      (eq, ":troop_faction", "$g_talk_troop_faction"),
      (assign, ":troop_found", 0),
      (try_for_range, ":j_stack", 0, ":num_stacks_2"),
        (party_stack_get_troop_id, ":stack_troop_2", "p_main_party", ":j_stack"),
        (party_stack_get_size, ":stack_size_2", "p_main_party", ":j_stack"),
        (neg|troop_is_hero, ":stack_troop_2"), #no heroes
        (eq, ":stack_troop", ":stack_troop_2"),
        (assign, ":troop_found", 1),
        (lt, ":stack_size_2", ":stack_size"), #stack_size-stack_size_2 of this troop were given away
        (store_sub, ":given_away", ":stack_size", ":stack_size_2"),
        (party_remove_members, "p_encountered_party_backup", ":stack_troop", ":given_away"),
      (try_end),
      # if not found in p_main_party, but still of the correct faction, whole stack was given
      (eq, ":troop_found", 0),
      (party_remove_members, "p_encountered_party_backup", ":stack_troop", ":stack_size"),
    (try_end),
    
    # now copy p_encountered_party_backup over p_main_party
    #(call_script, "script_party_copy", "p_main_party", "p_encountered_party_backup"), will copy the player too,
    #  so he'll be there twice, before the engine removes him - no need to risk anything funny there, so doing it manually
    (party_clear, "p_main_party"), #player still there!
    (assign, ":source_party", "p_encountered_party_backup"),
    (assign, ":target_party", "p_main_party"),
    # script_party_add_party_companions
    (party_get_num_companion_stacks, ":num_stacks",":source_party"),
    (try_for_range, ":stack_no", 0, ":num_stacks"),
      (party_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
      (neq, ":stack_troop", "trp_player"), #crucial
      (party_stack_get_size,         ":stack_size",":source_party",":stack_no"),
      (party_add_members, ":target_party", ":stack_troop", ":stack_size"),
      (party_stack_get_num_wounded, ":num_wounded", ":source_party", ":stack_no"),
      (party_wound_members, ":target_party", ":stack_troop", ":num_wounded"),
    (try_end),
    # script_party_prisoners_add_party_prisoners
    (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
    (try_for_range, ":stack_no", 0, ":num_stacks"),
      (party_prisoner_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
      (party_prisoner_stack_get_size,         ":stack_size",":source_party",":stack_no"),
      (party_add_prisoners, ":target_party", ":stack_troop", ":stack_size"),
    (try_end),
]),

#script_game_reset_player_party_name:
# This script is called from the game engine when the player name is changed.
# INPUT: none
# OUTPUT: none
("game_reset_player_party_name",
    [(str_store_troop_name, s5, "trp_player"),
     (party_set_name, "p_main_party", s5),
 ]),

# script_party_get_ideal_size @used for NPC parties.
# Input: arg1 = party_no
# Output: reg0: ideal size 
("party_get_ideal_size",
    [ (store_script_param_1, ":party_no"),
      (assign, ":limit", 30),
      (try_begin),
        (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
        (party_stack_get_troop_id, ":party_leader", ":party_no", 0),
        (store_faction_of_party, ":faction_id", ":party_no"),
        (assign, ":limit", 10),

        (store_skill_level, ":skill", "skl_leadership", ":party_leader"),
        (store_attribute_level, ":charisma", ":party_leader", ca_charisma),
        (val_mul, ":skill", 5),
        (val_add, ":limit", ":skill"),
        (val_add, ":limit", ":charisma"),

        (troop_get_slot, ":troop_renown", ":party_leader", slot_troop_renown),
        (store_div, ":renown_bonus", ":troop_renown", 25),
        (val_add, ":limit", ":renown_bonus"),

        (try_begin),
          (faction_slot_eq, ":faction_id", slot_faction_marshall, ":party_leader"),
          (val_add, ":limit", 70), #TLD: was 100, kings were too strong
        (try_end),
      (try_end),
      (store_character_level, ":level", "trp_player"), #increase limits a little bit as the game progresses.
      (store_add, ":level_factor", 90, ":level"),
      (val_mul, ":limit", ":level_factor"),
      (val_div, ":limit", 90),
	(troop_get_type, ":race", ":party_leader"),
     	(try_begin),	
		(is_between,":race",tf_elf_begin,tf_elf_end), # (CppCoder): Decrease party size of elven parties. 
		(val_mul, ":limit", 3), # CC: Was 2/3, upped to 3/4, elves wouldn't siege properly
      		(val_div, ":limit", 4),
	(else_try),
		(eq, ":faction_id", "fac_rhun"), # (CppCoder): Rhun now receives a boost to party size. (4/3)
		(val_mul, ":limit", 4), 
      		(val_div, ":limit", 3),
	(try_end),
      (assign, reg0, ":limit"),
]),

# stores the dominant race of a party (somewhat random)  (mtarini)
# input: PARTY.  Output: reg0: dominant race
("party_get_dominant_race",[
	(store_script_param_1, ":party"),
	(party_get_num_companion_stacks, ":num_stacks",":party"),
    (store_random_in_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":size_a",":party",":i_stack"),
	(party_stack_get_troop_id, ":tr",":party",":i_stack"),
	(troop_get_type,":val_a",":tr"),
    (store_random_in_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":size_b",":party",":i_stack"),
	(party_stack_get_troop_id, ":tr",":party",":i_stack"),
	(troop_get_type,":val_b",":tr"),
    (store_random_in_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":size_c",":party",":i_stack"),
	(party_stack_get_troop_id, ":tr",":party",":i_stack"),
	(troop_get_type,":val_c",":tr"),
	(try_begin),(eq,":val_a",":val_b"),(val_add,":size_a",":size_b"),(try_end),
	(try_begin),(eq,":val_b",":val_c"),(val_add,":size_b",":size_c"),(try_end),
	(try_begin),(eq,":val_c",":val_a"),(val_add,":size_c",":size_a"),(try_end),
	
	(try_begin),(ge,":size_a",":size_b"),(ge,":size_a",":size_c"),(assign, reg0, ":val_a"),
	 (else_try),(ge,":size_b",":size_a"),(ge,":size_b",":size_c"),(assign, reg0, ":val_b"),
	 (else_try),                                                  (assign, reg0, ":val_c"),
	(try_end),
]),

# stores the dominant faction of a party (somewhat random)  (mtarini)
# input: PARTY.  Output: reg0: dominant race
("party_get_dominant_faction",[
	(store_script_param_1, ":party"),
	(party_get_num_companion_stacks, ":num_stacks",":party"),
    (store_random_in_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":size_a",":party",":i_stack"),
	(party_stack_get_troop_id, ":tr",":party",":i_stack"),
	(store_troop_faction,":val_a",":tr"),
    (store_random_in_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":size_b",":party",":i_stack"),
	(party_stack_get_troop_id, ":tr",":party",":i_stack"),
	(store_troop_faction,":val_b",":tr"),
    (store_random_in_range, ":i_stack", 0, ":num_stacks"),
    (party_stack_get_size, ":size_c",":party",":i_stack"),
	(party_stack_get_troop_id, ":tr",":party",":i_stack"),
	(store_troop_faction,":val_c",":tr"),
	
	(try_begin),(eq,":val_a",fac_player_faction),(assign, ":val_a", "$players_kingdom"),(try_end),
	(try_begin),(eq,":val_b",fac_player_faction),(assign, ":val_b", "$players_kingdom"),(try_end),
	(try_begin),(eq,":val_c",fac_player_faction),(assign, ":val_c", "$players_kingdom"),(try_end),
	
	(try_begin),(eq,":val_a",":val_b"),(val_add,":size_a",":size_b"),(try_end),
	(try_begin),(eq,":val_b",":val_c"),(val_add,":size_b",":size_c"),(try_end),
	(try_begin),(eq,":val_c",":val_a"),(val_add,":size_c",":size_a"),(try_end),
	
	(try_begin),(ge,":size_a",":size_b"),(ge,":size_a",":size_c"),(assign, reg0, ":val_a"),
	(else_try), (ge,":size_b",":size_a"),(ge,":size_b",":size_c"),(assign, reg0, ":val_b"),
	(else_try), (assign, reg0, ":val_c"),
	(try_end),
]),

#script_game_get_party_prisoner_limit:
# This script is called from the game engine when the prisoner limit is needed for main party.
# INPUT: arg1 = party_no
# OUTPUT: reg0 = prisoner_limit
("game_get_party_prisoner_limit",
    [#(store_script_param_1, ":party_no"),
     #(assign, ":troop_no", "trp_player"),
      (assign, ":limit", 0),
      (store_skill_level, ":skill", "skl_prisoner_management", "trp_player"),
      (store_mul, ":limit", ":skill", 5),
      (assign, reg0, ":limit"),
      (set_trigger_result, reg0),
]),

#script_game_get_item_extra_text:
# This script is called from the game engine when an item's properties are displayed.
# INPUT: arg1 = item_no, arg2 = extra_text_id (this can be between 0-7 (7 included)), arg3 = item_modifier
# OUTPUT: result_string = item extra text, trigger_result = text color (0 for default)
("game_get_item_extra_text",
    [ (store_script_param, ":item_no", 1),
      (store_script_param, ":extra_text_id", 2),
      (store_script_param, ":item_modifier", 3),
	  #(item_get_type,":itp", ":item_no"),
      (try_begin),
		(eq,":item_no","itm_lembas"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+30 to Party Morale"),(try_end),
        (set_trigger_result, color_item_text_morale),
      (else_try),
		(eq,":item_no","itm_cooking_cauldron"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+20 to Party Morale"),(try_end),
        (set_trigger_result, color_item_text_morale),
      (else_try),
		(eq,":item_no","itm_rohan_saddle"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Riding Skill"),(try_end),
		#(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@+1 to Horse Archery"),(try_end),
        (set_trigger_result, color_item_text_bonus),
      (else_try),
		(eq,":item_no","itm_map"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Pathfinding"),(try_end),
        (set_trigger_result, color_item_text_bonus),
      (else_try),
		(eq,":item_no","itm_orc_brew"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Athletics"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_ent_water"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@Use from"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@Action Menu"),(try_end),
        (set_trigger_result, color_item_text_normal),
      (else_try),
		(eq,":item_no","itm_athelas_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to First Aid"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_hammer_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Weapon Mastery"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_garlic_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Wound Treatment"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_scroll_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Tactics"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_torque_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Power Strike"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(this_or_next|eq,":item_no","itm_westernesse1h_reward"),
		(eq,":item_no","itm_westernesse2h_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Power Strike"),(set_trigger_result, color_item_text_bonus),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@when equipped"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_ring_a_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Strength"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_ring_b_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Agility"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_herbarium_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Wound Treatment"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_silmarillion_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Leadership"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_elven_amulet_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Power Draw"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_angmar_whip_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Trainer"),(set_trigger_result, color_item_text_bonus),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(eq, "$tld_option_morale", 0),(set_result_string, "@Recruits Tribal Orcs"),(set_trigger_result, color_item_text_special),(try_end),
		(try_begin),
			(eq, "$tld_option_morale", 1),
			(eq, ":extra_text_id", 1),
			(store_skill_level, reg1, "skl_leadership", "trp_player"),
			(val_div, reg1, 3),
			(gt, reg1, 0),
			(str_store_string, s3, "@rally"),
			(try_begin),(gt, reg1, 1),(str_store_string, s3, "@rallies"),(try_end),		
			(set_result_string, "@+{reg1} {s3} in battle"),
			(set_trigger_result, color_item_text_bonus),
		(try_end),
		(try_begin),(eq, "$tld_option_morale", 1),(eq, ":extra_text_id", 2),(set_result_string, "@Recruits Tribal Orcs"),(set_trigger_result, color_item_text_special),(try_end),
      (else_try),
		(eq,":item_no","itm_horn_gondor_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Leadership"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@+1 to Charisma"),(try_end),		
		(try_begin),
			(eq, "$tld_option_morale", 1),
			(eq, ":extra_text_id", 2),
			(store_skill_level, reg1, "skl_leadership", "trp_player"),
			(val_div, reg1, 3),
			(gt, reg1, 0),
			(str_store_string, s3, "@rally"),
			(try_begin),(gt, reg1, 1),(str_store_string, s3, "@rallies"),(try_end),		
			(set_result_string, "@+{reg1} {s3} in battle"),
		(try_end),
        (set_trigger_result, color_item_text_bonus),
      (else_try),
		(eq,":item_no","itm_harad_totem_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to First Aid"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@+1 to Surgery"),(try_end),
        (set_trigger_result, color_item_text_bonus),
      (else_try),
		(eq,":item_no","itm_phial_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Persuasion"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@+1 to Leadership"),(try_end),
        (set_trigger_result, color_item_text_bonus),
      (else_try),
		(eq,":item_no","itm_khand_knife_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Leadership"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@+1 to Charisma"),(try_end),
        (set_trigger_result, color_item_text_bonus),
      (else_try),
		(eq,":item_no","itm_witchking_helmet"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Ironflesh"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@+1 to Prisoner Mgmt"),(try_end),
		(try_begin),(eq, ":extra_text_id", 2),(set_result_string, "@+1 to Charisma"),(try_end),
		(try_begin),(eq, ":extra_text_id", 3),(set_result_string, "@when equipped"),(try_end),
        (set_trigger_result, color_item_text_bonus),
      (else_try),
		(eq,":item_no","itm_explosive_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Tactics"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@+2 to Engineering"),(try_end),
        (set_trigger_result, color_item_text_bonus),
      (else_try),
		(eq,":item_no","itm_crebain_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+3 to Spotting"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
		(eq,":item_no","itm_miruvor_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Athletics"),(set_trigger_result, color_item_text_bonus),(try_end),
      (else_try),
	  (eq,":item_no","itm_isen_uruk_heavy_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Charisma"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@when equipped"),(try_end),
		(set_trigger_result, color_item_text_bonus),
		(else_try),
		(eq,":item_no","itm_leather_gloves_reward"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@+1 to Power Draw"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@when equipped"),(try_end),
		(set_trigger_result, color_item_text_bonus),
      (else_try),
	  (eq,":item_no","itm_beorn_chief"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@Less Beorning upkeep"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@when equipped"),(try_end),
		(set_trigger_result, color_item_text_bonus),
      (else_try),
	   (eq,":item_no","itm_dun_berserker"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@Less Dunnish upkeep"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@when equipped"),(try_end),
		(set_trigger_result, color_item_text_bonus),
      (else_try),
	  (eq,":item_no","itm_gundabad_helm_e"),
		(try_begin),(eq, ":extra_text_id", 0),(set_result_string, "@Less Wargs upkeep"),(try_end),
		(try_begin),(eq, ":extra_text_id", 1),(set_result_string, "@when equipped"),(try_end),
		(set_trigger_result, color_item_text_bonus),
      (else_try),
		#(store_and,reg20,":itp", itp_food), (neq, reg20,0),
		#(eq,":itp", itp_food), 
        (is_between, ":item_no", food_begin, food_end),
        (try_begin),
          (eq, ":extra_text_id", 0),
          (assign, ":continue", 1),
          (try_begin),
            (eq, ":item_no", "itm_cattle_meat"),
            (eq, ":item_modifier", imod_rotten),
            (assign, ":continue", 0),
          (try_end),
          (eq, ":continue", 1),
          (item_get_slot, ":food_bonus", ":item_no", slot_item_food_bonus),
          (assign, reg1, ":food_bonus"),
          (set_result_string, "@+{reg1} to Party Morale"),
          (set_trigger_result, color_item_text_morale),
        (try_end),
      (try_end),
]),

#script_game_on_disembark:
# This script is called from the game engine when the player reaches the shore with a ship.
# INPUT: pos0 = disembark position
("game_on_disembark",
   [(question_box,"@Do you want to disembark?"),
#   (jump_to_menu, "mnu_disembark"),
]),

#script_game_context_menu_get_buttons:
# This script is called from the game engine when the player clicks the right mouse button over a party on the map.
# INPUT: arg1 = party_no
# OUTPUT: none, fills the menu buttons
("game_context_menu_get_buttons",
   [(store_script_param, ":party_no", 1),
    (try_begin),
      (neq, ":party_no", "p_main_party"),
      (context_menu_add_item, "@Move here", cmenu_move),
    (try_end),
    (try_begin),
      (is_between, ":party_no", centers_begin, centers_end),
      (context_menu_add_item, "@View notes", 1),
    (else_try),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (gt, ":num_stacks", 0),
      (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
      (is_between, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
      (context_menu_add_item, "@View notes", 2),
    (try_end),
    #MV debug stuff
    (try_begin),
      (eq, cheat_switch, 1),
      (call_script, "script_party_calculate_strength", ":party_no", 0),
      (context_menu_add_item, "@Debug str: {reg0}", 3),
    (try_end),
]),

#script_game_event_context_menu_button_clicked:
# This script is called from the game engine when the player clicks on a button at the right mouse menu.
# INPUT: arg1 = party_no, arg2 = button_value
("game_event_context_menu_button_clicked",
   [(store_script_param, ":party_no", 1),
    (store_script_param, ":button_value", 2),
    (try_begin),
      (eq, ":button_value", 1),
      (change_screen_notes, 3, ":party_no"),
    (else_try),
      (eq, ":button_value", 2),
      (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
      (change_screen_notes, 1, ":troop_no"),
    (try_end),
]),

#script_game_get_skill_modifier_for_troop
# This script is called from the game engine when a skill's modifiers are needed  
#  Mtarini: added magic item effects
#  GA: added wounds effect
# INPUT: arg1 = troop_no, arg2 = skill_no
# OUTPUT: trigger_result = modifier_value
("game_get_skill_modifier_for_troop",[
    (store_script_param, ":troop_no", 1),
    (store_script_param, ":skill_no", 2),
	(troop_get_slot, ":wound_mask", ":troop_no", slot_troop_wound_mask),
    (assign, ":modifier_value", 0),
    (try_begin), #Pathfinding
   	  (eq, ":skill_no", "skl_pathfinding"),
	  (try_begin),
	    (call_script, "script_get_troop_item_amount", ":troop_no", "itm_map"),
	    (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
	  (try_end),
	  (try_begin),
        	(store_and, ":check" ,":wound_mask", wound_head), #head injury
		(neq, ":check", 0),
		(val_sub, ":modifier_value", 1),
	  (try_end),
	(else_try), #Riding
  	  (eq, ":skill_no", "skl_riding"),
	  (try_begin),
	    (call_script, "script_get_troop_item_amount", ":troop_no", "itm_rohan_saddle"),
	    (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
	  (try_end),
	  (try_begin),
        (store_and, ":check" ,":wound_mask", wound_leg), #leg injury
		(neq, ":check", 0),
        (val_sub, ":modifier_value", 1),
	  (try_end),
	  (try_begin),
	    #dwarf MEANS no riding skills (mtarini) and no mounted archery
		(troop_get_type, ":race", ":troop_no"),
		(eq, ":race", tf_dwarf),
		(assign, ":modifier_value", -10),
	  (try_end),
	(else_try), #Power Draw
  	  (eq, ":skill_no", "skl_power_draw"),
	  (try_begin),
	    (call_script, "script_get_troop_item_amount", ":troop_no", "itm_elven_amulet_reward"),
	    (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
	  (try_end),
	   (try_begin),
	    (troop_has_item_equipped, ":troop_no", "itm_leather_gloves_reward"),
	    (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
	  (try_end), 
	  (try_begin),
        (store_and, ":check" ,":wound_mask", wound_arm), #arm injury
		(neq, ":check", 0),
        (val_sub, ":modifier_value", 1),
	  (try_end),
	(else_try), #Trainer
  	  (eq, ":skill_no", "skl_trainer"),
	  (try_begin),
	    (call_script, "script_get_troop_item_amount", ":troop_no", "itm_angmar_whip_reward"),
	    (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
	  (try_end),
	  (try_begin),
        (store_and, ":check" ,":wound_mask", wound_head), #head injury
		(neq, ":check", 0),
        (val_sub, ":modifier_value", 1),
	  (try_end),
    (else_try), #First Aid
      (eq, ":skill_no", "skl_first_aid"),
      (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_harad_totem_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
      (try_end),
	  (try_begin),
        (store_and, ":check" ,":wound_mask", wound_head), #head injury
		(neq, ":check", 0),
        (val_sub, ":modifier_value", 1),
	  (try_end),
	  (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_athelas_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
	  (try_end),
    (else_try), #Surgery
      (eq, ":skill_no", "skl_surgery"),
	  (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_harad_totem_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
	  (try_end),
	  (try_begin),
        (store_and, ":check" ,":wound_mask", wound_head), #head injury
		(neq, ":check", 0),
        (val_sub, ":modifier_value", 1),
	  (try_end),
    (else_try), #Athletics
      (eq, ":skill_no", "skl_athletics"),
      (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_orc_brew"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
      (try_end),
	  (try_begin),
	    (call_script, "script_get_troop_item_amount", ":troop_no", "itm_miruvor_reward"),
	    (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
	  (try_end),
	  (try_begin),
        (store_and, ":check" ,":wound_mask", wound_leg), #leg injury
		(neq, ":check", 0),
        (val_sub, ":modifier_value", 1),
	  (try_end),
    (else_try), #Tactics
      (eq, ":skill_no", "skl_tactics"),
      (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_explosive_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
      (try_end),
	  (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_scroll_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
      (try_end),
	  (try_begin),
        (store_and, ":check" ,":wound_mask", wound_head), #head injury
		(neq, ":check", 0),
        (val_sub, ":modifier_value", 1),
	  (try_end),
    (else_try), #Power Strike
      (eq, ":skill_no", "skl_power_strike"),
      (try_begin),
        (troop_has_item_equipped, ":troop_no", "itm_westernesse1h_reward"),
        (val_add, ":modifier_value", 1),
      (try_end),
      (try_begin),
        (troop_has_item_equipped, ":troop_no", "itm_westernesse2h_reward"),
        (val_add, ":modifier_value", 1),
      (try_end),
      (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_torque_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
      (try_end),
	  (try_begin),
        (store_and, ":check" ,":wound_mask", wound_arm), #arm injury
		(neq, ":check", 0),
        (val_sub, ":modifier_value", 1),
	  (try_end),
    (else_try), #Weapon Master
      (eq, ":skill_no", "skl_weapon_master"),
	  (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_hammer_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
	  (try_end),
    (else_try), #Wound Treatment	
  	 (eq, ":skill_no", "skl_wound_treatment"),	
 	 (try_begin),
	    (call_script, "script_get_troop_item_amount", ":troop_no", "itm_garlic_reward"),
	    (gt, reg0, 0),
            (val_add, ":modifier_value", 1),
	 (try_end),
 	 (try_begin),
	    (call_script, "script_get_troop_item_amount", ":troop_no", "itm_herbarium_reward"),
	    (gt, reg0, 0),
            (val_add, ":modifier_value", 1),
	 (try_end),
	(try_begin),
        	(store_and, ":check" ,":wound_mask", wound_head), #head injury
		(neq, ":check", 0),
        	(val_sub, ":modifier_value", 1),
	(try_end),
    (else_try), #Leadership
      (eq, ":skill_no", "skl_leadership"), # cumulative
      (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_silmarillion_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
      (try_end),
      (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_horn_gondor_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
      (try_end),
      (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_khand_knife_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
      (try_end),
      (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_phial_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
      (try_end),
    (else_try), #Persuasion
  	  (eq, ":skill_no", "skl_persuasion"),
 	  (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_phial_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 1),
	  (try_end),
    (else_try), #Ironflesh
  	  (eq, ":skill_no", "skl_ironflesh"),
 	  (try_begin),
        (troop_has_item_equipped, ":troop_no", "itm_witchking_helmet"),
        (val_add, ":modifier_value", 1),
	  (try_end),
    (else_try), #Prisoner management
  	  (eq, ":skill_no", "skl_prisoner_management"),
 	  (try_begin),
        (troop_has_item_equipped, ":troop_no", "itm_witchking_helmet"),
        (val_add, ":modifier_value", 1),
	  (try_end),
    (else_try), #Engineering
  	  (eq, ":skill_no", "skl_engineer"),
	  (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_explosive_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 2),
	  (try_end),
	  (try_begin),
        (store_and, ":check" ,":wound_mask", wound_head), #head injury
		(neq, ":check", 0),
        (val_sub, ":modifier_value", 1),
	  (try_end),
    (else_try), #Spotting
  	  (eq, ":skill_no", "skl_spotting"),
	  (try_begin),
        (call_script, "script_get_troop_item_amount", ":troop_no", "itm_crebain_reward"),
        (gt, reg0, 0),
        (val_add, ":modifier_value", 3),
	  (try_end),
	  (try_begin),
        (store_and, ":check" ,":wound_mask", wound_head), #head injury
		(neq, ":check", 0),
        (val_sub, ":modifier_value", 1),
	  (try_end),
    (else_try), #Spotting
  	  (eq, ":skill_no", "skl_horse_archery"),
      (try_begin),
	    #dwarf MEANS no mounted archery (GA)
		(troop_get_type, ":race", ":troop_no"),
		(eq, ":race", tf_dwarf),
		(assign, ":modifier_value", -10),
	  (try_end),
	(try_end),
	
		
	(try_begin),
		(eq,"$disable_skill_modifiers",1),
		(set_trigger_result, 0),
	(else_try),
		(set_trigger_result, ":modifier_value"),
    (try_end),
]),

# Note to modders: Uncomment these if you'd like to use the following.
#script_game_check_party_sees_party
# This script is called from the game engine when a party is inside the range of another party
# INPUT: arg1 = party_no_seer, arg2 = party_no_seen
# OUTPUT: trigger_result = true or false (1 = true, 0 = false)
("game_check_party_sees_party",
	[(store_script_param, ":party_no_seer", 1),
	(store_script_param, ":party_no_seen", 2),
	(try_begin),
		(eq, ":party_no_seer", "p_main_party"), 
		(neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
		(party_get_skill_level, ":spot", "p_main_party", "skl_spotting"),
		(lt,":spot",7), # rangers are invis unless high spotting
		(party_get_template_id,":spot",":party_no_seen"),
		(this_or_next|eq, ":spot", "pt_ranger_scouts"),# evil player does not see rangers x_x
		(this_or_next|eq, ":spot", "pt_ranger_raiders"),
		(eq, ":party_no_seen", "p_town_henneth_annun"),# evil player does not see henneth
		(set_trigger_result, 0),
	(else_try),
		(set_trigger_result, 1),
	(try_end),
]),

##script_game_get_party_speed_multiplier
## This script is called from the game engine when a skill's modifiers are needed
## INPUT: arg1 = party_no
## OUTPUT: trigger_result = multiplier (scaled by 100, meaning that giving 100 as the trigger result does not change the party speed)
#("game_get_party_speed_multiplier",[
#   (store_script_param, ":party_no", 1),
#   (set_trigger_result, 100),
#]),

#script_setup_talk_info
# INPUT: $g_talk_troop, $g_talk_troop_relation, $current_town (TLD)
("setup_talk_info",
    [ (try_begin),
        (is_between, "$g_talk_troop", mayors_begin, mayors_end),
        (party_slot_eq, "$current_town", slot_town_elder, "$g_talk_troop"), #redundant, but doesn't hurt
        (party_get_slot, ":relation", "$current_town", slot_center_player_relation),
        (str_store_party_name, s61, "$current_town"),
      (else_try),
        (assign, ":relation", "$g_talk_troop_relation"),
        (str_store_troop_name, s61, "$g_talk_troop"),
      (try_end),
      (talk_info_set_relation_bar, ":relation"),
      (str_store_string, s61, "@ {s61}"),
      (assign, reg1, ":relation"),
      (str_store_string, s62, "str_relation_reg1"),
      (talk_info_set_line, 0, s61),
      (talk_info_set_line, 1, s62),
      (call_script, "script_describe_relation_to_s63", ":relation"),
      (talk_info_set_line, 3, s63),
]),

#script_setup_talk_info_companions
("setup_talk_info_companions",
    [ (call_script, "script_npc_morale", "$g_talk_troop"),
      (assign, ":troop_morale", reg0),
      (talk_info_set_relation_bar, ":troop_morale"),
      (str_store_troop_name, s61, "$g_talk_troop"),
      (str_store_string, s61, "@ {s61}"),
      (assign, reg1, ":troop_morale"),
      (str_store_string, s62, "str_morale_reg1"),
      (talk_info_set_line, 0, s61),
      (talk_info_set_line, 1, s62),
      (talk_info_set_line, 3, s63),
]),

#script_update_party_creation_random_limits
# INPUT: none
("update_party_creation_random_limits",
    [ (store_character_level, ":player_level", "trp_player"),
      (store_mul, ":upper_limit", ":player_level", 3),
      (val_add, ":upper_limit", 25),
      (val_min, ":upper_limit", 100),
      (set_party_creation_random_limits, 0, ":upper_limit"),
      (assign, reg0, ":upper_limit"),
]),

#script_set_trade_route_between_centers
# INPUT: param1: center_no_1, param2: center_no_2
("set_trade_route_between_centers",
    [(store_script_param, ":center_no_1", 1),
     (store_script_param, ":center_no_2", 2),
     (assign, ":center_1_added", 0),
     (assign, ":center_2_added", 0),
     (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
       (try_begin),
         (eq, ":center_1_added", 0),
         (party_slot_eq, ":center_no_1", ":cur_slot", 0),
         (party_set_slot, ":center_no_1", ":cur_slot", ":center_no_2"),
         (assign, ":center_1_added", 1),
       (try_end),
       (try_begin),
         (eq, ":center_2_added", 0),
         (party_slot_eq, ":center_no_2", ":cur_slot", 0),
         (party_set_slot, ":center_no_2", ":cur_slot", ":center_no_1"),
         (assign, ":center_2_added", 1),
       (try_end),
     (try_end),
     (try_begin),
       (eq, ":center_1_added", 0),
       (str_store_party_name, s1, ":center_no_1"),
       (display_message, "@ERROR: More than 15 trade routes are given for {s1}."),
     (try_end),
     (try_begin),
       (eq, ":center_2_added", 0),
       (str_store_party_name, s1, ":center_no_2"),
       (display_message, "@ERROR: More than 15 trade routes are given for {s1}."),
     (try_end),
]),

#script_center_change_trade_good_production
# INPUT: param1 = center_no, param2 = item_id, param3 = production_rate (should be between -100 (for net consumption) and 100 (for net production)
# param4: randomness (between 0-100)
("center_change_trade_good_production",[
      (store_script_param, ":center_no", 1),
      (store_script_param, ":item_no", 2),
      (store_script_param, ":production_rate", 3),
#      (val_mul, ":production_rate", 5),
      (store_script_param, ":randomness", 4),
      (store_random_in_range, ":random_num", 0, ":randomness"),
      (store_random_in_range, ":random_sign", 0, 2),
      (try_begin),
        (eq, ":random_sign", 0),
        (val_add, ":production_rate", ":random_num"),
      (else_try),
        (val_sub, ":production_rate", ":random_num"),
      (try_end),
      (val_sub, ":item_no", trade_goods_begin),
      (val_add, ":item_no", slot_town_trade_good_productions_begin),
      (party_get_slot, ":old_production_rate", ":center_no", ":item_no"),
      (val_add, ":production_rate", ":old_production_rate"),
      (party_set_slot, ":center_no", ":item_no", ":production_rate"),
]),

#script_average_trade_good_productions
# INPUT: none
("average_trade_good_productions",[
      (store_sub, ":item_to_slot", slot_town_trade_good_productions_begin, trade_goods_begin),
#      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD - not destroyed
        (try_for_range, ":other_center", centers_begin, centers_end),
          (party_is_active, ":other_center"), #TLD
          (party_slot_eq, ":other_center", slot_center_destroyed, 0), #TLD - not destroyed
          (is_between, ":center_no", centers_begin, centers_end),
          (neq, ":other_center", ":center_no"),
          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":other_center"),
          (lt, ":cur_distance", 110),
          (store_sub, ":dist_factor", 110, ":cur_distance"),
          (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
            (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
            (party_get_slot, ":other_center_production", ":other_center", ":cur_good_slot"),
            (store_sub, ":prod_dif", ":center_production", ":other_center_production"),
            (gt, ":prod_dif", 0),
            (store_mul, ":prod_dif_change", ":prod_dif", 1),
##            (try_begin),
##              (is_between, ":center_no", centers_begin, centers_end),
##              (is_between, ":other_center", centers_begin, centers_end),
##              (val_mul, ":cur_distance", 2),
##            (try_end),
            (val_mul ,":prod_dif_change", ":dist_factor"),
            (val_div ,":prod_dif_change", 110),
            (val_add, ":other_center_production", ":prod_dif_change"),
            (party_set_slot, ":other_center", ":cur_good_slot", ":other_center_production"),
          (try_end),
        (try_end),
      (try_end),
]),

#script_normalize_trade_good_productions
# INPUT: none
("normalize_trade_good_productions", [
      (store_sub, ":item_to_slot", slot_town_trade_good_productions_begin, trade_goods_begin),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (assign, ":total_production", 0),
        (assign, ":num_centers", 0),
        (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_is_active, ":center_no"), #TLD
          (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD - not destroyed
          (val_add, ":num_centers", 1),
          (try_begin),
            (is_between, ":center_no", centers_begin, centers_end), #each town is weighted as 5 villages...
            (val_add, ":num_centers", 4), 
          (try_end),
          (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
          (val_add, ":total_production", ":center_production"),
        (try_end),
        (store_div, ":new_production_difference", ":total_production", ":num_centers"),
        (neq, ":new_production_difference", 0),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_is_active, ":center_no"), #TLD
          (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD - not destroyed
          (is_between, ":center_no", centers_begin, centers_end),
          (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
          (val_sub, ":center_production", ":new_production_difference"),
          (party_set_slot, ":center_no", ":cur_good_slot", ":center_production"),
        (try_end),
      (try_end),
]),

#script_do_merchant_town_trade
# INPUT: arg1 = party_no (of the merchant), arg2 = center_no
("do_merchant_town_trade",[
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":center_no"),
      (call_script, "script_do_party_center_trade", ":party_no", ":center_no", 20), #change prices by 20%
      
      (assign, ":total_change", reg0),
      #Adding the earnings to the wealth (maximum changed price is the earning)
      (val_div, ":total_change", 2),
      (str_store_party_name, s1, ":party_no"),
      (str_store_party_name, s2, ":center_no"),
      (assign, reg1, ":total_change"),
##      (try_begin),
##        (eq, "$cheat_mode", 1),
##        (display_message, "@Merchant {s1} traded with {s2} and earned {reg1} denars."),
##      (try_end),

      #Adding tax revenue to the center
      (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
      (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
      (store_add, ":tax_gain", ":prosperity", 10),
      (val_mul, ":tax_gain", ":total_change"),
      (val_div, ":tax_gain", 2200), #(10 + prosperity) / 110 * 5% of the merchant's revenue.
      (val_add, ":accumulated_tariffs", ":tax_gain"),
      (party_set_slot, ":center_no", slot_center_accumulated_tariffs, ":accumulated_tariffs"),
      
#      (try_begin),
#        (is_between, ":center_no", centers_begin, centers_end),
#        (party_get_slot, ":merchant",":center_no",slot_town_merchant),
#        (gt, ":merchant", 0),
#        (store_mul, ":merchant_profit", ":total_change", 1),
#        (val_div, ":merchant_profit", 2),
#        (troop_add_gold, ":merchant", ":merchant_profit"),
#      (try_end),

      #Adding 1 to center prosperity
      (try_begin),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 35),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (try_end),
]),

#script_troop_calculate_strength:
# INPUT: arg1 = troop_id
# OUTPUT: reg0 = strength
("troop_calculate_strength",
    [ (store_script_param_1, ":troop"),
      #TLD: Troop strength = ((level+11)^2-27)/100
      (store_character_level, reg0, ":troop"),
      (val_add, reg0, 11),
      (val_mul, reg0, reg0),
      (val_sub, reg0, 27),
      (val_div, reg0, 100),
	  #(troop_get_type,":troop",":troop"),
	  #(try_begin),(eq, ":troop", tf_orc),(val_div, reg0, 2),(try_end), #GA: plain orcs get strength halved - MV: NO. They already have lower strength because of their levels - see below how low-tier orcs are inferior. If you want orc parties to be weaker in AI battles, change their party templates to have less high-tier and more low-tier troops. And do the math to make sure you don't go too far.
      # Here's the output
      # Humans (tiers 1-7): 2,4,6, 9,16,25,31 (Uruks use these too)
      # Elves (T1-6):       2,5,7,10,19,29
      # Dwarves (T1-6):     2,4,7, 9,18,28
      # Orcs (T1-6):        1,3,5, 8,14,22
]),

#script_party_calculate_regular_strength:
# INPUT: arg1 = party_id
# OUTPUT: reg0 = strength
("party_calculate_regular_strength",
    [ (store_script_param_1, ":party"), #Party_id
      (assign, ":strength", 0),
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (call_script, "script_troop_calculate_strength", ":stack_troop"),
        (assign, ":stack_strength", reg0),
        (party_stack_get_size, ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_mul, ":stack_strength", ":stack_size"),
        (val_add, ":strength", ":stack_strength"),
      (try_end),
      # Evil handicap when evil player
      (try_begin),
        (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
        (store_faction_of_party, ":party_faction", ":party"),
        (neg|faction_slot_eq, ":party_faction", slot_faction_side, faction_side_good),
        (val_mul, ":strength", evil_party_str_handicap),
        (val_div, ":strength", 100),
      (try_end),
      (assign, reg0, ":strength"),
]),

#script_party_calculate_strength:
# INPUT: arg1 = party_id, arg2 = exclude leader
# OUTPUT: reg0 = strength
("party_calculate_strength",
    [ (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":exclude_leader"), #Party_id
      (assign, ":strength", 0),
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, ":first_stack", 0),
      (try_begin),
        (neq, ":exclude_leader", 0),
        (assign, ":first_stack", 1),
      (try_end),
      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (call_script, "script_troop_calculate_strength", ":stack_troop"),
        (assign, ":stack_strength", reg0),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":stack_size", ":num_wounded"),
          (val_mul, ":stack_strength", ":stack_size"),
        (else_try),
          (troop_is_wounded, ":stack_troop"), #hero...
          (assign,":stack_strength",0),
        (try_end),
        (val_add, ":strength", ":stack_strength"),
      (try_end),
      (party_set_slot, ":party", slot_party_cached_strength, ":strength"),
      # Evil handicap when evil player
      (try_begin),
        (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
        (store_faction_of_party, ":party_faction", ":party"),
        (neg|faction_slot_eq, ":party_faction", slot_faction_side, faction_side_good),
        (val_mul, ":strength", evil_party_str_handicap),
        (val_div, ":strength", 100),
      (try_end),
      (assign, reg0, ":strength"),
]),

#script_loot_player_items:
# INPUT: arg1 = enemy_party_no
("loot_player_items",
    [ (store_script_param, ":enemy_party_no", 1),
      (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
        (ge, ":item_id", 0),
        (troop_get_inventory_slot_modifier, ":item_modifier", "trp_player", ":i_slot"),
# all items looted with max probability. No easy life :) GA
#        (try_begin),
#          (is_between, ":item_id", trade_goods_begin, trade_goods_end),
          (assign, ":randomness", 20),
#        (else_try),
#          (is_between, ":item_id", horses_begin, horses_end),
#          (assign, ":randomness", 15),
#        (else_try),
#          (this_or_next|is_between, ":item_id", weapons_begin, weapons_end),
#          (is_between, ":item_id", ranged_weapons_begin, ranged_weapons_end),
#          (assign, ":randomness", 5),
#        (else_try),
#          (this_or_next|is_between, ":item_id", armors_begin, armors_end),
#          (is_between, ":item_id", shields_begin, shields_end),
#          (assign, ":randomness", 5),
#        (try_end),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":randomness"),
        (troop_remove_item, "trp_player", ":item_id"),

        (try_begin),
          (gt, ":enemy_party_no", 0),
          (party_get_slot, ":cur_loot_slot", ":enemy_party_no", slot_party_next_looted_item_slot),
          (val_add, ":cur_loot_slot", slot_party_looted_item_1),
          (party_set_slot, ":enemy_party_no", ":cur_loot_slot", ":item_id"),
          (val_sub, ":cur_loot_slot", slot_party_looted_item_1),
          (val_add, ":cur_loot_slot", slot_party_looted_item_1_modifier),
          (party_set_slot, ":enemy_party_no", ":cur_loot_slot", ":item_modifier"),
          (val_sub, ":cur_loot_slot", slot_party_looted_item_1_modifier),
          (val_add, ":cur_loot_slot", 1),
          (val_mod, ":cur_loot_slot", num_party_loot_slots),
          (party_set_slot, ":enemy_party_no", slot_party_next_looted_item_slot, ":cur_loot_slot"),
        (try_end),
      (try_end),
      (store_troop_gold, ":cur_gold", "trp_player"),
      (store_div, ":max_lost", ":cur_gold", 4),
      (store_div, ":min_lost", ":cur_gold", 10),
      (store_random_in_range, ":lost_gold", ":min_lost", ":max_lost"),
      (troop_remove_gold, "trp_player", ":lost_gold"),
]),

#script_party_calculate_loot:
# INPUT: param1: Party-id
# Returns num looted items in reg(0)
("party_calculate_loot",
    [ (store_script_param_1, ":enemy_party"), #Enemy Party_id
	  (faction_get_slot, ":faction_mask", "$players_kingdom", slot_faction_mask),
      (call_script, "script_calculate_main_party_shares"),(assign, ":num_player_party_shares", reg0),
      #      (assign, ":num_ally_shares", reg1),
      #      (store_add, ":num_shares",  ":num_player_party_shares", ":num_ally_shares"),
      
      #Calculate player loot probability
      #      (assign, ":loot_probability", 100),
      #      (val_mul, ":loot_probability", 10),
      #      (val_div, ":loot_probability", ":num_shares"),

	  (assign, ":can_steal", 1),  # can steal objects of own faction or , of no faction
	  (try_begin), (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good), (assign, ":can_steal", 0),(try_end), # good guys don't steal
      # Loot the defeated party
      (store_mul, ":loot_probability", player_loot_share, 3),
      (val_mul, ":loot_probability", "$g_strength_contribution_of_player"),
      (party_get_skill_level, ":player_party_looting", "p_main_party", "skl_looting"),
      (val_add, ":player_party_looting", 10),
      (val_mul, ":loot_probability", ":player_party_looting"),
      (val_div, ":loot_probability", 10),
      (val_div, ":loot_probability", ":num_player_party_shares"),

	  (assign, ":dest", "trp_temp_troop"), #(try_begin),(eq,"$tld_option_crossdressing", 0),(assign, ":dest", "trp_temp_troop_2"),(try_end),
	  (troop_clear_inventory,"trp_temp_troop"),

      (party_get_num_companion_stacks, ":num_stacks",":enemy_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":enemy_party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":enemy_party",":i_stack"),
        (try_for_range, ":unused", 0, ":stack_size"),
          (troop_loot_troop,":dest",":stack_troop",":loot_probability"),
        (try_end),
      (try_end),
	  
	  #  substitute forbidden items  with "metal scraps"   (mtarini)
	  # ##################################
	  (try_begin),

	  (eq,"$tld_option_crossdressing", 0),

		(call_script,"script_troop_copy_all_items_from_troop", "trp_temp_troop_2","trp_temp_troop"),
	  
	    (troop_clear_inventory,"trp_temp_troop"),
		(troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop_2"),
		
		#(assign, reg10, ":inv_cap"), (display_message,"@debug: starting scrapization over {reg10} objects..."),
		
		(try_for_range, ":i_slot", 0, ":inv_cap"),
			(troop_get_inventory_slot, ":item_id", "trp_temp_troop_2", ":i_slot"),
			(ge, ":item_id", 0),
			#(display_message,"@debug: non zero obj..."),
			(try_begin),
				(item_get_type, ":it", ":item_id"),
				(eq, ":it", itp_type_horse),
				(try_begin),
					(troop_get_type, ":race","$g_player_troop"),
					(is_between, ":race", tf_orc_begin, tf_orc_end), # orcs:
					(try_begin),
						(is_between, ":item_id", item_warg_begin , item_warg_end),
						(troop_add_item, "trp_temp_troop", ":item_id"), # keep any warg
					(else_try),
						(troop_add_item, "trp_temp_troop", "itm_horse_meat"), # turn any horse in meat
					(try_end),
				(else_try),
					# non orcs: 
					(try_begin),
						(is_between, ":item_id", item_warg_begin , item_warg_end), # trash any warg
					(else_try),
						(troop_add_item, "trp_temp_troop", ":item_id"), # keep any horse
					(try_end),
				(try_end),
			(else_try),
				(eq, ":can_steal", 1), # if can steal...
				(item_get_slot, reg10,  ":item_id", slot_item_faction),
				(store_and, reg11, reg10, ":faction_mask"),
				(this_or_next|eq, reg10, 0), # can steal objects with no faction
				(neq, reg11, 0), # can steal objects of player's faction
				# don't replace item
				(troop_add_item, "trp_temp_troop", ":item_id"),
			(else_try),
				# replace item with scrap
				#(store_random_in_range, ":rand", 0, 100), (ge, ":rand", 75),
				(store_item_value, ":val", ":item_id"),
				
				(assign, reg20, ":val"),
				(str_store_item_name,s20,":item_id"),
				
				# random rounding of values (so that average total values is kept the same)
				(assign, ":rounding", 0),
				(try_begin), (lt,":val",scrap_bad_value),   (store_random_in_range, ":rounding", 0, scrap_bad_value),
				(else_try),  (lt,":val",scrap_medium_value),(store_random_in_range, ":rounding", 0, scrap_medium_value - scrap_bad_value),
				(else_try),  (lt,":val",scrap_good_value),  (store_random_in_range, ":rounding", 0, scrap_good_value - scrap_medium_value),
				(try_end),
				(val_add, ":val", ":rounding"), 
				(assign, reg21, ":rounding"),
				
				(str_store_string, s22, "@nothing"),
				(try_begin),(ge,":val",scrap_good_value),   (troop_add_item, "trp_temp_troop", "itm_metal_scraps_good"),  (str_store_string,s22,"@Good"),
				(else_try), (ge,":val",scrap_medium_value), (troop_add_item, "trp_temp_troop", "itm_metal_scraps_medium"),(str_store_string,s22,"@Med"),
				(else_try), (ge,":val",scrap_bad_value),    (troop_add_item, "trp_temp_troop", "itm_metal_scraps_bad"),   (str_store_string,s22,"@Bad"),
				(try_end),
				#(display_message,"@debug: turned a {s20} {reg20} (+{reg21}) into {reg22}..."),
			(try_end),	  
		(try_end),	  
      (try_end),	  
	  
	  # adding any special loot from party "looted item" slots (item that where stolen by the party)
      (try_for_range, ":i_loot", 0, num_party_loot_slots),
        (store_add, ":cur_loot_slot", ":i_loot", slot_party_looted_item_1),
        (party_get_slot, ":item_no", "$g_enemy_party", ":cur_loot_slot"),
        (gt, ":item_no", 0),
        (party_set_slot, "$g_enemy_party", ":cur_loot_slot", 0),
        (val_sub, ":cur_loot_slot", slot_party_looted_item_1),
        (val_add, ":cur_loot_slot", slot_party_looted_item_1_modifier),
        (party_get_slot, ":item_modifier", "$g_enemy_party", ":cur_loot_slot"),
        (troop_add_item, "trp_temp_troop", ":item_no", ":item_modifier"),
      (try_end),
      (party_set_slot, "$g_enemy_party", slot_party_next_looted_item_slot, 0),
	# put "goods" in loot if it was a caravan (or farmers)
      (assign, ":num_looted_items",0),
      (try_begin),
        (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
        (store_mul, ":plunder_amount", player_loot_share, 30),
        (val_mul, ":plunder_amount", "$g_strength_contribution_of_player"),
        (val_div, ":plunder_amount", 100),
        (val_div, ":plunder_amount", ":num_player_party_shares"),
        (try_begin),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
		   #  (val_clamp, ":plunder_amount", 1, 50),
          (reset_item_probabilities, 100),
          (assign, ":range_min", trade_goods_begin),
          (assign, ":range_max", trade_goods_end),
        (else_try),
          (val_div, ":plunder_amount", 5),
		  #(val_clamp, ":plunder_amount", 1, 10),
          (reset_item_probabilities, 1),
          (assign, ":range_min", normal_food_begin),
          (assign, ":range_max", food_end),
        (try_end),
        (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
        (try_for_range, ":cur_goods", ":range_min", ":range_max"),
          (store_add, ":cur_price_slot", ":cur_goods", ":item_to_price_slot"),
          (party_get_slot, ":cur_price", "$g_enemy_party", ":cur_price_slot"),
          (assign, ":cur_probability", 100),
          (val_mul, ":cur_probability", average_price_factor),
          (val_div, ":cur_probability", ":cur_price"),
          (val_mul, ":cur_probability", average_price_factor),
          (val_div, ":cur_probability", ":cur_price"),
          (val_mul, ":cur_probability", average_price_factor),
          (val_div, ":cur_probability", ":cur_price"),
          #(assign, reg0, ":cur_probability"),
          (set_item_probability_in_merchandise, ":cur_goods", ":cur_probability"),
        (try_end),
        (troop_add_merchandise, "trp_temp_troop", itp_type_goods, ":plunder_amount"),
        #(assign, reg5, ":plunder_amount"),
        (val_add, ":num_looted_items", ":plunder_amount"),
      (try_end),
	# count how many objects were accumulated in total
      (troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
        (ge, ":item_id", 0),
        (val_add, ":num_looted_items",1),
      (try_end),

      (assign, reg0, ":num_looted_items"),
]),

#script_calculate_main_party_shares:
# Returns number of player party shares in reg0
("calculate_main_party_shares",
    [ (assign, ":num_player_party_shares",player_loot_share),
      # Add shares for player's party
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
          (val_add, ":num_player_party_shares", ":stack_size"),
        (else_try),
          (val_add, ":num_player_party_shares", hero_loot_share),
        (try_end),
      (try_end),
      (assign, reg0, ":num_player_party_shares"),
]),

#script_party_give_xp_and_gold:
# INPUT: param1: destroyed Party-id
# calculates and gives player paty's share of gold and xp.
("party_give_xp_and_gold",
    [ (store_script_param_1, ":enemy_party"), #Party_id
      (call_script, "script_calculate_main_party_shares"),
      (assign, ":num_player_party_shares", reg0),
      #      (assign, ":num_ally_shares", reg1),
      #     (store_add, ":num_total_shares",  ":num_player_party_shares", ":num_ally_shares"),
      (assign, ":total_gain", 0),
      (party_get_num_companion_stacks, ":num_stacks",":enemy_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":enemy_party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":enemy_party",":i_stack"),
        (store_character_level, ":level", ":stack_troop"),
        (store_add, ":gain", ":level", 10),
        (val_mul, ":gain", ":gain"),
        (val_div, ":gain", 10),
        (store_mul, ":stack_gain", ":gain", ":stack_size"),
        (val_add, ":total_gain", ":stack_gain"),
      (try_end),
      
      (val_mul, ":total_gain", "$g_strength_contribution_of_player"),
      (val_div, ":total_gain", 100),
      (val_min, ":total_gain", 40000), #eliminate negative results
      #      (store_mul, ":player_party_xp_gain", ":total_gain", ":num_player_party_shares"),
      #      (val_div, ":player_party_xp_gain", ":num_total_shares"),
      (assign, ":player_party_xp_gain", ":total_gain"),
      
      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_party_xp_gain", ":r"),
      (val_div, ":player_party_xp_gain", 100),
      
      (party_add_xp, "p_main_party", ":player_party_xp_gain"),
      
      (store_mul, ":player_gold_gain", ":total_gain", player_loot_share),
      (val_min, ":player_gold_gain", 60000), #eliminate negative results
      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_gold_gain", ":r"),
      (val_div, ":player_gold_gain", 100),
      (val_div, ":player_gold_gain", ":num_player_party_shares"),
      
      #add gold now
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (call_script, "script_troop_add_gold", ":stack_troop", ":player_gold_gain"),
        (try_end),
      (try_end),
   #Add morale
      (assign, ":morale_gain", ":total_gain"),
      (val_div, ":morale_gain", ":num_player_party_shares"),
      (call_script, "script_change_player_party_morale", ":morale_gain"),
]),

#script_setup_troop_meeting:
# INPUT: param1: troop_id with which meeting will be made, param2: troop_dna (optional)
("setup_troop_meeting",
    [ (store_script_param_1, ":meeting_troop"),
      (store_script_param_2, ":troop_dna"),
      (modify_visitors_at_site, "scn_conversation_scene"),
	  (reset_visitors),
      (set_visitor, 0, "trp_player"),

	  (troop_equip_items, ":meeting_troop"),
      (try_begin),
		(this_or_next|eq, ":meeting_troop", "trp_mordor_lord"),
		(eq, ":meeting_troop", "trp_lorien_lord"),
		(set_visitor, 18, ":meeting_troop", ":troop_dna"),
	  (else_try),
		(set_visitor, 17, ":meeting_troop", ":troop_dna"),
      (try_end),
	  (set_jump_mission, "mt_conversation_encounter"),
      (jump_to_scene, "scn_conversation_scene"),
	(change_screen_map_conversation, ":meeting_troop"),
]),

#script_setup_party_meeting:
# INPUT: param1: Party-id with which meeting will be made.
("setup_party_meeting", [
	(store_script_param_1, ":meeting_party"),
	(try_begin), # party_meeting used as an indicator that conversation is with party
		(lt, "$g_encountered_party_relation", 0), #hostile
		(assign,"$party_meeting",-1),
	(else_try),
		(assign,"$party_meeting",1),
		#        (call_script, "script_music_set_situation_with_culture", mtf_sit_encounter_hostile),
	(try_end),

	(modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
	(set_visitor,0,"trp_player"),
	(party_stack_get_troop_id, ":meeting_troop",":meeting_party",0),
	(party_stack_get_troop_dna,":troop_dna",":meeting_party",0),
	(troop_equip_items, ":meeting_troop"),
	(try_begin),
		(this_or_next|eq,":meeting_troop","trp_mordor_lord"),
		(eq,":meeting_troop","trp_lorien_lord"),
		(set_visitor,18,":meeting_troop",":troop_dna"),
	(else_try),
		(set_visitor,17,":meeting_troop",":troop_dna"),
	(try_end),
	(call_script, "script_party_copy", "p_encountered_party_backup", ":meeting_party"),
	(party_remove_members,"p_encountered_party_backup",":meeting_troop",1),
	
	#add company to an opponent talker cf_party_remove_random_regular_troop
	(try_for_range, ":entry", 19, 30),
		(call_script, "script_cf_party_remove_random_regular_troop", "p_encountered_party_backup"),
		(store_random_in_range, ":rnd",1, 100000), # some random faces/equip for background troops
		(set_visitor,":entry",reg0,":rnd"),
	(try_end),
	
	(set_jump_mission,"mt_conversation_encounter"),
	(jump_to_scene,"scn_conversation_scene"),
	(change_screen_map_conversation, ":meeting_troop"),
]),

#script_party_remove_all_companions:
# INPUT:
# param1: Party-id from which  companions will be removed.
# "$g_move_heroes" : controls if heroes will also be removed.
("party_remove_all_companions",
    [ (store_script_param_1, ":party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_companion_stacks",":party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_companion_stacks"),
        (party_stack_get_troop_id,   ":stack_troop",":party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_stack_get_size,  ":stack_size",":party",":stack_no"),
        (party_remove_members, ":party", ":stack_troop",  ":stack_size"),
      (try_end),
]),

#script_party_remove_all_prisoners:
# INPUT: param1: Party-id from which  prisoners will be removed.
# "$g_move_heroes" : controls if heroes will also be removed.
("party_remove_all_prisoners",
    [ (store_script_param_1, ":party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_prisoner_stacks",":party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
        (party_prisoner_stack_get_troop_id,   ":stack_troop",":party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size, ":stack_size",":party",":stack_no"),
        (party_remove_prisoners, ":party", ":stack_troop", ":stack_size"),
      (try_end),
]),

#script_party_add_party_companions:
# INPUT: param1: Party-id to add the second part, param2: Party-id which will be added to the first one.
# "$g_move_heroes" : controls if heroes will also be added.
("party_add_party_companions",
    [ (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_stack_get_size,         ":stack_size",":source_party",":stack_no"),
        (party_add_members, ":target_party", ":stack_troop", ":stack_size"),
        (party_stack_get_num_wounded, ":num_wounded", ":source_party", ":stack_no"),
        (party_wound_members, ":target_party", ":stack_troop", ":num_wounded"),
      (try_end),
]),

#script_party_add_party_prisoners:
# INPUT: param1: Party-id to add the second party, param2: Party-id which will be added to the first one.
# "$g_move_heroes" : controls if heroes will also be added.
# mtarini: in TLD remember to set faction of target party before calling this!
("party_add_party_prisoners",
    [ (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
	  (store_faction_of_party, ":fac_a",":target_party"), # mtarini: store faction of receiving party
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size,         ":stack_size",":source_party",":stack_no"),
	# mtarini for TLD: adding freed prisoners to prisoners or to companinons, according to if they are friend enemies
		(store_troop_faction,":fac_b",":stack_troop"),
		(store_relation, ":rel" ,":fac_a" ,":fac_b"),
		(try_begin),
			(gt, ":rel", 0), # receiving partyis friend with freed prisoner
			(call_script, "script_cf_factions_are_allies", ":fac_b",":fac_a"),
			(party_add_members, ":target_party", ":stack_troop", ":stack_size"), 
		(else_try), # receiving party is enemy with freed prisoners
			(party_add_prisoners, ":target_party", ":stack_troop", ":stack_size"), 
		(try_end),
      (try_end),
]),

#script_party_prisoners_add_party_companions:
# INPUT: param1: Party-id to add the second part, param2: Party-id which will be added to the first one.
# "$g_move_heroes" : controls if heroes will also be added.
("party_prisoners_add_party_companions",
    [ (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (troop_get_type,":race",":stack_troop"),
        (neq,":race",tf_orc),        ## TLD good guys finish all orcs, evil guys finish all elves, GA
        (neq,":race",tf_uruk),
        (neq,":race",tf_urukhai),
        (neq,":race",tf_troll),
        (neq,":race",tf_lorien),
        (neq,":race",tf_imladris),
        (neq,":race",tf_woodelf),
        (party_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_prisoners, ":target_party", ":stack_troop", ":stack_size"),
      (try_end),
]),

#script_party_prisoners_add_party_prisoners:
# INPUT: param1: Party-id to add the second part, param2: Party-id which will be added to the first one.
# "$g_move_heroes" : controls if heroes will also be added.
("party_prisoners_add_party_prisoners",
    [ (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size,         ":stack_size",":source_party",":stack_no"),
        (party_add_prisoners, ":target_party", ":stack_troop", ":stack_size"),
      (try_end),
]),

# script_party_add_party:
# INPUT: param1: Party-id to add the second part, param2: Party-id which will be added to the first one.
# "$g_move_heroes" : controls if heroes will also be added.
("party_add_party",
    [ (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (call_script, "script_party_add_party_companions",          ":target_party", ":source_party"),
      (call_script, "script_party_prisoners_add_party_prisoners", ":target_party", ":source_party"),
]),

#script_party_copy:
# INPUT: param1: Party-id to copy the second party, param2: Party-id which will be copied to the first one.
("party_copy",
    [ (assign, "$g_move_heroes", 1),
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_clear, ":target_party"),
	  (store_faction_of_party, reg10, ":source_party"),
	  (party_set_faction, ":target_party", reg10),
      (call_script, "script_party_add_party", ":target_party", ":source_party"),
]),

#script_clear_party_group:
# INPUT: param1: Party-id of the root of the group.
#        param2: winner faction
# This script will clear the root party and all parties attached to it recursively.
("clear_party_group",
    [ (store_script_param_1, ":root_party"),
      (store_script_param_2, ":winner_faction"),
	  (try_begin),
        (ge, ":root_party", 0), #MV fix for script errors
  #TLD assign faction strength penalties for party destruction, GA
        (store_faction_of_party, ":faction", ":root_party"),
	    (try_begin),
	      (is_between, ":faction", kingdoms_begin, kingdoms_end),
	      (faction_get_slot,":strength",":faction",slot_faction_strength_tmp),
	      (party_get_slot,":party_value", ":root_party",slot_party_victory_value),
	    #(party_get_slot,":party_type", ":root_party",slot_party_type),
#	    (try_begin),
#	      (eq,":party_type",spt_kingdom_hero_party), #hosts dying decrease faction strength unconditionally 
		  (val_sub, ":strength", ":party_value"),
          #debug stuff
          (faction_get_slot, ":debug_loss", ":faction", slot_faction_debug_str_loss),
		  (val_add, ":debug_loss", ":party_value"),
          (faction_set_slot, ":faction", slot_faction_debug_str_loss, ":debug_loss"),
#	    (else_try),
#		  (store_div,":s0",":strength",1000),
#		  (store_sub,":s",":strength",":party_value"),
#		  (val_div,":s",1000),
#		  (eq,":s0",":s"),
#		    (val_sub, ":strength",":party_value"),   # lesser parties dying can't shift faction strength through threshold
#	    (try_end),
	      (faction_set_slot,":faction",slot_faction_strength_tmp,":strength"),  # new strength stored in tmp slot to be processed in a trigger every 2h
          # add half victory points to the winner faction
          (try_begin),
            (neq, "$tld_option_regen_rate", 3), #None - no regen, even from battles
            (is_between, ":winner_faction", kingdoms_begin, kingdoms_end),
            (faction_get_slot,":winner_strength",":winner_faction",slot_faction_strength_tmp),
		    (store_div, ":win_value", ":party_value", 2), #this formula could be balanced after playtesting
		    (val_add, ":winner_strength", ":win_value"),
            (val_min, ":winner_strength", fac_str_max), #limit max strength
	        (faction_set_slot,":winner_faction",slot_faction_strength_tmp,":winner_strength"),
            #debug stuff
            (faction_get_slot, ":debug_gain", ":winner_faction", slot_faction_debug_str_gain),
		    (val_add, ":debug_gain", ":win_value"),
            (faction_set_slot, ":winner_faction", slot_faction_debug_str_gain, ":debug_gain"),
          (try_end),
          #debug
          (try_begin),
            (eq, cheat_switch, 1),
	        (assign,reg0,":party_value"),
	        (assign,reg1,":strength"),
	        (assign,reg2,":win_value"),
	        (assign,reg3,":winner_strength"),
	        (str_store_faction_name,s1,":faction"),
	        (str_store_faction_name,s2,":winner_faction"),
            (try_begin),
              (is_between, ":winner_faction", kingdoms_begin, kingdoms_end),
	          #(display_message,"@DEBUG: {s1} strength -{reg0} to {reg1}, {s2} strength +{reg2} to {reg3}."), #mvdebug
            (else_try),
	          #(display_message,"@DEBUG: {s1} strength -{reg0} to {reg1}, defeat by {s2}."), #mvdebug
            (try_end),
          (try_end),
	    (try_end),
#end TLD
        (party_clear, ":root_party"),
        (party_get_num_attached_parties, ":num_attached_parties", ":root_party"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (party_get_attached_party_with_rank, ":attached_party", ":root_party", ":attached_party_rank"),
          (call_script, "script_clear_party_group", ":attached_party", ":winner_faction"), # TLD bug here: this will give str loss/gain twice in player battles
        (try_end),
	  (try_end),
]),

#script_get_nonempty_party_in_group:
# INPUT: param1: Party-id of the root of the group.
# OUTPUT: reg0: nonempy party-id
("get_nonempty_party_in_group",
    [ (store_script_param_1, ":party_no"),
      (party_get_num_companion_stacks, ":num_companion_stacks", ":party_no"),
      (try_begin),
        (gt, ":num_companion_stacks", 0),
        (assign, reg0, ":party_no"),
      (else_try),
        (assign, reg0, -1),
        
        (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (lt, reg0, 0),
          (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
          (call_script, "script_get_nonempty_party_in_group", ":attached_party"),
        (try_end),
      (try_end),
]),

#script_collect_prisoners_from_empty_parties:
# INPUT: param1: Party-id of the root of the group, param2: Party to collect prisoners in.
# make sure collection party is cleared before calling this.
("collect_prisoners_from_empty_parties",
    [ (store_script_param_1, ":party_no"),
      (store_script_param_2, ":collection_party"),
      (party_get_num_companions, ":num_companions", ":party_no"),
      (try_begin),
        (eq, ":num_companions", 0), #party is empty (has no companions). Collect its prisoners.
        (party_get_num_prisoner_stacks, ":num_stacks",":party_no"),
        (try_for_range, ":stack_no", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id,     ":stack_troop",":party_no",":stack_no"),
          (troop_is_hero, ":stack_troop"),
          (party_add_members, ":collection_party", ":stack_troop", 1),
        (try_end),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
        (call_script, "script_collect_prisoners_from_empty_parties", ":attached_party", ":collection_party"),
      (try_end),
]),

#script_print_casualties_to_s0:
# INPUT: param1: Party_id, param2: 0 = use new line, 1 = use comma, 2 = party of routed troops
#OUTPUT: string register 0.
("print_casualties_to_s0",
    [(store_script_param, ":party_no", 1),
     (store_script_param, ":use_comma", 2),
     (str_clear, s0),
     (assign, ":total_reported", 0),
     (assign, ":total_wounded", 0),
     (assign, ":total_killed", 0),
     (assign, ":total_routed", 0),
     (assign, ":num_routed", 0),
  
     (party_get_num_companion_stacks, ":num_stacks",":party_no"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
       (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
       (party_stack_get_num_wounded, ":num_wounded",":party_no",":i_stack"),
       (store_sub, ":num_killed", ":stack_size", ":num_wounded"),
	(try_begin),
		(eq, ":party_no", "p_player_casualties"),
		(troop_get_slot, ":num_routed", ":stack_troop", slot_troop_routed_us),
		(store_sub, ":num_killed", ":num_killed", ":num_routed"),
	(else_try),
		(eq, ":party_no", "p_ally_casualties"),
		(troop_get_slot, ":num_routed", ":stack_troop", slot_troop_routed_allies),
		(store_sub, ":num_killed", ":num_killed", ":num_routed"),
	(else_try),
		(eq, ":party_no", "p_enemy_casualties"),
		(troop_get_slot, ":num_routed", ":stack_troop", slot_troop_routed_enemies),
		(store_sub, ":num_killed", ":num_killed", ":num_routed"),
	(try_end),

       (store_sub, ":stack_size", ":stack_size", ":num_routed"),
       (val_add, ":total_killed", ":num_killed"),
       (val_add, ":total_wounded", ":num_wounded"),
       (val_add, ":total_routed", ":num_routed"),
       (try_begin),
         (this_or_next|gt, ":num_killed", 0),
         (this_or_next|gt, ":num_wounded", 0),
         (gt, ":num_routed", 0),
         (store_add, reg3, ":num_killed", ":num_wounded"),
         (val_add, reg3, ":num_routed"),
         (str_store_troop_name_by_count, s1, ":stack_troop", reg3),
         (try_begin),
           (troop_is_hero, ":stack_troop"),
           (assign, reg3, 0),
         (try_end),
         (try_begin),
           (gt, ":num_killed", 0),
           (gt, ":num_wounded", 0),
           (gt, ":num_routed", 0),
           (assign, reg4, ":num_killed"),
           (assign, reg5, ":num_wounded"),
           (assign, reg6, ":num_routed"),
           (str_store_string, s2, "@{reg4} killed, {reg5} wounded, {reg6} routed"),
         (else_try),
           (gt, ":num_killed", 0),
           (gt, ":num_wounded", 0),
           (assign, reg4, ":num_killed"),
           (assign, reg5, ":num_wounded"),
           (str_store_string, s2, "@{reg4} killed, {reg5} wounded"),
         (else_try),
           (gt, ":num_killed", 0),
           (gt, ":num_routed", 0),
           (assign, reg4, ":num_killed"),
           (assign, reg5, ":num_routed"),
           (str_store_string, s2, "@{reg4} killed, {reg5} routed"),
         (else_try),
           (gt, ":num_wounded", 0),
           (gt, ":num_routed", 0),
           (assign, reg4, ":num_wounded"),
           (assign, reg5, ":num_routed"),
           (str_store_string, s2, "@{reg4} wounded, {reg5} routed"),
         (else_try),
           (gt, ":num_killed", 0),
           (str_store_string, s2, "@killed"),
         (else_try),
           (gt, ":num_routed", 0),
           (str_store_string, s2, "@routed"),
         (else_try),
           (str_store_string, s2, "@wounded"),
         (try_end),
         (try_begin),
           (eq, ":use_comma", 1),
           (try_begin),
             (eq, ":total_reported", 0),
             (str_store_string, s0, "@{reg3?{reg3}:} {s1} ({s2})"),
           (else_try),
             (str_store_string, s0, "@{s0}, {reg3?{reg3}:} {s1} ({s2})"),
           (try_end),
         (else_try),
           (str_store_string, s0, "@{s0}^{reg3?{reg3}:} {s1} ({s2})"),
         (try_end),
         (val_add, ":total_reported", 1),
       (try_end),
     (try_end),

     (try_begin),
       (this_or_next|gt, ":total_killed", 0),
       (this_or_next|gt, ":total_wounded", 0),
       (gt, ":total_routed", 0),
       (store_add, reg3, ":total_killed", ":total_wounded"),
       (val_add, reg3, ":total_routed"),
       (try_begin),
         (gt, ":total_killed", 0),
         (gt, ":total_wounded", 0),
         (gt, ":total_routed", 0),
         (assign, reg4, ":total_killed"),
         (assign, reg5, ":total_wounded"),
         (assign, reg6, ":total_routed"),
         (str_store_string, s2, "@{reg4} killed, {reg5} wounded, {reg6} routed"),
       (else_try),
         (gt, ":total_killed", 0),
         (gt, ":total_wounded", 0),
         (assign, reg4, ":total_killed"),
         (assign, reg5, ":total_wounded"),
         (str_store_string, s2, "@{reg4} killed, {reg5} wounded"),
       (else_try),
         (gt, ":total_wounded", 0),
         (gt, ":total_routed", 0),
         (assign, reg4, ":total_wounded"),
         (assign, reg5, ":total_routed"),
         (str_store_string, s2, "@{reg4} wounded, {reg5} routed"),
       (else_try),
         (gt, ":total_killed", 0),
         (gt, ":total_routed", 0),
         (assign, reg4, ":total_killed"),
         (assign, reg5, ":total_routed"),
         (str_store_string, s2, "@{reg4} killed, {reg5} routed"),
       (else_try),
         (gt, ":total_killed", 0),
         (str_store_string, s2, "@killed"),
       (else_try),
         (gt, ":total_routed", 0),
         (str_store_string, s2, "@routed"),
       (else_try),
         (str_store_string, s2, "@wounded"),
       (try_end),
       (str_store_string, s0, "@{s0}^TOTAL: {reg3} ({s2})"),
     (else_try),
       (try_begin),(eq, ":use_comma", 1),(str_store_string, s0, "@None"),
        (else_try),                      (str_store_string, s0, "@^None"),
       (try_end),
     (try_end),
]),

#script_write_fit_party_members_to_stack_selection
# INPUT: param1: party_no, exclude_leader
#OUTPUT: trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
# trp_stack_selection_ids slots (2..n = stack troops)
("write_fit_party_members_to_stack_selection",
   [ (store_script_param, ":party_no", 1),
     (store_script_param, ":exclude_leader", 2),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":slot_index", 2),
     (assign, ":total_fit", 0),
     (try_for_range, ":stack_index", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_index"),
       (assign, ":num_fit", 0),
       (try_begin),
         (troop_is_hero, ":stack_troop"),
         (try_begin),
           (neg|troop_is_wounded, ":stack_troop"),
           (this_or_next|eq, ":exclude_leader", 0),
           (neq, ":stack_index", 0),
           (assign, ":num_fit",1),
         (try_end),
       (else_try),
         (party_stack_get_size, ":num_fit", ":party_no", ":stack_index"),
         (party_stack_get_num_wounded, ":num_wounded", ":party_no", ":stack_index"),
         (val_sub, ":num_fit", ":num_wounded"),
       (try_end),
       (try_begin),
         (gt, ":num_fit", 0),
         (troop_set_slot, "trp_stack_selection_amounts", ":slot_index", ":num_fit"),
         (troop_set_slot, "trp_stack_selection_ids", ":slot_index", ":stack_troop"),
         (val_add, ":slot_index", 1),
       (try_end),
       (val_add, ":total_fit", ":num_fit"),
     (try_end),
     (val_sub, ":slot_index", 2),
     (troop_set_slot, "trp_stack_selection_amounts", 0, ":slot_index"),
     (troop_set_slot, "trp_stack_selection_amounts", 1, ":total_fit"),
]),

#script_remove_fit_party_member_from_stack_selection
# INPUT: param1: slot_index
#OUTPUT: reg0 = troop_no
# trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
# trp_stack_selection_ids slots (2..n = stack troops)
("remove_fit_party_member_from_stack_selection",
   [ (store_script_param, ":slot_index", 1),
     (val_add, ":slot_index", 2),
     (troop_get_slot, ":amount", "trp_stack_selection_amounts", ":slot_index"),
     (troop_get_slot, ":troop_no", "trp_stack_selection_ids", ":slot_index"),
     (val_sub, ":amount", 1),
     (troop_set_slot, "trp_stack_selection_amounts", ":slot_index", ":amount"),
     (troop_get_slot, ":total_amount", "trp_stack_selection_amounts", 1),
     (val_sub, ":total_amount", 1),
     (troop_set_slot, "trp_stack_selection_amounts", 1, ":total_amount"),
     (try_begin),
       (le, ":amount", 0),
       (troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0),
       (store_add, ":end_cond", ":num_slots", 2),
       (store_add, ":begin_cond", ":slot_index", 1),
       (try_for_range, ":index", ":begin_cond", ":end_cond"),
         (store_sub, ":prev_index", ":index", 1),
         (troop_get_slot, ":value", "trp_stack_selection_amounts", ":index"),
         (troop_set_slot, "trp_stack_selection_amounts", ":prev_index", ":value"),
         (troop_get_slot, ":value", "trp_stack_selection_ids", ":index"),
         (troop_set_slot, "trp_stack_selection_ids", ":prev_index", ":value"),
       (try_end),
       (val_sub, ":num_slots", 1),
       (troop_set_slot, "trp_stack_selection_amounts", 0, ":num_slots"),
     (try_end),
     (assign, reg0, ":troop_no"),
]),

#script_remove_random_fit_party_member_from_stack_selection
#OUTPUT: reg0 = troop_no
# trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
# trp_stack_selection_ids slots (2..n = stack troops)
("remove_random_fit_party_member_from_stack_selection",
   [ (troop_get_slot, ":total_amount", "trp_stack_selection_amounts", 1),
     (store_random_in_range, ":random_troop", 0, ":total_amount"),
     (troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0),
     (store_add, ":end_cond", ":num_slots", 2),
     (try_for_range, ":index", 2, ":end_cond"),
       (troop_get_slot, ":amount", "trp_stack_selection_amounts", ":index"),
       (val_sub, ":random_troop", ":amount"),
       (lt, ":random_troop", 0),
       (assign, ":end_cond", 0),
       (store_sub, ":slot_index", ":index", 2),
     (try_end),
     (call_script, "script_remove_fit_party_member_from_stack_selection", ":slot_index"),
]),

#script_tld_start_training_at_training_ground
# Sets up the training scene and spawns player and opponents of appropriate race and equipment
# INPUT:
#   $g_tld_training_mode = abm_training, abm_team or abm_gauntlet
#   $g_tld_training_opponents = 1-4 for abm_training, 4-12 for abm_team
#   $g_tld_training_weapon = player weapon type
("tld_start_training_at_training_ground",
   [ (party_get_slot, ":training_scene", "$g_encountered_party", slot_town_arena),
     (modify_visitors_at_site, ":training_scene"),
     (reset_visitors),
   # Set up player and his team, if any
     (try_begin),
       (eq, "$g_tld_training_mode", abm_training),
       (assign, ":player_entry_point", 4),
     (else_try),
       (assign, ":player_entry_point", 12),
     (try_end),
   # Player
     (set_visitor, ":player_entry_point", "trp_player"),
     (call_script, "script_tld_training_equip_entry_point", ":player_entry_point", "trp_player", 0, "$g_tld_training_weapon", 0), #not mounted
   #Player team - first check for unwounded companions, then fill up with medium training troops
     (try_begin),
       (eq, "$g_tld_training_mode", abm_team),
       (assign, ":teammates_needed", 3),
       (store_add, ":teammate_entry_point", ":player_entry_point", 1),
       # companions
       (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
       (try_for_range, ":stack_no", 1, ":num_stacks"),
         (gt, ":teammates_needed", 0),
         (party_stack_get_troop_id, ":cur_troop", "p_main_party", ":stack_no"),
         (troop_is_hero, ":cur_troop"),
         (neg|troop_is_wounded, ":cur_troop"),
         (set_visitor, ":teammate_entry_point", ":cur_troop"),
         (call_script, "script_tld_training_equip_entry_point", ":teammate_entry_point", ":cur_troop", 0, -1, -1), #random weapon type and mount
         (val_add, ":teammate_entry_point", 1),
         (val_sub, ":teammates_needed", 1),
       (try_end),
       # filling up
       (try_for_range, ":unused", 0, ":teammates_needed"),
         (store_random_in_range, ":random_no", 0, 100),
         (try_begin),
           (lt, ":random_no", 30),
           (faction_get_slot, ":teammate", "$g_encountered_party_faction", slot_faction_tier_1_troop),
         (else_try),
           (lt, ":random_no", 70),
           (faction_get_slot, ":teammate", "$g_encountered_party_faction", slot_faction_tier_2_troop),
         (else_try),
           (faction_get_slot, ":teammate", "$g_encountered_party_faction", slot_faction_tier_3_troop),
         (try_end),
         (set_visitor, ":teammate_entry_point", ":teammate"),
         (call_script, "script_tld_training_equip_entry_point", ":teammate_entry_point", ":teammate", 0, -1, -1), #random weapon type and mount
         (val_add, ":teammate_entry_point", 1),
       (try_end),
     (else_try),
       (eq, "$g_tld_training_mode", abm_mass_melee),
       
       (store_add, ":teammate_entry_point", ":player_entry_point", 1),
       # filling up
       (try_for_range, ":unused", 0, 3),
         (store_random_in_range, ":random_no", 0, 100),
         (try_begin),
           (lt, ":random_no", 30),
           (faction_get_slot, ":teammate", "$g_encountered_party_faction", slot_faction_tier_1_troop),
         (else_try),
           (lt, ":random_no", 70),
           (faction_get_slot, ":teammate", "$g_encountered_party_faction", slot_faction_tier_2_troop),
         (else_try),
           (faction_get_slot, ":teammate", "$g_encountered_party_faction", slot_faction_tier_3_troop),
         (try_end),
         (set_visitors, ":teammate_entry_point", ":teammate", 6), # 1 player + 6*3 troops = 19 vs. 24 enemies
         (call_script, "script_tld_training_equip_entry_point", ":teammate_entry_point", ":teammate", 0, -1, -1), #random weapon type and mount
         (val_add, ":teammate_entry_point", 1),
       (try_end),
     (try_end),
    
     #Set up enemies
     (try_begin),
       (eq, "$g_tld_training_mode", abm_training),
       (assign, ":first_enemy_entry_point", 5),
     (else_try),
       (assign, ":first_enemy_entry_point", 16),
     (try_end),
     (store_add, ":last_enemy_entry_point_plus_one", ":first_enemy_entry_point", "$g_tld_training_opponents"),
     
     # (try_begin),
       (store_character_level, ":player_level_bias", "trp_player"),
       (val_clamp, ":player_level_bias", 1, 30), #1-29
       (val_sub, ":player_level_bias", 15), #-14..+14
       (try_for_range, ":entry_point", ":first_enemy_entry_point", ":last_enemy_entry_point_plus_one"),
         # choose opponent based on player level and random number
         (store_random_in_range, ":random_no", 0, 100),
         (val_add, ":random_no", ":player_level_bias"), #-14..+113
         (try_begin),(lt,":random_no",20),(faction_get_slot,":opponent","$g_encountered_party_faction",slot_faction_tier_1_troop),
          (else_try),(lt,":random_no",40),(faction_get_slot,":opponent","$g_encountered_party_faction",slot_faction_tier_2_troop),
          (else_try),(lt,":random_no",60),(faction_get_slot,":opponent","$g_encountered_party_faction",slot_faction_tier_3_troop),
          (else_try),(lt,":random_no",80),(faction_get_slot,":opponent","$g_encountered_party_faction",slot_faction_tier_4_troop),
          (else_try),                     (faction_get_slot,":opponent","$g_encountered_party_faction",slot_faction_tier_5_troop),
         (try_end),
         
         # arm the opponent randomly
         (try_begin),
           (eq, "$g_tld_training_mode", abm_mass_melee),
           (set_visitors, ":entry_point", ":opponent", 2), #24 dudes
         (else_try),
           (neq, "$g_tld_training_mode", abm_gauntlet),
           (set_visitor, ":entry_point", ":opponent"), #gauntlet does this in the mission template
         (try_end),
         (call_script, "script_tld_training_equip_entry_point", ":entry_point", ":opponent", 1, -1, -1), #random weapon type and mount
       (try_end),
     # (try_end),
     (set_jump_mission, "mt_training_ground_training"),
     (jump_to_scene, ":training_scene"),
     ]),
     
  #script_tld_training_equip_entry_point
  # Equip entry point with training items for a weapon type
  # INPUT: entry_point to override
  #        troop to spawn there
  #        team: 0-player, 1-enemy
  #        weapon_type = itp_X; -1 for random
  #        is_mounted = 0 or 1, flag for mounted weapons; -1 for random
  # OUTPUT: none
  ("tld_training_equip_entry_point",
   [ (store_script_param_1, ":entry_point"),
     (store_script_param_2, ":troop"),
     (store_script_param, ":team", 3),
     (store_script_param, ":weapon_type", 4),
     (store_script_param, ":is_mounted", 5),
     
     (troop_get_type, ":race", ":troop"),
     (assign, ":is_orc", 0),
	 (try_begin),
		(is_between, ":race", tf_orc_begin, tf_orc_end),
		(assign, ":is_orc", 1),
	 (try_end),
     
     #(set_visitor, ":entry_point", ":troop"),
     (mission_tpl_entry_clear_override_items, "mt_training_ground_training", ":entry_point"),
         
	 (try_begin),(eq,"$g_talk_troop","trp_trainer_gondor"),(assign,":shield_item","itm_gon_tab_shield_a"),
      (else_try),(eq,"$g_talk_troop","trp_trainer_rohan" ),(assign,":shield_item","itm_rohan_shield_c"),
      (else_try),(eq,"$g_talk_troop","trp_trainer_elf"   ),(assign,":shield_item","itm_mirkwood_spear_shield_c"),
      (else_try),(eq,"$g_talk_troop","trp_trainer_dwarf" ),(assign,":shield_item","itm_beorn_shield"),
      (else_try),(eq,"$g_talk_troop","trp_trainer_dale"  ),
		 (try_begin),(eq, ":team", 0),
			(assign, ":shield_item" , "itm_dale_shield_a"),
		 (else_try),
			(assign, ":shield_item" , "itm_dale_shield_b"),
		 (try_end),
      (else_try),(eq,"$g_talk_troop","trp_trainer_harad" ),(assign,":shield_item","itm_harad_shield_a"),
      (else_try),(eq,"$g_talk_troop","trp_trainer_rhun"  ),(assign,":shield_item","itm_rhun_shield"),
      (else_try),(eq,"$g_talk_troop","trp_trainer_khand" ),(assign,":shield_item","itm_tab_shield_small_round_b"),
      (else_try),(eq,"$g_talk_troop","trp_trainer_beorn" ),(assign,":shield_item","itm_beorn_shield"),
      (else_try),(eq,"$g_talk_troop","trp_trainer_umbar" ),(assign,":shield_item","itm_umb_shield_b"),
      (else_try),#(eq, "$g_talk_troop", "trp_trainer_mordor"), #or isengard - for all orcs
         (assign, ":shield_item" , "itm_orc_shield_a"),
     (try_end),
  # clothes 
     (try_begin),
       (eq, ":team", 0), #player team
       (try_begin),(eq,"$g_talk_troop","trp_trainer_gondor"),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_white_tunic_b"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_rohan" ),#(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_green_tunic"), #naked
        (else_try),(eq,"$g_talk_troop","trp_trainer_elf"   ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_white_tunic_b"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_dwarf" ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_red_tunic"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_dale"  ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_white_tunic_b"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_harad" ),#(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_red_tunic"), # naked
        (else_try),(eq,"$g_talk_troop","trp_trainer_rhun"  ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_black_tunic"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_khand" ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_white_tunic_b"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_beorn" ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_beorn_tunic"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_umbar" ),#(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_beorn_tunic"), # naked
        (else_try),                                          #(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_white_tunic_b"), #naked
       (try_end),
     (else_try),  #opponents
       (try_begin),(eq,"$g_talk_troop","trp_trainer_gondor"),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_black_tunic"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_rohan" ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_green_tunic"), 
        (else_try),(eq,"$g_talk_troop","trp_trainer_elf"   ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_green_tunic"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_dwarf" ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_blue_tunic"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_dale"  ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_blue_tunic"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_harad" ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_red_tunic"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_rhun"  ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_rhun_armor_a"), 
        (else_try),(eq,"$g_talk_troop","trp_trainer_khand" ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_khand_light"), 
        (else_try),(eq,"$g_talk_troop","trp_trainer_beorn" ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_woodman_tunic"),
        (else_try),(eq,"$g_talk_troop","trp_trainer_umbar" ),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point","itm_black_tunic"),
        (else_try),#(eq,"$g_talk_troop","trp_trainer_mordor"), #or isengard - for all orcs
		 # (try_begin),(eq, ":race", tf_orc),
           # (mission_tpl_entry_add_override_item, "mt_training_ground_training", ":entry_point", "itm_orc_tribal_a"),
		 # (else_try),
		   # (mission_tpl_entry_add_override_item, "mt_training_ground_training", ":entry_point", "itm_black_tunic"),
		 # (try_end),
       (try_end),
	 (try_end),
     # proper boots
     (try_begin),
       (is_between, ":race", tf_orc_begin, tf_orc_end), 
       #(mission_tpl_entry_add_override_item, "mt_training_ground_training", ":entry_point", "itm_orc_ragwrap"), # no footwear for orcs or urucs
     (else_try),
       (mission_tpl_entry_add_override_item, "mt_training_ground_training", ":entry_point", "itm_leather_boots"),
	 (try_end),
     
     # random equipment (no more type_thrown)
     (try_begin),
       (eq, ":weapon_type", -1),
       (store_random_in_range, ":random_no", 0, 100),
       (try_begin),
         (lt, ":random_no", 15),
         (neq, "$g_tld_training_mode", abm_mass_melee),
         (assign, ":weapon_type", itp_type_bow), #15% chance
       (else_try),
          (lt, ":random_no", 25),
          (neq, "$g_tld_training_mode", abm_mass_melee),
          (assign, ":weapon_type", itp_type_thrown), #10%
        (else_try),
         (lt, ":random_no", 50),
         (assign, ":weapon_type", itp_type_one_handed_wpn), #25%
       (else_try),
         (lt, ":random_no", 75),
         (assign, ":weapon_type", itp_type_two_handed_wpn), #25%
       (else_try),
         (assign, ":weapon_type", itp_type_polearm), #25%
       (try_end),
     (try_end),

     # random mounted status
     (try_begin),
       (eq, ":is_mounted", -1),
       (store_random_in_range, ":is_mounted", 0, 100),
       (val_div, ":is_mounted", 80), #20% chance mounted
       (eq, "$g_tld_training_mode", abm_mass_melee),
       (assign, ":is_mounted", 0),
     (try_end),
     # overrides: no horses for dwarves and big orcs, always horses for rohan
     (try_begin),
       (this_or_next|eq, "$g_talk_troop", "trp_trainer_dwarf"),
	   (is_between, ":race", tf_urukhai, tf_orc_end),  
       (assign, ":is_mounted", 0),
     (else_try),
       (eq, "$g_talk_troop", "trp_trainer_rohan"),
       (assign, ":is_mounted", 1),
     (try_end),
     
     # equip mount
     (try_begin),
       (eq, ":is_mounted", 1),
       (try_begin),
         (eq, ":is_orc", 1),
         (mission_tpl_entry_add_override_item, "mt_training_ground_training", ":entry_point", "itm_warg_1b"),
       (else_try),
         (mission_tpl_entry_add_override_item, "mt_training_ground_training", ":entry_point", "itm_sumpter_horse"),
       (try_end),
     (try_end),
     
     # choose set of items according to weapon type
     (assign, ":item_1", -1),
     (assign, ":item_2", -1),
     (assign, ":item_3", -1),
     (assign, ":item_4", -1),
     (try_begin),
       (eq, ":weapon_type", itp_type_bow),
       (assign, ":item_1", "itm_practice_bow"),
       (assign, ":item_2", "itm_arrows"),
       (assign, ":item_3", "itm_wood_club"),
     (else_try),
       (eq, ":weapon_type", itp_type_thrown),
       (assign, ":item_1", "itm_wooden_javelin"),
       (assign, ":item_2", ":shield_item"),
       (assign, ":item_3", "itm_wood_club"),
     (else_try),
       (eq, ":weapon_type", itp_type_one_handed_wpn),
       (store_random_in_range, ":random_no", 0, 3),
       (assign, ":item_1", "itm_wood_club"),
       (assign, ":item_2", ":shield_item"),
     (else_try),
       (eq, ":weapon_type", itp_type_two_handed_wpn),
       (assign, ":item_1", "itm_twohand_wood_club"),
     (else_try),
       #(eq, ":weapon_type", itp_type_polearm),
       (try_begin),
         (eq, ":is_mounted", 1),
         (assign, ":item_1", "itm_practice_staff"),
         (assign, ":item_2", ":shield_item"),
       (else_try),
         (assign, ":item_1", "itm_practice_staff"),
       (try_end),
     (try_end),

     #...and equip
	(try_begin),(ge,":item_1",0),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point",":item_1"),(try_end),
	(try_begin),(ge,":item_2",0),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point",":item_2"),(try_end),
	(try_begin),(ge,":item_3",0),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point",":item_3"),(try_end),
	(try_begin),(ge,":item_4",0),(mission_tpl_entry_add_override_item,"mt_training_ground_training",":entry_point",":item_4"),(try_end),
]),

#script_get_random_melee_training_weapon
# OUTPUT: reg0 = weapon_1, reg1 = weapon_2
("get_random_melee_training_weapon",
   [ (assign, ":weapon_1", -1),
     (assign, ":weapon_2", -1),
     (store_random_in_range, ":random_no", 0, 3),
     (try_begin),(eq, ":random_no", 0),
      (else_try),(eq, ":random_no", 1),
     (else_try),
     (try_end),
     (assign, reg0, ":weapon_1"),
     (assign, reg1, ":weapon_2"),
]),

#script_party_count_fit_regulars:
# Returns the number of unwounded regular companions in a party
# INPUT: param1: Party-id
("party_count_fit_regulars",
    [ (store_script_param_1, ":party"),
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size,         ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_add, reg0, ":stack_size"),
      (try_end),
]),

# small script, mtarini
("cf_party_is_mostly_mounted",
    [ (store_script_param_1, ":party"),
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, ":num_foot",0),
      (assign, ":num_mounted",0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
		(assign, ":x",1),
		(try_begin),  (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size,":x",":party",":i_stack"),
        (try_end),
		(try_begin),(troop_is_mounted, ":stack_troop"),
            (val_add, ":num_mounted",":x"),
		(else_try),
            (val_add, ":num_foot", ":x"),
        (try_end),
      (try_end),
	  (ge, ":num_mounted",":num_foot"),
]),

#script_party_count_fit_for_battle:
# Returns the number of unwounded companions in a party
# INPUT: param1: Party-id
# OUTPUT: reg0 = result
("party_count_fit_for_battle",
    [ (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party",":i_stack"),
        (assign, ":num_fit",0),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (try_begin),
            (neg|troop_is_wounded, ":stack_troop"),
            (assign, ":num_fit",1),
		  (else_try), # TLD, track wounded status
			(troop_set_slot, ":stack_troop", slot_troop_wounded, 1),
          (try_end),
        (else_try),
          (party_stack_get_size,         ":num_fit",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":num_fit", ":num_wounded"),
        (try_end),
        (val_add, reg0, ":num_fit"),
      (try_end),
]),
#script_party_count_members_with_full_health
# Returns the number of unwounded regulars, and heroes other than player with 100% hitpoints in a party
# INPUT: param1: Party-id
# OUTPUT: reg0 = result
("party_count_members_with_full_health",
    [ (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (assign, ":num_fit",0),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (neq, ":stack_troop", "trp_player"),
          (store_troop_health, ":troop_hp", ":stack_troop"),
          (try_begin),
            (ge,  ":troop_hp", 80),
            (assign, ":num_fit",1),
          (try_end),
        (else_try),
          (party_stack_get_size,         ":num_fit",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":num_fit", ":num_wounded"),
          (val_max, ":num_fit", 0),
        (try_end),
        (val_add, reg0, ":num_fit"),
      (try_end),
]),
("party_count_wounded",
    [ (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (store_troop_health, ":troop_hp", ":stack_troop"),
          (try_begin),
            (le,  ":troop_hp", 99),
            (val_add, reg0,5), # heros count for 5
          (try_end),
        (else_try),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_add, reg0, ":num_wounded"),
        (try_end),
      (try_end),
]),

#script_get_stack_with_rank:
# Returns the stack no, containing unwounded regular companions with rank rank.
# INPUT: param1: Party-id, param2: rank
("get_stack_with_rank",
    [ (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":rank"), #Rank
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg(0), -1),
      (assign, ":num_total", 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (eq, reg(0), -1), #continue only if we haven't found the result yet.
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size,         ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded,  ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_add, ":num_total", ":stack_size"),
        (try_begin),
          (lt, ":rank", ":num_total"),
          (assign, reg(0), ":i_stack"),
        (try_end),
      (try_end),
]),

#script_inflict_casualties_to_party:
# INPUT: param1 = Party-id, param2 = number of rounds
#OUTPUT: This script doesn't return a value but populates the parties p_temp_wounded and p_temp_killed with the wounded and killed.
#Example: (script_inflict_casualties_to_party, "_p_main_party" ,50), - simulates 50 rounds of casualties to main_party.
("inflict_casualties_to_party",
    [ (party_clear, "p_temp_casualties"),
      (store_script_param_1, ":party"), #Party_id
      (call_script, "script_party_count_fit_regulars", ":party"),
      (assign, ":num_fit", reg(0)), #reg(47) = number of fit regulars.
      (store_script_param_2, ":num_attack_rounds"), #number of attacks
      (try_for_range, ":unused", 0, ":num_attack_rounds"),
        (gt, ":num_fit", 0),
        (store_random_in_range, ":attacked_troop_rank", 0 , ":num_fit"), #attack troop with rank reg(46)
        (assign, reg1, ":attacked_troop_rank"),
        (call_script, "script_get_stack_with_rank", ":party", ":attacked_troop_rank"),
        (assign, ":attacked_stack", reg(0)), #reg(53) = stack no to attack.
        (party_stack_get_troop_id,     ":attacked_troop",":party",":attacked_stack"),
        (store_character_level, ":troop_toughness", ":attacked_troop"),
        (val_add, ":troop_toughness", 5),  #troop-toughness = level + 5
        (assign, ":casualty_chance", 10000),
        (val_div, ":casualty_chance", ":troop_toughness"), #dying chance
        (try_begin),
          (store_random_in_range, ":rand_num", 0 ,10000),
          (lt, ":rand_num", ":casualty_chance"), #check chance to be a casualty
          (store_random_in_range, ":rand_num2", 0, 2), #check if this troop will be wounded or killed
          (try_begin),
            (troop_is_hero,":attacked_troop"), #currently troop can't be a hero, but no harm in keeping this.
            (store_troop_health, ":troop_hp",":attacked_troop"),
            (val_sub, ":troop_hp", 45),
            (val_max, ":troop_hp", 1),
            (troop_set_health, ":attacked_troop", ":troop_hp"),
          (else_try),
            (lt, ":rand_num2", 1), #wounded
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_wound_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_wound_members, ":party", ":attacked_troop", 1),
          (else_try), #killed
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_remove_members, ":party", ":attacked_troop", 1),
          (try_end),
          (val_sub, ":num_fit", 1), #adjust number of fit regulars.
        (try_end),
      (try_end),
]),

#script_move_members_with_ratio:
# INPUT: param1 = Source Party-id, param2 = Target Party-id
# pin_number = ratio of members to move, multiplied by 1000
#OUTPUT: This script doesn't return a value but moves some of the members of source party to target party according to the given ratio.
("move_members_with_ratio",
    [ (store_script_param_1, ":source_party"), #Source Party_id
      (store_script_param_2, ":target_party"), #Target Party_id
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (party_prisoner_stack_get_size,    ":stack_size",":source_party",":stack_no"),
        (store_mul, ":number_to_move",":stack_size","$pin_number"),
        (val_div, ":number_to_move", 1000),
        (party_remove_prisoners, ":source_party", ":stack_troop", ":number_to_move"),
        (assign, ":number_moved", reg0),
        (party_add_prisoners, ":target_party", ":stack_troop", ":number_moved"),
      (try_end),
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (party_stack_get_size,    ":stack_size",":source_party",":stack_no"),
        (store_mul, ":number_to_move",":stack_size","$pin_number"),
        (val_div, ":number_to_move", 1000),
        (party_remove_members, ":source_party", ":stack_troop", ":number_to_move"),
        (assign, ":number_moved", reg0),
        (party_add_members, ":target_party", ":stack_troop", ":number_moved"),
      (try_end),
]),

# script_count_parties_of_faction_and_party_type:
# counts number of active parties with a template and faction.
# Input: arg1 = faction_no, arg2 = party_type
# Output: reg0 = count
("count_parties_of_faction_and_party_type",
    [ (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),
      (assign, reg0, 0),
      (try_for_parties, ":party_no"),
        (party_is_active, ":party_no"),
		(party_slot_eq, ":party_no", slot_center_destroyed, 0), #TLD
        (party_slot_eq, ":party_no", slot_party_type, ":party_type"),
        (store_faction_of_party, ":cur_faction", ":party_no"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, reg0, 1),
      (try_end),
]),

#script_cf_select_random_town_with_faction:
# This script selects a random town in range [centers_begin, centers_end) such that faction of the town is equal to given_faction
# INPUT: arg1 = faction_no
#OUTPUT: reg0 = town_no, this script may return false if there is no matching town.
("cf_select_random_town_with_faction",
    [ (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", centers_begin, centers_end),
        (party_is_active, ":cur_town"), #TLD
        (party_slot_eq, ":cur_town", slot_center_destroyed, 0), #TLD
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", centers_begin, centers_end),
        (party_is_active, ":cur_town"), #TLD
        (party_slot_eq, ":cur_town", slot_center_destroyed, 0), #TLD
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
        (gt, ":no_towns", ":random_town"),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
]),

#script_cf_select_random_town_allied:
# This script selects a random town in range [centers_begin, centers_end) such that faction of the town is allied
# INPUT: arg1 = faction_no
#OUTPUT: reg0 = town_no, this script may return false if there is no matching town. reg1 = distance
("cf_select_random_town_allied",
    [ (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":dist", 0),
      # First count num matching spawn points
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", centers_begin, centers_end),
        (party_is_active, ":cur_town"), #TLD
	    (party_slot_eq, ":cur_town", slot_center_destroyed, 0), #TLD
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":relation", ":faction_no", ":cur_faction"),
        (ge, ":relation", 0), #TLD: allied towns
        #(store_distance_to_party_from_party, ":dist", "p_main_party", ":cur_town"),
        (call_script, "script_get_tld_distance", "p_main_party", ":cur_town"),
        (assign, ":dist", reg0),
        (le, ":dist", tld_max_quest_distance), #TLD: not too far
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", centers_begin, centers_end),
        (party_is_active, ":cur_town"), #TLD
        (party_slot_eq, ":cur_town", slot_center_destroyed, 0), #TLD - not destroyed
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":relation", ":faction_no", ":cur_faction"),
        (ge, ":relation", 0), #TLD: allied towns
        #(store_distance_to_party_from_party, ":dist", "p_main_party", ":cur_town"),
        (call_script, "script_get_tld_distance", "p_main_party", ":cur_town"),
        (assign, ":dist", reg0),
        (le, ":dist", tld_max_quest_distance), #TLD: not too far
        (val_add, ":no_towns", 1),
        (gt, ":no_towns", ":random_town"),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
      (assign, reg1, ":dist"),
]),

#script_cf_select_random_walled_center_with_faction_and_owner_priority_no_siege:
# INPUT: arg1 = faction_no, arg2 = owner_troop_no
#OUTPUT: reg0 = center_no (Can fail)
("cf_select_random_walled_center_with_faction_and_owner_priority_no_siege",
    [ (store_script_param, ":faction_no", 1),
      (store_script_param, ":troop_no", 2),
      #This script is used only to spawn lords, so make sure they spawn in their home theater
      (faction_get_slot, ":home_theater", ":faction_no", slot_faction_home_theater), #TLD
      (assign, ":result", -1),
      (assign, ":no_centers", 0),
      (try_for_range,":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
		(party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_theater, ":home_theater"), #TLD
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_add, ":no_centers", 1),
        (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
        (val_add, ":no_centers", 1000),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range,":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
		(party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_theater, ":home_theater"), #TLD
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
          (val_sub, ":random_center", 1000),
        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
]),

#script_cf_select_random_walled_center_with_faction_and_less_strength_priority:
# This script selects a random center in range [centers_begin, centers_end) such that faction of the town is equal to given_faction
# INPUT: arg1 = faction_no, arg2 = preferred_center_no
#OUTPUT: reg0 = town_no, This script may return false if there is no matching town.
("cf_select_random_walled_center_with_faction_and_less_strength_priority",
    [ (store_script_param, ":faction_no", 1),
      (store_script_param, ":preferred_center_no", 2),
      (assign, ":result", -1),
#TLD begin
      (faction_get_slot, ":faction_theater", ":faction_no", slot_faction_active_theater),
      # TLD: First try to find a center in the active theater, if that fails, go anywhere as normal
      # Note: this script is only used when lords decide where to go next
      # First count num matching spawn points
      (assign, ":no_centers", 0),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
		(party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_theater, ":faction_theater"), #TLD
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_add, ":no_centers", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_add, ":no_centers", 99),
        (try_end),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
		(party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_theater, ":faction_theater"), #TLD
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
#TLD end
      # First count num matching spawn points
      (assign, ":no_centers", 0),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
		(party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_add, ":no_centers", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_add, ":no_centers", 99),
        (try_end),
##        (call_script, "script_party_calculate_regular_strength", ":cur_center"),
##        (assign, ":strength", reg0),
##        (lt, ":strength", 80),
##        (store_sub, ":strength", 100, ":strength"),
##        (val_div, ":strength", 20),
##        (val_add, ":no_centers", ":strength"),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
		(party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
##        (try_begin),
##          (call_script, "script_party_calculate_regular_strength", ":cur_center"),
##          (assign, ":strength", reg0),
##          (lt, ":strength", 80),
##          (store_sub, ":strength", 100, ":strength"),
##          (val_div, ":strength", 20),
##          (val_sub, ":random_center", ":strength"),
##        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
]),

#script_cf_select_random_town_at_peace_with_faction:
# This script selects a random town in range [centers_begin, centers_end) such that faction of the town is friendly to given_faction
# INPUT: arg1 = faction_no
#OUTPUT: reg0 = town_no, this script may return false if there is no matching town.
("cf_select_random_town_at_peace_with_faction",
    [ (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching towns
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", centers_begin, centers_end),
	    (party_is_active,":cur_town"), # TLD
		(party_slot_eq, ":cur_town", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation,":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", centers_begin, centers_end),
        (eq, ":result", -1),
		(party_is_active,":cur_town"), # TLD
		(party_slot_eq, ":cur_town", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation,":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
        (gt, ":no_towns", ":random_town"),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
]),

#script_cf_select_random_town_at_peace_with_faction_in_trade_route
# INPUT: arg1 = town_no, arg2 = faction_no
#OUTPUT: reg0 = town_no, this script may return false if there is no matching town.
("cf_select_random_town_at_peace_with_faction_in_trade_route",
    [ (store_script_param, ":town_no", 1),
      (store_script_param, ":faction_no", 2),
      (assign, ":result", -1),
      (assign, ":no_towns", 0),
      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),
	  	(party_is_active,":cur_town"), # TLD
		(party_slot_eq, ":cur_town", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (eq, ":result", -1),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),
		(party_is_active,":cur_town"), # TLD
		(party_slot_eq, ":cur_town", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_sub, ":random_town", 1),
        (lt, ":random_town", 0),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
]),

# script_shuffle_troop_slots:
# Shuffles a range of slots of a given troop. Used for exploiting a troop as an array.
# INPUT: arg1 = troop_no, arg2 = slot_begin, arg3 = slot_end
("shuffle_troop_slots",
    [ (store_script_param, ":troop_no", 1),
      (store_script_param, ":slots_begin", 2),
      (store_script_param, ":slots_end", 3),
      (try_for_range, ":cur_slot_no", ":slots_begin", ":slots_end"),
        (store_random_in_range, ":random_slot_no", ":slots_begin", ":slots_end"), #reg(58) = random slot. Now exchange slots reg(57) and reg(58)
        (troop_get_slot, ":cur_slot_value", ":troop_no", ":cur_slot_no"), #temporarily store the value in slot reg(57) in reg(59)
        (troop_get_slot, ":random_slot_value", ":troop_no", ":random_slot_no"), #temporarily store the value in slot reg(58) in reg(60)
        (troop_set_slot, ":troop_no", ":cur_slot_no", ":random_slot_value"), # Now exchange the two...
        (troop_set_slot, ":troop_no", ":random_slot_no", ":cur_slot_value"),
      (try_end),
]),

# script_get_random_quest
# INPUT: arg1 = troop_no (of the troop in conversation), arg2 = min_importance (of the quest)
#OUTPUT: reg0 = quest_no (the slots of the quest will be filled after calling this script)
("get_random_quest",
    [ (store_script_param_1, ":giver_troop"),
      
      (store_character_level, ":player_level", "trp_player"),
      (store_troop_faction, ":giver_faction_no", ":giver_troop"),
      (troop_get_slot, ":giver_party_no", ":giver_troop", slot_troop_leaded_party),
      #(troop_get_slot, ":giver_reputation", ":giver_troop", slot_lord_reputation_type),
      (assign, ":giver_center_no", -1),
      (try_begin),
        (gt, ":giver_party_no", 0),
        (party_get_attached_to, ":giver_center_no", ":giver_party_no"),
      (else_try),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (assign, ":giver_center_no", "$g_encountered_party"),
      (try_end),
      
      (try_begin),
        (troop_slot_eq, ":giver_troop", slot_troop_occupation, slto_kingdom_hero),
        (try_begin),
          (ge, "$g_talk_troop_faction_relation", 0),
          (assign, ":quests_begin", lord_quests_begin),
          (assign, ":quests_end", lord_quests_end),
        (else_try),
          (assign, ":quests_begin", enemy_lord_quests_begin),
          (assign, ":quests_end", enemy_lord_quests_end),
        (try_end),
      (else_try),
        (is_between, ":giver_troop", mayors_begin, mayors_end),
        (assign, ":quests_begin", mayor_quests_begin),
        (assign, ":quests_end", mayor_quests_end),
      (else_try),
        (assign, ":quests_begin", mayor_quests_begin),
        (assign, ":quests_end", mayor_quests_end),
      (try_end),
      (assign, ":result", -1),
      (try_for_range, ":unused", 0, 30), #Repeat trial twenty times - MV: changed to 30
        (eq, ":result", -1),
        (assign, ":quest_target_troop", -1),
        (assign, ":quest_target_center", -1),
        (assign, ":quest_target_faction", -1),
        (assign, ":quest_object_faction", -1),
        (assign, ":quest_object_troop", -1),
        (assign, ":quest_object_center", -1),
        (assign, ":quest_target_party", -1),
        (assign, ":quest_target_party_template", -1),
        (assign, ":quest_target_amount", -1),
        (assign, ":quest_target_dna", -1),
        (assign, ":quest_target_item", -1),
        (assign, ":quest_importance", 1),
        (assign, ":quest_xp_reward", 0),
        (assign, ":quest_gold_reward", 0),
        (assign, ":quest_rank_reward", 0), #TLD
        (assign, ":quest_convince_value", 0),
        (assign, ":quest_expiration_days", 0),
        (assign, ":quest_dont_give_again_period", 0),

        (store_random_in_range, ":quest_no", ":quests_begin", ":quests_end"),
#MV: Change this line and uncomment for testing only, don't let it slip into SVN (or else :))    
		#(assign, ":quest_no", "qst_escort_merchant_caravan"),
#mtarini: ok, ok, so we put in a menu:
		(try_begin), (ge, "$cheat_imposed_quest", 0),(assign, ":quest_no", "$cheat_imposed_quest"),(try_end),
		
        (neg|check_quest_active,":quest_no"),
        (neg|quest_slot_ge, ":quest_no", slot_quest_dont_give_again_remaining_days, 1),
        (try_begin),
          #GA: Galadriel wants sorcerer killed
          (eq, ":quest_no", "qst_mirkwood_sorcerer"),
		  (try_begin),
			(eq, ":giver_troop", "trp_lorien_lord"),  # only Galadriel gives this quest
			(ge, ":player_level", 15), # CC: Was 1, change to 15, too hard if available at level 1.
			(assign, ":quest_expiration_days", 10),
			(assign, ":quest_dont_give_again_period", 10000),
			(assign, ":quest_importance", 4),
			(assign, ":quest_xp_reward", 3000),
			(assign, ":quest_gold_reward", 1500),
			(assign, ":quest_rank_reward", 60),
			(assign, ":result", ":quest_no"),
		  (try_end),
        (else_try),          #mtarini: Saruman wants a troll be captured
          (eq, ":quest_no", "qst_capture_troll"),
		  (try_begin),
			(eq, ":giver_troop", "trp_isengard_lord"),  # only saruman gives this quest
			(ge, ":player_level", 3),
			(assign, ":quest_expiration_days", 15),
			(assign, ":quest_dont_give_again_period", 20),
			(store_free_inventory_capacity,":tmp"),(gt,":tmp",0), # otherwise,  no room for cage
			(assign, ":quest_importance", 3),
			(assign, ":quest_xp_reward", 1500),
			(assign, ":quest_gold_reward", 500),
			(assign, ":quest_rank_reward", 45),
			(assign, ":result", ":quest_no"),
		  (try_end),
        (else_try),
		  #mtarini: good-sided lords wants a troll be killed
          (eq, ":quest_no", "qst_kill_troll"),
		  (try_begin),
			(gt, ":player_level", 4),
			(faction_slot_eq, ":giver_faction_no", slot_faction_side, faction_side_good),
			#(faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),
			(call_script, "script_cf_select_random_town_with_faction", ":giver_faction_no"),#Can fail
			(assign, ":cur_object_center", reg0),
			(neq, ":cur_object_center", ":giver_center_no"),#Skip current center
            #(call_script, "script_get_random_enemy_center", ":giver_party_no"),
            #(assign, ":cur_target_center", reg0),
            #(ge, ":cur_target_center", 0),
            #(store_faction_of_party, ":cur_target_faction", ":cur_target_center"),
            #(is_between,  ":cur_target_faction", kingdoms_begin, kingdoms_end),
			(assign, ":quest_object_center", ":cur_object_center"),
			#(assign, ":quest_target_center", ":cur_target_center"),
			(assign, ":quest_importance", 3),
			(assign, ":quest_xp_reward", 1500),
			(assign, ":quest_gold_reward", 500),
			(assign, ":quest_rank_reward", 40),
			(assign, ":quest_expiration_days", 10),
			(assign, ":quest_dont_give_again_period", 30),
			(assign, ":result", ":quest_no"),
		  (try_end),
        (else_try),
          #mtarini: Saruman wants Fangorn to be investigated
          (eq, ":quest_no", "qst_investigate_fangorn"),
		  (try_begin),
			(eq, ":giver_troop", "trp_isengard_lord"),  # only saruman gives this quest
			(ge, ":player_level", 4),
			(assign, ":quest_expiration_days", 40),
			(assign, ":quest_dont_give_again_period", 180),
			(assign, ":quest_importance", 2),
			(assign, ":quest_xp_reward", 100),
			(assign, ":quest_gold_reward", 500),
			(assign, ":quest_rank_reward", 30),
			(assign, ":result", ":quest_no"),
		  (try_end),
        (else_try),
          #Kolba: Lost spears - given by Brand
          (eq, ":quest_no", "qst_find_lost_spears"),
		  (try_begin),
 			(eq, 1, cheat_switch), #CC: Enabled only with cheat switch
			(eq, ":giver_troop", "trp_dale_lord"),  # only brand gives this quest
			(ge, ":player_level", 4),
			(assign, ":quest_expiration_days", 40),
			(assign, ":quest_dont_give_again_period", 180),
			(assign, ":quest_importance", 2),
			(assign, ":quest_xp_reward", 100),
			(assign, ":quest_gold_reward", 500),
			(assign, ":quest_rank_reward", 50),
			(assign, ":result", ":quest_no"),
		  (try_end),
# Mayor quests
        (else_try),
          (eq, ":quest_no", "qst_escort_merchant_caravan"),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          (party_get_slot, ":quest_target_party_template", ":giver_center_no", slot_center_spawn_caravan),
          (gt, ":quest_target_party_template", 0), #only for centers that spawn caravans
          (call_script, "script_cf_select_random_town_allied", ":giver_faction_no"),#Can fail
          (assign, ":cur_target_dist", reg1),
          (neq, ":giver_center_no", reg0),
          (assign, ":quest_target_center", reg0),
          # (store_random_party_in_range, ":quest_target_center", centers_begin, centers_end),
          # (store_distance_to_party_from_party, ":dist", ":giver_center_no",":quest_target_center"),
          (assign, ":quest_gold_reward", ":cur_target_dist"),
          (val_add, ":quest_gold_reward", 25),
          (val_mul, ":quest_gold_reward", 25),
          (val_div, ":quest_gold_reward", 20),
          (assign, ":quest_xp_reward", ":quest_gold_reward"),
          (val_mul, ":quest_xp_reward", 5),
          (val_add, ":quest_xp_reward", 100),
          (store_random_in_range, ":quest_target_amount", 6, 12),
          (store_div, ":quest_rank_reward", ":quest_target_amount", 2),
          #(assign, ":quest_expiration_days", 7),
          (assign, "$escort_merchant_caravan_mode", 0),
          (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_deliver_wine"),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          #(store_random_party_in_range, ":quest_target_center", centers_begin, centers_end),
          (call_script, "script_cf_select_random_town_allied", ":giver_faction_no"),#Can fail
          (assign, ":quest_target_center", reg0),
          (assign, ":cur_target_dist", reg1),
          (neq, ":giver_center_no", ":quest_target_center"),
          (party_get_slot, ":elder", ":quest_target_center", slot_town_elder),
          (neq, ":elder", "trp_no_troop"), #make sure there is an elder to deliver stuff to
          (gt, ":elder", 0),
          (assign, ":quest_target_troop", ":elder"),
          # (store_random_in_range, ":random_no", 0, 2),
          # (try_begin),
            # (eq, ":random_no", 0),
            # (assign, ":quest_target_item", "itm_quest_wine"),
          # (else_try),
          (assign, ":quest_target_item", "itm_siege_supply"), #TLD
          # (try_end),
          (store_random_in_range, ":quest_target_amount", 6, 12),
          #(store_distance_to_party_from_party, ":dist", ":giver_center_no",":quest_target_center"),
          (assign, ":quest_gold_reward", ":cur_target_dist"),
          (val_add, ":quest_gold_reward", 2),
          (assign, ":multiplier", 5),
          (val_add, ":multiplier", ":quest_target_amount"),
          (val_mul, ":quest_gold_reward", ":multiplier"),
          (val_div, ":quest_gold_reward", 100),
          (val_mul, ":quest_gold_reward", 30),
          (store_mul, ":quest_xp_reward", ":quest_gold_reward", 4),
          (store_div, ":quest_rank_reward", ":quest_target_amount", 2),
		  (assign, ":quest_importance", 4),
          (assign, ":quest_expiration_days", 7),
          (assign, ":quest_dont_give_again_period", 20),
          (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_troublesome_bandits"),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          (store_character_level, ":quest_gold_reward", "trp_player"),
          (val_add, ":quest_gold_reward", 20),
          (val_mul, ":quest_gold_reward", 35),
          (val_div, ":quest_gold_reward",100),
          (val_mul, ":quest_gold_reward", 10),
          (store_mul, ":quest_xp_reward", ":quest_gold_reward", 7),
          (assign, ":quest_rank_reward", 5),
		  (assign, ":quest_importance", 4),
          (assign, ":quest_expiration_days", 30),
          (assign, ":quest_dont_give_again_period", 30),
          (assign, ":result", ":quest_no"),
        # (else_try),
          # (eq, ":quest_no", "qst_kidnapped_girl"),
          # (is_between, ":giver_center_no", centers_begin, centers_end),
          # (store_random_in_range, ":quest_target_center", villages_begin, villages_end),
          # (store_character_level, ":quest_target_amount"),
          # (val_add, ":quest_target_amount", 15),
          # (store_distance_to_party_from_party, ":dist", ":giver_center_no", ":quest_target_center"),
          # (val_add, ":dist", 15),
          # (val_mul, ":dist", 2),
          # (val_mul, ":quest_target_amount", ":dist"),
          # (val_div, ":quest_target_amount",100),
          # (val_mul, ":quest_target_amount",10),
          # (assign, ":quest_gold_reward", ":quest_target_amount"),
          # (val_div, ":quest_gold_reward", 40),
          # (val_mul, ":quest_gold_reward", 10),
          # (assign, ":quest_dont_give_again_period", 30),
          # (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_move_cattle_herd"),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          #(call_script, "script_cf_select_random_town_at_peace_with_faction", ":giver_faction_no"),
          (call_script, "script_cf_select_random_town_allied", ":giver_faction_no"),#Can fail
          (assign, ":cur_target_dist", reg1),
          (neq, ":giver_center_no", reg0),
          (assign, ":quest_target_center", reg0),
          #(store_distance_to_party_from_party, ":dist",":giver_center_no",":quest_target_center"),
          (assign, ":quest_gold_reward", ":cur_target_dist"),
          (val_add, ":quest_gold_reward", 25),
          (val_mul, ":quest_gold_reward", 50),
          (val_div, ":quest_gold_reward", 20),
          (store_div, ":quest_xp_reward", ":quest_gold_reward", 3),
          (store_mul, ":quest_rank_reward", ":cur_target_dist", 8),
          (val_div, ":quest_rank_reward", tld_max_quest_distance),
          (assign, ":quest_importance", 8),
          (assign, ":quest_expiration_days", 20),
          (assign, ":quest_dont_give_again_period", 20),
          (assign, ":result", ":quest_no"),
        # (else_try),
          # (eq, ":quest_no", "qst_persuade_lords_to_make_peace"),
          # (is_between, ":giver_center_no", centers_begin, centers_end),
          # (store_faction_of_party, ":cur_object_faction", ":giver_center_no"),
          # (call_script, "script_cf_faction_get_random_enemy_faction", ":cur_object_faction"),
          # (assign, ":cur_target_faction", reg0),
          # (call_script, "script_cf_get_random_lord_except_king_with_faction", ":cur_object_faction"),
          # (assign, ":cur_object_troop", reg0),
          # (call_script, "script_cf_get_random_lord_except_king_with_faction", ":cur_target_faction"),
          # (assign, ":quest_target_troop", reg0),
          # (assign, ":quest_object_troop", ":cur_object_troop"),
          # (assign, ":quest_target_faction", ":cur_target_faction"),
          # (assign, ":quest_object_faction", ":cur_object_faction"),
          # (assign, ":quest_gold_reward", 12000),
          # (assign, ":quest_convince_value", 7000),
          # (assign, ":quest_expiration_days", 30),
          # (assign, ":quest_dont_give_again_period", 100),
          # (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_deal_with_looters"),
          (is_between, ":player_level", 0, 15),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          # (store_faction_of_party, ":cur_object_faction", ":giver_center_no"),
          (assign, ":quest_target_party_template", "pt_looters"), #can be regionalized for different bandits
          (store_num_parties_destroyed_by_player, ":num_looters_destroyed", ":quest_target_party_template"),
          (party_template_set_slot,":quest_target_party_template",slot_party_template_num_killed,":num_looters_destroyed"),
          (quest_set_slot,"qst_deal_with_looters",slot_quest_current_state,0),
          #(quest_set_slot,"$random_merchant_quest_no",slot_quest_target_party_template,"pt_looters"),
          (assign, ":quest_gold_reward", 500),
          (assign, ":quest_xp_reward", 500),
          (assign, ":quest_rank_reward", 6),
          (assign, ":quest_importance", 2),
          (assign, ":quest_expiration_days", 20),
          (assign, ":quest_dont_give_again_period", 30),
          (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_deal_with_night_bandits"),
          (neg|faction_slot_eq, ":giver_faction_no", slot_faction_side, faction_side_good), #TLD: evil factions only
          (is_between, ":player_level", 0, 15),
          (is_between, ":giver_center_no", centers_begin, centers_end),
          (party_set_slot, ":giver_center_no", slot_center_has_bandits, "trp_mountain_goblin"), #TLD: goblins
          #(party_slot_ge, ":giver_center_no", slot_center_has_bandits, 1),
          (assign, ":quest_target_center", ":giver_center_no"),
          (assign, ":quest_gold_reward", 150),
          (assign, ":quest_xp_reward", 200),
          (assign, ":quest_rank_reward", 2),
          (assign, ":quest_importance", 2),
          (assign, ":quest_expiration_days", 4),
          (assign, ":quest_dont_give_again_period", 15),
          (assign, ":result", ":quest_no"),
        (else_try),
          (eq, ":quest_no", "qst_deliver_iron"),
          (eq, "$tld_option_crossdressing", 0), #only if Item Restriction is ON, so loot produces scraps
          (store_random_in_range, ":quest_target_amount", 3, 8),
          (store_random_in_range, ":quest_target_item", scraps_begin, scraps_end),
          #empty merchant store of that food - done here and not in dialogs to prevent exploit
          (party_get_slot, ":center_merchant", ":giver_center_no", slot_town_merchant), #horse+goods guy
          (try_begin),
            (neq, ":center_merchant", "trp_no_troop"),
            (store_item_kind_count, ":num_items", ":quest_target_item", ":center_merchant"),
            (ge, ":num_items", 1),
            (troop_remove_items, ":center_merchant", ":quest_target_item", ":num_items"),
            (troop_sort_inventory, ":center_merchant"),
          (try_end),
          (assign, ":quest_target_center", ":giver_center_no"),
          (store_item_value, ":item_value", ":quest_target_item"),
          (val_mul, ":item_value", 2), #2x profit
          (store_mul, ":quest_gold_reward", ":quest_target_amount", ":item_value"),
          (store_mul, ":quest_xp_reward", ":quest_target_amount", 20),
          (store_div, ":quest_rank_reward", ":quest_target_amount", 2), #1-3
          (assign, ":quest_expiration_days", 20),
          (assign, ":quest_dont_give_again_period", 15),
          (assign, ":result", ":quest_no"),
         (else_try),
           (eq, ":quest_no", "qst_deliver_food"),
           (store_random_in_range, ":quest_target_amount", 3, 10),
           #(store_random_in_range, ":quest_target_item", normal_food_begin, food_end),
          ###empty merchant store of all food - done here and not in dialogs to prevent exploit
           (party_get_slot, ":center_merchant", ":giver_center_no", slot_town_merchant), #horse+goods guy
           (try_for_range, ":food_item", food_begin, food_end),
             (neq, ":center_merchant", "trp_no_troop"),
             (store_item_kind_count, ":num_items", ":food_item", ":center_merchant"),
             (ge, ":num_items", 1),
             (troop_remove_items, ":center_merchant", ":food_item", ":num_items"),
             (troop_sort_inventory, ":center_merchant"),
           (try_end),
           (assign, ":quest_target_center", ":giver_center_no"),
           (assign, ":item_value", 80), # an average
           (store_mul, ":quest_gold_reward", ":quest_target_amount", ":item_value"),
           (store_mul, ":quest_xp_reward", ":quest_target_amount", 20),
           (store_div, ":quest_rank_reward", ":quest_target_amount", 3), #1-3
           (assign, ":quest_expiration_days", 10),
           (assign, ":quest_dont_give_again_period", 15),
           (assign, ":result", ":quest_no"),
		(else_try),
			(eq, ":quest_no", "qst_lend_surgeon"),
			(try_begin),
				(eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)
				#(neq, ":giver_reputation", lrep_quarrelsome),
				#(neq, ":giver_reputation", lrep_debauched),
				(assign, ":max_surgery_level", 0),
				(assign, ":best_surgeon", -1),
				(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
				(try_for_range, ":i_stack", 1, ":num_stacks"),
					(party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
					(troop_is_hero, ":stack_troop"),
					(store_skill_level, ":cur_surgery_skill", skl_surgery, ":stack_troop"),
					(gt, ":cur_surgery_skill", ":max_surgery_level"),
					(assign, ":max_surgery_level", ":cur_surgery_skill"),
					(assign, ":best_surgeon", ":stack_troop"),
				(try_end),
            	(store_character_level, ":cur_level", "trp_player"),
				(assign, ":required_skill", 5),
				(val_div, ":cur_level", 10),
				(val_add, ":required_skill", ":cur_level"),
				(ge, ":max_surgery_level", ":required_skill"), #Skip if party skill level is less than the required value
				(assign, ":quest_object_troop", ":best_surgeon"),
				(assign, ":quest_importance", 1),
				(assign, ":quest_xp_reward", 100),
				(assign, ":quest_gold_reward", 200),
				(assign, ":quest_dont_give_again_period", 30),
				(assign, ":result", ":quest_no"),
			(try_end),
# Lord Quests
        # (else_try),
          # (eq, ":quest_no", "qst_meet_spy_in_enemy_town"),
          # (try_begin),
            # (eq, "$players_kingdom", ":giver_faction_no"),
            # (neq, ":giver_reputation", lrep_goodnatured),
            # (call_script, "script_troop_get_player_relation", ":giver_troop"),
            # (assign, ":giver_relation", reg0),
            # (gt, ":giver_relation", 3),
            # (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),
            # (assign, ":enemy_faction", reg0),
            # (store_relation, ":reln", ":enemy_faction", "fac_player_supporters_faction"),
            # (lt, ":reln", 0),
            # (call_script, "script_cf_select_random_town_with_faction", ":enemy_faction"),
            # (assign, ":cur_target_center", reg0),
            # #Just to make sure that there is a free walker
            # (call_script, "script_cf_center_get_free_walker", ":cur_target_center"),
            # (assign, ":quest_target_center", ":cur_target_center"),
            # (store_random_in_range, ":quest_target_amount", secret_signs_begin, secret_signs_end),
            # (assign, ":result", ":quest_no"),
            # (assign, ":quest_gold_reward", 500),
            # (assign, ":quest_expiration_days", 30),
            # (assign, ":quest_dont_give_again_period", 50),
            # (quest_set_slot, "qst_meet_spy_in_enemy_town", slot_quest_gold_reward, 500),
          # (try_end),
        # (else_try),
          # (eq, ":quest_no", "qst_raid_caravan_to_start_war"),
          # (try_begin),
            # (eq, "$players_kingdom", ":giver_faction_no"),
            # (this_or_next|eq, ":giver_reputation", lrep_cunning),
            # (this_or_next|eq, ":giver_reputation", lrep_quarrelsome),
            # (             eq, ":giver_reputation", lrep_debauched),
            # (gt, ":player_level", 10),
            # (neg|faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),#Can not take the quest from the king
            # (call_script, "script_cf_faction_get_random_friendly_faction", ":giver_faction_no"),#Can fail
            # (assign, ":quest_target_faction", reg0),
            # (store_troop_faction, ":quest_object_faction", ":giver_troop"),
            # (assign, ":quest_target_party_template", "pt_kingdom_caravan_party"),
            # (assign, ":quest_target_amount", 2),
            # (assign, ":result", ":quest_no"),
            # (assign, ":quest_expiration_days", 30),
            # (assign, ":quest_dont_give_again_period", 100),
          # (try_end),
        (else_try),
          (eq, ":quest_no", "qst_deliver_message"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            (lt, ":player_level", 20),
            (call_script, "script_cf_get_random_lord_in_a_center_with_faction", ":giver_faction_no"),#Can fail
            (assign, ":cur_target_troop", reg0),
            (assign, ":cur_target_dist", reg1),
            (neq, ":cur_target_troop", ":giver_troop"),#Skip himself
            (call_script, "script_get_troop_attached_party", ":cur_target_troop"),
            (assign, ":cur_target_center", reg0),#cur_target_center will definitely be a valid center
            (neq,":giver_center_no", ":cur_target_center"),#Skip current center

            (assign, ":quest_target_center", ":cur_target_center"),
            (assign, ":quest_target_troop", ":cur_target_troop"),
            #(assign, ":quest_xp_reward", 30), #TLD: changed to 30-50
            (store_mul, ":quest_xp_reward", 20, ":cur_target_dist"),
            (val_div, ":quest_xp_reward", tld_max_quest_distance),
            (val_add, ":quest_xp_reward", 30),
            #(assign, ":quest_gold_reward", 40), #TLD: changed to 40-80
            (store_mul, ":quest_gold_reward", 40, ":cur_target_dist"),
            (val_div, ":quest_gold_reward", tld_max_quest_distance),
            (val_add, ":quest_gold_reward", 40),
            (store_mul, ":quest_rank_reward", 4, ":cur_target_dist"), # 3-7
            (val_div, ":quest_rank_reward", tld_max_quest_distance),
            (val_add, ":quest_rank_reward", 3),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 30),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_escort_messenger"),
          (try_begin),
            (hero_can_join, "p_main_party"), #Skip if player has no available slots
            (ge, "$g_talk_troop_faction_relation", 0),
            (ge, ":player_level", 10),
            # TLD: Choose messenger of appropriate race
            (try_begin),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_mordor"),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_isengard"),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_moria"),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_guldur"),
              (eq, "$g_talk_troop_faction", "fac_gundabad"),
              (assign, ":cur_object_troop", "trp_messenger_orc"),
            (else_try),
              (eq, "$g_talk_troop_faction", "fac_dwarf"),
              (assign, ":cur_object_troop", "trp_messenger_dwarf"),
            (else_try),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_lorien"),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_imladris"),
              (eq, "$g_talk_troop_faction", "fac_woodelf"),
              (assign, ":cur_object_troop", "trp_messenger_elf"),
            (else_try), # (CppCoder): Bugfix, evil men need different messenger than regular men.
	      (faction_slot_eq|neg, "$g_talk_troop_faction", slot_faction_side, faction_side_good),
              (assign, ":cur_object_troop", "trp_messenger_evil_man"),
            (else_try),
              (assign, ":cur_object_troop", "trp_messenger_man"),
            (try_end),
            (call_script, "script_cf_select_random_town_allied", ":giver_faction_no"),#Can fail
            (assign, ":cur_target_center", reg0),
            (assign, ":cur_target_dist", reg1),
            (neq, ":cur_target_center", ":giver_center_no"),
            
            (store_mul, ":quest_xp_reward", 200, ":cur_target_dist"), # 200-400
            (val_div, ":quest_xp_reward", tld_max_quest_distance),
            (val_add, ":quest_xp_reward", 200),
            (store_mul, ":quest_gold_reward", 100, ":cur_target_dist"), # 200-300
            (val_div, ":quest_gold_reward", tld_max_quest_distance),
            (val_add, ":quest_gold_reward", 200),
            (store_mul, ":quest_rank_reward", 10, ":cur_target_dist"), # 7-17
            (val_div, ":quest_rank_reward", tld_max_quest_distance),
            (val_add, ":quest_rank_reward", 7),
            
            (assign, ":quest_importance", 20),

            (assign, ":quest_object_troop", ":cur_object_troop"),
            (assign, ":quest_target_center", ":cur_target_center"),
            (assign, ":quest_expiration_days", 20),
            (assign, ":quest_dont_give_again_period", 30),
            (assign, ":result", ":quest_no"),
          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_hunt_down_raiders"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),
##            (call_script, "script_cf_select_random_town_with_faction", ":giver_faction_no"),#Can fail
##            (assign, ":cur_object_center", reg0),
##            (neq, ":cur_object_center", ":giver_center_no"),#Skip current center
##            (call_script, "script_get_random_enemy_center", ":giver_party_no"),
##            (assign, ":cur_target_center", reg0),
##            (ge, ":cur_target_center", 0),
##            (store_faction_of_party, ":cur_target_faction", ":cur_target_center"),
##            (is_between,  ":cur_target_faction", kingdoms_begin, kingdoms_end),
##
##            (assign, ":quest_object_center", ":cur_object_center"),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 1500),
##            (assign, ":quest_gold_reward", 1000),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_bring_back_deserters"),
##          (try_begin),
##            (gt, ":player_level", 5),
##            (faction_get_slot, ":cur_target_party_template", ":giver_faction_no", slot_faction_deserter_party_template),
##            (faction_get_slot, ":cur_target_troop", ":giver_faction_no", slot_faction_deserter_troop),
##            (gt, ":cur_target_party_template", 0),#Skip factions with no deserter party templates
##            (store_num_parties_of_template, ":num_deserters", ":cur_target_party_template"),
##            (ge, ":num_deserters", 2),#Skip if there are less than 2 active deserter parties
##
##            (assign, ":quest_target_troop", ":cur_target_troop"),
##            (assign, ":quest_target_party_template", ":cur_target_party_template"),
##            (assign, ":quest_target_amount", 5),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 500),
##            (assign, ":quest_gold_reward", 300),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_deliver_supply_to_center_under_siege"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (gt, ":giver_center_no", 0),#Skip if lord is outside the center
##            (call_script, "script_cf_get_random_siege_location_with_faction", ":giver_faction_no"),#Can fail
##            (assign, ":quest_target_center", reg0),
##            (assign, ":quest_target_amount", 10),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 500),
##            (assign, ":quest_gold_reward", 300),
##            (assign, ":result", ":quest_no"),
##          (try_end),

##        (else_try),
##          (eq, ":quest_no", "qst_bring_reinforcements_to_siege"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (call_script, "script_cf_get_random_siege_location_with_attacker_faction", ":giver_faction_no"),#Can fail
##            (assign, ":cur_target_center", reg0),
##            (store_random_in_range, ":random_no", 5, 11),
##            (troops_can_join, ":random_no"),#Skip if the player doesn't have enough room
##            (call_script, "script_cf_get_number_of_random_troops_from_party", ":giver_party_no", ":random_no"),#Can fail
##            (assign, ":cur_object_troop", reg0),
##            (party_get_battle_opponent, ":cur_target_party", ":cur_target_center"),
##            (party_get_num_companion_stacks, ":num_stacks", ":cur_target_party"),
##            (gt, ":num_stacks", 0),#Skip if the besieger party has no troops
##            (party_stack_get_troop_id, ":cur_target_troop", ":cur_target_party", 0),
##            (troop_is_hero, ":cur_target_troop"),#Skip if the besieger party has no heroes
##            (neq, ":cur_target_troop", ":giver_troop"),#Skip if the quest giver is the same troop
##            (assign, ":quest_target_troop", ":cur_target_troop"),
##            (assign, ":quest_object_troop", ":cur_object_troop"),
##            (assign, ":quest_target_party", ":cur_target_party"),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":quest_target_amount", ":random_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 400),
##            (assign, ":quest_gold_reward", 200),
##            (assign, ":result", ":quest_no"),
##          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_deliver_message_to_enemy_lord"),
          (try_begin),
   (eq, 1, 0), #disabled - no dealings with the enemy
            (ge, "$g_talk_troop_faction_relation", 0),
            (is_between, ":player_level", 5, 25),
            (call_script, "script_cf_get_random_lord_from_enemy_faction_in_a_center", ":giver_faction_no"),#Can fail
            (assign, ":cur_target_troop", reg0),
            (assign, ":cur_target_dist", reg1),
            (call_script, "script_get_troop_attached_party", ":cur_target_troop"),
            (assign, ":quest_target_center", reg0),#quest_target_center will definitely be a valid center
            (assign, ":quest_target_troop", ":cur_target_troop"),
            (assign, ":quest_importance", 8),
            #(assign, ":quest_xp_reward", 200), # TLD 200-300
            (store_mul, ":quest_xp_reward", 100, ":cur_target_dist"),
            (val_div, ":quest_xp_reward", tld_max_quest_distance),
            (val_add, ":quest_xp_reward", 200),
            #(assign, ":quest_gold_reward", 0), # TLD 300-400
            (store_mul, ":quest_gold_reward", 100, ":cur_target_dist"),
            (val_div, ":quest_gold_reward", tld_max_quest_distance),
            (val_add, ":quest_gold_reward", 300),
            (store_mul, ":quest_rank_reward", 5, ":cur_target_dist"), # rank 5-10
            (val_div, ":quest_rank_reward", tld_max_quest_distance),
            (val_add, ":quest_rank_reward", 5),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 40),
          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_bring_prisoners_to_enemy"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (is_between, ":giver_center_no", centers_begin, centers_end),#Skip if the quest giver is not at a center
##            (store_random_in_range, ":random_no", 5, 11),
##            (troops_can_join_as_prisoner, ":random_no"),#Skip if the player doesn't have enough room
##            (call_script, "script_get_random_enemy_town", ":giver_center_no"),
##            (assign, ":cur_target_center", reg0),
##            (ge, ":cur_target_center", 0),#Skip if there are no enemy towns
##            (store_faction_of_party, ":cur_target_faction", ":cur_target_center"),
##            (faction_get_slot, ":cur_object_troop", ":cur_target_faction", slot_faction_tier_5_troop),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":quest_object_troop", ":cur_object_troop"),
##            (assign, ":quest_target_amount", ":random_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 300),
##            (assign, ":quest_gold_reward", 200),
##            (assign, ":result", ":quest_no"),
##          (try_end),

	# (else_try), #GA: quest to defend refugees caravan from raiders
		# (eq, ":quest_no", "qst_deal_with_bandits_at_lords_village"),
		# (faction_slot_eq, ":giver_faction_no", slot_faction_side, faction_side_good),
		# (neg|is_between, ":giver_faction_no", fac_lorien,fac_dale), #elves and dwarves do not give such quests
		# (neq, ":giver_faction_no", fac_dwarf),
		# (ge, "$g_talk_troop_faction_relation", 0),
		# (ge, ":player_level", 5),
		# (gt, ":giver_center_no", 0),#Skip if lord is outside the center
		# (eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)

		# (assign, ":quest_target_party", ":cur_target_center"),
		# (assign, ":result", ":quest_no"),
		# (assign, ":quest_expiration_days", 1),
 
        (else_try),
          (eq, ":quest_no", "qst_raise_troops"),
          (try_begin),
            (neq, ":giver_faction_no", "fac_player_supporters_faction"), #we need tier_1_troop a valid value
            (ge, "$g_talk_troop_faction_relation", 0),
            (store_character_level, ":cur_level", "trp_player"),
            (gt, ":cur_level", 5),
             
            (store_random_in_range, ":quest_target_amount", 5, 8),
            (assign, ":quest_importance", ":quest_target_amount"),
            (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
            (le, ":quest_target_amount", ":free_capacity"),
            (faction_get_slot, ":quest_object_troop", ":giver_faction_no", slot_faction_tier_1_troop),
            (store_random_in_range, ":level_up", 20, 40),
            (val_add, ":level_up", ":cur_level"),
            (val_div, ":level_up", 10),

            (store_mul, ":quest_gold_reward", ":quest_target_amount", 10),

            (assign, ":quest_target_troop", ":quest_object_troop"),
            (try_for_range, ":unused", 0, ":level_up"),
              (troop_get_upgrade_troop, ":level_up_troop", ":quest_target_troop", 0),
              (gt, ":level_up_troop", 0),
              (assign, ":quest_target_troop", ":level_up_troop"),
              (val_mul, ":quest_gold_reward", 7),
              (val_div, ":quest_gold_reward", 4),
            (try_end),
      
##            (try_begin),
##              (ge, ":cur_level", 15),
##              (faction_get_slot, ":cur_target_troop", ":giver_faction_no", slot_faction_tier_5_troop),
##              (assign, ":quest_gold_reward", 300),
##            (else_try),
##              (faction_get_slot, ":cur_target_troop", ":giver_faction_no", slot_faction_tier_4_troop),
##              (assign, ":quest_gold_reward", 150),
##            (try_end),
##            (gt, ":cur_target_troop", 0),
            (assign, ":quest_xp_reward", ":quest_gold_reward"),
            (val_mul, ":quest_xp_reward", 3),
            (val_div, ":quest_xp_reward", 10),
            (assign, ":quest_rank_reward", ":quest_xp_reward"),
            (val_div, ":quest_rank_reward", 7),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 120),
            (assign, ":quest_dont_give_again_period", 15),
          (try_end),
        # (else_try),
          # (eq, ":quest_no", "qst_collect_taxes"),
          # (try_begin),
            # (neq, ":giver_reputation", lrep_goodnatured),
            # (neq, ":giver_reputation", lrep_upstanding),
            # (ge, "$g_talk_troop_faction_relation", 0),
            # (call_script, "script_cf_troop_get_random_leaded_town_or_village_except_center", ":giver_troop", ":giver_center_no"),
            # (assign, ":quest_target_center", reg0),
            # (assign, ":quest_importance", 1),
            # (assign, ":quest_gold_reward", 0),
            # (assign, ":quest_xp_reward", 100),
            # (assign, ":result", ":quest_no"),
            # (assign, ":quest_expiration_days", 50),
            # (assign, ":quest_dont_give_again_period", 20),
          # (try_end),
        (else_try),
          (eq, ":quest_no", "qst_hunt_down_fugitive"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            #(call_script, "script_cf_select_random_village_with_faction", ":giver_faction_no"),
            
            # TLD: Choose fugitive of appropriate race
            (try_begin),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_mordor"),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_isengard"),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_moria"),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_guldur"),
              (eq, "$g_talk_troop_faction", "fac_gundabad"),
              (assign, ":cur_object_troop", "trp_fugitive_orc"),
            (else_try),
              (eq, "$g_talk_troop_faction", "fac_dwarf"),
              (assign, ":cur_object_troop", "trp_fugitive_dwarf"),
            (else_try),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_lorien"),
              (this_or_next|eq, "$g_talk_troop_faction", "fac_imladris"),
              (eq, "$g_talk_troop_faction", "fac_woodelf"),
              (assign, ":cur_object_troop", "trp_fugitive_elf"),
            (else_try),
              (assign, ":cur_object_troop", "trp_fugitive_man"),
            (try_end),
            (assign, ":quest_object_troop", ":cur_object_troop"),
            
            (call_script, "script_cf_select_random_town_allied", ":giver_faction_no"),#Can fail
            (assign, ":quest_target_center", reg0),
            #(assign, ":quest_target_dist", reg1),
            (neq, ":quest_target_center", ":giver_center_no"),
            
            (assign, ":quest_importance", 4),
            (assign, ":quest_gold_reward", 300),
            (assign, ":quest_xp_reward", 300),
            (assign, ":quest_rank_reward", 13),
            
            (store_random_in_range, ":quest_target_dna", 0, 1000000),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 30),
          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_capture_messenger"),
##          (try_begin),
##            (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),
##            (assign, ":cur_target_faction", reg0),
##            (faction_get_slot, ":cur_target_troop", ":cur_target_faction", slot_faction_messenger_troop),
##            (gt, ":cur_target_troop", 0),#Checking the validiy of cur_target_troop
##            (store_num_parties_destroyed_by_player, ":quest_target_amount", "pt_messenger_party"),
##
##            (assign, ":quest_target_troop", ":cur_target_troop"),
##            (assign, ":quest_target_party_template", ":cur_target_party_template"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 700),
##            (assign, ":quest_gold_reward", 400),
##            (assign, ":result", ":quest_no"),
##          (try_end),

        # (else_try),
          # (eq, ":quest_no", "qst_kill_local_merchant"),
          # (try_begin),
            # (this_or_next|eq, ":giver_reputation", lrep_quarrelsome),
            # (this_or_next|eq, ":giver_reputation", lrep_cunning),
            # (             eq, ":giver_reputation", lrep_debauched),
            # (neg|faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),#Can not take the quest from the king
            # (ge, "$g_talk_troop_faction_relation", 0),
            # (gt, ":player_level", 5),
            # (is_between, ":giver_center_no", centers_begin, centers_end),
            # (assign, ":quest_importance", 1),
            # (assign, ":quest_xp_reward", 300),
            # (assign, ":quest_gold_reward", 1000),
            # (assign, ":result", ":quest_no"),
            # (assign, ":quest_expiration_days", 10),
            # (assign, ":quest_dont_give_again_period", 30),
          # (try_end),
        (else_try),
          (eq, ":quest_no", "qst_bring_back_runaway_serfs"),
          (try_begin),
            (neg|faction_slot_eq, ":giver_faction_no", slot_faction_side, faction_side_good),
            #(neq, ":giver_reputation", lrep_goodnatured),
            #(neq, ":giver_reputation", lrep_upstanding),
            (ge, "$g_talk_troop_faction_relation", 0),
            (ge, ":player_level", 5),
            (gt, ":giver_center_no", 0),#Skip if lord is outside the center
            (eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)
      
            (assign, ":cur_object_center", ":giver_center_no"), #TLD: just start from the same town
            #(call_script, "script_cf_select_random_town_with_faction", ":giver_faction_no"),
            (call_script, "script_cf_get_random_enemy_center_within_range", "p_main_party", tld_max_quest_distance),
            (assign, ":cur_target_center", reg0),
            (assign, ":dist", reg1),
            (neq, ":cur_target_center", ":giver_center_no"),#Skip current center
            (ge, ":dist", 20),
            (assign, ":quest_target_party_template", "pt_runaway_serfs"),
            (assign, ":quest_object_center", ":cur_object_center"),
            (assign, ":quest_target_center", ":cur_target_center"),
            (assign, ":quest_importance", 8),
            (assign, ":quest_xp_reward", 300),
            (assign, ":quest_gold_reward", 600),
            (assign, ":quest_rank_reward", 9),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 20),
            (assign, "$qst_bring_back_runaway_serfs_num_parties_returned", 0),
            (assign, "$qst_bring_back_runaway_serfs_num_parties_fleed", 0),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_follow_spy"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            #(neq, ":giver_reputation", lrep_goodnatured),
            (party_get_skill_level, ":tracking_skill", "p_main_party", "skl_tracking"),
            (ge, ":tracking_skill", 2),
            (ge, ":player_level", 10),
            (eq, "$g_defending_against_siege", 0), #Skip if the center is under siege (because of resting)
            (gt, ":giver_party_no", 0), #Skip if the quest giver doesn't have a party
            (gt, ":giver_center_no", 0), #skip if the quest giver is not in a center
            (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town), #skip if we are not in a town.
            (party_get_position, pos2, "p_main_party"),
            (assign, ":max_distance", 0),
            (assign, ":cur_object_center", 0),
            (try_for_range, ":unused_2", 0, 3), #MV: more distant centers more likely, was 10
              (call_script, "script_cf_get_random_enemy_center_within_range", ":giver_party_no", tld_max_quest_distance),
              (assign, ":random_object_center", reg0),
              (assign, ":cur_distance", reg1),
              (party_get_position, pos3, ":random_object_center"),
              (map_get_random_position_around_position, pos4, pos3, 6),
              (gt, ":cur_distance", 10), #MV: not too close
              (gt, ":cur_distance", ":max_distance"),
              (assign, ":max_distance", ":cur_distance"),
              (assign, ":cur_object_center", ":random_object_center"),
              (copy_position, pos63, pos4), #Do not change pos63 until quest is accepted
            (try_end),
            (gt, ":cur_object_center", 0), #Skip if there are no enemy centers

            #TLD good/evil troops and party templates
            (try_begin),
              (faction_slot_eq, ":giver_faction_no", slot_faction_side, faction_side_good),
              (assign, ":quest_object_troop", "trp_spy_evil"),
              (assign, ":quest_target_troop", "trp_spy_partner_evil"),
              (assign, ":quest_target_party_template", "pt_spy_evil"),
              (assign, ":quest_target_party", "pt_spy_partners_evil"), #abusing this for the second template
            (else_try),
              (assign, ":quest_object_troop", "trp_spy"),
              (assign, ":quest_target_troop", "trp_spy_partner"),
              (assign, ":quest_target_party_template", "pt_spy"),
              (assign, ":quest_target_party", "pt_spy_partners"), #abusing this for the second template
            (try_end),
            
            (assign, ":quest_object_center", ":cur_object_center"),
            (assign, ":cur_target_dist", ":max_distance"),

            (assign, ":quest_importance", 12),
            
            (store_mul, ":quest_xp_reward", 1000, ":cur_target_dist"), #TLD: 3000-4000
            (val_div, ":quest_xp_reward", tld_max_quest_distance),
            (val_add, ":quest_xp_reward", 3000),
            (store_mul, ":quest_gold_reward", 1000, ":cur_target_dist"), #TLD: 2000-3000
            (val_div, ":quest_gold_reward", tld_max_quest_distance),
            (val_add, ":quest_gold_reward", 2000),
            (store_mul, ":quest_rank_reward", 5, ":cur_target_dist"), # TLD: 15-20
            (val_div, ":quest_rank_reward", tld_max_quest_distance),
            (val_add, ":quest_rank_reward", 15),

            (assign, ":quest_dont_give_again_period", 50),
            (assign, ":result", ":quest_no"),
            (assign, "$qst_follow_spy_run_away", 0),
            (assign, "$qst_follow_spy_meeting_state", 0),
            (assign, "$qst_follow_spy_meeting_counter", 0),
            (assign, "$qst_follow_spy_spy_back_in_town", 0),
            (assign, "$qst_follow_spy_partner_back_in_town", 0),
            (assign, "$qst_follow_spy_no_active_parties", 0),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_capture_enemy_hero"),
          (try_begin),
            #(eq, "$players_kingdom", ":giver_faction_no"),
            #(neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
            (ge, ":player_level", 15),
            #(call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),#Can fail
            #(assign, ":quest_target_faction", reg0),
            (assign, ":quest_gold_reward", 2000),
            (assign, ":quest_xp_reward", 2500),
            (assign, ":quest_rank_reward", 20),
            (assign, ":quest_importance", 12),
            (assign, ":quest_expiration_days", 30),
            (assign, ":quest_dont_give_again_period", 80),
            (assign, ":result", ":quest_no"),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_lend_companion"),
          (try_begin),
            (ge, "$g_talk_troop_faction_relation", 0),
            (assign, ":total_heroes", 0),
            (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
            (try_for_range, ":i_stack", 0, ":num_stacks"),
              (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
              (troop_is_hero, ":stack_troop"),
              (is_between, ":stack_troop", companions_begin, companions_end),
              (store_character_level, ":stack_level", ":stack_troop"),
              (ge, ":stack_level", 15),
              (assign, ":is_quest_hero", 0),
              (try_for_range, ":i_quest", 0, all_quests_end),
                (check_quest_active, ":i_quest"),
                (this_or_next|quest_slot_eq, ":i_quest", slot_quest_target_troop, ":stack_troop"),
                (quest_slot_eq, ":i_quest", slot_quest_object_troop, ":stack_troop"),
                (assign, ":is_quest_hero", 1),
              (try_end),
              (eq, ":is_quest_hero", 0),
              (val_add, ":total_heroes", 1),
            (try_end),
            (gt, ":total_heroes", 0),#Skip if party has no eligible heroes
            (store_random_in_range, ":random_hero", 0, ":total_heroes"),
            (assign, ":total_heroes", 0),
            (assign, ":cur_target_troop", -1),
            (try_for_range, ":i_stack", 0, ":num_stacks"),
              (eq, ":cur_target_troop", -1),
              (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
              (troop_is_hero, ":stack_troop"),
              (neq, ":stack_troop", "trp_player"),
              (store_character_level, ":stack_level", ":stack_troop"),
              (ge, ":stack_level", 15),
              (assign, ":is_quest_hero", 0),
              (try_for_range, ":i_quest", 0, all_quests_end),
                (check_quest_active, ":i_quest"),
                (this_or_next|quest_slot_eq, ":i_quest", slot_quest_target_troop, ":stack_troop"),
                (quest_slot_eq, ":i_quest", slot_quest_object_troop, ":stack_troop"),
                (assign, ":is_quest_hero", 1),
              (try_end),
              (eq, ":is_quest_hero", 0),
              (val_add, ":total_heroes", 1),
              (gt, ":total_heroes", ":random_hero"),
              (assign, ":cur_target_troop", ":stack_troop"),
            (try_end),
            (assign, ":quest_target_troop", ":cur_target_troop"),
            (store_current_day, ":quest_target_amount"),
            (val_add, ":quest_target_amount", 8),

            (assign, ":quest_importance", 1),
            (assign, ":quest_xp_reward", 200),
            (assign, ":quest_gold_reward", 300),
            (assign, ":quest_rank_reward", 10),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_dont_give_again_period", 30),
          (try_end),
        # (else_try),
          # (eq, ":quest_no", "qst_collect_debt"),
          # (try_begin),
            # (ge, "$g_talk_troop_faction_relation", 0),
          # # Find a vassal (within the same kingdom?) 
            # (call_script, "script_cf_get_random_lord_in_a_center_with_faction", ":giver_faction_no"),#Can fail
            # (assign, ":quest_target_troop", reg0),
            # (neq, ":quest_target_troop", ":giver_troop"),#Skip himself
            # (call_script, "script_get_troop_attached_party", ":quest_target_troop"),
            # (assign, ":quest_target_center", reg0),#cur_target_center will definitely be a valid center
            # (neq,":giver_center_no", ":quest_target_center"),#Skip current center

            # (assign, ":quest_xp_reward", 30),
            # (assign, ":quest_gold_reward", 40),
            # (assign, ":result", ":quest_no"),
            # (store_random_in_range, ":quest_target_amount", 6, 9),
            # (val_mul, ":quest_target_amount", 500),
            # (store_div, ":quest_convince_value", ":quest_target_amount", 5),
            # (assign, ":quest_expiration_days", 90),
            # (assign, ":quest_dont_give_again_period", 20),
          # (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_capture_conspirators"),
##          (try_begin),
##            (eq, 1,0), #TODO: disable this for now
##            (ge, ":player_level", 10),
##            (is_between, ":giver_center_no", centers_begin, centers_end),#Skip if quest giver's center is not a town
##            (party_slot_eq, ":giver_center_no", slot_town_lord, ":giver_troop"),#Skip if the current center is not ruled by the quest giver
##            (call_script, "script_cf_get_random_kingdom_hero", ":giver_faction_no"),#Can fail
##
##            (assign, ":quest_target_troop", reg0),
##            (assign, ":quest_target_center", ":giver_center_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 10),
##            (assign, ":quest_gold_reward", 10),
##            (assign, ":result", ":quest_no"),
##            (store_character_level, ":cur_level"),
##            (val_div, ":cur_level", 5),
##            (val_max, ":cur_level", 3),
##            (store_add, ":max_parties", 4, ":cur_level"),
##            (store_random_in_range, "$qst_capture_conspirators_num_parties_to_spawn", 4, ":max_parties"),
##            (assign, "$qst_capture_conspirators_num_troops_to_capture", 0),
##            (assign, "$qst_capture_conspirators_num_parties_spawned", 0),
##            (assign, "$qst_capture_conspirators_leave_meeting_counter", 0),
##            (assign, "$qst_capture_conspirators_party_1", 0),
##            (assign, "$qst_capture_conspirators_party_2", 0),
##            (assign, "$qst_capture_conspirators_party_3", 0),
##            (assign, "$qst_capture_conspirators_party_4", 0),
##            (assign, "$qst_capture_conspirators_party_5", 0),
##            (assign, "$qst_capture_conspirators_party_6", 0),
##            (assign, "$qst_capture_conspirators_party_7", 0),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_defend_nobles_against_peasants"),
##          (try_begin),
##            (eq, 1,0), #TODO: disable this for now
##            (ge, ":player_level", 10),
##            (is_between, ":giver_center_no", centers_begin, centers_end),#Skip if quest giver's center is not a town
##            (party_slot_eq, ":giver_center_no", slot_town_lord, ":giver_troop"),#Skip if the current center is not ruled by the quest giver
##
##            (assign, ":quest_target_center", ":giver_center_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 10),
##            (assign, ":quest_gold_reward", 10),
##            (assign, ":result", ":quest_no"),
##            (store_character_level, ":cur_level"),
##            (val_div, ":cur_level", 5),
##            (val_max, ":cur_level", 4),
##            (store_add, ":max_parties", 4, ":cur_level"),
##            (store_random_in_range, "$qst_defend_nobles_against_peasants_num_peasant_parties_to_spawn", 4, ":cur_level"),
##            (store_random_in_range, "$qst_defend_nobles_against_peasants_num_noble_parties_to_spawn", 4, ":cur_level"),
##            (assign, "$qst_defend_nobles_against_peasants_num_nobles_to_save", 0),
##            (assign, "$qst_defend_nobles_against_peasants_num_nobles_saved", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_1", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_2", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_3", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_4", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_5", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_6", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_7", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_8", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_1", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_2", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_3", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_4", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_5", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_6", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_7", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_8", 0),
##          (try_end),
        # (else_try),
          # (eq, ":quest_no", "qst_incriminate_loyal_commander"),
          # (try_begin),
            # (neq, ":giver_reputation", lrep_upstanding),
            # (neq, ":giver_reputation", lrep_goodnatured),
            # (eq, "$players_kingdom", ":giver_faction_no"),
            # (ge, ":player_level", 10),
            # (faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),
            # (assign, ":try_times", 1),
            # (assign, ":found", 0),
            # (try_for_range, ":unused", 0, ":try_times"),
              # (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),#Can fail
              # (assign, ":cur_target_faction", reg0),

              # (faction_get_slot, ":cur_target_troop", ":cur_target_faction", slot_faction_leader),
              # (assign, ":num_centerless_heroes", 0),
              # (try_for_range, ":cur_kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
                # (troop_slot_eq, ":cur_kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
                # #(troop_slot_eq, ":cur_kingdom_hero", slot_troop_is_prisoner, 0),
                # (neg|troop_slot_ge, ":cur_kingdom_hero", slot_troop_prisoner_of_party, 0),
                # (neq, ":cur_target_troop", ":cur_kingdom_hero"),
                # (store_troop_faction, ":cur_kingdom_hero_faction", ":cur_kingdom_hero"),
                # (eq, ":cur_target_faction", ":cur_kingdom_hero_faction"),
# ##                (call_script, "script_get_number_of_hero_centers", ":cur_kingdom_hero"),
# ##                (eq, reg0, 0),
                # (val_add, ":num_centerless_heroes", 1),
              # (try_end),
              # (gt, ":num_centerless_heroes", 0),
              # (assign, ":cur_object_troop", -1),
              # (store_random_in_range, ":random_kingdom_hero", 0, ":num_centerless_heroes"),
              # (try_for_range, ":cur_kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
                # (eq, ":cur_object_troop", -1),
                # (troop_slot_eq, ":cur_kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
                # (neq, ":cur_target_troop", ":cur_kingdom_hero"),
                # (store_troop_faction, ":cur_kingdom_hero_faction", ":cur_kingdom_hero"),
                # (eq, ":cur_target_faction", ":cur_kingdom_hero_faction"),
# ##                (call_script, "script_get_number_of_hero_centers", ":cur_kingdom_hero"),
# ##                (eq, reg0, 0),
                # (val_sub, ":random_kingdom_hero", 1),
                # (lt, ":random_kingdom_hero", 0),
                # (assign, ":cur_object_troop", ":cur_kingdom_hero"),
              # (try_end),

              # (assign, ":cur_target_center", -1),
              # (call_script, "script_get_troop_attached_party", ":cur_target_troop"),
              # (is_between, reg0, centers_begin, centers_end),
              # (party_slot_eq, reg0, slot_town_lord, ":cur_target_troop"),
              # (assign, ":cur_target_center", reg0),

              # (assign, ":try_times", -1),#Exit the second loop
              # (assign, ":found", 1),
            # (try_end),
            # (eq, ":found", 1),

            # (assign, "$incriminate_quest_sacrificed_troop", 0),

            # (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
            # (try_for_range, ":i_stack", 1, ":num_stacks"),
              # (eq ,"$incriminate_quest_sacrificed_troop", 0),
              # (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
              # (neg|troop_is_hero, ":stack_troop"),
              # (store_character_level, ":stack_troop_level", ":stack_troop"),
              # (ge, ":stack_troop_level", 25),
              # (assign, "$incriminate_quest_sacrificed_troop", ":stack_troop"),
            # (try_end),
            # (gt, "$incriminate_quest_sacrificed_troop", 0),

            # (assign, ":quest_target_troop", ":cur_target_troop"),
            # (assign, ":quest_object_troop", ":cur_object_troop"),
            # (assign, ":quest_target_center", ":cur_target_center"),
            # (assign, ":quest_target_faction", ":cur_target_faction"),

            # (assign, ":quest_importance", 1),
            # (assign, ":quest_xp_reward", 700),
            # (assign, ":quest_gold_reward", 1000),
            # (assign, ":result", ":quest_no"),
            # (assign, ":quest_expiration_days", 30),
            # (assign, ":quest_dont_give_again_period", 180),
          # (try_end),
        (else_try),
          (eq, ":quest_no", "qst_capture_prisoners"),
          (try_begin),
            #not given by factions that have only elven or orcish enemies in the initial theatre, since elves and orcs can't be taken prisoner
            # central theater - no mercy there 
            (neq, ":giver_faction_no", "fac_moria"),
            (neq, ":giver_faction_no", "fac_guldur"),
            (neq, ":giver_faction_no", "fac_lorien"),
            (neq, ":giver_faction_no", "fac_imladris"),

            (store_character_level, ":quest_target_amount", "trp_player"),
            (gt, ":quest_target_amount", 5),
            (val_clamp, ":quest_target_amount", 6, 31),
            (val_div, ":quest_target_amount", 3), #2-10
            #(assign, ":quest_target_troop", ":cur_target_troop"),
            #(assign, ":quest_target_faction", ":cur_target_faction"),
            (assign, ":quest_importance", 1),
            #(store_character_level, ":quest_gold_reward", ":cur_target_troop"),
            (store_mul, ":quest_gold_reward", ":quest_target_amount", 20),
            (val_add, ":quest_gold_reward", 50), # 90-250
            (assign, ":quest_xp_reward", ":quest_gold_reward"),
            (val_mul, ":quest_xp_reward", 5),
            (val_div, ":quest_xp_reward", 7),
            (assign, ":quest_rank_reward", ":quest_target_amount"),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 90),
            (assign, ":quest_dont_give_again_period", 20),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_rescue_prisoners"),
          (try_begin),
            (store_character_level, ":quest_target_amount", "trp_player"),
            (gt, ":quest_target_amount", 7),
            (val_clamp, ":quest_target_amount", 8, 21),
            (val_sub, ":quest_target_amount", 4), #4-16
            (assign, ":quest_importance", 1),
            (store_mul, ":quest_gold_reward", ":quest_target_amount", 20),
            (assign, ":quest_xp_reward", ":quest_gold_reward"),
            (store_mul, ":quest_rank_reward", ":quest_target_amount", 2),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 60),
            (assign, ":quest_dont_give_again_period", 20),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_scout_enemy_town"),
          (try_begin),
            (call_script, "script_cf_get_random_enemy_center_within_range", "p_main_party", tld_max_quest_distance),
            (assign, ":quest_target_center", reg0),
            (assign, ":dist", reg1),
            (assign, ":quest_target_troop", 0), #abuse this as a boolean flag: if town scouted
            
            (assign, ":quest_importance", 1),
            (store_mul, ":quest_gold_reward", ":dist", 5),
            (assign, ":quest_xp_reward", ":dist"),
            (store_div, ":quest_rank_reward", ":dist", 7),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 7),
            (assign, ":quest_dont_give_again_period", 20),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_dispatch_scouts"),
          (try_begin),
            (ge, ":player_level", 5),
            (faction_get_slot, ":capital", ":giver_faction_no", slot_faction_capital), #count on capitals to have scouts
            (party_get_slot, ":center_scouts", ":capital", slot_center_spawn_scouts),
            (gt, ":center_scouts", 0),
            (assign, ":quest_target_party_template", ":center_scouts"),
            
            (call_script, "script_cf_get_random_enemy_center_within_range", "p_main_party", tld_max_quest_distance),
            (assign, ":quest_target_center", reg0),
            (assign, ":dist", reg1),
            
            (assign, ":quest_object_faction", ":giver_faction_no"),
            (faction_get_slot, ":tier_1_troop", ":quest_object_faction", slot_faction_tier_1_troop), #4 of these
            (faction_get_slot, ":tier_2_troop", ":quest_object_faction", slot_faction_tier_2_troop), #2 of these
            (faction_get_slot, ":tier_3_troop", ":quest_object_faction", slot_faction_tier_3_troop), #1 of these, and used for member chat
            (gt, ":tier_1_troop", 0),
            (gt, ":tier_2_troop", 0),
            (gt, ":tier_3_troop", 0),
            (assign, ":quest_object_troop", ":tier_3_troop"),
            
            (assign, ":quest_importance", 4),
            (store_mul, ":quest_gold_reward", ":dist", 7),
            (assign, ":quest_xp_reward", ":dist"),
            (store_div, ":quest_rank_reward", ":dist", 5),
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 15),
            (assign, ":quest_dont_give_again_period", 20),
          (try_end),
        (else_try),
          (eq, ":quest_no", "qst_eliminate_patrols"),
          (try_begin),
            (gt, "$tld_war_began", 0),
            (ge, ":player_level", 10),
            (call_script, "script_cf_get_random_enemy_center_within_range", "p_main_party", tld_max_quest_distance),
            (assign, ":quest_target_center", reg0),
            #(assign, ":dist", reg1),
            #find a random enemy scout/raider/patrol/caravan spawned in the enemy center
            (party_get_slot, ":center_scouts", ":quest_target_center", slot_center_spawn_scouts),
            (party_get_slot, ":center_raiders", ":quest_target_center", slot_center_spawn_raiders),
            (party_get_slot, ":center_patrol", ":quest_target_center", slot_center_spawn_patrol),
            (party_get_slot, ":center_caravan", ":quest_target_center", slot_center_spawn_caravan),
            (store_random_in_range, ":random_no", 0, 4),
            (assign, ":min_amount", 0),
            (assign, ":done", 0),
            (try_begin),
              (eq, ":random_no", 0),
              (gt, ":center_caravan", 0),
              (assign, ":done", 1),
              (assign, ":quest_target_party_template", ":center_caravan"),
              (assign, ":min_amount", 3),
            (else_try),
              (eq, ":done", 0),
              (le, ":random_no", 1),
              (gt, ":center_patrol", 0),
              (assign, ":done", 1),
              (assign, ":quest_target_party_template", ":center_patrol"),
              (assign, ":min_amount", 3),
            (else_try),
              (eq, ":done", 0),
              (le, ":random_no", 2),
              (gt, ":center_raiders", 0),
              (assign, ":done", 1),
              (assign, ":quest_target_party_template", ":center_raiders"),
              (assign, ":min_amount", 4),
            (else_try),
              (eq, ":done", 0),
              (gt, ":center_scouts", 0),
              (assign, ":done", 1),
              (assign, ":quest_target_party_template", ":center_scouts"),
              (assign, ":min_amount", 5),
            (try_end),
            
            (eq, ":done", 1), #should never happen, but who knows
            # get a random party, used only to find the template name - won't work for caravans with changed names!
            #(store_random_party_of_template, ":quest_target_party" ":quest_target_party_template"), #can fail, expensive
            
            (assign, ":quest_target_amount", ":player_level"),
            (val_clamp, ":quest_target_amount", 10, 31), #10-30
            (val_add, ":quest_target_amount", 10), #20-40
            (val_mul, ":quest_target_amount", 5), #100-200
            (val_mul, ":quest_target_amount", ":min_amount"),
            (val_div, ":quest_target_amount", 100), #min_amount - 2*min_amount
            
            (store_num_parties_destroyed_by_player, ":num_already_destroyed", ":quest_target_party_template"),
            (party_template_set_slot, ":quest_target_party_template", slot_party_template_num_killed, ":num_already_destroyed"),
            
            (assign, ":quest_importance", 12),
            (store_mul, ":quest_gold_reward", ":quest_target_amount", 100),
            (store_mul, ":quest_xp_reward", ":quest_target_amount", 40),
            (store_mul, ":quest_rank_reward", ":quest_target_amount", 4),
            
            (assign, ":result", ":quest_no"),
            (assign, ":quest_expiration_days", 40),
            (assign, ":quest_dont_give_again_period", 20),
          (try_end),
        (try_end),
      (try_end),
      (try_begin),
        (neq, ":result", -1),
        
        (try_begin),
          (ge, ":quest_target_center", 0),
          (store_faction_of_party, ":quest_target_faction", ":quest_target_center"),
        (try_end),
        
        (quest_set_slot, ":result", slot_quest_target_troop, ":quest_target_troop"),
        (quest_set_slot, ":result", slot_quest_target_center, ":quest_target_center"),
        (quest_set_slot, ":result", slot_quest_object_troop, ":quest_object_troop"),
        (quest_set_slot, ":result", slot_quest_target_faction, ":quest_target_faction"),
        (quest_set_slot, ":result", slot_quest_object_faction, ":quest_object_faction"),
        (quest_set_slot, ":result", slot_quest_object_center, ":quest_object_center"),
        (quest_set_slot, ":result", slot_quest_target_party, ":quest_target_party"),
        (quest_set_slot, ":result", slot_quest_target_party_template, ":quest_target_party_template"),
        (quest_set_slot, ":result", slot_quest_target_amount, ":quest_target_amount"),
        (quest_set_slot, ":result", slot_quest_importance, ":quest_importance"),
        (quest_set_slot, ":result", slot_quest_xp_reward, ":quest_xp_reward"),
        (quest_set_slot, ":result", slot_quest_gold_reward, ":quest_gold_reward"),
        (quest_set_slot, ":result", slot_quest_rank_reward, ":quest_rank_reward"),
        (quest_set_slot, ":result", slot_quest_convince_value, ":quest_convince_value"),
        (quest_set_slot, ":result", slot_quest_expiration_days, ":quest_expiration_days"),
        (quest_set_slot, ":result", slot_quest_dont_give_again_period, ":quest_dont_give_again_period"),
        (quest_set_slot, ":result", slot_quest_current_state, 0),
        (quest_set_slot, ":result", slot_quest_giver_troop, ":giver_troop"),
        (quest_set_slot, ":result", slot_quest_giver_center, ":giver_center_no"),
        (quest_set_slot, ":result", slot_quest_target_dna, ":quest_target_dna"),
        (quest_set_slot, ":result", slot_quest_target_item, ":quest_target_item"),
      (try_end),
      (assign, reg0, ":result"),
]),

# script_cf_get_random_enemy_center_within_range
# INPUT: arg1 = party_no, arg2 = range (in kms)
#OUTPUT: reg0 = center_no, reg1 = distance
("cf_get_random_enemy_center_within_range",
    [ (store_script_param, ":party_no", 1),
      (store_script_param, ":range", 2),
      (assign, ":num_centers", 0),
      (assign, ":dist", 0),
      (store_faction_of_party, ":faction_no", ":party_no"),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
		(party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (lt, ":cur_relation", 0),
        #(store_distance_to_party_from_party, ":dist", ":party_no", ":cur_center"),
        (call_script, "script_get_tld_distance", ":party_no", ":cur_center"),
        (assign, ":dist", reg0),
        (le, ":dist", ":range"),
        (val_add, ":num_centers", 1),
      (try_end),
      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":end_cond", centers_end),
      (try_for_range, ":cur_center", centers_begin, ":end_cond"),
        (party_is_active, ":cur_center"), #TLD
		(party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (lt, ":cur_relation", 0),
        #(store_distance_to_party_from_party, ":dist", ":party_no", ":cur_center"),
        (call_script, "script_get_tld_distance", ":party_no", ":cur_center"),
        (assign, ":dist", reg0),
        (le, ":dist", ":range"),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
        (assign, ":end_cond", 0),#break
      (try_end),
      (assign, reg0, ":result"),
      (assign, reg1, ":dist"),
]),

# script_cf_faction_get_random_enemy_faction
# INPUT: arg1 = faction_no
#OUTPUT: reg0 = faction_no (Can fail)
("cf_faction_get_random_enemy_faction",
    [ (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (le, ":cur_relation", -1),
        (val_add, ":count_factions", 1),
      (try_end),
      (store_random_in_range,":random_faction",0,":count_factions"),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (eq, ":result", -1),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (le, ":cur_relation", -1),
        (val_add, ":count_factions", 1),
        (gt, ":count_factions", ":random_faction"),
        (assign, ":result", ":cur_faction"),
      (try_end),
      
      (neq, ":result", -1),
      (assign, reg0, ":result"),
]),

# script_cf_faction_get_random_friendly_faction
# INPUT: arg1 = faction_no
#OUTPUT: reg0 = faction_no (Can fail)
("cf_faction_get_random_friendly_faction",
    [ (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (neq, ":cur_faction", ":faction_no"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (ge, ":cur_relation", 0),
        (val_add, ":count_factions", 1),
      (try_end),
      (store_random_in_range,":random_faction",0,":count_factions"),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (eq, ":result", -1),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (neq, ":cur_faction", ":faction_no"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (ge, ":cur_relation", 0),
        (val_add, ":count_factions", 1),
        (gt, ":count_factions", ":random_faction"),
        (assign, ":result", ":cur_faction"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
]),  

# script_cf_get_random_lord_in_a_center_with_faction
# INPUT: arg1 = faction_no
#OUTPUT: reg0 = troop_no, Can Fail! reg1 = distance
#TLD change: all allied lords, not only faction lords
("cf_get_random_lord_in_a_center_with_faction",
    [ (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":dist", 0),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        #(eq, ":faction_no", ":lord_faction_no"),
        (store_relation, ":relation", ":faction_no", ":lord_faction_no"),
        (ge, ":relation", 0), #TLD: allied lords
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        #(store_distance_to_party_from_party, ":dist", "p_main_party", ":lord_attachment"),
        (call_script, "script_get_tld_distance", "p_main_party", ":lord_attachment"),
        (assign, ":dist", reg0),
        (le, ":dist", tld_max_quest_distance), #TLD: not too far
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        #(eq, ":faction_no", ":lord_faction_no"),
        (store_relation, ":relation", ":faction_no", ":lord_faction_no"),
        (ge, ":relation", 0), #TLD: allied lords
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        #(store_distance_to_party_from_party, ":dist", "p_main_party", ":lord_attachment"),
        (call_script, "script_get_tld_distance", "p_main_party", ":lord_attachment"),
        (assign, ":dist", reg0),
        (le, ":dist", tld_max_quest_distance), #TLD: not too far
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
      (assign, reg1, ":dist"),
]),

# script_cf_get_random_lord_except_king_with_faction
# Input: arg1 = faction_no
# Output: reg0 = troop_no, Can Fail!
("cf_get_random_lord_except_king_with_faction",
    [ (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
]),

# script_cf_get_random_lord_from_enemy_faction_in_a_center
# Input: arg1 = faction_no
# Output: reg0 = troop_no, Can Fail! reg1 = distance
#TLD: gets an enemy lord - removed friendly-to-player condition, it will never happen
("cf_get_random_lord_from_enemy_faction_in_a_center",
    [ (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":dist", 0),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (neq, ":lord_faction_no", ":faction_no"),
        # (store_relation, ":our_relation", ":lord_faction_no", "fac_player_supporters_faction"),
        (store_relation, ":lord_relation", ":lord_faction_no", ":faction_no"),
        (lt, ":lord_relation", 0),
        # (ge, ":our_relation", 0),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        #(store_distance_to_party_from_party, ":dist", "p_main_party", ":lord_attachment"),
        (call_script, "script_get_tld_distance", "p_main_party", ":lord_attachment"),
        (assign, ":dist", reg0),
        (le, ":dist", tld_max_quest_distance), #TLD: not too far
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (neq, ":lord_faction_no", ":faction_no"),
        # (store_relation, ":our_relation", ":lord_faction_no", "fac_player_supporters_faction"),
        (store_relation, ":lord_relation", ":lord_faction_no", ":faction_no"),
        (lt, ":lord_relation", 0),
        # (ge, ":our_relation", 0),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        #(store_distance_to_party_from_party, ":dist", "p_main_party", ":lord_attachment"),
        (call_script, "script_get_tld_distance", "p_main_party", ":lord_attachment"),
        (assign, ":dist", reg0),
        (le, ":dist", tld_max_quest_distance), #TLD: not too far
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
      (assign, reg1, ":dist"),
]),

# script_get_closest_center
# Input: arg1 = party_no
# Output: reg0 = center_no (closest)
("get_closest_center",
    [ (store_script_param_1, ":party_no"),
      (assign, ":min_distance", 9999999),
      (assign, reg0, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, reg0, ":center_no"),
      (try_end),
]),

# script_get_close_landmark (mtarini) MV: corrected typo so searching for script_get_close_landmark works
# a landmark is more generic that just a center. Not only towns but every 3D object visibile on the map is a landmark
# Input: arg1 = party_no
# Output: reg0 = landmark no (closest, max dist 4),. Else -1
("get_close_landmark",
    [ (store_script_param_1, ":party_no"),
      (assign, ":min_distance", 6), # max range of landmarks
      (assign, reg0, -1),
	  
      (try_for_range, ":center_no", landmark_begin, landmark_end),
        (party_is_active, ":center_no"), #MV: Barad Dur caused script errors, probably because it was destroyed
		(this_or_next|eq, ":center_no", "p_town_erebor"), # erebor looks the same if destroyed
		(this_or_next|eq, ":center_no", "p_town_isengard"), # iseengard looks the same if destroyed
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # destroyed stuff are not landmarks
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, reg0, ":center_no"),
      (try_end),
	  
	  (try_begin),(eq, reg0, "p_town_minas_tirith"), (assign, ":sight_range", 4),
	  (else_try), (eq, reg0,  "p_town_erebor"), (assign, ":sight_range", 4),
	  (else_try), (eq, reg0,  "p_town_isengard"), (assign, ":sight_range", 6),
	  (else_try), (assign, ":sight_range", 2.5),(try_end), # default
	  
	  (try_begin),
		(gt, ":min_distance", ":sight_range"), # smaller sigth range of everything but minas thirit
		(assign, reg0, -1),
	  (try_end),
	  
	  (try_begin),(eq, reg0, -1), # no landmark found
		(set_fixed_point_multiplier,100.0),
		(party_get_position, pos10, ":party_no"),
	    (position_get_x,":x",pos10),(position_get_y,":y",pos10),
		(is_between, ":y", -19130, -18800),
		(try_begin), (gt, ":x", -2072),
			(assign, reg0, landmark_great_east_road ),
		(else_try),
			(assign, reg0, landmark_old_forest_road  ),
		(try_end),
	  (try_end),
]),

# script_cf_store_landmark_description_in_s17 (mtarini) MV: corrected careless copy/paste
# a landmark is more generic that just a center. Not only towns but every 3D object visibile on the map is a landmark
# Output: s17: the string
("cf_store_landmark_description_in_s17", [
	(store_script_param_1, ":landmark"),
	(ge, ":landmark", 0),
	
	(assign, ":ok", 1),
	(try_begin),
		(eq, ":landmark", landmark_great_east_road ),
		(str_store_string, s17, "@near the Great East Road, the abandoned old road"),
	(else_try),
		(eq, ":landmark", landmark_old_forest_road ),
		(str_store_string, s17, "@near what is left of the Old Forest Road, the ancient dwarven path that used to cross the thick forest"),
	(else_try),
		(str_store_party_name, s15, ":landmark"),
		(eq,":landmark","p_hand_isen"),	
		(str_store_string, s17, "@close to the Hand-shaped sign of Saruman, pointing toward the tower of Orthanc"),
	(else_try),
		(eq,":landmark","p_town_minas_tirith"),	
		(str_store_string, s17, "@in sight of the majestic City Walls of Minas Tirith, the White City"),
	(else_try),
		(eq,":landmark","p_town_erebor"),	
		(str_store_string, s17, "@in sight of the entrance to Erebor, the dwarven fortress"),
	(else_try),
		(eq,":landmark","p_town_isengard"),	
		(str_store_string, s17, "@in sight of the dark Tower of Orthanc"),
	(else_try),
		(eq,":landmark","p_old_ford"),
		(str_store_string, s17, "@near the Old Ford, where the Old Forest Road crosses the River Anduin"),
	(else_try),
		(is_between,":landmark",fords_big_begin, fords_big_end), # Anduin fords
		(str_store_string, s17, "@near a big ford crossing the River {s15}"),
	(else_try),
		(is_between,":landmark",fords_small_begin, fords_small_end), # small fords
		(str_store_string, s17, "@near a small ford crossing the River {s15}"),
	(else_try),
		(assign, ":ok", 0), # no good description found
	(try_end),
	(eq, ":ok", 1),
]),

# script_get_closest_walled_center_of_faction
# Input: arg1 = party_no, arg2 = kingdom_no
# Output: reg0 = center_no (closest)
("get_closest_center_of_faction",
    [ (store_script_param_1, ":party_no"),
      (store_script_param_2, ":kingdom_no"),
      (assign, ":min_distance", 99999),
      (assign, ":result", -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", ":kingdom_no"),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
]),

# script_let_nearby_parties_join_current_battle
# Input: arg1 = besiege_mode, arg2 = dont_add_friends
# Output: none
("let_nearby_parties_join_current_battle",
    [ (store_script_param, ":besiege_mode", 1),
      (store_script_param, ":dont_add_friends", 2),
      (assign, ":join_distance", 4),
      (try_begin),
        (is_currently_night),
        (assign, ":join_distance", 2),
      (try_end),
      (try_for_parties, ":party_no"),
        (party_is_active, ":party_no"), # Warband fix
        (party_get_battle_opponent, ":opponent",":party_no"),
        (lt, ":opponent", 0), #party is not itself involved in a battle
        (party_get_attached_to, ":attached_to",":party_no"),
        (lt, ":attached_to", 0), #party is not attached to another party
        (get_party_ai_behavior, ":behavior", ":party_no"),
        (neq, ":behavior", ai_bhvr_in_town),
        (neg|party_slot_eq, ":party_no", slot_party_type, spt_cattle_herd), #TLD: "cattle" won't join
      
        (store_distance_to_party_from_party, ":distance", ":party_no", "p_main_party"),
        (lt, ":distance", ":join_distance"),

        (store_faction_of_party, ":faction_no", ":party_no"),
        (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
        (try_begin),
          (eq, ":faction_no", "fac_player_supporters_faction"),
          (assign, ":reln_with_player", 100),
        (else_try),
          (store_relation, ":reln_with_player", ":faction_no", "fac_player_supporters_faction"),
        (try_end),
        (try_begin),
          (eq, ":faction_no", ":enemy_faction"),
          (assign, ":reln_with_enemy", 100),
        (else_try),
          (store_relation, ":reln_with_enemy", ":faction_no", ":enemy_faction"),
        (try_end),

        (assign, ":enemy_side", 1),
        (try_begin),
          (neq, "$g_enemy_party", "$g_encountered_party"),
          (assign, ":enemy_side", 2),
        (try_end),

        (try_begin),
          (eq, ":besiege_mode", 0),
          (lt, ":reln_with_player", 0),
          (gt, ":reln_with_enemy", 0),
          (party_get_slot, ":party_type", ":party_no"),
          #(eq, ":party_type", spt_kingdom_hero_party), #TLD: all parties can join
          (neq, ":party_type", spt_town), #...except towns

          (get_party_ai_behavior, ":ai_bhvr", ":party_no"),
          (neq, ":ai_bhvr", ai_bhvr_avoid_party),
          (party_quick_attach_to_current_battle, ":party_no", ":enemy_side"), #attach as enemy
          (str_store_party_name, s1, ":party_no"),
          (display_message, "str_s1_joined_battle_enemy", color_bad_news),
        (else_try),
          (eq, ":dont_add_friends", 0),
          (gt, ":reln_with_player", 0),
          (lt, ":reln_with_enemy", 0),
          (assign, ":do_join", 1),
          (try_begin),
            (eq, ":besiege_mode", 1),
            (assign, ":do_join", 0),
            # (eq, ":faction_no", "$players_kingdom"),
            # (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
            # (assign, ":do_join", 1),
          (try_end),
          (eq, ":do_join", 1),
          (party_get_slot, ":party_type", ":party_no"),
          #(eq, ":party_type", spt_kingdom_hero_party), #TLD: all parties can join
          (neq, ":party_type", spt_town), #...except towns

          #MV commented out personal relations
          #(party_stack_get_troop_id, ":leader", ":party_no", 0),
   #       (troop_get_slot, ":player_relation", ":leader", slot_troop_player_relation),
          #(call_script, "script_troop_get_player_relation", ":leader"),
          #(assign, ":player_relation", reg0),
          #(ge, ":player_relation", 0),
          (party_quick_attach_to_current_battle, ":party_no", 0), #attach as friend
          (str_store_party_name, s1, ":party_no"),
          (display_message, "str_s1_joined_battle_friend", color_good_news),
        (try_end),
      (try_end),
]),

# script_party_wound_all_members
# Input: arg1 = party_no
("party_wound_all_members_aux",
    [ (store_script_param_1, ":party_no"),
      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
          (party_wound_members, ":party_no", ":stack_troop", ":stack_size"),
        (else_try),
          (troop_set_health, ":stack_troop", 0),
        (try_end),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
        (call_script, "script_party_wound_all_members", ":attached_party"),
      (try_end),
]),

# script_party_wound_all_members. identical to script_party_wound_all_members
# Input: arg1 = party_no
("party_wound_all_members",
    [ (store_script_param_1, ":party_no"),
      (call_script, "script_party_wound_all_members", ":party_no"),
]),

# script_calculate_battle_advantage
# Output: reg0 = battle advantage
("calculate_battle_advantage",
    [ (call_script, "script_party_count_fit_for_battle", "p_collective_friends"),
      (assign, ":friend_count", reg0),
      (party_get_skill_level, ":player_party_tactics",  "p_main_party", skl_tactics),
      (party_get_skill_level, ":ally_party_tactics",  "p_collective_friends", skl_tactics),
      (val_max, ":player_party_tactics", ":ally_party_tactics"),
      (call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
      (assign, "$enemy_count1", reg0), ## of enemies also for scenes
  ## TLD, total number of combatants, needed for random scene generation, GA
	  (store_add, "$number_of_combatants", ":friend_count","$enemy_count1"),
      (party_get_skill_level, ":enemy_party_tactics",  "p_collective_enemy", skl_tactics),
      (val_add, ":friend_count", 1),
      (val_add, "$enemy_count1", 1),
      (try_begin),
        (ge, ":friend_count", "$enemy_count1"),
        (val_mul, ":friend_count", 100),
        (store_div, ":ratio", ":friend_count", "$enemy_count1"),
        (store_sub, ":raw_advantage", ":ratio", 100),
      (else_try),
        (val_mul, "$enemy_count1", 100),
        (store_div, ":ratio", "$enemy_count1", ":friend_count"),
        (store_sub, ":raw_advantage", 100, ":ratio"),
      (try_end),
      (val_mul, ":raw_advantage", 2),
      (val_mul, ":player_party_tactics", 30),
      (val_mul, ":enemy_party_tactics", 30),
      (val_add, ":raw_advantage", ":player_party_tactics"),
      (val_sub, ":raw_advantage", ":enemy_party_tactics"),
      (val_div, ":raw_advantage", 100),
      (assign, reg0, ":raw_advantage"),
      (display_message, "@Battle Advantage = {reg0}.", 0xFFFFFFFF),
]),

# script_cf_check_enemies_nearby
# Input: none
# Output: none, fails when enemies are nearby
("cf_check_enemies_nearby",
    [ (get_player_agent_no, ":player_agent"),
      (agent_is_alive, ":player_agent"),
      (agent_get_position, pos1, ":player_agent"),
      (assign, ":result", 0),
      (set_fixed_point_multiplier, 100),
      (try_for_agents,":cur_agent"),
        (neq, ":cur_agent", ":player_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (neg|agent_is_ally, ":cur_agent"),
        (agent_get_position, pos2, ":cur_agent"),
        (get_distance_between_positions, ":cur_distance", pos1, pos2),
        (le, ":cur_distance", 1500), #15 meters
        (assign, ":result", 1),
      (try_end),
      (eq, ":result", 0),
]),

# script_get_heroes_attached_to_center_aux
# For internal use only
("get_heroes_attached_to_center_aux",
    [ (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_get_num_companion_stacks, ":num_stacks",":center_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":center_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (party_add_members, ":party_no_to_collect_heroes", ":stack_troop", 1),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":center_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":attached_party_rank"),
        (call_script, "script_get_heroes_attached_to_center_aux", ":attached_party", ":party_no_to_collect_heroes"),
      (try_end),
]),

# script_get_heroes_attached_to_center
# Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
# Output: none, adds heroes to the party_no_to_collect_heroes party
("get_heroes_attached_to_center",
    [ (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),
      (call_script, "script_get_heroes_attached_to_center_aux", ":center_no", ":party_no_to_collect_heroes"),
]),

# script_get_heroes_attached_to_center_as_prisoner_aux
# For internal use only
("get_heroes_attached_to_center_as_prisoner_aux",
    [ (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_get_num_prisoner_stacks, ":num_stacks",":center_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":center_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (party_add_members, ":party_no_to_collect_heroes", ":stack_troop", 1),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":center_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":attached_party_rank"),
        (call_script, "script_get_heroes_attached_to_center_as_prisoner_aux", ":attached_party", ":party_no_to_collect_heroes"),
      (try_end),
]),

# script_get_heroes_attached_to_center_as_prisoner
# Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
# Output: none, adds heroes to the party_no_to_collect_heroes party
("get_heroes_attached_to_center_as_prisoner",
    [ (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),
      (call_script, "script_get_heroes_attached_to_center_as_prisoner_aux", ":center_no", ":party_no_to_collect_heroes"),
]),

# script_give_center_to_faction
# Input: arg1 = center_no, arg2 = faction
("give_center_to_faction",
    [ (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),
      (try_begin),
        (check_quest_active, "qst_join_siege_with_army"),
        (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, ":center_no"),
        (call_script, "script_abort_quest", "qst_join_siege_with_army", 0),
        #Reactivating follow army quest
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name_link, s9, ":faction_marshall"),
        (setup_quest_text, "qst_follow_army"),
        (str_store_string, s2, "@{s9} wants you to resume following his army until further notice."),
        (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
        #(assign, "$g_player_follow_army_warnings", 0),
      (try_end),
      (store_faction_of_party, ":old_faction", ":center_no"),
      (call_script, "script_give_center_to_faction_aux", ":center_no", ":faction_no"),
      #(call_script, "script_update_village_market_towns"),
      
      # If this is Edoras and Hornburg is still Rohan's, move capital
      (try_begin),
        (eq, ":center_no", "p_town_edoras"),
        (eq, ":old_faction", "fac_rohan"),
        (faction_slot_eq, "fac_rohan", slot_faction_capital, "p_town_edoras"),
        (store_faction_of_party, ":hornburg_faction", "p_town_hornburg"),
        (eq, ":hornburg_faction", "fac_rohan"),
        (faction_set_slot, "fac_rohan", slot_faction_capital, "p_town_hornburg"),
        (display_message, "@Rohan capital moved from Edoras to Hornburg!"),
      (try_end),

      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":cur_faction"),
      (try_end),
      (assign, "$g_recalculate_ais", 1),
]),

# script_give_center_to_faction_aux
# Input: arg1 = center_no, arg2 = faction
("give_center_to_faction_aux",
    [ (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),
      (store_faction_of_party, ":old_faction", ":center_no"),
      (party_set_slot, ":center_no", slot_center_ex_faction, ":old_faction"),
      (party_set_faction, ":center_no", ":faction_no"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (party_get_slot, ":farmer_party", ":center_no", slot_village_farmer_party),
        (gt, ":farmer_party", 0),
        (party_is_active, ":farmer_party"),
        (party_set_faction, ":farmer_party", ":faction_no"),
      (try_end),

      (party_get_slot, ":old_town_lord", ":center_no", slot_town_lord),
      
      #TLD changes: give captured centers to kings, place faction banner
      (faction_get_slot, ":king", ":faction_no", slot_faction_leader),
      (party_set_slot, ":center_no", slot_town_lord, ":king"),
	  (faction_get_slot,":faction_banner",":faction_no",slot_faction_party_map_banner),
      (party_set_banner_icon, ":center_no", ":faction_banner"),
      #TLD: change NPCs and walkers - since I'm lazy, I'll just give them clones of the faction capital NPCs and walkers
      (faction_get_slot, ":capital", ":faction_no", slot_faction_capital),
      (party_get_slot, ":value", ":capital", slot_town_elder),
      (party_set_slot, ":center_no", slot_town_elder, ":value"),
      (party_get_slot, ":value", ":capital", slot_town_barman),
      (party_set_slot, ":center_no", slot_town_barman, ":value"),
      (party_get_slot, ":value", ":capital", slot_town_weaponsmith),
      (party_set_slot, ":center_no", slot_town_weaponsmith, ":value"),
      (party_get_slot, ":value", ":capital", slot_town_merchant),
      (party_set_slot, ":center_no", slot_town_merchant, ":value"),
      (party_get_slot, ":value", ":capital", slot_town_recruits_pt),
      (party_set_slot, ":center_no", slot_town_recruits_pt, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_0_troop),
      (party_set_slot, ":center_no", slot_center_walker_0_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_1_troop),
      (party_set_slot, ":center_no", slot_center_walker_1_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_2_troop),
      (party_set_slot, ":center_no", slot_center_walker_2_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_3_troop),
      (party_set_slot, ":center_no", slot_center_walker_3_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_4_troop),
      (party_set_slot, ":center_no", slot_center_walker_4_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_5_troop),
      (party_set_slot, ":center_no", slot_center_walker_5_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_6_troop),
      (party_set_slot, ":center_no", slot_center_walker_6_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_7_troop),
      (party_set_slot, ":center_no", slot_center_walker_7_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_8_troop),
      (party_set_slot, ":center_no", slot_center_walker_8_troop, ":value"),
      (party_get_slot, ":value", ":capital", slot_center_walker_9_troop),
      (party_set_slot, ":center_no", slot_center_walker_9_troop, ":value"),
      (faction_get_slot, ":value", ":faction_no", slot_faction_guard_troop),
      (party_set_slot, ":center_no", slot_town_guard_troop, ":value"),
      (faction_get_slot, ":value", ":faction_no", slot_faction_prison_guard_troop),
      (party_set_slot, ":center_no", slot_town_prison_guard_troop, ":value"),
      (faction_get_slot, ":value", ":faction_no", slot_faction_castle_guard_troop),
      (party_set_slot, ":center_no", slot_town_castle_guard_troop, ":value"),
      
      # Change center spawns to be the same as for faction advance camps, only if there was such a spawn before
      (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
      (try_begin),
        (party_get_slot, ":old_value", ":center_no", slot_center_spawn_scouts),
        (gt, ":old_value", 0),
        (party_get_slot, ":value", ":adv_camp", slot_center_spawn_scouts),
        (party_set_slot, ":center_no", slot_center_spawn_scouts, ":value"),
      (try_end),
      (try_begin),
        (party_get_slot, ":old_value", ":center_no", slot_center_spawn_raiders),
        (gt, ":old_value", 0),
        (party_get_slot, ":value", ":adv_camp", slot_center_spawn_raiders),
        (party_set_slot, ":center_no", slot_center_spawn_raiders, ":value"),
      (try_end),
      (try_begin),
        (party_get_slot, ":old_value", ":center_no", slot_center_spawn_patrol),
        (gt, ":old_value", 0),
        (party_get_slot, ":value", ":adv_camp", slot_center_spawn_patrol),
        (party_set_slot, ":center_no", slot_center_spawn_patrol, ":value"),
      (try_end),
      (try_begin),
        (party_get_slot, ":old_value", ":center_no", slot_center_spawn_caravan),
        (gt, ":old_value", 0),
        (party_get_slot, ":value", ":adv_camp", slot_center_spawn_caravan),
        (party_set_slot, ":center_no", slot_center_spawn_caravan, ":value"),
      (try_end),
      
      #reduce income to 5 if non-zero
      (party_get_slot, ":strength_income", ":center_no", slot_center_strength_income),
      (val_min, ":strength_income", str_income_low),
      (party_set_slot, ":center_no", slot_center_strength_income, ":strength_income"),
      
      #TLD: old faction loses faction strength
      # (faction_get_slot,":strength",":old_faction",slot_faction_strength_tmp),
      # (val_sub, ":strength", ws_center_vp),
      # (faction_set_slot,":old_faction",slot_faction_strength_tmp,":strength"),
      # #debug stuff
      # (faction_get_slot, ":debug_loss", ":old_faction", slot_faction_debug_str_loss),
      # (val_add, ":debug_loss", ws_center_vp),
      # (faction_set_slot, ":old_faction", slot_faction_debug_str_loss, ":debug_loss"),
      # #TLD: conquering faction gains faction strength
      # (faction_get_slot,":winner_strength",":faction_no",slot_faction_strength_tmp),
      # (store_div, ":win_value", ws_center_vp, 2), #this formula could be balanced after playtesting
      # (val_add, ":winner_strength", ":win_value"),
      # (faction_set_slot,":faction_no",slot_faction_strength_tmp,":winner_strength"),
      # #debug stuff
      # (faction_get_slot, ":debug_gain", ":faction_no", slot_faction_debug_str_gain),
      # (val_add, ":debug_gain", ":win_value"),
      # (faction_set_slot, ":faction_no", slot_faction_debug_str_gain, ":debug_gain"),
      # #debug
      # (try_begin),
        # (eq, cheat_switch, 1),
        # (assign,reg0,ws_center_vp),
        # (assign,reg1,":strength"),
        # (assign,reg2,":win_value"),
        # (assign,reg3,":winner_strength"),
        # (str_store_faction_name,s1,":old_faction"),
        # (str_store_faction_name,s2,":faction_no"),
        # (str_store_party_name,s3,":center_no"),
        # (display_message,"@DEBUG: {s3} captured: {s1} strength -{reg0} to {reg1}, {s2} strength +{reg2} to {reg3}."),
      # (try_end),

      (call_script, "script_update_faction_notes", ":old_faction"),
      (call_script, "script_update_faction_notes", ":faction_no"),
      (call_script, "script_update_center_notes", ":center_no"),
      (call_script, "script_update_troop_notes", ":king"), # TLD
      (try_begin),
        (ge, ":old_town_lord", 0),
        (call_script, "script_update_troop_notes", ":old_town_lord"),
      (try_end),

      (try_for_range, ":other_center", centers_begin, centers_end),
        (party_is_active, ":other_center"), #TLD
		(party_slot_eq, ":other_center", slot_center_destroyed, 0), # TLD
        (party_slot_eq, ":other_center", slot_village_bound_center, ":center_no"),
        (call_script, "script_give_center_to_faction_aux", ":other_center", ":faction_no"),
      (try_end),
]),

# script_give_center_to_lord  # in TLD, used only at inital setup
# Input: arg1 = center_no, arg2 = lord_troop, arg3 = add_garrison_to_center
("give_center_to_lord",
    [ (store_script_param, ":center_no", 1),
      (store_script_param, ":lord_troop_id", 2),
      (store_script_param, ":add_garrison", 3),

      (party_get_slot, ":old_lord_troop_id", ":center_no", slot_town_lord),
      
      (store_troop_faction, ":lord_troop_faction", ":lord_troop_id"),
	  
      (party_set_faction, ":center_no", ":lord_troop_faction"),
      (party_set_slot, ":center_no", slot_town_lord, ":lord_troop_id"),

      (call_script, "script_update_troop_notes", ":lord_troop_id"),
      (call_script, "script_update_center_notes", ":center_no"),
      (call_script, "script_update_faction_notes", ":lord_troop_faction"),
      (try_begin),
        (ge, ":old_lord_troop_id", 0),
        (call_script, "script_update_troop_notes", ":old_lord_troop_id"),
        (store_troop_faction, ":old_lord_troop_faction", ":old_lord_troop_id"),
        (call_script, "script_update_faction_notes", ":old_lord_troop_faction"),
      (try_end),

      (try_begin),
        (eq, ":add_garrison", 1),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":garrison_strength", 3), 
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (assign, ":garrison_strength", 9),
        (try_end),
        (try_for_range, ":unused", 0, ":garrison_strength"),
          (call_script, "script_cf_reinforce_party", ":center_no"),
        (try_end),
        ## ADD some XP initially
        (try_for_range, ":unused", 0, 7),
          (store_random_in_range, ":xp", 1500, 2000),
          (party_upgrade_with_xp, ":center_no", ":xp", 0),
        (try_end),
      (try_end),
]),

# script_cf_get_random_enemy_center
# Input: arg1 = party_no
# Output: reg0 = center_no
("cf_get_random_enemy_center",
    [ (store_script_param_1, ":party_no"),
      (assign, ":result", -1),
      (assign, ":total_enemy_centers", 0),
      (store_faction_of_party, ":party_faction", ":party_no"),
      
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_relation, ":party_relation", ":center_faction", ":party_faction"),
        (lt, ":party_relation", 0),
        (val_add, ":total_enemy_centers", 1),
      (try_end),

      (gt, ":total_enemy_centers", 0),
      (store_random_in_range, ":random_center", 0, ":total_enemy_centers"),
      (assign, ":total_enemy_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (eq, ":result", -1),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_relation, ":party_relation", ":center_faction", ":party_faction"),
        (lt, ":party_relation", 0),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
]),

# script_find_travel_location
# Input: arg1 = center_no
# Output: reg0 = new_center_no (to travel within the same faction)
("find_travel_location",
    [ (store_script_param_1, ":center_no"),
      (store_faction_of_party, ":faction_no", ":center_no"),
      (assign, ":total_weight", 0),
      (try_for_range, ":cur_center_no", centers_begin, centers_end),
        (party_is_active, ":cur_center_no"), #TLD
		(party_slot_eq, ":cur_center_no", slot_center_destroyed, 0), # TLD
        (neq, ":center_no", ":cur_center_no"),
        (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
        (eq, ":faction_no", ":center_faction_no"),
        
        #(store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
        (call_script, "script_get_tld_distance", ":center_no", ":cur_center_no"),
        (assign, ":cur_distance", reg0),
        (val_add, ":cur_distance", 1),
        
        (assign, ":new_weight", 100000),
        (val_div, ":new_weight", ":cur_distance"),
        (val_add, ":total_weight", ":new_weight"),
      (try_end),
      (assign, reg0, -1),
      (try_begin),
        (eq, ":total_weight", 0),
      (else_try),
        (store_random_in_range, ":random_weight", 0 , ":total_weight"),
        (assign, ":total_weight", 0),
        (assign, ":done", 0),
        (try_for_range, ":cur_center_no", centers_begin, centers_end),
          (party_is_active, ":cur_center_no"), #TLD
		  (party_slot_eq, ":cur_center_no", slot_center_destroyed, 0), # TLD
          (eq, ":done", 0),
          (neq, ":center_no", ":cur_center_no"),
          (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
          (eq, ":faction_no", ":center_faction_no"),
          #(store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
          (call_script, "script_get_tld_distance", ":center_no", ":cur_center_no"),
          (assign, ":cur_distance", reg0),
          (val_add, ":cur_distance", 1),
          (assign, ":new_weight", 100000),
          (val_div, ":new_weight", ":cur_distance"),
          (val_add, ":total_weight", ":new_weight"),
          (lt, ":random_weight", ":total_weight"),
          (assign, reg0, ":cur_center_no"),
          (assign, ":done", 1),
        (try_end),
      (try_end),
]),

# script_get_relation_between_parties
# Input: arg1 = party_no_1, arg2 = party_no_2
# Output: reg0 = relation between parties
("get_relation_between_parties",
    [ (store_script_param_1, ":party_no_1"),
      (store_script_param_2, ":party_no_2"),
      (store_faction_of_party, ":party_no_1_faction", ":party_no_1"),
      (store_faction_of_party, ":party_no_2_faction", ":party_no_2"),
      (try_begin),
        (eq, ":party_no_1_faction", ":party_no_2_faction"),
        (assign, reg0, 100),
      (else_try),
        (store_relation, ":relation", ":party_no_1_faction", ":party_no_2_faction"),
        (assign, reg0, ":relation"),
      (try_end),
]),

# script_cf_reinforce_party
# Input: arg1 = party_no,
# Output: none
# Adds reinforcement to party according to its type and faction
("cf_reinforce_party",
    [ (store_script_param_1, ":party_no"),
      (store_faction_of_party, ":party_faction", ":party_no"),
      (party_get_slot, ":party_type",":party_no", slot_party_type),
      (try_begin),
        (eq, ":party_no", "p_main_party"), #for testing, but doesn't hurt
        (assign, ":party_type", spt_kingdom_hero_party),
        (assign, ":party_faction", "$players_kingdom"),
      (else_try),
        (eq, ":party_faction", "fac_player_supporters_faction"),
        (party_get_slot, ":town_lord", ":party_no", slot_town_lord),
        (try_begin),
          (gt, ":town_lord", 0),
          (troop_get_slot, ":party_faction", ":town_lord", slot_troop_original_faction),
        (else_try),
          (party_get_slot, ":party_faction", ":party_no", slot_center_original_faction),
        (try_end),
      (try_end),
      
      (faction_get_slot, ":party_template_a", ":party_faction", slot_faction_reinforcements_a),
      (faction_get_slot, ":party_template_b", ":party_faction", slot_faction_reinforcements_b),
      (faction_get_slot, ":party_template_c", ":party_faction", slot_faction_reinforcements_c),

	  # For Gondor subfaction garrisons, no harm for others (town_reinf=faction_reinf)
	  (try_begin),
        (eq, ":party_type", spt_town),
		(eq, ":party_faction", "fac_gondor"),
        (party_get_slot, ":party_template_a", ":party_no", slot_town_reinforcements_a),
        (party_get_slot, ":party_template_b", ":party_no", slot_town_reinforcements_b),
        (party_get_slot, ":party_template_c", ":party_no", slot_town_reinforcements_c),
      (try_end),

      (store_random_in_range, ":rand", 0, 100), # A, B, or C

	  (assign, ":offset", 0), 
	  # (MV: did) uncomment the following block to make a 8% of mixing between gondor subfactions
	  (try_begin), 
	  	(eq, ":party_faction", "fac_gondor"), # only in gondor....
		(store_random_in_range, ":rand2", 0, 100),
        (le, ":rand2", 20), # 20% of times... was 8%
        (party_get_slot, ":subfac", ":party_no", slot_party_subfaction),
		(try_begin),
			#Gondor subfaction lords get subfaction reinforcements, subfaction towns get Gondor reinforcements...
			(neq, ":subfac", 0),
            (try_begin),
              (eq, ":party_type", spt_town),
			  (faction_get_slot, ":party_template_a", ":party_faction", slot_faction_reinforcements_a),
			  (faction_get_slot, ":party_template_b", ":party_faction", slot_faction_reinforcements_b),
			  (faction_get_slot, ":party_template_c", ":party_faction", slot_faction_reinforcements_c),
            (else_try),
              (store_mul, ":offset", ":subfac", 3), 
            (try_end),
		(else_try),
			#regular Gondor parties get a random subfaction reinforcement...
			(store_random_in_range, ":offset", 1, len(subfaction_data)+1 ),
			(val_mul, ":offset", 3),
            #(val_mul,":rand",75),(val_div,":rand",100),  # but cannot pick "C" - MV: let them anyway
		(try_end),		
	  (try_end),

      (assign, ":party_template", 0),
      
      #MV/Native: different reinforcements for towns and heroes
      (try_begin),
        (eq, ":party_type", spt_town),
        (try_begin),
          (lt, ":rand", 60),
          (store_add, ":party_template", ":party_template_a", ":offset"), # base tier 1 and 2 troops
        (else_try),
          (lt, ":rand", 95),
          (store_add, ":party_template", ":party_template_b", ":offset"), # tier 3 archers mixed with other tier 3 troops and tier 2 archers
        (else_try),
          (store_add, ":party_template", ":party_template_c", ":offset"), # tier 4 troop mix
        (try_end),
      (else_try),
        #(eq, ":party_type", spt_kingdom_hero_party), #MV: hosts or guardians
        (try_begin),
          (lt, ":rand", 50),
          (store_add, ":party_template", ":party_template_a", ":offset"), # base tier 1 and 2 troops
        (else_try),
          (lt, ":rand", 80),
          (store_add, ":party_template", ":party_template_b", ":offset"), # tier 3 archers mixed with other tier 3 troops and tier 2 archers
        (else_try),
          (store_add, ":party_template", ":party_template_c", ":offset"), # tier 4 troop mix
        (try_end),
      (try_end),
      
	  (try_begin),
		(eq, ":party_no", "p_town_minas_tirith"), # special minas tirith rule,,,
		(store_random_in_range, ":rand2", 0, 100), (le, ":rand2", 20), # 20% of times...
		(assign, ":party_template", "pt_gondor_reinf_d"),
	  (try_end),
      
      (try_begin),
        (gt, ":party_template", 0),
        (party_is_active, ":party_no"), #TLD
		(party_slot_eq, ":party_no", slot_center_destroyed, 0), # TLD
        (party_add_template, ":party_no", ":party_template"),
      (try_end),
]),

# script_hire_men_to_kingdom_hero_party
# [Old TLD change: Hiring troops based on nearby town wealth instead of hero wealth]
# New TLD change: Hiring troops based only on current and ideal party size
# Input: arg1 = troop_no (hero of the party)
# Output: none
("hire_men_to_kingdom_hero_party",
    [ (store_script_param_1, ":troop_no"),
      (store_troop_faction, ":troop_faction", ":troop_no"),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        # (call_script, "script_find_random_nearby_friendly_town", ":party_no", 0),
        # (assign, ":nearby_center", reg0),
        # (party_get_slot, ":cur_wealth", ":nearby_center", slot_town_wealth),
      # (assign, ":hiring_budget", ":cur_wealth"),
      # (val_mul, ":hiring_budget", 4),
      # (val_div, ":hiring_budget", 5),
      (assign, ":num_rounds", 1),

	  #GA: add standard bearers to hero parties  
	  (try_begin),
        (eq,":troop_faction","fac_lorien"),
		(party_count_members_of_type,":num", ":party_no", "trp_lothlorien_standard_bearer"),
		(lt, ":num", 3),
		(party_add_members, ":party_no", "trp_lothlorien_standard_bearer", 2),
      (else_try),
        (eq,":troop_faction","fac_imladris"),
		(party_count_members_of_type,":num", ":party_no", "trp_rivendell_standard_bearer"),
		(lt, ":num", 3),
		(party_add_members, ":party_no", "trp_rivendell_standard_bearer", 2),
      (else_try),
        (eq,":troop_faction","fac_woodelf"),
		(party_count_members_of_type,":num", ":party_no", "trp_greenwood_standard_bearer"),
		(lt, ":num", 3),
		(party_add_members, ":party_no", "trp_greenwood_standard_bearer", 2),
      (else_try),
        (eq,":troop_faction","fac_mordor"),
		(party_count_members_of_type,":num", ":party_no", "trp_uruk_mordor_standard_bearer"),
		(lt, ":num", 4),
		(party_add_members, ":party_no", "trp_uruk_mordor_standard_bearer", 2),
      (else_try),
        (eq,":troop_faction","fac_isengard"),
		(party_count_members_of_type,":num", ":party_no", "trp_urukhai_standard_bearer"),
		(lt, ":num", 4),
		(party_add_members, ":party_no", "trp_urukhai_standard_bearer", 2),
      (try_end),

      (call_script, "script_party_get_ideal_size", ":party_no"),
      (assign, ":ideal_size", reg0),
#      (display_message, "@DEBUG: Host ideal size: {reg0}", debug_color),
      (store_mul, ":ideal_top_size", ":ideal_size", 3),
      (val_div, ":ideal_top_size", 2),
    
      (party_get_num_companions, ":party_size", ":party_no"),
      (try_for_range, ":unused", 0 , ":num_rounds"),
        (try_begin),
          (lt, ":party_size", ":ideal_size"),
#          (gt, ":hiring_budget", reinforcement_cost),
          (gt, ":party_no", 0),
          (call_script, "script_cf_reinforce_party", ":party_no"),
#          (val_sub, ":cur_wealth", reinforcement_cost),
#          (party_set_slot, ":nearby_center", slot_town_wealth, ":cur_wealth"), # TLD: wealth change to town
        (else_try),
          (gt, ":party_size", ":ideal_top_size"),
          (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
          (assign, ":total_regulars", 0),
          (assign, ":total_regular_levels", 0),
          (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
            (store_character_level, ":stack_level", ":stack_troop"),
            (store_troop_faction, ":stack_faction", ":stack_troop"),
            (try_begin),
              (eq, ":troop_faction", ":stack_faction"),
              (val_mul, ":stack_level", 3), #reducing the chance of the faction troops' removal
            (try_end),
            (val_mul, ":stack_level", ":stack_size"),
            (val_add, ":total_regulars", ":stack_size"),
            (val_add, ":total_regular_levels", ":stack_level"),
          (try_end),
          (gt, ":total_regulars", 0),
          (store_div, ":average_level", ":total_regular_levels", ":total_regulars"),
          (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
            (store_character_level, ":stack_level", ":stack_troop"),
            (store_troop_faction, ":stack_faction", ":stack_troop"),
            (try_begin),
              (eq, ":troop_faction", ":stack_faction"),
              (val_mul, ":stack_level", 3),
            (try_end),
            (store_sub, ":level_dif", ":average_level", ":stack_level"),
            (val_div, ":level_dif", 3),
            (store_add, ":prune_chance", 10, ":level_dif"),
            (gt, ":prune_chance", 0),
            (call_script, "script_get_percentage_with_randomized_round", ":stack_size", ":prune_chance"),
            (gt, reg0, 0),
            (party_remove_members, ":party_no", ":stack_troop", reg0),
          (try_end),
        (try_end),
      (try_end),
  #MV test code begin
  # (try_begin),
  # (eq, cheat_switch, 1),
  # (store_troop_faction, ":faction_no", ":troop_no"),
  # (this_or_next|eq, ":faction_no", "fac_gondor"),
  # (eq, ":faction_no", "fac_mordor"),
  # (assign, reg1, ":party_size"),
  # (assign, reg2, ":ideal_size"),
  # (str_store_troop_name, s1, ":troop_no"),
  # (party_get_num_companions, reg3, ":party_no"),
  # (display_message, "@DEBUG: {s1} reinforces, current:{reg1} ideal:{reg2} new:{reg3}.", 0x30FFC8),
  # (try_end),
  #MV test code end
]),

# script_find_random_nearby_friendly_town
# TLD script
# Input: arg1 = party_no, from where to find town; arg2 = include castles
# Output: reg0 = center party no
("find_random_nearby_friendly_town", [
    (store_script_param, ":party_no", 1),
    (store_script_param, ":c_castles", 2),
    (store_faction_of_party, ":party_faction", ":party_no"),
    (assign, ":min_dis", 10000000),
    (assign, reg0, -1),
    (try_for_parties, ":party"),
        (this_or_next|party_slot_eq, ":party", slot_party_type, spt_town),
        (neq, ":c_castles", 0),
        (this_or_next|party_slot_eq, ":party", slot_party_type, spt_town),
        (party_slot_eq, ":party", slot_party_type, spt_castle),
        (party_is_active, ":party"), #TLD
		(party_slot_eq, ":party", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":faction", ":party"),
        (eq, ":faction", ":party_faction"),
        (store_distance_to_party_from_party, ":dis", ":party", ":party_no"),
        (store_random_in_range, ":rand", 0, ":min_dis"),
        (this_or_next|gt, ":rand", ":dis"),
        (eq, reg0, -1),
        (assign, reg0, ":party"),
        (assign, ":min_dis", ":dis"),
    (try_end),
]),

# script_get_percentage_with_randomized_round
# Input: arg1 = value, arg2 = percentage
# Output: none
("get_percentage_with_randomized_round",
    [ (store_script_param, ":value", 1),
      (store_script_param, ":percentage", 2),

      (store_mul, ":result", ":value", ":percentage"),
      (val_div, ":result", 100),
      (store_mul, ":used_amount", ":result", 100),
      (val_div, ":used_amount", ":percentage"),
      (store_sub, ":left_amount", ":value", ":used_amount"),
      (try_begin),
        (gt, ":left_amount", 0),
        (store_mul, ":chance", ":left_amount", ":percentage"),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":chance"),
        (val_add, ":result", 1),
      (try_end),
      (assign, reg0, ":result"),
]),

# script_get_troop_attached_party
# Input: arg1 = troop_no
# Output: reg0 = party_no (-1 if troop's party is not attached to a party)
("get_troop_attached_party",
    [ (store_script_param_1, ":troop_no"),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (assign, ":attached_party_no", -1),
      (try_begin),
        (ge, ":party_no", 0),
        (party_get_attached_to, ":attached_party_no", ":party_no"),
      (try_end),
      (assign, reg0, ":attached_party_no"),
]),

# script_center_get_food_consumption
# Input: arg1 = center_no
# Output: reg0: food consumption (1 food item counts as 100 units)
("center_get_food_consumption",
    [ (store_script_param_1, ":center_no"),
      (assign, ":food_consumption", 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign, ":food_consumption", 500),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":food_consumption", 50),
      (try_end),
      (assign, reg0, ":food_consumption"),
]),

# script_center_get_food_store_limit
# Input: arg1 = center_no
# Output: reg0: food consumption (1 food item counts as 100 units)
("center_get_food_store_limit",
    [ (store_script_param_1, ":center_no"),
      (assign, ":food_store_limit", 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign, ":food_store_limit", 50000),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":food_store_limit", 1500),
      (try_end),
	(assign, reg0, ":food_store_limit"),
]),

# script_village_set_state
# Input: arg1 = center_no arg2:new_state
# Output: reg0: food consumption (1 food item counts as 100 units)
("village_set_state",[
      (store_script_param_1, ":village_no"),
      (store_script_param_2, ":new_state"),
#      (party_get_slot, ":old_state", ":village_no", slot_village_state),
      (try_begin),
        (eq, ":new_state", 0),
        (party_set_extra_text, ":village_no", "str_empty_string"),
        #(party_set_slot, ":village_no", slot_village_raided_by, -1),
      (else_try),
        (eq, ":new_state", svs_being_raided),
        (party_set_extra_text, ":village_no", "@(Being Raided)"),
      (else_try),
        (eq, ":new_state", svs_looted),
        (party_set_extra_text, ":village_no", "@(Looted)"),
        #(party_set_slot, ":village_no", slot_village_raided_by, -1),
        (call_script, "script_change_center_prosperity", ":village_no", -30),
      (else_try),
        (eq, ":new_state", svs_under_siege),
        (party_set_extra_text, ":village_no", "@(Under Siege)"),
      (try_end),
      #(party_set_slot, ":village_no", slot_village_state, ":new_state"),
]),

# script_process_sieges
#called from triggers
("process_sieges",
    [ (try_for_range, ":center_no", centers_begin, centers_end),
         (party_is_active, ":center_no"), #TLD
		 (party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
         #Reducing siege hardness every day by 20
         (party_get_slot, ":siege_hardness", ":center_no", slot_center_siege_hardness),
         (val_sub, ":siege_hardness", 20),
         (val_max, ":siege_hardness", 0),
         (party_set_slot, ":center_no", slot_center_siege_hardness, ":siege_hardness"),
       
         (party_get_slot, ":town_food_store", ":center_no", slot_party_food_store),
         (call_script, "script_center_get_food_store_limit", ":center_no"),
         (assign, ":food_store_limit", reg0),
         (try_begin),
           (party_get_slot, ":besieger_party", ":center_no", slot_center_is_besieged_by),
           (ge, ":besieger_party", 0), #town is under siege
       
           #Reduce prosperity of besieged center by -1 with a 33% chance every day.
           (try_begin),
             (store_random_in_range, ":random_no", 0, 3),
             (eq, ":random_no", 0),
             (call_script, "script_change_center_prosperity", ":center_no", -1),
           (try_end),

           (store_faction_of_party, ":center_faction", ":center_no"),
        # Lift siege unless there is an enemy party nearby
           (assign, ":siege_lifted", 0),
           (try_begin),
             (try_begin),
               (neg|party_is_active, ":besieger_party"),
               (assign, ":siege_lifted", 1),
             (else_try),
               (store_distance_to_party_from_party, ":besieger_distance", ":center_no", ":besieger_party"),
               (gt, ":besieger_distance", 5),
               (assign, ":siege_lifted", 1),
             (else_try), #MV: possibly redundant code
               (store_faction_of_party, ":besieger_faction", ":besieger_party"),
               (store_relation, ":reln", ":besieger_faction", ":center_faction"),
               (gt, ":reln", 0), #MV: if center changed hands
               (assign, ":siege_lifted", 1),
             (try_end),
             (eq, ":siege_lifted", 1),
             (try_for_range, ":enemy_hero", kingdom_heroes_begin, kingdom_heroes_end),
               (troop_slot_eq, ":enemy_hero", slot_troop_occupation, slto_kingdom_hero),
               (troop_get_slot, ":enemy_party", ":enemy_hero", slot_troop_leaded_party),
               (ge, ":enemy_party", 0),
               (party_is_active, ":enemy_party"),
               (store_faction_of_party, ":party_faction", ":enemy_party"),
               (store_relation, ":reln", ":party_faction", ":center_faction"),
               (lt, ":reln", 0),
               (store_distance_to_party_from_party, ":distance", ":center_no", ":enemy_party"),
               (lt, ":distance", 4),
               (assign, ":besieger_party", ":enemy_party"),
               (party_set_slot, ":center_no", slot_center_is_besieged_by, ":enemy_party"),
               (assign, ":siege_lifted", 0),
             (try_end),
           (try_end),
           (try_begin),
             (eq, ":siege_lifted", 1),
             (call_script, "script_lift_siege", ":center_no", 1),
           (else_try),
             (call_script, "script_center_get_food_consumption", ":center_no"),
             (assign, ":food_consumption", reg0),
             (val_sub, ":town_food_store", ":food_consumption"), # reduce food only under siege???
             (try_begin),
               (le, ":town_food_store", 0), #town is starving
               (store_random_in_range, ":r", 0, 100),
               (lt, ":r", 10), 
               (call_script, "script_party_wound_all_members", ":center_no"), # town falls with 10% chance if starving
             (try_end),
           (try_end),
         (else_try),
           #town is not under siege...
           (val_add, ":town_food_store", 30), #add 30 food (significant for castles only.
         (try_end),

         (val_min, ":town_food_store", ":food_store_limit"),
         (val_max, ":town_food_store", 0),
         (party_set_slot, ":center_no", slot_party_food_store, ":town_food_store"),
       (try_end),
]),

# script_lift_siege
# Input: arg1 = center_no, arg2 = display_message
# Output: none
#called from triggers
("lift_siege",
    [ (store_script_param, ":center_no", 1),
      (store_script_param, ":display_message", 2),
      (party_set_slot, ":center_no", slot_center_is_besieged_by, -1), #clear siege
      (call_script, "script_village_set_state",  ":center_no", 0), #clear siege flag
      (try_begin),
        (eq, ":center_no", "$g_player_besiege_town"),
        (assign, "$g_siege_method", 0), #remove siege progress
      (try_end),
      (try_begin),
        (eq, ":display_message", 1),
        (str_store_party_name_link, s3, ":center_no"),
        (try_begin),
          (store_faction_of_party, ":faction", ":center_no"),
          (store_relation, ":rel", "$players_kingdom", ":faction"),
          (gt, ":rel", 0),
          (assign, ":news_color", color_good_news),
        (else_try),
          (assign, ":news_color", color_bad_news),
        (try_end),
        (display_message, "@{s3} is no longer under siege.", ":news_color"),
      (try_end),
]),

# script_process_alarms
#called from triggers
("process_alarms",
    [(try_for_range, ":center_no", centers_begin, centers_end),
       (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
     (try_end),
     (assign, ":spotting_range", 2),
     (try_begin),
       (is_currently_night),
       (assign, ":spotting_range", 1),
     (try_end),
     (try_begin),
       (party_slot_eq, ":center_no", slot_center_has_watch_tower, 1),
       (val_mul, ":spotting_range", 2),
     (try_end),
     (try_for_parties, ":party_no"),
       (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
       (neg|party_is_in_any_town, ":party_no"),
       (store_faction_of_party, ":party_faction", ":party_no"),
       (try_for_range, ":center_no", centers_begin, centers_end),
         (party_is_active, ":center_no"), #TLD
 	     (party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
         (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
         (le, ":distance", ":spotting_range"),
         (store_faction_of_party, ":center_faction", ":center_no"),
         (store_relation, ":reln", ":center_faction", ":party_faction"),
         (lt, ":reln", 0),
         (party_set_slot, ":center_no", slot_center_last_spotted_enemy, ":party_no"), 
       (try_end),
     (try_end),
     (try_for_range, ":center_no", centers_begin, centers_end),
       (party_is_active, ":center_no"), #TLD
	   (party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
       (store_faction_of_party, ":center_faction", ":center_no"),
       (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
       (eq, ":center_faction", "$players_kingdom"),
       (party_get_slot, ":enemy_party", ":center_no", slot_center_last_spotted_enemy),
       (ge, ":enemy_party", 0),
       (store_distance_to_party_from_party, ":dist", "p_main_party", ":center_no"),
       (assign, ":has_messenger", 0),
       (try_begin),
         (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
         (eq, ":center_faction", "fac_player_supporters_faction"),
         (party_slot_eq, ":center_no", slot_center_has_messenger_post, 1),
         (assign, ":has_messenger", 1),
       (try_end),
       (this_or_next|lt, ":dist", 30),
       (eq, ":has_messenger", 1),
       (str_store_party_name_link, s1, ":center_no"),
       (display_message, "@Enemies spotted near {s1}."),
     (try_end),
]),

# script_get_center_faction_relation_including_player
# Input: arg1: center_no, arg2: target_faction_no
# Output: reg0: relation
#called from triggers
("get_center_faction_relation_including_player",
   [ (store_script_param, ":center_no", 1),
     (store_script_param, ":target_faction_no", 2),
     (store_faction_of_party, ":center_faction", ":center_no"),
     (store_relation, ":reln", ":center_faction", ":target_faction_no"),
     (try_begin),
       (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
       (store_relation, ":reln", "fac_player_supporters_faction", ":target_faction_no"),
     (try_end),
     (assign, reg0, ":reln"),
]),

# script_check_and_finish_active_army_quests_for_faction
# Input: faction_no
# Output: none
("check_and_finish_active_army_quests_for_faction",
   [ (store_script_param_1, ":faction_no"),
     (try_begin),
       (eq, "$players_kingdom", ":faction_no"),
       (try_begin),
         (check_quest_active, "qst_report_to_army"),
         (call_script, "script_cancel_quest", "qst_report_to_army"),
       (try_end),
       (assign, ":one_active", 0),
       (try_for_range, ":quest_no", army_quests_begin, army_quests_end),
         (check_quest_active, ":quest_no"),
         (call_script, "script_cancel_quest", ":quest_no"),
         (assign, ":one_active", 1),
       (try_end),
       (try_begin),
         (check_quest_active, "qst_follow_army"),
         (assign, ":one_active", 1),
         (call_script, "script_end_quest", "qst_follow_army"),
       (try_end),
       (eq, ":one_active", 1),
       (faction_get_slot, ":last_offensive_time", ":faction_no", slot_faction_ai_last_offensive_time),
       (store_current_hours, ":cur_hours"),
       (store_sub, ":total_time_served", ":cur_hours", ":last_offensive_time"),
       (store_mul, ":xp_reward", ":total_time_served", 5),
       (val_div, ":xp_reward", 50),
       (val_mul, ":xp_reward", 50),
       (val_add, ":xp_reward", 50),
       (add_xp_as_reward, ":xp_reward"),
     (try_end),
]),

# script_troop_get_player_relation
# Input: arg1 = troop_no
# Output: reg0 = effective relation (modified by troop reputation, honor, etc.)
#TLD: no reputation and honor
("troop_get_player_relation",
      [ (store_script_param_1, ":troop_no"),
        (troop_get_slot, ":effective_relation", ":troop_no", slot_troop_player_relation),
        (assign, reg0, ":effective_relation"),
]),

# script_change_player_relation_with_troop
# Input: arg1 = troop_no, arg2 = relation difference
("change_player_relation_with_troop",
    [ (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":difference"),
      (try_begin),
        (neq, ":troop_no", "trp_player"),
        (neg|is_between, ":troop_no", soldiers_begin, soldiers_end),
        (neq, ":difference", 0),
        (call_script, "script_troop_get_player_relation", ":troop_no"),
        (assign, ":old_effective_relation", reg0),
        (troop_get_slot, ":player_relation", ":troop_no", slot_troop_player_relation),
        (val_add, ":player_relation", ":difference"),
        (val_clamp, ":player_relation", -100, 101),
        (try_begin),
          (troop_set_slot, ":troop_no", slot_troop_player_relation, ":player_relation"),
          
          (str_store_troop_name_link, s1, ":troop_no"),
          (call_script, "script_troop_get_player_relation", ":troop_no"),
          (assign, ":new_effective_relation", reg0),
          (neq, ":old_effective_relation", ":new_effective_relation"),
          (assign, reg1, ":old_effective_relation"),
          (assign, reg2, ":new_effective_relation"),
          (try_begin),
            (gt, ":difference", 0),
            (display_message, "str_troop_relation_increased", color_good_news),
          (else_try),
            (lt, ":difference", 0),
            (display_message, "str_troop_relation_detoriated", color_bad_news),
          (try_end),
          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (assign, "$g_talk_troop_relation", ":new_effective_relation"),
            (call_script, "script_setup_talk_info"),
          (try_end),
          (call_script, "script_update_troop_notes", ":troop_no"),
        (try_end),
      (try_end),
]),

# script_change_player_relation_with_center
# Input: arg1 = party_no, arg2 = relation difference
("change_player_relation_with_center",
    [ (store_script_param_1, ":center_no"),
      (store_script_param_2, ":difference"),
      
      (party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (val_clamp, ":player_relation", -100, 100),
      (assign, reg2, ":player_relation"),
      (party_set_slot, ":center_no", slot_center_player_relation, ":player_relation"),
      
      (str_store_party_name_link, s1, ":center_no"),
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "@Your relation with {s1} has improved.", color_good_news),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "@Your relation with {s1} has deteriorated."),
      (try_end),
      
      (try_begin),
        (is_between, "$g_talk_troop", mayors_begin, mayors_end),
        (assign, "$g_talk_troop_relation", ":player_relation"),
        (call_script, "script_setup_talk_info"),
      (try_end),
]),

# script_change_player_relation_with_faction
# Input: arg1 = faction_no, arg2 = relation difference
("change_player_relation_with_faction",
    [ (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":difference"),
      
      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (assign, reg2, ":player_relation"),
      (set_relation, ":faction_no", "fac_player_faction", ":player_relation"),
      (set_relation, ":faction_no", "fac_player_supporters_faction", ":player_relation"),
      
      (str_store_faction_name_link, s1, ":faction_no"),
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "str_faction_relation_increased", color_good_news),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "str_faction_relation_detoriated", color_bad_news),
      (try_end),
      (call_script, "script_update_all_notes"),
]),

# script_set_player_relation_with_faction
# Input: arg1 = faction_no, arg2 = relation
("set_player_relation_with_faction",
    [ (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":relation"),
      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (store_sub, ":reln_dif", ":relation", ":player_relation"),
      (call_script, "script_change_player_relation_with_faction", ":faction_no", ":reln_dif"),
]),

# script_cf_get_random_active_faction_except_player_faction_and_faction
# Input: arg1 = except_faction_no
# Output: reg0 = random_faction
("cf_get_random_active_faction_except_player_faction_and_faction",
    [ (store_script_param_1, ":except_faction_no"),
      (assign, ":num_factions", 0),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (neq, ":faction_no", ":except_faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_add, ":num_factions", 1),
      (try_end),
      (gt, ":num_factions", 0),
      (assign, ":selected_faction", -1),
      (store_random_in_range, ":random_faction", 0, ":num_factions"),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (ge, ":random_faction", 0),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (neq, ":faction_no", ":except_faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_sub, ":random_faction", 1),
        (lt, ":random_faction", 0),
        (assign, ":selected_faction", ":faction_no"),
      (try_end),
      (assign, reg0, ":selected_faction"),
]),

# script_change_player_party_morale
# Input: arg1 = morale difference
# Output: none
("change_player_party_morale",
    [ (store_script_param_1, ":morale_dif"),
      (party_get_morale, ":cur_morale", "p_main_party"),
      (store_add, ":new_morale", ":cur_morale", ":morale_dif"),
      (val_clamp, ":new_morale", 0, 100),
      (party_set_morale, "p_main_party", ":new_morale"),
      (try_begin),
        (lt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":cur_morale", ":new_morale"),
        (display_message, "str_party_lost_morale", color_bad_news),
      (else_try),
        (gt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":new_morale", ":cur_morale"),
        (display_message, "str_party_gained_morale", color_good_news),
      (try_end),
]),

# script_cf_player_has_item_without_modifier
# Input: arg1 = item_id, arg2 = modifier
# Output: none (can_fail)
("cf_player_has_item_without_modifier",
    [ (store_script_param, ":item_id", 1),
      (store_script_param, ":modifier", 2),
      (player_has_item, ":item_id"),
      #checking if any of the meat is not rotten
      (assign, ":has_without_modifier", 0),
      (troop_get_inventory_capacity, ":inv_size", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":cur_item", "trp_player", ":i_slot"),
        (eq, ":cur_item", ":item_id"),
        (troop_get_inventory_slot_modifier, ":cur_modifier", "trp_player", ":i_slot"),
        (neq, ":cur_modifier", ":modifier"),
        (assign, ":has_without_modifier", 1),
        (assign, ":inv_size", 0), #break
      (try_end),
      (eq, ":has_without_modifier", 1),
]),

# script_get_player_party_morale_values
# Output: reg0 = player_party_morale_target
("get_player_party_morale_values",
    [ (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (assign, ":num_men", 0),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (val_add, ":num_men", 3),
        (else_try),
          (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
          (val_add, ":num_men", ":stack_size"),
        (try_end),
      (try_end),
      (assign, "$g_player_party_morale_modifier_party_size", ":num_men"),
    
      (store_skill_level, ":player_leadership", "skl_leadership", "trp_player"),
      (store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", 7),
      (assign, ":new_morale", "$g_player_party_morale_modifier_leadership"),
      (val_sub, ":new_morale", "$g_player_party_morale_modifier_party_size"),
      (val_add, ":new_morale", 50),

      (assign, "$g_player_party_morale_modifier_food", 0),
      (try_for_range, ":cur_edible", food_begin, food_end),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_edible", imod_rotten),
        (item_get_slot, ":food_bonus", ":cur_edible", slot_item_food_bonus),
        (val_add, "$g_player_party_morale_modifier_food", ":food_bonus"),
      (try_end),
      (val_add, ":new_morale", "$g_player_party_morale_modifier_food"),

      (try_begin),
        (eq, "$g_player_party_morale_modifier_food", 0),
        (assign, "$g_player_party_morale_modifier_no_food", 30),
        (val_sub, ":new_morale", "$g_player_party_morale_modifier_no_food"),
      (else_try),
        (assign, "$g_player_party_morale_modifier_no_food", 0),
      (try_end),
      
      # TLD morale-boosting items (non-cumulative)
      (try_begin),
	    (call_script, "script_get_troop_item_amount", "trp_player", "itm_lembas"),
	    (gt, reg0, 0),
        (val_add, ":new_morale", 30),
      (else_try),
	    (call_script, "script_get_troop_item_amount", "trp_player", "itm_cooking_cauldron"),
	    (gt, reg0, 0),
        (val_add, ":new_morale", 20),
      (try_end),

	  # TLD: nothing for this
      #(assign, "$g_player_party_morale_modifier_debt", 0),
      #(try_begin),
      #  (gt, "$g_player_debt_to_party_members", 0),
      #  (call_script, "script_calculate_player_faction_wage"),
      #  (assign, ":total_wages", reg0),
      #  (store_mul, "$g_player_party_morale_modifier_debt", "$g_player_debt_to_party_members", 10),
      #  (val_div, "$g_player_party_morale_modifier_debt", ":total_wages"),
      #  (val_clamp, "$g_player_party_morale_modifier_debt", 1, 31),
      #  (val_sub, ":new_morale", "$g_player_party_morale_modifier_debt"),
      #(try_end),

      (val_clamp, ":new_morale", 0, 100),
      (assign, reg0, ":new_morale"),
]),

# script_add_notification_menu
# Input: arg1 = menu_no, arg2 = menu_var_1, arg3 = menu_var_2
# Output: none
("add_notification_menu",
    [ (store_script_param, ":menu_no", 1),
      (store_script_param, ":menu_var_1", 2),
      (store_script_param, ":menu_var_2", 3),
      (assign, ":end_cond", 1),
      (try_for_range, ":cur_slot", 0, ":end_cond"),
        (try_begin),
          (troop_slot_ge, "trp_notification_menu_types", ":cur_slot", 1),
          (val_add, ":end_cond", 1),
        (else_try),
          (troop_set_slot, "trp_notification_menu_types", ":cur_slot", ":menu_no"),
          (troop_set_slot, "trp_notification_menu_var1", ":cur_slot", ":menu_var_1"),
          (troop_set_slot, "trp_notification_menu_var2", ":cur_slot", ":menu_var_2"),
        (try_end),
      (try_end),
]),

# script_finish_quest
# Input: arg1 = quest_no, arg2 = finish_percentage
# Output: none
("finish_quest",
    [ (store_script_param_1, ":quest_no"),
      (store_script_param_2, ":finish_percentage"),
      
      (quest_get_slot, ":quest_giver", ":quest_no", slot_quest_giver_troop),
      (store_troop_faction, ":quest_faction", ":quest_giver"),
      (quest_get_slot, ":quest_giver_center", ":quest_no", slot_quest_giver_center),
      (quest_get_slot, ":quest_importance", ":quest_no", slot_quest_importance),
      (quest_get_slot, ":quest_xp_reward", ":quest_no", slot_quest_xp_reward),
      (quest_get_slot, ":quest_gold_reward", ":quest_no", slot_quest_gold_reward),
      (quest_get_slot, ":quest_rank_reward", ":quest_no", slot_quest_rank_reward),
      
      #Exceptions
      (try_begin),
        (eq, ":quest_no", "qst_deliver_message"),
        (assign, ":quest_gold_reward", 0), #already paid in target currency
      (try_end),
      
      (try_begin),
        (lt, ":finish_percentage", 100),
        (val_mul, ":quest_xp_reward", ":finish_percentage"),
        (val_div, ":quest_xp_reward", 100),
        (val_mul, ":quest_gold_reward", ":finish_percentage"),
        (val_div, ":quest_gold_reward", 100),
        (val_mul, ":quest_rank_reward", ":finish_percentage"),
        (val_div, ":quest_rank_reward", 100),
        #Changing the relation factor. Negative relation if less than 75% of the quest is finished.
        #Positive relation if more than 75% of the quest is finished.
        (assign, ":importance_multiplier", ":finish_percentage"),
        (val_sub, ":importance_multiplier", 75),
        (val_mul, ":quest_importance", ":importance_multiplier"),
        (val_div, ":quest_importance", 100),
      (else_try),
        (val_div, ":quest_importance", 4),
        (val_add, ":quest_importance", 1),
      (try_end),
      
      (try_begin),
        (is_between, ":quest_giver", mayors_begin, mayors_end),
        (call_script, "script_change_player_relation_with_center", ":quest_giver_center", ":quest_importance"),
      (else_try),
        (call_script, "script_change_player_relation_with_troop", ":quest_giver", ":quest_importance"),
      (try_end),
      
      (add_xp_as_reward, ":quest_xp_reward"),
      (call_script, "script_add_faction_rps", ":quest_faction", ":quest_gold_reward"),
      (call_script, "script_increase_rank", ":quest_faction", ":quest_rank_reward"),
      (call_script, "script_end_quest", ":quest_no"),
]),

# script_get_information_about_troops_position
# Input: arg1 = troop_no, arg2 = time (0 if present tense, 1 if past tense)
# Output: s1 = String, reg0 = knows-or-not
("get_information_about_troops_position",
    [ (store_script_param_1, ":troop_no"),
      (store_script_param_2, reg3),
      (troop_get_type, reg4, ":troop_no"),
      (try_begin),
        (gt, reg4, 1), #MV: non-humans are male
        (assign, reg4, 0),
      (try_end),
      (str_store_troop_name, s2, ":troop_no"),
      
      (assign, ":found", 0),
      (troop_get_slot, ":center_no", ":troop_no", slot_troop_cur_center),
      (try_begin),
        (gt, ":center_no", 0),
        (is_between, ":center_no", centers_begin, centers_end),
        (str_store_party_name_link, s3, ":center_no"),
        (str_store_string, s1, "@{s2} {reg3?was:is currently} at {s3}."),
        (assign, ":found", 1),
      (else_try),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (gt, ":party_no", 0),
        (call_script, "script_get_troop_attached_party", ":troop_no"),
        (assign, ":center_no", reg0),
        (try_begin),
          (is_between, ":center_no", centers_begin, centers_end),
          (str_store_party_name_link, s3, ":center_no"),
          (str_store_string, s1, "@{s2} {reg3?was:is currently} at {s3}."),
          (assign, ":found", 1),
        (else_try),
          (get_party_ai_behavior, ":ai_behavior", ":party_no"),
          (eq, ":ai_behavior", ai_bhvr_travel_to_party),
          (get_party_ai_object, ":ai_object", ":party_no"),
          (is_between, ":ai_object", centers_begin, centers_end),
          (call_script, "script_get_closest_center", ":party_no"),
          (str_store_party_name_link, s4, reg0),
          (str_store_party_name_link, s3, ":ai_object"),
          (str_store_string, s1, "@{s2} {reg3?was:is} travelling to {s3} and {reg4?she:he} {reg3?was:should be} close to {s4}{reg3?: at the moment}."),
          (assign, ":found", 1),
        (else_try),
          (call_script, "script_get_closest_center", ":party_no"),
          (str_store_party_name_link, s3, reg0),
          (str_store_string, s1, "@{s2} {reg3?was:is} in wilderness and {reg4?she:he} {reg3?was:should be} close to {s3}{reg3?: at the moment}."),
          (assign, ":found", 1),
        (try_end),
      (else_try),
        #(troop_slot_ge, ":troop_no", slot_troop_is_prisoner, 1),
        (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_is_active, ":center_no"), #TLD
		  (party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
          (party_count_prisoners_of_type, ":num_prisoners", ":center_no", ":troop_no"),
          (gt, ":num_prisoners", 0),
          (assign, ":found", 1),
          (str_store_party_name_link, s3, ":center_no"),
          (str_store_string, s1, "@{s2} {reg3?was:is} being held captive at {s3}."),
        (try_end),
        (try_begin),
          (eq, ":found", 0),
          (str_store_string, s1, "@{s2} {reg3?was:has been} taken captive by {reg4?her:his} enemies."),
          (assign, ":found", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":found", 0),
        (str_store_string, s1, "@{reg3?{s2}'s location was unknown:I don't know where {s2} is}."),
      (try_end),
      (assign, reg0, ":found"),
]),

# script_recruit_troop_as_companion
# Input: arg1 = troop_no,
# Output: none
("recruit_troop_as_companion",
    [ (store_script_param_1, ":troop_no"),
      (troop_set_slot, ":troop_no", slot_troop_occupation, slto_player_companion),
      #(troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
      (troop_set_auto_equip, ":troop_no",0),
      (party_add_members, "p_main_party", ":troop_no", 1),
      (str_store_troop_name, s6, ":troop_no"),
      (display_message, "@{s6} has joined your party"),
]),

#  "script_str_store_race_adj" (stringNo, raceNo)  (mtarini)
("str_store_race_adj", [
	(store_script_param_1, ":stN"),
	(store_script_param_2, ":race"),

	(str_clear, ":stN"),
	(try_begin),
		(is_between,":race",tf_elf_begin,tf_elf_end),
		(str_store_string, ":stN", "@elven"), 
	(else_try),
		(eq,":race",tf_dwarf),
		(str_store_string, ":stN", "@dwarven"),
	(else_try),
		(eq,":race",tf_orc),
		(str_store_string, ":stN", "@orc"), # also an adjective
	(else_try),
		(eq,":race",tf_uruk),
		(str_store_string, ":stN", "@uruk"), # also an adjective
	(else_try),
		(eq,":race",tf_urukhai),
		(str_store_string, ":stN", "@uruk-hai"), # also an adjective
	(else_try),
		(eq,":race",tf_troll),
		(str_store_string, ":stN", "@trollish"), 
	(else_try),
		(eq,":race",tf_dwarf),
		(str_store_string, ":stN", "@dwarven"),
	(else_try),
		(str_store_string, ":stN", "@man"), # also and adjective
	(try_end),
]),

#  "script_str_store_party_movement_verb" (stringNo, PartyNo)  (mtarini)
# stores "charging, riding, marching" etc
("str_store_party_movement_verb", [
	(store_script_param_1, ":stN"),
	(store_script_param_2, ":party"),

	(str_clear, ":stN"),
	(try_begin),
		(call_script, "script_cf_party_is_mostly_mounted", ":party"),
		(str_store_string, ":stN", "@riding"), 
	(else_try),
		(store_faction_of_party, ":fac", ":party"),
		(try_begin),
			(is_between,":fac",kingdoms_begin,kingdoms_end),
			(str_store_string, ":stN", "@marching"), 
		(else_try),
			(str_store_string, ":stN", "@charging"), # for bandits, desertes, civilians, etc.
		(try_end),
	(try_end),
]),

# script_str_store_distrusting_friend_dialog_in_s14_to_18
# used to set dialog when party A (player) meets friendlty party B, but it is not trusted by them
# parameters: three factions (see below)
# output: 4 lines of dialogs
# s14 party B: first line,
# s15 party A: response 1:  (used to quit dialog) 
# s16 party B: answer  1
# s17 party A: response 2: (used to get an answer)
# s18 party B: answer  2
( "str_store_distrusting_friend_dialog_in_s14_to_18", [
	(store_script_param_1, ":facA"), # of party A (usually, player)
	(store_script_param_2, ":facB"), # of party B (other party)
	(store_script_param, ":facC", 3), # of the place of meeting, or -1 if no man land
	(str_store_faction_name, s20, ":facA"),
	(str_store_faction_name, s21, ":facB"),
	(faction_get_slot, ":sideA", ":facA", slot_faction_side),
	(faction_get_slot, ":sideB", ":facB", slot_faction_side),
	(store_add, ":tmp", "str_faction_side_name", ":sideA"),(str_store_string, s22, ":tmp"),
	(store_add, ":tmp", "str_faction_side_name", ":sideB"),(str_store_string, s23, ":tmp"),
	
	(try_begin),
		(eq, ":facA", ":facC"), # situation 1: partyB is traspassing!
		(try_begin), 
		    (eq, ":sideA", faction_side_good),
			(str_store_string, s14, "@We know this is your land, {playername}.^Trust us, we're here to fight our common Enemy."),
			(str_store_string, s15, "@I trust you. {s20} and {s21} should be friends and trust each other."),
			(str_store_string, s16, "@There is wisdom in your words, {playername}."),
			(str_store_string, s17, "@Why should I? Better leave the land of {s20}."),
			(str_store_string, s18, "@We will go in peace, as soon as we have completed our mission, of which, I'm afraid, we cannot tell you."),
		(else_try),
		    (eq, ":sideA", ":sideB"), # eye vs eye, or hand vs hand
			(str_store_string, s14, "@Is this your land, {playername}? This place stinks.^But stay calm, we are in {s20} only to follow orders by our common Master."),
			(str_store_string, s15, "@Yes, go on, do whatever {s22} says."),
			(str_store_string, s16, "@Of course."),
			(str_store_string, s17, "@I don't like this. What brings your lot here, all the way from {s21}?"),
			(str_store_string, s18, "@Do you fear us, {playername} from {s20}? Mmm, what are you hiding from {s22}?^^Leave us alone, and noone gets hurt."),
		(else_try),  # eye vs hand, or hand vs eye
			(str_store_string, s14, "@It's a servant of {s22}. Fear {s23}, {playername}!"),
			(str_store_string, s15, "@Our allies, are you? I guess you can pass. "),
			(str_store_string, s16, "@And we shall not kill you, for now."),
			(str_store_string, s17, "@This land belongs to {s20}... {s23} has no business here."),
			(str_store_string, s18, "@We will stay as long as  our master commands! Thank your fate that we didn't come for you."),
		(try_end),
	(else_try),
		(eq, ":facB", ":facC"), # situation 2: partyA is trespassing!
		(try_begin),
			(eq, ":sideB", faction_side_good), # good guys
			(str_store_string, s14, "@You wear the colors of {s20}. What is your business in {s21}?^Speak quickly!"),
			(str_store_string, s15, "@We are pursuing our enemies, who are also your enemies!"),
			(str_store_string, s16, "@Maybe. Or maybe you are spies.^Go back where you belong, soldier of {s20}."),
			(str_store_string, s17, "@We are friends of {s21}."),
			(str_store_string, s18, "@Time will tell if you speak the truth. It is difficult to tell friend from foe these days."),
		(else_try),
			# any bad guys
			(eq, ":sideA", ":sideB"), # eye vs eye, or hand vs hand
			(str_store_string, s14, "@What are you doing here in {s21}, {s20} scum? This is our place, not yours!"),
			(str_store_string, s15, "@You dare question direct orders from {s23}?"),
			(str_store_string, s16, "@Guess not. But I still don't like having you around.^I'll be watching you, {playername} of {s20}."),
			(str_store_string, s17, "@None of your business, pig!"),
			(str_store_string, s18, "@*growls*^You should be glad you fight for our Master, otherwise you would not get away with this trespassing."),
		(else_try),
			# any bad guys
			# eye vs hand, or hand vs eye
			(str_store_string, s14, "@What are you doing so far from home, slave of {s22}? Around here, {s23} is the Master!"),
			(str_store_string, s15, "@Quiet! I didn't came for you. This time."),
			(str_store_string, s16, "@And I've orders to let you pass. This time."),
			(str_store_string, s17, "@None of your business."),
			(str_store_string, s18, "@You slaves of {s22} are weak! You are fortunate that we consider you to be allies..."),
		(try_end),
	(else_try), # situation 3: common ground
		(try_begin),
			(eq, ":sideA", faction_side_good),
			(str_store_string, s14, "@Look whom we meet so far from home: soldiers of {s20}! Is this good news or bad?"),
			(str_store_string, s15, "@{s20} and {s21} fight for a common cause. We should cooperate in hostile lands."),
			(str_store_string, s16, "@In these dark times, it is everybody for themselves, {playername}.^But I wish you a safe journey home."),
			(str_store_string, s17, "@Neither good, nor bad.  Our business is our own."),
			(str_store_string, s18, "@Everybody on his way, then."),
		(else_try),
			# bad guys
			(str_store_string, s14, "@What are you trying to do, {s20} scum? Steal our spoils?"),
			(str_store_string, s15, "@Ha! Soon there will be spoils for everybody."),
			(str_store_string, s16, "@Yes. Unless you get killed first."),
			(str_store_string, s17, "@You don't get any spoils if YOU get killed, scum of {s21}."),
			(str_store_string, s18, "@Is that a threat? Be thankful that we have enemies around to slaughter before it is your turn."),
		(try_end),
	(try_end),
]),

#  "script_str_store_battle_cry" (stringNo, PartyNo)  (mtarini)
# used in prebattle dialog
("str_store_party_battle_cry_in_s4", [
	(store_script_param_1, ":partyA"),
	(store_script_param_2, ":defending"),
	
	(store_faction_of_party, ":factionA",":partyA"),
	# note: we get the *dominant* race of player party, so that he sees differnt things said to him according to who he is accompaning him
	# note: we get the *dominant* race of player party, so that he sees differnt things said to him according to who he is accompaning him
	(call_script, "script_party_get_dominant_faction", "p_main_party"),(assign,":factionB",reg0),
	#(store_faction_of_party, ":facB","p_main_party"),
	
	(troop_get_type, ":raceA" , "$g_talk_troop"),
	(call_script, "script_party_get_dominant_race", "p_main_party"),(assign,":raceB",reg0),
	#(troop_get_type, ":raceB" , "trp_player"),

	(faction_get_slot, ":sideA",":factionA", slot_faction_side),
	(faction_get_slot, ":sideB",":factionB", slot_faction_side),	

	(call_script, "script_get_region_of_party", "p_main_party"), (assign, ":region", reg1),
	(call_script, "script_region_get_faction", ":region", ":sideA" ), (assign, ":factionR", reg1), 
	
	# semplify all human races into "human"
	(try_begin),
		(neg|is_between, ":raceB", tf_orc_begin, tf_orc_end),
		(neg|is_between, ":raceB", tf_elf_begin, tf_elf_end),
		(neq, ":raceB", tf_dwarf),
		(neq, ":raceB", tf_troll),
		(assign, ":raceB", tf_male),
	(try_end),
	(try_begin),
		(neg|is_between, ":raceA", tf_orc_begin, tf_orc_end),
		(neg|is_between, ":raceA", tf_elf_begin, tf_elf_end),
		(neq, ":raceA", tf_dwarf),
		(assign, ":raceA", tf_male),
	(try_end),

	(str_clear, s14),(str_clear, s15),(str_clear, s16),(str_clear, s17),(str_clear, s18),(str_clear, s19),
	(str_store_faction_name, s16, ":factionA"),
	(call_script, "script_str_store_race_adj", s15, ":raceB"),
	(try_begin), (eq, ":raceB", tf_male), (str_store_string, s19, "@{s15} "), (try_end),
	(str_store_faction_name, s18, ":factionB"),

	# s14: possible incipit for when speaker is attacked
	(try_begin),
		(eq, ":defending", 1),
		(store_random_in_range, ":rand", 0,4), 
		(try_begin),(eq,":rand", 0),
			(str_store_string, s14, "@The enemy is upon us! ^"),
		(else_try),(eq,":rand", 1),
			(str_store_string, s14, "@They are upon us! ^"),
		(else_try),(eq,":rand", 3),
			(str_store_string, s14, "@{playername} and {his/her} rabble from {s18} is upon us! ^"),
		(try_end),
	(try_end),

	(store_add, reg2, str_shortname_region_begin , ":region"),
	(str_store_string,s17,reg2),

	(str_clear, s4),
	
	# for war cryes, you can use:
	# -- factionA,  sideA, raceA: faction, side, race of party WHICH IS TALKING
	# -- factionB,  sideB, raceB: faction, side, race of enemy of A (i.e. player)
	# -- region, factionR: the region where the battle takes pace, and the faction of that region
	# s14: "They are attacking", if A is being attacked, or nothing (empty string) 
	# s15: adjective for raceB
	# s16: faction name of A
	# s17: short region name
	# s18: faction name of B
	# s19: adjective for raceB, but nothing if human
	
	(assign,  ":done", 0), # first pass will fail
	(assign,  ":rand", -1), # first pass will fail
	(try_for_range, ":i", 0, 2000),
		(eq, ":done", 0), 
		
		(try_begin),(eq,":rand",first_count()),
			(eq, ":defending", 1),
			(neg|is_between, ":raceA", tf_orc_begin, tf_orc_end),
			(is_between, ":raceB", tf_orc_begin, tf_orc_end),
			(str_store_string, s4, "@ORCS! ORCS!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":defending", 1),
			(eq, ":sideB", faction_side_good),
			(neg|is_between, ":factionA", kingdoms_begin, kingdoms_end), # civilians
			(is_between, ":raceB", tf_orc_begin, tf_orc_end),
			(str_store_string, s4, "@ORCS! ORCS! Fight for your life!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":defending", 1),
			(is_between, ":raceA", tf_orc_begin, tf_orc_end),
			(is_between, ":raceB", tf_elf_begin, tf_elf_end),
			(str_store_string, s4, "@Elven ghosts!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":defending", 1),
			(eq, ":sideA", faction_side_good),
			(str_store_string, s4, "@Here they come! Hold ranks!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":defending", 1),
			(str_store_string, s4, "@We are under attack!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":defending", 1),
			(eq, ":factionB", fac_rohan),
			(str_store_string, s4, "@Horse people! The horse people are upon us!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":defending", 1),
			(eq, ":factionB", fac_gondor),
			(str_store_string, s4, "@Men from the White City? Let them come, to their death!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":raceA", tf_orc_begin, tf_orc_end),
			(eq, ":raceB", tf_male),
			(str_store_string, s4, "@Death to men!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":raceA", tf_orc_begin, tf_orc_end),
			(is_between, ":raceB", tf_orc_begin, tf_orc_end),
			(str_store_string, s4, "@Kill the maggots!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":sideA", faction_side_eye ),
			(eq, ":sideB", faction_side_hand ),
			(str_store_string, s4, "@Death to traitors of the Eye!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":sideA", faction_side_hand ),
			(eq, ":sideB", faction_side_eye ),
			(str_store_string, s4, "@Death to traitors of the White Hand!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":sideB", faction_side_good),
			(str_store_string, s4, "@{s14}Kill them all! Take no prisoners!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":raceA", tf_orc_begin, tf_orc_end),
			(str_store_string, s4, "@Tonight we feast on {s15} flesh!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":raceA", tf_orc_begin, tf_orc_end),
			(str_store_string, s4, "@Gharr! Kill! Kill! Kill!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":raceB", tf_dwarf),
			(str_store_string, s4, "@Slaughter these half men!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":raceB", tf_elf_begin, tf_elf_end),
			(str_store_string, s4, "@Fear no elven ghosts!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":raceA", tf_male),
			(eq, ":raceB", tf_male),
			(eq, ":sideB", faction_side_good),
			(str_store_string, s4, "@{s14}Double rations to the one bringing me the most heads!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":sideB", faction_side_good),
			(this_or_next|is_between, ":raceA", tf_orc_begin, tf_orc_end),
			(neq, ":raceB", tf_male),
			(str_store_string, s4, "@{s14}Double rations to the one bringing me the most {s15} heads!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_dunland),
			(eq, ":factionB", fac_rohan),
			(str_store_string, s4, "@{s14}Kill these horse thieves!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_dunland),
			(eq, ":factionB", fac_rohan),
			(str_store_string, s4, "@Kill them all! Take back what is ours!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":sideA", faction_side_good ),
			(str_store_string, s4, "@Tonight there will be one less enemy of {s16}!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_dwarf),
			(str_store_string, s4,"@Baruk Khazâd! Khazâd ai-mênu!"),
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_rohan ),
			(str_store_string, s4,"@{s14}Riders of Rohan! Remember what do you fight for!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_mordor),
			(str_store_string, s4,"@{s14}More {s19}heads to decorate the gates of Morannon!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_isengard),
			(str_store_string, s4,"@The Wise Master shall be pleased when I show him the body of {playername}!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":raceA", tf_elf_begin, tf_elf_end),
			(is_between, ":raceB", tf_orc_begin, tf_orc_end),
			(str_store_string, s4,"@{s14}Now we will put an end to the suffering of these foul things."), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_imladris),
			(str_store_string, s4,"@{s14}Today we shall battle the enemies of Imladris and all that is fair."), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":raceA", tf_elf_begin, tf_elf_end),
			(is_between, ":region", region_n_mirkwood, region_s_mirkwood+1),
			(str_store_string, s4,"@All who enter Mirkwood with malice shall never leave!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":raceA", tf_male),
			(eq, ":sideA", faction_side_good),
			(eq, ":defending", 1),
			(str_store_string, s4,"@Men of {s16}, the enemy is here! Fight for your land!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":raceA", tf_male),
			(eq, ":sideA", faction_side_good),
			(eq, ":defending", 0),
			(str_store_string, s4,"@Men of {s16}, charge! Fight for your land!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_harad),
			(str_store_string, s4,"@{s14}Grind their bodies into the sand!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_rhun),
			(eq, ":raceB", tf_dwarf),
			(str_store_string, s4,"@{s14}Dwarves or men, they are no match for our fierceness!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_rhun),
			(is_between, ":raceB", tf_elf_begin, tf_elf_end),
			(str_store_string, s4,"@{s14}Elves or men, they are no match for our fierceness!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":factionA", fac_rhun, fac_khand+1),
			(str_store_string, s4,"@{s14}Flesh to shatter, throats to cut, blood to spill!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_khand),
			(str_store_string, s4,"@Put on the masks of warriors, men! Today the doom falls upon our enemies from {s18}!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_umbar),
			(eq, ":defending", 1),
			(str_store_string, s4,"@They seek the tempest, and they shall have it! Men, prepare to fight!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_umbar),
			(eq, ":defending", 0),
			(str_store_string, s4,"@Draw your weapons, men, for tempest is unleashed upon our enemies!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":raceA", tf_orc_begin, tf_orc_end),
			(is_between, ":factionA", kingdoms_begin, kingdoms_end),
			(str_store_string, s4,"@Orcs of {s16}, get ready! Here are a few throats for you to cut!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_guldur),
			(neg|is_between, ":raceB", tf_elf_begin, tf_elf_end),
			(str_store_string, s4,"@These friend of elves will fall under our blades!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":raceB", tf_elf_begin, tf_elf_end),
			(str_store_string, s4,"@These Elves will fall under our blades!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":raceA", tf_orc_begin, tf_orc_end),
			(is_between, ":factionA", kingdoms_begin, kingdoms_end),
			(str_store_string, s4,"@Raahh! Draw your weapons, scum of {s16}! Tonight we feast on {s15} entrails!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(is_between, ":raceA", tf_orc_begin, tf_orc_end),
			(str_store_string, s4,"@Rha! {s14}More {s15} bodies to disfigure with our twisted weapons!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionB", fac_dunland),
			(str_store_string, s4,"@Slaughter these puny thieves of {s18} now! Then we burn their homes and cut down their families."), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", ":factionR"),
			(eq, ":defending", 0),
			(neq, ":factionA", fac_umbar),
			(str_store_string, s4,"@Death to the trespassers of the lands of {s16}!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":sideA", faction_side_good),
			(eq, ":factionA", ":factionR"),
			(eq, ":defending", 0),
			(str_store_string, s4,"@CHARGE! Let's clear the {s18} {s19}scum from {s17}!"), 
			(assign, ":done", 1),
		(else_try),(eq,":rand",next_count()),
			(eq, ":factionA", fac_beorn),
			(str_store_string, s4,"@{s14}Now that {s19}scum will taste the fury of the bear people!"), 
			(assign, ":done", 1),
		(try_end),
		
		# end of pass: roll a number beween 0 and N_POSSIBILITIES - 1  for next pass
		(store_random_in_range, ":rand", 0, next_count() ), 
		# fix for uneven randomization...
		(val_add, ":rand", ":i"), (val_mod, ":rand", curr_count() ),
	
	(try_end),
	
	(assign, reg55, curr_count() ),
	(assign, reg40, ":defending"),
	(assign, reg41,":factionA"),
	(assign, reg42,":factionB"),
	(assign, reg43,":factionR"),
	(assign, reg44,":sideA"),
	(assign, reg45,":sideB"),
	(assign, reg46,":raceA"),
	(assign, reg47,":raceB"),
	(assign, reg48,":region"),
#	(display_message, "@DEBUG: def:{reg40} Fac:({reg41},{reg42},{reg43}). Sid:({reg44},{reg45}). Rac:({reg46},{reg47}). Region:{reg48}"),
  # default battle cries, if no good one found
	(try_begin),(eq, ":done", 0),
		(try_begin),
			(encountered_party_is_attacker),
			(str_store_string, s4, "@Attack!"),
		(else_try),
			(str_store_string, s4, "@We are under attack!"),
		(try_end),
	(try_end),
]),

# regions... put results in reg1 (mtarini)
("get_region_of_party", [
	(store_script_param_1, ":party"),
	(party_get_current_terrain, ":t",":party"),
    (party_get_position, pos1, "p_main_party"),
	(call_script,"script_get_region_of_pos1", ":t"),
]),

# regions... of a pos: put results in reg1 (mtarini)
# first parameter: terrain type
("get_region_of_pos1", [
	(store_script_param_1, ":terrain_type"),
	
	(position_get_x,":x",pos1),(position_get_y,":y",pos1),
	
	#(store_add,":sum", ":x",":y"),
	(store_sub,":diff", ":x",":y"),
	 
	(set_fixed_point_multiplier,100.0),
	#(assign, reg5,":x"),(assign, reg6,":y"),(convert_to_fixed_point,reg5),(convert_to_fixed_point,reg6),(display_message,"@you are in ({reg5},{reg6})..."),
	 
	(assign, reg1, -1),
	 
	(try_begin),
		#  mordor?
		(is_between, ":x", -20800, -7784 ),(is_between, ":y", -3190, 8500), 
		(assign, reg1, region_mordor),
	(else_try),		
		# dead marshes?
		(ge, ":x", -6800), (ge, ":y", -4900),  (store_add,":h",":y",":x"), (lt, ":h", -8000),
		(eq, ":terrain_type", rt_swamp),
		(assign, reg1, region_dead_marshes),
	(else_try),
		# ithilien? (north or south)
		(is_between, ":x", -7084, -5890 ),(is_between, ":y", -2243, 6500), 
		(try_begin),(ge,":y",5546),
		 	(assign, reg1, region_s_ithilien),
		(else_try),(ge,":y",1143),
		 	(assign, reg1, region_c_ithilien),
		(else_try),
		 	(assign, reg1, region_n_ithilien),
		(try_end),
	(else_try),
		# s _ ithilien?  (second chance)
		(is_between, ":x", -8000, -3400 ),(is_between, ":y", 6000,8500), (lt, ":diff", -1065),
		(assign, reg1, region_s_ithilien),
	(else_try),
		# c_ ithilien?  (second chance)
		(is_between, ":x", -7800, -4700 ),(is_between, ":y", -3500,6500), 
		(position_set_x,pos20,-3215),(position_set_y,pos20,4185),(position_set_z,pos20,0.0),(get_distance_between_positions,":dist",pos1,pos20), (lt,":dist",850),
		(assign, reg1, region_c_ithilien),
	(else_try),
		# entwash? (delta entwash or wetwand)
		(position_set_x,pos20,-3710),(position_set_y,pos20,-1570),(position_set_z,pos20,0.0),
		(get_distance_between_positions,":dist",pos1,pos20), (lt,":dist",1900),
		(try_begin),(ge,":x",-3779),
			(assign, reg1, region_entwash),
		(else_try),		
			(assign, reg1, region_wetwang),
		(try_end),
	(else_try),
		# lorien forest?
		(is_between, ":x", -1200, 2910),(is_between, ":y", -14100, -12143), 
		(is_between, ":terrain_type", rt_forest_begin,rt_forest_end),
		(assign, reg1, region_lorien),
	(else_try),
		#plennor fields?
		(position_set_x,pos20,-5306),(position_set_y,pos20,+2132),(position_set_z,pos20,0),
		(get_distance_between_positions,":dist",pos1,pos20), (lt,":dist",700),
		(assign, reg1, region_pelennor), 
	(else_try),		
		# determine on which side of the white mountains...
		(store_mul,":k",":x",374.4),(store_mul,":k2",":y",1000), (val_add,":k",":k2"), 
		(ge,":k",725184),
	    # SOUTH of white mountains... pick region by GONDOR subfaction town proximity of gondor
		(assign, reg1, region_lebennin),
		(assign, ":min_dist", 1000000),
		(try_for_range, ":i", "p_town_pelargir" , "p_town_edoras" ), # scan all gondor fiefdom cityes
			(party_get_slot, ":fief", ":i", slot_party_subfaction),
			(gt, ":fief", 0),
			(party_get_position,pos20,":i"),
			(get_distance_between_positions, ":dist", pos20, pos1),
			(try_begin), 
				(le, ":dist", ":min_dist"),
				(store_add, reg1, region_pelennor, ":fief"),
				(assign, ":min_dist", ":dist"),
			(try_end),
		(try_end),
	(else_try),
	    # NORTH of white mountains...
		# ####
		# drudan forsest?
		(is_between, ":x", -4636, -3400),(is_between, ":y",   +941,    1997),
		(is_between, ":terrain_type", rt_forest_begin,rt_forest_end),
		(assign, reg1, region_druadan_forest),
	(else_try),
		# firien_wood?
		(is_between, ":x",  -3345, -1792),(is_between, ":y",   +80,    1449),
		(is_between, ":terrain_type", rt_forest_begin,rt_forest_end),
		(assign, reg1, region_firien_wood),
	(else_try),
		# helm's deep?
		(party_get_position,pos20,"p_town_hornburg"),
		(get_distance_between_positions, ":dist", pos20, pos1),
		(le, ":dist", 420),
		(assign, reg1, region_hornburg),
	(else_try),
		# harrowdale? (valley where edoras is)
		(is_between, ":x", 1958, 2515),(is_between, ":y",   -1778, -501),
		(assign, reg1, region_harrowdale),
	(else_try),
		# anorien? between entwash and white mountains
		(position_set_x,pos20,-4264),(position_set_y,pos20,+1520),(position_set_z,pos20,0),
		(get_distance_between_positions, ":dist", pos20, pos1),
		(le, ":dist", 1956),
		(assign, reg1, region_anorien),
	(else_try),
		# around isengard?
		(is_between, ":x", 4498, 5867),(is_between, ":y",   -6480,    -4680),
		(assign, reg1, region_isengard),
	(else_try),
		# gap of rohan?
		(is_between, ":x", 4856, 6269),(is_between, ":y",   -4215,-2812),
		(assign, reg1, region_gap_of_rohan),
	(else_try),
		# fangorn?
		(position_set_x,pos20,5105),(position_set_y,pos20,-8512),(position_set_z,pos20,0),
		(get_distance_between_positions, ":dist", pos20, pos1),
		(le, ":dist", 3050),
		(is_between, ":terrain_type", rt_forest_begin,rt_forest_end),
		(assign, reg1, region_fangorn),
	(else_try),
		# the region_emyn_muil?
		(position_set_x,pos20,-4593),(position_set_y,pos20,-4645),(position_set_z,pos20,0),
		(get_distance_between_positions, ":dist", pos20, pos1),
		(le, ":dist", 4593-3341),
		(assign, reg1, region_emyn_muil),
	(else_try),
		# the dagorlad?
		(is_between, ":x",-9371, -3474),(is_between, ":y",-6081 , -2932),
		(assign, reg1, region_dagorlad),
	(else_try),
		# the s updeep?
		(is_between, ":x",-4960, -3400),(is_between, ":y",-9335 , -5270),
		(assign, reg1, region_s_undeep),
	(else_try),
		# the n updeep?
		(is_between, ":x",-5000, -3400),(is_between, ":y",-10998 , -9022),
		(assign, reg1, region_n_undeep),
	(else_try),
		# the wold?
		(is_between, ":x", -4190,2307 ),(is_between, ":y",   -9615,  -6514),
		(assign, reg1, region_the_wold),
	(else_try),
		# the brwon_lands?
		(is_between, ":x", -8005,-3026 ),(is_between, ":y",   -10668,  -5261),
		(assign, reg1, region_brown_lands),
	(else_try),
		# evertything else, in a BIG region, is in rohan... 
		(is_between, ":x", -3557,5893 ),(is_between, ":y",   -4782,  1057),
		# pick emnet
		(assign, reg1, region_east_emnet),
		(assign, ":min_dist", 1000000),

		(try_for_range, ":i", "p_town_east_emnet" , "p_town_morannon" ), # scan all rohan "emnet/fold" cityes
			(party_get_slot, ":fief", ":i", slot_party_subfaction),
			(gt, ":fief", 0),
			(party_get_position,pos20,":i"),
			(get_distance_between_positions, ":dist", pos20, pos1),
			(try_begin), 
				(le, ":dist", ":min_dist"),
				(store_add, reg1, region_harrowdale, ":fief"),
				(assign, ":min_dist", ":dist"),
			(try_end),
		(try_end),
	(else_try),
		# n.mirkwood?
		(is_between, ":x",  -8041, -28),(is_between, ":y",   -29935,  -19881),
		(is_between, ":terrain_type", rt_forest_begin,rt_forest_end),
		(assign, reg1, region_n_mirkwood),
	(else_try),
		# s.mirkwood?
		(is_between, ":x",  -9828,-1943),(is_between, ":y",  -19881,  -11829),
		(is_between, ":terrain_type", rt_forest_begin,rt_forest_end),
		(assign, reg1, region_s_mirkwood),
	(else_try),
		# s.mirkwood?, road is still mirkwood
		(is_between, ":x",  -7500,-2000),(is_between, ":y",  -18581,  -19929),
		(assign, reg1, region_s_mirkwood),
	(else_try),
		# s.mirkwood?, dol gundur is still mirkwood
		(is_between, ":x", -4595,  -3750),(is_between, ":y",  -13519,  -12885),
		(assign, reg1, region_s_mirkwood),
	(else_try),
		# near misty mountains...
		(is_between, ":x", 4100, 6000),(is_between, ":y",  -10902, -18090),
		(assign, reg1, region_misty_mountains),
	(else_try),
		# near misty mountains., 2nd chance..
		(is_between, ":x", 1846,6000),(is_between, ":y",  -23809,-17336),
		(assign, reg1, region_misty_mountains),
	(else_try),
		# near grey mountains, far in the north
		(lt,  ":y",  -23220),
		(assign, reg1, region_grey_mountains),
	(else_try),
		# else, "vague locations": 
		(is_between, ":x", -3500,3500),(gt, ":y", -13400),
		(assign, reg1, region_anduin_banks),
	(else_try),
		(is_between, ":x", -3900,1800),
		(assign, reg1, region_anduin_banks),
	(else_try),	
		(lt, ":x", 0),(lt,  ":y",  -23662),
		(assign, reg1, region_above_mirkwook),
	(try_end),
]),
  
("tld_party_relocate_near_party", [
    (store_script_param_1, ":pa"),
    (store_script_param_2, ":pb"),
    (store_script_param, ":dist",3),
	(call_script, "script_party_which_side_of_white_mountains", ":pb"), (assign, ":pb_is_south", reg0),
	(try_for_range, ":i", 0, 40), # try 40 times
		(party_relocate_near_party, ":pa", ":pb",":dist"),
		(assign, ":pa_is_south", 0),
		(call_script, "script_party_which_side_of_white_mountains", ":pa"), (assign, ":pa_is_south", reg0), 
		(eq,":pa_is_south",":pb_is_south"),
		(assign, ":i", 20), # break
		(try_begin), 
			(ge,":i",39), 
			(display_message, "@TLD ERROR! could not spawn the party on the same side of the white mountains"),
		(try_end),
	(try_end),
]),

#  script_region_get_faction: (mtarini)
# given a region, it return (in reg1) the "default faction" ruling in that region, if any (else, -1)   (matrini)
# parameter 2: BIAS: use thinking of this side (good, eye, hand), or -1 if no bias
("region_get_faction", [
	(store_script_param_1, ":region_id"),
	(store_script_param_2, ":bias"),
	
	(try_begin), (eq,":region_id", region_gap_of_rohan), (ge, ":bias", faction_side_eye),
		(assign, reg1, fac_dunland),
	(else_try),(is_between,":region_id", region_n_ithilien, region_c_ithilien+1), (ge, ":bias", faction_side_eye),
		(assign, reg1, fac_mordor),
	(else_try), (eq,":region_id", region_s_ithilien), (ge, ":bias", faction_side_eye),
		(assign, reg1, fac_harad),
	(else_try), (eq,":region_id", region_befalas), (ge, ":bias", faction_side_eye),
		(assign, reg1, fac_umbar),
	(else_try), (is_between,":region_id", region_pelennor, region_harrowdale), 
		(assign, reg1, fac_gondor),
	(else_try), (is_between, ":region_id", 	region_harrowdale, region_entwash),
		(assign, reg1, fac_rohan),
	(else_try), (eq, ":region_id", 	region_isengard),
		(assign, reg1, fac_isengard),
	(else_try), (eq, ":region_id", 	region_lorien),
		(assign, reg1, fac_lorien),
	(else_try), (eq, ":region_id", 	region_n_mirkwood),
		(assign, reg1, fac_woodelf),
	(else_try), (eq, ":region_id", 	region_brown_lands ),
		(assign, reg1, fac_khand),
	(else_try), (eq, ":region_id", 	region_s_mirkwood),
		(assign, reg1, fac_guldur),
	(else_try), 
		(this_or_next|eq, ":region_id", region_mordor ), 
		(this_or_next|eq, ":region_id", region_dagorlad ), 
		(eq, ":region_id", region_emyn_muil ), 
		(assign, reg1, fac_mordor),
	(else_try),
		(assign, reg1, -1),  # no man land
	(try_end)
]),

 
# script_jump_to_random_scene (GA and mtarini)
# Input: arg1 = region  code
# Input: arg2 = terrain type
# Input: arg3 = visible landmark (if any, else -1)  
# Output: none
("jump_to_random_scene", [
	(store_script_param, ":region",1),
	(store_script_param, ":terrain",2),
	(store_script_param, ":landmark",3),
	#(assign, reg10, ":landmark"),(display_message,"@LANDMARK: {reg10}"),
	
	(assign,":small_scene",0),
	(try_begin),(lt,"$number_of_combatants",70),(assign,":small_scene",1), # small scene variants are right after standard ones in module_scenes
	 (else_try),(lt,"$enemy_count1",30),		(assign,":small_scene",1), # no point in walking half an hour to stomp couple orcs
	(try_end),

	# in the following, according to region and terrain type, setup the first, the second, or both these variables:
    (assign, ":native_terrain_to_use", -1), # this is you need random terrain generation using a ground level vanilla terrain
    (assign, ":scene_to_use", -1),   # this if you want to use a specific scene
	(assign, "$bs_day_sound", "snd_wind_ambiance"), # default ambience
	(assign, "$bs_night_sound", "snd_wind_ambiance"),
	(try_begin),
		(eq,":landmark","p_town_erebor"),
		(assign,":scene_to_use","scn_erebor_outside"), 
	(else_try),
		(eq,":landmark","p_town_minas_tirith"),
		(assign,":scene_to_use","scn_minas_tirith_outside"), 
	(else_try),
		(eq,":landmark","p_town_isengard"),
		(assign, ":native_terrain_to_use", rt_steppe), 
		(assign,":scene_to_use","scn_isengard_outside"), 
	(else_try),
		(eq,":landmark","p_hand_isen"),		
		(assign,":scene_to_use","scn_handsign"), # randomize this scene 
	(else_try),
		(is_between,":landmark", fords_big_begin, fords_big_end), # Anduin fords
		(store_mod, ":tmp", ":landmark", 3), #3  big fords scenes
		(store_add, ":scene_to_use", "scn_ford_big1", ":tmp"),

		#(store_random_in_range, ":scene_to_use", "scn_ford_big1", "scn_ford_small1"),
		(assign, "$bs_night_sound", "snd_night_ambiance"),
	(else_try),
		(is_between,":landmark", fords_small_begin, fords_small_end), # Anduin fords
		(store_mod, ":tmp", ":landmark", 3), #3  small fords scenes
		(store_add, ":scene_to_use", "scn_ford_small1", ":tmp"),		
		#(store_random_in_range, ":scene_to_use", "scn_ford_small1", "scn_erebor_siege"),
		(assign, "$bs_night_sound", "snd_night_ambiance"),
	(else_try),
		(eq,":landmark", landmark_great_east_road ), 
		(assign, ":native_terrain_to_use", rt_steppe), 
		(assign,":scene_to_use","scn_great_east_road"),
	(else_try),
		(eq,":landmark", landmark_old_forest_road ),
		(assign,":scene_to_use","scn_old_forest_road"),
	(else_try),
		(eq,":region",region_dead_marshes),
		(assign,":scene_to_use","scn_deadmarshes"),
		(assign, "$bs_day_sound", "snd_deadmarshes_ambiance"),
		(assign, "$bs_night_sound", "snd_deadmarshes_ambiance"),
	(else_try),
     	(this_or_next|eq,":region",region_firien_wood),
		(eq,":region",region_druadan_forest),
		(store_random_in_range, ":scene_to_use", "scn_forest_firien1", "scn_forest_end"),
		(assign, "$bs_day_sound", "snd_neutralforest_ambiance"),
		(assign, "$bs_night_sound", "snd_night_ambiance"),
	(else_try),
		(eq,":region",region_lorien),
		(store_random_in_range, ":scene_to_use", "scn_forest_lorien1", "scn_forest_mirkwood1"),
		(assign, "$bs_day_sound", "snd_neutralforest_ambiance"),
		(assign, "$bs_night_sound", "snd_night_ambiance"),
	(else_try),
		(eq,":region",region_fangorn),
		(store_random_in_range, ":scene_to_use", "scn_forest_fangorn1", "scn_forest_ithilien1"),
		(assign, "$bs_day_sound", "snd_fangorn_ambiance"),
		(assign, "$bs_night_sound", "snd_night_ambiance"),
	(else_try),
		(is_between,":region",region_n_mirkwood,region_s_mirkwood+1),
		(store_random_in_range, ":scene_to_use", "scn_forest_mirkwood1", "scn_forest_firien1"),
		(assign, "$bs_day_sound", "snd_evilforest_ambiance"),
		(assign, "$bs_night_sound", "snd_night_ambiance"),
	(else_try),
		(is_between,":region",region_n_ithilien,region_s_ithilien+1),
		(store_random_in_range, reg1, 0,5),
		(try_begin),(lt, reg1, 3),(store_random_in_range, ":scene_to_use", "scn_forest_ithilien1", "scn_forest_lorien1"),
		 (else_try),              (assign, ":native_terrain_to_use", rt_steppe_forest),
		(try_end),
		(assign, "$bs_night_sound", "snd_night_ambiance"),
	(else_try),		# occasional forest terrain, in gondor: use forest battlefield regardless of region (but gondor outer terrain)
		(is_between, ":terrain", rt_forest_begin, rt_forest_end),
		(is_between,":region",region_pelennor, region_anorien+1),
		(assign, ":native_terrain_to_use", rt_forest),
		(assign,":scene_to_use","scn_random_scene_plain_small"), # so that outer terrain of gondor is used
		(assign, "$bs_day_sound", "snd_neutralforest_ambiance"),
	(else_try),		# occasional forest terrain, in rohan: use forest battlefield regardless of region (but rohan outer terrain)
		(is_between, ":terrain", rt_forest_begin, rt_forest_end),
		(is_between,":region",region_harrowdale, region_westfold+1),
		(assign, ":native_terrain_to_use", rt_forest),
		(assign,":scene_to_use","scn_random_scene_steppe_small"), # so that outer terrain of rohan is used
		(assign, "$bs_day_sound", "snd_neutralforest_ambiance"),
	(else_try),		# occasional forest terrain, anywhere else: use forest battlefield regardless of region (but flat outer terrain)
		(is_between, ":terrain", rt_forest_begin, rt_forest_end),
		(assign, ":native_terrain_to_use", rt_forest),
		(assign,":scene_to_use","scn_random_scene_desert_small"), # so that outer terrain flat is used
		(assign, "$bs_day_sound", "snd_neutralforest_ambiance"),
	(else_try),		# gondor regions
		(is_between,":region",region_pelennor, region_anorien+1),
		(assign, ":native_terrain_to_use", rt_plain),  # gondor default
	(else_try),		# dry-brown regions
		(this_or_next|is_between,":region",region_n_undeep , region_s_undeep +1),
		(this_or_next|eq,":region",region_dagorlad),
		(eq,":region",region_brown_lands),
		(assign, ":native_terrain_to_use", rt_desert),  # should look more grey / drier
	(else_try),		# rohan regions
		(this_or_next|eq,":region",region_the_wold),
		(this_or_next|eq,":region",region_emyn_muil),
		(is_between,":region",region_harrowdale, region_gap_of_rohan+1),
		(assign, ":native_terrain_to_use", rt_steppe),  # rohan default
	(else_try),		# mountains regions
		(this_or_next|eq,":region",region_misty_mountains),
		(eq,":region",region_grey_mountains),
		(assign, ":native_terrain_to_use", rt_steppe),  # mountains
	(else_try),		# marshes 
		(this_or_next|eq,":region",region_entwash),
		(eq,":region",region_wetwang), 
		(assign, ":native_terrain_to_use", rt_snow),  # marsh
	(else_try),		# anything else
		(assign, ":native_terrain_to_use", rt_steppe),  
	(try_end),
	
	# not set the terrain
	(try_begin),(gt, ":native_terrain_to_use", -1), 
		# use native terrain autogeneration
		# make the terrain index SKIP the interval betweem desert (escluded) and mountain_forest (included) 
		(try_begin),(gt	,":native_terrain_to_use",rt_desert),(val_sub,":native_terrain_to_use",rt_mountain_forest-rt_desert),(try_end),
		(try_begin),(neq,"$relocated",1),
			(assign,"$relocated",1),						# don't store current location if already relocated
			(party_relocate_near_party,"p_pointer_player","p_main_party",0), #remember original player location 
		(try_end),
        (store_random_in_range, ":radius", 1, 5), # radius around base terrain Z=0 position for seed generation
		(store_add, reg10, "p_pointer_z_0_begin", ":native_terrain_to_use"),
		(party_relocate_near_party,"p_main_party",reg10,":radius"), # teleport to requested region
		
		#(display_message,"@debug: teleporitng to party ID N. {reg10}"),
		
		(try_begin),(eq,":scene_to_use",-1),
			# no scene_to_use defined: use the dafault one for the selected native terrain terrain
			(store_add, ":scene_to_use", ":native_terrain_to_use", "scn_random_scene_steppe" ),
			(val_sub, ":scene_to_use", 2), # steppe is terrain 2
			(try_begin), (eq, ":small_scene", 1), 
				# shring scene
				(le, ":native_terrain_to_use", rt_desert), #  forest don't have a small version
				
				(val_add, ":scene_to_use", "scn_random_scene_steppe_small"),
				(val_sub, ":scene_to_use", "scn_random_scene_steppe"),  # go to small scene index
			(try_end),
		(try_end),
	(try_end),
	(assign, reg10,":scene_to_use"), #(display_message,"@debug: using scene ID N. {reg10}"),
	(jump_to_scene,":scene_to_use"),

]),

# script_maybe_relocate_player_from_z0 (GA and mtarini)
("maybe_relocate_player_from_z0",[
	 (try_begin), #if "walk around place" used
	    (eq, "$relocated", 1),
	    (assign, "$relocated", 0),
        (party_relocate_near_party, "p_main_party", "p_pointer_player", 0),
	(try_end),
]),

# script_enter_dungeon
# Input: arg1 = center_no, arg2 = mission_template_no
# Output: none
("enter_dungeon",
    [ (store_script_param_1, ":center_no"),
      (store_script_param_2, ":mission_template_no"),
      
      (set_jump_mission,":mission_template_no"),
      (party_get_slot, ":dungeon_scene", ":center_no", slot_town_prison),
      
      (modify_visitors_at_site,":dungeon_scene"),(reset_visitors),
      (assign, ":cur_pos", 16),
      (call_script, "script_get_heroes_attached_to_center_as_prisoner", ":center_no", "p_temp_party"),
      (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),
        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":stack_troop"),
        (val_add,":cur_pos", 1),
      (try_end),
      
      (set_jump_entry, 0),
      (jump_to_scene,":dungeon_scene"),
      (scene_set_slot, ":dungeon_scene", slot_scene_visited, 1),
      (change_screen_mission),
]),

# script_enter_court
# Input: arg1 = center_no
# Output: none
("enter_court",
    [ (store_script_param_1, ":center_no"),
      
      (assign, "$talk_context", tc_court_talk),
      
      (set_jump_mission,"mt_visit_town_castle"),
      (party_get_slot, ":castle_scene", ":center_no", slot_town_castle),
      (modify_visitors_at_site,":castle_scene"),
      (reset_visitors),
      #Adding guards
      (party_get_slot, ":guard_troop", ":center_no", slot_town_castle_guard_troop),
##########
      (try_begin),
        (le, ":guard_troop", 0),
        (assign, ":guard_troop", "trp_guard_of_the_fountain_court"),
      (try_end),
      (set_visitor, 6, ":guard_troop"),
      (set_visitor, 7, ":guard_troop"),
	  
	  # place the two hobbits; USE ENTRY POINT 8 !!! (mtarini)
	  (try_begin),
	    (gt, "$tld_war_began", 0), (eq, ":castle_scene", "scn_minas_tirith_castle"),
		(try_begin), (troop_slot_eq, "trp_pippin_notmet", slot_troop_met_previously, 0),
			(set_visitor, 8, "trp_pippin_notmet"), # a "halfling"
		(else_try),
			(set_visitor, 8, "trp_pippin"),
		(try_end),
	  (else_try), 
	    (gt, "$tld_war_began", 0), (eq, ":castle_scene", "scn_edoras_castle"),
		(try_begin), (troop_slot_eq, "trp_merry_notmet", slot_troop_met_previously, 0),
			(set_visitor, 8, "trp_merry_notmet"),  # a "halfling"
		(else_try),
			(set_visitor, 8, "trp_merry"),
		(try_end),
	  (try_end),

      (assign, ":cur_pos", 16),
      (call_script, "script_get_heroes_attached_to_center", ":center_no", "p_temp_party"),
      (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
	  
	  # bugfix (mtarini): repirstinate original af_flags...
	  (try_for_range, ":i", 0, 32),
		 (try_begin),(is_between, ":i", 1, 16), (mission_tpl_entry_set_override_flags, "mt_visit_town_castle", ":i", af_override_horse),
		 (else_try),(mission_tpl_entry_set_override_flags, "mt_visit_town_castle", ":i", af_override_horse | af_override_weapons | af_override_head | af_override_gloves),
		 (try_end),
	  (end_try),
	  
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),
        (lt, ":cur_pos", 32), # spawn up to entry point 31
        (set_visitor, ":cur_pos", ":stack_troop"),
		(try_begin),
			(this_or_next|eq, ":stack_troop", "trp_knight_3_11"), #imladris elves all in helms
			(this_or_next|eq, ":stack_troop", "trp_knight_3_12"),
			(this_or_next|eq, ":stack_troop", "trp_imladris_lord"),
			(this_or_next|eq, ":stack_troop", "trp_lorien_lord"),
						 (eq, ":stack_troop", "trp_mordor_lord"), #Mouth in hood
			(mission_tpl_entry_set_override_flags, "mt_visit_town_castle", ":cur_pos", af_override_horse|af_override_weapons),
		(try_end),
        (val_add,":cur_pos", 1),
      (try_end),
      #TLD NPC companions
      (val_max, ":cur_pos", 17), #if no one else in court, skip 16 (could be a throne)
      (try_for_range, ":cur_troop", companions_begin, companions_end),
        (troop_slot_eq, ":cur_troop", slot_troop_cur_center, ":center_no"),
        (neg|main_party_has_troop, ":cur_troop"), #not already hired
        (assign, ":on_lease", 0),
        (try_begin),
          (check_quest_active,"qst_lend_companion"),
          (quest_slot_eq, "qst_lend_companion", slot_quest_target_troop, ":cur_troop"),
          (assign, ":on_lease", 1),
        (try_end),
        (eq, ":on_lease", 0),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_troop_faction, ":troop_faction", ":cur_troop"),
        (store_relation, ":rel", ":center_faction", ":troop_faction"),
        (ge, ":rel", 0), #only spawn if friendly center
        (lt, ":cur_pos", 32), # spawn up to entry point 31, can have multiple companions in a single town castle
        (set_visitor, ":cur_pos", ":cur_troop"),
        (val_add,":cur_pos", 1),
      (try_end),
	
	(jump_to_scene,":castle_scene"),
	(scene_set_slot, ":castle_scene", slot_scene_visited, 1),
	(change_screen_mission),
]),

# script_find_high_ground_around_pos1
# Input: pos1 should hold center_position_no,  arg1 = team_no, arg2 = search_radius (in meters)
# Output: pos52 contains highest ground within <search_radius> meters of team leader
# Destroys position registers: pos10, pos11, pos15
("find_high_ground_around_pos1",
    [ (store_script_param, ":team_no", 1),
      (store_script_param, ":search_radius", 2),
      (val_mul, ":search_radius", 100),
      (get_scene_boundaries, pos10,pos11),
      #(team_get_leader, ":ai_leader", ":team_no"),
      (call_script, "script_team_get_nontroll_leader", ":team_no"),
      (assign, ":ai_leader", reg0),
      (agent_get_position, pos1, ":ai_leader"),
      (set_fixed_point_multiplier, 100),
      (position_get_x, ":o_x", pos1),
      (position_get_y, ":o_y", pos1),
      (store_sub, ":min_x", ":o_x", ":search_radius"),
      (store_sub, ":min_y", ":o_y", ":search_radius"),
      (store_add, ":max_x", ":o_x", ":search_radius"),
      (store_add, ":max_y", ":o_y", ":search_radius"),
      (position_get_x, ":scene_min_x", pos10),
      (position_get_x, ":scene_max_x", pos11),
      (position_get_y, ":scene_min_y", pos10),
      (position_get_y, ":scene_max_y", pos11),
      (val_max, ":min_x", ":scene_min_x"),
      (val_max, ":min_y", ":scene_min_y"),
      (val_min, ":max_x", ":scene_max_x"),
      (val_min, ":max_y", ":scene_max_y"),
      
      (store_div, ":min_x_meters", ":min_x", 100),
      (store_div, ":min_y_meters", ":min_y", 100),
      (store_div, ":max_x_meters", ":max_x", 100),
      (store_div, ":max_y_meters", ":max_y", 100),
      
      (assign, ":highest_pos_z", -10000),
      (copy_position, pos52, pos1),
      (init_position, pos15),
      
      (try_for_range, ":i_x", ":min_x_meters", ":max_x_meters"),
        (store_mul, ":i_x_cm", ":i_x", 100),
        (try_for_range, ":i_y", ":min_y_meters", ":max_y_meters"),
          (store_mul, ":i_y_cm", ":i_y", 100),
          (position_set_x, pos15, ":i_x_cm"),
          (position_set_y, pos15, ":i_y_cm"),
          (position_set_z, pos15, 10000),
          (position_set_z_to_ground_level, pos15),
          (position_get_z, ":cur_pos_z", pos15),
          (try_begin),
            (gt, ":cur_pos_z", ":highest_pos_z"),
            (copy_position, pos52, pos15),
            (assign, ":highest_pos_z", ":cur_pos_z"),
          (try_end),
        (try_end),
      (try_end),
]),

# script_remove_agent (mtarini)
("remove_agent", [
	(store_script_param, ":agent", 1),
	(init_position, pos5),  # send agent to Pluto ;)
	(agent_set_position,":agent", pos5), 				
	(agent_set_hit_points, ":agent", 0,0), 	# self destruct it!
	(set_show_messages,0),
	(agent_deliver_damage_to_agent, ":agent", ":agent"), 
	(set_show_messages,1),
]),
  
# script_select_battle_tactic
("select_battle_tactic", [
	(assign, "$ai_team_1_battle_tactic", 0),
	(get_player_agent_no, ":player_agent"),
	(agent_get_team, ":player_team", ":player_agent"),
	(try_begin),
		(num_active_teams_le, 2),
		(try_begin),(eq, ":player_team", 0),(assign, "$ai_team_1", 1),
		 (else_try),						(assign, "$ai_team_1", 0),
		(try_end),
		(assign, "$ai_team_2", -1),
	(else_try),
		(try_begin),(eq, ":player_team", 0),(assign, "$ai_team_1", 1),
		 (else_try),						(assign, "$ai_team_1", 0),
		(try_end),
		(store_add, "$ai_team_2", ":player_team", 2),
	(try_end),
	(call_script, "script_select_battle_tactic_aux", "$ai_team_1"),
	(assign, "$ai_team_1_battle_tactic", reg0),
	(try_begin),
		(ge, "$ai_team_2", 0),
		(call_script, "script_select_battle_tactic_aux", "$ai_team_2"),
		(assign, "$ai_team_2_battle_tactic", reg0),
	(try_end),
]),
# script_select_battle_tactic_aux
# Input: team_no
# Output: battle_tactic
("select_battle_tactic_aux",
    [ (store_script_param, ":team_no", 1),
      (assign, ":battle_tactic", 0),
      (assign, ":defense_not_an_option", 0),
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (try_begin),
        (eq, "$cant_leave_encounter", 1),
        (teams_are_enemies, ":team_no", ":player_team"),
        (assign, ":defense_not_an_option", 1),
      (try_end),
      (call_script, "script_team_get_class_percentages", ":team_no", 0),
      #(assign, ":ai_perc_infantry", reg0),
      (assign, ":ai_perc_archers",  reg1),
      (assign, ":ai_perc_cavalry",  reg2),
      (call_script, "script_team_get_class_percentages", ":team_no", 1),#enemies of the ai_team
      #(assign, ":enemy_perc_infantry", reg0),
      (assign, ":enemy_perc_archers",  reg1),
      #(assign, ":enemy_perc_cavalry",  reg2),

      (store_random_in_range, ":rand", 0, 100),      
      (try_begin),
        (this_or_next|lt, ":rand", 20),
        (assign, ":continue", 0),
        (try_begin),
          (teams_are_enemies, ":team_no", ":player_team"),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_hero_party),
          (assign, ":continue", 1),
        (else_try),
          (neg|teams_are_enemies, ":team_no", ":player_team"),
          (gt, "$g_ally_party", 0),
          (party_slot_eq, "$g_ally_party", slot_party_type, spt_kingdom_hero_party),
          (assign, ":continue", 1),
        (try_end),
        (eq, ":continue", 1),
        (try_begin),
          (eq, ":defense_not_an_option", 0),
          (gt, ":ai_perc_archers", 50),
          (lt, ":ai_perc_cavalry", 35),
          (assign, ":battle_tactic", btactic_hold),
        (else_try),							# charge enemy archers!
		  (gt, ":enemy_perc_archers", 50),
          (lt, ":ai_perc_archers", 25),
		  (assign, ":battle_tactic", btactic_charge),
        (else_try),
          (lt, ":rand", 80),
          (assign, ":battle_tactic", btactic_follow_leader),
        (try_end),
      (try_end),
      (assign, reg0, ":battle_tactic"),
]),
# script_battle_tactic_init
("battle_tactic_init",
    [ (call_script, "script_battle_tactic_init_aux", "$ai_team_1", "$ai_team_1_battle_tactic"),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (call_script, "script_battle_tactic_init_aux", "$ai_team_2", "$ai_team_2_battle_tactic"),
      (try_end),
]),
# script_battle_tactic_init_aux
# Input: team_no, battle_tactic
("orig_battle_tactic_init_aux", # formations change
    [ (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
      #(team_get_leader, ":ai_leader", ":team_no"),
      (call_script, "script_team_get_nontroll_leader", ":team_no"),
      (assign, ":ai_leader", reg0),
      (try_begin),
        (eq, ":battle_tactic", btactic_hold),
        (agent_get_position, pos1, ":ai_leader"),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30),
        (copy_position, pos1, pos52),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30), # call again just in case we are not at peak point.
        (copy_position, pos1, pos52),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30), # call again just in case we are not at peak point.
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos52),
        (team_give_order, ":team_no", grc_archers, mordr_advance),
        (team_give_order, ":team_no", grc_archers, mordr_advance),
      (else_try), # GA: added spreaded charge
        (eq, ":battle_tactic", btactic_charge),
        (team_give_order, ":team_no", grc_everyone, mordr_spread_out),
        (team_give_order, ":team_no", grc_everyone, mordr_spread_out),
        (team_give_order, ":team_no", grc_everyone, mordr_charge),
      (else_try),
	    (eq, ":battle_tactic", btactic_follow_leader),
        #(team_get_leader, ":ai_leader", ":team_no"),
        (agent_set_speed_limit, ":ai_leader", 8),
        (agent_get_position, pos60, ":ai_leader"),
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos60),
      (try_end),
]),
# script_battle_tactic_apply
("battle_tactic_apply",
    [ (call_script, "script_battle_tactic_apply_aux", "$ai_team_1", "$ai_team_1_battle_tactic"),
      (assign, "$ai_team_1_battle_tactic", reg0),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (call_script, "script_battle_tactic_apply_aux", "$ai_team_2", "$ai_team_2_battle_tactic"),
        (assign, "$ai_team_2_battle_tactic", reg0),
      (try_end),
]),
# script_battle_tactic_apply_aux
# Input: team_no, battle_tactic
# Output: battle_tactic
("orig_battle_tactic_apply_aux", # formations change
    [ (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
      (store_mission_timer_a, ":mission_time"),
      (try_begin),
        (eq, ":battle_tactic", btactic_hold),
        (copy_position, pos1, pos52),
        (call_script, "script_get_closest3_distance_of_enemies_at_pos1", ":team_no", 1),
        (assign, ":avg_dist", reg0),
        (assign, ":min_dist", reg1),
        (try_begin),
          (this_or_next|lt, ":min_dist", 1000),
          (lt, ":avg_dist", 4000),
          (assign, ":battle_tactic", 0),
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        #(team_get_leader, ":ai_leader", ":team_no"),
        (call_script, "script_team_get_nontroll_leader", ":team_no"),
        (assign, ":ai_leader", reg0),
        (agent_set_speed_limit, ":ai_leader", 9),
        (call_script, "script_team_get_average_position_of_enemies", ":team_no"),
        (copy_position, pos60, pos0),
        (agent_get_position, pos61, ":ai_leader"),
        (position_transform_position_to_local, pos62, pos61, pos60), #pos62 = vector to enemy w.r.t leader
        (position_normalize_origin, ":distance_to_enemy", pos62),
        (convert_from_fixed_point, ":distance_to_enemy"),
        (assign, reg17, ":distance_to_enemy"),
        (position_get_x, ":dir_x", pos62),
        (position_get_y, ":dir_y", pos62),
        (val_mul, ":dir_x", 23),
        (val_mul, ":dir_y", 23), #move 23 meters
        (position_set_x, pos62, ":dir_x"),
        (position_set_y, pos62, ":dir_y"),
      
        (position_transform_position_to_parent, pos63, pos61, pos62), #pos63 is 23m away from leader in the direction of the enemy.
        (position_set_z_to_ground_level, pos63),
      
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos63),
#        (team_give_order, ":team_no", grc_everyone, mordr_follow),
        (agent_get_position, pos1, ":ai_leader"),
#        (call_script, "script_get_closest3_distance_of_enemies_at_pos1", ":team_no"),
#        (assign, ":avg_dist", reg0),
#        (assign, ":min_dist", reg1),
        (try_begin),
          (lt, ":distance_to_enemy", 50),
          (ge, ":mission_time", 30),
          (assign, ":battle_tactic", 0),
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
          (agent_set_speed_limit, ":ai_leader", 60),
        (try_end),
      (try_end),
      
      (try_begin), # charge everyone after a while
        (neq, ":battle_tactic", 0),
        (ge, ":mission_time", 300),
        (assign, ":battle_tactic", 0),
        (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (team_get_leader, ":ai_leader", ":team_no"),
        (agent_set_speed_limit, ":ai_leader", 60),
      (try_end),
      (assign, reg0, ":battle_tactic"),
]),

# script_team_get_class_percentages
# Input: arg1: team_no, arg2: try for team's enemies
# Output: reg0: percentage infantry, reg1: percentage archers, reg2: percentage cavalry
("team_get_class_percentages",
    [ (assign, ":num_infantry", 0),
      (assign, ":num_archers", 0),
      (assign, ":num_cavalry", 0),
      (assign, ":num_total", 0),
      (store_script_param, ":team_no", 1),
      (store_script_param, ":negate", 2),
      (try_for_agents,":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (assign, ":continue", 0),
        (try_begin),
          (eq, ":negate", 1),
          (teams_are_enemies, ":agent_team", ":team_no"),
          (assign, ":continue", 1),
        (else_try),
          (eq, ":agent_team", ":team_no"),
          (assign, ":continue", 1),
        (try_end),
        (eq, ":continue", 1),
        (val_add, ":num_total", 1),
        (agent_get_class, ":agent_class", ":cur_agent"),
        (try_begin),
          (eq, ":agent_class", grc_infantry),
          (val_add,  ":num_infantry", 1),
        (else_try),
          (eq, ":agent_class", grc_archers),
          (val_add,  ":num_archers", 1),
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (val_add,  ":num_cavalry", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq,  ":num_total", 0),
        (assign,  ":num_total", 1),
      (try_end),
      (store_mul, ":perc_infantry",":num_infantry",100),
      (val_div, ":perc_infantry",":num_total"),
      (store_mul, ":perc_archers",":num_archers",100),
      (val_div, ":perc_archers",":num_total"),
      (store_mul, ":perc_cavalry",":num_cavalry",100),
      (val_div, ":perc_cavalry",":num_total"),
      (assign, reg0, ":perc_infantry"),
      (assign, reg1, ":perc_archers"),
      (assign, reg2, ":perc_cavalry"),
]),

# script_get_closest3_distance_of_enemies_at_pos1
# Input: arg1: team_no, pos1
# Output: reg0: distance in cms.
("get_closest3_distance_of_enemies_at_pos1",
    [ (assign, ":min_distance_1", 100000),
      (assign, ":min_distance_2", 100000),
      (assign, ":min_distance_3", 100000),
      
      (store_script_param, ":team_no", 1),
      (try_for_agents,":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (teams_are_enemies, ":agent_team", ":team_no"),
       
        (agent_get_position, pos2, ":cur_agent"),
        (get_distance_between_positions,":cur_dist",pos2,pos1),
        (try_begin),
          (lt, ":cur_dist", ":min_distance_1"),
          (assign, ":min_distance_3", ":min_distance_2"),
          (assign, ":min_distance_2", ":min_distance_1"),
          (assign, ":min_distance_1", ":cur_dist"),
        (else_try),
          (lt, ":cur_dist", ":min_distance_2"),
          (assign, ":min_distance_3", ":min_distance_2"),
          (assign, ":min_distance_2", ":cur_dist"),
        (else_try),
          (lt, ":cur_dist", ":min_distance_3"),
          (assign, ":min_distance_3", ":cur_dist"),
        (try_end),
      (try_end),
      
      (assign, ":total_distance", 0),
      (assign, ":total_count", 0),
      (try_begin),
        (lt, ":min_distance_1", 100000),
        (val_add, ":total_distance", ":min_distance_1"),
        (val_add, ":total_count", 1),
      (try_end),
      (try_begin),
        (lt, ":min_distance_2", 100000),
        (val_add, ":total_distance", ":min_distance_2"),
        (val_add, ":total_count", 1),
      (try_end),
      (try_begin),
        (lt, ":min_distance_3", 100000),
        (val_add, ":total_distance", ":min_distance_3"),
        (val_add, ":total_count", 1),
      (try_end),
      (assign, ":average_distance", 100000),
      (try_begin),
        (gt, ":total_count", 0),
        (store_div, ":average_distance", ":total_distance", ":total_count"),
      (try_end),
      (assign, reg0, ":average_distance"),
      (assign, reg1, ":min_distance_1"),
      (assign, reg2, ":min_distance_2"),
      (assign, reg3, ":min_distance_3"),
]),

# script_team_get_average_position_of_enemies
# Input: arg1: team_no, 
# Output: pos0: average position.
("team_get_average_position_of_enemies",
    [ (store_script_param_1, ":team_no"),
      (init_position, pos0),
      (assign, ":num_enemies", 0),
      (assign, ":accum_x", 0),
      (assign, ":accum_y", 0),
      (assign, ":accum_z", 0),
      (try_for_agents,":enemy_agent"),
        (agent_is_alive, ":enemy_agent"),
        (agent_is_human, ":enemy_agent"),
        (agent_get_team, ":enemy_team", ":enemy_agent"),
        (teams_are_enemies, ":team_no", ":enemy_team"),
      
        (agent_get_position, pos62, ":enemy_agent"),
      
        (position_get_x, ":x", pos62),
        (position_get_y, ":y", pos62),
        (position_get_z, ":z", pos62),
      
        (val_add, ":accum_x", ":x"),
        (val_add, ":accum_y", ":y"),
        (val_add, ":accum_z", ":z"),
        (val_add, ":num_enemies", 1),
      (try_end),
      (store_div, ":average_x", ":accum_x", ":num_enemies"),
      (store_div, ":average_y", ":accum_y", ":num_enemies"),
      (store_div, ":average_z", ":accum_z", ":num_enemies"),

      (position_set_x, pos0, ":average_x"),
      (position_set_y, pos0, ":average_y"),
      (position_set_z, pos0, ":average_z"),
      (assign, reg0, ":num_enemies"),
]),

# script_search_troop_prisoner_of_party
# Input: arg1 = troop_no
# Output: reg0 = party_no (-1 if troop is not a prisoner.)
("search_troop_prisoner_of_party",
    [ (store_script_param_1, ":troop_no"),
      (assign, ":prisoner_of", -1),
      (try_for_parties, ":party_no"),
        (eq,  ":prisoner_of", -1),
        (this_or_next|eq, ":party_no", "p_main_party"),
        (ge, ":party_no", centers_begin),
        (party_count_prisoners_of_type, ":troop_found", ":party_no", ":troop_no"),
        (gt, ":troop_found", 0),
        (assign, ":prisoner_of", ":party_no"),
      (try_end),
      (assign, reg0, ":prisoner_of"),
]),

# script_change_debt_to_troop
# Input: arg1 = troop_no, arg2 = new debt amount
# Output: none NOT USED IN TLD
# ("change_debt_to_troop",
    # [ (store_script_param_1, ":troop_no"),
      # (store_script_param_2, ":new_debt"),
      
      # (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),
      # (assign, reg1, ":cur_debt"),
      # (val_add, ":cur_debt", ":new_debt"),
      # (assign, reg2, ":cur_debt"),
      # (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
      # (str_store_troop_name_link, s1, ":troop_no"),
	# (display_message, "@You now owe {reg2} RPs to {s1}."),
# ]),

# script_abort_quest
# Input: arg1 = quest_no, arg2 = apply relation penalty
# Output: none
("abort_quest",
    [ (store_script_param_1, ":quest_no"),
      (store_script_param_2, ":abort_type"), #0=aborted by event, 1=abort by talking 2=abort by expire
      (assign, ":quest_return_penalty", -1),
      (assign, ":quest_expire_penalty", -2),
      
#      (quest_get_slot, ":quest_object_troop", ":quest_no", slot_quest_object_troop),
      (try_begin),
        (this_or_next|eq, ":quest_no", "qst_deliver_message"),
        (eq, ":quest_no", "qst_deliver_message_to_enemy_lord"),
        (assign, ":quest_return_penalty", -2),
        (assign, ":quest_expire_penalty", -3),
      (else_try),
        (eq, ":quest_no", "qst_escort_messenger"),
        (quest_get_slot, ":quest_object_troop", "qst_escort_messenger", slot_quest_object_troop),
        (party_remove_members, "p_main_party", ":quest_object_troop", 1),
        (assign, ":quest_return_penalty", -2),
        (assign, ":quest_expire_penalty", -3),
##      (else_try),
##        (eq, ":quest_no", "qst_rescue_lady_under_siege"),
##        (party_remove_members, "p_main_party", ":quest_object_troop", 1),
##      (else_try),
##        (eq, ":quest_no", "qst_deliver_message_to_lover"),
##      (else_try),
##        (eq, ":quest_no", "qst_bring_prisoners_to_enemy"),
##        (try_begin),
##          (check_quest_succeeded, ":quest_no"),
##          (quest_get_slot, ":quest_target_amount", ":quest_no", slot_quest_target_amount),
##          (quest_get_slot, ":quest_object_troop", ":quest_no", slot_quest_object_troop),
##          (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
##          (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##          (assign, ":reward", reg0),
##          (val_mul, ":reward", ":quest_target_amount"),
##          (val_div, ":reward", 2),
##        (else_try),
##          (quest_get_slot, ":reward", ":quest_no", slot_quest_target_amount),
##        (try_end),
##        (call_script, "script_change_debt_to_troop", ":quest_giver_troop", ":reward"),
##      (else_try),
##        (eq, ":quest_no", "qst_bring_reinforcements_to_siege"),
##        (quest_get_slot, ":quest_target_amount", ":quest_no", slot_quest_target_amount),
##        (quest_get_slot, ":quest_object_troop", ":quest_no", slot_quest_object_troop),
##        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
##        (call_script, "script_game_get_join_cost", ":quest_object_troop"),
##        (assign, ":reward", reg0),
##        (val_mul, ":reward", ":quest_target_amount"),
##        (val_mul, ":reward", 2),
##        (call_script, "script_change_debt_to_troop", ":quest_giver_troop", ":reward"),
##      (else_try),
##        (eq, ":quest_no", "qst_deliver_supply_to_center_under_siege"),
##        (quest_get_slot, ":quest_target_amount", ":quest_no", slot_quest_target_amount),
##        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
##        (store_item_value, ":reward", "itm_siege_supply"),
##        (val_mul, ":reward", ":quest_target_amount"),
##        (call_script, "script_change_debt_to_troop", ":quest_giver_troop", ":reward"),
      (else_try),
        (eq, ":quest_no", "qst_raise_troops"),
        #(quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        #(call_script, "script_change_debt_to_troop", ":quest_giver_troop", 100),
        (assign, ":quest_return_penalty", -4),
        (assign, ":quest_expire_penalty", -5),
      (else_try),
        (eq, ":quest_no", "qst_deal_with_looters"),
        (quest_get_slot, ":looter_template", "qst_deal_with_looters", slot_quest_target_party_template),
        (try_for_parties, ":cur_party_no"),
          (party_get_template_id, ":cur_party_template", ":cur_party_no"),
          (eq, ":cur_party_template", ":looter_template"),
          (party_set_flags, ":cur_party_no", pf_quest_party, 0),
        (try_end),
        (assign, ":quest_return_penalty", -4),
        (assign, ":quest_expire_penalty", -5),
      # (else_try),
        # (eq, ":quest_no", "qst_deal_with_bandits_at_lords_village"),
        # (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        # (call_script, "script_change_debt_to_troop", ":quest_giver_troop", 200),
        # (assign, ":quest_return_penalty", -5),
        # (assign, ":quest_expire_penalty", -6),
      # (else_try),
        # (eq, ":quest_no", "qst_collect_taxes"),
        # (quest_get_slot, ":gold_reward", ":quest_no", slot_quest_gold_reward),
        # (quest_set_slot, ":quest_no", slot_quest_gold_reward, 0),
        # (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        # (call_script, "script_change_debt_to_troop", ":quest_giver_troop", ":gold_reward"),
        # (assign, ":quest_return_penalty", -4),
        # (assign, ":quest_expire_penalty", -6),
##      (else_try),
##        (eq, ":quest_no", "qst_capture_messenger"),
##      (else_try),
##        (eq, ":quest_no", "qst_bring_back_deserters"),
      (else_try),
        (eq, ":quest_no", "qst_hunt_down_fugitive"),
        (assign, ":quest_return_penalty", -3),
        (assign, ":quest_expire_penalty", -4),
      # (else_try),
        # (eq, ":quest_no", "qst_kill_local_merchant"),
      (else_try),
        (eq, ":quest_no", "qst_bring_back_runaway_serfs"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -1),
      (else_try),
        (eq, ":quest_no", "qst_lend_companion"),
      # (else_try),
        # (eq, ":quest_no", "qst_collect_debt"),
        # (try_begin),
          # (quest_slot_eq, "qst_collect_debt", slot_quest_current_state, 1), #debt collected but not delivered
          # (quest_get_slot, ":debt", "qst_collect_debt", slot_quest_target_amount),
          # (quest_get_slot, ":quest_giver", "qst_collect_debt", slot_quest_giver_troop),
          # (call_script, "script_change_debt_to_troop", ":quest_giver", ":debt"),
          # (assign, ":quest_return_penalty", -3),
          # (assign, ":quest_expire_penalty", -6),
        # (else_try),
          # (assign, ":quest_return_penalty", -3),
          # (assign, ":quest_expire_penalty", -4),
        # (try_end),
      # (else_try),
        # (eq, ":quest_no", "qst_deal_with_bandits_at_lords_village"),
        # (assign, ":quest_return_penalty", -6),
        # (assign, ":quest_expire_penalty", -6),
      # (else_try),
        # (eq, ":quest_no", "qst_raid_caravan_to_start_war"),
        # (assign, ":quest_return_penalty", -10),
        # (assign, ":quest_expire_penalty", -13),
      # (else_try),
        # (eq, ":quest_no", "qst_persuade_lords_to_make_peace"),
        # (assign, ":quest_return_penalty", -10),
        # (assign, ":quest_expire_penalty", -13),
      (else_try),
        (eq, ":quest_no", "qst_deal_with_night_bandits"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -1),
      (else_try),
        (eq, ":quest_no", "qst_deliver_food"),
        (assign, ":quest_return_penalty", -2),
        (assign, ":quest_expire_penalty", -4),
      (else_try),
        (eq, ":quest_no", "qst_deliver_iron"),
        (assign, ":quest_return_penalty", -2),
        (assign, ":quest_expire_penalty", -4),
    
      (else_try),
        (eq, ":quest_no", "qst_follow_spy"),
        (assign, ":quest_return_penalty", -2),
        (assign, ":quest_expire_penalty", -3),
        (try_begin),
          (party_is_active, "$qst_follow_spy_spy_party"),
          (remove_party, "$qst_follow_spy_spy_party"),
        (try_end),
        (try_begin),
          (party_is_active, "$qst_follow_spy_spy_partners_party"),
          (remove_party, "$qst_follow_spy_spy_partners_party"),
        (try_end),
      (else_try),
        (eq, ":quest_no", "qst_capture_enemy_hero"),
        (assign, ":quest_return_penalty", -3),
        (assign, ":quest_expire_penalty", -4),
      (else_try),
        (eq, ":quest_no", "qst_scout_enemy_town"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -2),
      (else_try),
        (eq, ":quest_no", "qst_dispatch_scouts"),
        (assign, ":quest_return_penalty", -2),
        (assign, ":quest_expire_penalty", -3),
#Enemy lord quests
      (else_try),
        (eq, ":quest_no", "qst_lend_surgeon"),

		##      (else_try),
##        (eq, ":quest_no", "qst_lend_companion"),
##        (quest_get_slot, ":quest_target_troop", "qst_lend_companion", slot_quest_target_troop),
##        (party_add_members, "p_main_party", ":quest_target_troop", 1),
##      (else_try),
##        (eq, ":quest_no", "qst_capture_conspirators"),
##      (else_try),
##        (eq, ":quest_no", "qst_defend_nobles_against_peasants"),
      # (else_try),
        # (eq, ":quest_no", "qst_incriminate_loyal_commander"),
        # (assign, ":quest_return_penalty", -5),
        # (assign, ":quest_expire_penalty", -6),
##      (else_try),
##        (eq, ":quest_no", "qst_hunt_down_raiders"),
##      (else_try),
##        (eq, ":quest_no", "qst_capture_prisoners"),

#Kingdom lady quests
      # (else_try),
        # (eq, ":quest_no", "qst_rescue_lord_by_replace"),
        # (assign, ":quest_return_penalty", -1),
        # (assign, ":quest_expire_penalty", -1),
      # (else_try),
        # (eq, ":quest_no", "qst_deliver_message_to_prisoner_lord"),
        # (assign, ":quest_return_penalty", 0),
        # (assign, ":quest_expire_penalty", -1),
      # (else_try),
        # (eq, ":quest_no", "qst_duel_for_lady"),
        # (assign, ":quest_return_penalty", -1),
        # (assign, ":quest_expire_penalty", -1),
      
      #Kingdom Army quests
      (else_try),
        (eq, ":quest_no", "qst_follow_army"),
        #(assign, ":quest_return_penalty", -4),
        #(assign, ":quest_expire_penalty", -5),
      (else_try),
        (eq, ":quest_no", "qst_deliver_cattle_to_army"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -2),
      (else_try),
        (eq, ":quest_no", "qst_join_siege_with_army"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -2),
      (else_try),
        (eq, ":quest_no", "qst_scout_waypoints"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -2),
    #Village Elder quests
      # (else_try),
        # (eq, ":quest_no", "qst_deliver_grain"),
        # (assign, ":quest_return_penalty", -6),
        # (assign, ":quest_expire_penalty", -7),
      # (else_try),
        # (eq, ":quest_no", "qst_deliver_cattle"),
        # (assign, ":quest_return_penalty", -3),
        # (assign, ":quest_expire_penalty", -4),
      # (else_try),
        # (eq, ":quest_no", "qst_train_peasants_against_bandits"),
        # (assign, ":quest_return_penalty", -4),
        # (assign, ":quest_expire_penalty", -5),

    #Mayor quests
      (else_try),
        (eq, ":quest_no", "qst_deliver_wine"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -3),
        #(val_add, "$debt_to_merchants_guild", "$qst_deliver_wine_debt"),
      (else_try),
        (eq, ":quest_no", "qst_move_cattle_herd"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -3),
      (else_try),
        (eq, ":quest_no", "qst_escort_merchant_caravan"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -3),
      (else_try),
        (eq, ":quest_no", "qst_troublesome_bandits"),
        (assign, ":quest_return_penalty", -1),
        (assign, ":quest_expire_penalty", -2),
      #Other quests
      # (else_try),
        # (eq, ":quest_no", "qst_join_faction"),
        # (assign, ":quest_return_penalty", -3),
        # (assign, ":quest_expire_penalty", -3),
        # (try_begin),
          # (call_script, "script_get_number_of_hero_centers", "trp_player"),
          # (gt, reg0, 0),
          # (call_script, "script_change_player_relation_with_faction", "$g_invite_faction", -10),
        # (try_end),
        # (assign, "$g_invite_faction", 0),
        # (assign, "$g_invite_faction_lord", 0),
        # (assign, "$g_invite_offered_center", 0),
      # (else_try),
        # (eq, ":quest_no", "qst_eliminate_bandits_infesting_village"),
        # (assign, ":quest_return_penalty", -3),
        # (assign, ":quest_expire_penalty", -3),
      (try_end),
      (try_begin),
        (gt, ":abort_type", 0),
        (quest_get_slot, ":quest_giver", ":quest_no", slot_quest_giver_troop),
        (assign, ":relation_penalty", ":quest_return_penalty"),
        (try_begin),
          (eq, ":abort_type", 2),
          (assign, ":relation_penalty", ":quest_expire_penalty"),
        (try_end),
        (try_begin),
#          (this_or_next|is_between, ":quest_giver", village_elders_begin, village_elders_end),
          (is_between, ":quest_giver", mayors_begin, mayors_end),
          (quest_get_slot, ":quest_giver_center", ":quest_no", slot_quest_giver_center),
          (call_script, "script_change_player_relation_with_center", ":quest_giver_center", ":relation_penalty"),
        (else_try),
          (call_script, "script_change_player_relation_with_troop", ":quest_giver", ":relation_penalty"),
        (try_end),
      (try_end),
      (fail_quest, ":quest_no"),
#NPC companion changes begin
      (try_begin),
        (gt, ":abort_type", 0),
        (call_script, "script_objectionable_action", tmt_honest, "str_fail_quest"),
      (try_end),
#NPC companion changes end
	(call_script, "script_end_quest", ":quest_no"),
]),

# script_cf_is_quest_troop
# Input: arg1 = troop_no
# Output: none (can fail)
("cf_is_quest_troop",
    [ (store_script_param_1, ":troop_no"),
      (assign, ":is_quest_troop", 0),
      (try_for_range, ":cur_quest", all_quests_begin, all_quests_end),
        (check_quest_active, ":cur_quest"),
        (quest_get_slot, ":quest_troop_1", ":cur_quest", slot_quest_target_troop),
        (quest_get_slot, ":quest_troop_2", ":cur_quest", slot_quest_object_troop),
        (quest_get_slot, ":quest_troop_3", ":cur_quest", slot_quest_giver_troop),
        (this_or_next|eq, ":quest_troop_1", ":troop_no"),
        (this_or_next|eq, ":quest_troop_2", ":troop_no"),
        (eq, ":quest_troop_3", ":troop_no"),
        (assign, ":is_quest_troop", 1),
      (try_end),
      (eq, ":is_quest_troop", 1),
]),

# script_check_friendly_kills
# Input: none
# Output: none (changes the morale of the player's party)
("check_friendly_kills",
    [(get_player_agent_own_troop_kill_count, ":count"),
     (try_begin),
       (neq, "$g_player_current_own_troop_kills", ":count"),
       (val_sub, ":count", "$g_player_current_own_troop_kills"),
       (val_add, "$g_player_current_own_troop_kills", ":count"),
       (val_mul, ":count", -1),
       (call_script, "script_change_player_party_morale", ":count"),
     (try_end),
]),

# script_simulate_retreat
# Input: arg1 = players_side_damage, arg2 = enemy_side_damage, s5 = title_string
# Output: none
("simulate_retreat",
    [ (call_script, "script_music_set_situation_with_culture", mtf_sit_killed),
      (set_show_messages, 0),
      (store_script_param, ":players_side_damage", 1),
      (store_script_param, ":enemy_side_damage", 2),

      (assign, ":players_side_strength", 0),
      (assign, ":enemy_side_strength", 0),
      
      (assign, ":do_calculate", 1),
      (try_begin),
        (try_for_agents, ":cur_agent"),
          (agent_is_human, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_set_slot, ":cur_agent", slot_agent_is_alive_before_retreat, 1),#needed for simulation

          (agent_get_troop_id, ":cur_troop", ":cur_agent"),
          (store_character_level, ":cur_level", ":cur_troop"),
          (val_add, ":cur_level", 5),
          (try_begin),
            (troop_is_hero, ":cur_troop"),
            (val_add, ":cur_level", 5),
          (try_end),
          (try_begin),
            (agent_is_ally, ":cur_agent"),
            (val_add, ":players_side_strength", ":cur_level"),
          (else_try),
            (val_add, ":enemy_side_strength", ":cur_level"),
          (try_end),
        (try_end),
        (eq, "$pin_player_fallen", 0),
        (lt, ":enemy_side_strength", ":players_side_strength"),
        (assign, ":do_calculate", 0),
      (try_end),
      
      (try_begin),
        (eq, ":do_calculate", 1),
        
        (assign, "$g_last_mission_player_damage", 0),
        (party_clear, "p_temp_party"),
        (party_clear, "p_temp_party_2"),
        (call_script, "script_simulate_battle_with_agents_aux", 0, ":players_side_damage"),
        (call_script, "script_simulate_battle_with_agents_aux", 1, ":enemy_side_damage"),
        
        (assign, ":display_casualties", 0),
        
        (try_begin),
          (gt, "$g_last_mission_player_damage", 0),
          (assign, ":display_casualties", 1),
          (assign, reg1, "$g_last_mission_player_damage"),
          (str_store_string, s12, "str_casualty_display_hp"),
        (else_try),
          (str_clear, s12),
        (try_end),
        
        (call_script, "script_print_casualties_to_s0", "p_temp_party", 1),
        (try_begin),
          (party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
          (gt, ":num_stacks", 0),
          (assign, ":display_casualties", 1),
        (try_end),
        (str_store_string_reg, s10, s0),
        
        (call_script, "script_print_casualties_to_s0", "p_temp_party_2", 1),
        (try_begin),
          (party_get_num_companion_stacks, ":num_stacks", "p_temp_party_2"),
          (gt, ":num_stacks", 0),
          (assign, ":display_casualties", 1),
        (try_end),
        (str_store_string_reg, s11, s0),
        (try_begin),
          (eq, ":display_casualties", 1),
          (dialog_box,"str_casualty_display", s5),
        (try_end),
      (try_end),
      (set_show_messages, 1),

      #Calculating morale penalty (can be between 0-30)
      (assign, ":ally_casualties", 0),
      (assign, ":enemy_casualties", 0),
      (assign, ":total_allies", 0),
      
      (try_for_agents, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (try_begin),
          (agent_is_ally, ":cur_agent"),
          (val_add, ":total_allies", 1),
          (try_begin),
            (neg|agent_is_alive, ":cur_agent"),
            (val_add, ":ally_casualties", 1),
          (try_end),
        (else_try),
          (neg|agent_is_alive, ":cur_agent"),
          (val_add, ":enemy_casualties", 1),
        (try_end),
      (try_end),
      (store_add, ":total_casualties", ":ally_casualties", ":enemy_casualties"),
      (try_begin),
        (gt, ":total_casualties", 0),
        (store_mul, ":morale_adder", ":ally_casualties", 100),
        (val_div, ":morale_adder", ":total_casualties"),
        (val_mul, ":morale_adder", ":ally_casualties"),
        (val_div, ":morale_adder", ":total_allies"),
        (val_mul, ":morale_adder", -30),
        (val_div, ":morale_adder", 100),
        (call_script, "script_change_player_party_morale", ":morale_adder"),
      (try_end),
]),

# script_simulate_battle_with_agents_aux
# For internal use only
# Input: arg1 = attacker_side (0 = ally, 1 = enemy), arg2 = damage amount
# Output: none
("simulate_battle_with_agents_aux",
    [ (store_script_param_1, ":attacker_side"),
      (store_script_param_2, ":damage"),
      
      (get_player_agent_no, ":player_agent"),
      (try_for_agents, ":cur_agent"),
        (neq, ":player_agent", ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        #do not check agent_is_alive, check slot_agent_is_alive_before_retreat instead, so that dead agents can still hit enemies
        (agent_slot_eq, ":cur_agent", slot_agent_is_alive_before_retreat, 1),
        (try_begin),
          (agent_is_ally, ":cur_agent"),
          (assign, ":cur_agents_side", 0),
        (else_try),
          (assign, ":cur_agents_side", 1),
        (try_end),
        (eq, ":cur_agents_side", ":attacker_side"),
        (agent_get_position, pos2, ":cur_agent"),
        (assign, ":closest_agent", -1),
        (assign, ":min_distance", 100000),
        (try_for_agents, ":cur_agent_2"),
          (agent_is_human, ":cur_agent_2"),
          (agent_is_alive, ":cur_agent_2"),
          (try_begin),
            (agent_is_ally, ":cur_agent_2"),
            (assign, ":cur_agents_side_2", 0),
          (else_try),
            (assign, ":cur_agents_side_2", 1),
          (try_end),
          (this_or_next|neq, ":cur_agent_2", ":player_agent"),
          (eq, "$pin_player_fallen", 0),
          (neq, ":attacker_side", ":cur_agents_side_2"),
          (agent_get_position, pos3, ":cur_agent_2"),
          (get_distance_between_positions, ":cur_distance", pos2, pos3),
          (lt, ":cur_distance", ":min_distance"),
          (assign, ":min_distance", ":cur_distance"),
          (assign, ":closest_agent", ":cur_agent_2"),
        (try_end),
        (ge, ":closest_agent", 0),
        #Fight
        (agent_get_class, ":agent_class", ":cur_agent"),
        (assign, ":agents_speed", 1),
        (assign, ":agents_additional_hit", 0),
        (try_begin),
          (eq, ":agent_class", grc_archers),
          (assign, ":agents_additional_hit", 2),
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (assign, ":agents_speed", 2),
        (try_end),
        (agent_get_class, ":agent_class", ":closest_agent"),
        (assign, ":agents_speed_2", 1),
        (try_begin),
          (eq, ":agent_class", grc_cavalry),
          (assign, ":agents_speed_2", 2),
        (try_end),
        (assign, ":agents_hit", 18000),
        (val_add, ":min_distance", 3000),
        (val_div, ":agents_hit", ":min_distance"),
        (val_mul, ":agents_hit", 2),# max 10, min 2 hits within 150 meters
        
        (val_mul, ":agents_hit", ":agents_speed"),
        (val_div, ":agents_hit", ":agents_speed_2"),
        (val_add, ":agents_hit", ":agents_additional_hit"),
        
        (assign, ":cur_damage", ":damage"),
        (agent_get_troop_id, ":closest_troop", ":closest_agent"),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (store_character_level, ":closest_level", ":closest_troop"),
        (store_character_level, ":cur_level", ":cur_troop"),
        (store_sub, ":level_dif", ":cur_level", ":closest_level"),
        (val_div, ":level_dif", 5),
        (val_add, ":cur_damage", ":level_dif"),
        
        (try_begin),
          (eq, ":closest_agent", ":player_agent"),
          (val_div, ":cur_damage", 2),
          (store_agent_hit_points, ":init_player_hit_points", ":player_agent", 1),
        (try_end),
        
        (try_for_range, ":unused", 0, ":agents_hit"),
          (store_random_in_range, ":random_damage", 0, 100),
          (lt, ":random_damage", ":cur_damage"),
          (agent_deliver_damage_to_agent, ":cur_agent", ":closest_agent"),
        (try_end),
        
        (try_begin),
          (eq, ":closest_agent", ":player_agent"),
          (store_agent_hit_points, ":final_player_hit_points", ":player_agent", 1),
          (store_sub, ":hit_points_difference", ":init_player_hit_points", ":final_player_hit_points"),
          (val_add, "$g_last_mission_player_damage", ":hit_points_difference"),
        (try_end),
        
        (neg|agent_is_alive, ":closest_agent"),
        (try_begin),
          (eq, ":attacker_side", 1),
          (party_add_members, "p_temp_party", ":closest_troop", 1),
          (try_begin),
            (agent_is_wounded, ":closest_agent"),
            (party_wound_members, "p_temp_party", ":closest_troop", 1),
          (try_end),
        (else_try),
          (party_add_members, "p_temp_party_2", ":closest_troop", 1),
          (try_begin),
            (agent_is_wounded, ":closest_agent"),
            (party_wound_members, "p_temp_party_2", ":closest_troop", 1),
          (try_end),
        (try_end),
      (try_end),
]),

# script_map_get_random_position_around_position_within_range
# Input: arg1 = minimum_distance in km, arg2 = maximum_distance in km, pos1 = origin position
# Output: pos2 = result position
("map_get_random_position_around_position_within_range",
    [ (store_script_param_1, ":min_distance"),
      (store_script_param_2, ":max_distance"),
      (val_mul, ":min_distance", 100),
      (assign, ":continue", 1),
      (try_for_range, ":unused", 0, 20),
        (eq, ":continue", 1),
        (map_get_random_position_around_position, pos2, pos1, ":max_distance"),
        (get_distance_between_positions, ":distance", pos2, pos1),
        (ge, ":distance", ":min_distance"),
        (assign, ":continue", 0),
      (try_end),
]),

# script_troop_get_leaded_center_with_index
# Input: arg1 = troop_no, arg2 = center index within range between zero and the number of centers that troop owns
# Output: reg0 = center_no
("troop_get_leaded_center_with_index",
    [ (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":random_center"),
      (assign, ":result", -1),
      (assign, ":center_count", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (val_add, ":center_count", 1),
        (gt, ":center_count", ":random_center"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
]),

# script_cf_troop_get_random_leaded_walled_center_with_less_strength_priority
# Input: arg1 = troop_no, arg2 = preferred_center_no
# Output: reg0 = center_no (Can fail)
("cf_troop_get_random_leaded_walled_center_with_less_strength_priority",
    [ (store_script_param, ":troop_no", 1),
      (store_script_param, ":preferred_center_no", 2),

      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
        (val_add, ":num_centers", 1),
        (try_begin),
          (eq, ":center_no", ":preferred_center_no"),
          (val_add, ":num_centers", 99),
        (try_end),
##        (call_script, "script_party_calculate_regular_strength", ":center_no"),
##        (assign, ":strength", reg0),
##        (lt, ":strength", 80),
##        (store_sub, ":strength", 100, ":strength"),
##        (val_div, ":strength", 20),
##        (val_add, ":num_centers", ":strength"),
      (try_end),
      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":result", -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":center_no", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
##        (try_begin),
##          (call_script, "script_party_calculate_regular_strength", ":center_no"),
##          (assign, ":strength", reg0),
##          (lt, ":strength", 80),
##          (store_sub, ":strength", 100, ":strength"),
##          (val_div, ":strength", 20),
##          (val_sub, ":random_center", ":strength"),
##        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
]),

# script_cf_troop_get_random_leaded_town_or_village_except_center
# Input: arg1 = troop_no, arg2 = except_center_no
# Output: reg0 = center_no (Can fail)
("cf_troop_get_random_leaded_town_or_village_except_center",
    [ (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":except_center_no"),

      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (neq, ":center_no", ":except_center_no"),
        (val_add, ":num_centers", 1),
      (try_end),

      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":end_cond", centers_end),
      (try_for_range, ":center_no", centers_begin, ":end_cond"),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (neq, ":center_no", ":except_center_no"),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":target_center", ":center_no"),
        (assign, ":end_cond", 0),
      (try_end),
      (assign, reg0, ":target_center"),
]),

("start_current_battle", [
  	(assign, "$g_battle_result", 0),
	(assign, "$g_engaged_enemy", 1),
	(call_script, "script_calculate_renown_value"),
	(call_script, "script_calculate_battle_advantage"),(set_battle_advantage, reg0),
	(call_script, "script_calculate_battleside_races"),
	(troop_get_type, reg1, "trp_player"),
	(try_begin), #TLD: dwarves are always on foot
		(eq, reg1, tf_dwarf),
		(mission_tpl_entry_set_override_flags, "mt_lead_charge", 3, af_override_horse),	
	(try_end),	
	(set_party_battle_mode),
	(set_jump_mission,"mt_lead_charge"),
	(call_script, "script_jump_to_random_scene","$current_player_region","$current_player_terrain","$current_player_landmark"),
	(assign, "$g_next_menu", "mnu_simple_encounter"), 
	(jump_to_menu, "mnu_battle_debrief"),
	(change_screen_mission),
]),

# script_collect_friendly_parties
# Fills the party p_collective_friends with the members of parties attached to main_party and ally_party_no
("collect_friendly_parties",
    [ (party_collect_attachments_to_party, "p_main_party", "p_collective_friends"),
      (try_begin),
        (gt, "$g_ally_party", 0),
        (party_collect_attachments_to_party, "$g_ally_party", "p_temp_party"),
        (assign, "$g_move_heroes", 1),
        (call_script, "script_party_add_party", "p_collective_friends", "p_temp_party"),
      (try_end),
]),

# script_encounter_calculate_fit
# Input: arg1 = troop_no
("encounter_calculate_fit",[
#      (assign, "$g_enemy_fit_for_battle_old",  "$g_enemy_fit_for_battle"),
#      (assign, "$g_friend_fit_for_battle_old", "$g_friend_fit_for_battle"),
#      (assign, "$g_main_party_fit_for_battle_old", "$g_main_party_fit_for_battle"),
      (call_script, "script_party_count_fit_for_battle", "p_main_party"),
 #     (assign, "$g_main_party_fit_for_battle", reg(0)),
      (call_script, "script_collect_friendly_parties"),
      (call_script, "script_party_count_fit_for_battle", "p_collective_friends"),
      (assign, "$g_friend_fit_for_battle", reg(0)),

      (party_clear, "p_collective_ally"),
      (try_begin),
        (gt, "$g_ally_party", 0),
        (party_is_active, "$g_ally_party"),
        (party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),
#        (call_script, "script_party_count_fit_for_battle", "p_collective_ally"),
#        (val_add, "$g_friend_fit_for_battle", reg(0)),
      (try_end),
      (party_clear, "p_collective_enemy"),
      (try_begin),
        (party_is_active, "$g_enemy_party"),
        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),
      (try_end),
      (call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
      (assign, "$g_enemy_fit_for_battle", reg(0)),
      (assign, reg11, "$g_enemy_fit_for_battle"),
      (assign, reg10, "$g_friend_fit_for_battle"),
]),

# script_encounter_init_variables
# Input: arg1 = troop_no
("encounter_init_variables",
    [ (assign, "$capture_screen_shown", 0),
      (assign, "$loot_screen_shown", 0),
      (assign, "$thanked_by_ally_leader", 0),
      (assign, "$g_battle_result", 0),
      (assign, "$cant_leave_encounter", 0),
      (assign, "$cant_talk_to_enemy", 0),
      (assign, "$last_defeated_hero", 0),
      (assign, "$last_freed_hero", 0),
      (assign, "$battle_renown_total", 0),

      (call_script, "script_encounter_calculate_fit"),
      (call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
      (call_script, "script_party_calculate_strength", "p_main_party", 0),
      (assign, "$g_starting_strength_main_party", reg0),
      (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"),
      (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
      (assign, "$g_starting_strength_enemy_party", reg0),
#      (assign, "$g_starting_strength_ally_party", 0),
      (assign, "$g_strength_contribution_of_player", 100),

      (call_script, "script_party_copy", "p_collective_friends_backup", "p_collective_friends"),
      (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
      (assign, "$g_starting_strength_friends", reg0),

      (store_mul, "$g_strength_contribution_of_player","$g_starting_strength_main_party", 100), # reduce contribution if we are helping someone.
      (val_div, "$g_strength_contribution_of_player","$g_starting_strength_friends"),

#      (try_begin),
#        (gt, "$g_ally_party", 0),
#        (call_script, "script_party_copy", "p_ally_party_backup", "p_collective_ally"),
#        (call_script, "script_party_calculate_strength", "p_collective_ally"),
#        (assign, "$g_starting_strength_ally_party", reg0),
#        (store_add, ":starting_strength_factor_combined","$g_starting_strength_ally_party","$g_starting_strength_main_party"),
#         (store_mul, "$g_strength_contribution_of_player","$g_starting_strength_main_party", 80), #reduce contribution if we are helping someone.
#        (val_div, "$g_strength_contribution_of_player",":starting_strength_factor_combined"),
#      (try_end),
]),

#script_party_vote_race
# each party member "votes" his race,. Votes accumulate in reg15 and reg16 (races groups)   17,18,19 (races) and tmp_slots (factions) -- mtarini
# outputs: reg20:  majority race group (tf_male: humans+elves+dwarf    OR    tf_orc: beasts)
# outputs: reg21:  majority race (beasts VS humans VS dwarf VS elves)
# outputs: reg22:  majority faction (or: NO FACTION for the rest)
("party_vote_race",
    [ 
	(store_script_param_1, ":party"), #Party_id
	# zero all voting
	(assign, reg15, 0), # humanoids
	(assign, reg16, 0), # orcoids
	(assign, reg17, 0), # humans
	(assign, reg18, 0), # dwarves
	(assign, reg19, 0), # elves
	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(faction_set_slot,":fac", slot_faction_temp_value, 0),
	(try_end),
	(assign, ":no_fac_votes", 0),
	
	# 
    (party_get_num_companion_stacks, ":num_stacks",":party"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_size, ":n",":party",":i_stack"),
		(party_stack_get_troop_id, ":tr",":party",":i_stack"),
		(troop_get_type,":race",":tr"),
		(store_troop_faction,":fac",":tr"),
		
        (try_begin),(eq, ":tr", "trp_player"),
			(val_mul, ":n", 8), # player "vote" counts for 8!
			(assign, ":fac", "$players_kingdom"),
		(try_end),
		
		(try_begin),(is_between, ":race", tf_orc_begin, tf_orc_end),
			(val_add, reg15, ":n"),
		(else_try), 
			(val_add, reg16, ":n"),
			(try_begin),(eq, ":race", tf_dwarf),
				(val_add, reg18, ":n"),
			(else_try), 
				(val_add, reg19, ":n"),
			(else_try), (is_between, ":race", tf_elf_begin, tf_elf_end),
				(val_add, reg17, ":n"),
			(try_end),
		(try_end),
		(try_begin),(is_between, ":fac", kingdoms_begin, kingdoms_end),
		   (faction_get_slot, ":tmp", ":fac", slot_faction_temp_value),
		   (val_add, ":tmp",":n"),
		   (faction_set_slot,  ":fac", slot_faction_temp_value,":tmp"),
		(else_try),
		   (val_add, ":no_fac_votes", ":n"),
		(try_end),
    (try_end),
	  
	# count votes
	(try_begin), (gt, reg15, reg16),
		(assign, reg20, tf_orc),     # RACE GROUP
		(assign, reg21, tf_orc),     # RACE
	(else_try), 
		(assign, reg20, tf_male), # RACE GROUP
		(try_begin), (gt, reg19, reg18),(gt, reg19, reg17),
			(assign, reg21, tf_elf_begin), # RACE
		(else_try), (gt, reg18, reg17),
			(assign, reg21, tf_dwarf),# RACE
		(else_try), 
			(assign, reg21, tf_male),# RACE
		(try_end),
	(try_end),
	
	(assign, reg22, fac_no_faction ), # a random default
	(assign, ":max", ":no_fac_votes"),
	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(faction_get_slot,":votes", ":fac", slot_faction_temp_value ),
		(gt, ":votes",  ":max"),
		(assign, ":max", ":votes"),
		(assign, reg22, ":fac"),
	(try_end),
	
	
]),

#script_calculate_battleside_races
# compute with domiant race each side of a battle is (mtarini)
# $player_side_race_group = humanoids or orchoids
# $player_side_race = eld, dwarves or men
("calculate_battleside_races", [

	# fcount friends
	(call_script, "script_party_vote_race", "p_collective_friends"),
	(assign, "$player_side_race_group", reg20),    
	(assign, "$player_side_race", reg21),     
	(assign, "$player_side_faction", reg22),   
	
	(call_script, "script_party_vote_race", "p_collective_enemy"),
	(assign, "$enemy_side_race_group", reg20),    
	(assign, "$enemy_side_race", reg21),     
	(assign, "$enemy_side_faction", reg22),   
	

]),

# script_get_first_agent_with_troop_id
# Input: arg1 = troop_no
# Output: agent_id
("cf_get_first_agent_with_troop_id",
    [ (store_script_param_1, ":troop_no"),
      #      (store_script_param_2, ":agent_no_to_begin_searching_after"),
      (assign, ":result", -1),
      (try_for_agents, ":cur_agent"),
        (eq, ":result", -1),
        ##        (try_begin),
        ##          (eq, ":cur_agent", ":agent_no_to_begin_searching_after"),
        ##          (assign, ":agent_no_to_begin_searching_after", -1),
        ##        (try_end),
        ##        (eq, ":agent_no_to_begin_searching_after", -1),
        (agent_get_troop_id, ":cur_troop_no", ":cur_agent"),
        (eq, ":cur_troop_no", ":troop_no"),
        (assign, ":result", ":cur_agent"),
      (try_end),
      (assign, reg0, ":result"),
      (neq, reg0, -1),
]),

# script_cf_team_get_average_position_of_agents_with_type_to_pos1
# Input: arg1 = team_no, arg2 = class_no (grc_everyone, grc_infantry, grc_cavalry, grc_archers, grc_heroes)
# Output: none, pos1 = average_position (0,0,0 if there are no matching agents)
("cf_team_get_average_position_of_agents_with_type_to_pos1",
    [ (store_script_param_1, ":team_no"),
      (store_script_param_2, ":class_no"),
      (assign, ":total_pos_x", 0),
      (assign, ":total_pos_y", 0),
      (assign, ":total_pos_z", 0),
      (assign, ":num_agents", 0),
      (set_fixed_point_multiplier, 100),
      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":cur_team_no", ":cur_agent"),
        (eq, ":cur_team_no", ":team_no"),
        (agent_get_class, ":cur_class_no", ":cur_agent"),
        (this_or_next|eq, ":class_no", grc_everyone),
        (eq, ":class_no", ":cur_class_no"),
        (agent_get_position, pos1, ":cur_agent"),
        (position_get_x, ":cur_pos_x", pos1),
        (val_add, ":total_pos_x", ":cur_pos_x"),
        (position_get_y, ":cur_pos_y", pos1),
        (val_add, ":total_pos_y", ":cur_pos_y"),
        (position_get_z, ":cur_pos_z", pos1),
        (val_add, ":total_pos_z", ":cur_pos_z"),
        (val_add, ":num_agents", 1),
      (try_end),
      (gt, ":num_agents", 1),
      (val_div, ":total_pos_x", ":num_agents"),
      (val_div, ":total_pos_y", ":num_agents"),
      (val_div, ":total_pos_z", ":num_agents"),
      (init_position, pos1),
      (position_move_x, pos1, ":total_pos_x"),
      (position_move_y, pos1, ":total_pos_y"),
      (position_move_z, pos1, ":total_pos_z"),
]),

# script_cf_turn_windmill_fans
# Input: arg1 = instance_no (none = 0)
("cf_turn_windmill_fans",
    [(store_script_param_1, ":instance_no"),
      (scene_prop_get_instance, ":windmill_fan_object", "spr_windmill_fan_turning", ":instance_no"),
      (ge, ":windmill_fan_object", 0),
      (prop_instance_get_position, pos1, ":windmill_fan_object"),
      (position_rotate_y, pos1, 10),
      (prop_instance_animate_to_position, ":windmill_fan_object", pos1, 100),
      (val_add, ":instance_no", 1),
      (call_script, "script_cf_turn_windmill_fans", ":instance_no"),
]),

# script_print_party_members
# Input: arg1 = party_no
# Output: s51 = output string. "noone" if the party is empty
("print_party_members",
    [(store_script_param_1, ":party_no"),
      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (try_begin),
          (eq, ":i_stack", 0),
          (str_store_troop_name, s51, ":stack_troop"),
        (try_end),
        (str_store_troop_name, s50, ":stack_troop"),
        (try_begin),
          (eq, ":i_stack", 1),
          (str_store_string, s51, "str_s50_and_s51"),
        (else_try),
          (gt, ":i_stack", 1),
          (str_store_string, s51, "str_s50_comma_s51"),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":num_stacks", 0),
        (str_store_string, s51, "str_noone"),
      (try_end),
]),

# script_round_value
# Input: arg1 = value
# Output: reg0 = rounded_value
("round_value",
    [ (store_script_param_1, ":value"),
      (try_begin),
        (lt, ":value", 100),
        (neq, ":value", 0),
        (val_add, ":value", 5),
        (val_div, ":value", 10),
        (val_mul, ":value", 10),
        (try_begin),
          (eq, ":value", 0),
          (assign, ":value", 5),
        (try_end),
      (else_try),
        (lt, ":value", 300),
        (val_add, ":value", 25),
        (val_div, ":value", 50),
        (val_mul, ":value", 50),
      (else_try),
        (val_add, ":value", 50),
        (val_div, ":value", 100),
        (val_mul, ":value", 100),
      (try_end),
      (assign, reg0, ":value"),
]),

# script_change_banners_and_chest
("change_banners_and_chest",
    [(party_get_slot, ":cur_leader", "$g_encountered_party", slot_town_lord),
     (try_begin),
       (ge, ":cur_leader", 0),
#normal_banner_begin
       (troop_get_slot, ":troop_banner_object", ":cur_leader", slot_troop_banner_scene_prop),
       (gt, ":troop_banner_object", 0),
       (replace_scene_props, banner_scene_props_begin, ":troop_banner_object"),
     (else_try),
       (replace_scene_props, banner_scene_props_begin, "spr_empty"),
#custom_banner_begin
#       (troop_get_slot, ":flag_spr", ":cur_leader", slot_troop_custom_banner_flag_type),
#       (ge, ":flag_spr", 0),
#       (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
#       (replace_scene_props, banner_scene_props_begin, ":flag_spr"),
#     (else_try),
#       (replace_scene_props, banner_scene_props_begin, "spr_empty"),
     (try_end),
     (try_begin),
       #(neq, ":cur_leader", "trp_player"),
       (faction_slot_eq, "$players_kingdom", slot_faction_capital, "$g_encountered_party"),
       (store_character_level, ":player_level", "trp_player"),
       (ge, ":player_level", tld_player_level_to_own_chest),
       #leave unlocked
     (else_try),
       (replace_scene_props, "spr_player_chest", "spr_locked_player_chest"),
     (try_end),
]),

# script_remove_siege_objects
# removes all objects inappropriate for siege scene (all troop/mount spawners etc)
("remove_siege_objects",[ 
	(try_for_range, ":prop", "spr_troop_guard", "spr_ZT_mb_chestnut"),
		(replace_scene_props, ":prop", "spr_empty"),
	(try_end),
	(try_for_range, ":prop", "spr_horse_riv_warhorse", "spr_spiderweb"),
		(replace_scene_props, ":prop", "spr_empty"),
	(try_end),
	(replace_scene_props, "spr_horse_player_horse", "spr_empty"),
	(try_for_range, ":prop", "spr_horse_warg_1C", "spr_sound_waterfall"),
		(replace_scene_props, ":prop", "spr_empty"),
	(try_end),
]),

# script_describe_relation_to_s63
# Input: arg1 = relation (-100 .. 100)
# Output: none
("describe_relation_to_s63",
    [(store_script_param_1, ":relation"),
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      (store_add, ":str_id", "str_relation_mnus_100",  ":str_offset"),
      (str_store_string, s63, ":str_id"),
]),

# script_describe_center_relation_to_s3
# Input: arg1 = relation (-100 .. 100)
# Output: none
# ("describe_center_relation_to_s3",
    # [(store_script_param_1, ":relation"),
      # (store_add, ":normalized_relation", ":relation", 100),
      # (val_add, ":normalized_relation", 5),
      # (store_div, ":str_offset", ":normalized_relation", 10),
      # (val_clamp, ":str_offset", 0, 20),
      # (store_add, ":str_id", "str_center_relation_mnus_100",  ":str_offset"),
      # (str_store_string, s3, ":str_id"),
# ]),

# script_center_ambiance_sounds
# to be called every two seconds. TODO for TLD centers
("center_ambiance_sounds",
   [(try_begin),
      (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
      (neg|is_currently_night),
        (party_get_slot,":sound","$g_encountered_party", slot_center_occasional_sound1_day), 
        (store_random_in_range, ":r", 0, 7),
        (ge, ":r", 5),
           (play_sound, ":sound"), 
    (try_end),
]),

# script_center_set_walker_to_type
# Input: arg1 = center_no, arg2 = walker_no, arg3 = walker_type, 
# Output: none
("center_set_walker_to_type",
   [   (store_script_param, ":center_no", 1),
       (store_script_param, ":walker_no", 2),
       (store_script_param, ":walker_type", 3),
       (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
       (party_set_slot, ":center_no", ":type_slot", ":walker_type"),
       (store_random_in_range, ":walker_dna", 0, 1000000),
       (store_add, ":dna_slot", slot_center_walker_0_dna, ":walker_no"),
       (party_set_slot, ":center_no", ":dna_slot", ":walker_dna"),
]),

# script_cf_center_get_free_walker
# Input: arg1 = center_no
# Output: reg0 = walker no (can fail)
("cf_center_get_free_walker",
   [   (store_script_param, ":center_no", 1),
       (assign, ":num_free_walkers", 0),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", walkert_default),
         (val_add, ":num_free_walkers", 1),
       (try_end),
       (gt, ":num_free_walkers", 0),
       (assign, reg0, -1),
       (store_random_in_range, ":random_rank", 0, ":num_free_walkers"),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", walkert_default),
         (val_sub, ":num_free_walkers", 1),
         (eq, ":num_free_walkers", ":random_rank"),
         (assign, reg0, ":walker_no"),
       (try_end),
]),

# script_center_remove_walker_type_from_walkers
# Input: arg1 = center_no, arg2 = walker_type, 
# Output: reg0 = 1 if comment found, 0 otherwise; s61 will contain comment string if found
("center_remove_walker_type_from_walkers",
   [   (store_script_param, ":center_no", 1),
       (store_script_param, ":walker_type", 2),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", ":walker_type"),
         (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
       (try_end),
]),

# script_init_town_walkers
("init_town_walkers",
    [(try_begin),
		(this_or_next|eq, "$town_nighttime", 0),
		(this_or_next|eq, "$current_town", "p_town_west_osgiliath"), # walkers there in osgiliaths
		(this_or_next|eq, "$current_town", "p_town_east_osgiliath"), # walkers there in osgiliaths
		(this_or_next|eq, "$current_town", "p_town_cair_andros"), # walkers there in osgiliaths
		(neq, "$g_defending_against_siege", 0), # walkers there when siege
		(try_for_range, ":walker_no", 0, num_town_walkers),
			(store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
			(try_begin),
				(eq, "$g_defending_against_siege", 0),
				(party_get_slot, ":walker_troop_id", "$current_town", ":troop_slot"),
			(else_try),
				# TODO: put military walkers when siege
				(party_get_slot, ":walker_troop_id", "$current_town", ":troop_slot"),
			(try_end),
			(gt, ":walker_troop_id", 0),
			(store_add, ":entry_no", town_walker_entries_start, ":walker_no"),
			(set_visitor, ":entry_no", ":walker_troop_id"), #entry points 32-39
		(try_end),
	(try_end),
]),

# script_cf_enter_center_location_bandit_check
("cf_enter_center_location_bandit_check",
    [ (neq, "$town_nighttime", 0),
      (party_slot_ge, "$current_town", slot_center_has_bandits, 1),
      (eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)
      (eq, "$sneaked_into_town", 0),#Skip if sneaked
      (party_get_slot, ":cur_scene", "$current_town", slot_town_center),
      (modify_visitors_at_site, ":cur_scene"),
      (reset_visitors),
      (party_get_slot, ":bandit_troop", "$current_town", slot_center_has_bandits),
      (store_character_level, ":level", "trp_player"),
      (set_jump_mission, "mt_bandits_at_night"),
        (assign, ":spawn_amount", 1),
        (assign, "$num_center_bandits", 0),
        (try_begin),
          (gt, ":level", 15),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (assign, ":spawn_amount", 2),
        (try_end),
        (val_add, "$num_center_bandits",  ":spawn_amount"),
        (set_visitors, 11, ":bandit_troop", ":spawn_amount"),
        (assign, ":spawn_amount", 1),
        (try_begin),
          (gt, ":level", 20),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (assign, ":spawn_amount", 2),
        (try_end),
        (set_visitors, 10, ":bandit_troop", ":spawn_amount"),
        (val_add, "$num_center_bandits",  ":spawn_amount"),
        (try_begin),
          (gt, ":level", 9),
          (assign, ":spawn_amount", 1),
          (try_begin),
            (gt, ":level", 25),
            (store_random_in_range, ":random_no", 0, 100),
            (lt, ":random_no", ":level"),
            (assign, ":spawn_amount", 2),
          (try_end),
          (set_visitors, 12, ":bandit_troop", ":spawn_amount"),
          (val_add, "$num_center_bandits",  ":spawn_amount"),
        (try_end),
        #(assign, "$town_entered", 1),
        (assign, "$all_doors_locked", 1),

      #(display_message, "@You have run into a trap!", 0xFFFF2222),
      (display_message, "@You are attacked by a group of goblins!", 0xFFFF2222),
      (jump_to_scene, ":cur_scene"),
      (change_screen_mission),
]),

# script_init_town_agent
("init_town_agent",
    [ (store_script_param, ":agent_no", 1),
      (agent_get_troop_id, ":troop_no", ":agent_no"),
      (set_fixed_point_multiplier, 100),
      (assign, ":stand_animation", -1),
	  
      (try_begin),
#        (this_or_next|is_between, ":troop_no", armor_merchants_begin, armor_merchants_end),
        (is_between, ":troop_no", weapon_merchants_begin, weapon_merchants_end),
        (try_begin),
          (troop_get_type, ":cur_troop_gender", ":troop_no"),
          (eq, ":cur_troop_gender", 0),
          (agent_set_animation, ":agent_no", "anim_stand_townguard"),
        (else_try),
          (agent_set_animation, ":agent_no", "anim_stand_townguard"),
        (try_end),
      (else_try),
        (this_or_next|eq, ":troop_no", "trp_gondor_lord"), # mtarini: let sire Denethor sit. GA: as well as Saruman. Them are always in capitals
        (eq, ":troop_no", "trp_isengard_lord"),
        (assign, ":stand_animation", "anim_sit_on_throne"),
      (else_try),
		(eq, ":troop_no", "trp_woodelf_lord"),(eq, "$current_town", "p_town_thranduils_halls"),
        (assign, ":stand_animation", "anim_sit_on_throne"), # GA: sitting Thranduil, but only in his halls
      (else_try),
		(eq, ":troop_no", "trp_gundabad_lord"),(eq, "$current_town", "p_town_gundabad"),
        (assign, ":stand_animation", "anim_sit_on_throne"), # GA: sitting Burza, but only in his cave
      (else_try),
		(is_between, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (assign, ":stand_animation", "anim_stand_lord"),
      (else_try),
        (is_between, ":troop_no", soldiers_begin, soldiers_end),
        (assign, ":stand_animation", "anim_stand_townguard"),
      (try_end),
      (try_begin),
        (ge, ":stand_animation", 0),
        (agent_set_stand_animation, ":agent_no", ":stand_animation"),
        (agent_set_animation, ":agent_no", ":stand_animation"),
        (store_random_in_range, ":random_no", 0, 100),
        (agent_set_animation_progress, ":agent_no", ":random_no"),
      (try_end),
]),

# script_init_town_walker_agents
("init_town_walker_agents",
    [(assign, ":num_walkers", 0),
     (try_for_agents, ":cur_agent"),
#       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
#       (is_between, ":cur_troop", walkers_begin, walkers_end),
	   (agent_get_entry_no, ":entry", ":cur_agent"),
	   (is_between, ":entry",town_walker_entries_start,40),
       (val_add, ":num_walkers", 1),
       (agent_get_position, pos1, ":cur_agent"),
       (try_for_range, ":i_e_p", 9, 40),#Entry points
         (entry_point_get_position, pos2, ":i_e_p"),
         (get_distance_between_positions, ":distance", pos1, pos2),
         (lt, ":distance", 200),
         (agent_set_slot, ":cur_agent", 0, ":i_e_p"),
       (try_end),
       (call_script, "script_set_town_walker_destination", ":cur_agent"),
     (try_end),
]),

# script_agent_get_town_walker_details
# This script assumes this is one of town walkers. 
# Input: agent_id
# Output: reg0: town_walker_type, reg1: town_walker_dna
("agent_get_town_walker_details",
    [(store_script_param, ":agent_no", 1),
     (agent_get_entry_no, ":entry_no", ":agent_no"),
     (store_sub, ":walker_no", ":entry_no", town_walker_entries_start),

     (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
     (party_get_slot, ":walker_type", "$current_town", ":type_slot"),
     (store_add, ":dna_slot", slot_center_walker_0_dna,  ":walker_no"),
     (party_get_slot, ":walker_dna", "$current_town", ":dna_slot"),
     (assign, reg0, ":walker_type"),
     (assign, reg1, ":walker_dna"),
     (assign, reg2, ":walker_no"),
]),

# script_tick_town_walkers
("tick_town_walkers",
    [(try_for_agents, ":cur_agent"),
#       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
#       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (agent_get_entry_no, ":entry", ":cur_agent"),
	   (is_between, ":entry",town_walker_entries_start,40),
       (agent_get_slot, ":target_entry_point", ":cur_agent", 0),
       (entry_point_get_position, pos1, ":target_entry_point"),
       (try_begin),
         (lt, ":target_entry_point", town_walker_entries_start),
         (init_position, pos2),
         (position_set_y, pos2, 250),
         (position_transform_position_to_parent, pos1, pos1, pos2),
       (try_end),
       (agent_get_position, pos2, ":cur_agent"),
       (get_distance_between_positions, ":distance", pos1, pos2),
       (lt, ":distance", 400),
       (assign, ":random_no", 0),
       (try_begin),
         (lt, ":target_entry_point", town_walker_entries_start),
         (store_random_in_range, ":random_no", 0, 100),
       (try_end),
       (lt, ":random_no", 20),
       (call_script, "script_set_town_walker_destination", ":cur_agent"),
     (try_end),
]),

# script_set_town_walker_destination
# Input: arg1 = agent_no
("set_town_walker_destination",
    [(store_script_param_1, ":agent_no"),
     (assign, reg0, 9),
     (assign, reg1, 10),
     (assign, reg2, 12),
     (assign, reg3, 32),
     (assign, reg4, 33),
     (assign, reg5, 34),
     (assign, reg6, 35),
     (assign, reg7, 36),
     (assign, reg8, 37),
     (assign, reg9, 38),
     (assign, reg10, 39),
     (try_for_agents, ":cur_agent"),
#       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
#       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (agent_get_entry_no, ":entry", ":cur_agent"),
	   (is_between, ":entry",town_walker_entries_start,40),
       (agent_get_slot, ":target_entry_point", ":cur_agent", 0),

       (try_begin),(eq, ":target_entry_point", 9),(assign, reg0, 0),
       (else_try) ,(eq, ":target_entry_point",10),(assign, reg1, 0),
       (else_try) ,(eq, ":target_entry_point",12),(assign, reg2, 0),
       (else_try) ,(eq, ":target_entry_point",32),(assign, reg3, 0),
       (else_try) ,(eq, ":target_entry_point",33),(assign, reg4, 0),
       (else_try) ,(eq, ":target_entry_point",34),(assign, reg5, 0),
       (else_try) ,(eq, ":target_entry_point",35),(assign, reg6, 0),
       (else_try) ,(eq, ":target_entry_point",36),(assign, reg7, 0),
       (else_try) ,(eq, ":target_entry_point",37),(assign, reg8, 0),
       (else_try) ,(eq, ":target_entry_point",38),(assign, reg9, 0),
       (else_try) ,(eq, ":target_entry_point",39),(assign,reg10, 0),
       (try_end),
     (try_end),
     (assign, ":try_limit", 100),
     (assign, ":target_entry_point", 0),
     (try_for_range, ":unused", 0, ":try_limit"),
       (shuffle_range, 0, 11),
       (gt, reg0, 0),
       (assign, ":target_entry_point", reg0),
       (assign, ":try_limit", 0),
     (try_end),
     (try_begin),
       (gt, ":target_entry_point", 0),
       (agent_set_slot, ":agent_no", 0, ":target_entry_point"),
       (entry_point_get_position, pos1, ":target_entry_point"),
       (try_begin),
         (lt, ":target_entry_point", town_walker_entries_start),
         (init_position, pos2),
         (position_set_y, pos2, 250),
         (position_transform_position_to_parent, pos1, pos1, pos2),
       (try_end),
       (agent_set_scripted_destination, ":agent_no", pos1, 0),

	   (agent_get_troop_id, ":troop_no", ":agent_no"), # orcs and dwarves walk slower
	   (troop_get_type,":try_limit",":troop_no"),
	   (try_begin),
			(neq, "$current_town", "p_town_west_osgiliath"), # guys run in osgiliaths
			(neq, "$current_town", "p_town_east_osgiliath"),
#			(neq, "$g_defending_against_siege", 0), # guys run when siege
			(try_begin),
				(this_or_next|eq,":try_limit",tf_orc),
				(eq,":try_limit",tf_dwarf),
				(store_random_in_range,reg10,2,4), (agent_set_speed_limit, ":agent_no", reg10), # orc dwarf walk slower
			(else_try),
				(store_random_in_range,reg10,3,6), (agent_set_speed_limit, ":agent_no", reg10), # humans
			(try_end),   
	   (try_end),
     (try_end),
]),

# script_siege_init_ai_and_belfry
# Output: none (required for siege mission templates)
("siege_init_ai_and_belfry",
   [(assign, "$cur_belfry_pos", 50),
    (assign, ":cur_belfry_object_pos", slot_scene_belfry_props_begin),
    (store_current_scene, ":cur_scene"),
    #Collecting belfry objects
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_a", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_a", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_b", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (assign, "$belfry_rotating_objects_begin", ":cur_belfry_object_pos"),
    (try_for_range, ":i_belfry_instance", 0, 5),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_wheel", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (assign, "$last_belfry_object_pos", ":cur_belfry_object_pos"),

    #Lifting up the platform  at the beginning
    (try_begin),
		(scene_prop_get_instance, ":belfry_object_to_rotate", "spr_belfry_platform_a", 0),
    (try_end),
    
    #Moving the belfry objects to their starting position
    (entry_point_get_position,pos1,55),
    (entry_point_get_position,pos3,50),
    (try_for_range, ":i_belfry_object_pos", slot_scene_belfry_props_begin, "$last_belfry_object_pos"),
      (assign, ":pos_no", pos_belfry_begin),
      (val_add, ":pos_no", ":i_belfry_object_pos"),
      (val_sub, ":pos_no", slot_scene_belfry_props_begin),
      (scene_get_slot, ":cur_belfry_object", ":cur_scene", ":i_belfry_object_pos"),
      (prop_instance_get_position, pos2, ":cur_belfry_object"),
      (try_begin),
        (eq, ":cur_belfry_object", ":belfry_object_to_rotate"),
        (position_rotate_x, pos2, 90),
      (try_end),
      (position_transform_position_to_local, ":pos_no", pos1, pos2),
      (position_transform_position_to_parent, pos4, pos3, ":pos_no"),
      (prop_instance_animate_to_position, ":cur_belfry_object", pos4, 1),
    (try_end),
    (assign, "$belfry_positioned", 0),
    (assign, "$belfry_num_slots_positioned", 0),
    (assign, "$belfry_num_men_pushing", 0),
]),

# script_cf_siege_move_belfry
# Output: none (required for siege mission templates)
("cf_siege_move_belfry",
   [(neq, "$last_belfry_object_pos", slot_scene_belfry_props_begin),
    (entry_point_get_position,pos1,50),
    (entry_point_get_position,pos4,55),
    (get_distance_between_positions, ":total_distance", pos4, pos1),
    (store_current_scene, ":cur_scene"),
    (scene_get_slot, ":first_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
    (prop_instance_get_position, pos2, ":first_belfry_object"),
    (entry_point_get_position,pos1,"$cur_belfry_pos"),
    (position_transform_position_to_parent, pos3, pos1, pos_belfry_begin),
    (position_transform_position_to_parent, pos5, pos4, pos_belfry_begin),
    (get_distance_between_positions, ":cur_distance", pos2, pos3),
    (get_distance_between_positions, ":distance_left", pos2, pos5),
    (try_begin),
      (le, ":cur_distance", 10),
      (val_add, "$cur_belfry_pos", 1),
      (entry_point_get_position,pos1,"$cur_belfry_pos"),
      (position_transform_position_to_parent, pos3, pos1, pos_belfry_begin),
      (get_distance_between_positions, ":cur_distance", pos2, pos3),
    (try_end),
    (neq, "$cur_belfry_pos", 50),

    (assign, ":base_speed", 20),
    (store_div, ":slow_range", ":total_distance", 60),
    (store_sub, ":distance_moved", ":total_distance", ":distance_left"),

    (try_begin),
      (lt, ":distance_moved", ":slow_range"),
      (store_mul, ":base_speed", ":distance_moved", -60),
      (val_div, ":base_speed", ":slow_range"),
      (val_add, ":base_speed", 80),
    (else_try),
      (lt, ":distance_left", ":slow_range"),
      (store_mul, ":base_speed", ":distance_left", -60),
      (val_div, ":base_speed", ":slow_range"),
      (val_add, ":base_speed", 80),
    (try_end),
    (store_mul, ":belfry_speed", ":cur_distance", ":base_speed"),
    (try_begin),
      (eq, "$belfry_num_men_pushing", 0),
      (assign, ":belfry_speed", 1000000),
    (else_try),
      (val_div, ":belfry_speed", "$belfry_num_men_pushing"),
    (try_end),

    (try_begin),
      (le, "$cur_belfry_pos", 55),
      (init_position, pos3),
      (position_rotate_x, pos3, ":distance_moved"),
      (scene_get_slot, ":base_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
      (prop_instance_get_position, pos4, ":base_belfry_object"),
      (entry_point_get_position,pos1,"$cur_belfry_pos"),
      (try_for_range, ":i_belfry_object_pos", slot_scene_belfry_props_begin, "$last_belfry_object_pos"),
        (scene_get_slot, ":cur_belfry_object", ":cur_scene", ":i_belfry_object_pos"),
        (try_begin),
          (ge, ":i_belfry_object_pos", "$belfry_rotating_objects_begin"),
          (prop_instance_get_starting_position, pos5, ":base_belfry_object"),
          (prop_instance_get_starting_position, pos6, ":cur_belfry_object"),
          (position_transform_position_to_local, pos7, pos5, pos6),
          (position_transform_position_to_parent, pos5, pos4, pos7),
          (position_transform_position_to_parent, pos6, pos5, pos3),
          (prop_instance_set_position, ":cur_belfry_object", pos6),
        (else_try),
          (assign, ":pos_no", pos_belfry_begin),
          (val_add, ":pos_no", ":i_belfry_object_pos"),
          (val_sub, ":pos_no", slot_scene_belfry_props_begin),
          (position_transform_position_to_parent, pos2, pos1, ":pos_no"),
          (prop_instance_animate_to_position, ":cur_belfry_object", pos2, ":belfry_speed"),
        (try_end),
      (try_end),
    (try_end),
    (gt, "$cur_belfry_pos", 55),
    (assign, "$belfry_positioned", 1),
]),

# script_cf_siege_rotate_belfry_platform
# Input: none
# Output: none (required for siege mission templates)
("cf_siege_rotate_belfry_platform",
   [(eq, "$belfry_positioned", 1),
    (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_a", 0),
    (prop_instance_get_position, pos1, ":belfry_object"),
    (position_rotate_x, pos1, -90),
    (prop_instance_animate_to_position, ":belfry_object", pos1, 400),
    (assign, "$belfry_positioned", 2),
]),

# script_cf_siege_assign_men_to_belfry
# Output: none (required for siege mission templates)
("cf_siege_assign_men_to_belfry",
   [(store_mission_timer_a, ":cur_seconds"),
    (neq, "$last_belfry_object_pos", slot_scene_belfry_props_begin),
    (assign, ":end_trigger", 0),
    (try_begin),
      (lt, "$belfry_positioned", 3),
      (get_player_agent_no, ":player_agent"),
      (store_current_scene, ":cur_scene"),
      (scene_get_slot, ":first_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
      (prop_instance_get_position, pos2, ":first_belfry_object"),
      (assign, ":slot_1_positioned", 0),
      (assign, ":slot_2_positioned", 0),
      (assign, ":slot_3_positioned", 0),
      (assign, ":slot_4_positioned", 0),
      (assign, ":slot_5_positioned", 0),
      (assign, ":slot_6_positioned", 0),
      (assign, "$belfry_num_slots_positioned", 0),
      (assign, "$belfry_num_men_pushing", 0),
      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (try_begin),
          (agent_get_slot, ":x_pos", ":cur_agent", slot_agent_target_x_pos),
          (neq, ":x_pos", 0),
          (agent_get_slot, ":y_pos", ":cur_agent", slot_agent_target_y_pos),
          (try_begin),
            (eq, ":x_pos", -600),
            (try_begin),
              (eq, ":y_pos", 0),
              (assign, ":slot_1_positioned", 1),
            (else_try),
              (eq, ":y_pos", -200),
              (assign, ":slot_2_positioned", 1),
            (else_try),
              (assign, ":slot_3_positioned", 1),
            (try_end),
          (else_try),
            (try_begin),
              (eq, ":y_pos", 0),
              (assign, ":slot_4_positioned", 1),
            (else_try),
              (eq, ":y_pos", -200),
              (assign, ":slot_5_positioned", 1),
            (else_try),
              (assign, ":slot_6_positioned", 1),
            (try_end),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (init_position, pos1),
          (position_move_x, pos1, ":x_pos"),
          (position_move_y, pos1, ":y_pos"),
          (init_position, pos3),
          (position_move_x, pos3, ":x_pos"),
          (position_move_y, pos3, -1000),
          (position_transform_position_to_parent, pos4, pos2, pos1),
          (position_transform_position_to_parent, pos5, pos2, pos3),
          (agent_get_position, pos6, ":cur_agent"),
          (get_distance_between_positions, ":target_distance", pos6, pos4),
          (get_distance_between_positions, ":waypoint_distance", pos6, pos5),
          (try_begin),
            (this_or_next|lt, ":target_distance", ":waypoint_distance"),
            (lt, ":waypoint_distance", 600),
            (agent_set_scripted_destination, ":cur_agent", pos4, 1),
          (else_try),
            (agent_set_scripted_destination, ":cur_agent", pos5, 1),
          (try_end),
          (try_begin),
            (le, ":target_distance", 300),
            (val_add, "$belfry_num_men_pushing", 1),
          (try_end),
        (else_try),
          (agent_get_team, ":cur_agent_team", ":cur_agent"),
          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
          (             eq, "$attacker_team_2", ":cur_agent_team"),
          (try_begin),
            (gt, ":cur_seconds", 20),
            (agent_get_position, pos1, ":cur_agent"),
            (agent_set_scripted_destination, ":cur_agent", pos1, 0),
          (else_try),
            (try_begin),
              (team_get_movement_order, ":order1", "$attacker_team", grc_infantry),
              (team_get_movement_order, ":order2", "$attacker_team", grc_cavalry),
              (team_get_movement_order, ":order3", "$attacker_team", grc_archers),
              (this_or_next|neq, ":order1", mordr_stand_ground),
              (this_or_next|neq, ":order2", mordr_stand_ground),
              (neq, ":order3", mordr_stand_ground),
              (set_show_messages, 0),
              (team_give_order, "$attacker_team", grc_everyone, mordr_stand_ground),
              (set_show_messages, 1),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
      (try_begin),
        (lt, "$belfry_num_slots_positioned", 6),
        (try_for_agents, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_get_team, ":cur_agent_team", ":cur_agent"),
          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
          (             eq, "$attacker_team_2", ":cur_agent_team"),
          (neq, ":player_agent", ":cur_agent"),
          (agent_get_class, ":agent_class", ":cur_agent"),
          (this_or_next|eq, ":agent_class", grc_infantry),
          (eq, ":agent_class", grc_cavalry),
          (agent_get_slot, ":x_pos", ":cur_agent", 1),
          (eq, ":x_pos", 0),
          (assign, ":y_pos", 0),
          (try_begin),
            (eq, ":slot_1_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_1_positioned", 1),
          (else_try),
            (eq, ":slot_2_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_2_positioned", 1),
          (else_try),
            (eq, ":slot_3_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_3_positioned", 1),
          (else_try),
            (eq, ":slot_4_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_4_positioned", 1),
          (else_try),
            (eq, ":slot_5_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_5_positioned", 1),
          (else_try),
            (eq, ":slot_6_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_6_positioned", 1),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (agent_set_slot, ":cur_agent", 1, ":x_pos"),
          (agent_set_slot, ":cur_agent", 2, ":y_pos"),
        (try_end),
      (try_end),
      (try_begin),
        (store_mission_timer_a, ":cur_timer"),
        (gt, ":cur_timer", 20),
        (lt, "$belfry_num_slots_positioned", 6),
        (try_for_agents, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_get_team, ":cur_agent_team", ":cur_agent"),
          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
          (             eq, "$attacker_team_2", ":cur_agent_team"),
          (neq, ":player_agent", ":cur_agent"),
          (agent_get_slot, ":x_pos", ":cur_agent", 1),
          (eq, ":x_pos", 0),
          (assign, ":y_pos", 0),
          (try_begin),
            (eq, ":slot_1_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_1_positioned", 1),
          (else_try),
            (eq, ":slot_2_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_2_positioned", 1),
          (else_try),
            (eq, ":slot_3_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_3_positioned", 1),
          (else_try),
            (eq, ":slot_4_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_4_positioned", 1),
          (else_try),
            (eq, ":slot_5_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_5_positioned", 1),
          (else_try),
            (eq, ":slot_6_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_6_positioned", 1),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (agent_set_slot, ":cur_agent", 1, ":x_pos"),
          (agent_set_slot, ":cur_agent", 2, ":y_pos"),
        (try_end),
      (try_end),
    (else_try),
      (assign, ":end_trigger", 1),
      (try_for_agents, ":cur_agent"),
        (agent_clear_scripted_mode, ":cur_agent"),
      (try_end),
      (set_show_messages, 0),
      (team_give_order, "$attacker_team", grc_everyone, mordr_charge),
      (set_show_messages, 1),
    (try_end),
    (eq, ":end_trigger", 1),
]),

# script_siege_move_archers_to_archer_positions
("siege_move_archers_to_archer_positions",
	[(try_for_agents, ":agent_no"),
		(agent_is_alive, ":agent_no"),
		(agent_get_class, ":agent_class", ":agent_no"),
		(agent_get_troop_id, ":agent_troop", ":agent_no"),
		(eq, ":agent_class", grc_archers),
		#       (agent_slot_eq, ":agent_no", slot_agent_is_not_reinforcement, 0),
		(try_begin),
			(agent_is_defender, ":agent_no"), # defending archers go to their respective points
			(try_begin),
				(agent_slot_eq, ":agent_no", slot_agent_target_entry_point, 0),
				(agent_get_team, ":team", ":agent_no"),
				(try_begin),(eq,":team",0),(store_random_in_range, ":random_entry_point", 50, 54), #TLD, was 40, 44
				 (else_try),(eq,":team",2),(store_random_in_range, ":random_entry_point", 54, 56), #TLD, was 40, 44
				 (else_try),               (store_random_in_range, ":random_entry_point", 56, 60), #TLD, was 40, 44
				(try_end),         
				(agent_set_slot, ":agent_no", slot_agent_target_entry_point, ":random_entry_point"),
			(try_end),
			(try_begin),
				(agent_get_position, pos0, ":agent_no"),
				(entry_point_get_position, pos1, ":random_entry_point"),
				(get_distance_between_positions, ":dist", pos0, pos1),
				(lt, ":dist", 300),
				(agent_clear_scripted_mode, ":agent_no"),
				(agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 0),
				#         (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 1),
				#         (str_store_troop_name, s1, ":agent_troop"),
				#         (assign, reg0, ":agent_no"),
				#         (display_message, "@{s1} ({reg0}) reached pos"),
			(else_try),
				(agent_get_simple_behavior, ":agent_sb", ":agent_no"),
				(agent_get_combat_state, ":agent_cs", ":agent_no"),
				(this_or_next|eq, ":agent_sb", aisb_ranged),
				(eq, ":agent_sb", aisb_go_to_pos),#scripted mode
				(eq, ":agent_cs", 7), # 7 = no visible targets (state for ranged units)
				(try_begin),
					(agent_slot_eq, ":agent_no", slot_agent_is_in_scripted_mode, 0),
					(agent_set_scripted_destination, ":agent_no", pos1, 0),
					(agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 1),
					#           (str_store_troop_name, s1, ":agent_troop"),
					#           (assign, reg0, ":agent_no"),
					#           (display_message, "@{s1} ({reg0}) moving to pos"),
				(try_end),
			(else_try),
				(try_begin),
					(agent_slot_eq, ":agent_no", slot_agent_is_in_scripted_mode, 1),
					(agent_clear_scripted_mode, ":agent_no"),
					(agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 0),
					(str_store_troop_name, s1, ":agent_troop"),
					(assign, reg0, ":agent_no"),
					#           (display_message, "@{s1} ({reg0}) seeing target or changed mode"),
				(try_end),
			(try_end),
		(else_try), # when archer is an attacker
			(agent_get_ammo,":ammo",":agent_no"),
			(try_begin),
				(lt,":ammo",2),
				(agent_clear_scripted_mode, ":agent_no"),
				(agent_ai_set_always_attack_in_melee, ":agent_no", 1),
			(try_end),
		(try_end),
	(try_end),
	 
	(set_show_messages, 0), # move attacker archers to firing positions unless target points are captured
    (try_for_range, ":slot",0,3),
		(neg|troop_slot_eq,"trp_no_troop",":slot",-1), #if flank not captured yet
		(store_mul,":atkteam",":slot",2),(val_add,":atkteam",1),
		(store_add,":random_entry_point",":slot",60),
		(entry_point_get_position, pos10, ":random_entry_point"),
		(team_give_order, ":atkteam", grc_archers, mordr_stand_ground),
		(team_set_order_position,":atkteam", grc_archers, pos10),
    (try_end),
    (set_show_messages, 1),
]),

# script_store_movement_order_name_to_s1
# Input: arg1 = team_no, arg2 = class_no
# Output: s1 = order_name
("store_movement_order_name_to_s1",
   [(store_script_param_1, ":team_no"),
    (store_script_param_2, ":class_no"),
    (team_get_movement_order, ":cur_order", ":team_no", ":class_no"),

    (try_begin),(eq, ":cur_order", mordr_hold        ),(str_store_string, s1, "@Holding"),
    (else_try) ,(eq, ":cur_order", mordr_follow      ),(str_store_string, s1, "@Following"),
    (else_try) ,(eq, ":cur_order", mordr_charge      ),(str_store_string, s1, "@Charging"),
    (else_try) ,(eq, ":cur_order", mordr_advance     ),(str_store_string, s1, "@Advancing"),
    (else_try) ,(eq, ":cur_order", mordr_fall_back   ),(str_store_string, s1, "@Falling Back"),
    (else_try) ,(eq, ":cur_order", mordr_stand_closer),(str_store_string, s1, "@Standing Closer"),
    (else_try) ,(eq, ":cur_order", mordr_spread_out  ),(str_store_string, s1, "@Spreading Out"),
    (else_try) ,(eq, ":cur_order", mordr_stand_ground),(str_store_string, s1, "@Standing"),
    (else_try) ,                                       (str_store_string, s1, "@N/A"),
    (try_end),
]),

# script_store_riding_order_name_to_s1
# Input: arg1 = team_no, arg2 = class_no
# Output: s1 = order_name
("store_riding_order_name_to_s1",
   [(store_script_param_1, ":team_no"),
    (store_script_param_2, ":class_no"),
    (team_get_riding_order, ":cur_order", ":team_no", ":class_no"),
    (try_begin),
      (eq, ":cur_order", rordr_free),
      (str_store_string, s1, "@Free"),
    (else_try),
      (eq, ":cur_order", rordr_mount),
      (str_store_string, s1, "@Mount"),
    (else_try),
      (eq, ":cur_order", rordr_dismount),
      (str_store_string, s1, "@Dismount"),
    (else_try),
      (str_store_string, s1, "@N/A"),
    (try_end),
]),

# script_store_weapon_usage_order_name_to_s1
# Input: arg1 = team_no, arg2 = class_no
# Output: s1 = order_name
("store_weapon_usage_order_name_to_s1",
   [(store_script_param_1, ":team_no"),
    (store_script_param_2, ":class_no"),
    (team_get_weapon_usage_order, ":cur_order", ":team_no", ":class_no"),
    (team_get_hold_fire_order, ":cur_hold_fire", ":team_no", ":class_no"),
    (try_begin),
      (eq, ":cur_order", wordr_use_any_weapon),
      (eq, ":cur_hold_fire", aordr_fire_at_will),
      (str_store_string, s1, "@Any Weapon"),
    (else_try),
      (eq, ":cur_order", wordr_use_blunt_weapons),
      (eq, ":cur_hold_fire", aordr_fire_at_will),
      (str_store_string, s1, "@Blunt Weapons"),
    (else_try),
      (eq, ":cur_order", wordr_use_any_weapon),
      (eq, ":cur_hold_fire", aordr_hold_your_fire),
      (str_store_string, s1, "str_hold_fire"),
    (else_try),
      (eq, ":cur_order", wordr_use_blunt_weapons),
      (eq, ":cur_hold_fire", aordr_hold_your_fire),
      (str_store_string, s1, "str_blunt_hold_fire"),
    (else_try),
      (str_store_string, s1, "@N/A"),
    (try_end),
]),

# script_team_give_order_from_order_panel
# Input: arg1 = leader_agent_no, arg2 = class_no
# Output: none
("team_give_order_from_order_panel",
   [(store_script_param_1, ":leader_agent_no"),
    (store_script_param_2, ":order"),
    (agent_get_team, ":team_no", ":leader_agent_no"),
    (set_show_messages, 0),
    (try_begin),
      (eq, "$g_formation_infantry_selected", 1),
      (team_give_order, ":team_no", grc_infantry, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_archers_selected", 1),
      (team_give_order, ":team_no", grc_archers, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_cavalry_selected", 1),
      (team_give_order, ":team_no", grc_cavalry, ":order"),
    (try_end),

    (try_begin),
      (eq, ":order", mordr_hold),
      (agent_get_position, pos1, ":leader_agent_no"),
      (try_begin),
        (eq, "$g_formation_infantry_selected", 1),
        (team_set_order_position, ":team_no", grc_infantry, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_archers_selected", 1),
        (team_set_order_position, ":team_no", grc_archers, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_cavalry_selected", 1),
        (team_set_order_position, ":team_no", grc_cavalry, pos1),
      (try_end),
    (try_end),
    
    (try_begin),
	  (eq, "$tld_option_formations", 1),
	  (call_script, "script_player_order_formations", ":order"),	#for formations
    (try_end),
    (set_show_messages, 1),
]),  

# script_update_order_panel
# Input: arg1 = team_no
("update_order_panel",
   [(store_script_param_1, ":team_no"),
    (set_fixed_point_multiplier, 1000),

    (assign, ":old_is_infantry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":team_no", grc_infantry),
      (assign, ":old_is_infantry_listening", 1),
    (try_end),
    (assign, ":old_is_archers_listening", 0),
    (try_begin),
      (class_is_listening_order, ":team_no", grc_archers),
      (assign, ":old_is_archers_listening", 1),
    (try_end),
    (assign, ":old_is_cavalry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":team_no", grc_cavalry),
      (assign, ":old_is_cavalry_listening", 1),
    (try_end),

    (call_script, "script_store_movement_order_name_to_s1", ":team_no", grc_infantry),
    (overlay_set_text, "$g_presentation_infantry_movement", s1),
    (call_script, "script_store_riding_order_name_to_s1", ":team_no", grc_infantry),
    (overlay_set_text, "$g_presentation_infantry_riding", s1),
    (call_script, "script_store_weapon_usage_order_name_to_s1", ":team_no", grc_infantry),
    (overlay_set_text, "$g_presentation_infantry_weapon_usage", s1),
    (call_script, "script_store_movement_order_name_to_s1", ":team_no", grc_archers),
    (overlay_set_text, "$g_presentation_archers_movement", s1),
    (call_script, "script_store_riding_order_name_to_s1", ":team_no", grc_archers),
    (overlay_set_text, "$g_presentation_archers_riding", s1),
    (call_script, "script_store_weapon_usage_order_name_to_s1", ":team_no", grc_archers),
    (overlay_set_text, "$g_presentation_archers_weapon_usage", s1),
    (call_script, "script_store_movement_order_name_to_s1", ":team_no", grc_cavalry),
    (overlay_set_text, "$g_presentation_cavalry_movement", s1),
    (call_script, "script_store_riding_order_name_to_s1", ":team_no", grc_cavalry),
    (overlay_set_text, "$g_presentation_cavalry_riding", s1),
    (call_script, "script_store_weapon_usage_order_name_to_s1", ":team_no", grc_cavalry),
    (overlay_set_text, "$g_presentation_cavalry_weapon_usage", s1),

    (try_begin),
      (eq, ":old_is_infantry_listening", 1),
      (eq, ":old_is_archers_listening", 1),
      (eq, ":old_is_cavalry_listening", 1),
      (team_set_order_listener, ":team_no", grc_everyone),
    (else_try),
      (eq, ":old_is_infantry_listening", 1),
      (team_set_order_listener, ":team_no", grc_infantry),
    (else_try),
      (eq, ":old_is_archers_listening", 1),
      (team_set_order_listener, ":team_no", grc_archers),
    (else_try),
      (eq, ":old_is_cavalry_listening", 1),
      (team_set_order_listener, ":team_no", grc_cavalry),
    (try_end),

    (position_set_y, pos1, 660),
    (position_set_x, pos1, 250),
    (overlay_set_position, "$g_presentation_infantry_movement", pos1),
    (position_set_x, pos1, 400),
    (overlay_set_position, "$g_presentation_infantry_riding", pos1),
    (position_set_x, pos1, 550),
    (overlay_set_position, "$g_presentation_infantry_weapon_usage", pos1),

    (position_set_y, pos1, 620),
    (position_set_x, pos1, 250),
    (overlay_set_position, "$g_presentation_archers_movement", pos1),
    (position_set_x, pos1, 400),
    (overlay_set_position, "$g_presentation_archers_riding", pos1),
    (position_set_x, pos1, 550),
    (overlay_set_position, "$g_presentation_archers_weapon_usage", pos1),

    (position_set_y, pos1, 580),
    (position_set_x, pos1, 250),
    (overlay_set_position, "$g_presentation_cavalry_movement", pos1),
    (position_set_x, pos1, 400),
    (overlay_set_position, "$g_presentation_cavalry_riding", pos1),
    (position_set_x, pos1, 550),
    (overlay_set_position, "$g_presentation_cavalry_weapon_usage", pos1),
]),

# script_update_agent_position_on_map
# Input: arg1 = agent_no, pos2 = map_size_pos
("update_agent_position_on_map",
   [(store_script_param_1, ":agent_no"),
    (agent_get_slot, ":agent_overlay", ":agent_no", slot_agent_map_overlay_id),

    (get_player_agent_no, ":player_agent"),
    (try_begin),
      (le, ":agent_overlay", 0),
      (set_fixed_point_multiplier, 1000),
      (try_begin),
        (eq, ":agent_no", ":player_agent"),
        (create_mesh_overlay, reg1, "mesh_player_dot"),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 500),
        (overlay_set_size, reg1, pos1),
      (else_try),
        (create_mesh_overlay, reg1, "mesh_white_dot"),
        (position_set_x, pos1, 200),
        (position_set_y, pos1, 200),
        (overlay_set_size, reg1, pos1),
      (try_end),
      (overlay_set_alpha, reg1, 0x88),
      (agent_set_slot, ":agent_no", slot_agent_map_overlay_id, reg1),
      (assign, ":agent_overlay", reg1),
    (try_end),

    (try_begin),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_party_id, ":agent_party", ":agent_no"),
      (try_begin),
        (eq, ":agent_party", "p_main_party"),
        (agent_get_class, ":agent_class", ":agent_no"),
        (try_begin),
          (eq, ":agent_class", grc_archers),
          (overlay_set_color, ":agent_overlay", 0x34c6e4),
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (overlay_set_color, ":agent_overlay", 0x569619),
       (else_try),
          #grc_infantry
          (overlay_set_color, ":agent_overlay", 0x8d5220),
        (try_end),
      (else_try),
        (agent_is_ally, ":agent_no"),
        (overlay_set_color, ":agent_overlay", 0x5555FF),
      (else_try),
        (overlay_set_color, ":agent_overlay", 0xFF0000),
      (try_end),
    (try_end),

    (try_begin),
      (eq, ":agent_no", ":player_agent"),
      (agent_get_look_position, pos1, ":agent_no"),
      (position_get_rotation_around_z, ":rot", pos1),
      (init_position, pos10),
      (position_rotate_z, pos10, ":rot"),
      (overlay_set_mesh_rotation, ":agent_overlay", pos10),
      (call_script, "script_convert_3d_pos_to_map_pos"),
    (else_try),
      (agent_get_position, pos1, ":agent_no"),
      (call_script, "script_convert_3d_pos_to_map_pos"),
    (try_end),
    (overlay_set_position, ":agent_overlay", pos0),
]),

# script_convert_3d_pos_to_map_pos
# Input: pos1 = 3d_pos, pos2 = map_size_pos
# Output: pos0 = map_pos
("convert_3d_pos_to_map_pos",
   [(set_fixed_point_multiplier, 1000),
    (position_transform_position_to_local, pos3, pos2, pos1),
    (position_get_x, ":agent_x_pos", pos3),
    (position_get_y, ":agent_y_pos", pos3),
    (val_div, ":agent_x_pos", "$g_battle_map_scale"),
    (val_div, ":agent_y_pos", "$g_battle_map_scale"),
    (set_fixed_point_multiplier, 1000),
    (store_sub, ":map_x", 980, "$g_battle_map_width"),
    (store_sub, ":map_y", 730, "$g_battle_map_height"),
    (val_add, ":agent_x_pos", ":map_x"),
    (val_add, ":agent_y_pos", ":map_y"),
    (position_set_x, pos0, ":agent_x_pos"),
    (position_set_y, pos0, ":agent_y_pos"),
]),

# script_update_order_flags_on_map
("update_order_flags_on_map",
   [(set_fixed_point_multiplier, 1000),
    (get_player_agent_no, ":player_agent"),
    (agent_get_team, ":player_team", ":player_agent"),

    (assign, ":old_is_infantry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_infantry),
      (assign, ":old_is_infantry_listening", 1),
    (try_end),
    (assign, ":old_is_archers_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_archers),
      (assign, ":old_is_archers_listening", 1),
    (try_end),
    (assign, ":old_is_cavalry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_cavalry),
      (assign, ":old_is_cavalry_listening", 1),
    (try_end),

    (get_scene_boundaries, pos2, pos3),

    (team_get_movement_order, ":cur_order", ":player_team", grc_infantry),
    (try_begin),
      (eq, ":cur_order", mordr_hold),
      (team_get_order_position, pos1, ":player_team", grc_infantry),
      (call_script, "script_convert_3d_pos_to_map_pos"),
      (overlay_set_alpha, "$g_battle_map_infantry_order_flag", 0xFF),
      (overlay_set_position, "$g_battle_map_infantry_order_flag", pos0),
    (else_try),
      (overlay_set_alpha, "$g_battle_map_infantry_order_flag", 0),
    (try_end),
    (team_get_movement_order, ":cur_order", ":player_team", grc_archers),
    (try_begin),
      (eq, ":cur_order", mordr_hold),
      (team_get_order_position, pos1, ":player_team", grc_archers),
      (call_script, "script_convert_3d_pos_to_map_pos"),
      (overlay_set_alpha, "$g_battle_map_archers_order_flag", 0xFF),
      (overlay_set_position, "$g_battle_map_archers_order_flag", pos0),
    (else_try),
      (overlay_set_alpha, "$g_battle_map_archers_order_flag", 0),
    (try_end),
    (team_get_movement_order, ":cur_order", ":player_team", grc_cavalry),
    (try_begin),
      (eq, ":cur_order", mordr_hold),
      (team_get_order_position, pos1, ":player_team", grc_cavalry),
      (call_script, "script_convert_3d_pos_to_map_pos"),
      (overlay_set_alpha, "$g_battle_map_cavalry_order_flag", 0xFF),
      (overlay_set_position, "$g_battle_map_cavalry_order_flag", pos0),
    (else_try),
      (overlay_set_alpha, "$g_battle_map_cavalry_order_flag", 0),
    (try_end),

    (try_begin),
      (eq, ":old_is_infantry_listening", 1),
      (eq, ":old_is_archers_listening" , 1),
      (eq, ":old_is_cavalry_listening" , 1),
      (team_set_order_listener, ":player_team", grc_everyone),
    (else_try),
      (eq, ":old_is_infantry_listening", 1),
      (team_set_order_listener, ":player_team", grc_infantry),
    (else_try),
      (eq, ":old_is_archers_listening", 1),
      (team_set_order_listener, ":player_team", grc_archers),
    (else_try),
      (eq, ":old_is_cavalry_listening", 1),
      (team_set_order_listener, ":player_team", grc_cavalry),
    (try_end),
]),

# script_update_order_panel_checked_classes
("update_order_panel_checked_classes",
   [(get_player_agent_no, ":player_agent"),
    (agent_get_team, ":player_team", ":player_agent"),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_infantry),
      (overlay_set_val, "$g_presentation_obj_4", 1),
      (assign, "$g_formation_infantry_selected", 1),
      (overlay_animate_to_alpha, "$g_presentation_obj_1", 250, 0x44),
    (else_try),
      (overlay_set_val, "$g_presentation_obj_4", 0),
      (assign, "$g_formation_infantry_selected", 0),
      (overlay_animate_to_alpha, "$g_presentation_obj_1", 250, 0),
    (try_end),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_archers),
      (overlay_set_val, "$g_presentation_obj_5", 1),
      (assign, "$g_formation_archers_selected", 1),
      (overlay_animate_to_alpha, "$g_presentation_obj_2", 250, 0x44),
    (else_try),
      (overlay_set_val, "$g_presentation_obj_5", 0),
      (assign, "$g_formation_archers_selected", 0),
      (overlay_animate_to_alpha, "$g_presentation_obj_2", 250, 0),
    (try_end),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_cavalry),
      (overlay_set_val, "$g_presentation_obj_6", 1),
      (assign, "$g_formation_cavalry_selected", 1),
      (overlay_animate_to_alpha, "$g_presentation_obj_3", 250, 0x44),
    (else_try),
      (overlay_set_val, "$g_presentation_obj_6", 0),
      (assign, "$g_formation_cavalry_selected", 0),
      (overlay_animate_to_alpha, "$g_presentation_obj_3", 250, 0),
    (try_end),
]),

# script_update_order_panel_statistics_and_map
("update_order_panel_statistics_and_map", #TODO: Call this in every battle mission template, once per second
   [(set_fixed_point_multiplier, 1000),

    (assign, ":num_us_ready_infantry", 0),
    (assign, ":num_us_ready_archers", 0),
    (assign, ":num_us_ready_cavalry", 0),

    (assign, ":num_us_wounded_infantry", 0),
    (assign, ":num_us_wounded_archers", 0),
    (assign, ":num_us_wounded_cavalry", 0),

    (assign, ":num_us_dead_infantry", 0),
    (assign, ":num_us_dead_archers", 0),
    (assign, ":num_us_dead_cavalry", 0),

    (assign, ":num_allies_ready_men", 0),
    (assign, ":num_allies_wounded_men", 0),
    (assign, ":num_allies_dead_men", 0),

    (assign, ":num_enemies_ready_men", 0),
    (assign, ":num_enemies_wounded_men", 0),
    (assign, ":num_enemies_dead_men", 0),

# CC: Modified code.
    (assign, ":num_us_routed_men", 0),
    (assign, ":num_allies_routed_men", 0),
    (assign, ":num_enemies_routed_men", 0),
# CC: Modified code ends here.

    (get_player_agent_no, ":player_agent"),
    (agent_get_team, ":player_team", ":player_agent"),

    (assign, ":old_is_infantry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_infantry),
      (assign, ":old_is_infantry_listening", 1),
    (try_end),
    (assign, ":old_is_archers_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_archers),
      (assign, ":old_is_archers_listening", 1),
    (try_end),
    (assign, ":old_is_cavalry_listening", 0),
    (try_begin),
      (class_is_listening_order, ":player_team", grc_cavalry),
      (assign, ":old_is_cavalry_listening", 1),
    (try_end),

    (get_scene_boundaries, pos2, pos3),

    (try_for_agents,":cur_agent"),

# CC: Modified to prevent routed enemies from showing as dead, wounded, or alive, and to count the routed troops.
      (try_begin),
		(eq, "$tld_option_morale", 1),
      		(agent_slot_eq, ":cur_agent", slot_agent_routed, 2),
      		(agent_get_party_id, ":agent_party", ":cur_agent"),
      		(try_begin),
        		(eq, ":agent_party", "p_main_party"),
			(val_add, ":num_us_routed_men", 1),
		(else_try),
			(agent_is_ally, ":cur_agent"),
			(val_add, ":num_allies_routed_men", 1),
		(else_try),
			(val_add, ":num_enemies_routed_men", 1),
		(try_end),
      (try_end),
      (agent_slot_eq|neg, ":cur_agent", slot_agent_routed, 2), 
# CC: Modified code ends here.

      (agent_is_human, ":cur_agent"),
      (agent_get_class, ":agent_class", ":cur_agent"),
      (agent_get_party_id, ":agent_party", ":cur_agent"),
      (agent_get_slot, ":agent_overlay", ":cur_agent", slot_agent_map_overlay_id),
      (try_begin),
        (eq, ":agent_party", "p_main_party"),
        (try_begin),
          (agent_is_alive, ":cur_agent"),
          (call_script, "script_update_agent_position_on_map", ":cur_agent"),
          (try_begin),(eq, ":agent_class", grc_archers),(val_add, ":num_us_ready_archers", 1),
           (else_try),(eq, ":agent_class", grc_cavalry),(val_add, ":num_us_ready_cavalry", 1),
           (else_try),                                  (val_add, ":num_us_ready_infantry",1),
          (try_end),
        (else_try),
          (overlay_set_alpha, ":agent_overlay", 0),
          (agent_is_wounded, ":cur_agent"),
          (try_begin),(eq, ":agent_class", grc_archers),(val_add, ":num_us_wounded_archers", 1),
           (else_try),(eq, ":agent_class", grc_cavalry),(val_add, ":num_us_wounded_cavalry", 1),
           (else_try),                                  (val_add, ":num_us_wounded_infantry",1),
          (try_end),
        (else_try),
          (try_begin),(eq, ":agent_class", grc_archers),(val_add, ":num_us_dead_archers", 1),
           (else_try),(eq, ":agent_class", grc_cavalry),(val_add, ":num_us_dead_cavalry", 1),
           (else_try),                                  (val_add, ":num_us_dead_infantry",1),
          (try_end),
        (try_end),
      (else_try),
        (agent_is_ally, ":cur_agent"),
        (try_begin),
          (agent_is_alive, ":cur_agent"),
          (call_script, "script_update_agent_position_on_map", ":cur_agent"),
          (val_add, ":num_allies_ready_men", 1),
        (else_try),
          (overlay_set_alpha, ":agent_overlay", 0),
          (agent_is_wounded, ":cur_agent"),
          (val_add, ":num_allies_wounded_men", 1),
        (else_try),
          (val_add, ":num_allies_dead_men", 1),
        (try_end),
      (else_try),
        (try_begin),
          (agent_is_alive, ":cur_agent"),
          (call_script, "script_update_agent_position_on_map", ":cur_agent"),
          (val_add, ":num_enemies_ready_men", 1),
        (else_try),
          (overlay_set_alpha, ":agent_overlay", 0),
          (agent_is_wounded, ":cur_agent"),
          (val_add, ":num_enemies_wounded_men", 1),
        (else_try),
          (val_add, ":num_enemies_dead_men", 1),
        (try_end),
      (try_end),
    (try_end),
    (assign, reg1, ":num_us_ready_infantry"),
    (assign, reg2, ":num_us_ready_archers"),
    (assign, reg3, ":num_us_ready_cavalry"),
    (store_add, ":num_us_ready_men", ":num_us_ready_infantry", ":num_us_ready_archers"),
    (val_add, ":num_us_ready_men", ":num_us_ready_cavalry"),
    (store_add, ":num_us_wounded_men", ":num_us_wounded_infantry", ":num_us_wounded_archers"),
    (val_add, ":num_us_wounded_men", ":num_us_wounded_cavalry"),
    (store_add, ":num_us_dead_men", ":num_us_dead_infantry", ":num_us_dead_archers"),
    (val_add, ":num_us_dead_men", ":num_us_dead_cavalry"),
    (assign, reg4, ":num_us_ready_men"),
    (assign, reg5, ":num_us_wounded_men"),
    (assign, reg6, ":num_us_dead_men"),
    (assign, reg7, ":num_allies_ready_men"),
    (assign, reg8, ":num_allies_wounded_men"),
    (assign, reg9, ":num_allies_dead_men"),
    (assign, reg10, ":num_enemies_ready_men"),
    (assign, reg11, ":num_enemies_wounded_men"),
    (assign, reg12, ":num_enemies_dead_men"),
    (overlay_set_text, "$g_presentation_obj_7", "@Infantry ({reg1})"),
    (overlay_set_text, "$g_presentation_obj_8", "@Archers ({reg2})"),
    (overlay_set_text, "$g_presentation_obj_9", "@Cavalry ({reg3})"),
    (overlay_set_text, "$g_battle_us_ready", "@{reg4}"),
    (overlay_set_text, "$g_battle_us_wounded", "@{reg5}"),
    (overlay_set_text, "$g_battle_us_dead", "@{reg6}"),
    (overlay_set_text, "$g_battle_allies_ready", "@{reg7}"),
    (overlay_set_text, "$g_battle_allies_wounded", "@{reg8}"),
    (overlay_set_text, "$g_battle_allies_dead", "@{reg9}"),
    (overlay_set_text, "$g_battle_enemies_ready", "@{reg10}"),
    (overlay_set_text, "$g_battle_enemies_wounded", "@{reg11}"),
    (overlay_set_text, "$g_battle_enemies_dead", "@{reg12}"),

    (try_begin),
	(eq, "$tld_option_morale", 1),
    	(assign, reg12, ":num_us_routed_men"),
    	(overlay_set_text, "$g_presentation_obj_31", "@{reg12}"),
    	(assign, reg12, ":num_allies_routed_men"),
    	(overlay_set_text, "$g_presentation_obj_32", "@{reg12}"),
    	(assign, reg12, ":num_enemies_routed_men"),
    	(overlay_set_text, "$g_presentation_obj_33", "@{reg12}"),
    (try_end),

    (assign, ":stat_position_x", 100),
    (assign, ":stat_position_y", 100),
    (val_add, ":stat_position_x", 150),
    (val_add, ":stat_position_y", 80),
    (position_set_x, pos1, ":stat_position_x"),
    (position_set_y, pos1, ":stat_position_y"),
    (overlay_set_position, "$g_battle_us_ready", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_us_wounded", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_us_dead", pos1),
    (try_begin),
	(eq, "$tld_option_morale", 1),
    	(val_add, ":stat_position_x", 150),
    	(position_set_x, pos1, ":stat_position_x"),
    	(overlay_set_position, "$g_presentation_obj_31", pos1),
    	(val_add, ":stat_position_x", -150),
    (try_end),
    (val_add, ":stat_position_x", -300),
    (val_add, ":stat_position_y", -40),
    (position_set_x, pos1, ":stat_position_x"),
    (position_set_y, pos1, ":stat_position_y"),
    (overlay_set_position, "$g_battle_allies_ready", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_allies_wounded", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_allies_dead", pos1),
    (try_begin),
	(eq, "$tld_option_morale", 1),
    	(val_add, ":stat_position_x", 150),
    	(position_set_x, pos1, ":stat_position_x"),
    	(overlay_set_position, "$g_presentation_obj_32", pos1),
    	(val_add, ":stat_position_x", -150),
    (try_end),
    (val_add, ":stat_position_x", -300),
    (val_add, ":stat_position_y", -40),
    (position_set_x, pos1, ":stat_position_x"),
    (position_set_y, pos1, ":stat_position_y"),
    (overlay_set_position, "$g_battle_enemies_ready", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_enemies_wounded", pos1),
    (val_add, ":stat_position_x", 150),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_enemies_dead", pos1),
    (try_begin),
	(eq, "$tld_option_morale", 1),
    	(val_add, ":stat_position_x", 150),
    	(position_set_x, pos1, ":stat_position_x"),
    	(overlay_set_position, "$g_presentation_obj_33", pos1),
    	(val_add, ":stat_position_x", -150),
    (try_end),

    (call_script, "script_update_order_flags_on_map"),

    (try_begin),
      (eq, ":old_is_infantry_listening", 1),
      (eq, ":old_is_archers_listening", 1),
      (eq, ":old_is_cavalry_listening", 1),
      (team_set_order_listener, ":player_team", grc_everyone),
    (else_try),
      (eq, ":old_is_infantry_listening", 1),
      (team_set_order_listener, ":player_team", grc_infantry),
    (else_try),
      (eq, ":old_is_archers_listening", 1),
      (team_set_order_listener, ":player_team", grc_archers),
    (else_try),
      (eq, ":old_is_cavalry_listening", 1),
      (team_set_order_listener, ":player_team", grc_cavalry),
    (try_end),
]),

# script_consume_food
# Input: arg1: order of the food to be consumed
# Output: none
("consume_food",
   [(store_script_param, ":selected_food", 1),
    (troop_get_inventory_capacity, ":capacity", "trp_player"),
    (try_for_range, ":cur_slot", 0, ":capacity"),
      (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
      (is_between, ":cur_item", food_begin, food_end),
      (troop_get_inventory_slot_modifier, ":item_modifier", "trp_player", ":cur_slot"),
      (neq, ":item_modifier", imod_rotten),
      (item_slot_eq, ":cur_item", slot_item_is_checked, 0),
      (item_set_slot, ":cur_item", slot_item_is_checked, 1),
      (val_sub, ":selected_food", 1),
      (lt, ":selected_food", 0),
      (assign, ":capacity", 0),
      (troop_inventory_slot_get_item_amount, ":cur_amount", "trp_player", ":cur_slot"),
      (val_sub, ":cur_amount", 1),
      (troop_inventory_slot_set_item_amount, "trp_player", ":cur_slot", ":cur_amount"),
    (try_end),
]),

# script_consume_orc_brew-- mtarini
# Input: arg1: how much
# Output: none
("consume_orc_brew",
   [(store_script_param, ":howmuch", 1),
    (troop_get_inventory_capacity, ":capacity", "trp_player"),
    (try_for_range, ":cur_slot", 0, ":capacity"),
      (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
      (eq, ":cur_item", "itm_orc_brew"),
	  (assign, ":capacity", 0), # stop loops
      (troop_inventory_slot_get_item_amount, ":cur_amount", "trp_player", ":cur_slot"),
      (val_sub, ":cur_amount", ":howmuch"),
	  (try_begin), 
	     (le, ":cur_amount", 0),
		 (display_message, "@Orc brew finished!"),
	  (try_end), 
      (troop_inventory_slot_set_item_amount, "trp_player", ":cur_slot", ":cur_amount"),
    (try_end),
]),

# script_calculate_troop_score_for_center
# Input: arg1 = troop_no, arg2 = center_no
# Output: reg0 = score
("calculate_troop_score_for_center",
   [(store_script_param, ":troop_no", 1),
    (store_script_param, ":center_no", 2),
    (assign, ":num_center_points", 1),
    (try_for_range, ":cur_center", centers_begin, centers_end),
      (party_is_active, ":cur_center"), #TLD
	  (party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
      (assign, ":center_owned", 0),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (party_slot_eq, ":cur_center", slot_town_lord, stl_reserved_for_player),
        (assign, ":center_owned", 1),
      (try_end),
      (this_or_next|party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
      (eq, ":center_owned", 1),
      (try_begin),
        (party_slot_eq, ":cur_center", slot_party_type, spt_town),
        (val_add, ":num_center_points", 4),
      (else_try),
        (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
        (val_add, ":num_center_points", 2),
      (else_try),
        (val_add, ":num_center_points", 1),
      (try_end),
    (try_end),
    (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
    (store_add, ":score", 500, ":troop_renown"),
    (val_div, ":score", ":num_center_points"),
    (store_random_in_range, ":random", 50, 100),
    (val_mul, ":score", ":random"),
    (try_begin),
      (party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":troop_no"),
      (val_mul, ":score", 3),
      (val_div, ":score", 2),
    (try_end),
    (try_begin),
      (eq, ":troop_no", "trp_player"),
      (faction_get_slot, ":faction_leader", "$players_kingdom"),
      (call_script, "script_troop_get_player_relation", ":faction_leader"),
      (assign, ":leader_relation", reg0),
      #(troop_get_slot, ":leader_relation", ":faction_leader", slot_troop_player_relation),
      (val_mul, ":leader_relation", 2),
      (val_add, ":score", ":leader_relation"),
    (try_end),
    (assign, reg0, ":score"),
]),

#script_do_party_center_trade
# INPUT: arg1 = party_no, arg2 = center_no, arg3 = percentage_change_in_center
# OUTPUT: reg0 = total_change
("do_party_center_trade",
    [ (store_script_param, ":party_no", 1),
      (store_script_param, ":center_no", 2),
      (store_script_param, ":percentage_change", 3),
      (assign, ":total_change", 0),
      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (store_add, ":cur_good_price_slot", ":cur_good", ":item_to_price_slot"),
        (party_get_slot, ":cur_merchant_price", ":party_no", ":cur_good_price_slot"),
        (party_get_slot, ":cur_center_price", ":center_no", ":cur_good_price_slot"),
        (store_sub, ":price_dif", ":cur_merchant_price", ":cur_center_price"),
        (assign, ":cur_change", ":price_dif"),
        (val_abs, ":cur_change"),
        (val_add, ":total_change", ":cur_change"),
        (val_mul, ":cur_change", ":percentage_change"),
        (val_div, ":cur_change", 100),
        (try_begin),
          (lt, ":price_dif", 0),
          (val_mul, ":cur_change", -1),
        (try_end),
        (val_add, ":cur_center_price", ":cur_change"),
        (party_set_slot, ":center_no", ":cur_good_price_slot", ":cur_center_price"),
        (party_set_slot, ":party_no", ":cur_good_price_slot", ":cur_center_price"),
      (try_end),
      (assign, reg0, ":total_change"),
]),


# script_find_cheapest_item_in_inv_of_type
#  puts in reg0 the cheapest item in an given troop invetory,  of a given type
# param1: troop id
# param2: object type MIN
# param3: object type MAX, or 0 if only one object type
("find_cheapest_item_in_inv_of_type",[
	(store_script_param_1, ":troop"),
	(store_script_param_2, ":item_type_min"),
	(store_script_param, ":item_type_max",3),
	
	(try_begin), (eq, ":item_type_max",0), 
		(store_add, ":item_type_max",":item_type_min", 1),
	(try_end),
	
	(assign, reg0, -1),
	(assign,  ":min_value", 1<<15 ),
	(troop_get_inventory_capacity, ":max", ":troop"),
	(try_for_range, ":i_slot", 0, ":max"),
        (troop_get_inventory_slot, ":item", ":troop", ":i_slot"),
        (ge, ":item", 0),
		(item_get_type,  ":type", ":item"),
		(is_between, ":type", ":item_type_min", ":item_type_max"),
		(store_item_value, ":value", ":item"),
		(lt, ":value", ":min_value"),
		(assign, ":min_value", ":value"),
		(assign, reg0, ":item"),
	(try_end),
]),

# script_start_as_one
# script to start the game as one... troop -- mtarini
# (copys that troop stats, items, factions, race, etc, into player)
("start_as_one",[
	(set_show_messages, 0),
    (store_script_param, ":troop", 1),
	(assign, "$player_current_troop_type", ":troop"),
	# copy faction
    (store_troop_faction, ":fac", ":troop"),
	(call_script, "script_player_join_faction", ":fac"),
    (troop_get_slot, "$players_subkingdom",":troop", slot_troop_subfaction), # subfaction
	# copy race
	(troop_get_type,":race",":troop"),
	(troop_get_type,":playerace","trp_player"),
    (try_begin), # if player chose woman, preserve woman. If chose orc/dwarf troop - force orc/dwarf
	   (this_or_next|neq, ":playerace", tf_female),
	   (this_or_next|is_between, ":race", tf_orc_begin,tf_orc_end),
	   (eq, ":race", tf_dwarf),
	   (troop_set_type,"trp_player",":race"),
	(try_end),
	# copy items
	(troop_clear_inventory, "trp_player"),
	(troop_get_inventory_capacity, ":inv_cap", ":troop"),
	
	# CC: Maybe fix?
	(set_show_messages, 0),
 	(try_for_range, ":item", 0, "itm_save_compartibility_item10"),
           	(troop_remove_items, "trp_player", ":item", 1),
	(try_end),
	(set_show_messages, 1),

	# option 1 add everything he has
    # (try_for_range, ":i_slot", 0, ":inv_cap"),
        # (troop_get_inventory_slot, ":item_id", ":troop", ":i_slot"),
        # (ge, ":item_id", 0),
		# (item_get_type,  ":type", ":item_id"),

		# (assign, ":problem", 0),
		# (try_begin),(eq, ":type", itp_type_body_armor), (assign, ":problem", imod_battered),
		# (else_try), (eq, ":type", itp_type_foot_armor), (assign, ":problem", imod_ragged),
		# (else_try), (eq, ":type", itp_type_head_armor), (assign, ":problem", imod_battered),
		# (else_try), (eq, ":type", itp_type_hand_armor), (assign, ":problem", imod_battered),
		# (else_try), (eq, ":type", itp_type_horse  )   , (assign, ":problem", imod_swaybacked), 
		# (else_try), (eq, ":type", itp_type_one_handed_wpn), (assign, ":problem", imod_cracked),
		# (else_try), (eq, ":type", itp_type_two_handed_wpn), (assign, ":problem", imod_cracked),
		# (else_try), (eq, ":type", itp_type_polearm), (assign, ":problem", imod_cracked),
		# (else_try), (eq, ":type", itp_type_arrows), (assign, ":problem", imod_bent), 
		# (else_try), (eq, ":type", itp_type_bolts), (assign, ":problem", imod_bent), 
		# (else_try), (eq, ":type", itp_type_shield), (assign, ":problem", imod_battered),
		# (else_try), (eq, ":type", itp_type_bow), (assign, ":problem", imod_cracked),
		# (else_try), (eq, ":type", itp_type_thrown), (assign, ":problem", imod_bent),
		# (try_end),
		# (troop_add_item, "trp_player", ":item_id", ":problem"),
	# (try_end),
	
	# option 2 for each category, add one object per category, onlg if required, and the cheapest!
	(troop_get_slot, ":flags", ":troop", slot_troop_flags),

	(try_begin),(store_and,reg13,":flags",tfg_boots),(neq,reg13,0),
		(call_script,"script_find_cheapest_item_in_inv_of_type",":troop",itp_type_foot_armor,0),(assign,":item",reg0),
		(gt,":item",0),
		(troop_add_item, "trp_player", ":item", imod_ragged),
	(try_end),

	(try_begin),(store_and,reg13,":flags",tfg_armor),(neq,reg13,0),
		(call_script,"script_find_cheapest_item_in_inv_of_type",":troop",itp_type_body_armor,0),(assign,":item",reg0),
		(gt,":item",0),
		(troop_add_item, "trp_player", ":item", imod_battered),
	(try_end),

	(try_begin),(store_and,reg13,":flags",tfg_helm),(neq,reg13,0),
		(call_script,"script_find_cheapest_item_in_inv_of_type",":troop",itp_type_head_armor,0),(assign,":item",reg0),
		(gt,":item",0),
		(troop_add_item, "trp_player", ":item", imod_battered),
	(try_end),

	(try_begin),(store_and,reg13,":flags",tfg_gloves),(neq,reg13,0),
		(call_script,"script_find_cheapest_item_in_inv_of_type",":troop",itp_type_hand_armor,0),(assign,":item",reg0),
		(gt,":item",0),
		(troop_add_item, "trp_player", ":item", imod_battered),
	(try_end),

	(try_begin),(store_and,reg13,":flags",tfg_horse),(neq,reg13,0),
		(call_script,"script_find_cheapest_item_in_inv_of_type",":troop",itp_type_horse,0),(assign,":item",reg0),
		(gt,":item",0),
		(troop_add_item, "trp_player", ":item", imod_swaybacked),
	(try_end),

	(try_begin),(store_and,reg13,":flags",tfg_shield),(neq,reg13,0),
		(call_script,"script_find_cheapest_item_in_inv_of_type",":troop",itp_type_shield,0),(assign,":item",reg0),
		(gt,":item",0),
		(troop_add_item, "trp_player", ":item", imod_battered),
	(try_end),

	(try_begin),(store_and,reg13,":flags",tfg_ranged),(neq,reg13,0),
		(call_script,"script_find_cheapest_item_in_inv_of_type",":troop",itp_type_bow,itp_type_thrown+1),(assign,":item",reg0),
		(gt,":item",0),
		(troop_add_item, "trp_player", ":item", imod_bent),

		(call_script,"script_find_cheapest_item_in_inv_of_type",":troop",itp_type_arrows,0),(assign,":item",reg0),
		(gt,":item",0),
		(troop_add_item, "trp_player", ":item", imod_bent),
	(try_end),

	# assign weapon
	(try_begin),
		(call_script,"script_find_cheapest_item_in_inv_of_type",":troop",itp_type_one_handed_wpn,itp_type_polearm+1),(assign,":item",reg0),
		(gt,":item",0),
		(assign,":problem", imod_cracked), 
		(try_begin),(eq, ":troop", "trp_dunnish_wildman"), (assign, ":item", "itm_dunland_spear"), (try_end), # exception!   Otherwie they get "orc club"
		(try_begin),(store_item_value, ":value", ":item"),(lt,":value", 50),(assign,":problem", 0), (try_end), # pity for pityful weapons!
		(troop_add_item, "trp_player", ":item", ":problem"),
	(try_end),

	# copy stats: attrib
    (try_for_range, ":i", 0, 4),
	  (store_attribute_level, ":x",":troop",":i"),
	  (troop_raise_attribute,  "trp_player",":i",-1000), 	  
	  (troop_raise_attribute,  "trp_player",":i",":x"), 
	  #(assign, reg10, ":x"),(assign, reg11, ":i"),(display_message, "@Rising skill {reg11} to {reg10}"),
	(try_end),
	# copy stats: skills
	(assign, "$disable_skill_modifiers", 1),
    (try_for_range, ":i", 0, 38 ),
	  (store_skill_level, ":x", ":i", ":troop"),
	  (troop_raise_skill,  "trp_player",":i",-1000), 	  
	  (troop_raise_skill,  "trp_player",":i",":x"), 
	(try_end),
	(assign, "$disable_skill_modifiers", 0),
	
	# copy stats: proficienceis
    (try_for_range, ":i", 0, 6),
	  (store_proficiency_level, ":x", ":i", ":troop"),
	  (troop_raise_proficiency,  "trp_player",":i",-1000), 	  
	  #(val_div, ":x", 4), # weapon proficiencies are too high!
	  #(val_min, ":x", 60),
	  (troop_raise_proficiency,  "trp_player",":i",":x"), 
	(try_end),

	(troop_equip_items, "trp_player"),
	# clear nonequipped inventory
	(try_for_range, ":i_slot", 9, ":inv_cap"), 
		(troop_set_inventory_slot, "trp_player", ":i_slot", -1),
	(try_end),
	
	# clear any non-ranged weapon except one
	(store_random_in_range, ":die_roll", 0, 2),
	(assign, ":weapon_found",0),
	(try_for_range, ":i", 0, 9), 
		(try_begin),(lt, ":die_roll", 1), (store_sub, ":j", 8, ":i"),(else_try), (assign,":j",":i"),(end_try), #50% chance of reverse order
		(troop_get_inventory_slot, ":item_id", "trp_player", ":j"),
		(ge, ":item_id", 0),
		(item_get_type,  ":type", ":item_id"),
		(this_or_next|eq, ":type", itp_type_one_handed_wpn), 
		(this_or_next|eq, ":type", itp_type_two_handed_wpn), 
		(eq, ":type", itp_type_polearm), 
		(try_begin),(eq,":weapon_found",1),(troop_set_inventory_slot, "trp_player", ":j", -1),(try_end),
		(assign, ":weapon_found",1),
	(try_end),
	
	# give appropriate food for race/faction
	(call_script, "script_get_food_of_race_and_faction", ":race", ":fac"),
	(troop_add_item, "trp_player", reg0 ),
	
]),

#script_player_join_faction
# INPUT: arg1 = faction_no
("player_join_faction",
    [ (set_show_messages,0),
      (store_script_param, ":faction_no", 1),
      (assign,"$players_kingdom",":faction_no"),
      (faction_set_slot, "fac_player_supporters_faction", slot_faction_ai_state, sfai_default),
#      (assign, "$players_oath_renounced_against_kingdom", 0),
      (try_for_range,":other_kingdom",kingdoms_begin,kingdoms_end),
        (faction_slot_eq, ":other_kingdom", slot_faction_state, sfs_active),
        (neq, ":other_kingdom", "fac_player_supporters_faction"),
        (try_begin),
          (neq, ":other_kingdom", ":faction_no"),
          (store_relation, ":other_kingdom_reln", ":other_kingdom", ":faction_no"),
        (else_try),
          (store_relation, ":other_kingdom_reln", "fac_player_supporters_faction", ":other_kingdom"),
          (val_max, ":other_kingdom_reln", 50), #TLD
        (try_end),
        (call_script, "script_set_player_relation_with_faction", ":other_kingdom", ":other_kingdom_reln"),
      (try_end),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
		(party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
        #Give center to kingdom if player is the owner
        (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
        (party_set_faction, ":cur_center", ":faction_no"),
      (try_end),
      (try_for_range, ":quest_no", lord_quests_begin, lord_quests_end),
        (check_quest_active, ":quest_no"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
        (store_relation, ":quest_giver_faction_relation", "fac_player_supporters_faction", ":quest_giver_faction"),
        (lt, ":quest_giver_faction_relation", 0),
        (call_script, "script_abort_quest", ":quest_no", 0),
      (try_end),
      (try_begin),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
        (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
      (try_end),
      (call_script, "script_store_average_center_value_per_faction"),
      (call_script, "script_update_all_notes"),
      (assign, "$g_recalculate_ais", 1),
	  (set_show_messages,1),
]),

#script_agent_reassign_team
# INPUT: arg1 = agent_no
("agent_reassign_team",
    [ (store_script_param, ":agent_no", 1),
      (get_player_agent_no, ":player_agent"),
      (try_begin),
        (ge, ":player_agent", 0),
        (agent_is_human, ":agent_no"),
        (agent_is_ally, ":agent_no"),
        (agent_get_party_id, ":party_no", ":agent_no"),
		(gt, ":party_no",  -1),
        (neq, ":party_no", "p_main_party"),
        (assign, ":continue", 1),
        (store_faction_of_party, ":party_faction", ":party_no"),
        (try_begin),
          (eq, ":party_faction", "$players_kingdom"),
          (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
          (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
          (assign, ":continue", 0),
        (else_try),
          (party_stack_get_troop_id, ":leader_troop_id", ":party_no", 0),
          (neg|is_between, ":leader_troop_id", kingdom_heroes_begin, kingdom_heroes_end),
          (assign, ":continue", 0),
        (try_end),
        (eq, ":continue", 1),
        (agent_get_team, ":player_team", ":player_agent"),
        (val_add, ":player_team", 2),
        (agent_set_team, ":agent_no", ":player_team"),
      (try_end),
]),

#script_start_quest
# INPUT: arg1 = quest_no, arg2 = giver_troop_no, s2 = description_text
("start_quest",
    [(store_script_param, ":quest_no", 1),
     (store_script_param, ":giver_troop_no", 2),
     (try_begin),
       (is_between, ":giver_troop_no", kingdom_heroes_begin, kingdom_heroes_end),
       (str_store_troop_name_link, s62, ":giver_troop_no"),
     (else_try),
       (str_store_troop_name, s62, ":giver_troop_no"),
     (try_end),
     (str_store_string, s63, "@Given by: {s62}"),
     (store_current_hours, ":cur_hours"),
     (str_store_date, s60, ":cur_hours"),
     (str_store_string, s60, "@Given on: {s60}"),
     (add_quest_note_from_sreg, ":quest_no", 0, s60, 0),
     (add_quest_note_from_sreg, ":quest_no", 1, s63, 0),
     (add_quest_note_from_sreg, ":quest_no", 2, s2, 0),

     (try_begin),
       (quest_slot_ge, ":quest_no", slot_quest_expiration_days, 1),
       (quest_get_slot, reg0, ":quest_no", slot_quest_expiration_days),
       (add_quest_note_from_sreg, ":quest_no", 7, "@You have {reg0} days to finish this quest.", 0),
     (try_end),

     #Adding dont_give_again_for_days value
     (try_begin),
       (quest_slot_ge, ":quest_no", slot_quest_dont_give_again_period, 1),
       (quest_get_slot, ":dont_give_again_period", ":quest_no", slot_quest_dont_give_again_period),
       (quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days, ":dont_give_again_period"),
     (try_end),
     (start_quest, ":quest_no", ":giver_troop_no"),
     (display_message, "str_quest_log_updated"),
]),
#script_conclude_quest
# INPUT: arg1 = quest_no
("conclude_quest",
    [(store_script_param, ":quest_no", 1),
     (conclude_quest, ":quest_no"),
     (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
     (str_store_troop_name, s59, ":quest_giver_troop"),
     (add_quest_note_from_sreg, ":quest_no", 7, "@This quest has been concluded. Talk to {s59} to finish it.", 0),
]),
#script_succeed_quest
# INPUT: arg1 = quest_no
("succeed_quest",
    [(store_script_param, ":quest_no", 1),
     (succeed_quest, ":quest_no"),
     (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
     (str_store_troop_name, s59, ":quest_giver_troop"),
     (add_quest_note_from_sreg, ":quest_no", 7, "@This quest has been successfully completed. Talk to {s59} to claim your reward.", 0),
]),
#script_fail_quest
# INPUT: arg1 = quest_no
("fail_quest",
    [(store_script_param, ":quest_no", 1),
     (fail_quest, ":quest_no"),
     (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
     (str_store_troop_name, s59, ":quest_giver_troop"),
     (add_quest_note_from_sreg, ":quest_no", 7, "@This quest has failed. Talk to {s59} to explain the situation.", 0),
]),
#script_report_quest_troop_positions
# INPUT: arg1 = quest_no, arg2 = troop_no, arg3 = note_index
("report_quest_troop_positions",
    [(store_script_param, ":quest_no", 1),
     (store_script_param, ":troop_no", 2),
     (store_script_param, ":note_index", 3),
     (call_script, "script_get_information_about_troops_position", ":troop_no", 1),
     (str_store_string, s5, "@At the time quest was given:^{s1}"),
     (add_quest_note_from_sreg, ":quest_no", ":note_index", s5, 1),
     (call_script, "script_update_troop_location_notes", ":troop_no", 1),
]),
#script_end_quest
# INPUT: arg1 = quest_no
("end_quest",
    [(store_script_param, ":quest_no", 1),
     (str_clear, s1),
     (add_quest_note_from_sreg, ":quest_no", 0, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 1, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 2, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 4, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 7, s1, 0),
     (try_begin),
       (neg|check_quest_failed, ":quest_no"),
       (val_add, "$g_total_quests_completed", 1),
     (try_end),
     (complete_quest, ":quest_no"),
     (try_begin),
       (is_between, ":quest_no", mayor_quests_begin, mayor_quests_end),
       (assign, "$merchant_quest_last_offerer", -1),
       (assign, "$merchant_offered_quest", -1),
     (try_end),
]),
#script_cancel_quest
# INPUT: arg1 = quest_no
("cancel_quest",
    [(store_script_param, ":quest_no", 1),
     (str_clear, s1),
     (add_quest_note_from_sreg, ":quest_no", 0, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 1, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 2, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 4, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 7, s1, 0),
     (cancel_quest, ":quest_no"),
     (try_begin),
       (is_between, ":quest_no", mayor_quests_begin, mayor_quests_end),
       (assign, "$merchant_quest_last_offerer", -1),
       (assign, "$merchant_offered_quest", -1),
     (try_end),
]),

#script_update_faction_notes
# INPUT: faction_no
("update_faction_notes",
    [(store_script_param, ":faction_no", 1),
     (try_begin),
       (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
       (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
       (str_store_faction_name, s5, ":faction_no"),
       (str_store_troop_name_link, s6, ":faction_leader"),
       (assign, ":num_centers", 0),
       (str_store_string, s8, "str_empty_string"),
       (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
         (party_is_active, ":cur_center"), #TLD
		 (party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
         (store_faction_of_party, ":center_faction", ":cur_center"),
         (eq, ":center_faction", ":faction_no"),
         (try_begin),
           (eq, ":num_centers", 0),
           (str_store_party_name_link, s8, ":cur_center"),
         (else_try),
           (eq, ":num_centers", 1),
           (str_store_party_name_link, s7, ":cur_center"),
           (str_store_string, s8, "@{s7} and {s8}"),
         (else_try),
           (str_store_party_name_link, s7, ":cur_center"),
           (str_store_string, s8, "@{s7}, {s8}"),
         (try_end),
         (val_add, ":num_centers", 1),
       (try_end),
       (assign, ":num_members", 0),
       (str_store_string, s10, "@noone"),
       (try_for_range_backwards, ":loop_var", "trp_kingdom_heroes_including_player_begin", kingdom_heroes_end),
         (assign, ":cur_troop", ":loop_var"),
         (try_begin),
           (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
           (assign, ":cur_troop", "trp_player"),
           (assign, ":troop_faction", "$players_kingdom"),
         (else_try),
           (store_troop_faction, ":troop_faction", ":cur_troop"),
         (try_end),
         (eq, ":troop_faction", ":faction_no"),
         (neq, ":cur_troop", ":faction_leader"),
         (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
         (try_begin),
           (eq, ":num_members", 0),
           (str_store_troop_name_link, s10, ":cur_troop"),
         (else_try),
           (eq, ":num_members", 1),
           (str_store_troop_name_link, s9, ":cur_troop"),
           (str_store_string, s10, "@{s9} and {s10}"),
         (else_try),
           (str_store_troop_name_link, s9, ":cur_troop"),
           (str_store_string, s10, "@{s9}, {s10}"),
         (try_end),
         (val_add, ":num_members", 1),
       (try_end),
       (str_store_string, s12, "@no one"),
       (assign, ":num_enemies", 0),
       (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
         (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
         (store_relation, ":cur_relation", ":cur_faction", ":faction_no"),
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
       (try_end),
	# Maybe we could add more information about the factions? Like where they come from. -CC
       (add_faction_note_from_sreg, ":faction_no", 0, "@{s5} is ruled by {s6}.^It controls {s8}.^Its commanders are {s10}.^{s5} is at war with {s12}.", 0),
     (else_try),
       (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_defeated),
       (str_store_faction_name, s5, ":faction_no"),
       (add_faction_note_from_sreg, ":faction_no", 0, "@{s5} has been defeated!", 0),
       (str_clear, s1),
       (add_faction_note_from_sreg, ":faction_no", 1, s1, 0),
     (else_try),
       (str_clear, s1),
       (add_faction_note_from_sreg, ":faction_no", 0, s1, 0),
       (add_faction_note_from_sreg, ":faction_no", 1, s1, 0),
     (try_end),
#MV: show faction leader banner instead of (non-existent) faction pic
#     (try_begin),
#       (is_between, ":faction_no", "fac_gondor", kingdoms_end), #Excluding player kingdom
#       (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh"),
#     (else_try),
       (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh_banner"),
#     (try_end),
]),

#script_update_faction_traveler_notes
# INPUT: faction_no
("update_faction_traveler_notes",
    [(store_script_param, ":faction_no", 1),
     (assign, ":total_men", 0),
     (try_for_parties, ":cur_party"),
       (store_faction_of_party, ":center_faction", ":cur_party"),
       (eq, ":center_faction", ":faction_no"),
       (party_get_num_companions, ":num_men", ":cur_party"),
       (val_add, ":total_men", ":num_men"),
     (try_end),
     (str_store_faction_name, s5, ":faction_no"),
     (assign, reg1, ":total_men"),
     (add_faction_note_from_sreg, ":faction_no", 1, "@{s5} has a strength of {reg1} men in total.", 1),
]),

#script_update_troop_notes
# INPUT: troop_no
("update_troop_notes",
    [(store_script_param, ":troop_no", 1),
     (str_store_troop_name, s54, ":troop_no"),
     (try_begin),
       (eq, ":troop_no", "trp_player"),
       # (this_or_next|eq, 0, 1), # "$player_has_homage" is always 0 in TLD
       # (             eq, "$players_kingdom", "fac_player_supporters_faction"),
       (assign, ":troop_faction", "$players_kingdom"),
     (else_try),
       (store_troop_faction, ":troop_faction", ":troop_no"),
     (try_end),
     (try_begin),
       (neq, ":troop_no", "trp_player"),
       (neg|is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
       (str_clear, s54),
       (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
       (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
       (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
     (else_try),
       (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
       (str_store_troop_name_link, s55, ":faction_leader"),
       (str_store_faction_name_link, s56, ":troop_faction"),
       (assign, reg4, 0),
       (assign, reg6, 0),
       (try_begin),
         (eq, ":troop_faction", "fac_player_faction"),
         (assign, reg6, 1),
       (else_try),
         (eq, ":faction_leader", ":troop_no"),
         (assign, reg4, 1),
       (try_end),
       (assign, ":num_centers", 0),
       (str_store_string, s58, "@no holdings"),
       (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
         (party_is_active, ":cur_center"), #TLD
		 (party_slot_eq, ":cur_center", slot_center_destroyed, 0), # TLD
         (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
         (try_begin),
           (eq, ":num_centers", 0),
           (str_store_party_name_link, s58, ":cur_center"),
         (else_try),
           (eq, ":num_centers", 1),
           (str_store_party_name_link, s57, ":cur_center"),
           (str_store_string, s58, "@{s57} and {s58}"),
         (else_try),
           (str_store_party_name_link, s57, ":cur_center"),
           (str_store_string, s58, "@{s57}, {s58}"),
         (try_end),
         (val_add, ":num_centers", 1),
       (try_end),
       (troop_get_type, reg3, ":troop_no"),
       (try_begin),
         (gt, reg3, 1), #MV: non-humans are male
         (assign, reg3, 0),
       (try_end),
#       (troop_get_slot, reg5, ":troop_no", slot_troop_renown),
       (str_clear, s59),
       (try_begin),
#         (troop_get_slot, ":relation", ":troop_no", slot_troop_player_relation),
         (call_script, "script_troop_get_player_relation", ":troop_no"),
         (assign, ":relation", reg0),
         (store_add, ":normalized_relation", ":relation", 100),
         (val_add, ":normalized_relation", 5),
         (store_div, ":str_offset", ":normalized_relation", 10),
         (val_clamp, ":str_offset", 0, 20),
         (store_add, ":str_id", "str_relation_mnus_100_ns",  ":str_offset"),
         (neq, ":str_id", "str_relation_plus_0_ns"),
         (str_store_string, s60, "@{reg3?She:He}"),
         (str_store_string, s59, ":str_id"),
         (str_store_string, s59, "@^{s59}"),
       (try_end),
       (assign, reg9, ":num_centers"),
       (assign, reg10, 0), #alive
       (try_begin),
         (troop_slot_eq, ":troop_no", slot_troop_wound_mask, wound_death), #dead
         (assign, reg10, 1),
       (try_end),
       (add_troop_note_from_sreg, ":troop_no", 0, "@{reg6?:{reg4?{s54} is the ruler of {s56}.^:{s54} serves {s55} of {s56}.^}}{reg9?{reg3?She:He} is the {reg3?lady:lord} of {s58}.:}{s59}{reg10?^{reg3?She:He} died on the battlefield!:}", 0),
#       (add_troop_note_from_sreg, ":troop_no", 0, "@{reg6?:{reg4?{s54} is the ruler of {s56}.^:{s54} serves {s55} of {s56}.^}}Renown: {reg5}.{reg9?^{reg3?She:He} is the {reg3?lady:lord} of {s58}.:}{s59}", 0),
       (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
     (try_end),
]),

#script_update_troop_location_notes
# INPUT: troop_no
("update_troop_location_notes",
    [(store_script_param, ":troop_no", 1),
     (store_script_param, ":see_or_hear", 2),
     (call_script, "script_get_information_about_troops_position", ":troop_no", 1),
     (try_begin),
       (neq, reg0, 0),
       (troop_get_type, reg1, ":troop_no"),
       (try_begin),
         (gt, reg1, 1), #MV: non-humans are male
         (assign, reg1, 0),
       (try_end),
       (try_begin),
         (eq, ":see_or_hear", 0),
         (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you saw {reg1?her:him}, {s1}", 1),
       (else_try),
         (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you heard about {reg1?her:him}, {s1}", 1),
       (try_end),
     (try_end),
]),

#script_update_center_notes
# INPUT: center_no
("update_center_notes",
    [(store_script_param, ":center_no", 1),

     (party_get_slot, ":lord_troop", ":center_no", slot_town_lord),
     (try_begin),
       (ge, ":lord_troop", 0),
       (store_troop_faction, ":lord_faction", ":lord_troop"),
       (faction_slot_eq, ":lord_faction", slot_faction_state, sfs_active), #TLD
       (str_store_troop_name_link, s1, ":lord_troop"),
       (try_begin),
         (eq, ":lord_troop", "trp_player"),
         (gt, "$players_kingdom", 0),
         (str_store_faction_name_link, s2, "$players_kingdom"),
       (else_try),
         (str_store_faction_name_link, s2, ":lord_faction"),
       (try_end),
       (str_store_party_name, s50, ":center_no"),
       (try_begin),
         (party_slot_eq, ":center_no", slot_party_type, spt_town),
         (str_store_string, s51, "@The {s50}"), # "town of" stricken out
       # (else_try),
         # (party_slot_eq, ":center_no", slot_party_type, spt_village),
         # (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
         # (str_store_party_name_link, s52, ":bound_center"),
         # (str_store_string, s51, "@The village of {s50} near {s52}"),
       (else_try),
         (str_store_string, s51, "@{s50}"),
       (try_end),
       (str_store_string, s2, "@{s50} belongs to {s1} of {s2}.^"), #TLD: was s51
     (else_try),
       (str_clear, s2),
     (try_end),

     (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
     (try_begin), #TLD: if party is disabled, clear all text so there will be no wiki entry
       (this_or_next|party_slot_eq, ":center_no", slot_center_destroyed, 1), # TLD
	   (neg|party_is_active, ":center_no"),
       (str_clear, s2),
     (try_end),
     (add_party_note_from_sreg, ":center_no", 0, "@{s2}", 0), #TLD: no prosperity
     #(add_party_note_from_sreg, ":center_no", 0, "@{s2}Its prosperity is: {s50}", 0),
     (add_party_note_tableau_mesh, ":center_no", "tableau_center_note_mesh"),
]),

#script_update_center_recon_notes
# INPUT: center_no
# OUTPUT: none
("update_center_recon_notes",
    [(store_script_param, ":center_no", 1),
     (try_begin),
       (is_between, ":center_no", centers_begin, centers_end),
       (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
       (call_script, "script_center_get_food_consumption", ":center_no"),
       (assign, ":food_consumption", reg0),
       (store_div, reg6, ":center_food_store", ":food_consumption"),
       (party_collect_attachments_to_party, ":center_no", "p_collective_ally"),
       (party_get_num_companions, reg5, "p_collective_ally"),
       (add_party_note_from_sreg, ":center_no", 1, "@Current garrison consists of {reg5} men.^Has food stock for {reg6} days.", 1),
     (try_end),
]),

#script_update_all_notes
("update_all_notes",
    [ (call_script, "script_update_troop_notes", "trp_player"),
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (call_script, "script_update_troop_notes", ":troop_no"),
      (try_end),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (call_script, "script_update_center_notes", ":center_no"),
      (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_update_faction_notes", ":faction_no"),
      (try_end),
]),


#script_shield_item_set_banner
# INPUT: agent_no
# OUTPUT: none
("shield_item_set_banner",
    [  (store_script_param, ":tableau_no",1),
       (store_script_param, ":agent_no", 2),
       (store_script_param, ":troop_no", 3),
       (assign, ":banner_troop", -1),
       (assign, ":banner_mesh", "mesh_banners_default_b"),
       (try_begin),
         (lt, ":agent_no", 0),
         (try_begin),
           (ge, ":troop_no", 0),
           (this_or_next|troop_slot_ge, ":troop_no", slot_troop_banner_scene_prop, 1),
           (             eq, ":troop_no", "trp_player"),
           (assign, ":banner_troop", ":troop_no"),
         (else_try),
           (is_between, ":troop_no", companions_begin, companions_end),
           (assign, ":banner_troop", "trp_player"),
         (else_try),
           (assign, ":banner_mesh", "mesh_banners_default_a"),
         (try_end),
       (else_try),
         (agent_get_troop_id, ":troop_id", ":agent_no"),
         (this_or_next|troop_slot_ge,  ":troop_id", slot_troop_banner_scene_prop, 1),
         (             eq, ":troop_no", "trp_player"),
         (assign, ":banner_troop", ":troop_id"),
       (else_try),
         (agent_get_party_id, ":agent_party", ":agent_no"),
         (try_begin),
           (lt, ":agent_party", 0),
           (is_between, ":troop_id", companions_begin, companions_end),
           (main_party_has_troop, ":troop_id"),
           (assign, ":agent_party", "p_main_party"),
         (try_end),
         (ge, ":agent_party", 0),
         (party_get_template_id, ":party_template", ":agent_party"),
         (try_begin),
           (eq, ":party_template", "pt_deserters"),
           (assign, ":banner_mesh", "mesh_banners_default_c"),
         (else_try),
           (is_between, ":agent_party", centers_begin, centers_end),
           (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
           (ge, ":town_lord", 0),
           (assign, ":banner_troop", ":town_lord"),
         (else_try),
           (this_or_next|party_slot_eq, ":agent_party", slot_party_type, spt_kingdom_hero_party),
           (             eq, ":agent_party", "p_main_party"),
           (party_get_num_companion_stacks, ":num_stacks", ":agent_party"),
           (gt, ":num_stacks", 0),
           (party_stack_get_troop_id, ":leader_troop_id", ":agent_party", 0),
           (this_or_next|troop_slot_ge,  ":leader_troop_id", slot_troop_banner_scene_prop, 1),
           (             eq, ":leader_troop_id", "trp_player"),
           (assign, ":banner_troop", ":leader_troop_id"),
         (try_end),
       (else_try), #Check if we are in a tavern
         (eq, "$talk_context", tc_tavern_talk),
         (neq, ":troop_no", "trp_player"),
         (assign, ":banner_mesh", "mesh_banners_default_d"),
       (else_try), #can't find party, this can be a town guard
         (neq, ":troop_no", "trp_player"),
         (is_between, "$g_encountered_party", centers_begin, centers_end),
         (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
         (ge, ":town_lord", 0),
         (assign, ":banner_troop", ":town_lord"),
       (try_end),
	   
       (try_begin),
         (ge, ":banner_troop", 0),
         (try_begin),
           (neg|troop_slot_ge, ":banner_troop", slot_troop_banner_scene_prop, 1),
           (assign, ":banner_mesh", "mesh_banners_default_b"),
         (else_try), 
           (troop_get_slot, ":banner_spr", ":banner_troop", slot_troop_banner_scene_prop),
           (store_add, ":banner_scene_props_end", banner_scene_props_end_minus_one, 1),
           (is_between, ":banner_spr", banner_scene_props_begin, ":banner_scene_props_end"),
           (val_sub, ":banner_spr", banner_scene_props_begin),
           (store_add, ":banner_mesh", ":banner_spr", arms_meshes_begin),
         (try_end),
       (try_end),
       (cur_item_set_tableau_material, ":tableau_no", ":banner_mesh"),
]),

#script_add_troop_to_cur_tableau
# INPUT: troop_no
("add_troop_to_cur_tableau",[
	(store_script_param, ":troop_no",1),
	(set_fixed_point_multiplier, 100),
	(assign, ":banner_mesh", -1),
	(troop_get_slot, ":banner_spr", ":troop_no", slot_troop_banner_scene_prop),
	(store_add, ":banner_scene_props_end", banner_scene_props_end_minus_one, 1),
	(try_begin),
		(is_between, ":banner_spr", banner_scene_props_begin, ":banner_scene_props_end"),
		(val_sub, ":banner_spr", banner_scene_props_begin),
		(store_add, ":banner_mesh", ":banner_spr", banner_meshes_begin),
	(try_end),

	(cur_tableau_clear_override_items),

	(try_begin),#TLD: mouth of sauron keeps his hood
		(eq,":troop_no","trp_mordor_lord"),
		(cur_tableau_set_override_flags, af_override_weapons),
	(else_try),
		(cur_tableau_set_override_flags, af_override_head|af_override_weapons),
	(try_end),

	(init_position, pos2),
	(cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),

	(init_position, pos5),
	(troop_get_type,":type",":troop_no"), # TLD: get dwarves and orcs on screen in notes
	(try_begin),
		(this_or_next|eq,":type",tf_dwarf),(eq,":type",tf_orc),
		(assign, ":eye_height", 142),
	(else_try),
		(assign, ":eye_height", 162),
	(try_end),
	(store_mul, ":camera_distance", ":troop_no", 87323),
	#       (val_mod, ":camera_distance", 5),
	(assign, ":camera_distance", 139),
	(store_mul, ":camera_yaw", ":troop_no", 124337),
	(val_mod, ":camera_yaw", 50),
	(val_add, ":camera_yaw", -25),
	(store_mul, ":camera_pitch", ":troop_no", 98123),
	(val_mod, ":camera_pitch", 20),
	(val_add, ":camera_pitch", -14),
	(assign, ":animation", anim_stand_man),

	##       (troop_get_inventory_slot, ":horse_item", ":troop_no", ek_horse),
	##       (try_begin),
	##         (gt, ":horse_item", 0),
	##         (assign, ":eye_height", 210),
	##         (cur_tableau_add_horse, ":horse_item", pos2, anim_horse_stand, 0),
	##         (assign, ":animation", anim_ride_0),
	##         (position_set_z, pos5, 125),
	##         (try_begin),
	##           (is_between, ":camera_yaw", -10, 10), #make sure horse head doesn't obstruct face.
	##           (val_min, ":camera_pitch", -5),
	##         (try_end),
	##       (try_end),
	(position_set_z, pos5, ":eye_height"),
	# camera looks towards -z axis
	(position_rotate_x, pos5, -90),
	(position_rotate_z, pos5, 180),
	# now apply yaw and pitch
	(position_rotate_y, pos5, ":camera_yaw"),
	(position_rotate_x, pos5, ":camera_pitch"),
	(position_move_z, pos5, ":camera_distance", 0),
	(position_move_x, pos5, 5, 0),

	(try_begin),
		(ge, ":banner_mesh", 0),

		(init_position, pos1),
		(position_set_z, pos1, -1500),
		(position_set_x, pos1, 265),
		(position_set_y, pos1, 400),
		(position_transform_position_to_parent, pos3, pos5, pos1),
		(cur_tableau_add_mesh, ":banner_mesh", pos3, 400, 0),
	(try_end),
	(cur_tableau_add_troop, ":troop_no", pos2, ":animation" , 0),

	(cur_tableau_set_camera_position, pos5),

	(copy_position, pos8, pos5),
	(position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
	(position_rotate_z, pos8, 30), 
	(position_rotate_x, pos8, -60), 
	(cur_tableau_add_sun_light, pos8, 175,150,125),
]),

#script_add_troop_to_cur_tableau_for_character
# INPUT: troop_no
("add_troop_to_cur_tableau_for_character",
    [  (store_script_param, ":troop_no",1),

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       (cur_tableau_set_override_flags, af_override_fullhelm),
##       (cur_tableau_set_override_flags, af_override_head|af_override_weapons),
       
       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 4, 8, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 150),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 360),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),
       
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
]),

#script_add_troop_to_cur_tableau_for_inventory
# INPUT: troop_no
("add_troop_to_cur_tableau_for_inventory",
    [  (store_script_param, ":troop_no",1),
       (store_mod, ":side", ":troop_no", 4), #side flag is inside troop_no value
       (val_div, ":troop_no", 4), #removing the flag bit
       (val_mul, ":side", 90), #to degrees
		
		(try_begin), # TLD equipment appropriateness check
			(eq, "$tld_option_crossdressing", 0),
			(this_or_next|eq, ":troop_no", "trp_player"),
			(is_between, ":troop_no", companions_begin, companions_end),
			(call_script, "script_check_equipped_items", ":troop_no"),
		(try_end),
       
	   (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       
       (init_position, pos2),
       (position_rotate_z, pos2, ":side"),
       (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 380),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),
       
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
]),

#script_add_troop_to_cur_tableau_for_party
# INPUT: troop_no
("add_troop_to_cur_tableau_for_party",
    [  (store_script_param, ":troop_no",1),
       (store_mod, ":hide_weapons", ":troop_no", 2), #hide_weapons flag is inside troop_no value
       (val_div, ":troop_no", 2), #removing the flag bit

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       (try_begin),
         (eq, ":hide_weapons", 1),
         (cur_tableau_set_override_flags, af_override_fullhelm|af_override_head|af_override_weapons),
       (try_end),
       
       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 450),
       (assign, ":camera_yaw", 15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),
       
       (troop_get_inventory_slot, ":horse_item", ":troop_no", ek_horse),
       (try_begin),
         (gt, ":horse_item", 0),
         (eq, ":hide_weapons", 0),
         (cur_tableau_add_horse, ":horse_item", pos2, "anim_horse_stand", 0),
         (assign, ":animation", "anim_ride_0"),
         (assign, ":camera_yaw", 23),
         (assign, ":cam_height", 150),
         (assign, ":camera_distance", 550),
       (try_end),
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
]),

#script_get_prosperity_text_to_s50
# INPUT: center_no
("get_prosperity_text_to_s50",
    [(store_script_param, ":center_no", 1),
     (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
     (val_div, ":prosperity", 20),
	 
     (try_begin),(eq, ":prosperity", 0),(str_store_string, s50, "@Very Poor"),
     (else_try) ,(eq, ":prosperity", 1),(str_store_string, s50, "@Poor"),
     (else_try) ,(eq, ":prosperity", 2),(str_store_string, s50, "@Average"),
     (else_try) ,(eq, ":prosperity", 3),(str_store_string, s50, "@Rich"),
     (else_try) ,                       (str_store_string, s50, "@Very Rich"),
     (try_end),
]),

#script_spawn_bandits
("spawn_bandits",
    [(set_spawn_radius,5),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_mountain_bandits"),
       (lt,":num_parties",num_mountain_bandit_spawn_points*2), # 2 bandits per spawn point on average - was 4
       (store_random,":spawn_point",num_mountain_bandit_spawn_points),
       (val_add,":spawn_point","p_mountain_bandit_spawn_point"),
       (spawn_around_party,":spawn_point","pt_mountain_bandits"),
       (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_forest_bandits"),
       (lt,":num_parties",num_forest_bandit_spawn_points*2),
       (store_random,":spawn_point",num_forest_bandit_spawn_points),
       (val_add,":spawn_point","p_forest_bandit_spawn_point"),
       (spawn_around_party,":spawn_point","pt_forest_bandits"),
       (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_sea_raiders"),
       (lt,":num_parties",num_sea_raider_spawn_points*2),
       (store_random,":spawn_point",num_sea_raider_spawn_points),
       (val_add,":spawn_point","p_sea_raider_spawn_point_1"),
       (spawn_around_party,":spawn_point","pt_sea_raiders"),
       (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_steppe_bandits"),
       (lt,":num_parties",num_steppe_bandit_spawn_points*2),
       (store_random,":spawn_point",num_steppe_bandit_spawn_points),
       (val_add,":spawn_point","p_steppe_bandit_spawn_point"),
       (spawn_around_party,":spawn_point","pt_steppe_bandits"),
       (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_looters"),
       (lt,":num_parties",20), # 1 looter per 3 towns
       (store_random_in_range,":spawn_point",centers_begin,advcamps_begin),
       (spawn_around_party,":spawn_point","pt_looters"),
       (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
       (assign, ":spawned_party_id", reg0),
       # (try_begin), #MV: commented out - quest looters don't disappear, they are neutral
         # (check_quest_active, "qst_deal_with_looters"),
         # (party_set_flags, ":spawned_party_id", pf_quest_party, 1),
       # (else_try),
         (party_set_flags, ":spawned_party_id", pf_quest_party, 0),
       # (try_end),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_deserters"),
       (lt,":num_parties",10), #was 15
       (set_spawn_radius, 4),
       (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 5),
         (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         (store_troop_faction, ":troop_faction", ":troop_no"),
         (neq, ":troop_faction", "fac_player_supporters_faction"),
         (gt, ":party_no", 0),
         (neg|party_is_in_any_town, ":party_no"), #MV: this doesn't seem to work, so added two equivalent lines
         (party_get_attached_to, ":attached_to_party", ":party_no"),
         (neg|is_between, ":attached_to_party", centers_begin, centers_end),

         (faction_get_slot, ":tier_1_troop", ":troop_faction", slot_faction_deserter_troop),
         (try_begin), # only evil factions have deserters, good ones have -1 for deserter troop
           (ge, ":tier_1_troop", 0),		 
##           (party_get_attached_to, ":attached_party_no", ":party_no"),
##           (lt, ":attached_party_no", 0),#in wilderness
           (spawn_around_party, ":party_no", "pt_deserters"),
           (party_set_slot, reg0, slot_party_type, spt_bandit), # Added by foxyman, TLD
           (assign, ":new_party", reg0),
           (store_character_level, ":level", "trp_player"),
           (store_mul, ":max_number_to_add", ":level", 2),
           (val_add, ":max_number_to_add", 11),
           (store_random_in_range, ":number_to_add", 10, ":max_number_to_add"),
           (party_add_members, ":new_party", ":tier_1_troop", ":number_to_add"),
           (store_random_in_range, ":random_no", 1, 4),
           (try_for_range, ":unused", 0, ":random_no"),
             (party_upgrade_with_xp, ":new_party", 1000000, 0),
           (try_end),
		 (try_end),
##         (str_store_party_name, s1, ":party_no"),
##         (call_script, "script_get_closest_center", ":party_no"),
##         (try_begin),
##           (gt, reg0, 0),
##           (str_store_party_name, s2, reg0),
##         (else_try),
##           (str_store_string, s2, "@unknown place"),
##         (try_end),
##         (assign, reg1, ":number_to_add"),
##         (display_message, "@{reg1} Deserters spawned from {s1}, near {s2}."),
       (try_end),
     (try_end),
]),

#script_count_mission_casualties_from_agents
("count_mission_casualties_from_agents",
    [(party_clear, "p_player_casualties"),
     (party_clear, "p_enemy_casualties"),
     (party_clear, "p_ally_casualties"),
     (assign, "$any_allies_at_the_last_battle", 0),

	# Reset routed count
	(try_for_range, ":troop_no", 0, "trp_last"),
		(troop_set_slot, ":troop_no", slot_troop_routed_us, 0),
		(troop_set_slot, ":troop_no", slot_troop_routed_allies, 0),
		(troop_set_slot, ":troop_no", slot_troop_routed_enemies, 0),
	(try_end),

     (try_for_agents, ":cur_agent"),
       #(agent_slot_eq|neg, ":cur_agent", slot_agent_routed, 2),
       (agent_is_human, ":cur_agent"),
       (agent_get_troop_id, ":agent_troop_id", ":cur_agent"),
       (neg|is_between, ":agent_troop_id", warg_ghost_begin, warg_ghost_end), # dont count riderless wargs
       (agent_get_party_id, ":agent_party", ":cur_agent"),

	# CC: code modified to count routed agents.
	(try_begin),
		(agent_slot_eq, ":cur_agent", slot_agent_routed, 2),
		(troop_get_slot, ":num_routed_us", ":agent_troop_id", slot_troop_routed_us),
		(troop_get_slot, ":num_routed_allies", ":agent_troop_id", slot_troop_routed_allies),
		(troop_get_slot, ":num_routed_enemies", ":agent_troop_id", slot_troop_routed_enemies),
		(try_begin),
         		(eq, ":agent_party", "p_main_party"),
			(val_add, ":num_routed_us", 1),
			(troop_set_slot, ":agent_troop_id", slot_troop_routed_us, ":num_routed_us"),
		(else_try),
			(agent_is_ally|neg, ":cur_agent"),	
			(val_add, ":num_routed_enemies", 1),
			(troop_set_slot, ":agent_troop_id", slot_troop_routed_enemies, ":num_routed_enemies"),	
		(else_try),
			(agent_is_ally, ":cur_agent"),			
			(val_add, ":num_routed_allies", 1),
			(troop_set_slot, ":agent_troop_id", slot_troop_routed_allies, ":num_routed_allies"),		
		(try_end),
	(try_end),
	# CC: code end.

       (try_begin),
         (neq, ":agent_party", "p_main_party"),
         (agent_is_ally, ":cur_agent"),
         (assign, "$any_allies_at_the_last_battle", 1),
       (try_end),
       (neg|agent_is_alive, ":cur_agent"),
       (try_begin),
         (eq, ":agent_party", "p_main_party"),
         (party_add_members, "p_player_casualties", ":agent_troop_id", 1),
         (try_begin),
       	   (agent_slot_eq|neg, ":cur_agent", slot_agent_routed, 2),
       	   (agent_slot_eq|this_or_next, ":cur_agent", slot_agent_wounded, 1),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_player_casualties", ":agent_troop_id", 1),
         (try_end),
       (else_try),
         (agent_is_ally, ":cur_agent"),
         (party_add_members, "p_ally_casualties", ":agent_troop_id", 1),
         (try_begin),
       	   (agent_slot_eq|neg, ":cur_agent", slot_agent_routed, 2),
       	   (agent_slot_eq|this_or_next, ":cur_agent", slot_agent_wounded, 1),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_ally_casualties", ":agent_troop_id", 1),
         (try_end),
       (else_try),
         (party_add_members, "p_enemy_casualties", ":agent_troop_id", 1),
         (try_begin),
       	   (agent_slot_eq|neg, ":cur_agent", slot_agent_routed, 2),
       	   (agent_slot_eq|this_or_next, ":cur_agent", slot_agent_wounded, 1),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_enemy_casualties", ":agent_troop_id", 1),
         (try_end),
       (try_end),
     (try_end),
]),

#script_get_max_skill_of_player_party
# INPUT: arg1 = skill_no
# OUTPUT: reg0 = max_skill, reg1 = skill_owner_troop_no
("get_max_skill_of_player_party",
    [(store_script_param, ":skill_no", 1),
     (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
     (store_skill_level, ":max_skill", ":skill_no", "trp_player"),
     (assign, ":skill_owner", "trp_player"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (neg|troop_is_wounded, ":stack_troop"),
       (store_skill_level, ":cur_skill", ":skill_no", ":stack_troop"),
       (gt, ":cur_skill", ":max_skill"),
       (assign, ":max_skill", ":cur_skill"),
       (assign, ":skill_owner", ":stack_troop"),
     (try_end),
     (assign, reg0, ":max_skill"),
     (assign, reg1, ":skill_owner"),
]),

#script_upgrade_hero_party
# INPUT: arg1 = party_id, arg2 = xp_amount
("upgrade_hero_party",
    [(store_script_param, ":party_no", 1),
     (store_script_param, ":xp_amount", 2),
     (party_upgrade_with_xp, ":party_no", ":xp_amount", 0),
]),

#script_get_improvement_details
# INPUT: arg1 = improvement
# OUTPUT: reg0 = base_cost
# ("get_improvement_details",
    # [(store_script_param, ":improvement_no", 1),
     # (try_begin),
       # (eq, ":improvement_no", slot_center_has_manor),
       # (str_store_string, s0, "@Manor"),
       # (str_store_string, s1, "@A manor lets you rest at the village and pay your troops half wages while you rest."),
       # (assign, reg0, 8000),
     # (else_try),
       # (eq, ":improvement_no", slot_center_has_fish_pond),
       # (str_store_string, s0, "@Mill"),
       # (str_store_string, s1, "@A mill increases village prosperity by 5%."),
       # (assign, reg0, 6000),
     # (else_try),
       # (eq, ":improvement_no", slot_center_has_watch_tower),
       # (str_store_string, s0, "@Watch Tower"),
       # (str_store_string, s1, "@A watch tower lets the villagers raise alarm earlier. The time it takes for enemies to loot the village increases by 25%."),
       # (assign, reg0, 5000),
     # (else_try),
       # (eq, ":improvement_no", slot_center_has_school),
       # (str_store_string, s0, "@School"),
       # (str_store_string, s1, "@A shool increases the loyality of the villagers to you by +1 every month."),
       # (assign, reg0, 9000),
     # (else_try),
       # (eq, ":improvement_no", slot_center_has_messenger_post),
       # (str_store_string, s0, "@Messenger Post"),
       # (str_store_string, s1, "@A messenger post lets the inhabitants send you a message whenever enemies are nearby, even if you are far away from here."),
       # (assign, reg0, 4000),
     # (else_try),
       # (eq, ":improvement_no", slot_center_has_prisoner_tower),
       # (str_store_string, s0, "@Prison Tower"),
       # (str_store_string, s1, "@A prison tower reduces the chance of captives held here running away successfully."),
       # (assign, reg0, 7000),
     # (try_end),
# ]),

#script_cf_troop_agent_is_alive
# INPUT: arg1 = troop_id
("cf_troop_agent_is_alive",
    [(store_script_param, ":troop_no", 1),
     (assign, ":alive_count", 0),
     (try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
       (eq, ":troop_no", ":cur_agent_troop"),
       (agent_is_alive, ":cur_agent"),
       (val_add, ":alive_count", 1),
     (try_end),
     (gt, ":alive_count", 0),
]),

#script_get_troop_item_amount
# INPUT: arg1 = troop_no, arg2 = item_no
# OUTPUT: reg0 = item_amount
("get_troop_item_amount",
    [(store_script_param, ":troop_no", 1),
     (store_script_param, ":item_no", 2),
     (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
     (assign, ":count", 0),
     (try_for_range, ":i_slot", 0, ":inv_cap"),
       (troop_get_inventory_slot, ":cur_item", ":troop_no", ":i_slot"),
       (eq, ":cur_item", ":item_no"),
       (val_add, ":count", 1),
     (try_end),
     (assign, reg0, ":count"),
]),

#script_apply_attribute_bonuses
# Checks if items that change attributes are in the player inventory and adds or removes an attribute bonus
("apply_attribute_bonuses",[
    # Tulcarisil, STR+1
    (call_script, "script_apply_attribute_bonus_for_item", "itm_ring_a_reward", 0, ca_strength, 1),
    
    # Finwarisil, AGI+1
    (call_script, "script_apply_attribute_bonus_for_item", "itm_ring_b_reward", 0, ca_agility, 1),

    # Light of Galadriel, INT+1
    (call_script, "script_apply_attribute_bonus_for_item", "itm_phial_reward", 0, ca_intelligence, 1),

    # Horn of Gondor, CHA+1
    (call_script, "script_apply_attribute_bonus_for_item", "itm_horn_gondor_reward", 0, ca_charisma, 1),

    # Khand Sacrificial Knife, CHA+1
    (call_script, "script_apply_attribute_bonus_for_item", "itm_khand_knife_reward", 0, ca_charisma, 1),

    # Witchking Helmet, CHA+1 when equipped
    (call_script, "script_apply_attribute_bonus_for_item", "itm_witchking_helmet", 1, ca_charisma, 1),
	
	(call_script, "script_apply_attribute_bonus_for_item", "itm_isen_uruk_heavy_reward", 1, ca_charisma, 1),
]),

#script_apply_attribute_bonus_for_item
# Checks if items that change attributes are in the player inventory and adds or removes an attribute bonus
("apply_attribute_bonus_for_item",[
    (store_script_param, ":item", 1),
    (store_script_param, ":must_be_equipped", 2),
    (store_script_param, ":attr", 3),
    (store_script_param, ":attr_bonus", 4),
    
    (try_begin),
      (eq, ":attr", ca_strength),
      (assign, ":slot", slot_item_strength_bonus),
    (else_try),
      (eq, ":attr", ca_agility),
      (assign, ":slot", slot_item_agility_bonus),
    (else_try),
      (eq, ":attr", ca_intelligence),
      (assign, ":slot", slot_item_intelligence_bonus),
    (else_try),
      #(eq, ":attr", ca_charisma),
      (assign, ":slot", slot_item_charisma_bonus),
    (try_end),
    
    (try_begin),
      (assign, ":item_gives_bonus", 0),
      (try_begin),
        (eq, ":must_be_equipped", 1),
        (troop_has_item_equipped, "trp_player", ":item"),
        (assign, ":item_gives_bonus", 1),
      (else_try),
        (eq, ":must_be_equipped", 0),
        (player_has_item, ":item"), # Doesn't work for equipped items
        (assign, ":item_gives_bonus", 1),
      (try_end),
      (eq, ":item_gives_bonus", 1),
      
      (try_begin), # just got it
        (item_slot_eq, ":item", ":slot", 0),
        (troop_raise_attribute, "trp_player", ":attr", ":attr_bonus"),
        (item_set_slot, ":item", ":slot", 1),
      (try_end),
    (else_try), #lost or unequipped it
      (item_slot_eq, ":item", ":slot", 1),
      (val_mul, ":attr_bonus", -1),
      (troop_raise_attribute, "trp_player", ":attr", ":attr_bonus"),
      (item_set_slot, ":item", ":slot", 0),
    (try_end),
]),

#script_get_name_from_dna_to_s50
# INPUT: arg1 = dna, arg2 = troop_no (MV added for races)
# OUTPUT: s50 = name
("get_name_from_dna_to_s50",
    [(store_script_param, ":dna", 1),
     (store_script_param, ":troop", 2),
     (troop_get_type, ":race", ":troop"),
     (try_begin),
       (is_between, ":race", tf_orc_begin, tf_orc_end),
       (assign, ":names_begin", names_orc_begin),
       (assign, ":names_end", names_orc_end),
     (else_try),
       (eq, ":race", tf_dwarf),
       (assign, ":names_begin", names_dwarf_begin),
       (assign, ":names_end", names_dwarf_end),
     (else_try),
       (is_between, ":race", tf_elf_begin, tf_elf_end),
       (assign, ":names_begin", names_elf_begin),
       (assign, ":names_end", names_elf_end),
     (else_try),
       (assign, ":names_begin", names_begin),
       (assign, ":names_end", names_end),
     (try_end),
     
     (store_sub, ":num_names", ":names_end", ":names_begin"),
     (store_sub, ":num_surnames", surnames_end, surnames_begin),
     (assign, ":selected_name", ":dna"),
     (val_mod, ":selected_name", ":num_names"),
     (assign, ":selected_surname", ":dna"),
     (val_div, ":selected_surname", ":num_names"),
     (val_mod, ":selected_surname", ":num_surnames"),
     (val_add, ":selected_name", ":names_begin"),
     (val_add, ":selected_surname", surnames_begin),
     (str_store_string, s50, ":selected_name"),
     (str_store_string, s50, ":selected_surname"),
     (try_begin), #add a little extra
       (lt, ":selected_surname", surnames_nickname_begin), # somebody of sometown format
       (try_begin),
         (is_between, ":race", tf_orc_begin, tf_orc_end),
         (str_store_string, s50, "@{s50} Caves"),
       (else_try),
         (eq, ":race", tf_dwarf),
         (str_store_string, s50, "@{s50} Mines"),
       (else_try),
         (is_between, ":race", tf_elf_begin, tf_elf_end),
         (str_store_string, s50, "@{s50} Woods"),
       (try_end),
     (try_end),
]),

#script_change_center_prosperity
# INPUT: arg1 = center_no, arg2 = difference
("change_center_prosperity",
    [(store_script_param, ":center_no", 1),
     (store_script_param, ":difference", 2),
     (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
     (store_add, ":new_prosperity", ":prosperity", ":difference"),
     (val_clamp, ":new_prosperity", 0, 100),
     (store_div, ":old_state", ":prosperity", 20),
     (store_div, ":new_state", ":new_prosperity", 20),
     (try_begin),
       (neq, ":old_state", ":new_state"),
       (str_store_party_name_link, s2, ":center_no"),
       (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
       (str_store_string, s3, s50),
       (party_set_slot, ":center_no", slot_town_prosperity, ":new_prosperity"),
       (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
       (str_store_string, s4, s50),
       #(display_message, "@Prosperity of {s2} has changed from {s3} to {s4}."),
       (call_script, "script_update_center_notes", ":center_no"),
     (else_try),
       (party_set_slot, ":center_no", slot_town_prosperity, ":new_prosperity"),
     (try_end),
]),

#script_get_center_ideal_prosperity
# INPUT: arg1 = center_no
# OUTPUT: reg0 = ideal_prosperity
("get_center_ideal_prosperity",
    [#(store_script_param, ":center_no", 1),
     (assign, ":ideal", 40),
     (assign, reg0, ":ideal"),
]),

#script_troop_add_gold
# INPUT: arg1 = troop_no, arg2 = amount
("troop_add_gold",
    [(store_script_param, ":troop_no", 1),
     (store_script_param, ":amount", 2),
     (troop_add_gold, ":troop_no", ":amount"),
     (try_begin),
       (eq, ":troop_no", "trp_player"),
       #(play_sound, "snd_money_received"),
     (try_end),
]),     

#NPC companion changes begin
("initialize_npcs",[
# set strings
#good companions
        # Mablung
        (troop_set_slot, "trp_npc1", slot_troop_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc1", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc1", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc1", slot_troop_2ary_morality_value, 2),
        (troop_set_slot, "trp_npc1", slot_troop_personalityclash_object, "trp_npc9"), #Gulm/none
        (troop_set_slot, "trp_npc1", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc1", slot_troop_personalitymatch_object, "trp_npc6"),  #Luevanna
        (troop_set_slot, "trp_npc1", slot_troop_home, "p_town_west_osgiliath"),
        (troop_set_slot, "trp_npc1", slot_troop_payment_request, 2000 / companionPriceMult ),
        (troop_set_slot, "trp_npc1", slot_troop_cur_center, "p_town_henneth_annun"),  #TLD
        (troop_set_slot, "trp_npc1", slot_troop_rank_request, 3),  #TLD

        # Cirdil
        (troop_set_slot, "trp_npc2", slot_troop_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc2", slot_troop_morality_value, 2),  
        (troop_set_slot, "trp_npc2", slot_troop_2ary_morality_type, -1),  
        (troop_set_slot, "trp_npc2", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc2", slot_troop_personalityclash_object, "trp_npc9"), #Gulm/none
        (troop_set_slot, "trp_npc2", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc2", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung
        (troop_set_slot, "trp_npc2", slot_troop_home, "p_town_minas_morgul"),
        (troop_set_slot, "trp_npc2", slot_troop_payment_request, 100 / companionPriceMult ), 
        (troop_set_slot, "trp_npc2", slot_troop_cur_center, "p_town_minas_tirith"),  #TLD
        (troop_set_slot, "trp_npc2", slot_troop_rank_request, 0),  #TLD

        # Ulfas
        (troop_set_slot, "trp_npc3", slot_troop_morality_type, tmt_aristocratic),
        (troop_set_slot, "trp_npc3", slot_troop_morality_value, 4),  
        (troop_set_slot, "trp_npc3", slot_troop_2ary_morality_type, -1), 
        (troop_set_slot, "trp_npc3", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc3", slot_troop_personalityclash_object, "trp_npc1"), #Mablung
        (troop_set_slot, "trp_npc3", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc3", slot_troop_personalitymatch_object, "trp_npc4"),  #Gálmynë
        (troop_set_slot, "trp_npc3", slot_troop_home, "p_ford_fangorn"),
        (troop_set_slot, "trp_npc3", slot_troop_payment_request, 1200 / companionPriceMult), 
        (troop_set_slot, "trp_npc3", slot_troop_cur_center, "p_town_west_emnet"),  #TLD
        (troop_set_slot, "trp_npc3", slot_troop_rank_request, 1),  #TLD

        # Gálmynë
        (troop_set_slot, "trp_npc4", slot_troop_morality_type, tmt_aristocratic),
        (troop_set_slot, "trp_npc4", slot_troop_morality_value, -1),  
        (troop_set_slot, "trp_npc4", slot_troop_2ary_morality_type, tmt_honest), 
        (troop_set_slot, "trp_npc4", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc4", slot_troop_personalityclash_object, "trp_npc9"), #Gulm/none
        (troop_set_slot, "trp_npc4", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc4", slot_troop_personalitymatch_object, "trp_npc8"),  #Faniul
        (troop_set_slot, "trp_npc4", slot_troop_home, "p_ford_brown_lands"), #Field of Celebrant ford
        (troop_set_slot, "trp_npc4", slot_troop_payment_request, 3000 / companionPriceMult), 
        (troop_set_slot, "trp_npc4", slot_troop_cur_center, "p_town_edoras"),  #TLD
        (troop_set_slot, "trp_npc4", slot_troop_rank_request, 4),  #TLD

        # Glorfindel
        (troop_set_slot, "trp_npc5", slot_troop_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc5", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc5", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc5", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc5", slot_troop_personalityclash_object, "trp_npc9"), #Gulm/none
        (troop_set_slot, "trp_npc5", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc5", slot_troop_personalitymatch_object, "trp_npc9"),  #Gulm/none
        (troop_set_slot, "trp_npc5", slot_troop_home, "p_town_isengard"),
        (troop_set_slot, "trp_npc5", slot_troop_payment_request, 5000 / companionPriceMult),
        (troop_set_slot, "trp_npc5", slot_troop_cur_center, "p_town_caras_galadhon"),  #TLD
        (troop_set_slot, "trp_npc5", slot_troop_rank_request, 7),  #TLD

        # Luevanna
        (troop_set_slot, "trp_npc6", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc6", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc6", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc6", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc6", slot_troop_personalityclash_object, "trp_npc7"), #Kíli
        (troop_set_slot, "trp_npc6", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc6", slot_troop_personalitymatch_object, "trp_npc5"),  #Glorfindel
        (troop_set_slot, "trp_npc6", slot_troop_home, "p_town_dol_guldur"),
        (troop_set_slot, "trp_npc6", slot_troop_payment_request, 100 / companionPriceMult),
        (troop_set_slot, "trp_npc6", slot_troop_cur_center, "p_town_thranduils_halls"),  #TLD
        (troop_set_slot, "trp_npc6", slot_troop_rank_request, 0),  #TLD

        # Kíli
        (troop_set_slot, "trp_npc7", slot_troop_morality_type, tmt_aristocratic),
        (troop_set_slot, "trp_npc7", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc7", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc7", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc7", slot_troop_personalityclash_object, "trp_npc5"), #Glorfindel
        (troop_set_slot, "trp_npc7", slot_troop_personalityclash2_object, "trp_npc6"),  #Luevanna
        (troop_set_slot, "trp_npc7", slot_troop_personalitymatch_object, "trp_npc8"),  #Faniul
        (troop_set_slot, "trp_npc7", slot_troop_home, "p_town_moria"),
        (troop_set_slot, "trp_npc7", slot_troop_payment_request, 800 / companionPriceMult ),
        (troop_set_slot, "trp_npc7", slot_troop_cur_center, "p_town_erebor"),  #TLD
        (troop_set_slot, "trp_npc7", slot_troop_rank_request, 1),  #TLD

        # Faniul
        (troop_set_slot, "trp_npc8", slot_troop_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc8", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc8", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc8", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc8", slot_troop_personalityclash_object, "trp_npc3"), #Ulfas
        (troop_set_slot, "trp_npc8", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc8", slot_troop_personalitymatch_object, "trp_npc7"),  #Kíli
        (troop_set_slot, "trp_npc8", slot_troop_home, "p_town_beorn_house"),
        (troop_set_slot, "trp_npc8", slot_troop_payment_request, 300 / companionPriceMult),
        (troop_set_slot, "trp_npc8", slot_troop_cur_center, "p_town_dale"),  #TLD
        (troop_set_slot, "trp_npc8", slot_troop_rank_request, 0),  #TLD

#evil companions
        # Gulm
        (troop_set_slot, "trp_npc9", slot_troop_morality_type, tmt_aristocratic),
        (troop_set_slot, "trp_npc9", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc9", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc9", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc9", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc9", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc9", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung/none
        (troop_set_slot, "trp_npc9", slot_troop_home, "p_town_hornburg"),
        (troop_set_slot, "trp_npc9", slot_troop_payment_request, 2000 / companionPriceMult),
        (troop_set_slot, "trp_npc9", slot_troop_cur_center, "p_town_urukhai_h_camp"),  #TLD
        (troop_set_slot, "trp_npc9", slot_troop_rank_request, 3),  #TLD

        # Durgash
        (troop_set_slot, "trp_npc10", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc10", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc10", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc10", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc10", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc10", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc10", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung/none
        (troop_set_slot, "trp_npc10", slot_troop_home, -1),
        (troop_set_slot, "trp_npc10", slot_troop_payment_request, 800 / companionPriceMult),
        (troop_set_slot, "trp_npc10", slot_troop_cur_center, "p_town_isengard"),  #TLD
        (troop_set_slot, "trp_npc10", slot_troop_rank_request, 1),  #TLD

        # Ufthak
        (troop_set_slot, "trp_npc11", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc11", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc11", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc11", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc11", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc11", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc11", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung/none
        (troop_set_slot, "trp_npc11", slot_troop_home, -1),
        (troop_set_slot, "trp_npc11", slot_troop_payment_request, 100 / companionPriceMult),
        (troop_set_slot, "trp_npc11", slot_troop_cur_center, "p_town_cirith_ungol"),  #TLD
        (troop_set_slot, "trp_npc11", slot_troop_rank_request, 0),  #TLD

        # Gorbag
        (troop_set_slot, "trp_npc12", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc12", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc12", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc12", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc12", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc12", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc12", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung/none
        (troop_set_slot, "trp_npc12", slot_troop_home, -1),
        (troop_set_slot, "trp_npc12", slot_troop_payment_request, 1800 / companionPriceMult),
        (troop_set_slot, "trp_npc12", slot_troop_cur_center, "p_town_minas_morgul"),  #TLD
        (troop_set_slot, "trp_npc12", slot_troop_rank_request, 3),  #TLD

        # Lykyada
        (troop_set_slot, "trp_npc13", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc13", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc13", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc13", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc13", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc13", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc13", slot_troop_personalitymatch_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc13", slot_troop_home, -1),
        (troop_set_slot, "trp_npc13", slot_troop_payment_request, 4000 / companionPriceMult),
        (troop_set_slot, "trp_npc13", slot_troop_cur_center, "p_town_harad_camp"),  #TLD
        (troop_set_slot, "trp_npc13", slot_troop_rank_request, 5),  #TLD

        # Fuldimir
        (troop_set_slot, "trp_npc14", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc14", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc14", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc14", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc14", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc14", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc14", slot_troop_personalitymatch_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc14", slot_troop_home, -1),
        (troop_set_slot, "trp_npc14", slot_troop_payment_request, 300 / companionPriceMult),
        (troop_set_slot, "trp_npc14", slot_troop_cur_center, "p_town_umbar_camp"),  #TLD
        (troop_set_slot, "trp_npc14", slot_troop_rank_request, 0),  #TLD

        # Bolzog
        (troop_set_slot, "trp_npc15", slot_troop_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc15", slot_troop_morality_value, 1),
        (troop_set_slot, "trp_npc15", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc15", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc15", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc15", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc15", slot_troop_personalitymatch_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc15", slot_troop_home, -1),
        (troop_set_slot, "trp_npc15", slot_troop_payment_request, 500 / companionPriceMult),
        (troop_set_slot, "trp_npc15", slot_troop_cur_center, "p_town_moria"),  #TLD
        (troop_set_slot, "trp_npc15", slot_troop_rank_request, 1),  #TLD

        # Varfang
        (troop_set_slot, "trp_npc16", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc16", slot_troop_morality_value, 0),
        (troop_set_slot, "trp_npc16", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc16", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc16", slot_troop_personalityclash_object, "trp_npc1"), #Mablung/none
        (troop_set_slot, "trp_npc16", slot_troop_personalityclash2_object, "trp_npc2"), #Cirdil/none
        (troop_set_slot, "trp_npc16", slot_troop_personalitymatch_object, "trp_npc1"),  #Mablung/none
        (troop_set_slot, "trp_npc16", slot_troop_home, -1),
        (troop_set_slot, "trp_npc16", slot_troop_payment_request, 1200 / companionPriceMult),
        (troop_set_slot, "trp_npc16", slot_troop_cur_center, "p_town_rhun_main_camp"),  #TLD
        (troop_set_slot, "trp_npc16", slot_troop_rank_request, 2),  #TLD

#additional companions        
        # Dímborn
        (troop_set_slot, "trp_npc17", slot_troop_morality_type, -1),
        (troop_set_slot, "trp_npc17", slot_troop_morality_value, 0), 
        (troop_set_slot, "trp_npc17", slot_troop_2ary_morality_type, -1), 
        (troop_set_slot, "trp_npc17", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc17", slot_troop_personalityclash_object, "trp_npc9"), #Gulm/none
        (troop_set_slot, "trp_npc17", slot_troop_personalityclash2_object, "trp_npc10"),  #Durgash/none
        (troop_set_slot, "trp_npc17", slot_troop_personalitymatch_object, "trp_npc6"),  #Luevanna
        (troop_set_slot, "trp_npc17", slot_troop_home, "p_town_cerin_dolen"),
        (troop_set_slot, "trp_npc17", slot_troop_payment_request, 400 / companionPriceMult ),
        (troop_set_slot, "trp_npc17", slot_troop_cur_center, "p_town_woodsmen_village"),  #TLD
        (troop_set_slot, "trp_npc17", slot_troop_rank_request, 0),  #TLD

        (store_sub, "$number_of_npc_slots", slot_troop_strings_end, slot_troop_intro), # 131-101=30 strings per NPC 
        (store_sub, ":total_companions", companions_end, companions_begin),
        (try_begin),
          (store_sub, reg1, "str_companion_strings_end", "str_npc1_intro"), #total actual strings
          (store_mul, reg2, "$number_of_npc_slots", ":total_companions"), #total strings needed
          (neq, reg1, reg2),
          (display_message, "@ERROR: Companion strings actual/needed: {reg1}/{reg2}", 0xFFFF2222),
        (try_end),
        
        (try_for_range, ":npc", companions_begin, companions_end),
            (try_for_range, ":slot_addition", 0, "$number_of_npc_slots"),
                (store_add, ":slot", ":slot_addition", slot_troop_intro),
                
                (store_mul, ":string_addition", ":slot_addition", ":total_companions"), #MV: was 16
                (store_add, ":string", "str_npc1_intro", ":string_addition"), 
                (val_add, ":string", ":npc"),
                (val_sub, ":string", companions_begin),

                (troop_set_slot, ":npc", ":slot", ":string"),
            (try_end),
        (try_end),
        (call_script, "script_add_log_entry", logent_game_start, "trp_player", -1, -1, -1),
]),

# script_objectionable_action
("objectionable_action",
    [   (store_script_param_1, ":action_type"),
        (store_script_param_2, ":action_string"),
#        (str_store_string, 12, ":action_string"),
#        (display_message, "@Objectionable action check: {s12}"),
        (assign, ":grievance_minimum", -2),
        (assign, ":npc_last_displayed", 0),
        (try_for_range, ":npc", companions_begin, companions_end),
            (main_party_has_troop, ":npc"),
###Primary morality check
            (try_begin),
                (troop_slot_eq, ":npc", slot_troop_morality_type, ":action_type"),
                (troop_get_slot, ":value", ":npc", slot_troop_morality_value),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_morality_state, tms_acknowledged),
# npc is betrayed, major penalty to player honor and morale
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_mul, ":value", 2),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
                    (this_or_next|troop_slot_eq, ":npc", slot_troop_morality_state, tms_dismissed),
                        (eq, "$disable_npc_complaints", 1),
# npc is quietly disappointed
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
# npc raises the issue for the first time
                    (troop_slot_eq, ":npc", slot_troop_morality_state, tms_no_problem),
                    (gt, ":value", ":grievance_minimum"),
                    (assign, "$npc_with_grievance", ":npc"),
                    (assign, "$npc_grievance_string", ":action_string"),
                    (assign, "$npc_grievance_slot", slot_troop_morality_state),
                    (assign, ":grievance_minimum", ":value"),
                    (assign, "$npc_praise_not_complaint", 0),
                    (try_begin),
                        (lt, ":value", 0),
                        (assign, "$npc_praise_not_complaint", 1),
                    (try_end),
                (try_end),
###Secondary morality check
            (else_try),
                (troop_slot_eq, ":npc", slot_troop_2ary_morality_type, ":action_type"),
                (troop_get_slot, ":value", ":npc", slot_troop_2ary_morality_value),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_acknowledged),
# npc is betrayed, major penalty to player honor and morale
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_mul, ":value", 2),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
                    (this_or_next|troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_dismissed),
                        (eq, "$disable_npc_complaints", 1),
# npc is quietly disappointed
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
# npc raises the issue for the first time
                    (troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_no_problem),
                    (gt, ":value", ":grievance_minimum"),
                    (assign, "$npc_with_grievance", ":npc"),
                    (assign, "$npc_grievance_string", ":action_string"),
                    (assign, "$npc_grievance_slot", slot_troop_2ary_morality_state),
                    (assign, ":grievance_minimum", ":value"),
                    (assign, "$npc_praise_not_complaint", 0),
                    (try_begin),
                        (lt, ":value", 0),
                        (assign, "$npc_praise_not_complaint", 1),
                    (try_end),
                (try_end),
            (try_end),

            (try_begin),
                (gt, "$npc_with_grievance", 0),
                (eq, "$npc_praise_not_complaint", 0),
                (neq, "$npc_with_grievance", ":npc_last_displayed"),                
                (str_store_troop_name, 4, "$npc_with_grievance"),
                (display_message, "@{s4} looks upset."),
                (assign, ":npc_last_displayed", "$npc_with_grievance"),
            (try_end),
        (try_end),        
]),

("post_battle_personality_clash_check",
[
#            (display_message, "@Post-victory personality clash check"),
            (try_for_range, ":npc", companions_begin, companions_end),
                (eq, "$disable_npc_complaints", 0),

                (main_party_has_troop, ":npc"),
                (neg|troop_is_wounded, ":npc"),

                (troop_get_slot, ":other_npc", ":npc", slot_troop_personalityclash2_object),
                (main_party_has_troop, ":other_npc"),
                (neg|troop_is_wounded, ":other_npc"),

#                (store_random_in_range, ":random", 0, 3),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_personalityclash2_state, 0),
                    (try_begin),
#                        (eq, ":random", 0),
                        (assign, "$npc_with_personality_clash_2", ":npc"),
                    (try_end),
                (try_end),

            (try_end),

            (try_for_range, ":npc", companions_begin, companions_end),
                (troop_slot_eq, ":npc", slot_troop_personalitymatch_state, 0),
                (eq, "$disable_npc_complaints", 0),
                (main_party_has_troop, ":npc"),
                (neg|troop_is_wounded, ":npc"),
                (troop_get_slot, ":other_npc", ":npc", slot_troop_personalitymatch_object),
                (main_party_has_troop, ":other_npc"),
                (neg|troop_is_wounded, ":other_npc"),
                (assign, "$npc_with_personality_match", ":npc"),
            (try_end),


            (try_begin),
                (gt, "$npc_with_personality_clash_2", 0),
                (assign, "$npc_map_talk_context", slot_troop_personalityclash2_state),
                (start_map_conversation, "$npc_with_personality_clash_2"),
            (else_try),
                (gt, "$npc_with_personality_match", 0),
                (assign, "$npc_map_talk_context", slot_troop_personalitymatch_state),
                (start_map_conversation, "$npc_with_personality_match"),
            (try_end),
]),

#script_event_player_defeated_enemy_party
("event_player_defeated_enemy_party",
    [# (try_begin),
       # (check_quest_active, "qst_raid_caravan_to_start_war"),
       # (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
       # (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
       # (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
       # (quest_slot_eq, "qst_raid_caravan_to_start_war", slot_quest_target_faction, ":enemy_faction"),
       # (quest_get_slot, ":cur_state", "qst_raid_caravan_to_start_war", slot_quest_current_state),
       # (quest_get_slot, ":quest_target_amount", "qst_raid_caravan_to_start_war", slot_quest_target_amount),
       # (val_add, ":cur_state", 1),
       # (quest_set_slot, "qst_raid_caravan_to_start_war", slot_quest_current_state, ":cur_state"),
       # (try_begin),
         # (ge, ":cur_state", ":quest_target_amount"),
         # #(quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
         # #(quest_get_slot, ":quest_giver_troop", "qst_raid_caravan_to_start_war", slot_quest_giver_troop),
         # #(store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
         # #(call_script, "script_diplomacy_start_war_between_kingdoms", ":quest_target_faction", ":quest_giver_faction", 1),
         # (call_script, "script_succeed_quest", "qst_raid_caravan_to_start_war"),
       # (try_end),
     # (try_end),

]),

#script_event_player_captured_as_prisoner
("event_player_captured_as_prisoner",
    [   #Removing followers of the player
        (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
          (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
          (gt, ":party_no", 0),
          (party_slot_eq, ":party_no", slot_party_commander_party, "p_main_party"),
          (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
          (assign, "$g_recalculate_ais", 1),
        (try_end),
]),

#NPC morale both returns a string and reg0 as the morale value
("npc_morale",
 [       (store_script_param_1, ":npc"),

        (troop_get_slot, ":morality_grievances", ":npc", slot_troop_morality_penalties),
        (troop_get_slot, ":personality_grievances", ":npc", slot_troop_personalityclash_penalties),
        (party_get_morale, ":party_morale", "p_main_party"),

        (store_sub, ":troop_morale", ":party_morale", ":morality_grievances"),
        (val_sub, ":troop_morale", ":personality_grievances"),
        (val_add, ":troop_morale", 50),

        (assign, reg8, ":troop_morale"),
        (val_mul, ":troop_morale", 3),
        (val_div, ":troop_morale", 4),
        (val_clamp, ":troop_morale", 0, 100),

        (assign, reg5, ":party_morale"),
        (assign, reg6, ":morality_grievances"),
        (assign, reg7, ":personality_grievances"),
        (assign, reg9, ":troop_morale"),

#        (str_store_troop_name, s11, ":npc"),
#        (display_message, "@{s11}'s morale = PM{reg5} + 50 - MG{reg6} - PG{reg7} = {reg8} x 0.75 = {reg9}"),

        (try_begin),(lt, ":morality_grievances", 3),(str_store_string, 7, "str_happy"),
        (else_try) ,(lt, ":morality_grievances",15),(str_store_string, 7, "str_content"),
        (else_try) ,(lt, ":morality_grievances",30),(str_store_string, 7, "str_concerned"),
        (else_try) ,(lt, ":morality_grievances",45),(str_store_string, 7, "str_not_happy"),
        (else_try) ,                                (str_store_string, 7, "str_miserable"),
        (try_end),

        (try_begin),(lt, ":personality_grievances", 3),(str_store_string, 6, "str_happy"),
        (else_try) ,(lt, ":personality_grievances",15),(str_store_string, 6, "str_content"),
        (else_try) ,(lt, ":personality_grievances",30),(str_store_string, 6, "str_concerned"),
        (else_try) ,(lt, ":personality_grievances",45),(str_store_string, 6, "str_not_happy"),
        (else_try) ,                                   (str_store_string, 6, "str_miserable"),
        (try_end),

        (try_begin),(gt,":troop_morale",80),(str_store_string,8, "str_happy"    ),(str_store_string, 63, "str_bar_enthusiastic"),
        (else_try) ,(gt,":troop_morale",60),(str_store_string,8, "str_content"  ),(str_store_string, 63, "str_bar_content"),
        (else_try) ,(gt,":troop_morale",40),(str_store_string,8, "str_concerned"),(str_store_string, 63, "str_bar_weary"),
        (else_try) ,(gt,":troop_morale",20),(str_store_string,8, "str_not_happy"),(str_store_string, 63, "str_bar_disgruntled"),
        (else_try) ,                        (str_store_string,8, "str_miserable"),(str_store_string, 63, "str_bar_miserable"),
        (try_end),

        (str_store_string, 21, "str_npc_morale_report"),
        (assign, reg0, ":troop_morale"),
 ]),
#NPC morale both returns a string and reg0 as the morale value

# "script_retire_companion"
("retire_companion",
 [   (store_script_param_1, ":npc"),
    (store_script_param_2, ":length"),

    (remove_member_from_party, ":npc", "p_main_party"),
    (troop_set_slot, ":npc", slot_troop_personalityclash_penalties, 0),
    (troop_set_slot, ":npc", slot_troop_morality_penalties, 0),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (store_add, ":return_renown", ":renown", ":length"),
    (troop_set_slot, ":npc", slot_troop_occupation, slto_retirement),
    (troop_set_slot, ":npc", slot_troop_return_renown, ":return_renown"),
    ]),

#script_reduce_companion_morale_for_clash
#script_calculate_ransom_amount_for_troop
# INPUT: arg1 = troop_no for companion1 arg2 = troop_no for companion2 arg3 = slot_for_clash_state
# slot_for_clash_state means: 1=give full penalty to companion1; 2=give full penalty to companion2; 3=give penalty equally
("reduce_companion_morale_for_clash",[
    (store_script_param, ":companion_1", 1),
    (store_script_param, ":companion_2", 2),
    (store_script_param, ":slot_for_clash_state", 3),

    (troop_get_slot, ":clash_state", ":companion_1", ":slot_for_clash_state"),
    (troop_get_slot, ":grievance_1", ":companion_1", slot_troop_personalityclash_penalties),
    (troop_get_slot, ":grievance_2", ":companion_2", slot_troop_personalityclash_penalties),
    (try_begin),
      (eq, ":clash_state", pclash_penalty_to_self),
      (val_add, ":grievance_1", 5),
    (else_try),
      (eq, ":clash_state", pclash_penalty_to_other),
      (val_add, ":grievance_2", 5),
    (else_try),
      (eq, ":clash_state", pclash_penalty_to_both),
      (val_add, ":grievance_1", 3),
      (val_add, ":grievance_2", 3),
    (try_end),
    (troop_set_slot, ":companion_1", slot_troop_personalityclash_penalties, ":grievance_1"),
    (troop_set_slot, ":companion_2", slot_troop_personalityclash_penalties, ":grievance_2"),
]),

#script_calculate_ransom_amount_for_troop
# INPUT: arg1 = troop_no
# OUTPUT: reg0 = ransom_amount
("calculate_ransom_amount_for_troop",
    [(store_script_param, ":troop_no", 1),
     (store_troop_faction, ":faction_no", ":troop_no"),
     (assign, ":ransom_amount", 400),
     (try_begin),
       (faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
       (val_add, ":ransom_amount", 4000),
     (try_end),

     (assign, ":num_center_points", 0),
     (try_for_range, ":cur_center", centers_begin, centers_end),
       (party_is_active, ":cur_center"), #TLD
       (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
       (try_begin),
         (party_slot_eq, ":cur_center", slot_party_type, spt_town),
         (val_add, ":num_center_points", 4),
       (else_try),
         (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
         (val_add, ":num_center_points", 2),
       (else_try),
         (val_add, ":num_center_points", 1),
       (try_end),
     (try_end),
     (val_mul, ":num_center_points", 500),
     (val_add, ":ransom_amount", ":num_center_points"),
     (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
     (val_mul, ":renown", 2),
     (val_add, ":ransom_amount", ":renown"),
     (store_mul, ":ransom_max_amount", ":ransom_amount", 3),
     (val_div, ":ransom_max_amount", 2),
     (store_random_in_range, ":random_ransom_amount", ":ransom_amount", ":ransom_max_amount"),
     (val_div, ":random_ransom_amount", 100),
     (val_mul, ":random_ransom_amount", 100),
     (assign, reg0, ":random_ransom_amount"),
]),  

# script_cf_check_hero_can_escape_from_player
# Input: arg1 = troop_no
# Output: none (can fail)
("cf_check_hero_can_escape_from_player",
    [   #(store_script_param_1, ":troop_no"),
        # (assign, ":quest_target", 0),
        # (try_begin),
          # (check_quest_active, "qst_persuade_lords_to_make_peace"),
          # (this_or_next|quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
          # (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
          # (assign, ":quest_target", 1),
        # (try_end),
        # (eq, ":quest_target", 0),
        
        (assign, ":always_capture", 0),
        (try_begin),
          (check_quest_active, "qst_capture_enemy_hero"),
          (assign, ":has_prisoner", 0),
          (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
          (try_for_range, ":i_stack", 0, ":num_stacks"),
            (party_prisoner_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
            (troop_is_hero, ":stack_troop"),
            (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
            (assign, ":has_prisoner", 1),
          (try_end),
          (eq, ":has_prisoner", 0),
          (assign, ":always_capture", 1),
        (try_end),
        (eq, ":always_capture", 0),
        
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", hero_escape_after_defeat_chance),
]),

# script_cf_party_remove_random_regular_troop
# Input: arg1 = party_no
# Output: troop_id that has been removed (can fail)
("cf_party_remove_random_regular_troop",
    [(store_script_param_1, ":party_no"),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":num_troops", 0),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_add, ":num_troops", ":stack_size"),
     (try_end),
     (assign, reg0, -1),
     (gt, ":num_troops", 0),
     (store_random_in_range, ":random_troop", 0, ":num_troops"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_sub, ":random_troop", ":stack_size"),
       (lt, ":random_troop", 0),
       (assign, ":num_stacks", 0), #break
       (party_remove_members, ":party_no", ":stack_troop", 1),
       (assign, reg0, ":stack_troop"),
     (try_end),
]),

# script_cf_party_select_random_regular_troop
# Input: arg1 = party_no
# Output: troop_id that has been removed (can fail)
("cf_party_select_random_regular_troop",
    [(store_script_param_1, ":party_no"),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":num_troops", 0),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_add, ":num_troops", ":stack_size"),
     (try_end),
     (assign, reg0, -1),
     (gt, ":num_troops", 0),
     (store_random_in_range, ":random_troop", 0, ":num_troops"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_sub, ":random_troop", ":stack_size"),
       (lt, ":random_troop", 0),
       (assign, ":num_stacks", 0), #break
       (assign, reg0, ":stack_troop"),
     (try_end),
]),

# script_place_player_banner_near_inventory
("place_player_banner_near_inventory",
    [   #normal_banner_begin
        (troop_get_slot, ":troop_banner_object", "trp_player", slot_troop_banner_scene_prop),
        #custom_banner_begin
#        (troop_get_slot, ":flag_spr", "trp_player", slot_troop_custom_banner_flag_type),
     (try_begin),
        #normal_banner_begin
       (gt, ":troop_banner_object", 0),
       (scene_prop_get_instance, ":flag_object", ":troop_banner_object", 0),
        #custom_banner_begin
#       (ge, ":flag_spr", 0),
#       (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
#       (scene_prop_get_instance, ":flag_object", ":flag_spr", 0),
       (try_begin),
         (ge, ":flag_object", 0),
         (get_player_agent_no, ":player_agent"),
         (agent_get_look_position, pos1, ":player_agent"),
         (position_move_y, pos1, -500),
         (position_rotate_z, pos1, 180),
         (position_set_z_to_ground_level, pos1),
         (position_move_z, pos1, 300),
         (prop_instance_set_position, ":flag_object", pos1),
       (try_end),
       (scene_prop_get_instance, ":pole_object", "spr_banner_pole", 0),
       (try_begin),
         (ge, ":pole_object", 0),
         (position_move_z, pos1, -320),
         (prop_instance_set_position, ":pole_object", pos1),
       (try_end),
     (else_try),
       (init_position, pos1),
       (position_move_z, pos1, -1000000),
       (scene_prop_get_instance, ":flag_object", banner_scene_props_begin, 0),
       (try_begin),
         (ge, ":flag_object", 0),
         (prop_instance_set_position, ":flag_object", pos1),
       (try_end),
       (scene_prop_get_instance, ":pole_object", "spr_banner_pole", 0),
       (try_begin),
         (ge, ":pole_object", 0),
         (prop_instance_set_position, ":pole_object", pos1),
       (try_end),
     (try_end),
]),

# script_place_player_banner_near_inventory_bms
("place_player_banner_near_inventory_bms",
    [           #normal_banner_begin
        (troop_get_slot, ":troop_banner_object", "trp_player", slot_troop_banner_scene_prop),
                #custom_banner_begin
#      (troop_get_slot, ":flag_spr", "trp_player", slot_troop_custom_banner_flag_type),
     (try_begin),
                #normal_banner_begin
       (gt, ":troop_banner_object", 0),
       (replace_scene_props, banner_scene_props_begin, ":troop_banner_object"),
                #custom_banner_begin
#       (ge, ":flag_spr", 0),
#       (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
#       (replace_scene_props, banner_scene_props_begin, ":flag_spr"),
     (try_end),
]),

# script_stay_captive_for_hours
# Input: arg1 = num_hours
# Output: none
("stay_captive_for_hours",
    [(store_script_param, ":num_hours", 1),
     (store_current_hours, ":cur_hours"),
     (val_add, ":cur_hours", ":num_hours"),
     (val_max, "$g_check_autos_at_hour", ":cur_hours"),
     (val_add, ":num_hours", 1),
     (rest_for_hours, ":num_hours", 0, 0),
]),

# script_set_parties_around_player_ignore_player
# Input: arg1 = ignore_range, arg2 = num_hours_to_ignore
("set_parties_around_player_ignore_player",
    [(store_script_param, ":ignore_range", 1),
     (store_script_param, ":num_hours", 2),
     (try_for_parties, ":party_no"),
       (party_is_active, ":party_no"),
       (store_distance_to_party_from_party, ":dist", "p_main_party", ":party_no"),
       (lt, ":dist", ":ignore_range"),
       (party_ignore_player, ":party_no", ":num_hours"),
     (try_end),
]),

# script_randomly_make_prisoner_heroes_escape_from_party
# Input: arg1 = party_no, arg2 = escape_chance_mul_1000
("randomly_make_prisoner_heroes_escape_from_party",
    [(store_script_param, ":party_no", 1),
     (store_script_param, ":escape_chance", 2),
     # (assign, ":quest_troop_1", -1),
     # (assign, ":quest_troop_2", -1),
     # (try_begin),
       # (check_quest_active, "qst_rescue_lord_by_replace"),
       # (quest_get_slot, ":quest_troop_1", "qst_rescue_lord_by_replace", slot_quest_target_troop),
     # (try_end),
     # (try_begin),
       # (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
       # (quest_get_slot, ":quest_troop_2", "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop),
     # (try_end),
     (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
     (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
       (party_prisoner_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (troop_is_hero, ":stack_troop"),
       # (neq, ":stack_troop", ":quest_troop_1"),
       # (neq, ":stack_troop", ":quest_troop_2"),
       (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
       (store_random_in_range, ":random_no", 0, 1000),
       (lt, ":random_no", ":escape_chance"),
       (party_remove_prisoners, ":party_no", ":stack_troop", 1),
       (call_script, "script_remove_troop_from_prison", ":stack_troop"),
       (str_store_troop_name_link, s1, ":stack_troop"),
       (try_begin),
         (eq, ":party_no", "p_main_party"),
         (str_store_string, s2, "@your party"),
       (else_try),
         (str_store_party_name, s2, ":party_no"),
       (try_end),
       (assign, reg0, 0),
       (try_begin),
         (this_or_next|eq, ":party_no", "p_main_party"),
         (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
         (assign, reg0, 1),
       (try_end),
       (store_troop_faction, ":troop_faction", ":stack_troop"),
       (str_store_faction_name_link, s3, ":troop_faction"),
       (display_message, "@{reg0?One of your prisoners, :}{s1} of {s3} has escaped from captivity!"),
     (try_end),
]),

# script_draw_banner_to_region
# Input: arg1 = troop_no, arg2 = center_pos_x, arg3 = center_pos_y, arg4 = width, arg5 = height, arg6 = stretch_width, arg7 = stretch_height, arg8 = default_scale, arg9 = max_charge_scale, arg10 = drawn_item_type
# drawn_item_type is 0 for banners, 1 for shields, 2 for heater shield, 3 for armor
# arguments will be used as fixed point values
("draw_banner_to_region",
    [ (store_script_param, ":troop_no", 1),
      (store_script_param, ":center_pos_x", 2),
      (store_script_param, ":center_pos_y", 3),
      (store_script_param, ":width", 4),
      (store_script_param, ":height", 5),
      (store_script_param, ":stretch_width", 6),
      (store_script_param, ":stretch_height", 7),
      (store_script_param, ":default_scale", 8),
      (store_script_param, ":max_charge_scale", 9),
      (store_script_param, ":drawn_item_type", 10),

      (troop_get_slot, ":bg_type", ":troop_no", slot_troop_custom_banner_bg_type),
      (val_add, ":bg_type", custom_banner_backgrounds_begin),
      (troop_get_slot, ":bg_color_1", ":troop_no", slot_troop_custom_banner_bg_color_1),
      (troop_get_slot, ":bg_color_2", ":troop_no", slot_troop_custom_banner_bg_color_2),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (troop_get_slot, ":positioning", ":troop_no", slot_troop_custom_banner_positioning),
      (call_script, "script_get_troop_custom_banner_num_positionings", ":troop_no"),
      (assign, ":num_positionings", reg0),
      (val_mod, ":positioning", ":num_positionings"),

      (init_position, pos2),
      (position_set_x, pos2, ":width"),
      (position_set_y, pos2, ":height"),
      (assign, ":default_value", 1),
      (convert_to_fixed_point, ":default_value"),
      (position_set_z, pos2, ":default_value"),

      (init_position, pos1),
      (position_set_x, pos1, ":center_pos_x"),
      (position_set_y, pos1, ":center_pos_y"),
      (position_move_z, pos1, -20),

      (init_position, pos3),
      (position_set_x, pos3, ":default_scale"),
      (position_set_y, pos3, ":default_scale"),
      (position_set_z, pos3, ":default_value"),
      (try_begin),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_bg"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg01"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg02"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg03"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg08"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg09"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg10"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg11"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg12"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg13"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg16"),
        (eq, ":bg_type", "mesh_custom_banner_fg17"),
        (cur_tableau_add_mesh_with_scale_and_vertex_color, ":bg_type", pos1, pos2, 0, ":bg_color_1"),
      (else_try),
        (cur_tableau_add_mesh_with_scale_and_vertex_color, ":bg_type", pos1, pos3, 0, ":bg_color_1"),
      (try_end),
      (position_move_z, pos1, -20),
      (position_move_x, pos2, ":width"),
      (position_move_y, pos2, ":height"),
      (cur_tableau_add_mesh_with_scale_and_vertex_color, "mesh_custom_banner_bg", pos1, pos2, 0, ":bg_color_2"),
      
      (assign, ":charge_stretch", ":stretch_width"),
      (val_min, ":charge_stretch", ":stretch_height"),
      (val_min, ":charge_stretch", ":max_charge_scale"),
      (call_script, "script_get_custom_banner_charge_type_position_scale_color", "trp_player", ":positioning"),

      (try_begin),
        (this_or_next|eq, ":drawn_item_type", 2), #heater shield
        (eq, ":drawn_item_type", 3), #armor
        (assign, ":change_center_pos", 0),
        (try_begin),
          (eq, ":num_charges", 1),
          (assign, ":change_center_pos", 1),
        (else_try),
          (eq, ":num_charges", 2),
          (eq, ":positioning", 1),
          (assign, ":change_center_pos", 1),
        (else_try),
          (eq, ":num_charges", 3),
          (eq, ":positioning", 1),
          (assign, ":change_center_pos", 1),
        (try_end),
        (try_begin),
          (eq, ":change_center_pos", 1),
          (val_add, ":center_pos_y", 30),
        (try_end),
      (try_end),
      
      (try_begin),
        (ge, ":num_charges", 1),
        (val_mul, reg1, ":charge_stretch"),
        (val_div, reg1, 10000),
        (position_get_x, ":x", pos0),
        (position_get_y, ":y", pos0),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos0, ":x"),
        (position_set_y, pos0, ":y"),
        (assign, ":scale_value", reg1),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg0, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg0, 256), #remove orientation flags
        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg0, pos0, pos4, 0, reg2),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 2),
        (val_mul, reg4, ":charge_stretch"),
        (val_div, reg4, 10000),
        (position_get_x, ":x", pos1),
        (position_get_y, ":y", pos1),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos1, ":x"),
        (position_set_y, pos1, ":y"),

        (assign, ":scale_value", reg4),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg3, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg3, 256), #remove orientation flags

        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg3, pos1, pos4, 0, reg5),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 3),
        (val_mul, reg7, ":charge_stretch"),
        (val_div, reg7, 10000),
        (position_get_x, ":x", pos2),
        (position_get_y, ":y", pos2),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos2, ":x"),
        (position_set_y, pos2, ":y"),

        (assign, ":scale_value", reg7),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg6, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg6, 256), #remove orientation flags

        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg6, pos2, pos4, 0, reg8),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 4),
        (val_mul, reg10, ":charge_stretch"),
        (val_div, reg10, 10000),
        (position_get_x, ":x", pos3),
        (position_get_y, ":y", pos3),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos3, ":x"),
        (position_set_y, pos3, ":y"),

        (assign, ":scale_value", reg10),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg9, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg9, 256), #remove orientation flags
        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg9, pos3, pos4, 0, reg11),
      (try_end),
]),

# script_get_troop_custom_banner_num_positionings
# Input: arg1 = troop_no
# Output: reg0 = num_positionings
("get_troop_custom_banner_num_positionings",
    [ (store_script_param, ":troop_no", 1),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (try_begin),
        (eq, ":num_charges", 1),
        (assign, ":num_positionings", 2),
      (else_try),
        (eq, ":num_charges", 2),
        (assign, ":num_positionings", 4),
      (else_try),
        (eq, ":num_charges", 3),
        (assign, ":num_positionings", 6),
      (else_try),
        (assign, ":num_positionings", 2),
      (try_end),
      (assign, reg0, ":num_positionings"),
]),

# script_get_custom_banner_charge_type_position_scale_color
# Input: arg1 = troop_no, arg2 = positioning_index
# Output: reg0 = type_1
#         reg1 = scale_1
#         reg2 = color_1
#         reg3 = type_2
#         reg4 = scale_2
#         reg5 = color_2
#         reg6 = type_3
#         reg7 = scale_3
#         reg8 = color_3
#         reg9 = type_4
#         reg10 = scale_4
#         reg11 = color_4
("get_custom_banner_charge_type_position_scale_color",[
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":positioning", 2),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (init_position, pos0),
      (init_position, pos1),
      (init_position, pos2),
      (init_position, pos3),

      (troop_get_slot, reg0, ":troop_no", slot_troop_custom_banner_charge_type_1),
      (val_add, reg0, custom_banner_charges_begin),
      (troop_get_slot, reg2, ":troop_no", slot_troop_custom_banner_charge_color_1),
      (troop_get_slot, reg3, ":troop_no", slot_troop_custom_banner_charge_type_2),
      (val_add, reg3, custom_banner_charges_begin),
      (troop_get_slot, reg5, ":troop_no", slot_troop_custom_banner_charge_color_2),
      (troop_get_slot, reg6, ":troop_no", slot_troop_custom_banner_charge_type_3),
      (val_add, reg6, custom_banner_charges_begin),
      (troop_get_slot, reg8, ":troop_no", slot_troop_custom_banner_charge_color_3),
      (troop_get_slot, reg9, ":troop_no", slot_troop_custom_banner_charge_type_4),
      (val_add, reg9, custom_banner_charges_begin),
      (troop_get_slot, reg11, ":troop_no", slot_troop_custom_banner_charge_color_4),

      (try_begin),
        (eq, ":num_charges", 1),
        (try_begin),
          (eq, ":positioning", 0),
          (assign, reg1, 100),
        (else_try),
          (assign, reg1, 50),
        (try_end),
      (else_try),
        (eq, ":num_charges", 2),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_y, pos0, 25),
          (position_set_y, pos1, -25),
          (assign, reg1, 40),
          (assign, reg4, 40),
        (else_try),
          (eq, ":positioning", 1),
          (position_set_x, pos0, -25),
          (position_set_x, pos1, 25),
          (assign, reg1, 40),
          (assign, reg4, 40),
        (else_try),
          (eq, ":positioning", 2),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
        (else_try),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, -25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, 25),
          (assign, reg1, 50),
          (assign, reg4, 50),
        (try_end),
      (else_try),
        (eq, ":num_charges", 3),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_y, pos0, 33),
          (position_set_y, pos2, -33),
          (assign, reg1, 30),
          (assign, reg4, 30),
          (assign, reg7, 30),
        (else_try),
          (eq, ":positioning", 1),
          (position_set_x, pos0, -33),
          (position_set_x, pos2, 33),
          (assign, reg1, 30),
          (assign, reg4, 30),
          (assign, reg7, 30),
        (else_try),
          (eq, ":positioning", 2),
          (position_set_x, pos0, -30),
          (position_set_y, pos0, 30),
          (position_set_x, pos2, 30),
          (position_set_y, pos2, -30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
        (else_try),
          (eq, ":positioning", 3),
          (position_set_x, pos0, -30),
          (position_set_y, pos0, -30),
          (position_set_x, pos2, 30),
          (position_set_y, pos2, 30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
        (else_try),
          (eq, ":positioning", 4),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, -25),
          (position_set_y, pos1, 25),
          (position_set_x, pos2, 25),
          (position_set_y, pos2, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
        (else_try),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_y, pos1, -25),
          (position_set_x, pos2, 25),
          (position_set_y, pos2, 25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
        (try_end),
      (else_try),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, 25),
          (position_set_x, pos2, -25),
          (position_set_y, pos2, -25),
          (position_set_x, pos3, 25),
          (position_set_y, pos3, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
          (assign, reg10, 50),
        (else_try),
          (position_set_y, pos0, 30),
          (position_set_x, pos1, -30),
          (position_set_x, pos2, 30),
          (position_set_y, pos3, -30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
          (assign, reg10, 35),
        (try_end),
      (try_end),
]),

# script_get_random_custom_banner
# Input: arg1 = troop_no
("get_random_custom_banner",[
      (store_script_param, ":troop_no", 1),
      (store_random_in_range, ":num_charges", 1, 5),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_num_charges, ":num_charges"),
      (store_random_in_range, ":random_color_index", 0, 42),
      (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
      (assign, ":color_1", reg0),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_color_1, ":color_1"),
      (assign, ":end_cond", 1),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_color_index", 0, 42),
        (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
        (assign, ":color_2", reg0),
        (try_begin),
          (call_script, "script_cf_check_color_visibility", ":color_1", ":color_2"),
          (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_color_2, ":color_2"),
        (else_try),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (assign, ":end_cond", 4),
      (assign, ":cur_charge", 0),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_color_index", 0, 42),
        (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
        (assign, ":charge_color", reg0),
        (try_begin),
          (call_script, "script_cf_check_color_visibility", ":charge_color", ":color_1"),
          (call_script, "script_cf_check_color_visibility", ":charge_color", ":color_2"),
          (store_add, ":cur_slot", ":cur_charge", slot_troop_custom_banner_charge_color_1),
          (troop_set_slot, ":troop_no", ":cur_slot", ":charge_color"),
          (store_random_in_range, ":random_charge", custom_banner_charges_begin, custom_banner_charges_end),
          (val_sub, ":random_charge", custom_banner_charges_begin),
          (store_add, ":cur_slot", ":cur_charge", slot_troop_custom_banner_charge_type_1),
          (troop_set_slot, ":troop_no", ":cur_slot", ":random_charge"),
          (val_add, ":cur_charge", 1),
        (else_try),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (store_random_in_range, ":random_bg", custom_banner_backgrounds_begin, custom_banner_backgrounds_end),
      (val_sub, ":random_bg", custom_banner_backgrounds_begin),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_type, ":random_bg"),
      (store_random_in_range, ":random_flag", custom_banner_flag_types_begin, custom_banner_flag_types_end),
      (val_sub, ":random_flag", custom_banner_flag_types_begin),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_flag_type, ":random_flag"),
      (store_random_in_range, ":random_positioning", 0, 4),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_positioning, ":random_positioning"),
]),

# script_get_custom_banner_color_from_index
# Input: arg1 = color_index
# Output: reg0 = color
("get_custom_banner_color_from_index",[
      (store_script_param, ":color_index", 1),

      (assign, ":cur_color", 0xFF000000), (assign, ":red", 0x00),(assign, ":green", 0x00),(assign, ":blue", 0x00),
      (store_mod, ":mod_i_color", ":color_index", 7),
      (try_begin),(eq, ":mod_i_color", 0),                                                (assign, ":blue", 0xFF),
      (else_try) ,(eq, ":mod_i_color", 1),(assign, ":red", 0xEE),
      (else_try) ,(eq, ":mod_i_color", 2),(assign, ":red", 0xFB),(assign, ":green", 0xAC),
      (else_try) ,(eq, ":mod_i_color", 3),(assign, ":red", 0x5F),                         (assign, ":blue", 0xFF),
      (else_try) ,(eq, ":mod_i_color", 4),(assign, ":red", 0x05),(assign, ":green", 0x44),
      (else_try) ,(eq, ":mod_i_color", 5),(assign, ":red", 0xEE),(assign, ":green", 0xEE),(assign, ":blue", 0xEE),
      (else_try) ,                        (assign, ":red", 0x22),(assign, ":green", 0x22),(assign, ":blue", 0x22),
      (try_end),

      (store_div, ":cur_tone", ":color_index", 7),
      (store_sub, ":cur_tone", 8, ":cur_tone"),
      (val_mul, ":red"  , ":cur_tone"),(val_div, ":red"  , 8),
      (val_mul, ":green", ":cur_tone"),(val_div, ":green", 8),
      (val_mul, ":blue" , ":cur_tone"),(val_div, ":blue" , 8),
      (val_mul, ":green", 0x100),
      (val_mul, ":red", 0x10000),
      (val_add, ":cur_color", ":blue"),
      (val_add, ":cur_color", ":green"),
      (val_add, ":cur_color", ":red"),
      (assign, reg0, ":cur_color"),
]),

# script_cf_check_color_visibility
# Input: arg1 = color_1, arg2 = color_2
("cf_check_color_visibility",[
      (store_script_param, ":color_1", 1),
      (store_script_param, ":color_2", 2),
      (store_mod, ":blue_1", ":color_1", 256),
      (store_div, ":green_1", ":color_1", 256),
      (val_mod, ":green_1", 256),
      (store_div, ":red_1", ":color_1", 256 * 256),
      (val_mod, ":red_1", 256),
      (store_mod, ":blue_2", ":color_2", 256),
      (store_div, ":green_2", ":color_2", 256),
      (val_mod, ":green_2", 256),
      (store_div, ":red_2", ":color_2", 256 * 256),
      (val_mod, ":red_2", 256),
      (store_sub, ":red_dif", ":red_1", ":red_2"),
      (val_abs, ":red_dif"),
      (store_sub, ":green_dif", ":green_1", ":green_2"),
      (val_abs, ":green_dif"),
      (store_sub, ":blue_dif", ":blue_1", ":blue_2"),
      (val_abs, ":blue_dif"),
      (assign, ":max_dif", 0),
      (val_max, ":max_dif", ":red_dif"),
      (val_max, ":max_dif", ":green_dif"),
      (val_max, ":max_dif", ":blue_dif"),
      (ge, ":max_dif", 64),
]),

# script_get_next_active_kingdom
# Input: arg1 = faction_no
# Output: reg0 = faction_no (does not choose player faction)
("get_next_active_kingdom",[
      (store_script_param, ":faction_no", 1),
      (assign, ":end_cond", kingdoms_end),
      (try_for_range, ":unused", kingdoms_begin, ":end_cond"),
        (val_add, ":faction_no", 1),
        (try_begin),
          (ge, ":faction_no", kingdoms_end),
          (assign, ":faction_no", kingdoms_begin),
        (try_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (assign, ":end_cond", 0),
      (try_end),
      (assign, reg0, ":faction_no"),
]),

# script_store_average_center_value_per_faction
# Output: sets $g_average_center_value_per_faction
("store_average_center_value_per_faction",[
      (store_sub, ":num_towns", centers_end, centers_begin),
      (assign, ":num_factions", 0),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_add, ":num_factions", 1),
      (try_end),
      (val_max, ":num_factions", 1),
      (store_mul, "$g_average_center_value_per_faction", ":num_towns", 2),
      (val_mul, "$g_average_center_value_per_faction", 10),
      (val_div, "$g_average_center_value_per_faction", ":num_factions"),
]),

# script_remove_cattles_if_herd_is_close_to_party
# Input: arg1 = party_no, arg2 = maximum_number_of_cattles_required
# Output: reg0 = number_of_cattles_removed
("remove_cattles_if_herd_is_close_to_party",
    [ (store_script_param, ":party_no", 1),
      (store_script_param, ":max_req", 2),
      (assign, ":cur_req", ":max_req"),
      (try_for_parties, ":cur_party"),
        (gt, ":cur_req", 0),
        (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
        (store_distance_to_party_from_party, ":dist", ":cur_party", ":party_no"),
        (lt, ":dist", 3),
        #Do not use the quest herd
        (assign, ":subcontinue", 1),
        (try_begin),
          (check_quest_active, "qst_move_cattle_herd"),
          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
          (assign, ":subcontinue", 0),
        (try_end),
        (eq, ":subcontinue", 1),
        (party_count_companions_of_type, ":num_cattle", ":cur_party", "trp_cattle"),
        (try_begin),
          (le, ":num_cattle", ":cur_req"),
          (assign, ":num_added", ":num_cattle"),
          (remove_party, ":cur_party"),
        (else_try),
          (assign, ":num_added", ":cur_req"),
          (party_remove_members, ":cur_party", "trp_cattle", ":cur_req"),
        (try_end),
        (val_sub, ":cur_req", ":num_added"),
        (try_begin),
          (party_slot_eq, ":party_no", slot_party_type, spt_village),
          (party_get_slot, ":village_cattle_amount", ":party_no", slot_village_number_of_cattle),
          (val_add, ":village_cattle_amount", ":num_added"),
          (party_set_slot, ":party_no", slot_village_number_of_cattle, ":village_cattle_amount"),
        (try_end),
        (assign, reg3, ":num_added"),
        (str_store_party_name_link, s1, ":party_no"),
        (display_message, "@You brought {reg3} heads of cattle to {s1}."),
      (try_end),
      (store_sub, reg0, ":max_req", ":cur_req"),
]),  

("lord_comment_to_s43",[
    (store_script_param, ":lord", 1),
    (store_script_param, ":default_string", 2),
    (troop_get_slot,":reputation", ":lord", slot_lord_reputation_type),
    (val_add,":reputation", ":default_string"),
    (str_store_string,43,":reputation"),
]),

#Troop Commentaries begin

# script_add_log_entry
# Input: arg1 = entry_type, arg2 = event_actor, arg3 = center_object, arg4 = troop_object, arg5 = faction_object
# Output: none
("add_log_entry",[
	(store_script_param, ":entry_type", 1),
	(store_script_param, ":actor", 2),
	(store_script_param, ":center_object", 3),
	(store_script_param, ":troop_object", 4),
	(store_script_param, ":faction_object", 5),
	(assign, ":center_object_lord", -1),
	(assign, ":center_object_faction", -1),
	(assign, ":troop_object_faction", -1),
	(try_begin),
		(gt, ":center_object", 0),
		(party_get_slot, ":center_object_lord", ":center_object", slot_town_lord),
		(store_faction_of_party, ":center_object_faction", ":center_object"),
	(try_end),
	(try_begin),
		(ge, ":troop_object", 0),
		(store_troop_faction, ":troop_object_faction", ":troop_object"),
	(try_end),

	(val_add, "$num_log_entries", 1),

	(store_current_hours, ":entry_time"),
	(troop_set_slot, "trp_log_array_entry_type",            "$num_log_entries", ":entry_type"),
	(troop_set_slot, "trp_log_array_entry_time",            "$num_log_entries", ":entry_time"),
	(troop_set_slot, "trp_log_array_actor",                 "$num_log_entries", ":actor"),
	(troop_set_slot, "trp_log_array_center_object",         "$num_log_entries", ":center_object"),
	(troop_set_slot, "trp_log_array_center_object_lord",    "$num_log_entries", ":center_object_lord"),
	(troop_set_slot, "trp_log_array_center_object_faction", "$num_log_entries", ":center_object_faction"),
	(troop_set_slot, "trp_log_array_troop_object",          "$num_log_entries", ":troop_object"),
	(troop_set_slot, "trp_log_array_troop_object_faction",  "$num_log_entries", ":troop_object_faction"),
	(troop_set_slot, "trp_log_array_faction_object",        "$num_log_entries", ":faction_object"),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(assign, reg3, "$num_log_entries"), 
		(assign, reg4, ":entry_type"),
		(display_message, "@Log entry {reg3}: type {reg4}"), 
		(try_begin),
			(gt, ":center_object", 0),
			(str_store_party_name, s4, ":center_object"),
			(display_message, "@Center: {s4}"), 
		(try_end),      
		(try_begin),
			(gt, ":troop_object", 0),
			(str_store_troop_name, s4, ":troop_object"),
			(display_message, "@Troop: {s4}"), 
		(try_end),      
		(try_begin),
			(gt, ":center_object_lord", 0),
			(str_store_troop_name, s4, ":center_object_lord"),
			(display_message, "@Lord: {s4}"), 
		(try_end),
	(try_end),
	(try_begin),
		(this_or_next|gt, "$g_ally_party", 0),
		(eq, ":entry_type", logent_player_participated_in_siege),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(display_message, "@Ally party is present"),
		(try_end),
		(try_for_range, ":hero", kingdom_heroes_begin, kingdom_heroes_end),
			(party_count_companions_of_type, ":hero_present", "p_collective_friends", ":hero"),
			(gt, ":hero_present", 0),
			(troop_set_slot, ":hero", slot_troop_present_at_event, "$num_log_entries"),
			#         (store_sub, ":skip_up_to_here", "$num_log_entries", 1),
			#         (troop_set_slot, ":hero", slot_troop_last_comment_slot, ":skip_up_to_here"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, 4, ":hero"),
				(display_message, "@{s4} is present at event"),
			(try_end),
		(try_end),
	(try_end),
]),

# script_get_relevant_comment_for_log_entry
# Input: arg1 = log_entry_no, 
# Output: reg0 = comment_id; reg1 = relevance
# Notes: 50 is the default relevance.
# A comment with relevance less than 30 will always be skipped.
# A comment with relevance 75 or more will never be skipped.
# A comment with relevance 50 has about 50% chance to be skipped.
# If there is more than one comment that is not skipped, the system will randomize their relevance values, and then choose the highest one.
# Also note that the relevance of events decreases as time passes. After three months, relevance reduces to 50%, after 6 months, 25%, etc...
("get_relevant_comment_for_log_entry",
    [(store_script_param, ":log_entry_no", 1),
     
     (troop_get_slot, ":entry_type",            "trp_log_array_entry_type",            ":log_entry_no"),
     (troop_get_slot, ":entry_time",            "trp_log_array_entry_time",            ":log_entry_no"),
     (troop_get_slot, ":actor",                 "trp_log_array_actor",                 ":log_entry_no"),
##     (troop_get_slot, ":center_object",         "trp_log_array_center_object",         ":log_entry_no"),
     (troop_get_slot, ":center_object_lord",    "trp_log_array_center_object_lord",    ":log_entry_no"),
     (troop_get_slot, ":center_object_faction", "trp_log_array_center_object_faction", ":log_entry_no"),
     (troop_get_slot, ":troop_object",          "trp_log_array_troop_object",          ":log_entry_no"),
     (troop_get_slot, ":troop_object_faction",  "trp_log_array_troop_object_faction",  ":log_entry_no"),
     (troop_get_slot, ":faction_object",        "trp_log_array_faction_object",        ":log_entry_no"),

     (assign, ":relevance", 0),
     (assign, ":comment", -1), 
     (assign, ":suggested_relation_change", 0),

     (troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
     (store_current_hours, ":current_time"),
     (store_sub, ":entry_hours_elapsed", ":current_time", ":entry_time"),

#Post 0907 changes begin
     (assign, ":players_kingdom_relation", 0), ##the below is so that lords will not congratulate player on attacking neutrals
     (try_begin),
       (eq, "$cheat_mode", 1),
       (try_begin),
         (assign, reg5, ":log_entry_no"),
         (assign, reg6, ":entry_type"),
         (assign, reg8, ":entry_time"),

         (gt, "$players_kingdom", 0),
         (try_begin),
            (gt, ":troop_object_faction", 0),
            (store_relation, ":players_kingdom_relation", "$players_kingdom", ":troop_object_faction"),
            (assign, reg7, ":players_kingdom_relation"),
            (display_message, "@Event #{reg5}, type {reg6}, time {reg8}: player's kingdom relation to troop object = {reg7}"),
         (else_try),
            (gt, ":center_object_faction", 0),
            (store_relation, ":players_kingdom_relation", "$players_kingdom", ":center_object_faction"),
            (assign, reg7, ":players_kingdom_relation"),
            (display_message, "@Event #{reg5}, type {reg6}, time {reg8}: player's kingdom relation to center object faction = {reg7}"),
         (else_try),
            (gt, ":faction_object", 0),
            (store_relation, ":players_kingdom_relation", "$players_kingdom", ":faction_object"),
            (assign, reg7, ":players_kingdom_relation"),

            (display_message, "@Event #{reg5}, type {reg6}, time {reg8}: player's kingdom relation to faction object = {reg7}"),
         (else_try),
            (display_message, "@Event #{reg5}, type {reg6}, time {reg8}. No relevant kingdom relation"),
         (try_end),
       (else_try),
         (display_message, "@Event #{reg5}, type {reg6}, time {reg8}. Player unaffiliated"),
       (try_end),
     (try_end),

     (try_begin),
       (eq, ":entry_type", logent_game_start),
       (eq, "$g_talk_troop_met", 0),
       (is_between, "$g_talk_troop_faction_relation", -5, 5),
       (is_between, "$g_talk_troop_relation", -5, 5),

       (assign, ":relevance", 25),
#       (troop_get_slot, ":plyr_renown", "trp_player", slot_troop_renown),
#normal_banner_begin
       (troop_get_slot, ":banner", "trp_player", slot_troop_banner_scene_prop),
#custom_banner_begin
#       (troop_get_slot, ":banner", "trp_player", slot_troop_custom_banner_flag_type),
       # (store_random_in_range, ":renown_check", 100, 200),
       (try_begin),
          (eq, ":reputation", lrep_none),
          (gt, "$players_kingdom", 0),
          (assign, ":comment", "str_comment_intro_liege_affiliated"),
       # (else_try),
          # (gt, ":plyr_renown", ":renown_check"), 
          # (assign, ":comment", "str_comment_intro_famous_liege"),
          # (val_add, ":comment", ":reputation"),
       (else_try),
#normal_banner_begin
          (gt, ":banner", 0), 
#custom_banner_begin
#          (ge, ":banner", 0), 
          (assign, ":comment", "str_comment_intro_noble_liege"),
          (val_add, ":comment", ":reputation"),
       (else_try),
          (assign, ":comment", "str_comment_intro_common_liege"),
          (val_add, ":comment", ":reputation"),
       (try_end),
#Post 0907 changes end

     (else_try),
       (eq, ":entry_type", logent_village_raided),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 200),
         (assign, ":suggested_relation_change", -1),
         (assign, ":comment", "str_comment_you_raided_my_village_default"),
         (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_benevolent"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_cunning),
                (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_coldblooded"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_spiteful"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_raided_my_village_unfriendly_spiteful"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_raided_my_village_friendly"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_village_extorted),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 30),
         (assign, ":suggested_relation_change", -1),
         (assign, ":comment", "str_comment_you_robbed_my_village_default"),
         (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_cunning),
                (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_you_robbed_my_village_enemy_coldblooded"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_robbed_my_village_enemy"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_robbed_my_village_friendly_spiteful"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_robbed_my_village_friendly"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_caravan_accosted),
       (eq, ":actor", "trp_player"),
       (eq, ":faction_object", "$g_talk_troop_faction"),
       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
       (assign, ":relevance", 30),
       (assign, ":suggested_relation_change", -1),
       (assign, ":comment", "str_comment_you_accosted_my_caravan_default"),
       (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_accosted_my_caravan_enemy"),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_helped_peasants),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 40),
         (assign, ":suggested_relation_change", 0),
         (try_begin),
            (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_you_helped_villagers_benevolent"),
            (assign, ":suggested_relation_change", 1),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_friendly_cruel"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_unfriendly_spiteful"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_helped_villagers_friendly"),
         (else_try),
            (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_cruel"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
             (assign, ":comment", "str_comment_you_helped_villagers_default"),
         (try_end),
       (try_end),

###Combat events
     (else_try),
       (eq, ":entry_type", logent_castle_captured_by_player),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_captured_my_castle_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_captured_my_castle_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_captured_my_castle_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_spiteful"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (gt, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_friendly"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_unfriendly_spiteful"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_unfriendly"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied"),
         (assign, ":relevance", 75),
       (try_end),

#Post 0907 changes begin
     (else_try),
       (this_or_next|eq, ":entry_type", logent_lord_defeated_by_player),
            (eq, ":entry_type", logent_lord_helped_by_player),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_defeated_a_lord_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_defeated_a_lord_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_defeated_a_lord_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),        
           (assign, ":comment", "str_comment_we_defeated_a_lord_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_defeated_a_lord_upstanding"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_defeated_a_lord_default"),
           (assign, ":relevance", 150),
       (try_end),


     (else_try),
       (this_or_next|eq, ":entry_type", logent_castle_captured_by_player),
            (eq, ":entry_type", logent_player_participated_in_siege),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_siege_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_fought_in_siege_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_siege_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),        
           (assign, ":comment", "str_comment_we_fought_in_siege_quarrelsome"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_fought_in_siege_upstanding"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_fought_in_siege_default"),
           (assign, ":relevance", 150),
       (try_end),
     (else_try),
       (eq, ":entry_type", logent_player_participated_in_major_battle),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_major_battle_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_fought_in_major_battle_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),        
           (assign, ":comment", "str_comment_we_fought_in_major_battle_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_upstanding"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_default"),
           (assign, ":relevance", 150),
       (try_end),
     (else_try),
       (eq, ":entry_type", logent_lord_defeated_by_player),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_debauched),
             (eq, ":reputation", lrep_quarrelsome),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_me_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_pragmatic"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_chivalrous"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_spiteful"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_liege"),
         (assign, ":relevance", 70),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied"),
         (assign, ":relevance", 65),
       (try_end),
     (else_try),
       (eq, ":entry_type", logent_lord_defeated_by_player),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_debauched),
             (eq, ":reputation", lrep_quarrelsome),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_me_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_pragmatic"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_chivalrous"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_spiteful"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_liege"),
         (assign, ":relevance", 70),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied"),
         (assign, ":relevance", 65),
       (try_end),
     (else_try),
       (eq, ":entry_type", logent_lord_helped_by_player),
       (neq, ":troop_object", "$g_talk_troop"),
       (eq, ":troop_object_faction", "$g_talk_troop_faction"),
       (try_begin),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly"),
         (assign, ":relevance", 0),
       (else_try),
         (eq, ":reputation", lrep_none),
         (assign, ":comment", "str_comment_you_helped_my_ally_liege"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 3),
       (else_try),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_helped_my_ally_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_helped_my_ally_chivalrous"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_helped_my_ally_default"),
       (try_end),
     (else_try),
       (eq, ":entry_type", logent_player_defeated_by_lord),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_were_defeated_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_were_defeated_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_we_were_defeated_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_were_defeated_default"),
           (assign, ":relevance", 150),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_defeated_by_lord),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_benevolent"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_coldblooded"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_I_defeated_you_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_I_defeated_you_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (gt, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_friendly_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly_cruel"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (le, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (eq, ":reputation", lrep_selfrighteous),
         (assign, ":comment", "str_comment_you_were_defeated_allied_pitiless"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (eq, ":reputation", lrep_upstanding),
         (lt, "$g_talk_troop_relation", -15),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly_upstanding"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, "$g_talk_troop_relation", -10),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_were_defeated_allied"),
         (assign, ":relevance", 65),
       (try_end),
     (else_try),
       (eq, ":entry_type", logent_player_retreated_from_lord),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_you_abandoned_us_unfriendly_spiteful"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (eq, ":reputation", lrep_selfrighteous),        
           (assign, ":comment", "str_comment_you_abandoned_us_unfriendly_pitiless"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),        
           (assign, ":comment", "str_comment_you_abandoned_us_spiteful"),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (eq, ":reputation", lrep_martial),
           (assign, ":comment", "str_comment_you_abandoned_us_chivalrous"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -2),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_upstanding),
               (eq, ":reputation", lrep_goodnatured),        
           (assign, ":comment", "str_comment_you_abandoned_us_benefitofdoubt"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -1),
       (else_try),
           (assign, ":comment", "str_comment_you_abandoned_us_default"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -2),
       (try_end),
     (else_try),
       (this_or_next|eq, ":entry_type", logent_player_retreated_from_lord),
            (eq, ":entry_type", logent_player_retreated_from_lord_cowardly),
       (eq, ":troop_object", "$g_talk_troop"),
       (try_begin),
         (eq, "$cheat_mode", 1),
         (assign, reg7, ":entry_hours_elapsed"),
         (display_message, "@Elapsed hours: {reg7}"),
       (try_end),
       (gt, ":entry_hours_elapsed", 2),
       (try_begin),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_spiteful"),
         (assign, ":relevance", 25),
       (else_try),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_chivalrous"),
         (assign, ":relevance", 25),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_benevolent"),
         (assign, ":relevance", 25),
       (else_try),
         (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_coldblooded"),
         (assign, ":relevance", 25),
       (else_try),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy"),
         (assign, ":relevance", 25),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_retreated_from_lord_cowardly),
       (try_begin),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", 5),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_chivalrous"),
         (assign, ":relevance", 80),
         (assign, ":suggested_relation_change", -3),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_upstanding"),
         (assign, ":relevance", 80),
         (assign, ":suggested_relation_change", -1),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", 5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_spiteful"),
         (assign, ":relevance", 80),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_lord_defeated_but_let_go_by_player),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_let_me_go_spiteful"),
         (assign, ":relevance", 300),
         (assign, ":suggested_relation_change", -15),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (ge, "$g_talk_troop_faction_relation", 0),
         (assign, ":comment", "str_comment_you_let_me_go_default"),
         (assign, ":relevance", 300),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_upstanding),
         (assign, ":suggested_relation_change", 5),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy_chivalrous"),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
             (eq, ":reputation", lrep_cunning),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy_coldblooded"),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy"),
         (assign, ":suggested_relation_change", 1),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_chivalrous"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_upstanding"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_cunning),
             (eq, ":reputation", lrep_selfrighteous),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_coldblooded"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied"),
         (assign, ":relevance", 80),
       (try_end),

#Internal faction relations

     (else_try),
       (eq, ":entry_type", logent_pledged_allegiance),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":faction_object", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (assign, ":relevance", 200),
         (try_begin),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_martial),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_martial_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_martial),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_martial"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_quarrelsome),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_quarrelsome_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_quarrelsome),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_quarrelsome"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_selfrighteous_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_selfrighteous"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_cunning_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_cunning"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_debauched_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_debauched"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_goodnatured),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_goodnatured_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_goodnatured),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_goodnatured"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_upstanding_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_upstanding"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_fief_granted_village),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":faction_object", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (eq, ":faction_object", "$players_kingdom"),
         (assign, ":relevance", 110),
         (try_begin),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly_cruel"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly_cynical"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly"),
         (else_try),
            (is_between, "$g_talk_troop_relation", -5, 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_spiteful"),
            (assign, ":suggested_relation_change", -2),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_unfriendly_upstanding"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_unfriendly_spiteful"),
         (else_try),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied"),
         (try_end),
       (try_end),

	(else_try),
		(eq, ":entry_type", logent_renounced_allegiance),
		(eq, ":actor", "trp_player"),
		(try_begin),
			(eq, ":faction_object", "$g_talk_troop_faction"),
			(neq, ":troop_object", "$g_talk_troop"),
			(try_begin),
				(ge, "$g_talk_troop_faction_relation", 0),
				(neq, "$g_talk_troop_faction", "$players_kingdom"),
				(assign, ":relevance", 180),
				(try_begin),
					(gt, "$g_talk_troop_relation", 5),
					(assign, ":comment", "str_comment_you_renounced_your_alliegance_friendly"),
				(else_try),
					(ge, "$g_talk_troop_relation", 0),
					(eq, ":reputation", lrep_goodnatured),
					(assign, ":comment", "str_comment_you_renounced_your_alliegance_friendly"),
				(try_end),
			(else_try),
				(lt, "$g_talk_troop_faction_relation", 0),
				(assign, ":relevance", 300),
				(try_begin),
					(ge, "$g_talk_troop_relation", 0),
					(this_or_next|eq, ":reputation", lrep_selfrighteous),
					(eq, ":reputation", lrep_debauched),
					(assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_moralizing"),
				(else_try),
					(gt, "$g_talk_troop_relation", 5),
					(this_or_next|eq, ":reputation", lrep_goodnatured),
					(eq, ":reputation", lrep_upstanding),
					(assign, ":comment", "str_comment_you_renounced_your_alliegance_enemy_friendly"),
				(else_try),
					(gt, "$g_talk_troop_relation", 5),
					(assign, ":comment", "str_comment_you_renounced_your_alliegance_enemy"),
				(else_try),
					(is_between, "$g_talk_troop_relation", -5, 5),
					(this_or_next|eq, ":reputation", lrep_quarrelsome),
					(eq, ":reputation", lrep_debauched),
					(assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_spiteful"),
					(assign, ":suggested_relation_change", -2),
				(else_try),
					(lt, "$g_talk_troop_relation", -5),
					(this_or_next|eq, ":reputation", lrep_quarrelsome),
					(this_or_next|eq, ":reputation", lrep_selfrighteous),
					(eq, ":reputation", lrep_debauched),
					(assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_spiteful"),
				(else_try),
					(assign, ":comment", "str_comment_you_renounced_your_alliegance_default"),
				(try_end),
			(try_end),
		(try_end),

	(try_end),
	(assign, reg0, ":comment"),
	(assign, reg1, ":relevance"),
	(assign, reg2, ":suggested_relation_change"),
]),

# script_get_relevant_comment_to_s42
# Input: none
# Output: reg0 = 1 if comment found, 0 otherwise; s61 will contain comment string if found
("get_relevant_comment_to_s42",
    [(troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
     (try_begin),
       (eq, "$cheat_mode", 1),
       (store_add, ":rep_string", ":reputation", "str_personality_archetypes"),
       (str_store_string, s15, ":rep_string"),
       (display_message, "@Reputation type: {s15}"),
     (try_end),
      
     (assign, ":highest_score_so_far", 50),
     (assign, ":best_comment_so_far", -1),
     (assign, ":comment_found", 0),
     (assign, ":best_log_entry", -1),
     (assign, ":comment_relation_change", 0),
     (store_current_hours, ":current_time"),

#prevents multiple comments in conversations in same hour

#     (troop_get_slot, ":talk_troop_last_comment_time", "$g_talk_troop", slot_troop_last_comment_time),
#"$num_log_entries should also be set to one, not zero. This is included in the initialize npcs script, although could be moved to game_start
     (troop_get_slot, ":talk_troop_last_comment_slot", "$g_talk_troop", slot_troop_last_comment_slot),
     (troop_set_slot, "$g_talk_troop", slot_troop_last_comment_slot, "$num_log_entries"),

     (store_add, ":log_entries_plus_one", "$num_log_entries", 1),
     (try_for_range, ":log_entry_no", 1, ":log_entries_plus_one"),
#      It should be log entries plus one, so that the try_ sequence does not stop short of the last log entry
#      $Num_log_entries is now the number of the last log entry, which begins at "1" rather than "0"
#      This is so that (le, ":log_entry_no", ":talk_troop_last_comment_slot") works properly
     
       (troop_get_slot, ":entry_time",           "trp_log_array_entry_time",           ":log_entry_no"),
#      (val_max, ":entry_time", 1), #This is needed for pre-game events to be commented upon, if hours are used rather than the order of events
       (store_sub, ":entry_hours_elapsed", ":current_time", ":entry_time"),
       (try_begin),
         (le, ":log_entry_no", ":talk_troop_last_comment_slot"),
#         (le, ":entry_time", ":talk_troop_last_comment_time"),
         (try_begin),
           (eq, ":log_entry_no", ":talk_troop_last_comment_slot"),
           (eq, "$cheat_mode", 1),
           (assign, reg5, ":log_entry_no"),
           (display_message, "@Entries up to #{reg5} skipped"),
         (try_end),
#       I suggest using the log entry number as opposed to time so that events in the same hour can be commented upon
#       This feels more natural, for example, if there are other lords in the court when the player pledges allegiance     
       (else_try),
#         (le, ":entry_hours_elapsed", 3), #don't comment on really fresh events 
#       (else_try),
         (call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
         (gt, reg1, 10),
         (assign, ":score", reg1),
         (assign, ":comment", reg0),
         (store_random_in_range, ":rand", 70, 140),
         (val_mul, ":score", ":rand"),
         (store_add, ":entry_time_score", ":entry_hours_elapsed", 500), #approx. one month 
         (val_mul, ":score", 1000),
         (val_div, ":score", ":entry_time_score"), ###Relevance decreases over time - halved after one month, one-third after two, etc
         (try_begin),
           (gt, ":score", ":highest_score_so_far"),
           (assign, ":highest_score_so_far", ":score"),
           (assign, ":best_comment_so_far",  ":comment"),
           (assign, ":best_log_entry", ":log_entry_no"),
           (assign, ":comment_relation_change", reg2),
         (try_end),
       (try_end),
     (try_end),

     (try_begin),
       (gt, ":best_comment_so_far", 0),
       (assign, ":comment_found", 1), #comment found print it to s61 now. 
       (troop_get_slot, ":actor",                 "trp_log_array_actor",                 ":best_log_entry"),
       (troop_get_slot, ":center_object",         "trp_log_array_center_object",         ":best_log_entry"),
       (troop_get_slot, ":center_object_lord",    "trp_log_array_center_object_lord",    ":best_log_entry"),
       (troop_get_slot, ":center_object_faction", "trp_log_array_center_object_faction", ":best_log_entry"),
       (troop_get_slot, ":troop_object",          "trp_log_array_troop_object",          ":best_log_entry"),
       (troop_get_slot, ":troop_object_faction",  "trp_log_array_troop_object_faction",  ":best_log_entry"),
       (troop_get_slot, ":faction_object",        "trp_log_array_faction_object",        ":best_log_entry"),
       (try_begin),
         (ge, ":actor", 0),
         (str_store_troop_name,   s50, ":actor"),
       (try_end),
       (try_begin),
         (ge, ":center_object", 0),
         (str_store_party_name,   s51, ":center_object"),
       (try_end),
       (try_begin),
         (ge, ":center_object_lord", 0),
         (str_store_troop_name,   s52, ":center_object_lord"),
       (try_end),
       (try_begin),
         (ge, ":center_object_faction", 0),
         (str_store_faction_name, s53, ":center_object_faction"),
       (try_end),
       (try_begin),
         (ge, ":troop_object", 0),
         (str_store_troop_name,   s54, ":troop_object"),
       (try_end),
       (try_begin),
         (ge, ":troop_object_faction", 0),
         (str_store_faction_name, s55, ":troop_object_faction"),
       (try_end),
       (try_begin),
         (ge, ":faction_object", 0),
         (str_store_faction_name, s56, ":faction_object"),
       (try_end),
       (str_store_string, s42, ":best_comment_so_far"),
     (try_end),
     
     (assign, reg0, ":comment_found"),
     (assign, "$log_comment_relation_change", ":comment_relation_change"),
]),

# script_get_culture_with_party_faction_for_music
# Input: arg1 = party_no
# Output: reg0 = culture
("get_culture_with_party_faction_for_music",
    [ (store_script_param, ":party_no", 1),
      (store_faction_of_party, ":faction_no", ":party_no"),
      (try_begin),
        (this_or_next|eq, ":faction_no", "fac_player_faction"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (assign, ":faction_no", "$players_kingdom"),
      (try_end),
      (try_begin),
        (is_between, ":party_no", centers_begin, centers_end),
        (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
        (neg|is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (party_get_slot, ":faction_no", ":party_no", slot_center_original_faction),
      (try_end),

      (faction_get_slot, ":result", ":faction_no", slot_faction_culture),

      #MV: commented this out! it overwrote a valid result!
      # (try_begin),
        # (this_or_next|eq, ":faction_no", "fac_outlaws"),
# #        (this_or_next|eq, ":faction_no", "fac_peasant_rebels"),
        # (this_or_next|eq, ":faction_no", "fac_deserters"),
        # (this_or_next|eq, ":faction_no", "fac_mountain_bandits"),
        # (eq, ":faction_no", "fac_forest_bandits"),
        # (assign, ":result", mtf_culture_6),
      # (else_try),
        # (assign, ":result", 0), #no culture, including player with no bindings to another kingdom
      # (try_end),
      (assign, reg0, ":result"),
]),
# script_music_set_situation_with_culture
# Input: arg1 = music_situation
("music_set_situation_with_culture",
    [ (store_script_param, ":situation", 1),
      (assign, ":culture", 0), #no culture
      (try_begin),
        (this_or_next|eq, ":situation", mtf_sit_town),
        (this_or_next|eq, ":situation", mtf_sit_day),
        (this_or_next|eq, ":situation", mtf_sit_night),
        (this_or_next|eq, ":situation", mtf_sit_town_infiltrate),
        (eq, ":situation", mtf_sit_encounter_hostile),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
      (else_try),
        (this_or_next|eq, ":situation", mtf_sit_ambushed),
        (eq, ":situation", mtf_sit_fight),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_closest_center", "p_main_party"),
        (call_script, "script_get_culture_with_party_faction_for_music", reg0),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_travel),
        #(call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        #(val_or, ":culture", reg0),
        (call_script, "script_get_closest_center", "p_main_party"),
        (call_script, "script_get_culture_with_party_faction_for_music", reg0),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_victorious),
        (call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_killed),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
      (try_end),
      (try_begin),
        (this_or_next|eq, ":situation", mtf_sit_town),
        (eq, ":situation", mtf_sit_day),
        (try_begin),
          (is_currently_night),
          (assign, ":situation", mtf_sit_night),
        (try_end),
      (try_end),
      (music_set_situation, ":situation"),
      (music_set_culture, ":culture"),

# (assign, reg0, ":situation"),
# (assign, reg1, ":culture"),
# (display_message,"@DEBUG: music_set_situation_with_culture: situation {reg0}, culture {reg1}"),
      
      #MV: Custom TLD music for towns, because we have too many cultures and town-specific tracks
      (try_begin),
        (eq, ":situation", mtf_sit_town),
        (assign, ":track", 0),
        (store_faction_of_party, ":town_faction", "$g_encountered_party"),
        (try_begin),
          (this_or_next|eq, ":town_faction", "fac_gondor"),
          (eq, ":town_faction", "fac_rohan"),
          (store_random_in_range, ":random", 0, 100),
          (lt, ":random", 10), #play alliance track 10% of the time
          (assign, ":track", "track_TLD_Alliance_Towns"),
        (else_try),
          (eq, ":town_faction", "fac_gondor"),
          (try_begin),
            (eq, "$g_encountered_party", "p_town_minas_tirith"),
            (assign, ":track", "track_TLD_Minas_Tirith"),
          (else_try),
            (eq, "$g_encountered_party", "p_town_dol_amroth"),
            (assign, ":track", "track_TLD_Dol_Amroth"),
          (else_try),
            (eq, "$g_encountered_party", "p_town_erech"),
            (assign, ":track", "track_TLD_Black_Root"),
          (else_try),
            (eq, "$g_encountered_party", "p_town_lossarnach"),
            (assign, ":track", "track_TLD_Lossarnach"),
          (else_try),
            (eq, "$g_encountered_party", "p_town_pinnath_gelin"),
            (assign, ":track", "track_TLD_Pinnath_Gelin"),
          (else_try),
            (eq, "$g_encountered_party", "p_town_west_osgiliath"),
            (assign, ":track", "track_TLD_Osgiliath"),
          (else_try),
            (eq, "$g_encountered_party", "p_town_henneth_annun"),
            (assign, ":track", "track_TLD_Henneth_Annun"),
          (else_try),
            (assign, ":track", "track_TLD_Gondor_Cities"),
          (try_end),
        (else_try),
          (eq, ":town_faction", "fac_rohan"),
          (try_begin),
            (eq, "$g_encountered_party", "p_town_edoras"),
            (assign, ":track", "track_TLD_Edoras"),
          (else_try),
            (eq, "$g_encountered_party", "p_town_hornburg"),
            (assign, ":track", "track_TLD_Helms_Deep"),
          (else_try),
            (assign, ":track", "track_TLD_Rohan_Village"),
          (try_end),
        (else_try),
          (eq, ":town_faction", "fac_dwarf"),
          (try_begin),
            (eq, "$g_encountered_party", "p_town_ironhill_camp"),
            (assign, ":track", "track_TLD_Iron_Hill_Mine"),
          (else_try),
            (assign, ":track", "track_TLD_Erebor"),
          (try_end),
        (else_try),
          (this_or_next|eq, ":town_faction", "fac_mordor"),
          (this_or_next|eq, ":town_faction", "fac_guldur"),
          (eq, ":town_faction", "fac_moria"),
          (try_begin),
            (eq, "$g_encountered_party", "p_town_minas_morgul"),
            (assign, ":track", "track_TLD_Minas_Morgul"),
          (else_try),
            (assign, ":track", "track_TLD_Orc_Camp"),
          (try_end),
        (else_try),
          (eq, ":town_faction", "fac_isengard"),
          (try_begin),
            (eq, "$g_encountered_party", "p_town_isengard"),
            (assign, ":track", "track_TLD_Isengard_Town"),
          (else_try),
            (assign, ":track", "track_TLD_Uruk_Camp"),
          (try_end),
        (else_try),
          (eq, ":town_faction", "fac_lorien"),
          (assign, ":track", "track_TLD_Lothlorien"),
        (else_try),
          (eq, ":town_faction", "fac_imladris"),
          (assign, ":track", "track_TLD_Rivendell_Camp"),
        (else_try),
          (eq, ":town_faction", "fac_woodelf"),
          (assign, ":track", "track_TLD_Mirkwood_Camp"),
        (else_try),
          (eq, ":town_faction", "fac_dale"),
          (try_begin),
            (eq, "$g_encountered_party", "p_town_esgaroth"),
            (assign, ":track", "track_TLD_Esgaroth"),
          (else_try),
            (assign, ":track", "track_TLD_Dale"),
          (try_end),
        (else_try),
          (eq, ":town_faction", "fac_harad"),
          (assign, ":track", "track_TLD_Harad_Camp"),
        (else_try),
          (eq, ":town_faction", "fac_rhun"),
          (assign, ":track", "track_TLD_Rhun_Encampment"),
        (else_try),
          (eq, ":town_faction", "fac_khand"),
          (assign, ":track", "track_TLD_Khand_Encampment"),
        (else_try),
          (eq, ":town_faction", "fac_umbar"),
          (assign, ":track", "track_TLD_Corsair_Camp"),
        (else_try),
          (eq, ":town_faction", "fac_gundabad"),
          (assign, ":track", "track_TLD_Gundabad_Camp"),
        (else_try),
          (eq, ":town_faction", "fac_dunland"),
          (assign, ":track", "track_TLD_Dunland_Camp"),
        (else_try),
          #(eq, ":town_faction", "fac_beorn"),
          (assign, ":track", "track_TLD_Beorning_Town"),
        (try_end),
        (play_track, ":track", 1),
      (try_end),
      
      #MV: Custom TLD music for battles, because we have too many cultures to use mtf_culture_X flags
      (try_begin),
        (this_or_next|eq, ":situation", mtf_sit_fight),
        (eq, ":situation", mtf_sit_ambushed),
        (assign, ":track", 0),
        (store_faction_of_party, ":faction", "$g_encountered_party"), #could be enemy or ally
        (try_begin),
          (neg|is_between, ":faction", kingdoms_begin, kingdoms_end), #bandits etc. have no music
          (try_begin),
            (gt, "$g_encountered_party_2", 0),
            (store_faction_of_party, ":faction", "$g_encountered_party_2"), #could be enemy or ally
          (try_end),
          (try_begin),
            (neg|is_between, ":faction", kingdoms_begin, kingdoms_end), #bandits etc. have no music
            (assign, ":faction", "$players_kingdom"), #third and last option
          (try_end),
        (try_end),
        # now ":faction" is one of the major factions
# (assign, reg0, ":faction"),
# (str_store_faction_name, s4, ":faction"),
# (display_message,"@DEBUG: choosing battle music for faction {reg0} ({s4})"),
        (try_begin),
          (eq, ":faction", "fac_gondor"),
	  (store_random_in_range, ":random", 0, 100),
	  (try_begin),
		(lt, ":random", 50), # 50/50 chance for each track (CppCoder)
          	(assign, ":track", "track_TLD_Battle_Gondor"),
	  (else_try),
          	(assign, ":track", "track_TLD_Battle_Gondor_2"),
	  (try_end),
        (else_try),
          (eq, ":faction", "fac_dwarf"),
          (assign, ":track", "track_TLD_Battle_Dwarves"),
        (else_try),
          (eq, ":faction", "fac_rohan"),
          (assign, ":track", "track_TLD_Battle_Rohan"),
        (else_try),
          (eq, ":faction", "fac_mordor"),
          (assign, ":track", "track_TLD_Battle_Mordor"),
        (else_try),
          (eq, ":faction", "fac_isengard"),
          (assign, ":track", "track_TLD_Battle_Isengard"),
        (else_try), 
          (eq, ":faction", "fac_lorien"),
          (assign, ":track", "track_TLD_Battle_Elves"),
        (else_try),
          (eq, ":faction", "fac_imladris"),
          (assign, ":track", "track_TLD_Battle_Imladris"),
        (else_try),
          (eq, ":faction", "fac_woodelf"),
          (assign, ":track", "track_TLD_Battle_Wood_Elves"),
        (else_try),
          (eq, ":faction", "fac_dale"),
          (assign, ":track", "track_TLD_Battle_Barding"),
        (else_try),
          (eq, ":faction", "fac_harad"),
          (assign, ":track", "track_TLD_Battle_Far_Harad"),
        (else_try), # Khand
          (eq, ":faction", "fac_khand"),
          (assign, ":track", "track_TLD_Battle_Khand"),
        (else_try), # Rhun
          (eq, ":faction", "fac_rhun"),
          (assign, ":track", "track_TLD_Battle_Rhun"),
        (else_try), # Corsairs
          (eq, ":faction", "fac_umbar"),
          (assign, ":track", "track_TLD_Battle_Corsair"),
        (else_try), #some orc factions
          (this_or_next|eq, ":faction", "fac_moria"),
          (eq, ":faction", "fac_guldur"),
          (assign, ":track", "track_TLD_Battle_Orcs"),
        (else_try),
          (eq, ":faction", "fac_gundabad"),
          (assign, ":track", "track_TLD_Battle_Gundabad"),
        (else_try),
          (eq, ":faction", "fac_dunland"),
          (assign, ":track", "track_TLD_Battle_Dunland"),
        (else_try),
          #(eq, ":faction", "fac_beorn"),
          (assign, ":track", "track_TLD_Battle_Beorn"),
        (try_end),
        
        (play_track, ":track", 0),
      (try_end),
      
      #MV: Custom TLD music for travel, because we have too many cultures to use mtf_culture_X flags
      #Picks closest center and tries to find the music of its ORIGINAL faction, if any
      #If there is none, plays standard travel music (TLD_Map_Day_X)
      #Even if there is a faction, there is 20% chance it will play standard travel music (so if the player doesn't travel much and stays in the same country, won't be bored by the same factional music)
      (try_begin),
        (eq, ":situation", mtf_sit_travel),
        (assign, ":track", 0),
        (call_script, "script_get_closest_center", "p_main_party"),
        (assign, ":closest_center", reg0),
        (party_get_slot, ":faction", ":closest_center", slot_center_original_faction),
        (store_random_in_range, ":random", 0, 100),
        (try_begin),
          (lt, ":random", 20), #20% of the time, just play standard travel music, regardless of territory
          (assign, ":faction", 0), #reset faction to invalid
        (try_end),
# (assign, reg0, ":faction"),
# (str_store_faction_name, s4, ":faction"),
# (display_message,"@DEBUG: choosing travel music for faction {reg0} ({s4})"),
        
        (assign, ":no_tracks", 0), #available tracks per faction, used to pick one at random
        (try_begin),
          (eq, ":faction", "fac_gondor"),
          (assign, ":track", "track_TLD_Map_Gondor_A"),
          (assign, ":no_tracks", 5),
        (else_try),
          (eq, ":faction", "fac_dwarf"),
          (assign, ":track", "track_TLD_Map_Dwarves_A"),
          (assign, ":no_tracks", 3),
        (else_try),
          (eq, ":faction", "fac_rohan"),
          (assign, ":track", "track_TLD_Map_Rohan_A"),
          (assign, ":no_tracks", 4),
        (else_try), #all orc factions
          (this_or_next|eq, ":faction", "fac_mordor"),
          (this_or_next|eq, ":faction", "fac_isengard"),
          (this_or_next|eq, ":faction", "fac_moria"),
          (this_or_next|eq, ":faction", "fac_guldur"),
          (eq, ":faction", "fac_gundabad"),
          (assign, ":track", "track_TLD_Map_Orcs_A"),
          (assign, ":no_tracks", 4),
        (else_try), #elven factions
          (this_or_next|eq, ":faction", "fac_lorien"),
          (this_or_next|eq, ":faction", "fac_imladris"),
          (eq, ":faction", "fac_woodelf"),
          (assign, ":track", "track_TLD_Map_Elven_A"),
          (assign, ":no_tracks", 5),
        # (else_try),
          # (eq, ":faction", "fac_dale"),
        (else_try),
          (eq, ":faction", "fac_harad"),
          (assign, ":track", "track_TLD_Map_Harad_A"),
          (assign, ":no_tracks", 4),
        (else_try), #some evil men
          (this_or_next|eq, ":faction", "fac_rhun"),
          (this_or_next|eq, ":faction", "fac_khand"),
          (eq, ":faction", "fac_umbar"),
          (assign, ":track", "track_TLD_Map_Khand_A"),
          (assign, ":no_tracks", 3),
        (else_try),
          (eq, ":faction", "fac_dunland"),
          (assign, ":track", "track_TLD_Map_Dunland_A"),
          (assign, ":no_tracks", 2),
        # (else_try),
          # (eq, ":faction", "fac_beorn"),
        (else_try), #couldn't find a faction (Dale, Beorn), play standard travel music
          (try_begin),
            (is_currently_night),
            (assign, ":track", "track_TLD_Map_Night_A"),
            (assign, ":no_tracks", 7),
          (else_try), 
            (assign, ":track", "track_TLD_Map_Day_A"),
            (assign, ":no_tracks", 11),
          (try_end),
        (try_end),
       
        (store_random_in_range, ":random_track_index", 0, ":no_tracks"),
        (val_add, ":track", ":random_track_index"),        
        (play_track, ":track", 0),
      (try_end),
]),
# script_combat_music_set_situation_with_culture
("combat_music_set_situation_with_culture",
    [ (assign, ":situation", mtf_sit_fight),
      (assign, ":num_allies", 0),
      (assign, ":num_enemies", 0),
      (try_for_agents, ":agent_no"),
        (agent_is_alive, ":agent_no"),
        (agent_is_human, ":agent_no"),
        (agent_get_troop_id, ":agent_troop_id", ":agent_no"),
        (store_character_level, ":troop_level", ":agent_troop_id"),
        (val_add,  ":troop_level", 10),
        (val_mul, ":troop_level", ":troop_level"),
        (try_begin),
          (agent_is_ally, ":agent_no"),
          (val_add, ":num_allies", ":troop_level"),
        (else_try),
          (val_add, ":num_enemies", ":troop_level"),
        (try_end),
      (try_end),
      (val_mul, ":num_allies", 4), #play ambushed music if we are 2 times outnumbered.
      (val_div, ":num_allies", 3),
      (try_begin),
        (lt, ":num_allies", ":num_enemies"),
        (assign, ":situation", mtf_sit_ambushed),
      (try_end),
      (call_script, "script_music_set_situation_with_culture", ":situation"),
]),

# script_set_items_for_tournament
# Input: arg1 = horse_chance, arg2 = lance_chance (with horse only), arg3 = sword_chance, arg4 = axe_chance, arg5 = bow_chance (without horse only), arg6 = javelin_chance (with horse only), arg7 = mounted_bow_chance (with horse only), arg8 = crossbow_sword_chance, arg9 = armor_item_begin, arg10 = helm_item_begin
# Output: none (sets mt_arena_melee_fight items)
("set_items_for_tournament",
    [ (store_script_param, ":horse_chance", 1),
      (store_script_param, ":lance_chance", 2),
      (store_script_param, ":sword_chance", 3),
      (store_script_param, ":axe_chance", 4),
      (store_script_param, ":bow_chance", 5),
      (store_script_param, ":javelin_chance", 6),
      (store_script_param, ":mounted_bow_chance", 7),
      (store_script_param, ":crossbow_sword_chance", 8),
      (store_script_param, ":armor_item_begin", 9),
      (store_script_param, ":helm_item_begin", 10),
      (store_add, ":total_chance", ":sword_chance", ":axe_chance"),
      (val_add, ":total_chance", ":crossbow_sword_chance"),
      (try_for_range, ":i_ep", 0, 32),
        (mission_tpl_entry_clear_override_items, "mt_arena_melee_fight", ":i_ep"),
        (assign, ":has_horse", 0),
        (store_div, ":cur_team", ":i_ep", 8),
        (try_begin),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":horse_chance"),
          (assign, ":has_horse", 1),
        (try_end),
        (try_begin),
          (eq, ":has_horse", 1),
          (store_add, ":cur_total_chance", ":total_chance", ":lance_chance"),
          (val_add, ":cur_total_chance", ":javelin_chance"),
          (val_add, ":cur_total_chance", ":mounted_bow_chance"),
        (else_try),
          (store_add, ":cur_total_chance", ":total_chance", ":bow_chance"),
        (try_end),
        (store_random_in_range, ":random_no", 0, ":cur_total_chance"),
        (try_begin),
          (val_sub, ":random_no", ":sword_chance"),
          (lt, ":random_no", 0),
          (try_begin),
            (store_random_in_range, ":sub_random_no", 0, 100),
            (lt, ":sub_random_no", 50),
#            (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_shield"),
          (else_try),
          (try_end),
        (else_try),
          (val_sub, ":random_no", ":axe_chance"),
          (lt, ":random_no", 0),
#         (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_shield"),
        (else_try),
          (val_sub, ":random_no", ":crossbow_sword_chance"),
          (lt, ":random_no", 0),
        (else_try),
          (eq, ":has_horse", 0),
          (val_sub, ":random_no", ":bow_chance"),
          (lt, ":random_no", 0),
        (else_try),
          (eq, ":has_horse", 1),
          (val_sub, ":random_no", ":lance_chance"),
          (lt, ":random_no", 0),
#          (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_shield"),
        (else_try),
          (eq, ":has_horse", 1),
          (val_sub, ":random_no", ":javelin_chance"),
          (lt, ":random_no", 0),
#          (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_shield"),
        (else_try),
          (eq, ":has_horse", 1),
          (val_sub, ":random_no", ":mounted_bow_chance"),
          (lt, ":random_no", 0),
          #(mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_bow"),
          #(mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", "itm_practice_arrows"),
        (try_end),
        (try_begin),
          (ge, ":armor_item_begin", 0),
          (store_add, ":cur_armor_item", ":armor_item_begin", ":cur_team"),
          (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", ":cur_armor_item"),
        (try_end),
        (try_begin),
          (ge, ":helm_item_begin", 0),
          (store_add, ":cur_helm_item", ":helm_item_begin", ":cur_team"),
          (mission_tpl_entry_add_override_item, "mt_arena_melee_fight", ":i_ep", ":cur_helm_item"),
        (try_end),
      (try_end),
]),

# script_custom_battle_end
("custom_battle_end",
    [ (assign, "$g_custom_battle_team1_death_count", 0),
      (assign, "$g_custom_battle_team2_death_count", 0),
      (try_for_agents, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (neg|agent_is_alive, ":cur_agent"),
        (agent_get_team, ":cur_team", ":cur_agent"),
        (try_begin),
          (eq, ":cur_team", 0),
          (val_add, "$g_custom_battle_team1_death_count", 1),
        (else_try),
          (val_add, "$g_custom_battle_team2_death_count", 1),
        (try_end),
      (try_end),
]),  

# script_remove_troop_from_prison
# Input: troop_no
("remove_troop_from_prison",
    [ (store_script_param, ":troop_no", 1),
      (troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
      # (try_begin),
        # (check_quest_active, "qst_rescue_lord_by_replace"),
        # (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, ":troop_no"),
        # (call_script, "script_cancel_quest", "qst_rescue_lord_by_replace"),
      # (try_end),
      # (try_begin),
        # (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
        # (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, ":troop_no"),
        # (call_script, "script_cancel_quest", "qst_deliver_message_to_prisoner_lord"),
      # (try_end),
]),  

# script_TLD_troop_banner_slot_init 
# run at the start of the game
("TLD_troop_banner_slot_init",
  [ (troop_set_slot, "trp_woodsman_of_lossarnach",      slot_troop_banner_scene_prop, "mesh_banner_e02"),
    (troop_set_slot, "trp_axeman_of_lossarnach",        slot_troop_banner_scene_prop, "mesh_banner_e03"),
    (troop_set_slot, "trp_axemaster_of_lossarnach",     slot_troop_banner_scene_prop, "mesh_banner_e04"),
    (troop_set_slot, "trp_clansman_of_lamedon",         slot_troop_banner_scene_prop, "mesh_banner_e09"),
    (troop_set_slot, "trp_footman_of_lamedon",          slot_troop_banner_scene_prop, "mesh_banner_e10"),
    (troop_set_slot, "trp_veteran_of_lamedon",          slot_troop_banner_scene_prop, "mesh_banner_e11"),
    (troop_set_slot, "trp_pinnath_gelin_plainsman",     slot_troop_banner_scene_prop, "mesh_banner_e05"),
    (troop_set_slot, "trp_pinnath_gelin_spearman",      slot_troop_banner_scene_prop, "mesh_banner_e06"),
    (troop_set_slot, "trp_warrior_of_pinnath_gelin",    slot_troop_banner_scene_prop, "mesh_banner_e07"),
    ## BRV does not have shields
    (troop_set_slot, "trp_dol_amroth_youth",            slot_troop_banner_scene_prop, "mesh_banner_e16"),
    (troop_set_slot, "trp_squire_of_dol_amroth",        slot_troop_banner_scene_prop, "mesh_banner_e17"),
    (troop_set_slot, "trp_veteran_squire_of_dol_amroth",slot_troop_banner_scene_prop, "mesh_banner_e17"),
    (troop_set_slot, "trp_knight_of_dol_amroth",        slot_troop_banner_scene_prop, "mesh_banner_e18"),
    (troop_set_slot, "trp_veteran_knight_of_dol_amroth",slot_troop_banner_scene_prop, "mesh_banner_e18"),
    (troop_set_slot, "trp_swan_knight_of_dol_amroth",   slot_troop_banner_scene_prop, "mesh_banner_e18"),
]),

#script_TLD_shield_item_set_banner, by GA
# INPUT: agent_no
("TLD_shield_item_set_banner",
  [ (store_script_param, ":tableau_no",1),
    (store_script_param, ":agent_no", 2),
    (store_script_param, ":troop_no", 3),
#    (assign, ":banner_troop", -1),
    (assign, ":banner_mesh", "mesh_banners_default_b"),
    (try_begin),
        (neq,":agent_no",-1),
#        (agent_get_party_id,":party",":agent_no"),
        (try_begin),
            (is_between,":troop_no","trp_rhun_tribesman","trp_rhun_veteran_swift_horseman"),# Rhun randomized heraldry
            (store_random_in_range,":banner_mesh","mesh_circular_8mosaic1","mesh_circular_8mosaic10"),                                            
        (else_try),
            (is_between,":troop_no","trp_harad_desert_warrior","trp_gold_serpent_horse_archer"),# Harad randomized heraldry
            (store_random_in_range,":banner_mesh",275,300),                                            
        #(else_try),
            #(eq,"$player_universal_banner",1),                # indicator for the ability to set player's own banner
            #(eq,":party",":player_party"),
            #(troop_get_slot,":banner_mesh","trp_player",slot_troop_banner_scene_prop),
        (try_end),
    (try_end),
    (cur_item_set_tableau_material, ":tableau_no",":banner_mesh"),
]),

# script_TLD_initialize_civilian_clothes
("TLD_initialize_civilian_clothes", 
    [(store_script_param, ":tableau_no", 1),
    #(store_script_param, ":agent_no", 2),
    (store_script_param, ":troop_no", 3),
    (store_troop_faction, ":fac", ":troop_no"),
    (val_sub, ":fac", kingdoms_begin),
    (try_begin),
        ]+concatenate_scripts([
            [
            (eq, ":fac", x),
            (try_begin),
            ]+concatenate_scripts([
                [
                (eq, ":tableau_no", fac_tableau_list[x][z][0]),
                (store_random_in_range, ":rand", 0, len(fac_tableau_list[x][z][1])),
                (try_begin),
                ]+concatenate_scripts([
                    [
                    (eq, ":rand", y),
                    (cur_item_set_tableau_material, ":tableau_no", fac_tableau_list[x][z][1][y]),
                (else_try),
                    ] for y in range(len(fac_tableau_list[x][z][1]))
                ])+[
                (try_end),
            (else_try),
                ] for z in range(len(fac_tableau_list[x]))
            ])+[
            (try_end),
        (else_try),
            ] for x in range(len(fac_tableau_list))
        ])+[
    (try_end),
]),

# script_set_item_faction
("set_item_faction",  set_item_faction()+[
	(item_set_slot, "itm_wood_club", slot_item_faction,0xFFFF), # mtarini: make a few items all factions
	(item_set_slot, "itm_twohand_wood_club", slot_item_faction,0xFFFF),
	(item_set_slot, "itm_metal_scraps_bad", slot_item_faction,0xFFFF), # scraps needed for selling w/o faction discount
	(item_set_slot, "itm_metal_scraps_medium", slot_item_faction,0xFFFF),
	(item_set_slot, "itm_metal_scraps_good", slot_item_faction,0xFFFF), 
	
	# CC: Easiest way to make this work...
	(faction_get_slot, ":mordor_mask", "fac_mordor", slot_faction_mask),
	(item_set_slot, "itm_spider", slot_item_faction, ":mordor_mask"), 
]), 

# script_fill_camp_chests
# INPUT: faction
# fills camp chests with items used by this faction
("fill_camp_chests",  [
   (store_script_param_1, ":faction"),
   (faction_get_slot, ":fm", ":faction", slot_faction_mask),
   
   (troop_clear_inventory,"trp_camp_chest_faction"),
   (troop_clear_inventory,"trp_camp_chest_none"),
   (troop_ensure_inventory_space,"trp_camp_chest_faction",70),
   (troop_ensure_inventory_space,"trp_camp_chest_none",70),
   
   (store_add,":last_item_plus_one","itm_ent_body",1),
   (try_for_range,":item","itm_no_item",":last_item_plus_one"),
      (item_get_slot,":item_faction_mask",":item",slot_item_faction),
#	  (assign,":ii",":item_faction_mask"),
      (try_begin),
        (eq,":item_faction_mask",0),
		  (troop_add_item,"trp_camp_chest_none",":item",0),
	  (else_try),
	    (val_and,":item_faction_mask",":fm"),
        (try_begin),
		  (neq,":item_faction_mask",0),
		    (troop_add_item,"trp_camp_chest_faction",":item",0),
		(try_end),
      (try_end),
   (try_end),
]),

# script_fill_merchants_CHEAT
# fills smiths across the land with faction stuff
("fill_merchants_cheat",  [
  (set_merchandise_modifier_quality,150),
  (try_for_range,":cur_merchant",weapon_merchants_begin,weapon_merchants_end),
    (reset_item_probabilities,100),     
    (troop_clear_inventory,":cur_merchant"),
	(store_troop_faction,":faction",":cur_merchant"),
	(faction_get_slot, ":fac_mask", ":faction", slot_faction_mask),
	(troop_get_slot,":subfaction",":cur_merchant",slot_troop_subfaction),
	(assign, ":subfac_mask", 1),(try_for_range, ":unused", 0, ":subfaction"),(val_mul, ":subfac_mask", 2),(try_end),
    (try_for_range,":item","itm_no_item","itm_ent_body"),
      (item_get_slot,":item_faction_mask",":item",slot_item_faction),
      (val_and,":item_faction_mask",":fac_mask"),
      (item_get_slot,":item_subfaction_mask",":item",slot_item_subfaction),
      (val_and,":item_subfaction_mask",":subfac_mask"),
      (try_begin),
		(neq,":item_faction_mask",0),(neq,":item_subfaction_mask",0),(troop_add_item,":cur_merchant",":item",0),
	  (try_end),
   (try_end),
  (try_end),
]),

# scripts for gondor tableau shields, by GA
# Input: tableau, agent, troop
("TLD_gondor_round_shield_banner",
  [ (store_script_param, ":tableau_no",1),(store_script_param, ":agent_no", 2),(store_script_param, ":tr", 3),
    (assign, ":bm", "mesh_banner_e08"), #default tableau black
    (try_begin),(neq,":agent_no",-1),
      (try_begin),(is_between,":tr","trp_blackroot_vale_archer"   ,"trp_dol_amroth_youth"        ),(assign, ":bm", "mesh_banner_e02"),
      (else_try) ,(is_between,":tr","trp_pinnath_gelin_plainsman" ,"trp_dol_amroth_youth"        ),(assign, ":bm", "mesh_banner_e05"),
      (else_try) ,(is_between,":tr","trp_clansman_of_lamedon"     ,"trp_pinnath_gelin_plainsman" ),(assign, ":bm", "mesh_banner_e09"),
      (else_try) ,(is_between,":tr","trp_pelargir_watchman"       ,"trp_clansman_of_lamedon"     ),(assign, ":bm", "mesh_banner_e12"),
      (else_try) ,(is_between,":tr","trp_dol_amroth_youth"        ,"trp_lothlorien_scout"        ),(assign, ":bm", "mesh_banner_e16"),
      (else_try) ,(is_between,":tr","trp_woodsman_of_lossarnach"  ,"trp_vet_axeman_of_lossarnach"),(assign, ":bm", "mesh_banner_e19"),
      (else_try) ,(is_between,":tr","trp_vet_axeman_of_lossarnach","trp_axemaster_of_lossarnach" ),(assign, ":bm", "mesh_banner_e20"),
      (else_try) ,(is_between,":tr","trp_axemaster_of_lossarnach" ,"trp_pelargir_watchman"       ),(assign, ":bm", "mesh_banner_e21"),
	  (else_try) ,(troop_get_slot,":b",":tr",slot_troop_banner_scene_prop),(neq,":b",0),(assign,":bm",":b"), # for other troops get mesh from banner slot
	  (try_end),
    (try_end),
    (cur_item_set_tableau_material, ":tableau_no",":bm"),
]),
("TLD_gondor_kite_shield_banner",
  [ (store_script_param, ":tableau_no",1),(store_script_param, ":agent_no", 2),(store_script_param, ":tr", 3),
    (assign, ":bm", "mesh_banner_e08"), #default tableau black
    (try_begin),(neq,":agent_no",-1),
      (try_begin),(is_between,":tr","trp_blackroot_vale_archer"  ,"trp_dol_amroth_youth"     ),(assign, ":bm", "mesh_banner_e04"),
      (else_try) ,(is_between,":tr","trp_pinnath_gelin_plainsman","trp_blackroot_vale_archer"),(assign, ":bm", "mesh_banner_e07"),
      (else_try) ,(is_between,":tr","trp_clansman_of_lamedon"  ,"trp_pinnath_gelin_plainsman"),(assign, ":bm", "mesh_banner_e11"),
      (else_try) ,(is_between,":tr","trp_pelargir_watchman"        ,"trp_clansman_of_lamedon"),(assign, ":bm", "mesh_banner_e14"),
      (else_try) ,(is_between,":tr","trp_dol_amroth_youth"   ,"trp_swan_knight_of_dol_amroth"),(assign, ":bm", "mesh_banner_e17"),
      (else_try) ,(is_between,":tr","trp_swan_knight_of_dol_amroth"   ,"trp_lothlorien_scout"),(assign, ":bm", "mesh_banner_e18"),
	  (else_try) ,(troop_get_slot,":b",":tr",slot_troop_banner_scene_prop),(neq,":b",0),(assign,":bm",":b"), # for other troops get mesh from banner slot
	  (try_end),
    (try_end),
    (cur_item_set_tableau_material, ":tableau_no",":bm"),
]),
("TLD_gondor_tower_shield_banner",
  [ (store_script_param, ":tableau_no",1),(store_script_param, ":agent_no", 2),(store_script_param, ":tr", 3),
    (assign, ":bm", "mesh_banner_e08"), #default tableau black
    (try_begin),(neq,":agent_no",-1),
      (try_begin),(is_between,":tr","trp_blackroot_vale_archer"   ,"trp_dol_amroth_youth"        ),(assign, ":bm", "mesh_banner_e03"),
      (else_try) ,(is_between,":tr","trp_pinnath_gelin_plainsman","trp_blackroot_vale_archer"   ),(assign, ":bm", "mesh_banner_e06"),
      (else_try) ,(is_between,":tr","trp_clansman_of_lamedon"     ,"trp_pinnath_gelin_plainsman"),(assign, ":bm", "mesh_banner_e10"),
	  (else_try) ,(troop_get_slot,":b",":tr",slot_troop_banner_scene_prop),(neq,":b",0),(assign,":bm",":b"), # for other troops get mesh from banner slot
	  (try_end),
    (try_end),
    (cur_item_set_tableau_material, ":tableau_no",":bm"),
]),
("TLD_gondor_square_shield_banner",
  [ (store_script_param, ":tableau_no",1),(store_script_param, ":agent_no", 2),(store_script_param, ":tr", 3),
    (assign, ":bm", "mesh_banner_e08"), #default tableau black
    (try_begin),(neq,":agent_no",-1),
      (try_begin),(is_between,":tr","trp_pelargir_watchman","trp_clansman_of_lamedon"),(assign, ":bm", "mesh_banner_e13"),
      (else_try) ,(is_between,":tr","trp_steward_guard"    ,"trp_ranger_of_ithilien" ),(assign, ":bm", "mesh_banner_e15"),
	  (try_end),
    (try_end),
    (cur_item_set_tableau_material, ":tableau_no",":bm"),
]),

# script_tld_get_rumor_to_s61
# Input: troop, center, agent
# Output: s61 will contain rumor string
("tld_get_rumor_to_s61",
    [(store_script_param, ":troop", 1),
     (store_script_param, ":center", 2),
     (store_script_param, ":agent", 3),

     #check rumor heard already (once a day), troop slot for merchants/lords/etc, center slots for walkers
	 (assign, ":no_new_rumor", 0),
     (agent_get_entry_no, ":entry_no", ":agent"),
     (try_begin),
	    (is_between,":entry_no", town_walker_entries_start, town_walker_entries_start+num_town_walkers),
		(val_add, ":entry_no", slot_center_rumor_check_begin),
	    (try_begin),
		   (party_slot_eq, ":center", ":entry_no", 1),  # rumor heard earlier
		   (assign, ":no_new_rumor", 1),
        (else_try),
           (party_set_slot, ":center", ":entry_no", 1), # rumor set as already heard
        (try_end),
	 (else_try),	 
	    (try_begin),
           (troop_slot_eq, ":troop", slot_troop_rumor_check, 1),  # rumor heard earlier
		   (assign, ":no_new_rumor", 1),
        (else_try),
           (troop_set_slot, ":troop", slot_troop_rumor_check, 1), # rumor set as already heard
        (try_end),
     (try_end),

     (try_begin),
	    (eq,":no_new_rumor", 1), # agent knows nothing new
	    (str_store_string, s61, "str_last_rumor"),
	 (else_try),
	   (store_random_in_range,":rumor_type",0,100),
       (store_troop_faction,":faction","$g_talk_troop"),
		 (try_begin),
         (is_between, ":rumor_type", 0, 80), #faction specific rumors
         (faction_get_slot,":rumors_begin",":faction",slot_faction_rumors_begin),
         (faction_get_slot,":rumors_end"  ,":faction",slot_faction_rumors_end),
         (store_random_in_range,":string",":rumors_begin",":rumors_end"),
       (else_try),
         (is_between, ":rumor_type", 80, 95), #generic rumors
         (faction_get_slot,":faction_side",":faction",slot_faction_side),
		 (try_begin),
            (eq,":faction_side",faction_side_good),
			(store_random_in_range,":string","str_good_rumor_begin","str_evil_rumor_begin"), #good guys get good and neutral rumors
         (else_try),
			(store_random_in_range,":string","str_neutral_rumor_begin","str_legendary_rumor_begin"),
         (try_end),
       (else_try),
         (is_between, ":rumor_type", 95, 100), #legendary rumors
		 (store_random_in_range,":string","str_legendary_rumor_begin","str_last_rumor"),
         (try_begin),
           (eq, ":string", "str_legendary_rumor_amonhen"),
           (neg|party_is_active, "p_legend_amonhen"),
           (enable_party, "p_legend_amonhen"),
           (display_log_message, "@A new location is now available on the map!", color_good_news),
         (else_try),
           (eq, ":string", "str_legendary_rumor_deadmarshes"),
           (neg|party_is_active, "p_legend_deadmarshes"),
           (enable_party, "p_legend_deadmarshes"),
           (display_log_message, "@A new location is now available on the map!", color_good_news),
         (else_try),
           (eq, ":string", "str_legendary_rumor_mirkwood"),
           (neg|party_is_active, "p_legend_mirkwood"),
           (enable_party, "p_legend_mirkwood"),
           (display_log_message, "@A new location is now available on the map!", color_good_news),
         (else_try),
           (this_or_next|eq, ":string", "str_legendary_rumor_begin"),
           (eq, ":string", "str_legendary_rumor_fangorn"),
           (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good), # evil guys can't uncover Entmoot
           (neg|party_is_active, "p_legend_fangorn"),
           (enable_party, "p_legend_fangorn"),
           (display_log_message, "@A new location is now available on the map!", color_good_news),
         (try_end),
       (try_end),
       (str_store_string, s61, ":string"),
     (try_end),
]),

##### TLD 808 TRAITS ###############################################################3

#script_gain_trait
#input: trait number - see slot_trait_*
("gain_trait",[
    (store_script_param, ":trait", 1),
    
    (troop_set_slot, "trp_traits", ":trait", 1),
    
    # Title string = First title string + 2*(slot-1)
    (store_sub, ":title_string", ":trait", 1),
    (val_add, ":title_string", ":title_string"),
    (val_add, ":title_string", tld_first_trait_string),
    (str_store_string, s5, ":title_string"),
    (display_log_message, "@New trait gained: {s5}.", color_good_news),
    (play_sound, "snd_gong"),
]),

#script_cf_gain_trait_blessed
("cf_gain_trait_blessed",[
    (troop_slot_eq, "trp_traits", slot_trait_blessed, 0),
	(troop_get_type, ":race","$g_player_troop"),
	(neg|is_between, ":race", tf_orc_begin, tf_orc_end),
    (call_script, "script_gain_trait", slot_trait_blessed),
	(troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, 20),
	(troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, 20),
	(troop_raise_proficiency_linear, "trp_player", wpt_polearm, 20),
	(troop_raise_proficiency_linear, "trp_player", wpt_archery, 20),
	(troop_raise_proficiency_linear, "trp_player", wpt_throwing, 20),
	(troop_raise_attribute, "trp_player", ca_strength, 1),
	(troop_raise_attribute, "trp_player", ca_agility , 1),
	(troop_raise_attribute, "trp_player", ca_charisma, 1),
    (display_log_message, "@Gained permanent +1 to Strength.", color_good_news),
    (display_log_message, "@Gained permanent +1 to Agility.", color_good_news),
    (display_log_message, "@Gained permanent +1 to Charisma.", color_good_news),
    (display_log_message, "@Gained permanent +20 to weapon proficiencies.", color_good_news),
]), 
#script_cf_gain_trait_reverent
("cf_gain_trait_reverent",[
    (troop_slot_eq, "trp_traits", slot_trait_reverent, 0),
    (call_script, "script_gain_trait", slot_trait_reverent),
]), 
#script_cf_gain_trait_merciful
("cf_gain_trait_merciful",[
    (troop_slot_eq, "trp_traits", slot_trait_merciful, 0),
    (call_script, "script_gain_trait", slot_trait_merciful),
]), 
#script_cf_gain_trait_elf_friend
("cf_gain_trait_elf_friend",[
    (troop_slot_eq, "trp_traits", slot_trait_elf_friend, 0),
    (call_script, "script_gain_trait", slot_trait_elf_friend),
]), 
#script_cf_gain_trait_kings_man
("cf_gain_trait_kings_man",[
    (troop_slot_eq, "trp_traits", slot_trait_rohan_friend, 0),
    (call_script, "script_gain_trait", slot_trait_rohan_friend),
]), 
#script_cf_gain_trait_stewards_blessing
("cf_gain_trait_stewards_blessing",[
    (troop_slot_eq, "trp_traits", slot_trait_gondor_friend, 0),
    (call_script, "script_gain_trait", slot_trait_gondor_friend),
]), 
#script_cf_gain_trait_brigand_friend
("cf_gain_trait_brigand_friend",[
    (troop_slot_eq, "trp_traits", slot_trait_brigand_friend, 0),
    (call_script, "script_gain_trait", slot_trait_brigand_friend),
]), 
#script_cf_gain_trait_oathkeeper
("cf_gain_trait_oathkeeper",[
    (troop_slot_eq, "trp_traits", slot_trait_oathkeeper, 0),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_oathbreaker, 1),
        (troop_set_slot, "trp_traits", slot_trait_oathbreaker, 0),
	(try_end),
    (call_script, "script_gain_trait", slot_trait_oathkeeper),
]), 
#script_cf_gain_trait_oathbreaker
("cf_gain_trait_oathbreaker",[
    (troop_slot_eq, "trp_traits", slot_trait_oathbreaker, 0),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_oathkeeper, 1),
        (troop_set_slot, "trp_traits", slot_trait_oathkeeper, 0),
	(try_end),
    (call_script, "script_gain_trait", slot_trait_oathbreaker),
]), 
#script_cf_gain_trait_orc_pit_champion
("cf_gain_trait_orc_pit_champion",[
    (troop_slot_eq, "trp_traits", slot_trait_orc_pit_champion, 0),
    (call_script, "script_gain_trait", slot_trait_orc_pit_champion),
]), 
#script_cf_gain_trait_despoiler
("cf_gain_trait_despoiler",[
    (troop_slot_eq, "trp_traits", slot_trait_despoiler, 0),
    (call_script, "script_gain_trait", slot_trait_despoiler),
]), 
#script_cf_gain_trait_accursed
("cf_gain_trait_accursed",[
    (troop_slot_eq, "trp_traits", slot_trait_accursed, 0),
    (call_script, "script_gain_trait", slot_trait_accursed),
]), 
#script_cf_gain_trait_berserker
("cf_gain_trait_berserker",[
    (troop_slot_eq, "trp_traits", slot_trait_berserker, 0),
	(troop_raise_attribute, "trp_player", ca_strength, 2),
    (display_log_message, "@Gained permanent +2 to Strength.", color_good_news),
    (call_script, "script_gain_trait", slot_trait_berserker),
]), 
#script_cf_gain_trait_stealthy
("cf_gain_trait_stealthy",[
    (troop_slot_eq, "trp_traits", slot_trait_stealthy, 0),
    (call_script, "script_gain_trait", slot_trait_stealthy),
]), 
#script_cf_gain_trait_infantry_captain
("cf_gain_trait_infantry_captain",[
    (troop_slot_eq, "trp_traits", slot_trait_infantry_captain, 0),
    (call_script, "script_gain_trait", slot_trait_infantry_captain),
]), 
#script_cf_gain_trait_archer_captain
("cf_gain_trait_archer_captain",[
    (troop_slot_eq, "trp_traits", slot_trait_archer_captain, 0),
    (call_script, "script_gain_trait", slot_trait_archer_captain),
]), 
#script_cf_gain_trait_cavalry_captain
("cf_gain_trait_cavalry_captain",[
    (troop_slot_eq, "trp_traits", slot_trait_cavalry_captain, 0),
    (call_script, "script_gain_trait", slot_trait_cavalry_captain),
]), 
#script_cf_gain_trait_command_voice
("cf_gain_trait_command_voice",[
    (troop_slot_eq, "trp_traits", slot_trait_command_voice, 0),
	(troop_get_type, ":race","$g_player_troop"),
	(neg|is_between, ":race", tf_orc_begin, tf_orc_end),
	(troop_raise_attribute, "trp_player", ca_charisma, 2),
    (display_log_message, "@Gained permanent +2 to Charisma.", color_good_news),
    (call_script, "script_gain_trait", slot_trait_command_voice),
]), 
#script_cf_gain_trait_battle_scarred
("cf_gain_trait_battle_scarred",[
    (troop_slot_eq, "trp_traits", slot_trait_battle_scarred, 0),
	(troop_get_type, ":race","$g_player_troop"),
	(neg|is_between, ":race", tf_orc_begin, tf_orc_end),
    (call_script, "script_gain_trait", slot_trait_battle_scarred),
	(troop_raise_attribute, "trp_player", ca_charisma, -1),
    (display_log_message, "@Lost permanent -1 to Charisma.", color_bad_news),
	(store_skill_level, ":skill", skl_ironflesh, "trp_player"),
	(neg|ge, ":skill", 10),
	(troop_raise_skill, "trp_player", skl_ironflesh, 1),
    (display_log_message, "@Gained permanent +1 to Ironflesh.", color_good_news),
 ]), 
#script_cf_gain_trait_fell_beast
("cf_gain_trait_fell_beast",[
    (troop_slot_eq, "trp_traits", slot_trait_fell_beast, 0),
	(troop_get_type, ":race","$g_player_troop"),
	(is_between, ":race", tf_orc_begin, tf_orc_end),
	(troop_raise_attribute, "trp_player", ca_strength, 5),
    (display_log_message, "@Gained permanent +5 to Strength.", color_good_news),
	(troop_raise_attribute, "trp_player", ca_charisma, -2),
    (display_log_message, "@Lost permanent -2 to Charisma.", color_bad_news),
	(store_skill_level, ":skill", skl_ironflesh, "trp_player"),
	(try_begin),(lt, ":skill",9),(troop_raise_skill, "trp_player", skl_ironflesh, 2),
                (display_log_message, "@Gained permanent +2 to Ironflesh.", color_good_news),
	 (else_try),(eq, ":skill",9),(troop_raise_skill, "trp_player", skl_ironflesh, 1),
                (display_log_message, "@Gained permanent +1 to Ironflesh.", color_good_news),
	(try_end),
	(troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, 10),
	(troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, 10),
	(troop_raise_proficiency_linear, "trp_player", wpt_polearm, 10),
	(troop_raise_proficiency_linear, "trp_player", wpt_archery, 10),
	(troop_raise_proficiency_linear, "trp_player", wpt_throwing, 10),
    (display_log_message, "@Gained permanent +10 to weapon proficiencies.", color_good_news),
    (call_script, "script_gain_trait", slot_trait_fell_beast),
 ]), 
#script_cf_gain_trait_foe_hammer
("cf_gain_trait_foe_hammer",[
        (troop_slot_eq, "trp_traits", slot_trait_foe_hammer, 0),
		(troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, 10),
		(troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, 10),
		(troop_raise_proficiency_linear, "trp_player", wpt_polearm, 10),
		(troop_raise_proficiency_linear, "trp_player", wpt_archery, 10),
		(troop_raise_proficiency_linear, "trp_player", wpt_throwing, 10),
        (display_log_message, "@Gained permanent +10 to weapon proficiencies.", color_good_news),
        (call_script, "script_gain_trait", slot_trait_foe_hammer),
		(store_skill_level, ":skill", skl_tactics, "trp_player"),
		(neg|ge, ":skill", 10),
		(troop_raise_skill, "trp_player", skl_tactics, 1),
        (display_log_message, "@Gained permanent +1 to Tactics.", color_good_news),
 ]), 
#script_cf_check_trait_captain
("cf_check_trait_captain",[
        (troop_slot_eq, "trp_traits", slot_trait_archer_captain, 0),
        (troop_slot_eq, "trp_traits", slot_trait_infantry_captain, 0),
        (troop_slot_eq, "trp_traits", slot_trait_cavalry_captain, 0),
        (party_get_num_companions, ":party_size", "p_main_party"),
		(ge, ":party_size", 50), #MV: has to command a sizable party to be called Captain
		(party_get_num_companion_stacks, ":numstacks", "p_main_party"),
		(assign, ":inf_count", 0),
		(assign, ":arc_count", 0),
		(assign, ":cav_count", 0),
		(try_for_range, ":stack", 1, ":numstacks"),
			(party_stack_get_troop_id, ":troop_type", "p_main_party", ":stack"),
            (party_stack_get_size, ":stack_size", "p_main_party", ":stack"), #MV: added this, so all troops are counted, not just types
			#(party_stack_get_troop_id, ":troop", "p_main_party", ":stack"),
			#(troop_get_slot, ":troop_type", ":troop", 6), #MV: whatever was kept here, it's not there now
			(try_begin),
				(neg|troop_is_guarantee_ranged, ":troop_type"),
				(neg|troop_is_mounted, ":troop_type"),
				(store_character_level, ":level", ":troop_type"),
				(ge, ":level", 10),
				(val_add, ":inf_count", ":stack_size"),
			  (else_try),
				(troop_is_guarantee_ranged, ":troop_type"),
				(neg|troop_is_mounted, ":troop_type"),
				(val_add, ":arc_count", ":stack_size"),
			  (else_try),
				(troop_is_mounted, ":troop_type"),
				(val_add, ":cav_count", ":stack_size"),
			(try_end),
		(try_end),
		(try_begin),
			(gt, ":inf_count", ":arc_count"), 
			(gt, ":inf_count", ":cav_count"), 
			(val_add, "$trait_captain_infantry_week", 1),
		  (else_try),
			(gt, ":arc_count", ":inf_count"), 
			(gt, ":arc_count", ":cav_count"), 
			(val_add, "$trait_captain_archer_week", 1),
		  (else_try),
			(gt, ":cav_count", ":arc_count"), 
			(gt, ":cav_count", ":inf_count"), 
			(val_add, "$trait_captain_cavalry_week", 1),
		(try_end),
		(store_skill_level, ":level", skl_leadership, "trp_player"),
		(ge, ":level", 6),
		(store_random,":rnd", 100),
		(try_begin),
			(gt, "$trait_captain_infantry_week", "$trait_captain_archer_week"),
			(gt, "$trait_captain_infantry_week", "$trait_captain_cavalry_week"),
			(assign, ":accumulated_captain", "$trait_captain_infantry_week"),
			(val_mul, ":accumulated_captain", 10),
			(neg|ge, ":rnd", ":accumulated_captain"),
			(call_script, "script_cf_gain_trait_infantry_captain"),
		  (else_try),
			(gt, "$trait_captain_archer_week", "$trait_captain_infantry_week"),
			(gt, "$trait_captain_archer_week", "$trait_captain_cavalry_week"),
			(assign, ":accumulated_captain", "$trait_captain_archer_week"),
			(val_mul, ":accumulated_captain", 10),
			(neg|ge, ":rnd", ":accumulated_captain"),
			(call_script, "script_cf_gain_trait_archer_captain"),
		  (else_try),
			(gt, "$trait_captain_cavalry_week", "$trait_captain_archer_week"),
			(gt, "$trait_captain_cavalry_week", "$trait_captain_infantry_week"),
			(assign, ":accumulated_captain", "$trait_captain_cavalry_week"),
			(val_mul, ":accumulated_captain", 10),
			(neg|ge, ":rnd", ":accumulated_captain"),
			(call_script, "script_cf_gain_trait_cavalry_captain"),
		(try_end),
 ]),
#script_check_agent_armor
("check_agent_armor",[
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_berserker, 0),
		(troop_get_inventory_slot, ":armor", "trp_player", ek_body),
		(try_begin),
		  (neg|ge, ":armor", 1),
		  (store_random, ":x", 2),
		  (val_add, "$trait_check_unarmored_berserker", ":x"),
		(try_end),
	(try_end),
 ]),
############### HEALING AND DEATH FROM 808 modified by GA ############################
#script_injury_routine
#Input: npc to injure
("injury_routine",[
	(store_script_param_1, ":npc"),
	(str_store_troop_name, s1, ":npc"),
	(try_begin),
		(eq,":npc", "trp_player"),
		(str_store_string,s11,"@You_have"),
        (val_add, "$trait_check_battle_scarred", 1), #MV
	(else_try),
		(str_store_string,s11,"@{s1}_has"),
	(try_end),
	(store_random, ":rnd", "$wound_setting"),
	(troop_get_slot, ":wound_mask", ":npc", slot_troop_wound_mask),
	(try_begin),
		(eq, ":rnd", 0),
		(store_and, ":x", ":wound_mask", wound_leg), (eq, ":x", 0),
		#(store_skill_level,":x",skl_riding   ,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_riding, ":x"),
		#(store_skill_level,":x",skl_athletics,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_athletics, ":x"),
		(troop_raise_attribute, ":npc", ca_agility, -2),
		(troop_raise_proficiency_linear, ":npc", wpt_one_handed_weapon, -15),
		(troop_raise_proficiency_linear, ":npc", wpt_two_handed_weapon, -15),
		(troop_raise_proficiency_linear, ":npc", wpt_polearm, -15),
		(val_or, ":wound_mask", wound_leg),
		(troop_set_slot, ":npc", slot_troop_wound_mask, ":wound_mask"),
		(display_message, "@{s11}_suffered_a_serious_wound.", color_bad_news),
		(display_message, "@The_leg_has_been_badly_maimed_in_battle."),
		(display_message, "@(-2_athletics,_-1_riding,_-2_agility,_-15_melee_skill)"),
	(else_try),
		(eq, ":rnd", 1),
		(store_and, ":x", ":wound_mask", wound_arm), (eq, ":x", 0),
		#(store_skill_level,":x",skl_power_draw  ,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_power_draw  ,":x"),
		#(store_skill_level,":x",skl_power_throw ,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_power_throw ,":x"),
		#(store_skill_level,":x",skl_power_strike,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_power_strike,":x"),
		(troop_raise_proficiency_linear, ":npc", wpt_one_handed_weapon, -20),
		(troop_raise_proficiency_linear, ":npc", wpt_two_handed_weapon, -20),
		(troop_raise_proficiency_linear, ":npc", wpt_polearm, -20),
		(troop_raise_proficiency_linear, ":npc", wpt_archery, -20),
		(troop_raise_proficiency_linear, ":npc", wpt_throwing, -20),
		(troop_raise_attribute, ":npc", ca_strength, -2),
		(val_or, ":wound_mask", wound_arm),
		(troop_set_slot, ":npc", slot_troop_wound_mask, ":wound_mask"),
		(display_message, "@{s11}_suffered_a_serious_wound.", color_bad_news),
		(display_message, "@The_arm_has_been_badly_maimed_in_battle."),
		(display_message, "@(-20_weapon_skill,_-2_strength,_-1_power_attacks)"),
	(else_try),
		(eq, ":rnd", 2),
		(store_and, ":x", ":wound_mask", wound_head), (eq, ":x", 0),
		#(store_skill_level,":x",skl_trade          ,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_trade, ":x"),
		#(store_skill_level,":x",skl_first_aid      ,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_first_aid, ":x"),
		#(store_skill_level,":x",skl_surgery        ,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_surgery, ":x"),
		#(store_skill_level,":x",skl_wound_treatment,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_wound_treatment, ":x"),
		#(store_skill_level,":x",skl_spotting       ,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_spotting, ":x"),
		#(store_skill_level,":x",skl_pathfinding    ,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_pathfinding, ":x"),
		#(store_skill_level,":x",skl_tactics        ,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_tactics, ":x"),
		#(store_skill_level,":x",skl_tracking       ,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_tracking, ":x"),
		#(store_skill_level,":x",skl_trainer        ,":npc"),(val_min,":x",1),(val_mul,":x",-1),(troop_raise_skill,":npc",skl_trainer, ":x"),
		(troop_raise_proficiency_linear, ":npc", wpt_archery , -15),
		(troop_raise_proficiency_linear, ":npc", wpt_throwing, -15),
		(val_or, ":wound_mask", wound_head),
		(troop_set_slot, ":npc", slot_troop_wound_mask, ":wound_mask"),
		(display_message, "@{s11}_suffered_a_serious_wound.", color_bad_news),
		(display_message, "@The_head_has_suffered_a_heavy_blow."),
		(display_message, "@(-1_intelligence_skills,_-15_missile_skill)"),
	(else_try),
		(eq, ":rnd", 3),
		(store_and, ":x", ":wound_mask", wound_chest), (eq, ":x", 0),
		(troop_raise_proficiency_linear, ":npc", wpt_one_handed_weapon, -20),
		(troop_raise_proficiency_linear, ":npc", wpt_two_handed_weapon, -20),
		(troop_raise_proficiency_linear, ":npc", wpt_polearm, -20),
		(troop_raise_proficiency_linear, ":npc", wpt_archery, -20),
		(troop_raise_proficiency_linear, ":npc", wpt_throwing, -20),
		(val_or, ":wound_mask", wound_chest),
		(troop_set_slot, ":npc", slot_troop_wound_mask, ":wound_mask"),
		(display_message, "@{s11}_suffered_a_serious_wound.", color_bad_news),
		(display_message, "@The_chest_has_suffered_some_cracked_ribs."),
		(display_message, "@(-20_weapon_skill)"),
	(else_try),
		(eq, ":rnd", 4),
		(assign, ":wounds", 0), #count # of wounds
		(try_begin),(store_and,":x",":wound_mask",wound_leg  ),(neq,":x",0),(val_add,":wounds",1),(try_end),
		(try_begin),(store_and,":x",":wound_mask",wound_arm  ),(neq,":x",0),(val_add,":wounds",1),(try_end),
		(try_begin),(store_and,":x",":wound_mask",wound_head ),(neq,":x",0),(val_add,":wounds",1),(try_end),
		(try_begin),(store_and,":x",":wound_mask",wound_chest),(neq,":x",0),(val_add,":wounds",1),(try_end),
		(val_mul, ":wounds", 10),
		(store_random, ":rnd", 100),
		(neg|ge, ":rnd", ":wounds"),
		(try_begin),
			(neq,":npc", "trp_player"),
			(eq, "$tld_option_death_npc", 1),
			(display_message, "@{s1}_has_been_killed.", color_bad_news),
			(troop_set_slot, ":npc", slot_troop_wound_mask, wound_death),
			(remove_member_from_party,":npc","p_main_party"),
			(call_script, "script_build_mound_for_dead_hero", ":npc", "p_main_party"),
		(else_try),
			(eq,":npc", "trp_player"),
			(eq, "$tld_option_death_player", 1),
			(display_message, "@You_were_killed.", color_bad_news),
			#(assign, "$g_tutorial_entered", 1),
			(finish_mission, 1),
			(jump_to_menu, "mnu_death"), #should be mnu_death here
		(try_end),
	(try_end),
 ]), 
#script_healing_routine
("healing_routine",[
	(store_script_param_1, ":npc"),
	(str_store_troop_name, s1, ":npc"),
	(try_begin),
		(eq,":npc", "trp_player"),
		(str_store_string,s11,"@You_have"),
	(else_try),
		(str_store_string,s11,"@{s1}_has"),
	(try_end),
	(troop_get_slot, ":wound_mask", ":npc", slot_troop_wound_mask),
	(try_begin),
		(neq, ":wound_mask", 0), # only injured heroes apply
		(neq, ":wound_mask", wound_death),# only alive heroes apply
		(store_random_in_range, ":rnd", 0, "$healing_setting"),
		(str_store_troop_name, s1, ":npc"),
		(try_begin),
			(eq, ":rnd", 0),
			(store_and, ":check", ":wound_mask", wound_leg), (neq, ":check", 0),
			#(store_skill_level,":skill",skl_riding   ,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_riding, ":x"),
			#(store_skill_level,":skill",skl_athletics,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",2),(troop_raise_skill,":npc",skl_athletics, ":x"),
			(troop_raise_attribute, ":npc", ca_agility, 2),
			(troop_raise_proficiency_linear, ":npc", wpt_one_handed_weapon, 15),
			(troop_raise_proficiency_linear, ":npc", wpt_two_handed_weapon, 15),
			(troop_raise_proficiency_linear, ":npc", wpt_polearm, 15),
			(val_sub, ":wound_mask", wound_leg),
			(display_message, "@{s1}_recovered_from_a_serious_wound.", color_good_news),
			(display_message, "@The_leg_wound_has_healed."),
			(display_message, "@(+2_athletics,_+1_riding,_+2_agility,_+15_melee_skill)"),
		(else_try),
			(eq, ":rnd", 1),
			(store_and, ":check", ":wound_mask", wound_arm), (neq, ":check", 0),
			#(store_skill_level,":skill",skl_power_draw  ,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_power_draw, ":x"),
			#(store_skill_level,":skill",skl_power_throw ,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_power_throw, ":x"),
			#(store_skill_level,":skill",skl_power_strike,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_power_strike, ":x"),
			(troop_raise_proficiency_linear, ":npc", wpt_one_handed_weapon, 20),
			(troop_raise_proficiency_linear, ":npc", wpt_two_handed_weapon, 20),
			(troop_raise_proficiency_linear, ":npc", wpt_polearm, 20),
			(troop_raise_proficiency_linear, ":npc", wpt_archery, 20),
			(troop_raise_proficiency_linear, ":npc", wpt_throwing, 20),
			(troop_raise_attribute, ":npc", ca_strength, 2),
			(val_sub, ":wound_mask", wound_arm),
			(display_message, "@{s1}_recovered_from_a_serious_wound.", color_good_news),
			(display_message, "@The_arm_wound_has_healed."),
			(display_message, "@(+20_weapon_skill,_+2_strength,_+1_power_attacks)"),
		(else_try),
			(eq, ":rnd", 2),
			(store_and, ":check", ":wound_mask", wound_head), (neq, ":check", 0),
			#(store_skill_level,":skill",skl_trade          ,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_trade, ":x"),
			#(store_skill_level,":skill",skl_first_aid      ,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_first_aid, ":x"),
			#(store_skill_level,":skill",skl_surgery        ,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_surgery, ":x"),
			#(store_skill_level,":skill",skl_wound_treatment,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_wound_treatment, ":x"),
			#(store_skill_level,":skill",skl_pathfinding    ,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_pathfinding, ":x"),
			#(store_skill_level,":skill",skl_spotting       ,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_spotting, ":x"),
			#(store_skill_level,":skill",skl_tracking       ,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_tracking, ":x"),
			#(store_skill_level,":skill",skl_tactics        ,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_tactics, ":x"),
			#(store_skill_level,":skill",skl_trainer        ,":npc"),(assign,":x",10),(val_sub,":x",":skill"),(val_min,":x",1),(troop_raise_skill,":npc",skl_trainer, ":x"),
			(troop_raise_proficiency_linear, ":npc", wpt_archery, 15),
			(troop_raise_proficiency_linear, ":npc", wpt_throwing, 15),
			(val_sub, ":wound_mask", wound_head),
			(display_message, "@{s1}_recovered_from_a_serious_wound.", color_good_news),
			(display_message, "@The_head_wound_has_healed."),
			(display_message, "@(+1_intelligence_skills,_+15_missile_skill)"),
		(else_try),
			(eq, ":rnd", 3),
			(store_and, ":check", ":wound_mask", wound_chest), (neq, ":check", 0),
			(troop_raise_proficiency_linear, ":npc", wpt_one_handed_weapon, 20),
			(troop_raise_proficiency_linear, ":npc", wpt_two_handed_weapon, 20),
			(troop_raise_proficiency_linear, ":npc", wpt_polearm, 20),
			(troop_raise_proficiency_linear, ":npc", wpt_archery, 20),
			(troop_raise_proficiency_linear, ":npc", wpt_throwing, 20),
			(val_sub, ":wound_mask", wound_chest),
			(display_message, "@{s1}_recovered_from_a_serious_wound.", color_good_news),
			(display_message, "@The_cracked_ribs_have_healed."),
			(display_message, "@(+20_weapon_skill)"),
		(try_end),
		(troop_set_slot, ":npc", slot_troop_wound_mask, ":wound_mask"),
		(store_troop_health, ":x", ":npc", 0),
		(val_add, ":x", 10),
		(troop_set_health, ":npc", ":x"),
	(try_end),
 ]), 
#script_heal_party
("heal_party",[
	(store_random, ":rnd", 4),
	(try_begin),
		(eq, ":rnd", 0),
		(heal_party, "p_main_party"),
	(else_try),
		(try_for_range, ":npc", companions_begin, companions_end),
			(party_count_companions_of_type, ":num", "p_main_party", ":npc"),
			(eq, ":num", 1),
			(store_troop_health, ":hp", ":npc", 0),
			(val_mul, ":hp", 10),
			(val_div, ":hp", 7),
			(troop_set_health, ":npc", ":hp"),
		(try_end),
		(store_troop_health, ":hp", "trp_player", 0),
		(val_mul, ":hp", 10),
		(val_div, ":hp", 7),
		(troop_set_health, "trp_player", ":hp"),
	(try_end),
 ]), 
#script_optional_healing_boost
("cf_optional_healing_boost",[
	#(neg|eq, "$healing_boost_setting", 0),
	(try_begin),
		(store_troop_health, ":hp", "trp_player", 0),
	#    (try_begin),
	#        (eq, "$healing_boost_setting", 20),
			(val_mul, ":hp", 10),
			(val_div, ":hp", 8),
	#    (else_try),
	#        (eq, "$healing_boost_setting", 10),
	#        (val_mul, ":hp", 10),
	#        (val_div, ":hp", 9),
	#    (try_end),
		(troop_set_health, "trp_player", ":hp"),
	(try_end),
	(try_for_range, ":troop", companions_begin, companions_end),
		(troop_get_slot, ":local3", ":troop", 0),
		(eq, ":local3", 1),
		(store_troop_health, ":hp", ":troop", 0),
		(neg|ge, ":hp", 100),
	#    (try_begin),
	#        (eq, "$healing_boost_setting", 20),
			(val_mul, ":hp", 10),
			(val_div, ":hp", 8),
	#        (else_try),
	#        (eq, "$healing_boost_setting", 10),
	#        (val_mul, ":hp", 10),
	#        (val_div, ":hp", 9),
	#    (try_end),
		(troop_set_health, ":troop", ":hp"),
		(str_store_troop_name, s1, ":troop"),
		(display_message, "@{s1}_has_had_his_health_boosted", 0),
	(try_end),
 ]), 
#script_hero_leader_killed_abstractly
("hero_leader_killed_abstractly",[
	(store_script_param_1, ":hero"),
	(store_script_param_2, ":place"),
	(troop_set_slot, ":hero", slot_troop_wound_mask, wound_death),
	(str_store_troop_name, s1, ":hero"),
	(store_troop_faction,":fac",":hero"),
	(str_store_faction_name, s2, ":fac"),
    (assign, ":news_color", color_bad_news),
    (try_begin),
        (store_relation, ":rel", "$players_kingdom", ":fac"),
        (lt, ":rel", 0),
        (assign, ":news_color", color_good_news),
        (play_sound, "snd_enemy_lord_dies"),
	(else_try),
        (play_sound, "snd_lord_dies"),
	(try_end),
	(display_message, "@News_has_arrived_that_{s1}_of_{s2}_was_killed_in_battle!", ":news_color"),
	(call_script,"script_build_mound_for_dead_hero",":hero",":place"),
    (call_script, "script_update_troop_notes", ":hero"),
 ]),
#script_build_mound_for_dead_hero
("build_mound_for_dead_hero",[
	(store_script_param_1, ":hero"),
	(store_script_param_2, ":place"),
	(troop_set_slot, ":hero", slot_troop_wound_mask, wound_death),
	(str_store_troop_name, s1, ":hero"),
	(store_troop_faction,":fac",":hero"),
    (set_spawn_radius, 0),
	(try_begin),
		(faction_slot_eq, ":fac", slot_faction_side, faction_side_good),
		(spawn_around_party, ":place", "pt_mound"),
		(party_set_name, reg0, "@{s1}'s_Burial_Mound"),
	(else_try),
		(spawn_around_party, ":place", "pt_pyre"),
		(party_set_name, reg0, "@{s1}'s_Funeral_Pyre"),
	(try_end),
	#(party_set_faction,reg0,":fac"),
	(party_set_slot, reg0, slot_mound_state, 1),
	(party_set_slot, reg0, slot_party_commander_party, ":hero"),
 ]),
#script_display_dead_heroes
("display_dead_heroes",[
	(try_for_range, ":hero", heroes_begin, heroes_end),
		(troop_slot_eq, ":hero", slot_troop_wound_mask, wound_death),
		(str_store_troop_name, s1, ":hero"),
		(display_message, "@{s1}_is_logged_as_dead"),
	(try_end),
 ]),

############ HEALING AND DEATH FROM 808 ENDS ##############################################
############ RESCUE & STEALTH FROM 808 BEGINS##############################################

#script_rescue_information
("rescue_information",[
	(try_begin),
		(eq, "$rescue_stage", 0),
		(display_message, "@You_have_been_discovered_before_scaling_the_wall.", color_bad_news),
		(display_message, "@The_enemy_is_coming_in_force,_you_must_flee!", color_bad_news),
	  (else_try),
		(eq, "$rescue_stage", 1),
		(display_message, "@Scout_this_area_alone_and_meet_your_men_beyond!"),
		(display_message, "@Be_stealthy_but_eliminate_any_threats_quickly!"),
	  (else_try),
		(eq, "$rescue_stage", 2),
		(display_message, "@You_are_spotted_by_a_patrol!", color_bad_news),
		(display_message, "@Eliminate_them_before_the_alarm_spreads!", color_bad_news),
	  (else_try),
		(eq, "$rescue_stage", 3),
		(display_message, "@Scout_this_area_alone_and_meet_your_men_beyond!"),
		(display_message, "@Be_stealthy_but_eliminate_any_threats_quickly!"),
	  (else_try),
		(eq, "$rescue_stage", 4),
		(display_message, "@You_are_spotted_by_a_patrol!", color_bad_news),
		(display_message, "@Eliminate_them_before_the_alarm_spreads!", color_bad_news),
	  (else_try),
		(eq, "$rescue_stage", 5),
		(display_message, "@You_have_reached_the_dungeons!"),
		(display_message, "@Eliminate_the_guards_and_free_your_men!"),
	(try_end),
 ]), 
#script_initialize_general_rescue
("initialize_general_rescue",[
 ]),
#script_initialize_sorcerer_quest
("initialize_sorcerer_quest",[
	(store_random, "$meta_alarm", 10),
	(assign, "$rescue_courtyard_scene_1", "scn_tld_sorcerer_forest_a"),
	(assign, "$rescue_stealth_scene_1", "scn_tld_sorcerer_forest_b"),
	(assign, "$rescue_final_scene", "scn_tld_sorcerer_forest_c"),
	(assign, "$guard_troop1", "trp_orc_snaga_of_mordor"),
	(assign, "$guard_troop2", "trp_orc_of_mordor"),
	(assign, "$guard_troop3", "trp_orc_of_mordor"),
	(assign, "$guard_troop4", "trp_orc_of_mordor"),
	(assign, "$guard_troop5", "trp_orc_archer_of_mordor"),
	(assign, "$guard_troop6", "trp_black_numenorean_renegade"),
	(assign, "$guard_troop7", "trp_large_orc_of_mordor"),
	(assign, "$guard_troop8", "trp_fell_orc_of_mordor"),
	(assign, "$guard_troop9", "trp_black_numenorean_renegade"),
	(assign, "$guard_troop10", "trp_orc_of_mordor"),
 ]), 
#script_final_sorcerer_fight
("final_sorcerer_fight",[
	(set_jump_mission, "mt_sorcerer_mission"),
	(jump_to_scene, "$rescue_final_scene", 0),
	(reset_visitors),
	(modify_visitors_at_site, "$rescue_final_scene"),
	(call_script, "script_set_infiltration_companions"),
	(set_visitor, 10, "trp_black_numenorean_sorcerer", 0),
	(try_begin),
		(is_between, "$meta_alarm", 0, 4),
		(set_visitor, 11, "$guard_troop2", 0),(set_visitor, 12, "$guard_troop2", 0),(set_visitor, 13, "$guard_troop3", 0),(set_visitor, 14, "$guard_troop3", 0),(set_visitor, 15, "$guard_troop3", 0),(set_visitor, 16, "$guard_troop4", 0),(set_visitor, 17, "$guard_troop4", 0),(set_visitor, 18, "$guard_troop5", 0),(set_visitor, 19, "$guard_troop5", 0),(set_visitor, 20, "$guard_troop6", 0),
	(else_try),
		(is_between, "$meta_alarm", 4, 7),
		(set_visitor, 11, "$guard_troop3", 0),(set_visitor, 12, "$guard_troop3", 0),(set_visitor, 13, "$guard_troop4", 0),(set_visitor, 14, "$guard_troop4", 0),(set_visitor, 15, "$guard_troop4", 0),(set_visitor, 16, "$guard_troop5", 0),(set_visitor, 17, "$guard_troop5", 0),(set_visitor, 18, "$guard_troop6", 0),(set_visitor, 19, "$guard_troop6", 0),(set_visitor, 20, "$guard_troop7", 0),
	(else_try),
		(is_between, "$meta_alarm", 7, 9),
		(set_visitor, 11, "$guard_troop4", 0),(set_visitor, 12, "$guard_troop4", 0),(set_visitor, 13, "$guard_troop5", 0),(set_visitor, 14, "$guard_troop5", 0),(set_visitor, 15, "$guard_troop5", 0),(set_visitor, 16, "$guard_troop6", 0),(set_visitor, 17, "$guard_troop6", 0),(set_visitor, 18, "$guard_troop7", 0),(set_visitor, 19, "$guard_troop7", 0),(set_visitor, 20, "$guard_troop8", 0),
	(else_try),
		(ge, "$meta_alarm", 9),
		(set_visitor, 11, "$guard_troop5", 0),(set_visitor, 12, "$guard_troop6", 0),(set_visitor, 13, "$guard_troop6", 0),(set_visitor, 14, "$guard_troop7", 0),(set_visitor, 15, "$guard_troop7", 0),(set_visitor, 16, "$guard_troop8", 0),(set_visitor, 17, "$guard_troop8", 0),(set_visitor, 18, "$guard_troop9", 0),(set_visitor, 19, "$guard_troop10",0),(set_visitor, 20, "$guard_troop10",0),
	(try_end),
 ]),
#script_set_infiltration_companions
("set_infiltration_companions",[
	(set_visitor, 0, "trp_player", 0),
	(assign, ":entry", 0),
	(try_for_range, ":faction", "fac_mission_companion_1", "fac_mission_companion_10"),
		(faction_get_slot, ":kia", ":faction", slot_fcomp_kia),
		(faction_get_slot, ":troop", ":faction", slot_fcomp_troopid),
		(val_add, ":entry", 1),
		(neg|eq, ":troop", 0),
		(neg|eq, ":kia", 1),
		(set_visitor, ":entry", ":troop", 0),
	(try_end),
]), 
#script_set_infiltration_player_record
("set_infiltration_player_record",[
	(store_troop_health, ":hp", "trp_player", 0),
	(faction_set_slot, "fac_mission_companion_10", slot_fcomp_troopid, "trp_player"),
	(faction_set_slot, "fac_mission_companion_10", slot_fcomp_hp     , ":hp"),
]),
#script_infiltration_battle_wall
("infiltration_battle_wall",[
	(set_jump_mission, "mt_battle_wall_mission"),
	(jump_to_scene, "$rescue_wall_battle", 0),
	(reset_visitors),
	(modify_visitors_at_site, "$rescue_wall_battle"),
		(try_for_range, reg1, 10, 20),
		(store_random_in_range, reg2, 1, 6),
		(try_begin),(eq, reg2, 1),(assign, reg3, "$wall_mounted_troop1"),
		 (else_try),(eq, reg2, 2),(assign, reg3, "$guard_troop3"),
		 (else_try),(eq, reg2, 3),(assign, reg3, "$wall_mounted_troop3"),
		 (else_try),(eq, reg2, 4),(assign, reg3, "$guard_troop4"),
		 (else_try),(eq, reg2, 5),(assign, reg3, "$wall_mounted_troop5"),
		(try_end),
		(set_visitor, reg1, reg3, 0),
	(try_end),
	(try_for_range, reg1, 23, 27),
		(store_random_in_range, reg2, 1, 6),
		(try_begin),(eq, reg2, 1),(assign, reg3, "$wall_missile_troop1"),
		 (else_try),(eq, reg2, 2),(assign, reg3, "$wall_missile_troop2"),
		 (else_try),(eq, reg2, 3),(assign, reg3, "$wall_missile_troop3"),
		 (else_try),(eq, reg2, 4),(assign, reg3, "$wall_missile_troop4"),
		 (else_try),(eq, reg2, 5),(assign, reg3, "$wall_missile_troop5"),
		(try_end),
		(set_visitor, reg1, reg3, 0),
	(try_end),
	(call_script, "script_set_infiltration_companions"),
]), 
#script_infiltration_combat_1
("infiltration_combat_1",[
	(set_jump_mission, "mt_infiltration_combat_mission"),
	(jump_to_scene, "$rescue_courtyard_scene_1", 0),
	(reset_visitors),
	(modify_visitors_at_site, "$rescue_courtyard_scene_1"),
	(call_script, "script_set_infiltration_companions", 0, 0),
	(assign, reg1, "$guard_troop2"),
	(assign, reg2, "$guard_troop2"),
	(assign, reg3, "$guard_troop3"),
	(assign, reg4, "$guard_troop3"),
	(assign, reg5, "$guard_troop4"),
	(assign, reg5, "$guard_troop4"),
	(assign, reg7, "$guard_troop5"),
	(assign, reg8, "$guard_troop5"),
	(assign, reg9, "$guard_troop6"),
	(assign, reg10, "$guard_troop6"),
	(assign, reg11, "$guard_troop7"),
	(assign, reg12, "$guard_troop7"),
	(assign, reg13, "$guard_troop8"),
	(assign, reg14, "$guard_troop8"),
	(assign, reg15, "$guard_troop9"),
	(assign, reg16, "$guard_troop9"),
	(assign, reg17, "$guard_troop10"),
	(store_random_in_range, ":local0", 1, 6),
	(val_add, ":local0", "$meta_alarm"),
	(val_min, ":local0", 10),
	(val_add, ":local0", 10),
	(assign, ":local1", 7),
	(val_add, ":local1", "$meta_alarm"),
	(try_for_range, ":entry", 10, ":local0"),
		(shuffle_range, 1, ":local1"),
		(neg|eq, reg1, 0),
		(set_visitor, ":entry", reg1, 0),
	(try_end),
]), 
#script_infiltration_combat_2
("infiltration_combat_2",[
	(set_jump_mission, "mt_infiltration_combat_mission"),
	(jump_to_scene, "$rescue_courtyard_scene_2", 0),
	(reset_visitors),
	(modify_visitors_at_site, "$rescue_courtyard_scene_2"),
	(call_script, "script_set_infiltration_companions"),
	(assign, reg1, "$guard_troop2"),
	(assign, reg2, "$guard_troop2"),
	(assign, reg3, "$guard_troop3"),
	(assign, reg4, "$guard_troop3"),
	(assign, reg5, "$guard_troop4"),
	(assign, reg5, "$guard_troop4"),
	(assign, reg7, "$guard_troop5"),
	(assign, reg8, "$guard_troop5"),
	(assign, reg9, "$guard_troop6"),
	(assign, reg10, "$guard_troop6"),
	(assign, reg11, "$guard_troop7"),
	(assign, reg12, "$guard_troop7"),
	(assign, reg13, "$guard_troop8"),
	(assign, reg14, "$guard_troop8"),
	(assign, reg15, "$guard_troop9"),
	(assign, reg16, "$guard_troop9"),
	(assign, reg17, "$guard_troop10"),
	(store_random_in_range, ":local0", 1, 6),
	(val_add, ":local0", "$meta_alarm"),
	(val_min, ":local0", 10),
	(val_add, ":local0", 10),
	(assign, ":local1", 7),
	(val_add, ":local1", "$meta_alarm"),
	(try_for_range, ":entry", 10, ":local0"),
		(shuffle_range, 1, ":local1"),
		(neg|eq, reg1, 0),
		(set_visitor, ":entry", reg1, 0),
	(try_end),
]), 
#script_infiltration_stealth_1
("infiltration_stealth_1",[
	(set_jump_mission, "mt_infiltration_stealth_mission"),
	(jump_to_scene, "$rescue_final_scene", 0),
	(reset_visitors),
	(modify_visitors_at_site, "$rescue_final_scene"),
	(set_visitor, 0, "trp_player", 0),
	(set_visitor, 1, "$guard_troop2", 0),
	(set_visitor, 3, "$guard_troop2", 0),
	(set_visitor, 6, "$guard_troop2", 0),
	(set_visitor, 9, "$guard_troop2", 0),
	(set_visitor, 14, "$guard_troop2", 0),
	(set_visitor, 16, "$guard_troop2", 0),
	]), 
	#script_infiltration_stealth_2
	("infiltration_stealth_2",[
	(set_jump_mission, "mt_infiltration_stealth_mission"),
	(jump_to_scene, "$rescue_stealth_scene_1", 0),
	(reset_visitors),
	(modify_visitors_at_site, "$rescue_stealth_scene_1"),
	(set_visitor, 0, "trp_player", 0),
	(set_visitor, 1, "$guard_troop1", 0),
	(set_visitor, 3, "$guard_troop1", 0),
	(set_visitor, 6, "$guard_troop1", 0),
	(set_visitor, 9, "$guard_troop1", 0),
	(set_visitor, 14, "$guard_troop1", 0),
	(set_visitor, 16, "$guard_troop1", 0),
]),
#script_set_meta_stealth
("set_meta_stealth",[
	(assign, "$current_companions_total", 0),
	(assign, "$meta_stealth", 0),
	(try_for_range, ":faction", "fac_mission_companion_1", "fac_mission_companion_10"),
		(faction_get_slot, ":troop", ":faction", 1),
		(neg|eq, ":troop", 0),
		(store_skill_level, reg1, skl_pathfinding, ":troop"),
		(val_add, "$meta_stealth", reg1),
		(val_add, "$current_companions_total", 1),
	(try_end),
	(try_begin),
		(ge, "$current_companions_total", 1),
		(assign, reg2, "$current_companions_total"),
		(val_add, reg2, 1),
		(store_skill_level, reg1, skl_pathfinding, "trp_player"),
		(val_add, "$meta_stealth", reg1),
		(val_div, "$meta_stealth", reg2),
		# (try_begin),
			# (gt, "$pick_stage", 0),
			# (neg|ge, "$pick_stage", 3),
		# (else_try),
			# (ge, "$pick_stage", 3),
			# (neg|ge, "$pick_stage", 5),
			# (val_sub, "$meta_stealth", 1),
			# (val_max, "$meta_stealth", 0),
		# (else_try),
			# (ge, "$pick_stage", 5),
			# (neg|ge, "$pick_stage", 9),
			# (val_sub, "$meta_stealth", 2),
			# (val_max, "$meta_stealth", 0),
		# (else_try),
			# (ge, "$pick_stage", 9),
			# (val_sub, "$meta_stealth", 3),
			# (val_max, "$meta_stealth", 0),
		# (try_end),
	(else_try),
		(eq, "$current_companions_total", 0),
		(store_skill_level, reg1, skl_pathfinding, "trp_player"),
	#    (val_sub, reg1, "$old_ranger_path_modifier"),
		(val_add, "$meta_stealth", reg1),
		(val_add, "$meta_stealth", 2),
		(val_min, "$meta_stealth", 10),
	(try_end),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_stealthy, 1),
		(try_begin),(    eq, "$current_companions_total", 0),(val_add, "$meta_stealth", 3),
		 (else_try),(neg|eq, "$current_companions_total", 0),(val_add, "$meta_stealth", 1),
		(try_end),
	(try_end),
]), 
#script_crunch_stealth_results
("crunch_stealth_results",[
	(assign, reg10, "$meta_alarm"),
	(val_sub, reg10, "$meta_stealth"),
	(val_mul, reg10, 5),
	(store_random, reg5, 100),
	(val_add, reg5, reg10),
	(assign, reg11, "$meta_stealth"),
	(assign, reg12, "$meta_alarm"),
	(assign, reg14, reg10),
	(assign, reg13, reg5),
	(try_begin),    (neg|ge, reg5, 15),    (assign, "$stealth_results", 1),
	 (else_try),(is_between, reg5, 15, 50),(assign, "$stealth_results", 2),
	 (else_try),(is_between, reg5, 50, 85),(assign, "$stealth_results", 3),
	 (else_try),        (ge, reg5, 85),    (assign, "$stealth_results", 4),
	(try_end),
]), 
#script_rescue_information
("rescue_information",[
	(try_begin),
		(eq, "$rescue_stage", 0),
		(display_message, "@You_have_been_discovered_before_scaling_the_wall.", 4294901760),
		(display_message, "@The_enemy_is_coming_in_force,_you_must_flee!", 4294901760),
	  (else_try),
		(eq, "$rescue_stage", 1),
		(display_message, "@Scout_this_area_alone_and_meet_your_men_beyond!", 4294901760),
		(display_message, "@Be_stealthy_but_eliminate_any_threats_quickly!", 4294901760),
	  (else_try),
		(eq, "$rescue_stage", 2),
		(display_message, "@You_are_spotted_by_a_patrol!", 4294901760),
		(display_message, "@Eliminate_them_before_the_alarm_spreads!", 4294901760),
	  (else_try),
		(eq, "$rescue_stage", 3),
		(display_message, "@Scout_this_area_alone_and_meet_your_men_beyond!", 4294901760),
		(display_message, "@Be_stealthy_but_eliminate_any_threats_quickly!", 4294901760),
	  (else_try),
		(eq, "$rescue_stage", 4),
		(display_message, "@You_are_spotted_by_a_patrol!", 4294901760),
		(display_message, "@Eliminate_them_before_the_alarm_spreads!", 4294901760),
	  (else_try),
		(eq, "$rescue_stage", 5),
		(display_message, "@You_have_reached_the_dungeons!", 0),
		(display_message, "@Eliminate_the_guards_and_free_your_men!", 0),
	(try_end),
]), 
#script_infiltration_mission_final_casualty_tabulation
("infiltration_mission_final_casualty_tabulation",[
	(try_for_range, ":faction", "fac_mission_companion_1", "fac_mission_companion_11"),
		(faction_get_slot, ":troop", ":faction", slot_fcomp_agentid),
		(faction_get_slot, ":local2", ":faction", slot_fcomp_hp),
		(faction_get_slot, ":local3", ":faction", slot_fcomp_kia),
		(try_begin),
			(troop_is_hero, ":troop"),
			(store_random_in_range, ":rnd", 20, 30),
			(try_begin),
				(eq, ":faction", "fac_mission_companion_10"),
				(neg|gt, ":rnd", ":local2"),
				(troop_set_health, ":troop", ":local2"),
			  (else_try),
				(eq, ":faction", "fac_mission_companion_10"),
				(gt, ":rnd", ":local2"),
				(troop_set_health, ":troop", ":rnd"),
			  (else_try),
				(neg|eq, ":troop", 0),
				(gt, ":rnd", ":local2"),
				(troop_set_health, ":troop", ":rnd"),
			  (else_try),
				(neg|eq, ":troop", 0),
				(neg|gt, ":rnd", ":local2"),
				(troop_set_health, ":troop", ":local2"),
			(try_end),
		  (else_try),
			(neg|troop_is_hero, ":troop"),
			(eq, ":local3", 1),
			(party_remove_members, "p_main_party", ":troop", 1),
		(try_end),
	(try_end),
]), 
#script_infiltration_initialize_companion_records
("infiltration_initialize_companion_records",[
	(try_for_range, ":faction", "fac_mission_companion_1", "fac_mission_companion_11"),
		(faction_set_slot, ":faction", slot_fcomp_troopid, 0), # troop ID
		(faction_set_slot, ":faction", slot_fcomp_agentid, 0), # agent ID
		(faction_set_slot, ":faction", slot_fcomp_hp, 0), # current hp
		(faction_set_slot, ":faction", slot_fcomp_kia, 0), # kia = 1
	(try_end),
]),
#script_infiltration_mission_update_companion_casualties
("infiltration_mission_update_companion_casualties",[
	#(faction_get_slot, ":compagent", "fac_mission_companion_10", slot_fcomp_agentid),
	(faction_get_slot, ":local1", "fac_mission_companion_10", slot_fcomp_hp),
	(store_agent_hit_points, ":hp", "$current_player_agent", 0),
	(try_begin),
		(neg|ge, ":hp", ":local1"),
		(faction_set_slot, "fac_mission_companion_10", slot_fcomp_hp, ":hp"),
	(try_end),
	#(get_player_agent_no, ":player"),
	(try_for_agents, ":agent"),
		(agent_is_ally, ":agent"),
		(agent_is_human, ":agent"),
		(neg|eq, ":agent", "$current_player_agent"),
		(store_agent_hit_points, ":hp", ":agent", 0),
	#    (agent_get_troop_id, ":local4", ":agent"),
		(try_begin),
			(agent_is_alive|neg, ":agent"),
			(try_for_range, ":fac", "fac_mission_companion_1", "fac_mission_companion_10"),
				(faction_get_slot, ":compagent", ":fac", slot_fcomp_agentid),
				(faction_get_slot, ":local6", ":fac", slot_fcomp_kia),
				(neg|eq, ":local6", 1),
				(eq, ":compagent", ":agent"),
				(faction_set_slot, ":fac", slot_fcomp_hp, ":hp"),
				(faction_set_slot, ":fac", slot_fcomp_kia, 1),
			(try_end),
		(else_try),
			(agent_is_alive, ":agent"),
			(try_for_range, ":fac", "fac_mission_companion_1", "fac_mission_companion_10"),
				(faction_get_slot, ":compagent", ":fac", slot_fcomp_agentid),
				(eq, ":compagent", ":agent"),
				(faction_get_slot, ":local1", ":fac", slot_fcomp_hp),
				(neg|ge, ":hp", ":local1"),
				(faction_set_slot, ":fac", slot_fcomp_hp, ":hp"),
			(try_end),
		(try_end),
	(try_end),
]), 
#script_infiltration_mission_synch_agents_and_troops
("infiltration_mission_synch_agents_and_troops",[
	(try_for_range, ":fac", "fac_mission_companion_1", "fac_mission_companion_10"),
		(faction_set_slot, ":fac", slot_fcomp_agentid, 0),
	(try_end),
	(get_player_agent_no, "$current_player_agent"),
	(faction_set_slot, "fac_mission_companion_10", slot_fcomp_agentid, "$current_player_agent"),
	(try_for_agents, ":agent"),
		(neg|eq, ":agent", "$current_player_agent"),
		(agent_is_ally, ":agent"),
		(agent_is_human, ":agent"),
		(agent_get_troop_id, ":troop", ":agent"),
			(try_for_range, ":fac", "fac_mission_companion_1", "fac_mission_companion_10"),
			(faction_get_slot, ":troop_comp", ":fac", slot_fcomp_troopid),
			(faction_get_slot, ":local4", ":fac", slot_fcomp_agentid),
			(faction_get_slot, ":local5", ":fac", slot_fcomp_kia),
			(neg|eq, ":local5", 1), # not kia
			(eq, ":local4", 0),
			(eq, ":troop_comp", ":troop"),
			(assign, ":local6", 0),
			(try_for_range, ":facc", "fac_mission_companion_1", "fac_mission_companion_10"),
				(faction_get_slot, ":agent2", ":facc", slot_fcomp_agentid),
				(eq, ":agent2", ":agent"),
				(assign, ":local6", 1),
			(try_end),
			(eq, ":local6", 0),
			(faction_set_slot, ":fac", slot_fcomp_agentid, ":agent"),
		(try_end),
	(try_end),
]),
#script_infiltration_mission_set_hit_points
("infiltration_mission_set_hit_points",[
	#(get_player_agent_no, ":player"),
	(try_for_range, ":comp", "fac_mission_companion_1", "fac_mission_companion_10"),
		(faction_get_slot, ":comp_agent", ":comp", slot_fcomp_agentid),
		(faction_get_slot, ":local3", ":comp", slot_fcomp_kia),
		(faction_get_slot, ":hp", ":comp", slot_fcomp_hp),
		(faction_get_slot, ":troop", ":comp", slot_fcomp_troopid),
		(try_begin),
			(neg|eq, ":comp_agent", "$current_player_agent"),
			(neg|eq, ":troop", 0),
			(neg|eq, ":local3", 1),
			(agent_set_hit_points, ":comp_agent", ":hp", 0),
		(try_end),
	#    (faction_get_slot, ":comp_agent", "fac_mission_companion_10", slot_fcomp_agentid),
		(faction_get_slot, ":hp", "fac_mission_companion_10", slot_fcomp_hp),
		(agent_set_hit_points, "$current_player_agent", ":hp", 0),
	(try_end),
]),
#script_rescue_failed
("rescue_failed",[
	(assign, ":local0", 0),
	(assign, ":comp_captured", 0),
	(try_begin),(eq, "$active_rescue", 1),(assign, ":local0", 1),
	 (else_try),(eq, "$active_rescue", 2),(assign, ":local0", 2),
	 (else_try),(eq, "$active_rescue", 3),(assign, ":local0", 3),
	 (else_try),(eq, "$active_rescue", 4),(assign, ":local0", 4),
	(try_end),
	(try_begin),
		(lt, "$active_rescue", 5),
		(neq, ":local0", 0),
		(assign, ":comp_captured", 0),
		(try_for_range, ":comp", "fac_mission_companion_1", "fac_mission_companion_10"),
			(assign, ":local3", 0),
	#		(faction_get_slot, ":local4", ":comp", slot_fcomp_hp),
			(faction_get_slot, ":local5", ":comp", slot_fcomp_kia),
			(faction_get_slot, ":troop_comp", ":comp", slot_fcomp_troopid),
			(eq, ":local5", 1),
			(try_for_range, ":npc", "trp_npc1", "trp_heroes_end"),
				(eq, ":troop_comp", ":npc"),
				(assign, ":local8", ":local0"),
				(val_add, ":local8", 5),
				(troop_set_slot, ":npc", 0, ":local8"),
				(assign, ":local3", 1),
				(party_remove_members, "p_main_party", ":npc", 1),
				(str_store_troop_name, s1, ":npc"),
				(display_message, "@{s1}_has_been_captured_by_the_enemy.", 4294901760),
				(try_begin),
					(eq, ":local3", 1),
					(eq, ":local0", 1),
	#				(val_add, "$heroes_captured_by_gondor", 1),
					(val_add, ":comp_captured", 1),
					(str_store_party_name, s2, "p_town_minas_tirith"),
					(display_message, "@Gondor_takes_a_captive"),
				(else_try),
					(eq, ":local3", 1),
					(eq, ":local0", 2),
	#				(val_add, "$heroes_captured_by_rohan", 1),
					(val_add, ":comp_captured", 1),
					(str_store_party_name, s2, "p_town_hornburg"),
					(display_message, "@Rohan_takes_a_captive"),
				(else_try),
					(eq, ":local3", 1),
					(eq, ":local0", 3),
	#				(val_add, "$heroes_captured_by_mordor", 1),
					(val_add, ":comp_captured", 1),
					(str_store_party_name, s2, "p_town_minas_morgul"),
					(display_message, "@Mordor_takes_a_captive"),
				(else_try),
					(eq, ":local3", 1),
					(eq, ":local0", 4),
	#				(val_add, "$heroes_captured_by_isengard", 1),
					(val_add, ":comp_captured", 1),
					(str_store_party_name, s2, "p_town_isengard"),
					(display_message, "@Isengard_takes_a_captive"),
				(try_end),
			(try_end),
		(try_end),
	(try_end),
	(try_begin),
		(lt, "$active_rescue", 5),
		(neq, ":local0", 0),
		(try_begin),
			(eq, "$current_companions_total", 0),
			(tutorial_box, "@You_were_grievously_wounded_and_your_body_piled_with_the_dead._Picking_your_moment_you_managed_to_escape_over_the_wall_but_the_enemy_may_have_seen_your_movements._Best_to_be_quickly_away."),
		(else_try),
			(eq, ":comp_captured", 1),
			(tutorial_box, "@You_were_grievously_wounded_in_battle._Your_men_managed_to_drag_you_away_but_took_horrific_casualties_in_the_effort."),
		(else_try),
			(gt, ":comp_captured", 1),
			(tutorial_box, "@You_were_grievously_wounded_in_battle._Your_men_managed_to_drag_you_away_but_took_horrific_casualties_in_the_effort._Unfortunately,_some_of_your_companions_have_been_captured and dragged to {s2}."),
		(try_end),
	(else_try),
		(eq, "$active_rescue", 5), # Mirkwood sorcerer
		(try_begin),
			(gt, "$current_companions_total", 0),
			(tutorial_box, "@You_were_grievously_wounded_in_battle._Your_men_managed_to_drag_you_away_from_the_fighting,_but_unfortunately_the_sorcerer_has_managed_to_escape."),
		(else_try),
			(eq, "$current_companions_total", 0),
			(tutorial_box, "@You_were_grievously_wounded_and_your_body_piled_with_the_dead._Picking_the_right_moment_you_managed_to_escape,_but_unfortunately_the_sorcerer_has_managed_to_escape."),
		(try_end),
		(try_begin),
			(check_quest_active, "qst_mirkwood_sorcerer"),
			(call_script, "script_fail_quest", "qst_mirkwood_sorcerer"),
		(try_end),		
	(try_end),
]),
#script_store_hero_death
("store_hero_death",[
	(assign, "$no_dead_companions", 0),
	(get_player_agent_no, "$current_player_agent"),
	(try_for_agents, ":agent"),
		(agent_is_human, ":agent"),
		(agent_is_ally, ":agent"),
		(neg|eq, ":agent", "$current_player_agent"),
		(agent_is_alive|neg, ":agent"),
		(val_add, "$no_dead_companions", 1),
	(try_end),
	(try_for_range, ":comp", "fac_mission_companion_1", "fac_mission_companion_10"),
		(faction_get_slot, ":local5", ":comp", slot_fcomp_kia),
		(eq, ":local5", 1),
		(faction_get_slot, ":troop_comp", ":comp", slot_fcomp_troopid),
		(neg|troop_is_hero, ":troop_comp"),
		(gt, "$no_dead_companions", 0),
		(val_sub, "$no_dead_companions", 1),
	(try_end),
]), 
#script_mt_sneak_1
("mt_sneak_1",[
	(store_script_param_1, ":enemy_agent"),
	(try_begin),(eq, "$positions", 3),(eq, "$last_agent_position", 2),(agent_set_scripted_destination, ":enemy_agent", 2),
	 (else_try),(eq, "$positions", 2),(eq, "$last_agent_position", 3),(agent_set_scripted_destination, ":enemy_agent", 1),
	 (else_try),(eq, "$positions", 7),(eq, "$last_agent_position", 6),(agent_set_scripted_destination, ":enemy_agent", 6),
	 (else_try),(eq, "$positions", 5),(eq, "$last_agent_position", 7),(agent_set_scripted_destination, ":enemy_agent", 4),
	 (else_try),(eq, "$positions",11),(agent_set_scripted_destination, ":enemy_agent", 8),
	 (else_try),(eq, "$positions",15),(agent_set_scripted_destination, ":enemy_agent", 14),
	 (else_try),(eq, "$positions",19),(agent_set_scripted_destination, ":enemy_agent", 17),
	 (else_try),(eq, "$positions",16),(agent_set_scripted_destination, ":enemy_agent", 20),
	 (else_try),(eq, "$positions",20),(agent_set_scripted_destination, ":enemy_agent", 16),
	 (else_try),(assign, reg20, "$positions"),(val_add, reg20, 1),(agent_set_scripted_destination, ":enemy_agent", reg20),
	(try_end),
]), 
#script_mt_sneak_2
("mt_sneak_2",[
	(store_script_param_1, ":enemy_agent"),
	(try_begin),(eq, "$positions", 4),(agent_set_scripted_destination, ":enemy_agent", 1),
	 (else_try),(eq, "$positions", 8),(agent_set_scripted_destination, ":enemy_agent", 5),
	 (else_try),(eq, "$positions", 14),(eq, "$last_agent_position", 13),(agent_set_scripted_destination, ":enemy_agent", 13),
	 (else_try),(eq, "$positions", 13),(eq, "$last_agent_position", 14),(agent_set_scripted_destination, ":enemy_agent", 12),
	 (else_try),(eq, "$positions", 12),(eq, "$last_agent_position", 13),(agent_set_scripted_destination, ":enemy_agent", 11),
	 (else_try),(eq, "$positions", 11),(eq, "$last_agent_position", 12),(agent_set_scripted_destination, ":enemy_agent", 10),
	 (else_try),(eq, "$positions", 10),(eq, "$last_agent_position", 11),(agent_set_scripted_destination, ":enemy_agent", 9),
	 (else_try),(eq, "$positions", 20),(eq, "$last_agent_position", 19),(agent_set_scripted_destination, ":enemy_agent", 19),
	 (else_try),(eq, "$positions", 19),(eq, "$last_agent_position", 20),(agent_set_scripted_destination, ":enemy_agent", 16),
	 (else_try),(eq, "$positions", 16),(eq, "$last_agent_position", 19),(agent_set_scripted_destination, ":enemy_agent", 15),
	 (else_try),(assign, reg20, "$positions"),(val_add, reg20, 1),(agent_set_scripted_destination, ":enemy_agent", reg20),
	(try_end),
]), 
#script_isen_sneak_1
("isen_sneak_1",[
	(store_script_param_1, ":enemy_agent"),
	(try_begin),(eq, "$positions", 1),(agent_set_scripted_destination, ":enemy_agent", 2),
	 (else_try),(eq, "$positions", 2),(agent_set_scripted_destination, ":enemy_agent", 1),
	 (else_try),(eq, "$positions", 3),(agent_set_scripted_destination, ":enemy_agent", 4),
	 (else_try),(eq, "$positions", 4),(agent_set_scripted_destination, ":enemy_agent", 3),
	 (else_try),(eq, "$positions", 6),(agent_set_scripted_destination, ":enemy_agent", 7),
	 (else_try),(eq, "$positions", 7),(agent_set_scripted_destination, ":enemy_agent", 6),
	 (else_try),(eq, "$positions", 9),(agent_set_scripted_destination, ":enemy_agent",10),
	 (else_try),(eq, "$positions",10),(agent_set_scripted_destination, ":enemy_agent", 9),
	 (else_try),(eq, "$positions",14),(agent_set_scripted_destination, ":enemy_agent",15),
	 (else_try),(eq, "$positions",15),(agent_set_scripted_destination, ":enemy_agent",14),
	 (else_try),(eq, "$positions",16),(agent_set_scripted_destination, ":enemy_agent",17),
	 (else_try),(eq, "$positions",17),(agent_set_scripted_destination, ":enemy_agent",16),
	 (else_try),(assign, reg20, "$positions"),(val_add, reg20, 1),(agent_set_scripted_destination, ":enemy_agent", reg20),
	(try_end),
]),
#script_wounded_hero_cap_mission_health
("wounded_hero_cap_mission_health",[
	(get_player_agent_no, ":player"),
	(assign, ":local1", 0),
	(try_for_agents, ":agent"),
		(neg|eq, ":agent", ":player"),
		(agent_is_human, ":agent"),
		(agent_is_ally, ":agent"),
		(agent_get_troop_id, ":local2", ":agent"),
		(try_for_range, ":npc", companions_begin, companions_end),
			(eq, ":local2", ":npc"),
			(troop_get_slot, ":local4", ":npc", slot_troop_wound_mask),
			(assign, ":hp", 100),
			(val_mul, ":local4", 10),
			(val_sub, ":hp", ":local4"),
			(store_agent_hit_points, ":hp_cur", ":agent", 0),
			(neg|ge, ":hp", ":hp_cur"),
			(agent_set_hit_points, ":agent", ":hp", 0),
			(assign, ":local1", 1),
		(try_end),
	(try_end),
	(try_begin),
		(eq, ":local1", 1),
		(display_message, "@Some_of_your_companions_are_suffering_from_old_wounds.", 4294901760),
	(try_end),
]),
#script_set_hero_companion
("set_hero_companion",[
	(store_script_param_1, ":comp_troop"),
	(try_begin), # store horoes actual health
		(troop_is_hero, ":comp_troop"),
		(store_troop_health, ":hp", ":comp_troop", 0),
	(else_try),
		(assign, ":hp", 100),
	(try_end),
	(store_add, ":comp", "fac_mission_companion_1", reg0), # reg0 traces total # of companions picked
	(faction_set_slot, ":comp", slot_fcomp_troopid, ":comp_troop"),
	(faction_set_slot, ":comp", slot_fcomp_hp, ":hp"),
	(faction_set_slot, ":comp", slot_fcomp_kia, 0),
	(val_add, reg0,1), # one more companion added
]), 


#script_initialize_center_scene
#GA: transferred from town menu so that can double it elsewhere
("initialize_center_scene",[
	(assign, "$talk_context", 0),
	(try_begin),
		(call_script, "script_cf_enter_center_location_bandit_check"),
	(else_try),
		(party_get_slot, ":town_scene", "$current_town", slot_town_center),
		(modify_visitors_at_site, ":town_scene"),
		(reset_visitors),
		(assign, "$g_mt_mode", tcm_default),
		(store_faction_of_party, ":town_faction","$current_town"),
        
		# TLD center specific guards
		(try_begin),
			(neg|party_slot_eq,"$current_town", slot_town_prison, -1),
			(party_get_slot, ":troop_prison_guard", "$current_town", slot_town_prison_guard_troop),
		(else_try),
			(party_get_slot, ":troop_prison_guard", "$current_town", slot_town_guard_troop),
		(try_end),
		(try_begin),
			(neg|party_slot_eq,"$current_town", slot_town_castle, -1),
			(party_get_slot, ":troop_castle_guard", "$current_town", slot_town_castle_guard_troop),
		(else_try),
			(party_get_slot, ":troop_castle_guard", "$current_town", slot_town_guard_troop),
		(try_end),
		(set_visitor, 23, ":troop_castle_guard"),
		(set_visitor, 24, ":troop_prison_guard"),
        
        # TLD center specific guards
        (party_get_slot, ":tier_2_troop", "$current_town", slot_town_guard_troop),
        (party_get_slot, ":tier_3_troop", "$current_town", slot_town_guard_troop), #was slot_town_prison_guard_troop
        ########
        (try_begin),
            (gt,":tier_2_troop", 0),
            (assign,reg0,":tier_3_troop"),(assign,reg1,":tier_3_troop"),(assign,reg2,":tier_2_troop"),(assign,reg3,":tier_2_troop"),
        (else_try),
            (assign,reg0,"trp_gondor_swordsmen"),(assign,reg1,"trp_gondor_swordsmen"),(assign,reg2,"trp_archer_of_gondor"),(assign,reg3,"trp_footman_of_rohan"),
        (try_end),
        (shuffle_range,0,4),
        (set_visitor,25,reg0),(set_visitor,26,reg1),(set_visitor,27,reg2),(set_visitor,28,reg3),

        #MV replaced by companion NPC, if any, and no castle
        #TLD NPC companions
        (try_begin),
            (party_slot_eq, "$current_town", slot_town_castle, -1), #no town castle
            (neq, "$sneaked_into_town", 1), #haven't sneaked in
            (try_for_range, ":cur_troop", companions_begin, companions_end),
                (troop_slot_eq, ":cur_troop", slot_troop_cur_center, "$current_town"),
                (neg|main_party_has_troop, ":cur_troop"), #not already hired
                (assign, ":on_lease", 0),
                (try_begin),
                    (check_quest_active,"qst_lend_companion"),
                    (quest_slot_eq, "qst_lend_companion", slot_quest_target_troop, ":cur_troop"),
                    (assign, ":on_lease", 1),
                (try_end),
                (eq, ":on_lease", 0),
                (store_troop_faction, ":troop_faction", ":cur_troop"),
                (store_relation, ":rel", ":town_faction", ":troop_faction"),
                (ge, ":rel", 0), #only spawn if friendly center
                (set_visitor, 9, ":cur_troop"), #only one companion NPC per town!
            (try_end),
        (try_end),

        (party_get_slot, ":spawned_troop", "$current_town", slot_town_weaponsmith),
        (try_begin),
            (neq, ":spawned_troop", "trp_no_troop"),
            (set_visitor, 10, ":spawned_troop"),
        (try_end),
        (party_get_slot, ":spawned_troop", "$current_town", slot_town_elder),
        (try_begin),
            (neq, ":spawned_troop", "trp_no_troop"),
            (set_visitor, 11, ":spawned_troop"),
        (try_end),
        (party_get_slot, ":spawned_troop", "$current_town", slot_town_merchant),
        (try_begin),
            (neq, ":spawned_troop", "trp_no_troop"),
            (set_visitor, 12, ":spawned_troop"),
        (try_end),
                 
        #TLD: lords in the streets 16-22, if no castle
        (try_begin),
            (party_slot_eq, "$current_town", slot_town_castle, -1), #no town castle
            (assign, ":cur_pos", 16),
            (call_script, "script_get_heroes_attached_to_center", "$current_town", "p_temp_party"),
            (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
            (try_for_range, ":i_stack", 0, ":num_stacks"),
                (party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),
                (lt, ":cur_pos", 23), # spawn up to entry point 22
                (set_visitor, ":cur_pos", ":stack_troop"),
                (try_begin),
                    (this_or_next|eq, ":stack_troop", "trp_knight_3_11"), #imladris elves all in helms
                    (this_or_next|eq, ":stack_troop", "trp_knight_3_12"),
                    (this_or_next|eq, ":stack_troop", "trp_imladris_lord"),
                                 (eq, ":stack_troop", "trp_lorien_lord"), #Galadriel in her invis peryphery
                    (mission_tpl_entry_set_override_flags, "mt_town_center", ":cur_pos", af_override_horse|af_override_weapons),
                (try_end),
                (val_add,":cur_pos", 1),
            (try_end),
        (try_end),

        (try_begin), #TLD: fugitive in a town
            (check_quest_active, "qst_hunt_down_fugitive"),
            #(neg|is_currently_night),
            (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
            (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
            (neg|check_quest_failed, "qst_hunt_down_fugitive"),
            (quest_get_slot, ":quest_object_troop", "qst_hunt_down_fugitive", slot_quest_object_troop),
            (set_visitor, 9, ":quest_object_troop"), #spawn in place of any NPC companion, so sceners won't make a fuss 
        (try_end),

        (call_script, "script_init_town_walkers"),
        (set_jump_mission,"mt_town_center"),
        (assign, ":override_state", af_override_horse),
        (try_begin),
            (eq, "$sneaked_into_town", 1), #setup disguise
            (assign, ":override_state", af_override_all),
        (try_end),
        (mission_tpl_entry_set_override_flags, "mt_town_center", 0, ":override_state"), #entry 0 always in center & w/o horse
        (try_begin),
            (this_or_next|eq, "$current_town", "p_town_moria"), #no mounts in cave towns
            (eq, "$current_town", "p_town_erebor"),
            (mission_tpl_entry_set_override_flags, "mt_town_center", 1, ":override_state"),
            (mission_tpl_entry_set_override_flags, "mt_town_center", 2, ":override_state"),
        (try_end),
        (mission_tpl_entry_set_override_flags, "mt_town_center", 3, ":override_state"),
        (mission_tpl_entry_set_override_flags, "mt_town_center", 4, ":override_state"),
        (mission_tpl_entry_set_override_flags, "mt_town_center", 5, ":override_state"),
        (mission_tpl_entry_set_override_flags, "mt_town_center", 6, ":override_state"),
        (mission_tpl_entry_set_override_flags, "mt_town_center", 7, ":override_state"),
    (try_end), #if bandits
]),

# script_calculate_renown_value
# Input: arg1 = troop_no
# Output: fills $battle_renown_value
("calculate_renown_value",
   [  (call_script, "script_party_calculate_strength", "p_main_party", 0),
      (assign, ":main_party_strength", reg0),
      (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
      (assign, ":enemy_strength", reg0),
      (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
      (assign, ":friends_strength", reg0),

      (val_add, ":friends_strength", 1),
      (store_mul, ":enemy_strength_ratio", ":enemy_strength", 100),
      (val_div, ":enemy_strength_ratio", ":friends_strength"),

      (assign, ":renown_val", ":enemy_strength"),
      (val_mul, ":renown_val", ":enemy_strength_ratio"),
      (val_div, ":renown_val", 100),

      (val_mul, ":renown_val", ":main_party_strength"),
      (val_div, ":renown_val",":friends_strength"),

      (store_div, "$battle_renown_value", ":renown_val", 5),
      (val_min, "$battle_renown_value", 2500),
      (convert_to_fixed_point, "$battle_renown_value"),
      (store_sqrt, "$battle_renown_value", "$battle_renown_value"),
      (convert_from_fixed_point, "$battle_renown_value"),
      (assign, reg8, "$battle_renown_value"),
      #(display_message, "@Renown value for this battle is {reg8}.",0xFFFFFFFF),
]),
  
# script_injure_companions
("injure_companions",[
 	 (try_begin),
		(eq, "$tld_option_injuries",1),
		(try_for_range, ":npc",companions_begin,companions_end), # assume companions are always in our main party, if ever spawned on battlefield
			(troop_slot_eq, ":npc", slot_troop_wounded, 1), # was wounded in this battle?
			(call_script, "script_injury_routine", ":npc"),
			(troop_set_slot,":npc", slot_troop_wounded, 0),
		(try_end),
	(try_end),  
]),

#script_check_equipped_items
("check_equipped_items",[
	(store_script_param_1, ":npc"),
	(assign,"$remove_item", 0),
	(troop_get_type, ":race", ":npc"),
	(try_for_range,":inv_slot",ek_body,ek_gloves), 			# EQUIPMENT CHECKS
		(troop_get_inventory_slot, ":item", ":npc", ":inv_slot"),
		(ge, ":item", 0),
		(store_add,":item_slot",slot_troop_armor_type-ek_body,":inv_slot"), #slot_troop_armor_type, slot_troop_boots_type consequtive slots
		(neg|troop_slot_eq,":npc",":item_slot",":item"), # equipped item changed to other?
		(store_item_value, reg30, ":item"),
		(val_mod, reg30,10),
		(neq, reg30, 0), # non-commonly used item? (item value last digit !=0, stores allowed races)
		(try_begin),(eq,reg30,8),(neq,":race",tf_dwarf  ),(assign,"$remove_item",1),
		 (else_try),(eq,reg30,1),(neq,":race",tf_orc    ),(assign,"$remove_item",1),
		 (else_try),(eq,reg30,2),(neq,":race",tf_uruk   ),(assign,"$remove_item",1),
		 (else_try),(eq,reg30,4),(neq,":race",tf_urukhai),(assign,"$remove_item",1),
		(try_end),
		(try_begin),
			(eq,"$remove_item",1),
			(dialog_box,"@Item you just equipped does not fit characters of this race and will be removed into player inventory shortly^^Make sure your equipment has space for the item, or it will be lost","@Inappropriate equipment"),
			(troop_set_slot,":npc",":item_slot",-1),		# needs removing!
		(else_try),
			(troop_set_slot,":npc",":item_slot", ":item"),	#remember new equipment
		(try_end),
	(try_end),
	
	# check for mount, issue warning if wrong
	(troop_get_inventory_slot, ":item", ":npc", ek_horse),
	(try_begin),
		(neg|troop_slot_eq,":npc",slot_troop_horse_type,":item"), # mount changed from previous?
		#(display_message, "@WOAH, MOUNT CHANGED!!"),
		(troop_set_slot,":npc",slot_troop_horse_type, ":item"), # remember new mount (it's not removed)
		(try_begin),
			(ge, ":item", 0),
			(call_script, "script_cf_troop_cant_ride_item",  ":npc", ":item"),
			(assign,"$remove_item", 1),
			(dialog_box,"@The mount you just equipped does not fit characters of this race. Be warned that there will be problems with the animal behaviour on the battlefield, if you leave it as this","@Inappropriate mount"),
		(try_end),
	(try_end),
]),
("unequip_items",[
	(store_script_param_1, ":npc"),
	(try_begin),
		(eq,"$tld_option_crossdressing",0),
		(eq,"$remove_item",1),
		(try_for_range,":inv_slot",ek_body,ek_gloves),				# CHECKS FOR EQUIPMENT REMOVAL for body and feet
			(troop_get_inventory_slot, ":item", ":npc", ":inv_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":mod", ":npc", ":inv_slot"),
			(store_add,":item_slot",slot_troop_armor_type-ek_body,":inv_slot"),
			(troop_slot_eq,":npc",":item_slot", -1), 				# item marked for removal?
			(troop_set_inventory_slot, ":npc", ":inv_slot", -1),	# remove item from equipment
			(troop_add_item, "trp_player", ":item", ":mod"),		# move item into player's inventory
		(try_end),
		(troop_get_inventory_slot, ":item", ":npc", ek_horse),
		(troop_set_slot,":npc",slot_troop_horse_type, ":item"),
		(assign,"$remove_item", 0),
	(try_end),
]),

#script_battle_health_management
#MV: copied over from 808 for use in a trigger for berserker and inf/arch/cav captain traits
("battle_health_management",[

	#don't do this, we want to heal only player troops on his command
	# (try_for_agents, ":agent"), # berserkers heal
		# (agent_is_alive, ":agent"),
		# (agent_get_troop_id, ":troop", ":agent"),
		# (this_or_next|eq, ":troop", "trp_dunnish_wolf_warrior"),
		# (this_or_next|eq, ":troop", "trp_dunnish_berserker"),
		# (this_or_next|eq, ":troop", "trp_fighting_uruk_hai_berserker"),
		# (this_or_next|eq, ":troop", "trp_variag_pitfighter"),
					 # (eq, ":troop", "trp_variag_gladiator"),
		# (store_agent_hit_points, ":hp", ":agent", 0),
		# (neg|ge, ":hp", 50),
		# (val_mul, ":hp", 10),
		# (val_div, ":hp", 8),
		# (agent_set_hit_points, ":agent", ":hp", 0),
		# (assign, reg1, ":hp"),
		# (str_store_troop_name, 1, ":troop"),
	# (try_end),

	(try_begin), # player heal when berserker or has torque #MV: berserker only
		(get_player_agent_no, ":player"),
		#(player_has_item|this_or_next, "itm_dunlending_torque"),
		(troop_slot_eq, "trp_traits", slot_trait_berserker, 1),
		(store_agent_hit_points, ":hp", ":player", 0),
		(val_add, ":hp", 20), #MV: gain absolute 20%, instead of relative +25%
		(val_min, ":hp", 100),
		(agent_set_hit_points, ":player", ":hp", 0),
		(str_store_string, s24, "str_trait_title_berserker"),
		(display_message, "@{s24}: Some of your wounds healed!"),
	(try_end),

	(try_begin), # heal classes acc to captainship
		(this_or_next|troop_slot_eq, "trp_traits", slot_trait_archer_captain, 1),
		(this_or_next|troop_slot_eq, "trp_traits", slot_trait_infantry_captain, 1),
					 (troop_slot_eq, "trp_traits", slot_trait_cavalry_captain, 1),
		(get_player_agent_no, ":player"),
		(agent_get_team, ":player_team", ":player"),
		(try_for_agents, ":agent"),
			#(agent_is_ally, ":agent"), #MV: replaced with player team check, makes more sense
			(agent_is_alive, ":agent"),
			(agent_is_human, ":agent"),
			(neq, ":agent", ":player"),
			(agent_get_team, ":agent_team", ":agent"),
			(eq, ":agent_team", ":player_team"),
			(agent_get_class, ":class", ":agent"),
			(assign, ":heal_agent", 0),
			(try_begin),
				(eq, ":class", grc_infantry),
				(troop_slot_eq, "trp_traits", slot_trait_infantry_captain, 1),
				(assign, ":heal_agent", 1),
			 (else_try),
				(eq, ":class", grc_archers),
				(troop_slot_eq, "trp_traits", slot_trait_archer_captain, 1),
				(assign, ":heal_agent", 1),
			 (else_try),
				(eq, ":class", grc_cavalry),
				(troop_slot_eq, "trp_traits", slot_trait_cavalry_captain, 1),
				(assign, ":heal_agent", 1),
			(try_end),
			(eq, ":heal_agent", 1),
			#(agent_slot_eq, ":agent", 6, 0), #MV: hm, what's this slot? marking which agents received healing? unneeded if done once per battle
			(store_agent_hit_points, ":hp", ":agent", 0),
			(val_add, ":hp", 20), #MV: gain absolute 20%, instead of relative +25%
			(val_min, ":hp", 100),
			(agent_set_hit_points, ":agent", ":hp", 0),
			#(agent_set_slot, ":agent", 6, 1),
		(try_end),
		(try_begin),
			(troop_slot_eq, "trp_traits", slot_trait_infantry_captain, 1),
			(str_store_string, s24, "str_trait_title_infantry_captain"),
			(display_message, "@{s24}: Your infantry feels better!"),
		(try_end),
		(try_begin),
			(troop_slot_eq, "trp_traits", slot_trait_archer_captain, 1),
			(str_store_string, s24, "str_trait_title_archer_captain"),
			(display_message, "@{s24}: Your archers feel better!"),
		(try_end),
		(try_begin),
			(troop_slot_eq, "trp_traits", slot_trait_cavalry_captain, 1),
			(str_store_string, s24, "str_trait_title_cavalry_captain"),
			(display_message, "@{s24}: Your cavalry feels better!"),
		(try_end),    
	(try_end),
]),

#script_start_conversation_cutscene (MV)
#Input: conversation number
#Starts a cutscene according to the conversation number
("start_conversation_cutscene",[
    (store_script_param_1, ":convo_code"),
    
    #determine talker
    (try_begin),
      (this_or_next|eq, ":convo_code", tld_cc_gandalf_advice),
      (this_or_next|eq, ":convo_code", tld_cc_gandalf_ally_down),
      (this_or_next|eq, ":convo_code", tld_cc_gandalf_enemy_down),
      (eq, ":convo_code", tld_cc_gandalf_victory),
      (assign, "$g_tld_convo_talker", "trp_gandalf"),
    (else_try),
      (assign, "$g_tld_convo_talker", "trp_nazgul"),
    (try_end),
    
    #fill up dialog lines in strings s50, s51... and set number of lines
    (try_begin),
      (eq, ":convo_code", tld_cc_gandalf_advice),
      
      # find closest good faction
      (faction_get_slot, ":player_capital", "$players_kingdom", slot_faction_capital),
      (assign, ":min_distance", 9999999),
      (assign, ":nearest_faction", -1),
      (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
        (neq, ":faction", "$players_kingdom"),
        (faction_slot_eq, ":faction", slot_faction_side, faction_side_good),
        (faction_get_slot, ":capital", ":faction", slot_faction_capital),
        (call_script, "script_get_tld_distance", ":player_capital", ":capital"),
        (assign, ":party_distance", reg0),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":nearest_faction", ":faction"),
        (assign, "$g_tld_convo_subject", ":capital"), #remember where to send Gandalf next
      (try_end),
      
      (str_store_faction_name, s2, "$players_kingdom"),
      (faction_get_slot, ":player_king", "$players_kingdom", slot_faction_leader),
      (str_store_troop_name, s3, ":player_king"),
      (faction_get_slot, ":nearest_king", ":nearest_faction", slot_faction_leader),
      (str_store_troop_name, s4, ":nearest_king"),
      
      (str_store_string, s50, "@Ah, what a coincidence, running into you {playername}! You might not know me, but are not unknown to me. I am on my way to {s4}, but I have just come from {s3} and your name has come up. {s3} is counting on you in these perilous times and if you had thought to pursue some distracting course of action, you might wish to reconsider it and focus on aiding {s3} to your utmost capabilities."),
      (str_store_string, s51, "@Who are you?"),
      (str_store_string, s52, "@A friend of {s3} and the people of {s2}. Now hurry! Mordor draws all wicked things, and the Dark Power is bending all its will to gather them there. Time is running out for all that is good in this world, lest we make count our every action to oppose it!"),
      (str_store_string, s53, "@What should I do?"),
      (str_store_string, s54, "@Find {s3}'s whereabouts immediately and speak with him. Good luck!"),
      (assign, "$g_tld_convo_lines", 5),
      (val_or, "$g_tld_conversations_done", tld_conv_bit_gandalf_advice),
    (else_try),
      (eq, ":convo_code", tld_cc_gandalf_ally_down),
      
      (assign, ":best_strength", -1),
      (assign, ":best_faction", -1),
      (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction", slot_faction_side, faction_side_good),
        (faction_get_slot, ":strength", ":faction", slot_faction_strength),
        (gt, ":strength", ":best_strength"),
        (assign, ":best_strength", ":strength"),
        (assign, ":best_faction", ":faction"),
      (try_end),
      
      (str_store_faction_name, s2, "$players_kingdom"),
      (str_store_faction_name, s3, "$g_tld_convo_subject"),
      (faction_get_slot, ":dead_king", "$g_tld_convo_subject", slot_faction_leader),
      (str_store_troop_name, s4, ":dead_king"),
      (str_store_faction_name, s5, ":best_faction"),
      
      (str_store_string, s50, "@Good to see the Shadow has not yet managed to defeat you {playername}."),
      (str_store_string, s51, "@You are the one they call Gandalf or Mithrandir."),
      (str_store_string, s52, "@That is what some call me. In my times I have also been called other things, but unless the Darkness is stopped, soon there may not be anyone left to call me anything at all."),
      (str_store_string, s53, "@What do you mean?"),
      (str_store_string, s54, "@In spite of their valiant resistance, {s3} has been overwhelmed by the forces of evil. {s3}'s people are scattered and the good {s4} is no more."),
      (str_store_string, s55, "@You bring dismal news, wizard."),
      (str_store_string, s56, "@But I also bring a message of hope. The people of {s5} are still holding firm. Their warriors are fearless and their leaders resolute."),
      (str_store_string, s57, "@What should I do?"),
      (str_store_string, s58, "@Help them fight the enemy as best as you can. Never relent! But be on your guard! There are older and fouler things than Orcs in the world."),
      (assign, "$g_tld_convo_lines", 9),
      (val_or, "$g_tld_conversations_done", tld_conv_bit_gandalf_ally_down),
    (else_try),
      (eq, ":convo_code", tld_cc_gandalf_enemy_down),
      
      (str_store_faction_name, s3, "$g_tld_convo_subject"),
      (faction_get_slot, ":dead_king", "$g_tld_convo_subject", slot_faction_leader),
      (str_store_troop_name, s4, ":dead_king"),
      
      (str_store_string, s50, "@Beware {playername}, the might of Darkness crumbles. {s3} has fallen, as has its leader {s4}."),
      (str_store_string, s51, "@What do you want of me, old man?"),
      (str_store_string, s52, "@Just know that a Dawn is coming. It is inevitable. And should you still be alive to see it, consider what you shall have to say for yourself then."),
      (assign, "$g_tld_convo_lines", 3),
      (val_or, "$g_tld_conversations_done", tld_conv_bit_gandalf_enemy_down),
    (else_try),
      (eq, ":convo_code", tld_cc_gandalf_victory),
      
      (call_script, "script_get_faction_rank", "$g_talk_troop_faction"),
      (call_script, "script_get_own_rank_title_to_s24", "$players_kingdom", reg0),
      
      (str_store_string, s50, "@Well met {playername}, {s24}. My trust in you has not been misplaced. The might of the forces of the Shadow has been broken and your efforts played no small part in it!"),
      (str_store_string, s51, "@Thank you, Mithrandir!"),
      (str_store_string, s52, "@The wizard Saruman is gone and Barad Dur has been shattered to dust along with its Dark Lord! All the peoples of Middle Earth are relieved of the threat that nearly consumed all that was good and pure in this world. The Enemy is vanquished and The King has returned!"),
      (str_store_string, s53, "@It was a long and bloody war and many of our close friends are also no longer with us."),
      (str_store_string, s54, "@There is much to regret and mourn, and even more to rebuild and mend in the coming days. But for now, let us be jubilant with those of our friends that are with us still and celebrate all we have achieved in The Last Days Of The Third Age."),
      (assign, "$g_tld_convo_lines", 5),
      (val_or, "$g_tld_conversations_done", tld_conv_bit_gandalf_victory),
    (else_try),
      (eq, ":convo_code", tld_cc_nazgul_baggins),
      
      (str_store_string, s50, "@Bagginsssss... Sssshhhire..."),
      (str_store_string, s51, "@I... don't know!"),
      (str_store_string, s52, "@It... beckonsssssss..."),
      (assign, "$g_tld_convo_lines", 3),      
      (val_or, "$g_tld_conversations_done", tld_conv_bit_nazgul_baggins),
    (else_try),
      (eq, ":convo_code", tld_cc_nazgul_evil_war),
      
      (str_store_string, s50, "@Treachery... Unforgiven..."),
      (str_store_string, s51, "@But I..."),
      (str_store_string, s52, "@Noone... oppossssses... Barad Dur... and livessss!"),
      (assign, "$g_tld_convo_lines", 3),      
      (val_or, "$g_tld_conversations_done", tld_conv_bit_nazgul_evil_war),
    (else_try),
      (eq, ":convo_code", tld_cc_nazgul_victory),
      
      (str_store_string, s50, "@All... must... submit... and... serve..."),
      (try_begin),
        (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_eye),
        (str_store_string, s51, "@I serve the Eye!"),
      (else_try),
        (str_store_string, s51, "@I shall serve the Eye!"),
      (try_end),
      (assign, "$g_tld_convo_lines", 2),      
      (val_or, "$g_tld_conversations_done", tld_conv_bit_nazgul_victory),
    (try_end),

    #start the cutscene
    (jump_to_menu, "mnu_auto_conversation_cutscene"),
    
    #send the conversation party back immediately
    (call_script, "script_send_from_conversation_mission", "$g_tld_convo_talker"),
]),

#script_send_on_conversation_mission (MV)
#Input: mission/conversation code
#Reroutes or spawns Gandalf/Nazgul party and sends it to meet the player for a specific conversation
("send_on_conversation_mission",[
    (store_script_param_1, ":mission_code"),
    
    #determine mission troop and its data
    (try_begin),
      (this_or_next|eq, ":mission_code", tld_cc_gandalf_advice),
      (this_or_next|eq, ":mission_code", tld_cc_gandalf_ally_down),
      (this_or_next|eq, ":mission_code", tld_cc_gandalf_enemy_down),
      (eq, ":mission_code", tld_cc_gandalf_victory),
      (assign, ":mission_troop", "trp_gandalf"),
      (assign, ":party_template", "pt_gandalf"),
      (assign, ":mission_troop_side", faction_side_good),
      (assign, ":state", "$g_tld_gandalf_state"),
    (else_try),
      (assign, ":mission_troop", "trp_nazgul"),
      (assign, ":party_template", "pt_nazgul"),
      (assign, ":mission_troop_side", faction_side_eye),
      (assign, ":state", "$g_tld_nazgul_state"),
    (try_end),
    
    # check if party is missing when it shouldn't be; recover by creating it (this should never happen, but we handle it anyway)
    (troop_get_slot, ":party", ":mission_troop", slot_troop_leaded_party),
    (assign, ":party_missing_bug", 0),
    (try_begin),
      (gt, ":party", 0),
      (neg|party_is_active, ":party"),
      (assign, ":party_missing_bug", 1),
    (try_end),
    
    #if it's not spawned, spawn it
    (try_begin),
      (this_or_next|eq, ":state", -1), #mission troop inactive
      (eq, ":party_missing_bug", 1), #...or a missing party
      
      #find nearest mission troop-friendly town
      (assign, ":min_distance", 9999999),
      (assign, ":nearest_town", -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":center_faction", ":center_no"),
        (faction_slot_eq, ":center_faction", slot_faction_side, ":mission_troop_side"), #e.g. Nazgul spawns in the nearest Eye town
        (call_script, "script_get_tld_distance", "p_main_party", ":center_no"),
        (assign, ":party_distance", reg0),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":nearest_town", ":center_no"),
      (try_end),
      #this should never happen, but it's handled
      (try_begin),
        (eq, ":nearest_town", -1),
        (assign, ":nearest_town", "p_main_party"),
      (try_end),
      
      #spawn the party
      (set_spawn_radius, 0),
      (spawn_around_party, ":nearest_town", ":party_template"),
      (assign, ":party", reg0),
      (troop_set_slot, ":mission_troop", slot_troop_leaded_party, ":party"), #this is how we know it has a party
    (try_end),
    
    #find the party and send it to meet the player
    (troop_get_slot, ":party", ":mission_troop", slot_troop_leaded_party),
    (try_begin),
      #(party_is_active, ":party"), #no need, we guarantee this
      (party_set_ai_behavior, ":party", ai_bhvr_attack_party),
      (party_set_ai_object, ":party", "p_main_party"),
      (party_set_flags, ":party", pf_default_behavior, 0),
    (try_end),
    
    (assign, ":state", ":mission_code"), #this overwrites any previous mission, even if it was a conversation - more recent news are more important
    
    (try_begin),
      (eq, ":mission_troop", "trp_gandalf"),
      (assign, "$g_tld_gandalf_state", ":state"),
    (else_try),
      (assign, "$g_tld_nazgul_state", ":state"),
    (try_end),
]),

#script_send_from_conversation_mission (MV)
#Input: mission troop
#Send a Gandalf/Nazgul party after the conversation to some town
("send_from_conversation_mission",[
    (store_script_param_1, ":mission_troop"),
    
    #determine mission troop data
    (try_begin),
      (eq, ":mission_troop", "trp_gandalf"),
      (assign, ":mission_troop_side", faction_side_good),
    (else_try),
      (assign, ":mission_troop_side", faction_side_eye),
    (try_end),
    
      #find nearest mission troop-friendly town
      (assign, ":min_distance", 9999999),
      (assign, ":nearest_town", -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
        (store_faction_of_party, ":center_faction", ":center_no"),
        (faction_slot_eq, ":center_faction", slot_faction_side, ":mission_troop_side"), #e.g. Nazgul spawns in the nearest Eye town
        (call_script, "script_get_tld_distance", "p_main_party", ":center_no"),
        (assign, ":party_distance", reg0),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":nearest_town", ":center_no"),
      (try_end),
      #this should never happen, but it's handled
      (try_begin),
        (eq, ":nearest_town", -1),
        (assign, ":nearest_town", "p_town_minas_tirith"),
      (try_end),
      (try_begin),
        (eq, ":mission_troop", "trp_gandalf"),
        (eq, "$g_tld_gandalf_state", tld_cc_gandalf_advice),
        (assign, ":nearest_town", "$g_tld_convo_subject"), #special case
      (try_end),
          
    #find the party and send it to the town
    (troop_get_slot, ":party", ":mission_troop", slot_troop_leaded_party),
    (try_begin),
      #(party_is_active, ":party"), #no need, we guarantee this
      (party_set_ai_behavior, ":party", ai_bhvr_travel_to_party),
      (party_set_ai_object, ":party", ":nearest_town"),
      (party_set_flags, ":party", pf_default_behavior, 0),
    (try_end),
    
    (assign, ":state", 0), # we are done, but the party still exists
    
    (try_begin),
      (eq, ":mission_troop", "trp_gandalf"),
      (assign, "$g_tld_gandalf_state", ":state"),
    (else_try),
      (assign, "$g_tld_nazgul_state", ":state"),
    (try_end),
]),

# script_party_eject_nonfaction (GA)
# troops nonfaction for ":source" & given from ":recipient_initial" to ":source" - are returned back to ":recipient"
# Input: arg1 = party_A, source, retains target faction and heroes
# Input: arg2 = party_B, gets non-faction troops it had initially according to arg4 (usually p_main_party)
# Input: arg3 = initial composition of party_B
#Output: arg3 stores troops returned back to recipient
("party_eject_nonfaction",[
	(store_script_param_1, ":source"),
	(store_script_param_2, ":recipient"),
	(store_script_param, ":recipient_initial", 3),

	#subtract recipient from recipient_initial, relies on recipient being subset of recipient_initial!
	(party_get_num_companion_stacks, ":num_stacks", ":recipient"),
	(try_for_range, ":i_stack", 0, ":num_stacks"),
		(party_stack_get_troop_id, ":st", ":recipient", ":i_stack"),
		(party_stack_get_size, ":ss",":recipient",":i_stack"),
		(party_remove_members, ":recipient_initial", ":st", ":ss"),
	(try_end),	
	
	#clear recipient_initial from any hero troops and prisoners
	(try_for_range, ":hero", heroes_begin, heroes_end),
		(remove_troops_from_prisoners, ":hero",":recipient_initial"),
		(remove_member_from_party, ":hero",":recipient_initial"),
	(try_end),
	(remove_member_from_party, "trp_player",":recipient_initial"),
	
	#remove faction from recipient_initial and nonfaction from source, add nonfaction to recipient
	(store_faction_of_party, ":fac", ":source"),
	(call_script, "script_party_copy", "p_temp_party", ":recipient_initial"), #needs a copy to iterate through, since member removing fucks up stacks order
	(party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
	(try_for_range, ":i_stack", 0, ":num_stacks"),
		(party_stack_get_size    , ":ss", "p_temp_party", ":i_stack"),
		(party_stack_get_troop_id, ":st", "p_temp_party", ":i_stack"),
		(store_troop_faction, ":ft", ":st"),
		(try_begin),
			(eq, ":ft", ":fac"),	(party_remove_members, ":recipient_initial", ":st", ":ss"),# factions outta recipient_initial, stay in source
		# CC: Mordor and Guldur share troops
		#(else_try),(eq, ":ft", "fac_guldur"),(eq,":fac","fac_mordor"),	(party_remove_members, ":recipient_initial", ":st", ":ss"),# factions outta recipient_initial, stay in source
		#(else_try),(eq, ":ft", "fac_mordor"),(eq,":fac","fac_guldur"), (party_remove_members, ":recipient_initial", ":st", ":ss"),# factions outta recipient_initial, stay in source
		 (else_try),			(party_remove_members, ":source"           , ":st", ":ss"),# nonfactions outta source, stay in recipient_initial
		(try_end),
	(try_end),
	(call_script, "script_party_add_party_companions", ":recipient", ":recipient_initial"), #transfer nonfactions to recipient
]),

# script_stand_back (GA)
# returns orcs and uruks to default body position at the end of conversation
("stand_back",[ # reset leaning animaton after dialog ends
	(get_player_agent_no, "$current_player_agent"),
	(agent_get_horse,reg1,"$current_player_agent"),
	(troop_get_type, ":race", "$player_current_troop_type"),
	(try_begin),
		(is_between, ":race", tf_orc_begin, tf_orc_end),
		(try_begin),(eq, reg1, -1),(agent_set_animation, "$current_player_agent", "anim_cancel_ani_stand"),
		 (else_try),               (agent_set_animation, "$current_player_agent", "anim_cancel_ani_ride"),
		(try_end),
	(try_end),
]),
# script_remove_empty_parties_in_group (GA)
# stashes prisoners into p_temp_party
("remove_empty_parties_in_group",[
	(store_script_param_1, ":root_party"),
    (try_begin),
        (gt, ":root_party", 0),
        (party_get_num_attached_parties, ":num_attached_parties",  ":root_party"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
            (party_get_attached_party_with_rank, ":attached_party", ":root_party", ":attached_party_rank"),
            (gt, ":attached_party", 0),
            (party_get_num_companions, ":troops", ":attached_party"),
            (try_begin),
                (eq, ":troops",0), # no more soldiers here?
                (party_get_num_prisoners,reg1, ":attached_party"),
                (try_begin), # transfer prisoners
                    (gt, reg1, 0),
                    (call_script, "script_party_add_party_prisoners", "p_temp_party", ":attached_party"),
                (try_end),
            (try_end),
            (call_script, "script_remove_empty_parties_in_group", ":attached_party"),
            (try_begin),
                (eq, ":troops", 0),
                (remove_party,":attached_party"),# remove empty party after subtree iterations and prisoner stashing are done 
            (try_end),
        (try_end),
	(try_end),
 ]),

	
#  script_get_food_of_race_and_faction (mtarini)
# puts resulting item in reg0
("get_food_of_race_and_faction",[
	(store_script_param_1, ":race"),
	(store_script_param_2, ":fac"),
	(try_begin),(is_between, ":race", tf_orc_begin, tf_orc_end),
		(assign, reg0, "itm_maggoty_bread"),
	(else_try),(is_between,  ":race", tf_elf_begin, tf_elf_end), 
		(assign, reg0, "itm_lembas"),
	(else_try),(this_or_next|eq,":fac", "fac_dale"),(this_or_next|eq,":fac","fac_umbar"),(eq,":fac","fac_beorn"), 
		(assign, reg0, "itm_smoked_fish"),
	(else_try),(faction_slot_eq,":fac", slot_faction_side, faction_side_good),
		(assign, reg0, "itm_cram"),
	(else_try),
		(assign, reg0, "itm_dried_meat"),
	(try_end),
]),
 
 # another useful self explainatory script... (mtarini)
("troop_copy_all_items_from_troop",[
	(store_script_param_1, ":dest"),
	(store_script_param_2, ":source"),
	(troop_get_inventory_capacity, ":n", ":source"),
	(troop_ensure_inventory_space,":dest",":n"),
	
	#(assign, ":debug_count", 0), # for debug
	(troop_clear_inventory,":dest"),
	(try_for_range, ":i", 0, ":n"),
		(troop_get_inventory_slot, ":item_id", ":source", ":i"),
		(ge, ":item_id", 0),
		(troop_get_inventory_slot_modifier, ":item_mod", ":source", ":i"),
		(troop_add_item, ":dest", ":item_id",":item_mod",),
		#(val_add, ":debug_count", 1), # for debug
	(try_end),

	#(assign, reg51, ":debug_count"), (display_message, "@debug: copyed {reg51} items"),
]),

 # another useful self explainatory script... (mtarini)
("store_random_scene_position_in_pos10",[
	(get_scene_boundaries,pos1,pos2),
	(position_get_x,":min_x",pos1),(position_get_y,":min_y",pos1),
	(position_get_x,":max_x",pos2),(position_get_y,":max_y",pos2),
	(val_add, ":min_x", 100),(val_sub, ":max_x", 100),
	(val_add, ":min_y", 100),(val_sub, ":min_y", 100),
	(store_random_in_range, ":x", ":min_x", ":max_x"),
	(store_random_in_range, ":y", ":min_y", ":max_y"),
	(init_position, pos10),
	(position_set_x, pos10, ":x"),
	(position_set_y, pos10, ":y"),
	(position_set_z_to_ground_level, pos10),
]),

# utility scropt (mtarini)
# removes from party A the prisoners, as dictated from party B (except wonded)
# returns removed number in reg0
("party_remove_party_from_prisoners",[

	(store_script_param_1, ":dest"),
	(store_script_param_2, ":remove_list"),

	(assign, ":removed", 0),
	
    (party_get_num_companion_stacks, ":num_stacks", ":remove_list"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":trp", ":remove_list", ":i_stack"),
	  (party_stack_get_size, ":n", ":remove_list", ":i_stack"),
	  (party_stack_get_num_wounded, ":w", ":remove_list", ":i_stack"),
	  (val_sub, ":n", ":w"),
	  (party_remove_prisoners, ":dest",  ":trp",  ":n"),
	  (val_add, ":removed", reg0),
    (try_end),
	(assign, reg0, ":removed"),
]),

	 
("save_compartibility_script7",[]),
("save_compartibility_script8",[]),
("save_compartibility_script9",[]),
("save_compartibility_script10",[]),

### WARBAND HARDCODED SCRIPTS
# ("game_quick_start",[]),
# ("game_set_multiplayer_mission_end",[]),
# ("game_enable_cheat_menu",[]),
# ("game_get_console_command",[]),
# ("game_get_scene_name",[]),
# ("game_get_mission_template_name",[]),
# ("game_receive_url_response",[]),
# ("game_get_cheat_mode",[]),
# ("game_receive_network_message",[]),
# ("game_get_multiplayer_server_option_for_mission_template",[]),
# ("game_multiplayer_server_option_for_mission_template_to_string",[]),
# ("game_multiplayer_event_duel_offered",[]),
# ("game_get_multiplayer_game_type_enum",[]),
# ("game_multiplayer_get_game_type_mission_template",[]),

# #script_add_troop_to_cur_tableau_for_profile
# # INPUT: troop_no
# # OUTPUT: none
# ("add_troop_to_cur_tableau_for_profile",
	# [(store_script_param, ":troop_no",1),

	# (set_fixed_point_multiplier, 100),
	# (cur_tableau_clear_override_items),
	# (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),
	# (init_position, pos5),
	# (assign, ":cam_height", 105),
	# #       (val_mod, ":camera_distance", 5),
	# (assign, ":camera_distance", 380),
	# (assign, ":camera_yaw", -15),
	# (assign, ":camera_pitch", -18),
	# (assign, ":animation", anim_stand_man),
	# (position_set_z, pos5, ":cam_height"),
	# # camera looks towards -z axis
	# (position_rotate_x, pos5, -90),
	# (position_rotate_z, pos5, 180),
	# # now apply yaw and pitch
	# (position_rotate_y, pos5, ":camera_yaw"),
	# (position_rotate_x, pos5, ":camera_pitch"),
	# (position_move_z, pos5, ":camera_distance", 0),
	# (position_move_x, pos5, 5, 0),

	# (profile_get_banner_id, ":profile_banner"),
	# (try_begin),
		# (ge, ":profile_banner", 0),
		# (init_position, pos2),
		# (val_add, ":profile_banner", banner_meshes_begin),
		# (position_set_x, pos2, -175),
		# (position_set_y, pos2, -300),
		# (position_set_z, pos2, 180),
		# (position_rotate_x, pos2, 90),
		# (position_rotate_y, pos2, -15),
		# (cur_tableau_add_mesh, ":profile_banner", pos2, 0, 0),
	# (try_end),
	# (init_position, pos2),
	# (try_begin),
		# (troop_is_hero, ":troop_no"),
		# (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
	# (else_try),
		# (store_mul, ":random_seed", ":troop_no", 126233),
		# (val_mod, ":random_seed", 1000),
		# (val_add, ":random_seed", 1),
		# (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
	# (try_end),
	# (cur_tableau_set_camera_position, pos5),

	# (copy_position, pos8, pos5),
	# (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
	# (position_rotate_z, pos8, 30), 
	# (position_rotate_x, pos8, -60), 
	# (cur_tableau_add_sun_light, pos8, 175,150,125),
# ]),

]

command_cursor_scripts = [

###command_cursor_minimod_begin###
  # script_cf_shirt_pos1_along_y_axis_to_ground
  # Input: max distance to shift before failing
  # Output: pos1 shifted to ground level along forward y-axis
  ("cf_shift_pos1_along_y_axis_to_ground",
    [
      (store_script_param, ":max_distance", 1),
      (assign, reg0, 1), #output value
      (assign, reg10, ":max_distance"),
      (assign, reg11, 0), #distance so far
      (get_scene_boundaries, pos10, pos11),
      (position_get_x, reg12, pos10),
      (position_get_y, reg13, pos10),
      (position_get_x, reg14, pos11),
      (position_get_y, reg15, pos11),
      (call_script, "script_shift_pos1_along_y_axis_to_ground_aux"),
      (eq, reg0, 1), #if max distance or scene boundaries were reached, fail
      (position_set_z_to_ground_level, pos1),
    ]),
    
  ("shift_pos1_along_y_axis_to_ground_aux", 
    [
      (val_add, reg2, 100),
      (copy_position, pos2, pos1),
      (position_set_z_to_ground_level, pos2),
      (position_get_x, ":pos1_x", pos1),
      (position_get_y, ":pos1_y", pos1),
      (position_get_z, ":pos1_z", pos1),
      (position_get_z, ":ground_z", pos2),
      (try_begin),                           #IF:
        (this_or_next|ge, reg11, reg10),     #distance so far > max_distance OR
        (this_or_next|le, ":pos1_x", reg12), #pos1 x <= scene min x OR
        (this_or_next|le, ":pos1_y", reg13), #pos1 y <= scene min y OR
        (this_or_next|ge, ":pos1_x", reg14), #pos1 x >= scene max x OR
        (ge, ":pos1_y", reg15),              #pos1 y >= scene max y THEN
        (assign, reg0, -1),                  #the outer function fails
      (else_try),
        (lt, ":ground_z", ":pos1_z"),
        (position_move_y, pos1, 100),
        (call_script, "script_shift_pos1_along_y_axis_to_ground_aux"),
      (try_end),
    ]),
###command_cursor_minimod_end###

]

scripts = scripts + ai_scripts + formAI_scripts + morale_scripts + command_cursor_scripts



