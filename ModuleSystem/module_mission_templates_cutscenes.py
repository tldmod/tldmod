from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *

from module_info import wb_compile_switch as is_a_wb_cutscene


#swy-- macro to select exit mode on all the cutscenes, that way we maintain compatibility and still works well in both games.
#swy-- this also makes the HP UI visible again, controlled by shader uniforms.
return_exit_macro = (is_a_wb_cutscene==1 and [ (set_fixed_point_multiplier, 100),
                                               (set_shader_param_float, "@swy_ui_opacity", 100), #rustic equivalent to 1.0f = 0xff = 255 alpha = show it!
                                               (jump_to_menu, "mnu_auto_return_to_map") ]
                                               
                                          or [ (change_screen_return) ])
                                          
#swy-- this restores the cutscene presentation in WB after coming back from the Esc menu...
guard_against_esc = (is_a_wb_cutscene==1 and [ (try_begin),
                                                (neg|is_presentation_active, "prsnt_conversation_titles"),
                                                (start_presentation, "prsnt_conversation_titles"),
                                               (try_end) ]
                                          or [])


fade_cutscene =  ((is_a_wb_cutscene==1) and [

        (ti_after_mission_start, 0, 0, [],
          [(mission_cam_set_screen_color,        0xFF000000), 
           (mission_cam_animate_to_screen_color, 0x00000000, 1500)])
        
        ] or [])

mission_templates_cutscenes = [

("intro_rohan", 0, -1,
    "Intro cutscene mission",
    [(0,mtef_visitor_source|mtef_team_2,0,0,1,[]),
     (1,mtef_visitor_source|mtef_team_2,0,0,1,[]),
    ], fade_cutscene+
    [
    (ti_tab_pressed, 0, 0, [],[(finish_mission,0),(jump_to_menu, "mnu_auto_intro_gondor"),]),
    
    (ti_before_mission_start, 0, 0, [],
      [ #remove cabbage guard spawn points
        (replace_scene_props, "spr_troop_archer", "spr_empty"),
        (replace_scene_props, "spr_troop_castle_guard", "spr_empty"),
        (replace_scene_props, "spr_troop_guard", "spr_empty"),
        
        (assign, "$g_tld_intro_state", 0),
        # all friends with player
        (team_set_relation, 0, 2, 1),
        (team_set_relation, 1, 2, 1),
        
        (music_set_situation, 0),
        (play_sound, "snd_elves_occasional"),
      ]),
      
      (0, 0, ti_once,
       [(start_presentation, "prsnt_intro_titles"),
        
        #spawn people
        (set_fixed_point_multiplier, 100),
        (init_position, pos1),
        (position_set_x, pos1, 4500),
        (position_set_y, pos1, 3900),
        (position_rotate_z, pos1, -20),
        (set_spawn_position, pos1),
        (spawn_agent, "trp_walker_man_rohan_t"), #has to be in a condition block, or it will crash
        (agent_set_team, reg0, 0),
        (agent_set_stand_animation, reg0, "anim_stand_man"),
        (agent_set_hit_points, reg0, 0, 1),
        (position_move_y, pos1, 200),
        (position_rotate_z, pos1, 180),
        (set_spawn_position, pos1),
        (spawn_agent, "trp_walker_woman_rohan_d"),
        (agent_set_team, reg0, 0),
        (agent_set_stand_animation, reg0, "anim_stand_man"),
        (agent_set_hit_points, reg0, 0, 1),
       ],[]),

      # detect player camera init
      (0, 0, ti_once,
        [
         (mission_cam_get_position, pos1),
         (position_get_z, ":z_pos", pos1),
         (neq, ":z_pos", 0),       
        ],
        [
         (assign, "$g_tld_intro_state", 1),
        ]),
      
      (0, 0, 0,
       [
         (set_show_messages, 0),
         (store_mission_timer_a, ":cur_time"),
         (store_mission_timer_b, ":cur_time_b"),
         (set_fixed_point_multiplier, 100),
         # make player agent static
         (get_player_agent_no, ":player_agent"),
         (agent_get_horse, ":horse_agent", ":player_agent"),					
         (try_begin),
           (eq, ":horse_agent", -1),
         #swy-- for M&B 1.011 we use anim_stand, and for WB anim_stand_cutscene
         ]+(is_a_wb_cutscene==0 and 
          [(agent_set_animation, ":player_agent", "anim_stand")]
            or
          [(agent_set_animation, ":player_agent", "anim_stand_cutscene")]
         )+[
         #swy-- here it finishes, just in case
         (else_try),
           (agent_set_animation, ":player_agent", "anim_ride_0"),
           (agent_set_animation, ":horse_agent", "anim_horse_stand"),
         (try_end),
         
         # peasants run!
         (init_position, pos1),
         (position_set_x, pos1, 4500),
         (position_set_y, pos1, 5500),
         (try_begin),
           (ge, "$g_tld_intro_state", 4),
           (try_for_agents, ":agent_no"), 
             (agent_get_team, ":team", ":agent_no"),
             (eq, ":team", 0),
             (agent_set_scripted_destination, ":agent_no", pos1, 1),
           (try_end),
         (try_end),
         
         (try_begin),
           (eq, "$g_tld_intro_state", 1), #look at the sky
           #(ge, ":cur_time", 1), #replaced by detection of player camera init
           (mission_cam_set_mode, 1),
           (init_position, pos1),
           (position_rotate_z, pos1, 90),
           (position_rotate_x, pos1, 45),
           (position_set_x, pos1, 5000),
           (position_set_y, pos1, 4000),
           (position_set_z, pos1,  800),
           (mission_cam_set_position, pos1),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 2), #pan to farmers
           (ge, ":cur_time", 4),
           (init_position, pos1),
           (position_rotate_z, pos1, 90),
           (position_rotate_x, pos1, -15),
           (position_set_x, pos1, 5000),
           (position_set_y, pos1, 4000),
           (position_set_z, pos1,  800),
           (mission_cam_animate_to_position, pos1, 3000, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 3), #warg riders attack peasants
           (ge, ":cur_time", 9),
           (play_sound, "snd_warg_lone_woof"),
           (play_sound, "snd_warg_lone_woof"),
           (play_sound, "snd_warg_lone_woof"),
           (play_cue_track, "track_victorious_evil2"),
           (init_position, pos1),
           (position_set_x, pos1, 4600),
           (position_set_y, pos1,  100),
           (set_spawn_position, pos1),
           (try_for_range, ":unused", 0, 10),
             (spawn_agent, "trp_ac3_isen_warg_rider"),
             (agent_set_team, reg0, 1),
           (try_end),
           (try_for_agents, ":agent_no"), # peasants run and scream!
             (agent_get_team, ":team", ":agent_no"),
             (eq, ":team", 0),
             (agent_get_troop_id, ":troop", ":agent_no"),
             (troop_get_type, ":is_female", ":troop"),
             (try_begin),
               (eq, ":is_female", 1),
               (agent_play_sound, ":agent_no", "snd_horror_scream_woman"),
             (else_try),
               (agent_play_sound, ":agent_no", "snd_horror_scream_man"),
             (try_end),
           (try_end),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 4), #pan to battle
           (ge, ":cur_time", 10),
           (init_position, pos1),
           (position_rotate_z, pos1, 180),
           (position_rotate_x, pos1, -15),
           (position_set_x, pos1, 4500),
           (position_set_y, pos1, 5700),
           (position_set_z, pos1, 1200),
           (mission_cam_animate_to_position, pos1, 5000, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 5), #peasants dead? do a flyby
           (num_active_teams_le, 2),
           (init_position, pos1),
           (position_set_x, pos1, 10000),
           (position_set_y, pos1, 4500),
           (try_for_agents, ":agent_no"), # warg riders ride away
             (agent_get_team, ":team", ":agent_no"),
             (eq, ":team", 1),
             (agent_set_scripted_destination, ":agent_no", pos1, 1),
           (try_end),
           (ge, ":cur_time", 20),
           (init_position, pos1),
           (position_rotate_z, pos1, 180),
           (position_rotate_x, pos1, 60),
           (position_set_x, pos1, 4500),
           (position_set_y, pos1,  100),
           (position_set_z, pos1, 2200),
           (mission_cam_animate_to_position, pos1, 4000, 0),
           (reset_mission_timer_b),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 6), #finish
           (ge, ":cur_time_b", 4),
           (finish_mission, 0),
           (val_add, "$g_tld_intro_state", 1),
           #chain to next intro mission
           (jump_to_menu, "mnu_auto_intro_gondor"), #GA: Minas Tirith causes crashes for many people
         (try_end),
         ], []),
    ],
),

