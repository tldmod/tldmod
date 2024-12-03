from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *

from module_info import wb_compile_switch as is_a_wb_mt

#MV: commented out - not used and ctrl-h already works this way (standard MB cheat)
# cheat_heal_self_on_ctrl_h = (0.5,0,2,[
    # (eq, "$cheat_mode",1),(key_is_down, key_h),(this_or_next|key_is_down, key_left_control),(key_is_down, key_right_control),
    # (get_player_agent_no, ":player_agent"),
	# (agent_set_hit_points , ":player_agent",100,0),
	# (display_message, "@{!}CHEAT: healed!!! (ctrl+h)"),
  # ], [ ]
# )

#MV: commented out - not used and if used will interfere with formation keys
################################ set up fog on a scene
scene_init_fog =(0, 0, ti_once,[],[
	(assign,"$fog_red"  , 255),
	(assign,"$fog_green", 255),
	(assign,"$fog_blue" , 255),
	(assign,"$fog_dist" ,1000),
	])
 
scene_set_fog = (0, 0, 0.5,
	[(this_or_next|key_clicked, key_o),	(this_or_next|key_clicked, key_l),
	 (this_or_next|key_clicked, key_i),	(this_or_next|key_clicked, key_k),
	 (this_or_next|key_clicked, key_u),	(this_or_next|key_clicked, key_j),
	 (this_or_next|key_clicked, key_y),	(key_clicked, key_h),
	],[
	(try_begin),(key_is_down, key_left_shift),	(assign, ":move_val", 50),
    (else_try),									(assign, ":move_val", 5),
    (try_end),
        
	(try_begin),(key_clicked, key_o),(val_add,"$fog_blue" ,":move_val"),
    (else_try),	(key_clicked, key_l),(val_sub,"$fog_blue" ,":move_val"),
    (else_try),	(key_clicked, key_i),(val_add,"$fog_green",":move_val"),
    (else_try),	(key_clicked, key_k),(val_sub,"$fog_green",":move_val"),
    (else_try),	(key_clicked, key_u),(val_add,"$fog_red"  ,":move_val"),
    (else_try),	(key_clicked, key_j),(val_sub,"$fog_red"  ,":move_val"),
	(else_try),	(key_clicked, key_y),(val_add,"$fog_dist" ,100),
	(else_try),	(key_clicked, key_h),(val_sub,"$fog_dist" ,100),
    (try_end),
	
	(try_begin),(lt,"$fog_red",  0),(assign,"$fog_red",  0),
	(else_try), (gt,"$fog_red",255),(assign,"$fog_red",255),
	(try_end),
	(try_begin),(lt,"$fog_green",  0),(assign,"$fog_green",  0),
	(else_try), (gt,"$fog_green",255),(assign,"$fog_green",255),
	(try_end),
	(try_begin),(lt,"$fog_blue",  0),(assign,"$fog_blue",  0),
	(else_try), (gt,"$fog_blue",255),(assign,"$fog_blue",255),
	(try_end),
	(try_begin),(lt,"$fog_dist",  0),(assign,"$fog_dist",  0),(try_end),
	
	(store_mul,"$fog_color","$fog_red",256),
	(store_add,"$fog_color","$fog_color","$fog_green"),
	(store_mul,"$fog_color","$fog_color",256),
	(store_add,"$fog_color","$fog_color","$fog_blue"),
	(set_fog_distance, "$fog_dist", "$fog_color"),
	(assign,reg0,"$fog_red"),
	(assign,reg1,"$fog_green"),	
	(assign,reg2,"$fog_blue"),	
	(assign,reg3,"$fog_dist"),	
	(display_message,"@FOG:R {reg0} G {reg1} B{reg2} dist {reg3}"),
	])
