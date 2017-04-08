from header_common import *
from header_operations import *
from header_mission_templates import *
from module_constants import *

## MadVader Warband deathcam begin

## cpp: Currently you can move outside of the boundries. TODO: Fix it. :)

common_init_deathcam_wb = (0, 0, ti_once, [],
[
  (assign, "$tld_camera_on", 0),
  
  # mouse center coordinates (non-windowed)
  (assign, "$tld_camera_mouse_center_x", 500),
  (assign, "$tld_camera_mouse_center_y", 375),
  # last recorded mouse coordinates
  (assign, "$tld_camera_mouse_x", "$tld_camera_mouse_center_x"),
  (assign, "$tld_camera_mouse_y", "$tld_camera_mouse_center_y"),
  # counts how many cycles the mouse stays in the same position, to determine new center in windowed mode
  (assign, "$tld_camera_mouse_counter", 0),
])

common_start_deathcam_wb = (0, 4, ti_once, # 4 seconds delay before the camera activates
[
  (main_hero_fallen),
  (eq, "$tld_camera_on", 0)
],
[
  (get_player_agent_no,      ":player_agent"),
  (agent_get_position, pos1, ":player_agent"),
  (position_get_x, ":pos_x", pos1),
  (position_get_y, ":pos_y", pos1),
  
  (init_position,   pos47),
  (position_set_x,  pos47, ":pos_x"),
  (position_set_y,  pos47, ":pos_y"),
  (position_set_z_to_ground_level, pos47),
  (position_move_z, pos47, 250),
  
  (mission_cam_set_mode, 1, 0, 0),
  (mission_cam_set_position, pos47),
  
  (assign, "$tld_camera_rotx", 0),
  
  #swy-- mark camera as initialized...
  (assign, "$tld_camera_on", 1)
])

common_move_deathcam_wb = (0, 0, 0,
[
  (eq, "$tld_camera_on", 1),
  (this_or_next|game_key_clicked, gk_move_forward),
  (this_or_next|game_key_is_down, gk_move_forward),
  
  (this_or_next|game_key_clicked, gk_move_backward),
  (this_or_next|game_key_is_down, gk_move_backward),
  
  (this_or_next|game_key_clicked, gk_move_left),
  (this_or_next|game_key_is_down, gk_move_left),

  (this_or_next|game_key_clicked, gk_move_right),
  (             game_key_is_down, gk_move_right),
],
[
  (mission_cam_get_position, pos47),
  
  (assign, ":move_x", 0),
  (assign, ":move_y", 0),
  
  (try_begin), #forward
    (this_or_next|game_key_clicked, gk_move_forward),
    (             game_key_is_down, gk_move_forward),
    (assign, ":move_y", 10),
  (try_end),
  (try_begin), #backward
    (this_or_next|game_key_clicked, gk_move_backward),
    (             game_key_is_down, gk_move_backward),
    (assign, ":move_y", -10),
  (try_end),
  (try_begin), #left
    (this_or_next|game_key_clicked, gk_move_left),
    (             game_key_is_down, gk_move_left),
    (assign, ":move_x", -10),
  (try_end),
  (try_begin), #right
    (this_or_next|game_key_clicked, gk_move_right),
    (             game_key_is_down, gk_move_right),
    (assign, ":move_x", 10),
  (try_end),
  
  (position_move_x, pos47, ":move_x"),
  (position_move_y, pos47, ":move_y"),
  
  (mission_cam_set_position, pos47),   
])

# set this to a positive number
# (MV: 2 or 3 works well for me, but needs testing on other people's PCs)
deathcam_wb_mouse_deadzone = 2

