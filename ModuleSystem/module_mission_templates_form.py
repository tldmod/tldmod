from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *

from module_info import wb_compile_switch as is_a_wb_mt


# cpp-- Prevents an issue of compiling where it doesnt know what this is if its M&B 1.011
if is_a_wb_mt==0: 
 ti_on_order_issued = 0 

# WARBAND FORMATIONS FIX #

# cpp-- Only blocks keys if it is M&B
block_mb_gamekeys = (not is_a_wb_mt==1 and 
[
		(neg|game_key_is_down, gk_order_charge), 		
		(neg|game_key_is_down, gk_order_dismount),
		(neg|game_key_is_down, gk_order_halt),
		(neg|game_key_is_down, gk_order_follow),
		(neg|game_key_is_down, gk_order_advance),
		(neg|game_key_is_down, gk_order_fall_back),
		(neg|game_key_is_down, gk_order_spread_out),
		(neg|game_key_is_down, gk_order_stand_closer)
] or [])

# VANILLA FORMATIONS FIX #
mb_only_formations = [

	# charge ends formation
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_charge)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_order_formations", mordr_charge)
	]),

	# dismount ends formation
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_dismount)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_order_formations", mordr_dismount),
	]),

	# On hold, any formations reform in new location		
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_halt)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_order_formations", mordr_hold)
	]),

	# Follow is hold repeated frequently
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_follow)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_order_formations", mordr_follow)
	]),

	(0,0,0,[(eq,"$tld_option_formations",1),(game_key_clicked,gk_order_advance     )],[(call_script,"script_player_order_formations",mordr_advance)]),
	(0,0,0,[(eq,"$tld_option_formations",1),(game_key_clicked,gk_order_fall_back   )],[(call_script,"script_player_order_formations",mordr_fall_back)]),
	(0,0,0,[(eq,"$tld_option_formations",1),(game_key_clicked,gk_order_spread_out  )],[(call_script,"script_player_order_formations",mordr_spread_out)]),
	(0,0,0,[(eq,"$tld_option_formations",1),(game_key_clicked,gk_order_stand_closer)],[(call_script,"script_player_order_formations",mordr_stand_closer)]),
]



mb_formations = (not is_a_wb_mt==1 and mb_only_formations or [])
# VANILLA FORMATIONS FIX #

wb_formation_order = (ti_on_order_issued, 0, 0, [(eq,"$tld_option_formations",1)], 
	[
		(store_trigger_param_1, ":order_id"), 
		(store_trigger_param_2, ":agent_id"),
		(try_begin),
			(call_script, "script_change_formation", ":order_id", ":agent_id"),
		(try_end),
	]) 

# cpp-- WB command cursor tracking
wb_command_cursor_init = (0, 0, ti_once, [(eq,"$tld_option_formations",1)], [(assign, "$hold_f1", tld_cursor_undefined)])
wb_command_cursor_f1_down = (0, 0, 0, [(eq,"$tld_option_formations",1),(key_is_down, key_f1),(eq, "$hold_f1", tld_cursor_undefined)], [(assign, "$hold_f1", 0)])
wb_command_cursor_f1_timer = (0, 0, 0, [(eq,"$tld_option_formations",1),(ge, "$hold_f1", 0)], [(val_add, "$hold_f1", 1)])
wb_command_cursor_arrow_mode = (0, 0, 0, [(eq,"$tld_option_formations",1),(ge, "$hold_f1", tld_cursor_time)], [(assign, "$hold_f1", tld_cursor_arrow_mode)])


wb_command_cursor_f1_up = (0, 0, 0, [(eq,"$tld_option_formations",1),(key_is_down|neg, key_f1),(neq, "$hold_f1", tld_cursor_undefined)], 
[
	(try_begin),
		(eq, "$hold_f1", tld_cursor_arrow_mode),
      		(get_player_agent_no, ":player"),
      		(agent_get_team, ":player_team", ":player"),
      		(agent_get_look_position, pos1, ":player"),
      		(position_move_z, pos1, 120),
      		(try_begin),
        		(try_begin),
        			(class_is_listening_order, ":player_team", grc_infantry),
					(team_get_order_position, pos1, ":player_team", grc_infantry),
					(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos1),
					#(display_message, "@DEBUG: Infantry Holding at Flag Location"),
				(try_end),
      			(try_begin),
        			(class_is_listening_order, ":player_team", grc_archers),
					(team_get_order_position, pos1, ":player_team", grc_archers),
					(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos1),
					#(display_message, "@DEBUG: Archers Holding at Flag Location"),
				(try_end),
      			(try_begin),
        			(class_is_listening_order, ":player_team", grc_cavalry),
					(team_get_order_position, pos1, ":player_team", grc_cavalry),
					(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos1),
					#(display_message, "@DEBUG: Cavalry Holding at Flag Location"),
				(try_end),
			(try_end),
	(try_end),
	(assign, "$hold_f1", tld_cursor_undefined),
])