("intro_gondor", 0, -1,
    "Intro cutscene mission",
    [(0,mtef_visitor_source|mtef_team_0,0,0,1,[]),
     (1,mtef_visitor_source|mtef_team_0,0,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (8 ,mtef_scene_source,af_override_horse,0,1,[]),
     (9 ,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,0,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_scene_source,0,0,1,[]),(14,mtef_scene_source,0,0,1,[]),(15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,0,0,1,[]),(17,mtef_visitor_source,0,0,1,[]),(18,mtef_visitor_source,0,0,1,[]),(19,mtef_visitor_source,0,0,1,[]),(20,mtef_visitor_source,0,0,1,[]),(21,mtef_visitor_source,0,0,1,[]),(22,mtef_visitor_source,0,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),(25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,0,1,[]),(28,mtef_visitor_source,af_override_horse,0,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     (32,mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),(33,mtef_visitor_source,af_override_horse|af_override_weapons,0,1,[]),(34,mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),(35,mtef_visitor_source,af_override_horse|af_override_weapons,0,1,[]),(36,mtef_visitor_source,af_override_horse,0,1,[]),(37,mtef_visitor_source,af_override_horse|af_override_head,0,1,[]),(38,mtef_visitor_source,af_override_horse|af_override_weapons,0,1,[]),(39,mtef_visitor_source,af_override_horse,0,1,[]),
     (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ], fade_cutscene+
    [
    (ti_tab_pressed, 0, 0, [],[(finish_mission,0),(jump_to_menu, "mnu_auto_intro_mordor"),]),

    ### TOWN CENTER TRIGGERS
            
            
    (1, 0, ti_once, [],[(call_script, "script_init_town_walker_agents"),]),
    (3, 0, 0, [(call_script, "script_tick_town_walkers")], []),

 ] + ((is_a_wb_cutscene==1) and [
          (1, 0, 15, [], [ # messenger props
                (scene_prop_get_num_instances, ":num_messengers", "spr_troop_messenger"),
                (scene_prop_get_num_instances, ":num_messenger_exits", "spr_troop_messenger_exit"),
                (set_fixed_point_multiplier, 100),
                
                (try_for_range, ":count", 0, ":num_messengers"),
                    (scene_prop_get_instance, ":instance_no", "spr_troop_messenger", ":count"),
                    
                    (try_begin), #spawn messenger at a exit point, send to destination
                        (store_random_in_range, ":chance", 0, 10),
                        (ge, ":chance", 8),
                        (store_faction_of_party, ":faction", "$current_town"),
                        (faction_get_slot, ":troop", ":faction", slot_faction_rider_troop),
                        (prop_instance_get_scale, pos2, ":instance_no"),
                        (position_get_scale_y, ":tier", pos2),
                        (val_sub, ":tier", 100),
                        (val_div, ":tier", 10),
                        (store_random_in_range, ":tier_randomizer", 0, 2),
                        (val_sub, ":tier", ":tier_randomizer"),
                        (try_begin),
                            (ge, ":tier", 1),
                            (try_for_range, ":unused", 0, ":tier"),
                                (troop_get_upgrade_troop, ":upgrade_troop", ":troop", 0),
                                (gt, ":upgrade_troop", 0),
                                (assign, ":troop", ":upgrade_troop"),
                            (try_end),
                        (try_end),
                                
                        (store_random_in_range, ":rand_exit", 0, ":num_messenger_exits"),
                        (scene_prop_get_instance, ":instance_no_target", "spr_troop_messenger_exit", ":rand_exit"),
                        (prop_instance_get_position, pos1, ":instance_no_target"),
                        (set_spawn_position, pos1),  (spawn_agent, ":troop"),
                        (lt, "$g_encountered_party_2", 0), #don't spawn riders in siege battles
                        (agent_set_team, reg0, 0),
                        (agent_set_slot, reg0, slot_agent_walker_type, 3), #messenger  
                        (prop_instance_get_position, pos2, ":instance_no"),
                        (agent_set_slot, reg0, slot_agent_is_running_away, 0),
                        (agent_set_scripted_destination, reg0, pos2),
                    (try_end),
                    
                    #find a random messenger exit point, send them out
                    (prop_instance_get_position, pos1, ":instance_no"),
                    (try_for_agents, ":agent_no", pos1, 500),
                        (agent_slot_eq, ":agent_no", slot_agent_walker_type, 3),
                        (store_random_in_range, ":chance", 0, 10),
                        (ge, ":chance", 3),
                        (gt, ":num_messenger_exits", 0),
                        (store_random_in_range, ":rand_exit", 0, ":num_messenger_exits"),
                        (scene_prop_get_instance, ":instance_no_target", "spr_troop_messenger_exit", ":rand_exit"),
                        (prop_instance_get_position, pos2, ":instance_no_target"),
                        (agent_set_scripted_destination, ":agent_no", pos2),
                        (agent_set_slot, ":agent_no", slot_agent_is_running_away, 1), #needed for tracking
                    (try_end),

                (try_end),
              ]),

              (3, 0, 0, [], [ #slow down or speed up at city entrance
                (entry_point_get_position, pos1, 2), #player spawn on foot
                (set_fixed_point_multiplier, 100),
                (try_for_agents, ":agent_no", pos1, 1500),
                    (agent_slot_eq, ":agent_no", slot_agent_walker_type, 3),
                    (agent_slot_eq, ":agent_no", slot_agent_is_running_away, 1),
                    (agent_set_speed_limit, ":agent_no", 100),
                (else_try),
                    (agent_slot_eq, ":agent_no", slot_agent_walker_type, 3),
                    (store_random_in_range, ":speed_limit", 10, 17),
                    (agent_set_speed_limit, ":agent_no", ":speed_limit"),
                (try_end),
                  ]),

              (0.2, 0, 0, [], [ #messengers leaving the scene
                #(entry_point_get_position, pos1, 1),
                (set_fixed_point_multiplier, 100),
                (scene_prop_get_num_instances, ":num_messenger_exits", "spr_troop_messenger_exit"),
                (try_for_range, ":count", 0, ":num_messenger_exits"),
                    (scene_prop_get_instance, ":instance_no", "spr_troop_messenger_exit", ":count"),
                    (prop_instance_get_position, pos1, ":instance_no"),
                    (try_for_agents, ":agent_no", pos1, 600),
                        (agent_slot_eq, ":agent_no", slot_agent_walker_type, 3),
                        (agent_slot_eq, ":agent_no", slot_agent_is_running_away, 1),
                        (agent_start_running_away, ":agent_no"),
                        (this_or_next|eq, "$current_town", "p_town_moria"), #indoor scenes
                        (this_or_next|eq, "$current_town", "p_town_goblin_north_outpost"), 
                        (eq, "$current_town", "p_town_erebor"),
                        (agent_fade_out, ":agent_no"),
                    (try_end),
                (try_end),
                  ]),

              ### town patrols (separate triggers, maybe shift the load of the nested prop loops)
              (15, 0, 0, [], [ 
                (call_script, "script_town_guard_patrols", "spr_troop_guard"),
                  ]),

              (9, 0, 0, [], [ 
                (call_script, "script_town_guard_patrols", "spr_troop_archer"),
                  ]),
                  
              (20, 0, 0, [], [ 
                (call_script, "script_town_guard_patrols", "spr_troop_rider"),
                  ]), 

] or []) + [

    ### CUTSCENE TRIGGERS
    (ti_before_mission_start, 0, 0, [],
      [ 
        (assign, "$g_tld_intro_state", 10),
        
        (music_set_situation, 0), (music_set_culture, 0),
        (play_track, "track_mount_and_blade_title_screen", 2),
        (music_set_situation, mtf_sit_fight),
      ]),
      
      (0, 0, ti_once,
       [(start_presentation, "prsnt_intro_titles"),
       ],[]),

      # detect player camera init
      (0, 0, ti_once,
        [
         (mission_cam_get_position, pos1),
         (position_get_z, ":z_pos", pos1),
         (neq, ":z_pos", 0),       
        ],
        [
         (assign, "$g_tld_intro_state", 11),
        ]),
      
      (0, 0, 0,
       [
         (set_show_messages, 0),
         (store_mission_timer_a, ":cur_time"),
         (set_fixed_point_multiplier, 100),
         # make player agent static
         (get_player_agent_no, ":player_agent"),
         (agent_get_horse, ":horse_agent", ":player_agent"),					
         (try_begin),
           (eq, ":horse_agent", -1),
         #swy-- for M&B 1.011 we use anim_stand, and for WB anim_stand_cutscene
         ]+(is_a_wb_cutscene==0 and 
          [(agent_set_animation, ":player_agent", "anim_stand")]
            or
          [(agent_set_animation, ":player_agent", "anim_stand_cutscene")]
         )+[
         #swy-- here it finishes, just in case
         (else_try),
           (agent_set_animation, ":player_agent", "anim_ride_0"),
           (agent_set_animation, ":horse_agent", "anim_horse_stand"),
         (try_end),
 
### InVain: Use entry points 43-53 instead of absolute positions for greater flexibility
 
         (try_begin),
           (eq, "$g_tld_intro_state", 11), #start with looking at the gate 43
           (mission_cam_set_mode, 1),
           (entry_point_get_position, pos1, 43),
          # (position_move_z, pos1, 300),
          # (position_set_x, pos1, 17522),
          # (position_set_y, pos1, 30724),
           (mission_cam_set_position, pos1),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 12), #through the gate 44
           (ge, ":cur_time", 5),								 
           (entry_point_get_position, pos1, 44),
          # (init_position, pos1),
          # (position_rotate_z, pos1, -120),
          # (position_set_x, pos1, 17300),
          # (position_set_y, pos1, 21600),
          # (position_set_z, pos1,  1300),
           (mission_cam_animate_to_position, pos1, 4100, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 13), #just turn in place
           (ge, ":cur_time", 9),
		   (entry_point_get_position, pos1, 45),
           #(init_position, pos1),
           #(position_rotate_z, pos1, -95),
           #(position_set_x, pos1, 17300),
           #(position_set_y, pos1, 21600),
           #(position_set_z, pos1,  1300),
           (mission_cam_animate_to_position, pos1, 2100, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 14), #left through the streets
           (ge, ":cur_time", 11),
		   (entry_point_get_position, pos1, 46),
           #(init_position, pos1),
           #(position_rotate_z, pos1, -100),
           #(position_set_x, pos1, 20800),
           #(position_set_y, pos1, 22000),
           #(position_set_z, pos1,  1300),
           (mission_cam_animate_to_position, pos1, 4100, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 15), #up a bit, look up to the tower
           (ge, ":cur_time", 15),
		   (entry_point_get_position, pos1, 47),
           #(init_position, pos1),
           #(position_rotate_z, pos1, -120),
           #(position_rotate_x, pos1, 15),
           #(position_set_x, pos1, 25000),
           #(position_set_y, pos1, 20100),
           #(position_set_z, pos1,  3000),
           (mission_cam_animate_to_position, pos1, 3100, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 16), #second gate, look at the tower
           (ge, ":cur_time", 18),
		   (entry_point_get_position, pos1, 48),
          # (init_position, pos1),
          # (position_rotate_z, pos1, -180),
          # (position_rotate_x, pos1, -20),
          # (position_set_x, pos1, 28300),
          # (position_set_y, pos1, 12500),
          # (position_set_z, pos1,  5000),
           (mission_cam_animate_to_position, pos1, 2700, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 17), #top of the city
           (ge, ":cur_time", 22),
		   (entry_point_get_position, pos1, 49),
           #(init_position, pos1),
           #(position_rotate_z, pos1, 100),
           #(position_rotate_x, pos1, -30),
           #(position_set_x, pos1, 21600),
           #(position_set_y, pos1,  8300),
           #(position_set_z, pos1, 17300),
           (mission_cam_animate_to_position, pos1, 2700, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 18), #white tree
           (ge, ":cur_time", 25),
		   (entry_point_get_position, pos1, 50),
          # (init_position, pos1),
          # (position_rotate_z, pos1, -150),
          # (position_rotate_x, pos1, -40),
          # (position_set_x, pos1, 16900),
          # (position_set_y, pos1,  9000),
          # (position_set_z, pos1, 16800),
           (mission_cam_animate_to_position, pos1, 3700, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 19), #off the cliff
           (ge, ":cur_time", 32),
		   (entry_point_get_position, pos1, 51),
         #  (init_position, pos1),
         #  (position_rotate_z, pos1, -160),
         #  (position_rotate_x, pos1, -20),
         #  (position_set_x, pos1, 15900),
         #  (position_set_y, pos1, 23200),
         #  (position_set_z, pos1, 17800),
           (mission_cam_animate_to_position, pos1, 2700, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 20), #drop to the right
           (ge, ":cur_time", 35),
		   (entry_point_get_position, pos1, 52),
         #  (init_position, pos1),
         #  (position_rotate_z, pos1, -150),
         #  (position_set_x, pos1,  7800),
         #  (position_set_y, pos1, 20300),
         #  (position_set_z, pos1,  7100),
           (mission_cam_animate_to_position, pos1, 3000, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 21), #guard position
           (ge, ":cur_time", 38),
		   (entry_point_get_position, pos1, 53),
         #  (init_position, pos1),
         #  (position_set_x, pos1, 14900),
         #  (position_set_y, pos1, 23200),
         #  (position_set_z, pos1,  3900),
           (mission_cam_animate_to_position, pos1, 4000, 0),
           # ominious music
           (play_cue_track, "track_victorious_evil3"),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 22), #finish
           (ge, ":cur_time", 44),
           (finish_mission, 0),
           (val_add, "$g_tld_intro_state", 1),
           #chain to next intro mission
           (jump_to_menu, "mnu_auto_intro_mordor"),
         (try_end),
         ], []),
    ],
),

("intro_mordor", 0, -1,
    "Intro cutscene mission",
    [(0,mtef_visitor_source|mtef_team_0,0,0,1,[]),
     (1,mtef_visitor_source|mtef_team_0,0,0,1,[]),
    ],fade_cutscene+
    [
    (ti_tab_pressed, 0, 0, [],[(finish_mission,0)]+return_exit_macro),
    
    (ti_before_mission_start, 0, 0, [],
      [ 
        (assign, "$g_tld_intro_state", 30),
        
        (music_set_situation, 0), (music_set_culture, 0),
        (play_track, "track_TLD_Minas_Morgul", 2), #new MM track
        (music_set_situation, mtf_sit_town),
      ]),
      
      (0, 0, ti_once,
       [(start_presentation, "prsnt_intro_titles"),
        
        #spawn a standard bearer and ranks of soldiers #entry point 48
        (set_fixed_point_multiplier, 100),
       # (init_position, pos1),
       # (position_set_x, pos1, 22644),
       # (position_set_y, pos1, 20078),
       # (position_rotate_z, pos1, -11),
        (entry_point_get_position, pos1, 21),
        (set_spawn_position, pos1),
        (spawn_agent, "trp_c5_mordor_num_knight"), #has to be in a condition block, or it will crash
        (agent_set_speed_limit, reg0, 7),
        (position_move_x, pos1, -225), #1.5x column width
        (position_move_y, pos1, -700), # bearer ahead of troops
        (try_for_range, ":unused", 0, 30), #ranks
          (try_for_range, ":unused2", 0, 4), #columns
            (set_spawn_position, pos1),
            (spawn_agent, "trp_i5_mordor_black_uruk"),
            (agent_set_speed_limit, reg0, 7),
            (position_move_x, pos1, 150), #1.5m between columns
          (try_end),
          # get back to first column of previous rank
          (position_move_x, pos1, -600), #4x1.5m
          (position_move_y, pos1, -150), #next rank 1.5m behind
        (try_end),
       ],[]),

      # detect player camera init
      (0, 0, ti_once,
        [
         (mission_cam_get_position, pos1),
         (position_get_z, ":z_pos", pos1),
         (neq, ":z_pos", 0),       
        ],
        [
         (assign, "$g_tld_intro_state", 31),
        ]),
      
      (0, 0, 0,
       [
         (set_show_messages, 0),
         (store_mission_timer_a, ":cur_time"),
         (set_fixed_point_multiplier, 100),

         # (try_begin),
           # (eq, ":horse_agent", -1),
         # #swy-- for M&B 1.011 we use anim_stand, and for WB anim_stand_cutscene
         # ]+(is_a_wb_cutscene==0 and 
          # [(agent_set_animation, ":player_agent", "anim_stand")]
            # or
          # [(agent_set_animation, ":player_agent", "anim_stand_cutscene")]
         # )+[
         # #swy-- here it finishes, just in case
         # (else_try),
           # (agent_set_animation, ":player_agent", "anim_ride_0"),
           # (agent_set_animation, ":horse_agent", "anim_horse_stand"),
         # (try_end),


        #remove player agent
        ] + ((is_a_wb_cutscene==1) and [
         (get_player_agent_no, ":player_agent"),
         (agent_get_horse, ":horse_agent", ":player_agent"),
         (agent_fade_out, ":player_agent"),
         (agent_fade_out, ":horse_agent"), 
        ] or []) + [
         
         (try_begin),
           (eq, "$g_tld_intro_state", 31), #start with looking at the city 43
           (mission_cam_set_mode, 1),
           (entry_point_get_position, pos1, 16),
          # (init_position, pos1),
          # (position_rotate_z, pos1, 169),
          # (position_set_x, pos1, 23600),
          # (position_set_y, pos1, 36200),
          # (position_set_z, pos1, 2100),
           (mission_cam_set_position, pos1),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 32), #pan to the bridge 44
           (ge, ":cur_time", 4),
           (entry_point_get_position, pos1, 17),
          # (init_position, pos1),
          # (position_rotate_z, pos1, 169),
          # (position_set_x, pos1, 25000),
          # (position_set_y, pos1, 32200),
          # (position_set_z, pos1, 1400),
           (mission_cam_animate_to_position, pos1, 2000, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 33), #pan to the other side of the bridge 45
           (ge, ":cur_time", 6),
           (entry_point_get_position, pos1, 18),
         #  (init_position, pos1),
         #  (position_rotate_z, pos1, 169),
         #  (position_set_x, pos1, 23000),
         #  (position_set_y, pos1, 22000),
         #  (position_set_z, pos1, 500),
           (mission_cam_animate_to_position, pos1, 10000, 0),
           # march the troops down the bridge
           (try_for_agents, ":agent_no"), # find everyone and march them off 49
             (agent_get_troop_id, ":agent_troop", ":agent_no"),
             (this_or_next|eq, ":agent_troop", "trp_c5_mordor_num_knight"),
             (eq, ":agent_troop", "trp_i5_mordor_black_uruk"),
             (entry_point_get_position, pos1, 22),
             #(agent_get_position, pos1, ":agent_no"),
             #(position_move_x, pos1, 1350), # correction for angle numerical loss
             #(position_move_y, pos1, 10000),
             (agent_set_scripted_destination, ":agent_no", pos1, 1),
             (eq, ":agent_troop", "trp_c5_mordor_num_knight"),
             (agent_play_sound, ":agent_no", "snd_nazgul_skreech_long"), #somebody has to screech
           (try_end),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 34), #turn around 46
           (ge, ":cur_time", 16),
           (entry_point_get_position, pos1, 19),
          # (init_position, pos1),
         #  (position_rotate_z, pos1, -11),
          # (position_set_x, pos1, 23000),
          # (position_set_y, pos1, 22000),
          # (position_set_z, pos1, 400),
           (mission_cam_animate_to_position, pos1, 1000, 0),
           # find the leader and make him make yell a little
           (try_for_agents, ":agent_no"), 
             (agent_get_troop_id, ":agent_troop", ":agent_no"),
             (eq, ":agent_troop", "trp_i5_mordor_uruk_standard_bearer"),
             (agent_play_sound, ":agent_no", "snd_uruk_victory"),
           (try_end),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 35), #and fly over again 47
           (ge, ":cur_time", 22),
           (entry_point_get_position, pos1, 20),
         #  (init_position, pos1),
         #  (position_rotate_x, pos1, 50),
           #(position_rotate_z, pos1, 30),
         #  (position_set_x, pos1, 25000),
         #  (position_set_y, pos1, 32200),
         #  (position_set_z, pos1, 400),
           (mission_cam_animate_to_position, pos1, 7000, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 36), #finish
           (ge, ":cur_time", 30),
           (finish_mission, 0),
           (val_add, "$g_tld_intro_state", 1),
           # finish chain
           ]+return_exit_macro+[
         (try_end),
         ], []),
    ],
),

