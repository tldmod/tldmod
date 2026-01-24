from header_common import *
from header_operations import *
from header_sounds import *
from header_mission_templates import *
from module_constants import *
from header_terrain_types import *

AI_triggers_moto = [
  # Trigger file: AI_before_mission_start
  (ti_before_mission_start, 0, 0, [(eq, "$tld_option_formations", 2),], [
      (assign, "$ranged_clock", 0),
      (assign, "$clock_reset", 0),
      (assign, "$temp_action_cost", 0), #TLD Kham: piggyback for F1 Fix
      (init_position, Team0_Cavalry_Destination),
      (init_position, Team1_Cavalry_Destination),
      (init_position, Team2_Cavalry_Destination),
      (init_position, Team3_Cavalry_Destination),
      
      (try_begin),
        (eq, "$player_deploy_troops", 0),
        (assign, "$battle_phase", BP_Setup_MOTO),
      (else_try),
        (assign, "$battle_phase", BP_Ready),  #deployment triggers must advance battle phase
      (try_end)
  ]),
  
  # Trigger file: AI_after_mission_start
  (0, 0, ti_once, [(eq, "$tld_option_formations", 2),
      (call_script, "script_cf_division_data_available_moto"),
      ], [
      (set_fixed_point_multiplier, 100),
      (try_for_range, ":team", 0, 4),
        (call_script, "script_battlegroup_get_position_moto", pos0, ":team", grc_everyone),
        (position_get_x, reg0, pos0),
        (team_set_slot, ":team", slot_team_starting_x, reg0),
        (position_get_y, reg0, pos0),
        (team_set_slot, ":team", slot_team_starting_y, reg0),
        
        #prevent confusion over AI not using formations for archers
        (neq, ":team", "$fplayer_team_no"),
        (store_add, ":slot", slot_team_d0_formation, grc_archers),
        (team_set_slot, ":team", ":slot", formation_none),
        
        #set up by spawn point until BP_Setup_MOTO
        (call_script, "script_field_start_position_moto", ":team"), #returns pos2
        (copy_position, pos1, pos2),
        (team_get_leader, ":ai_leader", ":team"),
        (call_script, "script_division_reset_places_moto"),
        
        (try_for_range, ":division", 0, 9),
          (call_script, "script_battlegroup_place_around_pos1_moto", ":team", ":division", ":ai_leader"),
        (try_end),
      (try_end),
  ]),
  
  # Trigger file: AI_setup
  (0, 0, ti_once, [(eq, "$tld_option_formations", 2),
      (get_player_agent_no, ":player"),
      (agent_set_slot, ":player", slot_agent_tournament_point, 0),
      (call_script, "script_cf_division_data_available_moto"),
      (ge, "$battle_phase", BP_Setup_MOTO), #wait 'til player deploys
      ],[
      (call_script, "script_field_tactics_moto", 1),
  ]),
  
  # Trigger file: AI_regular_trigger
  (.1, 0, 0, [(eq, "$tld_option_formations", 2),
      (gt, "$last_player_trigger", 0),
      (ge, "$battle_phase", BP_Setup_MOTO),
      
      (store_mission_timer_c_msec, reg0),
      (val_sub, reg0, "$last_player_trigger"),
      (ge, reg0, 250),  #delay to offset from formations trigger (trigger delay does not work right)
      ], [
      (val_add, "$last_player_trigger", 500),
      
      (try_begin),  #catch moment fighting starts
        (eq, "$clock_reset", 0),
        (call_script, "script_cf_any_fighting_moto"),
        (call_script, "script_cf_count_casualties_moto"),
        (assign, "$battle_phase", BP_Fight_MOTO),
      (try_end),
      
      (set_fixed_point_multiplier, 100),
      (call_script, "script_store_battlegroup_data_moto"),
      
      (try_begin),  #reassess ranged position when fighting starts
        (ge, "$battle_phase", BP_Fight_MOTO), #we have to do it this way because BP_Fight_MOTO may be set in ways other than casualties
        (eq, "$clock_reset", 0),
        (call_script, "script_field_tactics_moto", 1),
        (assign, "$ranged_clock", 0),
        (assign, "$clock_reset", 1),
        
      (else_try), #at longer intervals after setup...
        (ge, "$battle_phase", BP_Jockey_MOTO),
        (store_mul, ":five_sec_modulus", 5, Reform_Trigger_Modulus),
        (val_div, ":five_sec_modulus", formation_reform_interval),
        (store_mod, reg0, "$ranged_clock", ":five_sec_modulus"),
        # (eq, reg0, 0),  #MOTO uncomment this line if archers too fidgety
        
        #reassess archer position
        (call_script, "script_field_tactics_moto", 1),
        
        #catch reinforcements and set divisions to be retyped with new troops
        (try_begin),
          (neg|team_slot_eq, 0, slot_team_reinforcement_stage, "$defender_reinforcement_stage"),
          (team_set_slot, 0, slot_team_reinforcement_stage, "$defender_reinforcement_stage"),
          (try_for_range, ":division", 0, 9),
            (store_add, ":slot", slot_team_d0_type, ":division"),
            (team_set_slot, 0, ":slot", sdt_unknown),
            (team_set_slot, 2, ":slot", sdt_unknown),
          (try_end),
        (try_end),
        (try_begin),
          (neg|team_slot_eq, 1, slot_team_reinforcement_stage, "$attacker_reinforcement_stage"),
          (team_set_slot, 1, slot_team_reinforcement_stage, "$attacker_reinforcement_stage"),
          (try_for_range, ":division", 0, 9),
            (store_add, ":slot", slot_team_d0_type, ":division"),
            (team_set_slot, 1, ":slot", sdt_unknown),
            (team_set_slot, 3, ":slot", sdt_unknown),
          (try_end),
        (try_end),
        
      (else_try),
        (call_script, "script_field_tactics_moto", 0),
      (try_end),
      
      (try_begin),
        (eq, "$battle_phase", BP_Setup_MOTO),
        (assign, ":not_in_setup_position", 0),
        (try_for_range, ":bgteam", 0, 4),
          (neq, ":bgteam", "$fplayer_team_no"),
          (team_slot_ge, ":bgteam", slot_team_size, 1),
          (call_script, "script_battlegroup_get_position_moto", pos1, ":bgteam", grc_archers),
          (team_get_order_position, pos0, ":bgteam", grc_archers),
          (get_distance_between_positions, reg0, pos0, pos1),
          (gt, reg0, 500),
          (assign, ":not_in_setup_position", 1),
        (try_end),
        (eq, ":not_in_setup_position", 0),  #all AI reached setup position?
        (assign, "$battle_phase", BP_Jockey_MOTO),
      (try_end),
      
      (val_add, "$ranged_clock", 1),
  ]),
  
  # Trigger file: AI_hero_fallen
  #if AI to take over for mods with post-player battle action
  (0, 0, ti_once, [(eq, "$tld_option_formations", 2),
      (main_hero_fallen),
      (eq, "$FormAI_AI_Control_Troops", 1),
      ], [
      (set_show_messages, 0),
      #undo special player commands
      (team_set_order_listener, "$fplayer_team_no", grc_everyone),
      (team_give_order, "$fplayer_team_no", grc_everyone, mordr_use_any_weapon),
      (team_give_order, "$fplayer_team_no", grc_everyone, mordr_fire_at_will),
      
      #clear all scripted movement (for now)
      (call_script, "script_player_order_formations_moto", mordr_retreat),
      (set_show_messages, 1),
      
      (try_for_agents, ":agent"), #reassign agents to the divisions AI uses
        (agent_is_alive, ":agent"),
        (call_script, "script_agent_fix_division_moto", ":agent"),
      (try_end),
  ]),


# TLD Kham: Try to fix Flag Issue for New Formations

  (0, .3, 0, [(eq, "$tld_option_formations", 2),(game_key_clicked, gk_order_1)], [
    (game_key_is_down, gk_order_1), #player is holding down key?
    (assign, "$temp_action_cost", 1),
    #(display_message, "@{!}DEBUG: F1 Held"),
    (get_player_agent_no, ":player"), 
    (try_begin),
      (agent_slot_eq, ":player", slot_agent_tournament_point, 0),
      (eq, "$field_ai_horse_archer", 1),
      (agent_set_slot, ":player", slot_agent_tournament_point, 1),
      (assign, "$field_ai_horse_archer", 0),
    (try_end),
  ]),

(.5, 0, 0, [(eq, "$tld_option_formations", 2),(eq, "$temp_action_cost", 1),(neg|game_key_is_down, gk_order_1)], [   
    (assign, "$temp_action_cost", 0),
    #(display_message, "@{!}DEBUG: F1 Let Go"),
    (get_player_agent_no, ":player"),
    (try_begin),
      (agent_slot_eq, ":player", slot_agent_tournament_point, 1),
      (eq, "$field_ai_horse_archer", 0),
      (agent_set_slot, ":player", slot_agent_tournament_point, 0),
      (assign, "$field_ai_horse_archer", 1),
    (try_end),

  ]),

] #end AI triggers

