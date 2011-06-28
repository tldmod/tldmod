from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *

from module_constants import *

####################################################################################################################
# Simple triggers are the alternative to old style triggers. They do not preserve state, and thus simpler to maintain.
#
#  Each simple trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference. 
####################################################################################################################



simple_triggers = [

# This trigger is deprecated. Use "script_game_event_party_encounter" in module_scripts.py instead  
  (ti_on_party_encounter,[]),

# This trigger is deprecated. Use "script_game_event_simulate_battle" in module_scripts.py instead 
  (ti_simulate_battle,[]),

  (1,[(gt,"$auto_besiege_town",0),
      (gt,"$g_player_besiege_town", 0),
      (ge, "$g_siege_method", 1),
      (store_current_hours, ":cur_hours"),
      (eq, "$g_siege_force_wait", 0),
      (ge, ":cur_hours", "$g_siege_method_finish_hours"),
      (neg|is_currently_night),
      (rest_for_hours, 0, 0, 0), #stop resting
    ]),

  (0,[(eq,"$g_player_is_captive",1),
      (gt, "$capturer_party", 0),
      (party_is_active, "$capturer_party"),
      (party_relocate_near_party, "p_main_party", "$capturer_party", 0),
    ]),

#Auto-menu
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
         (assign, "$g_player_icon_state", pis_normal),
         (display_message, "@Breaking camp..."),
       (try_end),
     (try_end),
     ]),


