from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *

cheat_kill_self_on_ctrl_s = ( 1,1.5,1.5,
[
    (eq, "$cheat_mode",1),
	(key_is_down, key_s),(this_or_next|key_is_down, key_left_control),(key_is_down, key_right_control),
    (get_player_agent_no, ":player_agent"),
	(agent_get_team, ":player_team", ":player_agent"),
	(display_message, "@CHEAT: SELF mind blast!!! (ctrl+s)"),
    (try_for_agents, ":agent"),
        (agent_get_team, reg10, ":agent"), (neg|teams_are_enemies , reg10, ":player_team"),
		(agent_get_horse,":horse",":agent"),
		(try_begin), (gt, ":horse", -1), 
			(agent_set_animation, ":agent", "anim_nazgul_noooo_mounted_short"), 
			(agent_set_animation, ":horse", "anim_horse_rear"), 
		(else_try),
			(agent_set_animation, ":agent", "anim_nazgul_noooo_short"), 
		(try_end),
	(end_try),
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
	(end_try),
	(set_show_messages , 1),

	]
)

custom_tld_init_battle = (ti_before_mission_start,0,0,[],
  [
	(assign,"$trolls_in_battle",0),	
	(assign,"$nazgul_in_battle",0),	
	(assign,"$wargs_in_battle",0),	
	(assign, "$nazgul_team", -1), # will be found when needed
	(try_begin),
		(this_or_next|eq, "$g_encountered_party", "pt_mordor_war_party"),
		(eq, "$g_encountered_party_2", "pt_mordor_war_party"),
		(store_random_in_range,":die_roll",101),	
		(try_begin),
			(gt, ":die_roll", 95),
			(assign,"$nazgul_in_battle",3),	
			(display_log_message, "@Three Nazguls are circling in the sky above the battlefield!"),
		(else_try),
			(gt, ":die_roll", 70),
			(assign,"$nazgul_in_battle",2),	
			(display_log_message, "@Two Nazguls are circling in the sky above the battlefield!"),
		(else_try),
			(gt, ":die_roll", 5),
			(assign,"$nazgul_in_battle",1),	
			(display_log_message, "@A Nazgul is circling in the sky above the battlefield!"),
		(try_end),
	(try_end),
  ]
)

custom_tld_spawn_troop = (ti_on_agent_spawn, 0, 0, [],
  [
    (store_trigger_param_1, ":agent"),
    (try_begin),
	  (assign, ":troll", ":agent"),
	  (agent_get_troop_id,reg0,":troll"),
	  (troop_get_type, reg0, reg0),
	  (eq, reg0, tf_troll),
	  (agent_set_speed_limit,":troll",4),	# trolls go 4 km/h max <GA>
	  (assign,"$trolls_in_battle",1),	# condition on future troll triggers
	  (agent_set_walk_forward_animation,":troll","anim_walk_forward_troll"),
	  # troll gets x4 hp
	  #(store_agent_hit_points,reg0,":troll",1),
	  #(store_mul,":hp",4,":hp"),
	  #(agent_set_hit_points ,":troll",":hp",1),
	  #(assign, reg0, ":hp"),
	  #(display_message,"@DEBUG: troll spawned with {reg0} hitpoints!"),
	  (agent_set_stand_animation,":troll","anim_walk_forward_troll"),
	(try_end),
	(try_begin),
		(agent_get_item_id, ":warg_item", ":agent"),
		(is_between, ":warg_item", item_warg_begin , item_warg_end),
		(val_add,"$wargs_in_battle",1),
	(try_end),
  ]
)