("intro_joke", 0, -1,
    "Intro cutscene mission",
    [(0,mtef_visitor_source|mtef_team_2,0,0,1,[]),
     (1,mtef_visitor_source|mtef_team_2,0,0,1,[]),
    ],
    [
    (ti_tab_pressed, 0, 0, [],[(finish_mission,0)]+return_exit_macro),
    
    (ti_before_mission_start, 0, 0, [],
      [ 
        (assign, "$g_tld_intro_state", 100),
        # all friends with player and Denethor
        (team_set_relation, 0, 2, 1),
        (team_set_relation, 1, 2, 1),
        # Guards initially friendly
        (team_set_relation, 0, 1, 1), 
        
        (music_set_situation, 0),
        (play_cue_track, "track_TLD_Minas_Tirith"), #new track
      ]),
      
      (0, 0, ti_once,
       [(start_presentation, "prsnt_intro_titles"),
        
        #spawn people
        (set_fixed_point_multiplier, 100),
        # adventurers
        (init_position, pos1),
        (position_set_x, pos1, -200),
        (position_set_y, pos1, -1600),
        (position_rotate_z, pos1, 180),
        (set_spawn_position, pos1),
        (spawn_agent, "trp_i1_gon_levy"), #first
        (agent_set_stand_animation, reg0, "anim_stand_man"),
        (agent_set_team, reg0, 1),
        (agent_set_hit_points, reg0, 0, 1),
        (position_move_x, pos1, 100),
        (set_spawn_position, pos1),
        (spawn_agent, "trp_i1_dwarf_apprentice"),
        (agent_set_team, reg0, 1),
        (agent_set_stand_animation, reg0, "anim_stand_man"),
        (agent_set_hit_points, reg0, 0, 1),
        (position_move_x, pos1, 100),
        (set_spawn_position, pos1),
        (spawn_agent, "trp_a1_lorien_scout"),
        (agent_set_team, reg0, 1),
        (agent_set_stand_animation, reg0, "anim_stand_man"),
        (agent_set_hit_points, reg0, 0, 1),
        # denethor
        (entry_point_get_position, pos1, 16),
        (set_spawn_position, pos1),
        (troop_get_inventory_slot, ":horse_item", "trp_gondor_lord", 8),
        (troop_set_inventory_slot, "trp_gondor_lord", 8, -1),
        (spawn_agent, "trp_gondor_lord"),
        (agent_set_stand_animation, reg0, "anim_sit_on_throne"),####
        (agent_set_team, reg0, 2),
        (troop_set_inventory_slot, "trp_gondor_lord", 8, ":horse_item"),
        # guards
        (entry_point_get_position, pos1, 6),
        (set_spawn_position, pos1),
        (spawn_agent, "trp_steward_guard"),
        (agent_set_stand_animation, reg0, "anim_stand_townguard"),
        (agent_set_team, reg0, 0),
        (entry_point_get_position, pos1, 7),
        (set_spawn_position, pos1),
        (spawn_agent, "trp_steward_guard"),
        (agent_set_stand_animation, reg0, "anim_stand_townguard"),
        (agent_set_team, reg0, 0),
        (entry_point_get_position, pos1, 17),
        (set_spawn_position, pos1),
        (spawn_agent, "trp_steward_guard"),
        (agent_set_stand_animation, reg0, "anim_stand_townguard"),
        (agent_set_team, reg0, 0),
        (entry_point_get_position, pos1, 25),
        (set_spawn_position, pos1),
        (spawn_agent, "trp_steward_guard"),
        (agent_set_stand_animation, reg0, "anim_stand_townguard"),
        (agent_set_team, reg0, 0),        
       ],[]),

      # detect player camera init
      (0, 0, ti_once,
        [
         (mission_cam_get_position, pos1),
         (position_get_z, ":z_pos", pos1),
         (neq, ":z_pos", 0),       
        ],
        [
         (assign, "$g_tld_intro_state", 101),
        ]),
	
      (0, 0, 0,
       [
         (set_show_messages, 0),
         (store_mission_timer_a, ":cur_time"),
         (store_mission_timer_b, ":cur_time_b"),
         (set_fixed_point_multiplier, 100),
         # make player agent static
         (get_player_agent_no, ":player_agent"),
         (agent_get_horse, ":horse_agent", ":player_agent"),					
         (try_begin),
           (eq, ":horse_agent", -1),
         #swy-- for M&B 1.011 we use anim_stand, and for WB anim_stand_cutscene
         ]+(is_a_wb_cutscene==0 and 
          [(agent_set_animation, ":player_agent", "anim_stand")]
            or
          [(agent_set_animation, ":player_agent", "anim_stand_cutscene")]
         )+[
         #swy-- here it finishes, just in case
         (else_try),
           (agent_set_animation, ":player_agent", "anim_ride_0"),
           (agent_set_animation, ":horse_agent", "anim_horse_stand"),
         (try_end),
         
         (try_begin),
           (eq, "$g_tld_intro_state", 101), #look at the throne
           #(ge, ":cur_time", 1),
           (mission_cam_set_mode, 1),
           (entry_point_get_position, pos1, 0),
           (position_rotate_x, pos1, -5),
           (position_set_z, pos1, 300),
           (mission_cam_set_position, pos1),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 102), #pan closer
           (ge, ":cur_time", 4),
           (entry_point_get_position, pos1, 22),
           (position_rotate_z, pos1, 55),
           (position_rotate_x, pos1, -5),
           (position_set_z, pos1, 250),
           (mission_cam_animate_to_position, pos1, 3000, 0),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 103), #look at denethor
           (ge, ":cur_time", 10),
           (entry_point_get_position, pos1, 16),
           (position_rotate_z, pos1, 180),
           (position_set_z, pos1, 230),
           (position_move_y, pos1, -200),
           (mission_cam_set_position, pos1),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 104), #look at adventurers
           (ge, ":cur_time", 12),
           (entry_point_get_position, pos1, 16),
           #(position_rotate_z, pos1, 180),
           (position_set_z, pos1, 230),
           (position_move_y, pos1, 100),
           (position_move_x, pos1, -80),
           (mission_cam_set_position, pos1),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 105), #adventurers jump and cheer!
           (ge, ":cur_time", 15),
           (try_for_agents, ":agent_no"),
             (agent_get_team, ":team", ":agent_no"),
             (eq, ":team", 1),
             (agent_set_animation, ":agent_no", "anim_jump"),
             (agent_play_sound, ":agent_no", "snd_man_victory"),
           (try_end),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 106), #another look at denethor and adventurers, and more jumping
           (ge, ":cur_time", 16),
           (entry_point_get_position, pos1, 16),
           (position_rotate_z, pos1, 90),
           (position_set_z, pos1, 250),
           (position_move_y, pos1, -300),
           (position_move_x, pos1, 200),
           (mission_cam_set_position, pos1),
           (try_for_agents, ":agent_no"),
             (agent_get_team, ":team", ":agent_no"),
             (eq, ":team", 1),
             (agent_set_animation, ":agent_no", "anim_jump"),
             (agent_play_sound, ":agent_no", "snd_man_victory"),
           (try_end),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 107), #guards attack! and pan out
           (ge, ":cur_time", 18),
           (team_set_relation, 0, 1, -1),
           (init_position, pos1),
           (position_rotate_z, pos1, 170),
           (position_rotate_x, pos1, -5),
           (position_set_y, pos1, 100),
           (position_set_z, pos1, 300),
           (mission_cam_animate_to_position, pos1, 3000, 0),
           #spawn more guards behind the camera
           (set_spawn_position, pos1),
           (spawn_agent, "trp_steward_guard"),
           (agent_set_team, reg0, 0),        
           (spawn_agent, "trp_steward_guard"),
           (agent_set_team, reg0, 0),        
           (spawn_agent, "trp_steward_guard"),
           (agent_set_team, reg0, 0),        
           (spawn_agent, "trp_steward_guard"),
           (agent_set_team, reg0, 0),        
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 108), #wait for the fight to finish
           (ge, ":cur_time", 23),
           (num_active_teams_le, 2),
           (reset_mission_timer_b),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 109), #denethor final comment
           (ge, ":cur_time_b", 3),
           # make denethor sit again
           (try_for_agents, ":agent_no"),
             (agent_get_troop_id, ":troop", ":agent_no"),
             (eq, ":troop", "trp_gondor_lord"),
             (agent_set_animation, ":agent_no", "anim_sit_on_throne"),####
           (try_end),
           (entry_point_get_position, pos1, 16),
           (position_rotate_z, pos1, 180),
           (position_set_z, pos1, 230),
           (position_move_y, pos1, -200),
           (mission_cam_set_position, pos1),
           (val_add, "$g_tld_intro_state", 1),
         (else_try),
           (eq, "$g_tld_intro_state", 110), #finish
           (ge, ":cur_time_b", 7),
           (finish_mission, 0),
           (music_set_situation, 0),
           (val_add, "$g_tld_intro_state", 1),
           # finish chain
           ]+return_exit_macro+[
         (try_end),
         ], []),
    ],
),

