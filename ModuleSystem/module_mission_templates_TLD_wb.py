from header_common import *
from header_operations import *
from header_sounds import *
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
  1, 0, 0, [(eq, "$slow_when_wounded", 1)],
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
  (ti_on_agent_spawn, 0, 0, [], [(store_trigger_param_1, ":agent"),(call_script, "script_weapon_use_classify_agent", ":agent"), (agent_set_slot, ":agent", slot_team_shield_order, -1),]), 
  
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
    (agent_is_active, ":agent"),
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
                (agent_get_speed, pos10, ":agent"),
                (position_get_y, ":speed", pos10),                
                # (call_script, "script_get_closest3_distance_of_enemies_at_pos1", ":team", pos1),
                # (assign, ":avg_dist", reg0), # Find distance of nearest 3 enemies
                (agent_ai_get_cached_enemy, ":enemy_agent", ":agent", 0), #InVain: get closest cached enemy instead
                (ge, ":enemy_agent", 0),              
                (agent_is_active, ":enemy_agent"),
                (agent_is_alive, ":enemy_agent"),
                (agent_is_human, ":enemy_agent"),
                (agent_get_position, pos2, ":enemy_agent"),
                (get_distance_between_positions, ":dist", pos1, pos2),
    
     #SHOULD CLOSEST MATTER???
                (try_begin),
                    (eq, ":wielded", ":lance"), # Still using lance?
                    (lt, ":dist", 500), # Are the enemies within 5 meters? (InVain: changed to closest cached enemy only)
                    (lt, ":speed", 300), #slowed down? (InVain)
                    (agent_get_combat_state, ":combat", ":agent"),
                    (gt, ":combat", 3), # Agent currently in combat? ...avoids switching before contact                    
                      (try_begin),
                            (gt, ":shield_order", 0),
                          (assign, ":inc_two_handers", 0),
                      (else_try),
                            (assign, ":inc_two_handers", 1),
                      (try_end),
                    (call_script, "script_weapon_use_backup_weapon", ":agent", ":inc_two_handers"), # Then equip a close weapon
                (else_try),
                    (gt, ":dist", 500),
                    (neq, ":wielded", ":lance"), # Enemies farther than 5 meters and/or not fighting, and not using lance?
                    (neg|agent_slot_eq, ":agent", slot_team_shield_order, 2), #Not commanded to use side-arms
                    (agent_set_wielded_item, ":agent", ":lance"), # Then equip it!
                (try_end),
             (try_end),
        
        (else_try),
          (party_slot_eq, "p_main_party", slot_party_pref_wu_harcher, 1),
          (agent_get_slot, ":bow", ":agent", slot_agent_horsebow),
          (gt, ":bow", 0),  # Horse archer?
          (eq,"$field_ai_horse_archer",0), #InVain: Only if horse archer AI is turned off, avoids conflicts
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
                (neg|agent_slot_eq, ":agent", slot_team_shield_order, 2),
                (agent_set_wielded_item, ":agent", ":spear"), # Then equip it!                
            (try_end),
        (try_end),
    (try_end),
    ]),

## Piggy Back for Lone Wargs extra damage
(ti_on_agent_hit, 0, 0, [
    (store_trigger_param_1, ":agent"),
    (neg|agent_is_human, ":agent"), #Is a warg
    (agent_get_item_id,":warg_itm",":agent"),
    (is_between, ":warg_itm", item_warg_begin, item_warg_end),
    (agent_get_rider, ":rider", ":agent"),
    (agent_is_active,":rider"),
    (agent_get_troop_id, ":invis_warg", ":rider"),
    (is_between, ":invis_warg", warg_ghost_begin, warg_ghost_end), #Riderless Warg
  ],

  [
    (store_trigger_param_3, ":damage"),
    (val_mul, ":damage", 10),
    (val_div, ":damage", 7), 
    (set_trigger_result, ":damage"), 
  ]),