common_after_mission_start = (
  ti_after_mission_start, 0, ti_once, [(eq, "$tld_option_formations", 2),], [
    (get_player_agent_no, "$fplayer_agent_no"),
    (try_begin),
      (eq, "$fplayer_agent_no", -1),
      (assign, "$fplayer_team_no", -1),
    (else_try),
      (agent_get_group, "$fplayer_team_no", "$fplayer_agent_no"),
    (try_end),
    # (agent_get_horse, ":horse", "$fplayer_agent_no"),
    # (agent_set_slot, "$fplayer_agent_no", slot_agent_horse, ":horse"),
    (set_fixed_point_multiplier, 100),
    (get_scene_boundaries, pos2, pos3),
    (position_get_x, "$g_bound_right", pos3),
    (position_get_y, "$g_bound_top", pos3),
    (position_get_x, "$g_bound_left", pos2),
    (position_get_y, "$g_bound_bottom", pos2),
])

utility_triggers = [  #1 trigger
  common_after_mission_start,
]

#to prevent presentations from starting while old ones are still running
common_presentation_switcher = (
  .05, 0, 0, [
    (eq, "$tld_option_formations", 2),
    (neq, "$switch_presentation_new", 0), #we can safely ignore prsnt_game_start
    (neg|is_presentation_active, "$switch_presentation_old"),
    ], [
    (start_presentation, "$switch_presentation_new"),
    (assign, "$switch_presentation_old", "$switch_presentation_new"), #this makes the heroic assumption that all presentations use this system
    (assign, "$switch_presentation_new", 0),
])

battle_panel_triggers = [ #4 triggers
  common_presentation_switcher,
  
  (ti_on_agent_spawn, 0, 0, [(eq, "$tld_option_formations", 2),], [
      (store_trigger_param_1, ":agent_no"),
      (agent_set_slot, ":agent_no", slot_agent_map_overlay_id, 0),
  ]),
  
  (0, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (game_key_clicked, gk_view_orders)
  ],[
      (try_begin),
        (is_presentation_active, "prsnt_battle"),
        (presentation_set_duration, 0),
        
      (else_try),
        (presentation_set_duration, 0),
        (assign, "$switch_presentation_new", "prsnt_battle"),
      (try_end),
  ]),
  
  # (0.1, 0, 0, [ this is left from Native code
      # (is_presentation_active, "prsnt_battle")
  # ],[
      # (call_script, "script_update_order_panel_statistics_and_map"),
  # ]),
]

