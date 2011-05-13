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

#  (0.0, 0, ti_once, [(map_free,0)], [(call_script,"script_tld_war_system_init")] ),
#  (1, 0, 0.0, [(key_is_down,key_h)],[(call_script,"script_tld_war_system_debug")] ),  
#  (1, 0, 0.0, [(key_is_down,key_r)],[(call_script,"script_tld_war_system_init")] ),
#  
#  (1.0, 0, ti_once, [(map_free,0)], [(start_map_conversation,"trp_guide")]),

# Refresh Smiths
  (0.0, 0, 24.0, [], 
 [(set_merchandise_modifier_quality,150),
  (try_for_range,":cur_merchant",weapon_merchants_begin,weapon_merchants_end),
    (reset_item_probabilities,100),     
    (troop_clear_inventory,":cur_merchant"),
	(store_troop_faction,":faction",":cur_merchant" ),
    (call_script,"script_get_faction_mask",":faction"),(assign,":faction_mask",reg30),          
    (troop_get_slot,":subfaction",":cur_merchant", slot_troop_subfaction),
    (call_script,"script_get_faction_mask",":subfaction"),(assign,":subfaction_mask",reg30),          
    (store_add,":last_item_plus_one","itm_ent_body",1),

    (try_for_range,":item","itm_no_item",":last_item_plus_one"), # items with faction != merchant get 0 probability
            (item_get_slot,":item_faction_mask",":item",slot_item_faction),
            (val_and,":item_faction_mask",":faction_mask"),
			(try_begin),
				(eq,":item_faction_mask",0), # faction mismatch
				(set_item_probability_in_merchandise,":item",0),
			(else_try),
				(item_get_slot,":item_subfaction_mask",":item",slot_item_subfaction),
				(store_and,":and_sub_faction",":subfaction_mask",":item_subfaction_mask"), # subfaction mismatch
				(eq,":and_sub_faction",0),
				#(store_or , ":or_sub_faction",":subfaction_mask",":item_subfaction_mask"),
				#(val_and,   ":or_sub_faction",1),
				#(try_begin),
				#	(val_and,  ":or_sub_faction",1), # at last one of the two subfaction is regular (either regular item in special town, or viceversa)
				#	(set_item_probability_in_merchandise,":item",10), #   prob reduced to 10 %
				#(else_try),
					(set_item_probability_in_merchandise,":item",0),  #  prob reduced to 0 %
				#(try_end),
			(try_end),
   (try_end),


	(try_for_range,":itp_type",itp_type_one_handed_wpn, itp_type_pistol),
		(store_add,":slot",":itp_type",slot_troop_shop_horses-1), # itp_types and shop abundance slots in same order 
		(troop_get_slot,":items",":cur_merchant",":slot"), # get item shop abundance
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
  (0.0, 0, 24.0, [], [
    (set_merchandise_modifier_quality,150),
    #(store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),

    #(set_item_probability_in_merchandise,"itm_smoked_fish",400),
    #(troop_add_merchandise,"trp_salt_mine_merchant",itp_type_goods,num_merchandise_goods),
					  
    (try_for_range,":cur_center",towns_begin,towns_end),
        (party_get_slot,":cur_merchant",":cur_center",slot_town_merchant),
        (neq, ":cur_merchant", "trp_no_troop"),
        (reset_item_probabilities,100),     
        (troop_clear_inventory,":cur_merchant"),
        (store_troop_faction,":faction",":cur_merchant"),
        (call_script,"script_get_faction_mask",":faction"),(assign,":faction_mask",reg30),          
        (troop_get_slot,":subfaction",":cur_center", slot_troop_subfaction),
        (call_script,"script_get_faction_mask",":subfaction"),(assign,":subfaction_mask",reg30),          

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

        (try_for_range,":item","itm_sumpter_horse", "itm_dale_pike"),
            (item_get_slot,":item_faction_mask",":item",slot_item_faction),
            (val_and,":item_faction_mask",":faction_mask"),
			(try_begin),
				(eq,":item_faction_mask",0), # faction mismatch
				(set_item_probability_in_merchandise,":item",0),
			(else_try),
				(item_get_slot,":item_subfaction_mask",":item",slot_item_subfaction),
				(store_and,":and_sub_faction",":subfaction_mask",":item_subfaction_mask"), # subfaction mismatch
				(eq,":and_sub_faction",0),
				#(try_begin),
				#	(val_or,   ":item_subfaction_mask",1),
				#	(eq,"item_subfaction_mask",1), # regular object
				#	(set_item_probability_in_merchandise,":item",10), #   prob reduced to 10 %
				#(else_try),
					(set_item_probability_in_merchandise,":item",0),  #  prob reduced to 0 %
				#(try_end),
			(try_end),
        (try_end),
    # horses inventory
        (troop_get_slot,":items",":cur_merchant",slot_troop_shop_horses),
        (try_begin),
            (gt,":items",0),
            (troop_add_merchandise,":cur_merchant",itp_type_horse,":items"),
        (try_end),
    
    # Add trade goods to merchant inventories
        (reset_item_probabilities,100),
        (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
#            (store_add, ":cur_production_slot", ":cur_goods", ":item_to_production_slot"),
            # (store_add, ":cur_price_slot", ":cur_goods", ":item_to_price_slot"),
#            (party_get_slot, ":cur_production", ":cur_center", ":cur_production_slot"),
            # (party_get_slot, ":cur_price", ":cur_center", ":cur_price_slot"),
                    
            # (assign, ":cur_probability", 100),
            # (val_mul, ":cur_probability", average_price_factor),(val_div, ":cur_probability", ":cur_price"),
            # (val_mul, ":cur_probability", average_price_factor),(val_div, ":cur_probability", ":cur_price"),
            # (val_mul, ":cur_probability", average_price_factor),(val_div, ":cur_probability", ":cur_price"),
            # (val_mul, ":cur_probability", average_price_factor),(val_div, ":cur_probability", ":cur_price"),
            
            #MV: no non-edible trade goods and some factional food
            (try_begin),
              (is_between, ":cur_goods", food_begin, food_end),
              (this_or_next|eq, ":is_orc_faction", 1),
              (neq, ":cur_goods", "itm_human_meat"),
              # (this_or_next|eq, ":is_elf_faction", 1),
              # (neq, ":cur_goods", "itm_lembas"),
              
              (assign, ":quest_prevents", 0),
              (try_begin), # don't allow this food to generate if the quest says there is a shortage
                (check_quest_active, "qst_deliver_food"),
                (quest_slot_eq, "qst_deliver_food", slot_quest_target_center, ":cur_center"),
                (quest_slot_eq, "qst_deliver_food", slot_quest_target_item, ":cur_goods"),
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

#MV: removed manhunters
  # (5.7, 0, 0.0, [(store_num_parties_created,reg(3),"pt_manhunters"),
                 # (lt,reg(3),num_max_zendar_manhunters),
                 # (store_num_parties_of_template, reg(2), "pt_manhunters"), (lt,reg(2),3)],
                # [(set_spawn_radius,1),(spawn_around_party,"p_zendar","pt_manhunters")]),

  (2.0, 0, 0, [(store_random_party_of_template, reg(2), "pt_prisoner_train_party"),(party_is_in_any_town,reg(2)),],
              [(store_faction_of_party, ":faction_no", reg(2)),
               (call_script,"script_cf_select_random_walled_center_with_faction", ":faction_no", -1),
               (party_set_ai_behavior,reg(2),ai_bhvr_travel_to_party),
               (party_set_ai_object,reg(2),reg0),
               (party_set_flags, reg(2), pf_default_behavior, 0),
              ]),

##  (2.0, 0, 0, [(store_random_party_of_template, reg(2), "pt_kingdom_caravan_party"),
##               (party_is_in_any_town,reg(2)),
##               ],
##              [(store_faction_of_party, ":faction_no", reg(2)),
##               (call_script,"script_cf_select_random_town_with_faction", ":faction_no"),
##               (party_set_ai_behavior,reg(2),ai_bhvr_travel_to_party),
##               (party_set_ai_object,reg(2),reg0),
##               (party_set_flags, reg(2), pf_default_behavior, 0),
##            ]),
  
#  (4.0, 0, 0.0, [(eq, "$caravan_escort_state", 1), #cancel caravan_escort_state if caravan leaves the destination
#                 (get_party_ai_object,reg(1),"$caravan_escort_party_id"),
#                 (neq,reg(1),"$caravan_escort_destination_town"),
#                ],
#                     [(assign,"$caravan_escort_state",0),
#                      (add_xp_as_reward,100),
#                      ]),

#  (1.5, 0, 0, [(store_random_party_of_template, reg(2), "pt_messenger_party"),
#               (party_is_in_any_town,reg(2)),
#               ],
#   [(store_faction_of_party, ":faction_no", reg(2)),
#    (call_script,"script_cf_select_random_walled_center_with_faction", ":faction_no", -1),
#    (party_set_ai_behavior,reg(2),ai_bhvr_travel_to_party),
#    (party_set_ai_object,reg(2),reg0),
#    (party_set_flags, reg(2), pf_default_behavior, 0),
#    ]),
#  

#Kingdom Parties
  (24.0, 0, 0.0, [],
   [
        #############################################
        # TLD Parties spawn (foxyman)
        #
      (try_for_range, ":center", centers_begin, centers_end),
        (party_is_active, ":center"),
        
        (party_get_slot, ":center_scouts", ":center", slot_center_spawn_scouts),
        (party_get_slot, ":center_raiders", ":center", slot_center_spawn_raiders),
        (party_get_slot, ":center_patrol", ":center", slot_center_spawn_patrol),
        (party_get_slot, ":center_caravan", ":center", slot_center_spawn_caravan),
        (try_begin),
            (store_faction_of_party, ":faction_no", ":center"),
            (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active), # faction lives
            (party_get_slot, ":center_theater", ":center", slot_center_theater),
            (faction_slot_eq, ":faction_no", slot_faction_active_theater, ":center_theater"), #center in faction's active theater
            
            (faction_get_slot, ":strength", ":faction_no", slot_faction_strength),
            (val_clamp, ":strength", 0, 7001), # keep spawning chance and max limit within reason
			(store_div, ":chance_modifier", ":strength", 100),
            (val_sub, ":chance_modifier", 35), # -5 for str. 3000, 0 for 3500, +5 for 4000,... +35 for 7000 
            
            (try_begin),
                (gt, ":center_scouts", 0),
                # (store_random_in_range, ":rand", 0, int(15000/ws_scout_freq_multiplier)), # 0-4285
                # (le, ":rand", ":strength"), # 81% for fac.str. 3500
                (store_add, ":chance", ws_scout_chance, ":chance_modifier"),
                (store_random_in_range, ":rand", 0, 100),
                (lt, ":rand", ":chance"), # 60% for fac.str. 3500
                (store_mul, ":limit", ":strength", ws_scout_limit_multiplier*1000),
                (val_div, ":limit", 3500*1000), #14 for fac.str. 3500; 28 for 7000
                (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", spt_scout),
                (lt, reg0, ":limit"),
                (set_spawn_radius, 1),
                (spawn_around_party, ":center", ":center_scouts"),
                (assign, ":scout_party", reg0),
#                (display_message, "@DEBUG: Party spawn: {reg0}", 0xFF00fd33),
                (party_set_slot, ":scout_party", slot_party_type, spt_scout),
                (party_set_slot, ":scout_party", slot_party_home_center, ":center"),
				(party_set_slot, ":scout_party", slot_party_victory_value, ws_scout_vp), # victory points for party kill
                (party_set_faction, ":scout_party", ":faction_no"),
                (call_script, "script_find_closest_random_enemy_center_from_center", ":center"),
                (try_begin),
                    (neq, reg0, -1),
                    (assign, ":enemy_center", reg0),
                    (party_get_position, pos1, ":enemy_center"),
                    (party_get_position, pos2, ":center"),
                    (call_script, "script_calc_mid_point"),
                (else_try),
                    (party_get_position, pos1, ":center"),
                (try_end),
                (party_set_slot, ":scout_party", slot_party_ai_object, ":enemy_center"),
                (party_set_slot, ":scout_party", slot_party_ai_state, spai_undefined),
                (party_set_ai_behavior, ":scout_party", ai_bhvr_patrol_location),
                (party_set_ai_target_position, ":scout_party", pos1),
                (party_set_ai_patrol_radius, ":scout_party", 30),
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
                (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", spt_raider),
                (lt, reg0, ":limit"),
                (set_spawn_radius, 1),
                (spawn_around_party, ":center", ":center_raiders"),
                (assign, ":raider_party", reg0),
                (party_set_slot, ":raider_party", slot_party_home_center, ":center"),
                (party_set_faction, ":raider_party", ":faction_no"),
                (party_set_ai_behavior, ":raider_party", ai_bhvr_patrol_party),
                (party_set_ai_patrol_radius, ":raider_party", 30),
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
                (party_set_ai_patrol_radius, ":patrol_party", 30),
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
            (try_end),             
        (try_end),
      (try_end),
        #
        # 
        #############################################
    ]
  ),

   (0, 0, ti_once,
   [ #(entering_town,":party"),
     (neg|eq,"$ambient_faction","$players_kingdom"), ],
   [
		(str_store_faction_name, s11, "$ambient_faction"),
		(str_store_faction_name, s10, "$players_kingdom"),
		(dialog_box,"@When dealing with people in {s11}, remember that they do not know you and they don't necessarily acknowledge the merits you've earned in {s10}.                                                                                                                (the Resource Pts. which you can dispose of among people from {s11} are not the ones you earned in {s10}, but the ones you will earn in {s11} -- see also the Report screen)","@Info"),
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

# Incriminate Loyal Advisor quest
  # (0.2, 0.0, 0.0,
   # [
       # (check_quest_active, "qst_incriminate_loyal_commander"),
       # (neg|check_quest_concluded, "qst_incriminate_loyal_commander"),
       # (quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_current_state, 2),
       # (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
       # (quest_get_slot, ":quest_target_party", "qst_incriminate_loyal_commander", slot_quest_target_party),
       # (try_begin),
         # (neg|party_is_active, ":quest_target_party"),
         # (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 3),
         # (call_script, "script_fail_quest", "qst_incriminate_loyal_commander"),
       # (else_try),
         # (party_is_in_town, ":quest_target_party", ":quest_target_center"),
         # (remove_party, ":quest_target_party"),
         # (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 3),
         # (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
         # (assign, ":num_available_factions", 0),
         # (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
           # (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
           # (neq, ":faction_no", "fac_player_supporters_faction"),
           # (neg|quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_target_faction, ":faction_no"),
           # (val_add, ":num_available_factions", 1),
         # (try_end),
         # (try_begin),
           # (gt, ":num_available_factions", 0),
           # (store_random_in_range, ":random_faction", 0, ":num_available_factions"),
           # (assign, ":target_faction", -1),
           # (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
             # (eq, ":target_faction", -1),
             # (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
             # (neq, ":faction_no", "fac_player_supporters_faction"),
             # (neg|quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_target_faction, ":faction_no"),
             # (val_sub, ":random_faction", 1),
             # (lt, ":random_faction", 0),
             # (assign, ":target_faction", ":faction_no"),
           # (try_end),
         # (try_end),
         # (try_begin),
           # (gt, ":target_faction", 0),
           # (call_script, "script_change_troop_faction", ":quest_object_troop", ":target_faction"),
         # (else_try),
           # (call_script, "script_change_troop_faction", ":quest_object_troop", "fac_outlaws"),
         # (try_end),
         # (call_script, "script_succeed_quest", "qst_incriminate_loyal_commander"),
       # (try_end),
    # ],
   # []
   # ),

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
### Defend Nobles Against Peasants quest
##  (0.2, 0.0, 0.0,
##   [
##       (check_quest_active, "qst_defend_nobles_against_peasants"),
##       (neg|check_quest_succeeded, "qst_defend_nobles_against_peasants"),
##       (neg|check_quest_failed, "qst_defend_nobles_against_peasants"),
##       (quest_get_slot, ":quest_target_center", "qst_defend_nobles_against_peasants", slot_quest_target_center),
##       (assign, ":num_active_parties", 0),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_1", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_1"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_1", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_1"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_1"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_2", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_2"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_2", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_2"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_2"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_3", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_3"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_3", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_3"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_3"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_4", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_4"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_4", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_4"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_4"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_5", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_5"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_5", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_5"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_5"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_6", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_6"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_6", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_6"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_6"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_7", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_7"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_7", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_7"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_7"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_8", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_8"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_8", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_8"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_8"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (eq, ":num_active_parties", 0),
##       (try_begin),
##         (store_div, ":limit", "$qst_defend_nobles_against_peasants_num_nobles_to_save", 2),
##         (ge, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":limit"),
##         (call_script, "script_succeed_quest", "qst_defend_nobles_against_peasants"),
##       (else_try),
##         (call_script, "script_fail_quest", "qst_defend_nobles_against_peasants"),
##       (try_end),
##    ],
##   []
##   ),
### Capture Conspirators quest
##  (0.15, 0.0, 0.0,
##   [
##       (check_quest_active, "qst_capture_conspirators"),
##       (neg|check_quest_succeeded, "qst_capture_conspirators"),
##       (neg|check_quest_failed, "qst_capture_conspirators"),
##       (quest_get_slot, ":quest_target_center", "qst_capture_conspirators", slot_quest_target_center),
##       (quest_get_slot, ":faction_no", "qst_capture_conspirators", slot_quest_target_faction),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_num_parties_to_spawn", "$qst_capture_conspirators_num_parties_spawned"),
##         (store_random_in_range, ":random_no", 0, 100),
##         (lt, ":random_no", 20),
##         (set_spawn_radius, 3),
##         (spawn_around_party,":quest_target_center","pt_conspirator"),
##         (val_add, "$qst_capture_conspirators_num_parties_spawned", 1),
##         (party_get_num_companions, ":num_companions", reg0),
##         (val_add, "$qst_capture_conspirators_num_troops_to_capture", ":num_companions"),
##         (party_set_ai_behavior, reg0, ai_bhvr_travel_to_party),
##         (party_set_ai_object, reg0, "$qst_capture_conspirators_party_1"),
##         (party_set_flags, reg0, pf_default_behavior, 0),
##         (try_begin),
##           (le, "$qst_capture_conspirators_party_2", 0),
##           (assign, "$qst_capture_conspirators_party_2", reg0),
##         (else_try),
##           (le, "$qst_capture_conspirators_party_3", 0),
##           (assign, "$qst_capture_conspirators_party_3", reg0),
##         (else_try),
##           (le, "$qst_capture_conspirators_party_4", 0),
##           (assign, "$qst_capture_conspirators_party_4", reg0),
##         (else_try),
##           (le, "$qst_capture_conspirators_party_5", 0),
##           (assign, "$qst_capture_conspirators_party_5", reg0),
##         (else_try),
##           (le, "$qst_capture_conspirators_party_6", 0),
##           (assign, "$qst_capture_conspirators_party_6", reg0),
##         (else_try),
##           (le, "$qst_capture_conspirators_party_7", 0),
##           (assign, "$qst_capture_conspirators_party_7", reg0),
##         (try_end),
##       (try_end),
##
##       (assign, ":num_active_parties", 0),
##
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_1", 0),
##         (party_is_active, "$qst_capture_conspirators_party_1"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_1"),
##           (remove_party, "$qst_capture_conspirators_party_1"),
##         (else_try),
##           (party_get_num_attached_parties, ":num_attachments", "$qst_capture_conspirators_party_1"),
##           (gt, ":num_attachments", 0),
##           (assign, ":leave_meeting", 0),
##           (try_begin),
##             (store_sub, ":required_attachments", "$qst_capture_conspirators_num_parties_to_spawn", 1),
##             (eq, ":num_attachments", ":required_attachments"),
##             (val_add, "$qst_capture_conspirators_leave_meeting_counter", 1),
##             (ge, "$qst_capture_conspirators_leave_meeting_counter", 15),
##             (assign, ":leave_meeting", 1),
##           (try_end),
##           (try_begin),
##             (eq, "$qst_capture_conspirators_num_parties_to_spawn", "$qst_capture_conspirators_num_parties_spawned"),
##             (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_capture_conspirators_party_1"),
##             (assign, ":min_distance", 3),
##             (try_begin),
##               (is_currently_night),
##               (assign, ":min_distance", 2),
##             (try_end),
##             (lt, ":cur_distance", ":min_distance"),
##             (assign, "$qst_capture_conspirators_leave_meeting_counter", 15),
##             (assign, ":leave_meeting", 1),
##           (try_end),
##           (eq, ":leave_meeting", 1),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_1", ai_bhvr_travel_to_point),
##           (party_set_flags, "$qst_capture_conspirators_party_1", pf_default_behavior, 0),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_1"),
##           (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##           (party_set_ai_target_position, "$qst_capture_conspirators_party_1", pos2),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_2", 0),
##             (party_detach, "$qst_capture_conspirators_party_2"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_2", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_2", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_2", pos2),
##           (try_end),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_3", 0),
##             (party_detach, "$qst_capture_conspirators_party_3"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_3", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_3", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_3", pos2),
##           (try_end),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_4", 0),
##             (party_detach, "$qst_capture_conspirators_party_4"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_4", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_4", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_4", pos2),
##           (try_end),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_5", 0),
##             (party_detach, "$qst_capture_conspirators_party_5"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_5", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_5", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_5", pos2),
##           (try_end),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_6", 0),
##             (party_detach, "$qst_capture_conspirators_party_6"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_6", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_6", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_6", pos2),
##           (try_end),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_7", 0),
##             (party_detach, "$qst_capture_conspirators_party_7"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_7", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_7", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_7", pos2),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_1"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_1"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_1"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_1", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_1", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_1", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_1", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_2", 0),
##         (party_is_active, "$qst_capture_conspirators_party_2"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_2"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_2", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_2"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_2"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_2", ai_bhvr_hold),
##             (party_attach_to_party, "$qst_capture_conspirators_party_2", "$qst_capture_conspirators_party_1"),
##             (party_set_flags, "$qst_capture_conspirators_party_2", pf_default_behavior, 0),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_2"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_2"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_2"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_2", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_2", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_2", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_2", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_3", 0),
##         (party_is_active, "$qst_capture_conspirators_party_3"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_3"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_3", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_3"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_3"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_3", ai_bhvr_hold),
##             (party_attach_to_party, "$qst_capture_conspirators_party_3", "$qst_capture_conspirators_party_1"),
##             (party_set_flags, "$qst_capture_conspirators_party_3", pf_default_behavior, 0),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_3"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_3"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_3"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_3", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_3", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_3", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_3", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_4", 0),
##         (party_is_active, "$qst_capture_conspirators_party_4"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_4"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_4", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_4"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_4"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_4", ai_bhvr_hold),
##             (party_set_flags, "$qst_capture_conspirators_party_4", pf_default_behavior, 0),
##             (party_attach_to_party, "$qst_capture_conspirators_party_4", "$qst_capture_conspirators_party_1"),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_4"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_4"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_4"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_4", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_4", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_4", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_4", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_5", 0),
##         (party_is_active, "$qst_capture_conspirators_party_5"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_5"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_5", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_5"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_5"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_5", ai_bhvr_hold),
##             (party_set_flags, "$qst_capture_conspirators_party_5", pf_default_behavior, 0),
##             (party_attach_to_party, "$qst_capture_conspirators_party_5", "$qst_capture_conspirators_party_1"),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_5"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_5"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_5"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_5", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_5", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_5", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_5", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_6", 0),
##         (party_is_active, "$qst_capture_conspirators_party_6"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_6"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_6", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_6"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_6"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_6", ai_bhvr_hold),
##             (party_set_flags, "$qst_capture_conspirators_party_6", pf_default_behavior, 0),
##             (party_attach_to_party, "$qst_capture_conspirators_party_6", "$qst_capture_conspirators_party_1"),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_6"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_6"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_6"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_6", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_6", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_6", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_6", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_7", 0),
##         (party_is_active, "$qst_capture_conspirators_party_7"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_7"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_7", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_7"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_7"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_7", ai_bhvr_hold),
##             (party_set_flags, "$qst_capture_conspirators_party_7", pf_default_behavior, 0),
##             (party_attach_to_party, "$qst_capture_conspirators_party_7", "$qst_capture_conspirators_party_1"),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_7"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_7"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_7"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_7", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_7", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_7", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_7", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##
##       (eq, ":num_active_parties", 0),
##       (party_count_prisoners_of_type, ":count_captured_conspirators", "p_main_party", "trp_conspirator"),
##       (party_count_prisoners_of_type, ":count_captured_conspirator_leaders", "p_main_party", "trp_conspirator_leader"),
##       (val_add, ":count_captured_conspirators", ":count_captured_conspirator_leaders"),
##       (try_begin),
##         (store_div, ":limit", "$qst_capture_conspirators_num_troops_to_capture", 2),
##         (gt, ":count_captured_conspirators", ":limit"),
##         (call_script, "script_succeed_quest", "qst_capture_conspirators"),
##       (else_try),
##         (call_script, "script_fail_quest", "qst_capture_conspirators"),
##       (try_end),
##    ],
##   []
##   ),
# Follow Spy quest
  (0.5, 0.0, 0.0,
   [
       (check_quest_active, "qst_follow_spy"),
       (eq, "$qst_follow_spy_no_active_parties", 0),
       (quest_get_slot, ":quest_giver_center", "qst_follow_spy", slot_quest_giver_center),
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
       (try_end),
    ],
   []
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
  (24.0 * 7, 0.0, 0.0,
   [],
   [
       (val_mul,"$debt_to_merchants_guild",101),
       (val_div,"$debt_to_merchants_guild",100)
    ]
   ),
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


#Rebellion changes begin
#move 

  # (0, 0, 24 * 14,
   # [
        # (try_for_range, ":pretender", pretenders_begin, pretenders_end),
          # (troop_set_slot, ":pretender", slot_troop_cur_center, 0),
          # (neq, ":pretender", "$supported_pretender"),
          # (troop_get_slot, ":target_faction", ":pretender", slot_troop_original_faction),
          # (faction_slot_eq, ":target_faction", slot_faction_state, sfs_active),
          # (faction_slot_eq, ":target_faction", slot_faction_has_rebellion_chance, 1),
          # (neg|troop_slot_eq, ":pretender", slot_troop_occupation, slto_kingdom_hero),

          # (try_for_range, ":unused", 0, 30),
            # (troop_slot_eq, ":pretender", slot_troop_cur_center, 0),
            # (store_random_in_range, ":town", towns_begin, towns_end),
            # (store_faction_of_party, ":town_faction", ":town"),
            # (store_relation, ":relation", ":town_faction", ":target_faction"),
            # (le, ":relation", 0), #fail if nothing qualifies
           
            # (troop_set_slot, ":pretender", slot_troop_cur_center, ":town"),
            # (try_begin),
              # (eq, "$cheat_mode", 1),
              # (str_store_troop_name, 4, ":pretender"),
              # (str_store_party_name, 5, ":town"),
              # (display_message, "@{s4} is in {s5}"),
            # (try_end),
          # (try_end),

        # (try_end), 
       # ],
# []
# ),
#Rebellion changes end

#NPC system changes begin
#Move unemployed NPCs around taverns
   # (24 * 15, 0, 0,
   # [
    #(call_script, "script_update_companion_candidates_in_taverns"),
    # ],
   # []
   # ),

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
    (0, 0, ti_once, [
        ], [
### TLD variables initial assignment, GA		
		(assign, "$tld_war_began",0),
		#_(assign, "$g_center_to_give_to_player", "p_zendar"),
        (assign, "$prev_day", 1),

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
    (1, 0, ti_once, 
	   [(player_has_item,"itm_ent_water"),
	   ],[
		(dialog_box,"@You came into a possession of a strange, oversized bowl of fresh-looking water. It smells a little like musk.","@Obtained: Ent water."),
		(play_sound,"snd_quest_completed"),
        ]
    ),

#TLD magic items stuff(mtarini)
	(12, 12, ti_once, 
	   [
	     (eq,"$g_ent_water_taking_effect",1),
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
        ]
    ),
	
# TLD War beginning condition (player level = 2 at the moment), GA
    (1, 0, 0, 
	   [(eq,"$tld_war_began",0),
	    (store_character_level,":level","trp_player"),
		(ge,":level",tld_player_level_to_begin_war),
	   ],[
		(assign, "$tld_war_began",1),
		(dialog_box,"@The dark shadow finally broke into a storm, and evil hordes started their march on the free people of Middle Earth. Mordor against Gondor in the South, Isengard agains Rohan in the West, Dol Guldur against the Elves.. Even in the far North there is a war of its own.","@The War has started!"),
		(play_sound,"snd_evil_horn"),
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
        ]
    ),
	
  (0.5, 0, 0, [],[#(gt,"$g_fangorn_rope_pulled",-100)],[
	(call_script,"script_party_is_in_fangorn","p_main_party"),
	(assign,":inside_fangorn",reg0),
	(try_begin),
	  (eq, "$g_player_is_captive", 0),
	  (eq,":inside_fangorn",1),
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
  ] ),

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
                (display_message, "@Your companions' morale has risen from hatred.", 0xffaa3333),
                (val_add, ":morale", 10),
            (else_try), # base morale low, drop in fear
                (display_message, "@Your companions' morale has dropped from fear.", 0xffaa3333),
                (val_sub, ":morale", 10),
            (try_end),
            (party_set_morale, "p_main_party", ":morale"),
        (try_end),        
        ]
    ),

### war start movie sequence  
 # (0.1, 0.04, ti_once, [(map_free,0),],[#(key_clicked,key_k)],[
 #   (party_get_position,pos33,"p_main_party"),
#	(display_message,"@The War has started!"),
#	(set_camera_follow_party,"p_town_isengard"), (assign,"$warmovie",1),
#  ]),
#  (0, 0.04, ti_once, [(eq,"$warmovie",1)],[
#	(display_message,"@Rhun riders attack in the north"),
#	(set_camera_follow_party,"p_town_erebor"), (assign,"$warmovie",2),
#  ]),  
#  (0, 0.04, ti_once, [(eq,"$warmovie",2)],[
#	(display_message,"@Fierce desert warriors of Khand in the center"),
#	(set_camera_follow_party,"p_town_khand_camp"), (assign,"$warmovie",3),
#  ]),  
#  (0, 0.04, ti_once, [(eq,"$warmovie",3),(display_message,"@Go now, and help free people of MiddleEarth"),],[
#	(display_message,"@Because time is running out!"),
#	(set_camera_follow_party,"p_town_khand_camp"), (assign,"$warmovie",4),
#  ]),
#  (0, 0.04, ti_once, [(eq,"$warmovie",4),(display_message,"@Go now, and help free people of MiddleEarth"),],[
#	(display_message,"@Because time is running out!"),
#	(set_camera_follow_party,"p_main_party"), (assign,"$warmovie",5),
#  ]), 

####################################
# TLD faction ranks
#
# Detect new rank
  # (12, 0, 0, [], [
    # (troop_get_slot, ":status", "trp_player", slot_troop_faction_status),
    # (try_begin),
    # ]+concatenate_scripts([
        # [
        # (store_add, ":kd", kd, kingdoms_begin),
        # (eq, ":kd", "$players_kingdom"),
        # (try_begin),
        # ]+concatenate_scripts([
            # [
            # (ge, ":status", tld_faction_ranks[kd][rnk][0]),
            # (troop_get_slot, ":ofc_pos", "trp_player", slot_troop_faction_rank),
            # (store_and, ":rank", ":ofc_pos", stfr_rank_mask),
            # (val_div, ":rank", stfr_rank_unit),
            # (assign, ":continue", 0),
            # (try_begin),
                # (gt, ":rank", rnk),
                # (str_store_string, s11, "str_promote"),
# #            (else_try),
# #                (lt, ":rank", rnk),
# #                (str_store_string, s11, "str_demote"),
            # (else_try),
                # (assign, ":continue", 1),
            # (try_end),
            # (try_begin),
                # (eq, ":continue", 0),
                # (assign, "$tld_new_rank", rnk),
                # (jump_to_menu, "mnu_faction_rank_change"),
            # (try_end),
        # (else_try),
            # ] for rnk in range(len(tld_faction_ranks[kd]))
        # ])+[
        # (try_end),
    # (else_try),
        # ] for kd in range(len(tld_faction_ranks))
    # ])+[
    # (try_end),
  # ]),

#
# TLD faction ranks end
###################################
# starting quest WIP
# (1, 0, ti_once, [(map_free,0)],[(jump_to_menu,"mnu_starting_quest_good"),]
# ),

]