# mtarini nazgul sweeps 
nazgul_sweeps = (2,1.2,5,
  [  
	(this_or_next|key_is_down, key_n),
	(gt,"$nazgul_in_battle",0),
	(store_random_in_range,reg0,1,51),
   
	(this_or_next|key_is_down, key_n),
	(le,reg0,"$nazgul_in_battle"), # 2% chance every 2 seconds, for each nazgul present

	(display_log_message, "@Nazgul sweep!"),
			
	# if nazgul team is not computed, compute it
	(try_begin),
		(eq, "$nazgul_team", -1), 
		(try_for_agents,":agent"),
			(neg|eq, "$nazgul_team", -1), # stop when found
			(agent_get_party_id, ":party_id", ":agent"),
			(eq, ":party_id", "pt_mordor_war_party"),
			(agent_get_team, "$nazgul_team",":agent"),
		(try_end),
	(try_end),
	
	# choose long or short skretch
	(store_random_in_range, ":long_skretch", 0,2),
	
	# play sound
	(try_begin),
		(ge,":long_skretch",1),
		(play_sound, "snd_nazgul_skreech_long"),
		#(display_log_message, "@Debug: LONG sweep!"),
	(else_try), 
		(play_sound, "snd_nazgul_skreech_short"),
		#(display_log_message, "@Debug: SHORT sweep!"),
	(try_end), 
	 
	(get_player_agent_no, ":player_agent"), #for messages
			
	# psycological effect:
	(try_for_agents,":victim"),
		(agent_is_alive,":victim"),
		(agent_get_team, reg1, ":victim"),
		
		(this_or_next|eq, "$nazgul_team", -1),
		(teams_are_enemies, reg1, "$nazgul_team"),
		
		(agent_is_human,":victim"),

		# long skretch can make the horse rage twice (but only 66% of times)
		(try_begin), 
			(assign, ":horse_rage_twice",":long_skretch"),
			(store_random_in_range,":die_roll",1,4),
			(eq,":die_roll",1),		
		(try_end), 
		
		(agent_get_troop_id, ":trp_victim", ":victim"),
		(agent_get_horse,":horse",":victim"),
		(store_attribute_level, ":int", ":trp_victim", ca_intelligence),
		(store_skill_level, ":riding", "skl_riding", ":trp_victim"),
		(store_random_in_range,":die_roll_int",1,26),
        
		# (assign, ":human_resisted", 0),
		# (assign, ":horse_resisted", 0),

		# the horses couldrear
		(try_begin), 
			(ge,":horse",0), # there's an horse being riden
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
				# if rider success on intelligece test: he won'y panic, horse could
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
		
		# the guys can go nuts
		(try_begin), 
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
		# (else_try), 
			# (assign, ":human_resisted", 1),				
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
  ],
  [
	# physical attack on random agent
	  
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
		
		# this one is eligible for phisical effect,
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
	(agent_deliver_damage_to_agent,":random_agent",":random_agent"), 
	(set_show_messages,1),
	
	# display kill in a log message of appropriate color
	(assign, ":text_color", 0xFFAAFFAA),
	(try_begin),
		(agent_is_ally, ":random_agent"),
		(assign, ":text_color", 0xFFFFAAAA),
	(try_end),
	(str_store_string, s10, "@killed"),	
	(try_begin),
		(agent_is_wounded, ":random_agent"),
		(str_store_string, s10, "@knocked unconsciuos"),
	(try_end),
	(str_store_agent_name, s11, ":random_agent"),
	(display_log_message, "@Nazgul diving attack on {s11}!"),
	(display_log_message, "@{s11} is {s10} in the Nazgul attack!",":text_color"),
  ]
)

# if player attempts to ride non matching mount, mount rebels
tld_player_cant_ride = (0.90,1.5,0.5,
  [
    (eq, "$g_crossdressing_activated", 0),
	(get_player_agent_no, ":player_agent"),
	(agent_get_horse,":mount",":player_agent"),
    (troop_get_type, ":race", "$g_player_troop"),
	(ge, ":mount", 0),
	(assign, ":is_warg", 0),
	(assign, ":is_orc", 0),
	(agent_get_item_id,":mount_item", ":mount"),
	(try_begin), (is_between, ":mount_item", item_warg_begin, item_warg_end),(assign, ":is_warg", 1),(try_end),
	(try_begin), (is_between, ":race"      , tf_orc_begin   , tf_orc_end   ),(assign, ":is_orc" , 1),(try_end),
	(neq, ":is_warg", ":is_orc"), # non orc riding wargs, or orc riding non wargs
	(store_random_in_range, ":rand",0,100),
	(ge, ":rand", 50),
  ],
  [
	(get_player_agent_no, ":player"),
	(agent_get_horse,":mount",":player"),
	(ge, ":mount", 0),
	(agent_get_item_id,":mount_item", ":mount"),
	(agent_set_animation, ":mount", "anim_horse_rear"),
	(try_begin), 
		(is_between, ":mount_item", item_warg_begin, item_warg_end),
		(agent_deliver_damage_to_agent, ":mount", ":player"), # warg bytes!
		(display_message, "@Bitten by your own warg mount!"),
		(agent_play_sound, ":mount", "snd_warg_lone_woof"),
	(else_try),
		(display_message, "@Your horse rears, refusing to obey your commands!"),
		(agent_play_sound, ":mount", "snd_neigh"),
	(try_end),
  ]
)