extended_battle_menu = [  #15 triggers
  # Trigger file: extended_battle_menu_init
  (ti_before_mission_start ,0, ti_once, [(eq, "$tld_option_formations", 2),], [
      (assign, "$gk_order", 0), #tracks the first tier order given
      (assign, "$gk_order_hold_over_there", HOT_no_order),  #used to determine if F1 key is being held down
      (assign, "$native_opening_menu", 0),  #tracks whether the first tier battle menu would normally be showing
      (assign, "$g_presentation_active", 0),  #used here to track whether prsnt_battle is overridden when fake battle menu starts
  ]),
  
  common_presentation_switcher,
  
  # Trigger file: extended_battle_menu_division_selection
  (0,0,.1, [
      (eq, "$tld_option_formations", 2),
      (this_or_next|game_key_clicked, gk_group0_hear),
      (this_or_next|game_key_clicked, gk_group1_hear),
      (this_or_next|game_key_clicked, gk_group2_hear),
      (this_or_next|game_key_clicked, gk_group3_hear),
      (this_or_next|game_key_clicked, gk_group4_hear),
      (this_or_next|game_key_clicked, gk_group5_hear),
      (this_or_next|game_key_clicked, gk_group6_hear),
      (this_or_next|game_key_clicked, gk_group7_hear),
      (this_or_next|game_key_clicked, gk_group8_hear),
      (this_or_next|game_key_clicked, gk_reverse_order_group),  #shows up as "unknown 6" on Native screen
      (this_or_next|game_key_clicked, gk_everyone_around_hear),
      (game_key_clicked, gk_everyone_hear),
      (neg|main_hero_fallen),
      ],[
      (assign, "$gk_order", 0),
      # (try_begin), #InVain: Currently unused
        # (is_presentation_active, "prsnt_battle"),
        # (assign, "$g_presentation_active", 1),
      # (try_end),
      (try_begin),
        (presentation_set_duration, 0),
        (assign, "$switch_presentation_new", "prsnt_order_display"),
        # (try_begin), #InVain: unused
          # (gt, "$g_display_agent_labels", 0),
          # (eq, "$show_hide_labels", 1),
          # (start_presentation, "prsnt_display_agent_labels"),
        # (try_end),
      (try_end),
      (assign, "$native_opening_menu", 1),
      (try_begin),
        (eq, "$battle_phase", BP_Deploy),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (set_show_messages, 0),
          (call_script, "script_formation_to_native_order_moto", "$fplayer_team_no", ":division", ":formation"),  #force Native formation update to delink listening/non-listening
          (set_show_messages, 1),
        (try_end),
      (try_end),
  ]),
  
  # Trigger file: extended_battle_menu_tab_out
  # (ti_tab_pressed, 0, 0, [
  # (is_presentation_active, "prsnt_order_display"),
  # ],[
  # (assign, "$gk_order", 0),
  # (assign, "$native_opening_menu", 0),
  # (presentation_set_duration, 0),
  # ]),
  
  # Trigger file: extended_battle_menu_esc_or_die_out
  (0, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (this_or_next|main_hero_fallen),
      (key_is_down, key_escape),
      (is_presentation_active, "prsnt_order_display"),
      ],[
      (presentation_set_duration, 0),
      (assign, "$native_opening_menu", 0),
  ]),
  
  (0, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (this_or_next|main_hero_fallen),
      (key_is_down, key_escape),
      (neq, "$gk_order", 0),
      ],[
      (assign, "$gk_order", 0),
  ]),
  
  # Trigger file: extended_battle_menu_hold_F1
  (.1, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (neq, "$when_f1_first_detected", 0),
      # (store_application_time, reg0), #real time for when game time is slowed for real deployment
      (store_mission_timer_c_msec, reg0),
      (val_sub, reg0, "$when_f1_first_detected"),
      (ge, reg0, 250),  #check around .3 seconds later (Native trigger delay does not work right)
      (eq, "$gk_order", gk_order_1),  #next trigger set MOVE menu?
      ],[
      (assign, "$when_f1_first_detected", 0),
      
      (try_begin),
        (game_key_is_down, gk_order_1), #BUT player is holding down key?
        (assign, "$gk_order_hold_over_there", HOT_F1_held),
        (assign, "$gk_order", 0),
        
        (store_and, reg0, "$first_time", first_time_hold_F1),
        (try_begin),
          (eq, reg0, 0),
          (val_or, "$first_time", first_time_hold_F1),
          (dialog_box, "str_division_placement", "@Division Placement"),
        (try_end),
        
      (else_try),
        (eq, "$gk_order_hold_over_there", HOT_F1_pressed),
        (assign, "$gk_order_hold_over_there", HOT_no_order),
        (assign, "$gk_order", 0),
        (call_script, "script_player_order_formations_moto", mordr_hold),
      (try_end),
  ]),
  
  # Trigger file: extended_battle_menu_F1
  (0, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (game_key_clicked, gk_order_1),
      (neg|main_hero_fallen)
      ], [
      # (store_application_time, "$when_f1_first_detected"),
      (store_mission_timer_c_msec, "$when_f1_first_detected"),
      (try_begin),
        (neq, "$gk_order", gk_order_1),
        (neq, "$gk_order", gk_order_2),
        (neq, "$gk_order", gk_order_3),
        (assign, "$gk_order", gk_order_1),
        (assign, "$native_opening_menu", 0),
        (try_begin),
          (is_presentation_active, "prsnt_battle"),
          (assign, "$g_presentation_active", 1),
        (try_end),
        (presentation_set_duration, 0), #clear main menu additions
        (try_begin),
          (gt, "$g_display_agent_labels", 0),
          (eq, "$show_hide_labels", 1),
          (start_presentation, "prsnt_display_agent_labels"),
        (try_end),
        (assign, "$gk_order_hold_over_there", HOT_no_order),
      (else_try),
        (eq, "$gk_order", gk_order_1),  #HOLD
        (assign, "$gk_order_hold_over_there", HOT_F1_pressed),
      (else_try),
        (eq, "$gk_order", gk_order_2),  #ADVANCE
        (assign, "$gk_order", 0),
        (presentation_set_duration, 0), #clear F2 menu additions
        (call_script, "script_player_order_formations_moto", mordr_advance),
      (else_try),
        (eq, "$gk_order", gk_order_3),  #HOLD FIRE
        (assign, "$gk_order", 0),
      (try_end),
  ]),
  
  # Trigger file: extended_battle_menu_F2
  (0, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (game_key_clicked, gk_order_2),
      (neg|main_hero_fallen)
      ], [
      (try_begin),
        (neq, "$gk_order", gk_order_1),
        (neq, "$gk_order", gk_order_2),
        (neq, "$gk_order", gk_order_3),
        (assign, "$gk_order", gk_order_2),
        (assign, "$native_opening_menu", 0),
        (try_begin),
          (is_presentation_active, "prsnt_battle"),
          (assign, "$g_presentation_active", 1),
        (try_end),
        (presentation_set_duration, 0),
        (try_begin),
          (gt, "$g_display_agent_labels", 0),
          (eq, "$show_hide_labels", 1),
          (start_presentation, "prsnt_display_agent_labels"),
        (try_end),
        (assign, "$switch_presentation_new", "prsnt_order_display"),
      (else_try),
        (eq, "$gk_order", gk_order_1),  #FOLLOW
        (assign, "$gk_order", 0),
        (call_script, "script_player_order_formations_moto", mordr_follow),
      (else_try),
        (eq, "$gk_order", gk_order_2),  #FALL BACK
        (assign, "$gk_order", 0),
        (presentation_set_duration, 0), #clear F2 menu additions
        (call_script, "script_player_order_formations_moto", mordr_fall_back),
      (else_try),
        (eq, "$gk_order", gk_order_3),  #FIRE AT WILL
        (assign, "$gk_order", 0),
      (try_end),
  ]),
  
  # Trigger file: extended_battle_menu_F3
  (0, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (game_key_clicked, gk_order_3),
      (neg|main_hero_fallen)
      ], [
      (try_begin),
        (neq, "$gk_order", gk_order_1),
        (neq, "$gk_order", gk_order_2),
        (neq, "$gk_order", gk_order_3),
        (assign, "$gk_order", gk_order_3),
        (assign, "$native_opening_menu", 0),
        (try_begin),
          (is_presentation_active, "prsnt_battle"),
          (assign, "$g_presentation_active", 1),
        (try_end),
        (presentation_set_duration, 0), #clear main menu additions
        (try_begin),
          (gt, "$g_display_agent_labels", 0),
          (eq, "$show_hide_labels", 1),
          (start_presentation, "prsnt_display_agent_labels"),
        (try_end),
      (else_try),
        (eq, "$gk_order", gk_order_1),  #CHARGE
        (assign, "$gk_order", 0),
        (call_script, "script_player_order_formations_moto", mordr_charge),
      (else_try),
        (eq, "$gk_order", gk_order_2),  #SPREAD OUT
        (assign, "$gk_order", 0),
        (presentation_set_duration, 0), #clear F2 menu additions
        (call_script, "script_player_order_formations_moto", mordr_spread_out),
      (else_try),
        (eq, "$gk_order", gk_order_3),  #BLUNT WEAPONS
        (assign, "$gk_order", 0),
      (try_end),
  ]),
  
  # Trigger file: extended_battle_menu_F4
  (0, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (game_key_clicked, gk_order_4),
      (neg|main_hero_fallen)
      ], [
      (try_begin),
        (eq, "$gk_order", 0),
        (try_begin),
          (eq, "$FormAI_off", 0),
          (assign, "$gk_order", gk_order_4),
          (try_begin),
            (is_presentation_active, "prsnt_battle"),
            (assign, "$g_presentation_active", 1),
          (try_end),
          (presentation_set_duration, 0),
          (try_begin),
            (gt, "$g_display_agent_labels", 0),
            (eq, "$show_hide_labels", 1),
            (start_presentation, "prsnt_display_agent_labels"),
          (try_end),
          (assign, "$switch_presentation_new", "prsnt_order_display"),
          
          (store_and, reg0, "$first_time", first_time_formations),
          (try_begin),
            (eq, reg0, 0),
            (val_or, "$first_time", first_time_formations),
            (dialog_box, "str_formations", "@Complex Formations"),
          (try_end),
          
        (else_try),
          (display_message, "@Formations turned OFF in options menu"),
          (eq, "$native_opening_menu", 1),
          (try_begin),
            (is_presentation_active, "prsnt_battle"),
            (assign, "$g_presentation_active", 1),
          (try_end),
          (presentation_set_duration, 0),
          (assign, "$switch_presentation_new", "prsnt_order_display"),
        (try_end),
      (else_try),
        (eq, "$gk_order", gk_order_1),  #STAND GROUND
        (assign, "$gk_order", 0),
        (call_script, "script_player_order_formations_moto", mordr_stand_ground),
      (else_try),
        (eq, "$gk_order", gk_order_2),  #STAND CLOSER
        (assign, "$gk_order", 0),
        (presentation_set_duration, 0), #clear F2 menu additions
        (call_script, "script_player_order_formations_moto", mordr_stand_closer),
      (else_try),
        (eq, "$gk_order", gk_order_3),  #ANY WEAPON
        (assign, "$gk_order", 0),
      (else_try),
        (eq, "$gk_order", gk_order_4),  #FORMATION - RANKS
        (assign, "$gk_order", 0),
        (call_script, "script_division_reset_places_moto"),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          (call_script, "script_player_attempt_formation_moto", ":division", formation_ranks, 1),
        (try_end),
      (try_end),
  ]),
  
  # Trigger file: extended_battle_menu_F5
  (0, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (game_key_clicked, gk_order_5),
      (neg|main_hero_fallen)
      ], [
      (try_begin),
        (eq, "$gk_order", 0), #Redisplay
        (eq, "$native_opening_menu", 1),
        (try_begin),
          (is_presentation_active, "prsnt_battle"),
          (assign, "$g_presentation_active", 1),
        (try_end),
        (presentation_set_duration, 0),
        (try_begin),
          (gt, "$g_display_agent_labels", 0),
          (eq, "$show_hide_labels", 1),
          (start_presentation, "prsnt_display_agent_labels"),
        (try_end),
        (assign, "$switch_presentation_new", "prsnt_order_display"),
      (else_try),
        (eq, "$gk_order", gk_order_1),  #RETREAT
        (assign, "$gk_order", 0),
        (call_script, "script_player_order_formations_moto", mordr_retreat),
      (else_try),
        (eq, "$gk_order", gk_order_2),  #MOUNT
        (assign, "$gk_order", 0),
        (presentation_set_duration, 0), #clear F2 menu additions
      (else_try),
        (eq, "$gk_order", gk_order_4), #FORMATION - SHIELDWALL
        (assign, "$gk_order", 0),
        (call_script, "script_division_reset_places_moto"),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          (call_script, "script_player_attempt_formation_moto", ":division", formation_shield, 1),
        (try_end),
      (try_end),
  ]),
  
  # Trigger file: extended_battle_menu_F6
  (0, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (game_key_clicked, gk_order_6),
      (neg|main_hero_fallen)
      ], [
      (try_begin),
        (eq, "$gk_order", 0), #Redisplay
        (eq, "$native_opening_menu", 1),
        (try_begin),
          (is_presentation_active, "prsnt_battle"),
          (assign, "$g_presentation_active", 1),
        (try_end),
        (presentation_set_duration, 0),
        (try_begin),
          (gt, "$g_display_agent_labels", 0),
          (eq, "$show_hide_labels", 1),
          (start_presentation, "prsnt_display_agent_labels"),
        (try_end),
        (assign, "$switch_presentation_new", "prsnt_order_display"),
      (else_try),
        (eq, "$gk_order", gk_order_2),  #DISMOUNT
        (assign, "$gk_order", 0),
        (presentation_set_duration, 0), #clear F2 menu additions
        (call_script, "script_player_order_formations_moto", mordr_dismount),
      (else_try),
        (eq, "$gk_order", gk_order_4), #FORMATION - WEDGE
        (assign, "$gk_order", 0),
        (call_script, "script_division_reset_places_moto"),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          (call_script, "script_player_attempt_formation_moto", ":division", formation_wedge, 1),
        (try_end),
      (try_end),
  ]),
  
  # Trigger file: extended_battle_menu_F7
  (0, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (key_clicked, key_f7),
      (neg|main_hero_fallen)
      ], [
      (try_begin),
        (eq, "$gk_order", 0), #Redisplay
        (eq, "$native_opening_menu", 1),
        (try_begin),
          (is_presentation_active, "prsnt_battle"),
          (assign, "$g_presentation_active", 1),
        (try_end),
        (presentation_set_duration, 0),
        (try_begin),
          (gt, "$g_display_agent_labels", 0),
          (eq, "$show_hide_labels", 1),
          (start_presentation, "prsnt_display_agent_labels"),
        (try_end),
        (assign, "$switch_presentation_new", "prsnt_order_display"),
      (else_try),
        (eq, "$gk_order", gk_order_2),  #MEMORIZE DIVISION PLACEMENTS
        (call_script, "script_memorize_division_placements_moto"),
        
      (else_try),
        (eq, "$gk_order", gk_order_4), #FORMATION - SQUARE
        (assign, "$gk_order", 0),
        (call_script, "script_division_reset_places_moto"),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          (call_script, "script_player_attempt_formation_moto", ":division", formation_square, 1),
        (try_end),
      (try_end),
  ]),
  
  # Trigger file: extended_battle_menu_F8
  (0, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (key_clicked, key_f8),
      (neg|main_hero_fallen)
      ], [
      (try_begin),
        (eq, "$gk_order", 0), #Redisplay
        (eq, "$native_opening_menu", 1),
        (try_begin),
          (is_presentation_active, "prsnt_battle"),
          (assign, "$g_presentation_active", 1),
        (try_end),
        (presentation_set_duration, 0),
        (try_begin),
          (gt, "$g_display_agent_labels", 0),
          (eq, "$show_hide_labels", 1),
          (start_presentation, "prsnt_display_agent_labels"),
        (try_end),
        (assign, "$switch_presentation_new", "prsnt_order_display"),
      (else_try),
        (eq, "$gk_order", gk_order_2),  #FORGET DIVISION PLACEMENTS (WILL USE DEFAULT)
        (call_script, "script_default_division_placements_moto"),
      (else_try),
        (eq, "$gk_order", gk_order_4), #FORMATION - CANCEL
        (assign, "$gk_order", 0),
        (call_script, "script_player_order_formations_moto", mordr_charge),
      (try_end),
  ]),
  
  # Trigger file: extended_battle_menu_restore_prsnt_battle
  (0.7, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (eq, "$g_presentation_active", 1),
      (neg|is_presentation_active, "prsnt_order_display"), #InVain: Problem is that prsnt_order_display is disabled elsewhere, but only if divisions 1-3 are selected
      (eq, "$gk_order", 0),
      ],[
      #(presentation_set_duration, 0), #so we just disable the consequences, this looks somewhat better
      #(assign, "$switch_presentation_new", "prsnt_battle"),
      (assign, "$g_presentation_active", 0), #InVain: Makes this global ineffective, need to keep in mind for future
  ]),
]#end extended battle menu

