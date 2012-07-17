from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *

tld_morale_triggers = [

 	# This trigger always happens to prevent a "you killed 30000 troops in this battle." bug when you turn battle morale on
	# after it was turned off for some time.
     (1, 0, ti_once, [], [
        (get_player_agent_kill_count,"$base_kills",0),
        (assign,"$new_kills_a",0),
	(assign,"$new_kills",0),
	(assign, "$rout", 0),
	(assign, "$airout", 0),
         ]),

	# Custom trigger, ensures agents get to position and when they do, remove them

      (0.1, 0, 0, [(eq, "$tld_option_morale", 1)], 
	[
		(try_for_agents, ":cur_agent"),
			(agent_get_position, pos1, ":cur_agent"),
			(agent_get_position, pos2, ":cur_agent"),
			(try_begin),
				(agent_is_ally, ":cur_agent"),
				(agent_slot_eq,":cur_agent",slot_agent_routed,1),
				(agent_get_scripted_destination, pos1, ":cur_agent"),
				(agent_set_scripted_destination, ":cur_agent", pos1, 1),
				(get_distance_between_positions, ":dist", pos1, pos2),
				(lt, ":dist", 300),
				(call_script, "script_remove_agent_from_field", ":cur_agent"),
			(else_try),
				(agent_slot_eq,":cur_agent",slot_agent_routed,1),
				(agent_get_scripted_destination, pos1, ":cur_agent"),
				(agent_set_scripted_destination, ":cur_agent", pos1, 1),
				(get_distance_between_positions, ":dist", pos1, pos2),
				(lt, ":dist", 300),
				(call_script, "script_remove_agent_from_field", ":cur_agent"),
			(try_end),
			
		(try_end),
	]),

     (0, 0, 2, [(key_clicked, key_t),(eq, "$tld_option_morale", 1)], [
(call_script, "script_coherence"),    
(call_script, "script_healthbars"),       
         ]),
      
(1, 0, ti_once, [(eq, "$tld_option_morale", 1)], [
(call_script, "script_coherence"),    
         ]),						
      
(15, 0, 10, [(eq, "$tld_option_morale", 1)], [
(call_script, "script_coherence"),    
(call_script, "script_morale_check"),    
         ]),
(5, 0, 3, [(eq, "$tld_option_morale", 1)], [
(call_script, "script_coherence"),    
(call_script, "script_rout_check"),       
         ]),

     (3, 0, 3, [(eq, "$tld_option_morale", 1)], [
        (get_player_agent_kill_count,":more_kills",0),
        (val_sub,":more_kills","$base_kills"),
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