#AI triggers v3 by motomataru
# cpp: Quick Find [AITAKTIKS]
AI_triggers = [  
	(ti_before_mission_start, 0, 0, [(eq, "$tld_option_formations", 1), (eq, "$small_scene_used", 0)], [
		(assign, "$cur_casualties", 0),
		(assign, "$prev_casualties", 0),
		(assign, "$prev_casualties2", 0), #adeed by JL to use for checking every second
		(assign, "$ranged_clock", 1),
		(assign, "$battle_phase", BP_Setup),
		(assign, "$clock_reset", 0),
		(assign, "$charge_activated", 0), # added for cav charge control -JL
		(assign, "$charge_ongoing",0), # added for cav charge control -JL
		(assign, "$inf_charge_activated", 0), # added for inf charge control -JL
		(assign, "$inf_charge_ongoing", 0), # added for inf charge control -JL
		(assign, "$arc_charge_activated", 0), # added for archer charge control -JL
		(assign, "$att_reinforcements_arrived",0), #added for seeing if reinforcements have arrived -JL
		(assign, "$def_reinforcements_arrived",0), #added for seeing if reinforcements have arrived -JL
		(assign, "$att_reinforcements_needed", 0), #added for seeing if reinforcements are needed -JL
		(assign, "$def_reinforcements_needed", 0), #added for seeing if reinforcements are needed -JL
		(assign, "$formai_disengage", 0), #added for controlling cavalry disengagement -JL
		(assign, "$formai_patrol_mode", 0), #added for controlling patrol mode -JL
	##JL code for assigning random local variables:
		(store_random_in_range, "$formai_rand0", -1000, AI_Self_Defence_Distance), #JL close retreat/advance/position range randomness
		(store_random_in_range, "$formai_rand2", 800, 1501), # JL positive only close range randomness
		(store_random_in_range, "$formai_rand1", 0, 501), #JL close hold position to archers for cavalry
		(store_random_in_range, "$formai_rand3", AI_charge_distance, 3001), # JL main charge distance randomness
		(store_random_in_range, "$formai_rand4", AI_Self_Defence_Distance, 2201), #JL alternative charge range randomness
		(store_random_in_range, "$formai_rand5", -1000, 0), #JL retreat range randomness
		(store_random_in_range, "$formai_rand6", 4000, 5001), #JL grand charge distance and firing distance range randomness
		(store_random_in_range, "$formai_rand7", 55, 66), #JL random decision comparative number (that partly decides when AI strives to execute a grand charge). A value of 30 = Patrol Mode. A value of 35 = enemy has >40% archers/others
		(store_random_in_range, "$formai_rand8", -100, 101), #JL random very short range positioning for inf around archers in x pos.			
		(assign, "$team0_default_formation", formation_default),
		(assign, "$team1_default_formation", formation_default),
		(assign, "$team2_default_formation", formation_default),
		(assign, "$team3_default_formation", formation_default),
		(init_position, Team0_Cavalry_Destination),
		(init_position, Team1_Cavalry_Destination),
		(init_position, Team2_Cavalry_Destination),
		(init_position, Team3_Cavalry_Destination),
		(assign, "$team0_reinforcement_stage", 0),
		(assign, "$team1_reinforcement_stage", 0),
		(init_position, pos17), #added by JL
		(init_position, pos18), #added by JL
	]),

	(0, AI_Delay_For_Spawn, ti_once, [(eq, "$tld_option_formations", 1), (eq, "$small_scene_used", 0)], [
		(set_fixed_point_multiplier, 100),
		(call_script, "script_store_battlegroup_data"),
		(call_script, "script_battlegroup_get_position", Team0_Starting_Point, 0, grc_everyone),
		(call_script, "script_battlegroup_get_position", Team1_Starting_Point, 1, grc_everyone),
		(call_script, "script_battlegroup_get_position", Team2_Starting_Point, 2, grc_everyone),
		(call_script, "script_battlegroup_get_position", Team3_Starting_Point, 3, grc_everyone),
		(call_script, "script_field_tactics", 1)
	]),
    
	#JL new trigger for assigning randoms:
	(60, 0, 0, [(eq, "$tld_option_formations", 1), (eq, "$small_scene_used", 0)], [
	##JL code for assigning random local variables:
		(store_random_in_range, "$formai_rand0", -1000, AI_Self_Defence_Distance), #JL close retreat/advance/position range randomness
		(store_random_in_range, "$formai_rand2", 800, 1501), # JL positive only close range randomness
		(store_random_in_range, "$formai_rand1", -1000, AI_Self_Defence_Distance), #JL close retreat/advance/position range 2
		(store_random_in_range, "$formai_rand3", AI_charge_distance, 3001), # JL main charge distance randomness
		(store_random_in_range, "$formai_rand4", AI_Self_Defence_Distance, 3001), #JL alternative charge range randomness
		(store_random_in_range, "$formai_rand5", -1000, 0), #JL retreat range randomness
		(store_random_in_range, "$formai_rand6", 4000, 5001), #JL grand charge distance and firing distance range randomness
		(store_random_in_range, "$formai_rand7", 55, 66), #JL random decision comparative number (that partly decides when AI strives to execute a grand charge).
		(store_random_in_range, "$formai_rand8", -100, 101), #JL random very short range positioning for inf around archers in x pos.	
		#(display_message, "@Randoms  have been updated"),
	]), #End JL

	(1, .5, 0, [(eq, "$tld_option_formations", 1), (eq, "$small_scene_used", 0)], [	#delay to offset half a second from formations trigger
		(try_begin),
			(assign, "$prev_casualties2", "$cur_casualties"), #added by JL
			(call_script, "script_cf_count_casualties"),
			(assign, "$cur_casualties", reg0),
			(assign, "$battle_phase", BP_Fight),
		(try_end),
		
		(set_fixed_point_multiplier, 100),
		(call_script, "script_store_battlegroup_data"),
		(try_begin),	#reassess ranged position when fighting starts
			(eq, "$battle_phase", BP_Fight), #changed from ge to eq -JL
			(eq, "$clock_reset", 0),
			(call_script, "script_field_tactics", 1),
			(assign, "$ranged_clock", 0),
			(assign, "$clock_reset", 1),
		(else_try),	#reassess ranged position every five seconds after setup
			(ge, "$battle_phase", BP_Jockey),
			(store_mod, reg0, "$ranged_clock", 5),		
			(eq, reg0, 0),
			(call_script, "script_field_tactics", 1),
			(assign, "$team0_reinforcement_stage", "$defender_reinforcement_stage"),
			(assign, "$team1_reinforcement_stage", "$attacker_reinforcement_stage"),
		(else_try),
			(call_script, "script_field_tactics", 0),
		(try_end),

		(try_begin),
			(eq, "$battle_phase", BP_Setup),
			(assign, ":not_in_setup_position", 0),
			(try_for_range, ":bgteam", 0, 4),
				(neq, ":bgteam", "$fplayer_team_no"),
				(call_script, "script_battlegroup_get_size", ":bgteam", grc_everyone),
				(gt, reg0, 0),
				(call_script, "script_battlegroup_get_position", pos1, ":bgteam", grc_archers),
				(team_get_order_position, pos0, ":bgteam", grc_archers),
				(get_distance_between_positions, reg0, pos0, pos1),
				(gt, reg0, 500),
				(assign, ":not_in_setup_position", 1),
			(try_end),
			(eq, ":not_in_setup_position", 0),	#all AI reached setup position?
			(assign, "$battle_phase", BP_Jockey),
		(try_end),
		
		(val_add, "$ranged_clock", 1),
	]),

 (2, 0, ti_once, [(eq, "$tld_option_formations", 1),(store_mission_timer_a, reg0),(gt, reg0, 2)], [ #Force Cav to Stay Mounted - Kham
    (set_show_messages, 0),   
    (try_for_range, ":team", 0, 4),		
		#(try_for_range, ":division", 0, 9),
			(team_get_riding_order, reg0, ":team", grc_cavalry),
			(eq, reg0, rordr_free),
			(team_give_order, ":team", grc_cavalry, mordr_mount),
		#(try_end),		
	(try_end),
	(set_show_messages, 1),
   ]),
]

