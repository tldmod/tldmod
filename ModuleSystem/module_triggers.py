from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *

from module_constants import *

####################################################################################################################
#  Each trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Delay interval: Time to wait before applying the consequences of the trigger
#    After its conditions have been evaluated as true.
# 3) Re-arm interval. How much time must pass after applying the consequences of the trigger for the trigger to become active again.
#    You can put the constant ti_once here to make sure that the trigger never becomes active again after it fires once.
# 4) Conditions block (list). This must be a valid operation block. See header_operations.py for reference.
#    Every time the trigger is checked, the conditions block will be executed.
#    If the conditions block returns true, the consequences block will be executed.
#    If the conditions block is empty, it is assumed that it always evaluates to true.
# 5) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
####################################################################################################################

# Some constants for use below
#MV: removed - use those in module_constants.py
#merchant_inventory_space = 30
#num_merchandise_goods = 36

triggers = [
# Tutorial:
#  (0.1, 0, ti_once, [(map_free,0)], [(dialog_box,"str_tutorial_map1")]),
#  (1, 0, 0.0, [(key_is_down,key_h)],[(call_script,"script_tld_war_system_debug")] ),  
#  (1, 0, 0.0, [(key_is_down,key_r)],[(call_script,"script_tld_war_system_init")] ),
#  (1, 0, ti_once, [(map_free,0)], [(start_map_conversation,"trp_guide")]),

( 0, 0.5, ti_once, [], [
 (set_show_messages, 1), # all initial menu is done without messages. Putthem back only here!
 #(display_message, "@New game started!"),
]),

# Refresh Smiths
(0, 0, 24, [], [
	(try_for_range,":cur_merchant",weapon_merchants_begin,weapon_merchants_end),
		(reset_item_probabilities,100),     
		(troop_clear_inventory,":cur_merchant"),
		(store_troop_faction,":faction",":cur_merchant" ),
		(faction_get_slot, ":faction_mask", ":faction", slot_faction_mask),
		(troop_get_slot,":subfaction",":cur_merchant", slot_troop_subfaction),
		(store_add,":last_item_plus_one","itm_ent_body",1),
		
		(try_begin), # bad guys have shitty quality shops
			(neg|faction_slot_eq, ":faction", slot_faction_side, faction_side_good),
			(set_merchandise_modifier_quality,50),
		(else_try),
			(set_merchandise_modifier_quality,100),
		(try_end),
		
		(try_for_range,":item","itm_no_item",":last_item_plus_one"), # items with faction != merchant get 0 probability
			(item_get_slot,":item_faction_mask",":item",slot_item_faction),
			(val_and,":item_faction_mask",":faction_mask"),
			(try_begin),
				(eq,":item_faction_mask",0), # faction mismatch
				(set_item_probability_in_merchandise,":item",0),
			(else_try),
				(gt, ":subfaction", 0),
				(assign, ":subfaction_mask", 1),
				(try_for_range, ":unused", 0, ":subfaction"),(val_mul, ":subfaction_mask", 2),(try_end), # ":subfaction_mask"=1 if regular faction w/o subs, 2,4,8,16... for subs
				(item_get_slot,":item_subfaction_mask",":item",slot_item_subfaction),
				(store_and,reg1,":subfaction_mask",":item_subfaction_mask"), # subfaction mismatch
				(eq,reg1,0),
				(set_item_probability_in_merchandise, ":item", 0),  #  prob reduced to 1 %
			(else_try),
				(store_item_value,":value",":item"),
				(try_begin), # somewhat fewer expensive items in store
					(gt,":value",1500),
					(set_item_probability_in_merchandise,":item",50),
				(try_end),
			(try_end),
		(try_end),

		(try_for_range,":itp_type",itp_type_one_handed_wpn, itp_type_pistol),
			(troop_get_slot,":skill","trp_skill2item_type",":itp_type"), #abundance stored in merchant skills values
			(store_skill_level,":items",":skill",":cur_merchant"), 
			(try_begin),
				(gt,":items",0),(troop_add_merchandise,":cur_merchant",":itp_type",":items"),
			(try_end),
		(try_end),
		
		(troop_ensure_inventory_space,":cur_merchant",merchant_inventory_space),
		(troop_sort_inventory, ":cur_merchant"),
		(store_troop_gold, ":gold",":cur_merchant"),
		(lt, ":gold",900),
		(store_random_in_range,":new_gold",200,400),
		(call_script, "script_troop_add_gold",":cur_merchant",":new_gold"),
	(try_end),
]),

# Refresh Horse sellers
(0, 0, 24, [], [
    (set_merchandise_modifier_quality,100),
    (try_for_range,":cur_center",centers_begin, centers_end),
		(party_slot_eq, ":cur_center", slot_center_destroyed, 0), #TLD
        (party_get_slot,":cur_merchant",":cur_center",slot_town_merchant),
        (neq, ":cur_merchant", "trp_no_troop"),
        (reset_item_probabilities,100),     
        (troop_clear_inventory,":cur_merchant"),
        (store_troop_faction,":faction",":cur_merchant"),
		(faction_get_slot, ":faction_mask", ":faction", slot_faction_mask),
        (troop_get_slot,":subfaction",":cur_center", slot_troop_subfaction),
		(assign, ":subfaction_mask", 1),
		(try_for_range, ":unused", 0, ":subfaction"),(val_mul, ":subfaction_mask", 2),(try_end), #":subfaction_mask" = 2,4,8,16... if subfactions here

        (assign, ":is_orc_faction", 0),
        (try_begin),
          (this_or_next|eq, ":faction", "fac_mordor"),
          (this_or_next|eq, ":faction", "fac_isengard"),
          (this_or_next|eq, ":faction", "fac_moria"),
          (this_or_next|eq, ":faction", "fac_guldur"),
          (eq, ":faction", "fac_gundabad"),
          (assign, ":is_orc_faction", 1),
        (try_end),
        # (assign, ":is_elf_faction", 0),
        # (try_begin),
          # (this_or_next|eq, ":faction", "fac_imladris"),
          # (this_or_next|eq, ":faction", "fac_woodelf"),
          # (eq, ":faction", "fac_lorien"),
          # (assign, ":is_elf_faction", 1),
        # (try_end),
        (party_get_slot, ":center_str_income", ":cur_center", slot_center_strength_income),

        (try_for_range,":item","itm_sumpter_horse", "itm_warg_reward"),
            (item_get_slot,":item_faction_mask",":item",slot_item_faction),
            (val_and,":item_faction_mask",":faction_mask"),
			(try_begin),
				(eq,":item_faction_mask",0), # faction mismatch
				(set_item_probability_in_merchandise,":item",0),
			(else_try),
				(try_begin), # faction match but what about subfactions?
					(neq, ":subfaction", 0),
					(val_div, ":subfaction_mask", 2), #shift back
					(item_get_slot,":item_subfaction_mask",":item",slot_item_subfaction),
					(store_and,":subfaction_mask",":subfaction_mask",":item_subfaction_mask"), # subfaction mismatch
					(eq,":subfaction_mask",0),
					(set_item_probability_in_merchandise,":item", 0),  #  prob reduced to 0 %
				(try_end),
			(try_end),
        (try_end),
    # horses inventory
		(troop_get_slot,":skill","trp_skill2item_type",itp_type_horse), #abundance stored in merchant skills values
		(store_skill_level,":items",":skill",":cur_merchant"),         
		(try_begin),
            (gt,":items",0),
            (troop_add_merchandise,":cur_merchant",itp_type_horse,":items"),
        (try_end),
    
    # Add trade goods to merchant inventories
        (reset_item_probabilities,100),
        (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
            #MV: no non-edible trade goods and some factional food
            (try_begin),
              (is_between, ":cur_goods", food_begin, food_end),
              (this_or_next|eq, ":is_orc_faction", 1),
              (neq, ":cur_goods", "itm_human_meat"),
              # (this_or_next|eq, ":is_elf_faction", 1),
              # (neq, ":cur_goods", "itm_lembas"),
              (this_or_next|neg|faction_slot_eq, ":faction", slot_faction_side, faction_side_good),
              (neq, ":cur_goods", "itm_maggoty_bread"),
              (this_or_next|faction_slot_eq, ":faction", slot_faction_side, faction_side_good),
              (neq, ":cur_goods", "itm_cram"),
		  ## food quest: 
              (assign, ":quest_prevents", 0),
              (try_begin), # don't allow this food to generate if the quest says there is a shortage
                (check_quest_active, "qst_deliver_food"),
                (quest_slot_eq, "qst_deliver_food", slot_quest_target_center, ":cur_center"),
                #(quest_slot_eq, "qst_deliver_food", slot_quest_target_item, ":cur_goods"),
                (assign, ":quest_prevents", 1),
              (try_end),
              (eq, ":quest_prevents", 0),
              (set_item_probability_in_merchandise,":cur_goods",100),
            (else_try),
              (set_item_probability_in_merchandise,":cur_goods",0),
            (try_end),
            #(set_item_probability_in_merchandise,":cur_goods",":cur_probability"),
        (try_end),
        (store_div, ":num_goods", ":center_str_income", 5),
        (val_add, ":num_goods", num_merchandise_goods), #now 3-7
        (troop_add_merchandise,":cur_merchant",itp_type_goods,":num_goods"),
        (troop_ensure_inventory_space,":cur_merchant",merchant_inventory_space), #MV: moved after goods and changed from 65
        (troop_sort_inventory, ":cur_merchant"),
        (store_troop_gold, ":cur_gold",":cur_merchant"),
        (lt,":cur_gold",600),
        (store_random_in_range,":new_gold",200,400),
        (call_script, "script_troop_add_gold",":cur_merchant",":new_gold"),
	(try_end),
]),

#Kingdom Parties
(12, 0, 0, [],[  # TLD Parties spawn (foxyman)
      #corrupt saves possible retardant: limit number of total parties to 900
      (assign, ":total_parties", 0),
      (try_for_parties, ":unused"),
        (val_add, ":total_parties", 1),
      (try_end),

      (le, ":total_parties", "$tld_option_max_parties"),	# Modified: Let player's choose for their compatability -CppCoder
							 	#skip spawning if there are too many parties
     	 							#corrupt saves possible retardant: also limit the number of parties spawned at once

      (assign, ":to_spawn", 16),
      (try_begin),
	(store_div, ":spawn_slowdown", "$tld_option_max_parties", 6),
	(store_sub, ":spawn_slowdown", "$tld_option_max_parties", ":spawn_slowdown"),
        (ge, ":total_parties", ":spawn_slowdown"), #about 300 active parties, lords+bandits+patrols
        (assign, ":to_spawn", 10), #slows down spawning rate when there are many parties
      (try_end),
      
      #new: randomly choose centers to spawn parties from
      (assign, ":max_tries", 60),
      (try_for_range, ":unused", 0, ":max_tries"),
        (store_random_in_range, ":center", centers_begin, centers_end),
        (gt, ":to_spawn", 0),
        (party_is_active, ":center"),
        (party_slot_eq, ":center", slot_center_destroyed, 0), #TLD
        (party_get_slot, ":center_scouts", ":center", slot_center_spawn_scouts),
        (party_get_slot, ":center_raiders", ":center", slot_center_spawn_raiders),
        (party_get_slot, ":center_patrol", ":center", slot_center_spawn_patrol),
        (party_get_slot, ":center_caravan", ":center", slot_center_spawn_caravan),
	 #(display_message, "@DEBUG: Attempt to spawn parties", 0xFF00fd33),
        (try_begin),
            (store_faction_of_party, ":faction_no", ":center"),
            (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active), # faction lives
            (party_get_slot, ":center_theater", ":center", slot_center_theater),
            (faction_slot_eq, ":faction_no", slot_faction_active_theater, ":center_theater"), #center in faction's active theater
            
            (faction_get_slot, ":strength", ":faction_no", slot_faction_strength),
            (val_clamp, ":strength", 0, 5001), # keep spawning chance and max limit within reason 
                                               # 3.15 (was 7001): this should limit the Mordor and other swarms
			(store_div, ":chance_modifier", ":strength", 100),
            (val_sub, ":chance_modifier", 35), # -5 for str. 3000, 0 for 3500, +5 for 4000,... +35 for 7000 
            
            (try_begin),
                (gt, ":center_scouts", 0),
                #no warg scouts before the war starts
                (assign, ":early_wargs", 0),
                (try_begin),
                  (eq, "$tld_war_began", 0),
                  (this_or_next|eq, ":center_scouts", "pt_moria_scouts"),
                  (this_or_next|eq, ":center_scouts", "pt_gundabad_scouts"),
                  (eq, ":center_scouts", "pt_isengard_scouts_warg"),
                  (assign, ":early_wargs", 1),
                (try_end),
                (eq, ":early_wargs", 0),
                # (store_random_in_range, ":rand", 0, int(15000/ws_scout_freq_multiplier)), # 0-4285
                # (le, ":rand", ":strength"), # 81% for fac.str. 3500
                (store_add, ":chance", ws_scout_chance, ":chance_modifier"),
                (store_random_in_range, ":rand", 0, 100),
                (lt, ":rand", ":chance"), # 60% for fac.str. 3500
                (store_mul, ":limit", ":strength", ws_scout_limit_multiplier*1000),
                (val_div, ":limit", 3500*1000), #14 for fac.str. 3500; 28 for 7000
                # also limit by number of centers = 4+4*centers (8,12,16,20,..), to prevent minor factions map overcrowding 
                (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", spt_town),
                (store_mul, ":center_limit", reg0, 4), (val_add, ":center_limit", 4),
                (val_min, ":limit", ":center_limit"),
                (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", spt_scout),
                (lt, reg0, ":limit"),
                (set_spawn_radius, 1),
                (spawn_around_party, ":center", ":center_scouts"),
                (assign, ":scout_party", reg0),
        #(display_message, "@DEBUG: Party spawn scouts: {reg0}", 0xFF00fd33),
                (party_set_slot, ":scout_party", slot_party_type, spt_scout),
                (party_set_slot, ":scout_party", slot_party_home_center, ":center"),
				(party_set_slot, ":scout_party", slot_party_victory_value, ws_scout_vp), # victory points for party kill
                (party_set_faction, ":scout_party", ":faction_no"),
                (call_script, "script_find_closest_random_enemy_center_from_center", ":center"),
                (try_begin),
                    (neq, reg0, -1),
                    (assign, ":enemy_center", reg0),
                    (party_get_position, pos1, ":center"),
                    (party_get_position, pos2, ":enemy_center"),
                    (call_script, "script_calc_quarter_point"), # closer to home
                    #(call_script, "script_calc_mid_point"),
                (else_try),
                    (party_get_position, pos1, ":center"),
                (try_end),
                (party_set_slot, ":scout_party", slot_party_ai_object, ":enemy_center"),
                (party_set_slot, ":scout_party", slot_party_ai_state, spai_undefined),
                (party_set_ai_behavior, ":scout_party", ai_bhvr_patrol_location),
                (party_set_ai_target_position, ":scout_party", pos1),
                (party_set_ai_patrol_radius, ":scout_party", 10),
                (val_sub, ":to_spawn", 1),
            (try_end),
            (try_begin),
                (ge,"$tld_war_began",1), # No raiders before war
                (gt, ":center_raiders", 0),
                # (store_random_in_range, ":rand", 0, int(50000/ws_raider_freq_multiplier)), # 0-20000
                # (le, ":rand", ":strength"), # 17% for fac.str. 3500
                (store_add, ":chance", ws_raider_chance, ":chance_modifier"),
                (store_random_in_range, ":rand", 0, 100),
                (lt, ":rand", ":chance"), # 45% for fac.str. 3500
                (store_mul, ":limit", ":strength", ws_raider_limit_multiplier*1000),
                (val_div, ":limit", 3500*1000), #9 for fac.str. 3500
                # also limit by number of centers = 2+3*centers (5,8,11,14,..), to prevent minor factions map overcrowding 
                (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", spt_town),
                (store_mul, ":center_limit", reg0, 3), (val_add, ":center_limit", 2),
                (val_min, ":limit", ":center_limit"),
                (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", spt_raider),
                (lt, reg0, ":limit"),
                (set_spawn_radius, 1),
                (spawn_around_party, ":center", ":center_raiders"),
                (assign, ":raider_party", reg0),
                (party_set_slot, ":raider_party", slot_party_home_center, ":center"),
                (party_set_faction, ":raider_party", ":faction_no"),
                (party_set_ai_behavior, ":raider_party", ai_bhvr_patrol_party),
                (party_set_ai_patrol_radius, ":raider_party", 10),
                (party_set_slot, ":raider_party", slot_party_ai_state, spai_undefined),
                (party_set_slot, ":raider_party", slot_party_type, spt_raider),
				(party_set_slot, ":raider_party", slot_party_victory_value, ws_raider_vp), # victory points for party kill

                (call_script, "script_find_closest_random_enemy_center_from_center", ":center"),
                (try_begin),
                    (neq, reg0, -1),
                    (assign, ":enemy_center", reg0),
                (else_try),
                    (assign, ":enemy_center", ":center"),
                (try_end),
                (party_set_ai_object, ":raider_party", ":enemy_center"),
                (val_sub, ":to_spawn", 1),
            (try_end),                        
            (try_begin),
                (ge,"$tld_war_began",1), # No patrols before war
                (gt, ":center_patrol", 0),
                # (store_random_in_range, ":rand", 0, int(50000/ws_patrol_freq_multiplier)), # 0-33333
                # (le, ":rand", ":strength"), # 10% for fac.str. 3500
                (store_add, ":chance", ws_patrol_chance, ":chance_modifier"),
                (store_random_in_range, ":rand", 0, 100),
                (lt, ":rand", ":chance"), # 30% for fac.str. 3500
                (store_mul, ":limit", ":strength", ws_patrol_limit_multiplier*1000),
                (val_div, ":limit", 3500*1000), #6 for fac.str. 3500
                # also limit by number of centers = 1+2*centers (3,5,7,9,..), to prevent minor factions map overcrowding 
                (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", spt_town),
                (store_mul, ":center_limit", reg0, 2), (val_add, ":center_limit", 1),
                (val_min, ":limit", ":center_limit"),
                (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", spt_patrol),
                (lt, reg0, ":limit"),
                (set_spawn_radius, 1),
                (spawn_around_party, ":center", ":center_patrol"),
                (assign, ":patrol_party", reg0),
                (party_set_faction, ":patrol_party", ":faction_no"),
                (party_set_slot, ":patrol_party", slot_party_type, spt_patrol),
				(party_set_slot, ":patrol_party", slot_party_victory_value, ws_patrol_vp), # victory points for party kill
                (party_set_slot, ":patrol_party", slot_party_home_center, ":center"),

                (party_set_slot, ":patrol_party", slot_party_ai_state, spai_undefined),
                (party_set_ai_behavior, ":patrol_party", ai_bhvr_patrol_party),
                (party_set_ai_object, ":patrol_party", ":center"),
                (party_set_ai_patrol_radius, ":patrol_party", 15),
                (val_sub, ":to_spawn", 1),
            (try_end),
            (try_begin),
                (gt, ":center_caravan", 0),
                # (store_random_in_range, ":rand", 0, int(50000/ws_caravan_freq_multiplier)), # 0-20000
                # (le, ":rand", ":strength"), # 17% for fac.str. 3500
                (store_add, ":chance", ws_caravan_chance, ":chance_modifier"),
                (store_random_in_range, ":rand", 0, 100),
                (lt, ":rand", ":chance"), # 25% for fac.str. 3500
                (store_mul, ":limit", ":strength", ws_caravan_limit_multiplier*1000),
                (val_div, ":limit", 3500*1000), #5 for fac.str. 3500
                (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", spt_kingdom_caravan),
                (lt, reg0, ":limit"),
                (set_spawn_radius, 0),
                (spawn_around_party, ":center", ":center_caravan"),
                (assign, ":caravan_party", reg0),
                (party_set_faction, ":caravan_party", ":faction_no"),
                (party_set_slot, ":caravan_party", slot_party_home_center, ":center"),
                (party_set_slot, ":caravan_party", slot_party_type, spt_kingdom_caravan),
				(party_set_slot, ":caravan_party", slot_party_victory_value, ws_caravan_vp), # victory points for party kill
                
                (str_store_party_name, s1, ":caravan_party"),
                (str_store_party_name, s2, ":center"),
                (party_set_name, ":caravan_party", "@{s1} from {s2}"),

                (party_set_slot, ":caravan_party", slot_party_ai_state, spai_undefined),
                (party_set_ai_behavior, ":caravan_party", ai_bhvr_travel_to_party),
                (party_set_ai_object, ":caravan_party", ":center"),
                (party_set_flags, ":caravan_party", pf_default_behavior, 1),
                (val_sub, ":to_spawn", 1),
            (try_end),             
        (try_end),
        (try_begin),
          (le, ":to_spawn", 0),
          (assign, ":max_tries", 0), #exit loop
        (try_end),
      (try_end), #try_for_range
    ]
  ),

(0.1, 0, ti_once,
   [ #(entering_town,":party"),
     (neq,"$ambient_faction","$players_kingdom"),
	 (call_script, "script_cf_factions_are_allies", "$ambient_faction","$players_kingdom"),
   ],[	(str_store_faction_name, s11, "$ambient_faction"),
		(str_store_faction_name, s10, "$players_kingdom"),
		(dialog_box,"@When dealing with locals in {s11}, remember that they do not know you and they don't necessarily acknowledge the merits you've earned in {s10}.                                                                                                                      (the Resource Points which you can dispose of among people from {s11} are not the ones you earned in {s10}, but the ones you will earn in {s11} -- see also the Report screen)","@Info"),
	]),

#Companion quests

##  (0, 0, ti_once,
##   [ (entering_town,"p_town_minas_tirith"),
##     (main_party_has_troop,"trp_borcha"),
##     (eq,"$borcha_freed",0), ],
##   [ (assign,"$borcha_arrive_sargoth_as_prisoner",1),
##     (start_map_conversation,"trp_borcha"),]),
##
##  (1, 0, ti_once,
##   [  (map_free,0),
##      (eq,"$borcha_asked_for_freedom",0),
##      (main_party_has_troop,"trp_borcha"),],
##   [  (start_map_conversation,"trp_borcha"),]),
##  
##  (2, 0, ti_once,
##   [  (map_free, 0),
##      (neq,"$borcha_asked_for_freedom",0),
##      (eq,"$borcha_freed",0),
##      (main_party_has_troop,"trp_borcha"),],
##   [  (start_map_conversation,"trp_borcha"),]),

##### TODO: QUESTS COMMENT OUT BEGIN

###########################################################################
### Random Governer Quest triggers
###########################################################################

# Runaway Peasants quest
  (0.2, 0.0, 0.0,
   [
       (check_quest_active, "qst_bring_back_runaway_serfs"),
       (neg|check_quest_concluded, "qst_bring_back_runaway_serfs"),
       (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
       (quest_get_slot, ":quest_target_center", "qst_bring_back_runaway_serfs", slot_quest_target_center),
       (try_begin),
         (party_is_active, "$qst_bring_back_runaway_serfs_party_1"),
         (try_begin),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_1", ":quest_target_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_1"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_fleed", 1),
         (else_try),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_1", ":quest_object_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_1"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_returned", 1),
         (else_try),
           (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_bring_back_runaway_serfs_party_1"),
           (gt, ":cur_distance", 3),
           (party_set_ai_object, "$qst_bring_back_runaway_serfs_party_1", ":quest_target_center"),
         (try_end),
       (try_end),
       (try_begin),
         (party_is_active, "$qst_bring_back_runaway_serfs_party_2"),
         (try_begin),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_2", ":quest_target_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_2"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_fleed", 1),
         (else_try),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_2", ":quest_object_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_2"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_returned", 1),
         (else_try),
           (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_bring_back_runaway_serfs_party_2"),
           (gt, ":cur_distance", 3),
           (party_set_ai_object, "$qst_bring_back_runaway_serfs_party_2", ":quest_target_center"),
         (try_end),
       (try_end),
       (try_begin),
         (party_is_active, "$qst_bring_back_runaway_serfs_party_3"),
         (try_begin),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_3", ":quest_target_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_3"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_fleed", 1),
         (else_try),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_3", ":quest_object_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_3"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_returned", 1),
         (else_try),
           (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_bring_back_runaway_serfs_party_3"),
           (gt, ":cur_distance", 3),
           (party_set_ai_object, "$qst_bring_back_runaway_serfs_party_3", ":quest_target_center"),
         (try_end),
       (try_end),
       (assign, ":sum_removed", "$qst_bring_back_runaway_serfs_num_parties_returned"),
       (val_add, ":sum_removed", "$qst_bring_back_runaway_serfs_num_parties_fleed"),
       (ge, ":sum_removed", 3),
       (try_begin),
         (ge, "$qst_bring_back_runaway_serfs_num_parties_returned", 3),
         (call_script, "script_succeed_quest", "qst_bring_back_runaway_serfs"),
       (else_try),
         (eq, "$qst_bring_back_runaway_serfs_num_parties_returned", 0),
         (call_script, "script_fail_quest", "qst_bring_back_runaway_serfs"),
       (else_try),
         (call_script, "script_conclude_quest", "qst_bring_back_runaway_serfs"),
       (try_end),
    ],
   []
   ),


# Follow Spy quest
  (0.5, 0, 0,[	(check_quest_active, "qst_follow_spy"),
				(eq, "$qst_follow_spy_no_active_parties", 0),
    ],[(quest_get_slot, ":quest_giver_center", "qst_follow_spy", slot_quest_giver_center),
       (quest_get_slot, ":quest_object_center", "qst_follow_spy", slot_quest_object_center),
       (assign, ":abort_meeting", 0),
       (try_begin),
         (this_or_next|eq, "$qst_follow_spy_run_away", 1),
         (this_or_next|neg|party_is_active, "$qst_follow_spy_spy_party"),
         (neg|party_is_active, "$qst_follow_spy_spy_partners_party"),
       (else_try),
         (eq, "$qst_follow_spy_meeting_state", 0),
         (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_follow_spy_spy_party"),
         (try_begin),
           (assign, ":min_distance", 3),
           (try_begin),
             (is_currently_night),
             (assign, ":min_distance", 1),
           (try_end),
           (le, ":cur_distance", ":min_distance"),
           (store_distance_to_party_from_party, ":player_distance_to_quest_giver_center", "p_main_party", ":quest_giver_center"),
           (gt, ":player_distance_to_quest_giver_center", 1),
           (assign, ":abort_meeting", 1),
           (assign, "$qst_follow_spy_run_away", 1),
           (display_message, "str_qst_follow_spy_noticed_you"),
         (else_try),
           (store_distance_to_party_from_party, ":cur_distance", "$qst_follow_spy_spy_partners_party", "$qst_follow_spy_spy_party"),
           (le, ":cur_distance", 1),
           (party_attach_to_party, "$qst_follow_spy_spy_party", "$qst_follow_spy_spy_partners_party"),
           (assign, "$qst_follow_spy_meeting_state", 1),
           (assign, "$qst_follow_spy_meeting_counter", 0),
         (try_end),
       (else_try),
         (eq, "$qst_follow_spy_meeting_state", 1),
         (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_follow_spy_spy_partners_party"),
         (try_begin),
           (le, ":cur_distance", 1),
           (party_detach, "$qst_follow_spy_spy_party"),
           (assign, ":abort_meeting", 1),
           (assign, "$qst_follow_spy_run_away", 1),
           (display_message, "str_qst_follow_spy_noticed_you"),
         (else_try),
           (val_add, "$qst_follow_spy_meeting_counter", 1),
           (gt, "$qst_follow_spy_meeting_counter", 4),
           (party_detach, "$qst_follow_spy_spy_party"),
           (assign, ":abort_meeting", 0),
           (assign, "$qst_follow_spy_meeting_state", 2),
         (try_end),
       (try_end),
       (try_begin),
         (eq, ":abort_meeting", 1),
         (party_set_ai_object, "$qst_follow_spy_spy_party", ":quest_giver_center"),
         (party_set_ai_object, "$qst_follow_spy_spy_partners_party", ":quest_object_center"),
         (party_set_ai_behavior, "$qst_follow_spy_spy_party", ai_bhvr_travel_to_party),
         (party_set_ai_behavior, "$qst_follow_spy_spy_partners_party", ai_bhvr_travel_to_party),
         (party_set_flags, "$qst_follow_spy_spy_party", pf_default_behavior, 0),
         (party_set_flags, "$qst_follow_spy_spy_partners_party", pf_default_behavior, 0),
       (try_end),
       (assign, ":num_active", 0),
       (try_begin),
         (party_is_active, "$qst_follow_spy_spy_party"),
         (val_add, ":num_active", 1),
         (party_is_in_town, "$qst_follow_spy_spy_party", ":quest_giver_center"),
         (remove_party, "$qst_follow_spy_spy_party"),
         (assign, "$qst_follow_spy_spy_back_in_town", 1),
         (val_sub, ":num_active", 1),
       (try_end),
       (try_begin),
         (party_is_active, "$qst_follow_spy_spy_partners_party"),
         (val_add, ":num_active", 1),
         (party_is_in_town, "$qst_follow_spy_spy_partners_party", ":quest_object_center"),
         (remove_party, "$qst_follow_spy_spy_partners_party"),
         (assign, "$qst_follow_spy_partner_back_in_town", 1),
         (val_sub, ":num_active", 1),
       (try_end),
       (try_begin),
         (eq, "$qst_follow_spy_partner_back_in_town",1),
         (eq, "$qst_follow_spy_spy_back_in_town",1),
         (call_script, "script_fail_quest", "qst_follow_spy"),
       (try_end),
       (try_begin),
         (eq, ":num_active", 0),
         (assign, "$qst_follow_spy_no_active_parties", 1),
         (quest_get_slot, ":spy_troop", "qst_follow_spy", slot_quest_object_troop),
         (quest_get_slot, ":spy_partner", "qst_follow_spy", slot_quest_target_troop),
         (party_count_prisoners_of_type, ":num_spies", "p_main_party", ":spy_troop"),
         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", ":spy_partner"),
         (gt, ":num_spies", 0),
         (gt, ":num_spy_partners", 0),
         (call_script, "script_succeed_quest", "qst_follow_spy"),
       (try_end)]
),
### Raiders quest
##  (0.95, 0.0, 0.2,
##   [
##       (check_quest_active, "qst_hunt_down_raiders"),
##       (neg|check_quest_succeeded, "qst_hunt_down_raiders"),
##       (neg|check_quest_failed, "qst_hunt_down_raiders"),
##    ],
##   [
##       (quest_get_slot, ":quest_target_party", "qst_hunt_down_raiders", slot_quest_target_party),
##       (party_set_ai_behavior, ":quest_target_party", ai_bhvr_hold),
##       (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
##    ]
##   ),
##
##  (0.7, 0, 0.2,
##   [
##       (check_quest_active, "qst_hunt_down_raiders"),
##       (neg|check_quest_succeeded, "qst_hunt_down_raiders"),
##       (neg|check_quest_failed, "qst_hunt_down_raiders"),
##    ],
##   [
##       (quest_get_slot, ":quest_target_party", "qst_hunt_down_raiders", slot_quest_target_party),
##       (party_set_ai_behavior,":quest_target_party",ai_bhvr_travel_to_party),
##       (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
##    ]
##   ),
##  
##  (0.1, 0.0, 0.0,
##   [
##       (check_quest_active, "qst_hunt_down_raiders"),
##       (neg|check_quest_succeeded, "qst_hunt_down_raiders"),
##       (neg|check_quest_failed, "qst_hunt_down_raiders"),
##       (quest_get_slot, ":quest_target_party", "qst_hunt_down_raiders", slot_quest_target_party),
##       (neg|party_is_active, ":quest_target_party")
##    ],
##   [
##       (call_script, "script_succeed_quest", "qst_hunt_down_raiders"),
##    ]
##   ),
##  
##  (1.3, 0, 0.0,
##   [
##       (check_quest_active, "qst_hunt_down_raiders"),
##       (neg|check_quest_succeeded, "qst_hunt_down_raiders"),
##       (neg|check_quest_failed, "qst_hunt_down_raiders"),
##       (quest_get_slot, ":quest_target_party", "qst_hunt_down_raiders", slot_quest_target_party),
##       (quest_get_slot, ":quest_target_center", "qst_hunt_down_raiders", slot_quest_target_center),
##       (party_is_in_town,":quest_target_party",":quest_target_center")
##    ],
##   [
##       (call_script, "script_fail_quest", "qst_hunt_down_raiders"),
##       (display_message, "str_raiders_reached_base"),
##       (quest_get_slot, ":quest_target_party", "qst_hunt_down_raiders", slot_quest_target_party),
##       (remove_party, ":quest_target_party"),
##    ]
##   ),

##### TODO: QUESTS COMMENT OUT END

#########################################################################
# Random MERCHANT quest triggers
####################################  
 # Apply interest to merchants guild debt  1% per week
  # (24 * 7, 0, 0,
   # [],
   # [   (val_mul,"$debt_to_merchants_guild",101),
       # (val_div,"$debt_to_merchants_guild",100)
    # ]
   # ),
# Escort merchant caravan:
  (0.1, 0.0, 0.1, [(check_quest_active, "qst_escort_merchant_caravan"),
                   (eq, "$escort_merchant_caravan_mode", 1)
                   ],
                  [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                   (try_begin),
                     (party_is_active, ":quest_target_party"),
                     (party_set_ai_behavior, ":quest_target_party", ai_bhvr_hold),
                     (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                   (try_end),
                   ]),
  (0.1, 0.0, 0.1, [(check_quest_active, "qst_escort_merchant_caravan"),
                    (eq, "$escort_merchant_caravan_mode", 0),
                    ],
                   [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                    (try_begin),
                      (party_is_active, ":quest_target_party"),
                      (party_set_ai_behavior, ":quest_target_party", ai_bhvr_escort_party),
                      (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                      (party_set_ai_object, ":quest_target_party", "p_main_party"),
                    (try_end),
                    ]),

  (0.1, 0, 0.0, [(check_quest_active, "qst_escort_merchant_caravan"),
                 (quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                 (neg|party_is_active,":quest_target_party"),
                 ],
                [(call_script, "script_abort_quest", "qst_escort_merchant_caravan", 2),
                 ]),

# Troublesome bandits
  (0.3, 0.0, 1.1, [(check_quest_active, "qst_troublesome_bandits"),
                   (neg|check_quest_failed, "qst_troublesome_bandits"),
                   (store_num_parties_destroyed, ":cur_eliminated", "pt_troublesome_bandits"),
                   (lt, "$qst_troublesome_bandits_eliminated", ":cur_eliminated"),
                   (store_num_parties_destroyed_by_player, ":cur_eliminated_by_player", "pt_troublesome_bandits"),
                   (eq, ":cur_eliminated_by_player", "$qst_troublesome_bandits_eliminated_by_player"),
                   ],
                  [(display_message, "str_bandits_eliminated_by_another"),
                   (call_script, "script_abort_quest", "qst_troublesome_bandits", 2),
                   ]),

  (0.3, 0.0, 1.1, [(check_quest_active, "qst_troublesome_bandits"),
                   (neg|check_quest_succeeded, "qst_troublesome_bandits"),
                   (store_num_parties_destroyed, ":cur_eliminated", "pt_troublesome_bandits"),
                   (lt, "$qst_troublesome_bandits_eliminated", ":cur_eliminated"),
                   (store_num_parties_destroyed_by_player, ":cur_eliminated_by_player", "pt_troublesome_bandits"),
                   (neq, ":cur_eliminated_by_player", "$qst_troublesome_bandits_eliminated_by_player"),
                   ],
                  [(call_script, "script_succeed_quest", "qst_troublesome_bandits"),]),
                  
  (0.3, 0.0, 1.1, [(check_quest_active, "qst_treebeard_kill_orcs"),
                   (neg|check_quest_succeeded, "qst_treebeard_kill_orcs"),
                   (store_num_parties_destroyed_by_player, ":cur_eliminated_by_player", "pt_fangorn_orcs"),
                   (gt, ":cur_eliminated_by_player", 0),
                   ],
                  [(call_script, "script_succeed_quest", "qst_treebeard_kill_orcs"),]),

# Kidnapped girl:
   # (1, 0, 0,
   # [(check_quest_active, "qst_kidnapped_girl"),
    # (quest_get_slot, ":quest_target_party", "qst_kidnapped_girl", slot_quest_target_party),
    # (party_is_active, ":quest_target_party"),
    # (party_is_in_any_town, ":quest_target_party"),
    # (remove_party, ":quest_target_party"),
    # ],
   # []
   # ),

#NPC system changes begin
#Move unemployed NPCs around taverns
   # (24 * 15, 0, 0, [(call_script, "script_update_companion_candidates_in_taverns")],[]),

#Process morale and determine personality clashes
  (0, 0, 24,
   [],
[
#Count NPCs in party and get the "grievance divisor", which determines how fast grievances go away
#Set their relation to the player
        (assign, ":npcs_in_party", 0),
        (assign, ":grievance_divisor", 100),
        (try_for_range, ":npc1", companions_begin, companions_end),
            (main_party_has_troop, ":npc1"),
            (val_add, ":npcs_in_party", 1),
        (try_end),
        (val_sub, ":grievance_divisor", ":npcs_in_party"),
        (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
        (val_add, ":grievance_divisor", ":persuasion_level"),
        (assign, reg7, ":grievance_divisor"),

#        (display_message, "@Process NPC changes. GD: {reg7}"),



##Activate personality clash from 24 hours ago
        (try_begin), #scheduled personality clashes require at least 24hrs together
             (gt, "$personality_clash_after_24_hrs", 0),
             (eq, "$disable_npc_complaints", 0),
             (try_begin),
                  (troop_get_slot, ":other_npc", "$personality_clash_after_24_hrs", slot_troop_personalityclash_object),
                  (main_party_has_troop, "$personality_clash_after_24_hrs"),
                  (main_party_has_troop, ":other_npc"),
                  (assign, "$npc_with_personality_clash", "$personality_clash_after_24_hrs"),
             (try_end),
             (assign, "$personality_clash_after_24_hrs", 0),
        (try_end),
#

         
        (try_for_range, ":npc", companions_begin, companions_end),
###Reset meeting variables
            (troop_set_slot, ":npc", slot_troop_turned_down_twice, 0),
            (try_begin),
                (troop_slot_eq, ":npc", slot_troop_met, 1),
                (troop_set_slot, ":npc", slot_troop_met_previously, 1),
            (try_end),

###Check for coming out of retirement
            # (troop_get_slot, ":occupation", ":npc", slot_troop_occupation),
            # (try_begin),
                # (eq, ":occupation", slto_retirement),
                # (troop_get_slot, ":renown_min", ":npc", slot_troop_return_renown),

                # (str_store_troop_name, s31, ":npc"),
                # (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
                # (assign, reg4, ":player_renown"),
                # (assign, reg5, ":renown_min"),
# #                (display_message, "@Test {s31}  for retirement return {reg4}, {reg5}."),

                # (gt, ":player_renown", ":renown_min"),
                # (troop_set_slot, ":npc", slot_troop_personalityclash_penalties, 0),
                # (troop_set_slot, ":npc", slot_troop_morality_penalties, 0),
                # (troop_set_slot, ":npc", slot_troop_occupation, 0),
            # (try_end),




            (try_begin),
                (main_party_has_troop, ":npc"),

#Check for quitting
                # (call_script, "script_npc_morale", ":npc"),
                # (assign, ":npc_morale", reg0),

                # (try_begin),
                    # (lt, ":npc_morale", 20),
                    # (store_random_in_range, ":random", 0, 100),
                    # (val_add, ":npc_morale", ":random"),
                    # (lt, ":npc_morale", 20),
                    # (assign, "$npc_is_quitting", ":npc"),
                # (try_end),

#Reduce grievance over time (or augment, if party is overcrowded
                (troop_get_slot, ":grievance", ":npc", slot_troop_personalityclash_penalties),
                (val_mul, ":grievance", 90),
                (val_div, ":grievance", ":grievance_divisor"),
                (troop_set_slot, ":npc", slot_troop_personalityclash_penalties, ":grievance"),

                (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                (val_mul, ":grievance", 90),
                (val_div, ":grievance", ":grievance_divisor"),
                (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),


#Change personality grievance levels
                (try_begin),
                    (this_or_next|troop_slot_ge, ":npc", slot_troop_personalityclash_state, 1),
                        (eq, "$disable_npc_complaints", 1),
                    (troop_get_slot, ":object", ":npc", slot_troop_personalityclash_object),
                    (main_party_has_troop, ":object"),
                    (call_script, "script_reduce_companion_morale_for_clash", ":npc", ":object", slot_troop_personalityclash_state),
                (try_end),
                (try_begin),
                    (this_or_next|troop_slot_ge, ":npc", slot_troop_personalityclash2_state, 1),
                        (eq, "$disable_npc_complaints", 1),
                    (troop_get_slot, ":object", ":npc", slot_troop_personalityclash2_object),
                    (main_party_has_troop, ":object"),
                    (call_script, "script_reduce_companion_morale_for_clash", ":npc", ":object", slot_troop_personalityclash2_state),
                (try_end),
                (try_begin),
                    (this_or_next|troop_slot_ge, ":npc", slot_troop_personalitymatch_state, 1),
                        (eq, "$disable_npc_complaints", 1),
                    (troop_get_slot, ":object", ":npc", slot_troop_personalitymatch_object),
                    (main_party_has_troop, ":object"),
                    (troop_get_slot, ":grievance", ":npc", slot_troop_personalityclash_penalties),
                    (val_mul, ":grievance", 9),
                    (val_div, ":grievance", 10),
                    (troop_set_slot, ":npc", slot_troop_personalityclash_penalties, ":grievance"),
                (try_end),

#Check for new personality clashes

#Active personality clash 1 if at least 24 hours have passed
                (try_begin),
                    (eq, "$disable_npc_complaints", 0),
                    (eq, "$npc_with_personality_clash", 0),
                    (eq, "$npc_with_personality_clash_2", 0),
                    (eq, "$personality_clash_after_24_hrs", 0),
                    (troop_slot_eq, ":npc", slot_troop_personalityclash_state, 0),
                    (troop_get_slot, ":other_npc", ":npc", slot_troop_personalityclash_object),
                    (main_party_has_troop, ":other_npc"),
                    (assign, "$personality_clash_after_24_hrs", ":npc"),
# (str_store_troop_name, s4, ":npc"),
# (str_store_troop_name, s5, ":other_npc"),
# (display_message, "@Debug: activated clash1 between {s4} and {s5}."),
                (try_end),

#Personality clash 2 and personality match is triggered by battles

            (try_end),
        (try_end),
    ]),
    

# TLD initialization
    (0, 0, ti_once, [], [
### TLD troop penalties initialization (foxyman)
        (try_for_range, ":troop_id", tld_troops_begin, tld_troops_end),
            (troop_get_type, ":troop_type", ":troop_id"),
            (try_begin),
            ]+concatenate_scripts([
                [
                (eq, ":troop_type", Penalties_sys[x][0]),
                (assign, reg0, ":troop_type"),
                #(display_message, "@DEBUG: Troop type: {reg0}", 0xff00ff),
                ]+concatenate_scripts([
                    [
                    (try_begin),
                        (gt, Penalties_sys[x][1][y][1], 0),
                        (troop_raise_skill, ":troop_id", Penalties_sys[x][1][y][0], Penalties_sys[x][1][y][1]),
                    (try_end),
                    ] for y in range(len(Penalties_sys[x][1]))
                ]+[
                    [
                    #debug_point_2,
                    (store_proficiency_level, ":prof", ":troop_id", Penalties_sys[x][2][y][0]),
                    (store_mul, ":pen_prof", ":prof", Penalties_sys[x][2][y][1]),
                    (val_div, ":pen_prof", 100),
                    (assign, reg0, ":pen_prof"),
                    #(display_message, "@Penalty: {reg0}", 0xff00ff),
                    (try_begin),
                        (lt, ":pen_prof", 0),
                        (troop_raise_proficiency_linear, ":troop_id", Penalties_sys[x][2][y][0], ":pen_prof"),
                    (try_end),
                    (troop_set_slot, ":troop_id", slot_troop_prof_night_penalties_begin+y, ":pen_prof"),
                    ] for y in range(len(Penalties_sys[x][2]))
                ])+[
            (else_try),                    
                ] for x in range(len(Penalties_sys))
            ])+[
            (try_end),
        (try_end),
        ]
    ),
	
#TLD Info about magic items	in inventory! (mtarini)
(1, 0, ti_once, [(player_has_item,"itm_ent_water")],[
		(dialog_box,"@You came into a possession of a strange, oversized bowl of fresh-looking water. It smells a little like musk.","@Obtained: Ent water."),
		(play_sound,"snd_quest_completed"),
]),

#TLD magic items stuff(mtarini)
(12, 12,ti_once,[(eq,"$g_ent_water_taking_effect",1),
				 (troop_get_type,reg5,"trp_player"),
				 (store_troop_health,reg6, "trp_player"),
				 (ge|this_or_next, reg6, 95), # takes effect only after you fully recovered...
				 (neg|is_between,reg5,tf_orc_begin, tf_orc_end), # or regardless of health, if you are not an orc
	   ],[
	    (assign, "$g_ent_water_taking_effect", 0),
		(try_begin),
		  (is_between,reg5,tf_orc_begin, tf_orc_end),
  		  (dialog_box,"@A little after you fully recover from drinking the poisoned water you got from the walking trees, you start noticing a strange side effect. The worms in your group seem to... respect you and fear you more, as if you turned... bigger. And you would swear that you are, indeed, a bit taller. Is that really possible?","@Ent water effect."),
		(else_try),
		  (dialog_box,"@The water you drank from the Ents had a strange effect on your body. Initially you didn't believe it possible, but now,  in front of evidence, you must admit it: somehow, you grew taller! Still, the poison almost killed you. You will never take that risk again."),
		(try_end),
		(troop_raise_attribute,"trp_player",ca_strength,1),
		(troop_raise_attribute,"trp_player",ca_charisma,1),
		(display_log_message,"@Ent water effect: increase stature!"),
		(display_log_message,"@ +1 to Strength (permanent)"),
		(display_log_message,"@ +1 to Charisma (permanent)"),
]),
	
# TLD War beginning condition (player level >= 8 at the moment), GA
(1, 0, 0,[	(eq,"$tld_war_began",0),
			(store_character_level,":level","trp_player"),
			(ge,":level",tld_player_level_to_begin_war),
	   ],[
		(assign, "$tld_war_began",1),
		(dialog_box,"@The dark shadow finally broke into a storm, and evil hordes started their march on the free people of Middle Earth. Mordor against Gondor in the South, Isengard agains Rohan in the West, Dol Guldur against the Elves... Even in the far North there is a war of its own.","@The War has started!"),
		(play_sound,"snd_evil_horn"),
	# move Dun camp across Isen
		(party_get_position, pos1, "p_town_dunland_camp"),
		(position_move_x,pos1,-400),
		(position_move_y,pos1,500),
		(party_set_position, "p_town_dunland_camp", pos1),
	#	reveal evil camps through the land
		(try_for_range,":center",centers_begin,centers_end),
          (neg|party_is_active,":center"),
          (store_faction_of_party, ":cur_faction", ":center"),
          (neg|faction_slot_eq, ":cur_faction", slot_faction_advance_camp, ":center"), # don't reveal advance camps
		  (enable_party,":center"),
          (call_script, "script_update_center_notes", ":center"),
    # and reinforce
          (assign, ":garrison_strength", 13),
          (party_get_slot, ":garrison_limit", ":center", slot_center_garrison_limit),
          (try_for_range, ":unused", 0, ":garrison_strength"),
            (call_script, "script_cf_reinforce_party", ":center"),
            (try_begin), #TLD: don't go overboard
              (party_get_num_companions, ":garrison_size", ":center"),
              (le, ":garrison_limit", ":garrison_size"),
              (assign, ":garrison_strength", 0),
            (try_end),
          (try_end),
		(try_end),
    # start the intro cutscene sequence
		(try_begin),
			(eq, "$tld_option_cutscenes",1),
			(jump_to_menu, "mnu_auto_intro_rohan"),
		(try_end),
]),
	
(0.5, 0, 0, [],[#(gt,"$g_fangorn_rope_pulled",-100)],[
	(call_script,"script_party_is_in_fangorn","p_main_party"),
	(assign,":inside_fangorn",reg0),
	(try_begin),
	  (eq, "$g_player_is_captive", 0),
	  (eq,":inside_fangorn",1),
      (troop_slot_eq, "trp_treebeard", slot_troop_met_previously, 0), # and didn't meet Treabeard
	  #(assign,reg5,"$g_fangorn_rope_pulled"),
      (try_begin),
        (lt, "$g_fangorn_rope_pulled", 25),
        (str_store_string, s11, "@The forest seems peaceful."),
      (else_try),
        (lt, "$g_fangorn_rope_pulled", 50),
        (str_store_string, s11, "@There is a sense of danger in the air."),
      (else_try),
        (lt, "$g_fangorn_rope_pulled", 75),
        (str_store_string, s11, "@You have a feeling you disturbed the forest for long enough."),
      (else_try),
        (str_store_string, s11, "@Get out, now!"),
      (try_end),
      (display_message,"@You are inside Fangorn. {s11}"),
	  (store_random_in_range,":chance",0,100),
	  (lt,":chance",25),
	  (jump_to_menu,"mnu_fangorn_danger"),
	(try_end),
	(try_begin),
	  (eq,":inside_fangorn",0),	
	  (ge,"$g_fangorn_rope_pulled",5),
	  (val_sub,"$g_fangorn_rope_pulled", 5), # if outside fangorn, fangorn calms down (to 0).
	  (val_max,"$g_fangorn_rope_pulled", 0),
	(try_end),
]),

# Orc parties eat prisoners at night
(0, 18, 6, [(faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good)], #MV: only affects good sides
[
#        debug_point_4,
#        (try_begin),
#            (is_currently_night),
#            (display_message, "@DEBUG: Currently night", debug_color),
#        (try_end),
        (try_for_parties, ":party_no"),
            (party_get_slot, ":party_type", ":party_no", slot_party_type), 
            (this_or_next|eq, ":party_type", spt_patrol),
            (this_or_next|eq, ":party_type", spt_raider),
            (this_or_next|eq, ":party_type", spt_scout),
            (this_or_next|eq, ":party_type", spt_kingdom_caravan),
            (this_or_next|eq, ":party_type", spt_prisoner_train),
            (this_or_next|eq, ":party_type", spt_kingdom_hero_party),
            (eq, ":party_type", spt_bandit),
            (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
            (ge, ":troop_no", 0), #MV fix: apparently sometimes it's -1: empty party?
            (troop_get_type, ":race", ":troop_no"),
            (is_between, ":race", tf_orc_begin, tf_orc_end),
            (party_get_num_prisoner_stacks, ":num_pri_stk", ":party_no"),
            (gt, ":num_pri_stk", 0),
            (party_get_battle_opponent, ":opponent", ":party_no"),
            (eq, ":opponent", -1),
            (store_party_size_wo_prisoners, ":num_comps", ":party_no"),
#            (store_party_size, ":num_pri", ":party_no"),
            (val_div, ":num_comps", 10),
            (val_max, ":num_comps", 1),
#            (val_sub, ":num_pri", ":num_comps"),
#            (val_mul, ":num_pri", 10), #1/10 of the number of party companions equivalent prinsoners eaten
            (try_for_range, ":stk_no", 0, ":num_pri_stk"),
                (party_prisoner_stack_get_size, ":size", ":party_no", ":stk_no"),
                (party_prisoner_stack_get_troop_id, ":troop_id", ":party_no", ":stk_no"),
#                (assign, reg0, ":size"),
#                (assign, reg1, ":troop_id"),
#                (display_message, "@DEBUG: id: {reg1} num: {reg0}", debug_color),
                (try_begin),
#                    (gt, ":size", 1),
                    (val_min, ":size", ":num_comps"),
                    (party_remove_prisoners, ":party_no", ":troop_id", ":size"),
                    (assign, ":num_pri_stk", 0),
#                (else_try),
#                    (store_random_in_range, ":rand", 0, ":num_pri"),
#                    (lt, ":rand", ":num_comps"),
#                    (party_remove_prisoners, ":party_no", ":troop_id", 1),
                (try_end),
            (try_end),
            (store_distance_to_party_from_party, ":dis", ":party_no", "p_main_party"),
            (le, ":dis", 3),  #TODO: Adjust this distance later
            (display_message, "@Your party witnessed orcs eating prisoners.", 0xffaa3333),
            (party_get_morale, ":morale", "p_main_party"),
            (try_begin),
                (gt, ":morale", 50), # base morale high, get boost
                (display_message, "@Your party's morale has risen from hatred.", 0xffaa3333), # CC: was "Your companions' morale has risen from hatred.", 0xffaa3333
                (val_add, ":morale", 10),
            (else_try), # base morale low, drop in fear
                (display_message, "@Your party's morale has fallen from fear.", 0xffaa3333), # CC: was "Your companions' morale has dropped from fear.", 0xffaa3333
                (val_sub, ":morale", 10),
            (try_end),
            (party_set_morale, "p_main_party", ":morale"),
        (try_end),        
]),

### war start movie sequence  
#  (0.1, 0.04, ti_once, [(map_free,0),],[#(key_clicked,key_k)],[
#   (party_get_position,pos33,"p_main_party"),
#	(display_message,"@The War has started!"),
#	(set_camera_follow_party,"p_town_isengard"), 
#   (assign,"$warmovie",1),
#  ]),
#  (0, 0.04, ti_once, [(eq,"$warmovie",1)],[
#	(display_message,"@Rhun riders attack in the north"),
#	(set_camera_follow_party,"p_town_erebor"), 
#   (assign,"$warmovie",2),
#  ]),  
#  (0, 0.04, ti_once, [(eq,"$warmovie",2)],[
#	(display_message,"@Fierce desert warriors of Khand in the center"),
#	(set_camera_follow_party,"p_town_khand_camp"),
#   (assign,"$warmovie",3),
#  ]),  
#  (0, 0.04, ti_once, [(eq,"$warmovie",3),
#   (display_message,"@Go now, and help free people of MiddleEarth"),],[
#	(display_message,"@Because time is running out!"),
#	(set_camera_follow_party,"p_town_khand_camp"), 
#   (assign,"$warmovie",4),
#  ]),
#  (0, 0.04, ti_once, [(eq,"$warmovie",4),
#   (display_message,"@Go now, and help free people of MiddleEarth"),],[
#	(display_message,"@Because time is running out!"),
#	(set_camera_follow_party,"p_main_party"), 
#   (assign,"$warmovie",5),
#  ]), 

#################################################################################
# starting quest WIP
# (1, 0, ti_once, [(map_free,0)],[(jump_to_menu,"mnu_starting_quest_good"),]
# ),

#################################################################################
(1, 0, 168, [], [ #traits crunching
	# traits effect on influence
	(try_begin),
		(try_begin),
            		(troop_slot_eq, "trp_traits", slot_trait_oathkeeper, 1),
			(faction_get_slot, reg1, "$players_kingdom", slot_faction_influence),
			(faction_get_slot, reg2, "$players_kingdom", slot_faction_influence),
			(lt, reg1, tld_if_cap),
			(val_add, reg1, tld_influence_trait_bonus),
        		(str_store_string, s27, "str_trait_title_oathkeeper"),
			(faction_set_slot, "$players_kingdom", slot_faction_influence, reg1),
			(str_store_faction_name, s1, "$players_kingdom"),
			(display_log_message, "@{s27}: Influence with {s1} increases from {reg2} to {reg1}.", color_good_news),
		(try_end),
		(try_begin),
            		(troop_slot_eq, "trp_traits", slot_trait_reverent, 1),
			(faction_get_slot, reg1, "$players_kingdom", slot_faction_influence),
			(faction_get_slot, reg2, "$players_kingdom", slot_faction_influence),
			(lt, reg1, tld_if_cap),
			(val_add, reg1, tld_influence_trait_bonus),
        		(str_store_string, s27, "str_trait_title_reverent"),
			(faction_set_slot, "$players_kingdom", slot_faction_influence, reg1),
			(str_store_faction_name, s1, "$players_kingdom"),
			(display_log_message, "@{s27}: Influence with {s1} increases from {reg2} to {reg1}.", color_good_news),
		(try_end),
		(try_begin),
            		(troop_slot_eq, "trp_traits", slot_trait_merciful, 1),
			(faction_get_slot, reg1, "$players_kingdom", slot_faction_influence),
			(faction_get_slot, reg2, "$players_kingdom", slot_faction_influence),
			(lt, reg1, tld_if_cap),
			(val_add, reg1, tld_influence_trait_bonus),
        		(str_store_string, s27, "str_trait_title_merciful"),
			(faction_set_slot, "$players_kingdom", slot_faction_influence, reg1),
			(str_store_faction_name, s1, "$players_kingdom"),
			(display_log_message, "@{s27}: Influence with {s1} increases from {reg2} to {reg1}.", color_good_news),
		(try_end),
		(try_begin),
            		(troop_slot_eq, "trp_traits", slot_trait_despoiler, 1),
			(faction_get_slot, reg1, "$players_kingdom", slot_faction_influence),
			(faction_get_slot, reg2, "$players_kingdom", slot_faction_influence),
			(lt, reg1, tld_if_cap),
			(val_add, reg1, tld_influence_trait_bonus),
        		(str_store_string, s27, "str_trait_title_despoiler"),
			(faction_set_slot, "$players_kingdom", slot_faction_influence, reg1),
			(str_store_faction_name, s1, "$players_kingdom"),
			(display_log_message, "@{s27}: Influence with {s1} increases from {reg2} to {reg1}.", color_good_news),
		(try_end),
		(try_begin),
            		(troop_slot_eq, "trp_traits", slot_trait_oathbreaker, 1),
			(faction_get_slot, reg1, "$players_kingdom", slot_faction_influence),
			(faction_get_slot, reg2, "$players_kingdom", slot_faction_influence),
			(ge, reg1, 1),
			(try_begin),
				(ge, reg1, tld_influence_trait_bonus),
				(val_sub, reg1, tld_influence_trait_bonus),
			(else_try),
				(val_sub, reg1, 1),
			(try_end),
        		(str_store_string, s27, "str_trait_title_oathbreaker"),
			(faction_set_slot, "$players_kingdom", slot_faction_influence, reg1),
			(str_store_faction_name, s1, "$players_kingdom"),
			(display_log_message, "@{s27}: Influence with {s1} decreases from {reg2} to {reg1}.", color_bad_news),
		(try_end),
	(try_end),
	# traits effect on party morale
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_foe_hammer, 1),
		(party_get_morale, ":morale", "p_main_party"),
		(val_mul, ":morale", 10),
		(val_div, ":morale", 9),
		(party_set_morale, "p_main_party", ":morale"),
        (str_store_string, s27, "str_trait_title_foe_hammer"),
        (display_log_message, "@{s27}: Party morale increased.", color_good_news),
	(try_end),
	(try_begin),
        (this_or_next|troop_slot_eq, "trp_traits", slot_trait_battle_scarred, 1),
        (troop_slot_eq, "trp_traits", slot_trait_fell_beast, 1),
		(party_get_morale, ":morale", "p_main_party"),
		(val_mul, ":morale", 10),
		(val_div, ":morale", 9),
		(party_set_morale, "p_main_party", ":morale"),
        (try_begin),
          (troop_slot_eq, "trp_traits", slot_trait_battle_scarred, 1),
          (str_store_string, s27, "str_trait_title_battle_scarred"),
        (else_try),
          (str_store_string, s27, "str_trait_title_fell_beast"),
        (try_end),
        (display_log_message, "@{s27}: Party morale increased.", color_good_news),
	(try_end),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_orc_pit_champion, 1),
		(party_get_morale, ":morale", "p_main_party"),
		(val_mul, ":morale", 10),
		(val_div, ":morale", 9),
		(party_set_morale, "p_main_party", ":morale"), 
        (str_store_string, s27, "str_trait_title_orc_pit_champion"),
        (display_log_message, "@{s27}: Party morale increased.", color_good_news),
	(try_end),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_bravery, 1),
		(party_get_morale, ":morale", "p_main_party"),
		(val_mul, ":morale", 10),
		(val_div, ":morale", 9),
		(party_set_morale, "p_main_party", ":morale"), 
        (str_store_string, s27, "str_trait_title_bravery"),
        (display_log_message, "@{s27}: Party morale increased.", color_good_news),
	(try_end),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_accursed, 1),
		(party_get_morale, ":morale", "p_main_party"),
		(val_div, ":morale", 10),
		(val_mul, ":morale", 9),
		(party_set_morale, "p_main_party", ":morale"), 
        (str_store_string, s27, "str_trait_title_accursed"),
        (display_log_message, "@{s27}: Party morale decreased.", color_bad_news),
	(try_end),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_merciful, 1),
		(party_get_morale, ":morale", "p_main_party"),
		(val_div, ":morale", 10),
		(val_mul, ":morale", 9),
		(party_set_morale, "p_main_party", ":morale"), 
        (str_store_string, s27, "str_trait_title_merciful"),
        (display_log_message, "@{s27}: Party morale decreased.", color_bad_news),
	(try_end),
  # gaining new traits
	(try_begin),
		(call_script, "script_cf_check_trait_captain"),
	(try_end),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_command_voice, 0),
		(gt, "$trait_check_commands_issued", 0),
		(store_skill_level, ":check", skl_leadership, "trp_player"),
		(ge, ":check", 5),
		(assign, ":check", "$trait_check_commands_issued"),
		(val_mul, ":check", 7),
		(assign, "$trait_check_commands_issued", 0),
		(store_random, ":rnd", 100),
		(neg|ge, ":rnd", ":check"),
		(call_script, "script_cf_gain_trait_command_voice"),
	(try_end),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_stealthy, 0),
		(gt, "$trait_check_stealth_success", 0),
		(store_skill_level, ":check", skl_pathfinding, "trp_player"),
		(ge, ":check", 3),
		(assign, ":check", "$trait_check_stealth_success"),
		(val_mul, ":check", 10),
		(assign, "$trait_check_stealth_success", 0),
		(store_random, ":rnd", 100),
		(neg|ge, ":rnd", ":check"),
		(call_script, "script_cf_gain_trait_stealthy"),
	(try_end),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_berserker, 0),
		(gt, "$trait_check_unarmored_berserker", 0),
		(assign, ":check", "$trait_check_unarmored_berserker"),
		(val_mul, ":check", 5),
		(assign, "$trait_check_unarmored_berserker", 0),
		(store_random, ":rnd", 100),
		(neg|ge, ":rnd", ":check"),
		(store_skill_level, ":check", skl_ironflesh, "trp_player"),
		(ge, ":check", 6),
		(call_script, "script_cf_gain_trait_berserker"),
	(try_end),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_battle_scarred, 0),
        (troop_slot_eq, "trp_traits", slot_trait_fell_beast, 0),
		(gt, "$trait_check_battle_scarred", 0),
		(assign, ":check", "$trait_check_battle_scarred"),
		(val_mul, ":check", 3),
		(assign, "$trait_check_battle_scarred", 0),
		(gt, ":check", 15),
		(store_random, ":rnd", 100),
		(neg|ge, ":rnd", ":check"),
		(call_script, "script_cf_gain_trait_battle_scarred"),
		(call_script, "script_cf_gain_trait_fell_beast"), #MV: let the scripts sort out if it's an orc or not :)
	(try_end),
	(try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_foe_hammer, 0),
		(assign, ":count", 0),
		(store_troop_faction, ":tmp", "trp_player"),
		(faction_get_slot, ":player_side", ":tmp", slot_faction_side),
		(try_for_range, ":hero", heroes_begin, heroes_end), # count heroes brutally killed by player
			(troop_slot_eq, ":hero", slot_troop_wound_mask, wound_death),
			# insert condition for being killed by player
			(store_troop_faction, ":tmp", ":hero"),
			(faction_get_slot, ":hero_side", ":tmp", slot_faction_side),
			(try_begin),
				 (eq, ":player_side", faction_side_good),
				 (neq, ":hero_side", faction_side_good),
				 (val_add, ":count", 1),
			(else_try),
				 (eq, ":player_side", faction_side_eye),
				 (neq, ":hero_side", faction_side_eye),
				 (val_add, ":count", 1),
			(else_try),
				 (eq, ":player_side", faction_side_hand),
				 (neq, ":hero_side", faction_side_hand),
				(val_add, ":count", 1),
			(try_end),
		(try_end),
		(ge, ":count", 2),
		(val_mul, ":count", 8),
		(store_random, ":rnd", 100),
		(neg|ge, ":rnd", ":count"), 
		(call_script, "script_cf_gain_trait_foe_hammer"),
	(try_end),
	#(assign, "$minas_tirith_healing", 0),
	#(assign, "$edoras_healing"      , 0),
	#(assign, "$isengard_healing"    , 0),
	#(assign, "$morannon_healing"    , 0),
]),

#check progress on oath quest
(24, 0, 0, [(check_quest_active, "qst_oath_of_vengeance", 1)],[
	(quest_get_slot, ":start_killcount", "qst_oath_of_vengeance", 3),
	(quest_get_slot, ":target", "qst_oath_of_vengeance", 2),
	(quest_get_slot, ":start_day", "qst_oath_of_vengeance", 1),
	(quest_get_slot, ":source_fac", "qst_oath_of_vengeance", 4),
	(quest_get_slot, ":hero", "qst_oath_of_vengeance", 5),
	(store_current_day, ":day"), 
	(val_sub, ":day", 5), #checks start after 5 days under oath
	(gt, ":day", ":start_day"),
	
	(assign,":count", 0), #count current killcount for target faction
	(try_for_range, ":ptemplate", "pt_gondor_scouts", "pt_kingdom_hero_party"),
		(spawn_around_party,"p_main_party",":ptemplate"),
		(store_faction_of_party,":fac", reg0),
		(remove_party, reg0),
		(eq, ":fac", ":target"),
		(store_num_parties_destroyed_by_player, ":n", ":ptemplate"),
		(val_add,":count",":n"),
	(try_end),
	(val_sub, ":count", 3), # need to kill at least 3 target faction parties to succeed

	(try_begin),
		(faction_slot_eq, ":target", slot_faction_state, sfs_active), # CC: Faction must be alive to fail quest, otherwise you suceed.
		(neg|ge, ":count", ":start_killcount"),
		(call_script, "script_fail_quest", "qst_oath_of_vengeance"),
		(set_show_messages, 0),
		(call_script, "script_end_quest", "qst_oath_of_vengeance"),
		(set_show_messages, 1),
		#(str_store_faction_name, s1, ":source_fac"),
		(str_store_troop_name, s1, ":hero"),
		(display_message, "@You have failed to fulfill your oath of vengeance for {s1}'s heroic death!", color_bad_news),
		(call_script, "script_cf_gain_trait_oathbreaker"),
	(else_try),
		(faction_slot_eq|neg|this_or_next, ":target", slot_faction_state, sfs_active), # CC: If faction is not active, you have completed the quest.
		(ge, ":count", ":start_killcount"),
		(call_script, "script_succeed_quest", "qst_oath_of_vengeance"),
		(set_show_messages, 0),
		(call_script, "script_end_quest", "qst_oath_of_vengeance"),
		(set_show_messages, 1),
		(call_script, "script_cf_gain_trait_oathkeeper"),
		(val_sub, ":start_killcount", 3),
		(val_sub, ":count", ":start_killcount"),
		(store_mul, reg1, ":count", 4),
		#(str_store_faction_name, s1, ":source_fac"),
		(str_store_troop_name, s1, ":hero"),
		(display_message, "@You have fulfilled your oath of vengeance for {s1}'s heroic death!", color_good_news),
		(call_script, "script_increase_rank", ":source_fac", reg1),
	(try_end),
]),

# check for mutiny when orcs in party
(2, 0, 2, [
	(neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
	(val_sub, "$mutiny_counter",2),
	(le, "$mutiny_counter",0),
	(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
	(assign, ":orcs", 0),
	(try_for_range, ":stack_no", 0, ":num_stacks"), # count number of orcs and max level
		(party_stack_get_troop_id, ":stack_troop", "p_main_party" ,":stack_no"),
		(neg|troop_is_hero, ":stack_troop"),
		(troop_get_type, reg1, ":stack_troop"),
		(eq, reg1, tf_orc),
		(party_stack_get_size, reg1, "p_main_party",":stack_no"),
		(val_add, ":orcs", reg1),
	(try_end),
	(store_skill_level, reg1, "skl_persuasion", "trp_player"), # persuasion neutralizes 5 orcs per level
	(val_mul, reg1, 5),
	(val_sub, ":orcs", reg1),
	(troop_get_type, reg1, "trp_player"),
	(try_begin),(eq, reg1, tf_orc),(val_sub, ":orcs", 10),(try_end), # player being an orc himself neutralizes 10 orcs
	(val_max, ":orcs", 1),
	(party_get_num_companions, reg1, "p_main_party"),
	(gt, reg1, 15), # for big enough party
	(val_div, reg1, ":orcs"),
	(lt, reg1, 2), # more than 50% of "adjusted orcs" in party?
	(store_random_in_range, reg1, 0, 10),(lt, reg1, 2), #20% mutiny chance
	],[
	(assign, "$mutiny_counter",108), # 4.3 days between uprisings
	(try_begin),
		(eq,"$mutiny_stage",0),
	    (jump_to_menu,"mnu_premutiny"), #fire up warning dialog
	(else_try),
		(assign,"$mutiny_stage",2), #fire up pre_fight dialog
	    (jump_to_menu,"mnu_mutiny"),
	(try_end),
   ]),
   
	# CC: Ambushes
	(10, 0, 0, [],[
		(try_begin),
			(party_get_attached_to, ":attached_to_party", "p_main_party"),
         		(neg|is_between, ":attached_to_party", centers_begin, centers_end),
			(eq|this_or_next, "$current_player_region", region_misty_mountains),
			(eq|this_or_next, "$current_player_region", region_grey_mountains),
			(eq|this_or_next, "$current_player_region", region_n_mirkwood),
			(eq, "$current_player_region", region_s_mirkwood),
			(assign, ":continue", 1),
			(try_for_range, ":party_id", centers_begin, centers_end), # Don't allow ambushes if player is close to a center.
				(eq, ":continue", 1),
				(party_is_active, ":party_id"), # Skip non-existant adv. camps.
            			(store_distance_to_party_from_party, ":dist", ":party_id", "p_main_party"),
				(lt, ":dist", 300),
				(assign, ":continue", 0),
			(try_end),
			(eq, ":continue", 1),
			(assign, ":ambush_chance", 90),
			(party_get_num_companions, reg1, "p_main_party"),
			(try_begin),
				(lt, reg1, 8),
				(val_sub, ":ambush_chance", 50),
			(else_try),
				(gt, reg1, 35),
				(val_sub, ":ambush_chance", 70),
			(try_end),
			(call_script, "script_get_max_skill_of_player_party", "skl_spotting"),
			(try_begin),
				(gt, reg0, 4),
				(store_sub, reg2, reg0, 4),
				(val_mul, reg2, 10),
				(val_sub, ":ambush_chance", reg2), # -60% at max
			(try_end),
			(try_begin),
				(store_random_in_range, ":rnd", 1, 101),
				(lt, ":rnd", ":ambush_chance"),
				(jump_to_menu, "mnu_animal_ambush"),
			(try_end),
		(try_end),		
	]),


# save game compartibility triggers. replace those if you add new ones
   (999, 0, ti_once, [],[]),
   (999, 0, ti_once, [],[]),
   (999, 0, ti_once, [],[]),
   (999, 0, ti_once, [],[]),
   (999, 0, ti_once, [],[]),
   (999, 0, ti_once, [],[]),
   (999, 0, ti_once, [],[]),
   (999, 0, ti_once, [],[]),
   (999, 0, ti_once, [],[]),

]