#These triggers acquire division data
common_division_data = [  #4 triggers
  # Trigger file: common_division_data_ti_before_mission_start
  (ti_before_mission_start, 0, 0, [(eq, "$tld_option_formations", 2),], [
      (assign, "$last_player_trigger", -2),
      (try_for_range, ":team", 0, 4),
        (team_set_slot, ":team", slot_team_size, 0),
        (try_for_range, ":division", 0, 9),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (team_set_slot, ":team", ":slot", sdt_unknown),
        (try_end),
      (try_end),
  ]),
  
  # Trigger file: common_division_data_ti_after_mission_start
  (0, .2, ti_once, [(eq, "$tld_option_formations", 2),(mission_tpl_are_all_agents_spawned)], [  #only 300 or so agents are spawned by ti_after_mission_start
      (try_for_agents, ":agent"),
        (agent_is_human, ":agent"),
        (try_begin),
          (multiplayer_get_my_player, ":player"),
          (player_is_active, ":player"),
          (player_get_agent_id, ":player_agent", ":player"),
          (eq, ":agent", ":player_agent"),
          (assign, "$fplayer_agent_no", ":player_agent"),
          (player_get_team_no,  "$fplayer_team_no", ":player"),
        (else_try),
          (agent_is_non_player, ":agent"),
          (agent_get_group, ":team", ":agent"),
          (gt, ":team", -1),  #not a MP spectator
          (call_script, "script_agent_fix_division_moto", ":agent"), #Division fix
        (try_end),
      (try_end),
      
      (try_begin),
        (neg|game_in_multiplayer_mode),
        (set_fixed_point_multiplier, 100),
        (call_script, "script_store_battlegroup_data_moto"),
        
        #get modal team faction
        (store_sub, ":num_kingdoms", kingdoms_end, kingdoms_begin),
        (store_mul, ":end", 4, ":num_kingdoms"),
        (try_for_range, ":slot", 0, ":end"),
          (team_set_slot, scratch_team, ":slot", 0),
        (try_end),
        (try_for_agents, ":cur_agent"),
          (agent_is_human, ":cur_agent"),
          (agent_get_group, ":cur_team", ":cur_agent"),
          (agent_get_troop_id, ":cur_troop", ":cur_agent"),
          (store_troop_faction, ":cur_faction", ":cur_troop"),
          (is_between, ":cur_faction", kingdoms_begin, kingdoms_end),
          (store_mul, ":slot", ":cur_team", ":num_kingdoms"),
          (val_sub, ":cur_faction", kingdoms_begin),
          (val_add, ":slot", ":cur_faction"),
          (team_get_slot, ":count", scratch_team, ":slot"),
          (val_add, ":count", 1),
          (team_set_slot, scratch_team, ":slot", ":count"),
        (try_end),
        
        (try_for_range, ":team", 0, 4),
          (team_slot_ge, ":team", slot_team_size, 1),
          (team_get_leader, ":fleader", ":team"),
          (try_begin),
            (ge, ":fleader", 0),
            (agent_get_troop_id, ":fleader_troop", ":fleader"),
            (store_troop_faction, ":team_faction", ":fleader_troop"),
          (else_try),
            (assign, ":team_faction", 0),
            (assign, ":modal_count", 0),
            (store_mul, ":begin", ":team", ":num_kingdoms"),
            (store_add, ":end", ":begin", ":num_kingdoms"),
            (try_for_range, ":slot", ":begin", ":end"),
              (team_get_slot, ":count", scratch_team, ":slot"),
              (gt, ":count", ":modal_count"),
              (assign, ":modal_count", ":count"),
              (store_sub, ":team_faction", ":begin", ":slot"),
              (val_add, ":team_faction", kingdoms_begin),
            (try_end),
          (try_end),
          (team_set_slot, ":team", slot_team_faction, ":team_faction"),
        (try_end),
      (try_end),
      
      (val_add, "$last_player_trigger", 1), #signal .5 sec trigger to start
  ]),
  
  #catch spawning agents after initial setup
  (ti_on_agent_spawn, 0, 0, [(eq, "$tld_option_formations", 2),(call_script, "script_cf_division_data_available_moto")], [
      (store_trigger_param_1, ":agent"),
      (call_script, "script_agent_fix_division_moto", ":agent"), #Division fix
  ]),
  
  # Trigger file: common_division_data_regular_trigger
  (0.5, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (neq, "$last_player_trigger", -2),
      (neg|main_hero_fallen),
      ],[
      (set_fixed_point_multiplier, 100),
      (store_mission_timer_c_msec, "$last_player_trigger"),
      
      (try_begin),  #set up revertible types for type check
        (try_for_range, ":team", 0, 4),
          (try_for_range, ":division", 0, 9),
            (store_add, ":slot", slot_team_d0_type, ":division"),
            (this_or_next|team_slot_eq, ":team", ":slot", sdt_skirmisher),
            (team_slot_eq, ":team", ":slot", sdt_harcher),
            (team_set_slot, ":team", ":slot", sdt_unknown),
          (try_end),
        (try_end),
      (try_end),
      
      (call_script, "script_store_battlegroup_data_moto"),
  ]),
]#end common division data