################## FOOTBALL BEGIN ############################################
################## uses spr_stoneball ########################################
################## pos48 - ball prop, pos49 - ball position ##################
football_init =	(0, 0, ti_once, [],[
			(set_fixed_point_multiplier,10),
			(assign,"$stone_velocity_x",0),
			(assign,"$stone_velocity_y",0),
			(assign,"$stone_velocity_z",20),
			(assign,"$stone_rotation_x",0),				###### ball rotation speed in flight
			(assign,"$stone_rotation_y",0),
			(assign,"$stone_rotation_z",5),
			(assign,"$min__x",0),(assign,"$min__y",0),(assign,"$max__x",0),(assign,"$max__y",0),
			(scene_prop_get_instance,"$stone_picked_instance", "spr_football_ball", 0),
			(prop_instance_get_position,pos48,"$stone_picked_instance"),
			(copy_position,pos49,pos48),

			(scene_prop_get_instance,":b", "spr_arena_barrier_a", 0),(prop_instance_get_position,pos1,":b"),(position_get_y,":y0",pos1),			
			(scene_prop_get_instance,":b", "spr_arena_barrier_a", 1),(prop_instance_get_position,pos1,":b"),(position_get_y,":y1",pos1),
			(try_begin),(gt,":y0",":y1"),(assign,"$max__y",":y0"),(assign,"$min__y",":y1"),
			(else_try),					 (assign,"$max__y",":y1"),(assign,"$min__y",":y0"),
			(try_end),
			(scene_prop_get_instance,":b", "spr_arena_palisade_a",0),(prop_instance_get_position,pos1,":b"),(position_get_x,":x0",pos1),	
			(scene_prop_get_instance,":b", "spr_arena_palisade_a",1),(prop_instance_get_position,pos1,":b"),(position_get_x,":x1",pos1),
			(try_begin),(gt,":x0",":x1"),(assign,"$max__x",":x0"),(assign,"$min__x",":x1"),
			(else_try),					 (assign,"$max__x",":x1"),(assign,"$min__x",":x0"),
			(try_end),
#			(gt,"$max__y","$min__y"),(display_message,"@Y stored ok"),
#			(gt,"$max__x","$min__x"),(display_message,"@X stored ok"),
])

football_kick_ball = (0,0,1, [(key_clicked, key_e),										###### kick the ball
			],
			[(get_player_agent_no,":player_agent"),
			(agent_get_look_position,pos1,":player_agent"),
#			(position_rotate_z,pos1,135),								####### ball inside forward angle cone
#			(position_is_behind_position,pos1,pos49),
#			(position_rotate_z,pos1,135),
#			(position_is_behind_position,pos1,pos49),
			(get_distance_between_positions,":distance",pos1,pos49),
			(lt,":distance",100),
#				(position_rotate_z,pos1,90),
				(store_random_in_range,"$stone_velocity_x",-60,60),
				(store_random_in_range,"$stone_velocity_y",-60,60),
				(assign,"$stone_velocity_z",20),
#				(agent_set_walk_forward_animation,":player_agent", "anim_reload_crossbow"),
				(play_sound, "snd_man_grunt"),
			
			(assign,reg0,"$max__x"),(assign,reg1,"$min__x"),(display_message,"@DEBUG:borders Xmin:{reg1} Xmax{reg0}"),
			(assign,reg0,"$max__y"),(assign,reg1,"$min__y"),(display_message,"@DEBUG:borders Ymin:{reg1} Ymax{reg0}"),			
])
			