common_rotate_deathcam_wb = (0, 0, 0,
[
  (eq, "$tld_camera_on", 1),
  (neg|is_presentation_active, "prsnt_battle"),
  
  (mouse_get_position, pos1),
  (set_fixed_point_multiplier, 1000),
  
  (position_get_x, reg1, pos1),
  (position_get_y, reg2, pos1),
  
  (this_or_next|neq, reg1, "$tld_camera_mouse_center_x"),
  (             neq, reg2, "$tld_camera_mouse_center_y"),
],
[
  # fix for windowed mode: recenter the mouse
  (assign, ":continue", 1),
  (try_begin),
    (eq, reg1, "$tld_camera_mouse_x"),
    (eq, reg2, "$tld_camera_mouse_y"),
    (val_add,  "$tld_camera_mouse_counter", 1),
    (try_begin), #hackery: if the mouse hasn't moved for X cycles, recenter it
      (    gt, "$tld_camera_mouse_counter", 50),
      (assign, "$tld_camera_mouse_center_x", reg1),
      (assign, "$tld_camera_mouse_center_y", reg2),
      (assign, "$tld_camera_mouse_counter", 0),
    (try_end),
    (assign, ":continue", 0),
  (try_end),
  (eq, ":continue", 1), #continue only if mouse has moved
  (assign, "$tld_camera_mouse_counter", 0), # reset recentering hackery
 
  # update recorded mouse position
  (assign, "$tld_camera_mouse_x", reg1),
  (assign, "$tld_camera_mouse_y", reg2),
 
  (mission_cam_get_position, pos47),
  (store_sub, ":shift",                "$tld_camera_mouse_center_x", reg1), #horizontal shift for pass 0
  (store_sub, ":shift_vertical", reg2, "$tld_camera_mouse_center_y"),       #for pass 1
 
 
 #pass 0: check mouse x movement (left/right),
 #pass 1: check mouse y movement (up/down)
  (try_for_range, ":pass", 0, 2),
    (try_begin),
      #get ready for the second pass
      (eq, ":pass", 1),
      (assign, ":shift", ":shift_vertical"),
    (try_end),
    
    #skip pass if not needed (mouse deadzone)
    (this_or_next|lt, ":shift", -deathcam_wb_mouse_deadzone),
    (             gt, ":shift",  deathcam_wb_mouse_deadzone),
   
    (assign, ":sign", 1),
    (try_begin),
      (    lt, ":shift", 0),
      (assign, ":sign", -1),
    (try_end),
    
    # square root calc
    (val_abs, ":shift"),
    # ":shift" is now 1 or greater
    (val_sub, ":shift", deathcam_wb_mouse_deadzone),
    (convert_to_fixed_point,  ":shift"),
    (store_sqrt,    ":shift", ":shift"),
    (convert_from_fixed_point,":shift"),
    #limit rotation speed
    (val_clamp, ":shift", 1, 6),
    (val_mul, ":shift", ":sign"),
    
    (try_begin),
      # rotate around z (left/right)
      (eq, ":pass", 0),
      (store_mul, ":minusrotx", "$tld_camera_rotx", -1),
      #needed so camera yaw won't change
      (position_rotate_x, pos47, ":minusrotx"),
      (position_rotate_z, pos47, ":shift"),
      #needed so camera yaw won't change
      (position_rotate_x, pos47, "$tld_camera_rotx"),
    (try_end),
    
    (try_begin),
      # rotate around x (up/down)
      (eq, ":pass", 1),
      (position_rotate_x, pos47, ":shift"),
      (val_add, "$tld_camera_rotx", ":shift"),
    (try_end),
  (try_end), # <-try_for_range ":pass"
  
  #swy-- set final rotation
  (mission_cam_set_position, pos47),
])

## MadVader Warband deathcam end

#### Kham - Improved Field AI (Credit: Caba'drin PBOD & Diplomacy - Modified for TLD) START

##diplomacy begin
from header_skills import *

dplmc_horse_speed = (  #called in field_ai_triggers
  1, 0, 0, [],
  [  
  (try_for_agents, ":agent_no"),
    (agent_is_alive, ":agent_no"),
    (agent_is_human, ":agent_no"),
    (agent_get_horse, ":horse_agent", ":agent_no"),
    (try_begin),
      (ge, ":horse_agent", 0),
      (store_agent_hit_points, ":horse_hp",":horse_agent"),
      (store_sub, ":lost_hp", 100, ":horse_hp"),
      (try_begin),
        (le, ":lost_hp", 15),
        (val_div, ":lost_hp", 2),
        (store_add, ":speed_factor", 100, ":lost_hp"),
      (else_try),
        (val_mul, ":lost_hp", 2),
        (val_div, ":lost_hp", 3),
        (store_sub, ":speed_factor", 115, ":lost_hp"),
      (try_end),
      (agent_get_troop_id, ":agent_troop", ":agent_no"),
      (store_skill_level, ":skl_level", skl_riding, ":agent_troop"),
      (store_mul, ":speed_multi", ":skl_level", 2),
      (val_add, ":speed_multi", 100),
      (val_mul, ":speed_factor", ":speed_multi"),
      (val_div, ":speed_factor", 100),
      (agent_set_horse_speed_factor, ":agent_no", ":speed_factor"),
    (try_end),
  (try_end),
  ])
##diplomacy end