("test_gandalf", 0, -1,
    "Gandalf cutscene mission",
    [( 0,mtef_visitor_source|mtef_team_0,0,0,1,[]),
     (17,mtef_visitor_source|mtef_team_0,0,0,1,[]),
    ],fade_cutscene+
    [
    (ti_tab_pressed, 0, 0, [],[(finish_mission,0)]+return_exit_macro),
    
    (ti_before_mission_start, 0, 0, [],
      [ 
        (assign, "$g_tld_conversation_state", 0),
        (assign, "$g_tld_conversation_space_pressed", 1),
        
        (music_set_situation, 0), (music_set_culture, 0),
        # (play_track, "track_ambushed_by_khergit", 2), #orc ambush track
        # (music_set_situation, mtf_sit_siege),
      ]),
      
      (0, 0, ti_once,
       [(start_presentation, "prsnt_conversation_titles"),
        
        #spawn Gandalf behind the little hill
        (try_for_agents,":cur_agent"),
          (agent_get_troop_id, ":cur_agent_trp", ":cur_agent"),
          (eq,":cur_agent_trp", "$g_tld_convo_talker"),
          
          (set_fixed_point_multiplier, 100),
          
          #swy-- move here to the original spawn point position...
          (init_position, pos1),
          (position_set_x, pos1, 7800),
          (position_set_y, pos1, 8000),
          (agent_set_position,":cur_agent", pos1),
          
          #immediately have him ride over the hill to meet the player
          (position_set_x, pos1,  7550),
          (position_set_y, pos1, 11700),
          (agent_set_scripted_destination, ":cur_agent", pos1, 1),
        (try_end)
       ],[]),

      # detect player camera init
      (0, 0, ti_once,
        [
         (mission_cam_get_position, pos1),
         (position_get_z, ":z_pos", pos1),
         (neq, ":z_pos", 0),       
        ],
        [
         (assign, "$g_tld_conversation_state", 1),
        ]),
        
      # detect Space pressed
      (0, 0, 0,
        [
         (eq, "$g_tld_conversation_space_pressed", 0),
         (key_clicked, key_space),
         # (key_is_down, key_space),
        ],
        [
         (assign, "$g_tld_conversation_space_pressed", 1),
        ]),
        
      (0, 0, 0, guard_against_esc+
       [
         (set_show_messages, 0),
         (store_mission_timer_a, ":cur_time"),
         (set_fixed_point_multiplier, 100),
         # make player agent static
         (get_player_agent_no, ":player_agent"),
         (agent_get_horse, ":horse_agent", ":player_agent"),					
         (try_begin),
           (eq, ":horse_agent", -1),
         #swy-- for M&B 1.011 we use anim_stand, and for WB anim_stand_cutscene
         ]+(is_a_wb_cutscene==0 and 
          [(agent_set_animation, ":player_agent", "anim_stand")]
            or
          [(agent_set_animation, ":player_agent", "anim_stand_cutscene")]
         )+[
         #swy-- here it finishes, just in case
         (else_try),
           (agent_set_animation, ":player_agent", "anim_ride_0"),
           (agent_set_animation, ":horse_agent", "anim_horse_stand"),
         (try_end),
         
         (try_begin),
           (eq, "$g_tld_conversation_state", 1), #start with looking at Gandalf while he rides to meet the player
           (mission_cam_set_mode, 1),
           (init_position, pos1),
           (position_rotate_z, pos1, 180),
           (position_rotate_x, pos1, -20),
           (position_set_x, pos1, 7500),
           (position_set_y, pos1, 12300),
           (position_set_z, pos1, 1500),
           (mission_cam_set_position, pos1),
           (agent_get_position, pos1, ":player_agent"),
           (position_move_x, pos1, -50),
           (position_move_y, pos1, -200),
           (position_move_z, pos1, 180),
           (try_begin),
             (neq, ":horse_agent", -1),
             (position_move_z, pos1, 140),
           (try_end),
           # (mission_cam_set_position, pos1),
           # (init_position, pos1),
           # (position_rotate_z, pos1, 180),
           # (position_set_x, pos1, 7500),
           # (position_set_y, pos1, 12300),
           # (position_set_z, pos1, 600),
           (mission_cam_animate_to_position, pos1, 5000, 0), #camera goes down and ends up behind player facing Gandalf
           (str_store_string, s1, "str_empty_string"),
           (val_add, "$g_tld_conversation_state", 1),
         (else_try),
           (eq, "$g_tld_conversation_state", 2), #waiting for Gandalf to come
           (ge, ":cur_time", 6),
           (overlay_set_color, "$g_presentation_obj_1", 0x80FF80),
           (str_store_string, s1, "@Look at my over-the-shoulder shot, {playername}! I'm so beautiful from a distance!"),
           (val_add, "$g_tld_conversation_state", 1),
           (assign, "$g_tld_conversation_space_pressed", 0),
         (else_try),
           (eq, "$g_tld_conversation_state", 3), #camera behind Gandalf facing player
           (eq, "$g_tld_conversation_space_pressed", 1),
#           (ge, ":cur_time", 16),
           (init_position, pos1),
           (position_rotate_z, pos1, 0),
           (position_set_x, pos1, 7500),
           (position_set_y, pos1, 11500),
           (position_set_z, pos1, 560),
           (mission_cam_set_position, pos1),
           (overlay_set_color, "$g_presentation_obj_1", 0xFFFFFF),
           (str_store_string, s1, "@You wish, old man, my over-the-shoulder view is much prettier!"),
           (val_add, "$g_tld_conversation_state", 1),
           (assign, "$g_tld_conversation_space_pressed", 0),
         (else_try),
           (eq, "$g_tld_conversation_state", 4), #camera behind player facing Gandalf
           (eq, "$g_tld_conversation_space_pressed", 1),
#           (ge, ":cur_time", 18),
           # (init_position, pos1),
           # (position_rotate_z, pos1, 180),
           # (position_set_x, pos1, 7500),
           # (position_set_y, pos1, 12300),
           # (position_set_z, pos1, 600),
           (agent_get_position, pos1, ":player_agent"),
           (position_move_x, pos1, -50),
           (position_move_y, pos1, -200),
           (position_move_z, pos1, 180),
           (try_begin),
             (neq, ":horse_agent", -1),
             (position_move_z, pos1, 140),
           (try_end),
           (mission_cam_set_position, pos1),
           (overlay_set_color, "$g_presentation_obj_1", 0x80FF80),
           (str_store_string, s1, "@You should really see Steward Denetor's Facebook photos, he's amazing!"),
           (val_add, "$g_tld_conversation_state", 1),
           (assign, "$g_tld_conversation_space_pressed", 0),
         (else_try),
           (eq, "$g_tld_conversation_state", 5), #
           (eq, "$g_tld_conversation_space_pressed", 1),
#           (ge, ":cur_time", 25),
           (try_for_agents, ":agent_no"), # find Gandalf and send him on his way
             (agent_get_troop_id, ":agent_troop", ":agent_no"),
             (eq, ":agent_troop", "trp_gandalf"),
             (init_position, pos1),
             (position_set_x, pos1, 7800),
             (position_set_y, pos1, 7500),
             (position_rotate_z, pos1, 0),
             (set_spawn_position, pos1),
             (agent_set_scripted_destination, ":agent_no", pos1, 1),
           (try_end),
           (str_store_string, s1, "str_empty_string"),
           (val_add, "$g_tld_conversation_state", 1),
           (reset_mission_timer_a),
         (else_try),
           (eq, "$g_tld_conversation_state", 6), #wait a sec for Gandalf to turn around and ride off, then camera up
           (ge, ":cur_time", 1),
           (init_position, pos1),
           (position_rotate_z, pos1, 180),
           (position_rotate_x, pos1, -20),
           (position_set_x, pos1, 7500),
           (position_set_y, pos1, 12300),
           (position_set_z, pos1, 1500),
           (mission_cam_animate_to_position, pos1, 5000, 0), #camera goes up again
           (val_add, "$g_tld_conversation_state", 1),
         (else_try),
           (eq, "$g_tld_conversation_state", 7), #end mission
           (ge, ":cur_time", 7),
           (val_add, "$g_tld_conversation_state", 1),
           (finish_mission, 0),
           # finish chain
           ]+return_exit_macro+[
         (try_end),
         
         #presentation
         (overlay_set_text, "$g_presentation_obj_1", s1),
         (str_store_string, s2, "str_empty_string"),
         (try_begin),
           (eq, "$g_tld_conversation_space_pressed", 0),
           (str_store_string, s2, "@Press Space to continue..."),
         (try_end),
         (overlay_set_text, "$g_presentation_obj_2", s2),
       ], []),
    ],
),
    
