from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *

from module_constants import *
from module_info import wb_compile_switch as is_a_wb_trigger

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
      (try_for_range,":cur_merchant", weapon_merchants_begin, weapon_merchants_end),
        
        #swy-- for every single weapon merchant, blank out the inventory, reset any previous probability tweak to their defaults...
        #      edit: looks like reset_item_probabilities doesn't accept any arguments at all?!,
        #            just resets them to their default value specified in module_items, maybe misdocumented!
        (reset_item_probabilities, 100),
        (troop_clear_inventory,":cur_merchant"),
        
        
        #swy-- in WB we've to store the number of each available item type into a slot array, here we reset them to zero for every merchant...
        ] + (is_a_wb_trigger==1 and [
          
          (try_for_range, ":aval_slot", slot_troop_shop_aval_itp_counter_base + itp_type_one_handed_wpn,
            slot_troop_shop_aval_itp_counter_base + itp_type_hand_armor + 1),
            #swy-- reset the curr itp array member slot to zero...
            (troop_set_slot, "trp_skill2item_type", ":aval_slot", 0),
          (try_end),
          
        ] or []) + [
        
        #swy-- get his faction and subfaction mask, if any, used to compare against items' faction slot...
        (store_troop_faction,":faction",":cur_merchant"),
        
        (faction_get_slot, ":faction_mask", ":faction",      slot_faction_mask),
        (  troop_get_slot, ":subfaction",   ":cur_merchant", slot_troop_subfaction),
        
        
        #swy-- get the latest item, add one because that's how the game loops work...
        (store_add,":last_item_plus_one", "itm_ent_body", 1),
        
        # Add Center Relations modifier to Item Quality in Smiths
        (assign, ":base_chance", 50),
        (store_troop_faction, ":smith_faction", ":cur_merchant"),
        (assign, ":smith_found", 0),
        (try_for_range, ":center_list", centers_begin, centers_end),
          (eq, ":smith_found", 0),
          (store_faction_of_party, ":center_faction", ":center_list"),
          (eq, ":center_faction", ":smith_faction"),
          (party_slot_eq, ":center_list", slot_town_weaponsmith, ":cur_merchant"),
          (assign, ":smith_found", 1),
          (party_get_slot, ":center_relation", ":center_list", slot_center_player_relation),
        (try_end),

          (call_script, "script_get_faction_rank", ":faction"),
          (assign, ":rank", reg0),
          (store_mul, ":rank_modifier", ":rank", 5),
          (party_get_skill_level, ":player_party_trading", "p_main_party", "skl_trade"),
          (store_mul, ":trading_modifier", ":player_party_trading", 10),
          
          (store_add, ":quality_modifier", ":center_relation", ":rank_modifier"),
          (val_add, ":quality_modifier", ":trading_modifier"),         
          (val_div, ":quality_modifier", 3),
          (val_add, ":quality_modifier", ":base_chance"),
          (set_merchandise_modifier_quality, ":quality_modifier"), #new formula

        #swy-- for every item in the list, check if matches the seller's
        #      faction + subfaction and add it to the probability list if so...
        (try_for_range,":item","itm_no_item",":last_item_plus_one"), # items with faction != merchant get 0 probability
          
          #swy-- find out if the bitwise flag of the item matches the item seller's mask...
          #      [item bitfield slot & seller faction == item faction mask == 1/0]
          (item_get_slot,":item_faction_mask", ":item", slot_item_faction),
          (val_and,":item_faction_mask",":faction_mask"),
          
          (try_begin),
            #swy--> if the item doesn't belong to our faction, bail out early...
            (eq,":item_faction_mask",0),
            (set_item_probability_in_merchandise, ":item", 0),


        ] + (is_a_wb_trigger==1 and [   
          (else_try), #InVain: Rank requirement for items + reduction chance per trading and center relation
            (item_get_abundance, ":rank_req", ":item"),
            (is_between, ":rank_req", 1, 100),
            (val_sub, ":rank_req", 90),
            (store_add, ":rank_bonus", ":trading_modifier", ":center_relation"),
            (val_div, ":rank_bonus", 2),
            (val_sub, ":rank_bonus", 20), 
            (store_random_in_range, ":random", 0, 100),
            (try_begin),
                (lt, ":random", ":rank_bonus"),
                (val_sub, ":rank_req", 1),
            (try_end),
            (lt, ":rank", ":rank_req"),
            (set_item_probability_in_merchandise, ":item", 0),          
          ] or []) + [
          (else_try),
            #swy--> null out its probability if we are part of a subfaction but the item isn't...
            (gt, ":subfaction", 0),
            
            #swy-- if the subfaction mask bit index exists, let's make it, turning it into the proper bitmask with powers of two, emulating a leftshift [1 << mask index]:
            #  e.g: mask index 1 = 2             =>  2
            #       mask index 2 = 2 x 2         =>  4
            #       mask index 3 = 2 x 2 x 2     =>  8
            #       mask index 4 = 2 x 2 x 2 x 2 => 16
            
            # note: there's also a val_lshift operation in WB, but that makes it an opcode longer than a direct power of two. :-)
            (assign, ":subfaction_mask", 1),
            (try_for_range, ":unused", 0, ":subfaction"),
              (val_mul, ":subfaction_mask", 2),  # ":subfaction_mask"=1 if regular faction w/o subs, 2,4,8,16... for subs
            (try_end),
            
            (item_get_slot,":item_subfaction_field", ":item", slot_item_subfaction),
            
            # check for subfaction mismatch, in case they match, jump to the next else like a normal item...
            (store_and,":subfaction_result", ":subfaction_mask", ":item_subfaction_field"),
            (       eq,":subfaction_result", 0),
            # --
            (set_item_probability_in_merchandise, ":item", 0),
            
          (else_try), #Invain: Clean up Gondor regular (0no subfac) stores from subfac gear
            (eq, ":faction", fac_gondor),
            (eq, ":subfaction", 0),
            (item_get_slot,":item_subfaction_field", ":item", slot_item_subfaction),
            (assign, ":subfac_found", 0),
            (try_for_range, ":subfaction_check", 1, 7), #not rangers
                (eq, ":subfac_found", 0),
                (assign, ":subfaction_mask", 1),
                (try_for_range, ":unused", 0, ":subfaction_check"),
                  (val_mul, ":subfaction_mask", 2),  # ":subfaction_mask"=1 if regular faction w/o subs, 2,4,8,16... for subs
                (try_end),
                (eq, ":subfaction_mask", ":item_subfaction_field"),
                (assign, ":subfac_found", 1),                
            (try_end),
            (eq, ":subfac_found", 1),
            (set_item_probability_in_merchandise, ":item", 0),
          (else_try),
            (set_item_probability_in_merchandise, ":item", 100),
            #swy--> half its probability if the item costs more than 1500...
            #(store_item_value,":value",":item"),
            # (try_begin),
              # (gt,":value",1500),
              # (set_item_probability_in_merchandise, ":item", 50),
            # (try_end),
            
            ] + (is_a_wb_trigger==1 and [
              
              (item_get_type, ":cur_item_type", ":item"),
              
              #swy-- hacky fix to get rid of the tools sold by weapon merchants... don't count goods... we were counting stuff which is not going to appear because doesn't have the merchandise/shop flags?!
              (neq,":cur_item_type", itp_type_goods),
              
              #swy-- select the correct array member by using (curr itp + slot base) and calculate the minimum items to add...
              (store_add,":aval_slot", ":cur_item_type", slot_troop_shop_aval_itp_counter_base),
              
              #swy-- increment the curr itp array member slot by one...
              (troop_get_slot,":aval_items", "trp_skill2item_type", ":aval_slot"),(val_add,":aval_items", 1),
              (troop_set_slot,               "trp_skill2item_type", ":aval_slot",          ":aval_items"),
              
            ] or []) + [
            
          (try_end),
          
        (try_end),
        
        #swy-- add items depending on their type... some settlements don't have certain kinds of weapon...
        (try_for_range,":itp_type",itp_type_one_handed_wpn, itp_type_hand_armor + 1),
          (troop_get_slot,":skill","trp_skill2item_type",":itp_type"), #abundance stored in merchant skills values
          (store_skill_level,":items",":skill",":cur_merchant"),
          (try_begin),
            (gt,":items",0),
            
            #Invain: Relation+trade bonus; (rel+trade_skill*10)/100 (up to 2x)
            (store_add, ":abundance_bonus", ":center_relation", ":trading_modifier"), #get score, up to 200
            (store_mul, ":bonus_items", ":items", ":abundance_bonus"),
            (val_div, ":bonus_items", 100),
            (val_add, ":items", ":bonus_items"),
            
            ] + (is_a_wb_trigger==1 and [
              
              #swy-- select the correct array member by using (curr itp + slot base) and calculate the minimum items to add...
              (store_add,":aval_slot", ":itp_type", slot_troop_shop_aval_itp_counter_base),
              (troop_get_slot,":aval_items", "trp_skill2item_type", ":aval_slot"),
              #swy-- stores the minimum of :items or :aval_items in :items
              #      for example: if we ask for two helmets, but the faction only has one; min(2,1) = 1, just add one, the minimum, solves the WB bug.
              (val_min,":items",":aval_items"),
              
              #swy-- check again that we aren't adding zero items, may cause unexpected bugs, thanks to Marco.
              (gt,":items",0),
              
            ] or []) + [
            
            (troop_add_merchandise,":cur_merchant",":itp_type",":items"),
          (try_end),
        (try_end),
        
        #swy-- make room for the new items and give him some extra money if needed...
        (troop_ensure_inventory_space,":cur_merchant",merchant_inventory_space),
        (troop_sort_inventory, ":cur_merchant"),
		
		#InVain: Scale merchant gold
        (store_troop_gold, ":cur_gold",":cur_merchant"),
		(troop_get_slot, ":min_gold", ":cur_merchant", slot_troop_shop_gold),
		(call_script, "script_get_faction_rank", ":faction"),
	    (assign, ":rank", reg0),
		(val_mul, ":rank", 50),
		(val_add, ":min_gold", ":rank"),
		
		#(party_get_slot, ":center_relation", ":town", slot_center_player_relation),
		(party_get_skill_level, ":player_party_trading", "p_main_party", "skl_trade"),
		(val_mul, ":player_party_trading", 150),
		(val_add, ":min_gold", ":player_party_trading"),
		
		(val_mul, ":center_relation", 10),
		(val_add, ":min_gold", ":center_relation"),

        
        (lt, ":cur_gold",":min_gold"),
        (store_random_in_range,":new_gold",200,400),
        (val_div, ":player_party_trading", 5),
        (val_add, ":new_gold", ":player_party_trading"),
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
        
        (troop_get_slot,":subfaction",":cur_merchant", slot_troop_subfaction),
        
        (assign, ":is_orc_faction", 0),
        (try_begin),
          (this_or_next|eq, ":faction", "fac_mordor"),
          (this_or_next|eq, ":faction", "fac_isengard"),
          (this_or_next|eq, ":faction", "fac_moria"),
          (this_or_next|eq, ":faction", "fac_guldur"),
          (             eq, ":faction", "fac_gundabad"),
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
 
       # # Add Center Relations modifier to Item Quality in horse merchants
        (assign, ":base_chance", 50),
        (party_get_slot, ":center_relation", ":cur_center", slot_center_player_relation),
        (call_script, "script_get_faction_rank", ":faction"),
        (assign, ":rank", reg0),
        (store_mul, ":rank_modifier", ":rank", 5),
        (party_get_skill_level, ":player_party_trading", "p_main_party", "skl_trade"),
        (store_mul, ":trading_modifier", ":player_party_trading", 10),
      
        (store_add, ":quality_modifier", ":center_relation", ":rank_modifier"),
        (val_add, ":quality_modifier", ":trading_modifier"),
        (val_div, ":quality_modifier", 3),
        (val_add, ":quality_modifier", ":base_chance"),
        (set_merchandise_modifier_quality, ":quality_modifier"), #new formula
 
        (try_for_range,":item","itm_sumpter_horse", "itm_warg_reward"),
          (item_get_slot,":item_faction_mask",":item",slot_item_faction),
          (val_and,":item_faction_mask",":faction_mask"),
          
          (set_item_probability_in_merchandise,":item",100),
          (try_begin),
            (eq,":item_faction_mask",0), # faction mismatch
            (set_item_probability_in_merchandise,":item",0),
    ] + (is_a_wb_trigger==1 and [   
          (else_try), #InVain: Rank requirement for items + reduction chance per trading and center relation
            (item_get_abundance, ":rank_req", ":item"),
            (is_between, ":rank_req", 1, 100),
            (val_sub, ":rank_req", 90),
            (store_add, ":rank_bonus", ":trading_modifier", ":center_relation"),
            (val_div, ":rank_bonus", 2),
            (val_sub, ":rank_bonus", 20), 
            (store_random_in_range, ":random", 0, 100),
            (try_begin),
                (lt, ":random", ":rank_bonus"),
                (val_sub, ":rank_req", 1),
            (try_end),
            (lt, ":rank", ":rank_req"),
            (set_item_probability_in_merchandise, ":item", 0),          
    ] or []) + [
          (else_try),
            #swy--> null out its probability if we are part of a subfaction but the item isn't...
            (gt, ":subfaction", 0),
            (neg|is_between, ":item", "itm_sumpter_horse", "itm_steppe_horse"),
            (neg|is_between, ":item", "itm_gondor_courser", "itm_dol_amroth_warhorse"),
            
            #swy-- if the subfaction mask bit index exists, let's make it, turning it into the proper bitmask with powers of two, emulating a leftshift [1 << mask index]:
            #  e.g: mask index 1 = 2             =>  2
            #       mask index 2 = 2 x 2         =>  4
            #       mask index 3 = 2 x 2 x 2     =>  8
            #       mask index 4 = 2 x 2 x 2 x 2 => 16
            
            # note: there's also a val_lshift operation in WB, but that makes it an opcode longer than a direct power of two. :-)
            (assign, ":subfaction_mask", 1),
            (try_for_range, ":unused", 0, ":subfaction"),
              (val_mul, ":subfaction_mask", 2),  # ":subfaction_mask"=1 if regular faction w/o subs, 2,4,8,16... for subs
            (try_end),
            
            (item_get_slot,":item_subfaction_field", ":item", slot_item_subfaction),
            
            # check for subfaction mismatch, in case they match, jump to the next else like a normal item...
            (store_and,":subfaction_result", ":subfaction_mask", ":item_subfaction_field"),
            (       eq,":subfaction_result", 0),
            # --
            (set_item_probability_in_merchandise, ":item", 0),
            
          (else_try), #Invain: Clean up Gondor regular (0no subfac) stores from subfac gear
            (eq, ":faction", fac_gondor),
            (eq, ":subfaction", 0),
            (item_get_slot,":item_subfaction_field", ":item", slot_item_subfaction),
            (assign, ":subfac_found", 0),
            (try_for_range, ":subfaction_check", 1, 7), #not rangers
                (eq, ":subfac_found", 0),
                (assign, ":subfaction_mask", 1),
                (try_for_range, ":unused", 0, ":subfaction_check"),
                  (val_mul, ":subfaction_mask", 2),  # ":subfaction_mask"=1 if regular faction w/o subs, 2,4,8,16... for subs
                (try_end),
                (eq, ":subfaction_mask", ":item_subfaction_field"),
                (assign, ":subfac_found", 1),                
            (try_end),
            (eq, ":subfac_found", 1),
            (set_item_probability_in_merchandise, ":item", 0),
          (try_end),
        (try_end),
		
        #swy-- add poneys to the Iron Hills camp merchant, that's it.
        #      poneys are always cool if there are dwarves over them!
        
        (try_begin),
          (eq, ":cur_merchant", "trp_merchant_ironhill"),
          (set_item_probability_in_merchandise, "itm_pony", 100),
          (troop_add_merchandise, ":cur_merchant", itp_type_horse, 1), #one poney for you!
        (try_end),
        
        # Add mounts/horses to merchant inventories
        (troop_get_slot,":skill","trp_skill2item_type",itp_type_horse), #abundance stored in merchant skills values
        (store_skill_level,":items",":skill",":cur_merchant"),
        (try_begin),
          (gt,":items",0),
          
            #Invain: Relation+trade bonus; (rel+trade_skill*10)/100 (up to 2x)
            (store_add, ":abundance_bonus", ":center_relation", ":trading_modifier"), #get score, up to 200
            (store_mul, ":bonus_items", ":items", ":abundance_bonus"),
            (val_div, ":bonus_items", 100),
            (val_add, ":items", ":bonus_items"),
          
          (troop_add_merchandise,":cur_merchant",itp_type_horse,":items"),
        (try_end),
        
        # Add trade goods to merchant inventories
        (reset_item_probabilities,100),
        (try_for_range, ":cur_goods", food_begin, food_end), #InVain: Limit range to food, no trade goods in TLD
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
            (set_item_probability_in_merchandise,":cur_goods",100),
          (else_try),
            (set_item_probability_in_merchandise,":cur_goods",0),
          (try_end),
          #(set_item_probability_in_merchandise,":cur_goods",":cur_probability"),
        (try_end),
        
        (store_div, ":num_goods", ":center_str_income", 5),
        (val_add, ":num_goods", num_merchandise_goods), #now 3-7
        
            #Invain: Relation+trade bonus; (rel+trade_skill*10)/100 (up to 2x)
            (store_add, ":abundance_bonus", ":center_relation", ":trading_modifier"), #get score, up to 200
            (store_mul, ":bonus_items", ":num_goods", ":abundance_bonus"),
            (val_div, ":bonus_items", 100),
            (val_add, ":num_goods", ":bonus_items"),        

        (try_begin),
            # food quest:
            (assign, ":quest_prevents", 0),
            (try_begin), # don't allow food to generate if the quest says there is a shortage
              (check_quest_active, "qst_deliver_food"),
              (quest_slot_eq, "qst_deliver_food", slot_quest_target_center, ":cur_center"),
              (assign, ":quest_prevents", 1),
            (try_end),
            (eq, ":quest_prevents", 0),
            (troop_add_merchandise,":cur_merchant",itp_type_goods,":num_goods"),
            (troop_ensure_inventory_space,":cur_merchant",merchant_inventory_space), #MV: moved after goods and changed from 65
            (troop_sort_inventory, ":cur_merchant"),
        (try_end),
        
        #swy-- if the horse/ goods merchant is short of bucks, yo. give somm' money to da biotch!
        #      don't expect enlightening comments all the way down. this is the jungle!
		#InVain: Scale merchant gold
        (store_troop_gold, ":cur_gold",":cur_merchant"),
		(troop_get_slot, ":min_gold", ":cur_merchant", slot_troop_shop_gold),
		(val_mul, ":min_gold", 2),
		(val_div, ":min_gold", 3), #horse merchants have less base gold than smiths
		
		(call_script, "script_get_faction_rank", ":faction"),
	    (assign, ":rank", reg0),
		(val_mul, ":rank", 50),
		(val_add, ":min_gold", ":rank"),
		
		(party_get_slot, ":center_relation", ":cur_center", slot_center_player_relation),
		(val_mul, ":center_relation", 10),
		(val_add, ":min_gold", ":center_relation"),
		
		(party_get_skill_level, ":player_party_trading", "p_main_party", "skl_trade"),
		(val_mul, ":player_party_trading", 150),
		(val_add, ":min_gold", ":player_party_trading"),
        
        (lt, ":cur_gold",":min_gold"),
        (store_random_in_range,":new_gold",200,400),
        (val_div, ":player_party_trading", 5),
        (val_add, ":new_gold", ":player_party_trading"),
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
            (assign, ":no_early_scout", 0),
            (try_begin),
              (eq, "$tld_war_began", 0), #preserve pre-war scout balance, before Rhun and Gundabad outposts spawn
              (this_or_next|eq, ":center", "p_town_erebor"),
              #(this_or_next|eq, ":center", "p_town_esgaroth"),
              (eq, ":center", "p_town_beorning_village"),
              (assign, ":no_early_scout", 1),
            (try_end),
            (eq, ":no_early_scout", 0),
            # (store_random_in_range, ":rand", 0, int(15000/ws_scout_freq_multiplier)), # 0-4285
            # (le, ":rand", ":strength"), # 81% for fac.str. 3500
            (store_add, ":chance", ws_scout_chance, ":chance_modifier"),
            (store_random_in_range, ":rand", 0, 100),
            (lt, ":rand", ":chance"), # 60% for fac.str. 3500
            (store_mul, ":limit", ":strength", ws_scout_limit_multiplier*1000),
            (val_div, ":limit", 3500*1000), #17 for fac.str. 3500; 34 for 7000
            # also limit by number of centers = 4+4*centers (8,12,16,20,..), to prevent minor factions map overcrowding
            (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", spt_town),
			(assign, ":num_centers", reg0), #we need this later
            (store_mul, ":center_limit", ":num_centers", 4), (val_add, ":center_limit", 4),
            (val_min, ":limit", ":center_limit"),			
            (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", spt_scout),
			(assign, ":num_scouts", reg0),
            (lt, ":num_scouts", ":limit"),
			(val_mul, ":num_scouts", 2),
			(store_sub, ":spawn_chance", 100, ":num_scouts"),
				(try_begin),
					(gt, ":num_centers", 1), #buff factions that have only one center, by nerfing all other factions: affects Umbar, Khand, Harad, Dunland, Rhun (pre-war), Guldur (pre-war)
					(val_div, ":spawn_chance",2),
				(try_end),
			(store_random_in_range, ":random", 0, 100), #reduce spawn chance if faction already has many scouts, to prevent/slow _major_ factions map overcrowding
			(le, ":random", ":spawn_chance"),
            (set_spawn_radius, 1),
            (spawn_around_party, ":center", ":center_scouts"),
				# (str_store_faction_name, s1, ":faction_no"),
				# (display_message, "@{s1} scouts spawned"),
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
    [
      #(entering_town,":party"),
      (neq,"$ambient_faction","$players_kingdom"),
      (call_script, "script_cf_factions_are_allies", "$ambient_faction","$players_kingdom"),
    ],
    [
      (str_store_faction_name, s11, "$ambient_faction"),
      (str_store_faction_name, s10, "$players_kingdom"),
      (dialog_box,"@When dealing with locals in {s11}, remember that they do not know you and they don't necessarily acknowledge the merits you've earned in {s10}.^^(the Resource Points which you can dispose of among people from {s11} are not the ones you earned in {s10}, but the ones you will earn in {s11} -- see also the Report screen)","@Info"),
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
          (call_script, "script_safe_remove_party", "$qst_bring_back_runaway_serfs_party_1"),
          (val_add, "$qst_bring_back_runaway_serfs_num_parties_fleed", 1),
        (else_try),
          (party_is_in_town, "$qst_bring_back_runaway_serfs_party_1", ":quest_object_center"),
          (call_script, "script_safe_remove_party", "$qst_bring_back_runaway_serfs_party_1"),
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
          (call_script, "script_safe_remove_party", "$qst_bring_back_runaway_serfs_party_2"),
          (val_add, "$qst_bring_back_runaway_serfs_num_parties_fleed", 1),
        (else_try),
          (party_is_in_town, "$qst_bring_back_runaway_serfs_party_2", ":quest_object_center"),
          (call_script, "script_safe_remove_party", "$qst_bring_back_runaway_serfs_party_2"),
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
          (call_script, "script_safe_remove_party", "$qst_bring_back_runaway_serfs_party_3"),
          (val_add, "$qst_bring_back_runaway_serfs_num_parties_fleed", 1),
        (else_try),
          (party_is_in_town, "$qst_bring_back_runaway_serfs_party_3", ":quest_object_center"),
          (call_script, "script_safe_remove_party", "$qst_bring_back_runaway_serfs_party_3"),
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
        (call_script, "script_safe_remove_party", "$qst_follow_spy_spy_party"),
        (assign, "$qst_follow_spy_spy_back_in_town", 1),
        (val_sub, ":num_active", 1),
      (try_end),
      (try_begin),
        (party_is_active, "$qst_follow_spy_spy_partners_party"),
        (val_add, ":num_active", 1),
        (party_is_in_town, "$qst_follow_spy_spy_partners_party", ":quest_object_center"),
        (call_script, "script_safe_remove_party", "$qst_follow_spy_spy_partners_party"),
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
  ##       (call_script, "script_safe_remove_party", ":quest_target_party"),
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
  # (call_script, "script_safe_remove_party", ":quest_target_party"),
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
      (try_for_range, ":npc1", companions_begin, new_companions_end),
        (this_or_next|is_between, ":npc1", companions_begin, companions_end),
        (is_between, ":npc1", new_companions_begin, new_companions_end),
        (main_party_has_troop, ":npc1"),
        (val_add, ":npcs_in_party", 1),
      (try_end),
      (val_sub, ":grievance_divisor", ":npcs_in_party"),
      (store_skill_level, ":persuasion_level", "skl_leadership", "trp_player"), #changed from persuasion - Kham
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
      
      
      (try_for_range, ":npc", companions_begin, new_companions_end),
        (this_or_next|is_between, ":npc", companions_begin, companions_end),
        (is_between, ":npc", new_companions_begin, new_companions_end),
        ###Reset meeting variables
        (troop_set_slot, ":npc", slot_troop_turned_down_twice, 0),
        (try_begin),
          (troop_slot_eq, ":npc", slot_troop_met, 1),
          (troop_set_slot, ":npc", slot_troop_met_previously, 1),
        (try_end),
        
        
        
        
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
  (12, 12,0,[(eq,"$g_ent_water_taking_effect",1),
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
  (1, 0, 0,[
      (eq,"$tld_war_began",0),
      (store_character_level,":level","trp_player"),
      # Completely Replace constant with Global Var, so that we reduce likelihood of misfire.
      # Had the dual system here for savegame compat, but by this time, it should be safe. See Github for the old code.
      (ge, ":level", "$tld_player_level_to_begin_war"),
      
      ],[
      (assign, "$tld_war_began",1),
      (dialog_box,"@The dark shadow finally broke into a storm, and evil hordes started their march on the free people of Middle Earth. Mordor against Gondor in the South, Isengard agains Rohan in the West, Dol Guldur against the Elves... Even in the far North there is a war of its own.","@The War has started!"),
      (play_sound,"snd_evil_horn"),
      # move Dun camp across Isen
      #	(party_get_position, pos1, "p_town_dunland_camp"),
      #	(position_move_x,pos1,-400),
      #	(position_move_y,pos1,500),
      
      #swy-- hardcoded it with absolute positioning so it kind of works in WB... :)
      (set_fixed_point_multiplier, 10),
      (position_set_x,pos1, 459),
      (position_set_y,pos1,-435),
      
      (party_set_position, "p_town_dunland_camp", pos1),
      
      (set_fixed_point_multiplier, 10),
      (position_set_x,pos1,-542),
      (position_set_y,pos1,-130),
      
      (party_set_position, "p_town_khand_camp", pos1),
      
      (set_fixed_point_multiplier, 10),
      (position_set_x,pos1,-480),
      (position_set_y,pos1, 600),
      
      (party_set_position, "p_town_harad_camp", pos1),
      
      #	reveal evil camps through the land
      (try_for_range,":center",centers_begin,centers_end),
        (neg|party_is_active,":center"),
        (store_faction_of_party, ":cur_faction", ":center"),
        (neg|faction_slot_eq, ":cur_faction", slot_faction_advance_camp, ":center"), # don't reveal advance camps
        (enable_party,":center"),
        (call_script, "script_update_center_notes", ":center"),
        # and reinforce
        (assign, ":garrison_strength", 80), #InVain was 13. This is very high so the siegable_always camps don't get razed immediately
        (party_get_slot, ":garrison_limit", ":center", slot_center_garrison_limit),
		(val_mul, ":garrison_limit", 150),
		(val_div, ":garrison_limit", 100),
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
		(neq, "$g_fast_mode", 1),
        (jump_to_menu, "mnu_auto_intro_rohan"),
      (try_end),
      
      # Reveal Gondor Beacons
      (try_for_range, ":beacon", "p_amon_din", "p_scout_party"),
        (enable_party, ":beacon"),
      (try_end),
      
      #Send Gandalf on a little chat
      (try_begin),
        (faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
        (store_and, ":already_done", "$g_tld_conversations_done", tld_conv_bit_gandalf_advice),
        (eq, ":already_done", 0),
        (call_script, "script_send_on_conversation_mission", tld_cc_gandalf_advice),
      (try_end),
      
  ]),
  
  (0.5, 0, 0, [],[#(gt,"$g_fangorn_rope_pulled",-100)],[
      (call_script,"script_party_is_in_fangorn","p_main_party"),
      (assign,":inside_fangorn",reg0),
      (assign, ":continue", 1),
      (try_begin),
        (check_quest_active, "qst_investigate_fangorn"),
        (quest_get_slot, ":timeout", "qst_investigate_fangorn", slot_quest_target_amount), #used to disable fangorn check while burning trees
        (store_current_hours, ":hours"),
        (eq, ":hours", ":timeout"),
        (jump_to_menu, "mnu_fangorn_search_fails"),
        (assign, ":continue", 0),
       (else_try),
        (check_quest_active, "qst_investigate_fangorn"),
        (lt, ":hours", ":timeout"),
        (assign, ":continue", 0),
      (else_try),
        (check_quest_active, "qst_investigate_fangorn"),
        (gt, ":hours", ":timeout"),
        (assign, ":continue", 1),
      (try_end),
      
      (try_begin),
        (eq, "$g_player_is_captive", 0),
        (eq,":inside_fangorn",1),
        (eq,":continue",1),
        (neq, "$g_fast_mode", 1),
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
        (try_for_parties, ":ents"), #remove any ent parties, just to be sure
            (party_get_template_id, ":template", ":ents"),
            (eq, ":template", "pt_ents"),
            (call_script, "script_safe_remove_party",":ents"),
        (try_end),
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
        (party_is_active, ":party_no"),
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
  (1, 0, 90, [], [ #traits crunching
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
        (try_begin),
          (neq|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
          (str_store_string, s27, "@Savagery"),
        (try_end),
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
      # (try_begin),
        # (call_script, "script_cf_check_trait_captain"),
      # (try_end),
      (try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_command_voice, 0),
        (gt, "$trait_check_commands_issued", 0),
        (store_skill_level, ":check", skl_leadership, "trp_player"),
        (ge, ":check", 5),
        (assign, ":check", "$trait_check_commands_issued"),
        (val_mul, ":check", 7),
        (assign, "$trait_check_commands_issued", 0),
        (store_random_in_range, ":rnd", 0, 100),
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
        (store_random_in_range, ":rnd", 0, 100),
        (neg|ge, ":rnd", ":check"),
        (call_script, "script_cf_gain_trait_stealthy"),
      (try_end),
      (try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_berserker, 0),
        (gt, "$trait_check_unarmored_berserker", 0),
        (assign, ":check", "$trait_check_unarmored_berserker"),
        (val_mul, ":check", 5),
        (assign, "$trait_check_unarmored_berserker", 0),
        (store_random_in_range, ":rnd", 0, 100),
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
        (store_random_in_range, ":rnd", 0, 100),
        (neg|ge, ":rnd", ":check"),
        (call_script, "script_cf_gain_trait_battle_scarred"),
        (call_script, "script_cf_gain_trait_fell_beast"), #MV: let the scripts sort out if it's an orc or not :)
      (try_end),
      (try_begin),
        (eq, 0, 1), #disabled
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
        (store_random_in_range, ":rnd", 0, 100),
        (neg|ge, ":rnd", ":count"),
        (call_script, "script_cf_gain_trait_foe_hammer"),
      (try_end),
      #(assign, "$minas_tirith_healing", 0),
      #(assign, "$edoras_healing"      , 0),
      #(assign, "$isengard_healing"    , 0),
      #(assign, "$morannon_healing"    , 0),
      
      (try_begin), #Well-Travelled
        (troop_slot_eq, "trp_traits", slot_trait_well_travelled, 0),
        (assign, ":visited", 0),
        (try_for_range, ":places", "p_legend_amonhen", "p_theater_SE_center"),
          (party_slot_eq, ":places", slot_legendary_visited, 1),
          (val_add, ":visited",1),
        (try_end),
        #Don't forget to add Fangorn condition for side_good later, when we've added Fangorn description - Kham
        (ge, ":visited",3),
        (call_script, "script_gain_trait_well_travelled"),
      (try_end),
    ] + (is_a_wb_trigger==1 and [
      (try_begin), #Skinchanger trait -> BEAR Arsakes
        # Chance ~num_of_private_bear_meetings, but has to be more than 5
        # special case as we store value related to chance of getting it in the slot itslef
        (neg|troop_slot_eq, "trp_traits", slot_trait_bear_shape, 1), 
        (troop_get_slot, ":chance", "trp_traits", slot_trait_bear_shape),
        (val_sub, ":chance", 5),
        (ge, ":chance", 0), 
        (val_add, ":chance", 5), 
        (store_random_in_range, ":rnd", 0, 100),
        (le, ":rnd", ":chance"),
        (call_script, "script_cf_gain_trait_bear_shape"),
      (try_end),
  ] or [])
  ),
  
  #check progress on oath quest
  (24, 0, 0, [(check_quest_active, "qst_oath_of_vengeance", 1)],[
      #(quest_get_slot, ":start_killcount", "qst_oath_of_vengeance", 3),
      (quest_get_slot, ":target", "qst_oath_of_vengeance", 2),
      (quest_get_slot, ":start_day", "qst_oath_of_vengeance", 1),
      (quest_get_slot, ":source_fac", "qst_oath_of_vengeance", 4),
      (quest_get_slot, ":hero", "qst_oath_of_vengeance", 5),
      (quest_get_slot, ":moria", "qst_oath_of_vengeance", 6),
      (store_current_day, ":day"),
      (val_sub, ":day", 10), #checks start after 5 days under oath - #Kham - changed to 10 days
      (gt, ":day", ":start_day"),
      
      #Kham - Oath of Vengeance Refactor START
      #(assign,":count", 0), #count current killcount for target faction
      #(try_for_range, ":ptemplate", "pt_gondor_scouts", "pt_kingdom_hero_party"),
      #	(spawn_around_party,"p_main_party",":ptemplate"),
      #	(store_faction_of_party,":fac", reg0),
      #	(call_script, "script_safe_remove_party", reg0),
      #	(eq, ":fac", ":target"),
      #	(store_num_parties_destroyed_by_player, ":n", ":ptemplate"),
      #	(val_add,":count",":n"),
      #(try_end),
      #(val_sub, ":count", 3), # need to kill at least 3 target faction parties to succeed
      
      (faction_get_slot, ":target_faction_strength", ":target", slot_faction_strength),
      
      (try_begin),
        (eq, ":target_faction_strength", fac_str_dying),
        (store_div, ":tld_oath_kills", tld_oath_kills,2),
      (else_try),
        (eq, ":target_faction_strength", fac_str_very_weak),
        (store_sub, ":tld_oath_kills", tld_oath_kills, 30),
      (else_try),
        (assign, ":tld_oath_kills", tld_oath_kills),
      (try_end),
      
      (try_begin),
        (faction_slot_eq, ":target", slot_faction_state, sfs_active), # CC: Faction must be alive to fail quest, otherwise you suceed.
        #(neg|ge, ":count", ":start_killcount"), - #Kham Refactor Commented Out
        (neg|ge, "$oath_kills", ":tld_oath_kills"),
        (call_script, "script_fail_quest", "qst_oath_of_vengeance"),
        (set_show_messages, 0),
        (call_script, "script_end_quest", "qst_oath_of_vengeance"),
        (set_show_messages, 1),
        #(str_store_faction_name, s1, ":source_fac"),
        (try_begin),
          (eq, ":moria",1),
          (display_message, "@You have failed to fulfill your oath to avenge Balin and his company!", color_bad_news),
        (else_try),
          (str_store_troop_name, s1, ":hero"),
          (display_message, "@You have failed to fulfill your oath of vengeance for {s1}'s heroic death!", color_bad_news),
        (try_end),
        (call_script, "script_cf_gain_trait_oathbreaker"),
      (else_try),
        #(ge, ":count", ":start_killcount"), #Kham Refactor Commented Out
        (this_or_next|ge, "$oath_kills", ":tld_oath_kills"),
        (neg|faction_slot_eq, ":target", slot_faction_state, sfs_active), # CC: If faction is not active, you have completed the quest.
        (call_script, "script_succeed_quest", "qst_oath_of_vengeance"),
        (set_show_messages, 0),
        (call_script, "script_end_quest", "qst_oath_of_vengeance"),
        (set_show_messages, 1),
        (call_script, "script_cf_gain_trait_oathkeeper"),
        #(val_sub, ":start_killcount", 3), #Kham Refactor Commented Out
        #(val_sub, ":count", ":start_killcount"),
        #(store_mul, reg1, ":count", 4),
        #(str_store_faction_name, s1, ":source_fac"),
        
        #Kham - Oath of Vengeance Refactor END
        
        (try_begin),
          (neg|faction_slot_eq, ":target", slot_faction_state, sfs_active),
          (str_store_string, s22, "@Your troops value your effort to fulfill your oath, but acknowledge that events unfolded too quickly. As a result, "),
        (else_try),
          (faction_slot_eq, ":target", slot_faction_state, sfs_active),
          (str_store_string, s22, "@ "),
        (try_end),
        
        (try_begin),
          (eq, ":moria",1),
          (display_message, "@{s22}You have fulfilled your oath to avenge Balin and his company!", color_good_news),
        (else_try),
          (str_store_troop_name, s1, ":hero"),
          (display_message, "@{s22}You have fulfilled your oath of vengeance for {s1}'s heroic death!", color_good_news),
        (try_end),
        (call_script, "script_increase_rank", ":source_fac", reg1),
      (try_end),
  ]),
  
  # check for mutiny when orcs in party
  (2, 0, 2, [
      (neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good),
      (party_get_morale, ":party_morale", p_main_party),
      (le, ":party_morale", 90), #counter only ticks if morale is <90
      (val_sub, "$mutiny_counter",2),
      
      #InVain: Removed this block, instead added morale checks here and for final mutiny chance below
      ## Kham - Reduce rate of mutiny by level and rank (player faction, I could also look at player's rank in mordor & isengard, but lets start with this)
      # (store_character_level, ":level","trp_player"),
      # (call_script, "script_get_faction_rank", "$players_kingdom"),
      # (assign, ":rank", reg0),
      # (store_skill_level, reg1, "skl_leadership", "trp_player"),
      # (this_or_next|lt, reg1,     6),
      # (this_or_next|lt, ":level",17),
      # (             lt, ":rank",  5),
      
      # (try_begin), ## Reduce deduction by 1 when player is level 12 or rank 3, just to ease it a bit, before disappearing completely.
        # (this_or_next|eq, reg1,     5),
        # (this_or_next|is_between, ":level",13,17),
        # (             is_between, ":rank",  3,5),
        # (val_sub, "$mutiny_counter",1),
      # (else_try),
        # (val_sub, "$mutiny_counter",2),
      # (try_end),      
      ## Kham Changes END

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
      
      (store_skill_level, reg1, "skl_leadership", "trp_player"), # persuasion neutralizes 5 orcs per level ##Kham - Change to Leadership instead, as there is nothing else persuasion is used for
      (val_mul, reg1, 5),
      (val_sub, ":orcs", reg1),
      (troop_get_type, reg1, "trp_player"),
      
      (try_begin),
        (eq, reg1, tf_orc), (val_sub, ":orcs", 10),
      (try_end), # player being an orc himself neutralizes 10 orcs
      
      (val_max, ":orcs", 1),
      (party_get_num_companions, reg1, "p_main_party"),
      (gt, reg1, 15), # for big enough party
      (val_div, reg1, ":orcs"),
      (lt, reg1, 2), # more than 50% of "adjusted orcs" in party?
      
      #(store_sub, ":chance", 100, ":party_morale"),
      (store_random_in_range, reg1, 0, 80), 
      (gt, reg1, ":party_morale"), #mutiny chance, doesn't happen when morale is >80
      
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
  (8, 0, 0, [],[
      (eq, "$tld_option_animal_ambushes", 1), # Allows option to be toggled on and off.
      (neq,"$tld_war_began", 0),
      (try_begin),
        (party_get_attached_to, ":attached_to_party", "p_main_party"),
        (neg|is_between, ":attached_to_party", centers_begin, centers_end),
        (eq|this_or_next, "$current_player_region", region_misty_mountains),
        (eq|this_or_next, "$current_player_region", region_grey_mountains),
        (eq|this_or_next, "$current_player_region", region_n_mirkwood),
        (eq,              "$current_player_region", region_s_mirkwood),
        (assign, ":continue", 1),
        (try_for_range, ":party_id", centers_begin, centers_end), # Don't allow ambushes if player is close to a center.
          (eq, ":continue", 1),
          (party_is_active, ":party_id"), # Skip non-existant adv. camps.
          (store_distance_to_party_from_party, ":dist", ":party_id", "p_main_party"),
          #(display_message, "@8 Units away..."),
          (lt, ":dist", 8),
          (assign, ":continue", 0),
        (try_end),
        (eq, ":continue", 1),
        (assign, ":ambush_chance", 90), # 90% chance by default
        (party_get_num_companions, reg1, "p_main_party"),
        (try_begin),
          (lt, reg1, 8),
          (val_sub, ":ambush_chance", 50),
        (else_try),
          (gt, reg1, 16),
          (le, reg1, 35),
          (val_sub, ":ambush_chance", 70),
        (else_try),
          (gt, reg1, 35),
          (val_sub, ":ambush_chance", 200),
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
          (assign, reg10, ":rnd"),
          (assign, reg11, ":ambush_chance"),
          (lt, ":rnd", ":ambush_chance"),
          (store_random_in_range, ":rnd", 1, 101),
          (store_mul, ":ambush_counter", "$creature_ambush_counter", 5),
          (gt, ":rnd", ":ambush_counter"),
          (val_add, "$creature_ambush_counter", 1),
          (jump_to_menu, "mnu_animal_ambush"),
        (try_end),
      (try_end),
  ]),
  
  # Decrement the ambush counter every 20 hours (CppCoder)
  (18, 0, 0, [(gt, "$creature_ambush_counter", 0)],[(val_sub, "$creature_ambush_counter", 1)]),
  
  
  
  # Defend / Hunt Down Refugees quest
  (0.5, 0.0, 0.0,
    [
      (assign, ":continue", 0),
      
      (try_begin),
        (check_quest_active, "qst_blank_quest_01"),
        (neg|check_quest_concluded, "qst_blank_quest_01"),
        (assign, ":quest", "qst_blank_quest_01"),
        (assign, ":continue", 1),
      (else_try),
        (check_quest_active, "qst_blank_quest_02"),
        (neg|check_quest_concluded, "qst_blank_quest_02"),
        (assign, ":quest", "qst_blank_quest_02"),
        (assign, ":continue", 1),
      (else_try),
        (neg|check_quest_active, "qst_blank_quest_01"),
        (try_begin),
          (party_is_active, "$qst_raider_party_1"),
          (call_script, "script_safe_remove_party", "$qst_raider_party_1"),
        (try_end),
        (try_begin),
          (party_is_active, "$qst_raider_party_2"),
          (call_script, "script_safe_remove_party", "$qst_raider_party_2"),
        (try_end),
        (try_begin),
          (party_is_active, "$qst_raider_party_3"),
          (call_script, "script_safe_remove_party", "$qst_raider_party_3"),
        (try_end),
      (try_end),
      
      (eq, ":continue", 1),
      
      (assign, "$qst_raider_party_total", 0),
      
      (try_begin),
        (eq, ":quest", "qst_blank_quest_01"),
        (try_for_parties, ":qst_raider_parties"),
          (eq, ":qst_raider_parties", "$qst_raider_party_1"),
          (party_is_active, ":qst_raider_parties"),
          (party_is_active, "$qst_refugee_party_1"),
          (party_set_ai_behavior,":qst_raider_parties",ai_bhvr_attack_party),
          (party_set_ai_object,":qst_raider_parties","$qst_refugee_party_1"),
          (val_add, "$qst_raider_party_total", 1),
        (else_try),
          (eq, ":qst_raider_parties", "$qst_raider_party_2"),
          (party_is_active, ":qst_raider_parties"),
          (party_is_active, "$qst_refugee_party_2"),
          (party_set_ai_behavior,":qst_raider_parties",ai_bhvr_attack_party),
          (party_set_ai_object,":qst_raider_parties","$qst_refugee_party_2"),
          (val_add, "$qst_raider_party_total", 1),
        (else_try),
          (eq, ":qst_raider_parties", "$qst_raider_party_3"),
          (party_is_active, ":qst_raider_parties"),
          (party_is_active, "$qst_refugee_party_3"),
          (party_set_ai_behavior,":qst_raider_parties",ai_bhvr_attack_party),
          (party_set_ai_object,":qst_raider_parties","$qst_refugee_party_3"),
          (val_add, "$qst_raider_party_total", 1),
        (try_end),
      (try_end),
      
      (call_script, "script_find_theater", "p_main_party"),
      (assign, ":theater", reg0),
      (assign, ":raiders", "pt_mordor_scouts"),
      (assign, ":guards", "pt_gondor_scouts"),
      
      (try_begin),
        (eq, ":theater", theater_SE),
        (assign, ":raiders", "pt_mordor_scouts"),
        (assign, ":guards", "pt_gondor_scouts"),
      (else_try),
        (eq, ":theater", theater_SW),
        (assign, ":raiders", "pt_isengard_scouts_warg"),
        (assign, ":guards", "pt_rohan_scouts"),
      (else_try),
        (eq, ":theater", theater_C),
        (assign, ":raiders", "pt_gundabad_scouts"),
        (assign, ":guards", "pt_beorn_scouts"),
      (else_try),
        (assign, ":raiders", "pt_rhun_scouts"),
        (assign, ":guards", "pt_dale_scouts"),
      (try_end),
      
      (try_begin),
        (eq, ":quest", "qst_blank_quest_01"),
        (le, "$qst_raider_party_total", 1),
        (store_random_in_range, ":random", 0 , 100),
        (store_character_level, ":player_level", "trp_player"),
		(store_sub, ":raider_amount", ":player_level", 7),
		(val_div, ":raider_amount", 3),
		(val_add, ":raider_amount", 1),
		(val_min, ":raider_amount", 7),
        (le, ":random", 5),
        (set_spawn_radius, 15),
        
        (try_begin),
          (neg|party_is_active, "$qst_raider_party_1"),
          (party_is_active, "$qst_refugee_party_1"),
          (spawn_around_party,  "$qst_refugee_party_1", ":raiders"),
          (assign, "$qst_raider_party_1", reg0),
		  (try_for_range, ":unused", 0, ":raider_amount"),
			(party_add_template, "$qst_raider_party_1", ":raiders"),
			(party_upgrade_with_xp, "$qst_raider_party_1", 50),
          (try_end),
          (party_set_name, "$qst_raider_party_1", "@Raiders"),
          (party_set_flags, "$qst_raider_party_1", pf_quest_party, 1),
          (party_set_faction, "$qst_raider_party_1", "fac_manhunters"),
          (party_set_ai_initiative, "$qst_raider_party_1", 10),
        (else_try),
          (neg|party_is_active, "$qst_raider_party_2"),
          (party_is_active, "$qst_refugee_party_2"),
          (spawn_around_party,  "$qst_refugee_party_2", ":raiders"),
          (assign, "$qst_raider_party_2", reg0),
          (try_for_range, ":unused", 0, ":raider_amount"),
			(party_add_template, "$qst_raider_party_2", ":raiders"),
			(party_upgrade_with_xp, "$qst_raider_party_2", 50),
          (try_end),
          (party_set_name, "$qst_raider_party_2", "@Raiders"),
          (party_set_flags, "$qst_raider_party_2", pf_quest_party, 1),
          (party_set_faction, "$qst_raider_party_2", "fac_manhunters"),
          (party_set_ai_initiative, "$qst_raider_party_2", 10),
        (else_try),
          (neg|party_is_active, "$qst_raider_party_3"),
          (party_is_active, "$qst_refugee_party_3"),
          (spawn_around_party,  "$qst_refugee_party_3", ":raiders"),
          (assign, "$qst_raider_party_3", reg0),
          (try_for_range, ":unused", 0, ":raider_amount"),
			(party_add_template, "$qst_raider_party_3", ":raiders"),
			(party_upgrade_with_xp, "$qst_raider_party_3", 50),
          (try_end),
          (party_set_name, "$qst_raider_party_3", "@Raiders"),
          (party_set_flags, "$qst_raider_party_3", pf_quest_party, 1),
          (party_set_faction, "$qst_raider_party_3", "fac_manhunters"),
          (party_set_ai_initiative, "$qst_raider_party_3", 10),
        (try_end),
      (try_end),
      
      (try_begin),
        (eq, ":quest", "qst_blank_quest_02"),
        (this_or_next|ge, "$qst_refugees_escaped", 2),
        (ge, "$qst_refugees_killed", 2),
        
        (neg|party_is_active, "$qst_reinforcement_party"),
        
        (store_random_in_range, ":random", 0 , 100),
        (store_character_level, ":player_level", "trp_player"),
		(store_sub, ":reinf_amount", ":player_level", 7),
		(val_div, ":reinf_amount", 3),
		(val_add, ":reinf_amount", 1),
		(val_min, ":reinf_amount", 7),
        (le, ":random", 35),
        
        (set_spawn_radius, 12),
        (spawn_around_party,  "p_main_party", ":guards"),
        (assign, "$qst_reinforcement_party", reg0),
        (try_for_range, ":unused", 0, ":reinf_amount"),
			(party_add_template, "$qst_reinforcement_party", ":guards"),
			(party_upgrade_with_xp, "$qst_reinforcement_party", 50),
       (try_end),
        
        (party_set_name, "$qst_reinforcement_party", "@Reinforcements"),
        (party_set_ai_behavior, "$qst_reinforcement_party", ai_bhvr_attack_party),
        (party_set_ai_object, "$qst_reinforcement_party", "p_main_party"),
        (party_set_flags, "$qst_reinforcement_party", pf_quest_party, 1),
        (party_set_faction, "$qst_reinforcement_party", "fac_manhunters"),
        (party_set_ai_initiative, "$qst_reinforcement_party", 10),
        
        #(display_log_message, "@DEBUG: Reinforcement Party Spawned", color_bad_news),
      (try_end),
      
      (quest_get_slot, ":quest_target_center", ":quest", slot_quest_target_center),
      
      (try_begin),
        (party_is_active, "$qst_refugee_party_1"),
        (try_begin),
          (party_is_in_town, "$qst_refugee_party_1", ":quest_target_center"),
          (call_script, "script_safe_remove_party", "$qst_refugee_party_1"),
          (val_add, "$qst_refugees_escaped", 1),
          (assign, "$qst_refugee_party_1_escaped", 1),
          (try_begin),
            (eq, ":quest", "qst_blank_quest_01"),
            (party_is_active, "$qst_raider_party_1"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_1"),
          (try_end),
        (else_try),
          (store_distance_to_party_from_party, ":cur_distance", ":quest_target_center", "$qst_refugee_party_1"),
          (gt, ":cur_distance", 2),
          (party_set_ai_object, "$qst_refugee_party_1", ":quest_target_center"),
        (try_end),
      (else_try),
        (neg|party_is_active, "$qst_refugee_party_1"),
        (neq, "$qst_refugee_party_1_killed", 1),
        (neq, "$qst_refugee_party_1_escaped", 1),
        #(str_store_string, s3, "@DEBUG: Refugee Party 1 Destroyed"),
        #(add_quest_note_from_sreg, "qst_blank_quest_02", 3, s3, 0),
        (val_add, "$qst_refugees_killed", 1),
        (assign, "$qst_refugee_party_1_killed", 1),
      (try_end),
      
      (try_begin),
        (party_is_active, "$qst_refugee_party_2"),
        (try_begin),
          (party_is_in_town, "$qst_refugee_party_2", ":quest_target_center"),
          (call_script, "script_safe_remove_party", "$qst_refugee_party_2"),
          (val_add, "$qst_refugees_escaped", 1),
          (assign, "$qst_refugee_party_2_escaped", 1),
          (try_begin),
            (eq, ":quest", "qst_blank_quest_01"),
            (party_is_active, "$qst_raider_party_2"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_2"),
          (try_end),
        (else_try),
          (store_distance_to_party_from_party, ":cur_distance", ":quest_target_center", "$qst_refugee_party_2"),
          (gt, ":cur_distance", 2),
          (party_set_ai_object, "$qst_refugee_party_2", ":quest_target_center"),
        (try_end),
      (else_try),
        (neg|party_is_active, "$qst_refugee_party_2"),
        (neq, "$qst_refugee_party_2_killed", 1),
        (neq, "$qst_refugee_party_2_escaped", 1),
        #(str_store_string, s3, "@DEBUG: Refugee Party 2 Destroyed"),
        #(add_quest_note_from_sreg, "qst_blank_quest_02", 3, s3, 0),
        (val_add, "$qst_refugees_killed", 1),
        (assign, "$qst_refugee_party_2_killed", 1),
      (try_end),
      
      (try_begin),
        (party_is_active, "$qst_refugee_party_3"),
        (try_begin),
          (party_is_in_town, "$qst_refugee_party_3", ":quest_target_center"),
          (call_script, "script_safe_remove_party", "$qst_refugee_party_3"),
          (val_add, "$qst_refugees_escaped", 1),
          (assign, "$qst_refugee_party_3_escaped", 1),
          (try_begin),
            (eq, ":quest", "qst_blank_quest_01"),
            (party_is_active, "$qst_raider_party_3"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_3"),
          (try_end),
        (else_try),
          (store_distance_to_party_from_party, ":cur_distance", ":quest_target_center", "$qst_refugee_party_3"),
          (gt, ":cur_distance", 2),
          (party_set_ai_object, "$qst_refugee_party_3", ":quest_target_center"),
        (try_end),
      (else_try),
        (neg|party_is_active, "$qst_refugee_party_3"),
        (neq, "$qst_refugee_party_3_killed", 1),
        (neq, "$qst_refugee_party_3_escaped", 1),
        #(str_store_string, s3, "@DEBUG: Refugee Party 3 Destroyed"),
        #(add_quest_note_from_sreg, "qst_blank_quest_02", 3, s3, 0),
        (val_add, "$qst_refugees_killed", 1),
        (assign, "$qst_refugee_party_3_killed", 1),
      (try_end),
      
      (assign, ":sum_removed", "$qst_refugees_escaped"),
      (assign, reg10, "$qst_refugees_escaped"),
      
      (val_add, ":sum_removed", "$qst_refugees_killed"),
      (assign, reg11, "$qst_refugees_killed"),
      
      (str_store_string, s5, "@Refugees Escaped: {reg10} --- Refugees Killed: {reg11}"),
      (add_quest_note_from_sreg, ":quest", 3, s5, 0),
      (try_begin),
        (eq, ":quest", "qst_blank_quest_01"),
        (assign, reg12, "$qst_raider_party_defeated"),
        (str_store_string, s6, "@Raider Parties Killed: {reg12}"),
        (add_quest_note_from_sreg, ":quest", 4, s5, 0),
      (try_end),
      
      (ge, ":sum_removed", 3),
      
      (assign, ":continue_2", 0),
      
      (try_begin),
        (party_is_active, ":quest_target_center"),
        (assign, ":continue_2", 1),
      (else_try),
        (call_script, "script_cancel_quest", ":quest"),
        (display_message, "@One of the target centers by the refugee trains have been destroyed. The refugees have scattered, and are nowhere to be found.", color_bad_news),
        (set_show_messages, 0),
        (call_script, "script_safe_remove_party", "$qst_raider_party_1"),
        (call_script, "script_safe_remove_party", "$qst_raider_party_2"),
        (call_script, "script_safe_remove_party", "$qst_raider_party_3"),
        (call_script, "script_safe_remove_party", "$qst_refugee_party_1"),
        (call_script, "script_safe_remove_party", "$qst_refugee_party_2"),
        (call_script, "script_safe_remove_party", "$qst_refugee_party_3"),
        (set_show_messages, 1),
      (try_end),
      
      (eq, ":continue_2", 1),
      
      (try_begin),
        (eq, ":quest", "qst_blank_quest_01"),
        (try_begin),
          (ge, "$qst_refugees_escaped", 3),
          (call_script, "script_succeed_quest", "qst_blank_quest_01"),
          (try_begin),
            (party_is_active, "$qst_raider_party_1"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_1"),
          (try_end),
          (try_begin),
            (party_is_active, "$qst_raider_party_2"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_2"),
          (try_end),
          (try_begin),
            (party_is_active, "$qst_raider_party_3"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_3"),
          (try_end),
		  
        (else_try),
          (eq, "$qst_refugees_killed", 3),
          (call_script, "script_fail_quest", "qst_blank_quest_01"),
          (try_begin),
            (party_is_active, "$qst_raider_party_1"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_1"),
          (try_end),
          (try_begin),
            (party_is_active, "$qst_raider_party_2"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_2"),
          (try_end),
          (try_begin),
            (party_is_active, "$qst_raider_party_3"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_3"),
		  (try_end),
			
        (else_try),
			(assign, ":continue", 0),
			(try_begin), (ge, "$qst_refugees_escaped", 3), (assign, ":continue", 1),
			(else_try), (ge, "$qst_refugees_escaped", 2),(ge, "$qst_refugees_killed", 1), (assign, ":continue", 1),
			(else_try), (ge, "$qst_refugees_escaped", 1),(ge, "$qst_refugees_killed", 2), (assign, ":continue", 1),
			(try_end),
		  (eq, ":continue", 1),
		  (display_message, "@quest concluded"),
          (call_script, "script_conclude_quest", "qst_blank_quest_01"),
          (try_begin),
            (party_is_active, "$qst_raider_party_1"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_1"),
          (try_end),
          (try_begin),
            (party_is_active, "$qst_raider_party_2"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_2"),
          (try_end),
          (try_begin),
            (party_is_active, "$qst_raider_party_3"),
            (call_script, "script_safe_remove_party", "$qst_raider_party_3"),
		  (try_end),
        (try_end),
      (else_try),
        (eq, ":quest", "qst_blank_quest_02"),
        (try_begin),
          (ge, "$qst_refugees_killed", 3),
          (call_script, "script_succeed_quest", "qst_blank_quest_02"),
        (else_try),
          (ge, "$qst_refugees_escaped", 1),
          (call_script, "script_fail_quest", "qst_blank_quest_02"),
          (try_begin),
            (party_is_active, "$qst_refugee_party_1"),
            (call_script, "script_safe_remove_party", "$qst_refugee_party_1"),
          (try_end),
          (try_begin),
            (party_is_active, "$qst_refugee_party_2"),
            (call_script, "script_safe_remove_party", "$qst_refugee_party_2"),
          (try_end),
          (try_begin),
            (party_is_active, "$qst_refugee_party_3"),
            (call_script, "script_safe_remove_party", "$qst_refugee_party_3"),
          (try_end),
        (try_end),
      (try_end),
      
      ],[],
  ),
  
  # save game compatibility triggers. replace those if you add new ones
  
  #(999, 0, ti_once, [],[]), Replaced by Defend / Hunt Down Refugees Quest - Kham
  (999, 0, ti_once, [],[]),
  (999, 0, ti_once, [],[]),
  (999, 0, ti_once, [],[]),
  (999, 0, ti_once, [],[]),
  (999, 0, ti_once, [],[]),
  (999, 0, ti_once, [],[]),
  (999, 0, ti_once, [],[]),
  
]

# Custom Camera Trigger for Orc and Dwarf

if is_a_wb_trigger==1:
  triggers +=[
  (1, 0, ti_once,
    [(map_free),
      (this_or_next|eq, "$player_looks_like_an_orc",                1),
      (             eq,          "$players_kingdom",      "fac_dwarf"),
    ],
    
    [(dialog_box, "@As an Orc or a Dwarf, you can take advantage of the Custom Camera we have implemented in order to improve your experience with TLD's shorter races. See Game Concepts for more information about how to use this.", "@Custom Camera")]),
]
