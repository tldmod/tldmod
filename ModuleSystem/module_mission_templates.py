from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from module_constants import *
from module_mission_templates_TLD import *
from module_mission_templates_unneeded import *
from module_mission_templates_cutscenes import *
from module_mission_templates_morale import *

from module_info import wb_compile_switch as is_a_wb_mt

####################################################################################################################
#   Each mission-template is a tuple that contains the following fields:
#  1) Mission-template id (string): used for referencing mission-templates in other files.
#     The prefix mt_ is automatically added before each mission-template id
#
#  2) Mission-template flags (int): See header_mission-templates.py for a list of available flags
#  3) Mission-type(int): Which mission types this mission template matches.
#     For mission-types to be used with the default party-meeting system,
#     this should be 'charge' or 'charge_with_ally' otherwise must be -1.
#     
#  4) Mission description text (string).
#  5) List of spawn records (list): Each spawn record is a tuple that contains the following fields:
#    5.1) entry-no: Troops spawned from this spawn record will use this entry
#    5.2) spawn flags. 
#    5.3) alter flags. which equipment will be overriden
#    5.4) ai flags.
#    5.5) Number of troops to spawn.
#    5.6) list of equipment to add to troops spawned from here (maximum 8).
#  6) List of triggers (list).
#     See module_triggers.py for infomation about triggers.
#
####################################################################################################################

pilgrim_disguise  = [itm_blackroot_hood, itm_black_tunic, itm_practice_staff]

af_castle_lord    = af_override_horse | af_override_weapons | af_require_civilian
af_castle_warlord = af_override_horse | af_override_weapons | af_override_head | af_override_gloves
af_prisoner       = af_override_horse | af_override_weapons | af_override_head | af_override_gloves | af_override_gloves | af_override_foot

## Reset Fog 
reset_fog = (ti_before_mission_start,  0, ti_once, [], 
            [(set_fog_distance,0,0x999999)])

## Fade to Black
fade =  ((is_a_wb_mt==1) and [

        (ti_after_mission_start, 0, 0, [],
          [(mission_cam_set_screen_color,        0xFF000000), 
           (mission_cam_animate_to_screen_color, 0x00000000, 2500)])
        
        ] or [])

## Brighter Nights

bright_nights= ((is_a_wb_mt==1) and [ 
  
  (ti_before_mission_start, 0, 2,
    [ (eq, "$bright_nights", 1),
      (is_currently_night)],[
      (set_startup_ambient_light,15,24,37), #27,46,67 
      #(display_message, "@Bright Nights active")
    ])
  
  ] or [])


####################################################################################################################
## CUSTOM CAMERA by dunde, modified to add fixed-camera + implemented by Kham (WB Only)
####################################################################################################################


khams_custom_player_camera = ((is_a_wb_mt==1) and [

  #-- numeric constants

 # cam_mode_default = 0
 # cam_mode_free    = 1
 # cam_mode_fixed   = 2

  #-- camera_init
  (0, 0, ti_once,
  [
    (get_player_agent_no, "$cam_current_agent"),
    (gt,                  "$cam_current_agent", -1)
  ],
  [
    (assign, "$cam_mode",   "$pref_cam_mode"),
    (assign, "$shoot_mode", 0),
    (assign, "$cam_free",   0),
  ]),

 # Piggyback on Camera Code for Displaying Agent Labels.

  (ti_battle_window_opened, 0, 0, [(ge, "$g_display_agent_labels", 1),],
    [(start_presentation, "prsnt_display_agent_labels")]),

  (0,0,0, [(ge, "$g_display_agent_labels", 1), (key_clicked, key_y),],
    [(try_begin),
      (eq, "$show_hide_labels",1),
      (assign, "$show_hide_labels", 0),
     (else_try),
      (assign, "$show_hide_labels",1),
      (start_presentation, "prsnt_display_agent_labels"),
     (try_end)]),

  #-- camera_mode
  (0, 0, 0, [],
  [
    (try_begin),
      (eq, "$cam_mode", 1),
      (set_fixed_point_multiplier, 100),
      (agent_get_look_position, pos7, "$cam_current_agent"),
      (position_get_rotation_around_x, ":angle", pos7),
      (store_sub, ":reverse", 0, ":angle"),
      (position_rotate_x, pos7, ":reverse"),
      (position_move_y, pos7, "$g_camera_y"),
      (position_move_z, pos7, "$g_camera_z"),
      (agent_get_horse, ":horse_agent", "$cam_current_agent"),
      (try_begin),
        (ge, ":horse_agent", 0),
        (position_move_z, pos7, 80),
      (try_end),
      (store_mul, ":reverse", -1, "$g_camera_y"),
      (store_atan2, ":drop", "$g_camera_z", ":reverse"),
      (convert_from_fixed_point, ":drop"),
      (val_sub, ":angle", ":drop"),
      (position_rotate_x, pos7, ":angle"),
      (mission_cam_animate_to_position, pos7, 100, 0),

    (else_try),
      (eq, "$cam_mode", 2),
      (try_begin),
        (eq,"$cam_shoulder",0),
        (set_fixed_point_multiplier, 100),
        (agent_get_look_position, pos7, "$cam_current_agent"),
        (position_move_z, pos7,  180),
        (position_move_y, pos7, -190),
        (position_move_x, pos7,   70),
        (agent_get_horse, ":horse_agent", "$cam_current_agent"),
        (try_begin),
          (ge, ":horse_agent", 0),
          (position_move_z, pos7, 80),
        (try_end),
        (mission_cam_animate_to_position, pos7, 100),
      (else_try),
        (eq,"$cam_shoulder",1),
        (set_fixed_point_multiplier, 100),
        (agent_get_look_position, pos7, "$cam_current_agent"),
        (position_move_z, pos7,  180),
        (position_move_y, pos7, -190),
        (position_move_x, pos7,  -70),
        (agent_get_horse, ":horse_agent", "$cam_current_agent"),
        (try_begin),
          (ge, ":horse_agent", 0),
          (position_move_z, pos7, 80),
        (try_end),
        (mission_cam_animate_to_position, pos7, 100),
      (try_end),
    (else_try),
      (lt, "$cam_mode", 3),
      (main_hero_fallen),
      (agent_get_position, 1, "$cam_current_agent"),
      (get_player_agent_no,   ":player_agent"),
      (agent_set_position,    ":player_agent", 1),
    (try_end),
  ]),

  #-- camera_raise
  (0, 0, 0,
  [
    (this_or_next|key_is_down, key_right_control),
    (             key_is_down, key_left_control),
    (key_is_down, "$key_camera_height_plus"),
    (eq,          "$cam_mode",  1)
  ],
  [
    (val_add, "$g_camera_z",    1),
    (this_or_next|neg|key_is_down, key_right_shift),
    (             neg|key_is_down, key_left_shift),
    (val_add, "$g_camera_z",    9)
  ]),

  #-- camera_lower
  (0, 0, 0,
  [
    (this_or_next|key_is_down, key_right_control),
    (             key_is_down, key_left_control),
    (key_is_down, "$key_camera_height_min"),
    (eq,          "$cam_mode",  1)
  ],
  [
    (val_sub, "$g_camera_z",    1),
    (this_or_next|neg|key_is_down, key_right_shift),
    (             neg|key_is_down, key_left_shift),
    (val_sub, "$g_camera_z",    9),
    (val_max, "$g_camera_z",   50)
  ]),

  #--camera_zoom_out
  (0, 0, 0,
  [
    (this_or_next|key_is_down, key_right_control),
    (             key_is_down, key_left_control),
    (key_is_down, "$key_camera_zoom_min"),
    (eq,          "$cam_mode",  1)
  ],
  [
    (val_sub, "$g_camera_y",    1),
    (this_or_next|neg|key_is_down, key_right_shift),
    (             neg|key_is_down, key_left_shift),
    (val_sub, "$g_camera_y",    9),
  ]),

  #-- camera_zoom_in
  (0, 0, 0,
  [
    (this_or_next|key_is_down, key_right_control),
    (             key_is_down, key_left_control),
    (             key_is_down, "$key_camera_zoom_plus"),
    (eq, "$cam_mode",           1)
  ],
  [
    (val_add, "$g_camera_y",    1),
    (this_or_next|neg|key_is_down, key_right_shift),
    (             neg|key_is_down, key_left_shift),
    (val_add, "$g_camera_y",    9),
    (val_min, "$g_camera_y",  -50),
  ]),


  #-- camera_set
  (0, 0, 0,
  [
    (this_or_next|key_is_down, key_right_control),
    (             key_is_down, key_left_control),
    (key_clicked, "$key_camera_toggle"),
    (lt, "$cam_mode", 3),
    (neq, "$shoot_mode", 1)
  ],
  # toggling only when camera mode = 0, 1, 2 (3 = disable); shoot_mode = 1 temporarily disable toggling
  [
    (try_begin),
      (eq,     "$cam_mode", 0),
      (assign, "$cam_mode", 2),
      (display_message, "@Fixed Custom Camera"),
      (display_message, "@Press Ctrl + Left / Ctrl + Right Arrow Keys to Switch Shoulders"),

    (else_try),
      (eq,     "$cam_mode", 2),
      (assign, "$cam_mode", 1),
      (display_message, "@Free-Mode Custom Camera"),
      (display_message, "@Use +/- to zoom in/out"),
      (display_message, "@Use Up/Down arrow keys to tilt up/down"),

    (else_try),
      (eq, "$cam_mode", 1),
      # (try_begin),
      #   (neg|main_hero_fallen, 0),
      #   (get_player_agent_no, "$cam_current_agent"),
      # (try_end),
      (assign, "$cam_mode", 0),
      (display_message, "@Default Camera"),
    (try_end),

    (mission_cam_set_mode, "$cam_mode"),
  ]),

  #-- camera_cycle_forwards
  (0, 0, 0,
  [
    (this_or_next|key_is_down, key_right_control),
    (             key_is_down, key_left_control),
    (key_clicked, "$key_camera_next"),
    (try_begin),
      (eq, "$cam_mode",         3),
      (call_script, "script_dmod_cycle_forwards"),
    (else_try),
      (eq,     "$cam_mode",     2),
      (assign, "$cam_shoulder", 0),
      (display_message, "@Fixed Camera - Right Shoulder"),
    (try_end)
  ], []),

  #-- camera_cycle_backwards
  (0, 0, 0,
  [
    (this_or_next|key_is_down, key_right_control),
    (             key_is_down, key_left_control),
    (key_clicked, "$key_camera_prev"),
    (try_begin),
      (eq, "$cam_mode",         3),
      (call_script, "script_dmod_cycle_backwards"),
    (else_try),
      (eq,     "$cam_mode",     2),
      (assign, "$cam_shoulder", 1),
      (display_message, "@Fixed Camera - Left Shoulder"),
    (try_end)
  ], []),

  #-- camera_shot
  (0, 0, 0,
  [
    (key_is_down, key_left_mouse_button),
    (eq, "$cam_mode", 1)
  ],
  [
    #swy-- if the player agent is the currently selected agent
    (get_player_agent_no, ":player_agent"),
    (eq, ":player_agent", "$cam_current_agent"),

    #swy-- is not empty-handed
    (agent_get_wielded_item, ":weapon", "$cam_current_agent", 0),
    (neq, ":weapon", -1),

    #swy-- and is wielding a bow/crossbow/thrown
    (item_get_type,   ":type", ":weapon"),
    (this_or_next|eq, ":type", itp_type_bow),
    (this_or_next|eq, ":type", itp_type_crossbow),
    (             eq, ":type", itp_type_thrown),

    (assign,  "$cam_mode", 0),
    (assign,"$shoot_mode", 1),
    (mission_cam_set_mode, "$cam_mode")
  ]),

  #-- camera_normal (exit from shooting mode)
  (0, 0, 0,
  [
    (neg|key_is_down, key_left_mouse_button),
    (eq,    "$shoot_mode", 1)
  ],
  [
    (assign,  "$cam_mode", 1),
    (assign,"$shoot_mode", 0),
    (mission_cam_set_mode, "$cam_mode")
  ])

] or [])
############## CUSTOM CAMERA END ###################################################################################

##Kham - Unified Animal triggers

tld_animals_init = (
   ti_on_agent_spawn, 0, 0, [],
  [  (store_trigger_param_1, ":agent_no"),
     (agent_is_human, ":agent_no"),
     (agent_get_troop_id,":troopid", ":agent_no"),
     (is_between,  ":troopid", "trp_spider", "trp_dorwinion_sack"),
     (assign,"$animal_is_present",1),#general to activate scripts
   ])


## TLD Animal Strikes: 2 Versions for WB (optimized) / MB (original)


tld_animal_strikes = ((is_a_wb_mt==1) and (
  1, 0, 0, [(eq, "$animal_is_present",1)], [
  (set_fixed_point_multiplier, 100),

  (try_for_agents, ":agent"),
    (agent_is_alive, ":agent"),
    (agent_is_human, ":agent"),
    (agent_is_active, ":agent"),
    (agent_get_troop_id, ":agent_trp", ":agent"),
    
    #This is where we check the type of animal
    (eq|this_or_next, ":agent_trp", "trp_spider"),
    (eq|this_or_next, ":agent_trp", "trp_wolf"),
    (eq, ":agent_trp", "trp_bear"),

    #This is where we get the mount
    (agent_get_horse, ":horse", ":agent"),
    (ge, ":horse", 0),

    #This is where we cache the enemies:
    (agent_ai_get_num_cached_enemies, ":num_nearby_agents", ":agent"),
    (gt, ":num_nearby_agents", 0),

    #Kham - Let's increase the likelihood of special attacks for the big guys, as charge attacks are not enough
    (try_begin),
      (eq, ":agent_trp", "trp_wolf"),
      (assign, ":chance", 45),
    (else_try),
      (assign, ":chance", 55),
    (try_end),

    #Chance is calculated and checked here:
    (store_random_in_range, ":rnd", 0, 100),
    (lt, ":rnd", ":chance"),  #Kham - changed this to the above
    (assign, ":enemy_in_front", 0),

    #Get Agent's position here:
    (agent_get_position, pos6, ":agent"),

    #Look for the cached enemies
    (try_for_range, ":nearby_agent_no", 0, ":num_nearby_agents"),
      (neq, ":enemy_in_front", 1),
      (agent_ai_get_cached_enemy, ":enemy_agent", ":agent", ":nearby_agent_no"),
      (agent_is_alive, ":enemy_agent"),
      (agent_is_active, ":enemy_agent"),
      (agent_get_position, pos8, ":enemy_agent"), 
      (get_distance_between_positions, ":dist", pos6, pos8), #1 , 2
      (lt, ":dist", 300),
      (neg|position_is_behind_position, pos8, pos6), #2, 1
      (assign, ":enemy_in_front", 1),
    (try_end),

    (eq, ":enemy_in_front", 1),

    #Kham - let's give 'em some sounds when attacking
    (try_begin),
      (eq, ":agent_trp", "trp_spider"),
      (assign, ":sound", "snd_spider_strike"),
    (else_try),
      (eq, ":agent_trp", "trp_wolf"),
      (assign, ":sound", "snd_wolf_strike"),
    (else_try),
      (eq, ":agent_trp", "trp_bear"),
      (assign, ":sound", "snd_bear_strike"),
    (try_end),

    (store_random_in_range, ":rnd_2", 0, 100),
    (try_begin),
      (le, ":rnd_2", 25), #25% chance to make sound
      (agent_play_sound, ":horse", ":sound"),
    (try_end),

    #This is where Animation is assigned

    (assign, ":anim", "anim_bear_slap_right"),
    (try_begin),
      (eq, ":agent_trp", "trp_spider"),
      (assign, ":anim", "anim_spider_attack"),
    (else_try),
      (eq, ":agent_trp", "trp_wolf"),
      (try_begin),
        (le, ":rnd_2", 20),
        (assign, ":anim", "anim_warg_leapattack"),
      (else_try),
        (assign, ":anim", "anim_wolf_snap"),
      (try_end),
    (else_try),
      (eq, ":agent_trp", "trp_bear"),
      (store_random_in_range, ":rnd_2", 0, 100),
      (try_begin),
        (le, ":rnd_2", 49),
        (assign, ":anim", "anim_bear_slap_right"),
      (else_try),
        (assign, ":anim", "anim_bear_uppercut"),
      (try_end),
    (try_end),

    (agent_set_animation, ":horse", ":anim"),

    #Damaging Enemies
    (assign, ":damaged_agents", 0),

    (try_for_range, ":nearby_agent_no", 0, ":num_nearby_agents"),
      (agent_ai_get_cached_enemy, ":enemy_agent", ":agent", ":nearby_agent_no"),
      (agent_is_alive, ":enemy_agent"),
      (agent_is_human, ":enemy_agent"),
      (agent_is_active, ":enemy_agent"),
      (agent_get_position, pos8, ":enemy_agent"),
      (get_distance_between_positions, ":dist", pos6, pos8), #1 , 2
      (lt, ":dist", 300),
      (neg|position_is_behind_position, pos8, pos6), #2, 1
      (assign, ":agents_to_damage", 100), 
      (assign, ":channel", 0),
      (agent_get_horse, ":target_horse", ":enemy_agent"),

      (try_begin),
        (eq, ":agent_trp", "trp_spider"),
        (store_random_in_range, reg66, 5, 10),
        (try_begin),
          (le, ":rnd_2", 30), #30% chance for a fly back
          (assign, ":hit_anim", "anim_strike_fly_back"),
        (else_try),
          (assign, ":hit_anim", "anim_strike_legs_front"),
        (try_end),
        (assign, ":agents_to_damage", 1),
      (else_try),
        (eq, ":agent_trp", "trp_wolf"),
        (try_begin),
          (eq, ":anim", "anim_warg_leapattack"),
          (try_begin),
            (lt, ":target_horse", 0),
            (store_random_in_range, reg66, 5, 11), #Kham - reduced from 5, 10, cause there are a lot of wolves
            (assign, ":hit_anim", "anim_strike_fly_back"),
          (else_try),
            (gt, ":target_horse", 0),
            (assign, ":hit_anim", "anim_strike_fly_back"),
            (agent_start_running_away, ":target_horse"),
            (agent_stop_running_away, ":target_horse"),
            (store_random_in_range, reg66, 5, 11), #Kham - reduced from 5, 10, cause there are a lot of wolves
          (try_end),
        (else_try),
          (store_random_in_range, reg66, 3, 11), #Kham - reduced from 10, 15, cause there are a lot of wolves
          (try_begin),
            (lt, ":target_horse", 0),
            (assign, ":hit_anim", "anim_strike_legs_front"),
          (else_try),
            (gt, ":target_horse", 0),
            (assign, ":hit_anim", "anim_strike_legs_front"),
            (assign, ":channel", 1),
          (try_end),
        (try_end),
        (assign, ":agents_to_damage", 1),
      (else_try),
        (eq, ":agent_trp", "trp_bear"),
        (store_random_in_range, reg66, 10, 30),
        (try_begin),
          (lt, ":target_horse", 0),
          (assign, ":hit_anim", "anim_strike_fly_back"),
        (else_try),
          (gt, ":target_horse", 0),
          (assign, ":hit_anim", "anim_strike_fly_back"),
          (agent_start_running_away, ":target_horse"),
          (agent_stop_running_away, ":target_horse"),
        (try_end),
        (assign, ":agents_to_damage", 100),
      (try_end),
      #(display_message, "@DEBUG: Bear strikes!"),
      (try_begin),
        (get_player_agent_no, ":player"),
        (eq, ":enemy_agent", ":player"),
        (display_message, "@Received {reg66} damage."),
      (try_end),
      (le, ":damaged_agents", ":agents_to_damage"), # Allows us to limit the number of agents an animal can strike
      (set_show_messages, 0),
      (store_agent_hit_points,":hp",":enemy_agent",1),
      (val_sub, ":hp", reg66),
      (agent_set_hit_points, ":enemy_agent", ":hp", 1),
      (try_begin),
        (le, ":hp", 0),
        (agent_deliver_damage_to_agent, ":agent", ":enemy_agent"),
      (try_end),
      (set_show_messages, 1),
      (val_add, ":damaged_agents", 1),
      (agent_set_animation, ":enemy_agent", ":hit_anim", ":channel"),
    (try_end),
  (try_end),
    ])

or

## M&B Original Animal Attacks Start Here

 (
  1, 0, 0, [(eq, "$animal_is_present",1)], [
  (set_fixed_point_multiplier, 100),
  (try_for_agents, ":agent"),
    (agent_is_alive, ":agent"),
    (agent_is_human, ":agent"),
    (agent_get_troop_id, ":agent_trp", ":agent"),
    (eq|this_or_next, ":agent_trp", "trp_spider"),
    (eq|this_or_next, ":agent_trp", "trp_wolf"),
    (eq, ":agent_trp", "trp_bear"),
    (agent_get_horse, ":horse", ":agent"),
    (ge, ":horse", 0),
    (call_script, "script_count_enemy_agents_around_agent", ":agent", 300),
    (gt, reg0, 0),
    (store_random_in_range, ":rnd", 0, 100),

    #Kham - Let's increase the likelihood of special attacks for the big guys, as charge attacks are not enough
    (try_begin),
      (eq, ":agent_trp", "trp_wolf"),
      (assign, ":chance", 45),
    (else_try),
      (assign, ":chance", 55),
    (try_end),

    (lt, ":rnd", ":chance"),  #Kham - changed this to the above

    (assign, ":enemy_in_front", 0),
    (try_for_agents, ":target"),
      (neq, ":enemy_in_front", 1),
      (neq, ":agent", ":target"), # Stop hitting yourself!
      (neq, ":agent", ":horse"), # Stop hitting yourself!
      (agent_get_position, pos1, ":agent"),
      (agent_get_position, pos2, ":target"),
      (get_distance_between_positions, ":dist", pos1, pos2),
      (lt, ":dist", 300),
      (neg|position_is_behind_position, pos2, pos1),
      (agent_get_team, ":agent_team", ":agent"),
      (agent_get_team, ":target_team", ":target"),
      (teams_are_enemies, ":agent_team", ":target_team"),
      (assign, ":enemy_in_front", 1),
    (try_end),
    (eq, ":enemy_in_front", 1),
    (assign, ":anim", "anim_bear_slap_right"),
    (try_begin),
      (eq, ":agent_trp", "trp_spider"),
      (assign, ":anim", "anim_spider_attack"),
    (else_try),
      (eq, ":agent_trp", "trp_wolf"),
      (try_begin),
        (le, ":rnd", 10),
        (assign, ":anim", "anim_warg_leapattack"),
      (else_try),
        (assign, ":anim", "anim_wolf_snap"),
      (try_end),
    (else_try),
      (eq, ":agent_trp", "trp_bear"),
      (store_random_in_range, ":rnd", 0, 100),
      (try_begin),
        (le, ":rnd", 49),
        (assign, ":anim", "anim_bear_slap_right"),
      (else_try),
        (assign, ":anim", "anim_bear_uppercut"),
      (try_end),
    (try_end),

    #Kham - let's give 'em some sounds when attacking
    (try_begin),
      (eq, ":agent_trp", "trp_spider"),
      (assign, ":sound", "snd_spider_strike"),
    (else_try),
      (eq, ":agent_trp", "trp_wolf"),
      (assign, ":sound", "snd_wolf_strike"),
    (else_try),
      (eq, ":agent_trp", "trp_bear"),
      (assign, ":sound", "snd_bear_strike"),
    (try_end),

    (try_begin),
      (le, ":rnd", 25), #25% chance to make sound
      (agent_play_sound, ":horse", ":sound"),
    (try_end),

    (agent_set_animation, ":horse", ":anim"),
    (try_for_agents, ":target"),
      (neq, ":agent", ":target"), # Stop hitting yourself!
      (neq, ":agent", ":horse"), # Stop hitting yourself!
      (agent_is_alive, ":agent"),
      (agent_is_human, ":agent"),
      (agent_get_position, pos1, ":agent"),
      (agent_get_position, pos2, ":target"),
      (get_distance_between_positions, ":dist", pos1, pos2),
      (lt, ":dist", 300),
      (neg|position_is_behind_position, pos2, pos1),
      (agent_get_team, ":agent_team", ":agent"),
      (agent_get_team, ":target_team", ":target"),
      (teams_are_enemies, ":agent_team", ":target_team"), 
      (assign, ":damaged_agents", 0),
      (assign, ":agents_to_damage", 100),   
      (try_begin),
        (eq, ":agent_trp", "trp_spider"),
        (store_random_in_range, reg0, 5, 10),
        (try_begin),
          (le, ":rnd", 30), #30% chance for a fly back
          (assign, ":hit_anim", "anim_strike_fly_back"),
        (else_try),
          (assign, ":hit_anim", "anim_strike_legs_front"),
        (try_end),
        (assign, ":agents_to_damage", 1),
      (else_try),
        (eq, ":agent_trp", "trp_wolf"),
        (try_begin),
          (eq, ":anim", "anim_warg_leapattack"),
          (store_random_in_range, reg0, 10, 15), #Kham - reduced from 10, 15, cause there are a lot of wolves
          (assign, ":hit_anim", "anim_strike_fly_back"),
        (else_try),
          (store_random_in_range, reg0, 3, 11), #Kham - reduced from 10, 15, cause there are a lot of wolves
          (assign, ":hit_anim", "anim_strike_legs_front"),
        (try_end),
        (assign, ":agents_to_damage", 1),
      (else_try),
        (eq, ":agent_trp", "trp_bear"),
        (store_random_in_range, reg0, 10, 30),
        (assign, ":hit_anim", "anim_strike_fly_back"),
        (assign, ":agents_to_damage", 100),
      (try_end),
      #(display_message, "@DEBUG: Bear strikes!"),
      (try_begin),
        (get_player_agent_no, ":player"),
        (eq, ":target", ":player"),
        (display_message, "@Received {reg0} damage."),
      (try_end),
      (le, ":damaged_agents", ":agents_to_damage"), # Allows us to limit the number of agents an animal can strike
      (set_show_messages, 0),
      (store_agent_hit_points,":hp",":target",1),
      (val_sub, ":hp", reg0),
      (agent_set_hit_points, ":target", ":hp", 1),
      (try_begin),
        (le, ":hp", 0),
        (agent_deliver_damage_to_agent, ":agent", ":target"),
      (try_end),
      (set_show_messages, 1),
      (val_add, ":damaged_agents", 1),
      (agent_set_animation, ":target", ":hit_anim"),
    (try_end),
  (try_end),
  ])
)


tld_warg_leap_attack = ((is_a_wb_mt==1) and [ 
  (3, 0, 0, [], [
  (set_fixed_point_multiplier, 100),
  
  (try_for_agents, ":agent"), #Instead of Try_For_Agents nested loops, we cache them instead (WB only operation)
    (agent_is_alive, ":agent"),
    (agent_is_human, ":agent"),
    (agent_get_troop_id, ":agent_trp", ":agent"),
    (is_between, ":agent_trp", warg_ghost_begin, warg_ghost_end),
    (agent_get_horse, ":warg", ":agent"),
    (ge, ":warg", 0),
    (agent_ai_get_num_cached_enemies, ":num_nearby_agents", ":agent"),
    (gt, ":num_nearby_agents", 0),

    (store_random_in_range, ":rnd", 0, 100),
    (lt, ":rnd", 55), #Increased the Chance, but reduced the frequency.
    (assign, ":enemy_in_front", 0),

    (agent_get_position, pos6, ":agent"),
  
  (try_for_range, ":nearby_agent_no", 0, ":num_nearby_agents"),
    (neq, ":enemy_in_front", 1),
    (agent_ai_get_cached_enemy, ":enemy_agent", ":agent", ":nearby_agent_no"),
    (agent_is_alive, ":enemy_agent"),
    (agent_get_position, pos8, ":enemy_agent"),
    (get_distance_between_positions, ":dist", pos6, pos8), #1 , 2
    (lt, ":dist", 300),
    (neg|position_is_behind_position, pos8, pos6), #2, 1
    (assign, ":enemy_in_front", 1),
    (try_end),
  
    (eq, ":enemy_in_front", 1),

    #Kham - let's give 'em some sounds when attacking
    (try_begin),
      (le, ":rnd", 25), 
    (agent_play_sound, ":warg", "snd_wolf_strike"),
    (else_try),
      (agent_play_sound, ":warg", "snd_warg_lone_woof"),
    (try_end),

    (agent_set_animation, ":warg", "anim_warg_leapattack"),
  
  (assign, ":damaged_agents", 0),
  (try_for_range, ":nearby_agent_no", 0, ":num_nearby_agents"),
    (agent_ai_get_cached_enemy, ":enemy_agent", ":agent", ":nearby_agent_no"),
    (agent_is_alive, ":enemy_agent"),
      (agent_is_human, ":enemy_agent"),
      (agent_get_position, pos8, ":enemy_agent"),
      (get_distance_between_positions, ":dist", pos6, pos8), #1 , 2
      (lt, ":dist", 300),
      (neg|position_is_behind_position, pos8, pos6), #2, 1
      (store_random_in_range, reg66, 10, 16),
      (store_random_in_range, ":rand_2", 0, 100),
      (assign, ":channel", 0),
      (agent_get_horse, ":target_horse", ":enemy_agent"),
      (try_begin),
        (le, ":rand_2", 15), #15% chance for a fly back
        (try_begin),
          (lt, ":target_horse", 0),
          (assign, ":hit_anim", "anim_strike_fly_back"),
          (assign, reg66, 5),
        (else_try),
          (gt, ":target_horse", 0),
          (assign, ":hit_anim", "anim_strike_fly_back"),
          (agent_start_running_away, ":target_horse"),
          (agent_stop_running_away, ":target_horse"),
          (assign, reg66, 5),  
        (try_end),
      (else_try),
        (try_begin),
          (gt, ":target_horse", 0), 
          (assign, ":hit_anim", "anim_strike_legs_front"),
          (assign, ":channel", 1),
        (else_try),
          (assign, ":hit_anim", "anim_strike_chest_front"),
        (try_end),
      (try_end),
      #(display_message, "@DEBUG: Warg Jump!"),
      (try_begin),
        (get_player_agent_no, ":player"),
        (eq, ":enemy_agent", ":player"),
        (display_message, "@Received {reg66} damage."),
      (try_end),
      (le, ":damaged_agents", 1), # Allows us to limit the number of agents an animal can strike #
      (set_show_messages, 0),
      (store_agent_hit_points,":hp",":enemy_agent",1),
      (val_sub, ":hp", reg66),
      (agent_set_hit_points, ":enemy_agent", ":hp", 1),
      (try_begin),
        (le, ":hp", 0),
        (agent_deliver_damage_to_agent, ":agent", ":enemy_agent"),
      (try_end),
      (set_show_messages, 1),
      (val_add, ":damaged_agents", 1),
      (agent_set_animation, ":enemy_agent", ":hit_anim", ":channel"),
    (try_end),
  (try_end),
  ])

] or [])

## TLD Remove Riderless Animals: 2 Versions for WB (optimized) / MB (original)

tld_remove_riderless_animals =(
  1, 0, 0, [(eq, "$animal_is_present",1)], [
  (try_for_agents, ":agent"),
    (agent_is_alive, ":agent"),
    (agent_is_human, ":agent"),
    (agent_get_troop_id, ":agent_trp", ":agent"),
    (eq|this_or_next, ":agent_trp", "trp_spider"),
    (eq|this_or_next, ":agent_trp", "trp_bear"),
    (eq,              ":agent_trp", "trp_wolf"),
    (agent_get_horse, ":horse", ":agent"),
    (lt, ":horse", 0),
    (call_script, "script_remove_agent", ":agent"),
  (try_end),
])


tld_spawn_battle_animals = ((is_a_wb_mt==1) and [

  (ti_on_agent_spawn, 0,0, [
    (eq, "$tld_spawn_battle_animals", 1),
    (store_trigger_param_1, ":agent"),

    (agent_get_troop_id, ":agent_trp",":agent"),
    (gt, ":agent_trp", 0),

    (this_or_next|eq, ":agent_trp", "trp_dunnish_wolf_guard"),
    (this_or_next|eq, ":agent_trp", "trp_beorn_lord"),
    (this_or_next|eq, ":agent_trp", "trp_npc17"),
    (eq, ":agent_trp", "trp_player"),

    (assign, ":base_chance", 45), #45% chance to spawn a wolf

    (try_begin),
      (eq, ":agent_trp", "trp_player"),
      (assign, ":beorn_shield_equipped", 0),
      (try_for_range, ":item_slot", ek_item_0, ek_head),
        (eq, ":beorn_shield_equipped", 0),
        (agent_get_item_slot, ":item", ":agent", ":item_slot"),
        (gt, ":item", "itm_no_item"),
        (eq, ":item", "itm_beorn_shield_reward"),
        (assign, ":beorn_shield_equipped", 1),
      (try_end),

      (eq, ":beorn_shield_equipped", 1),
      (assign, ":base_chance", 10),
      (store_skill_level, ":wildcraft", "skl_persuasion", "trp_player"), 
      (store_mul, ":multiplier", ":wildcraft", 9),
      (val_add, ":base_chance", ":multiplier"),
    (else_try),
      (eq, ":agent_trp", "trp_player"),
      (assign, ":base_chance", -1),
    (try_end),


    (store_random_in_range, ":rnd", 0, 100),

    (le, ":rnd", ":base_chance")], 
    [
      (store_trigger_param_1, ":agent"),

      (agent_get_troop_id, ":agent_trp",":agent"),

      (this_or_next|eq, ":agent_trp", "trp_dunnish_wolf_guard"),
      (this_or_next|eq, ":agent_trp", "trp_beorn_lord"),
      (this_or_next|eq, ":agent_trp", "trp_npc17"),
      (eq, ":agent_trp", "trp_player"),

      (set_fixed_point_multiplier, 100),
      (agent_get_position, pos1, ":agent"),
      (position_move_x, pos1, 150),
      (set_spawn_position, pos1),
      (try_begin),
        (this_or_next|eq, ":agent_trp", "trp_npc17"),
        (this_or_next|eq, ":agent_trp", "trp_player"),
        (eq, ":agent_trp", "trp_beorn_lord"),
        (spawn_agent, "trp_bear"),
        (store_faction_of_troop, ":troop_faction", ":agent_trp"),
        (store_relation, ":relations", ":troop_faction", "$players_kingdom"),
        (try_begin),
          (gt, ":relations", 0),
          (assign, ":color", color_good_news),
        (else_try),
          (assign, ":color", color_bad_news),
        (try_end),
        (display_message, "@A bear has been summoned to battle!", ":color"),
      (else_try),
        (spawn_agent, "trp_wolf"),
      (try_end),
      (assign, ":animal", reg0),
      (assign, "$animal_is_present", 1),
      (agent_add_relation_with_agent, ":agent", ":animal", 0),
      (agent_set_hit_points, ":animal", 100, 0),
      
      (agent_get_team, ":agent_team", ":agent"),
      (agent_set_team, ":animal", ":agent_team"),
      (agent_get_division, ":agent_division", ":agent"),
      (agent_set_division, ":animal", ":agent_division"),
  ]),

  (ti_on_order_issued, 0, 0,
    [
      (eq, "$animal_is_present", 1),
      (store_trigger_param, ":order_no", 1),
      (eq, ":order_no", mordr_dismount),
    ],
    [
      (try_for_agents, ":agent"),
        (agent_get_troop_id, ":agent_trp",":agent"),
        (this_or_next|eq, ":agent_trp", "trp_wolf"),
        (eq, ":agent_trp", "trp_bear"),
        (agent_is_active, ":agent_trp"),
        (agent_is_alive,  ":agent_trp"),
        (get_player_agent_no, ":player_agent"),
        (agent_get_team, ":player_team", ":player_agent"),
        (agent_get_division, ":animal_division", ":agent"),
        (set_show_messages, 0),
        (team_give_order, ":player_team", ":animal_division", mordr_mount),
        (set_show_messages, 1),
      (try_end),
  ])
  
] or [])


tld_common_battle_scripts = ((is_a_wb_mt==1) and [

    ### WB only triggers 
    tld_archer_aim_fix,
    tld_archer_aim_fix_on_release,
    tld_move_ai,
    tld_ai_kicking,
    tld_ai_is_kicked,
    tld_melee_ai,
    #tld_footwork_melee_ai,
    tld_improved_horse_archer_ai,
    hp_shield_init,
    hp_shield_trigger,
    health_restore_on_kill,

    #Batching
    batching_agent_spawn_human,
    batching_agent_spawn_mount,

    
] or [] ) + [

	#tld_fix_viewpoint,
	#tld_wargs_attack_horses, # WIP (CppCoder)
	tld_slow_wounded,
 	custom_tld_spawn_troop, custom_tld_init_battle,
	custom_tld_horses_hate_trolls, custom_troll_hitting,
	tld_cheer_on_space_when_battle_over_press, tld_cheer_on_space_when_battle_over_release,
	nazgul_sweeps,
	custom_warg_sounds, custom_lone_wargs_are_aggressive, #custom_lone_wargs_special_attack, # WIP, needs more work (mtarini); Improved, but still WIP. (CppCoder)
	tld_player_cant_ride,
	custom_track_companion_casualties,
	common_battle_healing,
	#common_battle_kill_underwater,
  tld_animals_init,
  tld_animal_strikes,
  tld_remove_riderless_animals,
  reset_fog,
  horse_whistle_init,
  horse_whistle,
] + tld_morale_triggers + fade + khams_custom_player_camera + tld_fallen_riders_get_damaged + bright_nights + tld_spawn_battle_animals + tld_warg_leap_attack


tld_siege_battle_scripts = [
	#tld_fix_viewpoint,
 	custom_tld_spawn_troop, custom_tld_init_battle,
	tld_cheer_on_space_when_battle_over_press, tld_cheer_on_space_when_battle_over_release,
	custom_track_companion_casualties,
	common_battle_healing,
	custom_troll_hitting,
	tld_remove_galadriel,
  tld_remove_volunteer_troops,
	#common_battle_kill_underwater,
  reset_fog,
] + fade + bright_nights + khams_custom_player_camera + bright_nights