#These triggers process non-Native orders to divisions
#divorced from whatever command or AI interface (the back end)
division_order_processing = [ #4 triggers
  # Trigger file: division_order_processing_before_mission_start
  (ti_before_mission_start, 0, ti_once, [(eq, "$tld_option_formations", 2),], [
      (assign, "$g_division_order_processing", 1),  #flag showing these functions are active
      
      (try_for_range, ":team", 0, 4),
        (try_for_range, reg0, slot_team_d0_target_team, slot_team_d0_target_team+9),
          (team_set_slot, ":team", reg0, -1),
        (try_end),
        
        #represent Native initial state
        (try_begin),
          (eq, Native_Formations_Implementation, WFaS_Implementation),
          (try_for_range, reg0, slot_team_d0_formation, slot_team_d0_formation+9),
            (team_set_slot, ":team", reg0, formation_2_row),
          (try_end),
          (try_for_range, reg0, slot_team_d0_formation_num_ranks, slot_team_d0_formation_num_ranks+9),
            (team_set_slot, ":team", reg0, 2),
          (try_end),
          (try_for_range, reg0, slot_team_d0_formation_space, slot_team_d0_formation_space+9),
            (team_set_slot, ":team", reg0, 1),
          (try_end),
          
        (else_try),
          (try_for_range, reg0, slot_team_d0_formation, slot_team_d0_formation+9),
            (team_set_slot, ":team", reg0, formation_none),
          (try_end),
        (try_end),
        
        (try_for_range, reg0, slot_team_d0_move_order, slot_team_d0_move_order+9),
          (team_set_slot, ":team", reg0, mordr_charge),
        (try_end),
      (try_end),
  ]),
  
  # Trigger file: division_order_processing_one_second
  (1, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (eq, "$g_battle_result", 0),
      (call_script, "script_cf_division_data_available_moto"),
      ],[
      (set_fixed_point_multiplier, 100),
      
      (call_script, "script_team_get_position_of_enemies_moto", Enemy_Team_Pos_MOTO, "$fplayer_team_no", grc_everyone),
      (assign, ":num_enemies", reg0),
      
      (try_begin),
        (gt, ":num_enemies", 0),
        (call_script, "script_process_player_division_positioning_moto"),
      (try_end),
      
      # (try_begin),
      # (call_script, "script_cf_order_active_check", slot_team_d0_order_skirmish),
      # (call_script, "script_order_skirmish_skirmish"),
      # (try_end),
      
      (val_add, "$last_player_trigger", 500),
  ]),
  
  (ti_tab_pressed, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (this_or_next|main_hero_fallen),
      (eq, "$g_battle_result", 1),
      ],[
      (assign, "$g_division_order_processing", 0),
  ]),
  
  (ti_question_answered, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (store_trigger_param_1, ":answer"),
      (eq, ":answer", 0),
      ], [
      (assign, "$g_division_order_processing", 0),
  ]),
]#end division order processing