# Formations triggers v3 by motomataru, Warband port
# Global variables	*_formation_type holds type of formation: see "Formation modes" in module_constants
#					*_formation_move_order hold the current move order for the formation
#					*_space hold the multiplier of extra space ordered into formation by the player

formations_triggers = [


	(ti_before_mission_start, 0, 0, [(eq, "$tld_option_formations", 1)], [
		(assign, "$autorotate_at_player", formation_autorotate_at_player),
		(assign, "$infantry_formation_type", formation_default),	#type set by first call; depends on faction
		(assign, "$archer_formation_type", formation_default),
		(assign, "$cavalry_formation_type", formation_wedge),
		(assign, "$infantry_space", formation_start_spread_out),	#give a little extra space for ease of forming up
		(assign, "$archer_space", formation_start_spread_out),
		(assign, "$cavalry_space", 0),
		(assign, "$fclock", 1)
	]),
    
#JL: Simple start player troops in formations, when formations is disabled	
	(0, 1, ti_once, [(eq, "$tld_option_formations", 0)], [
		#(display_message, "@Forming up to meet the enemy at your command ..."),
		(get_player_agent_no, "$fplayer_agent_no"),
		(agent_get_team, "$fplayer_team_no", "$fplayer_agent_no"),
		(agent_get_position, pos1, "$fplayer_agent_no"),
		(set_show_messages, 0),
		(team_give_order, "$fplayer_team_no", grc_everyone, mordr_hold),
		(position_move_x, pos1, 1500),		#cavalry set up 15m RIGHT of leader
		(position_move_y, pos1, 500),		#cavalry set up 5m IN FRONT of leader
		(team_set_order_position, "$fplayer_team_no", grc_cavalry, pos1),
		(agent_get_position, pos1, "$fplayer_agent_no"),
		(position_move_x, pos1, -1500),		#infantry set up 15m LEFT of leader
		(position_move_y, pos1, 500),
		(team_set_order_position, "$fplayer_team_no", grc_infantry, pos1),
		(agent_get_position, pos1, "$fplayer_agent_no"),
		(position_move_y, pos1, 2000),		#archers set up 20m FRONT of leader
		(team_set_order_position, "$fplayer_team_no", grc_archers, pos1),
		(set_show_messages, 1),
	]),	 #End of standard start formations

# Start troops in formation
	(0, formation_delay_for_spawn, ti_once, [(eq, "$tld_option_formations", 1)], [
		(get_player_agent_no, "$fplayer_agent_no"),
		(agent_get_team, "$fplayer_team_no", "$fplayer_agent_no"),
		
		#get team fixed data
		(assign, ":team0_avg_faction", 0),
		(assign, ":team1_avg_faction", 0),
		(assign, ":team2_avg_faction", 0),
		(assign, ":team3_avg_faction", 0),
		(assign, "$team0_size", 0),
		(assign, "$team1_size", 0),
		(assign, "$team2_size", 0),
		(assign, "$team3_size", 0),
		(try_for_agents, ":cur_agent"),
			(agent_is_human, ":cur_agent"),
			(agent_get_team, ":cur_team", ":cur_agent"),
			(agent_get_troop_id, ":cur_troop", ":cur_agent"),
			(store_troop_faction, ":cur_faction", ":cur_troop"),
			(try_begin),
				(eq, ":cur_team", 0),
				(val_add, ":team0_avg_faction", ":cur_faction"),
				(val_add, "$team0_size", 1),
			(else_try),
				(eq, ":cur_team", 1),
				(val_add, ":team1_avg_faction", ":cur_faction"),
				(val_add, "$team1_size", 1),
			(else_try),
				(eq, ":cur_team", 2),
				(val_add, ":team2_avg_faction", ":cur_faction"),
				(val_add, "$team2_size", 1),
			(else_try),
				(eq, ":cur_team", 3),
				(val_add, ":team3_avg_faction", ":cur_faction"),
				(val_add, "$team3_size", 1),
			(try_end),
		(try_end),
		(try_begin),
			(gt, "$team0_size", 0),
			(team_get_leader, ":fleader", 0),
			(try_begin),
				(ge, ":fleader", 0),
				(agent_get_troop_id, ":fleader_troop", ":fleader"),
				(store_troop_faction, "$team0_faction", ":fleader_troop"),
			(else_try),
				(store_mul, "$team0_faction", ":team0_avg_faction", 10),
				(val_div, "$team0_faction", "$team0_size"),
				(val_add, "$team0_faction", 5),
				(val_div, "$team0_faction", 10),
			(try_end),
		(try_end),
		(try_begin),
			(gt, "$team1_size", 0),
			(team_get_leader, ":fleader", 1),
			(try_begin),
				(ge, ":fleader", 0),
				(agent_get_troop_id, ":fleader_troop", ":fleader"),
				(store_troop_faction, "$team1_faction", ":fleader_troop"),
			(else_try),
				(store_mul, "$team1_faction", ":team1_avg_faction", 10),
				(val_div, "$team1_faction", "$team1_size"),
				(val_add, "$team1_faction", 5),
				(val_div, "$team1_faction", 10),
			(try_end),
		(try_end),
		(try_begin),
			(gt, "$team2_size", 0),
			(team_get_leader, ":fleader", 2),
			(try_begin),
				(ge, ":fleader", 0),
				(agent_get_troop_id, ":fleader_troop", ":fleader"),
				(store_troop_faction, "$team2_faction", ":fleader_troop"),
			(else_try),
				(store_mul, "$team2_faction", ":team2_avg_faction", 10),
				(val_div, "$team2_faction", "$team2_size"),
				(val_add, "$team2_faction", 5),
				(val_div, "$team2_faction", 10),
			(try_end),
		(try_end),
		(try_begin),
			(gt, "$team3_size", 0),
			(team_get_leader, ":fleader", 3),
			(try_begin),
				(ge, ":fleader", 0),
				(agent_get_troop_id, ":fleader_troop", ":fleader"),
				(store_troop_faction, "$team3_faction", ":fleader_troop"),
			(else_try),
				(store_mul, "$team3_faction", ":team3_avg_faction", 10),
				(val_div, "$team3_faction", "$team3_size"),
				(val_add, "$team3_faction", 5),
				(val_div, "$team3_faction", 10),
			(try_end),
		(try_end),
		
		(display_message, "@Forming ranks."),
		(call_script, "script_get_default_formation", "$fplayer_team_no"),
		(assign, "$infantry_formation_type", reg0),
		(call_script, "script_player_attempt_formation", grc_infantry, "$infantry_formation_type"),
		(call_script, "script_player_attempt_formation", grc_cavalry, formation_wedge),
		(call_script, "script_player_attempt_formation", grc_archers, formation_default),
		(set_show_messages, 0),
		(try_for_range, reg0, 3, 9),
			(team_give_order, "$fplayer_team_no", reg0, mordr_hold),
		(try_end),

		#init troops for when formation ends
		(try_for_range, reg0, 0, "$infantry_space"),
			(team_give_order, "$fplayer_team_no", grc_infantry, mordr_spread_out),
		(try_end),
		(try_for_range, reg0, 0, "$archer_space"),
			(team_give_order, "$fplayer_team_no", grc_archers, mordr_spread_out),
		(try_end),
		(try_for_range, reg0, 0, "$cavalry_space"),
			(team_give_order, "$fplayer_team_no", grc_cavalry, mordr_spread_out),
		(try_end),
		(set_show_messages, 1),
	]),

# cpp: These should be fine, as they dont override anything

#form ranks command
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(key_clicked, key_for_ranks)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_attempt_formation", grc_infantry, formation_ranks),
		(call_script, "script_player_attempt_formation", grc_archers, formation_ranks)
	]),