tld_common_peacetime_scripts = [
	#tld_fix_viewpoint,
	tld_player_cant_ride,
	dungeon_darkness_effect,
  reset_fog,
] + custom_tld_bow_to_kings + bright_nights + fade + khams_custom_player_camera #Custom Cam triggers


tld_common_wb_muddy_water = ((is_a_wb_mt==1) and [

  (ti_before_mission_start,  0, 0, [],
  [
    (try_begin),
      (store_current_scene, ":cur_scene"),
      (this_or_next|eq,  ":cur_scene", "scn_morannon_outside_1"),
      (this_or_next|eq,  ":cur_scene", "scn_morannon_outside_2"),																 
      (this_or_next|eq,  ":cur_scene", "scn_morannon_center"),
      (this_or_next|eq,  ":cur_scene", "scn_morannon_siege"),																 
      (this_or_next|eq,  ":cur_scene", "scn_deadmarshes"),
      (this_or_next|eq,  ":cur_scene", "scn_fangorn"),
      (this_or_next|eq,  ":cur_scene", "scn_mirkwood"),
      
      (this_or_next|eq,  ":cur_scene", "scn_forest_mirkwood1"),
      (this_or_next|eq,  ":cur_scene", "scn_forest_mirkwood2"),
      (this_or_next|eq,  ":cur_scene", "scn_forest_mirkwood3"),
      (this_or_next|eq,  ":cur_scene", "scn_forest_mirkwood4"),
      (this_or_next|eq,  ":cur_scene", "scn_forest_mirkwood5"),
      
      (this_or_next|eq,  ":cur_scene", "scn_moria_castle"),
      (this_or_next|eq,  ":cur_scene", "scn_moria_secret_entry"),
      (this_or_next|eq,  ":cur_scene", "scn_moria_deep_mines"),
      
      (this_or_next|eq,  ":cur_scene", "scn_tld_sorcerer_forest_a"),
      (this_or_next|eq,  ":cur_scene", "scn_tld_sorcerer_forest_b"),
      (this_or_next|eq,  ":cur_scene", "scn_tld_sorcerer_forest_c"),
      
      (this_or_next|eq,  ":cur_scene", "scn_isengard_center"),
      (this_or_next|eq,  ":cur_scene", "scn_isengard_underground"),
      
      (this_or_next|eq,  ":cur_scene", "scn_harad_camp_center"),
      (this_or_next|eq,  ":cur_scene", "scn_north_rhun_camp_center"),
      
      (this_or_next|eq,  ":cur_scene", "scn_minas_morgul_siege"),
      (             eq,  ":cur_scene", "scn_minas_morgul_center"),
      
      (set_river_shader_to_mud),
    (try_end),
  ]),

] or [])

#Kham - Unified Siege Triggers

tld_common_siege_start = (
  ti_before_mission_start, 0, 0, [],[
    (team_set_relation, 0, 2, 1),(team_set_relation, 0, 4, 1),(team_set_relation, 4, 2, 1), # TLD expand teams
    (team_set_relation, 1, 3, 1),(team_set_relation, 1, 5, 1),(team_set_relation, 5, 3, 1),
    (team_set_relation, 6, 0, 1),(team_set_relation, 6, 2, 1),(team_set_relation, 6, 4, 1), # TLD gate aggravator team
    (assign, "$gate_aggravator_agent",-1), # can be reassigned by destructible gate scene prop presence
    (call_script, "script_change_banners_and_chest"),
    (call_script, "script_remove_siege_objects"),
  ])

tld_common_siege_question_answered = (
  ti_question_answered, 0, 0, [],[
    (store_trigger_param_1,":answer"),
    (eq,":answer",0),
    (assign, "$pin_player_fallen", 0),
    (get_player_agent_no, ":player_agent"),
    (agent_get_team, ":agent_team", ":player_agent"),
    (try_begin),
      (neq, "$attacker_team", ":agent_team"),
      (neq, "$attacker_team_2", ":agent_team"),
      (neq, "$attacker_team_3", ":agent_team"), # if defender - cannot retreat
      (str_store_string, s5, "str_can_not_retreat"),
      #(call_script, "script_simulate_retreat", 8, 15),
    (else_try),
      (str_store_string, s5, "str_retreat"),
      (call_script, "script_simulate_retreat", 5, 20),
    (try_end),
      (call_script, "script_count_mission_casualties_from_agents"),
      (finish_mission,0),
    ])

tld_common_siege_init = (
  0, 0, ti_once, [],[
    (assign,"$battle_won",0),
    (assign,"$defender_reinforcement_stage",0),
    (assign,"$attacker_reinforcement_stage",0),
    (assign,"$g_presentation_battle_active", 0),
    (assign,"$telling_counter",0),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_siege),
    ])

tld_common_siege_set_slot = (
  ti_on_agent_spawn, 0, 0, [],
        [
          (store_trigger_param_1, ":agent_no"),
          (agent_is_human, ":agent_no"),
          (agent_is_alive, ":agent_no"),
          (agent_set_slot, ":agent_no", slot_agent_arena_team_set,0),
        ])

tld_common_siege_ai_trigger_init = (
  ti_before_mission_start, 0, 0,[
    (assign, "$defender_team"  , 0),
    (assign, "$attacker_team"  , 1),
    (assign, "$defender_team_2", 2),
    (assign, "$attacker_team_2", 3),
    (assign, "$defender_team_3", 4),
    (assign, "$attacker_team_3", 5),
    ],[])

tld_common_siege_ai_trigger_init_after_2_secs =(
  0, 2, ti_once, [
  ], [
  (try_for_agents, ":agent_no"),
  (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 1),
  (try_end)
])

tld_common_siege_attacker_reinforcement_check = (
  1, 0, 5,
  [(lt,"$attacker_reinforcement_stage", 15)],
  [
   (assign,":atkteam","$attacker_team"),
   (assign,":entry",7), #iterate through 8 9 10
   (try_for_range,":unused",0,3), #cycle through attacker teams, check if depleted and reinforce
     (store_normalized_team_count,":num_attackers",":atkteam"),
     (val_add,":atkteam",2),
     (val_add,":entry",1),
     (lt,":num_attackers",10),
     (add_reinforcements_to_entry, ":entry", 12),
     (val_add,"$attacker_reinforcement_stage", 1),
     (assign, "$attacker_archer_melee",1), #Kham - Every reinforcement event leads to a refresh of attack mode.
   (try_end)])

tld_common_siege_defender_reinforcement_check = (
  3, 0, 5, [],
 [(lt,"$defender_reinforcement_stage", 15),
   (store_mission_timer_a,":mission_time"),
   (ge,":mission_time",10)],[
   (assign,":defteam","$defender_team"),
   (assign,":entry",4), #iterate through 5 6 7
   (try_for_range,":unused",0,3), #cycle through defender teams, check if depleted and reinforce
     (store_normalized_team_count,":num_defenders",":defteam"),
     (val_add,":defteam",2),
     (val_add,":entry",1),
     (lt,":num_defenders",14),
     (add_reinforcements_to_entry, ":entry", 10), #TLD, was 4, 7
     (val_add,"$defender_reinforcement_stage",1),
   (try_end),
   (try_begin),
     (ge, "$defender_reinforcement_stage", 7),
     (set_show_messages, 0),
     (team_give_order, "$defender_team"  , grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
     (team_give_order, "$defender_team_2", grc_infantry, mordr_charge),
     (team_give_order, "$defender_team_3", grc_infantry, mordr_charge),
     (set_show_messages, 1),
     (display_message,"@Defenders: infantry CHARGE!!"),
     (ge, "$defender_reinforcement_stage", 14),
     (set_show_messages, 0),
     (team_give_order, "$defender_team"  , grc_everyone, mordr_charge), #AI desperate charge: everyone!!!
     (team_give_order, "$defender_team_2", grc_everyone, mordr_charge),
     (team_give_order, "$defender_team_3", grc_everyone, mordr_charge),
     (set_show_messages, 1),
     (display_message,"@Defenders: everyone CHARGE!!"),
   (try_end),
    # put gate aggravator in place
   (try_begin),
     (neq, "$gate_aggravator_agent",-1),
     (eq, "$gate_breached",0),
     (entry_point_get_position, pos13, 39),
     (agent_set_scripted_destination,"$gate_aggravator_agent",pos13,1),
     (agent_set_position,"$gate_aggravator_agent",pos13),
     (agent_set_hit_points,"$gate_aggravator_agent",100,0),
   (try_end)])

tld_common_siege_defender_reinforcement_archer_reposition = (
  2, 0, 0,
  [
    (gt, "$defender_reinforcement_stage", 0),
  ],
  [
    (call_script, "script_siege_move_archers_to_archer_positions"),
])

tld_common_siege_check_defeat_condition = (
  1, 4, ti_once,
  [
    (main_hero_fallen)
  ],
  [
    (assign, "$pin_player_fallen", 1),
    (get_player_agent_no, ":player_agent"),
    (agent_get_team, ":agent_team", ":player_agent"),
    (try_begin),
      (neq, "$attacker_team", ":agent_team"),
      (neq, "$attacker_team_2", ":agent_team"),
      (neq, "$attacker_team_3", ":agent_team"),
      (str_store_string, s5, "str_siege_continues"),
      (call_script, "script_simulate_retreat", 8, 15, 0),
    (else_try),
      (str_store_string, s5, "str_retreat"),
      (call_script, "script_simulate_retreat", 5, 20, 0),
    (try_end),
    (assign, "$g_battle_result", -1),
    (set_mission_result,-1),
    (call_script, "script_count_mission_casualties_from_agents"),
    (finish_mission,0),
])

tld_common_siege_refill_ammo = (
  120, 0, 0, [],
  [#refill ammo of defenders every two minutes. #chief change to 4 m #InVain: back to two minutes, was 3
    (get_player_agent_no, ":player_agent"),
    (try_for_agents,":cur_agent"),
      (neq, ":cur_agent", ":player_agent"),
      (agent_is_alive, ":cur_agent"),
      (agent_is_human, ":cur_agent"),
      ##      (agent_is_defender, ":cur_agent"),
      (agent_get_team, ":agent_team", ":cur_agent"),
      (this_or_next|eq, ":agent_team", "$defender_team"),
      (this_or_next|eq, ":agent_team", "$defender_team_2"),
      (eq, ":agent_team", "$defender_team_3"),
      (agent_refill_ammo, ":cur_agent"),
    (try_end),
])


mission_templates = [ # not used in game
( "town_default",0,-1, "Default town visit",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),(1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (8,mtef_scene_source,af_override_horse,0,1,[]),(9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_scene_source,af_override_horse,0,1,[]),(11,mtef_scene_source,af_override_horse,0,1,[]),(12,mtef_scene_source,af_override_horse,0,1,[]),(13,mtef_scene_source,0,0,1,[]),(14,mtef_scene_source,0,0,1,[]),(15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),(24,mtef_visitor_source,af_override_horse,0,1,[]),
     (25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,0,1,[]),(28,mtef_visitor_source,af_override_horse,0,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     ],
    [ (ti_on_agent_spawn, 0, 0, [],[(store_trigger_param_1, ":agent_no"),(call_script, "script_init_town_agent", ":agent_no")]),
      
      (1, 0, ti_once, [], [			# ambience sounds
        (try_begin),
          (is_currently_night),
          (play_sound, "$bs_night_sound", sf_looping),
        (else_try),
          (play_sound, "$bs_day_sound",   sf_looping),
        (try_end),
        (store_current_scene, ":cur_scene"),
        (scene_set_slot, ":cur_scene", slot_scene_visited, 1)
      ]),
      
      (ti_before_mission_start,  0, 0, [], [(call_script, "script_change_banners_and_chest")]),
      (ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1)],[]),
      (ti_tab_pressed,           0, 0, [(set_trigger_result,1)],[]),
]),
# This template is used in party encounters and such.
( "conversation_encounter",0,-1,
  "Conversation_encounter",
    [( 0,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 1,mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
     ( 2,mtef_visitor_source,0,0,1,[]),( 3,mtef_visitor_source,0,0,1,[]),( 4,mtef_visitor_source,0,0,1,[]),( 5,mtef_visitor_source,0,0,1,[]),( 6,mtef_visitor_source,0,0,1,[]),
     ( 7,mtef_visitor_source,0,0,1,[]),( 8,mtef_visitor_source,0,0,1,[]),( 9,mtef_visitor_source,0,0,1,[]),(10,mtef_visitor_source,0,0,1,[]),(11,mtef_visitor_source,0,0,1,[]),
    #prisoners now...
     (12,mtef_visitor_source,0,0,1,[]),(13,mtef_visitor_source,0,0,1,[]),(14,mtef_visitor_source,0,0,1,[]),(15,mtef_visitor_source,0,0,1,[]),(16,mtef_visitor_source,0,0,1,[]),
    #Other party
     (17,mtef_visitor_source,0,0,1,[]),(18,mtef_visitor_source,0,0,1,[]),(19,mtef_visitor_source,0,aif_start_alarmed,1,[]),(20,mtef_visitor_source,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source,0,aif_start_alarmed,1,[]),
     (22,mtef_visitor_source,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source,0,aif_start_alarmed,1,[]),(24,mtef_visitor_source,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source,0,aif_start_alarmed,1,[]),(26,mtef_visitor_source,0,aif_start_alarmed,1,[]),
     (27,mtef_visitor_source,0,aif_start_alarmed,1,[]),(28,mtef_visitor_source,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source,0,aif_start_alarmed,1,[]),(30,mtef_visitor_source,0,aif_start_alarmed,1,[]),
	 (31,mtef_visitor_source,af_override_all,0,1,[itm_feet_chains]),#(32,mtef_attackers|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [ # other people in the backgroud (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", 17, af_override_all),
		(ti_on_agent_spawn, 0, 0, [], [
			(store_trigger_param_1, ":agent"),
			(agent_is_human, ":agent"),
			(store_random_in_range,reg0,0,100),(agent_set_animation_progress, ":agent", reg0), # break sincrony of people on background (mtarini)
			
			# (agent_get_entry_no,reg1,":agent"),
			# (eq, reg1, 1), # only those at entry point 1
			# (agent_get_troop_id, reg42, ":agent"),
			# (neq, reg42, "trp_player"),
			# (store_troop_faction, reg2, reg42),
			# (store_relation,reg1,reg2,"$players_kingdom"),
			# (display_message, "@Relations to player: {reg1}"),
			# (lt, reg1, 0),
				# (assign,"$talk_context",tc_prisoner_talk),
				# (assign, reg41, ":agent"), 
			    # (display_message, "@ATTEMPT REMEMBERING PRISONER AGENT!"),
				# (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", 1, af_override_all),
				# (mission_tpl_entry_add_override_item,  "mt_conversation_encounter", 1, "itm_prisoner_coll_chain")
		]),
		# (0,0, ti_once, [],[ #(eq,"$talk_context",tc_prisoner_talk)
			# (call_script, "script_remove_agent", reg41),
			# (add_visitors_to_current_scene,31, "trp_knight_2_11",1),
			# (display_message, "@ATTEMPT SPAWNING!"),]),
			
		# friendly greetings (after 0.35 secs)
		(0, 0.35, ti_once, [], [ 
			(eq,"$party_meeting",1), # friendly
			(try_for_agents,":agent"),
				(agent_is_human, ":agent"),
				(agent_get_entry_no,":e",":agent"),
				(try_begin),
					(eq,":e",17),
					(agent_get_troop_id, ":trp", ":agent"),
					(troop_get_type, ":race", ":trp"),
					(store_troop_faction, ":fac", ":trp"),
					(assign, ":greet_ani", -1),
					(this_or_next|is_between,  ":race", tf_orc_begin, tf_orc_end),(neg|faction_slot_eq, ":fac", slot_faction_rank, 0),
					(try_begin), (is_between,  ":race", tf_elf_begin, tf_elf_end), 
						(assign, ":greet_ani", "anim_greet_elf"),
					(else_try), (eq,  ":race", tf_orc), 
						(assign, ":greet_ani", "anim_greet_orc"),
					(else_try),
						(this_or_next|eq, ":fac", "fac_gondor"),
						(this_or_next|eq, ":fac", "fac_umbar"),
						(eq, ":fac", "fac_rohan"),
						(assign, ":greet_ani", "anim_greet_human"),
					(else_try), (is_between,  ":race", tf_orc_begin, tf_orc_end),  # other orcs
						(assign, ":greet_ani", "anim_greet_goaway"),
					(else_try), # all others
						(assign, ":greet_ani", "anim_greet_simple"),
					(try_end),
					(try_begin),
						(gt,":greet_ani",0), 
						(agent_get_horse,reg1,":agent"),					
						(try_begin),(ge,reg1,0), 
							(val_add, ":greet_ani", 1),
						(try_end),
						(agent_set_animation, ":agent", ":greet_ani"),
					(try_end),
				# (else_try),
					# (agent_set_animation, ":agent", "anim_stand"),
					# (store_random_in_range,reg0,0,100),
					# (agent_set_animation_progress, ":agent", reg0),
				(try_end),
			(try_end)]),
	   
     (0.3, 0, 2, [], [ 
		(try_begin),
			(eq,"$party_meeting",-1), # hostile, and only once
			(try_for_agents,":agent"),
			(agent_is_human, ":agent"),
				(agent_get_entry_no,reg1,":agent"),(neq,reg1,0),(neq,reg1,17),(neq,reg1,18), # main guys do not cheer
				(neq,reg1,31), # prisoners do not cheer
				(store_random_in_range,reg1,0,100),(lt,reg1,3), # 3% of times
				(agent_get_horse,reg1,":agent"),					
				(try_begin),(eq,reg1,-1),(agent_set_animation, ":agent", "anim_cheer"),
				 (else_try),			 (agent_set_animation, ":agent", "anim_cheer_player_ride"),
				(try_end),
				(agent_get_troop_id,":troop", ":agent"),
				(troop_get_type,reg1,":troop"),
				(try_begin),
					(is_between, reg1, tf_urukhai, tf_orc_end),
					(agent_play_sound, ":agent", "snd_meeting_uruk"),
				(else_try),
					(eq, reg1, tf_orc),
					(agent_play_sound, ":agent", "snd_meeting_orc"),
				(else_try),
					(is_between, reg1, tf_elf_begin, tf_elf_end),
					(agent_play_sound, ":agent", "snd_meeting_elf"),
				(else_try),				
					(agent_play_sound, ":agent", "snd_meeting_man"),
				(try_end),
			(try_end),
		(try_end)]),
]),
#----------------------------------------------------------------
#mission templates before this point are hardwired into the game.
#-----------------------------------------------------------------
( "town_center",0,-1,
    "Default town visit",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),(3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),(5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),(7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (8 ,mtef_scene_source,af_override_horse,0,1,[]),
     (9 ,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,0,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_scene_source,0,0,1,[]),(14,mtef_scene_source,0,0,1,[]),(15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_castle_warlord,0,1,[]),(17,mtef_visitor_source,af_castle_warlord,0,1,[]),(18,mtef_visitor_source,af_castle_warlord,0,1,[]),(19,mtef_visitor_source,af_castle_warlord,0,1,[]),(20,mtef_visitor_source,af_castle_warlord,0,1,[]),(21,mtef_visitor_source,af_castle_warlord,0,1,[]),(22,mtef_visitor_source,af_castle_warlord,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),(25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,0,1,[]),(28,mtef_visitor_source,af_override_horse,0,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     (32,mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),(33,mtef_visitor_source,af_override_horse|af_override_weapons,0,1,[]),(34,mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),(35,mtef_visitor_source,af_override_horse|af_override_weapons,0,1,[]),(36,mtef_visitor_source,af_override_horse,0,1,[]),(37,mtef_visitor_source,af_override_horse|af_override_head,0,1,[]),(38,mtef_visitor_source,af_override_horse|af_override_weapons,0,1,[]),(39,mtef_visitor_source,af_override_horse,0,1,[]),
     (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    tld_common_wb_muddy_water+
    tld_common_peacetime_scripts +[
       
	(1, 0, ti_once, [],[ # set walkers, music and ambient sounds
			(get_player_agent_no, "$current_player_agent"),
			(try_begin),
				(eq, "$g_mt_mode", tcm_default),
				(store_current_scene, ":cur_scene"),
				(scene_set_slot, ":cur_scene", slot_scene_visited, 1),
			(try_end),
			(call_script, "script_init_town_walker_agents"),
			(try_begin),(eq, "$sneaked_into_town", 1),(call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
			 (else_try),                              (call_script, "script_music_set_situation_with_culture", mtf_sit_town), #MV: was mtf_sit_travel
			(try_end),

			(try_begin),
				(eq, "$bs_day_sound", 0),
				(party_get_slot, ":a","$current_town",slot_center_ambient_sound_always),
				(try_begin),(gt,":a",0),(play_sound, ":a", sf_looping),(try_end),
			(else_try),
				(play_sound, "$bs_day_sound", sf_looping),
			(try_end),
			(neg|is_currently_night),
			(try_begin),
				(eq, "$bs_night_sound", 0),
				(party_get_slot, ":a","$current_town",slot_center_ambient_sound_day),
				(try_begin),(gt,":a",0),(play_sound, ":a", sf_looping),(try_end),
			(else_try),
				(play_sound, "$bs_night_sound", sf_looping),
			(try_end),
			]),
  (10, 0, ti_once, [], [ # Kham - Set Tutorial Message RE: Rumours
      (try_begin),
        (eq, "$first_time_town", 0),
        (tutorial_message, "@While visiting towns, settlements and camps, you can talk to people walking around. Members of different factions have different things to say - some will let you in on their own thoughts, others will share rumours. Both could merely give you a better understanding of the person's culture and faction, or they might hold clues to finding secret locations, or tips and tricks for travelling through the Wilderness and fighting in the War of the Ring.",0,15),
        (assign, "$first_time_town",1),
      (try_end),
      ]),
	(ti_before_mission_start, 0, 0, [], [
			(call_script, "script_change_banners_and_chest"),
			(try_begin),# remove beam bridges in osgiliath (for non battle scenes)
				(store_current_scene, ":cur_scene"),
				(this_or_next|eq,  ":cur_scene", "scn_east_osgiliath_center"),
				(             eq,  ":cur_scene", "scn_west_osgiliath_center"),
				(replace_scene_props, "spr_osgiliath_broken_bridge_beams", "spr_empty"),
			(try_end),
			# check if dungeons are present in a scene
			(assign, "$dungeons_in_scene", 0), 
			(try_for_range,":cur_scene","spr_light_fog_black0","spr_moria_rock"),
				(scene_prop_get_num_instances,":max_instance", ":cur_scene"),
				(ge,":max_instance", 1),
				(assign, "$dungeons_in_scene", 1), 
			(try_end),
			# put appropriate rain/snow
			(try_begin),
				(store_current_scene, ":cur_scene"),
				(is_between,  ":cur_scene", "scn_caras_galadhon_center", "scn_woodsmen_village_center"),
				(set_rain, 2,100), #yellow thingies in elven places
			(else_try),
				(set_rain, 0,100),
			(try_end),
			
			]),
	(ti_inventory_key_pressed, 0, 0, [],[
			(try_begin),
				(eq, "$g_mt_mode", tcm_default),
				(set_trigger_result,1),
			(else_try),
				(eq, "$g_mt_mode", tcm_disguised),
				(display_message,"str_cant_use_inventory_disguised"),
			(else_try),
				(display_message, "str_cant_use_inventory_now"),
			(try_end)]),
	(ti_tab_pressed, 0, 0,[],[
          (try_begin),
             (this_or_next|eq, "$g_mt_mode", tcm_default),
             (eq, "$g_mt_mode", tcm_disguised),
             (try_begin),
               (check_quest_active, "qst_hunt_down_fugitive"),
               (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
               (neg|check_quest_failed, "qst_hunt_down_fugitive"),
               (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
               (quest_get_slot, ":quest_object_troop", "qst_hunt_down_fugitive", slot_quest_object_troop),
               (try_begin),
                 (call_script, "script_cf_troop_agent_is_alive", ":quest_object_troop"),
                 (call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
               (else_try),
                 (call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
               (try_end),
             (try_end),
             (set_trigger_result,1),
           (else_try),
             (display_message, "@Cannot leave now."),
           (try_end)]),

	(ti_on_leave_area, 0, 0,[(try_begin),(eq, "$g_defending_against_siege", 0),(assign,"$g_leave_town",1),(try_end)],[]),
	(3, 0, 0, [(call_script, "script_tick_town_walkers")], []),
	(2, 0, 0, [(call_script, "script_center_ambiance_sounds")], []),
	(1, 0, ti_once, [
			(check_quest_active, "qst_hunt_down_fugitive"),
			(neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
			(neg|check_quest_failed, "qst_hunt_down_fugitive"),
			(quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
			(quest_get_slot, ":quest_object_troop", "qst_hunt_down_fugitive", slot_quest_object_troop),
			(assign, ":not_alive", 0),
			(try_begin),
				(call_script, "script_cf_troop_agent_is_alive", ":quest_object_troop"),
			(else_try),
				(assign, ":not_alive", 1),
			(try_end),
			(this_or_next|main_hero_fallen),
			(eq, ":not_alive", 1)
			],[
			(try_begin),
				(main_hero_fallen),
				(jump_to_menu, "mnu_village_hunt_down_fugitive_defeated"),
				(call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
				(finish_mission, 4),
			(else_try),
				(call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
			(try_end)]),
	(2, 0, 0, [],     # check for different checkpoints reach (merchants, center of town etc)
       [(get_player_agent_no, "$current_player_agent"),
	    (agent_get_position, pos1, "$current_player_agent"),
    (assign, reg3, 50),
		(try_begin),
			(party_slot_eq, "$current_town", slot_center_visited, 0),
			(entry_point_get_position, pos2, 0),
			(get_distance_between_positions, ":dist", pos2, pos1),
			(lt, ":dist", 500),
			(party_set_slot, "$current_town", slot_center_visited, 1),
		(try_end),
		(try_begin),
			(party_slot_eq, "$current_town", slot_weaponsmith_visited, 0),
			(neg|party_slot_eq, "$current_town", slot_town_weaponsmith, "trp_no_troop"),
			(entry_point_get_position, pos2, 10),
			(get_distance_between_positions, ":dist", pos2, pos1),
			(lt, ":dist", 300),
			(party_set_slot, "$current_town", slot_weaponsmith_visited, 1),
			(party_set_slot, "$current_town", slot_center_visited, 1), # assume visited when found at least 1 merchant
			(display_message, "@You_have_found_the_local_smithy... (+{reg3} XP)"),
      (add_xp_as_reward, 50),
		(try_end),      
		(try_begin),
			(party_slot_eq, "$current_town", slot_elder_visited, 0),
			(neg|party_slot_eq, "$current_town", slot_town_elder, "trp_no_troop"),
			(entry_point_get_position, pos2, 11),
			(get_distance_between_positions, ":dist", pos2, pos1),
			(lt, ":dist", 300),
			(party_set_slot, "$current_town", slot_elder_visited, 1),
			(party_set_slot, "$current_town", slot_center_visited, 1), # assume visited when found at least 1 merchant
			(display_message, "@You_have_found_the_local_authority...(+{reg3} XP)"),
      (add_xp_as_reward, 50),
		(try_end),      
		(try_begin),
			(party_slot_eq, "$current_town", slot_merchant_visited, 0),
			(neg|party_slot_eq, "$current_town", slot_town_merchant, "trp_no_troop"),
			(entry_point_get_position, pos2, 12),
			(get_distance_between_positions, ":dist", pos2, pos1),
			(lt, ":dist", 300),
			(party_set_slot, "$current_town", slot_merchant_visited, 1),
			(party_set_slot, "$current_town", slot_center_visited, 1), # assume visited when found at least 1 merchant
			(display_message, "@You_have_found_the_local_warehouse...(+{reg3} XP)"),
      (add_xp_as_reward, 50),
		(try_end)]),
]),
( "visit_town_castle",0,-1,
  "You enter the halls of the lord.",
    [(0,mtef_scene_source|mtef_team_0,af_castle_warlord,0,1,[]),
     (1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),(3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]), (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]), #for doors
     (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (8,mtef_visitor_source,af_override_horse,0,1,[]),(9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_scene_source,af_override_horse,0,1,[]),(11,mtef_scene_source,af_override_horse,0,1,[]),
     (12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_visitor_source,af_override_horse,0,1,[]),(14,mtef_visitor_source,af_override_horse,0,1,[]),(15,mtef_visitor_source,af_override_horse,0,1,[]),
     (16,mtef_visitor_source,af_castle_warlord,0,1,[]),(17,mtef_visitor_source,af_castle_warlord,0,1,[]),(18,mtef_visitor_source,af_castle_warlord,0,1,[]),(19,mtef_visitor_source,af_castle_warlord,0,1,[]),
     (20,mtef_visitor_source,af_castle_warlord,0,1,[]),(21,mtef_visitor_source,af_castle_warlord,0,1,[]),(22,mtef_visitor_source,af_castle_warlord,0,1,[]),(23,mtef_visitor_source,af_castle_warlord,0,1,[]),
     (24,mtef_visitor_source,af_castle_warlord,0,1,[]),(25,mtef_visitor_source,af_castle_warlord,0,1,[]),(26,mtef_visitor_source,af_castle_warlord,0,1,[]),(27,mtef_visitor_source,af_castle_warlord,0,1,[]),
     (28,mtef_visitor_source,af_castle_warlord,0,1,[]),(29,mtef_visitor_source,af_castle_warlord,0,1,[]),(30,mtef_visitor_source,af_castle_warlord,0,1,[]),(31,mtef_visitor_source,af_castle_warlord,0,1,[])
     ],
    tld_common_wb_muddy_water +
    tld_common_peacetime_scripts + [
      (ti_on_agent_spawn       , 0, 0, [],[ (store_trigger_param_1, ":agent_no"),(call_script, "script_init_town_agent", ":agent_no")]),
      (ti_before_mission_start , 0, 0, [],[ (call_script, "script_change_banners_and_chest"),(assign, "$dungeons_in_scene",1), (assign, "$temp_2", 0),]), #Use temp Global Var to prevent multiple scene prop spawns.
      (ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1)], []),
      (ti_tab_pressed          , 0, 0, [(set_trigger_result,1)], []),
	  (0, 0, ti_once, [], [#(set_fog_distance, 150, 0xFF736252)
        (try_begin),
          (eq, "$talk_context", tc_court_talk),
#          (call_script, "script_music_set_situation_with_culture", mtf_sit_lords_hall),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", 0), #prison
        (try_end)]),

 ] + (is_a_wb_mt==1 and [
  #Henneth Anun at Dusk Scene Prop
  (2, 0, 0, 
    [
      (eq, "$current_town", "p_town_henneth_annun"),
      (store_time_of_day, ":time"),
      (assign, reg5, ":time"),
      #(display_message, "@Time: {reg5}"),
      (is_between, ":time", 18, 21),
    ],    
    [
      (get_player_agent_no, "$current_player_agent"),
      (agent_get_position, pos1, "$current_player_agent"),
      (assign, reg3, 80),
      (try_begin),
        (entry_point_get_position, pos2, 13),
        (try_begin),
          (eq, "$temp_2", 0),
          #(display_message, "@Scene Prop Spawned"),
          (set_spawn_position, pos2),
          (spawn_scene_prop, "spr_moon_beam"),
          (assign, "$temp_2", 1),
        (try_end),
        (get_distance_between_positions, ":dist", pos2, pos1),
        (lt, ":dist", 400),
        (tutorial_message, "@You look through Henneth Annun, the Window of the Sunset. The beautiful sight restores your faith in the West and the Powers beyond.", 0 , 10),
        (party_slot_eq, "$current_town", slot_exploration_point_1, 0),
        (add_xp_as_reward, reg3),
        (party_set_slot, "$current_town", slot_exploration_point_1, 1),
      (try_end),
  ]),
 ] or []) + [	  
]),

# review troops (mtarini)
("review_troops",0,-1,"You review your troops",
[(1,mtef_defenders|mtef_team_0,0,0,0,[]),(0,mtef_defenders|mtef_team_0,0,0,0,[]), # not used
 (1,mtef_attackers|mtef_team_1,0,0,1,[]), # player 
 (4,mtef_attackers|mtef_team_2,0,0,30,[]), # troops
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains] ),  # prisoners (4)
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains] ),  # prisoners

 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains_dwarf] ),  # prisoners  (dwarf)(4)
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains_dwarf] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains_dwarf] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains_dwarf] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains_dwarf] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains_dwarf] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains_dwarf] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains_dwarf] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains_dwarf] ),  # prisoners
 (4,mtef_visitor_source, af_prisoner, 0,0,[itm_feet_chains_dwarf] ),  # prisoners