custom_warg_sounds = (0.65,0,0,  [(gt,"$wargs_in_battle",0)],
  [
    (assign, "$wargs_in_battle", 0), # recount them, to account for deaths
    (try_for_agents, ":warg"),
		(agent_get_item_id, ":warg_item", ":warg"),
		(is_between, ":warg_item", item_warg_begin ,item_warg_end),
		(agent_is_alive, ":warg"),
		(val_add, "$wargs_in_battle", 1), #  wargs_in_battle++
		(store_random_in_range, ":random", 1, 101), (le, ":random", 7),  # 7% of time
		#(display_message,"@warg says: 'woof, woof!'"),
		(agent_play_sound, ":warg", "snd_warg_lone_woof"),
	(try_end),
  ]
)

custom_troll_hitting = ( 0.3,0,0, [(gt,"$trolls_in_battle",0),],
  [
	#  for tuning: show current troll HP
	(try_for_agents,":troll"),
		(agent_is_alive,":troll"),
		(agent_is_human,":troll"),
		(agent_get_troop_id,reg0,":troll"), # is it a troll?
		(troop_get_type, reg0, reg0),
		(eq, reg0, tf_troll),

		#  for tuning: show current troll HP at random times
		(try_begin), 
			(store_random_in_range,":random",1,20),
			(eq,":random",1), # show it once in 20
			(store_agent_hit_points,reg1,":troll"),
			(display_message,"@DEBUG: troll health: {reg1}%!"),
		(try_end),
		
		(agent_get_slot,":status",":troll",slot_agent_troll_swing_status),
		(try_begin),
			(neg|eq,":status",0),
			(store_add,":status",":status",1),
		(else_try),
			# status is 0: *can* decide to start a swing
			(get_player_agent_no, ":player_agent"),
			(try_begin),
				(eq, ":player_agent", ":troll"),
				# player controlled trolls swing when button pressed
				(try_begin),
					(key_is_down, key_left_mouse_button),
					(assign,":status",1), 
				(try_end),
			(else_try),
				# AI attaks 10% of times, if at lest a  victim is in range
				(store_random_in_range,":random",1,101),
				(le,":random",10), 
				(agent_get_position,1,":troll"),
				(agent_get_team, ":troll_team", ":troll"),
				(try_for_agents,":victim"), # look for enemies in range
					(eq,":status",0),
					
					(agent_is_human,":victim"),
					(agent_is_alive, ":victim"),
					(agent_get_team, ":victim_team", ":victim"),
					(teams_are_enemies, ":victim_team", ":troll_team"),
					(agent_get_position,2,":victim"),
					(get_distance_between_positions,":dist",1,2),
					(store_random_in_range, reg0, 0,61), 
					(val_sub, ":dist", reg0), # swing earlier than in range (sometimes)
					(lt,":dist",300), # 200+weapon size/2
						
					(neg|position_is_behind_position,2,1),
					(assign,":status",1),
				(end_try),
			(try_end),
		(try_end),
		
		(store_agent_hit_points,":cur_hp",":troll",1),
		(agent_get_slot,":last_hp", ":troll",slot_agent_last_hp),
		# test for stun
		(try_begin),
			(store_add,":last_hp",3),
			(ge,":last_hp",":cur_hp"),
			(assign,":status",-4), # STUNNED: skip 4 "turns"
		(try_end),
		
		(agent_set_slot,":troll",slot_agent_troll_swing_status,":status"),
		(agent_set_slot, ":troll",slot_agent_last_hp,":cur_hp"),
		
		(try_begin),
			# status = 1: make troll start the attack!
			(eq,":status",1),
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
			(end_try),
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
			(end_try),
			#(agent_set_animation_progress, ":troll", 66),
	  
			(agent_play_sound,":troll","snd_big_weapon_swing"),
	  
			#(try_begin),
				#(eq,"$g_troll_chosen_move",3),
				#(agent_get_look_position,1,":troll"), # because move 3 (overswing) rotates torso!
			#(else_try),
			(agent_get_position,1,":troll"),
			#(end_try),
	  
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
				(end_try),
				(eq,":hit",1),
			
				# test if friendly troll...
				(agent_get_troop_id,reg0,":victim"),
				(troop_get_type, ":victim_type", reg0),
				(agent_get_team, reg1, ":victim"),
				(agent_get_team, reg2, ":troll"),
				(neq|this_or_next, ":victim_type", tf_troll), # trolls don't hit trolls!
				(teams_are_enemies, reg1, reg2),  # ...unless they are enemy trolls
			
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
							(store_random_in_range,reg0,1,5),
							(agent_set_animation_progress, ":victim", reg0), # differentiate timings a bit
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
			(end_try),
		(try_end),
	(try_end),
	]
 )

