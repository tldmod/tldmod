## MadVader deathcam begin
common_init_deathcam = (
   0, 0, ti_once,
   [
(eq, "$g_dplmc_battle_continuation", 0),
   (main_hero_fallen),
   (eq, "$g_dplmc_cam_activated", 1),
       ],
   [
      (assign, "$pop_camera_on", 0),
      # mouse center coordinates (non-windowed)
      (assign, "$pop_camera_mouse_center_x", 500),
      (assign, "$pop_camera_mouse_center_y", 375),
      # last recorded mouse coordinates
      (assign, "$pop_camera_mouse_x", "$pop_camera_mouse_center_x"),
      (assign, "$pop_camera_mouse_y", "$pop_camera_mouse_center_y"),
      # counts how many cycles the mouse stays in the same position, to determine new center in windowed mode
      (assign, "$pop_camera_mouse_counter", 0),
   ]
)

common_start_deathcam = (
   0, 4, ti_once, # 4 seconds delay before the camera activates
   [
(eq, "$g_dplmc_battle_continuation", 0),
     (main_hero_fallen),
   (eq, "$g_dplmc_cam_activated", 1),
   (eq, "$pop_camera_on", 0),
   ],
   [
      (get_player_agent_no, ":player_agent"),
      (agent_get_position, pos1, ":player_agent"),
      (position_get_x, ":pos_x", pos1),
      (position_get_y, ":pos_y", pos1),
      (init_position, pos47),
      (position_set_x, pos47, ":pos_x"),
      (position_set_y, pos47, ":pos_y"),
      (position_set_z_to_ground_level, pos47),
      (position_move_z, pos47, 250),
      (mission_cam_set_mode, 1, 0, 0),
      (mission_cam_set_position, pos47),
      (assign, "$pop_camera_rotx", 0),
      (assign, "$pop_camera_on", 1),
   ]
)

common_move_deathcam = (
   0, 0, 0,
   [
      (eq, "$pop_camera_on", 1),
      (this_or_next|game_key_clicked, gk_move_forward),
      (this_or_next|game_key_is_down, gk_move_forward),
      (this_or_next|game_key_clicked, gk_move_backward),
      (this_or_next|game_key_is_down, gk_move_backward),
      (this_or_next|game_key_clicked, gk_move_left),
      (this_or_next|game_key_is_down, gk_move_left),
      (this_or_next|game_key_clicked, gk_move_right),
      (game_key_is_down, gk_move_right),
   ],
   [
      (mission_cam_get_position, pos47),
      (assign, ":move_x", 0),
      (assign, ":move_y", 0),
      (try_begin), #forward
        (this_or_next|game_key_clicked, gk_move_forward),
        (game_key_is_down, gk_move_forward),
        (assign, ":move_y", 10),
      (try_end),
      (try_begin), #backward
        (this_or_next|game_key_clicked, gk_move_backward),
        (game_key_is_down, gk_move_backward),
        (assign, ":move_y", -10),
      (try_end),
      (try_begin), #left
        (this_or_next|game_key_clicked, gk_move_left),
        (game_key_is_down, gk_move_left),
        (assign, ":move_x", -10),
      (try_end),
      (try_begin), #right
        (this_or_next|game_key_clicked, gk_move_right),
        (game_key_is_down, gk_move_right),
        (assign, ":move_x", 10),
      (try_end),
      (position_move_x, pos47, ":move_x"),
      (position_move_y, pos47, ":move_y"),
      (mission_cam_set_position, pos47),     
   ]
)

deathcam_mouse_deadzone = 2 #set this to a positive number (MV: 2 or 3 works well for me, but needs testing on other people's PCs)

common_rotate_deathcam = (
   0, 0, 0,
   [
      (eq, "$pop_camera_on", 1),
      (neg|is_presentation_active, "prsnt_battle"),
      (mouse_get_position, pos1),
      (set_fixed_point_multiplier, 1000),
      (position_get_x, reg1, pos1),
      (position_get_y, reg2, pos1),
      (this_or_next|neq, reg1, "$pop_camera_mouse_center_x"),
      (neq, reg2, "$pop_camera_mouse_center_y"),
   ],
   [
      # fix for windowed mode: recenter the mouse
      (assign, ":continue", 1),
      (try_begin),
        (eq, reg1, "$pop_camera_mouse_x"),
        (eq, reg2, "$pop_camera_mouse_y"),
        (val_add, "$pop_camera_mouse_counter", 1),
        (try_begin), #hackery: if the mouse hasn't moved for X cycles, recenter it
          (gt, "$pop_camera_mouse_counter", 50),
          (assign, "$pop_camera_mouse_center_x", reg1),
          (assign, "$pop_camera_mouse_center_y", reg2),
          (assign, "$pop_camera_mouse_counter", 0),
        (try_end),
        (assign, ":continue", 0),
      (try_end),
      (eq, ":continue", 1), #continue only if mouse has moved
      (assign, "$pop_camera_mouse_counter", 0), # reset recentering hackery
     
      # update recorded mouse position
      (assign, "$pop_camera_mouse_x", reg1),
      (assign, "$pop_camera_mouse_y", reg2),
     
      (mission_cam_get_position, pos47),
      (store_sub, ":shift", "$pop_camera_mouse_center_x", reg1), #horizontal shift for pass 0
      (store_sub, ":shift_vertical", reg2, "$pop_camera_mouse_center_y"), #for pass 1
     
      (try_for_range, ":pass", 0, 2), #pass 0: check mouse x movement (left/right), pass 1: check mouse y movement (up/down)
        (try_begin),
          (eq, ":pass", 1),
          (assign, ":shift", ":shift_vertical"), #get ready for the second pass
        (try_end),
        (this_or_next|lt, ":shift", -deathcam_mouse_deadzone), #skip pass if not needed (mouse deadzone)
        (gt, ":shift", deathcam_mouse_deadzone),
       
        (assign, ":sign", 1),
        (try_begin),
          (lt, ":shift", 0),
          (assign, ":sign", -1),
        (try_end),
        # square root calc
        (val_abs, ":shift"),
        (val_sub, ":shift", deathcam_mouse_deadzone), # ":shift" is now 1 or greater
        (convert_to_fixed_point, ":shift"),
        (store_sqrt, ":shift", ":shift"),
        (convert_from_fixed_point, ":shift"),
        (val_clamp, ":shift", 1, 6), #limit rotation speed
        (val_mul, ":shift", ":sign"),
        (try_begin),
          (eq, ":pass", 0), # rotate around z (left/right)
          (store_mul, ":minusrotx", "$pop_camera_rotx", -1),
          (position_rotate_x, pos47, ":minusrotx"), #needed so camera yaw won't change
          (position_rotate_z, pos47, ":shift"),
          (position_rotate_x, pos47, "$pop_camera_rotx"), #needed so camera yaw won't change
        (try_end),
        (try_begin),
          (eq, ":pass", 1), # rotate around x (up/down)
          (position_rotate_x, pos47, ":shift"),
          (val_add, "$pop_camera_rotx", ":shift"),
        (try_end),
      (try_end), #try_for_range ":pass"
      (mission_cam_set_position, pos47),
   ]
)
## MadVader deathcam end