#form shield wall command
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(key_clicked, key_for_shield)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_attempt_formation", grc_infantry, formation_shield)
	]),

#form wedge command
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(key_clicked, key_for_wedge)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_attempt_formation", grc_infantry, formation_wedge),
		(call_script, "script_player_attempt_formation", grc_cavalry, formation_wedge)
	]),
#form square command
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(key_clicked, key_for_square)], [
		(assign, "$fclock", 1),
		(call_script, "script_player_attempt_formation", grc_infantry, formation_square)
	]),
#end formation command
	(0, 0, 1, [(eq, "$tld_option_formations", 1),(key_clicked, key_for_undo)], [(call_script, "script_player_order_formations", mordr_charge)]),


#Debug for Anims test

	#(0, 0, 1, [(key_clicked, key_t)], [(get_player_agent_no, ":player"), (agent_get_horse, ":horse", ":player"), (agent_set_animation, ":player", "anim_strike_fly_back_rise"), (agent_start_running_away, ":horse"),(agent_stop_running_away, ":horse"),]),
	#(0, 0, 1, [(key_clicked, key_y)], [(get_player_agent_no, ":player"), (agent_set_animation, ":player", "anim_strike_fall_back_rise_upper"),]),
	#(0, 0, 1, [(key_clicked, key_h)], [(get_player_agent_no, ":player"), (agent_get_horse, ":horse", ":player"), (agent_set_animation, ":player", "anim_strike_fly_back"),(agent_set_animation, ":horse", "anim_horse_fall_right"),]),
	
	] + ((is_a_wb_mt==1) and [

#Skirmish
	#(0, 0, 1, [(eq, "$tld_option_formations",1), (eq, "$cheat_mode",1), (key_clicked, key_for_skirmish)],[(assign, "$archer_aim_active", 1), (display_message, "@Archer Aim Activated!")]),
	#(0, 0, 1, [(eq, "$tld_option_formations",1), (eq, "$cheat_mode",1), (key_clicked, key_for_skirmish_end)],[(assign, "$archer_aim_active", 0), (display_message, "@Archer Aim DE-Activated!")]), 

	(0.5, 0, 0, [(eq,0,1), (call_script, "script_cf_order_skirmish_check")], [(call_script, "script_order_skirmish_skirmish")]), 
	(ti_after_mission_start, 0, 0, [(eq, "$cheat_mode",1) ], [
	          (get_player_agent_no, ":player"),
	          (agent_get_party_id, ":player_party", ":player"),
	          (try_for_range, ":i", slot_party_skirmish_d0, slot_party_skirmish_d8 + 1),
	               (party_set_slot, ":player_party", ":i", 0),
	          (try_end),]),

##Fix Divisions
	(ti_on_agent_spawn, 0, 0, [(eq, "$tld_option_formations",1)], [(store_trigger_param_1, ":agent"),(call_script, "script_agent_fix_division", ":agent")]),

## Formation Key Command Fixes

	(0, .3, 0, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_1)], [
		(eq, "$gk_order", gk_order_1),	#next trigger set MOVE menu?
		(game_key_is_down, gk_order_1),	#BUT player is holding down key?
		(assign, "$gk_order_hold_over_there", 1),
		(assign, "$gk_order", 0),
		(get_player_agent_no, ":player"), 
		(try_begin),
			(agent_slot_eq, ":player", slot_agent_tournament_point, 0),
			(eq, "$field_ai_horse_archer", 1),
			(agent_set_slot, ":player", slot_agent_tournament_point, 1),
			(assign, "$field_ai_horse_archer", 0),
		(try_end),
	]),

	(0, 0, 0, [(eq, "$tld_option_formations", 1),
		(game_key_clicked, gk_order_1)], [
		(try_begin),
			(eq, "$gk_order", 0),
			(assign, "$gk_order", gk_order_1),
		(else_try),
			(try_begin),
				(eq, "$gk_order", gk_order_1),	#HOLD			
				(call_script, "script_player_order_formations", mordr_hold),
				(assign, "$gk_order", 0),
			(else_try),
				(eq, "$gk_order", gk_order_2),	#ADVANCE
				(call_script, "script_player_order_formations", mordr_advance),
				(assign, "$gk_order", 0),
			(else_try),
				(eq, "$gk_order", gk_order_3),	#HOLD FIRE
			(try_end),
		(try_end),
	]),
	
	(0, 0, 0, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_2)], [
		(try_begin),
			(eq, "$gk_order", 0),
			(assign, "$gk_order", gk_order_2),
		(else_try),
			(try_begin),
				(eq, "$gk_order", gk_order_1),	#FOLLOW
				(call_script, "script_player_order_formations", mordr_follow),
				(assign, "$gk_order", 0),
			(else_try),
				(eq, "$gk_order", gk_order_2),	#FALL BACK
				(call_script, "script_player_order_formations", mordr_fall_back),
				(assign, "$gk_order", 0),
			(else_try),
				(eq, "$gk_order", gk_order_3),	#FIRE AT WILL
				(assign, "$gk_order", 0),
			(try_end),
		(try_end),
	]),
	
	(0, 0, 0, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_3)], [
		(try_begin),
			(eq, "$gk_order", 0),
			(assign, "$gk_order", gk_order_3),
		(else_try),
			(try_begin),
				(eq, "$gk_order", gk_order_1),	#CHARGE
				(call_script, "script_player_order_formations", mordr_charge),
				(assign, "$gk_order", 0),
			(else_try),
				(eq, "$gk_order", gk_order_2),	#SPREAD OUT
				(call_script, "script_player_order_formations", mordr_spread_out),
				(assign, "$gk_order", 0),
			(else_try),
				(eq, "$gk_order", gk_order_3),	#BLUNT WEAPONS
				(assign, "$gk_order", 0),
			(try_end),
		(try_end),
	]),
	
	(0, 0, 0, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_4)], [
		(try_begin),
			(eq, "$gk_order", gk_order_1),	#STAND GROUND
			(call_script, "script_player_order_formations", mordr_stand_ground),			
			(assign, "$gk_order", 0),
		(else_try),
			(eq, "$gk_order", gk_order_2),	#STAND CLOSER
			(call_script, "script_player_order_formations", mordr_stand_closer),
			(assign, "$gk_order", 0),
		(else_try),
			(eq, "$gk_order", gk_order_3),	#ANY WEAPON
			(assign, "$gk_order", 0),
		(try_end),
	]),
	
	(0, 0, 0, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_5)], [
		(try_begin),
			(eq, "$gk_order", gk_order_1),	#RETREAT
			(call_script, "script_player_order_formations", mordr_retreat),
			(assign, "$gk_order", 0),
		(else_try),
			(eq, "$gk_order", gk_order_2),	#MOUNT
			(assign, "$gk_order", 0),
      (try_end),
	]),
	
	(0, 0, 0, [(eq, "$tld_option_formations", 1),(game_key_clicked, gk_order_6)], [
		(eq, "$gk_order", gk_order_2),	#DISMOUNT
		(try_begin),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry), #JL: added 2/2/2011 to fix dismount issue
			(call_script, "script_formation_end", "$fplayer_team_no", grc_cavalry), #JL: added 2/2/2011 to fix dismount issue
		(try_end),
		(call_script, "script_player_order_formations", mordr_dismount),
		(assign, "$gk_order", 0),
	]),



	
	(0, 0, 0, [
		(eq, "$tld_option_formations", 1),
		(this_or_next|key_clicked, key_1),
		(this_or_next|key_clicked, key_2),
		(this_or_next|key_clicked, key_3),
		(this_or_next|key_clicked, key_4),
		(this_or_next|key_clicked, key_5),
		(this_or_next|key_clicked, key_6),
		(this_or_next|key_clicked, key_7),
		(this_or_next|key_clicked, key_8),
		(this_or_next|key_clicked, key_9),
		(this_or_next|key_clicked, key_0),
		(key_clicked, key_escape)	#doesn't work because ESC is omitted during command selection
	], [
		(assign, "$gk_order", 0)
	]),