custom_tld_horses_hate_trolls = (0,0,1, [(eq,"$trolls_in_battle",1)],[
		(try_for_agents,":troll"),										# horse rearing near troll
			(agent_get_troop_id,reg0,":troll"),
			(troop_get_type, reg0, reg0),
			(try_begin),
				(eq, reg0, tf_troll),
				(agent_get_position,1,":troll"),
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
					(store_random_in_range, reg0, 0,12),
					(try_begin),
						(eq,reg0,0),(agent_set_animation, ":horse", "anim_horse_rear"),(agent_play_sound,":horse","snd_neigh"),
					(else_try),
						(eq,reg0,1),(agent_set_animation, ":horse", "anim_horse_turn_right"),(agent_play_sound,":horse","snd_horse_low_whinny"),
					(else_try),
						(eq,reg0,2),(agent_set_animation, ":horse", "anim_horse_turn_right"),(agent_play_sound,":horse","snd_horse_low_whinny"),
					(try_end),
				(try_end),
			(try_end),
		(try_end),
])
		
################## SIEGE LADDERS BEGIN #######################################
HD_ladders_init = (0,0,ti_once,[],[
			 (scene_prop_get_instance,":ladder", "spr_siege_ladder_14m", 0),		###### lower siege ladders at battle start
			 (prop_instance_get_position,pos1,":ladder"),					###### saves the hassle of aligning props with wall
			 (position_rotate_x,pos1,120),
			 (prop_instance_set_position,":ladder",pos1),

			 (scene_prop_get_instance,":ladder", "spr_siege_ladder_14m", 1),
			 (prop_instance_get_position,pos1,":ladder"),
			 (position_rotate_x,pos1,120),
			 (prop_instance_set_position,":ladder",pos1),
#			 (play_sound, "snd_evil_horn"),
			])
HD_ladders_rise = (0,25,ti_once, [],[(scene_prop_get_instance,":ladder", "spr_siege_ladder_14m", 0),	###### raise siege ladders after 25 sec into battle
			 (prop_instance_get_position,pos1,":ladder"),
			 (position_rotate_x,pos1,-120),
			 (prop_instance_animate_to_position,":ladder",pos1,900),
			 (play_sound,"snd_distant_carpenter"),

			 (scene_prop_get_instance,":ladder", "spr_siege_ladder_14m", 1),
			 (prop_instance_get_position,pos1,":ladder"),
			 (position_rotate_x,pos1,-120),
			 (prop_instance_animate_to_position,":ladder",pos1,1100),
			 (play_sound, "snd_evil_horn"),
			 (display_message,"@The ladders on Deeping Wall! Watch out!"),
			])