#These triggers allow player to set up troops before a battle
real_deployment = [ #3 triggers
  # Trigger file: real_deployment_after_mission_start
  (ti_after_mission_start, 0, 0, [
      (eq, "$tld_option_formations", 2),
      (neq, "$player_deploy_troops", 0),
      ],[
      # (call_script, "script_init_overhead_camera"),
      (assign, "$battle_phase", BP_Init),
      #(assign, "$player_deploy_troops", 0),
  ]),
  
  # Trigger file: real_deployment_init
  (0, 0, ti_once, [
      (eq, "$tld_option_formations", 2),
      (eq, "$battle_phase", BP_Init),
      (call_script, "script_cf_division_data_available_moto"),
      # (eq, "$g_division_order_processing", 1),  #division_order_processing inits are done
      ],[
      # (assign, "$g_battle_command_presentation", bcp_state_order_groups),
      # (rebuild_shadow_map),
      (try_begin),
        (eq, "$g_division_order_processing", 1),  #division_order_processing inits are done
        (gt, "$fplayer_team_no", -1),
        
        #place divisions
        (set_fixed_point_multiplier, 100),
        (call_script, "script_division_reset_places_moto"),
        (call_script, "script_field_start_position_moto", "$fplayer_team_no"),  #returns pos2
        (copy_position, Target_Pos, pos2),
        
        (try_for_range_backwards, ":division", 0, 9),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_slot_ge, "$fplayer_team_no", ":slot", 1), #division exists
          (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":division"),
          (faction_get_slot, ":formation_is_memorized", "fac_player_faction", ":slot"),
          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_get_slot, ":current_spacing", "$fplayer_team_no", ":slot"),
          
          (try_begin),
            (neq, ":formation_is_memorized", 0),
            (store_add, ":slot", slot_faction_d0_mem_formation, ":division"),
            (faction_get_slot, ":formation", "fac_player_faction", ":slot"),
            (store_add, ":slot", slot_team_d0_formation, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":formation"), #do this here to prevent script_player_attempt_formation from resetting spacing
            
            (store_add, ":slot", slot_faction_d0_mem_formation_space, ":division"),
            (faction_get_slot, ":memorized_spacing", "fac_player_faction", ":slot"),
            
            #bring unformed divisions into sync with formations' minimum
            (set_show_messages, 0),
            (try_begin),
              (ge, ":memorized_spacing", ":current_spacing"),
              (try_for_range, reg0, ":current_spacing", ":memorized_spacing"),
                (team_give_order, "$fplayer_team_no", ":division", mordr_spread_out),
              (try_end),
            (else_try),
              (try_for_range, reg0, ":memorized_spacing", ":current_spacing"),
                (team_give_order, "$fplayer_team_no", ":division", mordr_stand_closer),
              (try_end),
            (try_end),
            (set_show_messages, 1),
            (store_add, ":slot", slot_team_d0_formation_space, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":memorized_spacing"),
            
            (try_begin),
              (gt, ":formation", formation_none),
              (assign, reg1, ":division"),
              (str_store_class_name, s2, reg1),
              (val_add, reg1, 1),
              (display_message, "@Division {reg1} {s2} goes to its memorized position..."),
              (call_script, "script_player_attempt_formation_moto", ":division", ":formation", 0),
            (else_try),
              (call_script, "script_formation_to_native_order_moto", "$fplayer_team_no", ":division", ":formation"),
              (call_script, "script_battlegroup_place_around_leader_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no"),
              
              (eq, Native_Formations_Implementation, WB_Implementation),
              (assign, reg0, ":memorized_spacing"),
              (assign, reg1, ":division"),
              (str_store_class_name, s2, reg1),
              (val_add, reg1, 1),
              (try_begin),
                (ge, reg0, 0),
                (display_message, "@Division {reg1} {s2} forms line (memorized)."),
              (else_try),
                (val_mul, reg0, -1),
                (val_add, reg0, 1),
                (display_message, "@Division {reg1} {s2} forms {reg0} lines (memorized)."),
              (try_end),
            (try_end),
            
          (else_try),
            (team_set_order_listener, "$fplayer_team_no", ":division"), #pick one division to listen; otherwise player agent gets moved as if part of infantry
            (store_add, ":slot", slot_team_d0_type, ":division"),
            
            (eq, "$FormAI_off", 0),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
            (call_script, "script_player_attempt_formation_moto", ":division", formation_wedge, 2),
            
          (else_try),
            (eq, "$FormAI_off", 0),
            (neg|team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
            (neg|team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
            (call_script, "script_get_default_formation_moto", "$fplayer_team_no"), #defined only for infantry
            (assign, ":formation", reg0),
            (gt, ":formation", formation_none),
            (call_script, "script_player_attempt_formation_moto", ":division", ":formation", 2),
            
            #Native defaults
          (else_try),
            (call_script, "script_pick_native_formation_moto", "$fplayer_team_no", ":division"),
            (assign, ":formation", reg0),
            (assign, ":ranks", reg1),
            (store_add, ":slot", slot_team_d0_formation, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":formation"),
            (store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":ranks"),
            (copy_position, pos1, Target_Pos),
            (call_script, "script_battlegroup_place_around_pos1_moto", "$fplayer_team_no", ":division", "$fplayer_agent_no"),
            (call_script, "script_formation_to_native_order_moto", "$fplayer_team_no", ":division", ":formation"),  #also forces reset for agent_get_position_in_group
            
            # (eq, Native_Formations_Implementation, WB_Implementation),  info overload?
            # (assign, reg0, ":current_spacing"),
            # (assign, reg1, ":division"),
            # (str_store_class_name, s2, reg1),
            # (val_add, reg1, 1),
            # (try_begin),
            # (ge, reg0, 0),
            # (display_message, "@Division {reg1} {s2} forms line."),
            # (else_try),
            # (val_mul, reg0, -1),
            # (val_add, reg0, 1),
            # (display_message, "@Division {reg1} {s2} forms {reg0} lines."),
            # (try_end),
          (try_end),
        (try_end),  #division loop
        
        # #Tactics-Based number of orders and placement limit
        # (try_begin),
        # (eq, "$g_is_quick_battle", 1),
        # (assign, ":num_orders", 3),
        # (else_try),
        # (party_get_skill_level, reg0, "p_main_party", "skl_tactics"),
        # (assign, ":num_orders", reg0),
        # (try_end),
        # # (team_set_slot, 6, slot_team_mv_temp_placement_counter, ":num_orders"), DEPRECATED
        
        # (store_add, ":times_ten_meters", ":num_orders", 2), #this makes base placement radius 20m
        # (store_mul, "$division_placement_limit", ":times_ten_meters", 1000),
        # (call_script, "script_team_get_position_of_enemies_moto", pos1, "$fplayer_team_no", grc_everyone),
        # (call_script, "script_battlegroup_get_position_moto", pos2, "$fplayer_team_no", grc_everyone),
        # (get_distance_between_positions, reg0, pos1, pos2),
        # (val_div, reg0, 3),
        # (val_min, "$division_placement_limit", reg0), #place no closer than 1/3 the distance between
        
        # #make placement border
        # (store_mul, ":num_dashes", 2, "$division_placement_limit"),
        # (val_mul, ":num_dashes", 314, "$division_placement_limit"),
        # (val_div, ":num_dashes", 100*400),  #number of 4-meters in circumference
        # (store_div, ":hundredths_degree", 36000, ":num_dashes"),
        # (agent_get_position, pos1, "$fplayer_agent_no"),
        # (try_for_range, reg1, 0, ":num_dashes"),
        # (position_rotate_z_floating, pos1, ":hundredths_degree"),
        # (copy_position, pos0, pos1),
        # (position_move_y, pos0, "$division_placement_limit"),
        # (position_move_x, pos0, -100),  #center the 200cm dash to avoid sawtooth effect
        # (position_set_z_to_ground_level, pos0),
        # (position_move_z, pos0, 50),
        # (set_spawn_position, pos0),
        # (spawn_scene_prop, "spr_deployment_boundary"),
        # (prop_instance_set_scale, reg0, 2000, 10000, 1),  #going for 2 meter dash
        # (try_end),
      (try_end),  #valid player team
      # ]),
      
      # # Trigger file: real_deployment_stop_time
      # (0, 0, ti_once, [
      # (eq, "$g_battle_command_presentation", bcp_state_order_groups), #wait til the above trigger fires
      # ],[
      (assign, "$battle_phase", BP_Deploy),
      # (set_fixed_point_multiplier, 1000),
      # (party_get_slot, reg0, "p_main_party", slot_party_pref_rdep_time_scale),
      # (try_begin),
      # (eq, reg0, 1),
      # (mission_set_time_speed, 5),
      # (else_try),
      # (eq, reg0, 2),
      # (mission_set_time_speed, 10),
      # (else_try),
      # (mission_set_time_speed, 1),
      # (try_end),
  ]),
  
  # # Trigger file: real_deployment_process_divisions
  # (0, 0, 0, [
  # (eq, "$battle_phase", BP_Deploy),
  # # (team_slot_ge, 6, slot_team_mv_temp_placement_counter, 1), ## Error Check to be sure placements remain
  # ],[
  # (set_fixed_point_multiplier, 100),
  # (try_begin),
  # (eq, "$BCP_mouse_state", HOT_F1_held),
  # (prop_instance_get_position, pos1, "$g_objects_selector"),
  # (set_show_messages, 0),
  # (try_for_range, ":division", 0, 9),
  # (store_add, ":slot", slot_team_d0_size, ":division"),
  # (team_slot_ge, "$fplayer_team_no", ":slot", 1), #division exists
  # (class_is_listening_order, "$fplayer_team_no", ":division"),
  # (team_set_order_position, "$fplayer_team_no", ":division", pos1),
  # (try_end),
  # (call_script, "script_process_place_divisions_moto"),
  # (set_show_messages, 1),
  # (try_end),
  # (call_script, "script_process_player_division_positioning_moto"),
  # (call_script, "script_prebattle_agents_set_start_positions", "$fplayer_team_no")
  # ]),
  
  # Trigger file: real_deployment_end
  (0, 0, ti_once, [
      (eq, "$tld_option_formations", 2),
      (eq, "$battle_phase", BP_Deploy),
      # (this_or_next|eq, "$g_battle_command_presentation", bcp_state_off),
      # (neg|team_slot_ge, 6, slot_team_mv_temp_placement_counter, 1),
      ],[
      (assign, "$battle_phase", BP_Setup_MOTO),
      # (set_fixed_point_multiplier, 10),
      # (mission_set_time_speed, 10),
      # (assign, "$g_battle_command_presentation", bcp_state_off),
      # (try_begin),
      # (is_presentation_active, "prsnt_battle_command"),
      # (presentation_set_duration, 0),
      # (try_end),
      # (assign, "$BCP_pointer_available", 0),
      # # (scene_prop_set_visibility, "$g_objects_selector", 0),
      (get_player_agent_no, ":agent"),
      (gt, ":agent", -1),
      (agent_get_team, reg0, ":agent"),
      # (team_set_order_listener, reg0, -1),
      (team_set_order_listener, reg0, grc_everyone),
      # (try_for_prop_instances, ":prop_instance", "spr_deployment_boundary"),
      # (scene_prop_fade_out, ":prop_instance", 2),
      # (try_end),
      # (assign, "$g_custom_camera_regime", normal_camera),
      # (mission_cam_set_mode, 0, 1000, 1)
  ]),
  
  # # Trigger file: real_deployment_rebuild_shadows
  # (0, 2, ti_once, [
  # (ge, "$battle_phase", BP_Setup_MOTO),
  # ],[
  # (try_for_prop_instances, ":prop_instance", "spr_deployment_boundary"),
  # (scene_prop_set_visibility, ":prop_instance", 0),
  # (try_end),
  # (rebuild_shadow_map),
  # ]),
]

