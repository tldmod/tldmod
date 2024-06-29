from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_constants import *
from module_info import wb_compile_switch as is_a_wb_trigger

####################################################################################################################
# Simple triggers are the alternative to old style triggers. They do not preserve state, and thus simpler to maintain.
#
#  Each simple trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

simple_triggers = [
  
  # (0)This trigger is deprecated. Use "script_game_event_party_encounter" in module_scripts.py instead
  (ti_on_party_encounter,[]),
  
  # (1)This trigger is deprecated. Use "script_game_event_simulate_battle" in module_scripts.py instead
  (ti_simulate_battle,[]),
  
  # (2)
  (1,[  (gt,"$auto_besiege_town",0),
      (gt,"$g_player_besiege_town", 0),
      (ge, "$g_siege_method", 1),
      (eq, "$g_siege_force_wait", 0),
      (store_current_hours, ":cur_hours"),
      (ge, ":cur_hours", "$g_siege_method_finish_hours"),
      (neg|is_currently_night),
      (rest_for_hours, 0, 0, 0), #stop resting
  ]),
  # (3)
  (0,[(eq,"$g_player_is_captive",1),
      (gt, "$capturer_party", 0),
      (party_is_active, "$capturer_party"),
      (party_relocate_near_party, "p_main_party", "$capturer_party", 0),
  ]),
  
  # (4) Auto-menu
  (0,[(try_begin),
        (ge, "$g_last_rest_center", 0),
        (party_get_battle_opponent, ":besieger_party", "$g_last_rest_center"),
        (gt, ":besieger_party", 0),
        (store_faction_of_party, ":encountered_faction", "$g_last_rest_center"),
        (store_relation, ":faction_relation", ":encountered_faction", "fac_player_supporters_faction"),
        (store_faction_of_party, ":besieger_party_faction", ":besieger_party"),
        (store_relation, ":besieger_party_relation", ":besieger_party_faction", "fac_player_supporters_faction"),
        (ge, ":faction_relation", 0),
        (lt, ":besieger_party_relation", 0),
        (start_encounter, "$g_last_rest_center"),
        (rest_for_hours, 0, 0, 0), #stop resting
      (else_try),
        (store_current_hours, ":cur_hours"),
        (assign, ":check", 0),
        (try_begin),
          (neq, "$g_check_autos_at_hour", 0),
          (ge, ":cur_hours", "$g_check_autos_at_hour"),
          (assign, ":check", 1),
          (assign, "$g_check_autos_at_hour", 0),
        (try_end),
        (this_or_next|eq, ":check", 1),
        (map_free),
        (try_begin),
          (ge,"$auto_menu",1),
          (jump_to_menu,"$auto_menu"),
          (assign,"$auto_menu",-1),
        (else_try),
          (ge,"$auto_enter_town",1),
          (start_encounter, "$auto_enter_town"),
        (else_try),
          (ge,"$auto_besiege_town",1),
          (start_encounter, "$auto_besiege_town"),
        (else_try),
          (ge,"$g_camp_mode", 1),
          (assign, "$g_camp_mode", 0),
			(try_begin),
			(eq, "$g_fast_mode", 1),
			(assign, "$g_fast_mode", 0),
			(store_character_level, ":player_level", "trp_player"),
			(val_mul, ":player_level", 1000),
			(add_xp_to_troop, ":player_level","trp_player"), #emulate some xp gain in test mode (for siege strength relaxation)
			(try_end),
          (assign, "$g_player_icon_state", pis_normal),
          (display_message, "@Breaking camp..."),
        (try_end),
      (try_end),
  ]),
  
  
  # (5) Notification menus
  (0,[ (troop_slot_ge, "trp_notification_menu_types", 0, 1),
      (troop_get_slot, ":menu_type", "trp_notification_menu_types", 0),
      (troop_get_slot, "$g_notification_menu_var1", "trp_notification_menu_var1", 0),
      (troop_get_slot, "$g_notification_menu_var2", "trp_notification_menu_var2", 0),
      (jump_to_menu, ":menu_type"),
      (assign, ":end_cond", 2),
      (try_for_range, ":cur_slot", 1, ":end_cond"),
        (try_begin),
          (troop_slot_ge, "trp_notification_menu_types", ":cur_slot", 1),
          (val_add, ":end_cond", 1),
        (try_end),
        (store_sub, ":cur_slot_minus_one", ":cur_slot", 1),
        (troop_get_slot, ":local_temp", "trp_notification_menu_types", ":cur_slot"),
        (troop_set_slot, "trp_notification_menu_types", ":cur_slot_minus_one", ":local_temp"),
        (troop_get_slot, ":local_temp", "trp_notification_menu_var1", ":cur_slot"),
        (troop_set_slot, "trp_notification_menu_var1", ":cur_slot_minus_one", ":local_temp"),
        (troop_get_slot, ":local_temp", "trp_notification_menu_var2", ":cur_slot"),
        (troop_set_slot, "trp_notification_menu_var2", ":cur_slot_minus_one", ":local_temp"),
      (try_end),
  ]),
  
  # (6) Music,
  (1,[(map_free),(call_script, "script_music_set_situation_with_culture", mtf_sit_travel),

# Piggyback for Horse Archer AI option
  (try_begin),
    (neq, "$options_horse_archer_ai", "$field_ai_horse_archer"),
    (assign, "$field_ai_horse_archer", "$options_horse_archer_ai"), # Used to keep track of player choice.
  (try_end),

    ]),
  
  # (7) Pay day, every four days here
  (24.1 * 4,[ (call_script, "script_make_player_pay_upkeep")]),
  # (8)
  (24,[(call_script, "script_rank_income_to_player"),
      (try_for_range, ":center_no", centers_begin, centers_end),               # TLD clear rumors in centers
        (try_for_range, ":walker", town_walker_entries_start, town_walker_entries_start+num_town_walkers),
          (store_add, ":slot", slot_center_rumor_check_begin,":walker"),
          (party_set_slot, ":center_no", ":slot", 0),
        (try_end),
      (try_end),
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),  # TLD clear rumors in lords
        (troop_set_slot, ":troop_no", slot_troop_rumor_check, 0),
        #Friendship Rewards Begin
        (try_begin),
                #Give some friendship reward progress for lords who already like the player
                (call_script, "script_troop_get_player_relation", ":troop_no"),
                (assign, ":player_relation", reg0),
                #Must have at least 20 relation to get friendship reward
                (ge, ":player_relation", 20),
                (val_div, ":player_relation", 10),
                (call_script, "script_lord_friendship_reward_progress", ":troop_no", ":player_relation"),
        (try_end),
        #Friendship Rewards End
      (try_end),
      (try_for_range, ":troop_no", weapon_merchants_begin, mayors_end), # TLD clear rumors in merchants/elders
        (troop_set_slot, ":troop_no", slot_troop_rumor_check, 0),
      (try_end),

  ]),
  # (9)
  (4.15,[ #unpaid troops leaving, desertion, prisoners escape
    (try_begin),
        (store_random_in_range, ":dieroll", 1,101), (lt,":dieroll",10),
        (call_script, "script_make_unpaid_troop_go"),
    
        #desertion
        (store_skill_level, ":player_leadership", "skl_leadership", "trp_player"),
        (party_get_morale, ":morale", "p_main_party"),
        (val_mul, ":player_leadership", 2),
        (store_sub, ":desertion_check", 40, ":player_leadership"),
        (try_begin),
            (lt, ":morale", ":desertion_check"),
            (val_mul, ":morale", 2),
            (store_random_in_range, ":rand", 0, 100),
            (gt, ":rand", ":morale"),
            (dialog_box, "@Party morale is low. Troops desert from your party.", "@Desertion"),
            (val_div, ":rand", 10),
            (try_for_range, ":unused", 0, ":rand"),
                (call_script, "script_cf_party_remove_random_regular_troop", "p_main_party"),
                (str_store_troop_name, s1, reg0),
                (display_message, "@{s1} has deserted from your party."),
            (try_end),
        (try_end),
        
        #prisoners escape
        (party_get_skill_level, ":prs_management", "p_main_party", "skl_prisoner_management"),
        (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
        (call_script, "script_game_get_party_prisoner_limit"),
        (assign, ":max_prisoners", reg0),
        
        (store_mul, ":chance", ":num_prisoners", 50),
        (val_div, ":chance", ":max_prisoners"),

        (try_begin),
            (party_get_num_companions, ":num_companions", "p_main_party"),
            (gt, ":num_prisoners", ":num_companions"),
            (val_mul, ":chance", ":num_prisoners"),
            (val_div, ":chance", ":num_companions"),
            (display_message, "@You don't have enough troops to guard all your prisoners. Their chance of escaping is increased."),
            #(dialog_box, "@You don't have enough troops to guard all your prisoners. Their chance of escaping is increased.", "@Too many prisoners"),
        (try_end),


        (gt, ":num_prisoners", ":prs_management"),
        (store_random_in_range, ":rolls", ":prs_management", ":num_prisoners"),
        (try_for_range, ":unused", 0, ":rolls"),
            (store_random_in_range, ":rand", 0, 1000),
            (lt, ":rand", ":chance"),
            (call_script, "script_cf_party_remove_random_prisoner", "p_main_party"),
            (str_store_troop_name, s1, reg0),
            (display_message, "@{s1} has escaped from your party."),
        (try_end),
    (try_end),        
  ]),
  
  # (10) Reducing luck by 1 in every 180 hours #No luck in TLD, still keeping this trigger to avoid "global variable never used" warning
  (180,[(val_sub, "$g_player_luck", 1),(val_max, "$g_player_luck", 0),]),
  
  # (11)Party Morale: Move morale towards target value.
  (24,[(call_script, "script_get_player_party_morale_values"),
      (assign, ":target_morale", reg0),
      (party_get_morale, ":cur_morale", "p_main_party"),
      (store_sub, ":dif", ":target_morale", ":cur_morale"),
      (store_div, ":dif_to_add", ":dif", 5),
      (store_mul, ":dif_to_add_correction", ":dif_to_add", 5),
      (try_begin),#finding ceiling of the value
        (neq, ":dif_to_add_correction", ":dif"),
        (try_begin),
          (gt, ":dif", 0),
          (val_add, ":dif_to_add", 1),
        (else_try),
          (val_sub, ":dif_to_add", 1),
        (try_end),
      (try_end),
      (val_add, ":cur_morale", ":dif_to_add"),
      (party_set_morale, "p_main_party", ":cur_morale"),
  ]),
  
  # (12) keep track of main party region ("$current_player_region"),
  # and display log messages keey player informed of what region is he in,   (mtarini) // Reset battle size if changed for siege
  (0.5,[(call_script,"script_get_region_of_party", "p_main_party"),
      (assign, ":new_region", reg1),
      (neq, "$current_player_region", ":new_region"), # region change!
      (try_begin),
        # entering a region without a clear name
        #(this_or_next|eq, ":new_region", region_c_mirkwood),
        #(this_or_next|eq, ":new_region", region_anduin_banks),
        (eq,":new_region",-1),
        (try_begin),
          (gt, "$current_player_region", -1),
          (store_add, reg2, str_shortname_region_begin , "$current_player_region"),
          (try_begin),
            (ge, "$current_player_region", region_rhun),
            (store_sub, reg2, "$current_player_region", region_rhun),
            (val_add, reg2, str_shortname_region_begin_new),
          (try_end),
          (str_store_string,s1,reg2),
          (display_log_message, "@You have left {s1}."),
        (try_end),
      (else_try),
        (store_add, reg2, str_shortname_region_begin, ":new_region"),
        (try_begin),
            (ge, ":new_region", region_rhun),
            (store_sub, reg2, ":new_region", region_rhun),
            (val_add, reg2, str_shortname_region_begin_new),
        (try_end),
        (str_store_string,s1,reg2),
        (call_script, "script_region_get_faction", ":new_region", -1), # unbiased
        (try_begin),
          (gt, reg1, -1),
          (str_store_faction_name, s2, reg1),
          (display_log_message, "@You are entering {s1} ({s2})."),
        (else_try),
          (display_log_message, "@You are entering {s1}."),
        (try_end),
      (try_end),
      (assign, "$current_player_region", ":new_region"),
      
      
      ] + (is_a_wb_trigger==1 and [
        (call_script, "script_reset_battle_size"),
      ] or []) + [      
  ]),
  
  # (13) Party AI: pruning some of the prisoners in each center (once a week) - Kham: Changed from 72 to 46 hours
  (24*2,[(try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
        (party_get_num_prisoner_stacks, ":num_prisoner_stacks",":center_no"),
        (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
          (party_prisoner_stack_get_troop_id, ":stack_troop",":center_no",":stack_no"),
          (neg|troop_is_hero, ":stack_troop"),
          (party_prisoner_stack_get_size, ":stack_size",":center_no",":stack_no"),
          (try_begin),
            (ge,":stack_size", 100),
            (store_random_in_range, ":rand_no", 40, 80),
          (else_try),
            (store_random_in_range, ":rand_no", 10, 40),
          (try_end),
          (val_mul, ":stack_size", ":rand_no"),
          (val_div, ":stack_size", 100),
          (try_begin), #MV added this block
            (ge, ":rand_no", 30),
            (val_max, ":stack_size", 1), #POP bugfix: at least one should escape, so there are not plenty of 1-2 prisoner stacks
          (try_end),
          (party_remove_prisoners, ":center_no", ":stack_troop", ":stack_size"),
        (try_end),
      (try_end),
  ]),
  
  # (14) Hiring men with center wealths (once a day)
  (24,[(try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (ge, ":party_no", 1),
        (party_is_active, ":party_no"), #MV
        (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party), #TLD: only hosts reinforce
        (party_get_attached_to, ":cur_attached_party", ":party_no"),
        (is_between, ":cur_attached_party", centers_begin, centers_end),
        (party_slot_eq, ":cur_attached_party", slot_center_is_besieged_by, -1), #center not under siege
        (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"), #Hiring men up to lord-specific limit
      (try_end),
      
      (try_begin),
        (lt,"$savegame_version",1),
        (call_script, "script_update_savegame"), # Rafa: ensure the volunteers system is up to date
      (try_end),
      
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
        (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center does not belong to player.
        (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
        # (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD - not destroyed - redundant since (party_is_active, ":center_no")
        # (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #center not under siege #InVain uncommented
        (store_faction_of_party, ":faction", ":center_no"),
        (neg|faction_slot_eq, ":faction", slot_faction_last_stand, 1), #No more garrisons for last stand factions
        # (assign, ":hiring_budget", ":cur_wealth"),
        # (val_div, ":hiring_budget", 5),
        # (gt, ":hiring_budget", reinforcement_cost),
        
        (call_script, "script_refresh_volunteers_in_town", ":center_no"),
        
        #TLD: above replaced by this
        (party_get_slot, ":garrison_limit", ":center_no", slot_center_garrison_limit),
			(try_begin),
				(neg|faction_slot_eq, ":faction", slot_faction_side, faction_side_good),
				(val_mul, ":garrison_limit", 150),
				(val_div, ":garrison_limit", 100),
			(try_end),
        (party_get_num_companions, ":garrison_size", ":center_no"),
 
        (faction_get_slot, ":fac_strength", ":faction", slot_faction_strength), #InVain Scale center reinforcements with fac strength
        (val_div, ":fac_strength", 250), #up to 32
        (store_random_in_range, ":chance", 0, 100), 
        (try_begin),
          (gt, ":garrison_limit", ":garrison_size"),
            (try_begin),
                (is_between, ":center_no", advcamps_begin, advcamps_end), #advance camps reinforce slightly faster, because they have low garrison
                (lt, ":chance", 30),
            (else_try),
                (lt, ":chance", ":fac_strength"),
            (try_end),
          (call_script, "script_cf_reinforce_party", ":center_no"),
		  (str_store_party_name, s1, ":center_no"),
		  #(display_message, "@{s1} reinforced"),
        (try_end),
        # (val_sub, ":cur_wealth", reinforcement_cost),
        # (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
      (try_end),
  ]),
  
  # (15) Converging center prosperity to ideal prosperity once in every 15 days - MV: removed this and replaced with this:
  # (15) Party cleanup: remove empty parties, and unstick parties stuck in impassable terrain, remove routed parties that are too far from player.
  
  (23*3,
    [
      (set_spawn_radius, 3),
      (assign, ":removed_empty_parties", 0), #For debugging - Kham
      
      (try_for_parties, ":cur_party"),
        (gt, ":cur_party", "p_scribble_242"), #avoid static map parties
        (party_is_active, ":cur_party"),
        
        #swy-- don't mess with the player!
        (neq,":cur_party", "p_main_party"),
        
        #remove empty parties
        (party_get_num_companion_stacks, ":num_stacks", ":cur_party"),
        (try_begin),
          (le, ":num_stacks", 0), #kham - changed from eq
          (party_get_battle_opponent, ":opponent", ":cur_party"),
          (lt, ":opponent", 0),
          (party_get_template_id, ":cur_party_template", ":cur_party"),
          (neq, ":cur_party_template", "pt_ruins"),
          (neq, ":cur_party_template", "pt_mound"),
          (neq, ":cur_party_template", "pt_pyre"),
          (neq, ":cur_party_template", "pt_legendary_place"),
          (neq, ":cur_party_template", "pt_volunteers"), #Rafa: don't delete volunteer's parties
          (party_detach, ":cur_party"),
          (call_script, "script_safe_remove_party", ":cur_party"),
          (val_add, ":removed_empty_parties", 1),
        (else_try), # remove distant routed parties
          (party_get_battle_opponent, ":opponent", ":cur_party"),
          (lt, ":opponent", 0),
          (party_get_template_id, ":cur_party_template", ":cur_party"),
          (eq|this_or_next, ":cur_party_template", "pt_routed_allies"),
          (eq|this_or_next, ":cur_party_template", "pt_routed_enemies"),
          (eq,              ":cur_party_template", "pt_retreat_troops"),
          (store_distance_to_party_from_party, ":routed_distance", "p_main_party", ":cur_party"),
          (gt, ":routed_distance", 50),
          (call_script, "script_safe_remove_party", ":cur_party"),
        (else_try), #unstick stuck parties
          (party_get_current_terrain, ":terrain_type", ":cur_party"),
          (try_begin),
            (this_or_next|eq, ":terrain_type", rt_water),
            (this_or_next|eq, ":terrain_type", rt_mountain),
            (this_or_next|eq, ":terrain_type", rt_river),
            (this_or_next|eq, ":terrain_type", rt_mountain_forest),
            (gt, ":terrain_type", rt_desert_forest),
            
            ] + (is_a_wb_trigger==1 and [ # Rafa: Couldn't this be unified? I don't see any only-WB operation, using header_operations_mb1011.py as reference
              
              (party_get_position, pos1, ":cur_party"),
              (assign, ":max_range", 1000),
              (try_for_range, ":unused", 0 , ":max_range"),
                (map_get_land_position_around_position, pos2, pos1, 5),
                (party_set_position, "p_terrain_party", pos2),
                (party_get_current_terrain, ":temp_terrain", "p_terrain_party"),
                (try_begin),
                  (this_or_next|is_between, ":temp_terrain", rt_plain, rt_river),
                  (             eq,         ":temp_terrain", rt_forest),
                  (party_set_position, ":cur_party", pos2),
                  (assign, ":max_range", 0),
                (try_end), #End for Temp Party
              (try_end), # End for Range
              (try_begin),
                (eq, "$cheat_mode", 1),
                (str_store_party_name, s1, ":cur_party"),
                (display_message, "@DEBUG: {s1} was stuck, repositioning somewhere else!", color_good_news),
              (try_end),
              
              ] or [
              
              (assign, ":max_tries", 10),
              (try_for_range, ":unused", 0, ":max_tries"),
                # check for suitable terrain
                (spawn_around_party, ":cur_party", "pt_none"),
                (assign, ":fake_party", reg0),
                #swy-- assign it a name just for kicks, maybe causes savegame corruption and this is a good marker!
                (party_set_name,  ":fake_party", "str_fake_party"),
                (party_set_flags, ":fake_party",  pf_no_label),
                # ----
                (party_get_position, pos1, ":fake_party"),
                (party_get_current_terrain, ":terrain_type", ":fake_party"),
                (call_script, "script_safe_remove_party", ":fake_party"),
                #check for impassable terrain
                (try_begin),
                  (this_or_next|eq, ":terrain_type", rt_water),
                  (this_or_next|eq, ":terrain_type", rt_mountain),
                  (this_or_next|eq, ":terrain_type", rt_river),
                  (this_or_next|eq, ":terrain_type", rt_mountain_forest),
                  (             gt, ":terrain_type", rt_desert_forest), # any custom types?
                  #bad terrain, try again
                (else_try), #good terrain, move party there and exit loop
                  (party_set_position, ":cur_party", pos1),
                  (assign, ":max_tries", 0),
                (try_end),
              (try_end), # try_for_range :unused
              
              ]) + [
            
          (try_end),
        (try_end), #unstick
      (try_end), #try_for_parties
      
      (try_begin),
        (eq, "$cheat_mode",1),
        (assign, reg3, ":removed_empty_parties"),
        #(display_message, "@DEBUG: Removed Parties: {reg3}", color_bad_news),
      (try_end),
      
  ]),
  
  # (16) Checking if the troops are resting at a half payment point (this has to stay, in TLD!)
  (6,[(store_current_day, ":cur_day"),
      (try_begin),
        (neq, ":cur_day", "$g_last_half_payment_check_day"),
        (assign, "$g_last_half_payment_check_day", ":cur_day"),
        (try_begin),
          (eq, "$g_half_payment_checkpoint", 1),
          (val_add, "$g_cur_week_half_daily_wage_payments", 1), #half payment for yesterday
        (try_end),
        (assign, "$g_half_payment_checkpoint", 1),
      (try_end),
      (assign, ":resting_at_manor_or_walled_center", 0),
      (try_begin),
        (neg|map_free),
        (ge, "$g_last_rest_center", 0),
        (this_or_next|party_slot_eq, "$g_last_rest_center", slot_center_has_manor, 1),
        (is_between, "$g_last_rest_center", centers_begin, centers_end),
        (assign, ":resting_at_manor_or_walled_center", 1),
      (try_end),
      (eq, ":resting_at_manor_or_walled_center", 0),
      (assign, "$g_half_payment_checkpoint", 0),
  ]),
  
  
  # (17) Give some xp to hero parties
  (48,[(try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 30),
        (troop_get_slot, ":hero_party", ":troop_no", slot_troop_leaded_party),
        (gt, ":hero_party", centers_end),
        (party_is_active, ":hero_party"),
        (store_skill_level, ":trainer_level", skl_trainer, ":troop_no"), #lords have between 3 and 7 trainer skill
        (val_add, ":trainer_level", 2), #5 - 9
        (store_mul, ":xp_gain", ":trainer_level", 500), #2500 - 4500
        (party_upgrade_with_xp, ":hero_party", ":xp_gain"),
      (try_end),
      
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
        # TLD: Always upgrade volunteers in friendly towns (slowly!)
		# InVain: volunteers are now trained in script_refresh_volunteers_in_town
        #(party_get_slot, ":volunteers", ":center_no", slot_town_volunteer_pt),
        # (try_begin), 
          # (gt, ":volunteers", 0),
          # (party_is_active, ":volunteers"),
          # (party_upgrade_with_xp, ":volunteers", 100), #negotiable
        # (try_end),
        # Town garrison
        (store_random_in_range, ":rand", 0, 100),
		(store_character_level, ":player_level", "trp_player"), #slight level scaling
		(val_max, ":player_level", 10),
        (lt, ":rand", ":player_level"),
        (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
        (neq, ":center_lord", "trp_player"),
        (party_upgrade_with_xp, ":center_no", 3000),
		(party_slot_eq, ":center_no", slot_center_siegability, tld_siegable_capital),
		(party_upgrade_with_xp, ":center_no", 1500), #capitals get a bonus
      (try_end),
  ]),
  
  # (18) MAIN AI STARTING POINT
  # Decide faction ai by default every 36 hours
  (36,[
  (assign, "$g_recalculate_ais", 2),
  #(display_message, "@recalculate all trigger"),
  ]),
  
  # (19) Decide faction ai whenever flag is set
  (0,[(gt, "$g_recalculate_ais", 0),(ge,"$tld_war_began",1),
        # (try_begin),
            # (eq, "$g_recalculate_ais", 2),
            # (display_message, "@recalculate all theaters"),
        # (else_try),
            # (call_script, "script_theater_name_to_s15", "$g_recalculate_ais"),
            # (display_message, "@recalculate theater {s15}"),
        # (try_end),
      (call_script, "script_recalculate_ais", "$g_recalculate_ais"), #g_recalculate_ais also stores the theater to be recalculated
      (assign, "$g_recalculate_ais", 0),     
  ]),
  
  # (20) Count faction armies
  (24,[ (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":faction_no"),
      (try_end),
      #TLD: ease siege requirements with player level to get a more dynamic game
      (store_character_level, ":player_level", "trp_player"),
      (try_begin),
        (gt, "$tld_player_level_to_begin_war", tld_player_level_to_own_chest), #If player chooses to change war start level higher than the constant
        (assign, ":siege_requirements_relax", "$tld_player_level_to_begin_war"),
      (else_try),
        (assign, ":siege_requirements_relax", tld_player_level_to_own_chest),
      (try_end),
      (try_begin),
        (gt, ":player_level", ":siege_requirements_relax"), #some min level needed to do this
        (store_sub, ":new_fac_str_siegable", ":player_level", ":siege_requirements_relax"), #1-..
        (val_mul, ":new_fac_str_siegable", "$tld_option_siege_relax_rate"),
        (val_add, ":new_fac_str_siegable", fac_str_weak),
        (neq, ":new_fac_str_siegable", "$g_fac_str_siegable"), #this is how we determine if the player leveled up :); also makes old savegames work
        (assign, "$g_fac_str_siegable", ":new_fac_str_siegable"),
        (display_message, "@The war expands, commanders are getting bolder! (siege requirements reduced)"),
      (try_end),
      #TLD, grow faction strength with time from center income
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        #(faction_slot_ge, ":faction_no", slot_faction_strength, "$tld_option_regen_limit"), #was 1: no annoying regen for dying factions (<500/1000/1500)  - Kham removed to allow regen.
        (faction_get_slot, ":strength", ":faction_no", slot_faction_strength_tmp),
        (faction_get_slot, ":debug_gain", ":faction_no", slot_faction_debug_str_gain), #debug
        #(val_add,":strength",ws_faction_restoration), #old flat rate, obsolete
        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_is_active, ":center_no"),
          (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
          (store_faction_of_party, ":center_faction", ":center_no"),
          (eq, ":center_faction", ":faction_no"), # center belongs to kingdom
          (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #center not under siege
          (party_get_slot, ":strength_income", ":center_no", slot_center_strength_income),
				(try_begin), #no income
					(this_or_next|eq, "$tld_war_began", 0), #InVain: No incaome before the war starts
					(this_or_next|eq, "$tld_option_regen_rate", 2), #Battles only
					(eq, "$tld_option_regen_rate", 3), #None
					(assign, ":strength_income", 0),
				(else_try), #halved income
					(this_or_next|eq, "$tld_option_regen_rate", 1),
					(le, ":strength", "$tld_option_regen_limit"), #Kham - Let weak factions regen with half income
					(val_div, ":strength_income", 2),
					(store_mod, ":to_sub_for_rounding", ":strength_income", 5),
					(val_sub, ":strength_income", ":to_sub_for_rounding"), #keep it in increments of 5
				(try_end),
				(try_begin), #evil handicap: if player is evil, evil factions get less
					(neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
					(neg|faction_slot_eq, ":faction_no", slot_faction_side, faction_side_good),
					(gt, ":strength_income", 0),
					(val_div, ":strength_income", 2), #half income - tweakable
					(store_mod, ":to_sub_for_rounding", ":strength_income", 5),
					(val_sub, ":strength_income", ":to_sub_for_rounding"), #keep it in increments of 5
					(val_max, ":strength_income", 5), #has to be >0
				(try_end),
                
                #] + (is_a_wb_trigger==1 and [
                (try_begin), #campaign AI (difficulty setting)
                    (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
                    (gt, ":player_relation", 0),
                    (assign, ":campaign_ai", "$tld_campaign_diffulty"),
                    (val_add, ":campaign_ai", 4),
                    (val_mul, ":strength_income", ":campaign_ai"),
                    (val_div, ":strength_income", 5), 
                (try_end),
                #] or []) + [
         
          (val_add, ":strength", ":strength_income"),
          (val_add, ":debug_gain", ":strength_income"), #debug
        (try_end),
        #one more evil handicap: Gondor and Rohan get +20.. cheaters! #InVain: Actually, give it to all factions for more fun
        (try_begin),
          (gt, "$tld_war_began", 0),
          (eq, "$tld_option_regen_rate", 0), #Normal
          (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
          (faction_slot_eq, ":faction_no", slot_faction_side, faction_side_good),
          # (this_or_next|eq, ":faction_no", "fac_gondor"),
          # (eq, ":faction_no", "fac_rohan"),
          (val_add, ":strength", 20), #tweakable
        (try_end),
        (val_min, ":strength", fac_str_max), #limit max strength
        (faction_set_slot, ":faction_no", slot_faction_strength_tmp, ":strength"),
        (faction_set_slot, ":faction_no", slot_faction_debug_str_gain, ":debug_gain"), #debug
      (try_end),
  ]),
  # (21) Decide vassal ai
  # 7 hours in vanilla
  ( 3,[(try_begin),
        (ge,"$tld_war_began",1),  # vassal AI can change only if War started, GA
        (call_script, "script_init_ai_calculation"),
        (call_script, "script_decide_kingdom_party_ais"), # TLD, script modified to also decide if a lord spawns a host
      (try_end),
  ]),
  # (22) Process vassal ai
  ( 2,[(call_script, "script_process_kingdom_parties_ai")]),
  # (23) Process sieges
(24,[(try_begin),(ge,"$tld_war_began",1),(call_script, "script_process_sieges"),(try_end)]),
  
  # (24) Changing readiness to join army - MV: might remove all "readiness" calculations (including this trigger), so we have maximum lord participation in campaigns
  (10,[(try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (assign, ":modifier", 1),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (try_begin),
          (gt, ":party_no", 0),
          (party_is_active, ":party_no"),
          (party_get_slot, ":commander_party", ":party_no", slot_party_commander_party),
          (ge, ":commander_party", 0),
          (party_is_active, ":commander_party"),
          (store_faction_of_party, ":faction_no", ":party_no"),
          (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
          (ge, ":faction_marshall", 0),
          (troop_get_slot, ":marshall_party", ":faction_marshall", slot_troop_leaded_party),
          (eq, ":commander_party", ":marshall_party"),
          (assign, ":modifier", 0), #MV: was -1, no readiness decrease when on campaign ("weariness")
        (try_end),
        (troop_get_slot, ":readiness", ":troop_no", slot_troop_readiness_to_join_army),
        (val_add, ":readiness", ":modifier"),
        (val_clamp, ":readiness", 0, 100),
        (troop_set_slot, ":troop_no", slot_troop_readiness_to_join_army, ":readiness"),
        (assign, ":modifier", 1),
        (try_begin),
          (gt, ":party_no", 0),
          (store_troop_faction, ":troop_faction", ":troop_no"),
          (eq, ":troop_faction", "fac_player_supporters_faction"),
          (neg|troop_slot_eq, ":troop_no", slot_troop_player_order_state, spai_undefined),
          (party_get_slot, ":party_ai_state", ":party_no", slot_party_ai_state),
          (party_get_slot, ":party_ai_object", ":party_no", slot_party_ai_object),
          #Check if party is following player orders
          (try_begin),
            (troop_slot_eq, ":troop_no", slot_troop_player_order_state, ":party_ai_state"),
            (troop_slot_eq, ":troop_no", slot_troop_player_order_object, ":party_ai_object"),
            (assign, ":modifier", -1),
          (else_try),
            #Leaving following player orders if the current party order is not the same.
            (troop_set_slot, ":troop_no", slot_troop_player_order_state, spai_undefined),
            (troop_set_slot, ":troop_no", slot_troop_player_order_object, -1),
          (try_end),
        (try_end),
        (troop_get_slot, ":readiness", ":troop_no", slot_troop_readiness_to_follow_orders),
        (val_add, ":readiness", ":modifier"),
        (val_clamp, ":readiness", 0, 100),
        (troop_set_slot, ":troop_no", slot_troop_readiness_to_follow_orders, ":readiness"),
        (try_begin),
          (lt, ":readiness", 10),
          (troop_set_slot, ":troop_no", slot_troop_player_order_state, spai_undefined),
          (troop_set_slot, ":troop_no", slot_troop_player_order_object, -1),
        (try_end),
      (try_end),
  ]),
  
  # (25) Process alarms
  (3,[(call_script, "script_process_alarms")]),
  
  # (26) Process siege ai - modified with script - Kham (Oct 2018)
  (3,[(store_current_hours, ":cur_hours"),
      #Preparations: Check for besieged centers, store besieger parties, store siege time
	  (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
        (party_get_slot, ":besieger_party", ":center_no", slot_center_is_besieged_by),
        (gt, ":besieger_party", 0),
        (party_is_active, ":besieger_party"),
        (store_faction_of_party, ":besieger_faction", ":besieger_party"),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (party_slot_ge, ":center_no", slot_center_is_besieged_by, 1),
        (party_get_slot, ":siege_begin_hours", ":center_no", slot_center_siege_begin_hours),
        (store_sub, ":siege_begin_hours", ":cur_hours", ":siege_begin_hours"),
        (assign, ":launch_attack", 0),
        (assign, ":call_attack_back", 0),
        (assign, ":attacker_strength", 0),
        (assign, ":marshall_attacking", 0),
		#not 100% sure, but this double checks for those hosts that actually besiege the center, circles through, collects their individual party strengths and adds it to the sum of the attacker party strength
        (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
          (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
          (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
          (gt, ":party_no", 0),
          (party_is_active,":party_no"), #GA bugfix
          (store_troop_faction, ":troop_faction_no", ":troop_no"),
          (eq, ":troop_faction_no", ":besieger_faction"),
          (assign, ":continue", 0),
          (try_begin),
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":center_no"),
            (assign, ":continue", 1),
          (else_try),
            (party_get_slot, ":commander_party", ":party_no", slot_party_commander_party),
            (gt, ":commander_party", 0),
            (party_is_active, ":commander_party"),
            (party_slot_eq, ":commander_party", slot_party_ai_state, spai_besieging_center),
            (party_slot_eq, ":commander_party", slot_party_ai_object, ":center_no"),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (party_get_battle_opponent, ":opponent", ":party_no"),
          (this_or_next|lt, ":opponent", 0),
          (eq, ":opponent", ":center_no"),
          (try_begin),
            (faction_slot_eq, ":besieger_faction", slot_faction_marshall, ":troop_no"),
            (assign, ":marshall_attacking", 1),
          (try_end),
          (call_script, "script_party_calculate_regular_strength", ":party_no"), # get individual attacker party strength
          (val_add, ":attacker_strength", reg0), # colletive attacker party strength
        (try_end),
        (try_begin),
          (gt, ":attacker_strength", 0),
          (party_collect_attachments_to_party, ":center_no", "p_collective_enemy"), #get collective defender party strength
          (call_script, "script_party_calculate_regular_strength", "p_collective_enemy"),
          (assign, ":defender_strength", reg0),
          (try_begin),
            (eq, "$auto_enter_town", ":center_no"),
            (eq, "$g_player_is_captive", 0),
            (call_script, "script_party_calculate_regular_strength", "p_main_party"),
            (val_add, ":defender_strength", reg0),
            (val_mul, ":attacker_strength", 2), #double the power of attackers if the player is defending the center???
          (try_end),
          (party_get_slot, ":siege_hardness", ":center_no", slot_center_siege_hardness),
          (val_add, ":siege_hardness", 100),
          (val_mul, ":defender_strength", ":siege_hardness"),
          (val_div, ":defender_strength", 100),
          (val_max, ":defender_strength", 1),
          (try_begin),
            (eq, ":marshall_attacking", 1),
            (eq, ":besieger_faction", "$players_kingdom"),
            (check_quest_active, "qst_follow_army"),
            (val_mul, ":attacker_strength", 2), #double the power of attackers if the player is in the campaign
          (try_end),
          (store_mul, ":strength_ratio", ":attacker_strength", 100),
          (val_div, ":strength_ratio", ":defender_strength"),
          (store_sub, ":random_up_limit", ":strength_ratio", 250), #Kham - was 200 (TLD 3.5 Apr 2017)
          (try_begin),
            (neg|faction_slot_ge, ":center_faction", slot_faction_strength, fac_str_very_weak),
            (val_max, ":random_up_limit", 0), #MV: if the defending faction is on its knees, even a suicidal siege attack is welcome, as it will lower the garrison and defending lord strength for the next siege; but mostly we hope that the player will intervene and win
          (try_end),
          (try_begin),
            (gt, ":random_up_limit", -100), #never attack if the strength ratio is less than 1:1 (was 2:1)
            (store_div, ":siege_begin_hours_effect", ":siege_begin_hours", 3),
            (val_add, ":random_up_limit", ":siege_begin_hours_effect"),
          (try_end),
          (val_div, ":random_up_limit", 5),
          (val_max, ":random_up_limit", 0),
          (store_sub, ":random_down_limit", 100, ":strength_ratio"), #was 200, less siege retreats now
          (val_max, ":random_down_limit", 0),
          (try_begin), #:random_up_limit is the chance to decide for attack
            (store_random_in_range, ":rand", 0, 100),
            (val_add, ":random_up_limit", 20), #kham - lets start sieges earlier
            (this_or_next|lt, ":rand", ":random_up_limit"),
            (faction_slot_ge, ":besieger_faction", slot_faction_scripted_until, ":cur_hours"), #always attack if in scripted mode
            (gt, ":siege_begin_hours", 24),#initial preparation
            (assign, ":launch_attack", 1),
          (else_try), #if not, :random_down_limit is the chance to give up siege
            (store_random_in_range, ":rand", 0, 100),
            (lt, ":rand", ":random_down_limit"),
            (assign, ":call_attack_back", 1),
          (try_end),
        (else_try),
          (assign, ":call_attack_back", 1),
        (try_end),
        
        #Assault the fortress
        (try_begin),
          (eq, ":launch_attack", 1),
          (call_script, "script_begin_assault_on_center", ":center_no"),
        (else_try),
          (eq, ":call_attack_back", 1),
          (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
            (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
            (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
            (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
            (gt, ":party_no", 0),
            (party_is_active, ":party_no"), #Kham - fix
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":center_no"),
            (party_slot_eq, ":party_no", slot_party_ai_substate, 1),
            (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
            (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":center_no"),
            #resetting siege begin time if at least 1 party retreats
            (party_set_slot, ":center_no", slot_center_siege_begin_hours, ":cur_hours"),
          (try_end),
        (try_end),
       (try_end),
    ]),
  
  # (27) Reset hero quest status
  # Change hero relation
  (12,[(try_for_range, ":troop_no", heroes_begin, heroes_end),
        (troop_set_slot, ":troop_no", slot_troop_does_not_give_quest, 0),
      (try_end),
      (try_for_range, ":troop_no", mayors_begin, mayors_end),
        (troop_set_slot, ":troop_no", slot_troop_does_not_give_quest, 0),
      (try_end),
  ]),
  
  # (28) Attach Lord Parties to the town they are in
  (0.1,[(try_for_range, ":troop_no", heroes_begin, heroes_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":troop_party_no", ":troop_no", slot_troop_leaded_party),
        (party_is_active, ":troop_party_no"), #GA. when hero loses battles slot is not emptied, can cause errors
        (ge, ":troop_party_no", 1),
        (party_get_attached_to, ":cur_attached_town", ":troop_party_no"),
        (lt, ":cur_attached_town", 1),
        (party_get_cur_town, ":destination", ":troop_party_no"),
        (is_between, ":destination", centers_begin, centers_end),
        (call_script, "script_get_relation_between_parties", ":destination", ":troop_party_no"),
        (try_begin),
          (ge, reg0, 0),
          (party_attach_to_party, ":troop_party_no", ":destination"),
        (else_try),
          (party_set_ai_behavior, ":troop_party_no", ai_bhvr_hold),
        (try_end),
        (try_begin),
          (this_or_next|party_slot_eq, ":destination", slot_party_type, spt_town),
          (party_slot_eq, ":destination", slot_party_type, spt_castle),
          (store_faction_of_party, ":troop_faction_no", ":troop_party_no"),
          (store_faction_of_party, ":destination_faction_no", ":destination"),
          (eq, ":troop_faction_no", ":destination_faction_no"),
          (party_get_num_prisoner_stacks, ":num_stacks", ":troop_party_no"),
          (gt, ":num_stacks", 0),
          (assign, "$g_move_heroes", 1),
          (call_script, "script_party_prisoners_add_party_prisoners", ":destination", ":troop_party_no"),#Moving prisoners to the center
          (assign, "$g_move_heroes", 1),
          (call_script, "script_party_remove_all_prisoners", ":troop_party_no"),
        (try_end),
      (try_end),
      
      # Piggybacking on this trigger to check for routed parties.
      # (call_script, "script_spawn_routed_parties"),
      
  ]),
  
  # (29) Check escape chances of hero prisoners.
  (24,[  
      (assign, ":hero_escape_chance", 210), #player party, scale chance with prisoner management
      (party_get_skill_level, ":prs_management", "p_main_party", "skl_prisoner_management"),
      (val_mul, ":prs_management", 20),
      (val_sub, ":hero_escape_chance", ":prs_management"),
      (assign, reg78, ":hero_escape_chance"),
      (call_script, "script_randomly_make_prisoner_heroes_escape_from_party", "p_main_party", ":hero_escape_chance"),
      
      (try_for_range, ":center_no", centers_begin, centers_end), #towns, maybe unneeded in TLD?
        ##         (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (party_is_active, ":center_no"), #TLD
        (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
        (assign, ":chance", 30),
        (try_begin),
          (party_slot_eq, ":center_no", slot_center_has_prisoner_tower, 1),
          (assign, ":chance", 5),
        (try_end),
        (call_script, "script_randomly_make_prisoner_heroes_escape_from_party", ":center_no", ":chance"),
      (try_end),
  ]),
  
  # (30) Respawn hero party after kingdom hero is released from captivity.
  (48,  # changed from 48 to 24 in TLD, GA # Changed again to 48, but gave them reinforcements - Kham (TLD 3.5 - Apr 2017)
    [  (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1),
        (neg|troop_slot_eq, ":troop_no", slot_troop_wound_mask, wound_death),

        (store_current_day, ":cur_day"), #set a minimal respawn time
        (troop_get_slot, ":day_of_defeat", ":troop_no", slot_troop_respawn_timer),
        (val_sub, ":cur_day", ":day_of_defeat"),
        (ge, ":cur_day", 2),
        
        (store_random_in_range, ":chance", 0, 7), #chance increases with waiting time, one week maximum
        (le, ":chance", ":cur_day"),
        
        
        (store_troop_faction, ":cur_faction", ":troop_no"),
        (try_begin),
          (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active), #MV, defensive
          (call_script, "script_cf_select_random_walled_center_with_faction_and_owner_priority_no_siege", ":cur_faction", ":troop_no"),#Can fail
          (assign, ":center_no", reg0),
          (call_script, "script_create_kingdom_hero_party", ":troop_no", ":center_no"),
          (party_attach_to_party, "$pout_party", ":center_no"),
          (call_script, "script_cf_reinforce_party", "$pout_party"), #Kham  (TLD 3.5 Apr 2017)
        (else_try),
          (neg|faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
          (troop_set_slot, ":troop_no", slot_troop_change_to_faction, "fac_commoners"), #TLD: defeated faction lords simply disappear
          # (try_begin),
          # (is_between, ":troop_no", kings_begin, kings_end),
          # (troop_set_slot, ":troop_no", slot_troop_change_to_faction, "fac_commoners"),
          # (else_try),
          # (store_random_in_range, ":random_no", 0, 100),
          # (lt, ":random_no", 10),
          # (call_script, "script_cf_get_random_active_faction_except_player_faction_and_faction", ":cur_faction"),
          # (troop_set_slot, ":troop_no", slot_troop_change_to_faction, reg0),
          # (try_end),
        (try_end),
      (try_end),
  ]),
  
  #(72,[(call_script, "script_update_trade_good_prices")]),
  
  # (31) Troop AI: Merchants thinking
  (8,[(try_for_parties, ":party_no"),
        (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
        (party_is_active, ":party_no"),
        #(assign, reg0, ":party_no"),
        #(display_message, "@DEBUG: Caravan {reg0}", 0xff00fd33),
        (party_is_in_any_town, ":party_no"),
        #(display_message, "@DEBUG: Point 1", 0xff00fd33),
        (store_faction_of_party, ":merchant_faction", ":party_no"),
        (faction_get_slot, ":num_towns", ":merchant_faction", slot_faction_num_towns),
        (try_begin),
          (le, ":num_towns", 0),
          (call_script, "script_safe_remove_party", ":party_no"),
          #(display_message, "@DEBUG: removed", 0xff00fd33),
        (else_try),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", 35),
          #(display_message, "@DEBUG: random", 0xff00fd33),
          (party_get_cur_town, ":cur_center", ":party_no"),
          (assign, ":can_leave", 1),
          (try_begin),
            (is_between, ":cur_center", centers_begin, centers_end),
            (neg|party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
            (assign, ":can_leave", 0),
          (try_end),
          (eq, ":can_leave", 1),
          #(display_message, "@DEBUG: can leave", 0xff00fd33),
          (assign, ":do_trade", 0),
          (try_begin),
            (party_get_slot, ":cur_ai_state", ":party_no", slot_party_ai_state),
            (eq, ":cur_ai_state", spai_trading_with_town),
            (party_get_slot, ":cur_ai_object", ":party_no", slot_party_ai_object),
            (eq, ":cur_center", ":cur_ai_object"),
            (assign, ":do_trade", 1),
          (try_end),
          (assign, ":target_center", -1),
          
          (try_begin), #Make sure escorted caravan continues to its original destination.
            #	(eq, "$caravan_escort_party_id", ":party_no"),
            #	(neg|party_is_in_town, ":party_no", "$caravan_escort_destination_town"),
            #	(assign, ":target_center", "$caravan_escort_destination_town"),
            #(else_try),
            (call_script, "script_cf_select_random_town_at_peace_with_faction_in_trade_route", ":cur_center", ":merchant_faction"),
            (assign, ":target_center", reg0),
            (eq, ":target_center", -1),
            (call_script, "script_safe_remove_party", ":party_no"), #MV: no towns to travel to, remove
          (try_end),
          
          (is_between, ":target_center", centers_begin, centers_end),
          #(display_message, "@DEBUG: target", 0xff00fd33),
          (neg|party_is_in_town, ":party_no", ":target_center"),
          #(display_message, "@DEBUG: set off", 0xff00fd33),
          (try_begin),
            (eq, ":do_trade", 1),
            (call_script, "script_do_merchant_town_trade", ":party_no", ":cur_center"),
          (try_end),
          (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
          (party_set_ai_object, ":party_no", ":target_center"),
          (party_set_flags, ":party_no", pf_default_behavior, 0),
          (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
          (party_set_slot, ":party_no", slot_party_ai_object, ":target_center"),
        (try_end),
      (try_end),
  ]),
  
  #cache party strengths (to avoid re-calculating)
  ##  (2,[ (try_for_range, ":cur_troop", heroes_begin, heroes_end),
  ##         (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
  ##         (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
  ##         (ge, ":cur_party", 0),
  ##         (call_script, "script_party_calculate_strength", ":cur_party", 0), #will update slot_party_cached_strength
  ##       (try_end),
  ##    ]),
  ##
  ##  (6,[ (try_for_range, ":cur_center", centers_begin, centers_end),
  ##         (call_script, "script_party_calculate_strength", ":cur_center", 0), #will update slot_party_cached_strength
  ##       (try_end),
  ##     ]),
  
  ##  (1,
  ##   [   (try_for_range, ":cur_center", centers_begin, centers_end),
  ##         (store_random_in_range, ":rand", 0, 100),
  ##         (lt, ":rand", 10),
  ##         (store_faction_of_party, ":center_faction", ":cur_center"),
  ##         (assign, ":friend_strength", 0),
  ##         (try_for_range, ":cur_troop", heroes_begin, heroes_end),
  ##           (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
  ##           (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
  ##           (gt, ":cur_troop_party", 0),
  ##           (store_distance_to_party_from_party, ":distance", ":cur_troop_party", ":cur_center"),
  ##           (lt, ":distance", 10),
  ##           (store_troop_faction, ":army_faction", ":cur_troop"),
  ##           (store_relation, ":rel", ":army_faction", ":center_faction"),
  ##           (try_begin),
  ##             (gt, ":rel", 10),
  ##             (party_get_slot, ":str", ":cur_troop_party", slot_party_cached_strength),
  ##             (val_add, ":friend_strength", ":str"),
  ##           (try_end),
  ##         (try_end),
  ##         (party_set_slot, ":cur_center", slot_party_nearby_friend_strength, ":friend_strength"),
  ##       (try_end),
  ##    ]),
  
# (32) Make heroes running away from someone retreat to friendly centers

  #WB Version - Take into account the angle of the center and the lord

] + (is_a_wb_trigger==1 and [
  (0.5,
   [
        (try_for_range, ":cur_troop", heroes_begin, heroes_end),
          (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
          (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
          (gt, ":cur_party", 0),
          (try_begin),
            (party_is_active, ":cur_party"),
            (try_begin),
              (get_party_ai_current_behavior, ":ai_bhvr", ":cur_party"),
              (eq, ":ai_bhvr", ai_bhvr_avoid_party),
              (assign, ":continue", 1),
              (get_party_ai_current_object, ":ai_object", ":cur_party"),
              (eq, ":continue", 1),
              (store_faction_of_party, ":party_faction", ":cur_party"),
              (party_get_slot, ":commander_party", ":cur_party", slot_party_commander_party),
              (faction_get_slot, ":faction_marshall", ":party_faction", slot_faction_marshall),
              (neq, ":faction_marshall", ":cur_troop"),
              (assign, ":continue", 1),
              (try_begin),
                (ge, ":faction_marshall", 0),
                (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
                (party_is_active, ":faction_marshall_party", 0),
                (eq, ":commander_party", ":faction_marshall_party"),
                (assign, ":continue", 0),
              (try_end),
              (eq, ":continue", 1),
              (assign, ":done", 0),
              (try_for_range, ":cur_center", centers_begin, centers_end),
                (party_is_active, ":cur_center"), #TLD
                (party_slot_eq, ":cur_center", slot_center_destroyed, 0), #TLD
                (eq, ":done", 0),
                (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
                (store_faction_of_party, ":center_faction", ":cur_center"),
                (store_relation, ":cur_relation", ":center_faction", ":party_faction"),
                (gt, ":cur_relation", 0),
                (store_distance_to_party_from_party, ":cur_distance", ":cur_party", ":cur_center"),
                (lt, ":cur_distance", 20),
                (party_get_position, pos1, ":cur_party"),
                (party_get_position, pos2, ":cur_center"),
                (neg|position_is_behind_position, pos2, pos1),
#Angle effect start
                (assign, ":alpha", 0),
                (assign, ":betta",0),
                (party_get_position, pos3, ":ai_object"),
                (position_get_x, ":x1", pos1),
                (position_get_y, ":y1", pos1),
                (position_get_x, ":x2", pos2),
                (position_get_y, ":y2", pos2),
                (position_get_x, ":x3", pos3),
                (position_get_y, ":y3", pos3),
                (store_sub, ":y", ":y1", ":y2"),
                (store_sub, ":x", ":x1", ":x2"),
                (store_atan2, ":alpha", ":y", ":x"),
                (store_sub, ":y", ":y1", ":y3"),
                (store_sub, ":x", ":x1", ":x3"),
                (store_atan2, ":betta", ":y", ":x"),
                (store_sub, ":angle", ":betta", ":alpha"),
                (val_abs, ":angle"),
                (store_distance_to_party_from_party, ":cur_distance", ":cur_party", ":ai_object"),
                (try_begin),
                  (gt, ":cur_distance", 5),
                  (gt, ":angle", 45),
                  (call_script, "script_party_set_ai_state", ":cur_party", spai_retreating_to_center, ":cur_center"),
                  (assign, ":done", 1),
                (else_try),
                  (gt, ":angle", 90),
                  (call_script, "script_party_set_ai_state", ":cur_party", spai_retreating_to_center, ":cur_center"),
                  (assign, ":done", 1),
                (try_end),
              (try_end),
            (try_end),
          (else_try),
            (troop_set_slot, ":cur_troop", slot_troop_leaded_party, -1),
          (try_end),
        (try_end),
    ]),

 #MB Version - Native

] or [
  (0.5,[(try_for_range, ":cur_troop", heroes_begin, heroes_end),
        (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
        (gt, ":cur_party", 0),
        (try_begin),
          (party_is_active, ":cur_party"),
          (try_begin),
            (get_party_ai_current_behavior, ":ai_bhvr", ":cur_party"),
            (eq, ":ai_bhvr", ai_bhvr_avoid_party),
            (store_faction_of_party, ":party_faction", ":cur_party"),
            (party_get_slot, ":commander_party", ":cur_party", slot_party_commander_party),
            (faction_get_slot, ":faction_marshall", ":party_faction", slot_faction_marshall),
            (neq, ":faction_marshall", ":cur_troop"),
            (assign, ":continue", 1),
            (try_begin),
              (ge, ":faction_marshall", 0),
              (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
              (ge, ":faction_marshall_party", 0),
              (eq, ":commander_party", ":faction_marshall_party"),
              (assign, ":continue", 0),
            (try_end),
            (try_begin),
              (store_current_hours, ":cur_time"),
              (party_slot_ge, ":cur_party", slot_party_follow_player_until_time, ":cur_time"), # MV: don't retreat if following orders
              (assign, ":continue", 0),
            (try_end),
            (eq, ":continue", 1),
            (assign, ":done", 0),
            (try_for_range, ":cur_center", centers_begin, centers_end),
              (party_is_active, ":cur_center"), #TLD
              (party_slot_eq, ":cur_center", slot_center_destroyed, 0), #TLD
              (eq, ":done", 0),
              (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
              (store_faction_of_party, ":center_faction", ":cur_center"),
              (store_relation, ":cur_relation", ":center_faction", ":party_faction"),
              (gt, ":cur_relation", 0),
              (store_distance_to_party_from_party, ":cur_distance", ":cur_party", ":cur_center"),
              (lt, ":cur_distance", 20),
              (party_get_position, pos1, ":cur_party"),
              (party_get_position, pos2, ":cur_center"),
              (neg|position_is_behind_position, pos2, pos1),
              (call_script, "script_party_set_ai_state", ":cur_party", spai_retreating_to_center, ":cur_center"),
              (assign, ":done", 1),
            (try_end),
          (try_end),
        (else_try),
          (troop_set_slot, ":cur_troop", slot_troop_leaded_party, -1),
        (try_end),
      (try_end),
  ]),
]) + [

  # (33) Centers give alarm if the player is around
  (0.5,[(store_current_hours, ":cur_hours"),
      (store_mod, ":cur_hours_mod", ":cur_hours", 11),
      (store_sub, ":hour_limit", ":cur_hours", 5),
      (party_get_num_companions, ":num_men", "p_main_party"),
      (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
      (val_add, ":num_men", ":num_prisoners"),
      (convert_to_fixed_point, ":num_men"),
      (store_sqrt, ":num_men_effect", ":num_men"),
      (convert_from_fixed_point, ":num_men_effect"),
      (try_begin),
        (eq, ":cur_hours_mod", 0),
        #Reduce alarm by 2 in every 11 hours.
        (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
          (faction_get_slot, ":player_alarm", ":cur_faction", slot_faction_player_alarm),
          (val_sub, ":player_alarm", 1),
          (val_max, ":player_alarm", 0),
          (faction_set_slot, ":cur_faction", slot_faction_player_alarm, ":player_alarm"),
        (try_end),
      (try_end),
      (eq, "$g_player_is_captive", 0),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
        (party_slot_eq, ":cur_center", slot_center_destroyed, 0), #TLD
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (store_relation, ":reln", ":cur_faction", "fac_player_supporters_faction"),
        (lt, ":reln", 0),
        (store_distance_to_party_from_party, ":dist", "p_main_party", ":cur_center"),
        (lt, ":dist", 5),
        (store_mul, ":dist_sqr", ":dist", ":dist"),
        (store_sub, ":dist_effect", 20, ":dist_sqr"),
        (store_sub, ":reln_effect", 20, ":reln"),
        (store_mul, ":total_effect", ":dist_effect", ":reln_effect"),
        (val_mul, ":total_effect", ":num_men_effect"),
        (store_div, ":spot_chance", ":total_effect", 10),
        (store_random_in_range, ":random_spot", 0, 1000),
        (lt, ":random_spot", ":spot_chance"),
        (faction_get_slot, ":player_alarm", ":cur_faction", slot_faction_player_alarm),
        (val_add, ":player_alarm", 1),
        (val_min, ":player_alarm", 100),
        (faction_set_slot, ":cur_faction", slot_faction_player_alarm, ":player_alarm"),
        (try_begin),
          (neg|party_slot_ge, ":cur_center", slot_center_last_player_alarm_hour, ":hour_limit"),
          (str_store_party_name_link, s1, ":cur_center"),
          (display_message, "@Your party is spotted by {s1}."),
          (party_set_slot, ":cur_center", slot_center_last_player_alarm_hour, ":cur_hours"),
        (try_end),
      (try_end),

      ##Kham - Piggyback on trigger for Player Controlled allies
      (try_begin),
        (neq, "$player_control_allies",0),
        (assign, "$player_control_allies",0),
        (try_begin),
          (eq, "$cheat_mode",1),
          (display_message, "@DEBUG: Player Control Allies RESET"),
        (try_end),
      (try_end),
  ]),
  
  # (34) Check active items for their deactivation hour
  (3,
  [(try_begin), #orc brew
        (player_has_item, "itm_orc_brew"),
        (item_slot_eq, "itm_orc_brew", slot_item_is_active, 1),
		#(call_script, "script_cf_troop_has_active_item", "trp_player", "itm_orc_brew"),
		(store_current_hours, ":now_hours"),
		(item_get_slot, ":expiration_hours", "itm_orc_brew", slot_item_deactivation_hour),
		(le, ":expiration_hours", ":now_hours"),
		(item_set_slot, "itm_orc_brew", slot_item_is_active, 0),
        (troop_get_inventory_capacity, ":capacity", "trp_player"),
        (try_for_range, ":cur_slot", 0, ":capacity"),
            (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
            (eq, ":cur_item", "itm_orc_brew"),
            (troop_inventory_slot_get_item_amount, ":cur_amount", "trp_player", ":cur_slot"),
            (val_sub, ":cur_amount", 1),
            (troop_inventory_slot_set_item_amount, "trp_player", ":cur_slot", ":cur_amount"),  
            (assign, ":capacity", 0), 
        (try_end),
		#(troop_remove_item, "trp_player", "itm_orc_brew"),
		(display_message, "@The effects of the Orc Brew have dissipated."),
    (else_try),
        (player_has_item, "itm_miruvor_reward"),
        (item_slot_eq, "itm_miruvor_reward", slot_item_is_active, 1),
		(store_current_hours, ":now_hours"),
		(item_get_slot, ":expiration_hours", "itm_miruvor_reward", slot_item_deactivation_hour),
		(le, ":expiration_hours", ":now_hours"),
		(item_set_slot, "itm_miruvor_reward", slot_item_is_active, 0),
        (troop_get_inventory_capacity, ":capacity", "trp_player"),
        (try_for_range, ":cur_slot", 0, ":capacity"),
            (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
            (eq, ":cur_item", "itm_miruvor_reward"),
            (troop_inventory_slot_get_item_amount, ":cur_amount", "trp_player", ":cur_slot"),
            (val_sub, ":cur_amount", 1),
            (troop_inventory_slot_set_item_amount, "trp_player", ":cur_slot", ":cur_amount"),  
            (assign, ":capacity", 0), 
        (try_end),
		(display_message, "@The effects of the Miruvor have dissipated."),
    (else_try),
        (player_has_item, "itm_athelas_reward"),
        (item_slot_eq, "itm_athelas_reward", slot_item_is_active, 1),
		(store_current_hours, ":now_hours"),
		(item_get_slot, ":expiration_hours", "itm_athelas_reward", slot_item_deactivation_hour),
		(le, ":expiration_hours", ":now_hours"),
		(item_set_slot, "itm_athelas_reward", slot_item_is_active, 0),
        (troop_get_inventory_capacity, ":capacity", "trp_player"),
        (try_for_range, ":cur_slot", 0, ":capacity"),
            (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
            (eq, ":cur_item", "itm_athelas_reward"),
            (troop_inventory_slot_get_item_amount, ":cur_amount", "trp_player", ":cur_slot"),
            (val_sub, ":cur_amount", 1),
            (troop_inventory_slot_set_item_amount, "trp_player", ":cur_slot", ":cur_amount"),  
            (assign, ":capacity", 0), 
        (try_end),
		(display_message, "@Athelas used up."),
    (try_end),
  ]),
  
  # (35) Consuming food at every 14 hours
  (14,[(eq, "$g_player_is_captive", 0),
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (assign, ":num_men", 0),
      (assign, ":num_orcs", 0), # Use for anyone who eats human flesh
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),        
        (party_stack_get_troop_id, ":troop", "p_main_party",":i_stack"),
        (troop_get_type, reg1, ":troop"),
			(try_begin), #trolls eat 30 times as much. Big bastards.
				(eq, reg1, tf_troll),
				(val_mul, ":stack_size", 30),
			(else_try),
			    (eq, reg1, tf_orc),
				(val_mul, ":stack_size", 3), # GA: orcs eat twice as much, mean little bastards #InVain: Slightly reduce to 1,5, because I added extra consumtion for Warg riders
				(val_div, ":stack_size", 2),
					(try_begin),
						(troop_is_guarantee_horse, ":troop"),
						(val_mul, ":stack_size", 2), #stacks with orc food malus: 1,5+2=3
					(try_end),
			(try_end),
		(val_add, ":num_men", ":stack_size"),	
		
		#Count orcs and trolls for rotten food consumption
        (try_begin),
          (eq|this_or_next, reg1, tf_orc),
		  (eq|this_or_next, reg1, tf_troll),
          (eq|this_or_next, reg1, tf_uruk),
          (eq, reg1, tf_urukhai),
          (val_add, ":num_orcs", ":stack_size"),
        (try_end),
        
      (try_end),
      (val_div, ":num_men", 3),
      (try_begin),
        (eq, ":num_men", 0),
        (val_add, ":num_men", 1),
      (try_end),
      
      (assign, ":consumption_amount", ":num_men"),	  
	  #(assign, reg2, ":consumption_amount"),
	  #(display_message, "@food_consumption: {reg2}"),
      
      (party_get_skill_level, reg0, "p_main_party", "skl_inventory_management"),
      (val_mul, reg0, 5),
      (store_sub, ":consumption_reduce", 100, reg0),
      (val_mul, ":consumption_amount", ":consumption_reduce"),
      (val_div, ":consumption_amount", 100),
      
      (assign, ":no_food_displayed", 0),
      (try_for_range, ":unused", 0, ":consumption_amount"),
        (assign, ":available_food", 0),
        (try_begin),
          (item_set_slot, "itm_horse_meat", slot_item_is_checked, 0),
          (call_script, "script_cf_player_has_item_without_modifier", "itm_horse_meat", imod_rotten),
          (val_add, ":available_food", 1),
        (try_end),
        (try_for_range, ":cur_food", food_begin, food_end),
          (item_set_slot, ":cur_food", slot_item_is_checked, 0),
          (call_script, "script_cf_player_has_item_without_modifier", ":cur_food", imod_rotten),
          
          (try_begin),
            # CC: If your party has human flesh, it only counts as food if orc(s) in party
            # CC: e.g., no more cannibalism.
            (eq, ":cur_food", "itm_human_meat"),
            (gt, ":num_orcs", 0),
            (val_add, ":available_food", 1),
          (else_try),
            (neq, ":cur_food", "itm_human_meat"),
            (val_add, ":available_food", 1),
          (try_end),
        (try_end),
        (try_begin),
          (gt, ":available_food", 0),
          (store_random_in_range, ":selected_food", 0, ":available_food"),
          (call_script, "script_consume_food", ":selected_food"),
        (else_try),
          (eq, ":no_food_displayed", 0),
		  (neq, "$g_fast_mode", 1),
          (display_message, "@Party has nothing to eat!", 0xFF0000),
          (call_script, "script_change_player_party_morale", -3),
          (assign, ":no_food_displayed", 1),
          #NPC companion changes begin
          (try_begin),
            (call_script, "script_party_count_fit_regulars", "p_main_party"),
            (gt, reg0, 0),
            (call_script, "script_objectionable_action", tmt_egalitarian, "str_men_hungry"),
          (try_end),
          #NPC companion changes end
        (try_end),
      (try_end),
      
      #Update Savegame for Horse Meat
      (try_begin),
        (lt, "$savegame_version", 6),
        (call_script, "script_update_savegame"),
      (try_end),
  ]),
  
  # (36) Setting item modifiers for food & Cannibalism Trigger (Kham)
  (24,[(troop_get_inventory_capacity, ":inv_size", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
        (eq, ":item_id", "itm_cattle_meat"),
        (troop_get_inventory_slot_modifier, ":modifier", "trp_player", ":i_slot"),
        (try_begin),
          (ge, ":modifier", imod_fresh),
          (lt, ":modifier", imod_rotten),
          (val_add, ":modifier", 1),
          (troop_set_inventory_slot_modifier, "trp_player", ":i_slot", ":modifier"),
        (else_try),
          (lt, ":modifier", imod_fresh),
          (troop_set_inventory_slot_modifier, "trp_player", ":i_slot", imod_fresh),
        (try_end),
      (try_end),
  ]),
  
  # (37) Updating player icon in every frame
  (0,[
      
      #Piggyback for item score
      ] + (is_a_wb_trigger==1 and [
        (call_script, "script_init_item_score"),
        ] or []) + [
      
      (troop_get_inventory_slot, ":cur_horse", "trp_player", ek_horse), #horse slot
      # determine if archer or not
      
      (try_begin),
        (troop_get_inventory_slot, reg5, "trp_player", ek_item_0),(val_max, reg5, 0),(item_get_type, reg5,reg5),
        (assign, ":archer", 0),(neg|is_between, reg5, itp_type_one_handed_wpn, itp_type_polearm +1),
        (assign, ":archer", 1),(neg|is_between, reg5, itp_type_bow, itp_type_crossbow+1),
        (troop_get_inventory_slot, reg5, "trp_player", ek_item_1),(val_max, reg5, 0),(item_get_type, reg5,reg5),
        (assign, ":archer", 0),(neg|is_between, reg5, itp_type_one_handed_wpn, itp_type_polearm +1),
        (assign, ":archer", 1),(neg|is_between, reg5, itp_type_bow, itp_type_crossbow+1),
        (troop_get_inventory_slot, reg5, "trp_player", ek_item_2),(val_max, reg5, 0),(item_get_type, reg5,reg5),
        (assign, ":archer", 0),(neg|is_between, reg5, itp_type_one_handed_wpn, itp_type_polearm +1),
        (assign, ":archer", 1),(neg|is_between, reg5, itp_type_bow, itp_type_crossbow+1),
        (troop_get_inventory_slot, reg5, "trp_player", ek_item_3),(val_max, reg5, 0),(item_get_type, reg5,reg5),
        (assign, ":archer", 0),(neg|is_between, reg5, itp_type_one_handed_wpn, itp_type_polearm +1),
        (assign, ":archer", 1),(neg|is_between, reg5, itp_type_bow, itp_type_crossbow+1),
        (assign, ":archer", 0),
      (try_end),
      (assign, ":new_icon", -1),
      
      (try_begin),
        (eq, "$g_player_icon_state", pis_normal),
        (try_begin), (ge, ":cur_horse", 0), (assign, ":new_icon", "$g_player_icon_mounted"),
        (else_try),
          (try_begin),(ge, ":archer", 1), (assign, ":new_icon", "$g_player_icon_foot_archer"),
          (else_try),					(assign, ":new_icon", "$g_player_icon_foot_melee"),
          (try_end),
        (try_end),
      (else_try),
        (eq, "$g_player_icon_state", pis_camping),
        (assign, ":new_icon", "icon_camp"),
      (else_try),
        (eq, "$g_player_icon_state", pis_ship),
        (assign, ":new_icon", "icon_ship"),
      (try_end),
      (neq, ":new_icon", "$g_player_party_icon"),
      (assign, "$g_player_party_icon", ":new_icon"),
      (party_set_icon, "p_main_party", ":new_icon"),
      
  ]),
  
  # (38) Update how good a target player is for bandits
  (2,[(store_troop_gold, ":total_value", "trp_player"),
      (store_div, ":bandit_attraction", ":total_value", (10000/100)), #10000 gold = excellent_target
      
      (troop_get_inventory_capacity, ":inv_size", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
        (ge, ":item_id", 0),
        (try_begin),
          (is_between, ":item_id", trade_goods_begin, trade_goods_end),
          (store_item_value, ":item_value", ":item_id"),
          (val_add, ":total_value", ":item_value"),
        (try_end),
      (try_end),
      (val_clamp, ":bandit_attraction", 0, 100),
      (party_set_bandit_attraction, "p_main_party", ":bandit_attraction"),
  ]),
  
  # (39) Setting random walker types
  (36,[(try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
        (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
        (             party_slot_eq, ":center_no", slot_party_type, spt_village),
        (call_script, "script_center_remove_walker_type_from_walkers", ":center_no", walkert_needs_money),
        (call_script, "script_center_remove_walker_type_from_walkers", ":center_no", walkert_needs_money_helped),
        (store_random_in_range, ":rand", 0, 100),
        (try_begin),
          (lt, ":rand", 70),
          (neg|party_slot_ge, ":center_no", slot_town_prosperity, 60),
          (call_script, "script_cf_center_get_free_walker", ":center_no"),
          (call_script, "script_center_set_walker_to_type", ":center_no", reg0, walkert_needs_money),
        (try_end),
      (try_end),
  ]),
  
  # Checking center upgrades
  # (12,
  # [(try_for_range, ":center_no", centers_begin, centers_end),
  # (party_is_active, ":center_no"), #TLD
  # (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
  # (party_get_slot, ":cur_improvement", ":center_no", slot_center_current_improvement),
  # (gt, ":cur_improvement", 0),
  # (party_get_slot, ":cur_improvement_end_time", ":center_no", slot_center_improvement_end_hour),
  # (store_current_hours, ":cur_hours"),
  # (ge, ":cur_hours", ":cur_improvement_end_time"),
  # (party_set_slot, ":center_no", ":cur_improvement", 1),
  # (party_set_slot, ":center_no", slot_center_current_improvement, 0),
  # (call_script, "script_get_improvement_details", ":cur_improvement"),
  # (try_begin),
  # (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
  # (str_store_party_name, s4, ":center_no"),
  # (display_log_message, "@Building of {s0} in {s4} has been completed."),
  # (try_end),
  # (try_end),
  # ]),
  
  # (40) Taking denars from player while resting in not owned centers
  (1,[(neg|map_free),
      (is_currently_night),
      (ge, "$g_last_rest_center", 0),
      (neg|party_slot_eq, "$g_last_rest_center", slot_town_lord, "trp_player"),
      (store_current_hours, ":cur_hours"),
      (ge, ":cur_hours", "$g_last_rest_payment_until"),
      (store_add, "$g_last_rest_payment_until", ":cur_hours", 24),
      (store_troop_gold, ":gold", "trp_player"),
      (party_get_num_companions, ":num_men", "p_main_party"),
      (store_div, ":total_cost", ":num_men", 4),
      (val_add, ":total_cost", 1),
      (try_begin),
        (ge, ":gold", ":total_cost"),
        (display_message, "@You pay for accommodation."),
        (troop_remove_gold, "trp_player", ":total_cost"),
      (else_try),
        (gt, ":gold", 0),
        (troop_remove_gold, "trp_player", ":gold"),
      (try_end),
  ]),
  
  # (41) Spawn some bandits 
  (24,[
      (call_script, "script_spawn_bandits"), ## Kham Edit - 24 hours instead of 36, to give player a bit more bandits to fight pre-war.
      
  ]),
  
  # (42) Make parties larger as game progresses.
  (24,[(call_script, "script_update_party_creation_random_limits")]),
  
  # (43) Removing cattle herds if they are way out of range
  (12,[(try_for_parties, ":cur_party"),
        (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
        (party_is_active, ":cur_party"),
        (store_distance_to_party_from_party, ":dist",":cur_party", "p_main_party"),
        (try_begin),
          (gt, ":dist", 30),
          (call_script, "script_safe_remove_party", ":cur_party"),
          (try_begin),
            #Fail quest if the party is the quest party
            (check_quest_active, "qst_move_cattle_herd"),
            (neg|check_quest_concluded, "qst_move_cattle_herd"),
            (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
            (call_script, "script_fail_quest", "qst_move_cattle_herd"),
          (try_end),
        (else_try),
          (gt, ":dist", 10),
          (party_set_slot, ":cur_party", slot_cattle_driven_by_player, 0),
          (party_set_ai_behavior, ":cur_party", ai_bhvr_hold),
        (try_end),
      (try_end),
  ]),
  
  # Quest triggers:
  
  # (44) capture troll quest (mtarini)
  # if the quest is active, add a wild troll party every now and then, up to two.
  (2,[(check_quest_active, "qst_capture_troll"),
      (neg|check_quest_concluded, "qst_capture_troll"),
      (store_distance_to_party_from_party, reg10, "p_town_troll_cave", "p_main_party"), (lt, reg10, 20),
      (store_num_parties_of_template, ":count", "pt_wild_troll"), (val_mul,":count",85),
      (store_random_in_range,":die_roll",0,100),(ge,":die_roll",":count"), # if (die_roll(100)>numtrolls*85)
      (set_spawn_radius,1),
      (spawn_around_party,"p_town_troll_cave","pt_wild_troll"),
  ]),
  
  # (45) kill troll quest: if troll dies on its own, cancel quest (mtarini)
  (5,[(check_quest_active, "qst_kill_troll"),
      (neg|check_quest_concluded, "qst_kill_troll"),
      (quest_get_slot, ":quest_target_party", "qst_kill_troll", slot_quest_target_party),
      (neg|party_is_active, ":quest_target_party"),
      (quest_get_slot, ":quest_object_center", "qst_kill_troll", slot_quest_object_center),
      (str_store_party_name,s2,":quest_object_center"),
      (display_message, "@The troll outside {s2} was killed. Mission canceled."),
      (call_script, "script_cancel_quest", "qst_kill_troll"),
  ]),
  
  # (46) Remaining days text update
  (24,[(try_for_range, ":cur_quest", all_quests_begin, all_quests_end),
        (try_begin),
          (check_quest_active, ":cur_quest"),
          (try_begin),
            (quest_get_slot, ":troop_no", ":cur_quest", slot_quest_giver_troop),
            (try_begin),
              (gt, ":troop_no", 0),
              (troop_slot_eq, ":troop_no", slot_troop_wound_mask, wound_death), # Is the troop dead?
              (str_store_troop_name, s1, ":troop_no"),
              (display_message, "@{s1} was killed on the battlefield. Mission canceled.", color_bad_news),
              (call_script, "script_cancel_quest", ":cur_quest", 1),
            (try_end),
            (try_begin),
              (check_quest_active, ":cur_quest"),
              (quest_get_slot, ":troop_no", ":cur_quest", slot_quest_giver_troop),
              (gt, ":troop_no", 0),
              (store_troop_faction, ":fac", ":troop_no"),
              (faction_slot_eq, ":fac", slot_faction_state, sfs_defeated),
              (str_store_faction_name, s1, ":fac"),
              (display_message, "@{s1} has been defeated. Mission canceled.", color_bad_news),
              (try_begin),
                (eq, ":cur_quest", "qst_mirkwood_sorcerer"),
                (disable_party, "p_ancient_ruins"),
              (try_end),
              (call_script, "script_abort_quest", ":cur_quest", 1),
            (try_end),
          (try_end),
          (try_begin),
            (neg|check_quest_concluded, ":cur_quest"),
            (quest_slot_ge, ":cur_quest", slot_quest_expiration_days, 1),
            (quest_get_slot, ":exp_days", ":cur_quest", slot_quest_expiration_days),
            (val_sub, ":exp_days", 1),
            (try_begin),
              (eq, ":exp_days", 0),
              (try_begin),
                (eq, ":cur_quest", "qst_mirkwood_sorcerer"), # (CppCoder) Disable the ruins party if you fail the sorcerer quest.
                (disable_party, "p_ancient_ruins"),
                (call_script, "script_fail_quest", ":cur_quest"),
              (else_try),
                (eq, ":cur_quest", "qst_defend_village"),
                (call_script, "script_safe_remove_party", "$qst_defend_village_party"),
                (call_script, "script_fail_quest", ":cur_quest"),
              (else_try),
                (eq, ":cur_quest", "qst_guardian_party_quest"),
                (call_script, "script_cf_isengard_guardian_quest_fail"),
              (else_try),
                (eq, ":cur_quest", "qst_raid_village"),
                (call_script, "script_safe_remove_party", "$qst_raid_village_party"),
                (call_script, "script_fail_quest", ":cur_quest"),
              (else_try),
                (eq, ":cur_quest", "qst_destroy_scout_camp"),
                (call_script,"script_destroy_scout_camp_consequences",0),
                (call_script, "script_safe_remove_party", "$qst_destroy_scout_camp_party"),
                (call_script, "script_abort_quest", ":cur_quest",2),
                (call_script, "script_end_quest",":cur_quest"),
              (else_try),
                (call_script, "script_abort_quest", ":cur_quest", 1),
              (try_end),
            (else_try),
              (quest_set_slot, ":cur_quest", slot_quest_expiration_days, ":exp_days"),
              (assign, reg0, ":exp_days"),
              (add_quest_note_from_sreg, ":cur_quest", 7, "@You have {reg0} days to finish this quest.", 0),
            (try_end),
          (try_end),
        (else_try),
          (quest_slot_ge, ":cur_quest", slot_quest_dont_give_again_remaining_days, 1),
          (quest_get_slot, ":value", ":cur_quest", slot_quest_dont_give_again_remaining_days),
          (val_sub, ":value", 1),
          (quest_set_slot, ":cur_quest", slot_quest_dont_give_again_remaining_days, ":value"),
        (try_end),
      (try_end),
  ]),
  
  # (47) Report to army quest #MV: make it more rare?, was 6
  (12,[(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
      (neq, "$g_fast_mode", 1),
	  (eq, "$g_player_is_captive", 0),
      (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
      (neg|check_quest_active, "qst_report_to_army"),
      (neg|check_quest_active, "qst_follow_army"),
      (neg|check_quest_active, "qst_guardian_party_quest"), #not during story quests      
      (neg|quest_slot_ge, "qst_report_to_army", slot_quest_dont_give_again_remaining_days, 1),
      (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
      (gt, ":faction_marshall", 0),
      (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
      (gt, ":faction_marshall_party", 0),
      (assign, ":has_no_quests", 1),
      (try_for_range, ":cur_quest", lord_quests_begin, lord_quests_end),
        (check_quest_active, ":cur_quest"),
        (quest_slot_eq, ":cur_quest", slot_quest_giver_troop, ":faction_marshall"),
        (assign, ":has_no_quests", 0),
      (try_end),
      (eq, ":has_no_quests", 1),
      (try_for_range, ":cur_quest", army_quests_begin, army_quests_end),
        (check_quest_active, ":cur_quest"),
        (assign, ":has_no_quests", 0),
      (try_end),
      (eq, ":has_no_quests", 1),
      (store_character_level, ":level", "trp_player"),
      (ge, ":level", 8),
      (assign, ":cur_target_amount", 2),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (party_is_active, ":cur_center"), #TLD
        (party_slot_eq, ":cur_center", slot_center_destroyed, 0), #TLD
        (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
        (try_begin),
          (party_slot_eq, ":cur_center", slot_party_type, spt_town),
          (val_add, ":cur_target_amount", 3),
        (else_try),
          (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
          (val_add, ":cur_target_amount", 1),
        (else_try),
          (val_add, ":cur_target_amount", 1),
        (try_end),
      (try_end),
      (val_mul, ":cur_target_amount", 4),
      (val_min, ":cur_target_amount", 60),
      (quest_set_slot, "qst_report_to_army", slot_quest_giver_troop, ":faction_marshall"),
      (quest_set_slot, "qst_report_to_army", slot_quest_target_troop, ":faction_marshall"),
      (quest_set_slot, "qst_report_to_army", slot_quest_target_amount, ":cur_target_amount"),
      (quest_set_slot, "qst_report_to_army", slot_quest_expiration_days, 4),
      (quest_set_slot, "qst_report_to_army", slot_quest_dont_give_again_period, 28),
      (jump_to_menu, "mnu_kingdom_army_quest_report_to_army"),
      
  ]),
  
  
  # (48) Army quest initializer
  (3,[(assign, "$g_random_army_quest", -1),
      (check_quest_active, "qst_follow_army", 1),
      (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
      #Rebellion changes begin
      #     (neg|is_between, "$players_kingdom", rebel_factions_begin, rebel_factions_end),
      #Rebellion changes end
      (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
      (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
      (neq, ":faction_marshall", "trp_player"),
      (gt, ":faction_marshall", 0),
      (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
      (gt, ":faction_marshall_party", 0),
      (store_distance_to_party_from_party, ":dist", ":faction_marshall_party", "p_main_party"),
      (try_begin),
        (lt, ":dist", 15),
        (assign, "$g_player_follow_army_warnings", 0),
        (store_current_hours, ":cur_hours"),
        (faction_get_slot, ":last_offensive_time", "$players_kingdom", slot_faction_ai_last_offensive_time),
        (store_sub, ":passed_time", ":cur_hours", ":last_offensive_time"),
        
        (assign, ":result", -1),
        (try_begin),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", 30),
          (troop_slot_eq, ":faction_marshall", slot_troop_does_not_give_quest, 0),
          (try_for_range, ":unused", 0, 20), #Repeat trial twenty times
            (eq, ":result", -1),
            (store_random_in_range, ":quest_no", army_quests_begin, army_quests_end),
            (neg|quest_slot_ge, ":quest_no", slot_quest_dont_give_again_remaining_days, 1),
            (try_begin),
              (eq, ":quest_no", "qst_deliver_cattle_to_army"),
              (try_begin),
                (faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_attacking_center),
                (gt, ":passed_time", 120),#5 days
                (store_random_in_range, ":quest_target_amount", 5, 10),
                (assign, ":result", ":quest_no"),
                (store_random_in_range, ":random_food", normal_food_begin, food_end),
                (quest_set_slot, ":result", slot_quest_target_item, ":random_food"),
                (quest_set_slot, ":result", slot_quest_target_amount, ":quest_target_amount"),
                (quest_set_slot, ":result", slot_quest_expiration_days, 10),
                (quest_set_slot, ":result", slot_quest_dont_give_again_period, 30),
              (try_end),
            (else_try),
              (eq, ":quest_no", "qst_join_siege_with_army"),
              (try_begin),
                (faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_attacking_center),
                (faction_get_slot, ":ai_object", "$players_kingdom", slot_faction_ai_object),
                (is_between, ":ai_object", centers_begin, centers_end),
                (party_get_battle_opponent, ":besieged_center", ":faction_marshall_party"),
                (eq, ":besieged_center", ":ai_object"),
                #army is assaulting the center
                (assign, ":result", ":quest_no"),
                (quest_set_slot, ":result", slot_quest_target_center, ":ai_object"),
                (quest_set_slot, ":result", slot_quest_expiration_days, 2),
                (quest_set_slot, ":result", slot_quest_dont_give_again_period, 15),
              (try_end),
            (else_try),
              (eq, ":quest_no", "qst_scout_waypoints"),
              (try_begin),
                (assign, ":end_cond", 100),
                (assign, "$qst_scout_waypoints_wp_1", -1),
                (assign, "$qst_scout_waypoints_wp_2", -1),
                (assign, "$qst_scout_waypoints_wp_3", -1),
                (assign, ":continue", 0),
                (try_for_range, ":unused", 0, ":end_cond"),
                  (try_begin),
                    (lt, "$qst_scout_waypoints_wp_1", 0),
                    (call_script, "script_cf_get_random_enemy_center_within_range", ":faction_marshall_party", 50),
                    (assign, "$qst_scout_waypoints_wp_1", reg0),
                  (try_end),
                  (try_begin),
                    (lt, "$qst_scout_waypoints_wp_2", 0),
                    (call_script, "script_cf_get_random_enemy_center_within_range", ":faction_marshall_party", 50),
                    (neq, "$qst_scout_waypoints_wp_1", reg0),
                    (assign, "$qst_scout_waypoints_wp_2", reg0),
                  (try_end),
                  (try_begin),
                    (lt, "$qst_scout_waypoints_wp_3", 0),
                    (call_script, "script_cf_get_random_enemy_center_within_range", ":faction_marshall_party", 50),
                    (neq, "$qst_scout_waypoints_wp_1", reg0),
                    (neq, "$qst_scout_waypoints_wp_2", reg0),
                    (assign, "$qst_scout_waypoints_wp_3", reg0),
                  (try_end),
                  (neq, "$qst_scout_waypoints_wp_1", "$qst_scout_waypoints_wp_2"),
                  (neq, "$qst_scout_waypoints_wp_1", "$qst_scout_waypoints_wp_2"),
                  (neq, "$qst_scout_waypoints_wp_2", "$qst_scout_waypoints_wp_3"),
                  (ge, "$qst_scout_waypoints_wp_1", 0),
                  (ge, "$qst_scout_waypoints_wp_2", 0),
                  (ge, "$qst_scout_waypoints_wp_3", 0),
                  (assign, ":end_cond", 0),
                  (assign, ":continue", 1),
                (try_end),
                (eq, ":continue", 1),
                (assign, "$qst_scout_waypoints_wp_1_visited", 0),
                (assign, "$qst_scout_waypoints_wp_2_visited", 0),
                (assign, "$qst_scout_waypoints_wp_3_visited", 0),
                (assign, ":result", ":quest_no"),
                (quest_set_slot, ":result", slot_quest_expiration_days, 7),
                (quest_set_slot, ":result", slot_quest_dont_give_again_period, 25),
              (try_end),
            (try_end),
          (try_end),
          (try_begin),
            (neq, ":result", -1),
            # (str_store_quest_name, s7, ":result"),
            # (display_log_message, "@DEBUG: Getting marshall quest: {s7}."),
            (quest_set_slot, ":result", slot_quest_current_state, 0),
            (quest_set_slot, ":result", slot_quest_giver_troop, ":faction_marshall"),
            (try_begin),
              (eq, ":result", "qst_join_siege_with_army"),
              (jump_to_menu, "mnu_kingdom_army_quest_join_siege_order"),
            (else_try),
              (assign, "$g_random_army_quest", ":result"),
              (quest_set_slot, "$g_random_army_quest", slot_quest_giver_troop, ":faction_marshall"),
              (jump_to_menu, "mnu_kingdom_army_quest_messenger"),
            (try_end),
          (try_end),
        (try_end),
      (else_try),
        (val_add, "$g_player_follow_army_warnings", 1),
        (try_begin),
          (lt, "$g_player_follow_army_warnings", 12),
          (try_begin),
            (store_mod, ":follow_mod", "$g_player_follow_army_warnings", 4),
            (eq, ":follow_mod", 0),
            (str_store_troop_name_link, s1, ":faction_marshall"),
            (try_begin),
              (lt, "$g_player_follow_army_warnings", 8),
              (display_message, "@You must follow {s1}!"),
            (else_try),
              (display_message, "@You must follow {s1}! This is your last warning!"),
            (try_end),
          (try_end),
        (else_try),
          (jump_to_menu, "mnu_kingdom_army_follow_failed"),
        (try_end),
      (try_end),
  ]),
  
  # (49) Move cattle herd + update eliminate patrols quest + update Oath Kills + update Targeted Kills
  (0.5,[
      (try_begin),
        (check_quest_active,"qst_move_cattle_herd"),
        (neg|check_quest_concluded,"qst_move_cattle_herd"),
        (quest_get_slot, ":target_party", "qst_move_cattle_herd", slot_quest_target_party),
        (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
        (try_begin),
          (neg|party_is_active, ":target_party"),
          (call_script, "script_fail_quest", "qst_move_cattle_herd"),
        (else_try),
          (store_distance_to_party_from_party, ":dist",":target_party", ":target_center"),
          (lt, ":dist", 3),
          (call_script, "script_safe_remove_party", ":target_party"),
          (call_script, "script_succeed_quest", "qst_move_cattle_herd"),
        (try_end),
      (try_end),
      
      #eliminate patrols quest - keep the count in the quest notes
      #not in the victory menus because parties are still not defeated then
      (try_begin),
        (check_quest_active, "qst_eliminate_patrols"),
        (neg|check_quest_concluded, "qst_eliminate_patrols"),
        (quest_get_slot, ":quest_target_party_template", "qst_eliminate_patrols", slot_quest_target_party_template),
        (quest_get_slot, ":quest_target_faction", "qst_eliminate_patrols", slot_quest_target_faction),
        (try_begin),
          (neg|faction_slot_eq, ":quest_target_faction", slot_faction_state, sfs_active),
          (call_script, "script_succeed_quest", "qst_eliminate_patrols"),
          (quest_get_slot, ":to_destroy", "qst_eliminate_patrols", slot_quest_target_amount),
          (quest_set_slot, "qst_eliminate_patrols",slot_quest_current_state, ":to_destroy"),
        (else_try),
          #Kham - Eliminate Patrols Refactor START
          #(store_num_parties_destroyed_by_player, ":num_destroyed", ":quest_target_party_template"),
          #(party_template_get_slot, ":previous_num_destroyed", ":quest_target_party_template", slot_party_template_num_killed),
          #(store_sub, ":parties_defeated", ":num_destroyed", ":previous_num_destroyed"),
          #(assign, reg1, ":parties_defeated"),
          (quest_slot_eq, "qst_eliminate_patrols", slot_quest_target_troop, ":quest_target_party_template"), #Check if last enemy party attacked was target (set in mnu_total_victory)
          (quest_get_slot,":current_defeated", "qst_eliminate_patrols", slot_quest_current_state), #Check how many player has defeated
          (store_add, ":total_defeated",":current_defeated",1), #Add one
          (try_begin),
            (quest_slot_eq, "qst_eliminate_patrols", slot_quest_target_troop, ":quest_target_party_template"),
            (gt, ":quest_target_party_template", 0),
            (set_spawn_radius,1),
            (spawn_around_party, "p_main_party",":quest_target_party_template"),
            (assign, ":spawn", reg0),
            (str_store_party_name, s1, ":spawn"),
            (call_script, "script_safe_remove_party", ":spawn"),
          (try_end),
          (quest_set_slot, "qst_eliminate_patrols", slot_quest_target_troop, 0), #Revert back to 0 state for target troop until encountered again
          (quest_set_slot, "qst_eliminate_patrols", slot_quest_current_state, ":total_defeated"), #Set # of troops defeated
          (assign, reg1, ":total_defeated"),
          (quest_get_slot, ":amount", "qst_eliminate_patrols", slot_quest_target_amount), #Keep track of target
          (assign, reg2,":amount"),
          (val_add, ":amount", 1),
          (val_clamp, ":total_defeated", 0,":amount"),
          
          (try_begin),
            (eq, "$cheat_mode",1),
            (assign, reg0, ":current_defeated"),
            (display_message, "@DEBUG: Eliminate Parties - Current: {reg0}, New: {reg1}"),
          (try_end),
          #Kham - Eliminate Patrols Refactor END
          (str_store_string, s2, "@{s1} parties defeated: {reg1} out of {reg2}"),
          (add_quest_note_from_sreg, "qst_eliminate_patrols", 3, s2, 0),
        (try_end),
      (try_end),
      
      #Report number of kills for the oath of vengeance quest
      (try_begin),
        (check_quest_active, "qst_oath_of_vengeance"),
        #(neg|check_quest_concluded, "qst_oath_of_vengeance"),
        (quest_get_slot, ":target","qst_oath_of_vengeance", 2),
        (str_store_faction_name, s3, ":target"),
        (assign, reg65, "$oath_kills"),
        (try_begin),
          (quest_slot_ge, "qst_oath_of_vengeance", 7, 1),
          (str_store_string, s4, "@{reg65} Moria and/or Gundabad troops killed. (Counter refreshes every hour)"),
        (else_try),
          (str_store_string, s4, "@{reg65} {s3} troops killed. (Counter refreshes every hour)"),
        (try_end),
        (add_quest_note_from_sreg, "qst_oath_of_vengeance", 2, s4, 0),
      (try_end),
      
      #Report number of kills for the kill quest
      (try_begin),
        (check_quest_active, "qst_blank_quest_05"),
        #(neg|check_quest_concluded, "qst_blank_quest_05"),
        (quest_get_slot, ":target_faction", "qst_blank_quest_05", slot_quest_target_faction),
        (quest_get_slot, ":current_amount", "qst_blank_quest_05", slot_quest_current_state),
        (str_clear, s5),
        (str_store_faction_name, s5, ":target_faction"),
        (assign, reg66, ":current_amount"),
        (str_store_string, s6, "@{reg66} {s5} troops killed. (Counter refreshes every hour)"),
        (add_quest_note_from_sreg, "qst_blank_quest_05", 2, s6, 0),
      (else_try),
        (check_quest_active, "qst_blank_quest_05"),
        (neg|check_quest_concluded, "qst_blank_quest_05"),
        (quest_get_slot, ":target_faction", "qst_blank_quest_05", slot_quest_target_faction),
        (faction_get_slot, ":target_active", ":target_faction", slot_faction_state),
        (eq, ":target_active", sfs_defeated),
        (call_script, "script_succeed_quest", "qst_blank_quest_05"),
      (try_end),
      
      #Report number of kills for the targeted kill quest
      (try_begin),
        (check_quest_active, "qst_blank_quest_04"),
        #(neg|check_quest_concluded, "qst_blank_quest_04"),
        (quest_get_slot, ":target_faction", "qst_blank_quest_04", slot_quest_target_faction),
        (quest_get_slot, ":target_troop", "qst_blank_quest_04", slot_quest_target_troop),
        (quest_get_slot, ":current_amount", "qst_blank_quest_04", slot_quest_current_state),
        (str_clear, s7),
        (str_store_faction_name, s7, ":target_faction"),
        (str_store_troop_name, s8, ":target_troop"),
        (assign, reg67, ":current_amount"),
        (str_store_string, s9, "@{reg67} {s7} {s8} troops killed. (Counter refreshes every hour)"),
        (add_quest_note_from_sreg, "qst_blank_quest_04", 2, s9, 0),
      (else_try),
        (check_quest_active, "qst_blank_quest_04"),
        (neg|check_quest_concluded, "qst_blank_quest_04"),
        (quest_get_slot, ":target_faction", "qst_blank_quest_04", slot_quest_target_faction),
        (faction_get_slot, ":target_active", ":target_faction", slot_faction_state),
        (eq, ":target_active", sfs_defeated),
        (call_script, "script_succeed_quest", "qst_blank_quest_04"),
      (try_end),
      
      #Report number of kills for the bandit kill quest
      (try_begin),
        (check_quest_active, "qst_blank_quest_17"),
        #(neg|check_quest_concluded, "qst_blank_quest_17"),
        (quest_get_slot, ":target_troop", "qst_blank_quest_17", slot_quest_target_troop),
        (quest_get_slot, ":current_amount", "qst_blank_quest_17", slot_quest_current_state),
        (quest_get_slot, ":quest_giver", "qst_blank_quest_17", slot_quest_giver_troop),
        (str_store_troop_name, s8, ":quest_giver"),
        (quest_get_slot, ":quest_giver_center", "qst_blank_quest_17", slot_quest_target_center),
        (str_store_party_name, s9, ":quest_giver_center"),
        (quest_get_slot, reg67, "qst_blank_quest_17", slot_quest_target_amount),
        (str_store_troop_name_by_count, s10, ":target_troop", reg67),
         #(str_store_troop_name, s10, ":target_troop"),
        (str_store_troop_name_by_count, s11, ":target_troop", ":current_amount"),
        (assign, reg68, ":current_amount"),
        (str_store_string, s11, "@{s8} in {s9} asked you to slay {reg67} {s10}.^ {reg68} {s11} killed. (Counter refreshes every hour)"),
        (add_quest_note_from_sreg, "qst_blank_quest_17", 2, s11, 0),
      (try_end),
      
      
  ]),
  # (50)
  (2,[(try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (ge, ":party_no", 1),
        (party_is_active, ":party_no"),
        (party_slot_eq, ":party_no", slot_party_following_player, 1),
        (store_current_hours, ":cur_time"),
        (neg|party_slot_ge, ":party_no", slot_party_follow_player_until_time, ":cur_time"),
        (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (party_set_slot, ":party_no", slot_party_following_player, 0),
        (assign,  ":dont_follow_period", 48), #MV was 200
        (store_add, ":dont_follow_time", ":cur_time", ":dont_follow_period"),
        (party_set_slot, ":party_no", slot_party_dont_follow_player_until_time,  ":dont_follow_time"),
      (try_end),
  ]),
  
  # Deliver cattle and deliver cattle to army
  # (0.5,[
  # (try_begin),
  # (check_quest_active,"qst_deliver_cattle"),
  # (neg|check_quest_succeeded, "qst_deliver_cattle"),
  # (quest_get_slot, ":target_center", "qst_deliver_cattle", slot_quest_target_center),
  # (quest_get_slot, ":target_amount", "qst_deliver_cattle", slot_quest_target_amount),
  # (quest_get_slot, ":cur_amount", "qst_deliver_cattle", slot_quest_current_state),
  # (store_sub, ":left_amount", ":target_amount", ":cur_amount"),
  # (call_script, "script_remove_cattles_if_herd_is_close_to_party", ":target_center", ":left_amount"),
  # (val_add, ":cur_amount", reg0),
  # (quest_set_slot, "qst_deliver_cattle", slot_quest_current_state, ":cur_amount"),
  # (le, ":target_amount", ":cur_amount"),
  # (call_script, "script_succeed_quest", "qst_deliver_cattle"),
  # (try_end),
  # (try_begin),
  # (check_quest_active, "qst_deliver_cattle_to_army"),
  # (neg|check_quest_succeeded, "qst_deliver_cattle_to_army"),
  # (quest_get_slot, ":giver_troop", "qst_deliver_cattle_to_army", slot_quest_giver_troop),
  # (troop_get_slot, ":target_party", ":giver_troop", slot_troop_leaded_party),
  # (try_begin),
  # (gt, ":target_party", 0),
  # (quest_get_slot, ":target_amount", "qst_deliver_cattle_to_army", slot_quest_target_amount),
  # (quest_get_slot, ":cur_amount", "qst_deliver_cattle_to_army", slot_quest_current_state),
  # (store_sub, ":left_amount", ":target_amount", ":cur_amount"),
  # (call_script, "script_remove_cattles_if_herd_is_close_to_party", ":target_party", ":left_amount"),
  # (val_add, ":cur_amount", reg0),
  # (quest_set_slot, "qst_deliver_cattle_to_army", slot_quest_current_state, ":cur_amount"),
  # (try_begin),
  # (le, ":target_amount", ":cur_amount"),
  # (call_script, "script_succeed_quest", "qst_deliver_cattle_to_army"),
  # (try_end),
  # (else_try),
  # (call_script, "script_abort_quest", "qst_deliver_cattle_to_army", 0),
  # (try_end),
  # (try_end),
  # ]),
  
  # Train peasants against bandits
  # (1,[
  # (neg|map_free),
  # (check_quest_active, "qst_train_peasants_against_bandits"),
  # (neg|check_quest_concluded, "qst_train_peasants_against_bandits"),
  # (eq, "$qst_train_peasants_against_bandits_currently_training", 1),
  # (val_add, "$qst_train_peasants_against_bandits_num_hours_trained", 1),
  # (call_script, "script_get_max_skill_of_player_party", "skl_trainer"),
  # (assign, ":trainer_skill", reg0),
  # (store_sub, ":needed_hours", 20, ":trainer_skill"),
  # (val_mul, ":needed_hours", 3),
  # (val_div, ":needed_hours", 5),
  # (ge, "$qst_train_peasants_against_bandits_num_hours_trained", ":needed_hours"),
  # (assign, "$qst_train_peasants_against_bandits_num_hours_trained", 0),
  # (rest_for_hours, 0, 0, 0), #stop resting
  # (jump_to_menu, "mnu_train_peasants_against_bandits_ready"),
  # ]),
  
  # (51) Scout waypoints
  (1,[(try_begin),
        (check_quest_active,"qst_scout_waypoints"),
        (neg|check_quest_succeeded, "qst_scout_waypoints"),
        (try_begin),
          (eq, "$qst_scout_waypoints_wp_1_visited", 0),
          (store_distance_to_party_from_party, ":distance", "$qst_scout_waypoints_wp_1", "p_main_party"),
          (le, ":distance", 3),
          (assign, "$qst_scout_waypoints_wp_1_visited", 1),
          (str_store_party_name_link, s1, "$qst_scout_waypoints_wp_1"),
          (display_message, "@{s1} is scouted."),
        (try_end),
        (try_begin),
          (eq, "$qst_scout_waypoints_wp_2_visited", 0),
          (store_distance_to_party_from_party, ":distance", "$qst_scout_waypoints_wp_2", "p_main_party"),
          (le, ":distance", 3),
          (assign, "$qst_scout_waypoints_wp_2_visited", 1),
          (str_store_party_name_link, s1, "$qst_scout_waypoints_wp_2"),
          (display_message, "@{s1} is scouted."),
        (try_end),
        (try_begin),
          (eq, "$qst_scout_waypoints_wp_3_visited", 0),
          (store_distance_to_party_from_party, ":distance", "$qst_scout_waypoints_wp_3", "p_main_party"),
          (le, ":distance", 3),
          (assign, "$qst_scout_waypoints_wp_3_visited", 1),
          (str_store_party_name_link, s1, "$qst_scout_waypoints_wp_3"),
          (display_message, "@{s1} is scouted."),
        (try_end),
        (eq, "$qst_scout_waypoints_wp_1_visited", 1),
        (eq, "$qst_scout_waypoints_wp_2_visited", 1),
        (eq, "$qst_scout_waypoints_wp_3_visited", 1),
        (call_script, "script_succeed_quest", "qst_scout_waypoints"),
      (try_end),
      
      (try_begin),
        (check_quest_active,"qst_scout_enemy_town"),
        (neg|check_quest_succeeded, "qst_scout_enemy_town"),
        (quest_get_slot, ":quest_target_center", "qst_scout_enemy_town", slot_quest_target_center),
        (quest_get_slot, ":quest_target_visited", "qst_scout_enemy_town", slot_quest_target_troop),
        (try_begin),
          (eq, ":quest_target_visited", 0),
          (store_distance_to_party_from_party, ":distance", ":quest_target_center", "p_main_party"),
          (le, ":distance", 3),
          (assign, ":quest_target_visited", 1),
          (str_store_party_name_link, s1, ":quest_target_center"),
          (display_message, "@{s1} is scouted."),
        (try_end),
        (eq, ":quest_target_visited", 1),
        (quest_set_slot, "qst_scout_enemy_town", slot_quest_target_troop, ":quest_target_visited"),
        (call_script, "script_succeed_quest", "qst_scout_enemy_town"),
      (try_end),
  ]),
  
  
  # (52) NPC changes begin
  #Resolve one issue each hour
  (1,[(assign, "$npc_map_talk_context", 0),
      (try_begin),
        ### Here do NPC that is quitting
        (gt, "$npc_is_quitting", 0),
        (try_begin),
          (main_party_has_troop, "$npc_is_quitting"),
          (neq, "$g_player_is_captive", 1),
          (start_map_conversation, "$npc_is_quitting"),
        (else_try),
          (assign, "$npc_is_quitting", 0),
        (try_end),
      (else_try),
        #### Grievance
        (gt, "$npc_with_grievance", 0),
        (eq, "$disable_npc_complaints", 0),
        (try_begin),
          (main_party_has_troop, "$npc_with_grievance"),
          (neq, "$g_player_is_captive", 1),
          
          (assign, "$npc_map_talk_context", slot_troop_morality_state),
          (start_map_conversation, "$npc_with_grievance"),
        (else_try),
          (assign, "$npc_with_grievance", 0),
        (try_end),
      (else_try),
        (gt, "$npc_with_personality_clash", 0),
        (eq, "$disable_npc_complaints", 0),
        (troop_get_slot, ":object", "$npc_with_personality_clash", slot_troop_personalityclash_object),
        (try_begin),
          (main_party_has_troop, "$npc_with_personality_clash"),
          (main_party_has_troop, ":object"),
          (neq, "$g_player_is_captive", 1),
          (assign, "$npc_map_talk_context", slot_troop_personalityclash_state),
          (start_map_conversation, "$npc_with_personality_clash"),
        (else_try),
          (assign, "$npc_with_personality_clash", 0),
        (try_end),
      (else_try), ###check for regional background
        (eq, "$disable_local_histories", 0),
        (try_for_range, ":npc", companions_begin, new_companions_end),
          (this_or_next|is_between, ":npc", companions_begin, companions_end),
          (is_between, ":npc", new_companions_begin, new_companions_end),
          (eq, "$npc_map_talk_context", 0),
          (main_party_has_troop, ":npc"),
          (troop_slot_eq, ":npc", slot_troop_home_speech_delivered, 0),
          # (eq, "$npc_map_talk_context", 0),
          (troop_get_slot, ":home", ":npc", slot_troop_home),
          (gt, ":home", 0),
          (store_distance_to_party_from_party, ":distance", ":home", "p_main_party"),
          (lt, ":distance", 7),
          (assign, "$npc_map_talk_context", slot_troop_home),
          (start_map_conversation, ":npc"),
        (try_end),
        (neq, "$npc_map_talk_context", 0), #fail if nothing happened here
      (else_try), ###TLD: complain about NPC's home faction getting demolished
        (try_for_range, ":npc", companions_begin, new_companions_end),
          (this_or_next|is_between, ":npc", companions_begin, companions_end),
          (is_between, ":npc", new_companions_begin, new_companions_end),
          (eq, "$npc_map_talk_context", 0),
          (main_party_has_troop, ":npc"),
          (store_troop_faction, ":npc_faction", ":npc"),
          (faction_slot_eq, ":npc_faction", slot_faction_state, sfs_active),
          
          (faction_get_slot, ":npc_faction_strength", ":npc_faction", slot_faction_strength),
          (lt, ":npc_faction_strength", fac_str_very_weak),
          
          (troop_get_slot, ":last_complaint_hours", ":npc", slot_troop_last_complaint_hours),
          (store_current_hours, ":hours"),
          (val_add, ":last_complaint_hours", 7*24), #complain every 7 days at most
          (gt, ":hours", ":last_complaint_hours"),
          
          (troop_set_slot, ":npc", slot_troop_last_complaint_hours, ":hours"), #reset complaint
          (assign, "$npc_map_talk_context", slot_troop_last_complaint_hours),
          (start_map_conversation, ":npc"),
        (try_end),
      (try_end),
  ]),
  #NPC changes end
  
  ##(1,
  ##   [(store_random_in_range, ":random_troop", kingdom_heroes_begin, kingdom_heroes_end),
  ##    (store_random_in_range, ":random_faction", kingdoms_begin, kingdoms_end),
  ##    (store_troop_faction, ":troop_faction", ":random_troop"),
  ##    (neq, ":troop_faction", ":random_faction"),
  ##    (faction_slot_eq, ":random_faction", slot_faction_state, sfs_active),
  ##    (troop_set_slot, ":random_troop", slot_troop_change_to_faction, ":random_faction"),
  ##    (str_store_troop_name, s1, ":random_troop"),
  ##    (str_store_faction_name, s2, ":troop_faction"),
  ##    (str_store_faction_name, s3, ":random_faction"),
  ##    (display_message, "@{s1} is willing to switch from {s2} to {s3}."),
  ##    ]),
  
  
  # what is this uncommented trigger?
  # seems to be realted to troops changing factions... why?
  # commenting out for now  (mtarini)
  # (4,
  # [(try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
  # (troop_slot_ge, ":troop_no", slot_troop_change_to_faction, 1),
  # (store_troop_faction, ":faction_no", ":troop_no"),
  # (troop_get_slot, ":new_faction_no", ":troop_no", slot_troop_change_to_faction),
  # (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
  # (assign, ":continue", 0),
  # (try_begin),
  # (le, ":party_no", 0),
  # #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
  # (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
  # (assign, ":continue", 1),
  # (else_try),
  # (gt, ":party_no", 0),
  # (party_is_active, ":party_no"), #MV fix
  
  # #checking if the party is outside the centers
  # (party_get_attached_to, ":cur_center_no", ":party_no"),
  # (try_begin),
  # (lt, ":cur_center_no", 0),
  # (party_get_cur_town, ":cur_center_no", ":party_no"),
  # (try_end),
  # (this_or_next|neg|is_between, ":cur_center_no", centers_begin, centers_end),
  # (party_slot_eq, ":cur_center_no", slot_town_lord, ":troop_no"),
  
  # #checking if the party is away from his original faction parties
  # (assign, ":end_cond", kingdom_heroes_end),
  # (try_for_range, ":enemy_troop_no", kingdom_heroes_begin, ":end_cond"),
  # (troop_get_slot, ":enemy_party_no", ":enemy_troop_no", slot_troop_leaded_party),
  # (gt, ":enemy_party_no", 0),
  # (store_faction_of_party, ":enemy_faction_no", ":enemy_party_no"),
  # (eq, ":enemy_faction_no", ":faction_no"),
  # (store_distance_to_party_from_party, ":dist", ":party_no", ":enemy_party_no"),
  # (lt, ":dist", 4),
  # (assign, ":end_cond", 0),
  # (try_end),
  # (neq, ":end_cond", 0),
  # (assign, ":continue", 1),
  # (try_end),
  # (eq, ":continue", 1),
  # (call_script, "script_change_troop_faction", ":troop_no", ":new_faction_no"),
  # (troop_set_slot, ":troop_no", slot_troop_change_to_faction, 0),
  # (try_begin),
  # (is_between, ":new_faction_no", kingdoms_begin, kingdoms_end),
  # (str_store_troop_name_link, s1, ":troop_no"),
  # (str_store_faction_name_link, s2, ":faction_no"),
  # (str_store_faction_name_link, s3, ":new_faction_no"),
  # (display_message, "@{s1} has switched from {s2} to {s3}."),
  # (try_begin),
  # (eq, ":faction_no", "$players_kingdom"),
  # (call_script, "script_add_notification_menu", "mnu_notification_troop_left_players_faction", ":troop_no", ":new_faction_no"),
  # (else_try),
  # (eq, ":new_faction_no", "$players_kingdom"),
  # (call_script, "script_add_notification_menu", "mnu_notification_troop_joined_players_faction", ":troop_no", ":faction_no"),
  # (try_end),
  # (try_end),
  # (try_end),
  # ]),
  
  # (53) Calculate day/night penalties
  (1,[(this_or_next|is_currently_night),
      (eq, "$prev_day", 0),
      (this_or_next|neg|is_currently_night),
      (eq, "$prev_day", 1),
      #debug_point_0,
      (try_begin),
        (neg|is_currently_night),
        (assign, "$prev_day", 1),
        (play_sound, "snd_reload_crossbow_continue"), # rooster at dawn
        (try_for_range, ":troop_id", tld_troops_begin, tld_troops_end),
          (call_script, "script_cf_is_a_night_troop", ":troop_id"), #Night Troops Exceptions
          (troop_get_type, ":troop_type", ":troop_id"),
          (try_begin),
            ]+concatenate_scripts([
              [(eq, ":troop_type", Penalties_sys[x][0]),
                ]+[
                (troop_raise_skill, ":troop_id", Penalties_sys[x][1][y][0], Penalties_sys[x][1][y][1])\
                for y in range(len(Penalties_sys[x][1]))
                ]+concatenate_scripts([
                  [
                    (troop_get_slot, ":pen_prof", ":troop_id", slot_troop_prof_night_penalties_begin+y),
                    (try_begin),
                      (troop_is_hero, ":troop_id"),
                      (lt, ":pen_prof", 0),
                      (store_proficiency_level, ":prof", ":troop_id", Penalties_sys[x][2][y][0]),
                      (val_mul, ":prof", Penalties_sys[x][2][y][1]),
                      (val_div, ":prof", 100),
                      (troop_set_slot, ":troop_id", slot_troop_prof_night_penalties_begin+y, ":prof"),
                      (assign, ":pen_prof", ":prof"),
                    (try_end),
                    (troop_raise_proficiency_linear, ":troop_id", Penalties_sys[x][2][y][0], ":pen_prof"),
                    (try_begin),
                      (troop_is_hero, ":troop_id"),
                      (gt, ":pen_prof", 0),
                      (store_proficiency_level, ":prof", ":troop_id", Penalties_sys[x][2][y][0]),
                      (val_mul, ":prof", Penalties_sys[x][2][y][1]),
                      (val_div, ":prof", 100),
                      (troop_set_slot, ":troop_id", slot_troop_prof_night_penalties_begin+y, ":prof"),
                    (try_end),
                    ] for y in range(len(Penalties_sys[x][2]))
                  ])+[
              (else_try),
                ] for x in range(len(Penalties_sys))
              ])+[
          (try_end),
        (try_end),
      (else_try),
        #debug_point_1,
        (assign, "$prev_day", 0),
        (play_sound, "snd_release_crossbow"), # wolf at dusk
        (try_for_range, ":troop_id", tld_troops_begin, tld_troops_end),
          
          (call_script, "script_cf_is_a_night_troop", ":troop_id"), #Night Troops Exceptions
          
          (troop_get_type, ":troop_type", ":troop_id"),
          (try_begin),
            ]+concatenate_scripts([
              [(eq, ":troop_type", Penalties_sys[x][0]),
                (assign, reg0, ":troop_type"),
                #(display_message, "@DEBUG: Troop type: {reg0}", 0xff00ff),
                ]+[
                (troop_raise_skill, ":troop_id", Penalties_sys[x][1][y][0], -Penalties_sys[x][1][y][1])\
                for y in range(len(Penalties_sys[x][1]))
                ]+concatenate_scripts([
                  [
                    #debug_point_2,
                    (troop_get_slot, ":pen_prof", ":troop_id", slot_troop_prof_night_penalties_begin+y),
                    (val_mul, ":pen_prof", -1),
                    (troop_raise_proficiency_linear, ":troop_id", Penalties_sys[x][2][y][0], ":pen_prof"),
                    ] for y in range(len(Penalties_sys[x][2]))
                  ])+[
              (else_try),
                ] for x in range(len(Penalties_sys))
              ])+[
          (try_end),
        (try_end),
      (try_end),
  ]),
  # TLD triggers end
  #####################################
  
  ## (54) question box (yes/no) on global map
  (ti_question_answered,
    [(store_trigger_param_1,":answer"),
      
      #swy-- add guards, this doesn't seem like it's protected to last, murphy's law! 69 is true in my book!
      (eq, "$do_you_want_to_disembark_called", 69),
      (assign, "$do_you_want_to_disembark_called", -1),
      
      (try_begin),
        (eq,":answer",0), # yes on "Do you want to disembark?" question box
        (assign, "$g_player_icon_state", pis_normal),
        (party_set_flags, "p_main_party", pf_is_ship, 0),
        (party_get_position, pos1, "p_main_party"),
        (map_get_land_position_around_position, pos0, pos1, 1),
        (party_set_position, "p_main_party", pos0),
        (rest_for_hours,0.2,1,1),
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
        (jump_to_menu, "mnu_auto_return_to_map"),
        #(else_try),
        #	(party_get_position, pos1, "p_main_party"),
        #	(map_get_water_position_around_position,pos0,pos1,0.5),
        #	(party_set_position, "p_main_party", pos0),
        #	(party_relocate_near_party,"p_main_party","p_main_party",10),
        #	(party_set_ai_object,"p_main_party", "p_town_minas_tirith"),
      (try_end),
  ]),
  
  # (55) Check if a faction is defeated every 12 hours
  # TLD modified to check for faction strength instead, GA
  (12,[(assign, ":num_active_factions", 0),
      (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
        (val_add, ":num_active_factions", 1),
        #MV for TLD: faction defeat if capital captured
        (faction_get_slot, ":capital", ":cur_kingdom", slot_faction_capital),
        (store_faction_of_party, ":capital_faction", ":capital"),
        
        # Kham - Removed crushed condition and added Last Stand Event

        # (assign, ":has_guardian", 0),
        # (assign, ":guardian_party_defeated", 0),
        # (try_begin),
          # (this_or_next|eq, ":cur_kingdom", "fac_isengard"),
          # (eq, ":cur_kingdom", "fac_woodelf"),
          # (assign, ":has_guardian", 1),
        # (try_end),

        (try_begin),
          #(eq, ":has_guardian", 0),
          (neg|faction_slot_ge, ":cur_kingdom", slot_faction_strength, 1), # TLD or faction strength down
          (faction_slot_eq, ":cur_kingdom", slot_faction_last_stand, 0),
          (faction_set_slot, ":cur_kingdom", slot_faction_last_stand, 1),
          #(str_store_faction_name, s10, ":cur_kingdom"),
          #(display_message, "@DEBUG: {s10} is now in Last Stand mode", color_neutral_news),
        # (else_try),
          # (eq, ":has_guardian", 1),
          # (faction_slot_eq, ":cur_kingdom", slot_faction_guardian_party_spawned, 1), #Guardian party has spawned
          # (faction_get_slot, ":guardian_party", ":cur_kingdom", slot_faction_guardian_party),
          # (neg|party_is_active, ":guardian_party"),
          # (assign, ":guardian_party_defeated", 1),
        (try_end),

        (this_or_next|neq, ":cur_kingdom", ":capital_faction"), # TLD capital captured
        #(this_or_next|eq, ":guardian_party_defeated", 1),
        (neg|party_slot_eq, ":capital", slot_center_destroyed,0), #TLD or capital destroyed

        
        (assign, ":faction_removed", 0),
        (try_begin),
          (eq, ":cur_kingdom", "fac_player_supporters_faction"),
          (try_begin),
            (faction_set_slot, ":cur_kingdom", slot_faction_state, sfs_inactive),
            (assign, ":faction_removed", 1),
          (try_end),
        (else_try),
          #(neq, "$players_kingdom", ":cur_kingdom"), #TLD: player kingdom can be defeated!
          (faction_set_slot, ":cur_kingdom", slot_faction_state, sfs_defeated),
          
          #Send Gandalf on a little chat
          (try_begin), #first good faction falls - good player
            (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
            (faction_slot_eq, ":cur_kingdom", slot_faction_side, faction_side_good),
            (assign, "$g_tld_convo_subject", ":cur_kingdom"),
            (store_and, ":already_done", "$g_tld_conversations_done", tld_conv_bit_gandalf_ally_down),
            (eq, ":already_done", 0),
            (call_script, "script_send_on_conversation_mission", tld_cc_gandalf_ally_down),
          (try_end),
          
          (try_begin), #first evil faction falls - evil player
            (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
            (neg|faction_slot_eq, ":cur_kingdom", slot_faction_side, faction_side_good),
            (neq, "$tld_war_began", 2),
            (assign, "$g_tld_convo_subject", ":cur_kingdom"),
            (store_and, ":already_done", "$g_tld_conversations_done", tld_conv_bit_gandalf_enemy_down),
            (eq, ":already_done", 0),
            (call_script, "script_send_on_conversation_mission", tld_cc_gandalf_enemy_down),
          (try_end),
          
          #TLD: find the strongest enemy faction in the current or home theather, it will receive the centers
          (assign, ":best_strength", 0),
          (assign, ":best_faction", "fac_mordor"), #if no other, Mordor gets all :)
          (faction_get_slot, ":active_theater", ":cur_kingdom", slot_faction_active_theater),
          (faction_get_slot, ":home_theater", ":cur_kingdom", slot_faction_home_theater),
          (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
            (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
            (faction_slot_eq, ":faction_no", slot_faction_home_theater, ":home_theater"), # home theater enemies get to pick first
            (store_relation, ":cur_relation", ":faction_no", ":cur_kingdom"),
            (lt, ":cur_relation", 0), #enemy
            (faction_get_slot, ":faction_strength", ":faction_no", slot_faction_strength),
            (gt, ":faction_strength", ":best_strength"), #better strength
            (assign, ":best_strength", ":faction_strength"),
            (assign, ":best_faction", ":faction_no"),
          (try_end),
          
          (try_begin),
            (eq, ":best_strength", 0),
            (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
              (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
              (this_or_next|faction_slot_eq, ":faction_no", slot_faction_active_theater, ":home_theater"), # if there are no home enemies, check for invaders
              (faction_slot_eq, ":faction_no", slot_faction_active_theater, ":active_theater"),
              (store_relation, ":cur_relation", ":faction_no", ":cur_kingdom"),
              (lt, ":cur_relation", 0), #enemy
              (faction_get_slot, ":faction_strength", ":faction_no", slot_faction_strength),
              (gt, ":faction_strength", ":best_strength"), #better strength
              (assign, ":best_strength", ":faction_strength"),
              (assign, ":best_faction", ":faction_no"),
            (try_end),
          (try_end),
          
          (try_for_parties, ":cur_party"),
            (party_is_active, ":cur_party"),
            (store_faction_of_party, ":party_faction", ":cur_party"),
            (eq, ":party_faction", ":cur_kingdom"),
            # TLD: parties are removed, they don't change faction
            # first detach all attached parties, in case there are some allies (in battle or in center)
            (party_get_num_attached_parties, ":num_attached_parties", ":cur_party"),
            (try_for_range_backwards, ":attached_party_rank", 0, ":num_attached_parties"),
              (party_get_attached_party_with_rank, ":attached_party", ":cur_party", ":attached_party_rank"),
              (gt, ":attached_party", 0),
              (party_is_active, ":attached_party"),
              (party_detach, ":attached_party"),
            (try_end),
            
            (try_begin),
              (neg|is_between, ":cur_party", centers_begin, centers_end),
              
              (try_begin),  # Special case: Destroy Barad-Dur
                (eq,":cur_party","p_town_barad_dur"),
                (party_set_slot,":cur_party",slot_center_destroy_on_capture,2),
                (call_script,"script_destroy_center",":cur_party"),
              (else_try), # General case: remove party
                (call_script, "script_safe_remove_party", ":cur_party"),
              (try_end),
            (else_try),
              # Centers: destroy what you can, give the rest to the best enemy
              #remove any volunteer parties
              (call_script,"script_delete_volunteers_party",":cur_party"),
              #(party_get_slot, ":volunteers", ":cur_party", slot_town_volunteer_pt),
              #(try_begin),
              #  (gt, ":volunteers", 0),
              #  (party_is_active, ":volunteers"),
              #  (party_detach,    ":volunteers"),
              #  (call_script, "script_safe_remove_party",    ":volunteers"),
              #(try_end),
              (try_begin), #TLD: if center destroyable, disable it, otherwise proceed as normal
                (party_slot_ge, ":cur_party", slot_center_destroy_on_capture, 1),
                (call_script, "script_destroy_center", ":cur_party"),
              (else_try),
                (party_clear, ":cur_party"), # remove previous garrison
                # if a center was besieged, give it to the besieger
                (party_get_slot, ":besieger_party", ":cur_party", slot_center_is_besieged_by),
                (try_begin),
                  (gt, ":besieger_party", 0),
                  (party_is_active, ":besieger_party"),
                  (store_faction_of_party, ":besieger_faction", ":besieger_party"),
                  (party_slot_ge, ":cur_party", slot_center_is_besieged_by, 1),
                  (call_script, "script_give_center_to_faction", ":cur_party", ":besieger_faction"),
                  (call_script, "script_lift_siege", ":cur_party", 0),
                (else_try),
                  # if not give it to the best+closest faction in the theater
                  (assign, ":closest_faction", ":best_faction"),
                  (assign, ":closest_score", 0),
                  (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
                    (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
                    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_active_theater, ":home_theater"), # if there are no home enemies, check for invaders
                    (faction_slot_eq, ":faction_no", slot_faction_active_theater, ":active_theater"),
                    (store_relation, ":cur_relation", ":faction_no", ":cur_kingdom"),
                    (lt, ":cur_relation", 0), #enemy
                    (faction_get_slot, ":faction_strength", ":faction_no", slot_faction_strength),
                    (faction_get_slot, ":faction_capital", ":faction_no", slot_faction_capital),
                    (call_script, "script_get_tld_distance", ":cur_party", ":faction_capital"),
                    (assign, ":dist", reg0),
                    #(val_mul, ":dist", ":dist"),
                    (val_min, ":faction_strength", 7000),
                    (val_mul, ":faction_strength", 1000),
                    # score = 1000*str/dist
                    (store_div, ":score", ":faction_strength", ":dist"),
                    # (assign, reg0, ":score"),
                    # (assign, reg1, ":dist"),
                    # (str_store_party_name, s1, ":cur_party"),
                    # (str_store_faction_name, s13, ":faction_no"),
                    # (display_message, "@Debug: Closest faction score: {reg0} for {s13} claiming {s1} (dist: {reg1})."),
                    (gt, ":score", ":closest_score"),
                    (assign, ":closest_score", ":score"),
                    (assign, ":closest_faction", ":faction_no"),
                  (try_end),
                  (call_script, "script_give_center_to_faction", ":cur_party", ":closest_faction"),
                  #(call_script, "script_give_center_to_faction", ":cur_party", ":best_faction"),
                (try_end),
                
                # add a small garrison
                (try_for_range, ":unused", 0, 5),
                  (call_script, "script_cf_reinforce_party", ":cur_party"),
                (try_end),
              (try_end),
            (try_end),
            
            #(party_get_slot, ":home_center", ":cur_party", slot_party_home_center),
            #(store_faction_of_party, ":home_center_faction", ":home_center"),
            #(party_set_faction, ":cur_party", ":home_center_faction"),
          (try_end),
          
          # dispose of defeated heroes - unneeded?
          (try_for_range, ":defeated_lord", kingdom_heroes_begin, kingdom_heroes_end),
            (store_troop_faction, ":defeated_lord_faction", ":defeated_lord"),
            (eq, ":defeated_lord_faction", ":cur_kingdom"),
            (troop_set_slot, ":defeated_lord", slot_troop_occupation, 0),
          (try_end),

         #remove any prisoner lords from defeated faction
         (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
         (try_for_range, ":i_stack", 0, ":num_stacks"),
           (party_prisoner_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
           (troop_is_hero, ":stack_troop"),
           (store_troop_faction, ":stack_faction", ":stack_troop"),
           (eq, ":cur_kingdom", ":stack_faction"),
           (party_remove_prisoners, "p_main_party",  ":stack_troop", 1),
         (try_end),
          
          # check if all good factions are defeated, to start the eye-hand war
          (try_begin), #check wott
            (faction_slot_eq, ":cur_kingdom", slot_faction_side, faction_side_good),
            (assign, ":good_factions_left", 0),
            (try_for_range, ":good_kingdom", kingdoms_begin, kingdoms_end),
              (faction_slot_eq, ":good_kingdom", slot_faction_side, faction_side_good),
              (faction_slot_eq, ":good_kingdom", slot_faction_state, sfs_active),
              (val_add, ":good_factions_left", 1),
            (try_end),

          (str_store_faction_name,s2,":cur_kingdom"),
          (display_log_message,"@{s2} was defeated!"),

            
            # Start the war between Mordor and Isengard
            # Is this automatic defeat for good players?
            
            (try_begin), #start wott
              (eq, ":good_factions_left", 0),
              # uncomment this if you script that Mordor and Isengard can't be defeated before their allies
              #(faction_slot_eq, "fac_mordor", slot_faction_state, sfs_active),
              #(faction_slot_eq, "fac_isengard", slot_faction_state, sfs_active),
              
              #Nazgul chat with the evil player
              (try_begin),
                (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
                (store_and, ":already_done", "$g_tld_conversations_done", tld_conv_bit_nazgul_evil_war),
                (eq, ":already_done", 0),
                (call_script, "script_send_on_conversation_mission", tld_cc_nazgul_evil_war),
              (try_end),

              (call_script, "script_wott_reassign_faction_sides"),
              
              # make sides hostile
              (set_show_messages, 0),
              (try_for_range, ":mordor_ally", kingdoms_begin, kingdoms_end),
                (faction_slot_eq, ":mordor_ally", slot_faction_side, faction_side_eye),
                (try_for_range, ":isengard_ally", kingdoms_begin, kingdoms_end),
                  (faction_slot_eq, ":isengard_ally", slot_faction_side, faction_side_hand),
                  (set_relation, ":mordor_ally", ":isengard_ally", -50), # works both ways, I hope
                (try_end),
              (try_end),
              
              # update player relations to mirror his kingdom
              (try_for_range, ":some_faction", kingdoms_begin, kingdoms_end),
                (neq, ":some_faction", "fac_player_supporters_faction"),
                (store_relation, ":rel", "$players_kingdom", ":some_faction"),
                (call_script, "script_set_player_relation_with_faction", ":some_faction", ":rel"),
                #unrelated, but let's reset active theaters to home for every kingdom
                (faction_get_slot, ":home_theater", ":some_faction", slot_faction_home_theater),
                (faction_set_slot, ":some_faction", slot_faction_active_theater, ":home_theater"),
                #dismantle any existing advance camps
                (try_begin),
                  (faction_get_slot, ":adv_camp", ":some_faction", slot_faction_advance_camp),
                  (party_is_active, ":adv_camp"),
                    (try_begin),  # free up campable place
                        (party_get_slot, ":camp_pointer", ":adv_camp", slot_camp_place_occupied),
                        (gt, ":camp_pointer", 0),
                        (party_get_slot, ":occupied", ":camp_pointer", slot_camp_place_occupied),
                        (val_sub, ":occupied", 1),
                        (val_max, ":occupied", 0),
                        (party_set_slot, ":camp_pointer", slot_camp_place_occupied, ":occupied"),
                        (party_set_slot, ":adv_camp", slot_camp_place_occupied, 0),
                    (try_end),
				  (disable_party, ":adv_camp"),
                (try_end),
              (try_end),
              
              (assign, "$tld_war_began", 2),
              (set_show_messages, 1),

              (dialog_box,"@The Age of Men has finally passed. Now the Two Towers gather their remaining hosts and allies to decide who will be the sole ruler of Middle Earth!","@The War of the Two Towers has started!"),
              (play_sound,"snd_evil_horn"),
            (try_end), #start wott
          (try_end), #check wott
          
          
          #reinforce next theaters - Kham
          (try_begin),
            (faction_get_slot, ":defeated_theater", ":cur_kingdom", slot_faction_active_theater),
            (call_script, "script_cf_reinforce_next_theater", ":defeated_theater", ":cur_kingdom"),
          (try_end),
          # now update active theaters for all factions
          (call_script, "script_update_active_theaters"),
          
          # rethink strategies
          (assign, "$g_recalculate_ais", 2),
          
          (assign, ":faction_removed", 1),
          
          # (try_begin),
          # (eq, "$players_oath_renounced_against_kingdom", ":cur_kingdom"),
          # (assign, "$players_oath_renounced_against_kingdom", 0),
          # (call_script, "script_add_notification_menu", "mnu_notification_oath_renounced_faction_defeated", ":cur_kingdom", 0),
          # (try_end),
          
          #This menu must be at the end because faction banner will change after this menu if the player's supported pretender's original faction is cur_kingdom - but not in TLD!
          (call_script, "script_add_notification_menu", "mnu_notification_faction_defeated", ":cur_kingdom", 0),
          
          (try_begin), #Guardian Party Quest
            (eq, ":cur_kingdom", "fac_isengard"),
            (check_quest_active, "qst_guardian_party_quest"),
            (try_begin),
                (quest_get_slot, ":ent_party",  "qst_guardian_party_quest", slot_quest_target_party), #find and remove ent party
                (gt, ":ent_party", 0),
                (call_script, "script_safe_remove_party", ":ent_party"),
            (try_end),
            (call_script, "script_succeed_quest", "qst_guardian_party_quest"),
            (call_script, "script_end_quest", "qst_guardian_party_quest"),
            (try_for_range, ":lords", kingdom_heroes_begin, kingdom_heroes_end),
              (store_troop_faction, ":lord_fac", ":lords"),
              (eq, ":lord_fac", "fac_rohan"),
              (troop_get_slot, ":lord_party", ":lords", slot_troop_leaded_party),
              (gt, ":lord_party", 0),
              (party_set_slot, ":lord_party", slot_party_scripted_ai, 0),
              #(display_message, "@Scripted Party AI cleared"),
            (try_end),
          (try_end),

          (try_begin),
            (faction_slot_ge, ":cur_kingdom", slot_faction_last_stand, 1),
            (try_for_range, ":scripted_ai_lords", kingdom_heroes_begin, kingdom_heroes_end),
              (troop_get_slot, ":lord_party", ":scripted_ai_lords", slot_troop_leaded_party),
              (gt, ":lord_party", 0),
              (party_is_active, ":lord_party"),
              (party_slot_ge, ":lord_party", slot_party_scripted_ai, 1),
              (party_set_slot, ":lord_party", slot_party_scripted_ai, 0),
              (str_store_troop_name, s30, ":scripted_ai_lords"),
              #(display_message, "@{s30} scripted AI cleared", color_neutral_news),
            (try_end),
          (try_end),
          
          #If the player's home faction was defeated, offer the player to join another faction of the same side
          (try_begin),
            (eq, "$players_kingdom", ":cur_kingdom"),
            (faction_get_slot, ":player_side", "$players_kingdom", slot_faction_side),
            (assign, ":game_over", 1),
            (try_for_range, ":allied_kingdom", kingdoms_begin, kingdoms_end),
              (faction_slot_eq, ":allied_kingdom", slot_faction_state, sfs_active),
              (faction_slot_eq, ":allied_kingdom", slot_faction_side, ":player_side"),
              (assign, ":game_over", 0),
            (try_end),
            
            (try_begin),
              (eq, ":game_over", 1), #no living factions of the player's side remain - total defeat
              (call_script, "script_add_notification_menu", "mnu_notification_total_defeat", ":player_side", 0),
            (else_try), # some allies left, offer player to join
              #(call_script, "script_add_notification_menu", "mnu_notification_join_another_faction", ":player_side", 0),
              (call_script, "script_add_notification_menu", "mnu_notification_your_faction_collapsed", ":player_side", 0),
            (try_end),
          (try_end),
        (try_end),
        
        (try_begin),
          (eq, ":faction_removed", 1),
          (val_sub, ":num_active_factions", 1),
          (call_script, "script_store_average_center_value_per_faction"),
        (try_end),
        
        (try_for_range, ":cur_kingdom_2", kingdoms_begin, kingdoms_end),
          (call_script, "script_update_faction_notes", ":cur_kingdom_2"),
        (try_end),
        
      (try_end),
      # TLD: check for total victory
      (assign, ":game_over", 1),
      (assign, ":living_side", -1),
      (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
        (faction_get_slot, ":cur_side", ":cur_kingdom", slot_faction_side),
        (try_begin),
          (eq, ":living_side", -1),
          (assign, ":living_side", ":cur_side"), #first live faction
        (else_try),
          (neq, ":living_side", ":cur_side"),
          (assign, ":game_over", 0), # found a live faction that belongs to some other side
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":game_over", 1),
        (call_script, "script_add_notification_menu", "mnu_notification_one_side_left", ":living_side", 0),
        
        #Send Gandalf on a victory chat - good player
        (try_begin),
          (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
          (eq, ":living_side", faction_side_good),
          (store_and, ":already_done", "$g_tld_conversations_done", tld_conv_bit_gandalf_victory),
          (eq, ":already_done", 0),
          (call_script, "script_send_on_conversation_mission", tld_cc_gandalf_victory),
        (try_end),
        #Send Nazgul on a victory chat - evil player
        (try_begin),
          (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
          (neq, ":living_side", faction_side_good),
          (store_and, ":already_done", "$g_tld_conversations_done", tld_conv_bit_nazgul_victory),
          (eq, ":already_done", 0),
          (call_script, "script_send_on_conversation_mission", tld_cc_nazgul_victory),
        (try_end),
      (try_end),
      # TLD: replaced by the above
      # (try_begin),
      # (eq, ":num_active_factions", 1),
      # (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      # (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      # (call_script, "script_add_notification_menu", "mnu_notification_one_faction_left", ":cur_kingdom", 0),
      # (try_end),
      # (try_end),
  ]),

  
  # (56) TLD Messages about faction strength changes
  (5,[(gt, "$tld_war_began", 0),
	  (try_for_range,":faction",kingdoms_begin,kingdoms_end),
        (faction_slot_eq, ":faction", slot_faction_state, sfs_active),
        (faction_get_slot,":strength",":faction",slot_faction_strength),
        (ge, ":strength", 1), #additional check for above
        (faction_get_slot,":strength_new",":faction",slot_faction_strength_tmp),
        (faction_set_slot,":faction",slot_faction_strength,":strength_new"),
        #       (val_add,":strength",999),
        #       (val_add,":strength_new",999),
        (val_div,":strength",1000),
        (val_div,":strength_new",1000),
        
        (try_begin),
          (neq,":strength",":strength_new"),
          (store_relation, ":rel", "$players_kingdom", ":faction"),
          (try_begin),
            (store_sub, ":is_good", ":strength_new", ":strength"),
            (val_mul, ":is_good", ":rel"), # only the sign is important
            (ge, ":is_good", 0), # ++ or --
            (assign, ":news_color", color_good_news),
          (else_try),
            (assign, ":news_color", color_bad_news),
          (try_end),
          (str_store_faction_name, s22,":faction"),
          (call_script, "script_faction_strength_string_to_s23", ":faction"),
          (try_begin),
            (lt,":strength",":strength_new"),   # announce when strength threshold is crossed upwards
			(neq, "$g_fast_mode", 1),
            (display_message,"@The forces of {s22} have rallied! {s22} is now {s23}.", ":news_color"),
          (else_try),
			(neq, "$g_fast_mode", 1),
            (display_message,"@The might of {s22} has diminished! {s22} is now {s23}.", ":news_color"), # announce when strength threshold is crossed downwards
          (try_end),
        (try_end),
        
        #CC: spawn mordor legions of old when mordor strength is <= 2000, and mordor is the only (eye) faction left.
        (try_begin),
          (eq, ":faction", "fac_mordor"),
          (faction_slot_eq, ":faction", slot_faction_guardian_party, 0), #CC: We use this to track wether or not the legions have been spawned.
          (neg|faction_slot_ge, ":faction", slot_faction_strength, fac_str_guardian), #CC: Skip if the faction isn't weak enough
          (assign, ":mordor_only", 1),
          #(try_for_range, ":other_fac", kingdoms_begin, kingdoms_end),
          #	(eq, ":mordor_only", 1),
          #	(neq, ":other_fac", ":faction"),
          #	(faction_slot_eq, ":other_fac", slot_faction_state, sfs_active), # faction lives
          #	(faction_slot_eq, ":other_fac", slot_faction_side, faction_side_eye),
          #	(assign, ":mordor_only", 0), # Found another eye faction, do not spawn yet...
          #(try_end),
          (eq, ":mordor_only", 1),
          (set_spawn_radius, 8),
          (spawn_around_party, "p_town_morannon", "pt_legion_barad_dur"),
          (assign, ":guard_party", reg0),
          (party_set_slot, ":guard_party", slot_party_type, spt_guardian),
          (party_set_slot, ":guard_party", slot_party_victory_value, 200),
          (party_set_slot, ":guard_party", slot_party_home_center, "p_town_morannon"),
          (party_set_slot, ":guard_party", slot_party_ai_object, "p_town_morannon"),
          (party_set_slot, ":guard_party", slot_party_ai_state, spai_undefined),
          (party_set_ai_behavior, ":guard_party", ai_bhvr_patrol_location),
          (party_set_ai_patrol_radius, ":guard_party", 10),
          (spawn_around_party, "p_town_morannon", "pt_legion_minas_morgul"),
          (assign, ":guard_party", reg0),
          (party_set_slot, ":guard_party", slot_party_type, spt_guardian),
          (party_set_slot, ":guard_party", slot_party_victory_value, 200),
          (party_set_slot, ":guard_party", slot_party_home_center, "p_town_morannon"),
          (party_set_slot, ":guard_party", slot_party_ai_object, "p_town_morannon"),
          (party_set_slot, ":guard_party", slot_party_ai_state, spai_undefined),
          (party_set_ai_behavior, ":guard_party", ai_bhvr_patrol_location),
          (party_set_ai_patrol_radius, ":guard_party", 10),
          (spawn_around_party, "p_town_morannon", "pt_legion_udun"),
          (assign, ":guard_party", reg0),
          (party_set_slot, ":guard_party", slot_party_type, spt_guardian),
          (party_set_slot, ":guard_party", slot_party_victory_value, 200),
          (party_set_slot, ":guard_party", slot_party_home_center, "p_town_morannon"),
          (party_set_slot, ":guard_party", slot_party_ai_object, "p_town_morannon"),
          (party_set_slot, ":guard_party", slot_party_ai_state, spai_undefined),
          (party_set_ai_behavior, ":guard_party", ai_bhvr_patrol_location),
          (party_set_ai_patrol_radius, ":guard_party", 10),
          (spawn_around_party, "p_town_morannon", "pt_legion_gorgoroth"),
          (assign, ":guard_party", reg0),
          (party_set_slot, ":guard_party", slot_party_type, spt_guardian),
          (party_set_slot, ":guard_party", slot_party_victory_value, 200),
          (party_set_slot, ":guard_party", slot_party_home_center, "p_town_morannon"),
          (party_set_slot, ":guard_party", slot_party_ai_object, "p_town_morannon"),
          (party_set_slot, ":guard_party", slot_party_ai_state, spai_undefined),
          (party_set_ai_behavior, ":guard_party", ai_bhvr_patrol_location),
          (party_set_ai_patrol_radius, ":guard_party", 10),
          (faction_set_slot, "fac_mordor", slot_faction_guardian_party, 1),
          (try_begin),
            (store_relation, ":rel", "$players_kingdom", ":faction"),
            (gt, ":rel", 0),
            (assign, ":news_color", color_bad_news),
          (else_try),
            (assign, ":news_color", color_good_news),
          (try_end),
          (display_message, "@In a desperate attempt to defend against his enemies, Sauron sends out his legions of Mordor!", ":news_color"),
        (try_end),
        
        #MV: spawn a guardian party (once) when faction strength below fac_str_guardian
        # InVain: Disabled
        #this is a fun quick fix to defeat dying factions and avoid grinding
        # (try_begin),
          # #MV: disabled in 3.15, not needed anymore except for factions with unsiegable capitals like Isengard and Woodelves
          # (eq, ":faction", "fac_isengard"),
          # #(             eq, ":faction", "fac_woodelf"),
          # (neg|faction_slot_ge, ":faction", slot_faction_strength, fac_str_guardian),
          # (faction_slot_eq, ":faction", slot_faction_guardian_party, 0),
          
          # (faction_get_slot, ":capital", ":faction", slot_faction_capital),
          # (set_spawn_radius, 1),
          # (spawn_around_party, ":capital", "pt_none"),
          # (assign, ":guard_party", reg0),
          # (faction_set_slot, ":faction", slot_faction_guardian_party, ":guard_party"),
          # (faction_set_slot, ":faction", slot_faction_guardian_party_spawned, 1),
          
          # #party slots
          # (str_store_faction_name, s6, ":faction"),
          # (try_begin),
            # (faction_slot_eq, ":faction", slot_faction_side, faction_side_good),
            # (party_set_name, ":guard_party", "@Guardians of {s6}"),
          # (else_try),
            # (party_set_name, ":guard_party", "@Guard Legion of {s6}"),
          # (try_end),
          # # CC bugfix: set the icons to properly match the party
          # (try_begin),
            # (eq, ":faction", "fac_isengard"),
            # (party_set_icon, ":guard_party", icon_wargrider_walk_x4),
          # # (else_try),
            # # (eq, ":faction", "fac_woodelf"),
            # # (party_set_icon, ":guard_party", icon_mirkwood_elf_x3),
          # (try_end),
          # (party_set_slot, ":guard_party", slot_party_type, spt_guardian),
          # (party_set_slot, ":guard_party", slot_party_victory_value, ws_guard_vp), # huge victory points for party kill
          # (party_set_slot, ":guard_party", slot_party_home_center, ":capital"),
          # (party_set_faction, ":guard_party", ":faction"),
          # (party_set_slot, ":guard_party", slot_party_ai_object, ":capital"),
          # (party_set_slot, ":guard_party", slot_party_ai_state, spai_undefined),
          # (party_set_ai_behavior, ":guard_party", ai_bhvr_patrol_location),
          # (party_set_ai_patrol_radius, ":guard_party", 3), #must be tight radius
          
          # #fill it up with lord army reinforcements and upgrade a lot
          # (store_random_in_range, ":reinforcement_waves", 80, 100), #average about 8 troops per reinf
          # (try_for_range, ":unused", 0, ":reinforcement_waves"),
            # (call_script, "script_cf_reinforce_party", ":guard_party"),
          # (try_end),
          # (try_for_range, ":unused", 0, 40), #lords get initially about 14x4000, we do 40x6000 (about 4-5x more)
            # (party_upgrade_with_xp, ":guard_party", 6000, 0),
          # (try_end),
          
          # #tell the player what happened
          # (try_begin),
            # (store_relation, ":rel", "$players_kingdom", ":faction"),
            # (gt, ":rel", 0),
            # (assign, ":news_color", color_good_news),
          # (else_try),
            # (assign, ":news_color", color_bad_news),
          # (try_end),
          # (str_store_party_name, s7, ":capital"),
          # (assign, reg70, ":faction"),
          # (jump_to_menu, "mnu_guardian_party_spawned"),
          # (display_log_message, "@Scouts report that {s6} gathered a large army in the vicinity of {s7}, in a last ditch attempt to defend the capital.", ":news_color"),
        # (try_end),
      (try_end),
  ]),
  
  # (57) TLD deal with prisoner trains and routed parties reached destination (MV: shortened trigger from 8 to 3, so prisoners would update sooner), (CppCoder: Added routed parties to this trigger)
  # TLD: also check for temporary arrays
  # TLD: also check for temporary map props and smoking ruins
  (3,[
      (try_for_parties, ":party_no"),
        #(party_is_active, ":party_no"),
        (party_get_template_id, ":template", ":party_no"),
        (try_begin), # CC: Cleanup routed enemies / allies.
          (party_is_active, ":party_no"),
          #(party_get_template_id, ":template", ":party_no"),
          (is_between, ":template", "pt_routed_allies", "pt_legion_minas_morgul"),
          (party_is_in_any_town, ":party_no"),
          
          (call_script, "script_safe_remove_party", ":party_no"),
          
        (else_try), # Prisioner trains transfer / removing
          (party_is_active, ":party_no"),
          (party_slot_eq, ":party_no", slot_party_type, spt_prisoner_train),
          (party_is_in_any_town, ":party_no"),
          (party_get_cur_town, ":cur_center", ":party_no"),
          # (str_store_party_name, s22, ":cur_center"),
          # (display_message, "@DEBUG: Prisoner train arrives in {s22}"),
          (assign, "$g_move_heroes", 1),
          (party_detach, ":party_no"),
          #(party_get_position, pos1, ":party_no"),
          #(position_get_x, reg1, pos1),
          #(position_get_y, reg2, pos1),
          #(display_message, "@DEBUG: party at: {reg1}, {reg2} removed", debug_color),
          #(party_get_position, pos1, "p_main_party"),
          #(position_get_x, reg1, pos1),
          #(position_get_y, reg2, pos1),
          #(display_message, "@DEBUG: player at: {reg1}, {reg2}", debug_color),
          (call_script, "script_party_prisoners_add_party_prisoners", ":cur_center", ":party_no"),
          
          (call_script, "script_safe_remove_party", ":party_no"),
        (else_try), # Array handling
          (this_or_next|eq,":template","pt_warp_array"), # Also checked to prevent the array content triggering the prop handling of the next block
          (             eq,":template","pt_warp_temp_array"), # Temporary arrays, we will delete these
          (try_begin),
            (eq,":template","pt_warp_temp_array"),
            (call_script,"script_warp_array_delete",":party_no"),
          (try_end),
        (else_try), # Ruins and temporary map props handling - moved here for efficiency and support of temporary props
          (neg|party_slot_eq, ":party_no", slot_center_destroyed, 0),
          (neg|party_slot_eq, ":party_no", slot_village_smoke_added, 0),
          (party_get_slot, ":counter",":party_no", slot_village_smoke_added),
          (val_sub,":counter",3),
          (party_set_slot, ":party_no", slot_village_smoke_added, ":counter"),
          
          (try_begin),
            (lt,":counter",1),
            (party_clear_particle_systems, ":party_no"),
            (try_begin), # Temporary map props removal
              (neg|is_between,":party_no",centers_begin,centers_end),
              (neq,":party_no","p_town_barad_dur"),
              (party_set_flags,":party_no",pf_is_static,0), # This ensures the party icon is removed
              (call_script,"script_safe_remove_party",":party_no"),
            (else_try), # Permanent ruins just stop smoking
              (party_set_slot, ":party_no", slot_village_smoke_added, 0),
            (try_end),
          (try_end),
          
        (try_end),
        
        
      (try_end), # try_for_parties
      
      
  ]),
  
  # (58) TLD: establish advance camps in active, non-home theaters
  (6,[(store_current_hours, ":cur_hours"),
      (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction", slot_faction_state, sfs_active),
        (faction_get_slot, ":active_theater", ":faction", slot_faction_active_theater),
        (neg|faction_slot_eq, ":faction", slot_faction_home_theater, ":active_theater"), #not in home theater
        
        (faction_get_slot, ":strength", ":faction", slot_faction_strength),
        (gt, ":strength", 1500), #Kham- don't create adv camps when lower than 1500
        
        (faction_get_slot, ":adv_camp", ":faction", slot_faction_advance_camp),
        (neg|party_is_active, ":adv_camp"), #not already established
        
        (faction_get_slot, ":camp_requested_hours", ":faction", slot_faction_advcamp_timer),
        (val_add, ":camp_requested_hours", 5*24), # 3 days after faction changes theater or previous camp destroyed - Changed to 5 Days (kham)
        (ge, ":cur_hours", ":camp_requested_hours"),
        
        (store_random_in_range, ":rand", 0, 20000),
		(lt, ":rand", ":strength"), #faction strength /200 is spawn chance
        #(lt, ":rand", 30), # 30% chance every 6 hours
        (val_sub, ":strength", 500),
        (faction_set_slot, ":faction", slot_faction_strength, ":strength"), #simulate effort of establishing an advance camp (hopefully slows down steamrolling)
        
        # set up the advance camp
        (party_set_slot, ":adv_camp", slot_center_theater, ":active_theater"),
        (call_script, "script_get_advcamp_pos_predefined", ":faction"), #fills pos1
        (party_set_position, ":adv_camp", pos1), #teleport!
        (enable_party, ":adv_camp"), #enable.. works if it's enabled already too
        (call_script, "script_theater_name_to_s15", ":active_theater"),
        (str_store_faction_name, s2, ":faction"),
        (try_begin),
          (store_relation, ":rel", "$players_kingdom", ":faction"),
          (gt, ":rel", 0),
          (assign, ":news_color", color_good_news),
        (else_try),
          (assign, ":news_color", color_bad_news),
        (try_end),
        (display_log_message, "@The forces of {s2} established an Advance Camp in {s15}!", ":news_color"),
        (call_script, "script_update_center_notes", ":adv_camp"),
		
		#Relocate player's reserves
		(try_begin),
			(eq, ":faction", "$players_kingdom"),
			(troop_get_slot, ":reserve_party_ac", "trp_player", slot_troop_player_reserve_adv_camp),
			(gt, ":reserve_party_ac", 0),
			(enable_party, ":reserve_party_ac"),
			(party_relocate_near_party, ":reserve_party_ac", ":adv_camp", 0), 
			(party_attach_to_party, ":reserve_party_ac", ":adv_camp"),
		(try_end),
        
        # any enemy in the theater that has an advance camp elsewhere should return to defend their home theater
        (try_for_range, ":adv_camp_faction", kingdoms_begin, kingdoms_end),
          (faction_slot_eq, ":adv_camp_faction", slot_faction_state, sfs_active),
          (store_relation, ":rel", ":faction", ":adv_camp_faction"),
          (lt, ":rel", 0), # active enemy
          (faction_get_slot, ":home_theater", ":adv_camp_faction", slot_faction_home_theater),
          (party_slot_eq, ":adv_camp", slot_center_theater, ":home_theater"),
          #(neg|faction_slot_eq, ":enemy_faction", slot_faction_active_theater, ":next_theater"),
          
          #dismantle advance camp and return
          (faction_get_slot, ":established_adv_camp", ":adv_camp_faction", slot_faction_advance_camp),
          (try_begin),
            (party_is_active, ":established_adv_camp"),
            (call_script, "script_destroy_center", ":established_adv_camp"),
            (try_begin),  # free up campable place
                (party_get_slot, ":camp_pointer", ":established_adv_camp", slot_camp_place_occupied),
                (gt, ":camp_pointer", 0),
                (party_get_slot, ":occupied", ":camp_pointer", slot_camp_place_occupied),
                (val_sub, ":occupied", 1),
                (val_max, ":occupied", 0),
                (party_set_slot, ":camp_pointer", slot_camp_place_occupied, ":occupied"),
                (party_set_slot, ":established_adv_camp", slot_camp_place_occupied, 0),
            (try_end),
            #(disable_party, ":enemy_adv_camp"),
          (try_end),
          (str_store_faction_name, s2, ":adv_camp_faction"),
          (try_begin),
            (store_relation, ":rel", "$players_kingdom", ":adv_camp_faction"),
            (lt, ":rel", 0),
            (assign, ":news_color", color_bad_news),
          (else_try),
            (assign, ":news_color", color_good_news),
          (try_end),
          (try_begin),
            (neg|faction_slot_eq, ":adv_camp_faction", slot_faction_active_theater, ":home_theater"), #If they are not yet home,
            (display_log_message, "@The hosts of {s2} march back to defend their homes!", ":news_color"),
          (try_end),
		  (try_begin), #When retreating home, merge ac player reserves with capital reserves
			(eq, ":adv_camp_faction", "$players_kingdom"),
			(troop_get_slot, ":reserve_party_ac", "trp_player", slot_troop_player_reserve_adv_camp),
			(gt, ":reserve_party_ac", 0),
			(troop_get_slot, ":reserve_party_cap", "trp_player", slot_troop_player_reserve_party),

				(try_begin), #if there's no player reserves at capital, create a new one
					(eq, ":reserve_party_cap", 0), 
					(faction_get_slot, ":capital", ":adv_camp_faction", slot_faction_capital),
					(str_store_party_name, s1, ":capital"),
					(spawn_around_party, ":capital", "pt_volunteers"),
					(assign, ":reserve_party_cap", reg0),
					(party_add_members, ":reserve_party_cap", "trp_looter", 1), #.. or change_screen_exchange_with_party will crash #InVain: dunno if needed in this context too, keeping just in case.
					(party_remove_members, ":reserve_party_cap", "trp_looter", 1),
					(troop_set_slot, "trp_player", slot_troop_player_reserve_party, ":reserve_party_cap"),
					(party_attach_to_party, ":reserve_party_cap", ":capital"),
					(party_set_name, ":reserve_party_cap", "@{playername}'s Reserves"),
					(party_set_flags, ":reserve_party_cap", pf_no_label),
					(party_set_ai_behavior, ":reserve_party_cap", ai_bhvr_hold),
				(try_end),

			(enable_party, ":reserve_party_ac"), #just in case
			(party_get_num_companion_stacks, ":num_stacks", ":reserve_party_ac"),
			(try_for_range, ":i_stack", 0, ":num_stacks"),
				(party_stack_get_size, ":stack_size", ":reserve_party_ac", ":i_stack"),
				(party_stack_get_troop_id, ":troop", ":reserve_party_ac", ":i_stack"),
				(party_add_members, ":reserve_party_cap", ":troop", ":stack_size"),
			(try_end),
			(party_get_num_prisoner_stacks, ":num_stacks", ":reserve_party_ac"),
			(try_for_range, ":i_stack", 0, ":num_stacks"),
				(party_prisoner_stack_get_size, ":stack_size", ":reserve_party_ac", ":i_stack"),
				(party_prisoner_stack_get_troop_id, ":troop", ":reserve_party_ac", ":i_stack"),
				(party_add_prisoners, ":reserve_party_cap", ":troop", ":stack_size"),
			(try_end),			
			(call_script, "script_safe_remove_party", ":reserve_party_ac"),
			(troop_set_slot, "trp_player", slot_troop_player_reserve_adv_camp,  0),					
		  (try_end),
          (faction_set_slot, ":adv_camp_faction", slot_faction_active_theater, ":home_theater"), #reset to home
        (try_end),
        
        # clear and refill the garrison (advance camps always start weak)
        (party_clear, ":adv_camp"),
        (assign, ":garrison_strength", 20), 
        (party_get_slot, ":garrison_limit", ":adv_camp", slot_center_garrison_limit),
        (try_for_range, ":unused", 0, ":garrison_strength"),
          (try_begin),
            (party_get_num_companions, ":garrison_size", ":adv_camp"),
            (le, ":garrison_limit", ":garrison_size"), #TLD: don't go overboard
            (assign, ":garrison_strength", 0),
          (else_try),
            (call_script, "script_cf_reinforce_party", ":adv_camp"),
          (try_end),
        (try_end),
      (try_end), #try_for_range ":faction"
  ]),
  
  # (59) TLD: update player attributes for rings and such
  (1,[(call_script, "script_apply_attribute_bonuses")]),
  
  
  # (60) TLD: stop ruins from smoking as time passes
  # Rafa: Deprecated, can be used for something else 
  # Kham - Thanks! Will use for Faction Last Stand Event
  
  (3,[
    (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":faction", slot_faction_state, sfs_active), #still active
      (faction_get_slot, ":last_stand_counter", ":faction", slot_faction_last_stand),
      (try_begin),
        (eq, "$cheat_mode", 1),
        (assign, reg70, ":last_stand_counter"),
        (gt, reg70, 0),
        (display_message, "@{reg70} - Last Stand", color_bad_news),
      (try_end),
      (gt, ":last_stand_counter", 0),
      (call_script, "script_last_faction_stand", ":faction"),
      (val_add, ":last_stand_counter", 1),
      (faction_set_slot, ":faction", slot_faction_last_stand, ":last_stand_counter"),
      #(assign, reg50, ":last_stand_counter"),
      #(display_message, "@Current Last Stand Counter: {reg50}"),
    (try_end),

    (try_begin),
      #(troop_slot_eq, "trp_player", slot_troop_home, 22), #kham test
      (eq, "$cheat_mode", 1),
      (try_for_range, ":enemy_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":enemy_faction", slot_faction_state, sfs_active),
        (faction_slot_ge, ":enemy_faction", slot_faction_last_stand, 11),
        (faction_get_slot, ":capital", ":enemy_faction", slot_faction_capital),
        (party_slot_eq, ":capital", slot_center_destroyed, 0),
        (faction_get_slot, ":enemy_faction_current_theater", ":enemy_faction", slot_faction_active_theater),

        (try_for_range, ":besieger_faction", kingdoms_begin, kingdoms_end),
          (faction_slot_eq, ":besieger_faction", slot_faction_state, sfs_active), #must be active
          (faction_slot_ge, ":besieger_faction", slot_faction_strength, fac_str_ok),
          (faction_get_slot, ":attacker_faction_theater", ":besieger_faction", slot_faction_active_theater),
          (eq, ":attacker_faction_theater", ":enemy_faction_current_theater"), #Should be same theater
          (store_relation, ":reln", ":besieger_faction", ":enemy_faction"),
          (lt, ":reln", 0), #Must be enemies
          (faction_get_slot, ":faction_ai_state",  ":besieger_faction", slot_faction_ai_state),
          (neq, ":faction_ai_state", sfai_gathering_army), #Make sure they can gather army
          (faction_get_slot, ":besieger_marshall", ":besieger_faction", slot_faction_marshall), 
          (troop_get_slot, ":marshall_party", ":besieger_marshall", slot_troop_leaded_party),
          (gt, ":marshall_party", 0),
          (neg|party_slot_eq, ":marshall_party", slot_party_type, spt_kingdom_hero_alone), #Should not be alone
          (call_script, "script_party_count_fit_regulars", ":marshall_party"), 
          (ge, reg0, tld_siege_min_party_size),
          (faction_set_slot, ":besieger_faction", slot_faction_state, sfai_attacking_center),
          (call_script, "script_party_set_ai_state", ":marshall_party", spai_besieging_center, ":capital"),
          (party_set_ai_behavior, ":marshall_party", ai_bhvr_attack_party),
          (party_set_ai_object, ":marshall_party", ":capital"),
          (party_set_flags, ":marshall_party", pf_default_behavior, 1),
          (party_set_slot, ":marshall_party", slot_party_ai_substate, 1),
          (call_script, "script_begin_assault_on_center", ":capital"),
          (party_set_slot, ":marshall_party", slot_party_scripted_ai, 1),
          (party_set_ai_initiative, ":marshall_party", 10),
          #(str_store_troop_name, s31, ":besieger_marshall"),
          #(display_message, "@{s31} scripted AI set", color_neutral_news),
          #(display_message, "@Faction Marshall Starts Besieging last stand capital"),
        (try_end),
      (try_end),

      (try_begin),
        (faction_slot_eq, ":enemy_faction", slot_faction_last_stand, 15),
        (faction_set_slot, ":enemy_faction", slot_faction_last_stand, 1),
      (try_end),

    (try_end),

  ]),

  # (61) # Heal Wounds every 10 hours + check prisoners for Sorceress Companion
  (10,[

    (try_begin), # npc and player healing from wounds (should be 25 hours) - kham changed to 10 hours, was 1.
      (eq, "$tld_option_injuries",1),
      (party_get_skill_level, ":wound_treatment", skl_wound_treatment),
      (try_for_range, ":npc",companions_begin,new_companions_end),
        (this_or_next|is_between, ":npc", companions_begin, companions_end),
        (is_between, ":npc", new_companions_begin, new_companions_end),
        (store_add, ":chance", 15, ":wound_treatment"),
        (store_random_in_range, ":random",0,100),
        (le,":random",":chance"), #10% chance for healing - Kham: changed to 15% and added wound treatment effect
        (call_script, "script_healing_routine", ":npc"),
      (try_end),
      (store_random_in_range, ":random_2",0,100),
      (store_add, ":chance_2", 30, ":wound_treatment"),
      (le,":random_2",":chance_2"), #20% chance for healing - changed to 30% and added wound treatment effect
      (call_script, "script_healing_routine", "trp_player"),
    (try_end),

    (try_begin),
      (main_party_has_troop, "trp_npc20"), #player has Zigurphel
      (troop_get_slot, ":ziggy_talk", "trp_npc20", slot_troop_wealth), #Use this to check if she has asked and player has accepted already.
      (le, ":ziggy_talk", 1), 
      (party_get_num_prisoners, ":prisoners", "p_main_party"),
      (ge, ":prisoners", 6),
      (assign, "$talk_context", tc_starting_quest), #Use this for Ziggy's first convo
      (start_map_conversation, "trp_npc20"),
    (try_end),
  ]),
  
  # (62) Control Gandalf and Nazgul states
  (1,[
      #Send Nazgul to look for Baggins - evil player
      (try_begin),
        (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
        (store_and, ":already_done", "$g_tld_conversations_done", tld_conv_bit_nazgul_baggins),
        (eq, ":already_done", 0),
        (store_character_level, ":level", "trp_player"),
        (ge, ":level", 4),
        (call_script, "script_send_on_conversation_mission", tld_cc_nazgul_baggins),
      (try_end),
      
      (try_for_range, ":celebrity", 0, 2), #process Gandalf, then the Nazgul in the same way
        (try_begin),
          (eq, ":celebrity", 0),
          (assign, ":mission_troop", "trp_gandalf"),
          (assign, ":mission_troop_side", faction_side_good),
          (assign, ":state", "$g_tld_gandalf_state"),
        (else_try),
          (assign, ":mission_troop", "trp_nazgul"),
          (assign, ":mission_troop_side", faction_side_eye),
          (assign, ":state", "$g_tld_nazgul_state"),
        (try_end),
        
        (troop_get_slot, ":party", ":mission_troop", slot_troop_leaded_party),
        (try_begin),
          (eq, ":state", 0), #active, not on a mission
          (party_is_active, ":party"), #should always be true here
          # when in town, randomly make him travel to some nearby random town not too far from the player
          (try_begin),
            (party_is_in_any_town, ":party"),
            (store_random_in_range, ":rand", 0, 100),
            (eq, ":rand", 0), # every hour 1% chance
            
            #find random mission troop-friendly town close to the player
            (party_get_cur_town, ":cur_center", ":party"),
            (assign, ":min_distance", 9999999),
            (assign, ":nearest_town", -1),
            (try_for_range, ":center_no", centers_begin, centers_end),
              (party_is_active, ":center_no"), #TLD
              (party_slot_eq, ":center_no", slot_center_destroyed, 0), # TLD
              (neq, ":center_no", ":cur_center"),
              (store_faction_of_party, ":center_faction", ":center_no"),
              (faction_slot_eq, ":center_faction", slot_faction_side, ":mission_troop_side"), #e.g. Nazgul travels to the Eye town closest to player
              (call_script, "script_get_tld_distance", "p_main_party", ":center_no"),
              (assign, ":party_distance", reg0),
              (lt, ":party_distance", ":min_distance"),
              (store_random_in_range, ":rand2", 0, 100),
              (this_or_next|eq, ":nearest_town", -1),
              (ge, ":rand2", 50), #ignore 50% of the towns randomly
              (assign, ":min_distance", ":party_distance"),
              (assign, ":nearest_town", ":center_no"),
            (try_end),
            
            (neq, ":nearest_town", -1), #failing is no problem
            
            # (str_store_party_name, s4, ":nearest_town"),
            # (display_message, "@DEBUG: Celebrity departing to {s4}!", 0xff00ff),
            
            (party_set_ai_behavior, ":party", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":party", ":nearest_town"),
            (party_set_flags, ":party", pf_default_behavior, 0),
            
            # old party removal code
            #        (assign, ":state", -1),
            #        (troop_set_slot, ":mission_troop", slot_troop_leaded_party, -1),
            #(display_message, "@DEBUG: Party arrived and removed", 0xff00fd33),
          (try_end),
        (try_end),
        
        # (try_begin),
        # (eq, ":celebrity", 0),
        # (assign, "$g_tld_gandalf_state", ":state"),
        # (else_try),
        # (assign, "$g_tld_nazgul_state", ":state"),
        # (try_end),
        
      (try_end), # try_for_range
  ]),
  
  
  ] + (is_a_wb_trigger and False and [
    
    # (63) Propagate Mordor strength as shader uniform every hour...
    (0,
      [
        # get the general strength from the faction slot (which can be from 0 to 8000)
        # example: 6900
        (faction_get_slot, ":faction_strength", "fac_mordor", slot_faction_strength),
        
        # limit the range of values to 0-8000, just to make sure wonky things won't happen
        (val_clamp, ":faction_strength", 0, fac_str_max),
        
        # normalize it to the unit by dividing it by the maximum, taking care of
        # the two digits for decimals as we are doing integer operations on a future float
        # example: (6900*100) / (8000/100) = 8625 = 86.25%
        (val_mul,":faction_strength", 100),
        (val_div,":faction_strength", fac_str_max/100), # fixed point with two decimal points
        
        # reverse it, so that the more powerful the faction, darker the map
        # example: (100*100) - 8625 = 1325 = 13.75%
        (store_sub, ":faction_strength", 100 * 100, ":faction_strength"),
        
        # instead of linearly mapping the ambient light... map it to a pow curve,
        # darker the dark, brighter when Mordor is weak, looks less flat ambient-wise.
        # example: 1375 -> sqrt(0.1375) = 0.3708f = 37.08%
        (set_fixed_point_multiplier, 100 * 100),
        (store_pow, ":faction_strength", ":faction_strength", (1/2.0) * (100 * 100)),
        
        # min:     0 = 0.0f
        # max: 10000 = 1.0f
        
        # gradient it smoothly instead of abruptly
        (try_begin),
          (lt,":faction_strength","$cur_mordor_strength"),
          (val_add,"$cur_mordor_strength",100),
        (else_try),
          (gt,":faction_strength","$cur_mordor_strength"),
          (val_sub,"$cur_mordor_strength",100),
        (try_end),
        
        (neq,"$cur_mordor_strength",":faction_strength"),
        (store_div,":out","$cur_mordor_strength", 2),
        (set_shader_param_float, "@swy_mordor_strength_factor", ":out"),
    ]),
    
    ] or []) + [
  
  ##Kham - Eff it, lets buff Gondor completely by triggering hiring more often just for the special snowflakes -- Tested, they still suck, but they will be hard to defeat.
  
  #(12,[(try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
  #        (store_troop_faction, ":faction"),
  #        (eq, ":faction", "fac_gondor"),
  #        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
  #        (ge, ":party_no", 1),
  #        (party_is_active, ":party_no"), #MV
  #(party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party), #TLD: only hosts reinforce
  #        (party_get_attached_to, ":cur_attached_party", ":party_no"),
  #        (is_between, ":cur_attached_party", centers_begin, centers_end),
  #        (party_slot_eq, ":cur_attached_party", slot_center_is_besieged_by, -1), #center not under siege
  #        (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"), #Hiring men up to lord-specific limit
  #      (try_end),
  #      (display_message, "@Gondor Reinforces!", color_good_news),
  #      ]),
  
  
  ## Kham Gondor Reinforcement Event - Original / deprecated
  ## (6,
  ##  [(eq, "$tld_war_began", 1),
  ##   (assign, "$gondor_reinforcement_event", 0),
  ##   (eq, "$gondor_reinforcement_event",0),
  ##    (try_for_range,       ":cur_troop_fiefs", "trp_knight_1_1", "trp_knight_1_9"), ## Gondor Fiefs Troops
  ##      (this_or_next|eq,   ":cur_troop_fiefs", "trp_knight_1_3"),
  ##      (this_or_next|eq,   ":cur_troop_fiefs", "trp_knight_1_5"),
  ##      (             eq,   ":cur_troop_fiefs", "trp_knight_1_6"),
  ##      (troop_get_slot,    ":cur_party_fiefs", ":cur_troop_fiefs", slot_troop_leaded_party),
  ##      (party_is_active,   ":cur_party_fiefs"),
  ##      (party_slot_eq,     ":cur_party_fiefs", slot_party_type, spt_kingdom_hero_party),
  ##      (neg|party_slot_eq, ":cur_party_fiefs", slot_party_ai_state, spai_accompanying_army),
  ##      (call_script, "script_party_set_ai_state", ":cur_party_fiefs", spai_holding_center, "p_town_linhir"),
  ##      (party_set_ai_behavior, ":cur_party_fiefs",ai_bhvr_travel_to_party),
  ##      (party_set_ai_object,   ":cur_party_fiefs", "p_town_linhir"),
  ##    (try_end),
  ##    (try_for_range,       ":cur_troop_center", "trp_knight_1_1", "trp_knight_1_9"), ## Gondor Center Troops
  ##      (this_or_next|eq,   ":cur_troop_center", "trp_knight_1_1"),
  ##      (this_or_next|eq,   ":cur_troop_center", "trp_knight_1_4"),
  ##      (this_or_next|eq,   ":cur_troop_center", "trp_knight_1_7"),
  ##      (             eq,   ":cur_troop_center", "trp_knight_1_8"),
  ##      (troop_get_slot,    ":cur_party_center", ":cur_party_fiefs", slot_troop_leaded_party),
  ##      (party_is_active,   ":cur_party_center"),
  ##      (party_slot_eq,     ":cur_party_center", slot_party_type, spt_kingdom_hero_party),
  ##      (neg|party_slot_eq,   ":cur_party_center", slot_party_ai_state, spai_accompanying_army),
  ##      (call_script, "script_party_set_ai_state", ":cur_party_center", spai_holding_center, "p_town_minas_tirith"),
  ##      (party_set_ai_behavior, ":cur_party_center",ai_bhvr_travel_to_party),
  ##      (party_set_ai_object,   ":cur_party_center", "p_town_minas_tirith"),
  ##    (try_end),
  ##    (display_message, "@Gondor has called for aide!"),
  ##    (assign, "$gondor_reinforcement_event", 1),
  ##   ]),
  
  
  
  ## Kham Gondor Reinforcement Event - Via script_succeed_quest #unused
  
  (24,
    [
      #(eq, "$cheat_mode",1),
      (eq, "$tld_war_began", 1),
      (eq, "$gondor_reinforcement_event",0),
      
      (faction_get_slot, ":strength", "fac_mordor", slot_faction_strength),
      (ge, ":strength", 3500),
      
      (try_begin),
        (party_is_active, "p_town_minas_tirith"),
        (call_script, "script_defend_center", "trp_knight_1_1", "p_town_minas_tirith"),
        (call_script, "script_defend_center", "trp_knight_1_2", "p_town_minas_tirith"),
        (call_script, "script_defend_center", "trp_knight_1_3", "p_town_minas_tirith"),
        (call_script, "script_defend_center", "trp_knight_1_4", "p_town_minas_tirith"),
        (call_script, "script_defend_center", "trp_knight_1_5", "p_town_minas_tirith"),
        (call_script, "script_defend_center", "trp_knight_1_6", "p_town_minas_tirith"),
        (call_script, "script_defend_center", "trp_knight_1_7", "p_town_minas_tirith"),
        (call_script, "script_defend_center", "trp_knight_1_8", "p_town_minas_tirith"),
        (call_script, "script_defend_center", "trp_knight_6_1", "p_town_minas_tirith"),
        (call_script, "script_defend_center", "trp_knight_6_2", "p_town_minas_tirith"),
      (try_end),
      
      (try_begin),
        (eq, "$gondor_reinforcement_event_menu",0),
        (store_faction_of_party, ":fac_player", "p_main_party"),
        (eq, ":fac_player", "fac_gondor"),
        (jump_to_menu, "mnu_gondor_reinforcement_event"),
        (assign, "$gondor_reinforcement_event_menu",1),
      (try_end),
      
      (try_begin),
        (eq, "$cheat_mode",1),
        (neq, "$g_fast_mode",1),
        (display_message, "@Gondor has called for aide!"),
      (try_end),
      (assign, "$gondor_reinforcement_event",1),
  ]),
  
  
  (12, #unused
    [
      #(eq, "$cheat_mode",1),
      (eq, "$tld_war_began", 1),
      (eq, "$gondor_reinforcement_event",1),
      
      (faction_get_slot, ":strength", "fac_mordor", slot_faction_strength),
      (ge, ":strength", 3500),
      
      (try_begin),
        (troop_get_slot, ":party", "trp_knight_1_3", slot_troop_leaded_party),
        (party_is_active, ":party"),
        (call_script, "script_accompany_marshall", "trp_knight_1_1", "trp_knight_1_3"),
        (call_script, "script_accompany_marshall", "trp_knight_1_2", "trp_knight_1_3"),
        (call_script, "script_accompany_marshall", "trp_knight_1_4", "trp_knight_1_3"),
        (call_script, "script_accompany_marshall", "trp_knight_1_5", "trp_knight_1_3"),
        (call_script, "script_accompany_marshall", "trp_knight_1_6", "trp_knight_1_3"),
        (call_script, "script_accompany_marshall", "trp_knight_1_7", "trp_knight_1_3"),
        (call_script, "script_accompany_marshall", "trp_knight_1_8", "trp_knight_1_3"),
        (call_script, "script_accompany_marshall", "trp_knight_6_1", "trp_knight_1_3"),
        (call_script, "script_accompany_marshall", "trp_knight_6_2", "trp_knight_1_3"),
      (try_end),
      
      (try_begin),
        (eq, "$cheat_mode",1),
        (neq, "$g_fast_mode",1),
        (display_message, "@Gondor is accompanying the marshall!"),
      (try_end),
      (assign, "$gondor_reinforcement_event",0),
  ]),
  
  
  
  ## Kham - War Council + Siege Reports Trigger + Check Followers
   ##InVain: disabled reports, not really necessary and buggy
  
  (12,[
      # (try_for_range, ":faction_wc", kingdoms_begin, kingdoms_end),
        # (neq, "$g_fast_mode", 1),
        # (faction_slot_eq, ":faction_wc", slot_faction_state, sfs_active), #Needs to be alive
        # (call_script, "script_get_faction_rank", ":faction_wc"),
        # (assign, ":rank", reg0), #rank points to rank number 0-9
        # (try_begin),
          # (faction_slot_eq, ":faction_wc", slot_faction_war_council, 0),
          # (ge, ":rank",8),
          # (jump_to_menu, "mnu_player_added_to_war_council"),
          # (faction_set_slot, ":faction_wc", slot_faction_war_council, 1),
        # (else_try),
          # (faction_slot_eq, ":faction_wc", slot_faction_allowed_follow, 2),
          # (ge, ":rank",7),
          # (jump_to_menu, "mnu_player_added_to_allow_follow"),
          # (faction_set_slot, ":faction_wc", slot_faction_allowed_follow, 3),
        # (else_try),
          # (faction_slot_eq, ":faction_wc", slot_faction_allowed_follow, 1),
          # (ge, ":rank",5),
          # (jump_to_menu, "mnu_player_added_to_allow_follow"),
          # (faction_set_slot, ":faction_wc", slot_faction_allowed_follow, 2),
        # (else_try),
          # (faction_slot_eq, ":faction_wc", slot_faction_siege_reports, 0),
          # (ge, ":rank", 4),
          # (faction_set_slot, ":faction_wc", slot_faction_siege_reports, 1),
          # (jump_to_menu, "mnu_player_added_to_siege_reports"),
        # (else_try),
          # (faction_slot_eq, ":faction_wc", slot_faction_allowed_follow, 0),
          # (ge, ":rank",3),
          # (jump_to_menu, "mnu_player_added_to_allow_follow"),
          # (faction_set_slot, ":faction_wc", slot_faction_allowed_follow, 1),
        # (try_end),
      # (try_end), #End Range
      
      
      (try_begin),
        (party_get_slot, ":num_followers", "p_main_party", slot_party_number_following_player),
        #(assign, reg65, ":num_followers"),
        #(display_message, "@Trigger - {reg65} followers", color_good_news),
        (ge, ":num_followers", 1),
        (store_current_hours, ":cur_time"),
        (call_script, "script_find_theater", "p_main_party"),
        (assign, ":current_theater", reg0), 
        
        (try_for_parties, ":followers"),
          (party_slot_eq, ":followers", slot_party_following_player, 1),
          (party_is_active, ":followers"),
          (party_get_slot, ":follow_until", ":followers", slot_party_follow_player_until_time),
          (party_get_slot, ":home_center", ":followers", slot_party_home_center),
          (store_faction_of_party, ":party_faction", ":followers"),
          (assign, ":continue", 0),
          (assign, ":release", 0),
          
          (try_begin),
            (ge, ":cur_time", ":follow_until"), #check time
            (assign, ":release", 1), 
          (else_try), #check theater
            (faction_get_slot, ":faction_theater", ":party_faction", slot_faction_active_theater),
            (faction_get_slot, ":home_theater", ":party_faction", slot_faction_home_theater),
            (neq, ":faction_theater", ":current_theater"),
            (neq, ":home_theater", ":current_theater"),
            (assign, ":release", 1), 
          (try_end), 
          
          (try_begin),
            (eq, ":release", 1), 
            (party_set_slot, ":followers", slot_party_following_player, 0),
            (party_set_slot, ":followers", slot_party_commander_party, -1),
            (call_script, "script_find_closest_random_enemy_center_from_center", ":home_center"),
            (try_begin),
              (neq, reg0, -1),
              (assign, ":enemy_center", reg0),
              (party_get_position, pos1, ":home_center"),
              (party_get_position, pos2, ":enemy_center"),
              (call_script, "script_calc_quarter_point"), # closer to home
            (else_try),
              (party_get_position, pos1, ":home_center"),
            (try_end),
            (party_set_slot, ":followers", slot_party_ai_object, ":enemy_center"),
            (party_set_slot, ":followers", slot_party_ai_state, spai_undefined),
            (party_set_ai_behavior, ":followers", ai_bhvr_patrol_location),
            (party_set_ai_target_position, ":followers", pos1),
            (party_set_ai_patrol_radius, ":followers", 10),
            (str_store_party_name, s5, ":followers"),
            (display_message, "@{s5} has stopped following you."),
          (else_try),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          
          (assign, ":scouts", 0),
          (assign, ":raider", 0),
          (assign, ":war_party", 0),
          
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
      (try_end),
      
  ]),
  
  ## Kham Gondor Reinforcement Event - Let them patrol around the center
  
  ## Kham Denethor Sends Faramir to West Osgiliath
  
  ## Kham Gondor hero hears  the Horn of Gondor (Lore Trigger)
  
  ## Kham Isengard Hero sees Isengards Crebains (Lore Trigger)
  
  
  
  #Kham - Cannibalsim / Elven Migration Trigger Start
  (36,
    [


      #(eq, "$cheat_mode", 1),
      (try_begin),
        (troop_slot_eq, "trp_player", slot_troop_state, 0),
        (store_random_in_range, ":random",0,100), #Chance to trigger
        (try_begin),
          (map_free),
          (party_get_num_companions, ":size", "p_main_party"),
          (gt, ":size", 15), #Don't trigger if less than 15 troops
          #(assign, reg6, ":random"),
          #(display_message, "@Random Number - {reg6}", color_good_news),
          (faction_get_slot, ":side", "$players_kingdom", slot_faction_side),
          (party_get_morale, ":morale", "p_main_party"),
          
          (try_begin), #Now we check if we are going to cannibalize or elves wanna go west
            (neq, ":side", faction_side_good), #Evil only
            (le, ":random", 45), #45% chance to trigger
            (call_script, "script_are_there_orcs", "p_main_party"), #Are there orcs/uruks?
            (gt, reg0, 0),
            
            #(gt, "$g_player_party_morale_modifier_no_food", 0), #No food

            # TLD Kham: Change the above to check for food:
            (assign, ":available_food", 0),
            (try_begin),
              (item_set_slot, "itm_horse_meat", slot_item_is_checked, 0),
              (call_script, "script_cf_player_has_item_without_modifier", "itm_horse_meat", imod_rotten),
              (val_add, ":available_food", 1),
            (try_end),
            (try_for_range, ":cur_food", food_begin, food_end),
              (item_set_slot, ":cur_food", slot_item_is_checked, 0),
              (call_script, "script_cf_player_has_item_without_modifier", ":cur_food", imod_rotten),
              (val_add, ":available_food", 1),
            (try_end),
            (lt, ":available_food", 0), #No food at all.
            (jump_to_menu, "mnu_hungry_orc"),

          (else_try),
            (assign, ":chance", 30), #Base chance for it occurring
            (try_begin), #The conditions that reduce likelihood of triggering start here
              (is_between, "$current_player_region", region_lebennin, region_n_ithilien),
              (val_add, ":chance",10),
            (try_end),
            (try_begin),
              (troop_slot_eq, "trp_traits", slot_trait_elf_friend, 1),
              (val_sub, ":chance", 10),
            (try_end),
            (call_script, "script_are_there_elves", "p_main_party"),
            (gt, reg0,0),
            (le, ":random", ":chance"),
            (le, ":morale", low_party_morale),
            (jump_to_menu, "mnu_leaving_elf"),
          (try_end),
        (try_end),
      (else_try),
        (troop_set_slot, "trp_player", slot_troop_state, 0),
      (try_end),
  ]),
  
  # Update Active Theaters Trigger
  
  (24,
    [
      (ge, "$tld_war_began", 1),
      
      #(display_message, "@DEBUG: Update Active Theaters Trigger Fired", color_good_news),
      
      #Check if there are any factions that retreated.
      
      (try_for_range, ":retreated_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":retreated_faction", slot_faction_state, sfs_active),
        (faction_get_slot, ":theater_retreated_from", ":retreated_faction", slot_faction_theater_retreated_from),
        (gt, ":theater_retreated_from", 0), #must have retreated
        (faction_get_slot, ":current_active_theater", ":retreated_faction", slot_faction_active_theater),
        (call_script, "script_find_next_theater", ":retreated_faction", ":current_active_theater"), #Check Next Theater from retreated faction's home theater
        (assign, ":next_theater_after_home", reg0),
        
        (try_begin),
          (eq, "$tld_war_began", 2),
          (call_script, "script_wott_check_active_factions_in_theater", ":next_theater_after_home", ":retreated_faction"),
        (else_try),
          (call_script, "script_check_active_factions_in_theater", ":next_theater_after_home", ":retreated_faction"),
        (try_end),
        (assign, ":factions_still_active_1", reg0),
        (call_script, "script_check_active_advance_camps", ":next_theater_after_home", ":retreated_faction"), #Check if there are any adv camps there
        (assign, ":adv_camps_still_present_1", reg0),
        
        # We first will check if the next theater from home has enemies. If there are, move active theater there.
        # If there are no more enemies there, we move to the one after. Even if there are no enemies there,
        # it is fine, because the update theater script will run right after.
        # Example: Mordor retreated from Center Theater. Next Theater from home is Rohan
        # If there are enemies there, then move to Rohan. If not, look for the next theater after Rohan and move there.
        
        (try_begin),
          (this_or_next|eq, ":factions_still_active_1", 0), #There are still active factions there
          (eq, ":adv_camps_still_present_1", 0), #Or there are still advance camps
          (faction_set_slot, ":retreated_faction", slot_faction_active_theater, ":theater_retreated_from"), #set this as their active theater
          (assign, ":final_theater", ":theater_retreated_from"),
        (else_try), #There are no more enemies in the next theater
          (call_script, "script_find_next_theater", ":retreated_faction", ":next_theater_after_home"), #Check the 3rd theater
          (assign, ":third_theater", reg0),
          (faction_set_slot, ":retreated_faction", slot_faction_active_theater, ":third_theater"), #set their active theater to the third theater.
          (assign, ":final_theater", ":third_theater"),
        (try_end),
        
        (call_script, "script_theater_name_to_s15", ":final_theater"),
        (str_store_faction_name, s2, ":retreated_faction"),
        (try_begin),
          (store_relation, ":rel", "$players_kingdom", ":retreated_faction"),
          (gt, ":rel", 0),
          (assign, ":news_color", color_good_news),
        (else_try),
          (assign, ":news_color", color_bad_news),
        (try_end),
        
        (store_current_hours, ":cur_hours"),
        (val_add, ":cur_hours", 10*24), #10 day penalty when defeated.
        
        (display_log_message, "@The forces of {s2} have regrouped and march on to {s15}!", ":news_color"),
        (faction_set_slot, ":retreated_faction", slot_faction_advcamp_timer, ":cur_hours"), #set the timer for camp creation
        (faction_set_slot, ":retreated_faction", slot_faction_theater_retreated_from, 0), #reset retreated slot
      (try_end),
      
      # Run the Update Theaters Script again to move adv camps when a theater has been cleared before a faction gets defeated.
      
      (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction", slot_faction_state, sfs_active),
        (faction_get_slot, ":faction_theater", ":faction", slot_faction_active_theater),
        (try_begin),
          (eq, "$tld_war_began", 2),
          (call_script, "script_wott_check_active_factions_in_theater", ":faction_theater", ":faction"),
        (else_try),
          (call_script, "script_check_active_factions_in_theater", ":faction_theater", ":faction"),
        (try_end),
        (eq, reg0, 1),
        (call_script, "script_check_active_advance_camps", ":faction_theater", ":faction"),
        (eq, reg0, 1),
        (assign, ":theater_cleared", 1),
      (try_end),
      
      (eq, ":theater_cleared", 1),
      (call_script, "script_update_active_theaters"),
      
      
  ]),
  
  #Intro Quest Trigger
  
  (2, [
      (eq, "$tld_war_began", 1),
      (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
      (quest_slot_eq, "qst_tld_introduction", slot_quest_current_state, 0),
      (jump_to_menu, "mnu_evil_war_tutorial"),
      (quest_set_slot, "qst_tld_introduction", slot_quest_current_state, 1),]
  ),
  
  #lore events trigger
  
  (7, [
      (faction_get_slot, ":player_side", "$players_kingdom", slot_faction_side),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_get_slot, ":fac_strength", ":faction_no", slot_faction_strength),
        (neg|faction_slot_eq, ":faction_no", slot_faction_state, sfs_defeated),
        
        (try_begin), #Isengard Last Stand
            (eq, "$lore_mode", 1),
            (eq, ":faction_no", fac_isengard),
            (le, ":fac_strength", fac_str_guardian),
            (neg|check_quest_active, qst_guardian_party_quest),
            (neg|check_quest_finished, qst_guardian_party_quest),
            (eq, ":player_side", faction_side_good),
            (faction_slot_ge, fac_rohan, fac_str_ok), #Rohan still okay?
            (call_script, "script_find_theater", "p_main_party"),
            (eq, reg0, theater_SW), #player in Rohan?
            (call_script, "script_send_on_conversation_mission", tld_cc_gandalf_rohan_quest_start),
        (try_end),

      (try_end), #end faction loop
  ]),
  
  # Encounter Effects Trigger - InVain & Kham

  (5, [

] + (is_a_wb_trigger==1 and [
    (assign, ":continue", 0),
    (ge, "$tld_war_began", 1), #Only happens during war

    (eq, "$battle_encounter_effects", 1), #Toggle

    (try_begin),
      (party_slot_eq, "p_main_party", slot_party_battle_encounter_effect, NO_EFFECT_PRESENT),
      (store_random_in_range, ":rand_prob", 0, 100),
      (le, ":rand_prob", 65), #65% base chance of happening. 
      (assign, ":continue", 1),
    (else_try),
      (party_set_slot, "p_main_party", slot_party_battle_encounter_effect, NO_EFFECT_PRESENT),
      (set_global_cloud_amount, 0), # Clear Cloudiness
      #(display_message, "@EFFECTS CLEARED", color_bad_news),
    (try_end),

    (eq, ":continue", 1),


    (call_script, "script_get_region_of_party", "p_main_party"),
    (assign, ":region", reg1),

    (faction_get_slot, ":mordor_strength", "fac_mordor", slot_faction_strength),
    (store_div, ":chance_darkness", ":mordor_strength", 200),

    (faction_get_slot, ":isengard_strength", "fac_isengard", slot_faction_strength),
    (store_div, ":chance_storm", ":isengard_strength", 200),

    (faction_get_slot, ":guldur_strength", "fac_guldur", slot_faction_strength),
    (store_div, ":chance_fog", ":guldur_strength", 200),

    (faction_get_slot, ":lorien_strength", "fac_lorien", slot_faction_strength),
    (store_div, ":chance_mist", ":lorien_strength", 200),

    (store_random_in_range, ":random_chance", 0, 100),

    (party_get_position, pos5, "p_main_party"),

    
    (try_begin), # LORIEN MIST
      (faction_slot_eq, "fac_lorien", slot_faction_state, sfs_active),
      (party_get_position, pos6, "p_town_caras_galadhon"),
      (party_get_position, pos7, "p_town_cerin_dolen"),
      (party_get_position, pos8, "p_town_cerin_amroth"),
      (assign, ":continue_lorien", 0),
      (try_begin),
        (get_distance_between_positions_in_meters, ":distance_lorien", pos5, pos6),
        (le, ":distance_lorien", 12),
        (assign, ":continue_lorien", 1),
      (else_try),
        (get_distance_between_positions_in_meters, ":distance_lorien", pos5, pos7),
        (le, ":distance_lorien", 12),
        (assign, ":continue_lorien", 1),
      (else_try),
        (get_distance_between_positions_in_meters, ":distance_lorien", pos5, pos8),
        (le, ":distance_lorien", 12),
        (assign, ":continue_lorien", 1),
      (try_end),
      (eq, ":continue_lorien", 1),
      (lt, ":random_chance", ":chance_mist"),
      (party_set_slot, "p_main_party", slot_party_battle_encounter_effect, LORIEN_MIST),
      #(display_message, "@LORIEN_MIST", color_good_news),

    
    (else_try), #SAURON DARKNESS
      (faction_slot_eq, "fac_mordor", slot_faction_state, sfs_active),
      (this_or_next|eq, ":region", region_dagorlad),
      (is_between, ":region", region_n_ithilien, region_druadan_forest),
      (lt, ":random_chance", ":chance_darkness"),
      (party_set_slot, "p_main_party", slot_party_battle_encounter_effect, SAURON_DARKNESS),
      #(display_message, "@SAURON_DARKNESS", color_good_news),

    (else_try), #SARUMAN STORM
      (faction_slot_eq, "fac_isengard", slot_faction_state, sfs_active),
      (party_get_position, pos6, "p_town_isengard"),
      (party_get_position, pos7, "p_town_troll_cave"),
      (party_get_position, pos8, "p_town_moria"),
      (party_get_position, pos9, "p_town_goblin_north_outpost"),
      (assign, ":continue_saruman", 0),
      (try_begin),
        (get_distance_between_positions_in_meters, ":distance_saruman", pos5, pos6),
        (le, ":distance_saruman", 200),
        (assign, ":continue_saruman", 1),
      (else_try),
        (get_distance_between_positions_in_meters, ":distance_saruman", pos5, pos7),
        (le, ":distance_saruman", 200),
        (assign, ":continue_saruman", 1),
      (else_try),
        (get_distance_between_positions_in_meters, ":distance_saruman", pos5, pos8),
        (le, ":distance_saruman", 200),
        (assign, ":continue_saruman", 1),
      (else_try),
        (get_distance_between_positions_in_meters, ":distance_saruman", pos5, pos9),
        (le, ":distance_saruman", 200),
        (assign, ":continue_saruman", 1),
      (try_end),
      (eq, ":continue_saruman", 1),
      (lt, ":random_chance", ":chance_storm"),
      (party_set_slot, "p_main_party", slot_party_battle_encounter_effect, SARUMAN_STORM),
      (set_rain, 1, 500),
      #(display_message, "@DEBUG: SARUMAN_STORM", color_good_news),

    (else_try), #GULDUR FOG
      (faction_slot_eq, "fac_guldur", slot_faction_state, sfs_active),
      (party_get_position, pos6, "p_town_dol_guldur"),
      (party_get_position, pos7, "p_town_dol_guldur_north_outpost"),
      (assign, ":continue_guldur", 0),
      (try_begin),
        (get_distance_between_positions_in_meters, ":distance_guldur", pos5, pos6),
        (le, ":distance_guldur", 12),
        (assign, ":continue_guldur", 1),
      (else_try),
        (get_distance_between_positions_in_meters, ":distance_guldur", pos5, pos7),
        (le, ":distance_guldur", 12),
        (assign, ":continue_guldur", 1),
      (try_end),
      (eq, ":continue_guldur", 1),
      (lt, ":random_chance", ":chance_fog"),
      (party_set_slot, "p_main_party", slot_party_battle_encounter_effect, GULDUR_FOG),
      #(display_message, "@DEBUG: GULDUR_FOG", color_good_news),
    
    (try_end),
  ] or [ ]) + [

]),

# Quest Helper Trigger 

  
(12, 

  [
    
    (try_begin),
      (check_quest_active, "qst_eliminate_patrols"),
      (neg|check_quest_concluded, "qst_eliminate_patrols"),
      (quest_get_slot, ":target", "qst_eliminate_patrols", slot_quest_target_party_template),
      (quest_get_slot, ":center", "qst_eliminate_patrols", slot_quest_target_center),
	  (quest_get_slot, ":target_amount", "qst_eliminate_patrols", slot_quest_target_amount),
	  (quest_get_slot, ":defeated", "qst_eliminate_patrols", slot_quest_current_state),
	  (lt, ":defeated", ":target_amount"), #Additional check. The above neg|check_quest_concluded doesn't seem to work, parties kept spawning. 
      (gt, ":center", 0),
	  (call_script, "script_find_theater", ":center"), #only spawn armies if the player is in the theater
	  (assign, ":center_theater", reg0),
	  (call_script, "script_find_theater", "p_main_party"),
	  (eq, reg0, ":center_theater"), 
      (set_spawn_radius, 10),
      (spawn_around_party, "p_main_party", ":target"),
      (str_store_party_name, s2, reg0),
      (str_store_party_name, s3, ":center"),
	  (party_get_skill_level, ":spotting", "p_main_party", skl_spotting),
	  (party_get_skill_level, ":tracking", "p_main_party", skl_tracking),
	  (store_add, ":report_chance", ":tracking", ":spotting"),
	  (store_random_in_range, ":random", 1, 21), #10 spotting and 10 tracking = 100% spotting chance
      (try_begin),
        (le, ":random", ":report_chance"),
        (display_message, "@Your scouts report signs of a {s2} nearby."),
      (try_end),
    (try_end),
      
    # Looters for Deal With Looters Quest
    (try_begin),
      (check_quest_active, "qst_deal_with_looters"),
      (neg|check_quest_concluded, "qst_deal_with_looters"),
      (quest_get_slot, ":party_template", "qst_deal_with_looters", slot_quest_target_party_template),
	  (quest_get_slot, ":target_center", "qst_deal_with_looters", slot_quest_target_center),
	  (quest_get_slot, ":target_amount", "qst_deal_with_looters", slot_quest_target_amount),
	  (quest_get_slot, ":defeated", "qst_deal_with_looters", slot_quest_current_state),
	  (lt, ":defeated", ":target_amount"), #Additional check. The above neg|check_quest_concluded doesn't seem to work, parties kept spawning. 
	  (gt, ":target_center", 0),
	  (store_distance_to_party_from_party, ":distance", "p_main_party", ":target_center"),
	  (le, ":distance", 25), #only spawn looters if the player is still in the area
      (set_spawn_radius, 7),
      (spawn_around_party, ":target_center", ":party_template"),
      (party_set_flags, reg0, pf_quest_party, 1),
      (party_set_faction, reg0, "fac_deserters"), #Kham: so they don't get into fights
      #(display_message, "@DEBUG: Looter party spawned"),
    (try_end),

    (try_begin),
      (check_quest_active, "qst_blank_quest_17"),
      (neg|check_quest_concluded, "qst_blank_quest_17"),
      (quest_get_slot, ":target_template", "qst_blank_quest_17", slot_quest_target_party_template),
      (quest_get_slot, ":target_troop", "qst_blank_quest_17", slot_quest_target_troop),
	  (quest_get_slot, ":target_amount", "qst_blank_quest_17", slot_quest_target_amount),
	  (quest_get_slot, ":defeated", "qst_blank_quest_17", slot_quest_current_state),
	  (quest_get_slot, ":target_center", "qst_blank_quest_17", slot_quest_target_center),
	  (lt, ":defeated", ":target_amount"), #Additional check. The above neg|check_quest_concluded doesn't seem to work, parties kept spawning. 
      (store_distance_to_party_from_party, ":distance", "p_main_party", ":target_center"),
	  (le, ":distance", 25), #only spawn looters if the player is still in the area
	  (set_spawn_radius, 7),
	  (store_random_in_range, ":parties_to_spawn", 1, 3),
	  (try_for_range, ":unused", 0,":parties_to_spawn"),
		(spawn_around_party, ":target_center", ":target_template"),
		(assign, ":spawned", reg0),
		(party_set_flags, ":spawned", pf_quest_party, 1),
		(party_set_faction, ":spawned", "fac_deserters"), #Kham: so they don't get into fights
		(store_random_in_range, ":rand", 8, 15),
		(party_force_add_members, ":spawned", ":target_troop", ":rand"),
	  (try_end),
    (try_end),
      
]),

  
  
  ##############################################
  #trigger reserved for future save game compatibility
  
  #trigger reserved for future save game compatibility
  #(999,[]),   #Replaced by Gondor Reinforcement Event
  #trigger reserved for future save game compatibility
  #(999,[]),   # replaced by War council trigger
  #trigger reserved for future save game compatibility
  #(999,[]),   # Replaced by cannibalism trigger
  #trigger reserved for future save game compatibility
  #(999,[]), #Replaced by Update Theaters trigger
  #trigger reserved for future save game compatibility
  #(999,[]),   #Replaced by Evil Intro Quest event
  #trigger reserved for future save game compatibility
  #(999,[]), # Replaced by guardian party quest
  #trigger reserved for future save game compatibility
  #(999,[]), # Replaced by Battle Encounter Effects
  
  #trigger reserved for future save game compatibility
  #(999,[]),  # Replaced by Quest Helper Spawns
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  #trigger reserved for future save game compatibility
  (999,[]),
  
]