# Trolls
 (5,mtef_visitor_source, af_prisoner, 0,0,[] ),  # prisoners
 (5,mtef_visitor_source, af_prisoner, 0,0,[] ),  # prisoners
 (5,mtef_visitor_source, af_prisoner, 0,0,[] ),  # prisoners
 (5,mtef_visitor_source, af_prisoner, 0,0,[] ),  # prisoners
 (5,mtef_visitor_source, af_prisoner, 0,0,[] ),  # prisoners
 (5,mtef_visitor_source, af_prisoner, 0,0,[] ),  # prisoners
 (5,mtef_visitor_source, af_prisoner, 0,0,[] ),  # prisoners
 (5,mtef_visitor_source, af_prisoner, 0,0,[] ),  # prisoners
 (5,mtef_visitor_source, af_prisoner, 0,0,[] ),  # prisoners
 (5,mtef_visitor_source, af_prisoner, 0,0,[] ),  # prisoners

  ],
  #tld_common_peacetime_scripts +
  tld_common_wb_muddy_water + bright_nights +
  [  
 
  # make friend, prisoners, players, etc appear at the right locations and with scripted short starting walks
  (ti_on_agent_spawn, 0, 0, [],[
   (store_trigger_param_1, ":agent_no"),
	 
	 (get_player_agent_no, ":player_no"),
	 (agent_get_position, pos1, ":agent_no"),
	 
	 (try_begin),
	  (eq,":player_no", ":agent_no"), # player
		# player was spawned at a distant entry point so that it faces his troops (MaB bug: set poistion doesn't affect ... move back to his troops
		(entry_point_get_position,pos1,4),
		(position_move_y, pos1, 700, 0), # move player in front
		
		(party_get_num_companions, ":nc","p_main_party"),
		(val_mul, ":nc", 50), (val_sub, ":nc", 50), (val_min, ":nc", 750),
		(position_move_x, pos1, ":nc", 0),# center player on X
		#(position_rotate_z, pos1, 180), # rotate player to face troops ... if only this worked... sigh 
		(agent_set_position, ":agent_no", pos1),
		(try_begin),
			(agent_get_horse, reg12, ":agent_no" ),(ge, reg12, 0),
			(agent_set_position, reg12, pos1),
		(try_end),
	 (else_try),
	 
		# NPCS...
		(store_random_in_range,":speed_limit",2,6),
		
		(try_begin),
			(agent_get_horse, reg12, ":agent_no" ),(ge, reg12, 0),
			(agent_set_animation, ":agent_no", "anim_pause_mounted"),
			(val_add,":speed_limit",4),
			(store_random_in_range, reg6, 50, 100),(agent_set_animation_progress, ":agent_no", reg6),
			#(agent_set_animation, reg12, "anim_horse_stand"),
		(else_try),
			(agent_is_human,":agent_no"),
			(agent_set_animation, ":agent_no", "anim_pause"),
			(store_random_in_range, reg6, 90, 100),(agent_set_animation_progress, ":agent_no", reg6),
		(try_end),

		
		(copy_position, pos2, pos1),
		(store_random_in_range,":start_pos",-460,-330),
		(position_move_y, pos2, ":start_pos", 0), # ten steps backward please
		(store_random_in_range,":start_drift",-50,+50),
		(position_move_x, pos2, ":start_drift", 0), 		
		(position_move_y, pos1, 200, 0), # ten steps backward please
		
		# (position_get_x, reg10, pos1),
		# (position_get_y, reg11, pos1),
		# (position_get_x, reg12, pos2),
		# (position_get_y, reg13, pos2),
		 (agent_get_troop_id, reg16,  ":agent_no"), (str_store_troop_name, s3, reg16),
		 #(display_message, "@{reg10},{reg11} to {reg12},{reg13} ({s3})"),
		(try_begin),
			(this_or_next|agent_has_item_equipped, ":agent_no", itm_feet_chains),
			(agent_has_item_equipped, ":agent_no", itm_feet_chains_dwarf),

			(store_random_in_range,":speed_limit",1,2),
			(position_move_y, pos2, -600, 0),
			(position_move_y, pos1, -600, 0), # prisoners, stay back
			
			(agent_set_animation, ":agent_no", "anim_stay_tied"),
		# (display_message, "@Spawn pris: ({s3})"),
			(agent_set_position, ":agent_no", pos2),
			(store_agent_hit_points,":cur_hp",":agent_no",1),
			(agent_set_slot, ":agent_no", slot_agent_last_hp, ":cur_hp"),
			(agent_set_slot, ":agent_no", slot_agent_troll_swing_status, 0),
			(agent_set_animation_progress, ":agent_no", 20),
			(agent_set_team, ":agent_no", 3),
		(else_try),
			(agent_set_team, ":agent_no", 2),
			(agent_set_position, ":agent_no", pos2),
			(agent_set_scripted_destination, ":agent_no", pos1, 0),
		(try_end),
		(agent_set_speed_limit,":agent_no",":speed_limit"),
		#(agent_set_slot, ":agent_no", 1, 1),
		# (CppCoder) Prevent enemy trolls from spawning. Easiest fix IMO. 
		(try_begin),
			(agent_get_team, ":agent_team", ":agent_no"),
			(neq, ":agent_team", 2),
			(agent_get_troop_id, reg16, ":agent_no"),(troop_get_type, ":race", reg16),(eq, ":race", tf_troll),
			(call_script, "script_remove_agent", ":agent_no"),	
		(try_end),
	 (try_end),
  ]),
  

  (ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1)], []),
  tld_cheer_on_space_when_battle_over_press,tld_cheer_on_space_when_battle_over_release,
  (ti_before_mission_start,0,0,[],[
    (set_battle_advantage, 0),
	(team_set_relation,1,2,1), # player friend with troops
	(team_set_relation,2,3,0), # troops neutrl with pris
	(assign, "$talk_context", tc_troop_review_talk),
	(troop_get_xp, "$inital_player_xp", "trp_player"), 
	]),
  (ti_tab_pressed          , 0, 0, [], [   #(ti_on_leave_area,0,0,[],[]),
	(assign, "$talk_context", 0),
	(call_script, "script_count_mission_casualties_from_agents"),

	# (CppCoder) Remove killed trolls (maybe others) from killed party.
	(party_get_num_companion_stacks, ":num_stacks", "p_enemy_casualties"),
	(try_for_range, ":index", 0, ":num_stacks"),
        	(party_stack_get_troop_id, ":stack_troop",  "p_enemy_casualties", ":index"),
		(troop_get_type, ":race", ":stack_troop"),
		(eq, ":race", tf_troll),
		(party_stack_get_size, ":stack_size","p_enemy_casualties",":index"),
		(party_remove_members, "p_enemy_casualties", ":stack_troop", ":stack_size"),
	(try_end),

	(party_get_num_companions, reg20, "p_enemy_casualties"),

	#(display_message, "@(killed {reg20} prisoners)!"),
	(try_begin),
		(gt, reg20, 0),
		
		(call_script, "script_party_remove_party_from_prisoners", "p_main_party", "p_enemy_casualties"), # remove prisoners
		
		(try_begin), # add as many human meat pieces as number of removed prisoners
			(neg|faction_slot_eq, "$players_kingdom", slot_faction_side, faction_side_good), # unless good

      #Butcher trait gets 1.2x more human meat - Kham

      (try_begin),
        (troop_slot_eq, "trp_traits", slot_trait_butcher, 1),
        (try_begin),
          (le, reg0, 0),
          (assign, reg0,1),
        (try_end),
        (val_mul, reg0, 10),
        (val_div, reg0, 8),
        
      #Butcher mod ends

      (try_end),
			(try_for_range, ":unused", 0, reg0), 
				(troop_add_item,"trp_player", "itm_human_meat",imod_fresh),
			(try_end),
		(try_end),

    (try_begin),
      (lt, "$butcher_trait_kills",35),
      (val_add, "$butcher_trait_kills", reg0),
    (else_try),
      (ge, "$butcher_trait_kills", 35),
      (call_script, "script_cf_gain_trait_butcher"),
    (try_end),
		
		# remove undue XP gained from killing pris...
		(troop_get_xp, ":xp", "trp_player"), 
		(gt,":xp","$inital_player_xp"),
		(store_sub,":diff","$inital_player_xp",":xp"),
		(add_xp_to_troop, ":diff","trp_player"), # diff is neg: removes XP 
		(store_mul, reg10,":diff", -1),
		(display_message, "@(cancelled the {reg10} exp pts earned from killing prisoners)"),
	(try_end),
	(reset_visitors),
	(set_trigger_result,1),
  ]),

  (0,0,0,[(game_key_clicked,gk_attack)], [	(team_set_relation,1,3,-1) ]), # payer pressed attack: he can now hit/kill pris! 
  #(0,0,0,[(game_key_clicked,gk_action)], [	(team_set_relation,1,3,0) ]), # player pressed talk
  (2,2,2,[(neg|game_key_is_down,gk_attack)], [	(neg|game_key_is_down,gk_attack),(team_set_relation,1,3,0) ]), # player wasn't aggressive for 2 secs: he can  now talk to pris!
	
  # keep them tied...
  (0,0.5,0,[],[
	(try_for_agents,":agent_no"),
		(this_or_next|agent_has_item_equipped, ":agent_no", itm_feet_chains),
		(agent_has_item_equipped, ":agent_no", itm_feet_chains_dwarf),
		(agent_get_slot, reg10,      ":agent_no", slot_agent_troll_swing_status), 
		(agent_get_slot, ":last_hp", ":agent_no", slot_agent_last_hp), 
		(store_agent_hit_points,":cur_hp",":agent_no",1),
		(agent_set_slot, ":agent_no", slot_agent_last_hp, ":cur_hp"),
		(try_begin),
			(store_mod, reg11, reg10, 10),(this_or_next|eq, reg11, 0), # one turn every 10...
			(neq,":cur_hp",":last_hp"),
			(try_begin),
				(neq,":cur_hp",":last_hp"), # hit: fall
				(agent_set_animation, ":agent_no", "anim_fall_tied"),
				(assign, reg10, 6),
			(else_try),
				(eq,reg10,0), # first time: walk
				(agent_set_animation, ":agent_no", "anim_walk_tied"),
			(else_try),
				(agent_set_animation, ":agent_no", "anim_stay_tied"),
			(try_end),
		(try_end),
		(val_add, reg10, 1),
		(agent_set_slot, ":agent_no", slot_agent_troll_swing_status, reg10),
		(agent_set_slot, ":agent_no", slot_agent_last_hp, ":cur_hp"),
	(try_end),
	]),
  (0,0,ti_once,[],[
	# spawn all party
	(set_battle_advantage, 0),
	#(add_reinforcements_to_entry,3,30),
	
	#(display_message, "@Your troops are behind you"),
	
	# spawn prisoners...
	(assign, ":p", "p_main_party"),
	(party_get_num_prisoner_stacks, ":n",":p"),
	(assign, ":max_pris", 10),
	(store_current_scene, ":cur_scene"),
	(modify_visitors_at_site, ":cur_scene"), 
	(reset_visitors),
	(try_for_range, ":i",0,":n"),
	  (party_prisoner_stack_get_troop_id,   ":trp_id",":p",":i" ),
	  (party_prisoner_stack_get_size, ":trp_no",":p",":i" ),
	  (val_min, ":trp_no", ":max_pris"),
	  (store_add, ":entry", ":i", 4),
	  (troop_get_type, ":race", ":trp_id"),
	  (try_begin), (eq, ":race", tf_dwarf),(val_add, ":entry", 10), (try_end), # dwarf must be born with their chains
	  #(try_begin), (eq, ":race", tf_troll),(val_add, ":entry", 20), (try_end), # trolls must be born in the right spot
	  (add_visitors_to_current_scene,":entry",":trp_id",":trp_no"),
	  (val_sub,":max_pris",":trp_no"), 
	  #(str_store_troop_name, s3, ":trp_id"),(assign, reg3,":trp_no"),(display_message,"@debug: spawning {reg3} {s3} as prisoners"),
	(try_end),
  ],),
  (0,6,ti_once,[],[  # after X secs, cancel all scripted destinations
	(try_for_agents,":i"),
	(agent_clear_scripted_mode, ":i"),
	(try_end),
  ],),

  ],
),

