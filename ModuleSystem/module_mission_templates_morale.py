from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *

from module_info import wb_compile_switch as is_a_wb_mt

# This file contains a heavily modified and improved version
# of Chel's morale scripts. If you modify it, please leave a 
# note telling what you did. -CC

tld_morale_triggers = [

 	# This trigger always happens to prevent a "you killed 30000 troops in this battle." bug when you turn battle morale on
	# after it was turned off for some time. -CC

     	(2, 0, ti_once, [], [
        	(get_player_agent_kill_count,"$base_kills",0),
        	(assign,"$new_kills_a",0),
		(assign,"$new_kills",0),
		(try_begin),
			# Display the morale values once, so the players have a general idea.
			(eq, "$tld_option_morale", 1),
            (assign, "$allies_coh_modifier", 50), #set initial coherence bonus, will lower over time
            (assign, "$enemies_coh_modifier", 50),            
			(call_script, "script_coherence"),    
			(call_script, "script_healthbars"),
		(try_end),
        	#(assign,"$new_enemy_kills_a",0),
		#(assign,"$new_enemy_kills",0),
    	]),

	(0, 0, 0, [(key_clicked, key_z),(eq, cheat_switch, 1)],
	[
		(try_for_agents, ":agent"),
			(call_script, "script_cf_agent_get_morale", ":agent"),
			(agent_get_troop_id, ":troop", ":agent"),
			(str_store_troop_name, s1, ":troop"),
			#(display_message, "@{s1}'s morale: {reg1}"),
		(try_end),
	]),

	# Rally your troops, five second wait inbetween. -CC
     	(0, 0, 5, [(eq, "$tld_option_morale", 1),(get_player_agent_no, ":player"),(agent_is_alive, ":player"),(key_clicked, key_v)], 
	[
		(assign,":ally","$allies_coh"),
		(assign,":enemy","$enemies_coh"),
		(val_sub,":ally",":enemy"),
		(assign, ":continue", 0),
        (assign, ":rallied_agents", 0),
            
		(try_begin),
			#(le, ":ally", tld_morale_rout_allies),
			(assign, ":continue", 1),
		(else_try),
			(display_message, "@You do not need to rally your troops yet.", color_neutral_news),
		(try_end),

		(eq, ":continue", 1),
		(get_player_agent_no, ":player"),
	
		(assign, ":max_rallies", 1),
		(agent_get_slot, ":times_rallied", ":player", slot_agent_morale_modifier),
		(store_attribute_level, ":cha", "trp_player", ca_charisma),
		(store_div, ":normal_rallies", ":cha", 5),
		(val_add, ":max_rallies", ":normal_rallies"),
        (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
        (val_mul, ":leadership", 2),
        (val_mul, ":normal_rallies", 2),
        (store_add, ":rally_strength", ":normal_rallies", ":leadership"),
        (store_mul, ":rally_range", ":rally_strength", 500),
		(try_begin),
			(this_or_next|player_has_item, "itm_angmar_whip_reward"),
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
			(try_begin),
				(ge, reg1, 0),
				(agent_play_sound, ":player", reg1),
			(try_end),
			(val_add, ":times_rallied", 1),
			(agent_set_slot, ":player", slot_agent_morale_modifier, ":times_rallied"),
            (val_add, "$allies_coh_modifier", ":rally_strength"),
			(try_begin),
				(agent_get_horse, ":horse", ":player"),
				(ge, ":horse", 0),
				(agent_set_animation, ":player", "anim_cheer_player_ride"),
			(else_try),
				(agent_set_animation, ":player", "anim_cheer_player"),
			(try_end),
            
            (agent_get_position, pos90, ":player"),
            (set_fixed_point_multiplier, 100),

            ] + ((is_a_wb_mt==1) and [ #
            (try_for_agents, ":agent", pos90, ":rally_range"),
                (neq, ":agent", ":player"),
				(agent_is_human, ":agent"),
				(agent_is_alive, ":agent"),
				(agent_is_ally, ":agent"),
            ] or [
            (try_for_agents, ":agent"),
                (neq, ":agent", ":player"),
				(agent_is_human, ":agent"),
				(agent_is_alive, ":agent"),
				(agent_is_ally, ":agent"),
                (agent_get_position, pos0, ":agent"),
                (get_distance_between_positions, ":dist", pos0, pos90),
                (lt,":dist", ":rally_range"),
            ]) + [
            
				(call_script, "script_cf_agent_get_leader_troop", ":agent"),
				(assign, ":can_rally", 0),
				(try_begin),
					(eq, reg0, "trp_player"),
					(assign, ":can_rally", 1),
				(else_try), # Give player a chance to rally allied troops
					(store_skill_level,":ldr","skl_leadership","trp_player"),
					(gt, ":ldr", 3), # 3 or more leadership
					(store_random_in_range, ":rnd", 0, 100),
					(store_mul, ":chance", ":ldr", 10),
					(gt, ":chance", ":rnd"),
					(assign, ":can_rally", 1),
				(try_end),
				(eq, ":can_rally", 1),
                (val_add, ":rallied_agents", 1),
                # (str_store_agent_name, s1, ":agent"),
                # (display_message, "@rallied {s1}"),
                (agent_get_troop_id, ":troop_id", ":agent"),
                (agent_get_slot, ":morale_bonus", ":agent", slot_agent_morale_modifier),
                (val_add, ":morale_bonus", ":rally_strength"),
				(agent_set_slot, ":agent", slot_agent_morale_modifier, ":morale_bonus"),
                (agent_get_combat_state, ":agent_cs", ":agent"),
                (agent_get_horse, ":agent_horse", ":agent"),
                (store_random_in_range, ":chance_to_cheer", 0, 100),
                (try_begin), #chance to cheer if rallied (but not when in combat)
                    (gt, ":chance_to_cheer", 15),
                    (eq, ":agent_cs", 0),
                    (try_begin),
                        (gt, ":agent_horse", 0),
                        (agent_set_animation, ":agent", "anim_cheer_player_ride"),
                    (else_try),
                        (agent_set_animation, ":agent", "anim_cheer"),
                    (try_end),
                    (call_script, "script_troop_get_cheer_sound", ":troop_id"),
                    (ge, reg1, 0),
                    (agent_play_sound, ":agent", reg1),
                (try_end),
				(try_begin),
					(agent_slot_eq,":agent",slot_agent_routed,1),
					(agent_set_slot, ":agent", slot_agent_routed, 0),
					(agent_clear_scripted_mode, ":agent"),			
					] + ((is_a_wb_mt==1) and [	
					(agent_slot_eq, ":agent", slot_agent_is_running_away, 1),
					(agent_set_slot, ":agent", slot_agent_is_running_away, 0),
					(agent_stop_running_away, ":agent"), 
					] or []) + [	
				(try_end),
			(try_end),

            (assign, reg10, ":rallied_agents"),
            (display_message, "@You rally {reg10} troops!", color_good_news),            
		(try_end),

	] + ((is_a_wb_mt==1) and [
	  (try_begin),
	      (neg|is_presentation_active, "prsnt_battle"),
	      (start_presentation, "prsnt_show_num_rallies"),
      (try_end),
	] or []) + [

	]),

 	# AI rallies troops -CC
     	(3, 0, 0, [(eq, "$tld_option_morale", 1)], 
	[	
		(assign,":ally","$allies_coh"),
		(assign,":enemy","$enemies_coh"),
		(val_sub,":ally",":enemy"),

        (get_player_agent_no, ":player"),

		# When allied troops are routed, allied commanders rally their troops!	
        (try_for_agents, ":agent"), #find allied commanders
            (le, ":ally", tld_morale_rout_allies),
            (le, "$allies_coh", 60),
            (neq, ":agent", ":player"),
            (agent_is_human, ":agent"),
            (agent_is_alive, ":agent"),
            (agent_is_ally, ":agent"),
            (agent_get_troop_id, ":troop", ":agent"),
            (call_script, "script_cf_agent_get_leader_troop", ":agent"),
            (eq, ":troop", reg0),
            (troop_is_hero, ":troop"),
            (agent_get_slot, ":times_rallied", ":agent", slot_agent_morale_modifier),
            (store_attribute_level, ":cha", ":troop", ca_charisma),
            (store_skill_level, ":leadership", "skl_leadership", ":troop"),
            (store_div, ":max_rallies", ":cha", 5),
            (val_add, ":max_rallies", 1),
            (val_mul, ":leadership", 2),
            (val_mul, ":max_rallies", 2),
            (store_add, ":rally_strength", ":max_rallies", ":leadership"),
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
                (troop_get_type, reg65, ":troop"),
                (try_begin),
                   (neq, reg65, 1), #not female
                   (assign, reg65, 0), #make it male for strings
                (try_end),
                (str_store_troop_name, s5, ":troop"),
                (display_message, "@{s5} rallies {reg65?her:his} troops!", color_good_news),
                (val_add, ":times_rallied", 1),
                (agent_set_slot, ":agent", slot_agent_morale_modifier, ":times_rallied"),
                (val_add, "$allies_coh_modifier", ":rally_strength"),
                (call_script, "script_troop_get_cheer_sound", ":troop"),
                (try_begin),
                    (ge, reg1, 0),
                    (agent_play_sound, ":agent", reg1),
                (try_end),
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
                    (agent_get_slot, ":morale_bonus", ":cur_agent", slot_agent_morale_modifier),
                    (val_add, ":morale_bonus", ":rally_strength"),
                    (agent_set_slot, ":cur_agent", slot_agent_morale_modifier, ":morale_bonus"),
                    (agent_set_slot, ":cur_agent", slot_agent_routed, 0),
                    (agent_clear_scripted_mode, ":cur_agent"),
                    ] + ((is_a_wb_mt==1) and [	
                    (agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 1),
                    (agent_set_slot, ":cur_agent", slot_agent_is_running_away, 0),
                    (agent_stop_running_away, ":cur_agent"), 
                    ] or []) + [	
                (try_end),
			(try_end),
		(try_end),

		# When enemy troops are routed, enemy commanders rally their troops!
        (try_for_agents, ":agent"),
            (ge, ":ally", tld_morale_rout_enemies),
            (le, "$enemies_coh", 60),
            (agent_is_human, ":agent"),
            (agent_is_alive, ":agent"),
            (agent_is_ally|neg, ":agent"),
            (agent_get_troop_id, ":troop", ":agent"),
            (call_script, "script_cf_agent_get_leader_troop", ":agent"),
            (eq, ":troop", reg0),
            (troop_is_hero, ":troop"),
            (agent_get_slot, ":times_rallied", ":agent", slot_agent_morale_modifier),
            (store_attribute_level, ":cha", ":troop", ca_charisma),
            (store_skill_level, ":leadership", "skl_leadership", ":troop"),
            (store_div, ":max_rallies", ":cha", 5),
            (val_add, ":max_rallies", 1),
            (val_mul, ":leadership", 2),
            (val_mul, ":max_rallies", 2),                
            (store_add, ":rally_strength", ":max_rallies", ":leadership"),
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
                (troop_get_type, reg65, ":troop"),
                (try_begin),
                   (neq, reg65, 1), #not female
                   (assign, reg65, 0), #make it male for strings
                (try_end),
                (str_store_troop_name, s5, ":troop"),
                (display_message, "@{s5} rallies {reg65?her:his} troops!", color_bad_news),
                (val_add, ":times_rallied", 1),
                (agent_set_slot, ":agent", slot_agent_morale_modifier, ":times_rallied"),
                (val_add, "$enemies_coh_modifier", ":rally_strength"),
                (call_script, "script_troop_get_cheer_sound", ":troop"),
                (try_begin),
                    (ge, reg1, 0),
                    (agent_play_sound, ":agent", reg1),
                (try_end),
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
                    (agent_get_slot, ":morale_bonus", ":cur_agent", slot_agent_morale_modifier),
                    (val_add, ":morale_bonus", 20),
                    (agent_set_slot, ":cur_agent", slot_agent_morale_modifier, ":morale_bonus"),
                    (agent_set_slot, ":cur_agent", slot_agent_routed, 0),
                    (agent_clear_scripted_mode, ":cur_agent"),
                    ] + ((is_a_wb_mt==1) and [	
                    (agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 1),
                    (agent_set_slot, ":cur_agent", slot_agent_is_running_away, 0),
                    (agent_stop_running_away, ":cur_agent"), 
                    ] or []) + [	
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

	# morale check (changed from 15)
	(30, 0, 10, [(eq, "$tld_option_morale", 1)], 
	[
		(call_script, "script_coherence"),
        (call_script, "script_normalize_coherence_modifier"),            
		(call_script, "script_morale_check"),    
        ]),

	# rout check (changed from 20)
	(40, 0, 5, [(eq, "$tld_option_morale", 1)], 
	[
		(call_script, "script_coherence"),    
		(call_script, "script_rout_check"),       
        ]),


    # temporary coherence effect of killed friendlies/allies (WB only)
	] + ((is_a_wb_mt==1) and [	
    (ti_on_agent_killed_or_wounded, 0, 0, [],
      [
        (store_trigger_param_1, ":killed_agent"),
        (agent_is_active, ":killed_agent"),
        (agent_is_human, ":killed_agent"),
        (gt, ":killed_agent", 0),
        (store_random_in_range, ":chance", 0, 100), #tweakable
        
        (try_begin),
            (agent_is_ally, ":killed_agent"),
            (le, "$allies_leadership", ":chance"),
            (val_sub, "$allies_coh_modifier", 1),
            #(val_add, "$enemies_coh_modifier", 1),
        (else_try),
           # (val_add, "$allies_coh_modifier", 1),
            (val_sub, "$enemies_coh_modifier", 1), 
        (try_end),             
    ]),
	] or []) + [


	# Custom trigger, ensures agents get to position and when they do, remove them, but
	# only after 90 seconds, to ensure agents have time to advance and engage in 
	# battle before immediately fleeing, otherwise there is no fight. -CppCoder - Changed to 3.5 mins (kham)
      	(0.1, 0, 0, [(eq, "$tld_option_morale", 1),(store_mission_timer_a,reg1),(ge,reg1,210)], 
	[
		(try_for_agents, ":cur_agent"),
			(agent_is_alive, ":cur_agent"),
			(try_begin),
				(agent_slot_eq,":cur_agent",slot_agent_routed,1),
				
				] + ((is_a_wb_mt==1) and [

		        ## WB has an operation for fleeing - Kham
		        (agent_start_running_away, ":cur_agent"),
		        (agent_set_slot, ":cur_agent", slot_agent_is_running_away, 1),
		            
		        ] or [
				(call_script, "script_find_exit_position_at_pos4", ":cur_agent"),
				(agent_set_scripted_destination, ":cur_agent", pos4, 1),
				
				]) + [

				(agent_get_position, pos2, ":cur_agent"),
				(get_distance_between_positions, ":dist", pos4, pos2),
				(lt, ":dist", 300),
				(store_random_in_range, ":rand", 0, 100),
				(lt, ":rand", 50),
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
            (store_sub, ":recent_kills", ":more_kills", "$new_kills_a"),
            (val_add,"$allies_coh_modifier",":recent_kills"), #for temporary coherence effect
            (assign,"$new_kills_a",":more_kills"),
			(assign,"$new_kills",":more_kills"), #/2 for permanent coherence effect
			(val_div,"$new_kills",2),
            (assign,reg1,":more_kills"),
            (display_message,"@You have killed {reg1} enemies in this battle!",0x6495ed),         
            (display_message,"@Your bravery inspires your troops!",0x6495ed),
        	(try_end),
        ]),


#Show num rallies
] + ((is_a_wb_mt==1) and [
(ti_after_mission_start, 0, ti_once, [],[(start_presentation, "prsnt_show_num_rallies")]),

(1, 0, 0, [
    (this_or_next|game_key_is_down, gk_move_forward),
    (this_or_next|game_key_is_down, gk_move_backward),
    (this_or_next|game_key_is_down, gk_move_left),
    (game_key_is_down, gk_move_right),
    (neg|is_presentation_active, "prsnt_show_num_rallies"),
    (neg|is_presentation_active, "prsnt_battle"),
    (neg|main_hero_fallen),
    ],[    
    (start_presentation, "prsnt_show_num_rallies"),
]),

(0, 0, 0, [
		  (eq, "$show_key_binds_toggle", 0),
          (key_clicked, key_insert),
          (this_or_next|neg|key_is_down, key_left_control),
          (neg|key_is_down, key_right_control),],

          [(assign, "$show_key_binds_toggle", 1),(start_presentation, "prsnt_show_key_binds"),
]),

] or []) + [

]
