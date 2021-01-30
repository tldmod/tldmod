from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *

from module_info import wb_compile_switch as is_a_wb_mt

if(is_a_wb_mt):
  #swy-- import Warband-specific death cam and AI/formation code... if needed.
  from module_mission_templates_TLD_wb import *

# COMMAND CURSOR MINIMOD by dstemmer # (Added by CppCoder) (I forgot original author)
# http://forums.taleworlds.com/index.php?topic=63370.0

common_init_command_cursor = (
  ti_before_mission_start, 0, 0, [],
  [
    (assign, "$order_move_to_pos43_start", 0),
    (assign, "$hold_key_1second",0),
  ])

# Sped up from 1 second to 0.5 second.
common_command_cursor_countdown = (
  0, 0.5, 0, 
  [
    (try_begin),
      (neg|game_key_is_down, gk_order_halt),
	    (assign, "$hold_key_1second",0),
    (try_end),
    (game_key_is_down, gk_order_halt),
  ],
  [
    (try_begin),
      (game_key_is_down, gk_order_halt),
	    (assign, "$hold_key_1second",1),
    (try_end),
  ])

common_command_cursor_key_pressed = (
  0.05, 0, 0,
    [
      (game_key_is_down, gk_order_halt),
      (eq, "$hold_key_1second",1),
      (get_player_agent_no, ":player"),
      (agent_get_look_position, pos1, ":player"),
      (position_move_z, pos1, 120),
      (try_begin),
        (call_script, "script_cf_shift_pos1_along_y_axis_to_ground", 30000),
        (assign, "$order_move_to_pos43_start", 1),
        (particle_system_burst, "psys_fat_arrow", pos1, 1),
        (copy_position, pos43, pos1),
      (else_try),
        (assign, "$order_move_to_pos43_start", 0),
      (try_end),
    ], []
)

# Modified to have proper message when multiple groups are selected (e.g., "Infantry and Cavalry"). (CppCoder)
common_order_move_to_pos43 = (
  0, 0, 0,
    [
      (eq, "$order_move_to_pos43_start", 1),
      (neg|game_key_is_down, gk_order_halt),
      
      (assign, "$order_move_to_pos43_start", 0),
      (particle_system_burst, "psys_fat_arrow_rising", pos43, 1),
      (get_player_agent_no, ":player"),
      (agent_get_team, ":player_team", ":player"),
      (set_show_messages, 0),
      (assign, ":num_listening", 0),
      (assign, ":str_id", s1),
      (try_begin),
        (class_is_listening_order, ":player_team", grc_infantry),
        (class_is_listening_order, ":player_team", grc_archers),
        (class_is_listening_order, ":player_team", grc_cavalry),
	(try_begin),
		(eq, "$tld_option_formations", 1),
		(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos43),
		(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos43),
		(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos43),
	(else_try),
        	(team_give_order, ":player_team", grc_everyone, mordr_hold),
        	(team_set_order_position, ":player_team", grc_everyone, pos43),
	(try_end),
        (str_store_string, s1, "@Everyone"),
      (else_try),
	(try_begin),
        	(class_is_listening_order, ":player_team", grc_infantry),
      		(set_show_messages, 0),
		(try_begin),
			(eq, "$tld_option_formations", 1),
			(call_script, "script_set_formation_position", "$fplayer_team_no", grc_infantry, pos43),
		(else_try),
        		(team_give_order, ":player_team", grc_infantry, mordr_hold),
        		(team_set_order_position, ":player_team", grc_infantry, pos43),
		(try_end),
      		(set_show_messages, 1),
        	(str_store_string, ":str_id", "@Infantry"),
		(val_add, ":str_id", 1),
		(val_add, ":num_listening", 1),
      	(try_end),
	(try_begin),
        	(class_is_listening_order, ":player_team", grc_archers),
      		(set_show_messages, 0),
		(try_begin),
			(eq, "$tld_option_formations", 1),
			(call_script, "script_set_formation_position", "$fplayer_team_no", grc_archers, pos43),
		(else_try),
        		(team_give_order, ":player_team", grc_archers, mordr_hold),
        		(team_set_order_position, ":player_team", grc_archers, pos43),
		(try_end),
      		(set_show_messages, 1),
        	(str_store_string, ":str_id", "@Archers"),
		(val_add, ":str_id", 1),
		(val_add, ":num_listening", 1),
      	(try_end),
	(try_begin),
        	(class_is_listening_order, ":player_team", grc_cavalry),
      		(set_show_messages, 0),
		(try_begin),
			(eq, "$tld_option_formations", 1),
			(call_script, "script_set_formation_position", "$fplayer_team_no", grc_cavalry, pos43),
		(else_try),
        		(team_give_order, ":player_team", grc_cavalry, mordr_hold),
        		(team_set_order_position, ":player_team", grc_cavalry, pos43),
		(try_end),
      		(set_show_messages, 1),
        	(str_store_string, ":str_id", "@Cavalry"),
		(val_add, ":str_id", 1),
		(val_add, ":num_listening", 1),
      	(try_end),
      (try_end),
      (set_show_messages, 1),
      (try_begin),
		(try_begin),
			(le, ":num_listening", 1),
			(str_store_string, s10, "@{s1}"),
		(else_try),
			(eq, ":num_listening", 2),
			(str_store_string, s10, "@{s1} and {s2}"),
		(else_try),
			(eq, ":num_listening", 3),
			(str_store_string, s10, "@{s1}, {s2} and {s3}"),
		(try_end),
      (try_end),
      (display_message, "@{s10}, Move over there!"),
    ], []
)
#swy-- command cursor minimod only included with M&B 1.011, as Warband already seems to come with similar functionality when long-pressing F1 key.
command_cursor_sub_mod = (not is_a_wb_mt==1 and 
[
	common_init_command_cursor,
  
	common_command_cursor_countdown,
	common_command_cursor_key_pressed,
  
	common_order_move_to_pos43,
] or [])
# COMMAND CURSOR MINIMOD #

# cpp-- Prevents an issue of compiling where it doesnt know what this is if its M&B 1.011
if is_a_wb_mt==0: 
 ti_on_order_issued = 0 

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

mb_formations = (not is_a_wb_mt==1 and mb_only_formations or [])
# VANILLA FORMATIONS FIX #

# WARBAND FORMATIONS FIX #

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



#cpp-- The formation updates are only included with M&B Warband.

wb_formations = (is_a_wb_mt==1 and 
[
	wb_formation_order,
] or [])

wb_command_cursor = (is_a_wb_mt==1 and 
[
	wb_command_cursor_init,
	wb_command_cursor_f1_down,
	wb_command_cursor_f1_timer,
	wb_command_cursor_arrow_mode,
	wb_command_cursor_f1_up
	
] or [])

# WARBAND FORMATIONS FIX #



# Something I'm testing with. -CC
tld_wargs_attack_horses = (2, 0, 0, [(gt, "$wargs_in_battle", 0)], 
			[
				(try_for_agents, ":warg"),
					(agent_is_human, ":warg"),
					(agent_is_alive, ":warg"),
					(agent_get_horse, ":mount", ":warg"),
					(gt, ":mount", -1),
					(agent_get_troop_id, ":troop", ":warg"),
					(is_between, ":troop", warg_ghost_begin, warg_ghost_end),
					(assign, ":stop", 0),
					(try_for_agents, ":target"),
						(neq, ":stop", 1),
						(agent_is_human, ":target"),
						(agent_is_alive, ":target"),
						(agent_get_horse, ":horse", ":target"),
						(gt, ":horse", -1),
						(agent_get_position, pos1, ":warg"),
						(agent_get_position, pos2, ":target"),
						(set_fixed_point_multiplier, 100),
						(get_distance_between_positions, ":dist", pos1, pos2),
						(lt, ":dist", 300),
						(agent_get_team, ":team_a", ":warg"),
						(agent_get_team, ":team_b", ":target"),
						(teams_are_enemies, ":team_a", ":team_b"),
						(store_random_in_range, reg0, 0, 100),
						(store_random_in_range, reg1, 5, 10),
						(try_begin),
							(get_player_agent_no, ":player"),
							(eq, ":target", ":player"),
							(lt, reg0, 15), # 15% chance
							(agent_get_troop_id,":troop", ":warg"),
							(str_store_troop_name, s1, ":troop"),
							(display_message, "@{s1} delivers {reg1} damage to mount."),
							(set_show_messages, 0),
							(store_agent_hit_points, ":hp", ":horse", 1),
							(val_sub, ":hp", reg1),
	  	 					(agent_set_hit_points, ":horse", ":hp", 1),
	   						(agent_deliver_damage_to_agent, ":warg", ":horse"),
							(set_show_messages, 1),
						(else_try),
							(lt, reg0, 15), # 15% chance
							(store_agent_hit_points, ":hp", ":horse", 1),
							(val_sub, ":hp", reg1),
	  	 					(agent_set_hit_points, ":horse", ":hp", 1),
	   						(agent_deliver_damage_to_agent, ":warg", ":horse"),
							(assign, ":stop", 1),
						(try_end),
					(try_end),
				(try_end),
			])


# This trigger tracks horses for riders falling off horse. -CC
tld_track_riders = (ti_on_agent_spawn, 0, 0, [], 
			[
				(store_trigger_param_1,     ":cur_agent"),

 				(agent_is_human,            ":cur_agent"),
 				(agent_is_alive,            ":cur_agent"),
				(agent_get_horse, ":horse", ":cur_agent"),

				# no need to check, -1 means no horse, while 0+ means a horse.
				(agent_set_slot, ":cur_agent", slot_agent_mount, ":horse"),
			])

# This trigger damages agents that have fallen off their horse. :) -CC
tld_damage_fallen_riders = (0.1, 0, 0, [], 
				[
				(try_for_agents, ":mount"),
					(agent_is_human|neg, ":mount"),
					(agent_is_alive|neg, ":mount"),
					(assign, ":continue", 1),
					(try_for_agents, ":rider"),
						(agent_is_human, ":rider"),
						(agent_is_alive, ":rider"),	
						(agent_get_troop_id,":troop_id", ":rider"),
						(is_between|neg, ":troop_id", warg_ghost_begin, warg_ghost_end), # cpp: Dont allow wargs to fall unconscious
						(eq, ":continue", 1),
						(agent_slot_eq, ":rider", slot_agent_mount, ":mount"),
						(store_agent_hit_points, ":hp", ":rider", 1),
						(store_random_in_range, reg0, 5, 15), # damage calculation here, reg0 stores damage.
						(try_begin),
			 				(get_player_agent_no, ":player_agent"),
							(eq, ":rider", ":player_agent"),
							(display_message, "@You fall off of your mount!", color_bad_news),
							(display_message, "@Received {reg0} damage.", 0xD5B7B7),
						(try_end),					
						(val_sub, ":hp", reg0),
	  	 				(agent_set_hit_points, ":rider", ":hp", 1),
						(try_begin),
			 				(get_player_agent_no, ":player_agent"),
							(neq, ":rider", ":player_agent"),
							(assign, ":agent_killed", 0),
							(assign, ":agent_killed_1", 0),
							(try_begin),
								(lt, ":hp", 0),
								(set_show_messages, 0),	
								(agent_get_kill_count, ":agent_killed", ":rider"),
	   							(agent_deliver_damage_to_agent, ":rider", ":rider"),
								(agent_get_kill_count, ":agent_killed_1", ":rider"),
								(set_show_messages, 1),
							(try_end),
							(try_begin),
								(agent_is_alive|neg, ":rider"),
								(agent_get_party_id, ":party_no", ":rider"),
								(agent_get_troop_id,":troop", ":rider"),
								(str_store_troop_name, s1, ":troop"),
								(try_begin),
									(eq, ":party_no", "p_main_party"),
									(assign, ":color", 0xB48211), # Gold colored msg
								(else_try),
									(agent_is_ally|neg, ":rider"),
									(assign, ":color", 0x42D8A6), # teal-green colored msg
								(else_try),
									(assign, ":color", 0xB06EDA), # Lt. Purple colored msg
								(try_end),
								(display_message, "@{s1} fell unconscious.", ":color"),
							(try_end),
							# MESSAGE CODE END
							(try_begin), # Clone the agent back into party if killed.
								(gt, ":agent_killed_1", ":agent_killed"),
								(agent_get_party_id, ":party_no", ":rider"),
								(agent_get_troop_id,":troop", ":rider"),
								(neg|troop_is_hero, ":troop"),	# Catch to prevent duplicate heroes.
								(agent_set_slot, ":rider", slot_agent_wounded, 1),
								(gt, ":party_no", -1),
								(party_add_members, ":party_no", ":troop", 1),
								(party_wound_members, ":party_no", ":troop", 1),
							(try_end),
						(else_try),
	   						(agent_deliver_damage_to_agent, ":rider", ":rider"),
						(try_end),
						(agent_set_slot, ":rider", slot_agent_mount, -1), # no horse now.
						(assign, ":continue", 0),
					(try_end),
				(try_end),
				])


tld_fallen_riders_get_damaged = (is_a_wb_mt==1 and 
[
	kham_track_riders,
	kham_damage_fallen_riders,
	noxbru_rider_dismounts,
	noxbru_rider_mounts


] or [

	tld_damage_fallen_riders, 
	tld_track_riders
	
])
		

# This trigger makes wounded agents move slower. -CC
tld_slow_wounded  = (1, 0, 0, [(eq, "$slow_when_wounded", 1),],
	[
				(try_for_agents, ":cur_agent"),
					(agent_is_human, ":cur_agent"),
					(agent_is_alive, ":cur_agent"),
					(agent_get_troop_id,":troop", ":cur_agent"),
	 		 		(troop_get_type, ":race", ":troop"),
	 				(neq, ":race", tf_troll),			# trolls are not influenced by wounds.
					(agent_get_horse, ":horse", ":cur_agent"),
				
				] + ((is_a_wb_mt==1) and [
					(try_begin),
						(le, ":horse", -1),
						(store_agent_hit_points, ":hp", ":cur_agent"),
						(try_begin),
							(lt, ":hp", 25),
	  						(agent_set_speed_limit,":cur_agent", 2),
						(else_try),
							(lt, ":hp", 50),
	  						(agent_set_speed_limit,":cur_agent", 4),
						(else_try),
							(le, ":hp", 75),
	  						(agent_set_speed_limit,":cur_agent", 8),
						(else_try),
							(gt, ":hp", 75),
	  						(agent_set_speed_limit,":cur_agent", 100), # no speed limit
						(try_end),
					(try_end),
				(try_end),
				
				] or [
					(try_begin),
						(gt, ":horse", -1),
						(store_agent_hit_points, ":hp", ":horse"),
						(try_begin),
							(lt, ":hp", 25),
	  						(agent_set_speed_limit,":cur_agent", 8),
						(else_try),
							(lt, ":hp", 50),
	  						(agent_set_speed_limit,":cur_agent", 16),
						(else_try),
							(le, ":hp", 75),
	  						(agent_set_speed_limit,":cur_agent", 32),
						(else_try),
							(agent_set_speed_limit,":cur_agent", 100), # no speed limit
						(try_end),
					(else_try),
						(store_agent_hit_points, ":hp", ":cur_agent"),
						(try_begin),
							(lt, ":hp", 25),
	  						(agent_set_speed_limit,":cur_agent", 2),
						(else_try),
							(lt, ":hp", 50),
	  						(agent_set_speed_limit,":cur_agent", 4),
						(else_try),
							(le, ":hp", 75),
	  						(agent_set_speed_limit,":cur_agent", 8),
						(else_try),
							(gt, ":hp", 75),
	  						(agent_set_speed_limit,":cur_agent", 100), # no speed limit
						(try_end),
					(try_end),
				(try_end),
				]) + [
	])
			
	

# CC: This trigger prevents galadriel (maybe other non-battle heroes?) from fighting in battles.
tld_remove_galadriel = 	(0.1,0,0,
			[(eq, "$current_town", "p_town_caras_galadhon")], 
			[
			(try_for_agents, ":cur_agent"),
				(agent_get_troop_id,":troop", ":cur_agent"),
				(eq, ":troop", "trp_lorien_lord"),
				(call_script, "script_remove_agent", ":cur_agent"),
			(try_end),
			])

tld_remove_volunteer_troops = (0.1,0,0, [(is_between, "$current_town", centers_begin, centers_end)], 
			[
			(try_for_agents, ":cur_agent"),
				(agent_get_troop_id,":troop", ":cur_agent"),
				(this_or_next|eq, ":troop", "trp_volunteers"), #Kham - remove 'volunteer' agent
				(eq, ":troop", "trp_werewolf"), # Kham - Remove Werewolves from Sieges
				(call_script, "script_remove_agent", ":cur_agent"),
			(try_end),
			])
	

# a trigger to fix viewpoint... not used. Too many drawbacks (mtarini)
tld_fix_viewpoint = (0,0,0,[],[
  (try_begin),
    #(this_or_next|game_key_clicked, gk_view_char),
    (this_or_next|key_clicked, key_t),
    (game_key_clicked, gk_cam_toggle),
	
	#(mission_cam_set_mode,1,
	(store_sub, reg55, 1, reg55), # toggle reg 55
	(mission_cam_set_mode,reg55,0.55),
	(display_message,"@camera mode: {reg55?custom:natural}"),
  (try_end),

  (try_begin),
    (eq, reg55, 1),
	(get_player_agent_no, ":player_agent"),
	(agent_get_look_position, pos40, ":player_agent"),
	
	(agent_get_horse, ":horse_agent", ":player_agent"),
    (try_begin),(ge, ":horse_agent", 0),
      (position_move_z, pos40, 80,1), # lift for mounted players
    (try_end),
	
	(try_begin),
		#(agent_get_class, ":race", ":player_agent"),
		(position_move_z, pos40, 180, 1),
		(position_move_y, pos40, 10, 0), # move camera forward a bit
	(try_end),
	(mission_cam_set_position, pos40),
  (try_end),
])

common_battle_mission_start = (ti_before_mission_start, 0, 0, [],[
	(team_set_relation, 0, 2, 1),
	(team_set_relation, 1, 3, 1),
	(call_script, "script_change_banners_and_chest"),
	#(set_rain, 0,100), # switch off ingame weather
	] + ((is_a_wb_mt==1) and [
	(party_get_slot, ":encounter_effect", "p_main_party", slot_party_battle_encounter_effect),
	(try_begin),
		(eq, ":encounter_effect", LORIEN_MIST),
		(set_rain, 2,500), #yellow thingies in elven places
	(else_try),
		(eq, ":encounter_effect", SARUMAN_STORM),
		(set_rain, 1,300),
	(else_try),
		(set_rain, 0, 100),
	(try_end),
	
	] or [(set_rain, 0, 100)]) + [
	])

common_battle_tab_press = (ti_tab_pressed, 0, 0, [],[
	(try_begin),
		(eq, "$battle_won", 1),
		(call_script, "script_count_mission_casualties_from_agents"),
		(party_set_slot, "p_main_party", slot_party_battle_encounter_effect, NO_EFFECT_PRESENT),
		(finish_mission,0),
		(assign, "$g_custom_battle_team1_death_count", 0),
		(get_player_agent_no, ":player"),
	    (agent_get_kill_count, "$g_custom_battle_team1_death_count",":player"),
	    (agent_get_kill_count, ":wounded",":player", 1),
	    (val_add, "$g_custom_battle_team1_death_count", ":wounded"),
	(else_try), #MV added this section
		(main_hero_fallen),
		(assign, "$pin_player_fallen", 1),
		(str_store_string, s5, "str_retreat"),
		(call_script, "script_simulate_retreat", 10, 20),
		(assign, "$g_battle_result", -1),
		(set_mission_result,-1),
		(call_script, "script_count_mission_casualties_from_agents"),
		(party_set_slot, "p_main_party", slot_party_battle_encounter_effect, NO_EFFECT_PRESENT),
		(finish_mission,0),
		(assign, "$g_custom_battle_team1_death_count", 0),
		(get_player_agent_no, ":player"),
	    (agent_get_kill_count, "$g_custom_battle_team1_death_count",":player"),
	    (agent_get_kill_count, ":wounded",":player", 1),
	    (val_add, "$g_custom_battle_team1_death_count", ":wounded"),
	(else_try),
		(call_script, "script_cf_check_enemies_nearby"),
		(question_box,"str_do_you_want_to_retreat"),
	(else_try),
		(display_message,"str_can_not_retreat"),
	(try_end)])

common_arena_fight_tab_press = (ti_tab_pressed, 0, 0, [],[(question_box,"str_give_up_fight")])

common_custom_battle_tab_press = (ti_tab_pressed, 0, 0, [],[
	(try_begin),
		(neq, "$g_battle_result", 0),
		(call_script, "script_custom_battle_end"),
		(finish_mission),
	(else_try),
		(question_box,"str_give_up_fight"),
	(try_end)])

custom_battle_check_victory_condition = (1, 60, ti_once,[
	(store_mission_timer_a,reg1),
	(ge,reg1,10),
	(all_enemies_defeated, 2),
	(neg|main_hero_fallen, 0),
	(set_mission_result,1),
	(display_message,"str_msg_battle_won"),
	(assign, "$battle_won",1),
	(assign, "$g_battle_result", 1),
	],[
	(call_script, "script_custom_battle_end"),
	(finish_mission, 1)])

custom_battle_check_defeat_condition = (1, 4, ti_once, [(main_hero_fallen),(assign,"$g_battle_result",-1)],[
	(call_script, "script_custom_battle_end"),
	(finish_mission)])

common_custom_battle_question_answered = (ti_question_answered, 0, 0, [],
   [ (store_trigger_param_1,":answer"),
     (eq,":answer",0),
     (assign, "$g_battle_result", -1),
     (call_script, "script_custom_battle_end"),
     (finish_mission)]
)