################## SIEGE LADDERS END #########################################

#################################################################
################ BALLISTA BEGIN #################################     
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
			
ballista_operate = (0, 0, 1,	[(key_clicked, key_e),  								###### initiate ballista
			 (eq,"$ballista_action",0),
			],
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
			 (try_end),
			])
			
ballista_disengage = (0, 0, 1, 	[(key_clicked, key_f),(eq,"$ballista_action",1),],		###### disengage ballista
			[(mission_cam_set_mode,0),(assign,"$ballista_action",0),
			])
			
ballista_shoot = (0, 0, 0,   [(key_clicked, key_space),(eq,"$ballista_action",1),(eq,"$missile_flying",0),],	###### fire in the hole!
			[#(display_message,"@Ballista: shooting"),
			 (assign,"$ballista_action",2),
			 (assign,"$missile_flying",1),
			 (scene_prop_get_instance,"$missile_flying_instance", "spr_ballista_missile","$missile_count"),
			 (prop_instance_get_position,pos1,"$ballista_instance"),
			 (position_move_z,pos1,300),
			 (position_move_y,pos1,300),
			 (position_rotate_z,pos1,180),
			 (mission_cam_animate_to_position, pos1, 500, 0),
			 (play_sound,"snd_release_crossbow"),
			])

ballista_reload_pause = (0, 2, 0, 	[(eq,"$ballista_action",2),], 							###### reloading pause
			[(assign,"$ballista_action",3),
			])

ballista_reload = (0, 0.1, 0, [(eq,"$ballista_action",3),],
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
			 (try_end),
			])
			
ballista_fly_missile = (0, 0, 0,   [(eq,"$missile_flying",1),],  
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
			(try_end),
			])
			
ballista_toggle_fire_arrow = (0, 0.1,0.5,[(key_clicked, key_t),(eq,"$ballista_action",1),(eq,"$missile_flying",0)], ### toggle fire on missile
			[(try_begin),(eq,"$ballista_fire",1),(assign,"$ballista_fire",0),
			 (else_try),				 (assign,"$ballista_fire",1),
			 (try_end),
			])

ballista_missile_illumination = (0, 0, 0, 	[(eq,"$ballista_fire",1),],   							###### missile illumination
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
				(particle_system_burst, "psys_torch_fire_sparks",pos1,10),
			])

ballista_camera_alignment = (0, 0, 0, 	[(eq,"$ballista_action",1),], 							###### camera and loaded missile alignment
			[(prop_instance_get_position,pos1,"$ballista_instance"),
			 (scene_prop_get_instance,":missile_instance", "spr_ballista_missile", "$missile_count"),
			 (position_move_z,pos1,5),
			 (prop_instance_set_position,":missile_instance",pos1),
			 (position_move_z,pos1,105),
			 (position_move_y,pos1,150),
			 (position_rotate_z,pos1,180),
		 	 (mission_cam_animate_to_position, pos1, 5,0),
			 (get_player_agent_no,":player_agent"),
			 (agent_set_animation,":player_agent", "anim_ready_crossbow"),
			])
																		###### turning ballista mesh and aiming
ballista_turn_up =		(0, 0, 0, 	[(key_is_down, key_up),   (eq,"$ballista_action",1),],[(prop_instance_get_position,pos5,"$ballista_instance"),(position_rotate_x,pos5,1), (prop_instance_animate_to_position,"$ballista_instance",pos5,3),])
ballista_turn_down =	(0, 0, 0, 	[(key_is_down, key_down), (eq,"$ballista_action",1),],[(prop_instance_get_position,pos5,"$ballista_instance"),(position_rotate_x,pos5,-1),(prop_instance_animate_to_position,"$ballista_instance",pos5,3),])
ballista_turn_left =	(0, 0, 0, 	[(key_is_down, key_left), (eq,"$ballista_action",1),],[(prop_instance_get_position,pos5,"$ballista_instance"),(position_rotate_z,pos5,1), (prop_instance_animate_to_position,"$ballista_instance",pos5,3),])
ballista_turn_right =	(0, 0, 0, 	[(key_is_down, key_right),(eq,"$ballista_action",1),],[(prop_instance_get_position,pos5,"$ballista_instance"),(position_rotate_z,pos5,-1),(prop_instance_animate_to_position,"$ballista_instance",pos5,3),])
ballista_aim =			(0, 0, 0, 	[(key_is_down, key_left_shift),(eq,"$ballista_action",1),],[(prop_instance_get_position,pos6,"$ballista_instance"),(position_move_y,pos6,60),(position_move_z,pos6,15),(position_rotate_z,pos6,180),(mission_cam_animate_to_position,pos6,100,1),])
################## BALLISTA END ##############################################