football_fly_ball = (0.1,0,0, [],															###### ball movement
			[
			(position_get_x,":x0",pos49),					###### bouncing from field borders
			(store_add,":x1",":x0","$stone_velocity_x"),
			(try_begin),
				(lt,":x1","$min__x"),
				(lt,"$stone_velocity_x",0),
				(store_sub,"$stone_velocity_x",0,"$stone_velocity_x"),
				(play_sound, "snd_incoming_stone_hit_ground"),
				(assign,reg0,":x0"),
				(display_message,"@ball X:{reg0}"),
			(else_try),
				(gt,":x1","$max__x"),
				(gt,"$stone_velocity_x",0),
				(store_sub,"$stone_velocity_x",0,"$stone_velocity_x"),
				(play_sound, "snd_incoming_stone_hit_ground"),
				(assign,reg0,":x0"),
				(display_message,"@ball X:{reg0}"),
			(try_end),
			
			(position_get_y,":y0",pos49),
			(store_add,":y1",":y0","$stone_velocity_y"),
			(try_begin),
				(lt,":y1","$min__y"),(lt,":y1",":y0"),
				(store_sub,"$stone_velocity_y",0,"$stone_velocity_y"),
				(play_sound, "snd_incoming_stone_hit_ground"),
				(assign,reg0,":y0"),
				(display_message,"@ball Y:{reg0}"),
			(else_try),
				(gt,":y1","$max__y"),(gt,":y1",":y0"),
				(store_sub,"$stone_velocity_y",0,"$stone_velocity_y"),
				(play_sound, "snd_incoming_stone_hit_ground"),
				(assign,reg0,":y0"),
				(display_message,"@ball Y:{reg0}"),
			(try_end),
#			(assign,reg0,":x0"),(assign,reg1,":y0"),
#			(display_message,"@ball X:{reg0} Y:{reg1}"),
						
			(position_get_z,":z0",pos49),					###### bouncing from field
			(try_begin),
				(lt,":z0",5),
				(lt,"$stone_velocity_z",0),
				(val_div,"$stone_velocity_z",-2),
				(val_mul,"$stone_velocity_x",10),(val_div,"$stone_velocity_x",11),
				(val_mul,"$stone_velocity_y",10),(val_div,"$stone_velocity_y",11),
				(gt,"$stone_velocity_z",10),(play_sound, "snd_incoming_stone_hit_ground"),
			(try_end),
			
			(position_move_x, pos49,"$stone_velocity_x"),(position_move_y, pos49, "$stone_velocity_y"),(position_move_z, pos49, "$stone_velocity_z"),
			(val_sub,"$stone_velocity_z",1),
			(position_copy_origin,pos48,pos49),								###### stone rotation
			(position_rotate_x,pos48,"$stone_rotation_x"),(position_rotate_y,pos48,"$stone_rotation_y"),(position_rotate_z,pos48,"$stone_rotation_z"),
			(prop_instance_animate_to_position,"$stone_picked_instance",pos48,10),
])

########### Custom 3d person view camera			
custom_commander_camera = (0, 0, 0.5, [],
      [ (get_player_agent_no, ":player_agent"),
        (agent_get_look_position, pos1, ":player_agent"),
        (position_move_z, pos1, "$g_camera_z"),(position_move_y, pos1, "$g_camera_y"),
        (agent_get_horse, ":horse_agent", ":player_agent"),
        (try_begin),
          (ge, ":horse_agent", 0),
          (position_move_z, pos1, 80),
        (try_end),
        (mission_cam_set_position, pos1),
        
		(try_begin),(key_is_down, key_right_control),(assign, ":move_val", 50),
        (else_try),									 (assign, ":move_val", 10),
        (try_end),
        
		(try_begin),(key_clicked, key_up),		(mission_cam_set_mode, 1),(val_add, "$g_camera_z", ":move_val"),
        (else_try),	(key_clicked, key_down),	(mission_cam_set_mode, 1),(val_sub, "$g_camera_z", ":move_val"),
        (else_try),	(key_clicked, key_left),	(mission_cam_set_mode, 1),(val_add, "$g_camera_y", ":move_val"),
        (else_try),	(key_clicked, key_right),	(mission_cam_set_mode, 1),(val_sub, "$g_camera_y", ":move_val"),
        (try_end),
        
		(try_begin),
		  (this_or_next|key_is_down, gk_zoom),
          (this_or_next|game_key_clicked, gk_view_char),
          (game_key_clicked, gk_cam_toggle),
          (mission_cam_set_mode, 0),
        (try_end),
      ])
	  