field_ai_triggers = [
  dplmc_horse_speed,
  
  # On spawn, mark lancers, spears, horse archers using a slot. Force lancers to equip lances, horse archers to equip bows 
  (ti_on_agent_spawn, 0, 0, [], [(store_trigger_param_1, ":agent"),(call_script, "script_weapon_use_classify_agent", ":agent")]), 
  
  (2, 0, 0, [(this_or_next|party_slot_eq, "p_main_party", slot_party_pref_wu_lance, 1),(this_or_next|party_slot_eq, "p_main_party", slot_party_pref_wu_harcher, 1),(party_slot_eq, "p_main_party", slot_party_pref_wu_spear, 1),(store_mission_timer_a, reg0),(gt, reg0, 4)],
  
   # Check to make sure there are no lance users on foot, if so force them to
   # switch to their sword. This should also affect troops that were NEVER mounted,
   # but are still equipped with lances, such as Taiga Bandits.
   # Check horse archers ammo, and if none left, switch to sword.
   # For mounted lancers and foot spears, affect their Decision on weapon use,
   # based on if closest 3 enemies are within 5 meters and if currently attacking/defending.
  
 [       
  (try_for_agents, ":agent"), # Run through all active NPCs on the battle field.
     # Hasn't been defeated.
    (agent_is_alive, ":agent"),
    (agent_is_non_player, ":agent"),
    (assign, ":caba_weapon_order", clear), # For Caba'drin Orders
    (assign, ":shield_order", clear), # For Caba'drin Orders
    (assign, ":weapon_order", 0),
    (assign, ":fire_order", 0),
    (try_begin),
        (agent_get_team, ":team", ":agent"),
        (eq, ":team", "$fplayer_team_no"),
        (agent_get_division, ":class", ":agent"),
        (team_get_weapon_usage_order, ":weapon_order", ":team", ":class"),
        (team_get_hold_fire_order, ":fire_order", ":team", ":class"),

        #(store_add, ":slot", slot_team_d0_order_weapon, ":class"),
        #(team_get_slot, ":caba_weapon_order", ":team", ":slot"),
        #(store_add, ":slot", slot_team_d0_order_shield, ":class"),
        #(team_get_slot, ":shield_order", ":team", ":slot"),
    (try_end),
    (neq, ":weapon_order", wordr_use_blunt_weapons), #Not ordered to use blunts
    (eq, ":caba_weapon_order", clear), # For Caba'drin orders; no active weapon order
        (try_begin),
          (party_slot_eq, "p_main_party", slot_party_pref_wu_lance, 1),
          (agent_get_slot, ":lance", ":agent", slot_agent_lance),
          (gt, ":lance", 0),  # Lancer?
    
     # Get wielded item.
          (agent_get_wielded_item, ":wielded", ":agent", 0),
          (agent_get_wielded_item, ":shield_order", ":agent",1),
    
    # They riding a horse?
          (agent_get_horse, ":horse", ":agent"),
             (try_begin),
                (le, ":horse", 0), # Isn't riding a horse.
                (agent_set_slot, ":agent", slot_agent_lance, 0), # No longer a lancer
                (eq, ":wielded", ":lance"), # Still using lance?
                  (try_begin),
                      (eq, ":shield_order", 1),
                    (assign, ":inc_two_handers", 0),
                  (else_try),
                      (assign, ":inc_two_handers", 1),
                  (try_end),
                (call_script, "script_weapon_use_backup_weapon", ":agent", ":inc_two_handers"), # Then equip a close weapon
             (else_try),
    
    # Still mounted
                (agent_get_position, pos1, ":agent"),    
                (call_script, "script_get_closest3_distance_of_enemies_at_pos1", ":team", pos1),
                (assign, ":avg_dist", reg0), # Find distance of nearest 3 enemies
    
     #SHOULD CLOSEST MATTER???
                (try_begin),
                    (lt, ":avg_dist", 500), # Are the enemies within 5 meters?
                    (agent_get_combat_state, ":combat", ":agent"),
                    (gt, ":combat", 3), # Agent currently in combat? ...avoids switching before contact
                    (eq, ":wielded", ":lance"), # Still using lance?
                      (try_begin),
                            (eq, ":shield_order", 1),
                          (assign, ":inc_two_handers", 0),
                      (else_try),
                            (assign, ":inc_two_handers", 1),
                      (try_end),
                    (call_script, "script_weapon_use_backup_weapon", ":agent", ":inc_two_handers"), # Then equip a close weapon
                (else_try),
                    (neq, ":wielded", ":lance"), # Enemies farther than 5 meters and/or not fighting, and not using lance?
                    (agent_set_wielded_item, ":agent", ":lance"), # Then equip it!
                (try_end),
             (try_end),
        
        (else_try),
          (party_slot_eq, "p_main_party", slot_party_pref_wu_harcher, 1),
          (agent_get_slot, ":bow", ":agent", slot_agent_horsebow),
          (gt, ":bow", 0),  # Horse archer?
          (neq, ":fire_order", aordr_hold_your_fire), #Not ordered to hold fire
    
     # Get wielded item.
            (agent_get_wielded_item, ":wielded", ":agent", 0),
            (agent_get_wielded_item, ":shield_order", ":agent",1),
    
     # They have ammo left?
            (agent_get_ammo, ":ammo", ":agent"),
            (try_begin),
               (le, ":ammo", 0), # No ammo left
               (agent_set_slot, ":agent", slot_agent_horsebow, 0), # No longer a horse archer
               (eq, ":wielded", ":bow"), # Still using bow?
                  (try_begin),
                      (eq, ":shield_order", 1),
                      (assign, ":inc_two_handers", 0),
                  (else_try),
                      (assign, ":inc_two_handers", 1),
                  (try_end),
               (call_script, "script_weapon_use_backup_weapon", ":agent", ":inc_two_handers"), # Then equip a close weapon
            (else_try),
              (gt, ":ammo", 0),
              (agent_get_horse, ":horse", ":agent"),
              (le, ":horse", 0), #No Horse, no command, let AI choose (I think)
            (else_try),
                (gt, ":ammo", 0),
                (neq, ":wielded", ":bow"), # Still have ammo, still mounted and not using bow?
                (agent_set_wielded_item, ":agent", ":bow"), # Then equip it!
            (try_end),
    
        (else_try),
            (party_slot_eq, "p_main_party", slot_party_pref_wu_spear, 1),
            (agent_get_slot, ":spear", ":agent", slot_agent_spear),   
            (gt, ":spear", 0), # Spear-Unit?   

            #(store_add, ":slot", slot_team_d0_formation, ":class"),
            #(team_slot_eq, ":team", ":slot", formation_none),     
            (agent_get_wielded_item, ":shield_order", ":agent",1),
            (neq, ":shield_order", 1),
      
            (agent_get_position, pos1, ":agent"), # Find distance of nearest 3 enemies
            (call_script, "script_get_closest3_distance_of_enemies_at_pos1", ":team", pos1),
            (assign, ":avg_dist", reg0),
            (assign, ":closest_dist", reg1),
            (agent_get_wielded_item, ":wielded", ":agent", 0), # Get wielded
            (try_begin), #Weapon Use
                (this_or_next|lt, ":closest_dist", 300), # Closest enemy within 3 meters?
                (lt, ":avg_dist", 700), # Are the 3 enemies within an average of 7 meters?
                (agent_get_combat_state, ":combat", ":agent"),
                (gt, ":combat", 3), # Agent currently in combat? ...avoids switching before contact
                (eq, ":wielded", ":spear"), # Still using spear?
                (call_script, "script_weapon_use_backup_weapon", ":agent", 1), # Then equip a close weapon
            (else_try),
                (neq, ":wielded", ":spear"), # Enemies farther than 7 meters and/or not fighting, and not using spear?
                (agent_set_wielded_item, ":agent", ":spear"), # Then equip it!                
            (try_end),
        (try_end),
    (try_end),
    ]),

# Horse Trample buff  
  (ti_on_agent_hit, 0, 0, [],

   [
    (store_trigger_param_1, ":agent"),
    (store_trigger_param_2, ":attacker"),
    (store_trigger_param_3, ":damage"),
    (assign, ":weapon", reg0),
    
    (assign, ":orig_damage", ":damage"),
    
    (try_begin),
        (agent_is_human, ":agent"), 
      #(agent_is_non_player, ":agent"), #Maybe remove?
        (try_begin), #Horse Trample Buff
          (neg|agent_is_human, ":attacker"),
              (eq, ":weapon", -1),
              (agent_get_item_id, ":horse", ":attacker"),
              (ge, ":horse", 0),
              (gt, ":orig_damage", 5),
              (item_get_slot, ":horse_charge", ":horse", slot_item_horse_charge), #Approximation for weight
              (try_begin),      
                (lt, ":horse_charge", 18),
                (val_div, ":horse_charge", 3),
                (val_max, ":damage", ":horse_charge"),
              (else_try),
                (is_between, ":horse_charge", 18, 25),
                (val_div, ":horse_charge", 2),
                (val_max, ":damage", ":horse_charge"),      
              (else_try),
                (val_max, ":damage", ":horse_charge"),
              (try_end),
              (try_begin),
                (agent_get_speed, pos0, ":attacker"),
                (position_get_y, ":forward_speed", pos0),
                (position_get_x, ":lateral_speed", pos0), #Double check
                (val_max, ":forward_speed", ":lateral_speed"), #Double check
                (convert_from_fixed_point, ":forward_speed"),
                (gt, ":forward_speed", 6),
                (val_mul, ":damage", 2),
              (try_end),
        (try_end),

    (else_try),     
      
      #Horses randomly rear if they take damage
      (item_slot_ge, ":weapon", slot_item_length, 150),
      (store_random_in_range, ":random_no", 0, 100),
      (try_begin),
          (store_div, ":chance_mod", ":orig_damage", 5),
        (val_sub, ":random_no", ":chance_mod"),
        (val_sub, ":random_no", ":forward_speed"),
        (agent_get_action_dir, ":direction", ":attacker"), #invalid = -1, down = 0, right = 1, left = 2, up = 3
        (try_begin),
          (gt, ":orig_damage", 5),
          (eq, ":direction", 0), #Thrust
          (val_sub, ":random_no", 10),
        (try_end),
        (lt, ":random_no", 10),
        (agent_set_animation, ":agent", "anim_horse_rear"),
      (try_end),  
    (try_end), #Human v Horse
    
    (gt, ":damage", ":orig_damage"),
    (val_sub, ":damage", ":orig_damage"),
      (store_agent_hit_points, ":hitpoints" , ":agent", 1),
      (val_sub, ":hitpoints", ":damage"),
    (agent_set_hit_points, ":agent", ":hitpoints", 1),  
    
    (assign, reg2, -1),
    (agent_get_horse,":playerhorse","$fplayer_agent_no"),
    (try_begin),
      (try_begin),
            (eq, ":agent", ":playerhorse"),
        (assign, reg2, 0),
      (else_try),
          (eq, ":agent", "$fplayer_agent_no"),
        (assign, reg2, 1),
      (try_end),
      (neq, reg2, -1),
        (assign, reg1, ":damage"),    
        (display_message, "@{reg2?You:Your mount} received {reg1} extra damage!",0xff4040),
      (else_try),
        (try_begin),
          (eq, ":attacker", ":playerhorse"),
        (assign, reg2, 0),
      (else_try),
          (eq, ":attacker", "$fplayer_agent_no"),
        (assign, reg2, 1),
      (try_end),
      (neq, reg2, -1),
      (assign, reg1, ":damage"),  
      (display_message, "@{reg2?You strike:Your horse charges} for {reg1} bonus damage!"),
      (try_end),
   ]),  
  
  #De-Horse Trigger #Valid division 0-8
  (ti_on_agent_dismount, 0, 0, [(party_get_slot, reg3, "p_main_party", slot_party_pref_div_dehorse),(is_between, reg3, 0, 9)], 
   [
    (store_trigger_param_2, ":horse"),
    (neg|agent_is_alive, ":horse"),
    
    (store_trigger_param_1, ":rider"), 
    (agent_is_alive, ":rider"),
    (agent_is_non_player, ":rider"),
    
    (agent_get_team, ":team", ":rider"),
  
    (try_begin),
      (eq, ":team", "$fplayer_team_no"),
      (agent_set_division, ":rider", reg3),
      (agent_set_slot, ":rider", slot_agent_new_division, reg3),
    (else_try),
      (agent_set_division, ":rider", grc_infantry),
      (agent_set_slot, ":rider", slot_agent_new_division, grc_infantry),
    (try_end),
 ]),

 #Out of Ammo Trigger #Valid division 0-8
  (ti_on_item_unwielded, 0, 0, [(party_get_slot, reg3, "p_main_party", slot_party_pref_div_no_ammo),(is_between, reg3, 0, 9)], 
   [
    (store_trigger_param_2, ":weapon"),
    (ge, ":weapon", 0),
    (item_get_type, ":type", ":weapon"),
    (this_or_next|eq, ":type", itp_type_bow),
    (eq, ":type", itp_type_crossbow),
    
    (store_trigger_param_1, ":agent"),
    (agent_is_alive, ":agent"),
    (agent_is_non_player, ":agent"),
    
    (agent_get_ammo, ":ammo", ":agent", 0),
    (le, ":ammo", 0), 
    (agent_get_horse, ":horse", ":agent"),
    (eq, ":horse", -1),
  
    (agent_get_team, ":team", ":agent"),
    (assign, ":continue", 1),
    (try_begin),
      (this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town), #Sieges
      (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),   
      (this_or_next|eq, ":team", "$defender_team"),
      (eq, ":team", "$defender_team_2"),
      (assign, ":continue", 0), #To not reassign units that will get their ammo refilled.
    (try_end),
    (eq, ":continue", 1), 
  
    (try_begin),
      (eq, ":team", "$fplayer_team_no"),
      (agent_set_division, ":agent", reg3),
      (agent_set_slot, ":agent", slot_agent_new_division, reg3),
    (else_try),
      (agent_set_division, ":agent", grc_infantry),
      (agent_set_slot, ":agent", slot_agent_new_division, grc_infantry),
    (try_end),  
   ]),
   

 ###GENERAL AI TRIGGER for SPECIAL ORDERS  ##Deal with Formations    
#  (1, 0, 0, [(eq, "$cheat_mode",1),(store_mission_timer_a, reg0),(gt, reg0, 2)], [ 
#    (set_fixed_point_multiplier, 100),
#      (try_for_range, ":team", 0, 4), #For AI
#      (neq, ":team", "$fplayer_team_no"),
     # (team_slot_ge, ":team", slot_team_size, 1),
#      (assign, ":mordr", -1),
#      (team_get_faction, ":faction", ":team"),
#      (neq, ":faction", "fac_no_faction"),
#      (assign, ":ai_skirmish",0),
#      (try_begin), #Volley/Skirmish Decision Making
        #(neq, ":faction", "fac_"),
        #(neq, ":faction", "fac_kingdom_5"), 
#        (store_add, ":slot", slot_party_skirmish_d0, grc_archers),
#        (neg|team_slot_eq, ":team", ":slot", 1),
#        (call_script, "script_battlegroup_get_size", ":team", grc_archers),
#        (assign, ":num_archers", reg1 ),
#        (call_script, "script_battlegroup_get_size", ":team", grc_everyone),
#        (assign, ":size", reg1),
        #(team_get_slot, reg1, ":team", slot_team_num_archers),
        #(team_get_slot, ":size", ":team", slot_team_size),
#        (val_mul, reg0, 100),
#        (val_div, ":num_archers", ":size"),
#        (gt, ":num_archers", 25), #>25% archers
#        (team_set_order_listener, ":team", grc_archers),
#        (eq, ":ai_skirmish",0),
#        (call_script, "script_order_skirmish_begin_end"),
       # (display_message, "@AI Archers starting skirmish"),
#        (team_set_order_listener, ":team", -1),
#        (assign, ":ai_skirmish",1),
   #   (else_try),
        #(this_or_next|eq, ":faction", "fac_kingdom_1"), #Swadia
        #(eq, ":faction", "fac_kingdom_5"), #Rhodoks... Cross-bow users
       # (assign, ":distance", 99999),
        #(try_begin),
        #  (store_add, ":slot", slot_team_d0_order_volley, grc_archers),
        #  (neg|team_slot_ge, ":team", ":slot", 1), #Not Volleying
        #  (team_get_slot, reg1, ":team", slot_team_num_archers),
        #  (team_get_slot, ":size", ":team", slot_team_size),
        #  (val_mul, reg1, 100),
        #  (val_div, reg1, ":size"),
        #  (gt, reg1, 25), #>25% archers
        #  (team_get_movement_order, ":mordr", ":team", grc_archers),
        #  (neq, ":mordr", mordr_charge),  
        #  (call_script, "script_battlegroup_get_position", pos2, ":team", grc_archers),
        #  (call_script, "script_get_nearest_enemy_battlegroup_location", Temp_Pos, ":team", pos2),          
        #  (is_between, reg0, 1000, 7000),
        #  (team_set_order_listener, ":team", grc_archers),
        #  (call_script, "script_order_volley_begin_end", begin, ":team"),
        #  (team_set_order_listener, ":team", -1),
   #     (else_try),
        #  (store_add, ":slot", slot_team_d0_order_volley, grc_archers),
        #  (team_slot_ge, ":team", ":slot", 1),
        #  (assign, ":end", 0),
#          (try_begin),
#            (team_get_movement_order, ":mordr", ":team", grc_archers),
#            (eq, ":mordr", mordr_charge),
           # (display_message, "@AI Archers ordered to charge - ending skirmish"), 
#            (assign, ":end", 1),
#          (else_try),
#            (call_script, "script_battlegroup_get_position", pos2, ":team", grc_archers),
#            (call_script, "script_get_nearest_enemy_battlegroup_location", Nearest_Enemy_Battlegroup_Pos, ":team", pos2),
#            (neg|is_between, reg0, 1000, 8000),
          #  (display_message, "@Enemy too close to AI Archers - ending skirmish"), 
#            (assign, ":end", 1),
#         (try_end),          
##          (eq, ":end", 1),
##          (eq, ":ai_skirmish",1),
#          (team_set_order_listener, ":team", grc_archers),
#          (call_script, "script_order_skirmish_begin_end"),
#          (assign, ":ai_skirmish",0),
#          (team_set_order_listener, ":team", -1),
     #   (try_end),
#     (try_end), #End Skirmish/Volley
#    (try_end), #Team Loop
#    ]),

#### Kham - Improved Field AI (Credit: Caba'drin PBOD & Diplomacy - Modified for TLD) END
 ] 


