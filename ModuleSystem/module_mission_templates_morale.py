from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *

# This file contains a heavily modified and improved version
# of Chel's morale scripts. If you modify it, please leave a 
# note telling what you did. -CC

tld_morale_triggers = [

 	# This trigger always happens to prevent a "you killed 30000 troops in this battle." bug when you turn battle morale on
	# after it was turned off for some time. -CC

     	(1, 0, ti_once, [], [
        	(get_player_agent_kill_count,"$base_kills",0),
        	(assign,"$new_kills_a",0),
		(assign,"$new_kills",0),
		(try_begin),
			# Display the morale values once.
			(eq, "$tld_option_morale", 1),
			(call_script, "script_coherence"),    
			(call_script, "script_healthbars"),
		(try_end),
        	#(assign,"$new_enemy_kills_a",0),
		#(assign,"$new_enemy_kills",0),
    	]),

	# Rally your troops, five second wait inbetween. -CC
     	(0, 0, 5, [(eq, "$tld_option_morale", 1),(get_player_agent_no, ":player"),(agent_is_alive, ":player"),(key_clicked, key_v)], 
	[
		(assign,":ally","$allies_coh"),
		(assign,":enemy","$enemies_coh"),
		(val_sub,":ally",":enemy"),
		(le, ":ally", tld_morale_rout_allies),
		(get_player_agent_no, ":player"),
	
		(assign, ":max_rallies", 1),
		(agent_get_slot, ":times_rallied", ":player", slot_agent_rallied),
		(store_attribute_level, ":cha", "trp_player", ca_charisma),
		(store_div, ":normal_rallies", ":cha", 5),
		(val_add, ":max_rallies", ":normal_rallies"),
		(try_begin),
			(player_has_item|this_or_next, "itm_angmar_whip_reward"),
			(player_has_item, "itm_horn_gondor_reward"),
			(store_skill_level,":horn_rallies","skl_leadership","trp_player"),
			(val_div, ":horn_rallies", 3),
			(val_add, ":max_rallies", ":horn_rallies"),		
		(try_end),
		#(assign, reg0, ":max_rallies"),
		#(assign, reg1, ":times_rallied"),
		#(display_message, "@Max Rallies: {reg0}, Times Rallied: {reg1}"),
		(try_begin),
			(lt, ":times_rallied", ":max_rallies"),
			(call_script, "script_troop_get_cheer_sound", "trp_player"),
			#(play_sound, "snd_evil_horn"),
			(agent_play_sound, ":player", reg1),
			(display_message, "@You rally your troops!", color_good_news),
			(val_add, ":times_rallied", 1),
			(agent_set_slot, ":player", slot_agent_rallied, ":times_rallied"),
			(try_begin),
				(agent_get_horse, ":horse", ":player"),
				(ge, ":horse", 0),
				(agent_set_animation, ":player", "anim_cheer_player_ride"),
			(else_try),
				(agent_set_animation, ":player", "anim_cheer_player"),
			(try_end),
			(try_for_agents, ":agent"),
				(neq, ":agent", ":player"),
				(agent_is_human, ":agent"),
				(agent_is_alive, ":agent"),
				(agent_is_ally, ":agent"),
				# You can only rally YOUR troops.
				(call_script, "script_cf_agent_get_leader_troop", ":agent"),
				(eq, reg0, "trp_player"),
				(agent_set_slot, ":agent", slot_agent_rallied, 1),
				(try_begin),
					(agent_slot_eq,":agent",slot_agent_routed,1),
					(agent_set_slot, ":agent", slot_agent_routed, 0),
					(agent_clear_scripted_mode, ":agent"),					
				(try_end),
			(try_end),
		(try_end),
	]),

 	# AI rallies troops -CC
     	(3, 0, 0, [(eq, "$tld_option_morale", 1)], 
	[	
		(assign,":ally","$allies_coh"),
		(assign,":enemy","$enemies_coh"),
		(val_sub,":ally",":enemy"),

		# When allied troops are routed, allied commanders rally their troops!
		(try_begin),
			(le, ":ally", tld_morale_rout_allies),
			(get_player_agent_no, ":player"),
			(try_for_agents, ":agent"),
				(neq, ":agent", ":player"),
				(agent_is_human, ":agent"),
				(agent_is_alive, ":agent"),
				(agent_is_ally, ":agent"),
				(agent_get_troop_id, ":troop", ":agent"),
				(call_script, "script_cf_agent_get_leader_troop", ":agent"),
				(eq, ":troop", reg0),
				(troop_is_hero, ":troop"),
				(agent_get_slot, ":times_rallied", ":agent", slot_agent_rallied),
				(store_attribute_level, ":cha", ":troop", ca_charisma),
				(store_div, ":max_rallies", ":cha", 5),
				(val_add, ":max_rallies", 1),
				(try_begin),
					(call_script, "script_count_enemy_agents_around_agent", ":agent", 300), # AI won't rally if surrounded. The 
					(le, reg0, 0),								# animation makes him vulnerable. -CC
					(store_random_in_range, ":die_roll", 0, 101),
					(store_mul, ":rally_penalty", ":times_rallied", 20), # The more they have rallied, the less likely to do it again. -CC
					(store_sub, ":chance", 80, ":rally_penalty"),
					(lt, ":die_roll", ":chance"), # lil' bit of personality in AI commanders
					(lt, ":times_rallied", ":max_rallies"), # ":max_rallies"
					(str_store_troop_name, s1, ":troop"),
					#(assign, reg0, ":chance"),
					#(assign, reg1, ":die_roll"),
					#(assign, reg2, ":times_rallied"),
					(agent_get_troop_id, ":troop", ":agent"),
					(str_store_troop_name, s5, ":troop"),
					(display_message, "@{s5} rallies his troops!", color_good_news),
					(val_add, ":times_rallied", 1),
					(agent_set_slot, ":agent", slot_agent_rallied, ":times_rallied"),
					(call_script, "script_troop_get_cheer_sound", ":troop"),
					(agent_play_sound, ":agent", reg1),
					(try_begin),
						(agent_get_horse, ":horse", ":agent"),
						(ge, ":horse", 0),
						(agent_set_animation, ":agent", "anim_cheer_player_ride"),
					(else_try),
						(agent_set_animation, ":agent", "anim_cheer_player"),
					(try_end),
					(try_for_agents, ":cur_agent"),
						(neq, ":agent", ":cur_agent"),
						(agent_is_human, ":cur_agent"),
						(agent_is_alive, ":cur_agent"),
						(agent_is_ally, ":cur_agent"),
						(call_script, "script_cf_agent_get_leader_troop", ":cur_agent"),
						(eq, ":troop", reg0),
						(agent_set_slot, ":cur_agent", slot_agent_rallied, 1),
						(agent_set_slot, ":cur_agent", slot_agent_routed, 0),
						(agent_clear_scripted_mode, ":cur_agent"),
					(try_end),
				(try_end),
			(try_end),
		(try_end),

		# When enemy troops are routed, enemy commanders rally their troops!
		(try_begin),
			(ge, ":ally", tld_morale_rout_enemies),
			(try_for_agents, ":agent"),
				(agent_is_human, ":agent"),
				(agent_is_alive, ":agent"),
				(agent_is_ally|neg, ":agent"),
				(agent_get_troop_id, ":troop", ":agent"),
				(call_script, "script_cf_agent_get_leader_troop", ":agent"),
				(eq, ":troop", reg0),
				(troop_is_hero, ":troop"),
				(agent_get_slot, ":times_rallied", ":agent", slot_agent_rallied),
				(store_attribute_level, ":cha", ":troop", ca_charisma),
				(store_div, ":max_rallies", ":cha", 5),
				(val_add, ":max_rallies", 1),
				(try_begin),
					(call_script, "script_count_enemy_agents_around_agent", ":agent", 300), # AI won't rally if surrounded. The 
					(le, reg0, 0),								# animation makes him vulnerable. -CC
					(store_random_in_range, ":die_roll", 0, 101),
					(store_mul, ":rally_penalty", ":times_rallied", 20), # The more they have rallied, the less likely to do it again. -CC
					(store_sub, ":chance", 80, ":rally_penalty"),
					(lt, ":die_roll", ":chance"), # lil' bit of personality in AI commanders
					(lt, ":times_rallied", ":max_rallies"), # ":max_rallies"
					(assign, reg0, ":chance"),
					(assign, reg1, ":die_roll"),
					(assign, reg2, ":times_rallied"),
					(agent_get_troop_id, ":troop", ":agent"),
					(str_store_troop_name, s5, ":troop"),
					(display_message, "@{s5} rallies his troops!", color_bad_news),
					(val_add, ":times_rallied", 1),
					(agent_set_slot, ":agent", slot_agent_rallied, ":times_rallied"),
					(call_script, "script_troop_get_cheer_sound", ":troop"),
					(agent_play_sound, ":agent", reg1),
					(try_begin),
						(agent_get_horse, ":horse", ":agent"),
						(ge, ":horse", 0),
						(agent_set_animation, ":agent", "anim_cheer_player_ride"),
					(else_try),
						(agent_set_animation, ":agent", "anim_cheer_player"),
					(try_end),
					(try_for_agents, ":cur_agent"),
						(neq, ":agent", ":cur_agent"), # Ralliers don't rally themselves.
						(agent_is_human, ":cur_agent"),
						(agent_is_alive, ":cur_agent"),
						(agent_is_ally|neg, ":cur_agent"),
						(call_script, "script_cf_agent_get_leader_troop", ":cur_agent"),
						(eq, ":troop", reg0),
						(agent_set_slot, ":cur_agent", slot_agent_rallied, 1),
						(agent_set_slot, ":cur_agent", slot_agent_routed, 0),
						(agent_clear_scripted_mode, ":cur_agent"),
					(try_end),
				(try_end),
			(try_end),
		(try_end),
	]),

 	# let the player know of his troop's morale
     	(0, 0, 2, [(key_clicked, key_t),(eq, "$tld_option_morale", 1)], 
	[
		(call_script, "script_coherence"),    
		(call_script, "script_healthbars"),       
	]),
      
	# calculate coherence once
	(1, 0, ti_once, [(eq, "$tld_option_morale", 1)], 
	[
		(call_script, "script_coherence"),    
	]),						

	# morale check      
	(15, 0, 10, [(eq, "$tld_option_morale", 1)], 
	[
		(call_script, "script_coherence"),    
		(call_script, "script_morale_check"),    
        ]),

	# rout check
	(5, 0, 3, [(eq, "$tld_option_morale", 1)], 
	[
		(call_script, "script_coherence"),    
		(call_script, "script_rout_check"),       
        ]),

	# Custom trigger, ensures agents get to position and when they do, remove them, but
	# only after 15 seconds, to ensure agents have time to advance and engage in 
	# battle before immediately fleeing. -CppCoder
      	(0.1, 0, 0, [(eq, "$tld_option_morale", 1),(store_mission_timer_a,reg1),(ge,reg1,15)], 
	[
		(try_for_agents, ":cur_agent"),
			(agent_is_alive, ":cur_agent"),
			(try_begin),
				(agent_slot_eq,":cur_agent",slot_agent_routed,1),
				(call_script, "script_find_exit_position_at_pos4", ":cur_agent"),
				(agent_set_scripted_destination, ":cur_agent", pos4, 1),
				(agent_get_position, pos2, ":cur_agent"),
				(get_distance_between_positions, ":dist", pos4, pos2),
				(lt, ":dist", 300),
				(call_script, "script_count_enemy_agents_around_agent", ":cur_agent", 600),
				(agent_get_troop_id,":troop_no", ":cur_agent"),
				(le|this_or_next, reg0, 0),
				(is_between, ":troop_no", warg_ghost_begin, warg_ghost_end), # Lone wargs can always flee
				(call_script, "script_remove_agent_from_field", ":cur_agent"),
			(try_end),
		(try_end),
	]),

     	(3, 0, 3, [(eq, "$tld_option_morale", 1)], 
	[
        	(get_player_agent_kill_count,":more_kills",0),
        	(val_sub,":more_kills","$base_kills"),

		# TODO: CC: Find enemy leader(s) and calculate their morale boost.	

		(try_begin),
            		(gt,":more_kills","$new_kills_a"),
            		(assign,"$new_kills_a",":more_kills"),
			(assign,"$new_kills",":more_kills"),
			(val_div,"$new_kills",2),
            		(assign,reg1,":more_kills"),
            		(display_message,"@You have killed {reg1} enemies in this battle!",0x6495ed),         
            		(display_message,"@Your bravery inspires your troops!",0x6495ed),
        	(try_end),
        ]),
]