#test_val_and = (0, 0, 0.5,[(key_clicked, key_p)],[(assign, reg30, "$mask"),(assign, reg31, "$mask"),(val_and, reg31 ,512),(display_message,"@Mask: {reg30} Result: {reg31}"),(val_mul,"$mask",2)])

########## Vanilla siege and tournament triggers


common_custom_siege_init = (0, 0, ti_once, [],
  [ (assign, "$g_battle_result", 0),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_siege),
  ])

common_siege_ai_trigger_init_2 = (0, 0, ti_once,
  [ (set_show_messages, 0),
    (entry_point_get_position, pos10, 41), #TLD, was 10
    (team_give_order, "$defender_team", grc_infantry, mordr_hold),
    (team_give_order, "$defender_team", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team", grc_archers, mordr_stand_ground),
    (team_set_order_position, "$defender_team", grc_everyone, pos10),
    (team_give_order, "$defender_team_2", grc_infantry, mordr_hold),
    (team_give_order, "$defender_team_2", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team_2", grc_infantry, mordr_stand_closer),
    (team_give_order, "$defender_team_2", grc_archers, mordr_stand_ground),
    (team_set_order_position, "$defender_team_2", grc_everyone, pos10),
    (set_show_messages, 1),
    ], [])


common_siege_attacker_do_not_stall = (5, 0, 0, [],
  [ (try_for_agents, ":agent_no"),   #Make sure attackers do not stall on the ladders...
      (agent_is_human, ":agent_no"),
      (agent_is_alive, ":agent_no"),
      (agent_get_team, ":agent_team", ":agent_no"),
      (this_or_next|eq, ":agent_team", "$attacker_team"),(eq, ":agent_team", "$attacker_team_2"),
      (agent_ai_set_always_attack_in_melee, ":agent_no", 1),
    (try_end),
    ])


common_siege_init_ai_and_belfry   = (0, 0, ti_once,[(call_script, "script_siege_init_ai_and_belfry")],[])
common_siege_move_belfry          = (0, 0, ti_once,[(call_script, "script_cf_siege_move_belfry")], [])
common_siege_rotate_belfry        = (0, 2, ti_once,[(call_script, "script_cf_siege_rotate_belfry_platform")],[(assign, "$belfry_positioned", 3)])
common_siege_assign_men_to_belfry = (0, 0, ti_once,[(call_script, "script_cf_siege_assign_men_to_belfry")], [])

tournament_triggers = [
  (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest"),
                                       (assign, "$g_arena_training_num_agents_spawned", 0)]),
  (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_arena")], []),
  (ti_tab_pressed, 0, 0, [],
   [(try_begin),
      (eq, "$g_mt_mode", abm_visit),
      (set_trigger_result, 1),
    (else_try),
      (question_box,"str_give_up_fight"),
    (try_end),
    ]),
  (ti_question_answered, 0, 0, [],
   [(store_trigger_param_1,":answer"),
    (eq,":answer",0),
    (finish_mission,0),
    ]),

  (1, 0, ti_once, [], [
      (eq, "$g_mt_mode", abm_visit),
      (call_script, "script_music_set_situation_with_culture", mtf_sit_travel),
      (store_current_scene, reg(1)),
      (scene_set_slot, reg(1), slot_scene_visited, 1),
      (mission_enable_talk),
      (get_player_agent_no, ":player_agent"),
      (assign, ":team_set", 0),
      (try_for_agents, ":agent_no"),
        (neq, ":agent_no", ":player_agent"),
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (is_between, ":troop_id", regular_troops_begin, regular_troops_end),
        (eq, ":team_set", 0),
        (agent_set_team, ":agent_no", 1),
        (assign, ":team_set", 1),
      (try_end),
    ]),
  
  (0, 0, ti_once, [],
   [
     (eq, "$g_mt_mode", abm_tournament),
     #(play_sound, "snd_arena_ambiance", sf_looping),
     (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
     ]),


  (0, 0, ti_once, [], [(eq, "$g_mt_mode", abm_training),(start_presentation, "prsnt_arena_training")]),
  (0, 0, ti_once, [], [(eq, "$g_mt_mode", abm_training),
                       (assign, "$g_arena_training_max_opponents", 40),
                       (assign, "$g_arena_training_num_agents_spawned", 0),
                       # (assign, "$g_arena_training_kills", 0),
                       # (assign, "$g_arena_training_won", 0),
                       (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
                       ]),

  (1, 4, ti_once, [(eq, "$g_mt_mode", abm_training),
                   (store_mission_timer_a, ":cur_time"),
                   (gt, ":cur_time", 3),
                   (assign, ":win_cond", 0),
                   (try_begin),
                     (ge, "$g_arena_training_num_agents_spawned", "$g_arena_training_max_opponents"),#spawn at most 40 agents
                     (num_active_teams_le, 1),
                     (assign, ":win_cond", 1),
                   (try_end),
                   (this_or_next|eq, ":win_cond", 1),
                   (main_hero_fallen)],
   [
       # (get_player_agent_no, ":player_agent"),
       # (agent_get_kill_count, "$g_arena_training_kills", ":player_agent", 1),#use this for conversation
       # (assign, "$g_arena_training_won", 0),
       (try_begin),
         (neg|main_hero_fallen),
         # (assign, "$g_arena_training_won", 1),#use this for conversation
       (try_end),
       (assign, "$g_mt_mode", abm_visit),
       (set_jump_mission, "mt_arena_melee_fight"),
       (party_get_slot, ":arena_scene", "$current_town", slot_town_arena),
       (modify_visitors_at_site, ":arena_scene"),
       (reset_visitors),
       (set_visitor, 35, "trp_veteran_fighter"),
       #(set_visitor, 36, "trp_brigand_lieutenant"),
       (set_jump_entry, 50),
       (jump_to_scene, ":arena_scene"),
    ]),


  # (0.2, 0, 0,
   # [
       # (eq, "$g_mt_mode", abm_training),
       # (assign, ":num_active_fighters", 0),
       # (try_for_agents, ":agent_no"),
         # (agent_is_human, ":agent_no"),
         # (agent_is_alive, ":agent_no"),
         # (agent_get_team, ":team_no", ":agent_no"),
         # (is_between, ":team_no", 0 ,7),
         # (val_add, ":num_active_fighters", 1),
       # (try_end),
       # (lt, ":num_active_fighters", 7),
       # (neg|main_hero_fallen),
       # (store_mission_timer_a, ":cur_time"),
       # (this_or_next|ge, ":cur_time", "$g_arena_training_next_spawn_time"),
       # (this_or_next|lt, "$g_arena_training_num_agents_spawned", 6),
       # (num_active_teams_le, 1),
       # (lt, "$g_arena_training_num_agents_spawned", "$g_arena_training_max_opponents"),
      # ],
    # [
       # (assign, ":added_troop", "$g_arena_training_num_agents_spawned"),
       # (store_div,  ":added_troop", "$g_arena_training_num_agents_spawned", 6),
       # (assign, ":added_troop_sequence", "$g_arena_training_num_agents_spawned"),
       # (val_mod, ":added_troop_sequence", 6),
       # (val_add, ":added_troop", ":added_troop_sequence"),
       # (val_min, ":added_troop", 9),
       # (val_add, ":added_troop", "trp_arena_training_fighter_1"),
       # (assign, ":end_cond", 10000),
       # (get_player_agent_no, ":player_agent"),
       # (agent_get_position, pos5, ":player_agent"),
       # (try_for_range, ":unused", 0, ":end_cond"),
         # (store_random_in_range, ":random_entry_point", 32, 40),
         # (neq, ":random_entry_point", "$g_player_entry_point"), # make sure we don't overwrite player
         # (entry_point_get_position, pos1, ":random_entry_point"),
         # (get_distance_between_positions, ":dist", pos5, pos1),
         # (gt, ":dist", 1200), #must be at least 12 meters away from the player
         # (assign, ":end_cond", 0),
       # (try_end),
       # (add_visitors_to_current_scene, ":random_entry_point", ":added_troop", 1),
       # (store_add, ":new_spawned_count", "$g_arena_training_num_agents_spawned", 1),
       # (store_mission_timer_a, ":cur_time"),
       # (store_add, "$g_arena_training_next_spawn_time", ":cur_time", 14),
       # (store_div, ":time_reduction", ":new_spawned_count", 3),
       # (val_sub, "$g_arena_training_next_spawn_time", ":time_reduction"),
       # ]),

  (0, 0, 0, [(eq, "$g_mt_mode", abm_training)],
    [
       (assign, ":max_teams", 6),
       (val_max, ":max_teams", 1),
       (get_player_agent_no, ":player_agent"),
       (try_for_agents, ":agent_no"),
         (agent_is_human, ":agent_no"),
         (agent_is_alive, ":agent_no"),
         (agent_slot_eq, ":agent_no", slot_agent_arena_team_set, 0),
         (agent_get_team, ":team_no", ":agent_no"),
         (is_between, ":team_no", 0 ,7),
         (try_begin),
           (eq, ":agent_no", ":player_agent"),
           (agent_set_team, ":agent_no", 6), #player is always team 6.
         (else_try),
           (store_random_in_range, ":selected_team", 0, ":max_teams"),
          # find strongest team
           (try_for_range, ":t", 0, 6),
             (troop_set_slot, "trp_temp_array_a", ":t", 0),
           (try_end),
           (try_for_agents, ":other_agent_no"),
             (agent_is_human, ":other_agent_no"),
             (agent_is_alive, ":other_agent_no"),
             (neq, ":agent_no", ":player_agent"),
             (agent_slot_eq, ":other_agent_no", slot_agent_arena_team_set, 1),
             (agent_get_team, ":other_agent_team", ":other_agent_no"),
             (troop_get_slot, ":count", "trp_temp_array_a", ":other_agent_team"),
             (val_add, ":count", 1),
             (troop_set_slot, "trp_temp_array_a", ":other_agent_team", ":count"),
           (try_end),
           (assign, ":strongest_team", 0),
           (troop_get_slot, ":strongest_team_count", "trp_temp_array_a", 0),
           (try_for_range, ":t", 1, 6),
             (troop_slot_ge, "trp_temp_array_a", ":t", ":strongest_team_count"),
             (troop_get_slot, ":strongest_team_count", "trp_temp_array_a", ":t"),
             (assign, ":strongest_team", ":t"),
           (try_end),
           (store_random_in_range, ":rand", 5, 100),
           (try_begin),
             (lt, ":rand", "$g_arena_training_num_agents_spawned"),
             (assign, ":selected_team", ":strongest_team"),
           (try_end),
           (agent_set_team, ":agent_no", ":selected_team"),
         (try_end),
         (agent_set_slot, ":agent_no", slot_agent_arena_team_set, 1),
         (try_begin),
           (neq, ":agent_no", ":player_agent"),
           (val_add, "$g_arena_training_num_agents_spawned", 1),
         (try_end),
       (try_end),
       ]),
  ]


# mtarini nazgul sweeps. improved by cppcoder.
nazgul_sweeps = (4,1.2,5,[
	#(this_or_next|key_is_down, key_n),
	(gt,"$nazgul_in_battle",0),
    (eq, 0, 1), #disabled
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
		#(display_log_message, "@{!}Debug: LONG sweep!"),
	(else_try),
		(agent_play_sound, ":player_agent", "snd_nazgul_skreech_short"),
		#(display_log_message, "@{!}Debug: SHORT sweep!"),
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

#Kham: Actual Nazgul troop fighting
nazgul_attack = (20, 0, ti_once, [
      (gt, "$nazgul_in_battle", 1), #Has to be 2 nazgul

      (store_mission_timer_a, ":mission_time_a"),
      (store_random_in_range, ":ran_time", 45, 60),
      (ge, ":mission_time_a", ":ran_time"), #Random time between 45 - 60 secs

      (store_random_in_range, ":random", 0, 100),
      (store_faction_of_party, ":faction", "p_main_party"),
      (faction_get_slot, ":side", ":faction", slot_faction_side),

      (le, ":random", 40), #40% Chance every 20 seconds

      (try_begin),
        (eq, ":side", faction_side_good),
        (assign, ":color", color_bad_news),
      (else_try),
        (eq, "$tld_war_began", 2),
        (eq, ":side", faction_side_hand),
        (assign, ":color", color_bad_news),
      (else_try),
        (assign, ":color", color_good_news),
      (try_end),


      (display_message, "@A Nazgul has joined the battle!", ":color"),
      (str_store_string, s30, "@Feeeeel.....ourrr.....wraaaath!"),
      (call_script, "script_troop_talk_presentation", "trp_nazgul", 7, 0),

      (get_player_agent_no, ":player"),
      (call_script, "script_find_exit_position_at_pos4", ":player"),
      (set_spawn_position, pos4), 

      (spawn_agent, "trp_nazgul"),
      (assign, "$temp2", reg0), #Save the nazgul agent
      (agent_set_team, "$temp2", 2),
      (agent_get_horse, ":nazgul_horse", "$temp2"),
      (agent_set_slot, ":nazgul_horse", slot_agent_hp_shield_active, 1),
      (agent_set_slot, ":nazgul_horse", slot_agent_hp_shield, 100000),
      (team_set_relation, 2, "$nazgul_team", 1),
      (agent_get_team, ":player_team", ":player"),
      (team_set_relation, ":player_team", 2, -1),
      (set_show_messages, 0),
      (team_give_order, 2, grc_everyone, mordr_charge),
      (set_show_messages, 1),

      ],

      [ (store_mission_timer_a, ":mission_time_a"),
        (agent_set_slot, "$temp2", slot_nazgul_timer, ":mission_time_a"),
        (set_show_messages, 0),
        (team_give_order, 2, grc_everyone, mordr_charge),
        (set_show_messages, 1),
    ])

nazgul_run_away = (20, 0, ti_once,
    [ 
      (gt, "$nazgul_in_battle", 1), #Has to be 2 nazgul
      
      (agent_is_active, "$temp2"),

      (store_mission_timer_a, ":mission_time_a"),
      (agent_get_slot, ":time_active", "$temp2", slot_nazgul_timer),
      (val_add, ":time_active", 60),
      (agent_get_kill_count, ":kills", "$temp2"),
      (this_or_next|ge, ":mission_time_a", ":time_active"),
      (ge, ":kills", 10),
    ],

    [
      (call_script, "script_find_exit_position_at_pos4", "$temp2"),
      (agent_start_running_away, "$temp2", pos4),
      (agent_set_scripted_destination_no_attack, "$temp2", pos4),

      (store_faction_of_party, ":faction", "p_main_party"),
      (faction_get_slot, ":side", ":faction", slot_faction_side),

      (try_begin),
        (eq, ":side", faction_side_good),
        (assign, ":color", color_bad_news),
      (else_try),
        (eq, "$tld_war_began", 2),
        (eq, ":side", faction_side_hand),
        (assign, ":color", color_bad_news),
      (else_try),
        (assign, ":color", color_good_news),
      (try_end),


      (display_message, "@The Nazgul is leaving the battle.", ":color"),
      (str_store_string, s30, "@It......Beckonsssss....."),
      (call_script, "script_troop_talk_presentation", "trp_nazgul", 7, 0),

    ])
################################################################################

  #mission_templates_unneeded = [  ]