#implement HOLD OVER THERE when player lets go of key
	(.5, 0, 0, [(eq, "$tld_option_formations", 1),(eq, "$gk_order_hold_over_there", 1),(neg|game_key_is_down, gk_order_1)], [		
		(call_script, "script_team_get_average_position_of_enemies_augmented", pos60, "$fplayer_team_no", grc_everyone),
		(assign, ":num_bgroups", 0),
		(try_for_range, reg0, 0, 9),
			(class_is_listening_order, "$fplayer_team_no", reg0),
			(val_add, ":num_bgroups", 1),
		(try_end),		
        (get_player_agent_no, "$fplayer_agent_no"), #can prevent script errors in rare cases
		(agent_get_position, pos22, "$fplayer_agent_no"),		
		(try_begin),
			(neq, "$infantry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_infantry),
			(team_get_order_position, pos2, "$fplayer_team_no", grc_infantry),
			(call_script, "script_point_y_toward_position", pos2, pos60),
			(try_begin),
				(gt, ":num_bgroups", 1),
				(agent_set_position, "$fplayer_agent_no", pos2),	#fake out script_cf_formation
				(try_begin),	#ignore script failure
					(call_script, "script_cf_formation", "$fplayer_team_no", grc_infantry, "$infantry_space", "$infantry_formation_type"),
				(try_end),
			(else_try),
				(assign, ":troop_count", 0),
				(try_for_agents, reg0),
					(call_script, "script_cf_valid_formation_member", "$fplayer_team_no", grc_infantry, "$fplayer_agent_no", reg0),
					(val_add, ":troop_count", 1),
				(try_end),
				(call_script, "script_get_centering_amount", "$infantry_formation_type", ":troop_count", "$infantry_space"),
				(position_move_x, pos2, reg0),
				(copy_position, pos1, pos2),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos1),
				(call_script, "script_form_infantry", "$fplayer_team_no", "$fplayer_agent_no", "$infantry_space", "$infantry_formation_type"),		
			(try_end),
			(assign, "$infantry_formation_move_order", mordr_hold),
		(try_end),
		(try_begin),
			(neq, "$cavalry_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_cavalry),
			(team_get_order_position, pos2, "$fplayer_team_no", grc_cavalry),
			(call_script, "script_point_y_toward_position", pos2, pos60),
			(try_begin),
				(gt, ":num_bgroups", 1),
				(agent_set_position, "$fplayer_agent_no", pos2),	#fake out script_cf_formation
				(try_begin),	#ignore script failure
					(call_script, "script_cf_formation", "$fplayer_team_no", grc_cavalry, "$cavalry_space", "$cavalry_formation_type"),
				(try_end),
			(else_try),
				# (assign, ":troop_count", 0),
				# (try_for_agents, reg0),
					# (call_script, "script_cf_valid_formation_member", "$fplayer_team_no", grc_cavalry, "$fplayer_agent_no", reg0),
					# (val_add, ":troop_count", 1),
				# (try_end),
				# (call_script, "script_get_centering_amount", "$cavalry_formation_type", ":troop_count", "$cavalry_space"),
				# (position_move_x, pos2, reg0),
				(copy_position, pos1, pos2),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos1),
				(call_script, "script_form_cavalry", "$fplayer_team_no", "$fplayer_agent_no", "$cavalry_space"),		
			(try_end),
			(assign, "$cavalry_formation_move_order", mordr_hold),
		(try_end),
		(try_begin),
			(neq, "$archer_formation_type", formation_none),
			(class_is_listening_order, "$fplayer_team_no", grc_archers),
			(team_get_order_position, pos2, "$fplayer_team_no", grc_archers),
			(call_script, "script_point_y_toward_position", pos2, pos60),
			(try_begin),
				(gt, ":num_bgroups", 1),
				(agent_set_position, "$fplayer_agent_no", pos2),	#fake out script_cf_formation
				(try_begin),	#ignore script failure
					(call_script, "script_cf_formation", "$fplayer_team_no", grc_archers, "$archer_space", "$archer_formation_type"),
				(try_end),
			(else_try),
				(assign, ":troop_count", 0),
				(try_for_agents, reg0),
					(call_script, "script_cf_valid_formation_member", "$fplayer_team_no", grc_archers, "$fplayer_agent_no", reg0),
					(val_add, ":troop_count", 1),
				(try_end),
				#(call_script, "script_get_centering_amount", "$archer_formation_type", ":troop_count", "$archer_space"), --old form code
				(call_script, "script_get_centering_amount", formation_default, ":troop_count", "$archer_space"),
				(val_mul, reg0, -1),
				(position_move_x, pos2, reg0),
				(copy_position, pos1, pos2),
				(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos1),
				#(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space"), #old from code
				(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
			(try_end),
			(assign, "$archer_formation_move_order", mordr_hold),
		(try_end),
		(agent_set_position, "$fplayer_agent_no", pos22),
		(assign, "$gk_order_hold_over_there", 0),
		(get_player_agent_no, ":player"),
		(try_begin),
			(agent_slot_eq, ":player", slot_agent_tournament_point, 1),
			(eq, "$field_ai_horse_archer", 0),
			(agent_set_slot, ":player", slot_agent_tournament_point, 0),
			(assign, "$field_ai_horse_archer", 1),
		(try_end),
	]),

] or []) + [

#attempt to avoid simultaneous formations function calls
	(1, 0, 0, [	
        (eq, "$tld_option_formations", 1),
		(neg|key_is_down, key_for_ranks),
		(neg|key_is_down, key_for_shield),
		(neg|key_is_down, key_for_wedge),
		(neg|key_is_down, key_for_square),
		(neg|key_is_down, key_for_undo),
	  ]+block_mb_gamekeys, [
		(set_fixed_point_multiplier, 100),
		(store_mod, ":fifth_second", "$fclock", 5),
		(call_script, "script_team_get_average_position_of_enemies_augmented", pos60, "$fplayer_team_no", grc_everyone),
		(try_begin),
			(eq, reg0, 0),	#no more enemies?
            (neq, "$g_encountered_party", -1), #not a training drill without enemies?
			(call_script, "script_formation_end", "$fplayer_team_no", grc_everyone),
		(else_try),
			(assign, "$autorotate_at_player", 0),
			(try_begin),
				(neq, "$infantry_formation_type", formation_none),
				(try_begin),
					(eq, "$infantry_formation_move_order", mordr_follow),
					(call_script, "script_cf_formation", "$fplayer_team_no", grc_infantry, "$infantry_space", "$infantry_formation_type"),
				(else_try),	#periodically reform
					(eq, ":fifth_second", 0),
	#				(team_get_order_position, pos0, "$fplayer_team_no", grc_infantry),
					(call_script, "script_get_formation_position", pos0, "$fplayer_team_no", grc_infantry),
					(call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", "$fplayer_team_no", grc_infantry),
					(call_script, "script_point_y_toward_position", pos1, pos60),
					(position_copy_rotation, pos0, pos1),
					(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos0),
					(copy_position, pos1, pos0),
					(call_script, "script_form_infantry", "$fplayer_team_no", "$fplayer_agent_no", "$infantry_space", "$infantry_formation_type"),
				(try_end),
			(try_end),
			(try_begin),
				(neq, "$cavalry_formation_type", formation_none),
				(try_begin),
					(eq, "$cavalry_formation_move_order", mordr_follow),
					(call_script, "script_cf_formation", "$fplayer_team_no", grc_cavalry, "$cavalry_space", "$cavalry_formation_type"),
				(else_try),	#periodically reform
					(eq, ":fifth_second", 0),
	#				(team_get_order_position, pos0, "$fplayer_team_no", grc_cavalry),
					(call_script, "script_get_formation_position", pos0, "$fplayer_team_no", grc_cavalry),
					(call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", "$fplayer_team_no", grc_cavalry),
					(call_script, "script_point_y_toward_position", pos1, pos60),
					(position_copy_rotation, pos0, pos1),
					(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos0),
					(copy_position, pos1, pos0),
					(call_script, "script_form_cavalry", "$fplayer_team_no", "$fplayer_agent_no", "$cavalry_space"),
				(try_end),
			(try_end),
			(try_begin),
				(neq, "$archer_formation_type", formation_none),
				(try_begin),
					(eq, "$archer_formation_move_order", mordr_follow),
					(call_script, "script_cf_formation", "$fplayer_team_no", grc_archers, "$archer_space", "$archer_formation_type"),
				(else_try),	#periodically reform
					(eq, ":fifth_second", 0),
	#				(team_get_order_position, pos0, "$fplayer_team_no", grc_archers),
					(call_script, "script_get_formation_position", pos0, "$fplayer_team_no", grc_archers),
					(call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", "$fplayer_team_no", grc_archers),
					(call_script, "script_point_y_toward_position", pos1, pos60),
					(position_copy_rotation, pos0, pos1),
					(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos0),
					(copy_position, pos1, pos0),
					#(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space"), old form code
					(call_script, "script_form_archers", "$fplayer_team_no", "$fplayer_agent_no", "$archer_space", "$archer_formation_type"),
				(try_end),
			(try_end),
			(assign, "$autorotate_at_player", formation_autorotate_at_player),
		(try_end),
		(val_add, "$fclock", 1),
	]),

]+mb_formations

#end formations triggers