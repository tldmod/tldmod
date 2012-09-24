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

ai_scripts = [

# script_recalculate_ais
("recalculate_ais",
	[(try_begin),
	  (ge,"$tld_war_began",1),  # faction AI can change only if War started, GA
	  (call_script, "script_init_ai_calculation"),
	  (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),   # recalculate AI for active non-player factions
		(faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
		(neg|faction_slot_eq, ":faction_no",  slot_faction_marshall, "trp_player"),
		(call_script, "script_decide_faction_ai", ":faction_no"),
	  (try_end),
	  (call_script, "script_decide_kingdom_party_ais"),               # recalculate AI for hero-led parties
	(try_end),
]),

# script_init_ai_calculation
# sets own and combined nearby friends' strength into slots of hero and center parties
  ("init_ai_calculation",
    [ (try_for_range, ":cur_troop", heroes_begin, heroes_end),
        (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
        (ge, ":cur_party", 0),
        (call_script, "script_party_calculate_strength", ":cur_party", 0), #will update slot_party_cached_strength for hero parties
      (try_end),
      (call_script, "script_party_calculate_strength", "p_main_party", 0), #will update slot_party_cached_strength for player party
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (call_script, "script_party_calculate_strength", ":cur_center", 0), #will update slot_party_cached_strength for centers
      (try_end),
      
      #MV: also calculate the strength of faction patrols
      (try_for_parties, ":patrol"),
        (party_is_active, ":patrol"),
        (party_get_slot, ":party_type", ":patrol", slot_party_type), 
        (this_or_next|eq, ":party_type", spt_patrol),
        (this_or_next|eq, ":party_type", spt_raider),
        (eq, ":patrol", spt_scout),
        (call_script, "script_party_calculate_strength", ":patrol", 0), #will update slot_party_cached_strength
      (try_end),    

      (try_for_range, ":cur_center", centers_begin, centers_end),
        (store_faction_of_party, ":center_faction", ":cur_center"),
        (is_between, ":center_faction", kingdoms_begin, kingdoms_end),
        (call_script, "script_party_calculate_and_set_nearby_friend_strength", ":cur_center"),
      (try_end),
      (try_for_range, ":cur_troop", heroes_begin, heroes_end),
        (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
        (gt, ":cur_troop_party", 0),
        (party_is_active, ":cur_troop_party"),
        (call_script, "script_party_calculate_and_set_nearby_friend_strength", ":cur_troop_party"),
      (try_end),
      (call_script, "script_party_calculate_and_set_nearby_friend_strength", "p_main_party"),
      ]),

# script_decide_faction_ai
# INPUT: arg1 faction_no
#called from triggers
  ("decide_faction_ai",
   [(try_begin),
	   (ge,"$tld_war_began",1),  # faction AI can change only if War started, GA
       
	   (store_script_param_1, ":faction_no"),
	   (faction_get_slot, ":old_faction_ai_state", ":faction_no", slot_faction_ai_state),
       (faction_get_slot, ":old_faction_ai_object", ":faction_no", slot_faction_ai_object),
       (faction_get_slot, ":old_faction_ai_last_offensive_time", ":faction_no", slot_faction_ai_last_offensive_time),
       (faction_get_slot, ":faction_theater", ":faction_no", slot_faction_active_theater), #TLD
       (faction_get_slot, ":faction_strength", ":faction_no", slot_faction_strength), #TLD
       
       (assign, ":faction_marshall_party", -1),
       (assign, ":faction_marshall_army_strength", 1),#0 might cause division by zero problems
       (assign, ":faction_marshall_num_followers", 1),
# TLD no change of marshall
#       (call_script, "script_select_faction_marshall", ":faction_no"),
#       (assign, ":faction_marshall", reg0),
#       (assign, ":marshall_changed", 0),
#       (try_begin),
#         (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":faction_marshall"),
#         (assign, ":marshall_changed", 1),
#         (eq, "$players_kingdom", ":faction_no"),
#         (str_store_troop_name, s1, ":faction_marshall"),
#         (str_store_faction_name, s2, ":faction_no"),
#         (display_message, "@{s1} is the new marshall of {s2}."),
#         (call_script, "script_check_and_finish_active_army_quests_for_faction", ":faction_no"),
#       (try_end),
#       (faction_set_slot, ":faction_no", slot_faction_marshall, ":faction_marshall"),
        (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
        (assign, ":marshall_changed", 0),
       (try_begin),
         (gt, ":faction_marshall", 0),
         (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
         (gt, ":faction_marshall_party", 0),
         (party_get_slot, ":faction_marshall_army_strength", ":faction_marshall_party", slot_party_cached_strength),
         (party_get_slot, ":follower_strength", ":faction_marshall_party", slot_party_follower_strength),
         (val_add, ":faction_marshall_army_strength", ":follower_strength"),
         (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
           (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
           (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
           (gt, ":cur_party", 0),
           (party_is_active, ":cur_party"),
           (party_slot_eq, ":cur_party", slot_party_commander_party, ":faction_marshall_party"),
           (val_add, ":faction_marshall_num_followers", 1),
         (try_end),
       (try_end),

       (faction_get_slot, ":marshall_num_old_followers", ":faction_no", slot_faction_ai_offensive_max_followers),
       (val_max, ":marshall_num_old_followers", 1),
       (store_mul, ":offensive_rating", ":faction_marshall_num_followers", 100),
       (val_mul, ":offensive_rating", ":faction_marshall_num_followers"),
       (val_div, ":offensive_rating", ":marshall_num_old_followers"),
       (val_div, ":offensive_rating", ":marshall_num_old_followers"),
       (val_min, ":offensive_rating", 100),#Max 100% efficiency
       
       (faction_get_slot, ":num_armies", ":faction_no", slot_faction_num_armies),
       #(faction_get_slot, ":num_castles", ":faction_no", slot_faction_num_castles),
       #(faction_get_slot, ":num_towns",  ":faction_no", slot_faction_num_towns),

       (store_current_hours, ":cur_hours"),
       (store_sub, ":offensive_hours", ":cur_hours", ":old_faction_ai_last_offensive_time"),

       (assign, ":num_enemies", 0),
       (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
         (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
         (store_relation, ":reln", ":cur_kingdom", ":faction_no"),
         (lt, ":reln", 0),
         (val_add, ":num_enemies", 1),
       (try_end),

       (assign, ":chance_defend", 0),
       (assign, ":chance_gathering_army", 0),
       (assign, ":chance_attacking_center", 0),
       (assign, ":chance_raiding_village", 0),
       (assign, ":chance_attacking_enemy_army", 0),
       (assign, ":chance_attacking_enemies_around_center", 0),
       (assign, ":target_attacking_center", -1),
		#(assign, ":target_raiding_village", -1),
       (assign, ":target_attacking_enemy_army", -1),
       (assign, ":target_attacking_enemies_around_center", -1),

       (try_begin),#Defend
         (eq, ":old_faction_ai_state", sfai_default),
         (assign, ":chance_defend", 100),
       (else_try),
         (eq, ":old_faction_ai_state", sfai_gathering_army),
         (gt, ":offensive_hours", 180),
         (assign, ":chance_defend", 10000),#army can not be gathered, cancel; MV: also used to check for campaign cancellation later
         #else, keep it as 0
       (else_try),
         (store_div, ":chance_defend", ":offensive_hours", 10),
         (store_mul, ":marshall_change_effect", ":marshall_changed", 300),
         (val_add, ":chance_defend", ":marshall_change_effect"),
       (try_end),
		## Gathering army
       (try_begin),
         (eq, ":old_faction_ai_state", sfai_default),
         (gt, ":faction_marshall_party", 0),
         (try_begin),
           #No chance of gathering an army if there are no enemies
           (gt, ":num_enemies", 0),
           (store_mul, ":num_enemies_effect", ":num_enemies", 20),
           (val_add, ":chance_gathering_army", ":num_enemies_effect"),

           #Last offensive
           (store_sub, ":last_offensive_effect", ":offensive_hours", 24 * 4),
           (val_min, ":last_offensive_effect", 200),
           (val_add, ":chance_gathering_army", ":last_offensive_effect"),

           #Number of walled centers (inversely related)
        #TLD: centers don't change hands in TLD frequently, take this
		#           (store_mul, ":center_value", ":num_towns", 2),
		#           (val_add, ":center_value", ":num_castles"),
		#           (val_mul, ":center_value", 10),
		#           (val_max, ":center_value", 5),
		#           (store_sub, ":num_centers_effect", "$g_average_center_value_per_faction", ":center_value"),
		#           (val_add, ":chance_gathering_army", ":num_centers_effect"),

           #Number of armies (inversely related)
           (store_mul, ":num_armies_effect", ":num_armies", 4),
           (store_sub, ":num_armies_effect", 80, ":num_armies_effect"),
           (val_add, ":chance_gathering_army", ":num_armies_effect"),

           #Number of walled centers under siege
           (assign, ":num_centers_under_siege", 0),
           (try_for_range, ":cur_center", centers_begin, centers_end),
		     (party_slot_eq, ":cur_center", slot_center_destroyed, 0), #TLD
             (party_slot_ge, ":cur_center", slot_center_is_besieged_by, 0),
             (store_faction_of_party, ":center_faction", ":cur_center"),
             (eq, ":center_faction", ":faction_no"),
             (val_add, ":num_centers_under_siege", 1),
           (try_end),
           (store_mul, ":num_centers_under_siege_effect", ":num_centers_under_siege", 100),
           (val_add, ":chance_gathering_army", ":num_centers_under_siege_effect"),
         (try_end),
       (else_try),
         (eq, ":old_faction_ai_state", sfai_gathering_army),
#         (this_or_next|lt, ":offensive_hours", 60),
#         (lt, ":faction_marshall_num_followers", 4),
        #TLD: not many hosts in TLD
         (lt, ":offensive_hours", 48), #wait for lords for two days max
         (lt, ":faction_marshall_num_followers", 2), #if we have two+ lords in tow, go and do something creative
         (assign, ":chance_gathering_army", 300), #was 3000, caused too much waiting when there were other interesting opportunities
       (try_end),
## Attacking center
       (try_begin),
         (this_or_next|neq, "$tld_option_siege_reqs", 0), # Disabled normal attacking siege reqs
         (ge, ":faction_strength", fac_str_ok), #TLD
         (neq, ":old_faction_ai_state", sfai_default),
         (gt, ":faction_marshall_party", 0),
         (assign, ":old_target_attacking_center", -1),
         (try_begin),
           (eq, ":old_faction_ai_state", sfai_attacking_center),
           (assign, ":old_target_attacking_center", ":old_faction_ai_object"),
         (try_end),
         (assign, ":best_besiege_center", -1),
         (assign, ":best_besiege_center_score", 0),
         (try_for_range, ":enemy_walled_center", centers_begin, centers_end),
           (party_is_active, ":enemy_walled_center"), #don't attack disabled centers
           (party_slot_eq, ":enemy_walled_center", slot_center_destroyed, 0), #TLD
           #MV: make sure the center is in the active theater
           (party_slot_eq, ":enemy_walled_center", slot_center_theater, ":faction_theater"),
           
           (store_faction_of_party, ":center_faction", ":enemy_walled_center"),
           (party_get_slot, ":siegable", ":enemy_walled_center", slot_center_siegability),
           
           (neq, ":siegable", tld_siegable_never), #some places are never siegable
           
           #MV: make sure the enemy faction is weak enough to be sieged
           (faction_get_slot, ":center_faction_strength", ":center_faction", slot_faction_strength),
           
           (this_or_next|eq, "$tld_option_siege_reqs", 2), # No siege reqs
           (this_or_next|eq, ":siegable", tld_siegable_always), # camps and such can always be sieged
           (lt, ":center_faction_strength", "$g_fac_str_siegable"), # otherwise, defenders need to be weak
           #MV: if it's a faction capital, the enemy needs to be very weak
           (store_sub, ":capital_siegable_str", "$g_fac_str_siegable", fac_str_weak-fac_str_very_weak), #-1000
           (this_or_next|eq, "$tld_option_siege_reqs", 2), # No siege reqs
           (this_or_next|lt, ":center_faction_strength", ":capital_siegable_str"),
           (this_or_next|eq, ":siegable", tld_siegable_always), # camps and such can always be sieged
           (neq, ":siegable", tld_siegable_capital), #if a capital, needs also fac_str_very_weak

           #MV: a small, 10% chance to ignore the center, to add variety to sieging targets
           (store_random_in_range, ":random_ignore", 0, 100),
           (this_or_next|lt, ":random_ignore", 90),
           (eq, ":old_target_attacking_center", ":enemy_walled_center"), #don't ignore if we are currently sieging it
           
           (party_get_slot, ":besieger_party", ":enemy_walled_center", slot_center_is_besieged_by),
           (assign, ":besieger_own_faction", 0),
           (try_begin),
             (ge, ":besieger_party", 0),
             (party_is_active, ":besieger_party"),
             (store_faction_of_party, ":besieger_faction", ":besieger_party"),
             (eq, ":besieger_faction", ":faction_no"),
             (assign, ":besieger_own_faction", 1),
           (try_end),
           (this_or_next|eq, ":besieger_party", -1),
           (eq, ":besieger_own_faction", 1),
           (call_script, "script_get_center_faction_relation_including_player", ":enemy_walled_center", ":faction_no"),
           (assign, ":reln", reg0),
           (lt, ":reln", 0),
           (val_mul, ":reln", -1),
           (val_add, ":reln", 50),
           #(store_distance_to_party_from_party, ":dist", ":enemy_walled_center", ":faction_marshall_party"),
           (call_script, "script_get_tld_distance", ":enemy_walled_center", ":faction_marshall_party"),
           (assign, ":dist", reg0),
           (val_add, ":dist", 20),
           (val_mul, ":dist", 10), #TLD: give more weight on distance consideration
           (party_get_slot, ":center_str", ":enemy_walled_center", slot_party_cached_strength),
           (party_get_slot, ":center_near_str", ":enemy_walled_center", slot_party_nearby_friend_strength),
           (val_add, ":center_str", ":center_near_str"),
           (val_add, ":center_str", 1),
#MV test code begin
# (try_begin),
  # (eq, cheat_switch, 1),
  # (this_or_next|eq, ":faction_no", "fac_gondor"),
  # (eq, ":faction_no", "fac_mordor"),
  # (assign, reg1, ":faction_marshall_army_strength"),
  # (assign, reg2, ":center_str"),
  # (str_store_faction_name, s1, ":faction_no"),
  # (str_store_party_name, s2, ":enemy_walled_center"),
  # (display_message, "@DEBUG: {s1} considers sieging {s2}, marshall str:{reg1} center str:{reg2}.", 0x30FFC8),
# (try_end),
#MV test code end
           (store_mul, ":center_score", 1000, ":faction_marshall_army_strength"),
           (val_div, ":center_score", ":center_str"),
           (store_sub, ":capital_siegable_str", "$g_fac_str_siegable", fac_str_weak-fac_str_very_weak), #-1000
           (this_or_next|lt, ":center_faction_strength", ":capital_siegable_str"), #too much?
           #(this_or_next|lt, ":center_faction_strength", fac_str_very_weak), #attack very weak factions regardless of odds (not too smart, but hopefully the player will help out)
           (gt, ":center_score", 1200), #siege attacks more likely with worse odds (down to +20% advantage), was 1500 (+50%)
           (val_min, ":center_score", 20000),#20 times stronger means an easy victory, distance is more important
           (try_begin),
             (party_slot_eq, ":enemy_walled_center", slot_center_original_faction, ":faction_no"),
             (val_mul, ":center_score", 2),
           (try_end),
           (try_begin),
             (party_slot_eq, ":enemy_walled_center", slot_center_ex_faction, ":faction_no"),
             (val_mul, ":center_score", 2),
           (try_end),
           (try_begin), # if it's a capital, pretty much go for it
             (eq, ":siegable", tld_siegable_capital),
             (val_mul, ":center_score", 3),
             (lt, ":center_faction_strength", fac_str_dying),
             (val_mul, ":center_score", 100),
           (try_end),
           (val_mul, ":center_score", ":reln"),
           (val_div, ":center_score", ":dist"),

           (try_begin),
             (eq, ":enemy_walled_center", ":old_target_attacking_center"),
             (val_mul, ":center_score", 100),
           (try_end),
           (try_begin),
             (gt, ":center_score", ":best_besiege_center_score"),
             (assign, ":best_besiege_center_score", ":center_score"),
             (assign, ":best_besiege_center", ":enemy_walled_center"),
           (try_end),
         (try_end),
      
         (ge, ":best_besiege_center", 0),
         #Center with equal strength at 30 kms away will have a center_score of 1300 (with -40 reln)
         (store_div, ":chance_attacking_center", ":best_besiege_center_score", 15),
         (val_min, ":chance_attacking_center", 1000),
         (assign, ":target_attacking_center", ":best_besiege_center"),
         (try_begin),
           (eq, ":old_target_attacking_center", ":target_attacking_center"),
           (val_mul, ":chance_attacking_center", 100),
         (try_end),
       
         (val_mul, ":chance_attacking_center", ":offensive_rating"),
         (val_div, ":chance_attacking_center", 100),
       (try_end),

#Attacking enemy army that is sieging
       (try_begin),
         (gt, ":faction_strength", fac_str_very_weak), #TLD: conserve strength if very weak
         (neq, ":old_faction_ai_state", sfai_default),
         (gt, ":faction_marshall_party", 0),
         (assign, ":old_target_attacking_enemy_army", -1),
         (try_begin),
           (eq, ":old_faction_ai_state", sfai_attacking_enemy_army),
           (assign, ":old_target_attacking_enemy_army", ":old_faction_ai_object"),
         (try_end),

         (assign, ":best_attack_army", -1),
         (assign, ":best_attack_army_score", 0),
         (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
           (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
           (faction_get_slot, ":cur_kingdom_marshall", ":cur_kingdom", slot_faction_marshall),
           (ge, ":cur_kingdom_marshall", 0),
           (troop_slot_eq, ":cur_kingdom_marshall", slot_troop_occupation, slto_kingdom_hero),
           (troop_get_slot, ":cur_kingdom_marshall_party", ":cur_kingdom_marshall", slot_troop_leaded_party),
           (ge, ":cur_kingdom_marshall_party", 0),
           (party_is_active, ":cur_kingdom_marshall_party"),
           (store_troop_faction, ":cur_kingdom_marshall_faction", ":cur_kingdom_marshall"),
           (store_relation, ":rel", ":cur_kingdom_marshall_faction", ":faction_no"),
           (lt, ":rel", 0),
           (faction_slot_eq, ":cur_kingdom_marshall_faction", slot_faction_ai_state, sfai_attacking_center), #sieging
           (party_get_slot, ":cur_kingdom_marshall_party_follower_strength", ":cur_kingdom_marshall_party", slot_party_follower_strength),
           (party_get_slot, ":cur_kingdom_marshall_party_strength", ":cur_kingdom_marshall_party", slot_party_cached_strength),
           (val_add, ":cur_kingdom_marshall_party_strength", ":cur_kingdom_marshall_party_follower_strength"),
           (store_mul, ":attack_army_score", ":cur_kingdom_marshall_party_strength", 1000),
           (val_div, ":attack_army_score", ":faction_marshall_army_strength"),
           (try_begin),
             (gt, ":attack_army_score", 850),
             (store_sub, ":attack_army_score", 1700, ":attack_army_score"),
           (try_end),
           (gt, ":attack_army_score", 0),
           (val_mul, ":attack_army_score", 2),
           (try_begin),
             (faction_slot_eq, ":cur_kingdom_marshall_faction", slot_faction_ai_state, sfai_attacking_center), #always true
             (val_mul, ":attack_army_score", 5),
           (try_end),
           (try_begin),
             (eq, ":old_target_attacking_enemy_army", ":cur_kingdom_marshall_party"),
             (val_mul, ":attack_army_score", 100),
           (try_end),
           #(store_distance_to_party_from_party, ":dist", ":cur_kingdom_marshall_party", ":faction_marshall_party"),
           (call_script, "script_get_tld_distance", ":cur_kingdom_marshall_party", ":faction_marshall_party"),
           (assign, ":dist", reg0),
           #new condition: either in active theater, or helping out a home town, or distance less than 100
           #this is to prevent long and frequent journeys across the map to help far off allies
           (faction_get_slot, ":besieged_center", ":cur_kingdom_marshall_faction", slot_faction_ai_object),
           (store_faction_of_party, ":besieged_faction", ":besieged_center"),
           (this_or_next|faction_slot_eq, ":cur_kingdom_marshall_faction", slot_faction_active_theater, ":faction_theater"),
           (this_or_next|eq, ":besieged_faction", ":faction_no"),
           (lt, ":dist", 100),
           (val_add, ":dist", 20),
           (try_begin), #TLD: large effect of different active theaters, but still allowed for more random fun
             (neg|faction_slot_eq, ":cur_kingdom_marshall_faction", slot_faction_active_theater, ":faction_theater"),
             (val_mul, ":dist", 200),
           (try_end),
           (val_div, ":attack_army_score", ":dist"),
           (gt, ":attack_army_score", ":best_attack_army_score"),
           (assign, ":best_attack_army", ":cur_kingdom_marshall_party"),
           (assign, ":best_attack_army_score", ":attack_army_score"),
         (try_end),
         (ge, ":best_attack_army", 0),
         #Army having with equal strength and 30 kms away will have a best_attack_army_score of 28
         (store_mul, ":chance_attacking_enemy_army", ":best_attack_army_score", 2),
         #(val_min, ":chance_attacking_enemy_army", 1500), #TLD - too big scores
         (assign, ":target_attacking_enemy_army", ":best_attack_army"),
         (try_begin),
           (eq, ":old_target_attacking_enemy_army", ":target_attacking_enemy_army"),
           (val_mul, ":chance_attacking_enemy_army", 100),
         (try_end),
       
         (val_mul, ":chance_attacking_enemy_army", ":offensive_rating"),
         (val_div, ":chance_attacking_enemy_army", 100),
       (try_end),
#Attacking enemies around center (defensive patrols)
       (try_begin),
         # MV commented out for 3.15: to lessen inactivity of weak factions
         #(gt, ":faction_strength", fac_str_very_weak), #TLD: was fac_str_weak - more defensive patrols by weak factions 
         #(neq, ":old_faction_ai_state", sfai_default), #MV: allow switching from defense to defensive patrols
         (gt, ":faction_marshall_party", 0),
         (assign, ":old_target_attacking_enemies_around_center", -1),
         (try_begin),
           (eq, ":old_faction_ai_state", sfai_attacking_enemies_around_center),
           (assign, ":old_target_attacking_enemies_around_center", ":old_faction_ai_object"),
         (try_end),
         
         (assign, ":best_attack_army_center", -1),
         (assign, ":best_attack_army_score", 0),
         (try_for_range, ":center_no", centers_begin, centers_end),
           (party_is_active, ":center_no"), #TLD
		   (party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
           (store_faction_of_party, ":center_faction", ":center_no"),
           #TLD: factions helping allies
           (store_relation, ":fac_rln", ":center_faction", ":faction_no"),
           (this_or_next|gt, ":fac_rln", 0),
           (eq, ":center_faction", ":faction_no"),
           
           #MV: make sure the center is in the active theater
           (party_slot_eq, ":center_no", slot_center_theater, ":faction_theater"),
           #(faction_slot_eq, ":center_faction", slot_faction_active_theater, ":faction_theater"),
           
           (party_get_slot, ":nearby_enemy_strength", ":center_no", slot_party_nearby_enemy_strength),
#MV test code begin
# (try_begin),
  # (eq, cheat_switch, 1),
  # #(this_or_next|eq, ":faction_no", "fac_gondor"),
  # (eq, ":faction_no", "fac_imladris"),
  # (assign, reg1, ":faction_marshall_army_strength"),
  # (assign, reg2, ":nearby_enemy_strength"),
  # (str_store_faction_name, s1, ":faction_no"),
  # (str_store_party_name, s2, ":center_no"),
  # (display_message, "@DEBUG: {s1} considers patroling around {s2}, marshall str:{reg1} enemy str:{reg2}.", 0x30FFC8),
# (try_end),
#MV test code end
           (store_mul, ":attack_army_score", ":nearby_enemy_strength", 1000),
           (val_div, ":attack_army_score", ":faction_marshall_army_strength"), 
           (try_begin),
             (gt, ":attack_army_score", 850),
             (store_sub, ":attack_army_score", 1700, ":attack_army_score"),
           (try_end),
           (this_or_next|gt, ":attack_army_score", 0),
           (eq, ":center_faction", ":faction_no"),
           (try_begin),
             (store_random_in_range, ":random_patrol", 0, 100),
             (lt, ":random_patrol", 50), #50%
             (val_max, ":attack_army_score", 5), #MV: always some small chance of patrol around home towns
           (try_end),
           (val_mul, ":attack_army_score", 4),
           (try_begin),
             # (party_slot_eq, ":center_no", slot_party_type, spt_village),
             # (try_begin),
               # (party_slot_eq, ":center_no", slot_village_state, svs_being_raided),
               # (val_mul, ":attack_army_score", 3),
             # (try_end),
           # (else_try),
             # (try_begin),
               (party_slot_ge, ":center_no", slot_center_is_besieged_by, 0),
               (val_mul, ":attack_army_score", 10),
             # (try_end),
           (try_end),
           (try_begin),
             (eq, ":old_target_attacking_enemies_around_center", ":center_no"),
             (val_mul, ":attack_army_score", 100),
           (try_end),
#MV test code begin
# (try_begin),
  # (eq, cheat_switch, 1),
  # #(this_or_next|eq, ":faction_no", "fac_gondor"),
  # (eq, ":faction_no", "fac_imladris"),
  # (assign, reg1, ":attack_army_score"),
  # (str_store_faction_name, s1, ":faction_no"),
  # (str_store_party_name, s2, ":center_no"),
  # (display_message, "@DEBUG: {s1} considers patroling around {s2}: attack score before distance: {reg1}.", 0x30FFC8),
# (try_end),
#MV test code end
           #(store_distance_to_party_from_party, ":dist", ":center_no", ":faction_marshall_party"),
           (call_script, "script_get_tld_distance", ":center_no", ":faction_marshall_party"),
           (assign, ":dist", reg0),
           (val_add, ":dist", 20),
           #(val_mul, ":dist", 10), #TLD: bigger effect of distance
           (val_div, ":attack_army_score", ":dist"),
#MV test code begin
# (try_begin),
  # (eq, cheat_switch, 1),
  # #(this_or_next|eq, ":faction_no", "fac_gondor"),
  # (eq, ":faction_no", "fac_imladris"),
  # (assign, reg1, ":attack_army_score"),
  # (assign, reg2, ":dist"),
  # (str_store_faction_name, s1, ":faction_no"),
  # (str_store_party_name, s2, ":center_no"),
  # (display_message, "@DEBUG: {s1} considers patroling around {s2}: attack score after distance: {reg1}, distance+20: {reg2}.", 0x30FFC8),
# (try_end),
#MV test code end
           (gt, ":attack_army_score", ":best_attack_army_score"),
           (assign, ":best_attack_army_center", ":center_no"),
           (assign, ":best_attack_army_score", ":attack_army_score"),
         (try_end),
         (ge, ":best_attack_army_center", 0),
#MV test code begin
# (try_begin),
  # (eq, cheat_switch, 1),
  # #(this_or_next|eq, ":faction_no", "fac_gondor"),
  # (eq, ":faction_no", "fac_imladris"),
  # (assign, reg1, ":best_attack_army_score"),
  # (str_store_faction_name, s1, ":faction_no"),
  # (str_store_party_name, s2, ":best_attack_army_center"),
  # (display_message, "@DEBUG: {s1} best patrol center is {s2} with attack score: {reg1}.", 0x30FFC8),
# (try_end),
#MV test code end
         #Center having enemies at equal strength and 30 kms away will have a best_attack_army_score of 56
         (store_mul, ":chance_attacking_enemies_around_center", ":best_attack_army_score", 2),
         (val_min, ":chance_attacking_enemies_around_center", 2000),
         (assign, ":target_attacking_enemies_around_center", ":best_attack_army_center"),
         (try_begin),
           (eq, ":old_target_attacking_enemies_around_center", ":target_attacking_enemies_around_center"),
           (val_mul, ":chance_attacking_enemies_around_center", 1000),
         (try_end),
       
         (val_mul, ":chance_attacking_enemies_around_center", ":offensive_rating"),
         (val_div, ":chance_attacking_enemies_around_center", 100),

         (try_begin),
           (gt, ":chance_attacking_enemies_around_center", ":chance_attacking_enemy_army"),
           (assign, ":end_cond", kingdoms_end),
           (try_for_range, ":cur_kingdom", kingdoms_begin, ":end_cond"),
             (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
             (faction_get_slot, ":cur_kingdom_marshall", ":cur_kingdom", slot_faction_marshall),
             (ge, ":cur_kingdom_marshall", 0),
             (troop_slot_eq, ":cur_kingdom_marshall", slot_troop_occupation, slto_kingdom_hero),
             (troop_get_slot, ":cur_kingdom_marshall_party", ":cur_kingdom_marshall", slot_troop_leaded_party),
             (ge, ":cur_kingdom_marshall_party", 0),
             (party_is_active, ":cur_kingdom_marshall_party"),
             (store_troop_faction, ":cur_kingdom_marshall_faction", ":cur_kingdom_marshall"),
             (store_relation, ":rel", ":cur_kingdom_marshall_faction", ":faction_no"),
             (lt, ":rel", 0),
             (store_distance_to_party_from_party, ":distance", ":cur_kingdom_marshall_party", ":target_attacking_enemies_around_center"),
             (lt, ":distance", 10),
             (assign, ":chance_attacking_enemy_army", ":chance_attacking_enemies_around_center"),
             (assign, ":target_attacking_enemy_army", ":cur_kingdom_marshall_party"),
             (assign, ":chance_attacking_enemies_around_center", 0),
             (assign, ":target_attacking_enemies_around_center", -1),
             (assign, ":end_cond", 0),#break
           (try_end),
         (try_end),
         
         #MV 3.15: prevent campaign cancellation while questing, or too soon
         (try_begin),
           (gt, ":chance_defend", 0), #any campaign can be cancelled
           (eq, "$players_kingdom", ":faction_no"),
#           (this_or_next|check_quest_active, "qst_follow_army"),
           (this_or_next|lt, ":offensive_hours", 3*24), #campaign can be cancelled after minimum of 3 days
           (this_or_next|check_quest_active, "qst_deliver_cattle_to_army"),
           (check_quest_active, "qst_scout_waypoints"),
           (assign, ":chance_defend", 0), #if the player is questing, don't cancel at all
         (try_end),


       (try_end),
          
       (assign, ":sum_weights", 0),
       (val_add, ":sum_weights", ":chance_defend"),
       (val_add, ":sum_weights", ":chance_gathering_army"),
       (val_add, ":sum_weights", ":chance_attacking_center"),
       (val_add, ":sum_weights", ":chance_raiding_village"),
       (val_add, ":sum_weights", ":chance_attacking_enemy_army"),
       (val_add, ":sum_weights", ":chance_attacking_enemies_around_center"),
       
       #MV 3.15: another attempt to avoid doing nothing
       (try_begin), #patrol around the capital
         (eq, ":sum_weights", 0),
         (assign, ":sum_weights", 1),
         (assign, ":chance_attacking_enemies_around_center", 1),
         (faction_get_slot, ":capital", ":faction_no", slot_faction_capital),
         (assign, ":target_attacking_enemies_around_center", ":capital"),
       (try_end),
#MV test code begin
# (try_begin),
  # (eq, cheat_switch, 1),
#  (this_or_next|eq, ":faction_no", "fac_gondor"),
  # (eq, ":faction_no", "fac_mordor"),
  # (assign, reg1, ":chance_defend"),
  # (assign, reg2, ":chance_gathering_army"),
  # (assign, reg3, ":chance_attacking_center"),
  # (assign, reg4, ":chance_attacking_enemy_army"),
  # (assign, reg5, ":chance_attacking_enemies_around_center"),
  # (str_store_faction_name, s1, ":faction_no"),
  # (display_message, "@DEBUG: {s1} chances: D:{reg1} GA:{reg2} AC:{reg3} AEA:{reg4} AEAC:{reg5}.", 0x30FFC8),
# (try_end),
#MV test code end
       
       (store_random_in_range, ":random_no", 0, ":sum_weights"),
       (val_sub, ":random_no", ":chance_defend"),
       (try_begin),
         (lt, ":random_no", 0),
         (faction_set_slot, ":faction_no", slot_faction_ai_state, sfai_default),
         (faction_set_slot, ":faction_no", slot_faction_ai_object, -1),
         (try_begin),
           (neq, ":old_faction_ai_state", sfai_default),
           (call_script, "script_check_and_finish_active_army_quests_for_faction", ":faction_no"),
           (faction_set_slot, ":faction_no", slot_faction_ai_last_offensive_time, ":cur_hours"),
         (try_end),
         (try_begin),
           (eq, cheat_switch, 1),
           (eq, ":faction_no", "fac_imladris"),
           (str_store_faction_name, s1, ":faction_no"),
           #(display_message, "@DEBUG: {s1} decided to do nothing."),
         (try_end),
       (else_try),
         (val_sub, ":random_no", ":chance_gathering_army"),
         (lt, ":random_no", 0),
         (faction_set_slot, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
         (faction_set_slot, ":faction_no", slot_faction_ai_object, -1),
         (try_begin),
           (neq, ":old_faction_ai_state", sfai_gathering_army),
           (faction_set_slot, ":faction_no", slot_faction_ai_last_offensive_time, ":cur_hours"),
           (faction_set_slot, ":faction_no", slot_faction_ai_offensive_max_followers, 1),
         (try_end),
         (try_begin),
           (eq, cheat_switch, 1),
           (eq, ":faction_no", "fac_imladris"),
           (str_store_faction_name, s1, ":faction_no"),
           #(display_message, "@DEBUG: {s1} decided to gather army."),
         (try_end),
       (else_try),
         (val_sub, ":random_no", ":chance_attacking_center"),
         (lt, ":random_no", 0),
         (faction_set_slot, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
         (faction_set_slot, ":faction_no", slot_faction_ai_object, ":target_attacking_center"),
         (try_begin),
           (gt, ":faction_marshall_num_followers", ":marshall_num_old_followers"),
           (faction_set_slot, ":faction_no", slot_faction_ai_offensive_max_followers, ":faction_marshall_num_followers"),
         (try_end),
         (try_begin),
           (eq, cheat_switch, 1),
           (eq, ":faction_no", "fac_imladris"),
           (str_store_faction_name, s1, ":faction_no"),
           (str_store_party_name, s2, ":target_attacking_center"),
           #(display_message, "@DEBUG: {s1} decided to besiege {s2}."),
         (try_end),
       (else_try),
         (val_sub, ":random_no", ":chance_attacking_enemy_army"),
         (lt, ":random_no", 0),
         (faction_set_slot, ":faction_no", slot_faction_ai_state, sfai_attacking_enemy_army),
         (faction_set_slot, ":faction_no", slot_faction_ai_object, ":target_attacking_enemy_army"),
         (try_begin),
           (gt, ":faction_marshall_num_followers", ":marshall_num_old_followers"),
           (faction_set_slot, ":faction_no", slot_faction_ai_offensive_max_followers, ":faction_marshall_num_followers"),
         (try_end),
         (try_begin),
           (eq, cheat_switch, 1),
           (eq, ":faction_no", "fac_imladris"),
           (str_store_faction_name, s1, ":faction_no"),
           (str_store_party_name, s2, ":target_attacking_enemy_army"),
           #(display_message, "@DEBUG: {s1} decided to attack {s2}."),
		  (assign, reg1, ":chance_defend"),
		  (assign, reg2, ":chance_gathering_army"),
		  (assign, reg3, ":chance_attacking_center"),
		  (assign, reg4, ":chance_attacking_enemy_army"),
		  (assign, reg5, ":chance_attacking_enemies_around_center"),
		  (str_store_faction_name, s1, ":faction_no"),
		  #(display_message, "@DEBUG: {s1} chances: D:{reg1} GA:{reg2} AC:{reg3} AEA:{reg4} AEAC:{reg5}.", 0x30FFC8), #mvdebug
         (try_end),
       (else_try),
         (val_sub, ":random_no", ":chance_attacking_enemies_around_center"),
         (lt, ":random_no", 0),
         (faction_set_slot, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
         (faction_set_slot, ":faction_no", slot_faction_ai_object, ":target_attacking_enemies_around_center"),
         (try_begin),
           (gt, ":faction_marshall_num_followers", ":marshall_num_old_followers"),
           (faction_set_slot, ":faction_no", slot_faction_ai_offensive_max_followers, ":faction_marshall_num_followers"),
         (try_end),
         (try_begin),
           (eq, cheat_switch, 1),
           (eq, ":faction_no", "fac_imladris"),
           (str_store_faction_name, s1, ":faction_no"),
           (str_store_party_name, s2, ":target_attacking_enemies_around_center"),
           #(display_message, "@DEBUG: {s1} decided to attack enemies around {s2}."),
         (try_end),
       (try_end),
       (try_begin),
         (eq, "$players_kingdom", ":faction_no"),
         (neg|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
         (check_quest_active, "qst_join_siege_with_army"),
         (call_script, "script_abort_quest", "qst_join_siege_with_army", 0),
       (try_end),
   (try_end),
  ]),

# script_party_calculate_and_set_nearby_friend_strength
# Input: party_no
# Output: none
("party_calculate_and_set_nearby_friend_strength",
    [ (store_script_param, ":party_no", 1),
      (assign, ":follower_strength", 0),
      (assign, ":friend_strength", 0),
      (assign, ":enemy_strength", 0),
      (store_faction_of_party, ":party_faction", ":party_no"),

      (store_add, ":end_cond", kingdom_heroes_end, 1),      
      (try_for_range, ":iteration", kingdom_heroes_begin, ":end_cond"),
        (try_begin),
          (eq, ":iteration", kingdom_heroes_end),
          (assign, ":cur_troop", "trp_player"),
        (else_try),
          (assign, ":cur_troop", ":iteration"),
        (try_end),
        (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
        (ge, ":cur_troop_party", 0),
        (party_is_active, ":cur_troop_party"),
        (neq, ":party_no", ":cur_troop_party"),
        (party_get_slot, ":str", ":cur_troop_party", slot_party_cached_strength),
        (try_begin),
          (party_get_slot, ":commander_party", ":cur_troop_party", slot_party_commander_party),
          (eq, ":commander_party", ":party_no"),
          (val_add, ":follower_strength", ":str"),
        (try_end),
        (store_distance_to_party_from_party, ":distance", ":cur_troop_party", ":party_no"),
        (lt, ":distance", 10),
        (store_troop_faction, ":army_faction", ":cur_troop"),
        (store_relation, ":rel", ":army_faction", ":party_faction"),
        (try_begin),
          (this_or_next|eq, ":army_faction", ":party_faction"),
          (gt, ":rel", 0),
          (val_add, ":friend_strength", ":str"),
        (else_try),
          (lt, ":rel", 0),
          (val_add, ":enemy_strength", ":str"),
        (try_end),
      (try_end),
      
      #MV: also calculate the strength of nearby faction patrols
      (try_for_parties, ":patrol"),
        (party_is_active, ":patrol"),
        (party_get_slot, ":party_type", ":patrol", slot_party_type), 
        (this_or_next|eq, ":party_type", spt_patrol),
        (this_or_next|eq, ":party_type", spt_raider),
        (eq, ":patrol", spt_scout),
        (store_distance_to_party_from_party, ":distance", ":patrol", ":party_no"),
        (lt, ":distance", 10),
        (party_get_slot, ":str", ":patrol", slot_party_cached_strength), #pre-calculated in script_init_ai_calculation
        (store_faction_of_party, ":patrol_faction", ":patrol"),
        (store_relation, ":rel", ":patrol_faction", ":party_faction"),
        (try_begin),
          (this_or_next|eq, ":patrol_faction", ":party_faction"),
          (gt, ":rel", 0),
          (val_add, ":friend_strength", ":str"),
        (else_try),
          (lt, ":rel", 0),
          (val_add, ":enemy_strength", ":str"),
        (try_end),
      (try_end),
      
      (party_set_slot, ":party_no", slot_party_follower_strength, ":follower_strength"),
      (party_set_slot, ":party_no", slot_party_nearby_friend_strength, ":friend_strength"),
      (party_set_slot, ":party_no", slot_party_nearby_enemy_strength, ":enemy_strength"),
      ]),

# script_faction_get_number_of_armies
# Input: arg1 = faction_no
# Output: reg0 = number_of_armies
  ("faction_get_number_of_armies",
   [  (store_script_param_1, ":faction_no"),
      (assign, ":num_armies", 0),
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (store_troop_faction, ":hero_faction_no", ":troop_no"),
        (eq, ":hero_faction_no", ":faction_no"),
        (troop_get_slot, ":hero_party", ":troop_no", slot_troop_leaded_party),
        (ge, ":hero_party", 0),
        (party_is_active, ":hero_party"), #MV
        (party_slot_eq, ":hero_party", slot_party_type, spt_kingdom_hero_party), # TLD: heroes alone don't count into army
        (call_script, "script_party_count_fit_regulars", ":hero_party"),
        (assign, ":party_size", reg0),
        (call_script, "script_party_get_ideal_size", ":hero_party"),
        (assign, ":ideal_size", reg0),
        (val_mul, ":ideal_size", 60),
        (val_div, ":ideal_size", 100),
        (gt, ":party_size", ":ideal_size"),
        (val_add, ":num_armies", 1),
      (try_end),
      (assign, reg0, ":num_armies"),
    ]),  
  
# script_faction_recalculate_strength
# Input: arg1 = faction_no
# Output: reg0 = strength
  ("faction_recalculate_strength",
   [  (store_script_param_1, ":faction_no"),
      (call_script, "script_faction_get_number_of_armies", ":faction_no"),
      (assign, ":num_armies", reg0),
      (assign, ":num_castles", 0),
      (assign, ":num_towns", 0),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_is_active, ":center_no"), #TLD
		(party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
        (store_faction_of_party, ":center_faction", ":center_no"),
        (eq, ":center_faction", ":faction_no"),
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_castle),
          (val_add, ":num_castles", 1),
        (else_try),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (val_add, ":num_towns", 1),
        (try_end),
      (try_end),

      (faction_set_slot, ":faction_no", slot_faction_num_armies, ":num_armies"),
      (faction_set_slot, ":faction_no", slot_faction_num_castles, ":num_castles"),
      (faction_set_slot, ":faction_no", slot_faction_num_towns, ":num_towns"),
    ]),  
  
# script_party_set_ai_state
# Input: arg1 = party_no, arg2 = new_ai_state, arg3 = action_object (if necessary)
# Output: none (Can fail)
("party_set_ai_state",
    [ (store_script_param, ":party_no", 1),
      (store_script_param, ":new_ai_state", 2),
      (store_script_param, ":new_ai_object", 3),

      (party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
      (party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),
      (party_get_attached_to, ":attached_to_party", ":party_no"),
      (assign, ":party_is_in_town", 0),
      (try_begin),
        (is_between, ":attached_to_party", centers_begin, centers_end),
        (assign, ":party_is_in_town", ":attached_to_party"),
      (try_end),

      (party_set_slot, ":party_no", slot_party_follow_me, 0),

      (try_begin),
        (eq, ":old_ai_state", ":new_ai_state"),
        (eq, ":old_ai_object", ":new_ai_object"),
        #do nothing. Nothing is changed.
      (else_try),
        (try_begin),
          (eq, ":new_ai_state", spai_accompanying_army),
          (party_set_ai_behavior, ":party_no", ai_bhvr_escort_party),
          (party_set_ai_object, ":party_no", ":new_ai_object"),
          (party_set_flags, ":party_no", pf_default_behavior, 0),
          (try_begin),
            (gt, ":party_is_in_town", 0),
            (party_detach, ":party_no"),
          (try_end),
        (else_try),
          (eq, ":new_ai_state", spai_besieging_center),
          (party_get_position, pos1, ":new_ai_object"),
          (map_get_random_position_around_position, pos2, pos1, 2),
          (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
          (party_set_ai_target_position, ":party_no", pos2),
          (party_set_ai_object, ":party_no", ":new_ai_object"),
          (party_set_flags, ":party_no", pf_default_behavior, 0),
          (party_set_slot, ":party_no", slot_party_follow_me, 1),
          (party_set_slot, ":party_no", slot_party_ai_substate, 0),
          (try_begin),
            (gt, ":party_is_in_town", 0),
            (neq, ":party_is_in_town", ":new_ai_object"),
            (party_detach, ":party_no"),
          (try_end),
        (else_try),
          (eq, ":new_ai_state", spai_holding_center),
          (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
          (party_set_ai_object, ":party_no", ":new_ai_object"),
          (party_set_flags, ":party_no", pf_default_behavior, 0),
          (try_begin),
            (gt, ":party_is_in_town", 0),
            (neq, ":party_is_in_town", ":new_ai_object"),
            (party_detach, ":party_no"),
          (try_end),
        (else_try),
          (eq, ":new_ai_state", spai_patrolling_around_center),
          (party_get_position, pos1, ":new_ai_object"),
          (map_get_random_position_around_position, pos2, pos1, 1),
          (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
          (party_set_ai_target_position, ":party_no", pos2),
          (party_set_ai_object, ":party_no", ":new_ai_object"),
          (party_set_ai_patrol_radius, ":party_no", 5),
          (party_set_flags, ":party_no", pf_default_behavior, 0),
          (party_set_slot, ":party_no", slot_party_follow_me, 1),
          (party_set_slot, ":party_no", slot_party_ai_substate, 0),
          (try_begin),
            (gt, ":party_is_in_town", 0),
            (party_detach, ":party_no"),
          (try_end),
        (else_try),
          (eq, ":new_ai_state", spai_recruiting_troops),
          (party_get_position, pos1, ":new_ai_object"),
          (map_get_random_position_around_position, pos2, pos1, 2),
          (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
          (party_set_ai_target_position, ":party_no", pos2),
          (party_set_ai_object, ":party_no", ":new_ai_object"),
          (party_set_flags, ":party_no", pf_default_behavior, 0),
          (party_set_slot, ":party_no", slot_party_ai_substate, 0),
          (try_begin),
            (gt, ":party_is_in_town", 0),
            (neq, ":party_is_in_town", ":new_ai_object"),
            (party_detach, ":party_no"),
          (try_end),
        (else_try),
          (eq, ":new_ai_state", spai_raiding_around_center),
          (party_get_position, pos1, ":new_ai_object"),
          (map_get_random_position_around_position, pos2, pos1, 1),
          (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_location),
          (party_set_ai_patrol_radius, ":party_no", 10),
          (party_set_ai_target_position, ":party_no", pos2),
          (party_set_ai_object, ":party_no", ":new_ai_object"),
          (party_set_flags, ":party_no", pf_default_behavior, 0),
          (party_set_slot, ":party_no", slot_party_follow_me, 1),
          (party_set_slot, ":party_no", slot_party_ai_substate, 0),
          (try_begin),
            (gt, ":party_is_in_town", 0),
            (neq, ":party_is_in_town", ":new_ai_object"),
            (party_detach, ":party_no"),
          (try_end),
        (else_try),
##          (eq, ":new_ai_state", spai_raiding_village),
##          (party_get_position, pos1, ":new_ai_object"),
##          (map_get_random_position_around_position, pos2, pos1, 1),
##          (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
##          (party_set_ai_target_position, ":party_no", pos2),
##          (party_set_ai_object, ":party_no", ":new_ai_object"),
##          (party_set_flags, ":party_no", pf_default_behavior, 0),
##          (party_set_slot, ":party_no", slot_party_follow_me, 1),
##          (try_begin),
##            (gt, ":party_is_in_town", 0),
##            (neq, ":party_is_in_town", ":new_ai_object"),
##            (party_detach, ":party_no"),
##          (try_end),
##        (else_try),
          (eq, ":new_ai_state", spai_engaging_army),
          (party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
          (party_set_ai_object, ":party_no", ":new_ai_object"),
          (party_set_flags, ":party_no", pf_default_behavior, 0),
          (try_begin),
            (gt, ":party_is_in_town", 0),
            (party_detach, ":party_no"),
          (try_end),
        (else_try),
          (eq, ":new_ai_state", spai_retreating_to_center),
          (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
          (party_set_ai_object, ":party_no", ":new_ai_object"),
          (party_set_flags, ":party_no", pf_default_behavior, 1),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
          (try_begin),
            (gt, ":party_is_in_town", 0),
            (neq, ":party_is_in_town", ":new_ai_object"),
            (party_detach, ":party_no"),
          (try_end),
        (else_try),
          (eq, ":new_ai_state", spai_undefined),
          (party_set_ai_behavior, ":party_no", ai_bhvr_hold),
          (party_set_flags, ":party_no", pf_default_behavior, 0),
        (try_end),
      (try_end),
      (party_set_slot, ":party_no", slot_party_ai_state, ":new_ai_state"),
      (party_set_slot, ":party_no", slot_party_ai_object, ":new_ai_object"),
]),

# script_party_decide_next_ai_state_under_command
# Input: arg1 = party_no
#called from triggers
("party_decide_next_ai_state_under_command",
    [ (store_script_param_1, ":party_no"),
      (party_get_slot, ":commander_party", ":party_no", slot_party_commander_party),
      (try_begin),
        (party_is_active, ":commander_party"),
        (party_get_slot, ":commander_ai_state", ":commander_party", slot_party_ai_state),
        (party_get_slot, ":commander_ai_object", ":commander_party", slot_party_ai_object),
        (store_faction_of_party, ":faction_no", ":party_no"),
        
        (store_distance_to_party_from_party, ":distance_to_commander", ":party_no", ":commander_party"),
        (try_begin),
          (gt, ":distance_to_commander", 5),
          (call_script, "script_party_set_ai_state", ":party_no", spai_accompanying_army, ":commander_party"),
        (else_try),
          (try_begin),
            (eq, ":commander_party", "p_main_party"),
            (call_script, "script_party_set_ai_state", ":party_no", spai_accompanying_army, "p_main_party"),
          (else_try),
            (eq, ":commander_ai_state", spai_besieging_center),
            (store_distance_to_party_from_party, ":distance_to_object", ":party_no", ":commander_ai_object"),
            (le, ":distance_to_object", 5),
            (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":commander_ai_object"),
          (else_try),
            #find current center
            (party_get_attached_to, ":cur_center_no", ":commander_party"),
            (assign, ":handled", 0),
            (try_begin),
              (lt, ":cur_center_no", 0),
              (party_get_cur_town, ":cur_center_no", ":commander_party"),
            (try_end),
            (try_begin),
              (eq, ":commander_ai_state", spai_holding_center),
              (call_script, "script_party_set_ai_state", ":party_no", spai_holding_center, ":commander_ai_object"),
              (assign, ":handled", 1),
            (else_try),
              (eq, ":commander_ai_state", spai_undefined),
              (is_between, ":cur_center_no", centers_begin, centers_end),
              (call_script, "script_party_set_ai_state", ":party_no", spai_holding_center, ":cur_center_no"),
              (assign, ":handled", 1),
            (try_end),
            (eq, ":handled", 1),
          (else_try),
            (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
            (ge, ":faction_marshall", 0),
            (troop_slot_eq, ":faction_marshall", slot_troop_leaded_party, ":commander_party"),
            (call_script, "script_party_set_ai_state", ":party_no", spai_accompanying_army, ":commander_party"),
          (else_try),
            (this_or_next|eq, ":commander_ai_state", spai_patrolling_around_center),
            (this_or_next|eq, ":commander_ai_state", spai_raiding_around_center),
            (eq, ":commander_ai_state", spai_engaging_army),
            (call_script, "script_party_set_ai_state", ":party_no", spai_accompanying_army, ":commander_party"),
          (else_try),
            #Commander doesn't need accompany. Cancel
            (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
            (party_set_slot, ":party_no", slot_party_commander_party, -1),
          (try_end),
        (try_end),
      (try_end),
]),

# script_kingdom_hero_decide_next_ai_state_follow_or_not
# Input: arg1 = troop_no
#called from triggers
("kingdom_hero_decide_next_ai_state_follow_or_not",
    [ (store_script_param_1, ":troop_no"),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      
      (try_begin),
        (party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),

        (assign, ":cancel", 0),
        (try_begin), #if we are retreating to a center keep retreating
          (eq, ":old_ai_state", spai_retreating_to_center),
          (neg|party_is_in_any_town, ":party_no"),
          (assign, ":cancel", 1),
        (try_end),
        (eq, ":cancel", 0),

        (party_get_slot, ":our_strength", ":party_no", slot_party_cached_strength),
        (store_div, ":min_strength_behind", ":our_strength", 2),

        (assign, ":under_siege", 0),
        #find current center
        (party_get_attached_to, ":cur_center_no", ":party_no"),
        (try_begin),
          (lt, ":cur_center_no", 0),
          (party_get_cur_town, ":cur_center_no", ":party_no"),
        (try_end),
        (try_begin),
          (neg|is_between, ":cur_center_no", centers_begin, centers_end),
          (assign, ":cur_center_no", -1),
          (assign, ":cur_center_nearby_strength", 0),
          (store_sub, ":cur_center_left_strength", 1000000),#must be higher than our strength
        (else_try),
          (party_get_slot, ":cur_center_nearby_strength", ":cur_center_no", slot_party_nearby_friend_strength),
          (store_sub, ":cur_center_left_strength", ":cur_center_nearby_strength", ":our_strength"),
          (party_get_slot, ":besieger_party", ":cur_center_no", slot_center_is_besieged_by),
          (gt, ":besieger_party", 0),
          (party_is_active, ":besieger_party"),
          (assign, ":under_siege", 1),
        (try_end),

        (store_troop_faction, ":faction_no", ":troop_no"),
        (faction_get_slot, ":faction_ai_state",  ":faction_no", slot_faction_ai_state),

        (party_get_slot, ":commander_party", ":party_no", slot_party_commander_party),
        (try_begin),
          (ge, ":commander_party", 0),
          (try_begin),
            (party_is_active, ":commander_party"),
            (try_begin),
              (store_faction_of_party, ":commander_faction", ":commander_party"),
              (neq, ":faction_no", ":commander_faction"),
              (assign, ":continue", 0),
              (try_begin),
                (neq, ":commander_party", "p_main_party"),
                (assign, ":continue", 1),
              (else_try),
                (neq, "$players_kingdom", ":faction_no"),
                (assign, ":continue", 1),
              (try_end),
              (eq, ":continue", 1),
              (assign, ":commander_party", -1),
            (try_end),
          (else_try),
            (assign, ":commander_party", -1),
          (try_end),
        (try_end),
      
        (faction_get_slot, ":num_towns", ":faction_no", slot_faction_num_towns),
        (store_mul, ":faction_center_value", ":num_towns", 2),
        (faction_get_slot, ":num_castles", ":faction_no", slot_faction_num_castles),
        (val_add, ":faction_center_value", ":num_castles"),
        (val_mul, ":faction_center_value", 10),
        (val_max, ":faction_center_value", 5),

        (troop_get_slot, ":readiness", ":troop_no", slot_troop_readiness_to_join_army),

        (assign, ":chance_to_follow_other_party", 0),
        (assign, ":target_to_follow_other_party", -1),
      
        (try_begin), #follow other party
          (eq, ":under_siege", 0),
          (ge, ":cur_center_left_strength", ":min_strength_behind"),
          (assign, ":continue", 0),
          (try_begin),
            (ge, ":commander_party", 0),
            (gt, "$party_relative_strength", 30),
            (assign, ":continue", 1),
          (else_try),
            (gt, "$party_relative_strength", 50),
            (lt, "$ratio_of_prisoners", 50),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (try_begin),
            (eq, ":faction_no", "fac_player_supporters_faction"),
            (neg|troop_slot_eq, ":troop_no", slot_troop_player_order_state, spai_undefined),
            (assign, ":continue", 0),
          (try_end),
          (eq, ":continue", 1),
          (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
          (ge, ":faction_marshall", 0),
          #(troop_slot_eq, ":faction_marshall", slot_troop_is_prisoner, 0),
          (neg|troop_slot_ge, ":faction_marshall", slot_troop_prisoner_of_party, 0),
          (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
          (neq, ":faction_marshall", ":troop_no"),
          (ge, ":faction_marshall_party", 0),
          (party_slot_eq, ":faction_marshall_party", slot_party_type, spt_kingdom_hero_party), # TLD: don't follow hostless kings
          (try_begin),
            (eq, ":faction_ai_state", sfai_gathering_army),
            (assign, ":old_target_to_follow_other_party", -1),
            (try_begin),
              (ge, ":commander_party", 0),
              (assign, ":old_target_to_follow_other_party", ":commander_party"),
            (try_end),

            (assign, ":continue", 0),
            (try_begin),
              (ge, ":readiness", 60),
              (assign, ":continue", 1),
            (else_try),
              (ge, ":readiness", 10),
              (eq, ":old_target_to_follow_other_party", ":faction_marshall_party"),
              (assign, ":continue", 1),
            (try_end),

            (try_begin),
              (eq, ":continue", 1),
              # (store_distance_to_party_from_party, ":dist", ":faction_marshall_party", ":party_no"),
              # (store_sub, ":chance", 120, ":dist"),
  # ##            (val_mul, ":chance", 3),
  # ##            (val_div, ":chance", 2),
              # (val_min, ":chance", 100),
              # (val_max, ":chance", 20),
#MV              (store_sub, ":faction_advantage_effect", "$g_average_center_value_per_faction", ":faction_center_value"),
#              (val_mul, ":faction_advantage_effect", 2),
#              (val_add, ":chance", ":faction_advantage_effect"),
#              (val_max, ":chance", 10),
              (assign, ":target_to_follow_other_party", ":faction_marshall_party"),
              (assign, ":chance_to_follow_other_party", 90), #MV: almost ALWAYS follow, regardless of distance
#              (assign, ":chance_to_follow_other_party", ":chance"),
              (try_begin),
                (eq, ":old_target_to_follow_other_party", ":target_to_follow_other_party"),
                (val_mul, ":chance_to_follow_other_party", 1000),
              (try_end),
            (try_end),
          (else_try),
            (this_or_next|eq, ":faction_ai_state", sfai_attacking_center),
#            (this_or_next|eq, ":faction_ai_state", sfai_raiding_village),
            (this_or_next|eq, ":faction_ai_state", sfai_attacking_enemies_around_center),
            (eq, ":faction_ai_state", sfai_attacking_enemy_army),
            (eq, ":commander_party", ":faction_marshall_party"),
            (ge, ":readiness", 10),
            (assign, ":target_to_follow_other_party", ":faction_marshall_party"),
            (assign, ":chance_to_follow_other_party", 100000),
          (try_end),
        (try_end),
        (try_begin), #follow other party with initiative
          (le, ":chance_to_follow_other_party", 0),
          (eq, ":under_siege", 0),
          (ge, ":cur_center_left_strength", ":min_strength_behind"),
          (assign, ":continue", 0),
          (try_begin),
            (ge, ":commander_party", 0),
            (gt, "$party_relative_strength", 40),
            (assign, ":continue", 1),
          (else_try),
            (gt, "$party_relative_strength", 75),
            (lt, "$ratio_of_prisoners", 50),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (try_begin),
            (eq, ":faction_no", "fac_player_supporters_faction"),
            (neg|troop_slot_eq, ":troop_no", slot_troop_player_order_state, spai_undefined),
            (neg|troop_slot_eq, ":troop_no", slot_troop_player_order_state, spai_accompanying_army),
            (assign, ":continue", 0),
          (try_end),
          (eq, ":continue", 1),
          (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),

          (assign, ":old_target_to_follow_other_party", -1),
          (try_begin),
            (ge, ":commander_party", 0),
            (assign, ":old_target_to_follow_other_party", ":commander_party"),
          (try_end),

          #(troop_get_slot, ":hero_renown", ":troop_no", slot_troop_renown), #MV: no renown influence on following marshalls
          (assign, ":num_available_to_follow", 0),
          (try_begin),
            (eq, "p_main_party", ":old_target_to_follow_other_party"),
            (val_add, ":num_available_to_follow", 1),
            (eq, "p_main_party", ":old_target_to_follow_other_party"),
            (val_add, ":num_available_to_follow", 999),
          (try_end),
          (try_for_range, ":other_hero", kingdom_heroes_begin, kingdom_heroes_end),
            (neq, ":other_hero", ":troop_no"),
            (store_troop_faction, ":troop_faction", ":other_hero"),
            (eq, ":troop_faction", ":faction_no"),
            (troop_get_slot, ":other_party", ":other_hero", slot_troop_leaded_party),
            (ge, ":other_party", 0),
            #(troop_get_slot, ":other_hero_renown", ":other_hero", slot_troop_renown),
            #(lt, ":hero_renown", ":other_hero_renown"),
            (neg|party_slot_ge, ":other_party", slot_party_commander_party, 0), #other party is not under command itself.
            #MV: disregard distance when deciding to follow - our map is too large for that kind of finesse, and we have too few lords per faction
            # (store_distance_to_party_from_party, ":dist", ":other_party", ":party_no"),
            # (lt, ":dist", 100), #was 25
            (party_slot_eq, ":other_party", slot_party_follow_me, 1),
            (val_add, ":num_available_to_follow", 1),
            (eq, ":other_party", ":old_target_to_follow_other_party"),
            (val_add, ":num_available_to_follow", 999),
          (try_end),
          (gt, ":num_available_to_follow", 0),
          (store_random_in_range, ":random_party_to_follow", 0, ":num_available_to_follow"),
          (try_begin),
            (eq, "p_main_party", ":old_target_to_follow_other_party"),
            (val_sub, ":random_party_to_follow", 1),
            (try_begin),
              (eq, "p_main_party", ":old_target_to_follow_other_party"),
              (val_sub, ":random_party_to_follow", 999),
            (try_end),
            (lt, ":random_party_to_follow", 0),
#MV            (store_mul, ":chance", 100, "$g_average_center_value_per_faction"),#this value is calculated at the beginning of the game
#            (val_div, ":chance", ":faction_center_value"),
#            (val_max, ":chance", 10),
            (assign, ":chance", 90), #MV: average
            (assign, ":chance_to_follow_other_party", ":chance"),
            (val_mul, ":chance_to_follow_other_party", 2),#trp_player is always the leader
            (assign, ":target_to_follow_other_party", "p_main_party"),
            (eq, ":old_target_to_follow_other_party", ":target_to_follow_other_party"),
            (val_mul, ":chance_to_follow_other_party", 100),
          (try_end),
          (try_for_range, ":other_hero", kingdom_heroes_begin, kingdom_heroes_end),
            (eq, ":target_to_follow_other_party", -1),
            (neq, ":other_hero", ":troop_no"),
            (store_troop_faction, ":troop_faction", ":other_hero"),
            (eq, ":troop_faction", ":faction_no"),
            (troop_get_slot, ":other_party", ":other_hero", slot_troop_leaded_party),
            (ge, ":other_party", 0),
            #(troop_get_slot, ":other_hero_renown", ":other_hero", slot_troop_renown),
            #(lt, ":hero_renown", ":other_hero_renown"),
            (neg|party_slot_ge, ":other_party", slot_party_commander_party, 0), #other party is not under command itself.
            #(store_distance_to_party_from_party, ":dist", ":other_party", ":party_no"),
            #(lt, ":dist", 25),
            (party_slot_eq, ":other_party", slot_party_follow_me, 1),
            (val_sub, ":random_party_to_follow", 1),
            (try_begin),
              (eq, ":other_party", ":old_target_to_follow_other_party"),
              (val_sub, ":random_party_to_follow", 999),
            (try_end),
            (lt, ":random_party_to_follow", 0),
            (store_mul, ":chance", 100, "$g_average_center_value_per_faction"),#this value is calculated at the beginning of the game
            (val_div, ":chance", ":faction_center_value"),
            (val_max, ":chance", 10),
            (assign, ":chance_to_follow_other_party", ":chance"),
            (try_begin),
              (faction_slot_eq, ":faction_no", slot_faction_leader, ":other_hero"),
              (val_mul, ":chance_to_follow_other_party", 2),
            (try_end),
            (assign, ":target_to_follow_other_party", ":other_party"),
            (eq, ":old_target_to_follow_other_party", ":target_to_follow_other_party"),
            (val_mul, ":chance_to_follow_other_party", 100),
          (try_end),
        (try_end),
        # TLD: lords without hosts have very low chances to follow
        (try_begin),
          (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_alone),
          (assign, ":chance_to_follow_other_party", 10),
        (try_end),
#MV test code begin
# (try_begin),
  # (eq, cheat_switch, 1),
  # (this_or_next|eq, ":faction_no", "fac_gondor"),
  # (eq, ":faction_no", "fac_mordor"),
  # (assign, reg1, ":chance_to_follow_other_party"),
  # (str_store_troop_name, s1, ":troop_no"),
  # (try_begin),
    # (neq, ":target_to_follow_other_party", -1),
    # (str_store_party_name, s2, ":target_to_follow_other_party"),
    # (display_message, "@DEBUG: {s1} chance to follow {s2}: {reg1}", 0x30FFC8),
# #  (else_try),
# #    (display_message, "@DEBUG: {s1} won't follow anyone", 0x30FFC8),
  # (try_end),
# (try_end),
#MV test code end
        # (assign, ":sum_chances", ":chance_to_follow_other_party"),
        # (val_add, ":sum_chances", 11), #MV: 10% chance won't follow if 100, was 600
        (store_random_in_range, ":random_no", 0, 100), #MV: normalized chance to mean probability
        (try_begin),
          # (val_sub, ":random_no", ":chance_to_follow_other_party"),
          (lt, ":random_no", ":chance_to_follow_other_party"),
          (party_set_slot, ":party_no", slot_party_commander_party, ":target_to_follow_other_party"),
        (else_try),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (try_end),
      (try_end),
]),
  
# script_kingdom_hero_decide_next_ai_state
# Input: arg1 = troop_no
#called from triggers
("kingdom_hero_decide_next_ai_state",
    [ (store_script_param_1, ":troop_no"),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),

      (try_begin),
        (party_get_slot, ":our_strength", ":party_no", slot_party_cached_strength),
        (store_div, ":min_strength_behind", ":our_strength", 2),
        (party_get_slot, ":our_follower_strength", ":party_no", slot_party_follower_strength),

        (store_troop_faction, ":faction_no", ":troop_no"),
        (faction_get_slot, ":faction_theater", ":faction_no", slot_faction_active_theater), #TLD

        #find current center
        (assign, ":besieger_party", -1),
        (party_get_attached_to, ":cur_center_no", ":party_no"),
        (try_begin),
          (lt, ":cur_center_no", 0),
          (party_get_cur_town, ":cur_center_no", ":party_no"),
        (try_end),
		
        (try_begin),
          (neg|is_between, ":cur_center_no", centers_begin, centers_end),
          (assign, ":cur_center_no", -1),
          (assign, ":cur_center_nearby_strength", 0),
          (store_sub, ":cur_center_left_strength", 1000000),#must be higher than our strength
        (else_try),
          (party_get_slot, ":cur_center_nearby_strength", ":cur_center_no", slot_party_nearby_friend_strength),
          (store_sub, ":cur_center_left_strength", ":cur_center_nearby_strength", ":our_strength"),
          (party_get_slot, ":besieger_party", ":cur_center_no", slot_center_is_besieged_by),
          (try_begin),
            (neg|party_is_active, ":besieger_party"),
            (assign, ":besieger_party", -1),
          (try_end),
          (store_faction_of_party, ":cur_center_faction", ":cur_center_no"),
          (store_relation, ":cur_center_relation", ":cur_center_faction", ":faction_no"),
        (try_end),

        (party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
        (party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),

        (assign, ":cancel", 0),
        (try_begin), #if we are retreating to a center keep retreating
          (eq, ":old_ai_state", spai_retreating_to_center),
          (neg|party_is_in_any_town, ":party_no"),
          (assign, ":cancel", 1),
        (try_end),
        (eq, ":cancel", 0),

##        (faction_get_slot, ":faction_ai_state",  ":faction_no", slot_faction_ai_state),
##        (faction_get_slot, ":faction_ai_object", ":faction_no", slot_faction_ai_object),

        (faction_get_slot, ":num_towns", ":faction_no", slot_faction_num_towns),
        (store_mul, ":faction_center_value", ":num_towns", 2),
        (faction_get_slot, ":num_castles", ":faction_no", slot_faction_num_castles),
        (val_add, ":faction_center_value", ":num_castles"),
        (val_mul, ":faction_center_value", 10),
        (val_max, ":faction_center_value", 5),

        (assign, ":chance_move_to_home_center", 0),
        (assign, ":target_move_to_home_center", -1),
        (assign, ":chance_move_to_other_center", 0),
        (assign, ":target_move_to_other_center", -1),
        (assign, ":chance_besiege_enemy_center", 0),
        (assign, ":target_besiege_enemy_center", -1),
        (assign, ":chance_patrol_around_center", 0),
        (assign, ":target_patrol_around_center", -1),
        (assign, ":chance_raid_around_center", 0),
        (assign, ":target_raid_around_center", -1),
        (assign, ":chance_recruit_troops", 0),
        (assign, ":target_recruit_troops", -1),
#Moving to home center
        (try_begin),
          (eq, ":besieger_party", -1),
          (assign, ":old_target_move_to_home_center", -1),
          (try_begin),
            (eq, ":old_ai_state", spai_holding_center),
            (assign, ":old_target_move_to_home_center", ":old_ai_object"),
          (try_end),
          (try_begin),
            (is_between, ":cur_center_no", centers_begin, centers_end), #already in our center
            (assign, ":target_move_to_home_center", ":cur_center_no"),
            (assign, ":chance_move_to_home_center", 100),
          (try_end),
          (try_begin),
            (eq, ":target_move_to_home_center", -1),
            (this_or_next|gt, "$party_relative_strength", 20),#stay inside if strength is too low
            (eq, ":cur_center_no", -1),
            (ge, ":cur_center_left_strength", ":min_strength_behind"),#stay inside if center strength is too low
            (call_script, "script_cf_troop_get_random_leaded_walled_center_with_less_strength_priority", ":troop_no", ":old_target_move_to_home_center"),#Can fail
            (assign, ":target_move_to_home_center", reg0),
            (assign, ":chance_move_to_home_center", 50),
            (try_begin),
              (eq, ":old_target_move_to_home_center", ":target_move_to_home_center"),
              (val_mul, ":chance_move_to_home_center", 100),
            (try_end),
          (try_end),
        (try_end),
#Moving to other center
        (try_begin),
          (try_begin),
            (ge, ":besieger_party", 0),
            (ge, ":cur_center_relation", 0),
            (assign, ":chance_move_to_other_center", 50000),
            (assign, ":target_move_to_other_center", ":cur_center_no"),
          (else_try),
            (assign, ":old_target_move_to_other_center", -1),
            (try_begin),
              (eq, ":old_ai_state", spai_holding_center),
              (assign, ":old_target_move_to_other_center", ":old_ai_object"),
            (try_end),

            (try_begin),
              (eq, ":target_move_to_other_center", -1),
              (try_begin),
                (this_or_next|le, "$party_relative_strength", 20),#stay inside if strength is too low
                (lt, ":cur_center_left_strength", ":min_strength_behind"),#stay inside if center strength is too low
                (is_between, ":cur_center_no", centers_begin, centers_end),
                (ge, ":cur_center_relation", 0),
                (assign, ":chance_move_to_other_center", 500),
                (assign, ":target_move_to_other_center", ":cur_center_no"),
              (else_try),
                (call_script, "script_cf_select_random_walled_center_with_faction_and_less_strength_priority", ":faction_no", ":old_target_move_to_other_center"),
                (assign, ":target_move_to_other_center", reg0),
                (assign, ":chance_move_to_other_center", 10),
                (try_begin),
                  (eq, ":old_target_move_to_other_center", ":target_move_to_other_center"),
                  (val_mul, ":chance_move_to_other_center", 1000),
                (try_end),
              (try_end),
            (try_end),
          (try_end),
        (try_end),
        (try_begin),
          (lt, "$party_relative_strength", 50),
          (store_sub, ":factor", 100, "$party_relative_strength"),
          (try_begin),
            (gt, ":chance_move_to_home_center", 0),
            (val_mul, ":chance_move_to_home_center", 200),
            (val_div, ":chance_move_to_home_center", ":factor"),
          (else_try),
            (val_mul, ":chance_move_to_other_center", 200),
            (val_div, ":chance_move_to_other_center", ":factor"),
          (try_end),
        (try_end),
        (try_begin),
          (gt,  "$ratio_of_prisoners", 50),
          (try_begin),
            (gt, ":chance_move_to_home_center", 0),
            (val_mul, ":chance_move_to_home_center", 2),
          (else_try),
            (val_mul, ":chance_move_to_other_center", 2),
          (try_end),
        (try_end),

#besiege center
        (try_begin), 
          #(eq,1,0), # no sieges so far, GA #MV: yes, sieges
          (eq, ":besieger_party", -1),
          (ge, ":cur_center_left_strength", ":min_strength_behind"),#stay inside if center strength is too low
          (assign, ":continue", 0),
	  (party_get_num_companions, ":party_size", ":party_no"), # CC Bugfix: Need at least tld_siege_min_party_size troops to siege
	  (gt, ":party_size", tld_siege_min_party_size), 
          (try_begin),
            (eq, ":old_ai_state", spai_besieging_center),
            (gt, "$party_relative_strength", 30),
            (assign, ":continue", 1),
          (else_try),
            (gt, "$party_relative_strength", 75),
            (lt, "$ratio_of_prisoners", 50),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),

          (assign, ":our_estimated_str", ":our_follower_strength"),
          (val_add, ":our_estimated_str", ":our_strength"),

          (assign, ":old_target_besiege_enemy_center", -1),
          (try_begin),
            (eq, ":old_ai_state", spai_besieging_center),
            (assign, ":old_target_besiege_enemy_center", ":old_ai_object"),
          (try_end),

          (assign, ":best_besiege_center", -1),
          (assign, ":best_besiege_center_score", 0),
          (try_for_range, ":enemy_walled_center", centers_begin, centers_end),
            (party_is_active, ":enemy_walled_center"), #TLD
            (party_slot_eq, ":enemy_walled_center", slot_center_destroyed, 0), #TLD
            #MV: make sure the center is in the active theater
            (party_slot_eq, ":enemy_walled_center", slot_center_theater, ":faction_theater"),
            
            (party_get_slot, ":other_besieger_party", ":enemy_walled_center", slot_center_is_besieged_by),
            (assign, ":besieger_own_faction", 0),
            (try_begin),
              (ge, ":other_besieger_party", 0),
              (party_is_active, ":other_besieger_party"),
              (store_faction_of_party, ":besieger_faction", ":other_besieger_party"),
              (eq, ":besieger_faction", ":faction_no"),
              (assign, ":besieger_own_faction", 1),
            (try_end),
            (this_or_next|eq, ":other_besieger_party", -1),
            (eq, ":besieger_own_faction", 1),
            (call_script, "script_get_center_faction_relation_including_player", ":enemy_walled_center", ":faction_no"),
            (assign, ":reln", reg0),
            (lt, ":reln", 0),
            (val_mul, ":reln", -1),
            (val_add, ":reln", 50),
            #(store_distance_to_party_from_party, ":dist", ":enemy_walled_center", ":party_no"),
            (call_script, "script_get_tld_distance", ":enemy_walled_center", ":party_no"),
            (assign, ":dist", reg0),
            (store_sub, ":dist_factor", 75, ":dist"),
            (val_max, ":dist_factor", 3),
            (party_get_slot, ":center_str", ":enemy_walled_center", slot_party_cached_strength),
            (party_get_slot, ":center_near_str", ":enemy_walled_center", slot_party_nearby_friend_strength),
            (val_add, ":center_str", ":center_near_str"),

            (store_mul, ":relative_center_str", ":center_str", 100),
            (val_div, ":relative_center_str", ":our_estimated_str"),
            (store_sub, ":center_score", 1000, ":relative_center_str"),
            (val_max, ":center_score", 1),

            (val_mul, ":center_score", ":reln"),
            (val_mul, ":center_score", ":dist_factor"),
            
            (try_begin),
              (party_slot_eq, ":enemy_walled_center", slot_town_lord, "trp_player"),
              (call_script, "script_troop_get_player_relation", ":troop_no"),
              (assign, ":player_relation", reg0),
              #(troop_get_slot, ":player_relation", ":troop_no", slot_troop_player_relation),
              (lt, ":player_relation", 0),
              (store_sub, ":multiplier", 50, ":player_relation"),
              (val_mul, ":center_score", ":multiplier"),
              (val_div, ":center_score", 50),
            (try_end),

            (try_begin),
              (eq, ":enemy_walled_center", ":old_target_besiege_enemy_center"),
              (val_mul, ":center_score", 100),
            (try_end),
            (try_begin),
              (gt, ":center_score", ":best_besiege_center_score"),
              (assign, ":best_besiege_center_score", ":center_score"),
              (assign, ":best_besiege_center", ":enemy_walled_center"),
            (try_end),
          (try_end),
      
          (ge, ":best_besiege_center", 0),
          (assign, ":chance_besiege_enemy_center", 20),
          (assign, ":target_besiege_enemy_center", ":best_besiege_center"),
          (try_begin),
            (eq, ":old_target_besiege_enemy_center", ":target_besiege_enemy_center"),
            (val_mul, ":chance_besiege_enemy_center", 100),
          (try_end),
        (try_end),
#patrol alarmed center
        (try_begin), 
          (eq, ":besieger_party", -1),
          (ge, ":cur_center_left_strength", ":min_strength_behind"),#stay inside if center strength is too low
          (ge, "$party_relative_strength", 60),
          (try_begin),
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_patrolling_around_center),
            (party_get_slot, ":target_patrol_around_center", ":party_no", slot_party_ai_object),
          (try_end),

          (assign, ":old_target_patrol_around_center", -1),
          (try_begin),
            (eq, ":old_ai_state", spai_patrolling_around_center),
            (assign, ":old_target_patrol_around_center", ":old_ai_object"),
          (try_end),

          (assign, ":best_patrol_score", 0),
          (assign, ":best_patrol_target", -1),
          (try_for_range, ":center_no", centers_begin, centers_end), #find closest center that has spotted enemies.
            (party_is_active, ":center_no"), #TLD
			(party_slot_eq, ":center_no", slot_center_destroyed, 0), #TLD
            (store_faction_of_party, ":center_faction", ":center_no"),
            (eq, ":center_faction", ":faction_no"),
            #(store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
            (call_script, "script_get_tld_distance", ":party_no", ":center_no"),
            (assign, ":distance", reg0),
            (store_sub, ":this_center_score", 100, ":distance"),
            (val_max, ":this_center_score", 1),
            (try_begin),
              (party_slot_ge, ":center_no", slot_center_last_spotted_enemy, 0),
              (val_mul, ":this_center_score", 100),
            (try_end),
            (try_begin),
              (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
              (val_mul, ":this_center_score", 2),
            (try_end),
            (try_begin),
              (eq, ":center_no", ":old_target_patrol_around_center"),
              (val_mul, ":this_center_score", 1000),
            (try_end),
            (try_begin),
              (gt, ":this_center_score", ":best_patrol_score"),
              (assign, ":best_patrol_score", ":this_center_score"),
              (assign, ":best_patrol_target", ":center_no"),
            (try_end),
          (try_end),
          (try_begin),
            (gt, ":best_patrol_score", 0),
            (assign, ":target_patrol_around_center", ":best_patrol_target"),
          (try_end),
          (try_begin),
             (is_between, ":target_patrol_around_center", centers_begin, centers_end),
             (assign, ":chance_patrol_around_center", 80),
          (try_end),
          (try_begin),
            (troop_slot_ge, ":troop_no", slot_troop_change_to_faction, 1),
            (val_mul, ":chance_patrol_around_center", 10),
          (try_end),
          (try_begin),
             (eq, ":old_target_patrol_around_center", ":target_patrol_around_center"),
             (val_mul, ":chance_patrol_around_center", 100),
          (try_end),
        (try_end),

##        (try_begin), #cancel actions
##          (party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
##          (party_get_slot, ":ai_object", ":party_no", slot_party_ai_object),
##          (neq, ":ai_state", spai_undefined),
##          (assign, ":cancel_cur_action", 0),
##          (try_begin),
##            (eq, ":ai_state", spai_patrolling_around_center),
##            (neg|party_slot_ge, ":ai_object", slot_center_last_spotted_enemy, 0),
##            (store_random_in_range, ":rand", 0, 100),
##            (lt, ":rand", 25),
##            (assign, ":cancel_cur_action", 1),
##          (else_try),
##            (this_or_next|eq, ":ai_state", spai_besieging_center),
##            (eq, ":ai_state", spai_raiding_around_center),
##            (store_faction_of_party, ":ai_object_faction", ":ai_object"),
##            (store_relation, ":ai_object_relation", ":ai_object_faction", ":faction_no"),
##            (ge, ":ai_object_relation", 0),
##            (assign, ":cancel_cur_action", 1),
##          (try_end),
##          (eq, ":cancel_cur_action", 0),
##          (assign, ":chance_stay", 100),
##        (try_end),
      
##        (try_begin),
##          (eq, ":siege_going_badly", 1),
##          (assign, ":chance_besiege_enemy_center", 0),
##          (assign, ":chance_stay", 0),
##        (try_end),
##        (try_begin),
##          (eq, ":siege_going_well", 1),
##          (assign, ":chance_move_to_home_center", 0),
##          (assign, ":chance_move_to_other_center", 0),
##          (assign, ":chance_patrol_around_center", 0),
##          (assign, ":chance_besiege_enemy_center", 0),
##          (assign, ":chance_help_besieged_center", 0),
##        (try_end),

# no village raids or sieges so far, GA
        (assign, ":chance_besiege_enemy_center", 0),
        (assign, ":chance_raid_around_center", 0),
##########################################
		
        (assign, ":sum_chances", ":chance_move_to_home_center"),
        (val_add, ":sum_chances", ":chance_move_to_other_center"),
#        (val_add, ":sum_chances", ":chance_recruit_troops"),
#        (val_add, ":sum_chances", ":chance_raid_around_center"),
        (val_add, ":sum_chances", ":chance_besiege_enemy_center"),
        (val_add, ":sum_chances", ":chance_patrol_around_center"),
##        (val_add, ":sum_chances", ":chance_stay"),
        (val_max, ":sum_chances", 1),
        (store_random_in_range, ":random_no", 0, ":sum_chances"),
        (try_begin),
          (val_sub, ":random_no", ":chance_move_to_home_center"),
          (lt, ":random_no", 0),
          (call_script, "script_party_set_ai_state", ":party_no", spai_holding_center, ":target_move_to_home_center"),
          (party_set_flags, ":party_no", pf_default_behavior, 1),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (else_try),
          (val_sub, ":random_no", ":chance_move_to_other_center"),
          (lt, ":random_no", 0),
          (call_script, "script_party_set_ai_state", ":party_no", spai_holding_center, ":target_move_to_other_center"),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (else_try),
          (eq,1,0), # village removal by MV
          (val_sub, ":random_no", ":chance_recruit_troops"),
          (lt, ":random_no", 0),
          (call_script, "script_party_set_ai_state", ":party_no", spai_recruiting_troops, ":target_recruit_troops"),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (else_try),
          (eq,1,0), # village removal by MV
          (val_sub, ":random_no", ":chance_raid_around_center"),
          (lt, ":random_no", 0),
          (call_script, "script_party_set_ai_state", ":party_no", spai_raiding_around_center, ":target_raid_around_center"),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (else_try),
          (val_sub, ":random_no", ":chance_besiege_enemy_center"),
          (lt, ":random_no", 0),
          (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":target_besiege_enemy_center"),
        (else_try),
          (val_sub, ":random_no", ":chance_patrol_around_center"),
          (lt, ":random_no", 0),
          (call_script, "script_party_set_ai_state", ":party_no", spai_patrolling_around_center, ":target_patrol_around_center"),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (else_try),
          (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (try_end),
      (try_end),
]),
  
# script_process_kingdom_parties_ai
# This is called more frequently than decide_kingdom_parties_ai
# Input: none
# Output: none
#called from triggers
("process_kingdom_parties_ai",
    [  (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),  # hero not prisoner and has party
         (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
           (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
           (gt, ":party_no", 0),
             (call_script, "script_process_hero_ai", ":troop_no"),
       (try_end),
]),
  
# script_process_hero_ai
# This is called more frequently than script_decide_kingdom_party_ais
#called from triggers
("process_hero_ai",
    [ (store_script_param_1, ":troop_no"),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (try_begin),
        (party_is_active, ":party_no"),
        (store_faction_of_party, ":faction_no", ":party_no"),
        (party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
        (party_get_slot, ":ai_object", ":party_no", slot_party_ai_object),
        (try_begin),
          (eq, ":ai_state", spai_besieging_center),
          (try_begin),
            (party_slot_eq, ":ai_object", slot_center_is_besieged_by, -1),
	    (party_get_num_companions, ":party_size", ":party_no"),
	    (gt, ":party_size", tld_siege_min_party_size), # CC Bugfix: Need at least tld_siege_min_party_size troops to siege
            (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
            (lt, ":distance", 3),
            (try_begin),
              (party_slot_ge, ":party_no", slot_party_commander_party, 0),
              (party_get_slot, ":commander_party", ":party_no", slot_party_commander_party),
              (party_set_slot, ":ai_object", slot_center_is_besieged_by, ":commander_party"),
            (else_try),
              (party_set_slot, ":ai_object", slot_center_is_besieged_by, ":party_no"),
            (try_end),
            (store_current_hours, ":cur_hours"),
            (party_set_slot, ":ai_object", slot_center_siege_begin_hours, ":cur_hours"),

            (str_store_party_name_link, s1, ":ai_object"),
            (str_store_troop_name_link, s2, ":troop_no"),
            (str_store_faction_name_link, s3, ":faction_no"),
            (try_begin),
              (store_relation, ":rel", "$players_kingdom", ":faction_no"),
              (gt, ":rel", 0),
              (assign, ":news_color", color_good_news),
            (else_try),
              (assign, ":news_color", color_bad_news),
            (try_end),
            (display_log_message, "@{s1} has been besieged by {s2} of {s3}.", ":news_color"),
            (try_begin),
              (store_faction_of_party, ":ai_object_faction", ":ai_object"),
              (this_or_next|party_slot_eq, ":ai_object", slot_town_lord, "trp_player"),
              (eq, ":ai_object_faction", "fac_player_supporters_faction"),
              (call_script, "script_add_notification_menu", "mnu_notification_center_under_siege", ":ai_object", ":troop_no"),
            (try_end),
            (call_script, "script_village_set_state", ":ai_object", svs_under_siege),
            (assign, "$g_recalculate_ais", 1),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_recruiting_troops),
          (try_begin),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
            (lt, ":distance", 3),
            (store_current_hours, ":cur_hours"),
            (party_get_slot, ":substate", ":party_no", slot_party_ai_substate),
            (val_add, ":substate", 1),
            (party_set_slot, ":party_no", slot_party_ai_substate, ":substate"),
            (try_begin),
              (ge, ":substate", 4),
              (party_set_slot, ":party_no", slot_party_ai_substate, ":cur_hours"),
              (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
              (party_set_flags, ":party_no", pf_default_behavior, 0),
              (party_set_slot, ":party_no", slot_party_commander_party, -1),
              (party_get_slot, ":troop_type", ":ai_object", slot_center_npc_volunteer_troop_type),
              (party_get_slot, ":troop_amount", ":ai_object", slot_center_npc_volunteer_troop_amount),
              (party_set_slot, ":ai_object", slot_center_npc_volunteer_troop_amount, -1),
              (party_add_members, ":party_no", ":troop_type", ":troop_amount"),
            (try_end),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_retreating_to_center),
          (try_begin),
            (party_get_battle_opponent, ":enemy_party", ":party_no"),
            (ge, ":enemy_party", 0), #we are in a battle! we may be caught in a loop!
            (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_commander_party, -1),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_patrolling_around_center),
          (try_begin),
            (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
            (lt, ":distance", 3),
            (party_set_slot, ":party_no", slot_party_ai_substate, 1),
            (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_party),
            (party_set_ai_object, ":party_no", ":ai_object"),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_holding_center),
          (party_get_attached_to, ":cur_town", ":party_no"),
          (try_begin),          # Make the party sortie outside, so that it will drive away any enemies??
            (is_between, ":cur_town", centers_begin, centers_end),
            (assign, ":sortie_chance", 50),
            (try_begin),
              (party_get_attached_to, ":cur_town", ":party_no"),
              (party_slot_ge, ":party_no", slot_center_is_besieged_by, 0), #town is under siege
              (assign, ":sortie_chance", 5),
            (try_end),
            (store_random_in_range, ":rand", 0, 100),
            (lt, ":rand", ":sortie_chance"),
            (assign, ":enemies_nearby", 0),
            (call_script, "script_party_calculate_regular_strength", ":party_no"),
            (assign, ":our_strength", reg0),
            (try_for_range, ":enemy_hero", kingdom_heroes_begin, kingdom_heroes_end),
              (store_troop_faction, ":enemy_hero_faction", ":enemy_hero"),
              (store_relation, ":reln", ":enemy_hero_faction", ":faction_no"),
              (lt, ":reln", 0),
              (troop_get_slot, ":enemy_party", ":enemy_hero", slot_troop_leaded_party),
              (gt, ":enemy_party", 0),
              (party_is_active, ":enemy_party"),
              (store_distance_to_party_from_party, ":dist", ":enemy_party", ":party_no"),
              (lt, ":dist", 7),
              (call_script, "script_party_calculate_regular_strength", "p_collective_enemy"),
              (gt, reg0, ":our_strength"),
              (assign, ":enemies_nearby", 1),
            (try_end),
            (eq, ":enemies_nearby", 0),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":party_no", ":ai_object"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_detach, ":party_no"),
          (try_end),
        (try_end),
      (try_end),
]),
    
##########################################
# TLD War System Scripts (foxyman)
#
# script_find_closest_random_enemy_center_from_center
# Find the closest enemy center from current center
# Input: arg1 - center_no
# Output: reg0 - enemy_center_no
("find_closest_random_enemy_center_from_center", [
        (store_script_param, ":center_no", 1),
        (store_faction_of_party, ":faction", ":center_no"),
        (faction_get_slot, ":faction_theater", ":faction", slot_faction_active_theater),
        (assign, ":dist", 1000000000),
        (assign, ":result", -1),
        (try_for_range, ":cur_center", centers_begin, centers_end),
            (party_is_active, ":cur_center"), #TLD
			(party_slot_eq, ":cur_center", slot_center_destroyed, 0), #TLD
            (store_faction_of_party, ":cur_faction", ":cur_center"),
            (store_relation, ":rel", ":cur_faction", ":faction"),
            (lt, ":rel", 0),
            (party_slot_eq, ":cur_center", slot_center_theater, ":faction_theater"), #MV: must be in the active theater to make sense
            (call_script, "script_get_tld_distance", ":center_no", ":cur_center"),
            (assign, ":cur_dist", reg0),
            (lt, ":cur_dist", ":dist"),
            (store_random_in_range, ":rand", 0, 100),
            (lt, ":rand", 50), # 50% to not ignore (was 25%)
            (assign, ":dist", ":cur_dist"),
            (assign, ":result", ":cur_center"),
        (else_try),
            (lt, ":rel", 0),
            (eq, ":result", -1),
            (assign, ":result", ":cur_center"),
            (assign, ":dist", ":cur_dist"),
        (try_end),
        (assign, reg0, ":result"),
]),
    
# script_calc_mid_point
# calculate the middle piont on the segment between pos1 and pos2
# Input: pos1, pos2
# Output: pos1 - middle point
("calc_mid_point", [
        (set_fixed_point_multiplier, 100),
        (position_get_x, ":x1", pos1),
        (position_get_y, ":y1", pos1),
        (position_get_x, ":x2", pos2),
        (position_get_y, ":y2", pos2),
        (val_add, ":x1", ":x2"),
        (val_add, ":y1", ":y2"),
        (val_div, ":x1", 2),
        (val_div, ":y1", 2),
        (position_set_x, pos1, ":x1"),
        (position_set_y, pos1, ":y1"),        
]),

# script_calc_quarter_point
# calculate the quarter point on the segment between pos1 and pos2 (closer to pos1)
# Input: pos1, pos2
# Output: pos1 - quarter point
("calc_quarter_point", [
        (set_fixed_point_multiplier, 100),
        (position_get_x, ":x1", pos1),
        (position_get_y, ":y1", pos1),
        (position_get_x, ":x2", pos2),
        (position_get_y, ":y2", pos2),
        (store_sub, ":xdiff", ":x2", ":x1"),
        (store_sub, ":ydiff", ":y2", ":y1"),
        (val_div, ":xdiff", 4),
        (val_div, ":ydiff", 4),
        (val_add, ":x1", ":xdiff"),
        (val_add, ":y1", ":ydiff"),
        (position_set_x, pos1, ":x1"),
        (position_set_y, pos1, ":y1"),        
]),

# TLD War System Scripts end (foxyman)
##########################################

# script_calculate_troop_ai
# Input: troop_no
# Output: none
("calculate_troop_ai",
    [ (store_script_param, ":troop_no", 1),
      (try_begin),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(call_script, "script_cf_fails_if_sitting_king", ":troop_no"),		
		
        #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (gt, ":party_no", 0),
        (party_slot_eq, ":party_no", slot_party_following_player, 0),
        (store_faction_of_party, ":faction_no", ":party_no"),
        (assign, ":continue", 1),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"), # do not calculate AI if troop is marshall.
          (neg|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_default),
          (assign, ":continue", 0),
        (try_end),
        (try_begin),
          (store_current_hours, ":cur_time"),
          (party_slot_ge, ":party_no", slot_party_follow_player_until_time, ":cur_time"), # MV: don't calc if following orders by player
          (assign, ":continue", 0),
        (try_end),
        (eq, ":continue", 1),
        (call_script, "script_party_count_fit_for_battle", ":party_no"),
        (assign, ":party_fit_for_battle", reg0),
        (call_script, "script_party_get_ideal_size", ":party_no"),
        (assign, ":ideal_size", reg0),
        (store_mul, "$party_relative_strength", ":party_fit_for_battle", 100),
        (val_div, "$party_relative_strength", ":ideal_size"),
        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_num_towns, 0),
          (faction_slot_eq, ":faction_no", slot_faction_num_castles, 0),
          (assign, "$ratio_of_prisoners", 0), #do not let prisoners have an effect on ai calculation
        (else_try),
          (party_get_num_prisoners, ":num_prisoners", ":party_no"),
          (store_div, "$ratio_of_prisoners", ":num_prisoners", ":party_fit_for_battle"),
        (try_end),
        (call_script, "script_kingdom_hero_decide_next_ai_state_follow_or_not", ":troop_no"),
        (party_slot_eq, ":party_no", slot_party_commander_party, -1),
        (call_script, "script_kingdom_hero_decide_next_ai_state", ":troop_no"),
      (try_end),
]),

# script_calculate_troop_ai_under_command
# this computes what a party lead (by a given troop) will do, if it is following the command of another party
# Input: troop_no
# Output: none
("calculate_troop_ai_under_command",
    [ (store_script_param, ":troop_no", 1),
      (try_begin),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
		
		(call_script, "script_cf_fails_if_sitting_king", ":troop_no"),
		
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (gt, ":party_no", 0),
          (party_slot_ge, ":party_no", slot_party_commander_party, 0),
          (party_set_ai_initiative, ":party_no", 10), #MV: review this number, was 50
          (call_script, "script_party_decide_next_ai_state_under_command", ":party_no"),
      (try_end),
]),
  
# script_recalculate_ai_for_troop
# Input: troop id
("recalculate_ai_for_troop",
	[ (store_script_param, ":troop_no", 1),
	  (call_script, "script_init_ai_calculation"), 
	  (call_script, "script_calculate_troop_ai", ":troop_no"), 
	  (call_script, "script_calculate_troop_ai_under_command", ":troop_no"),
]),

# script_faction_strength_string_to_s23
# INPUT: faction ID
#OUTPUT: s23 contains name of faction strength
("faction_strength_string_to_s23",
    [ (store_script_param, ":faction_no", 1),
      (faction_get_slot,":strength",":faction_no",slot_faction_strength),
	  (val_add,":strength",999),
	  (val_div,":strength",1000),
	  (store_sub,":total_strings","str_faction_strength_last","str_faction_strength_crushed"),
	  (val_clamp,":strength",0,":total_strings"),
	  (val_add,":strength","str_faction_strength_crushed"),
      (str_store_string,s23,":strength"),
]),

# a simple script: 	give a troop, fails if that troop is a sitting king, i.e. a faction leader with a different faction marshal
("cf_fails_if_sitting_king", [
	(store_script_param, ":troop_no", 1),
	(store_troop_faction, ":faction_id", ":troop_no"),
	# leaders of factions which have a different marshal are SITTING KINGS.
	# they don't leave the place
	(this_or_next|faction_slot_eq,":faction_id",slot_faction_marshall,":troop_no"),
	(neg|faction_slot_eq,":faction_id",slot_faction_leader,":troop_no"),
]),

# script_create_kingdom_hero_party
# Input: arg1 = troop_no, arg2 = center_no
# Output: $pout_party = party_no
("create_kingdom_hero_party",
    [ (store_script_param, ":troop_no", 1),
      (store_script_param, ":center_no", 2),
      (store_troop_faction, ":troop_faction_no", ":troop_no"),
      (assign, "$pout_party", -1),
      (set_spawn_radius,0),
      (spawn_around_party,":center_no", "pt_kingdom_hero_party"),
      (assign, "$pout_party", reg0),
      (party_set_faction, "$pout_party", ":troop_faction_no"),
	  
	  # make it use the icon of the corresponding host (mtarini)
	  (store_sub, ":icon", ":troop_faction_no", "fac_gondor"),
	  (val_add, ":icon", "icon_knight_gondo_trot_x3"),  # exlpoit ordering of combined icons, with a few exception below:
	  (try_begin),(eq, ":troop_faction_no", "fac_beorn"),
		(assign, ":icon", "icon_generic_knight_x3"),
	  (else_try), (eq, ":troop_faction_no", "fac_gundabad"),
		(assign, ":icon", "icon_orc_tribal_x4"),
	  (else_try), (eq, ":troop_no", "trp_rohan_lord"),
		(assign, ":icon", "icon_theoden_x3"),
	  (try_end),
	  (party_set_icon, "$pout_party", ":icon"),
	    
	  
	# TLD faction specific party banners
	  (faction_get_slot,":cur_banner",":troop_faction_no",slot_faction_party_map_banner),
	# rohan gets somewhat random flags, for now (mtarini)
	  (try_begin),(eq,  ":troop_faction_no", "fac_rohan"),
		(neg|faction_slot_eq, ":troop_faction_no", slot_faction_leader, ":troop_no"), # not for kings
		(store_mod, ":tmp", ":troop_no", 6),
		(neq, ":tmp", 0),
		(val_sub, ":tmp", 1),
		(store_add, ":cur_banner", ":tmp", "icon_mfp_rohan_a"),  # alternative flag assigned( troopNO % 6 )
	  (try_end),
	# gondor gets flags specific of subfactions  (mtarini)
	  (try_begin),(eq,  ":troop_faction_no", "fac_gondor"),
		#(neg|faction_slot_eq, ":troop_faction_no", slot_faction_leader, ":troop_no"), # not for kings
		(party_get_slot, ":fief", ":center_no", slot_party_subfaction),
		(party_set_slot,"$pout_party", slot_party_subfaction, ":fief"), # assign subfaction of spawned party
		(neq,  ":fief", 0), # not for regulars
		(neq,  ":fief", subfac_rangers), # not for ithilien
		(store_add, ":cur_banner", "icon_mfp_pelargir", ":fief"),
		(val_sub, ":cur_banner", 1),  
	  (try_end),

      (call_script, "script_party_set_ai_state", "$pout_party", spai_undefined, -1),
      (troop_set_slot, ":troop_no", slot_troop_leaded_party, "$pout_party"),
      (party_add_leader, "$pout_party", ":troop_no"),
      (party_set_slot, "$pout_party", slot_party_commander_party, -1), #we need this because 0 is player's party!
      (party_set_slot, "$pout_party", slot_party_type, spt_kingdom_hero_alone), # TLD party type - lord w/o host
	  (party_set_slot, "$pout_party", slot_party_victory_value, ws_alone_vp), # TLD victory points for party kill
      (str_store_troop_name, s5, ":troop_no"),
      (party_set_name, "$pout_party", "str_s5_s_party"),
  # add bodyguards. Transformation of lord+guards to a host moved to simple triggers
	  (faction_get_slot,":guard",":troop_faction_no",slot_faction_prison_guard_troop),
      (try_begin),
        (faction_slot_eq, ":troop_faction_no", slot_faction_marshall, ":troop_no"),
        (faction_get_slot,":guard",":troop_faction_no",slot_faction_castle_guard_troop), # marshalls get elite guards
		(le, ":troop_faction_no", "fac_lorien"), # in all factions until lorien, no royal banners (mtarini)
		(neq,  ":troop_faction_no", "fac_gondor"), # not gondors
		(val_add, ":cur_banner", 1), # marshall get royal flags (mtarini)
      (try_end),
	  (store_random_in_range,":tmp",9,17),
	  (party_add_members,"$pout_party",":guard",":tmp"), 
	  (party_set_banner_icon, "$pout_party", ":cur_banner"),
	  (party_attach_to_party, "$pout_party", ":center_no")
]),

# script_decide_kingdom_party_ais
# Input: none
# Output: none
#called from triggers
("decide_kingdom_party_ais",
   [(try_begin),
      (ge,"$tld_war_began",1),  # party AI can change only if War started, GA
	  (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
         (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
         (neq, ":faction_no", "fac_player_supporters_faction"),
         (faction_get_slot, ":faction_ai_state", ":faction_no", slot_faction_ai_state),
         (neq, ":faction_ai_state", sfai_default),
         (faction_get_slot, ":faction_ai_object", ":faction_no", slot_faction_ai_object),
         (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
         (gt, ":faction_marshall", 0),
         (neq, ":faction_marshall", "trp_player"),
         (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
         (gt, ":faction_marshall_party", 0),
         (try_begin),
           (eq, ":faction_ai_state", sfai_gathering_army),
           (try_begin), #TLD: if there is an advance camp, travel there to gather your army
             (faction_get_slot, ":adv_camp", ":faction_no", slot_faction_advance_camp),
             (party_is_active, ":adv_camp"),
             (call_script, "script_party_set_ai_state", ":faction_marshall_party", spai_holding_center, ":adv_camp"),
           (else_try),
             (call_script, "script_party_set_ai_state", ":faction_marshall_party", spai_undefined, -1),
           (try_end),
           (party_set_ai_initiative, ":faction_marshall_party", 100),
         (else_try),
           (eq, ":faction_ai_state", sfai_attacking_center),
           (call_script, "script_party_set_ai_state", ":faction_marshall_party", spai_besieging_center, ":faction_ai_object"),
           (party_set_ai_initiative, ":faction_marshall_party", 0), #MV: was 50, but too much chasing breaks sieges
#         (else_try),
#           (eq, ":faction_ai_state", sfai_raiding_village),
#           (call_script, "script_party_set_ai_state", ":faction_marshall_party", spai_raiding_around_center, ":faction_ai_object"),
#           (party_set_ai_initiative, ":faction_marshall_party", 50),
         (else_try),
           (eq, ":faction_ai_state", sfai_attacking_enemies_around_center),
           (call_script, "script_party_set_ai_state", ":faction_marshall_party", spai_patrolling_around_center, ":faction_ai_object"),
           (party_set_ai_initiative, ":faction_marshall_party", 50),
         (else_try),
           (eq, ":faction_ai_state", sfai_attacking_enemy_army),
           (call_script, "script_party_set_ai_state", ":faction_marshall_party", spai_engaging_army, ":faction_ai_object"),
           (party_set_ai_initiative, ":faction_marshall_party", 50),
         (try_end),
         (party_set_slot, ":faction_marshall_party", slot_party_commander_party, -1),
      (try_end),

	# TLD decide if a lone lord spawns a host
	 # calculate number of alive hosts in each faction
	   (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
	      (faction_set_slot, ":faction_no", slot_faction_hosts, 0),
	   (try_end),
	   (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end), 
          (store_troop_faction, ":troop_faction_no", ":troop_no"),
		  (troop_get_slot, ":party", ":troop_no", slot_troop_leaded_party),
		  (gt,":party",0),
          (party_is_active, ":party"),
		  (party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_party),
		      (faction_get_slot, ":hosts", ":troop_faction_no", slot_faction_hosts),
			  (val_add,":hosts",1),
			  (faction_set_slot, ":troop_faction_no", slot_faction_hosts, ":hosts"),
	   (try_end),
	# host spawning conditions
       (try_for_range, ":hero", kingdom_heroes_begin, kingdom_heroes_end), # cycle through heros w/o hosts and try to spawn a host
		  (store_troop_faction, ":troop_faction_no", ":hero"),
          (faction_slot_eq, ":troop_faction_no", slot_faction_state, sfs_active),
          
	      (troop_get_slot, ":party", ":hero", slot_troop_leaded_party),
		  (gt,":party",0),
          (party_is_active, ":party"),
	      (party_slot_eq, ":party", slot_party_type, spt_kingdom_hero_alone), # if lonely hero

		  (faction_get_slot, ":hosts", ":troop_faction_no", slot_faction_hosts),
		  (faction_get_slot, ":strength", ":troop_faction_no", slot_faction_strength),
		  (val_div, ":strength", 1000), #MV: 3.15 tweak, was 1300 - to get more hosts
		  (val_add, ":strength", 1),
		  (lt, ":hosts", ":strength"), # faction passes strength check 

		  (store_random_in_range,":rnd",0,100),
          (this_or_next|faction_slot_eq, ":troop_faction_no", slot_faction_marshall, ":hero"), # marshall/king bypasses random check
		  (lt,":rnd",10),              # faction passes random check 

			(val_add, ":hosts",1),
            (faction_set_slot, ":troop_faction_no", slot_faction_hosts,":hosts"), # host is spawned
			
            (party_set_slot, ":party", slot_party_type, spt_kingdom_hero_party), # TLD party type changed to host
	        (party_set_slot, ":party", slot_party_victory_value, ws_host_vp), # TLD victory points for party kill
            (try_begin), #MV: double that for kings
              (faction_slot_eq, ":troop_faction_no", slot_faction_marshall, ":hero"),
              (party_set_slot, ":party", slot_party_victory_value, ws_host_vp*2),
            (try_end),
            (str_store_faction_name, s6, ":troop_faction_no"), # TLD host naming after faction
			(str_store_troop_name, s5, ":hero"),
			(str_store_troop_name_link, s7, ":hero"),
            #(party_set_name, ":party", "@Host of {s5}"),
            (party_set_name, ":party", "str_s5_s_host"),
		#	(display_message, "@{s7} has assumed the command of a {s6} host!", 0x87D7FF),
	     # hire troops to host, marshals (kings) get more
            (assign, ":num_tries", 30),
            (try_begin),
               (faction_slot_eq, ":troop_faction_no", slot_faction_marshall, ":hero"),
               (assign, ":num_tries", 50),
            (try_end),
            (try_for_range, ":unused", 0, ":num_tries"),
               (call_script, "script_hire_men_to_kingdom_hero_party", ":hero"),
            (try_end),
         # upgrade troops in party based on hero renown  
            (store_random_in_range, ":xp_rounds", 2, 6),
            (troop_get_slot, ":renown", ":hero", slot_troop_renown),
            (store_div, ":renown_xp_rounds", ":renown", 100),
            (val_add, ":xp_rounds", ":renown_xp_rounds"),
            (try_for_range, ":unused", 0, ":xp_rounds"),
               (call_script, "script_upgrade_hero_party", ":party", 4000),
            (try_end),
       (try_end),
	   
       (try_for_range, ":hero", kingdom_heroes_begin, kingdom_heroes_end),
         (store_troop_faction, ":troop_faction", ":hero"),
         (faction_slot_eq, ":troop_faction", slot_faction_state, sfs_active),
         (try_begin),
           (neg|faction_slot_eq, ":troop_faction", slot_faction_marshall, ":hero"),
           (troop_get_slot, ":troop_party", ":hero", slot_troop_leaded_party),
           (gt, ":troop_party", 0),
           (party_is_active, ":troop_party"),
           (party_set_ai_initiative, ":troop_party", 100), #MV: review this number
         (try_end),
         (call_script, "script_calculate_troop_ai", ":hero"),
       (try_end),

       (try_for_range, ":hero", kingdom_heroes_begin, kingdom_heroes_end),
         (call_script, "script_calculate_troop_ai_under_command", ":hero"),
       (try_end),
	(try_end),
]),
 
# script_update_active_theaters
# Input: none
# Output: none
# updates active theaters for all factions, called after a faction defeat
("update_active_theaters", [        
        # theater sequences: SE-SW-C-N, SW-SE-C-N, C-SW-N-SE, N-C-SW-SE
        (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
          (faction_slot_eq, ":faction", slot_faction_state, sfs_active),
          (faction_get_slot, ":faction_theater", ":faction", slot_faction_active_theater),
          (assign, ":theater_cleared", 1),
          (try_for_range, ":enemy_faction", kingdoms_begin, kingdoms_end),
            (faction_slot_eq, ":enemy_faction", slot_faction_state, sfs_active),
            (store_relation, ":rel", ":faction", ":enemy_faction"),
            (lt, ":rel", 0), # active enemy
            (faction_slot_eq, ":enemy_faction", slot_faction_active_theater, ":faction_theater"),
            (assign, ":theater_cleared", 0), # found active enemy faction in the same theater, do nothing
          (try_end),
          # find another theater with active enemies
          (try_begin),
            (eq, ":theater_cleared", 1),
            (assign, ":next_theater", ":faction_theater"),
            (assign, ":continue_loop", 4),
            (try_for_range, ":unused", 0, ":continue_loop"),
              #get the next theater in hardcoded theater sequences
              (call_script, "script_find_next_theater", ":faction", ":next_theater"),
              (assign, ":next_theater", reg0),
              (try_begin),
                (neq, ":next_theater", -1),
                (assign, ":theater_cleared", 1),
                # find enemies in the next theater
                (try_for_range, ":enemy_faction", kingdoms_begin, kingdoms_end),
                  (faction_slot_eq, ":enemy_faction", slot_faction_state, sfs_active),
                  (store_relation, ":rel", ":faction", ":enemy_faction"),
                  (lt, ":rel", 0), # active enemy
                  (faction_slot_eq, ":enemy_faction", slot_faction_active_theater, ":next_theater"),
                  (assign, ":theater_cleared", 0), # found active enemy faction in the same theater
                (try_end),
                # if enemies found, move active theater
                (try_begin),
                  (eq, ":theater_cleared", 0),
                  (faction_set_slot, ":faction", slot_faction_active_theater, ":next_theater"),
                  (assign, ":continue_loop", 0), # exit loop
                  (call_script, "script_theater_name_to_s15", ":next_theater"),
                  (str_store_faction_name, s2, ":faction"),
                  (try_begin),
                    (store_relation, ":rel", "$players_kingdom", ":faction"),
                    (gt, ":rel", 0),
                    (assign, ":news_color", color_good_news),
                  (else_try),
                    (assign, ":news_color", color_bad_news),
                  (try_end),
                  (display_log_message, "@The forces of {s2} march to {s15}!", ":news_color"),
                  
                  (store_current_hours, ":cur_hours"),
                  (faction_set_slot, ":faction", slot_faction_advcamp_timer, ":cur_hours"), #set the timer for camp creation

                  (faction_get_slot, ":adv_camp", ":faction", slot_faction_advance_camp),
                  #dismantle any existing camp, emptying it of lords
                  (try_begin),
                    (party_is_active, ":adv_camp"),
                    # detach all attached parties, in case there are parties in the camp
                    (party_get_num_attached_parties, ":num_attached_parties", ":adv_camp"),
                    (try_for_range_backwards, ":attached_party_rank", 0, ":num_attached_parties"),
                      (party_get_attached_party_with_rank, ":attached_party", ":adv_camp", ":attached_party_rank"),
                      (gt, ":attached_party", 0),
                      (party_is_active, ":attached_party"),
                      (party_detach, ":attached_party"),
                    (try_end),
			# CC: Remove volunteers from the adv. camp.
    			(party_get_slot, ":volunteers", ":adv_camp", slot_town_volunteer_pt),
    			(try_begin),
        			(gt, ":volunteers", 0),
        			(party_is_active, ":volunteers"),
        			(party_detach, ":volunteers"),
        			(remove_party, ":volunteers"),
			(try_end),
                    (disable_party, ":adv_camp"),
                  (try_end),
                                    
                  # any enemy in the theater that has an advance camp elsewhere should return to defend their home theater
                  (try_for_range, ":enemy_faction", kingdoms_begin, kingdoms_end),
                    (faction_slot_eq, ":enemy_faction", slot_faction_state, sfs_active),
                    (store_relation, ":rel", ":faction", ":enemy_faction"),
                    (lt, ":rel", 0), # active enemy
                    (faction_get_slot, ":home_theater", ":enemy_faction", slot_faction_home_theater),
                    (eq, ":home_theater", ":next_theater"),
                    (neg|faction_slot_eq, ":enemy_faction", slot_faction_active_theater, ":next_theater"),
                    (faction_set_slot, ":enemy_faction", slot_faction_active_theater, ":home_theater"), #reset to home
                    #dismantle advance camp and return
                    (faction_get_slot, ":enemy_adv_camp", ":enemy_faction", slot_faction_advance_camp),
                    (try_begin),
                      (party_is_active, ":enemy_adv_camp"),
                      (call_script, "script_destroy_center", ":enemy_adv_camp"),
                    (try_end),
                    (str_store_faction_name, s2, ":enemy_faction"),
                    (try_begin),
                      (store_relation, ":rel", "$players_kingdom", ":enemy_faction"),
                      (lt, ":rel", 0),
                      (assign, ":news_color", color_good_news),
                    (else_try),
                      (assign, ":news_color", color_bad_news),
                    (try_end),
                    (display_log_message, "@The hosts of {s2} march back to defend their homes!", ":news_color"),
                  (try_end),
                  
                (try_end),
              (else_try),
                # ERROR (or victory!)
                (assign, ":continue_loop", 0), # exit loop
                #(str_store_faction_name, s2, ":faction"),
                #(display_log_message, "@ERROR: Couldn't find a theater with enemies for {s2}.", 0xFF0000),
              (try_end),
            (try_end), # try_for_range, ":unused"
          (try_end), # end find another theater
        (try_end), # end update active theaters       
]),
 
# script_find_next_theater
# Input: faction, current theater
# Output: reg0 = theater_SE, theater_SW, theater_C, theater_N or -1 for error
# theater sequences: SE-SW-C-N, SW-SE-C-N, C-SW-N-SE, N-C-SW-SE
("find_next_theater", [
     (store_script_param, ":faction", 1),
     (store_script_param, ":active_theater", 2),
     (assign, ":next_theater", -1),
     (faction_get_slot, ":home_theater", ":faction", slot_faction_home_theater),
     #hardcoded theater sequences
     (try_begin),
       (eq, ":home_theater", theater_SE), # SE-SW-C-N
       (try_begin),(eq, ":active_theater", theater_SE),(assign, ":next_theater", theater_SW),
        (else_try),(eq, ":active_theater", theater_SW),(assign, ":next_theater", theater_C),
        (else_try),(eq, ":active_theater", theater_C ),(assign, ":next_theater", theater_N),
       (try_end),
     (else_try),
       (eq, ":home_theater", theater_SW), # SW-SE-C-N
       (try_begin),(eq, ":active_theater", theater_SW),(assign, ":next_theater", theater_SE),
        (else_try),(eq, ":active_theater", theater_SE),(assign, ":next_theater", theater_C),
        (else_try),(eq, ":active_theater", theater_C ),(assign, ":next_theater", theater_N),
       (try_end),
     (else_try),
       (eq, ":home_theater", theater_C), # C-SW-N-SE
       (try_begin),(eq, ":active_theater", theater_C ),(assign, ":next_theater", theater_SW),
        (else_try),(eq, ":active_theater", theater_SW),(assign, ":next_theater", theater_N),
        (else_try),(eq, ":active_theater", theater_N ),(assign, ":next_theater", theater_SE),
       (try_end),
     (else_try),
       (eq, ":home_theater", theater_N), # N-C-SW-SE
       (try_begin),(eq, ":active_theater", theater_N ),(assign, ":next_theater", theater_C),
        (else_try),(eq, ":active_theater", theater_C ),(assign, ":next_theater", theater_SW),
        (else_try),(eq, ":active_theater", theater_SW),(assign, ":next_theater", theater_SE),
       (try_end),
     (try_end),
     (assign, reg0, ":next_theater"),  
]),

# script_theater_name_to_s15
# Input: theater
# Output: s15
("theater_name_to_s15",[
     (store_script_param, ":theater", 1),
     (str_store_string, s15, "@ERROR"),
     (try_begin),(eq, ":theater", theater_SE),(str_store_string, s15, "str_theater_SE"),
      (else_try),(eq, ":theater", theater_SW),(str_store_string, s15, "str_theater_SW"),
      (else_try),(eq, ":theater", theater_C ),(str_store_string, s15, "str_theater_C"),
      (else_try),(eq, ":theater", theater_N ),(str_store_string, s15, "str_theater_N"),
     (try_end),
]),
   
# script_get_advcamp_pos
# Gets a position of the advance camp in another theater (looks up faction active theater)
# Input: faction
# Output: pos1
# Uses pos2 and pos3
("get_advcamp_pos",[
     (store_script_param, ":faction", 1),
     
     (faction_get_slot, ":active_theater", ":faction", slot_faction_active_theater),
     (faction_get_slot, ":capital", ":faction", slot_faction_capital),
     
     (assign, ":center_party", "p_town_east_emnet"), # some default
     (try_begin),(eq, ":active_theater", theater_N ),(assign, ":center_party", "p_theater_N_center"),
      (else_try),(eq, ":active_theater", theater_C ),(assign, ":center_party", "p_theater_C_center"),
      (else_try),(eq, ":active_theater", theater_SW),(assign, ":center_party", "p_theater_SW_center"),
      (else_try),(eq, ":active_theater", theater_SE),(assign, ":center_party", "p_theater_SE_center"),
     (try_end),
     
     (party_get_position, pos2, ":capital"),
     (party_get_position, pos3, ":center_party"),     
     
     # Get a position at 80% of the way from the capital to the theater center point
     (set_fixed_point_multiplier, 100),
     (position_get_x, ":capital_xpos", pos2),
     (position_get_y, ":capital_ypos", pos2),
     (position_get_x, ":theater_xpos", pos3),
     (position_get_y, ":theater_ypos", pos3),
     
     # get the distance
     (store_sub, ":xdiff", ":theater_xpos", ":capital_xpos"),
     (store_sub, ":ydiff", ":theater_ypos", ":capital_ypos"),
     (store_mul, ":xdiffsquared", ":xdiff", ":xdiff"),
     (store_mul, ":ydiffsquared", ":ydiff", ":ydiff"),
     (store_add, ":whole_distance", ":xdiffsquared", ":ydiffsquared"),
     (store_sqrt, ":whole_distance", ":whole_distance"),
# (assign, reg1, ":xdiff"),
# (assign, reg2, ":ydiff"),
# (assign, reg3, ":whole_distance"),
# (display_message, "@DEBUG: diff {reg1}, {reg2} distance {reg3}."),
     
     # Calculate 20% from theater center and clamp it at 7-35 clicks (note: non-optimal code for readability)
     (assign, ":distance", ":whole_distance"),
     (val_mul, ":distance", 2), 
     (val_div, ":distance", 10),
     (val_clamp, ":distance", 7000, 35001),
     
     # Get the new scaled x,y differences
     (val_mul, ":xdiff", ":distance"),
     (val_div, ":xdiff", ":whole_distance"),
     (val_mul, ":ydiff", ":distance"),
     (val_div, ":ydiff", ":whole_distance"),

     # finally.. the ideal position
     (store_sub, ":ideal_xpos", ":theater_xpos", ":xdiff"),
     (store_sub, ":ideal_ypos", ":theater_ypos", ":ydiff"),
     
     # now find a suitable random position around the ideal point     
     (position_set_x, pos2, ":ideal_xpos"),
     (position_set_y, pos2, ":ideal_ypos"),
     #(set_fixed_point_multiplier, 1), #doesn't work!
     
     (assign, ":radius", 5),
     (assign, ":continue", 1),
     (try_for_range, ":tries", 0, 1000),
       (eq, ":continue", 1),
       (map_get_random_position_around_position, pos1, pos2, ":radius"), # random circle with 5+ clicks radius
       (assign, ":too_close", 0),
       # check for suitable terrain
       (try_begin),
         #use a fake party to check the terrain
         (spawn_around_party, "p_main_party", "pt_none"),
         (assign, ":fake_party", reg0),
         (party_set_position, ":fake_party", pos1),
         (party_get_current_terrain, ":terrain_type", ":fake_party"),
         (remove_party, ":fake_party"),
         #check for impassable terrain
         (this_or_next|eq, ":terrain_type", rt_water),
         (this_or_next|eq, ":terrain_type", rt_mountain),
         (this_or_next|eq, ":terrain_type", rt_river),
         (this_or_next|eq, ":terrain_type", rt_mountain_forest),
         (             gt, ":terrain_type", rt_desert_forest), # any custom types?
         (assign, ":too_close", 1), #exit loop, try again
       (try_end),
       # check if too close to another center
       (try_for_range, ":cur_center", centers_begin, centers_end),
         (eq, ":too_close", 0),
         (party_is_active, ":cur_center"), #TLD
		 (party_slot_eq, ":cur_center", slot_center_destroyed, 0), #TLD
         (store_faction_of_party, ":cur_faction", ":cur_center"),
         (store_relation, ":rel", ":cur_faction", ":faction"),
         (party_get_position, pos3, ":cur_center"),
         (get_distance_between_positions, ":cur_dist", pos1, pos3),
# (try_begin),
# (eq, ":faction", "fac_mordor"),
# (assign, reg3, ":cur_dist"),
# (str_store_party_name, s2, ":cur_center"),
# (display_message, "@DEBUG: camp distance from {s2}: {reg3}."),
# (try_end),
         (try_begin),
           (lt, ":cur_dist", 800), #at least 10(8 GA) clicks from enemy centers
           (this_or_next|lt, ":rel", 0),
           (lt, ":cur_dist", 400), #at least 5 (4 GA) clicks from friendly centers
           (assign, ":too_close", 1),
         (try_end),
       (try_end),
       (try_begin),
         (eq, ":too_close", 0),
         (assign, ":continue", 0),
       (else_try), # increase radius for every 5 unsuccessful tries
         (store_mod, ":tries_mod", ":tries", 5),
         (eq, ":tries_mod", 4),
         (val_add, ":radius", 1),
       (try_end),
     (try_end),     # out comes pos1
]),

# script_destroy_center
# Destroys a captured center (faction retreats if it's its last center in its active theater?)
# Input: center
# Output: none
# Note: Depends on the destroyable flag being set for advance camps
("destroy_center",[
	(store_script_param, ":center", 1),
	(store_faction_of_party, ":center_faction", ":center"),

    (party_set_slot, ":center", slot_center_is_besieged_by, -1),
    
    # first remove any volunteers
    (party_get_slot, ":volunteers", ":center", slot_town_volunteer_pt),
    (try_begin),
        (gt, ":volunteers", 0),
        (party_is_active, ":volunteers"),
        (party_detach, ":volunteers"),
        (remove_party, ":volunteers"),
	(try_end),
    
    # remove player's reserves, if player's capital is destroyed
    (try_begin),
      (faction_slot_eq, "$players_kingdom", slot_faction_capital, ":center"),
      (troop_get_slot, ":reserve_party", "trp_player", slot_troop_player_reserve_party),
      (gt, ":reserve_party", 0),
      (party_is_active, ":reserve_party"),
      (party_detach, ":reserve_party"),
      (remove_party, ":reserve_party"),
	(try_end),
    
	# detach all attached parties, in case there are parties in the camp
	(party_get_num_attached_parties, ":num_attached_parties", ":center"),
	(try_for_range_backwards, ":attached_party_rank", 0, ":num_attached_parties"),
		(party_get_attached_party_with_rank, ":attached_party", ":center", ":attached_party_rank"),
		(gt, ":attached_party", 0),
		(party_is_active, ":attached_party"),
		(party_detach, ":attached_party"),
	(try_end),

	(try_begin),
		(is_between, ":center", advcamps_begin, advcamps_end), # advance camps not replaced by ruins
		#reestablish the advance camp in 3+ days     
		(store_current_hours, ":cur_hours"),
		(faction_set_slot, ":center_faction", slot_faction_advcamp_timer, ":cur_hours"), #set the timer for camp creation
		(faction_get_slot, ":theater", ":center_faction", slot_faction_home_theater),
		(party_set_slot, ":center", slot_center_theater, ":theater"), #reset advance camp theater, just in case
		(try_for_range, ":camp_pointer", "p_camplace_N1", "p_ancient_ruins"), # free up campable place
			(store_distance_to_party_from_party,":dist", ":center", ":camp_pointer"),
			(le, ":dist",1),
			(party_set_slot, ":camp_pointer", slot_camp_place_occupied, 0),
		(try_end),
		(disable_party, ":center"),
	(else_try),
		(party_set_slot, ":center", slot_center_destroyed, 1), # DESTROY!
		(party_set_flags, ":center", pf_is_static|pf_always_visible|pf_hide_defenders|pf_label_small, 1),

		(try_begin),
			(party_slot_eq, ":center", slot_center_destroy_on_capture,2),
			(party_set_icon, ":center", "icon_debris"),
		(else_try),
			(try_begin),
				(neq,":center","p_town_minas_tirith"), # minas tirith has an elevated flag
				(party_set_banner_icon, ":center", "icon_debris"),
			(else_try),
				(party_set_banner_icon, ":center", "icon_empty"),
			(try_end),
		(try_end),
		(str_store_party_name, s1, ":center"),
		(party_set_name, ":center", "@___Ruins_of_{s1}___"), # spaces to make writings smaller (GA)
		#	   (party_set_extra_text, ":center", "@in_ruins"),  
		(party_set_faction, ":center", "fac_neutral"),
		(party_add_particle_system, ":center", "psys_map_village_looted_smoke"),
		(party_set_slot, ":center", slot_village_smoke_added, 25), # smoking for a day
	(try_end),

	(call_script, "script_update_center_notes", ":center"),
]),

# script_get_tld_distance
# Store real walking distance between parties (to handle Gondor towns), because aerial distance across White Mountains can be way off
# Input: party1, party2
# Output: reg0 - distance
("get_tld_distance", [
     (store_script_param, ":party1", 1),
     (store_script_param, ":party2", 2),
     # (try_begin), # one is south of WM, the other north of WM
       # (assign, ":count", 0),
       # (try_begin),
         # (call_script, "script_cf_party_is_south_of_white_mountains", ":party1"),
         # (call_script, "script_cf_party_is_north_of_white_mountains", ":party2"),
         # (val_add, ":count", 1),
       # (try_end),
       # (try_begin),
         # (call_script, "script_cf_party_is_south_of_white_mountains", ":party2"),
         # (call_script, "script_cf_party_is_north_of_white_mountains", ":party1"),
         # (val_add, ":count", 1),
       # (try_end),
       # (eq, ":count", 1), #xor, but should never be 2
	(try_begin),
		(call_script, "script_cf_party_west_of_minas_tirith", ":party1"),
		(call_script, "script_party_which_side_of_white_mountains", ":party2"), (assign, ":s2", reg0),
		(call_script, "script_party_which_side_of_white_mountains", ":party1"), (assign, ":s1", reg0),
		(neq, ":s1", ":s2"),  # not on same side
		(store_distance_to_party_from_party, ":dist1", ":party1", "p_town_minas_tirith"),
		(store_distance_to_party_from_party, reg0, ":party2", "p_town_minas_tirith"),
		(val_add, reg0, ":dist1"),
	(else_try),
		(store_distance_to_party_from_party, reg0, ":party1", ":party2"),
	(try_end),
# (store_distance_to_party_from_party, reg1, ":party1", ":party2"),
# (str_store_party_name, s13, ":party1"),
# (str_store_party_name, s14, ":party2"),
# (display_message, "@Debug: TLD distance between {s13} and {s14}: {reg0} (regular: {reg1})."),
]),

# script_cf_party_is_south_of_white_mountains  (drastically simpler version -- mtarini)
# Input: party
# Output: reg1 = 0 if NORTH. reg1 = 1 if SOUTH
("party_which_side_of_white_mountains", [
	(set_fixed_point_multiplier, 100), 
	(store_script_param, ":party", 1),
	(party_get_position, pos10, ":party"),
    (position_get_x, ":x", pos10),
    (position_get_y, ":y", pos10),
	(store_mul,":k",":x",374.4),(store_mul,":k2",":y",1000), (val_add,":k",":k2"), 
	(try_begin),
		(ge,":k",725184),
		(assign, reg1, 1),
	(else_try),
		(assign, reg1, 0),
	(try_end),
]),

("cf_party_west_of_minas_tirith", [
	(set_fixed_point_multiplier, 100), 
	(store_script_param, ":party", 1),
	(party_get_position, pos10, ":party"),
    (position_get_x, ":x", pos10),
	(gt, ":x", 4631),
]),
	 
# # script_cf_party_is_south_of_white_mountains
# # Party is south of White Mountains, i.e. south of the Hornburg-Minas Tirith line, west of Minas Tirith-Haradrim Camp line
# # Input: party
# ("cf_party_is_south_of_white_mountains",
   # [
     # (store_script_param, ":party", 1),
     
     # (set_fixed_point_multiplier, 1000), #needed
     
     # (try_begin),
       # (eq, "$g_tld_line_A1_mul", 0), #if globals not initialized, do it here (globals are for optimization, they are constant)
       # (call_script, "script_get_line_through_parties", "p_town_hornburg", "p_town_minas_tirith"),
       # (assign, "$g_tld_line_A1_mul", reg0),
       # (assign, "$g_tld_line_A1_div", reg1),
       # (assign, "$g_tld_line_B1", reg2),
       # (call_script, "script_get_line_through_parties", "p_town_harad_camp", "p_town_minas_tirith"),
       # (assign, "$g_tld_line_A2_mul", reg0),
       # (assign, "$g_tld_line_A2_div", reg1),
       # (assign, "$g_tld_line_B2", reg2),
       # (call_script, "script_get_line_through_parties", "p_town_morannon", "p_town_minas_tirith"),
       # (assign, "$g_tld_line_A3_mul", reg0),
       # (assign, "$g_tld_line_A3_div", reg1),
       # (assign, "$g_tld_line_B3", reg2),
     # (try_end),
     
     # (party_get_position, pos1, ":party"),
     # (position_get_x, ":xparty", pos1),
     # (position_get_y, ":yparty", pos1),
     
     # (store_mul, ":yline", ":xparty", "$g_tld_line_A1_mul"),
     # (val_div, ":yline", "$g_tld_line_A1_div"),
     # (val_add, ":yline", "$g_tld_line_B1"), # yline = a1*xparty + b1
     # (gt, ":yparty", ":yline"), # is party south of Hornburg-MT line?
# # (assign, reg0, ":yline"),
# # (assign, reg1, ":yparty"),
# # (display_message, "@Debug: The party is south of Hornburg-MT line. (Line: {reg0}, Party: {reg1})"),
     
     # (store_mul, ":yline", ":xparty", "$g_tld_line_A2_mul"),
     # (val_div, ":yline", "$g_tld_line_A2_div"),
     # (val_add, ":yline", "$g_tld_line_B2"), # yline = a2*xparty + b2
     # (gt, ":yparty", ":yline"), # is party west of Harad-MT line?
# # (assign, reg0, ":yline"),
# # (assign, reg1, ":yparty"),
# # (display_message, "@Debug: The party is west of Harad-MT line. (Line: {reg0}, Party: {reg1})"),
# ]),

# # script_cf_party_is_north_of_white_mountains
# # Party is north of White Mountains, i.e. north of the Hornburg-Minas Tirith line, west of Minas Tirith-Morannon line
# # Input: party
# ("cf_party_is_north_of_white_mountains",
   # [
     # (store_script_param, ":party", 1),
     
     # (set_fixed_point_multiplier, 1000), #needed
     
     # (try_begin),
       # (eq, "$g_tld_line_A1_mul", 0), #if globals not initialized, do it here (globals are for optimization, they are constant)
       # (call_script, "script_get_line_through_parties", "p_town_hornburg", "p_town_minas_tirith"),
       # (assign, "$g_tld_line_A1_mul", reg0),
       # (assign, "$g_tld_line_A1_div", reg1),
       # (assign, "$g_tld_line_B1", reg2),
       # (call_script, "script_get_line_through_parties", "p_town_harad_camp", "p_town_minas_tirith"),
       # (assign, "$g_tld_line_A2_mul", reg0),
       # (assign, "$g_tld_line_A2_div", reg1),
       # (assign, "$g_tld_line_B2", reg2),
       # (call_script, "script_get_line_through_parties", "p_town_morannon", "p_town_minas_tirith"),
       # (assign, "$g_tld_line_A3_mul", reg0),
       # (assign, "$g_tld_line_A3_div", reg1),
       # (assign, "$g_tld_line_B3", reg2),
     # (try_end),
     
     # (party_get_position, pos1, ":party"),
     # (position_get_x, ":xparty", pos1),
     # (position_get_y, ":yparty", pos1),
     
     # (store_mul, ":yline", ":xparty", "$g_tld_line_A1_mul"),
     # (val_div, ":yline", "$g_tld_line_A1_div"),
     # (val_add, ":yline", "$g_tld_line_B1"), # yline = a1*xparty + b1
     # (lt, ":yparty", ":yline"), # is party north of Hornburg-MT line?
# # (assign, reg0, ":yline"),
# # (assign, reg1, ":yparty"),
# # (display_message, "@Debug: The party is north of Hornburg-MT line. (Line: {reg0}, Party: {reg1})"),
     
     # (store_mul, ":yline", ":xparty", "$g_tld_line_A3_mul"),
     # (val_div, ":yline", "$g_tld_line_A3_div"),
     # (val_add, ":yline", "$g_tld_line_B3"), # yline = a3*xparty + b3
     # (lt, ":yparty", ":yline"), # is party west of Morannon-MT line?
# # (assign, reg0, ":yline"),
# # (assign, reg1, ":yparty"),
# # (display_message, "@Debug: The party is west of Morannon-MT line. (Line: {reg0}, Party: {reg1})"),
# ]),

# # script_get_line_through_parties
# # Get a line y=Ax+B that passes through both input parties, where A=A_mul/A_div
# # Input: party1, party2
# # Output: reg0=A_mul, reg1=A_div, reg2=B
# ("get_line_through_parties",
   # [
     # (store_script_param, ":party1", 1),
     # (store_script_param, ":party2", 2),
     
     # (set_fixed_point_multiplier, 1000), #we need some accuracy here
     
     # (party_get_position, pos1, ":party1"),
     # (position_get_x, ":x1", pos1),
     # (position_get_y, ":y1", pos1),
     # (party_get_position, pos1, ":party2"),
     # (position_get_x, ":x2", pos1),
     # (position_get_y, ":y2", pos1),
     
     # #get A=(y2-y1)/(x2-x1)= A_mul/A_div
     # (store_sub, reg0, ":y2", ":y1"), #A_mul
     # (store_sub, reg1, ":x2", ":x1"), #A_div
     
     # #get B=y1-A*x1= y1-A_mul*x1/A_div
     # (store_mul, reg2, reg0, ":x1"),
     # (val_div, reg2, reg1), #some numerical loss
     # (val_mul, reg2, -1),
     # (val_add, reg2, ":y1"),
# # (display_message, "@Debug: script_get_line_through_parties: y = {reg0}/{reg1}*x + {reg2}"),
# ]),

# script_get_advcamp_pos_predefined
# Gets a position of the advance camp in another theater (looks up faction active theater)
# Input: faction
# Output: pos1
# Uses pos2 and pos3
("get_advcamp_pos_predefined",
   [(store_script_param, ":faction", 1),
    (faction_get_slot, ":active_theater", ":faction", slot_faction_active_theater),
    (faction_get_slot, ":home_theater", ":faction", slot_faction_home_theater),
    (assign, ":camp", "p_camplace_M1"), # some default
	(assign, ":campend", "p_camplace_S1"),
    (try_begin),
        (eq, ":active_theater", theater_N), (assign, ":camp", "p_camplace_N1"),(assign, ":campend", "p_camplace_M1"),
    (else_try),
        (eq, ":active_theater", theater_SE), (assign, ":camp", "p_camplace_S1"),(assign, ":campend", "p_ancient_ruins"),
	(else_try),
        (eq, ":active_theater", theater_C),(eq, ":home_theater", theater_N),(assign, ":camp", "p_camplace_N1"),(assign, ":campend", "p_camplace_M1"),
	(else_try),
        (eq, ":active_theater", theater_C),(neq, ":home_theater", theater_N),(assign, ":camp", "p_camplace_M1"),(assign, ":campend", "p_camplace_S1"),
    (else_try),
        (eq, ":active_theater", theater_SW),(eq, ":home_theater", theater_SE),(assign, ":camp", "p_camplace_S1"),(assign, ":campend", "p_ancient_ruins"),
    (else_try),
         (eq, ":active_theater", theater_SW),(neq, ":home_theater", theater_SE),(assign, ":camp", "p_camplace_M1"),(assign, ":campend", "p_camplace_S1"),
    (try_end),
     
	(assign, ":continue", 1),
	(try_for_range, ":cur_center", ":camp", ":campend"), # look for available predefined places
		(eq, ":continue", 1), 
		(party_slot_eq, ":cur_center", slot_camp_place_occupied, 0),
		(party_set_slot,":cur_center", slot_camp_place_occupied, 1),
		(party_get_position, pos1, ":cur_center"),
		(assign, ":continue", 0),
	(try_end),
	
	(party_get_position, pos2, ":camp"),
    (try_begin),
		(eq, ":continue", 1), # all predefined places occupied, spawn around camp begin
		(assign, ":radius", 5),
		(try_for_range, ":tries", 0, 1000),
		   (eq, ":continue", 1),
		   (map_get_random_position_around_position, pos1, pos2, ":radius"), # random circle with 5+ clicks radius
		   (assign, ":too_close", 0),
		   (try_for_range, ":cur_center", centers_begin, centers_end),		   # check if too close to another center
			 (eq, ":too_close", 0),
			 (party_is_active, ":cur_center"), #TLD
			 (party_slot_eq, ":cur_center", slot_center_destroyed, 0), #TLD
			 (store_faction_of_party, ":cur_faction", ":cur_center"),
			 (store_relation, ":rel", ":cur_faction", ":faction"),
			 (party_get_position, pos3, ":cur_center"),
			 (get_distance_between_positions, ":cur_dist", pos1, pos3),
			 (try_begin),
			   (lt, ":cur_dist", 800), #at least 10(8 GA) clicks from enemy centers
			   (this_or_next|lt, ":rel", 0),
			   (lt, ":cur_dist", 400), #at least 5 (4 GA) clicks from friendly centers
			   (assign, ":too_close", 1),
			 (try_end),
		   (try_end),
		   (try_begin),
			 (eq, ":too_close", 0),
			 (assign, ":continue", 0),
		   (else_try), # increase radius for every 5 unsuccessful tries
			 (store_mod, ":tries_mod", ":tries", 5),
			 (eq, ":tries_mod", 4),
			 (val_add, ":radius", 1),
		   (try_end),
		(try_end),
	(try_end),     # out comes pos1
]),

]