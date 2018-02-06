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
                      (gt, ":shield_order", 0),
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
                            (gt, ":shield_order", 0),
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
                      (gt, ":shield_order", 0),
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
            (lt, ":shield_order", 0),
      
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
    (ge, ":weapon",0), #Kham - Fix
    
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
tld_archer_hold_fire = (1, 0, ti_once, [(eq,"$field_ai_archer_aim",1)],
  [
    (assign, ":counter", 0),
    (get_player_agent_no, ":player"),
    (agent_get_team, ":team", ":player"),

    (try_for_agents, ":agent1"),

        (agent_is_active,":agent1"),
        (agent_is_alive,":agent1"),
        (agent_is_non_player, ":agent1"),

        (agent_get_team, ":agent_team", ":agent1"),
        (eq, ":agent_team", ":team"),

        (agent_get_wielded_item, ":weapon", ":agent1", 0),
        (ge, ":weapon", 0),
        (this_or_next|item_has_property, ":weapon", itp_type_bow),
        (item_has_property, ":weapon", itp_type_crossbow),

        #TLD Check
        (agent_get_troop_id, ":troop1", ":agent1"),
        (store_proficiency_level, ":prof", ":troop1", wpt_archery),
        (ge, ":prof", 200),

        (agent_ai_get_look_target,":agent2", ":agent1"),
        (agent_is_active,":agent2"),
        (agent_is_alive,":agent2"),

        (agent_get_position, pos2, ":agent2"),
        (agent_get_position, pos3, ":agent1"),
        (get_distance_between_positions, ":distance", pos3, pos2),


        (try_begin),
          (eq, "$cheat_mode",1),
          (eq,":counter",0),
          (assign, reg1, ":distance"),
         # (display_message, "@DEBUG: Distance: {reg1}"),
        (end_try),

        (ge, ":distance", 7000),

        (try_begin),
          (eq, ":counter", 0),
          (set_show_messages, 0),
          (team_give_order, ":team", grc_archers, mordr_hold_fire),
          (set_show_messages, 1),
          (display_message, "@Your high-level archers determines that the enemy is too far away. They are holding their fire to conserve arrows until ordered otherwise.", color_good_news),
          (assign, ":counter", 1),
        (try_end),
    (try_end),
  ])




# TLD: fix game bug: archers aim at hard-coded head/torax-position instead of real head/torax-position 
# (e.g. elven archers consistently shooting ABOVE orc heads)
tld_archer_aim_fix = (0, 0, 0, [(eq,"$field_ai_archer_aim",1)],
    [   
        
        (assign, ":counter", 0),

        (try_for_agents, ":agent1"),
            (agent_is_active,":agent1"),
            (agent_is_alive,":agent1"),
            (agent_is_non_player, ":agent1"),

            (agent_get_troop_id, ":troop1", ":agent1"),
            
            (agent_slot_eq, ":agent1", agent_aim_overridden, 0), # override only once (DISABLED for now)
            

            # is agent a very good shooter? (not necessary?)
            (store_proficiency_level, ":prof", ":troop1", wpt_archery),
            (ge, ":prof", 200),
         
            # is agent a shooter? (i.e. wielding a ranged weapon)
            (agent_get_wielded_item, ":weapon", ":agent1", 0),
            (ge, ":weapon", 0),
            (this_or_next|item_has_property, ":weapon", itp_type_bow),
            (item_has_property, ":weapon", itp_type_crossbow),

            # todo: add other ranged weapons... pistols, javelins...
            
            # is shooter in the process of aiming?
            (agent_get_combat_state, ":state", ":agent1"),
            (eq, ":state", 1),  
            (agent_ai_get_look_target,":agent2", ":agent1"),
            
            # is target alive? (not necessary?)
            (agent_is_active,":agent2"),
            (agent_is_alive,":agent2"),

            # is target short?
            (agent_get_troop_id, ":troop2", ":agent2"),
            (ge, ":troop2", 0),  # not necessary?

            (troop_get_type, ":race", ":troop2"),
            (this_or_next|eq, ":race", tf_orc), 
            (eq, ":race", tf_dwarf),

        
            (val_add, ":counter",1), # book-keeping...
  
            (assign, ":bone", 8), # by default, aim at torax
       
          # consider current distance to target to decide stuff (e.g. aim at head or torax? shoot or not?)
            (agent_get_position, pos2, ":agent2"),  # pos2 = target pos
            (agent_get_position, pos3, ":agent1"),  # pos3 = shooter pos
            (get_distance_between_positions, ":distance", pos3, pos2),
            
            (try_begin),
              (ge, ":distance", 6300),
              (assign, ":continue", 0),
            (else_try),
              (is_between, ":distance", 1000, 6300),
              (assign, ":bone", 8),  # aim at thorax if between than 20 - 50 meters (todo: adjust distance with proficency)
              (assign, ":continue", 1),
            (else_try),
              (lt, ":distance", 1000),
              (assign, ":bone", 7), #aim at head if distance is less than 20m
              (assign, ":continue", 1),
            (try_end),
            
            (eq, ":continue", 1), #Do we modify aim? It will be based on distance

            (agent_is_in_line_of_sight, ":agent1", pos2),
           
            (agent_get_bone_position, pos1, ":agent2", ":bone", 1), # pos1 = target BONE pos
            (agent_set_attack_action, ":agent1", 0, 0),      # enforce shooting (DISABLED)
            (agent_set_look_target_position, ":agent1", pos1),      # override aimed location
           # (agent_set_look_target_agent, ":agent1", ":agent2"),    # desperate attempt at making archer fight on and actually shoot
            
        (try_end),

        (try_begin),
            (gt, ":counter",0),
            (assign, reg10, ":counter"),
            (assign, reg11, ":bone"),
            #(assign, reg12, ":continue"),
            #(display_message, "@DEBUG: OVERRRIDING AIM x{reg10}!. TARGETTING {reg11}."),
        (try_end),
    ])