#Notification menus
  (0,[
     (troop_slot_ge, "trp_notification_menu_types", 0, 1),
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

  #Music,
  (1,[(map_free),(call_script, "script_music_set_situation_with_culture", mtf_sit_travel),]),

#Player raiding a village
# This trigger will check if player's raid has been completed and will lead control to village menu.
# commented by GA, village removal
#  (1,[
#      (ge,"$g_player_raiding_village",1),
#      (try_begin),
#        (neq, "$g_player_is_captive", 0),
#        (rest_for_hours, 0, 0, 0), #stop resting - abort
#        (assign,"$g_player_raiding_village",0),
#      (else_try),
#        (map_free), #we have been attacked during raid
#        (assign,"$g_player_raiding_village",0),
#      (else_try),
#        (this_or_next|party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_looted),
#        (party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_deserted),
#        (start_encounter, "$g_player_raiding_village"),
#        (rest_for_hours, 0),
#        (assign,"$g_player_raiding_village",0),
#        (assign,"$g_player_raid_complete",1),
#      (else_try),
#        (party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_being_raided),
#        (rest_for_hours, 3, 5, 1), #rest while attackable
#      (else_try),
#        (rest_for_hours, 0, 0, 0), #stop resting - abort
#        (assign,"$g_player_raiding_village",0),
#        (assign,"$g_player_raid_complete",0),
#      (try_end),
#    ]),

  #Pay day, every four days here
  (24.1 * 4,
   [ (call_script, "script_make_player_pay_upkeep"),
   ]),
   
  (24,
   [ (call_script, "script_rank_income_to_player"),

	 (try_for_range, ":center_no", centers_begin, centers_end),               # TLD clear rumors in centers
	   (try_for_range, ":walker", town_walker_entries_start, town_walker_entries_start+num_town_walkers),
	       (store_add, ":slot", slot_center_rumor_check_begin,":walker"),
		   (party_set_slot, ":center_no", ":slot", 0),
       (try_end),
	 (try_end),
	 (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),  # TLD clear rumors in lords
         (troop_set_slot, ":troop_no", slot_troop_rumor_check, 0),
     (try_end),
	 (try_for_range, ":troop_no", armor_merchants_begin, village_elders_end), # TLD clear rumors in merchants/elders
         (troop_set_slot, ":troop_no", slot_troop_rumor_check, 0),
     (try_end),
   ]),

  (4.15,
   [ (try_begin),
		(store_random_in_range, ":dieroll", 1,101), (lt,":dieroll",10),
		(call_script, "script_make_unpaid_troop_go"),
     (try_end),
   ]),

   # Reducing luck by 1 in every 180 hours
  (180,[(val_sub, "$g_player_luck", 1),(val_max, "$g_player_luck", 0),]),

  # Banner selection menu
  #GA: no custom banners in TLD
#  (24,[(eq, "$g_player_banner_granted", 1),
#       (troop_slot_eq, "trp_player", slot_troop_banner_scene_prop, 0),
#       (le,"$auto_menu",0),
#normal_banner_begin
#       (start_presentation, "prsnt_banner_selection"),
#custom_banner_begin
#    (start_presentation, "prsnt_custom_banner"),
#      ]),

  # Party Morale: Move morale towards target value.
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
  
  # keep track of main party region ("$current_player_region"), 
  # and display log messages keey player informed of what region is he in,   (mtarini)
  (0.5,[
    (party_get_position, pos1, "p_main_party"),
	(party_get_current_terrain, ":tt","p_main_party"),
	(call_script,"script_get_region_of_pos1", ":tt"),
	(assign, ":new_region", reg1),
	(neq, "$current_player_region", ":new_region"), # region change!
	
	(try_begin), 
		# regions without a clear name
		(this_or_next|eq, ":new_region", region_above_mirkwook), 
		(this_or_next|eq, ":new_region", region_anduin_banks), 
		(eq,":new_region",-1),
		
		(try_begin),
			(gt, "$current_player_region", -1),
			(store_add, reg2, str_shortname_region_begin , "$current_player_region"),
			(str_store_string,s1,reg2),
			(display_log_message, "@you have left {s1}"),
		(try_end),
    (else_try),
		(store_add, reg2, str_shortname_region_begin, ":new_region"),
		(str_store_string,s1,reg2),
		(call_script, "script_region_get_faction", ":new_region"),
		(try_begin), 
			(gt, reg1, -1),
			(str_store_faction_name, s2, reg1),
			(display_log_message, "@you are entering {s1} ({s2})"),
		(else_try),
			(display_log_message, "@you are entering {s1}"),
		(try_end),
	(try_end),
	(assign, "$current_player_region", ":new_region"),	
  ]),

#Party AI: pruning some of the prisoners in each center (once a week)
(24*7,[(try_for_range, ":center_no", centers_begin, centers_end),
         (party_is_active, ":center_no"), #TLD
         (party_get_num_prisoner_stacks, ":num_prisoner_stacks",":center_no"),
         (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
           (party_prisoner_stack_get_troop_id, ":stack_troop",":center_no",":stack_no"),
           (neg|troop_is_hero, ":stack_troop"),
           (party_prisoner_stack_get_size, ":stack_size",":center_no",":stack_no"),
           (store_random_in_range, ":rand_no", 0, 40),
           (val_mul, ":stack_size", ":rand_no"),
           (val_div, ":stack_size", 100),
           (party_remove_prisoners, ":center_no", ":stack_troop", ":stack_size"),
         (try_end),
       (try_end),
    ]),

 
  #Hiring men with center wealths (once a day)
  (24,[
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (ge, ":party_no", 1),
        (party_is_active, ":party_no"), #MV
        (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party), #TLD: only hosts reinforce
        (party_get_attached_to, ":cur_attached_party", ":party_no"),
        (is_between, ":cur_attached_party", centers_begin, centers_end),
        (party_slot_eq, ":cur_attached_party", slot_center_is_besieged_by, -1), #center not under siege
        (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"), #Hiring men up to lord-specific limit
      (try_end),
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         (party_is_active, ":center_no"), #TLD
         (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center does not belong to player.
         (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
         (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD - not destroyed - redundant since (party_is_active, ":center_no")
         # (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
         # (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #center not under siege
         # (assign, ":hiring_budget", ":cur_wealth"),
         # (val_div, ":hiring_budget", 5),
         # (gt, ":hiring_budget", reinforcement_cost),
         
		 (call_script, "script_refresh_volunteers_in_town", ":center_no"),
         
         #TLD: above replaced by this
         (party_get_slot, ":garrison_limit", ":center_no", slot_center_garrison_limit),
         (party_get_num_companions, ":garrison_size", ":center_no"),
         (gt, ":garrison_limit", ":garrison_size"),
         
         (call_script, "script_cf_reinforce_party", ":center_no"),
		 
         # (val_sub, ":cur_wealth", reinforcement_cost),
         # (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
       (try_end),
    ]),

  #Converging center prosperity to ideal prosperity once in every 15 days
  (24*15,
   [(try_for_range, ":center_no", centers_begin, centers_end),
      (party_is_active, ":center_no"), #TLD
      (call_script, "script_get_center_ideal_prosperity", ":center_no"),
      (assign, ":ideal_prosperity", reg0),
      (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
      (try_begin),
        (gt, ":prosperity", ":ideal_prosperity"),
        (call_script, "script_change_center_prosperity", ":center_no", -1),
      (else_try),
        (lt, ":prosperity", ":ideal_prosperity"),
        (call_script, "script_change_center_prosperity", ":center_no", 1),
      (try_end),
    (try_end),
    ]),

  #Checking if the troops are resting at a half payment point (this has to stay, in TLD!)
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
      (is_between, "$g_last_rest_center", walled_centers_begin, walled_centers_end),
      (assign, ":resting_at_manor_or_walled_center", 1),
    (try_end),
    (eq, ":resting_at_manor_or_walled_center", 0),
    (assign, "$g_half_payment_checkpoint", 0),
    ]),


  # Give some xp to hero parties
  (48,[(try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
         (store_random_in_range, ":rand", 0, 100),
         (lt, ":rand", 30),
         (troop_get_slot, ":hero_party", ":troop_no", slot_troop_leaded_party),
         (gt, ":hero_party", centers_end),
         (party_is_active, ":hero_party"),
         (store_skill_level, ":trainer_level", skl_trainer, ":troop_no"),
         (val_add, ":trainer_level", 2),
         (store_mul, ":xp_gain", ":trainer_level", 500),
         (party_upgrade_with_xp, ":hero_party", ":xp_gain"),
       (try_end),
       
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         (party_is_active, ":center_no"), #TLD
         (store_random_in_range, ":rand", 0, 100),
         (lt, ":rand", 10),
         (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
         (neq, ":center_lord", "trp_player"),
         #(party_upgrade_with_xp, ":center_no", 3000),
       (try_end),
    ]),

# Process village raids
# commented by GA, village removal
#   (2,[(call_script, "script_process_village_raids"),]),

# MAIN AI STARTING POINT
# Decide faction ai by default every 36 hours
 (36,[(assign, "$g_recalculate_ais", 1),
     ]),
# Decide faction ai whenever flag is set
 (0,[ 
    (eq, "$g_recalculate_ais", 1),(ge,"$tld_war_began",1),
     (assign, "$g_recalculate_ais", 0),
     (call_script, "script_recalculate_ais"),
    ]),
# Count faction armies
 (24,[(try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":faction_no"),
      (try_end),
      
      #TLD, grow faction strength with time from center income
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),  
	     (faction_slot_ge,":faction_no",slot_faction_strength,1),
	     (faction_get_slot, ":strength", ":faction_no", slot_faction_strength_tmp),
         (faction_get_slot, ":debug_gain", ":faction_no", slot_faction_debug_str_gain), #debug
		 #(val_add,":strength",ws_faction_restoration), #old flat rate, obsolete
         (try_for_range, ":center_no", centers_begin, centers_end),
           (party_is_active, ":center_no"),
           (store_faction_of_party, ":center_faction", ":center_no"),
           (eq, ":center_faction", ":faction_no"), # center belongs to kingdom
           (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD - not destroyed - redundant
           (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #center not under siege
           (party_get_slot, ":strength_income", ":center_no", slot_center_strength_income),
           (try_begin),
             (eq, "$tld_war_began", 0),
             (val_div, ":strength_income", 2), #halve income before the War
             (store_mod, ":to_sub_for_rounding", ":strength_income", 5),
             (val_sub, ":strength_income", ":to_sub_for_rounding"), #keep it increments of 5
           (try_end),
           (val_add, ":strength", ":strength_income"),
           (val_add, ":debug_gain", ":strength_income"), #debug
         (try_end),
         (val_min, ":strength", 9999), #limit max strength
		 (faction_set_slot, ":faction_no", slot_faction_strength_tmp, ":strength"),
         (faction_set_slot, ":faction_no", slot_faction_debug_str_gain, ":debug_gain"), #debug
	  (try_end),
     ]),
# Decide vassal ai
# 7 hours in vanilla
 ( 3,[(try_begin),
        (ge,"$tld_war_began",1),  # vassal AI can change only if War started, GA
        (call_script, "script_init_ai_calculation"),
        (call_script, "script_decide_kingdom_party_ais"), # TLD, script modified to also decide if a lord spawns a host
	  (try_end),
     ]),
# Process vassal ai
 ( 2,[(call_script, "script_process_kingdom_parties_ai"),
     ]),
# Process sieges
 (24,[(try_begin),(ge,"$tld_war_began",1),(call_script, "script_process_sieges"),(try_end),
     ]),

# Changing readiness to join army
   (10,[(try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (assign, ":modifier", 1),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (try_begin),
          (gt, ":party_no", 0),
          (party_is_active,":party_no"),
          (party_get_slot, ":commander_party", ":party_no", slot_party_commander_party),
          (ge, ":commander_party", 0),
          (store_faction_of_party, ":faction_no", ":party_no"),
          (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
          (ge, ":faction_marshall", 0),
          (troop_get_slot, ":marshall_party", ":faction_marshall", slot_troop_leaded_party),
          (eq, ":commander_party", ":marshall_party"),
          (assign, ":modifier", -1),
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
  
  # Process alarms
   (3,[(call_script, "script_process_alarms"),
      ]),

  # Process siege ai
  (3,[(store_current_hours, ":cur_hours"),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_get_slot, ":besieger_party", ":center_no", slot_center_is_besieged_by),
        (gt, ":besieger_party", 0),
        (party_is_active, ":besieger_party"),
        (store_faction_of_party, ":besieger_faction", ":besieger_party"),
        (party_slot_ge, ":center_no", slot_center_is_besieged_by, 1),
        (party_get_slot, ":siege_begin_hours", ":center_no", slot_center_siege_begin_hours),
        (store_sub, ":siege_begin_hours", ":cur_hours", ":siege_begin_hours"),
        (assign, ":launch_attack", 0),
        (assign, ":call_attack_back", 0),
        (assign, ":attacker_strength", 0),
        (assign, ":marshall_attacking", 0),
        (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
          (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
          (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
          (gt, ":party_no", 0),
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
          (call_script, "script_party_calculate_regular_strength", ":party_no"),
          (val_add, ":attacker_strength", reg0),
        (try_end),
        (try_begin),
          (gt, ":attacker_strength", 0),
          (party_collect_attachments_to_party, ":center_no", "p_collective_enemy"),
          (call_script, "script_party_calculate_regular_strength", "p_collective_enemy"),
          (assign, ":defender_strength", reg0),
          (try_begin),
            (eq, "$auto_enter_town", ":center_no"),
            (eq, "$g_player_is_captive", 0),
            (call_script, "script_party_calculate_regular_strength", "p_main_party"),
            (val_add, ":defender_strength", reg0),
            (val_mul, ":attacker_strength", 2), #double the power of attackers if the player is in the campaign
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
          (store_sub, ":random_up_limit", ":strength_ratio", 300),
          (try_begin),
            (gt, ":random_up_limit", -100), #never attack if the strength ratio is less than 200%
            (store_div, ":siege_begin_hours_effect", ":siege_begin_hours", 3),
            (val_add, ":random_up_limit", ":siege_begin_hours_effect"),
          (try_end),
          (val_div, ":random_up_limit", 5),
          (val_max, ":random_up_limit", 0),
          (store_sub, ":random_down_limit", 200, ":strength_ratio"),
          (val_max, ":random_down_limit", 0),
          (try_begin),
            (store_random_in_range, ":rand", 0, 100),
            (lt, ":rand", ":random_up_limit"),
            (gt, ":siege_begin_hours", 24),#initial preparation
            (assign, ":launch_attack", 1),
          (else_try),
            (store_random_in_range, ":rand", 0, 100),
            (lt, ":rand", ":random_down_limit"),
            (assign, ":call_attack_back", 1),
          (try_end),
        (else_try),
          (assign, ":call_attack_back", 1),
        (try_end),
        (try_begin),
          (eq, ":launch_attack", 1),
          (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
            (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
            #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
            (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
            (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
            (gt, ":party_no", 0),

            (assign, ":continue", 0),
            (try_begin),
              (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
              (party_slot_eq, ":party_no", slot_party_ai_object, ":center_no"),
              (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
              (assign, ":continue", 1),
            (else_try),
              (party_get_slot, ":commander_party", ":party_no", slot_party_commander_party),
              (gt, ":commander_party", 0),
              (party_is_active, ":commander_party"),
              (party_slot_eq, ":commander_party", slot_party_ai_state, spai_besieging_center),
              (party_slot_eq, ":commander_party", slot_party_ai_object, ":center_no"),
              (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":center_no"),
              (assign, ":continue", 1),
            (try_end),
            (eq, ":continue", 1),

            (party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
            (party_set_ai_object, ":party_no", ":center_no"),
            (party_set_flags, ":party_no", pf_default_behavior, 1),
            (party_set_slot, ":party_no", slot_party_ai_substate, 1),
          (try_end),
        (else_try),
          (eq, ":call_attack_back", 1),
          (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
            (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
            #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
            (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
            (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
            (gt, ":party_no", 0),
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

  # Reset hero quest status
  # Change hero relation
 (12,[(try_for_range, ":troop_no", heroes_begin, heroes_end),
        (troop_set_slot, ":troop_no", slot_troop_does_not_give_quest, 0),
      (try_end),
     
      (try_for_range, ":troop_no", mayors_begin, mayors_end),
        (troop_set_slot, ":troop_no", slot_troop_does_not_give_quest, 0),
      (try_end),
     ]),

  # Refresh merchant inventories
  # commented by GA, village removal
  # (24,
  # [  (try_for_range, ":village_no", villages_begin, villages_end),
  #      (call_script, "script_refresh_village_merchant_inventory", ":village_no"),
  #    (try_end),
  #  ]),

  #Refreshing village defenders
  #Clearing slot_village_player_can_not_steal_cattle flags
  # commented by GA, village removal
  # (48,[(try_for_range, ":village_no", villages_begin, villages_end),
  #        (call_script, "script_refresh_village_defenders", ":village_no"),
  #        (party_set_slot, ":village_no", slot_village_player_can_not_steal_cattle, 0),
  #      (try_end),
  #     ]),

  # Refresh number of cattle in villages
  # commented by GA, village removal
  #(24,[(try_for_range, ":village_no", villages_begin, villages_end),
  #    (party_get_slot, ":num_cattle", ":village_no", slot_village_number_of_cattle),
  #    (store_random_in_range, ":random_no", 0, 100),
  #    (try_begin),
  #      (lt, ":random_no", 3),#famine
  #      (assign, ":num_cattle", 0),
  #      (try_begin),
#          (eq, "$cheat_mode", 1),
#          (str_store_party_name, s1, ":village_no"),
#          (display_message, "@Cattle in {s1} are exterminated due to famine."),
  #      (try_end),
  #    (else_try),
  #      (lt, ":random_no", 10),#double growth
  #      (store_random_in_range, ":random_no", 111, 121),
  #      (val_mul, ":num_cattle", ":random_no"),
  #      (val_div, ":num_cattle", 100),
  #      (store_random_in_range, ":random_no", 1, 3),
  #      (val_add, ":num_cattle", ":random_no"),
  #    (else_try),
  #      (lt, ":random_no", 50),#negative growth
  #      (store_random_in_range, ":random_no", 3, 8),
  #      (val_sub, ":num_cattle", ":random_no"),
  #    (else_try),#positive growth
  #      (store_random_in_range, ":random_no", 101, 111),
  #      (val_mul, ":num_cattle", ":random_no"),
  #      (val_div, ":num_cattle", 100),
  #      (store_random_in_range, ":random_no", 1, 3),
  #      (val_add, ":num_cattle", ":random_no"),
  #    (try_end),
  #    (val_clamp, ":num_cattle", 0, 101),
  #    (party_set_slot, ":village_no", slot_village_number_of_cattle, ":num_cattle"),
  #    #Reassigning the cattle production in the village
  #    (store_sub, ":production", ":num_cattle", 10),
  #    (val_div, ":production", 2),
  #    (call_script, "script_center_change_trade_good_production", ":village_no", "itm_cattle_meat", ":production", 0),
  #  (try_end),
  #  ]),

  # Accumulate taxes every week
#TLD: removed
   # (24 * 7,
   # [  (try_for_range, ":center_no", centers_begin, centers_end),
        # (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
        # (assign, ":cur_rents", 0),
        # (try_begin),
          # (party_slot_eq, ":center_no", slot_party_type, spt_village),
          # (try_begin),
            # (party_slot_eq, ":center_no", slot_village_state, svs_normal),
            # (assign, ":cur_rents", 500),
          # (try_end),
        # (else_try),
          # (party_slot_eq, ":center_no", slot_party_type, spt_castle),
          # (assign, ":cur_rents", 250),
        # (else_try),
          # (party_slot_eq, ":center_no", slot_party_type, spt_town),
          # (assign, ":cur_rents", 1000),
        # (try_end),
        # (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
        # (store_add, ":multiplier", 10, ":prosperity"),
        # (val_mul, ":cur_rents", ":multiplier"),
        # (val_div, ":cur_rents", 110),#Prosperity of 100 gives the default values
        # (val_add, ":accumulated_rents", ":cur_rents"),
        # (party_set_slot, ":center_no", slot_center_accumulated_rents, ":accumulated_rents"),
      # (try_end),

      # #Adding earnings to town lords' wealths.
      # (try_for_range, ":center_no", centers_begin, centers_end),
        # (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
        # (neq, ":town_lord", "trp_player"),
        # (is_between, ":town_lord", kingdom_heroes_begin, kingdom_heroes_end),
        # (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
        # (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
        # (troop_get_slot, ":troop_wealth", ":town_lord", slot_troop_wealth),
        # (val_add, ":troop_wealth", ":accumulated_rents"),
        # (val_add, ":troop_wealth", ":accumulated_tariffs"),
        # (troop_set_slot, ":town_lord", slot_troop_wealth, ":troop_wealth"),
        # (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
        # (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),
        # (try_begin),
          # (eq, "$cheat_mode", 1),
          # (assign, reg1, ":troop_wealth"),
          # (add_troop_note_from_sreg, ":town_lord", 1, "@Current wealth: {reg1}", 0),
        # (try_end),
      # (try_end),
    # ]),


  # Reset kingdom lady current centers
##   (28,
##   [  (try_for_range, ":troop_no", heroes_begin, heroes_end),
##         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
##
##         # Find the active quest ladies
##         (assign, ":not_ok", 0),
##         (try_for_range, ":quest_no", lord_quests_begin, lord_quests_end),
##           (eq, ":not_ok", 0),
##           (check_quest_active, ":quest_no"),
##           (quest_slot_eq, ":quest_no", slot_quest_object_troop, ":troop_no"),
##           (assign, ":not_ok", 1),
##         (try_end),
##         (eq, ":not_ok", 0),
##
##         (troop_get_slot, ":troop_center", ":troop_no", slot_troop_cur_center),
##         (assign, ":is_under_siege", 0),
##         (try_begin),
##           (is_between, ":troop_center", walled_centers_begin, walled_centers_end),
##           (party_get_battle_opponent, ":besieger_party", ":troop_center"),
##           (gt, ":besieger_party", 0),
##           (assign, ":is_under_siege", 1),
##         (try_end),
##
##         (eq, ":is_under_siege", 0),# Omit ladies in centers under siege
##
##         (try_begin),
##           (store_random_in_range, ":random_num",0, 100),
##           (lt, ":random_num", 20),
##           (store_troop_faction, ":cur_faction", ":troop_no"),
##           (call_script, "script_cf_select_random_town_with_faction", ":cur_faction"),#Can fail
##           (troop_set_slot, ":troop_no", slot_troop_cur_center, reg0),
##         (try_end),
##       
##         (store_random_in_range, ":random_num",0, 100),
##         (lt, ":random_num", 50),
##         (troop_get_slot, ":lord_no", ":troop_no", slot_troop_father),
##         (try_begin),
##           (eq, ":lord_no", 0),
##           (troop_get_slot, ":lord_no", ":troop_no", slot_troop_spouse),
##         (try_end),
##         (gt, ":lord_no", 0),
##         (troop_get_slot, ":cur_party", ":lord_no", slot_troop_leaded_party),
##         (gt, ":cur_party", 0),
##         (party_get_attached_to, ":cur_center", ":cur_party"),
##         (gt, ":cur_center", 0),
##
##         (troop_set_slot, ":troop_no", slot_troop_cur_center, ":cur_center"),
##       (try_end),
##    ]),


  # Attach Lord Parties to the town they are in
  (0.1,
   [  (try_for_range, ":troop_no", heroes_begin, heroes_end),
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (troop_get_slot, ":troop_party_no", ":troop_no", slot_troop_leaded_party),
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
    ]),

  # Check escape chances of hero prisoners.
  (48,
   [   (call_script, "script_randomly_make_prisoner_heroes_escape_from_party", "p_main_party", 50),
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##         (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
         (party_is_active, ":center_no"), #TLD
         (assign, ":chance", 30),
         (try_begin),
           (party_slot_eq, ":center_no", slot_center_has_prisoner_tower, 1),
           (assign, ":chance", 5),
         (try_end),
         (call_script, "script_randomly_make_prisoner_heroes_escape_from_party", ":center_no", ":chance"),
       (try_end),
    ]),

# TLD - removed
  # # Asking the ownership of captured centers to the player
  # (3,
   # [(assign, "$g_center_taken_by_player_faction", -1),
    # (try_for_range, ":center_no", centers_begin, centers_end),
      # (eq, "$g_center_taken_by_player_faction", -1),
      # (store_faction_of_party, ":center_faction", ":center_no"),
      # (eq, ":center_faction", "fac_player_supporters_faction"),
      # (this_or_next|party_slot_eq, ":center_no", slot_town_lord, stl_reserved_for_player),
      # (this_or_next|party_slot_eq, ":center_no", slot_town_lord, stl_unassigned),
      # (party_slot_eq, ":center_no", slot_town_lord, stl_rejected_by_player),
      # (assign, "$g_center_taken_by_player_faction", ":center_no"),
    # (try_end),
    # (ge, "$g_center_taken_by_player_faction", 0),
    # (faction_get_slot, ":leader", "fac_player_supporters_faction", slot_faction_leader),
    # (start_map_conversation, ":leader"),
   # ]),


  # Respawn hero party after kingdom hero is released from captivity.
  (24,  # changed from 48 to 24 in TLD, GA
   [  (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
         (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
         (neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1),

         (store_troop_faction, ":cur_faction", ":troop_no"),
         (try_begin),
           (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active), #MV, defensive
           (call_script, "script_cf_select_random_walled_center_with_faction_and_owner_priority_no_siege", ":cur_faction", ":troop_no"),#Can fail
           (assign, ":center_no", reg0),
           (call_script, "script_create_kingdom_hero_party", ":troop_no", ":center_no"),
           (party_attach_to_party, "$pout_party", ":center_no"),
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

  # Spawn merchant caravan parties
##  (3,
##   [   (try_for_range, ":troop_no", merchants_begin, merchants_end),
##         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_merchant),
##         (troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
##         (neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1),
##
##         (call_script, "script_cf_create_merchant_party", ":troop_no"),
##       (try_end),
##    ]),

  # Spawn village farmer parties
  #(24,
  # [   (try_for_range, ":village_no", villages_begin, villages_end),
  #       (party_slot_eq, ":village_no", slot_village_state, svs_normal),
  #       (party_get_slot, ":farmer_party", ":village_no", slot_village_farmer_party),
  #       (this_or_next|eq, ":farmer_party", 0),
  #       (neg|party_is_active, ":farmer_party"),
  #       (store_random_in_range, ":random_no", 0, 100),
  #       (lt, ":random_no", 30),
  #       (call_script, "script_create_village_farmer_party", ":village_no"),
  #       (party_set_slot, ":village_no", slot_village_farmer_party, reg0),
#         (str_store_party_name, s1, ":village_no"),
#         (display_message, "@Village farmers created at {s1}."),
  #     (try_end),
  #  ]),

  
   (72,[
 # Updating trade good prices according to the productions
       (call_script, "script_update_trade_good_prices"),
 # Updating player odds
       # (try_for_range, ":cur_center", centers_begin, centers_end),
         # (party_get_slot, ":player_odds", ":cur_center", slot_town_player_odds),
         # (try_begin),
           # (gt, ":player_odds", 1000),
           # (val_mul, ":player_odds", 95),
           # (val_div, ":player_odds", 100),
           # (val_max, ":player_odds", 1000),
         # (else_try),
           # (lt, ":player_odds", 1000),
           # (val_mul, ":player_odds", 105),
           # (val_div, ":player_odds", 100),
           # (val_min, ":player_odds", 1000),
         # (try_end),
         # (party_set_slot, ":cur_center", slot_town_player_odds, ":player_odds"),
       # (try_end),
    ]),


  #Troop AI: Merchants thinking
  (8,[(try_for_parties, ":party_no"),
         (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
         (assign, reg0, ":party_no"),
#         (display_message, "@DEBUG: Caravan {reg0}", 0xff00fd33),
         (party_is_in_any_town, ":party_no"),
#         (display_message, "@DEBUG: Point 1", 0xff00fd33),
         (store_faction_of_party, ":merchant_faction", ":party_no"),
         (faction_get_slot, ":num_towns", ":merchant_faction", slot_faction_num_towns),
         (try_begin),
           (le, ":num_towns", 0),
           (remove_party, ":party_no"),
#           (display_message, "@DEBUG: removed", 0xff00fd33),
         (else_try),
           (store_random_in_range, ":random_no", 0, 100),
           (lt, ":random_no", 35),
       
#           (display_message, "@DEBUG: random", 0xff00fd33),
           (party_get_cur_town, ":cur_center", ":party_no"),

           (assign, ":can_leave", 1),
           (try_begin),
             (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
             (neg|party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
             (assign, ":can_leave", 0),
           (try_end),
           (eq, ":can_leave", 1),

#           (display_message, "@DEBUG: can leave", 0xff00fd33),
           (assign, ":do_trade", 0),
           (try_begin),
             (party_get_slot, ":cur_ai_state", ":party_no", slot_party_ai_state),
             (eq, ":cur_ai_state", spai_trading_with_town),
             (party_get_slot, ":cur_ai_object", ":party_no", slot_party_ai_object),
             (eq, ":cur_center", ":cur_ai_object"),
             (assign, ":do_trade", 1),
           (try_end),

           (assign, ":target_center", -1),
           
           #(try_begin), #Make sure escorted caravan continues to its original destination.
           #  (eq, "$caravan_escort_party_id", ":party_no"),
           #  (neg|party_is_in_town, ":party_no", "$caravan_escort_destination_town"),
           #  (assign, ":target_center", "$caravan_escort_destination_town"),
           #(else_try),
             (call_script, "script_cf_select_random_town_at_peace_with_faction_in_trade_route", ":cur_center", ":merchant_faction"),
             (assign, ":target_center", reg0),
             (eq, ":target_center", -1),
             (remove_party, ":party_no"), #MV: no towns to travel to, remove
           #(try_end),
           (is_between, ":target_center", towns_begin, towns_end),
#           (display_message, "@DEBUG: target", 0xff00fd33),
           (neg|party_is_in_town, ":party_no", ":target_center"),
#            (display_message, "@DEBUG: set off", 0xff00fd33),
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

  #Troop AI: Village farmers thinking
  # village cutout, GA
  #(8,
  # [  (try_for_parties, ":party_no"),
  #       (party_slot_eq, ":party_no", slot_party_type, spt_village_farmer),
  #       (party_is_in_any_town, ":party_no"),
  #       (party_get_slot, ":home_center", ":party_no", slot_party_home_center),
  #       (party_get_cur_town, ":cur_center", ":party_no"),
#
#         (assign, ":can_leave", 1),
#         (try_begin),
#           (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
#           (neg|party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
#           (assign, ":can_leave", 0),
#         (try_end),
#         (eq, ":can_leave", 1),
#
#         (try_begin),
#           (eq, ":cur_center", ":home_center"),
#           (try_begin),
#             (store_random_in_range, ":random_no", 0, 100),
#             (lt, ":random_no", 5),
#             (call_script, "script_do_party_center_trade", ":party_no", ":home_center", 50),
#             (assign, ":total_change", reg0),
#             (party_get_slot, ":prosperity", ":home_center", slot_town_prosperity),
#             (val_add, ":prosperity", 30),
#             (val_mul, ":total_change", ":prosperity"),
#             (val_div, ":total_change", 2600), #(30 + prosperity) / 130 * 5% of the sales.
#
#             #Adding tax revenue to the center
#             (party_get_slot, ":accumulated_tariffs", ":home_center", slot_center_accumulated_tariffs),
#             (val_add, ":accumulated_tariffs", ":total_change"),
#             (party_set_slot, ":home_center", slot_center_accumulated_tariffs, ":accumulated_tariffs"),
#      
#             #Moving farmers to the home town
#             (party_get_slot, ":market_town", ":home_center", slot_village_market_town),
#             (party_set_slot, ":party_no", slot_party_ai_object, ":market_town"),
#             (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
#             (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
#             (party_set_ai_object, ":party_no", ":market_town"),
##             (try_begin),
##               (eq, "$cheat_mode", 1),
##               (str_store_party_name, s1, ":home_center"),
##               (assign, reg1, ":total_change"),
##               (display_message, "@Village farmers traded with {s1} merchants. Tax={reg1}"),
##             (try_end),
#           (try_end),
#         (else_try),
#           (try_begin),
#             (party_get_slot, ":cur_ai_object", ":party_no", slot_party_ai_object),
#             (eq, ":cur_center", ":cur_ai_object"),
#
#             (call_script, "script_do_party_center_trade", ":party_no", ":cur_ai_object", 10),
#             (assign, ":total_change", reg0),
#             (party_get_slot, ":prosperity", ":cur_ai_object", slot_town_prosperity),
#             (val_add, ":prosperity", 30),
#             (val_mul, ":total_change", ":prosperity"),
#             (val_div, ":total_change", 2600), #(30 + prosperity) / 130 * 5% of the sales.
#
#             #Adding tax revenue to the center
#             (party_get_slot, ":accumulated_tariffs", ":cur_ai_object", slot_center_accumulated_tariffs),
#             (val_add, ":accumulated_tariffs", ":total_change"),
#             (party_set_slot, ":cur_ai_object", slot_center_accumulated_tariffs, ":accumulated_tariffs"),
#             #Adding tax revenue to the home center
#             (party_get_slot, ":accumulated_tariffs", ":home_center", slot_center_accumulated_tariffs),
#             (val_add, ":accumulated_tariffs", ":total_change"),
#             (party_set_slot, ":home_center", slot_center_accumulated_tariffs, ":accumulated_tariffs"),
#
#             #Increasing food stocks of the town
#             (party_get_slot, ":town_food_store", ":cur_ai_object", slot_party_food_store),
#             (call_script, "script_center_get_food_store_limit", ":cur_ai_object"),
#             (assign, ":food_store_limit", reg0),
#             (val_add, ":town_food_store", 1000),
#             (val_min, ":town_food_store", ":food_store_limit"),
#             (party_set_slot, ":cur_ai_object", slot_party_food_store, ":town_food_store"),
#
#             #Adding 1 to village prosperity
#             (try_begin),
#               (store_random_in_range, ":rand", 0, 100),
#               (lt, ":rand", 35),
#               (call_script, "script_change_center_prosperity", ":home_center", 1),
#             (try_end),
#           (try_end),
#
#           #Moving farmers to their home village
#           (party_set_slot, ":party_no", slot_party_ai_object, ":home_center"),
#           (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
#           (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
#           (party_set_ai_object, ":party_no", ":home_center"),
##           (try_begin),
##             (eq, "$cheat_mode", 1),
##             (str_store_party_name, s1, ":cur_ai_object"),
##             (assign, reg1, ":total_change"),
##             (display_message, "@Village farmers traded with {s1} merchants. Tax={reg1} to both sides"),
##           (try_end),
#         (try_end),
#       (try_end),
#    ]),

 #Increase castle food stores
  (2,[(try_for_range, ":center_no", castles_begin, castles_end),
         (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #castle is not under siege
         (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
         (val_add, ":center_food_store", 100),
         (call_script, "script_center_get_food_store_limit", ":center_no"),
         (assign, ":food_store_limit", reg0),
         (val_min, ":center_food_store", ":food_store_limit"),
         (party_set_slot, ":center_no", slot_party_food_store, ":center_food_store"),
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
##  (6,[ (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
##         (call_script, "script_party_calculate_strength", ":cur_center", 0), #will update slot_party_cached_strength
##       (try_end),
##     ]),

##  (1,
##   [   (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
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

  # Make heroes running away from someone retreat to friendly centers
  (0.5,
   [  (try_for_range, ":cur_troop", heroes_begin, heroes_end),
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
             (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
               (party_is_active, ":cur_center"), #TLD
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

  # Centers give alarm if the player is around
  (0.5,
   [ (store_current_hours, ":cur_hours"),
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
    ]),
  
  (5, # consuming orc brew if wounded every 5 hors -- mtarini
  [
	#(eq, "$orc_brew_activated", 1),
	(call_script,"script_party_count_wounded", "p_main_party"),(assign, ":n_drinks",reg0),
	#(display_message, "@DEBUG: {reg0} drinks of orc brew"),
	(gt, ":n_drinks",0),
	#(store_random_in_range, reg10, 0, 10),(val_add, ":n_drinks",10),(val_div, ":n_drinks",10), # div 10, roudning at random
	(call_script,"script_consume_orc_brew",":n_drinks"),
  ]),
  
  # Consuming food at every 14 hours
  (14,
   [(eq, "$g_player_is_captive", 0),
    (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
    (assign, ":num_men", 0),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
      (val_add, ":num_men", ":stack_size"),
    (try_end),
    (val_div, ":num_men", 3),
    (try_begin),
      (eq, ":num_men", 0),
      (val_add, ":num_men", 1),
    (try_end),
    
    (assign, ":consumption_amount", ":num_men"),
    (assign, ":no_food_displayed", 0),
    (try_for_range, ":unused", 0, ":consumption_amount"),
      (assign, ":available_food", 0),
      (try_for_range, ":cur_food", food_begin, food_end),
        (item_set_slot, ":cur_food", slot_item_is_checked, 0),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_food", imod_rotten),
        (val_add, ":available_food", 1),
      (try_end),
      (try_begin),
        (gt, ":available_food", 0),
        (store_random_in_range, ":selected_food", 0, ":available_food"),
        (call_script, "script_consume_food", ":selected_food"),
      (else_try),
        (eq, ":no_food_displayed", 0),
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
    ]),

  # Setting item modifiers for food
  (24,[
     (troop_get_inventory_capacity, ":inv_size", "trp_player"),
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

  # # Assigning lords to centers with no leaders
  # (72,[(call_script, "script_assign_lords_to_empty_centers"),
      # ]),
  
  # Updating player icon in every frame
  (0,
   [(troop_get_inventory_slot, ":cur_horse", "trp_player", ek_horse), #horse slot
	
	# determine if archer or not
	(try_begin),
		(troop_get_inventory_slot, reg5, "trp_player", ek_item_0),(val_max, reg5, 0),(item_get_type, reg5,reg5),
		(assign, ":archer", 0),(neg|is_between, reg5, itp_type_one_handed_wpn, itp_type_one_handed_wpn+1), 
		(assign, ":archer", 1),(neg|is_between, reg5, itp_type_bow, itp_type_crossbow+1),
		(troop_get_inventory_slot, reg5, "trp_player", ek_item_1),(val_max, reg5, 0),(item_get_type, reg5,reg5),
		(assign, ":archer", 0),(neg|is_between, reg5, itp_type_one_handed_wpn, itp_type_one_handed_wpn+1), 
		(assign, ":archer", 1),(neg|is_between, reg5, itp_type_bow, itp_type_crossbow+1),
		(troop_get_inventory_slot, reg5, "trp_player", ek_item_2),(val_max, reg5, 0),(item_get_type, reg5,reg5),
		(assign, ":archer", 0),(neg|is_between, reg5, itp_type_one_handed_wpn, itp_type_one_handed_wpn+1), 
		(assign, ":archer", 1),(neg|is_between, reg5, itp_type_bow, itp_type_crossbow+1),
		(troop_get_inventory_slot, reg5, "trp_player", ek_item_3),(val_max, reg5, 0),(item_get_type, reg5,reg5),
		(assign, ":archer", 0),(neg|is_between, reg5, itp_type_one_handed_wpn, itp_type_one_handed_wpn+1), 
		(assign, ":archer", 1),(neg|is_between, reg5, itp_type_bow, itp_type_crossbow+1),
	(try_end),
    (assign, ":new_icon", -1),
	
    (try_begin),
      (eq, "$g_player_icon_state", pis_normal),
      (try_begin),
		# mounted
		(try_begin),
			(ge, ":cur_horse", 0), 
			(assign, ":new_icon", "$g_player_icon_mounted"),
		(else_try),
			(try_begin),
				(ge, ":archer", 1), 
				(assign, ":new_icon", "$g_player_icon_foot_archer"),
			(else_try),
				(assign, ":new_icon", "$g_player_icon_foot_melee"),
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
  
 #Update how good a target player is for bandits
  (2,[ (store_troop_gold, ":total_value", "trp_player"),
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

  # Checking escape chances of prisoners that joined the party recently.
(6,[(gt, "$g_prisoner_recruit_troop_id", 0),
    (gt, "$g_prisoner_recruit_size", 0),
    (gt, "$g_prisoner_recruit_last_time", 0),
    (is_currently_night),
    (try_begin),
      (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
      (val_mul, ":leadership", 5),
      (store_sub, ":chance", 66, ":leadership"),
      (gt, ":chance", 0),
      (assign, ":num_escaped", 0),
      (try_for_range, ":unused", 0, "$g_prisoner_recruit_size"),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":chance"),
        (val_add, ":num_escaped", 1),
      (try_end),
      (party_remove_members, "p_main_party", "$g_prisoner_recruit_troop_id", ":num_escaped"),
      (assign, ":num_escaped", reg0),
      (gt, ":num_escaped", 0),
      (try_begin),
        (gt, ":num_escaped", 1),
        (assign, reg2, 1),
      (else_try),
        (assign, reg2, 0),
      (try_end),
      (assign, reg1, ":num_escaped"),
      (str_store_troop_name_by_count, s1, "$g_prisoner_recruit_troop_id", ":num_escaped"),
      (display_log_message, "@{reg1} {s1} {reg2?have:has} escaped from your party during the night."),
    (try_end),
    (assign, "$g_prisoner_recruit_troop_id", 0),
    (assign, "$g_prisoner_recruit_size", 0),
    ]),

  # Offering ransom fees for player's prisoner heroes
# no such thing in TLD, might later be replaced with "deliver prisoner" quest, GA
#  (24,
#   [(neq, "$g_ransom_offer_rejected", 1),
#    (call_script, "script_offer_ransom_amount_to_player_for_prisoners_in_party", "p_main_party"),
#    (eq, reg0, 0),#no prisoners offered
#    (assign, ":end_cond", walled_centers_end),
#    (try_for_range, ":center_no", walled_centers_begin, ":end_cond"),
#      (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
#      (call_script, "script_offer_ransom_amount_to_player_for_prisoners_in_party", ":center_no"),
#      (eq, reg0, 1),#a prisoner is offered
#      (assign, ":end_cond", 0),#break
#    (try_end),
#    ]), 

  # Exchanging hero prisoners between factions and clearing old ransom offers
# no such thing in TLD, GA
#  (72,
#   [(assign, "$g_ransom_offer_rejected", 0),
#    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
#      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
#      (gt, ":town_lord", 0),
#      (party_get_num_prisoner_stacks, ":num_stacks", ":center_no"),
#      (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
#        (party_prisoner_stack_get_troop_id, ":stack_troop", ":center_no", ":i_stack"),
#        (troop_is_hero, ":stack_troop"),
#        (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
#        (store_random_in_range, ":random_no", 0, 100),
#        (try_begin),
#          (le, ":random_no", 10),
#          (call_script, "script_calculate_ransom_amount_for_troop", ":stack_troop"),
#          (assign, ":ransom_amount", reg0),
#          (troop_get_slot, ":wealth", ":town_lord", slot_troop_wealth),
#          (val_add, ":wealth", ":ransom_amount"),
#          (troop_set_slot, ":town_lord", slot_troop_wealth, ":wealth"),
#          (party_remove_prisoners, ":center_no", ":stack_troop", 1),
#          (call_script, "script_remove_troop_from_prison", ":stack_troop"),
#          (store_troop_faction, ":faction_no", ":town_lord"),
#          (store_troop_faction, ":troop_faction", ":stack_troop"),
#          (str_store_troop_name, s1, ":stack_troop"),
#          (str_store_faction_name, s2, ":faction_no"),
#          (str_store_faction_name, s3, ":troop_faction"),
#          (display_log_message, "@{s1} of {s3} has been released from captivity."),
#        (try_end),
#      (try_end),
#    (try_end),
#    ]),
  
  # Adding mercenary troops to the towns
  (72,
   [(call_script, "script_update_mercenary_units_of_towns"),
#NPC changes begin
# removes   (call_script, "script_update_companion_candidates_in_taverns"),
#NPC changes end
    (call_script, "script_update_ransom_brokers"),
    (call_script, "script_update_tavern_travelers"),
    (call_script, "script_update_tavern_minstels"),
# commented by GA, village removal
#    (call_script, "script_update_villages_infested_by_bandits"),
#    (try_for_range, ":village_no", villages_begin, villages_end),
#      (call_script, "script_update_volunteer_troops_in_village", ":village_no"),
#      (call_script, "script_update_npc_volunteer_troops_in_village", ":village_no"),
#    (try_end),
    ]),

  # Setting random walker types
  (36,
   [(try_for_range, ":center_no", centers_begin, centers_end),
      (party_is_active, ":center_no"), #TLD
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
  (12,
   [(try_for_range, ":center_no", centers_begin, centers_end),
      (party_is_active, ":center_no"), #TLD
      (party_get_slot, ":cur_improvement", ":center_no", slot_center_current_improvement),
      (gt, ":cur_improvement", 0),
      (party_get_slot, ":cur_improvement_end_time", ":center_no", slot_center_improvement_end_hour),
      (store_current_hours, ":cur_hours"),
      (ge, ":cur_hours", ":cur_improvement_end_time"),
      (party_set_slot, ":center_no", ":cur_improvement", 1),
      (party_set_slot, ":center_no", slot_center_current_improvement, 0),
      (call_script, "script_get_improvement_details", ":cur_improvement"),
      (try_begin),
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (str_store_party_name, s4, ":center_no"),
        (display_log_message, "@Building of {s0} in {s4} has been completed."),
      (try_end),
# commented by GA, village removal
#      (try_begin),
#        (is_between, ":center_no", villages_begin, villages_end),
#        (eq, ":cur_improvement", slot_center_has_fish_pond),
#        (call_script, "script_change_center_prosperity", ":center_no", 5),
#      (try_end),
    (try_end),
    ]),


# Asking to give center to player
# commented by GA, no ownership of centers 
#  (8,[
#    (assign, ":done", 0),
#    (try_for_range, ":center_no", centers_begin, centers_end),
#      (eq, ":done", 0),
#      (party_slot_eq, ":center_no", slot_town_lord, stl_reserved_for_player),
#      (assign, "$g_center_to_give_to_player", ":center_no"),
#      (try_begin),
#        (eq, "$g_center_to_give_to_player", "$g_castle_requested_by_player"),
#        (assign, "$g_castle_requested_by_player", 0),
#        (jump_to_menu, "mnu_requested_castle_granted_to_player"),
#      (else_try),
#        (jump_to_menu, "mnu_give_center_to_player"),
#      (try_end),
#      (assign, ":done", 1),
#    (else_try),
#      (eq, ":center_no", "$g_castle_requested_by_player"),
#      (party_slot_ge, ":center_no", slot_town_lord, kingdom_heroes_begin),
#      (assign, "$g_castle_requested_by_player", 0),
#      (store_faction_of_party, ":faction", ":center_no"),
#      (eq, ":faction", "$players_kingdom"),
#      (assign, "$g_center_to_give_to_player", ":center_no"),
#      (jump_to_menu, "mnu_requested_castle_granted_to_another"),
#      (assign, ":done", 1),
#    (try_end),
#    ]),
  
  # Taking denars from player while resting in not owned centers
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

#  (6,[(call_script, "script_tld_war_system"),
#     ]),

  #Spawn some bandits.
  (36,[(call_script, "script_spawn_bandits"),
      ]),

  # Make parties larger as game progresses.
  (24,[(call_script, "script_update_party_creation_random_limits"),
      ]),
  
  # Reduce renown slightly by 0.5% every week
  (7 * 24,[(troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
           (store_div, ":renown_decrease", ":player_renown", 200),
           (val_sub, ":player_renown", ":renown_decrease"),
           (troop_set_slot, "trp_player", slot_troop_renown, ":player_renown"),
          ]),

# Removing cattle herds if they are way out of range
  (12, [(try_for_parties, ":cur_party"),
          (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
          (store_distance_to_party_from_party, ":dist",":cur_party", "p_main_party"),
          (try_begin),
            (gt, ":dist", 30),
            (remove_party, ":cur_party"),
            (try_begin),
              #Fail quest if the party is the quest party
              (check_quest_active, "qst_move_cattle_herd"),
              (neg|check_quest_concluded, "qst_move_cattle_herd"),
              (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
              (call_script, "script_fail_quest", "qst_move_cattle_herd"),
            (end_try),
          (else_try),
            (gt, ":dist", 10),
            (party_set_slot, ":cur_party", slot_cattle_driven_by_player, 0),
            (party_set_ai_behavior, ":cur_party", ai_bhvr_hold),
          (try_end),
        (try_end),
    ]),
    
# Quest triggers:

# capture troll quest (mtarini)
# if the quest is active, add a wild troll party every now and then, up to two.
(10, [(check_quest_active, "qst_capture_troll"),
     (assign,":count",0), # count active wild troll parties (*45)
	 (try_for_parties,":i"),(party_is_active, ":i"),(party_get_template_id, ":j", ":i"),(eq,":j","pt_wild_troll"),(val_add,":count",45),(try_end),
	 (store_random_in_range,":die_roll",0,100),(ge,":die_roll",":count"), # if (die_roll(100)>numtrolls*45)
	 (set_spawn_radius,1),
	 (spawn_around_party,"p_town_troll_cave","pt_wild_troll"),
	]),

# kill troll quest: if troll dies on its own, cancel quest (mtarini)
(5, [
  (check_quest_active, "qst_kill_troll"),
  (quest_get_slot, ":quest_target_party", "qst_kill_troll", slot_quest_target_party),
  (neg|party_is_active, ":quest_target_party"),
  (quest_get_slot, ":quest_object_center", "qst_kill_troll", slot_quest_object_center),
  (str_store_party_name,2,":quest_object_center"),
  (display_message, "@Troll outside {s2} was killed. Mission canceled."),
  (cancel_quest, "qst_kill_troll"),
]),
	
 
# Remaining days text update
  (24, [(try_for_range, ":cur_quest", all_quests_begin, all_quests_end),
          (try_begin),
            (check_quest_active, ":cur_quest"),
            (try_begin),
              (neg|check_quest_concluded, ":cur_quest"),
              (quest_slot_ge, ":cur_quest", slot_quest_expiration_days, 1),
              (quest_get_slot, ":exp_days", ":cur_quest", slot_quest_expiration_days),
              (val_sub, ":exp_days", 1),
              (try_begin),
                (eq, ":exp_days", 0),
                (call_script, "script_abort_quest", ":cur_quest", 1),
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

# Report to army quest
  (12, #MV: make it more rare?, was 6
   [
     (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
     (eq, "$g_player_is_captive", 0),
     (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
     (neg|check_quest_active, "qst_report_to_army"),
     (neg|check_quest_active, "qst_follow_army"),
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


# Army quest initializer
  (3,
   [ (assign, "$g_random_army_quest", -1),
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
               (is_between, ":ai_object", walled_centers_begin, walled_centers_end),
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

# Move cattle herd
  (0.5, [(check_quest_active,"qst_move_cattle_herd"),
         (neg|check_quest_concluded,"qst_move_cattle_herd"),
         (quest_get_slot, ":target_party", "qst_move_cattle_herd", slot_quest_target_party),
         (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
         (store_distance_to_party_from_party, ":dist",":target_party", ":target_center"),
         (lt, ":dist", 3),
         (remove_party, ":target_party"),
         (call_script, "script_succeed_quest", "qst_move_cattle_herd"),
    ]),

  (2, [
       (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
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

# Scout waypoints
  (1,[
       (try_begin),
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
  

#NPC changes begin
#Resolve one issue each hour
(1,[
        (assign, "$npc_map_talk_context", 0),
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
            (try_for_range, ":npc", companions_begin, companions_end),
                (eq, "$npc_map_talk_context", 0),
                (main_party_has_troop, ":npc"),           
                (troop_slot_eq, ":npc", slot_troop_home_speech_delivered, 0),
#                (eq, "$npc_map_talk_context", 0),
                (troop_get_slot, ":home", ":npc", slot_troop_home),
                (gt, ":home", 0),
                (store_distance_to_party_from_party, ":distance", ":home", "p_main_party"),
                (lt, ":distance", 7),                
                (assign, "$npc_map_talk_context", slot_troop_home),
                (start_map_conversation, ":npc"),
            (try_end),
            (neq, "$npc_map_talk_context", 0), #fail if nothing happened here
        (else_try), ###TLD: complain about NPC's home faction getting demolished
            (try_for_range, ":npc", companions_begin, companions_end),
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

(4, 
   [(try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
      (troop_slot_ge, ":troop_no", slot_troop_change_to_faction, 1),
      (store_troop_faction, ":faction_no", ":troop_no"),
      (troop_get_slot, ":new_faction_no", ":troop_no", slot_troop_change_to_faction),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (assign, ":continue", 0),
      (try_begin),
        (le, ":party_no", 0),
        #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (assign, ":continue", 1),
      (else_try),
        (gt, ":party_no", 0),
        (party_is_active, ":party_no"), #MV fix

        #checking if the party is outside the centers
        (party_get_attached_to, ":cur_center_no", ":party_no"),
        (try_begin),
          (lt, ":cur_center_no", 0),
          (party_get_cur_town, ":cur_center_no", ":party_no"),
        (try_end),
        (this_or_next|neg|is_between, ":cur_center_no", centers_begin, centers_end),
        (party_slot_eq, ":cur_center_no", slot_town_lord, ":troop_no"),
    
        #checking if the party is away from his original faction parties
        (assign, ":end_cond", kingdom_heroes_end),
        (try_for_range, ":enemy_troop_no", kingdom_heroes_begin, ":end_cond"),
          (troop_get_slot, ":enemy_party_no", ":enemy_troop_no", slot_troop_leaded_party),
          (gt, ":enemy_party_no", 0),
          (store_faction_of_party, ":enemy_faction_no", ":enemy_party_no"),
          (eq, ":enemy_faction_no", ":faction_no"),
          (store_distance_to_party_from_party, ":dist", ":party_no", ":enemy_party_no"),
          (lt, ":dist", 4),
          (assign, ":end_cond", 0),
        (try_end),
        (neq, ":end_cond", 0),
        (assign, ":continue", 1),
      (try_end),
      (eq, ":continue", 1),
      (call_script, "script_change_troop_faction", ":troop_no", ":new_faction_no"),
      (troop_set_slot, ":troop_no", slot_troop_change_to_faction, 0),
      (try_begin),
        (is_between, ":new_faction_no", kingdoms_begin, kingdoms_end),
        (str_store_troop_name_link, s1, ":troop_no"),
        (str_store_faction_name_link, s2, ":faction_no"),
        (str_store_faction_name_link, s3, ":new_faction_no"),
        (display_message, "@{s1} has switched from {s2} to {s3}."),
        (try_begin),
          (eq, ":faction_no", "$players_kingdom"),
          (call_script, "script_add_notification_menu", "mnu_notification_troop_left_players_faction", ":troop_no", ":new_faction_no"),
        (else_try),
          (eq, ":new_faction_no", "$players_kingdom"),
          (call_script, "script_add_notification_menu", "mnu_notification_troop_joined_players_faction", ":troop_no", ":faction_no"),
        (try_end),
      (try_end),
    (try_end),
    ]),


    #####################################
    # TLD triggers begin (by foxyman)
    #

    # Calculate day/night penalties
    (1, [
        (this_or_next|is_currently_night),
        (eq, "$prev_day", 0),
        (this_or_next|neg|is_currently_night),
        (eq, "$prev_day", 1),
        #debug_point_0,
        (try_begin),
            (neg|is_currently_night),
            (assign, "$prev_day", 1),
            (try_for_range, ":troop_id", tld_troops_begin, tld_troops_end),
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
            (try_for_range, ":troop_id", tld_troops_begin, tld_troops_end),
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
        ]
    ),

    #
    # TLD triggers end
    #####################################


	
## question box (yes/no) on global map
(ti_question_answered, 
   [(store_trigger_param_1,":answer"),
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
#    (else_try),
#      	(party_get_position, pos1, "p_main_party"),
#		(map_get_water_position_around_position,pos0,pos1,0.5),
#        (party_set_position, "p_main_party", pos0),
#		(party_relocate_near_party,"p_main_party","p_main_party",10),
#		(party_set_ai_object,"p_main_party", "p_town_minas_tirith"),
    (try_end),
   ]),


    #########################################
    # TLD War system 
    #

  # Check if a faction is defeated every 12 hours
  # TLD modified to check for faction strength instead, GA
  (12,[
    (assign, ":num_active_factions", 0),
#    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
#      (faction_set_slot, ":cur_kingdom", slot_faction_number_of_parties, 0),
#    (try_end),
#    (try_for_parties, ":cur_party"),
#      (store_faction_of_party, ":party_faction", ":cur_party"),
#      (is_between, ":party_faction", kingdoms_begin, kingdoms_end),
#      (this_or_next|is_between, ":cur_party", centers_begin, centers_end),
#      (party_slot_eq, ":cur_party", slot_party_type, spt_kingdom_hero_party),
#      (faction_get_slot, ":kingdom_num_parties", ":party_faction", slot_faction_number_of_parties),
#      (val_add, ":kingdom_num_parties", 1),
#      (faction_set_slot, ":party_faction", slot_faction_number_of_parties, ":kingdom_num_parties"),
#    (try_end),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
#      (try_begin),
#        (eq, "$cheat_mode", 1),
#        (str_store_faction_name, s1, ":cur_kingdom"),
#        (faction_get_slot, reg1, ":cur_kingdom", slot_faction_number_of_parties),
#        (display_message, "@DEBUG:Number of parties belonging to {s1}: {reg1}"),
#      (try_end),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (val_add, ":num_active_factions", 1),
#      (this_or_next|faction_slot_eq, ":cur_kingdom", slot_faction_number_of_parties, 0),

      #MV for TLD: faction defeat if capital captured
      (faction_get_slot, ":capital", ":cur_kingdom", slot_faction_capital),
      (store_faction_of_party, ":capital_faction", ":capital"),
	  (this_or_next|neq, ":cur_kingdom", ":capital_faction"),
	  (neg|faction_slot_ge, ":cur_kingdom", slot_faction_strength, 1), # TLD faction strength check, GA
      
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
            (remove_party, ":cur_party"),
          (else_try),
            # Centers: destroy what you can, give the rest to the best enemy
            (try_begin), #TLD: if center destroyable, disable it, otherwise proceed as normal
              (party_slot_eq, ":cur_party", slot_center_destroy_on_capture, 1),
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

        # check if all good factions are defeated, to start the eye-hand war
        (try_begin),
          (faction_slot_eq, ":cur_kingdom", slot_faction_side, faction_side_good),
          (assign, ":good_factions_left", 0),
          (try_for_range, ":good_kingdom", kingdoms_begin, kingdoms_end),
            (faction_slot_eq, ":good_kingdom", slot_faction_side, faction_side_good),
            (faction_slot_eq, ":good_kingdom", slot_faction_state, sfs_active),
            (val_add, ":good_factions_left", 1),
          (try_end),
          # Start the war between Mordor and Isengard
          # Is this automatic defeat for good players?
          (try_begin),
            (eq, ":good_factions_left", 0),
            # uncomment this if you script that Mordor and Isengard can't be defeated before their allies
            #(faction_slot_eq, "fac_mordor", slot_faction_state, sfs_active),
            #(faction_slot_eq, "fac_isengard", slot_faction_state, sfs_active),
            
            # make sides hostile
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
                (call_script, "script_destroy_center", ":adv_camp"),
              (try_end),
            (try_end),
            
		    (assign, "$tld_war_began", 2),
		    (dialog_box,"@The Age of Men has finally passed. Now the Two Towers gather their remaining hosts and allies to decide who will be the sole ruler of Middle Earth!","@The War of the Two Towers has started!"),
            (play_sound,"snd_evil_horn"),
          (try_end),
        (try_end),
	    
	    (str_store_faction_name,s2,":cur_kingdom"),
	    (display_log_message,"@{s2} was defeated!"),
        # now update active theaters for all factions
        (call_script, "script_update_active_theaters"),
        # rethink strategies
        (assign, "$g_recalculate_ais", 1),

        (assign, ":faction_removed", 1),
        (try_begin),
          (eq, "$players_oath_renounced_against_kingdom", ":cur_kingdom"),
          (assign, "$players_oath_renounced_against_kingdom", 0),
          (call_script, "script_add_notification_menu", "mnu_notification_oath_renounced_faction_defeated", ":cur_kingdom", 0),
        (try_end),
   #This menu must be at the end because faction banner will change after this menu if the player's supported pretender's original faction is cur_kingdom - but not in TLD!
        (call_script, "script_add_notification_menu", "mnu_notification_faction_defeated", ":cur_kingdom", 0),
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
            (call_script, "script_add_notification_menu", "mnu_notification_join_another_faction", ":player_side", 0),
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


   
 # TLD Messages about faction strength changes
(5,[(try_for_range,":faction",kingdoms_begin,kingdoms_end),
       (faction_get_slot,":strength",":faction",slot_faction_strength),
       (faction_get_slot,":strength_new",":faction",slot_faction_strength_tmp),
       (faction_set_slot,":faction",slot_faction_strength,":strength_new"),
#       (val_add,":strength",999),
#       (val_add,":strength_new",999),
       (val_div,":strength",1000),
       (val_div,":strength_new",1000),
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
       (call_script, "script_faction_strength_string", ":faction"),
       (try_begin),
          (lt,":strength",":strength_new"),   # announce when strength threshold is crossed upwards
          (display_message,"@The forces of {s22} have rallied! {s22} is now {s23}.", ":news_color"),
       (else_try),
          (display_message,"@The might of {s22} has diminished! {s22} is now {s23}.", ":news_color"), # announce when strength threshold is crossed downwards
       (try_end),
     (try_end),
    ]),

    # TLD deal with prisoner trains reached destination
    (8, [
        (try_for_parties, ":party_no"),
            (party_is_active, ":party_no"),
            (party_slot_eq, ":party_no", slot_party_type, spt_prisoner_train),
            (party_is_in_any_town, ":party_no"),
            (party_get_cur_town, ":cur_center", ":party_no"),
            (assign, "$g_move_heroes", 1),
            (party_detach, ":party_no"),
#            (party_get_position, pos1, ":party_no"),
#            (position_get_x, reg1, pos1),
#            (position_get_y, reg2, pos1),
#            (display_message, "@DEBUG: party at: {reg1}, {reg2} removed", debug_color),
#            (party_get_position, pos1, "p_main_party"),
#            (position_get_x, reg1, pos1),
#            (position_get_y, reg2, pos1),
#            (display_message, "@DEBUG: player at: {reg1}, {reg2}", debug_color),
            (call_script, "script_party_prisoners_add_party_prisoners", ":cur_center", ":party_no"),
            (remove_party, ":party_no"),
        (try_end),
    ]
    ),

    # TLD: establish advance camps in active, non-home theaters 
    (6, [
      (store_current_hours, ":cur_hours"),
      (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction", slot_faction_state, sfs_active),
        (faction_get_slot, ":active_theater", ":faction", slot_faction_active_theater),
        (neg|faction_slot_eq, ":faction", slot_faction_home_theater, ":active_theater"), #not in home theater
        (faction_get_slot, ":adv_camp", ":faction", slot_faction_advance_camp),
        (neg|party_is_active, ":adv_camp"), #not already established
        
        (faction_get_slot, ":camp_requested_hours", ":faction", slot_faction_advcamp_timer),
        (val_add, ":camp_requested_hours", 3*24), # 3 days after faction changes theater or previous camp destroyed
        (ge, ":cur_hours", ":camp_requested_hours"),
        
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 30), # 30% chance every 6 hours
        
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
        (display_log_message, "@The forces of {s2} established an advanced camp in {s15}!", ":news_color"),
        (call_script, "script_update_center_notes", ":adv_camp"),
          
        # fill the garrison if needed
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
    ]
    ),

    # TLD: update player attributes for rings and such
    (1, [(call_script, "script_apply_attribute_bonuses")]),
    
    # # TLD Add some cheats for ease of testing
    # (0, [
        # (eq, cheat_switch, 1),
        # (key_clicked, key_z),
        # (key_is_down, key_left_control),
        # (add_xp_to_troop, 500, "trp_player"),
        # (troop_get_slot, ":stat", "trp_player", slot_troop_faction_status),
        # (val_add, ":stat", 1000),
        # (troop_set_slot, "trp_player", slot_troop_faction_status, ":stat"),
        # (display_message, "@DEBUG: Faction status raised by 1000", debug_color),
    # ]
    # ),
    
    #
    # TLD War system end
    ###################################

     ######################################
     # TLD faction ranks
     #
    # pay wage
    # (24*7, [
        # (troop_get_slot,":faction_rank","trp_player",slot_troop_faction_rank),
        # (store_and, ":pos", ":faction_rank", stfr_position_mask),
        # (val_div, ":pos", stfr_position_unit),
        # (store_and, ":rank", ":faction_rank", stfr_rank_mask),
        # (val_div, ":rank", stfr_rank_unit),
        # (val_or, ":faction_rank", stfr_soldiers_permit),
        # (val_or, ":faction_rank", stfr_supplies_permit),
        # (troop_set_slot, "trp_player", slot_troop_faction_rank, ":faction_rank"),
        # (try_begin),
        # ]+concatenate_scripts([
            # [
            # (store_add, ":kd", kd, kingdoms_begin),
            # (eq, ":kd", "$players_kingdom"),
            # (try_begin),
            # ]+concatenate_scripts([
                # [
                # (eq, ":rank", rnk),
                # (display_message, "@You received weekly wage."),
                # (troop_add_gold, "trp_player", tld_faction_ranks[kd][rnk][1]),
            # (else_try),
                # ] for rnk in range(len(tld_faction_ranks[kd]))
            # ])+[
            # (try_end),        
        # (else_try),
            # ] for kd in range(len(tld_faction_ranks))
        # ])+[
        # (try_end),
    
        # ]
    # ), 
    
    # refresh reinforcement
    #(12, [ 
    #        (troop_
    #        (try_begin),
    #        ]+concantenate_scripts([
    #            [
    #            (eq, kd+fac_kingdom_1, "$players_kingdom"),
    #            (try_begin),
    #            ]+concantenate_scripts([
    #                [
    #                (eq, ":rank", rnk),
    #                (try_begin),
    #                ]+concantenate_scripts([
    #                    [
    #                    (eq, ":pos", pos),
    #                    (try_begin),
    #                        (ge, 
    #                    (try_end),
    #                (else_try),
    #                    ] for pos in range(len(tld_faction_ranks[kd][rnk][2]))
    #                ])+[
    #                (try_end),
    #            (else_try),
    #                ] for rnk in range(len(tld_faction_ranks[kd]))
    #            ])+[
    #            (try_end),        
    #        (else_try),
    #            ] for kd in range(len(tld_faction_ranks))
    #        ])+[
    #        (try_end),
    #    ]
    #), 
    #
    # TLD faction ranks end
    ###################################

##############################################
#trigger reserved for future save game compartibility
(999,[]),   
#trigger reserved for future save game compartibility
(999,[]),   
#trigger reserved for future save game compartibility
(999,[]),   
#trigger reserved for future save game compartibility
(999,[]),   
#trigger reserved for future save game compartibility
(999,[]),   
#trigger reserved for future save game compartibility
(999,[]),   
#trigger reserved for future save game compartibility
(999,[]),   
#trigger reserved for future save game compartibility
(999,[]),   

]

