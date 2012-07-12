from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *

tld_morale_init  =	(0.1, 0, ti_once, [(eq, "$tld_option_morale", 1)],
			[
				(try_for_agents, ":cur_agent"),
					(agent_set_slot, ":cur_agent", slot_agent_routed, 0),
				(try_end),
			])

tld_morale_check = 	(1, 0, 0, # check every five seconds 
			[(eq, "$tld_option_morale", 1)], 
			[
				(assign, ":allies", 0),
				(assign, ":enemies", 0),

				# Calculate team agents
				(try_for_agents, ":cur_agent"),

					(agent_is_human, ":cur_agent"),
					(agent_is_alive, ":cur_agent"),
					(try_begin),
						(agent_is_ally, ":cur_agent"),
						(val_add, ":allies", 1),
					(else_try),
						(neg|agent_is_ally, ":cur_agent"),
						(val_add, ":enemies", 1),
					(try_end),

					# Determine if agent has been routed.

					(assign, ":near_allies", 0),
					(assign, ":near_enemies", 0),
					(assign, ":near_allies_strength", 0),
					(assign, ":near_enemies_strength", 0),

					(try_for_agents, ":nearby_agent"),
						(agent_is_human, ":nearby_agent"),
						(agent_is_alive, ":nearby_agent"),
						(get_player_agent_no, ":player_no"),
						(agent_get_team, ":plr_team", ":player_no"),
						(agent_get_team, ":cur_team", ":cur_agent"),
						(agent_get_team, ":oth_team", ":nearby_agent"),
						(agent_get_position,pos1,":cur_agent"),
						(agent_get_position,pos2,":nearby_agent"),
						(set_fixed_point_multiplier, 100),
						(get_distance_between_positions, ":dist", pos1, pos2),
						(lt, ":dist", 500),
						# Code for determining strength of nearby enemies
					(try_end),

					# Average strength of nearby enemies?
					#(try_begin),(gt, ":near_allies", 0),(val_div, ":near_allies_strength", ":near_allies"),(try_end),
					#(try_begin),(gt, ":near_enemies", 0),(val_div, ":near_enemies_strength", ":near_enemies"),(try_end),

					(agent_get_troop_id, ":cur_troop", ":cur_agent"),
					(store_character_level, ":cur_level", ":cur_troop"),
      					(str_store_troop_name, s1, ":cur_troop"),

					(try_begin),
						(get_player_agent_no, ":player_no"),
						(neq, ":cur_agent", ":player_no"),
						(agent_is_ally, ":cur_agent"),
						(agent_slot_eq, ":cur_agent", slot_agent_routed, 0),
						(gt, ":near_enemies", 0),
						(gt, ":near_enemies_strength", ":near_allies_strength"),
						(agent_set_slot, ":cur_agent", slot_agent_routed, 1),
						(display_message, "@{s1} was routed..."),
					(else_try),
						(get_player_agent_no, ":player_no"),
						(neq, ":cur_agent", ":player_no"),
						(agent_is_ally|neg, ":cur_agent"),
						(agent_slot_eq, ":cur_agent", slot_agent_routed, 0),
						(gt, ":near_allies", 0),
						(gt, ":near_allies_strength", ":near_enemies_strength"),
						(agent_set_slot, ":cur_agent", slot_agent_routed, 1),
						(display_message, "@{s1} was routed..."),
					(try_end),

					(try_begin),
						(get_player_agent_no, ":player_no"),
						(neq, ":cur_agent", ":player_no"),
						(agent_is_human, ":cur_agent"),
						(agent_is_alive, ":cur_agent"),
						(agent_slot_eq, ":cur_agent", slot_agent_routed, 1),
						(agent_get_entry_no, ":entry_no", ":cur_agent"),
						(entry_point_get_position, pos1, ":entry_no"),
						(position_set_z_to_ground_level, pos1),
						(agent_set_scripted_destination,":cur_agent",pos1,1),
					(try_end),
				(try_end),
			])


# Check for routed troops to remove them.
tld_morale_routed =	(0.2, 0, 0,
			[(eq, "$tld_option_morale", 1)], 
			[
				(try_for_agents, ":cur_agent"),
					(get_player_agent_no, ":player_no"),
					(neq, ":cur_agent", ":player_no"),
					(agent_is_human, ":cur_agent"),
					(agent_is_alive, ":cur_agent"),
					(agent_slot_eq, ":cur_agent", slot_agent_routed, 1),
					(agent_get_position, pos2, ":cur_agent"),
					(agent_get_entry_no, ":entry_no", ":cur_agent"),
					(entry_point_get_position, pos1, ":entry_no"),
					(position_set_z_to_ground_level, pos1),
					(set_fixed_point_multiplier, 100),
					(get_distance_between_positions, ":dist", pos1, pos2),
					(lt, ":dist", 200),
					(call_script, "script_remove_agent_from_field", ":cur_agent"),
				(try_end),
			])

# tld_morale_triggers = [tld_morale_init, tld_morale_check, tld_morale_routed]
tld_morale_triggers = []