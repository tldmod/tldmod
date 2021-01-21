# -*- coding: utf-8 -*-
from header_common import *
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *

from module_constants import *

from module_info import wb_compile_switch as is_a_wb_cutscene
from module_info import wb_compile_switch as is_a_wb_menu

####################################################################################################################
#  (menu-id, menu-flags, menu_text, mesh-name, [<operations>], [<options>]),
#
#   Each game menu is a tuple that contains the following fields:
#  
#  1) Game-menu id (string): used for referencing game-menus in other files.
#     The prefix menu_ is automatically added before each game-menu-id
#
#  2) Game-menu flags (int). See header_game_menus.py for a list of available flags.
#     You can also specify menu text color here, with the menu_text_color macro
#  3) Game-menu text (string).
#  4) mesh-name (string). Not currently used. Must be the string "none"
#  5) Operations block (list). A list of operations. See header_operations.py for reference.
#     The operations block is executed when the game menu is activated.
#  6) List of Menu options (List).
#     Each menu-option record is a tuple containing the following fields:
#   6.1) Menu-option-id (string) used for referencing game-menus in other files.
#        The prefix mno_ is automatically added before each menu-option.
#   6.2) Conditions block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The conditions are executed for each menu option to decide whether the option will be shown to the player or not.
#   6.3) Menu-option text (string).
#   6.4) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The consequences are executed for the menu option that has been selected by the player.
#
# Note: The first Menu is the initial character creation menu.
####################################################################################################################


# just stuff to make search for troop cheat (mtarini)
tmp_menu_steps = 5 # how many entries per meny page
tmp_menu_max_fac = 21
tmp_menu_max_tier = 4
tmp_max_troop = 858 # troop_end

magic_items = [itm_lembas] + [itm_pony] +  [itm_warg_reward] + range(itm_ent_water, itm_witchking_helmet)  # first non magic item

city_menu_color = menu_text_color(0xFF010101)  # city menu text color: black

# code snipped to set city meny background
code_to_set_city_background = [
  (party_get_slot,":mesh","$g_encountered_party",slot_town_menu_background),
  (set_background_mesh, ":mesh"),
 ]

# (a common code snippet that is used twice in the add troop cheat menu... ) -- mtarini
code_to_set_search_string = [
  (set_background_mesh, "mesh_ui_default_menu_window"),
  (try_begin), (ge,"$menu_select_any_troop_search_fac", tmp_menu_max_fac+1), 
	(str_store_string, s10, "@any"), 
  (else_try),
	(str_store_faction_name, s10, "$menu_select_any_troop_search_fac"), 
  (try_end),
  (try_begin)
  ]+concatenate_scripts([[
	(eq,"$menu_select_any_troop_search_race",x),
	(str_store_string, s13, race_names[x]),
  (else_try),
  ]for x in range(len(race_names)) ])+[ 
	(str_store_string, s13, "@any"), 
  (try_end),
  (try_begin), (eq,"$menu_select_any_troop_search_tier", tmp_menu_max_tier+1), 
	(str_store_string, s11, "@any"), 
  (else_try),
	(assign, reg11, "$menu_select_any_troop_search_tier"),
	(str_store_string, s11, "@{reg11}0 - {reg11}9"), 
  (try_end),
  
  (try_begin), (eq,"$menu_select_any_troop_search_hero", 0), 
	(str_store_string, s12, "@Regular troops only"), 
  (else_try),  (eq,"$menu_select_any_troop_search_hero", 1), 
	(str_store_string, s12, "@Heroes only"), 
  (else_try),  
	(str_store_string, s12, "@Regulars and Heroes"), 
  (try_end),
  ]
# just stuff to make search for troop cheat (mtarini)
  
game_menus = [
#This needs to be the first window!!!
( "start_game_1",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "^^^^^^^^^^What do you fight for?", "none", [
	(set_background_mesh, "mesh_relief01"),
	(set_show_messages,0),

	#swy-- SWC trick: enable developer mode when the cursor is in the lower edge of the screen
	#   -- during loading... (or even lower, if the game is in windowed mode), sneaky!
	(try_begin),
	  (mouse_get_position,                  pos42),
	  (    position_get_y, ":cursor_y_pos", pos42),
	  (                le, ":cursor_y_pos",     0),
	  # --
#	  (assign,             "$cheat_switch",     1),
	  (assign,               "$cheat_mode",     1),
	(try_end),

	# item faction slots
	(call_script,"script_set_item_faction"),
	(assign, "$disable_skill_modifiers", 0),
	(assign, "$intro_presentation_stage", 1),
	(start_presentation, "prsnt_faction_selection"),
    ],
    [("start_good",[],"the DAWN of a new Era"    ,[(jump_to_menu,"mnu_start_good" ),]),
     ("start_evil",[],"the TWILIGHT of Man"      ,[(jump_to_menu,"mnu_start_evil" ),]),
	 ("spacer"    ,[],"_"  ,[]),
	 ("faction_intros", [], "Learn about the different factions of Middle-Earth", [(start_presentation, "prsnt_faction_intro_text")]),
	 ("spacer"    ,[],"_"  ,[]),
	 ("go_bback"  ,[],"Go Back",[(change_screen_quit              ),]), 
	]+concatenate_scripts([[
	 ("quick"     ,[(eq, cheat_switch, 1),],"[dev: quick start Gondor]",[(call_script,"script_start_as_one","trp_i1_gon_levy"),(jump_to_menu,"mnu_start_phase_2" ),]), 
	 ("quick2"    ,[(eq, cheat_switch, 1),],"[dev: quick start Mordor]",[(call_script,"script_start_as_one","trp_i1_mordor_uruk_snaga"),(jump_to_menu,"mnu_start_phase_2" ),]), 
	] for ct in range(cheat_switch)])+[	
	]
 ),
#This needs to be the second window!!!
( "start_phase_2",mnf_disable_all_keys,
    "^^^^^______________Middle Earth. A shadow is growing in the East, ^______________and dark things come forth that have long been hidden. ^______________The free peoples prepare for war, the like of which has not been seen for an age. ^______________Men, Elves, Dwarves and Orcs; all will play their part. ^^______________What part, however, remains to be seen... ",
    "none",
   [(set_background_mesh, "mesh_ui_default_menu_window"),
	(assign, "$tld_game_options",0),
	(try_begin), (eq,"$start_phase_initialized",0),(assign,"$start_phase_initialized",1), # do this only once
		(set_show_messages,0),
		#(call_script,"script_TLD_troop_banner_slot_init"),
		(call_script,"script_reward_system_init"),
		(call_script,"script_init_player_map_icons"),
		#(call_script,"script_get_player_party_morale_values"), (party_set_morale, "p_main_party", reg0),
		(troop_add_gold, "trp_player", 50),#  add a little money
	# relocate party next to own capital
		(faction_get_slot, reg20, "$players_kingdom", slot_faction_capital),
		(try_for_range, ":i", centers_begin, centers_end),
			(party_is_active, ":i"), 
		    (party_slot_eq, ":i", slot_center_destroyed, 0),
			(gt, "$players_subkingdom", 0), # player has a subfaction
			(store_faction_of_party, reg15, ":i"), (eq, reg15, "$players_kingdom"),
			(party_slot_eq, ":i", slot_party_subfaction, "$players_subkingdom"), # i this is the  capital of the subfaction
			(assign, reg20, ":i"), 
			(assign, ":i", centers_end),  # break
		(try_end),
		(call_script, "script_tld_party_relocate_near_party", "p_main_party", reg20, 5), # MV: was 16km - too far
	
		# initialization of "search troop" menu (only once)  mtarini
		(assign, "$menu_select_any_troop_search_race", len(race_names)),  # any race
		(assign, "$menu_select_any_troop_search_tier", tmp_menu_max_tier+1), # any tier
		(assign, "$menu_select_any_troop_search_fac", "$players_kingdom"), # player's kingdom
		(assign, "$menu_select_any_troop_search_hero", 0),	

		(assign, "$cheat_imposed_quest", -1),	

		(call_script, "script_determine_what_player_looks_like"), # for drawings meshes
		#(set_show_messages,1),
	(try_end),
    (call_script, "script_update_troop_notes", "trp_player"), #MV fixes
    (call_script, "script_update_faction_notes", "$players_kingdom"),
	],
    [ ("go_forth",[],"__________Go forth upon your chosen path...",
       [#(troop_add_item, "trp_player","itm_dried_meat",0),#  free food for everyone
        (call_script, "script_get_player_party_morale_values"),
        (party_set_morale, "p_main_party", reg0),
		(assign, "$recover_after_death_menu", "mnu_recover_after_death_default"),
		(assign, "$tld_game_options",1),
		# TEMP: a spear for everyone
		#(troop_add_item, "trp_player","itm_rohan_lance_standard",0),
		##   (troop_add_item, "trp_player","itm_horn",0),
		(troop_equip_items, "trp_player"),
        (troop_sort_inventory, "trp_player"),
		#(set_show_messages, 1),
        #(change_screen_map), #(change_screen_return),
         (jump_to_menu,"mnu_faction_intro_menu"), # Start Quest - Kham
       ]),
	  ("spacer",[],"_",[]),
	  
	   ] + (is_a_wb_menu==1 and [
	  ("change_tld_options",[],"Change TLD options.",[(start_presentation, "prsnt_tld_mod_options")]),
	  ] or [
	  ("change_tld_options",[],"Change TLD options.",[(jump_to_menu, "mnu_game_options")]),
	  ]) + [

	  ("spacer",[],"_",[]),
	]+concatenate_scripts([[
      ("cheat00",[(eq, cheat_switch, 1),(troop_get_upgrade_troop,":t","$player_current_troop_type",0),(gt,":t",0),(str_store_troop_name,s21,":t"),
	    ],"CHEAT: become a {s21}",[
		(troop_get_upgrade_troop,":t","$player_current_troop_type",0),
	    (call_script,"script_start_as_one",":t"),
		(jump_to_menu,"mnu_start_phase_2" ),
	  ]),
      ("cheat01",[(eq, cheat_switch, 1),(troop_get_upgrade_troop,":t","$player_current_troop_type",1),(gt,":t",0),(str_store_troop_name,s21,":t"),
	    ],"CHEAT: become a  {s21}",[
		(troop_get_upgrade_troop,":t","$player_current_troop_type",1),
	    (call_script,"script_start_as_one",":t"),
		(jump_to_menu,"mnu_start_phase_2" ),
	  ]),
      ("cheat03",[(eq, cheat_switch, 1),(str_store_troop_name_plural,s21,"$player_current_troop_type")],"CHEAT: add 10 {s21} to party",
	  [(party_add_members, "p_main_party", "$player_current_troop_type", 10),	  
	  ]),
	] for ct in range(cheat_switch)])+[	 
    ]
 ),

# This needs to be the third window!!!  
( "start_game_3",mnf_disable_all_keys,
    "^^^^^^^^Choose your scenario:",
    "none",
    [ #Default banners
      (troop_set_slot, "trp_banner_background_color_array", 126, 0xFF212221),
      (troop_set_slot, "trp_banner_background_color_array", 127, 0xFF212221),
      (troop_set_slot, "trp_banner_background_color_array", 128, 0xFF2E3B10),
      (troop_set_slot, "trp_banner_background_color_array", 129, 0xFF425D7B),
      (troop_set_slot, "trp_banner_background_color_array", 130, 0xFF394608),
	  
	  # initialization (mtarini)
      (assign, "$testbattle_team_a_num", 40),(assign, "$testbattle_team_a_troop", "trp_i2_isen_orc"),
      (assign, "$testbattle_team_b_num", 10),(assign, "$testbattle_team_b_troop", "trp_i4_gon_swordsman"),
      (assign, "$menu_select_any_troop_search_race", len(race_names)),  # any race
      (assign, "$menu_select_any_troop_search_tier", tmp_menu_max_tier+1), # any tier
      (assign, "$menu_select_any_troop_search_fac", "fac_gondor"), # player's kingdom
      (assign, "$menu_select_any_troop_search_hero", 0),
      
    # (call_script,"script_TLD_troop_banner_slot_init"), 	  #TLD troops banners
      
    #swy-- added unused merlkir illustration here... it looks cool!
      (set_background_mesh, "mesh_draw_war_starts"),
      
      ],
   [("custom_battle_scenario_1" ,[], "Skirmish, Gondor factions vs Harad",
		[(assign, "$g_custom_battle_scenario", 1),(jump_to_menu, "mnu_custom_battle_2"),]),
	]+concatenate_scripts([[
	("custom_battle_scenario_12",[],"Choose factions for battle",
		[(assign, "$g_custom_battle_scenario",16),(jump_to_menu, "mnu_custom_battle_choose_faction1"),]),
	] for ct in range(cheat_switch)])+[	
	("custom_battle_scenario_3" ,[],"Skirmish, Elves vs Black_Numenoreans",
		[(assign, "$g_custom_battle_scenario", 2),(jump_to_menu, "mnu_custom_battle_2"),]),
	("custom_battle_scenario_4" ,[],"Helms Deep Defense, Rohan vs Isengard",
		[(assign, "$g_custom_battle_scenario", 3),(jump_to_menu, "mnu_custom_battle_2"),]),
	("custom_battle_scenario_5" ,[],"Skirmish, North factions vs Rhun",
		[(assign, "$g_custom_battle_scenario", 4),(jump_to_menu, "mnu_custom_battle_2"),]),
	("custom_battle_scenario_6" ,[(eq, cheat_switch, 1),],"Siege Attack, Orcs vs Dwarves",
		[(assign, "$g_custom_battle_scenario", 5),(jump_to_menu, "mnu_custom_battle_2"),]),
	("custom_battle_scenario_7" ,[],"Ambush, Orcs vs Mirkwood",
		[(assign, "$g_custom_battle_scenario", 6),(jump_to_menu, "mnu_custom_battle_2"),]),
	] + (is_a_wb_menu==1 and [
	("custom_battle_scenario_8",[],"The Last Stand of Durin's Folk",
		[(assign, "$g_custom_battle_scenario", 8),(jump_to_menu, "mnu_custom_battle_2"),]),
	] or []) + [
#	("custom_battle_scenario_9",[],"Football fun        ",
#		[(assign, "$g_custom_battle_scenario", 8),(jump_to_menu, "mnu_custom_battle_2"),]),

# 	(CppCoder) placeholder, should we want to implement this.
#	("custom_battle_choose" ,[],"____________Build your own battle____________.",
#		[(assign, "$g_custom_battle_scenario", 1),(jump_to_menu, "mnu_custom_battle_2"),]),

	]+concatenate_scripts([[
	("custom_battle_scenario_88",[],"Chasing an Orc Scout Party",
		[(assign, "$g_custom_battle_scenario", 88),(jump_to_menu, "mnu_custom_battle_2"),]),
	("custom_battle_scenario_11",[],"Test Battles (Tune Balancing!)",
		[(jump_to_menu, "mnu_quick_battle_general_test"),]),
	("custom_battle_scenario_10",[],"Scenery test battle",
		[(assign, "$g_custom_battle_scenario", 9),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario",[],"Test Troll Battles",
		[(jump_to_menu, "mnu_quick_battle_troll"),]),
	("warg_battle_scenario",[],"Test Warg Battles",
		[(jump_to_menu, "mnu_quick_battle_wargs"),]),
	("choose_scene"             ,[],"** Scene Chooser **",
		[                                         (jump_to_menu, "mnu_choose_scenes_0"),]),
	] for ct in range(cheat_switch)])+[
    ("build_your_own_scene"     ,[],"** Build your own scene for TLD **",
		[                                         (jump_to_menu, "mnu_build_your_scene"),]),
#	("dressing_room" ,[(eq, cheat_switch, 1)],"Dressing Room",
		#[(assign, "$g_custom_battle_scenario", 99),(jump_to_menu, "mnu_custom_battle_2"),]),
    ("go_back"                  ,[],"Go back",[(change_screen_quit)])]
 ),
# This needs to be the fourth window!!!

] + (is_a_wb_menu==1 and [
(
    "tutorial",menu_text_color(0xFF000d2c)|mnf_disable_all_keys,
    "^^ Welcome to the Combat Tutorial for Mount & Blade. Here you will learn the basics of combat, as well as a brief overview of troop command during field battles.",
    "none",
    [(set_background_mesh, "mesh_town_goodcamp"),
     (set_passage_menu, "mnu_tutorial"),
     (try_begin),
       (eq, "$tutorial_1_finished", 1),
       (str_store_string, s1, "str_finished"),
     (else_try),
       (str_store_string, s1, "str_empty_string"),
     (try_end),
     (try_begin),
       (eq, "$tutorial_2_finished", 1),
       (str_store_string, s2, "str_finished"),
     (else_try),
       (str_store_string, s2, "str_empty_string"),
     (try_end),
     (try_begin),
       (eq, "$tutorial_3_finished", 1),
       (str_store_string, s3, "str_finished"),
     (else_try),
       (str_store_string, s3, "str_empty_string"),
     (try_end),
     (try_begin),
       (eq, "$tutorial_4_finished", 1),
       (str_store_string, s4, "str_finished"),
     (else_try),
       (str_store_string, s4, "str_empty_string"),
     (try_end),
     (try_begin),
       (eq, "$tutorial_5_finished", 1),
       (str_store_string, s5, "str_finished"),
     (else_try),
       (str_store_string, s5, "str_empty_string"),
     (try_end),
        ],
    [
      ("tutorial_1",[],"Tutorial #1: Basic movement and weapon selection. {s1}",[
           (modify_visitors_at_site,"scn_tutorial_1"),(reset_visitors,0),
           (set_jump_mission,"mt_tutorial_1"),
           (call_script,"script_start_as_one","trp_i1_gon_levy"),
           (assign, "$g_player_troop", "$player_current_troop_type"),
       	   (set_player_troop, "$g_player_troop"),
           (jump_to_scene,"scn_tutorial_1"),(change_screen_mission)]),
      ("tutorial_2",[],"Tutorial #2: Fighting with a shield. {s2}",[
           (modify_visitors_at_site,"scn_tutorial_2"),(reset_visitors,0),
           (call_script,"script_start_as_one","trp_i2_isen_uruk"),
           (assign, "$g_player_troop", "$player_current_troop_type"),
       	   (set_player_troop, "$g_player_troop"),
           (set_visitor,1,"trp_c2_squire_of_rohan"),
           (set_visitor,2,"trp_ac3_skirmisher_of_rohan"),
           (set_jump_mission,"mt_tutorial_2"),
           (jump_to_scene,"scn_tutorial_2"),(change_screen_mission)]),
      ("tutorial_3",[],"Tutorial #3: Fighting without a shield. {s3}",[
           (modify_visitors_at_site,"scn_tutorial_3"),(reset_visitors,0),
           (call_script,"script_start_as_one","trp_i3_beorning_tolltacker"),
           (assign, "$g_player_troop", "$player_current_troop_type"),
       	   (set_player_troop, "$g_player_troop"),
           (set_visitor,1,"trp_i2_mordor_orc"),
           (set_visitor,2,"trp_i4_mordor_num_vet_warrior"),
           (set_jump_mission,"mt_tutorial_3"),
           (jump_to_scene,"scn_tutorial_3"),(change_screen_mission)]),
      ("tutorial_3b",[(eq,0,1)],"Tutorial 3 b",[(try_begin),
                                                  (ge, "$tutorial_3_state", 12),
                                                  (modify_visitors_at_site,"scn_tutorial_3"),(reset_visitors,0),
                                                  (set_visitor,1,"trp_i2_mordor_orc"),
                                                  (set_visitor,2,"trp_i4_mordor_num_vet_warrior"),
                                                  (set_jump_mission,"mt_tutorial_3_2"),
                                                  (jump_to_scene,"scn_tutorial_3"),
                                                  (change_screen_mission),
                                                (else_try),
                                                  (display_message,"str_door_locked",0xFFFFAAAA),
                                                (try_end)], "next level"),
	  ("tutorial_4",[],"Tutorial #4: Riding a horse or a warg. {s4}",[
           (modify_visitors_at_site,"scn_tutorial_4"),(reset_visitors,0),
           (call_script,"script_start_as_one","trp_ca4_gunda_skirmisher"),
           (assign, "$g_player_troop", "$player_current_troop_type"),
       	   (set_player_troop, "$g_player_troop"),
           (set_jump_mission,"mt_tutorial_4"),
           (jump_to_scene,"scn_tutorial_4"),(change_screen_mission)]),
      ("tutorial_5",[],"Tutorial #5: Commanding a band of soldiers. {s5}",[
           (modify_visitors_at_site,"scn_tutorial_5"),(reset_visitors,0),
           (call_script,"script_start_as_one","trp_a6_riv_guardian"),
           (assign, "$g_player_troop", "$player_current_troop_type"),
       	   (set_player_troop, "$g_player_troop"),
           (set_visitors,1,"trp_i3_riv_swordbearer",3),
           (set_visitors,2,"trp_i3_riv_swordbearer",3),
           (set_visitors,3,"trp_i4_riv_vet_swordbearer",2),
           (set_visitors,4,"trp_i6_riv_champion",2),
           (set_jump_mission,"mt_tutorial_5"),
           (jump_to_scene,"scn_tutorial_5"),(change_screen_mission)]),

      ("go_back_dot",[],"Go back.",
       [(change_screen_quit),
        ]
       ),
    ]
  ),
] or [

( "tutorial",mnf_disable_all_keys,
    "^^TLD has a lot of features unknown to native M&B. Those are described in some non-spoilerish detail in PDF included with the release. For tutorial on basic game mechanics please use Native module",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window")],
	[("go_back_dot",[],"Go back.",[(change_screen_quit)])]),

]) + [

# This needs to be the fifth window!!!  
( "reports",0,
   "^^^{s9}", "none",
   [(set_background_mesh, "mesh_ui_default_menu_window"),
	# Player Reward System (mtarini)
	(call_script, "script_update_respoint"), # so that current money is registered as res point of appropriate faction
	(faction_get_slot, reg10, "$players_kingdom", slot_faction_rank),
	(faction_get_slot, reg11, "$players_kingdom", slot_faction_influence),
	(faction_get_slot, reg12, "$players_kingdom", slot_faction_respoint ),
	(str_store_faction_name, s16, "$players_kingdom"),
    (call_script, "script_get_faction_rank", "$players_kingdom"),
    (assign, reg13, reg0),
	(call_script, "script_get_own_rank_title_to_s24", "$players_kingdom", reg13),
	(store_add, ":next_rank", reg13, 1),
	(call_script, "script_get_rank_points_for_rank", ":next_rank"), #convert to rank points
	(assign, reg20, reg0),
	(val_sub, reg20, reg10),
	(str_store_string, s11, "@{s24} ({reg13}) - {reg20} until next promotion^"),  # first title (own faction)
	(str_store_string, s13, "@Influence:^ {reg11} (with {s16})^"),  # first inf
	(str_store_string, s15, "@Resource Points:^ {reg12} (in {s16})^"),  # first rp

	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(neg|eq,"$players_kingdom", ":fac"),
		(faction_get_slot, reg10, ":fac", slot_faction_rank),
		(faction_get_slot, reg11, ":fac", slot_faction_influence),
		(faction_get_slot, reg12, ":fac", slot_faction_respoint ),
		(str_store_faction_name, s16, ":fac"),
		
		(call_script, "script_get_faction_rank", ":fac"),
		(assign, reg13, reg0),
		(call_script, "script_get_allied_rank_title_to_s24", ":fac", reg13),
		(store_add, ":next_rank_ally", reg13, 1),
		(call_script, "script_get_rank_points_for_rank", ":next_rank_ally"), #convert to rank points
		(assign, reg21, reg0),
		(val_sub, reg21, reg10),
		(try_begin), 
			(this_or_next|gt, reg10, 0),(eq, "$ambient_faction", ":fac"), (str_store_string, s11, "@{s11} {s24} ({reg13}) - {reg21} until next promotion^"),  # title
		(try_end),
		(try_begin), 
			(this_or_next|gt, reg11, 0),(eq, "$ambient_faction", ":fac"), (str_store_string, s13, "@{s13} {reg11} (with {s16})^"),  # finf
		(try_end),
		(try_begin), 
			(this_or_next|gt, reg12, 0),(eq, "$ambient_faction", ":fac"), (str_store_string, s15, "@{s15} {reg12} (in {s16})^"),  # first rp
		(try_end),
	(try_end),
	(str_store_troop_name, s10, "$g_player_troop"),
	(str_store_string, s9, "@-={s10}=-^{s11}^^^{s13}^^^{s15}."),
    ],
    [ 
 ]+concatenate_scripts([[		
	  ("cheat_faction_orders"  ,[(eq,"$cheat_mode",1)],"Cheat: Faction orders."   ,[(jump_to_menu, "mnu_faction_orders"   ),]),
 ] for ct in range(cheat_switch)])

 	 +
 	   ## Kham - Troop Trees
	   ((is_a_wb_menu==1) and
	   [
	      ("action_view_troop_trees",[],"View troop trees.", [(start_presentation, "prsnt_faction_troop_trees"),]),
	   ]
	   or
	   [
	      # 1011: do nothing
	   ])
	   ## Troop Trees End
	   +
	 
	 [("view_upkeep_costs"     ,[                    ],"View upkeep costs."       ,[(jump_to_menu, "mnu_upkeep_report" ),]),
      ("view_character_report" ,[                    ],"View character report."   ,[(jump_to_menu, "mnu_character_report" ),]),
      ("view_party_size_report",[                    ],"View party size report."  ,[(jump_to_menu, "mnu_party_size_report"),]),
      ("view_morale_report"    ,[                    ],"View party morale report.",[(jump_to_menu, "mnu_morale_report"    ),]),
#NPC companion changes begin
#      ("view_party_preferences",[],"View party management preferences.", [(jump_to_menu, "mnu_party_preferences"),]),
      
      ("view_active_theaters", [(eq, "$cheat_mode", 1)], "View Active Theaters",
      	[(try_for_range, ":factions", kingdoms_begin, kingdoms_end),
      		(faction_slot_eq, ":factions", slot_faction_state, sfs_active), 
      		(faction_get_slot, ":theater", ":factions", slot_faction_active_theater),
      		(call_script, "script_theater_name_to_s15", ":theater"),
      		(str_store_faction_name, s1, ":factions"),
      		(display_message, "@{s1} - {s15}", color_good_news),
      	 (try_end)]),

    	("view_active_factions", [(eq, "$cheat_mode", 1)], "View Active Factions",
      	[(try_for_range, ":factions", kingdoms_begin, kingdoms_end),
      		(faction_get_slot, reg1, ":factions", slot_faction_state),
      		(str_store_faction_name, s1, ":factions"),
      		(display_message, "@{s1} - {reg1}", color_good_news),
      	 (try_end)]),

      ("view_character_report_02" ,[(eq,"$cheat_mode",1)],"NPC status check.",
       [(try_for_range, ":npc", companions_begin, companions_end),
            (main_party_has_troop, ":npc"),
            (str_store_troop_name, s4, ":npc"),
            (troop_get_slot, reg3, ":npc", slot_troop_morality_state),
            (troop_get_slot, reg4, ":npc", slot_troop_2ary_morality_state),
            (troop_get_slot, reg5, ":npc", slot_troop_personalityclash_state),    
            (troop_get_slot, reg6, ":npc", slot_troop_personalityclash2_state),    
            (troop_get_slot, reg7, ":npc", slot_troop_personalitymatch_state),    
            (display_message, "@{s4}: M{reg3}, 2M{reg4}, PC{reg5}, 2PC{reg6}, PM{reg7}"),
        (try_end),
        (try_for_range, ":npc", new_companions_begin, new_companions_end),
            (main_party_has_troop, ":npc"),
            (str_store_troop_name, s4, ":npc"),
            (troop_get_slot, reg3, ":npc", slot_troop_morality_state),
            (troop_get_slot, reg4, ":npc", slot_troop_2ary_morality_state),
            (troop_get_slot, reg5, ":npc", slot_troop_personalityclash_state),    
            (troop_get_slot, reg6, ":npc", slot_troop_personalityclash2_state),    
            (troop_get_slot, reg7, ":npc", slot_troop_personalitymatch_state),    
            (display_message, "@{s4}: M{reg3}, 2M{reg4}, PC{reg5}, 2PC{reg6}, PM{reg7}"),
        (try_end),
        ]),
#NPC companion changes end
      ("view_faction_strengths_report",[],"View faction strengths report.",[(jump_to_menu, "mnu_faction_strengths_report"),]),
      #("view_faction_relations_report",[],"View faction relations report.",[(jump_to_menu, "mnu_faction_relations_report"),]),
      ("view_traits_report",[],"View traits.",[(jump_to_menu, "mnu_traits_report"),]),
      ("resume_travelling"            ,[],"Resume travelling."            ,[(change_screen_return),]),
    ]
 ),

###CUSTOMBATTLE2###

("custom_battle_2",mnf_disable_all_keys,
    "^^^^^^{s16}",
    "none",
    [(assign, "$g_battle_result", 0),
     (set_show_messages, 0),
     (troop_clear_inventory, "trp_player"),
     (troop_raise_attribute, "trp_player", ca_strength, -1000),
     (troop_raise_attribute, "trp_player", ca_agility, -1000),
     (troop_raise_skill, "trp_player", skl_shield, -1000),
     (troop_raise_skill, "trp_player", skl_athletics, -1000),
     (troop_raise_skill, "trp_player", skl_riding, -1000),
     (troop_raise_skill, "trp_player", skl_power_strike, -1000),
     (troop_raise_skill, "trp_player", skl_power_throw, -1000),
     (troop_raise_skill, "trp_player", skl_weapon_master, -1000),
     (troop_raise_skill, "trp_player", skl_horse_archery, -1000),
     (troop_raise_skill, "trp_player", skl_ironflesh, -1000),
     (troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, -10000),
     (troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, -10000),
     (troop_raise_proficiency_linear, "trp_player", wpt_polearm, -10000),
     (troop_raise_proficiency_linear, "trp_player", wpt_archery, -10000),
     (troop_raise_proficiency_linear, "trp_player", wpt_crossbow, -10000),
     (troop_raise_proficiency_linear, "trp_player", wpt_throwing, -10000),
     (reset_visitors),

############################################   Scene 1 Start "Gondor factions vs Harad"
     (try_begin),
       (eq, "$g_custom_battle_scenario", 1),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_1"),

       (assign, "$g_player_troop", "trp_knight_1_1"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
       (troop_add_item, "$g_player_troop","itm_gondor_bow",0),
       (troop_add_item, "$g_player_troop","itm_khergit_arrows",0),
       (troop_equip_items, "$g_player_troop"),
     
		(set_visitors, 1, "trp_i1_loss_woodsman",			10),
		(set_visitors, 2, "trp_i2_loss_axeman",			6),
		(set_visitors, 3, "trp_i5_loss_axemaster",		4),
		(set_visitors, 4, "trp_i1_lam_clansman",			10),
		(set_visitors, 5, "trp_i2_lam_footman",				6),
		(set_visitors, 6, "trp_i3_lam_veteran",				4),
		(set_visitors, 7, "trp_i1_pinnath_plainsman",		10),
		(set_visitors, 8, "trp_c2_pinnath_rider",			6),
		(set_visitors, 9, "trp_c3_pinnath_knight",		4),
		(set_visitors, 10, "trp_c4_amroth_knight",			10),
		(set_visitors, 11, "trp_c5_amroth_vet_knight",	6),
		(set_visitors, 12, "trp_c6_amroth_swan_knight",		4),
#       (set_visitors, 13, "trp_i1_amroth_recruit",				5),
#       (set_visitors, 14, "trp_c2_amroth_squire",			3),
#       (set_visitors, 15, "trp_c3_amroth_vet_squire",	2),
		(set_visitors, 13, "trp_c4_amroth_knight",			10),
		(set_visitors, 14, "trp_c5_amroth_vet_knight",	6),
		(set_visitors, 15, "trp_c6_amroth_swan_knight",		4),
#		Enemy
		(set_visitors, 16, "trp_i1_harad_levy",			6),
		(set_visitors, 17, "trp_i1_harad_levy",			6),
		(set_visitors, 18, "trp_c2_harondor_scout",				6),
		(set_visitors, 19, "trp_i3_harad_infantry",				6),
		(set_visitors, 20, "trp_i4_harad_spearman",		6),
		(set_visitors, 21, "trp_i5_harad_tiger_guard",				6),
		(set_visitors, 22, "trp_i5_harad_lion_guard",				6),
		(set_visitors, 23, "trp_c3_harondor_rider",				6),
		(set_visitors, 24, "trp_c4_harondor_light_cavalry",		6),
		(set_visitors, 25, "trp_c5_harondor_serpent_knight",			6),
		(set_visitors, 26, "trp_a3_harad_hunter",				6),
		(set_visitors, 27, "trp_a4_harad_archer",					6),
		(set_visitors, 28, "trp_a5_harad_eagle_guard",				6),
		#(set_visitors, 29, "trp_moria_troll",				1),
		(str_store_string, s16, "str_custom_battle_1"),

############################################# "Dressing Room"
     (else_try),
     (eq, "$g_custom_battle_scenario", 99),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_ambush"),
       (assign, "$g_player_troop", "trp_lorien_marshall"), #Celeborn
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
       (set_visitor, 1, "trp_dorwinion_spirit_leader"),
       (set_visitors,2, "trp_dorwinion_spirit", 2),
       (set_visitor,3, "trp_knight_6_1"),
       (set_visitor,4, "trp_knight_6_2"),
       (str_store_string, s16, "@Dressing Room"),
     (else_try),
	   # Kham - Formations Test
       (eq, "$g_custom_battle_scenario", 98),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_5"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_jump_entry, 0),
       (set_visitor, 0, "trp_player"),
	   (set_visitors, 17, "trp_i3_isen_uruk_pikeman",				20),
	   (str_store_string, s16, "@Formations Test"),
     (else_try),
       (eq, "$g_custom_battle_scenario", 2),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_3"),

############################################# "Elves kick ass"
       (assign, "$g_player_troop", "trp_knight_3_6"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
     
		(set_visitors, 1, "trp_a1_lorien_scout",					5),
		(set_visitors, 2, "trp_a2_lorien_warden",			5),
		(set_visitors, 3, "trp_a3_lorien_vet_warden",					5),
		(set_visitors, 4, "trp_a4_lorien_gal_warden",			5),
		(set_visitors, 5, "trp_a5_lorien_gal_royal_warden",			5),
		(set_visitors, 6, "trp_a6_lorien_grey_warden",				5),
		(set_visitors, 7, "trp_galadhrim_royal_marksman",			5),
		(set_visitors, 8, "trp_noldorin_mounted_archer",			5),
		(set_visitors, 9, "trp_a2_lorien_archer",				5),
		(set_visitors, 10, "trp_a3_lorien_vet_archer",		5),
		(set_visitors, 11, "trp_a4_lorien_gal_archer",			5),
		(set_visitors, 12, "trp_a5_lorien_gal_royal_archer",			5),
		(set_visitors, 13, "trp_i3_lorien_inf",					5),
		(set_visitors, 14, "trp_i4_lorien_gal_inf",			5),
		(set_visitors, 15, "trp_i5_lorien_gal_royal_inf",			5),
#		ENEMY
		(set_visitors, 16, "trp_i3_mordor_num_warrior",			5),
		(set_visitors, 17, "trp_i4_mordor_num_vet_warrior",	5),
		(set_visitors, 18, "trp_i5_mordor_num_champion",			5),
		(set_visitors, 19, "trp_i5_mordor_num_assassin",			5),
		(set_visitors, 20, "trp_c4_mordor_num_horseman",	5),
		(set_visitors, 21, "trp_c5_mordor_num_knight",		5),
		(set_visitors, 22, "trp_black_numenorean_captain",			5),
		(set_visitors, 23, "trp_black_numenorean_lieutenant",		4),
		(set_visitors, 25, "trp_high_captain_of_mordor",			4),
		(set_visitors, 26, "trp_ac4_harondor_horse_archer",		6),
		(set_visitors, 27, "trp_ac5_harondor_black_snake",		6),
		(str_store_string, s16, "str_custom_battle_2"),

     (else_try),
##########################################   SCENE 4 Start "Helms Deep defence"
       (eq, "$g_custom_battle_scenario", 3),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_4"),

       (assign, "$g_player_troop", "trp_knight_1_9"),
       (set_player_troop, "$g_player_troop"),
     
       (troop_raise_attribute, "$g_player_troop", ca_strength, 12),
       (troop_raise_attribute, "$g_player_troop", ca_agility, 9),
       (troop_raise_skill, "$g_player_troop", skl_shield, 3),
       (troop_raise_skill, "$g_player_troop", skl_athletics, 4),
       (troop_raise_skill, "$g_player_troop", skl_riding, 3),
       (troop_raise_skill, "$g_player_troop", skl_power_strike, 4),
       (troop_raise_skill, "$g_player_troop", skl_power_draw, 5),
       (troop_raise_skill, "$g_player_troop", skl_ironflesh, 6),
       (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 200),
       (troop_raise_proficiency_linear, "$g_player_troop", wpt_two_handed_weapon, 200),
       (troop_raise_proficiency_linear, "$g_player_troop", wpt_polearm, 200),
       (troop_raise_proficiency_linear, "$g_player_troop", wpt_archery, 210),
       (troop_raise_proficiency_linear, "$g_player_troop", wpt_throwing, 110),
     
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
       (troop_add_item, "$g_player_troop","itm_strong_bow",0),
       (troop_add_item, "$g_player_troop","itm_khergit_arrows",0),
       (troop_equip_items, "$g_player_troop"),
## US     
		(set_visitors, 1, "trp_i6_2h_guard_of_rohan",				6),
		(set_visitors, 2, "trp_dismounted_elite_skirmisher_of_rohan",		6),
		(set_visitors, 3, "trp_dismounted_elite_skirmisher_of_rohan",			6),
		(set_visitors, 4, "trp_i5_raider_of_rohan",					6),
		(set_visitors, 5, "trp_i6_footman_guard_of_rohan",					6),
		(set_visitors, 6, "trp_i4_veteran_footman_of_rohan",					6),
		(set_visitors, 7, "trp_i6_warden_of_methuseld",						6),
		(set_visitors, 8, "trp_dismounted_veteran_skirmisher_of_rohan",		6),
		(set_visitors, 9, "trp_i1_rohan_youth",								6),
		(set_visitors, 10, "trp_i2_guardsman_of_rohan",						6),
		(set_visitors, 11, "trp_i3_footman_of_rohan",							6),
		(set_visitors, 12, "trp_i5_elite_footman_of_rohan",					6),
		(set_visitors, 13, "trp_a4_lorien_gal_warden",					8),
		(set_visitors, 14, "trp_dismounted_veteran_skirmisher_of_rohan",	6),
		(set_visitors, 15, "trp_dismounted_veteran_skirmisher_of_rohan",	6),
		(set_visitors, 40, "trp_dismounted_veteran_skirmisher_of_rohan",	2),
		(set_visitors, 41, "trp_dismounted_veteran_skirmisher_of_rohan",	2),
		(set_visitors, 42, "trp_dismounted_veteran_skirmisher_of_rohan",	2),
		(set_visitors, 43, "trp_dismounted_veteran_skirmisher_of_rohan",	2),
		(set_visitors, 44, "trp_dismounted_veteran_skirmisher_of_rohan",	2),
## ENEMY
		(set_visitors, 16, "trp_a2_isen_uruk_tracker",							6),
		(set_visitors, 17, "trp_a3_isen_large_uruk_tracker",					6),
		(set_visitors, 18, "trp_a4_isen_fighting_uruk_tracker",					6),
		(set_visitors, 19, "trp_i6_isen_uruk_berserker",				16),
		(set_visitors, 20, "trp_i1_isen_uruk_snaga",					30),
		(set_visitors, 21, "trp_i2_isen_uruk",						30),
		(set_visitors, 22, "trp_i3_isen_large_uruk",				20),
		(set_visitors, 23, "trp_i4_isen_fighting_uruk_warrior",					10),
		(set_visitors, 24, "trp_i3_isen_uruk_pikeman",							20),
		(set_visitors, 25, "trp_i4_isen_fighting_uruk_pikeman",					10),
		(set_visitors, 26, "trp_i5_isen_fighting_uruk_champion",				10),
		(set_visitors, 27, "trp_i4_dun_wolf_warrior",						30),
		(set_visitors, 28, "trp_i2_dun_warrior",							15),
		(set_visitors, 29, "trp_i5_dun_wolf_guard",						5),
		(str_store_string, s16, "str_custom_battle_3"),
     
     (else_try),
##########################################   Scene 5 "Northen guys vs Rhun
       (eq, "$g_custom_battle_scenario", 4),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_5"),

       (assign, "$g_player_troop", "trp_knight_4_11"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
     
## US     
       (set_visitors, 1, "trp_i1_woodmen_man",				30),
#       (set_visitors, 2, "trp_woodsman_scout",				3),
#		(set_visitors, 1, "trp_a2_dale_scout",				3),
		(set_visitors, 2, "trp_a3_dale_bowman",			6),
		(set_visitors, 3, "trp_a4_dale_archer",			6),
		(set_visitors, 4, "trp_i1_beorning_man",			6),
		(set_visitors, 5, "trp_i2_beorning_warrior",			6),
#       (set_visitors, 3, "trp_dale_noble",					3),
#       (set_visitors, 4, "trp_dale_squire",				3),   
#       (set_visitors, 5, "trp_dale_mounted_moble",			3),
		(set_visitors, 6, "trp_i3_beorning_tolltacker",		6),
		(set_visitors, 7, "trp_i4_beorning_sentinel",			6),
		(set_visitors, 8, "trp_i5_beorning_warden_of_the_ford",6),
		(set_visitors, 9, "trp_i3_beorning_carrock_lookout",	6),
		(set_visitors, 10, "trp_i4_beorning_carrock_fighter",	6),
		(set_visitors, 11, "trp_i1_dale_militia",				6),
		(set_visitors, 12, "trp_i2_dale_man_at_arms",			6),
		(set_visitors, 13, "trp_i3_dale_swordsman",				6),
		(set_visitors, 14, "trp_i4_dale_sergeant",		6),
		(set_visitors, 15, "trp_i5_dale_hearthman",			6),
#       (set_visitors, 15, "trp_bardian_master_archer",		3),
##     enemy Rhun
		(set_visitors, 16, "trp_i1_rhun_tribesman",			7),
		(set_visitors, 17, "trp_ac2_rhun_horse_scout",			7),
		(set_visitors, 18, "trp_ac3_rhun_horse_archer",			7),
		(set_visitors, 19, "trp_ac4_rhun_veteran_horse_archer",	7),
		(set_visitors, 20, "trp_ac5_rhun_balchoth_horse_archer",7),
		(set_visitors, 21, "trp_c3_rhun_swift_horseman",		7),
		(set_visitors, 22, "trp_c4_rhun_veteran_swift_horseman",7),
		(set_visitors, 23, "trp_c5_rhun_falcon_horseman",           7),
		(set_visitors, 24, "trp_i2_rhun_tribal_warrior",		7),
		(set_visitors, 25, "trp_i3_rhun_tribal_infantry",		7),
		(set_visitors, 26, "trp_i4_rhun_vet_infantry",			7),
		(set_visitors, 27, "trp_i5_rhun_ox_warrior",		7),
		(set_visitors, 28, "trp_c2_rhun_horseman",       7),
		(set_visitors, 29, "trp_c3_rhun_outrider",        7),
		(set_visitors, 30, "trp_c4_rhun_noble_rider",        7),
		(set_visitors, 31, "trp_c6_rhun_warlord",	7),
		(str_store_string, s16, "str_custom_battle_4"),
     
     (else_try),
########################################## MORIA GUNDA VS DWARVES  
       (eq, "$g_custom_battle_scenario", 5),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_7"),

       (assign, "$g_player_troop", "trp_knight_2_1"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor,  0, "$g_player_troop"),

		(set_visitors, 1, "trp_i1_moria_snaga",					5),
		(set_visitors, 2, "trp_i2_moria_goblin",				5),
		(set_visitors, 3, "trp_i3_moria_large_goblin",			5),
		(set_visitors, 4, "trp_i4_moria_fell_goblin",			5),
		(set_visitors, 5, "trp_a2_moria_goblin_archer",			5),
		(set_visitors, 6, "trp_a3_moria_large_goblin_archer",	5),
		(set_visitors, 7, "trp_i5_moria_deep_dweller",	5),
		(set_visitors, 8, "trp_i1_gunda_goblin",				5),
		(set_visitors, 9, "trp_i2_gunda_orc",					5),
## ENEMY
		(set_visitors, 11, "trp_i1_dwarf_apprentice",		3),
		(set_visitors, 12, "trp_i2_dwarf_warrior",			3),
		(set_visitors, 13, "trp_i3_dwarf_hardened_warrior",	3),
		(set_visitors, 14, "trp_i4_dwarf_spearman",			3),
		(set_visitors, 16, "trp_i5_dwarf_pikeman",			3),
		(set_visitors, 17, "trp_i6_dwarf_longpikeman",		3),
		(set_visitors, 18, "trp_i4_dwarf_axeman",			3),
		(set_visitors, 40, "trp_i5_dwarf_expert_axeman",		3),
		(set_visitors, 41, "trp_i6_dwarf_longbeard_axeman",			3),
		(set_visitors, 42, "trp_a3_dwarf_scout",				2),
		(set_visitors, 43, "trp_a4_dwarf_bowman",			2),
		(set_visitors, 44, "trp_a4_dwarf_bowman",			2),
		(set_visitors, 45, "trp_a4_dwarf_bowman",		2),
		(str_store_string, s16, "str_custom_battle_5"),
     (else_try),
########################################## ORCS VS MIRKWOOD  
       (eq, "$g_custom_battle_scenario", 6),
       (assign, "$g_custom_battle_scene", "scn_quick_battle_ambush"),

       (assign, "$g_player_troop", "trp_knight_1_15"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),

		(set_visitors, 1, "trp_i3_gunda_orc_fighter",				8),
		(set_visitors, 2, "trp_i4_gunda_orc_warrior",		6),
		(set_visitors, 3, "trp_i4_gunda_orc_berserker",			10),
		(set_visitors, 4, "trp_i4_moria_fell_goblin",					6),
		(set_visitors, 5, "trp_c5_moria_clan_rider",						2),
		(set_visitors, 6, "trp_c4_moria_warg_rider",					4),
		(set_visitors, 7, "trp_c3_moria_wolf_rider",					4),
		(set_visitors, 8, "trp_i1_gunda_goblin",					10),
		(set_visitors, 9, "trp_i2_gunda_orc",						12),
		(set_visitors, 10, "trp_ca4_gunda_skirmisher",8),
		(set_visitors, 11, "trp_ca5_gunda_clan_skirmisher",		4),
		(set_visitors, 12, "trp_c4_gunda_warg_rider",			4),
		(set_visitors, 13, "trp_c4_gunda_warg_rider",				4),
		(set_visitors, 14, "trp_c5_gunda_clan_rider",				2),
## ENEMY
		(set_visitors, 16, "trp_a1_greenwood_scout",						5),
		(set_visitors, 17, "trp_a2_greenwood_veteran_scout",				5),
		(set_visitors, 18, "trp_a3_greenwood_archer",						5),
		(set_visitors, 19, "trp_a4_greenwood_veteran_archer",				3),
		(set_visitors, 20, "trp_a5_greenwood_master_archer",				3),
		(set_visitors, 21, "trp_a6_greenwood_chosen_marksman",				3),
		(set_visitors, 22, "trp_noldorin_mounted_archer",				3),
		(set_visitors, 23, "trp_a1_riv_scout",						3),
		(set_visitors, 24, "trp_a2_riv_vet_scout",				3),
		(set_visitors, 25, "trp_a3_riv_archer",					3),
		(set_visitors, 26, "trp_i4_greenwood_elite_infantry",				3),
		(set_visitors, 27, "trp_i3_greenwood_vet_infantry",			3),
		(set_visitors, 28, "trp_i2_greenwood_infantry",					3),
		(str_store_string, s16, "str_custom_battle_6"),
     (else_try),
     ########################################## Ori's Last Stand
       	(eq, "$g_custom_battle_scenario", 8),
       	(assign, "$g_custom_battle_scene", "scn_erebor_castle_2"),



       	(modify_visitors_at_site, "$g_custom_battle_scene"),
       	(assign, "$g_player_troop", "trp_multiplayer_profile_troop_male"),
       	(set_visitor, 0, "$g_player_troop"),

		(set_visitor, 1, "trp_generic_hero_infantry"),
		(set_visitor, 2, "trp_generic_hero_ranged"),
		(set_visitor, 3, "trp_generic_hero_knight"),
		(set_visitor, 4, "trp_generic_hero_mounted_archer"),
		
## ENEMY
		(set_visitors, 16, "trp_i1_moria_snaga",						5),
		(set_visitors, 17, "trp_i1_moria_snaga",						5),
		(set_visitors, 18, "trp_i1_moria_snaga",						5),
		
		(str_store_string, s16, "@Four years after bringing a group of Dwarves from Erebor to attempt to resettle the once-Dwarven city of Khazad-dûm, Balin was killed by an Orc arrow while peering into Lake Mirrormere, and his people became immediately engaged with many Orcs coming up the Silverlode River. After a continuous retreat from the East-gate and First Hall, then the Bridge of Khazad-dûm and Second Hall, the remaining Longbeards were forced all the way back into the Twenty-first Hall. After an unsuccessful attempt to escape through the Doors of Durin that saw the death of Óin, the Chamber of Mazarbul became the last hold-out of the Colony after losing the Twenty-first Hall just outside the chamber. Barring the gates, Ori and the few survivors set up a final defense."),
		(set_background_mesh, "mesh_town_erebor"),
	 (else_try),
     ########################################## Darkness Attack
       	(eq, "$g_custom_battle_scenario", 88),
       	(assign, "$g_custom_battle_scene", "scn_random_scene_plain_forest_custom_5"),
       	(troop_set_slot, "trp_dorwinion_spirit_leader", slot_troop_hp_shield, 200),
       	(assign, "$g_player_troop", "trp_knight_1_7"),
    	(set_player_troop, "$g_player_troop"),
	    (modify_visitors_at_site, "$g_custom_battle_scene"),

       	(set_visitor, 0, "$g_player_troop"),
		(set_visitors, 4, "trp_i1_mordor_orc_snaga", 2),
		(set_visitors, 5, "trp_i1_mordor_orc_snaga", 2),
		(set_visitors, 6, "trp_i1_mordor_orc_snaga", 2),

		
## ENEMY
		
		(str_store_string, s16, "@You chase an orc scout party into the forest..."),
		(set_background_mesh, "mesh_draw_orc_raiders"),
     (else_try),
########################################## GONDOR VS CORSAIRS  
       (eq, "$g_custom_battle_scenario", 7),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_outside"),

       (assign, "$g_player_troop", "trp_knight_1_1"), #Malvogil
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),

		(set_visitors, 1, "trp_i1_gon_levy",				8),
		(set_visitors, 2, "trp_i2_gon_watchman",				6),
		(set_visitors, 3, "trp_i3_gon_footman",				6),
		(set_visitors, 4, "trp_i4_gon_spearman",				6),
		(set_visitors, 5, "trp_i5_gon_vet_spearman",		2),
		(set_visitors, 6, "trp_i6_gon_tower_spearman",	4),
		(set_visitors, 7, "trp_a4_ithilien_ranger",				4),
		(set_visitors, 8, "trp_i4_gon_swordsman",				6),
		(set_visitors, 9, "trp_i5_gon_vet_swordsman",		6),
		(set_visitors, 10, "trp_i6_gon_tower_swordsman",	4),
		(set_visitors, 11, "trp_a6_gon_tower_archer",		4),
		(set_visitors, 12, "trp_a3_gon_bowman",				4),
		(set_visitors, 13, "trp_a4_gon_archer",				4),
		(set_visitors, 14, "trp_a5_gon_vet_archer",		2),
## ENEMY
		(set_visitors, 16, "trp_mordor_olog_hai",				2),
		(set_visitors, 16, "trp_i1_corsair_youth",					6),
		(set_visitors, 17, "trp_i2_corsair_warrior",				6),
		(set_visitors, 18, "trp_i3_corsair_swordsman",				6),
		(set_visitors, 19, "trp_i4_corsair_veteran_swordsman",		4),
		(set_visitors, 20, "trp_i5_corsair_night_raider",			4),
		(set_visitors, 21, "trp_a2_corsair_marine",				4),
		(set_visitors, 22, "trp_a3_corsair_marksman",				4),
		(set_visitors, 23, "trp_a4_corsair_veteran_marksman",		4),
		(set_visitors, 24, "trp_a5_corsair_master_marksman",		4),
		(set_visitors, 25, "trp_i3_corsair_swordsman",				4),
		(set_visitors, 26, "trp_i4_corsair_veteran_swordsman",		4),
		(set_visitors, 27, "trp_i5_corsair_master_swordsman",		4),
		(set_visitors, 28, "trp_a4_corsair_assassin",				4),
		(str_store_string, s16, "str_custom_battle_7"),
 ]+concatenate_scripts([[
	(else_try),
########################################## FOOTBALL  
       # (eq, "$g_custom_battle_scenario", 8),
       # (assign, "$g_custom_battle_scene", "scn_town_1_arena_football"),

	   # (assign, "$g_player_troop", "trp_knight_1_1"), #Malvogil
       # (set_player_troop, "$g_player_troop"),
	   # (modify_visitors_at_site, "$g_custom_battle_scene"),
       # (set_visitor, 0, "$g_player_troop"),

		# (set_visitors, 1, "trp_i1_gon_levy", 1),
		# (set_visitors, 2, "trp_i1_gon_levy", 1),
		# (set_visitors, 3, "trp_i1_gon_levy", 1),
		# (set_visitors, 4, "trp_i1_gon_levy", 1),
		# (set_visitors, 5, "trp_i1_gon_levy", 1),
		# (set_visitors, 6, "trp_i1_gon_levy", 1),
		
		# (set_visitors, 16, "trp_townsman", 1),
		# (set_visitors, 17, "trp_townsman", 1),
		# (set_visitors, 18, "trp_townsman", 1),
		# (set_visitors, 19, "trp_townsman", 1),
		# (set_visitors, 20, "trp_townsman", 1),
		# (set_visitors, 21, "trp_townsman", 1),
		# (str_store_string, s16, "@They came here after we kicked their asses 5:0 in the first round! Let's do it again."),
      # (else_try),

	    # TROLL TEST
       (eq, "$g_custom_battle_scenario", 10),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_c3_pinnath_knight"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
			(try_for_range, ":trolls", trp_moria_troll, trp_ent2),
				(call_script, "script_get_hp_shield_value", ":trolls"),
			(try_end),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 1, "trp_i5_gon_vet_spearman",		8),
	   (set_visitors, 16, "trp_mordor_troll",				1),
	   (str_store_string, s16, "@TEST: troll VS infantry"),
     (else_try),
       (eq, "$g_custom_battle_scenario", 17),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign,"$field_ai_lord",1),
       (assign, "$g_player_troop", "trp_i5_gon_vet_spearman"),
			(try_for_range, ":trolls", trp_moria_troll, trp_ent2),
				(call_script, "script_get_hp_shield_value", ":trolls"),
			(try_end),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   #(set_visitors, 1, "trp_i4_gon_spearman",		30),
	   #(set_visitors, 1, "trp_i4_gon_swordsman",		10),
	   (set_visitors, 1, "trp_i3_gon_footman",		20),
	   (set_visitors, 16, "trp_mordor_troll",				2),
	   #(set_visitors, 16, "trp_mordor_olog_hai",				2),
	   #(set_visitors, 17, "trp_i2_mordor_orc",				20),
	   (str_store_string, s16, "@TEST: troll VS Weak infantry"),
     (else_try),
       (eq, "$g_custom_battle_scenario", 18),

       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_i4_greenwood_elite_infantry"),
			(try_for_range, ":trolls", trp_moria_troll, trp_ent2),
				(call_script, "script_get_hp_shield_value", ":trolls"),
			(try_end),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 1, "$g_player_troop"),
	   #(set_visitors, 1, "trp_i3_greenwood_vet_infantry",		7),
	   (set_visitors, 1, "trp_a4_greenwood_veteran_archer",		5),
	   (set_visitors, 16, "trp_gunda_vet_troll",				1),
	   (str_store_string, s16, "@TEST: troll VS Elves"),
     (else_try),
	    # TROLL TEST
       (eq, "$g_custom_battle_scenario", 11),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_a6_gon_tower_archer"),
			(try_for_range, ":trolls", trp_moria_troll, trp_ent2),
				(call_script, "script_get_hp_shield_value", ":trolls"),
			(try_end),
	   (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 1, "trp_a5_gon_vet_archer",		7),
	   (set_visitors, 16, "trp_isen_troll",				1),
	   (set_visitors, 17, "trp_i1_isen_orc_snaga",				1),
	   (str_store_string, s16, "@TEST: troll VS archers"),
	(else_try),
	    # TROLL TEST
       (eq, "$g_custom_battle_scenario", 12),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
			(try_for_range, ":trolls", trp_moria_troll, trp_ent2),
				(call_script, "script_get_hp_shield_value", ":trolls"),
			(try_end),
       (assign, "$g_player_troop", "trp_c6_rider_guard_of_rohan"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 1, "trp_c5_elite_rider_of_rohan",		6),
	   (set_visitors, 16, "trp_isen_armored_troll",				1),
	   (str_store_string, s16, "@TEST: troll VS chavalry"),
    (else_try),
	    # TROLL TEST
       (eq, "$g_custom_battle_scenario", 13),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
			(try_for_range, ":trolls", trp_moria_troll, trp_ent2),
				(call_script, "script_get_hp_shield_value", ":trolls"),
			(try_end),																   
       (assign, "$g_player_troop", "trp_c5_elite_lancer_of_rohan"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 1, "trp_c4_lancer_of_rohan",		6),
	   (set_visitors, 16, "trp_mordor_olog_hai",				1),
	   (str_store_string, s16, "@TEST: troll VS lancers"),
      (else_try),
	    # TROLL TEST
       (eq, "$g_custom_battle_scenario", 14),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_i6_isen_uruk_berserker"),
			(try_for_range, ":trolls", trp_moria_troll, trp_ent2),
				(call_script, "script_get_hp_shield_value", ":trolls"),
			(try_end),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 0, "trp_i2_isen_orc",	15),
	   (set_visitors, 0, "trp_isen_armored_troll",	1),
	   (set_visitors, 0, "trp_isen_vet_troll",	1),
	   (set_visitors, 16, "trp_mordor_olog_hai",	2),
	   (set_visitors, 17, "trp_i2_mordor_orc",	15),
 	   (str_store_string, s16, "@TEST: Troll vs Troll"),
    (else_try),
	    # TROLL TEST 3
       (eq, "$g_custom_battle_scenario", 15),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_mordor_olog_hai"),
			(try_for_range, ":trolls", trp_moria_troll, trp_ent2),
				(call_script, "script_get_hp_shield_value", ":trolls"),
			(try_end),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 16, "$g_player_troop"),
	   #(set_visitors, 1, "trp_i5_gon_vet_swordsman",				8),
	   (set_visitors, 1, "trp_i5_gon_vet_spearman",		8),
	   (set_visitors, 0, "trp_i5_gon_vet_swordsman",				1),
	   (str_store_string, s16, "@TEST: Troll by player"),
	   (str_store_string, s16, "@TROLL TEST"),
    (else_try),
	    # WARG TEST 1vs1
       (eq, "$g_custom_battle_scenario", 20),
       (assign, "$g_custom_battle_scene", "scn_random_scene_plain_forest"),
       (assign, "$g_player_troop", "trp_a6_gon_tower_archer"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 4, "$g_player_troop"),
	   (set_visitors, 1, "trp_ac2_isen_wolf_rider",				1),
	   (set_visitors, 2, "trp_ac2_isen_wolf_rider",				1),
	   (set_visitors, 3, "trp_ac2_isen_wolf_rider",				1),
	   (str_store_string, s16, "@TEST: warg test 1 VS 1"),
    (else_try),
	    # WARG TEST 2vs3
       (eq, "$g_custom_battle_scenario", 21),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_a6_gon_tower_archer"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 2, "trp_a5_gon_vet_archer",		1),
	   (set_visitors, 16, "trp_ac2_isen_wolf_rider",		    3),
	   (set_visitors, 17, "trp_i1_isen_orc_snaga",				1),
	   (str_store_string, s16, "@TEST: warg test 2 VS 3"),
    (else_try),
	    # WARG TEST 12vs8
       (eq, "$g_custom_battle_scenario", 22),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_a6_gon_tower_archer"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 2, "trp_a5_gon_vet_archer",		9),
	   (set_visitors, 16, "trp_ac2_isen_wolf_rider",		    9),
	   (set_visitors, 17, "trp_i1_isen_orc_snaga",				4),
	   (str_store_string, s16, "@TEST: warg test many VS many"),
    (else_try),
	    # WARG TEST 1vs1
       (eq, "$g_custom_battle_scenario", 23),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_ac2_isen_wolf_rider"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 17, "$g_player_troop"),
	   (set_visitors, 0, "trp_a5_gon_vet_archer",		1),
	   (str_store_string, s16, "@TEST: play warg, test 1 VS 1"),
    (else_try),
	    # WARG TEST 2vs3
       (eq, "$g_custom_battle_scenario", 24),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_ac4_isen_white_hand_rider"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 2, "trp_ac2_isen_wolf_rider",		    2),
	   (set_visitors, 16, "trp_a5_gon_vet_archer",		2),
	   #(set_visitors, 18, "trp_i1_isen_orc_snaga",				1),
	   (str_store_string, s16, "@TEST: play wargs, test 2 VS 3"),
    (else_try),
	    # WARG TEST 12vs8
       (eq, "$g_custom_battle_scenario", 25),
       (assign, "$g_custom_battle_scene", "scn_minas_tirith_center"),
       (assign, "$g_player_troop", "trp_ac4_isen_white_hand_rider"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   (set_visitors, 2, "trp_ac2_isen_wolf_rider",		    12),
	   (set_visitors, 16, "trp_a5_gon_vet_archer",		10),
	   #(set_visitors, 18, "trp_i1_isen_orc_snaga",				4),
	   (str_store_string, s16, "@TEST: play wargs, many VS many"),
   (else_try),########################################## TEST SCENE FOR DYNAMIC SCENERY  
		(eq, "$g_custom_battle_scenario", 26),
		#(assign, "$g_custom_battle_scene", "scn_quick_battle_3"),
		#(assign, "$g_custom_battle_scene", "scn_random_scene_plain_small"),
		(assign, "$g_custom_battle_scene", "scn_random_scene_parade"),
		#(modify_visitors_at_site, "$g_custom_battle_scene"),
		#(assign, "$g_player_troop", "$testbattle_team_a_troop"),
		#(set_player_troop, "$g_player_troop"),
	   (call_script, "script_get_hp_shield_value", "trp_mordor_olog_hai"),
	   (assign, "$g_player_troop", "$testbattle_team_a_troop"),
       (set_player_troop, "$g_player_troop"),
       (modify_visitors_at_site, "$g_custom_battle_scene"),
       (set_visitor, 0, "$g_player_troop"),
	   
		#(set_visitor, 0, "$g_player_troop"),

		
		(set_visitors, 2,"$testbattle_team_a_troop","$testbattle_team_a_num"),
		(set_visitors, 30,"$testbattle_team_b_troop","$testbattle_team_b_num"),
		(str_store_string, s16, "@TEST BATTLE: {reg10} {s10} vs {reg11} {s11}"),
   (else_try),########################################## TEST SCENE FOR DYNAMIC SCENERY  
		(eq, "$g_custom_battle_scenario", 9),
		(assign, "$g_custom_battle_scene", "scn_quick_battle_random"),

		(assign, "$g_player_troop", "trp_knight_1_1"), #Malvogil
		(set_player_troop, "$g_player_troop"),
		(modify_visitors_at_site, "$g_custom_battle_scene"),
	    (set_visitor, 0, "$g_player_troop"),
		
		(store_random_in_range,":gfac",0,9),  ## good faction chosen randomly
		(try_begin),
			(eq,":gfac",0),(assign,":trp_good_min","trp_i1_beorning_man"),(assign,":trp_good_max","trp_i5_beorning_warden_of_the_ford" ),(else_try),
			(eq,":gfac",1),(assign,":trp_good_min","trp_i1_dale_militia"     ),(assign,":trp_good_max","trp_ac5_rhovanion_marchwarden"       ),(else_try),
			(eq,":gfac",2),(assign,":trp_good_min","trp_i1_dwarf_apprentice"),(assign,":trp_good_max","trp_i6_dwarf_longpikeman"         ),(else_try),
			(eq,":gfac",3),(assign,":trp_good_min","trp_i1_loss_woodsman"),(assign,":trp_good_max","trp_a3_blackroot_archer"),(else_try),
			(eq,":gfac",4),(assign,":trp_good_min","trp_i1_amroth_recruit" ),(assign,":trp_good_max","trp_c6_amroth_swan_knight"   ),(else_try),
			(eq,":gfac",5),(assign,":trp_good_min","trp_a1_lorien_scout" ),(assign,":trp_good_max","trp_i5_lorien_gal_royal_inf"      ),(else_try),
			(eq,":gfac",6),(assign,":trp_good_min","trp_a1_greenwood_scout"  ),(assign,":trp_good_max","trp_ac6_riv_knight"         ),(else_try),
			(eq,":gfac",7),(assign,":trp_good_min","trp_a1_arnor_scout"   ),(assign,":trp_good_max","trp_a5_arnor_master_ranger"      ),(else_try),
			(eq,":gfac",8),(assign,":trp_good_min","trp_i1_rohan_youth"      ),(assign,":trp_good_max","trp_c6_rider_guard_of_rohan"         ),
		(try_end),

		(store_random_in_range,":bfac",0,9),  ## bad faction chosen randomly
		(try_begin),
			(eq,":bfac",0),(assign,":trp_bad_min","trp_i1_rhun_tribesman"       ),(assign,":trp_bad_max","trp_c6_rhun_warlord"    ),(else_try),
			(eq,":bfac",1),(assign,":trp_bad_min","trp_i1_harad_levy" ),(assign,":trp_bad_max","trp_ac5_harondor_black_snake" ),(else_try),
			(eq,":bfac",2),(assign,":trp_bad_min","trp_i1_dun_wildman"      ),(assign,":trp_bad_max","trp_ac5_dun_raven_rider"           ),(else_try),
			(eq,":bfac",3),(assign,":trp_bad_min","trp_i1_khand_bondsman"     ),(assign,":trp_bad_max","trp_ac5_khand_heavy_skirmisher"),(else_try),
			(eq,":bfac",4),(assign,":trp_bad_min","trp_i1_corsair_youth"        ),(assign,":trp_bad_max","trp_i5_corsair_master_pikeman"       ),(else_try),
			(eq,":bfac",5),(assign,":trp_bad_min","trp_i1_isen_orc_snaga"),(assign,":trp_bad_max","trp_i4_isen_fighting_uruk_pikeman"  ),(else_try),
			(eq,":bfac",6),(assign,":trp_bad_min","trp_i1_mordor_orc_snaga"  ),(assign,":trp_bad_max","trp_a4_mordor_fell_orc_archer"  ),(else_try),
			(eq,":bfac",7),(assign,":trp_bad_min","trp_c3_moria_wolf_rider"  ),(assign,":trp_bad_max","trp_i5_moria_deep_dweller"),(else_try),
			(eq,":bfac",8),(assign,":trp_bad_min","trp_i1_gunda_goblin"      ),(assign,":trp_bad_max","trp_c5_gunda_clan_rider"    ),
		(try_end),

		(store_random_in_range,":player_good",0,2),
		(try_begin),
			(eq,":player_good",0),
			(assign,":trp0_min",":trp_bad_min" ),(assign,":trp0_max",":trp_bad_max"),
			(assign,":trp1_min",":trp_good_min"),(assign,":trp1_max",":trp_good_max"),
		(else_try),
			(assign,":trp0_min",":trp_good_min"),(assign,":trp0_max",":trp_good_max"),
			(assign,":trp1_min",":trp_bad_min" ),(assign,":trp1_max",":trp_bad_max"),
		(try_end),

		(try_for_range,":i",1,7),
			(store_random_in_range,":trp",":trp0_min",":trp0_max"),
			(store_random_in_range,":n",3,10),
			(set_visitors, ":i", ":trp", ":n"),
		(try_end),
		(try_for_range,":i",16,22),
			(store_random_in_range,":trp",":trp1_min",":trp1_max"),
			(store_random_in_range,":n",3,10),
			(set_visitors, ":i", ":trp", ":n"),
		(try_end),
		
		(str_store_string, s16, "@TEST SCENE"),
		
    (else_try),########################################## CUSTOM FACTIONS  
		(eq, "$g_custom_battle_scenario", 16),
		(assign, "$g_custom_battle_scene", "scn_random_scene_parade"),

		(assign, "$g_player_troop", "trp_knight_1_1"), #Malvogil
		(set_player_troop, "$g_player_troop"),
		(modify_visitors_at_site, "$g_custom_battle_scene"),
	    (set_visitor, 0, "$g_player_troop"),
		
		# determine player and enemy faction
		(try_begin),(gt,"$cbadvantage",0),(assign,":ally_faction","$faction_good"),(assign,":enemy_faction","$faction_evil"),
         (else_try),                      (assign,":ally_faction","$faction_evil"),(assign,":enemy_faction","$faction_good"),(val_mul,"$cbadvantage",-1),
        (try_end),

		#spawn all ally and enemy faction troops 
		(assign,":ally_n",4),
		(assign,":enemy_n",4),
		(assign,":ally_entry",1),
		(assign,":enemy_entry",30),
		(try_for_range,":troop","trp_mercenaries_end","trp_looter"),
		    (neg|troop_is_hero,":troop"),
			(troop_get_type,":troop_faction",":troop"),
			(neq,":troop_faction",tf_troll), #GA: no trolls on battlefield
            (store_troop_faction,":troop_faction",":troop"),
			(try_begin),
			   (eq,":troop_faction",":ally_faction"),
               (lt,":ally_entry",30),
			      (set_visitors, ":ally_entry", ":troop", ":ally_n"),
			      (val_add,":ally_entry",1),
			(else_try),
			   (eq,":troop_faction",":enemy_faction"),
               (lt,":enemy_entry",60),
			      (set_visitors, ":enemy_entry", ":troop", ":enemy_n"),
			      (val_add,":enemy_entry",1),
		    (try_end),
		(try_end),

		(str_store_string, s16, "@FACTION SHOWOFF"),
 ] for ct in range(cheat_switch)])+[
	(try_end),
	(set_show_messages, 1),
	],
    
    [("custom_battle_go",[],"Start.",
       [(try_begin),(eq, "$g_custom_battle_scenario", 5),(set_jump_mission,"mt_custom_battle_5"),
         (else_try),(eq, "$g_custom_battle_scenario", 3),(set_jump_mission,"mt_custom_battle_HD"),#(rest_for_hours,8,1000,0),
		 ] + (is_a_wb_menu==1 and [
		 (else_try),(eq, "$g_custom_battle_scenario", 8),(set_jump_mission,"mt_ori_last_stand"),
		 (else_try),(eq, "$g_custom_battle_scenario", 88),(set_jump_mission,"mt_darkness_attack"),(rest_for_hours,3,1000,0),(stop_all_sounds, 1),
		 ] or []) + [
         (else_try),(eq, "$g_custom_battle_scenario", 9),(set_jump_mission,"mt_custom_battle_dynamic_scene"),
         (else_try),(eq, "$g_custom_battle_scenario",16),(set_jump_mission,"mt_custom_battle_parade"),#(rest_for_hours,12,1000,0),
         (else_try),(eq, "$g_custom_battle_scenario",26),(set_jump_mission,"mt_custom_battle_parade"),#(rest_for_hours,12,1000,0),
         (else_try),(eq, "$g_custom_battle_scenario",98),(set_jump_mission,"mt_custom_battle_form_test"),
	 (else_try),(set_jump_mission,"mt_custom_battle"),
        (try_end),
        (jump_to_menu, "mnu_custom_battle_end"),
        (jump_to_scene,"$g_custom_battle_scene"),
		(change_screen_mission),
       ]),
      ("leave_custom_battle_2",[],"Cancel.", [(jump_to_menu, "mnu_start_game_3"), ]),
    ]
 ),
( "custom_battle_end",mnf_disable_all_keys,
    "^^^^^^The battle is over. {s1} Your side killed {reg5} enemies and lost {reg6} troops over the battle.^You personally slew {reg7} opponents in the fighting.",
    "none",
    [(music_set_situation, 0),
     (assign, reg5, "$g_custom_battle_team2_death_count"),
     (assign, reg6, "$g_custom_battle_team1_death_count"),
     (get_player_agent_kill_count, ":kill_count"),
     (get_player_agent_kill_count, ":wound_count", 1),
     (store_add, reg7, ":kill_count", ":wound_count"),
     (try_begin),
       (eq, "$g_battle_result", 1),
       (str_store_string, s1, "str_battle_won"),
     (else_try),
       (str_store_string, s1, "str_battle_lost"),
     (try_end),
	],

	# (CppCoder) Ease not for only testing but for playing as well.
    	[
		("replay",[],"Play this battle again.",[(assign, "$battle_won", 0),(jump_to_menu, "mnu_custom_battle_2")]),
    		("continue_dot",[],"Continue.",[(try_begin),(eq,"$g_custom_battle_scenario",26),(jump_to_menu, "mnu_quick_battle_general_test"),(else_try),(change_screen_quit),(try_end)]),
   	]
 ),

( "custom_battle_durin_end",mnf_disable_all_keys,
    "^^^^^^It was an admirable last stand, but ultimately doomed.^^ You and your kinsmen killed {reg5} enemies.^You personally slew {reg7} opponents in the fighting.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
     (music_set_situation, 0),
     (assign, reg5, "$g_custom_battle_team2_death_count"),
     (get_player_agent_kill_count, ":kill_count"),
     (get_player_agent_kill_count, ":wound_count", 1),
     (store_add, reg7, ":kill_count", ":wound_count"),
	],

	# (CppCoder) Ease not for only testing but for playing as well.
    	[
		("replay_cbd",[],"Play this battle again.",[(assign, "$battle_won", 0),(jump_to_menu, "mnu_custom_battle_2")]),
    		("continue_dot_cbd",[],"Continue.",[(try_begin),(eq,"$g_custom_battle_scenario",26),(jump_to_menu, "mnu_quick_battle_general_test"),(else_try),(change_screen_quit),(try_end)]),
   	]
 ),

######################################
#TLD Troll quick battle choser
( "quick_battle_general_test",mnf_disable_all_keys,
    "^^^Current battle: ^team A: {reg10} {s10}^^VS^^ team B: {reg11} {s11}",
    "none",
    [ #(set_background_mesh, "mesh_draw_wild_troll"),
	  (assign, reg10, "$testbattle_team_a_num"),
	  (assign, reg11, "$testbattle_team_b_num"),
	  (str_store_troop_name_by_count, s10, "$testbattle_team_a_troop",reg10),
	  (str_store_troop_name_by_count, s11, "$testbattle_team_b_troop",reg11),
	],
   [
 ]+concatenate_scripts([[
	("tAA",[],"        +5 Team A", [(val_add, "$testbattle_team_a_num", 5),(val_clamp, "$testbattle_team_a_num", 1,101),(jump_to_menu, "mnu_quick_battle_general_test"),]),
	("tAB",[],"        -5 Team A", [(val_sub, "$testbattle_team_a_num", 5),(val_clamp, "$testbattle_team_a_num", 1,101),(jump_to_menu, "mnu_quick_battle_general_test"),]),
	("tAC",[],"        Select Troop A", [
	   (store_troop_faction, "$menu_select_any_troop_search_fac", "$testbattle_team_a_troop"),
	   (troop_get_type, "$menu_select_any_troop_search_race", "$testbattle_team_a_troop"),
	   (assign, "$select_any_troop_nextmenu","mnu_quick_battle_general_test_select_a" ), 
	   (assign, "$select_any_troop_add_selected_troops",0 ), 
	   (jump_to_menu, "mnu_select_any_troop"),
	]),
	#("B",[],"_", []),
	("tBA",[],"        +5 Team B", [(val_add, "$testbattle_team_b_num", 5),(val_clamp, "$testbattle_team_b_num", 1,101),(jump_to_menu, "mnu_quick_battle_general_test"),]),
	("tBB",[],"        -5 Team B", [(val_sub, "$testbattle_team_b_num", 5),(val_clamp, "$testbattle_team_b_num", 1,101),(jump_to_menu, "mnu_quick_battle_general_test"),]),
	("tBC",[],"        Select Troop B", [
	   (store_troop_faction, "$menu_select_any_troop_search_fac", "$testbattle_team_b_troop"),
	   (troop_get_type, "$menu_select_any_troop_search_race", "$testbattle_team_b_troop"),
	   (assign, "$select_any_troop_nextmenu","mnu_quick_battle_general_test_select_b" ), 
	   (assign, "$select_any_troop_add_selected_troops",0 ), 
	   (jump_to_menu, "mnu_select_any_troop"),
	]),
	#("B",[],"_", []),
	("B",[],"         Preset 1", [
	          (assign, "$testbattle_team_b_num", 40),(assign, "$testbattle_team_b_troop", "trp_i2_isen_orc"),
	          (assign, "$testbattle_team_a_num", 10),(assign, "$testbattle_team_a_troop", "trp_i4_gon_swordsman")
	]),
	#("B",[],"_", []),
	("F",[],"          START FIGHT!",
		[(assign, "$g_custom_battle_scenario", 26),(jump_to_menu, "mnu_custom_battle_2"),]),
 ] for ct in range(cheat_switch)])+[
    ("dot_go_back",[],".                 Go back",[(jump_to_menu, "mnu_start_game_3"),]),    ]
 ),
( "quick_battle_general_test_select_a",0,"_","none",[
  (try_begin),(ge, "$select_any_troop_result", 0), (assign, "$testbattle_team_a_troop", "$select_any_troop_result"),(try_end),
  (jump_to_menu, "mnu_quick_battle_general_test"),],[],
 ),
( "quick_battle_general_test_select_b",0,"_","none",[
  (try_begin),(ge, "$select_any_troop_result", 0), (assign, "$testbattle_team_b_troop", "$select_any_troop_result"),(try_end),
  (jump_to_menu, "mnu_quick_battle_general_test"),],[],
 ),


#TLD Troll quick battle choser
( "quick_battle_troll",mnf_disable_all_keys,
    "^^^^^^^^Choose your troll scenario:",
    "none",
    [(set_background_mesh, "mesh_draw_wild_troll"),],
   [
 ]+concatenate_scripts([[ 
	("troll_battle_scenario_10",[],"          Test: Troll VS Infantry",
		[(assign, "$g_custom_battle_scenario", 10),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_17",[],"          Test: Troll VS Weak Infantry",
		[(assign, "$g_custom_battle_scenario", 17),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_18",[],"          Test: Troll VS Elves",
		[(assign, "$g_custom_battle_scenario", 18),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_11",[],"          Test: Troll VS Archers",
		[(assign, "$g_custom_battle_scenario", 11),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_12",[],"          Test: Troll VS Cavalry",
		[(assign, "$g_custom_battle_scenario", 12),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_13",[],"          Test: Troll VS Lancers",
		[(assign, "$g_custom_battle_scenario", 13),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_14",[],"          Test: Troll VS Troll",
		[(assign, "$g_custom_battle_scenario", 14),(jump_to_menu, "mnu_custom_battle_2"),]),
	("troll_battle_scenario_15",[],"          Toy-Test: player controlled Troll",
		[(assign, "$g_custom_battle_scenario", 15),(jump_to_menu, "mnu_custom_battle_2"),]),
 ] for ct in range(cheat_switch)])+[
    ("dot_go_back",[],".                 Go back",[(jump_to_menu, "mnu_start_game_3"),]),    ]
 ),
( "quick_battle_wargs",mnf_disable_all_keys,
    "^^^^^^^^Choose your TEST Warg scenario:",
    "none",
    [(set_background_mesh, "mesh_draw_orc_raiders"),],
   [
 ]+concatenate_scripts([[
	("warg_battle_scenario_10",[],"          Against Wargs: 1 vs 1",
		[(assign, "$g_custom_battle_scenario", 20),(jump_to_menu, "mnu_custom_battle_2"),]),
	("warg_battle_scenario_11",[],"          Against Wargs: 2 vs 3",
		[(assign, "$g_custom_battle_scenario", 21),(jump_to_menu, "mnu_custom_battle_2"),]),
	("warg_battle_scenario_12",[],"          Against Wargs: many vs many",
		[(assign, "$g_custom_battle_scenario", 22),(jump_to_menu, "mnu_custom_battle_2"),]),
	("warg_battle_scenario_10b",[],"          Play Wargs: 1 vs 1",
		[(assign, "$g_custom_battle_scenario", 23),(jump_to_menu, "mnu_custom_battle_2"),]),
	("warg_battle_scenario_11b",[],"          Play Wargs: 2 vs 3",
		[(assign, "$g_custom_battle_scenario", 24),(jump_to_menu, "mnu_custom_battle_2"),]),
	("warg_battle_scenario_12b",[],"          Play Wargs: many vs many",
		[(assign, "$g_custom_battle_scenario", 25),(jump_to_menu, "mnu_custom_battle_2"),]),
 ] for ct in range(cheat_switch)])+[
    ("dot_go_back",[],".                 Go back",[(jump_to_menu, "mnu_start_game_3"),]),    ]
 ),
######################################
#TLD Character creation menus CONTINUE
( "start_good",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Select your race:", "none",[(set_show_messages,0),],[
  ("start_ma",[],"MAN",                 [(jump_to_menu,"mnu_start_good_man"),]),
  ("start_el",[],"ELF",                 [(jump_to_menu,"mnu_start_good_elf"),]),
  ("start_dw",[],"DWARF",               [(jump_to_menu,"mnu_start_good_dwarf"),]),
  ("spacer"  ,[],"_",[]),  
  ("go_back" ,[],"Go back",[(jump_to_menu, "mnu_start_game_1")]),    ]
 ),
( "start_evil",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Whom do you Serve?", "none",[],
 [("start_eye"   ,[],"SAURON of Mordor, the Lord of the Rings",   [(jump_to_menu,"mnu_start_eye"),]),
  ("start_hand"  ,[],"SARUMAN of Isengard, the White Hand",       [(jump_to_menu,"mnu_start_hand"),]),
  ("spacer",[],"_",[]),
  ("go_back"     ,[],"Go back",[(jump_to_menu, "mnu_start_game_1")]),    ]
 ),
( "start_eye",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^Your Master is the Lidless Eye^Choose your Race", "none",[(assign, "$last_menu", "mnu_start_eye")],[
 ("start_or"  ,[],"an ORC, serving the Lidless Eye"       ,[(jump_to_menu,"mnu_start_eye_orc"),]),
 ("start_ur"  ,[],"an URUK, the new breed of Orcs"        ,[(call_script,"script_start_as_one","trp_i1_mordor_uruk_snaga"),  (jump_to_menu,"mnu_start_as_one"),]),
 ("start_em"  ,[],"a MAN, subjugated by Sauron"           ,[(jump_to_menu,"mnu_start_eye_man"),]),
 ("spacer",[],"_",[]),
 ("go_back"     ,[],"Go back",[(jump_to_menu, "mnu_start_evil")]),    ]
 ),
( "start_hand",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^Your Master is the White Hand^Choose your Race", "none",[(assign, "$last_menu", "mnu_start_hand")],[
 ("start_whor",[],"an ORC, serving the White Hand",          [(jump_to_menu,"mnu_start_hand_orc"),]),
 ("start_isur",[],"one of the URUK-HAI, bred in Isengard",           [(call_script,"script_start_as_one","trp_i1_isen_uruk_snaga"),(jump_to_menu,"mnu_start_as_one"),]),
 ("start_duma",[],"a MAN of Dunland, the Western Plains",    [(call_script,"script_start_as_one","trp_i1_dun_wildman"),       (jump_to_menu,"mnu_choose_gender"),]), #(jump_to_menu,"mnu_choose_skill"),]),
 ("spacer",[],"_",[]),
 ("go_back"     ,[],"Go back",[(jump_to_menu, "mnu_start_evil")]),    ]
 ),
( "start_good_man",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Select your people:", "none",[(assign, "$last_menu", "mnu_start_good_man")],[
  ("start_go",[],"GONDOR, the Kingdom of the White Tower",[(jump_to_menu,"mnu_start_gondor"),]),
  ("start_ro",[],"ROHAN, the Horse people"               ,[(call_script,"script_start_as_one","trp_i1_rohan_youth"),           (jump_to_menu,"mnu_choose_gender"),]),
  ("start_du",[],"DUNEDAIN, the ancient dynasty of Men"  ,[(call_script,"script_start_as_one","trp_a1_arnor_scout"),        (jump_to_menu,"mnu_choose_gender"),]),
  ("start_be",[],"BEORNINGS, the Bear people"            ,[(call_script,"script_start_as_one","trp_i1_beorning_man"),     (jump_to_menu,"mnu_choose_gender"),]),
  ("start_da",[],"the northern Kingdom of DALE"          ,[(call_script,"script_start_as_one","trp_i1_dale_militia"),         (jump_to_menu,"mnu_choose_gender"),]),
  ("spacer"  ,[],"_",[]),  
  ("go_back" ,[],"Go back",[
  	#(jump_to_menu, "mnu_start_good")
  	(start_presentation, "prsnt_faction_selection_good"),]),    ]
 ),
( "start_good_elf",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^which Forest do you live in, Elder?", "none",[(assign, "$last_menu", "mnu_start_good_elf")],[
  ("start_ri", [],"RIVENDELL, of Lord Elrond"            ,[(call_script,"script_start_as_one","trp_a1_riv_scout"),      (jump_to_menu,"mnu_choose_gender"),]),
  ("start_lo", [],"LOTHLORIEN, of Lady Galadriel"        ,[(call_script,"script_start_as_one","trp_a1_lorien_scout"),     (jump_to_menu,"mnu_choose_gender"),]),
  ("start_mi", [],"MIRKWOOD, land of the Silvan Elves"   ,[(call_script,"script_start_as_one","trp_a1_greenwood_scout"),      (jump_to_menu,"mnu_choose_gender"),]),
  ("spacer" , [],"_",[]),  
  ("go_back", [],"Go back",[
  	#(jump_to_menu, "mnu_start_good")
  	(start_presentation, "prsnt_faction_selection_good")]),    ]
 ),
( "start_good_dwarf",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Select your Lineage:", "none",[(assign, "$last_menu", "mnu_start_good_dwarf")],[
  ("start_er", [],"a dweller of EREBOR"                  ,[(call_script,"script_start_as_one","trp_i1_dwarf_apprentice"),   (jump_to_menu,"mnu_start_as_one"),]),
  ("start_ih", [],"a miner of the IRON HILLS"            ,[(call_script,"script_start_as_one","trp_i2_iron_hills_miner"),     (jump_to_menu,"mnu_start_as_one"),]),
  ("spacer" , [],"_",[]),  
  ("go_back", [],"Go back",[
  	#(jump_to_menu, "mnu_start_good")
  	(start_presentation, "prsnt_faction_selection_good")]),    ]
 ),
( "start_gondor",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Where are you from, in Gondor?", "none",[(assign, "$last_menu", "mnu_start_gondor")],[
 ("quick_start_gondor"     ,[(eq, cheat_switch, 1),],"[dev: quick start]",[(assign, "$tld_option_cutscenes", 0),(assign, "$tld_option_town_menu_hidden", 0), (call_script,"script_start_as_one","trp_c1_gon_nobleman"), (jump_to_menu,"mnu_start_phase_2" ),]),
 ("start_mt",[],"MINAS TIRITH, the Capital"                    ,[(troop_set_slot, "trp_player", slot_troop_subfaction, subfac_regular),(jump_to_menu,"mnu_start_gondor_mt"),]),
 ("start_ls",[],"LOSSARNACH, the Fiefdom of the Axemen"        ,[(call_script,"script_start_as_one","trp_i1_loss_woodsman"),  (troop_set_slot, "trp_player", slot_troop_subfaction, subfac_lossarnach),  	   (jump_to_menu,"mnu_choose_gender"),]),
 ("start_la",[],"LAMEDON, the Fiefdom of the Mountain Clansmen",[(call_script,"script_start_as_one","trp_i1_lam_clansman"),     (troop_set_slot, "trp_player", slot_troop_subfaction, subfac_ethring),   	   (jump_to_menu,"mnu_choose_gender"),]),
 ("start_pg",[],"PINNATH GELIN, the Fiefdom of Green Hills"    ,[(call_script,"script_start_as_one","trp_i1_pinnath_plainsman"), (troop_set_slot, "trp_player", slot_troop_subfaction, subfac_pinnath_gelin),   (jump_to_menu,"mnu_choose_gender"),]),
 ("start_do",[],"DOL AMROTH, the Fiefdom of Swan Knights"      ,[(call_script,"script_start_as_one","trp_i1_amroth_recruit"),        (troop_set_slot, "trp_player", slot_troop_subfaction, subfac_dol_amroth),	   (jump_to_menu,"mnu_choose_gender"),]),
 ("start_pe",[],"PELARGIR, the Coastal Fiefdom"                ,[(call_script,"script_start_as_one","trp_i1_pel_watchman"), 		(troop_set_slot, "trp_player", slot_troop_subfaction, subfac_pelargir),        (jump_to_menu,"mnu_choose_gender"),]),
 ("start_bl",[],"BLACKROOT VALE, the Fiefdom of Archers"       ,[(call_script,"script_start_as_one","trp_a1_blackroot_hunter"), 	(troop_set_slot, "trp_player", slot_troop_subfaction, subfac_blackroot),	   (jump_to_menu,"mnu_choose_gender"),]),
 ("spacer",[],"_",[]),
 ("go_back"     ,[],"Go back",[
 	#(jump_to_menu, "mnu_start_good")
 	(start_presentation, "prsnt_faction_selection_good")]),    ]
 ),
( "start_eye_man",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Select your people:", "none",[(assign, "$last_menu", "mnu_start_eye_man")],[
 ("quick_start_harad"     ,[(eq, cheat_switch, 1),],"[dev: quick start]",[(assign, "$tld_option_cutscenes", 0),(assign, "$tld_option_town_menu_hidden", 0), (call_script,"script_start_as_one","trp_c2_harondor_scout"), (jump_to_menu,"mnu_start_phase_2" ),]),
 ("start_hr",[],"HARADRIM, the desert people from the South",    [(jump_to_menu,"mnu_start_haradrim"),]),  
 ("start_bn",[],"Black NUMENOREANS, the renegades from the West",[(call_script,"script_start_as_one","trp_i2_mordor_num_renegade"),(jump_to_menu,"mnu_start_numenorean"),]),
 ("start_um",[],"UMBAR, the pirates from the South Seas",        [(call_script,"script_start_as_one","trp_i1_corsair_youth"),            (jump_to_menu,"mnu_choose_gender"),]),
 ("start_rh",[],"RHUN, the barbarians from the East",            [(call_script,"script_start_as_one","trp_i1_rhun_tribesman"),           (jump_to_menu,"mnu_choose_gender"),]),
 ("start_kh",[],"KHAND, the savage people from South-East",      [(call_script,"script_start_as_one","trp_i1_khand_bondsman"),         (jump_to_menu,"mnu_choose_gender"),]),
 ("spacer",[],"_",[]),
 ("go_back",[],"Go back",[
 	#(jump_to_menu, "mnu_start_eye")
 	(start_presentation, "prsnt_faction_selection_eye")]),    ]
 ),

( "start_eye_uruk",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Where do you lurk?", "none",[(assign, "$last_menu", "mnu_start_eye_uruk")],[
 ("quick_start_uruk"     ,[(eq, cheat_switch, 1),],"[dev: quick start]",[(assign, "$tld_option_cutscenes", 0),(assign, "$tld_option_town_menu_hidden", 0), (call_script,"script_start_as_one","trp_i1_mordor_uruk_snaga"), (jump_to_menu,"mnu_start_phase_2" ),]),
 ("start_arm_uruk",[],"in the armies amassed at MORDOR", [(call_script,"script_start_as_one","trp_i1_mordor_uruk_snaga"),   (jump_to_menu,"mnu_start_as_one"),]),
 ("start_cav_uruk",[],"in the caves of DOL GULDUR",      [(call_script,"script_start_as_one","trp_i1_mordor_uruk_snaga"), (call_script, "script_player_join_faction", "fac_guldur"), (jump_to_menu,"mnu_start_as_one"),]),
 ("spacer" ,[],"_"  ,[]),
 ("go_back",[],"Go back",[
 	#(jump_to_menu, "mnu_start_eye")
 	(start_presentation, "prsnt_faction_selection_eye")]),    ]
 ),
( "start_eye_orc",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Where do you lurk?", "none",[(assign, "$last_menu", "mnu_start_eye_orc")],[
 ("quick_start_orc"     ,[(eq, cheat_switch, 1),],"[dev: quick start]",[(assign, "$tld_option_cutscenes", 0),(assign, "$tld_option_town_menu_hidden", 0), (call_script,"script_start_as_one","trp_i1_mordor_orc_snaga"), (jump_to_menu,"mnu_start_phase_2" ),]),
 ("start_arm",[],"in the armies amassed at MORDOR", [(call_script,"script_start_as_one","trp_i1_mordor_orc_snaga"),   (jump_to_menu,"mnu_start_as_one"),]),
 ("start_cav",[],"in the caves of DOL GULDUR",      [(call_script,"script_start_as_one","trp_i1_guldur_orc_snaga"),   (jump_to_menu,"mnu_start_as_one"),]),
 ("spacer" ,[],"_"  ,[]),
 ("go_back",[],"Go back",[
 	#(jump_to_menu, "mnu_start_eye")
 	(start_presentation, "prsnt_faction_selection_eye")]),    ]
 ),
( "start_hand_orc",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Where do you lurk?", "none",[(assign, "$last_menu", "mnu_start_hand_orc")],[
 ("quick_start_moria"     ,[(eq, cheat_switch, 1),],"[dev: quick start Moria]",[(assign, "$tld_option_cutscenes", 0),(assign, "$tld_option_town_menu_hidden", 0), (call_script,"script_start_as_one","trp_i1_moria_snaga"), (jump_to_menu,"mnu_start_phase_2" ),]),
 ("start_armis",[],"in the Armies amassed at ISENGARD",[(call_script,"script_start_as_one","trp_i1_isen_orc_snaga"),(jump_to_menu,"mnu_start_as_one"),]),
 ("start_minmo",[],"in the Mines of MORIA"            ,[(call_script,"script_start_as_one","trp_i1_moria_snaga"),       (jump_to_menu,"mnu_start_as_one"),]),
 ("start_cliff",[],"in the cliffs of Mount GUNDABAD",  [(call_script,"script_start_as_one","trp_i1_gunda_goblin"),      (jump_to_menu,"mnu_start_as_one"),]),
 ("spacer" ,[],"_",[]),
 ("go_back",[],"Go back",[
 	#(jump_to_menu, "mnu_start_hand")
 	(start_presentation, "prsnt_faction_selection_hand")]),    ]
 ),
( "start_gondor_mt",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Select your Lineage", "none",[(assign, "$last_menu", "mnu_start_gondor_mt")],[
 ("start_1_com",[],"Commoner" ,[(call_script,"script_start_as_one","trp_i1_gon_levy"),(jump_to_menu,"mnu_choose_gender"),]),
 ("start_2_hib",[],"High-born",[(call_script,"script_start_as_one","trp_c1_gon_nobleman"),(jump_to_menu,"mnu_choose_gender"),]),
 ("spacer" ,[],"_"        ,[]),
 ("go_back",[],"Go back"  ,[(jump_to_menu, "mnu_start_gondor")]),    ]
 ),
( "start_haradrim",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^You are one of the Haradrim,^a Man of the Desert.^Select your line", "none",[(assign, "$last_menu", "mnu_start_haradrim")],[
 ("start_1_des",[],"Desert Man",                          [(call_script,"script_start_as_one","trp_i1_harad_levy"),   (jump_to_menu,"mnu_choose_gender"),]),
 ("start_2_far",[],"Far Harad Tribesman",                 [(call_script,"script_start_as_one","trp_i2_far_harad_tribesman"),    (jump_to_menu,"mnu_choose_gender"),]),
# ("start_3",[],"Harondor Noble",                      [(call_script,"script_start_as_one","trp_c2_harondor_scout"),(jump_to_menu,"mnu_choose_gender"),]),
 ("spacer",[],"_",[]),
 ("go_back",[],"Go back",[(jump_to_menu, "mnu_start_eye_man")]),    ]
 ),

( "start_numenorean",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^You are a Black Numenorean,^faithful to the Darkness and Morgoth.^Select where you serve the Eye", "none",[(assign, "$last_menu", "mnu_start_numenorean")],[
 ("start_1_bn",[],"Next to the Mouth of Sauron, in MORANNON",		[(jump_to_menu,"mnu_choose_gender"),]),
 ("start_2_bn",[],"In the Fortress of the Necromancer, DOL GULDUR", [(call_script, "script_player_join_faction", "fac_guldur"), (jump_to_menu,"mnu_choose_gender"),]),
 ("spacer",[],"_",[]),
 ("go_back",[],"Go back",[(jump_to_menu, "mnu_start_eye_man")]),    ]
 ),


( "choose_gender",menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "^^^^^^^^^^Your gender?", "none",[],
 [("start_male"  ,[],"Male"   ,[#(assign,"$character_gender",tf_male  ),
    (jump_to_menu,"mnu_start_as_one"),]),
  ("start_female",[],"Female" ,[
    (troop_set_type,"trp_player",tf_female), # override race for females elves and mans
    #(assign,"$character_gender",tf_female), no need
    (jump_to_menu,"mnu_start_as_one"),
  ]),
  ("spacer",[],"_",[]),

  ("go_back"     ,[],"Go back",[(troop_clear_inventory, "trp_player"),
    (try_begin),
    	(eq, "$intro_presentation_stage", 33),
    	(start_presentation, "prsnt_faction_selection_hand"),
    (else_try),
    	(jump_to_menu,"$last_menu"),
    (try_end),]),    ]
 ),
( "choose_skill",mnf_disable_all_keys|menu_text_color(0xFF0000FF),
 "^^^^^^^^FOR DEVS:^*normally*, at this point^you would go to edit skills^and then face...","none",[
	 (jump_to_menu, "mnu_auto_return"), # comment this line to let devs skip skill/face editing
	],
	[ ("skip",[],"SKIP THAT: let me playtest now",[(jump_to_menu, "mnu_start_phase_2"),]),
	  ("proc",[],"Proceed as normal",[(jump_to_menu, "mnu_auto_return"),])]
 ),

##Kham Menu to Allow Easy Start 

("start_as_one",0, "^^^^^^^^^^What type of Soldier are you?","none", 

	[

		] + (is_a_wb_menu==1 and [

		# swy-- at this point should be safe to set the correct good/evil UI skin on Warband; keep in mind that $players_kingdom
		#       gets first set when script_player_join_faction gets called by script_start_as_one in one of the previous menus.
		(call_script, "script_tld_internal_set_good_or_evil_ui"),

		] or []) + [
		
		(assign, reg55, 0),
		(try_begin),
			(eq, "$players_kingdom", "fac_guldur"),
			(assign, reg55, 1),
		(try_end),

		(str_store_troop_name, s23, "$player_current_troop_type"),
		(troop_get_upgrade_troop,reg0,"$player_current_troop_type",0),
		(troop_get_upgrade_troop, reg1,"$player_current_troop_type",1),
		(gt,reg0,0),
		(str_store_troop_name,s21,reg0),
		(gt,reg1,0),
		(str_store_troop_name,s22,reg1),

	],
	    
    [
     ("quick_default"     ,[(eq, cheat_switch, 1),],"[dev: quick start]",[(assign, "$tld_option_cutscenes", 0),(assign, "$tld_option_town_menu_hidden", 0), (jump_to_menu,"mnu_start_phase_2" ),]),
	 ("start_default",[], "Become a {s23} (Default)", [(troop_add_proficiency_points, "trp_player", 10),(jump_to_menu, "mnu_choose_skill")]),
     ("start_up1", [(gt,reg0,0)], "Become a {s21} (Easy)", [(call_script, "script_start_as_one", reg0),(troop_add_proficiency_points, "trp_player", 15), (try_begin), (eq, reg55, 1), (call_script, "script_player_join_faction", "fac_guldur"), (try_end), (jump_to_menu, "mnu_choose_skill")]),
     ("start_up2", [(gt,reg1,0)], "Become a {s22} (Easy)", [(call_script, "script_start_as_one", reg1),(troop_add_proficiency_points, "trp_player", 15), (try_begin), (eq, reg55, 1), (call_script, "script_player_join_faction", "fac_guldur"), (try_end), (jump_to_menu, "mnu_choose_skill")]),
     ("spacer",[],"_",[]), 
     ("go_back"     ,[],"Go back",[(troop_clear_inventory, "trp_player"), (try_for_range, ":i", 0,6), (troop_raise_proficiency, "trp_player", ":i", -10),(try_end),
     	(try_begin), (eq, "$intro_presentation_stage", 33), (start_presentation, "prsnt_faction_selection_hand"),(else_try),
     	(eq, "$intro_presentation_stage", 3), (start_presentation, "prsnt_faction_selection_eye"), (else_try), 
     	(jump_to_menu,"$last_menu"),(try_end)]),
  ]),


############################################### 
( "auto_return",0,
    "This menu automatically returns to caller.",
    "none",
    [(change_screen_return, 0)],[]
 ),

( "morale_report",0,
   "^^{s1}",
   "none",
   [(set_background_mesh, "mesh_ui_default_menu_window"),
    (call_script, "script_get_player_party_morale_values"),
    (assign, ":target_morale", reg0),
    (assign, reg1, "$g_player_party_morale_modifier_party_size"),
    (try_begin),(gt, reg1, 0),(str_store_string, s2, "@ -"),
     (else_try),              (str_store_string, s2, "@ "),
    (try_end),

    (assign, reg2, "$g_player_party_morale_modifier_leadership"),
    (try_begin),(gt, reg2, 0),(str_store_string, s3, "@ +"),
     (else_try),              (str_store_string, s3, "@ "),
    (try_end),

    (try_begin),
      (gt, "$g_player_party_morale_modifier_no_food", 0),
      (assign, reg7, "$g_player_party_morale_modifier_no_food"),
      (str_store_string, s5, "@^No food:  -{reg7}"),
    (else_try),
      (str_store_string, s5, "@ "),
    (try_end),
    (assign, reg3, "$g_player_party_morale_modifier_food"),
    (try_begin),(gt, reg3, 0),(str_store_string, s4, "@ +"),
     (else_try),              (str_store_string, s4, "@ "),
    (try_end),
    
    # TLD morale-boosting items (non-cumulative)
    (assign, reg6, 0),
    (str_store_string, s6, "@ "),
    (try_begin),
        (player_has_item, "itm_lembas"),
        (assign, reg6, 30),
        (str_store_string, s6, "@ +"),
    (else_try),
        (player_has_item, "itm_cooking_cauldron"),
        (assign, reg6, 20),
        (str_store_string, s6, "@ +"),
    (try_end),

    (party_get_morale, reg5, "p_main_party"),
    (store_sub, reg4, reg5, ":target_morale"),
    (try_begin),(gt, reg4, 0),(str_store_string, s7, "@ +"),
     (else_try),              (str_store_string, s7, "@ "),
    (try_end),
    (str_store_string, s1, "@Current party morale is {reg5}.^Current party morale modifiers are:^^Base morale:  +50^Party size: {s2}{reg1}^Leadership: {s3}{reg2}^Food variety: {s4}{reg3}{s5}^Special items: {s6}{reg6}^Recent events: {s7}{reg4}^TOTAL:  {reg5}"),
    ],
    [("continue",[],"Continue...",[(jump_to_menu, "mnu_reports")])]
 ),
( "faction_orders",0,
   "{s9}", "none",
   [ 
     (set_background_mesh, "mesh_ui_default_menu_window"),
     (str_clear, s9),
     (store_current_hours, ":cur_hours"),
     (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
       (neq, ":faction_no", "fac_player_supporters_faction"),
       (faction_get_slot, ":faction_ai_state", ":faction_no", slot_faction_ai_state),
       (faction_get_slot, ":faction_ai_object", ":faction_no", slot_faction_ai_object),
       (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
       (faction_get_slot, ":faction_ai_last_offensive_time", ":faction_no", slot_faction_ai_last_offensive_time),
       (faction_get_slot, ":faction_ai_offensive_max_followers", ":faction_no", slot_faction_ai_offensive_max_followers),
       (str_store_faction_name, s10, ":faction_no"),
       (store_sub, reg1, ":cur_hours", ":faction_ai_last_offensive_time"),
       (assign, reg2, ":faction_ai_offensive_max_followers"),
       (try_begin),
         (eq, ":faction_ai_state", sfai_default),
         (str_store_string, s11, "@Defending"),
       (else_try),
         (eq, ":faction_ai_state", sfai_gathering_army),
         (str_store_string, s11, "@Gathering army"),
       (else_try),
         (eq, ":faction_ai_state", sfai_attacking_center),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@Besieging {s11}"),
       (else_try),
         (eq, ":faction_ai_state", sfai_raiding_village),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@Raiding {s11}"),
       (else_try),
         (eq, ":faction_ai_state", sfai_attacking_enemy_army),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@Attacking enemies around {s11}"),
       (try_end),
       (str_store_faction_name, s10, ":faction_no"),
       (try_begin),
         (lt, ":faction_marshall", 0),
         (str_store_string, s12, "@No one"),
       (else_try),
         (str_store_troop_name, s12, ":faction_marshall"),
       (try_end),
       (str_store_string, s9, "@{s9}{s10}^Current state: {s11}^Marshall: {s12}^Since the last offensive: {reg1} hours^Offensive maximum followers: {reg2}^^"),
     (try_end),
     (try_begin),
       (neg|is_between, "$g_cheat_selected_faction", kingdoms_begin, kingdoms_end),
       (call_script, "script_get_next_active_kingdom", kingdoms_end),
       (assign, "$g_cheat_selected_faction", reg0),
     (try_end),
     (str_store_faction_name, s10, "$g_cheat_selected_faction"),
     (str_store_string, s9, "@Selected faction is: {s10}^^{s9}"),
    ],
    [ 
 ]+concatenate_scripts([[	
	("faction_orders_next_faction", [],"Select next faction.",
       [ (call_script, "script_get_next_active_kingdom", "$g_cheat_selected_faction"),
         (assign, "$g_cheat_selected_faction", reg0),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
      ("faction_orders_defend", [],"Force defend.",
       [ (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_state, sfai_default),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_object, -1),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
      ("faction_orders_gather", [],"Force gather army.",
       [ (store_current_hours, ":cur_hours"),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_state, sfai_gathering_army),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_last_offensive_time, ":cur_hours"),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_offensive_max_followers, 1),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_object, -1),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
      ("faction_orders_increase_time", [],"Increase last offensive time by 24 hours.",
       [ (faction_get_slot, ":faction_ai_last_offensive_time", "$g_cheat_selected_faction", slot_faction_ai_last_offensive_time),
         (val_sub, ":faction_ai_last_offensive_time", 24),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_last_offensive_time, ":faction_ai_last_offensive_time"),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
      ("faction_orders_rethink", [],"Force rethink.",
       [ (call_script, "script_init_ai_calculation"),
         (call_script, "script_decide_faction_ai", "$g_cheat_selected_faction"),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
      ("faction_orders_rethink_all", [],"Force rethink for all factions.",
       [ (call_script, "script_recalculate_ais"),
         (jump_to_menu, "mnu_faction_orders"),
        ]),
 ] for ct in range(cheat_switch)])+[
      ("go_back_dot",[],"Go back.",[(jump_to_menu, "mnu_reports"),]),
    ]
 ),
( "character_report",0,
   "^^^^^Party Morale: {reg8}^Party Size Limit: {reg7}^{s5}",
#   "^^^^^Character Renown: {reg5}^Honor Rating: {reg6}^Party Morale: {reg8}^Party Size Limit: {reg7}^{s5}",
   "none",
   [(set_background_mesh, "mesh_ui_default_menu_window"),

    (call_script, "script_game_get_party_companion_limit"),
    (assign, ":party_size_limit", reg0),
    (assign, reg7, ":party_size_limit"),
    (party_get_morale, reg8, "p_main_party"),
	# CppCoder: Injury Report. Feel free to edit/remove/improve. :)
	(eq, 0, 0), # on / off toggle
	(assign, ":str_reg", s1), 
	(assign, ":wounds", 0), #count # of wounds
	(assign, ":wound_mask", 0), #count # of wounds
	(troop_get_slot, ":wound_mask", "trp_player", slot_troop_wound_mask),
	(try_begin),(store_and,":x",":wound_mask",wound_head ),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_head"),(val_add, ":str_reg", 1),(try_end),
	(try_begin),(store_and,":x",":wound_mask",wound_chest),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_chest"),(val_add, ":str_reg", 1),(try_end),
	(try_begin),(store_and,":x",":wound_mask",wound_arm  ),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_arm"),(val_add, ":str_reg", 1),(try_end),
	(try_begin),(store_and,":x",":wound_mask",wound_leg  ),(neq,":x",0),(val_add,":wounds",1),(str_store_string, ":str_reg", "str_wound_leg"),(val_add, ":str_reg", 1),(try_end),
	(str_store_string, s5, "@You are in perfect health."),
        (try_begin),
		(eq, ":wounds", 1),
		(str_store_string, s5, "@You are suffering from {s1}."),
	(else_try),
		(eq, ":wounds", 2),
		(str_store_string, s5, "@You are suffering from {s1} and {s2}."),
	(else_try),
		(eq, ":wounds", 3),
		(str_store_string, s5, "@You are suffering from {s1}, {s2}, and {s3}."),
	(else_try),
		(eq, ":wounds", 4),
		(str_store_string, s5, "@You are suffering from {s1}, {s2}, {s3} and {s4}."),
	(else_try),
		(str_store_string, s5, "@You are in perfect health."),
	(try_end),
   ],
   [("continue",[],"Continue...",[(jump_to_menu, "mnu_reports"),]),]
 ),
( "upkeep_report", 0,
 "{s12}", "none",[ (set_background_mesh, "mesh_ui_default_menu_window"),
    (assign, reg5, 0),
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (neq, ":faction_no", "fac_player_supporters_faction"),
  	  (call_script, "script_compute_wage_per_faction", ":faction_no"),
	  (val_add, reg5, reg4),
    (try_end),
    
    (try_begin),
      (gt,reg5,0),
      (str_store_string, s12, "@Weekly upkeep for troops:^{reg5} Resource Points^"),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (call_script, "script_compute_wage_per_faction", ":faction_no"),
        (gt, reg4, 0),
        (str_store_faction_name, s4, ":faction_no"),
        (faction_get_slot, reg5, ":faction_no", slot_faction_respoint),
        (str_store_string, s12, "@{s12}^  {s4}: {reg4} Resource points ({reg5})"),
      (try_end),
	(else_try),
	  (str_store_string, s12, "@No upkeep costs"),
    (try_end),
   ],
   [("continue",[],"Continue...",[(jump_to_menu, "mnu_reports")])]
 ),
( "party_size_report",0,
   "^^^^{s1}", "none",
   [(set_background_mesh, "mesh_ui_default_menu_window"),
    (call_script, "script_game_get_party_companion_limit"),
    (assign, ":party_size_limit", reg0),

    (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
    (val_mul, ":leadership", 5),
    (store_attribute_level, ":charisma", "trp_player", ca_charisma),

    (assign, ":ranks", 0),
    (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
      (call_script, "script_get_faction_rank", ":faction"),
      (val_add, ":ranks", reg0),
      (try_begin),
		(eq, ":faction", "$players_kingdom"),
        (val_add, ":ranks", reg0), # double for home faction
      (try_end),
    (try_end),

    (try_begin),(gt, ":leadership", 0),(str_store_string, s2, "@ +"),
     (else_try),                       (str_store_string, s2, "@ "),
    (try_end),
    (try_begin),(gt, ":charisma", 0),(str_store_string, s3, "@ +"),
     (else_try),                     (str_store_string, s3, "@ "),
    (try_end),
    (try_begin),(gt, ":ranks", 0),(str_store_string, s4, "@ +"),
     (else_try),                   (str_store_string, s4, "@ "),
    (try_end),
    (assign, reg5, ":party_size_limit"),
    (assign, reg1, ":leadership"),
    (assign, reg2, ":charisma"),
    (assign, reg3, ":ranks"),
    (str_clear, s5),
    (try_begin),
      (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
      (str_store_string, s5, "@Orc hiring bonus: +2/3 for each orc^"),
    (try_end),
    (str_store_string, s1, "@Current party size limit is {reg5}.^Current party size modifiers are:^^Base size:  +10^Leadership: {s2}{reg1}^Charisma: {s3}{reg2}^Ranks: {s4}{reg3}^{s5}TOTAL:  {reg5}"),
#    (str_store_string, s1, "@Current party size limit is {reg5}.^Current party size modifiers are:^^Base size:  +10^Leadership: {s2}{reg1}^Charisma: {s3}{reg2}^TOTAL:  {reg5}"),
#    (str_store_string, s1, "@Current party size limit is {reg5}.^Current party size modifiers are:^^Base size:  +10^Leadership: {s2}{reg1}^Charisma: {s3}{reg2}^Renown: {s4}{reg3}^TOTAL:  {reg5}"),
    ],
    [("continue",[],"Continue...",[(jump_to_menu, "mnu_reports"),]),]
 ),
( "faction_strengths_report",0,
   "{s1}",
   "none",
   [(set_background_mesh, "mesh_ui_default_menu_window"),
    (str_clear, s2),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (neq, ":cur_kingdom", "fac_player_supporters_faction"),
      (call_script, "script_faction_strength_string_to_s23", ":cur_kingdom"),
      (str_store_faction_name, s4, ":cur_kingdom"),
      (faction_get_slot, reg1, ":cur_kingdom", slot_faction_strength),
      (str_store_string, s2, "@{s2}^_________{s4}: {reg1} ({s23})"),
    (try_end),
    (str_store_string, s1, "@_________Faction strengths report:^{s2}"),
    (assign, reg1, "$g_fac_str_siegable"),
    (str_store_string, s1, "@{s1}^^Factions are normally sieged when below {reg1} strength."),
    ],
    [("continue",[],"Continue...", [(jump_to_menu, "mnu_reports")])]
 ),
# ( "faction_relations_report",0,
   # "{s1}",
   # "none",
   # [(str_clear, s2),
    # (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      # (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      # (neq, ":cur_kingdom", "fac_player_supporters_faction"),
      # (store_relation, ":cur_relation", "fac_player_supporters_faction", ":cur_kingdom"),
      # (try_begin),(ge, ":cur_relation", 90),(str_store_string, s3, "@Loyal"),
      # (else_try), (ge, ":cur_relation", 80),(str_store_string, s3, "@Devoted"),
      # (else_try), (ge, ":cur_relation", 70),(str_store_string, s3, "@Fond"),
      # (else_try), (ge, ":cur_relation", 60),(str_store_string, s3, "@Gracious"),
      # (else_try), (ge, ":cur_relation", 50),(str_store_string, s3, "@Friendly"),
      # (else_try), (ge, ":cur_relation", 40),(str_store_string, s3, "@Supportive"),
      # (else_try), (ge, ":cur_relation", 30),(str_store_string, s3, "@Favorable"),
      # (else_try), (ge, ":cur_relation", 20),(str_store_string, s3, "@Cooperative"),
      # (else_try), (ge, ":cur_relation", 10),(str_store_string, s3, "@Accepting"),
      # (else_try), (ge, ":cur_relation", 0 ),(str_store_string, s3, "@Indifferent"),
      # (else_try), (ge, ":cur_relation",-10),(str_store_string, s3, "@Suspicious"),
      # (else_try), (ge, ":cur_relation",-20),(str_store_string, s3, "@Grumbling"),
      # (else_try), (ge, ":cur_relation",-30),(str_store_string, s3, "@Hostile"),
      # (else_try), (ge, ":cur_relation",-40),(str_store_string, s3, "@Resentful"),
      # (else_try), (ge, ":cur_relation",-50),(str_store_string, s3, "@Angry"),
      # (else_try), (ge, ":cur_relation",-60),(str_store_string, s3, "@Hateful"),
      # (else_try), (ge, ":cur_relation",-70),(str_store_string, s3, "@Revengeful"),
      # (else_try),                           (str_store_string, s3, "@Vengeful"),
      # (try_end),
      # (str_store_faction_name, s4, ":cur_kingdom"),
      # (assign, reg1, ":cur_relation"),
      # (str_store_string, s2, "@{s2}^{s4}: {reg1} ({s3})"),
    # (try_end),
    # (str_store_string, s1, "@Your relation with the factions are:^{s2}"),
    # ],
    # [("continue",[],"Continue...", [(jump_to_menu, "mnu_reports"),]),
    # ]
 # ),
( "traits_report",0,
   "{s1}",
   "none",
   [(set_background_mesh, "mesh_ui_default_menu_window"),
    (str_clear, s2),
    (try_for_range, ":trait", slot_trait_first, slot_trait_last+1),
      (troop_slot_eq, "trp_traits", ":trait", 1),
      
      # Title string = First title string + 2*(slot-1)
      (store_sub, ":title_string", ":trait", 1),
      (val_add, ":title_string", ":title_string"),
      (val_add, ":title_string", tld_first_trait_string),
      (str_store_string, s5, ":title_string"),
      (try_begin),
      	(eq, ":trait", slot_trait_bravery),
      	(neq|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
      	(str_store_string, s5, "@Savagery"),
      (try_end),
      (val_add, ":title_string", 1),
      (str_store_string, s6, ":title_string"), #description string
    
      (str_store_string, s2, "@{s2}^^{s5}^{s6}"),
    (try_end),
    (str_store_string, s1, "@Traits gained:^{s2}"),
    ],
    [("continue",[],"Continue...", [(jump_to_menu, "mnu_reports")])]
 ),

( "camp",0,
   "^^^^You are in {s1}.{s2}^^What do you want to do?",
   "none",
	[ (assign, "$g_player_icon_state", pis_normal),
	  (call_script,"script_maybe_relocate_player_from_z0"),
	  #(party_get_current_terrain, reg78,"p_main_party"),
	  #(display_message, "@current terrain: {reg78}"),

	  #(assign, reg0, "$current_player_landmark",), (display_message, "@DEBUG: LANDMARK ID {reg0}"),
	  
	  (str_clear, s2),
	  (try_begin), 
		(call_script, "script_cf_store_landmark_description_in_s17", "$current_player_landmark"),
		(str_store_string,s2,"@^^You are {s17}."), 
	  (try_end),
	  
	  (store_add, reg2, "$current_player_region", str_fullname_region_begin),
	  (str_store_string,s1,reg2),
	  (set_background_mesh, "mesh_ui_default_menu_window"),
    ],[
		("camp_scene"      ,[],"Walk around."  ,[
			(assign, "$number_of_combatants", 1), # use a scene as if a battle with one combatant...
			(call_script, "script_jump_to_random_scene", "$current_player_region", "$current_player_terrain",  "$current_player_landmark"), 
			#    (jump_to_scene, "scn_camp_scene"),
			(change_screen_mission)]),
		("camp_troop"      ,[
		    (party_get_num_companions,reg10,"p_main_party"),(val_sub,reg10,1),
		    (party_get_num_prisoners,reg11,"p_main_party"),
              	    (party_count_prisoners_of_type, ":troll_count", "p_main_party", "trp_moria_troll"),(val_sub,reg11,":troll_count"),
              	    (party_count_prisoners_of_type, ":troll_count", "p_main_party", "trp_isen_armored_troll"),(val_sub,reg11,":troll_count"),
              	    (party_count_prisoners_of_type, ":troll_count", "p_main_party", "trp_mordor_olog_hai"),(val_sub,reg11,":troll_count"),
		    (this_or_next|gt,reg10,0),(gt,reg11,0),
			(store_mul, reg12, reg10,reg11),
		],"Review{reg10?_troops:}{reg12?_and:}{reg11?_prisoners:}."  ,[
			(assign, "$number_of_combatants", 1), # use a scene as if a battle with one combatant...
			(call_script, "script_jump_to_random_scene", "$current_player_region", "$current_player_terrain",  "$current_player_landmark"), 
			#    (jump_to_scene, "scn_camp_scene"),
			(set_jump_mission,"mt_review_troops"),
			(change_screen_mission)]),
		("camp_action"     ,[],"Use an object."    ,[(jump_to_menu, "mnu_camp_action")]),

  #TLD - modified rest menu, added chance of being attacked by assasins (Kolba)
		("camp_wait_here",[],"Camp here for some time.",
      [		(store_random_in_range,":r",0,10),#random number
			(try_begin),
				(gt,":r",10),#NEVER! 10% of time we are attacked
				#clearing temporary slots
				(try_for_range,":slot",0,10),
					(troop_set_slot,"trp_temp_array_a",":slot",-1),
				(try_end),
				
				(assign,":slot",0),
				(try_for_range,":faction",kingdoms_begin,kingdoms_end),
					(faction_slot_eq,":faction",slot_faction_state,sfs_active),
					(neq,":faction","fac_player_supporters_faction"),
					(store_relation,":relation",":faction","fac_player_faction"),
					(lt,":relation",0),
					(troop_set_slot,"trp_temp_array_a",":slot",":faction"),#save enemy faction to slot
					(val_add,":slot",1),#continue to next slot
				(try_end),
				
				(gt,":slot",0),#if there are no enemy factions, we are simply sleeping
				(store_random_in_range,":faction_slot",0,":slot"),#choose random slot of enemy faction
				(troop_get_slot,":faction","trp_temp_array_a",":faction_slot"),#get faction number from slot
				
				(troop_set_slot,"trp_temp_array_a",0,":faction"),#saves faction (to use it later, in the battle)
          
				#(call_script, "script_asasins_ambush_setup"), # set scene, it's exported to rego0
				(assign,":scene",scn_khand_camp_center),#save scene to variable
				(modify_visitors_at_site,":scene"),
				(reset_visitors),
				(set_visitor,0,"trp_player"),
				
				(faction_get_slot,":troop",":faction",slot_faction_tier_2_troop),# get troop from faction, you can set other tier
				(try_begin),
					(le,":troop",0),#if there are any problems with troop, it's set to normal bandit
					(assign,":troop","trp_bandit"),
				(try_end),
				(set_visitors,1,":troop",5),
                
                (display_message, "@Assassins in the camp, defend yourself!", 0xFF0000),

				(set_jump_mission,"mt_assasins_attack"), #jump to mission template
				(jump_to_scene,":scene"), #jump to scene
				(change_screen_mission), #run mission
			(else_try),
				(assign,"$g_camp_mode", 1),
				#(assign, "$g_infinite_camping", 0),
				(assign, "$g_player_icon_state", pis_camping),
				(rest_for_hours_interactive, 24 * 365, 5, 1), #rest while attackable
				(change_screen_return),
			(try_end), #end trying
	]),

   	] + (is_a_wb_menu==1 and [
	("camp_options",[],"Change TLD options.",[(start_presentation, "prsnt_tld_mod_options")]),
	] or [
	("camp_options",[],"Change TLD options.",[(jump_to_menu, "mnu_game_options")]),
	]) + [

    #Kham - Removed Compile Dependence for Cheat Menu

 	("spacer_dev_menu"    ,[],"_"  ,[]),
 	("Dev_Menu", [], "Developer Menu", [(jump_to_menu, "mnu_dev_menu")]),
    ("resume_travelling",[],"Resume travelling.",[(change_screen_return)]),
    ]
 ),
  
## Dev Menu Begin

("dev_menu", 0,
	"These are Development Options that gives you alot of cheats/tools to play with.^^ However, this will result in some WIP events, triggers, campaign changes that could be game breaking.^^ Use at your own risk! ^^ Also, when reporting bugs, please tell us that you are using the Dev Menu.",
	"none", [(set_background_mesh, "mesh_ui_default_menu_window"),],
  [
  #SW - added enable/disable camp cheat menu by ConstantA - http://forums.taleworlds.net/index.php/topic,63142.msg1647442.html#msg1647442
	 ("Cheat_enable",[(eq,"$cheat_mode",0)],"Enable cheat/modding options.",[(assign, "$cheat_mode", 1),(jump_to_menu, "mnu_camp")]),
     ("camp_cheat_option", [(eq,"$cheat_mode",1)] ,"Cheats  (for development use).",[(jump_to_menu, "mnu_camp_cheat")]),
  ## MadVader test begin
     ("camp_test_madvader",[],"MV Test Menu",[(jump_to_menu, "mnu_camp_mvtest")]),
  ## MadVader test end
     ("camp_test_cppcoder",[],"Cpp Test Menu",[(jump_to_menu, "mnu_camp_cctest")]),
  ## Kham Test begin
  	 ("camp_test_kham",[(eq, cheat_switch, 1)],"Kham Test Menu",[(jump_to_menu, "mnu_camp_khamtest")]),

  	 ("camp_back_camp_menu",[],"Back to Camp Menu.",[(jump_to_menu, "mnu_camp")]),
 ]
),

## CppCoder test begin
( "camp_cctest",0,
   "Hurry up and pick something already.",
   "none", [],
  [
     	("camp_cctest_injure",[],"Injure Me",[(call_script,"script_injury_routine", "trp_player")]),

	("camp_cctest_injure_party_heroes", [], "Injure Companions",
	[
		(try_for_range, ":npc", companions_begin, companions_end),
    		(main_party_has_troop, ":npc"),
			(call_script,"script_injury_routine", ":npc"),
    	(try_end),
		(try_for_range, ":npc", new_companions_begin, new_companions_end),
    		(main_party_has_troop, ":npc"),
			(call_script,"script_injury_routine", ":npc"),
    	(try_end),
	]),

    	("camp_cctest_heal",[],"Heal my Injuries. (Does not fix prof. or attributes.)",[(troop_set_slot, "trp_player", slot_troop_wound_mask, 0)]),

     	("camp_cctest_kill_lord",[],"Kill a Random Lord",
	[
		(store_random_in_range, ":cur_troop_id", "trp_knight_1_1", kingdom_heroes_end), #kings and marshals cannot die for now
		(call_script, "script_hero_leader_killed_abstractly", ":cur_troop_id","p_main_party")
	]),

     	("camp_cctest_rout_ally",[],"Add troops to routed allies",
	[
		(store_random_in_range, ":troop_no", "trp_c1_gon_nobleman", "trp_steward_guard"),
		(party_add_members, "p_routed_allies", ":troop_no", 1),
    		(party_get_num_companions, reg1, "p_routed_allies"),
		(display_message, "@Ally party size: {reg1}", color_good_news),
	]),

     	("camp_cctest_rout_enemy",[],"Add troops to routed enemies",
	[
		(store_random_in_range, ":troop_no", "trp_i1_mordor_orc_snaga", "trp_c3_moria_wolf_rider"),
		(party_add_members, "p_routed_enemies", ":troop_no", 1),
    		(party_get_num_companions, reg1, "p_routed_enemies"),
		(display_message, "@Enemy party size: {reg1}", color_bad_news),
	]),

     	("camp_cctest_rout_spawn",[],"Spawn routed parties",
	[
		(assign, "$g_spawn_allies_routed", 1),
		(assign, "$g_spawn_enemies_routed", 1),
		(call_script,"script_cf_spawn_routed_parties"),
		(display_message, "@Spawned routed parties!", color_good_news),
	]),		
	

     	("camp_cctest_gain_traits",[],"Get All Traits",
	[
		(try_for_range, ":trait", slot_trait_first, slot_trait_last+1),
			(call_script, "script_gain_trait", ":trait"),
		(try_end),
	]),

     	("camp_cctest_parties",[],"Count Parties",
	[
		(assign, reg0, 0),
		(try_for_parties, ":unused"),
			(val_add, reg0, 1),
		(try_end),
		(display_message, "@Party count: {reg0}"),
	]),

     	("camp_cctest_items",[],"Refactionize Items",[(call_script, "script_set_item_faction")]),
     	("camp_cctest_pos",[],"Print Coords x100",
	[
		(set_fixed_point_multiplier, 100),
		(party_get_position, pos13, "p_main_party"),
       		(position_get_x, reg2, pos13),
      		(position_get_y, reg3, pos13),
      		(display_message, "@Party position ({reg2},{reg3}).", 0x30FFC8),
	]),

    ("party_add_xp",[], "Add 1000000 XP to Party", 
    	[(party_add_xp, "p_main_party", 1000000), (display_message, "@XP added", color_good_news),
	]),
#     	("camp_cctest_defiled",[],"Add WIP Items",
#	[
#		(troop_add_item, "trp_player","itm_defiled_armor_gondor"),
#		(troop_add_item, "trp_player","itm_defiled_armor_rohan"),
#		(troop_add_item, "trp_player","itm_defiled_armor_dale"),
#		(troop_add_item, "trp_player","itm_gon_leader_surcoat_cloak"),
#	]),

     ("camp_cctest_return",[],"Back to dev menu.",[(jump_to_menu, "mnu_dev_menu")]),
  ]
),

## MadVader test begin
( "camp_mvtest",0,
   "What do you want to test today?",
   "none", [],
  [
 
  ("camp_mvtest_pimp",[],"Pimp me up first!",
    [(troop_raise_attribute, "trp_player",ca_strength,20),
     (troop_raise_attribute, "trp_player",ca_agility,20),
     (troop_raise_attribute, "trp_player",ca_intelligence,20),
     (troop_raise_attribute, "trp_player",ca_charisma,20),
     (troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, 500),
     (troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, 500),
     (troop_raise_proficiency_linear, "trp_player", wpt_polearm, 500),
     (troop_raise_proficiency_linear, "trp_player", wpt_archery, 500),
     (troop_raise_proficiency_linear, "trp_player", wpt_crossbow, 500),
     (troop_raise_proficiency_linear, "trp_player", wpt_throwing, 500),
     (troop_raise_skill, "trp_player",skl_ironflesh,10),
     (troop_raise_skill, "trp_player",skl_power_strike,10),
     (troop_raise_skill, "trp_player",skl_weapon_master,10),
     (troop_raise_skill, "trp_player",skl_athletics,10),
     (troop_raise_skill, "trp_player",skl_power_draw,10),
     (troop_raise_skill, "trp_player",skl_riding,10),
     (troop_raise_skill, "trp_player",skl_spotting,10),
     (troop_raise_skill, "trp_player",skl_prisoner_management,10),
     (troop_raise_skill, "trp_player",skl_tactics,10),
     (troop_raise_skill, "trp_player",skl_inventory_management,10),
     (troop_raise_skill, "trp_player",skl_wound_treatment,10),
     (troop_raise_skill, "trp_player",skl_surgery,10),
     (troop_raise_skill, "trp_player",skl_first_aid,10),
     (troop_raise_skill, "trp_player",skl_pathfinding,10),
     (troop_raise_skill, "trp_player",skl_leadership,10),
     (troop_raise_skill, "trp_player",skl_engineer,10),
     (troop_add_gold, "trp_player", 1000000),
	 (troop_set_health, "trp_player", 100),
     (troop_add_item, "trp_player","itm_gondor_lance",imod_balanced),
     (troop_add_item, "trp_player","itm_shield_of_tuor",imod_reinforced),
     (troop_add_item, "trp_player","itm_gondor_ranger_sword",imod_masterwork),
     (troop_add_item, "trp_player","itm_gondor_hunter",imod_champion),
     (troop_add_item, "trp_player","itm_riv_helm_c",imod_lordly),
     (troop_add_item, "trp_player","itm_gon_tower_knight",imod_lordly),
     (troop_add_item, "trp_player","itm_mail_mittens",imod_lordly),
     (troop_add_item, "trp_player","itm_dol_greaves",imod_lordly),
     (troop_add_items, "trp_player","itm_lembas",3),
     (troop_add_items, "trp_player","itm_map",3),
     (troop_equip_items, "trp_player"),
     (troop_sort_inventory, "trp_player"),
     (display_message, "@You have been pimped up!", 0x30FFC8),
    ]
   ),
   ("camp_mvtest_expwar",[(eq,"$tld_war_began",0)],"Start the War!",[(add_xp_to_troop,9000,"trp_player"), (display_message, "@9000 XP added - now wait for the War...(assumes war starts at level 8)", 0x30FFC8),]),
   ("camp_mvtest_evilwar",[(eq,"$tld_war_began",1)],"Start the War of Two Towers! (defeat all good factions)",[
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
       (neq, ":cur_kingdom", "fac_player_supporters_faction"),
       (faction_slot_eq, ":cur_kingdom", slot_faction_side, faction_side_good),
       (faction_set_slot,":cur_kingdom",slot_faction_strength_tmp,-1000),
    (try_end),
    (display_message, "@Good factions defeated! Now wait for it...", 0x30FFC8),
   ]),
   ("camp_mvtest_rank",[],"Give me local money, rank and influence.",[
    (troop_add_gold, "trp_player", 10000),
    (call_script, "script_increase_rank", "$ambient_faction", 100),
    (faction_get_slot, reg0, "$ambient_faction", slot_faction_rank),
    (faction_get_slot, reg1, "$ambient_faction", slot_faction_influence),
    (val_add, reg1, 100),
    (faction_set_slot, "$ambient_faction", slot_faction_influence, reg1),
    (str_store_faction_name, s1, "$ambient_faction"),
    (display_message, "@{s1} rank points increased to {reg0}, influence to {reg1}!", 0x30FFC8),
   ]),
   ("camp_mvtest_wait",[(eq, cheat_switch, 1),],"Fast forward for 30 days.",[
         (troop_add_item, "trp_player", "itm_cram"),
		 (assign, "$g_camp_mode", 1),
		 (assign, "$g_fast_mode", 1),
         (assign, "$g_player_icon_state", pis_camping),
         (rest_for_hours_interactive, 24 * 30, 60), #30 day rest while not attackable with 40x speed #kham x 60
         (change_screen_return),
   ]), 
   # ("camp_mvtest_rankfunc",[],"Test rank functions.",[
    # (try_for_range, ":rank_index", 0, 13),
      # (call_script, "script_get_own_rank_title_to_s24", "$ambient_faction", ":rank_index"),
      # (call_script, "script_get_rank_points_for_rank", ":rank_index"),
      # (assign, reg1, ":rank_index"),
      # (display_message, "@Rank {reg1} ({reg0} points): {s24}", 0x30FFC8),
    # (try_end),
    # (try_for_range, ":something", 0, 25),
      # (store_mul, ":rank_points", ":something", 40),
      # (call_script, "script_get_rank_for_rank_points", ":rank_points"),
      # (assign, reg1, ":rank_points"),
      # (display_message, "@Rank points {reg1}: at rank {reg0}.", 0x30FFC8),
    # (try_end),
   # ]),
   # ("camp_mvtest_goodvictory",[],"Defeat all evil factions!",[
    # (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
       # (neq, ":cur_kingdom", "fac_player_supporters_faction"),
       # (neg|faction_slot_eq, ":cur_kingdom", slot_faction_side, faction_side_good),
       # (faction_set_slot,":cur_kingdom",slot_faction_strength_tmp,-1000),
    # (try_end),
    # (display_message, "@Evil factions defeated! Now wait for it...", 0x30FFC8),
   # ]),
   # ("camp_mvtest_influence",[],"Increase ambient faction influence by 100.",[
    # (faction_get_slot, reg0, "$ambient_faction", slot_faction_influence),
    # (val_add, reg0, 100),
    # (faction_set_slot, "$ambient_faction", slot_faction_influence, reg0),
    # (str_store_faction_name, s1, "$ambient_faction"),
    # (display_message, "@{s1} influence increased to {reg0}!", 0x30FFC8),
   # ]),
   ("camp_mvtest_reinf",[],"Reinforce me!",[
    (party_get_num_companions, ":old_size", "p_main_party"),
    (try_for_range, ":unused", 0, 10),
      (call_script, "script_cf_reinforce_party", "p_main_party"),
    (try_end),
    (party_get_num_companions, ":new_size", "p_main_party"),
	(store_mul, ":party_xp", ":new_size", 200),
	(party_upgrade_with_xp, "p_main_party", ":party_xp", 0),
    (assign, reg0, ":old_size"),
	(assign, reg1, ":new_size"),
    (display_message, "@Party size increased from {reg0} to {reg1}!", 0x30FFC8),
    (troop_set_slot, "trp_player", slot_troop_state, 0),
   ]),
   # ("camp_mvtest_free_willy",[],"Free all prisoners (for corrupt saves)",[
    # (spawn_around_party, "p_main_party", "pt_looters"),
    # (try_for_parties, ":cur_party"),
      # (party_is_active, ":cur_party"),
      # (party_get_num_prisoner_stacks, ":num_stacks", ":cur_party"),
      # (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        # (party_prisoner_stack_get_troop_id,     ":stack_troop",":cur_party",":stack_no"),
        # (party_prisoner_stack_get_size,         ":stack_size",":cur_party",":stack_no"),
        # (party_remove_prisoners, ":cur_party", ":stack_troop", ":stack_size"),
      # (try_end),
    # (try_end),
    # (display_message, "@All prisoners freed!", 0x30FFC8),
   # ]),
   # ("camp_mvtest_save_bug",[],"Create a party (for corrupt saves)",[
    # (spawn_around_party, "p_main_party", "pt_looters"),
    # (display_message, "@Party created, ID={reg0}!", 0x30FFC8),
   # ]),
   # ("camp_mvtest_test_music",[],"Test music path (plays track)",[
    # (play_track, "track_TLD_Map_Day_A", 1),
    # (display_message, "@Playing track - can you hear it?", 0x30FFC8),
   # ]),
   ("camp_mvtest_sieges",[],"Test sieges...",[(jump_to_menu, "mnu_mvtest_sieges")]),
   # ("camp_mvtest_trolls",[],"Test trolls in battle.",[
     # (party_add_members, "p_main_party", "trp_moria_troll", 3),
     # (set_spawn_radius, 0),
     # (spawn_around_party, "p_main_party", "pt_mordor_war_party"),
     # (assign, ":troll_party", reg0),
     # (party_clear, ":troll_party"),
     # (party_add_members, ":troll_party", "trp_c5_mordor_num_knight", 3),
     # (party_add_members, ":troll_party", "trp_mordor_olog_hai", 3),
     # (party_add_members, ":troll_party", "trp_a2_mordor_orc_archer", 10),
     # (party_add_members, ":troll_party", "trp_i3_mordor_large_orc", 20),
     # (display_message, "@Mordor party with olog hai spawned!", 0x30FFC8),
   # ]),            
   ("camp_mvtest_legend",[],"Enable legendary places.",[
    (enable_party, "p_legend_amonhen"),
    (enable_party, "p_legend_deadmarshes"),
    (enable_party, "p_legend_mirkwood"),
    (enable_party, "p_legend_fangorn"),
    (display_message, "@All four legendary places enabled!", 0x30FFC8),
   ]),
   ("camp_mvtest_intro",[(eq, cheat_switch, 1),],"Test cutscenes...",[(jump_to_menu, "mnu_mvtest_cutscenes"),]),
   # ("camp_mvtest_rewards",[],"Print ambient faction reward items.",[
    # (store_sub, ":faction_index", "$ambient_faction", kingdoms_begin),
    # (try_begin),
        # ]+concatenate_scripts([
            # [
            # (eq, ":faction_index", x),
            # ]+concatenate_scripts([[
                # (assign, ":rank", fac_reward_items_list[x][item_entry][0]),
                # (assign, ":item", fac_reward_items_list[x][item_entry][1]),
                # (assign, ":modifier", fac_reward_items_list[x][item_entry][2]),
                # (assign, reg0, ":rank"),
                # (assign, reg1, ":modifier"),
                # (str_store_item_name, s20, ":item"),
                # (display_message, "@Rank {reg0}: {s20}, mod {reg1}.", 0x30FFC8),
                # ] for item_entry in range(len(fac_reward_items_list[x]))
            # ])+[
         # (else_try),
            # ] for x in range(len(fac_reward_items_list))
        # ])+[
    # (try_end),   
   # ]),
   # ("camp_mvtest_coords",[],"Print party coordinates x100.",[
      # (set_fixed_point_multiplier, 100),
      # (party_get_position, pos13, "p_main_party"),
      # (position_get_x, reg2, pos13),
      # (position_get_y, reg3, pos13),
      # (display_message, "@Party position ({reg2},{reg3}).", 0x30FFC8),
   # ]),
   ("camp_mvtest_facstr",[(eq, cheat_switch, 1),],"View faction strengths.",[(jump_to_menu, "mnu_mvtest_facstr_report")]),
   ("camp_mvtest_killed",[(eq, cheat_switch, 1),],"View faction casualties.",[(jump_to_menu, "mnu_mvtest_faction_casualties")]),
   ("camp_mvtest_facai",[(eq, cheat_switch, 1),],"View faction AI.",[(jump_to_menu, "mnu_mvtest_facai_report")]),
   ("camp_mvtest_towns",[(eq, cheat_switch, 1),],"View center strength income.",[(jump_to_menu, "mnu_mvtest_town_wealth_report")]),
   # ("camp_mvtest_wm",[],"Where is my party?",[
    # (try_begin),
      # (call_script, "script_cf_party_is_south_of_white_mountains", "p_main_party"),
      # (display_message, "@The party is south of the White Mountains.", 0x30FFC8),
    # (else_try),
      # (call_script, "script_cf_party_is_north_of_white_mountains", "p_main_party"),
      # (display_message, "@The party is north of the White Mountains.", 0x30FFC8),
    # (else_try),
      # (display_message, "@The party is east of the White Mountains.", 0x30FFC8),
    # (try_end),
   # ]),
   # ("camp_mvtest_formula",[],"Test line formulas.",[
    # (call_script, "script_get_line_through_parties", "p_town_hornburg", "p_town_minas_tirith"),
    # (display_message, "@Debug: Hornburg-MT line: y = {reg0}/{reg1}*x + {reg2}"),
    # (call_script, "script_get_line_through_parties", "p_town_harad_camp", "p_town_minas_tirith"),
    # (display_message, "@Debug: Harad-MT line: y = {reg0}/{reg1}*x + {reg2}"),
    # (call_script, "script_get_line_through_parties", "p_town_morannon", "p_town_minas_tirith"),
    # (display_message, "@Debug: Morannon-MT line: y = {reg0}/{reg1}*x + {reg2}"),
   # ]),
   ("camp_mvtest_defeat",[],"Set Faction to Crushed.",[(jump_to_menu, "mnu_mvtest_destroy_faction")]),
   ("camp_mvtest_destroy",[],"Defeat a faction.",[(jump_to_menu, "mnu_mvtest_destroy_capital")]),
   ("camp_mvtest_advcamps",[(eq, cheat_switch, 1),],"Test advance camps.",[(jump_to_menu, "mnu_mvtest_advcamps")]),
   # ("camp_mvtest_destroy",[],"Destroy Hornburg!",[
     # (assign, ":root_defeated_party", "p_town_hornburg"),
     # (party_set_slot, ":root_defeated_party", slot_center_destroyed, 1), # DESTROY!
     # # disable and replace with ruins
     # (set_spawn_radius, 0),
     # (spawn_around_party, ":root_defeated_party", "pt_ruins"),
     # (assign, ":ruin_party", reg0),
     # #(party_get_icon, ":map_icon", ":root_defeated_party"),
     # #(party_set_icon, ":ruin_party", ":map_icon"),
     # (str_store_party_name, s1, ":root_defeated_party"),
     # (disable_party, ":root_defeated_party"),
     # (party_set_flags, ":ruin_party", pf_is_static|pf_always_visible|pf_hide_defenders|pf_label_medium, 1),
     # (party_set_name, ":ruin_party", "@{s1} ruins"),
     # (display_message, "@Hornburg razed - check map!", 0x30FFC8),
   # ]),
   # ("camp_mvtest_notes",[],"Update lord locations.",[
     # (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
       # (call_script, "script_update_troop_location_notes", ":troop_no", 0),
     # (try_end),
     # (display_message, "@Lord locations updated - see wiki!", 0x30FFC8),
   # ]),            
   # ("camp_mvtest_rescue",[],"Spawn a party with prisoners.",[
     # (set_spawn_radius, 0),
     # (spawn_around_party, "p_main_party", "pt_looters"),
     # (party_add_prisoners, reg0, "trp_peasant_woman", 10),
     # (display_message, "@Tribal orcs with women spawned!", 0x30FFC8),
   #]),
   # ("camp_mvtest_npcs",[],"Get all good npcs.",[
    # (try_for_range, ":npc", companions_begin, companions_end),
		# (store_troop_faction, ":fac", ":npc"),
		# (faction_slot_eq, ":fac", slot_faction_side, faction_side_good),
		# (party_add_members,"p_main_party",":npc",1),
	# (try_end),
    # (display_message, "@You got them all, pardner!", 0x30FFC8),
   # ]),
   ("camp_mvtest_back",[],"Back to dev menu.",[(jump_to_menu, "mnu_dev_menu")]),   

 ]),
( "mvtest_destroy_faction",0,
   "Choose a faction to set Strength to CRUSHED:",
   "none",
   [],
  [("back_test",[],"Back to test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),]
  +
  concatenate_scripts([[
  (
	"kill_faction",
	[(faction_slot_eq, faction_init[y][0], slot_faction_state, sfs_active),
     (faction_slot_ge, faction_init[y][0], slot_faction_strength_tmp, 0),
     (str_store_faction_name, s10, faction_init[y][0]),],
	"{s10}.",
	[
		(faction_set_slot, faction_init[y][0], slot_faction_strength_tmp, -1000),
        (str_store_faction_name, s10, faction_init[y][0]),
		(display_message, "@{s10} crushed! Lords will go to their capitals...", 0x30FFC8),
    ]
  )
  ]for y in range(len(faction_init)) ])      
 ),


( "mvtest_destroy_capital",0,
   "Choose a faction to defeat (Some factions may need you to click the button twice):",
   "none",
   [],
  [("back_test_2",[],"Back to test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),]
  +
  concatenate_scripts([[
  (
	"kill_capital",
	[(faction_slot_eq, faction_init[y][0], slot_faction_state, sfs_active),
     (faction_get_slot, ":capital", faction_init[y][0], slot_faction_capital),
     (party_slot_eq, ":capital", slot_faction_capital, 0),
     (str_store_faction_name, s10, faction_init[y][0]),],
	"{s10}.",
	[
		(faction_get_slot, ":capital", faction_init[y][0], slot_faction_capital),
 		(party_slot_eq, ":capital", slot_faction_capital, 0),
		(party_set_slot, ":capital", slot_center_destroyed, 1),
        (str_store_faction_name, s10, faction_init[y][0]),
		(display_message, "@{s10} defeated! Now wait for it...", 0x30FFC8),
    ]
  )
  ]for y in range(len(faction_init)) ])      
 ),


( "mvtest_facstr_report",0,
   "{s1}",
   "none",
   [(str_clear, s2),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (neq, ":cur_kingdom", "fac_player_supporters_faction"),
      (call_script, "script_faction_strength_string_to_s23", ":cur_kingdom"),
      (str_store_faction_name, s4, ":cur_kingdom"),
      (faction_get_slot, reg1, ":cur_kingdom", slot_faction_strength),
      (faction_get_slot, reg2, ":cur_kingdom", slot_faction_debug_str_gain),
      (faction_get_slot, reg3, ":cur_kingdom", slot_faction_debug_str_loss),
      (val_sub, reg2, reg3),
      (str_store_string, s2, "@{s2}^{s4}: {reg1} ({s23}) Diff: {reg2}"),
    (try_end),
    (str_store_string, s1, "@Faction strengths report:^{s2}"),
    ],
    [("back_test",[],"Back to test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
( "mvtest_facai_report",0,
   "{s1}",
   "none",
   [(str_clear, s2),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (neq, ":cur_kingdom", "fac_player_supporters_faction"),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (faction_get_slot, ":faction_ai_state", ":cur_kingdom", slot_faction_ai_state),
      (faction_get_slot, ":faction_ai_object", ":cur_kingdom", slot_faction_ai_object),
      (faction_get_slot, ":faction_theater", ":cur_kingdom", slot_faction_active_theater),
      (faction_get_slot, ":home_theater", ":cur_kingdom", slot_faction_home_theater),
      
	  # calculate number of active hosts
      (assign,":hosts",0),
	  (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end), 
        (store_troop_faction, ":troop_faction_no", ":troop_no"),
        (eq, ":troop_faction_no", ":cur_kingdom"),
		(troop_get_slot, ":party", ":troop_no", slot_troop_leaded_party),
		(gt,":party",0),
		(party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_party),
	    (val_add,":hosts",1),
	  (try_end),
      
      # AI string
      (try_begin),
        (eq, ":faction_ai_state", sfai_default),
        (str_store_string, s11, "@Defending"),
      (else_try),
        (eq, ":faction_ai_state", sfai_gathering_army),
        (str_store_string, s11, "@Gathering army"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_center),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Besieging {s11}"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_enemies_around_center),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Attacking enemies around {s11}"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_enemy_army),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Attacking enemy party {s11}"),
      (else_try),
        (assign, reg3, ":faction_ai_state"), (str_store_string, s11, "@Unknown({reg3})"),
      (try_end),
      
      # theater string
      (try_begin),
        (eq, ":home_theater", theater_SE),
        (str_store_string, s9, "@SE"),
      (else_try),
        (eq, ":home_theater", theater_SW),
        (str_store_string, s9, "@SW"),
      (else_try),
        (eq, ":home_theater", theater_C),
        (str_store_string, s9, "@C"),
      (else_try),
        (eq, ":home_theater", theater_N),
        (str_store_string, s9, "@N"),
      (else_try),
        (str_store_string, s9, "@INVALID"),
      (try_end),
      # theater string
      (try_begin),
        (eq, ":faction_theater", theater_SE),
        (str_store_string, s10, "@SE"),
      (else_try),
        (eq, ":faction_theater", theater_SW),
        (str_store_string, s10, "@SW"),
      (else_try),
        (eq, ":faction_theater", theater_C),
        (str_store_string, s10, "@C"),
      (else_try),
        (eq, ":faction_theater", theater_N),
        (str_store_string, s10, "@N"),
      (else_try),
        (str_store_string, s10, "@INVALID"),
      (try_end),
      
      (str_store_faction_name, s4, ":cur_kingdom"),
      (faction_get_slot, reg1, ":cur_kingdom", slot_faction_strength),
      (assign, reg2, ":hosts"),
      (str_store_string, s2, "@{s2}^{s4}: Th: {s9}-{s10} Str: {reg1} Hosts: {reg2} {s11}"),
    (try_end),
    (str_store_string, s1, "@Faction AI report:^{s2}"),
    ],
    [("details",[],"Detailed faction report...", [(jump_to_menu, "mnu_mvtest_facai_details"),]),
     ("back_mtest",[],"Back to main test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
( "mvtest_facai_details",0,
   "{s1}",
   "none",
   [
      (try_begin),
	    (neg|is_between, "$g_mvtest_faction", kingdoms_begin, kingdoms_end), #first use?
	    (assign, "$g_mvtest_faction", kingdoms_begin), #gondor
	  (try_end),
        
      (assign, ":cur_kingdom", "$g_mvtest_faction"),
      
      (faction_get_slot, ":faction_ai_state", ":cur_kingdom", slot_faction_ai_state),
      (faction_get_slot, ":faction_ai_object", ":cur_kingdom", slot_faction_ai_object),
      (faction_get_slot, ":faction_theater", ":cur_kingdom", slot_faction_active_theater),
      (faction_get_slot, ":home_theater", ":cur_kingdom", slot_faction_home_theater),
      
	  # calculate number of active hosts
      (assign,":hosts",0),
	  (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end), 
        (store_troop_faction, ":troop_faction_no", ":troop_no"),
        (eq, ":troop_faction_no", ":cur_kingdom"),
		(troop_get_slot, ":party", ":troop_no", slot_troop_leaded_party),
		(gt,":party",0),
		(party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_party),
	    (val_add,":hosts",1),
	  (try_end),
      
      # AI string
      (try_begin),
        (eq, ":faction_ai_state", sfai_default),
        (str_store_string, s11, "@Defending"),
      (else_try),
        (eq, ":faction_ai_state", sfai_gathering_army),
        (str_store_string, s11, "@Gathering army"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_center),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Besieging {s11}"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_enemies_around_center),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Attacking enemies around {s11}"),
      (else_try),
        (eq, ":faction_ai_state", sfai_attacking_enemy_army),
        (str_store_party_name, s11, ":faction_ai_object"),
        (str_store_string, s11, "@Attacking enemy party {s11}"),
      (else_try),
        (assign, reg3, ":faction_ai_state"), (str_store_string, s11, "@Unknown({reg3})"),
      (try_end),
      
      # theater string
      (try_begin),
        (eq, ":home_theater", theater_SE),
        (str_store_string, s9, "@SE"),
      (else_try),
        (eq, ":home_theater", theater_SW),
        (str_store_string, s9, "@SW"),
      (else_try),
        (eq, ":home_theater", theater_C),
        (str_store_string, s9, "@C"),
      (else_try),
        (eq, ":home_theater", theater_N),
        (str_store_string, s9, "@N"),
      (else_try),
        (str_store_string, s9, "@INVALID"),
      (try_end),
      # theater string
      (try_begin),
        (eq, ":faction_theater", theater_SE),
        (str_store_string, s10, "@SE"),
      (else_try),
        (eq, ":faction_theater", theater_SW),
        (str_store_string, s10, "@SW"),
      (else_try),
        (eq, ":faction_theater", theater_C),
        (str_store_string, s10, "@C"),
      (else_try),
        (eq, ":faction_theater", theater_N),
        (str_store_string, s10, "@N"),
      (else_try),
        (str_store_string, s10, "@INVALID"),
      (try_end),
      
      (str_store_faction_name, s4, ":cur_kingdom"),
      (faction_get_slot, reg1, ":cur_kingdom", slot_faction_strength),
      (assign, reg2, ":hosts"),
      (str_store_string, s1, "@Detailed faction AI report for {s4}:^Theater:{s9}-{s10} Str:{reg1} Hosts:{reg2} {s11}"),
      (try_begin),
        (neg|faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
        (str_store_string, s1, "@Faction defeated!^{s1}"),
      (try_end),
      
	  # AI details for each host
	  (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end), 
        (store_troop_faction, ":troop_faction_no", ":troop_no"),
        (eq, ":troop_faction_no", ":cur_kingdom"),
		(troop_get_slot, ":party", ":troop_no", slot_troop_leaded_party),
		(gt,":party",0),
        
        (str_store_troop_name, s6, ":troop_no"),
        (str_store_party_name, s7, ":party"),
        (str_store_string, s1, "@{s1}^{s6} leads {s7}, "),
        (try_begin),
          (party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_alone),
          (str_store_string, s1, "@{s1}(no host), "),          
        (try_end),
        
        (party_get_slot, ":party_ai_state", ":party", slot_party_ai_state),
        (party_get_slot, ":party_ai_object", ":party", slot_party_ai_object),
        (try_begin),
          (ge, ":party_ai_object", 0),
          (str_store_party_name, s7, ":party_ai_object"),
        (else_try),
          (str_store_string, s7, "@INVALID"),
        (try_end),
        
        # AI string
        (try_begin),(eq, ":party_ai_state", spai_undefined),               (str_store_string, s1, "@{s1}doing nothing"),
         (else_try),(eq, ":party_ai_state", spai_accompanying_army),       (str_store_string, s1, "@{s1}escorting {s7}"),
         (else_try),(eq, ":party_ai_state", spai_besieging_center),        (str_store_string, s1, "@{s1}besieging {s7}"),
         (else_try),(eq, ":party_ai_state", spai_holding_center),          (str_store_string, s1, "@{s1}defending {s7}"),
         (else_try),(eq, ":party_ai_state", spai_patrolling_around_center),(str_store_string, s1, "@{s1}patrolling around {s7}"),
         (else_try),(eq, ":party_ai_state", spai_recruiting_troops),       (str_store_string, s1, "@{s1}recruiting in {s7} - INVALID"),
         (else_try),(eq, ":party_ai_state", spai_raiding_around_center),   (str_store_string, s1, "@{s1}raiding around {s7} - INVALID"),
         (else_try),(eq, ":party_ai_state", spai_engaging_army),           (str_store_string, s1, "@{s1}engaging {s7}"),
         (else_try),(eq, ":party_ai_state", spai_retreating_to_center),    (str_store_string, s1, "@{s1}retreating to {s7}"),
         (else_try),                    (assign, reg3, ":party_ai_state"), (str_store_string, s1, "@{s1}unknown({reg3})"),
        (try_end),
	  (try_end),
    ],
    [("change",[
        (str_store_faction_name, s7, "$g_mvtest_faction"),
      ],
      "Change faction: {s7}",
      [
        (val_add, "$g_mvtest_faction", 1),
        (try_begin),
	      (eq, "$g_mvtest_faction", "fac_player_supporters_faction"),
	      (assign, "$g_mvtest_faction", kingdoms_begin),
	    (try_end),
      ]),
     ("defeat",[],"Set faction strength to -1000 (defeat).", [
       (faction_set_slot,"$g_mvtest_faction",slot_faction_strength_tmp,-1000),
       (display_message, "@Faction defeated! Now wait for it...", 0x30FFC8),]),
     ("dying",[],"Set faction strength to 300 (dying).", [
       (faction_set_slot,"$g_mvtest_faction",slot_faction_strength_tmp,300),
       (display_message, "@Faction almost defeated! Wait for the guardians to spawn...", 0x30FFC8),]),
     ("spent",[],"Set faction strength to 600 (spent).", [
       (faction_set_slot,"$g_mvtest_faction",slot_faction_strength_tmp,600),
       (display_message, "@Faction almost defeated! The AI can go for the capital now...", 0x30FFC8),]),
     ("back_ai",[],"Back to faction AI.", [(jump_to_menu, "mnu_mvtest_facai_report"),]),
    ]
 ),
( "mvtest_faction_casualties",0,
   "{s1}",
   "none",
   [  (try_begin),
	    (neg|is_between, "$g_mvtest_faction", kingdoms_begin, kingdoms_end), #first use?
	    (assign, "$g_mvtest_faction", kingdoms_begin), #gondor
	  (try_end),
        
      (assign, ":total_strength_loss", 0),
      
      (store_current_day, reg1),
      (str_store_faction_name, s4, "$g_mvtest_faction"),
      (str_store_string, s1, "@{s4} spawn losses after {reg1} days^"),
      
      # (assign, ":faction_scouts", 0),
      # (assign, ":faction_raiders", 0),
      # (assign, ":faction_patrol", 0),
      (assign, ":faction_caravan", 0),
      
      # abusing chests as scout, raider, patrol arrays (slot 0: length, slots 1,2,3.. array)
      (troop_set_slot, "trp_bonus_chest_1", 0, 0),
      (troop_set_slot, "trp_bonus_chest_2", 0, 0),
      (troop_set_slot, "trp_bonus_chest_3", 0, 0),
      
      # determine faction spawns (scouts, raiders, patrol, caravan) by looking at center spawns
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (store_faction_of_party, ":center_faction", ":center_no"),
        (eq, ":center_faction", "$g_mvtest_faction"),
        #(party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD - not destroyed; not important
        (party_get_slot, ":center_scouts", ":center_no", slot_center_spawn_scouts),
        (party_get_slot, ":center_raiders", ":center_no", slot_center_spawn_raiders),
        (party_get_slot, ":center_patrol", ":center_no", slot_center_spawn_patrol),
        (party_get_slot, ":center_caravan", ":center_no", slot_center_spawn_caravan),
        (try_begin),
          (gt, ":center_scouts", 0),
          (troop_get_slot, ":number_spawns", "trp_bonus_chest_1", 0),
          (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
          (assign, ":scout_found", 0),
          (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
            (troop_slot_eq, "trp_bonus_chest_1", ":slot", ":center_scouts"),
            (assign, ":scout_found", 1),
          (try_end),
          (eq, ":scout_found", 0),
          (troop_set_slot, "trp_bonus_chest_1", 0, ":number_spawns_plus_one"),
          (troop_set_slot, "trp_bonus_chest_1", ":number_spawns_plus_one", ":center_scouts"),
        (try_end),
        (try_begin),
          (gt, ":center_raiders", 0),
          (troop_get_slot, ":number_spawns", "trp_bonus_chest_2", 0),
          (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
          (assign, ":scout_found", 0),
          (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
            (troop_slot_eq, "trp_bonus_chest_2", ":slot", ":center_raiders"),
            (assign, ":scout_found", 1),
          (try_end),
          (eq, ":scout_found", 0),
          (troop_set_slot, "trp_bonus_chest_2", 0, ":number_spawns_plus_one"),
          (troop_set_slot, "trp_bonus_chest_2", ":number_spawns_plus_one", ":center_raiders"),
        (try_end),
        (try_begin),
          (gt, ":center_patrol", 0),
          (troop_get_slot, ":number_spawns", "trp_bonus_chest_3", 0),
          (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
          (assign, ":scout_found", 0),
          (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
            (troop_slot_eq, "trp_bonus_chest_3", ":slot", ":center_patrol"),
            (assign, ":scout_found", 1),
          (try_end),
          (eq, ":scout_found", 0),
          (troop_set_slot, "trp_bonus_chest_3", 0, ":number_spawns_plus_one"),
          (troop_set_slot, "trp_bonus_chest_3", ":number_spawns_plus_one", ":center_patrol"),
        (try_end),
        (try_begin), #one type of caravan, if any
          (eq, ":faction_caravan", 0), (gt, ":center_caravan", 0), (assign, ":faction_caravan", ":center_caravan"),
        (try_end),
	  (try_end),
      
      # Print out the results
      (try_begin),
        (troop_get_slot, ":number_spawns", "trp_bonus_chest_1", 0),
        (gt, ":number_spawns", 0),
        (assign, ":spawns_destroyed", 0),
        (assign, ":spawns_active", 0),
        (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
        (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
          (troop_get_slot, ":spawn", "trp_bonus_chest_1", ":slot"),
          (store_num_parties_destroyed, ":val", ":spawn"),
          (val_add, ":spawns_destroyed", ":val"),
          (store_num_parties_of_template, ":val", ":spawn"),
          (val_add, ":spawns_active", ":val"),
        (try_end),
        (assign, reg1, ":spawns_destroyed"),
        (assign, reg3, ":spawns_active"),
        (store_mul, reg2, reg1, ws_scout_vp), #strength loss
        (str_store_string, s1, "@{s1}^Scouts lost: {reg1} Str loss: {reg2} Active: {reg3}"),
        (val_add, ":total_strength_loss", reg2),
      (try_end),
      (try_begin),
        (troop_get_slot, ":number_spawns", "trp_bonus_chest_2", 0),
        (gt, ":number_spawns", 0),
        (assign, ":spawns_destroyed", 0),
        (assign, ":spawns_active", 0),
        (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
        (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
          (troop_get_slot, ":spawn", "trp_bonus_chest_2", ":slot"),
          (store_num_parties_destroyed, ":val", ":spawn"),
          (val_add, ":spawns_destroyed", ":val"),
          (store_num_parties_of_template, ":val", ":spawn"),
          (val_add, ":spawns_active", ":val"),
        (try_end),
        (assign, reg1, ":spawns_destroyed"),
        (assign, reg3, ":spawns_active"),
        (store_mul, reg2, reg1, ws_raider_vp), #strength loss
        (str_store_string, s1, "@{s1}^Raiders lost: {reg1} Str loss: {reg2} Active: {reg3}"),
        (val_add, ":total_strength_loss", reg2),
      (try_end),
      (try_begin),
        (troop_get_slot, ":number_spawns", "trp_bonus_chest_3", 0),
        (gt, ":number_spawns", 0),
        (assign, ":spawns_destroyed", 0),
        (assign, ":spawns_active", 0),
        (store_add, ":number_spawns_plus_one", ":number_spawns", 1),
        (try_for_range, ":slot", 1, ":number_spawns_plus_one"),
          (troop_get_slot, ":spawn", "trp_bonus_chest_3", ":slot"),
          (store_num_parties_destroyed, ":val", ":spawn"),
          (val_add, ":spawns_destroyed", ":val"),
          (store_num_parties_of_template, ":val", ":spawn"),
          (val_add, ":spawns_active", ":val"),
        (try_end),
        (assign, reg1, ":spawns_destroyed"),
        (assign, reg3, ":spawns_active"),
        (store_mul, reg2, reg1, ws_patrol_vp), #strength loss
        (str_store_string, s1, "@{s1}^Patrols lost: {reg1} Str loss: {reg2} Active: {reg3}"),
        (val_add, ":total_strength_loss", reg2),
      (try_end),
      (try_begin),
        (gt, ":faction_caravan", 0),
        (store_num_parties_destroyed, reg1, ":faction_caravan"),
        (store_mul, reg2, reg1, ws_caravan_vp), #strength loss
        (store_num_parties_of_template, reg3, ":faction_caravan"),
        (str_store_string, s1, "@{s1}^Caravans lost: {reg1} Str loss: {reg2} Active: {reg3}"),
        (val_add, ":total_strength_loss", reg2),
      (try_end),
      (faction_get_slot, ":prisoner_train_pt", "$g_mvtest_faction", slot_faction_prisoner_train),
      (try_begin),
        (gt, ":prisoner_train_pt", 0),
        (store_num_parties_destroyed, reg1, ":prisoner_train_pt"), #note that removed on arrival are also counted here
        (store_mul, reg2, reg1, ws_p_train_vp), #strength loss
        (store_num_parties_of_template, reg3, ":prisoner_train_pt"),
        (str_store_string, s1, "@{s1}^P. trains lost-arrived: {reg1} Strength loss: 0{reg2?-{reg2}:} Active: {reg3}"),
        #(val_add, ":total_strength_loss", reg2),
      (try_end),
      
      (faction_get_slot, reg1, "$g_mvtest_faction", slot_faction_debug_str_gain),
      (str_store_string, s1, "@{s1}^^Total strength gain: {reg1}"),
      (faction_get_slot, reg2, "$g_mvtest_faction", slot_faction_debug_str_loss),
      (str_store_string, s1, "@{s1}^Total strength loss: {reg2}"),
      (assign, reg3, ":total_strength_loss"),
      (str_store_string, s1, "@{s1}^(Strength loss from spawns: {reg3})"),
      (val_sub, reg1, reg2),
      (str_store_string, s1, "@{s1}^Difference: {reg1}"),
    ],
    [("prev_faction",[],
      "Previous faction",
      [
        (try_begin),
	      (eq, "$g_mvtest_faction", kingdoms_begin),
	      (assign, "$g_mvtest_faction", kingdoms_end),
	    (try_end),
        (val_sub, "$g_mvtest_faction", 1),
      ]),
     ("next_faction",[],
      "Next faction",
      [
        (val_add, "$g_mvtest_faction", 1),
        (try_begin),
	      (eq, "$g_mvtest_faction", kingdoms_end),
	      (assign, "$g_mvtest_faction", kingdoms_begin),
	    (try_end),
      ]),
     ("back_mtest",[],"Back to main test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
( "mvtest_town_wealth_report",0,
   "{s1}",
   "none",
   [  (try_begin),
	    (neg|is_between, "$g_mvtest_faction", kingdoms_begin, kingdoms_end), #first use?
	    (assign, "$g_mvtest_faction", kingdoms_begin), #gondor
	  (try_end),
        
      (assign, ":cur_kingdom", "$g_mvtest_faction"),
      (assign, ":total_income", 0),
      
      (str_store_faction_name, s4, ":cur_kingdom"),
      (str_store_string, s1, "@Daily strength income and garrisons for {s4}"),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
        (store_faction_of_party, ":center_faction", ":center_no"),
        (eq, ":center_faction", ":cur_kingdom"),
        (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD - not destroyed
        (str_store_party_name, s7, ":center_no"),
        (party_get_slot, reg1, ":center_no", slot_center_strength_income),
        (party_get_slot, reg2, ":center_no", slot_center_garrison_limit),
        (party_get_num_companions, reg3, ":center_no"),
        (party_get_slot, reg4, ":center_no", slot_center_destroy_on_capture),
        (val_add, ":total_income", reg1),
        (str_store_string, s1, "@{s1}^{s7}: {reg1}  Garrison: {reg3}/{reg2}{reg4?: Capturable}"),
	  (try_end),
      (assign, reg1, ":total_income"),
      (str_store_string, s1, "@{s1}^^Total: {reg1}"),
    ],
    [("change",[
        (str_store_faction_name, s7, "$g_mvtest_faction"),
      ],
      "Change faction: {s7}",
      [
        (val_add, "$g_mvtest_faction", 1),
        (try_begin),
	      (eq, "$g_mvtest_faction", "fac_player_supporters_faction"),
	      (assign, "$g_mvtest_faction", kingdoms_begin),
	    (try_end),
      ]),
     ("back_mtest",[],"Back to main test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
( "mvtest_sieges",0,
   "Test sieges",
   "none",
   [],
 	[
	("order_siege",[],"Order ambient faction to besiege...", [(jump_to_menu, "mnu_mvtest_order_siege")]),
     ("order_siege_wo",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege West Osgiliath.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
		(try_for_range, ":unused", 0, 40),
			(call_script, "script_cf_reinforce_party", ":king_party"),
		(try_end),
        (party_relocate_near_party, ":king_party", "p_town_west_osgiliath", 0),
        (party_set_slot, "p_town_west_osgiliath", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_west_osgiliath"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_west_osgiliath"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges West Osgiliath!", 0x30FFC8),
        (change_screen_map),
      ]),
	  ("order_siege_erech",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege Erech.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
		(try_for_range, ":unused", 0, 40),
			(call_script, "script_cf_reinforce_party", ":king_party"),
		(try_end),
        (party_relocate_near_party, ":king_party", "p_town_erech", 0),
        (party_set_slot, "p_town_erech", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_erech"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_erech"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges Erech!", 0x30FFC8),
        (change_screen_map),
      ]),
	 ("order_siege_pinnath",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege Pinnath Gelin.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
		(try_for_range, ":unused", 0, 40),
			(call_script, "script_cf_reinforce_party", ":king_party"),
		(try_end),
        (party_relocate_near_party, ":king_party", "p_town_pinnath_gelin", 0),
        (party_set_slot, "p_town_pinnath_gelin", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_pinnath_gelin"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_pinnath_gelin"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges Pinnath Gelin!", 0x30FFC8),
        (change_screen_map),
      ]),
	 ("order_siege_edhellond",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege Edhellond.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
		(try_for_range, ":unused", 0, 40),
			(call_script, "script_cf_reinforce_party", ":king_party"),
		(try_end),
        (party_relocate_near_party, ":king_party", "p_town_edhellond", 0),
        (party_set_slot, "p_town_edhellond", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_edhellond"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_edhellond"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges Edhellond!", 0x30FFC8),
        (change_screen_map),
      ]),
     ("order_siege_candros",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege Edoras.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
		(try_for_range, ":unused", 0, 40),
			(call_script, "script_cf_reinforce_party", ":king_party"),
		(try_end),
        (party_relocate_near_party, ":king_party", "p_town_edoras", 0),
        (party_set_slot, "p_town_edoras", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_edoras"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_edoras"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges Edoras!", 0x30FFC8),
        (change_screen_map),
      ]),
     ("order_siege_cairandros",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege Cair Andros.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
		(try_for_range, ":unused", 0, 40),
			(call_script, "script_cf_reinforce_party", ":king_party"),
		(try_end),
        (party_relocate_near_party, ":king_party", "p_town_cair_andros", 0),
        (party_set_slot, "p_town_cair_andros", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_cair_andros"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_cair_andros"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges Cair Andros!", 0x30FFC8),
        (change_screen_map),
      ]),
	("order_siege_pelargir",[
        (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Gothmog to besiege Pelargir.",
      [ (troop_get_slot, ":king_party", "trp_mordor_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
		(try_for_range, ":unused", 0, 40),
			(call_script, "script_cf_reinforce_party", ":king_party"),
		(try_end),
        (party_relocate_near_party, ":king_party", "p_town_pelargir", 0),
        (party_set_slot, "p_town_pelargir", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_pelargir"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_pelargir"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Gothmog besieges Pelargir!", 0x30FFC8),
        (change_screen_map),
      ]),
     ("order_siege_wemnet",[
        (troop_get_slot, ":king_party", "trp_isengard_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Saruman to besiege Edoras.",
      [
        (troop_get_slot, ":king_party", "trp_isengard_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
		(try_for_range, ":unused", 0, 40),
			(call_script, "script_cf_reinforce_party", ":king_party"),
		(try_end),
        (party_relocate_near_party, ":king_party", "p_town_edoras", 0),
        (party_set_slot, "p_town_edoras", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_edoras"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_edoras"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Saruman besieges Edoras!", 0x30FFC8),
        (change_screen_map),
      ]),
     ("order_siege_dale",[
        (troop_get_slot, ":king_party", "trp_rhun_lord", slot_troop_leaded_party),
        (party_is_active, ":king_party"),
     ],"Order Partitava to besiege Dale.",
      [
        (troop_get_slot, ":king_party", "trp_rhun_lord", slot_troop_leaded_party),
        (party_detach, ":king_party"),
		(try_for_range, ":unused", 0, 40),
			(call_script, "script_cf_reinforce_party", ":king_party"),
		(try_end),
        (party_relocate_near_party, ":king_party", "p_town_dale", 0),
        (party_set_slot, "p_town_dale", slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, "p_town_dale"),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", "p_town_dale"),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (display_message, "@Partitava besieges Dale!", 0x30FFC8),
        (change_screen_map),
      ]),
     ("back_mtest",[],"Back to main test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
( "mvtest_order_siege",0,
   "Order {s1} to besiege...",
   "none",
   [(str_store_faction_name, s1, "$ambient_faction"),],
   [("back_sieg",[],"Back to siege menu.", [(jump_to_menu, "mnu_mvtest_sieges"),]),]
  +
  concatenate_scripts([[
  (
	"siege_town",
	[(party_is_active, center_list[y][0]),
     (faction_get_slot, ":king", "$ambient_faction", slot_faction_marshall),
     (troop_get_slot, ":king_party", ":king", slot_troop_leaded_party),
     (party_is_active, ":king_party"),
     (store_faction_of_party, ":town_faction", center_list[y][0]),
     (store_relation, ":reln", ":town_faction", "$ambient_faction"),
	 (lt, ":reln", 0),
     (faction_get_slot, ":faction_theater", "$ambient_faction", slot_faction_active_theater),
     (party_slot_eq, center_list[y][0], slot_center_theater, ":faction_theater"),
     (party_slot_eq, center_list[y][0], slot_center_is_besieged_by, -1),
     (str_store_party_name, s10, center_list[y][0]),],
	"{s10}.",
	[
        #order ambient king to besiege
        (faction_get_slot, ":king", "$ambient_faction", slot_faction_marshall),
        (troop_get_slot, ":king_party", ":king", slot_troop_leaded_party),
        (party_detach, ":king_party"),
        (party_relocate_near_party, ":king_party", center_list[y][0], 0),
        (party_set_slot, center_list[y][0], slot_center_is_besieged_by, ":king_party"),
        (call_script, "script_party_set_ai_state", ":king_party", spai_besieging_center, center_list[y][0]),
        (party_set_ai_behavior, ":king_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":king_party", center_list[y][0]),
        (party_set_flags, ":king_party", pf_default_behavior, 1),
        (party_set_slot, ":king_party", slot_party_ai_substate, 1),
        (str_store_party_name, s10, center_list[y][0]),
		(display_message, "@{s10} besieged!", 0x30FFC8),
        (change_screen_map),
    ]
  )
  ]for y in range(len(center_list)) ])      
 ),
( "mvtest_advcamps",0,
   "Test advance camps",
   "none",
   [], [
    ("spawnSW",[],"Spawn SW advance camps", [
	  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		  (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
	  (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_SW),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_SW),
          (disable_party, ":adv_camp"),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (display_message, "@SW advance camps spawned around a point northwest of East Emnet!", 0x30FFC8),
    ]),
    ("spawnSE",[],"Spawn SE advance camps", [
	  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		  (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
	  (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_SE),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_SE),
          (disable_party, ":adv_camp"),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (display_message, "@SE advance camps spawned around a point west of West Osgiliath!", 0x30FFC8),
    ]),
    ("spawnC",[],"Spawn C advance camps", [
	  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		  (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
	  (try_end),
	  (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_C),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_C),
          (disable_party, ":adv_camp"),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (display_message, "@C advance camps spawned around Cerin Amroth!", 0x30FFC8),
    ]),
    ("spawnN",[],"Spawn N advance camps", [
	  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		  (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
	  (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_N),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_N),
          (disable_party, ":adv_camp"),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (display_message, "@N advance camps spawned around Beorn's House!", 0x30FFC8),
    ]),

    ("disable",[],"Remove all advance camps", [
	  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		(party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
	  (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        
        (faction_get_slot, ":home_theater", ":faction_no", slot_faction_home_theater),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, ":home_theater"),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (call_script, "script_destroy_center", ":adv_camp"),
      (try_end),
      #(call_script, "script_update_active_theaters"),
      (display_message, "@Advance camps disabled, theaters restored!", 0x30FFC8),
    ]),

    ("movespawnSW",[],"Move SW theater center and spawn camps there", [
      (party_get_position, pos13, "p_main_party"),
      (party_set_position, "p_theater_sw_center", pos13),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_SW),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_SW),
          (disable_party, ":adv_camp"),
		  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		      (store_distance_to_party_from_party,":dist", ":adv_camp", ":camp_pointer"),
		      (le, ":dist",1),
		      (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
		  (try_end),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (set_fixed_point_multiplier, 1000),
      (position_get_x, reg2, pos13),
      (position_get_y, reg3, pos13),
      (display_message, "@SW advance camps spawned around {reg2},{reg3}!", 0x30FFC8),
    ]),
    ("movespawnSE",[],"Move SE theater center and spawn camps there", [
      (party_get_position, pos13, "p_main_party"),
      (party_set_position, "p_theater_se_center", pos13),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_SE),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_SE),
          (disable_party, ":adv_camp"),
		  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		      (store_distance_to_party_from_party,":dist", ":adv_camp", ":camp_pointer"),
		      (le, ":dist",1),
		      (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
		  (try_end),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (set_fixed_point_multiplier, 1000),
      (position_get_x, reg2, pos13),
      (position_get_y, reg3, pos13),
      (display_message, "@SE advance camps spawned around {reg2},{reg3}!", 0x30FFC8),
    ]),
    ("movespawnC",[],"Move C theater center and spawn camps there", [
      (party_get_position, pos13, "p_main_party"),
      (party_set_position, "p_theater_c_center", pos13),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_C),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_C),
          (disable_party, ":adv_camp"),
		  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		      (store_distance_to_party_from_party,":dist", ":adv_camp", ":camp_pointer"),
		      (le, ":dist",1),
		      (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
		  (try_end),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (set_fixed_point_multiplier, 1000),
      (position_get_x, reg2, pos13),
      (position_get_y, reg3, pos13),
      (display_message, "@C advance camps spawned around {reg2},{reg3}!", 0x30FFC8),
    ]),
    ("movespawnN",[],"Move N theater center and spawn camps there", [
      (party_get_position, pos13, "p_main_party"),
      (party_set_position, "p_theater_n_center", pos13),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, ":faction_no", slot_faction_active_theater, theater_N),
        (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_home_theater, theater_N),
          (disable_party, ":adv_camp"),
		  (try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
		      (store_distance_to_party_from_party,":dist", ":adv_camp", ":camp_pointer"),
		      (le, ":dist",1),
		      (party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
		  (try_end),
        (else_try),        
          (call_script, "script_get_advcamp_pos_predefined", ":faction_no"), #fills pos1
          (party_set_position, ":adv_camp", pos1),
          (enable_party, ":adv_camp"),
        (try_end),
      (try_end),
      (set_fixed_point_multiplier, 1000),
      (position_get_x, reg2, pos13),
      (position_get_y, reg3, pos13),
      (display_message, "@N advance camps spawned around {reg2},{reg3}!", 0x30FFC8),
    ]),
 
    ("continue",[],"Continue...", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
  ),
( "mvtest_cutscenes",0,
   "Choose an option:",
   "none",
   [],
    [("intro",[], "Play intro.", [(jump_to_menu, "mnu_auto_intro_rohan"),]),
     ("joke",[],  "Play GA joke.", [(jump_to_menu, "mnu_auto_intro_joke"),]),
 ]+concatenate_scripts([[ 
     #("test",[],  "Play Gandalf test encounter.", [(jump_to_menu, "mnu_auto_convo"),]),
     ("gandalf_1",[], "Play Gandalf advice.", [(call_script, "script_start_conversation_cutscene", tld_cc_gandalf_advice),]),
     ("gandalf_2",[], "Play Gandalf ally down.", [(assign, "$g_tld_convo_subject", "fac_dale"),(call_script, "script_start_conversation_cutscene", tld_cc_gandalf_ally_down),]),
     ("gandalf_3",[], "Play Gandalf enemy down.", [(assign, "$g_tld_convo_subject", "fac_gundabad"),(call_script, "script_start_conversation_cutscene", tld_cc_gandalf_enemy_down),]),
     ("gandalf_4",[], "Play Gandalf victory.", [(call_script, "script_start_conversation_cutscene", tld_cc_gandalf_victory),]),
     ("nazgul_1",[], "Play Nazgul Baggins.", [(call_script, "script_start_conversation_cutscene", tld_cc_nazgul_baggins),]),
     ("nazgul_2",[], "Play Nazgul evil war.", [(call_script, "script_start_conversation_cutscene", tld_cc_nazgul_evil_war),]),
     ("nazgul_3",[], "Play Nazgul victory.", [(call_script, "script_start_conversation_cutscene", tld_cc_nazgul_victory),]),
     ("scenetest",[], "Enter conversation scene.", [
                                (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
                                (set_visitor,0,"trp_player"),
                                (set_visitor,1,"trp_gandalf"),
                                (set_jump_mission,"mt_test_gandalf"),
                                (jump_to_scene,"scn_conversation_scene"),
                                (change_screen_mission),
                                ]),
     ("partytest",[], "Create a Gandalf party following you.", [
                                (set_spawn_radius, 5),
                                (spawn_around_party, "p_main_party", "pt_gandalf"),
                                (assign, ":party", reg0),
                                (party_set_ai_behavior, ":party", ai_bhvr_attack_party),
                                (party_set_ai_object, ":party", "p_main_party"),
                                (party_set_flags, ":party", pf_default_behavior, 0),
                                (party_set_slot, ":party", slot_party_ai_state, spai_undefined),
                                (troop_set_slot, "trp_gandalf", slot_troop_leaded_party, ":party"),
                                (assign, "$g_tld_gandalf_state", tld_cc_gandalf_advice),
                                (display_message, "@Gandalf would like to have a little chat!", 0x30FFC8),
                                ]),
 ] for ct in range(cheat_switch)])+[
     ("back_mtest",[],"Back to main test menu.", [(jump_to_menu, "mnu_camp_mvtest"),]),
    ]
 ),
## MadVader test end
## Kham Test Begin
( "camp_khamtest",0,
	"^^^^^Click on an option to toggle.^^^Tweaks Gondor to have more troops in a party, gives them more hosts, gives them hosts more frequently, and lets Gondor lords wait longer to gather.^^Have to wait for the trigger to occur","none",[],
    [
    ("enable_kham_cheat",[],"Enable Kham Cheat Mode", [(troop_set_slot, "trp_player", slot_troop_home, 22), (display_message, "@Kham Cheat Mode ON!")]),
    ] + (is_a_wb_menu==1 and [
    ("action_view_all_items",[],"View all items.", [(assign, "$temp", 0), (start_presentation, "prsnt_all_items")]),
    ("give_custom_armor",[],"Give Custom Armor", [(troop_add_item, "trp_player", "itm_gondor_custom"), (troop_add_item, "trp_player", "itm_uruk_spear")]),
    ] or []) + [
    ("spawn_orc_horde_troll",[],"Spawn Orc Horde with Trolls",[
        (jump_to_menu, "mnu_orc_horde_troll")]),
    ("add_trolls",[],"Add 1 Troll to your party (spam for more!)",[
        (party_force_add_members, "p_main_party", "trp_mordor_olog_hai", 1),
        (display_message, "@1 troll added!")]),
    #("give_siege_stones", [],"Siege Stones Test",[(troop_add_item, "trp_player","itm_stones_siege"), (party_add_members, "p_main_party", "trp_test_vet_archer", 10), (display_message, "@Siege Stones Test")]),
    ("enable_raftmen",[],"Enable Raft Men Party", [(enable_party, "p_raft"), (display_message, "@Raft Men party enabled. They are down River Running", color_good_news)]),
    #("test_presentation",[],"Test Presentation", [(start_presentation, "prsnt_faction_intro_text")]),
    ] + (is_a_wb_menu==1 and [
    ("what_theater",[], "Which Theater Am I in?", [(call_script, "script_find_theater", "p_main_party"), (display_message, "@theater: {reg0}")]),
    ("what_region",[], "Add 1000000 XP to Party", 
    	[(party_add_xp, "p_main_party", 1000000), (display_message, "@XP added", color_good_news),
    	]),
    ("player_control_allies",[],"Battlesize set to {reg66}", [(options_set_battle_size, reg66),]),
     ] or []) + [
    ("spawn_orc_horde",[],"Spawn Orc Horde", [(set_spawn_radius,3),(spawn_around_party, "p_main_party", "pt_orc_horde"),(display_message, "@Orc Horde Spawned!"),]),
    ("spawn_vet_archer",[],"Spawn Vet Archer", [(set_spawn_radius,3),(spawn_around_party, "p_main_party", "pt_vet_archer"),(display_message, "@Vet Archer Spawned!"),(assign, ":party", reg0),(call_script, "script_party_wound_all_members", ":party"),]),
    ("melee_ai_test",[],"Melee AI Test", [
    	(set_spawn_radius,1),
    	(spawn_around_party, "p_main_party", "pt_vet_archer"),
    	(party_add_members, "p_main_party", "trp_badass_theo",1), 
    	(display_message, "@Killer WItcher Spawned, Badass King Theo added!")]),
    ("player_enable_siege",[], "Enable Player Siege", [(assign, "$player_allowed_siege",1),(display_message, "@Player Siege Enabled", color_bad_news)]),
    ("animal_test",[], "Animal Ambush Test", [
    	(try_begin), 
    		(this_or_next|eq, "$current_player_region", region_n_mirkwood),
			(this_or_next|eq, "$current_player_region", region_s_mirkwood), 
			(this_or_next|eq, "$current_player_region", region_grey_mountains),
			(			  eq, "$current_player_region", region_misty_mountains),
			(jump_to_menu, "mnu_animal_ambush"),
		(else_try),
			(display_message, "@You are not in the right region to spawn animal ambushes. Please go to N Mirkwood, S Mirkwood, Grey Mountains, or Misty Mountains", color_bad_news),
		(try_end)]),
    #("check_if_capital",[], "How Many Centers Left (Gondor)", [(call_script, "script_cf_check_if_only_capital_left", "p_town_pinnath_gelin")]),
    ("camp_khamtest_back",[],"Back",[(jump_to_menu, "mnu_dev_menu")]),
 ]),

( "orc_horde_troll",0,
	"^^^^^^^^Click on an option to change number of trolls in the orc horde to spawn","none",[],
	[	
	 ("orc_horde_choice",
		[
			(assign, reg1, "$temp2"),
			(str_store_string, s1, "@{reg1}"),

		],

		"Number of trolls to add to Orc Horde: {s1}",
		[
				(val_add, "$temp2", 1),
				(try_begin),
					(gt, "$temp2", 30),
					(assign, "$temp2", 1),
				(try_end),
				(jump_to_menu, "mnu_auto_orc_horde_troll"),
		]),
	("orc_horde_select", [(assign, reg1, "$temp2"),], "Spawn Orc Horde with {reg1} Olog Hai", [
		(set_spawn_radius,3),
    	(spawn_around_party, "p_main_party", "pt_orc_horde"),
    	(party_add_members, reg0, "trp_mordor_olog_hai", reg1),
    	(display_message, "@Orc Horde Spawned!"),
    	]),

    ("orc_horde_back",[],"Back to Kham Test menu.",[(jump_to_menu, "mnu_camp_khamtest")]),
	]
),
## Kham Test End
( "game_options",0,
	"^^^^^^^^Click on an option to toggle:","none",[(try_begin), (lt, "$savegame_version",4),(call_script, "script_update_savegame"), (try_end)],
    [

    ("game_options_war_level_start",[

    		(assign, reg0, "$tld_player_level_to_begin_war"),
			(str_store_string, s1, "@{reg0}")],

		"War Starts at Level: {s1}",[
			(store_add, "$tld_player_level_to_begin_war", 2, "$tld_player_level_to_begin_war"),
			(try_begin),
				(gt, "$tld_player_level_to_begin_war", 21),
				(assign, "$tld_player_level_to_begin_war",2),
			(try_end),(jump_to_menu, "mnu_auto_options")]),

    ("game_options_restrict_items",[(try_begin),(eq,"$tld_option_crossdressing",0),(str_store_string, s7, "@ON"),
									(else_try),(str_store_string, s7, "@OFF (cheat)"),(try_end),
        ],"Restricted player equipment:  {s7}",[
        (store_sub, "$tld_option_crossdressing", 1, "$tld_option_crossdressing"),(val_clamp, "$tld_option_crossdressing", 0, 2),(jump_to_menu, "mnu_auto_options"),]),

    ("game_options_formations",[(try_begin),(neq, "$tld_option_formations", 0),(str_store_string, s7, "@ON"),
								(else_try),(str_store_string, s7, "@OFF"),(try_end),
        ],"Battle formations and AI:  {s7}",[
        (store_sub, "$tld_option_formations", 1, "$tld_option_formations"),(val_clamp, "$tld_option_formations", 0, 2),(jump_to_menu, "mnu_auto_options"),]),

    ("game_options_siege_ai",[(try_begin),(neq, "$advanced_siege_ai", 0),(str_store_string, s7, "@ON"),
								(else_try),(str_store_string, s7, "@Native"),(try_end),
        ],"Advanced Siege AI:  {s7}",[
        (store_sub, "$advanced_siege_ai", 1, "$advanced_siege_ai"),(val_clamp, "$advanced_siege_ai", 0, 2),(jump_to_menu, "mnu_auto_options"),]),

	("game_options_town_menu",[(try_begin),(eq, "$tld_option_town_menu_hidden", 0),(str_store_string, s7, "@ON"),
								 (else_try),(str_store_string, s7, "@OFF"),(try_end),
	    ],"Town NPCs always accessible from Menus:  {s7}",[
	    (store_sub,"$tld_option_town_menu_hidden",1,"$tld_option_town_menu_hidden"),(val_clamp,"$tld_option_town_menu_hidden",0,2),(jump_to_menu, "mnu_auto_options"),]),

	("game_options_cutscenes",[(try_begin),(neq, "$tld_option_cutscenes", 0),(str_store_string, s7, "@ON"),
								 (else_try),(str_store_string, s7, "@OFF"),(try_end),
	    ],"Cutscenes:  {s7}",[
	    (store_sub,"$tld_option_cutscenes",1,"$tld_option_cutscenes"),(val_clamp, "$tld_option_cutscenes",0,2),(jump_to_menu, "mnu_auto_options"),]),

	("game_options_injuries",[(try_begin),(neq, "$tld_option_injuries", 0),(str_store_string, s7, "@ON"),
                                  (else_try),(str_store_string, s7, "@OFF"),(try_end),
	    ],"Injuries for companions:  {s7}.",[
		(store_sub,"$tld_option_injuries",1,"$tld_option_injuries"),(val_clamp,"$tld_option_injuries",0,2),(jump_to_menu, "mnu_auto_options"),]),
 
	("game_options_death",[(try_begin),(neq, "$tld_option_death_npc", 0),(str_store_string, s7, "@ON"),
							(else_try),(str_store_string, s7, "@OFF"),(try_end),
	    ],"Permanent death for lords and companions:  {s7}.",[
	     (store_sub, "$tld_option_death_npc", 1, "$tld_option_death_npc"),(val_clamp, "$tld_option_death_npc", 0, 2),(jump_to_menu, "mnu_auto_options"),]),

	("game_options_death2",[(try_begin),(neq, "$tld_option_death_player", 0),(str_store_string, s7, "@ON"),
							(else_try),(str_store_string, s7, "@OFF"),(try_end),
	    ],"Permanent death for player (that is YOU!):  {s7}.",[
	     (store_sub, "$tld_option_death_player", 1, "$tld_option_death_player"),(val_clamp, "$tld_option_death_player", 0, 2),(jump_to_menu, "mnu_auto_options"),]),

    ("game_options_morale",[(try_begin),(eq,"$tld_option_morale",1),(str_store_string, s7, "@ON"),
									(else_try),(str_store_string, s7, "@OFF"),(try_end),
        ],"Battle morale system:  {s7}",[
        (store_sub, "$tld_option_morale", 1, "$tld_option_morale"),(val_clamp, "$tld_option_morale", 0, 2),(jump_to_menu, "mnu_auto_options"),]),

    ("game_options_animal_ambushes",[(try_begin),(eq,"$tld_option_animal_ambushes",1),(str_store_string, s7, "@ON"),
									(else_try),(str_store_string, s7, "@OFF"),(try_end),
        ],"Animal ambushes:  {s7}",[
        (store_sub, "$tld_option_animal_ambushes", 1, "$tld_option_animal_ambushes"),(val_clamp, "$tld_option_animal_ambushes", 0, 2),(jump_to_menu, "mnu_auto_options"),]),

    ("game_options_horse_ko",[	   (try_begin),(eq,"$show_mount_ko_message",2),(str_store_string, s7, "@All messages"),
									(else_try),(eq,"$show_mount_ko_message",1),(str_store_string, s7, "@Player damage only"),
									(else_try),(eq,"$show_mount_ko_message",0),(str_store_string, s7, "@No Messages"), (try_end),
        ],"Fallen rider damage messages:  {s7}",[
        (val_add, "$show_mount_ko_message", 1,),(val_mod, "$show_mount_ko_message", 3),(jump_to_menu, "mnu_auto_options"),]),


   ] + (is_a_wb_menu==1 and [

    ("game_options_bright_nights",[(try_begin),(neq, "$bright_nights", 0),(str_store_string, s7, "@ON"),
                                  (else_try),(str_store_string, s7, "@OFF"),(try_end),
	    ],"Brighter Nights:  {s7}.",[
		(store_sub,"$bright_nights",1,"$bright_nights"),(val_clamp,"$bright_nights",0,2),(jump_to_menu, "mnu_auto_options"),]),

    ("game_options_camera_pref", [	(try_begin),(eq,"$pref_cam_mode",1),(str_store_string, s7, "@Free-Mode Custom Camera"),
									(else_try),(eq,"$pref_cam_mode",2),(str_store_string, s7, "@Fixed Over-The-Shoulder Camera"),
									(else_try),(eq,"$pref_cam_mode",0),(str_store_string, s7, "@Default Camera"), (try_end),
	    ],"Preferred Camera Mode:  {s7}.",[
		 (val_add, "$pref_cam_mode", 1,),(val_mod, "$pref_cam_mode", 3),(jump_to_menu, "mnu_auto_options"),]),
	
	] or []) + [

    ("game_options_tweaks",[],"Gameplay tweaks...",[(jump_to_menu, "mnu_camp_tweaks")]),

    ("game_options_back",[(eq, "$tld_game_options", 1)],"Back to camp menu.",[(jump_to_menu, "mnu_camp")]),

    ("game_options_start_back",[(eq, "$tld_game_options", 0)],"Back.",[(jump_to_menu, "mnu_start_phase_2")]),
 ]),

( "auto_options",0,
    "This menu automatically returns to caller.",
    "none",
    [(jump_to_menu, "mnu_game_options")],[]
 ),




( "camp_tweaks",0,
	"^^^^^^^^Choose an option that you would like to adjust.","none",[],
	[
   	 	("tweak_options_compat",[],"Compatibility tweaks...",[(jump_to_menu, "mnu_camp_compat_tweaks")]),
    		("tweak_options_strat",[],"Strategy tweaks...",[(jump_to_menu, "mnu_camp_strat_tweaks")]),
    		 ] + (is_a_wb_menu==1 and [
    		("tweak_options_battlefield_ai",[],"Battlefield AI tweaks...",[(jump_to_menu, "mnu_camp_field_ai")]),
    		("tweak_options_back",[],"Back to options menu.",[(start_presentation, "prsnt_tld_mod_options")]),
    		] or [
    		("tweak_options_back",[],"Back to options menu.",[(jump_to_menu, "mnu_game_options")])
    		]) + [
    		
	]
),

( "camp_compat_tweaks",0,
	"^^^^^^^^Click on an option to change (hold shift to decrease):^(these are for compatibilty and are not cheats)","none",[],
	[	
    		("game_options_compat_party",
		[
			(assign, reg0, "$tld_option_max_parties"),
			(try_begin),
				(ge, "$tld_option_max_parties", tld_party_count_option_high_crash),
				(str_store_string, s1, "@{reg0} (will most likely cause save crashes)"),
			(else_try),
				(ge, "$tld_option_max_parties", tld_party_count_option_med_crash),
				(str_store_string, s1, "@{reg0} (could possibly cause save crashes)"),
			(else_try),
				(str_store_string, s1, "@{reg0}"),
			(try_end),
		],

		"Maximum number of parties: {s1}",
		[
			(try_begin),
				(key_is_down|this_or_next, key_left_shift),
				(key_is_down, key_right_shift),
				(val_sub, "$tld_option_max_parties", tld_party_count_option_increment),
				(try_begin),
					(lt, "$tld_option_max_parties", tld_party_count_option_min),
					(assign, "$tld_option_max_parties", tld_party_count_option_max),
				(try_end),
			(else_try),
				(val_add, "$tld_option_max_parties", tld_party_count_option_increment),
				(try_begin),
					(gt, "$tld_option_max_parties", tld_party_count_option_max),
					(assign, "$tld_option_max_parties", tld_party_count_option_min),
				(try_end),
			(try_end),
			(jump_to_menu, "mnu_auto_compat_tweak"),
		]),

    		("game_options_compat_back",[],"Back to tweaks menu.",[(jump_to_menu, "mnu_camp_tweaks")]),
	]
),

( "camp_strat_tweaks",0,
	"^^^^^^^^Click on an option to toggle:^(warning: these are cheats!)","none",[],
    [
    ("strat_tweaks_siege_reqs",[
      (try_begin),
        (eq,"$tld_option_siege_reqs",0),(str_store_string, s7, "@Normal"),
	  (else_try),
        (eq,"$tld_option_siege_reqs",1),(str_store_string, s7, "@Defender only"),
	  (else_try),
        (str_store_string, s7, "@None"),
      (try_end),
        ],"Siege strength requirements: {s7}",[
        (val_add, "$tld_option_siege_reqs", 1),
        (val_mod, "$tld_option_siege_reqs", 3),#0-2
        (jump_to_menu, "mnu_auto_strat_tweak")]), 

    ("strat_tweaks_siege_relax_rate",[
      (val_max, "$tld_option_siege_relax_rate", 50), #deals with old saves
      (assign, reg1, "$tld_option_siege_relax_rate"),
        ],"Siege str. req. relaxation rate: {reg1}",[
        (val_mul, "$tld_option_siege_relax_rate", 2),
        (try_begin),
          (eq, "$tld_option_siege_relax_rate", 400),
          (assign, "$tld_option_siege_relax_rate", 50),
        (try_end),#50, 100, 200
        (jump_to_menu, "mnu_auto_strat_tweak")]), 
        
    ("strat_tweaks_regen_rate",[
      (try_begin),
        (eq,"$tld_option_regen_rate",0),(str_store_string, s7, "@Normal"),
	  (else_try),
        (eq,"$tld_option_regen_rate",1),(str_store_string, s7, "@Halved"),
	  (else_try),
        (eq,"$tld_option_regen_rate",2),(str_store_string, s7, "@Battles only"),
	  (else_try),
        (str_store_string, s7, "@None"),
      (try_end),
        ],"Strength regen rate: {s7}",[
        (val_add, "$tld_option_regen_rate", 1),
        (val_mod, "$tld_option_regen_rate", 4), #0,1,2,3
        (jump_to_menu, "mnu_auto_strat_tweak")]), 
        
    ("strat_tweaks_siege_regen_limit",[
      (val_max, "$tld_option_regen_limit", 500), #deals with old saves
      (assign, reg1, "$tld_option_regen_limit"),
        ],"Faction strength regenerate slower at: {reg1}",[
        (val_add, "$tld_option_regen_limit", 500),
        (try_begin),
          (eq, "$tld_option_regen_limit", 2500),
          (assign, "$tld_option_regen_limit", 500),
        (try_end), #500/1000/1500/2000
        (jump_to_menu, "mnu_auto_strat_tweak")]), 

    #swy-- added these two by per khamukkamu request, they make sense:
    ("strat_tweaks_influence_gain_rate",
      [
        (try_begin),
          (eq, "$tld_option_influence_gain_rate", 0),
          (str_store_string, s7, "@Normal"),
        (else_try),
          (eq, "$tld_option_influence_gain_rate", 1),
          (str_store_string, s7, "@Doubled"),
        (else_try),
          (eq, "$tld_option_influence_gain_rate", 2),
          (str_store_string, s7, "@Tripled"),
        (else_try),
          (eq, "$tld_option_influence_gain_rate", 3),
          (str_store_string, s7, "@Quadrupled"),
        (try_end),
      ],
      "Influence gain rate: {s7}",
      [
        (val_add, "$tld_option_influence_gain_rate", 1),
        (val_mod, "$tld_option_influence_gain_rate", 4),
        (jump_to_menu, "mnu_auto_strat_tweak"),
      ]
    ), #0,1,2,3

    ("strat_tweaks_rank_gain_rate",
      [
        (try_begin),
          (eq, "$tld_option_rank_gain_rate", 0),
          (str_store_string, s7, "@Normal"),
        (else_try),
          (eq, "$tld_option_rank_gain_rate", 1),
          (str_store_string, s7, "@Doubled"),
        (else_try),
          (eq, "$tld_option_rank_gain_rate", 2),
          (str_store_string, s7, "@Tripled"),
        (else_try),
          (eq, "$tld_option_rank_gain_rate", 3),
          (str_store_string, s7, "@Quadrupled"),
        (try_end),
      ],
      "Rank gain rate: {s7}",
      [
        (val_add, "$tld_option_rank_gain_rate", 1),
        (val_mod, "$tld_option_rank_gain_rate", 4),
        (jump_to_menu, "mnu_auto_strat_tweak"),
      ]
    ), #0,1,2,3

    ("strat_tweaks_back",[],"Back to tweaks menu.",[(jump_to_menu, "mnu_camp_tweaks")]),
 ]),

( "auto_strat_tweak",0,
    "This menu automatically returns to caller.",
    "none",
    [(jump_to_menu, "mnu_camp_strat_tweaks")],[]
 ),

( "auto_compat_tweak",0,
    "This menu automatically returns to caller.",
    "none",
    [(jump_to_menu, "mnu_camp_compat_tweaks")],[]
 ),

( "auto_orc_horde_troll",0,
    "This menu automatically returns to caller.",
    "none",
    [(jump_to_menu, "mnu_orc_horde_troll")],[]
 ),
 
#-swy- Nothing leads to this menu, not even with cheats/dev thingie on, probably disabled for a good reason.
( "camp_chest_fill",0,
 "^^^^^^^^Please choose faction to get items from.",
 "none",
 [],
 [

 ("f_gondor"  ,[],"Gondor items"    ,[(call_script,"script_fill_camp_chests","fac_gondor"  ),(jump_to_menu, "mnu_camp"),]),
  ("f_rohan"   ,[],"Rohan items"     ,[(call_script,"script_fill_camp_chests","fac_rohan"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_isengard",[],"Isengard items"  ,[(call_script,"script_fill_camp_chests","fac_isengard"),(jump_to_menu, "mnu_camp"),]),
  ("f_mordor"  ,[],"Mordor items"    ,[(call_script,"script_fill_camp_chests","fac_mordor"  ),(jump_to_menu, "mnu_camp"),]),
  ("f_dwarf"   ,[],"Dwarf items"     ,[(call_script,"script_fill_camp_chests","fac_dwarf"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_lorien"  ,[],"Lothlorien items",[(call_script,"script_fill_camp_chests","fac_lorien"  ),(jump_to_menu, "mnu_camp"),]),
  ("f_woodelf" ,[],"Mirkwood items"  ,[(call_script,"script_fill_camp_chests","fac_woodelf" ),(jump_to_menu, "mnu_camp"),]),
  ("f_imladris",[],"Imladris items"  ,[(call_script,"script_fill_camp_chests","fac_imladris"),(jump_to_menu, "mnu_camp"),]),	   
  ("f_harad"   ,[],"Harad items"     ,[(call_script,"script_fill_camp_chests","fac_harad"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_khand"   ,[],"Khand items"     ,[(call_script,"script_fill_camp_chests","fac_khand"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_rhun"    ,[],"Rhun items"      ,[(call_script,"script_fill_camp_chests","fac_rhun"    ),(jump_to_menu, "mnu_camp"),]),	   
  ("f_dale"    ,[],"Dale items"      ,[(call_script,"script_fill_camp_chests","fac_dale"    ),(jump_to_menu, "mnu_camp"),]),
  ("f_umbar"   ,[],"Umbar items"     ,[(call_script,"script_fill_camp_chests","fac_umbar"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_moria"   ,[],"Moria items"     ,[(call_script,"script_fill_camp_chests","fac_moria"   ),(jump_to_menu, "mnu_camp"),]),
  ("f_gundabad",[],"Gundabad items"  ,[(call_script,"script_fill_camp_chests","fac_gundabad"),(jump_to_menu, "mnu_camp"),]),
  ("f_dunland" ,[],"Dunland items"   ,[(call_script,"script_fill_camp_chests","fac_dunland" ),(jump_to_menu, "mnu_camp"),]), 
  ("go_back"   ,[],"Go back"         ,[(jump_to_menu, "mnu_camp"),]),
 ]
 ),
( "cheat_change_race",0,
 "^^^^^Please choose your race:^^Note: You should review your character in the face generator after making this change.",
 "none",
 [],
 [
 ("race_test     " ,[],"TEST     " ,[(troop_set_type,"trp_player",16), (jump_to_menu, "mnu_camp"),]),	   
  ("race_male"      ,[],"Male"      ,[(troop_set_type,"trp_player", 0), (jump_to_menu, "mnu_camp"),]),
  ("race_female"    ,[],"Female"    ,[(troop_set_type,"trp_player", 1), (jump_to_menu,"mnu_camp"),]),
  ("race_gondor"    ,[],"Gondor"    ,[(troop_set_type,"trp_player", 2), (assign,"$players_kingdom","fac_gondor"),(jump_to_menu, "mnu_camp"),]),
  ("race_rohan"     ,[],"Rohan"     ,[(troop_set_type,"trp_player", 3), (assign,"$players_kingdom","fac_rohan"),(jump_to_menu, "mnu_camp"),]),
  ("race_dunlander" ,[],"Dunlander" ,[(troop_set_type,"trp_player", 4), (assign,"$players_kingdom","fac_dunland"),(jump_to_menu, "mnu_camp"),]),
  ("race_orc"       ,[],"Orc"       ,[(troop_set_type,"trp_player", 5), (jump_to_menu, "mnu_camp"),]),
  ("race_uruk"      ,[],"Uruk"      ,[(troop_set_type,"trp_player", 6), (jump_to_menu, "mnu_camp"),]),
  ("race_haradrim"  ,[],"Haradrim"  ,[(troop_set_type,"trp_player", 7), (jump_to_menu, "mnu_camp"),]),	   
  ("race_easterling",[],"Easterling",[(troop_set_type,"trp_player", 8), (jump_to_menu, "mnu_camp"),]),
  ("race_dwarf"     ,[],"Dwarf"     ,[(troop_set_type,"trp_player", 9), (jump_to_menu, "mnu_camp"),]),
  ("race_troll"     ,[],"Troll"     ,[(troop_set_type,"trp_player",10), (jump_to_menu, "mnu_camp"),]),	   
  ("race_dunedain"  ,[],"Dunedain"  ,[(troop_set_type,"trp_player",11), (jump_to_menu, "mnu_camp"),]),
  ("race_lothlorien",[],"Lothlorien",[(troop_set_type,"trp_player",12), (jump_to_menu, "mnu_camp"),]),
  ("race_rivendell" ,[],"Rivendell" ,[(troop_set_type,"trp_player",13), (jump_to_menu, "mnu_camp"),]),
  ("race_mirkwood"  ,[],"Mirkwood"  ,[(troop_set_type,"trp_player",14), (jump_to_menu, "mnu_camp"),]),
  ("race_evil_male" ,[],"Evil Male" ,[(troop_set_type,"trp_player",15), (jump_to_menu, "mnu_camp"),]),
  ("go_back"        ,[],"Go back"   ,[(jump_to_menu, "mnu_camp_cheat"),]),
 ]),  
 
("camp_action",0,
  "^^^^^^^^^     Which object?", "none",
 [(set_background_mesh, "mesh_ui_default_menu_window"),],
 [ 

#    ("camp_customize_defilement",
#		[
#			# (CppCoder) Only evil players can do this, though only evil players should be able to aqquire the items anyway.
#			(eq, cheat_switch, 1),
#			(neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
#			(troop_has_item_equipped|this_or_next, "trp_player", "itm_defiled_armor_gondor"),
#			(troop_has_item_equipped|this_or_next, "trp_player", "itm_defiled_armor_rohan"),
#			(troop_has_item_equipped, "trp_player", "itm_defiled_armor_dale"),
#		],
#		"Customize Defiled Armor",
#		[			
#			(try_for_range, ":item_id", defiled_items_begin, defiled_items_end),
#				(troop_has_item_equipped, "trp_player", ":item_id"), # (CppCoder) Must be done for efficiency's sake
#				(assign, "$g_defiled_armor_item", ":item_id"),
#			(try_end),
#			(start_presentation, "prsnt_customize_defilement"),
#		]
#	),

    ("camp_drink_water",
		[
			(player_has_item,"itm_ent_water"),
			(eq,"$g_ent_water_ever_drunk",0), # can drink only if never before
		],
		"Drink the Ent Water!",
		[
	    (troop_get_type,reg5,"trp_player"),
	    (troop_remove_item,"itm_ent_water"),
		(display_log_message,"@You drank the Ent Water..."),
		(assign,"$g_ent_water_ever_drunk",1),
		(assign,"$g_ent_water_taking_effect",1),
		(try_begin),
			(neg|is_between,reg5,tf_orc_begin, tf_orc_end),
			(jump_to_menu,"mnu_drank_ent_water_human"),
		(else_try),
			(jump_to_menu,"mnu_drank_ent_water_orc"),
		(try_end),
		]
	),

    ("camp_drink_orc_brew",
        [
            (player_has_item, "itm_orc_brew"),
            (item_slot_eq, "itm_orc_brew", slot_item_is_active, 0),
        ],
        "Pass around the Orc Brew!",
        [
        # Orc brew will be active until:
        (store_current_hours, ":now_hours"),
        (store_add, ":then_hours", ":now_hours", 7*24),
        (item_set_slot, "itm_orc_brew", slot_item_is_active, 1),
        (item_set_slot, "itm_orc_brew", slot_item_deactivation_hour, ":then_hours"),

        (display_log_message, "@You used the Orc Brew."),
        (jump_to_menu, "mnu_camp"),
        ]
    ),


    # ("camp_recruit_prisoners",
       # [(troops_can_join, 1),
        # (store_current_hours, ":cur_time"),
        # (val_sub, ":cur_time", 24),
        # (gt, ":cur_time", "$g_prisoner_recruit_last_time"),
        # (try_begin),
          # (gt, "$g_prisoner_recruit_last_time", 0),
          # (assign, "$g_prisoner_recruit_troop_id", 0),
          # (assign, "$g_prisoner_recruit_size", 0),
          # (assign, "$g_prisoner_recruit_last_time", 0),
        # (try_end),
        # ], "Recruit some of your prisoners to your party.",[(jump_to_menu, "mnu_camp_recruit_prisoners"),],
	# ),
	
    #("action_read_book",[],"Select a book to read.",[(jump_to_menu, "mnu_camp_action_read_book"),]),
	
    #("action_modify_banner",[(eq, "$cheat_mode", 1)],"Cheat: Modify your banner.",
    #                                               [(start_presentation, "prsnt_banner_selection"), #(start_presentation, "prsnt_custom_banner"),
    #                                                ]),
    #("action_retire",[],"Retire from adventuring.",[(jump_to_menu, "mnu_retirement_verify"),]),
	
    ("camp_action_4",[],"Back.",[(jump_to_menu, "mnu_camp"),]),
   ]
 ),
################################ CHEAT/MODDING MENU END ########################################  

##     #TLD - assasination menus begin (Kolba)
( "assasins_attack_player_won",mnf_disable_all_keys,
    "You have successfully defeated assassins from {s2}, sent by {s3}.",
    "none",
    [#add prize
		#(call_script,"script_troop_add_gold","trp_player",100),#add gold
        (call_script, "script_add_faction_rps", "$ambient_faction", 100),
		(add_xp_to_troop,1000,"trp_player"),#add exp
		
		(troop_get_slot,":faction","trp_temp_array_a",0),#get number of enemy faction, which organised assasination
		(str_store_faction_name,s2,":faction"),#save faction name
		(faction_get_slot,":leader",":faction",slot_faction_leader),#get faction leader
		(str_store_troop_name,s3,":leader"),#save faction leader name
		],
    [("continue",[],"Continue...",[(leave_encounter),(change_screen_return)])],
 ),
( "assasins_attack_player_retreat",mnf_disable_all_keys,
  "You escaped with your life!",
    "none",
    [#add here any consequences of retreat
	],
    [("continue",[],"Continue...",[(leave_encounter),(change_screen_return)])],
 ),
# what is this? a cut and paste version of defeat? plase merge code rather than cutting and pasting. --- mtarini
( "assasins_attack_player_defeated",0,
    "You should not be reading this...",
    "none",
    [	# (troop_get_type, ":is_female", "trp_player"),
		# (try_begin),
			# (eq, ":is_female", 1),
			# (set_background_mesh, "mesh_pic_prisoner_fem"),
		# (else_try),
			# (set_background_mesh, "mesh_pic_prisoner_man"),
		# (try_end),
		
		#consequences of defeat
		(play_track,"track_captured",1),#music
		
		(troop_get_slot,":faction","trp_temp_array_a",0),#get number of assasin's faction
		(str_store_faction_name,s2,":faction"),#save it
		(faction_get_slot,":leader",":faction",slot_faction_leader),#get faction leader
		(str_store_troop_name,s3,":leader"),#save it
		
		(assign,"$capturer_party",1),
		
		#(troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
		(assign,":end",centers_end),#breaking control flow
		(try_for_range,":center",centers_begin,":end"),
            (party_is_active, ":center"), #TLD
	        (party_slot_eq, ":center", slot_center_destroyed, 0), #TLD
			(party_get_slot,":owner",":center",slot_town_lord),
			(eq,":owner",":leader"),
			(assign,"$capturer_party",":center"),#prison for player
			(assign,":end",centers_begin),#ending control flow
		(try_end),
		
		#freeing player's prisoners
		(party_get_num_prisoner_stacks,":num_prisoner_stacks","p_main_party"),
		(try_for_range,":stack_no",0,":num_prisoner_stacks"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
			(troop_is_hero,":stack_troop"),
			(call_script,"script_remove_troop_from_prison",":stack_troop"),
		(try_end),
		
		(call_script,"script_loot_player_items","$g_enemy_party"),#player loose some equipment
		
		(assign,"$g_move_heroes",0),
		(party_clear, "p_temp_party"),
		
		(store_faction_of_party, ":fac","$g_enemy_party"),
		(party_set_faction, "p_temp_party", ":fac"), # mtarini: need this 
		
		(call_script, "script_party_add_party_prisoners", "p_temp_party", "p_main_party"),
		(call_script, "script_party_prisoners_add_party_companions", "p_temp_party", "p_main_party"),
		(distribute_party_among_party_group, "p_temp_party","$capturer_party"),
		
		(call_script,"script_party_remove_all_companions","p_main_party"),#removing all troops
		(assign, "$g_move_heroes",1),
		(call_script,"script_party_remove_all_prisoners","p_main_party"),#removing all prisoners
		
		#setting captivity
		(assign,"$g_player_is_captive",1),
		(assign,"$auto_menu",-1),
		

		#(set_camera_follow_party,"$capturer_party"),#camera
		#(store_random_in_range,":random_hours",30,60),#random time of captivity
		#(call_script,"script_event_player_captured_as_prisoner"),
		#(call_script,"script_stay_captive_for_hours",":random_hours"),
		#(assign,"$auto_menu","mnu_assasins_attack_captivity_check"),
		
		(assign, "$recover_after_death_menu", "mnu_recover_after_death_default"),
		(jump_to_menu, "mnu_tld_player_defeated"),
		
		],
    [
      # ("continue",[],"Continue...",[(leave_encounter),(change_screen_return)]),
    ],
  ),
#TLD - assasination menus end (Kolba)
 
################################ FANGORN MENU START ########################################
( "fangorn_danger",0, # player face fangor dangers
   "^^^^^^Strange, threatening noises all around you.^Are the trees talking? There's a sense of deep anger and pain in the air.^Your orders?",
   "none",
   [(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_fangorn"), (set_background_mesh, reg10),
    (troop_get_type,reg5,"trp_player"),
    
    #swy-- added unused merlkir illustration here... it looks cool!
    (eq, "$player_looks_like_an_orc", 1),
    (set_background_mesh, "mesh_draw_lorien_magic"),

    ],
   [("be_quiet_elf",
	 [(is_between,reg5,tf_elf_begin, tf_elf_end)], "Respect the hatred of the trees. Move along quietly.",
	 [(assign,"$g_fangorn_rope_pulled", -100), # disable fangorn menu from now on
	  (change_screen_map),
	 ]),
   ("be_quiet",
	 [(neg|is_between,reg5,tf_orc_begin, tf_orc_end),# no orc can do this
	  (neg|is_between,reg5,tf_elf_begin, tf_elf_end) # no elf can do this
	 ],
	 "Put the weapons down and stay quiet! Now out of here!",
	 [(val_add,"$g_fangorn_rope_pulled", 5), 
	  (val_clamp,"$g_fangorn_rope_pulled", 0,65), 
	  (call_script,"script_fangorn_deal_damage","p_main_party"),
	  (call_script,"script_after_fangorn_damage_to_player"),
	 ]
    ),
   ("be_bold",
	 [(neg|is_between,reg5,tf_elf_begin, tf_elf_end)], # no elf can do this
	 "Go on! I'm not afraid of plants or old myths!",
	 [(val_add,"$g_fangorn_rope_pulled", 30), 
	  (val_clamp,"$g_fangorn_rope_pulled", 0,75), 
	  (call_script,"script_fangorn_deal_damage","p_main_party"),
	  (call_script,"script_after_fangorn_damage_to_player"),
	 ]),
   ("fight_back",
	 [
	 (this_or_next|is_between,reg5,tf_orc_begin, tf_orc_end) ,# orcs olny option
	 (check_quest_active, "qst_investigate_fangorn"), #  or also whoever was given the quest to investigate can...
	 ]
	 ,"Let's find out! Search the area! Burn down a tree or two!",
	 [(store_random_in_range,":chance",0,100),
	  (try_begin),
	    (lt,":chance",60),
		(call_script,"script_fangorn_fight_ents"),
	(else_try),
		(val_add,"$g_fangorn_rope_pulled", 30), 
		(val_clamp,"$g_fangorn_rope_pulled", 0,75), 
		(display_message,"@Fangorn search: failed."),
		(jump_to_menu, "mnu_fangorn_search_fails"),
	  (try_end),
	  #(change_screen_map),
	 ]),
   ]
 ),
( "fangorn_search_fails",0, # (orc) player searched fangorn but found nothing
   "^^^^^^You search the dark, thick forest but find nothing.^Still, you feel observed and threatened, more and more.",
   "none",[(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_fangorn"), (set_background_mesh, reg10),],[
    ("continue",[],"Continue...",
	 [(call_script,"script_fangorn_deal_damage","p_main_party"),
	  (call_script,"script_after_fangorn_damage_to_player"),
	 ]),
   ]
 ),
( "fangorn_battle_debrief",0, # player faced fangor dangers. Did he win?
    "you shouldn't be reading this",
	"none",[
		(try_begin),
			(eq, "$g_battle_result", 1),
			(assign,"$g_fangorn_rope_pulled", 0), # ents calm down after a good fight
			(jump_to_menu, "mnu_fangorn_battle_debrief_won"),
		(else_try),
			(assign, "$recover_after_death_menu", "mnu_recover_after_death_fangorn"),
		#	(jump_to_menu, "mnu_tld_player_defeated"),
			(jump_to_menu, "mnu_fangorn_battle_debrief_won"),
		(try_end),
	 ],[]
 ),
( "fangorn_battle_debrief_won",0, # player faced fangor dangers, and won!
    "{s55}",
	"none",[		
		(try_begin),
			(eq, "$g_battle_result", 1),
			(str_store_string, s55, "@^^^A great victory!^^^So this is what all the myths about Fangorn meant..."),
		(else_try),
			(neq, "$g_battle_result", 1),
			(str_store_string, s55, "@^^^Defeated...^^^Scattered in the Fangorn Forest... Alone..."),
		(try_end),],[
	("continue",[

		(try_begin),
			(eq, "$g_battle_result", 1),
			(assign,"$g_fangorn_rope_pulled", 0), # ents calm down after a good fight
			(str_store_string, s55, "@^^^A great victory!^^^So this is what all the myths about Fangorn meant..."),
			(check_quest_active, "qst_investigate_fangorn"),
			(neg|check_quest_succeeded, "qst_investigate_fangorn"),
			(neg|check_quest_failed, "qst_investigate_fangorn"),
			(call_script, "script_succeed_quest", "qst_investigate_fangorn"),
			(troop_add_item, "trp_player", "itm_ent_water", 0), #MV: reward for defeating the Ents
		(else_try),
			(eq, "$g_battle_result", 1),
			(neg|check_quest_active, "qst_investigate_fangorn"),
			(str_store_string, s55, "@^^^A great victory!^^^So this is what all the myths about Fangorn meant..."),
		(else_try),
			(neq, "$g_battle_result", 1),
			(assign, "$recover_after_death_menu", "mnu_recover_after_death_fangorn"),
			(str_store_string, s55, "@^^^Defeated...^^^Scattered in the Fangorn Forest... Alone..."),
		#	(jump_to_menu, "mnu_tld_player_defeated"),
			(jump_to_menu, "mnu_auto_return_to_map"),
		(try_end),

	],"Continue...",[
		(change_screen_map),
	]),
 ]),
( "fangorn_killed_player_only",0, # player only was killed by fangorn
   "^^^^^^You wander in the thick, dark forest.^All of a sudden you are hit by something! Maybe a heavy branch fell on your head?^You stay unconcious only for minutes. You are badly hurt but you can go on.",
   "none",[(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_fangorn"), (set_background_mesh, reg10),],
		[("ow_get_out",[],"Ouch! Let's get out of this cursed place!",[(jump_to_menu,"mnu_auto_return_to_map")] ),]
 ),
( "fangorn_killed_troop_and_player",0, # player and troops were killed by fangorn
   "^^^^^^You wander in the thick, dark forest.^^All of a sudden you are hit by something! Maybe a heavy branch fell on your head.^^When you recover, minutes later, you find that not all of your troops were that lucky.^^",
   "none",[(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_fangorn"), (set_background_mesh, reg10),],
   [("ow_get_out",[],"Ouch! Let's get out of this cursed place!",[(jump_to_menu,"mnu_auto_return_to_map")] ),]
 ),
( "fangorn_killed_troop_only",0, # troops were killed by fangorn
   "^^^^^^^^You wander in the thick, dark forest. Your troops are fearful.^^All of a sudden, you hear screams from the rear! You hurry back, only to find a few of your troops on the ground, in a pool of blood.^^A few others are nowhere to be found...",
   "none",[(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_fangorn"), (set_background_mesh, reg10),],
   [("get_out",[],"Let's get out of this cursed place!",[(jump_to_menu,"mnu_auto_return_to_map")] ),]
 ),

#### CAPTURE TROLL MENU
( "can_capture_troll",0,"The downed wild troll still breaths!^^Its evil eyes stare at you filled with pain and rage.^Even now that it has been taken down, and lies helpless in a pool of its blood, it looks tremendously dangerous...",
  "none",[(set_background_mesh, "mesh_draw_wild_troll")], [
	("killit",[],"Dispatch it, now. Make sure it dies.",[(jump_to_menu,"$g_next_menu")],),
	("cageit1",[
	  (player_has_item,"itm_wheeled_cage"),(troops_can_join_as_prisoner,1),
	  (party_count_prisoners_of_type, ":num_trolls", "p_main_party", "trp_wild_troll"),(eq, ":num_trolls", 0),
	 ],
	 "Cage it and drag it around.",[
      (party_add_prisoners, "p_main_party", "trp_wild_troll", 1),
	  (display_message,"@Troll caged in wheeled cage."),
      (jump_to_menu,"$g_next_menu")],
	),
	("cageit2",[ # capture a second troll as prisoner
	   (player_has_item,"itm_wheeled_cage"),(troops_can_join_as_prisoner,1),
	   (party_count_prisoners_of_type, ":num_trolls", "p_main_party", "trp_wild_troll"),(eq, ":num_trolls", 1),
	],"Cage it together with the other troll.",[
      (party_add_prisoners, "p_main_party", "trp_wild_troll", 1),
	  (display_message,"@A second troll is caged in wheeled cage."),
      (jump_to_menu,"$g_next_menu")],
	),
  ]
 ),
  
################################ CHEAT/MODDING MENU START ########################################
# Find and grab item cheat

("cheat_find_item",0,
"{!}Current item range: {reg5} to {reg6}",
"none",
[ (set_background_mesh, "mesh_ui_default_menu_window"),
  (assign, reg5, "$cheat_find_item_range_begin"),
  (store_add, reg6, "$cheat_find_item_range_begin", max_inventory_items),
  (val_min, reg6, "itm_save_compartibility_item10"),
  (val_sub, reg6, 1),
],
[
  ("cheat_find_item_next_range",[], "{!}Move to next item range.",
    [
      (val_add, "$cheat_find_item_range_begin", max_inventory_items),
      (try_begin),
        (ge, "$cheat_find_item_range_begin", "itm_save_compartibility_item10"),
        (assign, "$cheat_find_item_range_begin", 0),
      (try_end),
      (jump_to_menu, "mnu_cheat_find_item"),
    ]
  ),
  
  ("cheat_find_item_choose_this",[], "{!}Choose from this range.",
    [
      (troop_clear_inventory, "trp_dormant"),
      (store_add, ":max_item", "$cheat_find_item_range_begin", max_inventory_items),
      (val_min, ":max_item", "itm_save_compartibility_item10"),
      (store_sub, ":num_items_to_add", ":max_item", "$cheat_find_item_range_begin"),
      (try_for_range, ":i_slot", 0, ":num_items_to_add"),
        (store_add, ":item_id", "$cheat_find_item_range_begin", ":i_slot"),
        (troop_add_items, "trp_dormant", ":item_id", 1),
      (try_end),
      (change_screen_trade, "trp_dormant"),
    ]
  ),
  ("camp_action_4_cheat",[],"{!}Back to cheat menu.",
    [(jump_to_menu, "mnu_camp_cheat"),
    ]
  ),
]
),

# free magic item cheat (mtarini)   
("cheat_free_magic_item",0,"Which free magic item do you want?","none",[(set_background_mesh, "mesh_ui_default_menu_window")],
   [ ("cheat_free_magic_item_back",[],"Back",[(jump_to_menu, "mnu_camp_cheat")]), ]
   +
   [ ("mi20",[(neg|player_has_item,x),(str_store_item_name,s20,x)],"{s20}",[(troop_add_item ,"trp_player",x),(display_message, "@Here you are."),]) 
	for x in magic_items ]
 ),
# choose quest cheat (mtarini)
("cheat_impose_quest",0,"Current imposed quest:^{s20}^^Which quest do you want to impose?^(no other quests will be given)","none",[
    (set_background_mesh, "mesh_ui_default_menu_window"),
    (try_begin),(ge,"$cheat_imposed_quest",0),(str_store_quest_name,s20,"$cheat_imposed_quest"),(else_try),(str_store_string,s20,"@None"),(try_end),
  ],[
	("just_back",[],"Back",[(jump_to_menu, "mnu_camp_cheat")]),
	("none",[],"None",[(assign,"$cheat_imposed_quest",-1),(jump_to_menu, "mnu_cheat_impose_quest")]),
	("cheat_kill_quest",[],"qst_troublesome_bandits",[(assign,"$cheat_imposed_quest","qst_troublesome_bandits")]),
	("cheat_kill_faction_quest",[],"Kill GuildMaster Bandit Quest",[(assign,"$cheat_imposed_quest","qst_blank_quest_17")]),
	("cheat_raise_troops",[],"Raise Troops",[(assign,"$cheat_imposed_quest","qst_raise_troops")]),
	("cheat_defend_refugees",[],"Defend Refugees",[(assign,"$cheat_imposed_quest","qst_blank_quest_01")]),
	("cheat_attack_refugees",[],"Hunt Down Refugees",[(assign,"$cheat_imposed_quest","qst_blank_quest_02")]),
	("night_bandits",[],"Night Bandits",[(assign,"$cheat_imposed_quest","qst_deal_with_night_bandits")]),
	("spears",[],"Lost Spears",[(assign,"$cheat_imposed_quest","qst_find_lost_spears")]),
	("scout_camp", [], "Destroy Scout Camp", [(assign, "$cheat_imposed_quest", "qst_destroy_scout_camp")]),
	("defend_village", [], "Investigate Fangorn", [(assign, "$cheat_imposed_quest", "qst_investigate_fangorn")]),
	("raid_village", [], "Raid Village", [(assign, "$cheat_imposed_quest", "qst_raid_village")]),
    ("eliminate_patrols", [], "Defeat Target Lord", [(assign, "$cheat_imposed_quest", "qst_blank_quest_06")]),
    ("eliminate_troll", [], "Dispatch Troll", [
    	(try_begin),
    		(store_faction_of_party, ":fac", "p_main_party"),
    		(faction_slot_eq, ":fac",slot_faction_side, faction_side_good),
    		(assign, "$cheat_imposed_quest", "qst_kill_troll"),
    	(else_try),
    		(assign, "$cheat_imposed_quest", "qst_capture_troll"),
    	(try_end)
    ])
    ]+[("mi21",[(str_store_quest_name,s21,x)],"{s21}",[(assign,"$cheat_imposed_quest",x),(jump_to_menu, "mnu_cheat_impose_quest")]) for x in range(qst_quests_end) ]+[
  ]),
  
  ### CHOSE TOWN WHERE TO RELOCATE PART 2: chose city (mtarini)
  ("teleport_to_town_part_two",0,"^^^^^^^^Ride Shadowfax:^to which city inside {s11}?","none",[(set_background_mesh, "mesh_ui_default_menu_window")],
  concatenate_scripts([[
  (
	"go_to_town_",
	[
	(store_faction_of_party, ":fact", center_list[y][0]),
	(eq, ":fact", "$teleport_menu_chosen_faction"),
	(str_store_party_name, s10, center_list[y][0]),],
	"{s10}.",
	[
		(str_store_party_name, s10, center_list[y][0]),
		(display_message, "@Player was moved to {s10}."),
		(party_relocate_near_party, "p_main_party", center_list[y][0], 3),
		(jump_to_menu, "mnu_camp"),
    ]
  )
  ]for y in range(len(center_list)) ])
  +[
  ("another_kingdom",[],"No, Another Kingdom",[(jump_to_menu, "mnu_teleport_to_town"),]),	   
 ]),
# CHOSE TOWN WHERE TO RELOCATE PART 1: chose faction (mtarini)
( "teleport_to_town",0,"^^^^^^^^Ride Shadowfax:^to which kingdom?","none",[(set_background_mesh, "mesh_ui_default_menu_window"),],
  concatenate_scripts([[
  (
	"go_to_town",
	[
	(str_store_faction_name, s10, faction_init[y][0]),
	(eq, "$teleport_menu_chosen_faction_group", y/7),],
	"{s10}.",
	[
		(assign, "$teleport_menu_chosen_faction", faction_init[y][0]),
		(jump_to_menu, "mnu_teleport_to_town_part_two"),
		(str_store_faction_name, s11, faction_init[y][0])
    ]
  )
  ]for y in range(len(faction_init)) ])
  +[
	("teleport_neutrals",[(eq, "$teleport_menu_chosen_faction_group", 2),],"Others/neutrals",[
		(assign, "$teleport_menu_chosen_faction", -1),
		(str_store_string, s11, "@neutral whereabouts"),
		(jump_to_menu, "mnu_teleport_to_town_part_two"),
	]),
	("teleport_others_factions",[(store_add, reg5, "$teleport_menu_chosen_faction_group", 1),],"More... ({reg5}/3)",[
		(try_begin),
			(eq, "$teleport_menu_chosen_faction_group", 2),
			(assign, "$teleport_menu_chosen_faction_group", 0),
		(else_try),
			(store_add, "$teleport_menu_chosen_faction_group", "$teleport_menu_chosen_faction_group", 1),
		(try_end),
		(jump_to_menu, "mnu_teleport_to_town"),
	]),
	("teleport_back",[],"Back to camp menu.",[(jump_to_menu, "mnu_camp"),]),
 ]),
### A MENU TO SELECT ANY TROOP (mtarini)
( "select_any_troop",0,
  "Select troops:^^^Current search parameters:^Faction: {s10}^Race: {s13}^Tier: {s11}^{s12}","none",
  code_to_set_search_string+[
  (assign,"$tmp_menu_entry_n",0),
  (assign,"$tmp_menu_skipped",0),
  ],
  [
  ]+concatenate_scripts([[
     ("trp",[ 
		(lt,"$tmp_menu_entry_n",tmp_menu_steps),
		
		(store_character_level, reg11, y),
		(store_div, reg14, reg11, 10),
		(this_or_next|eq, reg14, "$menu_select_any_troop_search_tier"),
		(eq, "$menu_select_any_troop_search_tier", tmp_menu_max_tier+1),
		
		(assign, ":ok", 1),
		(try_begin), (eq,"$menu_select_any_troop_search_hero", 0), 
			(try_begin),(troop_is_hero, y), (assign, ":ok", 0),(try_end),	
		(else_try),  (eq,"$menu_select_any_troop_search_hero", 1), 
			(try_begin),(neg|troop_is_hero, y), (assign, ":ok", 0),(try_end),	
		(try_end),		
		(eq, ":ok", 1),
		
		(store_troop_faction, reg12, y),
		(this_or_next|eq, reg12, "$menu_select_any_troop_search_fac"),
		(eq, "$menu_select_any_troop_search_fac", tmp_menu_max_fac+1),
		
		(troop_get_type, reg13, y),
		(this_or_next|eq, reg13, "$menu_select_any_troop_search_race"),
		(eq, "$menu_select_any_troop_search_race", len(race_names)),
		
		
		(val_add,"$tmp_menu_skipped",1),
		(gt,"$tmp_menu_skipped" , "$add_troop_menu_index"),
		(val_add,"$tmp_menu_entry_n",1),
		(str_store_troop_name, s11, y),
	 ],
	 "{s11} (lvl:{reg11})",
	 [ (try_begin), (eq, "$select_any_troop_add_selected_troops",1), (troop_join, y ),
	   (else_try), (assign, "$select_any_troop_result" , y), (jump_to_menu, "$select_any_troop_nextmenu"), (try_end),
	 ]
	 )
  ]for y in range(5,tmp_max_troop+1) ])
  +[
  ("prev_page" ,[],"[Prev Page]" ,[(val_sub, "$add_troop_menu_index", tmp_menu_steps),(val_max,  "$add_troop_menu_index", 0),(jump_to_menu, "mnu_select_any_troop"),]), 
  ("next_page" ,[],"[Next Page]" ,[(val_add, "$add_troop_menu_index", tmp_menu_steps), (jump_to_menu, "mnu_select_any_troop"),]), 
  ("opt" ,[],"[Search Option]" ,[(jump_to_menu, "mnu_select_any_troop_setup_search"),]), 
  ("done"   ,[ (eq, "$select_any_troop_add_selected_troops",1) ],"[Done]" ,[(jump_to_menu, "$select_any_troop_nextmenu"),]), 
  ("cancel"   ,[ (eq, "$select_any_troop_add_selected_troops",0) ],"[Cancel]" ,[(assign, "$select_any_troop_result" , -1), (jump_to_menu, "$select_any_troop_nextmenu"),]), 
 ]),
### ADD TROOPS CHEAT PART 2 (mtarini)
( "select_any_troop_setup_search",0,
  "Add troops: setup search parameters^^^Current parameters:^Faction: {s10}^Race: {s13}^Tier: {s11}^{s12}","none",
  code_to_set_search_string,
  [
	("one" ,[],"[Change Tier]" ,[
		(val_add, "$menu_select_any_troop_search_tier", 1),
		(try_begin) , (ge, "$menu_select_any_troop_search_tier", tmp_menu_max_tier+2), (assign, "$menu_select_any_troop_search_tier", 0), (try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
	]), 
	("facup" ,[],"[Prev Faction]" ,[
		(val_sub, "$menu_select_any_troop_search_fac", 1),
		(try_begin) , (eq, "$menu_select_any_troop_search_fac", -1), (assign,"$menu_select_any_troop_search_fac", tmp_menu_max_fac+1), (try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
	]), 
	("facdown" ,[],"[Next Faction]" ,[
		(val_add, "$menu_select_any_troop_search_fac", 1),
		(try_begin) , (ge, "$menu_select_any_troop_search_fac", tmp_menu_max_fac+2), (assign,"$menu_select_any_troop_search_fac", 0), (try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
	]), 

	("raceup" ,[],"[Prev Race]" ,[
		(val_sub, "$menu_select_any_troop_search_race", 1),
		(try_begin), (eq, "$menu_select_any_troop_search_race", -1), (assign,"$menu_select_any_troop_search_race", len(race_names)), (try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
	]), 
	("racedown" ,[],"[Next Race]" ,[
		(val_add, "$menu_select_any_troop_search_race", 1),
		(try_begin), 
			(ge, "$menu_select_any_troop_search_race", len(race_names)+1), 
			(assign,"$menu_select_any_troop_search_race", 0),
		(try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
	]), 
	("three" ,[],"[Regulars or Heroes]" ,[
		(val_add, "$menu_select_any_troop_search_hero", 1),
		(try_begin), 
			(eq, "$menu_select_any_troop_search_hero", 3), 
			(assign,"$menu_select_any_troop_search_hero", 0), 
		(try_end),
		(jump_to_menu, "mnu_select_any_troop_setup_search"),
		]), 

	("done"   ,[],"[Done]" ,[(assign, "$add_troop_menu_index", 0),(jump_to_menu, "mnu_select_any_troop"),]), 
 ]),
( "camp_cheat",0,
   "Other Cheats Menu (for development use):^^This menu is intended for development use while we are working on improving this mod. If you enable this option then additonal CHEAT menu's will also appear in other game menu's. Please do not report any bugs with this functionality since it is for testing only.",
   "none",
	[(set_background_mesh, "mesh_ui_default_menu_window"),
	 (call_script, "script_determine_what_player_looks_like"), # if back from change race
	],
	[
 	 ("cheat_disabable",[],
		"Disable cheat/modding options.",[(assign, "$cheat_mode", 0),	(jump_to_menu, "mnu_camp"),]),

	("camp_cheat_find_item",[], "Find an item...",[(jump_to_menu, "mnu_cheat_find_item")]),

	("crossdressing", [(assign,reg6, "$tld_option_crossdressing"), ], "Crossdressing: {reg6?Enabled:Disabled}", 
	  [(store_sub, "$tld_option_crossdressing", 1, "$tld_option_crossdressing"), (jump_to_menu, "mnu_camp_cheat"),]),

	("cheat_change_race",[],"Change your race (for development use).",[(jump_to_menu, "mnu_cheat_change_race"),]),	   
	("impose_quest", [], "Impose a quest...",  [(jump_to_menu, "mnu_cheat_impose_quest")]),
	("relocate_party", [],   "Move to town...", [(jump_to_menu, "mnu_teleport_to_town")]),
	("add_troops", [], "Add troops to player party.", [
	   (assign, "$select_any_troop_nextmenu","mnu_camp_cheat" ), 
	   (assign, "$select_any_troop_add_selected_troops",1 ), 
	   (jump_to_menu, "mnu_select_any_troop") 
	 ]),
	("cheat_get_item", [], "Gain a free magic item", [(jump_to_menu, "mnu_cheat_free_magic_item")]),
	("cheat_add_xp", [], "Add 1000 experience to player.", [(add_xp_to_troop, 1000, "trp_player"), (display_message, "@Added 1000 experience to player."), ]),	  	
    ("camp_mod_2",    [],
      "Raise player's attributes, skills, and proficiencies.",
      [ #attributes
         (troop_raise_attribute, "trp_player",ca_intelligence,20),
         (troop_raise_attribute, "trp_player",ca_strength,20),
		 (troop_raise_attribute, "trp_player",ca_agility,20),
		 (troop_raise_attribute, "trp_player",ca_charisma,20),
		 #skills
         (troop_raise_skill, "trp_player",skl_riding,10),
		 (troop_raise_skill, "trp_player",skl_shield,5),		#there is a bug in M&B 1.x where the shield skill helps out the other team so don't raise it too high
         (troop_raise_skill, "trp_player",skl_spotting,10),
         (troop_raise_skill, "trp_player",skl_pathfinding,10),
         (troop_raise_skill, "trp_player",skl_trainer,10),
         (troop_raise_skill, "trp_player",skl_leadership,10),
         (troop_raise_skill, "trp_player",skl_trade,10),
         (troop_raise_skill, "trp_player",skl_prisoner_management,10),
		(troop_raise_skill, "trp_player", skl_athletics, 10),
		(troop_raise_skill, "trp_player", skl_power_strike, 10),
		(troop_raise_skill, "trp_player", skl_power_draw, 10),
		(troop_raise_skill, "trp_player", skl_power_throw, 10),
		(troop_raise_skill, "trp_player", skl_weapon_master, 10),
		(troop_raise_skill, "trp_player", skl_horse_archery, 10),
		(troop_raise_skill, "trp_player", skl_ironflesh, 10),
		(troop_raise_skill, "trp_player", skl_inventory_management, 10),
	
		#proficiencies
		(troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_polearm, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_archery, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_crossbow, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_throwing, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_firearm, 350),	 
		 
         (display_message, "@Attributes, skills and proficiencies raised."),
        ]
      ),      

     ("camp_mod_3",   [],
      "Add gear and gold to player.",
       [(troop_add_gold, "trp_player", 10000),
   
#		(troop_add_item, "trp_player","itm_mail_hauberk",0),
		(troop_add_item, "trp_player","itm_mail_mittens",0),
#		(troop_add_item, "trp_player","itm_mail_boots",0),
#		(troop_add_item, "trp_player","itm_shield_heater_c",0),
#		(troop_add_item, "trp_player","itm_bastard_sword_a",0),
		(troop_add_item, "trp_player","itm_gondor_bow",0),
		(troop_add_item, "trp_player","itm_arrows",0),		
#		(troop_add_item, "trp_player","itm_wargarmored_1c",0),		
		(troop_equip_items, "trp_player"),
		
        (troop_add_item, "trp_player","itm_arrows",0),
		(troop_add_item, "trp_player","itm_dried_meat",0),
		(troop_add_item, "trp_player","itm_tools",0),
		
	    (display_message, "@Items added to player inventory."),
        ]
       ),	  
	  
      #("camp_mod_1",   [],
	  #"Increase relations with all Factions.",
#       [(try_for_range,":faction",kingdoms_begin,kingdoms_end),
#		   (call_script, "script_set_player_relation_with_faction", ":faction", 40),
        #(try_end),
		#(display_message, "@Increased relations with all factions."),
        #]
       #),
	   
      #("camp_mod_1b", [],
	  #"Decrease relations with all Factions.",
#       [(try_for_range,":faction",kingdoms_begin,kingdoms_end),
#		   (call_script, "script_set_player_relation_with_faction", ":faction", -40),
        #(try_end),
		#(display_message, "@Decreased relations with all factions."),
        #]),	   

      ("camp_mod_4",   [],
      "Spawn a looter party nearby.",
      [  (spawn_around_party, "p_main_party", "pt_looters"),
         (display_message, "@Looter party was spawned nearby."),
      ]),
	  
      ("camp_mod_5",   [],
      "Fill merchants with faction stuff",
      [(call_script,"script_fill_merchants_cheat"),(display_message,"@DEBUG: Smiths just got stuffed!"),(jump_to_menu, "mnu_camp"),]),

	 #("test1",[],"Test: pay upkeep now", [(call_script,"script_make_player_pay_upkeep")]),
	 #("test2",[],"Test: make unpaid troop leave now", [(call_script, "script_make_unpaid_troop_go")]),
	 ("cheat_back",[],"Back to camp menu.",[(jump_to_menu, "mnu_camp"),]),	 
 ]),

( "drank_ent_water_human",0,# human player drank Ent water
    "^^^You drink the water. It tastes clean and refreshing. It has a pleasant fragrance, as of musk.^You feel refreshed.^^However, you also have a strange, unnatural feeling. Something tells you that you'd better never, ever again drink this water.",
  "none",[  (try_begin),
              (troop_get_type, ":player_race", "trp_player"),
              (            eq, ":player_race",  tf_dwarf),
              # --
              (set_background_mesh, "mesh_draw_entdrink_dwarf"),
              
            (else_try),
              (call_script, "script_determine_what_player_looks_like"),
              (         eq, "$player_looks_like_an_orc", 1),
              # --
              (set_background_mesh, "mesh_draw_entdrink_orc"),
              
            (else_try),
              (set_background_mesh, "mesh_draw_entdrink_human"),
            (try_end),

  ],[("continue_dot",[],"Continue.",[(change_screen_return,0),] ),]
 ),
( "drank_ent_water_orc",0,# orc player drank Ent water (mtarini)
	"^^^You drink the water. It is just water.^Suddenly, you grasp your throath, in a raptus of pain.^Poisoned!^You choke, you throw up black blood, you almost pass away.^^It hurts, oh, it hurts.",
	"none",[(display_log_message,"@HP lost from poisoning."),(troop_set_health,"trp_player",5),]
	,[("i_shall_surv",[],"I... shall... survive!",[(change_screen_return,0)])]
 ),

( "end_game",0,
 "^^^^^The decision is made, and you resolve to give up your adventurer's\
 life and settle down. You sell off your weapons and armour, gather up\
 all your belongings, and ride off into the sunset....",
 "none",
 [],
 [("end_game_bye",[],"Farewell.",[(change_screen_quit)])]
 ),

#MV: DON'T REMOVE THIS AGAIN - IT'S USED IN A QUEST
  ("cattle_herd",mnf_scale_picture,
   "You encounter some people.",
   "none",
   [],
    [ ("cattle_drive_away",[],"Order them to follow.",
       [(party_set_slot, "$g_encountered_party", slot_cattle_driven_by_player, 1),
        (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_escort_party),
        (party_set_ai_object,"$g_encountered_party", "p_main_party"),
        (change_screen_return),
        ]),
      ("cattle_stop",[],"Bring them to a stop.",
       [(party_set_slot, "$g_encountered_party", slot_cattle_driven_by_player, 0),
        (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_hold),
        (change_screen_return),
        ]),
      ("leave",[],"Leave.",[(change_screen_return),]),
    ]
  ),

( "simple_encounter",mnf_enable_hot_keys,
    "^^^^^{s2}^You have {reg22} troops fit for battle against their {reg11}.^^The battle is taking place in {s3}{s4}.^^Your orders?",
    "none",
    [	#(set_background_mesh, "mesh_ui_default_menu_window"),
		(try_begin), 
			(eq, "$prebattle_talk_done",1),
			(assign, "$prebattle_talk_done",0),
			(call_script,"script_start_current_battle"),
		(try_end),

		#swy-- avoid undesired relocation when losing/running away from battle
		#(call_script, "script_maybe_relocate_player_from_z0"), #InVain: Disabled this to fix wrong terrain type in battles (Player would teleport back too early).

		# get region + landmark (mtarini)
		#(party_get_current_terrain, "$current_player_terrain","p_main_party"),
		#(call_script, "script_get_region_of_party","p_main_party"),(assign, "$current_player_region", reg1),
		#(call_script, "script_get_close_landmark","p_main_party"), (assign, "$current_player_landmark", reg0),
		
		(store_add, reg2, str_shortname_region_begin, "$current_player_region",),
		(str_store_string,s3,reg2),
		
		(str_clear, s4),
		(try_begin), 
			(call_script, "script_cf_store_landmark_description_in_s17", "$current_player_landmark"),
			(str_store_string,s4,"@, {s17}."), 
		(try_end),

        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (call_script, "script_encounter_calculate_fit"),
		(assign, reg22, reg10),
        (try_begin),
		  # first turn...
          (eq, "$new_encounter", 1),
          
          #(assign, "$g_encounter_is_in_village", 0),
          #(assign, "$g_encounter_type", 0),
          (try_begin),
            (party_slot_eq, "$g_enemy_party", slot_party_ai_state, spai_raiding_around_center),
            (party_get_slot, ":village_no", "$g_enemy_party", slot_party_ai_object),
            (store_distance_to_party_from_party, ":dist", ":village_no", "$g_enemy_party"),
            (try_begin),
              (lt, ":dist", raid_distance),
              #(assign, "$g_encounter_is_in_village", ":village_no"),
#              (assign, "$g_encounter_type", enctype_fighting_against_village_raid),
            (try_end),
          (try_end),

          (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
          (call_script, "script_encounter_init_variables"),
          (assign, "$encountered_party_hostile", 0),
          (assign, "$encountered_party_friendly", 0),
          
          #MV: Quest exceptions
          (assign, ":is_quest_party", 0),
          (try_begin),
            (this_or_next|eq, "$g_encountered_party_template", "pt_gandalf"),
            (this_or_next|eq, "$g_encountered_party_template", "pt_nazgul"),
            (eq, "$g_encountered_party_template", "pt_runaway_serfs"),
            (assign, ":is_quest_party", 1),
          (try_end),
          
          (try_begin),
            (this_or_next|gt, "$g_encountered_party_relation", 0),
            (eq, ":is_quest_party", 1),
            (assign, "$encountered_party_friendly", 1),
			# talk with non-hostile parties OR quest parties
			(assign, "$new_encounter", 0),
			(assign, "$talk_context", tc_party_encounter),
            (try_begin), #cutscene dialogs
              (eq, "$g_encountered_party_template", "pt_gandalf"),
              (gt, "$g_tld_gandalf_state", 0),
              (call_script, "script_start_conversation_cutscene", "$g_tld_gandalf_state"),
            (else_try), 
              (eq, "$g_encountered_party_template", "pt_nazgul"),
              (gt, "$g_tld_nazgul_state", 0),
              (call_script, "script_start_conversation_cutscene", "$g_tld_nazgul_state"),
            (else_try), #normal dialogs
			  (call_script, "script_setup_party_meeting", "$g_encountered_party"),
            (try_end),
          (try_end),
          (try_begin),
            (lt, "$g_encountered_party_relation", 0),
            (assign, "$encountered_party_hostile", 1),
            (try_begin),
              (encountered_party_is_attacker),
              (assign, "$cant_leave_encounter", 1),
            (try_end),
          (try_end),
        (else_try), 
		  #second or more wave
		  #          (try_begin),
		  #            (call_script, "script_encounter_calculate_morale_change"),
		  #          (try_end),
          (try_begin),
            # We can leave battle only after some troops have been killed. 
            (eq, "$cant_leave_encounter", 1),
            (call_script, "script_party_count_members_with_full_health", "p_main_party_backup"),
            (assign, ":org_total_party_counts", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_encountered_party_backup"),
            (val_add, ":org_total_party_counts", reg0),

            (call_script, "script_party_count_members_with_full_health", "p_main_party"),
            (assign, ":cur_total_party_counts", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
            (val_add, ":cur_total_party_counts", reg0),

            (store_sub, ":leave_encounter_limit", ":org_total_party_counts", 10),
            (lt, ":cur_total_party_counts", ":leave_encounter_limit"),
            (assign, "$cant_leave_encounter", 0),
          (try_end),
          (eq, "$g_leave_encounter",1),
		  (call_script, "script_maybe_relocate_player_from_z0"),
          (change_screen_return),
        (try_end),

        #setup s2
        (try_begin),
          (party_is_active,"$g_encountered_party"),
          (str_store_party_name, s1,"$g_encountered_party"),
          (try_begin),
			(eq, "$new_encounter", 1),
			(eq, "$encountered_party_hostile", 1),
			(encountered_party_is_attacker),
			(call_script, "script_str_store_party_movement_verb", s10, "$g_encountered_party"),
            (str_store_string, s2,"@A group of {s1} is {s10} toward you."),
			#(str_store_string, s2,"@A group of {s1}  are {reg10?riding:marching} toward you."),
          (else_try),
			(eq, "$new_encounter", 1),
			(this_or_next|eq, "$g_encountered_party_template", "pt_wild_troll"),
			(this_or_next|eq, "$g_encountered_party_template", "pt_raging_trolls"),
			(this_or_next|eq, "$g_encountered_party_template", "pt_refugees"),
			(eq, "$encountered_party_hostile", 1),
			(neg|encountered_party_is_attacker),
            (str_store_string, s2,"@You are attacking a group of {s1}."),
          (else_try),
			(eq, "$new_encounter", 0),
            (str_store_string, s2,"@The battle against the group of {s1} continues."),
          (try_end),
        (try_end),
		
		
        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (assign, ":num_enemy_regulars_remaining", reg0 ),
          (assign, ":enemy_finished",0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (this_or_next|le, ":num_enemy_regulars_remaining", 0), #battle won #Kham - edited from eq
            (le, ":num_enemy_regulars_remaining",  "$num_routed_enemies"),  #Kham - we don't want routed enemies to spawn

            (assign, ":continue", 0),
          	(try_begin),
          		(gt, reg11, 0),
          		(store_div, ":player_to_enemy_ratio", reg22, reg11),
          		(gt, ":player_to_enemy_ratio", 5), #test for routed enemies again...
          		(assign, ":continue", 1),
          	(else_try),
          		(le, reg11, 0),
          		(assign, ":continue", 1),
          	(try_end),
          	(eq, ":continue", 1),

            (assign, ":enemy_finished",1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),
            (this_or_next|le, ":num_enemy_regulars_remaining", 0),
            (le, "$g_enemy_fit_for_battle","$num_routed_enemies"), #Kham - we don't want routed enemies to spawn.
            (ge, "$g_friend_fit_for_battle",1),
           
            (assign, ":continue", 0),
          	(try_begin),
          		(gt, reg11, 0),
          		(store_div, ":player_to_enemy_ratio", reg22, reg11),
          		(gt, ":player_to_enemy_ratio", 5), #test for routed enemies again...
          		(assign, ":continue", 1),
          	(else_try),
          		(le, reg11, 0),
          		(assign, ":continue", 1),
          	(try_end),
          	(eq, ":continue", 1),

            (assign, ":enemy_finished",1),
          (try_end),
          (this_or_next|eq, ":enemy_finished",1),
          (eq,"$g_enemy_surrenders",1),
          (assign, "$g_next_menu", -1),
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
		  #     (eq, "$encountered_party_hostile", 1),
          (call_script, "script_party_count_members_with_full_health","p_main_party"),
          (assign, reg3, reg0),
          (assign, ":friends_finished",0),
          (try_begin),
            (eq, "$g_battle_result", -1),
            #(eq, reg3, 0), #battle lost
            (le, reg3,  "$num_routed_us"), #Kham - we don't want routed allies to spawn
            (assign,  ":friends_finished",1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),
            (ge, "$g_enemy_fit_for_battle",1),
            (le, "$g_friend_fit_for_battle",0),
            (assign,  ":friends_finished",1),
          (try_end),
		  
          (this_or_next|eq,"$g_player_surrenders",1),
          (eq,  ":friends_finished",1),
		  (assign, "$recover_after_death_menu", "mnu_recover_after_death_default"),
          (assign, "$g_next_menu", "mnu_tld_player_defeated"),
          (jump_to_menu, "mnu_total_defeat"),
        (try_end),

    ## set background mesh
    (set_background_mesh, "mesh_ui_default_menu_window"),
    (try_begin),
      #swy-- native looters are tribal orcs, neat, huh?
      (eq, "$g_encountered_party_template", "pt_looters"),
      (set_background_mesh, "mesh_draw_tribal_orcs"),
    (else_try),
      #swy-- if "tree-chopping orcs" then show this illustration thingy...
      (eq, "$g_encountered_party_template", "pt_fangorn_orcs"),
      (set_background_mesh, "mesh_draw_lumberjack_orcs"),
    (else_try),
      #swy-- if "wild goblins" then show this illustration thingy...
      (eq, "$g_encountered_party_template", "pt_mountain_bandits"),
      (set_background_mesh, "mesh_draw_mountain_goblins"),
    (else_try),
      #swy-- if "troublesome goblins" then show this illustration thingy...
      (eq, "$g_encountered_party_template", "pt_troublesome_bandits"),
      (set_background_mesh, "mesh_draw_troublesome_goblins"),
    (else_try),
      #swy-- if "corsair renegades" or "corsair scouts" then show this illustration thingy...
      (this_or_next|eq, "$g_encountered_party_template", "pt_sea_raiders"),
      (             eq, "$g_encountered_party_template", "pt_umbar_scouts"),
      (set_background_mesh, "mesh_draw_corsair_renegades"),
    (else_try),
      #swy-- if "dunland outcasts" or "dunland scouts" then show this illustration thingy...
      (this_or_next|eq, "$g_encountered_party_template", "pt_dunland_scouts"),
      (             eq, "$g_encountered_party_template", "pt_steppe_bandits"),
      (set_background_mesh, "mesh_draw_dunland_outcasts"),
    (else_try),
      (is_between, "$g_encountered_party_template", "pt_forest_bandits", "pt_steppe_bandits"),
      (set_background_mesh, "mesh_draw_orc_raiders"),
    (else_try),
      (is_between, "$g_encountered_party_template", "pt_wild_troll", "pt_looters"),
      (set_background_mesh, "mesh_draw_wild_troll"),
    (else_try),
    	(eq, "$g_encountered_party_template", "pt_ring_hunters"),
    	(set_background_mesh, "mesh_draw_ring_hunters_army"),
    (try_end),
		
		
		# set reg21, to change the options string in the menu
		(try_begin), (encountered_party_is_attacker),
			(assign, reg21, 0),
		(else_try),
			(assign, reg21, 1),
		(try_end),

	#Calculate Formula A here - Kham
	(try_begin), 
		(eq, "$new_rank_formula_calculated", 0),
		(call_script, "script_calculate_formula_a", 0),
	(try_end),
	#Calculate Formula A END
    ],
	
    [
       # For unfriendly enemies (e.g bandits, trolls, quest parties)
      ("encounter_attack",[
          (this_or_next|eq, 		"$encountered_party_friendly", 0),
		  (this_or_next|is_between, "$g_encountered_party_template", "pt_wild_troll" ,"pt_looters"),
		  (this_or_next|eq, 		"$g_encountered_party_template", "pt_ring_hunters"),
		  (this_or_next|eq,			"$g_encountered_party", "$qst_raider_party_1"),
		  (this_or_next|eq,			"$g_encountered_party", "$qst_raider_party_2"),
		  (this_or_next|eq,			"$g_encountered_party", "$qst_raider_party_3"),
		  (				eq,			"$g_encountered_party", "$qst_reinforcement_party"),
##           (neg|troop_is_wounded, "trp_player"), #a test: what happes if I let player partecipate? #Kham - let's have the player participate
##          (store_troop_health,reg(5)),
##          (ge,reg(5),5),
          ],
         "{reg21?Charge_them:Prepare_to_face_them}.",[
			(try_begin),
				# talk with hostile troops after you have chose to attack
				(eq, "$new_encounter", 1),
				(assign, "$new_encounter", 0),
				(assign, "$prebattle_talk_done",1),
				(assign, "$talk_context", tc_party_encounter),
				(call_script, "script_setup_party_meeting", "$g_encountered_party"),
			(else_try),
				(call_script,"script_start_current_battle"),
			(try_end),

      ]),

      ("encounter_order_attack",[
          (eq, "$encountered_party_friendly", 0),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),(ge, reg0, 4),
          ],
           "Order your troops to {reg21?attack:face_them} without you.",[
		     (assign, "$new_encounter", 0),
		     (jump_to_menu,"mnu_order_attack_begin"),
                                                            #(simulate_battle,3)
		]),

      # Kham - Control Allies for Inf Points
      ("control_allies_menu", [
      	#(eq, "$cheat_mode", 1),
  	    (call_script, "script_get_faction_rank", "$players_kingdom"), (assign, ":rank", reg0), #rank points to rank number 0-9
     	(ge, ":rank", 3), #Must be at least rank 3
      	(gt, "$g_starting_strength_friends", 0), # we have allies
      	(neq, "$player_control_allies", 1),
      	(party_get_num_companion_stacks, ":num_stacks", "p_collective_friends"),
      	(assign, ":num_lords", 0),
      	(try_for_range, ":stack_no", 0, ":num_stacks"),
      		(party_stack_get_troop_id,   ":stack_troop","p_collective_friends",":stack_no"),
      		(is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
      		(val_add, ":num_lords", 1),
      	(try_end),
      	(gt, ":num_lords", 0), # have to have lords in battle
      	],
      	 "Use Influence to Command Your Allies in the Field.", [
      	 	(jump_to_menu, "mnu_player_control_allies"),
      ]),

      # Kham - Control Allies for Inf Points END

      #Kham - Hide from Enemy when party < 8  or wildcraft skill allows it.

       ("encounter_hide",[
          (eq, "$encountered_party_friendly", 0),
          (eq, "$cant_leave_encounter", 1),
          #(party_get_num_companions, ":no", "p_main_party"),(lt, ":no", 8),
          (call_script, "script_cf_can_hide_from_enemy"),
          ],
           "Hide from the enemy...",[
           (jump_to_menu, "mnu_hide"),]),

		("special_whip",[
			(eq, "$new_encounter", 1),
		    (is_between, "$g_encountered_party_template", "pt_looters","pt_steppe_bandits"),
		    (player_has_item, "itm_angmar_whip_reward"),
			(str_store_item_name, s4, "itm_angmar_whip_reward"),
			(party_can_join_party, "$g_encountered_party","p_main_party"),
		],
		"Rush forward toward them cracking the {s4}.",[
			(call_script, "script_setup_party_meeting", "$g_encountered_party"),
			(assign,"$talk_context",tc_make_enemy_join_player),
		]),

 ]+concatenate_scripts([[	 
      ("debug_leave",[
          (eq,"$cant_leave_encounter", 1),
		  (eq, "$cheat_mode", 1),
          ],"DEBUG: avoid this battle.",[ (leave_encounter),(change_screen_return)]),
 ] for ct in range(cheat_switch)]) + (is_a_wb_menu==1 and [("encounter_attack_bearform",[
          # Arsakes: BEAR shapeshift option
          (this_or_next|eq, 		"$encountered_party_friendly", 0),
		  (this_or_next|is_between, "$g_encountered_party_template", "pt_wild_troll",
                      "pt_looters"),
		  (this_or_next|eq,"$g_encountered_party_template", "pt_ring_hunters"),
		  (this_or_next|eq, "$g_encountered_party", "$qst_raider_party_1"),
		  (this_or_next|eq, "$g_encountered_party", "$qst_raider_party_2"),
		  (this_or_next|eq, "$g_encountered_party", "$qst_raider_party_3"),
                  (eq, "$g_encountered_party", "$qst_reinforcement_party"),
                  (this_or_next|troop_slot_eq, "trp_traits", slot_trait_bear_shape, 1),
                  (eq, "$cheat_mode", 1),
          ],
         "{reg21?Leap_into_battle_in_bear_form:Turn_skin_and_face_them}.",[
                        (call_script, "script_cf_select_bear_form"),
                        (call_script,"script_start_current_battle"),

      ]),] or []) + [

      ("encounter_leave",[
          (eq,"$cant_leave_encounter", 0),
          ],"Disengage.",[
###NPC companion changes begin
              #(try_begin),
              #    (eq, "$encountered_party_friendly", 0),
              #    (encountered_party_is_attacker),
              #    (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
              #(try_end),
###NPC companion changes end
#Troop commentary changes begin
              # (try_begin),
                  # (eq, "$encountered_party_friendly", 0),
                  # (encountered_party_is_attacker),
                  # (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
                  # (try_for_range, ":stack_no", 0, ":num_stacks"),
                    # (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
                    # (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
                    # (store_troop_faction, ":victorious_faction", ":stack_troop"),
                    # (call_script, "script_add_log_entry", logent_player_retreated_from_lord, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
                  # (try_end),
              # (try_end),
#Troop commentary changes end
		# This is here so when you flee/leave it checks for routed parties -CC
		(try_begin),(call_script, "script_cf_spawn_routed_parties"),(try_end),
          	(leave_encounter),(change_screen_return)]),
			
      ("encounter_retreat",[
         (eq,"$cant_leave_encounter", 1),
         (party_get_num_companions, ":no", "p_main_party"),(gt, ":no", 8),
         (call_script, "script_get_max_skill_of_player_party", "skl_tactics"),
         (assign, ":max_skill", reg0),
         (val_add, ":max_skill", 4),

         (call_script, "script_party_count_members_with_full_health", "p_collective_enemy", 0),
         (assign, ":enemy_party_strength", reg0),
         (val_div, ":enemy_party_strength", 2),

         (val_div, ":enemy_party_strength", ":max_skill"),
         (val_max, ":enemy_party_strength", 1),

         (call_script, "script_party_count_fit_regulars", "p_main_party"),
         (assign, ":player_count", reg0),
         (ge, ":player_count", ":enemy_party_strength"),
         ],"Pull back, leaving some soldiers behind to cover your retreat.",[(jump_to_menu, "mnu_encounter_retreat_confirm"),]),

 ]+concatenate_scripts([[		 
      ("encounter_surrender",[
         (eq,"$cant_leave_encounter", 1),
		 (eq, "$cheat_mode", 1),
          ],"DEBUG: surrender.",[(assign,"$g_player_surrenders",1)]),

	  ("encounter_cheat_heal",[
         (eq, "$cheat_mode",1),
		 (store_troop_health  , reg20, "trp_player",0), (lt, reg20,95),
          ],"CHEAT: heal yourself.",[
		    (troop_set_health  , "trp_player",100),
	        (display_message, "@CHEAT: healed!!!"),
			(jump_to_menu, "mnu_simple_encounter"),
		]),
 ] for ct in range(cheat_switch)])+[
    ]
 ),

# Player Control Allies Menu (Simple Enncounter),

("player_control_allies", 0, 
	"^^^^^{s60}^^^", "none",
	[(set_background_mesh, "mesh_ui_default_menu_window"),
     (gt, "$g_starting_strength_friends", 0), # we have allies
     (neq, "$player_control_allies", 1),
     (party_get_num_companion_stacks, ":num_stacks", "p_collective_friends"),
     (party_get_num_companions, ":num_companions", "p_collective_friends"),
     (assign, ":num_lords", 0),
     (assign, ":base_inf_cost", player_control_allies_inf),
     (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id,   ":stack_troop","p_collective_friends",":stack_no"),
        (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
        (val_add, ":num_lords", 1),
     (try_end),
     (gt, ":num_lords", 0), # have to have lords in battle
     (assign, reg39, ":num_lords"),
     (store_div, ":divide", ":num_companions", 40),
     (val_max, ":divide", 0),
     (try_begin),
        (gt, ":num_lords", 1),
        (val_mul, ":num_lords", 3),
     (try_end),
     (val_add, ":base_inf_cost", ":num_lords"),
     (val_add, ":base_inf_cost", ":divide"),
     (assign, reg40, ":base_inf_cost"),
     (str_store_string, s60, "@There are {reg39} ally commanders in this battle. You can command them and their troops for {reg40} influence points."),
    ],[
		("player_control_allies_simple", [], "Command them and charge the enemy", [
			(call_script, "script_spend_influence_of", reg40, "$players_kingdom"),
          	(assign, "$player_control_allies", 1),
  			(try_begin),
  			   # talk with hostile troops after you have chose to attack
  			   (eq, "$new_encounter", 1),
  			   (assign, "$new_encounter", 0),
  			   (assign, "$prebattle_talk_done",1),
  			   (assign, "$talk_context", tc_party_encounter),
  			   (call_script, "script_setup_party_meeting", "$g_encountered_party"),
  			(else_try),
  			   (call_script,"script_start_current_battle"),
  			(try_end),]),
		("player_control_allies_back", [], "Go back...", [
			(jump_to_menu, "mnu_simple_encounter"),]),
	]),

##Kham - Hide Menu - Skill requirement TBD

("hide",0,
	"^^^^^{s5}^^^","none",
	[(set_background_mesh, "mesh_town_evilcamp"),
	 (party_get_num_companions, ":number", "p_main_party"),
	 (party_get_skill_level, ":skill", "p_main_party", skl_persuasion), #Wildcraft
	 (try_begin),
	 	(le, ":number", 8),
	 	(str_store_string, s5, "@Having a small party has its benefits...You and your troops hide from the enemy for a few hours to be sure that you are not seen."),
	 (else_try),
		(ge, ":skill", 1),
		(val_mul, ":skill", 4), #Multiplier
		(val_add, ":skill", 10), #Base 10 troops
		(assign, reg1, ":skill"),
		(assign, reg2, ":number"),
		(str_store_string, s5, "@Your ability to master your environments allowed you to find a safe place to hide. (Your skill in Wildcraft allows you to hide with {reg1} troops)"),
	(try_end),],
	[("hide_close",[], "Continue...",[
		(call_script, "script_hide_number_of_hours"),
		(leave_encounter),
		(change_screen_return)])]),

##Kham - Hide Menu End


( "encounter_retreat_confirm",0,
    "^^^^^As the party member with the highest tactics skill,\
   ({reg2}), {reg3?you devise:{s3} devises} a plan that will allow you and your men to escape with your lives,\
   but you'll have to leave {reg4} soldiers behind to stop the enemy from giving chase.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
	 (call_script, "script_get_max_skill_of_player_party", "skl_tactics"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),
     (val_add, ":max_skill", 4),

     (call_script, "script_party_count_members_with_full_health", "p_collective_enemy", 0),
     (assign, ":enemy_party_strength", reg0),
     (val_div, ":enemy_party_strength", 2),

     (store_div, reg4, ":enemy_party_strength", ":max_skill"),
     (val_max, reg4, 1),
     
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),
     ],
    [
      ("leave_behind",[],"Go on. The sacrifice of these men will save the rest.",[
      	(assign, ":num_casualties", reg4),
    	(display_message, "@{reg4} will be lost."),
        (set_spawn_radius, 0),
        (spawn_around_party, "p_main_party", "pt_retreat_troops"),
        (assign, ":retreat_party", reg0),
        (party_set_faction, ":retreat_party", "$players_kingdom"),
        (faction_get_slot, ":tier_1_troop", "$players_kingdom", slot_faction_tier_1_troop),
        (party_add_members, ":retreat_party", ":tier_1_troop",1),
        (party_remove_members, ":retreat_party", "trp_farmer", 1),
         ] + (is_a_wb_menu==1 and [
        (party_set_aggressiveness, ":retreat_party",15),
        ] or []) + [
        (party_set_ai_initiative, ":retreat_party", 0),
        (party_get_icon, ":player_icon", "p_main_party"), 
        (party_set_icon, ":retreat_party", ":player_icon"),
        (party_set_ai_behavior, ":retreat_party", ai_bhvr_attack_party),
        (party_set_ai_object, ":retreat_party", "$g_encountered_party"),
        (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_attack_party),
        (party_set_ai_object, "$g_encountered_party", ":retreat_party"),
        (try_for_range, ":unused", 0, ":num_casualties"),
          (call_script, "script_cf_party_remove_random_regular_troop", "p_main_party"),
          (assign, ":lost_troop", reg0),
          (store_random_in_range, ":random_no", 0, 100),
          (try_begin),
          	(ge, ":random_no", 30),
            (party_add_prisoners, "$g_encountered_party", ":lost_troop", 1),
          (else_try),
           	(party_add_members, ":retreat_party", ":lost_troop", 1),
          (try_end),         
        (try_end),
        (call_script, "script_change_player_party_morale", -20),
        (jump_to_menu, "mnu_encounter_retreat"),
          ]),
      ("dont_leave_behind",[],"No. We leave no one behind.",[(jump_to_menu, "mnu_simple_encounter"),]),
    ]
 ),
( "encounter_retreat",0,
    "^^^^^You tell {reg4} of your troops to hold the enemy while you retreat with the rest of your party.",
    "none",
    [],
    [("continue",[],"Continue...",[
###Troop commentary changes begin
          (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
          (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
          (try_for_range, ":stack_no", 0, ":num_stacks"),
              (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
              (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
              (store_troop_faction, ":victorious_faction", ":stack_troop"),
              (call_script, "script_add_log_entry", logent_player_retreated_from_lord_cowardly, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
          (try_end),
###Troop commentary changes end  

			# This is here so when you flee it checks for routed parties -CC
		  (try_begin),(call_script, "script_cf_spawn_routed_parties"),(try_end),
		  (party_ignore_player, "$g_encountered_party", 3), #Kham - Fix
	      (leave_encounter),(change_screen_return)]),
    ]
 ),
( "order_attack_begin",0,
    "^^^^^^__________Your troops prepare to attack the enemy.",
    "none",
    [],
    [ ("order_attack_begin",[],"Order the attack to begin.", [(assign, "$g_engaged_enemy", 1),(jump_to_menu,"mnu_order_attack_2")]),
      ("call_back",[],"Call them back.",[(jump_to_menu,"mnu_simple_encounter")]),
    ]
 ),
( "order_attack_2",mnf_disable_all_keys,
    "^{s4}^Your casualties: {s8}^^Enemy casualties: {s9}",
    "none",
    [	(set_background_mesh, "mesh_ui_default_menu_window"),	
	
	# Reset routed count (needs to be here to prevent bugs...)
	(try_for_range, ":troop_no", 0, "trp_last"),
		(troop_set_slot, ":troop_no", slot_troop_routed_us, 0),
		(troop_set_slot, ":troop_no", slot_troop_routed_allies, 0),
		(troop_set_slot, ":troop_no", slot_troop_routed_enemies, 0),
	(try_end),
	
		(call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
		(assign, ":player_party_strength", reg0),
		(val_div, ":player_party_strength", 5),
		(call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
		(assign, ":enemy_party_strength", reg0),
		(val_div, ":enemy_party_strength", 5),
		#(call_script,"script_inflict_casualties_to_party", "p_main_party", ":enemy_party_strength"),
		(inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength", "p_temp_casualties"),
		(call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
		(str_store_string_reg, s8, s0),
		#(call_script,"script_inflict_casualties_to_party", "$g_encountered_party", ":player_party_strength"),
		(inflict_casualties_to_party_group, "$g_encountered_party", ":player_party_strength", "p_temp_casualties"),
		(call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
		(str_store_string_reg, s9, s0),
		(party_collect_attachments_to_party, "$g_encountered_party", "p_collective_enemy"),
		#(assign, "$cant_leave_encounter", 0),
		(assign, "$no_soldiers_left", 0),
		(try_begin),
		  (call_script, "script_party_count_members_with_full_health","p_main_party"),
		  (assign, ":num_our_regulars_remaining", reg0),
          (store_add, ":num_routed_us_plus_one", "$num_routed_us", 1),
          (le, ":num_our_regulars_remaining", ":num_routed_us_plus_one"), #Kham - don't let routed enemies spawn
		  (assign, "$no_soldiers_left", 1),
		  (str_store_string, s4, "str_order_attack_failure"),
		(else_try),
		  (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
		  (assign, ":num_enemy_regulars_remaining", reg0),
          (this_or_next|le, ":num_enemy_regulars_remaining", 0),
          (le, ":num_enemy_regulars_remaining", "$num_routed_enemies"), #Kham - don't let routed enemies spawn
		  (assign, ":continue", 0),
		  (party_get_num_companion_stacks, ":party_num_stacks", "p_collective_enemy"),
		  (try_begin),
			(eq, ":party_num_stacks", 0),
			(assign, ":continue", 1),
		  (else_try),
			(party_stack_get_troop_id, ":party_leader", "p_collective_enemy", 0),
			(try_begin),
			  (neg|troop_is_hero, ":party_leader"),
			  (assign, ":continue", 1),
			(else_try),
			  (troop_is_wounded, ":party_leader"),
			  (assign, ":continue", 1),
			(try_end),
		  (try_end),
		  (eq, ":continue", 1),
		  (assign, "$g_battle_result", 1),
		  (assign, "$no_soldiers_left", 1),
		  (str_store_string, s4, "str_order_attack_success"),
		(else_try),
		  (str_store_string, s4, "str_order_attack_continue"),
		(try_end),
    ],
    [("order_attack_continue",[(eq, "$no_soldiers_left", 0)],"Order your soldiers to continue the attack.",[(jump_to_menu,"mnu_order_attack_2")]),
     ("order_retreat",[(eq, "$no_soldiers_left", 0)],"Call your soldiers back.",[(jump_to_menu,"mnu_simple_encounter")]),
     ("continue",[(eq, "$no_soldiers_left", 1)],"Continue...",[(jump_to_menu,"mnu_simple_encounter")]),
    ]
 ),

# remove us - MV: reintroduced from Native
( "kingdom_army_quest_report_to_army",0,
   "{s8} sends word that he wishes you to join his new military campaign.\
   You need to bring at least {reg13} troops to the army,\
   and are instructed to raise more warriors with all due haste if you do not have enough.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$players_kingdom", pos0),
        
        (quest_get_slot, ":quest_target_troop", "qst_report_to_army", slot_quest_target_troop),
        (quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
        (call_script, "script_get_information_about_troops_position", ":quest_target_troop", 0),
        (str_clear, s9),
        (try_begin),
          (eq, reg0, 1), #troop is found and text is correct
          (str_store_string, s9, s1),
        (try_end),
        (str_store_troop_name, s8, ":quest_target_troop"),
        (assign, reg13, ":quest_target_amount"),
      ],
    [
      ("reject",[],"Send a message you are too busy.",
       [   (quest_set_slot, "qst_report_to_army", slot_quest_dont_give_again_remaining_days, 7),
           (change_screen_return),
        ]),
      ("send_word",[],"Send word you'll join him shortly.",
       [   (quest_get_slot, ":quest_target_troop", "qst_report_to_army", slot_quest_target_troop),
           (quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
           (str_store_troop_name_link, s13, ":quest_target_troop"),
           (assign, reg13, ":quest_target_amount"),
           (setup_quest_text, "qst_report_to_army"),
           (str_store_string, s2, "@{s13} asked you to report to him with at least {reg13} troops."),
           (call_script, "script_start_quest", "qst_report_to_army", ":quest_target_troop"),
           (call_script, "script_report_quest_troop_positions", "qst_report_to_army", ":quest_target_troop", 3),
           (change_screen_return),
        ]),
     ]
 ),
( "kingdom_army_quest_messenger",0,
   "{s8} sends word that he wishes to speak with you about a task he needs performed.\
   He requests you to come and see him as soon as possible.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$players_kingdom", pos0),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name, s8, ":faction_marshall"),
      ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),
( "kingdom_army_quest_join_siege_order",0,
    "{s8} sends word that you are to join the siege of {s9} in preparation for a full assault.\
    Your troops are to take {s9} at all costs.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$players_kingdom", pos0),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (quest_get_slot, ":quest_target_center", "qst_join_siege_with_army", slot_quest_target_center),
        (str_store_troop_name, s8, ":faction_marshall"),
        (str_store_party_name, s9, ":quest_target_center"),
      ],
    [
      ("continue",[],"Continue...",
       [   (call_script, "script_end_quest", "qst_follow_army"),
           (quest_get_slot, ":quest_target_center", "qst_join_siege_with_army", slot_quest_target_center),
           (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
           (str_store_troop_name_link, s13, ":faction_marshall"),
           (str_store_party_name_link, s14, ":quest_target_center"),
           (setup_quest_text, "qst_join_siege_with_army"),
           (str_store_string, s2, "@{s13} ordered you to join the assault against {s14}."),
           (call_script, "script_start_quest", "qst_join_siege_with_army", ":faction_marshall"),
           (change_screen_return),
        ]),
     ]
 ),
( "kingdom_army_follow_failed",0,
    "You have disobeyed orders and failed to follow {s8}. He sends a message he assumes you have more pressing matters, but warns his patience is not unlimited.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$players_kingdom", pos0),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name, s8, ":faction_marshall"),
        (call_script, "script_abort_quest", "qst_follow_army", 1),
        #(call_script, "script_change_player_relation_with_troop", ":faction_marshall", -3),
      ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),

( "battle_debrief",mnf_disable_all_keys,
    "{s11}^Your Casualties:{s8}{s10}^^Enemy Casualties:{s9}",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
	(call_script, "script_maybe_relocate_player_from_z0"),
    (val_add, "$battle_renown_total", "$battle_renown_value"),
	(call_script, "script_encounter_calculate_fit"),
	 
	(call_script, "script_party_count_fit_regulars", "p_main_party"),
    (assign, "$playerparty_postbattle_regulars", reg0),

	(try_begin), # set background picture for victory/defeat -- mtarini

		(this_or_next|eq, "$g_enemy_fit_for_battle",0),(eq, "$g_friend_fit_for_battle", 0 ), # battle is totally over: proceed!
		
		(try_begin),
			(eq, "$g_battle_result", 1),
			(assign, ":winning_side_race_group", "$player_side_race_group" ),
			(assign, ":losing_side_race_group",  "$enemy_side_race_group" ),
			(assign, ":winning_side_race", "$player_side_race" ),
			#(assign, ":losing_side_race",  "$enemy_side_race" ), # not used... yet
			(assign, ":winning_side_faction", "$player_side_faction" ),
			#(assign, ":losing_side_faction",  "$enemy_side_faction" ), # not used... yet
		(else_try),
			(assign, ":winning_side_race_group", "$enemy_side_race_group" ),
			(assign, ":losing_side_race_group",  "$player_side_race_group" ),
			(assign, ":winning_side_race", "$enemy_side_race" ),
			#(assign, ":losing_side_race",  "$player_side_race" ),   # not used... yet
			(assign, ":winning_side_faction", "$enemy_side_faction" ),
			#(assign, ":losing_side_faction",  "$player_side_faction" ), # not used... yet
		(try_end),

		# CppCoder quick search tag [VIKTOREE] (For adding the new victory paintings)
		
		(try_begin),
			# orc VS anything not orc
			( eq, ":winning_side_race_group", tf_orc ),
			(neq, ":losing_side_race_group",  tf_orc ),
			(store_random_in_range,":rnd",0,2),
			(try_begin),(eq,":rnd",0),(set_background_mesh, "mesh_draw_victory_orc"),  # specific victory-loss image:  orcs VS humans
			 (else_try),(set_background_mesh, "mesh_draw_victory_uruk"),
			(try_end),
		(else_try),	
			# orc VS orc
			( eq, ":winning_side_race_group", tf_orc ),
			( eq, ":losing_side_race_group",  tf_orc ),
			(neq, ":winning_side_faction",    fac_no_faction), # not good for winning tribals etc.
			(set_background_mesh, "mesh_draw_victory_orc_orc"),  # specific victory-loss image:  orcs VS orcs
		(else_try),
			# dwarf VS anything
			(eq, ":winning_side_race", tf_dwarf ),
			(set_background_mesh, "mesh_draw_victory_dwarf"),  # specific victory-loss image: dwarves VS anything
		(else_try),
			# evil men VS anything
			(eq, ":winning_side_race", tf_evil_man ),
			(set_background_mesh, "mesh_draw_victory_evilman"),  # specific victory-loss image: evil men VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_gondor" ),
			(set_background_mesh, "mesh_draw_victory_gondor"), # specific victory-loss image: gondor VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_rohan" ),
			(set_background_mesh, "mesh_draw_victory_rohan"), # specific victory-loss image: rohan VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_imladris" ),
			(set_background_mesh, "mesh_draw_victory_rivendell"), # specific victory-loss image: rivendell VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_woodelf" ),
			(set_background_mesh, "mesh_draw_victory_mirkwood"), # specific victory-loss image: mirkwood VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_dunland" ),
			(set_background_mesh, "mesh_draw_victory_dunland"), # specific victory-loss image: dunland VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_khand" ),
			(set_background_mesh, "mesh_draw_victory_khand"), # specific victory-loss image: khand VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_harad" ),
			(set_background_mesh, "mesh_draw_victory_harad"), # specific victory-loss image: harad VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_rhun" ),
			(set_background_mesh, "mesh_draw_victory_rhun"), # specific victory-loss image: rhun VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_beorn" ),
			(set_background_mesh, "mesh_draw_victory_beornings"), # specific victory-loss image: beorn VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_umbar" ),
			(set_background_mesh, "mesh_draw_victory_corsairs"), # specific victory-loss image: umbar VS anything
		(else_try),
			(eq, ":winning_side_faction", "fac_dale" ),
			(set_background_mesh, "mesh_draw_victory_dale"), # specific victory-loss image: dale VS anything
		(else_try),
			(eq, ":winning_side_race", tf_elf_begin),
			(eq, ":losing_side_race_group", tf_orc ),
			(set_background_mesh, "mesh_draw_lorien_arrows"),  # specific victory-loss image: elves VS orcs 
		(else_try),
			(eq, ":winning_side_faction", "fac_lorien" ),
			(set_background_mesh, "mesh_draw_victory_lorien"), # specific victory-loss image: lórien VS anything
		(else_try),
			# generic  defeat image: orcs....
			(eq, "$g_battle_result", -1), (eq, "$player_looks_like_an_orc", 1),
			(set_background_mesh,  "mesh_draw_defeat_orc"), 
		(else_try),
			# generic  defeat image: anybody else....
			(eq, "$g_battle_result", -1), (neq, "$player_looks_like_an_orc", 1),
			(set_background_mesh,  "mesh_draw_defeat_human"), 
		(try_end),
		
		# special case override: ent image 
		(try_begin),  
			(eq, "$g_encountered_party", "p_legend_fangorn"),
			(eq, "$g_battle_result", -1),
			# override the victory image with this ent image 
			(store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_ent_attack"), (set_background_mesh, reg10),
		(try_end),
	 (try_end),
	 
	 (str_clear, s11),
     (try_begin),
       (eq, "$g_battle_result", 1),
       (eq, "$g_enemy_fit_for_battle", 0),
       (str_store_string, s11, "@You were victorious!"),
#       (play_track, "track_bogus"), #clear current track.
#       (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
       #(try_begin),
			#(gt, "$g_friend_fit_for_battle", 1),
			#(set_background_mesh, "mesh_pic_victory"),

       #(try_end),
     (else_try),
       (eq, "$g_battle_result", -1),
       (ge, "$g_enemy_fit_for_battle",1),
       (this_or_next|le, "$g_friend_fit_for_battle",0),
       (             le, "$playerparty_postbattle_regulars", 0),
       (str_store_string, s11, "@The battle was lost. Your forces were utterly crushed."),
       #(set_background_mesh, "mesh_ui_default_menu_window"),
	   #(set_background_mesh, "mesh_pic_defeat"),
     (else_try),
       (eq, "$g_battle_result", -1),
       (str_store_string, s11, "@Your companions carry you away from the fighting."),
       #(troop_get_type, ":is_female", "trp_player"),
       #(try_begin),
       #  (eq, ":is_female", tf_female),
         #(set_background_mesh, "mesh_pic_wounded_fem"),
       #(else_try),
         #(set_background_mesh, "mesh_pic_wounded"),
       #(try_end),
     (else_try),
       (eq, "$g_battle_result", 1),
       (str_store_string, s11, "@You have defeated the enemy."),
       #(try_begin),
       #  (gt, "$g_friend_fit_for_battle", 1),
         #(set_background_mesh, "mesh_pic_victory"),
       #(try_end),
     (else_try),
       (eq, "$g_battle_result", 0),
       (str_store_string, s11, "@You have retreated from the fight."),
     (try_end),
#NPC companion changes begin
#check for excessive casualties, more forgiving if battle result is good
     (try_begin),
       (gt, "$playerparty_prebattle_regulars", 9),
       (store_add, ":divisor", 3, "$g_battle_result"), 
       (store_div, ":half_of_prebattle_regulars", "$playerparty_prebattle_regulars", ":divisor"),
       (lt, "$playerparty_postbattle_regulars", ":half_of_prebattle_regulars"),
       (call_script, "script_objectionable_action", tmt_egalitarian, "str_excessive_casualties"),
     (try_end),
#NPC companion changes end

	
     (call_script, "script_print_casualties_to_s0", "p_player_casualties", 0),
     (str_store_string_reg, s8, s0),
     (call_script, "script_print_casualties_to_s0", "p_enemy_casualties", 0),
     (str_store_string_reg, s9, s0),
     #(try_begin),
    # 	(gt, "$g_custom_battle_team1_death_count",0),
    # 	(assign, reg55, "$g_custom_battle_team1_death_count"),
  	# 	(str_store_string, s22, "@^ You Personally Defeated {reg55} Enemies"),
  	# (else_try),
  	# 	(str_store_string, s22, "@"),
  	# (try_end),
     (str_clear, s10),
     (try_begin),
       (eq, "$any_allies_at_the_last_battle", 1),
       (call_script, "script_print_casualties_to_s0", "p_ally_casualties", 0),
       (str_store_string, s10, "@^^Ally Casualties:{s0}"),
     (try_end),
	 # # kill troll quest (mtarini)
     # (try_begin),
       # (check_quest_active, "qst_kill_troll"),
       # (eq, "$g_battle_result", 1),
	   # (quest_get_slot, ":quest_object_troop","qst_kill_troll", slot_quest_target_party),
	   # (eq, ":quest_object_troop", "$g_enemy_party"),
	   # (call_script, "script_succeed_quest", "qst_kill_troll"),
     # (try_end),
    ],
	[
	 #options for players:
	 # capture troll quest troll quest (mtarini)
	 ("inspect_troll",
	  [(eq, "$g_battle_result", 1),
	   (check_quest_active, "qst_capture_troll"),
	   (party_get_template_id, ":j", "$g_enemy_party"),(eq,":j","pt_wild_troll"),
	  ],"Inspect downed troll",[ (jump_to_menu, "mnu_can_capture_troll")]) ,
	  
     ("continue",[],"Continue...",
	[
		(try_begin),
			(gt, "$g_next_menu", -1),
			(jump_to_menu, "$g_next_menu"),
		(else_try),
            		(change_screen_return),
		(try_end),
		(try_begin),(call_script, "script_cf_spawn_routed_parties"),(try_end),  
	]),
	],
 ),

( "total_victory",0,
    "You shouldn't be reading this... {s9}",
    "none",
    [   # We exploit the menu condition system below.
        # The conditions should make sure that always another screen or menu is called.
        (assign, ":done", 0),

	(call_script, "script_maybe_relocate_player_from_z0"),
	(try_begin),
		(ge, "$battle_won", 0), # (CppCoder): Battle was won, or was neutral
					# (CppCoder): Gonna do more testing, is this required? Even if a battle is lost, shouldn't the troops spawn?
		(call_script, "script_cf_spawn_routed_parties"), 
	(try_end),  
					  
		(assign, ":ambient_faction_backup", "$ambient_faction"), #TLD
        
        (try_begin),
          # Talk to ally leader
          (eq, "$thanked_by_ally_leader", 0),
          (assign, "$thanked_by_ally_leader", 1),
          
#TLD begin - do this only once
		  
		  #Get the Strength of the party AFTER the battle
		  (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
		  (assign, "$after_battle_enemy_strength", reg0),
		  (call_script, "script_party_calculate_strength", "p_main_party", 0),
		  (assign, "$after_battle_player_strength", reg0),

		  (call_script, "script_calculate_rank_gain_new"), 
	  	  (assign,":rank_increase", reg62),

		  # select what friendly faction was most interested in this victory (mtarini)
		  (assign, "$impressed_faction", "$players_kingdom"), # by default, it is player starting fatcion
		  (store_faction_of_party, ":defeated_faction", "$g_enemy_party"),
		
	      (str_store_faction_name, s4, ":defeated_faction"),
          #(display_log_message, "@DEBUG: player defeated a party of faction {s4}."),

		  (call_script, "script_find_closest_enemy_town_or_host", ":defeated_faction", "p_main_party"),
          (assign, ":impressed_party", reg0),
		
		  (try_begin),
		  	  (gt, "$g_ally_party", 0), #If there was an ally in battle, give their faction all the points. 
		  	  (store_faction_of_party, ":ally_faction","$g_ally_party"),
		  	  (str_store_party_name, s3, "$g_ally_party"),
  		  	  (display_log_message, "@You and {s3} celebrate your victory against {s4}.", color_good_news),
		  	  (call_script, "script_increase_rank", ":ally_faction", ":rank_increase"), 

		  (else_try),
			  (ge, ":impressed_party", 0), #If there was no ally in battle, check nearest faction
			  (str_store_party_name, s3, ":impressed_party"),
			  (store_faction_of_party, "$impressed_faction", ":impressed_party"),
			  (try_begin),
                (is_between, ":impressed_party", centers_begin, centers_end), 
                (display_log_message, "@News of your victory against {s4} reach {s3}.", color_good_news),
                
			  (else_try), 
				(display_log_message, "@{s3} witnesses your victory against {s4}.", color_good_news),
			  (try_end), 
              #(store_div, ":rank_increase", "$battle_renown_total", 2), # MV: give some rank increase according to renown (should be small 1-10) #was 4, now (1-20)
              
              (assign,":rank_increase", reg62), #Replaced by new formula
              
              #Debug:
              (try_begin),
				(troop_slot_eq, "trp_player", slot_troop_home, 22),
				(display_message, "@Debug: giving {reg62} rank points for impressed faction.", color_good_news),
			  (try_end),

              (call_script, "script_increase_rank", "$impressed_faction", ":rank_increase"),
		  (else_try),
		  	  (call_script, "script_party_get_dominant_faction", "p_main_party"), #Kham - Check dominant faction in player party and increase the rank from that faction
		  	  (assign, ":impressed_troop_faction", reg0),
		  	  #(store_div, ":rank_increase", "$battle_renown_total", 2), # MV: give some rank increase according to renown (should be small 1-10) #was 4, now (1-20)
		  	  (assign,":rank_increase", reg62), #Replaced by new formula
		  	  (call_script, "script_increase_rank", ":impressed_troop_faction", ":rank_increase"),
			  (display_log_message, "@Even though there were no allies to witness your victory, your troops nevertheless celebrate your triumph.", color_good_news), #Kham - Let's still give player some rank.
		  (try_end),

		  (call_script, "script_set_ambient_faction","$impressed_faction"),
          
          # Bravery trait check (chance greater if outnumbered; uses battle_renown_value=0-50 to figure it out)
		  (try_begin),
            (ge, "$battle_renown_value", 20), #minimum renown for being outnumbered
            (troop_slot_eq, "trp_traits", slot_trait_bravery, 0),
            (store_random_in_range, ":random", 0, 100),
            (ge, "$battle_renown_value", ":random"),
            (call_script, "script_gain_trait", slot_trait_bravery),
		  (try_end),
          
#TLD end
          
          (gt, "$g_ally_party", 0),
          
          (store_add, ":total_str_without_player", "$g_starting_strength_friends", "$g_starting_strength_enemy_party"),
          (val_sub, ":total_str_without_player", "$g_starting_strength_main_party"),
          (store_sub, ":ally_strength_without_player", "$g_starting_strength_friends", "$g_starting_strength_main_party"),
          (store_mul, ":ally_advantage", ":ally_strength_without_player", 100),
          (val_add, ":total_str_without_player", 1),
          (val_div, ":ally_advantage", ":total_str_without_player"),
          #Ally advantage=50  means battle was evenly matched

          (store_sub, ":enemy_advantage", 100, ":ally_advantage"),
        
          (store_mul, ":faction_reln_boost", ":enemy_advantage", "$g_starting_strength_enemy_party"),
          (val_div, ":faction_reln_boost", 300),
          (val_min, ":faction_reln_boost", 50), #was 40 in 3.1 
          (val_div, ":faction_reln_boost", 2), #MV: nerf to be close to normal battles - MV: upped a bit after 3.1 - MV: not used at all in 3.15, back to renown

          (store_mul, "$g_relation_boost", ":enemy_advantage", ":enemy_advantage"),
          (val_div, "$g_relation_boost", 700),
          (val_clamp, "$g_relation_boost", 0, 20),
        
          (party_get_num_companion_stacks, ":num_ally_stacks", "$g_ally_party"),
          (gt, ":num_ally_stacks", 0), # anybody survived
		  
          #(call_script, "script_change_player_relation_with_faction", ":ally_faction", ":faction_reln_boost"),
          (party_stack_get_troop_id, ":ally_leader", "$g_ally_party"),
          (party_stack_get_troop_dna, ":ally_leader_dna", "$g_ally_party"),
          (try_begin),
            (troop_is_hero, ":ally_leader"),
            (troop_get_slot, ":hero_relation", ":ally_leader", slot_troop_player_relation),
            (assign, ":rel_boost", "$g_relation_boost"),
            (try_begin),
              (lt, ":hero_relation", -5),
              (val_div, ":rel_boost", 3),
            (try_end),
            (call_script,"script_change_player_relation_with_troop", ":ally_leader", ":rel_boost"),
          (try_end),
          (assign, "$talk_context", tc_ally_thanks),
          (call_script, "script_setup_troop_meeting",":ally_leader", ":ally_leader_dna"),
        (else_try),
          # Talk to enemy leaders
          (assign, ":done", 0),
          (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
        
          (try_for_range, ":stack_no", "$last_defeated_hero", ":num_stacks"),
            (eq, ":done", 0),
            (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
            (party_stack_get_troop_dna,   ":stack_troop_dna","p_encountered_party_backup",":stack_no"),
            
            (troop_is_hero, ":stack_troop"),
            (store_add, "$last_defeated_hero", ":stack_no", 1),
        
            (call_script, "script_remove_troop_from_prison", ":stack_troop"),
            
            (troop_set_slot, ":stack_troop", slot_troop_leaded_party, -1),
            (store_troop_faction, ":defeated_faction", ":stack_troop"),

            (try_begin),
              (call_script, "script_cf_check_hero_can_escape_from_player", ":stack_troop"),
              (str_store_troop_name, s1, ":stack_troop"),
              (str_store_faction_name, s3, ":defeated_faction"),
              (str_store_string, s17, "@{s1} of {s3} managed to escape."),
              (display_log_message, "@{s17}"),
              (jump_to_menu, "mnu_enemy_slipped_away"),
              (assign, ":done", 1),
            (else_try),
              (assign, "$talk_context", tc_hero_defeated),
              (call_script, "script_setup_troop_meeting",":stack_troop", ":stack_troop_dna"),
              (assign, ":done", 1),
            (try_end),
          (try_end),
          (eq, ":done", 1),
        (else_try),
          # Talk to freed heroes
          (assign, ":done", 0),
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_encountered_party_backup"),
          (try_for_range, ":stack_no", "$last_freed_hero", ":num_prisoner_stacks"),
            (eq, ":done", 0),
            (party_prisoner_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
            (troop_is_hero, ":stack_troop"),
            (party_prisoner_stack_get_troop_dna,   ":stack_troop_dna","p_encountered_party_backup",":stack_no"),
            (store_add, "$last_freed_hero", ":stack_no", 1),
            (assign, "$talk_context", tc_hero_freed),
            (call_script, "script_setup_troop_meeting",":stack_troop", ":stack_troop_dna"),
            (assign, ":done", 1),
          (try_end),
          (eq, ":done", 1),
        (else_try),
          (eq, "$capture_screen_shown", 0),
          (assign, "$capture_screen_shown", 1),
          (party_clear, "p_temp_party"),

		  (party_set_faction, "p_temp_party", "$players_kingdom"),  # mtarini: need this to avoid to free enemyes
		
          (assign, "$g_move_heroes", 0),
          (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", "p_collective_enemy"),
          (call_script, "script_party_add_party_prisoners", "p_temp_party", "p_collective_enemy"),

          (try_begin),
            (call_script, "script_party_calculate_strength", "p_collective_friends_backup",0),
            (assign,":total_initial_strength", reg(0)),
            (gt, ":total_initial_strength", 0),
#            (gt, "$g_ally_party", 0),
            (call_script, "script_party_calculate_strength", "p_main_party_backup",0),
            (assign,":player_party_initial_strength", reg(0)),
            # move ally_party_initial_strength/(player_party_initial_strength + ally_party_initial_strength) prisoners to ally party.
            # First we collect the share of prisoners of the ally party and distribute those among the allies.
            (store_sub, ":ally_party_initial_strength", ":total_initial_strength", ":player_party_initial_strength"),


#            (call_script, "script_party_calculate_strength", "p_ally_party_backup"),
#            (assign,":ally_party_initial_strength", reg(0)),
#            (store_add, ":total_initial_strength", ":player_party_initial_strength", ":ally_party_initial_strength"),
            (store_mul, ":ally_share", ":ally_party_initial_strength", 1000),
            (val_div, ":ally_share", ":total_initial_strength"),
            (assign, "$pin_number", ":ally_share"), #we send this as a parameter to the script.
            (party_clear, "p_temp_party_2"),
            (call_script, "script_move_members_with_ratio", "p_temp_party", "p_temp_party_2"),
        
            #TODO: This doesn't handle prisoners if our allies joined battle after us.
            (try_begin),
              (gt, "$g_ally_party", 0),
              (distribute_party_among_party_group, "p_temp_party_2", "$g_ally_party"),
            (try_end),
             #next if there's anything left, we'll open up the party exchange screen and offer them to the player.
          (try_end),

          
          (party_get_num_companions, ":num_rescued_prisoners", "p_temp_party"),
          (try_begin),
            (check_quest_active, "qst_rescue_prisoners"),
            (quest_set_slot, "qst_rescue_prisoners", slot_quest_target_center, ":num_rescued_prisoners"), #abusing a slot as a global
          (try_end),
		  
		  
          (party_get_num_prisoners,  ":num_captured_enemies", "p_temp_party"),
          (store_add, ":total_capture_size", ":num_rescued_prisoners", ":num_captured_enemies"),
          (gt, ":total_capture_size", 0),
          (change_screen_exchange_with_party, "p_temp_party"),
        (else_try),
          (eq, "$loot_screen_shown", 0),
          (assign, "$loot_screen_shown", 1),
          
          (try_begin),
            (check_quest_active, "qst_rescue_prisoners"),
            (neg|check_quest_succeeded, "qst_rescue_prisoners"),
            (neg|check_quest_failed, "qst_rescue_prisoners"),
            (quest_get_slot, ":available", "qst_rescue_prisoners", slot_quest_target_center), #before...
            (party_get_num_companions, ":not_rescued", "p_temp_party"), #...and after
            (store_sub, ":rescued", ":available", ":not_rescued"),
            (gt, ":rescued", 0), #ignore dismissing troops
            (quest_get_slot, ":total_rescued", "qst_rescue_prisoners", slot_quest_current_state),
            (val_add, ":total_rescued", ":rescued"),
            (quest_set_slot, "qst_rescue_prisoners", slot_quest_current_state, ":total_rescued"),
            (assign, reg1, ":total_rescued"),
            (str_store_string, s2, "@Prisoners rescued so far: {reg1}"),
            (add_quest_note_from_sreg, "qst_rescue_prisoners", 3, s2, 0),
            (quest_get_slot, ":quest_target_amount", "qst_rescue_prisoners", slot_quest_target_amount),
            (try_begin),
              (ge, ":total_rescued", ":quest_target_amount"),
              (call_script, "script_succeed_quest", "qst_rescue_prisoners"),
            (try_end),
          (try_end),

          (try_begin),
            (gt, "$g_ally_party", 0),
            (call_script, "script_party_add_party", "$g_ally_party", "p_temp_party"), #Add remaining prisoners to ally TODO: FIX it.
          (else_try),
            (party_get_num_attached_parties, ":num_quick_attachments", "p_main_party"),
            (gt, ":num_quick_attachments", 0),
            (party_get_attached_party_with_rank, ":helper_party", "p_main_party", 0),
            (call_script, "script_party_add_party", ":helper_party", "p_temp_party"), #Add remaining prisoners to our reinforcements
          (try_end),
          (troop_clear_inventory, "trp_temp_troop"),
          (call_script, "script_party_calculate_loot", "p_encountered_party_backup"),
          (gt, reg0, 0),
          (troop_sort_inventory, "trp_temp_troop"),

	# Clean loot
	# This code cleans the inventory of other forbidden items, such as maggoty bread or human flesh
	 (troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop"),
	 (try_for_range, ":i_slot", 0, ":inv_cap"),
		(troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
		(try_begin),
			(faction_slot_eq,"$players_kingdom", slot_faction_side, faction_side_good),
			(eq|this_or_next, ":item_id", "itm_human_meat"),
			(eq, ":item_id", "itm_maggoty_bread"),
        		(troop_remove_item, "trp_temp_troop", ":item_id"),
		(try_end),
	  (try_end),
          (troop_sort_inventory, "trp_temp_troop"),	  

          (change_screen_loot, "trp_temp_troop"),
        (else_try),
          #finished all
          (try_begin),
            (le, "$g_ally_party", 0),
            (end_current_battle),
          (try_end),
		  
		  
          (call_script, "script_party_give_xp_and_gold", "p_encountered_party_backup"),
          (try_begin),
            (eq, "$g_enemy_party", 0),
            (display_message,"str_error_string"),
          (try_end),
          (call_script, "script_event_player_defeated_enemy_party", "$g_enemy_party"),
          (call_script, "script_clear_party_group", "$g_enemy_party", "$players_kingdom"),
          (try_begin),
            (eq, "$g_next_menu", -1),

#NPC companion changes begin
           (call_script, "script_post_battle_personality_clash_check"),
#NPC companion changes end

#Post 0907 changes begin
        (party_stack_get_troop_id,   ":enemy_leader","p_encountered_party_backup",0),
        (try_begin),
            (is_between, ":enemy_leader", kingdom_heroes_begin, kingdom_heroes_end),
            (neg|is_between, "$g_encountered_party", centers_begin, centers_end),
            (store_troop_faction, ":enemy_leader_faction", ":enemy_leader"),

            (try_begin),
                (eq, "$g_ally_party", 0),
                (call_script, "script_add_log_entry", logent_lord_defeated_by_player, "trp_player",  -1, ":enemy_leader", ":enemy_leader_faction"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  #(display_message, "@Victory comment. Player was alone"),
                (try_end),
            (else_try),
                (ge, "$g_strength_contribution_of_player", 40), 
                (call_script, "script_add_log_entry", logent_lord_defeated_by_player, "trp_player",  -1, ":enemy_leader", ":enemy_leader_faction"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  #(display_message, "@Ordinary victory comment. The player provided at least 40 percent forces."),
                (try_end),
            (else_try),
                (gt, "$g_starting_strength_enemy_party", 1000),
                (call_script, "script_get_closest_center", "p_main_party"),
                (assign, ":battle_of_where", reg0),
                (call_script, "script_add_log_entry", logent_player_participated_in_major_battle, "trp_player",  ":battle_of_where", -1, ":enemy_leader_faction"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  #(display_message, "@Player participation comment. The enemy had at least 1k starting strength."),
                (try_end),
            (else_try),
                (eq, "$cheat_mode", 1),
                #(display_message, "@No victory comment. The battle was small, and the player provided less than 40 percent of allied strength"),
            (try_end),
        (try_end),
#Post 0907 changes end
            (val_add, "$g_total_victories", 1),
            
            # MV: handle post-victory quest checks
            (try_begin),
              # fail if messenger died in a battle
              (check_quest_active, "qst_escort_messenger"),
              (quest_get_slot, ":quest_object_troop", "qst_escort_messenger", slot_quest_object_troop),
              (party_count_companions_of_type, ":amount", "p_main_party", ":quest_object_troop"),
              (eq, ":amount", 0),
              (call_script, "script_abort_quest", "qst_escort_messenger", 1),
              #(call_script, "script_change_player_honor", -5),
            (try_end),
              ##Kham - Ring Hunters Quest - Messenger Start
           	(try_begin),
          		(check_quest_active, "qst_ring_hunters"),(quest_slot_eq,"qst_ring_hunters",slot_quest_current_state,14),
          		(eq,"$qst_ring_hunter_party","$g_enemy_party"),
          		(disable_party,"p_ring_hunter_lair"),                  
      			(quest_set_slot, "qst_ring_hunters", slot_quest_current_state, 15),
      			(set_spawn_radius,1),
      			(spawn_around_party, "p_main_party", "pt_beorn_messenger"),
      			(assign,":beorn_m",reg0),
      			(party_set_ai_behavior, ":beorn_m", ai_bhvr_attack_party),
    			(party_set_ai_object, ":beorn_m", "p_main_party"),
           	(try_end),
          	###Kham - Ring Hunters Quest - Messenger End
            # kill troll quest
            (try_begin),
              (check_quest_active, "qst_kill_troll"),
              (quest_get_slot, ":troll_party", "qst_kill_troll", slot_quest_target_party),
              (try_begin),
                (eq, ":troll_party", "$g_enemy_party"),
                (call_script, "script_succeed_quest", "qst_kill_troll"),
              (else_try),
                (party_get_num_attached_parties, ":num_attached_parties",  "$g_enemy_party"),
                (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
                  (party_get_attached_party_with_rank, ":attached_party", "$g_enemy_party", ":attached_party_rank"),
                  (eq, ":troll_party", ":attached_party"),
                  (call_script, "script_succeed_quest", "qst_kill_troll"),
                (try_end),
              (try_end),
            (try_end),

		# Spawn routed parties after battle. -CC
		(try_begin),(call_script, "script_cf_spawn_routed_parties"),(try_end),    

            (leave_encounter),
            (change_screen_return),
            (assign, "$new_rank_formula_calculated", 0),
          (else_try),
            (jump_to_menu, "$g_next_menu"),
          (try_end),
        (try_end),
		
		(call_script, "script_set_ambient_faction",":ambient_faction_backup"),
		
		# TLD injure your KO-ed companions
		(try_begin),
			(eq, "$tld_option_injuries",1),
			(try_for_range, ":npc",companions_begin,companions_end), # assume companions are always in our main party, if ever spawned on battlefield
				(main_party_has_troop,":npc"),
				(troop_slot_eq, ":npc", slot_troop_wounded, 1), # was wounded in this battle?
				(troop_set_slot,":npc", slot_troop_wounded, 0),
				(store_random_in_range, reg12,0,10),
				(eq,reg12,0), #10% chance for injury
				(call_script,"script_injury_routine", ":npc"), # chances to get injury halved when victory
			(try_end),
			(try_for_range, ":npc",new_companions_begin,new_companions_end), # assume companions are always in our main party, if ever spawned on battlefield
				(main_party_has_troop,":npc"),
				(troop_slot_eq, ":npc", slot_troop_wounded, 1), # was wounded in this battle?
				(troop_set_slot,":npc", slot_troop_wounded, 0),
				(store_random_in_range, reg12,0,10),
				(eq,reg12,0), #10% chance for injury
				(call_script,"script_injury_routine", ":npc"), # chances to get injury halved when victory
			(try_end),
		(try_end),
		## Kham - Oath of Vengeance Kills Start
		(try_begin),
			(check_quest_active, "qst_oath_of_vengeance"),
			(quest_get_slot, ":target","qst_oath_of_vengeance", 2),
			(quest_get_slot, ":moria", "qst_oath_of_vengeance",6),
			(try_begin),
				(gt, ":moria",0),
				(quest_get_slot, ":gundabad", "qst_oath_of_vengeance",7),
				(this_or_next|eq, ":defeated_faction",  ":target"),
				(eq, ":defeated_faction", ":gundabad"),
				(get_player_agent_kill_count, ":temp_kills"),
				(val_sub, ":temp_kills", "$total_kills"),
				(val_add, "$oath_kills", ":temp_kills"),
			(else_try),
				(eq, ":defeated_faction",  ":target"),
				(get_player_agent_kill_count, ":temp_kills"),
				(val_sub, ":temp_kills", "$total_kills"),

				## Dwarves & Elves count twice
					(try_begin),
						(this_or_next|eq, ":defeated_faction", fac_imladris),
						(this_or_next|eq, ":defeated_faction", fac_woodelf),
						(this_or_next|eq, ":defeated_faction", fac_lorien),
						(			  eq, ":defeated_faction", fac_dwarf),
						(val_mul, ":temp_kills", 2), 
						(val_add, "$oath_kills", ":temp_kills"),
					(else_try),
						(val_add, "$oath_kills", ":temp_kills"),
					(try_end),	
			(try_end),
			(try_begin),
				(eq, "$cheat_mode",1),
				(assign, reg1, "$oath_kills"),
				(assign, reg0, "$total_kills"),
				(str_store_faction_name, s1, ":target"),
				(display_message, "@{reg1} kills of {s1} faction troops counted towards Oath. TOTAL Kills: {reg0}"),
			(try_end),
		(try_end),
		(get_player_agent_kill_count, "$total_kills"),
		## Kham - Oath of Vengeance Kills END
		## Kham - Eliminate Patrols Assist START
		(try_begin),
			(check_quest_active, "qst_eliminate_patrols"),
			(quest_get_slot, ":target_pt", "qst_eliminate_patrols", slot_quest_target_party_template),
			(party_get_template_id, ":current_target", "$g_enemy_party"),
			(eq, ":current_target", ":target_pt"),
			(quest_set_slot, "qst_eliminate_patrols", slot_quest_target_troop, ":current_target"), #slot to store target template 
			(try_begin),
				(eq, "$cheat_mode",1),
				(eq, ":current_target",":target_pt"),
				(display_message, "@DEBUG: Target Party - YES"),
			(else_try),
				(eq, "$cheat_mode",1),
				(display_message, "@DEBUG: Target Party - NO"),
			(try_end),
		(try_end),
		## Kham - Eliminate Patrols Assist END

		## Kham - Defeat Target Lord START
		(try_begin),
			(check_quest_active, "qst_blank_quest_06"),
			(quest_get_slot, ":target_lord", "qst_blank_quest_06", slot_quest_target_troop),
			(troop_get_slot, ":party", ":target_lord", slot_troop_leaded_party),
			(eq, ":party", "$g_enemy_party"),
			(call_script, "script_succeed_quest", "qst_blank_quest_06"),
		(else_try),
			(check_quest_active, "qst_blank_quest_06"),
			(quest_get_slot, ":target_lord", "qst_blank_quest_06", slot_quest_target_troop),
			(troop_get_slot, ":party", ":target_lord", slot_troop_leaded_party),
			(neq, ":party", "$g_enemy_party"),
			(party_get_num_companion_stacks, ":num_stacks", "p_collective_enemy"),
			(assign, ":found", 0),
			(try_for_range, ":stacks", 0, ":num_stacks"),
	  			(eq, ":found", 0),
				(party_stack_get_troop_id, ":stack_troop", "p_collective_enemy", ":stacks"),
	  			(troop_is_hero, ":stack_troop"),
	  			(eq, ":stack_troop", ":target_lord"),
	  			(assign, ":found", 1),
	  			(call_script, "script_succeed_quest", "qst_blank_quest_06"),
	  		(try_end),
		(try_end),
		## Kham - Eliminate Patrols Assist END

		## Kham - Refugees Quest Start

		(try_begin),
			(check_quest_active, "qst_blank_quest_01"),
			(this_or_next|eq, "$g_enemy_party", "$qst_raider_party_1"),
			(this_or_next|eq, "$g_enemy_party", "$qst_raider_party_2"),
			(			  eq, "$g_enemy_party", "$qst_raider_party_3"),
			(val_add, "$qst_raider_party_defeated", 1),
		(try_end),

		## Kham - Refugees Quest End

      ],
    [("continue",[],"Continue...",[(change_screen_return)]),]
 ),
( "enemy_slipped_away",0,
    "^^^^^{s17}",
    "none",
    [],
    [("continue",[],"Continue...",[(jump_to_menu,"mnu_total_victory")]),]
 ),
( "total_defeat",0,
    "You shouldn't be reading this...",
    "none",
    [     (play_track, "track_captured", 1),
		  (call_script, "script_maybe_relocate_player_from_z0"),
          # Free prisoners
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_main_party"),
          (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
            (party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
            (troop_is_hero, ":stack_troop"),
            (call_script, "script_remove_troop_from_prison", ":stack_troop"),
          (try_end),

          (call_script, "script_loot_player_items", "$g_enemy_party"),
          (assign, "$g_move_heroes", 0),
          (party_clear, "p_temp_party"),
		  (store_faction_of_party, ":fac","$g_enemy_party"),
		  (party_set_faction, "p_temp_party", ":fac"),

          (call_script, "script_party_add_party_prisoners", "p_temp_party", "p_main_party"),
          (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", "p_main_party"),
          (distribute_party_among_party_group, "p_temp_party", "$g_enemy_party"),
        
          (call_script, "script_party_remove_all_companions", "p_main_party"),
          (assign, "$g_move_heroes", 1),
          (call_script, "script_party_remove_all_prisoners", "p_main_party"),

          (val_add, "$g_total_defeats", 1),
            
          # MV: handle post-defeat quest checks
          (try_begin),
            (check_quest_active, "qst_escort_messenger"),
            (call_script, "script_abort_quest", "qst_escort_messenger", 1),
            #(call_script, "script_change_player_honor", -5),
          (try_end),

           (try_begin), #No luck in TLD
             (store_random_in_range, ":random_no", 0, 1),
             (ge, ":random_no", "$g_player_luck"),
             (jump_to_menu, "mnu_permanent_damage"),
           (else_try),
            (try_begin),
              (eq, "$g_next_menu", -1),
              (leave_encounter),
              (change_screen_return),
            (else_try),
              (jump_to_menu, "$g_next_menu"),
            (try_end),
          (try_end),
          (try_begin),
            (gt, "$g_ally_party", 0),
            (call_script, "script_party_wound_all_members", "$g_ally_party"),
          (try_end),

	#Troop commentary changes begin
          (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
          (try_for_range, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
            (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
            (store_troop_faction, ":victorious_faction", ":stack_troop"),
            (call_script, "script_add_log_entry", logent_player_defeated_by_lord, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
          (try_end),
	#Troop commentary changes end
			# TLD injure your KO-ed companions
			(try_begin),
				(eq, "$tld_option_injuries",1),
				(try_for_range, ":npc",companions_begin,companions_end), # assume companions are always in our main party, if ever spawned on battlefield
					(main_party_has_troop,":npc"),
					(troop_slot_eq, ":npc", slot_troop_wounded, 1), # was wounded in this battle?
					(troop_set_slot,":npc", slot_troop_wounded, 0),
					(store_random_in_range, reg12,0,5),
					(eq,reg12,0), #20% chance for injury
					(call_script, "script_injury_routine", ":npc"),
				(try_end),
				(try_for_range, ":npc",new_companions_begin,new_companions_end), # assume companions are always in our main party, if ever spawned on battlefield
					(main_party_has_troop,":npc"),
					(troop_slot_eq, ":npc", slot_troop_wounded, 1), # was wounded in this battle?
					(troop_set_slot,":npc", slot_troop_wounded, 0),
					(store_random_in_range, reg12,0,5),
					(eq,reg12,0), #20% chance for injury
					(call_script, "script_injury_routine", ":npc"),
				(try_end),
			(try_end),
      ],
    []
 ),

#No luck system in TLD
( "permanent_damage",mnf_disable_all_keys, 
    "^^^^^{s0}",
    "none",
    [ (assign, ":end_cond", 1),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_attribute", 0, 4),
        (store_attribute_level, ":attr_level", "trp_player", ":random_attribute"),
        (try_begin),
          (gt, ":attr_level", 3),
          (neq, ":random_attribute", ca_charisma),
          # (try_begin),
            # (eq, ":random_attribute", ca_strength),
            # (str_store_string, s0, "@Some of your tendons have been damaged in the battle. You lose 1 strength."),
          # (else_try),
            # (eq, ":random_attribute", ca_agility),
            # (str_store_string, s0, "@You took a nasty wound which will cause you to limp slightly even after it heals. Your lose 1 agility."),
# ##          (else_try),
# ##            (eq, ":random_attribute", ca_charisma),
# ##            (str_store_string, s0, "@After the battle you are aghast to find that one of the terrible blows you suffered has left a deep, disfiguring scar on your face, horrifying those around you. Your charisma is reduced by 1."),
          # (else_try),
# ##            (eq, ":random_attribute", ca_intelligence),
            # (str_store_string, s0, "@You have trouble thinking straight after the battle, perhaps from a particularly hard hit to your head, and frequent headaches now plague your existence. Your intelligence is reduced by 1."),
          # (try_end),
        (else_try),
          (lt, ":end_cond", 200),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":end_cond", 200),
        (try_begin),
          (eq, "$g_next_menu", -1),
          (leave_encounter),
          (change_screen_return),
        (else_try),
          (jump_to_menu, "$g_next_menu"),
        (try_end),
      (else_try),
        (troop_raise_attribute, "trp_player", ":random_attribute", -1),
      (try_end),
      ],
    [
      ("s0",
       [
         (store_random_in_range, ":random_no", 0, 4),
         (try_begin),
           (eq, ":random_no", 0),
           (str_store_string, s0, "@Perhaps I'm getting unlucky..."),
         (else_try),
           (eq, ":random_no", 1),
           (str_store_string, s0, "@Retirement is starting to sound better and better."),
         (else_try),
           (eq, ":random_no", 2),
           (str_store_string, s0, "@No matter! I will persevere!"),
         (else_try),
           (eq, ":random_no", 3),
           (troop_get_type, ":is_female", "trp_player"),
           (try_begin),
             (eq, ":is_female", 1),
             (str_store_string, s0, "@What did I do to deserve this?"),
           (else_try),
             (str_store_string, s0, "@I suppose it'll make for a good story, at least..."),
           (try_end),
         (try_end),
         ],
       "{s0}",
       [
         (try_begin),
           (eq, "$g_next_menu", -1),
           (leave_encounter),
           (change_screen_return),
         (else_try),
           (jump_to_menu, "$g_next_menu"),
         (try_end),
         ]),
      ]
 ),
  
( "pre_join",0,
    "^^^^^You come across a battle between {s2} and {s1}. You decide to...",
    "none",
    [ (str_store_party_name, 1,"$g_encountered_party"),
      (str_store_party_name, 2,"$g_encountered_party_2"),
    ],
    [ ("pre_join_help_attackers",
	  [   (store_faction_of_party, ":attacker_faction", "$g_encountered_party_2"),
          (store_relation, ":attacker_relation", ":attacker_faction", "fac_player_supporters_faction"),
          (store_faction_of_party, ":defender_faction", "$g_encountered_party"),
          (store_relation, ":defender_relation", ":defender_faction", "fac_player_supporters_faction"),
          (ge, ":attacker_relation", 0),
          (lt, ":defender_relation", 0),
          ],
          "Move in to help the {s2}.",[
              (select_enemy,0),
              (assign,"$g_enemy_party","$g_encountered_party"),
              (assign,"$g_ally_party","$g_encountered_party_2"),
              (jump_to_menu,"mnu_join_battle")]),
      ("pre_join_help_defenders",[
          (store_faction_of_party, ":attacker_faction", "$g_encountered_party_2"),
          (store_relation, ":attacker_relation", ":attacker_faction", "fac_player_supporters_faction"),
          (store_faction_of_party, ":defender_faction", "$g_encountered_party"),
          (store_relation, ":defender_relation", ":defender_faction", "fac_player_supporters_faction"),
          (ge, ":defender_relation", 0),
          (lt, ":attacker_relation", 0),
          ],
          "Rush to the aid of the {s1}.",[
              (select_enemy,1),
              (assign,"$g_enemy_party","$g_encountered_party_2"),
              (assign,"$g_ally_party","$g_encountered_party"),
              (jump_to_menu,"mnu_join_battle")]),
      ("pre_join_help_refugees",[
         (this_or_next|eq, "$g_encountered_party_2", "$qst_raider_party_1"),
         (this_or_next|eq, "$g_encountered_party_2", "$qst_raider_party_2"),
         (			   eq, "$g_encountered_party_2", "$qst_raider_party_3"),
          ],
          "Rush to the aid of the {s1}.",[
              (select_enemy,1),
              (assign,"$g_enemy_party","$g_encountered_party_2"),
              (assign,"$g_ally_party","$g_encountered_party"),
              (jump_to_menu,"mnu_join_battle")]),
      ("pre_join_leave",[],"Don't get involved.",[(leave_encounter),(change_screen_return)]),
    ]
 ),
( "join_battle",mnf_enable_hot_keys,
    "^^^You are helping {s2} against {s1}.^ You have {reg22} troops fit for battle against the enemy's {reg11}.^^The battle is taking place in {s3}{s4}.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
	
		#(party_get_current_terrain, "$current_player_terrain","p_main_party"),
		#(call_script, "script_get_region_of_party","p_main_party"),(assign, "$current_player_region", reg1),	
		#(call_script, "script_get_close_landmark","p_main_party"), (assign, "$current_player_landmark", reg0),
		
		(store_add, reg2, str_shortname_region_begin, "$current_player_region"),
		(str_store_string,s3,reg2),
		
		(str_clear, s4),
		(try_begin), 
			(call_script, "script_cf_store_landmark_description_in_s17", "$current_player_landmark"),
			(str_store_string,s4,"@, {s17}"), 
		(try_end),
		
		(str_store_party_name, 1,"$g_enemy_party"),
        (str_store_party_name, 2,"$g_ally_party"),
        (call_script, "script_encounter_calculate_fit"),
        (assign, reg22, reg10), 

        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (call_script, "script_encounter_init_variables"),
##          (assign, "$capture_screen_shown", 0),
##          (assign, "$loot_screen_shown", 0),
##          (assign, "$g_battle_result", 0),
##          (assign, "$cant_leave_encounter", 0),
##          (assign, "$last_defeated_hero", 0),
##          (assign, "$last_freed_hero", 0),
##          (call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
##          (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"),
##          (call_script, "script_party_copy", "p_ally_party_backup", "p_collective_ally"),
        (else_try), #second or more turn
          (eq, "$g_leave_encounter",1),
		  (call_script, "script_maybe_relocate_player_from_z0"),
          (change_screen_return),
        (try_end),

        (try_begin),
          (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
          (assign, ":num_enemy_regulars_remaining", reg0),
          (assign, ":enemy_finished",0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (this_or_next|le, ":num_enemy_regulars_remaining", 0), #battle won
          	(le, ":num_enemy_regulars_remaining", "$num_routed_enemies"), #Kham - routed enemies don't get spawned

          	(assign, ":continue", 0),
          	(try_begin),
          		(gt, reg11, 0),
          		(store_div, ":player_to_enemy_ratio", reg22, reg11),
          		(gt, ":player_to_enemy_ratio", 5), #test for routed enemies again...
          		(assign, ":continue", 1),
          	(else_try),
          		(le, reg11, 0),
          		(assign, ":continue", 1),
          	(try_end),

          	(eq, ":continue", 1),
          	(assign, ":enemy_finished", 1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),
            (le, "$g_enemy_fit_for_battle",0),
            (ge, "$g_friend_fit_for_battle",1),
            (assign, ":enemy_finished",1),
          (try_end),
          (this_or_next|eq, ":enemy_finished",1),
          (eq,"$g_enemy_surrenders",1),
          (assign, "$g_next_menu", -1),
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
#          (eq, "$encountered_party_hostile", 1),
          (call_script, "script_party_count_members_with_full_health","p_collective_friends"),
          (assign, ":ally_num_soldiers", reg(0)),
          (assign, ":battle_lost", 0),
          (try_begin),
            (eq, "$g_battle_result", -1),
            #(eq, ":ally_num_soldiers", 0), #battle lost
            (le, ":ally_num_soldiers",  "$num_routed_allies"), #kham - routed enemies don't get spawned
            (assign, ":battle_lost",1),
          (try_end),
          (this_or_next|eq, ":battle_lost",1),
          (eq,"$g_player_surrenders",1),
        # TODO: Split prisoners to all collected parties.
        # NO Need? Let default battle logic do it for us. 
#          (assign, "$g_move_heroes", 0),
#          (call_script, "script_party_add_party_prisoners", "$g_enemy_party", "p_collective_ally"),
#          (call_script, "script_party_prisoners_add_party_companions", "$g_enemy_party", "p_collective_ally"),
        #TODO: Clear all attached allies.
#          (call_script, "script_party_remove_all_companions", "$g_ally_party"),
#          (call_script, "script_party_remove_all_prisoners", "$g_ally_party"),
          (leave_encounter),
          (change_screen_return),
        (try_end),
        
	#Calculate Formula A here - Kham
	(try_begin), 
		(eq, "$new_rank_formula_calculated", 0),
		(call_script, "script_calculate_formula_a"),
		(assign, "$nf_helping_allies", 1),
	(try_end),
	#Calculate Formula A END
      ],
    [ ("join_attack",[
#          (neq, "$encountered_party_hostile", 0),
          #(neg|troop_is_wounded, "trp_player"),
##          (store_troop_health,reg(5),"trp_player"),
##          (ge,reg(5),20),
          ],
                            "Charge the enemy.",[
                                (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
                                (assign, "$g_battle_result", 0),
                                (call_script, "script_calculate_renown_value"),
                                (call_script, "script_calculate_battle_advantage"),(set_battle_advantage, reg0),
                                (call_script, "script_calculate_battleside_races"),
                                
                                (set_party_battle_mode),
                                (set_jump_mission,"mt_lead_charge"),
								
                                (call_script, "script_jump_to_random_scene","$current_player_region","$current_player_terrain","$current_player_landmark"),
                                (assign, "$g_next_menu", "mnu_join_battle"),
                                (jump_to_menu, "mnu_battle_debrief"),
                                (change_screen_mission),
                                ]),

      ("join_order_attack",[
#          (gt, "$encountered_party_hostile", 0),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),(ge, reg(0), 3),
          ],
           "Order your troops to attack with your allies while you stay back.",[(party_set_next_battle_simulation_time, "$g_encountered_party", -1),
                                                                         (jump_to_menu,"mnu_join_order_attack"),
                                                            ]),
      
#      ("join_attack",[],"Lead a charge against the enemies",[(set_jump_mission,"mt_charge_with_allies"),
#                                (call_script, "script_setup_random_scene"),
#                                                             (change_screen_mission,0)]),


      # Kham - Control Allies for Inf Points
      ("control_allies_join_menu", [
      	#(eq, "$cheat_mode", 1),
  	    (call_script, "script_get_faction_rank", "$players_kingdom"), (assign, ":rank", reg0), #rank points to rank number 0-9
     	(ge, ":rank", 3), #Must be at least rank 3
      	(neq, "$player_control_allies", 1),
      	(party_get_num_companion_stacks, ":num_stacks", "p_collective_friends"),
      	(assign, ":num_lords", 0),
      	(try_for_range, ":stack_no", 0, ":num_stacks"),
      		(party_stack_get_troop_id,   ":stack_troop","p_collective_friends",":stack_no"),
      		(is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
      		(val_add, ":num_lords", 1),
      	(try_end),
      	(gt, ":num_lords", 0), # have to have lords in battle
      	],
      	 "Use Influence Points to Command Your Allies in the Field.", [
      		(jump_to_menu, "mnu_player_control_allies_join"),
      ]),] + (is_a_wb_menu==1 and [("join_attack_bearform",[
          # BEAR SHAPESHIFT OPTION
          (this_or_next|troop_slot_eq, "trp_traits", slot_trait_bear_shape, 1),
          (eq, "$cheat_mode", 1),
        ],
        "Leap_into_battle_in_bear_form",[
            (call_script, "script_cf_select_bear_form"), # Select bear form
            (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
            (assign, "$g_battle_result", 0),
            (call_script, "script_calculate_renown_value"),
            (call_script, "script_calculate_battle_advantage"),(set_battle_advantage, reg0),
            (call_script, "script_calculate_battleside_races"),
            (set_party_battle_mode),
            (set_jump_mission,"mt_lead_charge"),
                                            
            (call_script, "script_jump_to_random_scene","$current_player_region","$current_player_terrain","$current_player_landmark"),
            (assign, "$g_next_menu", "mnu_join_battle"),
            (jump_to_menu, "mnu_battle_debrief"),
            (change_screen_mission),
        ]),
    ] or []) + [
      ("join_leave",[],"Disengage.",[
        (try_begin),
           #(neg|troop_is_wounded, "trp_player"),
           (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
           (party_stack_get_troop_id, ":enemy_leader","$g_enemy_party",0),
           (call_script, "script_add_log_entry", logent_player_retreated_from_lord, "trp_player",  -1, ":enemy_leader", -1),
           (display_message, "@You retreated from battle."),
        (try_end),
        (leave_encounter),(change_screen_return)]),
		  
    ("join_cheat_heal",[
         (eq, "$cheat_mode",1),
		 (store_troop_health  , reg20, "trp_player",0), (lt, reg20,95),
          ],"CHEAT: heal yourself.",[
		    (troop_set_health  , "trp_player",100),
	        (display_message, "@CHEAT: healed!!!"),
			(jump_to_menu, "mnu_pre_join"),
		]),
    ]
),

# Player Control Allies Join

("player_control_allies_join", 0, 
	"^^^^^{s60}^^^", "none",
	[(set_background_mesh, "mesh_ui_default_menu_window"),
     (gt, "$g_starting_strength_friends", 0), # we have allies
     (neq, "$player_control_allies", 1),
     (party_get_num_companion_stacks, ":num_stacks", "p_collective_friends"),
     (party_get_num_companions, ":num_companions", "p_collective_friends"),
     (assign, ":num_lords", 0),
     (assign, ":base_inf_cost", player_control_allies_inf),
     (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id,   ":stack_troop","p_collective_friends",":stack_no"),
        (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
        (val_add, ":num_lords", 1),
     (try_end),
     (gt, ":num_lords", 0), # have to have lords in battle
     (assign, reg39, ":num_lords"),
     (store_div, ":divide", ":num_companions", 40),
     (val_max, ":divide", 0),
     (try_begin),
        (gt, ":num_lords", 1),
        (val_mul, ":num_lords", 3),
     (try_end),
     (val_add, ":base_inf_cost", ":num_lords"),
     (val_add, ":base_inf_cost", ":divide"),
     (assign, reg40, ":base_inf_cost"),
     (str_store_string, s60, "@There are {reg39} ally commanders in this battle. You can command them and their troops for {reg40} influence points."),
    ],[
		("player_control_allies_join_menu", [], "Command them and charge the enemy", [
			(call_script, "script_spend_influence_of", reg40, "$players_kingdom"),
			(assign, "$player_control_allies", 1),
			(party_set_next_battle_simulation_time, "$g_encountered_party", -1),
			(assign, "$g_battle_result", 0),
			(call_script, "script_calculate_renown_value"),
			(call_script, "script_calculate_battle_advantage"),(set_battle_advantage, reg0),
			(call_script, "script_calculate_battleside_races"),
			
			(set_party_battle_mode),
			(set_jump_mission,"mt_lead_charge"),
			
			(call_script, "script_jump_to_random_scene","$current_player_region","$current_player_terrain","$current_player_landmark"),
			(assign, "$g_next_menu", "mnu_join_battle"),
			(jump_to_menu, "mnu_battle_debrief"),
			(change_screen_mission),]),
		("player_control_allies_back", [], "Go back...", [
			(jump_to_menu, "mnu_join_battle"),]),
	]),


( "join_order_attack",mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    [	(set_background_mesh, "mesh_ui_default_menu_window"),

	    	(call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
		(assign, ":player_party_strength", reg0),
		(val_div, ":player_party_strength", 5),

		(call_script, "script_party_calculate_strength", "p_collective_friends", 0),
		(assign, ":friend_party_strength", reg0),
		(val_div, ":friend_party_strength", 5),
		
		(call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
		(assign, ":enemy_party_strength", reg0),
		(val_div, ":enemy_party_strength", 5),

		(assign, ":enemy_party_strength_for_p", ":enemy_party_strength"),
		(val_mul, ":enemy_party_strength_for_p", ":player_party_strength"),
		(val_div, ":enemy_party_strength_for_p", ":friend_party_strength"),

		(val_sub, ":enemy_party_strength", ":enemy_party_strength_for_p"),
		(inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength_for_p", "p_temp_casualties"),
		(call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
		(str_store_string_reg, s8, s0),
		
		(inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties"),
		(call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
		(str_store_string_reg, s10, s0),
		
		(call_script, "script_collect_friendly_parties"),
#                                    (party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),

		(inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
		(call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
		(str_store_string_reg, s9, s0),
		(party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

#                                    (assign, "$cant_leave_encounter", 0),
		(assign, "$no_soldiers_left", 0),
		(try_begin),
		  (call_script, "script_party_count_members_with_full_health","p_main_party"),
		  (assign, ":num_our_regulars_remaining", reg0),
          (le, ":num_our_regulars_remaining", "$num_routed_us"), #Kham - routed allies do not spawn again
		  (assign, "$no_soldiers_left", 1),
		  (str_store_string, s4, "str_join_order_attack_failure"),
		(else_try),
		  (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
		  (assign, ":num_enemy_regulars_remaining", reg0),
          (this_or_next|le, ":num_enemy_regulars_remaining", 0),
          (le, ":num_enemy_regulars_remaining", "$num_routed_enemies"), #Kham - routed allies do not spawn again
		  (assign, "$g_battle_result", 1),
		  (assign, "$no_soldiers_left", 1),
		  (str_store_string, s4, "str_join_order_attack_success"),
		(else_try),
		  (str_store_string, s4, "str_join_order_attack_continue"),
		(try_end),
    ],
    [("continue",[],"Continue...",[(jump_to_menu,"mnu_join_battle")])]
 ),

( "test_scene",mnf_auto_enter,
    "You enter the test scene.",
    "none",
    [],
    [ ("enter",[],"Enter.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_test_scene"],[change_screen_mission]]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
 ),

( "battlefields",0,
    "^^^^^^^^^Select a field...",
    "none",
    [],
    [ ("enter_f1",[],"Field 1",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_1"],[change_screen_mission]]),
      ("enter_f2",[],"Field 2",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_2"],[change_screen_mission]]),
      ("enter_f3",[],"Field 3",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_3"],[change_screen_mission]]),
      ("enter_f4",[],"Field 4",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_4"],[change_screen_mission]]),
      ("enter_f5",[],"Field 5",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_5"],[change_screen_mission]]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
 ),

( "join_siege_outside",0,
    "^^^^^^{s1} has come under siege by {s2}.",
    "none",
    code_to_set_city_background + [ 
	    (str_store_party_name, s1, "$g_encountered_party"),
        (str_store_party_name, s2, "$g_encountered_party_2"),
    ],
    [ ("approach_besiegers",[(store_faction_of_party, ":faction_no", "$g_encountered_party_2"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (ge, ":relation", 0),
                             (store_faction_of_party, ":faction_no", "$g_encountered_party"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (lt, ":relation", 0),
                             ],"Approach the siege camp.",[
          (jump_to_menu, "mnu_besiegers_camp_with_allies"),
                                ]),
      ("pass_through_siege",[(store_faction_of_party, ":faction_no", "$g_encountered_party"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (ge, ":relation", 0),
                             ],"Pass through the siege lines and enter {s1}.",
       [
            (jump_to_menu,"mnu_cut_siege_without_fight"),
          ]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
 ),
( "cut_siege_without_fight",0,
    "The besiegers let you approach the gates without challenge.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),],
    [
      ("continue",[],"Continue...",[(try_begin),
                                   (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                                   (eq, "$g_encountered_party_faction", "$players_kingdom"),
                                   (jump_to_menu, "mnu_town"),
                                 (else_try),
                                   (jump_to_menu, "mnu_castle_outside"),
                                 (try_end)]),
      ]
 ),
( "besiegers_camp_with_allies",mnf_enable_hot_keys,
    "{s1} remains under siege. The banners of {s2} fly above the camp of the besiegers,\
    where you and your troops are welcomed.",
    "none",
    code_to_set_city_background + [
        (str_store_party_name, s1, "$g_encountered_party"),
        (str_store_party_name, s2, "$g_encountered_party_2"),
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", "$g_encountered_party_2"),
        (select_enemy, 0),
        (call_script, "script_encounter_calculate_fit"),
        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (call_script, "script_encounter_init_variables"),
        (try_end),

        (try_begin),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (else_try),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
            (assign, "$g_next_menu", -1),
            (jump_to_menu, "mnu_battle_debrief"),
            #(display_message, "@DEBUG: ENEMY FINISHED - NEXT MENU Total Vic"),
          (else_try),
            (this_or_next|le, "$g_enemy_fit_for_battle",0),
          	(le, "$g_enemy_fit_for_battle", "$num_routed_enemies"),  #Kham - don't let routed enemies spawn again
            (assign, ":enemy_finished", 1),
            (assign, "$g_next_menu", -1),
            (jump_to_menu, "mnu_battle_debrief"),
            #(display_message, "@DEBUG: ENEMY FINISHED 2 - NEXT MENU Total Vi"),
          (try_end),
          (this_or_next|eq, ":enemy_finished", 1),
          (eq, "$g_enemy_surrenders", 1),
         ## (assign, "$g_next_menu", -1),#"mnu_castle_taken_by_friends"),
         ## (jump_to_menu, "mnu_total_victory"),
          (call_script, "script_party_wound_all_members", "$g_enemy_party"),
          (assign, ":root_defeated_party", "$g_enemy_party"), #Kham - fix
          (call_script, "script_lift_siege", ":root_defeated_party", 0), #Kham - Fix
          #(leave_encounter),
          #(change_screen_return),
           (jump_to_menu, "mnu_total_victory"),
           ] + (is_a_wb_menu==1 and [
           (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
           		(options_set_battle_size, "$player_battlesize"),
           	(try_end),
           ] or []) + [
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_collective_friends"),
          (assign, ":ally_num_soldiers", reg0),
          (eq, "$g_battle_result", -1),
          (this_or_next|eq, ":ally_num_soldiers", 0), #battle lost 
          (le, ":ally_num_soldiers",  "$num_routed_allies"), #Kham - don't let routed allies spawn again
		  (assign, "$recover_after_death_menu", "mnu_recover_after_death_default"),
          (assign, "$g_next_menu", "mnu_tld_player_defeated"),
          (jump_to_menu, "mnu_total_defeat"),
          ] + (is_a_wb_menu==1 and [
          (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
           		(options_set_battle_size, "$player_battlesize"),
          (try_end),
          ] or []) + [
          #(leave_encounter),
          #(change_screen_return),
        (try_end),

	#Calculate Formula A here - Kham
	(try_begin), 
		(eq, "$new_rank_formula_calculated", 0),
		(call_script, "script_calculate_formula_a"),
		(assign, "$nf_helping_allies", 1),
	(try_end),
	#Calculate Formula A END
        ],
    [
      ("talk_to_siege_commander",[]," Request a meeting with the commander.",[
                                (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
                                (set_visitor,0,"trp_player"),
                                (party_stack_get_troop_id, ":siege_leader_id","$g_encountered_party_2",0),
                                (party_stack_get_troop_dna,":siege_leader_dna","$g_encountered_party_2",0),
                                (set_visitor,17,":siege_leader_id",":siege_leader_dna"),
                                (set_jump_mission,"mt_conversation_encounter"),
                                (jump_to_scene,"scn_conversation_scene"),
                                (assign, "$talk_context", tc_siege_commander),
                                (change_screen_map_conversation, ":siege_leader_id")]),
      ("join_siege_with_allies",[(neg|troop_is_wounded, "trp_player")], "Join the next assault.",
       [
           (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
           (try_begin),
             (check_quest_active, "qst_join_siege_with_army"),
             (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, "$g_encountered_party"),
             (add_xp_as_reward, 250),
			 (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
			 (store_div, ":rank_reward", reg0, 100),
			 (call_script, "script_increase_rank", "$players_kingdom", ":rank_reward"),
			 (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
			 (store_div, ":relation_reward", ":rank_reward", 2),
			 (call_script, "script_change_player_relation_with_troop", ":faction_marshall", ":relation_reward"),
             (call_script, "script_end_quest", "qst_join_siege_with_army"),
             #Reactivating follow army quest
             (str_store_troop_name_link, s9, ":faction_marshall"),
             (setup_quest_text, "qst_follow_army"),
             (str_store_string, s2, "@{s9} wants you to follow his army until further notice."),
             (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
             #(assign, "$g_player_follow_army_warnings", 0),
           (try_end),
           (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),

           (call_script, "script_calculate_battle_advantage"),
           (val_mul, reg0, 2),
           (val_div, reg0, 3), #scale down the advantage a bit in sieges.
           ] + (is_a_wb_menu==1 and [
           (options_get_battle_size, "$player_battlesize"),
		   (try_begin),
				(gt, "$player_battlesize", 415),
				(options_set_battle_size, 415), #200
				(assign, "$player_battlesize_changed", 1),
			(try_end),
           	] or []) + [
           (set_battle_advantage, reg0),
           (set_party_battle_mode),
           (assign, ":siege_mission", "mt_castle_attack_walls_ladder"),
           (try_begin),
           	(eq, "$advanced_siege_ai",1),
           	(assign, ":siege_mission", "mt_castle_attack_walls_ladder"),
           (else_try),
           	(eq, "$advanced_siege_ai", 0),
           	(assign, ":siege_mission", "mt_castle_attack_walls_ladder_native"),
           (try_end),
           (set_jump_mission,":siege_mission"),
           (jump_to_scene,":battle_scene"),
           (assign, "$g_siege_final_menu", "mnu_besiegers_camp_with_allies"), 
           (assign, "$g_siege_battle_state", 1),
           #(assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (assign, "$g_next_menu", "mnu_besiegers_camp_with_allies"), 
           (jump_to_menu, "mnu_besiegers_camp_with_allies"),
           (change_screen_mission),
          ]),
      ("join_siege_stay_back", [(call_script, "script_party_count_members_with_full_health", "p_main_party"),
                                (ge, reg0, 3),
                                ],
       "Order your soldiers to join the next assault without you.",
       [
         (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
         (try_begin),
           (check_quest_active, "qst_join_siege_with_army"),
           (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, "$g_encountered_party"),
           (add_xp_as_reward, 250),
			(call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
			(store_div, ":rank_reward", reg0, 100),
			(call_script, "script_increase_rank", "$players_kingdom", ":rank_reward"),
			(faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
			(store_div, ":relation_reward", ":rank_reward", 2),
			(call_script, "script_change_player_relation_with_troop", ":faction_marshall", ":relation_reward"),
           (call_script, "script_end_quest", "qst_join_siege_with_army"),
           #Reactivating follow army quest
           (str_store_troop_name_link, s9, ":faction_marshall"),
           (setup_quest_text, "qst_follow_army"),
           (str_store_string, s2, "@{s9} wants you to follow his army until further notice."),
           (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
           #(assign, "$g_player_follow_army_warnings", 0),
         (try_end),
         (jump_to_menu,"mnu_castle_attack_walls_with_allies_simulate")]),
      ("leave",[],"Leave.",[
      	] + (is_a_wb_menu==1 and [
          (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
           		(options_set_battle_size, "$player_battlesize"),
          (try_end),
        ] or []) + [
          (leave_encounter),
          (change_screen_return)]),
    ]
 ),


( "moria_must_escape",city_menu_color, # dungeon crawl: way out of moria
 "^^The book seems to give the account of the last attempt of dwarves to resettle in Moria.\
 Attempt which apparently ended with gruesome death for all involved. Perusing the book, \
 you stumble on the words 'true silver'! Studying the pages you suddenly understand \
 that those are the descriptions of dwarven stashes somewhere on the lower levels. Hah! \
 Would not it be cool to uncover the long lost dwarven mithril!? \
 ^You eagerly follow the directions, into a narrow winding tunnel and down... \
 ^...^After a couple of hours of fruitless search you understand that you are lost deep in Moria and need to find a way out.",
    "none",[(set_background_mesh, "mesh_town_moria"),],[
	  ("moria_exit_scene",[], "Find your way out!",[
			(modify_visitors_at_site,"scn_moria_deep_mines"),
			(reset_visitors),
            		(set_visitor,0,"trp_player"),
			(set_jump_mission,"mt_dungeon_crawl_moria_deep"),
            		(jump_to_scene, "scn_moria_deep_mines"),
			(jump_to_menu, "mnu_auto_return_to_map"),
            (change_screen_mission),
	  ]),
	  # ("moria_exit_found",[(eq,1,0)], "Exit is here!",[
			# (jump_to_menu, "mnu_auto_return_to_map"),
            # (change_screen_map),
	  # ], "Fresh air behind this door!"),
	]
 ),

( "castle_outside",city_menu_color,
    "You are outside {s2}.{s11} {s3} {s4}",
    "none",
    code_to_set_city_background + [
	    
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (str_store_party_name, s2,"$g_encountered_party"),
        (call_script, "script_encounter_calculate_fit"),
        (assign,"$all_doors_locked",1),
		#(str_store_party_name, s15, "$g_encountered_party"),(display_message, "@castle_outside_menu: {s15}"),

        (assign, "$current_town","$g_encountered_party"),
        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (call_script, "script_let_nearby_parties_join_current_battle", 1, 0),
          (call_script, "script_encounter_init_variables"),
          (assign, "$entry_to_town_forbidden",0),
          (assign, "$sneaked_into_town",0),
          #(assign, "$town_entered", 0),
#          (assign, "$waiting_for_arena_fight_result", 0),
          (assign, "$encountered_party_hostile", 0),
          (assign, "$encountered_party_friendly", 0),
          (try_begin),
            (gt, "$g_player_besiege_town", 0),
            (neq,"$g_player_besiege_town","$g_encountered_party"),
            (party_slot_eq, "$g_player_besiege_town", slot_center_is_besieged_by, "p_main_party"),
            (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
            (assign,"$g_player_besiege_town",-1),
          (try_end),
          (try_begin),
            (lt, "$g_encountered_party_relation", 0),
            (assign, "$encountered_party_hostile", 1),
            (assign,"$entry_to_town_forbidden",1),
          (try_end),

          (assign,"$cant_sneak_into_town",0),
          (try_begin),
            (eq,"$current_town","$last_sneak_attempt_town"),
            (store_current_hours,reg(2)),
            (val_sub,reg(2),"$last_sneak_attempt_time"),
            (lt,reg(2),12),
            (assign,"$cant_sneak_into_town",1),
          (try_end),
        (else_try), #second or more turn
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (try_end),

        (str_clear,s4),
        (try_begin), 
          (eq,"$entry_to_town_forbidden",1),
          (try_begin),
            (eq,"$cant_sneak_into_town",1),
            (str_store_string,s4,"str_sneaking_to_town_impossible"),
          (else_try),
            (str_store_string,s4,"str_entrance_to_town_forbidden"),
          (try_end),
        (try_end),

        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (store_faction_of_party, ":center_faction", "$current_town"),
        (str_store_faction_name,s9,":center_faction"),
        (try_begin),
          (ge, ":center_lord", 0),
          (str_store_troop_name,s8,":center_lord"),
          (str_store_string,s7,"@{s8} of {s9}"),
        (try_end),

        (try_begin), # same mnu_town
          (party_slot_eq,"$current_town",slot_party_type, spt_castle),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string,s11,"@ Your own banner flies over the castle gate."),
          (else_try),
            (ge, ":center_lord", 0),
            (str_store_string,s11,"@ You see the banner of {s7} over the castle gate."),
          (else_try),
            (str_store_string,s11,"@ This castle seems to belong to no one."),
          (try_end),
        (else_try),
          (try_begin),
            (eq, ":center_lord", "trp_player"),
            (str_store_string,s11,"@ Your own banner flies over the town gates."),
          (else_try),
            (ge, ":center_lord", 0),
            (str_store_string,s11,"@ You see the banner of {s7} over the town gates."),
          (else_try),
            (str_store_string,s11,"@ The townsfolk here have declared their independence."),
          (try_end),
        (try_end),

        (party_get_num_companions, reg(7),"p_collective_enemy"),
        (assign,"$castle_undefended",0),
        (str_clear, s3),
        (try_begin),
          (eq,reg(7),0),
          (assign,"$castle_undefended",1),
#          (party_set_faction,"$g_encountered_party","fac_neutral"),
#          (party_set_slot, "$g_encountered_party", slot_town_lord, stl_unassigned),
          (str_store_string, s3, "str_castle_is_abondened"),
        (else_try),
          (eq,"$g_encountered_party_faction","fac_player_supporters_faction"),
          (str_store_string, s3, "str_place_is_occupied_by_player"),
        (else_try),
          (lt, "$g_encountered_party_relation", 0),
          (str_store_string, s3, "str_place_is_occupied_by_enemy"),
#        (else_try),
#          (str_store_string, s3, "str_place_is_occupied_by_friendly"),
        (try_end),

        (try_begin),
          (eq, "$g_leave_town_outside",1),
          (assign, "$g_leave_town_outside",0),
          (assign, "$g_permitted_to_center", 0),
          (change_screen_return),
        (else_try),
          (check_quest_active, "qst_escort_messenger"),
          (quest_slot_eq, "qst_escort_messenger", slot_quest_target_center, "$g_encountered_party"),
          (quest_get_slot, ":quest_object_troop", "qst_escort_messenger", slot_quest_object_troop),
          (modify_visitors_at_site,"scn_conversation_scene"),
          (reset_visitors),
          (set_visitor,0, "trp_player"),
          (set_visitor,17, ":quest_object_troop"),
          (set_jump_mission, "mt_conversation_encounter"),
          (jump_to_scene, "scn_conversation_scene"),
          (assign, "$talk_context", tc_entering_center_quest_talk),
          (change_screen_map_conversation, ":quest_object_troop"),
        # (else_try),
          # (check_quest_active, "qst_kidnapped_girl"),
          # (quest_slot_eq, "qst_kidnapped_girl", slot_quest_giver_center, "$g_encountered_party"),
          # (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 3),
          # (modify_visitors_at_site,"scn_conversation_scene"),
          # (reset_visitors),
          # (set_visitor,0, "trp_player"),
          # (set_visitor,17, "trp_kidnapped_girl"),
          # (set_jump_mission, "mt_conversation_encounter"),
          # (jump_to_scene, "scn_conversation_scene"),
          # (assign, "$talk_context", tc_entering_center_quest_talk),
          # (change_screen_map_conversation, "trp_kidnapped_girl"),
##        (else_try),
##          (gt, "$lord_requested_to_talk_to", 0),
##          (store_current_hours, ":cur_hours"),
##          (neq, ":cur_hours", "$quest_given_time"),
##          (modify_visitors_at_site,"scn_conversation_scene"),
##          (reset_visitors),
##          (assign, ":cur_lord", "$lord_requested_to_talk_to"),
##          (assign, "$lord_requested_to_talk_to", 0),
##          (set_visitor,0,"trp_player"),
##          (set_visitor,17,":cur_lord"),
##          (set_jump_mission,"mt_conversation_encounter"),
##          (jump_to_scene,"scn_conversation_scene"),
##          (assign, "$talk_context", tc_castle_gate_lord),
##          (change_screen_map_conversation, ":cur_lord"),
        (else_try),
          (eq, "$g_town_visit_after_rest", 1),
          (assign, "$g_town_visit_after_rest", 0),
          (jump_to_menu,"mnu_town"),
        # (else_try),
          # (party_slot_eq,"$g_encountered_party", slot_town_lord, "trp_player"),
          # (party_slot_eq,"$g_encountered_party", slot_party_type,spt_castle),
          # (jump_to_menu, "mnu_enter_your_own_castle"),
        (else_try),
          (party_slot_eq,"$g_encountered_party", slot_party_type,spt_castle),
          (ge, "$g_encountered_party_relation", 0),
          (this_or_next|eq,"$castle_undefended",1),
          (eq, "$g_permitted_to_center",1),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (party_slot_eq,"$g_encountered_party", slot_party_type,spt_town),
          (ge, "$g_encountered_party_relation", 0),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (eq, "$g_player_besiege_town", "$g_encountered_party"),
          (jump_to_menu, "mnu_castle_besiege"),
        (try_end),
        ],
    [

	  ("moria_enter",[
				(eq, "$current_town", "p_town_moria"),
				(this_or_next|eq, "$found_moria_entrance", 1),(eq,"$cheat_mode",1), (eq, "$moria_book_given",0),
	        ], "Return into main hall of Moria trough the secret entrance",[
			(modify_visitors_at_site,"scn_moria_center",),
			(reset_visitors),
            (set_visitor,1,"trp_player"),
			(set_jump_mission,"mt_dungeon_crawl_moria_hall"),
            (jump_to_scene, "scn_moria_center"),
			(assign, "$found_moria_entrance", 1),
            (change_screen_mission),
	  ],"Enter Moria."),
	  
	  #Enter dungeon in Moria begin (mtarini)
      ("moria_secret",[
        (eq, "$current_town", "p_town_moria"),
	  	(eq,"$entry_to_town_forbidden",1), 
	  	(eq, "$moria_book_given",0),
		(try_begin), (eq, "$found_moria_entrance", 1),
			(str_store_string, s12, "@Go to the secret entrance to Moria" ),
		(else_try),
			(str_store_string, s12, "@Search for a secret entrance to Moria" ),
		(try_end),
		
        ],"{s12}",[
            (modify_visitors_at_site,"scn_moria_secret_entry"),
			(reset_visitors),
            (set_visitor,0,"trp_player"),
			(set_jump_mission,"mt_dungeon_crawl_moria_entrance"),
            (jump_to_scene, "scn_moria_secret_entry"),
            (change_screen_mission),
       ]),
      #Enter dungeon in Moria end (mtarini)
	  
	  ("cheat_steal_book",[(eq, "$current_town", "p_town_moria"),(eq,"$cheat_mode",1),], "CHEAT: steal book now",[
			(troop_add_item, "trp_player","itm_book_of_moria",0),
			(try_begin),
				(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
				(str_store_string, s12, "@Get book." ),
				(jump_to_menu,"mnu_moria_must_escape"),
				(finish_mission),
			(else_try),
				(str_store_string, s12, "str_empty_string"),
			(try_end),
	  ]
	  ,"Get the book"),
	  ##Kham - Player Initiated Siege BEGIN
	  ("player_castle_initiate_siege",
	 	[#(eq, "$cheat_mode",1),
	 	 (eq, "$player_allowed_siege",1), #Kham - Global Var that allows player to siege. Set in Dialogues.
	 	 (store_faction_of_party, ":faction_no", "$g_encountered_party"),
	 	 (faction_get_slot, ":faction_strength", ":faction_no", slot_faction_strength), #Check Faction Strength
	 	 
	 	 (party_get_slot, ":siegable", "$g_encountered_party", slot_center_siegability), #Check if we can siege

	 	 (assign, ":continue", 0),
	     
	     (try_begin),
	     	(eq, ":siegable", tld_siegable_never), #some places are never siegable
		    #(display_message, "@Passed 1st"),
		    (assign, ":continue", 0),
	     (else_try),    
	     	(neq, ":siegable", tld_siegable_capital), #not a capital (separate condition)
		 	(this_or_next|eq, "$tld_option_siege_reqs", 2), # No siege reqs
	     	(this_or_next|eq, ":siegable", tld_siegable_always), # camps and such can always be sieged
	     	(lt, ":faction_strength", "$g_fac_str_siegable"), # otherwise, defenders need to be weak
	     	#(display_message, "@Passed 2nd"),
	     	(assign, ":continue", 1),
		 (else_try),
		 	(eq, ":siegable", tld_siegable_capital), #If it is the capital, check if there are other centers left
	     	(this_or_next|eq, "$tld_option_siege_reqs", 2), # No siege reqs
	     	(lt, ":faction_strength", "$g_fac_str_siegable"), #and fac str is low enough to siege
	     	(call_script, "script_cf_check_if_only_capital_left", "$g_encountered_party"), #and there is only 1 center left (capital - script fails when there is more than 1 center left.)
	     	#(display_message, "@Passed 3rd"),
	     	(assign, ":continue", 1),
	     (try_end),

	     (eq, ":continue", 1),

	 	 (neg|troop_is_wounded, "trp_player"),
	 	 (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1), #if besieged by Marshall, player can't attack.
	     (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
	     (lt, ":reln", 0),
	     (lt, "$g_encountered_party_2", 1),
	     (call_script, "script_party_count_fit_for_battle","p_main_party"),
	     (gt, reg0, 1),
	     (try_begin),
	    	 (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
	           (assign, reg6, 1),
	         (else_try),
	           (assign, reg6, 0),
	         (try_end),

 	#Calculate Formula A here - Kham
	(try_begin), 
		(eq, "$new_rank_formula_calculated", 0),
		(call_script, "script_calculate_formula_a", 0),
	(try_end),
	#Calculate Formula A END

	    ],
	    "Attack the {reg6?town:castle}...",
	    [
	     (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
	     (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
	     (call_script, "script_let_nearby_parties_join_current_battle", 0, 0), #Kham - Let nearby lords join the battle
         (call_script, "script_encounter_init_variables"),
	     (call_script, "script_calculate_battle_advantage"),
		 (val_mul, reg0, 2),
		 (val_div, reg0, 3), #scale down the advantage a bit in sieges.
		 ] + (is_a_wb_menu==1 and [
         (options_get_battle_size, "$player_battlesize"),
		  (try_begin),
				(gt, "$player_battlesize", 415),
				(options_set_battle_size, 415), #200
				(assign, "$player_battlesize_changed", 1),
		  (try_end),
     	 ] or []) + [
		 (set_battle_advantage, reg0),
		 (set_party_battle_mode),
 		 (assign, ":siege_mission", "mt_castle_attack_walls_ladder"),
           (try_begin),
           	(eq, "$advanced_siege_ai",1),
           	(assign, ":siege_mission", "mt_castle_attack_walls_ladder"),
           (else_try),
           	(eq, "$advanced_siege_ai", 0),
           	(assign, ":siege_mission", "mt_castle_attack_walls_ladder_native"),
           (try_end),
           (set_jump_mission,":siege_mission"),
		 (jump_to_scene,":battle_scene"),
		 (assign, "$g_siege_final_menu", "mnu_player_initiated_siege_result"),
		 (assign, "$g_siege_battle_state", 1),
		 (assign, "$g_next_menu", "mnu_player_initiated_siege_result"),
		 (jump_to_menu, "mnu_battle_debrief"),
		 (change_screen_mission),
		],
	),
	 ##Kham - Player Initiated Siege END
	  
      # ("approach_gates",[(this_or_next|eq,"$entry_to_town_forbidden",1),
                          # (party_slot_eq,"$g_encountered_party", slot_party_type,spt_castle)],
       # "Approach the gates and hail the guard.",[
                                                  # (jump_to_menu, "mnu_castle_guard"),
# ##                                                   (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
# ##                                                   (set_visitor,0,"trp_player"),
# ##                                                   (store_faction_of_party, ":cur_faction", "$g_encountered_party"),
# ##                                                   (faction_get_slot, ":cur_guard", ":cur_faction", slot_faction_guard_troop),
# ##                                                   (set_visitor,17,":cur_guard"),
# ##                                                   (set_jump_mission,"mt_conversation_encounter"),
# ##                                                   (jump_to_scene,"scn_conversation_scene"),
# ##                                                   (assign, "$talk_context", tc_castle_gate),
# ##                                                   (change_screen_map_conversation, ":cur_guard")
                                                   # ]),
 ]+concatenate_scripts([[	  
      ("town_sneak",[(eq, cheat_switch, 1),
					(eq, "$cheat_mode", 1),
					 (party_slot_eq,"$g_encountered_party", slot_party_type,spt_town),
                     (eq,"$entry_to_town_forbidden",1),
                     (eq,"$cant_sneak_into_town",0)],
       "TEST: Disguise yourself and try to sneak into the town.",
       [
         (faction_get_slot, ":player_alarm", "$g_encountered_party_faction", slot_faction_player_alarm),
         (party_get_num_companions, ":num_men", "p_main_party"),
         (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
         (val_add, ":num_men", ":num_prisoners"),
         (val_mul, ":num_men", 2),
         (val_div, ":num_men", 3),
         (store_add, ":get_caught_chance", ":player_alarm", ":num_men"),
         (store_random_in_range, ":random_chance", 0, 100),
         (try_begin),
           (this_or_next|ge, ":random_chance", ":get_caught_chance"),
           (eq, "$g_last_defeated_bandits_town", "$g_encountered_party"),
           (assign, "$g_last_defeated_bandits_town", 0),
           (assign, "$sneaked_into_town",1),
           #(assign, "$town_entered", 1),
           (jump_to_menu,"mnu_sneak_into_town_suceeded"),
         (else_try),
           (jump_to_menu,"mnu_sneak_into_town_caught"),
         (try_end)
         ]),

      ##KHAM_SIEGE_TEST (ctrl-f shortcut)
      ("castle_start_siege",
       [ (eq, cheat_switch, 1),(eq, 0, 1), #MV: player can't start a sieg
           (this_or_next|party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
           (             party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
           (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
           (lt, ":reln", 0),
           (lt, "$g_encountered_party_2", 1),
           (call_script, "script_party_count_fit_for_battle","p_main_party"),
           (gt, reg(0), 5),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (assign, reg6, 1),
           (else_try),
             (assign, reg6, 0),
           (try_end),
           ],
       "Besiege the {reg6?town:castle}.",
       [
         (eq, "$cheat_mode", 1), #MV: player can't start a siege
         (assign,"$g_player_besiege_town","$g_encountered_party"),
         (store_relation, ":relation", "fac_player_supporters_faction", "$g_encountered_party_faction"),
         (val_min, ":relation", -40),
         (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":relation"),
         (call_script, "script_update_all_notes"),
         (jump_to_menu, "mnu_castle_besiege"),
         ]),


      ("cheat_castle_start_siege",
       [ (eq, cheat_switch, 1),
         (eq, "$cheat_mode", 1),
         (this_or_next|party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
         (             party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
         (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
         (ge, ":reln", 0),
         (lt, "$g_encountered_party_2", 1),
         (call_script, "script_party_count_fit_for_battle","p_main_party"),
         (gt, reg(0), 1),
         (try_begin),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (assign, reg6, 1),
         (else_try),
           (assign, reg6, 0),
         (try_end),
           ],
       "CHEAT: Besiege the {reg6?town:castle}...",
       [   (assign,"$g_player_besiege_town","$g_encountered_party"),
           (jump_to_menu, "mnu_castle_besiege"),
           ]),
 ] for ct in range(cheat_switch)])+[
	   
 ]+concatenate_scripts([[
	  ("town_sneak",[(eq,0,1)],"Dont.",[]),
	  ("castle_start_siege",[(eq,0,1)],"Dont.",[]),
	  ("cheat_castle_start_siege",[(eq,0,1)],"Dont.",[]),
 ] for ct in range(1-cheat_switch)])+[

      ("castle_leave",[],"Leave.",[(change_screen_return,0)]),

 ]+concatenate_scripts([[
      ("castle_cheat_interior",[(eq, "$cheat_mode", 1)], "CHEAT! Interior.",[(set_jump_mission,"mt_ai_training"),
                                                       (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
                                                       (jump_to_scene,":castle_scene"),
                                                       (change_screen_mission)]),
      ("castle_cheat_exterior",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1)], "CHEAT! Exterior.",[
                                                       (set_jump_mission,"mt_ai_training"),
                                                       (party_get_slot, ":castle_scene", "$current_town", slot_castle_exterior),
                                                       (jump_to_scene,":castle_scene"),
                                                       (change_screen_mission)]),
      ("castle_cheat_town_walls",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1),(party_slot_eq,"$current_town",slot_party_type, spt_town),], "CHEAT! Town Walls.",
       [
         (party_get_slot, ":scene", "$current_town", slot_town_walls),
         (set_jump_mission,"mt_ai_training"),
         (jump_to_scene,":scene"),
         (change_screen_mission)]),
 ] for ct in range(cheat_switch)])+[
    ]
 ),
( "castle_besiege",mnf_enable_hot_keys,
    "You are laying siege to {s1}. {s2} {s3}",
    "none",
    code_to_set_city_background + [   (assign, "$g_siege_force_wait", 0),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
          (party_set_slot, "$g_encountered_party", slot_center_is_besieged_by, "p_main_party"),
          (store_current_hours, ":cur_hours"),
          (party_set_slot, "$g_encountered_party", slot_center_siege_begin_hours, ":cur_hours"),
          (assign, "$g_siege_method", 0),
          (assign, "$g_siege_sallied_out_once", 0),
        (try_end),

        (party_get_slot, ":town_food_store", "$g_encountered_party", slot_party_food_store),
        (call_script, "script_center_get_food_consumption", "$g_encountered_party"),
        (assign, ":food_consumption", reg0),
        (assign, reg7, ":food_consumption"),
        (assign, reg8, ":town_food_store"),
        (store_div, reg3, ":town_food_store", ":food_consumption"),

        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (assign, reg6, 1),
        (else_try),
          (assign, reg6, 0),
        (try_end),
        
        (try_begin),
          (gt, reg3, 0),
          (str_store_string, s2, "@The {reg6?town's:castle's} food stores should last for {reg3} more days."),
        (else_try),
          (str_store_string, s2, "@The {reg6?town's:castle's} food stores have run out and the defenders are starving."),
        (try_end),

        (str_store_string, s3, "str_empty_string"),
        (try_begin),
          (ge, "$g_siege_method", 1),
          (store_current_hours, ":cur_hours"),
          (try_begin),
            (lt, ":cur_hours",  "$g_siege_method_finish_hours"),
            (store_sub, reg9, "$g_siege_method_finish_hours", ":cur_hours"),
            (try_begin),
              (eq, "$g_siege_method", 1),
              (str_store_string, s3, "@You're preparing to attack the walls, the work should finish in {reg9} hours."),
            (else_try),
              (eq, "$g_siege_method", 2),
              (str_store_string, s3, "@Your forces are building a siege tower. They estimate another {reg9} hours to complete the build."),
            (try_end),
          (else_try),
            (try_begin),
              (eq, "$g_siege_method", 1),
              (str_store_string, s3, "@You are ready to attack the walls at any time."),
            (else_try),
              (eq, "$g_siege_method", 2),
              (str_store_string, s3, "@The siege tower is built and ready to make an assault."),
            (try_end),
          (try_end),
        (try_end),
        
        #Check if enemy leaves the castle to us...
        (try_begin),
          (eq, "$g_castle_left_to_player",1), #we come here after dialog. Empty the castle and send parties away.
          (assign, "$g_castle_left_to_player",0),
          (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
          (party_set_faction,"$g_encountered_party","fac_neutral"), #temporarily erase faction so that it is not the closest town
          (party_get_num_attached_parties, ":num_attached_parties_to_castle","$g_encountered_party"),
          (try_for_range_backwards, ":iap", 0, ":num_attached_parties_to_castle"),
            (party_get_attached_party_with_rank, ":attached_party", "$g_encountered_party", ":iap"),
            (party_detach, ":attached_party"),
            (party_get_slot, ":attached_party_type", ":attached_party", slot_party_type),
            (eq, ":attached_party_type", spt_kingdom_hero_party),
            (store_faction_of_party, ":attached_party_faction", ":attached_party"),
            (call_script, "script_get_closest_center_of_faction", ":attached_party", ":attached_party_faction"),
            (try_begin),
              (gt, reg0, 0),
              (call_script, "script_party_set_ai_state", ":attached_party", spai_holding_center, reg0),
            (else_try),
              (call_script, "script_party_set_ai_state", ":attached_party", spai_patrolling_around_center, "$g_encountered_party"),
            (try_end),
          (try_end),
          (call_script, "script_party_remove_all_companions", "$g_encountered_party"),
          (change_screen_return),
          (party_collect_attachments_to_party, "$g_encountered_party", "p_collective_enemy"), #recalculate so that
          (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"), #leaving troops will not be considered as captured
          (party_set_faction,"$g_encountered_party",":castle_faction"), 
        (try_end),

        #Check for victory or defeat....
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (str_store_party_name, 1,"$g_encountered_party"),
        (call_script, "script_encounter_calculate_fit"),
        
        (assign, reg11, "$g_enemy_fit_for_battle"),
        (assign, reg10, "$g_friend_fit_for_battle"),


        (try_begin),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (else_try),
          (call_script, "script_party_count_fit_regulars","p_collective_enemy"),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
          (else_try),
            (this_or_next|le, "$g_enemy_fit_for_battle",0),
         	(le, "$g_enemy_fit_for_battle", "$num_routed_enemies"), #kham - don't let routed enemies spawn again
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
          (try_end),
          (this_or_next|eq, ":enemy_finished", 1),
          (eq, "$g_enemy_surrenders", 1),
          (assign, "$g_next_menu", "mnu_castle_taken"),
          ] + (is_a_wb_menu==1 and [
          (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
           		(options_set_battle_size, "$player_battlesize"),
          (try_end),
          ] or []) + [
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),
          (assign, ":main_party_fit_regulars", reg(0)),
          (eq, "$g_battle_result", -1),
          ] + (is_a_wb_menu==1 and [
          (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
           		(options_set_battle_size, "$player_battlesize"),
          (try_end),
          ] or []) + [
          (eq, ":main_party_fit_regulars", 0), #all lost
		  (assign, "$recover_after_death_menu", "mnu_recover_after_death_town"),
          (assign, "$g_next_menu", "mnu_tld_player_defeated"),
          (jump_to_menu, "mnu_total_defeat"),
        (try_end),
    ],
	
    [ ("siege_request_meeting",[(eq, "$cant_talk_to_enemy", 0)],"Call for a meeting with the castle commander.", [
          (assign, "$cant_talk_to_enemy", 1),
          (assign, "$g_enemy_surrenders",0),
          (assign, "$g_castle_left_to_player",0),
          (assign, "$talk_context", tc_castle_commander),
          (party_get_num_attached_parties, ":num_attached_parties_to_castle","$g_encountered_party"),
          (try_begin),
            (gt, ":num_attached_parties_to_castle", 0),
            (party_get_attached_party_with_rank, ":leader_attached_party", "$g_encountered_party", 0),
            (call_script, "script_setup_party_meeting", ":leader_attached_party"),
          (else_try),
            (call_script, "script_setup_party_meeting", "$g_encountered_party"),
          (try_end),
           ]),
        
      ("wait_24_hours",[],"Wait until tomorrow.", [
          (assign,"$auto_besiege_town","$g_encountered_party"),
          (assign, "$g_siege_force_wait", 1),
          (store_time_of_day,":cur_time_of_day"),
          (val_add, ":cur_time_of_day", 1),
          (assign, ":time_to_wait", 31),
          (val_sub,":time_to_wait",":cur_time_of_day"),
          (val_mod,":time_to_wait",24),
          (val_add, ":time_to_wait", 1),
          (rest_for_hours_interactive, ":time_to_wait", 5, 1), #rest while attackable
          (assign, "$cant_talk_to_enemy", 0),
          (change_screen_return),
          ]),

      
      ("castle_lead_attack",
       [ (neg|troop_is_wounded, "trp_player"),
         (ge, "$g_siege_method", 1),
         (gt, "$g_friend_fit_for_battle", 3),
         (store_current_hours, ":cur_hours"),
         (ge, ":cur_hours", "$g_siege_method_finish_hours"),
         ],
       "Lead your soldiers in an assault.", [
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
           (else_try),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
           (try_end),
           (call_script, "script_calculate_battle_advantage"),
           (assign, ":battle_advantage", reg0),
           (val_mul, ":battle_advantage", 2),
           (val_div, ":battle_advantage", 3), #scale down the advantage a bit in sieges.
           ] + (is_a_wb_menu==1 and [
           (options_get_battle_size, "$player_battlesize"),
           (try_begin),
				(gt, "$player_battlesize", 415),
				(options_set_battle_size, 415), #200
				(assign, "$player_battlesize_changed", 1),
		   (try_end),
           	] or []) + [
           (set_battle_advantage, ":battle_advantage"),
           (set_party_battle_mode),
           (assign, "$g_siege_battle_state", 1),
           (assign, ":siege_sally", 0),
           (try_begin),
             (le, ":battle_advantage", -4), #we are outnumbered, defenders sally out
             (eq, "$g_siege_sallied_out_once", 0),
             (set_jump_mission,"mt_castle_attack_walls_defenders_sally"),
             (assign, "$g_siege_battle_state", 0),
             (assign, ":siege_sally", 1),
#           (else_try),
#             (party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),
#             (set_jump_mission,"mt_castle_attack_walls_belfry"),
		   (else_try),
			(assign, ":siege_mission", "mt_castle_attack_walls_ladder"),
			(try_begin),
				(eq, "$advanced_siege_ai",1),
				(assign, ":siege_mission", "mt_castle_attack_walls_ladder"),
			(else_try),
				(eq, "$advanced_siege_ai", 0),
				(assign, ":siege_mission", "mt_castle_attack_walls_ladder_native"),
			(try_end),
			(set_jump_mission,":siege_mission"),
           (try_end),
           (assign, "$cant_talk_to_enemy", 0),           
           (assign, "$g_siege_final_menu", "mnu_castle_besiege"),
           (assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (assign, "$g_siege_method", 0), #reset siege timer
           (jump_to_scene,":battle_scene"),
           (try_begin),
             (eq, ":siege_sally", 1),
             (jump_to_menu, "mnu_siege_attack_meets_sally"),
           (else_try),
#           (jump_to_menu,"mnu_castle_outside"),
##           (assign, "$g_next_menu", "mnu_castle_besiege"),
             (jump_to_menu, "mnu_battle_debrief"),
             (change_screen_mission),
           (try_end),
       ]),
      ("attack_stay_back",
       [ (ge, "$g_siege_method", 1),
         (gt, "$g_friend_fit_for_battle", 3),
         (store_current_hours, ":cur_hours"),
         (ge, ":cur_hours",  "$g_siege_method_finish_hours"),
         ],
       "Order your soldiers to attack while you stay back...", [(assign, "$cant_talk_to_enemy", 0),(jump_to_menu,"mnu_castle_attack_walls_simulate")]),

      ("build_ladders",[(party_slot_eq, "$current_town", slot_center_siege_with_belfry, 0),(eq, "$g_siege_method", 0)],
       "Prepare ladders to attack the walls.", [(jump_to_menu,"mnu_construct_ladders")]),

      # ("build_siege_tower",[(party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),(eq, "$g_siege_method", 0)],
       # "Build a siege tower.", [(jump_to_menu,"mnu_construct_siege_tower")]),

      ("cheat_castle_lead_attack",[(eq, "$cheat_mode", 1),
                                   (eq, "$g_siege_method", 0)],
       "CHEAT: Instant build equipments.",
       [
         (assign, "$g_siege_method", 1),
         (assign, "$g_siege_method_finish_hours", 0),
         (jump_to_menu, "mnu_castle_besiege"),
       ]),
      ("lift_siege",[],"Abandon the siege.",
       [ (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
         (assign,"$g_player_besiege_town", -1),
         (change_screen_return)]),
    ]
 ),
( "siege_attack_meets_sally",0,
    "^^^^^^The defenders sally out to meet your assault.",    "none",    [],
    [("continue",[], "Continue...", [(jump_to_menu, "mnu_battle_debrief"),(change_screen_mission),]),]
 ),
( "castle_besiege_inner_battle",0,
    "{s1}",
    "none",
    [   # (troop_get_type, ":is_female", "trp_player"),
        # (try_begin),
          # (eq, ":is_female", 1),
          # (set_background_mesh, "mesh_pic_siege_sighted_fem"),
        # (else_try),
          # (set_background_mesh, "mesh_pic_siege_sighted"),
        # (try_end),
        (assign, ":result", "$g_battle_result"),#will be reset at script_encounter_calculate_fit
        (call_script, "script_encounter_calculate_fit"),
        
# TODO: To use for the future:
            (str_store_string, s1, "@As a last defensive effort, you retreat to the main hall of the keep.\
 You and your remaining soldiers will put up a desperate fight here. If you are defeated, there's no other place to fall back to."),
            (str_store_string, s1, "@You've been driven away from the walls.\
 Now the attackers are pouring into the streets. IF you can defeat them, you can perhaps turn the tide and save the day."),
        (try_begin),
          (this_or_next|neq, ":result", 1),
          (this_or_next|le, "$g_friend_fit_for_battle", 0),
          (le, "$g_enemy_fit_for_battle", 0),
          (jump_to_menu, "$g_siege_final_menu"),
        (else_try),
          (call_script, "script_encounter_calculate_fit"),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (try_begin),
            (eq, "$g_siege_battle_state", 0),
            (eq, ":result", 1),
            (assign, "$g_battle_result", 0),
            (jump_to_menu, "$g_siege_final_menu"),
          (else_try),
            (eq, "$g_siege_battle_state", 1),
            (eq, ":result", 1),
            (str_store_string, s1, "@You've breached the town walls,\
 but the stubborn defenders continue to resist you in the streets!\
 You'll have to deal with them before you can attack the keep at the heart of the town."),
          (else_try),
            (eq, "$g_siege_battle_state", 2),
            (eq, ":result", 1),
            (str_store_string, s1, "@The town centre is yours,\
 but the remaining defenders have retreated to the castle.\
 It must fall before you can complete your victory."),
          (else_try),
            (jump_to_menu, "$g_siege_final_menu"),
          (try_end),
        (else_try),
          (try_begin),
            (eq, "$g_siege_battle_state", 0),
            (eq, ":result", 1),
            (assign, "$g_battle_result", 0),
            (jump_to_menu, "$g_siege_final_menu"),
          (else_try),
            (eq, "$g_siege_battle_state", 1),
            (eq, ":result", 1),
            (str_store_string, s1, "@The remaining defenders have retreated to the castle as a last defense. You must go in and crush any remaining resistance."),
          (else_try),
            (jump_to_menu, "$g_siege_final_menu"),
          (try_end),
        (try_end),
    ],
    [ ("continue",[],"Continue...",
       [   (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (try_begin),
               (eq, "$g_siege_battle_state", 1),
               (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
               (set_jump_mission, "mt_besiege_inner_battle_town_center"),
             (else_try),
               (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
               (set_jump_mission, "mt_besiege_inner_battle_castle"),
             (try_end),
           (else_try),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
             (set_jump_mission, "mt_besiege_inner_battle_castle"),
           (try_end),
##           (call_script, "script_calculate_battle_advantage"),
##           (set_battle_advantage, reg0),
           (set_party_battle_mode),
           (jump_to_scene, ":battle_scene"),
           (val_add, "$g_siege_battle_state", 1),
           (assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (jump_to_menu, "mnu_battle_debrief"),
           (change_screen_mission),
       ]),
    ]
 ),
( "construct_ladders",0,
    "As the party member with the highest Engineer skill ({reg2}), {reg3?you estimate:{s3} estimates} that it will take\
 {reg4} hours to build enough scaling ladders for the assault.",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),

     (store_sub, reg4, 14, ":max_skill"),
     (val_mul, reg4, 2),
     (val_div, reg4, 3),
     
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),
    ],
    [ ("build_ladders_cont",[],
       "Do it.", [
           (assign, "$g_siege_method", 1),
           (store_current_hours, ":cur_hours"),
           (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
           (store_sub, ":hours_takes", 14, reg0),
           (val_mul, ":hours_takes", 2),
           (val_div, ":hours_takes", 3),
           (store_add, "$g_siege_method_finish_hours",":cur_hours", ":hours_takes"),
           (assign,"$auto_besiege_town","$current_town"),
           (rest_for_hours_interactive, 96, 5, 1), #rest while attackable. A trigger will divert control when attack is ready.
           (change_screen_return),
           ]),
      ("go_back_dot",[],"Go back.", [(jump_to_menu,"mnu_castle_besiege")]),],
 ),
( "castle_attack_walls_simulate",mnf_disable_all_keys,
    "{s4}^^Your casualties:{s8}^^Enemy casualties were: {s9}",
    "none",
    [   (troop_get_type, ":is_female", "trp_player"),
        (try_begin),
          (eq, ":is_female", 1),
          #(set_background_mesh, "mesh_pic_siege_sighted_fem"),
        (else_try),
          #(set_background_mesh, "mesh_pic_siege_sighted"),
        (try_end),
        
        (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
        (assign, ":player_party_strength", reg0),
        (val_div, ":player_party_strength", 10),

        (call_script, "script_party_calculate_strength", "$g_encountered_party", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 4),

        (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s8, s0),

        (inflict_casualties_to_party_group, "$g_encountered_party", ":player_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),

        (assign, "$no_soldiers_left", 0),
        (try_begin),
          (call_script, "script_party_count_members_with_full_health","p_main_party"),
          (le, reg(0), 0),
          (assign, "$no_soldiers_left", 1),
          (str_store_string, s4, "str_attack_walls_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health","$g_encountered_party"),
          (le, reg(0), 0),
          (assign, "$no_soldiers_left", 1),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_attack_walls_success"),
        (else_try),
          (str_store_string, s4, "str_attack_walls_continue"),
        (try_end),
     ],
    [
##      ("lead_next_wave",[(eq, "$no_soldiers_left", 0)],"Lead the next wave of attack personally.", [
##           (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
##           (set_party_battle_mode),
##           (set_jump_mission,"mt_castle_attack_walls"),
##           (jump_to_scene,":battle_scene"),
##           (jump_to_menu,"mnu_castle_outside"),
##           (change_screen_mission),
##       ]),
##      ("continue_attacking",[(eq, "$no_soldiers_left", 0)],"Order your soldiers to keep attacking...", [
##                                    (jump_to_menu,"mnu_castle_attack_walls_3"),
##                                    ]),
##      ("call_soldiers_back",[(eq, "$no_soldiers_left", 0)],"Call your soldiers back.",[(jump_to_menu,"mnu_castle_outside")]),
      ("continue",[],"Continue...",[(jump_to_menu,"mnu_castle_besiege")]),
    ]
 ),
( "castle_attack_walls_with_allies_simulate",mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    [
        (troop_get_type, ":is_female", "trp_player"),
        (try_begin),
          (eq, ":is_female", 1),
          #(set_background_mesh, "mesh_pic_siege_sighted_fem"),
        (else_try),
          #(set_background_mesh, "mesh_pic_siege_sighted"),
        (try_end),

        (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
        (assign, ":player_party_strength", reg0),
        (val_div, ":player_party_strength", 10),
        (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
        (assign, ":friend_party_strength", reg0),
        (val_div, ":friend_party_strength", 10),

        (val_max, ":friend_party_strength", 1),

        (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 4),

##        (assign, reg0, ":player_party_strength"),
##        (assign, reg1, ":friend_party_strength"),
##        (assign, reg2, ":enemy_party_strength"),
##        (assign, reg3, "$g_enemy_party"),
##        (assign, reg4, "$g_ally_party"),
##        (display_message, "@player_str={reg0} friend_str={reg1} enemy_str={reg2}"),
##        (display_message, "@enemy_party={reg3} ally_party={reg4}"),

        (assign, ":enemy_party_strength_for_p", ":enemy_party_strength"),
        (val_mul, ":enemy_party_strength_for_p", ":player_party_strength"),
        (val_div, ":enemy_party_strength_for_p", ":friend_party_strength"),
        (val_sub, ":enemy_party_strength", ":enemy_party_strength_for_p"),

        (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength_for_p", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s8, s0),
                                    
        (inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s10, s0),

        (call_script, "script_collect_friendly_parties"),

        (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),

        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

        (assign, "$no_soldiers_left", 0),
        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),
          (le, reg0, 0),
          (assign, "$no_soldiers_left", 1),
          (str_store_string, s4, "str_attack_walls_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (le, reg0, 0),
          (assign, "$no_soldiers_left", 1),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_attack_walls_success"),
        (else_try),
          (str_store_string, s4, "str_attack_walls_continue"),
        (try_end),
     ],
    [("continue",[],"Continue...",[(jump_to_menu,"mnu_besiegers_camp_with_allies")]),]
 ),
( "castle_taken_by_friends",0,
    "Nothing to see here.",
    "none",
    [   (party_clear, "$g_encountered_party"),
        (party_stack_get_troop_id, ":leader", "$g_encountered_party_2", 0),
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, ":leader"),
        (store_troop_faction, ":faction_no", ":leader"),
        #Reduce prosperity of the center by 5
        (call_script, "script_change_center_prosperity", "$g_encountered_party", -5),
        (call_script, "script_give_center_to_faction", "$g_encountered_party", ":faction_no"),
        (call_script, "script_add_log_entry", logent_player_participated_in_siege, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
        (change_screen_return),
    ],
    [],
 ),
( "castle_taken",mnf_disable_all_keys,
    "{s3} has fallen to your troops, and you now have full control of the {reg2?town:castle}.\
  {reg1? It would seem that there is nothing stopping you from taking it for yourself...:}",# Only visible when castle is taken without being a vassal of a kingdom.
    "none",
    [   (party_clear, "$g_encountered_party"),
        (call_script, "script_lift_siege", "$g_encountered_party", 0),
        (assign, "$g_player_besiege_town", -1),
        (call_script, "script_add_log_entry", logent_castle_captured_by_player, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
        #Reduce prosperity of the center by 5
        (call_script, "script_change_center_prosperity", "$g_encountered_party", -5),
        (call_script, "script_add_log_entry", logent_castle_captured_by_player, "trp_player", "$g_encountered_party", -1, "$g_encountered_party_faction"),
        (try_begin),
          (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
          (neq, "$players_kingdom", "fac_player_supporters_faction"),
          (call_script, "script_give_center_to_faction", "$g_encountered_party", "$players_kingdom"),
          (call_script, "script_order_best_besieger_party_to_guard_center", "$g_encountered_party", "$players_kingdom"),
          (jump_to_menu, "mnu_castle_taken_2"),
        (else_try),
          (call_script, "script_give_center_to_faction", "$g_encountered_party", "fac_player_supporters_faction"),
          (call_script, "script_order_best_besieger_party_to_guard_center", "$g_encountered_party", "fac_player_supporters_faction"),
          (str_store_party_name, s3, "$g_encountered_party"),
          (assign, reg1, 0),
          # (try_begin),
            # (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
            # (assign, reg1, 1),
          # (try_end),
        (try_end),
        (assign, reg2, 0),
        (try_begin),
          (is_between, "$g_encountered_party", centers_begin, centers_end),
          (assign, reg2, 1),
        (try_end),
    ],
    [ ("continue",[],"Continue...",[(assign, "$auto_enter_town", "$g_encountered_party"),(change_screen_return),]),],
 ),
( "castle_taken_2",mnf_disable_all_keys,
    "{s3} has fallen to your troops, and you now have full control of the castle.\
 It is time to send word to {s9} about your victory. {s5}",
    "none",
    [   (str_store_party_name, s3, "$g_encountered_party"),
        (str_clear, s5),
        (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
        (str_store_troop_name, s9, ":faction_leader"),
        (try_begin),
#          (eq, "$player_has_homage", 0),
          (assign, reg8, 0),
          (try_begin),
            (party_slot_eq, "$g_encountered_party", spt_town),
            (assign, reg8, 1),
          (try_end),
          (str_store_string, s5, "@However, since you are not a sworn {man/follower} of {s9}, there is no chance he would recognize you as the {lord/lady} of this {reg8?town:castle}."),
        (try_end),
    ],
    [ # commented by GA, no castle ownership in TLD
	  #("castle_taken_claim",[(eq, "$player_has_homage", 1)],"Request that {s3} be awarded to you.",
      # [
      #  (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
      #  (assign, "$g_castle_requested_by_player", "$current_town"),
      #  (assign, "$auto_enter_town", "$g_encountered_party"),
      #  (change_screen_return),
      #  ]),
      ("castle_taken_no_claim",[],"Ask no rewards.",
       [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, -1),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
#        (jump_to_menu, "mnu_town"),
        ]),
    ],
 ),
 
( "siege_started_defender",mnf_scale_picture|mnf_enable_hot_keys,
    "{s1} is launching an assault against the walls of {s2}. You have {reg22} troops fit for battle against the enemy's {reg11}. You decide to...",
    "none",
    code_to_set_city_background + [
        (select_enemy,1),
        (assign, "$g_enemy_party", "$g_encountered_party_2"),
        (assign, "$g_ally_party", "$g_encountered_party"),
        (str_store_party_name, 1,"$g_enemy_party"),
        (str_store_party_name, 2,"$g_ally_party"),
        (call_script, "script_encounter_calculate_fit"),
        (assign, reg22, reg10), #TLD fix
        (try_begin),
          (eq, "$g_siege_first_encounter", 1),
          (call_script, "script_let_nearby_parties_join_current_battle", 0, 1), #MV from 0, 1, so no enemies standing by would join - Kham - That is actually what we want.
          (call_script, "script_encounter_init_variables"),
        (try_end),

        (try_begin),
          (eq, "$g_siege_first_encounter", 0),
          (try_begin),
            (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
            (assign, ":num_enemy_regulars_remaining", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_collective_friends"),
            (assign, ":num_ally_regulars_remaining", reg0),
            (assign, ":enemy_finished", 0),
            (try_begin),
              (eq, "$g_battle_result", 1),
              (this_or_next|le, ":num_enemy_regulars_remaining", 0), #battle won
           	  (le, ":num_enemy_regulars_remaining",  "$num_routed_enemies"), #kham - don't let routed enemies spawn
              (assign, ":enemy_finished",1),
            (else_try),
              (eq, "$g_engaged_enemy", 1),
              (this_or_next|le, "$g_enemy_fit_for_battle", 0),
              (le, "$g_enemy_fit_for_battle", "$num_routed_enemies"), #kham - don't let routed enemies spawn
              (assign, ":enemy_finished",1),
            (try_end),
            (this_or_next|eq, ":enemy_finished",1),
            (eq,"$g_enemy_surrenders",1),
            (assign, "$g_next_menu", -1),
            ] + (is_a_wb_menu==1 and [
           (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
           		(options_set_battle_size, "$player_battlesize"),
          	(try_end),
          	] or []) + [
            (jump_to_menu, "mnu_total_victory"),
          (else_try),
            (assign, ":battle_lost", 0),
            (try_begin),
              (this_or_next|eq, "$g_battle_result", -1),
              (troop_is_wounded,  "trp_player"),
              (this_or_next|eq, ":num_ally_regulars_remaining", 0), 
              (le, ":num_ally_regulars_remaining",  "$num_routed_allies"), #Kham = don't let routed allies spawn
              (assign, ":battle_lost",1),
            (try_end),
            (this_or_next|eq, ":battle_lost",1),
            (eq,"$g_player_surrenders",1),
			(assign, "$recover_after_death_menu", "mnu_recover_after_death_town"),
            (assign, "$g_next_menu", "mnu_tld_player_defeated"),
            ] + (is_a_wb_menu==1 and [
            (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
           		(options_set_battle_size, "$player_battlesize"),
            (try_end),
            ] or []) + [
            (jump_to_menu, "mnu_total_defeat"),
          (else_try),
            # Ordinary victory/defeat.
            (assign, ":attackers_retreat", 0),
            (try_begin),
            #check whether enemy retreats
              (eq, "$g_battle_result", 1),
  ##            (store_mul, ":min_enemy_str", "$g_enemy_fit_for_battle", 2),
  ##            (lt, ":min_enemy_str", "$g_friend_fit_for_battle"),
              (assign, ":attackers_retreat", 1),
            (else_try),
              (eq, "$g_battle_result", 0),
              (store_div, ":min_enemy_str", "$g_enemy_fit_for_battle", 3),
              (lt, ":min_enemy_str", "$g_friend_fit_for_battle"),
              (assign, ":attackers_retreat", 1),
            (else_try),
              (store_random_in_range, ":random_no", 0, 100),
              (lt, ":random_no", 10),
              (neq, "$new_encounter", 1),
              (assign, ":attackers_retreat", 1),
            (try_end),
            (try_begin),
              (eq, ":attackers_retreat", 1),
              (party_get_slot, ":siege_hardness", "$g_encountered_party", slot_center_siege_hardness),
              (val_add, ":siege_hardness", 100),
              (party_set_slot, "$g_encountered_party", slot_center_siege_hardness, ":siege_hardness"),
              (party_set_slot, "$g_enemy_party", slot_party_retreat_flag, 1),

              (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
                (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
                (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
                (gt, ":party_no", 0),
                (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
                (party_slot_eq, ":party_no", slot_party_ai_object, "$g_encountered_party"),
                (party_slot_eq, ":party_no", slot_party_ai_substate, 1),
                (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
                (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, "$g_encountered_party"),
              (try_end),
              (display_message, "@The enemy has been forced to retreat. The assault is over, but the siege continues."),
              (assign, "$g_battle_simulation_cancel_for_party", "$g_encountered_party"),
              ] + (is_a_wb_menu==1 and [
              (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
           		(options_set_battle_size, "$player_battlesize"),
         	  (try_end),
         	  ] or []) + [
              (leave_encounter),
              (change_screen_return),
              (assign, "$g_battle_simulation_auto_enter_town_after_battle", "$g_encountered_party"),
            (try_end),
          (try_end),
        (try_end),
        (assign, "$g_siege_first_encounter", 0),
        (assign, "$new_encounter", 0),

	#Calculate Formula A here - Kham
	(try_begin), 
		(eq, "$new_rank_formula_calculated", 0),
		(call_script, "script_calculate_formula_a"),
		(assign, "$nf_helping_allies", 1),
	(try_end),
	#Calculate Formula A END
        ],
    [
      ("siege_defender_join_battle",
       [
         (neg|troop_is_wounded, "trp_player"),
         ],
          "Join the battle.",[
              (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
              (assign, "$g_battle_result", 0),
              (try_begin),
                (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
                (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
              (else_try),
                (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
              (try_end),
              (call_script, "script_calculate_battle_advantage"),
              (val_mul, reg0, 2),
              (val_div, reg0, 3), #scale down the advantage a bit.
              ] + (is_a_wb_menu==1 and [
              (options_get_battle_size, "$player_battlesize"),
           	  (try_begin),
				(gt, "$player_battlesize", 415),
				(options_set_battle_size, 415), #200
				(assign, "$player_battlesize_changed", 1),
			  (try_end),
          	  ] or []) + [
              (set_battle_advantage, reg0),
              (set_party_battle_mode),
#              (try_begin),
#                (party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),
#                (set_jump_mission,"mt_castle_attack_walls_belfry"),
#              (else_try),
              (assign, ":siege_mission", "mt_castle_attack_walls_ladder"),
	          (try_begin),
	           	(eq, "$advanced_siege_ai",1),
	           	(assign, ":siege_mission", "mt_castle_attack_walls_ladder"),
	          (else_try),
	           	(eq, "$advanced_siege_ai", 0),
	           	(assign, ":siege_mission", "mt_castle_attack_walls_ladder_native"),
	          (try_end),
	          (set_jump_mission,":siege_mission"),
#              (try_end),
              (jump_to_scene,":battle_scene"),
              (assign, "$g_next_menu", "mnu_siege_started_defender"),
              (jump_to_menu, "mnu_battle_debrief"),
              (change_screen_mission)]),
      ("siege_defender_troops_join_battle",[(call_script, "script_party_count_members_with_full_health", "p_main_party"),
                                            (this_or_next|troop_is_wounded,  "trp_player"),
                                            (ge, reg0, 3)],
          "Order your men to join the battle without you.",[
              (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
              (select_enemy,1),
              (assign,"$g_enemy_party","$g_encountered_party_2"),
              (assign,"$g_ally_party","$g_encountered_party"),
              (assign,"$g_siege_join", 1),
              (jump_to_menu,"mnu_siege_join_defense")]),
     ("siege_defender_do_not_join_battle",[(eq, cheat_switch, 1),(call_script, "script_party_count_fit_regulars","p_collective_ally"),
                                           (gt, reg0, 0)],
      "Don't get involved.", [(leave_encounter),
                              (change_screen_return),
          ]),

##      ("siege_defender_surrender",[(call_script, "script_party_count_fit_regulars","p_collective_ally"),
##                                   (this_or_next|eq, reg0, 0),
##                                   (party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player"),
##                                   ],
##       "Surrender.",[(assign, "$g_player_surrenders", 1),
##                     (jump_to_menu,"mnu_under_siege_attacked_continue")]),
    ]
 ),
( "siege_join_defense",mnf_scale_picture|mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    code_to_set_city_background + [
        (try_begin),
          (eq, "$g_siege_join", 1),
          (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
          (assign, ":player_party_strength", reg0),
          (val_div, ":player_party_strength", 5),
        (else_try),
          (assign, ":player_party_strength", 0),
        (try_end),
        
        (call_script, "script_party_calculate_strength", "p_collective_ally", 0),
        (assign, ":ally_party_strength", reg0),
        (val_div, ":ally_party_strength", 5),
        (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 10),

        (store_add, ":friend_party_strength", ":player_party_strength", ":ally_party_strength"),
        (assign, ":enemy_party_strength_for_p", ":enemy_party_strength"),
        (val_mul, ":enemy_party_strength_for_p", ":player_party_strength"),
        (val_div, ":enemy_party_strength_for_p", ":friend_party_strength"),

        (val_sub, ":enemy_party_strength", ":enemy_party_strength_for_p"),
        (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength_for_p", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s8, s0),

        (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),
        (party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),

        (inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s10, s0),
        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

        (try_begin),
          (call_script, "script_party_count_members_with_full_health","p_main_party"),
          (le, reg(0), 0),
          (str_store_string, s4, "str_siege_defender_order_attack_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
          (le, reg(0), 0),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_siege_defender_order_attack_success"),
        (else_try),
          (str_store_string, s4, "str_siege_defender_order_attack_continue"),
        (try_end),
    ],
    [("continue",[],"Continue...",[(jump_to_menu,"mnu_siege_started_defender"),]),]
 ),

( "village_hunt_down_fugitive_defeated",0,
    "^^^^^A heavy blow from the fugitive sends you to the ground, and your vision spins and goes dark.\
 Time passes. When you open your eyes again you find yourself battered and bloody,\
 but luckily none of the wounds appear to be lethal.",
    "none",
    [],
    [("continue",[],"Continue...",[(jump_to_menu, "mnu_town"),]),],
 ),

( "town_bandits_failed",mnf_disable_all_keys,
    "^^^^^{s4} {s5}",
    "none",
    [
#      (call_script, "script_loot_player_items", 0),
      (store_troop_gold, ":total_gold", "trp_player"),
      (store_div, ":gold_loss", ":total_gold", 30),
      (store_random_in_range, ":random_loss", 40, 100),
      (val_add, ":gold_loss", ":random_loss"),
      (val_min, ":gold_loss", ":total_gold"),
      (troop_remove_gold, "trp_player",":gold_loss"),
      (party_set_slot, "$current_town", slot_center_has_bandits, 0),
      (party_get_num_companions, ":num_companions", "p_main_party"),
      (str_store_string, s4, "@The assasins beat you down and leave you for dead. ."),
      (str_store_string, s4, "@You have fallen. The bandits quickly search your body for valuables they can find,\
 then vanish into the night. They have left you alive, if only barely."),
      (try_begin),
        (gt, ":num_companions", 2),
        (str_store_string, s5, "@Luckily some of your companions came to search for you when you did not return, and find you lying in the ditch. They carried you to safety and dressed your wounds."),
      (else_try),
        (str_store_string, s5, "@Luckily some passing locals found you lying in the ditch, and recognised you as someone other than a simple beggar. They carried you to safety and dressed your wounds."),
      (try_end),
    ],
    [("continue",[],"Continue...",[(change_screen_return)]),],
 ),
( "town_bandits_succeeded",mnf_disable_all_keys,
    "^^^^^The goblins fall before you as wheat to a scythe! Soon you stand alone\
 while most of your attackers lie unconscious, dead or dying.\
 Surely the locals would be very grateful that you saved them from this menace.",
    "none",
    [
      (party_set_slot, "$current_town", slot_center_has_bandits, 0),
      (assign, "$g_last_defeated_bandits_town", "$g_encountered_party"),
      (try_begin),
        (check_quest_active, "qst_deal_with_night_bandits"),
        (neg|check_quest_succeeded, "qst_deal_with_night_bandits"),
        (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_target_center, "$g_encountered_party"),
        (call_script, "script_succeed_quest", "qst_deal_with_night_bandits"),
      (try_end),
      (store_mul, ":xp_reward", "$num_center_bandits", 117),
      (add_xp_to_troop, ":xp_reward", "trp_player"),
      (store_mul, ":gold_reward", "$num_center_bandits", 50),
      (quest_get_slot, ":quest_giver", "qst_deal_with_night_bandits", slot_quest_giver_troop),
      (store_troop_faction, ":quest_faction", ":quest_giver"),
      #(call_script, "script_troop_add_gold","trp_player",":gold_reward"),
      (call_script, "script_add_faction_rps", ":quest_faction", ":gold_reward"),
    ],
    [("continue",[],"Continue...",[(change_screen_return)]),],
 ),

( "town_brawl_lost",mnf_disable_all_keys,
    "^^^^^^You have been knocked out cold. The people you attacked quickly search you for valuables, before carrying on with their daily business.",
    "none",
    [ (store_troop_gold, ":total_gold", "trp_player"),
      (store_div, ":gold_loss", ":total_gold", 30),
      (store_random_in_range, ":random_loss", 40, 100),
      (val_add, ":gold_loss", ":random_loss"),
      (val_min, ":gold_loss", ":total_gold"),
      #(troop_remove_gold, "trp_player",":gold_loss"),
      (call_script, "script_add_faction_rps", "$ambient_faction", ":gold_loss"),
    ],
    [("continue",[],"Continue...",[(change_screen_return)]),],
 ),
( "town_brawl_won",mnf_disable_all_keys,
    "^^^^^You have beaten all the opponents and the guards sent to quell the disturbance. You quickly frisk them for valuables then vanish until tempers quieten down.^Maybe next time they would show more respect and back off.",
    "none",
    [ (store_random_in_range, ":random_gold", 200, 500),
      #(call_script, "script_troop_add_gold", "trp_player", ":random_gold"),
      (call_script, "script_add_faction_rps", "$ambient_faction", ":random_gold"),
    ],
    [("continue",[],"Continue...",[(change_screen_return)]),],
 ),
  
( "close",0,"Nothing.", "none",[(change_screen_return)],[]),

( "town",mnf_enable_hot_keys|city_menu_color,
	"You arrived in {s60}.{s12}{s13}",
    "none",
    code_to_set_city_background + [   
		
		(call_script, "script_unequip_items", "trp_player"), # after a shop, player returns to this menu so check here
		
		# Workaround for Isengard underground
		(troop_set_slot, "trp_player", slot_troop_morality_state, 0),

		(try_begin), # Fix elders and barmen at capturable centers
			(lt,"$savegame_version",2),
			(call_script,"script_update_savegame"),
		(try_end),

		(try_begin),
          (eq, "$sneaked_into_town", 1),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
        (else_try),
          #MV: commented this out - lets both the map travel and town music continue to this menu
          #(call_script, "script_music_set_situation_with_culture", mtf_sit_travel), 
        (try_end),
		(assign, "$current_town","$g_encountered_party"),   # mtarini...  was:(store_encountered_party,"$current_town"),
		
		(try_begin),
			(eq, "$cheat_mode",1),
			(str_store_party_name, s29, "$current_town"),
			(display_message, "@{s29}"),
		(try_end),
		
        (call_script, "script_update_center_recon_notes", "$current_town"),
        (assign, "$g_defending_against_siege", 0),
        (str_clear, s3),
        (party_get_battle_opponent, ":besieger_party", "$current_town"),
        (store_faction_of_party, ":encountered_faction", "$g_encountered_party"),
        (party_get_slot, ":encountered_subfaction", "$g_encountered_party", slot_party_subfaction),

		(try_begin),
			(eq, ":encountered_faction", "fac_gondor"),
			(neq, ":encountered_subfaction", 0),
			(store_add, ":str_subfaction", ":encountered_subfaction", "str_subfaction_gondor_name_begin"),
			(str_store_string, s61, ":str_subfaction"),
		(else_try),
			(str_store_faction_name, s61,":encountered_faction"), # non subfaction city get faction name in S61
		(try_end),

        (store_relation, ":faction_relation", ":encountered_faction", "fac_player_supporters_faction"),
		
		#(party_get_slot,reg22, "$current_town", slot_party_subfaction),
		#(party_get_slot,reg23, "$current_town", slot_town_weaponsmith),
		#(str_store_troop_name, s24, reg23 ),
		#(troop_get_slot, reg24, reg23 , slot_troop_subfaction),
		
        (try_begin),
          (gt, ":besieger_party", 0),
          (ge, ":faction_relation", 0),
          (store_faction_of_party, ":besieger_party_faction", ":besieger_party"),
          (store_relation, ":besieger_party_relation", ":besieger_party_faction", "fac_player_supporters_faction"),
          (lt, ":besieger_party_relation", 0),
          (assign, "$g_defending_against_siege", 1),
          (assign, "$g_siege_first_encounter", 1),
          (jump_to_menu, "mnu_siege_started_defender"),
        (try_end),

        #Quest menus
        (try_begin),
          (gt, "$quest_auto_menu", 0),
          (jump_to_menu, "$quest_auto_menu"),
          (assign, "$quest_auto_menu", 0),
        (try_end),

        (assign, "$talk_context", 0),
        (assign,"$all_doors_locked",0),

        (try_begin),
          (eq, "$g_town_visit_after_rest", 1),
          (assign, "$g_town_visit_after_rest", 0),
          #(assign, "$town_entered", 1),
        (try_end),

        (try_begin),
          (eq,"$g_leave_town",1),
          (assign,"$g_leave_town",0),
          (assign,"$g_permitted_to_center",0),
          (leave_encounter),
          (change_screen_return),
        (try_end),

        (str_store_party_name,s2, "$current_town"),
		(str_store_string, s60, s2),
        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (store_faction_of_party, ":center_faction", "$current_town"),
        (str_store_faction_name,s9,":center_faction"),
        (try_begin),
          (ge, ":center_lord", 0),
          (str_store_troop_name,s8,":center_lord"),
          (str_store_string,s7,"@{s8} of {s9}"),
        (try_end),
        
        #(try_begin),
        #  (party_slot_eq,"$current_town",slot_party_type, spt_town),
        #  (party_get_slot, ":prosperity", "$current_town", slot_town_prosperity),
        #  (val_add, ":prosperity", 5),
        #  (store_div, ":str_offset", ":prosperity", 10),
        #  (store_add, ":str_id", "str_town_prosperity_0",  ":str_offset"),
        #  (str_store_string, s10, ":str_id"),
        #(else_try),
        #  (str_store_string,s10,"@You are at {s2}."),
        #(try_end),
        
        (str_clear, s12),
        # (try_begin),
          # (party_slot_eq,"$current_town",slot_party_type, spt_town),
          # (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
          # (call_script, "script_describe_center_relation_to_s3", ":center_relation"),
          # (assign, reg9, ":center_relation"),
          # (str_store_string, s12, "@ {s3} ({reg9})."),
		# (try_end),

        (str_clear, s13),

        #night?
        (try_begin), 
         (store_time_of_day,reg(12)),
         (ge,reg(12),5),
         (lt,reg(12),21),
         (assign,"$town_nighttime",0),
        (else_try),
         (assign,"$town_nighttime",1),
         (party_slot_eq,"$current_town",slot_party_type, spt_town),
         (str_store_string, s13, "str_town_nighttime"),
        (try_end),
        
        (try_begin), 
          (gt,"$entry_to_town_forbidden",0),
          (str_store_string, s13, "@{s13}^^You have successfully sneaked in."),
        (try_end),
		
		(assign, "$bs_day_sound", 0), # specific ambiance?
		(assign, "$bs_night_sound", 0),
	
        #(assign,"$castle_undefended",0),
        #(party_get_num_companions, ":castle_garrison_size", "p_collective_enemy"),
        #(try_begin),
        #  (eq,":castle_garrison_size",0),
        #  (assign,"$castle_undefended",1),
        #(try_end),
        ],
    [
       # stub menus to make passage 2 lead to castle
	   ("town_menu_0",[(eq,0,1),],"Go to some location.",
       [], "Door to some location."),

       ("town_approach",[(party_slot_eq,"$current_town",slot_party_type, spt_town),
          (this_or_next|eq,"$entry_to_town_forbidden",0),
          (eq, "$sneaked_into_town",1),
		  (try_begin),
		    #kham fix for some weird elder switching that occurs...
		  	#(eq, "$current_town", "p_town_cair_andros"),
		  	#(party_set_slot, "p_town_cair_andros", slot_town_elder, "trp_elder_cairandros"),
		  	#(str_store_troop_name_plural, s1, "trp_elder_cairandros"),
		  #(else_try), # elder troop stores center common name in plural register

		  # Rafa: For towns that don't get destroyed, we get the original elder's plural name
		]+concatenate_scripts([[
			(eq, "$current_town", center_list[x][0]),
		  	(neg|party_slot_eq, "$current_town", slot_town_elder, "trp_no_troop"),
		    (str_store_troop_name_plural, s1, center_list[x][2][3]),
		  (else_try),] for x in range(len(center_list)) if center_list[x][8]==0] )+[
		  	(neg|party_slot_eq, "$current_town", slot_town_elder, "trp_no_troop"),
			(party_get_slot, ":elder_troop", "$current_town", slot_town_elder),
		    (str_store_troop_name_plural, s1, ":elder_troop"),
		  (else_try),
		    (str_store_string, s1, "@the_place"),
		  (try_end),
		  ],"Approach {s1}...",
       [(call_script, "script_initialize_center_scene"),
		(assign, "$spawn_horse", 0),
		(try_begin),(troop_is_mounted, "trp_player"),(set_jump_entry, 1),
		 (else_try),                                 (set_jump_entry, 2),
		(try_end),
		(party_get_slot, ":town_scene", "$current_town", slot_town_center),
        (jump_to_scene, ":town_scene"),
        (change_screen_mission),
	   ]),

	   ("town_castle",[
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          (eq,"$entry_to_town_forbidden",0),
          (neg|party_slot_eq,"$current_town", slot_town_castle, -1),

		  (try_begin),   # barman troop stores center common name in plural register
			(party_get_slot, ":barman_troop", "$current_town", slot_town_barman),
		    (neq, ":barman_troop",  "trp_no_troop"),
		    (neq, ":barman_troop",  -1),
			(party_get_slot, ":barman_troop", "$current_town", slot_town_barman),
		    (str_store_troop_name_plural, s1, ":barman_troop"),
		  (else_try),
		    (str_store_string, s1, "@the_castle"),
		  (try_end),
		  
#          (party_slot_eq, "$current_town", slot_castle_visited, 1), #check if scene has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
          ],"Go to {s1}.",
		  
       [
           (try_begin),
             (this_or_next|eq, "$all_doors_locked", 1),
             (eq, "$sneaked_into_town", 1),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (else_try),
#             (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
#             (scene_slot_eq, ":castle_scene", slot_scene_visited, 0),
#             (display_message,"str_door_locked",0xFFFFAAAA),
#           (else_try),
             #(assign, "$town_entered", 1),
             (call_script, "script_enter_court", "$current_town"),
           (try_end),
        ], "Door to the castle."),
      
      ("town_center",[
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
		  (party_slot_eq,"$current_town",slot_center_visited, 1),
          (this_or_next|eq,"$entry_to_town_forbidden",0),
          (eq, "$sneaked_into_town",1),
	   ], "Walk to the main square...",
     [ (call_script, "script_initialize_center_scene"),
	   (assign, "$spawn_horse", 1),
       #(assign, "$town_entered", 1),
	   (party_set_slot,"$current_town", slot_center_visited, 1),
	   #(set_jump_entry, 0),
       (party_get_slot, ":town_scene", "$current_town", slot_town_center),
	   (jump_to_scene, ":town_scene"),
       (change_screen_mission),
	   ], "Door to the town center."),

	          
	   ("aw_chamber",
       [(eq, 1, 0)],"Never: Enter the AW chamber.",
       [ 
	  	 (set_jump_mission,"mt_aw_tomb"),
	     (jump_to_scene, "scn_aw_tomb"),
         (change_screen_mission),
       ],"Open the door."),

		
	  ("trade_with_arms_merchant",[(party_slot_eq,"$current_town",slot_party_type, spt_town),
	  (this_or_next|eq,"$tld_option_crossdressing", 1),(eq,"$entry_to_town_forbidden",0), #  crossdresser can get in
      (this_or_next|eq,"$tld_option_town_menu_hidden",0),(party_slot_eq, "$current_town", slot_weaponsmith_visited, 1), #check if weaponsmith has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
      (neg|party_slot_eq, "$current_town", slot_town_weaponsmith, "trp_no_troop"),
      (try_begin),
      	(eq, "$current_town", "p_town_cair_andros"), ##Kham fix for weird slot switching
		(store_faction_of_party, ":town_faction", "$current_town"),
		(eq, ":town_faction", "fac_gondor"), #InVain Fix to Cair Andros smith always belonging to Gondor, even after CA has been captured
	  	(party_set_slot, "p_town_cair_andros", slot_town_weaponsmith, "trp_smith_candros"),
	  	(str_store_troop_name_plural, s40, "trp_smith_candros"),
	  (else_try),
	    (this_or_next|eq, "$current_town", "p_town_west_osgiliath"),
		(eq, "$current_town", "p_town_east_osgiliath"),
		(store_faction_of_party, ":town_faction", "$current_town"),
		(eq, ":town_faction", "fac_gondor"),
	  	(party_set_slot, "$current_town", slot_town_weaponsmith, "trp_smith_wosgiliath"),
	  	(str_store_troop_name_plural, s40, "trp_smith_wosgiliath"),
	  (else_try),
		(party_get_slot, ":troop", "$current_town", slot_town_weaponsmith),
	  	(str_store_troop_name_plural, s40, ":troop"),
	  	(try_end),],
       "Visit the {s40}.",
       [(party_get_slot, ":troop", "$current_town", slot_town_weaponsmith),(change_screen_trade, ":troop")]),
		
	  ("trade_with_horse_merchant",[(party_slot_eq,"$current_town",slot_party_type, spt_town),
	  (this_or_next|eq,"$tld_option_crossdressing", 1),(eq,"$entry_to_town_forbidden",0), #  crossdresser can get in
      (this_or_next|eq,"$tld_option_town_menu_hidden",0),(party_slot_eq, "$current_town", slot_merchant_visited, 1), #check if horse_merchant has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
      (neg|party_slot_eq, "$current_town", slot_town_merchant, "trp_no_troop"),
	  (party_get_slot, ":troop", "$current_town", slot_town_merchant),
	  (str_store_troop_name_plural, s41, ":troop"),],
       "Visit the {s41}.",
       [(party_get_slot, ":troop", "$current_town", slot_town_merchant),(change_screen_trade, ":troop")]),

#	  ("improve_equipment",[
#		(party_slot_eq,"$current_town",slot_party_type, spt_town),
#	  	(this_or_next|eq,"$tld_option_crossdressing", 1),(eq,"$entry_to_town_forbidden",0), #  crossdresser can get in
#      		(this_or_next|eq,"$tld_option_town_menu_hidden",0),(party_slot_eq, "$current_town", slot_weaponsmith_visited, 1), #check if weaponsmith has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
#      		(neg|party_slot_eq, "$current_town", slot_town_weaponsmith, "trp_no_troop"),
#      		(call_script, "script_get_faction_rank", "$g_talk_troop_faction"), (assign, ":rank", reg0), #rank points to rank number 0-9
#     		(ge, ":rank", 9),
#	  	(party_get_slot, ":troop", "$current_town", slot_town_weaponsmith),
#	  	(str_store_troop_name, s40, ":troop"),],
#       "Have {s40} improve your equipment.",
#       [
#	(party_get_slot, ":troop", "$current_town", slot_town_weaponsmith),
#             (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
#             (set_visitor,	0,	"trp_player"),
#             (set_visitor,	17,	":troop"),
#             (set_jump_mission,"mt_conversation_encounter"),
#             (jump_to_scene,"scn_conversation_scene"),
#             (assign, "$talk_context", tc_improve_equipment),
#             (change_screen_map_conversation, ":troop")
#	]),


	   ("town_prison", [(eq,1,0)],"Never: Enter the prison.",
       [   (try_begin),
             (eq,"$all_doors_locked",1),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (else_try),
             (this_or_next|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
             (eq, "$g_encountered_party_faction", "$players_kingdom"),
             #(assign, "$town_entered", 1),
             (call_script, "script_enter_dungeon", "$current_town", "mt_visit_town_castle"),
           (else_try),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (try_end),
        ],"Door to the prison."),
		
		
	 #Enter dungeon in Erebor begin (Kolba)
      ("dungeon_enter",[#(eq, cheat_switch, 1), # not done yet
	    (party_slot_eq,"$current_town",slot_party_type, spt_town),
        (eq, "$current_town", "p_town_erebor"),
        (quest_slot_ge, "qst_find_lost_spears", slot_quest_current_state, 1),
        ],"Search for the lost spears inside the mountains.",[
              (set_jump_mission, "mt_tld_erebor_dungeon"),
              (modify_visitors_at_site,"scn_erebor_dungeon_01"),	      
              (reset_visitors),
              (set_visitor,1,"trp_player"),
              (set_visitor, 2, "trp_i1_gunda_goblin"),
              (set_visitor, 3, "trp_i4_gunda_orc_warrior"),
              (set_visitor, 4, "trp_i3_gunda_orc_fighter"),
              (jump_to_scene, "scn_erebor_dungeon_01"),
              (change_screen_mission),
       ],"Open the door."),
      #Enter dungeon in Erebor end (Kolba)	  

      #Enter Dwarven Warehouse (Kham)
	("dwarven_warehouse",[(eq,1,0)],
	"Visit the Dwarven Warehouse",[
							(set_jump_mission,"mt_tld_dwarven_warehouse"),
							(set_passage_menu, "mnu_town"),
							(jump_to_scene,"scn_underground_warehouse"),
							(change_screen_mission),
		],"Enter Dwarven Warehouse"),
	#Enter Dwarven Warehouse End (Kham)
		
	("talk_to_castle_commander",[(party_slot_eq,"$current_town",slot_party_type, spt_town),
	   	  (eq,"$entry_to_town_forbidden",0), 
          (party_get_num_companions, ":no_companions", "$g_encountered_party"),
          (ge, ":no_companions", 1),
       ],"Visit the {s61} Barracks.",[
             (set_jump_mission,"mt_conversation_encounter"),
             (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
             (set_visitor,0,"trp_player"),
             (call_script, "script_get_party_max_ranking_slot", "$g_encountered_party"),
             (party_stack_get_troop_id, reg6,"$g_encountered_party",reg0),
             (party_stack_get_troop_dna,reg7,"$g_encountered_party",reg0),
             (set_visitor,17,reg6,reg7),
             (jump_to_scene,"scn_conversation_scene"),
             (assign, "$talk_context", tc_hire_troops),
             (change_screen_map_conversation, reg6)
             ]),
		
      ("speak_with_elder",[(party_slot_eq,"$current_town",slot_party_type, spt_town),
	  (this_or_next|eq,"$tld_option_crossdressing", 1),(eq,"$entry_to_town_forbidden",0), #  crossdresser can get in
      (this_or_next|eq,"$tld_option_town_menu_hidden",0),(party_slot_eq, "$current_town", slot_elder_visited, 1), #check if elder has been visited before to allow entry from menu. Otherwise scene will only be accessible from the town center.
      (neg|party_slot_eq, "$current_town", slot_town_elder, "trp_no_troop"),
	  (party_get_slot, ":elder_troop", "$current_town", slot_town_elder),
	  (str_store_troop_name, s6, ":elder_troop"),
	  ],
       "Speak with the {s6}.",
       [   (party_get_slot, ":elder_troop", "$current_town", slot_town_elder),
           (call_script, "script_setup_troop_meeting", ":elder_troop", 0),
        ]),

	  ("castle_wait",
       [   (party_slot_eq,"$current_town",slot_party_type, spt_town),
		   (eq,"$entry_to_town_forbidden",0),
           (this_or_next|ge, "$g_encountered_party_relation", 0),
           (eq,"$castle_undefended",1),
           (str_clear, s1),
           (str_clear, s2),
           (try_begin),
             #(neg|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
             (party_get_num_companions, ":num_men", "p_main_party"),
             (store_div, reg1, ":num_men", 4),
             (val_add, reg1, 1),
             (store_troop_gold, ":gold", "trp_player"),
             (ge, ":gold", reg1),
             (str_store_string, s1, "@Stay indoors for some time ({reg1} Resource points per night)"),
           (else_try),
		     # not enough money... can rest anyway (but no health bonus)
             (str_store_string, s1, "@Camp outside for some time (free)"),
           (try_end),
			##           (eq, "$g_defending_against_siege", 0),
        ],
         "{s1}.",
         [ (assign,"$auto_enter_town","$current_town"),
           (assign, "$g_town_visit_after_rest", 1),
           (assign, "$g_last_rest_center", "$current_town"),
           (assign, "$g_last_rest_payment_until", -1),
           (rest_for_hours_interactive, 24 * 7, 5, 0), #rest while not attackable
           (change_screen_return),
          ]),

	  ##Kham - Player Initiated Siege BEGIN
	  ("player_initiate_siege",
	 	[#(eq, "$cheat_mode",1),
	 	 (eq, "$player_allowed_siege",1), #Kham - Global Var that allows player to siege. Set in Dialogues.
	 	 
	 	 (store_faction_of_party, ":faction_no", "$g_encountered_party"),
	 	 (faction_get_slot, ":faction_strength", ":faction_no", slot_faction_strength), #Check Faction Strength
	 	 
	 	 (party_get_slot, ":siegable", "$g_encountered_party", slot_center_siegability), #Check if we can siege
	     
	     (assign, ":continue", 0),
	     
	     (try_begin),
	     	(eq, ":siegable", tld_siegable_never), #some places are never siegable
		    #(display_message, "@Passed 1st"),
		    (assign, ":continue", 0),
	     (else_try),    
	     	(neq, ":siegable", tld_siegable_capital), #not a capital (we have a separate condition below)
		 	(this_or_next|eq, "$tld_option_siege_reqs", 2), # No siege reqs
	     	(this_or_next|eq, ":siegable", tld_siegable_always), # camps and such can always be sieged
	     	(lt, ":faction_strength", "$g_fac_str_siegable"), # otherwise, defenders need to be weak
	     	#(display_message, "@Passed 2nd"),
	     	(assign, ":continue", 1),
		 (else_try),
		 	(eq, ":siegable", tld_siegable_capital), #If it is the capital, check if there are other centers left
	     	(this_or_next|eq, "$tld_option_siege_reqs", 2), # No siege reqs
	     	(lt, ":faction_strength", "$g_fac_str_siegable"), #and fac str is low enough to siege
	     	(call_script, "script_cf_check_if_only_capital_left", "$g_encountered_party"), #and there are no other centers left (script fails when there is more than 1 center left.)
	     	#(display_message, "@Passed 3rd"),
	     	(assign, ":continue", 1),
	     (try_end),

	     (eq, ":continue", 1),

	 	 (neg|troop_is_wounded, "trp_player"),
	 	 (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1), #if besieged by Marshall, player can't attack.
	     (store_relation, ":reln", "$g_encountered_party_faction", "fac_player_supporters_faction"),
	     (lt, ":reln", 0),
	     (lt, "$g_encountered_party_2", 1),
	     (call_script, "script_party_count_fit_for_battle","p_main_party"),
	     (gt, reg0, 1),
	     (try_begin),
	    	 (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
	           (assign, reg6, 1),
	         (else_try),
	           (assign, reg6, 0),
	         (try_end),

	#Calculate Formula A here - Kham
	(try_begin), 
		(eq, "$new_rank_formula_calculated", 0),
		(call_script, "script_calculate_formula_a", 0),
	(try_end),
	#Calculate Formula A END
	
	    ],
	    "Attack the {reg6?town:castle}...",
	    [
	     (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
	     (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
	     (call_script, "script_let_nearby_parties_join_current_battle", 0, 0), #Kham - Let nearby lords join the battle
         (call_script, "script_encounter_init_variables"),
	     (call_script, "script_calculate_battle_advantage"),
		 (val_mul, reg0, 2),
		 (val_div, reg0, 3), #scale down the advantage a bit in sieges.
		 ] + (is_a_wb_menu==1 and [
         (options_get_battle_size, "$player_battlesize"),
         (try_begin),
				(gt, "$player_battlesize", 415),
				(options_set_battle_size, 415), #200
				(assign, "$player_battlesize_changed", 1),
		 (try_end),
         ] or []) + [
		 (set_battle_advantage, reg0),
		 (set_party_battle_mode),
 		 (assign, ":siege_mission", "mt_castle_attack_walls_ladder"),
         (try_begin),
           	(eq, "$advanced_siege_ai",1),
           	(assign, ":siege_mission", "mt_castle_attack_walls_ladder"),
         (else_try),
           	(eq, "$advanced_siege_ai", 0),
           	(assign, ":siege_mission", "mt_castle_attack_walls_ladder_native"),
         (try_end),
         (set_jump_mission,":siege_mission"),
		 (jump_to_scene,":battle_scene"),
		 (assign, "$g_siege_final_menu", "mnu_player_initiated_siege_result"),
		 (assign, "$g_siege_battle_state", 1),
		 (assign, "$g_next_menu", "mnu_player_initiated_siege_result"),
		 (jump_to_menu, "mnu_battle_debrief"),
		 (change_screen_mission),
		],
	),
	 ##Kham - Player Initiated Siege END

#      ("siege_leave",[(eq, "$g_defending_against_siege", 1)],"Try to break out...",[(jump_to_menu,"mnu_siege_break_out")]),#TODO: Go to Menu here.
 ]+concatenate_scripts([[ 
 #    ("town_cheat_alley",[(eq, cheat_switch, 1),(party_slot_eq,"$current_town",slot_party_type, spt_town),(eq, "$cheat_mode", 1)], "CHEAT: Go to the alley.",[
#							(party_get_slot, reg(11), "$current_town", slot_town_alley),
#							(set_jump_mission,"mt_ai_training"),
#							(jump_to_scene,reg(11)),
#							(change_screen_mission)]),
      ("castle_cheat_interior",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1)], "CHEAT! Interior.",[
							(set_jump_mission,"mt_ai_training"),
							(party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
							(jump_to_scene,":castle_scene"),
							(change_screen_mission)]),
      ("castle_cheat_town_exterior",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1)], "CHEAT: Exterior.",[
							(try_begin),
								(party_slot_eq,"$current_town",slot_party_type, spt_castle),
								(party_get_slot, ":scene", "$current_town", slot_castle_exterior),
							(else_try),
								(party_get_slot, ":scene", "$current_town", slot_town_center),
							(try_end),
							(set_jump_mission,"mt_ai_training"),
							(jump_to_scene,":scene"),
							(change_screen_mission)]),
      ("castle_cheat_dungeon",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1)], "CHEAT: Prison.",[
							(set_jump_mission,"mt_ai_training"),
							(party_get_slot, ":castle_scene", "$current_town", slot_town_prison),
							(jump_to_scene,":castle_scene"),
							(change_screen_mission)]),
      ("castle_cheat_town_walls",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1),(party_slot_eq,"$current_town",slot_party_type, spt_town),], "CHEAT! Town Walls.",[
							(party_get_slot, ":scene", "$current_town", slot_town_walls),
							(set_jump_mission,"mt_ai_training"),
							(jump_to_scene,":scene"),
							(change_screen_mission)]),
      ("cheat_town_start_siege",[(eq, cheat_switch, 1),(eq, "$cheat_mode", 1),
								(party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
								(lt, "$g_encountered_party_2", 1),
								(call_script, "script_party_count_fit_for_battle","p_main_party"),
								(gt, reg(0), 1),
								(try_begin),
									(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
									(assign, reg6, 1),
								(else_try),
									(assign, reg6, 0),
								(try_end)],
				   "CHEAT: Besiege the {reg6?town:castle}...",
				   [   (assign,"$g_player_besiege_town","$g_encountered_party"),
					   (jump_to_menu, "mnu_castle_besiege"),
					   ]),
#      ("center_reports",[(eq, "$cheat_mode", 1),], "CHEAT: Show reports.",
#						[(jump_to_menu,"mnu_center_reports")]),
#    ("sail_from_port",[(eq, cheat_switch, 1),(party_slot_eq,"$current_town",slot_party_type, spt_town),(eq, "$cheat_mode", 1),#(party_slot_eq,"$current_town",slot_town_near_shore, 1),
#                       ], "CHEAT: Sail from port.",
#						[(assign, "$g_player_icon_state", pis_ship),
#						(party_set_flags, "p_main_party", pf_is_ship, 1),
#						(party_get_position, pos1, "p_main_party"),
#						(map_get_water_position_around_position, pos2, pos1, 6),
#						(party_set_position, "p_main_party", pos2),
#						(assign, "$g_main_ship_party", -1),
#						(change_screen_return)]),
 ] for ct in range(cheat_switch)])+[

 ]+concatenate_scripts([[ 
      ("town_cheat_alley",[(eq, 0, 1),], "CHEAT",[]),
	  ("castle_cheat_interior",[(eq, 0, 1),], "CHEAT",[]),
	  ("castle_cheat_town_exterior",[(eq, 0, 1),], "CHEAT",[]),
	  ("castle_cheat_dungeon",[(eq, 0, 1),], "CHEAT",[]),
	  ("castle_cheat_town_walls",[(eq, 0, 1),], "CHEAT",[]),
	  ("cheat_town_start_siege",[(eq, 0, 1),], "CHEAT",[]),
	  ("center_reports",[(eq, 0, 1),], "CHEAT",[]),
	  ("sail_from_port",[(eq, 0, 1),], "CHEAT",[]),
 ] for ct in range(1-cheat_switch)])+[

#menu no. 19
	  ("isengard_underground",[(party_slot_eq,"$current_town",slot_party_type, spt_town),(eq, "$current_town", "p_town_isengard"),(eq,"$entry_to_town_forbidden",0)
						], "Go to the underground caverns.",
						[
						(troop_set_slot, "trp_player", slot_troop_morality_state, 22),
						(call_script, "script_initialize_center_scene"),
						#(set_jump_mission, "mt_town_center"),
						(jump_to_scene, "scn_isengard_underground"),
						(change_screen_mission)], "Go to the underground caverns"),

#menu no. 20
	  ("tirith_toplevel",[(party_slot_eq,"$current_town",slot_party_type, spt_town),(eq, "$current_town", "p_town_minas_tirith"),(eq,"$entry_to_town_forbidden",0)
						], "Climb up to the top level.",
						[(assign, "$bs_day_sound", "snd_wind_ambiance"),
						 (assign, "$bs_night_sound", "snd_wind_ambiance"),
						 (set_jump_mission, "mt_town_center"),
						 (jump_to_scene, "scn_minas_tirith_center_top"),
						 (change_screen_mission)]),
						 
#menu no. 21						 
  	  ("erebor_gates",[(party_slot_eq,"$current_town",slot_party_type, spt_town),(eq, "$current_town", "p_town_erebor"),(eq,"$entry_to_town_forbidden",0)
						], "Visit the Great Gates.",
						[(set_jump_mission, "mt_town_center"),
						 (jump_to_scene, "scn_erebor_outside"),
						 (change_screen_mission)]),
						
      ("town_leave",[],"Leave...",[
            (assign, "$g_permitted_to_center",0),
            (change_screen_return,0),
            (store_faction_of_party, ":fac", "$current_town"),
            (try_begin),
		(eq|this_or_next, ":fac", "fac_mordor"),
		(eq, ":fac", "fac_guldur"),
	    	(call_script, "script_update_respoint"), # Updates resource points		
	    (try_end),
          ],"Leave Area"),

    ]
 ),


##### Kham - Player Initiated Siege Result Begin
("player_initiated_siege_result",mnf_enable_hot_keys,  
    "You attacked this center under the banner of {s2}.",
    "none",
    code_to_set_city_background + [
    	(str_clear, s2),
        (str_store_faction_name, s2, "$players_kingdom"),
        (assign, "$g_enemy_party", "$g_encountered_party"),
        #(select_enemy, 0),
        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (assign, ":num_enemy_regulars_remaining", reg0),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
            (assign, ":next_menu", "mnu_total_victory"),
            ] + (is_a_wb_menu==1 and [
            (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
           		(options_set_battle_size, "$player_battlesize"),
         	(try_end),
          	] or []) + [
            (assign, "$g_next_menu", -1),
            (try_begin), #TLD: if center destroyable, disable it, otherwise proceed as normal
				(party_slot_ge, "$g_enemy_party", slot_center_destroy_on_capture, 1),
				(call_script, "script_destroy_center", "$g_enemy_party"),
			(else_try),
				(call_script, "script_give_center_to_faction", "$g_enemy_party", "$players_kingdom"),
				(call_script, "script_order_best_besieger_party_to_guard_center", "$g_enemy_party", "$players_kingdom"),
					# add a small garrison
					(try_for_range, ":unused", 0, 5),
						(call_script, "script_cf_reinforce_party", "$g_enemy_party"),
					(try_end),
		    (try_end),
          (else_try),
            (this_or_next|le, ":num_enemy_regulars_remaining", 0),
            (le, "$g_enemy_fit_for_battle", "$num_routed_enemies"), #kham - don't let routed enemies spawn
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
            (assign, ":next_menu", "mnu_total_victory"),
            ] + (is_a_wb_menu==1 and [
            (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
       			(options_set_battle_size, "$player_battlesize"),
         	(try_end),
         	] or []) + [
            (assign, "$g_next_menu", -1),
          (else_try),
          	(eq, "$g_battle_result", -1),
          	(assign, "$player_allowed_siege", 0),
          	] + (is_a_wb_menu==1 and [
            (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
           		(options_set_battle_size, "$player_battlesize"),
          	(try_end),
          	] or []) + [
          	(str_store_faction_name, s4, "$players_kingdom"),
          	(display_message, "@{s4}'s scouts have seen and reported your failure. You have brought shame to {s4} and the responsibility of this failure is yours alone.", color_bad_news),
          	(call_script, "script_increase_rank", "$players_kingdom", -250),
          (try_end),
          (eq, ":enemy_finished", 1),
          (call_script, "script_party_wound_all_members", "$g_enemy_party"),
          (jump_to_menu, ":next_menu"),
        (else_try),
          #(call_script, "script_party_count_members_with_full_health", "p_collective_friends"),
         # (assign, ":ally_num_soldiers", reg0),
          (eq, "$g_battle_result", -1),
          ] + (is_a_wb_menu==1 and [
          (try_begin),
           		(eq, "$player_battlesize_changed", 1),
           		(assign, "$player_battlesize_changed",0),
           		(options_set_battle_size, "$player_battlesize"),
          (try_end),
          ] or []) + [
          #(eq, ":ally_num_soldiers", 0), #battle lost
          #(assign, "$player_allowed_siege",0),
		  (assign, "$recover_after_death_menu", "mnu_recover_after_death_default"),
          (assign, "$g_next_menu", "mnu_tld_player_defeated"),
          (jump_to_menu, "mnu_total_defeat"),
        (try_end),
        ],
    [
          ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
 ),

##### Kham - Player Initiate Siege Result END

( "disembark",0,
    "Do you wish to disembark?",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"), ],
    [("disembark_yes", [], "Yes.",
       [(assign, "$g_player_icon_state", pis_normal),
        (party_set_flags, "p_main_party", pf_is_ship, 0),
        (party_get_position, pos1, "p_main_party"),
		(map_get_land_position_around_position,pos0,pos1,1),
        (party_set_position, "p_main_party", pos0),
        (try_begin),
#          (eq,1,0),  # empty ship commented out, GA
		  (le, "$g_main_ship_party", 0),
          (set_spawn_radius, 0),
          (spawn_around_party, "p_main_party", "pt_none"),
          (assign, "$g_main_ship_party", reg0),
          (party_set_flags, "$g_main_ship_party", pf_is_static|pf_always_visible|pf_hide_defenders|pf_is_ship, 1),
          (str_store_troop_name, s1, "trp_player"),
          (party_set_name, "$g_main_ship_party", "@{s1}'s Ship"),
          (party_set_icon, "$g_main_ship_party", "icon_ship"),
          (party_set_slot, "$g_main_ship_party", slot_party_type, spt_ship),
        (try_end),
        (enable_party, "$g_main_ship_party"),
        (party_set_position, "$g_main_ship_party", pos0),
        (party_set_icon, "$g_main_ship_party", "icon_ship_on_land"),
        (assign, "$g_main_ship_party", -1),
        (change_screen_return),
        ]),
      ("disembark_no", [], "No.",
       [(party_get_position, pos1, "p_main_party"),
		(map_get_water_position_around_position,pos0,pos1,1),
        (party_set_position, "p_main_party", pos0),
		(party_set_ai_object,"p_main_party", "p_main_party"),
		(change_screen_return),
        ]),
    ]
 ),
( "ship_reembark",0,
    "Do you wish to embark?",
    "none",
    [],
    [ ("reembark_yes", [], "Yes.",
       [(assign, "$g_player_icon_state", pis_ship),
        (party_set_flags, "p_main_party", pf_is_ship, 1),
        (party_get_position, pos1, "p_main_party"),
        (map_get_water_position_around_position, pos2, pos1, 6),
        (party_set_position, "p_main_party", pos2),
        (assign, "$g_main_ship_party", "$g_encountered_party"),
        (disable_party, "$g_encountered_party"),
        (change_screen_return),
        ]),
      ("reembark_no", [], "No.",
       [(change_screen_return),
        ]),
    ]
 ),

( "center_reports",city_menu_color,
    "Town Name: {s1}^Rent Income: {reg1} denars^Tariff Income: {reg2} denars^Food Stock: for {reg3} days",
    "none",
    code_to_set_city_background + [
	 (set_background_mesh, "mesh_ui_default_menu_window"),

	 (party_get_slot, ":town_food_store", "$g_encountered_party", slot_party_food_store),
     (call_script, "script_center_get_food_consumption", "$g_encountered_party"),
     (assign, ":food_consumption", reg0),
     (store_div, reg3, ":town_food_store", ":food_consumption"),
     (str_store_party_name, s1, "$g_encountered_party"),
     (party_get_slot, reg1, "$g_encountered_party", slot_center_accumulated_rents),
     (party_get_slot, reg2, "$g_encountered_party", slot_center_accumulated_tariffs),
     ],
    [
      
      ("go_back_dot",[],"Go back.",
       [(try_begin),
          # (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
          # (jump_to_menu, "mnu_village"),
        # (else_try),
          (jump_to_menu, "mnu_town"),
        (try_end),
        ]),
    ]
 ),

( "sneak_into_town_suceeded",city_menu_color,
    "Disguised in the garments of a poor pilgrim, you fool the guards and make your way into the town.",
    "none",
     code_to_set_city_background +  [	],
    [("continue",[],"Continue...",[(assign, "$sneaked_into_town",1),(jump_to_menu,"mnu_town")])]
 ),
( "sneak_into_town_caught",city_menu_color,
    "As you try to sneak in, one of the guards recognizes you and raises the alarm!\
 You must flee back through the gates before all the guards in the town come down on you!",
    "none",
     code_to_set_city_background + [
	 (assign, "$recover_after_death_menu", "mnu_recover_after_death_town_alone"),
     #(assign,"$auto_menu","mnu_tld_player_defeated"),
    ],
    [("sneak_caught_fight",[],"Try to fight your way out!",
       [   (assign,"$all_doors_locked",1),
           (party_get_slot, ":sneak_scene", "$current_town",slot_town_center), # slot_town_gate),
           (set_jump_mission,"mt_sneak_caught_fight"),
           (modify_visitors_at_site,":sneak_scene"),(reset_visitors),
           (set_visitor,0,"trp_player"),
           (store_faction_of_party, ":town_faction","$current_town"),
           (faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_2_troop),
           (faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
           (try_begin),
             (gt, ":tier_2_troop", 0),
             (gt, ":tier_3_troop", 0),
             (assign,reg(0),":tier_3_troop"),
             (assign,reg(1),":tier_3_troop"),
             (assign,reg(2),":tier_2_troop"),
             (assign,reg(3),":tier_2_troop"),
           (else_try),
             (assign,reg(0),"trp_ac3_skirmisher_of_rohan"),
             (assign,reg(1),"trp_ac4_veteran_skirmisher_of_rohan"),
             (assign,reg(2),"trp_i5_gon_vet_swordsman"),
             (assign,reg(3),"trp_ac4_veteran_skirmisher_of_rohan"),
           (try_end),
           (assign,reg(4),-1),
           (shuffle_range,0,5),
           (set_visitor,1,reg(0)),
           (set_visitor,2,reg(1)),
           (set_visitor,3,reg(2)),
           (set_visitor,4,reg(3)),
 #          (jump_to_menu,"mnu_captivity_start_castle_defeat"),
           (set_passage_menu,"mnu_town"),
           (jump_to_scene,":sneak_scene"),
           (change_screen_mission),
        ]),
      ("sneak_caught_surrender",[],"Surrender.",
       [   (assign, "$recover_after_death_menu", "mnu_recover_after_death_town_alone"),
           (jump_to_menu,"mnu_tld_player_defeated"),
        ]),
    ]
 ),
( "sneak_into_town_caught_dispersed_guards",city_menu_color,
    "You drive off the guards and cover your trail before running off, easily losing your pursuers in the maze of streets.",
    "none",
    code_to_set_city_background + [],
     [("continue",[],"Continue...",[(assign, "$sneaked_into_town",1),(jump_to_menu,"mnu_town")])]
 ),
( "sneak_into_town_caught_ran_away",0,
    "You make your way back through the gates and quickly retreat to the safety out of town.",
    "none",
    [],
    [("continue",[],"Continue...",
       [ (assign,"$auto_menu",-1),
         (store_encountered_party,"$last_sneak_attempt_town"),
         (store_current_hours,"$last_sneak_attempt_time"),
         (change_screen_return),
        ]),
    ]
 ),

( "auto_training_ground_trainer", 0, "stub", "none",
	[	(jump_to_menu, "mnu_town"),
		(assign, "$talk_context", tc_town_talk),
		(party_get_slot, ":training_scene", "$g_encountered_party", slot_town_arena),
		(set_jump_mission, "mt_training_ground_trainer_talk"),
		(modify_visitors_at_site, ":training_scene"),
		(reset_visitors),
		(set_visitor, 0, "trp_player"),
		(jump_to_scene, ":training_scene"),
		(change_screen_mission),
		(music_set_situation, 0),
    ],
    []
 ),
  
## UNIFIED PLAYER DEFEATED MENUS... (mtarini)
###########################
# player death scenario in TLD: no capture, only injury
( "tld_player_defeated",0,
     "^^^^^Suddenly a shattering pain explodes in the back of your head! \ You shiver, as all the world goes black around you...^Is this your end?",
     "none",[
	 (store_add, reg10, "$player_looks_like_an_orc", "mesh_draw_defeat_human"), (set_background_mesh, reg10),
	 (val_add, "$number_of_player_deaths", 1),
	 ],[      
	    ("continue",[],"Continue...",
        [	(assign, "$auto_menu", "$recover_after_death_menu"),
            (rest_for_hours, 8, 8, 0),
			#(jump_to_menu, "$recover_after_death_menu"),
            
            #MV: lose some of your companions
            (try_for_range, ":npc", companions_begin, companions_end),
              (main_party_has_troop, ":npc"),
              (store_random_in_range, ":rand", 0, 100),
              (lt, ":rand", 30),
              (remove_member_from_party, ":npc", "p_main_party"),
              (troop_set_slot, ":npc", slot_troop_occupation, 0),
              (troop_set_slot, ":npc", slot_troop_playerparty_history, pp_history_scattered),
              (store_faction_of_party, ":victorious_faction", "$g_encountered_party"),
              (troop_set_slot, ":npc", slot_troop_playerparty_history_string, ":victorious_faction"),
              (troop_set_health, ":npc", 100),
            (try_end),
            (try_for_range, ":npc", new_companions_begin, new_companions_end),
              (main_party_has_troop, ":npc"),
              (store_random_in_range, ":rand", 0, 100),
              (lt, ":rand", 30),
              (remove_member_from_party, ":npc", "p_main_party"),
              (troop_set_slot, ":npc", slot_troop_occupation, 0),
              (troop_set_slot, ":npc", slot_troop_playerparty_history, pp_history_scattered),
              (store_faction_of_party, ":victorious_faction", "$g_encountered_party"),
              (troop_set_slot, ":npc", slot_troop_playerparty_history_string, ":victorious_faction"),
              (troop_set_health, ":npc", 100),
            (try_end),
            
			(change_screen_map),
			(display_message,"@Time passes..."),
         ]),
	 ]
 ),
( "recover_after_death_fangorn",0,
    "You wake up. The forest is still around you. Every bone hurts. You are alive, by miracle.^^It was a defeat, but at least you were able to see what happened. ^Now you know what is going on in this accursed forest,^and you survived to tell. ^^Will anyone ever believe you?",
	"none",[(try_begin),
				(eq, "$g_battle_result", 1),
				(jump_to_menu, "mnu_fangorn_battle_debrief_won"),
			(else_try),
				(assign, "$recover_after_death_menu", "mnu_recover_after_death_fangorn"),
				(jump_to_menu, "mnu_tld_player_defeated"),
			(try_end),
	 ],[
	 ("continue",[],"Continue...",[
		(troop_set_health,"trp_player",0),
		(try_begin),
			(check_quest_active, "qst_investigate_fangorn"),
			(neg|check_quest_succeeded, "qst_investigate_fangorn"),
			(neg|check_quest_failed, "qst_investigate_fangorn"),
			(call_script, "script_succeed_quest", "qst_investigate_fangorn"),
		(try_end),
		(change_screen_map)])]
 ),
( "recover_after_death_moria",city_menu_color,
    "^^^^^You regain your conciousness. You are lying on soft soil, fresh air breezing on your face. You are outside!^The orcs must have taken you for dead and thrown you in some murky pit.^You must have been carried to the surface by an underground stream.",
    "none",[(set_background_mesh, "mesh_town_moria"),],[
	  ("whatever",[], "Get up!",[ (change_screen_map),(jump_to_menu,"mnu_castle_outside"), ]),
	]
 ),
( "recover_after_death_default",0,
     "^^^^^You regain your conciousness. You lie on the spot you fell.\
  The enemies must have taken you up for dead and left you there.\
  However, it seems that none of your wounds were lethal,\
  and although you feel awful, you find out you can still walk.\
  You get up and try to look for any other survivors from your party.",
     "none",
	 [(set_background_mesh, "mesh_ui_default_menu_window")],[      
	 ("continue",[],"Continue...",[(change_screen_map)])]
 ),
( "recover_after_death_town",0,
     "^^^^You regain your conciousness and find yourself at the town outskirts. \
  You are alive!\
  Nobody is around and you take your chance to drag yourself outside the town.\
  It seems that none of your wounds were lethal,\
  and although you feel awful, you can still walk.",
     "none",code_to_set_city_background,
	 [("continue",[],"Continue...",[(change_screen_map),
	 #(jump_to_menu,"mnu_castle_outside"),
	 ])]
 ),
( "recover_after_death_town_alone",0,
     "You regain your conciousness and find yourself at the town outskirts. \
  You are alive!\
  Nobody is around and you take your chance to drag yourself outside the town.\
 Your companions found you.\
 It seems that none of your wounds were lethal,\
  and although you feel awful, you can still walk.",
     "none",code_to_set_city_background,[      
	 ("continue",[],"Continue...",
        [   (change_screen_map),
            #(jump_to_menu,"mnu_castle_outside"),
         ]),
	 ]
 ),

( "notification_center_under_siege",0,
    "{s1} has been besieged by {s2} of {s3}!",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (str_store_troop_name, s2, "$g_notification_menu_var2"),
      (store_troop_faction, ":troop_faction", "$g_notification_menu_var2"),
      (str_store_faction_name, s3, ":troop_faction"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 62),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_center_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),  
( "notification_one_side_left",0,
    "^^^^^The War of the Ring is over!^^The {s1} have defeated all their enemies and stand victorious!",
    "none",
    # $g_notification_menu_var1 - faction_side_*
    [ (assign, ":side", "$g_notification_menu_var1"),
      (try_begin),
        (eq, ":side", faction_side_good),
        (assign, ":faction", "fac_gondor"),
        (str_store_string, s1, "@Forces of Good"),
      (else_try),
        (eq, ":side", faction_side_eye),
        (assign, ":faction", "fac_mordor"),
        (str_store_string, s1, "@Forces of Mordor"),
      (else_try),
        #(eq, ":side", faction_side_hand),
        (assign, ":faction", "fac_isengard"),
        (str_store_string, s1, "@Forces of Isengard"),
      (try_end),
      
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":faction", pos0),
    ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),
( "notification_total_defeat",0,
    "^^^^^The War of the Ring is over for you!^^The {s1} have been defeated by their enemies and you stand alone in defeat!",
    "none",
    # $g_notification_menu_var1 - faction_side_*
    [ (assign, ":side", "$g_notification_menu_var1"),
      
      (try_begin),
        (eq, ":side", faction_side_good),
        (assign, ":faction", "fac_gondor"),
        (str_store_string, s1, "@Forces of Good"),
      (else_try),
        (eq, ":side", faction_side_eye),
        (assign, ":faction", "fac_mordor"),
        (str_store_string, s1, "@Forces of Mordor"),
      (else_try),
        #(eq, ":side", faction_side_hand),
        (assign, ":faction", "fac_isengard"),
        (str_store_string, s1, "@Forces of Isengard"),
      (try_end),
      
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":faction", pos0),
    ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),
( "notification_your_faction_collapsed",0,
    "^^^^^Your {s11} homeland was defeated!^Still, other allies remain in the War. You, together with anyone left from {s11}, can still help your side win.",
    "none",
    [ (str_store_faction_name, s11, "$players_kingdom"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$players_kingdom", pos0),
    ],
    [("continue",[],"Continue...", [(change_screen_return)])]
 ),
( "notification_faction_defeated",0,
    "^^^^^{s1} Defeated!^{s1} is no more, defeated by the forces of {s13}!",
    "none",
    [ (str_store_faction_name, s1, "$g_notification_menu_var1"),
    
      (assign, ":num_theater_enemies", 0),
      (str_store_string, s13, "@their enemies"), #defensive
      (faction_get_slot, ":faction_theater", "$g_notification_menu_var1", slot_faction_home_theater),
      (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (store_relation, ":cur_relation", ":cur_faction", "$g_notification_menu_var1"),
        (lt, ":cur_relation", 0),
        (faction_slot_eq, ":cur_faction", slot_faction_home_theater, ":faction_theater"),
        (try_begin),
          (eq, ":num_theater_enemies", 0),
          (str_store_faction_name, s13, ":cur_faction"),
        (else_try),
          (eq, ":num_theater_enemies", 1),
          (str_store_faction_name, s11, ":cur_faction"),
          (str_store_string, s13, "@{s11} and {s13}"),
        (else_try),
          (str_store_faction_name, s11, ":cur_faction"),
          (str_store_string, s13, "@{s11}, {s13}"),
        (try_end),
        (val_add, ":num_theater_enemies", 1),
      (try_end),
      
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      # (try_begin),
        # (is_between, "$g_notification_menu_var1", "fac_gondor", kingdoms_end), #Excluding player kingdom
        # (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      # (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      # (try_end),
      ],
    [("continue",[],"Continue...",[(change_screen_return)])]
 ),

( "ruins", 0,
    "^^^^You approach the {s1}. A once strong encampment was razed to the ground, though you can still see traces of fortifications and scattered rusty weapons.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
     (str_store_party_name, s1, "$g_encountered_party"),
    ],
    [("leave",[],"Leave.",[(change_screen_return)])]
 ),
( "legendary_place",0,
    "^^^^You have followed the rumors and found {s1}. You can now explore this place and see for yourself if the rumors are true.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window"),
     (str_store_party_name, s1, "$g_encountered_party"),
    ],
    [("explore",[],"Explore this place.",
       [(set_jump_mission, "mt_legendary_place_visit"),
        (try_begin),
          (eq, "$g_encountered_party", "p_legend_amonhen"),
          (assign, ":lp_scene", "scn_amon_hen"),
		  (assign, "$bs_day_sound", "snd_wind_ambiance"),
		  (assign, "$bs_night_sound", "snd_night_ambiance"),
        (else_try),
          (eq, "$g_encountered_party", "p_legend_deadmarshes"),
          (assign, ":lp_scene", "scn_deadmarshes"),
		  (assign, "$bs_day_sound", "snd_deadmarshes_ambiance"),
		  (assign, "$bs_night_sound", "snd_deadmarshes_ambiance"),
        (else_try),
          (eq, "$g_encountered_party", "p_legend_mirkwood"),
          (assign, ":lp_scene", "scn_mirkwood"),
		  (assign, "$bs_day_sound", "snd_evilforest_ambiance"),
		  (assign, "$bs_night_sound", "snd_night_ambiance"),
        (else_try),
          #(eq, "$g_encountered_party", "p_legend_fangorn"),
          (assign, ":lp_scene", "scn_fangorn"),
		  (assign, "$bs_day_sound", "snd_fangorn_ambiance"),
		  (assign, "$bs_night_sound", "snd_night_ambiance"),
        (try_end),
        (modify_visitors_at_site,":lp_scene"),
        (reset_visitors),
        (set_visitor, 1, "trp_player"),
        (jump_to_menu, "mnu_legendary_place"),
        (jump_to_scene,":lp_scene"),
        (change_screen_mission),
       ]),
     ("leave",[],"Leave.",[(change_screen_return)]),
    ]
 ),

##Ring Hunters - Bandit Lair - Start (Kham)

("ring_hunter_lair",0,
    "^^^^You have followed the trail of the Ring Hunters through Mirkwood Forest and have arrived at the {s1}. You see them getting ready to leave with a chest.",
    "none",
    [(set_background_mesh, "mesh_draw_ring_hunters_lair"), 
     (str_store_party_name, s1, "$g_encountered_party")],
    [("attack_lair",[],"Attack them now",
       [(set_jump_mission, "mt_bandit_lair"),
        (try_begin),
			(eq, "$g_encountered_party", "p_ring_hunter_lair"),
			(assign, ":lp_scene", "scn_lair_forest_bandits"),
			#(assign, "$bs_night_sound", "snd_night_ambiance"),
		(try_end),
		(modify_visitors_at_site,":lp_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 1, "trp_ring_hunter_lt"),
        (set_visitors, 2, "trp_ring_hunter_one",2),
        (set_visitors, 3, "trp_ring_hunter_one",2),
        (set_visitors, 4, "trp_ring_hunter_two",2),
        (set_visitors, 5, "trp_ring_hunter_two",2),
        (set_visitors, 6, "trp_ring_hunter_three",3),
        (set_visitors, 7, "trp_ring_hunter_three",2),
        (set_visitors, 8, "trp_ring_hunter_four",3),
        (set_visitors, 9, "trp_ring_hunter_four",2),
        (jump_to_menu, "mnu_ring_hunter_lair"),
        (jump_to_scene,":lp_scene"),
        (change_screen_mission),
       ]),
     ("leave_bandit_lair",[],"Leave for now.",[(change_screen_return)]),
	]
),

( "ring_hunter_lair_destroyed",0,"null","none",
    [(call_script, "script_setup_troop_meeting","trp_ring_hunter_lt", 255),
     #(encounter_attack),
    # (change_screen_return),
	],[]
 ),

###Ring Hunters - Bandit Lair - End

## Kham - Spears of Bladorthin - Raft Men - Start

("raftmen",0,
    "^^^^You follow the River Running southeast towards Rhûn, hoping to find the old merchant road.^^ After some time, you arrive at a small village nestled along the riverbank.^^You ask the villagers how you might reach the road and are directed towards a pair of men who navigate the river by raft.^^It takes some negotiating but you arrange for the men to bring you downriver.",
    "none",
    [(set_background_mesh, "mesh_town_goodcamp"), 
    ],
    [("go_with_the_raftmen",[],"Take the raft to Dorwinion",
       [(jump_to_menu, "mnu_ride_to_dorwinion"),
       ]),
     ("leave_bandit_lair",[],"Leave for now.",[(change_screen_return)]),
	]
),

("ride_to_dorwinion",0,
    "^^^^You relax and enjoy the fair weather as the men steer the raft downriver. The River Running, cold and clear amidst the falls and rapids of the Lonely Mountain, here is tepid, gentle, and muddy.^^ In the afternoon sun, you watch rolling plains and verdant woodlands drift by as the raft floats along the winding meanders. The region is sparsely dotted with small farmsteads and vineyards with low stone walls and you pass the occasional stilted cottage tucked away in the reeds.^^The peaceful motion of the raft helps you drift off to sleep...",
    "none",
    [(set_background_mesh, "mesh_town_goodcamp"), 
    ],
    [("ride_to_dorwinion_next",[],"Next...",
       [(jump_to_menu, "mnu_amath_dollen_fortress"),
       ]),
	]
),

### Amath Dollen Fortress Entry Points
### 0, 1 player
### 2 bandit captain
### 3-13 archer guards
### 14-23 infantry guards
### 24-28 walkers

("amath_dollen_fortress",0,
    "^^^^You awake from your nap late in the afternoon and shortly reach a jetty where the men moor the raft. They direct you to a narrow track that disappears into the marsh grass and set up camp to await your return.^^You follow the track, which ascends quickly from the wetlands onto a grassy plain, and walk until it meets the old merchant road.^^After some time, you see a bandit fortress.",
    "none",
    [(set_background_mesh, "mesh_town_evilcamp"), 
    ],
    [("bandit_fortress_with_companions",[],"Approach the Bandit Fortress with only your companions and attempt to talk with their leader.",
       [(set_jump_mission, "mt_amath_dollen_peace"),
				(eq, "$g_encountered_party", "p_raft"),
				(assign, ":lp_scene", "scn_black_shield_fortress"),
				#(assign, "$bs_day_sound", "snd_"),
				#(assign, "$bs_night_sound", "snd_"),
				(modify_visitors_at_site,":lp_scene"),
		    (reset_visitors),
		    (set_visitor, 0, "trp_player"),
		    (set_visitor, 2, "trp_black_shield"),
		    (assign, ":cur_entry", 3),
				(try_for_range, ":unused", 0, 11),
					(set_visitor, ":cur_entry", "trp_black_shield_scout"),
					(val_add, ":cur_entry", 1),
				(try_end),
				(assign, ":cur_entry", 14),
				(try_for_range, ":unused", 0, 10),
					(set_visitor, ":cur_entry", "trp_black_shield_bandit"),
					(val_add, ":cur_entry", 1),
				(try_end),
        (set_visitor, 24, "trp_black_shield_bandit"),
        (set_visitor, 25, "trp_black_shield_bandit"),
        (set_visitor, 26, "trp_black_shield_guard"),
        (set_visitor, 27, "trp_black_shield_guard"),
        (set_visitor, 28, "trp_black_shield_guard"),
        (jump_to_menu, "mnu_amath_dollen_fortress"),
        (jump_to_scene,":lp_scene"),
        (change_screen_mission),
       ]),

# Siege by player: 0 player
# 1-15 team_0 infantry/archers
# 16-18 team_1 infantry
# 19-31 team_1 archers (best 2 each)
 
     ("bandit_fortress_with_army",[],"Attack the bandit fortress with all your men.",
       [(eq, "$g_encountered_party", "p_raft"),
			(assign, ":lp_scene", "scn_black_shield_fortress_siege_player"),
			#(assign, "$bs_day_sound", "snd_"),
			#(assign, "$bs_night_sound", "snd_"),
			(modify_visitors_at_site,":lp_scene"),
	        (reset_visitors),
	        (set_jump_entry, 0),
	        (set_visitor, 0, "trp_player"),
	        (store_character_level, ":level", "trp_player"),
			(val_div, ":level", 4),
			(store_add, ":min_guards", ":level", 1),
			(store_add, ":max_guards", ":min_guards", 5),
	        (store_random_in_range, ":random_no", ":min_guards", ":max_guards"),
	        (val_clamp, ":random_no", 1, 71),
	        (store_random_in_range, ":watchtower", 1, 3),
	        (set_visitors, 16, "trp_black_shield_bandit",":random_no"),
	        (set_visitors, 17, "trp_black_shield_bandit",":random_no"),
	        (set_visitors, 18, "trp_black_shield_guard", ":random_no"),
			(set_visitors, 19, "trp_black_shield_scout", ":watchtower"),
			(set_visitors, 20, "trp_black_shield_scout", ":watchtower"),
			(set_visitors, 21, "trp_black_shield_scout", ":watchtower"),
			(set_visitors, 22, "trp_black_shield_scout", ":watchtower"),
			(set_visitors, 23, "trp_black_shield_scout", ":watchtower"),
			(set_visitors, 24, "trp_black_shield_scout", ":watchtower"),
			(set_visitors, 25, "trp_black_shield_scout", ":watchtower"),
			(set_visitors, 26, "trp_black_shield_scout", ":watchtower"),
			(set_visitors, 27, "trp_black_shield_scout", ":watchtower"),
			(set_visitors, 28, "trp_black_shield_scout", ":watchtower"),
			(set_visitors, 29, "trp_black_shield_scout", ":watchtower"),
			(set_visitors, 30, "trp_black_shield_scout", ":watchtower"),
			(set_party_battle_mode),
	      (set_battle_advantage, 0),
	      (assign, "$g_battle_result", 0),
	      (set_jump_mission, "mt_amath_dollen_attack"),
        (jump_to_scene,":lp_scene"),
        (change_screen_mission),
       ]),

# Siege by Easterlings: 0 player
# 1,2 team_0 infantry
# 3-15 team_0 archers (1 or 2 each)
# 16-31 team_1 infantry

      ("bandit_fortress_against_easterlings",[],"Defend the Fortress against the Siege",
       [(eq, "$g_encountered_party", "p_raft"),
		(assign, ":lp_scene", "scn_black_shield_fortress_siege_easterlings"),
		#(assign, "$bs_day_sound", "snd_"),
		#(assign, "$bs_night_sound", "snd_"),
		(modify_visitors_at_site,"scn_black_shield_fortress_siege_easterlings"),
        (reset_visitors),
        (set_jump_entry, 0),
        (store_character_level, ":level", "trp_player"),
		(val_div, ":level", 4),
		(store_add, ":min_guards", ":level", 2),
		(store_add, ":max_guards", ":min_guards", 4),
	    (store_random_in_range, ":random_no", ":min_guards", ":max_guards"),
	    (store_div, ":low", ":random_no",2),
	    (store_div, ":mid", ":random_no",4),
	    (store_div, ":high",":random_no",6),
      	(assign, ":cur_entry", 16),
				(try_for_range, ":unused", 0, 5),
					(set_visitors, ":cur_entry", "trp_i2_rhun_tribal_warrior",":low"),
					(val_add, ":cur_entry", 1),
				(try_end),
				(assign, ":cur_entry", 21),
				(try_for_range, ":unused", 0, 5),
					(set_visitors, ":cur_entry", "trp_i4_rhun_vet_infantry",":low"),
					(val_add, ":cur_entry", 1),
				(try_end),
				(assign, ":cur_entry", 26),
				(try_for_range, ":unused", 0, 3),
					(set_visitors, ":cur_entry", "trp_i5_rhun_ox_warrior",":mid"),
					(val_add, ":cur_entry", 1),
				(try_end),
				(assign, ":cur_entry", 29),
				(try_for_range, ":unused", 0, 3),
					(set_visitors, ":cur_entry", "trp_c6_rhun_warlord", ":high"),
					(val_add, ":cur_entry", 1),
				(try_end),
	      (set_battle_advantage, 0),
	      (assign, "$g_battle_result", 0),
	      (set_jump_mission, "mt_amath_dollen_defend"),
        (jump_to_scene,":lp_scene"),
        (change_screen_mission),
       ]),

		("bandit_fortress_spirits",[(is_currently_night)],"Go talk with the spirits.",
       [(set_jump_mission, "mt_amath_dollen_spirit"),
				(eq, "$g_encountered_party", "p_raft"),
				(assign, ":lp_scene", "scn_black_shield_fortress"),
				(modify_visitors_at_site,":lp_scene"),
		    (reset_visitors),
		    (set_jump_entry, 1),
		    (set_visitor, 1, "trp_player"),
		    (assign, ":cur_entry", 3),
				(try_for_range, ":unused", 0, 10),
					(set_visitor, ":cur_entry", "trp_black_shield_scout"),
					(val_add, ":cur_entry", 1),
				(try_end),
				(assign, ":cur_entry", 14),
				(try_for_range, ":unused", 0, 10),
					(set_visitor, ":cur_entry", "trp_black_shield_bandit"),
					(val_add, ":cur_entry", 1),
				(try_end),
        (set_visitor, 29, "trp_dorwinion_spirit_leader"),
        (set_visitors, 30, "trp_dorwinion_spirit",2),
        (set_visitors, 31, "trp_dorwinion_spirit",2),
        (jump_to_menu, "mnu_amath_dollen_fortress"),
        (jump_to_scene,":lp_scene"),
        (change_screen_mission),
       ]),

	 ("formations_test" ,[],"Formations Test",
		[(assign, "$g_custom_battle_scenario", 98),(jump_to_menu, "mnu_custom_battle_2"),]),

     ("leave_amath_dollen_fortress",[],"Leave for now.",[(change_screen_return)]),
	]
),
	
## Kham - Spears of bladorthin - Raft Men - End


## Kham - Gondor Reinforcement Event Menu - Start

("gondor_reinforcement_event",0,
   "^^^^^The beacons of Gondor are lit, Minas Tirith calls for aid!^^The lords of the southern fiefs will now march north to defend the White City against the coming darkness.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "fac_gondor", pos0)],
   	[("gondor_reinforcement_event_close", [], "Close", [(change_screen_return)]),
   	
]),

## Kham - Gondor Reinforcement Event Menu - END
## Kham - Gondor Beacons Menu - Start

("gondor_beacons",0,
   "You look up at {s1}, one of the warning beacons of Gondor, used to raise the alarm in northern and southern Gondor.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (str_store_party_name, s1, "$g_encountered_party"),
    ],
   	[("gondor_beacons_close", [], "Leave...", [(change_screen_return)]),
   	
]),

## Kham - Gondor Beacons Menu - END
## Kham - Player Added to War Council Start

("player_added_to_war_council",0,
   "^^^^^A messenger arrived and has told you that now, as {s24}, {s2} has asked you to be part of his War Council. You can now suggest strategies that can influence the course of this war.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
    	(try_for_range, ":faction_wc", kingdoms_begin, kingdoms_end),
    		(faction_slot_eq, ":faction_wc", slot_faction_war_council, 1),
        	(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":faction_wc", pos0),
			(call_script, "script_get_rank_title_to_s24", ":faction_wc"),
			(faction_get_slot, ":fac_marshall", ":faction_wc", slot_faction_marshall), 
			(str_store_troop_name, s2, ":fac_marshall"),
        (try_end)
    ],

   	[("player_added_to_war_council_close", [], "Close", [(change_screen_return)]),

]),

## Kham - Player Added to War Council END
## Kham - Player Added to Siege Reports

("player_added_to_siege_reports",0,
   "^^^^^A messenger arrived and has told you that now, as {s24}, you will be receiving reports whenever {s2} besieges a center or when {s2}'s centers are sieged.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
    	(try_for_range, ":faction_wc", kingdoms_begin, kingdoms_end),
    		(faction_slot_eq, ":faction_wc", slot_faction_siege_reports, 1),
        	(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":faction_wc", pos0),
			(call_script, "script_get_rank_title_to_s24", ":faction_wc"),
			(str_store_faction_name, s2, ":faction_wc"),
        (try_end)
    ],

   	[("player_added_to_siege_reports_close", [], "Close", [(change_screen_return)]),

]),

## Kham - Player Added to Siege Reports END

## Kham - Player Added to Allow Party Follow

("player_added_to_allow_follow",0,
   "^^^^^A messenger arrived and has told you that now, as {s24}, you will be allowed to command {s2} to follow you, for a total of {reg55} maximum followers.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
    	(try_for_range, ":faction_wc", kingdoms_begin, kingdoms_end),
    		(faction_get_slot, ":faction_follow", ":faction_wc", slot_faction_allowed_follow),
    		(faction_get_slot, ":faction_side", ":faction_wc", slot_faction_side),
    		(str_store_faction_name, s3, ":faction_wc"),
    		(try_begin),
    			(eq, ":faction_follow", 1),
    			(str_store_string, s2, "@a scout party from {s3}"),
    			(assign, reg55, 1),
        		(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":faction_wc", pos0),
				(call_script, "script_get_rank_title_to_s24", ":faction_wc"),
    		(else_try),
    			(eq, ":faction_follow", 2),
    			(eq, ":faction_side", faction_side_good),
    			(str_store_string, s2, "@two scout parties and a forager party from {s3}"),
    			(assign, reg55, 3),
        		(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":faction_wc", pos0),
				(call_script, "script_get_rank_title_to_s24", ":faction_wc"),
    		(else_try),
    			(eq, ":faction_follow", 2),
    			(neq, ":faction_side", faction_side_good),
    			(str_store_string, s2, "@two scout parties and a raider party from {s3}"),
    			(assign, reg55, 3),
        		(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":faction_wc", pos0),
				(call_script, "script_get_rank_title_to_s24", ":faction_wc"),
    		(else_try),
    			(eq, ":faction_follow", 3),
    			(eq, ":faction_side", faction_side_good),
    			(str_store_string, s2, "@three scouts, two foragers, and a patrol from {s3}"),
    			(assign, reg55, 4),
        		(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":faction_wc", pos0),
				(call_script, "script_get_rank_title_to_s24", ":faction_wc"),
    		(else_try),
    			(eq, ":faction_follow", 3),
    			(neq, ":faction_side", faction_side_good),
    			(str_store_string, s2, "@three scouts, two raiders, and a war party from {s3}"),
    			(assign, reg55, 4),
        		(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":faction_wc", pos0),
				(call_script, "script_get_rank_title_to_s24", ":faction_wc"),
    		(try_end),
        (try_end)
    ],

   	[("player_added_to_allow_follow_close", [], "Close", [(change_screen_return)]),

]),

## Kham - Player Added to Allow Party Follow END

## Kham - Center Besieged Menu - Start

("center_besieged_event",0,
   "^^^^^A messenger arrived reporting that {s1} has been besieged by {s2} of {s3}.",
    "none",
    [   
    	(str_store_party_name, s1, "$besieged_center_for_menu"),
    	(str_store_faction_name, s3, "$besieged_by_faction_for_menu"),
    	(str_store_troop_name, s2, "$besieged_by_troop_for_menu"),
		(party_get_slot,":mesh","$besieged_center_for_menu",slot_town_menu_background),
		(set_background_mesh, ":mesh"),
		(set_fixed_point_multiplier, 100),
		(position_set_x, pos0, 65),
		(position_set_y, pos0, 30),
		(position_set_z, pos0, 100),
		(set_game_menu_tableau_mesh, "tableau_troop_note_mesh", "$besieged_by_troop_for_menu", pos0)],
   	[("center_besieged_event_close", [], "Close", [(change_screen_return)]),
   	
]),

## Kham - Center Besieged Menu - END

## Kham - Guardian Party Spawned - Start

("guardian_party_spawned",0,
   "^^^^^Scouts report that {s6} gathered a large army in the vicinity of {s7}, in a last ditch attempt to defend the capital.",
    "none",
    [   (set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
    	(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", reg70, pos0),

    ],

   	[("guardian_party_spawned_close", [], "Close", [(change_screen_return)]),

]),

## Kham - Guardian Party Spawned - END

( "auto_return_to_map",0,"stub","none",[(change_screen_map)],[]),
#MV: hackery to get around change_screen_exchange_with_party limitations
( "auto_player_garrison",0,"stub","none",
    [(jump_to_menu, "mnu_auto_player_garrison_2"),
     (try_begin),
     	(is_between, "$g_encountered_party", "p_advcamp_gondor", "p_centers_end"),
        (troop_get_slot, ":reserve_party", "trp_player", slot_troop_player_reserve_adv_camp),
     (else_try),
     	(troop_get_slot, ":reserve_party", "trp_player", slot_troop_player_reserve_party),
     (try_end),
     (change_screen_exchange_with_party, ":reserve_party")
    ],
    []
 ),
( "auto_player_garrison_2",0,"stub","none",
    [(jump_to_menu, "mnu_town"),
     
     (set_jump_mission,"mt_conversation_encounter"),
     (modify_visitors_at_site,"scn_conversation_scene"),(reset_visitors),
     (set_visitor,0,"trp_player"),
     (call_script, "script_get_party_max_ranking_slot", "$g_encountered_party"),
     (party_stack_get_troop_id, reg(6),"$g_encountered_party",reg0),
     (party_stack_get_troop_dna,reg(7),"$g_encountered_party",reg0),
     (set_visitor,17,reg(6),reg(7)),
     (jump_to_scene,"scn_conversation_scene"),
     (assign, "$talk_context", tc_hire_troops),
     (change_screen_map_conversation, reg(6)),
    ],
    []
 ),

( "auto_town_brawl",0,"stub","none",
    [
     (party_get_slot, ":town_scene", "$current_town", slot_town_center),
     (modify_visitors_at_site, ":town_scene"),
     (reset_visitors),
     (call_script, "script_init_town_walkers"),
     (set_jump_mission,"mt_town_brawl"),
     (jump_to_scene, ":town_scene"),
     (change_screen_mission),
    ],
    []
 ),
( "auto_intro_rohan",0,"stub","none",
    [
     (set_jump_mission,"mt_intro_rohan"),
     (assign, "$current_town", "p_town_edoras"),
     (modify_visitors_at_site,"scn_westfold_center"),
     (reset_visitors,0),
     (set_visitor, 1, "trp_player"), #needed
     (jump_to_scene,"scn_westfold_center"),
     (change_screen_mission),
    ],
    []
 ),
( "auto_intro_gondor",0,"stub","none",
    [
       (set_jump_mission, "mt_intro_gondor"),
       (assign, "$current_town", "p_town_minas_tirith"), #for the cabbage guards 
       (modify_visitors_at_site, "scn_minas_tirith_center"),
       (reset_visitors),
       (set_visitor, 1, "trp_player"),
       (jump_to_scene, "scn_minas_tirith_center"),
       (change_screen_mission),
    ],
    []
 ),
( "auto_intro_mordor",0,"stub","none",
    [
       (set_jump_mission, "mt_intro_mordor"),
       (assign, "$current_town", "p_town_minas_morgul"), #for the cabbage guards 
       (modify_visitors_at_site, "scn_minas_morgul_center"),
       (reset_visitors),
       (set_visitor, 1, "trp_player"),
       (jump_to_scene, "scn_minas_morgul_center"),
       (change_screen_mission),
    ],
    []
 ),
( "auto_intro_joke",0,"stub","none",
    [
       (set_jump_mission, "mt_intro_joke"),
       (modify_visitors_at_site, "scn_minas_tirith_castle"),
       (reset_visitors),
       (set_visitor, 1, "trp_player"),
       (jump_to_scene, "scn_minas_tirith_castle"),
       (change_screen_mission),
    ],
    []
 ),
( "auto_convo",0,"stub","none",
    [
       (set_jump_mission, "mt_test_gandalf"),
       (modify_visitors_at_site, "scn_conversation_scene"),
       (reset_visitors),
       (set_visitor, 0, "trp_player"),
       (set_visitor, 1, "$g_tld_convo_talker"),
       (jump_to_scene, "scn_conversation_scene"),
       (change_screen_mission),
    ],
    []
 ),
( "auto_conversation_cutscene",0,"stub","none",
    [
       (set_jump_mission, "mt_conversation_cutscene"),
       (modify_visitors_at_site, "scn_conversation_scene"),
       (reset_visitors),
       (set_visitor, 0, "trp_player"),
       (set_visitor, 1, "$g_tld_convo_talker"),
       (jump_to_scene, "scn_conversation_scene"),
       (change_screen_mission),
    ],
    []
 ),
 
###################### starting quest, GA (replaced by Unified Start Quest - Kham) ##############################  
#( "starting_quest_good",0,
#   "^^^^^^You spot a small caravan under attack from a band of orcs. What will you do?",
#   "none",[],
#   [("help",[], "Help the strangers!",
#     [
#     (set_jump_mission,"mt_tld_caravan_help"),
#     (modify_visitors_at_site,"scn_starting_quest"),
#      (reset_visitors),
#      (set_visitor,0,"trp_player"),
#      (set_visitors,7,"trp_brigand", 3),
#      (set_visitors,8,"trp_brigand", 3),
#      (set_visitors,9,"trp_start_quest_caravaneer", 1),
#      (set_visitors,17,"trp_tribal_orc", 8),
#      (set_visitors,18,"trp_mountain_goblin", 8),
#      (set_visitors,19,"trp_i4_mordor_fell_uruk", 1),
#      (jump_to_scene,"scn_starting_quest"),
#      (set_battle_advantage, 0),
#      (assign, "$g_battle_result", 0),
#      (assign, "$g_next_menu", "mnu_starting_quest_victory"),
#      (assign, "$g_mt_mode", vba_normal),
#      (assign, "$cant_leave_encounter", 1),
      
#      (jump_to_menu, "mnu_starting_quest_victory"),
#      (change_screen_mission),
#      (assign,"$talk_context",tc_starting_quest),
#     (call_script, "script_setup_troop_meeting","trp_start_quest_caravaneer", 255),
#      ]),
#   ("go_your_way",[],"Leave them alone",[(change_screen_map),]),
# ]),
#( "starting_quest_victory",0,"null","none",
#    [(call_script, "script_setup_troop_meeting","trp_start_quest_caravaneer", 255),
#     (leave_encounter),
#     (change_screen_return),
#	],[]
# ),


###################### Unified Starting Quests (Kham) ############################## 

("faction_intro_menu",0,
	"{s5}",
	"none", [
	(call_script, "script_get_intro_text", "$players_kingdom"),
	(faction_get_slot, ":capital", "$players_kingdom", slot_faction_capital),
	(party_get_slot,":mesh",":capital",slot_town_menu_background),
  	(set_background_mesh, ":mesh"),], 
	[("intro_next", [], "Continue...", [(jump_to_menu, "mnu_unified_start_quest"),])]),


( "unified_start_quest",0,
	"{s10}",
	"none",[
		(try_begin),
			(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
			(set_background_mesh, "mesh_town_goodcamp"),
		(else_try),
			(set_background_mesh, "mesh_town_evilcamp"),
		(try_end)],

	[("start_defend_caravan",
		[(this_or_next|eq, "$players_kingdom", "fac_gondor"),
		 (this_or_next|eq, "$players_kingdom", "fac_dale"),
		 (this_or_next|eq, "$players_kingdom", "fac_dwarf"),
		 (             eq, "$players_kingdom", "fac_rohan")],
		"Defend the Caravan!", [
			(set_jump_mission,"mt_tld_caravan_help"),
		    (modify_visitors_at_site,"scn_starting_quest"),
		      (reset_visitors),
		      	(try_begin),
		      		(eq, "$players_kingdom", "fac_gondor"),
		      		(assign,"$assist","fac_rohan"),
		      	(else_try),
		      		(eq, "$players_kingdom", "fac_rohan"),
		      		(assign,"$assist","fac_gondor"),
		      	(else_try),
		      		(eq, "$players_kingdom", "fac_dwarf"),
		      		(assign,"$assist","fac_dale"),
		   		(else_try),
		      		(assign,"$assist","fac_dwarf"),
		      	(try_end),
		      (faction_get_slot, ":tier_1_troop", "$assist", slot_faction_tier_1_troop),
		      (faction_get_slot, ":tier_2_troop", "$assist", slot_faction_tier_2_troop),
		      (set_visitor, 0,"trp_player"),
		      (set_visitors,2,":tier_1_troop", 7),
		      (set_visitors,4,":tier_2_troop", 4),
		      (set_visitors,6,"trp_start_quest_caravaneer", 1),
		      (set_visitors,16,"trp_tribal_orc", 8),
		      (set_visitors,18,"trp_mountain_goblin", 5),
		      (set_visitors,20,"trp_i4_mordor_fell_uruk", 1),
		      (jump_to_scene,"scn_starting_quest"),
		      (set_battle_advantage, 0),
		      (assign, "$g_battle_result", 0),
		      (assign, "$g_next_menu", "mnu_starting_quest_victory_good"),
		      (assign, "$g_mt_mode", vba_normal),
		      (assign, "$cant_leave_encounter", 1),	      
		      (jump_to_menu, "mnu_starting_quest_victory_good"),
		      (change_screen_mission),

      	]),
	("start_raid_caravan",
		[(this_or_next|eq, "$players_kingdom", "fac_isengard"),
		 (this_or_next|eq, "$players_kingdom", "fac_moria"),
		 (this_or_next|eq, "$players_kingdom", "fac_gundabad"),
		 (this_or_next|eq, "$players_kingdom", "fac_mordor"),
		 (this_or_next|eq, "$players_kingdom", "fac_dunland"),
		 (this_or_next|eq, "$players_kingdom", "fac_rhun"),
		 (this_or_next|eq, "$players_kingdom", "fac_umbar"),
		 (             eq, "$players_kingdom", "fac_guldur"),],
		"Raid the Caravan!", [
			(set_jump_mission,"mt_tld_caravan_help"),
		    (modify_visitors_at_site,"scn_starting_quest"),
		      (reset_visitors),
		      	(try_begin),
		      		(this_or_next|eq, "$players_kingdom", "fac_isengard"),
		      		(			  eq, "$players_kingdom", "fac_gundabad"),
		      		(assign,"$assist","fac_moria"),
		      	(else_try),
		      		(eq,"$players_kingdom", "fac_dunland"),
		      		(assign,"$assist","fac_isengard"),
		      	(else_try),
		      		(this_or_next|eq, "$players_kingdom",   "fac_rhun"),
		      		(this_or_next|eq, "$players_kingdom",  "fac_umbar"),
		      		(			  eq, "$players_kingdom", "fac_guldur"),
		      		(assign,"$assist", "fac_mordor"),
		      	(else_try),
		      		(eq, "$players_kingdom", "fac_moria"),
		      		(assign, "$assist", "fac_gundabad"),
		      	(else_try),
		      		(eq, "$players_kingdom", "fac_mordor"), ##
		      		(assign,"$assist","fac_rhun"), 
		      	(try_end),
		      (faction_get_slot, ":tier_1_troop", "$assist", slot_faction_tier_1_troop),
		      (set_visitor,22,"trp_player"),
		      (try_begin),
			      (this_or_next|eq, "$players_kingdom", "fac_isengard"),
			      ( 			eq, "$players_kingdom",  "fac_dunland"),
			      (set_visitors,2,"trp_i3_footman_of_rohan", 3),
			      (set_visitors,4,"trp_i3_footman_of_rohan", 3),
		      (else_try),
		      	  (this_or_next|eq,"$players_kingdom", "fac_mordor"),
		      	  (				eq,"$players_kingdom", "fac_umbar"),
			      (set_visitors,2,"trp_i2_gon_watchman", 3),
			      (set_visitors,4,"trp_i2_gon_watchman", 3),
			  (else_try),
			  	  (				eq,"$players_kingdom", "fac_guldur"),
  	  			  (set_visitors,2,"trp_i2_beorning_warrior", 3),
			      (set_visitors,4,"trp_i2_beorning_warrior", 3),
			 (else_try),
			  	  (				eq,"$players_kingdom", "fac_rhun"),
  	  			  (set_visitors,2,"trp_a2_dale_scout", 3),
			      (set_visitors,4,"trp_i2_dale_man_at_arms", 3),
			 (else_try),
			  	  (this_or_next|eq,"$players_kingdom", "fac_moria"),
  			  	  (				eq,"$players_kingdom", "fac_gundabad"),
  	  			  (set_visitors,2,"trp_i2_dwarf_warrior", 2),
			      (set_visitors,4,"trp_i1_dwarf_apprentice", 3),
		      (try_end),
		      (set_visitors,6,"trp_start_quest_caravaneer", 1),
		      (set_visitors,16,":tier_1_troop", 8),
		      (set_visitors,18,":tier_1_troop", 8),
		      (set_visitors,20,"trp_start_quest_uruk", 1),
		      (set_visitors,24,"trp_start_quest_orc", 1),
		      (jump_to_scene,"scn_starting_quest"),
		      (set_battle_advantage, 0),
		      (assign, "$g_battle_result", 0),
		      (assign, "$g_next_menu", "mnu_starting_quest_victory_evil"),
		      (assign, "$g_mt_mode", vba_normal),
		      (assign, "$cant_leave_encounter", 1),
		      
		      (jump_to_menu, "mnu_starting_quest_victory_evil"),
		      (change_screen_mission),

      		]),
	("start_ambush_orcs",
		[(this_or_next|eq, "$players_kingdom", "fac_imladris"),
		 (this_or_next|eq, "$players_kingdom", 	 "fac_lorien"),
		 (this_or_next|eq, "$players_kingdom", 	"fac_woodelf"),
		 (			   eq, "$players_kingdom", 	"fac_beorn")],
		"Ambush the Orcs!", [
			(set_jump_mission,"mt_tld_start_quest_ambush"),
		    (try_begin),
		      (this_or_next|eq,"$players_kingdom","fac_woodelf"),
		      (			  eq,"$players_kingdom","fac_beorn"),
		      (modify_visitors_at_site,"scn_start_woodelf"),
		    (else_try),
		      (eq, "$players_kingdom", "fac_imladris"),
		   	  (modify_visitors_at_site,"scn_start_rivendell"),
		    (else_try),
		      (modify_visitors_at_site,"scn_start_lorien"),
		    (try_end),
		      (reset_visitors),
		      (try_begin),
		      	(eq, "$players_kingdom","fac_lorien"),
		      	(assign,"$assist", "fac_beorn"),
		      (else_try),
		      	(assign,"$assist","fac_lorien"),
		      (try_end),
		      (faction_get_slot, ":tier_1_troop", "$assist", slot_faction_tier_1_troop),
		      (faction_get_slot, ":tier_2_troop", "$assist", slot_faction_tier_2_troop),
		      (set_visitor,16,"trp_player"),
		      (try_begin),
		      	(eq,"$assist", "fac_beorn"),
		      	(set_visitors,2,":tier_1_troop", 6),
		      	(set_visitors,4,":tier_2_troop", 6),
				(set_visitors,6,"trp_start_quest_beorning", 1),
			  (else_try),    
			     (set_visitors,2,":tier_1_troop", 4),
			     (set_visitors,4,":tier_2_troop", 4),
		      	 (set_visitors,6,"trp_start_quest_woodelf", 1),
		      (try_end),
		      (set_visitors,20,"trp_tribal_orc", 13),
		      (set_visitors,22,"trp_tribal_orc_warrior", 10),
		      (set_visitors,24,"trp_i4_mordor_fell_uruk", 1),
		      (try_begin),
		        (this_or_next|eq,"$players_kingdom","fac_woodelf"),
		        (			  eq,"$players_kingdom","fac_beorn"),
		        (jump_to_scene,"scn_start_woodelf"),
		      (else_try),
		        (eq, "$players_kingdom", "fac_imladris"),
		   	    (jump_to_scene,"scn_start_rivendell"),
		      (else_try),
		        (jump_to_scene,"scn_start_lorien"),
		      (try_end),
		      (set_battle_advantage, 0),
		      (assign, "$g_battle_result", 0),
		      (assign, "$g_next_menu", "mnu_starting_quest_victory_elves"),
		      (assign, "$g_mt_mode", vba_normal),
		      (assign, "$cant_leave_encounter", 1),	      
		      (jump_to_menu, "mnu_starting_quest_victory_elves"),
		      (change_screen_mission),

      	]),

	("start_kill_scouts",
		[(this_or_next|eq, "$players_kingdom", "fac_harad"),
		 (			   eq, "$players_kingdom", 	"fac_khand")],
		"Stop the scouts from reporting your arrival!", [
			(set_jump_mission,"mt_tld_start_quest_scouts"),
		    (modify_visitors_at_site,"scn_quick_battle_ambush"),
		      (reset_visitors),
		      (try_begin),
		      	(eq,"$players_kingdom", "fac_harad"),
		      	(assign, "$assist","fac_harad"),
		      (else_try),
		      	(assign,"$assist", "fac_khand"),
		      (try_end),
		      (faction_get_slot, ":tier_2_troop", "$assist", slot_faction_tier_2_troop),
		      (faction_get_slot, ":tier_4_troop", "$assist", slot_faction_tier_4_troop),
		      (set_visitor,0,"trp_player"),
		      (set_visitors,2,":tier_4_troop", 8),
		       (set_visitors,4,":tier_2_troop", 8),
		      (set_visitor,6,"trp_start_quest_mordor_scout"),
		      (set_visitors,22,"trp_a4_ithilien_ranger", 2),
		      (set_visitors,23,"trp_a4_ithilien_ranger", 3),
		      (set_visitors,24,"trp_a5_ithilien_vet_ranger", 1),
		      (jump_to_scene,"scn_quick_battle_ambush"),
		      (set_battle_advantage, 0),
		      (assign, "$g_battle_result", 0),
		      (assign, "$g_next_menu", "mnu_starting_quest_victory_easterlings"),
		      (assign, "$g_mt_mode", vba_normal),
		      (assign, "$cant_leave_encounter", 1),	      
		      (jump_to_menu, "mnu_starting_quest_victory_easterlings"),
		      (change_screen_mission),

      	]),

		("go_your_way",[],"Leave them alone",[(change_screen_map),]),
	]),
###################### Unified Starting Quests Menu End (Kham) ############################## 
###################### Unified Starting Quests Victory Menus Start (Kham) ###################

( "starting_quest_victory_good",0,"null","none",
    [(call_script, "script_setup_troop_meeting","trp_start_quest_caravaneer", 255),
	],[]
 ),

( "starting_quest_victory_evil",0,"null","none",
    [(call_script, "script_setup_troop_meeting","trp_start_quest_uruk", 255),
	],[]
 ),

( "starting_quest_victory_evil_no_duel",0,"null","none",
    [(call_script, "script_setup_troop_meeting","trp_start_quest_orc", 255),
	],[]
 ),

( "start_quest_duel_won",0,"null","none",
    [(try_begin),
    	(lt, "$g_battle_result", 0),
    	(jump_to_menu, "mnu_recover_after_death_default"),
    (else_try),
    	(call_script, "script_setup_troop_meeting","trp_start_quest_orc", 260),
    (try_end),
	],[]
 ),

( "starting_quest_victory_elves",0,"null","none",
    [
    	(try_begin),
	    	(eq,"$players_kingdom", "fac_lorien"),
	    	(call_script, "script_setup_troop_meeting","trp_start_quest_beorning", 255),
    	(else_try),
    		(call_script, "script_setup_troop_meeting","trp_start_quest_woodelf", 255),
    	(try_end),
	],[]
 ),

( "starting_quest_victory_easterlings",0,"null","none",
    [(call_script, "script_setup_troop_meeting","trp_start_quest_mordor_scout", 255),
	],[]
 ),

###################### Evil Duel Menu Start (Kham) ########################################

("start_quest_duel",0,"null","none",
   [(try_begin),
		(modify_visitors_at_site, "scn_duel_scene"),
		(reset_visitors),
		(set_jump_entry, 0), 
		(try_begin),
      		(this_or_next|eq, "$players_kingdom", "fac_isengard"),
      		(			  eq, "$players_kingdom", "fac_gundabad"),
      		(assign,"$assist","fac_moria"),
      	(else_try),
      		(eq,"$players_kingdom", "fac_dunland"),
      		(assign,"$assist","fac_isengard"),
      	(else_try),
      		(this_or_next|eq, "$players_kingdom",   "fac_rhun"),
      		(this_or_next|eq, "$players_kingdom",  "fac_umbar"),
      		(			  eq, "$players_kingdom", "fac_guldur"),
      		(assign,"$assist", "fac_mordor"),
      	(else_try),
      		(eq, "$players_kingdom", "fac_moria"),
      		(assign, "$assist", "fac_gundabad"),
      	(else_try),
      		(eq, "$players_kingdom", "fac_mordor"), ##
      		(assign,"$assist","fac_rhun"),
		(try_end),
		(faction_get_slot, ":tier_1_troop", "$assist", slot_faction_tier_1_troop),
		(set_visitor, 0, 			"trp_player"),
		(set_visitor, 1,  "trp_start_quest_uruk"),
		(set_visitor, 2,         ":tier_1_troop"),
		(set_visitor, 4,         ":tier_1_troop"),
		(set_visitor, 6,         ":tier_1_troop"),
		(set_visitor, 8,         ":tier_1_troop"),
		(set_visitor, 10,        ":tier_1_troop"),
		(set_visitor, 12,        ":tier_1_troop"),
		(set_visitor, 14,        ":tier_1_troop"),
		(set_visitor, 16,        ":tier_1_troop"),
		(set_visitor, 18,        ":tier_1_troop"),
		(set_visitor, 20,        ":tier_1_troop"),
		(set_visitor, 21,  "trp_start_quest_orc"),
		(set_visitor, 22,        ":tier_1_troop"),
		(set_visitor, 23,        ":tier_1_troop"),
		(set_visitor, 24,        ":tier_1_troop"),
		(set_visitor, 25,        ":tier_1_troop"),
		(set_visitor, 26,        ":tier_1_troop"),
	(try_end),
		(set_jump_mission, "mt_start_quest_duel"),
		(jump_to_scene, "scn_duel_scene"),
      	(set_battle_advantage, 0),
      	(assign, "$g_battle_result", 0),
      	(assign, "$g_next_menu", "mnu_start_quest_duel_won"),
      	(assign, "$g_mt_mode", vba_normal),
      	(assign, "$cant_leave_encounter", 1),
      	(jump_to_menu, "mnu_start_quest_duel_won"),
      (change_screen_mission),
    ],[
	("leave",[],"Leave.",[(change_screen_map)])]
 ),

###################### Evil Duel Menu End (Kham) ##########################################
###################### Unified Starting Quests Victory Menus End (Kham) ###################


###################### Defend / Raid Village Quest Start (Kham) ##########################################
	
	("village_quest",0,
	   "{s9}.",
	   "none",[

	 #Check which quest (Evil / Good)
	   (try_begin),
	   	(check_quest_active,"qst_defend_village"),
	   	(set_background_mesh, "mesh_town_goodcamp"),
	   	(str_store_string,s9,"@You see the village being raided by bandits. You ask most of your troops to watch out for other raiders while you take a small group and prepare to defend villagers."),
	   (else_try),
	    (set_background_mesh,"mesh_town_evilcamp"),
	    (str_store_string,s9,"@You see the village you were tasked to raid. You and a small group of your raiders prepare to attack the village so as not to be seen."),
	   (try_end)],

	 #If Good (Defend Village)
	 [("defend_villagers",[(check_quest_active,"qst_defend_village")], "Defend the Villagers!",
	     [  
	     	(quest_get_slot, ":quest_object_faction","qst_defend_village", slot_quest_object_faction),
	  
	 #Randomize Raiders
	        (store_random_in_range, ":random_no", 0, 2),
	        (try_begin),
	          (eq, ":quest_object_faction","fac_gondor"),
				(try_begin),				
					(eq, ":random_no", 0),
					(assign, ":bandit_troop_1", "trp_i2_corsair_warrior"),
					(assign, ":bandit_troop_2", "trp_a2_corsair_marine"),
				(else_try),						
					(assign, ":bandit_troop_1", "trp_i3_isen_large_orc_despoiler"),
					(assign, ":bandit_troop_2", "trp_ac2_isen_wolf_rider"),	
				(try_end),
	        (else_try),
	          (eq, ":quest_object_faction","fac_rohan"),
			  	(try_begin),				
					(eq, ":random_no", 0),
					(assign, ":bandit_troop_1", "trp_i1_dun_wildman"),
					(assign, ":bandit_troop_2", "trp_ac4_dun_crebain_rider"),
				(else_try),						
					(assign, ":bandit_troop_1", "trp_i3_mordor_large_orc"),
					(assign, ":bandit_troop_2", "trp_c3_mordor_warg_rider"),	
				(try_end),
	        (else_try),

	          (this_or_next|eq, ":quest_object_faction", "fac_dwarf"),
	          (			    eq, ":quest_object_faction", "fac_dale"),
				(try_begin),
					(eq, ":random_no", 0),
					(assign, ":bandit_troop_1", "trp_i2_rhun_tribal_warrior"),
					(assign, ":bandit_troop_2", "trp_ac2_rhun_horse_scout"),
				(else_try),						
					(assign, ":bandit_troop_1", "trp_i3_mordor_large_orc"),
					(assign, ":bandit_troop_2", "trp_c3_mordor_warg_rider"),	
				(try_end),
		    (else_try),
	          (eq, ":quest_object_faction","fac_beorn"),
				(try_begin),
				  (eq, ":random_no", 0),
					(assign, ":bandit_troop_1", "trp_i4_gunda_orc_warrior"),
					(assign, ":bandit_troop_2", "trp_c4_gunda_warg_rider"),
				(else_try),
					(assign, ":bandit_troop_1", "trp_i3_moria_large_goblin"),
					(assign, ":bandit_troop_2", "trp_c3_moria_wolf_rider"),
				(try_end),
			(else_try),
				(assign, ":bandit_troop_1", "trp_i3_mordor_large_orc"),
				(assign, ":bandit_troop_2", "trp_c3_mordor_warg_rider"),					
	        (try_end),

		#Set Which Scene Village is at
	 	## Get Region of Village
		 	(try_begin),
			 	(is_between, "$current_player_region", region_harrowdale, region_misty_mountains),
				(store_random_in_range, ":random_scene", 1, 3),
				(try_begin),
				(eq, ":random_scene",1),
					(assign, ":village_scene", "scn_village_rohan"),
				(else_try),
					(assign, ":village_scene", "scn_village_rohan_2"),
				(try_end),
			(else_try),
				(is_between, "$current_player_region", region_pelennor, region_harrowdale),
				(assign, ":village_scene", "scn_village_gondor"),
			(else_try),
				(is_between, "$current_player_region", region_misty_mountains, region_above_mirkwook),
				(assign, ":village_scene", "scn_village_anduin"),
			(else_try), #InVain - just use the northern village as default
				(assign, ":village_scene", "scn_village_north"),
		    (try_end),

	 #Set Entry and Number of Enemies / Villagers
	        (reset_visitors),
	        (modify_visitors_at_site, ":village_scene"),
	        (store_character_level, ":level", "trp_player"),
	        #(val_div, ":level", 2),
	        #(store_add, ":min_bandits", ":level", 18),
	        (store_mul, ":min_bandits", ":level", 3), #InVain - nerf attacker numbers and scale them better to the player's level (might be too easy now, we'll see)
			(val_div, ":min_bandits", 2),
	        (store_add, ":max_bandits", ":min_bandits", ":level"), #InVain - make range of max attackers scale on player level, too
			(val_min, ":min_bandits", 40),
	        (store_random_in_range, ":random_no", ":min_bandits", ":max_bandits"),
	        (set_jump_entry, 0), 
	        (set_visitor, 0, "trp_player"),
	        (gt, ":bandit_troop_1", 0),
	        (set_visitors, 16, ":bandit_troop_1", ":random_no"),
	        (set_visitors, 10, "trp_farmer", 8),
	        (set_visitors, 11, "trp_peasant_woman", 8),
	        (val_div,":random_no",4),
	        (set_visitors, 18, ":bandit_troop_2", ":random_no"),
	        (set_party_battle_mode),
	        (set_battle_advantage, 0),
	        (assign, "$g_battle_result", 0),
	        (set_jump_mission,"mt_village_attack_bandits"),
	       	(jump_to_scene, ":village_scene"),
	        (change_screen_mission),
	       ]),

	 #If Evil (Raid Village)

	 ("raid_villagers",[(check_quest_active,"qst_raid_village")], "Raid the Village!",
	     [  
	     	(quest_get_slot, ":raid_village_faction", "qst_raid_village", slot_quest_target_faction),
	     	
	 #Set Village Defender Faction
	     	(try_begin), ## Elves are not likely to be guarding villages. Make an exception
			    (this_or_next|eq,":raid_village_faction", "fac_imladris"),
			    (this_or_next|eq,":raid_village_faction", "fac_lorien"),
			    (this_or_next|eq,":raid_village_faction", "fac_woodelf"),
			    (neg|is_between, ":raid_village_faction", kingdoms_begin, kingdoms_end),  ## For some reason, the search counts 'ruins' etc. This takes them out! 
			    (assign,":raid_village_faction", "fac_beorn"), ## Beornings is the closest to areas where elves would mostly be.
	     	(try_end),
	     	(faction_get_slot, ":tier_1_troop", ":raid_village_faction", slot_faction_tier_1_troop),
	     	(faction_get_slot, ":tier_2_troop", ":raid_village_faction", slot_faction_tier_2_troop),
	        (assign, ":guard_troop_1", ":tier_1_troop"),
	        (assign, ":guard_troop_2", ":tier_2_troop"),
	        (assign, ":guard_troop_3", "trp_farmer"),
		
		#Set Which Scene Village is at
	 	## Get Region of Village
		 	(try_begin),
			 	(is_between, "$current_player_region", region_harrowdale, region_misty_mountains),
				(store_random_in_range, ":random_scene", 1, 3),
				(try_begin),
				(eq, ":random_scene",1),
					(assign, ":village_scene", "scn_village_rohan"),
				(else_try),
					(assign, ":village_scene", "scn_village_rohan_2"),
				(try_end),
			(else_try),
				(is_between, "$current_player_region", region_pelennor, region_harrowdale),
				(assign, ":village_scene", "scn_village_gondor"),
			(else_try),
				(is_between, "$current_player_region", region_misty_mountains, region_above_mirkwook),
				(assign, ":village_scene", "scn_village_anduin"),
			(else_try), #InVain - just use the northern village as default
				#(this_or_next|eq, "$current_player_region", region_above_mirkwook),
				#(			  eq, "$current_player_region", region_grey_mountains),
				(assign, ":village_scene", "scn_village_north"),
	 #Randomize Scene
	 		# (else_try),
		        # (store_random_in_range, ":random_scene", 1, 3),
		        # (try_begin),
		        	# (eq, ":random_scene",1),
		        	# (assign, ":village_scene", "scn_village_1"), ## Need new scene - Kham
		        # (else_try),
		        	# (assign, ":village_scene", "scn_village_3"),
		        # (try_end),
		    (try_end),
	
	#Set Entry and Number of Defenders   
	        (reset_visitors),
	        (modify_visitors_at_site, ":village_scene"),
	        (store_character_level, ":level", "trp_player"),
	        # (val_div, ":level", 2),
	        # (store_add, ":min_guards", ":level", 10),
			(val_div, ":level", 3),
			(store_mul, ":min_guards", ":level", 2), #InVain - nerf defender numbers and scale them better to the player's level (might be too easy now, we'll see)
	        (store_add, ":max_guards", ":min_guards", 6),
	        (store_random_in_range, ":random_no", ":min_guards", ":max_guards"),
	        (set_jump_entry, 16), 
	        (set_visitor, 16, "trp_player"),
	        (gt, ":guard_troop_1",0),
	        (set_visitors, 11, ":guard_troop_1", ":random_no"),
	        (val_div,":random_no",6),
	        (gt, ":guard_troop_2",0),
	        (set_visitors,11, ":guard_troop_2", ":random_no"),
	        (gt, ":guard_troop_3",0),
	        (set_visitors, 10, ":guard_troop_3", 6),
	        (set_party_battle_mode),
	        (set_battle_advantage, 0),
	        (assign, "$g_battle_result", 0),
	        (set_jump_mission,"mt_village_attack_farmers"),
	        (jump_to_scene, ":village_scene"),
	        (change_screen_mission),
	       ]),
	   ("go_away",[],"Leave and regroup for now.",[(change_screen_map)]),
	 ]),


("village_quest_result",mnf_scale_picture|mnf_disable_all_keys,
	    "{s9}",
	    "none",
	    [
	      (try_begin),
	      	(check_quest_active,"qst_defend_village"),
	        (eq, "$g_battle_result", 1),
	        (str_store_string, s9, "@The raiders are defeated! Those few who remain alive and conscious scurry off to the darkness from whence they came, terrified of the villagers and their new champion."),
			(call_script, "script_succeed_quest", "qst_defend_village"),
			(party_is_active,"$qst_defend_village_party"),
			(call_script, "script_safe_remove_party","$qst_defend_village_party"),
	      (else_try),
	      	(check_quest_active,"qst_defend_village"),
	      	(neq, "$g_battle_result", 1),
	        (call_script, "script_fail_quest", "qst_defend_village"),
	        (str_store_string, s9, "@Try as you might, you could not defeat the raiders. They raze the village to the ground and enslave the remaining peasants."),
	      #  (set_background_mesh, "mesh_draw_victory_orc"),
	        (party_is_active,"$qst_defend_village_party"),
	        (call_script, "script_safe_remove_party","$qst_defend_village_party"),
	      (else_try),
	      	(check_quest_active,"qst_raid_village"),
	        (eq, "$g_battle_result", 1),
	        (str_store_string, s9, "@The village has been razed, villagers killed or taken as slaves. The Dark Lord will be pleased."),
			(call_script, "script_succeed_quest", "qst_raid_village"),
			(troop_add_items, "trp_player", itm_human_meat, 4),
			#(set_background_mesh, "mesh_draw_victory_orc"),
			(party_is_active,"$qst_raid_village_party"),
			(call_script, "script_safe_remove_party","$qst_raid_village_party"),
		  (else_try),
			(check_quest_active,"qst_raid_village"),
	      	(neq, "$g_battle_result", 1),
	        (call_script, "script_fail_quest", "qst_raid_village"),
	        (str_store_string, s9, "@You failed to raid the village and you were sent scurrying with your men. You hear the victors cheering as you feel the disapproving gaze of the Eye."),
	       # (set_background_mesh, "mesh_draw_victory_gondor"),
	        (party_is_active,"$qst_raid_village_party"),
	        (call_script, "script_safe_remove_party","$qst_raid_village_party"),
	      (try_end),
	     ],
	    [
	      ("continue", [], "Continue...",
	       [
	        (change_screen_map),
		 ]),
	      ]
	    ),
###################### Defend / Raid Village Quest End (Kham) ##########################################



###################### Destroy Scout Camp Quest Start (Kham) ##########################################
	
	("scout_camp_quest",0,
	   "You see the scout camp nearby. You prepare your men to attack them",
	   "none",[],

	 #If Good
	 [
	 ("attack_scout_camp",[], "Attack the Scout Camp!",
	     [  
	     	(quest_get_slot, ":scout_camp_faction", "qst_destroy_scout_camp", slot_quest_target_faction),
			#(quest_get_slot, ":scout_camp_template","qst_destroy_scout_camp",slot_quest_target_party_template),
	       	(party_get_template_id,":scout_camp_template","$g_encountered_party"),
	       	(store_character_level, ":level", "trp_player"),
	     	
	 #Set Scout Camp Defender Faction
	 		(faction_get_slot, ":tier_ranged_troop", 	 ":scout_camp_faction", slot_faction_ranged_troop),
	     	(faction_get_slot, ":tier_3_troop", 		 ":scout_camp_faction", slot_faction_tier_3_troop),
	     	(faction_get_slot, ":tier_4_troop", 		 ":scout_camp_faction", slot_faction_tier_4_troop),
	     	(faction_get_slot, ":tier_5_troop", 		 ":scout_camp_faction", slot_faction_tier_5_troop),
	     	# Let's try to populate the camp with valid troops
	        (assign, ":guard_troop_1", ":tier_3_troop"),
	        (assign, ":guard_troop_2", ":tier_3_troop"),
	        (try_begin),
	        	(neq,":tier_4_troop",0),
	        	(assign, ":guard_troop_2", ":tier_4_troop"),
	        (try_end),
	        (try_begin), # Rafa: if player level is >= 17, try to upgrade the troops
	 			(ge,":level",17),
	 			(try_begin),
	 				(neq,":tier_4_troop",0),
			        (assign, ":guard_troop_1", ":tier_4_troop"),
			        (assign, ":guard_troop_2", ":tier_4_troop"),
	 			(try_end),
	 			(try_begin),
	 				(neq,":tier_5_troop",0),
			        (assign, ":guard_troop_2", ":tier_5_troop"),
			    (try_end),
			(try_end),
	        (assign, ":watchtower_troop",":tier_ranged_troop"),

	 #Get Player Level
	       	(store_character_level, ":level", "trp_player"),

	 ## Get Side & Region of Scout Camp to check which scene to spawn 	
			(try_begin),
				(is_between, "$current_player_region", region_harrowdale, region_misty_mountains),
		 		(try_begin),
		 			(eq,":scout_camp_template","pt_scout_camp_small"), #Small camp
		 			(try_begin),
		 				(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
			 			(modify_visitors_at_site, "scn_scout_camp_rohan_evil_small"),
			 			(assign, ":scout_camp_scene", "scn_scout_camp_rohan_evil_small"),
		 			(else_try),
			 			(modify_visitors_at_site, "scn_scout_camp_rohan_good_small"),
			 			(assign, ":scout_camp_scene", "scn_scout_camp_rohan_good_small"),
			 		(try_end),
		 		(else_try),    # Fortified Camp
	 				(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
		 			(modify_visitors_at_site, "scn_scout_camp_rohan_evil_big"),
		 			(assign, ":scout_camp_scene", "scn_scout_camp_rohan_evil_big"),
		 		(else_try),
		 			(modify_visitors_at_site, "scn_scout_camp_rohan_good_big"),
		 			(assign, ":scout_camp_scene", "scn_scout_camp_rohan_good_big"),
		 		(try_end),
		 		#(display_message, "@DEBUG: Rohan Region"),
		 	(else_try),
			
			## Get Region of Scout Camp
				(is_between, "$current_player_region", region_pelennor, region_harrowdale),

			## Get Side of Player to check which scout camp to spawn 	
		 		(try_begin),
		 			(eq,":scout_camp_template","pt_scout_camp_small"), #Small camp
		 			(try_begin),
		 				(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
			 			(modify_visitors_at_site, "scn_scout_camp_gondor_evil_small"),
			 			(assign, ":scout_camp_scene", "scn_scout_camp_gondor_evil_small"),
		 			(else_try),
			 			(modify_visitors_at_site, "scn_scout_camp_gondor_good_small"),
			 			(assign, ":scout_camp_scene", "scn_scout_camp_gondor_good_small"),
			 		(try_end),
		 		(else_try),  # Fortified Camp
	 				(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
		 			(modify_visitors_at_site, "scn_scout_camp_gondor_evil_big"),
		 			(assign, ":scout_camp_scene", "scn_scout_camp_gondor_evil_big"),
		 		(else_try),
		 			(gt, ":level", 17),
		 			(modify_visitors_at_site, "scn_scout_camp_gondor_good_big"),
		 			(assign, ":scout_camp_scene", "scn_scout_camp_gondor_good_big"),
		 		(try_end),
			 		#(display_message, "@DEBUG: Gondor Region"),
		 	(else_try),
			
			## Get Region of Scout Camp
				(is_between, "$current_player_region", region_n_mirkwood, region_above_mirkwook),


			## Get Side of Player to check which scout camp to spawn 	
			 	(try_begin),
		 			(eq,":scout_camp_template","pt_scout_camp_small"), #Small camp
		 			(try_begin),
		 				(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
			 			(modify_visitors_at_site, "scn_scout_camp_mirk_evil_small"),
			 			(assign, ":scout_camp_scene", "scn_scout_camp_mirk_evil_small"),
			 		(else_try),
			 			(modify_visitors_at_site, "scn_scout_camp_mirk_good_small"),
			 			(assign, ":scout_camp_scene", "scn_scout_camp_mirk_good_small"),
			 		(try_end),
		 		(else_try),  # Fortified Camp
	 				(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
		 			(modify_visitors_at_site, "scn_scout_camp_mirk_evil_big"),
		 			(assign, ":scout_camp_scene", "scn_scout_camp_mirk_evil_big"),
		 		(else_try),
		 			(modify_visitors_at_site, "scn_scout_camp_mirk_good_big"),
		 			(assign, ":scout_camp_scene", "scn_scout_camp_mirk_good_big"),
		 		(try_end),
			 		#(display_message, "@DEBUG: Mirkwood Region"),

			##North is the only region left
		 	(else_try),
				(try_begin),
		 			(eq,":scout_camp_template","pt_scout_camp_small"), #Small camp
		 			(try_begin),
		 				(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
			 			(modify_visitors_at_site, "scn_scout_camp_north_evil_small"),
			 			(assign, ":scout_camp_scene", "scn_scout_camp_north_evil_small"),
			 		(else_try),
			 			(modify_visitors_at_site, "scn_scout_camp_north_good_small"),
			 			(assign, ":scout_camp_scene", "scn_scout_camp_north_good_small"),
			 		(try_end),
		 		(else_try), # Fortified Camp
	 				(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
		 			(modify_visitors_at_site, "scn_scout_camp_north_evil_big"),
		 			(assign, ":scout_camp_scene", "scn_scout_camp_north_evil_big"),
		 		(else_try),
		 			(modify_visitors_at_site, "scn_scout_camp_north_good_big"),
		 			(assign, ":scout_camp_scene", "scn_scout_camp_north_good_big"),
		 		(try_end),
		 		#(display_message, "@DEBUG: North Region"),
		 	(try_end),
	#Set Entry and Number of Defenders   
	#0, player
	#16 & 18 - where at least 10 troops will spawn per spawn point
	#20,21,22,23,24 - Watchtower / Archer guards (1 troop per spawn point)
	        (reset_visitors),
	        (set_jump_entry, 0), 
	        (set_visitor, 0, "trp_player"),
	        (try_begin),
		        (lt, ":level",17),
		       	(val_div, ":level", 3),
		        (store_add, ":min_guards", ":level", 3),
		        (store_add, ":max_guards", ":min_guards", 3),
	        (else_try),
	        	(val_div, ":level", 5),
		        (store_add, ":min_guards", ":level", 3),
		        (store_add, ":max_guards", ":min_guards", 3),
	        (try_end),
	        (store_random_in_range, ":random_no", ":min_guards", ":max_guards"),
	        (try_begin),
		        (gt, ":guard_troop_1", 0),
		        (set_visitors, 18, ":guard_troop_1", ":random_no"),
		    (try_end),
	        (store_random_in_range, ":random_no", ":min_guards", ":max_guards"), # Rafa: rolling again
	        (val_div,":random_no",4),
	        (try_begin),
		        (gt, ":guard_troop_2", 0),
		        (set_visitors, 16, ":guard_troop_2", ":random_no"),
		    (try_end),
	        (try_begin),
		        (gt, ":watchtower_troop", 0),
		        (set_visitor, 20, ":watchtower_troop"),
		        (set_visitor, 21, ":watchtower_troop"),
		        (set_visitor, 22, ":watchtower_troop"),
		        (set_visitor, 23, ":watchtower_troop"),
		        (set_visitor, 24, ":watchtower_troop"),
		    (try_end),
	        (set_party_battle_mode),
	        (set_battle_advantage, 0),
	        (assign, "$g_battle_result", 0),
	        (set_jump_mission,"mt_destroy_scout_camp"),
	        (jump_to_scene,":scout_camp_scene"),
	        (change_screen_mission),
	       ]),
	   ("go_away",[],"Leave and regroup for now.",[(change_screen_map)]),
	 ]),


("destroy_scout_camp_quest_result",mnf_scale_picture|mnf_disable_all_keys,
	    "{s9}",
	    "none",
	    [
	      (try_begin),
	        (eq, "$g_battle_result", 1),
	        (str_store_string, s9, "@The Scout Camp has been razed, This will slow the advance of the enemy."),
			(call_script, "script_succeed_quest", "qst_destroy_scout_camp"),
			#(set_background_mesh, "mesh_draw_victory_orc"),
			(party_is_active,"$g_encountered_party"),
			(party_get_template_id, ":template", "$g_encountered_party"),
			(try_begin),
				(eq,":template","pt_scout_camp_small"),
				(call_script,"script_create_smoking_remnants","$g_encountered_party","icon_debris",6,1),
			(else_try),
				(call_script,"script_create_smoking_remnants","$g_encountered_party","icon_debris",12,1),
			(try_end),
			(call_script, "script_safe_remove_party","$g_encountered_party"),

		  (else_try),
	      	(neq, "$g_battle_result", 1),
	        (call_script, "script_fail_quest", "qst_destroy_scout_camp"),
	        (str_store_string, s9, "@You failed to destroy the Scout Camp. The enemy has taken measure of your faction and has decidedly stuck."),
	       # (set_background_mesh, "mesh_draw_victory_gondor"),
	        (party_is_active,"$g_encountered_party"),
	        (call_script, "script_safe_remove_party","$g_encountered_party"),
	      (try_end),
	     ],
	    [
	      ("continue", [], "Continue...",
	       [
	        (change_screen_map),
		 ]),
	      ]
	    ),
###################### Destroy Scout Camp Quest End (Kham) ##########################################


###################### Sea Battle Quest Start (Kham) ##########################################
	
	("sea_battle_quest",0,
	   "You meet an enemy fleet. The ships close in and sailors throw down planks...",
	   "none",[(set_background_mesh, "mesh_ui_default_menu_window")],

	 #If Good
	 [
	 ("sb_defend_the_town",[
	 	(faction_slot_eq, "$g_encountered_party_faction", slot_faction_side, faction_side_good),
	 	], "Board them! Destroy their fleet!",
	     [  
	     	#(quest_get_slot, ":target_center", "qst_blank_quest_03", slot_quest_target_center),
	     	(quest_get_slot, ":object_troop", "qst_blank_quest_03", slot_quest_object_center),
			#(store_faction_of_party, ":target_fac", ":target_center"),
			(store_faction_of_party, ":object_fac", ":object_troop"),
	       	(store_character_level, ":level", "trp_player"),
				
		# This checks what type of enemy troops to spawn, depending on faction of quest giver (North or South)
		# Once checked, we then spawn the troop we want. For higher level players, they get upgraded.
	       	# (try_begin),
	   			# (eq, ":object_fac", "fac_gondor"), #If Gondor, Allies are Gondor
	   			# (assign, ":allies_melee_tier_1", "trp_i2_pel_infantry"),
	   			# (troop_get_upgrade_troop, ":allies_melee_tier_2", "trp_i2_pel_infantry",0), #Commented out - If we want to upgrade allies too.
	   			# (assign, ":allies_archer_tier_1", "trp_a2_pel_marine"),
	   			# (troop_get_upgrade_troop, ":allies_archer_tier_2", "trp_a2_pel_marine",0),   #Commented out - If we want to upgrade allies too.

	   			# (assign, ":enemy_melee_tier_1", "trp_i3_corsair_swordsman"),
	   			# (troop_get_upgrade_troop, ":enemy_melee_tier_2", "trp_i3_corsair_swordsman",0),
	   			# (assign, ":enemy_archer_tier_1", "trp_a3_corsair_marksman"),
	   			# (troop_get_upgrade_troop, ":enemy_archer_tier_2", "trp_a3_corsair_marksman",0), 
   			# (else_try), #Dale
	   			# (eq, ":object_fac", "fac_dale"), #If Dale, Allies are Dale
	   			# (assign, ":allies_melee_tier_1", "trp_c3_rhovanion_auxilia"),
	   			# (troop_get_upgrade_troop, ":allies_melee_tier_2", "trp_c3_rhovanion_auxilia",0), #Commented out - If we want to upgrade allies too.
	   			# (assign, ":allies_archer_tier_1", "trp_a3_dale_bowman"),
	   			# (troop_get_upgrade_troop, ":allies_archer_tier_2", "trp_a3_dale_bowman",0),   #Commented out - If we want to upgrade allies too.

	   			# (assign, ":enemy_melee_tier_1", "trp_i2_rhun_tribal_warrior"),
	   			# (troop_get_upgrade_troop, ":enemy_melee_tier_2", "trp_i2_rhun_tribal_warrior",0),
	   			# (assign, ":enemy_archer_tier_1", "trp_ac3_rhun_horse_archer"),
	   			# (troop_get_upgrade_troop, ":enemy_archer_tier_2", "trp_ac3_rhun_horse_archer",0), 
   			# (try_end),
		
		# This is where we check what to spawn depending on player level (Med/High Tier)
	        # (try_begin),
	        	# (ge, ":level", 25),
	        	# (assign, ":ally_melee_troop",   ":allies_melee_tier_2"),  #Commented out - If we want to upgrade allies too.
	        	# (assign, ":ally_ranged_troop",  ":allies_archer_tier_2"), #Commented out - If we want to upgrade allies too.
	        	# (assign, ":enemy_melee_troop",  ":enemy_melee_tier_2"),
	        	# (assign, ":enemy_ranged_troop", ":enemy_archer_tier_2"),
	        # (else_try),
	        	# (assign, ":ally_melee_troop",   ":allies_melee_tier_1"),
	        	# (assign, ":ally_ranged_troop",  ":allies_archer_tier_1"),
	        	# (assign, ":enemy_melee_troop",  ":enemy_melee_tier_1"),
	        	# (assign, ":enemy_ranged_troop", ":enemy_archer_tier_1"),
	        # (try_end),

	    #This assigns the scene
   			#(assign, ":sea_battle_scene", "scn_battlefield3"), #InVain: Moved to block below
   			#(modify_visitors_at_site, ":sea_battle_scene"),

		#Set Entry and Number of Defenders. Change the last numbers in `set_visitors` to change the amount of troops to spawn.		
	        # (reset_visitors),
	        # (set_jump_entry, 0), 
	        # (set_visitor, 0, "trp_player"),

			(try_begin),
	   		(eq, ":object_fac", "fac_gondor"),  #If Gondor, Allies are Gondor
			(assign, ":sea_battle_scene", "scn_sea_battle_south"),
   			(modify_visitors_at_site, ":sea_battle_scene"),
	        (reset_visitors),
	        (set_jump_entry, 0), 
	        (set_visitor, 0, "trp_player"),
			   (try_begin),
					(lt, ":level", 25),
						#ally infantry, entries 2-7
						(set_visitors, 2, "trp_i1_pel_watchman", 3),(set_visitors, 3, "trp_i2_pel_infantry", 2),(set_visitors, 4, "trp_i3_pel_vet_infantry", 2),(set_visitors, 5, "trp_i3_gon_footman", 2),(set_visitors, 6, "trp_i3_gon_footman", 2),(set_visitors, 7, "trp_i2_pel_infantry", 2),
						#ally archers, entries 8-10
						(set_visitors, 8, "trp_i1_pel_watchman", 3),(set_visitors, 9, "trp_a3_gon_bowman", 3),(set_visitors, 10, "trp_a2_pel_marine", 3),
						#enemy infantry, entries 12-17
						(set_visitors, 12, "trp_i3_corsair_swordsman", 3),(set_visitors, 13, "trp_i3_harad_infantry", 5),(set_visitors, 14, "trp_i4_harad_swordsman", 3),(set_visitors, 15, "trp_i3_corsair_swordsman", 3),(set_visitors, 16, "trp_i2_corsair_warrior", 5),(set_visitors, 17, "trp_i3_mordor_num_warrior", 3),
						#enemy archers, entries 18-20
						(set_visitors, 18, "trp_a2_corsair_marine", 3),(set_visitors, 19, "trp_a3_harad_hunter", 3),(set_visitors, 20, "trp_a2_corsair_marine", 3),
				(else_try),
					(ge, ":level", 25),
						#ally infantry, entries 2-7
						(set_visitors, 2, "trp_i1_pel_watchman", 3),(set_visitors, 3, "trp_i2_pel_infantry", 2),(set_visitors, 4, "trp_i3_pel_vet_infantry", 2),(set_visitors, 5, "trp_i3_gon_footman", 2),(set_visitors, 6, "trp_i3_gon_footman", 2),(set_visitors, 7, "trp_i2_pel_infantry", 2),
						#ally archers, entries 8-10
						(set_visitors, 8, "trp_a2_pel_marine", 3),(set_visitors, 9, "trp_a3_gon_bowman", 3),(set_visitors, 10, "trp_a2_pel_marine", 3),
						#enemy infantry, entries 12-17
						(set_visitors, 12, "trp_i3_corsair_swordsman", 5),(set_visitors, 13, "trp_i4_harad_swordsman", 3),(set_visitors, 14, "trp_i3_harad_infantry", 5),(set_visitors, 15, "trp_i4_corsair_veteran_swordsman", 3),(set_visitors, 16, "trp_i3_corsair_swordsman", 5),(set_visitors, 17, "trp_i4_mordor_num_vet_warrior", 5),
						#enemy archers, entries 18-20
						(set_visitors, 18, "trp_a3_corsair_marksman", 3),(set_visitors, 19, "trp_a4_harad_archer", 3),(set_visitors, 20, "trp_a2_corsair_marine", 3),
				(try_end),
			(else_try),
			#(eq, ":object_fac", "fac_dale"), #If Dale, Allies are Dale
			(assign, ":sea_battle_scene", "scn_sea_battle_north"),
   			(modify_visitors_at_site, ":sea_battle_scene"),
	        (reset_visitors),
	        (set_jump_entry, 0), 
	        (set_visitor, 0, "trp_player"),
				(try_begin),
					(lt, ":level", 25),
						# ally infantry, entries 2-7
						(set_visitors, 2, "trp_i3_dale_swordsman", 3),(set_visitors, 3, "trp_i3_dale_swordsman", 3),(set_visitors, 4, "trp_i4_dale_sergeant", 2),(set_visitors, 5, "trp_i2_dale_man_at_arms", 5),(set_visitors, 6, "trp_i3_dale_spearman", 2),(set_visitors, 7, "trp_i3_dale_spearman", 2),
						#ally archers, entries 8-10
						(set_visitors, 8, "trp_a3_dale_bowman", 3),(set_visitors, 9, "trp_a3_dale_bowman", 3),(set_visitors, 10, "trp_a4_dale_archer", 3),
						#enemy infantry, entries 12-17
						(set_visitors, 12, "trp_i3_rhun_tribal_infantry", 5),(set_visitors, 13, "trp_i3_rhun_tribal_infantry", 5),(set_visitors, 14, "trp_i4_rhun_vet_infantry", 5),(set_visitors, 15, "trp_i2_rhun_tribal_warrior", 5),(set_visitors, 16, "trp_c2_rhun_horseman", 5),(set_visitors, 17, "trp_c3_rhun_swift_horseman", 5),
						#enemy archers, entries 18-20
						(set_visitors, 18, "trp_ac3_rhun_horse_archer", 4),(set_visitors, 19, "trp_ac3_rhun_horse_archer", 4),(set_visitors, 20, "trp_ac4_rhun_veteran_horse_archer", 4),
				  
				(else_try),
					(ge, ":level", 25),
						# ally infantry, entries 2-7
						(set_visitors, 2, "trp_i3_dale_swordsman", 3),(set_visitors, 3, "trp_i3_dale_swordsman", 3),(set_visitors, 4, "trp_i4_dale_sergeant", 2),(set_visitors, 5, "trp_i2_dale_man_at_arms", 5),(set_visitors, 6, "trp_i3_dale_spearman", 2),(set_visitors, 7, "trp_i3_dale_spearman", 2),
						#ally archers, entries 8-10
						(set_visitors, 8, "trp_a3_dale_bowman", 3),(set_visitors, 9, "trp_a3_dale_bowman", 3),(set_visitors, 10, "trp_a4_dale_archer", 3),
						#enemy infantry, entries 12-17
						(set_visitors, 12, "trp_i3_rhun_tribal_infantry", 5),(set_visitors, 13, "trp_i4_rhun_vet_infantry", 5),(set_visitors, 14, "trp_i4_rhun_vet_infantry", 5),(set_visitors, 15, "trp_i5_rhun_ox_warrior", 5),(set_visitors, 16, "trp_c3_rhun_outrider", 5),(set_visitors, 17, "trp_c4_rhun_noble_rider", 5),
						#enemy archers, entries 18-20
						(set_visitors, 18, "trp_ac4_rhun_veteran_horse_archer", 4),(set_visitors, 19, "trp_ac3_rhun_horse_archer", 4),(set_visitors, 20, "trp_ac4_rhun_veteran_horse_archer", 4),
						
					(try_end),
			(try_end),
			
			# (try_for_range, ":melee_allies", 2, 8), #Entry 2 - 7
				# (set_visitors, ":melee_allies", ":ally_melee_troop", 3), #Ally
			# (try_end),

			# (try_for_range, ":ranged_allies", 8, 11),  #Entry 8 - 10
				# (set_visitors, ":ranged_allies", ":ally_ranged_troop", 3), #Ally
			# (try_end),

			# (try_for_range, ":melee_enemies", 12,18 ),  #Entry 12 - 17
				# (set_visitors, ":melee_enemies", ":enemy_melee_troop", 5), #Enemy
			# (try_end),	    

			# (try_for_range, ":ranged_enemies", 18,21),  #Entry 18 - 20
				# (set_visitors, ":ranged_enemies", ":enemy_ranged_troop", 5), #Enemy
			# (try_end),	 

	        (set_party_battle_mode),
	        (set_battle_advantage, 0),
	        (assign, "$g_battle_result", 0),
	        (set_jump_mission,"mt_sea_battle_quest_good"),
	        (jump_to_scene,":sea_battle_scene"),
	        (change_screen_mission),
	       ]),

	 #If evil:
	 ("sb_attack_the_town",[
	 	(neg|faction_slot_eq, "$g_encountered_party_faction", slot_faction_side, faction_side_good),
	 	], "They try to intercept us! Defend the fleet!",
	     [  
	     	#(quest_get_slot, ":target_center", "qst_blank_quest_03", slot_quest_target_center),
	     	(quest_get_slot, ":object_troop", "qst_blank_quest_03", slot_quest_object_center),
			#(store_faction_of_party, ":target_fac", ":target_center"),
			(store_faction_of_party, ":object_fac", ":object_troop"),
	       	(store_character_level, ":level", "trp_player"),
	     	
	    # #This checks what type of enemy troops to spawn, depending on faction of quest giver (North or South)
		# #Once checked, we then spawn the troop we want. For higher level players, they get upgraded.
	       	# (try_begin),
	   			# (eq, ":object_fac", "fac_umbar"), #If Umbar, Allies are Umbar
	   			# (assign, ":allies_melee_tier_1", "trp_i3_corsair_swordsman"),
	   			# #(troop_get_upgrade_troop, ":allies_melee_tier_2", "trp_i3_corsair_swordsman",0), #Commented out - If we want to upgrade allies too.
	   			# (assign, ":allies_archer_tier_1", "trp_a3_corsair_marksman"),
	   			# #(troop_get_upgrade_troop, ":allies_archer_tier_2", "trp_a3_corsair_marksman",0),   #Commented out - If we want to upgrade allies too.

	   			# (assign, ":enemy_melee_tier_1", "trp_i2_pel_infantry"),
	   			# (troop_get_upgrade_troop, ":enemy_melee_tier_2", "trp_i2_pel_infantry",0),
	   			# (assign, ":enemy_archer_tier_1", "trp_a2_pel_marine"),
	   			# (troop_get_upgrade_troop, ":enemy_archer_tier_2", "trp_a2_pel_marine",0), 
   			# (else_try), #Rhun
	   			# (eq, ":object_fac", "fac_dale"), #If Rhun, Allies are Rhun
	   			# (assign, ":allies_melee_tier_1", "trp_i2_rhun_tribal_warrior"),
	   			# #(troop_get_upgrade_troop, ":allies_melee_tier_2", "trp_i2_rhun_tribal_warrior",0), #Commented out - If we want to upgrade allies too.
	   			# (assign, ":allies_archer_tier_1", "trp_ac3_rhun_horse_archer"),
	   			# #(troop_get_upgrade_troop, ":allies_archer_tier_2", "trp_ac3_rhun_horse_archer",0),   #Commented out - If we want to upgrade allies too.

	   			# (assign, ":enemy_melee_tier_1", "trp_c3_rhovanion_auxilia"),
	   			# (troop_get_upgrade_troop, ":enemy_melee_tier_2", "trp_c3_rhovanion_auxilia",0),
	   			# (assign, ":enemy_archer_tier_1", "trp_a3_dale_bowman"),
	   			# (troop_get_upgrade_troop, ":enemy_archer_tier_2", "trp_a3_dale_bowman",0), 
   			# (try_end),

		# #This is where we check what to spawn depending on player level (Med/High Tier)
	        # (try_begin),
	        	# (ge, ":level", 25),
	        	# #(assign, ":ally_melee_troop",   ":allies_melee_tier_2"),  #Commented out - If we want to upgrade allies too.
	        	# #(assign, ":ally_ranged_troop",  ":allies_archer_tier_2"), #Commented out - If we want to upgrade allies too.
	        	# (assign, ":enemy_melee_troop",  ":enemy_melee_tier_2"),
	        	# (assign, ":enemy_ranged_troop", ":enemy_archer_tier_2"),
	        # (else_try),
	        	# (assign, ":ally_melee_troop",   ":allies_melee_tier_1"),
	        	# (assign, ":ally_ranged_troop",  ":allies_archer_tier_1"),
	        	# (assign, ":enemy_melee_troop",  ":enemy_melee_tier_1"),
	        	# (assign, ":enemy_ranged_troop", ":enemy_archer_tier_1"),
	        # (try_end),

		#This assigns the scene
   			#(assign, ":sea_battle_scene", "scn_battlefield3"), #moved to the block below
   			#(modify_visitors_at_site, ":sea_battle_scene"),

		#Set Entry and Number of Defenders. Change the last numbers in `set_visitors` to change the amount of troops to spawn.

	        # (reset_visitors),
	        # (set_jump_entry, 11), 
	        # (set_visitor, 11, "trp_player"),

			(try_begin),
	   		(eq, ":object_fac", "fac_umbar"),  #If Umbar, Allies are Umbar
			(assign, ":sea_battle_scene", "scn_sea_battle_south"),
   			(modify_visitors_at_site, ":sea_battle_scene"),
	        (reset_visitors),
	        (set_jump_entry, 0), 
	        (set_visitor, 0, "trp_player"),
			   (try_begin),
					(lt, ":level", 25),
						#enemy infantry, entries 2-7
						(set_visitors, 2, "trp_i1_pel_watchman", 3),(set_visitors, 3, "trp_i2_pel_infantry", 3),(set_visitors, 4, "trp_i3_pel_vet_infantry", 3),(set_visitors, 5, "trp_i3_gon_footman", 3),(set_visitors, 6, "trp_i3_gon_footman", 3),(set_visitors, 7, "trp_i2_pel_infantry", 3),
						#enemy archers, entries 8-10
						(set_visitors, 8, "trp_i1_pel_watchman", 3),(set_visitors, 9, "trp_a3_gon_bowman", 2),(set_visitors, 10, "trp_a2_pel_marine", 2),
						#ally infantry, entries 12-17
						(set_visitors, 12, "trp_i3_corsair_swordsman", 5),(set_visitors, 13, "trp_i3_harad_infantry", 5),(set_visitors, 14, "trp_i4_harad_swordsman", 5),(set_visitors, 15, "trp_i3_corsair_swordsman", 5),(set_visitors, 16, "trp_i4_corsair_veteran_swordsman", 5),(set_visitors, 17, "trp_i3_mordor_num_warrior", 5),
						#ally archers, entries 18-20
						(set_visitors, 18, "trp_a3_corsair_marksman", 5),(set_visitors, 19, "trp_a3_harad_hunter", 5),(set_visitors, 20, "trp_a3_corsair_marksman", 5),
				(else_try),
					(ge, ":level", 25),
						#enemy infantry, entries 2-7
						(set_visitors, 2, "trp_i2_pel_infantry", 3),(set_visitors, 3, "trp_i3_pel_vet_infantry", 3),(set_visitors, 4, "trp_i3_pel_vet_infantry", 3),(set_visitors, 5, "trp_i4_gon_swordsman", 3),(set_visitors, 6, "trp_i5_gon_vet_swordsman", 3),(set_visitors, 7, "trp_i2_pel_infantry", 3),
						#enemy archers, entries 8-10
						(set_visitors, 8, "trp_a2_pel_marine", 3),(set_visitors, 9, "trp_a4_gon_archer", 2),(set_visitors, 10, "trp_a3_pel_vet_marine", 2),
						#ally infantry, entries 12-17
						(set_visitors, 12, "trp_i3_corsair_swordsman", 5),(set_visitors, 13, "trp_i3_harad_infantry", 5),(set_visitors, 14, "trp_i4_harad_swordsman", 5),(set_visitors, 15, "trp_i3_corsair_swordsman", 5),(set_visitors, 16, "trp_i4_corsair_veteran_swordsman", 5),(set_visitors, 17, "trp_i3_mordor_num_warrior", 5),
						#ally archers, entries 18-20
						(set_visitors, 18, "trp_a3_corsair_marksman", 5),(set_visitors, 19, "trp_a3_harad_hunter", 5),(set_visitors, 20, "trp_a3_corsair_marksman", 5),
				(try_end),
			(else_try),
			#(eq, ":object_fac", "fac_rhun"), #If Rhun, Allies are Rhun
			(assign, ":sea_battle_scene", "scn_sea_battle_north"),
   			(modify_visitors_at_site, ":sea_battle_scene"),
	        (reset_visitors),
	        (set_jump_entry, 0), 
	        (set_visitor, 0, "trp_player"),
				(try_begin),
					(lt, ":level", 25),
						# enemy infantry, entries 2-7
						(set_visitors, 2, "trp_i3_dale_swordsman", 4),(set_visitors, 3, "trp_i3_dale_swordsman", 4),(set_visitors, 4, "trp_i4_dale_sergeant", 4),(set_visitors, 5, "trp_i2_dale_man_at_arms", 4),(set_visitors, 6, "trp_i3_dale_spearman", 4),(set_visitors, 7, "trp_i3_dale_spearman", 4),
						#enemy archers, entries 8-10
						(set_visitors, 8, "trp_a3_dale_bowman", 4),(set_visitors, 9, "trp_a3_dale_bowman", 4),(set_visitors, 10, "trp_a4_dale_archer", 4),
						#ally infantry, entries 12-17
						(set_visitors, 12, "trp_i3_rhun_tribal_infantry", 5),(set_visitors, 13, "trp_i3_rhun_tribal_infantry", 5),(set_visitors, 14, "trp_i4_rhun_vet_infantry", 5),(set_visitors, 15, "trp_i2_rhun_tribal_warrior", 5),(set_visitors, 16, "trp_c2_rhun_horseman", 5),(set_visitors, 17, "trp_c3_rhun_swift_horseman", 5),
						#ally archers, entries 18-20
						(set_visitors, 18, "trp_ac3_rhun_horse_archer", 5),(set_visitors, 19, "trp_ac3_rhun_horse_archer", 5),(set_visitors, 20, "trp_ac4_rhun_veteran_horse_archer", 5),
				  
				(else_try),
					(ge, ":level", 25),
						# enemy infantry, entries 2-7
						(set_visitors, 2, "trp_i3_dale_swordsman", 3),(set_visitors, 3, "trp_i4_dale_sergeant", 3),(set_visitors, 4, "trp_i5_dale_hearthman", 3),(set_visitors, 5, "trp_i4_dale_sergeant", 3),(set_visitors, 6, "trp_i4_dale_billman", 3),(set_visitors, 7, "trp_i3_dale_spearman", 3),
						#enemy archers, entries 8-10
						(set_visitors, 8, "trp_a4_dale_archer", 3),(set_visitors, 9, "trp_a3_dale_bowman", 3),(set_visitors, 10, "trp_a5_barding_bowman", 3),
						#ally infantry, entries 12-17
						(set_visitors, 12, "trp_i3_rhun_tribal_infantry", 5),(set_visitors, 13, "trp_i3_rhun_tribal_infantry", 5),(set_visitors, 14, "trp_i4_rhun_vet_infantry", 5),(set_visitors, 15, "trp_i2_rhun_tribal_warrior", 5),(set_visitors, 16, "trp_c2_rhun_horseman", 5),(set_visitors, 17, "trp_c3_rhun_swift_horseman", 5),
						#ally archers, entries 18-20
						(set_visitors, 18, "trp_ac3_rhun_horse_archer", 5),(set_visitors, 19, "trp_ac3_rhun_horse_archer", 5),(set_visitors, 20, "trp_ac4_rhun_veteran_horse_archer", 5),
						
					(try_end),
			(try_end),			
			
			# (try_for_range, ":melee_enemies", 2, 8), #Entry 2 - 7
				# (set_visitors, ":melee_enemies", ":enemy_melee_troop", 5), #Enemy
			# (try_end),

			# (try_for_range, ":ranged_enemies", 8, 11), #Entry 8 - 10
				# (set_visitors, ":ranged_enemies", ":enemy_ranged_troop", 5), #Enemy
			# (try_end),

			# (try_for_range, ":melee_allies", 12,18 ), #Entry 12 - 17
				# (set_visitors, ":melee_allies", ":ally_melee_troop", 3), #Ally
			# (try_end),	    

			# (try_for_range, ":ranged_allies", 18,21), #Entry 18 - 20
				# (set_visitors, ":ranged_allies", ":ally_ranged_troop", 3), #Ally
			# (try_end),	 

	        (set_party_battle_mode),
	        (set_battle_advantage, 0),
	        (assign, "$g_battle_result", 0),
	        (set_jump_mission,"mt_sea_battle_quest_evil"),
	        (jump_to_scene,":sea_battle_scene"),
	        (change_screen_mission),
	       ]),
	   ("go_away",[],"Leave and regroup for now.",[(change_screen_map)]),
	 ]),

("sea_battle_quest_results",mnf_scale_picture|mnf_disable_all_keys,
	    "{s9}",
	    "none",
	    [ (set_background_mesh, "mesh_ui_default_menu_window"),
	      (try_begin),
	        (eq, "$g_battle_result", 1),
	        (try_begin),
	        	(faction_slot_eq, "$g_encountered_party_faction", slot_faction_side, faction_side_good),
	        	(str_store_string, s9, "@You have defeated the raiding fleet! This is a heavy blow to the enemy's plans!"),
	        (else_try),
	        	(str_store_string, s9, "@You defeated the intercepting fleet! Even though you do not have enough strength left to raid the city, this is a great victory!"),
	        (try_end),
			(call_script, "script_succeed_quest", "qst_blank_quest_03"),
		  (else_try),
	      	(neq, "$g_battle_result", 1),
	        (call_script, "script_fail_quest", "qst_blank_quest_03"),
	        (try_begin),
	        	(faction_slot_eq, "$g_encountered_party_faction", slot_faction_side, faction_side_good),
	        	(str_store_string, s9, "@You drove back the enemy fleet, but lost most of your ships!"),
	        (else_try),
	        	(str_store_string, s9, "@You were defeated by the intercepting fleet and failed to raid the city!"),
	        (try_end),
	      (try_end),
	     ],
	    [
	      ("continue", [], "Continue...",
	       [
	        (change_screen_map),
		 ]),
	      ]
	    ),
###################### Destroy Scout Camp Quest End (Kham) ##########################################
###################### Field AI Options Menu Begin (Kham)  ##########################################

( "camp_field_ai",0,
	"^^^^^Click on an option to toggle.^^^Turning Off One or More Options Will Improve Performance (FPS)","none",[(try_begin), (lt, "$savegame_version",3),(call_script, "script_update_savegame"), (try_end)],
    [
    ("lord_field_ai",[(str_clear, s7),(try_begin),(neq, "$field_ai_lord", 1),(str_store_string, s7, "@OFF"),
								(else_try),(str_store_string, s7, "@ON"),(try_end),
        ],"Lords Have Improved Battlefield AI:  {s7}",[
        (store_sub, "$field_ai_lord", 1, "$field_ai_lord"),(val_clamp, "$field_ai_lord", 0, 2), (jump_to_menu, "mnu_auto_field_ai"),]),
  
    ("horse_archer_field_ai",[(str_clear, s7),(try_begin),(neq, "$field_ai_horse_archer", 1),(str_store_string, s7, "@OFF"),
								(else_try),(str_store_string, s7, "@ON"),(try_end),
        ],"Horse Archers Have Improved Battlefield AI:  {s7}",[
        (store_sub, "$field_ai_horse_archer", 1, "$field_ai_horse_archer"),(val_clamp, "$field_ai_horse_archer", 0, 2), 
		(assign, "$options_horse_archer_ai", "$field_ai_horse_archer"), # Used to keep track of player choice.
        (jump_to_menu, "mnu_auto_field_ai")]),

   ("vs_orcs_field_ai",[(str_clear, s7),(try_begin),(neq, "$field_ai_archer_aim", 1),(str_store_string, s7, "@OFF"),
								(else_try),(str_store_string, s7, "@ON"),(try_end),
        ],"Archers have better aim against orcs (doesn't aim above orc heads):  {s7}",[
        (store_sub, "$field_ai_archer_aim", 1, "$field_ai_archer_aim"),(val_clamp, "$field_ai_archer_aim", 0, 2), (jump_to_menu, "mnu_auto_field_ai")]),

   ("battlefield_animals",[(str_clear, s7),(try_begin),(neq, "$tld_spawn_battle_animals", 1),(str_store_string, s7, "@OFF"),
								(else_try),(str_store_string, s7, "@ON"),(try_end),
        ],"Non-Warg / Horse Animal Companions Spawn in Battle:  {s7}",[
        (store_sub, "$tld_spawn_battle_animals", 1, "$tld_spawn_battle_animals"),(val_clamp, "$tld_spawn_battle_animals", 0, 2), (jump_to_menu, "mnu_auto_field_ai")]),

	("slow_when_wounded",[(str_clear, s7),(try_begin),(neq, "$slow_when_wounded", 1),(str_store_string, s7, "@OFF"),
								(else_try),(str_store_string, s7, "@ON"),(try_end),
        ],"Agents become Slow when Wounded:  {s7}",[
        (store_sub, "$slow_when_wounded", 1, "$slow_when_wounded"),(val_clamp, "$slow_when_wounded", 0, 2), (jump_to_menu, "mnu_auto_field_ai")]),
   
   ("battle_encounter_effects",[(str_clear, s7),(try_begin),(neq, "$battle_encounter_effects", 1),(str_store_string, s7, "@OFF"),
								(else_try),(str_store_string, s7, "@ON"),(try_end),
        ],"Special Faction Based Effects on Battlefields (e.g storms, mists):  {s7}",[
        (store_sub, "$battle_encounter_effects", 1, "$battle_encounter_effects"),(val_clamp, "$battle_encounter_effects", 0, 2), (jump_to_menu, "mnu_auto_field_ai")]),
   
   ("game_options_compat_back",[],"Back to tweaks menu.",[(jump_to_menu, "mnu_camp_tweaks")]),

    ]),



( "auto_field_ai",0,
    "This menu automatically returns to caller.",
    "none",
    [(jump_to_menu, "mnu_camp_field_ai")],[]
 ),

###################### Field AI Options Menu END (Kham)  ##########################################

###################### Dummy Menus for Morale Conversation Troop Triggers  ########################
###################### Cannibalism / Elves Leaving  START (Kham) ##################################

("hungry_orc",0,"none","none", #dummy menu to trigger hungry orc conversation
   [(store_random_in_range, ":random",0,100),
   (try_begin),
   	(le, ":random", 49),
   	(assign, "$g_talk_troop", "trp_hungry_orc"),
   	(call_script, "script_setup_troop_meeting", "trp_hungry_orc",100),
   (else_try),
   	(assign, "$g_talk_troop", "trp_hungry_uruk"),
   	(call_script, "script_setup_troop_meeting", "trp_hungry_uruk", 100),
   (try_end),
    ],[]
 ),

("leaving_elf",0,"none","none", #dummy menu to trigger leaving elf conversation
   [(try_begin),
    	(eq, "$players_kingdom", "fac_lorien"),
	   	(assign, "$g_talk_troop", "trp_longing_lorien"),
   		(call_script, "script_setup_troop_meeting", "trp_longing_lorien", 255),
   		#(display_message, "@Lorien"),
    (else_try),
    	(eq, "$players_kingdom", "fac_imladris"),
	   	(assign, "$g_talk_troop", "trp_longing_imladris"),
    	(call_script, "script_setup_troop_meeting", "trp_longing_imladris", 255),
    	#(display_message, "@Imladris"),
    (else_try),
	   	(assign, "$g_talk_troop", "trp_longing_woodelf"),
    	(call_script, "script_setup_troop_meeting", "trp_longing_woodelf", 255),
    	#(display_message, "@Woodelf"),
    (try_end),
    ],[]
 ),
###################### Cannibalism / Elves Leaving  END (Kham) ##################################
###################### Defend / Attack Refugees  START (Kham)  ##################################

("refugees_quest",0,
	"{s1}","none", 
   [(this_or_next|check_quest_active, "qst_blank_quest_01"),
    (			  check_quest_active, "qst_blank_quest_02"),
   	(try_begin),
   		(check_quest_active, "qst_blank_quest_01"),
   		(assign, ":quest", "qst_blank_quest_01"),
   	(else_try),
   		(assign, ":quest", "qst_blank_quest_02"),
   	(try_end),
   	(quest_get_slot, ":quest_target_center", ":quest", slot_quest_target_center),
    (quest_get_slot, ":quest_object_center", ":quest", slot_quest_object_center),
    (str_store_party_name, s2, ":quest_object_center"),
    (str_store_party_name, s3, ":quest_target_center"),
    (try_begin),
    	(eq, ":quest", "qst_blank_quest_01"),
    	(str_store_string, s1, "@^^^^^^^You come upon the refugees leaving {s2} and on their way to {s3}. ^^They are mostly the old and the infirmed, accompanied by women and children.^^ There are guards, but not enough to protect everyone from a raid."),
    (else_try),
    	(str_store_string, s1, "@^^^^^^^You come upon the refugees you have been tracking since {s2}. They seem to be on their way to {s3}, and are mostly the old and the infirmed. ^^ There are few guards, but not enough to stop you and your men from killing all of them."),
    (try_end),
    ],
   [("defend_refugees" ,[(check_quest_active, "qst_blank_quest_01")],"Keep your eye out for raiders...",[(change_screen_map)]),
    ("attack_refugees" ,[(check_quest_active, "qst_blank_quest_02")],"Attack the refugee train...",[(jump_to_menu, "mnu_simple_encounter")]),
    ("leave_refugees",  [(check_quest_active, "qst_blank_quest_02")],"Leave them for now...", [(change_screen_map)]),
   ],
 ),
###################### Defend / Attack Refugees  END (Kham)  ##################################

### Kham - Evil Intro Quest Menu Start

("evil_war_tutorial", 0, 
	"{s1}", "none", 
	[
	 (faction_get_slot, ":faction_lord", "$players_kingdom", slot_faction_leader),
	 (str_store_troop_name, s2, ":faction_lord"), 
 	 (faction_get_slot, ":capital", "$players_kingdom", slot_faction_capital),
	 (str_store_party_name, s3, ":capital"),
	 (try_begin),
	 	(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_hand),
	 	(assign, ":background", "mesh_town_isengard"),
	 	(str_store_string, s1, "@^^At last, the Master is making His move! The torches burn bright. The sharp weapons gleam. You and your stout lads will receive marching orders soon. Ai, there'll be fighting, lots of it, and glory enough to go around!^^You have the honour of being summoned to audience with the Master in His tower. Likely enough your first orders will be snaga's work - raid a village here, waylay a caravan there. But you'll prove yourself soon enough. Who's to say you won't play as large a role as any commander of {s2} in {s3}?^^The War has begun; the fall of Man and their allies begins!"),
	 	(set_background_mesh, ":background"),
	 (else_try),
	 	(assign, ":background", "mesh_town_morannon"),
	 	(str_store_string, s1, "@^^Your head suddenly fills with a vision - the flaming Eye. All around you, your warriors stop in their tracks. Somehow, you know at that moment that all of you are hearing the same summons, seeing the same vision. Great is the art of the Lidless Eye - great is the power of Barad-dûr!.^^The knowledge, unspoken, seeps into your very bones. The time has come. The Dark Lord commands - you shall all march upon your enemies in open war. Orders from {s2} in {s3} will come. Your part at first will not be great, but you'll prove yourself soon enough.^^ The War has begun; the fall of the West begins!"),
	 	(set_background_mesh, ":background"),
	 (try_end),],
	[
	 ("evil_war_tut_continue", [], "Continue...", [
	 	(faction_get_slot, ":capital", "$players_kingdom", slot_faction_capital),
	    (str_store_party_name, s1, ":capital"),
	    (faction_get_slot, ":faction_lord", "$players_kingdom", slot_faction_leader),
	    (str_store_troop_name_link, s9, ":faction_lord"),
	    (setup_quest_text, "qst_tld_introduction"),
	    (str_store_string, s2, "@Go to {s1} and speak with {s9}."),
	    (call_script, "script_start_quest", "qst_tld_introduction", ":faction_lord"),
	    (quest_set_slot, "qst_tld_introduction", slot_quest_target_troop, ":faction_lord"),
	    (change_screen_map),
	]),
]),
##### EVIL Intro Quest END #######

##### Guardian Party Quest Start ########


( "guardian_party_quest",0,
   "{s8} sends word that Isengard is on its heels and has prepared its last stand. He wishes you to join this final battle against Isengard's Armies.\
   You need to bring at least {reg13} troops to the army,\
   and are instructed to raise more warriors with all due haste if you do not have enough.",
    "none",
    [   
    	(quest_get_slot, ":attacking_faction", "qst_guardian_party_quest", slot_quest_object_center),
    	(set_background_mesh, "mesh_ui_default_menu_window"),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 65),
        (position_set_y, pos0, 30),
        (position_set_z, pos0, 170),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", ":attacking_faction", pos0),
        
        (quest_get_slot, ":quest_target_troop", "qst_guardian_party_quest", slot_quest_target_troop),
        (assign, ":quest_target_amount", 30),
        (call_script, "script_get_information_about_troops_position", ":quest_target_troop", 0),
        (str_clear, s9),
        (try_begin),
          (eq, reg0, 1), #troop is found and text is correct
          (str_store_string, s9, s1),
        (try_end),
        (str_store_troop_name, s8, ":quest_target_troop"),
        (assign, reg13, ":quest_target_amount"),
      ],
    [
      ("guardian_party_reject",[],"Send a message you cannot join him.",
       [  (change_screen_return),
       	  (quest_set_slot, "qst_guardian_party_quest", slot_quest_current_state, 2), # Set AI to go attack Guardian Party
        ]),
      ("guardian_party_send_word",[],"Send word you'll join him shortly.",
       [   (quest_get_slot, ":quest_target_troop", "qst_guardian_party_quest", slot_quest_target_troop),
       	   (quest_get_slot, ":attacking_faction", "qst_guardian_party_quest", slot_quest_object_center),
           (assign, ":quest_target_amount", 30),
           (str_store_troop_name_link, s13, ":quest_target_troop"),
           (assign, reg13, ":quest_target_amount"),
           (setup_quest_text, "qst_guardian_party_quest"),
           (str_store_string, s2, "@{s13} asked you to join him with at least {reg13} troops and meet Isengard's Last Stand."),
           (call_script, "script_start_quest", "qst_guardian_party_quest", ":quest_target_troop"),
           (call_script, "script_report_quest_troop_positions", "qst_guardian_party_quest", ":quest_target_troop", 3),

           #Gather army
			(try_for_range, ":accompany_marshall", heroes_begin, heroes_end),
				(store_troop_faction, ":troop_faction", ":accompany_marshall"),
				(eq, ":troop_faction", ":attacking_faction"),
				(neq, ":accompany_marshall", ":quest_target_troop"),
				(call_script, "script_accompany_marshall", ":accompany_marshall", ":quest_target_troop"),
			(try_end),
           (change_screen_return),
        ]),
     ]
 ),


#Kham - Training START
] + (is_a_wb_menu==1 and [
  
  ("alternate_training_fight",0,
    "You will be facing {reg5} opponents. Are you ready?",
    "none",
    [	(quest_get_slot, reg5, "qst_raise_troops", slot_quest_target_amount),
    	],
    [
      ("training_continue",[],"Begin training...",
        [
          #(assign, "$g_leave_encounter", 0),
          (party_get_attached_to, ":cur_center", "$g_talk_troop_party"),
          (faction_get_slot, ":fac_side", "$players_kingdom", slot_faction_side),

          (try_begin),
            (is_between, ":cur_center", centers_begin, centers_end),
            (party_get_slot, ":duel_scene", ":cur_center", slot_town_arena),
            (gt, ":duel_scene", 0),
          (else_try),
            (assign, ":closest_town", -1),
            (assign, ":minimum_dist", 10000),
            (try_for_range, ":cur_town", centers_begin, centers_end),
              (store_faction_of_party, ":town_faction", ":cur_town"),
              (faction_get_slot, ":town_side", ":town_faction", slot_faction_side),
              (eq, ":town_side", ":fac_side"),
              (store_distance_to_party_from_party, ":dist", ":cur_town", "p_main_party"),
              (lt, ":dist", ":minimum_dist"),
              (assign, ":minimum_dist", ":dist"),
              (assign, ":closest_town", ":cur_town"),
            (try_end),
            (ge, ":closest_town", 0),
            (party_get_slot, ":duel_scene", ":closest_town", slot_town_arena),
            (gt, ":duel_scene", 0),
          (else_try),
            (party_get_current_terrain, ":terrain", "$g_talk_troop_party"),
            (try_begin),
	            (eq, ":terrain", 4),
	            (assign, ":duel_scene", "scn_khand_arena"),
	        (else_try),
            	(eq, ":terrain", 5),
            	(assign, ":duel_scene", "scn_rhun_arena"),
          	(else_try),
            	(assign, ":duel_scene", "scn_dale_arena"),
          	(try_end),
          (try_end),
          (assign, "$g_encountered_party", "$g_talk_troop_party"),

          (faction_get_slot, ":troop_type", "$g_talk_troop_faction", slot_faction_tier_1_troop),
          (quest_get_slot, ":num_recruits", "qst_raise_troops", slot_quest_target_amount),

          (modify_visitors_at_site, ":duel_scene"),
          (reset_visitors),
          (set_visitor, 4, "trp_player"),
          (set_visitors, 5, ":troop_type", ":num_recruits"),
          (set_jump_mission, "mt_alternate_training"),
          (try_begin),
          	(lt, ":duel_scene", 0),
          	(assign, ":duel_scene", "scn_dale_arena"),
          (try_end),
          (jump_to_scene, ":duel_scene"),
          (jump_to_menu, "mnu_alternate_training_conclusion"),
          (change_screen_mission),
      ]),
      
    ]
  ),
  
  ("alternate_training_conclusion",0,
    "{s5}",
    "none",
    [(assign, reg5, "$g_arena_training_kills"),
      (try_begin),
        (ge, reg5, 1),
        (try_begin),
          (ge, reg5, 6),
          (store_div, ":rel_gain", reg5, 2),
          (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", ":rel_gain"), #Increase relationship by kills/2.
          (str_store_string, s5, "@You defeated {reg5} enemies and have impressed your commander."),
        (else_try),
          (str_store_string, s5, "@You defeated {reg5} enemies."),
        (try_end),
      (else_try),
        (str_store_string, s5, "@You failed to defeat any enemy."),
      (try_end),],
    [
      
      ("alternate_training_retry",[(eq, "$g_arena_training_kills", 0),],"Try again...",
        [(jump_to_menu, "mnu_alternate_training_fight")],
      ),

      ("alternate_training_finish",[(gt, "$g_arena_training_kills", 0), (quest_set_slot, "qst_raise_troops", slot_quest_current_state, "$g_arena_training_kills"), (troop_set_health, "trp_player", 100)],"Leave the arena...",
        [(change_screen_map)],
      ),
  ]),
  
] or []) + [
  #Kham - Training END


#swy-- avoid crashing from mnu_start_game_1 when returning to the main menu from anywhere else (i.e. prsnt_faction_selection_good)
#   -- this is every bit as stupid as it looks; i almost gave up.
#   --
#   -- seems like (change_screen_quit) needs to be in the consequences block of an actual menu for it to work at all,
#   -- and it turns out mnf_auto_enter just clicks the first option in the list, so we have a match made in heaven.
( "auto_quit", mnf_auto_enter,
    "This menu automatically returns to caller.",
    "none",[],
    [
        ("go_back",[],"Go back",[(change_screen_quit)])    
    ]
 ),

#( "auto_quit",0,
#    "This menu automatically returns to caller.",
#    "none",
#    [(change_screen_quit)],[]
# ),

##### Guardian Party Quest END ##########

###############Kham Menus END ####################





( "custom_battle_choose_faction1",0,
    "^^^^^^^^^^Choose your side and advantage:", "none", [(set_background_mesh, "mesh_relief01")],
    [
 ]+concatenate_scripts([[ 	
	#("good_2xmore",[],"Good faction, 2x advantage",[(assign,"$cbadvantage", 3),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
     ("good_equal" ,[],"Good faction"         ,[(assign,"$cbadvantage", 2),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
	 #("good_2xless",[],"Good faction, 2x handicap" ,[(assign,"$cbadvantage", 1),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
     #("bad_2xmore" ,[],"Evil faction, 2x advantage",[(assign,"$cbadvantage",-3),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
     ("bad_equal"  ,[],"Evil faction"         ,[(assign,"$cbadvantage",-2),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
	 #("bad_2xless" ,[],"Evil faction, 2x handicap" ,[(assign,"$cbadvantage",-1),(jump_to_menu,"mnu_custom_battle_choose_faction2"),]),
     ("replay_prev",[],"Replay previous setup",[(jump_to_menu,"mnu_custom_battle_2"),]),
 ] for ct in range(cheat_switch)])+[
     ("go_back"    ,[],"Go back"              ,[(jump_to_menu,"mnu_start_game_3")]),
 ]),
( "custom_battle_choose_faction2",0,
    "^^^^^^^^^^Choose good faction", "none", [(set_background_mesh, "mesh_relief01")],
    [
 ]+concatenate_scripts([[	
	("cb_gondor"    ,[],"Gondor"    ,[(assign,"$faction_good",fac_gondor  ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor1"   ,[],"Rohan"     ,[(assign,"$faction_good",fac_rohan   ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor2"   ,[],"Lothlorien",[(assign,"$faction_good",fac_lorien  ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor3"   ,[],"Rivendell" ,[(assign,"$faction_good",fac_imladris),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor4"   ,[],"Mirkwood"  ,[(assign,"$faction_good",fac_woodelf ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor5"   ,[],"Dwarves"   ,[(assign,"$faction_good",fac_dwarf   ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor6"   ,[],"Dale"      ,[(assign,"$faction_good",fac_dale    ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
     ("cb_gondor7"   ,[],"Beornings" ,[(assign,"$faction_good",fac_beorn   ),(jump_to_menu,"mnu_custom_battle_choose_faction3"),]),
 ] for ct in range(cheat_switch)])+[
     ("go_back"      ,[],"Go back"   ,[(jump_to_menu,"mnu_custom_battle_choose_faction1")]),
 ]),
( "custom_battle_choose_faction3",0,
    "^^^^^^^^^^Choose evil faction", "none", [(set_background_mesh, "mesh_relief01")],
    [
 ]+concatenate_scripts([[	
	("cb_mordor"    ,[],"Mordor"     ,[(assign,"$faction_evil",fac_mordor  ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor1"   ,[],"Isengard"   ,[(assign,"$faction_evil",fac_isengard),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor2"   ,[],"Dunland"    ,[(assign,"$faction_evil",fac_dunland ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor3"   ,[],"Haradrim"   ,[(assign,"$faction_evil",fac_harad   ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor4"   ,[],"Easterlings",[(assign,"$faction_evil",fac_khand   ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor5"   ,[],"Moria"      ,[(assign,"$faction_evil",fac_moria   ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor6"   ,[],"Gundabad"   ,[(assign,"$faction_evil",fac_gundabad),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor7"   ,[],"Rhun"       ,[(assign,"$faction_evil",fac_rhun    ),(jump_to_menu,"mnu_custom_battle_2"),]),
     ("cb_mordor8"   ,[],"Corsairs"   ,[(assign,"$faction_evil",fac_umbar   ),(jump_to_menu,"mnu_custom_battle_2"),]),
 ] for ct in range(cheat_switch)])+[
     ("go_back"      ,[],"Go back"    ,[(jump_to_menu,"mnu_custom_battle_choose_faction2")]),
	 ]
 ),


######################### TLD808 menus ##########################
( "ancient_ruins",0,
  "{s1}", "none", 
		[
			(set_background_mesh, "mesh_ui_default_menu_window"),
			(try_begin),
				(check_quest_succeeded, "qst_mirkwood_sorcerer"),
				(str_store_string, s1, "@The sorcerer slain, you and your companions hastily bandage up wounds and slip out into the night. Foul voices shriek at your backs and you can feel many burning eyes looking for you in the shadows. Soon the anger turns to disappointment and the sounds of pursuit are muffled, replaced by the usual heavy silence of Mirkwood. You have escaped"),			
			(else_try),
				(check_quest_failed, "qst_mirkwood_sorcerer"),
				(str_store_string, s1, "@The sorcerer slipped from your grasp and slithered into the darkness of his domain. With hearts weighted by failure, you and your companions hastily bandage up wounds and withdraw into the night. Mocking voices shriek at your backs and you can feel many burning eyes trying to pierce the shadows. Laughter and insults are soon mercifully muffled, replaced by the usual heavy silence of Mirkwood. You have escaped."),
			(else_try),
				(str_store_string, s1, "@You approach a heavily guarded region of the forest..."),				
			(try_end),
		],
  [ ("rescue_mission",  [(neg|quest_slot_ge, "qst_mirkwood_sorcerer",slot_quest_current_state,2)],
  "Sneak into the sorcerer's lair under the night's cover.",
	[
	(try_begin),
		(neg|is_currently_night),
		(store_time_of_day, reg1),
		(assign, reg2, 24),
		(val_sub, reg2, reg1),
		(display_message, "@You wait for darkness to fall...", color_good_news),
		(rest_for_hours, reg2), #rest while not attackable
		(change_screen_map),
	(else_try),
		(set_party_battle_mode),
		(call_script, "script_initialize_general_rescue"),
		(call_script, "script_initialize_sorcerer_quest"),
		(assign, "$rescue_stage", 0),
		(assign, "$active_rescue", 5),
        	(quest_set_slot,"qst_mirkwood_sorcerer",slot_quest_current_state,3),
		(disable_party, "p_ancient_ruins"), # (CppCoder) Only one chance...
		(call_script, "script_set_meta_stealth"),
		(call_script, "script_crunch_stealth_results"),
		(call_script, "script_set_infiltration_player_record"),
		(try_begin),(ge, "$stealth_results", 3),(assign, "$rescue_stage", 0),(call_script, "script_infiltration_combat_1"),
		(display_message, "@You_are_quickly_discovered_by_the_enemy."),
		(display_message, "@Eliminate_them_before_the_alarm_spreads!"),
	 	(else_try),(eq, "$stealth_results", 2),(assign, "$rescue_stage", 1),(call_script, "script_infiltration_stealth_2"),
		(display_message, "@You_advance_stealthily_far_into_the_forest."),
		(display_message, "@Scout_this_area_alone_and_meet_your_men_beyond!"),
		(display_message, "@Be_stealthy_but_eliminate_any_threats_quickly!"),
	 	(else_try),(eq, "$stealth_results", 1),(assign, "$rescue_stage", 2),(call_script, "script_final_sorcerer_fight"),
		(display_message, "@You_have_evaded_the_patrols_and_crept_close_to_the_ruins!"),
		(display_message, "@You_have_found_the_sorcerer!"),
		(try_end),
		(assign, "$active_rescue", 5),
		(change_screen_mission),
	(try_end),
	]),
    ("next_rescue_scene", [(eq, 1, 0)], "_",  
						[
						 (try_begin),
							(neq, "$alarm_level", 0),
							(display_message, "@You cannot leave until the guards lose you!", color_bad_news),
						 (try_end),
						 (eq, "$alarm_level", 0),
						 (call_script, "script_store_hero_death"),
						 (call_script, "script_set_meta_stealth"),
						 (call_script, "script_crunch_stealth_results"),
						 (try_begin),
							(eq, "$rescue_stage", 0),
							(try_begin),
								(ge, "$stealth_results", 2),
								(assign, "$rescue_stage", 1),
								(call_script, "script_infiltration_stealth_2"),
								(display_message, "@Scout_this_area_alone_and_meet_your_men_beyond!"),
								(display_message, "@Be_stealthy_but_eliminate_any_threats_quickly!"),
							(else_try),
								(assign, "$rescue_stage", 2),
								(call_script, "script_final_sorcerer_fight"),
								(display_message, "@You_have_found_the_sorcerer!"),
								(display_message, "@Kill_him_quickly_before_he_escapes!"),
							(try_end),
						(else_try),
							(eq, "$rescue_stage", 1),
							(assign, "$rescue_stage", 2),
							(call_script, "script_final_sorcerer_fight"),
							(display_message, "@You_have_found_the_sorcerer!"),
							(display_message, "@Kill_him_quickly_before_he_escapes!"),
						(try_end)],"Continue_onward!"),
		("pick_troops1", [(neg|quest_slot_ge, "qst_mirkwood_sorcerer",slot_quest_current_state,2)], "Pick companions for the mission, {reg0} selected",
							[(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
							(try_for_range, ":slot", 0, 40),
								(troop_set_slot,"trp_temp_array_a",":slot",0), # clear eligible troops array
							(try_end),
							(assign,":slot",1),
							(try_for_range, ":stack_no", 0, ":num_stacks"), # store troops eligible for stealth mission
							  (party_stack_get_troop_id,":stack_troop","p_main_party",":stack_no"),
							  (neq, ":stack_troop", "trp_player"),
							  (store_skill_level, reg1, skl_pathfinding, ":stack_troop"), # only troops with pathfinding or heroes can go on stealth missions
							  (this_or_next|gt, reg1, 0),
							  (troop_is_hero, ":stack_troop"),
								(troop_set_slot,"trp_temp_array_a",":slot",":stack_troop"),
								(val_add,":slot",1),
							(try_end),
							(assign,reg1,0),(assign,reg2,0),(assign,reg3,0),(assign,reg4,0),(assign,reg5,0),(assign,reg6,0),(assign,reg7,0),(assign,reg8,0),(assign,reg9,0),(assign,reg10,0),(assign,reg0,0),
							(jump_to_menu, "mnu_pick_troops")]),
		("leave", [], "Leave.",
							[(leave_encounter),
							(change_screen_return),
							(neg|eq, "$active_rescue", 0),
							(call_script, "script_infiltration_mission_final_casualty_tabulation")]),
	]
 ),
( "pick_troops", 0, 
  "Whom would you take with you into the stealth mission? \
   Currently you picked {reg0} companions. You can take up to 10 troops with you", "none",
   [(set_background_mesh, "mesh_ui_default_menu_window")], [ 
   #reg0 counts total # of companions picked
  ("troop1", [(troop_get_slot,":troop","trp_temp_array_a",1),(gt,":troop",0),(str_store_troop_name, s1, ":troop")],
   "{s1}: {reg1}", [(troop_get_slot,":troop","trp_temp_array_a",1),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg1,":n"),(lt,reg0,10),(val_add, reg1,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg1),(assign,reg1,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop2", [(troop_get_slot,":troop","trp_temp_array_a",2),(gt,":troop",0),(str_store_troop_name, s2, ":troop")],
   "{s2}: {reg2}", [(troop_get_slot,":troop","trp_temp_array_a",2),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg2,":n"),(lt,reg0,10),(val_add, reg2,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg2),(assign,reg2,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop3", [(troop_get_slot,":troop","trp_temp_array_a",3),(gt,":troop",0),(str_store_troop_name, s3, ":troop")],
   "{s3}: {reg3}", [(troop_get_slot,":troop","trp_temp_array_a",3),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg3,":n"),(lt,reg0,10),(val_add, reg3,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg3),(assign,reg3,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop4", [(troop_get_slot,":troop","trp_temp_array_a",4),(gt,":troop",0),(str_store_troop_name, s4, ":troop")],
   "{s4}: {reg4}", [(troop_get_slot,":troop","trp_temp_array_a",4),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg4,":n"),(lt,reg0,10),(val_add, reg4,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg4),(assign,reg4,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop5", [(troop_get_slot,":troop","trp_temp_array_a",5),(gt,":troop",0),(str_store_troop_name, s5, ":troop")],
   "{s5}: {reg5}", [(troop_get_slot,":troop","trp_temp_array_a",5),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg5,":n"),(lt,reg0,10),(val_add, reg5,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg5),(assign,reg5,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop6", [(troop_get_slot,":troop","trp_temp_array_a",6),(gt,":troop",0),(str_store_troop_name, s6, ":troop")],
   "{s6}: {reg6}", [(troop_get_slot,":troop","trp_temp_array_a",6),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg6,":n"),(lt,reg0,10),(val_add, reg6,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg6),(assign,reg6,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop7", [(troop_get_slot,":troop","trp_temp_array_a",7),(gt,":troop",0),(str_store_troop_name, s7, ":troop")],
   "{s7}: {reg7}", [(troop_get_slot,":troop","trp_temp_array_a",7),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg7,":n"),(lt,reg0,10),(val_add, reg7,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg7),(assign,reg7,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop8", [(troop_get_slot,":troop","trp_temp_array_a",8),(gt,":troop",0),(str_store_troop_name, s8, ":troop")],
   "{s8}: {reg8}", [(troop_get_slot,":troop","trp_temp_array_a",8),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg8,":n"),(lt,reg0,10),(val_add, reg8,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg8),(assign,reg8,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("troop9", [(troop_get_slot,":troop","trp_temp_array_a",9),(gt,":troop",0),(str_store_troop_name, s9, ":troop")],
   "{s9}: {reg9}", [(troop_get_slot,":troop","trp_temp_array_a",9),
                    (party_count_members_of_type, ":n", "p_main_party",":troop"),
					(try_begin),(lt,reg9,":n"),(lt,reg0,10),(val_add, reg9,1),(call_script, "script_set_hero_companion", ":troop"),
					(else_try),(val_sub,reg0,reg9),(assign,reg9,0),
					(try_end),(jump_to_menu, "mnu_pick_troops")]),  
  ("go_forward",   [], "End selecting companions and proceed.",  [#clear overflowing companions slots
					(store_add, ":empty", reg0, "fac_mission_companion_1"),
					(try_for_range, ":comp",":empty","fac_mission_companion_11"),
						(faction_set_slot, ":comp", slot_fcomp_troopid, 0),
						(faction_set_slot, ":comp", slot_fcomp_hp, 0),
					(try_end),
					(jump_to_menu, "mnu_ancient_ruins")]),  
 ]),  
( "burial_mound", 0, 
  "You_approach_the_burial_mound_of_{s1}_of_{s2}._\
  Defeated in battle by the forces of {s28}.\
  It_is_heaped_with_the_notched_weapons_of_his_fallen_enemies.", "none",
   [	(set_background_mesh, "mesh_draw_mound_visit"),
		(store_encountered_party, ":mound"),
		(party_get_slot, ":hero", ":mound", slot_party_commander_party),
		(store_troop_faction, reg1,":hero"),
		(str_store_faction_name, s2, reg1),
		(str_store_troop_name, s1, ":hero"),
		(party_get_slot, ":killer_faction", ":mound", slot_mound_killer_faction),
		(str_store_faction_name, s28, ":killer_faction"),], [
  ("pay_respects", [(store_encountered_party, ":mound"),
					(party_get_slot, ":hero", ":mound", slot_party_commander_party),
					(store_troop_faction,":faction",":hero"),
					(store_relation, reg1, ":faction", "fac_player_faction"),
					(gt, reg1, 0),
					(party_get_slot, ":state", ":mound", slot_mound_state),
					(eq, ":state", 1)],
   "Kneel_and_pay_your_respects.", [(jump_to_menu, "mnu_burial_mound_respects")]),  
  ("swear_oath",   [(store_encountered_party, ":mound"),
					(party_get_slot, ":hero", ":mound", slot_party_commander_party),
					(store_troop_faction,":faction",":hero"),
					(store_relation, reg1, ":faction", "fac_player_faction"),
					(gt, reg1, 0),
					(party_get_slot, ":state", ":mound", slot_mound_state),
					(eq, ":state", 1),
					(check_quest_active|neg, "qst_oath_of_vengeance")],
   "Swear_an_oath_of_vengeance!",  [(jump_to_menu, "mnu_burial_mound_oath")]),  
  ("despoil",      [(store_encountered_party, ":mound"),
					(str_store_party_name, s1, ":mound"),
					(party_get_slot, ":hero", ":mound", slot_party_commander_party),
					(store_troop_faction,":faction",":hero"),
					(store_relation,reg1, ":faction", "fac_player_faction"),
					(neg|gt, reg1, 0)],
   "Desecrate_the_site",  [(jump_to_menu, "mnu_burial_mound_despoil")]),  
  ("leave_mound",        [], "Leave_the_mound.",  [(leave_encounter),(change_screen_return)]),
 ]),  
( "burial_mound_respects", 0, 
  "You kneel and pay your respects to {s1}, silently mouthing a prayer for a speedy journey to the afterlife.\
  There is nothing left to be done here.", "none",
					[(set_background_mesh, "mesh_draw_mound_kneel"),
					(store_encountered_party, ":mound"),
					(party_get_slot, ":hero", ":mound", slot_party_commander_party),
					(str_store_troop_name, s1, ":hero"),
					(party_set_slot, ":mound", slot_mound_state, 2),
					(store_random_in_range, ":rnd", 0, 100),
					(try_begin),(is_between, ":rnd", 5, 15),
					(call_script, "script_cf_gain_trait_reverent"),
					 (else_try),		(neg|ge, ":rnd", 5),
					 (call_script, "script_cf_gain_trait_blessed"),
					(try_end)
					],[
  ("leave_mound",  [], "Leave_the_mound.",  [(leave_encounter),(change_screen_return)]),
 ]),  
( "burial_mound_oath", 0, 
  "You loudly swear an oath of vengeance for the death of {s4}. \
  You would relentlessly seek out the forces of {s3} and destroy them. \
  Your words carry far on the wind and who can say that they were not heard beyond the sea?", "none",
	[(set_background_mesh, "mesh_draw_mound_oath"),
	(store_encountered_party, ":mound"),
	(party_get_slot, ":hero", ":mound", slot_party_commander_party),
	(str_store_troop_name, s4, ":hero"),
	(store_troop_faction, ":target", ":hero"),
	(quest_set_slot, "qst_oath_of_vengeance", 4, ":target"), # remember source ally faction
	(quest_set_slot, "qst_oath_of_vengeance", 5, ":hero"), # CppCoder: remember source hero
	(party_get_slot, ":killer_faction", ":mound", slot_mound_killer_faction),
	(assign,":count",1000000),  # choose nearest enemy capital as target faction
	(assign,":target", 0),
	
	(try_begin),
		(faction_slot_eq, ":killer_faction", slot_faction_state, sfs_active),
		(assign, ":target", ":killer_faction"),
	(else_try),
		(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
			(store_relation, ":dist", ":fac", "fac_player_faction"),
			(lt, ":dist", 0), #enemies only
			(faction_slot_eq,":fac",slot_faction_state, sfs_active), # enemy not dead yet
			(faction_get_slot, ":capital", ":fac", slot_faction_capital),
			(store_distance_to_party_from_party,":dist",":mound",":capital"),  # choose nearest enemy capital for vengeance
			(lt, ":dist", ":count"),
			(assign,":count",":dist"),
			(assign,":target", ":fac"),
		(try_end),
	(try_end),
	
	(str_store_faction_name, s3, ":target"),
	(store_current_day, ":day"),
	(quest_set_slot, "qst_oath_of_vengeance", 1, ":day"),
	(quest_set_slot, "qst_oath_of_vengeance", 2, ":target"), # target faction
	
	#Kham - Oath of Vengeance Refactor Start
	#(assign,":count", 0), # count and store initial killcount of target faction' parties
	#(try_for_range, ":ptemplate", "pt_gondor_scouts", "pt_kingdom_hero_party"),
	#	(spawn_around_party,"p_main_party",":ptemplate"),
	#	(store_faction_of_party,":fac", reg0),
	#	(call_script, "script_safe_remove_party", reg0),
	#	(eq, ":fac", ":target"),
	#	(store_num_parties_destroyed_by_player, ":n", ":ptemplate"),
	#	(val_add,":count",":n"),
	#(try_end),
	#(quest_set_slot, "qst_oath_of_vengeance", 3, ":count"), # counter for destroyed parties of target faction at quest start
	
	(assign, "$oath_kills",0),
	#Kham - Oath of Vengeance Refactor END

	(party_set_slot, ":mound", slot_mound_state, 3), # no more oaths from here
        (setup_quest_text, "qst_oath_of_vengeance"),
        (str_store_string, s2, "@Enraged by the death of {s4}, you have sworn an oath of vengeance upon the forces of {s3}. You must now destroy as many of the troops of {s3} as possible in the coming days. You are keenly aware that your followers have witnessed this oath and you do not wish to become known as an oathbreaker. An orgy of bloodletting must now begin!"),
	(call_script, "script_start_quest", "qst_oath_of_vengeance", "trp_player"),
	],[
    ("leave_mound", [], "Leave_the_mound.", [(leave_encounter),(change_screen_return)]),
 ]),

( "funeral_pyre_oath", 0, 
  "You loudly swear an oath of vengeance for the death of {s4}. \
  You would relentlessly seek out the forces of {s3} and destroy them. \
  Your words carry far on the wind and who can say that they were not heard beyond the sea?", "none",
	[(set_background_mesh, "mesh_draw_funeral_pyre_oath"),
	(store_encountered_party, ":mound"),
	(party_get_slot, ":hero", ":mound", slot_party_commander_party),
	(str_store_troop_name, s4, ":hero"),
	(store_troop_faction, ":target", ":hero"),
	(quest_set_slot, "qst_oath_of_vengeance", 4, ":target"), # remember source ally faction
	(quest_set_slot, "qst_oath_of_vengeance", 5, ":hero"), # CppCoder: remember source hero
	
	(assign,":count",10000000),  # choose nearest enemy capital as target faction
	(assign,":target", 0),
	(try_for_range, ":fac", kingdoms_begin, kingdoms_end),
		(store_relation, ":rel", ":fac", "fac_player_faction"),
		(lt, ":rel", 0), #enemies only
		(faction_slot_eq,":fac",slot_faction_state, sfs_active), # enemy not dead yet
		(faction_get_slot, ":capital", ":fac", slot_faction_capital),
		(store_distance_to_party_from_party,":dist",":mound",":capital"),  # choose nearest enemy capital for vengeance
		(lt, ":dist", ":count"),
			(assign,":count",":dist"),
			(assign,":target", ":fac"),
	(try_end),
	
	(str_store_faction_name, s3, ":target"),
	(store_current_day, ":day"),
	(quest_set_slot, "qst_oath_of_vengeance", 1, ":day"),
	(quest_set_slot, "qst_oath_of_vengeance", 2, ":target"), # target faction
	
	#Kham - Oath of Vengeance Refactor Start
	#(assign,":count", 0), # count and store initial killcount of target faction' parties
	#(try_for_range, ":ptemplate", "pt_gondor_scouts", "pt_kingdom_hero_party"),
	#	(spawn_around_party,"p_main_party",":ptemplate"),
	#	(store_faction_of_party,":fac", reg0),
	#	(call_script, "script_safe_remove_party", reg0),
	#	(eq, ":fac", ":target"),
	#	(store_num_parties_destroyed_by_player, ":n", ":ptemplate"),
	#	(val_add,":count",":n"),
	#(try_end),
	#(quest_set_slot, "qst_oath_of_vengeance", 3, ":count"), # counter for destroyed parties of target faction at quest start
	
	(assign, "$oath_kills",0),
	#Kham - Oath of Vengeance Refactor END

	(party_set_slot, ":mound", slot_mound_state, 3), # no more oaths from here
        (setup_quest_text, "qst_oath_of_vengeance"),
        (str_store_string, s2, "@Enraged by the death of {s4}, you have sworn an oath of vengeance upon the forces of {s3}. You must now destroy as many of the troops of {s3} as possible in the coming days. You are keenly aware that your followers have witnessed this oath and you do not wish to become known as an oathbreaker. An orgy of bloodletting must now begin!"),
	(call_script, "script_start_quest", "qst_oath_of_vengeance", "trp_player"),
	],[
    ("leave_pyre_oath", [], "Leave_the_pyre.", [(leave_encounter),(change_screen_return)]),
 ]),

( "burial_mound_despoil", 0, 
  "You tear down the monument to {s1} with your own hands and defile the very stones with curses, fell chants and unspeakable acts.\
  Your followers fall back in fear of the dead but they seem to have renewed respect for your wickedness.", "none", 
	[(set_background_mesh, "mesh_draw_mound_desecrated"),
	(store_encountered_party, ":mound"),(party_get_slot, ":hero", ":mound", slot_party_commander_party),(str_store_troop_name, s1, ":hero"),
	 (store_random_in_range, ":rnd", 0, 100),
	 (try_begin),(is_between, ":rnd", 5, 10),
	 (call_script, "script_cf_gain_trait_despoiler"),
	  (else_try),    (neg|ge, ":rnd", 5),    
	  (call_script, "script_cf_gain_trait_accursed"),
	 (try_end),
	 (party_set_slot, ":mound", slot_mound_state, 4),
	 (disable_party, ":mound")],[
 ("leave_mound", [], "Leave_the_mound.", [(leave_encounter),(change_screen_return)]),
 ]),
( "funeral_pyre", 0, 
  "You approach the charred remnants of the funeral pyre of {s3} of {s2}. \
  Defeated in battle by the forces of {s28}.\
  Here, the corpse was ceremoniously burned by his personal bodyguards. \
  Nothing of value remains.", "none", 
   [(set_background_mesh, "mesh_draw_funeral_pyre"),
    (store_encountered_party, ":mound"),
	(party_get_slot, ":hero", ":mound", slot_party_commander_party),
	(str_store_troop_name, s3, ":hero"),
	(store_troop_faction,":faction",":hero"),
	(str_store_faction_name, s2, ":faction"),
	(party_get_slot, ":killer_faction", ":mound", slot_mound_killer_faction),
	(str_store_faction_name, s28, ":killer_faction"),],[
 ("swear_oath",   [(store_encountered_party, ":mound"),
					(party_get_slot, ":hero", ":mound", slot_party_commander_party),
					(store_troop_faction,":faction",":hero"),
					(store_relation, ":local2", ":faction", "fac_player_faction"),
					(gt, ":local2", 0),
					(party_get_slot, ":state", ":mound", slot_mound_state),
					(eq, ":state", 1),
					(check_quest_active|neg, "qst_oath_of_vengeance")],
   "Swear_an_oath_of_vengeance!",  [(jump_to_menu, "mnu_funeral_pyre_oath")]),  
 ("leave_pyre", [], "Leave_the_pyre.", [(leave_encounter),(change_screen_return)]), 
 ]),
( "town_ruins",mnf_enable_hot_keys|city_menu_color,
	"When you approach, you see that {s1} is {s2}",
    "none",
	code_to_set_city_background + [
	(try_begin),
		(eq, "$g_encountered_party", "p_town_isengard"),
		(str_store_string, s2, "@flooded. Somebody or something must have ruined the Isen dams."),
	(else_try),
		(str_store_string, s2, "@destroyed. Only smoldering ruins remain."),
	(try_end),
	(party_get_slot, ":elder_troop", "$g_encountered_party", slot_town_elder),
	(str_store_troop_name_plural, s1, ":elder_troop"), # elders store place referral, "trp_no_troop" stores "the_place"
    ],
    [("ruin_menu_0",[(eq, "$g_encountered_party", "p_town_isengard")],"Explore the place.",[
	    (modify_visitors_at_site,"scn_isengard_center_flooded"),
        (reset_visitors),
        (set_visitor, 1, "trp_player"),
        (jump_to_menu, "mnu_town_ruins"),
        (jump_to_scene,"scn_isengard_center_flooded"),
        (change_screen_mission),], "_"),
     ("ruin_leave",[],"Leave...",[(change_screen_return)]),
 ]),

("premutiny",0,"none","none", #dummy menu for showing orc pretender pre-mutiny dialog
   [(try_begin),
		(eq,"$mutiny_stage",0), # warning
		(call_script, "script_setup_troop_meeting", "trp_orc_pretender",100),
	(else_try),
		(change_screen_map),
	(try_end),
    ],[]
 ),
("mutiny",0,"{s1}","none",
   [(try_begin),
		(eq,"$mutiny_stage",5), # fight lost
		(str_store_string, s1, "@^^^You lost your fight against the mutiny! ^Seems like your orcs have a new commander now."),
		(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
		(try_for_range, ":stack_no", 0, ":num_stacks"), # remove all orcs
			(party_stack_get_troop_id, ":stack_troop", "p_main_party" ,":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(troop_get_type, reg3, ":stack_troop"),
			(eq, reg3, tf_orc),
			(party_stack_get_size, reg3, "p_main_party",":stack_no"),
			(party_remove_members, "p_main_party", ":stack_troop", reg3),
		(try_end),
		(assign,"$mutiny_stage",0),
    (else_try),
		(eq,"$mutiny_stage",4), #fight won
		(str_store_string, s1, "@^^^You have slain the offender, and other orcs quickly fall back in line. ^ For some time the maggots will be quiet for sure."),
		(assign,"$mutiny_stage",0),
		(call_script, "script_change_player_party_morale", 20), #kham - Give + morale when player wins.
    (else_try),
		(eq,"$mutiny_stage",2), # pre-fight dialog begin
		(call_script, "script_setup_troop_meeting", "trp_orc_pretender",100),
	(else_try),
		(eq,"$mutiny_stage",3), # pre-fight dialog ended and fight on the way
		(modify_visitors_at_site, "scn_duel_scene"),
		(reset_visitors),
		(set_jump_entry, 0), 
		(set_visitor, 0, "trp_player"),
		(set_visitor, 1, "trp_orc_pretender"),
		(call_script, "script_party_copy", "p_encountered_party_backup", "p_main_party"),
		(party_remove_members, "p_encountered_party_backup", "trp_player", 1),
		(try_for_range, ":entry", 2, 29), # populate spectators
			(call_script, "script_cf_party_remove_random_regular_troop", "p_encountered_party_backup"), #returns reg0
			(store_random_in_range, reg1,1, 100000), #rnd dna
			(set_visitor,":entry",reg0, reg1),
		(try_end),
		(set_jump_mission, "mt_arena_challenge_fight"),
		(jump_to_scene, "scn_duel_scene"),
		(change_screen_mission),
	(try_end),
    ],[
    # ("start_fight",[(eq, "$party_meeting", 0), (eq, 1,0),],"Confront the mutinee!",[
		# (modify_visitors_at_site, "scn_duel_scene"),
		# (reset_visitors),
		# (set_jump_entry, 0), 
		# (set_visitor, 0, "trp_player"),
		# (set_visitor, 1, "trp_orc_pretender"),
		# (call_script, "script_party_copy", "p_encountered_party_backup", "p_main_party"),
		# (party_remove_members, "p_encountered_party_backup", "trp_player", 1),
		# (try_for_range, ":entry", 2, 29), # populate spectators
			# (call_script, "script_cf_party_remove_random_regular_troop", "p_encountered_party_backup"), #returns reg0
			# (store_random_in_range, reg1,1, 100000), #rnd dna
			# (set_visitor,":entry",reg0, reg1),
		# (try_end),
		# (set_jump_mission, "mt_arena_challenge_fight"),
		# (jump_to_scene, "scn_duel_scene"),
		# (change_screen_mission)]),
	("leave",[],"Leave.",[(change_screen_map)])]
 ),

# ("taunt",0,
 # "You taunted the defenders, shouting insults and parading a good distance away for some time. There was no reaction apart from several arrows which fell well short of your ranks. ^Looks like there is nothing to do here",
 # "none",
   # [],[("leave",[],"Back...",[(change_screen_return)])],
 # ),


## Dummy Menu for Cannibalism. This seems to be needed...

("precannibalism",0,"none","none", 
   [
	(change_screen_map),
   ],[]
 ),


# Death menu. Just a placeholder...
( "death", mnf_disable_all_keys,
    "You have been killed. Though the war still rages on, you will no longer be part of it.",
    "none",
    [(set_background_mesh, "mesh_ui_default_menu_window")],
	[("continue",[],"Continue...",[(change_screen_quit)])]
 ),

# Animal ambushes (CppCoder)
 ("animal_ambush", 0, 
 "You and your companions find yourselves separated from the rest of your party, when suddenly...",
 "none", 
 [
	(assign, ":ambush_troop", "trp_wolf"), # (CppCoder) Default, just in case something glitches...
	(assign, ":ambush_count", 1), 
	(try_begin),
		(eq|this_or_next, "$current_player_region", region_n_mirkwood),
		(eq, "$current_player_region", region_s_mirkwood),
		(assign, ":ambush_troop", "trp_spider"),
		(assign, ":ambush_scene", "scn_mirkwood_ambush"),
		(store_random_in_range, ":ambush_count", 1, 5), # 1 to 5 spiders...
	(else_try),
		(eq|this_or_next, "$current_player_region", region_grey_mountains),
		(eq, "$current_player_region", region_misty_mountains),
		(assign, ":ambush_scene", "scn_mountain_ambush"),
		(store_random_in_range, ":rnd", 0, 100),
		(try_begin),
			(eq, "$players_kingdom", "fac_dunland"),
			(assign, ":ambush_troop", "trp_bear"),
			(assign, ":ambush_count", 1),			# 1 bear only
		(else_try),
			(neq, "$players_kingdom", "fac_beorn"), # If not a beorning there is a 40% chance of a bear ambush
			(lt, ":rnd", 40),
			(assign, ":ambush_troop", "trp_bear"),
			(assign, ":ambush_count", 1),
		(else_try),
			(assign, ":ambush_troop", "trp_wolf"),
			(store_random_in_range, ":ambush_count", 5, 9), # 5 to 8 wolves
		(try_end),
	(try_end),
	(assign, reg20, ":ambush_troop"),
	(assign, reg21, ":ambush_count"),
	(assign, reg22, ":ambush_scene"),
  
  #swy-- set the background mesh depending on what's going to attack us!
  (try_begin),
    (eq,":ambush_troop", "trp_spider"),
    (set_background_mesh, "mesh_draw_spiders"),
  (else_try),
    (eq,":ambush_troop", "trp_bear"),
    (set_background_mesh, "mesh_draw_bear"),
  (else_try),
    (eq,":ambush_troop", "trp_wolf"),
    (set_background_mesh, "mesh_draw_wolf"), #swy-- we don't have an illustration for wolves yet!
  (try_end)
 ],
 [
	("continue",[],"Continue...",
	[
	(set_jump_mission, "mt_animal_ambush"),
	(set_jump_entry, 0),
	(modify_visitors_at_site, reg22),
	(reset_visitors),

	(assign, ":cur_entry", 1),
	(try_for_range, ":npc", companions_begin, companions_end),
		(main_party_has_troop, ":npc"),
		(set_visitor, ":cur_entry", ":npc"),
		(val_add, ":cur_entry", 1),
	(try_end),
	(try_for_range, ":npc", new_companions_begin, new_companions_end),
		(main_party_has_troop, ":npc"),
		(set_visitor, ":cur_entry", ":npc"),
		(val_add, ":cur_entry", 1),
	(try_end),

	(assign, ":cur_entry", 17),
	(try_for_range, ":unused", 0, reg21),
		(set_visitor, ":cur_entry", reg20),
		(val_add, ":cur_entry", 1),
	(try_end),

	(jump_to_scene, reg22),
	(change_screen_mission),
	]),
 ],
 ),

("animal_ambush_success", 0, "The {s2} {reg0?fall:falls} before you as wheat to a scythe! Soon all your attackers lie on the floor, wounded or dead. {s3}", "none", 
[
	(assign, reg5, -1), # Reward item id.
	(try_begin),
		(gt, reg21, 1),
		(assign, reg0, 1),
		(str_store_troop_name_plural, s2, reg20),
	(else_try),
		(assign, reg0, 0),
		(str_store_troop_name, s2, reg20),
	(try_end),
  
  (assign,":ambush_troop", reg20),
  
  #swy-- set the background mesh depending on what's going to attack us!
  (try_begin),
    (eq,":ambush_troop", "trp_spider"),
    (set_background_mesh, "mesh_draw_spiders"),
  (else_try),
    (eq,":ambush_troop", "trp_bear"),
    (set_background_mesh, "mesh_draw_bear"),
  (else_try),
    (eq,":ambush_troop", "trp_wolf"),
    (set_background_mesh, "mesh_draw_wolf"), #swy-- we don't have an illustration for wolves yet!
  (try_end),
  
	(str_store_string, s3, "@You cover up your tracks and move onward."), 
],
[
	("continue",[],"Continue...",[
		(store_mul, ":exp", 100, reg21),
		(add_xp_as_reward, ":exp"),
		(try_begin),
			(gt, reg5, -1),
			(troop_add_item, "trp_player",reg5),
		(try_end),
		(change_screen_map)]),
	("repeat",[(eq, cheat_switch, 1)],"DEBUG: Repeat...",[(jump_to_menu, "mnu_animal_ambush"),]),
]),

("animal_ambush_fail", 0, "The animals bite and tear at you{reg0?,: and your companion{reg2?s,:,}} but luckily you managed to fend them off. Hopefully they won't attack you again.", "none", 
[
  (assign,":ambush_troop", reg20),

  #swy-- set the background mesh depending on what's going to attack us!
  (try_begin),
    (eq,":ambush_troop", "trp_spider"),
    (set_background_mesh, "mesh_draw_spiders"),
  (else_try),
    (eq,":ambush_troop", "trp_bear"),
    (set_background_mesh, "mesh_draw_bear"),
  (else_try),
    (eq,":ambush_troop", "trp_wolf"),
    (set_background_mesh, "mesh_draw_wolf"), #swy-- we don't have an illustration for wolves yet!
  (try_end),

	(assign, reg0, 1),
	(assign, reg1, 0),
	(assign, reg2, 0),
	(try_for_range, ":npc", companions_begin, companions_end),
		(main_party_has_troop, ":npc"),
		(assign, reg0, 0),
		(val_add, reg1, 1),
	(try_end),
	(try_for_range, ":npc", new_companions_begin, new_companions_end),
		(main_party_has_troop, ":npc"),
		(assign, reg0, 0),
		(val_add, reg1, 1),
	(try_end),
	(try_begin),
		(gt, reg1, 1),
		(assign, reg2, 1),
	(try_end),
],
[
	("continue",[],"Continue...",[(change_screen_map)]),
	("repeat",[(eq, cheat_switch, 1)],"DEBUG: Repeat...",[(jump_to_menu, "mnu_animal_ambush"),]),
]),

("build_your_scene",0,
 "You can build your own battle scene, using one of the slots provided below and the game edit mode \
 (you need to switch edit mode ON in M&B lauching screen Options first, then press Ctrl+E within a scene to access the edit mode). \
 You can then submit scenes you constructed (namely, sco files from TLD/SceneObj folder) \
 to the dev team of TLD, and if your scene is good, \
 it can appear in later releases as one of random battlegrounds!^^\
 Try to specify which region on map you want your scene to appear.^\
 Couple hints: avoid deep water, steep mountains and other impassable places, \
 unless you are experienced scene-maker and know how to bar AI troops \
 from walking where you don't want them, and make AI mesh in other places.^\
 (Entries #0-1 are for attackers, #4 for defenders, do not touch #5-8",
 "none",
   [(set_background_mesh, "mesh_ui_default_menu_window")],[
   ("scene1",[],"Plain Big (file scn_custom_1.sco)",	[(1261,"scn_custom_1"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_custom_1"),(2048)]),
   ("scene2",[],"Plain Med (file scn_custom_2.sco)",	[(1261,"scn_custom_2"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_custom_2"),(2048)]),
   ("scene3",[],"Plain Small (file scn_custom_3.sco)",	[(1261,"scn_custom_3"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_custom_3"),(2048)]),
   ("scene4",[],"Steppe Big (file scn_custom_4.sco)",	[(1261,"scn_custom_4"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_custom_4"),(2048)]),
   ("scene5",[],"Steppe Med (file scn_custom_5.sco)",	[(1261,"scn_custom_5"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_custom_5"),(2048)]),
   ("scene6",[],"Steppe Small (file scn_custom_6.sco)",	[(1261,"scn_custom_6"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_custom_6"),(2048)]),
   ("scene7",[],"Forest Big (file scn_custom_7.sco)",	[(1261,"scn_custom_7"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_custom_7"),(2048)]),
   ("scene8",[],"Forest Med (file scn_custom_8.sco)",	[(1261,"scn_custom_8"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_custom_8"),(2048)]),
   ("scene9",[],"Forest Small (file scn_custom_9.sco)",	[(1261,"scn_custom_9"),(1262,0),(1263,0,0),(1911,"mt_scene_chooser"),(1910, "scn_custom_9"),(2048)]),
   ("back_3dot" ,[],"Back...",[(change_screen_quit)])],
 ),

# ("start_game_0",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    # "Welcome, adventurer, to TLD. Let the TLD for Warband experience start nao!",
    # "none", [],
    # [ ("continue",[],"Continue...",[(jump_to_menu, "mnu_start_game_1")]),
      # ("go_back",[],"Go back",[(change_screen_quit)])]
# ),
] 

## quick scene chooser
import header_scenes
from template_tools import *
from module_scenes import scenes

sorted_scenes = sorted(scenes)
for i in xrange(len(sorted_scenes)):
  current_scene = list(sorted_scenes[i])
  current_scene[1] = get_flags_from_bitmap(header_scenes, "sf_", current_scene[1])
  sorted_scenes[i] = tuple(current_scene)

choose_scene_template = Game_Menu_Template(
  id="choose_scenes_",
  text="Choose a scene: (Page {current_page} of {num_pages})",
  optn_id="choose_scene_",
  optn_text="{list_item[0]}{list_item[1]}",
  optn_consq = [
    (modify_visitors_at_site,"scn_{list_item[0]}"),
	(reset_visitors,0),
    (set_visitor,0,"trp_player"),    
	(set_jump_mission,"mt_scene_chooser"),
	(jump_to_scene, "scn_{list_item[0]}"),
    (change_screen_mission)
  ]
)

if cheat_switch: 
  game_menus += choose_scene_template.generate_menus(sorted_scenes)
