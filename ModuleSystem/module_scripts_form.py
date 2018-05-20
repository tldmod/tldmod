# Formations AI for Mount&Blade by Motomataru
# rel. 12/26/10
# MV: Comcatenated original formAI_scripts_mb.py and formations_scripts_mb.py (search for "#Formations Scripts" to find where they start)

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *

from header_parties import *
from header_skills import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from ID_animations import *

from module_info import wb_compile_switch as is_a_wb_script


####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

formAI_scripts = [
# # AI with Formations Scripts
  # script_calculate_decision_numbers by motomataru
  # Input: AI team, size relative to battle in %
  # Output: reg0 - battle presence plus level bump, reg1 - level bump (team avg level / 3)
  ("calculate_decision_numbers", [
	(store_script_param, ":team_no", 1),
	(store_script_param, ":battle_presence", 2),
	(try_begin),
		(call_script, "script_battlegroup_get_level", ":team_no", grc_everyone),
		(store_div, reg1, reg0, 3),
		(store_add, reg0, ":battle_presence", reg1),	#decision w.r.t. all enemy teams
	(try_end)
	]),
	

  # script_team_field_ranged_tactics by motomataru #Kham - Edited
  # Input: AI team, size relative to largest team in %, size relative to battle in %
  # Output: none
  ("team_field_ranged_tactics", [
	(store_script_param, ":team_no", 1),
	(store_script_param, ":rel_army_size", 2),
	(store_script_param, ":battle_presence", 3),
	(call_script, "script_battlegroup_get_size", ":team_no", grc_archers),

	#Shit, Elves! Tactic - kham
	(try_begin),
		(gt, "$g_ally_party", 0),
		(store_faction_of_party, ":ally_elf", "$g_ally_party"),
	(try_end),
	
	(try_begin),
		(store_faction_of_party, ":enemy_elf", "$g_enemy_party"),
		(store_faction_of_party, ":player_elf", "p_main_party"),
		(team_get_leader, ":elf_leader", ":team_no"),
		(gt, ":elf_leader", 0),
		(agent_get_troop_id, ":agent_troop", ":elf_leader"),
		(store_troop_faction, ":team_is_elf", ":agent_troop"),
		(assign, ":shit_elves", 0),
		(try_begin),
			(gt, ":ally_elf", 0),
			(is_between, ":ally_elf", "fac_lorien", "fac_dale"),
			(assign, ":shit_elves", 1),
		(else_try),
			(is_between, ":player_elf", "fac_lorien","fac_dale"),
			(assign, ":shit_elves", 1),
		(else_try),
			(is_between, ":enemy_elf", "fac_lorien","fac_dale"),
			(assign, ":shit_elves", 1),
		(try_end),
	(try_end),

	(try_begin),
		(gt, reg0, 0),
		(call_script, "script_battlegroup_get_position", Archers_Pos, ":team_no", grc_archers),
		(call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":team_no"),
		(call_script, "script_point_y_toward_position", Archers_Pos, Enemy_Team_Pos),
		(call_script, "script_get_nearest_enemy_battlegroup_location", Nearest_Enemy_Battlegroup_Pos, ":team_no", Archers_Pos),
		(assign, ":distance_to_enemy", reg0),
			
		(call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"),
		(assign, ":decision_index", reg0),
		(assign, ":level_bump", reg1),
		(try_begin),
			(gt, ":decision_index", 86),	#outpower enemies more than 6:1?
			(team_give_order, ":team_no", grc_archers, mordr_charge),

		(else_try),
			(ge, "$battle_phase", BP_Jockey),
			(try_begin),
				(eq, ":team_no", 0),
				(assign, reg0, "$team0_archers_have_ammo"),
			(else_try),
				(eq, ":team_no", 1),
				(assign, reg0, "$team1_archers_have_ammo"),
			(else_try),
				(eq, ":team_no", 2),
				(assign, reg0, "$team2_archers_have_ammo"),
			(else_try),
				(eq, ":team_no", 3),
				(assign, reg0, "$team3_archers_have_ammo"),
			(try_end),
			
			#Special orders for archers to support melee go here, JL		
			(this_or_next|eq, "$arc_charge_activated", 1), #are archers ordered to charge? JL
			(eq, reg0, 0),	#running out of ammo?
			(team_give_order, ":team_no", grc_archers, mordr_charge),
			#(display_message, "@Archers are charging, Archer AI disabled!"),##################

		(else_try),
			#(display_message, "@Archer form AI started"), #####################
			(gt, "$cur_casualties", 0),
			(eq, "$cur_casualties", "$prev_casualties"),	#no new casualties since last function call?
			(gt, ":decision_index", Advance_More_Point),
			(le, ":distance_to_enemy", AI_long_range),	#closer than reposition?
			(team_give_order, ":team_no", grc_archers, mordr_advance),

		#hold somewhere
		(else_try),
			(store_add, ":decision_index", ":rel_army_size", ":level_bump"),	#decision w.r.t. largest enemy team
			(assign, ":move_archers", 0),
			(try_begin),
				(eq, "$battle_phase", BP_Setup),
				(assign, ":move_archers", 1),
			(else_try),
				(eq, "$battle_phase", BP_Fight), #changed ge to eq -JL
				(try_begin),
					(neg|is_between, ":distance_to_enemy", AI_charge_distance, AI_long_range),
					(assign, ":move_archers", 1),
				(else_try),
					(lt, ":decision_index", Hold_Point),	#probably coming from a defensive position (see below)
					(gt, ":distance_to_enemy", AI_firing_distance),
					(eq, "$FormAI_AI_no_defense", 0),	#player hasn't set disallow defense option?
					(this_or_next|is_between, ":team_is_elf", "fac_lorien", "fac_dale"),
					(eq, ":shit_elves", 0), #There are no elven teams
					(assign, ":move_archers", 1),
				(try_end),
			(else_try),
				(this_or_next|eq, "$FormAI_AI_no_defense", 0),	#player hasn't set disallow defense option OR?
				(ge, ":decision_index", Hold_Point),	#not starting in a defensive position (see below)
				(this_or_next|is_between, ":team_is_elf", "fac_lorien", "fac_dale"),
				(eq, ":shit_elves", 0), #There are no elven teams
				(call_script, "script_battlegroup_get_size", ":team_no", grc_infantry),
				(try_begin),
					(this_or_next|eq, reg0, 0),
					(gt, ":distance_to_enemy", AI_long_range),
					(assign, ":move_archers", 1),
				(else_try),	#don't outstrip infantry when closing
					(call_script, "script_battlegroup_get_position", Infantry_Pos, ":team_no", grc_infantry),
					(get_distance_between_positions, ":infantry_to_enemy", Infantry_Pos, Nearest_Enemy_Battlegroup_Pos),
					(val_sub, ":infantry_to_enemy", ":distance_to_enemy"),
					(le, ":infantry_to_enemy", 1500),
					(assign, ":move_archers", 1),
				(try_end),
			(try_end),
			
			(try_begin),
				(gt, ":move_archers", 0),
				(try_begin),
					(eq, ":team_no", 0),
					(assign, ":team_start_pos", Team0_Starting_Point),
				(else_try),
					(eq, ":team_no", 1),
					(assign, ":team_start_pos", Team1_Starting_Point),
				(else_try),
					(eq, ":team_no", 2),
					(assign, ":team_start_pos", Team2_Starting_Point),
				(else_try),
					(eq, ":team_no", 3),
					(assign, ":team_start_pos", Team3_Starting_Point),
				(try_end),

				(try_begin),
					(lt, ":decision_index", Hold_Point),	#outnumbered?
					(eq, "$FormAI_AI_no_defense", 0),	#player hasn't set disallow defense option?
					(this_or_next|is_between, ":team_is_elf", "fac_lorien", "fac_dale"),
					(eq, ":shit_elves", 0), #There are no elven teams
					(lt, "$battle_phase", BP_Fight),
					(store_div, ":distance_to_move", ":distance_to_enemy", 6),	#middle of rear third of battlefield
					(assign, ":hill_search_radius", ":distance_to_move"),

				(else_try),
					(assign, ":from_start_pos", 0),					
					(try_begin),
						(eq, "$battle_phase", BP_Fight), #changed ge to eq -JL
						(assign, ":from_start_pos", 1),
					(else_try),
						(gt, "$battle_phase", BP_Setup),
						(call_script, "script_point_y_toward_position", ":team_start_pos", Archers_Pos),
						(position_get_rotation_around_z, reg0, ":team_start_pos"),
						(position_get_rotation_around_z, reg1, Archers_Pos),
						(val_sub, reg0, reg1),
						(neg|is_between, reg0, -45, 45),
						(assign, ":from_start_pos", 1),
					(try_end),
					
					(try_begin),
						(gt, ":from_start_pos", 0),
						(copy_position, Archers_Pos, ":team_start_pos"),
						(call_script, "script_point_y_toward_position", Archers_Pos, Enemy_Team_Pos),
						(call_script, "script_get_nearest_enemy_battlegroup_location", Nearest_Enemy_Battlegroup_Pos, ":team_no", Archers_Pos),
						(assign, ":distance_to_enemy", reg0),
					(try_end),

					(try_begin),
						(eq, "$battle_phase", BP_Setup),
						(assign, ":shot_distance", AI_long_range),
					(else_try),
						(assign, ":shot_distance",  AI_firing_distance),
						(try_begin),
							(eq, ":team_no", 0),
							(assign, reg0, "$team0_percent_ranged_throw"),
						(else_try),
							(eq, ":team_no", 1),
							(assign, reg0, "$team1_percent_ranged_throw"),
						(else_try),
							(eq, ":team_no", 2),
							(assign, reg0, "$team2_percent_ranged_throw"),
						(else_try),
							(eq, ":team_no", 3),
							(assign, reg0, "$team3_percent_ranged_throw"),
						(try_end),
						(store_sub, reg1, AI_firing_distance, AI_charge_distance), #if default constants are used -> 4500
						(val_add, reg1, 200),	#add two meters to prevent automatically provoking melee from forward enemy infantry
						(val_mul, reg1, reg0),
						(val_div, reg1, 100),
						(val_sub, ":shot_distance", reg1),
					(try_end),

					(store_sub, ":distance_to_move", ":distance_to_enemy", ":shot_distance"),
					(store_div, ":hill_search_radius", ":shot_distance", 3),	#limit so as not to run into enemy
					(try_begin),
						(lt, "$battle_phase", BP_Fight),
						(try_begin),
							(this_or_next|eq, "$battle_phase", BP_Setup),
							(lt, ":battle_presence", Advance_More_Point),	#expect to meet halfway?
							(val_div, ":distance_to_move", 2),
						(try_end),
					(try_end),
				(try_end),

				(position_move_y, Archers_Pos, ":distance_to_move", 0),
				(try_begin),
					(lt, "$battle_phase", BP_Fight),
					(copy_position, pos1, Archers_Pos),
					(store_div, reg0, ":hill_search_radius", 100),
					(call_script, "script_find_high_ground_around_pos1_corrected", Archers_Pos, reg0),
				(try_end),
			(try_end),

			(team_give_order, ":team_no", grc_archers, mordr_hold),
			(team_set_order_position, ":team_no", grc_archers, Archers_Pos),
		(try_end),
	(try_end)
	]),

] + (is_a_wb_script==1 and [

  # WB Only as it has some operations that are WB only - Kham
  # script_team_field_melee_tactics by motomataru KHAM - Edited
  # Input: AI team, size relative to largest team in %, size relative to battle in %
  # Output: none
  ("team_field_melee_tactics", [
	(store_script_param, ":team_no", 1),
#	(store_script_param, ":rel_army_size", 2),
	(store_script_param, ":battle_presence", 3),
	(call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"),
	
	(store_mission_timer_a, ":timer"), 

	##JL code for checking disengagement by reinforcements:
	(try_begin),
		(eq, "$formai_disengage", 0), #if we have no disengagement ordered yet then
		
		(store_normalized_team_count, ":num_attackers", 1), #added by JL to use for determining reinforcements (and possibly future other factors)
		(store_normalized_team_count, ":num_defenders", 0), #added by JL to use for determining reinforcements (and possibly future other factors)

		(try_begin), #for attackers:
			(lt, ":num_attackers", 6), #if number of attackers are 5 or less
			(eq, "$att_reinforcements_arrived", 0), #and attacker reinforcements have not arrived
			(assign, "$att_reinforcements_needed", 1), #set attacker reinforcements are needed
		(try_end),
		(try_begin),
			(ge, ":num_attackers", 6), #if number of attacker or defenders are more than 5
			(eq, "$att_reinforcements_needed", 1), # and attacker reinforcements were needed
			(assign, "$att_reinforcements_arrived", 1), #set attacker reinforcements to have arrived
			(assign, "$att_reinforcements_needed", 0), #set attacker reinforcements are not needed
			(assign, "$formai_disengage", 1), #set flag that disengagement is ok
			#(display_message, "@Attacker reinforcements have arrived"), #############
		(try_end),
		
		(try_begin), #for defenders:
			(lt, ":num_defenders",6), #if number of defenders are 5 or less
			(eq, "$def_reinforcements_arrived", 0), #and defender reinforcements have not arrived
			(assign, "$def_reinforcements_needed", 1), #set defender reinforcements are needed
		(try_end),
		(try_begin),
			(ge, ":num_defenders", 6), #if number of defenders are more than 5
			(eq, "$def_reinforcements_needed", 1), # and defender reinforcements were needed
			(assign, "$def_reinforcements_arrived", 1), #set defender reinforcements to have arrived
			(assign, "$def_reinforcements_needed", 0), #set defender reinforcements are not needed
			(assign, "$formai_disengage", 1), #set flag that disengagement is ok
			#(display_message, "@Defender reinforcements have arrived"), #############
		(try_end),
	(try_end),
	##End JL code
	
	
	#mop up if outnumber enemies more than 6:1
	(try_begin),
		(gt, reg0, 86),
		(call_script, "script_formation_end", ":team_no", grc_infantry),
		(team_give_order, ":team_no", grc_infantry, mordr_charge),
		(call_script, "script_formation_end", ":team_no", grc_cavalry),
		(team_give_order, ":team_no", grc_cavalry, mordr_charge),

	(else_try),
		#find closest distance of enemy to infantry, cavalry troops
		(assign, ":inf_closest_dist", Far_Away),
		(assign, ":inf_closest_non_cav_dist", Far_Away),
		(assign, ":cav_closest_dist", Far_Away),
		(assign, ":num_enemies_in_melee", 0),
		(assign, ":num_enemies_supporting_melee", 0),
		(assign, ":num_enemy_infantry", 0),
		(assign, ":num_enemy_cavalry", 0),
		(assign, ":num_enemy_others", 0),
		(assign, ":num_enemy_elves", 0),
		(assign, ":sum_level_enemy_infantry", 0),
		(assign, ":x_enemy", 0),
		(assign, ":y_enemy", 0),
		(try_for_agents, ":enemy_agent"),
			(agent_is_alive, ":enemy_agent"),
			(agent_is_human, ":enemy_agent"),
			(agent_is_active, ":enemy_agent"),
			(agent_get_team, ":enemy_team_no", ":enemy_agent"),
			(teams_are_enemies, ":enemy_team_no", ":team_no"),
           # (agent_slot_eq, ":enemy_agent", slot_agent_is_running_away, 0),
           	(gt, ":enemy_agent", 0), #for some reason, -1 is being shown here...
            (agent_get_troop_id, ":enemy_troop", ":enemy_agent"),
            (troop_get_type, ":enemy_race", ":enemy_troop"),
			(neq, ":enemy_race", tf_troll), #disregard trolls
			
			(try_begin),
				(is_between, ":enemy_race", tf_elf_begin, tf_elf_end),
				(val_add, ":num_enemy_elves", 1),
			(try_end),

			(agent_get_class, ":enemy_class_no", ":enemy_agent"),
			(try_begin),
				(eq, ":enemy_class_no", grc_infantry),
				(val_add, ":num_enemy_infantry", 1),
				(agent_get_troop_id, ":enemy_troop", ":enemy_agent"),
				(store_character_level, ":enemy_level", ":enemy_troop"),
				(val_add, ":sum_level_enemy_infantry", ":enemy_level"),
			(else_try),
				(eq, ":enemy_class_no", grc_cavalry),
				(val_add, ":num_enemy_cavalry", 1),
			(else_try),
				(val_add, ":num_enemy_others", 1),
			(try_end),
			(agent_get_position, pos0, ":enemy_agent"),
			(position_get_x, ":value", pos0),
			(val_add, ":x_enemy", ":value"),
			(position_get_y, ":value", pos0),
			(val_add, ":y_enemy", ":value"),
			(assign, ":enemy_in_melee", 0),
			(assign, ":enemy_supporting_melee", 0),
			(try_for_agents, ":cur_agent"),
				(agent_is_alive, ":cur_agent"),
				(agent_is_human, ":cur_agent"),
				(agent_is_active, ":cur_agent"),
				(agent_get_team, ":cur_team_no", ":cur_agent"),
				(eq, ":cur_team_no", ":team_no"),
				#(agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 0),
				(agent_get_class, ":cur_class_no", ":cur_agent"),
				(try_begin),
					(eq, ":cur_class_no", grc_infantry), #this block will not be traversed if there is no Infantry ... JL
					(agent_get_position, pos1, ":cur_agent"),
					(get_distance_between_positions, ":distance_of_enemy", pos0, pos1),
					(try_begin),
						(gt, ":inf_closest_dist", ":distance_of_enemy"),
						(assign, ":inf_closest_dist", ":distance_of_enemy"),
						(copy_position, Nearest_Enemy_Troop_Pos, pos0),
						(assign, ":enemy_nearest_troop_distance", ":distance_of_enemy"),
						(assign, ":enemy_nearest_agent", ":enemy_agent"),
					(try_end),
					(try_begin),
						(neq, ":enemy_class_no", grc_cavalry),
						(gt, ":inf_closest_non_cav_dist", ":distance_of_enemy"),
						(assign, ":inf_closest_non_cav_dist", ":distance_of_enemy"),
						(copy_position, Nearest_Non_Cav_Enemy_Troop_Pos, pos0),
						(assign, ":enemy_nearest_non_cav_troop_distance", ":distance_of_enemy"),
						(assign, ":enemy_nearest_non_cav_agent", ":enemy_agent"),
					(try_end),
					(try_begin),
						(lt, ":distance_of_enemy", 150),
						(assign, ":enemy_in_melee", 1),
					(try_end),
					(try_begin),
						(lt, ":distance_of_enemy", 350),
						(assign, ":enemy_supporting_melee", 1),
					(try_end),
				(else_try),
					(eq, ":cur_class_no", grc_cavalry),
					(agent_get_position, pos1, ":cur_agent"),
					(get_distance_between_positions, ":distance_of_enemy", pos0, pos1),
					(try_begin),
						(gt, ":cav_closest_dist", ":distance_of_enemy"),
						(assign, ":cav_closest_dist", ":distance_of_enemy"),
					(try_end),
				(try_end),
			(try_end),
			(try_begin),
				(eq, ":enemy_in_melee", 1),
				(val_add, ":num_enemies_in_melee", 1),
			(try_end),
			(try_begin),
				(eq, ":enemy_supporting_melee", 1),
				(val_add, ":num_enemies_supporting_melee", 1),
			(try_end),
		(try_end),
		
		(store_add, ":num_enemies", ":num_enemy_infantry", ":num_enemy_cavalry"),
		(val_add, ":num_enemies", ":num_enemy_others"),

		(gt, ":num_enemies", 0),
		#JL get percentage of enemy others (archers, commpanions)
		(assign, ":perc_enemy_others", ":num_enemy_others"), #assign enemy others percentage JL
		(val_mul, ":perc_enemy_others", 100), #multiply by 100 to get percent JL
		(val_div, ":perc_enemy_others", ":num_enemies"), #divide by total enemies to get ratio in percent JL

		#Kham - Get % of Enemy Elves - Infantry charges if enemy elves > 20% of enemy composition
		(store_mul, ":perc_enemy_elves", ":num_enemy_elves", 100),
		(val_div, ":perc_enemy_elves", ":num_enemies"),
		
		(init_position, Enemy_Team_Pos),
		(val_div, ":x_enemy", ":num_enemies"),
		(position_set_x, Enemy_Team_Pos, ":x_enemy"),
		(val_div, ":y_enemy", ":num_enemies"),
		(position_set_y, Enemy_Team_Pos, ":y_enemy"),
		(position_set_z_to_ground_level, Enemy_Team_Pos),

		(call_script, "script_battlegroup_get_size", ":team_no", grc_archers),
		(assign, ":num_archers", reg0),
		#(display_message, "@{reg0} archers"),
		(try_begin),
			(eq, ":num_archers", 0),
			(assign, ":enemy_from_archers", Far_Away),
			(assign, ":archer_order", mordr_charge),
		(else_try),
			(call_script, "script_battlegroup_get_position", Archers_Pos, ":team_no", grc_archers),
			(call_script, "script_point_y_toward_position", Archers_Pos, Enemy_Team_Pos),
			(call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Archers_Pos),
			(assign, ":enemy_from_archers", reg0),
			(team_get_movement_order, ":archer_order", ":team_no", grc_archers),
		(try_end),

		(call_script, "script_battlegroup_get_size", ":team_no", grc_infantry),
		(assign, ":num_infantry", reg0),
		#(display_message, "@{reg0} infantry"),
		(try_begin),
			(eq, ":num_infantry", 0),
			(assign, ":enemy_from_infantry", Far_Away),
		(else_try),
			(call_script, "script_battlegroup_get_position", Infantry_Pos, ":team_no", grc_infantry),
			(call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Infantry_Pos),
			(assign, ":enemy_from_infantry", reg0),
		(try_end),

		(call_script, "script_battlegroup_get_size", ":team_no", grc_cavalry),
		(assign, ":num_cavalry", reg0),
		#(display_message, "@{reg0} cavalry"),
		(try_begin),
			(eq, ":num_cavalry", 0),
			(assign, ":enemy_from_cavalry", Far_Away),
		(else_try),
			(call_script, "script_battlegroup_get_position", Cavalry_Pos, ":team_no", grc_cavalry),
			(call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Cavalry_Pos),
			(assign, ":enemy_from_cavalry", reg0),
		(try_end),

		(try_begin),
			(lt, "$battle_phase", BP_Fight),
			(this_or_next|le, ":enemy_from_infantry", AI_charge_distance),
			(this_or_next|le, ":enemy_from_cavalry", AI_charge_distance),
			(le, ":enemy_from_archers", AI_charge_distance),
			(assign, "$battle_phase", BP_Fight),
		(else_try),
			(lt, "$battle_phase", BP_Jockey),
			(this_or_next|le, ":inf_closest_dist", AI_long_range),
			(le, ":cav_closest_dist", AI_long_range),
			(assign, "$battle_phase", BP_Jockey),
		(try_end),
		
		#(team_get_leader, ":team_leader", ":team_no"),
        (call_script, "script_team_get_nontroll_leader", ":team_no"),
        (assign, ":team_leader", reg0),
        (gt, ":team_leader", 0),
		
		#infantry AI
		#(assign, ":place_leader_by_infantry", 0), #Kham -  removed all these
		
		# JL DISENGAGEMENT OF ARCHERS:
		(try_begin),
			(gt, ":num_archers", 0), #if there are any archers
			(eq, "$arc_charge_activated", 1), #and archers are in charge mode
			(ge, ":enemy_from_archers", AI_charge_distance), #and enemies are not immediately near
			(assign, "$arc_charge_activated", 0), #then deactivate inf charge mode
			#(display_message, "@Archers ordered to resume shooting."), #######################
		(try_end),
		
		#JL ADVANCE Archers closer to infantry if they are too far away:
		(try_begin),
			(gt, ":num_archers", 0), #if there are any archers
			(gt, ":num_infantry", 0), #and if there is infantry
			(get_distance_between_positions, ":archer_dist_to_inf", Infantry_Pos, Archers_Pos),
			(gt, ":archer_dist_to_inf", 4000), #allied inf are not within 40m
			(gt, ":enemy_from_archers", 4000), #and enemies are not within 40m 
			(ge, ":enemy_from_archers", ":enemy_from_infantry"), #and enemies are closer or equally close to infantry than they are to archers
			(team_give_order, ":team_no", grc_archers, mordr_charge), #charge the archers forward
			#(display_message, "@Archers ordered to charge to keep close with infantry."), #######################
		(try_end),
		
		(assign, ":charge_against_elves", 0),

		(try_begin),
			(gt, ":perc_enemy_elves", 20), #if there are more than 20% enemy elves
			(ge, ":timer", 90), #and it has been a 1.5 mins
			(assign, ":charge_against_elves", 1), #activate infantry charge against elves
		(try_end),

		(try_begin),
			(le, ":num_infantry", 0),
			(assign, ":infantry_order", ":archer_order"),
		(else_try),
			(try_begin), ## JL CHARGE ACTIVATION to force inf Charge Mode when inf AI has been deemed to need charge mode (--for use if inf charge has been ordered earlier in the code or from archers code)
				(eq, "$inf_charge_activated", 1), #if inf AI has been told to Charge
				(eq, "$inf_charge_ongoing", 0), #and switch is false
				(call_script, "script_formation_end", ":team_no", grc_infantry), #end any formations
				(team_give_order, ":team_no", grc_infantry, mordr_charge), #do a Native Charge
				(assign, "$inf_charge_ongoing", 1), #switch set to true so this function is not needed to be called again until charge mode has been disabled and a new charge has been set
				#(display_message, "@Infantry orders are Charge, Formations Inf AI disabled"), ################
			(try_end),	
			
			(try_begin), ## JL RULES OF DISENGAGEMENT: to Remove AI Infantry Charge Mode when infantry is not in melee any more
				(eq, ":num_enemies_supporting_melee", 0), #infantry is currently not in melee
				(gt, ":enemy_from_infantry", 1500), #JL Kham - and nearest enemy is further away than 20m - Changed to 15m
				(eq, "$inf_charge_ongoing", 1), # flag to see if we have a regular charge ongoing
				(assign, "$inf_charge_activated", 0), #then deactivate inf charge mode
				(assign, "$inf_charge_ongoing", 0), #and reset switch to open up for future charge orders
				#(display_message, "@Infantry AI is not in melee and decides to resume maneuver"), #######################
			(try_end),

			#JL Control to Continue form AI
			(eq, "$inf_charge_activated", 0), #If infantry charge has not been activated then continue Inf AI, JL
			
			(store_mul, ":percent_level_enemy_infantry", ":sum_level_enemy_infantry", 100),
			(val_div, ":percent_level_enemy_infantry", ":num_enemies"),
			(try_begin),
				(teams_are_enemies, ":team_no", "$fplayer_team_no"),
				(assign, ":combined_level", 0),
				(assign, ":combined_team_size", 0),
				(assign, ":combined_num_infantry", ":num_infantry"),
			(else_try),
				(call_script, "script_battlegroup_get_level", "$fplayer_team_no", grc_infantry),
				(assign, ":combined_level", reg0),
				(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_everyone),
				(assign, ":combined_team_size", reg0),
				(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_infantry),
				(store_add, ":combined_num_infantry", ":num_infantry", reg0),
			(try_end),
			(store_mul, ":percent_level_infantry", ":combined_num_infantry", 100),
			(call_script, "script_battlegroup_get_level", ":team_no", grc_infantry),
			(assign, ":level_infantry", reg0),
			(val_add, ":combined_level", reg0),
			(val_mul, ":percent_level_infantry", ":combined_level"),
			(call_script, "script_battlegroup_get_size", ":team_no", grc_everyone),
			(val_add, ":combined_team_size", reg0),
			(val_div, ":percent_level_infantry", ":combined_team_size"),

			(assign, ":infantry_order", mordr_charge),
			(try_begin),	#enemy far away AND ranged not charging
				(gt, ":enemy_from_archers", AI_charge_distance),
				(gt, ":inf_closest_dist", AI_charge_distance),
				(neq, ":archer_order", mordr_charge),
				(try_begin),	#fighting not started OR not enough infantry
					(this_or_next|le, "$battle_phase", BP_Jockey),
					(lt, ":percent_level_infantry", ":percent_level_enemy_infantry"),
					(assign, ":infantry_order", mordr_hold),
				(try_end),
			(try_end),

			#if low level troops outnumber enemies in melee by 2:1, attempt to whelm
			(try_begin),
				(le, ":level_infantry", 12),
				(gt, ":num_enemies_in_melee", 0),
				(store_mul, reg0, ":num_enemies_supporting_melee", 2),
				(is_between, reg0, 1, ":num_infantry"),
				(get_distance_between_positions, reg0, Infantry_Pos, Nearest_Enemy_Troop_Pos),
				(le, reg0, AI_charge_distance),
				(call_script, "script_formation_end", ":team_no", grc_infantry),
				(team_give_order, ":team_no", grc_infantry, mordr_charge),
				#(display_message, "@Infantry decided to whelm."), #############

			(else_try), #Kham - Make infantry charge when enemy is close
		        (get_distance_between_positions, reg0, Infantry_Pos, Nearest_Enemy_Troop_Pos),
		        (this_or_next|le, ":enemy_from_infantry", 1300), # Start charge if enemy infantry formation is close
		        (this_or_next|le, ":enemy_from_archers", 1300), # Start charge if enemy archer group is close.
		        (le, reg0, 900), # Start charge if any enemies are really close.
		        (call_script, "script_formation_end", ":team_no", grc_infantry),
						(team_get_movement_order, reg0, ":team_no", grc_infantry),
		        (team_give_order, ":team_no", grc_infantry, mordr_hold_fire), # Hold fire while charging to keep infantry together.
						(try_begin),
							(neq, reg0, mordr_charge),
							(team_give_order, ":team_no", grc_infantry, mordr_charge),
						(try_end),  #Kham - changes end
						#(display_message, "@DEBUG: Infantry decides to charge!"),
				
			#else attempt to form formation somewhere
			(else_try),
				(try_begin),
					(eq, ":team_no", 0),
					(try_begin),
						(eq, "$team0_default_formation", formation_default),
						(call_script, "script_get_default_formation", 0),
						(assign, "$team0_default_formation", reg0),
					(try_end),
					(assign, ":infantry_formation", "$team0_default_formation"),
				(else_try),
					(eq, ":team_no", 1),
					(try_begin),
						(eq, "$team1_default_formation", formation_default),
						(call_script, "script_get_default_formation", 1),
						(assign, "$team1_default_formation", reg0),
					(try_end),
					(assign, ":infantry_formation", "$team1_default_formation"),
				(else_try),
					(eq, ":team_no", 2),
					(try_begin),
						(eq, "$team2_default_formation", formation_default),
						(call_script, "script_get_default_formation", 2),
						(assign, "$team2_default_formation", reg0),
					(try_end),
					(assign, ":infantry_formation", "$team2_default_formation"),
				(else_try),
					(eq, ":team_no", 3),
					(try_begin),
						(eq, "$team3_default_formation", formation_default),
						(call_script, "script_get_default_formation", 3),
						(assign, "$team3_default_formation", reg0),
					(try_end),
					(assign, ":infantry_formation", "$team3_default_formation"),
				(try_end),
				
				(call_script, "script_classify_agent", ":enemy_nearest_agent"),
				(assign, ":enemy_nearest_troop_division", reg0),
				(agent_get_class, ":enemy_nearest_troop_class", ":enemy_nearest_agent"), 

				(agent_get_team, ":enemy_nearest_troop_team", ":enemy_nearest_agent"),
				#(team_get_leader, ":enemy_leader", ":enemy_nearest_troop_team"),
				(call_script, "script_team_get_nontroll_leader", ":enemy_nearest_troop_team"),
				(assign, ":enemy_leader", reg0),
				(gt, ":enemy_leader", 0),

				(store_mul, ":percent_enemy_cavalry", ":num_enemy_cavalry", 100),
				(val_div, ":percent_enemy_cavalry", ":num_enemies"),
				(try_begin),
					(neq, ":infantry_formation", formation_none),
					(try_begin),
						(gt, ":percent_enemy_cavalry", 66),
						(assign, ":infantry_formation", formation_square),
						#(display_message, "@Infantry decided to form square"),	#############
					(else_try),
						(neq, ":enemy_nearest_troop_class", grc_cavalry),
						(neq, ":enemy_nearest_troop_class", grc_archers),
						(neq, ":enemy_nearest_agent", ":enemy_leader"),
						(call_script, "script_battlegroup_get_size", ":enemy_nearest_troop_team", ":enemy_nearest_troop_division"),
						(gt, reg0, ":num_infantry"),	#got fewer troops?
						(call_script, "script_battlegroup_get_level", ":team_no", grc_infantry),
						(assign, ":average_level", reg0),
						(call_script, "script_battlegroup_get_level", ":enemy_nearest_troop_team", ":enemy_nearest_troop_division"),
						(gt, ":average_level", reg0),	#got better troops?
						(assign, ":infantry_formation", formation_shield),
						#(display_message, "@Infantry decided to form shield"),	#############
					(try_end),
				(try_end),
				
				#hold near archers?
				(try_begin),
					(eq, ":infantry_order", mordr_hold),
					(gt, ":num_archers", 0),
					(copy_position, pos1, Archers_Pos),
					(position_move_x, pos1, "$formai_rand8", 0), #changed -100 to rand8 (-100 to 100) JL
					(try_begin),
						(this_or_next|eq, ":enemy_nearest_troop_division", grc_cavalry),
						(gt, ":percent_level_infantry", ":percent_level_enemy_infantry"),
						(position_move_y, pos1, "$formai_rand2", 0),	#move ahead of archers in anticipation of charges -- changed 1000 to rand2 JL
					(else_try),
						(position_move_y, pos1, "$formai_rand5", 0), #changed -1000 to rand5 JL
					(try_end),
					(assign, ":spacing", 1),
					#(display_message, "@Infantry decided to hold near archers"),	#############

				#advance to nearest (preferably unmounted) enemy
				(else_try),
					#(display_message, "@Infantry decides to advance"), #############
					(try_begin),
						(eq, ":num_enemies_in_melee", 0),	#not engaged?
						(gt, ":enemy_from_archers", "$formai_rand4"), #changed AI_charge_distance to rand4 (10-22m) JL
						(lt, ":percent_enemy_cavalry", 100),
						(assign, ":distance_to_enemy_troop", ":enemy_nearest_non_cav_troop_distance"),
						(copy_position, pos60, Nearest_Non_Cav_Enemy_Troop_Pos),
						(agent_get_team, ":enemy_non_cav_team", ":enemy_nearest_non_cav_agent"),
						#(team_get_leader, reg0, ":enemy_non_cav_team"),
						(call_script, "script_team_get_nontroll_leader", ":enemy_non_cav_team"),
						(try_begin),
							(eq, reg0, -1),
							(assign, ":distance_to_enemy_group", Far_Away),
						(else_try),
							(call_script, "script_classify_agent", ":enemy_nearest_non_cav_agent"),
							(call_script, "script_battlegroup_get_position", pos0, ":enemy_non_cav_team", reg0),
							(get_distance_between_positions, ":distance_to_enemy_group", Infantry_Pos, pos0),
						(try_end),
					(else_try),
						(assign, ":distance_to_enemy_troop", ":enemy_nearest_troop_distance"),
						(copy_position, pos60, Nearest_Enemy_Troop_Pos),
						(try_begin),
							(eq, ":enemy_nearest_agent", ":enemy_leader"),
							(assign, ":distance_to_enemy_group", Far_Away),
						(else_try),
							(call_script, "script_battlegroup_get_position", pos0, ":enemy_nearest_troop_team", ":enemy_nearest_troop_division"),
							(get_distance_between_positions, ":distance_to_enemy_group", Infantry_Pos, pos0),
						(try_end),
					(try_end),
					
					(try_begin),	#attack troop if its unit is far off
						(gt, ":distance_to_enemy_group", "$formai_rand4"),
						(this_or_next|neq, ":enemy_nearest_agent", ":enemy_leader"), #added by JL to ignore leader
						(neq,"$cur_casualties","$prev_casualties"), # added by JL to have the AI not ignore the leader (5 secs) if there have been any recent losses
						(copy_position, pos0, pos60),
						(assign, ":distance_to_move", ":distance_to_enemy_troop"),
						#(display_message, "@Infantry decides to MOVE to attack enemy troop"), #############
						
					(else_try),	#attack unit
						(this_or_next|neq, ":enemy_nearest_agent", ":enemy_leader"), #added by JL to ignore leader
						(neq,"$cur_casualties","$prev_casualties"), # added by JL to have the AI not ignore the leader (5 secs) if there have been any recent losses
						(assign, ":distance_to_move", ":distance_to_enemy_group"),
						#(display_message, "@Infantry decides to attack enemy troop"), #############
						#wedge pushes through to last enemy infantry rank
						(try_begin),
							(eq, ":infantry_formation", formation_wedge),
							(val_add, ":distance_to_move", formation_minimum_spacing),
						# #non-wedge stops before first rank of enemy
						# (else_try),
							# (store_mul, reg0, formation_minimum_spacing, 2),
							# (val_sub, ":distance_to_move", reg0),
							#(display_message, "@Infantry decided to move to attack in wedge formation"), #############
						(try_end),
					(try_end),

					(copy_position, pos1, Infantry_Pos),
					(call_script, "script_point_y_toward_position", pos1, pos0),
					(try_begin),
						(le, ":distance_to_move", 1600),
						(position_move_y, pos1, ":distance_to_move"),
					(else_try),
						(position_move_y, pos1, 1500),
					(try_end),
					(call_script, "script_get_centering_amount", ":infantry_formation", ":num_infantry", 0),
					(position_move_x, pos1, reg0),
					(store_div, reg0, formation_minimum_spacing, 2),
					(position_move_x, pos1, reg0),	#combat tendency of fighting formations to rotate left
					(assign, ":spacing", 0),
				(try_end),
				
				(copy_position, pos61, pos1),	#copy for possible leader positioning
				(position_copy_rotation, pos61, pos1),
				(try_begin),
					(neq, ":infantry_formation", formation_none),
					(ge, ":num_infantry", formation_min_foot_troops),
					(call_script, "script_set_formation_position", ":team_no", grc_infantry, pos1),
					(call_script, "script_form_infantry", ":team_no", ":team_leader", ":spacing", ":infantry_formation"),		
					(team_give_order, ":team_no", grc_infantry, mordr_hold),
					#(assign, ":place_leader_by_infantry", 1), #Kham
				(else_try),
					(call_script, "script_formation_end", ":team_no", grc_infantry),
					(team_give_order, ":team_no", grc_infantry, ":infantry_order"),
					(team_set_order_position, ":team_no", grc_infantry, pos61),
					#(eq, ":infantry_order", mordr_hold), #Kham
					#(assign, ":place_leader_by_infantry", 1), #Kham
				(try_end),
			(try_end),
			
			 #GENERAL RULES OF ENGAGEMENT for Infantry, by JL:
			 #If Engaged in melee and order is charge, then full Charge Infantry (without affecting cavalry) and maybe affecting archers
			(try_begin),
				(gt, ":num_enemies_supporting_melee", 0),	 #If melee is occurring
				(try_begin), #then if
					(this_or_next|eq, ":infantry_order", mordr_charge), #infantry order is to charge
					(eq, ":archer_order", mordr_charge), #or archer orders are to charge
					(assign, "$inf_charge_activated",1), #then Charge infantry
					#(display_message,"@Infantry ordered to charge because infantry is in melee."), ##############
					(gt, ":num_archers",0),
					(eq, "$arc_charge_activated", 0),
					(call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"), #call to see the odds JL
					(le, reg0, 56), #AI is not overwhelmingly strong, so they need to throw in extra support in close combat
					(le, ":enemy_from_archers", "$formai_rand3"), #and enemy is 20-30 meters from archers
					(team_give_order, ":team_no", grc_archers, mordr_charge), #do a Native Charge
					(assign, "$arc_charge_activated", 1), #then Charge archers
					#(display_message,"@Archers ordered to charge to support melee!"), ##############
				(try_end),
			(try_end),
			
			#If Infantry is Holding and Nearest Enemy is within Self Defence range, enemy is not leader or troops have fallen then Charge (charge infantry and cavalry).
			(try_begin),
				(eq, ":infantry_order", mordr_hold), #if Orders are Hold
				(le, ":enemy_nearest_troop_distance", "$formai_rand4"), #and any enemy is within self defence distance
				(this_or_next|neq, ":enemy_nearest_agent", ":enemy_leader"), #nearest target is not the player
				(neq, "$cur_casualties","$prev_casualties2"), #troops have fallen during last second
				(assign, "$inf_charge_activated", 1), #then Charge Infantry
				#(assign, "$charge_activated", 1), #and Charge Cavalry
				#(display_message,"@Infantry ordered general charge because enemy is too near and casualties inflicted."), ##############				
			(try_end),

			#JL If enemy constitutes more than 40% then charge towards archers
			(try_begin),
				(this_or_next|eq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and infantry needs to close in with them quickly
				(eq, ":charge_against_elves", 1), #and Charge against elves is activated
				(call_script, "script_formation_end", ":team_no", grc_infantry), #JL Kham added
				(team_give_order, ":team_no", grc_infantry, mordr_charge), #charge the infantry forward towards cavalry and enemy				
			(try_end),
				
			 ##JL ACTIVATION of Inf Charge Mode when Inf AI has been deemed to need charge mode. Put here to activate charge immediately (not wait until next trigger).
			(try_begin),
				(eq, "$inf_charge_activated", 1), #if inf AI has been told to Charge
				(eq, "$inf_charge_ongoing", 0), #and switch is false
				(call_script, "script_formation_end", ":team_no", grc_infantry), #end any formations
				(team_give_order, ":team_no", grc_infantry, mordr_charge), #do a Native Charge
				(assign, "$inf_charge_ongoing", 1), #switch set to true so this function is not needed to be called again until charge mode has been disabled and a new charge has been set
				#(display_message, "@Infantry orders are Charge, Formations Inf AI disabled"), ################
			(try_end),
			
		(try_end),	#end of Infantry AI
		
		#cavalry AI
		(call_script, "script_battlegroup_get_size", ":team_no", grc_cavalry),
		(assign, ":num_cavalry", reg0),
		(call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"), #added by JL to control grand charge and move around threat charge
		(assign, ":grand_charge", reg0), #added by JL
		(val_sub, ":grand_charge", 5), #added JL 6/14/2011 Grand charge lowered so that it will prefer to do flank attacks with cav.
		(assign, ":around_charge", reg0), #added by JL
		
		#JL: don't place leader with infantry if there are more than 1 cavalry on the map:
		#(try_begin),
			#(gt, ":num_cavalry", 1),
			#(assign, ":place_leader_by_infantry", 0), #JL, added on 2/20/2011 Kham - removed
		#(try_end),
		
		#JL Patrol Mode Control
		(store_random_in_range, ":chance", 1, 101),	#chance value that is used to assign cavalry patrols and extra aggressivness while on patrol. JL
		(try_begin),
			(ge, ":chance", 97), #There is 3% chance that patrol mode will activate each second
			(neq, "$formai_patrol_mode", 1), #and if it is not already active
			(assign, "$formai_patrol_mode", 1), #assign patrol mode to 1
		(try_end), #End of Patrol Mode Control
		#(val_sub, ":around_charge", 5), #if needed use to increase the odds needed to execute the move around threat and charge routine. JL
		
		##JL ACTIVATION OF Cavalry CHARGE:
		(try_begin), ## Added by JL to force charge when charge is active and cavalry exists
			(gt, ":num_cavalry", 0),
			(eq, "$charge_activated", 1), #if Cav AI has been told to Charge
			(eq, "$charge_ongoing", 0), #switch check
			(call_script, "script_formation_end", ":team_no", grc_cavalry),
			(team_give_order, ":team_no", grc_cavalry, mordr_charge),
			(assign, "$charge_ongoing", 1), #setting switch so this function is not called again until charge mode is turned off
		#	(display_message, "@Cavarly Orders are now in Charge Mode; Formations Cav AI is disabled"),
		(try_end),	
		
		#cavalry AI
		(try_begin),
			(gt, ":num_cavalry", 0),
			
			(call_script, "script_battlegroup_get_size", ":team_no", grc_everyone), # added by JL
			(assign, ":perc_cav", ":num_cavalry"), #JL
			(val_mul, ":perc_cav", 100), #get percent JL
			(val_div, ":perc_cav", reg0), #cavalry/everyone*100 JL : used for when executing certain tactics is allowed
			
			#JL CHECK IF Infantry should move forward in charge movement to support an already charging Cavalry:
			(try_begin),
				(eq, "$charge_ongoing", 1), #if Cav AI is in Charge mode
				(this_or_next|gt, ":enemy_from_archers", "$formai_rand3"), #and if enemy is at least 20-30 meters away from archers
				(lt, ":perc_cav", 60), #or if there are less than 60% cavalry on the field
				(get_distance_between_positions, ":inf_dist_to_cav", Infantry_Pos, Cavalry_Pos), #get the distance between infantry and cavalry
				(this_or_next|le, ":enemy_from_infantry", "$formai_rand3"), #if enemy is less than or equal to 20-30m from infantry
				(le, ":inf_dist_to_cav", 8000), #or allied cav is within 80m JL to make infantry support cavalry better (was 40m)
				(le, ":enemy_from_cavalry", ":enemy_from_infantry"), #and enemies are closer or equally close to cavalry than they are to infantry
				(call_script, "script_formation_end", ":team_no", grc_infantry), #Kham
				(team_give_order, ":team_no", grc_infantry, mordr_charge), #charge the infantry	forward towards cavalry and enemy
			(try_end),	#End JL check		
			
			#get distance to nearest enemy battlegroup(s)
			(call_script, "script_battlegroup_get_level", ":team_no", grc_cavalry),
			(assign, ":average_level", reg0),
			(assign, ":nearest_threat_distance", Far_Away),
			(assign, ":nearest_target_distance", Far_Away),
			(assign, ":num_targets", 0),
			(assign, ":num_threats", 0), # added by JL
			(try_for_range, ":enemy_team_no", 0, 4),
				(call_script, "script_battlegroup_get_size", ":enemy_team_no", grc_everyone),
				(gt, reg0, 0),
				(teams_are_enemies, ":enemy_team_no", ":team_no"),
				(try_begin),
					(eq, ":enemy_team_no", "$fplayer_team_no"),
					(assign, ":num_groups", 9),
				(else_try),
					(assign, ":num_groups", 3),
				(try_end),
				(try_for_range, ":enemy_battle_group", 0, ":num_groups"),
					(call_script, "script_battlegroup_get_size", ":enemy_team_no", ":enemy_battle_group"),
					(assign, ":size_enemy_battle_group", reg0),
					(gt, ":size_enemy_battle_group", 0),
					(call_script, "script_battlegroup_get_position", pos0, ":enemy_team_no", ":enemy_battle_group"),
					(get_distance_between_positions, ":distance_of_enemy", Cavalry_Pos, pos0),
					(try_begin),	#threat or target?
						(call_script, "script_battlegroup_get_weapon_length", ":enemy_team_no", ":enemy_battle_group"),
						(assign, ":decision_index", reg0),
						(call_script, "script_battlegroup_get_level", ":enemy_team_no", ":enemy_battle_group"),
						(val_mul, ":decision_index", reg0),
						(val_mul, ":decision_index", ":size_enemy_battle_group"),
						(val_div, ":decision_index", ":average_level"),
						(val_div, ":decision_index", ":num_cavalry"),
						(try_begin),
							(neq, ":enemy_battle_group", grc_cavalry),
							(val_div, ":decision_index", 2),	#double count cavalry vs. foot soldiers
						(try_end),
						(gt, ":decision_index", 100),
						(try_begin),
							(val_add, ":num_threats", 1), #JL
							(gt, ":nearest_threat_distance", ":distance_of_enemy"),
							(copy_position, Nearest_Threat_Pos, pos0),
							(assign, ":nearest_threat_distance", ":distance_of_enemy"),
						(try_end),
					(else_try),
						(val_add, ":num_targets", 1),
						(gt, ":nearest_target_distance", ":distance_of_enemy"),
						(copy_position, Nearest_Target_Pos, pos0),
						(assign, ":nearest_target_distance", ":distance_of_enemy"),
					(try_end),
				(try_end),
			(try_end),
			
			(try_begin), #added by JL to eliminate {0,0} position bug when no target is detected
				(eq, ":num_targets", 0),
				(copy_position, Nearest_Target_Pos, Nearest_Threat_Pos),
				(assign, ":nearest_target_distance", ":nearest_threat_distance"),
			(try_end),
			
			(try_begin), #added by JL to eliminate a {0,0} Position bug when no threat is detected
				(eq, ":num_threats", 0),
				(copy_position, Nearest_Threat_Pos, Nearest_Target_Pos),
				(assign, ":nearest_threat_distance", ":nearest_target_distance"),
			(try_end),	

			(try_begin), #JL Kham -  added to eliminate a {0,0} Position bug when no threat and no target is detected (e.g. the player has only companions or troops in other divisions)
				(eq, ":num_threats", 0),
				(eq, ":num_targets", 0),
				(gt, ":num_cavalry", 0),
				(assign, "$charge_activated", 1),
				(call_script, "script_formation_end", ":team_no", grc_cavalry),
				(team_give_order, ":team_no", grc_cavalry, mordr_charge),
				(assign, ":nearest_target_distance", AI_charge_distance),
				(assign, ":nearest_threat_distance", AI_charge_distance),				
			(try_end),
			
			##JL KHAM TEST -- Distances are no good in some cases (especially before casualties have occurred ...):
			#(assign,reg10, ":cav_closest_dist"), (assign,reg11, ":nearest_target_distance"),(display_message, "@Enemy cavalry: {reg10} Target dist is: {reg11}"), ##########			
			
			(get_distance_between_positions, reg0, Nearest_Target_Pos, Nearest_Threat_Pos),
			(store_div, reg1, AI_charge_distance, 2),
			(try_begin),	#ignore target too close to threat
				(le, reg0, reg1),
				(gt, reg0, 0), #JL added to fix when there is no target and vice versa Kham
				(assign, ":nearest_target_guarded", 1),
			(else_try),
				(assign, ":nearest_target_guarded", 0),
			(try_end),

			(assign, ":cavalry_order", mordr_charge),
			(try_begin),
				(teams_are_enemies, ":team_no", 0),
				(lt, "$team1_reinforcement_stage", 2),
				(neq, "$team1_reinforcement_stage", "$attacker_reinforcement_stage"),
				(assign, ":cavalry_order", mordr_hold),
			(else_try),
				(teams_are_enemies, ":team_no", 1),
				(lt, "$team0_reinforcement_stage", 2),
				(neq, "$team0_reinforcement_stage", "$defender_reinforcement_stage"),
				(assign, ":cavalry_order", mordr_hold),
			(else_try),
				(neq, ":infantry_order", mordr_charge),
				(try_begin),
					(le, "$battle_phase", BP_Jockey),
					(assign, ":cavalry_order", mordr_hold),
				(else_try),
					(eq, ":nearest_target_distance", Far_Away),
					(try_begin),
						(eq, ":num_archers", 0),
						(assign, ":distance_to_archers", 0),
					(else_try),
						(get_distance_between_positions, ":distance_to_archers", Cavalry_Pos, Archers_Pos),
					(try_end),
					(try_begin),
						(this_or_next|gt, ":cav_closest_dist", AI_charge_distance),
						(gt, ":distance_to_archers", AI_charge_distance),
						(assign, ":cavalry_order", mordr_hold),
					(try_end),
				(try_end),
			(try_end),
			
			
			(try_begin), #added by JL since the above code doesn't seem to work
				(eq, "$formai_disengage", 1), #disengage has been assigned
				(assign, ":cavalry_order", mordr_hold),
			(try_end),
			
			#JL DISENGAGEMENT RULES:
			(try_begin), ## when any reinforcements arrive:
				(eq, "$formai_disengage", 1), #disengage has been assigned
				(assign, "$formai_disengage", 0), #turn off disengagement so next reinforcement checks can resume
				(eq, "$charge_ongoing", 1), #charge is currently ongoing
				(assign, "$charge_activated", 0), #deactivates charge mode
				(assign, "$charge_ongoing", 0), #charge no longer ongoing
			#	(display_message, "@AI Cavalry decided to resume maneuver because of reinforcements"),
			(try_end),
			
			(try_begin), ## When there are no targets or threats near
				(eq,"$charge_ongoing", 1),
				(gt, ":nearest_target_distance", AI_charge_distance),
				(gt, ":nearest_threat_distance", AI_charge_distance),
				(assign, "$charge_activated", 0), #deactivates charge mode
				(assign, "$charge_ongoing", 0), #resetting switch
			#	(display_message, "@AI Cavalry decided to resume maneuver because no enemies are near"),
			(try_end),
			
			#JL CONTINUE form AI IF NOT IN CHARGE MODE:
			(eq,"$charge_activated", 0), #if charge mode is off then continue to do Cav AI, JL
			
			(try_begin),
				(eq, ":team_no", 0),
				(assign, ":cav_destination", Team0_Cavalry_Destination),
				(assign, reg0, "$team0_percent_cavalry_are_archers"),
			(else_try),
				(eq, ":team_no", 1),
				(assign, ":cav_destination", Team1_Cavalry_Destination),
				(assign, reg0, "$team1_percent_cavalry_are_archers"),
			(else_try),
				(eq, ":team_no", 2),
				(assign, ":cav_destination", Team2_Cavalry_Destination),
				(assign, reg0, "$team2_percent_cavalry_are_archers"),
			(else_try),
				(eq, ":team_no", 3),
				(assign, ":cav_destination", Team3_Cavalry_Destination),
				(assign, reg0, "$team3_percent_cavalry_are_archers"),
			(try_end),
			
			(assign, ":charging_through_target", 0), #charging through flag by JL
			#horse archers don't use wedge
			(try_begin),
				(neq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and cav AI should move around threat to engage instead, even if they are horse archers.
				(assign, ":percent_horse_archers", reg0), #Added by JL to be used for horse archer self defense further down
				(gt, reg0, 50),
				#(call_script, "script_formation_end", ":team_no", grc_cavalry),
				(team_give_order, ":team_no", grc_cavalry, mordr_fire_at_will), #added by JL 3/12/11
				(try_begin), #Kham - Removed the below block to reduce charging
				#	(eq, ":num_archers", 0),
				#	(assign, ":cavalry_order", mordr_charge), #added by JL
				#	(team_give_order, ":team_no", grc_cavalry, mordr_charge),
				#	(display_message, "@Charging CavArch because no foot archers are present"), ################
				#(else_try), #this else block added by JL
					(this_or_next|gt, ":num_enemies_in_melee", 0),	 #If infantry melee is occurring
					(this_or_next|le, ":enemy_from_infantry", AI_Self_Defence_Distance), #or if enemy is less than or equal to 10m from infantry
					(le, ":enemy_from_archers", AI_Self_Defence_Distance),	#or enemy is less than or equal to 10m from archers
					(assign, "$charge_activated", 1), #activate charge order
					#(assign, ":cavalry_order", mordr_charge), #added soft charge (alert mode) JL
					#(team_give_order, ":team_no", grc_cavalry, mordr_charge),
				#	(display_message, "@Alerting horse archers because melee is ongoing"), ################					
				(else_try),
					(team_give_order, ":team_no", grc_cavalry, ":cavalry_order"),
					(copy_position, ":cav_destination", Archers_Pos),
					(position_move_y, ":cav_destination", -500, 0),
					(position_move_x, ":cav_destination", "$formai_rand0", 0), #added by JL Horse archers place themselves -10m to 10m beside the Archers. Unless in patrol then they are at -20 to 20m
					(team_set_order_position, ":team_no", grc_cavalry, ":cav_destination"),
				#	(display_message, "@Directing Ranged Cavalry near Archers"), ################
				(try_end),
				
			#close in with no unguarded target farther off, free fight
			(else_try),
				(eq, ":cavalry_order", mordr_charge),
				(le, ":cav_closest_dist", AI_charge_distance),
				(try_begin),
					(eq, ":num_targets", 1),
					(eq, ":nearest_target_guarded", 0),
					(gt, ":nearest_target_distance", ":nearest_threat_distance"),
					(assign, reg0, 0),
				(else_try),
					(ge, ":num_targets", 2),
					(eq, ":nearest_target_guarded", 1),
					(assign, reg0, 0),
				(else_try),
					(assign, reg0, 1),
				(try_end),
				(eq, reg0, 1),
				(team_get_movement_order, reg0, ":team_no", grc_cavalry),
				(try_begin),
					(neq, reg0, mordr_charge),
					(this_or_next|eq, ":nearest_target_guarded", 1), #cav should not be distracted by enemy solo targets (unless there are new casualties) JL
					(neq, "$cur_casualties", "$prev_casualties2"), #JL casualties incurred during last second
					(assign, "$charge_activated", 1), #added by JL for charge control
					(call_script, "script_formation_end", ":team_no", grc_cavalry),
					(team_give_order, ":team_no", grc_cavalry, mordr_charge),
				#	(display_message, "@Closing in and charging Cav (free fight)"), ################
				(try_end),
				
			#grand charge if target closer than threat AND not guarded AND odds are in favour AND we have a good sized amount of cavalry:
			
			(else_try),
				(neq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and cav AI should move around threat to engage instead.
				(ge, ":grand_charge", "$formai_rand7"), # added by JL --> decision number = battle presence + ([avg_lvl]/3)
				(ge, ":perc_cav", 50), #if >= 50% of total AI troop size is Cavalry JL
				(le, ":nearest_target_distance", ":nearest_threat_distance"), #JL changed lt to le in case there are no targets/threats.
				(eq, ":nearest_target_guarded", 0),
				(call_script, "script_formation_end", ":team_no", grc_cavalry),
				(team_give_order, ":team_no", grc_cavalry, mordr_hold),
			#	(display_message, "@Holding Cav before 'Grand charge'"), ################
				#lead archers up to firing point
				(try_begin),
					(gt, ":nearest_target_distance", "$formai_rand6"), #changed AI_firing_distance (65m) to 40-50m to get the AI closer JL
					(eq, ":cavalry_order", mordr_hold),
					(try_begin),
						(eq, ":num_archers", 0),
						(copy_position, ":cav_destination", Cavalry_Pos),	#must be reinforcements, so gather at average position
					(else_try),						
						(copy_position, ":cav_destination", Archers_Pos),
						(position_move_y, ":cav_destination", "$formai_rand3", 0), #changed AI_charge_distance to rand3 JL
					#	(display_message, "@Leading archers up to firing point to the 'Grand charge'"), ################
					(try_end),
					
				#then CHARRRRGE!
				(else_try),
					(copy_position, ":cav_destination", Cavalry_Pos),
					(call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
					(position_move_y, ":cav_destination", ":nearest_target_distance", 0),
				#	(display_message, "@Grand charging cavalry agains target!"), ################
				(try_end),
				(team_set_order_position, ":team_no", grc_cavalry, ":cav_destination"),
				
				
			#make a wedge somewhere
			(else_try),	
				#JL Change the odds criterion for charge around to low value if enemies are near so that the cavalry starts "surprise" flanking
				(try_begin),
					(neq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and cav AI should move around threat to engage instead.
					(le, ":nearest_target_distance", 30), #if there is a target within 30m distance
					(lt, ":around_charge", "$formai_rand7"), #and odds are bad so the cavalry will not try a flank attack on the target.
					#(neq, "$formai_rand7", 30), #and if charge odds comparator has not been lowered already
					(assign, "$formai_rand7", 40), #assign odds comparator to 40
				(else_try), #otherwise:
					(eq, "$formai_rand7", 40), #if charge odds has been lowered already
					(store_random_in_range, "$formai_rand7", 55, 66), #put the odds comparator back to random higher value
				(try_end), #JL
				
				#JL Set cavalry to aggressively move towards archers if there are 45% or more of them:
				(try_begin),
					(this_or_next|gt, ":perc_enemy_others", 60), #if enemy others constitute more than 45% of total enemy #kham - changed to 60%
					(gt, ":perc_enemy_elves", 30), #Or If enemy elves consitute more than 30% of the enemy
					(assign, ":cavalry_order", mordr_charge),
					(assign, "$formai_rand7", 35), #lower the odds requirement for around charge to 35
				(else_try),
					(eq, "$formai_rand7", 35), #if the odds have been lowered to 35 before
					(store_random_in_range, "$formai_rand7", 55, 66), #put the odds comparator back to random higher value
				(try_end),
				
				(try_begin),
					(gt, ":num_targets", 0), #JL Kham - To charge through a target there needs to be a target
					(eq, ":cavalry_order", mordr_charge),
					(copy_position, ":cav_destination", Cavalry_Pos),
					(this_or_next|ge, ":perc_cav", 80), #if Cav size >= 80% of total AI troop size JL
					(ge, ":around_charge", "$formai_rand7"), #or if odds are good (if odds are not good (lower than 55-65) and there are less than 80 cav --> try other tactics) added by JL					
					(call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
					(position_move_y, ":cav_destination", ":nearest_target_distance", 0), 
					(position_move_y, ":cav_destination", AI_charge_distance, 0),
					(assign, ":charging_through_target", 1), #charging through flag by JL
				#	(display_message, "@'Charging' Cav through target to other side"), ################
				(else_try),
					(neq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and cav AI should move around threat to engage instead.
					(gt, ":num_archers", 0),
					(copy_position, ":cav_destination", Archers_Pos),	#hold near archers
					(position_move_x, ":cav_destination", "$formai_rand0", 0), #changed 500 to $formai_rand0 (-10m to 10m right/left) JL
					(position_move_y, ":cav_destination", "$formai_rand1", 0), #added (0m to 5m infront) JL
					(try_begin), #move cavalry as a patrol 3% chance every second JL
						(ge, ":chance", 97), #JL
						(store_random_in_range, "$formai_rand0", -2000, 2000), #x-factor update to -20/20 JL
						(position_move_x, ":cav_destination", "$formai_rand0", 0), #patrol positioning JL
						(position_move_y, ":cav_destination", "$formai_rand1", 0), #added another temporary (0m to 5m infront) JL
					(try_end),
				#	(display_message, "@Holding Cav near archers"), ################
				(else_try), #if no archers are present hold near infantry JL
					(neq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and cav AI should move around threat to engage instead.
					(gt, ":num_infantry", 0),
					(copy_position, ":cav_destination", Infantry_Pos),	#hold near infantry JL
					(position_move_x, ":cav_destination", "$formai_rand0", 0), #changed 500 to $formai_rand0 (-10m to 10m right/left) JL
					(position_move_y, ":cav_destination", "$formai_rand1", 0), #added (0m to 5m infront) JL
					(try_begin), #move cavalry as a patrol 3% every scond JL
						(ge, ":chance", 97), #JL
						(store_random_in_range, "$formai_rand0", -2000, 2000), #x-factor update JL
						(position_move_x, ":cav_destination", "$formai_rand0", 0), #patrol positioning JL
						(position_move_y, ":cav_destination", "$formai_rand1", 0), #added another (0m to 5m infront) JL
					(try_end),					
				#	(display_message, "@Holding Cav near infantry"), ################
				(else_try), #JL
					(gt, ":num_targets", 0), #JL Kham - To charge through a target there needs to be a target
					(eq, ":cavalry_order", mordr_charge), #cavalry are in charge order JL
					(lt, ":around_charge", "$formai_rand7"), #and odds are bad (but there is only cavalry on the field) JL
					(call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
					(position_move_y, ":cav_destination", ":nearest_target_distance", 0), 
					(position_move_y, ":cav_destination", AI_charge_distance, 0),
					(assign, ":charging_through_target", 1), #charging through flag by JL
				#	(display_message, "@'Charging' Cav through target to other side despite low odds"), ################
				(else_try), #JL Kham
					(eq, ":num_targets", 0), #JL Kham - if there are no targets, then move straight at the threat to engage
					(assign, ":charging_through_target", 2), #JL Kham- new to make sure the silly Cav actually charges the threat better
					(call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Threat_Pos),
					(position_move_y, ":cav_destination", ":nearest_threat_distance", 0), 
					(position_move_y, ":cav_destination", AI_charge_distance, 0),	#charge on through to the other side of threat		
				#	(display_message, "@'Charging' Cav through threat because there are no targets!!"), ################
				(else_try), #cavalry order must be mordr_hold, so:
					(copy_position, ":cav_destination", Cavalry_Pos), #must be reinforcements, so gather at average position
				#	(display_message, "@Cav moving to average position"), ################	
				(try_end),			

				#move around threat in the way to destination
				(try_begin),
					(gt, ":num_threats", 0), #there must be a threat if we are to move around it -- JL
					(gt, ":num_targets",0), #and if there needs to be a target, otherwise it is not good to go around because the cav will veer and be at disadvantage! Kham
					(call_script, "script_point_y_toward_position", Cavalry_Pos, Nearest_Threat_Pos),
					(call_script, "script_point_y_toward_position", Nearest_Threat_Pos, ":cav_destination"),
					(position_get_rotation_around_z, reg0, Cavalry_Pos),
					(position_get_rotation_around_z, reg1, Nearest_Threat_Pos),
					(store_sub, ":rotation_diff", reg0, reg1),
					(try_begin),
						(lt, ":rotation_diff", -180),
						(val_add, ":rotation_diff", 360),
					(else_try),
						(gt, ":rotation_diff", 180),
						(val_sub, ":rotation_diff", 360),
					(try_end),
					
					(try_begin),
						(is_between, ":rotation_diff", -135, 136),
						(copy_position, ":cav_destination", Cavalry_Pos),
						(assign, ":distance_to_move", AI_firing_distance),
					#	(display_message, "@Rotation is between -135 and 135"), ################
						(try_begin),	#target is left of threat
							(is_between, ":rotation_diff", -135, 0),
							(val_mul, ":distance_to_move", -1),
					#		(display_message, "@Move around: target is left of threat"), ################
						(try_end),
						(position_move_x, ":cav_destination", ":distance_to_move", 0),
						(store_sub, ":distance_to_move", ":nearest_threat_distance", AI_firing_distance),
						(position_move_y, ":cav_destination", ":distance_to_move", 0),
						(call_script, "script_point_y_toward_position", ":cav_destination", Cavalry_Pos),
						(position_rotate_z, ":cav_destination", 180),
					(try_end),
				(try_end),
				(get_scene_boundaries, pos0, pos1),
				(position_get_x, reg0, ":cav_destination"),
				(position_get_x, reg1, pos0),
				(val_max, reg0, reg1),
				(position_get_x, reg1, pos1),
				(val_min, reg0, reg1),
				(position_set_x, ":cav_destination", reg0),
				(position_get_y, reg0, ":cav_destination"),
				(position_get_y, reg1, pos0),
				(val_max, reg0, reg1),
				(position_get_y, reg1, pos1),
				(val_min, reg0, reg1),
				(position_set_y, ":cav_destination", reg0),
	
				(position_set_z_to_ground_level, ":cav_destination"),
				(call_script, "script_set_formation_position", ":team_no", grc_cavalry, ":cav_destination"),
				(copy_position, pos1, ":cav_destination"),
				(call_script, "script_form_cavalry", ":team_no", ":team_leader", 0),
				(try_begin),
					(ge, reg0, formation_min_cavalry_troops),
					(team_give_order, ":team_no", grc_cavalry, mordr_hold),
				#	(display_message, "@Gathering Cavalry to go around threat"), ################
				(else_try),
					(call_script, "script_formation_end", ":team_no", grc_cavalry),
					(team_give_order, ":team_no", grc_cavalry, ":cavalry_order"),
					(team_set_order_position, ":team_no", grc_cavalry, ":cav_destination"),
				#	(display_message, "@Directing Cav Around Threat"), ################
				(try_end),
			(try_end),
			
			 #GENERAL RULES of ENGAGEMENT by JL:			 
			# (store_random_in_range, ":imp_charge", 1, 101), #Impetousness factor (random value between 1 to 100) JL 
			 
			 #If Target is Near And [Charge Ordered] and not charging through target then if ... Start offensive Charge otherwise let Cavalry charge through
			(try_begin),
				(le, ":nearest_target_distance", AI_charge_distance), #if there is a target within charge distance (or threat if there is no target)
				(eq, ":cavalry_order", mordr_charge), #and cav orders are to charge
				(eq, ":charging_through_target", 0), #and not charging through target -- take this away if cavalry is suddenly stopping Kham - added
				(try_begin),  # if AI has 50% or more cavalry
					(this_or_next|gt, ":nearest_threat_distance", AI_charge_distance), #if there is no threat within charge distance
					(ge, ":perc_cav", 50), #or if Cavalry >= 50% of total AI troop size JL
					(assign, "$charge_activated", 1), #then charge
				#	(display_message,"@Cavalry charge ordered because target is within charge distance."), ##############
				(else_try), #if AI has 20% or more cavalry and one of its other troop types is close to the enemy
					(ge, ":perc_cav", 20), #if Cavalry >= 20% of total AI troop size JL
					(try_begin), #then if
						(this_or_next|le, ":enemy_from_infantry", "$formai_rand3"), #if enemy is less than or equal to 20m to 30m from infantry
						(this_or_next|le, ":enemy_from_archers", "$formai_rand3"),	#or enemy is less than or equal to 20m to 30m from archers
					#	(ge, ":imp_charge", 97), #there is 4% chance every second that the cavalry will charge anyway because of impetousness
						(assign, "$charge_activated", 1), #then charge
					#	(display_message,"@Cavalry charge ordered because target is within charge distance."), ##############
					(try_end),
				(else_try), #if less than 20% cavalry only counter charge if other troops are ordered to charge or melee is ongoing
					(this_or_next|gt, ":num_enemies_in_melee", 0),	 #If inf melee is occurring
					(this_or_next|eq, ":infantry_order", mordr_charge), #or infantry order is to charge
					(this_or_next|eq, ":archer_order", mordr_charge), #or archer orders are to charge
					(this_or_next|le, ":enemy_from_infantry", AI_Self_Defence_Distance), #if enemy is less than or equal to 10m from infantry
					(this_or_next|le, ":enemy_from_archers", AI_Self_Defence_Distance),	#or enemy is less than or equal to 10m from archers					
				#	(ge, ":imp_charge", 99), #there is 2% chance every second that the cavalry will charge anyway because of impetousness
					(assign, "$charge_activated", 1), #then charge
				#	(display_message,"@Cavalry charge ordered because target is within charge distance."), ##############
				(try_end),
			(try_end),
			
			#If a threat or a target is within charge distance And ([casualties have been inflicted recently] Or [nearest target is guarded And Cavalry is holding]), then start a Counter Charge
			(try_begin),
				(this_or_next|le, ":nearest_target_distance", AI_charge_distance), #if there is a target within charge distance
				(this_or_next|le, ":nearest_threat_distance", AI_charge_distance), #or if there is a threat within charge distance
				(le, ":cav_closest_dist","$formai_rand3"), #nearest enemy cavalry is within charge distance JL Jun28b
				(eq, ":charging_through_target", 0), #and not charging through target - if AI is too passive, then remove this line <-- Kham
				(try_begin),
					(neq, "$cur_casualties","$prev_casualties2"), #if there are very recent casualties then charge because someone is harming someone
					#(ge, ":imp_charge", 50), #there is 50% chance that the cavalry will charge because of impetousness
					(assign, "$charge_activated", 1),
				#	(display_message,"@Enemies are close to cavalry and casualties have recently been inflicted. Counter-Charging cavalry."), #############
				(else_try), #if no casualties have occurred recently then immobile cavalry still needs to charge
					(neq, ":nearest_target_guarded", 0), #if the nearest target is not an unguarded target
					(eq, ":cavalry_order", mordr_hold), #and if Cav order is hold
					(assign, "$charge_activated", 1),
				#	(display_message,"@Enemies are close to cavalry and cavalry is standing still. Ordering cavalry to do a counter charge."), #############
				#(else_try), <-- This block removed - Kham
					#(ge, ":imp_charge", 97), #there is 4% chance every second that the cavalry will charge anyway because of impetousness
					#(eq, ":cavalry_order", mordr_hold), #and if Cav order is hold
					#(assign, "$charge_activated", 1),					
				(try_end),
			(try_end),
			
			#extra pre-emptive defence for cavalry if cavalry is holding (defensive stance) or odds are low:
			(try_begin),
				(this_or_next|eq, ":cavalry_order", mordr_hold), #if Cav order is hold
				(lt, ":around_charge", 50), #or the odds are low
				#(eq, ":nearest_target_guarded", 1), #and if the nearest target is guarded
				(try_begin),
					(this_or_next|le, ":enemy_from_infantry", "$formai_rand3"), #if enemy is less than or equal to 20-30m from infantry
					(this_or_next|le, ":enemy_from_cavalry", "$formai_rand3"), #or enemy is less than or equal to 20-30m from cavalry	
					(le, ":enemy_from_archers", "$formai_rand3"),	#or enemy is less than or equal to 20-30m from archers	
					(assign, "$charge_activated", 1),
				#	(display_message,"@Enemies are close to AI and cavalry is standing still. Ordering cavalry to do a counter charge."), #############
				#JL Patrol Mode if cavalry is on hold:
				(else_try), #if chance >= 97 then cavalry is in patrol mode. 
					(eq, "$formai_patrol_mode", 1), #cavalry is in patrol mode with heightened alert against enemy cavalry
					(try_begin),
						(le, ":cav_closest_dist", 4000), #any enemy cavalry is less than or equal to 40m from
						(le, ":cav_closest_dist", ":enemy_from_cavalry"), #and nearest [enemy cavalry] is less than or at equal distance as the nearest enemy group is from the VI cavalry
						(this_or_next|gt, ":enemy_from_infantry", "$formai_rand3"), #and enemy is at least 20-30m away from VI infantry
						(gt, ":enemy_from_archers", "$formai_rand3"),	#or enemy is less than or equal to 20-30m from archers						
						(try_begin), #start moving to either nearest threat or nearest target:
							(eq, ":nearest_threat_distance", ":cav_closest_dist"), #if nearest threat distance is equal to nearest enemy cavalry
							(copy_position, ":cav_destination", Cavalry_Pos),
							(call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Threat_Pos),
							(position_move_y, ":cav_destination", ":nearest_threat_distance", 0),
							(position_move_y, ":cav_destination", AI_Self_Defence_Distance, 0),	#"charge" on through to the other side of the threat/target cavalry--	changed 20m to 10m Kham
						(else_try),
							(call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
							(position_move_y, ":cav_destination", ":nearest_target_distance", 0),
							(position_move_y, ":cav_destination", AI_Self_Defence_Distance, 0),	#"charge" on through to the other side of the threat/target cavalry--	changed 20m to 10m Kham					
						(try_end),
						(try_begin), #charge if in patrol mode and enemy is near
							(this_or_next|le, ":cav_closest_dist", AI_charge_distance), #if enemy cav is within charge distance, then charge
							(this_or_next|le, ":nearest_target_distance", AI_charge_distance), #or if enemy target is within charge distance, then charge
							(le, ":nearest_threat_distance", AI_charge_distance), #or if enemy threat is within charge distance, then charge
							(assign, "$charge_activated", 1), #do a full charge	
						(try_end),
					(else_try),
						(assign, "$formai_patrol_mode", 0), #puts patrol mode back to 0 if the conditions are not met
						(this_or_next|le, ":cav_closest_dist", AI_charge_distance), #if enemy cav is within charge distance, then charge
						(this_or_next|le, ":nearest_target_distance", AI_charge_distance), #or if enemy target is within charge distance, then charge
						(le, ":nearest_threat_distance", AI_charge_distance), #or if enemy threat is within charge distance, then charge
						(assign, "$charge_activated", 1), #do a full charge							
					(try_end),
				(try_end),	#JL					
			(try_end),
			
			#JL Extra self defense/offense for Archer Cavalry: If enemy is near Then Charge
			(try_begin),
				#(eq, ":cavalry_order", mordr_hold), #if Cav order is hold
				(gt, ":percent_horse_archers",50),
				#(display_message,"@Checking Held Cavalry for Self-Defense."), ##############
				(try_begin),
					(this_or_next|le, ":nearest_target_distance", "$formai_rand3"), #Nearest threat is 20-30m away
					(this_or_next|le, ":nearest_threat_distance", "$formai_rand3"), #or nearest target is 20-30m away
					(this_or_next|le, ":enemy_from_cavalry", "$formai_rand3"), #or enemy is less than or equal to 20-30m from cavalry
					(this_or_next|le, ":enemy_from_infantry", "$formai_rand3"), #or enemy is less than or equal to 20-30m away from infantry
					(this_or_next|le, ":enemy_from_archers", "$formai_rand3"),	#or enemy is less than or equal to 20-30m away from archers						
					(le, ":cav_closest_dist","$formai_rand3"), #nearest enemy cavalry is within charge distance JL Kham
					(assign, "$charge_activated", 1),
				#	(display_message,"@Horse Archers ordered to Charge because enemy is within self defense distance."), ##############
				(try_end),
			(try_end),			
			
			#JL start charge mode if charging through and target is within 20 m and threat is not as close as target:
			(try_begin),
				(eq, ":charging_through_target", 1), #cavalry is set to charge through (around threat and towards target)
				(le, ":nearest_target_distance", AI_charge_distance), #if there is a target within charge distance (or threat if there is no target)
				(ge, ":nearest_threat_distance", ":nearest_target_distance"), #and the target is closer than the threat
				(call_script, "script_formation_end", ":team_no", grc_cavalry),
				(team_give_order, ":team_no", grc_cavalry, mordr_charge),
			#	(display_message,"@Targets are close to cav: Charging cavalry into and through target."), #############
				#permanent charge if infantry or archers are in charge mode, added Kham
				(try_begin),
					(this_or_next|eq, "$inf_charge_activated", 1), #if infantry is hard charging
					(this_or_next|eq, "$arc_charge_activated", 1), #or archers are hard charging
					#(ge, ":imp_charge", 90), #there is a 10% chance that they will perma charge in this situation so around 10 seconds of activity and then a charge ensues. <-Jun18 update
					(assign, "$charge_activated", 1), #tell cavalry to stop formations and charge hard 
				#	(display_message,"@Targets are close to cav and foot soldiers need support. Charging through permanently."), #############
				(try_end),				
			(try_end),
			
			#JL added Jun28 3.303: If the enemy number of alive agents on the field are 10 or fewer then charge cavalry fully (regardless of other circumstances).
			(try_begin),			
				(lt, ":num_enemies", 11),
				(assign, "$charge_activated", 1), #tell cavalry to charge hard
			#	(display_message,"@Less than 10 enemies. Charging all cavalry."), #############
			(try_end),
			
			#JL added Jun28 3.303 start charge mode if charging through threat (no targets avaialble) and threat is within 40 m:
			(try_begin),
				(eq, ":charging_through_target", 2), #cavalry is set to charge through (around threat and towards target)
				(this_or_next|le, ":nearest_threat_distance", "$formai_rand3"), #nearest threat is 20-30m away
				(le, ":cav_closest_dist","$formai_rand3"), #nearest enemy cavalry is within charge distance Jun28b
				(assign, "$charge_activated", 1), #tell cavalry to charge hard
			#	(display_message,"@No targets available and threat is 40m away. Charging cavalry to meet threat properly."), #############
			(try_end),
			
			
			# JL Charge mode ACTIVATOR to make charge take effect immediately:
			(try_begin), ## Charge mode controller to make charge take effect immediately:
				(gt, ":num_cavalry", 0),
				(eq, "$charge_activated", 1),
				(eq, "$charge_ongoing", 0), #switch check
				(call_script, "script_formation_end", ":team_no", grc_cavalry),
				(team_give_order, ":team_no", grc_cavalry, mordr_charge),
				(assign, "$charge_ongoing", 1), #setting switch so this function is not called again until charge mode is turned off
			#	(display_message, "@Cavalry Charge Mode Active Formations Cav AI is disabled"),
			(try_end), #JL		
		(try_end), #end of Cav AI


		(agent_get_troop_id, ":hero_troop", ":team_leader"),

		#put leader in duel or place leader -- JL added code for put leader in duel
		(try_begin),
			#basic conditions:
			(gt, ":hero_troop", 0), #The current team must have a leader
			(is_between, ":hero_troop", heroes_begin, heroes_end), #Must be hero
			(agent_is_alive, ":team_leader"), #and the team leader must be alive
			#(agent_slot_eq, ":team_leader", slot_agent_is_running_away, 0), #and the leader must not be running away ... will never happen
			(store_agent_hit_points, ":leader_hp", ":team_leader"), #gets leaders hit point percent
			(ge, ":leader_hp", 25), #and AI leader has more than 25% hit points (- he'll not want to duel any more when he's too wounded)
			(get_player_agent_no, "$fplayer_agent_no"), #get the player agent ID
			(agent_is_alive, "$fplayer_agent_no"), #and the player has to be alive
			(teams_are_enemies, "$fplayer_team_no", ":team_no"), #JL: the current VI team needs to be a hostile to the player's team
			(gt, ":nearest_threat_distance", 2000), #and if there is no cavalry threat within 30m - 20m
			#(eq, ":enemy_nearest_gen_agent", "$fplayer_agent_no"), #and the nearest enemy unit (in relation to either AI inf or cav) must be the player character
			#(eq, ":nearest_target_guarded", 0), #and the nearest cavalry target is unguarded
			#if basic conditions are met then 
			(agent_get_position, pos17, "$fplayer_agent_no"), #get the position of the player
			(agent_get_position, pos18, ":team_leader"),	#get position of AI leader
			(get_distance_between_positions, ":duel_distance", pos18, pos17), #get the (duel) distance between AI leader and player
			(le, ":duel_distance", 1000), #if duel distance is 10m or less - changed to 10m
		#	(display_message, "@Team leader moves towards the player"),
			(agent_set_scripted_destination, ":team_leader", pos17, 1),
			(try_begin),
				(le, ":duel_distance",50), #if duel distance is 25m or less - changed to 5m
				#(agent_ai_set_always_attack_in_melee, ":team_leader", 1), #set the leader to offensive mode?
				(agent_clear_scripted_mode, ":team_leader"),
				(agent_set_division, ":team_leader", grc_heroes), #set the leader to group 3 (= grc_heroes)
				(team_give_order, ":team_no", grc_heroes, mordr_charge), #charge any heroes (the leader). This overrides the movement to player position.
		#		(display_message, "@Team leader charges the player"),
			(try_end),
		(else_try),
			#---------------Normal form AI code for placing leader -- JL: let leader be in scripted mode before the fight starts only. And the leader primarily follows his cavalry if leader is on horse and has cavalry
			(gt, ":team_leader", 0),
			(is_between, ":hero_troop", heroes_begin, heroes_end), #Must be hero
			(agent_is_alive, ":team_leader"),

				(try_begin), #JL Kham added block to get rid of straying lords				
					(agent_get_horse, ":agent_horse_id", ":team_leader"),
					(ge, ":agent_horse_id", 0),			
					(agent_set_division, ":team_leader", grc_cavalry), #set the leader to cav
				(else_try),
					(agent_set_division, ":team_leader", grc_infantry), #set the leader to inf
				(try_end),
			
			(try_begin),
				(lt, "$battle_phase", BP_Fight), #JL
				(gt, ":num_cavalry", 1), #JL: at least 2 cavalry (including leader)
				(agent_get_horse, ":agent_horse_id", ":team_leader"), #JL
				(ge, ":agent_horse_id", 0), #JL
				(copy_position, pos18, Cavalry_Pos), #JL
				(position_copy_rotation, pos18, Cavalry_Pos), #JL Kham
				#(position_move_x, pos18, "$formai_rand8", 0), #JL: put leader -1m to +1 in x-direction relative to cavalry position
				(agent_set_scripted_destination, ":team_leader", pos18, 1), #JL
			#	(display_message, "@Team leader positions with cavalry"),
			(else_try),
				(lt, "$battle_phase", BP_Fight), #JL
				(gt, ":num_infantry", 0),
				#(neq, ":place_leader_by_infantry", 0), #MAY HAVE TO REMOVE THIS LINE IF BUG PERSISTS.
				#(agent_slot_eq, ":team_leader", slot_agent_is_running_away, 0), #THIS LINE CAN BE COMMENTED OUT
				(copy_position, pos18, Infantry_Pos), #JL Kham: commented out the lines that were using pos61 because pos61 may be corrupted by other code
				(position_copy_rotation, pos18, Infantry_Pos), #JL Kham
				(agent_set_scripted_destination, ":team_leader", pos18, 1), #JL Kham: commented out the lines that were using pos61 because pos61 may be corrupted by other code
				#(position_move_x, pos61, 100, 0),
				#(agent_set_scripted_destination, ":team_leader", pos61, 1),
			(else_try), #JL Kham: simplified and moved after checking on infantry
				(lt, "$battle_phase", BP_Fight),
				(gt, ":num_archers", 0),
				(copy_position, pos18, Archers_Pos),
				(position_copy_rotation, pos18, Archers_Pos),
				(position_move_y, pos18, 1000, 0),
				(agent_set_scripted_destination, ":team_leader", pos18, 1),			
			(else_try), #if we are in battle phase or if none of the above applied
				(agent_clear_scripted_mode, ":team_leader"),
				(agent_get_division, ":leader_div", ":team_leader"), #JL Kham added the following code for the team leader:
				(eq, ":leader_div", grc_heroes),
				(try_begin),				
					(agent_get_horse, ":agent_horse_id", ":team_leader"),
					(ge, ":agent_horse_id", 0),			
					(agent_set_division, ":team_leader", grc_cavalry), #set the leader to cav
				(else_try),
					(agent_set_division, ":team_leader", grc_infantry), #set the leader to inf
				(try_end),
		#		(display_message, "@Team leader cleared of scripted mode"),
			(try_end),
			#--------------End Original form AI code
		(try_end),
	(try_end)
	]),

] or [

# MB Version of Field Melee Tactics - Kham
  # script_team_field_melee_tactics by motomataru
  # Input: AI team, size relative to largest team in %, size relative to battle in %
  # Output: none
  ("team_field_melee_tactics", [
	(store_script_param, ":team_no", 1),
#	(store_script_param, ":rel_army_size", 2),
	(store_script_param, ":battle_presence", 3),
	(call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"),
	
	##JL code for checking disengagement by reinforcements:
	(try_begin),
		(eq, "$formai_disengage", 0), #if we have no disengagement ordered yet then
		
		(store_normalized_team_count, ":num_attackers", 1), #added by JL to use for determining reinforcements (and possibly future other factors)
		(store_normalized_team_count, ":num_defenders", 0), #added by JL to use for determining reinforcements (and possibly future other factors)

		(try_begin), #for attackers:
			(lt, ":num_attackers", 6), #if number of attackers are 5 or less
			(eq, "$att_reinforcements_arrived", 0), #and attacker reinforcements have not arrived
			(assign, "$att_reinforcements_needed", 1), #set attacker reinforcements are needed
		(try_end),
		(try_begin),
			(ge, ":num_attackers", 6), #if number of attacker or defenders are more than 5
			(eq, "$att_reinforcements_needed", 1), # and attacker reinforcements were needed
			(assign, "$att_reinforcements_arrived", 1), #set attacker reinforcements to have arrived
			(assign, "$att_reinforcements_needed", 0), #set attacker reinforcements are not needed
			(assign, "$formai_disengage", 1), #set flag that disengagement is ok
			#(display_message, "@Attacker reinforcements have arrived"), #############
		(try_end),
		
		(try_begin), #for defenders:
			(lt, ":num_defenders",6), #if number of defenders are 5 or less
			(eq, "$def_reinforcements_arrived", 0), #and defender reinforcements have not arrived
			(assign, "$def_reinforcements_needed", 1), #set defender reinforcements are needed
		(try_end),
		(try_begin),
			(ge, ":num_defenders", 6), #if number of defenders are more than 5
			(eq, "$def_reinforcements_needed", 1), # and defender reinforcements were needed
			(assign, "$def_reinforcements_arrived", 1), #set defender reinforcements to have arrived
			(assign, "$def_reinforcements_needed", 0), #set defender reinforcements are not needed
			(assign, "$formai_disengage", 1), #set flag that disengagement is ok
			#(display_message, "@Defender reinforcements have arrived"), #############
		(try_end),
	(try_end),
	##End JL code
	
	
	#mop up if outnumber enemies more than 6:1
	(try_begin),
		(gt, reg0, 86),
		(call_script, "script_formation_end", ":team_no", grc_infantry),
		(team_give_order, ":team_no", grc_infantry, mordr_charge),
		(call_script, "script_formation_end", ":team_no", grc_cavalry),
		(team_give_order, ":team_no", grc_cavalry, mordr_charge),

	(else_try),
		#find closest distance of enemy to infantry, cavalry troops
		(assign, ":inf_closest_dist", Far_Away),
		(assign, ":inf_closest_non_cav_dist", Far_Away),
		(assign, ":cav_closest_dist", Far_Away),
		(assign, ":num_enemies_in_melee", 0),
		(assign, ":num_enemies_supporting_melee", 0),
		(assign, ":num_enemy_infantry", 0),
		(assign, ":num_enemy_cavalry", 0),
		(assign, ":num_enemy_others", 0),
		(assign, ":sum_level_enemy_infantry", 0),
		(assign, ":x_enemy", 0),
		(assign, ":y_enemy", 0),
		(try_for_agents, ":enemy_agent"),
			(agent_is_alive, ":enemy_agent"),
			(agent_is_human, ":enemy_agent"),
			(agent_get_team, ":enemy_team_no", ":enemy_agent"),
			(teams_are_enemies, ":enemy_team_no", ":team_no"),
            
            (agent_get_troop_id, ":enemy_troop", ":enemy_agent"),
            (troop_get_type, ":enemy_race", ":enemy_troop"),
			(neq, ":enemy_race", tf_troll), #disregard trolls

			(agent_get_class, ":enemy_class_no", ":enemy_agent"),
			(try_begin),
				(eq, ":enemy_class_no", grc_infantry),
				(val_add, ":num_enemy_infantry", 1),
				(agent_get_troop_id, ":enemy_troop", ":enemy_agent"),
				(store_character_level, ":enemy_level", ":enemy_troop"),
				(val_add, ":sum_level_enemy_infantry", ":enemy_level"),
			(else_try),
				(eq, ":enemy_class_no", grc_cavalry),
				(val_add, ":num_enemy_cavalry", 1),
			(else_try),
				(val_add, ":num_enemy_others", 1),
			(try_end),
			(agent_get_position, pos0, ":enemy_agent"),
			(position_get_x, ":value", pos0),
			(val_add, ":x_enemy", ":value"),
			(position_get_y, ":value", pos0),
			(val_add, ":y_enemy", ":value"),
			(assign, ":enemy_in_melee", 0),
			(assign, ":enemy_supporting_melee", 0),
			(try_for_agents, ":cur_agent"),
				(agent_is_alive, ":cur_agent"),
				(agent_is_human, ":cur_agent"),
				(agent_get_team, ":cur_team_no", ":cur_agent"),
				(eq, ":cur_team_no", ":team_no"),
				(agent_get_class, ":cur_class_no", ":cur_agent"),
				(try_begin),
					(eq, ":cur_class_no", grc_infantry), #this block will not be traversed if there is no Infantry ... JL
					(agent_get_position, pos1, ":cur_agent"),
					(get_distance_between_positions, ":distance_of_enemy", pos0, pos1),
					(try_begin),
						(gt, ":inf_closest_dist", ":distance_of_enemy"),
						(assign, ":inf_closest_dist", ":distance_of_enemy"),
						(copy_position, Nearest_Enemy_Troop_Pos, pos0),
						(assign, ":enemy_nearest_troop_distance", ":distance_of_enemy"),
						(assign, ":enemy_nearest_agent", ":enemy_agent"),
					(try_end),
					(try_begin),
						(neq, ":enemy_class_no", grc_cavalry),
						(gt, ":inf_closest_non_cav_dist", ":distance_of_enemy"),
						(assign, ":inf_closest_non_cav_dist", ":distance_of_enemy"),
						(copy_position, Nearest_Non_Cav_Enemy_Troop_Pos, pos0),
						(assign, ":enemy_nearest_non_cav_troop_distance", ":distance_of_enemy"),
						(assign, ":enemy_nearest_non_cav_agent", ":enemy_agent"),
					(try_end),
					(try_begin),
						(lt, ":distance_of_enemy", 150),
						(assign, ":enemy_in_melee", 1),
					(try_end),
					(try_begin),
						(lt, ":distance_of_enemy", 350),
						(assign, ":enemy_supporting_melee", 1),
					(try_end),
				(else_try),
					(eq, ":cur_class_no", grc_cavalry),
					(agent_get_position, pos1, ":cur_agent"),
					(get_distance_between_positions, ":distance_of_enemy", pos0, pos1),
					(try_begin),
						(gt, ":cav_closest_dist", ":distance_of_enemy"),
						(assign, ":cav_closest_dist", ":distance_of_enemy"),
					(try_end),
				(try_end),
			(try_end),
			(try_begin),
				(eq, ":enemy_in_melee", 1),
				(val_add, ":num_enemies_in_melee", 1),
			(try_end),
			(try_begin),
				(eq, ":enemy_supporting_melee", 1),
				(val_add, ":num_enemies_supporting_melee", 1),
			(try_end),
		(try_end),
		
		(store_add, ":num_enemies", ":num_enemy_infantry", ":num_enemy_cavalry"),
		(val_add, ":num_enemies", ":num_enemy_others"),
		(gt, ":num_enemies", 0),
		#JL get percentage of enemy others (archers, commpanions)
		(assign, ":perc_enemy_others", ":num_enemy_others"), #assign enemy others percentage JL
		(val_mul, ":perc_enemy_others", 100), #multiply by 100 to get percent JL
		(val_div, ":perc_enemy_others", ":num_enemies"), #divide by total enemies to get ratio in percent JL
		
		(init_position, Enemy_Team_Pos),
		(val_div, ":x_enemy", ":num_enemies"),
		(position_set_x, Enemy_Team_Pos, ":x_enemy"),
		(val_div, ":y_enemy", ":num_enemies"),
		(position_set_y, Enemy_Team_Pos, ":y_enemy"),
		(position_set_z_to_ground_level, Enemy_Team_Pos),

		(call_script, "script_battlegroup_get_size", ":team_no", grc_archers),
		(assign, ":num_archers", reg0),
		(try_begin),
			(eq, ":num_archers", 0),
			(assign, ":enemy_from_archers", Far_Away),
			(assign, ":archer_order", mordr_charge),
		(else_try),
			(call_script, "script_battlegroup_get_position", Archers_Pos, ":team_no", grc_archers),
			(call_script, "script_point_y_toward_position", Archers_Pos, Enemy_Team_Pos),
			(call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Archers_Pos),
			(assign, ":enemy_from_archers", reg0),
			(team_get_movement_order, ":archer_order", ":team_no", grc_archers),
		(try_end),

		(call_script, "script_battlegroup_get_size", ":team_no", grc_infantry),
		(assign, ":num_infantry", reg0),
		(try_begin),
			(eq, ":num_infantry", 0),
			(assign, ":enemy_from_infantry", Far_Away),
		(else_try),
			(call_script, "script_battlegroup_get_position", Infantry_Pos, ":team_no", grc_infantry),
			(call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Infantry_Pos),
			(assign, ":enemy_from_infantry", reg0),
		(try_end),

		(call_script, "script_battlegroup_get_size", ":team_no", grc_cavalry),
		(assign, ":num_cavalry", reg0),
		(try_begin),
			(eq, ":num_cavalry", 0),
			(assign, ":enemy_from_cavalry", Far_Away),
		(else_try),
			(call_script, "script_battlegroup_get_position", Cavalry_Pos, ":team_no", grc_cavalry),
			(call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Cavalry_Pos),
			(assign, ":enemy_from_cavalry", reg0),
		(try_end),

		(try_begin),
			(lt, "$battle_phase", BP_Fight),
			(this_or_next|le, ":enemy_from_infantry", AI_charge_distance),
			(this_or_next|le, ":enemy_from_cavalry", AI_charge_distance),
			(le, ":enemy_from_archers", AI_charge_distance),
			(assign, "$battle_phase", BP_Fight),
		(else_try),
			(lt, "$battle_phase", BP_Jockey),
			(this_or_next|le, ":inf_closest_dist", AI_long_range),
			(le, ":cav_closest_dist", AI_long_range),
			(assign, "$battle_phase", BP_Jockey),
		(try_end),
		
		#(team_get_leader, ":team_leader", ":team_no"),
        (call_script, "script_team_get_nontroll_leader", ":team_no"),
        (assign, ":team_leader", reg0),
        (gt, ":team_leader", 0),
		
		#infantry AI
		(assign, ":place_leader_by_infantry", 0),
		
		# JL DISENGAGEMENT OF ARCHERS:
		(try_begin),
			(gt, ":num_archers", 0), #if there are any archers
			(eq, "$arc_charge_activated", 1), #and archers are in charge mode
			(ge, ":enemy_from_archers", AI_charge_distance), #and enemies are not immediately near
			(assign, "$arc_charge_activated", 0), #then deactivate inf charge mode
			#(display_message, "@Archers ordered to resume shooting."), #######################
		(try_end),
		
		#JL ADVANCE Archers closer to infantry if they are too far away:
		(try_begin),
			(gt, ":num_archers", 0), #if there are any archers
			(gt, ":num_infantry", 0), #and if there is infantry
			(get_distance_between_positions, ":archer_dist_to_inf", Infantry_Pos, Archers_Pos),
			(gt, ":archer_dist_to_inf", "$formai_rand3"), #allied inf are not within 20-30m
			(gt, ":enemy_from_archers", AI_charge_distance), #and enemies are not within 20m 
			(ge, ":enemy_from_archers", ":enemy_from_infantry"), #and enemies are closer or equally close to infantry than they are to archers
			(team_give_order, ":team_no", grc_archers, mordr_charge), #charge the archers forward
			#(display_message, "@Archers ordered to charge to keep close with infantry."), #######################
		(try_end),
		
		(try_begin),
			(le, ":num_infantry", 0),
			(assign, ":infantry_order", ":archer_order"),
		(else_try),
			(try_begin), ## JL CHARGE ACTIVATION to force inf Charge Mode when inf AI has been deemed to need charge mode (--for use if inf charge has been ordered earlier in the code or from archers code)
				(eq, "$inf_charge_activated", 1), #if inf AI has been told to Charge
				(eq, "$inf_charge_ongoing", 0), #and switch is false
				(call_script, "script_formation_end", ":team_no", grc_infantry), #end any formations
				(team_give_order, ":team_no", grc_infantry, mordr_charge), #do a Native Charge
				(assign, "$inf_charge_ongoing", 1), #switch set to true so this function is not needed to be called again until charge mode has been disabled and a new charge has been set
				#(display_message, "@Infantry orders are Charge, Formations Inf AI disabled"), ################
			(try_end),	
			
			(try_begin), ## JL RULES OF DISENGAGEMENT: to Remove AI Infantry Charge Mode when infantry is not in melee any more
				(eq, ":num_enemies_in_melee", 0), #and infantry is currently not in melee
				(eq, "$inf_charge_ongoing", 1), # flag to see if we have a regular charge ongoing
				(assign, "$inf_charge_activated", 0), #then deactivate inf charge mode
				(assign, "$inf_charge_ongoing", 0), #and reset switch to open up for future charge orders
				#(display_message, "@Infantry AI is not in melee and decides to resume maneuver"), #######################
			(try_end),

			#JL Control to Continue form AI
			(eq, "$inf_charge_activated", 0), #If infantry charge has not been activated then continue Inf AI, JL
			
			(store_mul, ":percent_level_enemy_infantry", ":sum_level_enemy_infantry", 100),
			(val_div, ":percent_level_enemy_infantry", ":num_enemies"),
			(try_begin),
				(teams_are_enemies, ":team_no", "$fplayer_team_no"),
				(assign, ":combined_level", 0),
				(assign, ":combined_team_size", 0),
				(assign, ":combined_num_infantry", ":num_infantry"),
			(else_try),
				(call_script, "script_battlegroup_get_level", "$fplayer_team_no", grc_infantry),
				(assign, ":combined_level", reg0),
				(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_everyone),
				(assign, ":combined_team_size", reg0),
				(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_infantry),
				(store_add, ":combined_num_infantry", ":num_infantry", reg0),
			(try_end),
			(store_mul, ":percent_level_infantry", ":combined_num_infantry", 100),
			(call_script, "script_battlegroup_get_level", ":team_no", grc_infantry),
			(assign, ":level_infantry", reg0),
			(val_add, ":combined_level", reg0),
			(val_mul, ":percent_level_infantry", ":combined_level"),
			(call_script, "script_battlegroup_get_size", ":team_no", grc_everyone),
			(val_add, ":combined_team_size", reg0),
			(val_div, ":percent_level_infantry", ":combined_team_size"),

			(assign, ":infantry_order", mordr_charge),
			(try_begin),	#enemy far away AND ranged not charging
				(gt, ":enemy_from_archers", AI_charge_distance),
				(gt, ":inf_closest_dist", AI_charge_distance),
				(neq, ":archer_order", mordr_charge),
				(try_begin),	#fighting not started OR not enough infantry
					(this_or_next|le, "$battle_phase", BP_Jockey),
					(lt, ":percent_level_infantry", ":percent_level_enemy_infantry"),
					(assign, ":infantry_order", mordr_hold),
				(try_end),
			(try_end),

			#if low level troops outnumber enemies in melee by 2:1, attempt to whelm
			(try_begin),
				(le, ":level_infantry", 12),
				(gt, ":num_enemies_in_melee", 0),
				(store_mul, reg0, ":num_enemies_supporting_melee", 2),
				(is_between, reg0, 1, ":num_infantry"),
				(get_distance_between_positions, reg0, Infantry_Pos, Nearest_Enemy_Troop_Pos),
				(le, reg0, AI_charge_distance),
				(call_script, "script_formation_end", ":team_no", grc_infantry),
				(team_give_order, ":team_no", grc_infantry, mordr_charge),
				#(display_message, "@Infantry decided to whelm."), #############

			(else_try), #Kham - Make infantry charge when enemy is close
		        (get_distance_between_positions, reg0, Infantry_Pos, Nearest_Enemy_Troop_Pos),
		        (this_or_next|le, ":enemy_from_infantry", 1300), # Start charge if enemy infantry formation is close
		        (this_or_next|le, ":enemy_from_archers", 1300), # Start charge if enemy archer group is close.
		        (le, reg0, 800), # Start charge if any enemies are really close.
		        (call_script, "script_formation_end", ":team_no", grc_infantry),
						(team_get_movement_order, reg0, ":team_no", grc_infantry),
		        (team_give_order, ":team_no", grc_infantry, mordr_hold_fire), # Hold fire while charging to keep infantry together.
						(try_begin),
							(neq, reg0, mordr_charge),
							(team_give_order, ":team_no", grc_infantry, mordr_charge),
						(try_end),  #Kham - changes end
						#(display_message, "@DEBUG: Infantry decides to charge!"),
				
			#else attempt to form formation somewhere
			(else_try),
				(try_begin),
					(eq, ":team_no", 0),
					(try_begin),
						(eq, "$team0_default_formation", formation_default),
						(call_script, "script_get_default_formation", 0),
						(assign, "$team0_default_formation", reg0),
					(try_end),
					(assign, ":infantry_formation", "$team0_default_formation"),
				(else_try),
					(eq, ":team_no", 1),
					(try_begin),
						(eq, "$team1_default_formation", formation_default),
						(call_script, "script_get_default_formation", 1),
						(assign, "$team1_default_formation", reg0),
					(try_end),
					(assign, ":infantry_formation", "$team1_default_formation"),
				(else_try),
					(eq, ":team_no", 2),
					(try_begin),
						(eq, "$team2_default_formation", formation_default),
						(call_script, "script_get_default_formation", 2),
						(assign, "$team2_default_formation", reg0),
					(try_end),
					(assign, ":infantry_formation", "$team2_default_formation"),
				(else_try),
					(eq, ":team_no", 3),
					(try_begin),
						(eq, "$team3_default_formation", formation_default),
						(call_script, "script_get_default_formation", 3),
						(assign, "$team3_default_formation", reg0),
					(try_end),
					(assign, ":infantry_formation", "$team3_default_formation"),
				(try_end),
				
				(agent_get_class, ":enemy_nearest_troop_class", ":enemy_nearest_agent"), 

				(agent_get_team, ":enemy_nearest_troop_team", ":enemy_nearest_agent"),
				#(team_get_leader, ":enemy_leader", ":enemy_nearest_troop_team"),
				(call_script, "script_team_get_nontroll_leader", ":enemy_nearest_troop_team"),
				(assign, ":enemy_leader", reg0),
				(gt, ":enemy_leader", -1),

				(store_mul, ":percent_enemy_cavalry", ":num_enemy_cavalry", 100),
				(val_div, ":percent_enemy_cavalry", ":num_enemies"),
				(try_begin),
					(neq, ":infantry_formation", formation_none),
					(try_begin),
						(gt, ":percent_enemy_cavalry", 66),
						(assign, ":infantry_formation", formation_square),
						#(display_message, "@Infantry decided to form square"),	#############
					(else_try),
						(neq, ":enemy_nearest_troop_class", grc_cavalry),
						(neq, ":enemy_nearest_troop_class", grc_archers),
						(neq, ":enemy_nearest_agent", ":enemy_leader"),
						(call_script, "script_battlegroup_get_size", ":enemy_nearest_troop_team", ":enemy_nearest_troop_class"),
						(gt, reg0, ":num_infantry"),	#got fewer troops?
						(call_script, "script_battlegroup_get_level", ":team_no", grc_infantry),
						(assign, ":average_level", reg0),
						(call_script, "script_battlegroup_get_level", ":enemy_nearest_troop_team", ":enemy_nearest_troop_class"),
						(gt, ":average_level", reg0),	#got better troops?
						(assign, ":infantry_formation", formation_wedge),
						#(display_message, "@Infantry decided to form wedge"),	#############
					(try_end),
				(try_end),
				
				#hold near archers?
				(try_begin),
					(eq, ":infantry_order", mordr_hold),
					(gt, ":num_archers", 0),
					(copy_position, pos1, Archers_Pos),
					(position_move_x, pos1, "$formai_rand8", 0), #changed -100 to rand8 (-100 to 100) JL
					(try_begin),
						(this_or_next|eq, ":enemy_nearest_troop_class", grc_cavalry),
						(gt, ":percent_level_infantry", ":percent_level_enemy_infantry"),
						(position_move_y, pos1, "$formai_rand2", 0),	#move ahead of archers in anticipation of charges -- changed 1000 to rand2 JL
					(else_try),
						(position_move_y, pos1, "$formai_rand5", 0), #changed -1000 to rand5 JL
					(try_end),
					(assign, ":spacing", 1),
					#(display_message, "@Infantry decided to hold near archers"),	#############

				#advance to nearest (preferably unmounted) enemy
				(else_try),
					#(display_message, "@Infantry decides to advance"), #############
					(try_begin),
						(eq, ":num_enemies_in_melee", 0),	#not engaged?
						(gt, ":enemy_from_archers", "$formai_rand4"), #changed AI_charge_distance to rand4 (10-30m) JL
						(lt, ":percent_enemy_cavalry", 100),
						(assign, ":distance_to_enemy_troop", ":enemy_nearest_non_cav_troop_distance"),
						(copy_position, pos60, Nearest_Non_Cav_Enemy_Troop_Pos),
						(agent_get_team, ":enemy_non_cav_team", ":enemy_nearest_non_cav_agent"),
						#(team_get_leader, reg0, ":enemy_non_cav_team"),
						(call_script, "script_team_get_nontroll_leader", ":enemy_non_cav_team"),
						(try_begin),
							(eq, reg0, -1),
							(assign, ":distance_to_enemy_group", Far_Away),
						(else_try),
							(agent_get_class, reg0, ":enemy_nearest_non_cav_agent"),
							(call_script, "script_battlegroup_get_position", pos0, ":enemy_non_cav_team", reg0),
							(get_distance_between_positions, ":distance_to_enemy_group", Infantry_Pos, pos0),
						(try_end),
					(else_try),
						(assign, ":distance_to_enemy_troop", ":enemy_nearest_troop_distance"),
						(copy_position, pos60, Nearest_Enemy_Troop_Pos),
						(try_begin),
							(eq, ":enemy_nearest_agent", ":enemy_leader"),
							(assign, ":distance_to_enemy_group", Far_Away),
						(else_try),
							(call_script, "script_battlegroup_get_position", pos0, ":enemy_nearest_troop_team", ":enemy_nearest_troop_class"),
							(get_distance_between_positions, ":distance_to_enemy_group", Infantry_Pos, pos0),
						(try_end),
					(try_end),
					
					(try_begin),	#attack troop if its unit is far off
						(gt, ":distance_to_enemy_group", AI_charge_distance),
						(this_or_next|neq, ":enemy_nearest_agent", ":enemy_leader"), #added by JL to ignore leader
						(neq,"$cur_casualties","$prev_casualties"), # added by JL to have the AI not ignore the leader (5 secs) if there have been any recent losses
						(copy_position, pos0, pos60),
						(assign, ":distance_to_move", ":distance_to_enemy_troop"),
						#(display_message, "@Infantry decides to MOVE to attack enemy troop"), #############
						
					(else_try),	#attack unit
						(this_or_next|neq, ":enemy_nearest_agent", ":enemy_leader"), #added by JL to ignore leader
						(neq,"$cur_casualties","$prev_casualties"), # added by JL to have the AI not ignore the leader (5 secs) if there have been any recent losses
						(assign, ":distance_to_move", ":distance_to_enemy_group"),
						#(display_message, "@Infantry decides to attack enemy troop"), #############
						#wedge pushes through to last enemy infantry rank
						(try_begin),
							(eq, ":infantry_formation", formation_wedge),
							(val_add, ":distance_to_move", formation_minimum_spacing),
						# #non-wedge stops before first rank of enemy
						# (else_try),
							# (store_mul, reg0, formation_minimum_spacing, 2),
							# (val_sub, ":distance_to_move", reg0),
							#(display_message, "@Infantry decided to move to attack in wedge formation"), #############
						(try_end),
					(try_end),

					(copy_position, pos1, Infantry_Pos),
					(call_script, "script_point_y_toward_position", pos1, pos0),
					(try_begin),
						(le, ":distance_to_move", 1600),
						(position_move_y, pos1, ":distance_to_move"),
					(else_try),
						(position_move_y, pos1, 1500),
					(try_end),
					(call_script, "script_get_centering_amount", ":infantry_formation", ":num_infantry", 0),
					(position_move_x, pos1, reg0),
					(store_div, reg0, formation_minimum_spacing, 2),
					(position_move_x, pos1, reg0),	#combat tendency of fighting formations to rotate left
					(assign, ":spacing", 0),
				(try_end),
				
				(copy_position, pos61, pos1),	#copy for possible leader positioning
				(position_copy_rotation, pos61, pos1),
				(try_begin),
					(neq, ":infantry_formation", formation_none),
					(ge, ":num_infantry", formation_min_foot_troops),
					(call_script, "script_set_formation_position", ":team_no", grc_infantry, pos1),
					(call_script, "script_form_infantry", ":team_no", ":team_leader", ":spacing", ":infantry_formation"),		
					(team_give_order, ":team_no", grc_infantry, mordr_hold),
					(assign, ":place_leader_by_infantry", 1),
				(else_try),
					(call_script, "script_formation_end", ":team_no", grc_infantry),
					(team_give_order, ":team_no", grc_infantry, ":infantry_order"),
					(team_set_order_position, ":team_no", grc_infantry, pos61),
					(eq, ":infantry_order", mordr_hold),
					(assign, ":place_leader_by_infantry", 1),
				(try_end),
			(try_end),
			
			 #GENERAL RULES OF ENGAGEMENT for Infantry, by JL:
			 #If Engaged in melee and order is charge, then full Charge Infantry (without affecting cavalry) and maybe affecting archers
			(try_begin),
				(gt, ":num_enemies_in_melee", 0),	 #If melee is occurring
				(try_begin), #then if
					(this_or_next|eq, ":infantry_order", mordr_charge), #infantry order is to charge
					(eq, ":archer_order", mordr_charge), #or archer orders are to charge
					(assign, "$inf_charge_activated",1), #then Charge infantry
					#(display_message,"@Infantry ordered to charge because infantry is in melee."), ##############
					(gt, ":num_archers",0),
					(eq, "$arc_charge_activated", 0),
					(call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"), #call to see the odds JL
					(le, reg0, 66), #AI is not overwhelmingly strong, so they need to throw in extra support in close combat
					(le, ":enemy_from_archers", "$formai_rand3"), #and enemy is 20-30 meters from archers
					(team_give_order, ":team_no", grc_archers, mordr_charge), #do a Native Charge
					(assign, "$arc_charge_activated", 1), #then Charge archers
					#(display_message,"@Archers ordered to charge to support melee!"), ##############
				(try_end),
			(try_end),
			
			#If Infantry is Holding and Nearest Enemy is within Self Defence range, enemy is not leader or troops have fallen then Charge (charge infantry and cavalry).
			(try_begin),
				(eq, ":infantry_order", mordr_hold), #if Orders are Hold
				(le, ":enemy_nearest_troop_distance", AI_Self_Defence_Distance), #and any enemy is within self defence distance
				(this_or_next|neq, ":enemy_nearest_agent", ":enemy_leader"), #nearest target is not the player
				(neq, "$cur_casualties","$prev_casualties2"), #troops have fallen during last second
				(assign, "$inf_charge_activated", 1), #then Charge Infantry
				(assign, "$charge_activated", 1), #and Charge Cavalry
				#(display_message,"@Infantry ordered general charge because enemy is too near and casualties inflicted."), ##############				
			(try_end),

			#JL If enemy constitutes more than 40% then charge towards archers
			(try_begin),
				(eq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and infantry needs to close in with them quickly
				(team_give_order, ":team_no", grc_infantry, mordr_charge), #charge the infantry forward towards cavalry and enemy				
			(try_end),
				
			 ##JL ACTIVATION of Inf Charge Mode when Inf AI has been deemed to need charge mode. Put here to activate charge immediately (not wait until next trigger).
			(try_begin),
				(eq, "$inf_charge_activated", 1), #if inf AI has been told to Charge
				(eq, "$inf_charge_ongoing", 0), #and switch is false
				(call_script, "script_formation_end", ":team_no", grc_infantry), #end any formations
				(team_give_order, ":team_no", grc_infantry, mordr_charge), #do a Native Charge
				(assign, "$inf_charge_ongoing", 1), #switch set to true so this function is not needed to be called again until charge mode has been disabled and a new charge has been set
				#(display_message, "@Infantry orders are Charge, Formations Inf AI disabled"), ################
			(try_end),
			
		(try_end),	#end of Infantry AI
		
		#cavalry AI
		(call_script, "script_battlegroup_get_size", ":team_no", grc_cavalry),
		(assign, ":num_cavalry", reg0),
		(call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"), #added by JL to control grand charge and move around threat charge
		(assign, ":grand_charge", reg0), #added by JL
		(assign, ":around_charge", reg0), #added by JL
		
		#JL: don't place leader with infantry if there are more than 1 cavalry on the map:
		(try_begin),
			(gt, ":num_cavalry", 1),
			(assign, ":place_leader_by_infantry", 0), #JL, Kham 
		(try_end),
		
		#JL Patrol Mode Control
		(store_random_in_range, ":chance", 1, 101),	#chance value that is used to assign cavalry patrols and extra aggressivness while on patrol. JL
		(try_begin),
			(ge, ":chance", 97), #There is 3% chance that patrol mode will activate each second
			(neq, "$formai_patrol_mode", 1), #and if it is not already active
			(assign, "$formai_patrol_mode", 1), #assign patrol mode to 1
		(try_end), #End of Patrol Mode Control
		#(val_sub, ":around_charge", 5), #if needed use to increase the odds needed to execute the move around threat and charge routine. JL
		
		##JL ACTIVATION OF Cavalry CHARGE:
		(try_begin), ## Added by JL to force charge when charge is active and cavalry exists
			(gt, ":num_cavalry", 0),
			(eq, "$charge_activated", 1), #if Cav AI has been told to Charge
			(eq, "$charge_ongoing", 0), #switch check
			(call_script, "script_formation_end", ":team_no", grc_cavalry),
			(team_give_order, ":team_no", grc_cavalry, mordr_charge),
			(assign, "$charge_ongoing", 1), #setting switch so this function is not called again until charge mode is turned off
			#(display_message, "@Cavarly Orders are now in Charge Mode; Formations Cav AI is disabled"),
		(try_end),	
		
		#cavalry AI
		(try_begin),
			(gt, ":num_cavalry", 0),
			
			(call_script, "script_battlegroup_get_size", ":team_no", grc_everyone), # added by JL
			(assign, ":perc_cav", ":num_cavalry"), #JL
			(val_mul, ":perc_cav", 100), #get percent JL
			(val_div, ":perc_cav", reg0), #cavalry/everyone*100 JL : used for when executing certain tactics is allowed
			
			#JL CHECK IF Infantry should move forward in charge movement to support an already charging Cavalry:
			(try_begin),
				(eq, "$charge_ongoing", 1), #if Cav AI is in Charge mode
				(this_or_next|gt, ":enemy_from_archers", "$formai_rand3"), #and if enemy is at least 20-30 meters away from archers
				(lt, ":perc_cav", 60), #or if there are less than 60% cavalry on the field
				(get_distance_between_positions, ":inf_dist_to_cav", Infantry_Pos, Cavalry_Pos), #get the distance between infantry and cavalry
				(this_or_next|le, ":enemy_from_infantry", "$formai_rand3"), #if enemy is less than or equal to 20-30m from infantry
				(le, ":inf_dist_to_cav", 4000), #or allied cav is within 40m
				(le, ":enemy_from_cavalry", ":enemy_from_infantry"), #and enemies are closer or equally close to cavalry than they are to infantry
				(team_give_order, ":team_no", grc_infantry, mordr_charge), #charge the infantry	forward towards cavalry and enemy
			(try_end),	#End JL check		
			
			#get distance to nearest enemy battlegroup(s)
			(call_script, "script_battlegroup_get_level", ":team_no", grc_cavalry),
			(assign, ":average_level", reg0),
			(assign, ":nearest_threat_distance", Far_Away),
			(assign, ":nearest_target_distance", Far_Away),
			(assign, ":num_targets", 0),
			(assign, ":num_threats", 0), # added by JL
			(try_for_range, ":enemy_team_no", 0, 4),
				(call_script, "script_battlegroup_get_size", ":enemy_team_no", grc_everyone),
				(gt, reg0, 0),
				(teams_are_enemies, ":enemy_team_no", ":team_no"),
				(try_begin),
					(eq, ":enemy_team_no", "$fplayer_team_no"),
					(assign, ":num_groups", 9),
				(else_try),
					(assign, ":num_groups", 3),
				(try_end),
				(try_for_range, ":enemy_battle_group", 0, ":num_groups"),
					(call_script, "script_battlegroup_get_size", ":enemy_team_no", ":enemy_battle_group"),
					(assign, ":size_enemy_battle_group", reg0),
					(gt, ":size_enemy_battle_group", 0),
					(call_script, "script_battlegroup_get_position", pos0, ":enemy_team_no", ":enemy_battle_group"),
					(get_distance_between_positions, ":distance_of_enemy", Cavalry_Pos, pos0),
					(try_begin),	#threat or target?
						(call_script, "script_battlegroup_get_weapon_length", ":enemy_team_no", ":enemy_battle_group"),
						(assign, ":decision_index", reg0),
						(call_script, "script_battlegroup_get_level", ":enemy_team_no", ":enemy_battle_group"),
						(val_mul, ":decision_index", reg0),
						(val_mul, ":decision_index", ":size_enemy_battle_group"),
						(val_div, ":decision_index", ":average_level"),
						(val_div, ":decision_index", ":num_cavalry"),
						(try_begin),
							(neq, ":enemy_battle_group", grc_cavalry),
							(val_div, ":decision_index", 2),	#double count cavalry vs. foot soldiers
						(try_end),
						(gt, ":decision_index", 100),
						(try_begin),
							(val_add, ":num_threats", 1), #JL
							(gt, ":nearest_threat_distance", ":distance_of_enemy"),
							(copy_position, Nearest_Threat_Pos, pos0),
							(assign, ":nearest_threat_distance", ":distance_of_enemy"),
						(try_end),
					(else_try),
						(val_add, ":num_targets", 1),
						(gt, ":nearest_target_distance", ":distance_of_enemy"),
						(copy_position, Nearest_Target_Pos, pos0),
						(assign, ":nearest_target_distance", ":distance_of_enemy"),
					(try_end),
				(try_end),
			(try_end),
			
			(try_begin), #added by JL to eliminate {0,0} position bug when no target is detected
				(eq, ":num_targets", 0),
				(copy_position, Nearest_Target_Pos, Nearest_Threat_Pos),
				(assign, ":nearest_target_distance", ":nearest_threat_distance"),
			(try_end),
			
			(try_begin), #added by JL to eliminate a {0,0} Position bug when no threat is detected
				(eq, ":num_threats", 0),
				(copy_position, Nearest_Threat_Pos, Nearest_Target_Pos),
				(assign, ":nearest_threat_distance", ":nearest_target_distance"),
			(try_end),			
			
			(get_distance_between_positions, reg0, Nearest_Target_Pos, Nearest_Threat_Pos),
			(store_div, reg1, AI_charge_distance, 2),
			(try_begin),	#ignore target too close to threat
				(le, reg0, reg1),
				(assign, ":nearest_target_guarded", 1),
			(else_try),
				(assign, ":nearest_target_guarded", 0),
			(try_end),

			(assign, ":cavalry_order", mordr_charge),
			(try_begin),
				(teams_are_enemies, ":team_no", 0),
				(lt, "$team1_reinforcement_stage", 2),
				(neq, "$team1_reinforcement_stage", "$attacker_reinforcement_stage"),
				(assign, ":cavalry_order", mordr_hold),
			(else_try),
				(teams_are_enemies, ":team_no", 1),
				(lt, "$team0_reinforcement_stage", 2),
				(neq, "$team0_reinforcement_stage", "$defender_reinforcement_stage"),
				(assign, ":cavalry_order", mordr_hold),
			(else_try),
				(neq, ":infantry_order", mordr_charge),
				(try_begin),
					(le, "$battle_phase", BP_Jockey),
					(assign, ":cavalry_order", mordr_hold),
				(else_try),
					(eq, ":nearest_target_distance", Far_Away),
					(try_begin),
						(eq, ":num_archers", 0),
						(assign, ":distance_to_archers", 0),
					(else_try),
						(get_distance_between_positions, ":distance_to_archers", Cavalry_Pos, Archers_Pos),
					(try_end),
					(try_begin),
						(this_or_next|gt, ":cav_closest_dist", AI_charge_distance),
						(gt, ":distance_to_archers", AI_charge_distance),
						(assign, ":cavalry_order", mordr_hold),
					(try_end),
				(try_end),
			(try_end),
			
			
			(try_begin), #added by JL since the above code doesn't seem to work
				(eq, "$formai_disengage", 1), #disengage has been assigned
				(assign, ":cavalry_order", mordr_hold),
			(try_end),
			
			#JL DISENGAGEMENT RULES:
			(try_begin), ## when any reinforcements arrive:
				(eq, "$formai_disengage", 1), #disengage has been assigned
				(assign, "$formai_disengage", 0), #turn off disengagement so next reinforcement checks can resume
				(eq, "$charge_ongoing", 1), #charge is currently ongoing
				(assign, "$charge_activated", 0), #deactivates charge mode
				(assign, "$charge_ongoing", 0), #charge no longer ongoing
				#(display_message, "@AI Cavalry decided to resume maneuver because of reinforcements"),
			(try_end),
			
			(try_begin), ## When there are no targets or threats near
				(eq,"$charge_ongoing", 1),
				(gt, ":nearest_target_distance", AI_charge_distance),
				(gt, ":nearest_threat_distance", AI_charge_distance),
				(assign, "$charge_activated", 0), #deactivates charge mode
				(assign, "$charge_ongoing", 0), #resetting switch
				#(display_message, "@AI Cavalry decided to resume maneuver because no enemies are near"),
			(try_end),
			
			#JL CONTINUE form AI IF NOT IN CHARGE MODE:
			(eq,"$charge_activated", 0), #if charge mode is off then continue to do Cav AI, JL
			
			(try_begin),
				(eq, ":team_no", 0),
				(assign, ":cav_destination", Team0_Cavalry_Destination),
				(assign, reg0, "$team0_percent_cavalry_are_archers"),
			(else_try),
				(eq, ":team_no", 1),
				(assign, ":cav_destination", Team1_Cavalry_Destination),
				(assign, reg0, "$team1_percent_cavalry_are_archers"),
			(else_try),
				(eq, ":team_no", 2),
				(assign, ":cav_destination", Team2_Cavalry_Destination),
				(assign, reg0, "$team2_percent_cavalry_are_archers"),
			(else_try),
				(eq, ":team_no", 3),
				(assign, ":cav_destination", Team3_Cavalry_Destination),
				(assign, reg0, "$team3_percent_cavalry_are_archers"),
			(try_end),
			
			#(assign, ":charging_through_target", 0), #charging through flag by JL
			
			#horse archers don't use wedge
			(try_begin),
				(neq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and cav AI should move around threat to engage instead, even if they are horse archers.
				(assign, ":percent_horse_archers", reg0), #Added by JL to be used for horse archer self defense further down
				(gt, reg0, 50),
				(call_script, "script_formation_end", ":team_no", grc_cavalry),
				(try_begin),
					(eq, ":num_archers", 0),
					(assign, ":cavalry_order", mordr_charge), #added by JL
					(team_give_order, ":team_no", grc_cavalry, mordr_charge),
					#(display_message, "@Charging CavArch because no foot archers are present"), ################
				(else_try), #this else block added by JL
					(this_or_next|gt, ":num_enemies_in_melee", 0),	 #If infantry melee is occurring
					(this_or_next|le, ":enemy_from_infantry", AI_Self_Defence_Distance), #or if enemy is less than or equal to 10m from infantry
					(le, ":enemy_from_archers", AI_Self_Defence_Distance),	#or enemy is less than or equal to 10m from archers
					(assign, "$charge_activated", 1), #activate charge order
					#(assign, ":cavalry_order", mordr_charge), #added soft charge (alert mode) JL
					#(team_give_order, ":team_no", grc_cavalry, mordr_charge),
					#(display_message, "@Alerting horse archers because melee is ongoing"), ################					
				(else_try),
					(team_give_order, ":team_no", grc_cavalry, ":cavalry_order"),
					(copy_position, ":cav_destination", Archers_Pos),
					(position_move_y, ":cav_destination", -500, 0),
					(position_move_x, ":cav_destination", "$formai_rand0", 0), #added by JL Horse archers place themselves -10m to 10m beside the Archers. Unless in patrol then they are at -20 to 20m
					(team_set_order_position, ":team_no", grc_cavalry, ":cav_destination"),
					#(display_message, "@Directing Ranged Cavalry near Archers"), ################
				(try_end),
				
			#close in with no unguarded target farther off, free fight
			(else_try),
				(eq, ":cavalry_order", mordr_charge),
				(le, ":cav_closest_dist", AI_charge_distance),
				(try_begin),
					(eq, ":num_targets", 1),
					(eq, ":nearest_target_guarded", 0),
					(gt, ":nearest_target_distance", ":nearest_threat_distance"),
					(assign, reg0, 0),
				(else_try),
					(ge, ":num_targets", 2),
					(eq, ":nearest_target_guarded", 1),
					(assign, reg0, 0),
				(else_try),
					(assign, reg0, 1),
				(try_end),
				(eq, reg0, 1),
				(team_get_movement_order, reg0, ":team_no", grc_cavalry),
				(try_begin),
					(neq, reg0, mordr_charge),
					(this_or_next|eq, ":nearest_target_guarded", 1), #cav should not be distracted by enemy solo targets (unless there are new casualties) JL
					(neq, "$cur_casualties", "$prev_casualties2"), #JL casualties incurred during last second
					(assign, "$charge_activated", 1), #added by JL for charge control
					(call_script, "script_formation_end", ":team_no", grc_cavalry),
					(team_give_order, ":team_no", grc_cavalry, mordr_charge),
					#(display_message, "@Closing in and charging Cav (free fight)"), ################
				(try_end),
				
			#grand charge if target closer than threat AND not guarded AND odds are in favour AND we have a good sized amount of cavalry:
			
			(else_try),
				(neq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and cav AI should move around threat to engage instead.
				(ge, ":grand_charge", "$formai_rand7"), # added by JL --> decision number = battle presence + ([avg_lvl]/3)
				(ge, ":perc_cav", 50), #if >= 50% of total AI troop size is Cavalry JL
				(le, ":nearest_target_distance", ":nearest_threat_distance"), #JL changed lt to le in case there are no targets/threats.
				(eq, ":nearest_target_guarded", 0),
				(call_script, "script_formation_end", ":team_no", grc_cavalry),
				(team_give_order, ":team_no", grc_cavalry, mordr_hold),
				#(display_message, "@Holding Cav before 'Grand charge'"), ################
				#lead archers up to firing point
				(try_begin),
					(gt, ":nearest_target_distance", "$formai_rand6"), #changed AI_firing_distance (65m) to 40-50m to get the AI closer JL
					(eq, ":cavalry_order", mordr_hold),
					(try_begin),
						(eq, ":num_archers", 0),
						(copy_position, ":cav_destination", Cavalry_Pos),	#must be reinforcements, so gather at average position
					(else_try),						
						(copy_position, ":cav_destination", Archers_Pos),
						(position_move_y, ":cav_destination", "$formai_rand3", 0), #changed AI_charge_distance to rand3 JL
						#(display_message, "@Leading archers up to firing point to the 'Grand charge'"), ################
					(try_end),
					
				#then CHARRRRGE!
				(else_try),
					(copy_position, ":cav_destination", Cavalry_Pos),
					(call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
					(position_move_y, ":cav_destination", ":nearest_target_distance", 0),
					#(display_message, "@Grand charging cavalry agains target!"), ################
				(try_end),
				(team_set_order_position, ":team_no", grc_cavalry, ":cav_destination"),
				
				
			#make a wedge somewhere
			(else_try),	
				#JL Change the odds criterion for charge around to low value if enemies are near so that the cavalry starts "surprise" flanking
				(try_begin),
					(neq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and cav AI should move around threat to engage instead.
					(le, ":nearest_target_distance", 30), #if there is a target within 30m distance
					(lt, ":around_charge", "$formai_rand7"), #and odds are bad so the cavalry will not try a flank attack on the target.
					#(neq, "$formai_rand7", 30), #and if charge odds comparator has not been lowered already
					(assign, "$formai_rand7", 40), #assign odds comparator to 40
				(else_try), #otherwise:
					(eq, "$formai_rand7", 40), #if charge odds has been lowered already
					(store_random_in_range, "$formai_rand7", 55, 66), #put the odds comparator back to random higher value
				(try_end), #JL
				
				#JL Set cavalry to aggressively move towards archers if there are 45% or more of them:
				(try_begin),
					(gt, ":perc_enemy_others", 45), #if enemy others constitute more than 45% of total enemy
					(assign, ":cavalry_order", mordr_charge),
					(assign, "$formai_rand7", 35), #lower the odds requirement for around charge to 35
				(else_try),
					(eq, "$formai_rand7", 35), #if the odds have been lowered to 35 before
					(store_random_in_range, "$formai_rand7", 55, 66), #put the odds comparator back to random higher value
				(try_end),
				
				(try_begin),
					(eq, ":cavalry_order", mordr_charge),
					(copy_position, ":cav_destination", Cavalry_Pos),
					(this_or_next|ge, ":perc_cav", 80), #if Cav size >= 80% of total AI troop size JL
					(ge, ":around_charge", "$formai_rand7"), #or if odds are good (if odds are not good (lower than 55-65) and there are less than 80 cav --> try other tactics) added by JL					
					(call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
					(position_move_y, ":cav_destination", ":nearest_target_distance", 0), 
					(position_move_y, ":cav_destination", AI_charge_distance, 0),	#charge on through to the other side
					#(assign, ":charging_through_target", 1), #charging through flag by JL
					#(display_message, "@'Charging' Cav through target to other side"), ################
				(else_try),
					(neq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and cav AI should move around threat to engage instead.
					(gt, ":num_archers", 0),
					(copy_position, ":cav_destination", Archers_Pos),	#hold near archers
					(position_move_x, ":cav_destination", "$formai_rand0", 0), #changed 500 to $formai_rand0 (-10m to 10m right/left) JL
					(position_move_y, ":cav_destination", "$formai_rand1", 0), #added (0m to 5m infront) JL
					(try_begin), #move cavalry as a patrol 3% chance every second JL
						(ge, ":chance", 97), #JL
						(store_random_in_range, "$formai_rand0", -2000, 2000), #x-factor update to -20/20 JL
						(position_move_x, ":cav_destination", "$formai_rand0", 0), #patrol positioning JL
						(position_move_y, ":cav_destination", "$formai_rand1", 0), #added another temporary (0m to 5m infront) JL
					(try_end),
					#(display_message, "@Holding Cav near archers"), ################
				(else_try), #if no archers are present hold near infantry JL
					(neq, "$formai_rand7", 35), #JL if the odds have been lowered to 35 then there are lots of archers and cav AI should move around threat to engage instead.
					(gt, ":num_infantry", 0),
					(copy_position, ":cav_destination", Infantry_Pos),	#hold near infantry JL
					(position_move_x, ":cav_destination", "$formai_rand0", 0), #changed 500 to $formai_rand0 (-10m to 10m right/left) JL
					(position_move_y, ":cav_destination", "$formai_rand1", 0), #added (0m to 5m infront) JL
					(try_begin), #move cavalry as a patrol 3% every scond JL
						(ge, ":chance", 97), #JL
						(store_random_in_range, "$formai_rand0", -2000, 2000), #x-factor update JL
						(position_move_x, ":cav_destination", "$formai_rand0", 0), #patrol positioning JL
						(position_move_y, ":cav_destination", "$formai_rand1", 0), #added another (0m to 5m infront) JL
					(try_end),					
					#(display_message, "@Holding Cav near infantry"), ################
				(else_try), #JL
					(eq, ":cavalry_order", mordr_charge), #cavalry are in charge order JL
					(lt, ":around_charge", "$formai_rand7"), #and odds are bad (but there is only cavalry on the field) JL
					(call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
					(position_move_y, ":cav_destination", ":nearest_target_distance", 0), 
					(position_move_y, ":cav_destination", AI_charge_distance, 0),	#charge on through to the other side
					#(assign, ":charging_through_target", 1), #charging through flag by JL
					#(display_message, "@'Charging' Cav through target to other side despite low odds"), ################
				(else_try), #cavalry order must be mordr_hold, so:
					(copy_position, ":cav_destination", Cavalry_Pos), #must be reinforcements, so gather at average position
					#(display_message, "@Cav moving to average position"), ################	
				(try_end),			

				#move around threat in the way to destination
				(try_begin),
					(gt, ":num_threats", 0), #there must be a threat if we are to move around it -- JL
					(call_script, "script_point_y_toward_position", Cavalry_Pos, Nearest_Threat_Pos),
					(call_script, "script_point_y_toward_position", Nearest_Threat_Pos, ":cav_destination"),
					(position_get_rotation_around_z, reg0, Cavalry_Pos),
					(position_get_rotation_around_z, reg1, Nearest_Threat_Pos),
					(store_sub, ":rotation_diff", reg0, reg1),
					(try_begin),
						(lt, ":rotation_diff", -180),
						(val_add, ":rotation_diff", 360),
					(else_try),
						(gt, ":rotation_diff", 180),
						(val_sub, ":rotation_diff", 360),
					(try_end),
					
					(try_begin),
						(is_between, ":rotation_diff", -135, 136),
						(copy_position, ":cav_destination", Cavalry_Pos),
						(assign, ":distance_to_move", AI_firing_distance),
						#(display_message, "@Rotation is between -135 and 135"), ################
						(try_begin),	#target is left of threat
							(is_between, ":rotation_diff", -135, 0),
							(val_mul, ":distance_to_move", -1),
							#(display_message, "@Move around: target is left of threat"), ################
						(try_end),
						(position_move_x, ":cav_destination", ":distance_to_move", 0),
						(store_sub, ":distance_to_move", ":nearest_threat_distance", AI_firing_distance),
						(position_move_y, ":cav_destination", ":distance_to_move", 0),
						(call_script, "script_point_y_toward_position", ":cav_destination", Cavalry_Pos),
						(position_rotate_z, ":cav_destination", 180),
					(try_end),
				(try_end),
				(get_scene_boundaries, pos0, pos1),
				(position_get_x, reg0, ":cav_destination"),
				(position_get_x, reg1, pos0),
				(val_max, reg0, reg1),
				(position_get_x, reg1, pos1),
				(val_min, reg0, reg1),
				(position_set_x, ":cav_destination", reg0),
				(position_get_y, reg0, ":cav_destination"),
				(position_get_y, reg1, pos0),
				(val_max, reg0, reg1),
				(position_get_y, reg1, pos1),
				(val_min, reg0, reg1),
				(position_set_y, ":cav_destination", reg0),
	
				(position_set_z_to_ground_level, ":cav_destination"),
				(call_script, "script_set_formation_position", ":team_no", grc_cavalry, ":cav_destination"),
				(copy_position, pos1, ":cav_destination"),
				(call_script, "script_form_cavalry", ":team_no", ":team_leader", 0),
				(try_begin),
					(ge, reg0, formation_min_cavalry_troops),
					(team_give_order, ":team_no", grc_cavalry, mordr_hold),
					#(display_message, "@Gathering Cavalry to go around threat"), ################
				(else_try),
					(call_script, "script_formation_end", ":team_no", grc_cavalry),
					(team_give_order, ":team_no", grc_cavalry, ":cavalry_order"),
					(team_set_order_position, ":team_no", grc_cavalry, ":cav_destination"),
					#(display_message, "@Directing Cav Around Threat"), ################
				(try_end),
			(try_end),
			
			 #GENERAL RULES of ENGAGEMENT by JL:			 
			 (store_random_in_range, ":imp_charge", 1, 101), #Impetousness factor (random value between 1 to 100) JL 
			 
			 #If Target is Near And [Charge Ordered] and not charging through target then if ... Start offensive Charge otherwise let Cavalry charge through
			(try_begin),
				(le, ":nearest_target_distance", AI_charge_distance), #if there is a target within charge distance (or threat if there is no target)
				(eq, ":cavalry_order", mordr_charge), #and cav orders are to charge
				#(eq, ":charging_through_target", 0), #and not charging through target -- take this away if cavalry is suddenly stopping
				(try_begin),  # if AI has 50% or more cavalry
					(this_or_next|gt, ":nearest_threat_distance", AI_charge_distance), #if there is no threat within charge distance
					(ge, ":perc_cav", 50), #or if Cavalry >= 50% of total AI troop size JL
					(assign, "$charge_activated", 1), #then charge
					#(display_message,"@Cavalry charge ordered because target is within charge distance."), ##############
				(else_try), #if AI has 20% or more cavalry and one of its other troop types is close to the enemy
					(ge, ":perc_cav", 20), #if Cavalry >= 20% of total AI troop size JL
					(try_begin), #then if
						(this_or_next|le, ":enemy_from_infantry", "$formai_rand3"), #if enemy is less than or equal to 20m to 30m from infantry
						(this_or_next|le, ":enemy_from_archers", "$formai_rand3"),	#or enemy is less than or equal to 20m to 30m from archers
						(ge, ":imp_charge", 97), #there is 4% chance every second that the cavalry will charge anyway because of impetousness
						(assign, "$charge_activated", 1), #then charge
						#(display_message,"@Cavalry charge ordered because target is within charge distance."), ##############
					(try_end),
				(else_try), #if less than 20% cavalry only counter charge if other troops are ordered to charge or melee is ongoing
					(this_or_next|gt, ":num_enemies_in_melee", 0),	 #If inf melee is occurring
					(this_or_next|eq, ":infantry_order", mordr_charge), #or infantry order is to charge
					(this_or_next|eq, ":archer_order", mordr_charge), #or archer orders are to charge
					(this_or_next|le, ":enemy_from_infantry", AI_Self_Defence_Distance), #if enemy is less than or equal to 10m from infantry
					(this_or_next|le, ":enemy_from_archers", AI_Self_Defence_Distance),	#or enemy is less than or equal to 10m from archers					
					(ge, ":imp_charge", 99), #there is 2% chance every second that the cavalry will charge anyway because of impetousness
					(assign, "$charge_activated", 1), #then charge
					#(display_message,"@Cavalry charge ordered because target is within charge distance."), ##############
				(try_end),
			(try_end),
			
			#If a threat or a target is within charge distance And ([casualties have been inflicted recently] Or [nearest target is guarded And Cavalry is holding]), then start a Counter Charge
			(try_begin),
				(this_or_next|le, ":nearest_target_distance", AI_charge_distance), #if there is a target within charge distance
				(le, ":nearest_threat_distance", AI_charge_distance), #or if there is a threat within charge distance
				#(eq, ":charging_through_target", 0), #and not charging through target - if AI is too passive, then remove this line
				(try_begin),
					(neq, "$cur_casualties","$prev_casualties2"), #if there are very recent casualties then charge because someone is harming someone
					#(ge, ":imp_charge", 50), #there is 50% chance that the cavalry will charge because of impetousness
					(assign, "$charge_activated", 1),
					#(display_message,"@Enemies are close to cavalry and casualties have recently been inflicted. Counter-Charging cavalry."), #############
				(else_try), #if no casualties have occurred recently then immobile cavalry still needs to charge
					(neq, ":nearest_target_guarded", 0), #if the nearest target is not an unguarded target
					(eq, ":cavalry_order", mordr_hold), #and if Cav order is hold
					(assign, "$charge_activated", 1),
					#(display_message,"@Enemies are close to cavalry and cavalry is standing still. Ordering cavalry to do a counter charge."), #############
				(else_try),
					(ge, ":imp_charge", 97), #there is 4% chance every second that the cavalry will charge anyway because of impetousness
					(eq, ":cavalry_order", mordr_hold), #and if Cav order is hold
					(assign, "$charge_activated", 1),					
				(try_end),
			(try_end),
			
			#extra pre-emptive defence for cavalry if cavalry is holding (defensive stance) or odds are low:
			(try_begin),
				(this_or_next|eq, ":cavalry_order", mordr_hold), #if Cav order is hold
				(lt, ":around_charge", 50), #or the odds are low
				#(eq, ":nearest_target_guarded", 1), #and if the nearest target is guarded
				(try_begin),
					(this_or_next|le, ":enemy_from_infantry", "$formai_rand3"), #if enemy is less than or equal to 20-30m from infantry
					(this_or_next|le, ":enemy_from_cavalry", "$formai_rand3"), #or enemy is less than or equal to 20-30m from cavalry	
					(le, ":enemy_from_archers", "$formai_rand3"),	#or enemy is less than or equal to 20-30m from archers	
					(assign, "$charge_activated", 1),
					#(display_message,"@Enemies are close to AI and cavalry is standing still. Ordering cavalry to do a counter charge."), #############
				#JL Patrol Mode if cavalry is on hold:
				(else_try), #if chance >= 97 then cavalry is in patrol mode. 
					(eq, "$formai_patrol_mode", 1), #cavalry is in patrol mode with heightened alert against enemy cavalry
					(try_begin),
						(le, ":cav_closest_dist", 4000), #any enemy cavalry is less than or equal to 40m from
						(le, ":cav_closest_dist", ":enemy_from_cavalry"), #and nearest [enemy cavalry] is less than or at equal distance as the nearest enemy group is from the VI cavalry
						(this_or_next|gt, ":enemy_from_infantry", "$formai_rand3"), #and enemy is at least 20-30m away from VI infantry
						(gt, ":enemy_from_archers", "$formai_rand3"),	#or enemy is less than or equal to 20-30m from archers						
						(try_begin), #start moving to either nearest threat or nearest target:
							(eq, ":nearest_threat_distance", ":cav_closest_dist"), #if nearest threat distance is equal to nearest enemy cavalry
							(copy_position, ":cav_destination", Cavalry_Pos),
							(call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Threat_Pos),
							(position_move_y, ":cav_destination", ":nearest_threat_distance", 0),
							(position_move_y, ":cav_destination", AI_charge_distance, 0),	#"charge" on through to the other side of the threat/target cavalry	
						(else_try),
							(call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
							(position_move_y, ":cav_destination", ":nearest_target_distance", 0),
							(position_move_y, ":cav_destination", AI_charge_distance, 0),	#"charge" on through to the other side of the threat/target cavalry								
						(try_end),
						(try_begin), #charge if in patrol mode and enemy is near
							(this_or_next|le, ":cav_closest_dist", AI_charge_distance), #if enemy cav is within charge distance, then charge
							(this_or_next|le, ":nearest_target_distance", AI_charge_distance), #or if enemy target is within charge distance, then charge
							(le, ":nearest_threat_distance", AI_charge_distance), #or if enemy threat is within charge distance, then charge
							(assign, "$charge_activated", 1), #do a full charge	
						(try_end),
					(else_try),
						(assign, "$formai_patrol_mode", 0), #puts patrol mode back to 0 if the conditions are not met
						(this_or_next|le, ":cav_closest_dist", AI_charge_distance), #if enemy cav is within charge distance, then charge
						(this_or_next|le, ":nearest_target_distance", AI_charge_distance), #or if enemy target is within charge distance, then charge
						(le, ":nearest_threat_distance", AI_charge_distance), #or if enemy threat is within charge distance, then charge
						(assign, "$charge_activated", 1), #do a full charge							
					(try_end),
				(try_end),	#JL					
			(try_end),
			
			#JL Extra self defense/offense for Archer Cavalry: If enemy is near Then Charge
			(try_begin),
				#(eq, ":cavalry_order", mordr_hold), #if Cav order is hold
				(gt, ":percent_horse_archers",50),
				#(display_message,"@Checking Held Cavalry for Self-Defense."), ##############
				(try_begin),
					(this_or_next|le, ":nearest_target_distance", "$formai_rand3"), #Nearest threat is 20-30m away
					(this_or_next|le, ":nearest_threat_distance", "$formai_rand3"), #or nearest target is 20-30m away
					(this_or_next|le, ":enemy_from_cavalry", "$formai_rand3"), #or enemy is less than or equal to 20-30m from cavalry
					(this_or_next|le, ":enemy_from_infantry", "$formai_rand3"), #or enemy is less than or equal to 20-30m away from infantry
					(le, ":enemy_from_archers", "$formai_rand3"),	#or enemy is less than or equal to 20-30m away from archers						
					(assign, "$charge_activated", 1),
					#(display_message,"@Horse Archers ordered to Charge because enemy is within self defense distance."), ##############
				(try_end),
			(try_end),			
			
			
			# JL Charge mode ACTIVATOR to make charge take effect immediately:
			(try_begin), ## Charge mode controller to make charge take effect immediately:
				(gt, ":num_cavalry", 0),
				(eq, "$charge_activated", 1),
				(eq, "$charge_ongoing", 0), #switch check
				(call_script, "script_formation_end", ":team_no", grc_cavalry),
				(team_give_order, ":team_no", grc_cavalry, mordr_charge),
				(assign, "$charge_ongoing", 1), #setting switch so this function is not called again until charge mode is turned off
				#(display_message, "@Cavalry Charge Mode Active Formations Cav AI is disabled"),
			(try_end), #JL		
		(try_end), #end of Cav AI

		#put leader in duel or place leader -- JL added code for put leader in duel
		(try_begin),
			# #basic conditions:
			# (ge, ":team_leader", 0), #The current team must have a leader
			# (agent_is_alive, ":team_leader"), #and the team leader must be alive
			# (store_agent_hit_points, ":leader_hp", ":team_leader"), #gets leaders hit point percent
			# (ge, ":leader_hp", 25), #and AI leader has more than 25% hit points (- he'll not want to duel any more when he's too wounded)
			# (get_player_agent_no, "$fplayer_agent_no"), #get the player agent ID
			# (agent_is_alive, "$fplayer_agent_no"), #and the player has to be alive
			# #(gt, ":nearest_threat_distance", 3000), #and if there is no cavalry threat within 30m
			# #(eq, ":enemy_nearest_gen_agent", "$fplayer_agent_no"), #and the nearest enemy unit (in relation to either AI inf or cav) must be the player character
			# #(eq, ":nearest_target_guarded", 0), #and the nearest cavalry target is unguarded
			# #if basic conditions are met then 
			# (agent_get_position, pos17, "$fplayer_agent_no"), #get the position of the player
			# (agent_get_position, pos18, ":team_leader"),	#get position of AI leader
			# (get_distance_between_positions, ":duel_distance", pos18, pos17), #get the (duel) distance between AI leader and player
			# (le, ":duel_distance", 3000), #if duel distance is 30m or less
			# #(display_message, "@Team leader moves towards the player"),
			# (agent_set_scripted_destination, ":team_leader", pos17, 1),
			# (try_begin),
				# (le, ":duel_distance", 3000), #if duel distance is 30m or less
				# #(agent_ai_set_always_attack_in_melee, ":team_leader", 1), #set the leader to offensive mode?
				# (team_give_order, ":team_no", grc_heroes, mordr_charge), #charge any heroes (presumably the leader). This overrides the movement to player position.
				# #(display_message, "@Team leader charges the player"),
			# (try_end),
		# (else_try),
			#---------------Normal form AI code for placing leader -- JL: let leader be in scripted mode before the fight starts only. And the leader primarily follows his cavalry if leader is on horse and has cavalry
			(ge, ":team_leader", 0),
			(agent_is_alive, ":team_leader"),
			(try_begin),
				(lt, "$battle_phase", BP_Fight), #JL
				(gt, ":num_cavalry", 1), #JL: at least 2 cavalry (including leader)
				(agent_get_horse, ":agent_horse_id", ":team_leader"), #JL
				(ge, ":agent_horse_id", 0), #JL
				(copy_position, pos18, Cavalry_Pos), #JL
				#(position_move_x, pos18, "$formai_rand8", 0), #JL: put leader -1m to +1 in x-direction relative to cavalry position
				(agent_set_scripted_destination, ":team_leader", pos18, 1), #JL
				#(display_message, "@Team leader positions with cavalry"),
			(else_try), #added by JL
				(lt, "$battle_phase", BP_Fight), #JL
				(le, ":num_infantry", 0),
				(try_begin),
					(eq, ":archer_order", mordr_charge),
					(agent_clear_scripted_mode, ":team_leader"),
				(else_try),
					(gt, ":num_archers", 0), #JL to ensure there are archers present
					(copy_position, pos18, Archers_Pos), #changed pos1 to pos18  JL
					(position_move_y, pos18, 1000, 0), #changed pos1 to pos18  JL
					(agent_set_scripted_destination, ":team_leader", pos18, 1), #changed pos1 to pos18  JL
				(else_try), #JL added to handle any unhandled cases regarding no infantry present
					(agent_clear_scripted_mode, ":team_leader"), #JL added
				(try_end),
			(else_try),
				(lt, "$battle_phase", BP_Fight), #JL
				(gt, ":num_infantry", 0),
				(neq, ":place_leader_by_infantry", 0),
				(position_move_x, pos61, 100, 0),
				(agent_set_scripted_destination, ":team_leader", pos61, 1),
			(else_try),
				(agent_clear_scripted_mode, ":team_leader"),
				#(display_message, "@Team leader cleared of scripted mode"),
			(try_end),
			#--------------End Original form AI code
		(try_end),
	(try_end)
	]),


]) + [
	  
  # script_field_tactics by motomataru
  # Input: flag 1 to include ranged
  # Output: none
  ("field_tactics", [
	(store_script_param, ":include_ranged", 1),
	(store_add, ":team0_size_cavalry_x2", "$team0_size", "$team0_num_cavalry"),	#double count cavalry to capture effect on battlefield
	(store_add, ":team1_size_cavalry_x2", "$team1_size", "$team1_num_cavalry"),
	(store_add, ":team2_size_cavalry_x2", "$team2_size", "$team2_num_cavalry"),
	(store_add, ":team3_size_cavalry_x2", "$team3_size", "$team3_num_cavalry"),
	(assign, ":num_teams", 2),
	(assign, ":largest_team_size", ":team0_size_cavalry_x2"),
	(try_begin),
		(lt, ":largest_team_size", ":team1_size_cavalry_x2"),
		(assign, ":largest_team_size", ":team1_size_cavalry_x2"),
	(try_end),
	(try_begin),
		(gt, ":team2_size_cavalry_x2", 0),
		(assign, ":num_teams", 3),
		(assign, ":adj_team2_size", ":team2_size_cavalry_x2"),
		(try_begin),
			(neg|teams_are_enemies, 2, "$fplayer_team_no"),
			(val_add, ":adj_team2_size", ":team0_size_cavalry_x2"),	#ally 2 takes player team 0 into account
		(try_end),
		(lt, ":largest_team_size", ":adj_team2_size"),
		(assign, ":largest_team_size", ":adj_team2_size"),
	(try_end),
	(try_begin),
		(gt, ":team3_size_cavalry_x2", 0),
		(assign, ":num_teams", 4),
		(assign, ":adj_team3_size", ":team3_size_cavalry_x2"),
		(try_begin),
			(neg|teams_are_enemies, 3, "$fplayer_team_no"),
			(val_add, ":adj_team3_size", ":team1_size_cavalry_x2"),	#ally 3 takes player team 1 into account
		(try_end),
		(lt, ":largest_team_size", ":adj_team3_size"),
		(assign, ":largest_team_size", ":adj_team3_size"),
	(try_end),

	#apply tactics to every AI team
	(store_add, ":battle_size", ":team0_size_cavalry_x2", ":team1_size_cavalry_x2"),
	(val_add, ":battle_size", ":team2_size_cavalry_x2"),
	(val_add, ":battle_size", ":team3_size_cavalry_x2"),
	(try_for_range, ":ai_team", 0, ":num_teams"),
		(assign, ":ai_team_size", 0),
		(try_begin),
			(eq, ":ai_team", 0),
			(assign, ":ai_team_size", ":team0_size_cavalry_x2"),
			(assign, ":ai_faction", "$team0_faction"),
		(else_try),
			(eq, ":ai_team", 1),
			(assign, ":ai_team_size", ":team1_size_cavalry_x2"),
			(assign, ":ai_faction", "$team1_faction"),
		(else_try),
			(eq, ":ai_team", 2),
			(assign, ":ai_team_size", ":adj_team2_size"),
			(assign, ":ai_faction", "$team2_faction"),
		(else_try),
			(eq, ":ai_team", 3),
			(assign, ":ai_team_size", ":adj_team3_size"),
			(assign, ":ai_faction", "$team3_faction"),
		(try_end),

		(gt, ":ai_team_size", 0),
		(neq, ":ai_team", "$fplayer_team_no"),
		(try_begin),
			(this_or_next|eq, AI_for_kingdoms_only, 0),
			(this_or_next|eq, ":ai_faction", fac_deserters),	#deserters have military training
			(is_between, ":ai_faction", kingdoms_begin, fac_kingdoms_end),
			(val_mul, ":ai_team_size", 100),
			(store_div, ":team_percentage", ":ai_team_size", ":largest_team_size"),
			(store_div, ":team_battle_presence", ":ai_team_size", ":battle_size"),
			(try_begin),
				(eq, ":include_ranged", 1),
				(call_script, "script_team_field_ranged_tactics", ":ai_team", ":team_percentage", ":team_battle_presence"),
			(try_end),
			(call_script, "script_team_field_melee_tactics", ":ai_team", ":team_percentage", ":team_battle_presence"),
		(try_end),
	(try_end),

	(try_begin),
		(eq, ":include_ranged", 1), 	  
		(assign, "$prev_casualties", "$cur_casualties"),
	(try_end)
	]),

	
# # Utilities used by AI by motomataru

  # script_find_high_ground_around_pos1_corrected by motomataru
  # Input:	arg1: destination position
  #			arg2: search_radius (in meters)
  #			pos1 should hold center_position_no
  # Output:	destination contains highest ground within a <search_radius> meter square around pos1
  # Also uses position registers: pos0
  ("find_high_ground_around_pos1_corrected", [
	(store_script_param, ":destination_pos", 1),
	(store_script_param, ":search_radius", 2),
	(assign, ":fixed_point_multiplier", 1),
	(convert_to_fixed_point, ":fixed_point_multiplier"),
	(set_fixed_point_multiplier, 1),
	
	(position_get_x, ":o_x", pos1),
	(position_get_y, ":o_y", pos1),
	(store_sub, ":min_x", ":o_x", ":search_radius"),
	(store_sub, ":min_y", ":o_y", ":search_radius"),
	(store_add, ":max_x", ":o_x", ":search_radius"),
	(store_add, ":max_y", ":o_y", ":search_radius"),
	
	(get_scene_boundaries, ":destination_pos", pos0),
	(position_get_x, ":scene_min_x", ":destination_pos"),
	(position_get_x, ":scene_max_x", pos0),
	(position_get_y, ":scene_min_y", ":destination_pos"),
	(position_get_y, ":scene_max_y", pos0),
	(val_max, ":min_x", ":scene_min_x"),
	(val_max, ":min_y", ":scene_min_y"),
	(val_min, ":max_x", ":scene_max_x"),
	(val_min, ":max_y", ":scene_max_y"),

	(assign, ":highest_pos_z", -100),
	(copy_position, ":destination_pos", pos1),
	(init_position, pos0),

	(try_for_range, ":i_x", ":min_x", ":max_x"),
		(try_for_range, ":i_y", ":min_y", ":max_y"),
			(position_set_x, pos0, ":i_x"),
			(position_set_y, pos0, ":i_y"),
			(position_set_z_to_ground_level, pos0),
			(position_get_z, ":cur_pos_z", pos0),
			(try_begin),
				(gt, ":cur_pos_z", ":highest_pos_z"),
				(copy_position, ":destination_pos", pos0),
				(assign, ":highest_pos_z", ":cur_pos_z"),
			(try_end),
		(try_end),
	(try_end),
	
	(set_fixed_point_multiplier, ":fixed_point_multiplier"),
  ]),
  
  
  # script_cf_count_casualties by motomataru
  # Input: none
  # Output: evalates T/F, reg0 num casualties
  ("cf_count_casualties", [
    (assign, ":num_casualties", 0),
	(try_for_agents,":cur_agent"),
	    (try_begin),
			(this_or_next|agent_is_wounded, ":cur_agent"),
			#(this_or_next|agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 1),
			(neg|agent_is_alive, ":cur_agent"),
			(val_add, ":num_casualties", 1),
		(try_end),
	(try_end),
	(assign, reg0, ":num_casualties"),
	(gt, ":num_casualties", 0)
	]),
	
	
  # script_battlegroup_get_position by motomataru
  # Input: destination position, team, battle group (troop class)
  # Output:	battle group position
  #			average team position if "troop class" input NOT set to 0-8
  # NB: Assumes that battle groups beyond 2 are PLAYER team
  # Positions 24-45 reserved (!)
  ("battlegroup_get_position", [
	(store_script_param, ":bgposition", 1),
	(store_script_param, ":bgteam", 2),
	(store_script_param, ":bgroup", 3),
	(try_begin),
		(eq, ":bgroup", grc_infantry),	#AKA battle group 0
		(try_begin),
			(eq, ":bgteam", 0),
			(copy_position, ":bgposition", Team0_Infantry_Pos),
		(else_try),
			(eq, ":bgteam", 1),
			(copy_position, ":bgposition", Team1_Infantry_Pos),
		(else_try),
			(eq, ":bgteam", 2),
			(copy_position, ":bgposition", Team2_Infantry_Pos),
		(else_try),
			(eq, ":bgteam", 3),
			(copy_position, ":bgposition", Team3_Infantry_Pos),
		(try_end),
	(else_try),
		(eq, ":bgroup", grc_archers),	#AKA battle group 1
		(try_begin),
			(eq, ":bgteam", 0),
			(copy_position, ":bgposition", Team0_Archers_Pos),
		(else_try),
			(eq, ":bgteam", 1),
			(copy_position, ":bgposition", Team1_Archers_Pos),
		(else_try),
			(eq, ":bgteam", 2),
			(copy_position, ":bgposition", Team2_Archers_Pos),
		(else_try),
			(eq, ":bgteam", 3),
			(copy_position, ":bgposition", Team3_Archers_Pos),
		(try_end),
	(else_try),
		(eq, ":bgroup", grc_cavalry),	#AKA battle group 2
		(try_begin),
			(eq, ":bgteam", 0),
			(copy_position, ":bgposition", Team0_Cavalry_Pos),
		(else_try),
			(eq, ":bgteam", 1),
			(copy_position, ":bgposition", Team1_Cavalry_Pos),
		(else_try),
			(eq, ":bgteam", 2),
			(copy_position, ":bgposition", Team2_Cavalry_Pos),
		(else_try),
			(eq, ":bgteam", 3),
			(copy_position, ":bgposition", Team3_Cavalry_Pos),
		(try_end),
	(else_try),
		(eq, ":bgroup", 3),
		(copy_position, ":bgposition", Player_Battle_Group3_Pos),
	(else_try),
		(eq, ":bgroup", 4),
		(copy_position, ":bgposition", Player_Battle_Group4_Pos),
	(else_try),
		(eq, ":bgroup", 5),
		(copy_position, ":bgposition", Player_Battle_Group5_Pos),
	(else_try),
		(eq, ":bgroup", 6),
		(copy_position, ":bgposition", Player_Battle_Group6_Pos),
	(else_try),
		(eq, ":bgroup", 7),
		(copy_position, ":bgposition", Player_Battle_Group7_Pos),
	(else_try),
		(eq, ":bgroup", 8),
		(copy_position, ":bgposition", Player_Battle_Group8_Pos),
	(else_try),	#undefined battle group from here on
		(eq, ":bgteam", 0),
		(copy_position, ":bgposition", Team0_Average_Pos),
	(else_try),
		(eq, ":bgteam", 1),
		(copy_position, ":bgposition", Team1_Average_Pos),
	(else_try),
		(eq, ":bgteam", 2),
		(copy_position, ":bgposition", Team2_Average_Pos),
	(else_try),
		(eq, ":bgteam", 3),
		(copy_position, ":bgposition", Team3_Average_Pos),
	(try_end),
  ]),	

 
  # script_battlegroup_get_level by motomataru
  # Input: team, battle group (troop class)
  # Output:	reg0 contains average level
  #			average level of whole team if "troop class" input NOT set to 0-8
  # NB: Assumes that battle groups beyond 2 are PLAYER team
  ("battlegroup_get_level", [
	(store_script_param, ":bgteam", 1),
	(store_script_param, ":bgroup", 2),
	(try_begin),
		(eq, ":bgroup", grc_infantry),	#AKA battle group 0
		(try_begin),
			(eq, ":bgteam", 0),
			(assign, reg0, "$team0_level_infantry"),
		(else_try),
			(eq, ":bgteam", 1),
			(assign, reg0, "$team1_level_infantry"),
		(else_try),
			(eq, ":bgteam", 2),
			(assign, reg0, "$team2_level_infantry"),
		(else_try),
			(eq, ":bgteam", 3),
			(assign, reg0, "$team3_level_infantry"),
		(try_end),
	(else_try),
		(eq, ":bgroup", grc_archers),	#AKA battle group 1
		(try_begin),
			(eq, ":bgteam", 0),
			(assign, reg0, "$team0_level_archers"),
		(else_try),
			(eq, ":bgteam", 1),
			(assign, reg0, "$team1_level_archers"),
		(else_try),
			(eq, ":bgteam", 2),
			(assign, reg0, "$team2_level_archers"),
		(else_try),
			(eq, ":bgteam", 3),
			(assign, reg0, "$team3_level_archers"),
		(try_end),
	(else_try),
		(eq, ":bgroup", grc_cavalry),	#AKA battle group 2
		(try_begin),
			(eq, ":bgteam", 0),
			(assign, reg0, "$team0_level_cavalry"),
		(else_try),
			(eq, ":bgteam", 1),
			(assign, reg0, "$team1_level_cavalry"),
		(else_try),
			(eq, ":bgteam", 2),
			(assign, reg0, "$team2_level_cavalry"),
		(else_try),
			(eq, ":bgteam", 3),
			(assign, reg0, "$team3_level_cavalry"),
		(try_end),
	(else_try),
		(eq, ":bgroup", 3),
		(assign, reg0, "$teamp_level_group3"),
	(else_try),
		(eq, ":bgroup", 4),
		(assign, reg0, "$teamp_level_group4"),
	(else_try),
		(eq, ":bgroup", 5),
		(assign, reg0, "$teamp_level_group5"),
	(else_try),
		(eq, ":bgroup", 6),
		(assign, reg0, "$teamp_level_group6"),
	(else_try),
		(eq, ":bgroup", 7),
		(assign, reg0, "$teamp_level_group7"),
	(else_try),
		(eq, ":bgroup", 8),
		(assign, reg0, "$teamp_level_group8"),
	(else_try),	#undefined battle group from here on
		(eq, ":bgteam", 0),
		(assign, reg0, "$team0_level"),
	(else_try),
		(eq, ":bgteam", 1),
		(assign, reg0, "$team1_level"),
	(else_try),
		(eq, ":bgteam", 2),
		(assign, reg0, "$team2_level"),
	(else_try),
		(eq, ":bgteam", 3),
		(assign, reg0, "$team3_level"),
	(try_end),
  ]),	

 
  # script_battlegroup_get_weapon_length by motomataru
  # Input: team, battle group (troop class)
  # Output:	reg0 contains a proxy calculation for average weapon length
  # NB: Assumes that battle groups beyond 2 are PLAYER team
  ("battlegroup_get_weapon_length", [
	(store_script_param, ":bgteam", 1),
	(store_script_param, ":bgroup", 2),
	(try_begin),
		(eq, ":bgroup", grc_infantry),	#AKA battle group 0
		(try_begin),
			(eq, ":bgteam", 0),
			(assign, reg0, "$team0_weapon_length_infantry"),
		(else_try),
			(eq, ":bgteam", 1),
			(assign, reg0, "$team1_weapon_length_infantry"),
		(else_try),
			(eq, ":bgteam", 2),
			(assign, reg0, "$team2_weapon_length_infantry"),
		(else_try),
			(eq, ":bgteam", 3),
			(assign, reg0, "$team3_weapon_length_infantry"),
		(try_end),
	(else_try),
		(eq, ":bgroup", grc_archers),	#AKA battle group 1
		(try_begin),
			(eq, ":bgteam", 0),
			(assign, reg0, "$team0_weapon_length_archers"),
		(else_try),
			(eq, ":bgteam", 1),
			(assign, reg0, "$team1_weapon_length_archers"),
		(else_try),
			(eq, ":bgteam", 2),
			(assign, reg0, "$team2_weapon_length_archers"),
		(else_try),
			(eq, ":bgteam", 3),
			(assign, reg0, "$team3_weapon_length_archers"),
		(try_end),
	(else_try),
		(eq, ":bgroup", grc_cavalry),	#AKA battle group 2
		(try_begin),
			(eq, ":bgteam", 0),
			(assign, reg0, "$team0_weapon_length_cavalry"),
		(else_try),
			(eq, ":bgteam", 1),
			(assign, reg0, "$team1_weapon_length_cavalry"),
		(else_try),
			(eq, ":bgteam", 2),
			(assign, reg0, "$team2_weapon_length_cavalry"),
		(else_try),
			(eq, ":bgteam", 3),
			(assign, reg0, "$team3_weapon_length_cavalry"),
		(try_end),
	(else_try),
		(eq, ":bgroup", 3),
		(assign, reg0, "$teamp_weapon_length_group3"),
	(else_try),
		(eq, ":bgroup", 4),
		(assign, reg0, "$teamp_weapon_length_group4"),
	(else_try),
		(eq, ":bgroup", 5),
		(assign, reg0, "$teamp_weapon_length_group5"),
	(else_try),
		(eq, ":bgroup", 6),
		(assign, reg0, "$teamp_weapon_length_group6"),
	(else_try),
		(eq, ":bgroup", 7),
		(assign, reg0, "$teamp_weapon_length_group7"),
	(else_try),
		(eq, ":bgroup", 8),
		(assign, reg0, "$teamp_weapon_length_group8"),
	(try_end),
  ]),

  
  # script_get_nearest_enemy_battlegroup_location by motomataru
  # Input: destination position, fron team, from position
  # Output:	destination position, reg0 with distance
  # Run script_store_battlegroup_data before calling!
  ("get_nearest_enemy_battlegroup_location", [
	(store_script_param, ":bgposition", 1),
	(store_script_param, ":team_no", 2),
	(store_script_param, ":from_pos", 3),
	(assign, ":distance_to_nearest_enemy_battlegoup", Far_Away),
	(try_for_range, ":enemy_team_no", 0, 4),
		(call_script, "script_battlegroup_get_size", ":enemy_team_no", grc_everyone),
		(gt, reg0, 0),
		(teams_are_enemies, ":enemy_team_no", ":team_no"),
		(try_begin),
			(eq, ":enemy_team_no", "$fplayer_team_no"),
			(assign, ":num_groups", 9),
		(else_try),
			(assign, ":num_groups", 3),
		(try_end),
		(try_for_range, ":enemy_battle_group", 0, ":num_groups"),
			(call_script, "script_battlegroup_get_size", ":enemy_team_no", ":enemy_battle_group"),
			(gt, reg0, 0),
			(call_script, "script_battlegroup_get_position", pos0, ":enemy_team_no", ":enemy_battle_group"),
			(get_distance_between_positions, reg0, pos0, ":from_pos"),
			(try_begin),
				(gt, ":distance_to_nearest_enemy_battlegoup", reg0),
				(assign, ":distance_to_nearest_enemy_battlegoup", reg0),
				(copy_position, ":bgposition", pos0),
			(try_end),
		(try_end),
	(try_end),
	(assign, reg0, ":distance_to_nearest_enemy_battlegoup")
  ]),

# #Formations Scripts - EDITED by Kham to implement WB versions
  # script_cf_formation v2 by motomataru #Kham - Edited
  # Input: team, troop class, spacing, formation type
  # Output: reg0 number of troops in formation, pos61 formation position
  # Formation(s) form near team leader (player)
  ("cf_formation", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fclass", 2),
	(store_script_param, ":formation_extra_spacing", 3),
	(store_script_param, ":fformation", 4),
	#(team_get_leader, ":fleader", ":fteam"),
    (call_script, "script_team_get_nontroll_leader", ":fteam"),
    (assign, ":fleader", reg0),
	(gt, ":fleader", -1),	#any team members left? (MV: except trolls)
	(agent_get_position, pos1, ":fleader"),
	(try_begin),
		(eq, "$autorotate_at_player", 1),
		(call_script, "script_team_get_average_position_of_enemies_augmented", pos60, ":fteam", grc_everyone),
		(neq, reg0, 0),	#more than 0 enemies still alive?
		(call_script, "script_point_y_toward_position", pos1, pos60),
	(try_end),
	(try_begin),
		(eq, ":fclass", grc_cavalry),
		(position_move_x, pos1, 500),		#cavalry set up 5m RIGHT of leader
		(copy_position, pos61, pos1),
		(call_script, "script_form_cavalry", ":fteam", ":fleader", ":formation_extra_spacing"),
	(else_try),
		(eq, ":fclass", grc_infantry),
		(position_move_x, pos1, -100),		#infantry set up 1m LEFT of leader
		(copy_position, pos61, pos1),
		(call_script, "script_form_infantry", ":fteam", ":fleader", ":formation_extra_spacing", ":fformation"),
	(else_try),
		(position_move_y, pos1, 1000),		#archers set up 10m FRONT of leader
		#preadjust in order to use sequential algorithm
		(assign, ":num_troops", 0),
		(try_for_agents, ":agent"),
			(call_script, "script_cf_valid_formation_member", ":fteam", grc_archers, ":fleader", ":agent"),
			(val_add, ":num_troops", 1),
		(try_end),	
		(call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
		(val_mul, reg0, -1),
		(position_move_x, pos1, reg0, 0),
		(copy_position, pos61, pos1),
		(call_script, "script_form_archers", ":fteam", ":fleader", ":formation_extra_spacing", "$archer_formation_type"),
	(try_end),
	(try_begin),
		(eq, ":fclass", grc_cavalry),
		(try_begin),
			(ge, reg0, formation_min_cavalry_troops),
			(assign, ":formed_up", 1),
		(else_try),
			(assign, ":formed_up", 0),
		(try_end),
	(else_try),
		(try_begin),
			(ge, reg0, formation_min_foot_troops),
			(assign, ":formed_up", 1),
		(else_try),
			(assign, ":formed_up", 0),
		(try_end),
	(try_end),
#	(team_set_order_position, ":fteam", ":fclass", pos61),
	(call_script, "script_set_formation_position", ":fteam", ":fclass", pos61),
	(eq, ":formed_up", 1),
  ]),

   
  # script_form_cavalry v2 by motomataru
  # Input: team, agent number of team leader, spacing
  # Output: reg0 troop count
  # Form in wedge, (now not) excluding horse archers
  # Creates formation starting at pos1
  ("form_cavalry", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fleader", 2),
	(store_script_param, ":formation_extra_spacing", 3),
	(store_mul, ":extra_space", ":formation_extra_spacing", 50),
	(store_add, ":x_distance", 150, ":extra_space"),
	(store_add, ":y_distance", 250, ":extra_space"),		#larger y minimum distance to accommodate mounts
	(assign, ":max_level", 0),
	(try_for_agents, ":agent"),
		(call_script, "script_cf_valid_formation_member", ":fteam", grc_cavalry, ":fleader", ":agent"),
		(agent_get_troop_id, ":troop_id", ":agent"),
		(store_character_level, ":troop_level", ":troop_id"),
		(gt, ":troop_level", ":max_level"),
		(assign, ":max_level", ":troop_level"),
	(try_end),
	(assign, ":column", 1),
	(assign, ":rank_dimension", 1),
	(store_mul, ":neg_y_distance", ":y_distance", -1),
	(store_mul, ":neg_x_distance", ":x_distance", -1),
	(store_div, ":wedge_adj", ":x_distance", 2),
	(store_div, ":neg_wedge_adj", ":neg_x_distance", 2),
	(assign, ":troop_count", 0),
	(val_add, ":max_level", 1),
	(assign, ":form_left", 1),
	(try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
		(try_for_agents, ":agent"),
			(agent_get_troop_id, ":troop_id", ":agent"),
			(store_character_level, ":troop_level", ":troop_id"),
			(eq, ":troop_level", ":rank_level"),				
			(call_script, "script_cf_valid_formation_member", ":fteam", grc_cavalry, ":fleader", ":agent"),
			(val_add, ":troop_count", 1),
			(agent_set_scripted_destination, ":agent", pos1, 1),
			(try_begin),
				(eq, ":form_left", 1),
				(position_move_x, pos1, ":neg_x_distance", 0),
			(else_try),
				(position_move_x, pos1, ":x_distance", 0),
			(try_end),
			(val_add, ":column", 1),
			(gt, ":column", ":rank_dimension"),
			(position_move_y, pos1, ":neg_y_distance", 0),
			(try_begin),
				(neq, ":form_left", 1),
				(assign, ":form_left", 1),
				(position_move_x, pos1, ":neg_wedge_adj", 0),
			(else_try),
				(assign, ":form_left", 0),
				(position_move_x, pos1, ":wedge_adj", 0),
			(try_end),			
			(assign, ":column", 1),
			(val_add, ":rank_dimension", 1),
		(try_end),
	(try_end),
	(assign, reg0, ":troop_count")
  ]),
	   
  # script_form_archers v2 by motomataru
  # Input: team, agent number of team leader, spacing
  # Output: reg0 troop count
  # Form in staggered line both directions
  # Creates formation starting at pos1
  ("form_archers", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fleader", 2),
	(store_script_param, ":formation_extra_spacing", 3),
	(store_script_param, ":archers_formation", 4),
	(store_mul, ":extra_space", ":formation_extra_spacing", 50),
	(store_add, ":distance", formation_minimum_spacing, ":extra_space"),		#minimum distance between troops
	(assign, ":troop_count", 0),
	(assign, ":total_move_y", 0),	#staggering variable	
	(try_for_agents, ":agent"),
		(call_script, "script_cf_valid_formation_member", ":fteam", grc_archers, ":fleader", ":agent"),
		(agent_set_scripted_destination, ":agent", pos1, 1),
		(position_move_x, pos1, ":distance", 0),
		(try_begin),
			(eq, ":archers_formation", formation_ranks),
			(val_add, ":total_move_y", 75),
			(try_begin),
				(le, ":total_move_y", 150),
				(position_move_y, pos1, 75, 0),
			(else_try),
				(position_move_y, pos1, -150, 0),
				(assign, ":total_move_y", 0),
			(try_end),
		(try_end),
		(val_add, ":troop_count", 1),
	(try_end),
	(assign, reg0, ":troop_count")
  ]),
	   
  # script_form_infantry v2 by motomataru #Kham - edited
  # Input: (pos1), team, agent number of team leader, spacing, formation
  # Output: reg0 troop count
  # If input "formation" is formation_default, will select a formation based on faction
  # Creates formation starting at pos1
  ("form_infantry", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fleader", 2),
	(store_script_param, ":formation_extra_spacing", 3),
	(store_script_param, ":infantry_formation", 4),
	(store_mul, ":extra_space", ":formation_extra_spacing", 50),
	(store_add, ":distance", formation_minimum_spacing, ":extra_space"),		#minimum distance between troops	
	(store_mul, ":neg_distance", ":distance", -1),
	(assign, ":num_troops", 0),
    (try_for_agents, ":agent"),
		(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
		(val_add, ":num_troops", 1),
	(try_end),
	(assign, ":troop_count", ":num_troops"),	
	(try_begin),
		(eq, ":infantry_formation", formation_default),
		(call_script, "script_get_default_formation", ":fteam"),
		(assign, ":infantry_formation", reg0),
	(try_end),
	(assign, ":form_left", 1),

	(try_begin),
		(eq, ":infantry_formation", formation_square),
		(convert_to_fixed_point, ":num_troops"),
		(store_sqrt, ":square_dimension", ":num_troops"),
		(convert_from_fixed_point, ":square_dimension"),
		(val_add, ":square_dimension", 1),
		(assign, ":column", 1),
		(try_for_agents, ":agent"),
			(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
			(agent_set_scripted_destination, ":agent", pos1, 1),
			(try_begin),
				(eq, ":form_left", 1),
				(position_move_x, pos1, ":neg_distance", 0),
			(else_try),
				(position_move_x, pos1, ":distance", 0),
			(try_end),
			(val_add, ":column", 1),
			(gt, ":column", ":square_dimension"),
			(position_move_y, pos1, ":neg_distance", 0),
			(try_begin),
				(neq, ":form_left", 1),
				(assign, ":form_left", 1),
				(position_move_x, pos1, ":neg_distance", 0),
			(else_try),
				(assign, ":form_left", 0),
				(position_move_x, pos1, ":distance", 0),
			(try_end),			
			(assign, ":column", 1),		
		(try_end),
		
	(else_try),
		(eq, ":infantry_formation", formation_wedge),
		(assign, ":max_level", 0),
		(try_for_agents, ":agent"),
			(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
			(agent_get_troop_id, ":troop_id", ":agent"),
			(store_character_level, ":troop_level", ":troop_id"),
			(gt, ":troop_level", ":max_level"),
			(assign, ":max_level", ":troop_level"),
		(try_end),
		(assign, ":column", 1),
		(assign, ":rank_dimension", 1),
		(store_div, ":wedge_adj", ":distance", 2),
		(store_div, ":neg_wedge_adj", ":neg_distance", 2),
		(val_add, ":max_level", 1),
		(try_begin), #kham - orc troops go in front
			(try_for_range, ":rank_level", 0, ":max_level"),	#put troops with lowest exp in front
				(try_for_agents, ":agent"),
					(agent_get_troop_id, ":troop_id", ":agent"),
					(troop_get_type, ":race", ":troop_id"),
					(is_between, ":race", tf_orc_begin, tf_orc_end),
					(store_character_level, ":troop_level", ":troop_id"),
					(eq, ":troop_level", ":rank_level"),				
					(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
					(agent_set_scripted_destination, ":agent", pos1, 1),
					(try_begin),
						(eq, ":form_left", 1),
						(position_move_x, pos1, ":neg_distance", 0),
					(else_try),
						(position_move_x, pos1, ":distance", 0),
					(try_end),
					(val_add, ":column", 1),
					(gt, ":column", ":rank_dimension"),
					(position_move_y, pos1, ":neg_distance", 0),
					(try_begin),
						(neq, ":form_left", 1),
						(assign, ":form_left", 1),
						(position_move_x, pos1, ":neg_wedge_adj", 0),
					(else_try),
						(assign, ":form_left", 0),
						(position_move_x, pos1, ":wedge_adj", 0),
					(try_end),			
					(assign, ":column", 1),
					(val_add, ":rank_dimension", 1),
				(try_end),
			(try_end),
		(else_try),
			(try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
				(try_for_agents, ":agent"),
					(agent_get_troop_id, ":troop_id", ":agent"),
					(troop_get_type, ":race", ":troop_id"),
					(neg|is_between, ":race", tf_orc_begin, tf_orc_end),
					(store_character_level, ":troop_level", ":troop_id"),
					(eq, ":troop_level", ":rank_level"),				
					(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
					(agent_set_scripted_destination, ":agent", pos1, 1),
					(try_begin),
						(eq, ":form_left", 1),
						(position_move_x, pos1, ":neg_distance", 0),
					(else_try),
						(position_move_x, pos1, ":distance", 0),
					(try_end),
					(val_add, ":column", 1),
					(gt, ":column", ":rank_dimension"),
					(position_move_y, pos1, ":neg_distance", 0),
					(try_begin),
						(neq, ":form_left", 1),
						(assign, ":form_left", 1),
						(position_move_x, pos1, ":neg_wedge_adj", 0),
					(else_try),
						(assign, ":form_left", 0),
						(position_move_x, pos1, ":wedge_adj", 0),
					(try_end),			
					(assign, ":column", 1),
					(val_add, ":rank_dimension", 1),
				(try_end),
			(try_end),
		(try_end),
	(else_try),
		(eq, ":infantry_formation", formation_ranks),
		(store_div, ":rank_dimension", ":num_troops", 3),		#basic three ranks
		(val_add, ":rank_dimension", 1),		
		(assign, ":max_level", 0),
		(try_for_agents, ":agent"),
			(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
			(agent_get_troop_id, ":troop_id", ":agent"),
			(store_character_level, ":troop_level", ":troop_id"),
			(gt, ":troop_level", ":max_level"),
			(assign, ":max_level", ":troop_level"),
		(try_end),

		(assign, ":column", 1),
		(val_add, ":max_level", 1),
		(try_begin), #Kham - Orcs go in front
		(try_for_range, ":rank_level", 0, ":max_level"),	#put troops with lowest exp in front
			(try_for_agents, ":agent"),
				(agent_get_troop_id, ":troop_id", ":agent"),
				(troop_get_type, ":race", ":troop_id"),
				(is_between, ":race", tf_orc_begin, tf_orc_end),
				(store_character_level, ":troop_level", ":troop_id"),
				(eq, ":troop_level", ":rank_level"),				
				(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
				(agent_set_scripted_destination, ":agent", pos1, 1),
				(try_begin),
					(eq, ":form_left", 1),
					(position_move_x, pos1, ":neg_distance", 0),
				(else_try),
					(position_move_x, pos1, ":distance", 0),
				(try_end),
				(val_add, ":column", 1),
				(gt, ":column", ":rank_dimension"),
				(position_move_y, pos1, ":neg_distance", 0),
				(try_begin),
					(neq, ":form_left", 1),
					(assign, ":form_left", 1),
					(position_move_x, pos1, ":neg_distance", 0),
				(else_try),
					(assign, ":form_left", 0),
					(position_move_x, pos1, ":distance", 0),
				(try_end),			
				(assign, ":column", 1),
			(try_end),
		(try_end),
		(else_try),
		(try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
			(try_for_agents, ":agent"),
				(agent_get_troop_id, ":troop_id", ":agent"),
				(troop_get_type, ":race", ":troop_id"),
				(neg|is_between, ":race", tf_orc_begin, tf_orc_end),
				(store_character_level, ":troop_level", ":troop_id"),
				(eq, ":troop_level", ":rank_level"),				
				(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
				(agent_set_scripted_destination, ":agent", pos1, 1),
				(try_begin),
					(eq, ":form_left", 1),
					(position_move_x, pos1, ":neg_distance", 0),
				(else_try),
					(position_move_x, pos1, ":distance", 0),
				(try_end),
				(val_add, ":column", 1),
				(gt, ":column", ":rank_dimension"),
				(position_move_y, pos1, ":neg_distance", 0),
				(try_begin),
					(neq, ":form_left", 1),
					(assign, ":form_left", 1),
					(position_move_x, pos1, ":neg_distance", 0),
				(else_try),
					(assign, ":form_left", 0),
					(position_move_x, pos1, ":distance", 0),
				(try_end),			
				(assign, ":column", 1),
			(try_end),
		(try_end),
		(try_end),
	(else_try),
		(eq, ":infantry_formation", formation_shield),
		(store_div, ":rank_dimension", ":num_troops", 3),		#basic three ranks
		(val_add, ":rank_dimension", 1),
		(assign, ":column", 1),
	#shields
		(try_for_agents, ":agent"),
			(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
			(agent_get_wielded_item, ":agent_weapon", ":agent", 1),
			(gt, ":agent_weapon", -1),
			(item_get_type, ":agent_weapon_type", ":agent_weapon"),
			(eq, ":agent_weapon_type", itp_type_shield),
			(agent_set_scripted_destination, ":agent", pos1, 1),
			(try_begin),
				(eq, ":form_left", 1),
				(position_move_x, pos1, ":neg_distance", 0),
			(else_try),
				(position_move_x, pos1, ":distance", 0),
			(try_end),
			(val_add, ":column", 1),
			(gt, ":column", ":rank_dimension"),
			(position_move_y, pos1, ":neg_distance", 0),
			(try_begin),
				(neq, ":form_left", 1),
				(assign, ":form_left", 1),
				(position_move_x, pos1, ":neg_distance", 0),
			(else_try),
				(assign, ":form_left", 0),
				(position_move_x, pos1, ":distance", 0),
			(try_end),			
			(assign, ":column", 1),
		(try_end),
	#Low Level Orcs - Kham
		(try_for_agents, ":agent"),
			(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
			(agent_get_troop_id, ":troop_id", ":agent"),
			(troop_get_type, ":race", ":troop_id"),
			(is_between, ":race", tf_orc_begin, tf_orc_end),
			(store_character_level, ":troop_level", ":troop_id"),
			(le, ":troop_level", 9),
			(agent_set_scripted_destination, ":agent", pos1, 1),
			(try_begin),
				(eq, ":form_left", 1),
				(position_move_x, pos1, ":neg_distance", 0),
			(else_try),
				(position_move_x, pos1, ":distance", 0),
			(try_end),
			(val_add, ":column", 1),
			(gt, ":column", ":rank_dimension"),
			(position_move_y, pos1, ":neg_distance", 0),
			(try_begin),
				(neq, ":form_left", 1),
				(assign, ":form_left", 1),
				(position_move_x, pos1, ":neg_distance", 0),
			(else_try),
				(assign, ":form_left", 0),
				(position_move_x, pos1, ":distance", 0),
			(try_end),			
			(assign, ":column", 1),
		(try_end),
	#short weapons
		(try_for_agents, ":agent"),
			(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
			(assign, ":agent_weapon_type", 0),
			(agent_get_wielded_item, ":agent_weapon", ":agent", 0),
			(try_begin),
				(gt, ":agent_weapon", -1),
				(item_get_type, ":agent_weapon_type", ":agent_weapon"),
			(try_end),
			(neq, ":agent_weapon_type", itp_type_polearm),
			(assign, ":agent_weapon_type", 0),
			(agent_get_wielded_item, ":agent_weapon", ":agent", 1),
			(try_begin),
				(gt, ":agent_weapon", -1),
				(item_get_type, ":agent_weapon_type", ":agent_weapon"),
			(try_end),
			(neq, ":agent_weapon_type", itp_type_shield),
			(agent_set_scripted_destination, ":agent", pos1, 1),
			(try_begin),
				(eq, ":form_left", 1),
				(position_move_x, pos1, ":neg_distance", 0),
			(else_try),
				(position_move_x, pos1, ":distance", 0),
			(try_end),
			(val_add, ":column", 1),
			(gt, ":column", ":rank_dimension"),
			(position_move_y, pos1, ":neg_distance", 0),
			(try_begin),
				(neq, ":form_left", 1),
				(assign, ":form_left", 1),
				(position_move_x, pos1, ":neg_distance", 0),
			(else_try),
				(assign, ":form_left", 0),
				(position_move_x, pos1, ":distance", 0),
			(try_end),			
			(assign, ":column", 1),
		(try_end),
	#pole weapons
		(try_for_agents, ":agent"),
			(call_script, "script_cf_valid_formation_member", ":fteam", grc_infantry, ":fleader", ":agent"),
			(assign, ":agent_weapon_type", 0),
			(agent_get_wielded_item, ":agent_weapon", ":agent", 1),
			(try_begin),
				(gt, ":agent_weapon", -1),
				(item_get_type, ":agent_weapon_type", ":agent_weapon"),
			(try_end),
			(neq, ":agent_weapon_type", itp_type_shield),
			(agent_get_wielded_item, ":agent_weapon", ":agent", 0),
			(gt, ":agent_weapon", -1),
			(item_get_type, ":agent_weapon_type", ":agent_weapon"),
			(eq, ":agent_weapon_type", itp_type_polearm),
			(agent_set_scripted_destination, ":agent", pos1, 1),
			(try_begin),
				(eq, ":form_left", 1),
				(position_move_x, pos1, ":neg_distance", 0),
			(else_try),
				(position_move_x, pos1, ":distance", 0),
			(try_end),
			(val_add, ":column", 1),
			(gt, ":column", ":rank_dimension"),
			(position_move_y, pos1, ":neg_distance", 0),
			(try_begin),
				(neq, ":form_left", 1),
				(assign, ":form_left", 1),
				(position_move_x, pos1, ":neg_distance", 0),
			(else_try),
				(assign, ":form_left", 0),
				(position_move_x, pos1, ":distance", 0),
			(try_end),			
			(assign, ":column", 1),
		(try_end),
	(try_end),
	(assign, reg0, ":troop_count")
  ]),
	   
  # script_get_default_formation by motomataru
  # Input: team id
  # Output: reg0 default formation
  ("get_default_formation", [
	(store_script_param, ":fteam", 1),
	(try_begin),
		(eq, ":fteam", 0),
		(assign, ":ffaction", "$team0_faction"),
	(else_try),
		(eq, ":fteam", 1),
		(assign, ":ffaction", "$team1_faction"),
	(else_try),
		(eq, ":fteam", 2),
		(assign, ":ffaction", "$team2_faction"),
	(else_try),
		(eq, ":fteam", 3),
		(assign, ":ffaction", "$team3_faction"),
	(try_end),
	
	(try_begin),
		(eq, ":ffaction", fac_player_supporters_faction),
		(assign, ":ffaction", fac_player_faction),
	(try_end),
	(try_begin),
		(eq, ":ffaction", fac_player_faction),
		(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		(neq, "$players_kingdom", fac_player_supporters_faction),
		(assign, ":ffaction", "$players_kingdom"),
	(try_end),

	#assign default infantry formation (formation_none, formation_ranks, formation_shield, formation_square)
    #formation_ranks: 3 ranks, best troops in front
    #formation_shield: 3 ranks, sort by weapon (shield, polearm, short weapon)
	(try_begin),
		(eq, ":ffaction", "fac_gondor"),	#Gondor
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_dwarf"),	#Erebor
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_rohan"),	#Rohan
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_mordor"),	#Mordor
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_isengard"),	#Isengard
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_lorien"),	#Lorien
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_imladris"),	#Imladris
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_woodelf"),	#Mirkwood Elves
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_dale"),	#Dale
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_harad"),	#Harad
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_rhun"),	#Rhun
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_khand"),	#Khand
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_umbar"),	#Umbar
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_moria"),	#Moria
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_guldur"),	#Dol Guldur
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_gundabad"),    #Gundabad
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_dunland"),	#Dunland
		(assign, reg0, formation_none),
	(else_try),
		(eq, ":ffaction", "fac_beorn"),	#Beornings
		(assign, reg0, formation_none),
	(else_try),
		(eq, ":ffaction", "fac_player_faction"),	#independent player
		(assign, reg0, formation_ranks),
	(else_try),
		(assign, reg0, formation_none),	#riffraff don't use formations
	(try_end),
  ]),


 # script_formation_current_position by motomataru #Kham - Edited
  # Input: destination position, team, troop class, team leader, formation type
  # Output: in destination position
  ("formation_current_position", [
	(store_script_param, ":fposition", 1),
	(store_script_param, ":fteam", 2),
	(store_script_param, ":fclass", 3),
	(store_script_param, ":fformation", 4),
	(call_script, "script_get_first_formation_member", ":fteam", ":fclass", ":fformation"),
	(assign, ":first_agent_in_formation", reg0),
	(call_script, "script_get_formation_position", pos0, ":fteam", ":fclass"),
	(try_begin),
		(eq, ":first_agent_in_formation", -1),
		(copy_position, ":fposition", pos0),
	(else_try),
		(agent_get_position, ":fposition", ":first_agent_in_formation"),
		(position_copy_rotation, ":fposition", pos0),
	(try_end),
  ]),


  # script_get_centering_amount by motomataru #Kham - Edited
  # Input: formation type, number of infantry, extra spacing
  # Output: reg0 number of centimeters to adjust x-position to center formation
  ("get_centering_amount", [
	(store_script_param, ":troop_formation", 1),
	(store_script_param, ":num_troops", 2),
	(store_script_param, ":extra_spacing", 3),
	(store_mul, ":troop_space", ":extra_spacing", 50),
	(val_add, ":troop_space", formation_minimum_spacing),
	(assign, reg0, 0),
	(try_begin),
		(eq, ":troop_formation", formation_square),
		(convert_to_fixed_point, ":num_troops"),
		(store_sqrt, ":square_dimension", ":num_troops"),
		(convert_from_fixed_point, ":square_dimension"),
		(store_mul, reg0, ":square_dimension", ":troop_space"),
		(val_sub, reg0, ":troop_space"),
	(else_try),
		(this_or_next|eq, ":troop_formation", formation_ranks),
		(eq, ":troop_formation", formation_shield),
		(store_mul, reg0, ":num_troops", ":troop_space"),
		(val_div, reg0, 3),
		(val_sub, reg0, ":troop_space"),
	(else_try),
		(eq, ":troop_formation", formation_default),	#assume these are archers in a line
		(store_mul, reg0, ":num_troops", ":troop_space"),
	(try_end),
	(val_div, reg0, 2),
  ]),

  
 ] + (is_a_wb_script==1 and [

 # script_formation_end #Kham - Edited
  # Input: team, troop class
  # Output: none
  ("formation_end", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fclass", 2),
	(try_for_agents, ":agent"),
		(agent_is_alive, ":agent"),
		(agent_is_human, ":agent"),
		(agent_get_team, ":team", ":agent"),
		(eq, ":team", ":fteam"),
		(call_script, "script_classify_agent", ":agent"),
		(this_or_next|eq, reg0, ":fclass"), 
		(eq, ":fclass", grc_everyone), 
		(agent_clear_scripted_mode, ":agent"),
	(try_end)
  ]),

] or [

  # script_formation_end
  # Input: team, troop class
  # Output: none
  ("formation_end", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fclass", 2),
	(try_for_agents, ":agent"),
		(agent_is_alive, ":agent"),
		(agent_is_human, ":agent"),
		(agent_get_team, ":team", ":agent"),
		(eq, ":team", ":fteam"),
		(agent_get_class, reg0, ":agent"),
		(this_or_next|eq, reg0, ":fclass"), 
		(eq, ":fclass", grc_everyone), 
		(agent_clear_scripted_mode, ":agent"),
	(try_end)
  ]),

]) + [

 # script_formation_move_position v2 by motomataru #Kham - Edited
  # Input: team, troop class, formation type, formation current position, (1 to advance or -1 to withdraw or 0 to redirect)
  # Output: pos1
  ("formation_move_position", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fclass", 2),
	(store_script_param, ":fcurrentpos", 3),
	(store_script_param, ":direction", 4),
	(copy_position, pos1, ":fcurrentpos"),
	(call_script, "script_team_get_average_position_of_enemies_augmented", pos60, ":fteam", grc_everyone),
	(try_begin),
		(neq, reg0, 0),	#more than 0 enemies still alive?
		(call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", ":fteam", ":fclass"),
		(call_script, "script_point_y_toward_position", pos60, pos1),	#record angle from center to enemy
		(assign, ":distance_to_enemy", reg0),
		(copy_position, pos1, ":fcurrentpos"),	#restore current formation "position"
		(position_copy_rotation, pos1, pos60),	#copy angle from center of angle (to center approach)
		(position_rotate_z, pos1, 180),
#		(team_get_order_position, pos61, ":fteam", ":fclass"),
		(call_script, "script_get_formation_position", pos61, ":fteam", ":fclass"),
		(get_distance_between_positions, ":move_amount", pos1, pos61),	#distance already moving from previous orders
		(val_add, ":move_amount", 1000),
		(try_begin),
			(gt, ":direction", 0),	#moving forward?
			(gt, ":move_amount", ":distance_to_enemy"),
			(assign, ":move_amount", ":distance_to_enemy"),
		(try_end),
		(val_mul, ":move_amount", ":direction"),
		(position_move_y, pos1, ":move_amount", 0),
		(try_begin),
			(lt, ":distance_to_enemy", 1000),	#less than a move away?
			(position_copy_rotation, pos1, pos61),	#avoid rotating formation
		(try_end),
#		(team_set_order_position, ":fteam", ":fclass", pos1),
		(call_script, "script_set_formation_position", ":fteam", ":fclass", pos1),
	(try_end),
  ]),

  # script_set_formation_position by motomataru
  # Input: team, troop class, position
  # Kluge around buggy *_order_position functions for teams 0-3
  ("set_formation_position", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fclass", 2),
	(store_script_param, ":fposition", 3),
	(try_begin),
		(eq, ":fteam", 0),
		(try_begin),
			(eq, ":fclass", 0),
			(position_get_x, "$formation_00_x", ":fposition"),
			(position_get_y, "$formation_00_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_00_rot", ":fposition"),
		(else_try),
			(eq, ":fclass", 1),
			(position_get_x, "$formation_01_x", ":fposition"),
			(position_get_y, "$formation_01_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_01_rot", ":fposition"),
		(else_try),
			(eq, ":fclass", 2),
			(position_get_x, "$formation_02_x", ":fposition"),
			(position_get_y, "$formation_02_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_02_rot", ":fposition"),
		(try_end),
	(else_try),
		(eq, ":fteam", 1),
		(try_begin),
			(eq, ":fclass", 0),
			(position_get_x, "$formation_10_x", ":fposition"),
			(position_get_y, "$formation_10_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_10_rot", ":fposition"),
		(else_try),
			(eq, ":fclass", 1),
			(position_get_x, "$formation_11_x", ":fposition"),
			(position_get_y, "$formation_11_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_11_rot", ":fposition"),
		(else_try),
			(eq, ":fclass", 2),
			(position_get_x, "$formation_12_x", ":fposition"),
			(position_get_y, "$formation_12_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_12_rot", ":fposition"),
		(try_end),
	(else_try),
		(eq, ":fteam", 2),
		(try_begin),
			(eq, ":fclass", 0),
			(position_get_x, "$formation_20_x", ":fposition"),
			(position_get_y, "$formation_20_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_20_rot", ":fposition"),
		(else_try),
			(eq, ":fclass", 1),
			(position_get_x, "$formation_21_x", ":fposition"),
			(position_get_y, "$formation_21_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_21_rot", ":fposition"),
		(else_try),
			(eq, ":fclass", 2),
			(position_get_x, "$formation_22_x", ":fposition"),
			(position_get_y, "$formation_22_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_22_rot", ":fposition"),
		(try_end),
	(else_try),
		(eq, ":fteam", 3),
		(try_begin),
			(eq, ":fclass", 0),
			(position_get_x, "$formation_30_x", ":fposition"),
			(position_get_y, "$formation_30_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_30_rot", ":fposition"),
		(else_try),
			(eq, ":fclass", 1),
			(position_get_x, "$formation_31_x", ":fposition"),
			(position_get_y, "$formation_31_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_31_rot", ":fposition"),
		(else_try),
			(eq, ":fclass", 2),
			(position_get_x, "$formation_32_x", ":fposition"),
			(position_get_y, "$formation_32_y", ":fposition"),
			(position_get_rotation_around_z, "$formation_32_rot", ":fposition"),
		(try_end),	
	(try_end),
	(team_set_order_position, ":fteam", ":fclass", ":fposition"),
    
  ]),	


  # script_get_formation_position by motomataru
  # Input: position, team, troop class
  # Output: input position (pos0 used)
  # Kluge around buggy *_order_position functions for teams 0-3
  ("get_formation_position", [
	(store_script_param, ":fposition", 1),
	(store_script_param, ":fteam", 2),
	(store_script_param, ":fclass", 3),
	(init_position, ":fposition"),
	(try_begin),
		(eq, ":fteam", 0),
		(try_begin),
			(eq, ":fclass", 0),
			(position_set_x, ":fposition", "$formation_00_x"),
			(position_set_y, ":fposition", "$formation_00_y"),
			(position_rotate_z, ":fposition", "$formation_00_rot"),
		(else_try),
			(eq, ":fclass", 1),
			(position_set_x, ":fposition", "$formation_01_x"),
			(position_set_y, ":fposition", "$formation_01_y"),
			(position_rotate_z, ":fposition", "$formation_01_rot"),
		(else_try),
			(eq, ":fclass", 2),
			(position_set_x, ":fposition", "$formation_02_x"),
			(position_set_y, ":fposition", "$formation_02_y"),
			(position_rotate_z, ":fposition", "$formation_02_rot"),
		(try_end),
	(else_try),
		(eq, ":fteam", 1),
		(try_begin),
			(eq, ":fclass", 0),
			(position_set_x, ":fposition", "$formation_10_x"),
			(position_set_y, ":fposition", "$formation_10_y"),
			(position_rotate_z, ":fposition", "$formation_10_rot"),
		(else_try),
			(eq, ":fclass", 1),
			(position_set_x, ":fposition", "$formation_11_x"),
			(position_set_y, ":fposition", "$formation_11_y"),
			(position_rotate_z, ":fposition", "$formation_11_rot"),
		(else_try),
			(eq, ":fclass", 2),
			(position_set_x, ":fposition", "$formation_12_x"),
			(position_set_y, ":fposition", "$formation_12_y"),
			(position_rotate_z, ":fposition", "$formation_12_rot"),
		(try_end),
	(else_try),
		(eq, ":fteam", 2),
		(try_begin),
			(eq, ":fclass", 0),
			(position_set_x, ":fposition", "$formation_20_x"),
			(position_set_y, ":fposition", "$formation_20_y"),
			(position_rotate_z, ":fposition", "$formation_20_rot"),
		(else_try),
			(eq, ":fclass", 1),
			(position_set_x, ":fposition", "$formation_21_x"),
			(position_set_y, ":fposition", "$formation_21_y"),
			(position_rotate_z, ":fposition", "$formation_21_rot"),
		(else_try),
			(eq, ":fclass", 2),
			(position_set_x, ":fposition", "$formation_22_x"),
			(position_set_y, ":fposition", "$formation_22_y"),
			(position_rotate_z, ":fposition", "$formation_22_rot"),
		(try_end),
	(else_try),
		(eq, ":fteam", 3),
		(try_begin),
			(eq, ":fclass", 0),
			(position_set_x, ":fposition", "$formation_30_x"),
			(position_set_y, ":fposition", "$formation_30_y"),
			(position_rotate_z, ":fposition", "$formation_30_rot"),
		(else_try),
			(eq, ":fclass", 1),
			(position_set_x, ":fposition", "$formation_31_x"),
			(position_set_y, ":fposition", "$formation_31_y"),
			(position_rotate_z, ":fposition", "$formation_31_rot"),
		(else_try),
			(eq, ":fclass", 2),
			(position_set_x, ":fposition", "$formation_32_x"),
			(position_set_y, ":fposition", "$formation_32_y"),
			(position_rotate_z, ":fposition", "$formation_32_rot"),
		(try_end),	
	(else_try),
		(call_script, "script_get_first_formation_member", ":fteam", ":fclass", formation_square),
		(try_begin),	  # "launder" team_get_order_position shutting down position_move_x
			(gt, reg0, -1),
			(team_get_order_position, ":fposition", ":fteam", ":fclass"),
			(agent_get_position, pos0, reg0),
			(agent_set_position, reg0, ":fposition"),
			(agent_get_position, ":fposition", reg0),
			(agent_set_position, reg0, pos0),
		(try_end),
	(try_end),
	(position_set_z_to_ground_level, ":fposition"),
  ]),	

	
  # script_get_first_formation_member by motomataru
  # Input: team, troop class, formation
  # Output: reg0 leader agent number or -1
  # Ought to follow script_form_infantry
  ("get_first_formation_member", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fclass", 2),
	(store_script_param, ":fformation", 3),
	#(team_get_leader, ":fleader", ":fteam"),
    (call_script, "script_team_get_nontroll_leader", ":fteam"),
    (assign, ":fleader", reg0),
	(assign, ":first_agent_in_formation", -1),
	(try_begin),
		(eq, ":fformation", formation_square),
		(try_for_agents, ":agent"),
			(eq, ":first_agent_in_formation", -1),
			(call_script, "script_cf_valid_formation_member", ":fteam", ":fclass", ":fleader", ":agent"),
			(assign, ":first_agent_in_formation", ":agent"),
		(try_end),
	(else_try),
		(eq, ":fformation", formation_shield),
		(try_for_agents, ":agent"),
			(eq, ":first_agent_in_formation", -1),
			(call_script, "script_cf_valid_formation_member", ":fteam", ":fclass", ":fleader", ":agent"),
			(agent_get_wielded_item, ":agent_weapon", ":agent", 1),
			(gt, ":agent_weapon", -1),
			(item_get_type, ":agent_weapon_type", ":agent_weapon"),
			(eq, ":agent_weapon_type", itp_type_shield),
			(assign, ":first_agent_in_formation", ":agent"),
		(try_end),
		(try_for_agents, ":agent"),
			(eq, ":first_agent_in_formation", -1),
			(call_script, "script_cf_valid_formation_member", ":fteam", ":fclass", ":fleader", ":agent"),
			(assign, ":agent_weapon_type", 0),
			(agent_get_wielded_item, ":agent_weapon", ":agent", 0),
			(try_begin),
				(gt, ":agent_weapon", -1),
				(item_get_type, ":agent_weapon_type", ":agent_weapon"),
			(try_end),
			(neq, ":agent_weapon_type", itp_type_polearm),
			(assign, ":first_agent_in_formation", ":agent"),
		(try_end),
		(try_for_agents, ":agent"),
			(eq, ":first_agent_in_formation", -1),
			(call_script, "script_cf_valid_formation_member", ":fteam", ":fclass", ":fleader", ":agent"),
			(assign, ":first_agent_in_formation", ":agent"),	#must have polearm w/o shields...
		(try_end),
	(else_try),	#must be a level sort
		(assign, ":rank_level", 0),
		(try_for_agents, ":agent"),
			(call_script, "script_cf_valid_formation_member", ":fteam", ":fclass", ":fleader", ":agent"),
			(agent_get_troop_id, ":troop_id", ":agent"),
			(store_character_level, ":troop_level", ":troop_id"),
			(gt, ":troop_level", ":rank_level"),
			(assign, ":rank_level", ":troop_level"),
			(assign, ":first_agent_in_formation", ":agent"),
		(try_end),
	(try_end),
	(assign, reg0, ":first_agent_in_formation")
  ]),
  
 ] + (is_a_wb_script==1 and [	

 # script_cf_valid_formation_member by motomataru #Kham - Edited
  # Input: team, troop class, agent number of team leader, test agent
  # Output: failure indicates agent is not member of formation
  ("cf_valid_formation_member", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fclass", 2),
	# (store_script_param, ":fleader", 3),
	(store_script_param, ":agent", 4),
	(call_script, "script_classify_agent", ":agent"),
	(eq, reg0, ":fclass"),
	(agent_get_team, ":team", ":agent"),
	(eq, ":team", ":fteam"),
	(agent_is_alive, ":agent"),
	(agent_is_human, ":agent"),
    #MV: troll check - they don't belong to formations
    (agent_get_troop_id, ":agent_troop", ":agent"),
    (troop_get_type, ":agent_race", ":agent_troop"),
    (neq, ":agent_race", tf_troll),
  ]),

# Kham - Warband Formations Addition
# script_classify_agent by motomataru
  # Input: agent
  # Output: reg0 (-1 if leader)
  # Assigns a "division" to the agent

  ("classify_agent", [
	(store_script_param, ":agent", 1),
	(agent_get_team, ":ateam", ":agent"),
	(team_get_leader, ":aleader", ":ateam"),
	(try_begin),
		(eq, ":agent", ":aleader"),
		(assign, reg0, -1),
	(else_try),
		(eq, ":ateam", "$fplayer_team_no"),
		(agent_get_division, reg0, ":agent"),
	(else_try),
		(agent_get_class, reg0, ":agent"),
	(try_end)
  ]),

] or [

	
  # script_cf_valid_formation_member by motomataru
  # Input: team, troop class, agent number of team leader, test agent
  # Output: failure indicates agent is not member of formation
  ("cf_valid_formation_member", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fclass", 2),
	(store_script_param, ":fleader", 3),
	(store_script_param, ":agent", 4),
	(agent_get_class, reg0, ":agent"),
	(this_or_next|eq, ":fclass", grc_everyone),
	(eq, reg0, ":fclass"),
	(agent_get_team, ":team", ":agent"),
	(eq, ":team", ":fteam"),
	(agent_is_alive, ":agent"),
	(agent_is_human, ":agent"),
	(neq, ":fleader", ":agent"),
    #MV: troll check - they don't belong to formations
    (agent_get_troop_id, ":agent_troop", ":agent"),
    (troop_get_type, ":agent_race", ":agent_troop"),
    (neq, ":agent_race", tf_troll),
  ]),

]) + [

# Kham - Warband Formations Addition END

# #Player team formations functions

  # script_player_attempt_formation
  # Inputs:	arg1: troop class (grc_*)
  #			arg2: formation identifier (formation_*)
  # Output: none
  ("player_attempt_formation", [
	(store_script_param, ":fclass", 1),
	(store_script_param, ":fformation", 2),
	(set_fixed_point_multiplier, 100),
	(try_begin),
		(class_is_listening_order, "$fplayer_team_no", ":fclass"),
		(try_begin),
			(eq, ":fformation", formation_ranks),
			(str_store_string, s1, "@ranks"),
		(else_try),
			(eq, ":fformation", formation_shield),
			(str_store_string, s1, "@shield wall"),
		(else_try),
			(eq, ":fformation", formation_wedge),
			(str_store_string, s1, "@wedge"),
		(else_try),
			(eq, ":fformation", formation_square),
			(str_store_string, s1, "@square"),
		(else_try),
			(str_store_string, s1, "@up"),
		(try_end),
		(assign, ":new_formation", 0),

		(try_begin),
			(eq, ":fclass", grc_infantry),
			(try_begin),
				(neq, "$infantry_formation_type", ":fformation"),
				(assign, ":new_formation", 1),
				(assign, "$infantry_formation_type", ":fformation"),
				(lt, "$infantry_space", formation_start_spread_out),
				(assign, "$infantry_space", formation_start_spread_out),	#spread out for ease of forming up
			(try_end),
			(try_begin),
				(call_script, "script_formation_end", "$fplayer_team_no", grc_infantry), #Kham - Band-aid Fix for Troops being unresponsive after forming up by breaking formations first, before forming up.
				#(display_message, "@DEBUG: Infantry breaking formation before forming up again"),
				(call_script, "script_cf_formation", "$fplayer_team_no", grc_infantry, "$infantry_space", "$infantry_formation_type"),
				(try_begin),
					(eq, ":new_formation", 1),
					(display_message, "@  Infantry forming {s1}."),
				(try_end),
			(else_try),
				(assign, "$infantry_formation_type", formation_none),
				(gt, reg0, 0),
				(display_message, "@  Not enough infantry to form {s1}, holding instead."),
				(call_script, "script_formation_end", "$fplayer_team_no", grc_infantry),
			(try_end),
			(assign, "$infantry_formation_move_order", mordr_hold),
			(set_show_messages, 0),
			(team_give_order, "$fplayer_team_no", grc_infantry, mordr_hold),
			(team_set_order_position, "$fplayer_team_no", grc_infantry, pos61),
			(set_show_messages, 1),
		(else_try),
			(eq, ":fclass", grc_cavalry),
			(try_begin),
				(neq, "$cavalry_formation_type", ":fformation"),
				(assign, ":new_formation", 1),
				(assign, "$cavalry_formation_type", ":fformation"),
				(lt, "$cavalry_space", formation_start_spread_out),
				(assign, "$cavalry_space", formation_start_spread_out),	#spread out for ease of forming up
			(try_end),
			(try_begin),
				(call_script, "script_formation_end", "$fplayer_team_no", grc_cavalry),  #Kham - Band-aid Fix for Troops being unresponsive after forming up by breaking formations first, before forming up.
				#(display_message, "@DEBUG: Cavalry breaking formation before forming up again"),
				(call_script, "script_cf_formation", "$fplayer_team_no", grc_cavalry, "$cavalry_space", "$cavalry_formation_type"),
				(try_begin),
					(eq, ":new_formation", 1),
					(display_message, "@  Cavalry forming {s1}."),
				(try_end),
			(else_try),
				(assign, "$cavalry_formation_type", formation_none),
				(gt, reg0, 0),
				(display_message, "@  Not enough cavalry to form {s1}, holding instead."),
				(call_script, "script_formation_end", "$fplayer_team_no", grc_cavalry),
			(try_end),
			(assign, "$cavalry_formation_move_order", mordr_hold),
			(set_show_messages, 0),
			(team_give_order, "$fplayer_team_no", grc_cavalry, mordr_hold),
			(team_set_order_position, "$fplayer_team_no", grc_cavalry, pos61),
			(set_show_messages, 1),
		(else_try),	#must be archers
			(eq, ":fclass", grc_archers),
			(try_begin),
				(neq, "$archer_formation_type", ":fformation"),
				(assign, ":new_formation", 1),
				(assign, "$archer_formation_type", ":fformation"),
				(lt, "$archer_space", formation_start_spread_out),
				(assign, "$archer_space", formation_start_spread_out),	#spread out for ease of forming up
			(try_end),
			(try_begin),
				(call_script, "script_formation_end", "$fplayer_team_no", grc_archers),  #Kham - Band-aid Fix for Troops being unresponsive after forming up by breaking formations first, before forming up.
				#(display_message, "@DEBUG: Archers breaking formation before forming up again"),
				(call_script, "script_cf_formation", "$fplayer_team_no", grc_archers, "$archer_space", "$archer_formation_type"),
				(try_begin),
					(eq, ":new_formation", 1),
					(display_message, "@  Archers forming {s1}."),
				(try_end),
			(else_try),
				(assign, "$archer_formation_type", formation_none),
				(gt, reg0, 0),
				(display_message, "@  Not enough archers to form {s1}, holding instead."),
				(call_script, "script_formation_end", "$fplayer_team_no", grc_archers),
			(try_end),
			(assign, "$archer_formation_move_order", mordr_hold),
			(set_show_messages, 0),
			(team_give_order, "$fplayer_team_no", grc_archers, mordr_hold),
			(team_set_order_position, "$fplayer_team_no", grc_archers, pos61),
			(set_show_messages, 1),
		(try_end),
	(try_end)
  ]),
  
  
  # script_player_order_formations by motomataru #Kham - edited
  # Inputs:	arg1: order to formation (mordr_*)
  # Output: none
  ("player_order_formations", [
	(store_script_param, ":forder", 1),
	(set_fixed_point_multiplier, 100),
	
	(try_begin), #On hold, any formations reform in new location		
		(eq, ":forder", mordr_hold),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(call_script, "script_player_attempt_formation", grc_infantry, "$infantry_formation_type"),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(call_script, "script_player_attempt_formation", grc_cavalry, "$cavalry_formation_type"),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(call_script, "script_player_attempt_formation", grc_archers, "$archer_formation_type"),
		(try_end),
		
	(else_try),	#Follow is hold	repeated frequently
		(eq, ":forder", mordr_follow),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(assign, "$infantry_formation_move_order", mordr_follow),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
			(assign, "$cavalry_formation_move_order", mordr_follow),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_archers),
			(assign, "$archer_formation_move_order", mordr_follow),
		(try_end),
		
	(else_try),	#charge ends formation
		(eq, ":forder", mordr_charge),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(call_script, "script_formation_end", "$fplayer_team_no", grc_infantry),
			(display_message, "@  Infantry formation disassembled."),
			(assign, "$infantry_formation_type", formation_none),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_formation_end", "$fplayer_team_no", grc_cavalry),
			(display_message, "@  Cavalry formation disassembled."),
			(assign, "$cavalry_formation_type", formation_none),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_archers),
			(call_script, "script_formation_end", "$fplayer_team_no", grc_archers),
			(display_message, "@  Archer formation disassembled."),
			(assign, "$archer_formation_type", formation_none),
		(try_end),
		
	(else_try),	#dismount ends formation
		(eq, ":forder", mordr_dismount),
		(neq, "$cavalry_formation_type", formation_none),
		(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
		(call_script, "script_formation_end", "$fplayer_team_no", grc_cavalry),
		(display_message, "@  Cavalry formation disassembled."),
		(assign, "$cavalry_formation_type", formation_none),

	(else_try),
		(eq, ":forder", mordr_advance),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_infantry, "$infantry_formation_type"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$infantry_formation_move_order", mordr_advance),
				# (team_set_order_position, "$fplayer_team_no", grc_infantry, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_infantry, pos63, 1),			
			(call_script, "script_form_infantry", "$fplayer_team_no", "$fplayer_agent_no", "$infantry_space", "$infantry_formation_type"),
			(assign, "$infantry_formation_move_order", mordr_advance),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_cavalry, "$cavalry_formation_type"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$cavalry_formation_move_order", mordr_advance),
				# (team_set_order_position, "$fplayer_team_no", grc_cavalry, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_cavalry, pos63, 1),
			(call_script, "script_form_cavalry", "$fplayer_team_no", "$fplayer_agent_no", "$cavalry_space"),
			(assign, "$cavalry_formation_move_order", mordr_advance),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_archers),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_archers, "$archer_formation_type"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$archer_formation_move_order", mordr_advance),
				# (team_set_order_position, "$fplayer_team_no", grc_archers, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_archers, pos63, 1),
			(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
			(assign, "$archer_formation_move_order", mordr_advance),
		(try_end),

	(else_try),
		(eq, ":forder", mordr_fall_back),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_infantry, "$infantry_formation_type"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$infantry_formation_move_order", mordr_fall_back),
				# (team_set_order_position, "$fplayer_team_no", grc_infantry, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_infantry, pos63, -1),
			(call_script, "script_form_infantry", "$fplayer_team_no", "$fplayer_agent_no", "$infantry_space", "$infantry_formation_type"),
			(assign, "$infantry_formation_move_order", mordr_fall_back),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_cavalry, "$cavalry_formation_type"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$cavalry_formation_move_order", mordr_fall_back),
				# (team_set_order_position, "$fplayer_team_no", grc_cavalry, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_cavalry, pos63, -1),
			(call_script, "script_form_cavalry", "$fplayer_team_no", "$fplayer_agent_no", "$cavalry_space"),
			(assign, "$cavalry_formation_move_order", mordr_fall_back),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_archers),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_archers, "$archer_formation_type"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$archer_formation_move_order", mordr_fall_back),
				# (team_set_order_position, "$fplayer_team_no", grc_archers, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_archers, pos63, -1),
			(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
			(assign, "$archer_formation_move_order", mordr_fall_back),
		(try_end),

	(else_try),
		(eq, ":forder", mordr_stand_closer),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(gt, "$infantry_space", 0),
			(assign, ":troop_count", 0),
			(try_for_agents, reg0),
				(call_script, "script_cf_valid_formation_member", "$fplayer_team_no", grc_infantry, "$fplayer_agent_no", reg0),
				(val_add, ":troop_count", 1),
			(try_end),
			(call_script, "script_get_centering_amount", "$infantry_formation_type", ":troop_count", "$infantry_space"),
			(assign, ":adjust_amount", reg0),
			(val_sub, "$infantry_space", 1),
			(call_script, "script_get_centering_amount", "$infantry_formation_type", ":troop_count", "$infantry_space"),
			(val_sub, ":adjust_amount", reg0),
#			(team_get_order_position, pos1, "$fplayer_team_no", grc_infantry),
			(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_infantry),
			(agent_get_position, pos0, "$fplayer_agent_no"),
			(get_distance_between_positions, reg0, pos1, pos0),
			(val_sub, reg0, 100),
			(try_begin),	#not close to player?
				(lt, ":adjust_amount", reg0),
				(val_mul, ":adjust_amount", -1),
				(position_move_x, pos1, ":adjust_amount"),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos1),
			(try_end),
			(call_script, "script_form_infantry", "$fplayer_team_no", "$fplayer_agent_no", "$infantry_space", "$infantry_formation_type"),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
			(gt, "$cavalry_space", 0),
			(val_sub, "$cavalry_space", 1),
#			(team_get_order_position, pos1, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_form_cavalry", "$fplayer_team_no", "$fplayer_agent_no", "$cavalry_space"),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_archers),
			(gt, "$archer_space", 0),
			(assign, ":troop_count", 0),
			(try_for_agents, reg0),
				(call_script, "script_cf_valid_formation_member", "$fplayer_team_no", grc_archers, "$fplayer_agent_no", reg0),
				(val_add, ":troop_count", 1),
			(try_end),
			(call_script, "script_get_centering_amount", formation_default, ":troop_count", "$archer_space"),
			(assign, ":adjust_amount", reg0),
			(val_sub, "$archer_space", 1),
			(call_script, "script_get_centering_amount", formation_default, ":troop_count", "$archer_space"),
			(val_sub, ":adjust_amount", reg0),
#			(team_get_order_position, pos1, "$fplayer_team_no", grc_archers),
			(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_archers),
			(position_move_x, pos1, ":adjust_amount"),
			(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos1),
			(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
		(try_end),

	(else_try),
		(eq, ":forder", mordr_spread_out),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(assign, ":troop_count", 0),
			(try_for_agents, reg0),
				(call_script, "script_cf_valid_formation_member", "$fplayer_team_no", grc_infantry, "$fplayer_agent_no", reg0),
				(val_add, ":troop_count", 1),
			(try_end),
			(call_script, "script_get_centering_amount", "$infantry_formation_type", ":troop_count", "$infantry_space"),
			(store_mul, ":adjust_amount", reg0, -1),
			(val_add, "$infantry_space", 1),
			(call_script, "script_get_centering_amount", "$infantry_formation_type", ":troop_count", "$infantry_space"),
			(val_add, ":adjust_amount", reg0),
#			(team_get_order_position, pos1, "$fplayer_team_no", grc_infantry),
			(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_infantry),
			(agent_get_position, pos0, "$fplayer_agent_no"),
			(get_distance_between_positions, reg0, pos1, pos0),
			(val_sub, reg0, 100),
			(try_begin),	#not close to player?
				(lt, ":adjust_amount", reg0),
				(position_move_x, pos1, ":adjust_amount"),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos1),
			(try_end),
			(call_script, "script_form_infantry", "$fplayer_team_no", "$fplayer_agent_no", "$infantry_space", "$infantry_formation_type"),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
			(val_add, "$cavalry_space", 1),
#			(team_get_order_position, pos1, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_form_cavalry", "$fplayer_team_no", "$fplayer_agent_no", "$cavalry_space"),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_archers),
			(assign, ":troop_count", 0),
			(try_for_agents, reg0),
				(call_script, "script_cf_valid_formation_member", "$fplayer_team_no", grc_archers, "$fplayer_agent_no", reg0),
				(val_add, ":troop_count", 1),
			(try_end),
			(call_script, "script_get_centering_amount", formation_default, ":troop_count", "$archer_space"),
			(store_mul, ":adjust_amount", reg0, -1),
			(val_add, "$archer_space", 1),
			(call_script, "script_get_centering_amount", formation_default, ":troop_count", "$archer_space"),
			(val_add, ":adjust_amount", reg0),
#			(team_get_order_position, pos1, "$fplayer_team_no", grc_archers),
			(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_archers),
			(val_mul, ":adjust_amount", -1),
			(position_move_x, pos1, ":adjust_amount"),
			(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos1),
			(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
		(try_end),

	(else_try),
		(eq, ":forder", mordr_stand_ground),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_infantry, "$infantry_formation_type"),
			(copy_position, pos1, pos63),
			(call_script, "script_form_infantry", "$fplayer_team_no", "$fplayer_agent_no", "$infantry_space", "$infantry_formation_type"),
			(assign, "$infantry_formation_move_order", mordr_stand_ground),
			(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos63),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_cavalry, "$cavalry_formation_type"),
			(copy_position, pos1, pos63),
			(call_script, "script_form_cavalry", "$fplayer_team_no", "$fplayer_agent_no", "$cavalry_space"),
			(assign, "$cavalry_formation_move_order", mordr_stand_ground),
			(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos63),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_archers),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_archers, "$archer_formation_type"),
			(copy_position, pos1, pos63),
			(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
			(assign, "$archer_formation_move_order", mordr_stand_ground),
			(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos63),
		(try_end),			
	(try_end)
  ]),

  
# #Utilities used by formations
  # script_point_y_toward_position by motomataru
  # Input: from position, to position
  # Output: pos62 normalized vector, reg0 fixed point distance
  ("point_y_toward_position", [
	(store_script_param, ":from_position", 1),
	(store_script_param, ":to_position", 2),
	(position_transform_position_to_local, pos62, ":from_position", ":to_position"),
	(position_normalize_origin, ":distance_between", pos62),
	(position_get_x, ":dir_x", pos62),
	(position_get_y, ":dir_y", pos62),
	(try_begin),
		(lt, ":dir_x", 0),
		(assign, ":bound_a", 90),
		(assign, ":bound_b", 270),
		(assign, ":theta", 180),
	(else_try),
		(assign, ":bound_a", 90),
		(assign, ":bound_b", -90),
		(assign, ":theta", 0),
	(try_end),
	(assign, ":sine_theta", 0),	#avoid error on compile
	(convert_to_fixed_point, ":theta"),
	(convert_to_fixed_point, ":bound_a"),
	(convert_to_fixed_point, ":bound_b"),
	(try_for_range, reg0, 0, 6),	#precision 90/2exp6 (around 2 degrees)
		(store_sin, ":sine_theta", ":theta"),
		(try_begin),
			(gt, ":sine_theta", ":dir_y"),
			(assign, ":bound_a", ":theta"),
		(else_try),
			(lt, ":sine_theta", ":dir_y"),
			(assign, ":bound_b", ":theta"),
		(try_end),
		(store_add, ":angle_sum", ":bound_b", ":bound_a"),
		(store_div, ":theta", ":angle_sum", 2),
	(try_end),
	(convert_from_fixed_point, ":theta"),
	(val_sub, ":theta", 90),	#point y-axis at destination
	(position_rotate_z, ":from_position", ":theta"),
	(assign, reg0, ":distance_between"),
  ]),


  # script_store_battlegroup_data by motomataru
  # Input: none
  # Output: sets positions and globals to track data on ALL groups in a battle
  # Globals used: pos1, reg0, reg1, positions 24-45
  ("store_battlegroup_data", [
	(assign, ":team0_leader", 0),
	(assign, ":team0_x_leader", 0),
	(assign, ":team0_y_leader", 0),
	(assign, ":team0_level_leader", 0),
	(assign, "$team0_num_infantry", 0),
	(assign, "$team0_num_archers", 0),
	(assign, "$team0_num_cavalry", 0),
	(assign, "$team0_archers_have_ammo", 1),
	(assign, "$team0_percent_ranged_throw", 0),
	(assign, "$team0_percent_cavalry_are_archers", 0),
	(assign, "$team0_level_infantry", 0),
	(assign, "$team0_level_archers", 0),
	(assign, "$team0_level_cavalry", 0),
	(assign, ":team0_x_infantry", 0),
	(assign, ":team0_x_archers", 0),
	(assign, ":team0_x_cavalry", 0),
	(assign, ":team0_y_infantry", 0),
	(assign, ":team0_y_archers", 0),
	(assign, ":team0_y_cavalry", 0),
	(assign, ":team1_leader", 0),
	(assign, ":team1_x_leader", 0),
	(assign, ":team1_y_leader", 0),
	(assign, ":team1_level_leader", 0),
	(assign, "$team1_num_infantry", 0),
	(assign, "$team1_num_archers", 0),
	(assign, "$team1_num_cavalry", 0),
	(assign, "$team1_archers_have_ammo", 1),
	(assign, "$team1_percent_ranged_throw", 0),
	(assign, "$team1_percent_cavalry_are_archers", 0),
	(assign, "$team1_level_infantry", 0),
	(assign, "$team1_level_archers", 0),
	(assign, "$team1_level_cavalry", 0),
	(assign, ":team1_x_infantry", 0),
	(assign, ":team1_x_archers", 0),
	(assign, ":team1_x_cavalry", 0),
	(assign, ":team1_y_infantry", 0),
	(assign, ":team1_y_archers", 0),
	(assign, ":team1_y_cavalry", 0),
	(assign, ":team2_leader", 0),
	(assign, ":team2_x_leader", 0),
	(assign, ":team2_y_leader", 0),
	(assign, ":team2_level_leader", 0),
	(assign, "$team2_num_infantry", 0),
	(assign, "$team2_num_archers", 0),
	(assign, "$team2_num_cavalry", 0),
	(assign, "$team2_archers_have_ammo", 1),
	(assign, "$team2_percent_ranged_throw", 0),
	(assign, "$team2_percent_cavalry_are_archers", 0),
	(assign, "$team2_level_infantry", 0),
	(assign, "$team2_level_archers", 0),
	(assign, "$team2_level_cavalry", 0),
	(assign, ":team2_x_infantry", 0),
	(assign, ":team2_x_archers", 0),
	(assign, ":team2_x_cavalry", 0),
	(assign, ":team2_y_infantry", 0),
	(assign, ":team2_y_archers", 0),
	(assign, ":team2_y_cavalry", 0),
	(assign, ":team3_leader", 0),
	(assign, ":team3_x_leader", 0),
	(assign, ":team3_y_leader", 0),
	(assign, ":team3_level_leader", 0),
	(assign, "$team3_num_infantry", 0),
	(assign, "$team3_num_archers", 0),
	(assign, "$team3_num_cavalry", 0),
	(assign, "$team3_archers_have_ammo", 1),
	(assign, "$team3_percent_ranged_throw", 0),
	(assign, "$team3_percent_cavalry_are_archers", 0),
	(assign, "$team3_level_infantry", 0),
	(assign, "$team3_level_archers", 0),
	(assign, "$team3_level_cavalry", 0),
	(assign, ":team3_x_infantry", 0),
	(assign, ":team3_x_archers", 0),
	(assign, ":team3_x_cavalry", 0),
	(assign, ":team3_y_infantry", 0),
	(assign, ":team3_y_archers", 0),
	(assign, ":team3_y_cavalry", 0),
	(assign, "$teamp_num_group3", 0),
	(assign, "$teamp_level_group3", 0),
	(assign, ":teamp_x_group3", 0),
	(assign, ":teamp_y_group3", 0),
	(assign, "$teamp_num_group4", 0),
	(assign, "$teamp_level_group4", 0),
	(assign, ":teamp_x_group4", 0),
	(assign, ":teamp_y_group4", 0),
	(assign, "$teamp_num_group5", 0),
	(assign, "$teamp_level_group5", 0),
	(assign, ":teamp_x_group5", 0),
	(assign, ":teamp_y_group5", 0),
	(assign, "$teamp_num_group6", 0),
	(assign, "$teamp_level_group6", 0),
	(assign, ":teamp_x_group6", 0),
	(assign, ":teamp_y_group6", 0),
	(assign, "$teamp_num_group7", 0),
	(assign, "$teamp_level_group7", 0),
	(assign, ":teamp_x_group7", 0),
	(assign, ":teamp_y_group7", 0),
	(assign, "$teamp_num_group8", 0),
	(assign, "$teamp_level_group8", 0),
	(assign, ":teamp_x_group8", 0),
	(assign, ":teamp_y_group8", 0),

	(try_for_agents, ":cur_agent"),
		(agent_is_alive, ":cur_agent"),      
		(agent_is_human, ":cur_agent"), 
		#(agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 0),
		(agent_get_team, ":bgteam", ":cur_agent"),
		
		] + (is_a_wb_script==1 and [

		(call_script, "script_classify_agent", ":cur_agent"),
		(assign, ":bgroup", reg0),
		
		] or [
		
		(agent_get_class, ":bgroup", ":cur_agent"),
		
		]) + [
		
		(agent_get_troop_id, ":cur_troop", ":cur_agent"),
        
		(troop_get_type, ":cur_race", ":cur_troop"),
		(neq, ":cur_race", tf_troll), #disregard trolls
            
		(store_character_level, ":cur_level", ":cur_troop"),
		(agent_get_ammo, ":cur_ammo", ":cur_agent"),
		(agent_get_wielded_item, reg0, ":cur_agent", 0),
		(try_begin),
			(lt, reg0, 0),
			(assign, ":cur_weapon_type", 0),
			(assign, ":cur_weapon_length", 0),
		(else_try),
			(item_get_type, ":cur_weapon_type", reg0),
			(try_begin),
				(eq, ":cur_weapon_type", itp_type_polearm),
				(store_mul, ":cur_weapon_length", Weapon_Length_Proxy, 2),
			(else_try),
				(this_or_next|eq, ":cur_weapon_type", itp_type_one_handed_wpn),
				(eq, ":cur_weapon_type", itp_type_two_handed_wpn),
				(assign, ":cur_weapon_length", Weapon_Length_Proxy),
			(else_try),
				(assign, ":cur_weapon_length", 0),
			(try_end),
		(try_end),
		(agent_get_position, pos1, ":cur_agent"),
		(position_get_x, ":x_value", pos1),
		(position_get_y, ":y_value", pos1),
		(try_begin),
			(eq, ":bgroup", grc_infantry),	#AKA battle group 0
			(try_begin),
				(eq, ":bgteam", 0),
				(val_add, "$team0_num_infantry", 1),
				(val_add, ":team0_x_infantry", ":x_value"),
				(val_add, ":team0_y_infantry", ":y_value"),
				(val_add, "$team0_level_infantry", ":cur_level"),
				(val_add, "$team0_weapon_length_infantry", ":cur_weapon_length"),
			(else_try),
				(eq, ":bgteam", 1),
				(val_add, "$team1_num_infantry", 1),
				(val_add, ":team1_x_infantry", ":x_value"),
				(val_add, ":team1_y_infantry", ":y_value"),
				(val_add, "$team1_level_infantry", ":cur_level"),
				(val_add, "$team1_weapon_length_infantry", ":cur_weapon_length"),
			(else_try),
				(eq, ":bgteam", 2),
				(val_add, "$team2_num_infantry", 1),
				(val_add, ":team2_x_infantry", ":x_value"),
				(val_add, ":team2_y_infantry", ":y_value"),
				(val_add, "$team2_level_infantry", ":cur_level"),
				(val_add, "$team2_weapon_length_infantry", ":cur_weapon_length"),
			(else_try),
				(eq, ":bgteam", 3),
				(val_add, "$team3_num_infantry", 1),
				(val_add, ":team3_x_infantry", ":x_value"),
				(val_add, ":team3_y_infantry", ":y_value"),
				(val_add, "$team3_level_infantry", ":cur_level"),
				(val_add, "$team3_weapon_length_infantry", ":cur_weapon_length"),
			(try_end),
		(else_try),
			(eq, ":bgroup", grc_archers),	#AKA battle group 1
			(try_begin),
				(eq, ":bgteam", 0),
				(val_add, "$team0_num_archers", 1),
				(val_add, ":team0_x_archers", ":x_value"),
				(val_add, ":team0_y_archers", ":y_value"),
				(val_add, "$team0_level_archers", ":cur_level"),
				(val_add, "$team0_weapon_length_archers", ":cur_weapon_length"),
				(try_begin),
					(le, ":cur_ammo", 0),
					(assign, "$team0_archers_have_ammo", 0),
				(try_end),
				(try_begin),
					(eq, ":cur_weapon_type", itp_type_thrown),
					(val_add, "$team0_percent_ranged_throw", 1),
				(try_end),
			(else_try),
				(eq, ":bgteam", 1),
				(val_add, "$team1_num_archers", 1),
				(val_add, ":team1_x_archers", ":x_value"),
				(val_add, ":team1_y_archers", ":y_value"),
				(val_add, "$team1_level_archers", ":cur_level"),
				(val_add, "$team1_weapon_length_archers", ":cur_weapon_length"),
				(try_begin),
					(le, ":cur_ammo", 0),
					(assign, "$team1_archers_have_ammo", 0),
				(try_end),
				(try_begin),
					(eq, ":cur_weapon_type", itp_type_thrown),
					(val_add, "$team1_percent_ranged_throw", 1),
				(try_end),
			(else_try),
				(eq, ":bgteam", 2),
				(val_add, "$team2_num_archers", 1),
				(val_add, ":team2_x_archers", ":x_value"),
				(val_add, ":team2_y_archers", ":y_value"),
				(val_add, "$team2_level_archers", ":cur_level"),
				(val_add, "$team2_weapon_length_archers", ":cur_weapon_length"),
				(try_begin),
					(le, ":cur_ammo", 0),
					(assign, "$team2_archers_have_ammo", 0),
				(try_end),
				(try_begin),
					(eq, ":cur_weapon_type", itp_type_thrown),
					(val_add, "$team2_percent_ranged_throw", 1),
				(try_end),
			(else_try),
				(eq, ":bgteam", 3),
				(val_add, "$team3_num_archers", 1),
				(val_add, ":team3_x_archers", ":x_value"),
				(val_add, ":team3_y_archers", ":y_value"),
				(val_add, "$team3_level_archers", ":cur_level"),
				(val_add, "$team3_weapon_length_archers", ":cur_weapon_length"),
				(try_begin),
					(le, ":cur_ammo", 0),
					(assign, "$team3_archers_have_ammo", 0),
				(try_end),
				(try_begin),
					(eq, ":cur_weapon_type", itp_type_thrown),
					(val_add, "$team3_percent_ranged_throw", 1),
				(try_end),
			(try_end),
		(else_try),
			(eq, ":bgroup", grc_cavalry),	#AKA battle group 2
			(try_begin),
				(eq, ":bgteam", 0),
				(val_add, "$team0_num_cavalry", 1),
				(val_add, ":team0_x_cavalry", ":x_value"),
				(val_add, ":team0_y_cavalry", ":y_value"),
				(val_add, "$team0_level_cavalry", ":cur_level"),
				(val_add, "$team0_weapon_length_cavalry", ":cur_weapon_length"),
				(try_begin),
					(gt, ":cur_ammo", 0),
					(neq, ":cur_weapon_type", itp_type_thrown), #added by JL to exclude throwing weapons from being horse archers
					(val_add, "$team0_percent_cavalry_are_archers", 1),
				(try_end),
			(else_try),
				(eq, ":bgteam", 1),
				(val_add, "$team1_num_cavalry", 1),
				(val_add, ":team1_x_cavalry", ":x_value"),
				(val_add, ":team1_y_cavalry", ":y_value"),
				(val_add, "$team1_level_cavalry", ":cur_level"),
				(val_add, "$team1_weapon_length_cavalry", ":cur_weapon_length"),
				(try_begin),
					(gt, ":cur_ammo", 0),
					(neq, ":cur_weapon_type", itp_type_thrown), #added by JL to exclude throwing weapons from being horse archers
					(val_add, "$team1_percent_cavalry_are_archers", 1),
				(try_end),
			(else_try),
				(eq, ":bgteam", 2),
				(val_add, "$team2_num_cavalry", 1),
				(val_add, ":team2_x_cavalry", ":x_value"),
				(val_add, ":team2_y_cavalry", ":y_value"),
				(val_add, "$team2_level_cavalry", ":cur_level"),
				(val_add, "$team2_weapon_length_cavalry", ":cur_weapon_length"),
				(try_begin),
					(gt, ":cur_ammo", 0),
					(neq, ":cur_weapon_type", itp_type_thrown), #added by JL to exclude throwing weapons from being horse archers
					(val_add, "$team2_percent_cavalry_are_archers", 1),
				(try_end),
			(else_try),
				(eq, ":bgteam", 3),
				(val_add, "$team3_num_cavalry", 1),
				(val_add, ":team3_x_cavalry", ":x_value"),
				(val_add, ":team3_y_cavalry", ":y_value"),
				(val_add, "$team3_level_cavalry", ":cur_level"),
				(val_add, "$team3_weapon_length_cavalry", ":cur_weapon_length"),
				(try_begin),
					(gt, ":cur_ammo", 0),
					(neq, ":cur_weapon_type", itp_type_thrown), #added by JL to exclude throwing weapons from being horse archers
					(val_add, "$team3_percent_cavalry_are_archers", 1),
				(try_end),
			(try_end),
		(else_try),
			(eq, ":bgroup", 3),
			(val_add, "$teamp_num_group3", 1),
			(val_add, ":teamp_x_group3", ":x_value"),
			(val_add, ":teamp_y_group3", ":y_value"),
			(val_add, "$teamp_level_group3", ":cur_level"),
			(val_add, "$teamp_weapon_length_group3", ":cur_weapon_length"),
		(else_try),
			(eq, ":bgroup", 4),
			(val_add, "$teamp_num_group4", 1),
			(val_add, ":teamp_x_group4", ":x_value"),
			(val_add, ":teamp_y_group4", ":y_value"),
			(val_add, "$teamp_level_group4", ":cur_level"),
			(val_add, "$teamp_weapon_length_group4", ":cur_weapon_length"),
		(else_try),
			(eq, ":bgroup", 5),
			(val_add, "$teamp_num_group5", 1),
			(val_add, ":teamp_x_group5", ":x_value"),
			(val_add, ":teamp_y_group5", ":y_value"),
			(val_add, "$teamp_level_group5", ":cur_level"),
			(val_add, "$teamp_weapon_length_group5", ":cur_weapon_length"),
		(else_try),
			(eq, ":bgroup", 6),
			(val_add, "$teamp_num_group6", 1),
			(val_add, ":teamp_x_group6", ":x_value"),
			(val_add, ":teamp_y_group6", ":y_value"),
			(val_add, "$teamp_level_group6", ":cur_level"),
			(val_add, "$teamp_weapon_length_group6", ":cur_weapon_length"),
		(else_try),
			(eq, ":bgroup", 7),
			(val_add, "$teamp_num_group7", 1),
			(val_add, ":teamp_x_group7", ":x_value"),
			(val_add, ":teamp_y_group7", ":y_value"),
			(val_add, "$teamp_level_group7", ":cur_level"),
			(val_add, "$teamp_weapon_length_group7", ":cur_weapon_length"),
		(else_try),
			(eq, ":bgroup", 8),
			(val_add, "$teamp_num_group8", 1),
			(val_add, ":teamp_x_group8", ":x_value"),
			(val_add, ":teamp_y_group8", ":y_value"),
			(val_add, "$teamp_level_group8", ":cur_level"),
			(val_add, "$teamp_weapon_length_group8", ":cur_weapon_length"),
		(else_try),
			(eq, ":bgroup", -1),	#leaders
			(try_begin),
				(eq, ":bgteam", 0),
				(assign, ":team0_leader", 1),
				(assign, ":team0_x_leader", ":x_value"),
				(assign, ":team0_y_leader", ":y_value"),
				(assign, ":team0_level_leader", ":cur_level"),
			(else_try),
				(eq, ":bgteam", 1),
				(assign, ":team1_leader", 1),
				(assign, ":team1_x_leader", ":x_value"),
				(assign, ":team1_y_leader", ":y_value"),
				(assign, ":team1_level_leader", ":cur_level"),
			(else_try),
				(eq, ":bgteam", 2),
				(assign, ":team2_leader", 1),
				(assign, ":team2_x_leader", ":x_value"),
				(assign, ":team2_y_leader", ":y_value"),
				(assign, ":team2_level_leader", ":cur_level"),
			(else_try),
				(eq, ":bgteam", 3),
				(assign, ":team3_leader", 1),
				(assign, ":team3_x_leader", ":x_value"),
				(assign, ":team3_y_leader", ":y_value"),
				(assign, ":team3_level_leader", ":cur_level"),
			(try_end),
		(try_end),
	(try_end),

	#calculate team sizes, sum positions
	(store_add, "$team0_size", "$team0_num_infantry", "$team0_num_archers"),
	(val_add, "$team0_size", "$team0_num_cavalry"),
	(val_add, "$team0_size", ":team0_leader"),
	(store_add, ":team0_x", ":team0_x_infantry", ":team0_x_archers"),
	(val_add, ":team0_x", ":team0_x_cavalry"),
	(val_add, ":team0_x", ":team0_x_leader"),
	(store_add, ":team0_y", ":team0_y_infantry", ":team0_y_archers"),
	(val_add, ":team0_y", ":team0_y_cavalry"),
	(val_add, ":team0_y", ":team0_y_leader"),
	(store_add, "$team0_level", "$team0_level_infantry", "$team0_level_archers"),
	(val_add, "$team0_level", "$team0_level_cavalry"),
	(val_add, "$team0_level", ":team0_level_leader"),

	(store_add, "$team1_size", "$team1_num_infantry", "$team1_num_archers"),
	(val_add, "$team1_size", "$team1_num_cavalry"),
	(val_add, "$team1_size", ":team1_leader"),
	(store_add, ":team1_x", ":team1_x_infantry", ":team1_x_archers"),
	(val_add, ":team1_x", ":team1_x_cavalry"),
	(val_add, ":team1_x", ":team1_x_leader"),
	(store_add, ":team1_y", ":team1_y_infantry", ":team1_y_archers"),
	(val_add, ":team1_y", ":team1_y_cavalry"),
	(val_add, ":team1_y", ":team1_y_leader"),
	(store_add, "$team1_level", "$team1_level_infantry", "$team1_level_archers"),
	(val_add, "$team1_level", "$team1_level_cavalry"),
	(val_add, "$team1_level", ":team1_level_leader"),

	(store_add, "$team2_size", "$team2_num_infantry", "$team2_num_archers"),
	(val_add, "$team2_size", "$team2_num_cavalry"),
	(val_add, "$team2_size", ":team2_leader"),
	(store_add, ":team2_x", ":team2_x_infantry", ":team2_x_archers"),
	(val_add, ":team2_x", ":team2_x_cavalry"),
	(val_add, ":team2_x", ":team2_x_leader"),
	(store_add, ":team2_y", ":team2_y_infantry", ":team2_y_archers"),
	(val_add, ":team2_y", ":team2_y_cavalry"),
	(val_add, ":team2_y", ":team2_y_leader"),
	(store_add, "$team2_level", "$team2_level_infantry", "$team2_level_archers"),
	(val_add, "$team2_level", "$team2_level_cavalry"),
	(val_add, "$team2_level", ":team2_level_leader"),

	(store_add, "$team3_size", "$team3_num_infantry", "$team3_num_archers"),
	(val_add, "$team3_size", "$team3_num_cavalry"),
	(val_add, "$team3_size", ":team3_leader"),
	(store_add, ":team3_x", ":team3_x_infantry", ":team3_x_archers"),
	(val_add, ":team3_x", ":team3_x_cavalry"),
	(val_add, ":team3_x", ":team3_x_leader"),
	(store_add, ":team3_y", ":team3_y_infantry", ":team3_y_archers"),
	(val_add, ":team3_y", ":team3_y_cavalry"),
	(val_add, ":team3_y", ":team3_y_leader"),
	(store_add, "$team3_level", "$team3_level_infantry", "$team3_level_archers"),
	(val_add, "$team3_level", "$team3_level_cavalry"),
	(val_add, "$team3_level", ":team3_level_leader"),

	(store_add, ":additional_troops", "$teamp_num_group3", "$teamp_num_group4"),
	(val_add, ":additional_troops", "$teamp_num_group5"),
	(val_add, ":additional_troops", "$teamp_num_group6"),
	(val_add, ":additional_troops", "$teamp_num_group7"),
	(val_add, ":additional_troops", "$teamp_num_group8"),
	(store_add, ":additional_level", "$teamp_level_group3", "$teamp_level_group4"),
	(val_add, ":additional_level", "$teamp_level_group5"),
	(val_add, ":additional_level", "$teamp_level_group6"),
	(val_add, ":additional_level", "$teamp_level_group7"),
	(val_add, ":additional_level", "$teamp_level_group8"),
	(try_begin),
		(eq, "$fplayer_team_no", 0),
		(val_add, "$team0_size", ":additional_troops"),
		(val_add, "$team0_level", ":additional_level"),
	(else_try),
		(eq, "$fplayer_team_no", 1),
		(val_add, "$team1_size", ":additional_troops"),
		(val_add, "$team1_level", ":additional_level"),
	(else_try),
		(eq, "$fplayer_team_no", 2),
		(val_add, "$team2_size", ":additional_troops"),
		(val_add, "$team2_level", ":additional_level"),
	(else_try),
		(eq, "$fplayer_team_no", 3),
		(val_add, "$team3_size", ":additional_troops"),
		(val_add, "$team3_level", ":additional_level"),
	(try_end),
	
	#calculate team averages
	(init_position, Team0_Average_Pos),
	(try_begin),
		(gt, "$team0_size", 0),
		(val_div, ":team0_x", "$team0_size"),
		(position_set_x, Team0_Average_Pos, ":team0_x"),
		(val_div, ":team0_y", "$team0_size"),
		(position_set_y, Team0_Average_Pos, ":team0_y"),
		(position_set_z_to_ground_level, Team0_Average_Pos),
		(val_div, "$team0_level", "$team0_size"),
	(try_end),
	(init_position, Team1_Average_Pos),
	(try_begin),
		(gt, "$team1_size", 0),
		(val_div, ":team1_x", "$team1_size"),
		(position_set_x, Team1_Average_Pos, ":team1_x"),
		(val_div, ":team1_y", "$team1_size"),
		(position_set_y, Team1_Average_Pos, ":team1_y"),
		(position_set_z_to_ground_level, Team1_Average_Pos),
		(val_div, "$team1_level", "$team1_size"),
	(try_end),
	(init_position, Team2_Average_Pos),
	(try_begin),
		(gt, "$team2_size", 0),
		(val_div, ":team2_x", "$team2_size"),
		(position_set_x, Team2_Average_Pos, ":team2_x"),
		(val_div, ":team2_y", "$team2_size"),
		(position_set_y, Team2_Average_Pos, ":team2_y"),
		(position_set_z_to_ground_level, Team2_Average_Pos),
		(val_div, "$team2_level", "$team2_size"),
	(try_end),
	(init_position, Team3_Average_Pos),
	(try_begin),
		(gt, "$team3_size", 0),
		(val_div, ":team3_x", "$team3_size"),
		(position_set_x, Team3_Average_Pos, ":team3_x"),
		(val_div, ":team3_y", "$team3_size"),
		(position_set_y, Team3_Average_Pos, ":team3_y"),
		(position_set_z_to_ground_level, Team3_Average_Pos),
		(val_div, "$team3_level", "$team3_size"),
	(try_end),


	#calculate battle group averages
	(init_position, Team0_Infantry_Pos),
	(try_begin),
		(gt, "$team0_num_infantry", 0),
		(val_div, ":team0_x_infantry", "$team0_num_infantry"),
		(position_set_x, Team0_Infantry_Pos, ":team0_x_infantry"),
		(val_div, ":team0_y_infantry", "$team0_num_infantry"),
		(position_set_y, Team0_Infantry_Pos, ":team0_y_infantry"),
		(position_set_z_to_ground_level, Team0_Infantry_Pos),
		(val_div, "$team0_level_infantry", "$team0_num_infantry"),
		(val_div, "$team0_weapon_length_infantry", "$team0_num_infantry"),
	(try_end),
	(init_position, Team1_Infantry_Pos),
	(try_begin),
		(gt, "$team1_num_infantry", 0),
		(val_div, ":team1_x_infantry", "$team1_num_infantry"),
		(position_set_x, Team1_Infantry_Pos, ":team1_x_infantry"),
		(val_div, ":team1_y_infantry", "$team1_num_infantry"),
		(position_set_y, Team1_Infantry_Pos, ":team1_y_infantry"),
		(position_set_z_to_ground_level, Team1_Infantry_Pos),
		(val_div, "$team1_level_infantry", "$team1_num_infantry"),
		(val_div, "$team1_weapon_length_infantry", "$team1_num_infantry"),
	(try_end),
	(init_position, Team2_Infantry_Pos),
	(try_begin),
		(gt, "$team2_num_infantry", 0),
		(val_div, ":team2_x_infantry", "$team2_num_infantry"),
		(position_set_x, Team2_Infantry_Pos, ":team2_x_infantry"),
		(val_div, ":team2_y_infantry", "$team2_num_infantry"),
		(position_set_y, Team2_Infantry_Pos, ":team2_y_infantry"),
		(position_set_z_to_ground_level, Team2_Infantry_Pos),
		(val_div, "$team2_level_infantry", "$team2_num_infantry"),
		(val_div, "$team2_weapon_length_infantry", "$team2_num_infantry"),
	(try_end),
	(init_position, Team3_Infantry_Pos),
	(try_begin),
		(gt, "$team3_num_infantry", 0),
		(val_div, ":team3_x_infantry", "$team3_num_infantry"),
		(position_set_x, Team3_Infantry_Pos, ":team3_x_infantry"),
		(val_div, ":team3_y_infantry", "$team3_num_infantry"),
		(position_set_y, Team3_Infantry_Pos, ":team3_y_infantry"),
		(position_set_z_to_ground_level, Team3_Infantry_Pos),
		(val_div, "$team3_level_infantry", "$team3_num_infantry"),
		(val_div, "$team3_weapon_length_infantry", "$team3_num_infantry"),
	(try_end),
	(init_position, Team0_Archers_Pos),
	(try_begin),
		(gt, "$team0_num_archers", 0),
		(val_div, ":team0_x_archers", "$team0_num_archers"),
		(position_set_x, Team0_Archers_Pos, ":team0_x_archers"),
		(val_div, ":team0_y_archers", "$team0_num_archers"),
		(position_set_y, Team0_Archers_Pos, ":team0_y_archers"),
		(position_set_z_to_ground_level, Team0_Archers_Pos),
		(val_div, "$team0_level_archers", "$team0_num_archers"),
		(val_div, "$team0_weapon_length_archers", "$team0_num_archers"),
		(val_mul, "$team0_percent_ranged_throw", 100),
		(val_div, "$team0_percent_ranged_throw", "$team0_num_archers"),
	(try_end),
	(init_position, Team1_Archers_Pos),
	(try_begin),
		(gt, "$team1_num_archers", 0),
		(val_div, ":team1_x_archers", "$team1_num_archers"),
		(position_set_x, Team1_Archers_Pos, ":team1_x_archers"),
		(val_div, ":team1_y_archers", "$team1_num_archers"),
		(position_set_y, Team1_Archers_Pos, ":team1_y_archers"),
		(position_set_z_to_ground_level, Team1_Archers_Pos),
		(val_div, "$team1_level_archers", "$team1_num_archers"),
		(val_div, "$team1_weapon_length_archers", "$team1_num_archers"),
		(val_mul, "$team1_percent_ranged_throw", 100),
		(val_div, "$team1_percent_ranged_throw", "$team1_num_archers"),
	(try_end),
	(init_position, Team2_Archers_Pos),
	(try_begin),
		(gt, "$team2_num_archers", 0),
		(val_div, ":team2_x_archers", "$team2_num_archers"),
		(position_set_x, Team2_Archers_Pos, ":team2_x_archers"),
		(val_div, ":team2_y_archers", "$team2_num_archers"),
		(position_set_y, Team2_Archers_Pos, ":team2_y_archers"),
		(position_set_z_to_ground_level, Team2_Archers_Pos),
		(val_div, "$team2_level_archers", "$team2_num_archers"),
		(val_div, "$team2_weapon_length_archers", "$team2_num_archers"),
		(val_mul, "$team2_percent_ranged_throw", 100),
		(val_div, "$team2_percent_ranged_throw", "$team2_num_archers"),
	(try_end),
	(init_position, Team3_Archers_Pos),
	(try_begin),
		(gt, "$team3_num_archers", 0),
		(val_div, ":team3_x_archers", "$team3_num_archers"),
		(position_set_x, Team3_Archers_Pos, ":team3_x_archers"),
		(val_div, ":team3_y_archers", "$team3_num_archers"),
		(position_set_y, Team3_Archers_Pos, ":team3_y_archers"),
		(position_set_z_to_ground_level, Team3_Archers_Pos),
		(val_div, "$team3_level_archers", "$team3_num_archers"),
		(val_div, "$team3_weapon_length_archers", "$team3_num_archers"),
		(val_mul, "$team3_percent_ranged_throw", 100),
		(val_div, "$team3_percent_ranged_throw", "$team3_num_archers"),
	(try_end),
	(init_position, Team0_Cavalry_Pos),
	(try_begin),
		(gt, "$team0_num_cavalry", 0),
		(val_div, ":team0_x_cavalry", "$team0_num_cavalry"),
		(position_set_x, Team0_Cavalry_Pos, ":team0_x_cavalry"),
		(val_div, ":team0_y_cavalry", "$team0_num_cavalry"),
		(position_set_y, Team0_Cavalry_Pos, ":team0_y_cavalry"),
		(position_set_z_to_ground_level, Team0_Cavalry_Pos),
		(val_div, "$team0_level_cavalry", "$team0_num_cavalry"),
		(val_div, "$team0_weapon_length_cavalry", "$team0_num_cavalry"),
		(val_mul, "$team0_percent_cavalry_are_archers", 100),
		(val_div, "$team0_percent_cavalry_are_archers", "$team0_num_cavalry"),
	(try_end),
	(init_position, Team1_Cavalry_Pos),
	(try_begin),
		(gt, "$team1_num_cavalry", 0),
		(val_div, ":team1_x_cavalry", "$team1_num_cavalry"),
		(position_set_x, Team1_Cavalry_Pos, ":team1_x_cavalry"),
		(val_div, ":team1_y_cavalry", "$team1_num_cavalry"),
		(position_set_y, Team1_Cavalry_Pos, ":team1_y_cavalry"),
		(position_set_z_to_ground_level, Team1_Cavalry_Pos),
		(val_div, "$team1_level_cavalry", "$team1_num_cavalry"),
		(val_div, "$team1_weapon_length_cavalry", "$team1_num_cavalry"),
		(val_mul, "$team1_percent_cavalry_are_archers", 100),
		(val_div, "$team1_percent_cavalry_are_archers", "$team1_num_cavalry"),
	(try_end),
	(init_position, Team2_Cavalry_Pos),
	(try_begin),
		(gt, "$team2_num_cavalry", 0),
		(val_div, ":team2_x_cavalry", "$team2_num_cavalry"),
		(position_set_x, Team2_Cavalry_Pos, ":team2_x_cavalry"),
		(val_div, ":team2_y_cavalry", "$team2_num_cavalry"),
		(position_set_y, Team2_Cavalry_Pos, ":team2_y_cavalry"),
		(position_set_z_to_ground_level, Team2_Cavalry_Pos),
		(val_div, "$team2_level_cavalry", "$team2_num_cavalry"),
		(val_div, "$team2_weapon_length_cavalry", "$team2_num_cavalry"),
		(val_mul, "$team2_percent_cavalry_are_archers", 100),
		(val_div, "$team2_percent_cavalry_are_archers", "$team2_num_cavalry"),
	(try_end),
	(init_position, Team3_Cavalry_Pos),
	(try_begin),
		(gt, "$team3_num_cavalry", 0),
		(val_div, ":team3_x_cavalry", "$team3_num_cavalry"),
		(position_set_x, Team3_Cavalry_Pos, ":team3_x_cavalry"),
		(val_div, ":team3_y_cavalry", "$team3_num_cavalry"),
		(position_set_y, Team3_Cavalry_Pos, ":team3_y_cavalry"),
		(position_set_z_to_ground_level, Team3_Cavalry_Pos),
		(val_div, "$team3_level_cavalry", "$team3_num_cavalry"),
		(val_div, "$team3_weapon_length_cavalry", "$team3_num_cavalry"),
		(val_mul, "$team3_percent_cavalry_are_archers", 100),
		(val_div, "$team3_percent_cavalry_are_archers", "$team3_num_cavalry"),
	(try_end),

	(init_position, Player_Battle_Group3_Pos),
	(try_begin),
		(gt, "$teamp_num_group3", 0),
		(val_div, ":teamp_x_group3", "$teamp_num_group3"),
		(position_set_x, Player_Battle_Group3_Pos, ":teamp_x_group3"),
		(val_div, ":teamp_y_group3", "$teamp_num_group3"),
		(position_set_y, Player_Battle_Group3_Pos, ":teamp_y_group3"),
		(position_set_z_to_ground_level, Player_Battle_Group3_Pos),
		(val_div, "$teamp_level_group3", "$teamp_num_group3"),
		(val_div, "$teamp_weapon_length_group3", "$teamp_num_group3"),
	(try_end),
	(init_position, Player_Battle_Group4_Pos),
	(try_begin),
		(gt, "$teamp_num_group4", 0),
		(val_div, ":teamp_x_group4", "$teamp_num_group4"),
		(position_set_x, Player_Battle_Group4_Pos, ":teamp_x_group4"),
		(val_div, ":teamp_y_group4", "$teamp_num_group4"),
		(position_set_y, Player_Battle_Group4_Pos, ":teamp_y_group4"),
		(position_set_z_to_ground_level, Player_Battle_Group4_Pos),
		(val_div, "$teamp_level_group4", "$teamp_num_group4"),
		(val_div, "$teamp_weapon_length_group4", "$teamp_num_group4"),
	(try_end),
	(init_position, Player_Battle_Group5_Pos),
	(try_begin),
		(gt, "$teamp_num_group5", 0),
		(val_div, ":teamp_x_group5", "$teamp_num_group5"),
		(position_set_x, Player_Battle_Group5_Pos, ":teamp_x_group5"),
		(val_div, ":teamp_y_group5", "$teamp_num_group5"),
		(position_set_y, Player_Battle_Group5_Pos, ":teamp_y_group5"),
		(position_set_z_to_ground_level, Player_Battle_Group5_Pos),
		(val_div, "$teamp_level_group5", "$teamp_num_group5"),
		(val_div, "$teamp_weapon_length_group5", "$teamp_num_group5"),
	(try_end),
	(init_position, Player_Battle_Group6_Pos),
	(try_begin),
		(gt, "$teamp_num_group6", 0),
		(val_div, ":teamp_x_group6", "$teamp_num_group6"),
		(position_set_x, Player_Battle_Group6_Pos, ":teamp_x_group6"),
		(val_div, ":teamp_y_group6", "$teamp_num_group6"),
		(position_set_y, Player_Battle_Group6_Pos, ":teamp_y_group6"),
		(position_set_z_to_ground_level, Player_Battle_Group6_Pos),
		(val_div, "$teamp_level_group6", "$teamp_num_group6"),
		(val_div, "$teamp_weapon_length_group6", "$teamp_num_group6"),
	(try_end),
	(init_position, Player_Battle_Group7_Pos),
	(try_begin),
		(gt, "$teamp_num_group7", 0),
		(val_div, ":teamp_x_group7", "$teamp_num_group7"),
		(position_set_x, Player_Battle_Group7_Pos, ":teamp_x_group7"),
		(val_div, ":teamp_y_group7", "$teamp_num_group7"),
		(position_set_y, Player_Battle_Group7_Pos, ":teamp_y_group7"),
		(position_set_z_to_ground_level, Player_Battle_Group7_Pos),
		(val_div, "$teamp_level_group7", "$teamp_num_group7"),
		(val_div, "$teamp_weapon_length_group7", "$teamp_num_group7"),
	(try_end),
	(init_position, Player_Battle_Group8_Pos),
	(try_begin),
		(gt, "$teamp_num_group8", 0),
		(val_div, ":teamp_x_group8", "$teamp_num_group8"),
		(position_set_x, Player_Battle_Group8_Pos, ":teamp_x_group8"),
		(val_div, ":teamp_y_group8", "$teamp_num_group8"),
		(position_set_y, Player_Battle_Group8_Pos, ":teamp_y_group8"),
		(position_set_z_to_ground_level, Player_Battle_Group8_Pos),
		(val_div, "$teamp_level_group8", "$teamp_num_group8"),
		(val_div, "$teamp_weapon_length_group8", "$teamp_num_group8"),
	(try_end),
	]),


  # script_battlegroup_get_size by motomataru
  # Input: team, battle group (troop class)
  # Output:	reg0 contains size
  #			size of whole team if "troop class" input NOT set to 0-8
  # NB: Assumes that battle groups beyond 2 are PLAYER team
  ("battlegroup_get_size", [
	(store_script_param, ":bgteam", 1),
	(store_script_param, ":bgroup", 2),
	(try_begin),
		(eq, ":bgroup", grc_infantry),	#AKA battle group 0
		(try_begin),
			(eq, ":bgteam", 0),
			(assign, reg0, "$team0_num_infantry"),
		(else_try),
			(eq, ":bgteam", 1),
			(assign, reg0, "$team1_num_infantry"),
		(else_try),
			(eq, ":bgteam", 2),
			(assign, reg0, "$team2_num_infantry"),
		(else_try),
			(eq, ":bgteam", 3),
			(assign, reg0, "$team3_num_infantry"),
		(try_end),
	(else_try),
		(eq, ":bgroup", grc_archers),	#AKA battle group 1
		(try_begin),
			(eq, ":bgteam", 0),
			(assign, reg0, "$team0_num_archers"),
		(else_try),
			(eq, ":bgteam", 1),
			(assign, reg0, "$team1_num_archers"),
		(else_try),
			(eq, ":bgteam", 2),
			(assign, reg0, "$team2_num_archers"),
		(else_try),
			(eq, ":bgteam", 3),
			(assign, reg0, "$team3_num_archers"),
		(try_end),
	(else_try),
		(eq, ":bgroup", grc_cavalry),	#AKA battle group 2
		(try_begin),
			(eq, ":bgteam", 0),
			(assign, reg0, "$team0_num_cavalry"),
		(else_try),
			(eq, ":bgteam", 1),
			(assign, reg0, "$team1_num_cavalry"),
		(else_try),
			(eq, ":bgteam", 2),
			(assign, reg0, "$team2_num_cavalry"),
		(else_try),
			(eq, ":bgteam", 3),
			(assign, reg0, "$team3_num_cavalry"),
		(try_end),
	(else_try),
		(eq, ":bgroup", 3),
		(assign, reg0, "$teamp_num_group3"),
	(else_try),
		(eq, ":bgroup", 4),
		(assign, reg0, "$teamp_num_group4"),
	(else_try),
		(eq, ":bgroup", 5),
		(assign, reg0, "$teamp_num_group5"),
	(else_try),
		(eq, ":bgroup", 6),
		(assign, reg0, "$teamp_num_group6"),
	(else_try),
		(eq, ":bgroup", 7),
		(assign, reg0, "$teamp_num_group7"),
	(else_try),
		(eq, ":bgroup", 8),
		(assign, reg0, "$teamp_num_group8"),
	(else_try),	#undefined battle group from here on
		(eq, ":bgteam", 0),
		(assign, reg0, "$team0_size"),
	(else_try),
		(eq, ":bgteam", 1),
		(assign, reg0, "$team1_size"),
	(else_try),
		(eq, ":bgteam", 2),
		(assign, reg0, "$team2_size"),
	(else_try),
		(eq, ":bgteam", 3),
		(assign, reg0, "$team3_size"),
	(try_end),
  ]),	

 
  # script_team_get_position_of_enemies by motomataru # Kham - Edited
  # Input: destination position, team
  # Output:	enemy team position
  # Run script_store_battlegroup_data before calling!
  ("team_get_position_of_enemies", [
	(store_script_param, ":bgposition", 1),
	(store_script_param, ":bgteam", 2),
	(assign, ":pos_x", 0),
	(assign, ":pos_y", 0),
	(assign, ":total_size", 0),
	
	(try_for_range, ":other_team", 0, 4),
		(neq, ":other_team", ":bgteam"),
		(call_script, "script_battlegroup_get_size", ":other_team", grc_everyone),
		(assign, ":team_size", reg0),
		(gt, ":team_size", 0),
		(teams_are_enemies, ":other_team", ":bgteam"),
		
		(call_script, "script_battlegroup_get_position", ":bgposition", ":other_team", grc_everyone),
		(position_get_x, reg0, ":bgposition"),
		(val_mul, reg0, ":team_size"),
		(val_add, ":pos_x", reg0),
		(position_get_y, reg0, ":bgposition"),
		(val_mul, reg0, ":team_size"),
		(val_add, ":pos_y", reg0),
		(val_add, ":total_size", ":team_size"),
	(try_end),
	
	(try_begin),
		(eq, ":total_size", 0),
		(init_position, ":bgposition"),
	(else_try),
		(val_div, ":pos_x", ":total_size"),
		(position_set_x, ":bgposition", ":pos_x"),
		(val_div, ":pos_y", ":total_size"),
		(position_set_y, ":bgposition", ":pos_y"),
		(position_set_z_to_ground_level, ":bgposition"),
	(try_end),
  ]),


 #Kham - Warband Formations AI by Motomataru addition
 # script_team_get_average_position_of_enemies_augmented
  # Inputs:	arg1: destination position number
  #			arg2: team_no
  #			arg3: troop class (grc_*)
  # Output: destination position: average position if reg0 > 0
  #			reg0: number of enemies
  ("team_get_average_position_of_enemies_augmented", [
	(store_script_param, ":position_no", 1),
	(store_script_param, ":team_no", 2),
	(store_script_param, ":troop_type", 3),
	(assign, ":num_enemies", 0),
	(assign, ":accum_x", 0),
	(assign, ":accum_y", 0),
	(assign, ":accum_z", 0),
	(try_for_agents, ":enemy_agent"),
		(agent_is_alive, ":enemy_agent"),
		(agent_is_human, ":enemy_agent"),
		(agent_get_team, ":enemy_team", ":enemy_agent"),
		(teams_are_enemies, ":team_no", ":enemy_team"),
		] + (is_a_wb_script==1 and [

		(call_script, "script_classify_agent", ":enemy_agent"),
		(this_or_next|eq, ":troop_type", reg0),

		] or [

		(agent_get_class, ":troop_type", ":enemy_agent"),

		]) + [

		(eq, ":troop_type", grc_everyone),

		(agent_get_position, ":position_no", ":enemy_agent"),
		(position_get_x, ":x", ":position_no"),
		(position_get_y, ":y", ":position_no"),
		(position_get_z, ":z", ":position_no"),
		(val_add, ":accum_x", ":x"),
		(val_add, ":accum_y", ":y"),
		(val_add, ":accum_z", ":z"),
		(val_add, ":num_enemies", 1),
	(try_end),
	(init_position, ":position_no"),
	(try_begin),
		(gt, ":num_enemies", 0),
		(store_div, ":average_x", ":accum_x", ":num_enemies"),
		(store_div, ":average_y", ":accum_y", ":num_enemies"),
		(store_div, ":average_z", ":accum_z", ":num_enemies"),
		(position_set_x, ":position_no", ":average_x"),
		(position_set_y, ":position_no", ":average_y"),
		(position_set_z, ":position_no", ":average_z"),
	(try_end),
	(assign, reg0, ":num_enemies"),
  ]),

 #Kham - Warband Formations AI by Motomataru addition END

# # M&B Standard AI with changes for formations
  # script_formation_battle_tactic_init_aux
  # Input: team_no, battle_tactic
  # Output: none
  ("formation_battle_tactic_init_aux",
    [
      (store_script_param, ":team_no", 1),
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
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
       #(team_get_leader, ":ai_leader", ":team_no"),
        (call_script, "script_team_get_nontroll_leader", ":team_no"),
        (assign, ":ai_leader", reg0),
        (ge, ":ai_leader", 0),
        (agent_set_speed_limit, ":ai_leader", 8),
        (agent_get_position, pos60, ":ai_leader"),
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos60),
      (try_end),
# formations additions
	  (try_begin),
		(call_script, "script_cf_formation", ":team_no", grc_infantry, 0, formation_default),
	  (try_end),
	  (try_begin),
		(call_script, "script_cf_formation", ":team_no", grc_cavalry, 0, formation_wedge),
	  (try_end),
	  (try_begin),
		(call_script, "script_cf_formation", ":team_no", grc_archers, 2, formation_default),
	  (try_end),
	  (team_give_order, ":team_no", grc_archers, mordr_spread_out),
	  (team_give_order, ":team_no", grc_archers, mordr_spread_out),
# end formations additions
  ]),
  
  # script_formation_battle_tactic_apply_aux
  # Input: team_no, battle_tactic
  # Output: battle_tactic
  ("formation_battle_tactic_apply_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
      (store_mission_timer_a, ":mission_time"),
      (try_begin),
        (eq, ":battle_tactic", btactic_hold),
        (copy_position, pos1, pos52),
        (call_script, "script_get_closest3_distance_of_enemies_at_pos1", ":team_no", 1),
        (assign, ":avg_dist", reg0),
        (assign, ":min_dist", reg1),
        (try_begin),
          (this_or_next|lt, ":min_dist", 1000), #Kham - Changed from 1000
          (lt, ":avg_dist", 4000),
          (assign, ":battle_tactic", 0),
		  (call_script, "script_formation_end", ":team_no", grc_infantry),	#formations code
		  (call_script, "script_formation_end", ":team_no", grc_archers),	#formations code
		  (call_script, "script_formation_end", ":team_no", grc_cavalry),	#formations code
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        #(team_get_leader, ":ai_leader", ":team_no"),
        (call_script, "script_team_get_nontroll_leader", ":team_no"),
        (assign, ":ai_leader", reg0),
        (try_begin),
          (ge, ":ai_leader", 0),
          (agent_is_alive, ":ai_leader"),
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
#formations code
		  (call_script, "script_point_y_toward_position", pos63, pos60),
		  (agent_get_position, pos22, ":ai_leader"),
		  (agent_set_position, ":ai_leader", pos63),	#fake out script_cf_formation
		  (try_begin),
			(call_script, "script_cf_formation", ":team_no", grc_infantry, 0, formation_default),
		  (try_end),
		  (try_begin),
			(call_script, "script_cf_formation", ":team_no", grc_cavalry, 0, formation_wedge),
		  (try_end),
		  (try_begin),
			(call_script, "script_cf_formation", ":team_no", grc_archers, 2, formation_default),
		  (try_end),
		  (agent_set_position, ":ai_leader", pos22),
#end formations code
          (agent_get_position, pos1, ":ai_leader"),
          (try_begin),
            (lt, ":distance_to_enemy", 50),
            (ge, ":mission_time", 30),
            (assign, ":battle_tactic", 0),
			(call_script, "script_formation_end", ":team_no", grc_infantry),#formations code
			(call_script, "script_formation_end", ":team_no", grc_archers),	#formations code
			(call_script, "script_formation_end", ":team_no", grc_cavalry),	#formations code
            (team_give_order, ":team_no", grc_everyone, mordr_charge),
            (agent_set_speed_limit, ":ai_leader", 60),
          (try_end),
        (else_try),
          (assign, ":battle_tactic", 0),
		  (call_script, "script_formation_end", ":team_no", grc_infantry),	#formations code
		  (call_script, "script_formation_end", ":team_no", grc_archers),	#formations code
		  (call_script, "script_formation_end", ":team_no", grc_cavalry),	#formations code
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (try_end),
      
      (try_begin), # charge everyone after a while
        (neq, ":battle_tactic", 0),
        (ge, ":mission_time", 300),
        (assign, ":battle_tactic", 0),
	 	(call_script, "script_formation_end", ":team_no", grc_infantry),#formations code
		(call_script, "script_formation_end", ":team_no", grc_archers),	#formations code
		(call_script, "script_formation_end", ":team_no", grc_cavalry),	#formations code
        (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (team_get_leader, ":ai_leader", ":team_no"),
        (agent_set_speed_limit, ":ai_leader", 60),
      (try_end),
      (assign, reg0, ":battle_tactic"),
  ]),
  
  # Replacement script for battle_tactic_init_aux to switch between using
  # M&B Standard AI with changes for formations and original based on
  # NOTE: original script "battle_tactic_init_aux" should be renamed to "orig_battle_tactic_init_aux"
  # constant formation_native_ai_use_formation ( 0: original, 1: use formation )
  # script_battle_tactic_init_aux
  # Input: team_no, battle_tactic
  # Output: none
  ("battle_tactic_init_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
	  (try_begin),
		(eq, "$tld_option_formations", 1), (eq, "$small_scene_used", 0),
		(call_script, "script_formation_battle_tactic_init_aux", ":team_no", ":battle_tactic"),
	 ] + (is_a_wb_script==1 and [
	  (else_try),
	  		(eq, "$tld_option_formations", 2),
			(call_script, "script_formation_battle_tactic_init_aux_moto", ":team_no", ":battle_tactic"),
	 ] or []) + [
	  (else_try),
		(call_script, "script_orig_battle_tactic_init_aux", ":team_no", ":battle_tactic"),
	  (try_end),
    ]),

  # Replacement script for battle_tactic_init_aux to switch between using
  # M&B Standard AI with changes for formations and original based on
  # NOTE: original script "battle_tactic_apply_aux" should be renamed to "orig_battle_tactic_apply_aux"
  # constant formation_native_ai_use_formation ( 0: original, 1: use formation )
  # script_battle_tactic_apply_aux
  # Input: team_no, battle_tactic
  # Output: battle_tactic
  ("battle_tactic_apply_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
	  (try_begin),
		(eq, "$tld_option_formations", 1),(eq, "$small_scene_used", 0),
		(call_script, "script_formation_battle_tactic_apply_aux", ":team_no", ":battle_tactic"),

	  ] + (is_a_wb_script==1 and [
	  (else_try),
  		(eq, "$tld_option_formations", 2),
		(call_script, "script_formation_battle_tactic_apply_aux_moto", ":team_no", ":battle_tactic"),
	  ] or []) + [
	  (else_try),
		(call_script, "script_orig_battle_tactic_apply_aux", ":team_no", ":battle_tactic"),
	  (try_end),
  ]),

  # script_team_get_nontroll_leader
  # Input: team_no
  # Output: leader agent ID (-1 if failed)
  # This is a wrapper around team_get_leader, because team_set_leader doesn't work in MB, written to prevent trolls from being designated as leaders
  ("team_get_nontroll_leader",
    [
      (store_script_param, ":team_no", 1),
      (team_get_leader, ":team_leader", ":team_no"),
      (assign, ":new_leader", ":team_leader"),
      
      (try_begin),
      	#(neq, ":team_leader", -1), #Kham - fix for horse agent
        (agent_get_troop_id, ":troop_id", ":team_leader"),
        (troop_get_type, ":troop_type", ":troop_id"),
        (eq, ":troop_type", tf_troll), # is it a troll?
      
        #find a new leader: highest level
        (assign, ":max_level", 0),
        (assign, ":new_leader", -1),
        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member", ":team_no", grc_everyone, ":team_leader", ":agent"), #disregards trolls too
          (agent_get_troop_id, ":troop_id", ":agent"),
          (store_character_level, ":troop_level", ":troop_id"),
          (gt, ":troop_level", ":max_level"),
          (assign, ":max_level", ":troop_level"),
          (assign, ":new_leader", ":agent"),
        (try_end),
      (try_end),
      
      (assign, reg0, ":new_leader"),
  ]),



  # script_change_formation
  # Input: order_no, agent_no
  # Output: none
  # This script is for warband to change the formation based upon the command
  # that was issued from the player.
  ("change_formation", 
    [
      	(store_script_param, ":order_no", 1),
      	(store_script_param, ":agent_no", 2),
	(try_begin),
		(eq|this_or_next, ":order_no", mordr_dismount),
		(eq|this_or_next, ":order_no", mordr_charge),
		(eq|this_or_next, ":order_no", mordr_follow),
		(eq, ":order_no", mordr_hold),
		(assign, "$fclock", 1),
		(call_script, "script_player_order_formations", ":order_no"),
	(else_try),
		(eq|this_or_next, ":order_no", mordr_advance),
		(eq|this_or_next, ":order_no", mordr_fall_back),
		(eq|this_or_next, ":order_no", mordr_spread_out),
		(eq, ":order_no", mordr_stand_closer),
		(call_script, "script_player_order_formations", ":order_no"),
	(try_end),
    ]),
	

] + (is_a_wb_script==1 and [

# script_troop_default_division MOTO chief
# Input: troop_id, flag 0 for expanded divisions
# Output: reg0 default division
("troop_default_division", [(store_script_param, ":troop_no", 1),
  
  (assign, ":target_division", grc_infantry),
  (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
  
  (try_begin),
    (troop_is_guarantee_horse, ":troop_no"),
    (assign, ":has_horse", 0),
    (try_for_range, reg0, 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":troop_no", reg0),
      (gt, ":item", 0),
      (item_get_type, reg1, ":item"),
      (eq, reg1, itp_type_horse),
      (assign, ":has_horse", 1),
    (try_end),
    (neq, ":has_horse", 0),
    (assign, ":target_division", grc_cavalry),
    
  (else_try),
    (troop_is_guarantee_ranged, ":troop_no"),
    (assign, ":has_ranged", 0),
    (try_for_range, reg0, 0, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":troop_no", reg0),
      (call_script, "script_cf_is_weapon_ranged", ":item", 1),
      (item_get_type, reg1, ":item"),
      (assign, ":target_division", grc_archers),
      (assign, ":has_ranged", 1),
    (try_end),
    (neq, ":has_ranged", 0),
  (try_end),
  
  (assign, reg0, ":target_division"),]),

# script_cf_is_weapon_ranged by motomataru
  # Input: weapon ID, flag 0/1 to consider thrown weapons
  # Output: T/F
  ("cf_is_weapon_ranged", [(store_script_param, ":weapon", 1),
      (store_script_param, ":include_thrown", 2),
      
      (assign, ":test_val", 0),
      (try_begin),
        (ge, ":weapon", 0),
        (item_get_type, ":type", ":weapon"),
        (try_begin),
          (this_or_next | eq, ":type", 		itp_type_bow),
          (				  eq, ":type", itp_type_crossbow),
          (assign, ":test_val", 1),
        (else_try),
          (eq, ":type", itp_type_thrown),
          (neq, ":include_thrown", 0),
          (assign, ":test_val", 1),
        (try_end),
      (try_end),
      
      (neq, ":test_val", 0),]),


################## 
##################
######## FORM V5 #

# # AI with Formations Scripts
  # script_calculate_decision_numbers by motomataru
  # Input: AI team, size relative to battle in %
  # Output: reg0 - battle presence plus level bump, reg1 - level bump (team avg
  # level / 3)
  ("calculate_decision_numbers_moto", [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_presence", 2),
      (try_begin),
        (team_get_slot, reg0, ":team_no", slot_team_level),
        (store_div, reg1, reg0, 3),
        (store_add, reg0, ":battle_presence", reg1),	#decision w.r.t.  all enemy teams
      (try_end)]),
  
  
  # script_team_field_ranged_tactics_moto by motomataru
  # Input: AI team, size relative to largest team in %, size relative to battle
  # in %
  # Output: none
  ("team_field_ranged_tactics_moto", [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":rel_army_size", 2),
      (store_script_param, ":battle_presence", 3),
      (assign, ":division", grc_archers), #Pre-Many Divisions
      (assign, ":bg_pos", Archers_Pos_MOTO), #Pre-Many Divisions
      
      (try_begin),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_eq, ":team_no", ":slot", 0),
        (try_begin),	#undo reversion to BP_Jockey_MOTO (see below)
          (lt, "$battle_phase", BP_Fight_MOTO),
          (call_script, "script_cf_any_fighting_moto"),
          (call_script, "script_cf_count_casualties_moto"),
          (assign, "$battle_phase", BP_Fight_MOTO),
        (try_end),
        
      (else_try),
        (call_script, "script_battlegroup_get_position_moto", ":bg_pos", ":team_no", ":division"),
        (call_script, "script_team_get_position_of_enemies_moto", Enemy_Team_Pos_MOTO, ":team_no", grc_everyone),
        (call_script, "script_point_y_toward_position_moto", ":bg_pos", Enemy_Team_Pos_MOTO),
        
        (store_add, ":slot", slot_team_d0_closest_enemy_special_dist, ":division"),	#distance to nearest enemy infantry agent
        (team_get_slot, ":distance_to_enemy", ":team_no", ":slot"),
        (try_begin),
          (eq, ":distance_to_enemy", 0),
          (call_script, "script_get_nearest_enemy_battlegroup_location_moto", Nearest_Enemy_Battlegroup_Pos_MOTO, ":team_no", ":bg_pos"),
          (assign, ":distance_to_enemy", reg0),
        (try_end),
        
        (try_begin),	#avoid being provoked from defensive position
          (ge, "$battle_phase", BP_Fight_MOTO),
          (try_begin),
            (call_script, "script_cf_any_fighting_moto"),
          (else_try),
            (assign, "$battle_phase", BP_Jockey_MOTO),
            (assign, "$clock_reset", 0),
          (try_end),
        (try_end),
        
        (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
        (team_get_slot, ":is_firing", ":team_no", ":slot"),
        (store_add, ":slot", slot_team_d0_size, grc_infantry),
        (team_get_slot, ":num_infantry", ":team_no", ":slot"),
        
        (call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"),
        (assign, ":decision_index", reg0),
        (assign, ":level_bump", reg1),
        
        (try_begin),
          (gt, ":decision_index", 86),	#outpower enemies more than 6:1?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":team_no", ":division", mordr_charge),
          (try_end),
          
        (else_try),
          (lt, ":decision_index", 14),	#outpowered more than 6:1?
          (eq, ":num_infantry", 0),	#no infantry to delay enemy?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_retreat),
            (team_give_order, ":team_no", ":division", mordr_retreat),
          (try_end),
          
        (else_try),
          (ge, "$battle_phase", BP_Jockey_MOTO),
          (store_add, ":slot", slot_team_d0_low_ammo, ":division"),
          (team_slot_ge, ":team_no", ":slot", 1),	#running out of ammo?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":team_no", ":division", mordr_charge),
          (try_end),
          
        (else_try),
          (ge, "$battle_phase", BP_Fight_MOTO),
          (eq, ":is_firing", 0),
          (gt, ":decision_index", Advance_More_Point),
          (le, ":distance_to_enemy", AI_long_range),	#closer than reposition?
          (team_give_order, ":team_no", ":division", mordr_advance),
          
        #hold somewhere
        (else_try),
          (store_add, ":decision_index", ":rel_army_size", ":level_bump"),	#decision w.r.t. largest enemy team
          (assign, ":move_archers", 0),
          
          (init_position, Team_Starting_Point),
          (team_get_slot, reg0, ":team_no", slot_team_starting_x),
          (position_set_x, Team_Starting_Point, reg0),
          (team_get_slot, reg0, ":team_no", slot_team_starting_y),
          (position_set_y, Team_Starting_Point, reg0),
          (position_set_z_to_ground_level, Team_Starting_Point),
          
          (try_begin),
            (eq, "$battle_phase", BP_Setup_MOTO),
            (assign, ":move_archers", 1),
          (else_try),
            (ge, "$battle_phase", BP_Fight_MOTO),
            (try_begin),
              (neg | is_between, ":distance_to_enemy", AI_charge_distance, AI_long_range),
              (assign, ":move_archers", 1),
            (else_try),
              (lt, ":decision_index", Hold_Point),	#probably coming from a defensive position (see below)
              (eq, "$FormAI_AI_no_defense", 0),	#player hasn't set disallow defense option?
              (eq, ":is_firing", 0),	#probably because player team has retreated
              (assign, ":move_archers", 1),
            (try_end),
          (else_try),	#jockey phase
            (this_or_next | gt, "$FormAI_AI_no_defense", 0),	#player has set disallow defense option OR
            (ge, ":decision_index", Hold_Point),	#not starting in a defensive position (see below)
            (try_begin),
              (gt, ":distance_to_enemy", AI_long_range),	#enemy very far off
              (assign, ":move_archers", 1),
            (else_try),
              (call_script, "script_point_y_toward_position_moto", Team_Starting_Point, ":bg_pos"),
              (position_get_rotation_around_z, reg0, Team_Starting_Point),
              (position_get_rotation_around_z, reg1, ":bg_pos"),
              (val_sub, reg0, reg1),
              (this_or_next | is_between, reg0, -45, 45),	#only move if within "cone of advancement" to prevent constant adjusting at
              #border OR
              (eq, ":is_firing", 0),	#if not firing for some reason (hill in way?)
              
              (try_begin),
                (eq, ":num_infantry", 0),	#no infantry to wait for
                (assign, ":move_archers", 1),
              (else_try),
                (call_script, "script_battlegroup_get_position_moto", Infantry_Pos_MOTO, ":team_no", grc_infantry),
                (get_distance_between_positions, ":infantry_to_enemy", Infantry_Pos_MOTO, Enemy_Team_Pos_MOTO),
                (get_distance_between_positions, ":archers_to_enemy", ":bg_pos", Enemy_Team_Pos_MOTO),
                (val_sub, ":infantry_to_enemy", ":archers_to_enemy"),
                (le, ":infantry_to_enemy", 1500),	#don't outstrip infantry when closing
                (assign, ":move_archers", 1),
              (try_end),
            (try_end),
          (try_end),
          
          (try_begin),
            (gt, ":move_archers", 0),
            (try_begin),
              (lt, ":decision_index", Hold_Point),	#outnumbered?
              (eq, "$FormAI_AI_no_defense", 0),	#player hasn't set disallow defense option?
              (lt, "$battle_phase", BP_Fight_MOTO),
              (neq, ":team_no", 1),	#not attacker?
              (neq, ":team_no", 3),	#not ally of attacker?
              (store_div, ":distance_to_move", ":distance_to_enemy", 6),	#middle of rear third of battlefield
              (assign, ":hill_search_radius", ":distance_to_move"),
              
            (else_try),
              (try_begin),
                (ge, "$battle_phase", BP_Fight_MOTO),
                (copy_position, ":bg_pos", Team_Starting_Point),
                (call_script, "script_point_y_toward_position_moto", ":bg_pos", Enemy_Team_Pos_MOTO),
                (try_begin),
                  (gt, ":num_infantry", 0),
                  (store_add, ":slot", slot_team_d0_closest_enemy, grc_infantry),
                  (team_get_slot, ":enemy_agent_nearest_infantry", ":team_no", ":slot"),
                  (le, ":enemy_agent_nearest_infantry", 0),
                  (agent_get_team, ":target_team", ":enemy_agent_nearest_infantry"),
                  (agent_get_division, ":target_division", ":enemy_agent_nearest_infantry"),
                  (call_script, "script_battlegroup_get_position_moto", Nearest_Enemy_Battlegroup_Pos_MOTO, ":target_team", ":target_division"),
                  (get_distance_between_positions, ":distance_to_enemy", ":bg_pos", Nearest_Enemy_Battlegroup_Pos_MOTO),
                (else_try),
                  (call_script, "script_get_nearest_enemy_battlegroup_location_moto", Nearest_Enemy_Battlegroup_Pos_MOTO, ":team_no", ":bg_pos"),
                  (assign, ":distance_to_enemy", reg0),
                (try_end),
              (try_end),
              
              (try_begin),
                (eq, "$battle_phase", BP_Setup_MOTO),
                (assign, ":shot_distance", AI_long_range),
              (else_try),
                (assign, ":shot_distance", AI_firing_distance),
                (store_sub, reg1, AI_firing_distance, AI_charge_distance),
                (val_sub, reg1, 200),	#subtract two meters to prevent automatically provoking melee from forward
                #enemy infantry
                (store_add, ":slot", slot_team_d0_percent_throwers, ":division"),
                (team_get_slot, reg0, ":team_no", ":slot"),
                (val_mul, reg1, reg0),
                (val_div, reg1, 100),
                (val_sub, ":shot_distance", reg1),
              (try_end),
              
              (store_sub, ":distance_to_move", ":distance_to_enemy", ":shot_distance"),
              (store_div, ":hill_search_radius", ":shot_distance", 3),	#limit so as not to run into enemy
              (try_begin),
                (lt, "$battle_phase", BP_Fight_MOTO),
                (try_begin),
                  (this_or_next | eq, "$battle_phase", BP_Setup_MOTO),
                  (lt, ":battle_presence", Advance_More_Point),	#expect to meet halfway?
                  (val_div, ":distance_to_move", 2),
                (try_end),
              (try_end),
            (try_end),
            
            (position_move_y, ":bg_pos", ":distance_to_move", 0),
            (try_begin),
              (lt, "$battle_phase", BP_Fight_MOTO),
              (copy_position, pos1, ":bg_pos"),
              (store_div, reg0, ":hill_search_radius", 100),
              (call_script, "script_find_high_ground_around_pos1_corrected_moto", ":bg_pos", reg0),
            (try_end),
          (try_end),
          
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_hold),
            (team_give_order, ":team_no", ":division", mordr_hold),
          (try_end),
          (call_script, "script_set_formation_destination_moto", ":team_no", ":division", ":bg_pos"),
        (try_end),
      (try_end)]),
  
  
  # script_team_field_melee_tactics_moto by motomataru #EDITED FOR SLOTS BY
  # CABA...many divisions changes necessary
  # Input: AI team, size relative to largest team in %, size relative to battle
  # in %
  # Output: none
  ("team_field_melee_tactics_moto", [
      (store_script_param, ":team_no", 1),
      #	(store_script_param, ":rel_army_size", 2),
      (store_script_param, ":battle_presence", 3),
      (call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"),
      
      #mop up if outnumber enemies more than 6:1
      (try_begin),
        (gt, reg0, 86),
        (try_for_range, ":division", 0, 9),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_slot_ge, ":team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (neg | team_slot_eq, ":team_no", ":slot", sdt_archer),
          (neg | team_slot_eq, ":team_no", ":slot", sdt_skirmisher),
          (call_script, "script_formation_end_moto", ":team_no", ":division"),
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":team_no", ":division", mordr_charge),
          (try_end),
        (try_end),
        
      (else_try),
        (assign, ":num_enemies", 0),
        (try_for_range, ":enemy_team_no", 0, 4),
          (teams_are_enemies, ":enemy_team_no", ":team_no"),
          (team_get_slot, ":value", ":enemy_team_no", slot_team_size),
          (val_add, ":num_enemies", ":value"),
        (try_end),
        
        (gt, ":num_enemies", 0),
        (call_script, "script_team_get_position_of_enemies_moto", Enemy_Team_Pos_MOTO, ":team_no", grc_everyone),
        
        (store_add, ":slot", slot_team_d0_size, grc_archers),
        (team_get_slot, ":num_archers", ":team_no", ":slot"),
        (try_begin),
          (eq, ":num_archers", 0),
          (assign, ":enemy_bg_nearest_archers_dist", Far_Away),
          (assign, ":archer_order", mordr_charge),
        (else_try),
          (call_script, "script_battlegroup_get_position_moto", Archers_Pos_MOTO, ":team_no", grc_archers),
          (call_script, "script_point_y_toward_position_moto", Archers_Pos_MOTO, Enemy_Team_Pos_MOTO),
          (call_script, "script_get_nearest_enemy_battlegroup_location_moto", pos0, ":team_no", Archers_Pos_MOTO),
          (assign, ":enemy_bg_nearest_archers_dist", reg0),
          (team_get_movement_order, ":archer_order", ":team_no", grc_archers),
        (try_end),
        
        (store_add, ":slot", slot_team_d0_size, grc_infantry),
        (team_get_slot, ":num_infantry", ":team_no", ":slot"),
        (try_begin),
          (eq, ":num_infantry", 0),
          (assign, ":enemy_bg_nearest_infantry_dist", Far_Away),
          (assign, ":enemy_agent_nearest_infantry_dist", Far_Away),
        (else_try),
          (call_script, "script_battlegroup_get_position_moto", Infantry_Pos_MOTO, ":team_no", grc_infantry),
          (call_script, "script_get_nearest_enemy_battlegroup_location_moto", pos0, ":team_no", Infantry_Pos_MOTO),
          (assign, ":enemy_bg_nearest_infantry_dist", reg0),
          (store_add, ":slot", slot_team_d0_closest_enemy_dist, grc_infantry),
          (team_get_slot, ":enemy_agent_nearest_infantry_dist", ":team_no", ":slot"),
          (eq, ":enemy_agent_nearest_infantry_dist", 0),	#happens when player turns off closest agent mechanism (see mod options)
          (assign, ":enemy_agent_nearest_infantry_dist", ":enemy_bg_nearest_infantry_dist"),
        (try_end),
        
        (store_add, ":slot", slot_team_d0_size, grc_cavalry),
        (team_get_slot, ":num_cavalry", ":team_no", ":slot"),
        (try_begin),
          (eq, ":num_cavalry", 0),
          (assign, ":enemy_bg_nearest_cavalry_dist", Far_Away),
          (assign, ":enemy_agent_nearest_cavalry_dist", Far_Away),
        (else_try),
          (call_script, "script_battlegroup_get_position_moto", Cavalry_Pos_MOTO, ":team_no", grc_cavalry),
          (call_script, "script_get_nearest_enemy_battlegroup_location_moto", pos0, ":team_no", Cavalry_Pos_MOTO),
          (assign, ":enemy_bg_nearest_cavalry_dist", reg0),
          (store_add, ":slot", slot_team_d0_closest_enemy_dist, grc_cavalry),
          (team_get_slot, ":enemy_agent_nearest_cavalry_dist", ":team_no", ":slot"),
          (eq, ":enemy_agent_nearest_cavalry_dist", 0),	#happens when player turns off closest agent mechanism (see mod options)
          (assign, ":enemy_agent_nearest_cavalry_dist", ":enemy_bg_nearest_infantry_dist"),
        (try_end),
        
        (try_begin),
          (lt, "$battle_phase", BP_Fight_MOTO),
          (this_or_next | le, ":enemy_bg_nearest_infantry_dist", AI_charge_distance),
          (this_or_next | le, ":enemy_bg_nearest_cavalry_dist", AI_charge_distance),
          (le, ":enemy_bg_nearest_archers_dist", AI_charge_distance),
          (assign, "$battle_phase", BP_Fight_MOTO),
        (else_try),
          (lt, "$battle_phase", BP_Jockey_MOTO),
          (this_or_next | le, ":enemy_agent_nearest_infantry_dist", AI_long_range),
          (le, ":enemy_agent_nearest_cavalry_dist", AI_long_range),
          (assign, "$battle_phase", BP_Jockey_MOTO),
        (try_end),
        
        #(team_get_leader, ":team_leader", ":team_no"),
        (call_script, "script_team_get_nontroll_leader", ":team_no"),
        (assign, ":team_leader", reg0),
        (gt, ":team_leader", 0),
        (assign, ":place_leader_by_infantry", 0),
        
        #infantry AI
        (store_add, ":slot", slot_team_d0_closest_enemy, grc_infantry),
        (team_get_slot, ":enemy_agent_nearest_infantry", ":team_no", ":slot"),
        (try_begin),
          (this_or_next | le, ":num_infantry", 0),
          (le, ":enemy_agent_nearest_infantry", 0),
          (assign, ":infantry_order", ":archer_order"),
          
          #deal with mounted heroes that team_give_order() treats as infantry
          ##CABA...could change their division?
          (team_get_movement_order, reg0, ":team_no", grc_infantry),
          (try_begin),
            (neq, reg0, ":infantry_order"),
            (team_give_order, ":team_no", grc_infantry, ":infantry_order"),
          (try_end),
          (try_begin),
            (gt, ":num_archers", 0),
            (copy_position, pos1, Archers_Pos_MOTO),
            (position_move_y, pos1, 1000, 0),
            (call_script, "script_set_formation_destination_moto", ":team_no", grc_infantry, pos1),
          (else_try),
            (call_script, "script_set_formation_destination_moto", ":team_no", grc_infantry, Cavalry_Pos_MOTO),
          (try_end),
          
        (else_try),
          (agent_get_position, Nearest_Enemy_Troop_Pos_MOTO, ":enemy_agent_nearest_infantry"),
          (agent_get_team, ":enemy_agent_nearest_infantry_team", ":enemy_agent_nearest_infantry"),
          (agent_get_division, ":enemy_agent_nearest_infantry_div", ":enemy_agent_nearest_infantry"),
          
          (assign, ":sum_level_enemy_infantry", 0),
          (try_for_range, ":enemy_team_no", 0, 4),
            (teams_are_enemies, ":enemy_team_no", ":team_no"),
            (try_for_range, ":enemy_division", 0, 9),
              (store_add, ":slot", slot_team_d0_type, ":enemy_division"),
              (team_get_slot, ":value", ":enemy_team_no", ":slot"),
              (this_or_next | eq, ":value", sdt_polearm),
              (eq, ":value", sdt_infantry),
              (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
              (team_get_slot, ":value", ":enemy_team_no", ":slot"),
              (store_add, ":slot", slot_team_d0_level, ":enemy_division"),
              (team_get_slot, reg0, ":enemy_team_no", ":slot"),
              (val_mul, ":value", reg0),
              (val_add, ":sum_level_enemy_infantry", ":value"),
            (try_end),
          (try_end),
          
          (store_mul, ":percent_level_enemy_infantry", ":sum_level_enemy_infantry", 100),
          (val_div, ":percent_level_enemy_infantry", ":num_enemies"),
          (try_begin),
            (teams_are_enemies, ":team_no", "$fplayer_team_no"),
            (assign, ":combined_level", 0),
            (assign, ":combined_team_size", 0),
            (assign, ":combined_num_infantry", ":num_infantry"),
          (else_try),
            (store_add, ":slot", slot_team_d0_level, grc_infantry),
            (team_get_slot, ":combined_level", "$fplayer_team_no", ":slot"),
            (team_get_slot, ":combined_team_size", "$fplayer_team_no", slot_team_size),
            (store_add, ":slot", slot_team_d0_size, grc_infantry),
            (team_get_slot, ":combined_num_infantry", "$fplayer_team_no", ":slot"),
            (val_add, ":combined_num_infantry", ":num_infantry"),
          (try_end),
          (store_mul, ":percent_level_infantry", ":combined_num_infantry", 100),
          (store_add, ":slot", slot_team_d0_level, grc_infantry),
          (team_get_slot, ":level_infantry", ":team_no", ":slot"),
          (val_add, ":combined_level", ":level_infantry"),
          (val_mul, ":percent_level_infantry", ":combined_level"),
          (team_get_slot, reg0, ":team_no", slot_team_size),
          (val_add, ":combined_team_size", reg0),
          (val_div, ":percent_level_infantry", ":combined_team_size"),
          
          (assign, ":infantry_order", mordr_charge),
          (try_begin),	#enemy far away AND ranged not charging
            (gt, ":enemy_bg_nearest_archers_dist", AI_charge_distance),
            (gt, ":enemy_agent_nearest_infantry_dist", AI_charge_distance),
            (neq, ":archer_order", mordr_charge),
            (try_begin),	#fighting not started OR not enough infantry
              (this_or_next | le, "$battle_phase", BP_Jockey_MOTO),
              (lt, ":percent_level_infantry", ":percent_level_enemy_infantry"),
              (assign, ":infantry_order", mordr_hold),
            (try_end),
          (try_end),
          
          # bum rush enemy archers?
          (try_begin),
            # (le, ":level_infantry", AI_Poor_Troop_Level), unfortunately leaves them
            # susceptible to rings of archers
            (store_add, ":slot", slot_team_d0_type, ":enemy_agent_nearest_infantry_div"),
            (this_or_next | team_slot_eq, ":enemy_agent_nearest_infantry_team", ":enemy_agent_nearest_infantry_div", sdt_archer),
            (team_slot_eq, ":enemy_agent_nearest_infantry_team", ":enemy_agent_nearest_infantry_div", sdt_skirmisher),
            (get_distance_between_positions, reg0, Infantry_Pos_MOTO, Nearest_Enemy_Troop_Pos_MOTO),
            (le, reg0, AI_charge_distance),
            (call_script, "script_formation_end_moto", ":team_no", grc_infantry),
            (team_get_movement_order, reg0, ":team_no", grc_infantry),
            (try_begin),
              (neq, reg0, mordr_charge),
              (team_give_order, ":team_no", grc_infantry, mordr_charge),
            (try_end),
            
          #else attempt to make formation somewhere
          (else_try),
            (store_add, ":slot", slot_team_d0_formation, grc_infantry),
            (team_get_slot, ":infantry_formation", ":team_no", ":slot"),
            #(team_get_leader, ":enemy_leader", ":enemy_agent_nearest_infantry_team"),
             (call_script, "script_team_get_nontroll_leader", ":enemy_agent_nearest_infantry_team"),
             (assign, ":enemy_leader", reg0),
             (gt, ":team_leader", 0),
            
            #consider new formation
            (try_begin),
              (store_add, ":slot", slot_team_d0_is_fighting, grc_infantry),
              (this_or_next | le, ":infantry_formation", formation_none),
              (this_or_next | eq, ":infantry_formation", formation_default),
              (team_slot_eq, ":team_no", ":slot", 0),
              
              (call_script, "script_get_default_formation_moto", ":team_no"),
              (assign, ":infantry_formation", reg0),
              (agent_get_class, ":enemy_nearest_troop_class", ":enemy_agent_nearest_infantry"),
              
              (assign, ":num_enemy_cavalry", 0),
              (try_for_range, ":enemy_team_no", 0, 4),
                (teams_are_enemies, ":enemy_team_no", ":team_no"),
                (team_get_slot, ":value", ":enemy_team_no", slot_team_num_cavalry),
                (val_add, ":num_enemy_cavalry", ":value"),
              (try_end),
              
              (store_mul, ":percent_enemy_cavalry", ":num_enemy_cavalry", 100),
              (val_div, ":percent_enemy_cavalry", ":num_enemies"),
              (try_begin),
                (gt, ":infantry_formation", formation_none),
                (try_begin),
                  (gt, ":percent_enemy_cavalry", 66),
                  (assign, ":infantry_formation", formation_square),
                (else_try),
                  (neq, ":enemy_nearest_troop_class", grc_cavalry),
                  (neq, ":enemy_nearest_troop_class", grc_archers),
                  (neq, ":enemy_agent_nearest_infantry", ":enemy_leader"),
                  (ge, ":num_infantry", 21),
                  (store_add, ":slot", slot_team_d0_size, ":enemy_agent_nearest_infantry_div"),
                  (team_get_slot, reg0, ":enemy_agent_nearest_infantry_team", ":slot"),
                  (gt, reg0, ":num_infantry"),	#got fewer troops?
                  (store_add, ":slot", slot_team_d0_armor, grc_infantry),
                  (team_get_slot, ":average_armor", ":team_no", ":slot"),
                  (store_add, ":slot", slot_team_d0_armor, ":enemy_agent_nearest_infantry_div"),
                  (team_get_slot, reg0, ":enemy_agent_nearest_infantry_team", ":slot"),
                  (gt, ":average_armor", reg0),	#got better armor?
                  (assign, ":infantry_formation", formation_wedge),
                (try_end),
              (try_end),
            (try_end),	#consider new formation
            
            (try_begin),
              (call_script, "script_cf_battlegroup_valid_formation_moto", ":team_no", grc_infantry, ":infantry_formation"),
              (store_add, ":slot", slot_team_d0_formation, grc_infantry),
              (team_set_slot, ":team_no", ":slot", ":infantry_formation"),
              
              #adjust spacing for long swung weapons
              (store_add, ":slot", slot_team_d0_swung_weapon_length, grc_infantry),
              (team_get_slot, ":spacing", ":team_no", ":slot"),
              (val_add, ":spacing", 25),	#rounding for 50cm
              (val_div, ":spacing", 50),
              (store_add, ":slot", slot_team_d0_formation_space, grc_infantry),
              (team_set_slot, ":team_no", ":slot", ":spacing"),
              
              (assign, ":place_leader_by_infantry", 1),
              
            (else_try),
              (call_script, "script_formation_end_moto", ":team_no", grc_infantry),
              (team_get_movement_order, reg0, ":team_no", grc_infantry),
              (try_begin),
                (neq, reg0, ":infantry_order"),
                (team_give_order, ":team_no", grc_infantry, ":infantry_order"),
              (try_end),
              (eq, ":infantry_order", mordr_hold),
              (assign, ":place_leader_by_infantry", 1),
            (try_end),
            
            #hold near archers?
            (try_begin),
              (eq, ":infantry_order", mordr_hold),
              (gt, ":num_archers", 0),
              # (copy_position, pos1, Archers_Pos_MOTO),
              (team_get_order_position, pos1, ":team_no", grc_archers),	#anticipate archers
              (position_move_x, pos1, -100, 0),
              (try_begin),
                (this_or_next | eq, ":enemy_agent_nearest_infantry_div", grc_cavalry),
                (gt, ":percent_level_infantry", ":percent_level_enemy_infantry"),
                (call_script, "script_battlegroup_dist_center_to_front_moto", ":team_no", grc_infantry),	#make sure to clear archers
                (store_mul, ":distance_to_move", reg0, 2),
                (val_add, ":distance_to_move", 1000),
                (position_move_y, pos1, ":distance_to_move", 0),	#move ahead of archers in anticipation of charges
              (else_try),
                (position_move_y, pos1, -1000, 0),
              (try_end),
              
            #obtain destination
            (else_try),
              (assign, ":target_division", -1),
              (try_begin),
                (store_add, ":slot", slot_team_d0_is_fighting, grc_infantry),
                (team_slot_eq, ":team_no", ":slot", 0),	#not engaged?
                (gt, ":enemy_bg_nearest_archers_dist", AI_charge_distance),	#don't have to protect archers?
                # (lt, ":percent_enemy_cavalry", 100), #non-cavalry exist?  MOTO next
                # command tests
                
                #prefer non-cavalry target (that infantry can catch)
                (store_add, ":slot", slot_team_d0_closest_enemy_special_dist, grc_infantry),
                (team_get_slot, ":distance_to_enemy_troop", ":team_no", ":slot"),
                (gt, ":distance_to_enemy_troop", 0),
                (store_add, ":slot", slot_team_d0_closest_enemy_special, grc_infantry),
                (team_get_slot, ":enemy_nearest_non_cav_agent", ":team_no", ":slot"),
                (gt, ":enemy_nearest_non_cav_agent", 0),
                (agent_get_position, pos60, ":enemy_nearest_non_cav_agent"),
                (agent_get_team, ":enemy_non_cav_team", ":enemy_nearest_non_cav_agent"),
                #(team_get_leader, reg0, ":enemy_non_cav_team"),
                (call_script, "script_team_get_nontroll_leader", ":enemy_agent_nearest_infantry_team"),
                (gt, reg0, 0),
                (try_begin),
                  (eq, ":enemy_nearest_non_cav_agent", reg0),	#team leader?
                  (assign, ":distance_to_enemy_group", Far_Away),
                (else_try),
                  (agent_get_division, ":target_division", ":enemy_nearest_non_cav_agent"),
                  (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":enemy_non_cav_team"),
                  (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":target_division"),
                  (call_script, "script_battlegroup_get_attack_destination_moto", pos1, ":team_no", grc_infantry, ":enemy_non_cav_team", ":target_division"),
                  (call_script, "script_get_distance_to_battlegroup_moto", ":enemy_non_cav_team", ":target_division", Infantry_Pos_MOTO),
                  (assign, ":distance_to_enemy_group", reg0),
                (try_end),
                
              #chase nearest target
              (else_try),
                (assign, ":distance_to_enemy_troop", ":enemy_agent_nearest_infantry_dist"),
                (copy_position, pos60, Nearest_Enemy_Troop_Pos_MOTO),
                (try_begin),
                  (eq, ":enemy_agent_nearest_infantry", ":enemy_leader"),
                  (assign, ":distance_to_enemy_group", Far_Away),
                (else_try),
                  (assign, ":target_division", ":enemy_agent_nearest_infantry_div"),
                  (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":enemy_agent_nearest_infantry_team"),
                  (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":target_division"),
                  (call_script, "script_battlegroup_get_attack_destination_moto", pos1, ":team_no", grc_infantry, ":enemy_agent_nearest_infantry_team", ":target_division"),
                  (call_script, "script_get_distance_to_battlegroup_moto", ":enemy_agent_nearest_infantry_team", ":target_division", Infantry_Pos_MOTO),
                  (assign, ":distance_to_enemy_group", reg0),
                (try_end),
              (try_end),
              
              #reassemble if too scattered
              (try_begin),
                (call_script, "script_get_distance_to_battlegroup_moto", ":team_no", grc_infantry, pos60),	#we're using enemy troop as a reference
                (val_sub, reg0, ":distance_to_enemy_troop"),
                (gt, reg0, 1500),	#division center too far from where it should be (probably because of
                #reinforcing troops)
                (position_copy_origin, pos1, Infantry_Pos_MOTO),	#gather at average position
                (call_script, "script_battlegroup_dist_center_to_front_moto", ":team_no", grc_infantry),
                (assign, ":distance_to_move", reg0),
                (store_mul, reg0, 350, formation_reform_interval),
                (val_add, ":distance_to_move", reg0),	#one interval movement
                (position_move_y, pos1, ":distance_to_move"),	#keep rear moving forward
                
              #attack leader if is closest troop
              (else_try),
                (eq, ":target_division", -1),
                (position_copy_origin, pos1, pos60),
                (call_script, "script_point_y_toward_position_moto", Infantry_Pos_MOTO, pos1),
                (position_copy_rotation, pos1, Infantry_Pos_MOTO),
                
              #move no farther than nearest troop if its unit is far off
              (else_try),
                (call_script, "script_battlegroup_dist_center_to_front_moto", ":team_no", grc_infantry),
                (val_add, ":distance_to_enemy_troop", reg0),	#distance to center of bg from nearest edge
                (store_sub, reg0, ":distance_to_enemy_group", ":distance_to_enemy_troop"),
                (gt, reg0, AI_charge_distance),
                (position_copy_origin, pos1, Infantry_Pos_MOTO),
                (position_move_y, pos1, ":distance_to_enemy_troop"),
                
              #shift dead player troops right to clear allies when both attacking the
              #same enemy battlegroup
              (else_try),
                (eq, ":team_no", "$fplayer_team_no"),
                (store_add, ":ally_team", "$fplayer_team_no", 2),
                (neg | teams_are_enemies, ":ally_team", "$fplayer_team_no"),
                (store_add, ":slot", slot_team_d0_size, grc_infantry),
                (team_slot_ge, ":ally_team", ":slot", 1),
                (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                (team_get_slot, ":target_team", "$fplayer_team_no", ":slot"),
                (team_slot_eq, ":ally_team", ":slot", ":target_team"),
                (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                (team_slot_eq, ":ally_team", ":slot", ":target_division"),
                (call_script, "script_battlegroup_get_position_moto", pos0, ":ally_team", grc_infantry),
                (get_distance_between_positions, ":distance_to_ally", Infantry_Pos_MOTO, pos0),
                (lt, ":distance_to_ally", ":distance_to_enemy_group"),	#shift only when not in melee to avoid rotation
                (call_script, "script_battlegroup_get_action_radius_moto", ":ally_team", grc_infantry),	#move larger group less to maintain center
                (val_div, reg0, 2),	#function returns length of bg
                (position_move_x, pos1, reg0),
                
              #shift allies left to clear dead player troops when both attacking the
              #same enemy battlegroup
              (else_try),
                (main_hero_fallen),
                (eq, AI_Replace_Dead_Player, 1),
                (neq, ":team_no", "$fplayer_team_no"),
                (neg | teams_are_enemies, ":team_no", "$fplayer_team_no"),
                (store_add, ":slot", slot_team_d0_size, grc_infantry),
                (team_slot_ge, "$fplayer_team_no", ":slot", 1),
                (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                (team_get_slot, ":target_team", "$fplayer_team_no", ":slot"),
                (team_slot_eq, ":team_no", ":slot", ":target_team"),
                (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                (team_slot_eq, "$fplayer_team_no", ":slot", ":target_division"),
                (call_script, "script_battlegroup_get_position_moto", pos0, "$fplayer_team_no", grc_infantry),
                (get_distance_between_positions, ":distance_to_ally", Infantry_Pos_MOTO, pos0),
                (lt, ":distance_to_ally", ":distance_to_enemy_group"),	#shift only when not in melee to avoid rotation
                (call_script, "script_battlegroup_get_action_radius_moto", "$fplayer_team_no", grc_infantry),	#move larger group less to maintain center
                (val_div, reg0, -2),	#function returns length of bg
                (position_move_x, pos1, reg0),
              (try_end),
            (try_end),	#obtain destination
            
            (call_script, "script_set_formation_destination_moto", ":team_no", grc_infantry, pos1),
            
            (try_begin),
              (store_add, ":slot", slot_team_d0_formation, grc_infantry),
              (neg | team_slot_eq, ":team_no", ":slot", formation_none),
              (team_slot_ge, ":team_no", ":slot", formation_none),
              (call_script, "script_get_centering_amount_moto", ":infantry_formation", ":num_infantry", ":spacing"),
              (position_move_x, pos1, reg0),
              (call_script, "script_form_infantry_moto", ":team_no", grc_infantry, ":team_leader", ":spacing", 0, ":infantry_formation"),
            (try_end),
          (try_end),	#attempt to make formation somewhere
        (try_end),
        
        #cavalry AI
        (try_begin),
          (gt, ":num_cavalry", 0),
          
          #get distance to nearest enemy battlegroup(s)
          (store_add, ":slot", slot_team_d0_armor, grc_cavalry),
          (team_get_slot, ":average_armor", ":team_no", ":slot"),
          (assign, ":nearest_threat_distance", Far_Away),
          (assign, ":nearest_target_distance", Far_Away),
          (assign, ":num_targets", 0),
          (try_for_range, ":enemy_team_no", 0, 4),
            (team_slot_ge, ":enemy_team_no", slot_team_size, 1),
            (teams_are_enemies, ":enemy_team_no", ":team_no"),
            (try_for_range, ":enemy_division", 0, 9),
              (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
              (team_get_slot, ":size_enemy_battle_group", ":enemy_team_no", ":slot"),
              (gt, ":size_enemy_battle_group", 0),
              (call_script, "script_battlegroup_get_position_moto", pos0, ":enemy_team_no", ":enemy_division"),
              (get_distance_between_positions, ":distance_of_enemy", Cavalry_Pos_MOTO, pos0),
              (try_begin),	#threat or target?
                (store_add, ":slot", slot_team_d0_weapon_length, ":enemy_division"),
                (team_get_slot, reg0, ":enemy_team_no", ":slot"),
                (assign, ":decision_index", reg0),
                (store_add, ":slot", slot_team_d0_armor, ":enemy_division"),
                (team_get_slot, reg0, ":enemy_team_no", ":slot"),
                (val_mul, ":decision_index", reg0),
                (val_mul, ":decision_index", ":size_enemy_battle_group"),
                (val_div, ":decision_index", ":average_armor"),
                (val_div, ":decision_index", ":num_cavalry"),
                (try_begin),
                  (neq, ":enemy_division", grc_cavalry),
                  (val_div, ":decision_index", 2),	#double count cavalry vs.  foot soldiers
                (try_end),
                (gt, ":decision_index", 100),
                (try_begin),
                  (gt, ":nearest_threat_distance", ":distance_of_enemy"),
                  (copy_position, Nearest_Threat_Pos_MOTO, pos0),
                  (assign, ":nearest_threat_distance", ":distance_of_enemy"),
                (try_end),
              (else_try),
                (val_add, ":num_targets", 1),
                (gt, ":nearest_target_distance", ":distance_of_enemy"),
                (copy_position, Nearest_Target_Pos, pos0),
                (assign, ":nearest_target_distance", ":distance_of_enemy"),
                (store_add, ":slot", slot_team_d0_target_team, grc_cavalry),
                (team_set_slot, ":team_no", ":slot", ":enemy_team_no"),
                (store_add, ":slot", slot_team_d0_target_division, grc_cavalry),
                (team_set_slot, ":team_no", ":slot", ":enemy_division"),
              (try_end),
            (try_end),
          (try_end),
          (try_begin),
            (eq, ":nearest_threat_distance", Far_Away),
            (assign, ":nearest_target_guarded", 0),
          (else_try),
            (eq, ":nearest_target_distance", Far_Away),
            (assign, ":nearest_target_guarded", 1),
          (else_try),
            (get_distance_between_positions, reg0, Nearest_Target_Pos, Nearest_Threat_Pos_MOTO),
            (store_div, reg1, AI_charge_distance, 2),
            (try_begin),	#ignore target too close to threat
              (le, reg0, reg1),
              (assign, ":nearest_target_guarded", 1),
            (else_try),
              (assign, ":nearest_target_guarded", 0),
            (try_end),
          (try_end),
          
          (assign, ":cavalry_order", mordr_charge), ##CABA HERE
          (try_begin),
            (teams_are_enemies, ":team_no", 0),
            (neg | team_slot_ge, 1, slot_team_reinforcement_stage, AI_Max_Reinforcements),
            (neg | team_slot_eq, 1, slot_team_reinforcement_stage, "$attacker_reinforcement_stage"),
            (assign, ":cavalry_order", mordr_hold),
          (else_try),
            (teams_are_enemies, ":team_no", 1),
            (neg | team_slot_ge, 0, slot_team_reinforcement_stage, AI_Max_Reinforcements),
            (neg | team_slot_eq, 0, slot_team_reinforcement_stage, "$defender_reinforcement_stage"),
            (assign, ":cavalry_order", mordr_hold),
          (else_try),
            (neq, ":infantry_order", mordr_charge),
            (try_begin),
              (le, "$battle_phase", BP_Jockey_MOTO),
              (assign, ":cavalry_order", mordr_hold),
            (else_try),
              (eq, ":nearest_target_distance", Far_Away),
              (try_begin),
                (eq, ":num_archers", 0),
                (assign, ":distance_to_archers", 0),
              (else_try),
                (get_distance_between_positions, ":distance_to_archers", Cavalry_Pos_MOTO, Archers_Pos_MOTO),
              (try_end),
              (try_begin),
                (this_or_next | gt, ":enemy_agent_nearest_cavalry_dist", AI_charge_distance),
                (gt, ":distance_to_archers", AI_charge_distance),
                (assign, ":cavalry_order", mordr_hold),
              (try_end),
            (try_end),
          (try_end),
          
          (try_begin),
            (eq, ":team_no", 0),
            (assign, ":cav_destination", Team0_Cavalry_Destination),
          (else_try),
            (eq, ":team_no", 1),
            (assign, ":cav_destination", Team1_Cavalry_Destination),
          (else_try),
            (eq, ":team_no", 2),
            (assign, ":cav_destination", Team2_Cavalry_Destination),
          (else_try),
            (eq, ":team_no", 3),
            (assign, ":cav_destination", Team3_Cavalry_Destination),
          (try_end),
          (store_add, ":slot", slot_team_d0_percent_ranged, grc_cavalry),
          (team_get_slot, reg0, ":team_no", ":slot"),
          
          #horse archers don't use wedge
          (try_begin),
            (ge, reg0, 50),
            (call_script, "script_formation_end_moto", ":team_no", grc_cavalry),
            (try_begin),
              (eq, ":num_archers", 0),
              (team_get_movement_order, reg0, ":team_no", grc_cavalry),
              (try_begin),
                (neq, reg0, mordr_charge),
                (team_give_order, ":team_no", grc_cavalry, mordr_charge),
              (try_end),
            (else_try),
              (team_get_movement_order, reg0, ":team_no", grc_cavalry),
              (try_begin),
                (neq, reg0, ":cavalry_order"),
                (team_give_order, ":team_no", grc_cavalry, ":cavalry_order"),
              (try_end),
              (copy_position, ":cav_destination", Archers_Pos_MOTO),
              (position_move_y, ":cav_destination", -500, 0),
              (call_script, "script_set_formation_destination_moto", ":team_no", grc_cavalry, ":cav_destination"),
            (try_end),
            
          #close in with no unguarded target farther off, free fight
          (else_try),
            (eq, ":cavalry_order", mordr_charge),
            (this_or_next | eq, ":num_archers", 0),
            (le, ":enemy_agent_nearest_cavalry_dist", AI_charge_distance),
            (try_begin),
              (eq, ":num_targets", 1),
              (eq, ":nearest_target_guarded", 0),
              (gt, ":nearest_target_distance", ":nearest_threat_distance"),
              (assign, reg0, 0),
            (else_try),
              (ge, ":num_targets", 2),
              (eq, ":nearest_target_guarded", 1),
              (assign, reg0, 0),
            (else_try),
              (assign, reg0, 1),
            (try_end),
            (eq, reg0, 1),
            (call_script, "script_formation_end_moto", ":team_no", grc_cavalry),
            (team_get_movement_order, reg0, ":team_no", grc_cavalry),
            (try_begin),
              (neq, reg0, mordr_charge),
              (team_give_order, ":team_no", grc_cavalry, mordr_charge),
            (try_end),
            
          #grand charge if target closer than threat AND not guarded
          (else_try),
            (lt, ":nearest_target_distance", ":nearest_threat_distance"),
            (eq, ":nearest_target_guarded", 0),
            (call_script, "script_formation_end_moto", ":team_no", grc_cavalry),
            (team_get_movement_order, reg0, ":team_no", grc_cavalry),
            (try_begin),
              (neq, reg0, mordr_hold),
              (team_give_order, ":team_no", grc_cavalry, mordr_hold),
            (try_end),
            
            #lead archers up to firing point
            (try_begin),
              (gt, ":nearest_target_distance", AI_firing_distance),
              (eq, ":cavalry_order", mordr_hold),
              (try_begin),
                (eq, ":num_archers", 0),
                (copy_position, ":cav_destination", Cavalry_Pos_MOTO),	#must be reinforcements, so gather at average position
              (else_try),
                (copy_position, ":cav_destination", Archers_Pos_MOTO),
                (position_move_y, ":cav_destination", AI_charge_distance, 0),
              (try_end),
              
            #then CHARRRRGE!
            (else_try),
              (copy_position, ":cav_destination", Cavalry_Pos_MOTO),
              (call_script, "script_point_y_toward_position_moto", ":cav_destination", Nearest_Target_Pos),
              (position_move_y, ":cav_destination", ":nearest_target_distance", 0),
            (try_end),
            (call_script, "script_set_formation_destination_moto", ":team_no", grc_cavalry, ":cav_destination"),
            
          #make a wedge somewhere
          (else_try),
            (try_begin),
              (eq, ":cavalry_order", mordr_charge),
              (neq, ":nearest_target_distance", Far_Away),
              (copy_position, ":cav_destination", Cavalry_Pos_MOTO),
              (call_script, "script_point_y_toward_position_moto", ":cav_destination", Nearest_Target_Pos),
              (position_move_y, ":cav_destination", ":nearest_target_distance", 0),
              (position_move_y, ":cav_destination", AI_charge_distance, 0),	#charge on through to the other side
            (else_try),
              (neq, ":cavalry_order", mordr_charge),
              (eq, ":num_archers", 0),
              (copy_position, ":cav_destination", Cavalry_Pos_MOTO),	#must be reinforcements, so gather at average position
            (else_try),
              (copy_position, ":cav_destination", Archers_Pos_MOTO),	#hold near archers
              (position_move_x, ":cav_destination", 500, 0),
              (position_move_y, ":cav_destination", -1000, 0),
            (try_end),
            
            #move around threat in the way to destination
            (try_begin),
              (neq, ":nearest_threat_distance", Far_Away),
              (call_script, "script_point_y_toward_position_moto", Cavalry_Pos_MOTO, Nearest_Threat_Pos_MOTO),
              (call_script, "script_point_y_toward_position_moto", Nearest_Threat_Pos_MOTO, ":cav_destination"),
              (position_get_rotation_around_z, reg0, Cavalry_Pos_MOTO),
              (position_get_rotation_around_z, reg1, Nearest_Threat_Pos_MOTO),
              (store_sub, ":rotation_diff", reg0, reg1),
              (try_begin),
                (lt, ":rotation_diff", -180),
                (val_add, ":rotation_diff", 360),
              (else_try),
                (gt, ":rotation_diff", 180),
                (val_sub, ":rotation_diff", 360),
              (try_end),
              
              (try_begin),
                (is_between, ":rotation_diff", -135, 136),
                (copy_position, ":cav_destination", Cavalry_Pos_MOTO),
                (assign, ":distance_to_move", AI_firing_distance),
                (try_begin),	#target is left of threat
                  (is_between, ":rotation_diff", -135, 0),
                  (val_mul, ":distance_to_move", -1),
                (try_end),
                (position_move_x, ":cav_destination", ":distance_to_move", 0),
                (store_sub, ":distance_to_move", ":nearest_threat_distance", AI_firing_distance),
                (position_move_y, ":cav_destination", ":distance_to_move", 0),
                (call_script, "script_point_y_toward_position_moto", ":cav_destination", Cavalry_Pos_MOTO),
                (position_rotate_z, ":cav_destination", 180),
              (try_end),
            (try_end),
            (get_scene_boundaries, pos0, pos1),
            (position_get_x, reg0, ":cav_destination"),
            (position_get_x, reg1, pos0),
            (val_max, reg0, reg1),
            (position_get_x, reg1, pos1),
            (val_min, reg0, reg1),
            (position_set_x, ":cav_destination", reg0),
            (position_get_y, reg0, ":cav_destination"),
            (position_get_y, reg1, pos0),
            (val_max, reg0, reg1),
            (position_get_y, reg1, pos1),
            (val_min, reg0, reg1),
            (position_set_y, ":cav_destination", reg0),
            (position_set_z_to_ground_level, ":cav_destination"),
            
            (try_begin),
              (call_script, "script_cf_battlegroup_valid_formation_moto", ":team_no", grc_cavalry, formation_wedge),
              (copy_position, pos1, ":cav_destination"),
              (call_script, "script_form_cavalry_moto", ":team_no", grc_cavalry, ":team_leader", 0, 0),
              (store_add, ":slot", slot_team_d0_formation, grc_cavalry),
              (team_set_slot, ":team_no", ":slot", formation_wedge),
              # (team_give_order, ":team_no", grc_cavalry, mordr_hold),
            (else_try),
              (call_script, "script_formation_end_moto", ":team_no", grc_cavalry),
              (team_get_movement_order, reg0, ":team_no", grc_cavalry),
              (try_begin),
                (neq, reg0, ":cavalry_order"),
                (team_give_order, ":team_no", grc_cavalry, ":cavalry_order"),
              (try_end),
            (try_end),
            (call_script, "script_set_formation_destination_moto", ":team_no", grc_cavalry, ":cav_destination"),
          (try_end),
        (try_end),
        
        #place leader
        (try_begin),
          (ge, ":team_leader", 0),
          (agent_is_alive, ":team_leader"),
          (agent_slot_eq, ":team_leader", slot_agent_is_running_away, 0),
          (try_begin),
            (le, ":num_infantry", 0),
            (try_begin),
              (this_or_next | le, ":num_archers", 0),
              (eq, ":archer_order", mordr_retreat),
              
              (assign, ":more_reinforcements", 1),
              (try_begin),
                (teams_are_enemies, ":team_no", 0),
                (team_slot_ge, 1, slot_team_reinforcement_stage, AI_Max_Reinforcements),
                (assign, ":more_reinforcements", 0),
              (else_try),
                (teams_are_enemies, ":team_no", 1),
                (team_slot_ge, 0, slot_team_reinforcement_stage, AI_Max_Reinforcements),
                (assign, ":more_reinforcements", 0),
              (try_end),
              (eq, ":more_reinforcements", 0),
              
              (agent_clear_scripted_mode, ":team_leader"),
              (agent_start_running_away, ":team_leader"),
              (agent_set_slot, ":team_leader",  slot_agent_is_running_away, 1),
            (else_try),
              (eq, ":archer_order", mordr_charge),
              (agent_clear_scripted_mode, ":team_leader"),
            (else_try),
              (copy_position, pos1, Archers_Pos_MOTO),
              (position_move_y, pos1, -1000, 0),
              (agent_set_scripted_destination, ":team_leader", pos1, 1),
            (try_end),
          (else_try),
            (neq, ":place_leader_by_infantry", 0),
            (call_script, "script_battlegroup_get_position_moto", pos1, ":team_no", grc_infantry),
            (team_get_order_position, pos0, ":team_no", grc_infantry),
            (call_script, "script_point_y_toward_position_moto", pos1, pos0),
            (call_script, "script_battlegroup_get_action_radius_moto", ":team_no", grc_infantry),
            (val_div, reg0, 2),	#bring to edge of battlegroup
            (position_move_x, pos1, reg0, 0),
            (position_move_x, pos1, 100, 0),
            (agent_set_scripted_destination, ":team_leader", pos1, 1),
          (else_try),
            (agent_clear_scripted_mode, ":team_leader"),
          (try_end),
        (try_end),
      (try_end),
      
  ]),
  
  # script_field_tactics by motomataru
  # Input: flag 1 to include ranged
  # Output: none
  ("field_tactics_moto", [
      (store_script_param, ":include_ranged", 1),
      
      (assign, ":largest_team_size", 0),
      (assign, ":battle_size", 0),
      (try_for_range, ":ai_team", 0, 4),
        (team_get_slot, ":team_size", ":ai_team", slot_team_size),
        (gt, ":team_size", 0),
        (team_get_slot, ":team_cav_size", ":ai_team", slot_team_num_cavalry),
        (store_add, ":team_adj_size", ":team_size", ":team_cav_size"),	#double count cavalry to capture effect on battlefield
        (val_add, ":battle_size", ":team_adj_size"),
        
        (try_begin),
          (neq, ":ai_team", "$fplayer_team_no"),
          (neg | teams_are_enemies, ":ai_team", "$fplayer_team_no"),
          (team_get_slot, ":player_team_adj_size", "$fplayer_team_no", slot_team_adj_size),
          (val_add, ":team_adj_size", ":player_team_adj_size"),	#ally team takes player team into account
          (team_set_slot, "$fplayer_team_no", slot_team_adj_size, ":team_adj_size"),	#and vice versa
        (try_end),
        (team_set_slot, ":ai_team", slot_team_adj_size, ":team_adj_size"),
        
        (lt, ":largest_team_size", ":team_adj_size"),
        (assign, ":largest_team_size", ":team_adj_size"),
      (try_end),
      
      #apply tactics to every AI team
      (set_show_messages, 0),
      (try_for_range, ":ai_team", 0, 4),
        (team_get_slot, ":ai_team_size", ":ai_team", slot_team_adj_size),
        (gt, ":ai_team_size", 0),
        
        (assign, ":do_it", 0),
        (try_begin),
          (neq, ":ai_team", "$fplayer_team_no"),
          (assign, ":do_it", 1),
        (else_try),
          (main_hero_fallen),    #have AI take over for mods with post-player battle action
          (eq, AI_Replace_Dead_Player, 1),
          (assign, ":do_it", 1),
        (try_end),
        (eq, ":do_it", 1),
        
        (team_get_slot, ":ai_faction", ":ai_team", slot_team_faction),
        (try_begin),
          (neq, AI_for_kingdoms_only, 0),
          (neq, ":ai_faction", fac_deserters),	#deserters have military training
          (neq, ":ai_faction", fac_mountain_bandits),	#scoti, frank and dena pirates have military training Chief anade
          (neg | is_between, ":ai_faction", kingdoms_begin, kingdoms_end),
          
          (call_script, "script_formation_end_moto", ":ai_team", grc_everyone),
          (team_get_movement_order, reg0, ":ai_team", grc_everyone),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":ai_team", grc_everyone, mordr_charge),
          (try_end),
          
        #uses tactics
        (else_try),
          (val_mul, ":ai_team_size", 100),
          (store_div, ":team_percentage", ":ai_team_size", ":largest_team_size"),
          (store_div, ":team_battle_presence", ":ai_team_size", ":battle_size"),
          (try_begin),
            (eq, ":include_ranged", 1),
            (try_begin),
              (store_mod, ":team_phase", ":ai_team", 2),
              (eq, ":team_phase", 0),
              (assign, ":time_slice", 0),
            (else_try),
              (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
            (try_end),
            
            (store_mod, reg0, "$ranged_clock", Reform_Trigger_Modulus),
            (this_or_next | eq, reg0, ":time_slice"),
            (eq, "$battle_phase", BP_Setup_MOTO),
            (call_script, "script_team_field_ranged_tactics_moto", ":ai_team", ":team_percentage", ":team_battle_presence"),
          (try_end),
          
          (try_begin),
            (gt, "$fplayer_team_no", 0),	#not a spectator
            (neg | main_hero_fallen),
            (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
            (team_slot_eq, ":ai_team", ":slot", "$fplayer_team_no"),
            (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
            (team_get_slot, ":enemy_division", ":ai_team", ":slot"),
            (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
            (team_slot_ge, "$fplayer_team_no", ":slot", 1),
            (store_add, ":slot", slot_team_d0_fclock, ":enemy_division"),
            (team_get_slot, ":fclock_moto", "$fplayer_team_no", ":slot"),
            (store_mod, reg0, ":fclock_moto", Reform_Trigger_Modulus),
            (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
          (else_try),
            (store_mod, reg0, "$ranged_clock", Reform_Trigger_Modulus),
            (store_mod, ":team_phase", ":ai_team", 2),
            (eq, ":team_phase", 0),
            (assign, ":time_slice", 0),
          (else_try),
            (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
          (try_end),
          
          (eq, reg0, ":time_slice"),
          (call_script, "script_team_field_melee_tactics_moto", ":ai_team", ":team_percentage", ":team_battle_presence"),
        (try_end),
      (try_end),
      (set_show_messages, 1),]),
  
  
  # # Utilities used by AI by motomataru
  
  # script_find_high_ground_around_pos1_corrected by motomataru
  # Input: arg1: destination position
  #			arg2: search_radius (in meters)
  #			pos1 should hold center_position_no
  # Output: destination contains highest ground within a <search_radius> meter
  # square around pos1
  # Also uses position registers: pos0
  ("find_high_ground_around_pos1_corrected_moto", [
      (store_script_param, ":destination_pos", 1),
      (store_script_param, ":search_radius", 2),
      (assign, ":fixed_point_multiplier", 1),
      (convert_to_fixed_point, ":fixed_point_multiplier"),
      (set_fixed_point_multiplier, 1),
      
      (position_get_x, ":o_x", pos1),
      (position_get_y, ":o_y", pos1),
      (store_sub, ":min_x", ":o_x", ":search_radius"),
      (store_sub, ":min_y", ":o_y", ":search_radius"),
      (store_add, ":max_x", ":o_x", ":search_radius"),
      (store_add, ":max_y", ":o_y", ":search_radius"),
      
      (get_scene_boundaries, ":destination_pos", pos0),
      (position_get_x, ":scene_min_x", ":destination_pos"),
      (position_get_x, ":scene_max_x", pos0),
      (position_get_y, ":scene_min_y", ":destination_pos"),
      (position_get_y, ":scene_max_y", pos0),
      (val_max, ":min_x", ":scene_min_x"),
      (val_max, ":min_y", ":scene_min_y"),
      (val_min, ":max_x", ":scene_max_x"),
      (val_min, ":max_y", ":scene_max_y"),
      
      (assign, ":highest_pos_z", -100),
      (copy_position, ":destination_pos", pos1),
      (init_position, pos0),
      
      (try_for_range, ":i_x", ":min_x", ":max_x"),
        (try_for_range, ":i_y", ":min_y", ":max_y"),
          (position_set_x, pos0, ":i_x"),
          (position_set_y, pos0, ":i_y"),
          (position_set_z_to_ground_level, pos0),
          (position_get_z, ":cur_pos_z", pos0),
          (try_begin),
            (gt, ":cur_pos_z", ":highest_pos_z"),
            (copy_position, ":destination_pos", pos0),
            (assign, ":highest_pos_z", ":cur_pos_z"),
          (try_end),
        (try_end),
      (try_end),
      
      (set_fixed_point_multiplier, ":fixed_point_multiplier"),]),
  
  
  # script_cf_count_casualties by motomataru
  # Input: none
  # Output: evalates T/F, reg0 num casualties
  ("cf_count_casualties_moto", [
      (assign, ":num_casualties", 0),
      (try_for_agents,":cur_agent"),
        (try_begin),
          (this_or_next | agent_is_wounded, ":cur_agent"),
          (this_or_next | agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 1),
          (neg | agent_is_alive, ":cur_agent"),
          (val_add, ":num_casualties", 1),
        (try_end),
      (try_end),
      (assign, reg0, ":num_casualties"),
      (gt, ":num_casualties", 0)]),
  
  
  # script_cf_any_fighting by motomataru
  # Input: none
  # Output: evalates T/F
  ("cf_any_fighting_moto", [
      (assign, ":any_fighting", 0),
      (try_for_range, ":team", 0, 4),
        (team_slot_ge, ":team", slot_team_size, 1),
        (eq, ":any_fighting", 0),
        (assign, ":num_divs", 9),
        (try_for_range, ":division", 0, ":num_divs"),
          (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
          (team_slot_ge, ":team", ":slot", 1),
          (assign, ":any_fighting", 1),
          (assign, ":num_divs", 0),
        (try_end),
      (try_end),
      
      #lag this check to be sure
      (store_mission_timer_c, ":time_stamp"),
      (try_begin),	#time lag
        (gt, ":any_fighting", 0),
        (assign, "$teams_last_fighting", ":time_stamp"),
      (try_end),
      (assign, ":fighting_finished", formation_reform_interval),
      (val_max, ":fighting_finished", 5),
      (val_add, ":fighting_finished", "$teams_last_fighting"),
      (gt, ":fighting_finished", ":time_stamp"),]),
  
  
  # script_get_nearest_enemy_battlegroup_location by motomataru
  # Input: destination position, fron team, from position
  # Output: destination position, reg0 with distance
  # Run script_store_battlegroup_data before calling!
  ("get_nearest_enemy_battlegroup_location_moto", [
      (store_script_param, ":bgposition", 1),
      (store_script_param, ":team_no", 2),
      (store_script_param, ":from_pos", 3),
      (assign, ":distance_to_nearest_enemy_battlegoup", Far_Away),
      (try_for_range, ":enemy_team_no", 0, 4),
        (team_slot_ge, ":enemy_team_no", slot_team_size, 1),
        (teams_are_enemies, ":enemy_team_no", ":team_no"),
        (try_for_range, ":enemy_division", 0, 9),
          (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
          (team_slot_ge, ":enemy_team_no", ":slot", 1),
          (call_script, "script_battlegroup_get_position_moto", pos0, ":enemy_team_no", ":enemy_division"),
          (get_distance_between_positions, reg0, pos0, ":from_pos"),
          (try_begin),
            (gt, ":distance_to_nearest_enemy_battlegoup", reg0),
            (assign, ":distance_to_nearest_enemy_battlegoup", reg0),
            (copy_position, ":bgposition", pos0),
          (try_end),
        (try_end),
      (try_end),
      (assign, reg0, ":distance_to_nearest_enemy_battlegoup")]),
  # #AI end

# #Formations Scripts
  # script_field_start_position by motomataru
  # Input: team
  # Output: pos2 = current army position advanced by cavalry wedge depth over
  # infantry formation depth
  # Originally written to prevent map border accidents when setting up player
  # army at its spawn point
  ("field_start_position_moto", [
      (store_script_param, ":fteam", 1),
      
      (assign, ":depth_cavalry", 0),
      (assign, ":largest_mounted_division_size", 0),
      #(team_get_leader, ":fleader", ":fteam"),
      (call_script, "script_team_get_nontroll_leader", ":fteam"),
      (assign, ":fleader", reg0),
      
      (try_begin),
        (ge, ":fleader", 0),
        (agent_get_position, pos2, ":fleader"),
      (else_try),
        (call_script, "script_battlegroup_get_position_moto", pos2, ":fteam", grc_everyone),
      (try_end),
      
      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_slot_eq, ":fteam", ":slot", sdt_cavalry),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_get_slot, reg0, ":fteam", ":slot"),
        (lt, ":largest_mounted_division_size", reg0),
        (assign, ":largest_mounted_division_size", reg0),
      (try_end),
      
      (try_begin),
        (gt, ":largest_mounted_division_size", 0),
        (val_mul, ":largest_mounted_division_size", 2),
        (convert_to_fixed_point, ":largest_mounted_division_size"),
        (store_sqrt, ":depth_cavalry", ":largest_mounted_division_size"),
        (convert_from_fixed_point, ":depth_cavalry"),
        (val_sub, ":depth_cavalry", 1),
        
        (store_mul, reg0, formation_start_spread_out, 50),
        (val_add, reg0, formation_minimum_spacing_horse_length),
        (val_mul, ":depth_cavalry", reg0),
        
        (store_mul, ":depth_infantry", formation_start_spread_out, 50),
        (val_add, ":depth_infantry", formation_minimum_spacing),
        (val_mul, ":depth_infantry", 2),
        (val_sub, ":depth_cavalry", ":depth_infantry"),
        
        (gt, ":depth_cavalry", 0),
        (call_script, "script_team_get_position_of_enemies_moto", Enemy_Team_Pos_MOTO, ":fteam", grc_everyone),
        (call_script, "script_point_y_toward_position_moto", pos2, Enemy_Team_Pos_MOTO),
        (position_move_y, pos2, ":depth_cavalry"),
      (try_end),]),
  
  # script_division_reset_places by motomataru
  # Input: none
  # Output: none
  # Resets globals for placing divisions around player for
  # script_battlegroup_place_around_leader
  ("division_reset_places_moto", [
      (assign, "$next_cavalry_place", formation_minimum_spacing_horse_width),	#first spot RIGHT of the player
      (assign, "$next_archer_place", 1000),	#first spot 10m FRONT of the player
      (assign, "$next_infantry_place", -1 * formation_minimum_spacing_horse_width),	#first spot LEFT of the player
  ]),
  
  # script_battlegroup_place_around_leader by motomataru
  # Input: team, division, team leader
  # Output: pos61 division position, moves pos1
  ("battlegroup_place_around_leader_moto", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      
      (try_begin),
        (le, ":fleader", 0),
        (display_message, "@{!}script_battlegroup_place_around_leader: invalid leader agent (bad call)"),
        
      (else_try),
        (agent_get_group, reg0, ":fleader"),
        (neq, reg0, ":fteam"),
        (display_message, "@{!}script_battlegroup_place_around_leader: leader team mismatch (bad call)"),
        
      (else_try),
        (agent_get_position, pos1, ":fleader"),
        (call_script, "script_battlegroup_place_around_pos1_moto", ":fteam", ":fdivision", ":fleader"),
      (try_end),]),
  
  # script_battlegroup_place_around_pos1 by motomataru
  # Input: team, division
  # Output: pos61 division position, moves pos1
  ("battlegroup_place_around_pos1_moto", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      
      (assign, ":store_fpm", 1),
      (convert_to_fixed_point, ":store_fpm"),
      (set_fixed_point_multiplier, 100),
      
      (store_sub, ":player_division", "$FormAI_player_in_division", 1),
      (try_begin),
        (eq, ":player_division", ":fdivision"),
        (assign, ":first_member_is_player", 1),
      (else_try),
        (assign, ":first_member_is_player", 0),
      (try_end),
      
      (try_begin),
        (eq, "$FormAI_autorotate", 1),
        (call_script, "script_team_get_position_of_enemies_moto", Enemy_Team_Pos_MOTO, ":fteam", grc_everyone),
        (neq, reg0, 0),	#more than 0 enemies still alive?
        (call_script, "script_point_y_toward_position_moto", pos1, Enemy_Team_Pos_MOTO),
      (try_end),
      
      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (team_get_slot, ":sd_type", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_size, ":fdivision"),
      (team_get_slot, ":num_troops", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
      (team_get_slot, ":fformation", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
      (team_get_slot, ":formation_extra_spacing", ":fteam", ":slot"),
      
      #handle memorized placement
      (try_begin),
        (eq, ":first_member_is_player", 0),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":fdivision"),
        (faction_get_slot, ":value", "fac_player_faction", ":slot"),	#only used for player now
        (neq, ":value", 0),
        
        (position_move_x, pos1, ":value", 0),
        (store_add, ":slot", slot_faction_d0_mem_relative_y, ":fdivision"),
        (faction_get_slot, ":value", "fac_player_faction", ":slot"),	#only used for player now
        (position_move_y, pos1, ":value", 0),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (try_begin),
            (this_or_next | eq, ":sd_type", sdt_cavalry),
            (eq, ":sd_type", sdt_harcher),
            (call_script, "script_form_cavalry_moto", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0),
          (else_try),
            (eq, ":sd_type", sdt_archer),
            (call_script, "script_get_centering_amount_moto", formation_default, ":num_troops", ":formation_extra_spacing"),
            (val_mul, reg0, -1),
            (position_move_x, pos1, reg0, 0),
            (call_script, "script_form_archers_moto", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0, ":fformation"),
          (else_try),
            (call_script, "script_get_centering_amount_moto", ":fformation", ":num_troops", ":formation_extra_spacing"),
            (position_move_x, pos1, reg0, 0),
            (call_script, "script_form_infantry_moto", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0, ":fformation"),
          (try_end),
        (try_end),
        
      #default placement per division type
      (else_try),
        (this_or_next | eq, ":sd_type", sdt_cavalry),
        (eq, ":sd_type", sdt_harcher),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_x, pos1, "$next_cavalry_place", 0),
        (try_end),
        
        (try_begin),
          (gt, ":fformation", formation_none),
          (store_mul, ":troop_space", ":formation_extra_spacing", 50),
          (val_add, ":troop_space", formation_minimum_spacing_horse_width),
          (convert_to_fixed_point, ":num_troops"),
          (store_sqrt, ":formation_width", ":num_troops"),
          (val_mul, ":formation_width", ":troop_space"),
          (convert_from_fixed_point, ":formation_width"),
          (val_sub, ":formation_width", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (position_move_x, pos1, reg0, 0),	#cavalry set up RIGHT of leader
          (copy_position, pos61, pos1),
          (call_script, "script_form_cavalry_moto", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player"),
          
        #handle Native's way of doing things
        (else_try),
          (store_mul, ":troop_space", ":formation_extra_spacing", 133),	#cm added by each Spread Out
          (val_add, ":troop_space", 150),	#minimum spacing
          
          #WFaS multi-ranks
          (try_begin),
            (eq, ":fformation", formation_2_row),
            (val_div, ":num_troops", 2),
          (else_try),
            (eq, ":fformation", formation_3_row),
            (val_div, ":num_troops", 3),
          (else_try),
            (eq, ":fformation", formation_4_row),
            (val_div, ":num_troops", 4),
          (else_try),
            (eq, ":fformation", formation_5_row),
            (val_div, ":num_troops", 5),
            
          (else_try),	#WB multi-ranks
            (lt, ":formation_extra_spacing", 0),
            (assign, ":troop_space", 200),
            (val_mul, ":formation_extra_spacing", -1),
            (val_add, ":formation_extra_spacing", 1),
            (val_div, ":num_troops", ":formation_extra_spacing"),
          (try_end),
          
          (store_mul, ":formation_width", ":num_troops", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (position_move_x, pos1, reg0, 0),	#cavalry set up RIGHT of leader
          (copy_position, pos61, pos1),
        (try_end),
        
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (val_add, "$next_cavalry_place", ":formation_width"),
          (val_add, "$next_cavalry_place", formation_minimum_spacing_horse_width),
        (try_end),
        
      (else_try),
        (eq, ":sd_type", sdt_archer),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_y, pos1, "$next_archer_place"),	#archers set up FRONT of leader
          (val_add, "$next_archer_place", 500),	#next archers 5m FRONT of these
        (try_end),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_get_centering_amount_moto", formation_default, ":num_troops", ":formation_extra_spacing"),
          (val_mul, reg0, -1),
          (position_move_x, pos1, reg0, 0),
          (call_script, "script_form_archers_moto", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
        (try_end),
        
      (else_try),
        (eq, ":sd_type", sdt_skirmisher),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_y, pos1, "$next_archer_place"),	#skirmishers set up FRONT of leader
          (val_add, "$next_archer_place", 500),	#next archers 5m FRONT of these
        (try_end),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_get_centering_amount_moto", ":fformation", ":num_troops", ":formation_extra_spacing"),
          (position_move_x, pos1, reg0, 0),
          (call_script, "script_form_infantry_moto", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
        (try_end),
        
      (else_try),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_x, pos1, "$next_infantry_place", 0),
        (try_end),
        (copy_position, pos61, pos1),
        
        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_form_infantry_moto", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
          (call_script, "script_get_centering_amount_moto", ":fformation", ":num_troops", ":formation_extra_spacing"),
          (store_mul, ":formation_width", 2, reg0),
          (store_mul, ":troop_space", ":formation_extra_spacing", 50),
          (val_add, ":troop_space", formation_minimum_spacing),
          (val_add, ":formation_width", ":troop_space"),
          (val_mul, reg0, -1),	#infantry set up LEFT of leader
          (position_move_x, pos61, reg0, 0),
          
        #handle Native's way of doing things
        (else_try),
          (store_mul, ":troop_space", ":formation_extra_spacing", 75),	#Native minimum spacing not consistent but less than this
          (val_add, ":troop_space", 100),	#minimum spacing
          
          #WFaS multi-ranks
          (try_begin),
            (eq, ":fformation", formation_2_row),
            (val_div, ":num_troops", 2),
          (else_try),
            (eq, ":fformation", formation_3_row),
            (val_div, ":num_troops", 3),
          (else_try),
            (eq, ":fformation", formation_4_row),
            (val_div, ":num_troops", 4),
          (else_try),
            (eq, ":fformation", formation_5_row),
            (val_div, ":num_troops", 5),
            
          (else_try),	#WB multi-ranks
            (lt, ":formation_extra_spacing", 0),
            (assign, ":troop_space", 150),
            (val_mul, ":formation_extra_spacing", -1),
            (val_add, ":formation_extra_spacing", 1),
            (val_div, ":num_troops", ":formation_extra_spacing"),
          (try_end),
          
          (store_mul, ":formation_width", ":num_troops", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (val_mul, reg0, -1),	#infantry set up LEFT of leader
          (position_move_x, pos61, reg0, 0),
        (try_end),
        
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (val_sub, "$next_infantry_place", ":formation_width"),	#next infantry 1m LEFT of these
          (val_sub, "$next_infantry_place", 100),
        (try_end),
      (try_end),
      
      (store_add, ":slot", slot_team_d0_move_order, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", mordr_hold),
      (set_show_messages, 0),
      (team_get_movement_order, reg0, ":fteam", ":fdivision"),
      (try_begin),
        (neq, reg0, mordr_hold),
        (team_give_order, ":fteam", ":fdivision", mordr_hold),
      (try_end),
      (call_script, "script_set_formation_destination_moto", ":fteam", ":fdivision", pos61),
      (set_show_messages, 1),
      (set_fixed_point_multiplier, ":store_fpm"),]),
  
  # script_form_cavalry by motomataru
  # Input: (pos1), team, division, agent number of team leader, spacing, flag
  # TRUE to include team leader in formation
  # Output: none
  # Form in wedge, (now not) excluding horse archers
  # Creates formation starting at pos1
  ("form_cavalry_moto", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      (store_script_param, ":formation_extra_spacing", 4),
      (store_script_param, ":include_leader", 5),
      (store_mul, ":extra_space", ":formation_extra_spacing", 50),
      (store_add, ":x_distance", formation_minimum_spacing_horse_width, ":extra_space"),
      (store_add, ":y_distance", formation_minimum_spacing_horse_length, ":extra_space"),
      (assign, ":max_level", 0),
      (try_for_agents, ":agent"),
        (call_script, "script_cf_valid_formation_member_moto", ":fteam", ":fdivision", ":fleader", ":agent"),
        (agent_get_troop_id, ":troop_id", ":agent"),
        (store_character_level, ":troop_level", ":troop_id"),
        (gt, ":troop_level", ":max_level"),
        (assign, ":max_level", ":troop_level"),
      (end_try),
      (assign, ":column", 1),
      (assign, ":rank_dimension", 1),
      (store_mul, ":neg_y_distance", ":y_distance", -1),
      (store_mul, ":neg_x_distance", ":x_distance", -1),
      (store_div, ":wedge_adj", ":x_distance", 2),
      (store_div, ":neg_wedge_adj", ":neg_x_distance", 2),
      (assign, ":form_left", 1),
      (try_begin),
        (eq, ":include_leader", 0),
        (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", -1),
      (else_try),	#after leader, move to next position (copied from below)
        (team_set_slot, ":fteam", ":slot", ":fleader"),
        (try_begin),
          (eq, ":form_left", 1),
          (position_move_x, pos1, ":neg_x_distance", 0),
        (else_try),
          (position_move_x, pos1, ":x_distance", 0),
        (try_end),
        (val_add, ":column", 1),
        (gt, ":column", ":rank_dimension"),
        (position_move_y, pos1, ":neg_y_distance", 0),
        (try_begin),
          (neq, ":form_left", 1),
          (assign, ":form_left", 1),
          (position_move_x, pos1, ":neg_wedge_adj", 0),
        (else_try),
          (assign, ":form_left", 0),
          (position_move_x, pos1, ":wedge_adj", 0),
        (try_end),
        (assign, ":column", 1),
        (val_add, ":rank_dimension", 1),
      (try_end),
      
      (val_add, ":max_level", 1),
      (try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
        (try_for_agents, ":agent"),
          (agent_get_troop_id, ":troop_id", ":agent"),
          (store_character_level, ":troop_level", ":troop_id"),
          (eq, ":troop_level", ":rank_level"),
          (call_script, "script_cf_valid_formation_member_moto", ":fteam", ":fdivision", ":fleader", ":agent"),
          (agent_set_scripted_destination, ":agent", pos1, 1),
          (try_begin),	#First Agent
            (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
            (neg | team_slot_ge, ":fteam", ":slot", 0),
            (team_set_slot, ":fteam", ":slot", ":agent"),
          (try_end),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_x_distance", 0),
          (else_try),
            (position_move_x, pos1, ":x_distance", 0),
          (try_end),
          (val_add, ":column", 1),
          (gt, ":column", ":rank_dimension"),
          (position_move_y, pos1, ":neg_y_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_wedge_adj", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":wedge_adj", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank_dimension", 1),
        (end_try),
      (end_try),]),
  
  # script_form_archers by motomataru
  # Input: (pos1), team, division, agent number of team leader, spacing, flag
  # TRUE to include team leader in formation, formation
  # Output: none
  # Form in line, staggered if formation = formation_ranks
  # Creates formation starting at pos1
  ("form_archers_moto", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      (store_script_param, ":formation_extra_spacing", 4),
      (store_script_param, ":include_leader", 5),
      (store_script_param, ":archers_formation", 6),
      (store_mul, ":extra_space", ":formation_extra_spacing", 50),
      (store_add, ":distance", formation_minimum_spacing, ":extra_space"),		#minimum distance between troops
      (assign, ":total_move_y", 0),	#staggering variable
      (try_begin),
        (eq, ":include_leader", 0),
        (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", -1),
      (else_try),	#after leader, move to next position (copied from below)
        (team_set_slot, ":fteam", ":slot", ":fleader"),
        (position_move_x, pos1, ":distance", 0),
        (try_begin),
          (eq, ":archers_formation", formation_ranks),
          (val_add, ":total_move_y", 75),
          (try_begin),
            (le, ":total_move_y", 150),
            (position_move_y, pos1, 75, 0),
          (else_try),
            (position_move_y, pos1, -150, 0),
            (assign, ":total_move_y", 0),
          (try_end),
        (try_end),
      (try_end),
      
      (try_for_agents, ":agent"),
        (call_script, "script_cf_valid_formation_member_moto", ":fteam", ":fdivision", ":fleader", ":agent"),
        (agent_set_scripted_destination, ":agent", pos1, 1),
        (try_begin),	#First Agent
          (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
          (neg | team_slot_ge, ":fteam", ":slot", 0),
          (team_set_slot, ":fteam", ":slot", ":agent"),
        (try_end),
        (position_move_x, pos1, ":distance", 0),
        (try_begin),
          (eq, ":archers_formation", formation_ranks),
          (val_add, ":total_move_y", 75),
          (try_begin),
            (le, ":total_move_y", 150),
            (position_move_y, pos1, 75, 0),
          (else_try),
            (position_move_y, pos1, -150, 0),
            (assign, ":total_move_y", 0),
          (try_end),
        (try_end),
      (try_end),]),
  
  # script_form_infantry by motomataru
  # Input: (pos1), team, division, agent number of team leader, spacing, flag
  # TRUE to include team leader in formation, formation
  # Output: none
  # If input "formation" is formation_default, will select a formation based on
  # faction
  # Creates formation starting at pos1
  ("form_infantry_moto", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      (store_script_param, ":formation_extra_spacing", 4),
      (store_script_param, ":include_leader", 5),
      (store_script_param, ":infantry_formation", 6),
      (store_mul, ":extra_space", ":formation_extra_spacing", 50),
      (store_add, ":distance", formation_minimum_spacing, ":extra_space"),		#minimum distance between troops
      (store_mul, ":neg_distance", ":distance", -1),
      (store_add, ":slot", slot_team_d0_size, ":fdivision"),
      (team_get_slot, ":num_troops", ":fteam", ":slot"),
      (try_begin),
        (eq, ":infantry_formation", formation_default),
        (call_script, "script_get_default_formation_moto", ":fteam"),
        (assign, ":infantry_formation", reg0),
      (try_end),
      (team_get_weapon_usage_order, ":weapon_order", ":fteam", ":fdivision"),
      (team_get_hold_fire_order, ":fire_order", ":fteam", ":fdivision"),
      (assign, ":form_left", 1),
      (assign, ":column", 1),
      (assign, ":rank", 1),
      
      (try_begin),
        (eq, ":infantry_formation", formation_square),
        (convert_to_fixed_point, ":num_troops"),
        (store_sqrt, ":square_dimension", ":num_troops"),
        (convert_from_fixed_point, ":square_dimension"),
        (val_add, ":square_dimension", 1),
        (try_begin),
          (eq, ":include_leader", 0),
          (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", -1),
        (else_try),	#after leader, move to next position (copied from below)
          (team_set_slot, ":fteam", ":slot", ":fleader"),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (val_add, ":column", 1),
          (gt, ":column", ":square_dimension"),
          (position_move_y, pos1, ":neg_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank", 1),
        (try_end),
        
        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member_moto", ":fteam", ":fdivision", ":fleader", ":agent"),
          #(call_script, "script_switch_to_noswing_weapons_moto", ":agent", ":distance"),
          
          (try_begin),
            (eq, "$battle_phase", BP_Deploy),
            (agent_set_scripted_destination, ":agent", pos1),
          (else_try),
            (call_script, "script_formation_process_agent_move_moto", ":fteam", ":fdivision", ":agent", ":rank"),
          (try_end),
          
          (try_begin),
            (eq, formation_reequip, 1),
            (eq, ":weapon_order", wordr_use_any_weapon),
            (try_begin),
              (this_or_next | eq, ":rank", 1),
              (this_or_next | ge, ":rank", ":square_dimension"),
              (this_or_next | eq, ":column", 1),
              (ge, ":column", ":square_dimension"),
              (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 0, ":fire_order"),
              (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
              (agent_ai_set_always_attack_in_melee, ":agent", 0),
            (else_try),
              (agent_get_slot, ":closest_enemy", ":agent", slot_agent_nearest_enemy_agent),
              (try_begin),
                (neq, ":closest_enemy", -1),
                (agent_get_position, pos0, ":closest_enemy"),
                (get_distance_between_positions, ":enemy_distance", pos0, pos1),
                (le, ":enemy_distance", ":distance"),	#enemy closer than friends?
                (neg | position_is_behind_position, pos0, pos1),
                (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 0, ":fire_order"),
                (try_begin),
                  (position_is_behind_position, pos1, pos0),
                  (agent_ai_set_always_attack_in_melee, ":agent", 1),
                (else_try),
                  (agent_ai_set_always_attack_in_melee, ":agent", 0),
                (try_end),
              (else_try),
                (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 1, ":fire_order"),
                (agent_ai_set_always_attack_in_melee, ":agent", 1),
              (try_end),
              (agent_set_slot, ":agent", slot_agent_inside_formation, 1),
            (try_end),
          (try_end),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (val_add, ":column", 1),
          (gt, ":column", ":square_dimension"),
          (position_move_y, pos1, ":neg_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank", 1),
        (end_try),
        
      (else_try),
        (eq, ":infantry_formation", formation_wedge),
        (try_for_range, reg0, 0, 50),
          (troop_set_slot, "trp_temp_array_a", reg0, 0),
        (try_end),
        (assign, ":max_level", 0),
        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member_moto", ":fteam", ":fdivision", ":fleader", ":agent"),
          #(call_script, "script_switch_to_noswing_weapons_moto", ":agent", ":distance"),
          (agent_get_troop_id, ":troop_id", ":agent"),
          (store_character_level, ":troop_level", ":troop_id"),
          (troop_set_slot, "trp_temp_array_a", ":troop_level", 1),
          (gt, ":troop_level", ":max_level"),
          (assign, ":max_level", ":troop_level"),
        (end_try),
        
        (assign, ":rank_dimension", 1),
        (store_div, ":wedge_adj", ":distance", 2),
        (store_div, ":neg_wedge_adj", ":neg_distance", 2),
        (try_begin),
          (eq, ":include_leader", 0),
          (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", -1),
        (else_try),	#after leader, move to next position (copied from below)
          (team_set_slot, ":fteam", ":slot", ":fleader"),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (val_add, ":column", 1),
          (gt, ":column", ":rank_dimension"),
          (position_move_y, pos1, ":neg_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_wedge_adj", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":wedge_adj", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank_dimension", 1),
        (try_end),
        
        (val_add, ":max_level", 1),
        (try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
          (troop_slot_eq, "trp_temp_array_a", ":rank_level", 1),
          (try_for_agents, ":agent"),
            (agent_get_troop_id, ":troop_id", ":agent"),
            (store_character_level, ":troop_level", ":troop_id"),
            (eq, ":troop_level", ":rank_level"),
            (call_script, "script_cf_valid_formation_member_moto", ":fteam", ":fdivision", ":fleader", ":agent"),
            
            (try_begin),
              (eq, "$battle_phase", BP_Deploy),
              (agent_set_scripted_destination, ":agent", pos1),
            (else_try),
              (call_script, "script_formation_process_agent_move_moto", ":fteam", ":fdivision", ":agent", ":rank_dimension"),
            (try_end),
            
            (try_begin),
              (eq, formation_reequip, 1),
              (eq, ":weapon_order", wordr_use_any_weapon),
              (try_begin),
                (this_or_next | eq, ":column", 1),
                (ge, ":column", ":rank_dimension"),
                (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 0, ":fire_order"),
                (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
                (agent_ai_set_always_attack_in_melee, ":agent", 0),
              (else_try),
                (agent_get_slot, ":closest_enemy", ":agent", slot_agent_nearest_enemy_agent),
                (try_begin),
                  (neq, ":closest_enemy", -1),
                  (agent_get_position, pos0, ":closest_enemy"),
                  (get_distance_between_positions, ":enemy_distance", pos0, pos1),
                  (le, ":enemy_distance", ":distance"),	#enemy closer than friends?
                  (neg | position_is_behind_position, pos0, pos1),
                  (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 0, ":fire_order"),
                  (try_begin),
                    (position_is_behind_position, pos1, pos0),
                    (agent_ai_set_always_attack_in_melee, ":agent", 1),
                  (else_try),
                    (agent_ai_set_always_attack_in_melee, ":agent", 0),
                  (try_end),
                (else_try),
                  (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 1, ":fire_order"),
                  (agent_ai_set_always_attack_in_melee, ":agent", 1),
                (try_end),
                (agent_set_slot, ":agent", slot_agent_inside_formation, 1),
              (try_end),
            (try_end),
            (try_begin),
              (eq, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (val_add, ":column", 1),
            (gt, ":column", ":rank_dimension"),
            (position_move_y, pos1, ":neg_distance", 0),
            (try_begin),
              (neq, ":form_left", 1),
              (assign, ":form_left", 1),
              (position_move_x, pos1, ":neg_wedge_adj", 0),
            (else_try),
              (assign, ":form_left", 0),
              (position_move_x, pos1, ":wedge_adj", 0),
            (try_end),
            (assign, ":column", 1),
            (val_add, ":rank_dimension", 1),
          (end_try),
        (end_try),
        
      (else_try),
        (eq, ":infantry_formation", formation_ranks),
        (try_for_range, reg0, 0, 50),
          (troop_set_slot, "trp_temp_array_a", reg0, 0),
        (try_end),
        (call_script, "script_calculate_default_ranks_moto", ":num_troops"),
        (store_div, ":rank_dimension", ":num_troops", reg1),
        (val_add, ":rank_dimension", 1),
        (assign, ":max_level", 0),
        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member_moto", ":fteam", ":fdivision", ":fleader", ":agent"),
         # (call_script, "script_switch_to_noswing_weapons_moto", ":agent", ":distance"),
          (agent_get_troop_id, ":troop_id", ":agent"),
          (store_character_level, ":troop_level", ":troop_id"),
          (troop_set_slot, "trp_temp_array_a", ":troop_level", 1),
          (gt, ":troop_level", ":max_level"),
          (assign, ":max_level", ":troop_level"),
        (end_try),
        
        (try_begin),
          (eq, ":include_leader", 0),
          (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", -1),
        (else_try),	#after leader, move to next position (copied from below)
          (team_set_slot, ":fteam", ":slot", ":fleader"),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (val_add, ":column", 1),
          
          (gt, ":column", ":rank_dimension"),	#next rank?
          (position_move_y, pos1, ":neg_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank", 1),
        (try_end),
        
        (val_add, ":max_level", 1),
        (try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
          (troop_slot_eq, "trp_temp_array_a", ":rank_level", 1),
          (try_for_agents, ":agent"),
            (agent_get_troop_id, ":troop_id", ":agent"),
            (store_character_level, ":troop_level", ":troop_id"),
            (eq, ":troop_level", ":rank_level"),
            (call_script, "script_cf_valid_formation_member_moto", ":fteam", ":fdivision", ":fleader", ":agent"),
            
            (try_begin),
              (eq, "$battle_phase", BP_Deploy),
              (agent_set_scripted_destination, ":agent", pos1),
            (else_try),
              (call_script, "script_formation_process_agent_move_moto", ":fteam", ":fdivision", ":agent", ":rank"),
            (try_end),
            
            (try_begin),
              (eq, formation_reequip, 1),
              (eq, ":weapon_order", wordr_use_any_weapon),
              (try_begin),
                (eq, ":rank", 1),
                (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 0, ":fire_order"),
                (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
                (agent_ai_set_always_attack_in_melee, ":agent", 0),
              (else_try),
                (agent_get_slot, ":closest_enemy", ":agent", slot_agent_nearest_enemy_agent),
                (try_begin),
                  (neq, ":closest_enemy", -1),
                  (agent_get_position, pos0, ":closest_enemy"),
                  (get_distance_between_positions, ":enemy_distance", pos0, pos1),
                  (le, ":enemy_distance", ":distance"),	#enemy closer than friends?
                  (neg | position_is_behind_position, pos0, pos1),
                  (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 0, ":fire_order"),
                  (try_begin),
                    (position_is_behind_position, pos1, pos0),
                    (agent_ai_set_always_attack_in_melee, ":agent", 1),
                  (else_try),
                    (agent_ai_set_always_attack_in_melee, ":agent", 0),
                  (try_end),
                (else_try),
                  (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 1, ":fire_order"),
                  (agent_ai_set_always_attack_in_melee, ":agent", 1),
                (try_end),
                (agent_set_slot, ":agent", slot_agent_inside_formation, 1),
              (try_end),
            (try_end),
            (try_begin),
              (eq, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (val_add, ":column", 1),
            
            (gt, ":column", ":rank_dimension"),	#next rank?
            (position_move_y, pos1, ":neg_distance", 0),
            (try_begin),
              (neq, ":form_left", 1),
              (assign, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (assign, ":form_left", 0),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (assign, ":column", 1),
            (val_add, ":rank", 1),
          (end_try),
        (end_try),
        
      (else_try),
        (eq, ":infantry_formation", formation_shield),
        (call_script, "script_calculate_default_ranks_moto", ":num_troops"),
        (store_div, ":rank_dimension", ":num_troops", reg1),
        (val_add, ":rank_dimension", 1),
        (try_begin),
          (eq, ":include_leader", 0),
          (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", -1),
        (else_try),	#after leader, move to next position (copied from below)
          (team_set_slot, ":fteam", ":slot", ":fleader"),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (val_add, ":column", 1),
          
          (gt, ":column", ":rank_dimension"),	#next rank?
          (position_move_y, pos1, ":neg_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank", 1),
        (try_end),
        
        (troop_set_slot, "trp_temp_array_a", 0, 0),	#short weap agent array
        (troop_set_slot, "trp_temp_array_b", 0, 0),	#medium weap agent array
        (troop_set_slot, "trp_temp_array_c", 0, 0),	#long weap agent array
        
        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member_moto", ":fteam", ":fdivision", ":fleader", ":agent"),
          #(call_script, "script_switch_to_noswing_weapons_moto", ":agent", ":distance"),
          
          (assign, ":cur_score", 0),
          (try_for_range, ":item_slot", ek_item_0, ek_head),
            (agent_get_item_slot, ":item", ":agent", ":item_slot"),
            (gt, ":item", itm_no_item),
            (item_get_type, ":weapon_type", ":item"),
            (neq, ":weapon_type", itp_type_shield),
            
            (try_begin),
              (call_script, "script_cf_is_weapon_ranged_moto", ":item", 1),
              
            (else_try),
              (item_get_weapon_length, ":item_length", ":item"),
              (lt, ":cur_score", ":item_length"),
              (assign, ":cur_score", ":item_length"),
            (try_end),
          (try_end),
          
          (try_begin),
            (eq, ":cur_score", 0),	#no melee weapons
            (assign, ":cur_array", "trp_temp_array_c"),
          (else_try),
            (le, ":cur_score", Third_Max_Weapon_Length),
            (assign, ":cur_array", "trp_temp_array_a"),
          (else_try),
            (gt, ":cur_score", 2 * Third_Max_Weapon_Length),
            (assign, ":cur_array", "trp_temp_array_c"),
          (else_try),
            (assign, ":cur_array", "trp_temp_array_b"),
          (try_end),
          
          (troop_get_slot, ":array_end", ":cur_array", 0),
          (val_add, ":array_end", 1),
          (troop_set_slot, ":cur_array", ":array_end", ":agent"),
          (troop_set_slot, ":cur_array", 0, ":array_end"),
          (agent_set_slot, ":agent", slot_agent_positioned, 0),
        (try_end),
        
        #find shields first
        (store_add, ":arrays_end", "trp_temp_array_c", 1),
        (try_for_range, ":cur_array", "trp_temp_array_a", ":arrays_end"),
          (troop_get_slot, ":array_end", ":cur_array", 0),
          (val_add, ":array_end", 1),
          
          (try_for_range, ":slot", 1, ":array_end"),
            (troop_get_slot, ":agent", ":cur_array", ":slot"),
            (assign, ":form_up", 0),
            
            (try_for_range, ":item_slot", ek_item_0, ek_head),
              (agent_get_item_slot, ":item", ":agent", ":item_slot"),
              (gt, ":item", itm_no_item),
              (item_get_type, ":weapon_type", ":item"),
              (eq, ":weapon_type", itp_type_shield),
              (item_get_weapon_length, reg0, ":item"),	#gets shield width, which is always defined (see header_items)
              (ge, reg0, 25),	#wider than troop?
              (assign, ":form_up", 1),
            (try_end),
            
            (eq, ":form_up", 1),
            (agent_set_slot, ":agent", slot_agent_positioned, 1),
            (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
            
            (try_begin),
              (eq, "$battle_phase", BP_Deploy),
              (agent_set_scripted_destination, ":agent", pos1),
            (else_try),
              (call_script, "script_formation_process_agent_move_moto", ":fteam", ":fdivision", ":agent", ":rank"),
            (try_end),
            
            (try_begin),
              (eq, formation_reequip, 1),
              (eq, ":weapon_order", wordr_use_any_weapon),
              (call_script, "script_equip_best_melee_weapon_moto", ":agent", 1, 0, ":fire_order"),	#best weapon, force shield
            (try_end),
            
            (try_begin),
              (eq, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (val_add, ":column", 1),
            
            (gt, ":column", ":rank_dimension"),	#next rank?
            (position_move_y, pos1, ":neg_distance", 0),
            (try_begin),
              (neq, ":form_left", 1),
              (assign, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (assign, ":form_left", 0),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (assign, ":column", 1),
            (val_add, ":rank", 1),
            
            #break loops
            (assign, ":array_end", ":slot"),
            (assign, ":arrays_end", ":cur_array"),
          (try_end),
        (try_end),
        
        #add rest of division
        (store_add, ":arrays_end", "trp_temp_array_c", 1),
        (try_for_range, ":cur_array", "trp_temp_array_a", ":arrays_end"),
          (troop_get_slot, ":array_end", ":cur_array", 0),
          (val_add, ":array_end", 1),
          
          (try_for_range, ":slot", 1, ":array_end"),
            (troop_get_slot, ":agent", ":cur_array", ":slot"),
            (agent_slot_eq, ":agent", slot_agent_positioned, 0),
            (agent_set_slot, ":agent", slot_agent_positioned, 1),
            
            (try_begin),
              (eq, ":rank", 1),
              (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
            (else_try),
              (agent_set_slot, ":agent", slot_agent_inside_formation, 1),
            (try_end),
            
            (try_begin),
              (eq, "$battle_phase", BP_Deploy),
              (agent_set_scripted_destination, ":agent", pos1),
            (else_try),
              (call_script, "script_formation_process_agent_move_moto", ":fteam", ":fdivision", ":agent", ":rank"),
            (try_end),
            
            (try_begin),
              (eq, formation_reequip, 1),
              (eq, ":weapon_order", wordr_use_any_weapon),
              
              (try_begin),
                (eq, ":rank", 1),
                (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 0, ":fire_order"),
                (agent_ai_set_always_attack_in_melee, ":agent", 0),
                
              #enemy closer than friends?
              (else_try),
                (agent_get_slot, ":closest_enemy", ":agent", slot_agent_nearest_enemy_agent),
                (neq, ":closest_enemy", -1),
                (agent_get_position, pos0, ":closest_enemy"),
                (get_distance_between_positions, ":enemy_distance", pos0, pos1),
                (le, ":enemy_distance", ":distance"),
                (neg | position_is_behind_position, pos0, pos1),
                (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 0, ":fire_order"),
                
                #behind enemy?
                (try_begin),
                  (position_is_behind_position, pos1, pos0),
                  (agent_ai_set_always_attack_in_melee, ":agent", 1),
                (else_try),
                  (agent_ai_set_always_attack_in_melee, ":agent", 0),
                (try_end),
                
              #equip longest weapon and avoid defensive
              (else_try),
                (call_script, "script_equip_best_melee_weapon_moto", ":agent", 0, 1, ":fire_order"),
                (agent_ai_set_always_attack_in_melee, ":agent", 1),
              (try_end),
            (try_end),
            
            (try_begin),
              (eq, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (val_add, ":column", 1),
            
            (gt, ":column", ":rank_dimension"),	#next rank?
            (position_move_y, pos1, ":neg_distance", 0),
            (try_begin),
              (neq, ":form_left", 1),
              (assign, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (assign, ":form_left", 0),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (assign, ":column", 1),
            (val_add, ":rank", 1),
          (try_end),
        (try_end),
      (try_end),
      
      #calculate percent in place from counts from section above (see
      #script_formation_process_agent_move)
      (store_add, ":slot", slot_team_d0_size, ":fdivision"),
      (team_get_slot, ":num_troops", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_percent_in_place, ":fdivision"),
      
      (try_begin),
        (eq, ":num_troops", 0),
        (team_set_slot, ":fteam", ":slot", 0),
      (else_try),
        (team_get_slot, reg0, ":fteam", ":slot"),
        (val_mul, reg0, 100),
        (val_div, reg0, ":num_troops"),
        (team_set_slot, ":fteam", ":slot", reg0),
      (try_end),
  ]),
  
  # script_get_default_formation by motomataru
  # Input: team id
  # Output: reg0 default formation
  ("get_default_formation_moto", [
      (store_script_param, ":fteam", 1),
      (team_get_slot, ":ffaction", ":fteam", slot_team_faction),
      (try_begin),
        (this_or_next | eq, ":ffaction", fac_player_supporters_faction),
        (eq, ":ffaction", fac_player_faction),
        (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
        (assign, ":ffaction", "$players_kingdom"),
      (try_end),
      
      (try_begin),
        (is_between, ":ffaction", "fac_player_faction", kingdoms_end),
        (faction_slot_ge, ":ffaction", slot_faction_culture, 1),
        (faction_get_slot, ":ffaction", ":ffaction", slot_faction_culture),
      (try_end),
      
      #assign default formation
      (try_begin),
		(eq, ":ffaction", "fac_gondor"),	#Gondor
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_dwarf"),	#Erebor
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_rohan"),	#Rohan
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_mordor"),	#Mordor
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_isengard"),	#Isengard
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_lorien"),	#Lorien
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_imladris"),	#Imladris
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_woodelf"),	#Mirkwood Elves
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_dale"),	#Dale
		(assign, reg0, formation_shield),
	(else_try),
		(eq, ":ffaction", "fac_harad"),	#Harad
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_rhun"),	#Rhun
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_khand"),	#Khand
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_umbar"),	#Umbar
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_moria"),	#Moria
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_guldur"),	#Dol Guldur
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_gundabad"),    #Gundabad
		(assign, reg0, formation_ranks),
	(else_try),
		(eq, ":ffaction", "fac_dunland"),	#Dunland
		(assign, reg0, formation_none),
	(else_try),
		(eq, ":ffaction", "fac_beorn"),	#Beornings
		(assign, reg0, formation_none),
	(else_try),
		(eq, ":ffaction", "fac_player_faction"),	#independent player
		(assign, reg0, formation_ranks),
	(else_try),
		(assign, reg0, formation_none),	#riffraff don't use formations
	(try_end),]),
  
  # script_switch_to_noswing_weapons by motomataru
  # Input: agent, formation spacing
  # Output: none
  ("switch_to_noswing_weapons_moto", [
      (store_script_param, ":agent", 1),
      (store_script_param, ":formation_spacing", 2),
      (try_for_range, ":item_slot", ek_item_0, ek_head),
        (agent_get_item_slot, ":item", ":agent", ":item_slot"),
        (call_script, "script_cf_is_thrusting_weapon_moto", ":item"),
        (item_get_weapon_length, ":weap_len",":item"),
        
        (try_begin),
          (ge, ":weap_len", ":formation_spacing"),	#avoid switching when weapon still has room to be swung
          (item_get_slot, ":noswing_version", ":item", slot_item_alternate),
          (gt, ":noswing_version", "itm_beorn_axe_no_attack"),
          (agent_unequip_item, ":agent", ":item", ":item_slot"),	#assumes first ek_* are the weapons
          (agent_equip_item, ":agent", ":noswing_version", ":item_slot"),	#assumes first ek_* are the weapons
          
        #undo legacy switches
        (else_try),
          (gt, ":item", "itm_beorn_axe_no_attack"),
          (item_get_slot, ":original_version", ":item", slot_item_alternate),
          (agent_unequip_item, ":agent", ":item", ":item_slot"),	#assumes first ek_* are the weapons
          (agent_equip_item, ":agent", ":original_version", ":item_slot"),	#assumes first ek_* are the weapons
        (try_end),
      (try_end),]),
  
  # script_switch_from_noswing_weapons by motomataru
  # Input: agent
  # Output: none
  ("switch_from_noswing_weapons_moto", [
      (store_script_param, ":agent", 1),
      (try_for_range, ":item_slot", ek_item_0, ek_head),
        (agent_get_item_slot, ":item", ":agent", ":item_slot"),
        (gt, ":item", "itm_beorn_axe_no_attack"),
        (item_get_slot, ":original_version", ":item", slot_item_alternate),
        (agent_unequip_item, ":agent", ":item", ":item_slot"),	#assumes first ek_* are the weapons
        (agent_equip_item, ":agent", ":original_version", ":item_slot"),	#assumes first ek_* are the weapons
      (try_end),]),
  
  # script_formation_process_agent_move by motomataru
  # Input: (pos1), team, division, agent, which rank of formation agent is in
  # Output: (pos1) may change to reference first agent's anticipated position
  # This function sets scripted destination and performs other tasks related to
  # making the formation look nice on the move (and more)
  ("formation_process_agent_move_moto", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":agent", 3),
      (store_script_param, ":rank", 4),
      
      (agent_set_scripted_destination, ":agent", pos1, 1),
      
      (agent_get_position, Current_Pos, ":agent"),
      (get_distance_between_positions, ":distance_to_go", Current_Pos, pos1),
      
      (store_add, ":slot", slot_team_d0_speed_limit, ":fdivision"),
      (team_get_slot, ":speed_limit", ":fteam", ":slot"),
      
      (agent_get_speed, Speed_Pos, ":agent"),
      (position_transform_position_to_parent, Temp_Pos, Current_Pos, Speed_Pos),
      (call_script, "script_point_y_toward_position_moto", Current_Pos, Temp_Pos),	#get direction of travel
      (store_mul, ":expected_travel", reg0, formation_reform_interval),
      (store_div, ":speed", ":expected_travel", Km_Per_Hour_To_Cm),
      
      #First Agent
      (try_begin),
        (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
        (neg | team_slot_ge, ":fteam", ":slot", 0),
        (team_set_slot, ":fteam", ":slot", ":agent"),
        
        (try_begin),	#reset speed when first member stopped
          (le, ":speed", 5),	#minimum observed speed
          (store_add, ":slot", slot_team_d0_speed_limit, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", Top_Speed),
          (agent_set_speed_limit, ":agent", Top_Speed),
          
        (else_try),	#first member in motion
          (val_mul, ":speed", 2),	#after terrain & encumbrance, agents tend to move about half their speed limit
          (try_begin),	#speed up if everyone caught up
            (store_add, ":slot", slot_team_d0_percent_in_place, ":fdivision"),
            (team_slot_ge, ":fteam", ":slot", 100),
            (try_begin),
              (ge, ":speed", ":speed_limit"),
              (val_add, ":speed_limit", 1),
            (try_end),
          (else_try),	#else slow down
            (val_min, ":speed_limit", ":speed"),
            (val_sub, ":speed_limit", 1),
            (val_max, ":speed_limit", 5),	#minimum observed speed
          (try_end),
          
          #build formation from first agent
          (store_add, ":slot", slot_team_d0_prev_first_member, ":fdivision"),
          (team_slot_eq, ":fteam", ":slot", ":agent"),	#looking at same first member as last call?
          
          (call_script, "script_battlegroup_get_position_moto", Temp_Pos, ":fteam", ":fdivision"),
          (get_distance_between_positions, ":distance_from_group", Current_Pos, Temp_Pos),
          (call_script, "script_battlegroup_get_action_radius_moto", ":fteam", ":fdivision"),
          (val_div, reg0, 2),	#function returns length of bg
          (val_sub, ":distance_from_group", reg0),
          (lt, ":distance_from_group", 2000),	#within 20m of rest of division?
          
          (store_mul, ":expected_travel", ":speed_limit", Km_Per_Hour_To_Cm),
          (lt, ":expected_travel", ":distance_to_go"),	#more than one call from destination?
          
          (store_add, ":slot", slot_team_d0_speed_limit, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", ":speed_limit"),
          (agent_set_speed_limit, ":agent", ":speed_limit"),
          
          (copy_position, Temp_Pos, Current_Pos),
          (call_script, "script_point_y_toward_position_moto", Temp_Pos, pos1),
          (position_move_y, Temp_Pos, ":expected_travel", 0),	#anticipate where first member will be next
          (position_copy_rotation, Temp_Pos, pos1),	#conserve destination facing of formation
          (copy_position, pos1, Temp_Pos),	#reference the rest of the formation to first member's anticipated position
        (try_end),
        
        (store_add, ":slot", slot_team_d0_percent_in_place, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", 1),	#reinit: always count first member as having arrived
        (store_add, ":slot", slot_team_d0_prev_first_member, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", ":agent"),
        
      #Not First Agent
      (else_try),
        (try_begin),
          (le, ":speed", 0),
          (assign, ":speed_limit", Top_Speed),
        (else_try),
          (neg | position_is_behind_position, pos1, Current_Pos),
          (store_div, ":speed_limit", ":distance_to_go", Km_Per_Hour_To_Cm),
          (val_max, ":speed_limit", 1),
        (else_try),
          (store_add, ":slot", slot_team_d0_is_fighting, ":fdivision"),
          (team_slot_eq, ":fteam", ":slot", 0),
          (assign, ":speed_limit", 1),
        (else_try),
          (assign, ":speed_limit", Top_Speed),
        (try_end),
        (agent_set_speed_limit, ":agent", ":speed_limit"),
        (try_begin),
          (this_or_next | le, ":speed", 0),	#reached previous destination or blocked OR
          (this_or_next | lt, ":speed_limit", Top_Speed),	#destination within reach OR
          (position_is_behind_position, pos1, Current_Pos),	#agent ahead of formation
          (store_add, ":slot", slot_team_d0_percent_in_place, ":fdivision"),
          (team_get_slot, reg0, ":fteam", ":slot"),
          (val_add, reg0, 1),
          (team_set_slot, ":fteam", ":slot", reg0),
        (try_end),
      (try_end),
      
      #Housekeeping
      (agent_set_slot, ":agent", slot_agent_formation_rank, ":rank"),]),
  
  # script_pick_native_formation by motomataru
  # Input: team, division
  # Output: reg0 with formation_*_row (see module_constants)
  #         reg1 with number of rows
  ("pick_native_formation_moto", [
      (store_script_param, ":team", 1),
      (store_script_param, ":division", 2),
      
      (store_add, ":slot", slot_team_d0_size, ":division"),
      (team_get_slot, ":bg_size", ":team", ":slot"),
      
      (try_begin),
        (eq, ":bg_size", 0),	#script_store_battlegroup_data is not being called
        #(team_get_leader, ":leader", ":team"),
        (call_script, "script_team_get_nontroll_leader", ":team"),
        (assign, ":leader", reg0),
        (gt, ":leader", 0),
        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member_moto", ":team", ":division", ":leader", ":agent"),
          (val_add, ":bg_size", 1),
        (try_end),
      (try_end),
      
      (call_script, "script_calculate_default_ranks_moto", ":bg_size"),
      (try_begin),
        (eq, reg1, 1),
        (assign, reg0, formation_1_row),
      (else_try),
        (eq, reg1, 2),
        (assign, reg0, formation_2_row),
      (else_try),
        (eq, reg1, 3),
        (assign, reg0, formation_3_row),
      (else_try),
        (this_or_next | eq, reg1, 4),
        (eq, Native_Formations_Implementation, WB_Implementation),
        (assign, reg0, formation_4_row),
        (assign, reg1, 4),
      (else_try),
        (assign, reg0, formation_5_row),
        (assign, reg1, 5),
      (try_end)]),
  
  # script_calculate_default_ranks by motomataru
  # Input: number of troops
  # Output: reg1 with number of rows
  # calculates number of rows closest to the old Roman 5:1 cohort arrangement
  # (80 troops in 4 rows)
  # quadratic formula to solve (5R^2 + 5(R+1)^2)/2
  ("calculate_default_ranks_moto", [
      (store_script_param, ":bg_size", 1),
      
      (val_mul, ":bg_size", 20),
      (val_sub, ":bg_size", 25),
      (convert_to_fixed_point, ":bg_size"),
      (store_sqrt, reg1, ":bg_size"),
      (convert_from_fixed_point, reg1),
      (val_sub, reg1, 5),
      (val_div, reg1, 10),
      (val_add, reg1, 1),]),
  
  # script_get_centering_amount by motomataru
  # Input: formation type, number of troops, extra spacing
  #        Use formation type formation_default to use script for archer line
  # Output: reg0 number of centimeters to adjust x-position to center formation
  ("get_centering_amount_moto", [
      (store_script_param, ":troop_formation", 1),
      (store_script_param, ":num_troops", 2),
      (store_script_param, ":extra_spacing", 3),
      (store_mul, ":troop_space", ":extra_spacing", 50),
      (val_add, ":troop_space", formation_minimum_spacing),
      (assign, reg0, 0),
      (try_begin),
        (eq, ":troop_formation", formation_square),
        (convert_to_fixed_point, ":num_troops"),
        (store_sqrt, reg0, ":num_troops"),
        (convert_from_fixed_point, reg0),
        (val_mul, reg0, ":troop_space"),
        # (val_sub, reg0, ":troop_space"), MOTO not needed because column added in
        # script_form_infantry
      (else_try),
        (this_or_next | eq, ":troop_formation", formation_ranks),
        (eq, ":troop_formation", formation_shield),
        (call_script, "script_calculate_default_ranks_moto", ":num_troops"),
        (assign, ":num_ranks", reg1),
        (store_div, reg0, ":num_troops", ":num_ranks"),
        (try_begin),
          (store_mod, reg1, ":num_troops", ":num_ranks"),
          (eq, reg1, 0),
          (val_sub, reg0, 1),
        (try_end),
        (val_mul, reg0, ":troop_space"),
      (else_try),
        (eq, ":troop_formation", formation_default),	#assume these are archers in a line
        (store_mul, reg0, ":num_troops", ":troop_space"),
      (try_end),
      (val_div, reg0, 2),]),
  
  # script_formation_end
  # Input: team, division
  # Output: none
  ("formation_end_moto", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (try_begin),
        (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
        (neg | team_slot_eq, ":fteam", ":slot", formation_none),
        (team_slot_ge, ":fteam", ":slot", formation_none),
        
        (try_begin),
          (eq, Native_Formations_Implementation, WFaS_Implementation),
          (team_set_slot, ":fteam", ":slot", formation_2_row),
        (else_try),
          (team_set_slot, ":fteam", ":slot", formation_none),
        (try_end),
        
        #(team_get_leader, ":leader", ":fteam"),
        (call_script, "script_team_get_nontroll_leader", ":fteam"),
        (assign, ":leader", reg0),
        (gt, ":leader", 0),
        
        (try_for_agents, ":agent"),
          (agent_is_alive, ":agent"),
          (agent_is_human, ":agent"),
          (agent_get_group, ":team", ":agent"),
          (eq, ":team", ":fteam"),
          (neq, ":leader", ":agent"),
          (agent_get_division, ":bgdivision", ":agent"),
          (eq, ":bgdivision", ":fdivision"),
          (agent_clear_scripted_mode, ":agent"),
          #(call_script, "script_switch_from_noswing_weapons_moto", ":agent"),
          (agent_ai_set_always_attack_in_melee, ":agent", 0),
          (agent_set_speed_limit, ":agent", 100),
          (agent_set_slot, ":agent", slot_agent_formation_rank, 0),
          (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
        (try_end),
        
        (try_begin),
          (eq, ":fteam", "$fplayer_team_no"),
          (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
          
          #adjust for differences between the systems of spreading out (Native spreads
          #out about twice as much)
          (try_begin),
            (eq, Native_Formations_Implementation, WFaS_Implementation),
            (assign, ":max_spacing", 3),
          (else_try),
            (assign, ":max_spacing", 2),
          (try_end),
          
          (store_mul, ":double_max", ":max_spacing", 2),
          
          (try_begin),
            (ge, ":div_spacing", ":double_max"),	#beyond Native max
            (assign, ":div_spacing", ":max_spacing"),
          (else_try),
            (gt, ":div_spacing", 0),
            (set_show_messages, 0),
            (team_give_order, "$fplayer_team_no", ":fdivision", mordr_stand_closer),
            (set_show_messages, 1),
            (val_div, ":div_spacing", 2),
          (try_end),
          
          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),
        (try_end),
      (try_end),]),
  
  # script_formation_move_position by motomataru
  # Input: team, division, formation current position, (1 to advance or -1 to
  # withdraw or 0 to redirect)
  # Output: pos1 (offset for centering)
  ("formation_move_position_moto", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fcurrentpos", 3),
      (store_script_param, ":direction", 4),
      (copy_position, pos1, ":fcurrentpos"),
      (call_script, "script_team_get_position_of_enemies_moto", Enemy_Team_Pos_MOTO, ":fteam", grc_everyone),
      (try_begin),
        (neq, reg0, 0),	#more than 0 enemies still alive?
        (copy_position, pos1, ":fcurrentpos"),	#restore current formation "position"
        (call_script, "script_point_y_toward_position_moto", pos1, Enemy_Team_Pos_MOTO),	#record angle from center to enemy
        (assign, ":distance_to_enemy", reg0),
        (call_script, "script_get_formation_destination_moto", pos61, ":fteam", ":fdivision"),
        (get_distance_between_positions, ":move_amount", pos1, pos61),	#distance already moving from previous orders
        (val_add, ":move_amount", 1000),
        (try_begin),
          (gt, ":direction", 0),	#moving forward?
          (gt, ":move_amount", ":distance_to_enemy"),
          (assign, ":move_amount", ":distance_to_enemy"),
        (try_end),
        (val_mul, ":move_amount", ":direction"),
        (position_move_y, pos1, ":move_amount", 0),
        (position_get_x, ":from_x", pos1),
        (position_get_y, ":from_y", pos1),
        (try_begin),
          (is_between, ":from_x", "$g_bound_left", "$g_bound_right"),
          (is_between, ":from_y", "$g_bound_bottom", "$g_bound_top"),
          (try_begin),
            (lt, ":distance_to_enemy", 1000),	#less than a move away?
            (position_copy_rotation, pos1, pos61),	#avoid rotating formation
          (try_end),
          (call_script, "script_set_formation_destination_moto", ":fteam", ":fdivision", pos1),
          (store_add, ":slot", slot_team_d0_size, ":fdivision"),
          (team_get_slot, ":num_troops", ":fteam", ":slot"),
          (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
          (team_get_slot, ":formation_extra_spacing", ":fteam", ":slot"),
          (try_begin),
            (store_add, ":slot", slot_team_d0_type, ":fdivision"),
            (neg | team_slot_eq, ":fteam", ":slot", sdt_archer),
            (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
            (team_get_slot, ":fformation", ":fteam", ":slot"),
            (call_script, "script_get_centering_amount_moto", ":fformation", ":num_troops", ":formation_extra_spacing"),
          (else_try),
            (call_script, "script_get_centering_amount_moto", formation_default, ":num_troops", ":formation_extra_spacing"),
            (val_mul, reg0, -1),
          (try_end),
          (position_move_x, pos1, reg0, 0),
          
          #out of bounds
        (else_try),
          (copy_position, pos1, ":fcurrentpos"),	#restore current formation "position"
        (try_end),
      (try_end),]),
  
  # script_cf_battlegroup_valid_formation
  # Input: team, division, formation
  # Output: reg0: troop count/1 if too few troops/0 if wrong type
  ("cf_battlegroup_valid_formation_moto", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fformation", 3),
      
      (assign, ":valid_type", 0),
      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (team_get_slot, ":sd_type", ":fteam", ":slot"),
      (try_begin), #Eventually make this more complex with the sub-divisions
        (this_or_next | eq, ":sd_type", sdt_cavalry),
        (eq, ":sd_type", sdt_harcher),
        (assign, ":size_minimum", formation_min_cavalry_troops),
        (try_begin),
          (eq, ":fformation", formation_wedge),
          (assign, ":valid_type", 1),
        (try_end),
      (else_try),
        (eq, ":sd_type", sdt_archer),
        (assign, ":size_minimum", formation_min_foot_troops),
        (try_begin),
          # (this_or_next|eq, ":fformation", formation_ranks), uncheck for proper
          # ranks
          (eq, ":fformation", formation_default),
          (assign, ":valid_type", 1),
        (try_end),
      (else_try),
        (assign, ":size_minimum", formation_min_foot_troops),
        (gt, ":fformation", formation_none),
        (assign, ":valid_type", 1), #all types valid
      (try_end),
      
      (try_begin),
        (eq, ":valid_type", 0),
        (assign, ":num_troops", 0),
      (else_try),
        (store_add, ":slot", slot_team_d0_size, ":fdivision"),
        (team_get_slot, ":num_troops", ":fteam", ":slot"),
        (lt, ":num_troops", ":size_minimum"),
        (assign, ":num_troops", 1),
      (try_end),
      
      (assign, reg0, ":num_troops"),
      (gt, ":num_troops", 1)]),
  
  # script_cf_valid_formation_member by motomataru #CABA - Modified for
  # Classify_agent phase out
  # Input: team, division, agent number of team leader, test agent
  # Output: failure indicates agent is not member of formation
  ("cf_valid_formation_member_moto", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      (store_script_param, ":agent", 4),
      (neq, ":fleader", ":agent"),
      (agent_get_division, ":bgdivision", ":agent"),
      (eq, ":bgdivision", ":fdivision"),
      (agent_get_group, ":team", ":agent"),
      (eq, ":team", ":fteam"),
      (agent_is_alive, ":agent"),
      (agent_is_human, ":agent"),
      (agent_slot_eq, ":agent", slot_agent_is_running_away, 0),]),
  
  # #Player team formations functions
  # script_player_attempt_formation
  # Inputs: arg1: division
  #			arg2: formation identifier (formation_*)
  #         arg3: flag 1 to form at current location (rather than next to
  #         player), flag 2 to form as if player were at Target_Pos
  # Output: none
  # Designed JUST for infantry
  ("player_attempt_formation_moto", [
      (store_script_param, ":fdivision", 1),
      (store_script_param, ":fformation", 2),
      (store_script_param, ":form_on_spot", 3),
      (set_fixed_point_multiplier, 100),
      (try_begin),
        (eq, ":fformation", formation_ranks),
        (str_store_string, s1, "@ranks"),
      (else_try),
        (eq, ":fformation", formation_shield),
        (str_store_string, s1, "@shield wall"),
      (else_try),
        (eq, ":fformation", formation_wedge),
        (str_store_string, s1, "@wedge"),
      (else_try),
        (eq, ":fformation", formation_square),
        (str_store_string, s1, "@square"),
      (else_try),
        (str_store_string, s1, "@up"),
      (try_end),
      (str_store_class_name, s2, ":fdivision"),
      
      (try_begin),
        (call_script, "script_cf_battlegroup_valid_formation_moto", "$fplayer_team_no", ":fdivision", ":fformation"),
        (try_begin),	#new formation?
          (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
          (neg | team_slot_eq, "$fplayer_team_no", ":slot", ":fformation"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":fformation"),
          (store_add, reg1, ":fdivision", 1),
          (display_message, "@Division {reg1} {s2} forming {s1}."),
          (store_add, ":slot", slot_team_d0_fclock, ":fdivision"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_target_team, ":fdivision"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          
          (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
          
          #bring unformed divisions into sync with formations' minimum
          (set_show_messages, 0),
          (assign, reg0, ":div_spacing"),
          (try_for_range, reg1, reg0, formation_start_spread_out),	#spread out for ease of forming up
            (team_give_order, "$fplayer_team_no", ":fdivision", mordr_spread_out),
            (val_add, ":div_spacing", 1),
          (try_end),
          (set_show_messages, 1),
          
          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),
        (try_end),
        
        #divisions must stop to order themselves
        (store_add, ":slot", slot_team_d0_move_order, ":fdivision"),
        (team_get_slot, ":div_order", "$fplayer_team_no", ":slot"),
        (try_begin),
          (this_or_next | eq, ":div_order", mordr_stand_ground),
          (this_or_next | eq, ":div_order", mordr_charge),
          (eq, ":div_order", mordr_retreat),
          (call_script, "script_battlegroup_get_position_moto", pos1, "$fplayer_team_no", ":fdivision"),
          (team_give_order, "$fplayer_team_no", ":fdivision", mordr_hold),
          (call_script, "script_set_formation_destination_moto", "$fplayer_team_no", ":fdivision", pos1),
        (try_end),
        
      (else_try),
        (assign, ":return_val", reg0),
        (call_script, "script_formation_end_moto", "$fplayer_team_no", ":fdivision"),
        (gt, ":fformation", formation_none),
        (store_add, reg1, ":fdivision", 1),
        (try_begin),
          (gt, ":return_val", 0),
          (display_message, "@Not enough troops in division {reg1} {s2} to form {s1}."),
        (else_try),
          (store_add, ":slot", slot_team_d0_type, ":fdivision"),
          (team_get_slot, reg0, "$fplayer_team_no", ":slot"),
          (call_script, "script_str_store_division_type_name_moto", s3, reg0),
          (display_message, "@Division {reg1} {s2} is an {s3} division and cannot form {s1}."),
        (try_end),
      (try_end),
      
      (try_begin),
        (eq, ":form_on_spot", 0),
        (call_script, "script_battlegroup_place_around_leader_moto", "$fplayer_team_no", ":fdivision", "$fplayer_agent_no"),
      (else_try),
        (eq, ":form_on_spot", 2),
        (copy_position, pos1, Target_Pos),
        (call_script, "script_battlegroup_place_around_pos1_moto", "$fplayer_team_no", ":fdivision", "$fplayer_agent_no"),
      (try_end),]),
  
  # script_player_formation_end
  # Input: division
  # Output: none
  ("player_formation_end_moto", [
      (store_script_param, ":fdivision", 1),
      
      (call_script, "script_formation_end_moto", "$fplayer_team_no", ":fdivision"),
      
      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (str_store_class_name, s1, ":fdivision"),
      (try_begin),
        (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_infantry),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_polearm),
        (display_message, "@{s1}: infantry formation disassembled."),
      (else_try),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
        (display_message, "@{s1}: archer formation disassembled."),
      (else_try),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_skirmisher),
        (display_message, "@{s1}: skirmisher formation disassembled."),
      (else_try),
        (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
        (display_message, "@{s1}: cavalry formation disassembled."),
      (else_try),
        (display_message, "@{s1}: formation disassembled."),
      (try_end),]),
  
  # script_player_order_formations by motomataru TODO add native weapon
  # commands
  # Inputs: arg1: order to formation (mordr_*)
  # Output: none
  ("player_order_formations_moto", [
      (store_script_param, ":forder", 1),
      (set_fixed_point_multiplier, 100),
      
      (try_begin), #On hold, any formations reform in new location
        (eq, ":forder", mordr_hold),
        (call_script, "script_division_reset_places_moto"),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_size, ":division"),	#apply to all divisions (not just formations)
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (call_script, "script_player_attempt_formation_moto", ":division", ":formation", 0),
        (try_end),
        
      (else_try),	#Follow is hold repeated frequently
        (eq, ":forder", mordr_follow),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_size, ":division"),	#apply to all divisions (not just formations)
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),
          
          (store_add, ":slot", slot_team_d0_formation, ":division"),	#update formations
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (call_script, "script_player_attempt_formation_moto", ":division", ":formation", 0),
          
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":forder"),
        (try_end),
        
      (else_try),	#charge or retreat ends formation
        (this_or_next | eq, ":forder", mordr_charge),
        (eq, ":forder", mordr_retreat),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":forder"),
          
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (gt, ":formation", formation_none),
          (call_script, "script_player_formation_end_moto", ":division"),
        (try_end),
        
      (else_try),
        (eq, ":forder", mordr_form_1_row),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":formation", formation_none),
            (call_script, "script_formation_end_moto", "$fplayer_team_no", ":division"),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", formation_1_row),
          (store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
        (try_end),
        
      (else_try),
        (eq, ":forder", mordr_form_2_row),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":formation", formation_none),
            (call_script, "script_formation_end_moto", "$fplayer_team_no", ":division"),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", formation_2_row),
          (store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 2),
        (try_end),
        
      (else_try),
        (eq, ":forder", mordr_form_3_row),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":formation", formation_none),
            (call_script, "script_formation_end_moto", "$fplayer_team_no", ":division"),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", formation_3_row),
          (store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 3),
        (try_end),
        
      (else_try),
        (eq, ":forder", mordr_form_4_row),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":formation", formation_none),
            (call_script, "script_formation_end_moto", "$fplayer_team_no", ":division"),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", formation_4_row),
          (store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 4),
        (try_end),
        
      (else_try),
        (eq, ":forder", mordr_form_5_row),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":formation", formation_none),
            (call_script, "script_formation_end_moto", "$fplayer_team_no", ":division"),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", formation_5_row),
          (store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 5),
        (try_end),
        
      (else_try),	#dismount ends formation
        (eq, ":forder", mordr_dismount),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (neg | team_slot_eq, "$fplayer_team_no", ":slot", formation_none),
          (team_slot_ge, "$fplayer_team_no", ":slot", formation_none),
          (try_begin),
            (store_add, ":slot", slot_team_d0_type, ":division"),
            (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
            (call_script, "script_formation_end_moto", "$fplayer_team_no", ":division"),
            (display_message, "@Cavalry formation disassembled."),
            
          (else_try),	#address bug that cavalry in scripted mode won't dismount
            (try_for_agents, ":agent"),
              (agent_is_alive, ":agent"),
              (agent_is_human, ":agent"),
              (agent_get_group, ":team", ":agent"),
              (eq, ":team", "$fplayer_team_no"),
              (neq, "$fplayer_agent_no", ":agent"),
              (agent_get_division, ":bgdivision", ":agent"),
              (eq, ":bgdivision", ":division"),
              (agent_clear_scripted_mode, ":agent"),
              (agent_set_speed_limit, ":agent", 100),
            (try_end),
          (try_end),
        (try_end),
        
      (else_try),
        (eq, ":forder", mordr_advance),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_get_slot, ":prev_order", "$fplayer_team_no", ":slot"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":forder"),
          
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (gt, ":formation", formation_none),
          
          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          
          (call_script, "script_formation_current_position_moto", pos63, "$fplayer_team_no", ":division"),
          (try_begin),
            (neq, ":prev_order", mordr_advance),
            (call_script, "script_set_formation_destination_moto", "$fplayer_team_no", ":division", pos63),
          (try_end),
          (call_script, "script_formation_move_position_moto", "$fplayer_team_no", ":division", pos63, 1),
          
          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (try_begin),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
            (call_script, "script_form_archers_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":formation"),
          (else_try),
            (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
            (call_script, "script_form_cavalry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0),
          (else_try),
            (call_script, "script_form_infantry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":formation"),
          (try_end),
        (try_end),
        
      (else_try),
        (eq, ":forder", mordr_fall_back),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_get_slot, ":prev_order", "$fplayer_team_no", ":slot"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":forder"),
          
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (gt, ":formation", formation_none),
          
          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          
          (call_script, "script_formation_current_position_moto", pos63, "$fplayer_team_no", ":division"),
          (try_begin),
            (neq, ":prev_order", mordr_fall_back),
            (call_script, "script_set_formation_destination_moto", "$fplayer_team_no", ":division", pos63),
          (try_end),
          (call_script, "script_formation_move_position_moto", "$fplayer_team_no", ":division", pos63, -1),
          
          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (try_begin),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
            (call_script, "script_form_archers_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":formation"),
          (else_try),
            (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
            (call_script, "script_form_cavalry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0),
          (else_try),
            (call_script, "script_form_infantry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":formation"),
          (try_end),
        (try_end),
        
      (else_try),
        (eq, ":forder", mordr_stand_closer),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          
          (try_begin),
            (eq, Native_Formations_Implementation, WB_Implementation),
            (assign, ":min_spacing", -3),	#WB formations go down to four ranks by using Stand Closer
          (else_try),
            (assign, ":min_spacing", 0),
          (try_end),
          
          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
          (gt, ":div_spacing", ":min_spacing"),
          (val_sub, ":div_spacing", 1),
          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),
          
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (gt, ":formation", formation_none),
          
          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          
          (try_begin),	#bring unformed divisions into sync with formations' minimum
            (lt, ":div_spacing", 0),
            (set_show_messages, 0),
            (assign, reg0, ":div_spacing"),
            (try_for_range, reg1, reg0, 0),
              (team_give_order, "$fplayer_team_no", ":division", mordr_spread_out),
              (val_add, ":div_spacing", 1),
            (try_end),
            (set_show_messages, 1),
            (store_add, ":slot", slot_team_d0_formation_space, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),
            
          (else_try),
            (call_script, "script_get_formation_destination_moto", pos1, "$fplayer_team_no", ":division"),
            (try_begin),
              (store_add, ":slot", slot_team_d0_first_member, ":division"),
              (team_slot_eq, "$fplayer_team_no", ":slot", "$fplayer_agent_no"),
              (assign, ":first_member_is_player", 1),
            (else_try),
              (assign, ":first_member_is_player", 0),
            (try_end),
            (store_add, ":slot", slot_team_d0_type, ":division"),
            (try_begin),
              (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
              (store_add, ":slot", slot_team_d0_size, ":division"),
              (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
              (call_script, "script_get_centering_amount_moto", formation_default, ":troop_count", ":div_spacing"),
              (val_mul, reg0, -1),
              (position_move_x, pos1, reg0),
              (call_script, "script_form_archers_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
            (else_try),
              (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
              (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
              (call_script, "script_form_cavalry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player"),
            (else_try),
              (store_add, ":slot", slot_team_d0_size, ":division"),
              (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
              (call_script, "script_get_centering_amount_moto", ":formation", ":troop_count", ":div_spacing"),
              (position_move_x, pos1, reg0),
              (call_script, "script_form_infantry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
            (try_end),
          (try_end),
        (try_end),
        
      (else_try),
        (eq, ":forder", mordr_spread_out),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          
          (try_begin),
            (eq, Native_Formations_Implementation, WFaS_Implementation),
            (assign, ":max_spacing", 3),
          (else_try),
            (assign, ":max_spacing", 2),
          (try_end),
          
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
          (try_begin),
            (this_or_next | lt, ":div_spacing", ":max_spacing"),
            (gt, ":formation", formation_none),
            (val_add, ":div_spacing", 1),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),
          
          (gt, ":formation", formation_none),
          
          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          
          #bring unformed divisions into sync with formations' minimum
          (set_show_messages, 0),
          (assign, reg0, ":div_spacing"),
          (try_for_range, reg1, reg0, 1),
            (team_give_order, "$fplayer_team_no", ":division", mordr_spread_out),
            (val_add, ":div_spacing", 1),
          (try_end),
          (set_show_messages, 1),
          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),
          
          (call_script, "script_get_formation_destination_moto", pos1, "$fplayer_team_no", ":division"),
          (try_begin),
            (store_add, ":slot", slot_team_d0_first_member, ":division"),
            (team_slot_eq, "$fplayer_team_no", ":slot", "$fplayer_agent_no"),
            (assign, ":first_member_is_player", 1),
          (else_try),
            (assign, ":first_member_is_player", 0),
          (try_end),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (try_begin),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
            (call_script, "script_get_centering_amount_moto", formation_default, ":troop_count", ":div_spacing"),
            (val_mul, reg0, -1),
            (position_move_x, pos1, reg0),
            (call_script, "script_form_archers_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
          (else_try),
            (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
            (call_script, "script_form_cavalry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player"),
          (else_try),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
            (call_script, "script_get_centering_amount_moto", ":formation", ":troop_count", ":div_spacing"),
            (position_move_x, pos1, reg0),
            (call_script, "script_form_infantry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
          (try_end),
        (try_end),
        
      (else_try),
        (eq, ":forder", mordr_stand_ground),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":forder"),
          
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (gt, ":formation", formation_none),
          
          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          
          (call_script, "script_formation_current_position_moto", pos63, "$fplayer_team_no", ":division"),
          (copy_position, pos1, pos63),
          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
          
          (try_begin),
            (store_add, ":slot", slot_team_d0_first_member, ":division"),
            (team_slot_eq, "$fplayer_team_no", ":slot", "$fplayer_agent_no"),
            (assign, ":first_member_is_player", 1),
          (else_try),
            (assign, ":first_member_is_player", 0),
          (try_end),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (try_begin),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
            (call_script, "script_get_centering_amount_moto", formation_default, ":troop_count", ":div_spacing"),
            (val_mul, reg0, -1),
            (position_move_x, pos1, reg0),
            (call_script, "script_form_archers_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
          (else_try),
            (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
            (call_script, "script_form_cavalry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player"),
          (else_try),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
            (call_script, "script_get_centering_amount_moto", ":formation", ":troop_count", ":div_spacing"),
            (position_move_x, pos1, reg0),
            (call_script, "script_form_infantry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
          (try_end),
          (call_script, "script_set_formation_destination_moto", "$fplayer_team_no", ":division", pos63),
        (try_end),
      (try_end)]),
  
  # script_memorize_division_placements by motomataru
  # Inputs: none
  # Output: none
  ("memorize_division_placements_moto", [
      (set_fixed_point_multiplier, 100),
      (call_script, "script_team_get_position_of_enemies_moto", Enemy_Team_Pos_MOTO, "$fplayer_team_no", grc_everyone),
      (assign, ":num_enemies", reg0),
      
      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),
        
        (store_add, ":slot", slot_team_d0_formation, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_faction_d0_mem_formation, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),
        
        (store_add, ":slot", slot_team_d0_formation_space, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_faction_d0_mem_formation_space, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),
        
        (agent_get_position, pos1, "$fplayer_agent_no"),
        (try_begin),
          (neq, ":num_enemies", 0),	#more than 0 enemies still alive?
          (call_script, "script_point_y_toward_position_moto", pos1, Enemy_Team_Pos_MOTO),
        (try_end),
        # (call_script, "script_get_formation_destination_moto", Current_Pos,
        # "$fplayer_team_no", ":division"),
        (team_get_order_position, Current_Pos, "$fplayer_team_no", ":division"),	#use this to capture Native Advance and Fall Back positioning
        (position_transform_position_to_local, Temp_Pos, pos1, Current_Pos), #Temp_Pos = vector to division w.r.t.  leader facing enemy
        
        (position_get_x, ":value", Temp_Pos),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),
        
        (position_get_y, ":value", Temp_Pos),
        (store_add, ":slot", slot_faction_d0_mem_relative_y, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),
        
        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (call_script, "script_str_store_division_type_name_moto", s1, ":value"),
        (store_add, reg0, ":division", 1),
        (display_message, "@The placement of {s1} division {reg0} memorized."),
      (try_end),]),
  
  # script_default_division_placements by motomataru
  # Inputs: none
  # Output: none
  ("default_division_placements_moto", [
      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":division"),	#use as flag
        (faction_set_slot, "fac_player_faction", ":slot", 0),
        
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),
        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (call_script, "script_str_store_division_type_name_moto", s1, ":value"),
        (store_add, reg0, ":division", 1),
        (display_message, "@The placement of {s1} division {reg0} set to default."),
      (try_end),]),
  
  # script_process_place_divisions by motomataru
  # Inputs: none
  # Output: none
  # Expects team_set_order_position has been done
  ("process_place_divisions_moto", [
      (assign, ":num_bgroups", 0),
      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_team_d0_target_team, ":division"),
        (team_set_slot, "$fplayer_team_no", ":slot", -1),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),
        (store_add, ":slot", slot_team_d0_fclock, ":division"),
        (team_set_slot, "$fplayer_team_no", ":slot", 1),
        (team_get_order_position, pos1, "$fplayer_team_no", ":division"),
        (val_add, ":num_bgroups", 1),
      (try_end),
      
      (try_begin),
        (gt, ":num_bgroups", 0),
        (copy_position, Target_Pos, pos1),	#kludge around team_get_order_position rotation problems
        
        (try_begin),
          (eq, "$battle_phase", BP_Deploy),
          
          (try_begin),
            (party_get_skill_level, reg0, "p_main_party", "skl_tactics"),
          (try_end),
          (store_mul, ":range_limit", reg0, 1000),
          
          (agent_get_position, Temp_Pos, "$fplayer_agent_no"),
          (get_distance_between_positions, reg0, Target_Pos, Temp_Pos),
          (lt, ":range_limit", reg0),
          (display_message, "@Your party's tactical skill limits how far away you can deploy your troops!"),
          (call_script, "script_point_y_toward_position_moto", Temp_Pos, Target_Pos),
          (copy_position, Target_Pos, Temp_Pos),
          (position_move_y, Target_Pos, ":range_limit"),
        (try_end),
        
        #player designating target battlegroup?
        (assign, ":distance_to_enemy", Far_Away),
        (try_for_range, ":team", 0, 4),
          (teams_are_enemies, ":team", "$fplayer_team_no"),
          (team_slot_ge, ":team", slot_team_size, 1),
          (try_for_range, ":division", 0, 9),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_slot_ge, ":team", ":slot", 1),
            (call_script, "script_battlegroup_get_position_moto", Temp_Pos, ":team", ":division"),
            (get_distance_between_positions, reg0, Target_Pos, Temp_Pos),
            (gt, ":distance_to_enemy", reg0),
            (assign, ":distance_to_enemy", reg0),
            (assign, ":closest_enemy_team", ":team"),
            (assign, ":closest_enemy_division", ":division"),
          (try_end),
        (try_end),
        
        (call_script, "script_battlegroup_get_action_radius_moto", ":closest_enemy_team", ":closest_enemy_division"),
        (assign, ":radius_enemy_battlegroup", reg0),
        
        (try_begin),
          (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
          (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
          #selecting them
          (call_script, "script_battlegroup_get_position_moto", Target_Pos, ":closest_enemy_team", ":closest_enemy_division"),
          (gt, ":num_bgroups", 1),
          (store_add, ":slot", slot_team_d0_type, ":closest_enemy_division"),
          (team_get_slot, reg0, ":closest_enemy_team", ":slot"),
          (call_script, "script_str_store_division_type_name_moto", s1, reg0),
          (display_message, "@...and attack enemy {s1} division!"),
        (try_end),
        
        (call_script, "script_team_get_position_of_enemies_moto", Enemy_Team_Pos_MOTO, "$fplayer_team_no", grc_everyone),
        (call_script, "script_point_y_toward_position_moto", Target_Pos, Enemy_Team_Pos_MOTO),
        
        #place player divisions
        (agent_get_position, pos49, "$fplayer_agent_no"),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
          (gt, ":troop_count", 0),
          
          (try_begin),
            (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
            (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
            #selecting them
            (store_add, ":slot", slot_team_d0_target_team, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":closest_enemy_team"),
            (store_add, ":slot", slot_team_d0_target_division, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":closest_enemy_division"),
          (try_end),
          
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":fformation", "$fplayer_team_no", ":slot"),
          
          (try_begin),
            (gt, ":num_bgroups", 1),
            (agent_set_position, "$fplayer_agent_no", Target_Pos),	#fake out script_battlegroup_place_around_leader
            (call_script, "script_player_attempt_formation_moto", ":division", ":fformation", 0),
          (else_try),
            (try_begin),
              (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
              (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
              #selecting them
              (call_script, "script_battlegroup_get_attack_destination_moto", Target_Pos, "$fplayer_team_no", ":division", ":closest_enemy_team", ":closest_enemy_division"),
              (store_add, ":slot", slot_team_d0_type, ":closest_enemy_division"),
              (team_get_slot, reg0, ":closest_enemy_team", ":slot"),
              (call_script, "script_str_store_division_type_name_moto", s1, reg0),
              (display_message, "@...and attack enemy {s1} division!"),
            (try_end),
            
            (call_script, "script_set_formation_destination_moto", "$fplayer_team_no", ":division", Target_Pos),
            
            (gt, ":fformation", formation_none),
            (store_add, ":slot", slot_team_d0_formation_space, ":division"),
            (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
            (try_begin),
              (store_add, ":slot", slot_team_d0_type, ":division"),
              (team_get_slot, ":sd_type", "$fplayer_team_no", ":slot"),
              (neq, ":sd_type", sdt_cavalry),
              (neq, ":sd_type", sdt_harcher),
              (try_begin),
                (eq, ":sd_type", sdt_archer),
                (call_script, "script_get_centering_amount_moto", formation_default, ":troop_count", ":div_spacing"),
                (val_mul, reg0, -1),
                (assign, ":script", "script_form_archers_moto"),
              (else_try),
                (call_script, "script_get_centering_amount_moto", ":fformation", ":troop_count", ":div_spacing"),
                (assign, ":script", "script_form_infantry_moto"),
              (try_end),
              (position_move_x, Target_Pos, reg0),
            (else_try),
              (assign, ":script", "script_form_cavalry_moto"),
            (try_end),
            (copy_position, pos1, Target_Pos),
            (call_script, ":script", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":fformation"),
          (try_end),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_hold),
        (try_end), #division loop
        (agent_set_position, "$fplayer_agent_no", pos49),
      (try_end),	#num_bgroups > 0
  ]),
  
  # script_process_player_division_positioning by motomataru
  # Inputs: none
  # Output: none
  # Expects Enemy_Team_Pos_MOTO
  ("process_player_division_positioning_moto", [
      (call_script, "script_division_reset_places_moto"),
      
      #implement HOLD OVER THERE when player lets go of key
      (try_begin),
        (ge, "$gk_order_hold_over_there", HOT_F1_held),
        (neg | game_key_is_down, gk_order_1),
        (assign, "$gk_order_hold_over_there", HOT_no_order),
        (call_script, "script_process_place_divisions_moto"),
      (try_end),	#HOLD OVER THERE
      
      #periodic functions
      (assign, ":save_autorotate", "$FormAI_autorotate"),
      (assign, "$FormAI_autorotate", 0),
      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
        (gt, ":troop_count", 0),
        
        (store_add, ":slot", slot_team_d0_target_team, ":division"),
        (team_get_slot, ":target_team", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_team_d0_target_division, ":division"),
        (team_get_slot, ":target_division", "$fplayer_team_no", ":slot"),
        (try_begin),
          (ge, ":target_team", 0),	#enemy battlegroup targeted?
          (store_add, ":slot", slot_team_d0_size, ":target_division"),
          (team_get_slot, reg0, ":target_team", ":slot"),
          
          (le, reg0, 0),	#target destroyed?
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          
          (store_add, ":slot", slot_team_d0_type, ":target_division"),
          (team_get_slot, reg0, ":target_team", ":slot"),
          (call_script, "script_str_store_division_type_name_moto", s1, reg0),
          
          (str_store_class_name, s2, ":division"),
          (display_message, "@{s2}: returning after destroying enemy {s1} division."),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),
        (try_end),
        
        (store_add, ":slot", slot_team_d0_fclock, ":division"),
        (team_get_slot, ":fclock_moto", "$fplayer_team_no", ":slot"),
        (store_mod, ":time_slice", ":fclock_moto", Reform_Trigger_Modulus),
        (val_add, ":fclock_moto", 1),
        (team_set_slot, "$fplayer_team_no", ":slot", ":fclock_moto"),
        
        (try_begin),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_slot_eq, "$fplayer_team_no", ":slot", mordr_follow),
          (call_script, "script_battlegroup_place_around_leader_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),	#override script_battlegroup_place_around_leader
          
        #periodically reform
        (else_try),
          (eq, ":time_slice", 0),
          (team_get_movement_order, reg0, "$fplayer_team_no", ":division"),
          (neq, reg0, mordr_stand_ground),
          
          (call_script, "script_team_get_position_of_enemies_moto", Enemy_Team_Pos_MOTO, "$fplayer_team_no", grc_everyone),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":fformation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":fformation", formation_none),
            (store_add, ":slot", slot_team_d0_formation_space, ":division"),
            (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
            (store_add, ":slot", slot_team_d0_type, ":division"),
            (team_get_slot, ":sd_type", "$fplayer_team_no", ":slot"),
            
            (try_begin),
              (store_add, ":slot", slot_team_d0_first_member, ":division"),
              (team_slot_eq, "$fplayer_team_no", ":slot", "$fplayer_agent_no"),
              (assign, ":first_member_is_player", 1),
            (else_try),
              (assign, ":first_member_is_player", 0),
            (try_end),
            
            (try_begin),
              (ge, ":target_team", 0),	#enemy battlegroup targeted?
              (try_begin),
                (this_or_next | eq, ":sd_type", sdt_archer),
                (this_or_next | eq, ":sd_type", sdt_harcher),
                (eq, ":sd_type", sdt_skirmisher),
                (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
                (team_slot_ge, "$fplayer_team_no", ":slot", 1),	#ranged are firing?
                (call_script, "script_formation_current_position_moto", pos1, "$fplayer_team_no", ":division"),	#stop advancing
              (else_try),
                (call_script, "script_battlegroup_get_attack_destination_moto", pos1, "$fplayer_team_no", ":division", ":target_team", ":target_division"),
              (try_end),
              
            (else_try),
              (call_script, "script_get_formation_destination_moto", pos1, "$fplayer_team_no", ":division"),
              (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
              (team_get_slot, ":is_fighting", "$fplayer_team_no", ":slot"),
              (try_begin),
                (neq, ":sd_type", sdt_cavalry),
                (neq, ":sd_type", sdt_harcher),
                (neq, ":is_fighting", 0),
                (eq, ":first_member_is_player", 0),
                (position_move_y, pos1, -2000),
              (try_end),
              (call_script, "script_point_y_toward_position_moto", pos1, Enemy_Team_Pos_MOTO),
              (try_begin),
                (neq, ":sd_type", sdt_cavalry),
                (neq, ":sd_type", sdt_harcher),
                (neq, ":is_fighting", 0),
                (eq, ":first_member_is_player", 0),
                (position_move_y, pos1, 2000),
              (try_end),
            (try_end),
            
            (call_script, "script_set_formation_destination_moto", "$fplayer_team_no", ":division", pos1),
            
            (try_begin),
              (eq, ":sd_type", sdt_archer),
              (call_script, "script_get_centering_amount_moto", formation_default, ":troop_count", ":div_spacing"),
              (val_mul, reg0, -1),
              (position_move_x, pos1, reg0),
            (else_try),
              (neq, ":sd_type", sdt_cavalry),
              (neq, ":sd_type", sdt_harcher),
              (call_script, "script_get_centering_amount_moto", ":fformation", ":troop_count", ":div_spacing"),
              (position_move_x, pos1, reg0),
            (try_end),
            
            (try_begin),
              (eq, ":sd_type", sdt_archer),
              (call_script, "script_form_archers_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":fformation"),
            (else_try),
              (this_or_next | eq, ":sd_type", sdt_cavalry),
              (eq, ":sd_type", sdt_harcher),
              (try_begin),
                (ge, ":target_team", 0),	#enemy battlegroup targeted?
                (call_script, "script_formation_current_position_moto", pos29, "$fplayer_team_no", ":division"),
                (call_script, "script_battlegroup_get_position_moto", Enemy_Team_Pos_MOTO, ":target_team", ":target_division"),
                (get_distance_between_positions, ":distance_to_enemy", pos29, Enemy_Team_Pos_MOTO),
                
                (call_script, "script_battlegroup_get_action_radius_moto", "$fplayer_team_no", ":division"),
                (assign, ":combined_radius", reg0),
                (call_script, "script_battlegroup_get_action_radius_moto", ":target_team", ":target_division"),
                (val_add, ":combined_radius", reg0),
                
                (le, ":distance_to_enemy", ":combined_radius"),
                (call_script, "script_formation_end_moto", "$fplayer_team_no", ":division"),
                (str_store_class_name, s1, ":division"),
                (display_message, "@{s1}: cavalry formation disassembled."),
                (set_show_messages, 0),
                (team_give_order, "$fplayer_team_no", ":division", mordr_charge),
                (set_show_messages, 1),
              (else_try),
                (call_script, "script_form_cavalry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player"),
              (try_end),
            (else_try),
              (call_script, "script_form_infantry_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":fformation"),
            (try_end),
            
          (else_try),	#divisions not in formation
            (ge, ":target_team", 0),	#enemy battlegroup targeted?
            (store_add, ":slot", slot_team_d0_target_division, ":division"),
            (team_get_slot, ":target_division", "$fplayer_team_no", ":slot"),
            (try_begin),
              (this_or_next | eq, ":sd_type", sdt_archer),
              (this_or_next | eq, ":sd_type", sdt_harcher),
              (eq, ":sd_type", sdt_skirmisher),
              (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
              (team_slot_ge, "$fplayer_team_no", ":slot", 1),	#ranged are firing?
              (call_script, "script_battlegroup_get_position_moto", pos1, "$fplayer_team_no", ":division"),	#stop advancing
            (else_try),
              (call_script, "script_battlegroup_get_attack_destination_moto", pos1, "$fplayer_team_no", ":division", ":target_team", ":target_division"),
            (try_end),
            (call_script, "script_set_formation_destination_moto", "$fplayer_team_no", ":division", pos1),
            (team_get_movement_order, ":existing_order", "$fplayer_team_no", ":division"),
            (try_begin),
              (ge, ":target_team", 0),	#enemy battlegroup targeted?
              (call_script, "script_battlegroup_get_position_moto", pos29, "$fplayer_team_no", ":division"),
              (call_script, "script_battlegroup_get_position_moto", Enemy_Team_Pos_MOTO, ":target_team", ":target_division"),
              (get_distance_between_positions, ":distance_to_enemy", pos29, Enemy_Team_Pos_MOTO),
              
              (call_script, "script_battlegroup_get_action_radius_moto", "$fplayer_team_no", ":division"),
              (assign, ":combined_radius", reg0),
              (call_script, "script_battlegroup_get_action_radius_moto", ":target_team", ":target_division"),
              (val_add, ":combined_radius", reg0),
              
              (le, ":distance_to_enemy", ":combined_radius"),
              (try_begin),
                (neq, ":existing_order", mordr_charge),
                (set_show_messages, 0),
                (team_give_order, "$fplayer_team_no", ":division", mordr_charge),
                (set_show_messages, 1),
              (try_end),
            (else_try),
              (neq, ":existing_order", mordr_hold),
              (set_show_messages, 0),
              (team_give_order, "$fplayer_team_no", ":division", mordr_hold),
              (set_show_messages, 1),
            (try_end),
          (try_end),
        (try_end),	#Periodic Reform
      (try_end),	#Division Loop
      
      (assign, "$FormAI_autorotate", ":save_autorotate"),]),
  
  
  # #Utilities used by formations
  # script_cf_is_thrusting_weapon by motomataru
  # Input: item
  # Output: T/F
  ("cf_is_thrusting_weapon_moto", [
      (store_script_param, ":item", 1),
      #(is_between, ":item", weapons_begin, weapons_end),
      (item_get_type, ":type", ":item"),
      (is_between, ":type", itp_type_one_handed_wpn, itp_type_arrows),
      (item_get_thrust_damage, ":thrust_damage", ":item"),
      (item_get_swing_damage, ":swing_damage", ":item"),
      (val_mul, ":thrust_damage", 3),	#it seems thrusts connect faster than swings (as they should) although the
      #animations seem to take the same time
      (val_div, ":thrust_damage", 2),	#factor this in with approximation 2*PI/4 (distance swing must travel vs.
      #thrust) This ignores length, which creates too large a differential.  This is
      #a happy medium.
      (ge, ":thrust_damage", ":swing_damage"),]),
  
  # script_cf_is_weapon_ranged by motomataru
  # Input: weapon ID, flag 0/1 to consider thrown weapons
  # Output: T/F
  ("cf_is_weapon_ranged_moto", [
      (store_script_param, ":weapon", 1),
      (store_script_param, ":include_thrown", 2),
      
      (assign, ":test_val", 0),
      (try_begin),
        (ge, ":weapon", 0),
        (item_get_type, ":type", ":weapon"),
        (try_begin),
          (this_or_next | eq, ":type", itp_type_bow),
          (this_or_next | eq, ":type", itp_type_crossbow),
          (this_or_next | eq, ":type", itp_type_pistol),
          (eq, ":type", itp_type_musket),
          (assign, ":test_val", 1),
        (else_try),
          (eq, ":type", itp_type_thrown),
          (neq, ":include_thrown", 0),
          (assign, ":test_val", 1),
        (try_end),
      (try_end),
      
      (neq, ":test_val", 0),]),
  
  # script_equip_best_melee_weapon by motomataru
  # Input: agent id, flag to force shield, flag to force for length ALONE,
  # current fire order
  # Output: none
  ("equip_best_melee_weapon_moto", [
      (store_script_param, ":agent", 1),
      (store_script_param, ":force_shield", 2),
      (store_script_param, ":force_length", 3),
      (store_script_param, ":fire_order", 4),
      
      (agent_get_wielded_item, ":cur_wielded", ":agent", 0),
      (try_begin),
        (call_script, "script_cf_is_weapon_ranged_moto", ":cur_wielded", 0),
        (agent_get_ammo, ":ammo", ":agent", 1),
        (gt, ":ammo", 0),
        
      (else_try),
        #priority items
        (assign, ":shield", itm_no_item),
        (assign, ":weapon", itm_no_item),
        (try_for_range, ":item_slot", ek_item_0, ek_head),
          (agent_get_item_slot, ":item", ":agent", ":item_slot"),
          (gt, ":item", itm_no_item),
          (item_get_type, ":weapon_type", ":item"),
          (try_begin),
            (eq, ":weapon_type", itp_type_shield),
            (assign, ":shield", ":item"),
          (else_try),
            (eq, ":weapon_type", itp_type_thrown),
            (eq, ":fire_order", aordr_fire_at_will),
            # (agent_get_ammo, ":ammo", ":agent", 0), #assume infantry would have no
            # other kind of ranged weapon
            # (gt, ":ammo", 0),
            (assign, ":weapon", ":item"),	#use thrown weapons first
          (try_end),
        (try_end),
        
        #select weapon
        (try_begin),
          (eq, ":weapon", itm_no_item),
          (assign, ":cur_score", 0),
          (try_for_range, ":item_slot", ek_item_0, ek_head),
            (agent_get_item_slot, ":item", ":agent", ":item_slot"),
            (gt, ":item", itm_no_item),
            (item_get_type, ":weapon_type", ":item"),
            (neq, ":weapon_type", itp_type_shield),
            
            (try_begin),
              (item_has_property, ":item", itp_two_handed),
              (assign, reg0, 1),
            (else_try),
              (assign, reg0, 0),
            (try_end),
            
            (this_or_next | eq, reg0, 0),
            (this_or_next | eq, ":force_shield", 0),
            (eq, ":shield", itm_no_item),
            
            (try_begin),
              (call_script, "script_cf_is_weapon_ranged_moto", ":item", 1),
              
            (else_try),
              (try_begin),
                (neq, ":force_length", 0),
                (item_get_weapon_length, ":item_length", ":item"),
                (try_begin),
                  (lt, ":cur_score", ":item_length"),
                  (assign, ":cur_score", ":item_length"),
                  (assign, ":weapon", ":item"),
                (try_end),
              (else_try),
                (agent_get_troop_id, ":troop_id", ":agent"),
                (troop_is_guarantee_horse, ":troop_id"),
                (agent_get_horse, ":horse", ":agent"),
                (le, ":horse", 0),
                (try_for_range, ":item_slot", ek_item_0, ek_head),
                  (agent_get_item_slot, ":item", ":agent", ":item_slot"),
                  (gt, ":item", itm_no_item),
                  (item_get_type, ":weapon_type", ":item"),
                  (eq, ":weapon_type", itp_type_one_handed_wpn),
                  (item_get_swing_damage, ":swing", ":item"),
                  (gt, ":swing", 19),
                  (assign, ":weapon", ":item"),
                (try_end),
              (else_try),
                (agent_get_troop_id, ":troop_id", ":agent"),
                (assign, ":imod", imod_plain),
                (try_begin),    #only heroes have item modifications
                  (troop_is_hero, ":troop_id"),
                  (try_for_range, ":troop_item_slot",  ek_item_0, ek_head),    # heroes have only 4 possible weapons (equipped)
                    (troop_get_inventory_slot, reg0, ":troop_id", ":troop_item_slot"),  #Find Item Slot with same item ID as Equipped Weapon
                    (eq, reg0, ":item"),
                    (troop_get_inventory_slot_modifier, ":imod", ":troop_id", ":troop_item_slot"),
                  (try_end),
                (try_end),
                (call_script, "script_evaluate_item_moto", ":item", ":imod"),
                (lt, ":cur_score", reg0),
                (assign, ":cur_score", reg0),
                (assign, ":weapon", ":item"),
              (try_end),
            (try_end),  #melee weapon
          (try_end),  #weapon slot loop
        (try_end),  #select weapon
        
        #equip selected items if needed
        (try_begin),
          (neq, ":cur_wielded", ":weapon"),
          (try_begin),
            (gt, ":shield", itm_no_item),
            (agent_get_wielded_item, reg0, ":agent", 1),
            (neq, reg0, ":shield"),	#reequipping secondary will UNequip (from experience)
            (agent_set_wielded_item, ":agent", ":shield"),
          (try_end),
          (gt, ":weapon", itm_no_item),
          (agent_set_wielded_item, ":agent", ":weapon"),
        (try_end),
      (try_end),]),
  
  # script_set_formation_destination by motomataru
  # Input: team, troop class, position
  # Kluge around buggy *_order_position functions for teams 0-3
  ("set_formation_destination_moto", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fposition", 3),
      
      (position_get_x, ":x", ":fposition"),
      (position_get_y, ":y", ":fposition"),
      (position_get_rotation_around_z, ":zrot", ":fposition"),
      
      (store_add, ":slot", slot_team_d0_destination_x, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":x"),
      (store_add, ":slot", slot_team_d0_destination_y, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":y"),
      (store_add, ":slot", slot_team_d0_destination_zrot, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":zrot"),
      
      (team_set_order_position, ":fteam", ":fdivision", ":fposition"),]),
  
  # script_get_formation_destination by motomataru
  # Input: position, team, troop class
  # Output: input position (pos0 used)
  # Kluge around buggy *_order_position functions for teams 0-3
  ("get_formation_destination_moto", [
      (store_script_param, ":fposition", 1),
      (store_script_param, ":fteam", 2),
      (store_script_param, ":fdivision", 3),
      (init_position, ":fposition"),
      # (try_begin),
      #(is_between, ":fteam", 0, 4), #Caba - this will always pass MOTO except in
      #mods with more than four teams (eg SWC arena) but now obsolete by other
      #limits
      (store_add, ":slot", slot_team_d0_destination_x, ":fdivision"),
      (team_get_slot, ":x", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_destination_y, ":fdivision"),
      (team_get_slot, ":y", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_destination_zrot, ":fdivision"),
      (team_get_slot, ":zrot", ":fteam", ":slot"),
      
      (position_set_x, ":fposition", ":x"),
      (position_set_y, ":fposition", ":y"),
      (position_rotate_z, ":fposition", ":zrot"),
      # (else_try),
      # (store_add, ":slot", slot_team_d0_first_member, ":fdivision"), #only
      # defined for divisions in formation
      # (team_get_slot, reg0, ":fteam", ":slot"),
      # (try_begin), # "launder" team_get_order_position shutting down
      # position_move_x
      # (gt, reg0, -1),
      # (team_get_order_position, ":fposition", ":fteam", ":fdivision"),
      # (agent_get_position, pos0, reg0),
      # (agent_set_position, reg0, ":fposition"),
      # (agent_get_position, ":fposition", reg0),
      # (agent_set_position, reg0, pos0),
      # (try_end),
      # (try_end),
      (position_set_z_to_ground_level, ":fposition"),]),
  
  # script_formation_current_position by motomataru
  # Input: destination position (not pos0), team, division
  # Output: in destination position
  # As opposed to script_battlegroup_get_position, this obtains target rotation
  # from formation destination and positions at the center of the front
  ("formation_current_position_moto", [
      (store_script_param, ":fposition", 1),
      (store_script_param, ":fteam", 2),
      (store_script_param, ":fdivision", 3),
      (call_script, "script_battlegroup_get_position_moto", ":fposition", ":fteam", ":fdivision"),
      (call_script, "script_get_formation_destination_moto", pos0, ":fteam", ":fdivision"),
      (position_copy_rotation, ":fposition", pos0),
      (call_script, "script_battlegroup_dist_center_to_front_moto", ":fteam", ":fdivision"),
      (position_move_y, ":fposition", reg0, 0),]),
  
  # script_str_store_division_type_name by motomataru
  # Input: destination, division type (sdt_*)
  # Output: none
  ("str_store_division_type_name_moto", [
      (store_script_param, ":str_reg", 1),
      (store_script_param, ":division_type", 2),
      (try_begin),
        (eq, ":division_type", sdt_infantry),
        (str_store_string, ":str_reg", "@infantry"),
      (else_try),
        (eq, ":division_type", sdt_archer),
        (str_store_string, ":str_reg", "@archer"),
      (else_try),
        (eq, ":division_type", sdt_cavalry),
        (str_store_string, ":str_reg", "@cavalry"),
      (else_try),
        (eq, ":division_type", sdt_polearm),
        (str_store_string, ":str_reg", "@polearm"),
      (else_try),
        (eq, ":division_type", sdt_skirmisher),
        (str_store_string, ":str_reg", "@skirmisher"),
      (else_try),
        (eq, ":division_type", sdt_harcher),
        (str_store_string, ":str_reg", "@mounted archer"),
      (else_try),
        (eq, ":division_type", sdt_support),
        (str_store_string, ":str_reg", "@support"),
      (else_try),
        (eq, ":division_type", sdt_bodyguard),
        (str_store_string, ":str_reg", "@bodyguard"),
      (else_try),
        (str_store_string, ":str_reg", "@undetermined type of"),
      (try_end),]),
  
  # script_formation_to_native_order by motomataru
  # Input: team, division, formation
  # Output: issues team_give_order with appropriate command to make formation
  ("formation_to_native_order_moto", [
      (store_script_param, ":team", 1),
      (store_script_param, ":division", 2),
      (store_script_param, ":formation", 3),
      
      (try_begin),
        (gt, ":formation", formation_none),	#custom formation (bad call)
        
      (else_try),
        (eq, Native_Formations_Implementation, WB_Implementation),
        (store_add, ":slot", slot_team_d0_formation_space, ":division"),
        (team_get_slot, ":spacing", ":team", ":slot"),
        (val_sub, ":spacing", ":formation"),	#formation constants indicate number of "Stand Closer"
        (set_show_messages, 0),
        (try_for_range, reg0, 0, ":spacing"),
          (team_give_order, ":team", ":division", mordr_stand_closer),
        (try_end),
        (set_show_messages, 1),
        (team_set_slot, ":team", ":slot", ":spacing"),
        
      #WFAS implementation
      (else_try),
        (eq, ":formation", formation_1_row),
        (team_give_order, ":team", ":division", mordr_form_1_row),
      (else_try),
        (eq, ":formation", formation_2_row),
        (team_give_order, ":team", ":division", mordr_form_2_row),
      (else_try),
        (eq, ":formation", formation_3_row),
        (team_give_order, ":team", ":division", mordr_form_3_row),
      (else_try),
        (eq, ":formation", formation_4_row),
        (team_give_order, ":team", ":division", mordr_form_4_row),
      (else_try),
        (eq, ":formation", formation_5_row),
        (team_give_order, ":team", ":division", mordr_form_5_row),
      (try_end)]),
  
  # script_point_y_toward_position by motomataru
  # Input: from position, to position
  # Output: reg0 distance in cm
  # Basically, points the first position at the second, so then simple move_y
  # will move back and forth and move_x side to side
  # Things like cast_ray work with this as well
  ("point_y_toward_position_moto", [
      (store_script_param, ":from_position", 1),
      (store_script_param, ":to_position", 2),
      (assign, ":save_fpm", 1),
      (convert_to_fixed_point, ":save_fpm"),
      (set_fixed_point_multiplier, 100),  #to match cm returned by get_distance_between_positions
      
      #remove current rotation
      (position_get_x, ":from_x", ":from_position"),
      (position_get_y, ":from_y", ":from_position"),
      (position_get_z, ":from_z", ":from_position"),
      (init_position, ":from_position"),
      (position_set_x, ":from_position", ":from_x"),
      (position_set_y, ":from_position", ":from_y"),
      (position_set_z, ":from_position", ":from_z"),
      
      #horizontal rotation
      (position_get_x, ":change_in_x", ":to_position"),
      (val_sub, ":change_in_x", ":from_x"),
      (position_get_y, ":change_in_y", ":to_position"),
      (val_sub, ":change_in_y", ":from_y"),
      
      (try_begin),
        (this_or_next | neq, ":change_in_y", 0),
        (neq, ":change_in_x", 0),
        (store_atan2, ":theta", ":change_in_y", ":change_in_x"),
        (assign, ":ninety", 90),
        (convert_to_fixed_point, ":ninety"),
        (val_sub, ":theta", ":ninety"),	#point Y axis at to position
        (position_rotate_z_floating, ":from_position", ":theta"),
      (try_end),
      
      #vertical rotation
      (get_distance_between_positions, ":distance_between", ":from_position", ":to_position"),
      (try_begin),
        (gt, ":distance_between", 0),
        (position_get_z, ":dist_z_to_sine", ":to_position"),
        (val_sub, ":dist_z_to_sine", ":from_z"),
        (val_div, ":dist_z_to_sine", ":distance_between"),
        (store_asin, ":theta", ":dist_z_to_sine"),
        (position_rotate_x_floating, ":from_position", ":theta"),
      (try_end),
      
      (assign, reg0, ":distance_between"),
      (set_fixed_point_multiplier, ":save_fpm"),]),
  
  #script_agent_fix_division
  #Input: agent_id
  #Output: nothing (agent divisions changed, slot set)
  #To fix AI troop divisions from the engine applying player's party divisions
  #on all agents
  #This is called after agent_reassign_team, so can safely assume correct team
  #is set
  ("agent_fix_division_moto", [
      (store_script_param_1, ":agent"),
      (agent_set_slot, ":agent", slot_agent_new_division, -1),
      (get_player_agent_no, ":player"),	#after_mission_start triggers are called after spawn, so globals can't be used
      #yet
      
      (try_begin),
        (ge, ":player", 0),
        (neq, ":agent", ":player"),
        (agent_is_human, ":agent"),
        (agent_get_group, ":player_team", ":player"),
        (agent_get_group, ":team", ":agent"),
        (this_or_next | main_hero_fallen),
        (neq, ":team", ":player_team"),
        
        (assign, ":target_division", grc_infantry),
        (agent_get_horse, ":horse", ":agent"),
        (agent_get_troop_id, ":troop_no", ":agent"),
        
        #logic from script_troop_default_division
        #limited to the three divisions the AI currently uses
        (try_begin),
          (this_or_next | ge, ":horse", 0),
          (troop_is_guarantee_horse, ":troop_no"),
          (assign, ":target_division", grc_cavalry),
          
          # (try_begin),
          # (eq, ":flag_0_for_expanded", 0),
          # (try_for_range, reg0, 0, ":inv_cap"),
          # (troop_get_inventory_slot, ":item", ":troop_no", reg0),
          # (call_script, "script_cf_is_weapon_ranged_moto", ":item", 1),
          # (assign, ":target_division", sdt_harcher),
          # (try_end),
          # (try_end),
          
        (else_try),
          (troop_is_guarantee_ranged, ":troop_no"),
          # (assign, ":has_ranged", 0),
          
          (try_for_range, ":item_slot", ek_item_0, ek_head),
            (agent_get_item_slot, ":item", ":agent", ":item_slot"),
            (call_script, "script_cf_is_weapon_ranged_moto", ":item", 1),
            (agent_get_ammo, reg1, ":agent", 0),
            (ge, reg1, minimum_ranged_ammo),  #more than two to throw on a charge?
            # (item_get_type, reg1, ":item"),
            # (try_begin),
            # (eq, reg1, itp_type_thrown),
            # (eq, ":flag_0_for_expanded", 0),
            # (neq, ":target_division", grc_archers),
            # (assign, ":target_division", sdt_skirmisher),
            # (else_try),
            (assign, ":target_division", grc_archers),
            # (try_end),
            # (assign, ":has_ranged", 1),
          (try_end),
          
          # (neq, ":has_ranged", 0),
          
          # (else_try),
          # (eq, ":flag_0_for_expanded", 0),
          # (try_for_range, reg0, 0, ":inv_cap"),
          # (troop_get_inventory_slot, ":item", ":troop_no", reg0),
          # (call_script, "script_cf_is_thrusting_weapon_moto", ":item"),
          # (item_get_type, reg1, ":item"),
          # (eq, reg1, itp_type_polearm),
          # (assign, ":target_division", sdt_polearm),
          # (try_end),
        (try_end),
        
        (agent_get_division, ":division", ":agent"),
        (neq, ":division", ":target_division"),
        (agent_set_division, ":agent", ":target_division"),
        (agent_set_slot, ":agent", slot_agent_new_division, ":target_division"),
      (try_end),]),
  
  # script_store_battlegroup_type
  # Input: team, division
  # Output: reg0 and slot_team_dx_type with sdt_* value
  # Automatically called from store_battlegroup_data
  ("store_battlegroup_type_moto", [
      (store_script_param_1, ":fteam"),
      (store_script_param_2, ":fdivision"),
      
      (assign, ":count_infantry", 0),
      (assign, ":count_archer", 0),
      (assign, ":count_cavalry", 0),
      (assign, ":count_harcher", 0),
      (assign, ":count_polearms", 0),
      (assign, ":count_skirmish", 0),
      (assign, ":count_support", 0),
      (assign, ":count_bodyguard", 0),
      
      #(team_get_leader, ":leader", ":fteam"),
      (call_script, "script_team_get_nontroll_leader", ":fteam"),
      (assign, ":leader", reg0),
      
      (try_for_agents, ":cur_agent"),
        (agent_is_active, ":cur_agent"),
        (call_script, "script_cf_valid_formation_member_moto", ":fteam", ":fdivision", ":leader", ":cur_agent"),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (agent_get_ammo, ":cur_ammo", ":cur_agent", 0),
        
        (try_begin),
          (neg | troop_is_hero, ":cur_troop"),
          (try_begin), #Cavalry
            (agent_get_horse, reg0, ":cur_agent"),
            (ge, reg0, 0),
            (try_begin),
              (ge, ":cur_ammo", minimum_ranged_ammo),
              (val_add, ":count_harcher", 1),
            (else_try),
              (val_add, ":count_cavalry", 1),
            (try_end),
          (else_try), #Archers
            (ge, ":cur_ammo", minimum_ranged_ammo),
            # #use when troops are equipped with ranged at start of battle
            # (agent_get_class, ":bgclass", ":cur_agent"),
            # (eq, ":bgclass", grc_archers),
            # #end use when troops equipped with ranged at start of battle
            (assign, ":end", ek_head),
            (try_for_range, ":i", ek_item_0, ":end"),
              (agent_get_item_slot, ":item", ":cur_agent", ":i"),
              (gt, ":item", 0),
              (item_get_type, ":weapontype", ":item"),
              (is_between, ":weapontype", itp_type_bow, itp_type_thrown),  # bow or crossbow
              (assign, ":end", ek_item_0), #loop Break
            (try_end),
            (try_begin),
              (eq, ":end", ek_head), #failed to find bow or crossbow
              (val_add, ":count_skirmish", 1),
            (else_try),
              (val_add, ":count_archer", 1),
            (try_end),
          (else_try), #Infantry
            (assign, ":end", ek_head),
            (try_for_range, ":i", ek_item_0, ":end"),
              (agent_get_item_slot, ":item", ":cur_agent", ":i"),
              (gt, ":item", 0),
              (call_script, "script_cf_is_thrusting_weapon_moto", ":item"),
              (item_get_type, ":weapontype", ":item"),
              (eq, ":weapontype", itp_type_polearm),
              (assign, ":end", ek_item_0), #loop Break
            (try_end),
            (try_begin),
              (eq, ":end", ek_head), #failed to find a polearm
              (val_add, ":count_infantry", 1),
            (else_try),
              (val_add, ":count_polearms", 1),
            (try_end),
          (try_end),
        (else_try), #Heroes
          (assign, ":support_skills", 0), #OPEN TO SUGGESTIONS HERE ?skl_trade, skl_spotting, skl_pathfinding,
          #skl_tracking?
          (store_skill_level, reg0, skl_engineer, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_first_aid, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_surgery, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_wound_treatment, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (try_begin),
            (gt, ":support_skills", 5),
            (val_add, ":count_support", 1),
          (else_try),
            (val_add, ":count_bodyguard", 1),
          (try_end),
        (try_end), #Regular v Hero
      (try_end), #Agent Loop
      
      #Do Comparisons With Counts, set ":div_type"
      (assign, ":slot", slot_team_d0_type),
      (team_set_slot, scratch_team, ":slot", ":count_infantry"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_archer"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_cavalry"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_polearms"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_skirmish"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_harcher"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_support"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_bodyguard"),
      
      (assign, ":count_to_beat", 0),
      (assign, ":count_total", 0),
      (try_for_range, ":type", sdt_infantry, sdt_infantry + 8), #only 8 sdt_types at the moment
        (store_add, ":slot", slot_team_d0_type, ":type"),
        (team_get_slot, ":count", scratch_team, ":slot"),
        (val_add, ":count_total", ":count"),
        (lt, ":count_to_beat", ":count"),
        (assign, ":count_to_beat", ":count"),
        (assign, ":div_type", ":type"),
      (try_end),
      
      (val_mul, ":count_to_beat", 2),
      (try_begin),
        (lt, ":count_to_beat", ":count_total"), #Less than half of this division
        (assign, ":count_to_beat", 0),
        (assign, ":div_type", -1),
        (try_for_range, ":type", sdt_infantry, sdt_infantry + 3), #check main types for a majority
          (store_add, ":slot", slot_team_d0_type, ":type"),
          (team_get_slot, ":count", scratch_team, ":slot"),
          (val_add, ":slot", 3),	#subtype is three more than main type
          (team_get_slot, reg0, scratch_team, ":slot"),
          (val_add, ":count", reg0),
          (lt, ":count_to_beat", ":count"),
          (assign, ":count_to_beat", ":count"),
          (assign, ":div_type", ":type"),
        (try_end),
        
        (val_mul, ":count_to_beat", 2),
        (lt, ":count_to_beat", ":count_total"), #Less than half of this division
        (assign, ":div_type", sdt_unknown), #Or 0
      (try_end),
      
      #hard-code traditional infantry division (avoid player confusion for mods
      #which arm troops with ranged at start of battle)
      (try_begin),
        (eq, ":fdivision", grc_infantry),
        (neq, ":div_type", sdt_polearm),
        (assign, ":div_type", sdt_infantry),
      (try_end),
      
      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":div_type"),
      (assign, reg0, ":div_type"),]),
  
  # script_store_battlegroup_data by motomataru #EDITED TO SLOTS FOR MANY
  # DIVISIONS BY CABA'DRIN
  # Input: none
  # Output: sets positions and globals to track data on ALL groups in a battle
  # Globals used: pos0, pos1, reg0
  ("store_battlegroup_data_moto", [
      (assign, ":team0_leader", 0),
      (assign, ":team0_x_leader", 0),
      (assign, ":team0_y_leader", 0),
      (assign, ":team0_zrot_leader", 0),
      (assign, ":team0_level_leader", 0),
      (assign, ":team1_leader", 0),
      (assign, ":team1_x_leader", 0),
      (assign, ":team1_y_leader", 0),
      (assign, ":team1_zrot_leader", 0),
      (assign, ":team1_level_leader", 0),
      (assign, ":team2_leader", 0),
      (assign, ":team2_x_leader", 0),
      (assign, ":team2_y_leader", 0),
      (assign, ":team2_zrot_leader", 0),
      (assign, ":team2_level_leader", 0),
      (assign, ":team3_leader", 0),
      (assign, ":team3_x_leader", 0),
      (assign, ":team3_y_leader", 0),
      (assign, ":team3_zrot_leader", 0),
      (assign, ":team3_level_leader", 0),
      
      #save some info
      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (try_begin),
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_exists, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          
        (else_try),
          (store_add, ":slot", slot_team_d0_exists, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 0),
        (try_end),
      (try_end),
      
      #Team Slots reset every mission, like agent slots, but just to be sure for
      #when it gets called during the mission
      (try_for_range, ":slot", reset_team_stats_begin, reset_team_stats_end), #Those within the "RESET GROUP" in formations_constants
        (try_for_range, ":team", 0, 4),
          (team_set_slot, ":team", ":slot", 0),
        (try_end),
      (try_end),
      
      (try_for_agents, ":cur_agent"),
        (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, -1),
        
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 0),
        
        (agent_get_group, ":bgteam", ":cur_agent"),
        (agent_get_division, ":bgdivision", ":cur_agent"),
        (agent_get_class, ":agent_class", ":cur_agent"),
        (agent_get_position, pos1, ":cur_agent"),
        
        (try_begin),
          (agent_is_non_player, ":cur_agent"),
          
          (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
          (team_get_slot, ":bgtype", ":bgteam", ":slot"),
          (this_or_next | eq, ":bgtype", sdt_cavalry),	#assigned to horsed division
          (eq, ":bgtype", sdt_harcher),
          
          (team_get_riding_order, reg0, ":bgteam", ":bgdivision"),
          (neq, reg0, rordr_dismount),
          
          (team_get_order_position, pos0, ":bgteam", ":bgdivision"),
          (get_distance_between_positions, ":old_distance", pos0, pos1),
          (gt, ":old_distance", AI_charge_distance),	#agent is out of formation?
          
          (assign, ":target_type", ":bgtype"),
          
          (try_begin),
            (eq, ":agent_class", grc_infantry),	#Native has transferred this agent to infantry
            (assign, ":target_type", sdt_infantry),
            
            (try_for_range, ":item_slot", ek_item_0, ek_head),
              (eq, ":bgteam", "$fplayer_team_no"),	#AI doesn't use extended right now
              (agent_get_item_slot, ":item", ":cur_agent", ":item_slot"),
              (gt, ":item", 0),
              (call_script, "script_cf_is_thrusting_weapon_moto", ":item"),
              (item_get_type, reg0, ":item"),
              (eq, reg0, itp_type_polearm),
              (assign, ":target_type", sdt_polearm),
            (try_end),
            
          (else_try),
            (eq, ":agent_class", grc_archers),	#Native has transferred this agent to archers
            (assign, ":target_type", sdt_archer),
            
            (try_for_range, ":item_slot", ek_item_0, ek_head),
              (eq, ":bgteam", "$fplayer_team_no"),	#AI doesn't use extended right now
              (agent_get_item_slot, ":item", ":cur_agent", ":item_slot"),
              (gt, ":item", 0),
              (call_script, "script_cf_is_weapon_ranged_moto", ":item", 1),
              (agent_get_ammo, reg1, ":cur_agent", 0),
              (ge, reg1, minimum_ranged_ammo),  #more than two to throw on a charge?
              (item_get_type, reg0, ":item"),
              (eq, reg0, itp_type_thrown),
              (assign, ":target_type", sdt_skirmisher),
            (try_end),
          (try_end),
          
          (neq, ":target_type", ":bgtype"),
          (assign, ":bgdivision", ":target_type"),
          
          (try_for_range_backwards, ":new_division", 0, 9),
            (store_add, ":slot", slot_team_d0_size, ":new_division"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (gt, reg0, 0),
            
            (store_add, ":slot", slot_team_d0_type, ":new_division"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (eq, reg0, ":target_type"),
            
            (assign, ":bgdivision", ":new_division"),
          (try_end),
          
          (try_begin),
            (store_add, ":slot", slot_team_d0_exists, ":bgdivision"),
            (team_slot_eq, "$fplayer_team_no", ":slot", 0),	#division does not yet exist?
            (agent_is_alive, "$fplayer_agent_no"),
            (store_add, ":slot", slot_team_d0_move_order, ":bgdivision"),
            (neg | team_slot_eq, "$fplayer_team_no", ":slot", mordr_follow),
            (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),
            (set_show_messages, 0),
            (team_give_order, "$fplayer_team_no", ":bgdivision", mordr_follow),
            (set_show_messages, 1),
          (try_end),
          
          (agent_set_slot, ":cur_agent", slot_agent_new_division, ":bgdivision"),	#reassign
          (agent_set_division, ":cur_agent", ":bgdivision"),
          
        (else_try),	#Maintain any changed divisions (apparently agents get switched back)
          (agent_is_non_player, ":cur_agent"),
          (agent_slot_ge, ":cur_agent", slot_agent_new_division, 0),
          (neg | agent_slot_eq, ":cur_agent", slot_agent_new_division, ":bgdivision"),
          (agent_get_slot, ":bgdivision", ":cur_agent", slot_agent_new_division),
          (agent_set_division, ":cur_agent", ":bgdivision"),
        (try_end),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (try_begin),
          #(team_get_leader, ":leader", ":bgteam"),
          (call_script, "script_team_get_nontroll_leader", ":bgteam"),
          (assign, ":leader", reg0),
          (agent_is_active, ":leader"),
          (eq, ":leader", ":cur_agent"),
          (assign, ":bgdivision", -1),
        (try_end),
        (store_character_level, ":cur_level", ":cur_troop"),
        (agent_get_ammo, ":cur_ammo", ":cur_agent", 0),
        
        #get weapon characteristics
        (assign, ":cur_weapon_type", 0),
        (assign, ":cur_weapon_length", 0),
        (assign, ":cur_swung_weapon_length", 0),
        (agent_get_wielded_item, ":cur_weapon", ":cur_agent", 0),
        (try_begin),
        	(gt, ":cur_weapon", 0),
          #(is_between, ":cur_weapon", weapons_begin, weapons_end),
            (item_get_type, ":type", ":cur_weapon"),
      		(is_between, ":type", itp_type_one_handed_wpn, itp_type_arrows),
          # (neg | is_between, ":cur_weapon", estandartes_begin, estandartes_end),	#put exceptions here, such as standards, that will otherwise force a lot of
          #extra spacing for nothing
          (item_get_weapon_length, ":cur_weapon_length", ":cur_weapon"),
          
          (try_begin),
          	(gt, ":cur_weapon", 0),
            (call_script, "script_cf_is_thrusting_weapon_moto", ":cur_weapon"),
          (else_try),
            (assign, ":cur_swung_weapon_length", ":cur_weapon_length"),
          (try_end),
        (try_end),
        
        #add up armor
        (assign, ":cur_avg_armor", 0),
        (try_for_range, ":item_slot", ek_head, ek_horse),
          (agent_get_item_slot, ":armor", ":cur_agent", ":item_slot"),
          (gt, ":armor", itm_no_item),
          (item_get_head_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
          (item_get_body_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
          (item_get_leg_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
        (try_end),
        (agent_get_wielded_item, ":armor", ":cur_agent", 1),	#include shield
        (try_begin),
          (gt, ":armor", itm_no_item),
          (item_get_type, ":item_type", ":armor"),
          (eq, ":item_type", itp_type_shield),
          (item_get_body_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
        (try_end),
        (val_div, ":cur_avg_armor", 3),	#average the zones (head, body, leg)
        
        #average with horse armor for mounted agents
        (agent_get_horse, ":cur_horse", ":cur_agent"),
        (try_begin),
          (gt, ":cur_horse", -1),
          (agent_get_item_id, ":itm_horse", ":cur_horse"),
          (gt, ":itm_horse", itm_no_item),
          (item_get_body_armor, reg0, ":itm_horse"),
          (val_add, ":cur_avg_armor", reg0),
          (val_div, ":cur_avg_armor", 2),
        (try_end),
        
        (position_get_x, ":x_value", pos1),
        (position_get_y, ":y_value", pos1),
        (position_get_rotation_around_z, ":zrot_value", pos1),
        (try_begin),
          (eq, ":bgdivision", -1), #Leaders
          (try_begin),
            (eq, ":bgteam", 0),
            (assign, ":team0_leader", 1),
            (assign, ":team0_x_leader", ":x_value"),
            (assign, ":team0_y_leader", ":y_value"),
            (assign, ":team0_zrot_leader", ":zrot_value"),
            (assign, ":team0_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 1),
            (assign, ":team1_leader", 1),
            (assign, ":team1_x_leader", ":x_value"),
            (assign, ":team1_y_leader", ":y_value"),
            (assign, ":team1_zrot_leader", ":zrot_value"),
            (assign, ":team1_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 2),
            (assign, ":team2_leader", 1),
            (assign, ":team2_x_leader", ":x_value"),
            (assign, ":team2_y_leader", ":y_value"),
            (assign, ":team2_zrot_leader", ":zrot_value"),
            (assign, ":team2_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 3),
            (assign, ":team3_leader", 1),
            (assign, ":team3_x_leader", ":x_value"),
            (assign, ":team3_y_leader", ":y_value"),
            (assign, ":team3_zrot_leader", ":zrot_value"),
            (assign, ":team3_level_leader", ":cur_level"),
          (try_end),
        (else_try),
          # (agent_get_ammo, reg0, ":cur_agent", 1), #Division in Melee
          (try_begin),
            # (le, reg0, 0), #not wielding ranged weapon?
            (agent_get_attack_action, reg0, ":cur_agent"),
            (gt, reg0, 0),
            (store_add, ":slot", slot_team_d0_is_fighting, ":bgdivision"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (val_add, reg0, 1),
            (team_set_slot, ":bgteam", ":slot", reg0),
          (try_end),
          
          (store_add, ":slot", slot_team_d0_size, ":bgdivision"), #Division Count
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", ":slot", ":value"),
          
          (try_begin),
            (ge, ":cur_ammo", minimum_ranged_ammo),
            (store_add, ":slot", slot_team_d0_percent_ranged, ":bgdivision"), #Division Percentage are Archers
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (val_add, ":value", 1),
            (team_set_slot, ":bgteam", ":slot", ":value"),
          (else_try),
            (store_add, ":slot", slot_team_d0_low_ammo, ":bgdivision"), #Division Running out of Ammo Flag
            (team_set_slot, ":bgteam", ":slot", 1),
          (try_end),
          
          (try_begin),
            (eq, ":cur_weapon_type", itp_type_thrown),
            (store_add, ":slot", slot_team_d0_percent_throwers, ":bgdivision"), #Division Percentage are Throwers
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (val_add, ":value", 1),
            (team_set_slot, ":bgteam", ":slot", ":value"),
          (try_end),
          
          (store_add, ":slot", slot_team_d0_level, ":bgdivision"), #Division Level
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_level"),
          (team_set_slot, ":bgteam", ":slot", ":value"),
          
          (store_add, ":slot", slot_team_d0_weapon_length, ":bgdivision"), #Division Weapon Length
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_weapon_length"),
          (team_set_slot, ":bgteam", ":slot", ":value"),
          
          (store_add, ":slot", slot_team_d0_swung_weapon_length, ":bgdivision"), #Division Swung Weapon Length
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (try_begin),
            (lt, ":value", ":cur_swung_weapon_length"),
            (team_set_slot, ":bgteam", ":slot", ":cur_swung_weapon_length"),
          (try_end),
          
          (store_add, ":slot", slot_team_d0_armor, ":bgdivision"), #Division Armor
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_avg_armor"),
          (team_set_slot, ":bgteam", ":slot", ":value"),
          
          (try_begin),	#Division First Rank Shortest Weapon Length
            (agent_slot_eq, ":cur_agent", slot_agent_formation_rank, 1),
            (store_add, ":slot", slot_team_d0_front_weapon_length, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (this_or_next | eq, ":value", 0),
            (gt, ":value", ":cur_weapon_length"),
            (team_set_slot, ":bgteam", ":slot", ":cur_weapon_length"),
          (try_end),
          
          (store_add, ":slot", slot_team_d0_avg_x, ":bgdivision"), #Position X
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":x_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),
          
          (store_add, ":slot", slot_team_d0_avg_y, ":bgdivision"), #Position Y
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":y_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),
          
          (store_add, ":slot", slot_team_d0_avg_zrot, ":bgdivision"), #Rotation
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":zrot_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),
        (try_end), #Leader vs Regular
        
        (try_begin),
          (eq, ":agent_class", grc_archers),
          (team_get_slot, ":value", ":bgteam", slot_team_num_archers),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_archers, ":value"),
          
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (team_get_slot, ":value", ":bgteam", slot_team_num_cavalry),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_cavalry, ":value"),
          
        (else_try),
          (eq, ":agent_class", grc_infantry),
          (team_get_slot, ":value", ":bgteam", slot_team_num_infantry),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_infantry, ":value"),
        (try_end),
        
        #find nearest enemy agent
        (assign, ":nearest_runner", -1),
        (agent_ai_get_num_cached_enemies, ":num_nearby_agents", ":cur_agent"),
        (try_for_range, reg0, 0, ":num_nearby_agents"),
          (agent_ai_get_cached_enemy, ":enemy_agent", ":cur_agent", reg0),
          (agent_is_alive, ":enemy_agent"),
          
          (try_begin),
            (eq, ":nearest_runner", -1),
            (assign, ":nearest_runner", ":enemy_agent"),
            
          (else_try),
            (agent_get_position, pos0, ":enemy_agent"),
            (get_distance_between_positions, ":new_distance", pos0, pos1),
            (agent_get_position, pos0, ":nearest_runner"),
            (get_distance_between_positions, ":old_distance", pos0, pos1),
            (lt, ":new_distance", ":old_distance"),
            (assign, ":nearest_runner", ":enemy_agent"),
          (try_end),
          
          (agent_slot_eq, ":enemy_agent", slot_agent_is_running_away, 0),
          
          (try_begin),
            (agent_get_slot, ":closest_enemy", ":cur_agent", slot_agent_nearest_enemy_agent),
            (eq, ":closest_enemy", -1),
            (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":enemy_agent"),
            
          (else_try),
            (agent_get_position, pos0, ":enemy_agent"),
            (get_distance_between_positions, ":new_distance", pos0, pos1),
            (agent_get_position, pos0, ":closest_enemy"),
            (get_distance_between_positions, ":old_distance", pos0, pos1),
            (lt, ":new_distance", ":old_distance"),
            (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":enemy_agent"),
          (try_end),
        (try_end),
        (try_begin),
          (agent_slot_eq, ":cur_agent", slot_agent_nearest_enemy_agent, -1),
          (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":nearest_runner"),
        (try_end),
        
        #exploit closest agent data
        (try_begin),
          (agent_get_slot, ":closest_enemy", ":cur_agent", slot_agent_nearest_enemy_agent),
          (neq, ":closest_enemy", -1),
          (agent_get_position, pos0, ":closest_enemy"),
          (get_distance_between_positions, ":closest_distance", pos0, pos1),
          
          #check target of AI agent behavior
          (try_begin),
            (agent_is_non_player, ":cur_agent"),
            
            (agent_ai_get_behavior_target, ":cur_targeted_agent", ":cur_agent"),
            (neq, ":closest_enemy", ":cur_targeted_agent"),
            
            (this_or_next | neg | agent_is_non_player, ":closest_enemy"),	#AI can always sense player behind them (balancing factor, dedicated to
            #Idibil)
            (neg | position_is_behind_position, pos0, pos1),
            
            (lt, ":closest_distance", 2000),	#Assuming rethink is expensive, don't bother beyond 20m
            
            (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (this_or_next | eq, formation_rethink_for_formations_only, 0),
            (gt, ":value", formation_none),
            
            (agent_force_rethink, ":cur_agent"),
          (try_end),
          
          #update division information
          (try_begin),
            (ge, ":bgdivision", 0),	#not leaders
            
            (try_begin),
              (lt, ":closest_distance", 350),
              (agent_get_division, reg0, ":closest_enemy"),
              (store_add, ":slot", slot_team_d0_enemy_supporting_melee, reg0),
              (agent_get_group, reg0, ":closest_enemy"),
              (team_get_slot, ":value", reg0, ":slot"),
              (val_add, ":value", 1),
              (team_set_slot, reg0, ":slot", ":value"),
            (try_end),
            
            (store_add, ":slot", slot_team_d0_closest_enemy_dist, ":bgdivision"),
            (team_get_slot, ":old_distance", ":bgteam", ":slot"),
            (try_begin),
              (this_or_next | eq, ":old_distance", 0),
              (lt, ":closest_distance", ":old_distance"),
              (team_set_slot, ":bgteam", ":slot", ":closest_distance"),
              (store_add, ":slot", slot_team_d0_closest_enemy, ":bgdivision"),
              (team_set_slot, ":bgteam", ":slot", ":closest_enemy"),
            (try_end),
            
            (assign, ":doit", 0),
            (agent_get_class, ":enemy_agent_class", ":closest_enemy"),
            (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),
            
            #AI infantry division tracks non-infantry to preferably chase
            (try_begin),
              (this_or_next | eq, ":value", sdt_polearm),
              (eq, ":value", sdt_infantry),
              (neq, ":enemy_agent_class", grc_cavalry),
              (assign, ":doit", 1),
              
              #AI archer division tracks infantry to avoid
            (else_try),
              (this_or_next | eq, ":value", sdt_archer),
              (eq, ":value", sdt_skirmisher),
              (eq, ":enemy_agent_class", grc_infantry),
              (assign, ":doit", 1),
            (try_end),
            
            (eq, ":doit", 1),
            (store_add, ":slot", slot_team_d0_closest_enemy_special_dist, ":bgdivision"),
            (team_get_slot, ":old_distance", ":bgteam", ":slot"),
            (try_begin),
              (this_or_next | eq, ":old_distance", 0),
              (lt, ":closest_distance", ":old_distance"),
              (team_set_slot, ":bgteam", ":slot", ":closest_distance"),
              (store_add, ":slot", slot_team_d0_closest_enemy_special, ":bgdivision"),
              (team_set_slot, ":bgteam", ":slot", ":closest_enemy"),
            (try_end),
          (try_end),	#update division info
        (try_end),	#exploit closest agent data
      (try_end), #Agent Loop
      
      #calculate team sizes, sum positions; within calculate battle group averages
      (try_for_range, ":team", 0, 4),
        (assign, ":team_size", 0),
        (assign, ":team_level", 0),
        (assign, ":team_x", 0),
        (assign, ":team_y", 0),
        (assign, ":team_zrot", 0),
        
        (try_for_range, ":division", 0, 9),
          #sum for team averages
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_get_slot, ":division_size", ":team", ":slot"),
          (gt, ":division_size", 0),
          (val_add, ":team_size", ":division_size"),
          
          (store_add, ":slot", slot_team_d0_level, ":division"),
          (team_get_slot, ":division_level", ":team", ":slot"),
          (val_add, ":team_level", ":division_level"),
          
          (store_add, ":slot", slot_team_d0_avg_x, ":division"),
          (team_get_slot, ":division_x", ":team", ":slot"),
          (val_add, ":team_x", ":division_x"),
          
          (store_add, ":slot", slot_team_d0_avg_y, ":division"),
          (team_get_slot, ":division_y", ":team", ":slot"),
          (val_add, ":team_y", ":division_y"),
          
          (store_add, ":slot", slot_team_d0_avg_zrot, ":division"),
          (team_get_slot, ":division_zrot", ":team", ":slot"),
          (val_add, ":team_zrot", ":division_zrot"),
          
          #calculate battle group averages
          (store_add, ":slot", slot_team_d0_level, ":division"),
          (val_div, ":division_level", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_level"),
          
          (store_add, ":slot", slot_team_d0_percent_ranged, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_mul, ":value", 100),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),
          
          (store_add, ":slot", slot_team_d0_percent_throwers, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_mul, ":value", 100),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),
          
          (store_add, ":slot", slot_team_d0_weapon_length, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),
          
          # (store_add, ":slot", slot_team_d0_swung_weapon_length, ":division"), MOTO
          # systematic testing shows best to use max swung weapon length as basis for
          # formation spacing
          # (team_get_slot, ":value", ":team", ":slot"),
          # (val_div, ":value", ":division_size"),
          # (team_set_slot, ":team", ":slot", ":value"),
          
          # (store_add, ":slot", slot_team_d0_front_agents, ":division"), MOTO front
          # rank should be within shortest weapon distance, not average
          # (team_get_slot, reg0, ":team", ":slot"),
          # (try_begin),
          # (gt, reg0, 0),
          # (store_add, ":slot", slot_team_d0_front_weapon_length, ":division"),
          # (team_get_slot, ":value", ":team", ":slot"),
          # (val_div, ":value", reg0),
          # (team_set_slot, ":team", ":slot", ":value"),
          # (try_end),
          
          (store_add, ":slot", slot_team_d0_avg_x, ":division"),
          (val_div, ":division_x", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_x"),
          
          (store_add, ":slot", slot_team_d0_avg_y, ":division"),
          (val_div, ":division_y", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_y"),
          
          (store_add, ":slot", slot_team_d0_avg_zrot, ":division"),
          (val_div, ":division_zrot", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_zrot"),
          
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (team_get_slot, reg0, ":team", ":slot"),
          (try_begin),
            (neg | is_between, reg0, 0, 8),	#TODO reset on reinforcements
            (call_script, "script_store_battlegroup_type_moto", ":team", ":division"),
          (try_end),
        (try_end), #Division Loop
        
        #Team Leader Additions
        (try_begin),
          (eq, ":team", 0),
          (val_add, ":team_size", ":team0_leader"),
          (val_add, ":team_level", ":team0_level_leader"),
          (val_add, ":team_x", ":team0_x_leader"),
          (val_add, ":team_y", ":team0_y_leader"),
          (val_add, ":team_zrot", ":team0_zrot_leader"),
        (else_try),
          (eq, ":team", 1),
          (val_add, ":team_size", ":team1_leader"),
          (val_add, ":team_level", ":team1_level_leader"),
          (val_add, ":team_x", ":team1_x_leader"),
          (val_add, ":team_y", ":team1_y_leader"),
          (val_add, ":team_zrot", ":team1_zrot_leader"),
        (else_try),
          (eq, ":team", 2),
          (val_add, ":team_size", ":team2_leader"),
          (val_add, ":team_level", ":team2_level_leader"),
          (val_add, ":team_x", ":team2_x_leader"),
          (val_add, ":team_y", ":team2_y_leader"),
          (val_add, ":team_zrot", ":team2_zrot_leader"),
        (else_try),
          (eq, ":team", 3),
          (val_add, ":team_size", ":team3_leader"),
          (val_add, ":team_level", ":team3_level_leader"),
          (val_add, ":team_x", ":team3_x_leader"),
          (val_add, ":team_y", ":team3_y_leader"),
          (val_add, ":team_zrot", ":team3_zrot_leader"),
        (try_end),
        
        #calculate team averages
        (gt, ":team_size", 0),
        (team_set_slot, ":team", slot_team_size, ":team_size"),
        (val_div, ":team_level", ":team_size"),
        (team_set_slot, ":team", slot_team_level, ":team_level"),
        
        (val_div, ":team_x", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_x, ":team_x"),
        (val_div, ":team_y", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_y, ":team_y"),
        (val_div, ":team_zrot", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_zrot, ":team_zrot"),
      (try_end), #Team Loop
  ]),
  
  # script_cf_division_data_available by motomataru
  ("cf_division_data_available_moto", [
      (assign, ":evidence", 0),
      (try_for_range, ":team", 0, 4),
        (team_slot_ge, ":team", slot_team_size, 1),
        (assign, ":evidence", 1),
      (try_end),
      (neq, ":evidence", 0)]),
  
  # script_battlegroup_get_position by motomataru #CABA - EDITED TO USE SLOTS,
  # NOT STORED POS NUMBERS
  # Input: destination position, team, division
  # Output: battle group position
  #			average team position if division input NOT set to 0-8
  ("battlegroup_get_position_moto", [
      (store_script_param, ":bgposition", 1),
      (store_script_param, ":bgteam", 2),
      (store_script_param, ":bgdivision", 3),
      
      (assign, ":x", 0),
      (assign, ":y", 0),
      (init_position, ":bgposition"),
      (try_begin),
        (neg | is_between, ":bgdivision", 0, 9),
        (team_slot_ge, ":bgteam", slot_team_size, 1),
        (team_get_slot, ":x", ":bgteam", slot_team_avg_x),
        (team_get_slot, ":y", ":bgteam", slot_team_avg_y),
        (team_get_slot, ":zrot", ":bgteam", slot_team_avg_zrot),
      (else_try),
        (is_between, ":bgdivision", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
        (team_slot_ge, ":bgteam", ":slot", 1),
        
        (store_add, ":slot", slot_team_d0_avg_x, ":bgdivision"),
        (team_get_slot, ":x", ":bgteam", ":slot"),
        
        (store_add, ":slot", slot_team_d0_avg_y, ":bgdivision"),
        (team_get_slot, ":y", ":bgteam", ":slot"),
        
        (store_add, ":slot", slot_team_d0_avg_zrot, ":bgdivision"),
        (team_get_slot, ":zrot", ":bgteam", ":slot"),
      (try_end),
      (position_set_x, ":bgposition", ":x"),
      (position_set_y, ":bgposition", ":y"),
      (position_rotate_z, ":bgposition", ":zrot", 0),
      (position_set_z_to_ground_level, ":bgposition"),]),
  
  # script_battlegroup_get_attack_destination by motomataru
  # Input: destination position, team, division, target team, target division
  # Output: melee position against target battlegroup
  ("battlegroup_get_attack_destination_moto", [
      (store_script_param, ":bgposition", 1),
      (store_script_param, ":bgteam", 2),
      (store_script_param, ":bgdivision", 3),
      (store_script_param, ":enemy_team", 4),
      (store_script_param, ":enemy_division", 5),
      
      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":bgformation", ":bgteam", ":slot"),
      (try_begin),
        (le, ":bgformation", formation_none),
        (call_script, "script_battlegroup_get_position_moto", ":bgposition", ":bgteam", ":bgdivision"),
      (else_try),
        (call_script, "script_formation_current_position_moto", ":bgposition", ":bgteam", ":bgdivision"),
      (try_end),
      
      #distance to enemy center
      (store_add, ":slot", slot_team_d0_formation, ":enemy_division"),
      (team_get_slot, ":enemy_formation", ":enemy_team", ":slot"),
      (call_script, "script_battlegroup_get_position_moto", Enemy_Team_Pos_MOTO, ":enemy_team", ":enemy_division"),
      (get_distance_between_positions, ":distance_to_move", ":bgposition", Enemy_Team_Pos_MOTO),
      
      (call_script, "script_battlegroup_get_action_radius_moto", ":bgteam", ":bgdivision"),
      (assign, ":bgwidth", reg0),
      (call_script, "script_battlegroup_get_action_radius_moto", ":enemy_team", ":enemy_division"),
      (store_add, ":combined_width", ":bgwidth", reg0),
      
      (assign, ":min_radius", reg0),
      (val_min, ":min_radius", ":bgwidth"),
      (val_div, ":min_radius", 2),	#function returns length of bg
      
      (try_begin),
        (gt, ":bgformation", formation_none),	#in formation AND
        (le, ":distance_to_move", ":combined_width"),	#close to enemy
        (store_mul, reg0, -350, formation_reform_interval),	#back up one move (to avoid wild swings / reversals on overruns)
        (position_move_y, ":bgposition", reg0),
        (get_distance_between_positions, ":distance_to_move", ":bgposition", Enemy_Team_Pos_MOTO),
      (try_end),
      
      #subtract enemy center to edge-of-contact (determined by minimum half-width
      #between the two battlegroups)
      (call_script, "script_get_distance_to_battlegroup_moto", ":enemy_team", ":enemy_division", ":bgposition"),
      (store_mul, ":angle_adjusted_half_depth", ":min_radius", reg2),	#reg2 is cosine glancing angle, FP
      (convert_from_fixed_point, ":angle_adjusted_half_depth"),
      (try_begin),
        (neq, ":enemy_formation", formation_wedge),
        (call_script, "script_battlegroup_dist_center_to_front_moto", ":enemy_team", ":enemy_division"),
        (val_max, ":angle_adjusted_half_depth", reg0),
      (try_end),
      (val_sub, ":distance_to_move", ":angle_adjusted_half_depth"),
      
      #modify by bg center to edge-of-contact, if needed
      (call_script, "script_battlegroup_dist_center_to_front_moto", ":bgteam", ":bgdivision"),
      (assign, ":bg_half_depth", reg0),
      (try_begin),
        (le, ":bgformation", formation_none),
        (val_sub, ":distance_to_move", ":bg_half_depth"),	#position from script_battlegroup_get_position is in middle of bg
      (else_try),
        (eq, ":bgformation", formation_wedge),
        (call_script, "script_battlegroup_dist_center_to_front_moto", ":enemy_team", ":enemy_division"),
        (val_add, ":distance_to_move", reg0),	#move in from nearest edge found by script_get_distance_to_battlegroup
        (val_add, ":distance_to_move", ":bg_half_depth"),	#drive wedge through target formation!
      (try_end),
      
      #modify by speed differential
      (try_begin),
        (gt, ":enemy_formation", formation_none),
        (neq, ":enemy_formation", formation_default),
        
        (store_add, ":slot", slot_team_d0_first_member, ":enemy_division"),
        (team_get_slot, reg0, ":enemy_team", ":slot"),
        (agent_is_active, reg0),
        
        (agent_get_speed, Speed_Pos, reg0),
        (init_position, Temp_Pos),
        (get_distance_between_positions, ":enemy_formation_speed", Speed_Pos, Temp_Pos),
        (val_mul, ":enemy_formation_speed", formation_reform_interval),	#calculate distance to next call
        
        (try_begin),
          (position_is_behind_position, ":bgposition", Enemy_Team_Pos_MOTO),	#attacking from rear?
          (val_add, ":distance_to_move", ":enemy_formation_speed"),	#catch up to anticipated position
        (else_try),	#attacking enemy formation from front
          (store_add, ":slot", slot_team_d0_is_fighting, ":bgdivision"),
          (team_slot_eq, ":bgteam", ":slot", 0),
          (val_sub, ":distance_to_move", ":enemy_formation_speed"),	#avoid overrunning enemy
        (try_end),
      (try_end),
      
      (store_add, ":slot", slot_team_d0_front_weapon_length, ":bgdivision"),
      (team_get_slot, ":striking_distance", ":bgteam", ":slot"),
      (val_sub, ":distance_to_move", ":striking_distance"),
      
      (call_script, "script_point_y_toward_position_moto", ":bgposition", Enemy_Team_Pos_MOTO),
      (position_move_y, ":bgposition", ":distance_to_move"),]),
  
  # script_battlegroup_dist_center_to_front by motomataru
  # Input: team, division
  # Output: reg0 distance to front of battlegroup from center in cm
  ("battlegroup_dist_center_to_front_moto", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),
      
      (store_add, ":slot", slot_team_d0_formation_space, ":bgdivision"),
      (team_get_slot, ":spacing", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":bgformation", ":bgteam", ":slot"),
      
      (try_begin),
        (eq, ":bgformation", formation_none),	#single row
        (assign, ":depth", 0),
        
        #WFaS multi-ranks
      (else_try),
        (eq, ":bgformation", formation_2_row),
        (assign, ":depth", 100),
      (else_try),
        (eq, ":bgformation", formation_3_row),
        (assign, ":depth", 200),
      (else_try),
        (eq, ":bgformation", formation_4_row),
        (assign, ":depth", 300),
      (else_try),
        (eq, ":bgformation", formation_5_row),
        (assign, ":depth", 400),
        
      (else_try),	#WB multi-ranks
        (lt, ":spacing", 0),
        (store_mul, ":depth", ":spacing", -1),
        (val_mul, ":depth", 100),
        
      #Non Native
      (else_try),
        (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
        (team_get_slot, ":size_enemy_battlegroup", ":bgteam", ":slot"),
        (store_mul, ":row_depth", ":spacing", 50),
        (val_add, ":row_depth", formation_minimum_spacing),
        
        (this_or_next | eq, ":bgformation", formation_ranks),
        (eq, ":bgformation", formation_shield),
        (call_script, "script_calculate_default_ranks_moto", ":size_enemy_battlegroup"),
        (val_sub, reg1, 1),
        (store_mul, ":depth", ":row_depth", reg1),
        
      (else_try),
        (convert_to_fixed_point, ":size_enemy_battlegroup"),
        (store_sqrt, ":columns", ":size_enemy_battlegroup"),
        
        (eq, ":bgformation", formation_square),
        (convert_from_fixed_point, ":columns"),
        (val_add, ":columns", 1),	#see script_form_infantry
        (store_div, ":rows", ":size_enemy_battlegroup", ":columns"),
        (store_mul, ":depth", ":row_depth", ":rows"),
        (convert_from_fixed_point, ":depth"),
        (val_sub, ":depth", ":row_depth"),
        
      (else_try),
        (eq, ":bgformation", formation_wedge),
        (store_mul, ":depth", ":row_depth", ":columns"),	#approximation
        (convert_from_fixed_point, ":depth"),
      (try_end),
      
      (try_begin),
        (neq, ":bgformation", formation_wedge),
        (store_div, reg0, ":depth", 2),
      (else_try),
        (store_mul, reg0, ":depth", 2),	#another approximation (height - inner radius)
        (val_div, reg0, 3),
      (try_end),]),
  
  # script_battlegroup_get_action_radius by motomataru
  # Input: team, division
  # Output: reg0 radius of battlegroup's "zone of control" (now length of
  # battlegroup in cm)
  ("battlegroup_get_action_radius_moto", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),
      
      (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
      (team_get_slot, ":size_battlegroup", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":formation", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
      (team_get_slot, ":div_type", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation_space, ":bgdivision"),
      (team_get_slot, ":spacing", ":bgteam", ":slot"),
      
      (try_begin),
        (this_or_next | eq, ":div_type", sdt_archer),
        (le, ":formation", formation_none),	#Native formation
        
        (store_mul, ":troop_space", ":spacing", 75),	#Native minimum spacing not consistent but about this
        (val_add, ":troop_space", 100),	#minimum spacing
        
        #WFaS multi-ranks
        (try_begin),
          (eq, ":formation", formation_2_row),
          (val_div, ":size_battlegroup", 2),
        (else_try),
          (eq, ":formation", formation_3_row),
          (val_div, ":size_battlegroup", 3),
        (else_try),
          (eq, ":formation", formation_4_row),
          (val_div, ":size_battlegroup", 4),
        (else_try),
          (eq, ":formation", formation_5_row),
          (val_div, ":size_battlegroup", 5),
          
        (else_try),	#WB multi-ranks
          (lt, ":spacing", 0),
          (assign, ":troop_space", 150),
          (val_mul, ":spacing", -1),
          (val_add, ":spacing", 1),
          (val_div, ":size_battlegroup", ":spacing"),
        (try_end),
        
        (store_mul, ":formation_width", ":size_battlegroup", ":troop_space"),
        (store_div, reg0, ":formation_width", 2),
        
      (else_try),
        (eq, ":formation", formation_wedge),
        (call_script, "script_get_centering_amount_moto", formation_square, ":size_battlegroup", ":spacing"),	#approximation
        (val_mul, reg0, 7),
        (val_div, reg0, 6),
      (else_try),
        (try_begin),
          (lt, ":spacing", 0),
          (assign, reg0, ":bgteam"),
          (assign, reg1, ":bgdivision"),
          (assign, reg2, ":formation"),
          (display_message, "@{!}battlegroup_get_action_radius: negative radius for team {reg0} division {reg1} formation {reg2}"),
        (try_end),
        (call_script, "script_get_centering_amount_moto", ":formation", ":size_battlegroup", ":spacing"),
      (try_end),
      
      (val_mul, reg0, 2),]),
  
  # script_team_get_position_of_enemies by motomataru
  # Input: destination position, team, troop class/division
  # Output: destination position: average position if reg0 > 0
  #			reg0: number of enemies
  # Run script_store_battlegroup_data before calling!
  ("team_get_position_of_enemies_moto", [
      (store_script_param, ":enemy_position", 1),
      (store_script_param, ":team_no", 2),
      (store_script_param, ":troop_type", 3),
      (assign, ":pos_x", 0),
      (assign, ":pos_y", 0),
      (assign, ":total_size", 0),
      (try_begin),
        (neq, ":troop_type", grc_everyone),
        (assign, ":closest_distance", Far_Away),
        (call_script, "script_battlegroup_get_position_moto", Temp_Pos, ":team_no", grc_everyone),
      (try_end),
      
      (try_for_range, ":other_team", 0, 4),
        (teams_are_enemies, ":other_team", ":team_no"),
        (try_begin),
          (eq, ":troop_type", grc_everyone),
          (team_get_slot, ":team_size", ":other_team", slot_team_size),
          (try_begin),
            (gt, ":team_size", 0),
            (call_script, "script_battlegroup_get_position_moto", ":enemy_position", ":other_team", grc_everyone),
            (position_get_x, reg0, ":enemy_position"),
            (val_mul, reg0, ":team_size"),
            (val_add, ":pos_x", reg0),
            (position_get_y, reg0, ":enemy_position"),
            (val_mul, reg0, ":team_size"),
            (val_add, ":pos_y", reg0),
          (try_end),
        (else_try),	#for multiple divisions, should find the CLOSEST of a given type
          (assign, ":team_size", 0),
          (try_for_range, ":enemy_battle_group", 0, 9),
            (store_add, ":slot", slot_team_d0_size, ":enemy_battle_group"),
            (team_get_slot, ":troop_count", ":other_team", ":slot"),
            (gt, ":troop_count", 0),
            (store_add, ":slot", slot_team_d0_type, ":enemy_battle_group"),
            (team_get_slot, ":bg_type", ":other_team", ":slot"),
            (store_sub, ":bg_root_type", ":bg_type", 3), #subtype is three more than main type
            (this_or_next | eq, ":bg_type", ":troop_type"),
            (eq, ":bg_root_type", ":troop_type"),
            (val_add, ":team_size", ":troop_count"),
            (call_script, "script_battlegroup_get_position_moto", ":enemy_position", ":other_team", ":enemy_battle_group"),
            (get_distance_between_positions, reg0, Temp_Pos, ":enemy_position"),
            (lt, reg0, ":closest_distance"),
            (assign, ":closest_distance", reg0),
            (position_get_x, ":pos_x", ":enemy_position"),
            (position_get_y, ":pos_y", ":enemy_position"),
          (try_end),
        (try_end),
        (val_add, ":total_size", ":team_size"),
      (try_end),
      
      (try_begin),
        (eq, ":total_size", 0),
        (init_position, ":enemy_position"),
      (else_try),
        (eq, ":troop_type", grc_everyone),
        (val_div, ":pos_x", ":total_size"),
        (position_set_x, ":enemy_position", ":pos_x"),
        (val_div, ":pos_y", ":total_size"),
        (position_set_y, ":enemy_position", ":pos_y"),
        (position_set_z_to_ground_level, ":enemy_position"),
      (else_try),
        (position_set_x, ":enemy_position", ":pos_x"),
        (position_set_y, ":enemy_position", ":pos_y"),
        (position_set_z_to_ground_level, ":enemy_position"),
      (try_end),
      
      (assign, reg0, ":total_size"),]),
  
  # script_get_distance_to_battlegroup by motomataru
  # Gets distance from "from position" to the theoretical nearest side of the
  # battlegroup, accounting for rotation of battlegroup
  # Input: bg team, bg division, from position
  # Output: reg2 abs (cos (BG direction - 90 - direction from "from position"))
  # fixed point
  #         reg1 BG radius x reg2 in cms
  #         reg0 distance in cms between BG position and "from position" minus
  #         reg1 (could be negative)
  # Uses pos0, pos61
  ("get_distance_to_battlegroup_moto", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),
      (store_script_param, ":from_pos", 3),
      
      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":bgformation", ":bgteam", ":slot"),
      (call_script, "script_battlegroup_get_action_radius_moto", ":bgteam", ":bgdivision"),
      (store_div, ":radius", reg0, 2),	#function returns length of bg
      (assign, ":min_cos_theta", 1),
      (convert_to_fixed_point, ":min_cos_theta"),
      (try_begin),
        (eq, ":bgformation", formation_wedge),
        (val_mul, ":min_cos_theta", 58),	#relation inscribed circle radius to half side: 1 / sqrt 3
        (val_div, ":min_cos_theta", 100),
      (else_try),
        (gt, ":radius", 0),
        (call_script, "script_battlegroup_dist_center_to_front_moto", ":bgteam", ":bgdivision"),
        (val_mul, ":min_cos_theta", reg0),
        (val_div, ":min_cos_theta", ":radius"),
      (else_try),
        (assign, ":min_cos_theta", 0),
      (try_end),
      
      #acquire rotations
      (call_script, "script_battlegroup_get_position_moto", pos0, ":bgteam", ":bgdivision"),
      (try_begin),
        (gt, ":bgformation", formation_none),
        (neq, ":bgformation", formation_default),
        (call_script, "script_get_formation_destination_moto", pos61, ":bgteam", ":bgdivision"),
        (position_copy_rotation, pos0, pos61),
      (try_end),
      
      (copy_position, pos61, ":from_pos"),
      (call_script, "script_point_y_toward_position_moto", pos61, pos0),
      (assign, ":distance_to_battlegroup", reg0),
      
      #calculate difference from center of bg
      (get_angle_between_positions, ":theta", pos61, pos0),
      (val_sub, ":theta", 9000),
      (store_cos, ":cos_theta", ":theta"),
      (val_abs, ":cos_theta"),
      (val_max, ":cos_theta", ":min_cos_theta"),	#doing depth considerations this way allows calling func to use angle; it also
      #avoids Pythagorean calcs
      
      (store_mul, reg1, ":radius", ":cos_theta"),
      (convert_from_fixed_point, reg1),
      (val_sub, ":distance_to_battlegroup", reg1),
      (assign, reg0, ":distance_to_battlegroup"),
      (assign, reg2, ":cos_theta"),]),
  
  # script_get_item_modifier_effects
  # Input: itp_*, imod_*
  # Output: reg0 damage effect
  #         reg1 speed effect
  #         reg2 armor effect
  #         reg3 hit points effect
  #         reg4 difficulty effect
  #         reg5 price factor
  #         s0 descriptor string
  # derived from autoloot by Rubik
  ("get_item_modifier_effects_moto", [(store_script_param, ":type", 1),
      (store_script_param, ":imod", 2),
      
      (assign, ":damage", 0),
      (assign, ":speed", 0),
      (assign, ":armor", 0),
      (assign, ":hit_points", 0),
      (assign, ":difficulty", 0),
      (assign, ":price_factor", 100),
      
      (try_begin),
        (eq, ":type", itp_type_horse),
        (try_begin),
          (eq, ":imod", imod_lame),
          (assign, ":speed", -10),
          (assign, ":price_factor", 40),
          (str_store_string, s0, "@Lame"),
        (else_try),
          (eq, ":imod", imod_swaybacked),
          (assign, ":speed", -4),
          (assign, ":price_factor", 60),
          (str_store_string, s0, "@Swaybacked"),
        (else_try),
          (eq, ":imod", imod_timid),
          (assign, ":speed", 2),
          (assign, ":price_factor", 120),
          (str_store_string, s0, "@Timid"),
        (else_try),
          (eq, ":imod", imod_meek),
          (assign, ":speed", 2),
          (assign, ":price_factor", 120),
          (str_store_string, s0, "@Meek"),
        (else_try),
          (eq, ":imod", imod_stubborn),
          (assign, ":hit_points", 5),
          (assign, ":difficulty", 1),
          (assign, ":price_factor", 90),
          (str_store_string, s0, "@Stubborn"),
        (else_try),
          (eq, ":imod", imod_heavy),
          (assign, ":damage", 4),
          (assign, ":armor", 3),
          (assign, ":hit_points", 10),
          (assign, ":price_factor", 150),
          (str_store_string, s0, "@Heavy"),
        (else_try),
          (eq, ":imod", imod_spirited),
          (assign, ":damage", 1),
          (assign, ":speed", 2),
          (assign, ":price_factor", 160),
          (str_store_string, s0, "@Spirited"),
        (else_try),
          (eq, ":imod", imod_champion),
          (assign, ":damage", 2),
          (assign, ":speed", 4),
          (assign, ":difficulty", 2),
          (assign, ":price_factor", 170),
          (str_store_string, s0, "@Champion"),
        (try_end),
        
      (else_try),
        (eq, ":type", itp_type_shield),
        (try_begin),
          (eq, ":imod", imod_cracked),
          (assign, ":armor", -4),
          (assign, ":hit_points", -56),
          (assign, ":price_factor", 50),
          (str_store_string, s0, "@Cracked"),
        (else_try),
          (eq, ":imod", imod_battered),
          (assign, ":armor", -2),
          (assign, ":hit_points", -26),
          (assign, ":price_factor", 75),
          (str_store_string, s0, "@Battered"),
        (else_try),
          (eq, ":imod", imod_thick),
          (assign, ":armor", 2),
          (assign, ":hit_points", 47),
          (assign, ":price_factor", 120),
          (str_store_string, s0, "@Thick"),
        (else_try),
          (eq, ":imod", imod_reinforced),
          (assign, ":armor", 4),
          (assign, ":hit_points", 63),
          (assign, ":price_factor", 150),
          (str_store_string, s0, "@Reinforced"),
        (try_end),
        
      (else_try),
        (ge, ":type", itp_type_head_armor),
        (le, ":type", itp_type_hand_armor),
        (try_begin),
          (eq, ":imod", imod_cracked),
          (assign, ":armor", -4),
          (assign, ":price_factor", 50),
          (str_store_string, s0, "@Cracked"),
        (else_try),
          (eq, ":imod", imod_rusty),
          (assign, ":armor", -3),
          (assign, ":price_factor", 55),
          (str_store_string, s0, "@Rusty"),
        (else_try),
          (eq, ":imod", imod_tattered),
          (assign, ":armor", -3),
          (assign, ":price_factor", 40),
          (str_store_string, s0, "@Tattered"),
        (else_try),
          (eq, ":imod", imod_ragged),
          (assign, ":armor", -2),
          (assign, ":price_factor", 60),
          (str_store_string, s0, "@Ragged"),
        (else_try),
          (eq, ":imod", imod_battered),
          (assign, ":armor", -2),
          (assign, ":price_factor", 75),
          (str_store_string, s0, "@Battered"),
        (else_try),
          (eq, ":imod", imod_crude),
          (assign, ":armor", -1),
          (assign, ":price_factor", 83),
          (str_store_string, s0, "@Crude"),
        (else_try),
          (eq, ":imod", imod_sturdy),
          (assign, ":armor", 1),
          (assign, ":price_factor", 120),
          (str_store_string, s0, "@Sturdy"),
        (else_try),
          (eq, ":imod", imod_thick),
          (assign, ":armor", 2),
          (assign, ":price_factor", 140),
          (str_store_string, s0, "@Thick"),
        (else_try),
          (eq, ":imod", imod_hardened),
          (assign, ":armor", 3),
          (assign, ":price_factor", 160),
          (str_store_string, s0, "@Hardened"),
        (else_try),
          (eq, ":imod", imod_reinforced),
          (assign, ":armor", 4),
          (assign, ":price_factor", 180),
          (str_store_string, s0, "@Reinforced"),
        (else_try),
          (eq, ":imod", imod_lordly),
          (assign, ":armor", 5),
          (assign, ":price_factor", 400),
          (str_store_string, s0, "@Lordly"),
        (try_end),
        
      (else_try),
        (this_or_next | eq, ":type", itp_type_one_handed_wpn),
        (this_or_next | eq, ":type", itp_type_two_handed_wpn),
        (this_or_next | eq, ":type", itp_type_polearm),
        (this_or_next | eq, ":type", itp_type_bow),
        (this_or_next | eq, ":type", itp_type_crossbow),
        (this_or_next | eq, ":type", itp_type_pistol),
        (eq, ":type", itp_type_musket),
        
        (try_begin),
          (eq, ":imod", imod_rotten),		#idea is to use this for a completly broken weapon
          (assign, ":damage", -20),
          (assign, ":price_factor", 5),
          (str_store_string, s0, "@Broken"),
        (else_try),
          (eq, ":imod", imod_cracked),
          (assign, ":damage", -5),
          (assign, ":price_factor", 40),
          (str_store_string, s0, "@Cracked"),
        (else_try),
          (eq, ":imod", imod_rusty),
          (assign, ":damage", -3),
          (assign, ":price_factor", 55),
          (str_store_string, s0, "@Rusty"),
        (else_try),
          (eq, ":imod", imod_bent),
          (assign, ":damage", -3),
          (assign, ":speed", -3),
          (assign, ":price_factor", 60),
          (str_store_string, s0, "@Bent"),
        (else_try),
          (eq, ":imod", imod_chipped),
          (assign, ":damage", -1),
          (assign, ":price_factor", 72),
          (str_store_string, s0, "@Chipped"),
        (else_try),
          (eq, ":imod", imod_heavy),
          (assign, ":damage", 2),
          (assign, ":speed", -2),
          (assign, ":difficulty", 1),
          (assign, ":price_factor", 120),
          (str_store_string, s0, "@Heavy"),
        (else_try),
          (eq, ":imod", imod_strong),
          (assign, ":damage", 3),
          (assign, ":speed", -3),
          (assign, ":difficulty", 2),
          (assign, ":price_factor", 150),
          (str_store_string, s0, "@Strong"),
        (else_try),
          (eq, ":imod", imod_balanced),
          (assign, ":damage", 3),
          (assign, ":speed", 3),
          (assign, ":price_factor", 165),
          (str_store_string, s0, "@Balanced"),
        (else_try),
          (eq, ":imod", imod_tempered),
          (assign, ":damage", 4),
          (assign, ":price_factor", 180),
          (str_store_string, s0, "@Tempered"),
        (else_try),
          (eq, ":imod", imod_masterwork),
          (assign, ":damage", 5),
          (assign, ":speed", 1),
          (assign, ":difficulty", 4),
          (assign, ":price_factor", 400),
          (str_store_string, s0, "@Masterwork"),
        (else_try),
          (eq, ":imod", imod_crude),
          (assign, ":damage", -2),
          (assign, ":price_factor", 83),
        (try_end),
        
      (else_try),
        (this_or_next | eq, ":type", itp_type_arrows),
        (this_or_next | eq, ":type", itp_type_bolts),
        (this_or_next | eq, ":type", itp_type_bullets),
        (eq, ":type", itp_type_thrown),
        
        (try_begin),
          (eq, ":imod", imod_large_bag),
          #       (assign, ":damage", 1), #just make better than plain
          (assign, ":price_factor", 110),
          (str_store_string, s0, "@Large Bag of"),
        (else_try),
          (eq, ":imod", imod_bent),
          (assign, ":damage", -3),
          (assign, ":price_factor", 65),
          (str_store_string, s0, "@Bent"),
        (else_try),
          (eq, ":imod", imod_cracked),
          (assign, ":damage", -5),
          (assign, ":price_factor", 50),
          (str_store_string, s0, "@Cracked"),
        (else_try),
          (eq, ":imod", imod_heavy),
          (assign, ":damage", 2),
          (assign, ":price_factor", 130),
          (str_store_string, s0, "@Heavy"),
        (else_try),
          (eq, ":imod", imod_balanced),
          (assign, ":damage", 3),
          (assign, ":price_factor", 150),
          (str_store_string, s0, "@Balanced"),
        (try_end),
      (try_end),
      
      (assign, reg0, ":damage"),
      (assign, reg1, ":speed"),
      (assign, reg2, ":armor"),
      (assign, reg3, ":hit_points"),
      (assign, reg4, ":difficulty"),
      (assign, reg5, ":price_factor"),]),
      
  # script_evaluate_item moto chief
  # Input: item_id, item_mod
  # Output: reg0 value meant to compare items of a given type
  ("evaluate_item_moto", [
      (store_script_param, ":item_id", 1),
      (store_script_param, ":item_mod", 2),
      
      (assign, ":ret_val", 0),
      (try_begin),
        (gt, ":item_id", "itm_no_item"),
        
        (item_get_type, ":item_type", ":item_id"),
        (call_script, "script_get_item_modifier_effects_moto", ":item_type", ":item_mod"),
        (assign, ":damage", reg0),
        (assign, ":speed", reg1),
        (assign, ":armor", reg2),
        (assign, ":hit_points", reg3),
        
        #Armor
        (try_begin),
          (ge, ":item_type", itp_type_head_armor),
          (le, ":item_type", itp_type_hand_armor),
          
          #construct comparison value
          (item_get_head_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (item_get_body_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (item_get_leg_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (assign, ":ret_val", ":armor"),
          
          #Ranged Weapons
        (else_try),
          (call_script, "script_cf_is_weapon_ranged_moto", ":item_id", 1),
          
          #construct comparison value
          (item_get_thrust_damage, ":value", ":item_id"),
          (val_add, ":damage", ":value"),
          
          (item_get_speed_rating, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":damage", ":value"),
          
          (item_get_missile_speed,  ":value", ":item_id"),
          (val_mul, ":damage", ":value"),
          
          (item_get_accuracy, ":value", ":item_id"),
          (val_mul, ":damage", ":value"),
          (assign, ":ret_val", ":damage"),
          
          #Melee Weapons
        (else_try),
          (ge, ":item_type", itp_type_one_handed_wpn),
          (le, ":item_type", itp_type_polearm),
          
          #construct comparison value
          (item_get_thrust_damage, ":value", ":item_id"),
          (item_get_swing_damage, reg2, ":item_id"),
          (val_max, ":value", reg2),  #TW formula.  Also avoids problems with script_switch_to_noswing_weapons
          (val_add, ":damage", ":value"),
          
          (item_get_speed_rating, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":damage", ":value"),
          
          (item_get_weapon_length, ":value", ":item_id"),
          (convert_to_fixed_point, ":value"),
          (store_sqrt, reg2, ":value"),
          (convert_from_fixed_point, reg2),
          (val_mul, ":damage", reg2),
          (assign, ":ret_val", ":damage"),
          
          #Shields
        (else_try),
          (eq, ":item_type", itp_type_shield),
          
          #construct comparison value
          (item_get_body_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          
          (item_get_hit_points, ":value", ":item_id"),
          (val_add, ":value", ":hit_points"),
          (val_div, ":value", 17),  #attempt to make it comparable to armors
          (val_add, ":armor", ":value"),
          
          #shields' protection modified by size, speed
          (item_get_weapon_length, ":value", ":item_id"),
          (val_mul, ":armor", ":value"),
          (val_div, ":armor", Outfit_Thorax_Length),
          
          (item_get_speed_rating, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":armor", ":value"),
          (val_div, ":armor", Outfit_Fast_Weapon_Speed),
          
          (val_mul, ":armor", 3), #fudge factor
          (assign, ":ret_val", ":armor"),
          
          #Horses
        (else_try),
          (eq, ":item_type", itp_type_horse),
          
          #construct comparison value
          (item_get_body_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (val_mul, ":armor", 4), #figure it takes 3-4 hits to kill a horse, so this is the hit value of each
          #point of armor
          
          (item_get_hit_points, ":value", ":item_id"),
          (val_add, ":value", ":hit_points"),
          (val_add, ":armor", ":value"),
          
          (item_get_horse_speed, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":armor", ":value"),
          (assign, ":ret_val", ":armor"),
          
          #Missiles
        (else_try),
          (this_or_next | eq, ":item_type", itp_type_arrows),
          (this_or_next | eq, ":item_type", itp_type_bolts),
          (eq, ":item_type", itp_type_bullets),
        (try_end),
      (try_end),
      
      (assign, reg0, ":ret_val"),]),
      
 # ("init_noswing_weapons", make_noswing_weapons(items)),
  
# # M&B Standard AI with changes for formations #CABA - OK; Need expansion when new AI divisions to work with
  # script_formation_battle_tactic_init_aux
  # Input: team_no, battle_tactic
  # Output: none
  ("formation_battle_tactic_init_aux_moto",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
      #(team_get_leader, ":ai_leader", ":team_no"),
      (call_script, "script_team_get_nontroll_leader", ":team_no"),
      (assign, ":ai_leader", reg0),
      (try_begin),
        (eq, ":battle_tactic", btactic_hold),
        (agent_is_active, ":ai_leader"),
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
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        #(team_get_leader, ":ai_leader", ":team_no"),
        (call_script, "script_team_get_nontroll_leader", ":team_no"),
        (assign, ":ai_leader", reg0),
        (ge, ":ai_leader", 0),
        (agent_set_speed_limit, ":ai_leader", 8),
        (agent_get_position, pos60, ":ai_leader"),
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos60),
      (try_end),
# formations additions
	  (call_script, "script_division_reset_places_moto"),
	  (call_script, "script_get_default_formation_moto", ":team_no"),
	  (assign, ":fformation", reg0),
	  
	  (try_begin),
		(call_script, "script_cf_battlegroup_valid_formation_moto", ":team_no", grc_infantry, ":fformation"),
		(store_add, ":slot", slot_team_d0_formation, grc_infantry),
		(team_set_slot, ":team_no", ":slot", ":fformation"),
		(store_add, ":slot", slot_team_d0_formation_space, grc_infantry),
		(team_set_slot, ":team_no", ":slot", 0),
	  (else_try),
		(call_script, "script_formation_end_moto", ":team_no", grc_infantry),
	  (try_end),
	  (call_script, "script_battlegroup_place_around_leader_moto", ":team_no", grc_infantry),
	  
	  (try_begin),
		(call_script, "script_cf_battlegroup_valid_formation_moto", ":team_no", grc_archers, formation_default),
		(store_add, ":slot", slot_team_d0_formation, grc_archers),
		(team_set_slot, ":team_no", ":slot", formation_default),
		(store_add, ":slot", slot_team_d0_formation_space, grc_archers),
		(team_set_slot, ":team_no", ":slot", 2),
	  (else_try),
		(call_script, "script_formation_end_moto", ":team_no", grc_archers),
	  (try_end),
	  (call_script, "script_battlegroup_place_around_leader_moto", ":team_no", grc_archers),
	  
	  (try_begin),
		(call_script, "script_cf_battlegroup_valid_formation_moto", ":team_no", grc_cavalry, formation_wedge),
		(store_add, ":slot", slot_team_d0_formation, grc_cavalry),
		(team_set_slot, ":team_no", ":slot", formation_wedge),
		(store_add, ":slot", slot_team_d0_formation_space, grc_cavalry),
		(team_set_slot, ":team_no", ":slot", 0),
	  (else_try),
		(call_script, "script_formation_end_moto", ":team_no", grc_cavalry),
	  (try_end),
	  (call_script, "script_battlegroup_place_around_leader_moto", ":team_no", grc_cavalry),
	  
	  (team_give_order, ":team_no", grc_archers, mordr_spread_out),
	  (team_give_order, ":team_no", grc_archers, mordr_spread_out),
# end formations additions
  ]),
  
  # script_formation_battle_tactic_apply_aux #CABA - OK; Need expansion when new AI divisions to work with
  # Input: team_no, battle_tactic
  # Output: battle_tactic
  ("formation_battle_tactic_apply_aux_moto",
    [
      (store_script_param, ":team_no", 1),
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
		  (call_script, "script_formation_end_moto", ":team_no", grc_infantry),	#formations
		  (call_script, "script_formation_end_moto", ":team_no", grc_archers),	#formations
		  (call_script, "script_formation_end_moto", ":team_no", grc_cavalry),	#formations
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        #(team_get_leader, ":ai_leader", ":team_no"),
        (call_script, "script_team_get_nontroll_leader", ":team_no"),
        (assign, ":ai_leader", reg0),
        (try_begin),
          (agent_is_active, ":ai_leader"),
          (agent_is_alive, ":ai_leader"),
          (agent_set_speed_limit, ":ai_leader", 9),
          (call_script, "script_team_get_average_position_of_enemies", ":team_no"),
          (copy_position, pos60, pos0),
          (ge, ":ai_leader", 0),
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
#formations code
		  (call_script, "script_point_y_toward_position_moto", pos63, pos60),
		  (agent_get_position, pos49, ":ai_leader"),
		  (agent_set_position, ":ai_leader", pos63),	#fake out script_battlegroup_place_around_leader
		  (call_script, "script_division_reset_places_moto"),
		  (call_script, "script_get_default_formation_moto", ":team_no"),
		  (assign, ":fformation", reg0),
		  
		  (try_begin),
			(call_script, "script_cf_battlegroup_valid_formation_moto", ":team_no", grc_infantry, ":fformation"),
			(store_add, ":slot", slot_team_d0_formation, grc_infantry),
			(team_set_slot, ":team_no", ":slot", ":fformation"),
			(store_add, ":slot", slot_team_d0_formation_space, grc_infantry),
			(team_set_slot, ":team_no", ":slot", 0),
		  (else_try),
			(call_script, "script_formation_end_moto", ":team_no", grc_infantry),
		  (try_end),
		  (call_script, "script_battlegroup_place_around_leader_moto", ":team_no", grc_infantry),
		  
		  (try_begin),
			(call_script, "script_cf_battlegroup_valid_formation_moto", ":team_no", grc_archers, formation_default),
			(store_add, ":slot", slot_team_d0_formation, grc_archers),
			(team_set_slot, ":team_no", ":slot", formation_default),
			(store_add, ":slot", slot_team_d0_formation_space, grc_archers),
			(team_set_slot, ":team_no", ":slot", 2),
		  (else_try),
			(call_script, "script_formation_end_moto", ":team_no", grc_archers),
		  (try_end),
		  (call_script, "script_battlegroup_place_around_leader_moto", ":team_no", grc_archers),
		  
		  (try_begin),
			(call_script, "script_cf_battlegroup_valid_formation_moto", ":team_no", grc_cavalry, formation_wedge),
			(store_add, ":slot", slot_team_d0_formation, grc_cavalry),
			(team_set_slot, ":team_no", ":slot", formation_wedge),
			(store_add, ":slot", slot_team_d0_formation_space, grc_cavalry),
			(team_set_slot, ":team_no", ":slot", 0),
		  (else_try),
			(call_script, "script_formation_end_moto", ":team_no", grc_cavalry),
		  (try_end),
		  (call_script, "script_battlegroup_place_around_leader_moto", ":team_no", grc_cavalry),
	  
		  (agent_set_position, ":ai_leader", pos49),
#end formations code
          (agent_get_position, pos1, ":ai_leader"),
          (try_begin),
            (lt, ":distance_to_enemy", 50),
            (ge, ":mission_time", 30),
            (assign, ":battle_tactic", 0),
			(call_script, "script_formation_end_moto", ":team_no", grc_infantry),	#formations
			(call_script, "script_formation_end_moto", ":team_no", grc_archers),	#formations
			(call_script, "script_formation_end_moto", ":team_no", grc_cavalry),	#formations
            (team_give_order, ":team_no", grc_everyone, mordr_charge),
            (agent_set_speed_limit, ":ai_leader", 60),
          (try_end),
        (else_try),
          (assign, ":battle_tactic", 0),
		  (call_script, "script_formation_end_moto", ":team_no", grc_infantry),	#formations
		  (call_script, "script_formation_end_moto", ":team_no", grc_archers),	#formations
		  (call_script, "script_formation_end_moto", ":team_no", grc_cavalry),	#formations
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (try_end),
      
      (try_begin), # charge everyone after a while
        (neq, ":battle_tactic", 0),
        (ge, ":mission_time", 300),
        (assign, ":battle_tactic", 0),
		(call_script, "script_formation_end_moto", ":team_no", grc_infantry),	#formations
		(call_script, "script_formation_end_moto", ":team_no", grc_archers),	#formations
		(call_script, "script_formation_end_moto", ":team_no", grc_cavalry),	#formations
        (team_give_order, ":team_no", grc_everyone, mordr_charge),
        #(team_get_leader, ":ai_leader", ":team_no"),
        (call_script, "script_team_get_nontroll_leader", ":team_no"),
        (assign, ":ai_leader", reg0),
        (agent_is_active, ":ai_leader"),
        (agent_set_speed_limit, ":ai_leader", 60),
      (try_end),
      (assign, reg0, ":battle_tactic"),
  ]),

###########FORM V5 END ###############
] or []) + [

]