# Horse Trample buff  
  (ti_on_agent_hit, 0, 0, [

    (store_trigger_param_1, ":agent"),
    (store_trigger_param_2, ":attacker"),
    (store_trigger_param_3, ":damage"),
    (assign, ":weapon", reg0),
    (ge, ":weapon",0), #Kham - Fix

    (assign, ":orig_damage", ":damage"),
    (agent_is_human, ":agent"), 
    (neg|agent_is_human, ":attacker"),
    (eq, ":weapon", -1),
    (agent_get_item_id, ":horse", ":attacker"),
    (ge, ":horse", 0),
    (gt, ":orig_damage", 5),
   ],

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
 # (ti_on_item_unwielded, 0, 0, [
# #   (party_get_slot, reg3, "p_main_party", slot_party_pref_div_no_ammo),(is_between, reg3, 0, 9),
# #   
# #   (store_trigger_param_2, ":weapon"),
# #   (ge, ":weapon", 0),
# #   (item_get_type, ":type", ":weapon"),
# #   (this_or_next|eq, ":type", itp_type_bow),
# #   (eq, ":type", itp_type_crossbow),
#
# #   (store_trigger_param_1, ":agent"),
# #   (agent_is_alive, ":agent"),
# #   (agent_is_non_player, ":agent"),
# #   
# #   (agent_get_ammo, ":ammo", ":agent", 0),
# #   (le, ":ammo", 0), 
# #   (agent_get_horse, ":horse", ":agent"),
# #   (eq, ":horse", -1),
#
 #  ], 
 #  
 #  [
 #   (store_trigger_param_2, ":weapon"),
 #   (ge, ":weapon", 0),
 #   (item_get_type, ":type", ":weapon"),
 #   (this_or_next|eq, ":type", itp_type_bow),
 #   (eq, ":type", itp_type_crossbow),
 #   
 #   (store_trigger_param_1, ":agent"),
 #   (agent_is_alive, ":agent"),
 #   (agent_is_non_player, ":agent"),
 #   
 #   (agent_get_ammo, ":ammo", ":agent", 0),
 #   (le, ":ammo", 0), 
 #   (agent_get_horse, ":horse", ":agent"),
 #   (eq, ":horse", -1),
 # 
 #   (agent_get_team, ":team", ":agent"),
 #   (assign, ":continue", 1),
 #   (try_begin),
 #     (this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town), #Sieges
 #     (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),   
 #     (this_or_next|eq, ":team", "$defender_team"),
 #     (eq, ":team", "$defender_team_2"),
 #     (assign, ":continue", 0), #To not reassign units that will get their ammo refilled.
 #   (try_end),
 #   (eq, ":continue", 1), 
 # 
 #   (try_begin),
 #     (eq, ":team", "$fplayer_team_no"),
 #     (agent_set_division, ":agent", reg3),
 #     (agent_set_slot, ":agent", slot_agent_new_division, reg3),
 #   (else_try),
 #     (agent_set_division, ":agent", grc_infantry),
 #     (agent_set_slot, ":agent", slot_agent_new_division, grc_infantry),
 #   (try_end),  
 #  ]),
   

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
        (store_mission_timer_a_msec, ":batch_time"),

        (assign, ":counter", 0),

        (try_for_agents, ":agent1"),
            (agent_is_active,":agent1"),
            (agent_is_alive,":agent1"),
            (agent_is_non_player, ":agent1"),
            (agent_is_active, ":agent1"),
            (agent_get_slot, ":check_time", ":agent1", slot_agent_tick_check_time),

            (agent_get_troop_id, ":troop1", ":agent1"),

            (try_begin),
              (ge, ":batch_time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
              (val_add, ":check_time", 100),
              (agent_set_slot, ":agent1", slot_agent_tick_check_time, ":check_time"),
              (try_begin),
                (agent_slot_eq, ":agent1", agent_aim_overridden, 0), # override only once

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
                #(agent_set_slot, ":agent1", agent_aim_overridden, 1),
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
                (agent_get_position, pos72, ":agent2"),  # pos72 = target pos
                (agent_get_position, pos73, ":agent1"),  # pos73 = shooter pos
                (get_distance_between_positions, ":distance", pos73, pos72),
                
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

                (agent_is_in_line_of_sight, ":agent1", pos72),
               
                (agent_get_bone_position, pos71, ":agent2", ":bone", 1), # pos1 = target BONE pos
                (agent_set_attack_action, ":agent1", 0, 0),      # enforce shooting (DISABLED)
                (agent_set_look_target_position, ":agent1", pos71),      # override aimed location
               #(agent_set_look_target_agent, ":agent1", ":agent2"),    # desperate attempt at making archer fight on and actually shoot
              (try_end),
            (try_end),
            (agent_get_slot, ":check_time", ":agent1", slot_agent_period_reset_time),
            (ge, ":batch_time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
            (val_add, ":check_time", "$batching_check_period"),
            (agent_set_slot, ":agent1", slot_agent_period_reset_time, ":check_time"),
        (try_end),

       # (try_begin),
       #     (gt, ":counter",0),
       #     (assign, reg10, ":counter"),
       #     (assign, reg11, ":bone"),
            #(assign, reg12, ":continue"),
            #(display_message, "@DEBUG: OVERRRIDING AIM x{reg10}!. TARGETTING {reg11}."),
      #  (try_end),
    ])


# fix part II: call on release arrow
tld_archer_aim_fix_on_release = (0, 0, 0, [(eq,"$field_ai_archer_aim",1)],
    [   (store_mission_timer_a_msec, ":batch_time"),
        
        (try_for_agents, ":agent1"),
          (agent_is_active,":agent1"),
          (agent_is_alive,":agent1"),
          (agent_is_non_player, ":agent1"),
          (agent_is_active, ":agent1"),
          (agent_get_slot, ":check_time", ":agent1", slot_agent_tick_check_time),
          (agent_get_slot, ":is_aiming", ":agent1", agent_aim_overridden),
          (try_begin),
            (ge, ":batch_time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
            (val_add, ":check_time", 100),
            (agent_set_slot, ":agent1", slot_agent_tick_check_time, ":check_time"),
            (try_begin),
              (eq, ":is_aiming", 1),
              (agent_get_attack_action, ":action", ":agent1"),
              (eq, ":action", 0),
            
              (agent_set_slot, ":agent1", agent_aim_overridden, 0),
            (try_end),
          (try_end),
          (agent_get_slot, ":check_time", ":agent1", slot_agent_period_reset_time),
          (ge, ":batch_time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
          (val_add, ":check_time", "$batching_check_period"),
          (agent_set_slot, ":agent1", slot_agent_period_reset_time, ":check_time"),
        (try_end),
    ])



#### Kham Improved High Level Archer Aim VS Orcs (Credit: Oliveran) END


tld_troll_aim_fix = (0, 0, 0, [(gt,"$trolls_in_battle",0)],
    [   
        (store_mission_timer_a_msec, ":batch_time"),

        (assign, ":counter", 0),

        (try_for_agents, ":agent1"),
            (agent_is_active,":agent1"),
            (agent_is_alive,":agent1"),
            (agent_is_non_player, ":agent1"),
            (agent_is_active, ":agent1"),
            (agent_get_slot, ":check_time", ":agent1", slot_agent_tick_check_time),

            (agent_get_troop_id, ":troop1", ":agent1"),
            (troop_get_type, ":troll_type", ":troop1"),
            (eq, ":troll_type", tf_troll),

            (try_begin),
              (ge, ":batch_time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
              (val_add, ":check_time", 100),
              (agent_set_slot, ":agent1", slot_agent_tick_check_time, ":check_time"),
              (try_begin),
                (agent_slot_eq, ":agent1", agent_aim_overridden, 0), # override only once
                
                # is shooter in the process of aiming?
                (agent_get_combat_state, ":state", ":agent1"),
                (eq, ":state", 3),  
                (agent_set_slot, ":agent1", agent_aim_overridden, 3),
                (agent_ai_get_look_target,":agent2", ":agent1"),
                
                # is target alive? (not necessary?)
                (agent_is_active,":agent2"),
                (agent_is_alive,":agent2"),

                # is target short?
               # (agent_get_troop_id, ":troop2", ":agent2"),
               # (ge, ":troop2", 0),  # not necessary?

                #(troop_get_type, ":race", ":troop2"),
                #(this_or_next|eq, ":race", tf_orc), 
                #(eq, ":race", tf_dwarf),

            
                (val_add, ":counter",1), # book-keeping...

                (assign, ":bone", 0), # by default, aim at torax
           
              # consider current distance to target to decide stuff (e.g. aim at head or torax? shoot or not?)
                (agent_get_position, pos2, ":agent2"),  # pos2 = target pos
                (agent_get_position, pos3, ":agent1"),  # pos3 = shooter pos
                (get_distance_between_positions, ":distance", pos3, pos2),
                
                (try_begin),
                  (lt, ":distance", 1000),
                  (assign, ":continue", 1),
                (try_end),
                
                (eq, ":continue", 1), #Do we modify aim? It will be based on distance

                (agent_is_in_line_of_sight, ":agent1", pos2),
               
                (agent_get_bone_position, pos1, ":agent2", ":bone", 1), # pos1 = target BONE pos
                (agent_set_look_target_position, ":agent1", pos1),      # override aimed location
                (agent_set_attack_action, ":agent1", 3, 0),      # enforce shooting (DISABLED)
                (agent_set_look_target_position, ":agent1", pos1),      # override aimed location
               #(agent_set_look_target_agent, ":agent1", ":agent2"),    # desperate attempt at making archer fight on and actually shoot
              (try_end),
            (try_end),
            (agent_get_slot, ":check_time", ":agent1", slot_agent_period_reset_time),
            (ge, ":batch_time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
            (val_add, ":check_time", "$batching_check_period"),
            (agent_set_slot, ":agent1", slot_agent_period_reset_time, ":check_time"),
        (try_end),

       # (try_begin),
       #     (gt, ":counter",0),
       #     (assign, reg10, ":counter"),
       #     (assign, reg11, ":bone"),
            #(assign, reg12, ":continue"),
            #(display_message, "@DEBUG: OVERRRIDING AIM x{reg10}!. TARGETTING {reg11}."),
      #  (try_end),
    ])


# fix part II: call on release
tld_troll_aim_fix_on_release = (0, 0, 0, [(gt,"$trolls_in_battle",0)],
    [   (store_mission_timer_a_msec, ":batch_time"),
        
        (try_for_agents, ":agent1"),
          (agent_is_active,":agent1"),
          (agent_is_alive,":agent1"),
          (agent_is_non_player, ":agent1"),
          (agent_is_active, ":agent1"),
          (agent_get_troop_id, ":troop1", ":agent1"),
          (troop_get_type, ":troll_type", ":troop1"),
          (eq, ":troll_type", tf_troll),
          (agent_get_slot, ":check_time", ":agent1", slot_agent_tick_check_time),
          (agent_get_slot, ":is_aiming", ":agent1", agent_aim_overridden),
          (try_begin),
            (ge, ":batch_time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
            (val_add, ":check_time", 100),
            (agent_set_slot, ":agent1", slot_agent_tick_check_time, ":check_time"),
            (try_begin),
              (eq, ":is_aiming", 3),
              (agent_get_attack_action, ":action", ":agent1"),
              (this_or_next|eq, ":action", 6),
              (eq, ":action", 4),
              (agent_set_slot, ":agent1", agent_aim_overridden, 0),
            (try_end),
          (try_end),
          (agent_get_slot, ":check_time", ":agent1", slot_agent_period_reset_time),
          (ge, ":batch_time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
          (val_add, ":check_time", "$batching_check_period"),
          (agent_set_slot, ":agent1", slot_agent_period_reset_time, ":check_time"),
        (try_end),
    ])


#### Kham Improved Track & Damage Fallen Riders

# Note that ti_on_agent_dismount also triggers when the horse is killed and
# before the ti_on_agent_killed_or_wounded, so we need to track if the horse
# is alive or not when invalidating the slots
noxbru_rider_dismounts = (ti_on_agent_dismount, 0, 0, [],
  [
    (store_trigger_param_1, ":agent"),
    (store_trigger_param_2, ":horse"),

    (try_begin),
      (ge, ":horse", 0), (agent_is_active, ":horse"), # Added by Arsakes
      (agent_is_alive, ":horse"),
      (agent_set_slot, ":agent", slot_agent_horse_agent, -1),
      (agent_set_slot, ":horse", slot_agent_rider_agent, -1),
    (end_try),
  ])

noxbru_rider_mounts = (ti_on_agent_mount, 0, 0, [],
  [
    (store_trigger_param_1, ":agent"),
    (store_trigger_param_2, ":horse"),

    (agent_set_slot, ":agent", slot_agent_horse_agent, ":horse"),
    (agent_set_slot, ":horse", slot_agent_rider_agent, ":agent"),
  ])

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
    (neg|is_between, ":troop_no", "trp_spider", "trp_dorwinion_sack"),
    (neq, ":troop_no", "trp_werewolf"),
    
    
    # Old damage formula:
    # max(w^2/100, w/2) * (v_y/2000) /110 * (1 - r*8/100)
    # New damage formula:
    # rand(1,5) + w * (clamp(v_y, 0, 500) / 10) / 125 * (1 - r*8/100)
    #
    # For r=5, w=50 and v_y>=500 we obtain that the *unreduced* damage is 25
    (store_random_in_range, ":random_damage", 1, 6),

    (call_script, "script_ce_get_troop_encumbrance", ":troop_no", -1),
    (assign, ":weight", reg1),

    (agent_get_speed, pos4, ":agent_rider"),
    (position_get_y, reg21, pos4),
    (val_abs, reg21),
    (val_min, reg21, 500),
    (store_div, ":speed", reg21, 10),

    (store_mul, ":raw_damage", ":weight", ":speed"),
    (val_div, ":raw_damage", 125),

    (store_skill_level, ":skill_riding", "skl_riding", ":troop_no"),
    (store_mul, ":riding_reduction", ":skill_riding", 8),
    (val_mul, ":riding_reduction", ":raw_damage"),
    (val_div, ":riding_reduction", 100),

    (store_add, ":damage", ":random_damage", ":raw_damage"),
    (val_sub,   ":damage", ":riding_reduction"),

    # (assign, reg30, ":random_damage"),    ### DIAGNOSTIC ### - Random Damage
    # (assign, reg31, ":weight"),           ### DIAGNOSTIC ### - Weight
    # (assign, reg32, ":speed"),            ### DIAGNOSTIC ### - Speed
    # (assign, reg33, ":raw_damage"),       ### DIAGNOSTIC ### - Raw Damage
    # (assign, reg34, ":skill_riding"),     ### DIAGNOSTIC ### - Riding Skill
    # (assign, reg35, ":riding_reduction"), ### DIAGNOSTIC ### - Damage Reduction %
    # (assign, reg36, ":damage"),           ### DIAGNOSTIC ### - Raw Reduced Damage
    # (display_message, "@DEBUG: {reg36} Damage: {reg30} + {reg31}x{reg32}/125 * (1 - {reg34}*8/100) = {reg30} + {reg33} - {reg35}", color_bad_news),

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

    ## PLAYER - Horse killed.
    (try_begin),
      (this_or_next|eq, "$show_mount_ko_message",1),
      (eq, "$show_mount_ko_message",2),
      (eq, ":agent_rider", ":agent_player"),
      (display_message, "@Your mount has fallen to the ground beneath you!", color_bad_news),
      (display_message, "@Receive {reg22} damage."), # due to falling from your mount.", color_bad_news),
      (try_begin),
        (eq, ":agent_killed", 1),
        (display_message, "@You have been knocked unconscious by {s22}.", color_bad_news),
      (try_end),
    (try_end),

    (try_begin),
      (eq, "$show_mount_ko_message",2),
      (troop_get_class, ":class", ":troop_no"),
      (this_or_next|troop_is_hero, ":troop_no"),
      (eq, ":class", 2), # Cavalry

      (try_begin),
        ## ANYONE - Killed someone's horse (teammate)
        (eq, ":team_player", ":team_victim"),
        (assign, reg25, 0xB48211),
      (else_try),
        ## ANYONE - Killed someone's horse (ally)
        (agent_is_ally, ":agent_rider"),
        (assign, reg25, 0xB06EDA),
      (else_try),
        ## ANYONE - Killed someone's horse (enemy)
        (teams_are_enemies, ":team_player", ":team_victim"),
        (assign, reg25, 0x42D8A6),
      (try_end),

      (display_message, "@{s21} has been knocked off of {reg23?her:his} mount when it fell.", reg25),
      #(display_message, "@{s21} receives {reg22} damage due to falling from {reg23?her:his} mount.", reg25),
      (try_begin),
        (eq, ":agent_killed", 1),
        (display_message, "@{s21} {reg24?killed:knocked unconscious} by {s22}.", reg25),
      (try_end),
    (try_end),
  ])

#AI kicking start
tld_move_ai = (0.01, 0, 0, [(eq,"$field_ai_lord",1)],
  [
    (try_for_agents, ":agent1"),

      #TLD Check
      (agent_get_troop_id, ":lord", ":agent1"),
      
      (troop_slot_eq, ":lord", slot_troop_has_combat_ai, 1), 

      #(this_or_next|is_between, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
      #(this_or_next|eq, ":lord", "trp_black_numenorean_sorcerer"),
      #(this_or_next|eq, ":lord", "trp_nazgul"),
      #(this_or_next|eq, ":lord", "trp_mordor_olog_hai"),
      #(is_between, ":lord", "trp_badass_theo", "trp_guldur_healer"),

      (agent_is_active,":agent1"),
      (agent_is_alive,":agent1"),
      (agent_is_human,":agent1"),
      
      #Should not be riding a horse
      (agent_get_horse, ":horse", ":agent1"),
      (le, ":horse", 0),
      
      (agent_get_animation, ":anim", ":agent1"),
      (eq, ":anim", "anim_strike3_abdomen_front"),
      (agent_get_position, pos81, ":agent1"),
      (position_move_y, pos81, -1 , 0),
      (agent_set_position, ":agent1", pos81),
    (try_end),
])

tld_ai_kicking = (1, 0, 0, [(eq,"$field_ai_lord",1)],
  [
    (try_for_agents, ":agent1"),

       #TLD Check
      (agent_get_troop_id, ":lord", ":agent1"),
      (troop_slot_eq, ":lord", slot_troop_has_combat_ai, 1), 

      #(this_or_next|is_between, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
      #(this_or_next|eq, ":lord", "trp_nazgul"),
      #(this_or_next|eq, ":lord", "trp_black_numenorean_sorcerer"),
      #(this_or_next|eq, ":lord", "trp_mordor_olog_hai"),
      #(is_between, ":lord", "trp_badass_theo", "trp_guldur_healer"),

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
      
      (agent_get_position, pos81, ":agent1"),
      (agent_get_position, pos82, ":agent2"),
      
      (neg|position_is_behind_position, pos81, pos82),
      (get_distance_between_positions, ":dist", pos81, pos82),
      
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
      (troop_slot_eq, ":lord", slot_troop_has_combat_ai, 1), 

      #(this_or_next|is_between, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
      #(this_or_next|eq, ":lord", "trp_nazgul"),
      #(this_or_next|eq, ":lord", "trp_black_numenorean_sorcerer"),
      #(this_or_next|eq, ":lord", "trp_mordor_olog_hai"),
      #(is_between, ":lord", "trp_badass_theo", "trp_guldur_healer"),

      (agent_is_active, ":agent1"),
      (agent_is_alive, ":agent1"),
      (agent_is_non_player, ":agent1"),

      #Should not be riding a horse
      (agent_get_horse, ":horse", ":agent1"),
      (le, ":horse", 0),
      
      (agent_get_team, ":agent1_team", ":agent1"),
      
      (set_fixed_point_multiplier, 100),
      (agent_get_position, pos89, ":agent1"),

      (try_for_agents, ":agent2", pos89, 100),
        (neq, ":agent1", ":agent2"),
        (agent_is_active, ":agent2"),
        (agent_is_alive, ":agent2"),
        (agent_is_human, ":agent2"),

        #Should not be riding a horse
        (agent_get_horse, ":horse2", ":agent2"),
        (le, ":horse2", 0),
      
        (agent_get_position, pos82, ":agent2"),
        (agent_get_team, ":agent2_team", ":agent2"),
        (neq, ":agent1_team", ":agent2_team"),
        
        (agent_get_bone_position, pos81, ":agent1", 6, 1),
        
        (assign, ":kicked", 0),
        (try_for_range, ":bone", 0, 20),
          (eq, ":kicked", 0),
          
          (agent_get_bone_position, pos82, ":agent2", ":bone", 1),
          
          (neg|position_is_behind_position, pos81, pos82),
          (get_distance_between_positions, ":dist", pos81, pos82),
          
          (le, ":dist", 25),
          
          (agent_get_animation, ":anim", ":agent1", 0),
          (eq, ":anim", "anim_kick_right_leg"),
          
          (agent_get_animation, ":anim", ":agent2", 0),
          (neq,":anim","anim_strike3_abdomen_front"),#Prevents mass kicking
          
          (agent_set_animation, ":agent2", "anim_strike3_abdomen_front"),#kicked
          (play_sound_at_position, "snd_blunt_hit", pos82),#Play dat phat bass boiz
          
          (store_random_in_range, ":dmg", 1, 6),
          (agent_deliver_damage_to_agent, ":agent1", ":agent2", ":dmg"),
          (assign, ":kicked", 1),
        (try_end),
      (try_end),
    (try_end),
])
#AI kicking end

#Attack/Block start
tld_melee_ai = (0, 0, 0, [(eq,"$field_ai_lord",1),

    (try_for_agents,":agent1"),
       #TLD Check
      (agent_get_troop_id, ":lord", ":agent1"),
      (this_or_next|is_between, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
      (this_or_next|eq, ":lord", "trp_nazgul"),
      (eq, ":lord", "trp_black_numenorean_sorcerer"),
    (try_end),
  ],
  [
    (store_mission_timer_a_msec, ":batch_time"),

    (try_for_agents,":agent1"),
      (agent_is_human, ":agent1"),
      (agent_is_active, ":agent1"),
      (agent_get_slot, ":check_time", ":agent1", slot_agent_tick_check_time),
      (try_begin), #Batching Start
        (ge, ":batch_time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
        (val_add, ":check_time", 100),
        (agent_set_slot, ":agent1", slot_agent_tick_check_time, ":check_time"),
        (try_begin),

           #TLD Check
          (agent_get_troop_id, ":lord", ":agent1"),
          (troop_slot_eq, ":lord", slot_troop_has_combat_ai, 1), 

          #(this_or_next|is_between, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
          #(this_or_next|eq, ":lord", "trp_black_numenorean_sorcerer"),
          #(is_between, ":lord", "trp_badass_theo", "trp_guldur_healer"),

          (agent_is_active,":agent1"),
          (agent_is_alive,":agent1"),
          
          (agent_ai_get_look_target, ":agent2", ":agent1"),
          (agent_is_active,":agent2"),
          (agent_is_alive,":agent2"),
          
          (agent_get_team, ":team1", ":agent1"),
          (agent_get_team, ":team2", ":agent2"),
          (neq, ":team1", ":team2"),
          
          (agent_get_position, pos81, ":agent1"),
          (agent_get_position, pos82, ":agent2"),
          
          (neg|position_is_behind_position, pos81, pos82),
          (get_distance_between_positions, ":dist", pos81, pos82),
          
          
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
      (try_end),
      (agent_get_slot, ":check_time", ":agent1", slot_agent_period_reset_time),
      (ge, ":batch_time", ":check_time"),#check agents in batches, splits the workload across as many frames as possible
      (val_add, ":check_time", "$batching_check_period"),
      (agent_set_slot, ":agent1", slot_agent_period_reset_time, ":check_time"),
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
      (this_or_next|eq, ":lord", "trp_nazgul"),
      (eq, ":lord", "trp_black_numenorean_sorcerer"),
      


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


tld_improved_horse_archer_ai =  (1, 0, 0, [ #Run it every 1 second instead of every half. Should be enough.

          (eq,"$field_ai_horse_archer",1),
          (neq, "$battle_won", 1),
          
  ],

  [       
        (set_fixed_point_multiplier, 1000),
        (try_for_agents, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_non_player, ":agent_no"),
            (agent_get_team, ":team_no", ":agent_no"),
            
            (agent_slot_eq, ":agent_no", slot_agent_positioned, 0), #InVain, from FormAI v5
            
            (try_begin),
                (this_or_next|all_enemies_defeated, ":team_no"),
                (agent_slot_eq, ":agent_no", slot_agent_is_running_away, 1),
                (agent_set_attack_action, ":agent_no", -2, 1),
                (assign, ":battle_over", 1),
            (try_end),
            
            (neq, ":battle_over", 1),
            
            (agent_get_troop_id, ":troop_id", ":agent_no"),
            (store_skill_level, ":horse_archery_level", "skl_horse_archery", ":troop_id"),
            (ge, ":horse_archery_level", 2), 

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
                #(assign, ":thrown_ammo", 0),
                (assign, ":ranged_weapon", -1),
                (try_for_range, ":item", 0, 4),
                  (agent_get_item_slot, ":item_weapon", ":agent_no", ":item"),
                  (gt, ":item_weapon", 0),
                  (item_get_type, ":item_weapon_type", ":item_weapon"),
                  (try_begin),
                    # (eq, ":item_weapon_type", itp_type_thrown),
                    # (agent_get_ammo_for_slot, ":ammo_for_slot", ":agent_no", ":item"),
                    # (val_add, ":thrown_ammo", ":ammo_for_slot"),
                  # (else_try),
                    (this_or_next|eq, ":item_weapon_type", itp_type_bow),
                    (this_or_next|eq, ":item_weapon_type", itp_type_thrown),
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
                #(val_sub, ":ammo", ":thrown_ammo"),
                (gt, ":ammo", 0),
                (agent_set_slot, ":agent_no", 1003, 2),
                (neg|eq, ":hold_fire", aordr_hold_your_fire),
                (neg|eq, ":weapon_usage_order", wordr_use_melee_weapons),
                (eq, ":movement_order", mordr_charge),
                (agent_get_position, pos100, ":agent_no"), 
                (agent_get_speed, pos91, ":agent_no"),
                (position_get_y,":speed_y",pos91),
                (assign, ":distance_closest", 100000),#1000m
                (assign, ":enemies_closest", -1),
                 #(try_for_agents, ":enemies"), #InVain: Get rid of this embedded full loop by checking cached or following enemies instead
                (agent_ai_get_num_cached_enemies, ":num_cached", ":agent_no"),
                (gt, ":num_cached", 0),
                (try_for_range, ":cached_index", 0, 3),
                    (agent_ai_get_cached_enemy, ":enemies", ":agent_no", ":cached_index"),    
                    (agent_is_active, ":enemies"), #double check
                    (agent_is_alive, ":enemies"),
                    (agent_is_human, ":enemies"),
                    (agent_get_position, pos96, ":enemies"),
                    (agent_get_team, ":enemies_team", ":enemies"),
                    (teams_are_enemies, ":team_no", ":enemies_team"),
                    (get_distance_between_positions, ":distance", pos100, pos96),
                    (try_begin),
                      (agent_slot_eq, ":enemies", slot_agent_is_running_away, 1),
                      (val_add, ":distance", 10000),
                    (try_end),
                    (try_begin),
                      (agent_get_horse, ":enemies_horse", ":enemies"),
                      (gt, ":enemies_horse", -1),
                      (agent_get_speed, pos92, ":enemies"),
                      (position_get_y,":speed_y_enemies",pos92),
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
                (agent_get_position, pos101, ":enemies_closest"),
                (get_distance_between_positions, ":distance_true", pos100, pos101),
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
                (try_begin), #InVain: This finetunes the archer's attack target and attack mode (also speed limit).
                            # This also is the reason for the synchronised shots. Without, HAs shoot too unreliably.
                    (agent_get_wielded_item, ":weapon_hold", ":agent_no", 0),
                    (gt, ":weapon_hold", 0),
                    (item_get_type, ":weapon_type", ":weapon_hold"),
                    (this_or_next|eq, ":weapon_type", itp_type_bow),
                    (this_or_next|eq, ":weapon_type", itp_type_thrown),
                    (eq, ":weapon_type", itp_type_musket),
                    (agent_get_bone_position, pos103, ":agent_no", 8, 1),
                    (agent_get_bone_position, pos104, ":enemies_closest", 9, 1),
                    (position_has_line_of_sight_to_position, pos103, pos104),
                    (agent_set_look_target_agent, ":agent_no", ":enemies_closest"),
                    (try_begin),
                      (assign, ":shoot_distance", 4000), #InVain: Can be used for further scaling
                      (try_begin),
                        (eq, ":weapon_type", itp_type_thrown),
                        (val_mul, ":shoot_distance", 2),
                        (val_div, ":shoot_distance", 3), 
                      (try_end),
                      (agent_get_attack_action, ":attack_action", ":agent_no"),
                      (eq, ":attack_action", 1),
                      (try_begin),
                        (gt, ":distance_closest", 700),
                        (le, ":distance_closest", ":shoot_distance"),
                        (store_mul, ":speed_limit", ":horse_archery_level", 4),
                        (val_sub, ":speed_limit", 10), #InVain: We use this for scaling: Force low-tier archers to slow down while shooting.
                        (val_max, ":speed_limit", 0),
                      (try_end),
                      #(eq, ":weapon_type", itp_type_bow),
                      (try_begin),
                        (le, ":distance_true", ":shoot_distance"),
                        (agent_set_defend_action, ":agent_no", -2, 1),
                        (store_random_in_range, ":chance", 0, 16),
                        (le, ":chance", ":horse_archery_level"),
                        (agent_set_attack_action, ":agent_no", 3, 0), #ready and release
                      (else_try),
                        (gt, ":distance_true", ":shoot_distance"),
                        (agent_set_attack_action, ":agent_no", -2, 1), #cancel
                        (agent_set_defend_action, ":agent_no", 3, 1),
                      (try_end),
                    (else_try),
                      #(eq, ":weapon_type", itp_type_bow),
                      (le, ":distance_true", ":shoot_distance"),#
                      (agent_get_combat_state, ":combat_state", ":agent_no"),
                      (neq, ":combat_state", 8),
                      (agent_set_attack_action, ":agent_no", 3, 1), #ready and hold
                    (try_end),
                (try_end),
                (agent_set_speed_limit, ":agent_no", ":speed_limit"),
                (try_begin), #InVain: This is the code for evading close enemies. Black magic.
                  (store_random_in_range, ":chance", 0, 10),
                    (try_begin),
                        (eq, ":weapon_type", itp_type_thrown), #skirmishers need a slight buff
                        (val_sub, ":chance", 2), 
                    (try_end),
                  (le, ":chance", ":horse_archery_level"),  #scaling: Better horse archers check distance more often. Bad HAs may get caught easier
                  (agent_slot_eq, ":enemies_closest", slot_agent_is_running_away, 0),
                  (lt, ":distance_closest", 10000),
                  (try_begin),
                    (get_scene_boundaries, pos112, pos113),
                    (position_transform_position_to_local, pos114, pos112,pos100),
                    (position_get_x, ":left", pos114),
                    (position_get_y, ":down", pos114),
                    (position_transform_position_to_local, pos114, pos112,pos113),
                    (position_get_x, ":map_width", pos114),
                    (position_get_y, ":map_height", pos114),
                    (store_sub, ":right", ":map_width", ":left"),
                    (store_sub, ":up", ":map_height", ":down"),
                    (position_transform_position_to_local, pos114, pos100, pos101),
                    (position_get_x, ":enemies_x", pos114),
                    (position_get_y, ":enemies_y", pos114),
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
                      (position_copy_origin, pos114, pos112),
                      (position_move_x, pos114, ":map_middle_x", 1),
                      (position_move_y, pos114, ":map_middle_y", 1),
                      (get_distance_between_positions,":distance_middle", pos114, pos100),
                      (position_transform_position_to_local, pos114, pos100, pos114),
                      (position_get_x, ":map_middle_x", pos114),
                      (position_get_y, ":map_middle_y", pos114),
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
                    (position_move_x, pos100, ":move_x", 0),
                    (position_move_y, pos100, ":move_y", 0),
                  (try_end),
                  (agent_set_scripted_destination, ":agent_no", pos100, 1),
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


# Order Weapon Type Triggers - Credit to Caba'drin (Kham)

order_weapon_type_triggers = [     
  (0, 0, 1, [(key_clicked, key_o)],
            [(val_add, "$weapon_order_type", 1),
             (val_mod, "$weapon_order_type", 5),
             (try_begin),
               (eq, "$weapon_order_type", 0),
               (assign, "$weapon_order_type", 1),
             (try_end), 
             (call_script, "script_order_weapon_type_switch", "$weapon_order_type"),]),

  (0, 0, 1, [(key_clicked, key_p)],
            [(val_add, "$shield_order_type", 1),
             (try_begin),
               (eq, "$shield_order_type", 1),
               (call_script, "script_order_weapon_type_switch", shield),
             (else_try),
               (call_script, "script_order_weapon_type_switch", noshield),
             (try_end),
             (val_mod, "$shield_order_type", 2)]),
]

# HP Shields - Credit to Vyrn team (Kham)
hp_shield_init = (ti_on_agent_spawn, 0, 0, [
  (store_trigger_param_1, ":agent"),
  (agent_is_human, ":agent"),
  (agent_get_troop_id, ":troop_id", ":agent"),
  (troop_get_slot, ":has_shield", ":troop_id", slot_troop_hp_shield),
  (gt, ":has_shield", 0)],
  
  [
    (store_trigger_param_1, ":agent"),
    (agent_is_human, ":agent"),
    (agent_get_troop_id, ":troop_id", ":agent"),
    (troop_get_slot, ":shield", ":troop_id", slot_troop_hp_shield),
    (agent_set_slot, ":agent", slot_agent_hp_shield_active, 1),
    (agent_set_slot, ":agent", slot_agent_hp_shield, ":shield"),
	
	(try_begin), #make up for reduced troll strength, also assign troll pushback cooldown
		(troop_get_type, ":race", ":troop_id"),
		(eq, ":race", tf_troll),
		(agent_set_max_hit_points, ":agent", 150,1),
		(store_mission_timer_a_msec, ":spawn_time"),
		(val_add, ":spawn_time", 30000),
		(agent_set_slot, ":agent", slot_agent_troll_swing_move, ":spawn_time"), #this slot is overwritten once mission time > spawn time +30 secs and if the troll qualifies for pushback
	(try_end),
		
	(try_begin), #player and companions
        (this_or_next|eq, ":troop_id", "trp_player"),
        (this_or_next|is_between, ":troop_id", "trp_npc1", heroes_begin),
        (is_between, ":troop_id", "trp_npc18", "trp_werewolf"),
        (store_skill_level, ":ironflesh",  skl_ironflesh, ":troop_id",),
        (val_mul, ":ironflesh", ":ironflesh"),
        (store_agent_hit_points, ":health", ":agent"),
        (val_mul, ":ironflesh", ":health"),
        (val_div, ":ironflesh", 200),
        (agent_set_slot, ":agent", slot_agent_hp_shield, ":ironflesh"),
    (try_end),
    
    #Debug
    # (assign, reg2, ":ironflesh"),
    # (str_store_troop_name, s33, ":troop_id"),
    # (display_message, "@{s33}: {reg2} set hp shield."),	 

  ])

hp_shield_trigger = (ti_on_agent_hit, 0, 0, [
  (store_trigger_param_1, ":agent"),

  (agent_slot_eq, ":agent", slot_agent_hp_shield_active, 1),

  (assign, ":continue", 0),
  (try_begin),
    (gt, "$nazgul_in_battle", 1), #There are nazguls
    (agent_is_active, "$temp2"),
    (assign, ":continue", 1),
  (else_try),
    (agent_is_human, ":agent"),
    (assign, ":continue", 1),
  (try_end),

  (eq, ":continue", 1),],
  
  [  
    (store_trigger_param_1, ":agent"),
    (store_trigger_param_2, ":dealer"),
    (store_trigger_param_3, ":damage"),
    
    (assign, ":weapon", reg0),
    (assign, ":deal_damage", 0),
    (gt, ":weapon", 0),

    (str_store_item_name, s2, ":weapon"),


    (item_get_type, ":type", ":weapon"),

    (get_player_agent_no, ":player"),
    (agent_get_troop_id, ":troop_id", ":agent"),

    (agent_get_slot, ":current_hp_shield", ":agent", slot_agent_hp_shield),

    ###non-trolls stagger###
    (try_begin),
        (neg|is_between, ":troop_id", "trp_moria_troll", "trp_multiplayer_profile_troop_male"),
        (neq, ":troop_id", "trp_npc21"), 
        (try_begin),
            (ge, ":damage", 30),
            (assign, ":deal_damage", 1),
            (agent_set_animation, ":agent", "anim_strike3_abdomen_front", 1),
          (else_try),
            (lt, ":current_hp_shield", 100),
            (ge, ":damage", 15),
            (assign, ":deal_damage", 3),
            (agent_set_animation, ":agent", "anim_strike3_abdomen_front", 1),
         (try_end),
     (try_end),
     ###non-trolls stagger end###

    ### TROLLS ###
    (try_begin),
      (this_or_next|is_between, ":troop_id", "trp_troll_of_moria", "trp_ent_old"), #old troll range
	  (is_between, ":troop_id", "trp_moria_troll", "trp_multiplayer_profile_troop_male"), #new troll range
      (gt, ":current_hp_shield", 0),

      #(assign, reg55, ":damage"),
      (agent_get_bone_position, pos1, ":agent", 7, 1),
      (get_distance_between_positions, ":dist", pos0, pos1),
      #(assign, reg57, ":dist"),
	  #(assign, reg56, ":damage"),
      #(display_message, "@{s2} weapon - {reg55} Before - {reg56} after - {reg57} Dist from Head"),

      (try_begin),
        (eq, ":type", itp_type_bow),
        (gt, ":dist", 30),
        (val_div, ":damage", 3),
	  (else_try), #buff spears and throwing spears, note: also affects swing attacks (blunt spears attacks, halberds etc)
		(this_or_next|item_has_property, ":weapon", itp_type_polearm),
        (item_has_property, ":weapon", itp_type_thrown),
		(item_get_thrust_damage_type, ":thrust_damage_type", ":weapon"),
		(eq, ":thrust_damage_type", 1), #check for spears, also finds halberds, bills etc
		(val_mul, ":damage", 3),
		(val_div, ":damage", 2),
		#(display_message, "@spear found"),
	  (else_try), #nerf blunt weapons		
		(item_get_thrust_damage_type, ":thrust_damage_type", ":weapon"),
		(neq, ":thrust_damage_type", 1), #exclude spears
		(item_get_swing_damage_type, ":swing_damage_type", ":weapon"),
		(eq, ":swing_damage_type", 2), #maces, hammers, clubs
		(val_mul, ":damage", 2),
		(val_div, ":damage", 3),
		#(display_message, "@blunt weapon found"),
      (try_end),

      (try_begin),
        (neg|item_has_property, ":weapon", itp_couchable),
        (ge, ":damage", 100),
        (val_div, ":damage", 2),
        (val_add, ":damage", 10),
		(agent_set_animation, ":agent", "anim_strike3_abdomen_front"),
		(play_sound, "snd_troll_hit"),
      (else_try),
        (item_has_property, ":weapon", itp_couchable),
        (ge, ":damage", 100),
		(troop_get_slot, ":hp_shield", ":troop_id", slot_troop_hp_shield),		
        (store_div, ":couched_damage", ":hp_shield", 3),
        (assign, ":damage", ":couched_damage"),
        (agent_set_animation, ":agent", "anim_strike3_abdomen_front"),
		(play_sound, "snd_troll_hit"),		
      (else_try),
        (ge, ":damage", 30),
        (agent_set_animation, ":agent", "anim_strike3_abdomen_front"),
		(play_sound, "snd_troll_hit"),
	  (else_try),
		(lt, ":current_hp_shield", 100),
        (ge, ":damage", 15),
        (agent_set_animation, ":agent", "anim_strike3_abdomen_front"),
		(play_sound, "snd_troll_hit"),
      (try_end),
    (try_end),
    ### TROLLS END ###

    (try_begin),
      (gt, ":current_hp_shield", 0),
      (val_sub, ":current_hp_shield", ":damage"),
      (val_max, ":current_hp_shield", 0),
      (agent_set_slot, ":agent", slot_agent_hp_shield, ":current_hp_shield"),  
    (else_try),
      (agent_set_slot, ":agent", slot_agent_hp_shield_active, 0),
    (try_end),
      
      #Debug
      #(assign, reg3, ":current_hp_shield"),
      #(display_message, "@Hp shield: {reg3} left."), 

   
    
    (try_begin),
      (eq, ":dealer", ":player"),
      (assign, reg60, ":damage"),
      (display_message, "@Delivered {reg60} damage."),
	  (set_show_messages, 0),
      (set_trigger_result, ":deal_damage"),

    (else_try),
		#(eq, ":dealer", ":player"),
      (set_trigger_result, ":deal_damage"),
    (try_end),
	
	(set_show_messages, 1),
    (assign, reg0, ":weapon"),

  ])  

## Health Restore on Kill Begin - Credit to Windyplains (Kham)
health_restore_on_kill = (ti_on_agent_killed_or_wounded, 0, 0, 
  [(store_trigger_param_1, ":agent_victim"),
   (store_trigger_param_2, ":agent_killer"),

   (agent_is_human, ":agent_victim"),
   (agent_get_troop_id, ":troop_killer", ":agent_killer"),

   (agent_get_wielded_item, ":weapon", ":agent_killer", 0),
   (ge, ":weapon", 0),
   (this_or_next|neg|item_has_property, ":weapon", itp_type_bow),
   (neg|item_has_property, ":weapon", itp_type_crossbow),

   (assign, ":continue", 0),
   (get_player_agent_no, ":agent_player"),

   (try_begin), 
      (troop_slot_eq, "trp_traits", slot_trait_berserker, 1), # Player has berserker trait?
      (troop_get_inventory_slot, ":armor", "trp_player", ek_body),
      (this_or_next|eq, ":armor", -1), #and is not wearing anything 
      (item_slot_eq, ":armor", slot_item_light_armor, 1), #or is the player wearing light armour / berserk appropriate clothing
      (eq, ":agent_killer", ":agent_player"),
      (assign, ":continue", 1),
   (else_try), # Is it a lord?
      (neq, ":agent_killer", ":agent_player"),
      (is_between, ":agent_killer", heroes_begin, heroes_end),
      (assign, ":continue", 1),
   (else_try),  #Berserkers
      (neq, ":agent_killer", ":agent_player"),
      (this_or_next|eq, ":troop_killer", "trp_npc9"), #Gulm
      (this_or_next|eq, ":troop_killer", "trp_i5_beorning_carrock_berserker"),
      (this_or_next|eq, ":troop_killer", "trp_i6_isen_uruk_berserker"),
      (this_or_next|eq, ":troop_killer", "trp_i4_gunda_orc_berserker"),
      (             eq, ":troop_killer", "trp_i5_khand_pit_master"),
      (assign, ":continue", 1),
   (try_end),

   (eq, ":continue", 1),

  ],
    
  [
    (store_trigger_param_1, ":agent_victim"),
    (store_trigger_param_2, ":agent_killer"),
      
    # Is this a valid kill worth gaining morale?
    (agent_is_human, ":agent_victim"),
    (agent_get_troop_id, ":troop_killer", ":agent_killer"),
    (get_player_agent_no, ":agent_player"),

    (assign, ":continue", 0),

    # Determine health amount to regenerate
    (try_begin), 
      (eq, ":agent_killer", ":agent_player"),
      (troop_slot_eq, "trp_traits", slot_trait_berserker, 1),# Player has berserker trait?
      (troop_get_inventory_slot, ":armor", "trp_player", ek_body),
      (this_or_next|eq, ":armor", -1), #and is not wearing anything 
      (item_slot_eq, ":armor", slot_item_light_armor, 1), #or is the player wearing light armour / berserk appropriate clothing
      (assign, ":health_regeneration", wp_hr_player_rate),
      (assign, ":continue", 1),
    (else_try), # Is it a lord?
      (neq, ":agent_killer", ":agent_player"),
      (is_between, ":agent_killer", heroes_begin, heroes_end),
      (assign, ":health_regeneration", wp_hr_lord_rate),
      (assign, ":continue", 1),
    (else_try),  #Berserkers
      (neq, ":agent_killer", ":agent_player"),
      (this_or_next|eq, ":troop_killer", "trp_npc9"), #Gulm
      (this_or_next|eq, ":troop_killer", "trp_i5_beorning_carrock_berserker"),
      (this_or_next|eq, ":troop_killer", "trp_i6_isen_uruk_berserker"),
      (this_or_next|eq, ":troop_killer", "trp_i4_gunda_orc_berserker"),
      (             eq, ":troop_killer", "trp_i5_khand_pit_master"),
      (assign, ":health_regeneration", wp_hr_berserker_rate),
      (assign, ":continue", 1),
    (try_end),
    
    (eq, ":continue", 1),
    # Adds in Strength as a bonus or penalty.  (STR - 10) / wp_hr_strength_factor
    
    (store_attribute_level, ":strength", ":troop_killer", ca_strength),
    (val_sub, ":strength", 10),
    (val_div, ":strength", wp_hr_strength_factor),
    (val_add, ":health_regeneration", ":strength"),
    
    (val_max, ":health_regeneration", 0), # We don't want a negative health regeneration.
    
    # Remove regeneration value if option not enabled for this unit type.
    (try_begin),  # Check if this is the player and regeneration is disabled.
      (eq, ":agent_killer", ":agent_player"),
      (eq, "$g_wp_player_hr_active", 0),
      (assign, ":health_regeneration", 0),
    (else_try),   # If not player assume AI troop and check if AI regen is disabled.
      (neq, ":agent_killer", ":agent_player"),  # To prevent player enabled, AI disabled conflicts.
      (eq, "$g_wp_ai_hr_active", 0),
      (assign, ":health_regeneration", 0),
    (try_end),
    
    # Displays debug messages if turned on.
    (try_begin), 
      (eq, wp_hr_debug, 1),
      (str_store_troop_name, s1, ":troop_killer"),
      (assign, reg0, ":health_regeneration"),
      (assign, reg1, ":strength"),   
      (display_message, "@DEBUG (Health Regen): {s1} regains {reg0}% health.  = +{reg1}% STR"),
    (try_end),
    
    # Regenerates the given health amount.
    (ge, ":health_regeneration", 1),
    (store_agent_hit_points, ":current_health", ":agent_killer", 0),
    (val_add, ":current_health", ":health_regeneration"),
    (agent_set_hit_points, ":agent_killer", ":current_health", 0),
  ])


nazgul_attack = (20, 0, ti_once, [
      (gt, "$nazgul_in_battle", 1), #Has to be 2 nazgul

      (store_mission_timer_a, ":mission_time_a"),
      (store_random_in_range, ":ran_time", 45, 60),
      (ge, ":mission_time_a", ":ran_time"), #Random time between 45 - 60 secs

      (store_random_in_range, ":random", 0, 100),
      (store_faction_of_party, ":faction", "p_main_party"),
      (faction_get_slot, ":side", ":faction", slot_faction_side),

      (le, ":random", 40), #40% Chance every 20 seconds

      (try_begin),
        (eq, ":side", faction_side_good),
        (assign, ":color", color_bad_news),
      (else_try),
        (eq, "$tld_war_began", 2),
        (eq, ":side", faction_side_hand),
        (assign, ":color", color_bad_news),
      (else_try),
        (assign, ":color", color_good_news),
      (try_end),


      (display_message, "@A Nazgul has joined the battle!", ":color"),
      (str_store_string, s30, "@Feeeeel.....ourrr.....wraaaath!"),
      (call_script, "script_troop_talk_presentation", "trp_nazgul", 7, 0),

      (get_player_agent_no, ":player"),
      (call_script, "script_find_exit_position_at_pos4", ":player"),
      (set_spawn_position, pos4), 

      (spawn_agent, "trp_nazgul"),
      (assign, "$temp2", reg0), #Save the nazgul agent
      (agent_set_team, "$temp2", 2),
      (agent_get_horse, ":nazgul_horse", "$temp2"),
      (agent_set_slot, ":nazgul_horse", slot_agent_hp_shield_active, 1),
      (agent_set_slot, ":nazgul_horse", slot_agent_hp_shield, 100000),
      (team_set_relation, 2, "$nazgul_team", 1),
      (agent_get_team, ":player_team", ":player"),
      (team_set_relation, ":player_team", 2, -1),
      (set_show_messages, 0),
      (team_give_order, 2, grc_everyone, mordr_charge),
      (set_show_messages, 1),

      ],

      [ (store_mission_timer_a, ":mission_time_a"),
        (agent_set_slot, "$temp2", slot_nazgul_timer, ":mission_time_a"),
        (set_show_messages, 0),
        (team_give_order, 2, grc_everyone, mordr_charge),
        (set_show_messages, 1),
    ])

nazgul_run_away = (20, 0, ti_once,
    [ 
      (gt, "$nazgul_in_battle", 1), #Has to be 2 nazgul
      
      (agent_is_active, "$temp2"),

      (store_mission_timer_a, ":mission_time_a"),
      (agent_get_slot, ":time_active", "$temp2", slot_nazgul_timer),
      (val_add, ":time_active", 60),
      (agent_get_kill_count, ":kills", "$temp2"),
      (this_or_next|ge, ":mission_time_a", ":time_active"),
      (ge, ":kills", 10),
    ],

    [
      (call_script, "script_find_exit_position_at_pos4", "$temp2"),
      (agent_start_running_away, "$temp2", pos4),
      (agent_set_scripted_destination_no_attack, "$temp2", pos4),

      (store_faction_of_party, ":faction", "p_main_party"),
      (faction_get_slot, ":side", ":faction", slot_faction_side),

      (try_begin),
        (eq, ":side", faction_side_good),
        (assign, ":color", color_bad_news),
      (else_try),
        (eq, "$tld_war_began", 2),
        (eq, ":side", faction_side_hand),
        (assign, ":color", color_bad_news),
      (else_try),
        (assign, ":color", color_good_news),
      (try_end),


      (display_message, "@The Nazgul is leaving the battle.", ":color"),
      (str_store_string, s30, "@It......Beckonsssss....."),
      (call_script, "script_troop_talk_presentation", "trp_nazgul", 7, 0),

    ])

tld_kill_or_wounded_triggers = (ti_on_agent_killed_or_wounded, 0, 0, [
    (this_or_next|check_quest_active, "qst_blank_quest_04"),
    (this_or_next|check_quest_active, "qst_blank_quest_05"),
    (this_or_next|check_quest_active, "qst_blank_quest_17"), #Bandit Kill quest
    (check_quest_active, "qst_oath_of_vengeance"), ],

    # trigger param 1 = defeated agent_id
    # trigger param 2 = attacker agent_id
    # trigger param 3 = wounded flag: 0 = agent is killed, 1 = agent is wounded
  [
    (store_trigger_param_1, ":killed"),
    (store_trigger_param_2, ":killer"),
    (store_trigger_param_3, ":result"),

    (agent_is_active, ":killed"),
    (agent_is_active, ":killer"),
    (agent_is_human, ":killed"),
    (agent_is_human, ":killer"),
    
    (agent_get_troop_id, ":troop_id", ":killed"),
    (troop_get_type, ":type", ":troop_id"),
    (get_player_agent_no, ":player"),
    (agent_get_team, ":player_team", ":player"),
    (agent_get_team, ":agent_team", ":killer"),

    (eq, ":agent_team", ":player_team"), #Is part of player's team?

    (try_begin),
      (check_quest_active, "qst_oath_of_vengeance"), #Oath of Vengeance Quest
      (neg|check_quest_succeeded, "qst_oath_of_vengeance"),
      (quest_get_slot, ":target","qst_oath_of_vengeance", 2),
      (quest_get_slot, ":moria", "qst_oath_of_vengeance",6),
      (quest_get_slot, ":gundabad", "qst_oath_of_vengeance",7),
      (this_or_next|eq, ":target", "fac_moria"),
      (this_or_next|eq, ":target", "fac_gundabad"),
      (this_or_next|eq, ":target", "fac_mordor"),
      (this_or_next|eq, ":target", "fac_isengard"),
      (this_or_next|gt, ":moria", 0),
      (gt, ":gundabad", 0),
      (eq, ":type", tf_troll),
      (this_or_next|eq, ":result", 0), #killed
      (eq, ":result", 1), #or wounded
      (val_add, "$oath_kills", 3),
    (try_end),

    (try_begin),
      (check_quest_active, "qst_blank_quest_04"), #Targeted Kill quest
      (neg|check_quest_succeeded, "qst_blank_quest_04"),
      (quest_get_slot, ":target", "qst_blank_quest_04", slot_quest_target_troop),
      (quest_get_slot, ":target_faction", "qst_blank_quest_04", slot_quest_target_faction),
      (store_character_level, ":target_level", ":target"),
      (quest_get_slot, ":current_amount", "qst_blank_quest_04", slot_quest_current_state),
      (quest_get_slot, ":target_amount", "qst_blank_quest_04", slot_quest_target_amount),
      (store_character_level, ":killed_level", ":troop_id"), 
      (store_faction_of_troop, ":troop_faction", ":troop_id"),
      (eq, ":target_faction", ":troop_faction"),
      (ge, ":killed_level", ":target_level"),
      (this_or_next|eq, ":result", 0), #killed
      (eq, ":result", 1), #or wounded
      (eq, ":killer", ":player"),
      (val_add, ":current_amount", 1),
      (quest_set_slot, "qst_blank_quest_04", slot_quest_current_state, ":current_amount"),

      #Debug
      #(assign, reg32, ":current_amount"),
      #(display_message, "@Kill Quest - {reg32}", color_good_news),

      (try_begin),
        (ge, ":current_amount", ":target_amount"),
        (call_script, "script_succeed_quest", "qst_blank_quest_04"),
      (try_end),

    (try_end),

    (try_begin),
      (check_quest_active, "qst_blank_quest_05"), #Faction Troop Kill Quest
      (neg|check_quest_succeeded, "qst_blank_quest_05"),
      (store_character_level, ":player_level", "trp_player"),
      (quest_get_slot, ":target_faction", "qst_blank_quest_05", slot_quest_target_faction),
      (quest_get_slot, ":current_amount", "qst_blank_quest_05", slot_quest_current_state),
      (quest_get_slot, ":target_amount", "qst_blank_quest_05", slot_quest_target_amount),
      (store_faction_of_troop, ":troop_faction", ":troop_id"),
      (eq, ":target_faction", ":troop_faction"),
      (this_or_next|eq, ":result", 0), #killed
      (eq, ":result", 1), #or wounded
      (try_begin),
        (gt, ":player_level", 20),
        (eq, ":killer", ":player"),
        (val_add, ":current_amount", 1),
      (else_try),
        (val_add, ":current_amount", 1),
      (try_end),

      (quest_set_slot, "qst_blank_quest_05", slot_quest_current_state, ":current_amount"),

      #Debug
      #(assign, reg33, ":current_amount"),
      #(display_message, "@Kill Quest Faction Troop - {reg33}", color_good_news),

      (try_begin),
        (ge, ":current_amount", ":target_amount"),
        (call_script, "script_succeed_quest", "qst_blank_quest_05"),
      (try_end),
    (try_end),

    (try_begin),
      (check_quest_active, "qst_blank_quest_17"), #Bandit Kill quest
      (neg|check_quest_succeeded, "qst_blank_quest_17"),
      (quest_get_slot, ":target", "qst_blank_quest_17", slot_quest_target_troop),
      (quest_get_slot, ":current_amount", "qst_blank_quest_17", slot_quest_current_state),
      (quest_get_slot, ":target_amount", "qst_blank_quest_17", slot_quest_target_amount),
      (eq, ":target", ":troop_id"),
      (this_or_next|eq, ":result", 0), #killed
      (eq, ":result", 1), #or wounded
      #(eq, ":killer", ":player"),
      (val_add, ":current_amount", 1),
      (quest_set_slot, "qst_blank_quest_17", slot_quest_current_state, ":current_amount"),

      #Debug
      #(assign, reg32, ":current_amount"),
      #(display_message, "@Kill Quest - {reg32}", color_good_news),

      (try_begin),
        (ge, ":current_amount", ":target_amount"),
        (call_script, "script_succeed_quest", "qst_blank_quest_17"),
      (try_end),

    (try_end),
  ])


#Batching Triggers:

batching_agent_spawn_human = (ti_on_agent_spawn, 0, 0, [], [(call_script, "script_cf_batching_ti_agent_spawn_human")])

batching_agent_spawn_mount = (ti_on_agent_spawn, 0, 0, [], [(call_script, "script_cf_batching_ti_agent_spawn_mount")])

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
    #(display_message, "@DEBUG: F1 Held"),
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
    #(display_message, "@DEBUG: F1 Let Go"),
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
#      (store_trigger_param, ":inflicted_agent_id", 1),
#      (agent_is_active,":inflicted_agent_id"),
#      (agent_is_human, ":inflicted_agent_id"),
#      (agent_is_alive, ":inflicted_agent_id"),
#    ], [
#      (store_trigger_param, ":inflicted_agent_id", 1),
#      (store_trigger_param, ":dealer_agent_id", 2),
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


battle_encounters_effects = [

(ti_before_mission_start, 0, ti_once, [

    (party_slot_eq, "p_main_party", slot_party_battle_encounter_effect, SARUMAN_STORM),

  ],[

  (set_rain, 1, 500),

]),

(ti_after_mission_start, 0, ti_once, [

  (party_get_slot, ":encounter_effect", "p_main_party", slot_party_battle_encounter_effect),
  (neq, ":encounter_effect", NO_EFFECT_PRESENT),

  ],[

  (party_get_slot, ":encounter_effect", "p_main_party", slot_party_battle_encounter_effect),
  (assign, ":fog_str", 500), #default

  (try_begin),
    (eq, "$small_scene_used", 1),
    (assign, ":fog_str", 1000),
  (try_end),

  (try_begin),
    (eq, ":encounter_effect", LORIEN_MIST),
    #(set_rain, 2,500), #yellow thingies in elven places
    (set_fog_distance,":fog_str",0xFFF09D),
    #(display_message, "@DEBUG: LORIEN_MIST"),
    (call_script, "script_lorien_mist_effect"), 
  (else_try),
    (eq, ":encounter_effect", SAURON_DARKNESS),
    (set_fog_distance,":fog_str",0x212020),
    (store_random_in_range, ":cloud_amount", 65, 90),
    (set_global_cloud_amount, ":cloud_amount"),
    #(display_message, "@DEBUG: SAURON_DARKNESS"),
    (call_script, "script_sauron_darkness_effect"), 
  (else_try),
    (eq, ":encounter_effect", SARUMAN_STORM),
    #(set_rain, 1,300), 
    (set_fog_distance, 500, 0x010101),
    (store_random_in_range, ":cloud_amount", 65, 90),
    (set_global_cloud_amount, ":cloud_amount"),
    #(display_message, "@DEBUG: SARUMAN_STORM"),
    (call_script, "script_saruman_storm_effect"), 
  (else_try),
    (eq, ":encounter_effect", GULDUR_FOG),
    (set_fog_distance,":fog_str",0x4B6047),
    #(display_message, "@DEBUG: GULDUR_FOG"),
    (call_script, "script_guldur_fog_effect"), 
  (try_end),

 ]),


# Thunder storms
  
  (3, 0.2, 5, [(party_slot_eq, "p_main_party", slot_party_battle_encounter_effect, SARUMAN_STORM), (store_random_in_range,":rnd",1,4),(eq,":rnd",1),(set_fog_distance, 200, 0xaaaaaa),],
        [(set_fog_distance, 500, 0x010101),(get_player_agent_no,":plyr"),(agent_play_sound, ":plyr", "snd_thunder"),(assign, "$lightning_cycle",1),]),
  (0.4,0.1, 5,[(party_slot_eq, "p_main_party", slot_party_battle_encounter_effect, SARUMAN_STORM), (eq,"$lightning_cycle",1),(set_fog_distance, 650, 0x777777),],   ###### Lightning afterflashes 
        [(set_fog_distance, 500, 0x010101),(assign,"$lightning_cycle",2),]),
  (0.5,0.1, 5,[(party_slot_eq, "p_main_party", slot_party_battle_encounter_effect, SARUMAN_STORM), (eq,"$lightning_cycle",2),(set_fog_distance, 620, 0x555555),],
        [(set_fog_distance, 500, 0x010101),(assign,"$lightning_cycle",0),]),


]

voice_commands = [(ti_on_order_issued,0,3, [
  
  #(store_trigger_param_1, ":order_issued"),
  (store_trigger_param_2, ":agent_id"),
  (get_player_agent_no, ":player"),
  (agent_is_alive, ":player"),
  (eq, ":agent_id", ":player"),

  ],[

  (store_trigger_param_1, ":order_issued"),
  (store_trigger_param_2, ":agent_id"),
  (get_player_agent_no, ":player"),
  (agent_is_alive, ":player"),
  (eq, ":agent_id", ":player"),

  (assign, ":sound_to_play", 0), # You can put a default sound here just in case. 

  (try_begin),
    (eq, ":order_issued", mordr_hold), #Hold Command
    (assign, ":sound_to_play", "snd_thunder"),  #add the sound you want here
  (else_try),
    (eq, ":order_issued", mordr_follow), #Follow Command
    (assign, ":sound_to_play", "snd_thunder"), 
  (else_try),
    (eq, ":order_issued", mordr_charge), #Charge Command
    (assign, ":sound_to_play", "snd_thunder"), 
  (else_try),
    (eq, ":order_issued", mordr_mount), #Mount Command
    (assign, ":sound_to_play", "snd_thunder"), 
  (try_end),

  (agent_play_sound, ":player", ":sound_to_play"),

]),

(0,0,3, [

  (assign, ":continue", 0),
  (assign, ":last_gk", gk_reverse_order_group),
  (get_player_agent_no, ":player"),
  (agent_is_alive, ":player"),
  (try_for_range, ":game_key", gk_everyone_hear, ":last_gk"),
    (game_key_clicked, ":game_key"),
    (assign, ":continue", 1),
    (assign, ":last_gk", 0), #loop breaker
  (try_end),

  (eq, ":continue", 1),

  ], [

  (get_player_agent_no, ":player"),
  (agent_is_alive, ":player"),

  (assign, ":continue", 0),
  (assign, ":last_gk", gk_reverse_order_group),

  (try_for_range, ":game_key", gk_everyone_hear, ":last_gk"),
    (game_key_clicked, ":game_key"),
    (assign, ":continue", 1),
    (assign, ":last_gk", 0), #loop breaker
    (assign, ":game_key_clicked", ":game_key"),
  (try_end),

  (eq, ":continue", 1),

  (assign, ":sound_to_play", 0), # You can put a default sound here just in case. 

  (try_begin),
    (eq, ":game_key_clicked", gk_everyone_hear),
    (assign, ":sound_to_play", "snd_thunder"), 
  (else_try), 
    (eq, ":game_key_clicked", gk_infantry_hear),
    (assign, ":sound_to_play", "snd_thunder"), 
  (try_end),
  (agent_play_sound, ":player", ":sound_to_play"),
])
]


# This code (set of triggers to be included in dynamic battle mission) allows character
# to shift into a bear form for a battle.
# Shapeshifters are identified by invisible armour and riding a bear
#
beorning_shapeshift = [

    # Change the form to alternative if one was selected, just prior battle
    (ti_before_mission_start, 0, ti_once, [], [
        (call_script, "script_cf_bear_form_selected"), (eq, reg0, 1),
        (assign, ":bear_troop", "trp_multiplayer_profile_troop_male"),
        (set_player_troop, ":bear_troop"),
    ]),
 
    # FIXING GRAPHIC GLITCH
    #by setting certain agents invisible (those who use invisible equipment)
    (ti_on_agent_spawn, 2.5, 0, [], [
        (store_trigger_param_1, ":agent"),
        (agent_is_human, ":agent"),
        (store_trigger_param_1, ":agent"),
        (agent_get_troop_id, ":troop", ":agent"),
        (this_or_next|is_between, ":troop", warg_ghost_begin, warg_ghost_end),
        (this_or_next|is_between, ":troop", "trp_spider", "trp_dorwinion_sack"),
        (this_or_next|is_between, ":troop", "trp_warg_ghost_1b", "trp_a2_isen_uruk_tracker"),
        (eq, ":troop", "trp_werewolf"),
        #(display_message, "@Agents glitch fix invisible"),
        (agent_set_visibility, ":agent", 0),
        #(display_message, "@Agents horse fix visible"),
        (agent_get_horse, ":horse", ":agent"),
        (agent_is_active, ":horse"),
        (agent_set_visibility, ":horse", 1),
    ]),

    # BEAR SETUP: After agent spawned
    # transfer stats from player clone troop to horse(bear) agent
    (ti_after_mission_start, 0, ti_once, [], [
        (get_player_agent_no, ":agent"),
        (agent_is_active, ":agent"),
        # If player agent is Beorning, those two are  set
        (call_script, "script_cf_bear_form_selected"), (eq, reg0, 1),

        (try_for_range, ":slot", ek_item_0, ek_horse),
            (troop_get_inventory_slot, ":item", "trp_player", ":slot"),
            (ge, ":item", 0), (agent_unequip_item, ":agent", ":item"),
        (end_try),
        (agent_equip_item, ":agent", "itm_warg_ghost_armour"),
        (agent_equip_item, ":agent", "itm_warg_ghost_lance", 1),
        (agent_set_wielded_item, ":agent", "itm_warg_ghost_lance"),
        (agent_equip_item, ":agent", "itm_empty_head"),
        (agent_equip_item, ":agent", "itm_empty_hands"),
        (agent_equip_item, ":agent", "itm_empty_legs"),

        # Remove the inventory bag out of player's reach
        # TODO this causes compiler warning
        (scene_prop_get_num_instances, ":max_inv", "spr_inventory"),
        (try_begin),
            (gt, ":max_inv", 0),
            (scene_prop_get_instance, ":prop_instance", "spr_inventory", 0),
            (prop_instance_get_position, pos1, ":prop_instance"),
            (position_move_z, pos1, -999),
            (prop_instance_set_position, ":prop_instance", pos1),
            (scene_prop_fade_out, ":prop_instance", 0),
        (try_end),

        # Set the visiblity of hidden rider and set proper health for the bear
        (agent_set_visibility, ":agent", 0),

        # Get the copied player alternative troop HP (has to be computed)
        (agent_get_troop_id, ":agent_troop", ":agent"),
        (store_attribute_level, ":bear_hp", ":agent_troop", ca_strength),
        (store_skill_level, ":ironflesh", skl_ironflesh, ":agent_troop"),
        (store_troop_health, ":curr_hp", ":agent_troop", 1),
        (val_add, ":bear_hp", 35), (val_mul, ":ironflesh", 2), (val_add, ":bear_hp", ":ironflesh"), 
        (val_mul, ":curr_hp", 3), # curr_bear_health = 3 x player_hp
        (val_mul, ":bear_hp", 3), # max_bear_hp = 3 x max_player_hp
 
        # Get bear agent and increase its hp
        (agent_get_horse, ":horse", ":agent"), (ge, ":horse", 0),
        (agent_set_max_hit_points, ":horse", ":bear_hp", 1),
        (agent_set_hit_points, ":horse", ":curr_hp", 1),
        (assign, reg1, ":bear_hp"), (assign, reg2, ":curr_hp"),
        (display_message, "@Your bear form has {reg2}/{reg1} HP!",0xff4040),

        (try_begin),
            (eq, "$cam_mode", 0),
            (assign, "$cam_mode", 4),
        (end_try),
    ]),

    # BEARFORM exit trigger: Leave area
    # NOTE This maybe source of bugs whenever player agent is not available
    (ti_on_leave_area, 0, 0, [(call_script, "script_cf_bear_form_selected"), (eq, reg0, 1),], [
        (call_script, "script_cf_select_human_form"),
    ]),

    # BEARFORM exit trigger: Leave area
    # NOTE This maybe source of bugs whenever player agent is not available
    (ti_on_player_exit, 0, 0, [(call_script, "script_cf_bear_form_selected"), (eq, reg0, 1),],[
        (call_script, "script_cf_select_human_form"),
    ]),

    # BEARFORM exit trigger: TAB pressed
    (ti_tab_pressed, 0, 0, [
        (this_or_next|eq, "$battle_won", 1), (this_or_next|eq, "$battle_won", 2),(main_hero_fallen),
        (call_script, "script_cf_bear_form_selected"), (eq, reg0, 1),
    ],[
        (call_script, "script_cf_select_human_form"),
    ]),

    # BEARFORM exit menu
    (ti_question_answered, 0, 0, [
        (store_trigger_param_1,":answer"),(eq,":answer",0),
        (call_script, "script_cf_bear_form_selected"), (eq, reg0, 1),],[
        (call_script, "script_cf_select_human_form"),
    ]),

    # BEARFORM dismounting action (should only be played for player)
    (ti_on_agent_dismount, 0, ti_once, [
        # Now check if agent that is dismounting is player agent (coz only he can be in bear form)
        (store_trigger_param_1, ":agent"),
        (get_player_agent_no, ":player_agent"), (eq, ":player_agent", ":agent"),
        (call_script, "script_cf_bear_form_selected"), (eq, reg0, 1),
    ],[
        (store_trigger_param_1, ":agent"),
        (store_trigger_param_2, ":horse"),
        (call_script, "script_cf_bearform_on_dismount", ":agent", ":horse"),
    ]),

    # Prevent unequiping empty weapon (triggers only in bearform)
    (ti_on_item_wielded, 0, 0, [
        (store_trigger_param_2,":item"), (neq, ":item", "itm_warg_ghost_lance"),
        (store_trigger_param_1,":agent"), (ge, ":agent", 0), (agent_is_active, ":agent"),
        (agent_get_horse, ":horse", ":agent"), (ge, ":horse", 0),
        (agent_is_active, ":horse"), (agent_is_alive, ":horse"),
        (agent_get_item_id, ":horse_item", ":horse"), (eq, ":horse_item", "itm_bear"),
    ],[
        (display_log_message, "@DEBUG: Ti on item wielded"),
        (store_trigger_param_1,":agent"),
        (store_trigger_param_2,":item"),
        (try_begin),
            (ge, ":item", 0),
            (agent_unequip_item, ":agent", ":item"),
            # (display_log_message, "@DEBUG: Unequip"),
        (end_try),
        (agent_equip_item, ":agent", "itm_warg_ghost_lance", 1),
        (agent_set_wielded_item, ":agent", "itm_warg_ghost_lance"),
        #(display_log_message, "@DEBUG: Item equipped"),
    ]),

    # Periodic weapon re-wield (2sec)
    (2, 0, 1, [
        (get_player_agent_no, ":agent"), (ge, ":agent", 0), (agent_is_active, ":agent"),
        (agent_get_horse, ":horse", ":agent"), (ge, ":horse", 0),
        (agent_is_active, ":horse"), (agent_is_alive, ":horse"),
        (agent_get_item_id, ":horse_item", ":horse"), 
        (eq, ":horse_item", "itm_bear"),
        #
        (agent_get_wielded_item, ":wielded", ":agent", 0),
        (neq, ":wielded", "itm_warg_ghost_lance"),
    ],[
        (omit_key_once, gk_drop_weapon),
        (get_player_agent_no, ":agent"),
        (agent_get_item_slot, ":weapon", ":agent", ek_item_0),

        (try_begin),
            (agent_has_item_equipped, ":agent", "itm_warg_ghost_lance"),
        (else_try), 
            (eq, ":weapon", -1),
            (agent_equip_item, ":agent", "itm_warg_ghost_lance", 1),
        (agent_set_wielded_item, ":agent", "itm_warg_ghost_lance"),
            (neq, ":weapon", -1),
            (agent_unequip_item, ":agent", "itm_warg_ghost_lance", 1),
            (agent_equip_item, ":agent", "itm_warg_ghost_lance", 1),
        (end_try),
        (agent_set_wielded_item, ":agent", "itm_warg_ghost_lance"),
    ]),

    # Dropping ghost lance gives you another one
    (0, 0.5, 0, [
        (game_key_clicked, gk_drop_weapon),
        (get_player_agent_no, ":agent"), (ge, ":agent", 0), (agent_is_active, ":agent"),
        (agent_get_horse, ":horse", ":agent"), (ge, ":horse", 0),
        (agent_is_active, ":horse"), (agent_is_alive, ":horse"),
        (agent_get_item_id, ":horse_item", ":horse"), 
        (eq, ":horse_item", "itm_bear"),
    ],[
        (get_player_agent_no, ":agent"),
        (agent_get_wielded_item, ":wielded", ":agent", 0),
        (neq, ":wielded", "itm_warg_ghost_lance"),
        (agent_equip_item, ":agent", "itm_warg_ghost_lance", 1),
        (agent_set_wielded_item, ":agent", "itm_warg_ghost_lance"),
    ]),


    # BEAR ATTACK TRIGGERING
    # Divided in two parts: etting animation and applying attack effects (delayed)
    #   Bear slap right/uppercut (LMB), cooldown 1.4s
    (0, 0, 1.4, [
        (game_key_clicked, gk_attack),
        # Check currently run anims
        (get_player_agent_no, ":agent_no"),(agent_is_alive, ":agent_no"),
        (agent_get_horse, ":horse", ":agent_no"), (ge, ":horse", 0), (agent_is_alive, ":horse"),
        (agent_get_animation, ":curr_anim_bear", ":horse", 0),
        (neg|is_between, ":curr_anim_bear", "anim_bear_slap_right", "anim_unused_horse_anim_12"),
        # Anims are simpler
        (this_or_next|is_between, ":curr_anim_bear", "anim_horse_stand", "anim_horse_rear"),
        (this_or_next|is_between, ":curr_anim_bear", "anim_horse_turn_right", 
            "anim_horse_fall_in_place"),
        (eq, ":curr_anim_bear", "anim_horse_walk_backward"),
        (neq, ":curr_anim_bear", "anim_horse_rear"),
    ],[

        # Check if agent is shapeshifted beorning
        (call_script, "script_cf_bear_form_selected"), (eq, reg0, 1),
 
        # Check if agent has right running speed
        (get_player_agent_no, ":agent_no"),(agent_get_horse, ":horse", ":agent_no"), 

        #(display_log_message, "@Bear SLAP anim triggered"),

        # Assign attack animation, knockback and play the first (for bear)
        (store_random_in_range, ":rnd_2", 0, 100),
        (try_begin),
            (le, ":rnd_2", 49),
            (assign, ":anim", "anim_bear_slap_right"),
        (else_try),
            (assign, ":anim", "anim_bear_uppercut"),
        (try_end),
        (agent_set_animation, ":horse", ":anim"),

        # Make sound
        (store_random_in_range, ":rnd_2", 0, 100),
        (try_begin),
          (le, ":rnd_2", 66), #66% chance to make sound
          (agent_play_sound, ":horse", "snd_bear_strike", sf_vol_14|sf_priority_12),
        (try_end),
    ]),

    # SLAM ATTACK ANIM (anim duration 1.6s, cooldown total : 2s)
    (0, 0, 2.0, [
        (game_key_clicked, gk_defend),
        # Check if agent is shapeshifted beorning
        (get_player_agent_no, ":agent_no"),
        (agent_is_alive, ":agent_no"), (agent_is_active, ":agent_no"),
        (agent_get_horse, ":horse", ":agent_no"), (ge, ":horse", 0),
        (agent_is_alive, ":horse"), (agent_is_active, ":horse"),

        # Start only if bear stands still or moves slowly
        (agent_get_animation, ":curr_anim_bear", ":horse", 0),
        (neg|is_between, ":curr_anim_bear", "anim_bear_slap_right", "anim_unused_horse_anim_12"),
        (this_or_next|is_between, ":curr_anim_bear", "anim_horse_stand", "anim_horse_pace_2"),
        (this_or_next|is_between, ":curr_anim_bear", "anim_horse_turn_right", 
            "anim_horse_fall_in_place"),
        (eq, ":curr_anim_bear", "anim_horse_walk_backward"),
        ],[

        # Check if player is beorning shapeshifter
        (call_script, "script_cf_bear_form_selected"), (eq, reg0, 1),

        # Get horse
        (get_player_agent_no, ":agent_no"),(agent_get_horse, ":horse", ":agent_no"),

        # Execute animation
        (agent_set_animation, ":horse", "anim_bear_slam"),

        #(display_log_message, "@Bear SLAM anim triggered"),
        # Make sound
        (store_random_in_range, ":rnd_2", 0, 100),
        (try_begin),
          (le, ":rnd_2", 70), #66% chance to make sound
          (agent_play_sound, ":horse", "snd_bear_strike", sf_vol_14|sf_priority_12),
        (try_end),
    ]),

    # LEAP ATTACK TRIGGER(ANIM)
    (0, 0, 1.5, [
        (game_key_clicked, gk_jump),
        
        # Check bear current anim
        (get_player_agent_no, ":agent_no"),(agent_is_alive, ":agent_no"),
        (agent_is_active, ":agent_no"),
        (agent_get_horse, ":horse", ":agent_no"),(ge, ":horse", 0), (agent_is_alive, ":horse"),
        (agent_is_active, ":horse"),

        # Stop if our horse(bear) is in the middle of attack already
        # Start only if bear stands still or moves slowly
        (agent_get_animation, ":curr_anim_bear", ":horse", 0),
        (neg|is_between, ":curr_anim_bear", "anim_bear_slap_right", "anim_unused_horse_anim_12"),

        # We have to be FAST OR SLOW..
        #(this_or_next|is_between, ":curr_anim_bear", "anim_horse_stand", "anim_horse_pace_4"),
        #(this_or_next|eq, ":curr_anim_bear", "anim_horse_walk_backward"),
        (this_or_next|is_between, ":curr_anim_bear", "anim_horse_stand", "anim_horse_rear"),
        (is_between, ":curr_anim_bear", "anim_horse_turn_right", "anim_horse_fall_in_place"),
    ],[
        # Check if player is beorning shapshifter
        (call_script, "script_cf_bear_form_selected"), (eq, reg0, 1),
    
        #(display_log_message, "@Bear LEAP anim triggered"),
        # Execute animation
        (get_player_agent_no, ":agent_no"),(agent_get_horse, ":horse", ":agent_no"), 
        (agent_set_animation, ":horse", "anim_warg_leapattack"),

        # Invincible charge
        (agent_set_invulnerable_shield, ":horse", 1),

        # Make sound
        (store_random_in_range, ":rnd_2", 0, 100),
        (try_begin),
          (le, ":rnd_2", 30), #30% chance to make sound
          (agent_play_sound, ":horse", "snd_bear_strike", sf_vol_14|sf_priority_12),
        (try_end),
    ]),

    # ATTACK EFFECTS
    # This trigger consequences are dealayed which mean bear should be playing attack 
    # animation while consequences are executed
    # BEAR SLAP/UPPERCUT/JUMP
    (0, 0.55, 0.85, [(this_or_next|game_key_clicked, gk_attack), (game_key_clicked, gk_jump),],[
         # Check if agent is in the middle of an attack
        (get_player_agent_no, ":agent_no"),
        (agent_is_alive, ":agent_no"),

        # We/our bear have to be alive
        (agent_get_horse, ":horse", ":agent_no"),
        (agent_is_active, ":horse"), (agent_is_alive, ":horse"),

        # Start if our horse(bear) is in the middle of attack
        (agent_get_animation, ":curr_anim_bear", ":horse", 0),
        (this_or_next|eq, ":curr_anim_bear", "anim_bear_slap_right"),
        (this_or_next|eq, ":curr_anim_bear", "anim_warg_leapattack"),
        (eq, ":curr_anim_bear", "anim_bear_uppercut"),

        #(display_message, "@Bear attack effect fired (SLAP/UPPERCUT)"),
 
        # Setup damage & execute the attack
        (agent_get_troop_id, ":agent_troop", ":agent_no"),
        (store_attribute_level, ":base_dmg", ":agent_troop", ca_strength),
        (store_skill_level, ":power_strike", skl_power_strike, ":agent_troop"),
        (val_add, ":base_dmg", ":power_strike"),
        (call_script, "script_bear_attack_no_anim", ":agent_no", ":base_dmg", ":curr_anim_bear"),
    ]),

    # Turn off bear shield
    (0, 1.3, 0.0, [(game_key_clicked, gk_jump),],[
        (get_player_agent_no, ":agent_no"), (agent_is_alive, ":agent_no"),
        # We/our bear have to be alive
        (agent_get_horse, ":horse", ":agent_no"),
        (agent_is_active, ":horse"), (agent_is_alive, ":horse"),

        (agent_get_animation, ":curr_anim_bear", ":horse", 0),
        (eq, ":curr_anim_bear", "anim_warg_leapattack"),

        (agent_set_invulnerable_shield, ":horse", 0),
    ]),

    # BEAR SLAM: Effect
    (0, 1.1, 1.0, [(game_key_clicked, gk_defend),],[
         # Check if agent is in the middle of an attack
        (get_player_agent_no, ":agent_no"),
        (agent_is_alive, ":agent_no"),

        # We/our bear have to be alive
        (agent_get_horse, ":horse", ":agent_no"),
        (agent_is_active, ":horse"), (agent_is_alive, ":horse"),

        # Start if our horse(bear) is in the middle of attack
        (agent_get_animation, ":curr_anim_bear", ":horse", 0),
        (eq, ":curr_anim_bear", "anim_bear_slam"),
     
        #(display_message, "@Bear attack effect fired (SLAM"),
        # Setup damage & execute the attack
        (agent_get_troop_id, ":agent_troop", ":agent_no"),
        (store_attribute_level, ":base_dmg", ":agent_troop", ca_strength),
        (store_skill_level, ":power_strike", skl_power_strike, ":agent_troop"),
        (val_add, ":base_dmg", ":power_strike"),
        (call_script, "script_bear_attack_no_anim", ":agent_no", ":base_dmg", ":curr_anim_bear"),
    ]),

    # BLOOD PARTICLES FOR SCRIPTED ATTACKS reg0 -> item_id
    (ti_on_agent_hit, 0.1, 0, [
        # Attack must deal damage and be dealt by an animal
        (store_trigger_param, ":dmg", 3), (gt, ":dmg", 9),
        # Only non-blunt dmg draws blood
        (ge, reg0, 0), (item_get_swing_damage_type, ":dmg_type", reg0),(neq, ":dmg_type", blunt),
        # Damager has to be an animal (all animals have scripted attacks with predetermined anims)
        (store_trigger_param, ":attacker", 2),
        (agent_get_horse, ":animal", ":attacker"), (ge, ":animal", 0),
        (agent_get_animation, ":attack_anim", ":animal", 0),
        (is_between, ":attack_anim", "anim_bear_slap_right", "anim_unused_horse_anim_12"),
    ],[
        # Check item damage
        (store_trigger_param, ":victim", 2),
        (store_trigger_param, ":dmg", 3),
        (item_get_swing_damage_type, ":dmg_type", reg0),
        (call_script, "script_cf_on_hit_blood", ":victim", ":dmg", ":dmg_type"),
    ]),
]

    
tld_bow_shield = [

# player only - check on equip
(ti_on_item_wielded, 0, 0, [
      (store_trigger_param_1, ":agent"),
      (get_player_agent_no, ":player"),
      (eq, ":player", ":agent")
    ],
    [(store_trigger_param_1, ":agent"),
     (store_trigger_param_2, ":equipped_item"),
      (agent_get_wielded_item, ":weapon", ":agent", 0),
      (gt, ":weapon", 0),
      (item_get_type, ":type", ":weapon"),
      (item_get_type, ":equipped_type", ":equipped_item"),
      #(eq, ":type", itp_type_bow), 
      (neg|item_has_property, ":equipped_item", itp_two_handed),
      (neg|item_has_property, ":weapon", itp_two_handed),
      (try_begin),
        (eq, ":type", itp_type_bow), 
          (agent_get_wielded_item, ":shield", ":agent", 1),
          (gt, ":shield", 0),
          (item_get_weapon_length, ":size",":shield"),
          (try_begin), #shield too big? Unwield
            (gt, ":size", 40),
            (agent_set_wielded_item, ":agent", -1), #this will unequip all items
            (display_message, "@Shield is too big to be used with a bow."),
            (assign, "$weapon_unequipped", ":equipped_item"),
            (val_mul, ":shield", -1),
            (assign, "$shield_unequipped", ":shield"),
          (else_try), #shield fits? Assign accuracy debuff
            (agent_slot_eq, ":agent", slot_agent_base_accuracy, 0), #slot not set yet? store original accuracy. We do this because environment effects can affect accuracy at mission start.
            (agent_get_accuracy_modifier, ":accuracy_mod", ":agent"),
            (agent_set_slot, ":agent", slot_agent_base_accuracy, ":accuracy_mod"),
            (store_skill_level, ":shield_skill", skl_shield, "trp_player"),
            (val_mul, ":shield_skill", 3),
            (store_sub, ":penalty", ":size", ":shield_skill"),
            (val_clamp, ":penalty", 5, 40),
            (val_sub, ":accuracy_mod", ":penalty"),
            (agent_set_accuracy_modifier, ":agent", ":accuracy_mod"),
          (else_try), #slot already set? check original accuracy!
            (agent_get_slot,":accuracy_mod",":agent", slot_agent_base_accuracy ),
            (gt, ":accuracy_mod", 0),
            (store_skill_level, ":shield_skill", skl_shield, "trp_player"),
            (val_mul, ":shield_skill", 3),
            (store_sub, ":penalty", ":size", ":shield_skill"),
            (val_clamp, ":penalty", 5, 40),
            (val_sub, ":accuracy_mod", ":penalty"),
            (agent_set_accuracy_modifier, ":agent", ":accuracy_mod"),
          (try_end),
      (else_try),
         (neq, ":equipped_type", itp_type_shield),
         (neq, ":equipped_type", itp_type_bow),
         (lt, "$shield_unequipped", 0),
         (val_mul, "$shield_unequipped", -1),
       (try_end),
    ]),

#Restore accuracy whenever shield or bow is unequipped (player and heroes)
(ti_on_item_unwielded, 0, 0, [
      (store_trigger_param_1, ":agent"),
      (agent_get_troop_id, ":troop", ":agent"),
      (troop_is_hero, ":troop"),
    ],
    [(store_trigger_param_1, ":agent"),
    #(agent_get_troop_id, ":troop", ":agent"),
    (store_trigger_param_2, ":item"),
    (item_get_type, ":type", ":item"),
    (this_or_next|eq, ":type", itp_type_bow),
    (eq, ":type", itp_type_shield),
    (agent_get_slot,":accuracy_mod",":agent", slot_agent_base_accuracy ),
    (gt, ":accuracy_mod", 0),
    (agent_set_accuracy_modifier, ":agent", ":accuracy_mod"),
    ]),

(0, 0.1, 0, [(gt, "$weapon_unequipped", 0)],
    [(get_player_agent_no, ":player"),
    (agent_set_wielded_item, ":player", "$weapon_unequipped"),
    (assign, "$weapon_unequipped", 0),
    ]),
    
(0, 0.1, 0, [(gt, "$shield_unequipped", 0)], 
    [(get_player_agent_no, ":player"),
    (agent_set_wielded_item, ":player", "$shield_unequipped"),
    (assign, "$shield_unequipped", 0),
    ]),

# Backup trigger, also tracks companions and heroes      
(2, 0, 0, [],
    [(try_for_agents, ":agent"),
      (agent_get_troop_id, ":troop", ":agent"),
      (troop_is_hero, ":troop"),
      (agent_get_wielded_item, ":weapon", ":agent", 0),
      (gt, ":weapon", 0),
      (item_get_type, ":type", ":weapon"),
      (eq, ":type", itp_type_bow), 
      (agent_get_wielded_item, ":shield", ":agent", 1),
      (gt, ":shield", 0),
      (item_get_weapon_length, ":size",":shield"),
      (try_begin), #shield too big? Unwield
        (gt, ":size", 40),
        (agent_set_wielded_item, ":agent", -1), #this will unequip all items
        (agent_set_wielded_item, ":agent", ":weapon"), #reequip bow
        (try_begin),
            (eq, ":troop","trp_player"),
            (display_message, "@Shield is too big to be used with a bow."),
        (try_end),
      (else_try), #shield fits? Assign accuracy debuff
        (agent_slot_eq, ":agent", slot_agent_base_accuracy, 0), #slot not set yet? store original accuracy. We do this because environment effects can affect accuracy at mission start.
        (agent_get_accuracy_modifier, ":accuracy_mod", ":agent"),
        (agent_set_slot, ":agent", slot_agent_base_accuracy, ":accuracy_mod"),
        (store_skill_level, ":shield_skill", skl_shield, ":troop"),
        (val_mul, ":shield_skill", 3),
        (store_sub, ":penalty", ":size", ":shield_skill"),
        (val_clamp, ":penalty", 5, 40),
        (val_sub, ":accuracy_mod", ":penalty"),
        (agent_set_accuracy_modifier, ":agent", ":accuracy_mod"),
      (else_try), #slot already set? check original accuracy for calculating debuff!
        (agent_slot_ge, ":agent", slot_agent_base_accuracy, 0),
        (agent_get_slot,":accuracy_mod",":agent", slot_agent_base_accuracy ),
        (store_skill_level, ":shield_skill", skl_shield, ":troop"),
        (val_mul, ":shield_skill", 3),
        (store_sub, ":penalty", ":size", ":shield_skill"),
        (val_clamp, ":penalty", 5, 40),
        (val_sub, ":accuracy_mod", ":penalty"),
        (agent_set_accuracy_modifier, ":agent", ":accuracy_mod"),
      (try_end),
     (try_end)
    ])
]


common_battle_init_banner = (
  ti_on_agent_spawn, 0, 0, [],
  [
    (store_trigger_param_1, ":agent_no"),
    (agent_get_troop_id, ":troop_no", ":agent_no"),
    (call_script, "script_troop_agent_set_banner", "tableau_game_troop_label_banner", ":agent_no", ":troop_no"),
  ])
  

tld_place_inventory_backup =   (0.1, 0, ti_once, [], [ #agent fadeout sphere test
        (scene_prop_get_num_instances, ":inv_found", "spr_inventory"),
        (try_begin),
          (lt, ":inv_found", 1),
          (get_player_agent_no, ":player"),
          (agent_get_position, pos1, ":player"),
          (set_spawn_position, pos1),
          (spawn_scene_prop, "spr_inventory"),
          #(display_message, "@inventory spawned"),
        (try_end),
    ])  
    
tld_ai_fadeout_spheres =   (3, 0, 0, [], [ #agent fadeout sphere test
    (scene_prop_get_num_instances, ":num_fadeout_spheres", "spr_ai_fadeout_sphere"),
    (set_fixed_point_multiplier, 100),
    (try_for_range, ":count", 0, ":num_fadeout_spheres"),
        (scene_prop_get_instance, ":instance_no", "spr_ai_fadeout_sphere", ":count"),
        (prop_instance_get_position, pos2, ":instance_no"),
        (prop_instance_get_scale, pos3, ":instance_no"),
        (position_get_scale_y, ":scale", pos3),
        (try_for_agents, ":agent_no", pos2, ":scale"),
            (agent_is_alive, ":agent_no"),
            (agent_get_position, pos4, ":agent_no"),
            (get_distance_between_positions, ":dist", pos2, pos4),
            (le, ":dist", ":scale"), #need to put this extra check because WSE breaks the try_for_agents operation
            (agent_fade_out, ":agent_no"),
            # (str_store_agent_name, s2, ":agent_no"),
            # (display_message, "@{s2} is in fadeout range"),
        (try_end),
    (try_end),
    ])    
    
tld_calculate_wounded = (ti_on_agent_killed_or_wounded, 0, 0, [], [ 
	(store_trigger_param_1, ":agent_no"),
    (agent_get_party_id, ":party_no", ":agent_no"),
    (ge, ":party_no", 0),
    (party_is_active, ":party_no"),
    (agent_get_troop_id, ":troop_no", ":agent_no"),
    (neg|troop_is_hero, ":troop_no"),
    
    #surgery
    (party_stack_get_troop_id, ":party_leader", ":party_no", 0),
    (store_skill_level, ":surgery", skl_surgery, ":party_leader"),    
    (try_begin),
        (eq, ":party_no", p_main_party),
        (party_get_skill_level, ":surgery", "p_main_party", skl_surgery),
    (try_end),        
    (assign, reg75, ":surgery"),
    (val_mul, ":surgery", 4),
    
    #troop level
    (store_character_level, ":chance", ":troop_no"), 
    (assign, reg76, ":chance"),
    (troop_get_type, ":race", ":troop_no"),
    (try_begin), 
        (is_between, ":race", tf_orc_begin, tf_orc_end),
        (val_mul, ":chance", 2),
        (val_div, ":chance", 3),
    (try_end),
    (val_add, ":chance", ":surgery"),
    #(val_div, ":chance", 100),
    (val_min, ":chance", 90),
    
    (assign, reg77, ":chance"),
    (str_store_agent_name, s55, ":agent_no"),
    (store_random_in_range, ":rnd", 0, 100),
    
    (try_begin),
        (le, ":rnd", ":chance"),
        (set_trigger_result, 2), #wound
        # (try_begin),
            # (agent_is_ally, ":agent_no"),
            # (display_message, "@{s55} wounded, surgery {reg75}, level {reg76}, chance: {reg77}"),
        # (try_end),
    (else_try),
        (set_trigger_result, 1), #kill
        # (try_begin),
            # (agent_is_ally, ":agent_no"),
            # (display_message, "@{s55} killed, surgery {reg75}, level {reg76}, chance: {reg77}"),
        # (try_end),
    (try_end),        
    ])
    
tld_ai_melee_spheres =   (3, 0, 0, [], [ #agent fadeout sphere test
    (scene_prop_get_num_instances, ":num_spheres", "spr_ai_melee_on_off_var1"),
    (set_fixed_point_multiplier, 100),
    (try_for_range, ":count", 0, ":num_spheres"),
        (scene_prop_get_instance, ":instance_no", "spr_ai_melee_on_off_var1", ":count"),
        (prop_instance_get_position, pos2, ":instance_no"),
        (prop_instance_get_scale, pos3, ":instance_no"),
        (prop_instance_get_variation_id, ":value", ":instance_no"),
        (position_get_scale_y, ":scale", pos3),
        (try_for_agents, ":agent_no", pos2, ":scale"),
            (agent_is_alive, ":agent_no"),
            (neg|agent_is_defender, ":agent_no"),
            (agent_get_position, pos4, ":agent_no"),
            (get_distance_between_positions, ":dist", pos2, pos4),
            (le, ":dist", ":scale"), #need to put this extra check because WSE breaks the try_for_agents operation
            (agent_ai_set_always_attack_in_melee, ":agent_no", ":value"),
            # (str_store_agent_name, s5, ":agent_no"),
            # (assign, reg77, ":value"),
            # (display_message, "@{s5} set to {reg77}"),
        (try_end),
    (try_end),
    ]) 
    
tld_animated_town_agents = [
  (0.3, 0, 0, [], [ #animated agents WB only
    
    #wood hackers
    (call_script, "script_animate_town_agents", spr_troop_work_wood_hacker_1h, 3, 3, itm_civilian_woodaxe_1h),
    (call_script, "script_animate_town_agents", spr_troop_work_wood_hacker_2h, 4, 3, itm_civilian_woodaxe_2h),
    (call_script, "script_animate_town_agents", spr_troop_work_tree_feller, 4, 1, itm_civilian_woodaxe_2h),   
    
    #hammerer
    (call_script, "script_animate_town_agents", spr_troop_work_hammer, 2, 3, itm_civilian_hammer),

    #farmers
    (call_script, "script_animate_town_agents", spr_troop_work_farmer_mattock, 4, 3, itm_civilian_war_mattock),
    (call_script, "script_animate_town_agents", spr_troop_work_farmer_shovel, 2, 0, itm_civilian_shovel), #doesn't work so well
    
    #miners use two attack actions, so we fire the script twice with higher pause count
    (call_script, "script_animate_town_agents", spr_troop_work_miner, 6, 4, itm_civilian_pickaxe),
    #(call_script, "script_animate_town_agents", spr_troop_civilian_miner, 6, 1), 
    
    #smiths
    (call_script, "script_animate_town_agents", spr_troop_smith, 3, 3, itm_civilian_hammer), 
    
    (call_script, "script_animate_town_agents", spr_troop_work_butcher, 4, 3, itm_orc_axe),
    
    (call_script, "script_animate_town_agents", spr_troop_guard_fight_single, 5, 4, itm_practice_staff),
      ]),

  (1, 0, 0, [], [ #oh no and cheer
    (get_player_agent_no, ":player_agent"),
    (agent_get_position, pos4, ":player_agent"),
    (set_fixed_point_multiplier, 100),
    
    #oh no
    (scene_prop_get_num_instances, ":num_props", "spr_troop_human_prisoner_oh_no"),
    (try_for_range, ":count", 0, ":num_props"),
        (scene_prop_get_instance, ":instance_no", "spr_troop_human_prisoner_oh_no", ":count"),
        (prop_instance_get_position, pos2, ":instance_no"),
        (scene_prop_get_slot, ":agent", ":instance_no", slot_prop_agent_1),
        (prop_instance_get_position, pos3,":instance_no"),
        (get_distance_between_positions, ":distance", pos3, pos4),
        (is_between, ":distance", 350, 3000), #only if player isn't too close, but also not too far either (avoid too many sounds)
        (agent_set_scripted_destination, ":agent", pos2),
        (agent_get_animation, ":cur_animation", ":agent", 1),
        (neq, ":cur_animation", "anim_nazgul_noooo_long"),
        (store_random_in_range, ":chance", 0, 100),
        (le, ":chance", 60),
        (agent_set_animation, ":agent", "anim_nazgul_noooo_short"),
        (le, ":chance", 30),
        (agent_set_animation, ":agent", "anim_nazgul_noooo_long"),
        #(agent_set_animation_progress, ":agent", ":chance"),
        (le, ":chance", 4),
        (agent_stop_sound, ":agent"),
        (agent_play_sound,":agent","snd_horror_scream_man"),
    (try_end),

    #cheer
    (scene_prop_get_num_instances, ":num_props", "spr_troop_civ_cheer"),
    (try_for_range, ":count", 0, ":num_props"),
        (scene_prop_get_instance, ":instance_no", "spr_troop_civ_cheer", ":count"),
        (prop_instance_get_position, pos2, ":instance_no"),
        (scene_prop_get_slot, ":agent", ":instance_no", slot_prop_agent_1),
        (prop_instance_get_position, pos3,":instance_no"),
        (get_distance_between_positions, ":distance", pos3, pos4),
        (is_between, ":distance", 350, 3000), #only if player isn't too close, but also not too far either (avoid too many sounds)
        (agent_set_scripted_destination, ":agent", pos2),
        (store_random_in_range, ":chance", 0, 100),
        (le, ":chance", 25),
        (agent_set_animation, ":agent", "anim_cheer"),
        (le, ":chance", 4),
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

    #worker stand
    (scene_prop_get_num_instances, ":num_props", "spr_troop_work_stand"),
    (try_for_range, ":count", 0, ":num_props"),
        (scene_prop_get_instance, ":instance_no", "spr_troop_work_stand", ":count"),
        (prop_instance_get_position, pos2, ":instance_no"),
        (scene_prop_get_slot, ":agent", ":instance_no", slot_prop_agent_1),
        (agent_set_scripted_destination, ":agent", pos2),
        (store_random_in_range, ":chance", 0, 100),
        (le, ":chance", 45),
        (agent_set_animation, ":agent", "anim_defend_up_staff_keep"),
        (le, ":chance", 30),
        (agent_set_animation, ":agent", "anim_defend_up_twohanded_keep"),
        (le, ":chance", 15),
        (agent_set_animation, ":agent", "anim_defend_up_onehanded_keep"),
    (try_end),

    #worker table
    (scene_prop_get_num_instances, ":num_props", "spr_troop_work_table"),
    (try_for_range, ":count", 0, ":num_props"),
        (scene_prop_get_instance, ":instance_no", "spr_troop_work_table", ":count"),
        (prop_instance_get_position, pos2, ":instance_no"),
        (scene_prop_get_slot, ":agent", ":instance_no", slot_prop_agent_1),
        (agent_set_scripted_destination, ":agent", pos2),
        (agent_set_look_target_position, ":agent", pos2),
        (store_random_in_range, ":chance", 0, 100),
        (assign, ":sound", 0),
        (try_begin),
            (le, ":chance", 45),
            (assign, ":sound", "snd_pull_bow"),
            (agent_set_animation, ":agent", "anim_defend_forward_staff"),
            (le, ":chance", 30),
            (agent_set_animation, ":agent", "anim_defend_forward_onehanded"),
            (le, ":chance", 15),
            (assign, ":sound", "snd_pull_arrow"),
            (agent_set_animation, ":agent", "anim_defend_forward_greatsword"),
        (try_end),
        (gt, ":sound", 0),
        (agent_play_sound, ":agent", ":sound"),
    (try_end),

    #priests / worshippers
    (scene_prop_get_num_instances, ":num_props", "spr_troop_priest"),
    (try_for_range, ":count", 0, ":num_props"),
        (scene_prop_get_instance, ":instance_no", "spr_troop_priest", ":count"),
        (prop_instance_get_position, pos2, ":instance_no"),
        (scene_prop_get_slot, ":agent", ":instance_no", slot_prop_agent_1),
        (agent_set_scripted_destination, ":agent", pos2),
        (store_random_in_range, ":chance", 0, 100),
        (le, ":chance", 15),
        (agent_set_animation, ":agent", "anim_troll_roar"),
    (try_end),

    #refill training archers
    (scene_prop_get_num_instances, ":num_props", "spr_troop_archer_fight_single"),
    (try_for_range, ":count", 0, ":num_props"),
        (scene_prop_get_instance, ":instance_no", "spr_troop_archer_fight_single", ":count"),
        (scene_prop_get_slot, ":agent", ":instance_no", slot_prop_agent_1),
        (agent_refill_ammo, ":agent"),
    (try_end),
 
    #turn fighting on/off based on distance, to avoid sounds
    (try_for_prop_instances, ":instance_no"),
        (prop_instance_get_scene_prop_kind, ":prop_type", ":instance_no"),
        (this_or_next|eq, ":prop_type", "spr_troop_guard_fight_duel"),
        (this_or_next|eq, ":prop_type", "spr_troop_troll_fight_duel"),
        (eq, ":prop_type", "spr_troop_archer_fight_single"),
        #(display_message, "@prop found"),
        (try_begin),
            (scene_prop_get_slot, ":fighter_1", ":instance_no", slot_prop_agent_1),
            (scene_prop_get_slot, ":fighter_2", ":instance_no", slot_prop_agent_2),
            (agent_get_position, pos5, ":fighter_1"),
            (get_distance_between_positions, ":dist", pos4, pos5),
            (ge, ":dist", 3000),
            #(assign, reg78, ":dist"),
            #(display_message, "@distance: {reg78}"),
            (agent_clear_relations_with_agents, ":fighter_1"),
            (agent_clear_relations_with_agents, ":fighter_2"),
            #(display_message, "@stop fight"),
         (else_try),
            (lt, ":dist", 3000),
            (agent_add_relation_with_agent, ":fighter_1", ":fighter_2", -1),
            (ge, ":fighter_2", 1),
            (agent_add_relation_with_agent, ":fighter_2", ":fighter_1", -1),
            #(display_message, "@start fight"),
        (try_end),
    (try_end),
      ]),        
]

tld_positional_sound_props = [


  (3, 0, 0, [], [ # positional sounds
    (set_fixed_point_multiplier, 100),
    (get_player_agent_no, ":player_agent"),
    (agent_get_position, pos4, ":player_agent"),
    (scene_prop_get_num_instances, ":num_props", "spr_sound_emitter_var1x10_plus_var2_scalable"),
    (try_for_range, ":count", 0, ":num_props"),
        (scene_prop_get_instance, ":instance_no", "spr_sound_emitter_var1x10_plus_var2_scalable", ":count"),
        (prop_instance_get_variation_id, ":sound", ":instance_no"),
        (val_mul, ":sound", 10),
        (prop_instance_get_variation_id_2, ":sound_2", ":instance_no"),
        (val_add, ":sound", ":sound_2"),
        (assign, reg76, ":sound"), 
        (prop_instance_get_scale, pos2, ":instance_no"),
        (position_get_scale_x, ":range", pos2),
        (val_sub, ":range", 100),
        (val_mul, ":range", 100),
        (prop_instance_get_position, pos3, ":instance_no"),
        (get_distance_between_positions, ":distance", pos3, pos4),
        # (assign, reg77, ":distance"),
        # (assign, reg78, ":range"),
        # (display_message, "@distance {reg77}/{reg78}"),
        (le, ":distance", ":range"),
        (scene_prop_slot_eq, ":instance_no", slot_prop_playing_sound, 0),
        (gt, ":sound", 0),
        (prop_instance_play_sound, ":instance_no", ":sound"),
        #(display_message, "@play_sound {reg76};"),
        (scene_prop_set_slot, ":instance_no", slot_prop_playing_sound, 1),
    (else_try),
        (gt, ":distance", ":range"),
        (scene_prop_slot_eq, ":instance_no", slot_prop_playing_sound, 1),
        (prop_instance_stop_sound, ":instance_no"),
        (scene_prop_set_slot, ":instance_no", slot_prop_playing_sound, 0),
        #(display_message, "@stop sound"),
    (try_end),
      ]),

  (3, 0, 0, [], [ # ambient sounds
    (set_fixed_point_multiplier, 100),
    (get_player_agent_no, ":player_agent"),
    (agent_get_position, pos4, ":player_agent"),
    (scene_prop_get_num_instances, ":num_props", "spr_sound_emitter_ambient_var1x10_plus_var2_scalable"),
    (try_for_range, ":count", 0, ":num_props"),
        (scene_prop_get_instance, ":instance_no", "spr_sound_emitter_ambient_var1x10_plus_var2_scalable", ":count"),
        (prop_instance_get_variation_id, ":sound", ":instance_no"),
        (val_mul, ":sound", 10),
        (prop_instance_get_variation_id_2, ":sound_2", ":instance_no"),
        (val_add, ":sound", ":sound_2"),
        (assign, reg76, ":sound"), 
        (prop_instance_get_scale, pos2, ":instance_no"),
        (position_get_scale_x, ":range", pos2),
        (val_sub, ":range", 100),
        (val_mul, ":range", 100),
        (prop_instance_get_position, pos3, ":instance_no"),
        (get_distance_between_positions, ":distance", pos3, pos4),
        # (assign, reg77, ":distance"),
        # (assign, reg75, ":range"),
        # (display_message, "@distance {reg77}/{reg75}"),
        (le, ":distance", ":range"),
        (eq, "$play_ambient_sounds", 1),
        (scene_prop_slot_eq, ":instance_no", slot_prop_playing_sound, 0),
        (gt, ":sound", 0),
        (stop_all_sounds, 0), #stop looping sounds
        (assign, "$play_ambient_sounds", 0), 
        (prop_instance_play_sound, ":instance_no", ":sound", sf_looping|sf_2d|sf_vol_15),
        (scene_prop_set_slot, ":instance_no", slot_prop_playing_sound, 1),
        #(display_message, "@play_sound {reg76}"),
    (else_try),
        (gt, ":distance", ":range"),
        (scene_prop_slot_eq, ":instance_no", slot_prop_playing_sound, 1),
        (prop_instance_stop_sound, ":instance_no"),
        (scene_prop_set_slot, ":instance_no", slot_prop_playing_sound, 0),
        (assign, "$play_ambient_sounds", 1),
        #(display_message, "@back to normal sounds"),
        
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

    (try_end),
      ]),

  (2, 0, 0, [], [ # positional fire sounds #workaround to prevent sound overflow if a town scene has lots of fire props like campfires, torches, lamps
    (set_fixed_point_multiplier, 100),
    (get_player_agent_no, ":player_agent"),
    (agent_get_position, pos4, ":player_agent"),
    (assign, ":count", 0),
    (try_for_prop_instances, ":instance_no"),
        (scene_prop_get_slot, ":sound", ":instance_no", slot_prop_sound),
        (this_or_next|eq, ":sound", "snd_fire_loop"),
        (eq, ":sound", "snd_torch_loop"),
        (try_begin),
            (prop_instance_get_position, pos3, ":instance_no"),
            (get_distance_between_positions, ":distance", pos3, pos4),
            (le, ":distance", 2000), #20m, need some range to fade in and out
            (scene_prop_slot_eq, ":instance_no", slot_prop_playing_sound, 0),
            (lt, ":count", 3), #not more than 3 at a time
            #(gt, ":sound", 0),
            (prop_instance_play_sound, ":instance_no", "snd_torch_loop"), 
            (scene_prop_set_slot, ":instance_no", slot_prop_playing_sound, 1),
            (val_add, ":count", 1),
            # (assign, reg78, ":count"),
            # (display_message, "@count: {reg78}"),
        (else_try),
            (lt, ":distance", 2000),
            (scene_prop_slot_eq, ":instance_no", slot_prop_playing_sound, 1),
            (val_add, ":count", 1), #important to also count the props that are already playing
        (else_try),    
            (gt, ":distance", 2000),
            (prop_instance_stop_sound, ":instance_no"),
            (scene_prop_set_slot, ":instance_no", slot_prop_playing_sound, 0),
        (else_try), 
            (ge, ":count", 3), #many sound sources around? Remove some earlier.
            (gt, ":distance", 1000),
            (prop_instance_stop_sound, ":instance_no"),
            (scene_prop_set_slot, ":instance_no", slot_prop_playing_sound, 0),        
        (try_end),
    (try_end),
      ]),
]
      
tld_points_of_interest = [
   
  #distance check for PoI and guardians, check requirements and apply consequences
  (1.5, 0, 0, [], [ 
    (set_fixed_point_multiplier, 100),
    (get_player_agent_no, ":player_agent"),
    (agent_get_position, pos4, ":player_agent"),
    (store_current_scene, ":scene"),
    (call_script, "script_get_faction_rank", "$ambient_faction"),
    (assign, ":rank", reg0),
    (store_character_level, ":player_level", "trp_player"),
    (agent_get_horse, ":player_mount", ":player_agent"),    
    (store_time_of_day, ":time"),
    #(assign, "$temp_2", 0), #for spawn control on scene props, particle effects etc.
    
    (try_for_prop_instances, ":instance_no", "spr_secret_point_of_interest"), #points of interest
        (scene_prop_slot_eq, ":instance_no", scene_prop_open_or_close_slot, 0), #we use a slot prop so we can also add explorations points that don't give a reward / don't need a party slot
        (prop_instance_get_variation_id, ":var1", ":instance_no"),
        (prop_instance_get_position, pos5, ":instance_no"),
        (get_distance_between_positions, ":dist", pos4, pos5),
        # (assign, reg78, ":dist"),
        # (assign, reg77, ":instance_no"),
        # (display_message, "@POI {reg77} distance {reg78}"),
        
        (try_begin),
            (eq, ":scene", scn_minas_tirith_center),
            (eq, ":var1", 1),
            (neg|party_slot_eq, "$current_town", slot_exploration_point_1, 1),
            (neg|is_currently_night),
            (lt, ":dist", 1000),
            #(tutorial_message, "@You happen upon an Old Guesthouse. As you inspect the weathered stone building, you notice a group of boys playing among the pillars, the only children you have seen in Minas Tirith.  One of them greets at you and you wave back, with your heart lightened for a brief moment from the sorrow of war.", 0 , 10),
            (display_message, "@You happen upon an Old Guesthouse. As you inspect the weathered stone building, you notice a group of boys playing among the pillars, the only children you have seen in Minas Tirith.  One of them greets you and you wave back. Your heart is gladdened and you forget, for a brief moment, the sorrow of war."),
            (add_xp_as_reward, 100),
            (call_script, "script_change_player_party_morale", 35),
            (call_script, "script_change_player_relation_with_center", "$current_town", 3),
            (party_set_slot, "$current_town", slot_exploration_point_1, 1),
            (scene_prop_set_slot, ":instance_no", scene_prop_open_or_close_slot, 1), #used            

        (else_try),
            (eq, ":scene", scn_henneth_annun_castle),
            (eq, ":var1", 1),
            (is_between, ":time", 18, 21),
            (try_begin),
              (eq, "$temp_2", 0),
              (set_spawn_position, pos5),
              (spawn_scene_prop, "spr_moon_beam"),
              (spawn_scene_prop, "spr_moon_beam"),
              (spawn_scene_prop, "spr_moon_beam"),
              (assign, "$temp_2", 1),
            (try_end),            
            (lt, ":dist", 400),
            (neg|party_slot_eq, "$current_town", slot_exploration_point_1, 1),            
            (display_message, "@You look through Henneth Annun, the Window of the Sunset. The beautiful sight restores your faith in the West and the Powers beyond."),
            (add_xp_as_reward, 100),
            (call_script, "script_change_player_party_morale", 35),
            (call_script, "script_change_player_relation_with_center", "$current_town", 3),
            (call_script, "script_increase_rank", "$ambient_faction", 10),
            (party_set_slot, "$current_town", slot_exploration_point_1, 1),
            (scene_prop_set_slot, ":instance_no", scene_prop_open_or_close_slot, 1), #used              

        (else_try), #Cirith Ungol Stairs
            (eq, ":scene", scn_minas_morgul_center),
            (eq, ":var1", 1),
            (neg|party_slot_eq, "$current_town", slot_exploration_point_1, 1),
            (lt, ":dist", 1000),
            (display_message, "@As you follow the straight stairs, cut into the rock of the mountain, and then a second set of stairs, winding as it clings to the cliff-face, you realize that you should not pursue this path any further if you value your own life."),
            (play_sound, "snd_spider"),
            (add_xp_as_reward, 500),
            (call_script, "script_change_player_relation_with_center", "$current_town", 3),
            (scene_prop_set_slot, ":instance_no", scene_prop_open_or_close_slot, 1), #used
            (party_set_slot, "$current_town", slot_exploration_point_1, 1),
           
        (else_try), #Minas Morgul citadel
            (eq, ":scene", scn_minas_morgul_center),
            (eq, ":var1", 2),
            (neg|party_slot_eq, "$current_town", slot_exploration_point_2, 1),
            (lt, ":dist", 8500),
            (try_begin),
                (lt, ":player_level", 12), 
                (store_random_in_range, ":chance", 3000, 11000),     
                (gt, ":chance", ":dist"),
                (store_random_in_range, ":long_skretch", 0,2),
                (try_begin), 
                    (ge,":player_mount",0), 
                    (agent_set_animation, ":player_mount", "anim_horse_rear"), 
                    (agent_set_animation, ":player_agent", "anim_nazgul_noooo_mounted_short"), 
                (else_try), 
                    (ge,":long_skretch",1),
                    (agent_set_animation, ":player_agent", "anim_nazgul_noooo_long"),
                (else_try), 
                    (agent_set_animation, ":player_agent", "anim_nazgul_noooo_short"),
                (try_end),
                (agent_deliver_damage_to_agent, ":player_agent", ":player_agent", 30),
                (val_div, ":chance", 2),
                (gt, ":chance", ":dist"),
                (try_begin),
                    (ge,":long_skretch",1),
                    (agent_play_sound, ":player_agent", "snd_nazgul_skreech_long" ),
                (else_try),
                    (agent_play_sound, ":player_agent", "snd_nazgul_skreech_short"),
                (try_end),
                (display_message, "@You are unable to endure the horrors of the Dead City."),
            (else_try),
                (lt, ":dist", 3000),
                (ge, ":player_level", 12),
                (store_random_in_range, ":chance", 0, 100),
                (lt, ":chance", 15), #so it doesn't happen immediatly
                (display_message, "@You endure the horrors of the Dead City and explore its innermost circles. The Silent Watchers recognise your valour and don't oppose you. (You gained 1 Charisma.)"),
                (add_xp_as_reward, 500),
                (call_script, "script_change_player_relation_with_center", "$current_town", 10),
                (call_script, "script_increase_rank", "$ambient_faction", 20),
                (troop_raise_attribute, "trp_player", ca_charisma, 1),
                (scene_prop_set_slot, ":instance_no", scene_prop_open_or_close_slot, 1), #used
                (party_set_slot, "$current_town", slot_exploration_point_2, 1),         
            (try_end),
            
        (else_try), #Rhun temple 
            (eq, ":scene", scn_north_rhun_camp_center),
            (eq, ":var1", 1),
            (neg|party_slot_eq, "$current_town", slot_exploration_point_1, 1),
            (lt, ":dist", 3000),
            (try_begin),          
                (lt, ":player_level", 8),
                (store_random_in_range, ":chance", 0, 4500),
                (assign, reg77, ":chance"),          
                (lt, ":chance", ":dist"),
                (agent_get_animation, ":cur_animation", ":player_agent", 1),
                (neq, ":cur_animation", "anim_nazgul_noooo_long"),
                (agent_set_animation, ":player_agent", "anim_nazgul_noooo_long"),
                (val_mul, ":chance", 2),
                (lt, ":chance", ":dist"),
                (agent_stop_sound, ":player_agent"),
                (play_sound_at_position ,"snd_horror_scream_man", pos5),            
                (display_message, "@You are unable to endure the horrors of the temple."),
            (else_try),
                (lt, ":dist", 1000),
                (ge, ":player_level", 8),
                (display_message, "@You endure the horrors of the unspeakable rituals in this sacred place. The cruel people of Rhun recognise the strength you have shown and some of their mightiest decide to join your party."),
                (agent_set_animation, ":player_agent", "anim_cheer"),
                (call_script, "script_troop_get_cheer_sound", "trp_player"),
                (ge, reg1, 0),
                (agent_play_sound, ":player_agent", reg1),            
                (add_xp_as_reward, 500),
                (call_script, "script_change_player_relation_with_center", "$current_town", 10),
                (call_script, "script_increase_rank", "$ambient_faction", 16),
                (party_force_add_members, "p_main_party", "trp_c6_rhun_warlord", 5),
                (scene_prop_set_slot, ":instance_no", scene_prop_open_or_close_slot, 1), #used
                (party_set_slot, "$current_town", slot_exploration_point_1, 1),
            (try_end),

        (else_try),
            (eq, ":scene", scn_gundabad_camp_center),
            (eq, ":var1", 1),
            (try_begin),
              (eq, "$temp_2", 0),
              (set_spawn_position, pos5),
              (spawn_scene_prop, "spr_moon_beam"),
              (assign, "$temp_2", 1),
            (try_end),            
            (neg|party_slot_eq, "$current_town", slot_exploration_point_1, 1),
            (lt, ":dist", 500),
            (try_begin),
                (lt, ":rank", 4),
                (display_message, "@You find yourself in a deep cavern. Your hackles rise as you look around you, and you begin to feel a strange sense of danger. This is no place for one such as you. Snarling, you make your retreat. When the Shadow has covered the world above, perhaps then, you may return here without fear..."),
                (agent_deliver_damage_to_agent, ":player_agent", ":player_agent", 30),
            (else_try),
                (ge, ":rank", 4),
                (display_message, "@You find yourself in a deep cavern. Your hackles rise as you look around you, and you begin to feel a strange sense of danger. Raising your weapon high, you snarl your defiance at the unseen foe in this place. This may have been a place of wonder once... but now, with the true power you have gained, you realize you have nothing to fear from the forgotten past of a broken world."),                
                (add_xp_as_reward, 800),
                (call_script, "script_change_player_party_morale", 35),
                (call_script, "script_change_player_relation_with_center", "$current_town", 3),
                (troop_raise_attribute, "trp_player", ca_charisma, 1),
                (party_set_slot, "$current_town", slot_exploration_point_1, 1),
            (try_end),
            (scene_prop_set_slot, ":instance_no", scene_prop_open_or_close_slot, 1), #used  

        (else_try),
            (eq, ":scene", scn_caras_galadhon_center),
            (eq, ":var1", 1),
            (try_begin),
              (eq, "$temp_2", 0),
              (is_currently_night),
              (position_move_z, pos5, 25),
              (set_spawn_position, pos5),
              (spawn_scene_prop, "spr_moon_beam"),
              (spawn_scene_prop, "spr_moon_beam"),
              (spawn_scene_prop, "spr_moon_sparks"),
              (assign, "$temp_2", 1),
            (try_end),            
            (lt, ":dist", 400),
            (troop_get_slot, ":galadriel_relation", "trp_lorien_lord", slot_troop_player_relation),
            (try_begin),
                (is_currently_night),
                (ge, ":galadriel_relation", 40),
                (neg|party_slot_eq, "$current_town", slot_exploration_point_1, 1),
                (store_random_in_range, ":chance", 0, 100),
                (lt, ":chance", 20), #so it doesn't happen immediatly                   
                (display_message, "@With trepidation, you look within the silver basin. The water shows you visions of horror; blood and terror and grief. You recoil... but then, the visions vanish and you see instead a clear night sky, with what seems to be a silver boat floating across the expanse. A sense of calm washes over you. Hope is not wholly gone."),
                (add_xp_as_reward, 1500),
                (troop_raise_attribute, "trp_player", ca_intelligence, 1),
                (call_script, "script_change_player_party_morale", 50),
                (party_set_slot, "$current_town", slot_exploration_point_1, 1),
                (scene_prop_set_slot, ":instance_no", scene_prop_open_or_close_slot, 1), #used
                (play_sound, "snd_elf_song"),
            (else_try),
                (neg|is_currently_night),
                (store_random_in_range, ":chance", 0, 100),
                (lt, ":chance", 20), #so it doesn't happen immediatly   
                (display_message, "@The Lady's garden lies peacefully in the bright daylight. You sense nothing out of the ordinary..."),
            (try_end),

        (else_try),
            (eq, ":scene", scn_edoras_center),
            (eq, ":var1", 1),            
            (lt, ":dist", 2000),
            #(eq, ":player_mount", -1),
            (neg|party_slot_eq, "$current_town", slot_exploration_point_1, 1),
            (store_random_in_range, ":chance", 0, 100),
            (lt, ":chance", 20), #so it doesn't happen immediatly            
            (try_begin),
                (ge, ":rank", 4),
                (display_message, "@You kneel to pay your respects to the fallen rulers of this fair realm. Beside you, a shield-maiden of Rohan raises her voice in song. Ne sceal hearpan sweg wigend weccean; ne winfaet gylden guma sceal healdan! Your heart aches to hear her words."),
                (add_xp_as_reward, 500),
                (call_script, "script_change_player_relation_with_center", "$current_town", 3),
                (call_script, "script_increase_rank", "$ambient_faction", 20),
                (party_set_slot, "$current_town", slot_exploration_point_1, 1),
                (scene_prop_set_slot, ":instance_no", scene_prop_open_or_close_slot, 1), #used
            (else_try),
                (lt, ":rank", 4),
                (call_script, "script_get_rank_title_to_s24", "$ambient_faction"),
                (display_message, "@You wonder about the two rows of burial mounds in front of the gates, yet as a mere {s24}, you do not understand their significance."),
            (try_end),
        (try_end),    
    (try_end),

    (try_for_prop_instances, ":instance_no", "spr_secret_guardian"), #guardians, can also be used for persons of interest, very nice!
        (prop_instance_get_variation_id, ":var1", ":instance_no"),
        (prop_instance_get_position, pos5, ":instance_no"),
        (get_distance_between_positions, ":dist", pos4, pos5),
        (assign, ":speak_dist", 0),
        (assign, ":rank_req", 0),
        
        #debug
        # (assign, reg78, ":dist"),
        # (assign, reg77, ":instance_no"),
        # (display_message, "@POI {reg77} distance {reg78}"),
        
        (str_store_string, s1, "@Halt! You are not allowed to enter here!"),
        
        (try_begin),
            (eq, ":scene", scn_minas_tirith_center),
            (eq, ":var1", 1),
            (party_slot_eq, "$current_town", slot_exploration_point_1, 0),
            (assign, ":rank_req", 4),
            (assign, ":speak_dist", 500),
        (else_try),
            (eq, ":scene", scn_caras_galadhon_center),
            (eq, ":var1", 1),
            (party_slot_eq, "$current_town", slot_exploration_point_1, 0),
            (troop_get_slot, ":rank", "trp_lorien_lord", slot_troop_player_relation),
            (assign, ":rank_req", 40),
            (assign, ":speak_dist", 500),
            (str_store_string, s1, "@Halt! You are not allowed to enter here without the Lady's leave!"),
        (try_end), 

        (scene_prop_get_slot, ":agent", ":instance_no", slot_prop_agent_1),
        (neg|agent_slot_eq, ":agent", slot_agent_secret_guardian, 0),

        (try_begin), #spawn barrier
            (agent_slot_eq, ":agent", slot_agent_assigned_prop, 0),
            (position_rotate_z, pos5, 180),
            (set_spawn_position, pos5),
            (spawn_scene_prop, "spr_barrier_8m"),
            (agent_set_slot, ":agent", slot_agent_assigned_prop, reg0),
        (try_end),

        (lt, ":dist", ":speak_dist"),
        (try_begin),
            (lt, ":rank", ":rank_req"),
            (agent_set_slot, ":agent", slot_agent_secret_guardian, 1), #used for tracking guardian status
        (else_try),
            (agent_set_slot, ":agent", slot_agent_secret_guardian, -1), #let player pass
        (try_end),

        (agent_get_troop_id, ":troop_no", ":agent"),
        (assign, "$temp", ":agent"), #very absurd workaround to make sure that it always catches the right agent for dialog window
        (assign, "$talk_context", tc_castle_gate),
        
        (start_mission_conversation, ":troop_no"),
    (try_end),    
    ]),

  # #spawn guardians
  # (ti_after_mission_start, 1, ti_once, [], [ 
    # (store_current_scene, ":scene"),
    # (try_for_prop_instances, ":instance_no", "spr_secret_guardian"), #guardians, can also be used for persons of interest, very nice!
        # (prop_instance_get_variation_id, ":var1", ":instance_no"),
        
        # (try_begin),
            # (eq, ":scene", scn_minas_tirith_center),
            # (eq, ":var1", 2), 
            # (assign, ":troop", trp_i6_gon_tower_swordsman),
        # (else_try),
            # (eq, ":scene", scn_caras_galadhon_center),
            # (eq, ":var1", 0), 
            # (assign, ":troop", trp_i6_gon_tower_swordsman),
        # (try_end),

        # (gt, ":troop", 0),
        # (prop_instance_get_position, pos5, ":instance_no"),
        # (set_spawn_position, pos5),
        # (spawn_agent, ":troop"),
        # (assign, ":agent", reg0),
        # (scene_prop_set_slot, ":instance_no", slot_prop_agent_1, ":agent"),
        # (agent_set_slot, ":agent", slot_agent_secret_guardian, 1),
        # (position_rotate_z, pos5, 180),
        # (set_spawn_position, pos5),
        # (spawn_scene_prop, "spr_barrier_8m"),
        # (agent_set_slot, ":agent", slot_agent_assigned_prop, reg0),
    # (try_end), 
      # ]),    
]