( "lead_charge",mtf_battle_mode,charge,
  "You lead your men to battle.",
	[(1,mtef_defenders|mtef_team_0,0,aif_start_alarmed,18,[]),(0,mtef_defenders|mtef_team_0,0,aif_start_alarmed,0,[]),
     (4,mtef_attackers|mtef_team_1,0,aif_start_alarmed,18,[]),(4,mtef_attackers|mtef_team_1,0,aif_start_alarmed,0,[]),
     (5,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 5th entry, for WARGS
     (6,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 6th entry, for WARGS
     (7,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 7th entry, for WARGS
     (8,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 8th entry, for WARGS
    ],
    tld_common_wb_muddy_water +
    formations_triggers + AI_triggers +   common_deathcam_triggers + moto_formations_triggers +  tld_common_battle_scripts + command_cursor_sub_mod + [
	common_battle_tab_press,
	common_music_situation_update,
	(0,0,ti_once,[],[]),
	common_battle_check_friendly_kills,
	common_battle_check_victory_condition,
	common_battle_victory_display,
	common_battle_on_player_down,
	common_battle_inventory,
	(ti_question_answered, 0, 0, [],[
			(store_trigger_param_1,":answer"),
			(eq,":answer",0),
			(assign, "$pin_player_fallen", 0),
			(try_begin),
				(store_mission_timer_a, ":elapsed_time"),
				(gt, ":elapsed_time", 20),
				(str_store_string, s5, "str_retreat"),
				(call_script, "script_simulate_retreat", 10, 20),
			(try_end),
			(call_script, "script_count_mission_casualties_from_agents"),
			(finish_mission,0)]),
	(ti_before_mission_start, 0, 0, [],[(team_set_relation, 0, 2, 1),(team_set_relation, 1, 3, 1),(call_script, "script_place_player_banner_near_inventory_bms")]),
	(0,0,ti_once,[],[
			(assign,"$battle_won",0),
			(assign,"$defender_reinforcement_stage",0),
			(assign,"$attacker_reinforcement_stage",0),
			(assign,"$g_presentation_battle_active", 0),
			(call_script, "script_place_player_banner_near_inventory"),
			(call_script, "script_combat_music_set_situation_with_culture"),
			# ambience sounds
			(try_begin),(is_currently_night),(play_sound, "$bs_night_sound", sf_looping),
			 (else_try),					 (play_sound, "$bs_day_sound",   sf_looping),
			(try_end),
			(get_player_agent_no, "$current_player_agent"),
			(agent_get_horse,"$horse_player","$current_player_agent"), #checks for horse lameness in mission
			(troop_get_inventory_slot_modifier,"$horse_mod","trp_player",8),
			]),
	(1, 0, 5,  [
			(lt,"$defender_reinforcement_stage",8),
			(store_mission_timer_a,":mission_time"),
			(ge,":mission_time",10),
			(store_normalized_team_count,":num_defenders", 0),
			(lt,":num_defenders",10)
			],[
			(add_reinforcements_to_entry,0,10),
			(val_add,"$defender_reinforcement_stage",1)]),
	(1, 0, 5, [
			(lt,"$attacker_reinforcement_stage",8),
			(store_mission_timer_a,":mission_time"),
			(ge,":mission_time",10),
			(store_normalized_team_count,":num_attackers", 1),
			(lt,":num_attackers",10)
			],[
			(add_reinforcements_to_entry,3,10),
			(val_add,"$attacker_reinforcement_stage",1)]),
  (6, 0 , ti_once, [
      (eq, "$tld_option_formations", 1),
      (le, "$formations_tutorial", 2)],
      [
      ] + (is_a_wb_mt==1 and [
      (tutorial_message_set_background, 1), 
      ] or []) + [
      (try_begin),
        (eq, "$formations_tutorial", 0),
        (tutorial_message, "@In The Last Days of the Third Age, your troops will position themselves and hold at the beginning of each battle, instead of blindly charging.^^To order your troops into formation, press 'J' for Ranks, 'K' for Shield-Wall, 'L' for Wedge, ';' for Square. To undo the formation, press 'U'. ^If your troops are fleeing, you can press 'V' to rally them. You get only a limited amount of rallies per battle, and the amount depends on your leadership and charisma.", 0 , 15),
       (else_try),
        (eq, "$formations_tutorial", 1),
        (tutorial_message, "@You can also order your troops to cycle through the type of weapon you want them to use.^^ Press O to cycle between Weapon Order types. Press P to cycle between Shield Order types.", 0 , 10),
       (else_try),
        (tutorial_message, "@The Last Days of the Third Age has implemented a Custom Camera in order to bypass the current camera limitation with regards to shorter races (e.g Orcs and Dwarves).^^Press CTRL + END to cycle through the 2 camera modes: Fixed Position and Free-Mode.^^Fixed position is the optimal position for all races, however it cannot be configured. You can press CTRL+Left/Right Arrow Keys to switch shoulders.^^Free-Mode Camera puts the character in the middle of the screen. You can press CTRL+Up/Down arrow keys to tilt the camera and CTRL+ Numpad +/- to zoom.^^See Info Pages for how to control the different camera modes.", 0 , 15),
      (try_end),
      (val_add, "$formations_tutorial", 1),
      ]),
	#AI Triggers
	(0, 0, ti_once,[(this_or_next|eq, "$small_scene_used", 1), (eq, "$tld_option_formations", 0),(neq, "$tld_option_formations", 2),(store_mission_timer_a,":mission_time"),(ge,":mission_time",2)],[
			(call_script, "script_select_battle_tactic"),
			(call_script, "script_battle_tactic_init"),
      (try_begin),
        (eq, "$small_scene_used", 1),
        (neq, "$tld_option_formations", 2),
        (display_message, "@Battlefield is too small for complex AI formations.", message_neutral),
      (try_end)]),
	(5, 0, 0, [(this_or_next|eq, "$small_scene_used", 1), (eq, "$tld_option_formations", 0),(neq, "$tld_option_formations", 2),(store_mission_timer_a,":mission_time"),(ge,":mission_time",3),(call_script, "script_battle_tactic_apply")], []),
	common_battle_order_panel,
	common_battle_order_panel_tick,
]),

( "bandits_at_night",0,-1,
  "Default town visit",
    [(0,mtef_scene_source|mtef_team_2, af_override_horse, 0, 1,[]), #MV: player set to team 2
     (1,mtef_scene_source|mtef_team_2, af_override_horse, 0, 1,[]), #(CppCoder): this and next entry fixes bugs somehow. :)
     (2,mtef_scene_source|mtef_team_2, af_override_horse, 0, 1,[]),
     (3,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_visitor_source|mtef_team_0,af_override_horse, aif_start_alarmed, 1, []),
     (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     
     (8,mtef_visitor_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_visitor_source,0,0,1,[]),(14,mtef_visitor_source,0,0,1,[]),(15,mtef_visitor_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),(25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(28,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     (32,mtef_visitor_source,af_override_horse,0,1,[]),(33,mtef_visitor_source,af_override_horse,0,1,[]),(34,mtef_visitor_source,af_override_horse,0,1,[]),(35,mtef_visitor_source,af_override_horse,0,1,[]),(36,mtef_visitor_source,af_override_horse,0,1,[]),(37,mtef_visitor_source,af_override_horse,0,1,[]),(38,mtef_visitor_source,af_override_horse,0,1,[]),(39,mtef_visitor_source,af_override_horse,0,1,[]),
     (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
     tld_common_wb_muddy_water +
    [ (ti_on_agent_spawn,0,0,[],[(store_trigger_param_1, ":agent_no"),
								(agent_get_troop_id, ":troop_no", ":agent_no"),
								(neq, ":troop_no", "trp_player"),
								(agent_set_team, ":agent_no", 1)]),
      (ti_before_mission_start, 0, 0,[],[(team_set_relation, 1, 0, 0),(team_set_relation, 2, 0, 0),  #MV: both player and bandits neutral to guards
        #remove cabbage guard spawn points
        (replace_scene_props, "spr_troop_prison_guard", "spr_empty"),
        (replace_scene_props, "spr_troop_castle_guard", "spr_empty"),
        (replace_scene_props, "spr_troop_guard", "spr_empty"),
		(replace_scene_props, "spr_troop_guard_sitting", "spr_empty"), # (CppCoder) These are what cause the "unable to finish" bugs.
		(replace_scene_props, "spr_troop_human_prisoner", "spr_empty"),
	
		(replace_scene_props, "spr_troop_civilian", "spr_empty"), #InVain: Added new troop spawn props
		(replace_scene_props, "spr_troop_civilian_sitting_ground", "spr_empty"),
		(replace_scene_props, "spr_troop_civilian_sitting_chair", "spr_empty"),	
      ]),
      common_inventory_not_available,
      (ti_tab_pressed  , 0, 0,[(display_message, "@Cannot leave now.")], []),
      (ti_on_leave_area, 0, 0,[(try_begin),(eq, "$g_defending_against_siege", 0),(assign,"$g_leave_town",1),(try_end)], []),
      (0, 0, ti_once,[],[(call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),(set_party_battle_mode)]),
      (1,4,ti_once,[(store_mission_timer_a,":cur_time"),
					(ge, ":cur_time", 5),
					(this_or_next|main_hero_fallen),
					(num_active_teams_le, 1) #MV: was 2
					],
       [ (try_begin),
           (main_hero_fallen),
           (jump_to_menu, "mnu_town_bandits_failed"),
         (else_try),
           (jump_to_menu, "mnu_town_bandits_succeeded"),
         (try_end),
         (finish_mission)]),
]),
( "town_brawl",0,-1,
  "Town brawl with walkers",
    [(0,mtef_scene_source|mtef_team_1, af_override_horse|af_override_weapons, aif_start_alarmed, 1, [itm_wood_club]), #MV: player set to team 1 (guards are enemies)
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_visitor_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     
     (8,mtef_scene_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_scene_source,0,0,1,[]),(14,mtef_scene_source,0,0,1,[]),(15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),(25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(28,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     #walkers: some friends, some enemies
     (32,mtef_visitor_source|mtef_team_2,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (33,mtef_visitor_source|mtef_team_2,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (34,mtef_visitor_source|mtef_team_2,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (35,mtef_visitor_source|mtef_team_2,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (36,mtef_visitor_source|mtef_team_1,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (37,mtef_visitor_source|mtef_team_1,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (38,mtef_visitor_source|mtef_team_1,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     (39,mtef_visitor_source|mtef_team_1,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     #(40,mtef_visitor_source|mtef_team_1,af_override_horse|af_override_weapons,aif_start_alarmed,1,[itm_wood_club]),
     ],
     tld_common_wb_muddy_water +
     tld_common_battle_scripts + [
	(ti_before_mission_start, 0, 0, [], [
			(call_script, "script_change_banners_and_chest"),
			(mission_disable_talk),
			#remove some cabbage guard spawn points, so castle and prison guards don't spawn
			(replace_scene_props, "spr_troop_prison_guard", "spr_empty"),
			(replace_scene_props, "spr_troop_castle_guard", "spr_empty"),
			# remove all other guards except the first five - doesn't work!
			# (init_position, pos1),
			# (position_move_z, pos1, -1000000),
			# (scene_prop_get_num_instances, ":num_guards", "spr_troop_guard"),
			# (try_for_range, ":count", 5, ":num_guards"),
			  # (scene_prop_get_instance, ":guard_instance", "spr_troop_guard", ":count"),
			  # (prop_instance_set_position, ":guard_instance", pos1), #does this work?? how do you remove a single prop? (GA: you can't)
			# (try_end),
			]),
	common_inventory_not_available,
	(ti_tab_pressed  , 0, 0,[(display_message, "@Cannot leave now.")], []),
	(ti_on_leave_area, 0, 0,[(try_begin),(eq, "$g_defending_against_siege", 0),(assign,"$g_leave_town",1),(try_end)], []),
	(0, 0, ti_once, [],[(call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),(set_party_battle_mode)]),
	(1,4,ti_once,[
			(store_mission_timer_a,":cur_time"),
			(ge, ":cur_time", 5),
			(this_or_next|main_hero_fallen),
			(num_active_teams_le, 1)
			],[
			(try_begin),(main_hero_fallen),(jump_to_menu, "mnu_town_brawl_lost"),
			 (else_try),                   (jump_to_menu, "mnu_town_brawl_won"),
			(try_end),
			(finish_mission)]),
]),
( "fangorn_battle",0,-1, # battle against random ents (mtarini)
    "You lead your men to battle Ents!",
    [	
	(0,mtef_defenders|mtef_team_0,0,0,0,[]),
	(1,mtef_defenders|mtef_team_0,0,0,0,[]),

	(4,mtef_attackers|mtef_team_1,0,0,1,[]), 
	(4,mtef_attackers|mtef_team_1,0,0,12,[]), # troops

     	(4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,0,[]),
     	(4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,0,[]),
     	(4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,0,[]),
    ],
  tld_common_wb_muddy_water +
	tld_common_battle_scripts + [   
	
	# (CppCoder) Fixes fangorn retreat bug.
	(ti_tab_pressed, 0, 0, [],
	[
		(try_begin),
			(eq, "$battle_won", 1),
			(call_script, "script_count_mission_casualties_from_agents"),
			(finish_mission,0),
		(else_try), #MV added this section
			(main_hero_fallen),
			(assign, "$pin_player_fallen", 1),
			(str_store_string, s5, "str_retreat"),
			(call_script, "script_simulate_retreat", 10, 20),
			(assign, "$g_battle_result", -1),
			(set_mission_result,-1),
			(call_script, "script_count_mission_casualties_from_agents"),
			(finish_mission,0),
		(else_try),
			(display_message, "@Cannot leave now."),
		(try_end),
	]),

	common_inventory_not_available, 
	common_music_situation_update,
	common_battle_check_friendly_kills,
	common_battle_check_victory_condition,
	common_battle_victory_display,
	common_battle_order_panel,
	common_battle_order_panel_tick,

	#  make ent spawn at random
	(ti_on_agent_spawn, 0, 0, [],
	[
     		(store_trigger_param_1, ":agent"),
	 	(agent_get_troop_id, ":trp", ":agent"), 

	 	(eq, ":trp", "trp_ent"), # a ent is spawned!
	 	(mission_cam_get_position, pos11), 
	 	# spawn it at random pos
	 	(try_for_range, ":unused", 0, 50),
	     		(call_script, "script_store_random_scene_position_in_pos10" ),
		 	(position_is_behind_position, pos10, pos11), # ent appear always out of view >:-)
		 	(assign, ":unused", 50), # ends for loop
	 	(end_try),
		(agent_set_position, ":agent", pos10),
	]),

	# initial conditions: 1 or 2 ents
	(0, 0, ti_once,[],[
			(assign,"$battle_won",0),
			(assign,"$defender_reinforcement_stage",0),
			(assign,"$attacker_reinforcement_stage",0),
			(assign,"$g_presentation_battle_active", 0),
			
			# start with 1 or 2 ents
			(store_current_scene, ":cur_scene"),
			(modify_visitors_at_site, ":cur_scene"), 
			(reset_visitors),
			#(set_visitor,0,"trp_player"),
			
			(store_random_in_range,":n_ents",-1,3),(val_max,":n_ents",1), #  2 ents once in four
			(add_visitors_to_current_scene,4,"trp_ent",":n_ents"), # add the (1 or 2) ent(s) to start with
			#(call_script, "script_place_player_banner_near_inventory"),
			(call_script, "script_combat_music_set_situation_with_culture"),
			(display_message, "@You have a clear perception of great imminent danger, from all around you!",color_bad_news),
			
			]),
	(ti_before_mission_start, 0, 0, [],
			[(team_set_relation, 1, 0, -1),
			(team_set_relation, 1, 2, -1)]),
	# add new ents from time to time
	(30,0,0, [], [
			(store_random_in_range,":d100",1,101),
			(lt,":d100", 10), #  5% of the times...
			(this_or_next|lt,":d100",8), # 8%: every 35 secs an ent appears anyway
			(gt,"$g_fangorn_rope_pulled",10), # or an ent appears at cost of 10 points of 
			(val_sub,"$g_fangorn_rope_pulled",10),
			(val_max,"$g_fangorn_rope_pulled",0),
			#(store_random_in_range,":entry_point",2,5),
			(add_visitors_to_current_scene, 4, "trp_ent", 1),
			(display_message, "@New ent reached battle scene...")]),
	(1, 4, ti_once, [(main_hero_fallen)],[
			(assign, "$pin_player_fallen", 1),
			(str_store_string, s5, "str_retreat"),
			(call_script, "script_simulate_retreat", 10, 20),
			(assign, "$g_battle_result", -1),
			(set_mission_result,-1),
			(call_script, "script_count_mission_casualties_from_agents"),
			(finish_mission,0)]),
	#common_battle_inventory,
]),
( "assasins_attack",mtf_battle_mode,-1,#TLD - assasins attack begin (Kolba)
  "assasins",
	[(0,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),
	 (1,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	],
  tld_common_wb_muddy_water + 
	tld_common_battle_scripts + [
	common_music_situation_update,
	common_battle_check_friendly_kills,
	common_battle_victory_display,
	common_battle_inventory,
	(ti_before_mission_start,0,0,[],[(call_script, "script_remove_siege_objects")]),	
	#if we are going to escape
	(ti_question_answered,0,0,[],[
			(store_trigger_param_1,":answer"),
			(eq,":answer",0),
			(assign,"$g_battle_result",-1),
			(jump_to_menu,"mnu_assasins_attack_player_retreat"),#jump to retreat menu
			(finish_mission,0)]),

	#if player dies
	(1,4,ti_once,[(main_hero_fallen)],[
			(assign,"$pin_player_fallen",1),
			(assign,"$g_battle_result",-1),
			(set_mission_result,-1),
			(jump_to_menu,"mnu_assasins_attack_player_defeated"),#jump to defeat menu
			(finish_mission,0)]),
		
	(ti_tab_pressed,0,0,[],[
			(try_begin),#If the battle is won, missions ends.
				(eq,"$battle_won",1),
				(jump_to_menu,"mnu_assasins_attack_player_won"),#jump to menu, where player gets message and prize
				(finish_mission,0),
			(else_try),#check if there are enemies nearby
				(call_script, "script_cf_check_enemies_nearby"),
				(question_box,"str_do_you_want_to_retreat"),
			(try_end)]),
	#Victory conditions
	#checking victory conditions (here it's set to 60 secunds)
	(1,60,ti_once,[
			(store_mission_timer_a,reg1),
			(ge,reg1,10),
			(all_enemies_defeated,5),
			(neg|main_hero_fallen,0)],[
			#if enemies are defeated and player survives, we continue
			(set_mission_result,1),
			(display_message,"str_msg_battle_won"),
			(assign,"$battle_won",1),
			(assign,"$g_battle_result",1),
			(call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
			(jump_to_menu,"mnu_assasins_attack_player_won"),#jump to menu, where player gets message and prize
			(finish_mission,1)]),
]),

( "tld_caravan_help",mtf_battle_mode,-1,#TLD - starting quest to help/kill caravan (GA) - Modified and hooked up by Kham
  "You rush to towards caravan.",
    [ (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
   tld_common_wb_muddy_water +
   tld_common_battle_scripts + [
  (1, 60, ti_once, 
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 1),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
  ],
  [
    (finish_mission, 1),
  ]),
  
  common_inventory_not_available, 
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,

  (ti_tab_pressed,0,0,[],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (faction_slot_eq,"$players_kingdom",slot_faction_side,faction_side_good),
      (jump_to_menu, "mnu_starting_quest_victory_good"),
      (display_message, "@battle won triggered - Good"),
      (finish_mission),
    (else_try),
      (eq, "$battle_won", 1),
      (jump_to_menu, "mnu_starting_quest_victory_evil"),
      (display_message, "@battle won triggered - Evil"),
      (finish_mission),
    (else_try), 
      (main_hero_fallen),
      (jump_to_menu, "mnu_recover_after_death_default"),
      (finish_mission),
    (try_end),
  ]),
]),


( "tld_start_quest_ambush",mtf_battle_mode,-1,#TLD - starting quest to ambush orcs in forest
  "You ambush the orcs.",
    [ (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
   tld_common_wb_muddy_water +
   tld_common_battle_scripts + [
  (1, 60, ti_once, 
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 1),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
  ],
  [
    (finish_mission, 1),
  ]),
  
  common_inventory_not_available, 
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,

  (ti_tab_pressed,0,0,[],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (faction_slot_eq,"$players_kingdom",slot_faction_side,faction_side_good),
      (jump_to_menu, "mnu_starting_quest_victory_elves"),
      (display_message, "@battle won triggered - Good"),
      (finish_mission),
    (else_try), 
      (main_hero_fallen),
      (jump_to_menu, "mnu_recover_after_death_default"),
      (finish_mission),
    (try_end),
  ]),
]),

( "tld_start_quest_scouts",mtf_battle_mode,-1,#TLD - starting quest to kill all scouts (Easterlings)
  "You rush towards the scouts.",
    [ (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
   tld_common_wb_muddy_water +
   tld_common_battle_scripts + [
  (1, 60, ti_once, 
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 1),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
  ],
  [
    (finish_mission, 1),
  ]),
  
  common_inventory_not_available, 
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,

  (ti_tab_pressed,0,0,[],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (this_or_next|eq,"$players_kingdom", fac_harad),
      (             eq,"$players_kingdom", fac_khand),
      (jump_to_menu, "mnu_starting_quest_victory_easterlings"),
     # (display_message, "@battle won triggered - Easterlings"),
      (finish_mission),
    (else_try), 
      (main_hero_fallen),
      (jump_to_menu, "mnu_recover_after_death_default"),
      (finish_mission),
    (try_end),
  ]),
]),

### Kham Start Quest Evil Duel - begin
( "start_quest_duel",mtf_team_fight, -1, # used for start quest duel
  "You enter a melee fight.",
    [ (0, mtef_visitor_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
    (1, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
    (2, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(3, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(4, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(5, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []), #spectators
    (6, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(7, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(8, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(9, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
    (10,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(11,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(12,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(13,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
    (14,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(15,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(16,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(17,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
    (18,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(19,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(20,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(21,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
    (22,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(23,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(24,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(25,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
    (26,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(27,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(28,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(29,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
    ],tld_common_wb_muddy_water+[
  common_inventory_not_available,
# (ti_tab_pressed, 0, 0, [(display_message, "@Cannot leave now.")], []),
      
  (ti_tab_pressed,0,0,[],[
    (try_begin),#If the battle is won, missions ends.
      (num_active_teams_le,2),
      (neg|main_hero_fallen, 0),
      (finish_mission),
    (else_try),
      (main_hero_fallen),
      (assign, "$g_battle_result", -1),
      (finish_mission),
    (else_try),
      (display_message, "@Cannot leave now."),
    (try_end)]),
      
  (ti_before_mission_start, 0, 0, [],[(team_set_relation, 0, 1, -1),(team_set_relation, 0, 2, 0),(team_set_relation, 1, 2, 0)]),
  (0, 0, ti_once, [],[(call_script, "script_music_set_situation_with_culture", mtf_sit_arena)]),

    (0.3, 0, 0, [], [ # spectators cheer
    (try_for_agents,":agent"),
      (agent_get_entry_no,reg1,":agent"),(neq,reg1,0),(neq,reg1,1), # main guys do not cheer
      (agent_get_slot,":counter",":agent",slot_agent_is_in_scripted_mode),
      (try_begin),
        (gt, ":counter", 0), (val_sub,":counter", 1),(agent_set_slot,":agent",slot_agent_is_in_scripted_mode,":counter"), # pass cheering cycles
      (else_try),
        (store_random_in_range,reg1,0,100),(lt,reg1,10), # 10% of times
        (agent_set_slot,":agent",slot_agent_is_in_scripted_mode,13), # remember that the guy is cheering now, pass 13 cycles after that
        (agent_set_animation, ":agent", "anim_cheer"),
        (agent_get_troop_id,":troop", ":agent"),
        (troop_get_type,reg1,":troop"),
        (try_begin),(is_between, reg1, tf_urukhai, tf_orc_end),(agent_play_sound, ":agent", "snd_uruk_yell"),
         (else_try),(eq, reg1, tf_orc),(agent_play_sound, ":agent", "snd_orc_cheer"),
         (else_try),(agent_play_sound, ":agent", "snd_man_yell"),
        (try_end),
      (try_end),
    (try_end)]),

    tld_cheer_on_space_when_battle_over_press,tld_cheer_on_space_when_battle_over_release,

  (1, 60, 1,[(store_mission_timer_a,reg1),(ge,reg1,10)],[
    (try_begin),
      (main_hero_fallen),
      (assign, "$g_battle_result", -1),
      (jump_to_menu, "mnu_recover_after_death_default"),
      (finish_mission),
    (else_try),
      (num_active_teams_le,2),
      (display_message,"str_msg_battle_won"),
      (jump_to_menu, "mnu_start_quest_duel_won"),
      (finish_mission),
    (try_end)]),
  
]),

### Kham Start Quest Duel End


### Kham - Ring Hunters - Start
 (	"bandit_lair",mtf_battle_mode|mtf_synch_inventory,charge,
    "Ambushing a bandit lair",
    [
    
    #Player
      (0,mtef_team_0|mtef_use_exact_number,af_override_horse, aif_start_alarmed, 8,[]),

    #Enemies
      (1,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,2,[]),
      (2,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,2,[]),
      (3,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,2,[]),
      (4,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,2,[]),
      (5,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,2,[]),
      (6,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,2,[]),
      (7,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,2,[]),
      (8,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,2,[]),
      (9,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,2,[]),
      (10,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,2,[]),
 	],
	
   # Triggers
  tld_common_wb_muddy_water+
  tld_common_battle_scripts+
  common_deathcam_triggers +
  moto_formations_triggers +  [
  

  common_battle_on_player_down,

  # Make the teams enemies...
  (ti_before_mission_start, 0, 0, [], [(team_set_relation, 0, 1, -1),(assign, "$battle_won", 0)]),

  (0, 0, ti_once, 
  [
    #(str_store_troop_name, s1, reg20),
    #(display_message, "@DEBUG: Enemy to spawn: {s1}"),
    #(display_message, "@DEBUG: Enemies to spawn: {reg21}"),

    # Make enemies charge...
    (set_show_messages, 0),
      (team_give_order, 1, grc_everyone, mordr_charge),
    (set_show_messages, 1),
  ], 
  []),

  (1, 60, ti_once, 
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 5),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
  ],
  [
    (finish_mission, 1)
  ]),

   (ti_tab_pressed,0,0,[],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (jump_to_menu, "mnu_ring_hunter_lair_destroyed"),
      (finish_mission),
    (else_try),
      (main_hero_fallen),
      (jump_to_menu, "mnu_recover_after_death_default"),
      (call_script,"script_fail_quest","qst_ring_hunters"),
      (faction_get_slot,":loss","fac_beorn",slot_faction_strength_tmp),
      (val_sub, ":loss", 50),
      (display_message,"@You receive word that Beorning villages were attacked. Beornings lose faction strength",color_bad_news),
      (faction_get_slot,":evil","fac_mordor",slot_faction_strength_tmp),
      (val_add, ":evil", 30),
      (display_message,"@You receive word that the Ring Hunter Leaders were seen travelling towards Mordor, a chest in tow. Mordor gains faction strength.",color_bad_news),
      (faction_set_slot,"fac_beorn",slot_faction_strength_tmp,":loss"),
      (faction_set_slot,"fac_mordor",slot_faction_strength_tmp,":evil"),
      (disable_party,"p_ring_hunter_lair"),
      (call_script, "script_safe_remove_party","$qst_ring_hunter_party"),
      (cancel_quest, "qst_ring_hunters"),
      (finish_mission),
    (try_end),
    # Apply health changes...
    (try_begin),
      (this_or_next|eq, "$battle_won", 1),
      (main_hero_fallen),
      (try_for_agents, ":agent"),
        (gt, ":agent",0),
        (agent_is_human, ":agent"),
        (agent_get_troop_id, ":troop", ":agent"),
        (troop_is_hero, ":troop"),
        (this_or_next|eq, ":troop", "trp_player"),
        (is_between, ":troop", companions_begin, companions_end),
        (store_agent_hit_points,":hp",":agent",0),
        (call_script, "script_get_max_skill_of_player_party", "skl_wound_treatment"),
        (store_mul, ":medic", reg0, 5),
        (val_add, ":hp", ":medic"),
        (val_clamp, ":hp", 0, 100),
        (troop_set_health, ":troop", ":hp"),
      (try_end),
    (try_end),
  ]),

  common_inventory_not_available, 
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,
  common_battle_inventory,      
  common_battle_order_panel,
  common_battle_order_panel_tick,

	
]),

#kham - Ring Hunters - End

### Defend Village MT Start (kham)###

 (
    "village_attack_bandits",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
      # Player
      (0,mtef_team_0|mtef_use_exact_number,0,aif_start_alarmed,14,[]),

      # Companions (Add more for more companions)
      (1,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (8,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[itm_practice_staff]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[itm_practice_staff]),
      (12,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,0,1,[]),
     

      # Enemies:
      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

   ],
  # Triggers
  tld_common_wb_muddy_water+
  tld_common_battle_scripts+
  common_deathcam_triggers +
  moto_formations_triggers + [
  

  common_battle_on_player_down,

  # Make the teams enemies... and disable morale
  (ti_before_mission_start, 0, 0, [], [(team_set_relation, 0, 1, -1),(assign, "$battle_won", 0), (assign, "$tld_option_morale", 0),]),

  (0, 0, ti_once, 
  [

    # Make enemies charge... and disable morale
    (set_show_messages, 0),
      (team_give_order, 1, grc_everyone, mordr_charge),
    (set_show_messages, 1),
  ], 
  []),

  (1, 60, ti_once, 
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 1),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
  ],
  [
    (finish_mission, 1)
  ]),

  (ti_tab_pressed,0,0,[],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (jump_to_menu, "mnu_village_quest_result"),
      (assign, "$tld_option_morale", 1),
      (finish_mission),
    (else_try),
      (main_hero_fallen),
      (jump_to_menu, "mnu_village_quest_result"),
      (assign, "$tld_option_morale", 1),
      (finish_mission),
    (try_end),
    # Apply health changes...
    (try_begin),
      (this_or_next|eq, "$battle_won", 1),
      (main_hero_fallen),
      (try_for_agents, ":agent"),
        (gt, ":agent",0),
        (agent_is_human, ":agent"),
        (agent_get_troop_id, ":troop", ":agent"),
        (troop_is_hero, ":troop"),
        (this_or_next|eq, ":troop", "trp_player"),
        (is_between, ":troop", companions_begin, companions_end),
        (store_agent_hit_points,":hp",":agent",0),
        (call_script, "script_get_max_skill_of_player_party", "skl_wound_treatment"),
        (store_mul, ":medic", reg0, 5),
        (val_add, ":hp", ":medic"),
        (val_clamp, ":hp", 0, 100),
        (troop_set_health, ":troop", ":hp"),
      (try_end),
    (try_end),
  ]),
  
  common_inventory_not_available, 
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,
  common_battle_inventory,      
  common_battle_order_panel,
  common_battle_order_panel_tick,
      
    ],
  ),


### Raid Village MT Start (kham)###

 (
    "village_attack_farmers",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
      # Enemies
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[itm_practice_staff]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
     

      # Player:
      (16,mtef_team_1|mtef_attackers|mtef_use_exact_number,0,aif_start_alarmed,14,[]),
     
      # Companions (Add more for more companions)
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

   ],
  # Triggers
  tld_common_wb_muddy_water+
  tld_common_battle_scripts+
  common_deathcam_triggers +
  moto_formations_triggers +  [
  

  common_battle_on_player_down,

  # Make the teams enemies... and disable morale
  (ti_before_mission_start, 0, 0, [], [(team_set_relation, 1, 0, -1),(assign, "$battle_won", 0), (assign, "$tld_option_morale", 0),]),

  (0, 0, ti_once, 
  [

    # Make enemies charge...
    (set_show_messages, 0),
      (team_give_order, 0, grc_everyone, mordr_charge),
    (set_show_messages, 1),
  ], 
  []),

  (1, 60, ti_once, 
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 0),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
  ],
  [
    (finish_mission, 1)
  ]),

  (ti_tab_pressed,0,0,[],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (jump_to_menu, "mnu_village_quest_result"),
      (assign, "$tld_option_morale", 1),
      (finish_mission),
    (else_try),
      (main_hero_fallen),
      (jump_to_menu, "mnu_village_quest_result"),
      (assign, "$tld_option_morale", 1),
      (finish_mission),
    (try_end),
    # Apply health changes...
    (try_begin),
      (this_or_next|eq, "$battle_won", 1),
      (main_hero_fallen),
      (try_for_agents, ":agent"),
        (gt, ":agent",0),
        (agent_is_human, ":agent"),
        (agent_get_troop_id, ":troop", ":agent"),
        (troop_is_hero, ":troop"),
        (this_or_next|eq, ":troop", "trp_player"),
        (is_between, ":troop", companions_begin, companions_end),
        (store_agent_hit_points,":hp",":agent",0),
        (call_script, "script_get_max_skill_of_player_party", "skl_wound_treatment"),
        (store_mul, ":medic", reg0, 5),
        (val_add, ":hp", ":medic"),
        (val_clamp, ":hp", 0, 100),
        (troop_set_health, ":troop", ":hp"),
      (try_end),
    (try_end),
  ]),
  
  common_inventory_not_available, 
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,
  common_battle_inventory,      
  common_battle_order_panel,
  common_battle_order_panel_tick,
      
    ],
  ),

### Defend / Raid Village MT End (kham)###

### Destroy Scout Camp MT Start (kham)###

 (
    "destroy_scout_camp",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
      # Player
      (0,mtef_team_0|mtef_attackers|mtef_use_exact_number,0,aif_start_alarmed,12,[]),

      # Companions (Add more for more companions)
      (1,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (8,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,0,1,[]),
     

      # Enemies:
      (16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

   ],
  # Triggers
  tld_common_wb_muddy_water+
  tld_common_battle_scripts+
  common_deathcam_triggers +
  moto_formations_triggers +  [
  

  common_battle_on_player_down,

  # Make the teams enemies... and disable morale
  (ti_before_mission_start, 0, 0, [], [(team_set_relation, 0, 1, -1),(assign, "$battle_won", 0), (assign, "$tld_option_morale", 0),]),

  (0, 0, ti_once, 
  [
    #(str_store_troop_name, s1, reg20),
    #(display_message, "@DEBUG: Enemy to spawn: {s1}"),
    #(display_message, "@DEBUG: Enemies to spawn: {reg21}"),

    # Make enemies charge...
    (set_show_messages, 0),
      (team_give_order, 1, grc_everyone, mordr_charge),
    (set_show_messages, 1),
  ], 
  []),

  (1, 60, ti_once, 
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 1),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
  ],
  [
    (finish_mission, 1)
  ]),

  (ti_tab_pressed,0,0,[],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (jump_to_menu, "mnu_destroy_scout_camp_quest_result"),
      (assign, "$tld_option_morale", 1),
      (finish_mission),
    (else_try),
      (main_hero_fallen),
      (jump_to_menu, "mnu_destroy_scout_camp_quest_result"),
      (assign, "$tld_option_morale", 1),
      (finish_mission),
    (try_end),
    # Apply health changes...
    (try_begin),
      (this_or_next|eq, "$battle_won", 1),
      (main_hero_fallen),
      (try_for_agents, ":agent"),
        (gt, ":agent",0),
        (agent_is_human, ":agent"),
        (agent_get_troop_id, ":troop", ":agent"),
        (troop_is_hero, ":troop"),
        (this_or_next|eq, ":troop", "trp_player"),
        (is_between, ":troop", companions_begin, companions_end),
        (store_agent_hit_points,":hp",":agent",0),
        (call_script, "script_get_max_skill_of_player_party", "skl_wound_treatment"),
        (store_mul, ":medic", reg0, 5),
        (val_add, ":hp", ":medic"),
        (val_clamp, ":hp", 0, 100),
        (troop_set_health, ":troop", ":hp"),
      (try_end),
    (try_end),
  ]),
  
  common_inventory_not_available, 
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,
  common_battle_inventory,      
  common_battle_order_panel,
  common_battle_order_panel_tick,
      
    ],
  ),


### Destroy Scout Camp MT End (kham)###

## Amath Dollen Fortress - Talk - MT Start (Kham)

( "amath_dollen_peace",0,-1,
  "You approach the bandit fortress.",
    [(0,mtef_team_0,af_override_horse,0,1,[]),
     (2,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (8,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (9,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (10,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (11,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (12,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (13,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (14,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (15,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (16,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (17,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (18,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (19,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (20,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (21,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (22,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (23,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (24,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (25,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (26,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (27,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (28,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),

     ],
    tld_common_wb_muddy_water +
    tld_common_peacetime_scripts + [
      (ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1)], []),
      (ti_tab_pressed          , 0, 0, [(set_trigger_result,1)], []),
    (0, 0, ti_once, [], [#(set_fog_distance, 150, 0xFF736252)
          (call_script, "script_music_set_situation_with_culture", 0)]),    
]),

## Amath Dollen Fortress MT Start (Kham)###

 (
    "amath_dollen_attack",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
      # Player
      (0,mtef_team_0|mtef_use_exact_number,af_override_horse,aif_start_alarmed,16,[]),

      # Companions (Add more for more companions)
      (1,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (8,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,0,1,[]),
     

      # Enemies:
      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
   ],

  # Triggers
  tld_common_wb_muddy_water+
  tld_common_battle_scripts+
  common_deathcam_triggers +
  moto_formations_triggers +  [
  

  common_battle_on_player_down,

  # Make the teams enemies...
  (ti_before_mission_start, 0, 0, [], [
    (set_rain,1,100),
    (team_set_relation, 0, 1, -1),
    (team_set_relation, 6,1, -1),
    (assign, "$gate_aggravator_agent", -1),
    (assign, "$battle_won", 0)
  ]),

  (0, 0, ti_once, 
  [
    #(str_store_troop_name, s1, reg20),
    #(display_message, "@DEBUG: Enemy to spawn: {s1}"),
    #(display_message, "@DEBUG: Enemies to spawn: {reg21}"),

    # Make enemies charge...
    (set_show_messages, 0),
      (team_give_order, 1, grc_infantry, mordr_charge),
      (team_give_order, 1, grc_archers, mordr_hold),
    (set_show_messages, 1),

    #Fog
    (set_fog_distance, 200, 0xCCCCCC),

      # put gate aggravator in place
    (try_begin),
      (neq, "$gate_aggravator_agent",-1),
      (eq, "$gate_breached",0),
      (entry_point_get_position, pos13, 39),
      (agent_set_scripted_destination,"$gate_aggravator_agent",pos13,1),
      (agent_set_position,"$gate_aggravator_agent",pos13),
      (agent_set_hit_points,"$gate_aggravator_agent",100,0),
    (try_end),
  ], 
  []),

  (1, 60, ti_once, 
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 5),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
  ],
  [
    (finish_mission, 1)
  ]),

  (ti_tab_pressed,0,0,[],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (jump_to_menu, "mnu_village_quest_result"),
      (finish_mission),
    (else_try),
      (main_hero_fallen),
      (jump_to_menu, "mnu_village_quest_result"),
      (finish_mission),
    (try_end),
    # Apply health changes...
    (try_begin),
      (this_or_next|eq, "$battle_won", 1),
      (main_hero_fallen),
      (try_for_agents, ":agent"),
        (gt, ":agent",0),
        (agent_is_human, ":agent"),
        (agent_get_troop_id, ":troop", ":agent"),
        (troop_is_hero, ":troop"),
        (this_or_next|eq, ":troop", "trp_player"),
        (is_between, ":troop", companions_begin, companions_end),
        (store_agent_hit_points,":hp",":agent",0),
        (call_script, "script_get_max_skill_of_player_party", "skl_wound_treatment"),
        (store_mul, ":medic", reg0, 5),
        (val_add, ":hp", ":medic"),
        (val_clamp, ":hp", 0, 100),
        (troop_set_health, ":troop", ":hp"),
      (try_end),
    (try_end),
  ]),

  
  common_inventory_not_available, 
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,
  common_battle_inventory,      
  common_battle_order_panel,
  common_battle_order_panel_tick,
      
    ],
  ),


### Against Siege

(
    "amath_dollen_defend",mtf_battle_mode|mtf_synch_inventory,charge,
    "You defend the fortress.",
    [
      # Player
      (0,mtef_team_0|mtef_attackers,af_override_horse,aif_start_alarmed,1,[]),

      # Companions (Add more for more companions)
      (1,mtef_attackers|mtef_use_exact_number|mtef_infantry_first|mtef_team_0,0,0,2,[]),
      (2,mtef_attackers|mtef_use_exact_number|mtef_infantry_first|mtef_team_0,0,0,2,[]),
      (3,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (4,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (5,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (6,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (7,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (8,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (9,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (10,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (11,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (12,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (13,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (14,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),
      (15,mtef_attackers|mtef_use_exact_number|mtef_archers_first|mtef_team_0,0,0,1,[]),

      # Enemies:
      (16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
   ],

 # Triggers
  # Triggers
  tld_common_wb_muddy_water+
  tld_common_battle_scripts+
  common_deathcam_triggers +
  moto_formations_triggers +  [
  
  common_battle_on_player_down,

  # Make the teams enemies...
  (ti_before_mission_start, 0, 0, [], [(team_set_relation, 0, 1, -1),(assign, "$battle_won", 0)]),

  (0, 0, ti_once, 
  [
    #(str_store_troop_name, s1, reg20),
    #(display_message, "@DEBUG: Enemy to spawn: {s1}"),
    #(display_message, "@DEBUG: Enemies to spawn: {reg21}"),

    # Make enemies charge...
    (set_show_messages, 0),
      (team_give_order, 1, grc_everyone, mordr_charge),
    (set_show_messages, 1),
  ], 
  []),

  (1, 60, ti_once, 
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 5),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
  ],
  [
    (finish_mission, 1)
  ]),

  (ti_tab_pressed,0,0,[],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (jump_to_menu, "mnu_animal_ambush_success"),
      (finish_mission),
    (else_try),
      (main_hero_fallen),
      (jump_to_menu, "mnu_animal_ambush_fail"),
      (finish_mission),
    (try_end),
    # Apply health changes...
    (try_begin),
      (this_or_next|eq, "$battle_won", 1),
      (main_hero_fallen),
      (try_for_agents, ":agent"),
        (gt, ":agent",0),
        (agent_is_human, ":agent"),
        (agent_get_troop_id, ":troop", ":agent"),
        (troop_is_hero, ":troop"),
        (this_or_next|eq, ":troop", "trp_player"),
        (is_between, ":troop", companions_begin, companions_end),
        (store_agent_hit_points,":hp",":agent",0),
        (call_script, "script_get_max_skill_of_player_party", "skl_wound_treatment"),
        (store_mul, ":medic", reg0, 5),
        (val_add, ":hp", ":medic"),
        (val_clamp, ":hp", 0, 100),
        (troop_set_health, ":troop", ":hp"),
      (try_end),
    (try_end),
  ]),


  common_inventory_not_available, 
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,
  common_battle_inventory,      
  common_battle_order_panel,
  common_battle_order_panel_tick,

]),


( "amath_dollen_spirit",0,-1,
  "You approach the hill towards the bandit's ancestors.",
    [(0,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (1,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (2,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (8,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (9,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (10,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (11,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (12,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (13,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (14,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (15,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (16,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (17,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (18,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (19,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (20,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (21,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (22,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (23,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (24,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (25,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (26,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (27,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (28,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (29,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (30,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (31,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (32,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     ],
    tld_common_wb_muddy_water +
    tld_common_peacetime_scripts + [
      (ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1)], []),
      (ti_tab_pressed          , 0, 0, [(set_trigger_result,1)], []),
    (0, 0, ti_once, [], [#(set_fog_distance, 150, 0xFF736252)
          (call_script, "script_music_set_situation_with_culture", 0)]),
    (ti_before_mission_start, 0, 0, [], [(set_rain,1,100)]),
    (0, 0, ti_once,[],[(set_fog_distance, 100, 0x6E6A5D)]),    #0x726438 Yellow; 
]),

## Amath Dollen Fortress MT End - Kham


### Sea Battle MT Start (kham)###

 (
    "sea_battle_quest_good",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
      # Player
	  (0,mtef_team_0|mtef_use_exact_number,0,aif_start_alarmed,0,[]), #just a dummy, so spawn records and entry points are the same.
      (1,mtef_team_0|mtef_use_exact_number,af_override_horse,aif_start_alarmed,10,[]),

      #Good Allies
      (2,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (8,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      
      #Enemies
      (11,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,0,[]), #just a dummy, so spawn records and entry points are the same.
      (12,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),

   ],
  # Triggers
  tld_common_wb_muddy_water+
  common_deathcam_triggers + 
  fade + khams_custom_player_camera + bright_nights + [
  
  tld_slow_wounded,
  custom_tld_spawn_troop, custom_tld_init_battle,
  tld_cheer_on_space_when_battle_over_press, tld_cheer_on_space_when_battle_over_release,
  #cheat_kill_self_on_ctrl_s,
  custom_track_companion_casualties,
  common_battle_healing,
  common_battle_on_player_down,

  # Make the teams enemies...
  (ti_before_mission_start, 0, 0, [], [(team_set_relation, 0, 1, -1),(assign, "$battle_won", 0)]),

  (0, 0, ti_once, 
  [

	(assign,"$enemy_reinforcement_stage",0),
	(assign,"$ally_reinforcement_stage",0),

    # Make enemies charge...
    (set_show_messages, 0),
      (team_give_order, 1, grc_everyone, mordr_charge),
    (set_show_messages, 1),
  ], 
  []),

 (1, 60, ti_once, 
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 1),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
  ],
  [
    (finish_mission, 1)
  ]),

(ti_tab_pressed,0,0,[],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (jump_to_menu, "mnu_sea_battle_quest_results"),
      (finish_mission),
    (else_try),
      (main_hero_fallen),
      (jump_to_menu, "mnu_sea_battle_quest_results"),
      (finish_mission),
    (try_end),
    # Apply health changes...
    (try_begin),
      (this_or_next|eq, "$battle_won", 1),
      (main_hero_fallen),
      (try_for_agents, ":agent"),
        (gt, ":agent",0),
        (agent_is_human, ":agent"),
        (agent_get_troop_id, ":troop", ":agent"),
        (troop_is_hero, ":troop"),
        (this_or_next|eq, ":troop", "trp_player"),
        (is_between, ":troop", companions_begin, companions_end),
        (store_agent_hit_points,":hp",":agent",0),
        (call_script, "script_get_max_skill_of_player_party", "skl_wound_treatment"),
        (store_mul, ":medic", reg0, 5),
        (val_add, ":hp", ":medic"),
        (val_clamp, ":hp", 0, 100),
        (troop_set_health, ":troop", ":hp"),
      (try_end),
      (call_script, "script_count_mission_casualties_from_agents"),
    (try_end),
  ]),


## Reinforcement Triggers - Note  that I am using the interloper code here, because this is a mission, instead of a battle between parties, 
## where there would actually be a pool for reinforcements. Also, because it is a relatively short battle, I put ally + enemy reinforcements instead of player reinforcements.

## Enemy Reinforcement Triggers: 
  (5, 0, 0, [
      (store_mission_timer_b, ":mission_time_b"),
      (store_random_in_range, ":ran_time", 5, 15),
      (ge, ":mission_time_b", ":ran_time"), #Random time between 10 - 20 secs
      (reset_mission_timer_b),
      (lt,"$enemy_reinforcement_stage", 8), #up to 8 reinforcements     
      (val_add, "$enemy_reinforcement_stage", 1), 
      #This checks the faction of the quest giver.
      (quest_get_slot, ":troop", "qst_blank_quest_03", slot_quest_object_center),
      (store_faction_of_party, ":faction", ":troop"),      
      
      #This checks what type of enemy troops to spawn, depending on faction of quest giver (North or South)
      #Once checked, we then spawn the troop we want. For higher level players, they get upgraded.
      (try_begin),
        (eq, ":faction", "fac_gondor"),
        (assign, ":enemy_melee_tier_1", "trp_corsair_marauder"),
        #(troop_get_upgrade_troop, ":enemy_melee_tier_2", "trp_corsair_marauder",0),
        (assign, ":enemy_archer_tier_1", "trp_militia_of_umbar"),
        #(troop_get_upgrade_troop, ":enemy_archer_tier_2", "trp_marksman_of_umbar",0),
      #  (display_message, "@DEBUG: Umbar Troops Spawned", color_bad_news),
      (else_try), #Dale
        (assign, ":enemy_melee_tier_1", "trp_rhun_tribal_warrior"),
        #(troop_get_upgrade_troop, ":enemy_melee_tier_2", "trp_rhun_tribal_warrior",0),
        (assign, ":enemy_archer_tier_1", "trp_rhun_tribal_infantry"),
        #(troop_get_upgrade_troop, ":enemy_archer_tier_2", "trp_rhun_tribal_infantry",0), 
      #  (display_message, "@DEBUG: Rhun Troops Spawned", color_bad_news),
      (try_end),

      # (store_character_level, ":level", "trp_player"),

      # #This is where we check what to spawn depending on player level (Med/High Tier)
      # (try_begin),
        # (ge, ":level", 25),
        # (assign, ":enemy_melee_troop",  ":enemy_melee_tier_1"),
        # (assign, ":enemy_ranged_troop", ":enemy_archer_tier_1"),
      # (else_try),
        (assign, ":enemy_melee_troop",  ":enemy_melee_tier_1"),
        (assign, ":enemy_ranged_troop", ":enemy_archer_tier_1"),
      # (try_end),

	  (store_character_level, ":level", "trp_player"),
	  (store_div, ":num_enemies", ":level", 3), #InVain - scale attacker # to the player's level, easier at the beginning, harder from lvl 24
      (val_min, ":num_enemies", 11),
	  #(assign, ":range_end", 7), #Change this number to change the number of troops spawned
      (assign, ":team_enemy", 1),
      (display_message, "@Enemy reinforcements have arrived", color_bad_news),
      (store_random_in_range, ":rand_speech", 0, 6),
      (try_begin),
        (eq, ":rand_speech", 0),
        (str_store_string, s30, "@Yarrrr!!"),
      (else_try),
        (eq, ":rand_speech", 1),
        (str_store_string, s30, "@Get all of them!"),
      (else_try),
        (eq, ":rand_speech", 2),
        (str_store_string, s30, "@Kill them all!"),
      (else_try),
        (eq, ":rand_speech", 3),
        (str_store_string, s30, "@Toss them overboard!"),
      (else_try),
        (eq, ":rand_speech", 4),
        (str_store_string, s30, "@It is a good day to die!"),
      (else_try),
        (str_store_string, s30, "@All hands on deck! Throw them back!"),
      (try_end),
      (try_begin),
        (lt, ":rand_speech", 3),
        (assign, ":troop_pic", ":enemy_melee_troop"),
      (else_try),
        (assign, ":troop_pic", ":enemy_ranged_troop"),
      (try_end),
      (call_script, "script_troop_talk_presentation", ":troop_pic", 7, 0),

      (store_random_in_range, ":enemy_entry", 12, 21), #This just randomizes the entry points the enemy comes from.
      (entry_point_get_position, pos5, ":enemy_entry"),
      (set_spawn_position, pos5), 
      
      #This spawns the troops, coin flip on whether troops are ranged / melee, as per the above troop assignments.
      (try_for_range, ":unused", 0, ":num_enemies"),
          (store_random_in_range, ":rnd_troop", 0,100),
          (le, ":rnd_troop", 50),
          (spawn_agent, ":enemy_melee_troop"),
          (agent_set_team, reg0, ":team_enemy"),
        (else_try),
          (spawn_agent, ":enemy_ranged_troop"),
          (agent_set_team, reg0, ":team_enemy"),
      (try_end),

      #This asks them to charge, secretly.
      (set_show_messages, 0),
      (team_give_order, ":team_enemy", grc_everyone, mordr_charge),
      (set_show_messages, 1),
 
      ],
    [
      #(display_message, "@DEBUG: Enemy Reinforced!")
    ]
  ),

# Had to separate the triggers because for some reason, it gets buggy if I combined both ally + enemy spawns. See notes above, they are exactly the same, other than this spawns allies.
# Ally Reinforcement Triggers: 
(5, 0, 0, [
      (store_mission_timer_c, ":mission_time_c"),
      (store_random_in_range, ":ran_time", 10, 20),
      (ge, ":mission_time_c", ":ran_time"), #Random time between 25 - 40 secs
      (reset_mission_timer_c),
      (lt,"$ally_reinforcement_stage", 4),      
      (val_add, "$ally_reinforcement_stage", 1),
#      (store_random_in_range, ":chance", 0, 2),
 #     (ge, ":chance", 1), #2 out of 3 times  
      (quest_get_slot, ":troop", "qst_blank_quest_03", slot_quest_object_center),
      (store_faction_of_party, ":faction", ":troop"),      
      
      (try_begin),
        (eq, ":faction", "fac_gondor"),
        (assign, ":allies_melee_tier_1", "trp_pelargir_watchman"),
        #(troop_get_upgrade_troop, ":allies_melee_tier_2", "trp_pelargir_infantry",0), #Commented out - If we want to upgrade allies too.
        (assign, ":allies_archer_tier_1", "trp_pelargir_marine"),
        #(troop_get_upgrade_troop, ":allies_archer_tier_2", "trp_pelargir_marine",0),   #Commented out - If we want to upgrade allies too.
      #  (display_message, "@DEBUG: Gondor Troops Spawned", color_bad_news),
      (else_try), #Dale
        (assign, ":allies_melee_tier_1", "trp_dale_veteran_warrior"),
        #(troop_get_upgrade_troop, ":allies_melee_tier_2", "trp_merchant_guard_of_dale",0), #Commented out - If we want to upgrade allies too.
        (assign, ":allies_archer_tier_1", "trp_laketown_bowmen"),
        #(troop_get_upgrade_troop, ":allies_archer_tier_2", "trp_laketown_bowmen",0),   #Commented out - If we want to upgrade allies too.
      #  (display_message, "@DEBUG: Dale Troops Spawned", color_bad_news),
      (try_end),

      (assign, ":ally_melee_troop",   ":allies_melee_tier_1"),
      (assign, ":ally_ranged_troop",  ":allies_archer_tier_1"),

      (assign, ":num_allies", 6),
      (assign, ":team_ally", 0),
      (display_message, "@Ally reinforcements have arrived", color_good_news),
      (store_random_in_range, ":rand_speech", 0, 6),
      (try_begin),
        (eq, ":rand_speech", 0),
        (str_store_string, s30, "@Forward, men!"),
      (else_try),
        (eq, ":rand_speech", 1),
        (str_store_string, s30, "@Leave none of these filth standing!"),
      (else_try),
        (eq, ":rand_speech", 2),
        (str_store_string, s30, "@End them all!"),
      (else_try),
        (eq, ":rand_speech", 3),
        (str_store_string, s30, "@Drive them back!"),
      (else_try),
        (eq, ":rand_speech", 4),
        (str_store_string, s30, "@Protect the City!"),
      (else_try),
        (str_store_string, s30, "@Forward! Board them!"),
      (try_end),
      (try_begin),
        (lt, ":rand_speech", 3),
        (assign, ":troop_pic", ":ally_melee_troop"),
      (else_try),
        (assign, ":troop_pic", ":ally_ranged_troop"),
      (try_end),
      (call_script, "script_troop_talk_presentation", ":troop_pic", 7, 0),
      (store_random_in_range, ":ally_entry", 2, 11),
      (entry_point_get_position, pos4, ":ally_entry"),
      (set_spawn_position, pos4), 
      (try_for_range, ":unused", 0, ":num_allies"),
          (store_random_in_range, ":rnd_troop", 0,100),
          (le, ":rnd_troop", 50),
          (spawn_agent, ":ally_melee_troop"),
          (agent_set_team, reg0, ":team_ally"),
        (else_try),
          (spawn_agent, ":ally_ranged_troop"),
          (agent_set_team, reg0, ":team_ally"),
      (try_end),

      (set_show_messages, 0),
      (team_give_order, ":team_ally", grc_everyone, mordr_charge),
      (set_show_messages, 1),
      ],
    [
      #(display_message, "@DEBUG: Ally Reinforced!")
    ]
  ),

## End Reinforcement Triggers

(1, 60, ti_once,[
  (store_mission_timer_a,reg(1)),
  (ge,reg(1),10),
  (all_enemies_defeated, 5),
  #(neg|main_hero_fallen, 0), #MV
  (set_mission_result,1),
  (display_message,"str_msg_battle_won"),
  (assign,"$battle_won",1),
  (assign, "$g_battle_result", 1),
  (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
    ],[
  (call_script, "script_count_mission_casualties_from_agents"),
  (jump_to_menu, "mnu_sea_battle_quest_results"),
  (finish_mission, 1),]),
 
  common_inventory_not_available, 
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_victory_display,
  common_battle_inventory,      
  common_battle_order_panel,
  common_battle_order_panel_tick,
      
    ],
  ),

(
    "sea_battle_quest_evil",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
      
	  (0,mtef_team_1|mtef_use_exact_number,0,aif_start_alarmed,0,[]), #just a dummy, so spawn records and entry points are the same.
      (1,mtef_team_1|mtef_use_exact_number,0,aif_start_alarmed,0,[]), #just a dummy, so spawn records and entry points are the same.

      #Good
      (2,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (8,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      
      #Evil
      
      (11,mtef_team_0|mtef_use_exact_number,af_override_horse,aif_start_alarmed,10,[]),
      (12,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (16,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),

   ],
  # Triggers
  tld_common_wb_muddy_water+
  common_deathcam_triggers + 
  fade + khams_custom_player_camera + bright_nights + [
  
  tld_slow_wounded,
  custom_tld_spawn_troop, custom_tld_init_battle,
  tld_cheer_on_space_when_battle_over_press, tld_cheer_on_space_when_battle_over_release,
  #cheat_kill_self_on_ctrl_s,
  custom_track_companion_casualties,
  common_battle_healing,
  common_battle_on_player_down,

  # Make the teams enemies...
  (ti_before_mission_start, 0, 0, [], [(team_set_relation, 0, 1, -1),(assign, "$battle_won", 0)]),

  (0, 0, ti_once, 
  [

  	(assign,"$enemy_reinforcement_stage",0),
	(assign,"$ally_reinforcement_stage",0),
  
    # Make enemies charge...
    (set_show_messages, 0),
      (team_give_order, 1, grc_everyone, mordr_charge),
    (set_show_messages, 1),
  ], 
  []),

  (1, 60, ti_once, 
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 1),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
  ],
  [
    (finish_mission, 1)
  ]),

(ti_tab_pressed,0,0,[],
  [
    (try_begin),
      (eq, "$battle_won", 1),
      (jump_to_menu, "mnu_sea_battle_quest_results"),
      (finish_mission),
    (else_try),
      (main_hero_fallen),
      (jump_to_menu, "mnu_sea_battle_quest_results"),
      (finish_mission),
    (try_end),
    # Apply health changes...
    (try_begin),
      (this_or_next|eq, "$battle_won", 1),
      (main_hero_fallen),
      (try_for_agents, ":agent"),
        (gt, ":agent",0),
        (agent_is_human, ":agent"),
        (agent_get_troop_id, ":troop", ":agent"),
        (troop_is_hero, ":troop"),
        (this_or_next|eq, ":troop", "trp_player"),
        (is_between, ":troop", companions_begin, companions_end),
        (store_agent_hit_points,":hp",":agent",0),
        (call_script, "script_get_max_skill_of_player_party", "skl_wound_treatment"),
        (store_mul, ":medic", reg0, 5),
        (val_add, ":hp", ":medic"),
        (val_clamp, ":hp", 0, 100),
        (troop_set_health, ":troop", ":hp"),
      (try_end),
      (call_script, "script_count_mission_casualties_from_agents"),
    (try_end),
  ]),

## Reinforcement Triggers - Note  that I am using the interloper code here, because this is a mission, instead of a battle between parties, 
## where there would actually be a pool for reinforcements. Also, because it is a relatively short battle, I put ally + enemy reinforcements instead of player reinforcements.

## Ally Reinforcement Triggers: 
  (5, 0, 0, [
      (store_mission_timer_b, ":mission_time_b"),
      (store_random_in_range, ":ran_time", 10, 20),
      (ge, ":mission_time_b", ":ran_time"), #Random time between 25 - 40 secs
      (reset_mission_timer_b),
      (lt,"$ally_reinforcement_stage", 4), #up to 4 reinforcements     
      (val_add, "$ally_reinforcement_stage", 1), 
      #This checks the faction of the quest giver.
      (quest_get_slot, ":troop", "qst_blank_quest_03", slot_quest_object_center),
      (store_faction_of_party, ":faction", ":troop"),      
      
      #This checks what type of enemy troops to spawn, depending on faction of quest giver (North or South)
      #Once checked, we then spawn the troop we want. For higher level players, they get upgraded.
      (try_begin),
        (eq, ":faction", "fac_umbar"),
        (assign, ":enemy_melee_tier_1", "trp_corsair_marauder"),
        #(troop_get_upgrade_troop, ":enemy_melee_tier_2", "trp_corsair_marauder",0),
        (assign, ":enemy_archer_tier_1", "trp_militia_of_umbar"),
        #(troop_get_upgrade_troop, ":enemy_archer_tier_2", "trp_marksman_of_umbar",0),
      #  (display_message, "@DEBUG: Umbar Troops Spawned", color_bad_news),
      (else_try), #Rhun
        (assign, ":enemy_melee_tier_1", "trp_rhun_tribal_warrior"),
        #(troop_get_upgrade_troop, ":enemy_melee_tier_2", "trp_rhun_tribal_warrior",0),
        (assign, ":enemy_archer_tier_1", "trp_rhun_tribal_infantry"),
        #(troop_get_upgrade_troop, ":enemy_archer_tier_2", "trp_rhun_tribal_infantry",0), 
       # (display_message, "@DEBUG: Rhun Troops Spawned", color_bad_news),
      (try_end),

      #(store_character_level, ":level", "trp_player"),

      #This is where we check what to spawn depending on player level (Med/High Tier)
      # (try_begin),
        # (ge, ":level", 25),
        # (assign, ":enemy_melee_troop",  ":enemy_melee_tier_2"),
        # (assign, ":enemy_ranged_troop", ":enemy_archer_tier_2"),
      # (else_try),
        (assign, ":enemy_melee_troop",  ":enemy_melee_tier_1"),
        (assign, ":enemy_ranged_troop", ":enemy_archer_tier_1"),
      # (try_end),

      (assign, ":num_allies", 6), #Change this number to change the number of troops spawned
      (assign, ":team_ally", 0),
      (display_message, "@Ally reinforcements have arrived", color_good_news),
      (store_random_in_range, ":rand_speech", 0, 6),
      (try_begin),
        (eq, ":rand_speech", 0),
        (str_store_string, s30, "@Yarrrr!!"),
      (else_try),
        (eq, ":rand_speech", 1),
        (str_store_string, s30, "@Get all of them!"),
      (else_try),
        (eq, ":rand_speech", 2),
        (str_store_string, s30, "@Kill them all!"),
      (else_try),
        (eq, ":rand_speech", 3),
        (str_store_string, s30, "@Toss them overboard!"),
      (else_try),
        (eq, ":rand_speech", 4),
        (str_store_string, s30, "@It is a good day to die!"),
      (else_try),
        (str_store_string, s30, "@All hands on deck! Throw them back!"),
      (try_end),
      (try_begin),
        (lt, ":rand_speech", 3),
        (assign, ":troop_pic", ":enemy_melee_troop"),
      (else_try),
        (assign, ":troop_pic", ":enemy_ranged_troop"),
      (try_end),
      (call_script, "script_troop_talk_presentation", ":troop_pic", 7, 0),

      (store_random_in_range, ":enemy_entry", 12, 21), #This just randomizes the entry points the enemy comes from.
      (entry_point_get_position, pos5, ":enemy_entry"),
      (set_spawn_position, pos5), 
      
      #This spawns the troops, coin flip on whether troops are ranged / melee, as per the above troop assignments.
      (try_for_range, ":unused", 0, ":num_allies"),
          (store_random_in_range, ":rnd_troop", 0,100),
          (le, ":rnd_troop", 50),
          (spawn_agent, ":enemy_melee_troop"),
          (agent_set_team, reg0, ":team_ally"),
        (else_try),
          (spawn_agent, ":enemy_ranged_troop"),
          (agent_set_team, reg0, ":team_ally"),
      (try_end),

      #This asks them to charge, secretly.
      (set_show_messages, 0),
      (team_give_order, ":team_ally", grc_everyone, mordr_charge),
      (set_show_messages, 1),
      ],    
    [
      #(display_message, "@DEBUG: Enemy Reinforced!")
    ]
  ),

## Had to separate the triggers because for some reason, it gets buggy if I combined both ally + enemy spawns. See notes above, they are exactly the same, other than this spawns allies.
## Enemy Reinforcement Triggers: 
(5, 0, 0, [
      (store_mission_timer_c, ":mission_time_c"),
      (store_random_in_range, ":ran_time", 5, 15),
      (ge, ":mission_time_c", ":ran_time"), #Random time between 25 - 40 secs
      (reset_mission_timer_c),
      (lt,"$enemy_reinforcement_stage", 8),      
      (val_add, "$enemy_reinforcement_stage", 1),
      (quest_get_slot, ":troop", "qst_blank_quest_03", slot_quest_object_center),
      (store_faction_of_party, ":faction", ":troop"),      
      
      (try_begin),
        (eq, ":faction", "fac_umbar"),
        (assign, ":allies_melee_tier_1", "trp_pelargir_infantry"),
        #(troop_get_upgrade_troop, ":allies_melee_tier_2", "trp_pelargir_infantry",0), #Commented out - If we want to upgrade allies too.
        (assign, ":allies_archer_tier_1", "trp_pelargir_marine"),
        #(troop_get_upgrade_troop, ":allies_archer_tier_2", "trp_pelargir_marine",0),   #Commented out - If we want to upgrade allies too.
        #(display_message, "@DEBUG: Gondor Troops Spawned", color_bad_news),
      (else_try), #Dale
        (assign, ":allies_melee_tier_1", "trp_dale_veteran_warrior"),
        #(troop_get_upgrade_troop, ":allies_melee_tier_2", "trp_merchant_guard_of_dale",0), #Commented out - If we want to upgrade allies too.
        (assign, ":allies_archer_tier_1", "trp_laketown_scout"),
        #(troop_get_upgrade_troop, ":allies_archer_tier_2", "trp_laketown_bowmen",0),   #Commented out - If we want to upgrade allies too.
        #(display_message, "@DEBUG: Dale Troops Spawned", color_bad_news),
      (try_end),


      (assign, ":ally_melee_troop",   ":allies_melee_tier_1"),
      (assign, ":ally_ranged_troop",  ":allies_archer_tier_1"),

	  
	  (store_character_level, ":level", "trp_player"),
	  (store_div, ":num_enemies", ":level", 4), #InVain - scale attacker # to the player's level, easier at the beginning, harder from lvl 24
      (val_min, ":num_enemies", 10),
      #(assign, ":range_end", 6),
      (assign, ":team_enemy", 1),
      (display_message, "@Enemy reinforcements have arrived", color_bad_news),
      (store_random_in_range, ":rand_speech", 0, 6),
      (try_begin),
        (eq, ":rand_speech", 0),
        (str_store_string, s30, "@Forward, men!"),
      (else_try),
        (eq, ":rand_speech", 1),
        (str_store_string, s30, "@Leave none of these filth standing!"),
      (else_try),
        (eq, ":rand_speech", 2),
        (str_store_string, s30, "@End them all!"),
      (else_try),
        (eq, ":rand_speech", 3),
        (str_store_string, s30, "@Drive them back!"),
      (else_try),
        (eq, ":rand_speech", 4),
        (str_store_string, s30, "@Protect the City!"),
      (else_try),
        (str_store_string, s30, "@Forward! Board them!"),
      (try_end),
      (try_begin),
        (lt, ":rand_speech", 3),
        (assign, ":troop_pic", ":ally_melee_troop"),
      (else_try),
        (assign, ":troop_pic", ":ally_ranged_troop"),
      (try_end),
      (call_script, "script_troop_talk_presentation", ":troop_pic", 7, 0),
      (store_random_in_range, ":ally_entry", 2, 11),
      (entry_point_get_position, pos4, ":ally_entry"),
      (set_spawn_position, pos4), 
      (try_for_range, ":unused", 0, ":num_enemies"),
          (store_random_in_range, ":rnd_troop", 0,100),
          (le, ":rnd_troop", 50),
          (spawn_agent, ":ally_melee_troop"),
          (agent_set_team, reg0, ":team_enemy"),
        (else_try),
          (spawn_agent, ":ally_ranged_troop"),
          (agent_set_team, reg0, ":team_enemy"),
      (try_end),

      (set_show_messages, 0),
      (team_give_order, ":team_enemy", grc_everyone, mordr_charge),
      (set_show_messages, 1),
      ],    
    [
      #(display_message, "@DEBUG: Ally Reinforced!")
    ]
  ),

## End Reinforcement Triggers

(1, 60, ti_once,[
  (store_mission_timer_a,reg(1)),
  (ge,reg(1),10),
  (all_enemies_defeated, 5),
  #(neg|main_hero_fallen, 0), #MV
  (set_mission_result,1),
  (display_message,"str_msg_battle_won"),
  (assign,"$battle_won",1),
  (assign, "$g_battle_result", 1),
  (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
    ],[
  (call_script, "script_count_mission_casualties_from_agents"),
  (jump_to_menu, "mnu_sea_battle_quest_results"),
  (finish_mission, 1),]),
 
  common_inventory_not_available, 
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_victory_display,
  common_battle_inventory,      
  common_battle_order_panel,
  common_battle_order_panel_tick,
      
    ],
  ),

### Sea Batlle Quest MT Start (kham)###



( "castle_attack_walls_defenders_sally",mtf_battle_mode,-1,
  "You attack the walls of the castle...",
    [(0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,12,[]),
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,0,[]),
     (3,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,12,[]),
     (3,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),
     ],
    tld_common_wb_muddy_water +
    formations_triggers + AI_triggers +
    common_deathcam_triggers+
    tld_siege_battle_scripts+[
      
      (ti_before_mission_start, 0, 0, [],
       [ (team_set_relation, 0, 2, 1),
         (team_set_relation, 1, 3, 1),
         (call_script, "script_change_banners_and_chest"),
         (call_script, "script_remove_siege_objects"),
		 ]),
      common_battle_tab_press,
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 5, 20),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),
      (0, 0, ti_once, [], [(assign,"$battle_won",0),
                           (assign,"$g_presentation_battle_active", 0),
                           (call_script, "script_combat_music_set_situation_with_culture")]),
      common_music_situation_update,
      common_battle_check_friendly_kills,
      (1, 60, ti_once, [(store_mission_timer_a, reg(1)),
                        (ge, reg(1), 10),
                        (all_enemies_defeated, 2),
                        (neg|main_hero_fallen,0),
                        (set_mission_result,1),
                        (display_message,"str_msg_battle_won"),
                        (assign, "$battle_won", 1),
                        (assign, "$g_battle_result", 1),
                        (assign, "$g_siege_sallied_out_once", 1),
                        (assign, "$g_siege_method", 1), #reset siege timer
                        (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
                        ],
           [(call_script, "script_count_mission_casualties_from_agents"),
            (finish_mission,1)]),
      common_battle_victory_display,
	  common_battle_on_player_down,
      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_battle_inventory,
]),

( "castle_attack_walls_ladder",mtf_battle_mode,-1,
  "You attack the walls of the castle...",
    [

    ## Kham - Distributed Teams using the mtef_team_X flag. 0, 2, 4 are defenders; 1, 3, 5 are attackers. 6 is for the gate. This allows for the attacker_team / defender_team globals to work.
    
    # Attacker initial spawn point (was 0) - Split this into 3 and distribute teams    
     (47,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (47,mtef_attackers|mtef_team_3,af_override_horse,aif_start_alarmed,1,[]),
     (47,mtef_attackers|mtef_team_5,af_override_horse,aif_start_alarmed,1,[]),
     
     # Initial defender spawn point (was 11)  - Split this into 3 and distribute teams   
     (40,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,1,[]),
     (40,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,0,[]),
     (40,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,0,[]),

     # Defender choke points (was 10)
     (41,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,3,[]), # team left flank
     (42,mtef_defenders|mtef_team_2|mtef_infantry_first,af_override_horse,aif_start_alarmed,3,[]), # team center
     (43,mtef_defenders|mtef_team_4|mtef_infantry_first,af_override_horse,aif_start_alarmed,3,[]), # team right flank

     # Defender reinforcements (was 15)
     (44,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]), #entry 5 for add_reinforcements_to_entry - 9, Kham
     (45,mtef_defenders|mtef_team_2,af_override_horse,aif_start_alarmed,0,[]),
     (46,mtef_defenders|mtef_team_4,af_override_horse,aif_start_alarmed,0,[]),

     # Attacker reinforcements (was 0)
     (47,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,5,[]), #entry 8 for add_reinforcements_to_entry - 12, Kham
     (48,mtef_attackers|mtef_team_3,af_override_horse,aif_start_alarmed,5,[]),
     (49,mtef_attackers|mtef_team_5,af_override_horse,aif_start_alarmed,5,[]),

     # defender archer target positions (was 40-43)
     (50,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]), # team left flank
     (51,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (52,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
   (53,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
   (54,mtef_defenders|mtef_team_2|mtef_archers_first,af_override_horse,aif_start_alarmed,2,[]), # team center
     (55,mtef_defenders|mtef_team_2|mtef_archers_first,af_override_horse,aif_start_alarmed,2,[]),
     (56,mtef_defenders|mtef_team_4|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]), # team right flank
   (57,mtef_defenders|mtef_team_4|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (58,mtef_defenders|mtef_team_4|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (59,mtef_defenders|mtef_team_4|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
  ],
   tld_common_wb_muddy_water+
    common_deathcam_triggers+
    tld_siege_battle_scripts+[
  (ti_before_mission_start, 0, 0, [],[
    (team_set_relation, 0, 2, 1),(team_set_relation, 0, 4, 1),(team_set_relation, 4, 2, 1), # TLD expand teams
    (team_set_relation, 1, 3, 1),(team_set_relation, 1, 5, 1),(team_set_relation, 5, 3, 1),
    (team_set_relation, 6, 0, 1),(team_set_relation, 6, 2, 1),(team_set_relation, 6, 4, 1), # TLD gate aggravator team
    (assign, "$gate_aggravator_agent",-1), # can be reassigned by destructible gate scene prop presence
    (assign, "$gate_breached",0), #for scenes without gates, just to make sure it's 0
    (call_script, "script_change_banners_and_chest"),
    (call_script, "script_remove_siege_objects")]),

  # Siege Tutorial

  (6, 0 , ti_once, [
      (eq, "$formations_tutorial", 3)],
      [
      ] + (is_a_wb_mt==1 and [
      (tutorial_message_set_background, 1), 
      ] or []) + [
      (try_begin),
        (eq, "$formations_tutorial", 3),
        (tutorial_message, "@The Last Days of the Third Age has an Advanced Siege AI, vastly different from Native. All troops, including the player's, are distributed amongst different teams (Left Flank / Center / Right Flank).^^ The player is then in charge of commanding their team, while the AI is in charge of commanding the other teams. This allows for a smarter, squad-based, siege battles.^^ Starting troops and reinforcements are commanded to CHARGE during the first few seconds after deployment. After that, your team can be commanded again.", 0 , 15),
      (try_end),
      (val_add, "$formations_tutorial", 1),
      ]),

  (0, 0, ti_once, [],[
    (assign,"$battle_won",0),
    (assign,"$defender_reinforcement_stage",0),
    (assign,"$attacker_reinforcement_stage",0),
    (assign,"$g_presentation_battle_active", 0),
    (assign,"$telling_counter",0),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_siege),
    (assign, "$defender_team"  , 0),(assign, "$attacker_team"  , 1),
    (assign, "$defender_team_2", 2),(assign, "$attacker_team_2", 3),
    (assign, "$defender_team_3", 4),(assign, "$attacker_team_3", 5),
    ]), 
    common_battle_tab_press,
  (ti_question_answered, 0, 0, [],[
    (store_trigger_param_1,":answer"),
    (eq,":answer",0),
    (assign, "$pin_player_fallen", 0),
    (get_player_agent_no, ":player_agent"),
    (agent_get_team, ":agent_team", ":player_agent"),
    (try_begin),
      (neq, "$attacker_team", ":agent_team"),
      (neq, "$attacker_team_2", ":agent_team"),
      (neq, "$attacker_team_3", ":agent_team"), # if defender - cannot retreat
      (str_store_string, s5, "str_can_not_retreat"),
      #(call_script, "script_simulate_retreat", 8, 15),
    (else_try),
      (str_store_string, s5, "str_retreat"),
      (call_script, "script_simulate_retreat", 5, 20),
    (try_end),
      (call_script, "script_count_mission_casualties_from_agents"),
      (finish_mission,0),
    ]),

  ## WB Only - When a horse archer spawns, we set them to Archers, instead of Cavalry.

  ] + (is_a_wb_mt==1 and [

  (ti_on_agent_spawn, 0, 0, [], 
    [
      (store_trigger_param_1, ":is_horse_archer_agent"),
      (get_player_agent_no, ":player_agent"),
      (neq, ":is_horse_archer_agent", ":player_agent"),
      (agent_get_troop_id, ":troop_id", ":is_horse_archer_agent"),
      (troop_is_guarantee_horse, ":troop_id"),
      (troop_is_guarantee_ranged, ":troop_id"),
      (agent_set_division, ":is_horse_archer_agent", grc_archers),
    ]),

  ] or []) + [

  ## End Horse Archer to Cavalry division

  ## This block starts the commands of both attackers and defenders at the beginning of battle. (trigger_initial_commands)
  ## Both Attackers & Defenders are asked to move towards Entry Point 41, 42, 43
  ## Attacker Archers are asked to HOLD at entry point 60,61,62.
  ## I added Siege order exception (charge) to attackers for Umbar Camp, so that they do not get stuck on boats.
  ## I also added an exception to Dol Amroth, but this may no longer be needed.

  (3, 0, 0, [(lt,"$telling_counter",3)],[ # need to repeat orders several times for the bitches to listen
    (val_add, "$telling_counter",1),
    (set_show_messages, 0),
    (assign,":defteam","$defender_team"),
    (assign,":atkteam","$attacker_team"),
    (assign,":entry2",60),
    (try_for_range,":entry",41,44), # cycle through flanks and assign teams' destinations 
      (entry_point_get_position, pos10, ":entry"), #TLD, was 10
      (team_give_order, ":defteam", grc_infantry, mordr_hold), 
      (team_give_order, ":defteam", grc_infantry, mordr_stand_closer),
      (team_give_order, ":defteam", grc_infantry, mordr_stand_closer),
      (team_give_order, ":defteam", grc_archers, mordr_stand_ground),
      (team_give_order, ":defteam", grc_cavalry, mordr_hold), 
      (team_give_order, ":defteam", grc_cavalry, mordr_stand_closer),
      (team_give_order, ":defteam", grc_cavalry, mordr_stand_closer),
      (team_set_order_position, ":defteam", grc_infantry, pos10), 
      (team_set_order_position, ":defteam", grc_cavalry, pos10), 
      (team_set_order_position, ":atkteam", grc_everyone, pos10), #InVain: Just disable this line if we want attacker infantry to charge and attacker player to command own troops freely.
      (entry_point_get_position, pos10, ":entry2"), #TLD, was 10
      (team_give_order, ":atkteam", grc_archers, mordr_hold),
      (team_set_order_position, ":atkteam", grc_archers, pos10),
      (val_add,":defteam",2),
      (val_add,":atkteam",2),
      (val_add,":entry2",1),
    (try_end),
    (set_show_messages, 1),
    (try_begin),  #Siege Order Exceptions (Kham)
      (eq, "$g_encountered_party", "p_town_umbar_camp"),
      (team_give_order, ":atkteam", grc_everyone, mordr_charge),
      #(display_message, "@Charge", color_bad_news),
    (else_try),
      (eq, "$g_encountered_party", "p_town_dol_amroth"),
      (entry_point_get_position, pos10, 62),
      (team_give_order, ":atkteam", grc_everyone, mordr_hold),
      (team_set_order_position, ":atkteam", grc_everyone, pos10),
     # (display_message, "@moving to pos10", color_good_news),
    (try_end),]),

  ## End of Starting Orders Block ##

  ## Reinforcement Scripted destinations (trigger_reinforcement_scripted_destination)
  ## I added this block so that reinforcements still try to take the flanks or the center (as above).
  ## We set a scripted destination for the agents, and after a few seconds, clear it, when they are close to their destination.
  ## We are using the slot_agent_is_not_reinforcement as a tracker.

  (ti_on_agent_spawn, 0, 0, [(this_or_next|ge, "$attacker_reinforcement_stage", 1), (ge, "$defender_reinforcement_stage",1)], [
    
    #(display_message, "@Scripting reinforcement destinations"),
    (store_trigger_param_1, ":agent_no"),
      (neq, ":agent_no", "$gate_aggravator_agent"), #We don't ask the gate aggravator to do anything :)
      (agent_is_human, ":agent_no"), #neither horses
      (agent_slot_eq, ":agent_no", slot_agent_is_not_reinforcement, 0), # We check if these are reinforcements, and not inital spawns
      (agent_get_team, ":reinforcement_team", ":agent_no"),
      (agent_get_class, ":agent_class", ":agent_no"),
      (neq, ":agent_class", grc_archers), #Do not apply to archers
      
      #This block here checks if chokepoints are taken (troop_slot for trp_no_troop, 0,1,2)

      (try_for_range, ":slot", 0, 3),
        (troop_get_slot, ":choke_point_taken", "trp_no_troop", ":slot"),
        (eq, ":choke_point_taken", -1),
        (set_show_messages, 0),
        (team_give_order, ":reinforcement_team", grc_infantry, mordr_charge),
        (team_give_order, ":reinforcement_team", grc_cavalry, mordr_charge),
        (set_show_messages, 1),

      #If chokepoints are not taken yet...

      (else_try),
          (eq, "$gate_breached", 1),
          (store_random_in_range, ":random", 0, 100),
          (le, ":random", 50), #75% Chance troop is asked to go through the portal. Other than that, go to team destinations. InVain - toned done
          (entry_point_get_position, pos10, 41), #InVain - #41 is center (cause that's the player's team), not 42
          (agent_set_scripted_destination, ":agent_no", pos10),
          ] + (is_a_wb_mt==1 and [
          (agent_force_rethink, ":agent_no"),
          ] or []) + [
          (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 42), #Kham - Use this slot to track scripted movement
         # (display_message, "@Reinforcement Agent moving towards Center"),

      (else_try), #If gate is not breached, and left flank not taken, move reinforcements there.
        (try_begin),
          (eq, ":slot", 0),
          (this_or_next|eq, ":reinforcement_team", 0),
          (             eq, ":reinforcement_team", 1),
          (entry_point_get_position, pos10, 41),
          (agent_set_scripted_destination, ":agent_no", pos10),
          ] + (is_a_wb_mt==1 and [
          (agent_force_rethink, ":agent_no"),
          ] or []) + [
          (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 41), #Kham - Use this slot to track scripted movement
          #(display_message, "@Reinforcement Agent moving towards Left"),

        (else_try), #If gate is not breached, and right flank not taken, move reinforcements there.
          (eq, ":slot", 2),
          (this_or_next|eq, ":reinforcement_team", 4),
          (             eq, ":reinforcement_team", 5),
          (entry_point_get_position, pos10, 43),
          (agent_set_scripted_destination, ":agent_no", pos10),
          ] + (is_a_wb_mt==1 and [
          (agent_force_rethink, ":agent_no"),
          ] or []) + [
          (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 43), #Kham - Use this slot to track scripted movement
          #(display_message, "@Reinforcement Agent moving towards Right"),  

        (else_try), #If gate is not breached, and center is not taken, move reinforcements there.
          (this_or_next|eq, ":reinforcement_team", 2),
          (             eq, ":reinforcement_team", 3),
          (entry_point_get_position, pos10, 42),
          (agent_set_scripted_destination, ":agent_no", pos10),
          ] + (is_a_wb_mt==1 and [
          (agent_force_rethink, ":agent_no"),
          ] or []) + [
          (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 42), #Kham - Use this slot to track scripted movement
          #(display_message, "@Reinforcement Agent moving towards Center"),
        (try_end),
      (try_end),
   ]),

  ## This is where we remove the scripted mode of the reinforcement agents. (trigger_remove_reinforcement_scripted_destinations)
  (7, 0, 0, [(this_or_next|ge, "$attacker_reinforcement_stage", 1), (ge, "$defender_reinforcement_stage",1)], [

    (get_player_agent_no, ":player_agent"),
    #(display_message, "@Ending reinforcement scripted destination"),
    (try_for_agents, ":agent_no"),
      (neq, ":agent_no", "$gate_aggravator_agent"),
      (neq, ":agent_no", ":player_agent"),
      (agent_is_human, ":agent_no"),
      (agent_get_slot, ":destination", ":agent_no", slot_agent_is_not_reinforcement),
      (ge, ":destination", 41),
      (agent_get_position, pos10, ":agent_no"),
      (entry_point_get_position, pos11, ":destination"),
      (get_distance_between_positions, ":destination_dist", pos10, pos11),
      (lt, ":destination_dist", 1000),
      (agent_clear_scripted_mode, ":agent_no"),
        ] + (is_a_wb_mt==1 and [
        (agent_force_rethink, ":agent_no"),
      (agent_set_is_alarmed, ":agent_no", 1),
        ] or []) + [
      (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement,3),
    (try_end),
 ]),

  ## END Reinforcement Scripted destinations

  ## This block seems to be for commanding the defenders to go back to their flanks. I do not think this is important, perhaps has been left for testing.
  ## From the MBX forums, this was the intetion: "TODO: 1) make player assume command of the nearest ally team when he is near and pushes a button -GA"
  ## I can attempt to do what is designed, just needs a lot of testing. 

  #(0, 0, 2,[(this_or_next|game_key_clicked, key_o),(game_key_is_down, key_o)],
  #  [(entry_point_get_position, pos10, 41),(team_set_order_position, "$defender_team"  , grc_everyone, pos10),
  #  (entry_point_get_position, pos10, 42),(team_set_order_position, "$defender_team_2", grc_everyone, pos10),
  #  (entry_point_get_position, pos10, 43),(team_set_order_position, "$defender_team_3", grc_everyone, pos10),
  #  (display_message,"@On your positions, bitchez!!")]),

  ## End of Team Command Control Block

  ## Reinforcements block

  ## This block checks the first spawns and sets their slot as 'not reinforcement'. This triggers once.
  (0, 2, ti_once, [], [(try_for_agents, ":agent_no"),(agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 1),(try_end)]),

  ## This block is what checks for reinforcements. Attackers first, then defenders.
  
  (1, 0, 5,[(lt,"$attacker_reinforcement_stage",10)],[ #InVain: max reinf stage was 15, it's no possible that siege attacks stop
    (assign,":atkteam","$attacker_team"),
    (assign,":entry",11), #iterate through 8 9 10 - changed to 12,13,14
    (try_for_range,":unused",0,3), #cycle through attacker teams, check if depleted and reinforce
      (store_normalized_team_count,":num_attackers",":atkteam"),
      (val_add,":atkteam",2),
      (val_add,":entry",1),
      (lt,":num_attackers",13), #InVain: was 10, attacker reinforcements arrive ealier...
      (add_reinforcements_to_entry, ":entry", 6), #was 8, ... but are smaller
      #(display_message, "@Attackers Reinforced", color_good_news),
      (val_add,"$attacker_reinforcement_stage", 1),
      (assign, "$attacker_archer_melee",1), #Kham - Every reinforcement event leads to a refresh of attack mode.
    (try_end)]),

  (3, 0, 5, [(lt,"$defender_reinforcement_stage", 25),(store_mission_timer_a,":mission_time"),(ge,":mission_time",10)],[ #InVain: max reinf stage was 15, defenders fight to the end. May need to adjust desperate charge conditions below.
    (assign,":defteam","$defender_team"),
    (assign,":entry",8), #iterate through 5 6 7 - Changed to 9,10,11
    (try_for_range,":unused",0,3), #cycle through defender teams, check if depleted and reinforce
      (store_normalized_team_count,":num_defenders",":defteam"),
      (val_add,":defteam",2),
      (val_add,":entry",1),
      (lt,":num_defenders",14),
      (add_reinforcements_to_entry, ":entry", 6), #TLD, was 4, 7 #InVain, was 7, now 6
      #(display_message, "@Defenders Reinforced", color_good_news),
      (val_add,"$defender_reinforcement_stage",1),
    (try_end),
    
    ## This block controls when Defender starts their desperate charge. I've added some improvements VC added to their sieges.

    (try_begin),
      (store_mission_timer_a,":mission_time"),
      (gt, ":mission_time", 180), #3 minutes before checking for desparate charge
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (neq, ":player_team", "$defender_team"),   #When player is defending, don't let defenders do a desparate charge.
      (neq, ":player_team", "$defender_team_2"), #When player is defending, don't let defenders do a desparate charge.
      (neq, ":player_team", "$defender_team_3"), #When player is defending, don't let defenders do a desparate charge.
      (ge, "$defender_reinforcement_stage", 7),
      (set_show_messages, 0),
      (team_give_order, "$defender_team"  , grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
      (team_give_order, "$defender_team_2", grc_infantry, mordr_charge),
      (team_give_order, "$defender_team_3", grc_infantry, mordr_charge),
      (team_give_order, "$defender_team"  , grc_cavalry, mordr_charge), #AI desperate charge:infantry!!!
      (team_give_order, "$defender_team_2", grc_cavalry, mordr_charge),
      (team_give_order, "$defender_team_3", grc_cavalry, mordr_charge),
      (set_show_messages, 1),
      #(display_message,"@Defenders: infantry CHARGE!!"),
      (ge, "$defender_reinforcement_stage", 14),
      (set_show_messages, 0),
      (team_give_order, "$defender_team"  , grc_everyone, mordr_charge), #AI desperate charge: everyone!!!
      (team_give_order, "$defender_team_2", grc_everyone, mordr_charge),
      (team_give_order, "$defender_team_3", grc_everyone, mordr_charge),
      (set_show_messages, 1),
      #(display_message,"@Defenders: everyone CHARGE!!"),
    (try_end),

    ## This block puts the gate aggravator in place

    (try_begin),
      (neq, "$gate_aggravator_agent",-1),
      (eq, "$gate_breached",0),
      (entry_point_get_position, pos13, 39),
      (agent_set_scripted_destination,"$gate_aggravator_agent",pos13,1),
      (agent_set_position,"$gate_aggravator_agent",pos13),
      (agent_set_hit_points,"$gate_aggravator_agent",100,0),
    (try_end)]),

   ## This block calls the script to move archers to archer positions. 
   ## In TLD, attacker archers are asked to hold ground in entry point 60, 61, and 62 if the right,left, center flanks have NOT been taken by the attackers

  (2, 0, 0,[(gt, "$defender_reinforcement_stage", 0)],[(call_script, "script_siege_move_archers_to_archer_positions")]),

  ## This block is so that we revert attacker archers to regular attack mode when reinforcement comes.

   (5, 0, 0, [
     (eq, "$attacker_archer_melee",1),
     ],
     [
     (try_for_agents, ":agent_no"),  
       (agent_is_human, ":agent_no"),
       (agent_is_alive, ":agent_no"),
       (agent_get_party_id, ":agent_party", ":agent_no"),
       (agent_get_team, ":agent_team", ":agent_no"),
       (this_or_next|eq, ":agent_team", "$attacker_team"),(this_or_next|eq, ":agent_team", "$attacker_team_2"),(eq, ":agent_team", "$attacker_team_3"),
       (neq, ":agent_party", "p_main_party"), 
       (agent_ai_set_always_attack_in_melee, ":agent_no", 0),
       (assign, "$attacker_archer_melee",0),
     (try_end),
     (try_begin),
      (eq, "$cheat_mode", 1),
      (display_message, "@DEBUG: Attackers go back to regular attack mode"),
     (try_end),
   ]),

   ## This block is to make sure attacker archers do not stall on ladders
   (35, 0, 0, [
     (eq, "$attacker_archer_melee", 0), 
     ],
     [
     (try_for_agents, ":agent_no"),  
       (agent_is_human, ":agent_no"),
       (agent_is_alive, ":agent_no"),
       (agent_get_party_id, ":agent_party", ":agent_no"),
       (agent_get_team, ":agent_team", ":agent_no"),
       (this_or_next|eq, ":agent_team", "$attacker_team"),(this_or_next|eq, ":agent_team", "$attacker_team_2"),(eq, ":agent_team", "$attacker_team_3"),
       (neq, ":agent_party", "p_main_party"),
       (agent_ai_set_always_attack_in_melee, ":agent_no", 1),
     (try_end),
     (try_begin),
      (eq, "$cheat_mode", 1),
      (display_message, "@DEBUG: Attackers do not stall on ladders triggered"),
     (try_end),
   ]),
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,
  common_siege_refill_ammo,
  common_siege_check_defeat_condition,
  common_battle_order_panel,
  common_battle_order_panel_tick,
  common_inventory_not_available,
   
   (5, 0, 0,[], # distribute agents among teams
     [(try_for_agents, ":agent"),
        (agent_is_alive,":agent"),
        (agent_is_human,":agent"),
		    (neg|agent_is_defender,":agent"), #InVain: So only attackers get redistributed. I know that this is crude :)
        (agent_slot_eq,":agent",slot_agent_arena_team_set,0),
        (store_random_in_range, ":team", 0,3),
        #(try_begin), # when gate breached assign more people to medium team (which is gate oriented)
        #  (eq,"$gate_breached",1),
        #  (store_random_in_range, ":x",0,2),
        #  (eq, ":x",1),
        #  (assign, ":team", 1),
        #(try_end),
        (val_mul, ":team", 2),
        (try_begin),
          (neg|agent_is_defender,":agent"),
          (val_add,":team",1),
        (try_end),
        (agent_set_team, ":agent", ":team"),
        (agent_set_slot,":agent",slot_agent_arena_team_set,1),

        (agent_get_party_id, ":party", ":agent"),
        (get_player_agent_no, ":player"),

        #Give player his troops.
        (try_begin),
          (eq, ":party", "p_main_party"),
          (agent_get_team, ":player_team", ":player"),
          (agent_set_team, ":agent", ":player_team"),
          #(display_message, "@Adding agent to player team"),
        (try_end),
    (try_end),
    ]),

  ## This Block checks if chokepoints are taken. (trigger_check_chokepoints)
  ## We check the troop slot of trp_no_troop (0,1,2) which corresponds to each choke point (entry 41,42,43)
  ## If we find less than 2 defenders near the chokepoint, we consider that chokepoint taken and the team that is assigned to that choke point is asked to charge.

  (10, 0, 0,[(store_mission_timer_a, ":mission_time"), (gt, ":mission_time", 30)], [# check if targets are captured by attackers; only fire after 30 seconds.
    (try_for_range, ":slot",0,3),
      (neg|troop_slot_eq,"trp_no_troop",":slot",-1), # -1 in slot means this flank defeated its choke and proceeds with charge
      (troop_set_slot,"trp_no_troop",":slot",0),
      #(display_message, "@DEBUG: Slot Set to 0"),
    (try_end),
    (try_for_agents, ":agent"),
      (agent_is_alive,":agent"),
      (agent_is_defender,":agent"),
      (agent_get_position, pos0, ":agent"),
      (try_for_range, ":entry",41,44), 
        (store_sub,":slot",":entry",41), #0, 1, 2
        (neg|troop_slot_eq,"trp_no_troop",":slot",-1), # proceed with counting defenders if choke not captured yet
        #(display_message, "@found valid defender"),
        (entry_point_get_position, pos10, ":entry"), # count defenders in proximity of choke points
        (get_distance_between_positions, ":dist", pos0, pos10),
        (lt,":dist", 500),
        (troop_get_slot,":x","trp_no_troop",":slot"), #+1 defender found
        (val_add, ":x", 1), #Kham - Add this here, to count number of defenders.
        #(display_message, "@DEBUG: +1 defender found", color_good_news),
        (troop_set_slot,"trp_no_troop",":slot",":x"),
      (try_end),
    (else_try),
      (neg|agent_is_defender, ":agent"), #attacker
      (agent_get_position, pos0, ":agent"),
      (try_for_range, ":entry",41,44),
        (store_sub,":slot",":entry",38), #3, 4, 5
        (neg|troop_slot_eq,"trp_no_troop",":slot",-1), # proceed with counting defenders if choke not captured yet
        #(display_message, "@found valid defender"),
        (entry_point_get_position, pos10, ":entry"), # count defenders in proximity of choke points
        (get_distance_between_positions, ":dist", pos0, pos10),
        (lt,":dist", 800),
        (troop_get_slot,":x","trp_no_troop",":slot"), #+1 attacker found
        (val_add, ":x", 1), #Kham - Add this here, to count number of attacker.
        #(display_message, "@DEBUG: +1 attacker found", color_good_news),
        (troop_set_slot,"trp_no_troop",":slot",":x"),
      (try_end),
    (try_end),
        (set_show_messages, 0),

    (get_player_agent_no, ":player_agent"),
    (agent_get_team, ":player_team", ":player_agent"),

    (try_for_range, ":slot",0,3),
      (neg|troop_slot_ge,"trp_no_troop",":slot",2), #if 0-1 defenders standing -> make attacking team and defender reinfs charge at will (if not > = 2, charge)
      (troop_set_slot,"trp_no_troop",":slot",-1),
      (store_mul,":defteam",":slot",2),(store_add,":atkteam",":defteam",1),
      #(assign, reg11, ":defteam"), (assign, reg12, ":atkteam"),
      #(display_message, "@DEBUG: Defender Team - {reg11}; Attacker Team - {reg12}", color_bad_news),
      (this_or_next|neq, ":defteam", ":player_team"),
      (             neq, ":atkteam", ":player_team"),
      (team_give_order, ":defteam", grc_everyone, mordr_charge),
      (team_give_order, ":atkteam", grc_everyone, mordr_charge),
      #(store_add,":entry",":slot",41),(entry_point_get_position, pos10, ":entry"), #sieges work better if archers charge, too
      #(team_give_order, ":atkteam", grc_archers, mordr_stand_closer),
      #(team_give_order, ":atkteam", grc_archers, mordr_stand_closer),
      #(team_set_order_position, ":atkteam", grc_archers, pos10),
      
    (try_end),

    (try_for_range, ":slot_attacker", 3,6),
      (troop_slot_ge,"trp_no_troop",":slot",3), #if there are 3 attackers in the area, charge.
      (troop_set_slot,"trp_no_troop",":slot",-1),
      (try_begin),
        (eq, ":slot_attacker", 3),
        (assign, ":atkteam", 1),
      (else_try),
        (eq, ":slot_attacker", 4),
        (assign, ":atkteam", 3),
      (else_try),
        (assign, ":atkteam",5),
      (try_end),
      (team_give_order, ":atkteam", grc_everyone, mordr_charge),
    (try_end),

    (set_show_messages, 1),
    #(display_message, "@DEBUG: Choke points taken, Attackers are charging!", color_bad_news),
   ]),
  ##      (15, 0, 0,
  ##       [
  ##         (get_player_agent_no, ":player_agent"),
  ##         (agent_get_team, ":agent_team", ":player_agent"),
  ##         (neq, "$attacker_team", ":agent_team"),
  ##         (assign, ":non_ranged", 0),
  ##         (assign, ":ranged", 0),
  ##         (assign, ":ranged_pos_x", 0),
  ##         (assign, ":ranged_pos_y", 0),
  ##         (set_fixed_point_multiplier, 100),
  ##         (try_for_agents, ":agent_no"),
  ##           (eq, ":non_ranged", 0),
  ##           (agent_is_human, ":agent_no"),
  ##           (agent_is_alive, ":agent_no"),
  ##           (neg|agent_is_defender, ":agent_no"),
  ##           (agent_get_class, ":agent_class", ":agent_no"),
  ##           (try_begin),
  ##             (neq, ":agent_class", grc_archers),
  ##             (val_add, ":non_ranged", 1),
  ##           (else_try),
  ##             (val_add, ":ranged", 1),
  ##             (agent_get_position, pos0, ":agent_no"),
  ##             (position_get_x, ":pos_x", pos0),
  ##             (position_get_y, ":pos_y", pos0),
  ##             (val_add, ":ranged_pos_x", ":pos_x"),
  ##             (val_add, ":ranged_pos_y", ":pos_y"),
  ##           (try_end),
  ##         (try_end),
  ##         (try_begin),
  ##           (eq, ":non_ranged", 0),
  ##           (gt, ":ranged", 0),
  ##           (val_div, ":ranged_pos_x", ":ranged"),
  ##           (val_div, ":ranged_pos_y", ":ranged"),
  ##           (entry_point_get_position, pos0, 10),
  ##           (init_position, pos1),
  ##           (position_set_x, pos1, ":ranged_pos_x"),
  ##           (position_set_y, pos1, ":ranged_pos_y"),
  ##           (position_get_z, ":pos_z", pos0),
  ##           (position_set_z, pos1, ":pos_z"),
  ##           (get_distance_between_positions, ":dist", pos0, pos1),
  ##           (gt, ":dist", 1000), #average position of archers is more than 10 meters far from entry point 10
  ##           (team_give_order, "$attacker_team", grc_archers, mordr_hold),
  ##           (team_set_order_position, "$attacker_team", grc_archers, pos0),
  ##         (else_try),
  ##           (team_give_order, "$attacker_team", grc_everyone, mordr_charge),
  ##         (try_end),
  ##         ],
  ##       []),
 (20, 0, 0,[], # report attackers and defenders distribution
   [(assign,reg0,0),(assign,reg1,0),(assign,reg2,0),(assign,reg3,0),(assign,reg4,0),(assign,reg5,0),
  (try_for_agents, ":agent"),
    (agent_is_alive,":agent"),
    (agent_is_human,":agent"),
    (agent_get_team, ":team", ":agent"),
    (try_begin),(eq,":team",0),(val_add, reg0,1),
     (else_try),(eq,":team",1),(val_add, reg1,1),
     (else_try),(eq,":team",2),(val_add, reg2,1),
     (else_try),(eq,":team",3),(val_add, reg3,1),
     (else_try),(eq,":team",4),(val_add, reg4,1),
     (else_try),(eq,":team",5),(val_add, reg5,1),
    (try_end),
  (try_end),
  (eq, "$cheat_mode", 1),
  (set_show_messages, 1),
  (display_message, "@Attackers: {reg1}/{reg3}/{reg5} Defenders: {reg0}/{reg2}/{reg4}")]),

]),

( "castle_attack_walls_ladder_native",mtf_battle_mode,-1,
  "You attack the walls of the castle...",
    [

    ## Kham - Distributed Teams using the mtef_team_X flag. 0, 2, 4 are defenders; 1, 3, 5 are attackers. 6 is for the gate. This allows for the attacker_team / defender_team globals to work.
    
    # Attacker initial spawn point (was 0) - Split this into 3 and distribute teams    
     (47,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (47,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (47,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     
     # Initial defender spawn point (was 11)  - Split this into 3 and distribute teams   
     (40,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,3,[]),
     (40,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,0,[]),
     (40,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,0,[]),

     # Defender choke points (was 10)
     (41,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,0,[]), # team left flank
     (42,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,0,[]), # team center
     (43,mtef_defenders|mtef_team_0|mtef_infantry_first,af_override_horse,aif_start_alarmed,0,[]), # team right flank

     # Defender reinforcements (was 15)
     (44,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,2,[]), #entry 5 for add_reinforcements_to_entry - 9, Kham
     (45,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,2,[]),
     (46,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,2,[]),

     # Attacker reinforcements (was 0)
     (47,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,5,[]), #entry 8 for add_reinforcements_to_entry - 12, Kham
     (48,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,5,[]),
     (49,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,5,[]),

     # defender archer target positions (was 40-43)
     (50,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]), # team left flank
     (51,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (52,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
   (53,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
   (54,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,2,[]), # team center
     (55,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,2,[]),
     (56,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]), # team right flank
   (57,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (58,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (59,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
  ],
   tld_common_wb_muddy_water+
    common_deathcam_triggers+
    tld_siege_battle_scripts+[
  (ti_before_mission_start, 0, 0, [],[
    (team_set_relation, 0, 2, 1),(team_set_relation, 0, 4, 1),(team_set_relation, 4, 2, 1), # TLD expand teams
    (team_set_relation, 1, 3, 1),(team_set_relation, 1, 5, 1),(team_set_relation, 5, 3, 1),
    (team_set_relation, 6, 0, 1),(team_set_relation, 6, 2, 1),(team_set_relation, 6, 4, 1), # TLD gate aggravator team
    (assign, "$gate_aggravator_agent",-1), # can be reassigned by destructible gate scene prop presence
    (call_script, "script_change_banners_and_chest"),
    (call_script, "script_remove_siege_objects")]),
  (0, 0, ti_once, [],[
    (assign,"$battle_won",0),
    (assign,"$defender_reinforcement_stage",0),
    (assign,"$attacker_reinforcement_stage",0),
    (assign,"$g_presentation_battle_active", 0),
    (assign,"$telling_counter",0),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_siege),
    (assign, "$defender_team"  , 0),(assign, "$attacker_team"  , 1),
    (assign, "$defender_team_2", 2),(assign, "$attacker_team_2", 3),
    (assign, "$defender_team_3", 4),(assign, "$attacker_team_3", 5),
    ]), 
    common_battle_tab_press,
  (ti_question_answered, 0, 0, [],[
    (store_trigger_param_1,":answer"),
    (eq,":answer",0),
    (assign, "$pin_player_fallen", 0),
    (get_player_agent_no, ":player_agent"),
    (agent_get_team, ":agent_team", ":player_agent"),
    (try_begin),
      (neq, "$attacker_team", ":agent_team"),
      (neq, "$attacker_team_2", ":agent_team"),
      (neq, "$attacker_team_3", ":agent_team"), # if defender - cannot retreat
      (str_store_string, s5, "str_can_not_retreat"),
      #(call_script, "script_simulate_retreat", 8, 15),
    (else_try),
      (str_store_string, s5, "str_retreat"),
      (call_script, "script_simulate_retreat", 5, 20),
    (try_end),
      (call_script, "script_count_mission_casualties_from_agents"),
      (finish_mission,0),
    ]),


  ## Reinforcements block

  ## This block checks the first spawns and sets their slot as 'not reinforcement'. This triggers once.
  (0, 2, ti_once, [], [(try_for_agents, ":agent_no"),(agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 1),(try_end)]),

  ## This block is what checks for reinforcements. Attackers first, then defenders.
  
  (1, 0, 5,[(lt,"$attacker_reinforcement_stage",10)],[ #InVain: max reinf stage was 15, it's no possible that siege attacks stop
    (assign,":atkteam","$attacker_team"),
    (assign,":entry",11), #iterate through 8 9 10 - changed to 12,13,14
    (try_for_range,":unused",0,3), #cycle through attacker teams, check if depleted and reinforce
      (store_normalized_team_count,":num_attackers",":atkteam"),
      (val_add,":atkteam",2),
      (val_add,":entry",1),
      (lt,":num_attackers",13), #InVain: was 10, attacker reinforcements arrive ealier...
      (add_reinforcements_to_entry, ":entry", 6), #was 8, ... but are smaller
      #(display_message, "@Attackers Reinforced", color_good_news),
      (val_add,"$attacker_reinforcement_stage", 1),
      (assign, "$attacker_archer_melee",1), #Kham - Every reinforcement event leads to a refresh of attack mode.
    (try_end)]),
  (3, 0, 5, [(lt,"$defender_reinforcement_stage", 25),(store_mission_timer_a,":mission_time"),(ge,":mission_time",10)],[ #InVain: max reinf stage was 15, defenders fight to the end. May need to adjust desperate charge conditions below.
    (assign,":defteam","$defender_team"),
    (assign,":entry",8), #iterate through 5 6 7 - Changed to 9,10,11
    (try_for_range,":unused",0,3), #cycle through defender teams, check if depleted and reinforce
      (store_normalized_team_count,":num_defenders",":defteam"),
      (val_add,":defteam",2),
      (val_add,":entry",1),
      (lt,":num_defenders",14),
      (add_reinforcements_to_entry, ":entry", 6), #TLD, was 4, 7 #InVain, was 7, now 6
      #(display_message, "@Defenders Reinforced", color_good_news),
      (val_add,"$defender_reinforcement_stage",1),
    (try_end),
    
    ## This block controls when Defender starts their desperate charge. I've added some improvements VC added to their sieges.

    (try_begin),
      (store_mission_timer_a,":mission_time"),
      (gt, ":mission_time", 180), #3 minutes before checking for desparate charge
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (neq, ":player_team", "$defender_team"),   #When player is defending, don't let defenders do a desparate charge.
      (neq, ":player_team", "$defender_team_2"), #When player is defending, don't let defenders do a desparate charge.
      (neq, ":player_team", "$defender_team_3"), #When player is defending, don't let defenders do a desparate charge.
      (ge, "$defender_reinforcement_stage", 7),
      (set_show_messages, 0),
      (team_give_order, "$defender_team"  , grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
      (team_give_order, "$defender_team_2", grc_infantry, mordr_charge),
      (team_give_order, "$defender_team_3", grc_infantry, mordr_charge),
      (team_give_order, "$defender_team"  , grc_cavalry, mordr_charge), #AI desperate charge:infantry!!!
      (team_give_order, "$defender_team_2", grc_cavalry, mordr_charge),
      (team_give_order, "$defender_team_3", grc_cavalry, mordr_charge),
      (set_show_messages, 1),
      #(display_message,"@Defenders: infantry CHARGE!!"),
      (ge, "$defender_reinforcement_stage", 14),
      (set_show_messages, 0),
      (team_give_order, "$defender_team"  , grc_everyone, mordr_charge), #AI desperate charge: everyone!!!
      (team_give_order, "$defender_team_2", grc_everyone, mordr_charge),
      (team_give_order, "$defender_team_3", grc_everyone, mordr_charge),
      (set_show_messages, 1),
      #(display_message,"@Defenders: everyone CHARGE!!"),
    (try_end),

    ## This block puts the gate aggravator in place

    (try_begin),
      (neq, "$gate_aggravator_agent",-1),
      (eq, "$gate_breached",0),
      (entry_point_get_position, pos13, 39),
      (agent_set_scripted_destination,"$gate_aggravator_agent",pos13,1),
      (agent_set_position,"$gate_aggravator_agent",pos13),
      (agent_set_hit_points,"$gate_aggravator_agent",100,0),
    (try_end)]),

   ## This block calls the script to move archers to archer positions. 
   ## In TLD, attacker archers are asked to hold ground in entry point 60, 61, and 62 if the right,left, center flanks have NOT been taken by the attackers

  (2, 0, 0,[(gt, "$defender_reinforcement_stage", 0)],[(call_script, "script_siege_move_archers_to_archer_positions")]),

  ## This block is so that we revert attacker archers to regular attack mode when reinforcement comes.

   (5, 0, 0, [
     (eq, "$attacker_archer_melee",1),
     ],
     [
     (try_for_agents, ":agent_no"),  
     (agent_is_human, ":agent_no"),
     (agent_is_alive, ":agent_no"),
     (agent_get_team, ":agent_team", ":agent_no"),
     (this_or_next|eq, ":agent_team", "$attacker_team"),(this_or_next|eq, ":agent_team", "$attacker_team_2"),(eq, ":agent_team", "$attacker_team_3"),
     (agent_ai_set_always_attack_in_melee, ":agent_no", 0),
     (assign, "$attacker_archer_melee",0),
     (try_end),
     (try_begin),
      (eq, "$cheat_mode", 1),
      (display_message, "@DEBUG: Attackers go back to regular attack mode"),
     (try_end),
   ]),

   ## This block is to make sure attacker archers do not stall on ladders
   (35, 0, 0, [
     (eq, "$attacker_archer_melee", 0), 
     ],
     [
     (try_for_agents, ":agent_no"),  
     (agent_is_human, ":agent_no"),
     (agent_is_alive, ":agent_no"),
     (agent_get_team, ":agent_team", ":agent_no"),
     (this_or_next|eq, ":agent_team", "$attacker_team"),(this_or_next|eq, ":agent_team", "$attacker_team_2"),(eq, ":agent_team", "$attacker_team_3"),
     (agent_ai_set_always_attack_in_melee, ":agent_no", 1),
     (try_end),
     (try_begin),
      (eq, "$cheat_mode", 1),
      (display_message, "@DEBUG: Attackers do not stall on ladders triggered"),
     (try_end),
   ]),
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,
  common_siege_refill_ammo,
  common_siege_check_defeat_condition,
  common_battle_order_panel,
  common_battle_order_panel_tick,
  common_inventory_not_available,
   
]),

( "besiege_inner_battle_castle",mtf_battle_mode,-1,
  "You attack the walls of the castle...",
    [(0 , mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (6 , mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (7 , mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (16, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (17, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (18, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (19, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (20, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     ],
    tld_common_wb_muddy_water+[
	(ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),
	common_battle_tab_press,
	(ti_question_answered, 0, 0, [],[
		(store_trigger_param_1,":answer"),
		(eq,":answer",0),
		(assign, "$pin_player_fallen", 0),
		(str_store_string, s5, "str_retreat"),
		(call_script, "script_simulate_retreat", 5, 20),
		(assign, "$g_battle_result", -1),
		(set_mission_result,-1),
		(call_script, "script_count_mission_casualties_from_agents"),
		(finish_mission,0)]),
	(0, 0, ti_once, [],[(assign,"$battle_won",0),
						(assign,"$g_presentation_battle_active", 0),
						(call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed)]),
	#AI Tiggers
	(0,0,ti_once,[(assign, "$defender_team", 0),(assign, "$attacker_team", 1),(assign, "$defender_team_2", 2),(assign, "$attacker_team_2", 3)], []),
	common_battle_check_friendly_kills,
	common_battle_check_victory_condition,
	common_battle_victory_display,
	common_battle_on_player_down,
	common_battle_order_panel,
	common_battle_order_panel_tick,
	common_battle_inventory,
]),
( "besiege_inner_battle_town_center",mtf_battle_mode,-1,
  "You attack the walls of the castle...",
    [(0 , mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,4,[]),
     (2 , mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (23, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (24, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (25, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (26, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (27, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (28, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     ],
  tld_common_wb_muddy_water+[
	(ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),
	common_battle_tab_press,
	(ti_question_answered, 0, 0, [],
		[(store_trigger_param_1,":answer"),
		(eq,":answer",0),
		(assign, "$pin_player_fallen", 0),
		(str_store_string, s5, "str_retreat"),
		(call_script, "script_simulate_retreat", 5, 20),
		(assign, "$g_battle_result", -1),
		(set_mission_result,-1),
		(call_script, "script_count_mission_casualties_from_agents"),
		(finish_mission,0)]),
	(0, 0, ti_once, [], [(assign,"$battle_won",0),
                           (assign,"$g_presentation_battle_active", 0),
                           (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed)]),
	(0, 0, ti_once, [],[
		(assign, "$defender_team", 0),
		(assign, "$attacker_team", 1),
		(assign, "$defender_team_2", 2),
		(assign, "$attacker_team_2", 3)]),

	common_battle_check_friendly_kills,
	common_battle_check_victory_condition,
	common_battle_victory_display,
	common_battle_on_player_down,
	common_battle_order_panel,
	common_battle_order_panel_tick,
	common_battle_inventory,
]),
( "sneak_caught_fight",mtf_arena_fight,-1,
  "You must fight your way out!",
    [ (0,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,pilgrim_disguise),
      (25,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (32,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
#      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
    ],
  tld_common_wb_muddy_water+[
	(ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),
	(ti_tab_pressed, 0, 0, [],
		[(question_box,"str_do_you_wish_to_surrender")]),
	(ti_question_answered, 0, 0, [],
		[(store_trigger_param_1,":answer"),(eq,":answer",0),
		(assign, "$recover_after_death_menu", "mnu_recover_after_death_town_alone"),
		(jump_to_menu,"mnu_tld_player_defeated"),(finish_mission,0)]),

	(1, 0, ti_once, [],[(play_sound,"snd_sneak_town_halt"),(call_script, "script_music_set_situation_with_culture", mtf_sit_fight)]),
	(0, 3, 0, [(main_hero_fallen,0)],[(assign, "$recover_after_death_menu", "mnu_recover_after_death_town_alone"),(jump_to_menu,"mnu_tld_player_defeated"),(finish_mission,0)]),
	(5, 1, ti_once, [(num_active_teams_le,1),(neg|main_hero_fallen)],[(assign,"$auto_menu",-1),(jump_to_menu,"mnu_sneak_into_town_caught_dispersed_guards"),(finish_mission,1)]),
	(ti_on_leave_area, 0, ti_once, [],[(assign,"$auto_menu",-1),(jump_to_menu,"mnu_sneak_into_town_caught_ran_away"),(finish_mission,0)]),
	(ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_arena")], []),
]),

( "training_ground_training", mtf_arena_fight, -1,
  "Training.",
    [ (0,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (1,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (2,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (3,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      # Player
      (4,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[]),
      # Opponents
      (5,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (6,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (7,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (8,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      # Spares
      (9,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (10,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (11,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      # Player team
      (12,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[]), #player
      (13,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (14,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (15,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      # Enemy team
      (16,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (17,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (18,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (19,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (20,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (21,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (22,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (23,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (24,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (25,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (26,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
      (27,mtef_visitor_source|mtef_team_1,af_override_all_but_horse,aif_start_alarmed,1,[itm_practice_staff]),
    ],tld_common_wb_muddy_water+[
	(0, 0, ti_once, [], [(eq, "$g_tld_training_mode", abm_gauntlet),(start_presentation, "prsnt_gauntlet")]),
	(0, 0, ti_once, [], [#(play_sound, "snd_arena_ambiance", sf_looping),
							(call_script, "script_music_set_situation_with_culture", mtf_sit_arena)]),
	# terrible workaround for the buggy? add_visitors_to_current_scene
	(0.2, 0, 0, [(eq, "$g_tld_training_mode", abm_gauntlet)],
		[(store_add, ":enemies", "$g_tld_training_wave", 2),
         (assign, ":alive_enemies", 0),
         (try_for_agents, ":agent_no"), # count enemy agents spawned
           (agent_is_alive, ":agent_no"),
           (agent_is_human, ":agent_no"),
           (agent_get_team, ":team_no", ":agent_no"),
           (eq, ":team_no", 1),
           (val_add, ":alive_enemies", 1),
         (try_end),
	# (assign, reg1, ":enemies"),
	# (assign, reg2, ":alive_enemies"),
	# (display_message, "@Spawned/alive: {reg1}/{reg2}."),
         (store_sub, ":enemies_to_kill", ":alive_enemies", ":enemies"), # the number of extra enemies to eliminate
	     (set_show_messages, 0),
         (init_position, pos1),
         (try_for_agents, ":agent_no"), #kill the first ":enemies_to_kill" enemy agents
           (gt, ":enemies_to_kill", 0),
           (agent_is_alive, ":agent_no"),
           (agent_is_human, ":agent_no"),
           (agent_get_team, ":team_no", ":agent_no"),
           (eq, ":team_no", 1),
           # suicide
		   (agent_get_horse, ":horse", ":agent_no"),
		   (try_begin),
             (gt, ":horse", -1), 
             (agent_set_hit_points, ":horse", 0, 1),
	         (agent_deliver_damage_to_agent, ":agent_no", ":horse"),
             (agent_set_position, ":horse", pos1),
		   (try_end),
           (agent_set_hit_points, ":agent_no", 0, 1),
	       (agent_deliver_damage_to_agent, ":agent_no", ":agent_no"),
           (agent_set_position, ":agent_no", pos1),
           (val_sub, ":enemies_to_kill", 1),
         (try_end),
	     (set_show_messages, 1)]),
      
	# spawn next wave of enemies
	(1, 0, 0,[
         (eq, "$g_tld_training_mode", abm_gauntlet),
         (neg|main_hero_fallen),
         (num_active_teams_le, 1)
         ],[
         (store_add, ":enemies", "$g_tld_training_wave", 3),
         (assign, ":enemy_entry_point", 16), #first entry point
         (assign, ":spawnings", ":enemies"),
         (val_min, ":spawnings", 12), #total entry points
         (store_div, ":to_spawn", ":enemies", ":spawnings"), #1 or more
         (store_add, ":to_spawn_plus_one", ":to_spawn", 1), #2 or more
         (store_mod, ":one_extra", ":enemies", ":spawnings"), #0-11
# (assign, reg1, ":enemies"),
# (assign, reg2, ":spawnings"),
# (assign, reg3, ":to_spawn"),
# (assign, reg4, ":one_extra"),
# (display_message, "@Enemies {reg1}. Spawnings {reg2}. To spawn {reg3}. One extra {reg4}."),

         (store_character_level, ":player_level_bias", "trp_player"),
         (val_clamp, ":player_level_bias", 1, 30), #1-29
         (val_sub, ":player_level_bias", 15), #-14..+14
         (try_for_range, ":spawn_number", 0, ":spawnings"),
           (store_random_in_range, ":random_no", 0, 100),
           (val_add, ":random_no", ":player_level_bias"), #-14..+113
           (try_begin),
             (lt, ":random_no", 20),
             (faction_get_slot, ":opponent", "$g_encountered_party_faction", slot_faction_tier_1_troop),
           (else_try),
             (lt, ":random_no", 40),
             (faction_get_slot, ":opponent", "$g_encountered_party_faction", slot_faction_tier_2_troop),
           (else_try),
             (lt, ":random_no", 60),
             (faction_get_slot, ":opponent", "$g_encountered_party_faction", slot_faction_tier_3_troop),
           (else_try),
             (lt, ":random_no", 80),
             (faction_get_slot, ":opponent", "$g_encountered_party_faction", slot_faction_tier_4_troop),
           (else_try),
             (faction_get_slot, ":opponent", "$g_encountered_party_faction", slot_faction_tier_5_troop),
           (try_end),
           
           (try_begin),
             (lt, ":spawn_number", ":one_extra"),
             (add_visitors_to_current_scene, ":enemy_entry_point", ":opponent", ":to_spawn_plus_one"),
# (assign, reg1, ":enemy_entry_point"),
# (assign, reg2, ":to_spawn_plus_one"),
# (display_message, "@Entry {reg1}: {reg2}."),
           (else_try),
             (add_visitors_to_current_scene, ":enemy_entry_point", ":opponent", ":to_spawn"),
# (assign, reg1, ":enemy_entry_point"),
# (assign, reg2, ":to_spawn"),
# (display_message, "@Entry {reg1}: {reg2}."),
           (try_end),
           (val_add, ":enemy_entry_point", 1),
         (try_end),
         (val_add, "$g_tld_training_wave", 1),
         (assign, reg1, "$g_tld_training_wave"),
         (display_message, "@Reached Gauntlet wave {reg1}!", 0x30FFC8)]),
      
	# finish mission
	(1, 3, ti_once,
       [ (assign, ":gauntlet_finished", 0),
         (try_begin),
           (eq, "$g_tld_training_mode", abm_gauntlet),
           (main_hero_fallen),
           (assign, ":gauntlet_finished", 1),
         (try_end),
         (assign, ":one_team_left", 0),
         (try_begin),
           (neq, "$g_tld_training_mode", abm_gauntlet),
           (num_active_teams_le, 1),
           (assign, ":one_team_left", 1),
         (try_end),
         (this_or_next|eq, ":gauntlet_finished", 1),
         (this_or_next|main_hero_fallen),
         (eq, ":one_team_left", 1)
         ],[
		 (try_begin),
           (eq, "$g_tld_training_mode", abm_gauntlet),
           (troop_set_slot, "$g_talk_troop", slot_troop_trainer_training_result, "$g_tld_training_wave"),
         (else_try),
           (neg|main_hero_fallen),
           (troop_set_slot, "$g_talk_troop", slot_troop_trainer_training_result, 100),
         (else_try),
           (assign, ":alive_enemies", 0),
           (try_for_agents, ":agent_no"),
             (agent_is_alive, ":agent_no"),
             (agent_is_human, ":agent_no"),
             (agent_get_team, ":team_no", ":agent_no"),
             (eq, ":team_no", 1),
             (val_add, ":alive_enemies", 1),
           (try_end),
           (store_sub, ":dead_enemies", "$g_tld_training_opponents", ":alive_enemies"),
           (store_mul, ":training_result", ":dead_enemies", 100),
           (val_div, ":training_result", "$g_tld_training_opponents"),
           (troop_set_slot, "$g_talk_troop", slot_troop_trainer_training_result, ":training_result"),
         (try_end),
         (jump_to_menu, "mnu_auto_training_ground_trainer"),
         (finish_mission)]),
]),
( "training_ground_trainer_talk", 0, -1,
    "Training.",
    [ (0,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (1,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (2,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (3,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (4,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (5,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (6,mtef_scene_source|mtef_team_0,0,0,1,[]),
    ],tld_common_wb_muddy_water+[
	(ti_before_mission_start , 0, 0,[],[(call_script, "script_change_banners_and_chest")]),
	(ti_inventory_key_pressed, 0, 0,[(set_trigger_result,1)], []),
	(ti_tab_pressed          , 0, 0,[(set_trigger_result,1)], []),
]),
( "arena_melee_fight",mtf_arena_fight,-1,
  "You enter a melee fight in the arena.",
    [ (0 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      (1 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (2 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      (3 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (4 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      (5 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b ]),
      (6 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse ]),
      (7 ,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),

      (8 ,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      (9 ,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (10,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (11,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b]),
      (12,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      (13,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (14,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (15,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b]),

      (16,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      (17,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (18,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      (19,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (20,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      (21,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b ]),
      (22,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse ]),
      (23,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      (25,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (26,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      (27,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (28,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      (29,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b]),
      (30,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      (31,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      (32, mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (33,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
      (34,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword, itm_tab_shield_small_round_b]),
      (35,mtef_visitor_source|mtef_team_4,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
      (36, mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      (37,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword, itm_tab_shield_small_round_b]),
      (38,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      (39,mtef_visitor_source|mtef_team_4,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
#40-49 not used yet
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_tab_shield_small_round_b]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_arena_lance,itm_tab_shield_small_round_b,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),
      #(24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_arrows,itm_saddle_horse]),

      (50, mtef_scene_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
      (51, mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
      (52, mtef_scene_source,af_override_horse,0,1,[]),
#not used yet:
      (53, mtef_scene_source,af_override_horse,0,1,[]),(54, mtef_scene_source,af_override_horse,0,1,[]),(55, mtef_scene_source,af_override_horse,0,1,[]),
#used for torunament master scene

      (56, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_tab_shield_small_round_b, itm_black_tunic]),
      (57, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_tab_shield_small_round_b, itm_black_tunic]),
    ],
    tld_common_wb_muddy_water+
    tournament_triggers
),
( "arena_challenge_fight",mtf_team_fight, -1, # used for orc mutiny
  "You enter a melee fight.",
    [ (0, mtef_visitor_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
	  (1, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
	  (2, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(3, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(4, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(5, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []), #spectators
	  (6, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(7, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(8, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(9, mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
	  (10,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(11,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(12,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(13,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
	  (14,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(15,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(16,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(17,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
	  (18,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(19,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(20,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(21,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
	  (22,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(23,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(24,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(25,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
	  (26,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(27,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(28,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),(29,mtef_visitor_source|mtef_team_2, af_override_horse, 0, 1, []),
    ],tld_common_wb_muddy_water+[
	common_inventory_not_available,
#	(ti_tab_pressed, 0, 0, [(display_message, "@Cannot leave now.")], []),
			
	(ti_tab_pressed,0,0,[],[
		(try_begin),#If the battle is won, missions ends.
			(num_active_teams_le,2),
			(neg|main_hero_fallen, 0),
			(assign, "$mutiny_stage", 4),
			(finish_mission),
		(else_try),
			(main_hero_fallen),
			(assign, "$mutiny_stage", 5),
			(finish_mission),
		(else_try),
			(display_message, "@Cannot leave now."),
		(try_end)]),
			
	(ti_before_mission_start, 0, 0, [],[(team_set_relation, 0, 1, -1),(team_set_relation, 0, 2, 0),(team_set_relation, 1, 2, 0)]),
	(0, 0, ti_once, [],[(call_script, "script_music_set_situation_with_culture", mtf_sit_arena)]),
    (0.3, 0, 0, [], [ # spectators cheer
		(try_for_agents,":agent"),
			(agent_get_entry_no,reg1,":agent"),(neq,reg1,0),(neq,reg1,1), # main guys do not cheer
			(agent_get_slot,":counter",":agent",slot_agent_is_in_scripted_mode),
			(try_begin),
				(gt, ":counter", 0), (val_sub,":counter", 1),(agent_set_slot,":agent",slot_agent_is_in_scripted_mode,":counter"), # pass cheering cycles
			(else_try),
				(store_random_in_range,reg1,0,100),(lt,reg1,10), # 10% of times
				(agent_set_slot,":agent",slot_agent_is_in_scripted_mode,13), # remember that the guy is cheering now, pass 13 cycles after that
				(agent_set_animation, ":agent", "anim_cheer"),
				(agent_get_troop_id,":troop", ":agent"),
				(troop_get_type,reg1,":troop"),
				(try_begin),(is_between, reg1, tf_urukhai, tf_orc_end),(agent_play_sound, ":agent", "snd_uruk_yell"),
				 (else_try),(eq, reg1, tf_orc),(agent_play_sound, ":agent", "snd_orc_cheer"),
				 (else_try),(agent_play_sound, ":agent", "snd_man_yell"),
				(try_end),
			(try_end),
		(try_end)]),
		tld_cheer_on_space_when_battle_over_press,tld_cheer_on_space_when_battle_over_release,
	(1, 60, 1,[(store_mission_timer_a,reg1),(ge,reg1,10)],[
		(try_begin),
			(main_hero_fallen),
			(assign, "$mutiny_stage", 5),
			(finish_mission),
		(else_try),
			(num_active_teams_le,2),
			(assign, "$mutiny_stage", 4),
			(display_message,"str_msg_battle_won"),
		(try_end)]),
	
]),

( "custom_battle",mtf_battle_mode,-1,
  "You lead your men to battle.",
    [ (0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    tld_common_wb_muddy_water+
    tld_common_battle_scripts+[
	common_custom_battle_tab_press,
	common_custom_battle_question_answered,
	common_inventory_not_available,
	(0, 0, ti_once, [],[ (assign, "$g_battle_result", 0),(call_script, "script_combat_music_set_situation_with_culture")]),
	common_music_situation_update,
	custom_battle_check_victory_condition,
	common_battle_victory_display,
	custom_battle_check_defeat_condition,
]),
( "custom_battle_siege",mtf_battle_mode,-1,
  "You lead your men to battle.",
    [ (0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    tld_common_wb_muddy_water+
    tld_common_battle_scripts+[
	common_battle_mission_start,
	(0, 0, ti_once,[ (assign, "$defender_team", 0),(assign, "$attacker_team", 1),(assign, "$defender_team_2", 2),(assign, "$attacker_team_2", 3)], []),
	common_custom_battle_tab_press,
	common_custom_battle_question_answered,
	common_inventory_not_available,
	common_custom_siege_init,
	common_music_situation_update,
	custom_battle_check_victory_condition,
	common_battle_victory_display,
	custom_battle_check_defeat_condition,
	common_siege_attacker_do_not_stall,
	common_siege_refill_ammo,
	common_siege_init_ai_and_belfry,
	common_siege_move_belfry,
	common_siege_rotate_belfry,
	common_siege_assign_men_to_belfry,
	common_siege_ai_trigger_init_2,
]),

( "custom_battle_form_test",mtf_battle_mode,-1,
  "You lead your men into battle",
 [
  # Player
  (0,mtef_team_0|mtef_use_exact_number,af_override_horse,aif_start_alarmed,30,[]),

  # Companions (Add more for more companions)
  (1,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (2,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (3,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (4,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (5,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (6,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (7,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (8,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (9,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (10,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (11,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (12,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (13,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (14,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (15,mtef_visitor_source|mtef_team_0,0,0,1,[]),
  (16,mtef_visitor_source|mtef_team_0,0,0,1,[]),

  # Enemies:
  (17,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (18,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (19,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (20,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (21,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (22,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (23,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (24,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (25,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (26,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (27,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (28,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (29,mtef_visitor_source|mtef_team_1,0,0,1,[]),
  (30,mtef_visitor_source|mtef_team_1,0,0,1,[]),

 ],
  # Triggers
  tld_common_wb_muddy_water +
  formations_triggers + 
  AI_triggers + 
  common_deathcam_triggers +
  moto_formations_triggers +  
  tld_common_battle_scripts + 
  command_cursor_sub_mod + [
  common_battle_tab_press,
  common_music_situation_update,
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,
  common_battle_on_player_down,
  common_battle_inventory,

  # Make the teams enemies...
  (ti_before_mission_start, 0, 0, [], [(team_set_relation, 0, 1, -1),(assign, "$battle_won", 0)]),

  (0, 0, ti_once, 
  [
    #(str_store_troop_name, s1, reg20),
    #(display_message, "@DEBUG: Enemy to spawn: {s1}"),
    #(display_message, "@DEBUG: Enemies to spawn: {reg21}"),

    # Make enemies charge...
    (set_show_messages, 0),
      (team_give_order, 1, grc_everyone, mordr_hold),
      (team_give_order, 1, grc_everyone, mordr_stand_ground),
    (set_show_messages, 1),
  ], 
  []),    
  common_battle_order_panel,
  common_battle_order_panel_tick,
]),

( "custom_battle_5",mtf_battle_mode,-1,
  "You lead your men to battle.",
    [ (0 ,mtef_attackers|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),     (1 ,mtef_attackers|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,20,[]),
      (2 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (4 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (6 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (8 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    tld_common_wb_muddy_water+
    tld_common_battle_scripts+[
	common_custom_battle_tab_press,
	common_custom_battle_question_answered,
	common_custom_siege_init,
	common_inventory_not_available,
	common_music_situation_update,
	custom_battle_check_victory_condition,
	common_battle_victory_display,
	custom_battle_check_defeat_condition,
	(0, 0, ti_once,[(assign, "$defender_team", 1),(assign, "$attacker_team", 0),(assign, "$defender_team_2", 3),(assign, "$attacker_team_2", 2)], []),
	common_siege_ai_trigger_init_2,
	common_siege_attacker_do_not_stall,
	common_siege_refill_ammo,
	common_siege_init_ai_and_belfry,
	common_siege_move_belfry,
	common_siege_rotate_belfry,
	common_siege_assign_men_to_belfry,
]),
( "custom_battle_HD",mtf_battle_mode,-1,
  "You wait on the walls for the incoming horde.",
    [	(0 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(2 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(4 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(6 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(8 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(10,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(12,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
		(14,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),

		(16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(18,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(20,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(22,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(24,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(26,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(28,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(30,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    tld_common_wb_muddy_water+
    tld_siege_battle_scripts +[
    common_custom_battle_tab_press,
    common_custom_battle_question_answered,
    common_custom_siege_init,
    common_inventory_not_available,
    common_music_situation_update,
    custom_battle_check_victory_condition,
    common_battle_victory_display,
    custom_battle_check_defeat_condition,
	(ti_before_mission_start,0,0,[],[(set_rain,1,100),(team_set_relation,6,0,1),(team_set_relation,6,2,1),(assign,"$gate_aggravator_agent",-1)]),
    (0, 0, ti_once,[],[
		(assign, "$defender_team", 0),
		(assign, "$attacker_team", 1),
		(assign, "$defender_team_2", 3),
		(assign, "$attacker_team_2", 2),
		(set_fog_distance, 80, 0x010101)]),
	common_siege_ai_trigger_init_2,
	common_siege_attacker_do_not_stall,
	common_siege_refill_ammo,
	ballista_init,ballista_operate,ballista_disengage,ballista_shoot,ballista_reload_pause,ballista_reload,ballista_fly_missile,ballista_toggle_fire_arrow,
	ballista_missile_illumination,ballista_camera_alignment,ballista_turn_up,ballista_turn_down,ballista_turn_left,ballista_turn_right,ballista_aim,
	################## THUNDER AND LIGHTNING BEGIN ###############################
	(3, 0.2, 6, [(store_random_in_range,":rnd",1,5),(eq,":rnd",1),(set_fog_distance, 200, 0xaaaaaa),],
				[(set_fog_distance, 80, 0x010101),(get_player_agent_no,":plyr"),(agent_play_sound, ":plyr", "snd_thunder"),(assign, "$lightning_cycle",1),]),
	(0.4,0.1, 6,[(eq,"$lightning_cycle",1),(set_fog_distance, 150, 0x777777),],		###### Lightning afterflashes 
				[(set_fog_distance, 80, 0x010101),(assign,"$lightning_cycle",2),]),
	(0.5,0.1, 6,[(eq,"$lightning_cycle",2),(set_fog_distance, 120, 0x555555),],
				[(set_fog_distance, 80, 0x010101),(assign,"$lightning_cycle",0),]),
	################## THUNDER AND LIGHTNING END #################################
	HD_ladders_init,HD_ladders_rise,
	stonelobbing_init_stone,stonelobbing_pick_stone,stonelobbing_throw_stone,stonelobbing_fly_stone,stonelobbing_carry_stone,
]),
( "custom_battle_dynamic_scene", mtf_battle_mode,-1,"You lead your men to random scenery battle!",
    [ (0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    tld_common_wb_muddy_water+
    tld_common_battle_scripts+[
    common_custom_battle_tab_press,
    common_custom_battle_question_answered,
    common_inventory_not_available,
    common_music_situation_update,
    custom_battle_check_victory_condition,
    common_battle_victory_display,
    custom_battle_check_defeat_condition,
    (0,0,ti_once,[(assign, "$defender_team", 0),(assign, "$attacker_team", 1),(assign, "$defender_team_2", 3),(assign, "$attacker_team_2", 2)],[]),
	horse_whistle_init,
	horse_whistle,
	######################################## tree selection and 
	scene_init_fog,scene_set_fog,
	scene_set_flora_init,scene_set_flora_army_spawn,
]),
( "custom_battle_parade",mtf_battle_mode,-1,
    "You line up your troops for the parade",
    [ (0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (2 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(3 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (4 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(5 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (6 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(7 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (8 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(9 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (16,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (24,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),

      (30,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (32,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(33,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(35,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(37,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(39,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (40,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(41,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(43,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(45,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(47,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (48,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(49,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(51,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(53,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(55,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (56,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(57,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(59,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
     ],
    tld_common_wb_muddy_water+
    tld_common_battle_scripts+[
	common_custom_battle_tab_press,
	common_custom_battle_question_answered,
	common_inventory_not_available,
  (5, 0, ti_once, [], [
    (tutorial_message, "@Press F3 to start the battle.",0,8)]),
	(0, 0, ti_once, [],[
		(assign, "$g_battle_result", 0),
		(assign, "$defender_team", 0),
		(assign, "$attacker_team", 1),
		(assign, "$defender_team_2", 2),
		(assign, "$attacker_team_2", 3),
		(team_set_relation, 0, 2, 1),
		(team_set_relation, 0, 1, -1),
		(call_script, "script_combat_music_set_situation_with_culture")]),
    (0,0,0, [(key_clicked, key_f3)],[#fight after F3 pressed
		(display_message,"@THREE.. TWO... ONE.... FIGHT!"),
		(try_for_agents,":agent"),
			(agent_is_human),
			(agent_get_entry_no,":entry",":agent"),
			(try_begin),(ge,":entry",30),(agent_set_team,":agent",1),
			 (else_try)                 ,(agent_set_team,":agent",0),
			(try_end),
		(try_end),
		(team_give_order, 0, grc_everyone, mordr_charge),
		(team_give_order, 1, grc_everyone, mordr_charge)]),
    common_battle_order_panel,
    common_battle_order_panel_tick,
    common_music_situation_update,
    common_battle_victory_display,
    custom_battle_check_defeat_condition,
]),

("camera_test",0,-1,
 "camera Test.",
    [],
    [(1, 0, 0, [],[(mission_cam_set_mode,1),
          (entry_point_get_position, pos3, 3),
          (mission_cam_set_position, pos3)]),
	#(ti_before_mission_start, 0, 0, [], [(set_rain, 1,100)]),
	(ti_tab_pressed, 0, 0, [],[(finish_mission,0)]),
]),
( "ai_training",0,-1,
  "You start training.",
    [(0,0,0,aif_start_alarmed,30,[]),
     ],
    tld_common_wb_muddy_water+
    tld_common_battle_scripts+[
	(ti_tab_pressed, 0, 0, [],[(finish_mission,0)]),
	(0, 0, ti_once, [], [(assign,"$g_presentation_battle_active", 0),]),
	common_battle_order_panel,
	common_battle_order_panel_tick,
]),
("legendary_place_visit",0,-1,
 "You visit a legendary place.",
    [(0,mtef_scene_source|mtef_team_0,0,0,1,[]),(1,mtef_scene_source|mtef_team_0,0,0,1,[]),(16,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (17,mtef_scene_source|mtef_team_0,0,0,1,[]),(18,mtef_scene_source|mtef_team_0,0,0,1,[]),(19,mtef_scene_source|mtef_team_0,0,0,1,[]),
     ],tld_common_wb_muddy_water+[
    (ti_tab_pressed, 0, 0, [],[(finish_mission,0)]),
	  
    (0,0,ti_once,[],
      [(try_begin),
        (is_currently_night),
        (play_sound, "$bs_night_sound", sf_looping),
			 (else_try),
         (play_sound, "$bs_day_sound",   sf_looping),
			 (try_end)]),
     (10, 0, ti_once, [], [ # Kham - Give legendary place description
        (try_begin),
          (eq, "$g_encountered_party", "p_legend_amonhen"),
          (party_slot_eq, "p_legend_amonhen", slot_legendary_visited, 0),
          (tutorial_message, "@You have come upon the ruins of Amon Hen, the Hill of Sight, a Gondorian watch-tower atop which rests the Seat of Seeing^^You sense that this place was once great but has long been forgotten",0,12),
          (add_xp_as_reward, 250),
          (party_set_slot, "p_legend_amonhen", slot_legendary_visited, 1),
        (else_try),
          (eq, "$g_encountered_party", "p_legend_deadmarshes"),
          (party_slot_eq, "p_legend_deadmarshes", slot_legendary_visited, 0),
          (tutorial_message, "@You have come upon the Dead Marshes, site of the battle of Dagorlad during the War of the Last Alliance^^The marshlands have swallowed up what was once a grassy plain, and now the only green is the scum of livid weed on the dark greasy surfaces of the sullen waters^^Dead grasses and rotting reeds loom up in the mists like ragged shadows of long forgotten summers, and bodies of men, elves, and orcs float in the murky depths^^The air feels cold and clammy, and you can't help but shiver as you see candle-lights flickering in the eyes of an elf corpse just beneath the water's surface",0,12),
          (add_xp_as_reward, 250),
          (party_set_slot, "p_legend_deadmarshes", slot_legendary_visited, 1),
        (else_try),
          (eq, "$g_encountered_party", "p_legend_mirkwood"),
          (party_slot_eq, "p_legend_mirkwood", slot_legendary_visited, 0),
          (tutorial_message, "@You have entered the woods of Southern Mirkwood, once known as Greenwood the Great^^The fortress of Dol Guldur is nearby and it casts a dark shadow over the forest. The woods here feel sickly and full of decay. Ancient oak trees are overrun with rot and fungus and great tangling webs stretch from trunk to trunk^^ The air is everlastingly still and dark and stuffy, and it feels like you are slowly being suffocated",0,12),
          (add_xp_as_reward, 250),
          (party_set_slot, "p_legend_mirkwood", slot_legendary_visited, 1),
        (try_end)]),
]),
( "tld_erebor_dungeon",0,-1,"Default town visit",
    [(0,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (1,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (2,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
     (3,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
     (4,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
	 ],tld_common_wb_muddy_water+fade+[
	#(ti_tab_pressed, 0, 0, [(set_trigger_result,1)], []),
	#(ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1),], []),
	#(1, 0, ti_once, [], [(tutorial_box,"str_tld_erebor_dungeon"),]),
	(ti_before_mission_start, 0, 0, [],[(assign, "$trap_is_active", 1),(assign, "$atak", 0),(team_set_relation, 0, 1, -1),(assign, "$dungeons_in_scene",1)]),
	dungeon_darkness_effect,
	(0, 0, 0, [(eq, "$trap_is_active", 1)],[
		(scene_prop_get_instance, ":instance", "spr_spear_trap_1", 0),
		(prop_instance_get_position, pos1, ":instance"),
		(get_player_agent_no, ":agent"),
		(agent_get_position, pos2, ":agent"),
		(get_distance_between_positions, ":dist", pos1, pos2),
		(le, ":dist", 200),
		(display_message, "str_tld_spear_hit", 0xFFFFAAFF),
		(position_move_z, pos1, 70),
		(prop_instance_animate_to_position, ":instance", pos1, 100),
		(store_agent_hit_points,":hp",":agent",0),
		(val_sub,":hp",20),
		(agent_set_hit_points,":agent",":hp"),
		(agent_play_sound,":agent","snd_spear_trap"),
		(agent_play_sound,":agent","snd_man_hit_pierce_strong"),
		(try_begin),
		(le, ":hp", 1),
		(agent_deliver_damage_to_agent, ":agent", ":agent"),
		(try_end),
		(assign, "$atak", 1)]),
	(1, 3, 0, [(eq, "$atak", 1),],[
		(assign, "$atak", 0),
		(scene_prop_get_instance, ":instance", "spr_spear_trap_1", 0),
		(prop_instance_get_position, pos1, ":instance"),
		(position_move_z, pos1, -70),
		(prop_instance_animate_to_position, ":instance", pos1)]),
]),



# Spears Quest - Dwarven Warehouse (Kham)

( "tld_dwarven_warehouse",0,-1,"Default town visit",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,() ),],tld_common_wb_muddy_water+fade+[
	   (0, 0, ti_once,  
      [
        (quest_slot_eq,"qst_find_lost_spears",slot_quest_current_state, 10),
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos1, ":player_agent"),
        (entry_point_get_position,pos2,15),
        (get_distance_between_positions, ":cur_distance", pos1, pos2),
        (le, ":cur_distance", 100),
        #(display_message, "@DEBUG:Trigger occured"),
      ],
      [ 
       (str_store_troop_name, s3, "trp_dwarf_lord"),
       #(tutorial_message_set_size, 17, 17),
       #(tutorial_message_set_position, 500, 650),
       #(tutorial_message_set_center_justify, 0),
       #(tutorial_message_set_background, 1),
       (tutorial_message, "@You have found the Dwarven Warehouse where the Legendary Spears could be. Report what you find to {s3}", 0, 8),
       (quest_set_slot,"qst_find_lost_spears",slot_quest_current_state, 15),
      ]),
	(ti_tab_pressed, 0, 0, [], [(question_box,"@Leave the Warehouse?")]),
	(ti_question_answered, 0, 0, [], [(store_trigger_param_1,":answer"), (eq,":answer",0), (finish_mission)])
	]),

# Spears Quest - Dwarven Warehouse - End
( "aw_tomb",0,-1,
  "silence...",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons|af_override_head,0,1,() ),],
    custom_tld_bow_always + [
	(ti_tab_pressed, 0, 0, [], [(question_box,"@Leave the place in silence?")]),
	(ti_question_answered, 0, 0, [], [(store_trigger_param_1,":answer"), (eq,":answer",0), (finish_mission)]),
	(0,0,ti_once,[],[(music_set_situation, 0),]),
]),
( "scene_chooser",mtf_battle_mode,-1,
    "You go to the scene",
    [(0 ,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),(4 ,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[])
	],tld_common_wb_muddy_water+[
	(ti_tab_pressed, 0, 0, [],[(finish_mission,0)]),
	(ti_before_mission_start, 0, 0, [], [(assign, "$dungeons_in_scene",1)]),	
	dungeon_darkness_effect,
]),

# daungeon crawl
( "dungeon_crawl_moria_entrance",0,-1,
    "Explore around Moria",
    [(0 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(4 ,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[])
	],tld_common_wb_muddy_water+[
    (ti_tab_pressed, 0, 0, [(eq, "$player_is_inside_dungeon",0)],[(question_box,"@Leave scene?")]),
    (ti_tab_pressed, 0, 0, [(eq, "$player_is_inside_dungeon",1)],[(question_box,"@Trace back your steps and go back in the open now?")]),
	(ti_question_answered, 0, 0, [], [ (store_trigger_param_1,":answer"), (eq,":answer",0), (finish_mission), ]),
	(ti_before_mission_start, 0, 0, [], [ (assign, "$player_is_inside_dungeon",0),(assign, "$dungeons_in_scene",1)]),
	dungeon_darkness_effect,
]),
( "dungeon_crawl_moria_hall",0,-1,
    "Explore around Moria",
    [(0 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(4 ,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[])
	],tld_common_wb_muddy_water+[
    (ti_tab_pressed, 0, 0, [],[(question_box,"@Trace back your steps and go back in the open now?")]),
	(ti_question_answered, 0, 0, [], [ (store_trigger_param_1,":answer"), (eq,":answer",0), (finish_mission)]),
	(ti_before_mission_start, 0, 0, [], [(assign, "$dungeons_in_scene",1), (play_sound, "snd_moria_ambiance", sf_looping), ]),
	dungeon_darkness_effect,
]),
( "dungeon_crawl_moria_deep",mtf_battle_mode,-1,
    "Lost in Moria! Orcs are everywhere! You must find a way out!",
    [(0 ,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),(1 ,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(4 ,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[])
	],tld_common_wb_muddy_water+[
    (ti_tab_pressed, 0, 0, [],[(question_box,"@There is no way out! Surrender to orcs?")]),
	(ti_question_answered, 0, 0, [], [ 
		(store_trigger_param_1,":answer"), (eq,":answer",0), (troop_remove_item, "trp_player","itm_book_of_moria"), (assign, "$recover_after_death_menu", "mnu_recover_after_death_moria"), (jump_to_menu,"mnu_tld_player_defeated"), (finish_mission)]),
	(ti_before_mission_start, 0, 0, [], [ (set_fog_distance,18,0x000001),(assign, "$dungeons_in_scene",1),(play_sound, "snd_moria_ambiance", sf_looping),]),
	dungeon_darkness_effect,
]),

############ 808 stealth & rescue templates
( "infiltration_stealth_mission", mtf_battle_mode,  -1,
  "Default_town_visit", 
	[(0,mtef_visitor_source|mtef_team_1,af_override_horse,                1,1,[]),( 1,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),  
	( 2,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),( 3,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),  
	( 4,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),( 5,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),  
	( 6,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),( 7,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	( 8,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),( 9,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(10,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(12,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(14,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(16,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]), 
	(18,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_2,                0,aif_start_alarmed,1,[]), 
	(20,mtef_visitor_source|mtef_team_2,                0,aif_start_alarmed,1,[]), 
	],tld_common_wb_muddy_water+[
	(0,0,ti_once,[],[
		#  (team_set_relation, 2, 1, 0),
		#  (team_set_relation, 3, 1, -1),
		#  (team_set_relation, 3, 2, 1),
		(call_script, "script_infiltration_mission_synch_agents_and_troops"),
		#  (call_script, "script_infiltration_mission_set_hit_points"),
		# (CppCoder) WTF?
		(try_for_range, reg10, 1, 32),
			(entry_point_get_position, reg10, reg10),
		(try_end),
		(get_player_agent_no, "$current_player_agent"),
		(assign, "$alarm_level", 0)]),

	#(5,0,0,[],[(call_script, "script_infiltration_mission_update_companion_casualties")]),

	(ti_tab_pressed,0,0,[],[(try_begin),(this_or_next|eq, "$battle_won", 1),(eq, "$battle_won", 2),(finish_mission),(try_end)]),
	(ti_question_answered,0,0,[],[(store_trigger_param_1, ":local0"),(eq, ":local0", 0),(finish_mission)]),
	(1,4,ti_once,[(main_hero_fallen)],[(call_script, "script_rescue_failed"),(assign, "$battle_won", 2),(set_mission_result, -1),(finish_mission)]),
	(1,0,ti_once,[(eq, "$sneak_tut", 0)],[
		(tutorial_box, "@Stealth mini-game tutorial: There are two alarm levels. Level 1 is set off by the guards seeing a dead body or by them spotting you. Level 2 is set off by the guards spotting you when level 1 is already active. Level two is dangerous because guards will continue to arrive. You can avoid being spotted by staying hidden. To hid simply move behind various bits of cover."),
		(assign, "$sneak_tut", 1)]),

	(3,0,0,[],[ 
	  (try_for_agents, ":enemy"),
		(agent_is_human, ":enemy"),
		(agent_is_alive, ":enemy"),
		(neg|eq, ":enemy", "$current_player_agent"),
		(store_agent_hit_points,":hp",":enemy",0),
		(try_begin),
			(eq, ":hp", 100), # healthy agents can patrol
			(agent_set_speed_limit,":enemy",4),
			(agent_get_position, pos32, ":enemy"),
			(try_for_range, "$positions", 1, 21),
				(get_distance_between_positions, "$position_distance", "$positions", pos32),
				(neg|gt, "$position_distance", 400),
				(agent_get_slot, "$last_agent_position", ":enemy", 10),
				(store_current_scene, reg45),
				(try_begin),
					(eq, reg45, "$rescue_stealth_scene_1"),
					(neg|eq, "$active_rescue", 4),
					(call_script, "script_mt_sneak_1", ":enemy"),
				(else_try),
					(eq, reg45, "$rescue_stealth_scene_2"),
					(neg|eq, "$active_rescue", 4),
					(call_script, "script_mt_sneak_2", ":enemy"),
				(else_try),
					(eq, "$active_rescue", 4),
					(call_script, "script_isen_sneak_1", ":enemy"),
				(try_end),
				(try_begin),
					(neg|gt, "$position_distance", 200),
					(agent_set_slot, ":enemy", 10, "$positions"),
				(try_end),
			(try_end),
		(else_try), # wounded agents do not patrol, bash player instead
			(agent_clear_scripted_mode,":enemy"),
			(agent_set_speed_limit,":enemy",10),
		(try_end),
	(try_end)]),

	(5,0,0,[],[ 
	  (agent_get_position, pos33, "$current_player_agent"),
	  (try_for_range, ":entries21_32", 21, 32),
		(get_distance_between_positions, ":dist", ":entries21_32", 33),
		(neg|gt, ":dist", 150),
		(eq, "$player_hiding", 0),
		(assign, "$player_hiding", ":entries21_32"),
		(display_message, "@You_are_now_hidden."),
		# (try_begin),
			# (eq, "$hiding_tut", 0),
			# (tutorial_box, "@Stealth_mini-game_tutorial:_There_are_two_alarm_levels._Level_1_is_set_off_by_the_guards_seeing_a_dead_body_or_by_them_spotting_you._Level_2_is_set_off_by_the_guards_spotting_you_when_level_1_is_already_active._Level_two_is_dangerous_because_guards_will_continue_to_arrive._You_can_avoid_being_spotted_by_staying_hidden._To_hid_simply_move_behind_various_bits_of_cover."),
			# (assign, "$hiding_tut", 1),
		# (try_end),
	  (try_end),
	  (assign, reg25, 0),
	  (try_for_range, ":entries21_32", 21, 32),
		(get_distance_between_positions, ":dist", ":entries21_32", pos33),
		(ge, "$player_hiding", 1),
		(ge, ":dist", 150),
		(val_add, reg25, 1),
	  (try_end),
	  (try_begin),
		(eq, reg25, 11),
		(display_message, "@You_move_out_of_hiding."),
		(assign, "$player_hiding", 0),
	  (try_end)]),

	(3,0,0,[],[ 
	  (try_for_agents, ":agent"),
		(agent_is_human, ":agent"),
		(agent_is_alive|neg, ":agent"),
		(neg|eq, ":agent", "$current_player_agent"),
		(agent_get_position, pos34, ":agent"),
		(try_for_agents, ":enemy"),
			(agent_is_human, ":enemy"),
			(agent_is_alive, ":enemy"),
			(neg|eq, ":enemy", "$current_player_agent"),
			(agent_get_position, pos32, ":enemy"),
			(get_distance_between_positions, ":dist", pos32, pos34),
			(try_begin),
				(eq, "$alarm_level", 0),
				(neg|gt, ":dist", 600),
				(assign, "$alarm_level", 1),
				(display_message, "@The_guards_have_spotted_a_dead_body!"),
				(display_message, "@Alarm_Level_is_now_at_1!", 4294945450),
				(agent_play_sound, ":enemy", "snd_man_yell"),
				(reset_mission_timer_a),
			(try_end),
		(try_end),
	  (try_end)]),

	(5,0,0,[(store_mission_timer_a, ":time"),(ge, ":time", 25)],[ 
	  (try_begin),
		(eq, "$alarm_level", 1),
		(assign, "$alarm_level", 0),
		(display_message, "@Alarm_Level_is_now_at_0!", 4289396650),
		(reset_mission_timer_a),
	  (else_try),
		(eq, "$alarm_level", 2),
		(assign, "$alarm_level", 1),
		(display_message, "@Alarm_Level_is_now_at_1!", 4289396650),
		(reset_mission_timer_a),
	  (try_end)]),

	(10,0,0,[(eq, "$alarm_level", 2)],[
	  (try_begin),
		(eq, "$spawn_cycle", 0),
		(set_visitor, 19, "$guard_troop2", 0),
		(set_visitor, 20, "$guard_troop3", 0),
		(assign, "$spawn_cycle", 1),
	  (try_end),
	  (store_random_in_range, ":rnd", 0, 2),
	  (try_begin),(eq, ":rnd", 0),(eq, "$spawn_cycle", 1),(add_reinforcements_to_entry, 19, 1),
	   (else_try),(eq, ":rnd", 1),(eq, "$spawn_cycle", 1),(add_reinforcements_to_entry, 20, 1),
	  (try_end)]),

	(3,0,0,[],[ 
	  (try_for_agents, ":agent"),
		(agent_is_human, ":agent"),
		(agent_is_alive, ":agent"),
		(neg|eq, ":agent", "$current_player_agent"),
		(agent_get_position, pos32, ":agent"),
		(agent_get_position, pos33, "$current_player_agent"),
		(get_distance_between_positions, ":dist", pos33, pos32),
		(try_begin),
			(neg|gt, ":dist", 1200),
			(neg|position_is_behind_position, pos33, pos32),
			(eq, "$player_hiding", 0),
			(try_begin),
				(eq, "$alarm_level", 0),
				(display_message, "@The_guards_have_spotted_you!"),
				(display_message, "@Alarm_Level_is_now_at_1!", 4294945450),
	#            (play_sound, [opmask_sound]53, 0),
				(reset_mission_timer_a),
				(assign, "$alarm_level", 1),
				(store_random_in_range, ":rnd", 0, 11),
				(try_begin),
					(ge, ":rnd", "$meta_stealth"),
					(val_add, "$meta_alarm", 1),
				(try_end),
			(else_try),
				(eq, "$alarm_level", 1),
	#			(agent_set_team  , ":agent", 3),
				(display_message, "@The_guards_have_spotted_you!"),
				(display_message, "@Alarm_Level_is_now_at_2!", 0xFFFFAAAA),
				(agent_play_sound, ":agent", "snd_man_yell"),
				(store_agent_hit_points, ":hp", ":agent", 1), # mark enemy as the one who spotted you (will not return to patrol)
				(val_sub,":hp",1),
				(agent_set_hit_points, ":agent", ":hp", 1),
				(reset_mission_timer_a),
				(assign, "$alarm_level", 2),
				(try_begin),
					(store_random_in_range, ":rnd", 0, 11),
					(ge, ":rnd", "$meta_stealth"),
					(val_add, "$meta_alarm", 1),
				(try_end),
				(store_random_in_range, ":rnd", 0, 2),
				(try_begin),(eq, ":rnd", 0),(set_visitor, 20, "$guard_troop2", 0),
				 (else_try),                (set_visitor, 20, "$guard_troop3", 0),
				(try_end),
				(add_reinforcements_to_entry, 20, 1),
			(try_end),
		(try_end),
	(try_end)]),
]),
( "infiltration_combat_mission",mtf_battle_mode,0,
  "You_lead_your_men_to_battle.",
	[(0,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),( 1,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	( 2,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),( 3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	( 4,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),( 5,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	( 6,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),( 7,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	( 8,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),( 9,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	(10,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(11,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(12,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(13,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(14,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(15,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(16,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(17,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(18,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(19,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(20,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(21,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(22,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(23,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(24,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(25,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(26,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(27,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(28,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(29,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	(30,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),(31,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),
	(32,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),(33,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),
	(34,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),(35,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),
	(36,mtef_visitor_source|mtef_team_2, 271,aif_start_alarmed,1,[]),
	],tld_common_wb_muddy_water+[
	(0,0,ti_once,[],[	(call_script, "script_infiltration_mission_synch_agents_and_troops"),
							(call_script, "script_infiltration_mission_set_hit_points"),
							(call_script, "script_wounded_hero_cap_mission_health")]),
	(5,0,0,[],[(call_script, "script_infiltration_mission_update_companion_casualties")]),
	(1,4,ti_once,[(main_hero_fallen),],[	(call_script, "script_rescue_failed"),
												(call_script, "script_infiltration_mission_update_companion_casualties"),
												(set_mission_result, -1),
												(finish_mission)]),
	(5,0,ti_once,[	(this_or_next|eq, "$rescue_stage", 2),
						(eq, "$rescue_stage", 4),
						(store_mission_timer_a, reg13),
						(ge, reg13, 90),
					],[
						(try_begin),
							(ge, "$meta_alarm", 9),
							(set_visitor, 21, "$guard_troop8", 0),(set_visitor, 22, "$guard_troop8", 0),(set_visitor, 23, "$guard_troop8", 0),(set_visitor, 24, "$guard_troop8", 0),(set_visitor, 25, "$guard_troop8", 0),
						(else_try),
							(is_between, "$meta_alarm", 6, 9),
							(set_visitor, 21, "$guard_troop3", 0),(set_visitor, 22, "$guard_troop3", 0),(set_visitor, 23, "$guard_troop3", 0),(set_visitor, 24, "$guard_troop3", 0),(set_visitor, 25, "$guard_troop3", 0),
						(else_try),
							(is_between, "$meta_alarm", 5, 7),
							(set_visitor, 21, "$guard_troop2", 0),(set_visitor, 22, "$guard_troop2", 0),(set_visitor, 23, "$guard_troop2", 0),(set_visitor, 24, "$guard_troop2", 0),(set_visitor, 25, "$guard_troop2", 0),
						(try_end),
						(reset_mission_timer_a)]),
	(2,0,0,[(eq, "$rescue_stage", 5)],[
				(get_player_agent_no, ":player"),
				(agent_get_position, pos5, ":player"),
				(entry_point_get_position, pos6, 31),
				(try_begin),
					(get_distance_between_positions, ":dist", pos5, pos6),
					(try_begin),
						(neg|ge, ":dist", 400),
				#        (assign, "$dungeon_rescue", 1),
						(call_script, "script_infiltration_mission_update_companion_casualties"),
						(start_mission_conversation, "$rescue_convo_troop"),
					(try_end),
				(try_end)]),
	(ti_tab_pressed,0,0,[],[(try_begin),(eq, "$battle_won", 1),(finish_mission),(try_end)]),
	(ti_question_answered,0,0,[],[(store_trigger_param_1, ":answer"),(eq, ":answer", 0),(finish_mission)]),
]),

# This mission template could be improved for better clarity
( "sorcerer_mission",mtf_battle_mode,0,
  "You_lead_your_men_to_battle.",
	[(0 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]),( 1 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]),  
	( 2 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]),( 3 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]), 
	( 4 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]),( 5 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]), 
	( 6 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]),( 7 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]), 
	( 8 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]),( 9 ,mtef_visitor_source|mtef_team_1 ,af_override_horse, aif_start_alarmed, 1,[]), 
	(10 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),(11 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
	(12 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),(13 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
	(14 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),(15 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),  
	(16 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),(17 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
	(18 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),(19 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),  
	(20 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),(21 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),  
	(22 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),(23 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
	(24 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]),(25 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]), 
	(26 ,mtef_visitor_source|mtef_team_2 ,af_override_horse, aif_start_alarmed, 1,[]) 
	],tld_common_wb_muddy_water+[	
	(0,0,ti_once,[],[ (call_script, "script_infiltration_mission_synch_agents_and_troops"),
						  (call_script, "script_infiltration_mission_set_hit_points"),
						  (call_script, "script_wounded_hero_cap_mission_health")]),
	(2,0,0, [], [(call_script, "script_infiltration_mission_update_companion_casualties")]),
	(1,4,ti_once,[(main_hero_fallen)],
	[
	(try_begin),
		(neg|check_quest_succeeded, "qst_mirkwood_sorcerer"),
		(display_message, "@The_sorcerer_has_fled!", 4294901760),
		(display_message, "@Report_this_ill_news_to_the_Lady_at_once.", 4294901760),
		(quest_set_slot,"qst_mirkwood_sorcerer",slot_quest_current_state,3),
		(call_script, "script_fail_quest","qst_mirkwood_sorcerer"),
	(try_end),
	(call_script, "script_infiltration_mission_update_companion_casualties"),
	(set_mission_result, -1),
	(finish_mission),
	]),

	(5,0, ti_once, [
		  (try_for_agents, ":agent"),
			(agent_is_ally|neg, ":agent"),
			(agent_is_alive, ":agent"),
			(agent_get_troop_id, ":troop", ":agent"),
			(eq, ":troop", "trp_black_numenorean_sorcerer"),
			(agent_get_slot, ":slot1", ":agent", 1),
		  (try_end),
		  (ge, ":slot1", 3),
		],[
		 (try_begin),
			(ge, "$meta_alarm", 9),
			(set_visitor, 21, "$guard_troop8", 0),(set_visitor, 22, "$guard_troop8", 0),(set_visitor, 23, "$guard_troop8", 0),(set_visitor, 24, "$guard_troop8", 0),(set_visitor, 25, "$guard_troop8", 0),
		 (else_try),
			(is_between, "$meta_alarm", 6, 9),
			(set_visitor, 21, "$guard_troop3", 0),(set_visitor, 22, "$guard_troop3", 0),(set_visitor, 23, "$guard_troop3", 0),(set_visitor, 24, "$guard_troop3", 0),(set_visitor, 25, "$guard_troop3", 0),
		 (else_try),
			(is_between, "$meta_alarm", 5, 7),
			(set_visitor, 21, "$guard_troop2", 0),(set_visitor, 22, "$guard_troop2", 0),(set_visitor, 23, "$guard_troop2", 0),(set_visitor, 24, "$guard_troop2", 0),(set_visitor, 25, "$guard_troop2", 0),
		 (try_end),
		 (reset_mission_timer_a)]),
	(5,0,0, [],  [
		(try_for_agents, ":agent"),
			(agent_is_ally|neg, ":agent"),
			(agent_is_alive, ":agent"),
			(agent_get_troop_id, ":troop", ":agent"),
			(eq, ":troop", "trp_black_numenorean_sorcerer"),
			(agent_get_slot, ":slot1", ":agent", 1),
			(try_begin),
				(eq, ":slot1", 0),
				(entry_point_get_position, pos5, 30),
				(agent_set_scripted_destination, ":agent", pos5),
				(agent_set_slot, ":agent", 1, 1),
			(else_try),
				(eq, ":slot1", 1),
				(agent_set_animation, ":agent", "anim_defend_up_staff_keep"),
		        	(play_sound, snd_ghost_ambient_long, 0), #spooky
				(assign, ":numenemies", 0),
				(try_for_agents, ":enemies"),
					(agent_is_alive, ":enemies"),
					(agent_is_ally|neg, ":enemies"),
					(val_add, ":numenemies", 1),
				(try_end),
				(try_begin),
					(neg|gt, ":numenemies", 21), #InVain: Adjusted this to fit the bigger bodyguard
					(agent_set_slot, ":agent", 1, 2),
				#(else_try),
				#	
				(try_end),
			(else_try),
				(eq, ":slot1", 2),
				(store_random, ":rnd", 4),
				(try_begin),
					(neg|ge, ":rnd", 2),
					(entry_point_get_position, pos6, 31),
					(agent_set_scripted_destination, ":agent", pos6),
					(display_message, "@The_sorcerer_is_fleeing!_Kill_him!", 4294967040),
					(agent_set_slot, ":agent", 1, 3),
				(else_try),
					(ge, ":rnd", 2),
					(agent_clear_scripted_mode, ":agent"),
          (display_message, "@The_sorcerer_has_joined_the_fight!_Kill_him!", 4294967040),			  
					(agent_set_slot, ":agent", 1, 4),
				(try_end),
			(else_try),
				(eq, ":slot1", 3),
				(agent_get_position, pos7, ":agent"),
				(get_distance_between_positions, ":dist", pos6, pos7),
				(neg|ge, ":dist", 500),
				(display_message, "@The_sorcerer_has_fled!", 4294901760),
				(display_message, "@Report_this_ill_news_to_the_Lady_at_once.", 4294901760),
				(quest_set_slot,"qst_mirkwood_sorcerer",slot_quest_current_state,3),
				(call_script, "script_fail_quest","qst_mirkwood_sorcerer"),
				(agent_set_slot, ":agent", 1, 4),
				(set_mission_result, -1),
				(finish_mission),
			(try_end),
		(try_end)]),
	(2,0,0, [(neg|quest_slot_eq,"qst_mirkwood_sorcerer",slot_quest_current_state,2)],[
		  (try_for_agents, ":deadenemy"),
			(agent_is_human, ":deadenemy"),
			(agent_is_ally|neg, ":deadenemy"),
			(agent_is_alive|neg, ":deadenemy"),
			(agent_get_troop_id, ":troop", ":deadenemy"),
			(eq, ":troop", "trp_black_numenorean_sorcerer"),
			(quest_set_slot,"qst_mirkwood_sorcerer",slot_quest_current_state,2),
			(display_message, "@The_sorcerer_is_dead!", 4294967040),
			(call_script, "script_succeed_quest","qst_mirkwood_sorcerer"),
      (finish_mission,5), #InVain So you don't have to search for the remaining enemies once the sorcerer's dead																	   
			(eq,"$rescue_stage",1), #dummy usage of global var
		#    (scene_prop_get_instance, ":local1", [opmask_scene_prop]528, 0),
		#    (prop_instance_get_position, pos1, ":local1"),
		#    (copy_position, pos2, pos1),
		#    (position_move_z, pos2, -1500, 0),
		#    (prop_instance_animate_to_position, ":local1", pos2, pos1),
		  (try_end)]),
	(1,60, ti_once, [
		(store_mission_timer_a, ":time"),
		(ge, ":time", 10),
		(all_enemies_defeated),
		(neg|main_hero_fallen),
		(neg|quest_slot_eq,"qst_mirkwood_sorcerer",slot_quest_current_state,3),
		(assign, "$g_battle_result", 1),
		(assign, "$battle_won", 1),
		(set_mission_result, 1),
		(display_message, "@The battle is won!"),
		(call_script, "script_infiltration_mission_update_companion_casualties"),
		],[
		(quest_set_slot,"qst_mirkwood_sorcerer",slot_quest_current_state,2),
		(finish_mission)]),
	(ti_tab_pressed,0,0, [],[(try_begin),(eq, "$battle_won", 1),(finish_mission),(try_end)]),
	(ti_question_answered,0,0, [],[(store_trigger_param_1, ":local0"),(eq, ":local0", 0),(finish_mission)]),
]),
( "battle_wall_mission",mtf_battle_mode,0,
  "You_lead_your_men_to_battle.", [
	  ( 0,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  ( 1,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  ( 2,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  ( 3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  ( 4,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  ( 5,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  ( 6,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  ( 7,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  ( 8,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  ( 9,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  (10,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (11,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (12,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (13,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (14,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (15,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (16,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (17,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (18,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (19,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (20,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (21,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (22,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (23,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (24,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (25,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	  (26,mtef_visitor_source|mtef_team_2,af_override_horse,aif_start_alarmed,1,[]),
	],tld_common_wb_muddy_water+[
	(0,0,ti_once,[],[
		(call_script, "script_infiltration_mission_synch_agents_and_troops"),
		(call_script, "script_infiltration_mission_set_hit_points"),
		(call_script, "script_wounded_hero_cap_mission_health"),
		#(try_begin),(eq, "$active_rescue", 1),(play_sound, [opmask_sound]133, 0),
		# (else_try),(eq, "$active_rescue", 2),(play_sound, [opmask_sound]134, 0),
		# (else_try),(eq, "$active_rescue", 3),(play_sound, [opmask_sound]135, 0),
		# (else_try),(eq, "$active_rescue", 4),(play_sound, [opmask_sound]136, 0),
		#(try_end),
		]),

	(1,0,0,[],[(call_script, "script_infiltration_mission_update_companion_casualties")]),

	(1,4,ti_once,[(main_hero_fallen)],[
		(call_script, "script_rescue_failed"),
		(call_script, "script_infiltration_mission_update_companion_casualties"),
		(set_mission_result, -1),
		(finish_mission)]),

	(5,0,0,[(store_mission_timer_a, reg13),(ge, reg13, 60)],[
		(try_begin),
			(ge, "$meta_alarm", 8),
			(set_visitor, 20, "$wall_mounted_troop5", 0),
			(set_visitor, 21, "$wall_mounted_troop5", 0),
			(set_visitor, 22, "$wall_mounted_troop5", 0),
			(set_visitor, 19, "$wall_mounted_troop5", 0),
			(set_visitor, 18, "$wall_mounted_troop5", 0),
			(add_reinforcements_to_entry, 20, 1),
			(add_reinforcements_to_entry, 21, 1),
			(add_reinforcements_to_entry, 22, 1),
			(add_reinforcements_to_entry, 23, 1),
			(add_reinforcements_to_entry, 24, 1),
			(reset_mission_timer_a),
		(else_try),
			(neg|gt, "$meta_alarm", 7),
			(set_visitor, 20, "$wall_mounted_troop3", 0),
			(set_visitor, 21, "$wall_mounted_troop3", 0),
			(set_visitor, 22, "$wall_mounted_troop3", 0),
			(set_visitor, 19, "$wall_mounted_troop3", 0),
			(set_visitor, 18, "$wall_mounted_troop3", 0),
			(add_reinforcements_to_entry, 20, 1),
			(add_reinforcements_to_entry, 21, 1),
			(add_reinforcements_to_entry, 22, 1),
			(add_reinforcements_to_entry, 23, 1),
			(add_reinforcements_to_entry, 24, 1),
			(reset_mission_timer_a),
		(try_end)]),

	(ti_tab_pressed      ,0,0,[],[(try_begin),(eq, "$battle_won", 1),(finish_mission),(try_end)]),
	(ti_question_answered,0,0,[],[(store_trigger_param_1, ":local0"),(eq, ":local0", 0),(finish_mission)]),
]),

# Animal Ambushes (CppCoder)
("animal_ambush",mtf_battle_mode,charge,
 "You are ambushed by an animal.",
 [
	# Player
	(0,mtef_scene_source|mtef_team_0,0,0,1,[]),

	# Companions (Add more for more companions)
	(1,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(2,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(3,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(4,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(5,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(6,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(7,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(8,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(9,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(10,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(11,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(12,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(13,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(14,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(15,mtef_visitor_source|mtef_team_0,0,0,1,[]),
	(16,mtef_visitor_source|mtef_team_0,0,0,1,[]),

	# Enemies:
	(17,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(18,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(19,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(20,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(21,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(22,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(23,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(24,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(25,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(26,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(27,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(28,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(29,mtef_visitor_source|mtef_team_1,0,0,1,[]),
	(30,mtef_visitor_source|mtef_team_1,0,0,1,[]),

 ],
	# Triggers
  tld_common_wb_muddy_water+
	common_deathcam_triggers +
  moto_formations_triggers + 
  khams_custom_player_camera+
  fade+ [
	
  tld_animals_init,
	custom_warg_sounds,
	common_battle_on_player_down,

	# Make the teams enemies...
	(ti_before_mission_start, 0, 0, [], [(team_set_relation, 0, 1, -1),(assign, "$battle_won", 0)]),

	(0, 0, ti_once, 
	[
		#(str_store_troop_name, s1, reg20),
		#(display_message, "@DEBUG: Enemy to spawn: {s1}"),
		#(display_message, "@DEBUG: Enemies to spawn: {reg21}"),

		# Make enemies charge...
		(set_show_messages, 0),
			(team_give_order, 1, grc_everyone, mordr_charge),
		(set_show_messages, 1),
	], 
	[]),

	(1, 60, ti_once, 
	[
		(store_mission_timer_a,reg(1)),
		(ge,reg(1),10),
		(all_enemies_defeated, 5),
		(set_mission_result,1),
		(display_message,"str_msg_battle_won"),
		(assign,"$battle_won",1),
		(assign, "$g_battle_result", 1),
		(call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
	],
	[
		(finish_mission, 1)
	]),

	(ti_tab_pressed,0,0,[],
	[
		(try_begin),
			(eq, "$battle_won", 1),
			(jump_to_menu, "mnu_animal_ambush_success"),
			(finish_mission),
		(else_try),
			(main_hero_fallen),
			(jump_to_menu, "mnu_animal_ambush_fail"),
			(finish_mission),
		(try_end),
    # Apply health changes...
    (try_begin),
      (this_or_next|eq, "$battle_won", 1),
      (main_hero_fallen),
      (try_for_agents, ":agent"),
        (gt, ":agent",0),
        (agent_is_human, ":agent"),
        (agent_get_troop_id, ":troop", ":agent"),
        (troop_is_hero, ":troop"),
        (this_or_next|eq, ":troop", "trp_player"),
        (is_between, ":troop", companions_begin, companions_end),
        (store_agent_hit_points,":hp",":agent",0),
        (call_script, "script_get_max_skill_of_player_party", "skl_wound_treatment"),
        (store_mul, ":medic", reg0, 5),
        (val_add, ":hp", ":medic"),
        (val_clamp, ":hp", 0, 100),
        (troop_set_health, ":troop", ":hp"),
      (try_end),
    (try_end),
	]),

tld_animal_strikes,
tld_remove_riderless_animals,

]),

( "hunt_down_refugees",mtf_battle_mode,charge,
  "You attack the refugee train.",
  [(1,mtef_defenders|mtef_team_0,0,aif_start_alarmed,18,[]),(0,mtef_defenders|mtef_team_0,0,aif_start_alarmed,0,[]),
     (4,mtef_attackers|mtef_team_1,0,aif_start_alarmed,18,[]),(4,mtef_attackers|mtef_team_1,0,aif_start_alarmed,0,[]),
     (5,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 5th entry, for WARGS
     (6,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 6th entry, for WARGS
     (7,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 7th entry, for WARGS
     (8,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),  # this needs be the 8th entry, for WARGS
    ],
    tld_common_wb_muddy_water +
    formations_triggers + AI_triggers +   common_deathcam_triggers +  moto_formations_triggers +  tld_common_battle_scripts + command_cursor_sub_mod + [
  common_battle_tab_press,
  common_music_situation_update,
  (0,0,ti_once,[],[]),
  common_battle_check_friendly_kills,
  common_battle_check_victory_condition,
  common_battle_victory_display,
  common_battle_on_player_down,
  common_battle_inventory,
  (ti_question_answered, 0, 0, [],[
      (store_trigger_param_1,":answer"),
      (eq,":answer",0),
      (assign, "$pin_player_fallen", 0),
      (try_begin),
        (store_mission_timer_a, ":elapsed_time"),
        (gt, ":elapsed_time", 20),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 10, 20),
      (try_end),
      (call_script, "script_count_mission_casualties_from_agents"),
      (finish_mission,0)]),
  (ti_before_mission_start, 0, 0, [],[(team_set_relation, 0, 2, 1),(team_set_relation, 1, 3, 1), (team_set_relation, 0,4,-1), (team_set_relation, 1,4,-1),(call_script, "script_place_player_banner_near_inventory_bms")]),
  (0,0,ti_once,[],[
      (assign,"$battle_won",0),
      (assign,"$defender_reinforcement_stage",0),
      (assign,"$attacker_reinforcement_stage",0),
      (assign,"$g_presentation_battle_active", 0),
      (call_script, "script_place_player_banner_near_inventory"),
      (call_script, "script_combat_music_set_situation_with_culture"),
      # ambience sounds
      (try_begin),(is_currently_night),(play_sound, "$bs_night_sound", sf_looping),
       (else_try),           (play_sound, "$bs_day_sound",   sf_looping),
      (try_end),
      (get_player_agent_no, "$current_player_agent"),
      (agent_get_horse,"$horse_player","$current_player_agent"), #checks for horse lameness in mission
      (troop_get_inventory_slot_modifier,"$horse_mod","trp_player",8),
      ]),
  (1, 0, 5,  [
      (lt,"$defender_reinforcement_stage",8),
      (store_mission_timer_a,":mission_time"),
      (ge,":mission_time",10),
      (store_normalized_team_count,":num_defenders", 0),
      (lt,":num_defenders",10)
      ],[
      (add_reinforcements_to_entry,0,10),
      (val_add,"$defender_reinforcement_stage",1)]),
  (1, 0, 5, [
      (lt,"$attacker_reinforcement_stage",8),
      (store_mission_timer_a,":mission_time"),
      (ge,":mission_time",10),
      (store_normalized_team_count,":num_attackers", 1),
      (lt,":num_attackers",10)
      ],[
      (add_reinforcements_to_entry,3,10),]),

    (5, 0, ti_once, [
      (store_mission_timer_a, ":mission_time_a"),
      (store_random_in_range, ":ran_time", 45, 90),
      (ge, ":mission_time_a", ":ran_time"), #Random time between 45 - 90 secs

       (call_script, "script_find_theater", "p_main_party"),

      (assign, ":theater", reg0),
      (assign, ":interloper", 0),  #Interloper 0 = Default = Tribal Orcs
      (assign, ":interloper_1", "trp_tribal_orc_warrior"),
      (assign, ":interloper_2", "trp_tribal_orc"),

      (store_random_in_range, ":random", 0, 100),

      (store_character_level, ":player_level", "trp_player"),

      (try_begin),
        
        (assign, ":troll_chance", 10),
        (try_begin),
          (gt, ":player_level", 13),
          (assign, ":troll_chance",15),
        (try_end),

        (le, ":random", ":troll_chance"), #10-15% Chance it is a troll!
        (assign, ":interloper", 2), #Interloper 2 = Trolls
        (assign, ":interloper_1", "trp_troll_of_moria"),
        (assign, ":interloper_2", "trp_troll_of_moria"),
      
      (else_try),

        (assign, ":troop_chance", 45),
        (try_begin),
          (gt, ":player_level", 13),
          (assign, ":troop_chance",50),
        (try_end),

        (le, ":random", ":troop_chance"), #30-35% Chance 
        (try_begin),
          (store_random_in_range, ":ran_2", 0,100),
          (le, ":ran_2", 50),
          (assign, ":interloper", 1), #Interloper 1 = Evil Faction
          (try_begin),
            (eq, ":theater", theater_SE),
            (assign, ":interloper_1", "trp_warg_rider_of_gorgoroth"),
            (assign, ":interloper_2", "trp_orc_tracker_of_mordor"),
            (str_store_faction_name, s31, "fac_mordor"),
          (else_try),
            (eq, ":theater", theater_SW),
            (assign, ":interloper_1", "trp_warg_rider_of_isengard"),
            (assign, ":interloper_2", "trp_large_uruk_hai_tracker"),
            (str_store_faction_name, s31, "fac_isengard"),
          (else_try),
            (eq, ":theater", theater_C),
            (assign, ":interloper_1", "trp_warg_rider_gundabad"),
            (assign, ":interloper_2", "trp_warg_skirmisher_gundabad"),
            (str_store_faction_name, s31, "fac_gundabad"),
          (else_try),
            (assign, ":interloper_1", "trp_rhun_veteran_swift_horseman"),
            (assign, ":interloper_2", "trp_rhun_veteran_horse_archer"),
            (str_store_faction_name, s31, "fac_rhun"),
          (try_end),
        (else_try),
          (assign, ":interloper", 3), #Interloper 3 = Good Faction
          (try_begin),
            (eq, ":theater", theater_SE),
            (assign, ":interloper_1", "trp_squire_of_gondor"),
            (assign, ":interloper_2", "trp_gondor_swordsmen"),
            (str_store_faction_name, s31, "fac_gondor"),
          (else_try),
            (eq, ":theater", theater_SW),
            (assign, ":interloper_1", "trp_veteran_skirmisher_of_rohan"),
            (assign, ":interloper_2", "trp_squire_of_rohan"),
            (str_store_faction_name, s31, "fac_rohan"),
          (else_try),
            (eq, ":theater", theater_C),
            (assign, ":interloper_1", "trp_woodmen_skilled_forester"),
            (assign, ":interloper_2", "trp_woodmen_scout"),
            (str_store_faction_name, s31, "fac_beorn"),
          (else_try),
            (assign, ":interloper_1", "trp_laketown_scout"),
            (assign, ":interloper_2", "trp_dale_pikeman"),
            (str_store_faction_name, s31, "fac_dale"),
          (try_end),
        (try_end),
      (try_end), #50% chance for tribal orcs 

      (try_begin),
        (eq, ":interloper", 0),
        (assign, ":range_end", 30),
        (assign, ":team", 4),
        (display_message, "@A band of tribal orcs have appeared!", color_bad_news),
        (str_store_string, s30, "@Gaaaar!! We wants those human meat!"),
        (call_script, "script_troop_talk_presentation", ":interloper_1", 7, 0),
      (else_try),
        (eq, ":interloper", 1),
        (assign, ":range_end", 20),
        (assign, ":team", 4),
        (display_message, "@{s31} scouts have appeared!", color_bad_news),
        (str_store_string, s30, "@Those are ours! We have been tracking them since they left! No one stands in our way!"),
        (call_script, "script_troop_talk_presentation", ":interloper_1", 7, 0),
      (else_try),
        (eq, ":interloper", 2),
        (assign, ":range_end", 2),
        (assign, ":team", 4),
        (display_message, "@Trolls appeared!"),
        (str_store_string, s30, "@Gaaaar!!"),
        (call_script, "script_troop_talk_presentation", ":interloper_1", 7, 0),
      (else_try),
        (eq, ":interloper", 3),
        (assign, ":range_end", 20),
        (assign, ":team", 0),
        (display_message, "@{s31} scouts have appeared to aid the refugees!"),
        (str_store_string, s30, "@Hurry, men! Help the refugees! Kill all the scum and do not let them escape!"),
        (call_script, "script_troop_talk_presentation", ":interloper_1", 7, 0),
      (try_end),

      (get_player_agent_no, ":player"),
      (call_script, "script_find_exit_position_at_pos4", ":player"),
      (set_spawn_position, pos4), 

      (try_for_range, ":unused", 0, ":range_end"),
        (store_random_in_range, ":rnd_troop", 0,100),
        (le, ":rnd_troop", 50),
        (spawn_agent, ":interloper_1"),
        (agent_set_team, reg0, ":team"),
      (else_try),
        (spawn_agent, ":interloper_2"),
        (agent_set_team, reg0, ":team"),
      (try_end),

      (set_show_messages, 0),
      (team_give_order, ":team", grc_everyone, mordr_charge),
      (set_show_messages, 1),
      ],

      []
  ),

  #AI Triggers
  (0, 0, ti_once,[(this_or_next|eq, "$small_scene_used", 1), (eq, "$tld_option_formations", 0),(neq, "$tld_option_formations", 2),(store_mission_timer_a,":mission_time"),(ge,":mission_time",2)],[
      (call_script, "script_select_battle_tactic"),
      (call_script, "script_battle_tactic_init"),
      (try_begin),
        (eq, "$small_scene_used", 1),
        (neq, "$tld_option_formations", 2),
        (display_message, "@Battlefield is too small for complex AI formations.", message_neutral),
      (try_end)]),
  (5, 0, 0, [(this_or_next|eq, "$small_scene_used", 1), (eq, "$tld_option_formations", 0),(neq, "$tld_option_formations", 2),(store_mission_timer_a,":mission_time"),(ge,":mission_time",3),(call_script, "script_battle_tactic_apply")], []),
  common_battle_order_panel,
  common_battle_order_panel_tick,

]),

# Tutorial MTs

] + (is_a_wb_mt==1 and [

(
    "tutorial_1",0,-1,
    "You enter the training ground.",
    [
        (0,mtef_leader_only,af_override_horse|af_override_weapons,0,1,[itm_gon_jerkin,itm_gondor_light_greaves,itm_short_bow,itm_gondor_arrows,itm_gon_tab_shield_a,itm_gondor_short_sword,]), #af_override_weapons
     ], 
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_1_state", 5),
         (question_box, "str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message, "str_cant_use_inventory_tutorial")], []),

      (0, 0, ti_once, [(assign, "$tutorial_1_state", 0),
                       (assign, "$tutorial_1_msg_1_displayed", 0),
                       (assign, "$tutorial_1_msg_2_displayed", 0),
                       (assign, "$tutorial_1_msg_3_displayed", 0),
                       (assign, "$tutorial_1_msg_4_displayed", 0),
                       (assign, "$tutorial_1_msg_5_displayed", 0),
                       (assign, "$tutorial_1_msg_6_displayed", 0),
                       ], []),

      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_1_state", 0),
                   (try_begin),
                     (eq, "$tutorial_1_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_1_msg_1_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_1_msg_1"),
                     (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                     (entry_point_get_position,pos1,1),
                     (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (try_end),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_1_msg_1"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position,pos2,1),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 100),
                   (val_add, "$tutorial_1_state", 1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (entry_point_get_position,pos1,2),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_1_state", 1),
                   (try_begin),
                     (eq, "$tutorial_1_msg_2_displayed", 0),
                     (assign, "$tutorial_1_msg_2_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_1_msg_2"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position,pos2,2),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 100),
                   (val_add, "$tutorial_1_state", 1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, 90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (entry_point_get_position,pos1,3),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_1_state", 2),
                   (try_begin),
                     (eq, "$tutorial_1_msg_3_displayed", 0),
                     (assign, "$tutorial_1_msg_3_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_1_msg_3"),
                     (assign, "$tutorial_num_total_dummies_destroyed", 0),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (ge, "$tutorial_num_total_dummies_destroyed", 4),
                   (val_add, "$tutorial_1_state", 1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 2),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, 90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                 (else_try),
                   (eq, "$tutorial_1_state", 3),
                   (try_begin),
                     (eq, "$tutorial_1_msg_4_displayed", 0),
                     (assign, "$tutorial_1_msg_4_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_1_msg_4"),
                     (store_mission_timer_a, "$tutorial_time"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (store_mission_timer_a, ":cur_time"),
                   (val_sub, ":cur_time", "$tutorial_time"),
                   (gt, ":cur_time", 10),
                   (val_add, "$tutorial_1_state", 1),
                 (else_try),
                   (eq, "$tutorial_1_state", 4),
                   (try_begin),
                     (eq, "$tutorial_1_msg_5_displayed", 0),
                     (assign, "$tutorial_1_msg_5_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_1_msg_5"),
                     (assign, "$g_last_archery_point_earned", 0),
                     (assign, "$tutorial_num_arrows_hit", 0),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (try_begin),
                     (get_player_agent_no, ":player_agent"),
                     (agent_get_ammo, ":cur_ammo", ":player_agent"),
                     (le, ":cur_ammo", 0),
                     (agent_refill_ammo, ":player_agent"),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_ammo_refilled"),
                   (try_end),
                   (gt, "$g_last_archery_point_earned", 0),
                   (assign, "$g_last_archery_point_earned", 0),
                   (val_add, "$tutorial_num_arrows_hit", 1),
                   (gt, "$tutorial_num_arrows_hit", 2),
                   (val_add, "$tutorial_1_state", 1),
                 (else_try),
                   (eq, "$tutorial_1_state", 5),
                   (eq, "$tutorial_1_msg_6_displayed", 0),
                   (assign, "$tutorial_1_msg_6_displayed", 1),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_1_msg_6"),
                   (play_sound, "snd_tutorial_2"),
                   (assign, "$tutorial_1_finished", 1),
                 (try_end),
                 ], []),
    ] + fade,
  ),


  (
    "tutorial_2",mtf_arena_fight,-1,
    "You enter the training ground.",
    [
        (0,mtef_leader_only|mtef_team_0,af_override_horse|af_override_weapons,0,1,[itm_uruk_ragwrap,itm_isen_uruk_helm_a,itm_isen_uruk_light_a,itm_isen_uruk_shield_b]),
        (2,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
        (4,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
     ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_2_state", 9),
         (question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),
      (0, 0, ti_once, [
          (store_mission_timer_a, ":cur_time"),
          (gt, ":cur_time", 2),
          (main_hero_fallen),
          (assign, "$tutorial_2_state", 100),
        ], []),

      (0, 0, ti_once, [(assign, "$tutorial_2_state", 0),
                       (assign, "$tutorial_2_msg_1_displayed", 0),
                       (assign, "$tutorial_2_msg_2_displayed", 0),
                       (assign, "$tutorial_2_msg_3_displayed", 0),
                       (assign, "$tutorial_2_msg_4_displayed", 0),
                       (assign, "$tutorial_2_msg_5_displayed", 0),
                       (assign, "$tutorial_2_msg_6_displayed", 0),
                       (assign, "$tutorial_2_msg_7_displayed", 0),
                       (assign, "$tutorial_2_msg_8_displayed", 0),
                       (assign, "$tutorial_2_msg_9_displayed", 0),
                       (assign, "$tutorial_2_melee_agent_state", 0),
                       ], []),

      (10, 0, 0, [(call_script, "script_cf_get_first_agent_with_troop_id", "trp_squire_of_rohan"),
                  (agent_refill_ammo, reg0)], []),

      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_2_state", 0),
                   (try_begin),
                     (eq, "$tutorial_2_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_2_msg_1_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_2_msg_1"),
                     (team_give_order, 1, grc_everyone, mordr_stand_ground),
                     (team_give_order, 1, grc_infantry, mordr_charge),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_skirmisher_of_rohan"),
                     (assign, ":cur_agent", reg0),
                     (agent_get_position, pos1, ":cur_agent"),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position,pos2,1),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, 90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 1),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 0),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 2),
                   (try_begin),
                     (eq, "$tutorial_2_melee_agent_state", 0),
                     (val_add, "$tutorial_2_melee_agent_state", 1),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_squire_of_rohan"),
                     (assign, ":cur_agent", reg0),
                     (entry_point_get_position, pos1, 3),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (else_try),
                     (eq, "$tutorial_2_melee_agent_state", 1),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_squire_of_rohan"),
                     (assign, ":cur_agent", reg0),
                     (entry_point_get_position, pos1, 3),
                     (agent_get_position, pos2, ":cur_agent"),
                     (get_distance_between_positions, ":cur_distance", pos1, pos2),
                     (le, ":cur_distance", 250),
                     (agent_clear_scripted_mode, ":cur_agent"),
                     (val_add, "$tutorial_2_melee_agent_state", 1),
                     (store_mission_timer_a,"$tutorial_time"),
                   (else_try),
                     (eq, "$tutorial_2_melee_agent_state", 2),
                     (try_begin),
                       (eq, "$tutorial_2_msg_2_displayed", 0),
                       (assign, "$tutorial_2_msg_2_displayed", 1),
                       (play_sound, "snd_tutorial_1"),
                     (try_end),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_squire_of_rohan"),
                     (assign, ":cur_agent", reg0),
                     (store_mission_timer_a,":cur_time"),
                     (val_sub, ":cur_time", "$tutorial_time"),
                     (store_sub, reg3, 20, ":cur_time"),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_2_msg_2"),
                     (gt, ":cur_time", 20),
                     (entry_point_get_position, pos1, 3),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (val_add, "$tutorial_2_melee_agent_state", 1),
                   (else_try),
                     (eq, "$tutorial_2_melee_agent_state", 3),
                     (try_begin),
                       (eq, "$tutorial_2_msg_3_displayed", 0),
                       (assign, "$tutorial_2_msg_3_displayed", 1),
                       (tutorial_message_set_background, 1),
                       (tutorial_message, "str_tutorial_2_msg_3"),
                       (play_sound, "snd_tutorial_1"),
                     (try_end),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_squire_of_rohan"),
                     (assign, ":cur_agent", reg0),
                     (entry_point_get_position, pos1, 3),
                     (agent_get_position, pos2, ":cur_agent"),
                     (get_distance_between_positions, ":cur_distance", pos1, pos2),
                     (le, ":cur_distance", 250),
                     (entry_point_get_position, pos1, 2),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (val_add, "$tutorial_2_melee_agent_state", 1),
                   (else_try),
                     (eq, "$tutorial_2_melee_agent_state", 4),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_squire_of_rohan"),
                     (assign, ":cur_agent", reg0),
                     (entry_point_get_position, pos1, 2),
                     (agent_get_position, pos2, ":cur_agent"),
                     (get_distance_between_positions, ":cur_distance", pos1, pos2),
                     (le, ":cur_distance", 250),
                     (entry_point_get_position, pos1, 30),
                     (agent_set_position, ":cur_agent", pos1),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 1),
                     (prop_instance_get_position, pos1, ":door_object"),
                     #(position_rotate_z, pos1, 90),
                     (position_move_z,pos1,400),
                     (prop_instance_animate_to_position, ":door_object", pos1, 150),
                     (val_add, "$tutorial_2_melee_agent_state", 1),
                     (val_add, "$tutorial_2_state", 1),
                   (try_end),
                 (else_try),
                   (eq, "$tutorial_2_state", 3),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 1),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (store_mission_timer_a,"$tutorial_time"),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 4),
                   (try_begin),
                     (eq, "$tutorial_2_msg_4_displayed", 0),
                     (assign, "$tutorial_2_msg_4_displayed", 1),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (store_mission_timer_a,":cur_time"),
                   (val_sub, ":cur_time", "$tutorial_time"),
                   (store_sub, reg3, 20, ":cur_time"),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_2_msg_4"),
                   (gt, ":cur_time", 20),
                   (entry_point_get_position,pos1,5),
                   (set_spawn_position, pos1),
                   (spawn_item, "itm_isengard_sword"),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_squire_of_rohan"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 3),
                   (agent_set_position, ":cur_agent", pos1),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 2),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, 90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 5),
                   (try_begin),
                     (eq, "$tutorial_2_msg_5_displayed", 0),
                     (assign, "$tutorial_2_msg_5_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_2_msg_5"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 2),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 2),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 6),
                   (try_begin),
                     (eq, "$tutorial_2_msg_6_displayed", 0),
                     (assign, "$tutorial_2_msg_6_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_2_msg_6"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_has_item_equipped, ":player_agent", "itm_isengard_sword"),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 3),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 7),
                   (try_begin),
                     (eq, "$tutorial_2_msg_7_displayed", 0),
                     (assign, "$tutorial_2_msg_7_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_2_msg_7"),
                     (play_sound, "snd_tutorial_1"),
                     (get_player_agent_no, ":player_agent"),
                     (agent_set_hit_points, ":player_agent", 100),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_skirmisher_of_rohan"),
                   (assign, ":cur_agent", reg0),
                   (neg|agent_is_alive, ":cur_agent"),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_squire_of_rohan"),
                   (assign, ":cur_agent", reg0),
                   (agent_clear_scripted_mode, ":cur_agent"),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 4),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 8),
                   (try_begin),
                     (eq, "$tutorial_2_msg_8_displayed", 0),
                     (assign, "$tutorial_2_msg_8_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_2_msg_8"),
                     (play_sound, "snd_tutorial_1"),
                     (get_player_agent_no, ":player_agent"),
                     (agent_set_hit_points, ":player_agent", 100),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_squire_of_rohan"),
                   (assign, ":cur_agent", reg0),
                   (neg|agent_is_alive, ":cur_agent"),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 9),
                   (eq, "$tutorial_2_msg_9_displayed", 0),
                   (assign, "$tutorial_2_msg_9_displayed", 1),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_2_msg_9"),
                   (play_sound, "snd_tutorial_2"),
                   (assign, "$tutorial_2_finished", 1),
                 (else_try),
                   (gt, "$tutorial_2_state", 30),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_failed"),
                 (try_end),
                 ], []),
    ] + fade,
  ),

  (
    "tutorial_3",mtf_arena_fight,-1,
    "You enter the training ground.",
    [
        (0,mtef_leader_only|mtef_team_0,af_override_horse|af_override_weapons,0,1,[itm_beorn_padded,itm_rohan_shoes,]),
        (3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
        (5,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_3_state", 12),
         (question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),

      (0, 0, ti_once, [
          (store_mission_timer_a, ":cur_time"),
          (gt, ":cur_time", 2),
          (main_hero_fallen),
          (assign, "$tutorial_3_state", 100),
        ], []),

      (ti_before_mission_start, 0, ti_once, [(assign, "$tutorial_3_state", 0),
                       (assign, "$tutorial_3_msg_1_displayed", 0),
                       (assign, "$tutorial_3_msg_2_displayed", 0),
                       (assign, "$tutorial_3_msg_3_displayed", 0),
                       (assign, "$tutorial_3_msg_4_displayed", 0),
                       (assign, "$tutorial_3_msg_5_displayed", 0),
                       (assign, "$tutorial_3_msg_6_displayed", 0),
                       ], []),

      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_3_state", 0),
                   (try_begin),
                     (eq, "$tutorial_3_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_3_msg_1_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_3_msg_1"),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_orc_of_mordor"),
                     (assign, ":cur_agent", reg0),
                     (agent_get_position, pos1, ":cur_agent"),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_black_numenorean_veteran_warrior"),
                     (assign, ":cur_agent", reg0),
                     (agent_get_position, pos1, ":cur_agent"),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (entry_point_get_position, pos1, 1),
                     (set_spawn_position, pos1),
                   (spawn_item, "itm_beorn_axe_no_attack"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_has_item_equipped, ":player_agent", "itm_beorn_axe_no_attack"),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 1),
                   (try_begin),
                     (eq, "$tutorial_3_msg_2_displayed", 0),
                     (assign, "$tutorial_3_msg_2_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_3_msg_2"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position,pos2,2),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 2),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 0),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, 90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 3),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_orc_of_mordor"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 4),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 4),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_orc_of_mordor"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 4),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (agent_clear_scripted_mode, ":cur_agent"),
                   (val_add, "$tutorial_3_state", 1),
                   (store_mission_timer_a,"$tutorial_time"),
                 (else_try),
                   (eq, "$tutorial_3_state", 5),
                   (try_begin),
                     (eq, "$tutorial_3_msg_3_displayed", 0),
                     (assign, "$tutorial_3_msg_3_displayed", 1),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_orc_of_mordor"),
                   (assign, ":cur_agent", reg0),
                   (store_mission_timer_a,":cur_time"),
                   (val_sub, ":cur_time", "$tutorial_time"),
                   (store_sub, reg3, 30, ":cur_time"),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_3_msg_3"),
                   (gt, ":cur_time", 30),
                   (entry_point_get_position, pos1, 4),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 6),
                   (try_begin),
                     (eq, "$tutorial_3_msg_4_displayed", 0),
                     (assign, "$tutorial_3_msg_4_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_3_msg_4"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_orc_of_mordor"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 4),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (entry_point_get_position, pos1, 3),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 7),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_orc_of_mordor"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 3),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (entry_point_get_position, pos1, 7),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (agent_set_position, ":cur_agent", pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
           (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 3),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
           (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 8),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 1),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, 90),
           (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 9),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_black_numenorean_veteran_warrior"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 6),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 10),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_black_numenorean_veteran_warrior"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 6),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (agent_clear_scripted_mode, ":cur_agent"),
                   (val_add, "$tutorial_3_state", 1),
                   (store_mission_timer_a,"$tutorial_time"),
                 (else_try),
                   (eq, "$tutorial_3_state", 11),
                   (try_begin),
                     (eq, "$tutorial_3_msg_5_displayed", 0),
                     (assign, "$tutorial_3_msg_5_displayed", 1),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_black_numenorean_veteran_warrior"),
                   (assign, ":cur_agent", reg0),
                   (store_mission_timer_a,":cur_time"),
                   (val_sub, ":cur_time", "$tutorial_time"),
                   (store_sub, reg3, 30, ":cur_time"),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_3_msg_5"),
                   (gt, ":cur_time", 30),
                   (entry_point_get_position, pos1, 6),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 12),
                   (try_begin),
                     (eq, "$tutorial_3_msg_6_displayed", 0),
                     (assign, "$tutorial_3_msg_6_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_3_msg_6"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_black_numenorean_veteran_warrior"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 6),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (entry_point_get_position, pos1, 5),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 13),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_black_numenorean_veteran_warrior"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 5),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (entry_point_get_position, pos1, 7),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (agent_set_position, ":cur_agent", pos1),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (gt, "$tutorial_3_state", 30),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_failed"),
                 (try_end),
                 ], []),
    ]+ fade,
  ),

  (
    "tutorial_3_2",mtf_arena_fight,-1,
    "You enter the training ground.",
    [
      (0,mtef_leader_only|mtef_team_0,af_override_horse|af_override_weapons,0,1,[itm_beorn_axe,itm_beorn_padded,itm_rohan_shoes,]),
      (4,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
    ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_3_state", 5),
         (question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),

      (0, 0, ti_once, [
          (store_mission_timer_a, ":cur_time"),
          (gt, ":cur_time", 2),
          (main_hero_fallen),
          (assign, "$tutorial_3_state", 100),
        ], []),


      (0, 0, ti_once, [(assign, "$tutorial_3_state", 0),
                       (assign, "$tutorial_3_msg_1_displayed", 0),
                       (assign, "$tutorial_3_msg_2_displayed", 0),
                       (assign, "$tutorial_3_msg_3_displayed", 0),
                       (assign, "$tutorial_3_msg_4_displayed", 0),
                       (assign, "$tutorial_3_msg_5_displayed", 0),
                       ], []),

      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_3_state", 0),
                   (try_begin),
                     (eq, "$tutorial_3_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_3_msg_1_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_3_2_msg_1"),
                     (play_sound, "snd_tutorial_1"),
                     (call_script, "script_cf_get_first_agent_with_troop_id","trp_orc_of_mordor"),
                     (assign, ":cur_agent", reg0),
                     (agent_get_position, pos1, ":cur_agent"),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_black_numenorean_veteran_warrior"),
                     (assign, ":cur_agent", reg0),
                     (agent_get_position, pos1, ":cur_agent"),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position,pos2,2),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 1),
                   (try_begin),
                     (eq, "$tutorial_3_msg_2_displayed", 0),
                     (assign, "$tutorial_3_msg_2_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_3_2_msg_2"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 0),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, 90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_orc_of_mordor"),
                   (agent_clear_scripted_mode, reg0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 2),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_orc_of_mordor"),
                   (neg|agent_is_alive, reg0),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 3),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, -90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 3),
                   (try_begin),
                     (eq, "$tutorial_3_msg_3_displayed", 0),
                     (assign, "$tutorial_3_msg_3_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_3_2_msg_3"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 1),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   #(position_rotate_z, pos1, 90),
                   (position_move_z,pos1,400),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_black_numenorean_veteran_warrior"),
                   (agent_clear_scripted_mode, reg0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 4),
                   (try_begin),
                     (eq, "$tutorial_3_msg_4_displayed", 0),
                     (assign, "$tutorial_3_msg_4_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_3_2_msg_4"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_black_numenorean_veteran_warrior"),
                   (neg|agent_is_alive, reg0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 5),
                   (eq, "$tutorial_3_msg_5_displayed", 0),
                   (assign, "$tutorial_3_msg_5_displayed", 1),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_3_2_msg_5"),
                   (play_sound, "snd_tutorial_2"),
                   (assign, "$tutorial_3_finished", 1),
                 (else_try),
                   (gt, "$tutorial_3_state", 30),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_failed"),
                 (try_end),
                 ], []),
    ]+ fade,
  ),

  (
    "tutorial_4",mtf_arena_fight,-1,
    "You enter the training ground.",
    [
      (0,mtef_leader_only|mtef_team_0,af_override_horse|af_override_weapons,0,1,[itm_orc_scimitar,itm_gundabad_helm_b,itm_gundabad_armor_b,itm_orc_shield_b,itm_orc_bow,itm_orc_hook_arrow,]), #af_override_weapons
    ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_4_state", 11),
         (question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),

      (ti_before_mission_start, 0, ti_once, [(assign, "$tutorial_4_state", 0),
                       (assign, "$tutorial_4_msg_1_displayed", 0),
                       (assign, "$tutorial_4_msg_2_displayed", 0),
                       (assign, "$tutorial_4_msg_3_displayed", 0),
                       (assign, "$tutorial_4_msg_4_displayed", 0),
                       (assign, "$tutorial_4_msg_5_displayed", 0),
                       (assign, "$tutorial_4_msg_6_displayed", 0),
                       (assign, "$tutorial_4_msg_7_displayed", 0),
                       (scene_set_day_time, 15),
                       (store_random_in_range, ":rand", 35, 50),
                       (set_global_cloud_amount, ":rand"),
                       ], []),

      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_4_state", 0),
                   (try_begin),
                     (eq, "$tutorial_4_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_4_msg_1_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_4_msg_1"),
                     (entry_point_get_position, pos1, 1),
                     (set_spawn_position, 1),
           (spawn_horse, "itm_warg_1c"),
                     (assign, "$tutorial_num_total_dummies_destroyed", 0),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_horse, ":horse_agent", ":player_agent"),
                   (ge, ":horse_agent", 0),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 2),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 1),
                   (try_begin),
                     (eq, "$tutorial_4_msg_2_displayed", 0),
                     (assign, "$tutorial_4_msg_2_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_4_msg_2"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 2),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 3),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 2),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 3),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 4),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 3),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 4),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 5),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 4),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 5),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 6),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 5),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 6),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 1),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 6),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 1),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 7),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 7),
                   (try_begin),
                     (eq, "$tutorial_4_msg_3_displayed", 0),
                     (assign, "$tutorial_4_msg_3_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_4_msg_3"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 7),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 20),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 8),
                   (try_begin),
                     (eq, "$tutorial_4_msg_4_displayed", 0),
                     (assign, "$tutorial_4_msg_4_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_4_msg_4"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (ge, "$tutorial_num_total_dummies_destroyed", 2),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 8),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 9),
                   (try_begin),
                     (eq, "$tutorial_4_msg_5_displayed", 0),
                     (assign, "$tutorial_4_msg_5_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_4_msg_5"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 8),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 20),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 10),
                   (try_begin),
                     (eq, "$tutorial_4_msg_6_displayed", 0),
                     (assign, "$tutorial_4_msg_6_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_4_msg_6"),
                     (play_sound, "snd_tutorial_1"),
                     (assign, "$g_last_archery_point_earned", 0),
                     (assign, "$tutorial_num_arrows_hit", 0),
                   (try_end),
                   (try_begin),
                     (get_player_agent_no, ":player_agent"),
                     (agent_get_ammo, ":cur_ammo", ":player_agent"),
                     (le, ":cur_ammo", 0),
                     (agent_refill_ammo, ":player_agent"),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_ammo_refilled"),
                   (try_end),
                   (gt, "$g_last_archery_point_earned", 0),
                   (assign, "$g_last_archery_point_earned", 0),
                   (val_add, "$tutorial_num_arrows_hit", 1),
                   (gt, "$tutorial_num_arrows_hit", 2),
                   (val_add, "$tutorial_4_state", 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 11),
                   (eq, "$tutorial_4_msg_7_displayed", 0),
                   (assign, "$tutorial_4_msg_7_displayed", 1),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_4_msg_7"),
                   (play_sound, "snd_tutorial_2"),
                   (assign, "$tutorial_4_finished", 1),
                 (try_end),
                 ], []),
    ] + fade,
  ),

  (
    "tutorial_5",mtf_arena_fight,-1,
    "You enter the training ground.",
    [
        (0,mtef_leader_only|mtef_team_0,af_override_horse,0,1,[]),
        (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (13,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,10,[]),
        (14,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,10,[]),
        (15,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,10,[]),
        (16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,10,[]),
    ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_5_state", 5),
         (question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),


      (0, 0, 0,
        [
          (call_script, "script_iterate_pointer_arrow"),
          ], []),

      (0, 0, ti_once, [
          (store_mission_timer_a, ":cur_time"),
          (gt, ":cur_time", 2),
          (main_hero_fallen),
          (assign, "$tutorial_5_state", 100),
        ], []),

      (ti_before_mission_start, 0, ti_once, [(assign, "$tutorial_5_state", 0),
                       (assign, "$tutorial_5_msg_1_displayed", 0),
                       (assign, "$tutorial_5_msg_2_displayed", 0),
                       (assign, "$tutorial_5_msg_3_displayed", 0),
                       (assign, "$tutorial_5_msg_4_displayed", 0),
                       (assign, "$tutorial_5_msg_5_displayed", 0),
                       (assign, "$tutorial_5_msg_6_displayed", 0),
                       (assign, "$g_pointer_arrow_height_adder", -1000),
                       (scene_set_day_time, 16),
                       (store_random_in_range, ":rand", 10, 30),
                       (set_global_cloud_amount, ":rand"),
                       ], []),

      (0, 0, ti_once, [(set_show_messages, 0),
                       (team_give_order, 0, grc_everyone, mordr_stand_ground),
                       (set_show_messages, 1),
                       (store_mission_timer_a, ":cur_time"),
                       (gt, ":cur_time", 3),
                       ], []),

      (0, 0, 0, [(call_script, "script_cf_turn_windmill_fans", 0)], []),

      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_5_state", 0),
                   (try_begin),
                     (eq, "$tutorial_5_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_5_msg_1_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_5_msg_1"),
                     (entry_point_get_position, pos1, 5),
                     (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                     (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                     (scene_prop_get_instance, ":pointer_instance", "spr_pointer_arrow", 0),
                     (prop_instance_set_position, ":pointer_instance", pos1),
                     (assign, "$g_pointer_arrow_height_adder", 200),
                   (try_end),
                   (call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", 0, grc_infantry),
                   (entry_point_get_position, pos2, 5),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 1000),
                   (val_add, "$tutorial_5_state", 1),
                   (entry_point_get_position, pos1, 6),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_red", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (scene_prop_get_instance, ":pointer_instance", "spr_pointer_arrow", 0),
                   (prop_instance_set_position, ":pointer_instance", pos1),
                   (assign, "$g_pointer_arrow_height_adder", 200),
                 (else_try),
                   (eq, "$tutorial_5_state", 1),
                   (try_begin),
                     (eq, "$tutorial_5_msg_2_displayed", 0),
                     (assign, "$tutorial_5_msg_2_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_5_msg_2"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", 0, grc_infantry),
                   (entry_point_get_position, pos2, 5),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 1000),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 6),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 1000),
                   (val_add, "$tutorial_5_state", 1),
                   (entry_point_get_position, pos1, 7),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0), #Windmill to grab archers
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (scene_prop_get_instance, ":pointer_instance", "spr_pointer_arrow", 0),
                   (prop_instance_set_position, ":pointer_instance", pos1),
                   (assign, "$g_pointer_arrow_height_adder", 200),
                   (entry_point_get_position, pos1, 30),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_red", 0), #Hides the flag
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_5_state", 2),
                   (try_begin),
                     (eq, "$tutorial_5_msg_3_displayed", 0),
                     (assign, "$tutorial_5_msg_3_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_5_msg_3"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 7),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 500),
                   (val_add, "$tutorial_5_state", 1),
                   (modify_visitors_at_site,"scn_tutorial_5"),
                   (reset_visitors),
                   (set_visitors,5,"trp_rivendell_scout",2),
                   (set_visitors,6,"trp_rivendell_scout",3),
                   (set_visitors,7,"trp_rivendell_veteran_scout",3),
                   (entry_point_get_position, pos1, 11),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (entry_point_get_position, pos1, 12),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_red", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (scene_prop_get_instance, ":pointer_instance", "spr_pointer_arrow", 0),
                   (prop_instance_set_position, ":pointer_instance", pos1),
                   (assign, "$g_pointer_arrow_height_adder", 200),
                   (set_show_messages, 0),
                   (team_give_order, 0, grc_archers, mordr_stand_ground),
                   (set_show_messages, 1),
                 (else_try),
                   (eq, "$tutorial_5_state", 3),
                   (try_begin),
                     (eq, "$tutorial_5_msg_4_displayed", 0),
                     (assign, "$tutorial_5_msg_4_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_5_msg_4"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", 0, grc_archers),
                   (entry_point_get_position, pos2, 11), #Yellow flag
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 1000),
                   (call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", 0, grc_infantry),
                   (entry_point_get_position, pos2, 12), #Red Flag
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 1000),
                   (val_add, "$tutorial_5_state", 1),
                   (entry_point_get_position, pos1, 30),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0), #Hide
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_red", 0), #Hide
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (scene_prop_get_instance, ":pointer_instance", "spr_pointer_arrow", 0), #Hide
                   (prop_instance_set_position, ":pointer_instance", pos1),
                   (modify_visitors_at_site,"scn_tutorial_5"),
                   (reset_visitors),
                   (set_visitors,8,"trp_khand_glaive_whirler", 5),
                   (set_visitors,9,"trp_easterling_axeman", 5),
                   (set_visitors,10,"trp_variag_pitfighter", 5),
                   (set_visitors,11,"trp_variag_pitfighter", 5),
                   (team_give_order, 1, grc_everyone, mordr_charge),
                 (else_try),
                   (eq, "$tutorial_5_state", 4),
                   (try_begin),
                     (eq, "$tutorial_5_msg_5_displayed", 0),
                     (assign, "$tutorial_5_msg_5_displayed", 1),
                     (tutorial_message_set_background, 1),
                     (tutorial_message, "str_tutorial_5_msg_5"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (assign, ":enemy_count", 0),
                   (try_for_agents, ":cur_agent"),
                     (agent_is_human, ":cur_agent"),
                     (agent_is_alive, ":cur_agent"),
                     (agent_get_team, ":cur_team", ":cur_agent"),
                     (eq, ":cur_team", 1),
                     (val_add, ":enemy_count", 1),
                   (try_end),
                   (eq, ":enemy_count", 0),
                   (val_add, "$tutorial_5_state", 1),
                 (else_try),
                   (eq, "$tutorial_5_state", 5),
                   (eq, "$tutorial_5_msg_6_displayed", 0),
                   (assign, "$tutorial_5_msg_6_displayed", 1),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_5_msg_6"),
                   (play_sound, "snd_tutorial_2"),
                   (assign, "$tutorial_5_finished", 1),
                 (else_try),
                   (gt, "$tutorial_5_state", 30),
                   (tutorial_message_set_background, 1),
                   (tutorial_message, "str_tutorial_failed"),
                   (entry_point_get_position, pos1, 30),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_red", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (try_end),
                 ], []),
    ] + fade,

  ),

 ### kham alternate Training START
  (
    "alternate_training",mtf_arena_fight|mtf_commit_casualties,-1,
    "You begin your training.",
    [
      (0,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (1,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (2,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (3,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      # Player
      (4,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      # Opponents
      (5,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (6,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (7,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (8,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),

    ], tld_common_wb_muddy_water+
    [
      common_inventory_not_available,
      tld_cheer_on_space_when_battle_over_press,
      tld_cheer_on_space_when_battle_over_release,
      (ti_tab_pressed, 0, 0, [(display_message, "@Cannot leave")], []),
      (ti_before_mission_start, 0, 0, [], [(assign, "$g_arena_training_kills", 0),]),
      
      (0, 0, ti_once, [],
        [
          (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
      ]),
      
      (1, 4, ti_once, [
          (this_or_next|main_hero_fallen),
          (num_active_teams_le,1)],
        [
          (get_player_agent_no, ":player_agent"),
          (agent_get_kill_count, "$g_arena_training_kills", ":player_agent", 1),
          (finish_mission),
      ]),
    ],
  ),
  ### Kham Freelancer Training END  

] or []) + [ 

] + mission_templates_cutscenes