("conversation_cutscene", 0, -1,
    "Gandalf/Nazgul conversation cutscene mission",
    [( 0,mtef_visitor_source|mtef_team_0,0,0,1,[]),
     (17,mtef_visitor_source|mtef_team_0,0,0,1,[]),
    ],fade_cutscene+
    [
    (ti_tab_pressed, 0, 0, [],[(finish_mission,0)]+return_exit_macro),
    
    (ti_before_mission_start, 0, 0, [],
      [ 
        (assign, "$g_tld_conversation_state", 0),
        (assign, "$g_tld_conversation_space_pressed", 1),
        
        (music_set_situation, 0), (music_set_culture, 0),
        # (play_track, "track_ambushed_by_khergit", 2), #orc ambush track
        # (music_set_situation, mtf_sit_siege),
		(try_begin), #GA: menacing ambiance for nazgul :)
			(eq, "$g_tld_convo_talker", "trp_nazgul"),
			(set_rain,1,100),
		(try_end),
      ]),
	################## THUNDER AND LIGHTNING BEGIN ###############################
	(3, 0.2, 6, [(eq, "$g_tld_convo_talker", "trp_nazgul"),(store_random_in_range,":rnd",1,5),(eq,":rnd",1),(set_fog_distance, 300, 0xaaaaaa),],
				[(set_fog_distance, 400, 0x010101),(play_sound,"snd_thunder"),(assign, "$lightning_cycle",1),]),
	(0.4,0.1, 6,[(eq, "$g_tld_convo_talker", "trp_nazgul"),(eq,"$lightning_cycle",1),(set_fog_distance, 300, 0x777777),],		###### Lightning afterflashes 
				[(set_fog_distance, 400, 0x010101),(assign,"$lightning_cycle",2),]),
	(0.5,0.1, 6,[(eq, "$g_tld_convo_talker", "trp_nazgul"),(eq,"$lightning_cycle",2),(set_fog_distance, 300, 0x555555),],
				[(set_fog_distance, 400, 0x010101),(assign,"$lightning_cycle",0),]),
	################## THUNDER AND LIGHTNING END #################################
  
  
      (0, 0, ti_once,
       [
        (try_begin), #GA: menacing ambiance for nazgul :)
          (eq, "$g_tld_convo_talker", "trp_nazgul"),
          (set_fog_distance,400,0x010101),
        (try_end),
        
        (start_presentation, "prsnt_conversation_titles"),
        
        ] + ((is_a_wb_cutscene==1) and [
        (set_camera_in_first_person, 0), 
        ] or []) + [
        
        #spawn Gandalf/Nazgul behind the little hill
        (try_for_agents,":cur_agent"),
          (agent_get_troop_id, ":cur_agent_trp", ":cur_agent"),
          (eq,":cur_agent_trp", "$g_tld_convo_talker"),
          
          (set_fixed_point_multiplier, 100),
          
          #swy-- move here to the original spawn point position...
          (init_position, pos1),
          (position_set_x, pos1, 7800),
          (position_set_y, pos1, 8000),
          (agent_set_position,":cur_agent", pos1),
          
          #immediately have him ride over the hill to meet the player
          (position_set_x, pos1,  7550),
          (position_set_y, pos1, 11700),
          (agent_set_scripted_destination, ":cur_agent", pos1, 1),
          
        ] + ((is_a_wb_cutscene==1) and [
           (agent_set_wielded_item, ":cur_agent", "itm_beorn_staff"), #equip staff 
        ] or []) + [

        (try_end)
        
       ],[]),

      # detect player camera init
      (0, 0, ti_once,
        [
         (mission_cam_get_position, pos1),
         (position_get_z, ":z_pos", pos1),
         (neq, ":z_pos", 0),       
        ],
        [
         (assign, "$g_tld_conversation_state", 1),
        ]),
        
      # detect Space pressed
      (0, 0, 0,
        [
         (eq, "$g_tld_conversation_space_pressed", 0),
         (key_clicked, key_space),
         # (key_is_down, key_space),
        ],
        [
         (assign, "$g_tld_conversation_space_pressed", 1),
        ]),
        
      # ambience sounds
      (1, 0, ti_once, [], [			
         (try_begin),
           (this_or_next|eq, "$g_tld_convo_talker", "trp_gandalf"),
           (eq, "$g_tld_convo_talker", "trp_radagast"),
           (play_sound, "snd_wind_ambiance", sf_looping),
         (else_try),
           (play_sound, "snd_morgul_ambiance", sf_looping),
         (try_end),
        ]),
        
      # agent noise
      (1, 1, ti_once, [(eq, "$g_tld_conversation_state", 102),], [	#as the talker rides off		
         # find Gandalf/Nazgul and make him screech
         (try_for_agents, ":agent_no"), 
           (agent_get_troop_id, ":agent_troop", ":agent_no"),
           (eq, ":agent_troop", "$g_tld_convo_talker"),
           (try_begin),
             (eq, "$g_tld_convo_talker", "trp_nazgul"),
             (agent_play_sound, ":agent_no", "snd_nazgul_skreech_short"),
           # (else_try),
             # (agent_play_sound, ":agent_no", "snd_nazgul_skreech_short"), #no Gandalf noise yet
           (try_end),
         (try_end),
        ]),
      
      #Positions used: pos50-52 talker views, pos53-55 player views (only pos53 done), pos60 bird's eye talker view
      (0, 0, 0, guard_against_esc+
       [
         (set_show_messages, 0),
         (store_mission_timer_a, ":cur_time"),
         (set_fixed_point_multiplier, 100),
         # make player agent static
         (get_player_agent_no, ":player_agent"),
         (agent_get_horse, ":horse_agent", ":player_agent"),					
         (try_begin),
           (eq, ":horse_agent", -1),
         #swy-- for M&B 1.011 we use anim_stand, and for WB anim_stand_cutscene
         ]+(is_a_wb_cutscene==0 and 
          [(agent_set_animation, ":player_agent", "anim_stand")]
            or
          [(agent_set_animation, ":player_agent", "anim_stand_cutscene")]
         )+[
         #swy-- here it finishes, just in case
         (else_try),
           (agent_set_animation, ":player_agent", "anim_ride_0"),
           (agent_set_animation, ":horse_agent", "anim_horse_stand"),
         (try_end),
         
         (try_begin),
           (eq, "$g_tld_conversation_state", 1), #start with looking at Gandalf/Nazgul while he rides to meet the player
           (mission_cam_set_mode, 1),
           (init_position, pos1),
           (position_rotate_z, pos1, 180),
           (position_rotate_x, pos1, -20),
           (position_set_x, pos1, 7500),
           (position_set_y, pos1, 12300),
           (position_set_z, pos1, 1500),
           (copy_position, pos60, pos1), #pos60 - bird's eye talker view
           (mission_cam_set_position, pos1),
           (agent_get_position, pos1, ":player_agent"),
           (position_move_x, pos1, -50),
           (position_move_y, pos1, -200),
           (position_move_z, pos1, 180),
           (try_begin),
             (neq, ":horse_agent", -1),
             (position_move_z, pos1, 120),
             #(position_rotate_x, pos1, 5),
           (try_end),
           (copy_position, pos50, pos1), #pos50 - over-the-shoulder talker view
           (mission_cam_animate_to_position, pos1, 5000, 0), #camera goes down and ends up behind player facing the talker
           #initialize more positions we use later
           (copy_position, pos51, pos50),
           (position_move_y, pos51, 250), #pos51 - wide shot talker view
           (position_rotate_z, pos51, 7),           
           (try_begin),
             (neq, ":horse_agent", -1),
             (position_move_z, pos51, -50),
           (try_end),
           (init_position, pos53),
           (position_rotate_x, pos53, -5),
           (try_begin),
             (eq, ":horse_agent", -1),
             (position_rotate_x, pos53, -10),
           (try_end),
           (position_set_x, pos53, 7500),
           (position_set_y, pos53, 11450),
           (position_set_z, pos53, 600), #pos53 - over-the-shoulder player view
           #end positions init
           (str_store_string, s1, "str_empty_string"),
           (val_add, "$g_tld_conversation_state", 1),
         (else_try),
           (eq, "$g_tld_conversation_state", 2), #waiting for the talker to come
           (ge, ":cur_time", 7),
           
           # find Gandalf/Nazgul and calculate pos52 for later use
           (try_for_agents, ":agent_no"), 
             (agent_get_troop_id, ":agent_troop", ":agent_no"),
             (eq, ":agent_troop", "$g_tld_convo_talker"),
             (agent_get_position, pos52, ":agent_no"),
             (position_move_z, pos52, 260),
             (position_move_y, pos52, 200),
             (position_rotate_z, pos52, 180), #pos52 - medium close up talker view
           (try_end),

           #Set text color
           (try_begin),
             (this_or_next|eq, "$g_tld_convo_talker", "trp_gandalf"),
             (eq, "$g_tld_convo_talker", "trp_radagast"),
             (overlay_set_color, "$g_presentation_obj_1", 0x80FF80), #Gandalf: green
           (else_try),
             (overlay_set_color, "$g_presentation_obj_1", 0xFF8080), #Nazgul: red
           (try_end),
           (str_store_string_reg, s1, s50), #first dialog line
           (val_sub, "$g_tld_convo_lines", 1),
           (val_add, "$g_tld_conversation_state", 1),
           (assign, "$g_tld_conversation_space_pressed", 0),
         (else_try),
           (is_between, "$g_tld_conversation_state", 3, 100), 
           (eq, "$g_tld_conversation_space_pressed", 1),
           
           (store_mod, ":player_speaks", "$g_tld_conversation_state", 2),
           (try_begin),
             (eq, ":player_speaks", 0),
             #Talker speaks: camera behind player facing the talker
             #(copy_position, pos1, pos50), #OTS talker
             (store_random_in_range, ":pos", pos50, pos53),
             (copy_position, pos1, ":pos"),
             (mission_cam_set_position, pos1),
             #Set text color
             (try_begin),
               (this_or_next|eq, "$g_tld_convo_talker", "trp_gandalf"),
               (eq, "$g_tld_convo_talker", "trp_radagast"),
               (overlay_set_color, "$g_presentation_obj_1", 0x80FF80), #Gandalf: green
             (else_try),
               (overlay_set_color, "$g_presentation_obj_1", 0xFF8080), #Nazgul: red
             (try_end),
           (else_try),
             #Player speaks: camera behind the talker facing player
             (copy_position, pos1, pos53), #OTS player
             (mission_cam_set_position, pos1),
             (overlay_set_color, "$g_presentation_obj_1", 0xFFFFFF), #Player: white
           (try_end),
           
           #find the next dialog line
           (store_sub, ":next_line_reg", "$g_tld_conversation_state", 2),
           (val_add, ":next_line_reg", s50), #MV=1337 h4x0r
           (str_store_string_reg, s1, ":next_line_reg"),
           
           (val_sub, "$g_tld_convo_lines", 1),
           (val_add, "$g_tld_conversation_state", 1),
           (try_begin),
             (eq, "$g_tld_convo_lines", 0), #no lines left, end the conversation
             (assign, "$g_tld_conversation_state", 100),
           (try_end),
           (assign, "$g_tld_conversation_space_pressed", 0),
         (else_try),
           (eq, "$g_tld_conversation_state", 100), #
           (eq, "$g_tld_conversation_space_pressed", 1),
           #Place the camera behind the player in case he was the last to speak
           (copy_position, pos1, pos50), #OTS talker
           (mission_cam_set_position, pos1),
           # find Gandalf/Nazgul and send him on his way
           (try_for_agents, ":agent_no"), 
             (agent_get_troop_id, ":agent_troop", ":agent_no"),
             (eq, ":agent_troop", "$g_tld_convo_talker"),
             (init_position, pos1),
             (position_set_x, pos1, 7800),
             (position_set_y, pos1, 7500),
             (agent_set_scripted_destination, ":agent_no", pos1, 1),
           (try_end),
           (str_store_string, s1, "str_empty_string"),
           (val_add, "$g_tld_conversation_state", 1),
           (reset_mission_timer_a),
         (else_try),
           (eq, "$g_tld_conversation_state", 101), #wait a sec for the talker to turn around and ride off, then camera up
           (ge, ":cur_time", 1),
           (mission_cam_animate_to_position, pos60, 5000, 0), #camera goes up again - same pos where it started in the scene
           (val_add, "$g_tld_conversation_state", 1),
         (else_try),
           (eq, "$g_tld_conversation_state", 102), #end mission
           (ge, ":cur_time", 6),
           (val_add, "$g_tld_conversation_state", 1),
           (finish_mission, 0),
           # finish chain
           ]+return_exit_macro+[
         (try_end),
         
         #presentation
         (overlay_set_text, "$g_presentation_obj_1", s1),
         (str_store_string, s2, "str_empty_string"),
         (try_begin),
           (eq, "$g_tld_conversation_space_pressed", 0),
           (str_store_string, s2, "@Press Space to continue..."),
         (try_end),
         (overlay_set_text, "$g_presentation_obj_2", s2),
       ], []),

    ],
),
    

]