################## STONELOBBING BEGIN ########################################
################## uses spr_stoneball and spr_throwing_stone  ################
################## pos49 is used globally for stone tracking! ################
																		######
stonelobbing_init_stone = (0, 0, ti_once, [],[(assign,"$stonelobbing_state",0),				###### 0 no stones, 1 stone picked, 2,3,4 stone flying & bouncing
						(assign,"$stone_horizontal_velocity",0),
						(assign,"$stone_vertical_velocity",0),
						(assign,"$stone_rotation_x",20),				###### stone rotation speed in flight
						(assign,"$stone_rotation_y",30),
						(assign,"$stone_rotation_z",30),	
						])
						
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
			(try_end),
			])
			
stonelobbing_throw_stone = (0,0,5, [(key_clicked, key_f),(eq,"$stonelobbing_state",1),			###### throwing a stone
			],
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
			(assign,"$stonelobbing_state",2),
			])
			
stonelobbing_fly_stone = (0,0,0, [(ge,"$stonelobbing_state",2),								###### stone flight
			],
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
			(try_end),
			])
			
stonelobbing_carry_stone = (0,0,0, [(eq,"$stonelobbing_state",1),								###### carrying stone sync
			],
			[(get_player_agent_no,":player_agent"), (agent_get_position,pos6,":player_agent"),
			(position_move_z,pos6,170),
			(position_move_x,pos6,25), 
			(prop_instance_animate_to_position,"$stone_picked_instance",pos6,3),
			(agent_set_walk_forward_animation,":player_agent","anim_ready_carrystone"),#    dont know how to assign upperbody animation yet :(
			])			
################## STONELOBBING END ########################################

################## FLORA BEGIN ###########################################
scene_set_flora_init = (ti_before_mission_start,0,0,[],
	[
	(try_for_range,":pointer",0,20),
		(store_random_in_range,":object","spr_tree0_yellow_flower","spr_trees_end"),	# assign type of tree
		(troop_set_slot,"trp_temp_array_a",":pointer",":object"),
		(assign,":num",1),
		(try_for_range,":i",0,":pointer"),												# tree was previously assigned?
			(try_begin),(troop_slot_eq,"trp_temp_array_a",":i",":object"),(val_add,":num",1),(try_end),
		(try_end),
		(troop_set_slot,"trp_temp_array_b",":pointer",":num"),
		(store_add,":spr_pointer","spr_zz_pointer00",":pointer"),
		(replace_scene_props,":spr_pointer",":object"),
	(try_end),
	])
##########################################################################
scene_set_flora_army_spawn = (0, 0, ti_once,[
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

		(troop_get_slot,":spr_pointer","trp_temp_array_a",":pointer"),	# poiting towards repeating trees
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
    ],[])
 

################# whistle for horse
horse_whistle_init = (0.2,0,ti_once,[],[(get_player_agent_no,":agent"),(agent_get_horse,"$player_horse",":agent"),])
horse_whistle = (0,0,3,[(gt,"$player_horse",0),(key_clicked, key_m),],
    [ (get_player_agent_no,":player"),(agent_play_sound,":player","snd_man_warcry"),(display_message,"@You yell for your horse."),
      (agent_is_alive, "$player_horse"),(agent_get_position, pos1, ":player"),(agent_set_scripted_destination, "$player_horse", pos1, 0),
    ])

##common_battle_kill_underwater = (
##  5, 0, 0, [],
##   [   
##      (try_for_agents,":agent"),
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