common_music_situation_update = (30, 0, 0, [],[(call_script, "script_combat_music_set_situation_with_culture")])
common_battle_check_friendly_kills = (2, 0, 0, [],[ (call_script, "script_check_friendly_kills")])
common_battle_check_victory_condition = (1, 60, ti_once,[
	(store_mission_timer_a,reg(1)),
	(ge,reg(1),10),
	(all_enemies_defeated, 5),
	#(neg|main_hero_fallen, 0), #MV
	(set_mission_result,1),
	(display_message,"str_msg_battle_won"),
	(assign,"$battle_won",1),
	(assign, "$g_battle_result", 1),
	(call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
    ],
   (is_a_wb_mt==1 and [
        (assign, ":hp", 0),
        (try_begin),
            (get_player_agent_no, ":agent"), (ge, ":agent", 0),
            (agent_get_horse, ":bear" ,":agent"), (ge, ":bear", 0),
            (store_agent_hit_points, ":hp", ":bear", 0), 
        (end_try),
        (call_script, "script_cf_select_human_form", ":hp"),
    ] or []) + [
	(call_script, "script_count_mission_casualties_from_agents"),
	(finish_mission, 1)])

common_battle_victory_display = (10, 0, 0, [ (eq,"$battle_won",1)],[(display_message,"str_msg_battle_won")])
common_battle_order_panel = (0, 0, 0, [],
	[
	    (try_begin),
	      #-- {show up the ticker on backspace}
	      (game_key_clicked, gk_view_orders),
	      (neq, "$g_presentation_battle_active", 1),
	      #--

	      (start_presentation, "prsnt_battle"),
	    (try_end),
	]
	 + (is_a_wb_mt==1 and 
	[
	    #swy-- what a shamefur dispray!
	    (try_begin),
	      #-- {guard against rogue Esc presses that kill the ticker without notice}
	      (eq, "$g_presentation_battle_active", 1),
	      (neg|is_presentation_active, "prsnt_battle"),
	      #--

	      (assign, "$g_presentation_battle_active", 0),
	      (set_show_messages, 1),

	      (try_for_agents, ":cur_agent"),
	        (agent_set_slot, ":cur_agent", slot_agent_map_overlay_id, 0),
	      (try_end),

	      (presentation_set_duration, 0),
	    (try_end)
	] or [])
)

common_battle_order_panel_tick = (0.1, 0, 0, [(eq, "$g_presentation_battle_active", 1),], [(call_script, "script_update_order_panel_statistics_and_map")])
common_battle_inventory = (ti_inventory_key_pressed, 0, 0, [],[(display_message,"str_use_baggage_for_inventory")])
common_inventory_not_available = (ti_inventory_key_pressed, 0, 0,[(display_message, "str_cant_use_inventory_now")],[])

common_battle_on_player_down =  (1, 4, ti_once, [(main_hero_fallen)],  [   # MV and MT
  (assign, "$pin_player_fallen", 1),
  (try_begin), #GA: player injury or death?
    (store_random_in_range, reg12,0,5),
    (eq,reg12,0), #20% chance for injury
    (eq, "$tld_option_injuries",1),
    (call_script, "script_injury_routine", "trp_player"),
  (try_end),
  (store_normalized_team_count,":a", 0), 	#  check that battle still goes on MT
  (store_normalized_team_count,":b", 1),
  (gt,":b",0),(gt,":a",0),

    #MV: not sure about this one, will see if it's needed
	# (set_show_messages, 0), #stop messages JL
	# (team_give_order, "$fplayer_team_no", grc_everyone, mordr_charge), #charges everyone JL
	# (try_begin),
	# (eq, "$tld_option_formations", 1), #if Formations is turned on JL
	# (team_set_order_listener, "$fplayer_team_no", grc_everyone,-1), #clear listener for everyone JL
	# (call_script, "script_player_order_formations", mordr_charge), #send formations order to charge JL
	# (try_end),
	# (team_give_order, "$fplayer_team_no", grc_everyone, mordr_fire_at_will), #JL PoP 3.3
	# (team_give_order, "$fplayer_team_no", grc_everyone, mordr_use_any_weapon), #JL PoP 3.3
	# (set_show_messages, 1), #show messages again JL
	# (display_message, "@Your troops are charging!"), # display message JL
              
    #Native calc retreat on player death
    # (str_store_string, s5, "str_retreat"),
    # (call_script, "script_simulate_retreat", 10, 20),
    # (assign, "$g_battle_result", -1),
    # (set_mission_result,-1),
    # (call_script, "script_count_mission_casualties_from_agents"),
    # (finish_mission,0)
    (display_message, "str_player_down"), #MV
])


## MadVader deathcam begin: this is a simple death camera from kt0, works by moving the player body so mouselook is automatic
common_init_deathcam = (0, 0, ti_once, [],
[
  (assign, "$tld_camera_on", 0),
  
  # restrictions on movement or crash happens
  (get_scene_boundaries,             pos1,
                                     pos2),
  # --
  (position_get_x,"$battlemap_min_x",pos1),
  (position_get_y,"$battlemap_min_y",pos1),
  (position_get_x,"$battlemap_max_x",pos2),
  (position_get_y,"$battlemap_max_y",pos2),
])
  
common_start_deathcam = (0, 4, ti_once, # 4 seconds delay before the camera activates
[
  (main_hero_fallen),
  (eq, "$tld_camera_on", 0)
],
[
  (assign, "$tld_camera_on", 1)
])

common_move_deathcam = (0, 0, 0,
[
  (eq, "$tld_camera_on", 1),
  (this_or_next|game_key_clicked, gk_move_forward),
  (this_or_next|game_key_is_down, gk_move_forward),
  
  (this_or_next|game_key_clicked, gk_move_backward),
  (this_or_next|game_key_is_down, gk_move_backward),
  
  (this_or_next|game_key_clicked, gk_move_left),
  (this_or_next|game_key_is_down, gk_move_left),

  (this_or_next|game_key_clicked, gk_move_right),
  (             game_key_is_down, gk_move_right),
],
[
  (get_player_agent_no,             ":player_agent"),
  (agent_get_look_position,   pos1, ":player_agent"),
  
  #swy-- made the controls async and monolithic!
  
  (try_begin),
    (this_or_next|game_key_clicked, gk_move_forward),
    (             game_key_is_down, gk_move_forward),
    # --
    (position_move_y,         pos1,  18),
  (try_end),
  
  (try_begin),
    (this_or_next|game_key_clicked, gk_move_backward),
    (             game_key_is_down, gk_move_backward),
    # --
    (position_move_y,         pos1, -18),
  (try_end),
  
  (try_begin),
    (this_or_next|game_key_clicked, gk_move_left),
    (             game_key_is_down, gk_move_left),
    # --
    (position_move_x,         pos1, -13),
  (try_end),
  
  (try_begin),
    (this_or_next|game_key_clicked, gk_move_right),
    (             game_key_is_down, gk_move_right),
    # --
    (position_move_x,         pos1,  13),
  (try_end),
  
  (position_get_x,":x",pos1),
  (position_get_y,":y",pos1),
  
  (try_begin),
    (is_between, ":x", "$battlemap_min_x", "$battlemap_max_x"),
    (is_between, ":y", "$battlemap_min_y", "$battlemap_max_y"),
    # --
    (agent_set_position, ":player_agent", pos1),
  (try_end)
])
 
common_deathcam_triggers = (not is_a_wb_mt==1 and 
[
	common_init_deathcam,
	common_start_deathcam,

	common_move_deathcam,

] or [

	common_init_deathcam_wb,
	common_start_deathcam_wb,

	common_move_deathcam_wb,
	common_rotate_deathcam_wb,
])


moto_formations_triggers = (not is_a_wb_mt==1 and 

[common_init_deathcam,] 

or  

  field_ai_triggers + order_weapon_type_triggers +
  utility_triggers + extended_battle_menu + common_division_data + division_order_processing + real_deployment + formations_triggers_moto + AI_triggers_moto + battle_encounters_effects + [
  tld_kill_or_wounded_triggers,
])

## MadVader deathcam end

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

cheat_kill_self_on_ctrl_s = ( 1,1.5,1.5,[
	(eq, "$cheat_mode",1),
	(key_is_down, key_s),(this_or_next|key_is_down, key_left_control),(key_is_down, key_right_control),
    (get_player_agent_no, ":player_agent"),
	(agent_get_team, ":player_team", ":player_agent"),
	(display_message, "@CHEAT: SELF mind blast!!! (ctrl+s)"),
    (try_for_agents, ":agent"),
   		(agent_is_human,":agent"),
        (agent_get_team, reg10, ":agent"), (neg|teams_are_enemies , reg10, ":player_team"),
		(agent_get_horse,":horse",":agent"),
		(try_begin), (gt, ":horse", -1), 
			(agent_set_animation, ":agent", "anim_nazgul_noooo_mounted_short"), 
			(agent_set_animation, ":horse", "anim_horse_rear"), 
		(else_try),
			(agent_set_animation, ":agent", "anim_nazgul_noooo_short"), 
		(try_end),
	(try_end),
	], [ 
	(key_is_down, key_s),(this_or_next|key_is_down, key_left_control),(key_is_down, key_right_control),
    (get_player_agent_no, ":player_agent"),
	(agent_get_team, ":player_team", ":player_agent"),
	(display_message, "@CHEAT: player team: \"A-a-a-a-argh!\" (ctrl+s)"),
	(set_show_messages , 0),
    (try_for_agents, ":agent"),
       (agent_get_team, reg10, ":agent"), (neg|teams_are_enemies , reg10, ":player_team"),
	   (agent_set_hit_points , ":agent",0,1),
	   (agent_deliver_damage_to_agent, ":player_agent", ":agent"),
	(try_end),
	(set_show_messages , 1),
])

#MV: commented out - not used and why not use built-in Ctrl-Shift-F4 like normal people? Really.
# MT: because this is much more versatile... tap, and enemies just stop. Keep pressed, and they all die insatantly (instead of pressing Ctrl+F4 like mad, often getting killed anyway). Beside, I Alt+F4 too often instead of Ctrl+F4. 
# No reasons to remove it...
#GA: use Ctrl+Shift+F4. commented to not use CPU cycles
# cheat_kill_all_on_ctrl_k = (1,1.5,1.5,[
    # (eq, "$cheat_mode",1),
	# (key_is_down, key_k),(this_or_next|key_is_down, key_left_control),(key_is_down, key_right_control),
    # (get_player_agent_no, ":player_agent"),
	# (agent_get_team, ":player_team", ":player_agent"),
	# (display_message, "@CHEAT: Mind blast!!! (ctrl+k)"),
    # (try_for_agents, ":agent"),
        # (agent_get_team, reg10, ":agent"), (teams_are_enemies , reg10, ":player_team"),
		# (agent_get_horse,":horse",":agent"),
		# (try_begin), (gt, ":horse", -1), 
			# (agent_set_animation, ":agent", "anim_nazgul_noooo_mounted_short"), 
			# (agent_set_animation, ":horse", "anim_horse_rear"), 
		# (else_try),
			# (agent_set_animation, ":agent", "anim_nazgul_noooo_short"), 
		# (try_end),
	# (try_end),
  # ], [ 
	# (key_is_down, key_k),(this_or_next|key_is_down, key_left_control),(key_is_down, key_right_control),
    # (get_player_agent_no, ":player_agent"),
	# (agent_get_team, ":player_team", ":player_agent"),
	# (display_message, "@CHEAT: everybody: \"A-a-a-a-argh!\" (ctrl+k)"),

	# (set_show_messages , 0),
    # (try_for_agents, ":agent"),
       # (agent_get_team, reg10, ":agent"), (teams_are_enemies , reg10, ":player_team"),
	   # (agent_set_hit_points , ":agent",0,1),
	   # (agent_deliver_damage_to_agent, ":player_agent", ":agent"),
	# (try_end),
	# (set_show_messages , 1),
# ])


 # triggers to bow to lords  -- a set of triggers  (mtarini)
custom_tld_bow_to_kings = [
	(ti_before_mission_start , 0, 0, [],[
		(assign, "$agent_king", -1),
		(assign, "$player_is_bowing", 0),]),
	(ti_on_agent_spawn       , 0, 0, [],[ # on spawn: register lords
		# to do: this way you bow to leaders OR to marshalls. Must both to both
	    (store_trigger_param_1, ":agent_no"), 
		(agent_get_troop_id, ":troop_no", ":agent_no"),
		(store_troop_faction, ":faction_no", ":troop_no",),
		#(this_or_next|faction_slot_eq,":faction_no",slot_faction_marshall,":troop_no"),
		(faction_slot_eq,":faction_no",slot_faction_leader,":troop_no"),
		(assign, "$agent_king", ":agent_no")]),
 	(0, 0.5, 0, [ # push putton: go down
		(gt, "$agent_king", -1),
        (game_key_clicked, gk_jump), 
		# (key_clicked, key_b),   # overrides jump key
	    (get_player_agent_no, reg10),
		(agent_get_horse, reg15, reg10), (eq, reg15, -1), # cancel if player mounted
		(agent_get_position, pos1, "$agent_king"),
		# see if facing the lord...
		(agent_get_position, pos2, reg10),
		(position_rotate_z,pos2,180-45),(position_is_behind_position, pos1, pos2),
		(position_rotate_z,pos2,90),(position_is_behind_position, pos1, pos2),
		# see if same height..
		(position_get_z,reg20,pos2),
		(position_get_z,reg21,pos1),
		(val_sub,reg20,reg21),(val_abs,reg20),(le,reg20,200.0),
		#(agent_set_scripted_destination, reg10, pos1, 1), # hopefully, turn toward lord
	    (get_player_agent_no, reg10),(agent_set_animation, reg10, "anim_bow_to_lord_go_down"),
		(assign, "$player_is_bowing", 1),
		],[ 
		# after 1 sec, play sound
		(game_key_is_down, gk_jump),
		(get_player_agent_no, reg10),
		(agent_play_sound, reg10, "snd_footstep_wood")]),
	(0, 0, 0, [],[ # release: get up
	    (neq, "$player_is_bowing", 0),
		(neg|game_key_is_down, gk_jump), # (key_is_down, key_b),  
		(get_player_agent_no, reg10),(agent_set_animation, reg10, "anim_bow_to_lord_get_up"),
		(assign, "$player_is_bowing", 0)]),
	(0.0, 1.0, 1.0, [(eq, "$player_is_bowing", 1)],[ # keep pressed: stay down
		# (key_is_down, key_b),  
		(game_key_is_down, gk_jump),
		(get_player_agent_no, reg10),(agent_set_animation, reg10, "anim_bow_to_lord_stay_down")]),
]
custom_tld_bow_always = [
	# push putton: go down
	(0, 0.5, 0, [ 
        (game_key_clicked, gk_jump), 
		# (key_clicked, key_b),   # overrides jump key
	    (get_player_agent_no, reg10),
		(agent_get_horse, reg15, reg10), (eq, reg15, -1), # cancel if player mounted

	    (get_player_agent_no, reg10),(agent_set_animation, reg10, "anim_bow_to_lord_go_down"),
		(assign, "$player_is_bowing", 1),
	],[ 
		# after 1 sec, play sound
		(game_key_is_down, gk_jump),
		(get_player_agent_no, reg10),
		(agent_play_sound, reg10, "snd_footstep_wood")
	]),
	# release: get up
	(0, 0, 0, [],[
	    (neq, "$player_is_bowing", 0 ),
		(neg|game_key_is_down, gk_jump), # (key_is_down, key_b),  
		(get_player_agent_no, reg10),(agent_set_animation, reg10, "anim_bow_to_lord_get_up"),
		(assign, "$player_is_bowing", 0 ),
	]),
	# keep pressed: stay down
	(0.0, 1.0, 1.0, [ (eq, "$player_is_bowing", 1)],[ 
		# (key_is_down, key_b),  
		(game_key_is_down, gk_jump),
		(get_player_agent_no, reg10),(agent_set_animation, reg10, "anim_bow_to_lord_stay_down"),
	]),
]
	  
custom_tld_init_battle = (ti_before_mission_start,0,0,[],
  [ (assign,"$trolls_in_battle",0),	
	(assign,"$nazgul_in_battle",0),	
	(assign,"$wargs_in_battle",0), (eq, "$wargs_in_battle", 0), #MV: to get rid of build warnings - remove on use
	(assign,"$animal_is_present",0), #Init Animals - Kham
	(assign,"$warg_to_be_replaced",-1),	#  this warg needs replacing
	(assign,"$nazgul_team", -1), # will be found when needed
	(call_script, "script_check_agent_armor"), # check for berserker trait
	#(set_rain, 0,100), #switch off vanilla rain and snow

	# CC: Maybe we could add a chance that if the player is playing as a mordor orc, a nazgul may come to his aid?

	# CC: Fixed the broken system. It was checking *parties* against *party templates*, plus some other bugs.
	(try_begin),
		(party_get_template_id, ":p_template_1", "$g_encountered_party"),
		(neg|main_party_has_troop, "trp_npc5"), #Glorfindel scares Nazguls away.
		(assign, ":p_template_2", -1),
		(try_begin),
			(gt, "$g_encountered_party_2", 0),
			(party_get_template_id, ":p_template_2", "$g_encountered_party_2"),
		(try_end),
		(this_or_next|eq, ":p_template_1", "pt_mordor_war_party"),
		(eq, ":p_template_2", "pt_mordor_war_party"),
		(store_random_in_range,":die_roll",0,101),
		(try_begin),
			(gt, ":die_roll", 95),
			(assign,"$nazgul_in_battle",3),	
			(display_log_message, "@Three Nazgul are circling in the sky above the battlefield!"),
		(else_try),
			(gt, ":die_roll", 70),
			(assign,"$nazgul_in_battle",2),	
			(display_log_message, "@Two Nazgul are circling in the sky above the battlefield!"),
		(else_try),
			(gt, ":die_roll", 55),
			(assign,"$nazgul_in_battle",1),	
			(display_log_message, "@A Nazgul is circling in the sky above the battlefield!"),
		(try_end),
	(try_end),
	
	(try_for_range, ":npc",companions_begin,companions_end), #reset KO tracking for companions
		(troop_set_slot,":npc",slot_companion_agent_id,0),
		(troop_set_slot,":npc",slot_troop_wounded,0),
	(try_end),
	(try_for_range, ":npc",new_companions_begin,new_companions_end), #reset KO tracking for companions
		(troop_set_slot,":npc",slot_companion_agent_id,0),
		(troop_set_slot,":npc",slot_troop_wounded,0),
	(try_end),

	# Night Troop message
	(try_begin),
		(is_currently_night),
		(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
	    (assign, ":yes",0),
	    (try_for_range, ":stack", 0, ":num_stacks"),
	    	(eq, ":yes", 0),
			(party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack"),
			(this_or_next|eq, ":troop_id", "trp_a5_dun_night_wolf"),
			(this_or_next|eq, ":troop_id", "trp_i5_woodmen_night_guard"),
			(this_or_next|eq, ":troop_id", "trp_a5_woodmen_night_stalker"),
			(this_or_next|eq, ":troop_id", "trp_i5_corsair_night_raider"),
			(this_or_next|eq, ":troop_id", "trp_a5_corsair_master_assassin"),			
			(this_or_next|eq, ":troop_id", "trp_i5_far_harad_panther_guard"),
			(this_or_next|eq, ":troop_id", "trp_i6_frealaf_raider"),
			(			  eq, ":troop_id", "trp_a5_blackroot_shadow_hunter"),
			(assign, ":yes",1),
			(display_message, "@Some of your human troops are not daunted by the darkness.(Night Troops are not affected by night time penalties)", color_neutral_news),
		(try_end),
	(try_end),

	(try_begin), # Player has berserker trait?
      (troop_slot_eq, "trp_traits", slot_trait_berserker, 1),
      (troop_get_inventory_slot, ":armor", "trp_player", ek_body),
	  (this_or_next|eq, ":armor", -1),
      (item_slot_eq, ":armor", slot_item_light_armor, 1),
      (display_message, "@You are filled with just rage as you set your eyes upon the enemy (Berserk active).", color_neutral_news),
    (try_end),
])

# cheer instead of jump on space if battle is won  (mtarini)
tld_cheer_on_space_when_battle_over_press = (0,1.5,0,[
    (game_key_clicked, gk_jump),
    (all_enemies_defeated, 2),
    (get_player_agent_no, reg10),
    (agent_is_alive, reg10),
    (call_script, "script_cf_bear_form_selected"), (neq, reg0, 1), # Arsakes not in bear form
    (try_begin),(agent_get_horse, reg12, reg10),(ge, reg12, 0), 
            (agent_set_animation, reg10, "anim_cheer_player_ride"),
            (agent_set_animation, reg12, "anim_horse_cancel_ani"), # to remove horse jump
    (else_try),
            (agent_set_animation, reg10, "anim_cheer_player"),
    (try_end),
    (agent_get_troop_id, reg11, reg10),
    (try_begin), 
            (eq,"$player_cheering",0), # don't reshout if just shouted
            (call_script, "script_troop_get_cheer_sound", reg11),
            (gt, reg1, -1), #MV fix
            (agent_play_sound, reg10, reg1),    
    (try_end),
    (assign,"$player_cheering",1),
    ],[
        (assign,"$player_cheering",2), # after 1 sec, can end ani
])
tld_cheer_on_space_when_battle_over_release = (0,0,0,[(eq,"$player_cheering",2),(neg|game_key_is_down, gk_jump)],[
        (call_script, "script_cf_bear_form_selected"), (neq, reg0, 1), # Arsakes not in bear form

	(get_player_agent_no, reg10),
	(agent_get_horse, reg12, reg10),
	(try_begin),(ge, reg12, 0),(agent_set_animation, reg10, "anim_cancel_ani_ride"),
	 (else_try),               (agent_set_animation, reg10, "anim_cancel_ani_stand"),
	(try_end),
	(assign,"$player_cheering",0),
])

# custom TLD functions for special troops spawning
custom_tld_spawn_troop = (ti_on_agent_spawn, 0, 0, [],
[
  (store_trigger_param_1, ":agent"),
  
  (agent_get_troop_id, ":agent_trp",       ":agent"),
  (agent_get_item_id,  ":agent_mount_itm", ":agent"),
  
  (try_begin), # when trolls in battle
    (troop_get_type, ":agent_trp_type", ":agent_trp"),
    (eq,             ":agent_trp_type", tf_troll),
    #--
    (agent_set_speed_limit, ":agent", 4), # trolls go 4 km/h max <GA>
    (assign, "$trolls_in_battle", 1),     # condition on future troll triggers
    
    # a failed test: set custom troll walking/standing animations... why wouldn't this work?
    #(agent_set_walk_forward_animation,":troll","anim_walk_forward_troll"),
    #(agent_set_stand_animation,":troll","anim_walk_forward_troll"),
  (try_end),
  
  (try_begin), # when wargs in battle
    (is_between, ":agent_mount_itm", item_warg_begin, item_warg_end),
    #--
    (val_add, "$wargs_in_battle", 1), # keep warg count up to date...
    (agent_set_slot, ":agent", slot_agent_mount_dead, 0),
    
    #(try_begin),
    #  (is_mbse_active),
    #  (display_message, "@MBSE working, warg spawning"),
    #  (agent_set_sound, ":agent", sound_horse_walk, "snd_warg_lone_woof"),
    #  (agent_set_sound, ":agent", sound_trot, "snd_evil_orders"),
    #  (agent_set_sound, ":agent", sound_canter, "snd_warg_lone_woof"),
    #  (agent_set_sound, ":agent", sound_gallop, "snd_warg_lone_woof"),
    #  (agent_set_sound, ":agent", sound_snort, "snd_warg_lone_woof"),
    #  (agent_set_sound, ":agent", sound_hit, "snd_nazgul_skreech_short"),
    #  (agent_set_sound, ":agent", sound_die, "snd_evil_orders"),
    #  (agent_set_sound, ":agent", sound_neigh, "snd_nazgul_skreech_short"),
    #(try_end),
  (try_end),
  
  (try_begin), # for ghost wargs: set it up to replace the unmounted warg
    (is_between, ":agent_trp", warg_ghost_begin, warg_ghost_end),
    (agent_set_slot, ":agent", slot_agent_time_counter, 0),
    (try_begin),
      (neq, "$warg_to_be_replaced", -1),                  # else, if is a spawn of a warg from start...
      (agent_get_position, pos4, "$warg_to_be_replaced"), # set position to match warg to be replaced...
      (agent_set_position, ":agent", pos4),
      
      (try_begin),
        #if is one of the warg mounts
        (neq, ":agent_mount_itm", -1), 
        # first spawn:  MOUNT set hit points
        (store_agent_hit_points,         ":agent_hit_points", "$warg_to_be_replaced", 1),
        (store_div,                      ":agent_hit_points", 3), # nerf riderlass wargs: reduce HP to 1/3
        (agent_set_hit_points, ":agent", ":agent_hit_points", 1),
        
        #(assign, reg12, ":agent_hit_points"),
        #(display_message,"@DEBUG: new wargs has {reg12} hitpoints left"),
        
      (else_try),
        # second spawn: GHOST RIDER set side
        
        #(agent_get_team, reg11, "$warg_to_be_replaced"),
        
        (agent_get_slot, ":agent_mount_side", "$warg_to_be_replaced", slot_agent_mount_side),
        (agent_set_team, ":agent", ":agent_mount_side"), # this was set just above
        
        #(assign, reg12, ":agent_mount_side"),
        #(display_message,"@DEBUG: new wargs team is now: {reg12}, was: {reg11}"),
        
        (agent_set_slot,"$warg_to_be_replaced", slot_agent_mount_dead, 1),
        (call_script, "script_remove_agent", "$warg_to_be_replaced"),			
        (assign, "$warg_to_be_replaced", -1),
      (try_end),
      
    ] + ((not is_a_wb_mt==1) and [
    
    (else_try), # UGLY FIX FOR CARRYOVER WARGS, KILL THOSE SPAWNED AT START. GA
      (agent_set_slot,":agent", slot_agent_mount_dead, 1), #silently
      (call_script, "script_remove_agent", ":agent"),
      
    ] or []) + [
    
    (try_end),
  (else_try), # normal team assignment
  	(try_begin),
	  	(eq, "$player_control_allies",0),
	    (call_script, "script_agent_reassign_team", ":agent"),
	(try_end),
  (try_end),
  
  #(try_begin),
  #  # if we spawned a rider, let's make his mount remember what side it is.
  #  # GA: and remember that it's alive
  #  (agent_get_horse, ":horse", ":agent"),
  #  (neq, ":horse", -1),
  #  #--
  #  (agent_get_team, ":agent_team", ":agent"),
  #  #swy-- assign the spawned agent's team,
  #  (agent_set_slot, ":horse", slot_agent_mount_side, ":agent_team"),
  #  (agent_set_slot, ":horse", slot_agent_mount_dead, 0),
  #(try_end),
  
  (try_begin),
    #swy-- the engine reverses the order of agent spawns, at least in Warband
    #----- it starts by the biggest ID number and iterates until the smallest one.
    #-----
    #----- because the horse is spawned right after its rider, agent_get_horse doesn't return anything yet at spawn time
    #----- we've to do it the other way around... getting the rider from its mount (by using agent_get_rider) and setting its slots accordingly.
    
    #----- eg: from warband playtesting:
    #-----  Entry points for scene 31 : 1 2 3 4 5 6 7 8 9 10 13 14 15 16 17 18 19 20 21 22 23 24 25 26 39 40 0 11 12 27 28 29 30 31 32 33 34 35 36 37 38 41 42 
    #-----  Total entry points for scene 31 : 43 
    #-----   SWYDEBUG: agent: 63 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 62 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 61 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 60 horse: -1 poss item id: 61 rider: 61
    #-----   SWYDEBUG: agent: 59 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 58 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 57 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 56 horse: -1 poss item id: 62 rider: 57
    #-----   SWYDEBUG: agent: 55 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 54 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 53 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 52 horse: -1 poss item id: 62 rider: 53
    #-----   SWYDEBUG: agent: 51 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 50 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 49 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 48 horse: -1 poss item id: 60 rider: 49
    #-----   SWYDEBUG: agent: 47 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 46 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 45 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 44 horse: -1 poss item id: 61 rider: 45
    #-----   SWYDEBUG: agent: 43 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 42 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 41 horse: -1 poss item id: 61 rider: 42
    #-----   SWYDEBUG: agent: 40 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 39 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 38 horse: -1 poss item id: 62 rider: 39
    #-----   SWYDEBUG: agent: 37 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 36 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 35 horse: -1 poss item id: 60 rider: 36
    #-----   SWYDEBUG: agent: 34 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 33 horse: -1 poss item id: -1 rider: -1
    #-----   SWYDEBUG: agent: 32 horse: -1 poss item id: 61 rider: 33

    #swy-- check if this :agent is a horse/ has a rider
    (agent_get_rider, ":agent_rider", ":agent"),
    (gt,              ":agent_rider", -1),
    #--
    (agent_get_team, ":agent_rider_team", ":agent_rider"),
    (agent_set_slot, ":agent", slot_agent_mount_side, ":agent_rider_team"), #swy-- assign the spawned agent's rider team,
    (agent_set_slot, ":agent", slot_agent_mount_dead, 0),
    #swy-- assign the built-in rider-at-startup to its mount for the lone_wargs mechanic, so that we can
    #   -- check if the orc is still alive but unmounted before attempting to delete + doing a stealthy swap.
    #   -- (take a look here for the reported bug: https://trello.com/c/lbGfx3Od)
    (agent_set_slot, ":agent", slot_agent_mount_orig_rider, ":agent_rider"),
  (try_end),
  
  (try_begin),
    (this_or_next|is_between, ":agent_trp", companions_begin, companions_end), # track companion injuries in battle
    (is_between, ":agent_trp", new_companions_begin, new_companions_end), # track companion injuries in battle

    #--
    (troop_set_slot, ":agent_trp", slot_troop_wounded, 0),
    (troop_set_slot, ":agent_trp", slot_companion_agent_id, ":agent"),
  (try_end),
  (set_show_messages, 1),
])

# mtarini nazgul sweeps. improved by cppcoder.
nazgul_sweeps = (4,1.2,5,[
	#(this_or_next|key_is_down, key_n),
	(gt,"$nazgul_in_battle",0),
	(store_random_in_range,reg0,0,100),
	#(this_or_next|key_is_down, key_n),
	#(le,reg0,"$nazgul_in_battle"), 
	(store_mul, reg1, "$nazgul_in_battle", 5), # 5% chance every 2 seconds, for each nazgul present
	(le,reg0,reg1),	
	(display_log_message, "@Nazgul sweep!"),
	# if nazgul team is not computed, compute it
	(try_begin),
		(eq, "$nazgul_team", -1), 
		(try_for_agents,":agent"),
			(eq, "$nazgul_team", -1),
			(agent_get_party_id, ":party_id", ":agent"),
			(ge, ":party_id", 0),
			(party_get_template_id, ":party_template", ":party_id"),
			(eq, ":party_template", "pt_mordor_war_party"),
			(agent_get_team, "$nazgul_team",":agent"),
		(try_end),
	(try_end),
	#(assign, reg0, "$nazgul_team"),
	#(display_message, "@Nazgul Team = {reg0}"),
	(store_random_in_range, ":long_skretch", 0,2),
	# play sound
	(get_player_agent_no, ":player_agent"), #for messages and sound origin
	(try_begin),
		(ge,":long_skretch",1),
		(agent_play_sound, ":player_agent", "snd_nazgul_skreech_long" ),
		#(display_log_message, "@Debug: LONG sweep!"),
	(else_try),
		(agent_play_sound, ":player_agent", "snd_nazgul_skreech_short"),
		#(display_log_message, "@Debug: SHORT sweep!"),
	(try_end), 

	(try_for_agents,":victim"), # psycological effect:
		(agent_is_alive,":victim"),
		(agent_get_team, reg1, ":victim"),
		(this_or_next|eq, "$nazgul_team", -1),
		(teams_are_enemies, reg1, "$nazgul_team"),
		(agent_is_human,":victim"),
		(try_begin), # long skretch can make the horse rage twice (but only 66% of times)
			(assign, ":horse_rage_twice",":long_skretch"),
			(store_random_in_range,":die_roll",1,4),
			(eq,":die_roll",1),		
		(try_end), 

		(agent_get_troop_id, ":trp_victim", ":victim"),
		(agent_get_horse,":horse",":victim"),
		(store_attribute_level, ":int", ":trp_victim", ca_intelligence),
		(store_skill_level, ":riding", "skl_riding", ":trp_victim"),
		(store_random_in_range,":die_roll_int",1,26),

		(try_begin), 		# the horses could rear
			(ge,":horse",0), # there's an horse being riden
                        # Arsakes: exclude animals (which have hidden riders so their "mounts" don't escape)
                        (neg|is_between, ":trp_victim", warg_ghost_begin, warg_ghost_end),
                        (neg|is_between, ":trp_victim", "trp_spider", "trp_dorwinion_sack"),
                        (neq, ":trp_victim", "trp_multiplayer_profile_troop_male"), (neq, ":trp_victim", "trp_werewolf"),

			(try_begin), 
				# if rider failed intelligece test: both horse and rider panic
				(ge, ":die_roll_int" , ":int"), 
				(try_begin),
					(ge,":horse_rage_twice",1),
					(agent_set_animation, ":horse", "anim_horse_rear_twice"), 
				(else_try), 
					(agent_set_animation, ":horse", "anim_horse_rear_fast_blend"), 
				(try_end),
        
				(try_begin), #always let the player know what affects him
					(eq, ":player_agent", ":victim"),
					(display_log_message, "@You and your horse panic, the Nazgul cries are unbearable!"),
				(try_end), 
			(else_try), 
				# if rider success on intelligence test: he won't panic, horse could
				(store_random_in_range,":die_roll_riding",1,13),
				(ge, ":die_roll_riding" , ":riding"), # riding test: horse is a victim if 1d12 rolls over riding skill
				(agent_set_animation, ":horse", "anim_horse_rear"),
				#(agent_play_sound,":horse","snd_neigh"),
        
				(try_begin), #always let the player know what affects him
					(eq, ":player_agent", ":victim"),
					(display_log_message, "@Your horse panics, the Nazgul cries are unbearable!"),
				(try_end), 
			# (else_try), 
				# (assign, ":horse_resisted", 1),
			(try_end), 
		(try_end), 
		
		(try_begin), # the guys can go nuts
			(ge, ":die_roll_int" , ":int"), # it is a victim if 1d25 rolled under intelligence	  
			(try_begin), 
				# mounted characters panic
				(ge,":horse",0), 
				(try_begin),
					(ge,":horse_rage_twice",1),
					(agent_set_animation, ":victim", "anim_nazgul_noooo_mounted_long"), 
				(else_try), 
					(agent_set_animation, ":victim", "anim_nazgul_noooo_mounted_short"),
				(try_end), 
			(else_try), 
				# unmounted characters panic
				(try_begin),
					(ge,":long_skretch",1),
					(agent_set_animation, ":victim", "anim_nazgul_noooo_long"),
				(else_try), 
					(agent_set_animation, ":victim", "anim_nazgul_noooo_short"),
				(try_end), 
			(try_end),
      
			(try_begin), #always let the player know what affects him
				(eq, ":player_agent", ":victim"),
				(display_log_message, "@You cower in terror, the Nazgul cries are unbearable!"),
			(try_end),
      
		(try_end), 
		# show message?
        # MV: commented out - resistance not important, it's the other way around, effects are important
		# (get_player_agent_no, ":player_agent"),
		# (eq,":player_agent", ":victim"),
		# (eq,":human_resisted", 1),
		# (display_log_message,"@Panic resisted!"),
		# (eq,":horse_resisted", 1),
		# (display_log_message,"@Horse panic avoided!"),
    (try_end),
	(store_random_in_range,":die_roll",1,4),
	(ge,":die_roll",2), # twice in 2 there is will an attack!
  ],[ # physical attack on random agent
	(assign,":random_agent",-1), # he will suffer a physical attack!
	(assign,":random_agent_score",99999),
	(mission_cam_get_position, 2),
	(get_player_agent_no, ":player_agent"),
	(try_for_agents,":victim"),
		(agent_is_alive,":victim"),
		(agent_is_human,":victim"),
		(agent_get_team, reg1, ":victim"),
		(neg|eq, ":victim",":player_agent"),
		
		(this_or_next|eq, "$nazgul_team", -1),
		(teams_are_enemies, reg1, "$nazgul_team"),
			
		(agent_get_position, 1,":victim"),
		(position_is_behind_position, 1,2), # a troop never suffers an attack if visible on the screen
		
		# this one is eligible for physical effect,
		(store_random_in_range,":die_roll",1,10000),
		(ge, ":random_agent_score",":die_roll"),
		(assign, ":random_agent_score", ":die_roll"),
		(assign, ":random_agent", ":victim"),
    (try_end),

	(gt, ":random_agent", -1),
	(agent_get_troop_id, reg1, ":random_agent"),
	(troop_get_type, reg2, reg1),
	# make it scream like a pig
	(try_begin),
		(this_or_next|eq, reg2, tf_troll ),
		(is_between, reg2, tf_orc_begin , tf_orc_end ),
		(agent_play_sound,":random_agent","snd_horror_scream_orc"),
	(else_try),
		(eq, reg1, tf_female ),
		(agent_play_sound,":random_agent","snd_horror_scream_woman"),
	(else_try),
		(agent_play_sound,":random_agent","snd_horror_scream_man"),
	(try_end),
	# get it killed...  (trick! self kill with hidden message... is there a better way?) NO, THERE IS NOT. GA
	(agent_set_hit_points,":random_agent",0,1), # this still doesn't kill it
	(set_show_messages,0),
	#--
	(agent_get_kill_count, ":killed", ":random_agent"),
	(agent_deliver_damage_to_agent,":random_agent",":random_agent"), 
	(agent_get_kill_count, ":killed_1", ":random_agent"),
	#--
	(set_show_messages,1),
	
	# display kill in a log message of appropriate color
	# changed 0xFFAAFFAA to color_good_news -CC
	(assign, ":text_color", color_good_news),
	(try_begin),
		(agent_is_ally, ":random_agent"),
		# changed 0xFFFFAAAA to color_bad_news -CC
		(assign, ":text_color", color_bad_news),
	(try_end),
	(str_store_string, s10, "@knocked unconscious"),	
	(try_begin),
		(gt, ":killed_1", ":killed"),
		(str_store_string, s10, "@killed"),
	(try_end),
	(str_store_agent_name, s11, ":random_agent"),
	(display_log_message, "@Nazgul diving attack on {s11}!"),
	(display_log_message, "@{s11} is {s10} in the Nazgul attack!",":text_color"),
])

# if player attempts to ride non matching mount, mount rebels (mtarini)
tld_player_cant_ride = (1.90,1.5,0.5,[

	(eq, "$tld_option_crossdressing", 0),
	(get_player_agent_no, "$current_player_agent"),

	] + ( is_a_wb_mt==1 and [
	(agent_is_active, "$current_player_agent"),
	] or []) + [
	(agent_get_horse,":mount","$current_player_agent"),
	(ge, ":mount", 0),
	] + ( is_a_wb_mt==1 and [
	(agent_is_active, ":mount"),
	] or []) + [

	(agent_get_item_id,":mount_item", ":mount"),
        (neq, ":mount_item", "itm_bear"), # Arsakes: exclude bears
	
	(try_begin), # lame horses can stall
		(eq, "$horse_mod", imod_lame),
		(eq, ":mount","$horse_player"),
		
		] + ( is_a_wb_mt==1 and [
		
		#swy-- reduced constant nagging, fire randomly just when the horse goes fast, this isn't even even fun or challenging!
		(agent_get_speed, pos1, ":mount"), # speed in m/s for both X and Y
    
		(position_get_x, ":mount_speed_x", pos1), # after some testing the game seems to use just the Y slot 
		(position_get_y, ":mount_speed_y", pos1), # of the position for speed, which is multiplied x10.
		
		#swy-- debug, see how the real speed is measured
	#	(assign, reg1, ":mount_speed_x"), # empty, always zero?
	#	(assign, reg2, ":mount_speed_y"), # actual speed counter...
		
	#	(display_message, "@going at {reg1}/{reg2} m/s x10"),
		
		(this_or_next|ge,":mount_speed_x", 590), # if the horse is lame and goes faster than 59 m/s (normal calloping speed is over ~60 m/s)
		(             ge,":mount_speed_y", 590), # there's a 95% chance of stalling every 2 secs.

		] or []) + [

		(store_random_in_range, ":rand_stall_horse", 0, 100),
		(ge, ":rand_stall_horse", 5),
		
		(agent_set_animation, ":mount", "anim_horse_cancel_ani"), 
		(display_message, "@Your mount stumbles! It seems to be lame.",color_bad_news),
	(try_end),
	
	(store_random_in_range, ":rand",0,100),(ge, ":rand", 20), # 20% of times...
	
	(call_script, "script_cf_troop_cant_ride_item", "$g_player_troop", ":mount_item"), 
		
	],[
	(get_player_agent_no, ":player"),
	] + ( is_a_wb_mt==1 and [
	(agent_is_active, ":player"),
	] or []) + [
	(agent_get_horse,":mount",":player"),
	(ge, ":mount", 0),
	] + ( is_a_wb_mt==1 and [
	(agent_is_active, ":mount"),
	] or []) + [
	(agent_get_item_id,":mount_item", ":mount"),
	(try_begin), # wargs rear and byte
		(is_between, ":mount_item", item_warg_begin, item_warg_end),
		(agent_set_animation, ":mount", "anim_horse_rear"),
		(agent_deliver_damage_to_agent, ":mount", ":player"), 
		(display_message, "@Bitten by your own warg mount!",color_bad_news),
		(agent_play_sound, ":mount", "snd_warg_lone_woof"),
	(else_try), # ponies stops
		(eq, ":mount_item", "itm_pony"),
		(agent_set_animation, ":mount", "anim_horse_cancel_ani"), 
		(display_message, "@You weigh too much for a pony!",color_bad_news),
		(agent_play_sound, ":mount", "snd_neigh"),
	(else_try), # other mount, rear
		(agent_set_animation, ":mount", "anim_horse_rear"), 
		(display_message, "@Your mount rears, refusing to obey your commands!",color_bad_news),
		(agent_play_sound, ":mount", "snd_neigh"),
	(try_end),
])


#Kham - Custom Troll MT

custom_troll_hitting_new = ((is_a_wb_mt==1) and [
 (ti_on_agent_spawn, 0, ti_once, [

	(store_trigger_param_1, ":troll"),

	(agent_is_active, ":troll"),
	(agent_is_human, ":troll"),
	(gt, ":troll", 0),

	(agent_get_troop_id, ":troop_id", ":troll"),
	(troop_get_type, ":type", ":troop_id"),
	(eq, ":type", tf_troll),

	],[

	(store_trigger_param_1, ":troll"),

	(agent_is_active, ":troll"),
	(agent_is_human, ":troll"),
	(gt, ":troll", 0),

	(agent_get_troop_id, ":troop_id", ":troll"),
	(troop_get_type, ":type", ":troop_id"),
	(eq, ":type", tf_troll),

	(agent_set_speed_modifier, ":troll", 100),
	#(agent_set_max_hit_points, ":troll", 35),
	(agent_ai_set_aggressiveness, ":troll", 500),

 ]),

(1,0,ti_once, [(gt, "$trolls_in_battle", 0)], [
	
	(try_for_agents,":troll"),
		(agent_is_alive,":troll"),
		(agent_is_human,":troll"),
		(agent_is_active, ":troll"),
		(agent_get_troop_id,":troll_troop_id",":troll"), # is it a troll?
		(troop_get_type, ":troll_type", ":troll_troop_id"),
		(eq, ":troll_type", tf_troll),

		(agent_ai_get_num_cached_enemies, ":num_nearby_agents", ":troll"),
        (gt, ":num_nearby_agents", 0),
        #Trolls charging - begin

        #(agent_get_team, ":troll_team", ":troll"),
        (agent_get_position, pos67, ":troll"),

        #get the closest noncav enemy
        (assign, ":min_dist", 1000000),
        (try_for_range, ":nearby_agent_no", 0, ":num_nearby_agents"),
        	(agent_ai_get_cached_enemy, ":enemy_agent", ":troll", ":nearby_agent_no"),
            (agent_is_alive, ":enemy_agent"),
            (agent_is_human, ":enemy_agent"),
            (agent_is_active, ":enemy_agent"),
            (agent_get_class, ":enemy_class_no", ":enemy_agent"),
            (neq, ":enemy_class_no", grc_cavalry),
            (agent_get_position, pos68, ":enemy_agent"),
            (get_distance_between_positions, ":dist", pos68, pos67),
            (gt, ":min_dist", ":dist"),
            (assign, ":min_dist", ":dist"),
            (copy_position, pos69, pos68), #pos69 holds the nearest enemy position
        (try_end),
    
      # (assign, reg0, ":min_dist"),
      # (assign, reg1, ":troll"),
      # (display_message, "@Debug: Troll {reg1} distance to enemy: {reg0}."),
        
        (try_begin),
          (this_or_next|eq, ":min_dist", 1000000),
          (lt, ":min_dist", 500),
          (agent_clear_scripted_mode, ":troll"), # leave the troll on its own if close enough to the enemy
        (else_try),
          (agent_set_scripted_destination, ":troll", pos69, 1), # head for the nearest enemy
        (try_end),
        #Trolls charging - end
    (try_end),
  ]),

(ti_on_agent_hit, 0, 0, [
	
    # trigger param 1 = damage inflicted agent_id
    # trigger param 2 = attacker agent_id
    # trigger param 3 = inflicted damage
    # trigger param 4 = hit bone
    # trigger param 5 = item_id of missile used to attack (if attack was with a ranged weapon)
    # reg0            = weapon item_id
    # pos0            = position of the hit area, rotation fields contain the direction of the blow
    # If (set_trigger_result) is used in the code with operation parameter equal or greater than zero, it will override the inflicted damage.


 	(store_trigger_param_2, ":dealer"),

 	(agent_is_active, ":dealer"),
 	(agent_is_alive, ":dealer"),
 	(gt, ":dealer", 0),
 	(agent_get_troop_id, ":troll_dealer", ":dealer"),
 	(troop_get_type, ":type_dealer", ":troll_dealer"),
 	(eq, ":type_dealer", tf_troll),
	(neq, reg0, "itm_troll_aoe"),
 	
	],[

	(store_trigger_param_1, ":receiver"),
 	(store_trigger_param_2, ":dealer"),
 	(store_trigger_param_3, ":damage"),
	(assign, ":weapon", reg0),
    (gt, ":weapon", 0),
	#(assign, ":hit_pos", pos0),
	#(str_store_item_name, s1, reg0),
	#(display_message, "@weapon: {s1}"),
	#(display_debug_message, "@weapon: {s1}"),

 	(agent_is_active, ":receiver"),
 	(agent_is_alive, ":receiver"),
 	(gt, ":receiver", 0),
 	
 	(agent_is_active, ":dealer"),
 	(agent_is_alive, ":dealer"),
 	(gt, ":dealer", 0),
 	(agent_get_troop_id, ":troll_dealer", ":dealer"),
 	(troop_get_type, ":type_dealer", ":troll_dealer"),
 	(eq, ":type_dealer", tf_troll),

    (agent_get_position, pos3, ":receiver"), #throwback + aoe around the receiver, to have it somewhat directional
    (set_fixed_point_multiplier, 100),
	(item_get_horse_speed, ":aoe", ":weapon"),

    (try_for_agents, ":aoe_hit", pos3, ":aoe"),
      (agent_is_active, ":aoe_hit"),
      (agent_is_alive, ":aoe_hit"),
      (agent_is_human, ":aoe_hit"),
      (neq, ":aoe_hit", ":dealer"), #don't hit yourself
	  (gt, ":aoe_hit", 0),				  
      #(agent_get_position, pos17, ":aoe_hit"),
      #(neg|position_is_behind_position, pos17, pos18),
      (agent_get_troop_id, ":victim_troop_id", ":aoe_hit"),
      (neg|is_between, ":victim_troop_id", warg_ghost_begin, warg_ghost_end),
      (neg|is_between, ":victim_troop_id", "trp_spider", "trp_dorwinion_sack"),
      (neq, ":victim_troop_id", "trp_werewolf"),
      (troop_get_type, ":victim_type", ":victim_troop_id"),
      (agent_get_horse, ":victim_horse", ":aoe_hit"),
      
      (store_random_in_range, ":flyback_anim", 0, 3),
      # then, set animation
      
      (neq, ":victim_type", tf_troll), #no flyback for trolls
      (agent_get_animation, ":current_anim", ":aoe_hit"),
      (this_or_next|neq, ":current_anim", "anim_strike_fall_back_rise"),
      (neq, ":current_anim", "anim_strike_fly_back_rise"),

      (assign, ":continue_ko", 0), 

	  (store_mission_timer_a, ":timer"),
	  (try_begin),
		(agent_slot_eq, ":aoe_hit", slot_agent_knocked_down, 0),
		(assign, ":continue_ko", 1),
		(agent_set_slot, ":aoe_hit", slot_agent_knocked_down, 1),
		(val_add, ":timer", 6), #4 seconds after Knock Down #InVain: Slightly increased to avoid stunlocking by multiple trolls
		(agent_set_slot, ":aoe_hit", slot_agent_last_knockdown_time, ":timer"),
	  (try_end),
      
      (eq, ":continue_ko", 1),

		(try_begin),
		  # human (non trolls, non horse) victims
			(try_begin),
			  (eq, ":flyback_anim", 0),
		  # troll is in front of victim
			  (agent_set_animation, ":aoe_hit", "anim_strike_fly_back_rise_from_left"), # send them flying back
			(else_try),
			  (eq, ":flyback_anim", 1),
			  (agent_set_animation, ":aoe_hit", "anim_strike_fly_back_rise"), # send them flying back
			(else_try),
			  (agent_set_animation, ":aoe_hit", "anim_strike_fly_back_near_rise"),
			(try_end),

			(store_random_in_range, ":rand_sound", 0, 6),
			(try_begin),
				(eq, ":rand_sound", 0),
				(agent_play_sound, ":aoe_hit", "snd_wooden_hit_low_armor_low_damage"),
			  (else_try),
				(eq, ":rand_sound", 1),
				(agent_play_sound, ":aoe_hit", "snd_wooden_hit_low_armor_high_damage"),
			  (else_try),
				(eq, ":rand_sound", 2),
				(agent_play_sound, ":aoe_hit", "snd_wooden_hit_high_armor_low_damage"),
			  (else_try),
				(eq, ":rand_sound", 3),
				(agent_play_sound, ":aoe_hit", "snd_wooden_hit_high_armor_low_damage"),
			  (else_try),
				(eq, ":rand_sound", 4),
				(agent_play_sound, ":aoe_hit", "snd_wooden_hit_high_armor_high_damage"),
			  (else_try),
				(agent_play_sound, ":aoe_hit", "snd_blunt_hit"),
			(try_end),

			(try_begin),
			  (gt, ":victim_horse", 1),
			  (agent_start_running_away, ":victim_horse"),
			  (agent_stop_running_away, ":victim_horse"),
			(try_end),
		(try_end),
	  
	  (try_begin),
			(neq, ":aoe_hit", ":receiver"),
			(agent_deliver_damage_to_agent, ":dealer", ":aoe_hit", -1, "itm_troll_aoe"),
			#(agent_deliver_damage_to_agent_advanced, ":aoe_damage", ":dealer", ":aoe_hit", -1, "itm_troll_aoe"),
 # 			(agent_deliver_damage_to_agent_advanced, <destination>, <attacker_agent_id>, <agent_id>, <value>, [weapon_item_id]),
			#(assign, reg6, ":aoe_damage"),
			#(display_message, "@aoe hit damage: {reg6}"),
			#(display_debug_message, "@aoe hit damage: {reg6}"),
	  (try_end),

    (try_end),
	
	(get_player_agent_no, ":player"),
	(eq, ":receiver", ":player"),
	#(display_message, "@player {s5} hit"),
	(val_div, ":damage", 2),
	(set_trigger_result, ":damage"),

]),

# Surrounded Pushback - Step 1

(5, 5, 7, [(gt, "$trolls_in_battle", 0)], 
	[
	
 	(try_for_agents, ":troll"),
		(agent_is_active, ":troll"),
		(agent_is_alive, ":troll"),
		(agent_is_human, ":troll"),
		(gt, ":troll", 0),
		(agent_get_troop_id, ":troll_troop_id", ":troll"),
		(troop_get_type, ":troll_type", ":troll_troop_id"),
		(eq, ":troll_type", tf_troll),
		(store_mission_timer_a_msec, ":timer"), 
		(agent_get_slot, ":cooldown", ":troll", slot_agent_troll_swing_move), #pushback cooldown slot set after troll (re-)spawn
		(ge, ":timer", ":cooldown"),
		(call_script, "script_cf_surrounded_pushback", ":troll", 1),
		#(display_message, "@pushback step 1"),
	(try_end),

	]),

# Surrounded Pushback - Step 2

(0.1, 0, 0.5, [
	(gt, "$trolls_in_battle", 0),
	(assign, ":troll_found", 0),
 	(try_for_agents, ":troll"),
		(agent_is_active, ":troll"),
		(agent_is_alive, ":troll"),
		(agent_is_human, ":troll"),
		(gt, ":troll", 0),
		(eq, ":troll_found", 0),
		(agent_get_troop_id, ":troll_troop_id", ":troll"),
		(troop_get_type, ":troll_type", ":troll_troop_id"),
		(eq, ":troll_type", tf_troll),
		(agent_slot_eq, ":troll", slot_agent_troll_swing_status, 1),
		(store_mission_timer_a_msec, ":timer_2"),
		(agent_get_slot, ":hit_timer", ":troll", slot_agent_troll_swing_move),
		(ge, ":timer_2", ":hit_timer"),
		(assign, ":troll_found", 1),
	(try_end),

	(eq, ":troll_found", 1),

	],[
 	(try_for_agents, ":troll"),
		(agent_is_active, ":troll"),
		(agent_is_alive, ":troll"),
		(agent_is_human, ":troll"),
		(gt, ":troll", 0),
		(agent_get_troop_id, ":troll_troop_id", ":troll"),
		(troop_get_type, ":troll_type", ":troll_troop_id"),
		(eq, ":troll_type", tf_troll),
		(agent_slot_eq, ":troll", slot_agent_troll_swing_status, 1),
		(call_script, "script_cf_surrounded_pushback", ":troll", 2),
		#(display_message, "@pushback step 2"),
	(try_end),

	]),

# End Surrounded Pushback

# Troll Charge
(10, 0, 5, [
	

 	(gt, "$trolls_in_battle", 0),

	],[

	(assign, ":troll_charging", 0), 

 	(try_for_agents, ":troll"), #Find trolls, apply cooldown timers
		(agent_is_active, ":troll"),
 		(agent_is_alive, ":troll"),
 		(agent_is_human, ":troll"),
 		(gt, ":troll", 0),
 		(agent_get_troop_id, ":troll_troop_id", ":troll"),
		(troop_get_type, ":troll_type", ":troll_troop_id"),
		(eq, ":troll_type", tf_troll),
		(agent_get_slot, ":last_charge", ":troll", slot_troll_agent_last_charge),
	 	(store_mission_timer_a, ":time"),
		(ge, ":time", 45), #Initial cooldown (InVain)
	 	(try_begin),
	 		(eq, ":last_charge", 0),
	 		(assign, ":cooldown", 0), # @kham: Initial cooldown could probably also be applied here? 
	 	(else_try),
	 		(assign, ":cooldown", 30),
	 	(try_end),

		(lt, ":troll_charging", 1), #First troll found? Block try_for_agents loop here
	 	(val_add, ":troll_charging",1),
 		
 		(agent_slot_eq, ":troll", slot_troll_agent_charging, 0),
		(val_add, ":last_charge", ":cooldown"),
		(gt, ":time", ":last_charge"), #check cooldown timer ( @kham: Why is it done _after_ the loop block?)
		#(display_message, "@troll charge found troll"),
	 	(agent_set_speed_modifier, ":troll", 500), #make him sprint
	 	(agent_set_slot, ":troll", slot_troll_agent_charging, 1),
	 	(store_mission_timer_a, ":time"),
	 	(agent_set_slot, ":troll", slot_troll_agent_last_charge, ":time"),

	 	(agent_get_position, pos15, ":troll"),

        (try_for_agents, ":nearby_agent_no", pos15, 450), #Find nearby agents, assign flyback animation and sound, riderless horses run away
			#(display_message, "@troll charge initial pushback"),
	 		(agent_is_active, ":nearby_agent_no"),
	 		(agent_is_alive, ":nearby_agent_no"),
	 		(agent_is_human, ":nearby_agent_no"),
	 		(gt, ":nearby_agent_no", 0),
	 		(neq, ":nearby_agent_no", ":troll"), #don't hit yourself
	 		
	 		(agent_get_position, pos16,":nearby_agent_no"), # @kham: What's this, why the double check with different distances?
			(get_distance_between_positions,":dist",pos15,pos16),
			(le, ":dist", 400),

			(agent_get_troop_id, ":victim_troop_id", ":nearby_agent_no"),
			(troop_get_type, ":victim_type", ":victim_troop_id"),
			(agent_get_horse, ":victim_horse", ":nearby_agent_no"),
			(neq, ":victim_type", tf_troll), #no plowthrough for trolls
	      	(neg|is_between, ":victim_troop_id", warg_ghost_begin, warg_ghost_end),
	      	(neg|is_between, ":victim_troop_id", "trp_spider", "trp_dorwinion_sack"),
	      	(neq, ":victim_troop_id", "trp_werewolf"),

			
			(agent_get_animation, ":cur_anim", ":nearby_agent_no"),
			(this_or_next|neq, ":cur_anim", "anim_strike_fall_back_rise"),
			(neq, ":cur_anim", "anim_strike_fly_back_rise"),

			
			(store_random_in_range, ":flyback_anim", 0, 2),
			# then, set animation
			# human (non trolls, non horse) victims
			(try_begin),
				(eq, ":flyback_anim", 0),
		# troll is in front of victim
				(agent_set_animation, ":nearby_agent_no", "anim_strike_fall_back_rise"), # send them flying back
			(else_try),
				(agent_set_animation, ":nearby_agent_no", "anim_strike_fly_back_rise"), # send them flying back
			(try_end),
			
			(store_random_in_range, ":rand_sound", 0, 150),
			(try_begin),
				(is_between, ":rand_sound", 0, 10),
				(agent_play_sound, ":nearby_agent_no", "snd_wooden_hit_low_armor_low_damage"),
			(else_try),
				(is_between, ":rand_sound", 10, 20),
				(agent_play_sound, ":nearby_agent_no", "snd_wooden_hit_low_armor_high_damage"),
			(else_try),
				(is_between, ":rand_sound", 20, 30),
				(agent_play_sound, ":nearby_agent_no", "snd_wooden_hit_high_armor_low_damage"),
			(else_try),
				(is_between, ":rand_sound", 30, 40),
				(agent_play_sound, ":nearby_agent_no", "snd_wooden_hit_high_armor_low_damage"),
			(else_try),
				(is_between, ":rand_sound", 50, 60),
				(agent_play_sound, ":nearby_agent_no", "snd_wooden_hit_high_armor_high_damage"),
			(else_try),
				(is_between, ":rand_sound", 60, 70),
				(agent_play_sound, ":nearby_agent_no", "snd_blunt_hit"),
			(try_end),

			(try_begin),
				(gt, ":victim_horse", 1),
				(agent_start_running_away, ":victim_horse"),
				(agent_stop_running_away, ":victim_horse"),
			(try_end),
			(set_fixed_point_multiplier, 1),
			(store_random_in_range,":random_timings",1,5),
			(agent_set_animation_progress, ":nearby_agent_no", ":random_timings"), # differentiate timings a bit
		(try_end),
		
		(agent_play_sound, ":troll", "snd_troll_grunt_long"),
	 	(try_begin), 
			(troop_has_item_equipped,":troll_troop_id","itm_troll_shield_a"),
	 		(agent_refill_wielded_shield_hit_points, ":troll"),
	 		# (agent_unequip_item, ":troll", "itm_troll_shield_a"),
	 		# (agent_equip_item, ":troll", "itm_troll_shield_a"), #Moves shield to back #InVain: let's try another way that preserves item's imod
			(agent_get_wielded_item, ":troll_weapon", ":troll", 0),
			(agent_set_wielded_item, ":troll", -1),
			(agent_set_wielded_item, ":troll", ":troll_weapon"),
	 	(try_end),
		
		(store_random_in_range, ":rand_charge", 0, 100),
		(try_begin),
			(lt, ":rand_charge", 50),
	 		(agent_set_animation, ":troll", "anim_troll_roar", 0),
	 	(else_try),
	 		(agent_set_animation, ":troll", "anim_troll_charge", 0),
	 	(try_end),
	 	#(display_message, "@Troll is Charging!"),
	(try_end),

]),


# Troll Charge Deactivate
(5, 0, 1, [

	(gt, "$trolls_in_battle"), #  @kham: Missing argument? Apparently it works anyway?
	],[

	(try_for_agents, ":troll"),
		(agent_is_alive, ":troll"),
		(agent_is_active, ":troll"),
		(agent_is_human, ":troll"),
		(gt, ":troll", 0),
		(store_mission_timer_a, ":time"),
		(agent_get_slot, ":knocked_down", ":troll", slot_agent_knocked_down),
		(agent_get_slot, ":knocked_down_time", ":troll", slot_agent_last_knockdown_time),

		(try_begin), # @kham: This is actually not only for troll charge deactivation, right? It clears the slot for all previously knocked down agents?
			(eq, ":knocked_down", 1),
			(ge, ":time", ":knocked_down_time"),
			(agent_set_slot, ":troll", slot_agent_knocked_down, 0),
		(try_end),
		
		(agent_get_troop_id,":troll_troop_id",":troll"), # is it a troll?
		(troop_get_type, ":troll_type", ":troll_troop_id"),
		(eq, ":troll_type", tf_troll),
		(agent_slot_eq, ":troll", slot_troll_agent_charging, 1),
		#(display_message, "@troll charge deactivate found charging troll"),
		(agent_get_slot, ":time_last_charge", ":troll", slot_troll_agent_last_charge), # @kham: Check if the charge has lasted for at least 10 seconds?
		(store_mission_timer_a, ":time"),
		(val_add, ":time_last_charge", 10),
		(gt, ":time", ":time_last_charge"),
		(agent_set_slot, ":troll", slot_troll_agent_charging, 0),
		(agent_set_speed_modifier, ":troll", 100),
		(assign, reg65, ":time"),
		(assign, reg66, ":time_last_charge"),
		#(display_message, "@Charge turned off -- Time: {reg65}, Last Charge: {reg66}"),
		(try_begin),
			(agent_get_troop_id, ":troop_id", ":troll"),
			(troop_has_item_equipped,":troop_id","itm_troll_shield_a"),
			# (this_or_next|eq, ":troop_id", "trp_mordor_olog_hai"),
			# (eq, ":troop_id", "trp_isen_armored_troll"),
 			(agent_set_wielded_item, ":troll", "itm_troll_shield_a"),
 			(agent_refill_wielded_shield_hit_points, ":troll"), # @kham: Does this serve any special purpose, or is it just to make troll shields sturdier?
 		(try_end),
	(try_end), 
		
]),

# Troll Charge Mode Pushbacks

(0.2,0.5,2, [(gt, "$trolls_in_battle", 0)],[ # @kham: Rearm timing intended? A charge lasts 10 seconds, so there will be at most 4 pushbacks per charge?

	(try_for_agents,":troll"), # @kham: This is actually the old "Troll doesn't listen to orders" code, right?
		#(display_message, "@troll charge MV"),
		(agent_is_alive,":troll"),
		(agent_is_human,":troll"),
		(agent_is_active, ":troll"),
		(agent_get_troop_id,":troll_troop_id",":troll"), # is it a troll?
		(troop_get_type, ":troll_type", ":troll_troop_id"),
		(eq, ":troll_type", tf_troll),

		(agent_ai_get_num_cached_enemies, ":num_nearby_agents", ":troll"),
        (gt, ":num_nearby_agents", 0),
        #Trolls charging - begin

        #(agent_get_team, ":troll_team", ":troll"),
        (agent_get_position, pos67, ":troll"),

        #get the closest noncav enemy
        (assign, ":min_dist", 1000000),
        (try_for_range, ":nearby_agent_no", 0, ":num_nearby_agents"),
        	(agent_ai_get_cached_enemy, ":enemy_agent", ":troll", ":nearby_agent_no"),
            (agent_is_alive, ":enemy_agent"),
            (agent_is_human, ":enemy_agent"),
            (agent_is_active, ":enemy_agent"),
            (agent_get_class, ":enemy_class_no", ":enemy_agent"),
            (neq, ":enemy_class_no", grc_cavalry),
            (agent_get_position, pos68, ":enemy_agent"),
            (get_distance_between_positions, ":dist", pos68, pos67),
            (gt, ":min_dist", ":dist"),
            (assign, ":min_dist", ":dist"),
            (copy_position, pos70, pos68), #pos70 holds the nearest enemy position
        (try_end),
    
      # (assign, reg0, ":min_dist"),
      # (assign, reg1, ":troll"),
      # (display_message, "@Debug: Troll {reg1} distance to enemy: {reg0}."),
        
        (try_begin),
          (this_or_next|eq, ":min_dist", 1000000),
          (lt, ":min_dist", 500),
          (agent_clear_scripted_mode, ":troll"), # leave the troll on its own if close enough to the enemy
        (else_try),
          (agent_set_scripted_destination, ":troll", pos70, 1), # head for the nearest enemy
        (try_end),
        #Trolls charging - end
    (try_end),


	(try_for_agents, ":troll"),
		(agent_is_active, ":troll"),
 		(agent_is_alive, ":troll"),
 		(agent_is_human, ":troll"),
 		(gt, ":troll", 0),
 		(agent_get_troop_id, ":troll_troop_id", ":troll"),
		(troop_get_type, ":troll_type", ":troll_troop_id"),
		(eq, ":troll_type", tf_troll),
		(agent_slot_eq, ":troll", slot_troll_agent_charging, 1),
		#(display_message, "@troll charge pushback found charging troll"),
 		(agent_get_position, pos19, ":troll"),
 		
 		(agent_ai_get_num_cached_enemies, ":nearby_enemies", ":troll"),
        (gt, ":nearby_enemies", 0),

        (try_for_range, ":nearby_agent_no", 0, ":nearby_enemies"), # @kham: Does this actually work without an additional agent_ai_get_cached_enemy check? 
			#(display_message, "@troll charge pushback find victims"),
			(agent_is_active, ":nearby_agent_no"),
	 		(agent_is_alive, ":nearby_agent_no"),
	 		(agent_is_human, ":nearby_agent_no"),
	 		(gt, ":nearby_agent_no", 0),
	 		(neq, ":nearby_agent_no", ":troll"), #don't hit yourself
	 		
	 		(agent_get_position, pos9,":nearby_agent_no"),
			(get_distance_between_positions,":dist",pos19,pos9),
			(le, ":dist", 400), #only affect agents closer than 4m

			(agent_get_troop_id, ":victim_troop_id", ":nearby_agent_no"),
			(troop_get_type, ":victim_type", ":victim_troop_id"),
			(agent_get_horse, ":victim_horse", ":nearby_agent_no"),
			(neq, ":victim_type", tf_troll), #no plowthrough for trolls
	      	(neg|is_between, ":victim_troop_id", warg_ghost_begin, warg_ghost_end),
	    	(neg|is_between, ":victim_troop_id", "trp_spider", "trp_dorwinion_sack"),
		    (neq, ":victim_troop_id", "trp_werewolf"),
					
			(agent_get_animation, ":cur_anim", ":nearby_agent_no"),
			(this_or_next|neq, ":cur_anim", "anim_strike_fall_back_rise"),
			(neq, ":cur_anim", "anim_strike_fly_back_rise"),

			(assign, ":continue_ko", 0),
			(store_mission_timer_a, ":timer"),
			(try_begin),
				(agent_slot_eq, ":nearby_agent_no", slot_agent_knocked_down, 0),
				(assign, ":continue_ko", 1),
				(agent_set_slot, ":nearby_agent_no", slot_agent_knocked_down, 1),
				(val_add, ":timer", 2), #2 seconds after Knock Down
				(agent_set_slot, ":nearby_agent_no", slot_agent_last_knockdown_time, ":timer"),
			(try_end),

			(eq, ":continue_ko", 1),
			
			(store_random_in_range, ":flyback_anim", 0, 2),
			# then, set animation
			# human (non trolls, non horse) victims
			(try_begin),
				(eq, ":flyback_anim", 0),
		# troll is in front of victim
				(agent_set_animation, ":nearby_agent_no", "anim_strike_fall_back_rise"), # send them flying back
			(else_try),
				(agent_set_animation, ":nearby_agent_no", "anim_strike_fly_back_rise"), # send them flying back
			(try_end),

			(agent_play_sound, ":troll", "snd_troll_yell"),
			
			(store_random_in_range, ":rand_sound", 0, 150),
			(try_begin),
				(is_between, ":rand_sound", 0, 10),
				(agent_play_sound, ":nearby_agent_no", "snd_wooden_hit_low_armor_low_damage"),
			(else_try),
				(is_between, ":rand_sound", 10, 20),
				(agent_play_sound, ":nearby_agent_no", "snd_wooden_hit_low_armor_high_damage"),
			(else_try),
				(is_between, ":rand_sound", 20, 30),
				(agent_play_sound, ":nearby_agent_no", "snd_wooden_hit_high_armor_low_damage"),
			(else_try),
				(is_between, ":rand_sound", 30, 40),
				(agent_play_sound, ":nearby_agent_no", "snd_wooden_hit_high_armor_low_damage"),
			(else_try),
				(is_between, ":rand_sound", 50, 60),
				(agent_play_sound, ":nearby_agent_no", "snd_wooden_hit_high_armor_high_damage"),
			(else_try),
				(is_between, ":rand_sound", 60, 70),
				(agent_play_sound, ":nearby_agent_no", "snd_blunt_hit"),
			(try_end),

			(try_begin),
				(gt, ":victim_horse", 1),
				(agent_start_running_away, ":victim_horse"),
				(agent_stop_running_away, ":victim_horse"),
			(try_end),
			(set_fixed_point_multiplier, 1),
			(store_random_in_range,":random_timings",1,5),
			(agent_set_animation_progress, ":nearby_agent_no", ":random_timings"), # differentiate timings a bit
		(try_end),
	(try_end),

]),

] or [])



# mtarini: troll fights by scripts
#MV: inserted troll "charging" (going ahead not following orders)
custom_troll_hitting = ((is_a_wb_mt==1) and ( 

0.3,0,0, [(gt,"$trolls_in_battle",0)],[
	(try_for_agents,":troll"),
		(agent_is_alive,":troll"),
		(agent_is_human,":troll"),
		(agent_is_active, ":troll"),
		(agent_get_troop_id,":troll_troop_id",":troll"), # is it a troll?
		(troop_get_type, ":troll_type", ":troll_troop_id"),
		(eq, ":troll_type", tf_troll),

		(agent_ai_get_num_cached_enemies, ":num_nearby_agents", ":troll"),
        (gt, ":num_nearby_agents", 0),
        #Trolls charging - begin

        #(agent_get_team, ":troll_team", ":troll"),
        (agent_get_position, pos1, ":troll"),

        #get the closest noncav enemy
        (assign, ":min_dist", 1000000),
        (try_for_range, ":nearby_agent_no", 0, ":num_nearby_agents"),
        	(agent_ai_get_cached_enemy, ":enemy_agent", ":troll", ":nearby_agent_no"),
            (agent_is_alive, ":enemy_agent"),
            (agent_is_human, ":enemy_agent"),
            (agent_is_active, ":enemy_agent"),
            (agent_get_class, ":enemy_class_no", ":enemy_agent"),
            (neq, ":enemy_class_no", grc_cavalry),
            (agent_get_position, pos9, ":enemy_agent"),
            (get_distance_between_positions, ":dist", pos9, pos1),
            (gt, ":min_dist", ":dist"),
            (assign, ":min_dist", ":dist"),
            (copy_position, pos2, pos9), #pos2 holds the nearest enemy position
        (try_end),
    
      # (assign, reg0, ":min_dist"),
      # (assign, reg1, ":troll"),
      # (display_message, "@Debug: Troll {reg1} distance to enemy: {reg0}."),
        
        (try_begin),
          (this_or_next|eq, ":min_dist", 1000000),
          (lt, ":min_dist", 500),
          (agent_clear_scripted_mode, ":troll"), # leave the troll on its own if close enough to the enemy
        (else_try),
          (agent_set_scripted_destination, ":troll", pos2, 1), # head for the nearest enemy
        (try_end),
        #Trolls charging - end
		
		# Troll Swing Status Check
		(agent_get_slot,":status",":troll",slot_agent_troll_swing_status),
		(try_begin),
			(neg|eq,":status",0),
			(store_add,":status",":status",1),
		(else_try),
			# status is 0: *can* decide to start a swing
			(get_player_agent_no, ":player_agent"),
			(try_begin),
				(eq, ":player_agent", ":troll"),
			#	(display_message, "@Debug: Player controlled troll."),
				# player controlled trolls swing when button pressed
				(try_begin),
					(key_is_down, key_left_mouse_button),
					(assign,":status",1), 
				#	(display_message, "@Debug: Troll attack key pressed."),
				(try_end),
			(else_try),
				# AI attacks 10% of times, if at least a victim is in range - changed to 20% (kham)
				(store_random_in_range,":random",1,101),
				(le,":random",20), 
				(agent_get_position, pos1,":troll"),
				(try_for_range, ":nearby_agent_no", 0, ":num_nearby_agents"),
					(eq,":status",0),
					(agent_ai_get_cached_enemy, ":victim", ":troll", ":nearby_agent_no"),
					(agent_is_human,":victim"),
					(agent_is_alive, ":victim"),
					(agent_is_active, ":victim"),
					(agent_get_position,pos2,":victim"),
					(get_distance_between_positions,":dist",pos1,pos2),
					(store_random_in_range, ":random_swing", 0,61), 
					(val_sub, ":dist", ":random_swing"), # swing earlier than in range (sometimes)
					(lt,":dist",300), # 200+weapon size/2
					(neg|position_is_behind_position,pos2,pos1),
					(assign,":status",1),
				(try_end),
			(try_end),
		(try_end),
		
		(store_agent_hit_points,":cur_hp",":troll",1),
		
		(agent_get_slot,":last_hp", ":troll",slot_agent_last_hp),
		
		# test for stun
		(try_begin),
		
			#swy-- i still don't get this logic, but anyway, from now on if there isn't
			#----- a previous health we'll use the current one, and trolls will get stunned
			#----- if they have received >= 3 points of damage in this delta/relative difference.
			
			(try_begin),
				(lt, ":last_hp", 1),
				(assign, ":last_hp", ":cur_hp"),
			(try_end),
			
		#	(val_add,":last_hp",3), #swy-- why this? getting the damage difference between frames and checking against as limit seems easier... i've tested this and works fine, and stun-rate is more of the same.
			
			(store_sub,":hp_difference", ":last_hp", ":cur_hp"),
			
		#	(assign,reg1,":last_hp"),
		#	(assign,reg2, ":cur_hp"),
		#	(assign,reg3, ":hp_difference"),
		#	(display_message,"@DEBUG: last hp:{reg1} cur hp:{reg2} diff:{reg3}"),
			
			# 282 >= 282 ?!!
			# 285 >= 282
		#	(ge,":last_hp",":cur_hp"), #swy-- this doesn't make sense, use a more straightforward logic. look under and above this.
			
			(ge,    ":hp_difference", 55),
			(assign,":status",       -3), # STUNNED: skip 4 "turns"
		#	(display_message, "@Debug: Troll STUNNED: skip 4 turns."),
		(try_end),
		
		(agent_set_slot, ":troll", slot_agent_troll_swing_status,":status"),
		(agent_set_slot, ":troll", slot_agent_last_hp,           ":cur_hp"),
		
		(try_begin),
			# status = 1: make troll start the attack!
			(eq,":status",1),
		#	(display_message, "@Debug: STATUS 1."),
			(store_random_in_range,":random_attack",1,4), #1 = left, 2 = right, 3 or more= overhead
			(try_begin),
				(eq,":random_attack",1),
				(agent_set_animation, ":troll", "anim_ready_slashright_troll"),
			(else_try),
				(eq,":random_attack",2),
				(agent_set_animation, ":troll", "anim_ready_slashleft_troll"),
			(else_try),
				(assign,":random_attack",3),
				(agent_set_animation, ":troll", "anim_ready_overswing_troll"),
			(try_end),
			(agent_play_sound,":troll","snd_troll_grunt_long"),
			(agent_set_slot,":troll",slot_agent_troll_swing_move,":random_attack"),
		(else_try),
			# status = 3: make troll end the attack!
			(eq,":status",3),
			(agent_set_slot,":troll",slot_agent_troll_swing_status,-2), # RECOVER: wait 2 "turns" before next attack
			(agent_get_slot,":attack",":troll",slot_agent_troll_swing_move),
			
			# make last piece of animation (should be useless, but necessary for when troll misteriously loses attack animation)
			(try_begin),
				(eq,":attack",1),
				(agent_set_animation, ":troll", "anim_ready_and_release_slashright_troll"),
			(else_try),
				(eq,":attack",2),
				(agent_set_animation, ":troll", "anim_ready_and_release_slashleft_troll"),
			(else_try),
				(agent_set_animation, ":troll", "anim_ready_and_release_overswing_troll"),
			(try_end),
	  
			(agent_play_sound,":troll","snd_big_weapon_swing"),
			(agent_get_position,pos1,":troll"),
	  		
			(try_for_range, ":nearby_agent_no", 0, ":num_nearby_agents"),
				(agent_ai_get_cached_enemy, ":victim", ":troll", ":nearby_agent_no"),
				(agent_is_alive,":victim"),
				(agent_is_active, ":victim"),
				(agent_get_position,pos2,":victim"),
				(neg|position_is_behind_position,pos2,pos1),
				(get_distance_between_positions,":dist",pos1,pos2),
				(lt,":dist",300), # troll disntance

				# decrease hit angle range for owerswing:
				(assign,":hit",1),
				(try_begin),
					(ge,":attack",3), # if overswing: smaller angle - interval 
					(copy_position,pos3,pos1),
					(position_rotate_z,pos3,75),
					(position_is_behind_position,pos2,pos3),
					(position_rotate_z,pos3,-150),
					(position_is_behind_position,pos2,pos3),
					(assign,":hit",0), # misses troops if not in +/- 30 degrees 
				(try_end),

				(eq,":hit",1),
			
				# get victim type
				(agent_get_troop_id,":victim_troop_id",":victim"),
				(troop_get_type, ":victim_type", ":victim_troop_id"),
				
			
				(try_begin),
					(agent_is_human,":victim"),
		
					(agent_play_sound,":victim","snd_blunt_hit"),			
					(agent_deliver_damage_to_agent, ":troll", ":victim"),
					(try_begin),
						(ge,":attack",3),
						(agent_deliver_damage_to_agent, ":troll", ":victim"), # double damage with overhead swing
					(try_end),

					# set victim animation:...
					
					# first, turn victim position according to swing direction  to better determine possible flight direction if hit
					(try_begin),
						(eq,":attack",2), # if swing left
						(position_rotate_z,pos2,45),
					(else_try),
						(eq,":attack",1), # if swing right
						(position_rotate_z,pos2,-45),
					(try_end),
					
					(agent_get_horse, ":victim_horse", ":victim"),
					# then, set animation
					(try_begin),
						(neg|is_between, ":victim_troop_id", warg_ghost_begin, warg_ghost_end),
						#(agent_is_alive,":victim"), # agent is STILL alive
						(try_begin),
							(eq, ":victim_type", tf_troll), # trolls don't send other trolls flying back: they just knowk them back
							(agent_set_animation, ":victim", "anim_strike_fall_back_rise"),
						(else_try),
							# human (non trolls, non horse) victims
							(try_begin),
								(position_is_behind_position,pos1,pos2), # troll is on back of victim
								(agent_set_animation, ":victim", "anim_strike_fly_front_rise"), # send them flying front
							(else_try),
								# troll is in front of victim
								(assign,":from_left",0), # animate as if swing comes from left?
								(try_begin),
									(eq,":attack",2), # if left swing, hurl, 
									(assign,":from_left",1),       # then from left
								(else_try),
									(eq,":attack",3), # if overswing, roll
									(store_random_in_range,":from_left",0,2),  # then 50% from left
								(try_end),
								(try_begin),
									(eq,":from_left",1), # if swing left
									(agent_set_animation, ":victim", "anim_strike_fly_back_rise_from_left"), # send them flying back
								(else_try),
									(agent_set_animation, ":victim", "anim_strike_fly_back_rise"), # send them flying back
								(try_end),
							(try_end),
							(try_begin),
								(gt, ":victim_horse", 1),
								(agent_start_running_away, ":victim_horse"),
								(agent_stop_running_away, ":victim_horse"),
							(try_end),
							(store_random_in_range,":random_timings",1,5),
							(agent_set_animation_progress, ":victim", ":random_timings"), # differentiate timings a bit
						(try_end),
					(try_end),
				
				(else_try),
					(agent_set_hit_points,":victim",0), # horses are killed on spot!
					(agent_deliver_damage_to_agent, ":troll", ":victim"),
				(try_end),
			(try_end),
		(try_end),
	(try_end),
])

or

( 0.3,0,0, [(gt,"$trolls_in_battle",0)],[
	(try_for_agents,":troll"),
		(agent_is_alive,":troll"),
		(agent_is_human,":troll"),
		(agent_get_troop_id,":troll_troop_id",":troll"), # is it a troll?
		(troop_get_type, ":troll_type", ":troll_troop_id"),
		(eq, ":troll_type", tf_troll),
        #Trolls charging - begin
        (agent_get_team, ":troll_team", ":troll"),
        (agent_get_position, pos1, ":troll"),

        #get the closest noncav enemy
        (assign, ":min_dist", 1000000),
        (try_for_agents, ":enemy_agent"),
            (agent_is_alive, ":enemy_agent"),
            (agent_is_human, ":enemy_agent"),
            (agent_get_team, ":enemy_team_no", ":enemy_agent"),
            (teams_are_enemies, ":enemy_team_no", ":troll_team"),
            (agent_get_class, ":enemy_class_no", ":enemy_agent"),
            (neq, ":enemy_class_no", grc_cavalry),
            
            (agent_get_position, pos0, ":enemy_agent"),
            (get_distance_between_positions, ":dist", pos0, pos1),
            (gt, ":min_dist", ":dist"),
            (assign, ":min_dist", ":dist"),
            (copy_position, pos2, pos0), #pos2 holds the nearest enemy position
        (try_end),
    
      # (assign, reg0, ":min_dist"),
      # (assign, reg1, ":troll"),
      # (display_message, "@Debug: Troll {reg1} distance to enemy: {reg0}."),

        (try_begin),
          (this_or_next|eq, ":min_dist", 1000000),
          (lt, ":min_dist", 500),
          (agent_clear_scripted_mode, ":troll"), # leave the troll on its own if close enough to the enemy
        (else_try),
          (agent_set_scripted_destination, ":troll", pos2, 1), # head for the nearest enemy
        (try_end),
        #Trolls charging - end
        
	#mtarini: for tuning: show current troll HP at random times
	#swy-- we don't actually need this entire block at all... don't selectively comment out the print leaving the other stuff there!
	#	(try_begin), 
	#		(store_random_in_range,":random",1,20),
	#		(eq,":random",1), # show it once in 20
	#		(store_agent_hit_points,reg1,":troll"),
	#		(display_message,"@DEBUG: troll health: {reg1}%!"),
	#	(try_end),
		
		(agent_get_slot,":status",":troll",slot_agent_troll_swing_status),
		(try_begin),
			(neg|eq,":status",0),
			(store_add,":status",":status",1),
		(else_try),
			# status is 0: *can* decide to start a swing
			(get_player_agent_no, ":player_agent"),
			(try_begin),
				(eq, ":player_agent", ":troll"),
			#	(display_message, "@Debug: Player controlled troll."),
				# player controlled trolls swing when button pressed
				(try_begin),
					(key_is_down, key_left_mouse_button),
					(assign,":status",1), 
				#	(display_message, "@Debug: Troll attack key pressed."),
				(try_end),
			(else_try),
				# AI attacks 10% of times, if at least a victim is in range - changed to 20% (kham)
				(store_random_in_range,":random",1,101),
				(le,":random",20), 
				(agent_get_position,1,":troll"),
				(agent_get_team, ":troll_team", ":troll"),
				(try_for_agents,":victim"),
					(eq,":status",0),
					(agent_is_human,":victim"),
					(agent_is_alive, ":victim"),
					(agent_get_team, ":victim_team", ":victim"),
					(teams_are_enemies, ":victim_team", ":troll_team"),
					(agent_get_position,2,":victim"),
					(get_distance_between_positions,":dist",1,2),
					(store_random_in_range, ":random_swing", 0,61), 
					(val_sub, ":dist", ":random_swing"), # swing earlier than in range (sometimes)
					(lt,":dist",300), # 200+weapon size/2
						
					(neg|position_is_behind_position,2,1),
					(assign,":status",1),
				(try_end),
			(try_end),
		(try_end),
		
		(store_agent_hit_points,":cur_hp",":troll",1),
		(agent_get_slot,":last_hp", ":troll",slot_agent_last_hp),
		# test for stun
		(try_begin),
		
			#swy-- i still don't get this logic, but anyway, from now on if there isn't
			#----- a previous health we'll use the current one, and trolls will get stunned
			#----- if they have received >= 3 points of damage in this delta/relative difference.
			
			(try_begin),
				(lt, ":last_hp", 1),
				(assign, ":last_hp", ":cur_hp"),
			(try_end),
			
		#	(val_add,":last_hp",3), #swy-- why this? getting the damage difference between frames and checking against as limit seems easier... i've tested this and works fine, and stun-rate is more of the same.
			
			(store_sub,":hp_difference", ":last_hp", ":cur_hp"),
			
		#	(assign,reg1,":last_hp"),
		#	(assign,reg2, ":cur_hp"),
		#	(assign,reg3, ":hp_difference"),
		#	(display_message,"@DEBUG: last hp:{reg1} cur hp:{reg2} diff:{reg3}"),
			
			# 282 >= 282 ?!!
			# 285 >= 282
		#	(ge,":last_hp",":cur_hp"), #swy-- this doesn't make sense, use a more straightforward logic. look under and above this.
			
			(ge,    ":hp_difference", 55),
			(assign,":status",       -4), # STUNNED: skip 4 "turns"
		#	(display_message, "@Debug: Troll STUNNED: skip 4 turns."),
		(try_end),
		
		(agent_set_slot, ":troll", slot_agent_troll_swing_status,":status"),
		(agent_set_slot, ":troll", slot_agent_last_hp,           ":cur_hp"),
		
		(try_begin),
			# status = 1: make troll start the attack!
			(eq,":status",1),
		#	(display_message, "@Debug: STATUS 1."),
			(store_random_in_range,":random_attack",1,4), #1 = left, 2 = right, 3 or more= overhead
			(try_begin),
				(eq,":random_attack",1),
				(agent_set_animation, ":troll", "anim_ready_slashright_troll"),
			(else_try),
				(eq,":random_attack",2),
				(agent_set_animation, ":troll", "anim_ready_slashleft_troll"),
			(else_try),
				(assign,":random_attack",3),
				(agent_set_animation, ":troll", "anim_ready_overswing_troll"),
			(try_end),
			(agent_play_sound,":troll","snd_troll_grunt_long"),
			(agent_set_slot,":troll",slot_agent_troll_swing_move,":random_attack"),
		(else_try),
			# status = 3: make troll end the attack!
			(eq,":status",3),
			(agent_set_slot,":troll",slot_agent_troll_swing_status,-2), # RECOVER: wait 2 "turns" before next attack
			(agent_get_slot,":attack",":troll",slot_agent_troll_swing_move),
			
			# make last piece of animation (should be useless, but necessary for when troll misteriously loses attack animation)
			(try_begin),
				(eq,":attack",1),
				(agent_set_animation, ":troll", "anim_ready_and_release_slashright_troll"),
			(else_try),
				(eq,":attack",2),
				(agent_set_animation, ":troll", "anim_ready_and_release_slashleft_troll"),
			(else_try),
				(agent_set_animation, ":troll", "anim_ready_and_release_overswing_troll"),
			(try_end),
			#(agent_set_animation_progress, ":troll", 66),
	  
			(agent_play_sound,":troll","snd_big_weapon_swing"),
	  
			#(try_begin),
				#(eq,"$g_troll_chosen_move",3),
				#(agent_get_look_position,1,":troll"), # because move 3 (overswing) rotates torso!
			#(else_try),
			(agent_get_position,1,":troll"),
			#(try_end),
	  		
			(try_for_agents,":victim"),
				(agent_is_alive,":victim"),
				(neq,":troll",":victim"), # a troll doesn't hit itself
				(agent_get_position,2,":victim"),
				(neg|position_is_behind_position,2,1),
				(get_distance_between_positions,":dist",1,2),
				(lt,":dist",300), # troll disntance
			
				# decrease hit angle range for owerswing:
				(assign,":hit",1),
				(try_begin),
					(ge,":attack",3), # if overswing: smaller angle - interval 
					(copy_position,3,1),
					(position_rotate_z,3,75),
					(position_is_behind_position,2,3),
					(position_rotate_z,3,-150),
					(position_is_behind_position,2,3),
					(assign,":hit",0), # misses troops if not in +/- 30 degrees 
				(try_end),
				(eq,":hit",1),
			
				# test if friendly troll...
				(agent_get_troop_id,":victim_troop_id",":victim"),
				(troop_get_type, ":victim_type", ":victim_troop_id"),
				(agent_get_team, ":victim_team", ":victim"),
				(agent_get_team, ":troll_team", ":troll"),
				(neq|this_or_next, ":victim_type", tf_troll), # trolls don't hit trolls!
				(teams_are_enemies, ":victim_team", ":troll_team"),  # ...unless they are enemy trolls
			
				(try_begin),
					(agent_is_human,":victim"),
		
					(agent_play_sound,":victim","snd_blunt_hit"),			
					(agent_deliver_damage_to_agent, ":troll", ":victim"),
					(try_begin),
						(ge,":attack",3),
						(agent_deliver_damage_to_agent, ":troll", ":victim"), # double damage with overhead swing
					(try_end),

					# set victim animation:...
					
					# first, turn victim position according to swing direction  to better determine possible flight direction if hit
					(try_begin),
						(eq,":attack",2), # if swing left
						(position_rotate_z,2,45),
					(else_try),
						(eq,":attack",1), # if swing right
						(position_rotate_z,2,-45),
					(try_end),
					
					# then, set animation
					(try_begin),
						#(agent_is_alive,":victim"), # agent is STILL alive
						(try_begin),
							(eq, ":victim_type", tf_troll), # trolls don't send other trolls flying back: they just knowk them back
							(agent_set_animation, ":victim", "anim_strike_fall_back_rise"),
						(else_try),
							# human (non trolls, non horse) victims
							(try_begin),
								(position_is_behind_position,1,2), # troll is on back of victim
								(agent_set_animation, ":victim", "anim_strike_fly_front_rise"), # send them flying front
							(else_try),
								# troll is in front of victim
								(assign,":from_left",0), # animate as if swing comes from left?
								(try_begin),
									(eq,":attack",2), # if left swing, hurl, 
									(assign,":from_left",1),       # then from left
								(else_try),
									(eq,":attack",3), # if overswing, roll
									(store_random_in_range,":from_left",0,2),  # then 50% from left
								(try_end),
								(try_begin),
									(eq,":from_left",1), # if swing left
									(agent_set_animation, ":victim", "anim_strike_fly_back_rise_from_left"), # send them flying back
								(else_try),
									(agent_set_animation, ":victim", "anim_strike_fly_back_rise"), # send them flying back
								(try_end),
							(try_end),
							(store_random_in_range,":random_timings",1,5),
							(agent_set_animation_progress, ":victim", ":random_timings"), # differentiate timings a bit
						(try_end),
					#(else_try),
						# victim has been killed: won't rise after fall USELESS: game won't listen...
						#(try_begin),
						#	(position_is_behind_position,1,2), # troll is on back of victim
						# 	(agent_set_animation, ":victim", "anim_strike_fly_front"), # send them flying front -- don't rise
						#(else_try),
						#  	(agent_set_animation, ":victim", "anim_strike_fly_back"), # send them flying back -- don't rise
						#(try_end),			
						#(display_message,"@DEBUG: troll kills!"),
					(try_end),
				
				(else_try),
					(agent_set_hit_points,":victim",0), # horses are killed on spot!
					(agent_deliver_damage_to_agent, ":troll", ":victim"),
				(try_end),
			(try_end),
		(try_end),
	(try_end),
])

)

custom_tld_horses_hate_trolls = ((is_a_wb_mt==1) and (
	1,0,1, [(eq,"$trolls_in_battle",1)],[
                (get_player_agent_no, ":player_agent"),
		(try_for_agents,":troll"),          # horse rearing near troll
			(agent_is_alive, ":troll"), #GA: horses hate dead trolls too - Removed (kham)
			(agent_get_troop_id,":troop_race",":troll"),
			(try_begin), # CC: Change string if it is an ent and not a troll			
				(assign, reg73, 0),
				(eq, ":troop_race", "trp_ent"),
				(assign, reg73, 1),
			(try_end),
			(troop_get_type, ":type", ":troop_race"),
			(try_begin),
				(eq, ":type", tf_troll),
				(agent_get_position,pos1,":troll"),
				(agent_ai_get_num_cached_enemies, ":num_nearby_agents", ":troll"),
				(assign, reg10, ":num_nearby_agents"),
				(gt, ":num_nearby_agents", 0),

				(try_for_range, ":nearby_agent_no", 0, ":num_nearby_agents"),
					(agent_ai_get_cached_enemy, ":rider", ":troll", ":nearby_agent_no"),
					(agent_is_active, ":rider"),
					(agent_get_horse, ":horse", ":rider"),
					(agent_is_alive,":rider"),
					(gt, ":horse", 1),
					(agent_get_position,pos2,":rider"),
					(get_distance_between_positions,":dist",pos1,pos2),
					(lt,":dist",700),
					(agent_get_troop_id, ":rider_troop", ":rider"), #Riding skill helps avoid (InVain)
                                        # Arsakes: exclude all invisible riders (animals + wargs + bearshifter)
                                        (neg|is_between, ":rider_troop", warg_ghost_begin, warg_ghost_end),
                                        (neg|is_between, ":rider_troop", "trp_spider", "trp_dorwinion_sack"),
                                        (neq, ":rider_troop", "trp_multiplayer_profile_troop_male"), (neq, ":rider_troop", "trp_werewolf"),

					(store_skill_level, ":riding", "skl_riding", ":rider_troop"),
					(store_add, ":riding_chance", ":riding", 6),
						#(assign, reg5, ":riding_chance"),
						#(display_message, "@chance = {reg5}"),
					(store_random_in_range, ":random", 0, ":riding_chance"),
						#(assign, reg6, ":random"),
						#(display_message, "@random = {reg6}"),
					(try_begin),(le,":random",1),(agent_set_animation,":horse","anim_horse_rear"      ),(agent_play_sound,":horse","snd_neigh"),
					 #(else_try),(eq,":random",1),(agent_set_animation,":horse","anim_horse_turn_right"),(agent_play_sound,":horse","snd_horse_low_whinny"), #these animations don't seem to bring the horse to a stop
					 #(else_try),(eq,":random",2),(agent_set_animation,":horse","anim_horse_turn_left"),(agent_play_sound,":horse","snd_horse_low_whinny"),
					(try_end),
                    # let the player know what happened
					(try_begin),
                        (eq, ":rider", ":player_agent"),
                        (is_between, ":random", 0, 2),
                        (display_message, "@Your mount is scared by the {reg73?ent:troll}!",color_bad_news),
					   (else_try),
					    (eq, ":rider", ":player_agent"),
                        (ge, ":random", 6),
                        (display_message, "@Your mount is scared by the {reg73?ent:troll}, but you can master it!",color_bad_news),
					(try_end),
				(try_end),
			(try_end),
		(try_end),
	])

or

	(1,0,1, [(eq,"$trolls_in_battle",1)],[
                (get_player_agent_no, ":player_agent"),
		(try_for_agents,":troll"),	    # horse rearing near troll
			(agent_is_alive, ":troll"), #GA: horses hate dead trolls too - Removed (kham)
			(agent_get_troop_id,":troop_race",":troll"),
			(try_begin), # CC: Change string if it is an ent and not a troll			
				(assign, reg73, 0),
				(eq, ":troop_race", "trp_ent"),
				(assign, reg73, 1),
			(try_end),
			(troop_get_type, ":type", ":troop_race"),
			(try_begin),
				(eq, ":type", tf_troll),
				(agent_get_position,pos1,":troll"),
				(agent_get_team, ":troll_team", ":troll"),
				(try_for_agents,":horse"),
					(neg|agent_is_human,":horse"),
					(agent_is_alive,":horse"),
					(agent_get_rider,":rider",":horse"),
					(neq,":rider",-1),
					(agent_get_team, ":rider_team", ":rider"),
					(teams_are_enemies, ":rider_team", ":troll_team"),
					(agent_get_position,2,":horse"),
					(get_distance_between_positions,":dist",1,2),
					(lt,":dist",700),
					(agent_get_troop_id, ":rider_troop", ":rider"), #Riding skill helps avoid (InVain)

                                        # Arsakes no animals or riderless wargs (no bear in MB)
                                        (neg|is_between, ":rider_troop", warg_ghost_begin, warg_ghost_end),
                                        (neg|is_between, ":rider_troop", "trp_spider", "trp_dorwinion_sack"),
                                        (neq, ":rider_troop", "trp_multiplayer_profile_troop_male"), (neq, ":rider_troop", "trp_werewolf")

					(store_skill_level, ":riding", "skl_riding", ":rider_troop"),
					(store_add, ":riding_chance", ":riding", 6),
					(store_random_in_range, ":random", 0, ":riding_chance"),
					(try_begin),(eq,":random",0),(agent_set_animation,":horse","anim_horse_rear"      ),(agent_play_sound,":horse","snd_neigh"),
					 (else_try),(eq,":random",1),(agent_set_animation,":horse","anim_horse_turn_right"),(agent_play_sound,":horse","snd_horse_low_whinny"),
					 (else_try),(eq,":random",2),(agent_set_animation,":horse","anim_horse_turn_left"),(agent_play_sound,":horse","snd_horse_low_whinny"),
					(try_end),
                    # let the player know what happened
					(try_begin),
                        (eq, ":rider", ":player_agent"),
                        (is_between, ":random", 0, 3),
                        (display_message, "@Your mount is scared by the {reg73?ent:troll}!",color_bad_news),
					   (else_try),
					    (eq, ":rider", ":player_agent"),
                        (ge, ":random", 6),
                        (display_message, "@Your mount is scared by the {reg73?ent:troll}, but you can master it!",color_bad_news),
					(try_end),
				(try_end),
			(try_end),
		(try_end),
	])
)


# matrini: warg attacks.... NOT USED YET (still WIP)
# CppCoder: improved, almost functional. :)

custom_lone_wargs_special_attack = (0.1, 0, 0, 
	[
		(gt,"$wargs_in_battle",0),
		(store_random_in_range,reg10,0,3), 
		(eq,reg10,1)
	],
	[
	(try_for_agents,":warg"), 
        	(agent_is_alive, ":warg"), #MV
		(agent_is_human, ":warg"),
		(agent_get_troop_id,reg0,":warg"),
		(is_between, reg0, warg_ghost_begin, warg_ghost_end),
		(agent_get_horse, ":warg_mount", ":warg"),
		(gt, ":warg_mount", -1),
        	(agent_get_position, pos0, ":warg_mount"),
		(agent_get_team, ":warg_team", ":warg"),
		(assign,":wants_to_jump",0),
        	(try_for_agents, ":enemy_agent"),
            		(agent_is_alive, ":enemy_agent"),
            		(agent_is_human, ":enemy_agent"),
            		(agent_get_team, ":enemy_team", ":enemy_agent"),
            		(teams_are_enemies, ":enemy_team", ":warg_team"),
            		(agent_get_position, pos10, ":enemy_agent"),
			(position_transform_position_to_local, pos2,pos0, pos10),
			(position_get_x, reg10, pos2),
			(position_get_y, reg11, pos2),
			(position_get_z, reg12, pos2),
			(position_normalize_origin, reg13, pos2),
			(val_mul, reg10,100.0),
			(val_mul, reg11,100.0),
			(val_mul, reg12,100.0),
			(val_mul, reg13,100.0),
			(convert_from_fixed_point, reg10),
			(convert_from_fixed_point, reg11),
			(convert_from_fixed_point, reg12),
			(convert_from_fixed_point, reg13),
			#(display_message, "@DEBUG: warg victim at ({reg10}, {reg11}, {reg12}) -- {reg13}"),
			(is_between, reg10, -100, 100),
			(is_between, reg11, +100, 600),
			(assign,":wants_to_jump",1),
        	(try_end),
		(try_begin),
			(agent_slot_eq, ":warg", slot_agent_warg_pouncing, 0),
			(eq,":wants_to_jump",1),
			(agent_set_animation, ":warg_mount", "anim_warg_jump"),
			(agent_set_animation, ":warg", "anim_ride_warg_jump"),
			(agent_set_slot,":warg", slot_agent_warg_pouncing, 1),
		(else_try),
			(agent_slot_eq, ":warg", slot_agent_warg_pouncing, 1),
			(agent_get_slot, ":warg_pounce_time", ":warg", slot_agent_warg_pounce_time),
			(val_add, ":warg_pounce_time", 1),
			(try_begin),
				(gt, ":warg_pounce_time", 30),
				# TODO: move agent to target pos and check for enemies to injure.
				(agent_set_slot,":warg", slot_agent_warg_pounce_time, 0),
				(agent_set_slot,":warg", slot_agent_warg_pouncing, 0),
			(else_try),
				(agent_set_slot,":warg", slot_agent_warg_pounce_time, ":warg_pounce_time"),
			(try_end),
		(try_end),
	(try_end),
])

# make mount sound by scripts (bypasses MaB limit to customize mount sounds),
custom_warg_sounds = (1,0,0, [(store_mission_timer_a,reg1),(ge,reg1,5),], # warg and horse sounds
  [ (assign, "$wargs_in_battle", 0), # recount them, to account for deaths
    
    (try_for_agents, ":mount"),
		(neg|agent_is_human, ":mount"),
		(agent_get_item_id, ":item", ":mount"),
		(try_begin),
			(is_between|this_or_next, ":item", item_horse_begin ,item_horse_end),
			(eq, ":item", "itm_mearas_reward"),			# CppCoder: Fixes minor sound bug
			(try_begin), 						#sounds for alive horses
				(agent_is_alive, ":mount"),
				(store_random_in_range, ":random", 1, 101), 
				(try_begin),(le, ":random", 7),(agent_play_sound, ":mount", "snd_horse_snort1"),(try_end),
			(else_try), 						#sounds for dying horses
				(agent_slot_eq, ":mount", slot_agent_mount_dead, 0),
				(agent_play_sound, ":mount", "snd_neigh1"),
				(agent_set_slot,":mount", slot_agent_mount_dead, 1),
			(try_end),
		(else_try),
			(eq, ":item", "itm_spider"),			# CppCoder: Spider sounds
			(try_begin), 	
				(agent_is_alive, ":mount"),
				(store_random_in_range, ":random", 1, 101), 
				(try_begin),(le, ":random", 7),(agent_play_sound, ":mount", "snd_spider"),(try_end),
			(else_try), 						
				(agent_slot_eq, ":mount", slot_agent_mount_dead, 0),
				(agent_play_sound, ":mount", "snd_spider_die"),
				(agent_set_slot,":mount", slot_agent_mount_dead, 1),
			(try_end),
		(else_try),
			(try_begin),						#sounds for alive wargs
				(agent_is_alive, ":mount"),
				(is_between, ":item", item_warg_begin ,item_warg_end),
				(val_add, "$wargs_in_battle", 1), #  wargs_in_battle++
				(store_random_in_range, ":random", 1, 101), (le, ":random", 4),  # 4% of time
				#(display_message,"@warg says: 'woof, woof!'"),
				(agent_play_sound, ":mount", "snd_warg_lone_woof"),
			(else_try), 						#sounds for dying wargs
				(agent_slot_eq, ":mount", slot_agent_mount_dead, 0),
				(agent_play_sound, ":mount", "snd_troll_die"),
				(agent_set_slot,":mount", slot_agent_mount_dead, 1),
			(try_end),
		(try_end),
	(try_end),
])

# mtarini: wargs attack even if they are not mounted
#swy-- note: the other half of the code is in custom_tld_spawn_troop
custom_lone_wargs_are_aggressive = (1.5,0,0, [],[ #GA: increased interval to 1.5 to have more time for dead riders to fall down (otherwise they disappear to Pluto with the mount)
	(try_for_agents,":ghost"), # self destruct any ghost rider which has no ride
		(agent_is_alive, ":ghost"), 
		(agent_is_human, ":ghost"),
		#--
		(agent_get_troop_id,":trp_ghost",":ghost"),
		(is_between,        ":trp_ghost", warg_ghost_begin, warg_ghost_end),
		
		(agent_set_animation, ":ghost", "anim_hide_inside_warg"), #anim_ride_1"),

		#swy-- there's a 6% prob every 1.5 secs of random lone warg sounds!
		(store_random_in_range, ":random", 0,100),
		(try_begin),
				(le,":random",6),
				# should be brutal GRRR of attacking warg here
				(agent_play_sound, ":ghost", "snd_warg_lone_woof"),
		(try_end),
		
		#swy-- add +1 to the time counter slot of this lone warg
		(agent_get_slot, reg1, ":ghost", slot_agent_time_counter), (val_add, reg1, 1),
		(agent_set_slot,       ":ghost", slot_agent_time_counter,            reg1),
		
		#swy-- make riderless wargs run away after X secs
		(try_begin),
			(eq, reg1, 15),
			(init_position, pos0), #send them to 0,0

		## WB has a routing operation we can use - Kham
		] + ((is_a_wb_mt==1) and [
			(agent_start_running_away, ":ghost"),
			#(display_message, "@DEBUG: Warg has started running away"),

		] or [
			(agent_set_scripted_destination, ":ghost", pos0, 1),
		]) + [

		(try_end),
		
		(agent_get_horse,":horse",":ghost"),
		(this_or_next|eq,":horse",-1), # remove wargless riders 
		(             gt, reg1, 25),   # or wargs running from battle for 45 sec ##Kham - reduce it by 10 seconds, see what happens... #Kham 3.5.1 revert back
		#--
		(call_script, "script_remove_agent", ":ghost"),
	(try_end),

	(try_for_agents,":cur_warg"), 
		(    agent_is_alive, ":cur_warg"),
		(neg|agent_is_human, ":cur_warg"),
		
		#swy-- if this agent is a horse/warg/mount, get the mount item...
		(agent_get_item_id,":warg_itm",":cur_warg"),
		
		#swy-- if this mount is a warg and riderless...
		(is_between, ":warg_itm", item_warg_begin, item_warg_end),
		#--- {ensure that the original rider hasn't just dismounted}
		(agent_get_slot,     ":orig_rider", ":cur_warg", slot_agent_mount_orig_rider),
		(gt, ":orig_rider", 0), #Kham - patch fix to MT errors. Not sure why it is getting 0 in that slot after the gundabad update. Will have to study.
		(neg|agent_is_alive, ":orig_rider"),
		#--- {there's no rider on top of the warg right now, old or new}
		(agent_get_rider,    ":curr_rider", ":cur_warg"),
		(eq,                 ":curr_rider", -1),
		#--- {this warg isn't owned by a ghost}
		(agent_get_troop_id, ":orig_rider_trp", ":orig_rider"),
		(neg|is_between,     ":orig_rider_trp", warg_ghost_begin, warg_ghost_end),

	#	(display_message,"@warg without rider found!"),
		#--
		(eq, "$warg_to_be_replaced", -1), # only spawn 1 new warg per "turn"
		(assign, "$warg_to_be_replaced", ":cur_warg"),
		
		#swy-- calculate the correct ghost warg troop by using the warg item offset, they are listed in the same order...
		(store_sub, ":warg_ghost_trp", ":warg_itm", item_warg_begin),
		(val_add,   ":warg_ghost_trp",             warg_ghost_begin),
		#--
		(assign, ":continue", 1),
		(agent_get_position, pos10, ":cur_warg"),

		] + ((is_a_wb_mt==1) and [
		(try_for_agents, ":old_rider", pos10, 50),
		] or [
		(try_for_agents, ":old_rider"),
		]) + [

			(eq, ":continue", 1),
			(agent_slot_eq,  ":old_rider", slot_agent_mount, ":cur_warg"),
			(agent_set_slot, ":old_rider", slot_agent_mount, -1),
			(assign, ":continue", 0),
		(try_end),
		

		
		] + ((not is_a_wb_mt==1) and [
    
		#swy-- classic 1.011 code path for spawning wargs
		(position_get_rotation_around_z, reg1, pos10),
		(call_script, "script_get_entry_point_with_most_similar_facing", reg1),
		(val_sub,reg1,1), # translate entry point number into mission entry
		#--
		(store_current_scene, ":cur_scene"),
		(modify_visitors_at_site, ":cur_scene"),  
		(add_visitors_to_current_scene,reg1,":warg_ghost_trp",1),
    
		] or [
    
		#swy-- new Warband code path for spawning wargs
		(set_spawn_position, pos10),
		(spawn_agent,":warg_ghost_trp"),
    
		]) + [
	#	(str_store_troop_name, s12, ":warg_ghost_trp"), 
	#	(display_message,"@DEBUG: trying respawn {s12} from entry {reg1}..."),
	(try_end),
	(set_show_messages,1)])

custom_track_companion_casualties = (0.5,0,0, [],[ 
	(try_for_range, ":npc",companions_begin,companions_end),
		(troop_get_slot,":agent",":npc",slot_companion_agent_id),
		(gt,":agent",0),
		(neg|agent_is_alive, ":agent"),
		(troop_set_slot, ":npc", slot_troop_wounded, 1),
	(try_end),
	(try_for_range, ":npc",new_companions_begin,new_companions_end),
		(troop_get_slot,":agent",":npc",slot_companion_agent_id),
		(gt,":agent",0),
		(neg|agent_is_alive, ":agent"),
		(troop_set_slot, ":npc", slot_troop_wounded, 1),
	(try_end)])

################## SIEGE LADDERS BEGIN #######################################
HD_ladders_init = (0,0,ti_once,[],[
			 (scene_prop_get_instance,":ladder", "spr_siege_ladder_14m", 0),###### lower siege ladders at battle start
			 (prop_instance_get_position,pos1,":ladder"),					###### saves the hassle of aligning props with wall
			 (position_rotate_x,pos1,120),
			 (prop_instance_set_position,":ladder",pos1),
			 (scene_prop_get_instance,":ladder", "spr_siege_ladder_14m", 1),
			 (prop_instance_get_position,pos1,":ladder"),
			 (position_rotate_x,pos1,120),
			 (prop_instance_set_position,":ladder",pos1)])
HD_ladders_rise = (0,25,ti_once, [],[(scene_prop_get_instance,":ladder", "spr_siege_ladder_14m", 0),	###### raise siege ladders after 25 sec into battle
			 (prop_instance_get_position,pos1,":ladder"),
			 (position_rotate_x,pos1,-120),
			 (prop_instance_animate_to_position,":ladder",pos1,900),
			 (play_sound,"snd_distant_carpenter"),

			 (scene_prop_get_instance,":ladder", "spr_siege_ladder_14m", 1),
			 (prop_instance_get_position,pos1,":ladder"),
			 (position_rotate_x,pos1,-120),
			 (prop_instance_animate_to_position,":ladder",pos1,1100),
			 (get_player_agent_no,":plyr"),
			 (agent_play_sound, ":plyr", "snd_evil_horn"),
			 (display_message,"@The ladders on Deeping Wall! Watch out!")])
################## SIEGE LADDERS END #########################################

################ BALLISTA BEGIN #################################
# Ibanez code heavily modified by GA
ballista_init = (0, 0, ti_once, [],[
			(assign,"$ballista_action",0),								###### 0 out of action, 1 is in action, 2 fired, 3 reloading
			(assign,"$ballista_fire",0),								###### arrow is not burning initially
			(assign,"$missile_count",0),								###### missiles spent
			(assign,"$missile_flying",0),								###### missile in flight indicator
			(scene_prop_get_instance,"$ballista_instance", "spr_ballista", 0),		###### ballista global position

			(scene_prop_get_num_instances,"$missile_max","spr_ballista_missile"),	###### max ammo. You need ballista_missile prop present on the map
			(prop_instance_get_position,pos1,"$ballista_instance"),					###### arrange missiles near ballista
			(position_move_z,pos1,10),
			(scene_prop_get_instance,":missile_instance", "spr_ballista_missile", 0),  ### first missile autoloaded
			(prop_instance_set_position,":missile_instance",pos1),
			(position_move_z,pos1,-107),
			(position_move_y,pos1,100),
			(position_rotate_z,pos1,90),
			(try_for_range,":count",1,"$missile_max"),
				(scene_prop_get_instance,":missile_instance", "spr_ballista_missile", ":count"),
				(store_random_in_range,":rnd",-4,4), (position_rotate_y,pos1,":rnd"),
				(store_random_in_range,":rnd",-4,4), (position_rotate_z,pos1,":rnd"),
				(store_random_in_range,":rnd",-10,10), (position_move_x,pos1,":rnd"),
				(store_random_in_range,":rnd",0,6), (position_move_z,pos1,":rnd"),
				(prop_instance_set_position,":missile_instance",pos1),
			(try_end),
#			(display_message,"@They are coming... Man the walls, Rohirrim!!"),
			])
			
ballista_operate = (0, 0, 1,	[(key_clicked, key_e),(eq,"$ballista_action",0)],
			[(try_begin),(ge,"$missile_count","$missile_max"),
				(display_message,"@Ballista: out of ammo!"),
			 (else_try),
			 	(prop_instance_get_position,pos1,"$ballista_instance"),
			 	(get_player_agent_no,":player_agent"),
				(agent_get_position,pos2,":player_agent"),
			 	(get_distance_between_positions,":distance",pos1,pos2),
			 	(lt,":distance",200),
					(mission_cam_set_mode,1),
					(position_move_z,pos1,125),
					(position_move_y,pos1,150),
					(position_rotate_z,pos1,180),
				 	(mission_cam_animate_to_position, pos1, 500,100),
					(display_message,"@Ballista: turn CURSOR, aim LSHIFT, shoot SPACE, set fire T, exit F"),
					(assign,"$ballista_action",1),
			 (try_end)])
ballista_disengage = (0, 0, 1, 	[(key_clicked, key_f),(eq,"$ballista_action",1)],		###### disengage ballista
			[
			 (mission_cam_set_mode,0),
			 (assign,"$ballista_action",0),
			 #swy-- disable the crossbow animation when leaving the ballista mode.
			 (get_player_agent_no,":player_agent"),
			 (agent_set_animation,":player_agent", "anim_cancel_ani_stand")
			])
ballista_shoot = (0, 0, 0,   [(key_clicked, key_space),(eq,"$ballista_action",1),(eq,"$missile_flying",0)],	###### fire in the hole!
			[#(display_message,"@Ballista: shooting"),
			 (assign,"$ballista_action",2),
			 (assign,"$missile_flying",1),
			 (scene_prop_get_instance,"$missile_flying_instance", "spr_ballista_missile","$missile_count"),
			 (prop_instance_get_position,pos1,"$ballista_instance"),
			 (position_move_z,pos1,300),
			 (position_move_y,pos1,300),
			 (position_rotate_z,pos1,180),
			 (mission_cam_animate_to_position, pos1, 500, 0),
			 (play_sound,"snd_release_crossbow")])
ballista_reload_pause = (0, 2, 0, 	[(eq,"$ballista_action",2),],[(assign,"$ballista_action",3)])
ballista_reload = (0, 0.1, 0, [(eq,"$ballista_action",3)],
			[(try_begin),(lt,"$missile_count","$missile_max"),
				(val_add,"$missile_count",1),								###### ammo count
				(play_sound,"snd_pull_ballista"),
			 	(prop_instance_get_position,pos1,"$ballista_instance"),		###### load missile mesh to ballista
			 	(position_move_z,pos1,10),
			 	(scene_prop_get_instance,":missile_instance", "spr_ballista_missile", "$missile_count"),
				(prop_instance_set_position,":missile_instance",pos1),
				(position_move_z,pos1,105),									###### set camera back to ballista
				(position_move_y,pos1,150),
				(position_rotate_z,pos1,180),
				(mission_cam_animate_to_position, pos1, 500,0),
				(assign,"$ballista_action",1),
#				(display_message,"@Ballista: reloaded successfully"),
			 (else_try),													###### exit ballista when ammo is out and replace with empty prop
			 	(prop_instance_get_position,pos1,"$ballista_instance"),		###### you need ballista_empty prop hidden on the map from the start
			 	(scene_prop_get_instance,":ballista_empty", "spr_ballista_empty",0),
			 	(prop_instance_get_position,pos2,":ballista_empty"),
				(prop_instance_set_position,":ballista_empty",pos1),
			 	(prop_instance_set_position,"$ballista_instance",pos2),
				(mission_cam_set_mode,0),
				(assign,"$ballista_action",0),
				(display_message,"@Ballista: out of ammo"),
			 (try_end)])
ballista_fly_missile = (0, 0, 0,   [(eq,"$missile_flying",1)],  
			[(prop_instance_get_position,pos1,"$missile_flying_instance"),		###### missile flight and killing
			 (copy_position,pos2,pos1),(position_get_z,":z_missile",pos1),
			 (position_set_z_to_ground_level, pos2),(position_get_z,":z_ground",pos2),
			 (val_sub,":z_missile",":z_ground"),
			 (try_begin),
			 (gt,":z_missile",50),							###### when ground is far away, fly the missile
				(position_move_y,pos1,-300),
				(position_rotate_x,pos1,1),
				(prop_instance_get_position,pos6,"$missile_flying_instance"),
				(prop_instance_animate_to_position,"$missile_flying_instance",pos1,10),
				(get_player_agent_no,":player_agent"),					###### when missile close, kill the agent by the player
				(try_for_agents,":agent"),
					(agent_is_alive, ":agent"),
					(agent_get_position,pos3,":agent"),
					(get_distance_between_positions,":missile_hit",pos1,pos3),
					(try_begin),
						(lt,":missile_hit",100),
							(agent_set_hit_points,":agent",0,0),
							(agent_deliver_damage_to_agent,":player_agent",":agent"),
							(particle_system_burst,"psys_game_blood",pos3,100),
							(agent_play_sound,":agent","snd_metal_hit_low_armor_high_damage"),
							(agent_play_sound,":agent","snd_orc_die"),
							### particle effect for MORE BLOOD!!!
					(try_end),
				(try_end),
			 (else_try),
#				(prop_instance_get_position,pos6,"$missile_flying_instance"),	###### stop missile on ground level
#				(position_rotate_x,pos6,-1),
#				(assign,":z_missile",-100),
#				(try_for_range,":knockback",1,10), 
#					(store_mul,":dy",":knockback",30),
#					(lt,":z_missile",100), 
#						(position_move_y,pos6,50),
#						(display_message,"@Ballista: missile shifted back"),
#						(position_get_z,":z_missile",pos6),
#						(copy_position,pos7,pos6),
#						(position_set_z_to_ground_level, pos7),
#						(position_get_z,":z_ground",pos7),
#						(val_sub,":z_missile",":z_ground"),
#				(try_end),
#				(prop_instance_set_position,"$missile_flying_instance",pos6),
#				(position_move_y,pos6,100),
#				(display_message,"@Ballista: missile hit ground!"),
				(assign,"$missile_flying",0),
				(position_move_y,pos1,100),
				(eq,"$ballista_fire",1),
					(particle_system_burst,"psys_torch_fire_sparks",pos1,70),
			(try_end)])
ballista_toggle_fire_arrow = (0, 0.1,0.5,[(key_clicked, key_t),(eq,"$ballista_action",1),(eq,"$missile_flying",0)], ### toggle fire on missile
			[(try_begin),(eq,"$ballista_fire",1),(assign,"$ballista_fire",0),
			  (else_try),				         (assign,"$ballista_fire",1),
			 (try_end)])
ballista_missile_illumination = (0, 0, 0, 	[(eq,"$ballista_fire",1)],   							###### missile illumination
			[(scene_prop_get_instance,":missile_instance", "spr_ballista_missile", "$missile_count"),
			 (prop_instance_get_position,pos1,":missile_instance"),
			 (position_move_y,pos1,-100),
			 (particle_system_burst, "psys_torch_fire",pos1,10),
#			 (particle_system_burst, "psys_torch_smoke",pos1,6),
			 (particle_system_burst, "psys_torch_fire_sparks",pos1,7),
			 (eq,"$missile_flying",1),
				(prop_instance_get_position,pos1,"$missile_flying_instance"),
				(position_move_y,pos1,-100),
				(particle_system_burst, "psys_torch_fire",pos1,10),
#				(particle_system_burst, "psys_torch_smoke",pos1,10),
				(particle_system_burst, "psys_torch_fire_sparks",pos1,10)])
ballista_camera_alignment = (0, 0, 0, 	[(eq,"$ballista_action",1)], 							###### camera and loaded missile alignment
			[(prop_instance_get_position,pos1,"$ballista_instance"),
			 (scene_prop_get_instance,":missile_instance", "spr_ballista_missile", "$missile_count"),
			 (position_move_z,pos1,5),
			 (prop_instance_set_position,":missile_instance",pos1),
			 (position_move_z,pos1,105),
			 (position_move_y,pos1,150),
			 (position_rotate_z,pos1,180),
		 	 (mission_cam_animate_to_position, pos1, 5,0),
			 (get_player_agent_no,":player_agent"),
			 (agent_set_animation,":player_agent", "anim_ready_crossbow")])
		###### turning ballista mesh and aiming
ballista_turn_up    =(0,0,0,[(key_is_down,key_up        ),(eq,"$ballista_action",1)],[(prop_instance_get_position,pos5,"$ballista_instance"),(position_rotate_x,pos5,1), (prop_instance_animate_to_position,"$ballista_instance",pos5,3)])
ballista_turn_down  =(0,0,0,[(key_is_down,key_down      ),(eq,"$ballista_action",1)],[(prop_instance_get_position,pos5,"$ballista_instance"),(position_rotate_x,pos5,-1),(prop_instance_animate_to_position,"$ballista_instance",pos5,3)])
ballista_turn_left  =(0,0,0,[(key_is_down,key_left      ),(eq,"$ballista_action",1)],[(prop_instance_get_position,pos5,"$ballista_instance"),(position_rotate_z,pos5,1), (prop_instance_animate_to_position,"$ballista_instance",pos5,3)])
ballista_turn_right =(0,0,0,[(key_is_down,key_right     ),(eq,"$ballista_action",1)],[(prop_instance_get_position,pos5,"$ballista_instance"),(position_rotate_z,pos5,-1),(prop_instance_animate_to_position,"$ballista_instance",pos5,3)])
ballista_aim        =(0,0,0,[(key_is_down,key_left_shift),(eq,"$ballista_action",1)],[(prop_instance_get_position,pos6,"$ballista_instance"),(position_move_y,pos6,60),(position_move_z,pos6,15),(position_rotate_z,pos6,180),(mission_cam_animate_to_position,pos6,100,1),])
################## BALLISTA END ##############################################

################## STONELOBBING BEGIN ########################################
################## uses spr_stoneball and spr_throwing_stone  ################
################## pos49 is used globally for stone tracking! ################
stonelobbing_init_stone = (0, 0, ti_once, [],[(assign,"$stonelobbing_state",0),				###### 0 no stones, 1 stone picked, 2,3,4 stone flying & bouncing
						(assign,"$stone_horizontal_velocity",0),
						(assign,"$stone_vertical_velocity",0),
						(assign,"$stone_rotation_x",20),				###### stone rotation speed in flight
						(assign,"$stone_rotation_y",30),
						(assign,"$stone_rotation_z",30)])
stonelobbing_pick_stone = (0,0,1, [(key_clicked, key_e),										###### picking up a stone
			(eq,"$stonelobbing_state",0),
			(get_player_agent_no,":player_agent"),
			(agent_get_wielded_item,reg1,":player_agent",0),			###### should be emptyhanded to pick up, duh
			(agent_get_wielded_item,reg2,":player_agent",1),
#			(display_message, "@DEBUG:STONE: Pick stone E, throw F, should be emptyhanded to pick"),
			(eq,reg1,-1),
			(eq,reg2,-1),
			],
			[(get_player_agent_no,":player_agent"),
			(agent_get_position,pos1,":player_agent"),
			(position_move_z,pos1,50),
			
			(scene_prop_get_num_instances,":num_stones","spr_stone_ball"), ### pick stone ball prop
			(try_for_range,":count",0,":num_stones"),
				(scene_prop_get_instance,":stone_instance", "spr_stone_ball", ":count"),
				(prop_instance_get_position,pos2,":stone_instance"),
				(get_distance_between_positions,":distance",pos1,pos2),
				(lt,":distance",150),
					(assign,"$stonelobbing_state",1),
					(assign,"$stone_picked_instance",":stone_instance"),
					(agent_set_walk_forward_animation,":player_agent", "anim_reload_crossbow"),
					(play_sound, "snd_man_grunt"),
			(try_end),
			
			(scene_prop_get_num_instances,":num_stones","spr_throwing_stone"),# or pick throwing stone prop
			(try_for_range,":count",0,":num_stones"),
				(scene_prop_get_instance,":stone_instance", "spr_throwing_stone", ":count"),
				(prop_instance_get_position,pos2,":stone_instance"),
				(get_distance_between_positions,":distance",pos1,pos2),
				(lt,":distance",150),(eq,"$stonelobbing_state",0),
					(assign,"$stonelobbing_state",1),
					(assign,"$stone_picked_instance",":stone_instance"),
					(agent_set_animation,":player_agent", "anim_reload_crossbow"),
					(play_sound, "snd_man_grunt"),
			(try_end)])
stonelobbing_throw_stone = (0,0,5, [(key_clicked, key_f),(eq,"$stonelobbing_state",1)],
			[(get_player_agent_no,":player_agent"),
			(agent_get_position,pos1,":player_agent"),
			(agent_get_look_position,pos2,":player_agent"),
			(copy_position,pos3,pos2),									####### get stone initial velocities
			(position_move_y,pos3,35),
			(position_transform_position_to_local, pos4, pos1,pos3),
			(position_get_y,"$stone_horizontal_velocity",pos4),
			(position_get_z,"$stone_vertical_velocity",pos4),
			(agent_get_position,pos49,":player_agent"),					###### orient stone with horizontal y for easier flight later
			(position_move_z,pos49,170),	
			(position_move_x,pos49,25),
			(prop_instance_set_position,"$stone_picked_instance",pos49),
			(agent_set_animation,":player_agent","anim_release_overswing_twohanded"),
			(play_sound, "snd_man_grunt"),
			(assign,"$stonelobbing_state",2)])
stonelobbing_fly_stone = (0,0,0, [(ge,"$stonelobbing_state",2)],
			[(prop_instance_get_position,pos1,"$stone_picked_instance"),
			(copy_position,pos2,pos49),
			(position_set_z_to_ground_level, pos2),
			(position_transform_position_to_local,pos4, pos49,pos2),
			(position_get_z,":z_missile",pos4),
			(try_begin),
			    (this_or_next|lt,":z_missile",-20), (gt,"$stone_vertical_velocity",0),		###### when ground is far away or flying up, fly stone
				(position_move_y,pos49,"$stone_horizontal_velocity"),
				(position_move_z,pos49,"$stone_vertical_velocity"),
				(val_sub,"$stone_vertical_velocity",1),					###### gravity

				(copy_position,pos2,pos49),								###### stone rotation
				(position_copy_rotation,pos2,pos1),
				(position_rotate_x,pos2,"$stone_rotation_x"),
				(position_rotate_y,pos2,"$stone_rotation_y"),
				(try_begin),											###### add spin when bounced
					(gt,"$stonelobbing_state",2),
					(position_rotate_z,pos2,"$stone_rotation_z"),
				(try_end),
				(prop_instance_animate_to_position,"$stone_picked_instance",pos2,5),

				(get_player_agent_no,":player_agent"),					###### when stone close to the agent
				(try_for_agents,":agent"),
					(agent_is_alive, ":agent"),
					(neq,":agent",":player_agent"),
					(agent_get_position,pos3,":agent"),
					(position_move_z,pos3,70),
					(get_distance_between_positions,":stone_hit",pos2,pos3),
					(try_begin),
						(lt,":stone_hit",100),
							(agent_play_sound,":agent","snd_blunt_hit"),
							(store_mul,":v","$stone_vertical_velocity",  "$stone_vertical_velocity"  ),
							(store_mul,":h","$stone_horizontal_velocity","$stone_horizontal_velocity"),
							(val_add,":v",":h"),
							(store_sqrt,":velocity",":v"),
							(try_begin),								###### kill the agent if stone is fast
								(gt,":velocity",40),
								(agent_set_hit_points,":agent",0,0),
								(agent_deliver_damage_to_agent,":player_agent",":agent"),
								(agent_play_sound,":agent","snd_orc_die"),
								(val_sub,"$stone_horizontal_velocity",5),	
							(else_try),									###### ko agent and deliver some damage if stone is slow
								(store_agent_hit_points,":hp",":agent",1),
								(val_div,":velocity",2),
								(val_sub,":hp",":velocity"),
								(try_begin), (lt,":hp",0),(assign,":hp",0),(try_end),
								(agent_set_hit_points,":agent",":hp",1),
								(agent_deliver_damage_to_agent,":player_agent",":agent"),
								(agent_set_animation,":agent","anim_strike_fall_back_rise"),
								(agent_play_sound,":agent","snd_orc_grunt"),
								(val_sub,"$stone_horizontal_velocity",2),
							(try_end),
					(try_end),
				(try_end),
			 (else_try),
			 	(play_sound,"snd_body_fall_small"),
				(prop_instance_get_position,pos1,"$stone_picked_instance"),
				(position_set_z_to_ground_level,pos1),
				(position_move_z,pos1,30),
				(prop_instance_set_position,"$stone_picked_instance",pos1),
				(try_begin),
					(lt,"$stonelobbing_state",4),						###### bouncing stone
					(val_div,"$stone_vertical_velocity",-2),
					(val_div,"$stone_horizontal_velocity",2),
					(val_add,"$stonelobbing_state",1),
				(else_try),												###### final rest
#					(display_message,"@DEBUG:STONE: missile hit final ground"),
					(assign,"$stonelobbing_state",0),
				(try_end),	
			(try_end)])
stonelobbing_carry_stone = (0,0,0, [(eq,"$stonelobbing_state",1)],
			[(get_player_agent_no,":player_agent"), (agent_get_position,pos6,":player_agent"),
			(position_move_z,pos6,170),
			(position_move_x,pos6,25), 
			(prop_instance_animate_to_position,"$stone_picked_instance",pos6,3),
			(agent_set_walk_forward_animation,":player_agent","anim_ready_carrystone")])			
################## STONELOBBING END ########################################

################## FLORA BEGIN ###########################################
scene_set_flora_init = (ti_before_mission_start,0,0,[],
	[(try_for_range,":pointer",0,20),
		(store_random_in_range,":object","spr_tree0_yellow_flower","spr_trees_end"),	# assign type of tree
		(troop_set_slot,"trp_temp_array_a",":pointer",":object"),
		(assign,":num",1),
		(try_for_range,":i",0,":pointer"),												# tree was previously assigned?
			(try_begin),(troop_slot_eq,"trp_temp_array_a",":i",":object"),(val_add,":num",1),(try_end),
		(try_end),
		(troop_set_slot,"trp_temp_array_b",":pointer",":num"),
		(store_add,":spr_pointer","spr_zz_pointer00",":pointer"),
		(replace_scene_props,":spr_pointer",":object"),
	(try_end)])
scene_set_flora_army_spawn = (0, 0, ti_once, [], [
	(get_scene_boundaries,pos1,pos2),
	(position_get_x,"$battlemap_min_x",pos1),
	(position_get_y,"$battlemap_min_y",pos1),
	(position_get_x,"$battlemap_max_x",pos2),
	(position_get_y,"$battlemap_max_y",pos2),
#	(val_add,"$battlemap_min_x",10),(val_sub,"$battlemap_max_x",10),
#	(val_add,"$battlemap_min_y",10),(val_sub,"$battlemap_max_y",10),
#	(store_mul,":center_spawn_min_x","$battlemap_min_x",1),(val_div,":center_spawn_min_x",4),	# center point btw 1/4 ans 3/4 of map boundaries
#	(store_mul,":center_spawn_max_x","$battlemap_max_x",3),(val_div,":center_spawn_max_x",4),
#	(store_mul,":center_spawn_min_y","$battlemap_min_y",1),(val_div,":center_spawn_min_y",4),
#	(store_mul,":center_spawn_max_y","$battlemap_max_y",3),(val_div,":center_spawn_max_y",4),
#	(store_random_in_range,":x0",":center_spawn_min_x",":center_spawn_max_x"),
#	(store_random_in_range,":y0",":center_spawn_min_y",":center_spawn_max_y"),

	(store_div,":x0","$battlemap_max_x",2),
	(store_div,":y0","$battlemap_max_y",2),
	(init_position, pos2),						# center point
	(position_set_x, pos2,":x0"),
	(position_set_y, pos2,":y0"),
	(store_random_in_range,":rotation",0,360),
	(position_rotate_z, pos2,":rotation"),

	(store_div,":delta","$battlemap_max_y",10),	# 2 delta from center in opposite diractions
	(copy_position, pos1, pos2),
	(position_move_y, pos1,":delta"),
	(position_rotate_z, pos1,180),				# player army spawn point
	(position_set_z_to_ground_level,pos1),
	#	(copy_position, pos2, pos10),
	(store_sub,":delta",0,":delta"),
	(position_move_y, pos2,":delta"),			# enemy army spawn point
	(position_set_z_to_ground_level,pos2),
	
	(try_for_agents,":agent"),
		(agent_is_human,":agent"),
		(agent_get_team,":team",":agent"),
		(agent_get_horse,":a",":agent"),
		(try_begin),							# assign appropriate teleport victim (horse for riders)
			(lt,":a",0),(assign,":a",":agent"),
		(try_end),
		(try_begin),							# teleport soldiers to respective starting positions
			(teams_are_enemies, ":team", 0),
			(agent_set_position,":a",pos2),	(position_move_x, pos2,50),
		(else_try),
			(agent_set_position,":a",pos1),	(position_move_x, pos1,50),
		(try_end),		
	(try_end),

################################ set up flora
	(store_div, ":max_a", "$battlemap_max_x", 10),		# ellipsoid min max dimensions
	(store_div, ":max_b", "$battlemap_max_y", 10),
	(store_div, ":min_a", "$battlemap_max_x", 32),
	(store_div, ":min_b", "$battlemap_max_y", 32),
	(try_for_range,":pointer",0,20),
		(store_random_in_range, ":a", ":min_a", ":max_a"),				# current ellipsoid dimensions
		(store_random_in_range, ":b", ":min_b", ":max_b"),
		(init_position, pos48),											# center of grove
		(store_random_in_range,":nx",3,30),(store_mul,":x0",":min_a",":nx"),(position_set_x, pos48,":x0"),
		(store_random_in_range,":ny",3,30),(store_mul,":y0",":min_b",":ny"),(position_set_y, pos48,":y0"),		
		(store_random_in_range,":ro",0,180),								(position_rotate_z, pos48,":ro"),

		(troop_get_slot,":spr_pointer","trp_temp_array_a",":pointer"),	# pointing towards repeating trees
		(troop_get_slot,":num","trp_temp_array_b",":pointer"),
		(store_mul,":n_max",20,":num"),
		(store_sub,":n_min",20,":n_max"),

		(try_for_range,":instance",":n_min",":n_max"),
			(store_random_in_range,":x",1,":a"),(store_random_in_range,":y",1,":b"),
#			(store_mul,":x",":x",100),(store_mul,":y",":y",100),
#			(store_div,":xx",":x",":a"),(store_mul,":xx",":xx",":xx"),
#			(store_div,":yy",":y",":b"),(store_mul,":yy",":yy",":yy"),
#			(store_add,":xx",":xx",":yy"),
			(try_begin),#(lt,":xx",100),								# position is inside ellips?
				(store_random_in_range,":xx",0,2),(try_begin),(eq,":xx",0),(store_sub,":x",0,":x"),(try_end),	#+-quadrant
				(store_random_in_range,":yy",0,2),(try_begin),(eq,":yy",0),(store_sub,":y",0,":y"),(try_end),
				(store_add,":xx",":x0",":x"),(store_add,":yy",":y0",":y"),
				(try_begin),
					(is_between,":xx","$battlemap_min_x","$battlemap_max_x"), 	# position is inside battlemap?
					(is_between,":yy","$battlemap_min_y","$battlemap_max_y"),
					(copy_position, pos1,pos48),
					(position_move_x,pos1,":x"),
					(position_move_y,pos1,":y"),
					(position_set_z_to_ground_level,pos1),
					(store_random_in_range,":rotation",0,360),
					(position_rotate_z, pos1,":rotation"),
					(scene_prop_get_instance,":object",":spr_pointer",":instance"),
					(prop_instance_set_position,":object",pos1),
#					(display_message,"@tree moved"),
#				(else_try),
#					(val_sub,":instance",1),			# tree not placed due to outta battlemap
				(try_end),
#			(else_try),
#				(val_sub,":instance",1),				# tree not placed due to outta ellips
			(try_end),
		(try_end),
	(try_end),
	(assign,reg0,"$battlemap_max_x"),
	(assign,reg1,"$battlemap_max_y"),	 
	(display_message,"@max X {reg0} max Y {reg1}"),
])
 

################# whistle for horse
horse_whistle_init = (0.2,0,ti_once,[],[(get_player_agent_no,":agent"),(agent_get_horse,"$player_horse",":agent")])
horse_whistle = (0,0,3,[(gt,"$player_horse",0),(key_clicked, key_m)],
    [ (get_player_agent_no,":player"),(display_message,"@You yell for your horse."),
      (agent_is_alive, "$player_horse"),(agent_get_position, pos9, ":player"),(agent_set_scripted_destination, "$player_horse", pos9, 0)])

##common_battle_kill_underwater = (
##  5, 0, 0, [],
##   [  (try_for_agents,":agent"),
##         (agent_is_alive,":agent"),
##         (agent_get_position,pos1,":agent"),
##         (position_get_z, ":pos_z", pos1),
##         #(assign, reg1, ":pos_z"), #debug only
##         #(display_message, "@agent z-position is {reg1}"),   #debug only
##         (try_begin),
##            (le, ":pos_z",-150),   #agent is about 6ft underwater
##            (store_agent_hit_points,":hp",":agent",1),
##            (val_sub,":hp",7),
##            (try_begin),
##               (le, ":hp", 0),
##               (agent_set_hit_points,":agent",0,0),
##            (else_try),
##               (agent_set_hit_points,":agent",":hp",1),
##            (try_end),            
##            (play_sound,"snd_man_grunt"),
##            (agent_deliver_damage_to_agent,":agent",":agent"),
##         (try_end),
##      (try_end),
##   ])


# dynamic fog in dungeons, governed by player triggering scene props (mtarini and GA)
dungeon_darkness_effect = (1, 0, 0, [(eq,"$dungeons_in_scene",1)], [ 
	(get_player_agent_no,":player"), 
    (agent_get_position,pos25,":player"),
 	(assign,":min_dist",200), # cycle through fog triggers, find closest one
	(assign,":min_pointer",-1),
    (try_for_range,":pointer","spr_light_fog_black0","spr_moria_rock"),
		(scene_prop_get_num_instances,":max_instance", ":pointer"),
		(ge,":max_instance", 1),
		(try_for_range,":instance_no",0,":max_instance"), # checking distance to player
			(scene_prop_get_instance, ":i", ":pointer", ":instance_no"),
			(ge, ":i", 0),
            (prop_instance_get_position,pos1,":i"),
            (get_distance_between_positions,":dist",pos1,pos25),
	        (le,":dist",":min_dist"),
			(assign, ":min_dist", ":dist"), 
			(assign, ":min_pointer", ":pointer"), 
        (try_end),
    (try_end),
	(try_begin), # setting fog thickness
		(neq,":min_pointer",-1),
		(try_begin),(eq,":min_pointer","spr_light_fog_black0"),(assign,reg11,10000), # 10000
		 (else_try),(eq,":min_pointer","spr_light_fog_black1"),(assign,reg11,120),# was 500
		 (else_try),(eq,":min_pointer","spr_light_fog_black2"),(assign,reg11,80), # was 200
		 (else_try),(eq,":min_pointer","spr_light_fog_black3"),(assign,reg11,40),  # was 120
		 (else_try),(eq,":min_pointer","spr_light_fog_black4"),(assign,reg11,20), # was 80
		 (else_try),(eq,":min_pointer","spr_light_fog_black5"),(assign,reg11,14), # was 20
		(try_end),
		(set_fog_distance,reg11,0x000001), 
		#(display_message, "@DEBUG: Fog distance: {reg11}"), 	
		(try_begin),(eq, reg11, 10000),(assign, "$player_is_inside_dungeon",0),
		 (else_try),				   (assign, "$player_is_inside_dungeon",1),
		(try_end),
	(try_end)])
	
common_battle_healing = (0, 0, ti_once, [(key_clicked, key_h)], [(call_script, "script_battle_health_management")])

### CWE flying birds, implemented by Ruthven

reward_birds_wb = ((is_a_wb_mt==1) and [ 
    #Three triggers:
    #T1 checks player inventory and spawns approptiate bird prop if needed 
    #T2 handles the vertex animation 
    #T3 handles the bird movement (position) 
    
    #These are adapted from CWE code; 
    # they used a custom GUI or something, 
    # so all the variables are numbered instead of named - readability is a bit of a pain
    
    (ti_after_mission_start, 0, 0, 
    [
    (this_or_next|player_has_item, "itm_crebain_reward"), #No birds if no items 
    (player_has_item, "itm_thrush_reward"),
    ],
    [
	(try_begin), #Spawn appropriate bird prop 
		(store_random_in_range, ":rot_x", -10, 10),
		#(store_random_in_range, ":rot_y", 0, 30),
		(try_begin),
            (get_player_agent_no, ":player"), #Use the player's spawn point as the starting point - could use map center etc  
            (agent_get_position, pos6, ":player"),
			(store_random_in_range, ":height", 700, 1500), #7-15m above ground 
			(position_move_z, pos6, ":height"),
			(position_rotate_x, pos6, ":rot_x"), 
			#(position_rotate_y, pos6, ":rot_y"),
			(set_spawn_position, pos6),
            (try_begin),
                (player_has_item, "itm_crebain_reward"), #Ruthven: if they have both items they only get this one - I'm assuming players never have both 
                (assign, ":birdprop", "spr_birds_crebain"),  #InVain: turned birdprop into a local var, we don't need it as a global
            (else_try),
                (player_has_item, "itm_thrush_reward"),
                (assign, ":birdprop", "spr_birds_thrush"),
            (try_end),
			(spawn_scene_prop, ":birdprop"),
        #  (scene_prop_set_slot, reg0, 44, ":var0"),
          (prop_instance_enable_physics, reg0, 0),
			#(display_message, "@birb"),
		(try_end),
	(try_end),
	]),

    (0.1, 0, 0,  #change refresh rate to alter wing speed - copy trigger for separate bird speeds 
    [
	(store_mission_timer_b_msec, ":cur_time"),
	(gt, ":cur_time", 500), #1/2 second grace period 
      (set_fixed_point_multiplier, 100),
      (assign, ":var0", 0),
      (try_begin), 
        #using global var for bird prop; if we validate player_has_item here it will stop animating if they discard it!
        #(assign, ":var1", "$birdprop"),
		(try_for_range, ":var1", "spr_birds_crebain", "spr_birds_end"), #InVain: So it also detects pre-palced bird props in scenes, not only those spawned from reward items
            
        (scene_prop_get_num_instances, ":var2", ":var1"),
        (ge, ":var2", 1),
        (try_for_range, ":var3", 0, ":var2"),
          (scene_prop_get_instance, ":var4", ":var1", ":var3"),
          (scene_prop_slot_eq, ":var4", 41, 0),
          (scene_prop_get_slot, ":var5", ":var4", 37),
          (prop_instance_deform_to_time, ":var4", ":var5"),
          (val_add, ":var5", 1),
          (try_begin),
            (ge, ":var5", 26),
            (assign, ":var5", 1),
          (try_end),
          (scene_prop_set_slot, ":var4", 37, ":var5"),
        (try_end),
      (else_try),
        (assign, ":var0", 1),
      (try_end),
      (eq, ":var0", 1),
       (try_begin),
       # # (eq, "$cheat_mode_sa", 1),
         #(display_message, "@{!}DEBUG -- vertex keys woron END (stage no animated crows)"),
       (try_end),
	   (try_end),
    ],
    []),


    (0.1, 0, ti_once, 
    [
	(store_mission_timer_b_msec, ":cur_time"),
	(gt, ":cur_time", 500), #1/2 second grace period 
      (set_fixed_point_multiplier, 100),
      (assign, ":var0", 1),
      (try_begin),
        # (eq, "$g_disable_flying_birds", 1),
      # (else_try),
        (try_for_range, ":var1", "spr_birds_crebain", "spr_birds_end"), 
          (scene_prop_get_num_instances, ":var2", ":var1"),
          (ge, ":var2", 1),
          (assign, ":var0", 0),
          (try_for_range, ":var3", 0, ":var2"),
            (scene_prop_get_instance, ":var4", ":var1", ":var3"),
            (try_begin),
              (scene_prop_slot_eq, ":var4", 41, 0),
              (try_begin),
                (try_begin),
                  (scene_prop_get_slot, ":var5", ":var4", 44),
                  (ge, ":var5", 0),
                  (prop_instance_get_position, pos1, ":var5"),
                (else_try),
                  (prop_instance_get_starting_position, pos1, ":var4"),
                (try_end),
                (try_begin),
                  (prop_instance_get_position, pos2, ":var4"),
                  (get_distance_between_positions, ":var6", pos2, pos1),
                  (le, ":var6", 200),
                  (try_begin),
                    (neg|scene_prop_slot_eq, ":var4", 45, 1),
                    (position_move_z, pos2, 700),
                  (try_end),
                  (position_move_x, 2, 4000),
                  (prop_instance_set_position, ":var4", pos2),
                  (prop_instance_enable_physics, ":var4", 1),
                (try_end),
                (assign, ":var7", 1),
                (try_begin),
                  (prop_instance_is_animating, ":var8", ":var4"),
                  (eq, ":var8", 1),
                  (assign, ":var7", 0),
                  (prop_instance_get_position, pos3, ":var4"),
                  (prop_instance_get_animation_target_position, 2, ":var4"),
                  (get_distance_between_positions, ":var9", pos2, pos3),
                  (le, ":var9", 50),
                  (assign, ":var7", 1),
                (try_end),
                (eq, ":var7", 1),
                (scene_prop_get_slot, ":var10", ":var4", 38),
                (scene_prop_get_slot, ":var11", ":var4", 39),
                (val_add, ":var10", 30),
                (position_rotate_z, pos1, ":var10"),
                (position_move_x, 1, 4000),
                (try_begin),
                  (neg|scene_prop_slot_eq, ":var4", 45, 1),
                  (store_add, ":var12", 700, ":var11"),
                (else_try),
                  (assign, ":var12", ":var11"),
                (try_end),
                (position_move_z, pos1, ":var12"),
                (try_begin),
                  (position_get_distance_to_terrain, ":var13", pos1),
                  (store_div, ":var14", 700, 2),
                  (this_or_next|ge, 0, ":var13"),
                  (ge, ":var14", ":var13"),
                  (position_set_z_to_ground_level, pos1),
                  (position_move_z, pos1, ":var12"),
                (try_end),
                (prop_instance_get_position, pos2, ":var4"),
                (get_distance_between_positions, ":var15", pos2, pos1),
                (val_div, ":var15", 9),
                (prop_instance_animate_to_position, ":var4", pos1, ":var15"),
                (try_begin),
                  (ge, ":var10", 360),
                  (assign, ":var10", 0),
                  (store_random_in_range, ":var11", 0, 16),
                  (val_mul, ":var11", 80),
                  (scene_prop_set_slot, ":var4", 39, ":var11"),
                (try_end),
                (scene_prop_set_slot, ":var4", 38, ":var10"),
              (try_end),
            (else_try), #Dead birds - currently unused 
              (scene_prop_slot_eq, ":var4", 41, 1),
              (set_fixed_point_multiplier, 100),
              (position_set_x, pos0, 2500),
              (position_set_y, pos0, 80),
              (position_set_z, pos0, 0),
              (prop_instance_dynamics_set_properties, ":var4", 0),
              (position_set_x, pos0, 0),
              (position_set_y, pos0, 0),
              (position_set_z, pos0, -800),
              (prop_instance_dynamics_set_omega, ":var4", 0),
              (try_begin),
                (prop_instance_get_position, pos1, ":var4"),
               # (particle_system_burst, "psys_hit_bird_blood", pos1, 1),
               # (particle_system_burst, "psys_hit_bird_feathers", pos1, 1),
                (position_get_distance_to_terrain, ":var15", pos1),
                (le, ":var15", 100),
                (position_get_rotation_around_z, ":var10", pos1),
                #(position_align_to_ground, pos1, 1, 1),
                (position_rotate_x, pos1, -90),
                (position_rotate_z, pos1, ":var10"),
                (prop_instance_enable_physics, ":var4", 0),
                (prop_instance_set_position, ":var4", pos1),
                (position_move_z, pos1, -1),
                (prop_instance_animate_to_position, ":var4", pos1, 100000000),
                (scene_prop_set_slot, ":var4", 41, 2),
                (scene_prop_get_slot, ":var16", ":var4", 43),
                (prop_instance_deform_to_time, ":var4", ":var16"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
      (eq, ":var0", 1),
      # (try_begin),
       # # (eq, "$cheat_mode_sa", 1),
        # (assign, "$g_mission_cam_set_bird_target", -2),
        # (display_message, "@{!}DEBUG -- animation of flight END (stage no animated birds)", 0x00005500),
      # (try_end),
    ],
    [])
	] or [])
	
# ( "custom_battle_football",mtf_battle_mode,-1,
    # "The match starts in a minute!",
    # [
		# (0, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (1, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (2, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (3, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (4, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (5, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (6, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a,itm_lossarnach_cloth_cap]),
		# (7, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),

		# (16,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a,itm_lossarnach_cloth_cap]),
		# (17,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (18,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (19,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (20,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (21,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),
		# (22,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_leather_boots,itm_white_tunic_a]),

     # ],
    # [
      # common_custom_battle_tab_press,
      # common_custom_battle_question_answered,
      # common_inventory_not_available,
      # common_music_situation_update,
      # custom_battle_check_victory_condition,
      # common_battle_victory_display,
      # custom_battle_check_defeat_condition,

    # (0, 0, ti_once,
       # [ (assign, "$defender_team", 0),
         # (assign, "$attacker_team", 1), # (display_message,"@DEBUG: mission template football"),
#         (assign, "$defender_team_2", 3),
#         (assign, "$attacker_team_2", 2),
       # ], []),
################## FOOTBALL BEGIN ############################################
		# football_init,
		# football_kick_ball,
		# football_fly_ball,				
	# ],
# ),