#### Kham Improved High Level Archer Aim VS Orcs (Credit: Oliveran)
oliveran_archer_has_released = (0, 0, 0, [],
    [
        (try_for_agents, ":agent1"),
            (agent_is_active,":agent1"),
            (agent_is_alive,":agent1"),
            (agent_is_non_player, ":agent1"),

            #TLD Check
            (agent_get_troop_id, ":troop", ":agent1"),
            (store_proficiency_level, ":prof", ":troop", wpt_archery),
            (ge, ":prof", 200),
        
            (agent_get_slot, ":is_aiming", ":agent1", agent_is_aiming),
            (eq, ":is_aiming", 1),
            (agent_get_attack_action, ":action", ":agent1"),
            (eq, ":action", 0),
            
            (agent_set_slot, ":agent1", agent_is_aiming, 0),
        (try_end),
    ])

oliveran_archer_bone_target = (0, 0, 0, [],
    [
        (try_for_agents, ":agent1"),
            (agent_is_active,":agent1"),
            (agent_is_alive,":agent1"),
            (agent_is_non_player, ":agent1"),

            #TLD Check
            (agent_get_troop_id, ":troop1", ":agent1"),
            (store_proficiency_level, ":prof", ":troop1", wpt_archery),
            (ge, ":prof", 200),
            
            (agent_get_slot, ":is_aiming", ":agent1", agent_is_aiming),
            (eq, ":is_aiming", 0),
            
            (agent_get_wielded_item, ":weapon", ":agent1", 0),
            (ge, ":weapon", 0),
            (this_or_next|item_has_property, ":weapon", itp_type_bow),
            (item_has_property, ":weapon", itp_type_crossbow),
            
            (agent_get_combat_state, ":state", ":agent1"),
            (eq, ":state", 3),
            
            (agent_ai_get_look_target,":agent2", ":agent1"),
            (agent_is_active,":agent2"),
            (agent_is_alive,":agent2"),
            
            (agent_get_position, pos2, ":agent2"),
            (agent_set_attack_action, ":agent1", -2, 0),
            
           # (assign, ":move_x", 0),
            (assign, ":move_z", 0),
            #(store_random_in_range, ":chance", 0, 2),
            #(agent_get_troop_id, ":troop2", ":agent2"),
            #(troop_get_type, ":race", ":troop2"),
            (agent_get_position, pos3, ":agent1"),
            (agent_get_bone_position, pos4, ":agent2", 0, 1),
            (get_distance_between_positions, ":distance", pos3, pos4),
            (assign, reg2, ":distance"),
           # (display_message, "@Distance: {reg2}"),
            (try_begin),
                (gt, ":distance", 2000),
                (store_div, ":move_z", ":distance", 100),
                (assign, reg3, ":move_z"),
            #    (display_message, "@Adjustment on Z: {reg3}"),
                (store_random_in_range, ":bone", 7, 10),
            (else_try),
                (assign, ":bone", 9),
            (try_end),
            
            (agent_is_in_line_of_sight, ":agent1", pos2),
            
            (agent_get_bone_position, pos1, ":agent2", ":bone", 1),
            (assign, reg1, ":bone"),
         #   (display_message, "@Target: {reg1}"),
            #(position_move_x, pos1, ":move_x", 0),#If aiming for feet, move slightly left or right
            (position_move_z, pos1, ":move_z", 0),
            (agent_set_attack_action, ":agent1", 0, 0),
            (agent_set_look_target_position, ":agent1", pos1),
            
            (agent_set_slot, ":agent1", agent_is_aiming, 1),
        (try_end),
    ])