formations_triggers_moto = [ #4 triggers
  # Trigger file: formations_before_mission_start
  (ti_before_mission_start, 0, 0, [(eq, "$tld_option_formations", 2),], [
      (try_for_range, ":team", 0, 4),
        (try_for_range, ":division", 0, 9),
          (store_add, ":slot", slot_team_d0_speed_limit, ":division"),
          (team_set_slot, ":team", ":slot", 10),
          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, ":team", ":slot", 1),
        (try_end),
      (try_end),
      
      #(call_script, "script_init_noswing_weapons"),
  ]),
  
  #kludge formation superiority
#  (ti_on_agent_hit, 0, 0, [
#      (eq, "$tld_option_formations", 2),
#      (store_trigger_param, ":missile", 5),
#      (le, ":missile", 0),
#      (store_trigger_param_1, ":inflicted_agent_id"),
#      (agent_is_active,":inflicted_agent_id"),
#      (agent_is_human, ":inflicted_agent_id"),
#      (agent_is_alive, ":inflicted_agent_id"),
#    ], [
#      (store_trigger_param_1, ":inflicted_agent_id"),
#      (store_trigger_param_2, ":dealer_agent_id"),
#      (store_trigger_param, ":inflicted_damage", 3),
#      
#      (try_begin),
#        (neq, ":inflicted_agent_id", "$fplayer_agent_no"),
#        (neq, ":dealer_agent_id", "$fplayer_agent_no"),
#        
#        (agent_get_team, ":inflicted_team", ":inflicted_agent_id"),
#        (agent_get_division, ":inflicted_division", ":inflicted_agent_id"),
#        (store_add, ":slot", slot_team_d0_formation, ":inflicted_division"),
#        (team_get_slot, ":inflicted_formation", ":inflicted_team", ":slot"),
#        
#        (agent_get_team, ":dealer_team", ":dealer_agent_id"),
#        (agent_get_division, ":dealer_division", ":dealer_agent_id"),
#        (store_add, ":slot", slot_team_d0_formation, ":dealer_division"),
#        (team_get_slot, ":dealer_formation", ":dealer_team", ":slot"),
#        
#        (try_begin),
#          (eq, ":inflicted_formation", 0),
#          (neq, ":dealer_formation", 0),
#          
#          (store_add, ":slot", slot_team_d0_percent_in_place, ":dealer_division"),
#          (team_slot_ge, ":dealer_team", ":slot", 80),
#          
#          (store_add, ":slot", slot_team_d0_formation_space, ":dealer_division"),
#          (team_get_slot, ":spacing", ":dealer_team", ":slot"),
#          
#          (try_begin),
#            (eq, ":spacing", 0),
#            (val_mul, ":inflicted_damage", 6),
#          (else_try),
#            (eq, ":spacing", 1),
#            (val_mul, ":inflicted_damage", 5),
#          (else_try),
#            (val_mul, ":inflicted_damage", 4),
#          (try_end),
#          (val_div, ":inflicted_damage", 2),
#          
#        (else_try),
#          (neq, ":inflicted_formation", 0),
#          (eq, ":dealer_formation", 0),
#          
#          (store_add, ":slot", slot_team_d0_percent_in_place, ":inflicted_division"),
#          (team_slot_ge, ":inflicted_team", ":slot", 80),
#          
#          (store_add, ":slot", slot_team_d0_formation_space, ":inflicted_division"),
#          (team_get_slot, ":spacing", ":inflicted_team", ":slot"),
#          
#          (val_mul, ":inflicted_damage", 2),
#          (try_begin),
#            (eq, ":spacing", 0),
#            (val_div, ":inflicted_damage", 6),
#          (else_try),
#            (eq, ":spacing", 1),
#            (val_div, ":inflicted_damage", 5),
#          (else_try),
#            (val_div, ":inflicted_damage", 4),
#          (try_end),
#          
#          (val_max, ":inflicted_damage", 1),
#        (try_end),
#      (try_end),
#      
#      (set_trigger_result, ":inflicted_damage"),
#  ]),
  
  # Trigger file: formations_victory_trigger
  (2, 0, ti_once, [
      (eq, "$tld_option_formations", 2),
      (eq, "$g_battle_result", 1),
      ],[
      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),
        (call_script, "script_formation_end_moto", "$fplayer_team_no", ":division"),
      (try_end),
  ]),
  
  # Trigger file: formations_on_agent_killed_or_wounded
#  (ti_on_agent_killed_or_wounded, 0, 0, [(eq, "$tld_option_formations", 2),], [ #prevent leaving noswing weapons around for player to pick up
#      (store_trigger_param_1, ":dead_agent_no"),
#      (call_script, "script_switch_from_noswing_weapons_moto", ":dead_agent_no"),
#  ]),
]#end formations triggers

