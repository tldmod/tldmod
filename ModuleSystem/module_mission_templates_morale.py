from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *

tld_morale_triggers = [

 	# This trigger always happens to prevent a "you killed 30000 troops in this battle." bug when you turn battle morale on
	# after it was turned off for some time. -CppCoder

     	(1, 0, ti_once, [], [
        	(get_player_agent_kill_count,"$base_kills",0),
        	(assign,"$new_kills_a",0),
		(assign,"$new_kills",0),
        	#(assign,"$new_enemy_kills_a",0),
		#(assign,"$new_enemy_kills",0),
    	]),

 	# TODO: rally your troops (once per battle).
     	#(0, 0, ti_once, [(key_clicked, key_v),(eq, "$tld_option_morale", 1)], []),

 	# TODO: AI rallies enemy troops (once per battle).
     	#(0.1, 0, ti_once, [(eq, "$tld_option_morale", 1)], []),

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
	# only after 10 seconds, to ensure agents have time to advance and engage in 
	# battle before immediately fleeing. -CppCoder

      	(0.1, 0, 0, [(eq, "$tld_option_morale", 1),(store_mission_timer_a,reg1),(ge,reg1,10)], 
	[
		(try_for_agents, ":cur_agent"),
			(try_begin),
				(agent_is_ally, ":cur_agent"),
				(agent_slot_eq,":cur_agent",slot_agent_routed,1),
				(call_script, "script_find_exit_position_at_pos4", ":cur_agent"),
				(agent_set_scripted_destination, ":cur_agent", pos4, 1),
				(agent_get_position, pos2, ":cur_agent"),
				(get_distance_between_positions, ":dist", pos4, pos2),
				(lt, ":dist", 300),
				(call_script, "script_remove_agent_from_field", ":cur_agent"),
			(else_try),
				(agent_slot_eq,":cur_agent",slot_agent_routed,1),
				(call_script, "script_find_exit_position_at_pos4", ":cur_agent"),
				(agent_set_scripted_destination, ":cur_agent", pos4, 1),
				(agent_get_position, pos2, ":cur_agent"),
				(get_distance_between_positions, ":dist", pos4, pos2),
				(lt, ":dist", 300),
				(call_script, "script_remove_agent_from_field", ":cur_agent"),
			(try_end),
		(try_end),
	]),

     	(3, 0, 3, [(eq, "$tld_option_morale", 1)], 
	[
        	(get_player_agent_kill_count,":more_kills",0),
        	(val_sub,":more_kills","$base_kills"),

		# TODO: Find enemy leader(s) and calculate their morale boost. -CppCoder	

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