#### Kham Improved High Level Archer Aim VS Orcs (Credit: Oliveran) END

#### Kham Improved Track & Damage Fallen Riders

kham_track_riders = (ti_after_mission_start, 0, ti_once, [],
  [
    (try_for_agents, ":agent_no"),
      (agent_set_slot, ":agent_no", slot_agent_horse_agent, -1),
      (agent_set_slot, ":agent_no", slot_agent_rider_agent, -1),
      (try_begin),
        ## Humans - Get the horse they're attached to and store it.
        (agent_is_human, ":agent_no"),
        (agent_get_horse, reg1, ":agent_no"),
        (agent_set_slot, ":agent_no", slot_agent_horse_agent, reg1),
      (else_try),
        ## Mounts - Get the human they're attached to and store it.
        (neg|agent_is_human, ":agent_no"),
        (agent_get_rider, reg1, ":agent_no"),
        (agent_set_slot, ":agent_no", slot_agent_rider_agent, reg1),
      (try_end),
    (try_end),
  ])


kham_damage_fallen_riders = (ti_on_agent_killed_or_wounded, 0, 0, [],
  [
    (store_trigger_param_1, ":agent_victim"),
    (store_trigger_param_2, ":agent_killer"),
    (agent_is_active, ":agent_killer"), # Put in to prevent script errors on bodysliding.
    (neg|agent_is_human, ":agent_victim"),
    (agent_get_slot, ":agent_rider", ":agent_victim", slot_agent_rider_agent),
    (ge, ":agent_rider", 0),
    (agent_is_active, ":agent_rider"),
    (agent_is_alive, ":agent_rider"),
    (agent_get_troop_id, ":troop_no", ":agent_rider"),
    (neg|is_between, ":troop_no", warg_ghost_begin, warg_ghost_end), # Dont allow wargs to fall unconscious
    
    
    (agent_get_speed, pos4, ":agent_rider"),
    (position_get_y, reg21, pos2),
    (store_div, ":speed", reg21, 2000), # Seems to usually produce a number in the mid 100's.
    (call_script, "script_ce_get_troop_encumbrance", ":troop_no", -1),
    (assign, ":weight", reg1),
    # (try_begin),
      # (gt, ":weight", 100),
      # (val_div, ":weight", 10),
    # (try_end),
    (store_mul, ":weighted_damage", ":weight", ":weight"),
    (val_div, ":weighted_damage", 100),
    (store_div, ":minimum_weighted", ":weight", 2),
    (val_max, ":weighted_damage", ":minimum_weighted"),
    (store_mul, ":damage", ":weighted_damage", ":speed"),
    (val_div, ":damage", 110),
    (assign, reg31, ":damage"), ### DIAGNOSTIC ### - Raw Damage
    (store_skill_level, ":skill_riding", "skl_riding", ":troop_no"),
    (assign, reg32, ":skill_riding"), ### DIAGNOSTIC ### - Riding Skill
    (val_mul, ":skill_riding", 8),
    (assign, reg34, ":skill_riding"), ### DIAGNOSTIC ### - Damage Reduction %
    (store_mul, ":damage_reduction", ":damage", ":skill_riding"),
    (val_div, ":damage_reduction", 100),
    (val_sub, ":damage", ":damage_reduction"),
    
    (assign, reg33, ":damage"), ### DIAGNOSTIC ### - Raw Reduced Damage
    
    (set_show_messages, 0),
    (store_agent_hit_points, ":health", ":agent_rider", 1),
    (val_sub, ":health", ":damage"),
    (try_begin),
      (lt, ":health", 1),
      (assign, ":agent_killed", 1),
      (assign, ":health", 1),
      (agent_set_hit_points, ":agent_rider", ":health", 1),
      (agent_get_kill_count, ":kills_before", ":agent_killer"),
      (agent_deliver_damage_to_agent_advanced, reg0, ":agent_killer", ":agent_rider", ":damage"), # WSE
      (agent_get_kill_count, ":kills_after", ":agent_killer"),
      (try_begin),
        (gt, ":kills_after", ":kills_before"), # If it is higher than the victim was killed.
        (assign, reg24, 1),
      (else_try),
        (assign, reg24, 0),
      (try_end),
    (else_try),
      (assign, ":agent_killed", 0),
      (agent_set_hit_points, ":agent_rider", ":health", 1),
    (try_end),
    (set_show_messages, 1),
    (str_store_troop_name, s21, ":troop_no"),
    ## script error
    (agent_get_troop_id, ":troop_killer", ":agent_killer"),
    (str_store_troop_name, s22, ":troop_killer"),
    ## script error
    (troop_get_type, reg23, ":troop_no"),
    (try_begin),
        (neq, reg23, 1), #not female
        (assign, reg23, 0), #make it male for strings
    (try_end),
    (get_player_agent_no, ":agent_player"),
    (agent_get_team, ":team_player", ":agent_player"),
    #(agent_get_team, ":team_killer", ":agent_killer"),
    (agent_get_team, ":team_victim", ":agent_rider"),
    (assign, reg22, ":damage"),
    (try_begin),
      (troop_get_class, ":class", ":troop_no"),
      (this_or_next|troop_is_hero, ":troop_no"),
      (eq, ":class", 2), # Cavalry
      (try_begin),
        ## PLAYER - Horse killed.
        (eq, ":agent_rider", ":agent_player"),
        (display_message, "@Your mount has fallen to the ground beneath you!", color_bad_news),
        (display_message, "@Receive {reg22} damage."), # due to falling from your mount.", color_bad_news),
        (try_begin),
          (eq, ":agent_killed", 1),
          (display_message, "@You have been knocked unconscious by {s22}.", color_bad_news),
        (try_end),
      (else_try),
        ## ANYONE - Killed someone's horse (teammate)
        (eq, ":team_player", ":team_victim"),
        (display_message, "@{s21} has been knocked off of {reg23?her:his} mount.", 0xB48211),
        #(display_message, "@{s21} receives {reg22} damage due to falling from {reg23?her:his} mount.", 0xB48211),
        (try_begin),
          (eq, ":agent_killed", 1),
          (display_message, "@{s21} {reg24?killed:knocked unconscious} by {s22}.", 0xB48211),
        (try_end),
      (else_try),
        ## ANYONE - Killed someone's horse (ally)
        (agent_is_ally, ":agent_rider"),
        (display_message, "@{s21} has been knocked off of {reg23?her:his} mount.", 0xB06EDA),
        #(display_message, "@{s21} receives {reg22} damage due to falling from {reg23?her:his} mount.", 0xB06EDA),
        (try_begin),
          (eq, ":agent_killed", 1),
          (display_message, "@{s21} {reg24?killed:knocked unconscious} by {s22}.", 0xB06EDA),
        (try_end),
      (else_try),
        ## ANYONE - Killed someone's horse (enemy)
        (teams_are_enemies, ":team_player", ":team_victim"),
        (display_message, "@{s21} has been knocked off of {reg23?her:his} mount.", 0x42D8A6),
        #(display_message, "@{s21} receives {reg22} damage due to falling from {reg23?her:his} mount.", 0x42D8A6),
        (try_begin),
          (eq, ":agent_killed", 1),
          (display_message, "@{s21} {reg24?killed:knocked unconscious} by {s22}.", 0x42D8A6),
        (try_end),
      (try_end),
    (try_end),
    #(ge, DEBUG_COMBAT_EFFECTS, 2),
    #(assign, reg35, ":weight"),
    #(assign, reg36, ":speed"),
    #(display_message, "@DEBUG: {reg31} [({reg35}wt^2/100 * {reg36}% speed)] raw -> {reg32} ride = -{reg34}% -> {reg33} given", color_bad_news),
  ])