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
	

  # script_team_field_ranged_tactics by motomataru
  # Input: AI team, size relative to largest team in %, size relative to battle in %
  # Output: none
  ("team_field_ranged_tactics", [
	(store_script_param, ":team_no", 1),
	(store_script_param, ":rel_army_size", 2),
	(store_script_param, ":battle_presence", 3),
	(call_script, "script_battlegroup_get_size", ":team_no", grc_archers),
	(try_begin),
		(gt, reg0, 0),
		(call_script, "script_battlegroup_get_position", Archers_Pos, ":team_no", grc_archers),
		(call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":team_no", grc_everyone),
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
					(assign, ":move_archers", 1),
				(try_end),
			(else_try),
				(ge, ":decision_index", Hold_Point),	#not starting in a defensive position (see below)
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
						(assign, ":shot_distance", AI_firing_distance),
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
			(assign, ":place_leader_by_infantry", 0), #JL, added on 2/20/2011 PoP3.3
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

# #Formations Scripts	  
  # script_cf_formation v2 by motomataru
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
		(call_script, "script_team_get_position_of_enemies", pos60, ":fteam", grc_everyone),
		(neq, reg0, 0),	#more than 0 enemies still alive?
		(call_script, "script_point_y_toward_position", pos1, pos60),
	(try_end),
	(call_script, "script_battlegroup_get_size", ":fteam", ":fclass"),
	(assign, ":num_troops", reg0),
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
		(call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
		(val_mul, reg0, -1),
		(position_move_x, pos61, reg0, 0),
	(else_try),
		(position_move_y, pos1, 1000),		#archers set up 10m FRONT of leader
		(copy_position, pos61, pos1),
		(call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
		(val_mul, reg0, -1),
		(position_move_x, pos1, reg0, 0),
		(call_script, "script_form_archers", ":fteam", ":fleader", ":formation_extra_spacing", "$archer_formation_type"),
	(try_end),
	(try_begin),
		(eq, ":fclass", grc_cavalry),
		(try_begin),
			(ge, ":num_troops", formation_min_cavalry_troops),
			(assign, ":formed_up", 1),
		(else_try),
			(assign, ":formed_up", 0),
		(try_end),
	(else_try),
		(this_or_next|eq, ":fclass", grc_infantry),
		(eq, ":fclass", grc_archers),
		(try_begin),
			(ge, ":num_troops", formation_min_foot_troops),
			(assign, ":formed_up", 1),
		(else_try),
			(assign, ":formed_up", 0),
		(try_end),
	(else_try),	#unsupported division
		(assign, ":formed_up", 0),
	(try_end),
#	(team_set_order_position, ":fteam", ":fclass", pos61),
	(call_script, "script_set_formation_position", ":fteam", ":fclass", pos61),
	(assign, reg0, ":num_troops"),
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
	   
  # script_form_infantry v2 by motomataru
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
	(call_script, "script_battlegroup_get_size", ":fteam", grc_infantry),
	(assign, ":num_troops", reg0),	
	(assign, ":troop_count", reg0),
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
		(try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
			(try_for_agents, ":agent"),
				(agent_get_troop_id, ":troop_id", ":agent"),
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
		(try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
			(try_for_agents, ":agent"),
				(agent_get_troop_id, ":troop_id", ":agent"),
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
		(assign, reg0, formation_ranks),
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


  # script_formation_current_position by motomataru
  # Input: destination position, team, troop class, formation type, extra spacing
  # Output: in destination position
  ("formation_current_position", [
	(store_script_param, ":fposition", 1),
	(store_script_param, ":fteam", 2),
	(store_script_param, ":fclass", 3),
	(store_script_param, ":fformation", 4),
	(store_script_param, ":formation_extra_spacing", 5),
	(call_script, "script_get_first_formation_member", ":fteam", ":fclass", ":fformation"),
	(assign, ":first_agent_in_formation", reg0),
	(call_script, "script_get_formation_position", pos0, ":fteam", ":fclass"),
	(try_begin),
		(eq, ":first_agent_in_formation", -1),
		(copy_position, ":fposition", pos0),
	(else_try),
		(agent_get_position, ":fposition", ":first_agent_in_formation"),
		(position_copy_rotation, ":fposition", pos0),
		(call_script, "script_battlegroup_get_size", ":fteam", ":fclass"),
		(assign, ":num_troops", reg0),
		(try_begin),
			(eq, ":fclass", grc_archers),
			(call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
		(else_try),
			(call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
			(val_mul, reg0, -1),
		(try_end),
		(position_move_x, ":fposition", reg0, 0),
	(try_end),
  ]),
  
  
  # script_get_centering_amount by motomataru
  # Input: formation type, number of infantry, extra spacing
  #        Use formation type formation_default to use script for archer line
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
		(store_sqrt, reg0, ":num_troops"),
		(val_mul, reg0, ":troop_space"),
		(convert_from_fixed_point, reg0),
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


  # script_formation_move_position v2 by motomataru
  # Input: team, troop class, formation current position, formation type, extra spacing, (1 to advance or -1 to withdraw or 0 to redirect)
  # Output: pos1 (offset for centering)
  ("formation_move_position", [
	(store_script_param, ":fteam", 1),
	(store_script_param, ":fclass", 2),
	(store_script_param, ":fcurrentpos", 3),
	(store_script_param, ":fformation", 4),
	(store_script_param, ":formation_extra_spacing", 5),
	(store_script_param, ":direction", 6),
	(copy_position, pos1, ":fcurrentpos"),
	(call_script, "script_team_get_position_of_enemies", pos60, ":fteam", grc_everyone),
	(try_begin),
		(neq, reg0, 0),	#more than 0 enemies still alive?
		(copy_position, pos1, ":fcurrentpos"),	#restore current formation "position"
		(call_script, "script_point_y_toward_position", pos1, pos60),	#record angle from center to enemy
		(assign, ":distance_to_enemy", reg0),
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
		(call_script, "script_battlegroup_get_size", ":fteam", ":fclass"),
		(assign, ":num_troops", reg0),
		(try_begin),
			(neq, ":fclass", grc_archers),
			(call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
		(else_try),
			(call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
			(val_mul, reg0, -1),
		(try_end),
		(position_move_x, pos1, reg0, 0),
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
  
  
  # script_player_order_formations by motomataru
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
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_infantry, "$infantry_formation_type", "$infantry_space"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$infantry_formation_move_order", mordr_advance),
				# (team_set_order_position, "$fplayer_team_no", grc_infantry, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_infantry, pos63, "$infantry_formation_type", "$infantry_space", 1),			
			(call_script, "script_form_infantry", "$fplayer_team_no", "$fplayer_agent_no", "$infantry_space", "$infantry_formation_type"),
			(assign, "$infantry_formation_move_order", mordr_advance),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_cavalry, "$cavalry_formation_type", "$cavalry_space"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$cavalry_formation_move_order", mordr_advance),
				# (team_set_order_position, "$fplayer_team_no", grc_cavalry, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_cavalry, pos63, "$cavalry_formation_type", "$cavalry_space", 1),
			(call_script, "script_form_cavalry", "$fplayer_team_no", "$fplayer_agent_no", "$cavalry_space"),
			(assign, "$cavalry_formation_move_order", mordr_advance),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_archers),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_archers, "$archer_formation_type", "$archer_space"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$archer_formation_move_order", mordr_advance),
				# (team_set_order_position, "$fplayer_team_no", grc_archers, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_archers, pos63, "$archer_formation_type", "$archer_space", 1),
			(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
			(assign, "$archer_formation_move_order", mordr_advance),
		(try_end),

	(else_try),
		(eq, ":forder", mordr_fall_back),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_infantry, "$infantry_formation_type", "$infantry_space"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$infantry_formation_move_order", mordr_fall_back),
				# (team_set_order_position, "$fplayer_team_no", grc_infantry, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_infantry, pos63, "$infantry_formation_type", "$infantry_space", -1),
			(call_script, "script_form_infantry", "$fplayer_team_no", "$fplayer_agent_no", "$infantry_space", "$infantry_formation_type"),
			(assign, "$infantry_formation_move_order", mordr_fall_back),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_cavalry, "$cavalry_formation_type", "$cavalry_space"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$cavalry_formation_move_order", mordr_fall_back),
				# (team_set_order_position, "$fplayer_team_no", grc_cavalry, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_cavalry, pos63, "$cavalry_formation_type", "$cavalry_space", -1),
			(call_script, "script_form_cavalry", "$fplayer_team_no", "$fplayer_agent_no", "$cavalry_space"),
			(assign, "$cavalry_formation_move_order", mordr_fall_back),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_archers),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_archers, "$archer_formation_type", "$archer_space"),
			(try_begin),	#on change of orders cancel order position
				(neq, "$archer_formation_move_order", mordr_fall_back),
				# (team_set_order_position, "$fplayer_team_no", grc_archers, pos63),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos63),
			(try_end),
			(call_script, "script_formation_move_position", "$fplayer_team_no", grc_archers, pos63, "$archer_formation_type", "$archer_space", -1),
			(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
			(assign, "$archer_formation_move_order", mordr_fall_back),
		(try_end),

	(else_try),
		(eq, ":forder", mordr_stand_closer),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(gt, "$infantry_space", 0),
			(val_sub, "$infantry_space", 1),
#			(team_get_order_position, pos1, "$fplayer_team_no", grc_infantry),
			(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_infantry),			
			(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_infantry),
			(assign, ":troop_count", reg0),			
			(call_script, "script_get_centering_amount", "$infantry_formation_type", ":troop_count", "$infantry_space"),
			(position_move_x, pos1, reg0),
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
			(val_sub, "$archer_space", 1),
#			(team_get_order_position, pos1, "$fplayer_team_no", grc_archers),
			(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_archers),
			(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_archers),
			(assign, ":troop_count", reg0),
			(call_script, "script_get_centering_amount", formation_default, ":troop_count", "$archer_space"),
			(val_mul, reg0, -1),
			(position_move_x, pos1, reg0),
			(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
		(try_end),

	(else_try),
		(eq, ":forder", mordr_spread_out),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(val_add, "$infantry_space", 1),
#			(team_get_order_position, pos1, "$fplayer_team_no", grc_infantry),
			(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_infantry),			
			(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_infantry),
			(assign, ":troop_count", reg0),			
			(call_script, "script_get_centering_amount", "$infantry_formation_type", ":troop_count", "$infantry_space"),
			(position_move_x, pos1, reg0),
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
			(val_add, "$archer_space", 1),
#			(team_get_order_position, pos1, "$fplayer_team_no", grc_archers),
			(call_script, "script_get_formation_position", pos1, "$fplayer_team_no", grc_archers),
			(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_archers),
			(assign, ":troop_count", reg0),
			(call_script, "script_get_centering_amount", formation_default, ":troop_count", "$archer_space"),
			(val_mul, reg0, -1),
			(position_move_x, pos1, reg0),
			(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
		(try_end),

	(else_try),
		(eq, ":forder", mordr_stand_ground),
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_infantry, "$infantry_formation_type", "$infantry_space"),
			(copy_position, pos1, pos63),
			(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_infantry),
			(assign, ":troop_count", reg0),			
			(call_script, "script_get_centering_amount", "$infantry_formation_type", ":troop_count", "$infantry_space"),
			(position_move_x, pos1, reg0),
			(call_script, "script_form_infantry", "$fplayer_team_no", "$fplayer_agent_no", "$infantry_space", "$infantry_formation_type"),
			(assign, "$infantry_formation_move_order", mordr_stand_ground),
			(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos63),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_cavalry, "$cavalry_formation_type", "$cavalry_space"),
			(copy_position, pos1, pos63),
			(call_script, "script_form_cavalry", "$fplayer_team_no", "$fplayer_agent_no", "$cavalry_space"),
			(assign, "$cavalry_formation_move_order", mordr_stand_ground),
			(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos63),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_archers),
			(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", grc_archers, "$archer_formation_type", "$archer_space"),
			(copy_position, pos1, pos63),
			(call_script, "script_battlegroup_get_size", "$fplayer_team_no", grc_archers),
			(assign, ":troop_count", reg0),
			(call_script, "script_get_centering_amount", formation_default, ":troop_count", "$archer_space"),
			(val_mul, reg0, -1),
			(position_move_x, pos1, reg0),
			(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
			(assign, "$archer_formation_move_order", mordr_stand_ground),
			(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos63),
		(try_end),			
	(try_end)
  ]),

  
# #Utilities used by formations
  # script_point_y_toward_position by motomataru
  # Input: from position, to position
  # Output: reg0 fixed point distance
  ("point_y_toward_position", [
	(store_script_param, ":from_position", 1),
	(store_script_param, ":to_position", 2),
	(position_get_x, ":dist_x_to_cosine", ":to_position"),
	(position_get_x, ":from_coord", ":from_position"),
	(val_sub, ":dist_x_to_cosine", ":from_coord"),
	(store_mul, ":sum_square", ":dist_x_to_cosine", ":dist_x_to_cosine"),
	(position_get_y, ":dist_y_to_sine", ":to_position"),
	(position_get_y, ":from_coord", ":from_position"),
	(val_sub, ":dist_y_to_sine", ":from_coord"),
	(store_mul, reg0, ":dist_y_to_sine", ":dist_y_to_sine"),
	(val_add, ":sum_square", reg0),
	(convert_from_fixed_point, ":sum_square"),
	(store_sqrt, ":distance_between", ":sum_square"),
	(convert_to_fixed_point, ":dist_x_to_cosine"),
	(val_div, ":dist_x_to_cosine", ":distance_between"),
	(convert_to_fixed_point, ":dist_y_to_sine"),
	(val_div, ":dist_y_to_sine", ":distance_between"),
	(try_begin),
		(lt, ":dist_x_to_cosine", 0),
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
			(gt, ":sine_theta", ":dist_y_to_sine"),
			(assign, ":bound_a", ":theta"),
		(else_try),
			(lt, ":sine_theta", ":dist_y_to_sine"),
			(assign, ":bound_b", ":theta"),
		(try_end),
		(store_add, ":angle_sum", ":bound_b", ":bound_a"),
		(store_div, ":theta", ":angle_sum", 2),
	(try_end),
	(convert_from_fixed_point, ":theta"),
	(position_get_rotation_around_z, reg0, ":from_position"),
	(val_sub, ":theta", reg0),
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
		(agent_get_team, ":bgteam", ":cur_agent"),
		(agent_get_class, ":bgroup", ":cur_agent"),
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
					(neq, ":cur_weapon_type", itp_type_thrown), #added by JL to exclude throwing weapons from being horse archers					(val_add, "$team0_percent_cavalry_are_archers", 1),
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

 
  # script_team_get_position_of_enemies by motomataru
  # Input: destination position, team, troop class/division
  # Output: destination position: average position if reg0 > 0
  #			reg0: number of enemies
  # Run script_store_battlegroup_data before calling!
  ("team_get_position_of_enemies", [
	(store_script_param, ":enemy_position", 1),
	(store_script_param, ":team_no", 2),
	(store_script_param, ":troop_type", 3),
	(assign, ":pos_x", 0),
	(assign, ":pos_y", 0),
	(assign, ":total_size", 0),
	
	(try_for_range, ":other_team", 0, 4),
		(teams_are_enemies, ":other_team", ":team_no"),
		(try_begin),
			(eq, ":troop_type", grc_everyone),
			(call_script, "script_battlegroup_get_size", ":other_team", grc_everyone),
			(assign, ":team_size", reg0),
			(try_begin),
				(gt, ":team_size", 0),
				(call_script, "script_battlegroup_get_position", ":enemy_position", ":other_team", grc_everyone),
				(position_get_x, reg0, ":enemy_position"),
				(val_mul, reg0, ":team_size"),
				(val_add, ":pos_x", reg0),
				(position_get_y, reg0, ":enemy_position"),
				(val_mul, reg0, ":team_size"),
				(val_add, ":pos_y", reg0),
			(try_end),
		(else_try),
			(assign, ":team_size", 0),
			(try_begin),
				(eq, ":other_team", "$fplayer_team_no"),
				(assign, ":num_groups", 9),
			(else_try),
				(assign, ":num_groups", 3),
			(try_end),
			(try_for_range, ":enemy_battle_group", 0, ":num_groups"),
				(eq, ":enemy_battle_group", ":troop_type"),
				(call_script, "script_battlegroup_get_size", ":other_team", ":troop_type"),
				(gt, reg0, 0),
				(val_add, ":team_size", reg0),
				(call_script, "script_battlegroup_get_position", ":enemy_position", ":other_team", ":troop_type"),
				(position_get_x, reg0, ":enemy_position"),
				(val_mul, reg0, ":team_size"),
				(val_add, ":pos_x", reg0),
				(position_get_y, reg0, ":enemy_position"),
				(val_mul, reg0, ":team_size"),
				(val_add, ":pos_y", reg0),
			(try_end),
		(try_end),
		(val_add, ":total_size", ":team_size"),
	(try_end),
	
	(try_begin),
		(eq, ":total_size", 0),
		(init_position, ":enemy_position"),
	(else_try),
		(val_div, ":pos_x", ":total_size"),
		(position_set_x, ":enemy_position", ":pos_x"),
		(val_div, ":pos_y", ":total_size"),
		(position_set_y, ":enemy_position", ":pos_y"),
		(position_set_z_to_ground_level, ":enemy_position"),
	(try_end),

	(assign, reg0, ":total_size"),
  ]),


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
          (this_or_next|lt, ":min_dist", 1000),
          (lt, ":avg_dist", 4000),
          (assign, ":battle_tactic", 0),
		  (call_script, "script_formation_end", ":team_no", grc_everyone),	#formations
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        #(team_get_leader, ":ai_leader", ":team_no"),
        (call_script, "script_team_get_nontroll_leader", ":team_no"),
        (assign, ":ai_leader", reg0),
        (try_begin),
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
		  (call_script, "script_point_y_toward_position", pos63, pos60),
		  (agent_get_position, pos49, ":ai_leader"),
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
		  (agent_set_position, ":ai_leader", pos49),
#end formations code
          (agent_get_position, pos1, ":ai_leader"),
          (try_begin),
            (lt, ":distance_to_enemy", 50),
            (ge, ":mission_time", 30),
            (assign, ":battle_tactic", 0),
			(call_script, "script_formation_end", ":team_no", grc_everyone),	#formations code
            (team_give_order, ":team_no", grc_everyone, mordr_charge),
            (agent_set_speed_limit, ":ai_leader", 60),
          (try_end),
        (else_try),
          (assign, ":battle_tactic", 0),
		  (call_script, "script_formation_end", ":team_no", grc_everyone),	#formations code
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (try_end),
      
      (try_begin), # charge everyone after a while
        (neq, ":battle_tactic", 0),
        (ge, ":mission_time", 300),
        (assign, ":battle_tactic", 0),
		(call_script, "script_formation_end", ":team_no", grc_everyone),	#formations code
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
		(eq, "$tld_option_formations", 1),
		(call_script, "script_formation_battle_tactic_init_aux", ":team_no", ":battle_tactic"),
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
		(eq, "$tld_option_formations", 1),
		(call_script, "script_formation_battle_tactic_apply_aux", ":team_no", ":battle_tactic"),
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


]