# fix part II: call on release arrow
tld_archer_aim_fix_on_release = (0, 0, 0, [(eq,"$field_ai_archer_aim",1)],
    [
        (try_for_agents, ":agent1"),
            (agent_is_active,":agent1"),
            (agent_is_alive,":agent1"),
            (agent_is_non_player, ":agent1"),
        
            (agent_get_slot, ":is_aiming", ":agent1", agent_aim_overridden),
            (eq, ":is_aiming", 1),
            (agent_get_attack_action, ":action", ":agent1"),
            (eq, ":action", 0),
            
            (agent_set_slot, ":agent1", agent_aim_overridden, 0),
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
        (this_or_next|eq, "$show_mount_ko_message",1),
        (eq, "$show_mount_ko_message",2),
        (eq, ":agent_rider", ":agent_player"),
        (display_message, "@Your mount has fallen to the ground beneath you!", color_bad_news),
        (display_message, "@Receive {reg22} damage."), # due to falling from your mount.", color_bad_news),
        (try_begin),
          (eq, ":agent_killed", 1),
          (display_message, "@You have been knocked unconscious by {s22}.", color_bad_news),
        (try_end),
      (else_try),
        (eq, "$show_mount_ko_message",2),
        ## ANYONE - Killed someone's horse (teammate)
        (eq, ":team_player", ":team_victim"),
        (display_message, "@{s21} has been knocked off of {reg23?her:his} mount when it fell.", 0xB48211),
        #(display_message, "@{s21} receives {reg22} damage due to falling from {reg23?her:his} mount.", 0xB48211),
        (try_begin),
          (eq, ":agent_killed", 1),
          (display_message, "@{s21} {reg24?killed:knocked unconscious} by {s22}.", 0xB48211),
        (try_end),
      (else_try),
        (eq, "$show_mount_ko_message",2),
        ## ANYONE - Killed someone's horse (ally)
        (agent_is_ally, ":agent_rider"),
        (display_message, "@{s21} has been knocked off of {reg23?her:his} mount when it fell.", 0xB06EDA),
        #(display_message, "@{s21} receives {reg22} damage due to falling from {reg23?her:his} mount.", 0xB06EDA),
        (try_begin),
          (eq, ":agent_killed", 1),
          (display_message, "@{s21} {reg24?killed:knocked unconscious} by {s22}.", 0xB06EDA),
        (try_end),
      (else_try),
        (eq, "$show_mount_ko_message",2),
        ## ANYONE - Killed someone's horse (enemy)
        (teams_are_enemies, ":team_player", ":team_victim"),
        (display_message, "@{s21} has been knocked off of {reg23?her:his} mount when it fell.", 0x42D8A6),
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

#AI kicking start
tld_move_ai = (0.01, 0, 0, [(eq,"$field_ai_lord",1)],
  [
    (try_for_agents, ":agent1"),

      #TLD Check
      (agent_get_troop_id, ":lord", ":agent1"),
      (this_or_next|is_between, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
      (this_or_next|eq, ":lord", "trp_black_numenorean_sorcerer"),
      (is_between, ":lord", "trp_badass_theo", "trp_guldur_healer"),

      (agent_is_active,":agent1"),
      (agent_is_alive,":agent1"),
      (agent_is_human,":agent1"),
      
      #Should not be riding a horse
      (agent_get_horse, ":horse", ":agent1"),
      (le, ":horse", 0),
      
      (agent_get_animation, ":anim", ":agent1"),
      (eq, ":anim", "anim_strike3_abdomen_front"),
      (agent_get_position, pos1, ":agent1"),
      (position_move_y, pos1, -1 , 0),
      (agent_set_position, ":agent1", pos1),
    (try_end),
])

tld_ai_kicking = (1, 0, 0, [(eq,"$field_ai_lord",1)],
  [
    (try_for_agents, ":agent1"),

       #TLD Check
      (agent_get_troop_id, ":lord", ":agent1"),
      (this_or_next|is_between, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
      (this_or_next|eq, ":lord", "trp_black_numenorean_sorcerer"),
      (is_between, ":lord", "trp_badass_theo", "trp_guldur_healer"),

      (agent_is_active,":agent1"),
      (agent_is_alive,":agent1"),
      (agent_is_human, ":agent1"),

      #Should not be riding a horse
      (agent_get_horse, ":horse", ":agent1"),
      (le, ":horse", 0),
      
      (agent_ai_get_look_target,":agent2", ":agent1"),
      
      (agent_is_active,":agent2"),
      (agent_is_alive,":agent2"),

      #Should not be riding a horse
      (agent_get_horse, ":horse2", ":agent2"),
      (le, ":horse2", 0),
      
      (agent_get_team, ":team1", ":agent1"),
      (agent_get_team, ":team2", ":agent2"),
      (neq, ":team1", ":team2"),
      
      (agent_get_position, pos1, ":agent1"),
      (agent_get_position, pos2, ":agent2"),
      
      (neg|position_is_behind_position, pos1, pos2),
      (get_distance_between_positions, ":dist", pos1, pos2),
      
      (agent_get_attack_action, ":action1", ":agent1"),
      (agent_get_attack_action, ":action2", ":agent2"),
      (this_or_next|neq, ":action1", 2),
      (this_or_next|neq, ":action1", 6),
      (neq, ":action2", 2),
      
      (store_random_in_range, ":kick_chance", 0, 100),
      
      (agent_get_animation, ":anim", ":agent1"),
      (neq, ":anim", "anim_kick_right_leg"),#Can't kick if you're already kickin'...
      
      (try_begin),#Kick attempt
        (lt, ":dist", 100),
        (is_between, ":kick_chance", 0, 10),#10% chance is enemy is in range of AI
        (agent_set_attack_action, ":agent1", -2, 0),
        (agent_set_defend_action, ":agent1", -2, 0),
        (agent_set_animation, ":agent1", "anim_kick_right_leg"),#Attempt kick if agent is close enough...
      (try_end),
    (try_end),
])

tld_ai_is_kicked = (0.2, 0, 0, [(eq,"$field_ai_lord",1)],
  [
    (try_for_agents, ":agent1"),

       #TLD Check
      (agent_get_troop_id, ":lord", ":agent1"),
      (this_or_next|is_between, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
      (this_or_next|eq, ":lord", "trp_black_numenorean_sorcerer"),
      (is_between, ":lord", "trp_badass_theo", "trp_guldur_healer"),

      (agent_is_active, ":agent1"),
      (agent_is_alive, ":agent1"),
      (agent_is_non_player, ":agent1"),

      #Should not be riding a horse
      (agent_get_horse, ":horse", ":agent1"),
      (le, ":horse", 0),
      
      (agent_get_team, ":agent1_team", ":agent1"),
      
      (set_fixed_point_multiplier, 100),
      (agent_get_position, pos19, ":agent1"),

      (try_for_agents, ":agent2", pos19, 100),
        (neq, ":agent1", ":agent2"),
        (agent_is_active, ":agent2"),
        (agent_is_alive, ":agent2"),

        #Should not be riding a horse
        (agent_get_horse, ":horse2", ":agent2"),
        (le, ":horse2", 0),
      
        (agent_get_position, pos2, ":agent2"),
        (agent_get_team, ":agent2_team", ":agent2"),
        (neq, ":agent1_team", ":agent2_team"),
        
        (agent_get_bone_position, pos1, ":agent1", 6, 1),
        
        (assign, ":kicked", 0),
        (try_for_range, ":bone", 0, 20),
          (eq, ":kicked", 0),
          
          (agent_get_bone_position, pos2, ":agent2", ":bone", 1),
          
          (neg|position_is_behind_position, pos1, pos2),
          (get_distance_between_positions, ":dist", pos1, pos2),
          
          (le, ":dist", 25),
          
          (agent_get_animation, ":anim", ":agent1", 0),
          (eq, ":anim", "anim_kick_right_leg"),
          
          (agent_get_animation, ":anim", ":agent2", 0),
          (neq,":anim","anim_strike3_abdomen_front"),#Prevents mass kicking
          
          (agent_set_animation, ":agent2", "anim_strike3_abdomen_front"),#kicked
          (play_sound_at_position, 124, pos2),#Play dat phat bass boiz
          
          (store_random_in_range, ":dmg", 1, 6),
          (agent_deliver_damage_to_agent, ":agent1", ":agent2", ":dmg"),
          (assign, ":kicked", 1),
        (try_end),
      (try_end),
    (try_end),
])
#AI kicking end

#Attack/Block start
tld_melee_ai = (0, 0, 0, [(eq,"$field_ai_lord",1)],
  [
    (try_for_agents,":agent1"),

       #TLD Check
      (agent_get_troop_id, ":lord", ":agent1"),
      (this_or_next|is_between, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
      (this_or_next|eq, ":lord", "trp_black_numenorean_sorcerer"),
      (is_between, ":lord", "trp_badass_theo", "trp_guldur_healer"),

      (agent_is_active,":agent1"),
      (agent_is_alive,":agent1"),
      
      (agent_ai_get_look_target, ":agent2", ":agent1"),
      (agent_is_active,":agent2"),
      (agent_is_alive,":agent2"),
      
      (agent_get_team, ":team1", ":agent1"),
      (agent_get_team, ":team2", ":agent2"),
      (neq, ":team1", ":team2"),
      
      (agent_get_position, pos1, ":agent1"),
      (agent_get_position, pos2, ":agent2"),
      
      (neg|position_is_behind_position, pos1, pos2),
      (get_distance_between_positions, ":dist", pos1, pos2),
      
      
      #Must be a legit melee weapon used
      (agent_get_wielded_item, ":agent1_weapon", ":agent1", 0),
      
      (try_begin),
        (lt, ":agent1_weapon", 0),
        (call_script, "script_weapon_use_backup_weapon", ":agent1", 1),
      (try_end),

      (gt, ":agent1_weapon",0),
      
      (item_get_weapon_length, ":agent1_weapon_length", ":agent1_weapon"),
      
      (assign, ":agent1_stab_allowed", 0),
      (try_begin),
        (assign, ":max_stab_dist", ":agent1_weapon_length"),
        (val_mul, ":max_stab_dist", 2),
        (is_between, ":dist", 120, ":max_stab_dist"),
        (assign, ":agent1_stab_allowed", 0),
      (else_try),
        (assign, ":agent1_stab_allowed", 1),
      (try_end),
      
      (agent_get_attack_action, ":agent1_attack_action", ":agent1"),
      (agent_get_attack_action, ":agent2_attack_action", ":agent2"),
      
      (neq, ":agent1_attack_action", 2),#Prevents blocking while releasing an attack...
      #If enemy is releasing an attack, agent must try to do a defensive maneuver
      (try_begin),
        (le, ":dist", 200),
        (this_or_next|eq, ":agent2_attack_action", 2),
        (eq, ":agent2_attack_action", 3),
        
        (agent_get_action_dir, ":agent2_attack_dir", ":agent2"),
        (agent_set_defend_action, ":agent1", ":agent2_attack_dir"),
        #If enemy has finished attacking (by being blocked, parried or after releasing his attack), attack back
      (else_try),
        (le, ":dist", 200),
        
        (agent_get_animation, ":anim", ":agent1", 0),
        (neq, ":anim", "anim_kick_right_leg"),#Don't attack if you're kicking!
        
        (this_or_next|eq, ":agent2_attack_action", 6),
        (this_or_next|eq, ":agent2_attack_action", 4),
        (eq, ":agent1_attack_action", 3),
        
        (try_begin),
          (eq, ":agent1_stab_allowed", 1),
          (store_random_in_range, ":random_dir", 0, 3),
        (else_try),
          (store_random_in_range, ":random_dir", 1, 3),
        (try_end),
        (agent_set_attack_action, ":agent1", ":random_dir", 0),
      (try_end),
    (try_end),
])
#Attack/Block end

#Footwork start
tld_footwork_melee_ai = (0.25, 0, 0, [(eq,"$field_ai_lord",1)],
  [
    (try_for_agents, ":agent1"),

       #TLD Check
      (agent_get_troop_id, ":lord", ":agent1"),
      (this_or_next|is_between, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
      (this_or_next|eq, ":lord", "trp_black_numenorean_sorcerer"),
      (is_between, ":lord", "trp_badass_theo", "trp_guldur_healer"),


      (agent_is_active,":agent1"),
      (agent_is_alive,":agent1"),
      
      (try_begin),#Get potential new target
        (call_script, "script_get_closest_melee_enemy", ":agent1"),
        (gt, reg1, 0),
        (agent_set_look_target_agent, ":agent1", reg1),
      (try_end),
      
      #Get the closest attacking target
      (agent_ai_get_look_target,":agent2", ":agent1"),
      (agent_is_active,":agent2"),
      (agent_is_alive,":agent2"),
      
      (agent_get_team, ":team1", ":agent1"),
      (agent_get_team, ":team2", ":agent2"),
      (neq, ":team1", ":team2"),
      
      (team_get_movement_order, ":order", ":team1", grc_everyone),#Only free if charging
      (try_begin),
        (agent_get_slot, ":free_pathing", ":agent1", agent_is_free_of_pathing),
        (try_begin),
          (neq, ":order", 2),
          (neq, ":free_pathing", 1),
          (assign, ":free_pathing", 1),
          (agent_clear_scripted_mode, ":agent1"),
          (agent_force_rethink, ":agent1"),
          (agent_set_slot, ":agent1", agent_is_free_of_pathing, ":free_pathing"),
        (else_try),
          (eq, ":order", 2),
          (eq, ":free_pathing", 1),
          (assign, ":free_pathing", 0),
          (agent_set_slot, ":agent1", agent_is_free_of_pathing, ":free_pathing"),
        (try_end),
        (eq, ":free_pathing", 1),
      (else_try),
        (agent_get_combat_state,":state",":agent1"),
        (neq,":state",1),#Not targetting the enemy in a ranged state
        
        (agent_get_position, pos1, ":agent1"),
        (agent_get_position, pos2, ":agent2"),
        
        (agent_get_wielded_item, ":agent1_weapon", ":agent1", 0),
        
        (neg|is_between, ":agent1_weapon", "itm_short_bow", "itm_dunland_javelin"),
        (is_between, ":agent1_weapon", "itm_short_bow", "itm_witchking_helmet"),
        
        (neg|position_is_behind_position, pos1, pos2),
        (get_distance_between_positions, ":dist", pos1, pos2),
        
        
        (try_begin),#If it's too far away, get back in!
          (is_between, ":dist", 250, 500),
          (agent_set_scripted_destination, ":agent1", pos2, 1),
        (else_try),#If it's in melee reach, RNG it baby!
          (is_between, ":dist", 50, 250),
          
          (store_random_in_range, ":forward_backwards", 0, 2),
          (store_random_in_range, ":left_right", 0, 2),
          
          (try_begin),
            (eq, ":forward_backwards", 0),
            (store_random_in_range, ":rand_y", -25, -5),
          (else_try),
            (store_random_in_range, ":rand_y", 25, 75),
          (try_end),
          
          (try_begin),
            (eq, ":left_right", 0),
            (store_random_in_range, ":rand_x", -200, -150),
          (else_try),
            (store_random_in_range, ":rand_x", 150, 200),
          (try_end),
          
          (position_move_x, pos1, ":rand_x", 0),
          (position_move_y, pos1, ":rand_y", 0),
          
          (agent_set_scripted_destination, ":agent1", pos1, 1),
        (else_try),#If it's too close, get out!
          (lt, ":dist", 50),
          (store_random_in_range, ":left_right", 0, 2),
          (try_begin),
            (eq, ":left_right", 0),
            (store_random_in_range, ":rand_x", -150, -100),
          (else_try),
            (store_random_in_range, ":rand_x", 100, 150),
          (try_end),
          (position_move_x, pos1, ":rand_x", 0),
          (position_move_y, pos1, -25, 0),
          (agent_set_scripted_destination, ":agent1", pos1),
        (else_try),#Otherwise, get back in there booooooy
          (gt, ":dist", 500),
          (agent_set_scripted_destination, ":agent1", pos2, 1),
          (agent_set_look_target_agent, ":agent1", ":agent2"),
        (try_end),
      (try_end),
    (try_end),
])
#Footwork end

kham_check_formations = (0, 0, 0, [
  (eq, "$tld_option_formations", 1),
  (this_or_next|neq, "$infantry_formation_type", formation_none),
  (this_or_next|neq, "$cavalry_formation_type",  formation_none),
  (       neq, "$archer_formation_type",   formation_none),
  (game_key_clicked, gk_order_2)], [
  (display_message, "@Cannot Order to Form Rows when Troops are In Formation. Undo it first by pressing U.", color_bad_news)])


tld_improved_horse_archer_ai =  (0.5, 0, 0, [(eq,"$field_ai_horse_archer",1)],
  [       
        (set_fixed_point_multiplier, 1000),
        (try_for_agents, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_non_player, ":agent_no"),
            
            (agent_get_troop_id, ":troop_id", ":agent_no"),
            (store_skill_level, ":horse_archery_level", "skl_horse_archery", ":troop_id"),
            (ge, ":horse_archery_level", 4),

            (neg|agent_slot_eq, ":agent_no", 1003, 1),
            (agent_get_horse, ":horse_no", ":agent_no"),
            (assign, ":melee_weapon", -1),
            (gt, ":horse_no", -1),
            (try_begin),
                (agent_slot_eq, ":agent_no", slot_agent_is_running_away, 0),
                (gt, ":horse_no", -1),
                (agent_get_team, ":team_no", ":agent_no"),
                (agent_get_division, ":class_no", ":agent_no"),
                (team_get_weapon_usage_order, ":weapon_usage_order", ":team_no", ":class_no"),
                (team_get_movement_order, ":movement_order", ":team_no", ":class_no"),
                (team_get_hold_fire_order, ":hold_fire", ":team_no", ":class_no"),
                (assign, ":thrown_ammo", 0),
                (assign, ":ranged_weapon", -1),
                (try_for_range, ":item", 0, 4),
                  (agent_get_item_slot, ":item_weapon", ":agent_no", ":item"),
                  (gt, ":item_weapon", 0),
                  (item_get_type, ":item_weapon_type", ":item_weapon"),
                  (try_begin),
                    (eq, ":item_weapon_type", itp_type_thrown),
                    (agent_get_ammo_for_slot, ":ammo_for_slot", ":agent_no", ":item"),
                    (val_add, ":thrown_ammo", ":ammo_for_slot"),
                  (else_try),
                    (this_or_next|eq, ":item_weapon_type", itp_type_bow),
                    (this_or_next|eq, ":item_weapon_type", itp_type_pistol),
                    (eq, ":item_weapon_type", itp_type_musket),
                    (assign, ":ranged_weapon", ":item_weapon"),
                  (else_try),
                    (this_or_next|eq, ":item_weapon_type", itp_type_one_handed_wpn),
                    (this_or_next|eq, ":item_weapon_type", itp_type_two_handed_wpn),
                    (eq, ":item_weapon_type", itp_type_polearm),
                    (assign, ":melee_weapon", ":item_weapon"),
                  (try_end),
                (try_end),
                (gt, ":ranged_weapon", -1),            
                (neg|item_has_property, ":ranged_weapon", itp_cant_reload_on_horseback),
                (neg|item_has_property, ":ranged_weapon", itp_cant_use_on_horseback),
                (agent_get_ammo, ":ammo", ":agent_no", 0),
                (val_sub, ":ammo", ":thrown_ammo"),
                (gt, ":ammo", 0),
                (agent_set_slot, ":agent_no", 1003, 2),
                (neg|eq, ":hold_fire", aordr_hold_your_fire),
                (neg|eq, ":weapon_usage_order", wordr_use_melee_weapons),
                (eq, ":movement_order", mordr_charge),
                (agent_get_position, pos50, ":agent_no"), 
                (agent_get_speed, pos31, ":agent_no"),
                (position_get_y,":speed_y",pos31),
                (assign, ":distance_closest", 100000),#1000m
                (assign, ":enemies_closest", -1),
                (try_for_agents, ":enemies"),
                    (agent_is_alive, ":enemies"),
                    (agent_is_human, ":enemies"),
                    (agent_get_position, pos36, ":enemies"),
                    (agent_get_team, ":enemies_team", ":enemies"),
                    (teams_are_enemies, ":team_no", ":enemies_team"),
                    (get_distance_between_positions, ":distance", pos50, pos36),
                    (try_begin),
                      (agent_slot_eq, ":enemies", slot_agent_is_running_away, 1),
                      (val_add, ":distance", 10000),
                    (try_end),
                    (try_begin),
                      (agent_get_horse, ":enemies_horse", ":enemies"),
                      (gt, ":enemies_horse", -1),
                      (agent_get_speed, pos32, ":enemies"),
                      (position_get_y,":speed_y_enemies",pos32),
                      (val_sub, ":speed_y_enemies", ":speed_y"),
                      (store_div, ":distance_cavalry", ":speed_y_enemies",5),
                      (val_max, ":distance_cavalry", 0),
                      (val_add, ":distance_cavalry", 500),
                      (val_sub, ":distance", ":distance_cavalry"),
                    (else_try),
                      (agent_get_wielded_item, ":weapon_hold", ":enemies", 1),
                      (neg|gt, ":weapon_hold", 1),
                      (val_sub, ":distance", 500),
                    (try_end),
                    (lt, ":distance", ":distance_closest"),
                    (assign, ":distance_closest", ":distance"),
                    (assign, ":enemies_closest", ":enemies"),
                (try_end),
                (neq, ":enemies_closest", -1),
                (agent_get_position, pos51, ":enemies_closest"),
                (get_distance_between_positions, ":distance_true", pos50, pos51),
                (try_begin),
                  (agent_slot_eq, ":enemies_closest", slot_agent_is_running_away, 0),
                  (gt,":distance_true",200),
                  (agent_set_wielded_item, ":agent_no", ":ranged_weapon"),
                (else_try),
                  (le, ":distance_true", 200),
                  (gt, ":melee_weapon", -1),
                  (agent_set_wielded_item, ":agent_no", ":melee_weapon"),
                (try_end),
                (assign, ":speed_limit", 1000),
                (try_begin),
                    (agent_get_wielded_item, ":weapon_hold", ":agent_no", 0),
                    (gt, ":weapon_hold", 0),
                    (item_get_type, ":weapon_type", ":weapon_hold"),
                    (this_or_next|eq, ":weapon_type", itp_type_bow),
                    (this_or_next|eq, ":weapon_type", itp_type_pistol),
                    (eq, ":weapon_type", itp_type_musket),
                    (agent_get_bone_position, pos53, ":agent_no", 8, 1),
                    (agent_get_bone_position, pos54, ":enemies_closest", 9, 1),
                    (position_has_line_of_sight_to_position, pos53, pos54),
                    (agent_set_look_target_agent, ":agent_no", ":enemies_closest"),
                    (try_begin),
                      (assign, ":shoot_distance", 4000),
                      (agent_get_attack_action, ":attack_action", ":agent_no"),
                      (eq, ":attack_action", 1),
                      (try_begin),
                        (gt, ":distance_closest", 700),
                        (le, ":distance_closest", ":shoot_distance"),
                        (store_div, ":speed_limit", ":speed_y",2000),#
                        (val_max, ":speed_limit", 0),
                      (try_end),
                      (eq, ":weapon_type", itp_type_bow),
                      (try_begin),
                        (le, ":distance_true", ":shoot_distance"),
                        (agent_set_defend_action, ":agent_no", -2, 1),
                        (agent_set_attack_action, ":agent_no", 3, 0),
                      (else_try),
                        (gt, ":distance_true", ":shoot_distance"),
                        (agent_set_attack_action, ":agent_no", -2, 1),
                        (agent_set_defend_action, ":agent_no", 3, 1),
                      (try_end),
                    (else_try),
                      (eq, ":weapon_type", itp_type_bow),
                      (le, ":distance_true", ":shoot_distance"),#
                      (agent_get_combat_state, ":combat_state", ":agent_no"),
                      (neq, ":combat_state", 8),
                      (agent_set_attack_action, ":agent_no", 3, 1),
                    (try_end),
                (try_end),
                (agent_set_speed_limit, ":agent_no", ":speed_limit"),
                (try_begin),
                  (agent_slot_eq, ":enemies_closest", slot_agent_is_running_away, 0),
                  (lt, ":distance_closest", 10000),
                  (try_begin),
                    (get_scene_boundaries, pos2, pos3),
                    (position_transform_position_to_local, pos4, pos2,pos50),
                    (position_get_x, ":left", pos4),
                    (position_get_y, ":down", pos4),
                    (position_transform_position_to_local, pos4, pos2,pos3),
                    (position_get_x, ":map_width", pos4),
                    (position_get_y, ":map_height", pos4),
                    (store_sub, ":right", ":map_width", ":left"),
                    (store_sub, ":up", ":map_height", ":down"),
                    (position_transform_position_to_local, pos4, pos50, pos51),
                    (position_get_x, ":enemies_x", pos4),
                    (position_get_y, ":enemies_y", pos4),
                    (assign, ":effect", 0),
                    (try_begin),
                      (neg|gt, ":distance_closest", 1000),
                      (assign, ":effect", -78000),
                    (else_try),
                      (gt, ":distance_closest", 2000),#
                      (store_sub,":effect", ":distance_closest", 0),
                      (val_mul, ":effect", 5),
                      (val_clamp, ":effect", 35000, 90000),
                    (try_end),
                    (assign, ":distance_to_boundary", 30000),
                    (val_min, ":distance_to_boundary", ":left"),
                    (val_min, ":distance_to_boundary", ":up"),
                    (val_min, ":distance_to_boundary", ":right"),
                    (val_min, ":distance_to_boundary", ":down"),
                    (try_begin),
                      (lt, ":distance_to_boundary", 30000),
                      (agent_slot_eq, ":enemies_closest", slot_agent_is_running_away, 0),
                      (store_div, ":map_middle_x", ":map_width", 20),
                      (store_div, ":map_middle_y", ":map_height", 20),
                      (position_copy_origin, pos4, pos2),
                      (position_move_x, pos4, ":map_middle_x", 1),
                      (position_move_y, pos4, ":map_middle_y", 1),
                      (get_distance_between_positions,":distance_middle", pos4, pos50),
                      (position_transform_position_to_local, pos4, pos50, pos4),
                      (position_get_x, ":map_middle_x", pos4),
                      (position_get_y, ":map_middle_y", pos4),
                      (val_mul, ":map_middle_x", 100),
                      (val_mul, ":map_middle_y", 100),
                      (val_mul, ":enemies_x", 100),
                      (val_mul, ":enemies_y", 100),
                      (store_div,":cos_middle",":map_middle_x",":distance_middle"),
                      (store_div,":sin_middle",":map_middle_y",":distance_middle"),
                      (store_div,":cos_enemies",":enemies_x",":distance_true"),
                      (store_div,":sin_enemies",":enemies_y",":distance_true"),
                      (store_acos, ":angle_cos", ":cos_middle"),
                      (store_asin, ":angle_sin", ":sin_middle"),
                      (store_acos, ":angle_cos_enemies", ":cos_enemies"),
                      (store_asin, ":angle_sin_enemies", ":sin_enemies"),
                      (try_begin),
                        (lt, ":angle_sin", 0),
                        (val_mul,":angle_cos", -1),
                        (val_add,":angle_cos", 360000),
                      (try_end),
                      (try_begin),
                        (lt, ":angle_sin_enemies", 0),
                        (val_mul,":angle_cos_enemies", -1),
                        (val_add,":angle_cos_enemies", 360000),
                      (try_end),
                      (store_sub, ":k2", ":angle_cos", ":angle_cos_enemies"),
                      (val_sub, ":k2", 270000),
                      (val_sub, ":k2", ":effect"),
                      (store_add, ":effect", ":k2", ":effect"),
                      (try_begin),
                        (lt, ":angle_cos", ":angle_cos_enemies"),
                        (val_add, ":effect", 360000),
                      (try_end),
                      (val_clamp,":effect",-210000, 15000),
                      (agent_set_attack_action, ":agent_no", -2, 1),
                      (agent_set_defend_action, ":agent_no", 3, 1),
                    (try_end),
                    (store_cos, ":cos", ":effect"),
                    (store_sin, ":sin", ":effect"),
                    (store_mul, ":k_x1", ":cos", ":enemies_y",),
                    (store_mul, ":k_x2", ":sin", ":enemies_x",),
                    (store_mul, ":k_y1", ":sin", ":enemies_y",),
                    (store_mul, ":k_y2", ":cos", ":enemies_x",),
                    (store_add, ":move_x",":k_x1", ":k_x2"),
                    (store_sub, ":move_y",":k_y1", ":k_y2"),
                    (position_move_x, pos50, ":move_x", 0),
                    (position_move_y, pos50, ":move_y", 0),
                  (try_end),
                  (agent_set_scripted_destination, ":agent_no", pos50, 1),
                (else_try),
                  (agent_clear_scripted_mode, ":agent_no"),
                  (agent_force_rethink, ":agent_no"),
                (try_end),
            (else_try),
                (try_begin),
                  (agent_slot_eq, ":agent_no", 1003, 0),
                  (agent_set_slot, ":agent_no", 1003, 1),
                (else_try),
                  (agent_slot_eq, ":agent_no", 1003, 2),
                  (this_or_next|agent_slot_eq, ":agent_no", slot_agent_is_running_away, 1),
                  (this_or_next|lt, ":horse_no", 0),
                  (this_or_next|eq, ":ammo", 0),
                  (this_or_next|eq, ":hold_fire", aordr_hold_your_fire),
                  (this_or_next|eq, ":weapon_usage_order", wordr_use_melee_weapons),
                  (neq, ":movement_order", mordr_charge),
                  (agent_clear_scripted_mode, ":agent_no"),
                  (agent_set_speed_limit, ":agent_no", 100),
                  (agent_force_rethink, ":agent_no"),
                  (agent_set_slot, ":agent_no", 1003, 3),
                  (this_or_next|eq, ":hold_fire", aordr_hold_your_fire),
                  (eq, ":ammo", 0),
                  (gt, ":melee_weapon", -1),
                  (agent_set_wielded_item, ":agent_no", ":melee_weapon"),
                (try_end),
            (try_end),
        (try_end),
  ])
